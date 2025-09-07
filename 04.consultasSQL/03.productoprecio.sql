USE [DatacrafterDB];
GO
SELECT 
    p.product_id,
    p.product_name,
    dv.precio_unitario
FROM productos p
JOIN detalle_ventas dv ON p.product_id = dv.product_id;
