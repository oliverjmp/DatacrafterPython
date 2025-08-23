import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar datos base
df_ventas = pd.read_csv('02.descargable/CSV/ventas.csv', encoding='utf-8-sig')

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

# Tomar 100 ventas únicas
ventas_muestra = df_ventas.sample(n=100)

for i, venta in enumerate(ventas_muestra.itertuples(), start=1):
    fecha_venta = pd.to_datetime(venta.fecha).date()

    reseñas.append({
        'reseña_id': f"RS-{i:05d}",
        'venta_id': venta.purchase_id,
        'client_id': venta.cliente,
        'puntuacion': random.choices([5, 4, 3, 2, 1], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0],
        'comentario': random.choice(comentarios),
        'fecha_reseña': fake.date_between(start_date=fecha_venta, end_date='today')
    })

# Exportar CSV
df_reseñas = pd.DataFrame(reseñas)
df_reseñas.to_csv('02.descargable/CSV/reseñas.csv', index=False, encoding='utf-8-sig')

print(df_reseñas.head())
print(f"✅ Se han generado {len(df_reseñas)} reseñas vinculadas a ventas reales.")


