import pandas as pd
from datetime import datetime

# Cargar inventario y compras
inventario = pd.read_csv('inventario.csv')
df_compras = pd.read_csv('compras.csv')
df_productos = pd.read_csv('productos.csv')

# Convertir fecha a datetime
df_compras['fecha_compra'] = pd.to_datetime(df_compras['fecha_compra'])

# Procesar cada compra
for _, compra in df_compras.iterrows():
    branch_id = compra['branch_id']
    product_id = compra['product_id']
    cantidad = compra['cantidad']
    fecha = compra['fecha_compra']

    # Buscar si ya existe el producto en esa sucursal
    filtro = (inventario['branch_id'] == branch_id) & (inventario['product_id'] == product_id)

    if filtro.any():
        # Actualizar stock y fecha
        inventario.loc[filtro, 'stock'] += cantidad
        inventario.loc[filtro, 'fecha_actualizacion'] = fecha
    else:
        # Crear nuevo registro
        producto = df_productos[df_productos['product_id'] == product_id].iloc[0]
        unidad = 'unidad'  # Puedes mejorar esto con tu lógica de unidades por categoría

        nuevo_registro = {
            'branch_id': branch_id,
            'product_id': product_id,
            'stock': cantidad,
            'stock_minimo': 5,
            'stock_maximo': cantidad + 100,
            'unidad_medida': unidad,
            'fecha_actualizacion': fecha
        }

        inventario = pd.concat([inventario, pd.DataFrame([nuevo_registro])], ignore_index=True)

# Exportar inventario actualizado
inventario.to_csv('inventario.csv', index=False)

print(inventario.head())
print("\n✅ Inventario actualizado con compras y exportado a 'inventario.csv'.")

