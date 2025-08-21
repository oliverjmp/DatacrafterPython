import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_clientes = pd.read_csv('clientes.csv')
df_sucursales = pd.read_csv('sucursales.csv')
df_empleados = pd.read_csv('empleados.csv')
df_productos = pd.read_csv('productos.csv')

# Canales y ajustes
canales = ['Presencial', 'Página Web', 'Amazon', 'Instagram', 'Distribuidor']
ajustes_precio = {
    'Presencial': 1.00,
    'Página Web': 0.95,
    'Amazon': 1.10,
    'Instagram': 0.97,
    'Distribuidor': 0.85
}
metodos_pago = {
    'Presencial': ['Efectivo', 'Tarjeta'],
    'Página Web': ['Tarjeta', 'PayPal'],
    'Amazon': ['Amazon Pay', 'Tarjeta'],
    'Instagram': ['Bizum', 'Transferencia'],
    'Distribuidor': ['Transferencia']
}
categorias_por_canal = {
    'Presencial': ['Snacks', 'Bebidas'],
    'Página Web': ['Electrónica', 'Hogar'],
    'Amazon': ['Libros', 'Tecnología'],
    'Instagram': ['Moda', 'Belleza'],
    'Distribuidor': ['Industrial']
}

ventas = []
detalle_ventas = []

for i in range(1, 151):
    cliente = df_clientes.sample(1).iloc[0]
    sucursal = df_sucursales.sample(1).iloc[0]
    empleados_sucursal = df_empleados[df_empleados['branch_id'] == sucursal['branch_id']]
    
    if empleados_sucursal.empty:
        continue
    
    empleado = empleados_sucursal.sample(1).iloc[0]
    canal = random.choice(canales)
    metodo = random.choice(metodos_pago[canal])
    venta_id = f"VT-{i:05d}"
    
    ventas.append({
        'venta_id': venta_id,
        'fecha': fake.date_between(start_date='-1y', end_date='today'),
        'client_id': cliente['client_id'],
        'branch_id': sucursal['branch_id'],
        'employee_id': empleado['employee_id'],
        'canal_venta': canal,
        'metodo_pago': metodo
    })
    
    categorias = categorias_por_canal[canal]
    productos_filtrados = df_productos[df_productos['category'].isin(categorias)]
    
    if productos_filtrados.empty:
        productos_filtrados = df_productos.sample(3)
    else:
        productos_filtrados = productos_filtrados.sample(min(3, len(productos_filtrados)))
    
    for _, prod in productos_filtrados.iterrows():
        cantidad = random.randint(1, 3)
        precio_ajustado = round(prod['price'] * ajustes_precio[canal], 2)
        detalle_ventas.append({
            'venta_id': venta_id,
            'product_id': prod['product_id'],
            'cantidad': cantidad,
            'precio_unitario': precio_ajustado
        })

# Exportar CSV
pd.DataFrame(ventas).to_csv('ventas.csv', index=False)
pd.DataFrame(detalle_ventas).to_csv('detalle_venta.csv', index=False)

# Mostrar ejemplo
print(pd.DataFrame(ventas).head())
print(pd.DataFrame(detalle_ventas).head())
print("✅ Datos generados con canal, método de pago y ajuste de precio.")
