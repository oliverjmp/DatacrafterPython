import pandas as pd
from datetime import datetime
import os

# Cargar inventario y productos
df_inventario = pd.read_csv('02.descargable/CSV/01.CSV correctos/inventario.csv', encoding='utf-8-sig')
df_productos = pd.read_csv('02.descargable/CSV/01.CSV correctos/productos.csv', encoding='utf-8-sig')

# Filtrar productos con stock bajo
df_alertas = df_inventario[df_inventario['stock_actual'] <= df_inventario['stock_minimo']].copy()

# Generar alerta_id y fecha
df_alertas['alerta_id'] = ['AL-' + str(i+1).zfill(5) for i in range(len(df_alertas))]
df_alertas['fecha_alerta'] = pd.Timestamp.today().strftime('%Y-%m-%d')

# Calcular prioridad
def calcular_prioridad(row):
    if row['stock_actual'] == 0:
        return 'Alta'
    elif row['stock_actual'] < row['stock_minimo'] / 2:
        return 'Media'
    else:
        return 'Baja'

df_alertas['prioridad'] = df_alertas.apply(calcular_prioridad, axis=1)

# Vincular proveedor desde productos
df_productos_reducido = df_productos[['product_id', 'provider_id', 'provider_name']]
df_alertas = df_alertas.merge(df_productos_reducido, on='product_id', how='left')

# Reordenar columnas
df_alertas = df_alertas[[
    'alerta_id', 'branch_id', 'product_id', 'stock_actual', 'stock_minimo',
    'fecha_actualizacion', 'fecha_alerta', 'prioridad', 'provider_id', 'provider_name'
]]

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_alertas(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/alertas_stock.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/alertas_stock.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/alertas_stock.json', orient='table'),
        'SQL': lambda: exportar_sql(df, f'{carpeta}/SQL/01.SQL correctos/alertas_stock.sql', 'AlertasStock'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/alertas_stock.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/alertas_stock.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/alertas_stock.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_alertas.head())
exportar_alertas(df_alertas)
print(f"\n⚠️ Se han generado y exportado {len(df_alertas)} alertas de stock bajo con prioridad y proveedor vinculado.")


