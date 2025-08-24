import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Cargar clientes
df_clientes = pd.read_csv("02.descargable/CSV/01.CSV correctos/clientes.csv", encoding='utf-8-sig')
client_ids = df_clientes["client_id"].dropna().unique()

# Niveles y beneficios
niveles = ['Bronce', 'Plata', 'Oro', 'Platino']
beneficios_por_nivel = {
    'Bronce': '5% descuento en snacks',
    'Plata': '10% en bebidas y envíos gratis',
    'Oro': '15% en todo + acceso anticipado',
    'Platino': '20% en todo + regalos exclusivos'
}

# Generar fidelización
fidelizacion = []
for i, client_id in enumerate(client_ids, start=1):
    nivel = random.choices(niveles, weights=[0.5, 0.3, 0.15, 0.05])[0]
    puntos = random.randint(100, 5000)
    fecha_actividad = fake.date_between(start_date='-3M', end_date='today')

    fidelizacion.append({
        'fidelizacion_id': f"FD-{i:05d}",
        'client_id': client_id,
        'nivel': nivel,
        'puntos_acumulados': puntos,
        'beneficios': beneficios_por_nivel[nivel],
        'fecha_ultima_actividad': fecha_actividad
    })

# Crear DataFrame
df_fidelizacion = pd.DataFrame(fidelizacion)

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_fidelizacion(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/fidelizacion.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/fidelizacion.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/fidelizacion.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/fidelizacion.sql', 'Fidelizacion'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/fidelizacion.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/fidelizacion.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/fidelizacion.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_fidelizacion.head())
exportar_fidelizacion(df_fidelizacion)
print(f"\n✅ Se han generado y exportado {len(df_fidelizacion)} registros de fidelización con client_id normalizado.")

