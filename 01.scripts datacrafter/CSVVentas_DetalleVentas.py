import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# Cargar productos, inventario y empleados
df_productos = pd.read_csv("02.descargable/CSV/productos.csv", encoding='utf-8-sig')
df_inventario = pd.read_csv("02.descargable/CSV/inventario.csv", encoding='utf-8-sig')
df_empleados = pd.read_csv("02.descargable/CSV/Empleados.csv", encoding='utf-8-sig')

# Canales y ajustes
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

# Índice rápido de stock disponible
stock_map = df_inventario.set_index("product_id")[["stock_actual", "branch_id"]].to_dict("index")

# Índice de empleados activos por sucursal
empleados_por_sucursal = (
    df_empleados[df_empleados["status"] == "Activo"]
    .groupby("branch_id")["employee_id"]
    .apply(list)
    .to_dict()
)

compras = []
detalles = []
purchase_id_counter = 1

# Simular compras
num_compras = 5000
for _ in range(num_compras):
    purchase_id = f"C-{purchase_id_counter:06d}"
    cliente = fake.name()
    fecha = fake.date_between(start_date='-90d', end_date='today')
    canal = random.choice(canales)
    metodo_pago = random.choice(metodos_pago[canal])
    ajuste = ajustes_precio[canal]

    productos_compra = df_productos.sample(random.randint(1, 5))
    total_compra = 0
    branch_id = None

    for _, prod in productos_compra.iterrows():
        product_id = prod["product_id"]
        precio_base = prod["price"]
        branch_id = prod["branch_id"]

        stock_info = stock_map.get(product_id)
        if not stock_info or stock_info["stock_actual"] <= 0:
            continue

        cantidad = random.randint(1, min(5, stock_info["stock_actual"]))
        precio_ajustado = round(precio_base * ajuste, 2)
        subtotal = round(cantidad * precio_ajustado, 2)
        total_compra += subtotal

        detalles.append({
            "purchase_id": purchase_id,
            "product_id": product_id,
            "cantidad": cantidad,
            "precio_unitario": precio_ajustado,
            "subtotal": subtotal
        })

        stock_map[product_id]["stock_actual"] -= cantidad

    if total_compra > 0:
        empleados_disponibles = empleados_por_sucursal.get(branch_id, [])
        employee_id = random.choice(empleados_disponibles) if empleados_disponibles else None

        compras.append({
            "purchase_id": purchase_id,
            "branch_id": branch_id,
            "cliente": cliente,
            "fecha": fecha,
            "canal": canal,
            "metodo_pago": metodo_pago,
            "employee_id": employee_id,
            "total": round(total_compra, 2)
        })
        purchase_id_counter += 1

# Crear DataFrames
df_compras = pd.DataFrame(compras)
df_detalles = pd.DataFrame(detalles)

# Exportar
def exportar_compras(df1, df2, carpeta='02.descargable'):
    rutas = {
        "ventas.csv": df1,
        "detalle_ventas.csv": df2
    }
    for nombre, df in rutas.items():
        ruta = os.path.join(carpeta, "CSV", nombre)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        df.to_csv(ruta, index=False, encoding='utf-8-sig')
        print(f"✅ Exportado: {nombre}")

# Mostrar y exportar
print(df_compras.head())
print(df_detalles.head())
exportar_compras(df_compras, df_detalles)
print(f"\n✅ Se han generado {len(df_compras)} compras y {len(df_detalles)} líneas de detalle.")

