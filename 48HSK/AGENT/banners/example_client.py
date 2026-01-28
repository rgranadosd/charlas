"""
Banner personalizado - EJEMPLO CLIENTE
Cambia los colores y el texto según tus necesidades
"""

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
    "MAGENTA": "\033[35m",
    "LIGHT_BLUE": "\033[38;5;51m",
}

# Configuración personalizable
BANNER_CONFIG = {
    "name": "Mi Cliente Agent",
    "version": "v1.0 BETA",
    "color_primary": COLORS["CYAN"],
    "color_secondary": COLORS["LIGHT_BLUE"],
    "show_info": True,
}

# ASCII Art - Personalizado para el cliente
BANNER_TOP = [
    " ███╗   ███╗██╗     ██████╗ ██╗      █████╗  ██████╗███████╗",
    " ████╗ ████║██║     ██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝",
    " ██╔████╔██║██║     ██║  ███╗██║     ███████║██║     █████╗  ",
    " ██║╚██╔╝██║██║     ██║   ██║██║     ██╔══██║██║     ██╔══╝  ",
    " ██║ ╚═╝ ██║███████╗╚██████╔╝███████╗██║  ██║╚██████╗███████╗",
    " ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝",
]

BANNER_BOTTOM = [
    "      █████╗  ██████╗ ███████╗███╗   ██╗████████╗",
    "     ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝",
    "     ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ",
    "     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ",
    "     ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ",
    "     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ",
]


def get_banner_lines(name=None, version=None, color=None):
    """Genera las líneas del banner con colores aplicados."""
    name = name or BANNER_CONFIG["name"]
    version = version or BANNER_CONFIG["version"]
    color = color or BANNER_CONFIG["color_primary"]
    bold = COLORS["BOLD"]
    reset = COLORS["RESET"]
    
    banner_art = BANNER_TOP + BANNER_BOTTOM
    formatted_lines = [f"{color}{bold}{line}{reset}" for line in banner_art]
    
    return formatted_lines


def get_title(name=None, version=None, color=None, color_secondary=None):
    """Genera el título formateado."""
    name = name or BANNER_CONFIG["name"]
    version = version or BANNER_CONFIG["version"]
    color = color or BANNER_CONFIG["color_primary"]
    color_secondary = color_secondary or BANNER_CONFIG["color_secondary"]
    bold = COLORS["BOLD"]
    reset = COLORS["RESET"]
    
    return f"{color}{bold}{name}{reset} {color_secondary}{version}{reset}"
