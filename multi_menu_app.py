import streamlit as st
import os
import sys
import warnings
from email_prompt import generate_email_prompt

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

# Create a sidebar for navigation
st.sidebar.title("Menu")
options = st.sidebar.radio("Select an option", ["Upload File", "Translate Text", "Generate Email"])

if options == "Upload File":
    st.sidebar.info("This app uses the Qwen2.5 model from Ollama to translate Korean into English or edit English Text for better quality.")
    version =st.sidebar.selectbox("Version", ["Short version", "Long version"])
    proficiency_level =st.sidebar.selectbox("Proficiency Level", ["Beginner", "High Beginner", "Low Intermediate", "Intermediate", "High Intermediate", "Low Advanced", "Advanced", "High Advanced"])
    formality =st.sidebar.selectbox("Formality", ["Casual", "Neutral", "Formal"])
    confirmation = st.sidebar.selectbox("Is this correct?", ["No", "Yes"])
    st.sidebar.write(f"Version: {version}")
    st.sidebar.write(f"Proficiency Level: {proficiency_level}")
    st.sidebar.write(f"Formality: {formality}")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
    if uploaded_file:
        file_type = uploaded_file.name.split('.')[1]
        if file_type == "txt":
            file_content = uploaded_file.read().decode("utf-8")
            text_input = st.text_area("File Content", file_content, height=300)
            
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
                    
        elif file_type == "pdf":
            # Process PDF file
            st.text("PDF file uploaded successfully!")
        elif file_type == "docx":
            # Process DOCX file
            st.text("DOCX file uploaded successfully!")
            
elif options == "Translate Text":
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

# Email Generation
elif options == "Generate Email":
    email_subject = st.text_input("Email Subject:")
    email_recipient = st.text_input("Email Recipient:")
    email_body = st.text_area("Email Body:", height=200)
    if st.button("Generate Email"):
        if not email_subject or not email_body:
            st.warning("Please enter both subject and body for the email.")
        elif llm is None:
            st.error("Language model is not available. Please check the error messages above.")
        else:
            try:
                with st.spinner("Generating email..."):
                    prompt = generate_email_prompt(email_subject, email_recipient, email_body)
                    response = llm.invoke(prompt)

                st.subheader("Generated Email:")
                st.write(f"Subject: {email_subject}")
                st.write(f"Body: {response.content}")

            except Exception as e:
                st.error(f"An error occurred while generating the email: {e}")
                st.info("Please make sure Ollama is running and the qwen2.5:latest model is available.")
                st.code(f"Error details: {str(e)}")

# End of app.py