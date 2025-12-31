"""
Ventana de Kardex - Historial de movimientos por producto
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.transacciones import Transaccion
from clases.productos import Producto
from constantes import *
from utilis import *

class VentanaKardex:
    """Ventana para ver el kardex de un producto"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Kardex - Historial por Producto")
        self.ventana.geometry("1400x800")
        centrar_ventana(self.ventana, 1400, 800)
        
        self.producto_actual = None
        
        self.crear_interfaz()
        self.cargar_productos()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana"""
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_SECUNDARIO, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="📊 Kardex - Historial por Producto",
            font=("Arial", 18, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear secciones
        self.crear_seccion_seleccion(frame_contenedor)
        self.crear_seccion_info_producto(frame_contenedor)
        self.crear_seccion_kardex(frame_contenedor)
    
    def crear_seccion_seleccion(self, parent):
        """Crea la sección de selección de producto"""
        frame_seleccion = tk.LabelFrame(
            parent,
            text="Seleccionar Producto",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_seleccion.pack(fill=tk.X, pady=(0, 10))
        
        frame_interno = tk.Frame(frame_seleccion, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            frame_interno,
            text="Producto:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.var_producto = tk.StringVar()
        self.combo_producto = ttk.Combobox(
            frame_interno,
            textvariable=self.var_producto,
            font=("Arial", 10),
            state='readonly',
            width=60
        )
        self.combo_producto.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_ver = tk.Button(
            frame_interno,
            text="👁️ Ver Kardex",
            font=("Arial", 10, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_kardex
        )
        btn_ver.pack(side=tk.LEFT)
    
    def crear_seccion_info_producto(self, parent):
        """Crea la sección de información del producto"""
        frame_info = tk.LabelFrame(
            parent,
            text="Información del Producto",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_info.pack(fill=tk.X, pady=(0, 10))
        
        frame_interno = tk.Frame(frame_info, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        # Variables de info
        self.var_codigo = tk.StringVar(value="-")
        self.var_descripcion = tk.StringVar(value="-")
        self.var_unidad = tk.StringVar(value="-")
        self.var_precio = tk.StringVar(value="-")
        self.var_stock_actual = tk.StringVar(value="-")
        
        # Grid de información
        labels = [
            ("Código:", self.var_codigo),
            ("Descripción:", self.var_descripcion),
            ("Unidad:", self.var_unidad),
            ("Precio:", self.var_precio),
            ("Stock Actual:", self.var_stock_actual)
        ]
        
        for i, (texto, var) in enumerate(labels):
            tk.Label(
                frame_interno,
                text=texto,
                font=("Arial", 9, "bold"),
                bg=COLOR_BLANCO
            ).grid(row=i//3, column=(i%3)*2, sticky='e', padx=(5, 5), pady=5)
            
            tk.Label(
                frame_interno,
                textvariable=var,
                font=("Arial", 9),
                bg=COLOR_BLANCO
            ).grid(row=i//3, column=(i%3)*2+1, sticky='w', padx=(0, 20), pady=5)
    
    def crear_seccion_kardex(self, parent):
        """Crea la sección del kardex"""
        frame_kardex = tk.LabelFrame(
            parent,
            text="Movimientos del Producto",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_kardex.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el treeview
        frame_tree = tk.Frame(frame_kardex, bg=COLOR_BLANCO)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL)
        
        # Treeview
        columnas = (
            'ID', 'Fecha', 'Tipo', 'Entrada', 'Salida', 'Saldo',
            'Costo/Precio', 'Total', 'Cliente/Proveedor', 'Documento', 'Concepto'
        )
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
        anchos = [50, 140, 70, 70, 70, 70, 90, 90, 150, 100, 200]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            align = 'center' if col not in ['Cliente/Proveedor', 'Concepto'] else 'w'
            self.tree.column(col, width=ancho, anchor=align)
        
        # Colocar widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Sin colores de fondo para mejor compatibilidad con tema oscuro
    
    def cargar_productos(self):
        """Carga los productos en el combobox"""
        try:
            productos = Producto.obtener_todos()
            self.productos_dict = {}
            valores = []
            
            for prod in productos:
                texto = f"{prod['codigo']} - {prod['descripcion']}"
                valores.append(texto)
                self.productos_dict[texto] = prod
            
            self.combo_producto['values'] = valores
            
        except Exception as e:
            mostrar_error(f"Error al cargar productos:\n{str(e)}")
    
    def cargar_kardex(self):
        """Carga el kardex del producto seleccionado"""
        if not self.var_producto.get():
            mostrar_error("Seleccione un producto")
            return
        
        try:
            # Obtener producto
            producto_data = self.productos_dict[self.var_producto.get()]
            self.producto_actual = producto_data
            
            # Actualizar información
            self.var_codigo.set(producto_data['codigo'])
            self.var_descripcion.set(producto_data['descripcion'])
            self.var_unidad.set(producto_data['unidad_medida'])
            self.var_precio.set(f"S/ {producto_data['precio']:.2f}")
            self.var_stock_actual.set(f"{producto_data['stock_actual']} unidades")
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener movimientos
            movimientos = Transaccion.obtener_por_producto(producto_data['id'], limite=500)
            
            # Calcular saldos
            saldo = 0
            
            # Fila de saldo inicial (opcional)
            # self.tree.insert('', tk.END, values=(
            #     '-', 'SALDO INICIAL', '-', '-', '-', saldo, '-', '-', '-', '-', '-'
            # ), tags=('saldo_inicial',))
            
            for mov in movimientos:
                tipo = mov['tipo_movimiento']
                
                if tipo == 'Entrada':
                    entrada = mov['cantidad_entrada']
                    salida = '-'
                    saldo += entrada
                    costo_precio = mov['costo']
                    total = mov['valor_entrada']
                    tag = 'entrada'
                else:  # Salida
                    entrada = '-'
                    salida = mov['cantidad_salida']
                    saldo -= salida
                    costo_precio = mov['costo']
                    total = mov['valor_salida']
                    tag = 'salida'
                
                valores = (
                    mov['id'],
                    formatear_fecha_hora(mov['fecha']),
                    tipo,
                    entrada if entrada != '-' else '-',
                    salida if salida != '-' else '-',
                    saldo,
                    f"S/ {costo_precio:.2f}",
                    f"S/ {total:.2f}",
                    mov['entidad_nombre'] if mov['entidad_nombre'] else '-',
                    mov['documento'] if mov['documento'] else '-',
                    mov['concepto'] if mov['concepto'] else '-'
                )
                
                self.tree.insert('', tk.END, values=valores, tags=(tag,))
            
            # Verificar que el saldo coincida con el stock actual
            if saldo != producto_data['stock_actual']:
                mostrar_advertencia(
                    f"Advertencia: El saldo calculado ({saldo}) "
                    f"no coincide con el stock actual ({producto_data['stock_actual']})"
                )
            
        except Exception as e:
            mostrar_error(f"Error al cargar kardex:\n{str(e)}")