# Guía: Personalizar Banners por Cliente

## Estructura

Los banners están organizados en la carpeta `banners/` y cada uno es un archivo Python independiente.

```
AGENT/
├── banners/
│   ├── __init__.py          # Gestor de banners
│   ├── default.py           # Banner por defecto (Rafa's Agent)
│   └── example_client.py    # Ejemplo de banner personalizado
└── agent_gpt4.py            # Agente principal
```

## Cómo crear un banner personalizado

1. **Copia** `banners/example_client.py` a un nuevo archivo:
   ```bash
   cp banners/example_client.py banners/mi_cliente.py
   ```

2. **Personaliza** el archivo con:
   - `BANNER_CONFIG`: Nombre, versión, colores
   - `BANNER_TOP`: Primera parte del ASCII art
   - `BANNER_BOTTOM`: Segunda parte del ASCII art
   - Funciones `get_banner_lines()` y `get_title()`

3. **Usa** el banner personalizado:
   ```bash
   ./start_demo.sh --custom mi_cliente
   ```

## Ejemplo: Cambiar colores

En tu archivo `banners/mi_cliente.py`:

```python
BANNER_CONFIG = {
    "name": "Mi Empresa AI Agent",
    "version": "v2.0",
    "color_primary": COLORS["GREEN"],      # Verde en lugar de naranja
    "color_secondary": COLORS["MAGENTA"],  # Magenta en lugar de cyan
    "show_info": True,
}
```

## Colores disponibles

```python
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
```

## Crear ASCII Art personalizado

Usa un generador online:
- http://www.patorjk.com/software/taag/
- Copia el texto generado en `BANNER_TOP` y `BANNER_BOTTOM`

## Comandos útiles

```bash
# Usar banner por defecto
./start_demo.sh

# Usar banner personalizado
./start_demo.sh --custom mi_cliente

# Listar banners disponibles
python agent_gpt4.py --list-banners

# Con otras opciones
./start_demo.sh --custom mi_cliente --debug --force-auth
```

## Estructura de un banner

Todo archivo de banner debe tener:

```python
"""Descripción del banner"""

COLORS = { ... }              # Códigos ANSI de colores

BANNER_CONFIG = {
    "name": str,              # Nombre a mostrar
    "version": str,           # Versión
    "color_primary": str,     # Color ANSI del banner
    "color_secondary": str,   # Color ANSI del título
    "show_info": bool,        # Mostrar info del sistema
}

BANNER_TOP = [...]            # Lista de strings (líneas superiores)
BANNER_BOTTOM = [...]         # Lista de strings (líneas inferiores)

def get_banner_lines(name=None, version=None, color=None):
    """Retorna lista de líneas formateadas con colores"""
    ...

def get_title(name=None, version=None, color=None, color_secondary=None):
    """Retorna título formateado"""
    ...
```

## Ejemplos de personalización

### Banner minimalista
```python
BANNER_TOP = [
    "╔════════════════════╗",
    "║   TU EMPRESA       ║",
    "║   AI Agent v1.0    ║",
    "╚════════════════════╝",
]
BANNER_BOTTOM = []
```

### Banner con colores degradados
```python
BANNER_TOP = [
    f"{COLORS['RED']}{ascii_line_1}",
    f"{COLORS['YELLOW']}{ascii_line_2}",
    f"{COLORS['GREEN']}{ascii_line_3}",
]
```

---

**Nota:** Los cambios a los banners se aplican inmediatamente sin necesidad de reiniciar el servidor.
