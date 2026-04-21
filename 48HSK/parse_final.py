import sys, json, html, urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, 'https://localhost:9453', 'admin', 'admin')
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)

url = 'https://localhost:9453/api/am/publisher/v4/apis/af7398e7-dc12-412c-9f78-84463b2aadbe'
try:
    with opener.open(url) as response:
        data = json.load(response)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)

pii_masks = []
regex_guards = []

for op in data.get('operations', []):
    if '/v1/chat/completions' in op.get('target', '') and op.get('verb') == 'POST':
        policies = op.get('operationPolicies', {}).get('request', [])
        for p in policies:
            pname = p.get('policyName', '')
            params = p.get('parameters', {}) or {}
            if 'PIIMasking' in pname:
                entity = params.get('piiEntity', 'N/A')
                if isinstance(entity, str): entity = html.unescape(entity)
                pii_masks.append((pname, entity))
            elif 'RegexGuardrail' in pname:
                regex_guards.append(pname)

print(f"PII_MASKING_COUNT: {len(pii_masks)}")
for name, ent in pii_masks:
    print(f"PII_POLICY: {name} | ENTITY: {ent}")
print(f"OTHER_REGEX_GUARDRAIL_COUNT: {len(regex_guards)}")
for name in regex_guards:
    print(f"REGEX_POLICY: {name}")
