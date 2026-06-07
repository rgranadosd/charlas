# Especificacion tecnica para RAG + pipeline de autogeneracion de juegos CPCtelera

## 1) Objetivo
Definir un contrato tecnico estable para que el sistema RAG y el pipeline generen juegos jugables de forma automatica, compilable y verificable, evitando errores recurrentes de paleta, coordenadas y colisiones.

## 2) Alcance
Esta especificacion aplica a proyectos en C con CPCtelera (modo de video 0), compilados con SDCC y ejecutados en Caprice32.

## 3) Contrato minimo de estructura de codigo
El generador debe producir, como minimo, estas funciones:
- init_game
- update_game
- draw_game
- reset_ball (o reset_player/respawn equivalente segun el genero)
- draw_score
- draw_lives (si aplica)
- main

Bucle principal obligatorio:
1. init_game una sola vez.
2. En cada frame:
   - cpct_scanKeyboard_f
   - update_game
   - draw_game
   - draw HUD
   - cpct_waitVSYNC

Regla: el estado runtime nunca debe depender solo de inicializadores globales. Debe inicializarse explicitamente en init_game.

## 4) Reglas de video y coordenadas (criticas)
### 4.1 Unidades en modo 0
- cpct_getScreenPtr: X en bytes, Y en scanlines.
- cpct_drawSolidBox: ancho en bytes, alto en scanlines.

Consecuencia:
- 1 byte horizontal en modo 0 = 2 pixeles.
- Si una entidad usa BALL_W y BALL_H, todas las colisiones deben usar esa caja real (AABB), no solo el punto superior izquierdo.

### 4.2 HUD en modo 0
- Cada caracter de cpct_drawStringM0 ocupa 4 bytes de ancho.
- Posiciones de HUD deben calcularse en bytes para evitar solape.

## 5) Reglas de color y paleta (criticas)
Configuracion recomendada al iniciar:
1. cpct_disableFirmware
2. cpct_setVideoMode(0)
3. cpct_setPALColour para cada PEN usada (0..3 minimo)
4. cpct_setBorder como marcador visual de diagnostico

Reglas:
- No hardcodear bytes de color ambiguos para sprites/bloques.
- Generar color de entidades con cpct_px2byteM0(pen, pen).
- En caso de duda visual, mantener borde de color de test hasta validar render.

## 6) Modelo de entidades y fisica
Cada entidad movil debe declarar:
- posicion: x, y
- velocidad: vx, vy
- tamano: w, h
- estado: activa/inactiva o fase (attached, launched, dead)

Colisiones obligatorias:
- Paredes laterales: usando x y right = x + w - 1.
- Techo: usando y.
- Suelo: usando bottom = y + h - 1.
- Pala/plataforma: overlap de cajas (AABB).
- Bloques/tiles: overlap de cajas con celda objetivo.

Para Breakout:
- Estado inicial: pelota pegada a pala (attached).
- Lanzamiento: al detectar Space pasa a launched.
- Al perder vida: reset a attached.

Reglas de velocidad y rebote en pala (Breakout):
- ball_vx y ball_vy SIEMPRE valen +1 o -1. Nunca 0, nunca ±2.
- Colision con pala: SOLO invertir ball_vy. NUNCA modificar ball_vx.
  Si ball_vx se pone a 0, la bola solo se mueve en vertical y el juego queda bloqueado.
  Si ball_vx se pone a ±2, combinado con ball_x += ball_vx sin guard causa underflow u8.
- Correcto:
    if (ball_vy > 0 && ball_bottom >= PADDLE_Y &&
        ball_x + BALL_W >= paddle_x && ball_x < paddle_x + PADDLE_WIDTH) {
        ball_vy = -1;
        ball_y = PADDLE_Y - BALL_H;  /* reposicionar para evitar tunnel */
        /* ball_vx NO se toca */
    }
- Movimiento de bola: usar guard direccional, nunca suma directa:
    if (ball_vx > 0) { if (ball_x < 79) ball_x++; else ball_vx = -1; }
    else             { if (ball_x > 0)  ball_x--; else ball_vx =  1; }
    if (ball_vy > 0) { ball_y++; }          /* SIN rebote abajo — el floor check lo gestiona */
    else             { if (ball_y > 0)  ball_y--; else ball_vy =  1; }

