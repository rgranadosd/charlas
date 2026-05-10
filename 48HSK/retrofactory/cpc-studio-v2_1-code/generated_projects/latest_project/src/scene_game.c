#include "game.h"
#include "systems/input.h"
#include "entities/player.h"

/* Auto-generated notes
Video mode: Mode 1

Gameplay:
Juego tipo 'avoidance' con mecánica ultra-simple: el jugador controla una nave (sprite de 16x16 píxeles) en la parte inferior de la pantalla, moviéndose horizontalmente para esquivar obstáculos (sprites de 8x8 o 16x16 píxeles) que caen desde la parte superior. 

- **Controles**: Teclado (O/P para mover izquierda/derecha) o joystick, con respuesta inmediata y sin inercia para maximizar la sensación de control. 
- **Mecánica**: Los obstáculos caen a velocidad constante, aumentando progresivamente (pero de forma sutil) para incrementar la dificultad. 
- **Puntuación**: Se otorga 1 punto por cada obstáculo esquivado, mostrando el marcador en la esquina superior derecha. 
- **Vidas**: 3 vidas, perdiendo una al colisionar con un obstáculo. Game over al agotarlas. 
- **Feedback visual**: Parpadeo breve de la nave al perder una vida y sonido de 'beep' para confirmar acciones (movimiento, colisión). 
- **Objetivo**: Sobrevivir el mayor tiempo posible y batir el récord de puntuación.

**Detalles técnicos**: 
- Sprites: 1 nave (16x16, 2 frames de animación para parpadeo), 2 tipos de obstáculos (8x8 o 16x16, sin animación). 
- Colisiones: Bounding boxes simplificadas para evitar cálculos costosos. 
- Sonido: Efectos básicos con el PSG (ej: beep al moverse, tono más grave al colisionar). 
- Pantalla: Mode 1 (320x200, 4 colores), con fondo estático y sin scroll para priorizar rendimiento.

Art:
- **Modo de vídeo**: Mode 1 (320x200, 4 colores) para equilibrio entre resolución y rendimiento. 
- **Paleta de colores**: 
  - Color 0: Negro (fondo). 
  - Color 1: Azul oscuro (obstáculos y detalles del fondo). 
  - Color 2: Azul claro (nave del jugador y elementos destacados). 
  - Color 3: Blanco (contornos y detalles para maximizar contraste). 
- **Diseño de sprites**: 
  - **Nave del jugador**: 16x16 píxeles, diseño simétrico con forma de 'V' invertida para facilitar la identificación. Contorno blanco y relleno en azul claro. 
  - **Obstáculos**: 
    - Tipo 1: 8x8 píxeles, forma de rombo (contorno blanco, relleno azul oscuro). 
    - Tipo 2: 16x16 píxeles, forma cuadrada con esquinas recortadas (contorno blanco, relleno azul oscuro). 
  - **Marcador**: Dígitos de 8x8 píxeles en blanco sobre fondo negro, con diseño pixel art claro y legible. 
  - **Vidas**: Iconos de 8x8 píxeles representando miniaturas de la nave en azul claro. 
- **Fondo**: Estático, con un degradado suave de azul oscuro a negro en la parte superior para simular profundidad, y líneas horizontales sutiles en azul claro para dar sensación de movimiento. 
- **Colisiones**: Bounding boxes simplificadas (rectángulos) para evitar cálculos costosos, priorizando la precisión sobre la complejidad. 
- **Herramientas**: 
  - **Diseño de sprites**: Aseprite (para crear y exportar los sprites en formato compatible con CPCtelera). 
  - **Integración**: Sprites exportados como arrays de bytes para su uso directo en el código con CPCtelera. 
  - **Optimización**: Comprimir sprites con herramientas como `cpct_zx7` si el espacio en memoria es crítico.

Tech:
**Fase 1: Configuración inicial (1 día)**
- Crear el proyecto con `cpct_mkproject` y configurar el Makefile.
- Configurar el modo de vídeo (Mode 1) y la paleta de colores.
- Implementar el doble buffer y probar el intercambio de buffers.

**Fase 2: Diseño e integración de sprites (2 días)**
- Crear los sprites en Aseprite (nave, obstáculos, dígitos) y exportarlos como arrays de bytes.
- Integrar los sprites en el proyecto y probar su renderizado.
- Comprimir sprites con `cpct_zx7` si es necesario.

**Fase 3: Lógica del juego (3 días)**
- Implementar la lectura de controles (teclado/joystick) y el movimiento de la nave.
- Programar la generación y caída de obstáculos, con aumento progresivo de velocidad.
- Implementar colisiones con bounding boxes y la lógica de vidas/puntuación.
- Añadir el parpadeo de la nave al perder una vida.

**Fase 4: Renderizado y sonido (2 días)**
- Implementar el renderizado del fondo, obstáculos, nave, marcador y vidas.
- Asegurar que el renderizado ocurra en el buffer inactivo y sincronizar con el barrido de la pantalla.
- Crear efectos de sonido simples (beep para movimiento, tono grave para colisión) e integrarlos.

**Fase 5: Interrupciones y optimización (2 días)**
- Configurar una interrupción de raster para sincronizar la lógica del juego y el renderizado.
- Optimizar el código para reducir el uso de CPU y memoria (ej: evitar bucles anidados, reutilizar sprites).
- Probar el juego en un emulador y ajustar la dificultad.

**Fase 6: Pruebas y ajustes (2 días)**
- Probar el juego en un emulador (ej: Retro Virtual Machine) y en hardware real si es posible.
- Ajustar la velocidad de los obstáculos, la respuesta de los controles y la dificultad.
- Corregir bugs y optimizar el rendimiento.

**Fase 7: Documentación y entrega (1 día)**
- Documentar el código y las decisiones técnicas.
- Incluir instrucciones para compilar y ejecutar el juego.
- Preparar el proyecto para su entrega final.
*/

void game_init(void) {
    player_init();
}

void game_update(void) {
    input_update();
    player_update();
}

void game_render(void) {
    player_render();
}
