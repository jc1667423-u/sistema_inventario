"""
Ventana para registrar entradas de mercancía con búsqueda mejorada
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.transacciones import Transaccion
from clases.productos import Producto
from clases.clientes import ClienteProveedor
from constantes import *
from utilis import *
from datetime import datetime

class VentanaEntrada:
    """Ventana para registrar entrada de productos"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Entrada de Mercancía")
        self.ventana.geometry("800x650")
        centrar_ventana(self.ventana, 800, 650)
        
        self.productos_completos = []  # Lista completa de productos
        self.proveedores_completos = []  # Lista completa de proveedores
        
        self.crear_interfaz()
        self.cargar_productos()
        self.cargar_proveedores()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_EXITO, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="📥 Registrar Entrada de Mercancía",
            font=("Arial", 18, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(pady=15)
        
        # Frame formulario
        frame_form = tk.Frame(frame_principal, bg=COLOR_BLANCO)
        frame_form.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Variables
        self.var_producto = tk.StringVar()
        self.var_busqueda_producto = tk.StringVar()
        self.var_proveedor = tk.StringVar()
        self.var_busqueda_proveedor = tk.StringVar()
        self.var_cantidad = tk.StringVar()
        self.var_costo = tk.StringVar()
        self.var_documento = tk.StringVar()
        self.var_fecha = tk.StringVar(value=obtener_fecha_actual())
        self.var_concepto = tk.StringVar()
        
        # Configurar trazas para búsqueda en tiempo real
        self.var_busqueda_producto.trace('w', self.filtrar_productos)
        self.var_busqueda_proveedor.trace('w', self.filtrar_proveedores)
        
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
        
        # Entry de búsqueda
        entry_busqueda_prod = ttk.Entry(
            frame_form,
            textvariable=self.var_busqueda_producto,
            font=("Arial", 10)
        )
        entry_busqueda_prod.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Label de ayuda
        tk.Label(
            frame_form,
            text="Escribe el código o nombre del producto",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).grid(row=row+1, column=1, sticky='w', padx=(10, 0))
        
        row += 2
        
        # Combobox de productos (se actualiza con la búsqueda)
        self.combo_producto = ttk.Combobox(
            frame_form,
            textvariable=self.var_producto,
            font=("Arial", 10),
            state='readonly',
            height=15
        )
        self.combo_producto.grid(row=row, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        row += 1
        
        # Proveedor con búsqueda
        tk.Label(
            frame_form,
            text="Proveedor",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        # Entry de búsqueda proveedor
        entry_busqueda_prov = ttk.Entry(
            frame_form,
            textvariable=self.var_busqueda_proveedor,
            font=("Arial", 10)
        )
        entry_busqueda_prov.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Label de ayuda
        tk.Label(
            frame_form,
            text="Escribe el nombre del proveedor",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO
        ).grid(row=row+1, column=1, sticky='w', padx=(10, 0))
        
        row += 2
        
        # Combobox de proveedores
        self.combo_proveedor = ttk.Combobox(
            frame_form,
            textvariable=self.var_proveedor,
            font=("Arial", 10),
            state='readonly',
            height=10
        )
        self.combo_proveedor.grid(row=row, column=1, sticky='ew', pady=5, padx=(10, 0))
        
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
        
        # Costo unitario
        tk.Label(
            frame_form,
            text="Costo Unitario (S/) *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        entry_costo = ttk.Entry(
            frame_form,
            textvariable=self.var_costo,
            font=("Arial", 10)
        )
        entry_costo.grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        configurar_validacion_decimal(entry_costo)
        
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
            text="💾 Registrar Entrada",
            font=("Arial", 11, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.registrar_entrada,
            width=20
        )
        btn_guardar.pack(side=tk.LEFT, padx=5, ipady=8)
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="❌ Cancelar",
            font=("Arial", 11, "bold"),
            bg=COLOR_PELIGRO,
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
                self.productos_dict[texto] = prod['id']
            
            self.combo_producto['values'] = valores
            
        except Exception as e:
            mostrar_error(f"Error al cargar productos:\n{str(e)}")
    
    def filtrar_productos(self, *args):
        """Filtra productos en tiempo real según el texto de búsqueda"""
        termino = self.var_busqueda_producto.get().strip().upper()
        
        if not termino:
            # Si no hay búsqueda, mostrar todos
            valores = [f"{p['codigo']} - {p['descripcion']}" for p in self.productos_completos]
            self.combo_producto['values'] = valores
            return
        
        # Filtrar productos por código o descripción
        productos_filtrados = []
        for prod in self.productos_completos:
            if (termino in prod['codigo'].upper() or 
                termino in prod['descripcion'].upper()):
                texto = f"{prod['codigo']} - {prod['descripcion']}"
                productos_filtrados.append(texto)
        
        self.combo_producto['values'] = productos_filtrados
        
        # Si solo hay un resultado, seleccionarlo automáticamente
        if len(productos_filtrados) == 1:
            self.var_producto.set(productos_filtrados[0])
        
        # Mostrar el combobox si hay resultados
        if productos_filtrados:
            self.combo_producto.event_generate('<Button-1>')
    
    def cargar_proveedores(self):
        """Carga todos los proveedores"""
        try:
            self.proveedores_completos = ClienteProveedor.obtener_proveedores()
            self.proveedores_dict = {}
            valores = ["(Sin proveedor)"]
            self.proveedores_dict["(Sin proveedor)"] = None
            
            for prov in self.proveedores_completos:
                texto = prov['nombre']
                valores.append(texto)
                self.proveedores_dict[texto] = prov['id']
            
            self.combo_proveedor['values'] = valores
            self.combo_proveedor.current(0)
            
        except Exception as e:
            mostrar_error(f"Error al cargar proveedores:\n{str(e)}")
    
    def filtrar_proveedores(self, *args):
        """Filtra proveedores en tiempo real según el texto de búsqueda"""
        termino = self.var_busqueda_proveedor.get().strip().upper()
        
        if not termino:
            # Si no hay búsqueda, mostrar todos
            valores = ["(Sin proveedor)"] + [p['nombre'] for p in self.proveedores_completos]
            self.combo_proveedor['values'] = valores
            return
        
        # Filtrar proveedores por nombre
        proveedores_filtrados = ["(Sin proveedor)"]
        for prov in self.proveedores_completos:
            if termino in prov['nombre'].upper():
                proveedores_filtrados.append(prov['nombre'])
        
        self.combo_proveedor['values'] = proveedores_filtrados
        
        # Si solo hay un resultado (además de "Sin proveedor"), seleccionarlo
        if len(proveedores_filtrados) == 2:
            self.var_proveedor.set(proveedores_filtrados[1])
        
        # Mostrar el combobox si hay resultados
        if len(proveedores_filtrados) > 1:
            self.combo_proveedor.event_generate('<Button-1>')
    
    def registrar_entrada(self):
        """Registra la entrada de mercancía"""
        # Validaciones
        if not validar_campo_vacio(self.var_fecha.get(), "Fecha"):
            return
        if not validar_campo_vacio(self.var_producto.get(), "Producto"):
            return
        if not validar_campo_vacio(self.var_cantidad.get(), "Cantidad"):
            return
        if not validar_campo_vacio(self.var_costo.get(), "Costo"):
            return
        
        if not validar_numero(self.var_cantidad.get()):
            mostrar_error("La cantidad debe ser un número válido")
            return
        
        if not validar_numero(self.var_costo.get()):
            mostrar_error("El costo debe ser un número válido")
            return
        
        cantidad = int(float(self.var_cantidad.get()))
        if cantidad <= 0:
            mostrar_error("La cantidad debe ser mayor a cero")
            return
        
        costo = float(self.var_costo.get())
        if costo < 0:
            mostrar_error("El costo no puede ser negativo")
            return
        
        try:
            producto_id = self.productos_dict[self.var_producto.get()]
            proveedor_id = self.proveedores_dict.get(self.var_proveedor.get())
            fecha = self.var_fecha.get()
            documento = self.var_documento.get().strip() if self.var_documento.get().strip() else None
            concepto = self.text_concepto.get("1.0", tk.END).strip() if self.text_concepto.get("1.0", tk.END).strip() else None
            
            # Registrar entrada
            Transaccion.registrar_entrada(
                producto_id=producto_id,
                cantidad=cantidad,
                costo=costo,
                fecha=fecha,
                proveedor_id=proveedor_id,
                documento=documento,
                concepto=concepto,
                usuario_id=self.usuario.id
            )
            
            mostrar_exito(f"Entrada registrada correctamente\nCantidad: {cantidad}\nTotal: S/ {cantidad * costo:.2f}")
            self.ventana.destroy()
            
        except Exception as e:
            mostrar_error(f"Error al registrar entrada:\n{str(e)}")