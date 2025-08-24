import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

inventario_erroneo = []

for i in range(1, 10001):
    inventory_id = random.choice([
        f"I-{i:06d}", f"inv_{i:06d}", None if i % 50 == 0 else f"I-{i:06d}"
    ])
    product_id = random.choice([
        f"PR-{random.randint(1, 9999)}", None if i % 40 == 0 else f"PR-{random.randint(1, 9999)}"
    ])
    branch_id = f"SUC-{random.randint(1, 50)}"
    stock_actual = random.choice([
        random.randint(0, 100),
        -random.randint(1, 20),
        "cien",
        None
    ]) if i % 30 == 0 else random.randint(0, 100)
    stock_minimo = random.choice([
        random.randint(5, 20),
        None,
        stock_actual + 10 if isinstance(stock_actual, int) else 50
    ]) if i % 25 == 0 else random.randint(5, 20)

    fecha_ingreso = fake.date_between(start_date='-180d', end_date='-30d')
    fecha_actualizacion = random.choice([
        fake.date_between(start_date=fecha_ingreso, end_date='today'),
        "2026-01-01",
        None
    ]) if i % 35 == 0 else fake.date_between(start_date=fecha_ingreso, end_date='today')

    # Asignar estado con validación segura
    if isinstance(stock_actual, (int, float)) and stock_actual == 0:
        estado = "Agotado"
    elif isinstance(stock_actual, (int, float)) and isinstance(stock_minimo, (int, float)) and stock_actual <= stock_minimo:
        estado = "Bajo stock"
    else:
        estado = random.choice(["Disponible", "Agotado", "Bajo stock", "Desconocido"]) if i % 20 == 0 else "Disponible"

    inventario_erroneo.append({
        "inventory_id": inventory_id,
        "branch_id": branch_id,
        "product_id": product_id,
        "stock_actual": stock_actual,
        "stock_minimo": stock_minimo,
        "fecha_ingreso": fecha_ingreso,
        "fecha_actualizacion": fecha_actualizacion,
        "estado": estado
    })

df_inventario_erroneo = pd.DataFrame(inventario_erroneo)

# Convertir fechas a datetime64[ns] para compatibilidad
df_inventario_erroneo['fecha_ingreso'] = pd.to_datetime(df_inventario_erroneo['fecha_ingreso'], errors='coerce')
df_inventario_erroneo['fecha_actualizacion'] = pd.to_datetime(df_inventario_erroneo['fecha_actualizacion'], errors='coerce')

# Convertir stock_actual y stock_minimo a numérico
df_inventario_erroneo['stock_actual'] = pd.to_numeric(df_inventario_erroneo['stock_actual'], errors='coerce')
df_inventario_erroneo['stock_minimo'] = pd.to_numeric(df_inventario_erroneo['stock_minimo'], errors='coerce')

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Exportar en múltiples formatos
def exportar_inventario_erroneo(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/02.CSV con errores/inventarioError.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/02.JSON con errores/inventarioError.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/02.JSON con errores/inventarioError.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/02.SQL con errores/inventarioError.sql', 'InventarioError'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/02.PARQUET con errores/inventarioError.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/02.FEATHER con errores/inventarioError.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/02.XLSX con errores/inventarioError.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_inventario_erroneo.head())
exportar_inventario_erroneo(df_inventario_erroneo)
print(f"\n⚠️ Se han generado y exportado {len(df_inventario_erroneo)} registros de inventario con errores simulados.")
