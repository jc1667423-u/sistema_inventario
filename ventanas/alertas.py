"""
Ventana de Productos con Stock Bajo
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from clases.productos import Producto
from constantes import *
from utilis import *
from datetime import datetime

class VentanaStockBajo:
    """Ventana para ver productos con stock bajo"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Productos con Stock Bajo")
        self.ventana.geometry("1200x700")
        centrar_ventana(self.ventana, 1200, 700)
        
        self.crear_interfaz()
        self.cargar_productos()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana"""
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_ADVERTENCIA, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="⚠️ Productos con Stock Bajo",
            font=("Arial", 18, "bold"),
            bg=COLOR_ADVERTENCIA,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sección de filtro
        self.crear_seccion_filtro(frame_contenedor)
        
        # Sección de lista
        self.crear_seccion_lista(frame_contenedor)
        
        # Sección de estadísticas
        self.crear_seccion_estadisticas(frame_contenedor)
    
    def crear_seccion_filtro(self, parent):
        """Crea la sección de filtro"""
        frame_filtro = tk.LabelFrame(
            parent,
            text="Configuración",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_filtro.pack(fill=tk.X, pady=(0, 10))
        
        frame_interno = tk.Frame(frame_filtro, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            frame_interno,
            text="Stock mínimo:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.var_limite = tk.StringVar(value="10")
        spinbox = ttk.Spinbox(
            frame_interno,
            from_=1,
            to=100,
            textvariable=self.var_limite,
            font=("Arial", 10),
            width=10
        )
        spinbox.pack(side=tk.LEFT, padx=(0, 20))
        
        btn_filtrar = tk.Button(
            frame_interno,
            text="🔍 Buscar",
            font=("Arial", 10, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_productos
        )
        btn_filtrar.pack(side=tk.LEFT, padx=5)
        
        btn_actualizar = tk.Button(
            frame_interno,
            text="↻ Actualizar",
            font=("Arial", 10, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_productos
        )
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        btn_exportar = tk.Button(
            frame_interno,
            text="📥 Exportar a Excel",
            font=("Arial", 10, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.exportar_excel
        )
        btn_exportar.pack(side=tk.LEFT, padx=5)
    
    def crear_seccion_lista(self, parent):
        """Crea la sección de lista"""
        frame_lista = tk.LabelFrame(
            parent,
            text="Productos con Stock Bajo",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame para el treeview
        frame_tree = tk.Frame(frame_lista, bg=COLOR_BLANCO)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL)
        
        # Treeview
        columnas = ('ID', 'Código', 'Descripción', 'Unidad', 'Stock Actual', 'Precio', 'Valor Total', 'Estado')
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
        anchos = [50, 100, 350, 80, 100, 100, 120, 80]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            align = 'center' if col != 'Descripción' else 'w'
            self.tree.column(col, width=ancho, anchor=align)
        
        # Colocar widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Sin colores de fondo para mejor compatibilidad con tema oscuro
    
    def crear_seccion_estadisticas(self, parent):
        """Crea la sección de estadísticas"""
        frame_stats = tk.LabelFrame(
            parent,
            text="Resumen",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_stats.pack(fill=tk.X)
        
        frame_interno = tk.Frame(frame_stats, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        # Variables
        self.var_total_productos = tk.StringVar(value="0")
        self.var_stock_critico = tk.StringVar(value="0")
        self.var_valor_total = tk.StringVar(value="S/ 0.00")
        
        # Tarjetas
        self.crear_tarjeta_stat(frame_interno, "Total Productos", self.var_total_productos, COLOR_SECUNDARIO)
        self.crear_tarjeta_stat(frame_interno, "Stock Crítico (≤3)", self.var_stock_critico, COLOR_PELIGRO)
        self.crear_tarjeta_stat(frame_interno, "Valor Total", self.var_valor_total, COLOR_EXITO)
    
    def crear_tarjeta_stat(self, parent, titulo, variable, color):
        """Crea una tarjeta de estadística"""
        frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            frame,
            text=titulo,
            font=("Arial", 10, "bold"),
            bg=color,
            fg=COLOR_BLANCO
        ).pack(pady=(15, 5))
        
        tk.Label(
            frame,
            textvariable=variable,
            font=("Arial", 16, "bold"),
            bg=color,
            fg=COLOR_BLANCO
        ).pack(pady=(5, 15))
    
    def cargar_productos(self):
        """Carga los productos con stock bajo"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener límite
            limite = int(self.var_limite.get()) if self.var_limite.get() else 10
            
            # Obtener productos
            productos = Producto.obtener_productos_bajo_stock(limite=limite)
            
            # Estadísticas
            total = 0
            critico = 0
            valor_total = 0
            
            # Insertar en tabla
            for prod in productos:
                stock = prod['stock_actual']
                precio = prod['precio']
                valor = stock * precio
                valor_total += valor
                total += 1
                
                # Determinar nivel de criticidad
                if stock <= 3:
                    tag = 'critico'
                    critico += 1
                elif stock <= 5:
                    tag = 'bajo'
                else:
                    tag = 'normal'
                
                estado = "⚠️ CRÍTICO" if stock == 0 else "⚠️ Bajo" if stock <= 5 else "Normal"
                
                valores = (
                    prod['id'],
                    prod['codigo'],
                    prod['descripcion'],
                    prod['unidad_medida'],
                    stock,
                    f"S/ {precio:.2f}",
                    f"S/ {valor:.2f}",
                    estado
                )
                
                self.tree.insert('', tk.END, values=valores, tags=(tag,))
            
            # Actualizar estadísticas
            self.var_total_productos.set(f"{total} productos")
            self.var_stock_critico.set(f"{critico} productos")
            self.var_valor_total.set(f"S/ {valor_total:,.2f}")
            
            if total == 0:
                mostrar_info("No hay productos con stock bajo el límite especificado")
            
        except Exception as e:
            mostrar_error(f"Error al cargar productos:\n{str(e)}")
    
    def exportar_excel(self):
        """Exporta los datos a Excel (CSV)"""
        try:
            # Verificar que hay datos
            if not self.tree.get_children():
                mostrar_advertencia("No hay datos para exportar")
                return
            
            # Preguntar dónde guardar
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"stock_bajo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not archivo:
                return
            
            # Generar CSV
            with open(archivo, 'w', encoding='utf-8-sig') as f:
                # Encabezados
                f.write("Código,Descripción,Unidad,Stock Actual,Precio,Valor Total,Estado\n")
                
                # Datos
                for item in self.tree.get_children():
                    valores = self.tree.item(item)['values']
                    f.write(f"{valores[1]},"
                           f"\"{valores[2]}\","
                           f"{valores[3]},"
                           f"{valores[4]},"
                           f"{valores[5]},"
                           f"{valores[6]},"
                           f"{valores[7]}\n")
                
                # Totales
                f.write(f"\n,,,Total Productos:,{self.var_total_productos.get()}\n")
                f.write(f",,,Stock Crítico:,{self.var_stock_critico.get()}\n")
                f.write(f",,,Valor Total:,{self.var_valor_total.get()}\n")
            
            mostrar_exito(f"Datos exportados correctamente:\n{archivo}")
            
            if confirmar_accion("Abrir archivo", "¿Desea abrir el archivo generado?"):
                import os
                os.startfile(archivo)
            
        except Exception as e:
            mostrar_error(f"Error al exportar:\n{str(e)}")