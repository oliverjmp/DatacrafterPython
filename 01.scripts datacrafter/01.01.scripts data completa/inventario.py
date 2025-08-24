import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Cargar productos y sucursales
df_productos = pd.read_csv("02.descargable/CSV/01.CSV correctos/productos.csv", encoding='utf-8-sig')
df_branches = pd.read_csv("02.descargable/CSV/01.CSV correctos/sucursales.csv", encoding='utf-8-sig')

# Generar inventario
inventario = []
inventory_id_counter = 1

for _, row in df_productos.iterrows():
    product_id = row["product_id"]
    branch_id = row["branch_id"]

    stock_minimo = random.randint(5, 20)
    stock_actual = random.randint(0, 100)
    fecha_ingreso = fake.date_between(start_date='-180d', end_date='-30d')
    fecha_actualizacion = fake.date_between(start_date=fecha_ingreso, end_date='today')

    if stock_actual == 0:
        estado = "Agotado"
    elif stock_actual <= stock_minimo:
        estado = "Bajo stock"
    else:
        estado = "Disponible"

    inventario.append({
        "inventory_id": f"I-{inventory_id_counter:06d}",
        "branch_id": branch_id,
        "product_id": product_id,
        "stock_actual": stock_actual,
        "stock_minimo": stock_minimo,
        "fecha_ingreso": fecha_ingreso,
        "fecha_actualizacion": fecha_actualizacion,
        "estado": estado
    })
    inventory_id_counter += 1

# Crear DataFrame
df_inventario = pd.DataFrame(inventario)

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_inventario(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/inventario.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/inventario.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/inventario.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/inventario.sql', 'Inventario'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/inventario.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/inventario.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/inventario.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_inventario.head())
exportar_inventario(df_inventario)
print(f"\n✅ Se han generado y exportado {len(df_inventario)} registros de inventario con fecha de actualización.")
