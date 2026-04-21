import base64, json, ssl, urllib.request, urllib.parse, urllib.error
from pathlib import Path
import sys

print("Script started", file=sys.stderr)

root = Path('/Users/rafagranados/Develop/charlas/48HSK/AI GATEWAY/aigateway-demo')

def load_env(path):
    out = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if s and not s.startswith('#') and '=' in s:
            k, v = s.split('=', 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out

try:
    env = load_env(root / '.env')
    print("Env loaded", file=sys.stderr)
    ctx = ssl._create_unverified_context()

    def get_token():
        req = urllib.request.Request(
            env['WSO2_TOKEN_URL'],
            data=urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode(),
            method='POST'
        )
        basic = base64.b64encode(f"{env['WSO2_CONSUMER_KEY']}:{env['WSO2_CONSUMER_SECRET']}".encode()).decode()
        req.add_header('Authorization', 'Basic ' + basic)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read().decode())['access_token']

    def call(prompt, token):
        payload = {
            'model': 'mistral-tiny',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_tokens': 2000,
        }
        req = urllib.request.Request(
            env['MISTRAL_CHAT_COMPLETIONS_URL'],
            data=json.dumps(payload).encode(),
            method='POST'
        )
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Content-Type', 'application/json')
        req.add_header('accept', 'application/json')
        req.add_header('User-Agent', 'WSO2-AI-Gateway-Demo/1.0')
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                body = resp.read().decode('utf-8', 'ignore')
                return resp.status, body
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'ignore')
            return e.code, body

    print("Requesting token", file=sys.stderr)
    token = get_token()
    print("Token received", file=sys.stderr)
    for label, prompt in [
        ('IBAN', 'Repeat exactly: IBAN ES7620770024003102575766'),
        ('CVV', 'Repeat exactly: CVV 123'),
    ]:
        print(f"Calling {label}", file=sys.stderr)
        status, body = call(prompt, token)
        print(f'=== {label} ===')
        print(f'STATUS: {status}')
        print(body[:2000])
        print()
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
