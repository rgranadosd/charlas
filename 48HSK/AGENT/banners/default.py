"""
Banner default para Rafa's Agent
Personalizable por cliente cambiando colores y texto
"""

# Códigos ANSI para colores
COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "DIM": "\033[2m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "CYAN": "\033[36m",
    "ORANGE": "\033[38;5;208m",
}

# Configuración personalizable
BANNER_CONFIG = {
    "name": "Rafa's Agent",
    "version": "v2.5 FINAL",
    "color_primary": COLORS["ORANGE"],
    "color_secondary": COLORS["CYAN"],
    "show_info": True,
}

# ASCII Art del banner - RAFA'S (arriba)
BANNER_TOP = [
    "██████╗  █████╗ ███████╗ █████╗     ███████╗",
    "██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔════╝",
    "██████╔╝███████║█████╗  ███████║    ███████╗",
    "██╔══██╗██╔══██║██╔══╝  ██╔══██║    ╚════██║",
    "██║  ██║██║  ██║██║     ██║  ██║    ███████║",
    "╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝    ╚══════╝",
]

# ASCII Art del banner - AGENT (abajo)
BANNER_BOTTOM = [
    "  █████╗  ██████╗ ███████╗███╗   ██╗████████╗",
    " ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝",
    " ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ",
    " ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ",
    " ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ",
    " ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ",
]


def get_banner_lines(name=None, version=None, color=None):
    """
    Genera las líneas del banner con colores aplicados.
    
    Args:
        name: Nombre personalizado (por defecto: config)
        version: Versión personalizada (por defecto: config)
        color: Color ANSI personalizado (por defecto: config)
    
    Returns:
        Lista de líneas del banner formateadas
    """
    name = name or BANNER_CONFIG["name"]
    version = version or BANNER_CONFIG["version"]
    color = color or BANNER_CONFIG["color_primary"]
    bold = COLORS["BOLD"]
    reset = COLORS["RESET"]
    
    # Combinar top y bottom
    banner_art = BANNER_TOP + BANNER_BOTTOM
    
    # Aplicar color y formato
    formatted_lines = [f"{color}{bold}{line}{reset}" for line in banner_art]
    
    return formatted_lines


def get_title(name=None, version=None, color=None, color_secondary=None):
    """
    Genera el título formateado.
    
    Args:
        name: Nombre personalizado
        version: Versión personalizada
        color: Color principal
        color_secondary: Color secundario para la versión
    
    Returns:
        Título formateado con colores
    """
    name = name or BANNER_CONFIG["name"]
    version = version or BANNER_CONFIG["version"]
    color = color or BANNER_CONFIG["color_primary"]
    color_secondary = color_secondary or BANNER_CONFIG["color_secondary"]
    bold = COLORS["BOLD"]
    reset = COLORS["RESET"]
    
    return f"{color}{bold}{name}{reset} {color_secondary}{version}{reset}"
