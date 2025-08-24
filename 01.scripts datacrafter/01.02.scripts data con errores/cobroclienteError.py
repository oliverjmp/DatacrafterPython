import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Simular cobros con errores
cobros_erroneos = []

for i in range(1, 10001):
    pago_id = random.choice([
        f"PG-{i:06d}", f"pg_{i:06d}", None if i % 50 == 0 else f"PG-{i:06d}"
    ])
    venta_id = random.choice([
        f"C-{random.randint(1, 9999)}", None if i % 40 == 0 else f"C-{random.randint(1, 9999)}"
    ])
    metodo_pago = random.choice([
        "Tarjeta", "PayPal", "Amazon Pay", "Bizum", "Transferencia", "Efectivo",
        "Cheque", "", None
    ]) if i % 25 == 0 else random.choice(["Tarjeta", "PayPal", "Amazon Pay", "Bizum", "Transferencia", "Efectivo"])
    fecha_cobro = random.choice([
        fake.date_between(start_date='-60d', end_date='today'),
        "2026-01-01",
        None
    ]) if i % 30 == 0 else fake.date_between(start_date='-60d', end_date='today')
    monto_total = random.choice([
        round(random.uniform(50, 2000), 2),
        -random.uniform(1, 500),
        "mil euros",
        None
    ]) if i % 35 == 0 else round(random.uniform(50, 2000), 2)
    estado_pago = random.choice([
        "Completado", "Pendiente", "Fallido", "En proceso", "✔ Pagado"
    ]) if i % 20 == 0 else random.choice(["Completado", "Pendiente", "Fallido"])

    cobros_erroneos.append({
        "pago_id": pago_id,
        "venta_id": venta_id,
        "fecha_cobro": fecha_cobro,
        "monto_total": monto_total,
        "metodo_pago": metodo_pago,
        "estado_pago": estado_pago
    })

df_cobros_erroneos = pd.DataFrame(cobros_erroneos)

# Convertir fecha y monto para compatibilidad
df_cobros_erroneos['fecha_cobro'] = pd.to_datetime(df_cobros_erroneos['fecha_cobro'], errors='coerce')
df_cobros_erroneos['monto_total'] = pd.to_numeric(df_cobros_erroneos['monto_total'], errors='coerce')

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Exportar en múltiples formatos
def exportar_cobros_ventas_erroneos(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/02.CSV con errores/cobrosVentasError.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/02.JSON con errores/cobrosVentasError.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/02.JSON con errores/cobrosVentasError.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/02.SQL con errores/cobrosVentasError.sql', 'CobrosVentasError'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/02.PARQUET con errores/cobrosVentasError.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/02.FEATHER con errores/cobrosVentasError.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/02.XLSX con errores/cobrosVentasError.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_cobros_erroneos.head())
exportar_cobros_ventas_erroneos(df_cobros_erroneos)
print(f"\n⚠️ Se han generado y exportado {len(df_cobros_erroneos)} registros de cobros con errores simulados.")
