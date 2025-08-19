import random
import pandas as pd
from faker import Faker

fake = Faker()

# Cargar proveedores desde CSV
df_providers = pd.read_csv('proveedores.csv')

# Horarios posibles
horarios = [
    "Lunes a Viernes, 9:00–18:00",
    "Lunes a Sábado, 10:00–20:00",
    "Todos los días, 8:00–22:00",
    "Lunes a Viernes, 8:30–17:30",
    "Martes a Domingo, 11:00–19:00"
]

# Servicios posibles
servicios_posibles = [
    "Atención al cliente",
    "Ventas",
    "Soporte técnico",
    "Logística",
    "Consultoría",
    "Reparaciones",
    "Entrega y recogida"
]

# Prefijos telefónicos por país
prefijos_telefonicos = {
    "Dominican Republic": "+1",
    "España": "+34",
    "México": "+52",
    "Estados Unidos": "+1",
    "Venezuela": "+58",
    "Japón": "+81",
    "Francia": "+33",
    "Italia": "+39",
    "Alemania": "+49",
    "Rusia": "+7",
    "Canadá": "+1"
}

# Función para generar teléfono por país
def generar_telefono_por_pais(pais):
    prefijo = prefijos_telefonicos.get(pais, "+00")
    numero_local = random.randint(600000000, 699999999)
    return f"{prefijo} {numero_local}"

# Número de sucursales ficticias
num_branches = 100

# Generar datos ficticios de sucursales
branches = []
for i in range(1, num_branches + 1):
    proveedor = df_providers.sample(1).iloc[0]
    country = proveedor['country']
    city = proveedor['city']
    
    branches.append({
        'branch_id': f"BR-{i:05d}",
        'provider_id': proveedor['provider_id'],
        'branch_name': f"Sucursal {fake.company_suffix()} {city}",
        'country': country,
        'city': city,
        'phone': generar_telefono_por_pais(country),
        'address': fake.address(),
        'manager': fake.name(),
        'opening_hours': random.choice(horarios),
        'services': ", ".join(random.sample(servicios_posibles, k=random.randint(2, 4)))
    })

# Crear DataFrame
df_branches = pd.DataFrame(branches)

# Exportar a CSV
df_branches.to_csv('sucursales.csv', index=False)

# Mostrar ejemplo
print(df_branches.head())
print(f"\nSe han generado y exportado {num_branches} sucursales ficticias en el archivo 'sucursales.csv'.")

