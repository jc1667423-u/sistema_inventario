"""
Ventana para ver todos los movimientos/transacciones
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.transacciones import Transaccion
from constantes import *
from utilis import *
from datetime import datetime, timedelta

class VentanaMovimientos:
    """Ventana para visualizar todos los movimientos"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Ver Movimientos")
        self.ventana.geometry("1400x800")
        centrar_ventana(self.ventana, 1400, 800)
        
        self.transaccion_seleccionada = None
        
        self.crear_interfaz()
        self.cargar_movimientos()
    
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
            text="📋 Historial de Movimientos",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Frame contenedor
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear secciones
        self.crear_seccion_filtros(frame_contenedor)
        self.crear_seccion_lista(frame_contenedor)
        self.crear_seccion_estadisticas(frame_contenedor)
    
    def crear_seccion_filtros(self, parent):
        """Crea la sección de filtros"""
        frame_filtros = tk.LabelFrame(
            parent,
            text="Filtros",
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
            text="Tipo:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.var_filtro_tipo = tk.StringVar(value="todos")
        
        tipos = [
            ("Todos", "todos"),
            ("Entradas", "Entrada"),
            ("Salidas", "Salida")
        ]
        
        for texto, valor in tipos:
            rb = ttk.Radiobutton(
                frame_fila1,
                text=texto,
                variable=self.var_filtro_tipo,
                value=valor,
                command=self.aplicar_filtros
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
        
        # Botones de fecha rápida
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
            text="Esta semana",
            font=("Arial", 9),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.filtro_semana
        )
        btn_semana.pack(side=tk.LEFT, padx=2)
        
        btn_mes = tk.Button(
            frame_fila2,
            text="Este mes",
            font=("Arial", 9),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.filtro_mes
        )
        btn_mes.pack(side=tk.LEFT, padx=2)
        
        # Botón aplicar filtros
        btn_filtrar = tk.Button(
            frame_fila2,
            text="🔍 Filtrar",
            font=("Arial", 10, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.aplicar_filtros
        )
        btn_filtrar.pack(side=tk.LEFT, padx=(15, 0))
        
        # Botón actualizar
        btn_actualizar = tk.Button(
            frame_fila2,
            text="↻",
            font=("Arial", 12, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cargar_movimientos,
            width=3
        )
        btn_actualizar.pack(side=tk.LEFT, padx=(5, 0))
    
    def crear_seccion_lista(self, parent):
        """Crea la sección de lista de movimientos"""
        frame_lista = tk.LabelFrame(
            parent,
            text="Lista de Movimientos",
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
        columnas = (
            'ID', 'Fecha', 'Tipo', 'Producto', 'Cantidad',
            'Costo/Precio', 'Total', 'Cliente/Proveedor', 'Documento', 'Usuario'
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
        anchos = [50, 90, 70, 250, 70, 80, 90, 150, 100, 120]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            align = 'center' if col not in ['Producto', 'Cliente/Proveedor'] else 'w'
            self.tree.column(col, width=ancho, anchor=align)
        
        # Colocar widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Sin colores de fondo para mejor compatibilidad con tema oscuro
        
        # Eventos
        self.tree.bind('<<TreeviewSelect>>', self.on_seleccionar_movimiento)
        self.tree.bind('<Double-1>', lambda e: self.ver_detalle())
        
        # Frame para botones
        frame_botones = tk.Frame(frame_lista, bg=COLOR_BLANCO)
        frame_botones.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        btn_detalle = tk.Button(
            frame_botones,
            text="👁️ Ver Detalle",
            font=("Arial", 10, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.ver_detalle,
            state=tk.DISABLED
        )
        btn_detalle.pack(side=tk.LEFT, padx=5)
        self.btn_detalle = btn_detalle
        
        # Solo admin puede eliminar
        if self.usuario.tiene_permiso('transacciones', 'eliminar'):
            btn_eliminar = tk.Button(
                frame_botones,
                text="🗑️ Eliminar",
                font=("Arial", 10, "bold"),
                bg=COLOR_PELIGRO,
                fg=COLOR_BLANCO,
                cursor="hand2",
                command=self.eliminar_movimiento,
                state=tk.DISABLED
            )
            btn_eliminar.pack(side=tk.LEFT, padx=5)
            self.btn_eliminar = btn_eliminar
    
    def crear_seccion_estadisticas(self, parent):
        """Crea la sección de estadísticas"""
        frame_stats = tk.LabelFrame(
            parent,
            text="Estadísticas",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_PRIMARIO
        )
        frame_stats.pack(fill=tk.X)
        
        frame_interno = tk.Frame(frame_stats, bg=COLOR_BLANCO)
        frame_interno.pack(fill=tk.X, padx=15, pady=15)
        
        # Variables de estadísticas
        self.var_total_entradas = tk.StringVar(value="0")
        self.var_total_salidas = tk.StringVar(value="0")
        self.var_valor_entradas = tk.StringVar(value="S/ 0.00")
        self.var_valor_salidas = tk.StringVar(value="S/ 0.00")
        
        # Entradas
        frame_entradas = tk.Frame(frame_interno, bg="#d4edda", relief=tk.RAISED, bd=1)
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
        
        # Salidas
        frame_salidas = tk.Frame(frame_interno, bg="#f8d7da", relief=tk.RAISED, bd=1)
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
    
    def cargar_movimientos(self):
        """Carga todos los movimientos"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener movimientos
            movimientos = Transaccion.obtener_todas(limite=500)
            
            # Estadísticas
            total_entradas = 0
            total_salidas = 0
            valor_entradas = 0
            valor_salidas = 0
            
            # Insertar en tabla
            for mov in movimientos:
                tipo = mov['tipo_movimiento']
                cantidad = mov['cantidad_entrada'] if tipo == 'Entrada' else mov['cantidad_salida']
                costo_precio = mov['costo'] if tipo == 'Entrada' else mov['costo']
                total = mov['valor_entrada'] if tipo == 'Entrada' else mov['valor_salida']
                
                valores = (
                    mov['id'],
                    formatear_fecha_hora(mov['fecha']),
                    tipo,
                    f"{mov['producto_codigo']} - {mov['producto_descripcion'][:40]}",
                    cantidad,
                    f"S/ {costo_precio:.2f}",
                    f"S/ {total:.2f}",
                    mov['entidad_nombre'] if mov['entidad_nombre'] else '-',
                    mov['documento'] if mov['documento'] else '-',
                    mov['usuario_nombre']
                )
                
                tag = 'entrada' if tipo == 'Entrada' else 'salida'
                self.tree.insert('', tk.END, values=valores, tags=(tag,))
                
                # Actualizar estadísticas
                if tipo == 'Entrada':
                    total_entradas += 1
                    valor_entradas += total
                else:
                    total_salidas += 1
                    valor_salidas += total
            
            # Actualizar labels de estadísticas
            self.var_total_entradas.set(f"{total_entradas} movimientos")
            self.var_total_salidas.set(f"{total_salidas} movimientos")
            self.var_valor_entradas.set(f"S/ {valor_entradas:,.2f}")
            self.var_valor_salidas.set(f"S/ {valor_salidas:,.2f}")
            
        except Exception as e:
            mostrar_error(f"Error al cargar movimientos:\n{str(e)}")
    
    def aplicar_filtros(self):
        """Aplica los filtros seleccionados"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener filtros
            tipo = self.var_filtro_tipo.get()
            fecha_desde = self.var_fecha_desde.get()
            fecha_hasta = self.var_fecha_hasta.get()
            
            # Obtener movimientos filtrados
            if tipo == "todos":
                movimientos = Transaccion.obtener_por_fecha(fecha_desde, fecha_hasta)
            else:
                # Primero filtrar por fecha, luego por tipo
                movimientos = Transaccion.obtener_por_fecha(fecha_desde, fecha_hasta)
                movimientos = [m for m in movimientos if m['tipo_movimiento'] == tipo]
            
            # Estadísticas
            total_entradas = 0
            total_salidas = 0
            valor_entradas = 0
            valor_salidas = 0
            
            # Insertar en tabla
            for mov in movimientos:
                tipo_mov = mov['tipo_movimiento']
                cantidad = mov['cantidad_entrada'] if tipo_mov == 'Entrada' else mov['cantidad_salida']
                costo_precio = mov['costo']
                total = mov['valor_entrada'] if tipo_mov == 'Entrada' else mov['valor_salida']
                
                valores = (
                    mov['id'],
                    formatear_fecha_hora(mov['fecha']),
                    tipo_mov,
                    f"{mov['producto_codigo']} - {mov['producto_descripcion'][:40]}",
                    cantidad,
                    f"S/ {costo_precio:.2f}",
                    f"S/ {total:.2f}",
                    mov['entidad_nombre'] if mov['entidad_nombre'] else '-',
                    mov['documento'] if mov['documento'] else '-',
                    mov['usuario_nombre']
                )
                
                tag = 'entrada' if tipo_mov == 'Entrada' else 'salida'
                self.tree.insert('', tk.END, values=valores, tags=(tag,))
                
                # Actualizar estadísticas
                if tipo_mov == 'Entrada':
                    total_entradas += 1
                    valor_entradas += total
                else:
                    total_salidas += 1
                    valor_salidas += total
            
            # Actualizar labels de estadísticas
            self.var_total_entradas.set(f"{total_entradas} movimientos")
            self.var_total_salidas.set(f"{total_salidas} movimientos")
            self.var_valor_entradas.set(f"S/ {valor_entradas:,.2f}")
            self.var_valor_salidas.set(f"S/ {valor_salidas:,.2f}")
            
        except Exception as e:
            mostrar_error(f"Error al aplicar filtros:\n{str(e)}")
    
    def filtro_hoy(self):
        """Establece el filtro para hoy"""
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.var_fecha_desde.set(hoy)
        self.var_fecha_hasta.set(hoy)
        self.aplicar_filtros()
    
    def filtro_semana(self):
        """Establece el filtro para esta semana"""
        hoy = datetime.now()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        self.var_fecha_desde.set(inicio_semana.strftime("%Y-%m-%d"))
        self.var_fecha_hasta.set(hoy.strftime("%Y-%m-%d"))
        self.aplicar_filtros()
    
    def filtro_mes(self):
        """Establece el filtro para este mes"""
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        self.var_fecha_desde.set(inicio_mes.strftime("%Y-%m-%d"))
        self.var_fecha_hasta.set(hoy.strftime("%Y-%m-%d"))
        self.aplicar_filtros()
    
    def on_seleccionar_movimiento(self, event):
        """Evento cuando se selecciona un movimiento"""
        seleccion = self.tree.selection()
        if seleccion:
            self.btn_detalle.config(state=tk.NORMAL)
            if hasattr(self, 'btn_eliminar'):
                self.btn_eliminar.config(state=tk.NORMAL)
            valores = self.tree.item(seleccion[0])['values']
            self.transaccion_seleccionada = valores[0]  # ID
        else:
            self.btn_detalle.config(state=tk.DISABLED)
            if hasattr(self, 'btn_eliminar'):
                self.btn_eliminar.config(state=tk.DISABLED)
            self.transaccion_seleccionada = None
    
    def ver_detalle(self):
        """Muestra el detalle de la transacción seleccionada"""
        if not self.transaccion_seleccionada:
            return
        
        # Aquí puedes implementar una ventana de detalle
        mostrar_info("Detalle de transacción - Función por implementar")
    
    def eliminar_movimiento(self):
        """Elimina el movimiento seleccionado"""
        if not self.transaccion_seleccionada:
            mostrar_error("Seleccione un movimiento")
            return
        
        if confirmar_accion(
            "Confirmar eliminación",
            "¿Está seguro de eliminar este movimiento?\n"
            "Esta acción revertirá el stock del producto."
        ):
            try:
                Transaccion.eliminar(self.transaccion_seleccionada)
                mostrar_exito("Movimiento eliminado correctamente")
                self.cargar_movimientos()
                
            except Exception as e:
                mostrar_error(f"Error al eliminar movimiento:\n{str(e)}")