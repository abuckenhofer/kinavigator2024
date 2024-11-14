import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# .env-Datei laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# OpenAI API-Schlüssel sicher laden
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise EnvironmentError("OPENAI_API_KEY ist nicht in der .env-Datei gesetzt.")

# OpenAI-Chat-LLM initialisieren
# Verwenden Sie das Modell "gpt-3.5-turbo" oder "gpt-4" falls verfügbar
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)

# Prompt-Vorlage erstellen
prompt_template = PromptTemplate(
    input_variables=["prompt_text"],
    template="Antwort basierend auf den folgenden Informationen: {prompt_text}"
)

# Funktion zur Ausführung der Pipeline
def run_pipeline(prompt_text):
    try:
        print("Pipeline gestartet...")
        
        # Prompt generieren
        prompt = prompt_template.format(prompt_text=prompt_text)
        
        # Die Chat-LLM-Ausführung mit invoke statt eines direkten Aufrufs
        response = llm.invoke(prompt)
        
        print("Pipeline abgeschlossen.")
        return response.content
    except Exception as e:
        print(f"Fehler: {e}")
        return None

# Beispielaufruf
#prompt = "Erkläre die Grundlagen des maschinellen Lernens."
#prompt = "In welchem Unternehmen arbeitet Andreas Buckenhofer, Principal Car Data Architecture?"
prompt = "Seit wann gibt es den Mercedes-Benz EQA?"
prompt = "Seit wann gibt es den Mercedes-Benz EQZ?"
antwort = run_pipeline(prompt)
print("Antwort:", antwort)
