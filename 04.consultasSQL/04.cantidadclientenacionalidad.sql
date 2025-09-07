USE [DatacrafterDB];
GO
SELECT country, COUNT(*) AS total_clientes
FROM clientes
GROUP BY country
ORDER BY total_clientes DESC;