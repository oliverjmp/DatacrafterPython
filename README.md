# 🛒 Simulación de Base de Datos para Tienda Minorista

## 📌 Descripción del Proyecto

Este proyecto simula una base de datos relacional para una tienda minorista de gran escala, con el objetivo de practicar habilidades en **SQL**, **Python** (usando Faker para generar datos simulados) y herramientas de visualización como **Power BI**. La base de datos incluye información sobre productos, clientes, ventas, inventario, proveedores y más.

## 🧰 Tecnologías Utilizadas

- **MySQL** – Gestión de base de datos relacional
- **Python** – Generación de datos simulados con Faker
- **Power BI** – Visualización de datos
- **Pandas / SQLAlchemy** – Manipulación y carga de datos

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

> Las tablas están relacionadas mediante claves primarias y foráneas para mantener la integridad referencial.

## 🧪 Generación de Datos Simulados

Se utilizó la librería **Faker** para generar datos realistas como nombres, direcciones, fechas y más. 
Además, se emplearon funciones aleatorias para simular cantidades, precios y relaciones entre entidades.
