import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('02.descargable/CSV/ventas.csv', encoding='utf-8-sig')
df_detalle = pd.read_csv('02.descargable/CSV/detalle_ventas.csv', encoding='utf-8-sig')

# Estados posibles y probabilidades realistas
estados_pago = ['Completado', 'Pendiente', 'Fallido']
probabilidades = [0.85, 0.10, 0.05]

cobros = []

for i, venta in df_ventas.iterrows():
    venta_id = venta['purchase_id']
    metodo = venta['metodo_pago']
    fecha_venta = pd.to_datetime(venta['fecha'])

    # Calcular total desde detalle_ventas
    detalle = df_detalle[df_detalle['purchase_id'] == venta_id]
    if detalle.empty:
        continue
    total = (detalle['cantidad'] * detalle['precio_unitario']).sum()

    estado = random.choices(estados_pago, weights=probabilidades)[0]

    # Fecha de cobro
    if estado == 'Completado':
        fecha_cobro = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + pd.Timedelta(days=3))
    else:
        fecha_cobro = fecha_venta

    cobros.append({
        'pago_id': f"PG-{i+1:05d}",
        'venta_id': venta_id,
        'fecha_cobro': fecha_cobro,
        'monto_total': round(total, 2),
        'metodo_pago': metodo,
        'estado_pago': estado
    })

# Exportar CSV
df_cobros = pd.DataFrame(cobros)
df_cobros.to_csv('02.descargable/CSV/cobros.csv', index=False, encoding='utf-8-sig')

print(df_cobros.head())
print(f"✅ Se han generado {len(df_cobros)} registros de cobros basados en ventas reales.")

