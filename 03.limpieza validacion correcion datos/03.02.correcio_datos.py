# 📦 Importación de librerías
import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ✅ Funciones de validación
def validar_id(val): 
    return bool(re.match(r"^CL-\d{5}$", str(val)))

def validar_email(val): 
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", str(val)))

def validar_telefono(val): 
    return bool(re.match(r"^\d{10,15}$", re.sub(r"\D", "", str(val))))

def validar_fecha(val):
    try:
        datetime.strptime(str(val), "%Y-%m-%d")
        return True
    except:
        return False

# 📁 Carga de datos
RUTA_ARCHIVO = "02.descargable/CSV/02.CSV con errores/clientesError.csv"
df_original = pd.read_csv(RUTA_ARCHIVO, encoding='utf-8-sig')
df_clientes = df_original.copy()

# 🧹 Corrección automática de errores

# 1. Género inválido → "No especificado"
VALORES_GENERO_VALIDOS = ["Femenino", "Masculino"]
df_clientes['genero'] = df_clientes['genero'].apply(lambda x: x if x in VALORES_GENERO_VALIDOS else "No especificado")

# 2. Teléfonos → eliminar símbolos y normalizar
def limpiar_telefono(val):
    num = re.sub(r"\D", "", str(val))
    return num if 10 <= len(num) <= 15 else None

df_clientes['telefono'] = df_clientes['telefono'].apply(limpiar_telefono)

