import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('02.descargable/CSV/01.CSV correctos/ventas.csv', encoding='utf-8-sig')

# Comentarios simulados
comentarios = [
    'Muy buen producto, llegó rápido.',
    'No era lo que esperaba.',
    'Excelente atención al cliente.',
    'El embalaje estaba dañado.',
    'Volveré a comprar sin duda.',
    'Precio justo y buena calidad.',
    'Tuve problemas con la entrega.',
    'Todo perfecto, gracias.',
    'La talla no era correcta.',
    'Me encantó, lo recomiendo.'
]

reseñas = []

# Tomar 100 ventas únicas
ventas_muestra = df_ventas.sample(n=100)

for i, venta in enumerate(ventas_muestra.itertuples(), start=1):
    fecha_venta = pd.to_datetime(venta.fecha).date()

    reseñas.append({
        'reseña_id': f"RS-{i:05d}",
        'venta_id': venta.purchase_id,
        'client_id': venta.client_id,
        'puntuacion': random.choices([5, 4, 3, 2, 1], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0],
        'comentario': random.choice(comentarios),
        'fecha_reseña': fake.date_between(start_date=fecha_venta, end_date='today')
    })

# Crear DataFrame
df_reseñas = pd.DataFrame(reseñas)

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_reseñas(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/reseñas.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/reseñas.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/reseñas.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/reseñas.sql', 'Reseñas'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/reseñas.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/reseñas.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/reseñas.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_reseñas.head())
exportar_reseñas(df_reseñas)
print(f"\n✅ Se han generado y exportado {len(df_reseñas)} reseñas con client_id normalizado y vinculadas a ventas reales.")




