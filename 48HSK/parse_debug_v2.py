import sys, json, html

content = sys.stdin.read()
if not content:
    print("NO_INPUT")
    sys.exit(0)

try:
    data = json.loads(content)
except Exception as e:
    print(f"JSON_ERROR: {e}")
    sys.exit(0)

all_ops = data.get('operations', [])
print(f"TOTAL_OPERATIONS: {len(all_ops)}")

found_pii = []
found_regex = []

for op in all_ops:
    t = op.get('target')
    v = op.get('verb')
    
    if t == '/v1/chat/completions' and v == 'POST':
        policies = op.get('operationPolicies', {}).get('request', [])
        for p in policies:
            pname = p.get('policyName', '')
            params = p.get('parameters', {})
            
            if 'PIIMasking' in pname:
                entity = params.get('piiEntity', 'N/A')
                # Try to decode if entity is a string
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
