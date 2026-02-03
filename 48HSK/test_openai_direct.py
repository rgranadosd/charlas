import urllib.request
import json
import ssl

# Clave nueva proporcionada
api_key = "YOUR_OPENAI_API_KEY"
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "Python-Test-Script"
}

data = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "user", "content": "Hola, responde solo con: 'Conexión directa exitosa'"}
    ],
    "max_tokens": 50
}

print(f"📡 Probando conexión directa a OpenAI ({url})...")

try:
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    
    # Contexto SSL por defecto
    context = ssl.create_default_context()
    
    with urllib.request.urlopen(req, context=context) as response:
        status_code = response.getcode()
        response_body = response.read().decode('utf-8')
        print(f"Status Code: {status_code}")
        print(json.dumps(json.loads(response_body), indent=2))
        print("\n✅ La clave FUNCIONA correctamente.")

except urllib.error.HTTPError as e:
    print(f"Status Code: {e.code}")
    print(e.read().decode('utf-8'))
    if e.code == 429:
        print("\n❌ Error 429: Cuota excedida o Rate Limit. La clave NO tiene saldo o ha superado límites.")
    else:
         print(f"\n❌ Error HTTP: {e.reason}")
except Exception as e:
    print(f"💥 Error de ejecución: {e}")
