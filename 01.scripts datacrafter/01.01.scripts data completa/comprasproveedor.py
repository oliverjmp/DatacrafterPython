import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# Cargar productos e inventario
df_productos = pd.read_csv("02.descargable/CSV/01.CSV correctos/productos.csv", encoding='utf-8-sig')
df_inventario = pd.read_csv("02.descargable/CSV/01.CSV correctos/inventario.csv", encoding='utf-8-sig')

# Crear índice rápido de productos
producto_map = df_productos.set_index("product_id")[["provider_id", "provider_name", "price"]].to_dict("index")

# Generar órdenes de compra
ordenes_compras = []
order_id_counter = 1
estados = ["Pendiente", "En tránsito", "Recibido"]

for _, row in df_inventario.iterrows():
    product_id = row["product_id"]
    branch_id = row["branch_id"]
    stock_actual = row["stock_actual"]
    stock_minimo = row["stock_minimo"]

    if stock_actual <= stock_minimo:
        proveedor = producto_map.get(product_id)
        if not proveedor or pd.isna(proveedor["provider_id"]):
            continue

        cantidad = random.randint(20, 100)
        precio_unitario = round(proveedor["price"], 2)
        total = round(cantidad * precio_unitario, 2)
        fecha_orden = fake.date_between(start_date='-60d', end_date='today')
        estado = random.choice(estados)

        ordenes_compras.append({
            "order_proveedor_id": f"O-{order_id_counter:06d}",
            "branch_id": branch_id,
            "product_id": product_id,
            "provider_id": proveedor["provider_id"],
            "provider_name": proveedor["provider_name"],
            "fecha_orden": fecha_orden,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total,
            "estado": estado
        })
        order_id_counter += 1

# Crear DataFrame
df_ordenes_compras = pd.DataFrame(ordenes_compras)

def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        # Crear tabla compras_proveedor
        f.write(f"-- Crear tabla {nombre_tabla}\n")
        f.write(f"CREATE TABLE {nombre_tabla} (\n")
        f.write("    order_proveedor_id VARCHAR(10) PRIMARY KEY,\n")
        f.write("    branch_id VARCHAR(8),\n")
        f.write("    product_id VARCHAR(8),\n")
        f.write("    provider_id VARCHAR(8),\n")
        f.write("    fecha_orden DATE,\n")
        f.write("    cantidad INT,\n")
        f.write("    precio_unitario DECIMAL(10,2),\n")
        f.write("    total DECIMAL(12,2),\n")
        f.write("    estado VARCHAR(20)\n")
        f.write(");\n\n")

        # Insertar datos
        for _, row in df.iterrows():
            columnas = ', '.join([col for col in df.columns if col != 'provider_name'])
            valores = ', '.join([f"'{str(row[col]).replace('\'', '\'\'')}'" for col in df.columns if col != 'provider_name'])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")


# Exportar
def exportar_ordenes(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df_ordenes_compras.to_csv(f'{carpeta}/CSV/01.CSV correctos/compras_proveedor.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df_ordenes_compras.to_json(f'{carpeta}/JSON/01.JSON correctos/compras_proveedor.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df_ordenes_compras.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/compras_proveedor.json', orient='table'),
        'SQL': lambda: exportar_sql(df_ordenes_compras, f'{carpeta}/SQL/01.SQL correctos/compras_proveedor.sql', 'ComprasProveedor'),
        'PARQUET': lambda: df_ordenes_compras.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/compras_proveedor.parquet', index=False),
        'FEATHER': lambda: df_ordenes_compras.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/compras_proveedor.feather'),
        'EXCEL': lambda: df_ordenes_compras.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/compras_proveedor.xlsx', index=False)
    }

   # Ejecutar exportaciones
    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_ordenes_compras.head())
exportar_ordenes(df_ordenes_compras)
print(f"\n✅ Se han generado y exportado {len(df_ordenes_compras)} órdenes de compra por proveedor.")