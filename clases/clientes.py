"""
Clase ClienteProveedor para gestión de clientes y proveedores
"""
from base_datos.config_db import ejecutar_query

class ClienteProveedor:
    """Clase que representa un cliente, proveedor o ambos"""
    
    def __init__(self, id, codigo, nombre, tipo, activo=1):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.activo = activo
    
    @staticmethod
    def obtener_todos(tipo_filtro=None, solo_activos=True):
        """
        Obtiene todos los clientes/proveedores
        tipo_filtro: 'cliente', 'proveedor', 'ambos' o None para todos
        """
        if tipo_filtro:
            if solo_activos:
                query = """
                    SELECT id, codigo, nombre, tipo, activo
                    FROM clientes_proveedores 
                    WHERE tipo = %s AND activo = 1
                    ORDER BY nombre
                """
                return ejecutar_query(query, (tipo_filtro,))
            else:
                query = """
                    SELECT id, codigo, nombre, tipo, activo
                    FROM clientes_proveedores 
                    WHERE tipo = %s
                    ORDER BY nombre
                """
                return ejecutar_query(query, (tipo_filtro,))
        else:
            if solo_activos:
                query = """
                    SELECT id, codigo, nombre, tipo, activo
                    FROM clientes_proveedores 
                    WHERE activo = 1
                    ORDER BY nombre
                """
            else:
                query = """
                    SELECT id, codigo, nombre, tipo, activo
                    FROM clientes_proveedores 
                    ORDER BY nombre
                """
            return ejecutar_query(query)
    
    @staticmethod
    def obtener_clientes(solo_activos=True):
        """Obtiene solo clientes"""
        if solo_activos:
            query = """
                SELECT id, codigo, nombre, tipo, activo
                FROM clientes_proveedores 
                WHERE (tipo = 'cliente' OR tipo = 'ambos') AND activo = 1
                ORDER BY nombre
            """
        else:
            query = """
                SELECT id, codigo, nombre, tipo, activo
                FROM clientes_proveedores 
                WHERE tipo = 'cliente' OR tipo = 'ambos'
                ORDER BY nombre
            """
        return ejecutar_query(query)
    
    @staticmethod
    def obtener_proveedores(solo_activos=True):
        """Obtiene solo proveedores"""
        if solo_activos:
            query = """
                SELECT id, codigo, nombre, tipo, activo
                FROM clientes_proveedores 
                WHERE (tipo = 'proveedor' OR tipo = 'ambos') AND activo = 1
                ORDER BY nombre
            """
        else:
            query = """
                SELECT id, codigo, nombre, tipo, activo
                FROM clientes_proveedores 
                WHERE tipo = 'proveedor' OR tipo = 'ambos'
                ORDER BY nombre
            """
        return ejecutar_query(query)
    
    @staticmethod
    def obtener_por_id(id_entidad):
        """Obtiene una entidad por su ID"""
        query = """
            SELECT id, codigo, nombre, tipo, activo
            FROM clientes_proveedores 
            WHERE id = %s
        """
        
        resultado = ejecutar_query(query, (id_entidad,))
        
        if resultado and len(resultado) > 0:
            e = resultado[0]
            return ClienteProveedor(
                id=e['id'],
                codigo=e['codigo'],
                nombre=e['nombre'],
                tipo=e['tipo'],
                activo=e['activo']
            )
        
        return None
    
    @staticmethod
    def obtener_por_codigo(codigo):
        """Obtiene una entidad por su código"""
        query = """
            SELECT id, codigo, nombre, tipo, activo
            FROM clientes_proveedores 
            WHERE codigo = %s
        """
        
        resultado = ejecutar_query(query, (codigo,))
        return resultado[0] if resultado else None
    
    @staticmethod
    def buscar(termino, tipo_filtro=None):
        """Busca por código o nombre"""
        if tipo_filtro:
            query = """
                SELECT id, codigo, nombre, tipo, activo
                FROM clientes_proveedores 
                WHERE (codigo LIKE %s OR nombre LIKE %s) 
                AND tipo = %s AND activo = 1
                ORDER BY nombre
            """
            termino_busqueda = f"%{termino}%"
            return ejecutar_query(query, (termino_busqueda, termino_busqueda, tipo_filtro))
        else:
            query = """
                SELECT id, codigo, nombre, tipo, activo
                FROM clientes_proveedores 
                WHERE (codigo LIKE %s OR nombre LIKE %s) AND activo = 1
                ORDER BY nombre
            """
            termino_busqueda = f"%{termino}%"
            return ejecutar_query(query, (termino_busqueda, termino_busqueda))
    
    @staticmethod
    def crear(codigo, nombre, tipo):
        """Crea un nuevo cliente/proveedor"""
        query = """
            INSERT INTO clientes_proveedores 
            (codigo, nombre, tipo, activo)
            VALUES (%s, %s, %s, 1)
        """
        
        ejecutar_query(query, (codigo, nombre, tipo), fetch=False)
        return True
    
    @staticmethod
    def actualizar(id_entidad, codigo, nombre, tipo):
        """Actualiza los datos de un cliente/proveedor"""
        query = """
            UPDATE clientes_proveedores 
            SET codigo = %s, nombre = %s, tipo = %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (codigo, nombre, tipo, id_entidad), fetch=False)
        return True
    
    @staticmethod
    def cambiar_estado(id_entidad, activo):
        """Activa o desactiva una entidad"""
        query = """
            UPDATE clientes_proveedores 
            SET activo = %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (activo, id_entidad), fetch=False)
        return True
    
    @staticmethod
    def eliminar(id_entidad):
        """Elimina (desactiva) una entidad"""
        return ClienteProveedor.cambiar_estado(id_entidad, 0)
    
    @staticmethod
    def existe_codigo(codigo, excluir_id=None):
        """Verifica si un código ya existe"""
        if excluir_id:
            query = """
                SELECT COUNT(*) as total
                FROM clientes_proveedores 
                WHERE codigo = %s AND id != %s
            """
            resultado = ejecutar_query(query, (codigo, excluir_id))
        else:
            query = """
                SELECT COUNT(*) as total
                FROM clientes_proveedores 
                WHERE codigo = %s
            """
            resultado = ejecutar_query(query, (codigo,))
        
        return resultado[0]['total'] > 0 if resultado else False
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas generales"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN tipo = 'cliente' THEN 1 ELSE 0 END) as total_clientes,
                SUM(CASE WHEN tipo = 'proveedor' THEN 1 ELSE 0 END) as total_proveedores,
                SUM(CASE WHEN tipo = 'ambos' THEN 1 ELSE 0 END) as total_ambos
            FROM clientes_proveedores 
            WHERE activo = 1
        """
        
        resultado = ejecutar_query(query)
        return resultado[0] if resultado else None
    
    @staticmethod
    def obtener_transacciones(id_entidad, limite=10):
        """Obtiene las últimas transacciones de una entidad"""
        query = """
            SELECT t.id, t.fecha, t.tipo_movimiento, p.descripcion as producto,
                   t.cantidad_entrada, t.cantidad_salida, t.documento
            FROM transacciones t
            INNER JOIN productos p ON t.producto_id = p.id
            WHERE t.cliente_proveedor_id = %s
            ORDER BY t.fecha DESC
            LIMIT %s
        """
        
        return ejecutar_query(query, (id_entidad, limite))
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"