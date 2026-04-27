import base64
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ENV_PATH = Path(__file__).resolve().parents[2] / "AI GATEWAY" / "aigateway-demo" / ".env"
CTX = ssl._create_unverified_context()


def load_env(path):
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def get_token(env):
    req = urllib.request.Request(
        env["WSO2_TOKEN_URL"],
        data=urllib.parse.urlencode({"grant_type": "client_credentials"}).encode(),
        method="POST",
    )
    credentials = f"{env['WSO2_CONSUMER_KEY']}:{env['WSO2_CONSUMER_SECRET']}".encode()
    req.add_header("Authorization", "Basic " + base64.b64encode(credentials).decode())
    with urllib.request.urlopen(req, context=CTX, timeout=20) as response:
        return json.loads(response.read().decode())["access_token"]


def run_case(env, token, name, content):
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": content}],
    }
    req = urllib.request.Request(
        env["MISTRAL_CHAT_COMPLETIONS_URL"],
        data=json.dumps(payload).encode(),
        method="POST",
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        status = error.code
        body = error.read().decode("utf-8", errors="replace")

    print(name)
    print(f"STATUS {status}")
    print(f"HAS_PII_PASSWORD {'PII_PASSWORD' in body}")
    print(f"BODY {body[:300].replace(chr(10), ' ')}")


def main():
    env = load_env(ENV_PATH)
    token = get_token(env)
    run_case(env, token, "CASE_A", "password=test123")
    run_case(env, token, "CASE_B", "pass\u200Bword=test123")


if __name__ == "__main__":
    main()