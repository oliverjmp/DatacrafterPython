# 🛒 Simulación de Base de Datos para una Cadena de Tiendas

## 📌 Descripción del Proyecto

Este proyecto simula una base de datos relacional para una cadena de tiendas minoristas de gran escala. Su propósito es servir como entorno de práctica para:

- 📐 Modelado de datos en SQL
- 🐍 Generación de datos simulados con Python
- 📊 Visualización con Power BI
- 🧮 Manipulación de datos con Pandas y SQLAlchemy

La base de datos incluye información sobre productos, clientes, ventas, inventario, proveedores, sucursales, empleados y más. También se han incorporado módulos adicionales como cobros, devoluciones, reseñas y fidelización para enriquecer el ecosistema de datos.

## 🧰 Tecnologías Utilizadas

- **MySQL** – Gestión de base de datos relacional
- **Python** – Generación de datos simulados con [Faker](https://faker.readthedocs.io/)
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
- `cobros`
- `devoluciones`
- `reseñas`
- `fidelizacion`
- `alertas_stock`

Todas las tablas están relacionadas mediante claves primarias y foráneas para mantener la integridad referencial. Puedes consultar el archivo [`diccionario_relacional.md`](https://github.com/oliverjmp/DatacrafterPython/blob/main/diccionario_relacional.md) para ver el esquema completo.

## 🧪 Generación de Datos Simulados

Se utiliza la librería **Faker** para generar datos realistas como nombres, direcciones, fechas y más. Además, se emplean funciones aleatorias para simular cantidades, precios y relaciones entre entidades.

Los datos se exportan en múltiples formatos: `CSV`, `JSON`, `Excel`, `Parquet`, `Feather` y `SQL`, organizados en la carpeta `02.descargable`. También se generan versiones con errores intencionales para prácticas de limpieza y validación de datos.

## 🔐 Protección de Datos

⚠️ Este software genera datos completamente ficticios con fines educativos.  
No contiene ni utiliza información personal real.  
Cualquier coincidencia con personas, empresas o ubicaciones reales es puramente accidental.

## 🧑‍💻 Contribuciones

Este repositorio está abierto a contribuciones. Para colaborar:

1. Haz un **fork** del repositorio  
2. Crea una **nueva rama** para tus cambios  
3. Realiza un **pull request** explicando tus modificaciones  
4. Espera la revisión y aprobación

💡 Se recomienda seguir buenas prácticas de desarrollo y documentación para mantener la integridad del proyecto.

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.  
Consulta el archivo [`LICENSE`](https://github.com/oliverjmp/DatacrafterPython/blob/main/LICENSE) para más detalles.

## ✨ Créditos

Creado por [@oliverjmp](https://github.com/oliverjmp)  
Diseñado para fines educativos, exploratorios y de entrenamiento en ciencia de ççdatos.

# 🛒 Simulated Retail Database for a Multi-Store Chain

## 📌 Project Overview

This project simulates a relational database for a large-scale retail chain. It serves as a practice environment for:

- 📐 Data modeling in SQL  
- 🐍 Synthetic data generation with Python  
- 📊 Data visualization using Power BI  
- 🧮 Data manipulation with Pandas and SQLAlchemy  

The database includes information on products, customers, sales, inventory, suppliers, branches, employees, and more. Additional modules such as payments, returns, reviews, and loyalty programs have been added to enrich the data ecosystem.

## 🧰 Technologies Used

- **MySQL** – Relational database management  
- **Python** – Data simulation using [Faker](https://faker.readthedocs.io/)  
- **Power BI** – Data visualization  
- **Pandas / SQLAlchemy** – Data manipulation and loading  

## 🗃️ Database Structure

The database contains the following core tables:

- `clientes` (customers)  
- `productos` (products)  
- `categorias` (categories)  
- `ventas` (sales)  
- `detalles_venta` (sales details)  
- `empleados` (employees)  
- `sucursales` (branches)  
- `inventario` (inventory)  
- `proveedores` (suppliers)  
- `compras` (purchases)  
- `cobros` (payments)  
- `devoluciones` (returns)  
- `reseñas` (reviews)  
- `fidelizacion` (loyalty)  
- `alertas_stock` (stock alerts)  

All tables are linked through primary and foreign keys to preserve referential integrity. You can explore the full schema in [`diccionario_relacional.md`](https://github.com/oliverjmp/DatacrafterPython/blob/main/diccionario_relacional.md).

## 🧪 Synthetic Data Generation

The **Faker** library is used to generate realistic data such as names, addresses, dates, and more. Randomized logic is applied to simulate quantities, prices, and relationships between entities.

All data is exported in multiple formats: `CSV`, `JSON`, `Excel`, `Parquet`, `Feather`, and `SQL`, organized under the `02.descargable` directory. Error-injected versions are also generated for data cleaning and validation exercises.

## 🔐 Data Protection

⚠️ This software generates entirely fictitious data for educational purposes.  
It does not contain or use any real personal information.  
Any resemblance to actual people, companies, or locations is purely coincidental.

## 🧑‍💻 Contributions

This repository is open to contributions. To collaborate:

1. Fork the repository  
2. Create a new branch for your changes  
3. Submit a pull request explaining your modifications  
4. Wait for review and approval  

💡 Please follow best practices in development and documentation to maintain project integrity.

## 📄 License

This project is licensed under the **MIT License**.  
See the [`LICENSE`](https://github.com/oliverjmp/DatacrafterPython/blob/main/LICENSE) file for details.

## ✨ Credits

Created by [@oliverjmp](https://github.com/oliverjmp)  
Designed for educational, exploratory, and data science training purposes.

