import streamlit as st
import os
import warnings

# Suppress warnings and set environment variables
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set page config
st.set_page_config(
    page_title="Ollama Translator",
    page_icon="🔤",
    layout="wide"
)

def main():
    try:
        from langchain_ollama import ChatOllama
        from prompt import generate_prompt
        
        # Initialize model
        @st.cache_resource
        def load_model():
            return ChatOllama(model="qwen2.5:latest")
        
        st.title("Ollama Translator with Qwen2.5")
        st.sidebar.info("This app uses the Qwen2.5 model from Ollama to translate Korean into English or edit English Text for better quality.")
        
        # Sidebar controls
        version = st.sidebar.selectbox("Version", ["Short version", "Long version"])
        proficiency_level = st.sidebar.selectbox(
            "Proficiency Level", 
            ["Beginner", "High Beginner", "Low Intermediate", "Intermediate", 
             "High Intermediate", "Low Advanced", "Advanced", "High Advanced"]
        )
        formality = st.sidebar.selectbox("Formality", ["Casual", "Neutral", "Formal"])
        confirmation = st.sidebar.selectbox("Is this correct?", ["Yes", "No"])
        st.sidebar.write(f"Version: {version}")
        st.sidebar.write(f"Proficiency Level: {proficiency_level}")
        st.sidebar.write(f"Formality: {formality}")
        # Main interface
        text_input = st.text_area("Enter text to translate or edit:", height=200)
        
        if st.button("Translate or Edit", type="primary"):
            if not text_input.strip():
                st.warning("Please enter text to translate or edit.")
            else:
                try:
                    llm = load_model()
                    
                    with st.spinner("Processing your text..."):
                        prompt = generate_prompt(text_input, version, proficiency_level, formality, confirmation)
                        response = llm.invoke(prompt)
                    
                    st.subheader("Response:")
                    st.write(response.content)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Please ensure Ollama is running and qwen2.5:latest model is available.")
                    
                    # Debug information
                    with st.expander("Debug Information"):
                        st.code(f"Error type: {type(e).__name__}\nError details: {str(e)}")
                        
    except ImportError as e:
        st.error("Failed to import required dependencies.")
        st.info("Please install the required packages: pip install langchain-ollama streamlit")
        st.code(f"Import error: {e}")
    
    except Exception as e:
        st.error(f"Application error: {e}")

if __name__ == "__main__":
    main()