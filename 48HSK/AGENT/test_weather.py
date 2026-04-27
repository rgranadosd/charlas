#!/usr/bin/env python3
"""Script de prueba para WeatherPlugin"""
import sys
sys.path.insert(0, '/Users/rafagranados/Develop/charlas/48HSK/AGENT')

from plugins.weather import WeatherPlugin

def test_weather():
    print("Inicializando WeatherPlugin...")
    plugin = WeatherPlugin()
    
    print("\nProbando clima de Barcelona...")
    result = plugin.get_current_weather('barcelona')
    print(f"Resultado: {result}")
    
    print("\nProbando pronóstico de Madrid...")
    result2 = plugin.get_weather_forecast('madrid', 3)
    print(f"Resultado: {result2}")

if __name__ == "__main__":
    test_weather()
