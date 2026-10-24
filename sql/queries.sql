SELECT id, name, year, price FROM exhibits ORDER BY year DESC;
SELECT id, name, lastname FROM authors ORDER BY lastname;
SELECT id, name, price FROM exhibits WHERE price > 1000000 ORDER BY price DESC;
SELECT id, name FROM exhibits WHERE is_available = TRUE AND condition_id = 1;
SELECT e.id, e.name AS exhibit_name, a.lastname AS author_lastname, c.name AS collection_name
FROM exhibits e
JOIN authors a ON e.author_id = a.id
JOIN collections c ON e.collection_id = c.id;

SELECT e.id, e.name, e.year 
FROM exhibits e
JOIN authors a ON e.author_id = a.id
WHERE a.lastname = 'Шишкин';

SELECT COUNT(*) AS total_exhibits FROM exhibits;

SELECT SUM(price) AS total_value, AVG(price) AS average_price FROM exhibits;

SELECT c.name AS collection_name, COUNT(e.id) AS exhibits_count
FROM collections c
LEFT JOIN exhibits e ON c.id = e.collection_id
GROUP BY c.id, c.name
ORDER BY exhibits_count DESC;

SELECT c.name AS collection_name, COUNT(e.id) AS exhibits_count
FROM collections c
JOIN exhibits e ON c.id = e.collection_id
GROUP BY c.id, c.name
HAVING COUNT(e.id) > 1;

SELECT id, name FROM exhibits WHERE name LIKE '%Утро%';

SELECT id, name, price FROM exhibits 
WHERE price > (SELECT AVG(price) FROM exhibits);