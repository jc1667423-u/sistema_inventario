"""
Constantes del sistema de inventario
"""

# Información del sistema
APP_NOMBRE = "Sistema de Gestión de Inventario"
APP_VERSION = "1.0.0"
APP_EMPRESA = "Tu Empresa"

# Roles de usuario
ROL_SUPER_ADMIN = "super_admin"
ROL_ADMIN = "admin"
ROL_TRABAJADOR = "trabajador"

ROLES = {
    ROL_SUPER_ADMIN: "Super Administrador",
    ROL_ADMIN: "Administrador",
    ROL_TRABAJADOR: "Trabajador"
}

# Tipos de movimiento
MOVIMIENTO_ENTRADA = "Entrada"
MOVIMIENTO_SALIDA = "Salida"

TIPOS_MOVIMIENTO = [MOVIMIENTO_ENTRADA, MOVIMIENTO_SALIDA]

# Tipos de cliente/proveedor
TIPO_CLIENTE = "cliente"
TIPO_PROVEEDOR = "proveedor"
TIPO_AMBOS = "ambos"

TIPOS_ENTIDAD = {
    TIPO_CLIENTE: "Cliente",
    TIPO_PROVEEDOR: "Proveedor",
    TIPO_AMBOS: "Cliente y Proveedor"
}

# Unidades de medida comunes
UNIDADES_MEDIDA = [
    "UND",  # Unidad
    "KG",   # Kilogramo
    "GR",   # Gramo
    "LT",   # Litro
    "ML",   # Mililitro
    "MT",   # Metro
    "CM",   # Centímetro
    "CJ",   # Caja
    "PAQ",  # Paquete
    "DOC",  # Docena
    "GLN",  # Galón
    "BLS",  # Bolsa
    "ROL",  # Rollo
]

# Cargar tema dinámicamente
try:
    import temas
    TEMA = temas.obtener_tema_actual()
    COLOR_PRIMARIO = TEMA['COLOR_PRIMARIO']
    COLOR_SECUNDARIO = TEMA['COLOR_SECUNDARIO']
    COLOR_EXITO = TEMA['COLOR_EXITO']
    COLOR_PELIGRO = TEMA['COLOR_PELIGRO']
    COLOR_ADVERTENCIA = TEMA['COLOR_ADVERTENCIA']
    COLOR_INFO = TEMA['COLOR_INFO']
    COLOR_FONDO = TEMA['COLOR_FONDO']
    COLOR_TEXTO = TEMA['COLOR_TEXTO']
    COLOR_BLANCO = TEMA['COLOR_BLANCO']
except:
    # Colores por defecto (tema claro) si falla la carga
    COLOR_PRIMARIO = "#2C3E50"
    COLOR_SECUNDARIO = "#3498DB"
    COLOR_EXITO = "#27AE60"
    COLOR_PELIGRO = "#E74C3C"
    COLOR_ADVERTENCIA = "#F39C12"
    COLOR_INFO = "#3498DB"
    COLOR_FONDO = "#ECF0F1"
    COLOR_TEXTO = "#2C3E50"
    COLOR_BLANCO = "#FFFFFF"

# Configuración de tablas (Treeview)
TREEVIEW_CONFIG = {
    'selectmode': 'browse',
    'show': 'headings',
    'height': 15
}

# Permisos por rol
PERMISOS = {
    ROL_SUPER_ADMIN: {
        'usuarios': ['crear', 'editar', 'eliminar', 'ver'],
        'productos': ['crear', 'editar', 'eliminar', 'ver'],
        'clientes': ['crear', 'editar', 'eliminar', 'ver'],
        'proveedores': ['crear', 'editar', 'eliminar', 'ver'],
        'transacciones': ['crear', 'editar', 'eliminar', 'ver'],
        'reportes': ['generar', 'exportar'],
        'configuracion': ['modificar'],
    },
    ROL_ADMIN: {
        'usuarios': ['ver'],
        'productos': ['crear', 'editar', 'eliminar', 'ver'],
        'clientes': ['crear', 'editar', 'eliminar', 'ver'],
        'proveedores': ['crear', 'editar', 'eliminar', 'ver'],
        'transacciones': ['crear', 'editar', 'eliminar', 'ver'],
        'reportes': ['generar', 'exportar'],
        'configuracion': [],
    },
    ROL_TRABAJADOR: {
        'usuarios': [],
        'productos': ['ver'],
        'clientes': ['ver'],
        'proveedores': ['ver'],
        'transacciones': ['crear', 'ver'],
        'reportes': ['generar'],
        'configuracion': [],
    }
}

# Mensajes del sistema
MENSAJES = {
    'login_exitoso': "Inicio de sesión exitoso",
    'login_fallido': "Usuario o contraseña incorrectos",
    'usuario_inactivo': "El usuario está inactivo",
    'cambiar_password': "Debe cambiar su contraseña",
    'guardar_exitoso': "Registro guardado exitosamente",
    'actualizar_exitoso': "Registro actualizado exitosamente",
    'eliminar_exitoso': "Registro eliminado exitosamente",
    'confirmar_eliminar': "¿Está seguro de eliminar este registro?",
    'campos_obligatorios': "Debe completar todos los campos obligatorios",
    'stock_insuficiente': "Stock insuficiente para realizar la operación",
    'error_conexion': "Error de conexión a la base de datos",
}

# Formato de fecha
FORMATO_FECHA = "%d/%m/%Y"
FORMATO_FECHA_HORA = "%d/%m/%Y %H:%M"
FORMATO_FECHA_BD = "%Y-%m-%d"
FORMATO_FECHA_HORA_BD = "%Y-%m-%d %H:%M:%S"

# Límites
MAX_INTENTOS_LOGIN = 3
MIN_LONGITUD_PASSWORD = 6
ITEMS_POR_PAGINA = 50

# Rutas
RUTA_REPORTES = "reportes"
RUTA_BACKUPS = "backups"
RUTA_LOGS = "logs"
RUTA_ASSETS = "assets"