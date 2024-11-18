import os
from dotenv import load_dotenv
from openai import OpenAI

# .env-Datei aus übergeordnetem Verzeichnis laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# OpenAI API-Schlüssel sicher laden
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise EnvironmentError("OPENAI_API_KEY ist nicht in der .env-Datei gesetzt.")

client = OpenAI()

prompt = "Who is the US president in 2024?"

# Make the API call passing the prompt to the LLM
response = client.chat.completions.create(
  model="gpt-4o",
  messages=	[
    {"role": "user", "content": prompt}
  		]
)

# Extract the answer from the response object
answer=response.choices[0].message.content

print("question: ", prompt)
print("answer: ", answer)


