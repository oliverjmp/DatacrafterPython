import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Simular errores en ventas
ventas_erroneas = []

canales_validos = ['Presencial', 'Página Web', 'Amazon', 'Instagram', 'Distribuidor']
canales_erroneos = ['TikTok', 'Desconocido', '', None]
metodos_pago_validos = ['Efectivo', 'Tarjeta', 'PayPal', 'Amazon Pay', 'Bizum', 'Transferencia']
metodos_erroneos = ['Cheque', '', None]

for i in range(1, 10001):
    purchase_id = random.choice([
        f"C-{i:06d}", f"c_{i:06d}", None if i % 50 == 0 else f"C-{i:06d}"
    ])
    client_id = random.choice([
        f"CL-{random.randint(1, 9999)}", None if i % 40 == 0 else f"CL-{random.randint(1, 9999)}"
    ])
    canal = random.choice(canales_validos + canales_erroneos) if i % 20 == 0 else random.choice(canales_validos)
    metodo_pago = random.choice(metodos_erroneos) if i % 25 == 0 else random.choice(metodos_pago_validos)
    total = random.choice([
        round(random.uniform(10, 1500), 2),
        -random.uniform(1, 500),
        None,
        "mil euros"
    ]) if i % 30 == 0 else round(random.uniform(10, 1500), 2)
    fecha = random.choice([
        fake.date_between(start_date='-90d', end_date='today'),
        "2026-01-01",
        None
    ]) if i % 35 == 0 else fake.date_between(start_date='-90d', end_date='today')
    branch_id = f"SUC-{random.randint(1, 50)}"
    employee_id = random.choice([
        f"EMP-{random.randint(1, 100)}",
        None,
        "EMP-00001"
    ]) if i % 45 == 0 else f"EMP-{random.randint(1, 100)}"

    ventas_erroneas.append({
        "purchase_id": purchase_id,
        "branch_id": branch_id,
        "client_id": client_id,
        "fecha": fecha,
        "canal": canal,
        "metodo_pago": metodo_pago,
        "employee_id": employee_id,
        "total": total
    })

df_ventas_erroneas = pd.DataFrame(ventas_erroneas)

# Convertir fecha a datetime64[ns] y total a float (con errores como NaN)
df_ventas_erroneas['fecha'] = pd.to_datetime(df_ventas_erroneas['fecha'], errors='coerce')
df_ventas_erroneas['total'] = pd.to_numeric(df_ventas_erroneas['total'], errors='coerce')

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Exportar en múltiples formatos
def exportar_ventas_erroneas(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/02.CSV con errores/ventasError.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/02.JSON con errores/ventasError.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/02.JSON con errores/ventasError.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/02.SQL con errores/ventasError.sql', 'VentasError'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/02.PARQUET con errores/ventasError.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/02.FEATHER con errores/ventasError.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/02.XLSX con errores/ventasError.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_ventas_erroneas.head())
exportar_ventas_erroneas(df_ventas_erroneas)
print(f"\n⚠️ Se han generado y exportado {len(df_ventas_erroneas)} registros de ventas con errores simulados.")
