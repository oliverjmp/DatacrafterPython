import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('ventas.csv')
df_detalle = pd.read_csv('detalle_venta.csv')

# Estados posibles y probabilidades realistas
estados_pago = ['Completado', 'Pendiente', 'Fallido']
probabilidades = [0.85, 0.10, 0.05]

pagos = []

for i, venta in df_ventas.iterrows():
    venta_id = venta['venta_id']
    metodo = venta['metodo_pago']
    fecha_venta = pd.to_datetime(venta['fecha'])
    
    # Calcular total desde detalle_venta
    detalle = df_detalle[df_detalle['venta_id'] == venta_id]
    if detalle.empty:
        continue
    total = (detalle['cantidad'] * detalle['precio_unitario']).sum()
    
    estado = random.choices(estados_pago, weights=probabilidades)[0]
    
    # Fecha de pago: si fallido, puede ser el mismo día; si completado, entre 0 y 3 días después
    if estado == 'Completado':
        fecha_pago = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + pd.Timedelta(days=3))
    else:
        fecha_pago = fecha_venta
    
    pagos.append({
        'pago_id': f"PG-{i+1:05d}",
        'venta_id': venta_id,
        'fecha_pago': fecha_pago,
        'monto_total': round(total, 2),
        'metodo_pago': metodo,
        'estado_pago': estado
    })

# Exportar CSV
df_pagos = pd.DataFrame(pagos)
df_pagos.to_csv('pagos.csv', index=False)

print(df_pagos.head())
print("✅ Archivo 'pagos.csv' generado con éxito.")
