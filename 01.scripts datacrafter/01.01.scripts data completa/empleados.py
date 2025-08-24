import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

# Cargar sucursales
df_branches = pd.read_csv("02.descargable/CSV/01.CSV correctos/sucursales.csv", encoding='utf-8-sig')

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

def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")


# Exportar empleados
def exportar_empleados(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df_empleados.to_csv(f'{carpeta}/CSV/01.CSV correctos/Empleados.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df_empleados.to_json(f'{carpeta}/JSON/01.JSON correctos/Empleados.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df_empleados.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/Empleados.json', orient='table'),
        'SQL': lambda: exportar_sql(df_empleados, f'{carpeta}/SQL/01.SQL correctos/Empleados.sql', 'Empleados'),
        'PARQUET': lambda: df_empleados.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/Empleados.parquet', index=False),
        'FEATHER': lambda: df_empleados.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/Empleados.feather'),
        'EXCEL': lambda: df_empleados.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/Empleados.xlsx', index=False)
    }

    # Ejecutar exportaciones
    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_empleados.head())
exportar_empleados(df_empleados)
print(f"\n✅ Se han generado y exportado {len(df_empleados)} empleados con jerarquía, estado laboral y control de vacaciones.")