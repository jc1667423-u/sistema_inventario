# 📦 Sistema de Gestión de Inventario

Sistema completo de gestión de inventario desarrollado en Python con interfaz gráfica Tkinter y base de datos MySQL. Implementa control de stock mediante método Kardex con trazabilidad completa de movimientos.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

##  Características Principales

-  **Gestión de Productos** - CRUD completo con control de stock
-  **Gestión de Clientes y Proveedores** - Entidades unificadas
-  **Movimientos de Inventario** - Entradas y salidas con Kardex
-  **Sistema de Usuarios** - Autenticación con roles y permisos
-  **Reportes** - Exportación a Excel y PDF
-  **Dashboard** - Estadísticas en tiempo real
-  **Auditoría** - Sistema de logging completo
-  **Seguridad** - Contraseñas encriptadas con bcrypt

---

## 📋 Requisitos del Sistema

### Software Necesario

- **Python 3.7 o superior**
- **MySQL 5.7 o superior** / MariaDB 10.x
- **Sistema Operativo**: Windows, Linux o macOS

### Dependencias Python

Todas las dependencias están listadas en `requerimientos.txt`:

```
pymysql==1.1.0
python-decouple==3.8
openpyxl==3.1.2
xlsxwriter==3.1.9
reportlab==4.0.7
matplotlib==3.8.2
pillow==10.1.0
python-dateutil==2.8.2
bcrypt==4.1.2
```

---

##  Instalación

### 1. Clonar o Descargar el Proyecto

```bash
git clone <url-del-repositorio>
cd sistema-inventario
```

O descargar y extraer el archivo ZIP.

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requerimientos.txt
```

### 4. Configurar Base de Datos

#### 4.1. Crear la Base de Datos

Ejecutar en MySQL:

```sql
CREATE DATABASE sistema_inventario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 4.2. Crear las Tablas

Ejecutar el script SQL de creación de tablas (si está disponible) o crear manualmente:

```sql
USE sistema_inventario;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol ENUM('super_admin', 'admin', 'trabajador') NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    debe_cambiar_password TINYINT(1) DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME NULL
);

-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    unidad_medida VARCHAR(10) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock_actual DECIMAL(10,2) DEFAULT 0,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de clientes y proveedores
CREATE TABLE clientes_proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo ENUM('cliente', 'proveedor', 'ambos') NOT NULL,
    documento VARCHAR(20),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(200),
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de transacciones (Kardex)
CREATE TABLE transacciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    cantidad_entrada DECIMAL(10,2) DEFAULT 0,
    cantidad_salida DECIMAL(10,2) DEFAULT 0,
    costo DECIMAL(10,2) DEFAULT 0,
    valor_entrada DECIMAL(10,2) DEFAULT 0,
    valor_salida DECIMAL(10,2) DEFAULT 0,
    fecha DATETIME NOT NULL,
    cliente_proveedor_id INT,
    documento VARCHAR(50),
    tipo_movimiento ENUM('Entrada', 'Salida') NOT NULL,
    concepto VARCHAR(200),
    usuario_id INT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (cliente_proveedor_id) REFERENCES clientes_proveedores(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

#### 4.3. Crear Usuario Administrador

```sql
-- Contraseña: admin123 (cambiar después del primer login)
INSERT INTO usuarios (username, password_hash, nombre_completo, rol, debe_cambiar_password)
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxF6q0OXu', 'Administrador', 'super_admin', 1);
```

### 5. Configurar Variables de Entorno

#### 5.1. Copiar el Archivo de Ejemplo

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

#### 5.2. Editar el Archivo `.env`

Abrir `.env` y configurar con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=sistema_inventario
DB_CHARSET=utf8mb4

APP_EMPRESA=Tu Empresa
DEBUG=False
```

> ⚠️ **IMPORTANTE**: Nunca subir el archivo `.env` a repositorios públicos. Ya está incluido en `.gitignore`.

### 6. Ejecutar la Aplicación

```bash
python main.py
```

---

## 🔐 Credenciales por Defecto

### Usuario Administrador

- **Usuario**: `admin`
- **Contraseña**: `admin123`

> ⚠️ **IMPORTANTE**: El sistema te pedirá cambiar la contraseña en el primer inicio de sesión.

---

## 📖 Guía de Uso

### Inicio de Sesión

1. Ejecutar `python main.py`
2. Ingresar usuario y contraseña
3. Si es el primer acceso, cambiar la contraseña

### Dashboard Principal

Al iniciar sesión verás:
- **Total de productos** en inventario
- **Valor total** del inventario
- **Productos con stock bajo**
- **Accesos rápidos** a funcionalidades

### Gestión de Productos

**Menú: Inventario → Productos**

- **Crear producto**: Código, descripción, unidad de medida, precio
- **Editar producto**: Modificar datos (el stock se actualiza con movimientos)
- **Buscar**: Por código o descripción
- **Activar/Desactivar**: En lugar de eliminar

### Movimientos de Inventario

#### Registrar Entrada (Compra)

**Menú: Movimientos → Nueva Entrada**

1. Seleccionar producto
2. Ingresar cantidad y costo
3. Seleccionar proveedor
4. Número de documento
5. Concepto/Observación
6. Guardar

El stock se actualiza automáticamente.

#### Registrar Salida (Venta)

**Menú: Movimientos → Nueva Salida**

