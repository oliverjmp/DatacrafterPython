# 🛒 Simulación de Base de Datos para una Cadena de Tiendas

## 📌 Descripción del Proyecto

Este proyecto simula una base de datos relacional para una cadena de tiendas minoristas de gran escala. Su propósito es servir como entorno de práctica para:

- 📐 Modelado de datos en SQL
- 🐍 Generación de datos simulados con Python
- 📊 Visualización con Power BI
- 🧮 Manipulación de datos con Pandas y SQLAlchemy

La base de datos incluye información sobre productos, clientes, ventas, inventario, proveedores, sucursales, empleados y más.

---

## 🧰 Tecnologías Utilizadas

- **MySQL** – Gestión de base de datos relacional  
- **Python** – Generación de datos simulados con [Faker](https://faker.readthedocs.io/)  
- **Power BI** – Visualización de datos  
- **Pandas / SQLAlchemy** – Manipulación y carga de datos

---

## 🗃️ Estructura de la Base de Datos

La base de datos contiene las siguientes tablas principales:

- `clientes`
- `productos`
- `categorias`
- `ventas`
- `detalles_venta`
- `empleados`
- `sucursales`
- `inventario`
- `proveedores`
- `compras`

Todas las tablas están relacionadas mediante claves primarias y foráneas para mantener la integridad referencial. Puedes consultar el archivo [`diccionario_relacional.md`](./diccionario_relacional.md) para ver el esquema completo.

---

## 🧪 Generación de Datos Simulados

Se utiliza la librería **Faker** para generar datos realistas como nombres, direcciones, fechas y más. Además, se emplean funciones aleatorias para simular cantidades, precios y relaciones entre entidades.

Los datos se exportan en múltiples formatos: CSV, JSON, Excel, Parquet, Feather y SQL, organizados en la carpeta `02.descargable`.

---

## 🔐 Protección de Datos

⚠️ Este software genera datos completamente ficticios con fines educativos.  
No contiene ni utiliza información personal real.  
Cualquier coincidencia con personas, empresas o ubicaciones reales es puramente accidental.

---

## 🧑‍💻 Contribuciones

Este repositorio está abierto a contribuciones. Para colaborar:

1. Haz un **fork** del repositorio  
2. Crea una **nueva rama** para tus cambios  
3. Realiza un **pull request** explicando tus modificaciones  
4. Espera la revisión y aprobación

> 💡 Se recomienda seguir buenas prácticas de desarrollo y documentación para mantener la integridad del proyecto.

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.  
Consulta el archivo [`LICENSE`](./LICENSE) para más detalles.

---

## ✨ Créditos

Creado por [@oliverjmp](https://github.com/oliverjmp)  
Diseñado para fines educativos, exploratorios y de entrenamiento en ciencia de datos.



