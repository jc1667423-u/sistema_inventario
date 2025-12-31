"""
Ventana de Gestión de Clientes y Proveedores
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.clientes import ClienteProveedor
from constantes import *
from utilis import (
    centrar_ventana, validar_campo_vacio,
    mostrar_exito, mostrar_error, confirmar_accion
)

class VentanaClientesProveedores:
    """Ventana para gestionar clientes y proveedores"""
    
    def __init__(self, parent, usuario, tipo_default='cliente'):
        self.parent = parent
        self.usuario = usuario
        self.tipo_default = tipo_default
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Clientes y Proveedores")
        self.ventana.geometry("1200x700")
        centrar_ventana(self.ventana, 1200, 700)
        
        self.entidad_seleccionada = None
        
        self.crear_interfaz()
        self.cargar_entidades()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana"""
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_PRIMARIO, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="👥 Gestión de Clientes y Proveedores",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Columna izquierda - Lista
        frame_izquierdo = tk.Frame(frame_contenedor, bg=COLOR_FONDO)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha - Formulario
        frame_derecho = tk.Frame(frame_contenedor, bg=COLOR_FONDO, width=400)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        frame_derecho.pack_propagate(False)
        
        # Crear secciones
        self.crear_seccion_filtros(frame_izquierdo)
        self.crear_seccion_lista(frame_izquierdo)
        self.crear_seccion_formulario(frame_derecho)
    
    def crear_seccion_filtros(self, parent):
        """Crea la sección de filtros y búsqueda"""
        frame_filtros = tk.LabelFrame(
            parent,
            text="Filtros y Búsqueda",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_filtros.pack(fill=tk.X, pady=(0, 10))
        
        frame_interno = tk.Frame(frame_filtros, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        # Filtro por tipo
        frame_tipo = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_tipo.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_tipo,
            text="Mostrar:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.var_filtro_tipo = tk.StringVar(value="todos")
        
        tipos = [
            ("Todos", "todos"),
            ("Clientes", "cliente"),
            ("Proveedores", "proveedor"),
            ("Ambos", "ambos")
        ]
        
        for texto, valor in tipos:
            rb = ttk.Radiobutton(
                frame_tipo,
                text=texto,
                variable=self.var_filtro_tipo,
                value=valor,
                command=self.aplicar_filtros
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Búsqueda
        frame_busqueda = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_busqueda.pack(fill=tk.X)
        
        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace('w', lambda *args: self.buscar_entidades())
        
        label_buscar = tk.Label(
            frame_busqueda,
            text="🔍 Buscar:",
            font=("Arial", 10),
            bg=COLOR_BLANCO
        )
        label_buscar.pack(side=tk.LEFT, padx=(0, 10))
        
        entry_buscar = ttk.Entry(
            frame_busqueda,
            textvariable=self.var_busqueda,
            font=("Arial", 10),
            width=50
        )
        entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Botón actualizar
        btn_actualizar = tk.Button(
            frame_busqueda,
            text="↻",
            font=("Arial", 12, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_entidades,
            width=3
        )
        btn_actualizar.pack(side=tk.LEFT, padx=(10, 0))
    
    def crear_seccion_lista(self, parent):
        """Crea la sección de lista"""
        frame_lista = tk.LabelFrame(
            parent,
            text="Lista de Clientes/Proveedores",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el treeview
        frame_tree = tk.Frame(frame_lista, bg=COLOR_BLANCO)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL)
        
        # Treeview
        columnas = ('ID', 'Código', 'Nombre', 'Tipo', 'Estado')
        self.tree = ttk.Treeview(
            frame_tree,
            columns=columnas,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        anchos = [50, 120, 400, 120, 100]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor='center' if col != 'Nombre' else 'w')
        
        # Colocar widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Eventos
        self.tree.bind('<<TreeviewSelect>>', self.on_seleccionar_entidad)
        self.tree.bind('<Double-1>', lambda e: self.cargar_entidad_seleccionada())
    
    def crear_seccion_formulario(self, parent):
        """Crea la sección del formulario"""
        frame_form = tk.LabelFrame(
            parent,
            text="Datos del Cliente/Proveedor",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_form.pack(fill=tk.BOTH, expand=True)
        
        frame_interno = tk.Frame(frame_form, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Variables
        self.var_id = tk.StringVar()
        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_tipo = tk.StringVar(value=self.tipo_default)
        
        # Código
        tk.Label(
            frame_interno,
            text="Código",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(5, 2))
        
        self.entry_codigo = ttk.Entry(
            frame_interno,
            textvariable=self.var_codigo,
            font=("Arial", 10)
        )
        self.entry_codigo.pack(fill=tk.X, ipady=5)
        
        tk.Label(
            frame_interno,
            text="(Dejar vacío para auto-generar)",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).pack(fill=tk.X, pady=(2, 0))
        
        # Nombre
        tk.Label(
            frame_interno,
            text="Nombre / Razón Social *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_nombre = ttk.Entry(
            frame_interno,
            textvariable=self.var_nombre,
            font=("Arial", 10)
        )
        self.entry_nombre.pack(fill=tk.X, ipady=5)
        
        # Tipo
        tk.Label(
            frame_interno,
            text="Tipo *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        frame_radio = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_radio.pack(fill=tk.X, pady=(5, 0))
        
        rb_cliente = ttk.Radiobutton(
            frame_radio,
            text="Cliente",
            variable=self.var_tipo,
            value="cliente"
        )
        rb_cliente.pack(side=tk.LEFT, padx=(0, 20))
        
        rb_proveedor = ttk.Radiobutton(
            frame_radio,
            text="Proveedor",
            variable=self.var_tipo,
            value="proveedor"
        )
        rb_proveedor.pack(side=tk.LEFT, padx=(0, 20))
        
        rb_ambos = ttk.Radiobutton(
            frame_radio,
            text="Ambos",
            variable=self.var_tipo,
            value="ambos"
        )
        rb_ambos.pack(side=tk.LEFT)
        
        # Separador
        ttk.Separator(frame_interno, orient='horizontal').pack(fill=tk.X, pady=20)
        
        # Nota
        label_nota = tk.Label(
            frame_interno,
            text="* Campos obligatorios",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            justify='left'
        )
        label_nota.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        frame_botones = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_botones.pack(fill=tk.X, pady=(10, 0))
        
        self.btn_guardar = tk.Button(
            frame_botones,
            text="💾 Guardar",
            font=("Arial", 10, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.guardar_entidad
        )
        self.btn_guardar.pack(fill=tk.X, ipady=8, pady=5)
        
        self.btn_nuevo = tk.Button(
            frame_botones,
            text="➕ Nuevo",
            font=("Arial", 10, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.limpiar_formulario
        )
        self.btn_nuevo.pack(fill=tk.X, ipady=8, pady=5)
        
        self.btn_eliminar = tk.Button(
            frame_botones,
            text="🗑️ Eliminar",
            font=("Arial", 10, "bold"),
            bg=COLOR_PELIGRO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.eliminar_entidad,
            state=tk.DISABLED
        )
        self.btn_eliminar.pack(fill=tk.X, ipady=8, pady=5)
    
    def cargar_entidades(self):
        """Carga todas las entidades según filtro"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener filtro
            filtro = self.var_filtro_tipo.get()
            
            # Obtener entidades
            if filtro == "todos":
                entidades = ClienteProveedor.obtener_todos()
            else:
                entidades = ClienteProveedor.obtener_todos(tipo_filtro=filtro)
            
            # Insertar en tabla
            for entidad in entidades:
                tipo_texto = TIPOS_ENTIDAD.get(entidad['tipo'], entidad['tipo'])
                estado = "Activo" if entidad['activo'] == 1 else "Inactivo"
                
                valores = (
                    entidad['id'],
                    entidad['codigo'] if entidad['codigo'] else '-',
                    entidad['nombre'],
                    tipo_texto,
                    estado
                )
                self.tree.insert('', tk.END, values=valores)
            
        except Exception as e:
            mostrar_error(f"Error al cargar entidades:\n{str(e)}")
    
    def aplicar_filtros(self):
        """Aplica los filtros seleccionados"""
        self.cargar_entidades()
    
    def buscar_entidades(self):
        """Busca entidades según el término ingresado"""
        termino = self.var_busqueda.get().strip()
        
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener filtro de tipo
            filtro = self.var_filtro_tipo.get()
            tipo_filtro = None if filtro == "todos" else filtro
            
            # Buscar o mostrar todos
            if termino:
                entidades = ClienteProveedor.buscar(termino, tipo_filtro)
            else:
                if tipo_filtro:
                    entidades = ClienteProveedor.obtener_todos(tipo_filtro=tipo_filtro)
                else:
                    entidades = ClienteProveedor.obtener_todos()
            
            # Insertar en tabla
            for entidad in entidades:
                tipo_texto = TIPOS_ENTIDAD.get(entidad['tipo'], entidad['tipo'])
                estado = "Activo" if entidad['activo'] == 1 else "Inactivo"
                
                valores = (
                    entidad['id'],
                    entidad['codigo'] if entidad['codigo'] else '-',
                    entidad['nombre'],
                    tipo_texto,
                    estado
                )
                self.tree.insert('', tk.END, values=valores)
                
        except Exception as e:
            mostrar_error(f"Error al buscar entidades:\n{str(e)}")
    
    def on_seleccionar_entidad(self, event):
        """Evento cuando se selecciona una entidad"""
        seleccion = self.tree.selection()
        if seleccion:
            self.btn_eliminar.config(state=tk.NORMAL)
            valores = self.tree.item(seleccion[0])['values']
            self.entidad_seleccionada = valores[0]  # ID
        else:
            self.btn_eliminar.config(state=tk.DISABLED)
            self.entidad_seleccionada = None
    
    def cargar_entidad_seleccionada(self):
        """Carga los datos de la entidad seleccionada"""
        if not self.entidad_seleccionada:
            return
        
        try:
            entidad = ClienteProveedor.obtener_por_id(self.entidad_seleccionada)
            
            if entidad:
                self.var_id.set(entidad.id)
                self.var_codigo.set(entidad.codigo if entidad.codigo else "")
                self.var_nombre.set(entidad.nombre)
                self.var_tipo.set(entidad.tipo)
                
                self.entry_nombre.focus()
                
        except Exception as e:
            mostrar_error(f"Error al cargar entidad:\n{str(e)}")
    
    def guardar_entidad(self):
        """Guarda o actualiza una entidad"""
        # Validar campos
        if not validar_campo_vacio(self.var_nombre.get(), "Nombre"):
            return
        
        codigo = self.var_codigo.get().strip().upper() if self.var_codigo.get().strip() else None
        nombre = self.var_nombre.get().strip()
        tipo = self.var_tipo.get()
        
        try:
            id_entidad = self.var_id.get()
            
            if id_entidad:  # Actualizar
                # Verificar código duplicado si tiene código
                if codigo and ClienteProveedor.existe_codigo(codigo, int(id_entidad)):
                    mostrar_error(f"El código '{codigo}' ya existe")
                    return
                
                ClienteProveedor.actualizar(int(id_entidad), codigo, nombre, tipo)
                mostrar_exito("Registro actualizado correctamente")
                
            else:  # Crear nuevo
                # Generar código automático si está vacío
                if not codigo:
                    from utilis import obtener_fecha_hora_actual
                    prefijo = "CLI" if tipo == "cliente" else "PROV" if tipo == "proveedor" else "AMB"
                    timestamp = obtener_fecha_hora_actual().replace("-", "").replace(" ", "").replace(":", "")
                    codigo = f"{prefijo}-{timestamp}"
                
                # Verificar código duplicado
                if ClienteProveedor.existe_codigo(codigo):
                    mostrar_error(f"El código '{codigo}' ya existe")
                    return
                
                ClienteProveedor.crear(codigo, nombre, tipo)
                mostrar_exito("Registro creado correctamente")
            
            # Recargar lista y limpiar formulario
            self.cargar_entidades()
            self.limpiar_formulario()
            
        except Exception as e:
            mostrar_error(f"Error al guardar entidad:\n{str(e)}")
    
    def eliminar_entidad(self):
        """Elimina (desactiva) una entidad"""
        if not self.entidad_seleccionada:
            mostrar_error("Seleccione un registro")
            return
        
        if confirmar_accion("Confirmar", "¿Está seguro de eliminar este registro?"):
            try:
                ClienteProveedor.eliminar(self.entidad_seleccionada)
                mostrar_exito("Registro eliminado correctamente")
                self.cargar_entidades()
                self.limpiar_formulario()
                
            except Exception as e:
                mostrar_error(f"Error al eliminar entidad:\n{str(e)}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.var_id.set("")
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_tipo.set(self.tipo_default)
        
        self.btn_eliminar.config(state=tk.DISABLED)
        self.entidad_seleccionada = None
        
        # Limpiar selección en tree
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        self.entry_codigo.focus()