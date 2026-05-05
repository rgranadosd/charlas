# Architecture

## Componentes

### Frontend SPA

Responsabilidades:

- autenticar al usuario con `@asgardeo/auth-react` contra WSO2 IS 7.2 local,
- mostrar el estado de la sesion humana,
- ejecutar cada paso del flujo desde botones explicitos,
- representar artefactos y claims en el `Artifact Inspector`,
- mostrar trazas de backend y resultados de autorizacion.

La SPA no conoce secretos del agente ni del flujo OBO. Solo conserva el access token del usuario emitido para la sesion del navegador y lo sincroniza con el backend para fines didacticos.

### Backend FastAPI

Responsabilidades:

- obtener `AGENT_TOKEN` desde WSO2 IS,
- generar `state`, `code_verifier` y `code_challenge`,
- construir la `authorization_url`,
- validar el callback OAuth,
- canjear `authorization_code + code_verifier + agent_token`,
- conservar el estado de la demo en memoria,
- llamar a la Resource API y devolver trazas interpretables.

Modulos clave:

- `app/services/oauth_service.py`: encapsula el detalle de llamadas al AS.
- `app/services/agent_token_service.py`: client credentials del agente.
- `app/services/obo_service.py`: estado PKCE y exchange OBO.
- `app/services/jwt_debug_service.py`: decodificacion y resumen de JWT.
- `app/state/session_store.py`: almacenamiento temporal por `X-Demo-Session-Id`.

### Resource API

Responsabilidades:

- validar firma JWT contra JWKS del IS,
- validar `iss`, `aud` y expiracion,
- inspeccionar `sub`, `act` y `scope`,
- rechazar el `AGENT_TOKEN` para recursos privados del usuario,
- aceptar el `OBO_TOKEN` cuando existe delegacion y scopes suficientes,
- devolver `token_analysis` para que la UI explique la decision.

## Modelo de seguridad

Separacion de identidades:

- Usuario: sujeto humano autenticado en la SPA.
- Agente registrado: identidad logica configurada en `AGENT_ID`.
- Cliente OAuth del agente: identidad tecnica autenticada con `AGENT_TOKEN`.
- OBO token: token delegado donde `sub` identifica al usuario y `act.sub` al agente delegado.

La PoC intenta parecerse al patron de `gardeo-hotels` en estos puntos:

- `AGENT_TOKEN` y `OBO_TOKEN` son artefactos distintos.
- La delegacion usa Authorization Code + PKCE.
- El backend mantiene `state` y `code_verifier`.
- El exchange mezcla el codigo con el token del agente.
- La API valida claims y aplica autorizacion diferenciada.

## Estado en memoria

Por cada sesion demo se guardan:

- `user_token`
- `user_claims`
- `configured_agent_id`
- `oauth_client_id`
- `agent_token`
- `agent_token_claims`
- `agent_token_sub`
- `agent_token_sub_same_as_client_id`
- `agent_token_authentication_type`
- `obo_authorization_url`
- `obo_state`
- `code_verifier`
- `code_challenge`
- `authorization_code`
- `obo_token`
- `obo_token_claims`
- `delegated_user_id`
- `delegated_agent_id`
- `last_api_request`
- `last_api_response`
- `last_security_explanation`
- timestamps y trazas

El almacenamiento es deliberadamente simple para que la PoC sea facil de leer y modificar.
