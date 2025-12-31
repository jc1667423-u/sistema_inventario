"""
Clase Usuario para gestión de usuarios del sistema
"""
from base_datos.config_db import ejecutar_query
from utilis import hashear_password, verificar_password
from datetime import datetime

# Importar logger
try:
    from logger import log_autenticacion, log_accion_critica, obtener_logger
    logger = obtener_logger('usuarios')
except ImportError:
    logger = None
    log_autenticacion = None
    log_accion_critica = None

class Usuario:
    """Clase que representa un usuario del sistema"""
    
    def __init__(self, id, username, nombre_completo, rol, activo=1, debe_cambiar_password=0):
        self.id = id
        self.username = username
        self.nombre_completo = nombre_completo
        self.rol = rol
        self.activo = activo
        self.debe_cambiar_password = debe_cambiar_password
    
    @staticmethod
    def autenticar(username, password):
        """
        Autentica un usuario con su username y password
        Retorna: objeto Usuario si es válido, None si no
        """
        query = """
            SELECT id, username, password_hash, nombre_completo, rol, 
                   activo, debe_cambiar_password
            FROM usuarios 
            WHERE username = %s
        """
        
        resultado = ejecutar_query(query, (username,))
        
        if resultado and len(resultado) > 0:
            usuario_data = resultado[0]
            
            # Verificar contraseña
            if verificar_password(password, usuario_data['password_hash']):
                # Login exitoso
                if log_autenticacion:
                    log_autenticacion(username, True, f"Rol: {usuario_data['rol']}")
                
                return Usuario(
                    id=usuario_data['id'],
                    username=usuario_data['username'],
                    nombre_completo=usuario_data['nombre_completo'],
                    rol=usuario_data['rol'],
                    activo=usuario_data['activo'],
                    debe_cambiar_password=usuario_data['debe_cambiar_password']
                )
            else:
                # Contraseña incorrecta
                if log_autenticacion:
                    log_autenticacion(username, False, "Contraseña incorrecta")
        else:
            # Usuario no encontrado
            if log_autenticacion:
                log_autenticacion(username, False, "Usuario no encontrado")
        
        return None
    
    @staticmethod
    def obtener_por_id(id_usuario):
        """Obtiene un usuario por su ID"""
        query = """
            SELECT id, username, nombre_completo, rol, activo, debe_cambiar_password
            FROM usuarios 
            WHERE id = %s
        """
        
        resultado = ejecutar_query(query, (id_usuario,))
        
        if resultado and len(resultado) > 0:
            u = resultado[0]
            return Usuario(
                id=u['id'],
                username=u['username'],
                nombre_completo=u['nombre_completo'],
                rol=u['rol'],
                activo=u['activo'],
                debe_cambiar_password=u['debe_cambiar_password']
            )
        
        return None
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los usuarios"""
        query = """
            SELECT id, username, nombre_completo, rol, activo, 
                   fecha_creacion, ultimo_acceso
            FROM usuarios 
            ORDER BY nombre_completo
        """
        
        return ejecutar_query(query)
    
    @staticmethod
    def crear(username, password, nombre_completo, rol):
        """Crea un nuevo usuario"""
        password_hash = hashear_password(password)
        
        query = """
            INSERT INTO usuarios (username, password_hash, nombre_completo, rol)
            VALUES (%s, %s, %s, %s)
        """
        
        ejecutar_query(query, (username, password_hash, nombre_completo, rol), fetch=False)
        
        # Log de creación
        if log_accion_critica:
            log_accion_critica('usuarios', f'Crear usuario: {username}', 'Sistema', f'Rol: {rol}')
        
        return True
    
    @staticmethod
    def actualizar(id_usuario, username, nombre_completo, rol, activo):
        """Actualiza los datos de un usuario"""
        query = """
            UPDATE usuarios 
            SET username = %s, nombre_completo = %s, rol = %s, activo = %s
            WHERE id = %s
        """
        
        ejecutar_query(query, (username, nombre_completo, rol, activo, id_usuario), fetch=False)
        return True
    
    @staticmethod
    def cambiar_password(id_usuario, nueva_password_hash):
        """Cambia la contraseña de un usuario"""
        query = """
            UPDATE usuarios 
            SET password_hash = %s, debe_cambiar_password = 0
            WHERE id = %s
        """
        
        ejecutar_query(query, (nueva_password_hash, id_usuario), fetch=False)
        
        # Log de cambio de contraseña
        if logger:
            logger.info(f"Cambio de contraseña - Usuario ID: {id_usuario}")
        
        return True
    
    @staticmethod
    def actualizar_ultimo_acceso(id_usuario):
        """Actualiza la fecha de último acceso"""
        query = """
            UPDATE usuarios 
            SET ultimo_acceso = %s
            WHERE id = %s
        """
        
        fecha_actual = datetime.now()
        ejecutar_query(query, (fecha_actual, id_usuario), fetch=False)
        return True
    
    @staticmethod
    def eliminar(id_usuario):
        """Elimina un usuario (desactiva)"""
        query = """
            UPDATE usuarios 
            SET activo = 0
            WHERE id = %s
        """
        
        ejecutar_query(query, (id_usuario,), fetch=False)
        
        # Log de eliminación
        if log_accion_critica:
            log_accion_critica('usuarios', f'Eliminar usuario ID: {id_usuario}', 'Sistema', 'Usuario desactivado')
        
        return True
    
    @staticmethod
    def existe_username(username, excluir_id=None):
        """Verifica si un username ya existe"""
        if excluir_id:
            query = """
                SELECT COUNT(*) as total
                FROM usuarios 
                WHERE username = %s AND id != %s
            """
            resultado = ejecutar_query(query, (username, excluir_id))
        else:
            query = """
                SELECT COUNT(*) as total
                FROM usuarios 
                WHERE username = %s
            """
            resultado = ejecutar_query(query, (username,))
        
        return resultado[0]['total'] > 0 if resultado else False
    
    def tiene_permiso(self, modulo, accion):
        """Verifica si el usuario tiene un permiso específico"""
        from constantes import PERMISOS
        
        if self.rol in PERMISOS:
            permisos_rol = PERMISOS[self.rol]
            if modulo in permisos_rol:
                return accion in permisos_rol[modulo]
        
        return False
    
    def __str__(self):
        return f"{self.nombre_completo} ({self.username})"