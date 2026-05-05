# Demo Files Repository

Este lab puede levantar un repositorio en memoria para `/files/me` sin usar base de datos real.

## Que hace

El resource API carga un seed desde `dev-data/demo-files.json` al arrancar.

Solo se activa cuando:

- `APP_ENV=local` o `APP_ENV=dev`
- `USE_IN_MEMORY_DEMO_FILES=true`

El ownership de `/files/me` se resuelve exclusivamente con `sub`.

Si tu despliegue emite subjects distintos segun el tipo de token para el mismo usuario, puedes añadir aliases en el seed con `owner_sub_aliases`.

- `USER_TOKEN` con `sub` presente en el JSON: devuelve sus ficheros.
- `AGENT_TOKEN`: se rechaza con `403` porque no aporta contexto de usuario.
- `OBO_TOKEN`: devuelve los mismos ficheros del usuario delegado cuando `sub` coincide con un `owner_sub` cargado.

## Seed JSON

Fuente única de verdad:

- `dev-data/demo-files.json`

Assets demo incluidos:

- `dev-data/assets/alice-demo/welcome-pack.txt`
- `dev-data/assets/alice-demo/hotel-voucher.svg`
- `dev-data/assets/bob-demo/expense-report-may.csv`

## Como adaptar los owner_sub

Edita `dev-data/demo-files.json` y sustituye:

- `REPLACE_WITH_REAL_SUB_ALICE`
- `REPLACE_WITH_REAL_SUB_BOB`

por los `sub` reales de tus usuarios demo.

Si el `USER_TOKEN` y el `OBO_TOKEN` de un mismo usuario no comparten exactamente el mismo `sub`, manten un `owner_sub` canonico y añade el otro valor en `owner_sub_aliases`.

No uses `client_id` ni `agent_id` como propietarios del recurso.

## Variables de entorno

Valores de referencia en `resource_api/.env.example`:

- `APP_ENV=local`
- `USE_IN_MEMORY_DEMO_FILES=true`
- `DEMO_FILES_JSON_PATH=dev-data/demo-files.json`

## Verificacion de carga

Endpoint solo local/dev:

- `GET /debug/demo-files`

Devuelve:

- ruta del JSON cargado
- si el repositorio demo esta activo
- numero de usuarios seed
- numero total de ficheros
- `owner_sub` cargados
- `canonical_owner_subs` cargados
- error de carga, si existiera

Si el JSON falta o esta mal formado, la app no se cae: el repositorio demo se desactiva y el endpoint debug lo refleja.

## Flujo recomendado

1. Edita `dev-data/demo-files.json` con los `sub` reales.
2. Arranca el entorno local.
3. Comprueba `GET /debug/demo-files`.
4. Prueba `GET /files/me` con `USER_TOKEN`.
5. Prueba `GET /files/me` con `AGENT_TOKEN` y verifica denegacion.
6. Repite `GET /files/me` con `OBO_TOKEN` para confirmar que reutiliza el mismo dataset del usuario delegado.