import pandas as pd

# Cargar inventario
df_inventario = pd.read_csv('inventario.csv')

# Filtrar productos con stock bajo
df_alertas = df_inventario[df_inventario['stock'] <= df_inventario['stock_minimo']].copy()

# Crear columna de alerta
df_alertas['alerta_id'] = ['AL-' + str(i+1).zfill(5) for i in range(len(df_alertas))]
df_alertas['fecha_alerta'] = pd.Timestamp.today().strftime('%Y-%m-%d')

# Reordenar columnas
df_alertas = df_alertas[[
    'alerta_id', 'branch_id', 'product_id', 'stock', 'stock_minimo',
    'fecha_actualizacion', 'fecha_alerta'
]]

# Exportar alertas
df_alertas.to_csv('alertas_stock.csv', index=False)

print(df_alertas.head())
print(f"\n⚠️ Se han generado {len(df_alertas)} alertas de stock bajo en 'alertas_stock.csv'.")
