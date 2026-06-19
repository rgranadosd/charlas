# Stub slice: player_core_movement

## Objective
Definir una slice mínima centrada en movimiento base del personaje y estructura inicial de integración.

## Implementation notes
- Usar una sola fuente de verdad para la posición X del sprite.
- Evitar colisiones y lógica de animación en esta primera slice.
- Mantener el bucle principal simple y legible.
- Preparar el código para futura extracción a player.c y player.h.

## Validation checks
- Existe src/main.c en el proyecto.
- El main.c contiene lectura de teclado.
- El main.c contiene espera a VSYNC.
- El main.c actualiza posición horizontal.
- Se genera un manifest JSON de artefactos.
- Se genera un documento markdown con resumen de la slice.
