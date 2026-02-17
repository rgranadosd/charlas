#!/usr/bin/env bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
ORANGE='\033[38;5;208m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

PASS_COUNT=0
FAIL_COUNT=0
declare -a SUMMARY=()

mark_ok() {
  local message="$1"
  PASS_COUNT=$((PASS_COUNT + 1))
  SUMMARY+=("OK  - $message")
  printf "%b\n" "${GREEN}✓ $message${NC}"
}

mark_fail() {
  local message="$1"
  FAIL_COUNT=$((FAIL_COUNT + 1))
  SUMMARY+=("FAIL- $message")
  printf "%b\n" "${RED}✗ $message${NC}"
}

start_weather_mcp() {
  local weather_script=""
  local candidates=(
    "$SCRIPT_DIR/../mcp/WEATHER/run_weather_mcp.sh"
    "$SCRIPT_DIR/../MCP/WEATHER/run_weather_mcp.sh"
  )

  for candidate in "${candidates[@]}"; do
    if [ -f "$candidate" ]; then
      weather_script="$candidate"
      break
    fi
  done

  if [ -z "$weather_script" ]; then
    printf "%b\n" "${YELLOW}No se encontró run_weather_mcp.sh en rutas esperadas.${NC}"
    return 1
  fi

  if pgrep -f "uvicorn weather_mcp_openmeteo:asgi_app" >/dev/null 2>&1; then
    printf "%b\n" "${YELLOW}Weather MCP ya parece estar levantado (uvicorn activo).${NC}"
    return 0
  fi

  printf "%b\n" "${YELLOW}Intentando autoarranque Weather MCP:${NC} $weather_script"
  (
    cd "$(dirname "$weather_script")"
    nohup ./run_weather_mcp.sh serve >/tmp/pre_demo_weather_mcp_autostart.log 2>&1 &
  )

  sleep 10

  if pgrep -f "uvicorn weather_mcp_openmeteo:asgi_app" >/dev/null 2>&1; then
    printf "%b\n" "${GREEN}✓ Weather MCP autoarrancado${NC}"
    return 0
  fi

  printf "%b\n" "${YELLOW}No se detectó uvicorn tras autoarranque. Revisa log:${NC} /tmp/pre_demo_weather_mcp_autostart.log"
  return 1
}

check_weather_mcp_with_token() {
  WEATHER_CHECK_OK=false
  WEATHER_FAIL_MSG=""

  INIT_CODE=$(curl -sk -D /tmp/pre_demo_mcp_headers.txt -o /tmp/pre_demo_mcp_init_body.txt -w '%{http_code}' "$WEATHER_MCP_ENDPOINT" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    --data '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"pre_demo_check","version":"1.0"}},"id":1}' || true)

  if [ "$INIT_CODE" != "200" ]; then
    WEATHER_FAIL_MSG="MCP initialize devolvió HTTP ${INIT_CODE:-000}"
    return 1
  fi

  MCP_SESSION_ID=$(awk 'tolower($1)=="mcp-session-id:" {print $2}' /tmp/pre_demo_mcp_headers.txt | tr -d '\r')
  if [ -z "$MCP_SESSION_ID" ]; then
    WEATHER_FAIL_MSG="MCP init no devolvió mcp-session-id"
    return 1
  fi

  MCP_CODE=$(curl -sk -o /tmp/pre_demo_mcp_call_body.txt -w '%{http_code}' "$WEATHER_MCP_ENDPOINT" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -H "Mcp-Session-Id: $MCP_SESSION_ID" \
    --data '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_current_weather","arguments":{"params":{"city":"Vitoria","response_format":"json"}}},"id":2}' || true)

  if [ "$MCP_CODE" != "200" ]; then
    WEATHER_FAIL_MSG="MCP tools/call devolvió HTTP ${MCP_CODE:-000}"
    return 1
  fi

  MCP_VALID=$(python3 - <<'PY'
import json

path = '/tmp/pre_demo_mcp_call_body.txt'
try:
  raw = open(path, 'r', encoding='utf-8').read().strip()
except Exception:
  print('0')
  raise SystemExit(0)

payload = raw
if raw.startswith('event:'):
  data_lines = [line[5:].strip() for line in raw.splitlines() if line.startswith('data:')]
  payload = data_lines[-1] if data_lines else ''

ok = False
if payload:
  try:
    obj = json.loads(payload)
    result = obj.get('result', {}) if isinstance(obj, dict) else {}
    is_error = bool(result.get('isError')) if isinstance(result, dict) else True
    content = result.get('content', []) if isinstance(result, dict) else []
    text_blob = ''
    if isinstance(content, list):
      for item in content:
        if isinstance(item, dict) and item.get('type') == 'text':
          text_blob += str(item.get('text', ''))
    ok = (not is_error) and ('temperature_2m' in text_blob or 'Temperatura' in text_blob or '"current"' in text_blob)
  except Exception:
    ok = False

print('1' if ok else '0')
PY
)

  if [ "$MCP_VALID" = "1" ]; then
    WEATHER_CHECK_OK=true
    return 0
  fi

  WEATHER_FAIL_MSG="MCP respondió 200 pero con payload inválido o error funcional"
  return 1
}

