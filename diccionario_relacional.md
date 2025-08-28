# 📘 Diccionario Relacional — Cadena de Tiendas

Este documento describe la estructura relacional de la base de datos simulada para la cadena de tiendas. Incluye las claves primarias, foráneas y recomendaciones de integridad referencial, basadas en los scripts de generación, validación y simulación implementados.

---

## 🔑 Claves Primarias

| Tabla                   | Clave Primaria                  | Ejemplo de valor     |
|------------------------|----------------------------------|----------------------|
| clientes.csv           | client_id                        | CL-00001             |
| productos.csv          | product_id                       | P-00001              |
| proveedores.csv        | provider_id                      | PR-00001             |
| sucursales.csv         | branch_id                        | BR-00001             |
| empleados.csv          | employee_id                      | E-000001             |
| ventas.csv             | purchase_id                      | C-000001             |
| detalle_ventas.csv     | purchase_id + product_id         | C-000001 + P-00001   |
| inventario.csv         | inventory_id                     | I-000001             |
| entregas.csv           | entrega_id                       | ET-00001             |
| devoluciones.csv       | devolucion_id                    | DV-00001             |
| reseñas.csv            | reseña_id                        | RS-00001             |
| fidelizacion.csv       | fidelizacion_id                  | FD-00001             |
| compras_proveedor.csv  | order_proveedor_id               | O-000001             |
| pagos_proveedor.csv    | pago_id                          | PP-000001            |
| cobros.csv             | cobro_id                         | PG-00001             |
| alertas_stock.csv      | alerta_id                        | AL-00001             |

---

## 🔗 Claves Foráneas

| Tabla                   | Clave Foránea         | Referencia a…             |
|------------------------|------------------------|---------------------------|
| ventas.csv             | client_id              | clientes.csv              |
|                        | branch_id              | sucursales.csv            |
|                        | employee_id            | empleados.csv             |
| detalle_ventas.csv     | purchase_id            | ventas.csv                |
|                        | product_id             | productos.csv             |
| inventario.csv         | product_id             | productos.csv             |
|                        | branch_id              | sucursales.csv            |
| entregas.csv           | venta_id               | ventas.csv                |
| devoluciones.csv       | venta_id               | ventas.csv                |
|                        | entrega_id             | entregas.csv              |
|                        | product_id             | productos.csv             |
|                        | provider_id            | proveedores.csv           |
|                        | branch_id              | sucursales.csv            |
|                        | employee_id            | empleados.csv             |
| reseñas.csv            | venta_id               | ventas.csv                |
|                        | client_id              | clientes.csv              |
| fidelizacion.csv       | client_id              | clientes.csv              |
| compras_proveedor.csv  | provider_id            | proveedores.csv           |
|                        | product_id             | productos.csv             |
|                        | branch_id              | sucursales.csv            |
| pagos_proveedor.csv    | order_proveedor_id     | compras_proveedor.csv     |
|                        | provider_id            | proveedores.csv           |
| cobros.csv             | venta_id               | ventas.csv                |
| alertas_stock.csv      | product_id             | productos.csv             |
|                        | provider_id            | proveedores.csv           |
|                        | branch_id              | sucursales.csv            |

---

## 📌 Recomendaciones Técnicas

- Todas las claves primarias deben ser únicas, consistentes y validadas antes de inserción.
- Las claves foráneas deben respetar integridad referencial: no deben existir registros huérfanos.
- Se recomienda definir índices sobre claves foráneas para mejorar el rendimiento en consultas JOIN.
- Las claves compuestas (como en detalle_ventas.csv) deben definirse explícitamente en el modelo físico.
- Los campos derivados como prioridad, estado_pago, cumplimiento_72h, beneficios, etc., deben documentarse como parte del modelo lógico aunque no sean claves.

---

## 🧠 Validaciones Implementadas

Tu sistema incluye validaciones automáticas que refuerzan la calidad del modelo:

- Detección de duplicados en claves primarias
- Verificación de claves foráneas entre tablas
- Identificación de ventas sin detalle
- Detección de productos vendidos sin inventario
- Separación entre datos válidos y erróneos para auditoría
