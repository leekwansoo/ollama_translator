import streamlit as st
import os
import warnings
import requests
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

# Set environment variables
# Suppress warnings
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.set_page_config(
    page_title="AI Translator & Editor",
    page_icon="🔤",
    layout="wide"
)

def create_system_prompt(version: str, proficiency_level: str, formality: str) -> str:
    """Create the system prompt with user preferences"""
    return f"""You are an expert English-Korean translator, editor, and language coach. 
Your role is to handle Korean and English student writing and provide fully educational, corrected, and enhanced outputs.

CURRENT SETTINGS:
- Version: {version}
- Level: {proficiency_level}
- Formality: {formality}

CORE OUTPUT RULES:

Grammar and paragraphing:
- Always correct grammar, punctuation, and style, and insert natural paragraph breaks
- Group related ideas into paragraphs; do not insert page breaks
- Keep sentence variety and cohesion appropriate to the selected level and formality

Visual Support conventions (In the "Improved English Version with Visual Support" only):
- **bold** for key verbs
- *italics* for nouns and adjectives
- [brackets] for phrasal verbs or grouped expressions
- _underlines_ for slang or idioms
- Retain all paragraph breaks from the plain version
- Apply the markers consistently across the passage

WHEN YOU RECEIVE KOREAN TEXT:

1) Original Korean Text
Display the original Korean exactly as submitted (no edits).

2) Plain Improved English Version
Produce a fluent, natural English translation that:
- Fully corrects grammar, punctuation, and style
- Inserts clear paragraph breaks at logical idea boundaries
- Adapts tone and complexity to the selected level and formality

3) Improved English Version with Visual Support
Repeat the plain improved English version and apply visual support formatting:
- **bold** for key verbs
- *italics* for nouns and adjectives
- [brackets] for phrasal verbs or grouped expressions
- _underlines_ for slang or idioms
Keep the same paragraphing as the plain version.

4) Vocabulary List from Visual Aid
List 5 to 10 high-value items pulled from the marked text.
For each item, include the English headword, Korean meaning, and a brief formality tag (Casual / Neutral / Formal).

WHEN YOU RECEIVE ENGLISH TEXT:

1) Plain Improved English Version
Rewrite and improve the student's English to enhance grammar, flow, and clarity, with proper paragraph breaks and level/formality adaptation.

2) Improved English Version with Visual Support
Repeat the improved English with the same paragraphing and apply visual support formatting:
- **bold** for key verbs
- *italics* for nouns and adjectives
- [brackets] for phrasal verbs or grouped expressions
- _underlines_ for slang or idioms"""

@st.cache_resource
def initialize_llm(provider: str, api_key: Optional[str] = None, model_name: Optional[str] = None):
    """Initialize the selected LLM provider"""
    try:
        if provider == "OpenAI":
            if not api_key:
                return None, "API key required for OpenAI"
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                openai_api_key=api_key,
                temperature=0.3
            ), None
            
        elif provider == "Anthropic":
            if not api_key:
                return None, "API key required for Anthropic"
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-3-haiku-20240307",
                anthropic_api_key=api_key,
                temperature=0.3
            ), None
            
        elif provider == "Google Gemini":
            if not api_key:
                return None, "API key required for Google Gemini"
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=api_key,
                temperature=0.3
            ), None
            
       
        elif provider == "Groq":
            if not api_key:
                return None, "API key required for Groq"
            from langchain_groq import ChatGroq
            return ChatGroq(
                model="llama-3.1-8b-instant",
                groq_api_key=api_key,
                temperature=0.3
            ), None
                               
            
    except ImportError as e:
        return None, f"Required package not installed: {e}"
    except Exception as e:
        return None, f"Error initializing {provider}: {e}"

def process_text(llm, text: str, version: str, proficiency_level: str, formality: str) -> str:
    """Process the input text with the LLM"""
    try:
        system_prompt = create_system_prompt(version, proficiency_level, formality)
        
        from langchain_core.messages import HumanMessage, SystemMessage
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text)
        ]
        
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo failed" in error_msg:
            return "🔌 **Connection Error**: Could not connect to the API endpoint. This might mean:\n\n" + \
                   "1. The service is temporarily down\n" + \
                   "2. The API endpoint URL is incorrect\n" + \
                   "3. Your internet connection has issues\n" + \
                   "4. The service is still in beta (for Ollama Cloud)\n\n" + \
                   "💡 **Try**: Switch to Groq or Together AI for reliable service."
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            return "🔑 **Authentication Error**: Invalid API key. Please check your API key and try again."
        elif "timeout" in error_msg.lower():
            return "⏱️ **Timeout Error**: The request took too long. The service might be overloaded. Try again in a moment."
        else:
            return f"❌ **Error**: {error_msg}\n\n💡 **Suggestion**: Try a different provider if the issue persists."

