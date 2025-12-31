"""
Sistema de Logging Centralizado
Configuración de logging para todo el sistema
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Crear directorio de logs si no existe
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuración de formato
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def obtener_logger(nombre_modulo):
    """
    Obtiene un logger configurado para un módulo específico
    
    Args:
        nombre_modulo: Nombre del módulo que solicita el logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(nombre_modulo)
    
    # Si ya tiene handlers, no agregar más
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Handler para archivo general (INFO y superior)
    archivo_general = os.path.join(LOG_DIR, 'sistema.log')
    handler_general = RotatingFileHandler(
        archivo_general,
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=10,
        encoding='utf-8'
    )
    handler_general.setLevel(logging.INFO)
    handler_general.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    
    # Handler para archivo de errores (ERROR y superior)
    archivo_errores = os.path.join(LOG_DIR, 'errores.log')
    handler_errores = RotatingFileHandler(
        archivo_errores,
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=10,
        encoding='utf-8'
    )
    handler_errores.setLevel(logging.ERROR)
    handler_errores.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    
    # Handler para consola (WARNING y superior)
    handler_consola = logging.StreamHandler()
    handler_consola.setLevel(logging.WARNING)
    handler_consola.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    
    # Agregar handlers al logger
    logger.addHandler(handler_general)
    logger.addHandler(handler_errores)
    logger.addHandler(handler_consola)
    
    return logger

def log_autenticacion(username, exitoso, mensaje=""):
    """
    Registra intentos de autenticación
    
    Args:
        username: Usuario que intenta autenticarse
        exitoso: True si fue exitoso, False si falló
        mensaje: Mensaje adicional
    """
    logger = obtener_logger('autenticacion')
    
    if exitoso:
        logger.info(f"Login exitoso - Usuario: {username} - {mensaje}")
    else:
        logger.warning(f"Login fallido - Usuario: {username} - {mensaje}")

def log_transaccion(tipo, producto, cantidad, usuario, mensaje=""):
    """
    Registra transacciones de inventario
    
    Args:
        tipo: 'Entrada' o 'Salida'
        producto: Código o descripción del producto
        cantidad: Cantidad del movimiento
        usuario: Usuario que realiza la transacción
        mensaje: Mensaje adicional
    """
    logger = obtener_logger('transacciones')
    logger.info(f"{tipo} - Producto: {producto} - Cantidad: {cantidad} - Usuario: {usuario} - {mensaje}")

def log_error_bd(operacion, error, query=""):
    """
    Registra errores de base de datos
    
    Args:
        operacion: Descripción de la operación
        error: Objeto de excepción
        query: Query SQL que causó el error (opcional)
    """
    logger = obtener_logger('base_datos')
    mensaje = f"Error en {operacion}: {str(error)}"
    if query:
        mensaje += f" - Query: {query[:100]}..."  # Primeros 100 caracteres
    logger.error(mensaje)

def log_accion_critica(modulo, accion, usuario, detalles=""):
    """
    Registra acciones críticas del sistema
    
    Args:
        modulo: Módulo donde ocurre la acción
        accion: Descripción de la acción
        usuario: Usuario que realiza la acción
        detalles: Detalles adicionales
    """
    logger = obtener_logger('auditoria')
    logger.warning(f"[CRÍTICO] {modulo} - {accion} - Usuario: {usuario} - {detalles}")

# Logger general del sistema
sistema_logger = obtener_logger('sistema')
