import sys, json, ssl, urllib.request, urllib.parse, os, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def load_env(path):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env[k] = v.strip('"').strip("'")
    return env

api_id = "af7398e7-dc12-412c-9f78-84463b2aadbe"
publisher_url = f"https://localhost:9453/api/am/publisher/v4/apis/{api_id}"
auth_header = "Basic YWRtaW46YWRtaW4="

print(f"Starting script for API {api_id}...")

# 1. GET
req = urllib.request.Request(publisher_url, headers={"Authorization": auth_header})
with urllib.request.urlopen(req, context=ctx) as r:
    api_data = json.loads(r.read().decode())
print("GET API Success")

# 2. Update
found = False
for op in api_data.get('operations', []):
    if op.get('target') == '/v1/chat/completions' and op.get('verb') == 'POST':
        policies = op.get('operationPolicies', {}).get('request', [])
        new_policies = [p for p in policies if not (p.get('policyName') == 'RegexGuardrail' and p.get('parameters', {}).get('name') == 'PreventPromptOverride')]
        if len(new_policies) < len(policies):
            found = True
            op['operationPolicies']['request'] = new_policies
            print(f"Policy removed. New list: {[p.get('policyName') + ':' + p.get('parameters',{}).get('name','') for p in new_policies]}")

if found:
    req = urllib.request.Request(publisher_url, data=json.dumps(api_data).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req, context=ctx) as r:
        print(f"PUT API status: {r.getcode()}")

# 4. Revision
rev_url = f"{publisher_url}/revisions"
try:
    req = urllib.request.Request(rev_url, data=json.dumps({"description": "fix"}).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx) as r:
        rev_id = json.loads(r.read().decode()).get('id')
except Exception:
    req = urllib.request.Request(rev_url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req, context=ctx) as r:
        revisions = json.loads(r.read().decode()).get('list', [])
        if revisions:
            rid = revisions[0]['id']
            urllib.request.urlopen(urllib.request.Request(f"{rev_url}/{rid}", headers={"Authorization": auth_header}, method="DELETE"), context=ctx)
            print(f"Deleted {rid}")
            req = urllib.request.Request(rev_url, data=json.dumps({"description": "fix"}).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, context=ctx) as r:
                rev_id = json.loads(r.read().decode()).get('id')
print(f"Revision {rev_id}")

# 5. Deploy
urllib.request.urlopen(urllib.request.Request(f"{rev_url}/{rev_id}/deployments", data=json.dumps([{"vhost": "localhost", "name": "Default"}]).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"}), context=ctx)
print("Deployed")

# 6. Test
env = load_env('.env')
token_url, cid, csecret, murl = env.get('WSO2_TOKEN_URL'), env.get('WSO2_CONSUMER_KEY'), env.get('WSO2_CONSUMER_SECRET'), env.get('MISTRAL_CHAT_COMPLETIONS_URL')
auth = base64.b64encode(f'{cid}:{csecret}'.encode()).decode()
with urllib.request.urlopen(urllib.request.Request(token_url, data=urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode(), headers={'Authorization': f'Basic {auth}'}), context=ctx) as r:
    tok = json.loads(r.read().decode())['access_token']

req = urllib.request.Request(murl, data=json.dumps({'model': 'mistral-small-latest', 'messages': [{'role': 'user', 'content': 'Escribe esto 34742515A'}]}).encode(), headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        print(f"Test Status: {r.getcode()}")
        print(f"Test Body: {r.read().decode()[:500]}")
except Exception as e:
    print(f"Test Error: {e}")
