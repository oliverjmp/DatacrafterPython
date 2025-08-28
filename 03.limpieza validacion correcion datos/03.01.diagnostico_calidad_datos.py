# 📦 Importación de librerías
import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# 📁 Carga de datos
RUTA_ARCHIVO = "02.descargable/CSV/02.CSV con errores/clientesError.csv"
df_clientes = pd.read_csv(RUTA_ARCHIVO, encoding='utf-8-sig')

# ✅ Funciones de validación
def validar_id(val): return bool(re.match(r"^CL-\d{5}$", str(val)))
def validar_email(val): return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", str(val)))
def validar_telefono(val): return bool(re.match(r"^\d{10,15}$", re.sub(r"\D", "", str(val))))
def validar_fecha(val):
    try:
        datetime.strptime(str(val), "%Y-%m-%d")
        return True
    except:
        return False

# 🎯 Validación de registros
VALORES_GENERO_VALIDOS = ["Femenino", "Masculino"]

errores_df = pd.DataFrame({
    'id_invalido': ~df_clientes['client_id'].apply(validar_id),
    'email_invalido': ~df_clientes['email'].apply(validar_email),
    'telefono_invalido': ~df_clientes['telefono'].apply(validar_telefono),
    'fecha_invalida': ~df_clientes['fecha_registro'].apply(validar_fecha),
    'semantico': ~df_clientes['genero'].isin(VALORES_GENERO_VALIDOS),
    'faltante': df_clientes.isnull().any(axis=1),
    'duplicado': df_clientes.duplicated()
})

# 🧮 Cálculo de errores sintácticos por registro
errores_df['sintactico'] = errores_df[['id_invalido', 'email_invalido', 'telefono_invalido', 'fecha_invalida']].any(axis=1)
errores_df['total_errores'] = errores_df[['sintactico', 'semantico', 'faltante', 'duplicado']].sum(axis=1)

# 📊 Clasificación por gravedad
def clasificar_gravedad(n):
    if n >= 3: return "Alta"
    elif n == 2: return "Media"
    elif n == 1: return "Baja"
    else: return "Sin errores"

errores_df['gravedad'] = errores_df['total_errores'].apply(clasificar_gravedad)

# 📈 Distribución de errores por registro
distribucion = errores_df['total_errores'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
bars = plt.bar(distribucion.index, distribucion.values, color='skyblue', edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, str(int(yval)), ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("📊 Distribución de errores por registro", fontsize=14, fontweight='bold')
plt.xlabel("Cantidad de errores en un registro")
plt.ylabel("Número de registros")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 📌 Resumen por tipo de error
resumen_errores = errores_df[['sintactico', 'semantico', 'faltante', 'duplicado']].sum().reset_index()
resumen_errores.columns = ['Tipo de error', 'Cantidad de registros']
plt.figure(figsize=(10, 6))
bars = plt.bar(resumen_errores['Tipo de error'], resumen_errores['Cantidad de registros'], color='salmon', edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, str(int(yval)), ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("📌 Cantidad de registros por tipo de error", fontsize=14, fontweight='bold')
plt.xlabel("Tipo de error")
plt.ylabel("Cantidad")
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 📋 Desglose por cantidad de errores
desglose = []
for n in sorted(errores_df['total_errores'].unique()):
    subset = errores_df[errores_df['total_errores'] == n]
    desglose.append({
        'Cantidad de errores': n,
        'Sintáctico': subset['sintactico'].sum(),
        'Semántico': subset['semantico'].sum(),
        'Faltante': subset['faltante'].sum(),
        'Duplicado': subset['duplicado'].sum()
    })
tabla_desglose = pd.DataFrame(desglose)
print("\n📋 Desglose de errores por tipo y cantidad de errores:")
print(tabla_desglose)

# 🧪 Errores sintácticos por campo
errores_sintacticos = {
    'ID inválido': errores_df['id_invalido'].sum(),
    'Email inválido': errores_df['email_invalido'].sum(),
    'Teléfono inválido': errores_df['telefono_invalido'].sum(),
    'Fecha inválida': errores_df['fecha_invalida'].sum()
}
print("\n🧪 Cantidad de errores sintácticos por tipo:")
for tipo, cantidad in errores_sintacticos.items():
    print(f"{tipo}: {cantidad}")
print(f"Total de errores sintácticos: {sum(errores_sintacticos.values())}")

# 📊 Distribución de errores sintácticos por registro
errores_df['errores_sintacticos_por_registro'] = errores_df[['id_invalido', 'email_invalido', 'telefono_invalido', 'fecha_invalida']].sum(axis=1)
distribucion_sintacticos = errores_df['errores_sintacticos_por_registro'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
bars = plt.bar(distribucion_sintacticos.index, distribucion_sintacticos.values, color='lightcoral', edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, str(int(yval)), ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("📈 Distribución de errores sintácticos por registro", fontsize=14, fontweight='bold')
plt.xlabel("Cantidad de errores sintácticos en un registro")
plt.ylabel("Número de registros")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 🔍 Mapa de calor de correlación (excluyendo columna no numérica)
correlacion = errores_df.drop(columns=['gravedad']).corr().dropna(axis=1, how='all').dropna(axis=0, how='all')
plt.figure(figsize=(8, 6))
sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("🔍 Mapa de calor de correlación entre tipos de errores", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# 📆 Tendencia de errores por mes
df_clientes['fecha_registro'] = pd.to_datetime(df_clientes['fecha_registro'], errors='coerce')
errores_por_mes = errores_df.groupby(df_clientes['fecha_registro'].dt.to_period('M')).sum(numeric_only=True)
errores_por_mes['total_errores'].plot(kind='line', marker='o', figsize=(10, 5), title='📆 Tendencia de errores por mes')
plt.grid(True)
plt.tight_layout()
plt.show()

# 📤 Exportación opcional de registros con errores
df_errores = df_clientes[errores_df['total_errores'] > 0]
# df_errores.to_csv("clientes_con_errores.csv", index=False)  # ← Descomenta si deseas exportar

print("\n✅ Análisis completado.")

