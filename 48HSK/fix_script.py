import json, html, sys

try:
    with open('api_mistral.json') as f:
        api = json.load(f)

    for op in api.get('operations', []):
        if op.get('target') == '/v1/chat/completions' and op.get('verb') == 'POST':
            for p in op.get('operationPolicies', {}).get('request', []):
                if p['policyName'] == 'PIIMaskingRegex':
                    params = p['parameters']
                    params['jsonPath'] = '$.messages[-1:].content'
                    
                    if params.get('name') == 'PII_DNI_ES':
                        entities_str = html.unescape(params['piiEntities'])
                        entities = json.loads(entities_str)
                        for e in entities:
                            e['piiRegex'] = e['piiRegex'].strip()
                        params['piiEntities'] = json.dumps(entities)
                    elif params.get('name') == 'Catch_Email_PII':
                        entities_str = html.unescape(params['piiEntities'])
                        entities = json.loads(entities_str)
                        params['piiEntities'] = json.dumps(entities)
                    
                    print(f"Fixed policy: {params['name']}")

    with open('api_mistral_fixed.json', 'w') as f:
        json.dump(api, f)
    print("SAVED_FILE")
except Exception as e:
    print(f"ERROR: {e}")
