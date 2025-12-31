"""
Sistema de Temas para el Sistema de Inventario
Gestiona temas claro y oscuro
"""
import json
import os

# ============================================
# TEMA CLARO (Por defecto)
# ============================================
TEMA_CLARO = {
    'COLOR_PRIMARIO': "#2C3E50",
    'COLOR_SECUNDARIO': "#3498DB",
    'COLOR_EXITO': "#27AE60",
    'COLOR_PELIGRO': "#E74C3C",
    'COLOR_ADVERTENCIA': "#F39C12",
    'COLOR_INFO': "#3498DB",
    'COLOR_FONDO': "#ECF0F1",
    'COLOR_TEXTO': "#2C3E50",
    'COLOR_BLANCO': "#FFFFFF",
    'nombre': 'claro'
}

# ============================================
# TEMA OSCURO
# ============================================
TEMA_OSCURO = {
    'COLOR_PRIMARIO': "#5dade2",      # Celeste claro para títulos de ventanas
    'COLOR_SECUNDARIO': "#5dade2",    # Celeste claro para botones
    'COLOR_EXITO': "#81c995",         # Verde brillante
    'COLOR_PELIGRO': "#f28b82",       # Rojo brillante
    'COLOR_ADVERTENCIA': "#fdd663",   # Amarillo brillante
    'COLOR_INFO': "#78d9ec",          # Cyan brillante
    'COLOR_FONDO': "#2b2b2b",         # Fondo gris oscuro (no tan oscuro)
    'COLOR_TEXTO': "#ffffff",         # Blanco para labels
    'COLOR_BLANCO': "#3a3a3a",        # Fondo de widgets (gris medio-oscuro)
    'nombre': 'oscuro'
}

# Archivo de configuración
CONFIG_FILE = "config_usuario.json"

def cargar_config_usuario():
    """Carga la configuración del usuario"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # Configuración por defecto
    return {
        "tema": "claro",
        "imagen_fondo": None,
        "mostrar_marca_agua": True
    }

def guardar_config_usuario(config):
    """Guarda la configuración del usuario"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar configuración: {e}")
        return False

def obtener_tema_actual():
    """Obtiene el tema actual desde la configuración"""
    config = cargar_config_usuario()
    if config.get('tema') == 'oscuro':
        return TEMA_OSCURO
    return TEMA_CLARO

def cambiar_tema(nuevo_tema='claro'):
    """
    Cambia el tema del sistema
    
    Args:
        nuevo_tema: 'claro' o 'oscuro'
    
    Returns:
        dict: El nuevo tema aplicado
    """
    config = cargar_config_usuario()
    config['tema'] = nuevo_tema
    guardar_config_usuario(config)
    
    if nuevo_tema == 'oscuro':
        return TEMA_OSCURO
    return TEMA_CLARO

def alternar_tema():
    """Alterna entre tema claro y oscuro"""
    config = cargar_config_usuario()
    tema_actual = config.get('tema', 'claro')
    nuevo_tema = 'oscuro' if tema_actual == 'claro' else 'claro'
    return cambiar_tema(nuevo_tema)

def obtener_nombre_tema():
    """Obtiene el nombre del tema actual"""
    config = cargar_config_usuario()
    return config.get('tema', 'claro')

# Aplicar tema al importar
TEMA_ACTUAL = obtener_tema_actual()
