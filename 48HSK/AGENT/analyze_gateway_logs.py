#!/usr/bin/env python3
"""
Analizar logs de APIM para obtener estadísticas de consumo
"""
import re
from collections import defaultdict
from datetime import datetime
import glob

log_files = glob.glob('/Users/rafagranados/Develop/wso2/wso2am-4.6.0/repository/logs/http_access_*.log')

if not log_files:
    print("❌ No se encontraron logs de acceso HTTP")
    exit(1)

stats = {
    'shopify': defaultdict(int),
    'openai': defaultdict(int),
    'total_requests': 0
}

print("📊 Analizando logs de acceso del Gateway...\n")

for log_file in log_files:
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Formato típico: IP - - [fecha] "METHOD /path HTTP/1.1" STATUS SIZE
                if '/shopify/' in line or '/openaiapi/' in line:
                    stats['total_requests'] += 1
                    
                    # Detectar API
                    if '/shopify/' in line:
                        api = 'shopify'
                    else:
                        api = 'openai'
                    
                    # Extraer status code
                    match = re.search(r'" (\d{3}) ', line)
                    if match:
                        status = match.group(1)
                        stats[api][f'status_{status}'] += 1
                    
                    # Detectar método HTTP
                    match = re.search(r'"(GET|POST|PUT|DELETE|PATCH)', line)
                    if match:
                        method = match.group(1)
                        stats[api][f'method_{method}'] += 1
    except Exception as e:
        print(f"⚠️  Error leyendo {log_file}: {e}")

print("=" * 60)
print("📦 SHOPIFY API")
print("=" * 60)
print(f"Total requests: {sum(v for k,v in stats['shopify'].items() if k.startswith('status_'))}")
print("\nPor método:")
for k, v in stats['shopify'].items():
    if k.startswith('method_'):
        print(f"  {k.replace('method_', '')}: {v}")
print("\nPor status:")
for k, v in stats['shopify'].items():
    if k.startswith('status_'):
        print(f"  {k.replace('status_', '')}: {v}")

print("\n" + "=" * 60)
print("🤖 OPENAI API")
print("=" * 60)
print(f"Total requests: {sum(v for k,v in stats['openai'].items() if k.startswith('status_'))}")
print("\nPor método:")
for k, v in stats['openai'].items():
    if k.startswith('method_'):
        print(f"  {k.replace('method_', '')}: {v}")
print("\nPor status:")
for k, v in stats['openai'].items():
    if k.startswith('status_'):
        print(f"  {k.replace('status_', '')}: {v}")

print("\n" + "=" * 60)
print(f"📊 TOTAL: {stats['total_requests']} requests procesados")
print("=" * 60)
print("\n💡 Para monitoreo en tiempo real ejecuta:")
print("   ./monitor_gateway.sh")
