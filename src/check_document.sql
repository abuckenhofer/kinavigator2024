select id
     , content
     , left(embedding::text, 50) as embedding_part 
from document;
