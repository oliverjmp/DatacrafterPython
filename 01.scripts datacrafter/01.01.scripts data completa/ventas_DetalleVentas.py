import pandas as pd
import random
from faker import Faker
from datetime import timedelta
import os

fake = Faker()

# Cargar datos base
df_productos = pd.read_csv("02.descargable/CSV/01.CSV correctos/productos.csv", encoding='utf-8-sig')
df_inventario = pd.read_csv("02.descargable/CSV/01.CSV correctos/inventario.csv", encoding='utf-8-sig')
df_empleados = pd.read_csv("02.descargable/CSV/01.CSV correctos/Empleados.csv", encoding='utf-8-sig')
df_clientes = pd.read_csv("02.descargable/CSV/01.CSV correctos/clientes.csv", encoding='utf-8-sig')

# Índices rápidos
client_ids = df_clientes["client_id"].tolist()
stock_map = df_inventario.set_index("product_id")[["stock_actual", "branch_id"]].to_dict("index")
empleados_por_sucursal = (
    df_empleados[df_empleados["status"] == "Activo"]
    .groupby("branch_id")["employee_id"]
    .apply(list)
    .to_dict()
)

# Configuración de ventas
canales = ['Presencial', 'Página Web', 'Amazon', 'Instagram', 'Distribuidor']
ajustes_precio = {
    'Presencial': 1.00,
    'Página Web': 0.95,
    'Amazon': 1.10,
    'Instagram': 0.97,
    'Distribuidor': 0.85
}
metodos_pago = {
    'Presencial': ['Efectivo', 'Tarjeta'],
    'Página Web': ['Tarjeta', 'PayPal'],
    'Amazon': ['Amazon Pay', 'Tarjeta'],
    'Instagram': ['Bizum', 'Transferencia'],
    'Distribuidor': ['Transferencia']
}

ventas = []
detalles = []
purchase_id_counter = 1
num_ventas = 5000

# Simulación de ventas
for _ in range(num_ventas):
    purchase_id = f"C-{purchase_id_counter:06d}"
    client_id = random.choice(client_ids)
    fecha = fake.date_between(start_date='-90d', end_date='today')
    canal = random.choice(canales)
    metodo_pago = random.choice(metodos_pago[canal])
    ajuste = ajustes_precio[canal]
    productos_venta = df_productos.sample(random.randint(1, 5))
    total_venta = 0
    branch_id = None

    for _, prod in productos_venta.iterrows():
        product_id = prod["product_id"]
        precio_base = prod["price"]
        branch_id = prod["branch_id"]
        stock_info = stock_map.get(product_id)

        if not stock_info or stock_info["stock_actual"] <= 0:
            continue

        cantidad = random.randint(1, min(5, stock_info["stock_actual"]))
        precio_ajustado = round(precio_base * ajuste, 2)
        subtotal = round(cantidad * precio_ajustado, 2)
        total_venta += subtotal

        detalles.append({
            "purchase_id": purchase_id,
            "product_id": product_id,
            "cantidad": cantidad,
            "precio_unitario": precio_ajustado,
            "subtotal": subtotal
        })

        stock_map[product_id]["stock_actual"] -= cantidad

    if total_venta > 0:
        empleados_disponibles = empleados_por_sucursal.get(branch_id, [])
        employee_id = random.choice(empleados_disponibles) if empleados_disponibles else None

        ventas.append({
            "purchase_id": purchase_id,
            "branch_id": branch_id,
            "client_id": client_id,
            "fecha": fecha,
            "canal": canal,
            "metodo_pago": metodo_pago,
            "employee_id": employee_id,
            "total": round(total_venta, 2)
        })
        purchase_id_counter += 1

# Crear DataFrames
df_ventas = pd.DataFrame(ventas)
df_detalles = pd.DataFrame(detalles)

# Función para exportar en SQL
def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

# Función para exportar en múltiples formatos
def exportar_ventas(df1, df2, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: (
            df1.to_csv(f'{carpeta}/CSV/01.CSV correctos/ventas.csv', index=False, encoding='utf-8-sig'),
            df2.to_csv(f'{carpeta}/CSV/01.CSV correctos/detalle_ventas.csv', index=False, encoding='utf-8-sig')
        ),
        'JSON': lambda: (
            df1.to_json(f'{carpeta}/JSON/01.JSON correctos/ventas.json', orient='records', lines=True, force_ascii=False),
            df2.to_json(f'{carpeta}/JSON/01.JSON correctos/detalle_ventas.json', orient='records', lines=True, force_ascii=False)
        ),
        'JSON_EXCEL': lambda: (
            df1.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/ventas.json', orient='table'),
            df2.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/detalle_ventas.json', orient='table')
        ),
        'SQL': lambda: (
            exportar_sql(df1, f'{carpeta}/SQL/01.SQL correctos/ventas.sql', 'Ventas'),
            exportar_sql(df2, f'{carpeta}/SQL/01.SQL correctos/detalle_ventas.sql', 'DetalleVentas')
        ),
        'PARQUET': lambda: (
            df1.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/ventas.parquet', index=False),
            df2.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/detalle_ventas.parquet', index=False)
        ),
        'FEATHER': lambda: (
            df1.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/ventas.feather'),
            df2.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/detalle_ventas.feather')
        ),
        'EXCEL': lambda: (
            df1.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/ventas.xlsx', index=False),
            df2.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/detalle_ventas.xlsx', index=False)
        )
    }

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_ventas.head())
print(df_detalles.head())
exportar_ventas(df_ventas, df_detalles)
print(f"\n✅ Se han generado {len(df_ventas)} ventas y {len(df_detalles)} líneas de detalle con client_id normalizado.")
