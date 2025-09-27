## ollama_translator

app to translate korean texts into english or edit english texts for improvements

platform :  Ollama
llm-model: qwen2.5: latest (working properly for korean texts)

program modules:    main.py
                    app.py
                    app_simple.py


# to run the cloned or downloaded package
if you don't have ollama installed on your computer:
    download ollama from "www.ollama.org" and install it
from powershell terminal,
    pull model "qwen2.5" with "ollama pull qwen2.5"
    run model with "ollama run qwen2.5"


from the terminal:
    step_1: create venv with "python -m venv venv"
    step_2: activate venv with "venv\Scripts\activate"  
    step_3: install dependencies with "pip install -r requirements.txt"
    step_4: run the streamlit_app with " streamlit run app_simple.py

Voila! "Ollama_Translator UI" will pop up on the window
