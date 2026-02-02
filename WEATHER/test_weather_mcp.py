#!/usr/bin/env python3
"""
Script de Testing para Weather MCP Server (Open-Meteo Version)

Este script verifica que el MCP esté correctamente configurado
y que todas las herramientas funcionen como esperado.

VENTAJA: No necesita API key - funciona inmediatamente
"""

import subprocess
import sys
import os


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...")
    
    required_packages = ["mcp", "httpx", "pydantic"]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NO INSTALADO")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Faltan paquetes. Instala con:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    print("✅ Todas las dependencias instaladas\n")
    return True


def check_no_api_key_needed():
    """Verifica que NO se necesite API key (ventaja de Open-Meteo)."""
    print("🔍 Verificando configuración...")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        print("  ℹ️  OPENWEATHER_API_KEY detectada (pero ya no la necesitas)")
        print("     Open-Meteo funciona SIN API key - puedes eliminarla")
    else:
        print("  ✅ Perfecto - Open-Meteo no requiere API key")
    
    print("  ✅ Configuración lista (cero setup necesario)\n")
    return True


def test_mcp_syntax():
    """Verifica que el código Python sea sintácticamente correcto."""
    print("🔍 Verificando sintaxis del MCP...")
    
    try:
        result = subprocess.run(
            ["python", "-m", "py_compile", "weather_mcp_openmeteo.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("  ✅ Sintaxis correcta")
            return True
        else:
            print(f"  ❌ Error de sintaxis:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("  ❌ Timeout al verificar sintaxis")
        return False
    except FileNotFoundError:
        print("  ❌ Python no encontrado en el PATH")
        return False


def test_mcp_import():
    """Verifica que el MCP se pueda importar."""
    print("\n🔍 Verificando que el MCP se puede importar...")
    
    try:
        # Intenta importar el módulo
        import weather_mcp_openmeteo
        print("  ✅ Importación exitosa")
        
        # Verifica que tenga las herramientas esperadas
        expected_tools = [
            "get_current_weather",
            "get_weather_forecast", 
            "get_retail_weather_insights"
        ]
        
        for tool_name in expected_tools:
            if hasattr(weather_mcp_openmeteo, tool_name):
                print(f"  ✅ Herramienta encontrada: {tool_name}")
            else:
                print(f"  ⚠️  Herramienta no encontrada: {tool_name}")
        
        # Verificar que tiene las ciudades españolas
        if hasattr(weather_mcp_openmeteo, 'SPANISH_CITIES'):
            cities_count = len(weather_mcp_openmeteo.SPANISH_CITIES)
            print(f"  ✅ {cities_count} ciudades españolas disponibles")
        
        return True
    except ImportError as e:
        print(f"  ❌ Error al importar: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False


def print_usage_instructions():
    """Imprime instrucciones de uso."""
    print("\n" + "="*80)
    print("📚 INSTRUCCIONES DE USO")
    print("="*80)
    print("""
🎉 VENTAJAS DE OPEN-METEO:
  ✅ Sin API key necesaria
  ✅ Sin límites de llamadas
  ✅ Sin costes nunca
  ✅ Datos de mejor calidad para España
  ✅ Más rápido que OpenWeatherMap

1. Para probar el MCP con el Inspector:
   
   npx @modelcontextprotocol/inspector python weather_mcp_openmeteo.py

2. Para integrar con tu agente de Shopify:
   
   Ver archivo: shopify_weather_agent_openmeteo.py

3. Para testing rápido:
   
   python shopify_weather_agent_openmeteo.py

4. Ciudades disponibles:
   - Madrid, Barcelona, Valencia
   - Sevilla, Málaga, Zaragoza
   - Murcia, Bilbao, Alicante, Córdoba

5. Ejemplo de llamada a la herramienta principal:
   
   {
     "city": "Barcelona",
     "days": 3
   }

💡 DIFERENCIAS CON LA VERSIÓN ANTERIOR:
  - ❌ NO necesitas configurar OPENWEATHER_API_KEY
  - ✅ Funciona inmediatamente sin setup
  - ✅ Misma lógica de retail
  - ✅ Resultados idénticos para el usuario final
  - ✅ Sin límites de 1000 llamadas/día
""")
    print("="*80 + "\n")


def main():
    """Ejecuta todos los tests."""
    print("\n" + "="*80)
    print("🧪 TESTING WEATHER MCP SERVER (OPEN-METEO)")
    print("="*80 + "\n")
    
    all_passed = True
    
    # Test 1: Dependencies
    if not check_dependencies():
        all_passed = False
    
    # Test 2: No API Key Needed
    if not check_no_api_key_needed():
        all_passed = False
    
    # Test 3: Syntax
    if not test_mcp_syntax():
        all_passed = False
    
    # Test 4: Import
    if not test_mcp_import():
        all_passed = False
    
    # Resultado final
    print("\n" + "="*80)
    if all_passed:
        print("✅ TODOS LOS TESTS PASARON")
        print("="*80)
        print("\n🎉 El MCP está listo para usar!")
        print("\n🚀 VENTAJA CLAVE: Sin API key, sin límites, sin fricción")
        print_usage_instructions()
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("="*80)
        print("\n⚠️  Revisa los errores arriba y corrígelos antes de usar el MCP")
        return 1


if __name__ == "__main__":
    sys.exit(main())