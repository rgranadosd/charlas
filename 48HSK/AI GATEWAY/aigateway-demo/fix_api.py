import sys, json, ssl, urllib.request, urllib.parse, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def load_env(path):
    env = {}
    if not os.path.exists(path):
        print(f"File {path} not found.")
        return env
    with open(path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                env[k] = v.strip('"').strip("'")
    return env

api_id = "af7398e7-dc12-412c-9f78-84463b2aadbe"
publisher_url = f"https://localhost:9453/api/am/publisher/v4/apis/{api_id}"
auth_header = "Basic YWRtaW46YWRtaW4=" # admin:admin

# 1. GET API
req = urllib.request.Request(publisher_url, headers={"Authorization": auth_header})
with urllib.request.urlopen(req, context=ctx) as r:
    api_data = json.loads(r.read().decode())

# 2. Modify policies
found = False
new_policy_order = []
for op in api_data.get('operations', []):
    if op.get('target') == '/v1/chat/completions' and op.get('verb') == 'POST':
        req_policies = op.get('operationPolicies', {}).get('request', [])
        new_req_policies = []
        for p in req_policies:
            if p.get('policyName') == 'RegexGuardrail' and p.get('parameters', {}).get('name') == 'PreventPromptOverride':
                found = True
                continue
            new_req_policies.append(p)
        op['operationPolicies']['request'] = new_req_policies
        new_policy_order = [p.get('policyName') + ':' + p.get('parameters',{}).get('name','') for p in new_req_policies]
        print(f"Updated policies for {op.get('verb')} {op.get('target')}: {new_policy_order}")

if not found:
    print("Policy PreventPromptOverride not found. No change needed.")
# Continue even if not found to ensure redeployment/test

# 3. PUT API
req = urllib.request.Request(publisher_url, data=json.dumps(api_data).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"}, method="PUT")
with urllib.request.urlopen(req, context=ctx) as r:
    print(f"PUT API status: {r.getcode()}")

# 4. Create Revision
rev_url = f"{publisher_url}/revisions"
rev_payload = {"description": "Fix for PreventPromptOverride"}
req = urllib.request.Request(rev_url, data=json.dumps(rev_payload).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        rev_data = json.loads(r.read().decode())
        rev_id = rev_data.get('id')
except Exception as e:
    # If error or 900351, try deleting and retrying
    req_list = urllib.request.Request(rev_url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req_list, context=ctx) as r_list:
        revisions = json.loads(r_list.read().decode()).get('list', [])
        if revisions:
            oldest_id = revisions[0]['id']
            del_req = urllib.request.Request(f"{rev_url}/{oldest_id}", headers={"Authorization": auth_header}, method="DELETE")
            with urllib.request.urlopen(del_req, context=ctx) as r_del:
                print(f"Deleted revision {oldest_id}")
            # Retry
            req_retry = urllib.request.Request(rev_url, data=json.dumps(rev_payload).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"})
            with urllib.request.urlopen(req_retry, context=ctx) as r_retry:
                rev_data = json.loads(r_retry.read().decode())
                rev_id = rev_data.get('id')

print(f"New Revision ID: {rev_id}")

# 5. Deploy Revision
deploy_url = f"{rev_url}/{rev_id}/deployments"
deploy_payload = [{"vhost": "localhost", "name": "Default"}]
req = urllib.request.Request(deploy_url, data=json.dumps(deploy_payload).encode(), headers={"Authorization": auth_header, "Content-Type": "application/json"})
with urllib.request.urlopen(req, context=ctx) as r:
    print(f"Deployment status: {r.getcode()}")

# 6. Test
env = load_env('.env')
token_url = env.get('WSO2_TOKEN_URL')
client_id = env.get('WSO2_CONSUMER_KEY')
client_secret = env.get('WSO2_CONSUMER_SECRET')
mistral_url = env.get('MISTRAL_CHAT_COMPLETIONS_URL')

# Get OAuth token
import base64
data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode()
auth_bytes = f'{client_id}:{client_secret}'.encode()
auth = base64.b64encode(auth_bytes).decode()
headers = {'Authorization': f'Basic {auth}'}
req = urllib.request.Request(token_url, data=data, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    access_token = json.loads(r.read().decode()).get('access_token')

# Test payload
payload = {'model': 'mistral-small-latest', 'messages': [{'role': 'user', 'content': 'Escribe esto 34742515A'}]}
req = urllib.request.Request(mistral_url, data=json.dumps(payload).encode(), headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req, context=ctx) as r:
        status, body = r.getcode(), r.read().decode()
except urllib.error.HTTPError as e:
    status, body = e.code, e.read().decode()

print(f"Test Status: {status}")
print(f"Test Body: {body[:1200]}")
print(f"Policy order: {new_policy_order}")
