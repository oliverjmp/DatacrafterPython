import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('es_ES')

# Cargar ventas generadas
df_ventas = pd.read_csv('ventas.csv')

# Empresas logísticas
empresas_logisticas = ['DHL', 'SEUR', 'Correos Express', 'Amazon Logistics', 'FedEx', 'MRW', 'UPS']
estados_entrega = ['Pendiente', 'Enviado', 'Entregado', 'Cancelado']

entregas = []

for i, venta in df_ventas.iterrows():
    entrega_id = f"ET-{i+1:05d}"
    tipo_entrega = random.choice(['Propia', 'Logística'])
    estado = random.choices(estados_entrega, weights=[0.1, 0.3, 0.5, 0.1])[0]
    
    # Convertir fecha de venta a tipo datetime.date
    fecha_venta = datetime.strptime(venta['fecha'], '%Y-%m-%d').date()
    
    # Inicializar fechas
    fecha_envio = None
    fecha_entrega = None
    
    if estado == 'Pendiente':
        fecha_envio = None
        fecha_entrega = None
    elif estado == 'Enviado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=5))
        fecha_entrega = None
    elif estado == 'Entregado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=3))
        fecha_entrega = fake.date_between(start_date=fecha_envio, end_date=fecha_envio + timedelta(days=5))
    elif estado == 'Cancelado':
        fecha_envio = fake.date_between(start_date=fecha_venta, end_date=fecha_venta + timedelta(days=2))
        fecha_entrega = None
    
    empresa = random.choice(empresas_logisticas) if tipo_entrega == 'Logística' else None
    
    entregas.append({
        'entrega_id': entrega_id,
        'venta_id': venta['venta_id'],
        'fecha_envio': fecha_envio,
        'fecha_entrega': fecha_entrega,
        'estado': estado,
        'tipo_entrega': tipo_entrega,
        'empresa_logistica': empresa
    })

# Exportar CSV
df_entregas = pd.DataFrame(entregas)
df_entregas.to_csv('entregas.csv', index=False)

print(df_entregas.head())
print("✅ Datos de entregas generados correctamente.")

