import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos
df_productos = pd.read_csv('productos.csv')
df_sucursales = pd.read_csv('sucursales.csv')
df_proveedores = pd.read_csv('proveedores.csv')

compras = []

# Número de compras a generar
num_compras = 500

for i in range(1, num_compras + 1):
    sucursal = df_sucursales.sample(1).iloc[0]
    producto = df_productos.sample(1).iloc[0]
    proveedor = df_proveedores[df_proveedores['provider_id'] == producto['provider_id']].iloc[0]

    cantidad = random.randint(10, 100)
    precio_unitario = round(producto['price'] * random.uniform(0.7, 1.2), 2)
    fecha = fake.date_between(start_date='-2mo', end_date='today')

    compras.append({
        'compra_id': f"CP-{i:05d}",
        'branch_id': sucursal['branch_id'],
        'product_id': producto['product_id'],
        'provider_id': proveedor['provider_id'],
        'cantidad': cantidad,
        'precio_unitario': precio_unitario,
        'fecha_compra': fecha
    })

# Exportar a CSV
df_compras = pd.DataFrame(compras)
df_compras.to_csv('compras.csv', index=False)

print(df_compras.head())
print(f"\n✅ Se han generado {num_compras} compras simuladas en 'compras.csv'.")
