import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar proveedores desde el CSV
df_proveedores = pd.read_csv('proveedores.csv')

# Listas de nombres por categoría
nombres_productos = {
    'Electrónica': ['Auriculares Bluetooth', 'Smartwatch', 'Cargador USB-C', 'Altavoz portátil'],
    'Alimentos': ['Café molido', 'Galletas integrales', 'Aceite de oliva', 'Arroz basmati'],
    'Hogar': ['Almohada viscoelástica', 'Lámpara LED', 'Cortina blackout', 'Organizador de cocina'],
    'Ropa': ['Camiseta básica', 'Pantalón vaquero', 'Chaqueta impermeable', 'Zapatillas deportivas'],
    'Juguetes': ['Bloques de construcción', 'Muñeca articulada', 'Puzzle 500 piezas', 'Pelota sensorial'],
    'Deportes': ['Mancuernas 5kg', 'Esterilla yoga', 'Balón de fútbol', 'Botella térmica']
}

# Formatos de venta por categoría
formatos_venta = {
    'Electrónica': ['Unidad', 'Set de 2 piezas', 'Caja con accesorios'],
    'Alimentos': ['Paquete de 500g', 'Botella de 1L', 'Caja de 12 unidades'],
    'Hogar': ['Unidad', 'Pack de 3', 'Set de cocina'],
    'Ropa': ['Talla M', 'Talla única', 'Pack de 2 camisetas'],
    'Juguetes': ['Caja con piezas', 'Set de construcción', 'Unidad'],
    'Deportes': ['Unidad', 'Pack de 2', 'Botella de 750ml']
}

# Función para generar descripción
def generar_descripcion(nombre, categoria):
    formato = random.choice(formatos_venta[categoria])
    return f"{nombre} en formato: {formato}"

# Número de productos
num_products = 200
productos = []

for i in range(1, num_products + 1):
    categoria = random.choice(list(nombres_productos.keys()))
    nombre = random.choice(nombres_productos[categoria])
    proveedor = df_proveedores.sample(1).iloc[0]
    
    productos.append({
        'product_id': f"PD-{i:05d}",
        'name': nombre,
        'description': generar_descripcion(nombre, categoria),
        'price': round(random.uniform(5, 500), 2),
        'category': categoria,
        'provider_id': proveedor['provider_id']
    })

# Crear DataFrame y exportar
df_productos = pd.DataFrame(productos)
df_productos.to_csv('productos.csv', index=False)

# Mostrar ejemplo
print(df_productos.head())
print(f"\n✅ Se han generado {num_products} productos con formato de venta realista en 'productos.csv'.")
