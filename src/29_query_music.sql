-- erzwinge, dass ein Index verwendet wird
-- Aufgrund der geringen Datenmenge wird sonst kein Index verwendet
SET enable_seqscan = OFF;
SELECT 
    artistName, 
    songName, 
    songVector <=> (SELECT songVector 
                    FROM music 
                    WHERE id = 5) AS cosine_distance
FROM music
ORDER BY cosine_distance
FETCH FIRST 5 ROWS ONLY;