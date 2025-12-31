"""
Clase Transaccion para gestión de movimientos de inventario
"""
from base_datos.config_db import ejecutar_query
from clases.productos import Producto
from datetime import datetime

# Importar logger
try:
    from logger import log_transaccion, log_accion_critica, obtener_logger
    logger = obtener_logger('transacciones')
except ImportError:
    logger = None
    log_transaccion = None
    log_accion_critica = None

class Transaccion:
    """Clase que representa una transacción de inventario"""
    
    def __init__(self, id, producto_id, cantidad_entrada, cantidad_salida, 
                 costo, valor_entrada, valor_salida, fecha, 
                 cliente_proveedor_id, documento, tipo_movimiento, 
                 concepto, usuario_id):
        self.id = id
        self.producto_id = producto_id
        self.cantidad_entrada = cantidad_entrada
        self.cantidad_salida = cantidad_salida
        self.costo = costo
        self.valor_entrada = valor_entrada
        self.valor_salida = valor_salida
        self.fecha = fecha
        self.cliente_proveedor_id = cliente_proveedor_id
        self.documento = documento
        self.tipo_movimiento = tipo_movimiento
        self.concepto = concepto
        self.usuario_id = usuario_id
    
    @staticmethod
    def registrar_entrada(producto_id, cantidad, costo, fecha, proveedor_id, 
                         documento, concepto, usuario_id):
        """Registra una entrada de mercancía"""
        try:
            valor_entrada = cantidad * costo
            
            query = """
                INSERT INTO transacciones 
                (producto_id, cantidad_entrada, cantidad_salida, costo, 
                 valor_entrada, valor_salida, fecha, cliente_proveedor_id, 
                 documento, tipo_movimiento, concepto, usuario_id)
                VALUES (%s, %s, 0, %s, %s, 0, %s, %s, %s, 'Entrada', %s, %s)
            """
            
            ejecutar_query(
                query,
                (producto_id, cantidad, costo, valor_entrada, fecha, 
                 proveedor_id, documento, concepto, usuario_id),
                fetch=False
            )
            
            # Actualizar stock
            Producto.incrementar_stock(producto_id, cantidad)
            
            # Log de transacción
            if log_transaccion:
                producto = Producto.obtener_por_id(producto_id)
                producto_desc = f"{producto.codigo}" if producto else f"ID:{producto_id}"
                log_transaccion('Entrada', producto_desc, cantidad, usuario_id, f"Doc: {documento}")
            
            return True
            
        except Exception as e:
            # Log de error
            if logger:
                logger.error(f"Error al registrar entrada - Producto ID: {producto_id} - {str(e)}")
            raise Exception(f"Error al registrar entrada: {str(e)}")
    
    @staticmethod
    def registrar_salida(producto_id, cantidad, precio, fecha, cliente_id, 
                        documento, concepto, usuario_id):
        """Registra una salida de mercancía"""
        try:
            # Verificar stock disponible
            producto = Producto.obtener_por_id(producto_id)
            if not producto:
                raise Exception("Producto no encontrado")
            
            if producto.stock_actual < cantidad:
                raise Exception(f"Stock insuficiente. Disponible: {producto.stock_actual}")
            
            valor_salida = cantidad * precio
            
            query = """
                INSERT INTO transacciones 
                (producto_id, cantidad_entrada, cantidad_salida, costo, 
                 valor_entrada, valor_salida, fecha, cliente_proveedor_id, 
                 documento, tipo_movimiento, concepto, usuario_id)
                VALUES (%s, 0, %s, %s, 0, %s, %s, %s, %s, 'Salida', %s, %s)
            """
            
            ejecutar_query(
                query,
                (producto_id, cantidad, precio, valor_salida, fecha, 
                 cliente_id, documento, concepto, usuario_id),
                fetch=False
            )
            
            # Actualizar stock
            Producto.decrementar_stock(producto_id, cantidad)
            
            # Log de transacción
            if log_transaccion:
                log_transaccion('Salida', producto.codigo, cantidad, usuario_id, f"Doc: {documento}")
            
            return True
            
        except Exception as e:
            # Log de error (especialmente stock insuficiente)
            if logger:
                if "Stock insuficiente" in str(e):
                    logger.warning(f"Intento de salida con stock insuficiente - Producto ID: {producto_id} - Cantidad solicitada: {cantidad}")
                else:
                    logger.error(f"Error al registrar salida - Producto ID: {producto_id} - {str(e)}")
            raise Exception(f"Error al registrar salida: {str(e)}")
    
    @staticmethod
    def obtener_todas(limite=100):
        """Obtiene todas las transacciones"""
        query = """
            SELECT t.*, p.codigo as producto_codigo, p.descripcion as producto_descripcion,
                   cp.nombre as entidad_nombre, u.nombre_completo as usuario_nombre
            FROM transacciones t
            INNER JOIN productos p ON t.producto_id = p.id
            LEFT JOIN clientes_proveedores cp ON t.cliente_proveedor_id = cp.id
            INNER JOIN usuarios u ON t.usuario_id = u.id
            ORDER BY t.fecha DESC, t.id DESC
            LIMIT %s
        """
        
        return ejecutar_query(query, (limite,))
    
    @staticmethod
    def obtener_por_producto(producto_id, limite=50):
        """Obtiene transacciones de un producto específico (Kardex)"""
        query = """
            SELECT t.*, cp.nombre as entidad_nombre, u.nombre_completo as usuario_nombre
            FROM transacciones t
            LEFT JOIN clientes_proveedores cp ON t.cliente_proveedor_id = cp.id
            INNER JOIN usuarios u ON t.usuario_id = u.id
            WHERE t.producto_id = %s
            ORDER BY t.fecha ASC, t.id ASC
            LIMIT %s
        """
        
        return ejecutar_query(query, (producto_id, limite))
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene transacciones en un rango de fechas"""
        query = """
            SELECT t.*, p.codigo as producto_codigo, p.descripcion as producto_descripcion,
                   cp.nombre as entidad_nombre, u.nombre_completo as usuario_nombre
            FROM transacciones t
            INNER JOIN productos p ON t.producto_id = p.id
            LEFT JOIN clientes_proveedores cp ON t.cliente_proveedor_id = cp.id
            INNER JOIN usuarios u ON t.usuario_id = u.id
            WHERE DATE(t.fecha) BETWEEN %s AND %s
            ORDER BY t.fecha DESC, t.id DESC
        """
        
        return ejecutar_query(query, (fecha_inicio, fecha_fin))
    
    @staticmethod
    def obtener_por_tipo(tipo_movimiento, limite=100):
        """Obtiene transacciones por tipo (Entrada/Salida)"""
        query = """
            SELECT t.*, p.codigo as producto_codigo, p.descripcion as producto_descripcion,
                   cp.nombre as entidad_nombre, u.nombre_completo as usuario_nombre
            FROM transacciones t
            INNER JOIN productos p ON t.producto_id = p.id
            LEFT JOIN clientes_proveedores cp ON t.cliente_proveedor_id = cp.id
            INNER JOIN usuarios u ON t.usuario_id = u.id
            WHERE t.tipo_movimiento = %s
            ORDER BY t.fecha DESC, t.id DESC
            LIMIT %s
        """
        
        return ejecutar_query(query, (tipo_movimiento, limite))
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de transacciones"""
        query = """
            SELECT 
                COUNT(*) as total_transacciones,
                SUM(CASE WHEN tipo_movimiento = 'Entrada' THEN 1 ELSE 0 END) as total_entradas,
                SUM(CASE WHEN tipo_movimiento = 'Salida' THEN 1 ELSE 0 END) as total_salidas,
                SUM(cantidad_entrada) as total_unidades_entrada,
                SUM(cantidad_salida) as total_unidades_salida,
                SUM(valor_entrada) as total_valor_entradas,
                SUM(valor_salida) as total_valor_salidas
            FROM transacciones
        """
        
        resultado = ejecutar_query(query)
        return resultado[0] if resultado else None
    
    @staticmethod
    def eliminar(id_transaccion):
        """Elimina una transacción y revierte el stock"""
        try:
            # Obtener datos de la transacción
            query = "SELECT * FROM transacciones WHERE id = %s"
            resultado = ejecutar_query(query, (id_transaccion,))
            
            if not resultado:
                raise Exception("Transacción no encontrada")
            
            trans = resultado[0]
            
            # Revertir stock
            if trans['tipo_movimiento'] == 'Entrada':
                Producto.decrementar_stock(trans['producto_id'], trans['cantidad_entrada'])
            else:  # Salida
                Producto.incrementar_stock(trans['producto_id'], trans['cantidad_salida'])
            
            # Eliminar transacción
            query_delete = "DELETE FROM transacciones WHERE id = %s"
            ejecutar_query(query_delete, (id_transaccion,), fetch=False)
            
            # Log de eliminación
            if log_accion_critica:
                log_accion_critica('transacciones', f'Eliminar transacción ID: {id_transaccion}', 'Sistema', 
                                 f"Tipo: {trans['tipo_movimiento']}, Producto ID: {trans['producto_id']}")
            
            return True
            
        except Exception as e:
            if logger:
                logger.error(f"Error al eliminar transacción ID: {id_transaccion} - {str(e)}")
            raise Exception(f"Error al eliminar transacción: {str(e)}")
    
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.fecha}"