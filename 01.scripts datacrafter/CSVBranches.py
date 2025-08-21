import random
import pandas as pd
from faker import Faker
import os

fake = Faker()

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

# Categorías y subcategorías
categorias_subcategorias = {
    'Tecnología': ['Software', 'Hardware', 'Redes', 'Ciberseguridad', 'IoT'],
    'Alimentos': ['Frutas y Verduras', 'Carnes y Embutidos', 'Bebidas', 'Panadería', 'Comida Congelada'],
    'Ropa': ['Moda Hombre', 'Moda Mujer', 'Infantil', 'Deportivo', 'Accesorios'],
    'Electrónica': ['Electrodomésticos', 'Audio y Video', 'Telefonía', 'Computación', 'Gadgets'],
    'Servicios': ['Instalación', 'Reparación'],
    'Accesorios y Repuestos': ['Automotrices', 'Electrodomésticos', 'Tecnológicos', 'Industriales', 'Mecánicos'],
    'Construcción': ['Materiales', 'Maquinaria', 'Herramientas', 'Arquitectura', 'Ingeniería'],
    'Cuidado Personal': ['Cosméticos', 'Farmacéuticos', 'Higiene', 'Spa', 'Nutrición'],
    'Hogar y Decoración': ['Muebles', 'Iluminación', 'Textiles', 'Organización', 'Arte decorativo'],
    'Productos de Limpieza': ['Desinfectantes', 'Detergentes', 'Ambientadores', 'Limpiadores multiusos', 'Escobas y utensilios']
}

# Tipos de tienda
tipos_tienda = {
    'Tienda Express': {'metros': 200, 'categorias': ['Productos de Limpieza', 'Cuidado Personal', 'Alimentos']},
    'Tienda Mediana': {'metros': 500, 'categorias': ['Productos de Limpieza', 'Cuidado Personal', 'Alimentos', 'Ropa']},
    'Supermercado': {'metros': 1500, 'categorias': ['Productos de Limpieza', 'Cuidado Personal', 'Alimentos', 'Ropa', 'Hogar y Decoración', 'Electrónica']},
    'Hipermercado': {'metros': 3000, 'categorias': ['Productos de Limpieza', 'Cuidado Personal', 'Alimentos', 'Ropa', 'Hogar y Decoración', 'Electrónica', 'Tecnología', 'Servicios', 'Accesorios y Repuestos', 'Construcción']}
}

# Horarios y servicios
horarios = [
    "Lunes a Viernes, 9:00–18:00",
    "Lunes a Sábado, 10:00–20:00",
    "Todos los días, 8:00–22:00",
    "Lunes a Viernes, 8:30–17:30",
    "Martes a Domingo, 11:00–19:00"
]

servicios_posibles = [
    "Atención al cliente", "Ventas", "Soporte técnico", "Logística",
    "Consultoría", "Reparaciones", "Entrega y recogida"
]

# Funciones auxiliares
def generar_telefono_por_pais(pais):
    prefijo = paises_ciudades[pais]['prefix']
    numero_local = random.randint(600000000, 699999999)
    return f"{prefijo} {numero_local}"

def generar_direccion_personalizada(pais, ciudad):
    calle = fake.street_name()
    numero = random.randint(1, 200)
    return f"{calle} {numero}, {ciudad}, {pais}"

# Generar sucursales
branches = []
branch_id_counter = 1
total_tiendas_objetivo = 500
paises = list(paises_ciudades.keys())
tiendas_por_pais = total_tiendas_objetivo // len(paises)

for pais in paises:
    config = paises_ciudades[pais]
    fake_local = Faker(config['locale'])
    ciudad = random.choice(config['ciudades'])

    # Distribución proporcional por tipo
    distribucion = {
        'Hipermercado': 2,
        'Supermercado': 8,
        'Tienda Mediana': 15,
        'Tienda Express': tiendas_por_pais - (2 + 8 + 15)
    }

    for tipo, cantidad in distribucion.items():
        info = tipos_tienda[tipo]
        for _ in range(cantidad):
            categoria = random.choice(info['categorias'])
            subcategoria = random.choice(categorias_subcategorias[categoria])

            branches.append({
                'branch_id': f"BR-{branch_id_counter:05d}",
                'store_type': tipo,
                'size_m2': info['metros'],
                'category': categoria,
                'subcategory': subcategoria,
                'country': pais,
                'city': ciudad,
                'address': generar_direccion_personalizada(pais, ciudad),
                'phone': generar_telefono_por_pais(pais),
                'manager': fake_local.name(),
                'opening_hours': random.choice(horarios),
                'services': ", ".join(random.sample(servicios_posibles, k=random.randint(2, 4)))
            })
            branch_id_counter += 1

# Exportar
df_branches = pd.DataFrame(branches)
os.makedirs('02.descargable/CSV', exist_ok=True)
def exportar_branches(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df_branches.to_csv(f'{carpeta}/CSV/sucursales.csv', index=False),
        'JSON': lambda: df_branches.to_json(f'{carpeta}/JSON/sucursales.json', orient='records', lines=True, force_ascii=False),
        'SQL': lambda: exportar_sql(df_branches, f'{carpeta}/SQL/sucursales.sql', 'sucursales'),
        'PARQUET': lambda: df_branches.to_parquet(f'{carpeta}/PARQUET/sucursales.parquet', index=False),
        'FEATHER': lambda: df_branches.to_feather(f'{carpeta}/FEATHER/sucursales.feather'),
        'EXCEL': lambda: df_branches.to_excel(f'{carpeta}/XLSX/sucursales.xlsx', index=False)
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

print(df_branches.head())
exportar_branches(df_branches)
num_branches = len(df_branches)
print(f"\n✅ Se han generado y exportado {num_branches} sucursales en el archivo 'sucursales'.")