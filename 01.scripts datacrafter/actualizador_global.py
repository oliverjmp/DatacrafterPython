import subprocess
import time

# Lista de scripts en orden lógico
scripts = [
    "01.scripts datacrafter/clientes.py",
    "01.scripts datacrafter/proveedores.py",
    "01.scripts datacrafter/productos.py",
    "01.scripts datacrafter/sucursales.py",
    "01.scripts datacrafter/empleados.py",
    "01.scripts datacrafter/inventario.py",
    "01.scripts datacrafter/ventas_DetalleVentas.py",
    "01.scripts datacrafter/entregas.py",
    "01.scripts datacrafter/devoluciones.py",
    "01.scripts datacrafter/reseñas.py",
    "01.scripts datacrafter/fidelizacion.py",
    "01.scripts datacrafter/comprasproveedor.py",
    "01.scripts datacrafter/pagosproveedores.py",
    "01.scripts datacrafter/cobros_Ventas.py",
    "01.scripts datacrafter/generador_AlertasInv.py",
    "01.scripts datacrafter/validador_Integral.py"
]

print("\n🛠️ INICIO DE ACTUALIZACIÓN GLOBAL\n")

for script in scripts:
    print(f"🚀 Ejecutando: {script}")
    inicio = time.time()
    try:
        subprocess.run(["python", script], check=True)
        duracion = round(time.time() - inicio, 2)
        print(f"✅ Completado en {duracion} segundos\n")
    except subprocess.CalledProcessError:
        print(f"❌ Error al ejecutar: {script}\n")

print("🎯 Actualización global finalizada.")
