"""
Ventana para registrar salidas de mercancía con búsqueda mejorada
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.transacciones import Transaccion
from clases.productos import Producto
from clases.clientes import ClienteProveedor
from constantes import *
from utilis import *

class VentanaSalida:
    """Ventana para registrar salida de productos"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Salida de Mercancía")
        self.ventana.geometry("800x700")
        centrar_ventana(self.ventana, 800, 700)
        
        self.productos_completos = []
        self.clientes_completos = []
        
        self.crear_interfaz()
        self.cargar_productos()
        self.cargar_clientes()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_PELIGRO, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="📤 Registrar Salida de Mercancía",
            font=("Arial", 18, "bold"),
            bg=COLOR_PELIGRO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(pady=15)
        
        # Frame formulario
        frame_form = tk.Frame(frame_principal, bg=COLOR_BLANCO)
        frame_form.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Variables
        self.var_producto = tk.StringVar()
        self.var_busqueda_producto = tk.StringVar()
        self.var_cliente = tk.StringVar()
        self.var_busqueda_cliente = tk.StringVar()
        self.var_cantidad = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_documento = tk.StringVar()
        self.var_fecha = tk.StringVar(value=obtener_fecha_actual())
        self.var_concepto = tk.StringVar()
        self.var_stock_disponible = tk.StringVar(value="Stock disponible: -")
        
        # Configurar trazas
        self.var_busqueda_producto.trace('w', self.filtrar_productos)
        self.var_busqueda_cliente.trace('w', self.filtrar_clientes)
        
        row = 0
        
        # Fecha
        tk.Label(
            frame_form,
            text="Fecha *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_fecha = ttk.Entry(
            frame_form,
            textvariable=self.var_fecha,
            font=("Arial", 10)
        )
        entry_fecha.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Producto con búsqueda
        tk.Label(
            frame_form,
            text="Producto *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_busqueda_prod = ttk.Entry(
            frame_form,
            textvariable=self.var_busqueda_producto,
            font=("Arial", 10)
        )
        entry_busqueda_prod.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        tk.Label(
            frame_form,
            text="Escribe el código o nombre del producto",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).grid(row=row+1, column=1, sticky='w', padx=(10, 0))
        
        row += 2
        
        self.combo_producto = ttk.Combobox(
            frame_form,
            textvariable=self.var_producto,
            font=("Arial", 10),
            state='readonly',
            height=15
        )
        self.combo_producto.grid(row=row, column=1, sticky='ew', pady=5, padx=(10, 0))
        self.combo_producto.bind('<<ComboboxSelected>>', self.mostrar_stock)
        
        row += 1
        
        # Stock disponible
        label_stock = tk.Label(
            frame_form,
            textvariable=self.var_stock_disponible,
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_SECUNDARIO
        )
        label_stock.grid(row=row, column=1, sticky='w', padx=(10, 0), pady=5)
        
        row += 1
        
        # Cliente con búsqueda
        tk.Label(
            frame_form,
            text="Cliente",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_busqueda_cli = ttk.Entry(
            frame_form,
            textvariable=self.var_busqueda_cliente,
            font=("Arial", 10)
        )
        entry_busqueda_cli.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        tk.Label(
            frame_form,
            text="Escribe el nombre del cliente",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).grid(row=row+1, column=1, sticky='w', padx=(10, 0))
        
        row += 2
        
        self.combo_cliente = ttk.Combobox(
            frame_form,
            textvariable=self.var_cliente,
            font=("Arial", 10),
            state='readonly',
            height=10
        )
        self.combo_cliente.grid(row=row, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        row += 1
        
        # Cantidad
        tk.Label(
            frame_form,
            text="Cantidad *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_cantidad = ttk.Entry(
            frame_form,
            textvariable=self.var_cantidad,
            font=("Arial", 10)
        )
        entry_cantidad.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        configurar_validacion_decimal(entry_cantidad)
        
        row += 1
        
        # Precio unitario
        tk.Label(
            frame_form,
            text="Precio Unitario (S/) *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_precio = ttk.Entry(
            frame_form,
            textvariable=self.var_precio,
            font=("Arial", 10)
        )
        entry_precio.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        configurar_validacion_decimal(entry_precio)
        
        row += 1
        
        # Documento
        tk.Label(
            frame_form,
            text="N° Documento",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_documento = ttk.Entry(
            frame_form,
            textvariable=self.var_documento,
            font=("Arial", 10)
        )
        entry_documento.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Concepto
        tk.Label(
            frame_form,
            text="Concepto",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='nw', pady=10)
        
        text_concepto = tk.Text(
            frame_form,
            font=("Arial", 10),
            height=3,
            width=40
        )
        text_concepto.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        self.text_concepto = text_concepto
        
        row += 1
        
        # Nota
        label_nota = tk.Label(
            frame_form,
            text="* Campos obligatorios",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        )
        label_nota.grid(row=row, column=0, columnspan=2, pady=(20, 10))
        
        row += 1
        
        # Botones
        frame_botones = tk.Frame(frame_form, bg=COLOR_BLANCO)
        frame_botones.grid(row=row, column=0, columnspan=2, pady=20)
        
        btn_guardar = tk.Button(
            frame_botones,
            text="💾 Registrar Salida",
            font=("Arial", 11, "bold"),
            bg=COLOR_PELIGRO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.registrar_salida,
            width=20
        )
        btn_guardar.pack(side=tk.LEFT, padx=5, ipady=8)
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="❌ Cancelar",
            font=("Arial", 11, "bold"),
            bg=COLOR_TEXTO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.ventana.destroy,
            width=15
        )
        btn_cancelar.pack(side=tk.LEFT, padx=5, ipady=8)
        
        # Configurar grid
        frame_form.columnconfigure(1, weight=1)
    
    def cargar_productos(self):
        """Carga todos los productos"""
        try:
            self.productos_completos = Producto.obtener_todos()
            self.productos_dict = {}
            valores = []
            
            for prod in self.productos_completos:
                texto = f"{prod['codigo']} - {prod['descripcion']}"
                valores.append(texto)
                self.productos_dict[texto] = {
                    'id': prod['id'],
                    'stock': prod['stock_actual'],
                    'precio': prod['precio']
                }
            
            self.combo_producto['values'] = valores
            
        except Exception as e:
            mostrar_error(f"Error al cargar productos:\n{str(e)}")
    
    def filtrar_productos(self, *args):
        """Filtra productos en tiempo real"""
        termino = self.var_busqueda_producto.get().strip().upper()
        
        if not termino:
            valores = [f"{p['codigo']} - {p['descripcion']}" for p in self.productos_completos]
            self.combo_producto['values'] = valores
            return
        
        productos_filtrados = []
        for prod in self.productos_completos:
            if (termino in prod['codigo'].upper() or 
                termino in prod['descripcion'].upper()):
                texto = f"{prod['codigo']} - {prod['descripcion']}"
                productos_filtrados.append(texto)
        
        self.combo_producto['values'] = productos_filtrados
        
        if len(productos_filtrados) == 1:
            self.var_producto.set(productos_filtrados[0])
            self.mostrar_stock()
        
        if productos_filtrados:
            self.combo_producto.event_generate('<Button-1>')
    
    def cargar_clientes(self):
        """Carga todos los clientes"""
        try:
            self.clientes_completos = ClienteProveedor.obtener_clientes()
            self.clientes_dict = {}
            valores = ["(Sin cliente)"]
            self.clientes_dict["(Sin cliente)"] = None
            
            for cli in self.clientes_completos:
                texto = cli['nombre']
                valores.append(texto)
                self.clientes_dict[texto] = cli['id']
            
            self.combo_cliente['values'] = valores
            self.combo_cliente.current(0)
            
        except Exception as e:
            mostrar_error(f"Error al cargar clientes:\n{str(e)}")
    
    def filtrar_clientes(self, *args):
        """Filtra clientes en tiempo real"""
        termino = self.var_busqueda_cliente.get().strip().upper()
        
        if not termino:
            valores = ["(Sin cliente)"] + [c['nombre'] for c in self.clientes_completos]
            self.combo_cliente['values'] = valores
            return
        
        clientes_filtrados = ["(Sin cliente)"]
        for cli in self.clientes_completos:
            if termino in cli['nombre'].upper():
                clientes_filtrados.append(cli['nombre'])
        
        self.combo_cliente['values'] = clientes_filtrados
        
        if len(clientes_filtrados) == 2:
            self.var_cliente.set(clientes_filtrados[1])
        
        if len(clientes_filtrados) > 1:
            self.combo_cliente.event_generate('<Button-1>')
    
    def mostrar_stock(self, event=None):
        """Muestra el stock disponible del producto seleccionado"""
        producto_texto = self.var_producto.get()
        if producto_texto and producto_texto in self.productos_dict:
            info = self.productos_dict[producto_texto]
            stock = info['stock']
            precio = info['precio']
            
            if stock <= 0:
                self.var_stock_disponible.set(f"⚠️ SIN STOCK - Stock: {stock}")
            elif stock <= 5:
                self.var_stock_disponible.set(f"⚠️ STOCK BAJO - Stock disponible: {stock} unidades")
            else:
                self.var_stock_disponible.set(f"✅ Stock disponible: {stock} unidades")
            
            self.var_precio.set(str(precio))
    
    def registrar_salida(self):
        """Registra la salida de mercancía"""
        # Validaciones
        if not validar_campo_vacio(self.var_fecha.get(), "Fecha"):
            return
        if not validar_campo_vacio(self.var_producto.get(), "Producto"):
            return
        if not validar_campo_vacio(self.var_cantidad.get(), "Cantidad"):
            return
        if not validar_campo_vacio(self.var_precio.get(), "Precio"):
            return
        
        if not validar_numero(self.var_cantidad.get()):
            mostrar_error("La cantidad debe ser un número válido")
            return
        
        if not validar_numero(self.var_precio.get()):
            mostrar_error("El precio debe ser un número válido")
            return
        
        cantidad = int(float(self.var_cantidad.get()))
        if cantidad <= 0:
            mostrar_error("La cantidad debe ser mayor a cero")
            return
        
        precio = float(self.var_precio.get())
        if precio < 0:
            mostrar_error("El precio no puede ser negativo")
            return
        
        try:
            info = self.productos_dict[self.var_producto.get()]
            producto_id = info['id']
            stock_actual = info['stock']
            
            # Verificar stock
            if cantidad > stock_actual:
                if not confirmar_accion(
                    "Stock insuficiente",
                    f"El stock actual es {stock_actual} unidades.\n"
                    f"¿Desea registrar la salida de {cantidad} unidades de todas formas?"
                ):
                    return
            
            cliente_id = self.clientes_dict.get(self.var_cliente.get())
            fecha = self.var_fecha.get()
            documento = self.var_documento.get().strip() if self.var_documento.get().strip() else None
            concepto = self.text_concepto.get("1.0", tk.END).strip() if self.text_concepto.get("1.0", tk.END).strip() else None
            
            # Registrar salida
            Transaccion.registrar_salida(
                producto_id=producto_id,
                cantidad=cantidad,
                precio=precio,
                fecha=fecha,
                cliente_id=cliente_id,
                documento=documento,
                concepto=concepto,
                usuario_id=self.usuario.id
            )
            
            mostrar_exito(f"Salida registrada correctamente\nCantidad: {cantidad}\nTotal: S/ {cantidad * precio:.2f}")
            self.ventana.destroy()
            
        except Exception as e:
            mostrar_error(f"Error al registrar salida:\n{str(e)}")