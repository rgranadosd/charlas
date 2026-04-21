import sys, json, html
d = json.load(sys.stdin)
ops = d.get('operations', [])
for op in ops:
    target = op.get('target','')
    verb = op.get('verb','')
    req_policies = op.get('operationPolicies', {}).get('request', [])
    resp_policies = op.get('operationPolicies', {}).get('response', [])
    if req_policies or resp_policies:
        print(f'=== {verb} {target} ===')
        if req_policies:
            print('  REQUEST policies:')
            for p in req_policies:
                pname = p.get('policyName')
                print(f'    - {pname} ({p.get("policyVersion")})')
                params = p.get('parameters', {})
                decoded_params = {}
                for k, v in params.items():
                    if isinstance(v, str):
                        decoded_params[k] = html.unescape(v)
                    else:
                        decoded_params[k] = v
                print(f"      params: {json.dumps(decoded_params, indent=6)}")
        if resp_policies:
            print('  RESPONSE policies:')
            for p in resp_policies:
                pname = p.get('policyName')
                print(f'    - {pname} ({p.get("policyVersion")})')
                params = p.get('parameters', {})
                decoded_params = {}
                for k, v in params.items():
                    if isinstance(v, str):
                        decoded_params[k] = html.unescape(v)
                    else:
                        decoded_params[k] = v
                print(f"      params: {json.dumps(decoded_params, indent=6)}")
        print()
