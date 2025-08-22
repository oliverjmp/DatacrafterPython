import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# Cargar productos e inventario
df_productos = pd.read_csv("02.descargable/CSV/productos.csv", encoding='utf-8-sig')
df_inventario = pd.read_csv("02.descargable/CSV/inventario.csv", encoding='utf-8-sig')

# Crear índice rápido de productos
producto_map = df_productos.set_index("product_id")[["provider_id", "provider_name", "price"]].to_dict("index")

# Generar órdenes de compra
ordenes = []
order_id_counter = 1
estados = ["Pendiente", "En tránsito", "Recibido"]

for _, row in df_inventario.iterrows():
    product_id = row["product_id"]
    branch_id = row["branch_id"]
    stock_actual = row["stock_actual"]
    stock_minimo = row["stock_minimo"]

    if stock_actual <= stock_minimo:
        proveedor = producto_map.get(product_id)
        if not proveedor or pd.isna(proveedor["provider_id"]):
            continue

        cantidad = random.randint(20, 100)
        precio_unitario = round(proveedor["price"], 2)
        total = round(cantidad * precio_unitario, 2)
        fecha_orden = fake.date_between(start_date='-60d', end_date='today')
        estado = random.choice(estados)

        ordenes.append({
            "order_id": f"O-{order_id_counter:06d}",
            "branch_id": branch_id,
            "product_id": product_id,
            "provider_id": proveedor["provider_id"],
            "provider_name": proveedor["provider_name"],
            "fecha_orden": fecha_orden,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total,
            "estado": estado
        })
        order_id_counter += 1

# Crear DataFrame
df_ordenes = pd.DataFrame(ordenes)

# Exportar
def exportar_ordenes(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/compras_proveedor.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/compras_proveedor.json', orient='records', lines=True, force_ascii=False),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/compras_proveedor.xlsx', index=False)
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
print(df_ordenes.head())
exportar_ordenes(df_ordenes)
print(f"\n✅ Se han generado y exportado {len(df_ordenes)} órdenes de compra por proveedor.")