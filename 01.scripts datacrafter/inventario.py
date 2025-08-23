import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

# Cargar productos y sucursales
df_productos = pd.read_csv("02.descargable/CSV/productos.csv", encoding='utf-8-sig')
df_branches = pd.read_csv("02.descargable/CSV/sucursales.csv", encoding='utf-8-sig')

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

# Exportar inventario
def exportar_inventario(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/inventario.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/inventario.json', orient='records', lines=True, force_ascii=False),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/inventario.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        carpeta_formato = os.path.join(carpeta, nombre.split('/')[0])
        os.makedirs(carpeta_formato, exist_ok=True)
        try:
            funcion()
            print(f"✅ Inventario exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar inventario en {nombre}: {e}")

# Mostrar y exportar
print(df_inventario.head())
exportar_inventario(df_inventario)
print(f"\n✅ Se han generado y exportado {len(df_inventario)} registros de inventario con fecha de actualización.")
