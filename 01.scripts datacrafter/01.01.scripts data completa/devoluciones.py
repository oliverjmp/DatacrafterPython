import pandas as pd
import random
from faker import Faker
import os

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('02.descargable/CSV/01.CSV correctos/ventas.csv', encoding='utf-8-sig')
df_detalle = pd.read_csv('02.descargable/CSV/01.CSV correctos/detalle_ventas.csv', encoding='utf-8-sig')
df_productos = pd.read_csv('02.descargable/CSV/01.CSV correctos/productos.csv', encoding='utf-8-sig')
df_entregas = pd.read_csv('02.descargable/CSV/01.CSV correctos/entregas.csv', encoding='utf-8-sig')

# Filtrar entregas completadas
entregas_entregadas = df_entregas[df_entregas['estado'] == 'Entregado']

# Motivos realistas
motivos_reales = [
    'Producto defectuoso', 'Tamaño incorrecto', 'No coincide con la descripción',
    'Llegó dañado', 'Retraso en la entrega', 'Cambio de opinión', 'Error en el pedido',
    'Producto incompleto', 'Calidad inferior a lo esperado', 'Recibí otro artículo',
    'Pedido duplicado', 'Problema con el embalaje', 'No funciona correctamente',
    'Vencido o caducado', 'Cliente no lo reconoce'
]

# Estados posibles
estados = ['Pendiente', 'Procesada', 'Rechazada']

# Lista para almacenar devoluciones
devoluciones = []

# Generar devoluciones simuladas
for i in range(1, 101):
    entrega = entregas_entregadas.sample(1).iloc[0]
    venta_id = entrega['venta_id']
    entrega_id = entrega['entrega_id']

    venta = df_ventas[df_ventas['purchase_id'] == venta_id]
    if venta.empty:
        continue
    venta = venta.iloc[0]

    productos_venta = df_detalle[df_detalle['purchase_id'] == venta_id]
    if productos_venta.empty:
        continue
    producto = productos_venta.sample(1).iloc[0]
    product_id = producto['product_id']

    producto_info = df_productos[df_productos['product_id'] == product_id]
    if producto_info.empty:
        continue
    proveedor_id = producto_info.iloc[0]['provider_id']

    devoluciones.append({
        'devolucion_id': f"DV-{i:05d}",
        'venta_id': venta_id,
        'client_id': venta['client_id'],
        'entrega_id': entrega_id,
        'product_id': product_id,
        'provider_id': proveedor_id,
        'branch_id': venta['branch_id'],
        'employee_id': venta['employee_id'],
        'fecha_devolucion': fake.date_between(start_date='-6M', end_date='today'),
        'motivo': random.choice(motivos_reales),
        'estado': random.choice(estados)
    })

# Crear DataFrame
df_devoluciones = pd.DataFrame(devoluciones)

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_devoluciones(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/devoluciones.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/devoluciones.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/devoluciones.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/devoluciones.sql', 'Devoluciones'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/devoluciones.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/devoluciones.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/devoluciones.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_devoluciones.head())
exportar_devoluciones(df_devoluciones)
print(f"\n✅ Se han generado y exportado {len(df_devoluciones)} devoluciones con client_id normalizado, solo de entregas completadas.")
