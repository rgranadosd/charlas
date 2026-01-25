#!/usr/bin/env python3
"""
Obtener credenciales de PRODUCTION
"""
import requests
import os
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings()

load_dotenv()

APIM_USER = os.getenv("WSO2_APIM_USERNAME", "admin")
APIM_PASS = os.getenv("WSO2_APIM_PASSWORD", "admin")

app_id = "9ca65ce1-d679-4254-a37e-c16a94330590"
key_mapping_id = "da679bcb-5a3b-4cf9-b8bb-f928221700b9"  # Production key

# Obtener detalles completos incluyendo el secret
key_details = requests.get(
    f"https://localhost:9453/api/am/devportal/v3/applications/{app_id}/oauth-keys/{key_mapping_id}",
    auth=(APIM_USER, APIM_PASS),
    verify=False
)

print("=" * 60)
print("Credenciales de PRODUCTION")
print("=" * 60)

data = key_details.json()
print(f"Consumer Key: {data.get('consumerKey')}")
print(f"Consumer Secret: {data.get('consumerSecret')}")
print(f"Key Type: {data.get('keyType')}")

print("\n" + "=" * 60)
print("Para actualizar .env, usa estas líneas:")
print("=" * 60)
print(f"WSO2_CONSUMER_KEY={data.get('consumerKey')}")
print(f"WSO2_CONSUMER_SECRET={data.get('consumerSecret')}")
