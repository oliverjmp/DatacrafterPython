import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('ventas.csv')

# Comentarios simulados
comentarios = [
    'Muy buen producto, llegó rápido.',
    'No era lo que esperaba.',
    'Excelente atención al cliente.',
    'El embalaje estaba dañado.',
    'Volveré a comprar sin duda.',
    'Precio justo y buena calidad.',
    'Tuve problemas con la entrega.',
    'Todo perfecto, gracias.',
    'La talla no era correcta.',
    'Me encantó, lo recomiendo.'
]

reseñas = []

for i in range(1, 101):
    venta = df_ventas.sample(1).iloc[0]
    
    # ✅ Conversión de fecha a tipo date
    fecha_venta = pd.to_datetime(venta['fecha']).date()
    
    reseñas.append({
        'reseña_id': f"RS-{i:05d}",
        'venta_id': venta['venta_id'],
        'client_id': venta['client_id'],
        'puntuacion': random.choices([5, 4, 3, 2, 1], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0],
        'comentario': random.choice(comentarios),
        'fecha_reseña': fake.date_between(start_date=fecha_venta, end_date='today')
    })

# Exportar CSV
df_reseñas = pd.DataFrame(reseñas)
df_reseñas.to_csv('reseñas.csv', index=False)

print(df_reseñas.head())
print("✅ Archivo 'reseñas.csv' generado con puntuaciones y comentarios.")

