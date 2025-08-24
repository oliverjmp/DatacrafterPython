import pandas as pd

# Cargar tablas base
df_clientes = pd.read_csv("02.descargable/CSV/clientes.csv", encoding='utf-8-sig')
df_ventas = pd.read_csv("02.descargable/CSV/ventas.csv", encoding='utf-8-sig')
df_detalle = pd.read_csv("02.descargable/CSV/detalle_ventas.csv", encoding='utf-8-sig')
df_productos = pd.read_csv("02.descargable/CSV/productos.csv", encoding='utf-8-sig')
df_devoluciones = pd.read_csv("02.descargable/CSV/devoluciones.csv", encoding='utf-8-sig')
df_entregas = pd.read_csv("02.descargable/CSV/entregas.csv", encoding='utf-8-sig')
df_inventario = pd.read_csv("02.descargable/CSV/inventario.csv", encoding='utf-8-sig')
df_reseñas = pd.read_csv("02.descargable/CSV/reseñas.csv", encoding='utf-8-sig')
df_fidelizacion = pd.read_csv("02.descargable/CSV/fidelizacion.csv", encoding='utf-8-sig')

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

# Validaciones de claves foráneas
validar_foraneas(df_ventas, "client_id", df_clientes, "client_id")
validar_foraneas(df_detalle, "product_id", df_productos, "product_id")
validar_foraneas(df_devoluciones, "product_id", df_productos, "product_id")
validar_foraneas(df_devoluciones, "entrega_id", df_entregas, "entrega_id")
validar_foraneas(df_reseñas, "client_id", df_clientes, "client_id")
validar_foraneas(df_fidelizacion, "client_id", df_clientes, "client_id")
validar_foraneas(df_detalle, "product_id", df_inventario, "product_id")

# Validación de ventas sin detalle
ventas_sin_detalle = ~df_ventas["purchase_id"].isin(df_detalle["purchase_id"])
print(f"⚠️ Ventas sin detalle: {ventas_sin_detalle.sum()}")

# Validación de productos vendidos que no están en inventario
productos_vendidos = df_detalle["product_id"].unique()
productos_inventario = df_inventario["product_id"].unique()
faltantes = set(productos_vendidos) - set(productos_inventario)
print(f"⚠️ Productos vendidos sin inventario registrado: {len(faltantes)}")

print("\n✅ Validación completada.")

