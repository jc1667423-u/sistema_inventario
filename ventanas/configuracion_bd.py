"""
Ventana de Configuración de Base de Datos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from constantes import *
from utilis import centrar_ventana, validar_campo_vacio
import os

class VentanaConfiguracionBD:
    """Ventana para configurar la conexión a la base de datos"""
    
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Configuración de Base de Datos")
        self.ventana.geometry("600x500")
        centrar_ventana(self.ventana, 600, 500)
        self.ventana.resizable(False, False)
        
        self.crear_interfaz()
        self.cargar_configuracion_actual()
    
    def crear_interfaz(self):
        """Crea la interfaz"""
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        frame_titulo = tk.Frame(frame_principal, bg=COLOR_PRIMARIO, height=60)
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_titulo,
            text="⚙️ Configuración de Base de Datos",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        )
        label_titulo.pack(pady=15)
        
        # Frame formulario
        frame_form = tk.Frame(frame_principal, bg=COLOR_BLANCO)
        frame_form.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Variables
        self.var_host = tk.StringVar()
        self.var_port = tk.StringVar()
        self.var_user = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_database = tk.StringVar()
        
        row = 0
        
        # Host
        tk.Label(
            frame_form,
            text="Host / Servidor *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        ttk.Entry(
            frame_form,
            textvariable=self.var_host,
            font=("Arial", 10),
            width=40
        ).grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Puerto
        tk.Label(
            frame_form,
            text="Puerto *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        ttk.Entry(
            frame_form,
            textvariable=self.var_port,
            font=("Arial", 10),
            width=40
        ).grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Usuario
        tk.Label(
            frame_form,
            text="Usuario *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        ttk.Entry(
            frame_form,
            textvariable=self.var_user,
            font=("Arial", 10),
            width=40
        ).grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Contraseña
        tk.Label(
            frame_form,
            text="Contraseña *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        ttk.Entry(
            frame_form,
            textvariable=self.var_password,
            font=("Arial", 10),
            show="*",
            width=40
        ).grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Base de datos
        tk.Label(
            frame_form,
            text="Base de Datos *",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO
        ).grid(row=row, column=0, sticky='w', pady=10)
        
        ttk.Entry(
            frame_form,
            textvariable=self.var_database,
            font=("Arial", 10),
            width=40
        ).grid(row=row, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        row += 1
        
        # Nota
        label_nota = tk.Label(
            frame_form,
            text="* Campos obligatorios\n\n⚠️ Los cambios requieren reiniciar la aplicación",
            font=("Arial", 8, "italic"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            justify='left'
        )
        label_nota.grid(row=row, column=0, columnspan=2, pady=(20, 10))
        
        row += 1
        
        # Botones
        frame_botones = tk.Frame(frame_form, bg=COLOR_BLANCO)
        frame_botones.grid(row=row, column=0, columnspan=2, pady=20)
        
        btn_probar = tk.Button(
            frame_botones,
            text="🔌 Probar Conexión",
            font=("Arial", 10, "bold"),
            bg=COLOR_INFO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.probar_conexion,
            width=18
        )
        btn_probar.pack(side=tk.LEFT, padx=5, ipady=8)
        
        btn_guardar = tk.Button(
            frame_botones,
            text="💾 Guardar",
            font=("Arial", 10, "bold"),
            bg=COLOR_EXITO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.guardar_configuracion,
            width=15
        )
        btn_guardar.pack(side=tk.LEFT, padx=5, ipady=8)
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="❌ Cancelar",
            font=("Arial", 10, "bold"),
            bg=COLOR_TEXTO,
            fg=COLOR_BLANCO,
            cursor="hand2",
            command=self.ventana.destroy,
            width=15
        )
        btn_cancelar.pack(side=tk.LEFT, padx=5, ipady=8)
        
        # Configurar grid
        frame_form.columnconfigure(1, weight=1)
    
    def cargar_configuracion_actual(self):
        """Carga la configuración actual desde .env"""
        try:
            if os.path.exists('.env'):
                with open('.env', 'r', encoding='utf-8') as f:
                    for linea in f:
                        linea = linea.strip()
                        if '=' in linea and not linea.startswith('#'):
                            clave, valor = linea.split('=', 1)
                            clave = clave.strip()
                            valor = valor.strip()
                            
                            if clave == 'DB_HOST':
                                self.var_host.set(valor)
                            elif clave == 'DB_PORT':
                                self.var_port.set(valor)
                            elif clave == 'DB_USER':
                                self.var_user.set(valor)
                            elif clave == 'DB_PASSWORD':
                                self.var_password.set(valor)
                            elif clave == 'DB_NAME':
                                self.var_database.set(valor)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar configuración:\n{str(e)}")
    
    def probar_conexion(self):
        """Prueba la conexión con los datos ingresados"""
        if not self.validar_campos():
            return
        
        try:
            import pymysql
            
            conexion = pymysql.connect(
                host=self.var_host.get(),
                port=int(self.var_port.get()),
                user=self.var_user.get(),
                password=self.var_password.get(),
                database=self.var_database.get(),
                charset='utf8mb4'
            )
            conexion.close()
            
            messagebox.showinfo(
                "✅ Conexión Exitosa",
                "La conexión a la base de datos fue exitosa."
            )
            
        except Exception as e:
            messagebox.showerror(
                "❌ Error de Conexión",
                f"No se pudo conectar a la base de datos:\n\n{str(e)}"
            )
    
    def validar_campos(self):
        """Valida que todos los campos estén llenos"""
        if not validar_campo_vacio(self.var_host.get(), "Host"):
            return False
        if not validar_campo_vacio(self.var_port.get(), "Puerto"):
            return False
        if not validar_campo_vacio(self.var_user.get(), "Usuario"):
            return False
        if not validar_campo_vacio(self.var_password.get(), "Contraseña"):
            return False
        if not validar_campo_vacio(self.var_database.get(), "Base de Datos"):
            return False
        
        # Validar que el puerto sea numérico
        try:
            int(self.var_port.get())
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número")
            return False
        
        return True
    
    def guardar_configuracion(self):
        """Guarda la configuración en el archivo .env"""
        if not self.validar_campos():
            return
        
        try:
            # Leer el archivo .env actual
            lineas = []
            if os.path.exists('.env'):
                with open('.env', 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
            
            # Actualizar valores
            nuevas_lineas = []
            claves_actualizadas = set()
            
            for linea in lineas:
                linea_strip = linea.strip()
                if '=' in linea_strip and not linea_strip.startswith('#'):
                    clave = linea_strip.split('=', 1)[0].strip()
                    
                    if clave == 'DB_HOST':
                        nuevas_lineas.append(f"DB_HOST={self.var_host.get()}\n")
                        claves_actualizadas.add('DB_HOST')
                    elif clave == 'DB_PORT':
                        nuevas_lineas.append(f"DB_PORT={self.var_port.get()}\n")
                        claves_actualizadas.add('DB_PORT')
                    elif clave == 'DB_USER':
                        nuevas_lineas.append(f"DB_USER={self.var_user.get()}\n")
                        claves_actualizadas.add('DB_USER')
                    elif clave == 'DB_PASSWORD':
                        nuevas_lineas.append(f"DB_PASSWORD={self.var_password.get()}\n")
                        claves_actualizadas.add('DB_PASSWORD')
                    elif clave == 'DB_NAME':
                        nuevas_lineas.append(f"DB_NAME={self.var_database.get()}\n")
                        claves_actualizadas.add('DB_NAME')
                    else:
                        nuevas_lineas.append(linea)
                else:
                    nuevas_lineas.append(linea)
            
            # Agregar claves que no existían
            if 'DB_HOST' not in claves_actualizadas:
                nuevas_lineas.append(f"DB_HOST={self.var_host.get()}\n")
            if 'DB_PORT' not in claves_actualizadas:
                nuevas_lineas.append(f"DB_PORT={self.var_port.get()}\n")
            if 'DB_USER' not in claves_actualizadas:
                nuevas_lineas.append(f"DB_USER={self.var_user.get()}\n")
            if 'DB_PASSWORD' not in claves_actualizadas:
                nuevas_lineas.append(f"DB_PASSWORD={self.var_password.get()}\n")
            if 'DB_NAME' not in claves_actualizadas:
                nuevas_lineas.append(f"DB_NAME={self.var_database.get()}\n")
            
            # Guardar archivo
            with open('.env', 'w', encoding='utf-8') as f:
                f.writelines(nuevas_lineas)
            
            messagebox.showinfo(
                "✅ Configuración Guardada",
                "La configuración se guardó correctamente.\n\n"
                "⚠️ Reinicie la aplicación para aplicar los cambios."
            )
            
            self.ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración:\n{str(e)}")
