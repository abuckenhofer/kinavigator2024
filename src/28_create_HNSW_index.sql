DROP INDEX IF EXISTS music_ivf;
DROP INDEX IF EXISTS music_hnsw;

CREATE INDEX music_hnsw ON music 
       USING hnsw (songVector vector_cosine_ops);
