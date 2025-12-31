"""
Configuración de la base de datos
"""
import pymysql
from pymysql.cursors import DictCursor
import os
from pathlib import Path

# Intentar cargar python-decouple
try:
    from decouple import config
    USAR_ENV = True
except ImportError:
    USAR_ENV = False
    print("⚠️ python-decouple no instalado. Usando configuración por defecto.")
    print("   Instale con: pip install python-decouple")

# Importar logger
try:
    from logger import obtener_logger, log_error_bd
    logger = obtener_logger('base_datos')
except ImportError:
    logger = None

# Configuración de conexión
if USAR_ENV:
    DB_CONFIG = {
        'host': config('DB_HOST', default='localhost'),
        'port': config('DB_PORT', default=3306, cast=int),
        'user': config('DB_USER', default='root'),
        'password': config('DB_PASSWORD', default=''),
        'database': config('DB_NAME', default='sistema_inventario'),
        'charset': config('DB_CHARSET', default='utf8mb4'),
        'cursorclass': DictCursor
    }
else:
    # Configuración por defecto (fallback)
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Jesus25@db',  
        'database': 'sistema_inventario',
        'charset': 'utf8mb4',
        'cursorclass': DictCursor
    }

def obtener_conexion():
    """
    Obtiene una conexión a la base de datos
    Returns:
        connection: Objeto de conexión a MySQL
    """
    try:
        conexion = pymysql.connect(**DB_CONFIG)
        return conexion
    except pymysql.Error as e:
        error_msg = f"Error al conectar a la base de datos: {e}"
        print(error_msg)
        if logger:
            log_error_bd("obtener_conexion", e)
        raise

def verificar_conexion():
    """
    Verifica que la conexión a la base de datos sea exitosa
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        conn = obtener_conexion()
        conn.close()
        if logger:
            logger.info("Conexión a base de datos verificada exitosamente")
        return True
    except Exception as e:
        error_msg = f"Error de conexión: {e}"
        print(error_msg)
        if logger:
            log_error_bd("verificar_conexion", e)
        return False

def ejecutar_query(query, params=None, fetch=True):
    """
    Ejecuta una query en la base de datos
    Args:
        query: Query SQL a ejecutar
        params: Parámetros para la query (tupla o diccionario)
        fetch: Si True, retorna los resultados (SELECT), si False solo ejecuta (INSERT/UPDATE/DELETE)
    Returns:
        list/dict/int: Resultados de la query o número de filas afectadas
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if fetch:
                resultados = cursor.fetchall()
                return resultados
            else:
                conexion.commit()
                return cursor.rowcount
                
    except Exception as e:
        if conexion:
            conexion.rollback()
        error_msg = f"Error al ejecutar query: {e}"
        print(error_msg)
        if logger:
            log_error_bd("ejecutar_query", e, query)
        raise
    finally:
        if conexion:
            conexion.close()

def ejecutar_muchas(query, data_list):
    """
    Ejecuta múltiples inserts/updates en una sola transacción
    Args:
        query: Query SQL preparada con placeholders
        data_list: Lista de tuplas con los datos
    Returns:
        int: Número de filas afectadas
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.executemany(query, data_list)
            conexion.commit()
            return cursor.rowcount
    except Exception as e:
        if conexion:
            conexion.rollback()
        error_msg = f"Error al ejecutar múltiples queries: {e}"
        print(error_msg)
        if logger:
            log_error_bd("ejecutar_muchas", e, query)
        raise
    finally:
        if conexion:
            conexion.close()