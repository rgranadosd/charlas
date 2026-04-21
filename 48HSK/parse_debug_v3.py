import sys, json, html

content = sys.stdin.read()
data = json.loads(content)

found_pii = []
found_regex = []

for op in data.get('operations', []):
    # Check if target matches exactly or contains the string
    if '/v1/chat/completions' in op.get('target', '') and op.get('verb') == 'POST':
        policies = op.get('operationPolicies', {}).get('request', [])
        for p in policies:
            pname = p.get('policyName', '')
            params = p.get('parameters', {})
            
            if 'PIIMasking' in pname:
                entity = params.get('piiEntity', 'N/A')
                if isinstance(entity, str):
                    entity = html.unescape(entity)
                found_pii.append((pname, entity))
            elif 'RegexGuardrail' in pname:
                found_regex.append(pname)

print(f"PII_MASKING_COUNT: {len(found_pii)}")
for name, ent in found_pii:
    print(f"PII_POLICY: {name} | ENTITY: {ent}")
print(f"OTHER_REGEX_GUARDRAIL_COUNT: {len(found_regex)}")
for name in found_regex:
    print(f"REGEX_POLICY: {name}")
