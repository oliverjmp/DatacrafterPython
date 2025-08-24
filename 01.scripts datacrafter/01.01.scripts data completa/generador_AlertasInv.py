import pandas as pd
from datetime import datetime

# Cargar inventario y productos
df_inventario = pd.read_csv('02.descargable/CSV/inventario.csv', encoding='utf-8-sig')
df_productos = pd.read_csv('02.descargable/CSV/productos.csv', encoding='utf-8-sig')

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

# Exportar
df_alertas.to_csv('02.descargable/CSV/alertas_stock.csv', index=False, encoding='utf-8-sig')

print(df_alertas.head())
print(f"\n⚠️ Se han generado {len(df_alertas)} alertas de stock bajo con prioridad y proveedor vinculado.")

