"""
Funciones de base de datos para productos
Este archivo es opcional si usas la clase Productos directamente
"""
from config_db import ejecutar_query

def obtener_todos_productos():
    """Obtiene todos los productos activos"""
    query = "SELECT * FROM productos WHERE activo = 1 ORDER BY descripcion"
    return ejecutar_query(query)

def obtener_producto_por_id(id_producto):
    """Obtiene un producto por su ID"""
    query = "SELECT * FROM productos WHERE id = %s"
    return ejecutar_query(query, (id_producto,))

def buscar_productos(termino):
    """Busca productos por código o descripción"""
    query = """
        SELECT * FROM productos 
        WHERE (codigo LIKE %s OR descripcion LIKE %s) AND activo = 1
        ORDER BY descripcion
    """
    termino_busqueda = f"%{termino}%"
    return ejecutar_query(query, (termino_busqueda, termino_busqueda))

def insertar_producto(codigo, descripcion, unidad_medida, precio, stock_actual=0):
    """Inserta un nuevo producto"""
    query = """
        INSERT INTO productos 
        (codigo, descripcion, unidad_medida, precio, stock_actual, activo)
        VALUES (%s, %s, %s, %s, %s, 1)
    """
    return ejecutar_query(query, (codigo, descripcion, unidad_medida, precio, stock_actual), fetch=False)

def actualizar_producto(id_producto, codigo, descripcion, unidad_medida, precio):
    """Actualiza un producto"""
    query = """
        UPDATE productos 
        SET codigo = %s, descripcion = %s, unidad_medida = %s, precio = %s
        WHERE id = %s
    """
    return ejecutar_query(query, (codigo, descripcion, unidad_medida, precio, id_producto), fetch=False)

def eliminar_producto(id_producto):
    """Elimina (desactiva) un producto"""
    query = "UPDATE productos SET activo = 0 WHERE id = %s"
    return ejecutar_query(query, (id_producto,), fetch=False)

def actualizar_stock(id_producto, cantidad):
    """Actualiza el stock de un producto"""
    query = "UPDATE productos SET stock_actual = %s WHERE id = %s"
    return ejecutar_query(query, (cantidad, id_producto), fetch=False)