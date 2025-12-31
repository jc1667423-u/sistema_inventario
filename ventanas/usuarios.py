"""
Ventana de Gestión de Usuarios
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.usuarios import Usuario
from constantes import *
from utilis import *

class VentanaUsuarios:
    """Ventana para gestionar usuarios del sistema"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        
        # Verificar permisos
        if not self.usuario.tiene_permiso('usuarios', 'ver'):
            mostrar_error("No tiene permisos para acceder a este módulo")
            return
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Usuarios")
        self.ventana.geometry("1200x700")
        centrar_ventana(self.ventana, 1200, 700)
        
        self.usuario_seleccionado = None
        
        self.crear_interfaz()
        self.cargar_usuarios()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana"""
        
        # Frame principal
        frame_principal = ttk.Frame(self.ventana)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_PRIMARIO, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="👥 Gestión de Usuarios",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor
        frame_contenedor = ttk.Frame(frame_principal)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Columna izquierda - Lista
        frame_izquierdo = ttk.Frame(frame_contenedor)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha - Formulario
        frame_derecho = ttk.Frame(frame_contenedor, width=400)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        frame_derecho.pack_propagate(False)
        
        # Crear secciones
        self.crear_seccion_lista(frame_izquierdo)
        self.crear_seccion_formulario(frame_derecho)
    
    def crear_seccion_lista(self, parent):
        """Crea la sección de lista de usuarios"""
        frame_lista = ttk.LabelFrame(
            parent,
            text="Lista de Usuarios",
            padding=10
        )
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        # Botón actualizar
        frame_botones_top = ttk.Frame(frame_lista)
        frame_botones_top.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        btn_actualizar = ttk.Button(
            frame_botones_top,
            text="↻ Actualizar",
            command=self.cargar_usuarios,
            style="TButton"
        )
        btn_actualizar.pack(side=tk.LEFT)
        
        # Frame para el treeview
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL)
        
        # Treeview
        columnas = ('ID', 'Usuario', 'Nombre Completo', 'Rol', 'Estado', 'Último Acceso')
        self.tree = ttk.Treeview(
            frame_tree,
            columns=columnas,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=20
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        anchos = [50, 120, 250, 150, 80, 150]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            align = 'center' if col != 'Nombre Completo' else 'w'
            self.tree.column(col, width=ancho, anchor=align)
        
        # Colocar widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # No usar colores de fondo para filas (mejor para tema oscuro)
        
        # Eventos
        self.tree.bind('<<TreeviewSelect>>', self.on_seleccionar_usuario)
        self.tree.bind('<Double-1>', lambda e: self.cargar_usuario_seleccionado())
    
    def crear_seccion_formulario(self, parent):
        """Crea la sección del formulario"""
        frame_form = ttk.LabelFrame(
            parent,
            text="Datos del Usuario",
            padding=10
        )
        frame_form.pack(fill=tk.BOTH, expand=True)
        
        frame_interno = ttk.Frame(frame_form)
        frame_interno.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Variables
        self.var_id = tk.StringVar()
        self.var_username = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_rol = tk.StringVar(value="trabajador")
        self.var_password = tk.StringVar()
        self.var_confirmar_password = tk.StringVar()
        self.var_activo = tk.IntVar(value=1)
        
        # ID (oculto)
        # self.var_id = tk.StringVar() # This line was already present at the top of the variables section. Keeping it there.
        
        # Username
        ttk.Label(
            frame_interno,
            text="Usuario *",
            font=("Segoe UI", 9, "bold")
        ).pack(fill=tk.X, pady=(0, 2))
        
        self.entry_username = ttk.Entry(
            frame_interno,
            textvariable=self.var_username,
            font=("Arial", 10)
        )
        self.entry_username.pack(fill=tk.X, ipady=5)
        
        # Nombre completo
        ttk.Label(
            frame_interno,
            text="Nombre Completo *",
            font=("Segoe UI", 9, "bold")
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_nombre = ttk.Entry(
            frame_interno,
            textvariable=self.var_nombre,
            font=("Arial", 10)
        )
        self.entry_nombre.pack(fill=tk.X, ipady=5)
        
        # Rol
        ttk.Label(
            frame_interno,
            text="Rol *",
            font=("Segoe UI", 9, "bold")
        ).pack(fill=tk.X, pady=(15, 2))
        
        frame_rol = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_rol.pack(fill=tk.X, pady=(5, 0))
        
        if self.usuario.rol == ROL_SUPER_ADMIN:
            roles = [
                ("Super Admin", ROL_SUPER_ADMIN),
                ("Admin", ROL_ADMIN),
                ("Trabajador", ROL_TRABAJADOR)
            ]
        else:
            roles = [
                ("Admin", ROL_ADMIN),
                ("Trabajador", ROL_TRABAJADOR)
            ]
        
        for texto, valor in roles:
            rb = ttk.Radiobutton(
                frame_rol,
                text=texto,
                variable=self.var_rol,
                value=valor
            )
            rb.pack(side=tk.LEFT, padx=(0, 10))
        
        # Contraseña
        tk.Label(
            frame_interno,
            text="Contraseña *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_password = ttk.Entry(
            frame_interno,
            textvariable=self.var_password,
            font=("Arial", 10),
            show="●"
        )
        self.entry_password.pack(fill=tk.X, ipady=5)
        
        tk.Label(
            frame_interno,
            text="(Dejar vacío para no cambiar)",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).pack(fill=tk.X, pady=(2, 0))
        
        # Confirmar contraseña
        tk.Label(
            frame_interno,
            text="Confirmar Contraseña *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_confirmar = ttk.Entry(
            frame_interno,
            textvariable=self.var_confirmar_password,
            font=("Arial", 10),
            show="●"
        )
        self.entry_confirmar.pack(fill=tk.X, ipady=5)
        
        # Estado
        tk.Label(
            frame_interno,
            text="Estado",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        check_activo = ttk.Checkbutton(
            frame_interno,
            text="Usuario Activo",
            variable=self.var_activo
        )
        check_activo.pack(anchor='w', pady=(5, 0))
        
        # Nota
        label_nota = tk.Label(
            frame_interno,
            text="* Campos obligatorios\n\nLa contraseña debe tener\nal menos 6 caracteres",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            justify='left'
        )
        label_nota.pack(fill=tk.X, pady=(20, 20))
        
        # Botones
        frame_botones = ttk.Frame(frame_interno)
        frame_botones.pack(fill=tk.X, pady=(10, 0))
        
        self.btn_guardar = ttk.Button(
            frame_botones,
            text="💾 Guardar",
            command=self.guardar_usuario,
            style="TButton"
        )
        self.btn_guardar.pack(fill=tk.X, ipady=8, pady=5)
        
        self.btn_nuevo = ttk.Button(
            frame_botones,
            text="➕ Nuevo",
            command=self.limpiar_formulario,
            style="TButton"
        )
        self.btn_nuevo.pack(fill=tk.X, ipady=8, pady=5)
        
        self.btn_eliminar = ttk.Button(
            frame_botones,
            text="🗑️ Eliminar Usuario",
            command=self.eliminar_usuario,
            style="Danger.TButton"
        )
        self.btn_eliminar.pack(fill=tk.X, ipady=8, pady=5)
    
    def cargar_usuarios(self):
        """Carga todos los usuarios"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            usuarios = Usuario.obtener_todos()
            
            for user in usuarios:
                ultimo_acceso = formatear_fecha_hora(user['ultimo_acceso']) if user['ultimo_acceso'] else 'Nunca'
                estado = '✓ Activo' if user['activo'] else '✗ Inactivo'
                
                self.tree.insert('', tk.END, values=(
                    user['id'],
                    user['username'],
                    user['nombre_completo'],
                    ROLES.get(user['rol'], user['rol']),
                    estado,
                    ultimo_acceso
                ))
            
        except Exception as e:
            mostrar_error(f"Error al cargar usuarios:\n{str(e)}")
    
    def on_seleccionar_usuario(self, event):
        """Evento cuando se selecciona un usuario"""
        seleccion = self.tree.selection()
        if seleccion:
            if hasattr(self, 'btn_eliminar'):
                self.btn_eliminar.config(state=tk.NORMAL)
            valores = self.tree.item(seleccion[0])['values']
            self.usuario_seleccionado = valores[0]
        else:
            if hasattr(self, 'btn_eliminar'):
                self.btn_eliminar.config(state=tk.DISABLED)
            self.usuario_seleccionado = None
    
    def cargar_usuario_seleccionado(self):
        """Carga los datos del usuario seleccionado"""
        if not self.usuario_seleccionado:
            return
        
        try:
            usuario = Usuario.obtener_por_id(self.usuario_seleccionado)
            
            if usuario:
                self.var_id.set(usuario.id)
                self.var_username.set(usuario.username)
                self.var_nombre.set(usuario.nombre_completo)
                self.var_rol.set(usuario.rol)
                self.var_activo.set(usuario.activo)
                
                # Limpiar contraseñas
                self.var_password.set("")
                self.var_confirmar_password.set("")
                
                self.entry_username.focus()
                
        except Exception as e:
            mostrar_error(f"Error al cargar usuario:\n{str(e)}")
    
    def guardar_usuario(self):
        """Guarda o actualiza un usuario"""
        # Validaciones
        if not validar_campo_vacio(self.var_username.get(), "Usuario"):
            return
        if not validar_campo_vacio(self.var_nombre.get(), "Nombre Completo"):
            return
        
        username = self.var_username.get().strip()
        nombre = self.var_nombre.get().strip()
        rol = self.var_rol.get()
        activo = self.var_activo.get()
        password = self.var_password.get()
        confirmar = self.var_confirmar_password.get()
        
        id_usuario = self.var_id.get()
        
        try:
            # Si es nuevo usuario o si está cambiando contraseña
            if not id_usuario or password:
                if not password:
                    mostrar_error("La contraseña es obligatoria para nuevos usuarios")
                    return
                
                if len(password) < MIN_LONGITUD_PASSWORD:
                    mostrar_error(f"La contraseña debe tener al menos {MIN_LONGITUD_PASSWORD} caracteres")
                    return
                
                if password != confirmar:
                    mostrar_error("Las contraseñas no coinciden")
                    return
            
            if id_usuario:  # Actualizar
                # No permitir que un usuario se desactive a sí mismo
                if int(id_usuario) == self.usuario.id and activo == 0:
                    mostrar_error("No puede desactivarse a sí mismo")
                    return
                
                # Verificar username duplicado
                if Usuario.existe_username(username, int(id_usuario)):
                    mostrar_error(f"El usuario '{username}' ya existe")
                    return
                
                # Actualizar datos básicos
                Usuario.actualizar(int(id_usuario), username, nombre, rol, activo)
                
                # Actualizar contraseña si se proporcionó
                if password:
                    nuevo_hash = hashear_password(password)
                    Usuario.cambiar_password(int(id_usuario), nuevo_hash)
                
                mostrar_exito("Usuario actualizado correctamente")
                
            else:  # Crear nuevo
                if Usuario.existe_username(username):
                    mostrar_error(f"El usuario '{username}' ya existe")
                    return
                
                Usuario.crear(username, password, nombre, rol)
                mostrar_exito("Usuario creado correctamente")
            
            self.cargar_usuarios()
            self.limpiar_formulario()
            
        except Exception as e:
            mostrar_error(f"Error al guardar usuario:\n{str(e)}")
    
    def eliminar_usuario(self):
        """Desactiva un usuario"""
        if not self.usuario_seleccionado:
            mostrar_error("Seleccione un usuario")
            return
        
        # No permitir desactivarse a sí mismo
        if self.usuario_seleccionado == self.usuario.id:
            mostrar_error("No puede desactivarse a sí mismo")
            return
        
        if confirmar_accion("Confirmar", "¿Está seguro de desactivar este usuario?"):
            try:
                Usuario.eliminar(self.usuario_seleccionado)
                mostrar_exito("Usuario desactivado correctamente")
                self.cargar_usuarios()
                self.limpiar_formulario()
                
            except Exception as e:
                mostrar_error(f"Error al desactivar usuario:\n{str(e)}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.var_id.set("")
        self.var_username.set("")
        self.var_nombre.set("")
        self.var_rol.set("trabajador")
        self.var_password.set("")
        self.var_confirmar_password.set("")
        self.var_activo.set(1)
        
        if hasattr(self, 'btn_eliminar'):
            self.btn_eliminar.config(state=tk.DISABLED)
        self.usuario_seleccionado = None
        
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        self.entry_username.focus()