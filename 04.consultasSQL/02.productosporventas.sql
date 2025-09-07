USE [DatacrafterDB];
GO
SELECT dv.purchase_id, dv.product_id, p.product_name, p.category, dv.cantidad, dv.precio_unitario
FROM detalle_ventas dv
JOIN productos p ON dv.product_id = p.product_id;
