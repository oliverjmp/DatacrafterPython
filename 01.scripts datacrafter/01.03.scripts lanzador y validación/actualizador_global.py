import subprocess
import time

# Lista de scripts en orden lógico
scripts = [
    "01.scripts datacrafter/01.01.scripts data completa/clientes.py",
    "01.scripts datacrafter/01.01.scripts data completa/proveedores.py",
    "01.scripts datacrafter/01.01.scripts data completa/productos.py",
    "01.scripts datacrafter/01.01.scripts data completa/sucursales.py",
    "01.scripts datacrafter/01.01.scripts data completa/empleados.py",
    "01.scripts datacrafter/01.01.scripts data completa/inventario.py",
    "01.scripts datacrafter/01.01.scripts data completa/ventas_DetalleVentas.py",
    "01.scripts datacrafter/01.01.scripts data completa/entregas.py",
    "01.scripts datacrafter/01.01.scripts data completa/devoluciones.py",
    "01.scripts datacrafter/01.01.scripts data completa/reseñas.py",
    "01.scripts datacrafter/01.01.scripts data completa/fidelizacion.py",
    "01.scripts datacrafter/01.01.scripts data completa/comprasproveedor.py",
    "01.scripts datacrafter/01.01.scripts data completa/pagosproveedores.py",
    "01.scripts datacrafter/01.01.scripts data completa/cobros_Ventas.py",
    "01.scripts datacrafter/01.01.scripts data completa/generador_AlertasInv.py",
    "01.scripts datacrafter/01.03.scripts lanzador y validación/validador_Integral.py"
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