CRÍTICO: NO añadir ningún límite ni rebote en y abajo dentro del movimiento.
  INCORRECTO (rebote):  if (ball_y >= FLOOR_Y - BALL_H) { ball_vy = -1; }
  INCORRECTO (clamp):   if (ball_y >= FLOOR_Y - BALL_H) { ball_y = FLOOR_Y - BALL_H; }
  INCORRECTO (clamp+rebote): if (ball_vy > 0) { ball_y++; if (ball_y >= 200-BALL_H) { ball_y=200-BALL_H; ball_vy=-1; }}
  Cualquiera de estos tres patrones impide que ball_y alcance FLOOR_Y → el floor check nunca dispara → las vidas nunca se decrementan → el game over nunca aparece.
  CORRECTO: la bola cae libremente; el floor check en update_game maneja la pérdida de vida:
    if (ball_y + BALL_H - 1 >= FLOOR_Y) { g_lives--; if (g_lives == 0) { game_over=1; draw_game_over(); } else reset_ball(); }

## 7) Plantilla generativa obligatoria para el pipeline
El pipeline debe seguir estas fases:

### Fase A: Normalizacion de prompt
Extraer una GameSpec interna:
- tipo de juego
- numero de entidades
- controles
- HUD requerido
- condiciones de victoria/derrota

### Fase B: Seleccion de plantilla base
Elegir plantilla por genero:
- breakout_like
- shooter_like
- platform_like
- topdown_like

### Fase C: Relleno de plantilla
Completar:
- constantes de tamano y limites
- layout de HUD
- estados iniciales
- transiciones de estado
- tablas de colores por entidad

### Fase D: Insercion de guardrails de codigo
Validaciones estaticas antes de compilar:
1. Existe init_game/update_game/draw_game/main.
2. Se llama cpct_scanKeyboard_f en loop.
3. Se llama cpct_waitVSYNC en loop.
4. Se configura modo 0.
5. Se configura paleta con cpct_setPALColour.
6. Se usan dimensiones reales en colisiones (w/h en formulas).
7. No hay dependencia de estado global sin init explicita.

### Fase E: Build y validacion automatica
1. make del output.
2. Si falla, autocorreccion hasta N intentos.
3. Si compila, ejecutar smoke test en emulador.
4. Captura de frame para inspeccion visual rapida.

## 8) Checklist de Definition of Done (DoD)
Un juego generado se considera valido si cumple todo:
- Compila sin errores.
- Arranca en emulador.
- Input basico funciona (movimiento/lanzamiento/disparo segun genero).
- Entidades principales visibles.
- Colisiones principales funcionales.
- HUD legible y no solapado.
- Si hay vidas/puntuacion, actualizan correctamente.

## 9) Errores recurrentes a bloquear en pipeline
- Mezclar pixeles y bytes en X o anchos.
- Colision de pelota usando solo punto (sin w/h).
- No inicializar vx/vy y estados en init_game.
- HUD con offsets incorrectos en modo 0.
- Hardcodear bytes de color incompatibles con paleta activa.
- Dejar modo de debug estatico activado por defecto.

## 10) Salida estructurada recomendada para trazabilidad
Ademas del codigo, el pipeline debe emitir un resumen JSON:

{
  "template": "breakout_like",
  "build_status": "ok|fail",
  "checks": {
    "functions_present": true,
    "palette_configured": true,
    "vsync_in_loop": true,
    "bbox_collisions": true,
    "hud_non_overlap": true
  },
  "runtime_notes": [
    "ball starts attached to paddle",
    "space launches ball"
  ]
}

## 11) Politica de fallback automatica
Si el juego compila pero no se ve jugable:
1. Activar modo diagnostico visual temporal:
   - borde color de test
   - marcadores grandes de entidades
2. Recolectar captura.
3. Aplicar parche de precision (coordenadas/collision) y desactivar diagnostico antes de entrega final.

## 12) Recomendacion para integracion RAG
Indexar esta especificacion junto con:
- ejemplos validos por genero
- lista de APIs CPCtelera permitidas
- anti-patrones detectados historicamente

Al generar codigo nuevo:
- recuperar primero esta especificacion
- recuperar 1 ejemplo del genero objetivo
- aplicar reglas de secciones 4, 5, 6 y 8 como hard constraints
