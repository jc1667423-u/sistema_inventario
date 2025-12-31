"""
Clase Producto para gestión de productos del inventario
"""
from base_datos.config_db import ejecutar_query

class Producto:
    """Clase que representa un producto del inventario"""
    
    def __init__(self, id, codigo, descripcion, unidad_medida, precio, stock_actual, stock_minimo=10, activo=1):
        self.id = id
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad_medida = unidad_medida
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.activo = activo
    
    @staticmethod
    def obtener_todos(solo_activos=True):
        """Obtiene todos los productos"""
        if solo_activos:
            query = """
                SELECT id, codigo, descripcion, unidad_medida, 
                       precio, stock_actual, stock_minimo, activo
                FROM productos 
                WHERE activo = 1
                ORDER BY descripcion
            """
        else:
            query = """
                SELECT id, codigo, descripcion, unidad_medida, 
                       precio, stock_actual, stock_minimo, activo
                FROM productos 
                ORDER BY descripcion
            """
        
        return ejecutar_query(query)
    
    @staticmethod
    def obtener_por_id(id_producto):
        """Obtiene un producto por su ID"""
        query = """
            SELECT id, codigo, descripcion, unidad_medida, 
                   precio, stock_actual, stock_minimo, activo
            FROM productos 
            WHERE id = %s
        """
        
        resultado = ejecutar_query(query, (id_producto,))
        
        if resultado and len(resultado) > 0:
            p = resultado[0]
            return Producto(
                id=p['id'],
                codigo=p['codigo'],
                descripcion=p['descripcion'],
                unidad_medida=p['unidad_medida'],
                precio=p['precio'],
                stock_actual=p['stock_actual'],
                stock_minimo=p.get('stock_minimo', 10),
                activo=p['activo']
            )
        
        return None
    
    @staticmethod
    def obtener_por_codigo(codigo):
        """Obtiene un producto por su código"""
        query = """
            SELECT id, codigo, descripcion, unidad_medida, 
                   precio, stock_actual, stock_minimo, activo
            FROM productos 
            WHERE codigo = %s
        """
        
        resultado = ejecutar_query(query, (codigo,))
        return resultado[0] if resultado else None
    
    @staticmethod
    def buscar(termino):
        """Busca productos por código o descripción"""
        query = """
            SELECT id, codigo, descripcion, unidad_medida, 
                   precio, stock_actual, stock_minimo, activo
            FROM productos 
            WHERE (codigo LIKE %s OR descripcion LIKE %s) AND activo = 1
            ORDER BY descripcion
        """
        
        termino_busqueda = f"%{termino}%"
        return ejecutar_query(query, (termino_busqueda, termino_busqueda))
    
    @staticmethod
    def crear(codigo, descripcion, unidad_medida, precio, stock_actual=0, stock_minimo=10):
        """Crea un nuevo producto"""
        query = """
            INSERT INTO productos 
            (codigo, descripcion, unidad_medida, precio, stock_actual, stock_minimo, activo)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
        """
        
        ejecutar_query(
            query, 
            (codigo, descripcion, unidad_medida, precio, stock_actual, stock_minimo), 
            fetch=False
        )
        return True
    
    @staticmethod
    def actualizar(id_producto, codigo, descripcion, unidad_medida, stock_minimo):
        """Actualiza los datos de un producto (sin modificar stock ni precio)"""
        query = """
            UPDATE productos 
            SET codigo = %s, descripcion = %s, unidad_medida = %s, stock_minimo = %s
            WHERE id = %s
        """
        
        ejecutar_query(
            query, 
            (codigo, descripcion, unidad_medida, stock_minimo, id_producto), 
            fetch=False
        )
        return True
    
    @staticmethod
    def actualizar_stock(id_producto, nuevo_stock):
        """Actualiza solo el stock de un producto"""
        query = """
            UPDATE productos 
            SET stock_actual = %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (nuevo_stock, id_producto), fetch=False)
        return True
    
    @staticmethod
    def actualizar_precio(id_producto, nuevo_precio):
        """Actualiza solo el precio de un producto"""
        query = """
            UPDATE productos 
            SET precio = %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (nuevo_precio, id_producto), fetch=False)
        return True
    
    @staticmethod
    def incrementar_stock(id_producto, cantidad):
        """Incrementa el stock de un producto"""
        query = """
            UPDATE productos 
            SET stock_actual = stock_actual + %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (cantidad, id_producto), fetch=False)
        return True
    
    @staticmethod
    def decrementar_stock(id_producto, cantidad):
        """Decrementa el stock de un producto"""
        query = """
            UPDATE productos 
            SET stock_actual = stock_actual - %s
            WHERE id = %s AND stock_actual >= %s
        """
        
        filas_afectadas = ejecutar_query(
            query, 
            (cantidad, id_producto, cantidad), 
            fetch=False
        )
        return filas_afectadas > 0
    
    @staticmethod
    def cambiar_estado(id_producto, activo):
        """Activa o desactiva un producto"""
        query = """
            UPDATE productos 
            SET activo = %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (activo, id_producto), fetch=False)
        return True
    
    @staticmethod
    def eliminar(id_producto):
        """Elimina un producto (desactiva)"""
        return Producto.cambiar_estado(id_producto, 0)
    
    @staticmethod
    def existe_codigo(codigo, excluir_id=None):
        """Verifica si un código ya existe"""
        if excluir_id:
            query = """
                SELECT COUNT(*) as total
                FROM productos 
                WHERE codigo = %s AND id != %s
            """
            resultado = ejecutar_query(query, (codigo, excluir_id))
        else:
            query = """
                SELECT COUNT(*) as total
                FROM productos 
                WHERE codigo = %s
            """
            resultado = ejecutar_query(query, (codigo,))
        
        return resultado[0]['total'] > 0 if resultado else False
    
    @staticmethod
    def obtener_productos_bajo_stock(limite=10):
        """Obtiene productos con stock bajo"""
        query = """
            SELECT id, codigo, descripcion, unidad_medida, 
                   precio, stock_actual, activo
            FROM productos 
            WHERE stock_actual < %s AND activo = 1
            ORDER BY stock_actual ASC
        """
        
        return ejecutar_query(query, (limite,))
    
    @staticmethod
    def obtener_valor_inventario():
        """Calcula el valor total del inventario"""
        query = """
            SELECT SUM(stock_actual * precio) as valor_total
            FROM productos 
            WHERE activo = 1
        """
        
        resultado = ejecutar_query(query)
        return resultado[0]['valor_total'] if resultado[0]['valor_total'] else 0
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas generales de productos"""
        query = """
            SELECT 
                COUNT(*) as total_productos,
                SUM(stock_actual) as total_unidades,
                SUM(stock_actual * precio) as valor_total,
                AVG(precio) as precio_promedio
            FROM productos 
            WHERE activo = 1
        """
        
        resultado = ejecutar_query(query)
        return resultado[0] if resultado else None
    
    @staticmethod
    def obtener_productos_bajo_stock(limite=None):
        """
        Obtiene productos con stock bajo.
        Si limite es None, usa stock_minimo individual de cada producto.
        Si limite es un número, usa ese límite global.
        """
        if limite is None:
            # Usar stock_minimo individual
            query = """
                SELECT 
                    id, codigo, descripcion, unidad_medida, 
                    stock_actual, precio, stock_minimo, activo
                FROM productos 
                WHERE activo = 1 AND stock_actual <= stock_minimo
                ORDER BY stock_actual ASC, descripcion ASC
            """
            return ejecutar_query(query)
        else:
            # Usar límite global
            query = """
                SELECT 
                    id, codigo, descripcion, unidad_medida, 
                    stock_actual, precio, stock_minimo, activo
                FROM productos 
                WHERE activo = 1 AND stock_actual <= %s
                ORDER BY stock_actual ASC, descripcion ASC
            """
            return ejecutar_query(query, (limite,))
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"