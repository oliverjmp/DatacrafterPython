import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')
df_clientes = pd.read_csv('clientes.csv')

niveles = ['Bronce', 'Plata', 'Oro', 'Platino']
beneficios_por_nivel = {
    'Bronce': '5% descuento en snacks',
    'Plata': '10% en bebidas y envíos gratis',
    'Oro': '15% en todo + acceso anticipado',
    'Platino': '20% en todo + regalos exclusivos'
}

fidelizacion = []

for i, cliente in df_clientes.iterrows():
    nivel = random.choices(niveles, weights=[0.5, 0.3, 0.15, 0.05])[0]
    puntos = random.randint(100, 5000)
    fidelizacion.append({
        'fidelizacion_id': f"FD-{i+1:05d}",
        'client_id': cliente['client_id'],
        'nivel': nivel,
        'puntos_acumulados': puntos,
        'beneficios': beneficios_por_nivel[nivel],
        'fecha_ultima_actividad': fake.date_between(start_date='-3M', end_date='today')
    })

df_fidelizacion = pd.DataFrame(fidelizacion)
df_fidelizacion.to_csv('fidelizacion.csv', index=False)
print(df_fidelizacion.head())
print("✅ Archivo 'fidelizacion.csv' generado con niveles y beneficios.")
