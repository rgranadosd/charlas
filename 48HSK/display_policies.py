import json, html
try:
    with open('api_mistral.json', 'r') as f:
        d = json.load(f)
    print("File loaded successfully.")
    for op in d.get('operations', []):
        target = op.get('target', '')
        verb = op.get('verb', '')
        req_policies = op.get('operationPolicies', {}).get('request', [])
        if req_policies:
            print(f'=== {verb} {target} ===')
            for p in req_policies:
                pname = p.get('policyName')
                pversion = p.get('policyVersion')
                print(f'  - {pname} ({pversion})')
                params = p.get('parameters', {})
                decoded_params = {}
                for k, v in params.items():
                    if isinstance(v, str):
                        decoded_params[k] = html.unescape(v)
                    else:
                        decoded_params[k] = v
                print(f'    params: {json.dumps(decoded_params, indent=4)}')
except Exception as e:
    print(f"An error occurred: {e}")
