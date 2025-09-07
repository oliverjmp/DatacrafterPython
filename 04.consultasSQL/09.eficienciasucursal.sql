USE [DatacrafterDB];
GO
SELECT s.branch_id, s.country,
       COUNT(DISTINCT v.purchase_id) AS ventas,
       SUM(dv.cantidad * dv.precio_unitario) AS ingresos,
       COUNT(DISTINCT d.devolucion_id) AS devoluciones,
       CAST(COUNT(DISTINCT d.devolucion_id) AS FLOAT) / NULLIF(COUNT(DISTINCT v.purchase_id), 0) AS tasa_devolucion
FROM sucursales s
LEFT JOIN ventas v ON s.branch_id = v.branch_id
LEFT JOIN detalle_ventas dv ON v.purchase_id = dv.purchase_id
LEFT JOIN devoluciones d ON v.purchase_id = d.venta_id
GROUP BY s.branch_id, s.country;
