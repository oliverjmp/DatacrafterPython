import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('ventas.csv')
df_detalle = pd.read_csv('detalle_venta.csv')
df_productos = pd.read_csv('productos.csv')
df_entregas = pd.read_csv('entregas.csv')

# Motivos realistas
motivos_reales = [
    'Producto defectuoso',
    'Tamaño incorrecto',
    'No coincide con la descripción',
    'Llegó dañado',
    'Retraso en la entrega',
    'Cambio de opinión',
    'Error en el pedido',
    'Producto incompleto',
    'Calidad inferior a lo esperado',
    'Recibí otro artículo',
    'Pedido duplicado',
    'Problema con el embalaje',
    'No funciona correctamente',
    'Vencido o caducado',
    'Cliente no lo reconoce'
]

# Estados posibles
estados = ['Pendiente', 'Procesada', 'Rechazada']

# Lista para almacenar devoluciones
devoluciones = []

# Generar devoluciones simuladas
for i in range(1, 101):
    venta = df_ventas.sample(1).iloc[0]
    venta_id = venta['venta_id']
    client_id = venta['client_id']
    branch_id = venta['branch_id']
    employee_id = venta['employee_id']
    
    entrega = df_entregas[df_entregas['venta_id'] == venta_id]
    if entrega.empty:
        continue
    entrega_id = entrega.sample(1).iloc[0]['entrega_id']
    
    productos_venta = df_detalle[df_detalle['venta_id'] == venta_id]
    if productos_venta.empty:
        continue
    producto = productos_venta.sample(1).iloc[0]
    product_id = producto['product_id']
    
    producto_info = df_productos[df_productos['product_id'] == product_id].iloc[0]
    proveedor_id = producto_info['provider_id']
    
    devoluciones.append({
        'devolucion_id': f"DV-{i:05d}",
        'venta_id': venta_id,
        'client_id': client_id,
        'entrega_id': entrega_id,
        'product_id': product_id,
        'provider_id': proveedor_id,
        'branch_id': branch_id,
        'employee_id': employee_id,
        'fecha_devolucion': fake.date_between(start_date='-6M', end_date='today'),
        'motivo': random.choice(motivos_reales),
        'estado': random.choice(estados)
    })

# Exportar a CSV
df_devoluciones = pd.DataFrame(devoluciones)
df_devoluciones.to_csv('devoluciones.csv', index=False)

print(df_devoluciones.head())
print("✅ Archivo 'devoluciones.csv' generado con motivos realistas.")
print(df_devoluciones.head())