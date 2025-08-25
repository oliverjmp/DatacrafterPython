import pandas as pd

# Cargar tablas base
df_clientes = pd.read_csv("02.descargable/CSV/01.CSV correctos/clientes.csv", encoding='utf-8-sig')
df_ventas = pd.read_csv("02.descargable/CSV/01.CSV correctos/ventas.csv", encoding='utf-8-sig')
df_detalle = pd.read_csv("02.descargable/CSV/01.CSV correctos/detalle_ventas.csv", encoding='utf-8-sig')
df_productos = pd.read_csv("02.descargable/CSV/01.CSV correctos/productos.csv", encoding='utf-8-sig')
df_devoluciones = pd.read_csv("02.descargable/CSV/01.CSV correctos/devoluciones.csv", encoding='utf-8-sig')
df_entregas = pd.read_csv("02.descargable/CSV/01.CSV correctos/entregas.csv", encoding='utf-8-sig')
df_inventario = pd.read_csv("02.descargable/CSV/01.CSV correctos/inventario.csv", encoding='utf-8-sig')
df_reseñas = pd.read_csv("02.descargable/CSV/01.CSV correctos/reseñas.csv", encoding='utf-8-sig')
df_fidelizacion = pd.read_csv("02.descargable/CSV/01.CSV correctos/fidelizacion.csv", encoding='utf-8-sig')
df_providers = pd.read_csv("02.descargable/CSV/01.CSV correctos/proveedores.csv", encoding='utf-8-sig')
df_branches = pd.read_csv("02.descargable/CSV/01.CSV correctos/sucursales.csv", encoding='utf-8-sig')
df_empleados = pd.read_csv("02.descargable/CSV/01.CSV correctos/empleados.csv", encoding='utf-8-sig')
df_pagos_proveedor = pd.read_csv("02.descargable/CSV/01.CSV correctos/pagos_proveedor.csv", encoding='utf-8-sig')
df_cobros_ventas = pd.read_csv("02.descargable/CSV/01.CSV correctos/cobros.csv", encoding='utf-8-sig')
df_ordenes_compras = pd.read_csv("02.descargable/CSV/01.CSV correctos/compras_proveedor.csv", encoding='utf-8-sig')
df_alertas = pd.read_csv("02.descargable/CSV/01.CSV correctos/alertas_stock.csv", encoding='utf-8-sig')

# Cargar tablas erróneas
df_clientes_erroneos = pd.read_csv("02.descargable/CSV/02.CSV con errores/clientesError.csv", encoding='utf-8-sig')
df_cobros_erroneos = pd.read_csv("02.descargable/CSV/02.CSV con errores/cobrosVentasError.csv", encoding='utf-8-sig')
df_inventario_erroneo = pd.read_csv("02.descargable/CSV/02.CSV con errores/inventarioError.csv", encoding='utf-8-sig')
df_ventas_erroneas = pd.read_csv("02.descargable/CSV/02.CSV con errores/ventasError.csv", encoding='utf-8-sig')


# Función para validar duplicados
def validar_duplicados(df, clave):
    duplicados = df.duplicated(subset=clave).sum()
    if duplicados > 0:
        print(f"⚠️ Duplicados en {clave}: {duplicados}")
    else:
        print(f"✅ Sin duplicados en {clave}")

# Función para validar claves foráneas
def validar_foraneas(df_origen, campo, df_destino, clave):
    inconsistencias = ~df_origen[campo].isin(df_destino[clave])
    if inconsistencias.sum() > 0:
        print(f"⚠️ {inconsistencias.sum()} registros con {campo} no válido en {clave}")
    else:
        print(f"✅ Todos los {campo} existen en {clave}")

# Validaciones de duplicados
validar_duplicados(df_clientes, "client_id")
validar_duplicados(df_ventas, "purchase_id")
validar_duplicados(df_detalle, ["purchase_id", "product_id"])
validar_duplicados(df_devoluciones, "devolucion_id")
validar_duplicados(df_entregas, "entrega_id")
validar_duplicados(df_reseñas, "reseña_id")
validar_duplicados(df_fidelizacion, "fidelizacion_id")
validar_duplicados(df_productos, "product_id")
validar_duplicados(df_inventario, "product_id")
validar_duplicados(df_providers, "provider_id")
validar_duplicados(df_branches, "branch_id")
validar_duplicados(df_empleados, "employee_id")
validar_duplicados(df_pagos_proveedor, "pago_id")
validar_duplicados(df_cobros_ventas, "cobro_id")
validar_duplicados(df_ordenes_compras, "order_proveedor_id")
validar_duplicados(df_alertas, "alerta_id")

# Validaciones de claves foráneas
print("\n--- Validación de claves foráneas ---")
print("---Ventas---")
validar_foraneas(df_ventas, "client_id", df_clientes, "client_id")
print("---Detalle de Ventas")
validar_foraneas(df_detalle, "product_id", df_productos, "product_id")
validar_foraneas(df_detalle, "product_id", df_inventario, "product_id")
print("---Devoluciones---")
validar_foraneas(df_devoluciones, "product_id", df_productos, "product_id")
validar_foraneas(df_devoluciones, "entrega_id", df_entregas, "entrega_id")
print("---Reseñas---")
validar_foraneas(df_reseñas, "client_id", df_clientes, "client_id")
print("---Fidelización---")
validar_foraneas(df_fidelizacion, "client_id", df_clientes, "client_id")
print("---Pagos a Proveedores---")
validar_foraneas(df_pagos_proveedor, "provider_id", df_providers, "provider_id")
print("---Órdenes de Compras---")
validar_foraneas(df_ordenes_compras, "provider_id", df_providers, "provider_id")



# Validación de ventas sin detalle
ventas_sin_detalle = ~df_ventas["purchase_id"].isin(df_detalle["purchase_id"])
print(f"\n⚠️ Ventas sin detalle: {ventas_sin_detalle.sum()}")

# Validación de productos vendidos que no están en inventario
productos_vendidos = df_detalle["product_id"].unique()
productos_inventario = df_inventario["product_id"].unique()
faltantes = set(productos_vendidos) - set(productos_inventario)
print(f"⚠️ Productos vendidos sin inventario registrado: {len(faltantes)}")

print("\n✅ Validación completada.")

