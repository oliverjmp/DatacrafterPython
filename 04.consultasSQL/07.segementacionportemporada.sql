SELECT 
    YEAR(v.fecha) AS año,
    MONTH(v.fecha) AS mes,
    SUM(dv.cantidad * dv.precio_unitario) AS total_ventas
FROM ventas v
JOIN detalle_ventas dv ON v.purchase_id = dv.purchase_id
GROUP BY YEAR(v.fecha), MONTH(v.fecha)
ORDER BY año, mes;
