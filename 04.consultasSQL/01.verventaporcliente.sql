USE [DatacrafterDB];
GO
SELECT v.purchase_id, v.fecha, c.client_id, c.name
FROM ventas v
JOIN clientes c ON v.client_id = c.client_id;
