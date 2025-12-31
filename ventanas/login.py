"""
Ventana de Login y Kardex del Sistema de Inventario
"""
import tkinter as tk
from tkinter import ttk, messagebox
from clases.usuarios import Usuario
from ventanas.ventana_principal import VentanaPrincipal
from utilis import centrar_ventana, hashear_password
from constantes import *

class VentanaLogin:
    """Ventana de inicio de sesión"""
    
    def __init__(self, root):
        self.root = root
        self.ventana = tk.Toplevel(root)
        self.ventana.title(f"{APP_NOMBRE} - Login")
        self.ventana.geometry("400x500")
        self.ventana.resizable(False, False)
        centrar_ventana(self.ventana, 400, 500)
        
        # Variables
        self.var_usuario = tk.StringVar()
        self.var_password = tk.StringVar()
        self.intentos = 0
        
        # Configurar ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # Crear interfaz
        self.crear_widgets()
        
        # Foco en campo usuario
        self.entry_usuario.focus()
        
    def crear_widgets(self):
        """Crea los widgets de la interfaz"""
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Logo / Título
        frame_header = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_header.pack(pady=(0, 30))
        
        # Icono (puedes agregar una imagen aquí)
        label_icono = tk.Label(
            frame_header,
            text="📦",
            font=("Arial", 48),
            bg=COLOR_FONDO
        )
        label_icono.pack()
        
        label_titulo = tk.Label(
            frame_header,
            text=APP_NOMBRE,
            font=("Arial", 16, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_PRIMARIO
        )
        label_titulo.pack()
        
        label_subtitulo = tk.Label(
            frame_header,
            text="Inicie sesión para continuar",
            font=("Arial", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        label_subtitulo.pack()
        
        # Frame del formulario
        frame_form = tk.Frame(frame_principal, bg=COLOR_BLANCO, relief=tk.RAISED, bd=1)
        frame_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Padding interno
        frame_interno = tk.Frame(frame_form, bg=COLOR_BLANCO)
        frame_interno.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Campo Usuario
        label_usuario = tk.Label(
            frame_interno,
            text="Usuario:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            anchor='w'
        )
        label_usuario.pack(fill=tk.X, pady=(10, 5))
        
        self.entry_usuario = ttk.Entry(
            frame_interno,
            textvariable=self.var_usuario,
            font=("Arial", 11)
        )
        self.entry_usuario.pack(fill=tk.X, ipady=8)
        
        # Campo Contraseña
        label_password = tk.Label(
            frame_interno,
            text="Contraseña:",
            font=("Arial", 10, "bold"),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            anchor='w'
        )
        label_password.pack(fill=tk.X, pady=(20, 5))
        
        self.entry_password = ttk.Entry(
            frame_interno,
            textvariable=self.var_password,
            font=("Arial", 11),
            show="●"
        )
        self.entry_password.pack(fill=tk.X, ipady=8)
        
        # Bind Enter key
        self.entry_password.bind('<Return>', lambda e: self.iniciar_sesion())
        
        # Botón Iniciar Sesión
        self.btn_login = tk.Button(
            frame_interno,
            text="INICIAR SESIÓN",
            font=("Arial", 11, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.iniciar_sesion
        )
        self.btn_login.pack(fill=tk.X, pady=(30, 10), ipady=10)
        
        # Efecto hover en botón
        self.btn_login.bind('<Enter>', lambda e: self.btn_login.config(bg="#2980B9"))
        self.btn_login.bind('<Leave>', lambda e: self.btn_login.config(bg=COLOR_SECUNDARIO))
        
        # Footer
        frame_footer = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_footer.pack(side=tk.BOTTOM, pady=(10, 0))
        
        label_version = tk.Label(
            frame_footer,
            text=f"Versión {APP_VERSION}",
            font=("Arial", 8),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        label_version.pack()
        
    def iniciar_sesion(self):
        """Valida credenciales e inicia sesión"""
        
        usuario = self.var_usuario.get().strip()
        password = self.var_password.get()
        
        # Validar campos vacíos
        if not usuario or not password:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor ingrese usuario y contraseña"
            )
            return
        
        # Verificar credenciales
        try:
            usuario_obj = Usuario.autenticar(usuario, password)
            
            if usuario_obj:
                # Verificar si está activo
                if not usuario_obj.activo:
                    messagebox.showerror(
                        "Usuario inactivo",
                        MENSAJES['usuario_inactivo']
                    )
                    return
                
                # Actualizar último acceso
                Usuario.actualizar_ultimo_acceso(usuario_obj.id)
                
                # Verificar si debe cambiar password
                if usuario_obj.debe_cambiar_password:
                    messagebox.showinfo(
                        "Cambio de contraseña",
                        "Debe cambiar su contraseña en el primer inicio de sesión"
                    )
                    self.mostrar_cambio_password(usuario_obj)
                    return
                
                # Login exitoso
                messagebox.showinfo(
                    "Bienvenido",
                    f"¡Bienvenido {usuario_obj.nombre_completo}!"
                )
                
                # Cerrar ventana de login y abrir principal
                self.abrir_ventana_principal(usuario_obj)
                
            else:
                self.intentos += 1
                intentos_restantes = MAX_INTENTOS_LOGIN - self.intentos
                
                if self.intentos >= MAX_INTENTOS_LOGIN:
                    messagebox.showerror(
                        "Acceso bloqueado",
                        "Ha excedido el número máximo de intentos"
                    )
                    self.cerrar_aplicacion()
                else:
                    messagebox.showerror(
                        "Error de login",
                        f"{MENSAJES['login_fallido']}\n"
                        f"Intentos restantes: {intentos_restantes}"
                    )
                    self.var_password.set("")
                    
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al iniciar sesión:\n{str(e)}"
            )
    
    def mostrar_cambio_password(self, usuario):
        """Muestra ventana para cambiar contraseña"""
        ventana_cambio = tk.Toplevel(self.ventana)
        ventana_cambio.title("Cambiar Contraseña")
        ventana_cambio.geometry("400x300")
        ventana_cambio.resizable(False, False)
        centrar_ventana(ventana_cambio, 400, 300)
        ventana_cambio.grab_set()
        
        frame = tk.Frame(ventana_cambio, bg=COLOR_BLANCO)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Variables
        var_nueva = tk.StringVar()
        var_confirmar = tk.StringVar()
        
        # Título
        label_titulo = tk.Label(
            frame,
            text="Cambiar Contraseña",
            font=("Arial", 14, "bold"),
            bg=COLOR_BLANCO
        )
        label_titulo.pack(pady=(0, 20))
        
        # Nueva contraseña
        tk.Label(frame, text="Nueva contraseña:", bg=COLOR_BLANCO).pack(anchor='w')
        entry_nueva = ttk.Entry(frame, textvariable=var_nueva, show="●")
        entry_nueva.pack(fill=tk.X, pady=(5, 15), ipady=5)
        
        # Confirmar contraseña
        tk.Label(frame, text="Confirmar contraseña:", bg=COLOR_BLANCO).pack(anchor='w')
        entry_confirmar = ttk.Entry(frame, textvariable=var_confirmar, show="●")
        entry_confirmar.pack(fill=tk.X, pady=(5, 20), ipady=5)
        
        def cambiar():
            nueva = var_nueva.get()
            confirmar = var_confirmar.get()
            
            if not nueva or not confirmar:
                messagebox.showwarning("Error", "Complete todos los campos")
                return
            
            if len(nueva) < MIN_LONGITUD_PASSWORD:
                messagebox.showwarning(
                    "Error",
                    f"La contraseña debe tener al menos {MIN_LONGITUD_PASSWORD} caracteres"
                )
                return
            
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            
            # Actualizar contraseña
            try:
                nuevo_hash = hashear_password(nueva)
                Usuario.cambiar_password(usuario.id, nuevo_hash)
                messagebox.showinfo("Éxito", "Contraseña actualizada correctamente")
                ventana_cambio.destroy()
                self.abrir_ventana_principal(usuario)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cambiar contraseña:\n{str(e)}")
        
        # Botón cambiar
        btn_cambiar = tk.Button(
            frame,
            text="Cambiar Contraseña",
            bg=COLOR_SECUNDARIO,
            fg=COLOR_BLANCO,
            command=cambiar
        )
        btn_cambiar.pack(fill=tk.X, ipady=8)
        
    def abrir_ventana_principal(self, usuario):
        """Abre la ventana principal del sistema"""
        self.ventana.destroy()
        VentanaPrincipal(self.root, usuario)
        
    def cerrar_aplicacion(self):
        """Cierra la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.root.quit()