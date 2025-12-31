"""
Kardex General - Todos los productos con filtros
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from clases.transacciones import Transaccion
from constantes import *
from utilis import *
from datetime import datetime, timedelta

class VentanaKardexGeneral:
    """Ventana para ver kardex general de todos los productos"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Kardex General - Todos los Productos")
        self.ventana.geometry("1500x800")
        centrar_ventana(self.ventana, 1500, 800)
        
        self.crear_interfaz()
        self.cargar_kardex()
    
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
            text="📊 Kardex General - Todos los Productos",
            font=("Arial", 18, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear secciones
        self.crear_seccion_filtros(frame_contenedor)
        self.crear_seccion_kardex(frame_contenedor)
        self.crear_seccion_estadisticas(frame_contenedor)
    
    def crear_seccion_filtros(self, parent):
        """Crea la sección de filtros"""
        frame_filtros = tk.LabelFrame(
            parent,
            text="Filtros de Búsqueda",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_filtros.pack(fill=tk.X, pady=(0, 10))
        
        frame_interno = tk.Frame(frame_filtros, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        # Primera fila - Tipo de movimiento
        frame_fila1 = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_fila1.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_fila1,
            text="Tipo de Movimiento:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.var_tipo = tk.StringVar(value="todos")
        
        tipos = [
            ("Todos", "todos"),
            ("Entradas", "Entrada"),
            ("Salidas", "Salida")
        ]
        
        for texto, valor in tipos:
            rb = ttk.Radiobutton(
                frame_fila1,
                text=texto,
                variable=self.var_tipo,
                value=valor
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Segunda fila - Fechas
        frame_fila2 = tk.Frame(frame_interno, bg=COLOR_BLANCO)
        frame_fila2.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_fila2,
            text="Desde:",
            font=("Arial", 10),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.var_fecha_desde = tk.StringVar(
            value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        )
        entry_desde = ttk.Entry(
            frame_fila2,
            textvariable=self.var_fecha_desde,
            font=("Arial", 10),
            width=12
        )
        entry_desde.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            frame_fila2,
            text="Hasta:",
            font=("Arial", 10),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.var_fecha_hasta = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )
        entry_hasta = ttk.Entry(
            frame_fila2,
            textvariable=self.var_fecha_hasta,
            font=("Arial", 10),
            width=12
        )
        entry_hasta.pack(side=tk.LEFT, padx=(0, 15))
        
        # Botones rápidos de fecha
        tk.Label(
            frame_fila2,
            text="Rápido:",
            font=("Arial", 10),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        btn_hoy = tk.Button(
            frame_fila2,
            text="Hoy",
            font=("Arial", 9),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.filtro_hoy
        )
        btn_hoy.pack(side=tk.LEFT, padx=2)
        
        btn_semana = tk.Button(
            frame_fila2,
            text="Semana",
            font=("Arial", 9),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.filtro_semana
        )
        btn_semana.pack(side=tk.LEFT, padx=2)
        
        btn_mes = tk.Button(
            frame_fila2,
            text="Mes",
            font=("Arial", 9),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.filtro_mes
        )
        btn_mes.pack(side=tk.LEFT, padx=2)
        
        # Botones de acción
        btn_filtrar = tk.Button(
            frame_fila2,
            text="🔍 Aplicar Filtros",
            font=("Arial", 10, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_kardex
        )
        btn_filtrar.pack(side=tk.LEFT, padx=(15, 5))
        
        btn_exportar = tk.Button(
            frame_fila2,
            text="📥 Exportar a Excel",
            font=("Arial", 10, "bold"),
            bg=COLOR_ADVERTENCIA,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.exportar_excel
        )
        btn_exportar.pack(side=tk.LEFT, padx=5)
    
    def crear_seccion_kardex(self, parent):
        """Crea la sección del kardex"""
        frame_kardex = tk.LabelFrame(
            parent,
            text="Movimientos de Inventario",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_kardex.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame para el treeview
        frame_tree = tk.Frame(frame_kardex, bg=COLOR_BLANCO)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL)
        
        # Treeview
        columnas = (
            'ID', 'Fecha', 'Tipo', 'Producto', 'Código',
            'Entrada', 'Salida', 'Costo/Precio', 'Total',
            'Cliente/Proveedor', 'Documento', 'Usuario'
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
        anchos = [50, 140, 70, 220, 100, 70, 70, 90, 90, 150, 100, 120]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            align = 'center' if col not in ['Producto', 'Cliente/Proveedor'] else 'w'
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
            text="Resumen del Período",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_stats.pack(fill=tk.X)
        
        frame_interno = tk.Frame(frame_stats, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        # Variables
        self.var_total_movimientos = tk.StringVar(value="0")
        self.var_total_entradas = tk.StringVar(value="0")
        self.var_total_salidas = tk.StringVar(value="0")
        self.var_valor_entradas = tk.StringVar(value="S/ 0.00")
        self.var_valor_salidas = tk.StringVar(value="S/ 0.00")
        
        # Frame para entradas
        frame_entradas = tk.Frame(frame_interno, bg="#d4edda", relief=tk.RAISED, bd=2)
        frame_entradas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            frame_entradas,
            text="📥 ENTRADAS",
            font=("Arial", 11, "bold"),
            bg="#d4edda"
        ).pack(pady=(10, 5))
        
        tk.Label(
            frame_entradas,
            textvariable=self.var_total_entradas,
            font=("Arial", 16, "bold"),
            bg="#d4edda",
            fg=COLOR_EXITO
        ).pack()
        
        tk.Label(
            frame_entradas,
            textvariable=self.var_valor_entradas,
            font=("Arial", 10),
            bg="#d4edda"
        ).pack(pady=(0, 10))
        
        # Frame para salidas
        frame_salidas = tk.Frame(frame_interno, bg="#f8d7da", relief=tk.RAISED, bd=2)
        frame_salidas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            frame_salidas,
            text="📤 SALIDAS",
            font=("Arial", 11, "bold"),
            bg="#f8d7da"
        ).pack(pady=(10, 5))
        
        tk.Label(
            frame_salidas,
            textvariable=self.var_total_salidas,
            font=("Arial", 16, "bold"),
            bg="#f8d7da",
            fg=COLOR_PELIGRO
        ).pack()
        
        tk.Label(
            frame_salidas,
            textvariable=self.var_valor_salidas,
            font=("Arial", 10),
            bg="#f8d7da"
        ).pack(pady=(0, 10))
        
        # Frame para total
        frame_total = tk.Frame(frame_interno, bg=COLOR_SECUNDARIO, relief=tk.RAISED, bd=2)
        frame_total.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            frame_total,
            text="📋 TOTAL MOVIMIENTOS",
            font=("Arial", 11, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO
        ).pack(pady=(10, 5))
        
        tk.Label(
            frame_total,
            textvariable=self.var_total_movimientos,
            font=("Arial", 16, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO
        ).pack(pady=(0, 10))
    
    def cargar_kardex(self):
        """Carga el kardex con los filtros aplicados"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener filtros
            tipo = self.var_tipo.get()
            fecha_desde = self.var_fecha_desde.get()
            fecha_hasta = self.var_fecha_hasta.get()
            
            # Obtener movimientos
            movimientos = Transaccion.obtener_por_fecha(fecha_desde, fecha_hasta)
            
            # Filtrar por tipo si es necesario
            if tipo != "todos":
                movimientos = [m for m in movimientos if m['tipo_movimiento'] == tipo]
            
            # Estadísticas
            total_movimientos = 0
            total_entradas = 0
            total_salidas = 0
            valor_entradas = 0
            valor_salidas = 0
            
            # Insertar en tabla
            for mov in movimientos:
                tipo_mov = mov['tipo_movimiento']
                
                if tipo_mov == 'Entrada':
                    cantidad_entrada = mov['cantidad_entrada']
                    cantidad_salida = '-'
                    total = mov['valor_entrada']
                    valor_entradas += total
                    total_entradas += 1
                    tag = 'entrada'
                else:  # Salida
                    cantidad_entrada = '-'
                    cantidad_salida = mov['cantidad_salida']
                    total = mov['valor_salida']
                    valor_salidas += total
                    total_salidas += 1
                    tag = 'salida'
                
                total_movimientos += 1
                
                valores = (
                    mov['id'],
                    formatear_fecha_hora(mov['fecha']),
                    tipo_mov,
                    mov['producto_descripcion'][:40],
                    mov['producto_codigo'],
                    cantidad_entrada,
                    cantidad_salida,
                    f"S/ {mov['costo']:.2f}",
                    f"S/ {total:.2f}",
                    mov['entidad_nombre'] if mov['entidad_nombre'] else '-',
                    mov['documento'] if mov['documento'] else '-',
                    mov['usuario_nombre']
                )
                
                self.tree.insert('', tk.END, values=valores, tags=(tag,))
            
            # Actualizar estadísticas
            self.var_total_movimientos.set(f"{total_movimientos}")
            self.var_total_entradas.set(f"{total_entradas} movimientos")
            self.var_total_salidas.set(f"{total_salidas} movimientos")
            self.var_valor_entradas.set(f"S/ {valor_entradas:,.2f}")
            self.var_valor_salidas.set(f"S/ {valor_salidas:,.2f}")
            
            if total_movimientos == 0:
                mostrar_info("No se encontraron movimientos con los filtros seleccionados")
            
        except Exception as e:
            mostrar_error(f"Error al cargar kardex:\n{str(e)}")
    
    def filtro_hoy(self):
        """Filtra movimientos de hoy"""
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.var_fecha_desde.set(hoy)
        self.var_fecha_hasta.set(hoy)
        self.cargar_kardex()
    
    def filtro_semana(self):
        """Filtra movimientos de esta semana"""
        hoy = datetime.now()
        inicio = hoy - timedelta(days=hoy.weekday())
        self.var_fecha_desde.set(inicio.strftime("%Y-%m-%d"))
        self.var_fecha_hasta.set(hoy.strftime("%Y-%m-%d"))
        self.cargar_kardex()
    
    def filtro_mes(self):
        """Filtra movimientos de este mes"""
        hoy = datetime.now()
        inicio = hoy.replace(day=1)
        self.var_fecha_desde.set(inicio.strftime("%Y-%m-%d"))
        self.var_fecha_hasta.set(hoy.strftime("%Y-%m-%d"))
        self.cargar_kardex()
    
    def exportar_excel(self):
        """Exporta el kardex a Excel (CSV)"""
        try:
            # Verificar que hay datos
            if not self.tree.get_children():
                mostrar_advertencia("No hay datos para exportar")
                return
            
            # Preguntar dónde guardar
            fecha_desde = self.var_fecha_desde.get()
            fecha_hasta = self.var_fecha_hasta.get()
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"kardex_general_{fecha_desde}_a_{fecha_hasta}.csv"
            )
            
            if not archivo:
                return
            
            # Generar CSV
            with open(archivo, 'w', encoding='utf-8-sig') as f:
                # Encabezado
                f.write(f"KARDEX GENERAL DE INVENTARIO\n")
                f.write(f"Período: {formatear_fecha(fecha_desde)} al {formatear_fecha(fecha_hasta)}\n")
                f.write(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Usuario: {self.usuario.nombre_completo}\n\n")
                
                # Columnas
                f.write("Fecha,Tipo,Producto,Código,Entrada,Salida,Costo/Precio,Total,Cliente/Proveedor,Documento,Usuario\n")
                
                # Datos
                for item in self.tree.get_children():
                    valores = self.tree.item(item)['values']
                    f.write(f"{valores[1]},"
                           f"{valores[2]},"
                           f"\"{valores[3]}\","
                           f"{valores[4]},"
                           f"{valores[5]},"
                           f"{valores[6]},"
                           f"{valores[7]},"
                           f"{valores[8]},"
                           f"\"{valores[9]}\","
                           f"{valores[10]},"
                           f"\"{valores[11]}\"\n")
                
                # Resumen
                f.write(f"\n\nRESUMEN DEL PERÍODO\n")
                f.write(f"Total Movimientos:,{self.var_total_movimientos.get()}\n")
                f.write(f"Total Entradas:,{self.var_total_entradas.get()}\n")
                f.write(f"Total Salidas:,{self.var_total_salidas.get()}\n")
                f.write(f"Valor Total Entradas:,{self.var_valor_entradas.get()}\n")
                f.write(f"Valor Total Salidas:,{self.var_valor_salidas.get()}\n")
            
            mostrar_exito(f"Kardex exportado correctamente:\n{archivo}")
            
            if confirmar_accion("Abrir archivo", "¿Desea abrir el archivo generado?"):
                import os
                os.startfile(archivo)
            
        except Exception as e:
            mostrar_error(f"Error al exportar:\n{str(e)}")