# 3. Fechas → convertir y rellenar inválidas con fecha por defecto
def corregir_fecha(val):
    try:
        return datetime.strptime(str(val), "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        return "2000-01-01"

df_clientes['fecha_registro'] = df_clientes['fecha_registro'].apply(corregir_fecha)

# 4. Eliminar duplicados
df_clientes = df_clientes.drop_duplicates()

# 5. Generar nuevos IDs para registros inválidos
df_clientes['id_valido'] = df_clientes['client_id'].apply(validar_id)
ids_validos = df_clientes[df_clientes['id_valido']]['client_id']
numeros_existentes = ids_validos.str.extract(r"CL-(\d{5})")[0].astype(int)
contador = numeros_existentes.max() + 1 if not numeros_existentes.empty else 10000

def generar_id(row):
    global contador
    if row['id_valido']:
        return row['client_id']
    nuevo_id = f"CL-{contador:05d}"
    contador += 1
    return nuevo_id

df_clientes['client_id'] = df_clientes.apply(generar_id, axis=1)
df_clientes.drop(columns=['id_valido'], inplace=True)

print("\n✅ Corrección automática completada. Todos los campos han sido limpiados y los IDs inválidos regenerados.")

# 🧮 Revalidación después de corrección
def validar_registro(row):
    return validar_id(row['client_id']) and \
           validar_email(row['email']) and \
           validar_telefono(row['telefono']) and \
           validar_fecha(row['fecha_registro']) and \
           row['genero'] in VALORES_GENERO_VALIDOS and \
           pd.notnull(row['telefono']) and \
           pd.notnull(row['fecha_registro'])

df_clientes['registro_valido'] = df_clientes.apply(validar_registro, axis=1)

# 📤 Separar registros corregidos vs no reparables
df_limpio = df_clientes[df_clientes['registro_valido'] == True].copy()
df_con_errores = df_clientes[df_clientes['registro_valido'] == False].copy()

# 🧾 Generar log de motivos de descarte
def motivos_descarte(row):
    motivos = []
    if not validar_id(row['client_id']): motivos.append("ID inválido")
    if not validar_email(row['email']): motivos.append("Email inválido")
    if not validar_telefono(row['telefono']): motivos.append("Teléfono inválido")
    if not validar_fecha(row['fecha_registro']): motivos.append("Fecha inválida")
    if row['genero'] not in VALORES_GENERO_VALIDOS: motivos.append("Género inválido")
    if pd.isnull(row['telefono']): motivos.append("Teléfono ausente")
    if pd.isnull(row['fecha_registro']): motivos.append("Fecha ausente")
    return ", ".join(motivos) if motivos else "Desconocido"

df_con_errores['motivo_descarte'] = df_con_errores.apply(motivos_descarte, axis=1)

# 📁 Crear carpeta de salida si no existe
os.makedirs("02.descargable/CSV/03.CSV Limpiados", exist_ok=True)

# 📤 Exportar archivos
df_limpio.to_csv("02.descargable/CSV/03.CSV Limpiados/clientes_limpios.csv", index=False)
df_con_errores.to_csv("02.descargable/CSV/03.CSV Limpiados/clientes_no_reparables_log.csv", index=False)

# 📊 Tabla resumen
total_original = len(df_original)
total_procesado = len(df_clientes)
total_validos = len(df_limpio)
total_invalidos = len(df_con_errores)

resumen = pd.DataFrame({
    'Categoría': [
        'Registros válidos después de corrección',
        'Registros no reparables',
        'Total de registros procesados',
        'Total original de registros',
        'Registros perdidos en el proceso'
    ],
    'Cantidad': [
        total_validos,
        total_invalidos,
        total_procesado,
        total_original,
        total_original - total_procesado
    ]
})

print("\n📋 Resumen de calidad de datos:")
print(resumen)

# 📊 Comparación entre registros válidos y no reparables

# Totales
total_validos = len(df_limpio)
total_invalidos = len(df_con_errores)
total = total_validos + total_invalidos

# 📋 Resumen de Calidad de Datos

# Totales
total_original = len(df_original)
total_procesado = len(df_clientes)
total_validos = len(df_limpio)
total_invalidos = len(df_con_errores)
registros_perdidos = total_original - total_procesado

# Crear tabla resumen
resumen_calidad = pd.DataFrame({
    'Estado del registro': [
        '✅ Registros válidos después de corrección',
        '❌ Registros no reparables',
        '📦 Total de registros procesados',
        '📂 Total original de registros',
        '🕳️ Registros perdidos en el proceso'
    ],
    'Cantidad': [
        total_validos,
        total_invalidos,
        total_procesado,
        total_original,
        registros_perdidos
    ]
})

# Mostrar tabla
print("\n📋 Resumen de Calidad de Datos:")
print(resumen_calidad)


# Crear tabla comparativa
tabla_comparativa = pd.DataFrame({
    '🧾 Estado del Registro': ['Válidos (Fin exitoso)', 'No reparables (Descartados)'],
    'Cantidad de registros': [total_validos, total_invalidos],
    'Porcentaje del total': [f"{(total_validos/total)*100:.2f} %", f"{(total_invalidos/total)*100:.2f} %"],
    'ID válido': ['✅ Regenerado si necesario', '❌ Ausente o mal formado'],
    'Email válido': ['✅ Corregido si posible', '❌ Formato inválido o nulo'],
    'Teléfono válido': ['✅ Normalizado', '❌ Letras o longitud incorrecta'],
    'Fecha válida': ['✅ Corregida o imputada', '❌ Futura o malformada'],
    'Género válido': ['✅ Reasignado si inválido', '❌ Valor no reconocido'],
    'Utilidad para análisis': ['Alta', 'Nula']
})

# Mostrar tabla
print("\n📊 Comparación de registros procesados:")
print(tabla_comparativa)


# 🔍 Verificación de registros perdidos tras la limpieza

# 1. Comparar el total original con el total procesado
print("Total original de registros:", len(df_original))
print("Total después de limpieza:", len(df_clientes))

# 2. Detectar si hay registros faltantes por índice
print("\n🔍 Verificación de registros perdidos tras la limpieza:")
faltantes = set(df_original.index) - set(df_clientes.index)
print("\nÍndices faltantes:", faltantes)

# 3. Inspeccionar el registro descartado
if faltantes:
    registro_descartado = df_original.loc[list(faltantes)]
    print("\n📌 Registro descartado:")
    print(registro_descartado)


# 🔍 Función para convertir índice de pandas a línea en CSV
def indice_a_linea_csv(indice_pandas, tiene_encabezado=True):
    """
    Convierte un índice de pandas al número de línea en el archivo CSV.
    Si el CSV tiene encabezado, suma 2 (1 por encabezado + 1 porque pandas empieza en 0).
    """
    return indice_pandas + (2 if tiene_encabezado else 1)

# 🔍 Función para convertir línea del CSV a índice en pandas
def linea_csv_a_indice(linea_csv, tiene_encabezado=True):
    """
    Convierte una línea del CSV al índice correspondiente en pandas.
    Si el CSV tiene encabezado, resta 2 (1 por encabezado + 1 porque pandas empieza en 0).
    """
    return linea_csv - (2 if tiene_encabezado else 1)
# ¿Qué línea del CSV corresponde al índice 2879?
print("\nLínea en CSV:", indice_a_linea_csv(2879))  # Resultado: 2881

# ¿Qué índice en pandas corresponde a la línea 2881 del CSV?
print("Índice en pandas:", linea_csv_a_indice(2881))  # Resultado: 2879

print("\n---------FIN------------")

