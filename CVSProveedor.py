import random
from faker import Faker
import pandas as pd

fake = Faker()

def generar_telefono():
    return f"+25-{random.randint(100000000, 199999999)}"


def generar_vat_espanol():
    letras = 'DEGHJNPQRSUVW'  # Letras válidas para empresas
    letra = random.choice(letras)
    numero = random.randint(10000000, 99999999)
    return f"{letra}{numero}"


# Número de proveedor ficticios
num_provider = 50

# Generar datos ficticios de proveedor
provider = [{
    'provider_id': f"PR-{i:05d}",  # ID único con prefijo y ceros
    'name': fake.company(),
    'nif': generar_vat_espanol(),
    'email': fake.email(),
    'phone': generar_telefono()
} for i in range(1, num_provider + 1)]

df_providers = pd.DataFrame(provider)

# Exportar a archivo CSV
df_providers.to_csv('proveedores.csv', index=False)

# Imprimir ejemplo
print(df_providers.head())