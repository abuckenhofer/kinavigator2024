import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from psycopg2.extras import execute_batch
import psycopg2
from langchain_openai import OpenAIEmbeddings

# .env-Datei laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# OpenAI API-Schlüssel und Datenbankkonfiguration aus Umgebungsvariablen laden
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

# Verbindung zur PostgreSQL-Datenbank herstellen
db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
connection = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

# Funktion zum Erstellen der Tabelle "documents"
def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;
            DROP TABLE IF EXISTS document;
            CREATE TABLE document (
                id SERIAL PRIMARY KEY,
                content VARCHAR(500),
                embedding VECTOR(1536)  -- Vektorlänge für OpenAI-Embeddings
            );
        """)
    connection.commit()
    print("Tabelle 'documents' erstellt oder existiert bereits.")

# Embeddings-Instanz initialisieren
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# CSV-Datei einlesen
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_directory, "input.csv")

# Überprüfen, ob die Datei existiert
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"Die Datei 'input.csv' wurde im Verzeichnis '{current_directory}' nicht gefunden.")

df = pd.read_csv(csv_file_path)

# Funktion zum Einfügen von Texten und Embeddings in Batches
def insert_documents_batch(df):
    texts = df['contents'].tolist()
    
    # Berechne Embeddings für jeden Text
    embeddings_list = [embeddings.embed_query(text) for text in texts]
    
    # Batch-Insert vorbereiten
    insert_query = "INSERT INTO document (content, embedding) VALUES (%s, %s)"
    data_to_insert = [(text, embedding) for text, embedding in zip(texts, embeddings_list)]

    with connection.cursor() as cursor:
        # Batch-Insert mit execute_batch
        execute_batch(cursor, insert_query, data_to_insert)
    connection.commit()
    print("Texte und Embeddings wurden erfolgreich in die Datenbank eingefügt.")

# Hauptprogramm
create_table()
insert_documents_batch(df)
print("Datenbankaktualisierung abgeschlossen.")

# Verbindung schließen
connection.close()
