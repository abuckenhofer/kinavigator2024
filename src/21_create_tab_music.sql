CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS music;
CREATE TABLE music (
   id INTEGER PRIMARY KEY,
   artistname VARCHAR(250),
   songname VARCHAR(250),
   songvector VECTOR(4) 
);
