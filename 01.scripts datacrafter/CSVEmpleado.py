import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

# Cargar sucursales
df_branches = pd.read_csv("02.descargable/CSV/sucursales.csv", encoding='utf-8-sig')

# Parámetros
roles = ["Manager", "Sub Manager", "Vendedor"]
salarios = {
    "Manager": (2500, 3500),
    "Sub Manager": (1800, 2500),
    "Vendedor": (1200, 1800)
}
status_posibles = ["Activo", "De baja", "De vacaciones", "Despedido"]
horarios = [
    "Lunes a Viernes, 9:00–18:00",
    "Lunes a Sábado, 10:00–20:00",
    "Todos los días, 8:00–22:00",
    "Lunes a Viernes, 8:30–17:30",
    "Martes a Domingo, 11:00–19:00"
]

# Generar empleados
empleados = []
employee_id_counter = 1

for _, row in df_branches.iterrows():
    branch_id = row["branch_id"]
    num_empleados = int(row["num_empleados"])

    for i in range(num_empleados):
        # Asignar rol jerárquico
        if i == 0:
            rol = "Manager"
        elif i == 1:
            rol = "Sub Manager"
        else:
            rol = "Vendedor"

        salario = random.randint(*salarios[rol])
        horas_extras = random.randint(0, 20)
        status = random.choices(status_posibles, weights=[0.85, 0.05, 0.08, 0.02])[0]
        fecha_ingreso = fake.date_between(start_date='-5y', end_date='today')

        # Vacaciones y egreso
        if status == "De vacaciones":
            usados = random.randint(1, 22)
        elif status == "Despedido":
            usados = 22
        else:
            usados = random.randint(0, 15)

        vacaciones_restantes = max(0, 22 - usados)

        if status in ["De baja", "Despedido"]:
            fecha_egreso = fake.date_between(start_date=fecha_ingreso, end_date='today')
        else:
            fecha_egreso = None

        empleados.append({
            "employee_id": f"E-{employee_id_counter:06d}",
            "branch_id": branch_id,
            "nombre": fake.name(),
            "rol": rol,
            "horario": random.choice(horarios),
            "salario_base": salario,
            "horas_extras": horas_extras,
            "status": status,
            "vacaciones_restantes": vacaciones_restantes,
            "fecha_ingreso": fecha_ingreso,
            "fecha_egreso": fecha_egreso
        })
        employee_id_counter += 1

# Crear DataFrame
df_empleados = pd.DataFrame(empleados)

# Exportar empleados
def exportar_empleados(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/Empleados.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/Empleados.json', orient='records', lines=True, force_ascii=False),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/Empleados.xlsx', index=False)
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
print(df_empleados.head())
exportar_empleados(df_empleados)
print(f"\n✅ Se han generado y exportado {len(df_empleados)} empleados con jerarquía, estado laboral y control de vacaciones.")