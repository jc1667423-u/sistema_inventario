"""
Funciones de base de datos para clientes y proveedores
Este archivo es opcional si usas la clase ClienteProveedor directamente
"""
from config_db import ejecutar_query

def obtener_todos_clientes():
    """Obtiene todos los clientes activos"""
    query = """
        SELECT * FROM clientes_proveedores 
        WHERE (tipo = 'cliente' OR tipo = 'ambos') AND activo = 1
        ORDER BY nombre
    """
    return ejecutar_query(query)

def obtener_todos_proveedores():
    """Obtiene todos los proveedores activos"""
    query = """
        SELECT * FROM clientes_proveedores 
        WHERE (tipo = 'proveedor' OR tipo = 'ambos') AND activo = 1
        ORDER BY nombre
    """
    return ejecutar_query(query)

def obtener_por_id(id_entidad):
    """Obtiene una entidad por su ID"""
    query = "SELECT * FROM clientes_proveedores WHERE id = %s"
    return ejecutar_query(query, (id_entidad,))

def buscar_entidades(termino, tipo=None):
    """Busca clientes/proveedores por código o nombre"""
    if tipo:
        query = """
            SELECT * FROM clientes_proveedores 
            WHERE (codigo LIKE %s OR nombre LIKE %s) AND tipo = %s AND activo = 1
            ORDER BY nombre
        """
        termino_busqueda = f"%{termino}%"
        return ejecutar_query(query, (termino_busqueda, termino_busqueda, tipo))
    else:
        query = """
            SELECT * FROM clientes_proveedores 
            WHERE (codigo LIKE %s OR nombre LIKE %s) AND activo = 1
            ORDER BY nombre
        """
        termino_busqueda = f"%{termino}%"
        return ejecutar_query(query, (termino_busqueda, termino_busqueda))

def insertar_entidad(codigo, nombre, tipo):
    """Inserta una nueva entidad"""
    query = """
        INSERT INTO clientes_proveedores (codigo, nombre, tipo, activo)
        VALUES (%s, %s, %s, 1)
    """
    return ejecutar_query(query, (codigo, nombre, tipo), fetch=False)

def actualizar_entidad(id_entidad, codigo, nombre, tipo):
    """Actualiza una entidad"""
    query = """
        UPDATE clientes_proveedores 
        SET codigo = %s, nombre = %s, tipo = %s
        WHERE id = %s
    """
    return ejecutar_query(query, (codigo, nombre, tipo, id_entidad), fetch=False)

def eliminar_entidad(id_entidad):
    """Elimina (desactiva) una entidad"""
    query = "UPDATE clientes_proveedores SET activo = 0 WHERE id = %s"
    return ejecutar_query(query, (id_entidad,), fetch=False)