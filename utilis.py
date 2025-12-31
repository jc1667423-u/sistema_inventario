"""
Funciones de utilidad para el sistema
"""
import re
from datetime import datetime
import bcrypt
import tkinter as tk
from tkinter import messagebox

def validar_email(email):
    """Valida formato de email"""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Valida formato de teléfono (solo números y algunos caracteres)"""
    patron = r'^[\d\s\-\+\(\)]+$'
    return re.match(patron, telefono) is not None

def validar_numero(texto):
    """Valida que el texto sea un número válido"""
    try:
        float(texto)
        return True
    except ValueError:
        return False

def validar_entero(texto):
    """Valida que el texto sea un entero válido"""
    try:
        int(texto)
        return True
    except ValueError:
        return False

def formatear_moneda(valor):
    """Formatea un valor numérico como moneda"""
    try:
        return f"S/ {float(valor):,.2f}"
    except:
        return "S/ 0.00"

def formatear_fecha(fecha):
    """Formatea una fecha al formato DD/MM/YYYY"""
    if isinstance(fecha, str):
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d")
            except:
                return fecha
    
    if isinstance(fecha, datetime):
        return fecha.strftime("%d/%m/%Y")
    
    return str(fecha)

def formatear_fecha_hora(fecha):
    """Formatea una fecha con hora al formato DD/MM/YYYY HH:MM"""
    if isinstance(fecha, str):
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        except:
            return fecha
    
    if isinstance(fecha, datetime):
        return fecha.strftime("%d/%m/%Y %H:%M")
    
    return str(fecha)

def hashear_password(password):
    """Genera un hash seguro de la contraseña"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_password(password, password_hash):
    """Verifica si una contraseña coincide con su hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except:
        return False

def centrar_ventana(ventana, ancho, alto):
    """Centra una ventana en la pantalla"""
    ventana.update_idletasks()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def confirmar_accion(titulo, mensaje):
    """Muestra un cuadro de confirmación"""
    return messagebox.askyesno(titulo, mensaje)

def mostrar_error(mensaje):
    """Muestra un mensaje de error"""
    messagebox.showerror("Error", mensaje)

def mostrar_info(mensaje):
    """Muestra un mensaje informativo"""
    messagebox.showinfo("Información", mensaje)

def mostrar_advertencia(mensaje):
    """Muestra un mensaje de advertencia"""
    messagebox.showwarning("Advertencia", mensaje)

def mostrar_exito(mensaje):
    """Muestra un mensaje de éxito"""
    messagebox.showinfo("Éxito", mensaje)

def limpiar_frame(frame):
    """Elimina todos los widgets de un frame"""
    for widget in frame.winfo_children():
        widget.destroy()

def solo_numeros(texto):
    """Valida que solo se ingresen números"""
    return texto.isdigit() or texto == ""

def solo_decimales(texto):
    """Valida que solo se ingresen números decimales"""
    if texto == "":
        return True
    try:
        float(texto)
        return True
    except ValueError:
        return False

def generar_codigo_producto(prefijo="PROD"):
    """Genera un código único para producto"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefijo}-{timestamp}"

def obtener_fecha_actual():
    """Retorna la fecha actual en formato YYYY-MM-DD"""
    return datetime.now().strftime("%Y-%m-%d")

def obtener_fecha_hora_actual():
    """Retorna la fecha y hora actual en formato YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generar_codigo_auto(prefijo="COD"):
    """Genera un código automático con timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefijo}-{timestamp}"

def validar_campo_vacio(valor, nombre_campo):
    """Valida que un campo no esté vacío"""
    if not valor or valor.strip() == "":
        mostrar_error(f"El campo '{nombre_campo}' es obligatorio")
        return False
    return True

def configurar_validacion_numerica(entry):
    """Configura un Entry para que solo acepte números"""
    vcmd = (entry.register(solo_numeros), '%P')
    entry.config(validate='key', validatecommand=vcmd)

def configurar_validacion_decimal(entry):
    """Configura un Entry para que solo acepte decimales"""
    vcmd = (entry.register(solo_decimales), '%P')
    entry.config(validate='key', validatecommand=vcmd)