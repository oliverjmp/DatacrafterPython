import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar sucursales y productos
df_branches = pd.read_csv('sucursales.csv')
df_products = pd.read_csv('productos.csv')

# Unidades de medida por categoría
unidades_por_categoria = {
    'Electrónica': 'unidad',
    'Alimentos': random.choice(['kg', 'g', 'litro', 'unidad']),
    'Hogar': 'unidad',
    'Ropa': 'unidad',
    'Juguetes': 'unidad',
    'Deportes': random.choice(['unidad', 'litro', 'kg'])
}

inventario = []

for _, branch in df_branches.iterrows():
    productos_sample = df_products.sample(random.randint(20, 50))
    for _, prod in productos_sample.iterrows():
        stock = random.randint(10, 200)
        stock_min = random.randint(5, 15)
        stock_max = stock + random.randint(50, 150)
        unidad = unidades_por_categoria.get(prod['category'], 'unidad')
        fecha = fake.date_between(start_date='-3mo', end_date='today')
        
        inventario.append({
            'branch_id': branch['branch_id'],
            'product_id': prod['product_id'],
            'stock': stock,
            'stock_minimo': stock_min,
            'stock_maximo': stock_max,
            'unidad_medida': unidad,
            'fecha_actualizacion': fecha
        })

df_inventario = pd.DataFrame(inventario)
df_inventario.to_csv('inventario.csv', index=False)

print(df_inventario.head())
print(f"\n✅ Inventario enriquecido generado y exportado a 'inventario.csv'.")