"""
Banner personalizado - EL CORTE INGLES
Banners ASCII con colores personalizables
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
    "LIGHT_GREEN": "\033[38;5;82m",
    "BRIGHT_GREEN": "\033[92m",
}


# Configuración personalizable
BANNER_CONFIG = {
    "name": "El Corte Inglés",
    "version": "AI Agent v1.0",
    "color_primary": COLORS["RED"],       # Rojo (color corporativo)
    "color_secondary": COLORS["YELLOW"],  # Amarillo
    "show_info": True,
}


# ASCII Art - El Corte Ingles
BANNER_LINES = [
    " ███████╗██╗         ██████╗ ██████╗ ██████╗ ████████╗███████╗",
    " ██╔════╝██║        ██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝",
    " █████╗  ██║        ██║     ██║   ██║██████╔╝   ██║   █████╗  ",
    " ██╔══╝  ██║        ██║     ██║   ██║██╔══██╗   ██║   ██╔══╝  ",
    " ███████╗███████╗   ╚██████╗╚██████╔╝██║  ██║   ██║   ███████╗",
    " ╚══════╝╚══════╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝",
    "",
    " ██╗███╗   ██╗ ██████╗ ██╗     ███████╗███████╗",
    " ██║████╗  ██║██╔════╝ ██║     ██╔════╝██╔════╝",
    " ██║██╔██╗ ██║██║  ███╗██║     █████╗  ███████╗",
    " ██║██║╚██╗██║██║   ██║██║     ██╔══╝  ╚════██║",
    " ██║██║ ╚████║╚██████╔╝███████╗███████╗███████║",
    " ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝",
]


def get_banner_lines(name=None, version=None, color=None):
    """Genera las líneas del banner con colores aplicados."""
    color = color or BANNER_CONFIG["color_primary"]
    bold = COLORS["BOLD"]
    reset = COLORS["RESET"]

    formatted_lines = [f"{color}{bold}{line}{reset}" for line in BANNER_LINES]

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


def print_banner():
    """Imprime el banner completo."""
    print()
    for line in get_banner_lines():
        print(line)
    print()
    print(f"  {get_title()}")
    print()


if __name__ == "__main__":
    print_banner()
