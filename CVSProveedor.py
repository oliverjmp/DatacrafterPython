import random
from faker import Faker
import pandas as pd

fake = Faker()


# Diccionario de países con ciudades válidas
paises_ciudades = {
    "Dominican Republic": ["Santo Domingo", "Santiago de los Caballeros", "Punta Cana", "La Romana"],
    "España": ["Madrid", "Barcelona", "Valencia", "Sevilla"],
    "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Cancún"],
    "Estados Unidos": ["Nueva York", "Los Ángeles", "Chicago", "Houston"],
    "Venezuela": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto"],
    "Japón": ["Tokio", "Osaka", "Kioto", "Yokohama"],
    "Francia": ["París", "Marsella", "Lyon", "Toulouse"],
    "Italia": ["Roma", "Milán", "Nápoles", "Turín"],
    "Alemania": ["Berlín", "Múnich", "Fráncfort", "Hamburgo"],
    "Rusia": ["Moscú", "San Petersburgo", "Nizhni Nóvgorod", "Ekaterimburgo"],
    "Canadá": ["Toronto", "Vancouver", "Montreal", "Calgary"]
}

# Diccionario de prefijos telefónicos por país
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

# Función para generar NIF español ficticio
def generar_vat_espanol():
    letras = 'ABCDEFGHJNPQRSUVW'
    letra = random.choice(letras)
    numero = random.randint(10000000, 99999999)
    return f"{letra}{numero}"

# Función para generar teléfono con prefijo según país
def generar_telefono_por_pais(pais):
    prefijo = prefijos_telefonicos.get(pais, "+00")  # "+00" como fallback
    numero_local = random.randint(600000000, 699999999)
    return f"{prefijo} {numero_local}"

# Número de proveedores ficticios
num_provider = 100

# Generar datos ficticios de proveedor
provider = []
for i in range(1, num_provider + 1):
    country = random.choice(list(paises_ciudades.keys()))
    city = random.choice(paises_ciudades[country])
    
    provider.append({
        'provider_id': f"PR-{i:05d}",
        'name': fake.company(),
        'nif': generar_vat_espanol(),
        'email': fake.email(),
        'phone': generar_telefono_por_pais(country),
        'country': country,
        'city': city,
        'address': fake.address()
    })

# Crear DataFrame
df_providers = pd.DataFrame(provider)

# Exportar a CSV si lo deseas
df_providers.to_csv('proveedores.csv', index=False)

# Mostrar ejemplo
print(df_providers.head())