SELECT TOP 50
    p.product_id,
    p.product_name,
    p.category,
    s.branch_id,
    s.store_type,
    s.city,
    SUM(dv.cantidad) AS unidades_vendidas,
    AVG(dv.precio_unitario) AS precio_promedio_venta,
    MAX(v.fecha) AS ultima_venta,
    i.stock_actual AS stock_actual
FROM productos p
LEFT JOIN detalle_ventas dv ON p.product_id = dv.product_id
LEFT JOIN ventas v ON dv.purchase_id = v.purchase_id
LEFT JOIN sucursales s ON v.branch_id = s.branch_id
LEFT JOIN inventario i ON p.product_id = i.product_id AND s.branch_id = i.branch_id
GROUP BY 
    p.product_id, p.product_name, p.category,
    s.branch_id, s.store_type, s.city, i.stock_actual
HAVING 
    SUM(dv.cantidad) < 10 AND i.stock_actual > 50
ORDER BY i.stock_actual DESC;
