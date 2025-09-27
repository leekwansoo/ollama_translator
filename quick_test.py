import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('LLAMA_CLOUD_API_KEY')
print(f"API Key: {key[:20]}..." if key else "No API key found")

endpoints = [
    'https://api.llama-api.com/v1/models',
    'https://api.llama-api.com/chat/completions', 
    'https://api.aimlapi.com/v1/models',
    'https://api.aimlapi.com/v1/chat/completions'
]

for ep in endpoints:
    try:
        r = requests.get(ep, headers={'Authorization': f'Bearer {key}'}, timeout=5)
        print(f'{ep}: {r.status_code}')
    except Exception as e:
        print(f'{ep}: ERROR - {e}')