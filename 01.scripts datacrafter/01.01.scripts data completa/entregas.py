import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker('es_ES')

# Cargar ventas existentes
df_ventas = pd.read_csv('02.descargable/CSV/01.CSV correctos/ventas.csv', encoding='utf-8-sig')

# Filtrar solo ventas que requieren entrega
canales_con_entrega = ['Página Web', 'Amazon', 'Instagram', 'Uber Eats']
df_ventas_envio = df_ventas[df_ventas['canal'].isin(canales_con_entrega)]

# Configuración de entregas
empresas_logisticas = ['DHL', 'SEUR', 'Correos Express', 'Amazon Logistics', 'FedEx', 'MRW', 'UPS']
estados_entrega = ['Pendiente', 'Enviado', 'Entregado', 'Cancelado']

entregas = []

for i, venta in df_ventas_envio.iterrows():
    entrega_id = f"ET-{i+1:05d}"
    tipo_entrega = random.choice(['Propia', 'Logística'])
    estado = random.choices(estados_entrega, weights=[0.1, 0.3, 0.5, 0.1])[0]

    fecha_venta = pd.to_datetime(venta['fecha']).date()
    fecha_envio = None
    fecha_entrega = None
    cumplimiento = None

    if estado == 'Enviado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=5))
    elif estado == 'Entregado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=3))
        fecha_entrega = fake.date_between(start_date=fecha_envio, end_date=fecha_envio + timedelta(days=5))
        delta = (fecha_entrega - fecha_envio).days
        cumplimiento = 'Entregado a tiempo' if delta <= 3 else 'Retrasado'
    elif estado == 'Cancelado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=2))

    empresa = random.choice(empresas_logisticas) if tipo_entrega == 'Logística' else None

    entregas.append({
        'entrega_id': entrega_id,
        'venta_id': venta['purchase_id'],
        'fecha_envio': fecha_envio,
        'fecha_entrega': fecha_entrega,
        'estado': estado,
        'tipo_entrega': tipo_entrega,
        'empresa_logistica': empresa,
        'cumplimiento_72h': cumplimiento
    })

# Crear DataFrame
df_entregas = pd.DataFrame(entregas)

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_entregas(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/entregas.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/entregas.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/entregas.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/entregas.sql', 'Entregas'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/entregas.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/entregas.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/entregas.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_entregas.head())
exportar_entregas(df_entregas)
print(f"\n✅ Se han generado y exportado {len(df_entregas)} entregas con evaluación de cumplimiento en 72h.")
