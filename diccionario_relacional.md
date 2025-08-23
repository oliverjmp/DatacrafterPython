📘 Diccionario Relacional
Este documento describe la estructura relacional de la base de datos simulada para la cadena de tiendas. Incluye las claves primarias y foráneas que conectan las distintas entidades del sistema.

🔑 Claves Primarias
Tabla	Clave Primaria	Ejemplo de valor
clientes.csv	client_id	CL-00001
productos.csv	product_id	P-00001
proveedores.csv	provider_id	PR-00001
sucursales.csv	branch_id	BR-00001
Empleados.csv	employee_id	E-000001
ventas.csv	purchase_id	C-000001
detalle_ventas.csv	(compuesto)	purchase_id + product_id
inventario.csv	inventory_id	I-000001
entregas.csv	entrega_id	ET-00001
devoluciones.csv	devolucion_id	DV-00001
reseñas.csv	reseña_id	RS-00001
fidelizacion.csv	fidelizacion_id	FD-00001
compras_proveedor.csv	order_id	O-000001
pagos_proveedor.csv	pago_id	PP-000001
🔗 Claves Foráneas
Tabla	Clave Foránea	Referencia a…
ventas.csv	client_id	clientes.csv
branch_id	sucursales.csv
employee_id	Empleados.csv
detalle_ventas.csv	purchase_id	ventas.csv
product_id	productos.csv
inventario.csv	product_id	productos.csv
branch_id	sucursales.csv
entregas.csv	venta_id	ventas.csv
devoluciones.csv	venta_id	ventas.csv
product_id	productos.csv
provider_id	proveedores.csv
branch_id	sucursales.csv
employee_id	Empleados.csv
reseñas.csv	venta_id	ventas.csv
client_id	clientes.csv
fidelizacion.csv	client_id	clientes.csv
compras_proveedor.csv	provider_id	proveedores.csv
product_id	productos.csv
branch_id	sucursales.csv
pagos_proveedor.csv	order_id	compras_proveedor.csv
provider_id	proveedores.csv
📌 Recomendaciones
Todas las claves primarias deben ser únicas y consistentes.

Las claves foráneas deben validarse contra sus tablas de referencia para evitar registros huérfanos.

Se recomienda documentar estas relaciones en el modelo físico si se migra a una base de datos SQL.
