import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker('es_ES')

# Cargar ventas existentes
df_ventas = pd.read_csv('02.descargable/CSV/ventas.csv', encoding='utf-8-sig')

# Filtrar solo ventas que requieren entrega
canales_con_entrega = ['Página Web', 'Amazon', 'Instagram', 'Uber Eats']
df_ventas_envio = df_ventas[df_ventas['canal'].isin(canales_con_entrega)]

# Configuración de entregas
empresas_logisticas = ['DHL', 'SEUR', 'Correos Express', 'Amazon Logistics', 'FedEx', 'MRW', 'UPS']
estados_entrega = ['Pendiente', 'Enviado', 'Entregado', 'Cancelado']

entregas = []

for i, venta in df_ventas_envio.iterrows():
    entrega_id = f"ET-{i+1:05d}"
    tipo_entrega = random.choice(['Propia', 'Logística'])
    estado = random.choices(estados_entrega, weights=[0.1, 0.3, 0.5, 0.1])[0]

    fecha_venta = pd.to_datetime(venta['fecha']).date()
    fecha_envio = None
    fecha_entrega = None
    cumplimiento = None

    if estado == 'Enviado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=5))
    elif estado == 'Entregado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=3))
        fecha_entrega = fake.date_between(start_date=fecha_envio, end_date=fecha_envio + timedelta(days=5))
        # Evaluar cumplimiento de 72h
        if fecha_envio and fecha_entrega:
            delta = (fecha_entrega - fecha_envio).days
            cumplimiento = 'Entregado a tiempo' if delta <= 3 else 'Retrasado'
    elif estado == 'Cancelado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=2))

    empresa = random.choice(empresas_logisticas) if tipo_entrega == 'Logística' else None

    entregas.append({
        'entrega_id': entrega_id,
        'venta_id': venta['purchase_id'],
        'fecha_envio': fecha_envio,
        'fecha_entrega': fecha_entrega,
        'estado': estado,
        'tipo_entrega': tipo_entrega,
        'empresa_logistica': empresa,
        'cumplimiento_72h': cumplimiento
    })

# Guardar entregas.csv
df_entregas = pd.DataFrame(entregas)
ruta_entregas = os.path.join('02.descargable', 'CSV', 'entregas.csv')
os.makedirs(os.path.dirname(ruta_entregas), exist_ok=True)
df_entregas.to_csv(ruta_entregas, index=False, encoding='utf-8-sig')

print(df_entregas.head())
print(f"✅ Se han generado {len(df_entregas)} entregas con evaluación de cumplimiento en 72h.")