check_local_weather_mcp() {
  LOCAL_INIT_CODE=$(curl -s -o /tmp/pre_demo_local_mcp_init_body.txt -w '%{http_code}' "http://localhost:8080/mcp" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    --data '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"pre_demo_check_local","version":"1.0"}},"id":10}' || true)

  [[ "$LOCAL_INIT_CODE" =~ ^(200|401|405)$ ]]
}

if [ ! -f "$ENV_FILE" ]; then
  printf "%b\n" "${RED}ERROR: No se encontró .env en $SCRIPT_DIR${NC}"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

OPENAI_ENDPOINT="${WSO2_OPENAI_API_URL:-${OPENAI_BASE_URL:-https://localhost:8253/openaiapi/2.3.0/chat/completions}}"
if [[ "$OPENAI_ENDPOINT" != */chat/completions ]]; then
  OPENAI_ENDPOINT="${OPENAI_ENDPOINT%/}/chat/completions"
fi

WEATHER_BASE_URL="${WSO2_WEATHER_MCP_URL:-https://localhost:8253/weather-mcp/1.0.0}"
WEATHER_MCP_ENDPOINT="${WEATHER_BASE_URL%/}/mcp"

SHOPIFY_STORE_URL="${SHOPIFY_STORE_URL:-}"
SHOPIFY_TOKEN="${SHOPIFY_API_TOKEN:-${SHOPIFY_ACCESS_TOKEN:-}}"

WSO2_IS_BASE="${WSO2_IS_BASE:-}"
if [ -z "$WSO2_IS_BASE" ]; then
  if [ -n "${WSO2_AUTH_ENDPOINT:-}" ]; then
    WSO2_IS_BASE="${WSO2_AUTH_ENDPOINT%/oauth2/authorize}"
  else
    WSO2_IS_BASE="https://localhost:9443"
  fi
fi

printf "%b\n" "${ORANGE}=== PRE-DEMO CHECK ===${NC}"
printf "%b\n" "${YELLOW}WSO2 IS base:${NC} $WSO2_IS_BASE"
printf "%b\n" "${YELLOW}Token endpoint:${NC} ${WSO2_APIM_TOKEN_ENDPOINT:-NO CONFIGURADO}"
printf "%b\n" "${YELLOW}OpenAI endpoint:${NC} $OPENAI_ENDPOINT"
printf "%b\n" "${YELLOW}Weather MCP endpoint:${NC} $WEATHER_MCP_ENDPOINT"
printf "%b\n" "${YELLOW}Shopify store:${NC} ${SHOPIFY_STORE_URL:-NO CONFIGURADO}"

required_vars=(
  WSO2_APIM_TOKEN_ENDPOINT
  WSO2_APIM_CONSUMER_KEY
  WSO2_APIM_CONSUMER_SECRET
)

