import streamlit as st
import os
import warnings
from typing import Optional

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
def initialize_llm(provider: str, api_key: Optional[str] = None):
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
                anthropic_api_key=api_key,localhost:8501
                locallocalhost:8501
                
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
            
        elif provider == "Ollama (Local)":
            from langchain_ollama import ChatOllama
            return ChatOllama(
                model="qwen2.5:latest",
                temperature=0.3
            ), None
            
        elif provider == "Groq":
            if not api_key:
                return None, "API key required for Groq"
            from langchain_groq import ChatGroq
            return ChatGroq(
                model="qwen/qwen3-32b",
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
        return f"Error processing text: {str(e)}"

# Sidebar for configuration
st.sidebar.title("🔤 AI Translator & Editor")
st.sidebar.markdown("---")

# LLM Provider Selection
provider = st.sidebar.selectbox(
    "Choose LLM Provider",
    ["OpenAI", "Anthropic", "Google Gemini", "Groq", "Ollama (Local)"],
    help="Select your preferred AI provider. API key required for cloud providers."
)

# API Key input (if needed)
api_key = None
if provider != "Ollama (Local)":
    api_key = st.sidebar.text_input(
        f"{provider} API Key",
        type="password",
        help=f"Enter your {provider} API key. Get one from their official website."
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
    
    **Supported Providers:**
    - **OpenAI**: GPT-3.5-turbo (requires API key)
    - **Anthropic**: Claude-3-haiku (requires API key)
    - **Google Gemini**: Gemini-pro (requires API key)  
    - **Groq**: Llama3-8b (requires API key - FREE tier available)
    - **Ollama**: Local installation (no API key needed)
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
            llm, error = initialize_llm(provider, api_key)
        
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
    **OpenAI**
    - Visit: [platform.openai.com](https://platform.openai.com)
    - Pay-per-use model
    - High quality results
    """)

with col2:
    st.markdown("""
    **Groq** ⭐ (Recommended)
    - Visit: [groq.com](https://groq.com)
    - FREE tier available
    - Very fast inference
    """)

with col3:
    st.markdown("""
    **Anthropic**
    - Visit: [console.anthropic.com](https://console.anthropic.com)
    - Pay-per-use model
    - Excellent for editing
    """)