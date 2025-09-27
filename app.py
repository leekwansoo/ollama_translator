import streamlit as st
import os
import sys
import warnings

# Suppress warnings and set environment variables
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Fix for compatibility issues
os.environ["OMP_NUM_THREADS"] = "1"

# Set Streamlit config to avoid file watcher issues
st.set_page_config(
    page_title="Ollama Translator",
    page_icon="🔤",
    layout="wide"
)

try:
    from langchain_ollama import ChatOllama
    from prompt import generate_prompt
    
    # Initialize the model with error handling
    @st.cache_resource
    def load_model():
        try:
            return ChatOllama(model="qwen2.5:latest")
        except Exception as e:
            st.error(f"Failed to load Ollama model: {e}")
            st.info("Please ensure Ollama is running and qwen2.5:latest model is installed")
            return None
    
    llm = load_model()
    
except Exception as e:
    st.error(f"Error importing dependencies: {e}")
    llm = None

st.title("Ollama Translator with Qwen2.5")
st.sidebar.info("This app uses the Qwen2.5 model from Ollama to translate Korean into English or edit English Text for better quality.")
version =st.sidebar.selectbox("Version", ["Short version", "Long version"])
proficiency_level =st.sidebar.selectbox("Proficiency Level", ["Beginner", "High Beginner", "Low Intermediate", "Intermediate", "High Intermediate", "Low Advanced", "Advanced", "High Advanced"])
formality =st.sidebar.selectbox("Formality", ["Casual", "Neutral", "Formal"])
confirmation = st.sidebar.selectbox("Is this correct?", ["No", "Yes"])
st.sidebar.write(f"Version: {version}")
st.sidebar.write(f"Proficiency Level: {proficiency_level}")
st.sidebar.write(f"Formality: {formality}")
# Main interface
text_input = st.text_area("Enter text to translate or edit:", height=200)

if st.button("Translate or Edit"):
    if not text_input.strip():
        st.warning("Please enter text to translate or edit.")
    elif llm is None:
        st.error("Language model is not available. Please check the error messages above.")
    else:
        try:
            with st.spinner("Processing your text..."):
                prompt = generate_prompt(text_input, version, proficiency_level, formality, confirmation)
                response = llm.invoke(prompt)
                
            st.subheader("Response:")
            st.write(response.content)
            
        except Exception as e:
            st.error(f"An error occurred while processing your text: {e}")
            st.info("Please make sure Ollama is running and the qwen2.5:latest model is available.")
            st.code(f"Error details: {str(e)}")