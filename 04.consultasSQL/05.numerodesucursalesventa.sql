USE [DatacrafterDB];
GO
SELECT 
    s.country,
    COUNT(DISTINCT s.branch_id) AS total_sucursales,
    SUM(v.total) AS total_ventas
FROM sucursales s
JOIN ventas v ON s.branch_id = v.branch_id
GROUP BY s.country
ORDER BY total_ventas DESC;

