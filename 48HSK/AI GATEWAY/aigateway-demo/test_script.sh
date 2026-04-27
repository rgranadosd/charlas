#!/bin/bash
cd "/Users/rafagranados/Develop/charlas/48HSK/AI GATEWAY/aigateway-demo"
WSO2_TOKEN_URL=$(grep WSO2_TOKEN_URL .env | cut -d '=' -f2)
CLIENT_ID=$(grep CLIENT_ID .env | cut -d '=' -f2)
CLIENT_SECRET=$(grep CLIENT_SECRET .env | cut -d '=' -f2)
TOKEN=$(curl -s -k -u "$CLIENT_ID:$CLIENT_SECRET" -d grant_type=client_credentials "$WSO2_TOKEN_URL" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token',''))")
if [ -z "$TOKEN" ]; then echo "Error: No token"; exit 1; fi
echo "TS: $(date +'%Y-%m-%d %H:%M:%S')"
curl -s -k -i -X POST https://localhost:8253/mistralaiapi/0.0.2/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "My pass\u200Bword=test123 && $(whoami)"}]}'
