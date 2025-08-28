import random   
from faker import Faker
import pandas as pd
import os

fake = Faker()

# Cargar sucursales
df_branches = pd.read_csv('02.descargable/CSV/01.CSV correctos/sucursales.csv', encoding='utf-8-sig')

# Cargar productos
df_productos = pd.read_csv('02.descargable/CSV/01.CSV correctos/productos.csv', encoding='utf-8-sig')

# Cargar proveedores
df_proveedores = pd.read_csv("02.descargable/CSV/01.CSV correctos/proveedores.csv")

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

def exportar_sql_productos(df, ruta, nombre_tabla):
    with open(ruta, 'w', encoding='utf-8') as f:
        # 🏗️ Crear tabla productos
        f.write(f"-- Crear tabla {nombre_tabla}\n")
        f.write(f"CREATE TABLE {nombre_tabla} (\n")
        f.write("    product_id VARCHAR(10) PRIMARY KEY,\n")
        f.write("    name VARCHAR(100),\n")
        f.write("    subcategory VARCHAR(50),\n")
        f.write("    branch_id VARCHAR(10),\n")
        f.write("    provider_id VARCHAR(8),\n")
        f.write("    provider_name VARCHAR(100)\n")
        f.write(");\n\n")

        # 📥 Insertar datos
        for _, row in df.iterrows():
            columnas = ', '.join(df.columns)
            valores = ', '.join([f"'{str(valor).replace('\'', '\'\'')}'" for valor in row])
            f.write(f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({valores});\n")


# Exportar productos enriquecidos
def exportar_productos(df, carpeta='02.descargable'):
    formatos = {
        'CSV': lambda: df.to_csv(f'{carpeta}/CSV/01.CSV correctos/productos.csv', index=False, encoding='utf-8-sig'),
        'JSON': lambda: df.to_json(f'{carpeta}/JSON/01.JSON correctos/productos.json', orient='records', lines=True, force_ascii=False),
        'JSON_EXCEL': lambda: df.to_json(f'{carpeta}/JSON para excel/01.JSON para excel correctos/productos.json', orient='table'),
        'SQL': lambda: exportar_sql_productos(df, f'{carpeta}/SQL/01.SQL correctos/productos.sql', 'Productos'),
        'PARQUET': lambda: df.to_parquet(f'{carpeta}/PARQUET/01.PARQUET correctos/productos.parquet', index=False),
        'FEATHER': lambda: df.to_feather(f'{carpeta}/FEATHER/01.FEATHER correctos/productos.feather'),
        'EXCEL': lambda: df.to_excel(f'{carpeta}/XLSX/01.XLSX correctos/productos.xlsx', index=False)
    }

# Ejecutar exportaciones
    for nombre, funcion in formatos.items():
        try:
            funcion()
            print(f"✅ Exportado en formato {nombre}")
        except Exception as e:
            print(f"⚠️ Error al exportar en {nombre}: {e}")

# Mostrar y exportar
print(df_productos.head())
exportar_productos(df_productos)
print(f"\n✅ Se han generado y exportado {len(df_productos)} productos con proveedor asociado.")
