import os
from dotenv import load_dotenv
from openai import OpenAI, embeddings
from langchain_openai import OpenAIEmbeddings
import psycopg2


# Generate embedding for the prompt

def get_embedding(text, model="text-embedding-3-small"):
   #text = text.replace("\n", " ")
   #return client.embeddings.create(input = [text], model=model).data[0].embedding
   embeddings = OpenAIEmbeddings(api_key=openai_api_key)
   embeddings_list = embeddings.embed_query(text)

# Connect to the PostgreSQL database
def get_relevant_content(embedding):
    # Establish the connection
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    # Convert the embedding to a PostgreSQL vector-friendly format
    embedding_str = ','.join(map(str, embedding))

    # Define the SQL query to retrieve the most similar content using cosine similarity
    query = f"""
        SELECT content, embedding <=> '[{embedding_str}]'::vector AS similarity
        FROM documents
        ORDER BY similarity
        LIMIT 1;
    """
    
    try:
        # Execute the query
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
            
            if result:
                return result[0]  # Return the content
            else:
                return "No relevant content found."

    except Exception as e:
        print(f"Error querying the database: {e}")
    finally:
        # Close the connection
        conn.close()

# .env-Datei aus übergeordnetem Verzeichnis laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
if not all([db_host, db_name, db_user, db_password]):
    raise EnvironmentError("Database credentials are not set correctly in the .env file.")

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise EnvironmentError("OPENAI_API_KEY ist nicht in der .env-Datei gesetzt.")

client = OpenAI()


prompt = "Who is the US president in 2024?"

# Instantiate the embeddings object
#embeddings=OpenAIEmbeddings(model="text-embedding-3-large")

embeddings = OpenAIEmbeddings(api_key=openai_api_key)
embedding = embeddings.embed_query(prompt)

retrieved_context = get_relevant_content(embedding)
print(retrieved_context)

augmented_prompt=f"""

Given the context below answer the question.

Question: {prompt} 

Context : {retrieved_context}

Remember to answer only based on the context provided and not from any other source. 

If the question cannot be answered based on the provided context, say I don’t know.

"""

# Make the API call passing the prompt to the LLM
response = client.chat.completions.create(
  model="gpt-4o",
  messages=	[
    {"role": "user", "content": augmented_prompt}
  		]
)

# Extract the answer from the response object
answer=response.choices[0].message.content

print(answer)
