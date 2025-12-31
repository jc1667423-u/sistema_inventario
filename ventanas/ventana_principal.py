"""
Ventana Principal del Sistema de Inventario
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from constantes import *
from utilis import centrar_ventana
import temas
try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

class VentanaPrincipal:
    """Ventana principal del sistema con menú y área de trabajo"""
    
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        
        # Crear ventana principal
        self.ventana = tk.Toplevel(root)
        self.ventana.title(f"{APP_NOMBRE} - {usuario.nombre_completo}")
        self.ventana.geometry("1200x700")
        centrar_ventana(self.ventana, 1200, 700)
        
        # Maximizar ventana
        self.ventana.state('zoomed')
        
        # Al cerrar ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)
        
        # Variables para imagen de fondo
        self.imagen_fondo = None
        self.label_fondo = None
        
        # Crear interfaz
        self.crear_menu()
        self.crear_barra_superior()
        self.crear_area_trabajo()
        self.mostrar_dashboard()
    
    def crear_menu(self):
        """Crea el menú principal"""
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Menú Productos
        menu_productos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Productos", menu=menu_productos)
        menu_productos.add_command(label="Gestión de Productos", command=self.abrir_productos)
        menu_productos.add_command(label="Categorías", command=self.abrir_categorias)
        
        # Menú Transacciones
        menu_transacciones = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Movimientos", menu=menu_transacciones)
        menu_transacciones.add_command(label="Nueva Entrada", command=self.nueva_entrada)
        menu_transacciones.add_command(label="Nueva Salida", command=self.nueva_salida)
        menu_transacciones.add_separator()
        menu_transacciones.add_command(label="Ver Movimientos", command=self.ver_movimientos)
        menu_transacciones.add_command(label="Kardex", command=self.ver_kardex)
        
        # Menú Clientes/Proveedores
        menu_entidades = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Clientes/Proveedores", menu=menu_entidades)
        menu_entidades.add_command(label="Clientes", command=self.abrir_clientes)
        menu_entidades.add_command(label="Proveedores", command=self.abrir_proveedores)
        
        # Menú Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        menu_reportes.add_command(label="Inventario Actual", command=self.reporte_inventario)
        menu_reportes.add_command(label="Movimientos por Período", command=self.reporte_movimientos)
        menu_reportes.add_command(label="Valorización", command=self.reporte_valorizacion)
        menu_reportes.add_separator()
        menu_reportes.add_command(label="Stock Bajo", command=self.ver_stock_bajo)
        menu_reportes.add_command(label="Kardex General", command=self.ver_kardex_general)
        
        # Menú Usuarios (solo admin y super_admin)
        if self.usuario.tiene_permiso('usuarios', 'ver'):
            menu_usuarios = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Usuarios", menu=menu_usuarios)
            menu_usuarios.add_command(label="Gestión de Usuarios", command=self.abrir_usuarios)
        
        # Menú Configuración (solo super_admin para BD)
        menu_config = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configuración", menu=menu_config)
        
        # Configuración de BD solo para super_admin
        if self.usuario.rol == 'super_admin':
            menu_config.add_command(label="Base de Datos", command=self.abrir_config_bd)
            menu_config.add_separator()
        
        menu_config.add_command(label="Imagen de Fondo", command=self.seleccionar_imagen_fondo)
        menu_config.add_command(label="Quitar Imagen de Fondo", command=self.quitar_imagen_fondo)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
    
    def crear_barra_superior(self):
        """Crea la barra superior con información del usuario"""
        frame_barra = tk.Frame(self.ventana, bg=COLOR_PRIMARIO, height=60)
        frame_barra.pack(side=tk.TOP, fill=tk.X)
        frame_barra.pack_propagate(False)
        
        # Usuario actual
        label_usuario = tk.Label(
            frame_barra,
            text=f"👤 {self.usuario.nombre_completo}",
            font=("Arial", 11, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_usuario.pack(side=tk.RIGHT, padx=20)
        
        # Título
        label_titulo = tk.Label(
            frame_barra,
            text=APP_NOMBRE,
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(side=tk.LEFT, padx=20)
        
        # Botón cambiar tema
        tema_actual = temas.obtener_nombre_tema()
        icono_tema = "☀️" if tema_actual == "oscuro" else "🌙"
        texto_tema = "Modo Claro" if tema_actual == "oscuro" else "Modo Oscuro"
        
        self.btn_tema = tk.Button(
            frame_barra,
            text=f"{icono_tema} {texto_tema}",
            font=("Arial", 9, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.cambiar_tema,
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        self.btn_tema.pack(side=tk.RIGHT, padx=10)
    
    def crear_area_trabajo(self):
        """Crea el área de trabajo principal"""
        self.frame_trabajo = ttk.Frame(self.ventana, style="TFrame")
        self.frame_trabajo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def limpiar_area_trabajo(self):
        """Limpia el área de trabajo"""
        for widget in self.frame_trabajo.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal"""
        self.limpiar_area_trabajo()
        
        # Frame principal con padding
        frame_principal = ttk.Frame(self.frame_trabajo, style="TFrame")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        label_titulo = ttk.Label(
            frame_principal,
            text="📊 Panel de Control",
            style="Titulo.TLabel"
        )
        label_titulo.pack(pady=(0, 30))
        
        # Frame para tarjetas
        frame_tarjetas = ttk.Frame(frame_principal, style="TFrame")
        frame_tarjetas.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid
        frame_tarjetas.columnconfigure(0, weight=1)
        frame_tarjetas.columnconfigure(1, weight=1)
        frame_tarjetas.columnconfigure(2, weight=1)
        
        # Obtener estadísticas
        stats = self.obtener_estadisticas()
        
        # Tarjeta 1: Total Productos
        self.crear_tarjeta(
            frame_tarjetas,
            "📦 Total Productos",
            str(stats['total_productos']),
            COLOR_SECUNDARIO,
            0, 0
        )
        
        # Tarjeta 2: Productos con Stock Bajo
        stock_bajo_color = COLOR_ADVERTENCIA if stats['stock_bajo'] > 0 else COLOR_EXITO
        self.crear_tarjeta(
            frame_tarjetas,
            "⚠️ Stock Bajo",
            str(stats['stock_bajo']),
            stock_bajo_color,
            0, 1,
            comando=self.ver_stock_bajo if stats['stock_bajo'] > 0 else None
        )
        
        # Tarjeta 3: Valor Total Inventario
        self.crear_tarjeta(
            frame_tarjetas,
            "💰 Valor Inventario",
            f"S/ {stats['valor_total']:,.2f}",
            COLOR_EXITO,
            0, 2
        )
        
        # Frame para accesos rápidos
        frame_accesos = ttk.LabelFrame(
            frame_principal,
            text="Accesos Rápidos",
            padding=15
        )
        frame_accesos.pack(fill=tk.BOTH, expand=True, pady=(30, 0))
        
        # Contenedor interno para botones
        frame_botones = ttk.Frame(frame_accesos)
        frame_botones.pack(fill=tk.BOTH, expand=True)
        
        # Botones de acceso rápido
        botones = [
            ("📦 Productos", self.abrir_productos),
            ("📥 Nueva Entrada", self.nueva_entrada),
            ("📤 Nueva Salida", self.nueva_salida),
            ("👥 Clientes", self.abrir_clientes),
            ("🏢 Proveedores", self.abrir_proveedores),
            ("⚠️ Stock Bajo", self.ver_stock_bajo),
            ("📊 Kardex General", self.ver_kardex_general),
            ("📋 Ver Movimientos", self.ver_movimientos),
            ("📈 Reportes", self.reporte_inventario),
        ]
        
        for i, (texto, comando) in enumerate(botones):
            btn = ttk.Button(
                frame_botones,
                text=texto,
                command=comando,
                style="TButton"
            )
            btn.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='ew', ipady=10)
        
        # Marca de agua del desarrollador
        label_marca = ttk.Label(
            frame_principal,
            text="Sistema desarrollado por Jesús Calderón Chávez",
            font=("Segoe UI", 8),
            foreground="#888888"
        )
        label_marca.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)
    
    def crear_tarjeta(self, parent, titulo, valor, color, row, col, comando=None):
        """Crea una tarjeta de estadística"""
        # Usar tk.Frame para control de color específico
        frame = tk.Frame(parent, bg=color, relief=tk.FLAT, bd=0)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Si hay comando, hacer la tarjeta clickeable
        if comando:
            frame.config(cursor="hand2")
            frame.bind('<Button-1>', lambda e: comando())
        
        # Título
        label_titulo = tk.Label(
            frame,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(pady=(20, 5))
        
        if comando:
            label_titulo.bind('<Button-1>', lambda e: comando())
        
        # Valor
        label_valor = tk.Label(
            frame,
            text=valor,
            font=("Segoe UI", 24, "bold"),
            bg=color,
            fg=COLOR_BLANCO
        )
        label_valor.pack(pady=(0, 20))
        
        if comando:
            label_valor.bind('<Button-1>', lambda e: comando())
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas para el dashboard"""
        from base_datos.config_db import ejecutar_query
        
        # Total productos activos
        query_total = "SELECT COUNT(*) as total FROM productos WHERE activo = 1"
        total_productos = ejecutar_query(query_total)[0]['total']
        
        # Productos con stock bajo (menos de 10)
        query_bajo = "SELECT COUNT(*) as total FROM productos WHERE stock_actual < 10 AND activo = 1"
        stock_bajo = ejecutar_query(query_bajo)[0]['total']
        
        # Valor total del inventario
        query_valor = "SELECT SUM(stock_actual * precio) as valor FROM productos WHERE activo = 1"
        resultado_valor = ejecutar_query(query_valor)
        valor_total = resultado_valor[0]['valor'] if resultado_valor[0]['valor'] else 0
        
        return {
            'total_productos': total_productos,
            'stock_bajo': stock_bajo,
            'valor_total': valor_total
        }
    
    # Métodos de los módulos
    def abrir_productos(self):
        """Abre la ventana de gestión de productos"""
        from ventanas.productos import VentanaProductos
        VentanaProductos(self.ventana, self.usuario)
    
    def abrir_categorias(self):
        messagebox.showinfo("Info", "Módulo de Categorías - Próximamente")
    
    def nueva_entrada(self):
        """Abre la ventana para registrar entrada"""
        from ventanas.entrada import VentanaEntrada
        VentanaEntrada(self.ventana, self.usuario)
    
    def nueva_salida(self):
        """Abre la ventana para registrar salida"""
        from ventanas.salida import VentanaSalida
        VentanaSalida(self.ventana, self.usuario)
    
    def ver_movimientos(self):
        """Abre la ventana de ver movimientos"""
        from ventanas.movimientos import VentanaMovimientos
        VentanaMovimientos(self.ventana, self.usuario)
    
    def ver_kardex(self):
        """Abre la ventana de kardex"""
        from ventanas.kardex_producto import VentanaKardex
        VentanaKardex(self.ventana, self.usuario)
    
    def abrir_clientes(self):
        """Abre la ventana de gestión de clientes"""
        from ventanas.clientes import VentanaClientesProveedores
        VentanaClientesProveedores(self.ventana, self.usuario, tipo_default='cliente')
    
    def abrir_proveedores(self):
        """Abre la ventana de gestión de proveedores"""
        from ventanas.clientes import VentanaClientesProveedores
        VentanaClientesProveedores(self.ventana, self.usuario, tipo_default='proveedor')
    
    def reporte_inventario(self):
        """Abre la ventana de reportes"""
        from ventanas.reportes import VentanaReportes
        VentanaReportes(self.ventana, self.usuario)
    
    def reporte_movimientos(self):
        """Abre la ventana de reportes"""
        from ventanas.reportes import VentanaReportes
        VentanaReportes(self.ventana, self.usuario)
    
    def reporte_valorizacion(self):
        """Abre la ventana de reportes"""
        from ventanas.reportes import VentanaReportes
        VentanaReportes(self.ventana, self.usuario)
    
    def abrir_usuarios(self):
        """Abre la ventana de gestión de usuarios"""
        from ventanas.usuarios import VentanaUsuarios
        VentanaUsuarios(self.ventana, self.usuario)
    
    def mostrar_acerca_de(self):
        """Muestra información del sistema"""
        messagebox.showinfo(
            "Acerca de",
            f"{APP_NOMBRE}\n"
            f"Versión {APP_VERSION}\n\n"
            f"{APP_EMPRESA}\n"
            f"Sistema de gestión de inventario"
        )
    
    def ver_stock_bajo(self):
        """Abre la ventana de productos con stock bajo"""
        from ventanas.alertas import VentanaStockBajo
        VentanaStockBajo(self.ventana, self.usuario)
    
    def ver_kardex_general(self):
        """Abre la ventana de kardex general"""
        from ventanas.kardex_general import VentanaKardexGeneral
        VentanaKardexGeneral(self.ventana, self.usuario)
    
    def cambiar_tema(self):
        """Cambia entre tema claro y oscuro"""
        messagebox.showinfo(
            "Cambio de Tema",
            "El cambio de tema se aplicará al reiniciar la aplicación."
        )
        temas.alternar_tema()
    
    def abrir_config_bd(self):
        """Abre la ventana de configuración de BD"""
        from ventanas.configuracion_bd import VentanaConfiguracionBD
        VentanaConfiguracionBD(self.ventana)
    
    def seleccionar_imagen_fondo(self):
        """Permite seleccionar una imagen de fondo"""
        if not PIL_DISPONIBLE:
            messagebox.showerror(
                "Error",
                "La librería PIL/Pillow no está instalada.\n\n"
                "Instale con: pip install Pillow"
            )
            return
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar imagen de fondo",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            # Guardar ruta en configuración
            config = temas.cargar_config_usuario()
            config['imagen_fondo'] = archivo
            temas.guardar_config_usuario(config)
            
            messagebox.showinfo(
                "Imagen de Fondo",
                "La imagen de fondo se aplicará al reiniciar la aplicación."
            )
    
    def quitar_imagen_fondo(self):
        """Quita la imagen de fondo"""
        config = temas.cargar_config_usuario()
        config['imagen_fondo'] = None
        temas.guardar_config_usuario(config)
        
        messagebox.showinfo(
            "Imagen de Fondo",
            "La imagen de fondo se quitará al reiniciar la aplicación."
        )
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar la sesión?"):
            self.ventana.destroy()
            # Volver a mostrar el login
            from ventanas.login import VentanaLogin
            VentanaLogin(self.root)