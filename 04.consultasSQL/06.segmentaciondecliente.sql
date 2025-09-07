USE [DatacrafterDB];
GO
SELECT 
    c.client_id,
    c.name,
    COUNT(DISTINCT v.purchase_id) AS frecuencia_compra,
    SUM(dv.cantidad * dv.precio_unitario) AS gasto_total,
    COUNT(dv.product_id) AS productos_comprados
FROM clientes c
JOIN ventas v ON c.client_id = v.client_id
JOIN detalle_ventas dv ON v.purchase_id = dv.purchase_id
GROUP BY c.client_id, c.name
ORDER BY gasto_total DESC;
