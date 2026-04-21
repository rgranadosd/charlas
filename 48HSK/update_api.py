import json, sys

with open('api.json', 'r') as f:
    api = json.load(f)

for op in api.get('operations', []):
    if op.get('target') == '/v1/chat/completions' and op.get('verb') == 'POST':
        req_policies = op.get('operationPolicies', {}).get('request', [])
        new_policies = []
        for p in req_policies:
            params = p.get('parameters', {})
            # Remove ONLY the policy with name 'PreventPromptOverride'
            if p.get('policyName') == 'RegexGuardrail' and params.get('name') == 'PreventPromptOverride':
                continue
            new_policies.append(p)
        op['operationPolicies']['request'] = new_policies

with open('api_updated.json', 'w') as f:
    json.dump(api, f)
