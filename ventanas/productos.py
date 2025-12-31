"""
Ventana de Gestión de Productos
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from clases.productos import Producto
from constantes import *
from utilis import (
    centrar_ventana, validar_campo_vacio, formatear_moneda,
    configurar_validacion_decimal, mostrar_exito, mostrar_error,
    confirmar_accion, validar_numero
)

class VentanaProductos:
    """Ventana para gestionar productos"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Productos")
        self.ventana.geometry("1200x700")
        centrar_ventana(self.ventana, 1200, 700)
        
        self.producto_seleccionado = None
        
        self.crear_interfaz()
        self.cargar_productos()
    
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
            text="📦 Gestión de Productos",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor (dividido en dos columnas)
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Columna izquierda - Lista de productos
        frame_izquierdo = tk.Frame(frame_contenedor, bg=COLOR_FONDO)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha - Formulario
        frame_derecho = tk.Frame(frame_contenedor, bg=COLOR_FONDO, width=400)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        frame_derecho.pack_propagate(False)
        
        # Crear secciones
        self.crear_seccion_busqueda(frame_izquierdo)
        self.crear_seccion_lista(frame_izquierdo)
        self.crear_seccion_formulario(frame_derecho)
    
    def crear_seccion_busqueda(self, parent):
        """Crea la sección de búsqueda"""
        frame_busqueda = tk.LabelFrame(
            parent,
            text="Búsqueda",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_busqueda.pack(fill=tk.X, pady=(0, 10))
        
        frame_interno = tk.Frame(frame_busqueda, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace('w', lambda *args: self.buscar_productos())
        
        label_buscar = tk.Label(
            frame_interno,
            text="🔍 Buscar:",
            font=("Arial", 10),
            bg=COLOR_BLANCO
        )
        label_buscar.pack(side=tk.LEFT, padx=(0, 10))
        
        entry_buscar = ttk.Entry(
            frame_interno,
            textvariable=self.var_busqueda,
            font=("Arial", 10),
            width=50
        )
        entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Botón actualizar
        btn_actualizar = tk.Button(
            frame_interno,
            text="↻",
            font=("Arial", 12, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_productos,
            width=3
        )
        btn_actualizar.pack(side=tk.LEFT, padx=(10, 0))
    
    def crear_seccion_lista(self, parent):
        """Crea la sección de lista de productos"""
        frame_lista = tk.LabelFrame(
            parent,
            text="Lista de Productos",
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
        columnas = ('ID', 'Código', 'Descripción', 'Unidad', 'Precio', 'Stock', 'Estado')
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
        anchos = [50, 100, 300, 80, 100, 80, 80]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor='center' if col != 'Descripción' else 'w')
        
        # Colocar widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.on_seleccionar_producto)
        
        # Doble clic para editar
        self.tree.bind('<Double-1>', lambda e: self.cargar_producto_seleccionado())
    
    def crear_seccion_formulario(self, parent):
        """Crea la sección del formulario"""
        frame_form = tk.LabelFrame(
            parent,
            text="Datos del Producto",
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
        self.var_descripcion = tk.StringVar()
        self.var_unidad = tk.StringVar()
        self.var_precio = tk.StringVar(value="0")
        self.var_stock_minimo = tk.StringVar(value="10")
        
        # Campo ID (oculto)
        self.var_id.set("")
        
        # Código
        tk.Label(
            frame_interno,
            text="Código *",
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
        
        # Descripción
        tk.Label(
            frame_interno,
            text="Descripción *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_descripcion = ttk.Entry(
            frame_interno,
            textvariable=self.var_descripcion,
            font=("Arial", 10)
        )
        self.entry_descripcion.pack(fill=tk.X, ipady=5)
        
        # Unidad de medida
        tk.Label(
            frame_interno,
            text="Unidad de Medida *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.combo_unidad = ttk.Combobox(
            frame_interno,
            textvariable=self.var_unidad,
            values=UNIDADES_MEDIDA,
            state='readonly',
            font=("Arial", 10)
        )
        self.combo_unidad.pack(fill=tk.X, ipady=5)
        
        # Precio
        tk.Label(
            frame_interno,
            text="Precio (S/) *",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_precio = ttk.Entry(
            frame_interno,
            textvariable=self.var_precio,
            font=("Arial", 10)
        )
        self.entry_precio.pack(fill=tk.X, ipady=5)
        configurar_validacion_decimal(self.entry_precio)
        
        # Stock mínimo para alertas
        tk.Label(
            frame_interno,
            text="Stock Mínimo (Alertas)",
            font=("Arial", 9, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X, pady=(15, 2))
        
        self.entry_stock_minimo = ttk.Entry(
            frame_interno,
            textvariable=self.var_stock_minimo,
            font=("Arial", 10)
        )
        self.entry_stock_minimo.pack(fill=tk.X, ipady=5)
        configurar_validacion_decimal(self.entry_stock_minimo)
        
        tk.Label(
            frame_interno,
            text="Se alertará cuando stock ≤ este valor",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).pack(fill=tk.X, pady=(2, 0))
        
        # Nota
        label_nota = tk.Label(
            frame_interno,
            text="* Campos obligatorios\n\nNota: El stock se establece\n en 'Nueva Entrada' (Movimientos).\nEl stock mínimo define cuándo\nse generan alertas.",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            justify='left'
        )
        label_nota.pack(fill=tk.X, pady=(20, 20))
        
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
            command=self.guardar_producto
        )
        self.btn_guardar.pack(fill=tk.X, ipady=8, pady=5)
        
        self.btn_actualizar_precio = tk.Button(
            frame_botones,
            text="💰 Actualizar Precio",
            font=("Arial", 10, "bold"),
            bg=COLOR_ADVERTENCIA,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.actualizar_precio_producto,
            state=tk.DISABLED
        )
        self.btn_actualizar_precio.pack(fill=tk.X, ipady=8, pady=5)
        
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
            command=self.eliminar_producto,
            state=tk.DISABLED
        )
        self.btn_eliminar.pack(fill=tk.X, ipady=8, pady=5)
    
    def cargar_productos(self):
        """Carga todos los productos en la tabla"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            productos = Producto.obtener_todos()
            
            for producto in productos:
                estado = "Activo" if producto['activo'] == 1 else "Inactivo"
                valores = (
                    producto['id'],
                    producto['codigo'],
                    producto['descripcion'],
                    producto['unidad_medida'],
                    f"S/ {producto['precio']:.2f}",
                    producto['stock_actual'],
                    estado
                )
                self.tree.insert('', tk.END, values=valores)
            
        except Exception as e:
            mostrar_error(f"Error al cargar productos:\n{str(e)}")
    
    def buscar_productos(self):
        """Busca productos según el término ingresado"""
        termino = self.var_busqueda.get().strip()
        
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if termino:
                productos = Producto.buscar(termino)
            else:
                productos = Producto.obtener_todos()
            
            for producto in productos:
                estado = "Activo" if producto['activo'] == 1 else "Inactivo"
                valores = (
                    producto['id'],
                    producto['codigo'],
                    producto['descripcion'],
                    producto['unidad_medida'],
                    f"S/ {producto['precio']:.2f}",
                    producto['stock_actual'],
                    estado
                )
                self.tree.insert('', tk.END, values=valores)
                
        except Exception as e:
            mostrar_error(f"Error al buscar productos:\n{str(e)}")
    
    def on_seleccionar_producto(self, event):
        """Evento cuando se selecciona un producto"""
        seleccion = self.tree.selection()
        if seleccion:
            self.btn_eliminar.config(state=tk.NORMAL)
            self.btn_actualizar_precio.config(state=tk.NORMAL)
            valores = self.tree.item(seleccion[0])['values']
            self.producto_seleccionado = valores[0]
        else:
            self.btn_eliminar.config(state=tk.DISABLED)
            self.btn_actualizar_precio.config(state=tk.DISABLED)
            self.producto_seleccionado = None
    
    def cargar_producto_seleccionado(self):
        """Carga los datos del producto seleccionado en el formulario"""
        if not self.producto_seleccionado:
            return
        
        try:
            producto = Producto.obtener_por_id(self.producto_seleccionado)
            
            if producto:
                self.var_id.set(producto.id)
                self.var_codigo.set(producto.codigo)
                self.var_descripcion.set(producto.descripcion)
                self.var_unidad.set(producto.unidad_medida)
                self.var_precio.set(str(producto.precio))
                self.var_stock_minimo.set(str(producto.stock_minimo))
                
                self.entry_codigo.focus()
                
        except Exception as e:
            mostrar_error(f"Error al cargar producto:\n{str(e)}")
    
    def guardar_producto(self):
        """Guarda o actualiza un producto"""
        if not validar_campo_vacio(self.var_codigo.get(), "Código"):
            return
        if not validar_campo_vacio(self.var_descripcion.get(), "Descripción"):
            return
        if not validar_campo_vacio(self.var_unidad.get(), "Unidad de Medida"):
            return
        
        codigo = self.var_codigo.get().strip().upper()
        descripcion = self.var_descripcion.get().strip()
        unidad = self.var_unidad.get()
        precio = float(self.var_precio.get()) if self.var_precio.get() else 0
        stock_minimo = int(self.var_stock_minimo.get()) if self.var_stock_minimo.get() else 10
        
        try:
            id_producto = self.var_id.get()
            
            if id_producto:
                # Actualizar producto existente (ahora incluye precio)
                if Producto.existe_codigo(codigo, int(id_producto)):
                    mostrar_error(f"El código '{codigo}' ya existe")
                    return
                
                Producto.actualizar(int(id_producto), codigo, descripcion, unidad, stock_minimo)
                Producto.actualizar_precio(int(id_producto), precio)
                mostrar_exito("Producto actualizado correctamente")
                
            else:
                # Crear nuevo producto con precio inicial
                if Producto.existe_codigo(codigo):
                    mostrar_error(f"El código '{codigo}' ya existe")
                    return
                
                # Crear producto con precio y stock en 0
                Producto.crear(codigo, descripcion, unidad, precio=precio, stock_actual=0, stock_minimo=stock_minimo)
                
                # Mostrar alerta especial al crear producto
                messagebox.showinfo(
                    "✅ Producto Creado",
                    f"Producto '{descripcion}' creado exitosamente.\n\n"
                    f"Precio: S/ {precio:.2f}\n\n"
                    "⚠️ Recuerda:\n"
                    "• Ir a 'Nueva Entrada' para agregar stock"
                )
            
            self.cargar_productos()
            self.limpiar_formulario()
            
        except Exception as e:
            mostrar_error(f"Error al guardar producto:\n{str(e)}")
    
    def eliminar_producto(self):
        """Elimina (desactiva) un producto"""
        if not self.producto_seleccionado:
            mostrar_error("Seleccione un producto")
            return
        
        if confirmar_accion("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                Producto.eliminar(self.producto_seleccionado)
                mostrar_exito("Producto eliminado correctamente")
                self.cargar_productos()
                self.limpiar_formulario()
                
            except Exception as e:
                mostrar_error(f"Error al eliminar producto:\n{str(e)}")
    
    def actualizar_precio_producto(self):
        """Actualiza el precio de un producto"""
        if not self.producto_seleccionado:
            mostrar_error("Seleccione un producto")
            return
        
        try:
            producto = Producto.obtener_por_id(self.producto_seleccionado)
            
            if not producto:
                mostrar_error("Producto no encontrado")
                return
            
            # Solicitar nuevo precio
            nuevo_precio = simpledialog.askfloat(
                "💰 Actualizar Precio",
                f"Producto: {producto.descripcion}\n"
                f"Precio actual: S/ {producto.precio:.2f}\n\n"
                f"Ingrese el nuevo precio:",
                minvalue=0.01,
                parent=self.ventana
            )
            
            if nuevo_precio is not None:
                Producto.actualizar_precio(self.producto_seleccionado, nuevo_precio)
                mostrar_exito(f"Precio actualizado a S/ {nuevo_precio:.2f}")
                self.cargar_productos()
                self.limpiar_formulario()
                
        except Exception as e:
            mostrar_error(f"Error al actualizar precio:\n{str(e)}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.var_id.set("")
        self.var_codigo.set("")
        self.var_descripcion.set("")
        self.var_unidad.set("")
        self.var_precio.set("0")
        self.var_stock_minimo.set("10")
        
        self.btn_eliminar.config(state=tk.DISABLED)
        self.btn_actualizar_precio.config(state=tk.DISABLED)
        self.producto_seleccionado = None
        
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        self.entry_codigo.focus()