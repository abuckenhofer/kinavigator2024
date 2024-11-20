DROP INDEX IF EXISTS music_ivf;
DROP INDEX IF EXISTS music_hnsw;

CREATE INDEX music_ivf ON music 
       USING ivfflat (songVector vector_cosine_ops) 
       WITH (lists = 10);

