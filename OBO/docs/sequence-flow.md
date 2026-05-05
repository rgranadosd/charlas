# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuario
    participant SPA as React SPA
    participant B as FastAPI Backend
    participant IS as WSO2 IS 7.2
    participant API as Resource API

    U->>SPA: Login usuario
    SPA->>IS: Authorization Code + PKCE (SDK)
    IS-->>SPA: USER_TOKEN
    SPA->>B: POST /api/session/user-token
    B-->>SPA: USER_TOKEN decodificado y trazas

    U->>SPA: Obtener AGENT_TOKEN
    SPA->>B: POST /api/agent-token
    B->>IS: grant_type=client_credentials
    IS-->>B: AGENT_TOKEN
    B-->>SPA: AGENT_TOKEN + claims

    U->>SPA: Probar recurso privado con AGENT_TOKEN
    SPA->>B: POST /api/test/agent-access
    B->>API: GET /files/me Authorization: Bearer AGENT_TOKEN
    API-->>B: 403 token sin contexto de usuario
    B-->>SPA: traza + explicacion de seguridad

    U->>SPA: Iniciar delegacion OBO
    SPA->>B: POST /api/obo/start
    B->>B: genera state + code_verifier + code_challenge
    B-->>SPA: authorization_url + PKCE metadata

    U->>SPA: Abrir pantalla de consentimiento
    SPA->>IS: GET authorization_url
    IS-->>B: GET /api/obo/callback?code=...&state=...
    B->>B: valida state y guarda AUTHORIZATION_CODE
    B-->>SPA: popup close + session refresh

    U->>SPA: Intercambiar code por OBO_TOKEN
    SPA->>B: POST /api/obo/exchange
    B->>IS: code + code_verifier + agent_token
    IS-->>B: OBO_TOKEN
    B-->>SPA: OBO_TOKEN + claims

    U->>SPA: Leer mis ficheros con OBO_TOKEN
    SPA->>B: POST /api/test/obo-access
    B->>API: GET /files/me Authorization: Bearer OBO_TOKEN
    API-->>B: 200 token delegado aceptado
    B-->>SPA: token_analysis + respuesta protegida
```

## Lectura del diagrama

- `USER_TOKEN` pertenece al canal SPA <-> IS.
- `AGENT_TOKEN` pertenece al canal Backend <-> IS.
- `AUTHORIZATION_CODE` es temporal y solo sirve como entrada del exchange.
- `OBO_TOKEN` es el artefacto delegado que el backend usa frente a la Resource API.
