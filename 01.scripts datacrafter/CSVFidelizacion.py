import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar ventas
df_ventas = pd.read_csv('02.descargable/CSV/ventas.csv', encoding='utf-8-sig')

# Extraer clientes únicos desde ventas
clientes_unicos = df_ventas['cliente'].dropna().unique()

# Niveles y beneficios
niveles = ['Bronce', 'Plata', 'Oro', 'Platino']
beneficios_por_nivel = {
    'Bronce': '5% descuento en snacks',
    'Plata': '10% en bebidas y envíos gratis',
    'Oro': '15% en todo + acceso anticipado',
    'Platino': '20% en todo + regalos exclusivos'
}

# Generar fidelización
fidelizacion = []

for i, client_id in enumerate(clientes_unicos, start=1):
    nivel = random.choices(niveles, weights=[0.5, 0.3, 0.15, 0.05])[0]
    puntos = random.randint(100, 5000)
    fecha_actividad = fake.date_between(start_date='-3M', end_date='today')

    fidelizacion.append({
        'fidelizacion_id': f"FD-{i:05d}",
        'client_id': client_id,
        'nivel': nivel,
        'puntos_acumulados': puntos,
        'beneficios': beneficios_por_nivel[nivel],
        'fecha_ultima_actividad': fecha_actividad
    })

# Exportar CSV
df_fidelizacion = pd.DataFrame(fidelizacion)
df_fidelizacion.to_csv('02.descargable/CSV/fidelizacion.csv', index=False, encoding='utf-8-sig')

print(df_fidelizacion.head())
print(f"✅ Se han generado {len(df_fidelizacion)} registros de fidelización basados en clientes reales de ventas.")

