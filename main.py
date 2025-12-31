"""
Sistema de Gestión de Inventario
Archivo principal de entrada
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ventanas.login import VentanaLogin
from ventanas.login import VentanaLogin
from base_datos.config_db import verificar_conexion
from clases.estilos import configurar_estilos

class AplicacionInventario:
    """Clase principal que gestiona la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal inicialmente
        
        # Configurar estilos globales
        self.estilo = configurar_estilos(self.root)
        
        self.configurar_aplicacion()
        
    def configurar_aplicacion(self):
        """Configura los parámetros básicos de la aplicación"""
        self.root.title("Sistema de Gestión de Inventario")
        
        # Configurar icono (si existe)
        try:
            if os.path.exists('assets/icono.ico'):
                self.root.iconbitmap('assets/icono.ico')
        except:
            pass
        
        # Centrar ventana en la pantalla
        self.centrar_ventana(400, 300)
        
    def centrar_ventana(self, ancho, alto):
        """Centra la ventana en la pantalla"""
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 2
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def verificar_sistema(self):
        """Verifica que el sistema esté correctamente configurado"""
        try:
            # Verificar conexión a base de datos
            if not verificar_conexion():
                messagebox.showerror(
                    "Error de Conexión",
                    "No se pudo conectar a la base de datos.\n"
                    "Verifique la configuración en config_db.py"
                )
                return False
            
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Error del Sistema",
                f"Error al inicializar el sistema:\n{str(e)}"
            )
            return False
    
    def iniciar_login(self):
        """Inicia la ventana de login"""
        try:
            ventana_login = VentanaLogin(self.root)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al iniciar la ventana de login:\n{str(e)}"
            )
            self.root.quit()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        # Verificar sistema
        if not self.verificar_sistema():
            self.root.quit()
            return
        
        # Iniciar ventana de login
        self.iniciar_login()
        
        # Iniciar loop principal
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        # Crear y ejecutar aplicación
        app = AplicacionInventario()
        app.ejecutar()
        
    except KeyboardInterrupt:
        print("\nAplicación terminada por el usuario")
        sys.exit(0)
        
    except Exception as e:
        messagebox.showerror(
            "Error Fatal",
            f"Error crítico en la aplicación:\n{str(e)}\n\n"
            "La aplicación se cerrará."
        )
        sys.exit(1)

if __name__ == "__main__":
    main()