import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('02.descargable/CSV/ventas.csv', encoding='utf-8-sig')
df_detalle = pd.read_csv('02.descargable/CSV/detalle_ventas.csv', encoding='utf-8-sig')
df_productos = pd.read_csv('02.descargable/CSV/productos.csv', encoding='utf-8-sig')
df_entregas = pd.read_csv('02.descargable/CSV/entregas.csv', encoding='utf-8-sig')

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
        'client_id': venta['client_id'],  # ← Normalizado
        'entrega_id': entrega_id,
        'product_id': product_id,
        'provider_id': proveedor_id,
        'branch_id': venta['branch_id'],
        'employee_id': venta['employee_id'],
        'fecha_devolucion': fake.date_between(start_date='-6M', end_date='today'),
        'motivo': random.choice(motivos_reales),
        'estado': random.choice(estados)
    })

# Exportar a CSV
df_devoluciones = pd.DataFrame(devoluciones)
df_devoluciones.to_csv('02.descargable/CSV/devoluciones.csv', index=False, encoding='utf-8-sig')

print(df_devoluciones.head())
print(f"✅ Se han generado {len(df_devoluciones)} devoluciones con client_id normalizado, solo de entregas completadas.")

