"""
Ventana de Reportes - Generación y exportación
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from clases.productos import Producto
from clases.transacciones import Transaccion
from constantes import *
from utilis import *
from datetime import datetime
import os

class VentanaReportes:
    """Ventana para generar y exportar reportes"""
    
    def __init__(self, parent, usuario):
        self.parent = parent
        self.usuario = usuario
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Reportes del Sistema")
        self.ventana.geometry("900x600")
        centrar_ventana(self.ventana, 900, 600)
        
        self.crear_interfaz()
    
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
            text="📊 Reportes del Sistema",
            font=("Arial", 18, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(pady=15)
        
        # Frame contenedor
        frame_contenedor = tk.Frame(frame_principal, bg=COLOR_BLANCO)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título
        tk.Label(
            frame_contenedor,
            text="Seleccione el tipo de reporte que desea generar:",
            font=("Arial", 12),
            bg=COLOR_BLANCO
        ).pack(pady=(0, 20))
        
        # Reportes disponibles
        reportes = [
            {
                'nombre': '📦 Inventario Actual',
                'descripcion': 'Listado completo de productos con stock y valores',
                'comando': self.reporte_inventario
            },
            {
                'nombre': '📋 Movimientos por Período',
                'descripcion': 'Historial de entradas y salidas en un rango de fechas',
                'comando': self.reporte_movimientos
            },
            {
                'nombre': '💰 Valorización de Inventario',
                'descripcion': 'Valor total del inventario por producto',
                'comando': self.reporte_valorizacion
            },
            {
                'nombre': '📊 Kardex por Producto',
                'descripcion': 'Movimientos detallados de un producto específico',
                'comando': self.reporte_kardex
            },
            {
                'nombre': '📈 Productos con Stock Bajo',
                'descripcion': 'Productos que están por debajo del stock mínimo',
                'comando': self.reporte_stock_bajo
            }
        ]
        
        for reporte in reportes:
            self.crear_boton_reporte(frame_contenedor, reporte)
    
    def crear_boton_reporte(self, parent, reporte):
        """Crea un botón para cada tipo de reporte"""
        frame = tk.Frame(parent, bg=COLOR_BLANCO, relief=tk.RAISED, bd=1)
        frame.pack(fill=tk.X, pady=10)
        
        frame_info = tk.Frame(frame, bg=COLOR_BLANCO)
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(
            frame_info,
            text=reporte['nombre'],
            font=("Arial", 11, "bold"),
            bg=COLOR_BLANCO,
            anchor='w'
        ).pack(fill=tk.X)
        
        tk.Label(
            frame_info,
            text=reporte['descripcion'],
            font=("Arial", 9),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            anchor='w'
        ).pack(fill=tk.X)
        
        btn = tk.Button(
            frame,
            text="Generar ➜",
            font=("Arial", 10, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=reporte['comando'],
            width=12
        )
        btn.pack(side=tk.RIGHT, padx=15, pady=15)
    
    def reporte_inventario(self):
        """Genera reporte de inventario actual"""
        try:
            productos = Producto.obtener_todos()
            
            if not productos:
                mostrar_advertencia("No hay productos para reportar")
                return
            
            # Preguntar dónde guardar
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not archivo:
                return
            
            # Generar CSV
            with open(archivo, 'w', encoding='utf-8-sig') as f:
                # Encabezados
                f.write("Código,Descripción,Unidad,Precio,Stock,Valor Total,Estado\n")
                
                # Datos
                for prod in productos:
                    valor_total = prod['precio'] * prod['stock_actual']
                    estado = "Activo" if prod['activo'] == 1 else "Inactivo"
                    
                    f.write(f"{prod['codigo']},"
                           f"\"{prod['descripcion']}\","
                           f"{prod['unidad_medida']},"
                           f"{prod['precio']:.2f},"
                           f"{prod['stock_actual']},"
                           f"{valor_total:.2f},"
                           f"{estado}\n")
            
            mostrar_exito(f"Reporte generado correctamente:\n{archivo}")
            
            # Preguntar si desea abrir
            if confirmar_accion("Abrir archivo", "¿Desea abrir el archivo generado?"):
                os.startfile(archivo)
            
        except Exception as e:
            mostrar_error(f"Error al generar reporte:\n{str(e)}")
    
    def reporte_movimientos(self):
        """Genera reporte de movimientos por período"""
        # Ventana para seleccionar fechas
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Seleccionar Período")
        ventana.geometry("400x250")
        centrar_ventana(ventana, 400, 250)
        ventana.grab_set()
        
        frame = tk.Frame(ventana, bg=COLOR_BLANCO)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(
            frame,
            text="Seleccione el período:",
            font=("Arial", 12, "bold"),
            bg=COLOR_BLANCO
        ).pack(pady=(0, 20))
        
        # Fecha desde
        tk.Label(frame, text="Fecha Desde:", bg=COLOR_BLANCO).pack(anchor='w')
        var_desde = tk.StringVar(value=obtener_fecha_actual())
        entry_desde = ttk.Entry(frame, textvariable=var_desde)
        entry_desde.pack(fill=tk.X, pady=(5, 15))
        
        # Fecha hasta
        tk.Label(frame, text="Fecha Hasta:", bg=COLOR_BLANCO).pack(anchor='w')
        var_hasta = tk.StringVar(value=obtener_fecha_actual())
        entry_hasta = ttk.Entry(frame, textvariable=var_hasta)
        entry_hasta.pack(fill=tk.X, pady=(5, 20))
        
        def generar():
            try:
                fecha_desde = var_desde.get()
                fecha_hasta = var_hasta.get()
                
                movimientos = Transaccion.obtener_por_fecha(fecha_desde, fecha_hasta)
                
                if not movimientos:
                    mostrar_advertencia("No hay movimientos en el período seleccionado")
                    return
                
                # Preguntar dónde guardar
                archivo = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    initialfile=f"movimientos_{fecha_desde}_a_{fecha_hasta}.csv"
                )
                
                if not archivo:
                    return
                
                # Generar CSV
                with open(archivo, 'w', encoding='utf-8-sig') as f:
                    f.write("Fecha,Tipo,Producto,Cantidad,Costo/Precio,Total,Cliente/Proveedor,Documento,Usuario\n")
                    
                    for mov in movimientos:
                        tipo = mov['tipo_movimiento']
                        cantidad = mov['cantidad_entrada'] if tipo == 'Entrada' else mov['cantidad_salida']
                        total = mov['valor_entrada'] if tipo == 'Entrada' else mov['valor_salida']
                        entidad = mov['entidad_nombre'] if mov['entidad_nombre'] else ''
                        
                        f.write(f"{formatear_fecha_hora(mov['fecha'])},"
                               f"{tipo},"
                               f"\"{mov['producto_descripcion']}\","
                               f"{cantidad},"
                               f"{mov['costo']:.2f},"
                               f"{total:.2f},"
                               f"\"{entidad}\","
                               f"{mov['documento'] if mov['documento'] else ''},"
                               f"\"{mov['usuario_nombre']}\"\n")
                
                ventana.destroy()
                mostrar_exito(f"Reporte generado correctamente:\n{archivo}")
                
                if confirmar_accion("Abrir archivo", "¿Desea abrir el archivo generado?"):
                    os.startfile(archivo)
                
            except Exception as e:
                mostrar_error(f"Error al generar reporte:\n{str(e)}")
        
        btn_generar = tk.Button(
            frame,
            text="Generar Reporte",
            font=("Arial", 10, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=generar
        )
        btn_generar.pack(fill=tk.X, ipady=8)
    
    def reporte_valorizacion(self):
        """Genera reporte de valorización"""
        try:
            productos = Producto.obtener_todos()
            
            if not productos:
                mostrar_advertencia("No hay productos para reportar")
                return
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"valorizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not archivo:
                return
            
            with open(archivo, 'w', encoding='utf-8-sig') as f:
                f.write("Código,Descripción,Stock,Precio Unitario,Valor Total\n")
                
                total_general = 0
                
                for prod in productos:
                    valor_total = prod['precio'] * prod['stock_actual']
                    total_general += valor_total
                    
                    f.write(f"{prod['codigo']},"
                           f"\"{prod['descripcion']}\","
                           f"{prod['stock_actual']},"
                           f"{prod['precio']:.2f},"
                           f"{valor_total:.2f}\n")
                
                f.write(f"\n,,,TOTAL:,{total_general:.2f}\n")
            
            mostrar_exito(f"Reporte generado correctamente:\n{archivo}\n\nValor Total: S/ {total_general:,.2f}")
            
            if confirmar_accion("Abrir archivo", "¿Desea abrir el archivo generado?"):
                os.startfile(archivo)
            
        except Exception as e:
            mostrar_error(f"Error al generar reporte:\n{str(e)}")
    
    def reporte_kardex(self):
        """Genera reporte de kardex por producto"""
        mostrar_info("Seleccione un producto desde el módulo Kardex\npara generar el reporte")
    
    def reporte_stock_bajo(self):
        """Genera reporte de productos con stock bajo"""
        try:
            productos = Producto.obtener_productos_bajo_stock(limite=20)
            
            if not productos:
                mostrar_info("No hay productos con stock bajo")
                return
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"stock_bajo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not archivo:
                return
            
            with open(archivo, 'w', encoding='utf-8-sig') as f:
                f.write("Código,Descripción,Unidad,Stock Actual,Precio\n")
                
                for prod in productos:
                    f.write(f"{prod['codigo']},"
                           f"\"{prod['descripcion']}\","
                           f"{prod['unidad_medida']},"
                           f"{prod['stock_actual']},"
                           f"{prod['precio']:.2f}\n")
            
            mostrar_exito(f"Reporte generado correctamente:\n{archivo}")
            
            if confirmar_accion("Abrir archivo", "¿Desea abrir el archivo generado?"):
                os.startfile(archivo)
            
        except Exception as e:
            mostrar_error(f"Error al generar reporte:\n{str(e)}")