import json
with open('api.json','r') as f: api = json.load(f)
for op in api['operations']:
    if op['target'] == '/v1/chat/completions' and op['verb'] == 'POST':
        op['operationPolicies']['request'] = [p for p in op['operationPolicies'].get('request',[]) if not (p.get('policyName') == 'RegexGuardrail' and p.get('parameters',{}).get('name') == 'PreventPromptOverride')]
with open('api_updated.json','w') as f: json.dump(api, f)
