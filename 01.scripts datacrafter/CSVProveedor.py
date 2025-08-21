import random
from faker import Faker
import pandas as pd
import os

# Diccionario de países con ciudades, locale y prefijo
paises_ciudades = {
    "Dominican Republic": {"ciudades": ["Santo Domingo", "Santiago de los Caballeros", "Punta Cana", "La Romana"], "locale": "es_ES", "prefix": "+1-809"},
    "España": {"ciudades": ["Madrid", "Barcelona", "Valencia", "Sevilla"], "locale": "es_ES", "prefix": "+34"},
    "México": {"ciudades": ["Ciudad de México", "Guadalajara", "Monterrey", "Cancún"], "locale": "es_MX", "prefix": "+52"},
    "Estados Unidos": {"ciudades": ["Nueva York", "Los Ángeles", "Chicago", "Houston"], "locale": "en_US", "prefix": "+1"},
    "Venezuela": {"ciudades": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto"], "locale": "es_ES", "prefix": "+58"},
    "Japón": {"ciudades": ["Tokio", "Osaka", "Kioto", "Yokohama"], "locale": "ja_JP", "prefix": "+81"},
    "Francia": {"ciudades": ["París", "Marsella", "Lyon", "Toulouse"], "locale": "fr_FR", "prefix": "+33"},
    "Italia": {"ciudades": ["Roma", "Milán", "Nápoles", "Turín"], "locale": "it_IT", "prefix": "+39"},
    "Alemania": {"ciudades": ["Berlín", "Múnich", "Fráncfort", "Hamburgo"], "locale": "de_DE", "prefix": "+49"},
    "Rusia": {"ciudades": ["Moscú", "San Petersburgo", "Nizhni Nóvgorod", "Ekaterimburgo"], "locale": "ru_RU", "prefix": "+7"},
    "Canadá": {"ciudades": ["Toronto", "Vancouver", "Montreal", "Calgary"], "locale": "en_CA", "prefix": "+1"},
    "Brasil": {"ciudades": ["São Paulo", "Río de Janeiro", "Brasilia", "Salvador"], "locale": "pt_BR", "prefix": "+55"},
    "China": {"ciudades": ["Pekín", "Shanghái", "Guangzhou", "Shenzhen"], "locale": "zh_CN", "prefix": "+86"}
}

# Diccionario de categorías y subcategorías
categorias_subcategorias = {
    'Tecnología': ['Software', 'Hardware', 'Redes', 'Ciberseguridad', 'IoT'],
    'Alimentos': ['Frutas y Verduras', 'Carnes y Embutidos', 'Bebidas', 'Panadería', 'Comida Congelada'],
    'Ropa': ['Moda Hombre', 'Moda Mujer', 'Infantil', 'Deportivo', 'Accesorios'],
    'Electrónica': ['Electrodomésticos', 'Audio y Video', 'Telefonía', 'Computación', 'Gadgets'],
    'Servicios': ['Instalación', 'Reparación'],
    'Accesorios y Repuestos': ['Automotrices', 'Electrodomésticos', 'Tecnológicos', 'Industriales', 'Mecánicos'],
    'Construcción': ['Materiales', 'Maquinaria', 'Herramientas', 'Arquitectura', 'Ingeniería'],
    'Cuidado Personal': ['Cosméticos', 'Farmacéuticos', 'Higiene', 'Spa', 'Nutrición'],
    'Hogar y Decoración': ['Muebles', 'Iluminación', 'Textiles', 'Organización', 'Arte decorativo']
}

# Función para generar NIF español ficticio
def generar_vat_espanol():
    letras = 'ABCDEFGHJNPQRSUVW'
    letra = random.choice(letras)
    numero = random.randint(10000000, 99999999)
    return f"{letra}{numero}"

# Función para generar teléfono con prefijo según país
def generar_telefono_por_pais(prefijo):
    numero_local = random.randint(600000000, 699999999)
    return f"{prefijo} {numero_local}"

# Generar datos ficticios de proveedor
provider = []
provider_id_counter = 1

# Paso 1: asegurar al menos 1 proveedor por subcategoría por país
for pais, config in paises_ciudades.items():
    fake_local = Faker(config['locale'])
    ciudad = random.choice(config['ciudades'])

    for categoria, subcategorias in categorias_subcategorias.items():
        for subcategoria in subcategorias:
            provider.append({
                'provider_id': f"PR-{provider_id_counter:05d}",
                'name': fake_local.company(),
                'nif': generar_vat_espanol(),
                'email': fake_local.email(),
                'phone': generar_telefono_por_pais(config['prefix']),
                'country': pais,
                'city': ciudad,
                'address': fake_local.address().replace('\n', ', '),
                'category': categoria,
                'subcategory': subcategoria
            })
            provider_id_counter += 1

# Paso 2: completar hasta 1500 proveedores con datos aleatorios
while provider_id_counter <= 1500:
    pais = random.choice(list(paises_ciudades.keys()))
    config = paises_ciudades[pais]
    fake_local = Faker(config['locale'])
    ciudad = random.choice(config['ciudades'])

    categoria = random.choice(list(categorias_subcategorias.keys()))
    subcategoria = random.choice(categorias_subcategorias[categoria])

    provider.append({
        'provider_id': f"PR-{provider_id_counter:05d}",
        'name': fake_local.company(),
        'nif': generar_vat_espanol(),
        'email': fake_local.email(),
        'phone': generar_telefono_por_pais(config['prefix']),
        'country': pais,
        'city': ciudad,
        'address': fake_local.address().replace('\n', ', '),
        'category': categoria,
        'subcategory': subcategoria
    })
    provider_id_counter += 1

# Crear DataFrame
df_providers = pd.DataFrame(provider)

def exportar_providers(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df_providers.to_csv(f'{carpeta}/CSV/proveedores.csv', index=False),
        'JSON': lambda: df_providers.to_json(f'{carpeta}/JSON/proveedores.json', orient='records', lines=True, force_ascii=False),
        'SQL': lambda: exportar_sql(df_providers, f'{carpeta}/SQL/proveedores.sql', 'proveedores'),
        'PARQUET': lambda: df_providers.to_parquet(f'{carpeta}/PARQUET/proveedores.parquet', index=False),
        'FEATHER': lambda: df_providers.to_feather(f'{carpeta}/FEATHER/proveedores.feather'),
        'EXCEL': lambda: df_providers.to_excel(f'{carpeta}/XLSX/proveedores.xlsx', index=False)
    }

# Ejecutar exportaciones
    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

def exportar_sql(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")

print(df_providers.head())
exportar_providers(df_providers)
num_providers = len(df_providers)
print(f"\n✅ Se han generado y exportado {num_providers} proveedores internacionales en el archivo 'proveedores .csv'.")