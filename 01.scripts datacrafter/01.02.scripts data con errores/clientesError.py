import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Generar clientes con errores
clientes_erroneos = []

for i in range(1, 10001):
    client_id = random.choice([
        f"CL-{i:05d}", f"cl_{i:05d}", None if i % 20 == 0 else f"CL-{i:05d}"
    ])
    nombre = random.choice([fake.name(), "", "@Oliver", "123"]) if i % 15 == 0 else fake.name()
    email = random.choice([
        fake.email(), "correo@.com", "@gmail.com", "", None
    ]) if i % 10 == 0 else fake.email()
    telefono = random.choice([
        fake.phone_number(), "61234abc", "123456", "6-123-456"
    ]) if i % 12 == 0 else fake.msisdn()
    genero = random.choice(["Masculino", "Femenino", "Desconocido", "M", "fem"]) if i % 8 == 0 else random.choice(["Masculino", "Femenino"])
    fecha_registro = random.choice([
        fake.date_between(start_date='-2y', end_date='today'),
        "2026-01-01", None
    ]) if i % 18 == 0 else fake.date_between(start_date='-2y', end_date='today')

    clientes_erroneos.append({
        "client_id": client_id,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "genero": genero,
        "fecha_registro": fecha_registro
    })

# Crear DataFrame
df_clientes_erroneos = pd.DataFrame(clientes_erroneos)

# Convertir fecha_registro a datetime64[ns] para compatibilidad
df_clientes_erroneos['fecha_registro'] = pd.to_datetime(df_clientes_erroneos['fecha_registro'], errors='coerce')

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_clientes_erroneos(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/02.CSV con errores/clientesError.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/02.JSON con errores/clientesError.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/02.JSON con errores/clientesError.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/02.SQL con errores/clientesError.sql', 'ClientesError'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/02.PARQUET con errores/clientesError.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/02.FEATHER con errores/clientesError.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/02.XLSX con errores/clientesError.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_clientes_erroneos.head())
exportar_clientes_erroneos(df_clientes_erroneos)
print(f"\n⚠️ Se han generado y exportado {len(df_clientes_erroneos)} registros de clientes con errores simulados.")
