# Breakout postmortem y guardrails para autogeneracion

## Objetivo
Registrar de forma precisa los fallos reales encontrados durante la generacion de Breakout en CPCtelera y convertirlos en reglas obligatorias para que el pipeline no repita esos errores.

## Fallos observados en la practica
1. Pantalla gris/negra por uso inconsistente de paleta.
2. Entidades invisibles por mezclar bytes y pixeles en coordenadas X.
3. Bloques invisibles por anchos interpretados como pixeles cuando la API espera bytes.
4. Pelota aparentemente inexistente por tamano exagerado o posicion fuera de la logica esperada.
5. Pelota inmovil por estado no inicializado correctamente o modo de debug estatico activo.
6. Rebote en pala defectuoso por colision basada en un solo punto en lugar de caja completa.
7. HUD desalineado por no considerar ancho real de caracteres en modo 0.
8. Capturas de validacion no concluyentes por solape de ventanas del host.

## Causas raiz
- No aplicar de forma estricta semantica de APIs CPCtelera:
  - cpct_getScreenPtr usa X en bytes.
  - cpct_drawSolidBox usa width en bytes.
- Colisiones calculadas con coordenada superior izquierda de la pelota, ignorando BALL_W/BALL_H.
- Dependencia de inicializadores globales en lugar de inicializacion runtime en init_game.
- Falta de modo de validacion visual determinista separado del modo gameplay.

## Reglas obligatorias para el pipeline
### R1. Inicializacion runtime explicita
Todas las variables de estado deben inicializarse en init_game:
- posicion y velocidad
- score/lives
- flags de estado (ej. ball_launched, game_over)

No depender de valores globales por defecto.

### R2. Colision por caja (AABB)
Siempre calcular:
- right = x + w - 1
- bottom = y + h - 1

Y usar overlap real para:
- paredes
- techo
- suelo
- pala
- bloques

### R3. Modo 0: unidades correctas
- X y width en bytes.
- Documentar en constantes si representan bytes o scanlines.

### R4. Color robusto
- Configurar paleta con cpct_setPALColour.
- Construir bytes de color con cpct_px2byteM0(pen, pen).
- Evitar hardcodes de bytes de color salvo casos validados.

### R5. HUD sin solapes
- En modo 0: 1 caracter de cpct_drawStringM0 = 4 bytes de ancho.
- Posicionar labels y valores con esa metrica.

### R6. Estados de gameplay claros
Para Breakout:
- attached: pelota pegada a pala
- launched: pelota en movimiento

Transiciones:
- Space: attached -> launched
- perder vida: launched -> attached

### R7. Debug mode controlado
Si se activa un modo visual estatico para diagnostico:
- Debe estar con flag explicito.
- Debe desactivarse antes de marcar build como final/master.

## Checklist automatico (gate)
Una build NO pasa si alguna regla falla:
1. Compila sin errores.
2. Existe init_game/update_game/draw_game/main.
3. cpct_scanKeyboard_f y cpct_waitVSYNC en loop principal.
4. Uso de BALL_W/BALL_H en formulas de colision.
5. Uso de cpct_setPALColour en init.
6. Uso de cpct_px2byteM0 para colores de entidades principales.
7. HUD sin overlap en coordenadas objetivo.
8. Estado de lanzamiento (attached/launched) presente en Breakout-like.

## Politica de validacion visual
- Hacer al menos una captura limpia del emulador con ventana visible y sin overlays.
- Confirmar visualmente: bloques, pelota, pala, HUD.
- Si algo no aparece, activar marcador visual temporal y repetir.

## Salida minima de auditoria para cada run
El pipeline debe guardar un resumen estructurado por run con:
- prompt original
- estado de checks (pass/fail)
- parametros de entidad (x,y,w,h,vx,vy)
- paleta aplicada
- ruta del output generado
- estado final (master_candidate true/false)

## Criterio para promover a master
Solo promover output a master si:
- build y run OK
- controles basicos OK
- colision pala OK
- HUD legible
- sin debug estatico activo
