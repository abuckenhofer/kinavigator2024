import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector  # Ensure this import is correct

# .env-Datei laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# API-Schlüssel und Datenbankdetails sicher aus Umgebungsvariablen laden
openai_api_key = os.getenv("OPENAI_API_KEY")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Überprüfen, ob alle erforderlichen Umgebungsvariablen gesetzt sind
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY ist nicht in der .env-Datei gesetzt.")
if not all([db_host, db_name, db_user, db_password]):
    raise EnvironmentError("Datenbankkonfigurationswerte sind nicht in der .env-Datei gesetzt.")

# SQLAlchemy-Engine erstellen
db_connection_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(db_connection_string)

# Embeddings-Instanz initialisieren
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# PGVector-Instanz mit SQLAlchemy-Engine und Embedding-Instanz erstellen
vector_store = PGVector(connection=engine, embedding_function=embeddings)

# OpenAI-Chat-LLM initialisieren
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

# Prompt-Vorlage erstellen
prompt_template = PromptTemplate(
    input_variables=["context", "prompt_text"],
    template="Antwort basierend auf den folgenden Informationen:\n\n{context}\n\nFrage: {prompt_text}"
)

# Funktion zur Ausführung der RAG-Pipeline
def run_pipeline(prompt_text):
    try:
        print("Pipeline gestartet...")
        
        # 1. Erzeuge den Embedding-Vektor für die Frage
        question_embedding = embeddings.embed_query(prompt_text)
        
        # 2. Suche relevante Dokumente in der Vektordatenbank
        results = vector_store.similarity_search(query_vector=question_embedding, k=1)
        context = results[0]["content"] if results else "Kein relevanter Kontext gefunden."
        
        # 3. Prompt generieren mit Kontext
        prompt = prompt_template.format(context=context, prompt_text=prompt_text)
        
        # 4. Die Chat-LLM-Ausführung mit dem generierten Prompt
        response = llm.invoke(prompt)
        
        print("Pipeline abgeschlossen.")
        return response.content
    except Exception as e:
        print(f"Fehler: {e}")
        return None

# Beispielaufruf
prompt = "Erkläre die Grundlagen des maschinellen Lernens."
antwort = run_pipeline(prompt)
print("Antwort:", antwort)
