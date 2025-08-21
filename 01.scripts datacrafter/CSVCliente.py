import random
from faker import Faker
import pandas as pd

# Diccionario de países con su configuración de Faker y prefijo telefónico
localizaciones = {
    'España': {'locale': 'es_ES', 'prefix': '+34'},
    'Estados Unidos': {'locale': 'en_US', 'prefix': '+1'},
    'Francia': {'locale': 'fr_FR', 'prefix': '+33'},
    'Alemania': {'locale': 'de_DE', 'prefix': '+49'},
    'Japón': {'locale': 'ja_JP', 'prefix': '+81'},
    'Brasil': {'locale': 'pt_BR', 'prefix': '+55'},
    'China': {'locale': 'zh_CN', 'prefix': '+86'}
}

# Función para calcular la letra del DNI
def calcular_letra(numero):
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    return letras[int(numero) % 23]

# Función para generar identidad ficticia (DNI o NIE)
def generar_identidad_ficticia():
    tipo = random.choice(['DNI', 'NIE'])
    if tipo == 'DNI':
        numero = random.randint(1000000, 9999999)
        letra = calcular_letra(numero)
        return f"SIM-{numero:07d}{letra}"
    else:
        letra_inicial = random.choice('XYZ')
        numero_base = random.randint(100000, 999999)
        conversion = {'X': '0', 'Y': '1', 'Z': '2'}
        numero_convertido = conversion[letra_inicial] + f"{numero_base:06d}"
        letra_final = calcular_letra(numero_convertido)
        return f"SIM-{letra_inicial}{numero_convertido}{letra_final}"

# Número total de clientes
num_clients = 10000

# Generar datos ficticios de clientes internacionales
clients = []
for i in range(1, num_clients + 1):
    pais = random.choice(list(localizaciones.keys()))
    config = localizaciones[pais]
    fake_local = Faker(config['locale'])

    ciudad = fake_local.city()
    direccion = fake_local.address().replace('\n', ', ')
    telefono = f"{config['prefix']}-{random.randint(100000000, 999999999)}"

    client = {
        'client_id': f"CL-{i:05d}",
        'name': fake_local.first_name(),
        'lastname': fake_local.last_name(),
        'ID': generar_identidad_ficticia(),
        'email': fake_local.email(),
        'phone': telefono,
        'country': pais,
        'city': ciudad,
        'address': direccion,
        'fecha_registro': fake_local.date_between(start_date='-2y', end_date='today'),
        'fecha_nacimiento': fake_local.date_of_birth(minimum_age=18, maximum_age=80),
        'genero': random.choice(['Masculino', 'Femenino', 'Otro']),
        'estado': random.choices(['Activo', 'Inactivo', 'Suspendido'],
          weights=[80, 12, 8],
          k=1
          )[0],
        'canal': random.choice(['Web', 'Tienda física', 'Instagram', 'Referido'])
    }
    clients.append(client)

# Convertir a DataFrame y exportar
df_clients = pd.DataFrame(clients)
df_clients.to_csv('02.descargable/CSV/clientes.csv', index=False)
# Exportar también como JSON
df_clients.to_json('02.descargable/JSON/clientes.json', orient='records', lines=True, force_ascii=False)
print(df_clients.head())
print(f"\n✅ Se han generado y exportado {num_clients} clientes internacionales en el archivo 'clientes.csv'.")