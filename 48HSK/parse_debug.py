import sys, json, html

def main():
    try:
        content = sys.stdin.read()
        if not content:
            print("No input received")
            return
        data = json.loads(content)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return

    ops = data.get('operations', [])
    pii_masks = []
    other_regex_guards = []

    for op in ops:
        target = op.get('target')
        verb = op.get('verb')
        
        # We search specifically for the POST /v1/chat/completions or just check all
        req_policies = op.get('operationPolicies', {}).get('request', [])
        for p in req_policies:
            pname = p.get('policyName', '')
            params = p.get('parameters', {})
            
            if 'PIIMasking' in pname or 'RegexGuardrail' in pname:
                # Only if it matches the requested operation or if target is what we expect
                if target == '/v1/chat/completions' and verb == 'POST':
                    decoded_params = {}
                    for k, v in params.items():
                        if isinstance(v, str):
                            decoded_params[k] = html.unescape(v)
                        else:
                            decoded_params[k] = v

                    if 'PIIMasking' in pname:
                        pii_entity = decoded_params.get('piiEntity', 'N/A')
                        pii_masks.append({"name": pname, "entity": pii_entity})
                    elif 'RegexGuardrail' in pname:
                        other_regex_guards.append(pname)

    print(f"PII_MASKING_COUNT: {len(pii_masks)}")
    for item in pii_masks:
        print(f"PII_POLICY: {item['name']} | ENTITY: {item['entity']}")
    
    print(f"OTHER_REGEX_GUARDRAIL_COUNT: {len(other_regex_guards)}")
    for name in other_regex_guards:
        print(f"REGEX_POLICY: {name}")

if __name__ == '__main__':
    main()