# Sidebar for configuration
st.sidebar.title("🔤 AI Translator & Editor")
st.sidebar.markdown("---")

# LLM Provider Selection
provider = st.sidebar.selectbox(
    "Choose LLM Provider",
    ["Groq", "OpenAI", "Anthropic", "Google Gemini"],
    help="🟢 Groq & Together AI are recommended for reliable service. LlamaAPI works with Ollama-style models."
)

# API Key input (if needed)
api_key = None
base_url = None

# Show environment variable status
env_keys = {
    
}

if provider != "Ollama (Local)":
    # Check if API key exists in environment
    env_key = env_keys.get(provider)
    if env_key:
        st.sidebar.success(f"✅ {provider} API key found in environment")
        api_key = env_key
    else:
        api_key = st.sidebar.text_input(
            f"{provider} API Key",
            type="password",
            help=f"Enter your {provider} API key. You can also add it to your .env file."
        )
    
    
# User preferences
st.sidebar.markdown("### Settings")
version = st.sidebar.selectbox("Version", ["Short version", "Long version"])
proficiency_level = st.sidebar.selectbox(
    "Proficiency Level", 
    ["Beginner", "High Beginner", "Low Intermediate", "Intermediate", 
     "High Intermediate", "Low Advanced", "Advanced", "High Advanced"]
)
formality = st.sidebar.selectbox("Formality", ["Casual", "Neutral", "Formal"])

# Display current settings
st.sidebar.markdown("### Current Settings")
st.sidebar.write(f"**Provider:** {provider}")

st.sidebar.write(f"**Version:** {version}")
st.sidebar.write(f"**Level:** {proficiency_level}")
st.sidebar.write(f"**Formality:** {formality}")

# Main interface
st.title("AI-Powered Korean-English Translator & Editor")
st.markdown("### Transform your Korean text to English or improve your English writing!")

# Instructions
with st.expander("📖 How to use"):
    st.markdown("""
    1. **Choose your LLM provider** from the sidebar
    2. **Enter API key** if using cloud providers (OpenAI, Anthropic, etc.)
    3. **Set your preferences** (version type, proficiency level, formality)
    4. **Enter text** in Korean (for translation) or English (for improvement)
    5. **Click Process** to get enhanced output with visual formatting
    
    **✅ Working Providers:**
    - **Groq**: Llama-3.1-8b (FREE tier available) ⭐ **Recommended**
    - **OpenAI**: GPT4o-mini (requires API key)
    - **Google Gemini**: Gemini-pro (requires API key)

""")

# Text input
text_input = st.text_area(
    "Enter text to translate (Korean) or edit (English):",
    height=200,
    placeholder="한국어 텍스트를 입력하면 영어로 번역하고, 영어 텍스트를 입력하면 개선해드립니다..."
)

# Process button
if st.button("🚀 Process Text", type="primary"):
    if not text_input.strip():
        st.warning("⚠️ Please enter text to process.")
    else:
        # Initialize LLM
        with st.spinner("Initializing AI model..."):
            # Get selected model for AIML API
            selected_model = None
            if provider == "AIML API (Qwen Models)" and 'aiml_model' in locals():
                selected_model = aiml_model
            
            llm, error = initialize_llm(provider, api_key, selected_model)
        
        if llm is None:
            st.error(f"❌ {error}")
            if provider != "Ollama (Local)":
                st.info("💡 Make sure you have entered a valid API key.")
        else:
            # Process text
            with st.spinner("Processing your text..."):
                result = process_text(llm, text_input, version, proficiency_level, formality)
            
            # Display results
            st.markdown("### 📝 Results")
            st.markdown(result)
            
            # Download option
            st.download_button(
                label="📄 Download Result",
                data=result,
                file_name="translation_result.txt",
                mime="text/plain"
            )

# Footer with API key information
st.markdown("---")
st.markdown("### 🔑 Getting API Keys")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Groq** ⭐ (Recommended)
    - Visit: [groq.com](https://groq.com)
    - FREE tier available
    - Very fast inference
    """)

with col2:
    st.markdown("""
    **Google Gemini**
    - Visit: [google.ai](https://google.ai)
    - Hosts Gemini models
    - Good performance/price
    """)

with col3:
    st.markdown("""
    **OpenAI**
    - Visit: [platform.openai.com](https://platform.openai.com)
    - Pay-per-use model
    - High quality results
    """)