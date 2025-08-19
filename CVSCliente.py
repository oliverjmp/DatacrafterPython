import random
from faker import Faker
import pandas as pd

fake = Faker()

def calcular_letra(numero):
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    return letras[int(numero) % 23]

def generar_identidad():
    tipo = random.choice(['DNI', 'NIE'])
    if tipo == 'DNI':
        numero = random.randint(10000000, 99999999)
        letra = calcular_letra(numero)
        return f"{numero}{letra}"
    else:  # NIE
        letra_inicial = random.choice('XYZ')
        numero_base = random.randint(1000000, 9999999)
        conversion = {'X': '0', 'Y': '1', 'Z': '2'}
        numero_convertido = conversion[letra_inicial] + f"{numero_base:07d}"
        letra_final = calcular_letra(numero_convertido)
        return f"{letra_inicial}{numero_base:07d}{letra_final}"

def generar_telefono_espanol():
    return f"+34{random.randint(600000000, 699999999)}"

# Número de clientes ficticios
num_clients = 50

# Generar datos ficticios de clientes
clients = [{
    'client_id': f"CL-{i:05d}",  # ID único con prefijo y ceros
    'name': fake.first_name(),
    'lastname': fake.last_name(),
    'ID': generar_identidad(),  # DNI o NIE
    'email': fake.email(),
    'phone': generar_telefono_espanol()
} for i in range(1, num_clients + 1)]

# Convertir a DataFrame
df_clients = pd.DataFrame(clients)

# Exportar a archivo CSV
df_clients.to_csv('clientes.csv', index=False)

# Mostrar ejemplo
print(df_clients.head())
print(f"\nSe han generado y exportado {num_clients} clientes ficticios en el archivo 'clientes.csv'.")