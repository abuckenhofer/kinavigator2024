select id
     , content
     , vector_dims(embedding) AS dimensions
     , left(embedding::text, 50) as embedding_part 
from document;
