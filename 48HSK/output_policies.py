import json, html
try:
    with open('api_response.json') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

pii_masks = []
regex_guards = []
for op in data.get('operations', []):
    if '/v1/chat/completions' in op.get('target', '') and op.get('verb') == 'POST':
        for p in op.get('operationPolicies', {}).get('request', []):
            pname = p.get('policyName', '')
            params = p.get('parameters', {}) or {}
            if 'PIIMasking' in pname:
                ent = params.get('piiEntity', 'N/A')
                if isinstance(ent, str): ent = html.unescape(ent)
                pii_masks.append((pname, ent))
            elif 'RegexGuardrail' in pname:
                regex_guards.append(pname)
print(f"PII_MASKING_COUNT: {len(pii_masks)}")
for name, ent in pii_masks:
    print(f"PII_POLICY: {name} | ENTITY: {ent}")
print(f"OTHER_REGEX_GUARDRAIL_COUNT: {len(regex_guards)}")
for name in regex_guards:
    print(f"REGEX_POLICY: {name}")
