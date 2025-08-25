import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Cargar sucursales
df_clientes_erroneos = pd.read_csv("02.descargable/CSV/02.CSV con errores/clientesError.csv", encoding='utf-8-sig')

print(df_clientes_erroneos.head())

# Validacion de Datos
def validar_id(val): return bool(re.match(r"^CL-\d{5}$", str(val)))
def validar_email(val): return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", str(val)))
def validar_telefono(val): return bool(re.match(r"^\d{10,15}$", re.sub(r"\D", "", str(val))))
def validar_fecha(val):
    try: datetime.strptime(str(val), "%Y-%m-%d"); return True
    except: return False

valores_genero_validos = ["Femenino", "Masculino"]

# Series de errores
sintacticos = df_clientes_erroneos.apply(lambda row: not validar_id(row['client_id']) or
                                    not validar_email(row['email']) or
                                    not validar_telefono(row['telefono']) or
                                    not validar_fecha(row['fecha_registro']), axis=1)
semanticos = ~df_clientes_erroneos['genero'].isin(valores_genero_validos)
faltantes = df_clientes_erroneos.isnull().any(axis=1)
duplicados = df_clientes_erroneos.duplicated()

# DataFrame de errores
errores_df = pd.DataFrame({
    'sintactico': sintacticos,
    'semantico': semanticos,
    'faltante': faltantes,
    'duplicado': duplicados
})
errores_df['total_errores'] = errores_df.sum(axis=1)

# Distribución de errores por registro
distribucion = errores_df['total_errores'].value_counts().sort_index()
print("\nDistribución de errores por registro:")
for errores, cantidad in distribucion.items():
    print(f"{errores} error(es): {cantidad} registro(s)")

# Gráfico de distribución
# Colores personalizados
colores = ['skyblue'] * len(distribucion)
colores[0] = 'green'  # La primera barra (índice 0) será verde

plt.figure(figsize=(10,6))
bars = plt.bar(distribucion.index, distribucion.values, color=colores, edgecolor='black')

# Etiquetas centradas en cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval / 2,
             str(int(yval)), ha='center', va='center', fontsize=10, fontweight='bold', color='black')

# Anotación del valor máximo (ajustada para no solaparse)
max_idx = distribucion.index.get_loc(distribucion.idxmax())  # índice posicional del valor máximo
max_val = distribucion.max()
plt.annotate(f'{max_val} máximo',
             xy=(max_idx, max_val),
             xytext=(max_idx, max_val + 300),
             arrowprops=dict(facecolor='red', shrink=0.05),
             fontsize=12, color='red', ha='center')

# Estética
plt.title("📊 Distribución de errores por registro", fontsize=14, fontweight='bold')
plt.xlabel("Cantidad de errores en un registro", fontsize=12)
plt.ylabel("Número de registros", fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Tabla resumen por tipo de error
resumen_errores = errores_df[['sintactico', 'semantico', 'faltante', 'duplicado']].sum().reset_index()
resumen_errores.columns = ['Tipo de error', 'Cantidad de registros']
print("\nResumen por tipo de error:")
print(resumen_errores)

# Gráfico por tipo de error
# Colores: resalta el tipo de error más frecuente
colores = ['salmon'] * len(resumen_errores)
max_idx = resumen_errores['Cantidad de registros'].idxmax()
colores[max_idx] = 'crimson'

plt.figure(figsize=(10,6))
bars = plt.bar(resumen_errores['Tipo de error'], resumen_errores['Cantidad de registros'], 
               color=colores, edgecolor='black')

# Etiquetas centradas en cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval / 2, 
             str(int(yval)), ha='center', va='center', fontsize=10, fontweight='bold', color='black')

# Anotación del valor máximo
max_val = resumen_errores['Cantidad de registros'].max()
plt.annotate(f'{max_val} máximo',
             xy=(max_idx, max_val),
             xytext=(max_idx, max_val + 300),
             arrowprops=dict(facecolor='red', shrink=0.05),
             fontsize=12, color='red', ha='center')

# Estética
plt.title("📌 Cantidad de registros por tipo de error", fontsize=14, fontweight='bold')
plt.xlabel("Tipo de error", fontsize=12)
plt.ylabel("Cantidad", fontsize=12)
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Desglose por tipo y cantidad de errores
desglose = []
for n in sorted(errores_df['total_errores'].unique()):
    subset = errores_df[errores_df['total_errores'] == n]
    sintactico = subset['sintactico'].sum()
    semantico = subset['semantico'].sum()
    faltante = subset['faltante'].sum()
    duplicado = subset['duplicado'].sum()
    desglose.append({
        'Cantidad de errores': n,
        'Sintáctico': sintactico,
        'Semántico': semantico,
        'Faltante': faltante,
        'Duplicado': duplicado
    })

tabla_desglose = pd.DataFrame(desglose)
print("\nDesglose de errores por tipo y cantidad de errores:")
print(tabla_desglose)

# Contar errores sintácticos por tipo
errores_sintacticos = {
    'ID inválido': (~df_clientes_erroneos['client_id'].apply(validar_id)).sum(),
    'Email inválido': (~df_clientes_erroneos['email'].apply(validar_email)).sum(),
    'Teléfono inválido': (~df_clientes_erroneos['telefono'].apply(validar_telefono)).sum(),
    'Fecha inválida': (~df_clientes_erroneos['fecha_registro'].apply(validar_fecha)).sum()
}

# Calcular total de errores sintácticos
total_errores_sintacticos = sum(errores_sintacticos.values())

# Mostrar resultados
print("\nCantidad de errores sintácticos por tipo:")
for tipo, cantidad in errores_sintacticos.items():
    print(f"{tipo}: {cantidad}")
print(f"\nTotal de errores sintácticos: {total_errores_sintacticos}")

print("\n📊 Mapa de calor de correlación entre tipos de errores:")

# Calcular la matriz de correlación y eliminar columnas/filas con NaN
correlacion = errores_df.corr().dropna(axis=1, how='all').dropna(axis=0, how='all')

# Mostrar la matriz en consola
print(correlacion)

# Graficar el mapa de calor
plt.figure(figsize=(8,6))
sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("🔍 Mapa de calor de correlación entre tipos de errores", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()


# Grafico como HTML
fig = px.bar(resumen_errores, x='Tipo de error', y='Cantidad de registros',
             color='Cantidad de registros', text='Cantidad de registros',
             title='Cantidad de registros por tipo de error')
fig.update_traces(textposition='inside')

# Guardar como HTML
fig.write_html("grafico_errores.html")