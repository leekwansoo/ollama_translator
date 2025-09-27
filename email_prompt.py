from email.mime import text

from prompt_toolkit import prompt
from langchain_ollama import ChatOllama

llm = ChatOllama( model="qwen2.5:latest" )

from langchain_core.prompts import ChatPromptTemplate

def generate_email_prompt(email_subject, email_recipient, email_body):
    system_prompt = f"""You are an expert email writer and language translator for korean-english.
Your role is to help users compose professional emails in English either from Korean contents or English contents.

USER SETTINGS:
- Email Subject: {email_subject}
- Email Recipient: {email_recipient}
- Email Body: {email_body}
"""

    email_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{text}")
    ])

    return email_prompt.format(text=text)




