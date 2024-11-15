# RAG demo for KI-Navigator 2024

## Prerequisites 
Python must be installed.

A PostgreSQL database with installed pg_vector exists. Follow [installation description](https://github.com/pgvector/pgvector) or use a pgvector-ready docker container, e.g.

docker run -d -e POSTGRES_PASSWORD=... --name pgvector pgvector/pgvector:pg16

docker exec -it pgvector bash

Now the PostgreSQL command shell can be started: psql -U postgres 

Create a .env file with entries:

OPENAI_API_KEY=

DB_HOST=localhost

DB_NAME=

DB_USER=

DB_PASSWORD=

## Steps to run example
First, install the required Python packages with "pip install -r requirements.txt"
Then run the scripts in directory src:
- no_rag_pipeline.py will prompt a LLM for an answer
- rag_pipeline.py will prompt a LLM with augmented information. The information comes from teh vector store that must be loaded before using index_pipeline.py.

For more information on Vector databases see my personal blog, e.g. [Vector databases - what, why, and how](https://buckenhofer.com/2024/05/vector-database-what-why-and-how/).

