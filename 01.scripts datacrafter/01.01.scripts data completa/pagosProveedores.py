import pandas as pd
import random
from faker import Faker
from datetime import timedelta, datetime
import os

fake = Faker('es_ES')

# Cargar datos base
df_ordenes = pd.read_csv("02.descargable/CSV/compras_proveedor.csv", encoding='utf-8-sig')
df_proveedores = pd.read_csv("02.descargable/CSV/proveedores.csv", encoding='utf-8-sig')

# Crear índice rápido de condición de pago por proveedor
condiciones_map = df_proveedores.set_index("provider_id")["condicion_pago"].to_dict()

# Estados posibles
estados_pago = ['Pagado', 'Pendiente', 'Retrasado']

# Generar pagos
pagos = []

for i, orden in df_ordenes.iterrows():
    provider_id = orden["provider_id"]
    condicion = condiciones_map.get(provider_id, '30 días')
    dias_plazo = {
        'Contado': 0,
        '30 días': 30,
        '60 días': 60,
        '90 días': 90
    }.get(condicion, 30)

    fecha_orden = pd.to_datetime(orden["fecha_orden"])
    fecha_vencimiento = fecha_orden + timedelta(days=dias_plazo)

    # Simular estado de pago según vencimiento
    hoy = datetime.today().date()
    if fecha_vencimiento.date() < hoy:
        estado = random.choices(estados_pago, weights=[0.7, 0.1, 0.2])[0]
    else:
        estado = random.choices(estados_pago, weights=[0.5, 0.5, 0])[0]

    fecha_pago = None
    if estado == 'Pagado':
        fecha_pago = fake.date_between(start_date=fecha_orden, end_date=fecha_vencimiento)

    pagos.append({
        "pago_id": f"PP-{i+1:06d}",
        "order_id": orden["order_id"],
        "provider_id": provider_id,
        "provider_name": orden["provider_name"],
        "fecha_orden": fecha_orden.date(),
        "condicion_pago": condicion,
        "fecha_vencimiento": fecha_vencimiento.date(),
        "fecha_pago": fecha_pago,
        "monto_total": orden["total"],
        "estado_pago": estado
    })

# Crear DataFrame
df_pagos = pd.DataFrame(pagos)

# Exportar
def exportar_pagos(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/pagos_proveedor.csv', index=False, encoding='utf-8-sig'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/pagos_proveedor.xlsx', index=False)
    }

    for nombre, funcion in formatos.items():
        carpeta_formato = os.path.join(carpeta, nombre.split('/')[0])
        os.makedirs(carpeta_formato, exist_ok=True)
        try:
            funcion()
            print(f"✅ Exportado: {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar {nombre}: {e}")

# Mostrar y exportar
print(df_pagos.head())
exportar_pagos(df_pagos)
print(f"\n✅ Se han generado y exportado {len(df_pagos)} pagos a proveedores con fechas de vencimiento y estado.")