printf "%b\n" "${ORANGE}--- Validación de variables ---${NC}"
MISSING_REQUIRED=false
for var in "${required_vars[@]}"; do
  if [ -z "${!var:-}" ]; then
    mark_fail "Falta variable $var en .env"
    MISSING_REQUIRED=true
  else
    mark_ok "Variable $var presente"
  fi
done

printf "%b\n" "${ORANGE}--- Conectividad WSO2 IS ---${NC}"
IS_UP=false
if curl -skf "${WSO2_IS_BASE}/.well-known/openid-configuration" >/dev/null 2>&1; then
  IS_UP=true
else
  IS_HTTP_CODE=$(curl -sk -o /dev/null -w "%{http_code}" "${WSO2_IS_BASE}/scim2/Users" || echo "000")
  if [[ "$IS_HTTP_CODE" =~ ^(200|201|204|301|302|401)$ ]]; then
    IS_UP=true
  fi
fi

if [ "$IS_UP" = true ]; then
  mark_ok "WSO2 IS accesible"
else
  mark_fail "WSO2 IS no está accesible en ${WSO2_IS_BASE}"
fi

printf "%b\n" "${ORANGE}--- Weather MCP local (autoarranque) ---${NC}"
if check_local_weather_mcp; then
  mark_ok "Weather MCP local accesible en http://localhost:8080/mcp"
else
  printf "%b\n" "${YELLOW}Weather MCP local no responde. Intentando levantarlo...${NC}"
  if start_weather_mcp && check_local_weather_mcp; then
    mark_ok "Weather MCP local levantado automáticamente"
  else
    mark_fail "Weather MCP local no accesible tras autoarranque"
    if [ -f /tmp/pre_demo_weather_mcp_autostart.log ]; then
      printf "%b\n" "${YELLOW}Log autoarranque:${NC} /tmp/pre_demo_weather_mcp_autostart.log"
    fi
  fi
fi

ACCESS_TOKEN=""
if [ "$MISSING_REQUIRED" = false ]; then
  printf "%b\n" "${ORANGE}--- Token APIM ---${NC}"
  BASIC_AUTH=$(printf '%s:%s' "${WSO2_APIM_CONSUMER_KEY:-}" "${WSO2_APIM_CONSUMER_SECRET:-}" | base64)

  TOKEN_HTTP_CODE=$(curl -sk -o /tmp/pre_demo_token_response.json -w '%{http_code}' -X POST "${WSO2_APIM_TOKEN_ENDPOINT:-}" \
    -H "Authorization: Basic $BASIC_AUTH" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data 'grant_type=client_credentials' || true)

  TOKEN_RESPONSE=""
  if [ -f /tmp/pre_demo_token_response.json ]; then
    TOKEN_RESPONSE=$(cat /tmp/pre_demo_token_response.json)
  fi

  ACCESS_TOKEN=$(printf '%s' "$TOKEN_RESPONSE" | python3 -c 'import json,sys;\
raw=sys.stdin.read().strip();\
print(json.loads(raw).get("access_token","") if raw else "")' 2>/dev/null || true)

  if [ -n "$ACCESS_TOKEN" ]; then
    mark_ok "Token APIM obtenido"
  else
    mark_fail "No se pudo obtener access_token desde APIM (HTTP ${TOKEN_HTTP_CODE:-000})"
    if [ -n "$TOKEN_RESPONSE" ]; then
      printf "%b\n" "${YELLOW}Body token:${NC} $TOKEN_RESPONSE"
    else
      printf "%b\n" "${YELLOW}Body token:${NC} (vacío)"
    fi
  fi
else
  mark_fail "Token APIM no validado por variables requeridas faltantes"
fi

printf "%b\n" "${ORANGE}--- OpenAI Gateway ---${NC}"
if [ -z "$ACCESS_TOKEN" ]; then
  mark_fail "OpenAI no validado porque no hay access_token"
