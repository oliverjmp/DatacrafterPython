import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

# Cargar sucursales
df_branches = pd.read_csv('sucursales.csv')

# Roles y salarios
roles = ['Manager', 'Vendedor', 'Conductor', 'Mozo de almacén', 'Cajero', 'Reponedor', 'Servicio técnico', 'Limpieza']
salarios = {
    'Manager': (1800, 2500),
    'Vendedor': (1200, 1600),
    'Conductor': (1300, 1700),
    'Mozo de almacén': (1100, 1500),
    'Cajero': (1000, 1400),
    'Reponedor': (1000, 1300),
    'Servicio técnico': (1400, 1800),
    'Limpieza': (900, 1200)
}

# Turnos y horarios
turnos = {
    'Mañana': '08:00–16:00',
    'Tarde': '14:00–22:00',
    'Noche': '22:00–06:00'
}
dias_posibles = ['Lunes a Viernes', 'Martes a Sábado', 'Miércoles a Domingo', 'Turno rotativo']

empleados = []

for i in range(1, 301):
    sucursal = df_branches.sample(1).iloc[0]
    rol = random.choice(roles)
    salario = round(random.uniform(*salarios[rol]), 2)
    turno = random.choice(list(turnos.keys()))
    horario = turnos[turno]
    dias = random.choice(dias_posibles)
    
    empleados.append({
        'employee_id': f"EMP-{i:05d}",
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'branch_id': sucursal['branch_id'],
        'role': rol,
        'fecha_ingreso': fake.date_between(start_date='-3y', end_date='today'),
        'salario': salario,
        'turno': turno,
        'horario': horario,
        'dias_trabajo': dias
    })

df_empleados = pd.DataFrame(empleados)
df_empleados.to_csv('empleados.csv', index=False)

print(df_empleados.head())
print(f"\n✅ Se han generado 300 empleados con roles, turnos y horarios en 'empleados.csv'.")
