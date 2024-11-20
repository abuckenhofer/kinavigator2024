SELECT 
    artistName, 
    songName, 
    songVector <-> (SELECT songVector 
                    FROM music 
                    WHERE id = 5) AS euclidean_distance
FROM music
ORDER BY euclidean_distance
FETCH FIRST 5 ROWS ONLY;

SELECT 
    artistName, 
    songName, 
    songVector <=> (SELECT songVector 
                    FROM music 
                    WHERE id = 5) AS cosine_distance
FROM music
ORDER BY cosine_distance
FETCH FIRST 5 ROWS ONLY;