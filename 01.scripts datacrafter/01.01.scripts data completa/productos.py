import random   
from faker import Faker
import pandas as pd
import os

fake = Faker()

# Cargar sucursales
df_branches = pd.read_csv('02.descargable/CSV/sucursales.csv', encoding='utf-8-sig')

# Cargar productos
df_productos = pd.read_csv('02.descargable/CSV/productos.csv', encoding='utf-8-sig')

# Cargar proveedores
df_proveedores = pd.read_csv("02.descargable/CSV/proveedores.csv")

# Validar columnas necesarias
required_columns = ["provider_id", "name", "country", "subcategory"]
missing = [col for col in required_columns if col not in df_proveedores.columns]
if missing:
    raise ValueError(f"❌ Faltan columnas en proveedores.csv: {missing}")

# Normalizar campos para comparación
df_proveedores["subcategory"] = df_proveedores["subcategory"].astype(str).str.strip().str.lower()
df_proveedores["country"] = df_proveedores["country"].astype(str).str.strip()

# Crear mapeo rápido de branch_id → country
branch_country_map = df_branches.set_index("branch_id")["country"].to_dict()

# Función para encontrar proveedor compatible
def encontrar_proveedor(pais, subcategoria):
    subcat = subcategoria.strip().lower()
    posibles = df_proveedores[
        (df_proveedores["country"] == pais) &
        (df_proveedores["subcategory"] == subcat)
    ]
    if not posibles.empty:
        proveedor = posibles.sample(1).iloc[0]
        return proveedor["provider_id"], proveedor["name"]
    else:
        return None, None

# Asociar proveedor a cada producto
df_productos["provider_id"] = None
df_productos["provider_name"] = None

for idx, row in df_productos.iterrows():
    pais = branch_country_map.get(row["branch_id"], None)
    subcat = row["subcategory"]
    prov_id, prov_name = encontrar_proveedor(pais, subcat)
    df_productos.at[idx, "provider_id"] = prov_id
    df_productos.at[idx, "provider_name"] = prov_name

# Reporte de cobertura
sin_proveedor = df_productos["provider_id"].isna().sum()
print(f"🔍 Productos sin proveedor asignado: {sin_proveedor} de {len(df_productos)}")

# Exportar productos enriquecidos
def exportar_productos(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/productos.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/productos.json', orient='records', lines=True, force_ascii=False),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/productos.xlsx', index=False)
    }

    for formato in formatos:
        carpeta_formato = os.path.join(carpeta, formato)
        os.makedirs(carpeta_formato, exist_ok=True)

    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Productos exportados en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar productos en {nombre}: {e}")

# Mostrar y exportar
print(df_productos.head())
exportar_productos(df_productos)
print(f"\n✅ Se han generado y exportado {len(df_productos)} productos con proveedor asociado.")
