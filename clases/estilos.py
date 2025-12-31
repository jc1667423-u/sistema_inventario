"""
Módulo de Estilos para el Sistema de Inventario
Centraliza la configuración de la apariencia de la aplicación (ttk.Style)
"""
import tkinter as tk
from tkinter import ttk
from constantes import *

def configurar_estilos(root):
    """
    Configura los estilos globales de la aplicación utilizando ttk.Style
    Adapta los colores según el tema actual (Claro/Oscuro)
    """
    style = ttk.Style(root)
    
    # Intentar usar tema 'clam' como base por ser más moderno/configurable
    # Si no existe, usar 'alt' o 'default'
    temas_disponibles = style.theme_names()
    if 'clam' in temas_disponibles:
        style.theme_use('clam')
    elif 'alt' in temas_disponibles:
        style.theme_use('alt')
        
    # Colores definidos en constantes.py (que carga el tema actual)
    bg_color = COLOR_BLANCO
    bg_fondo = COLOR_FONDO
    fg_color = COLOR_TEXTO
    primary = COLOR_PRIMARIO
    secondary = COLOR_SECUNDARIO
    
    # ----------------------------------------------------
    # Configuración General
    # ----------------------------------------------------
    
    # Configurar TFrame (contenedores)
    style.configure("TFrame", 
                    background=bg_fondo)
    
    # Configurar TLable (etiquetas)
    style.configure("TLabel", 
                    background=bg_fondo, 
                    foreground=fg_color,
                    font=("Segoe UI", 10))
    
    style.configure("Titulo.TLabel",
                    background=bg_fondo,
                    foreground=primary,
                    font=("Segoe UI", 16, "bold"))
                    
    style.configure("Subtitulo.TLabel",
                    background=bg_fondo,
                    foreground=primary, 
                    font=("Segoe UI", 12, "bold"))
                    
    style.configure("Error.TLabel",
                    background=bg_fondo,
                    foreground=COLOR_PELIGRO,
                    font=("Segoe UI", 9))
    
    # ----------------------------------------------------
    # Botones (TButton)
    # ----------------------------------------------------
    style.configure("TButton", 
                    background=secondary, 
                    foreground="#FFFFFF" if obtener_nombre_tema() == 'claro' else "#000000",
                    font=("Segoe UI", 10, "bold"),
                    borderwidth=1,
                    focusthickness=3,
                    focuscolor=primary,
                    padding=6)
                    
    style.map("TButton", 
              background=[('active', primary), ('disabled', '#cccccc')],
              foreground=[('disabled', '#666666')])
              
    # Botón Principal (Primary)
    style.configure("Primary.TButton",
                    background=primary,
                    foreground="#FFFFFF")
    
    # Botón de Peligro (Danger)
    style.configure("Danger.TButton",
                    background=COLOR_PELIGRO,
                    foreground="#FFFFFF")
                    
    # ----------------------------------------------------
    # Entradas de texto (TEntry)
    # ----------------------------------------------------
    style.configure("TEntry", 
                    fieldbackground=bg_color,
                    foreground=fg_color,
                    insertcolor=fg_color, # Color del cursor
                    borderwidth=1,
                    relief="solid")
                    
    # ----------------------------------------------------
    # Combobox (TCombobox)
    # ----------------------------------------------------
    style.configure("TCombobox",
                    fieldbackground=bg_color,
                    background=bg_color,
                    foreground=fg_color,
                    arrowcolor=fg_color,
                    borderwidth=1,
                    relief="solid")
                    
    style.map("TCombobox", 
              fieldbackground=[('readonly', bg_color)],
              selectbackground=[('readonly', primary)],
              selectforeground=[('readonly', '#FFFFFF')])
              
    # ----------------------------------------------------
    # Tablas (Treeview)
    # ----------------------------------------------------
    style.configure("Treeview", 
                    background=bg_color, 
                    foreground=fg_color, 
                    fieldbackground=bg_color,
                    borderwidth=0,
                    rowheight=30,
                    font=("Segoe UI", 10))
                    
    style.configure("Treeview.Heading", 
                    background=primary, 
                    foreground="#FFFFFF" if obtener_nombre_tema() == 'claro' else "#000000",
                    relief="flat",
                    font=("Segoe UI", 10, "bold"),
                    padding=10)
                    
    style.map("Treeview.Heading",
              background=[('active', secondary)])
              
    style.map("Treeview", 
              background=[('selected', secondary)], 
              foreground=[('selected', '#FFFFFF' if obtener_nombre_tema() == 'claro' else '#000000')])
              
    # ----------------------------------------------------
    # Scrollbars
    # ----------------------------------------------------
    style.configure("Vertical.TScrollbar",
                    background=bg_fondo,
                    troughcolor=bg_color,
                    bordercolor=bg_fondo,
                    arrowcolor=fg_color)
    
    # Configurar fondo global de la ventana raíz si es necesario
    try:
        root.configure(bg=bg_fondo)
    except:
        pass
        
    return style

def obtener_nombre_tema():
    """Helper para obtener nombre del tema (evita import circular)"""
    try:
        from temas import obtener_nombre_tema as get_tema
        return get_tema()
    except:
        return 'claro'