1. Seleccionar producto
2. Ingresar cantidad y precio
3. Seleccionar cliente
4. Número de documento
5. Concepto/Observación
6. Guardar

El sistema valida que haya stock suficiente.

### Kardex

**Menú: Consultas → Kardex por Producto**

Muestra el historial completo de movimientos de un producto:
- Entradas y salidas
- Saldo acumulado
- Valores
- Fechas y documentos
- Usuario que registró

### Reportes

**Menú: Reportes**

- **Inventario**: Listado de productos con stock y valores
- **Movimientos**: Transacciones en rango de fechas
- **Valorización**: Valor total del inventario

Exportar a Excel o PDF.

### Gestión de Usuarios

**Menú: Configuración → Usuarios** (Solo Super Admin)

- Crear usuarios con diferentes roles
- Asignar permisos
- Activar/Desactivar usuarios

#### Roles Disponibles

| Rol | Permisos |
|-----|----------|
| **Super Admin** | Acceso total, incluye gestión de usuarios |
| **Admin** | Gestión completa excepto usuarios |
| **Trabajador** | Solo consultas y registro de movimientos |

---

## 📁 Estructura del Proyecto

```
sistema-inventario/
├── base_datos/          # Módulos de acceso a datos
│   ├── config_db.py     # Configuración de BD y funciones
│   ├── clientes.py      # Funciones auxiliares de clientes
│   └── productos.py     # Funciones auxiliares de productos
├── clases/              # Modelos de negocio
│   ├── productos.py     # Clase Producto
│   ├── usuarios.py      # Clase Usuario
│   ├── clientes.py      # Clase ClienteProveedor
│   └── transacciones.py # Clase Transaccion
├── ventanas/            # Interfaces gráficas
│   ├── login.py         # Ventana de login
│   ├── ventana_principal.py  # Dashboard
│   ├── productos.py     # Gestión de productos
│   ├── clientes.py      # Gestión de clientes
│   ├── usuarios.py      # Gestión de usuarios
│   ├── entrada.py       # Registro de entradas
│   ├── salida.py        # Registro de salidas
│   ├── movimientos.py   # Historial de movimientos
│   └── kardex_producto.py    # Kardex por producto
├── logs/                # Archivos de log (se crea automáticamente)
├── main.py              # Punto de entrada
├── logger.py            # Sistema de logging
├── constantes.py        # Constantes del sistema
├── utilis.py            # Funciones utilitarias
├── .env                 # Configuración (NO versionar)
├── .env.example         # Plantilla de configuración
├── .gitignore           # Archivos ignorados por git
├── requerimientos.txt   # Dependencias
└── README.md            # Este archivo
```

---

## 🔧 Solución de Problemas

### Error: "No se puede conectar a la base de datos"

**Solución:**
1. Verificar que MySQL esté ejecutándose
2. Revisar credenciales en `.env`
3. Verificar que la base de datos `sistema_inventario` exista
4. Comprobar que el usuario tenga permisos

### Error: "ModuleNotFoundError: No module named 'xxx'"

**Solución:**
```bash
pip install -r requerimientos.txt
```

### Error: "python-decouple no instalado"

**Solución:**
```bash
pip install python-decouple
```

El sistema funcionará con configuración por defecto, pero se recomienda instalar python-decouple.

### La ventana no se muestra correctamente

**Solución:**
- Verificar resolución de pantalla (mínimo 1024x768)
- Actualizar drivers de video
- En Linux, instalar: `sudo apt-get install python3-tk`

### Olvidé la contraseña del administrador

**Solución:**

Ejecutar el script `fix_password.py`:

```bash
python fix_password.py
```

O ejecutar en MySQL:

```sql
UPDATE usuarios 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxF6q0OXu',
    debe_cambiar_password = 1
WHERE username = 'admin';
```

Esto restablece la contraseña a `admin123`.

---

## 📊 Sistema de Logging

El sistema registra automáticamente:

-  **Autenticaciones** (exitosas y fallidas)
-  **Movimientos de inventario** (entradas y salidas)
-  **Errores de base de datos**
-  **Acciones críticas** (creación/eliminación de usuarios, etc.)

Los logs se guardan en la carpeta `logs/`:
- `sistema.log` - Log general (INFO y superior)
- `errores.log` - Solo errores (ERROR y superior)

### Rotación de Logs

- Tamaño máximo por archivo: 5 MB
- Archivos de respaldo: 10
- Los logs antiguos se comprimen automáticamente

---

## 🔒 Seguridad

### Contraseñas

- Encriptadas con **bcrypt**
- Nunca se almacenan en texto plano
- Cambio obligatorio en primer acceso

### Base de Datos

- Queries parametrizadas (prevención de SQL injection)
- Credenciales en archivo `.env` (no versionado)
- Conexiones con manejo de errores

### Permisos

- Sistema de roles granular
- Validación de permisos en cada acción
- Auditoría de acciones críticas

---

## 🚀 Próximas Mejoras

- [ ] Exportación de reportes a PDF
- [ ] Gráficos estadísticos en dashboard
- [ ] Sistema de respaldos automáticos
- [ ] Notificaciones de stock bajo
- [ ] Módulo de compras y ventas
- [ ] API REST para integraciones
- [ ] Versión web con FastAPI + React

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👥 Contacto y Soporte

Para reportar errores o sugerencias:

- **Email**: jc1667423@gmail.com
- **Issues**: [GitHub Issues](https://github.com/jc1667423-u/sistema_inventario.git)

---


**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025