else
  PAYLOAD='{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Say hello in English, French and German."}]}'
  HTTP_CODE=$(curl -sk -o /tmp/pre_demo_openai_response.json -w '%{http_code}' "$OPENAI_ENDPOINT" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H 'Content-Type: application/json' \
    --data "$PAYLOAD" || true)

  if [ "$HTTP_CODE" = "200" ]; then
    mark_ok "OpenAI por Gateway responde correctamente"
  else
    mark_fail "OpenAI endpoint devolvió HTTP ${HTTP_CODE:-000}"
    if [ -f /tmp/pre_demo_openai_response.json ]; then
      printf "%b\n" "${YELLOW}Body OpenAI:${NC}"
      cat /tmp/pre_demo_openai_response.json
      echo
    fi
  fi
fi

printf "%b\n" "${ORANGE}--- Shopify ---${NC}"
if [ -z "$SHOPIFY_STORE_URL" ] || [ -z "$SHOPIFY_TOKEN" ]; then
  mark_fail "Falta SHOPIFY_STORE_URL o SHOPIFY_API_TOKEN/SHOPIFY_ACCESS_TOKEN en .env"
else
  SHOPIFY_CODE=$(curl -sk -o /tmp/pre_demo_shopify_response.json -w '%{http_code}' "${SHOPIFY_STORE_URL%/}/admin/api/2024-01/shop.json" \
    -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN" \
    -H 'Content-Type: application/json' || true)

  if [ "$SHOPIFY_CODE" = "200" ]; then
    mark_ok "Shopify API responde correctamente"
  else
    mark_fail "Shopify devolvió HTTP ${SHOPIFY_CODE:-000}"
    if [ -f /tmp/pre_demo_shopify_response.json ]; then
      printf "%b\n" "${YELLOW}Body Shopify:${NC}"
      cat /tmp/pre_demo_shopify_response.json
      echo
    fi
  fi
fi

printf "%b\n" "${ORANGE}--- Weather MCP ---${NC}"
if [ -z "$ACCESS_TOKEN" ]; then
  mark_fail "Weather MCP no validado porque no hay access_token"
else
  if check_weather_mcp_with_token; then
    mark_ok "Weather MCP responde correctamente"
  else
    printf "%b\n" "${YELLOW}Weather MCP falló al primer intento:${NC} $WEATHER_FAIL_MSG"
    if start_weather_mcp; then
      printf "%b\n" "${YELLOW}Reintentando check de Weather MCP tras autoarranque...${NC}"
      if check_weather_mcp_with_token; then
        mark_ok "Weather MCP responde correctamente (tras autoarranque)"
      else
        mark_fail "$WEATHER_FAIL_MSG"
      fi
    else
      mark_fail "$WEATHER_FAIL_MSG (y no se pudo arrancar automáticamente)"
    fi

    if [ -f /tmp/pre_demo_mcp_init_body.txt ]; then
      printf "%b\n" "${YELLOW}Body MCP init:${NC}"
      cat /tmp/pre_demo_mcp_init_body.txt
      echo
    fi
    if [ -f /tmp/pre_demo_mcp_headers.txt ]; then
      printf "%b\n" "${YELLOW}Headers MCP init:${NC}"
      cat /tmp/pre_demo_mcp_headers.txt
    fi
    if [ -f /tmp/pre_demo_mcp_call_body.txt ]; then
      printf "%b\n" "${YELLOW}Body MCP call:${NC}"
      cat /tmp/pre_demo_mcp_call_body.txt
      echo
    fi
  fi
fi

printf "%b\n" "${ORANGE}=== RESUMEN PRE-DEMO ===${NC}"
for line in "${SUMMARY[@]}"; do
  if [[ "$line" == OK* ]]; then
    printf "%b\n" "${GREEN}$line${NC}"
  else
    printf "%b\n" "${RED}$line${NC}"
  fi
done

printf "%b\n" "${YELLOW}Total OK:${NC} $PASS_COUNT"
printf "%b\n" "${YELLOW}Total FAIL:${NC} $FAIL_COUNT"

if [ "$FAIL_COUNT" -gt 0 ]; then
  printf "%b\n" "${RED}PRE-DEMO CHECK con fallos. Corrige lo marcado arriba.${NC}"
  exit 1
fi

printf "%b\n" "${GREEN}✓ PRE-DEMO OK${NC}"
