"""
Gestor de banners personalizables
Carga y renderiza banners dinámicamente según el cliente
"""

import os
import importlib.util
from pathlib import Path


def load_banner_module(banner_name="default"):
    """
    Carga un módulo de banner dinámicamente.
    
    Args:
        banner_name: Nombre del banner (sin .py)
        
    Returns:
        Módulo del banner o None si no existe
    """
    banners_dir = Path(__file__).parent
    banner_file = banners_dir / f"{banner_name}.py"
    
    if not banner_file.exists():
        print(f"Banner '{banner_name}' no encontrado. Usando 'default'")
        banner_file = banners_dir / "default.py"
    
    if not banner_file.exists():
        raise FileNotFoundError(f"Banner por defecto no encontrado en {banner_file}")
    
    spec = importlib.util.spec_from_file_location(f"banner_{banner_name}", banner_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module


def get_banner(banner_name="default", custom_name=None, custom_version=None, custom_color=None):
    """
    Obtiene el banner formateado.
    
    Args:
        banner_name: Nombre del archivo de banner a usar
        custom_name: Nombre personalizado para reemplazar
        custom_version: Versión personalizada para reemplazar
        custom_color: Color ANSI personalizado
        
    Returns:
        Diccionario con 'lines' y 'title'
    """
    banner_module = load_banner_module(banner_name)
    
    # Obtener funciones del módulo
    get_banner_lines_fn = getattr(banner_module, "get_banner_lines")
    get_title_fn = getattr(banner_module, "get_title")
    
    lines = get_banner_lines_fn(name=custom_name, version=custom_version, color=custom_color)
    title = get_title_fn(name=custom_name, version=custom_version, color=custom_color)
    
    return {
        "lines": lines,
        "title": title,
    }


def list_available_banners():
    """
    Lista todos los banners disponibles.
    
    Returns:
        Lista de nombres de banners disponibles
    """
    banners_dir = Path(__file__).parent
    banners = [f.stem for f in banners_dir.glob("*.py") if f.name != "__init__.py"]
    return sorted(banners)
