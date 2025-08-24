import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('02.descargable/CSV/01.CSV correctos/ventas.csv', encoding='utf-8-sig')
df_detalle = pd.read_csv('02.descargable/CSV/01.CSV correctos/detalle_ventas.csv', encoding='utf-8-sig')

# Estados posibles y probabilidades realistas
estados_pago = ['Completado', 'Pendiente', 'Fallido']
probabilidades = [0.85, 0.10, 0.05]

cobros = []

for i, venta in df_ventas.iterrows():
    venta_id = venta['purchase_id']
    metodo = venta['metodo_pago']
    fecha_venta = pd.to_datetime(venta['fecha'])

    # Calcular total desde detalle_ventas
    detalle = df_detalle[df_detalle['purchase_id'] == venta_id]
    if detalle.empty:
        continue
    total = (detalle['cantidad'] * detalle['precio_unitario']).sum()

    estado = random.choices(estados_pago, weights=probabilidades)[0]

    # Fecha de cobro
    if estado == 'Completado':
        fecha_cobro = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + pd.Timedelta(days=3))
    else:
        fecha_cobro = fecha_venta

    cobros.append({
        'pago_id': f"PG-{i+1:05d}",
        'venta_id': venta_id,
        'fecha_cobro': fecha_cobro,
        'monto_total': round(total, 2),
        'metodo_pago': metodo,
        'estado_pago': estado
    })

# Crear DataFrame
df_cobros = pd.DataFrame(cobros)

# Convertir fecha_cobro a datetime64[ns] para compatibilidad con Parquet y Feather
df_cobros['fecha_cobro'] = pd.to_datetime(df_cobros['fecha_cobro'])

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_cobros(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/cobros.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/cobros.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/cobros.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/cobros.sql', 'Cobros'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/cobros.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/cobros.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/cobros.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_cobros.head())
exportar_cobros(df_cobros)
print(f"\n✅ Se han generado y exportado {len(df_cobros)} registros de cobros basados en ventas reales.")



