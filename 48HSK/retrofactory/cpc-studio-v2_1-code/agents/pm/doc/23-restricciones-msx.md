---
title: "Restricciones de producción: MSX"
platform: "msx"
category: ["restrictions", "production", "graphics", "audio", "memory", "storage"]
audience: ["pm", "programmer", "artist", "technical-lead"]
keywords: ["MSX", "MSX2", "TMS9918A", "V9938", "sprites", "scanline", "slots", "VDP", "MegaROM", "color clash"]
version: "1.0"
---

# MSX — Restricciones de producción

## Resumen

El MSX es un estándar abierto con múltiples fabricantes, lo que introduce una restricción única: fragmentación de hardware. Sus limitaciones gráficas principales son el límite de 4 sprites por scanline (MSX1), los sprites monocolor, y una forma particular de color clash en Screen 2. El sistema de slots es una fuente de complejidad sin equivalente en las otras 3 plataformas.

---

## 1. Sprites — 32 definidos, pero solo 4 por scanline

### Restricción: el 5º sprite en una línea horizontal desaparece

El TMS9918A puede manejar 32 sprites en total, pero solo dibuja **4 por cada línea de escaneo (scanline)**. Si 5 o más sprites coinciden en la misma línea horizontal, el 5º (y siguientes, por prioridad numérica) simplemente no se dibujan ese frame.

| Propiedad | MSX1 (TMS9918A) | MSX2 (V9938) |
|-----------|-----------------|--------------|
| Sprites definidos | 32 | 32 |
| Sprites por scanline | **4** | **8** |
| Tamaño | 8×8 o 16×16 | 8×8 o 16×16 |
| Colores por sprite | 1 (monocolor) | 1 por línea (multicolor por línea) |

### Qué significa para el PM

- **El límite real no son los 32 sprites sino los 4 por scanline.** Un juego que pone 5 enemigos alineados horizontalmente tendrá flickering obligatorio.
- **Solución por software: rotación de prioridad.** El programador rota el orden de los sprites cada frame para que el "desaparecido" alterne, creando un parpadeo distribuido (flickering controlado). Esto es normal en MSX y aceptado por los jugadores, pero debe ser consciente.
- **Impacto en diseño de juego**: los niveles deben diseñarse evitando acumular más de 4 objetos a la misma altura. En un shoot'em up, las oleadas de enemigos deben escalonarse verticalmente.
- **Presupuesto de diseño**: si el personaje del jugador ocupa 1 sprite (16×16), quedan 3 slots de scanline para enemigos/balas en esa franja. Con un personaje de 2 sprites (32×16), solo quedan 2.
- El MSX2 duplica a 8 por scanline, aliviando enormemente este problema. Si el target es MSX2, esta restricción se relaja mucho.

### Restricción: sprites monocolor (MSX1)

Cada sprite del TMS9918A tiene **un solo color** (de 15 posibles). No hay sprites multicolor como en C64.

### Qué significa para el PM

- Los personajes se ven "planos" comparados con C64.
- **Técnica de overlay**: superponer 2 sprites de distinto color en la misma posición para crear un sprite "bicolor". Gasta 2 slots de los 4 disponibles por scanline. El PM debe decidir: ¿personaje bonito (2 sprites) o más objetos en pantalla?
- El MSX2 (V9938) permite color diferente por línea horizontal del sprite, mejorando mucho sin gastar slots extra.

---

## 2. Gráficos de fondo — Color clash en Screen 2

### Restricción: 2 colores por bloque de 8×1 pixeles

En Screen 2 (el modo bitmap estándar para juegos MSX1), cada fila de 8 pixeles dentro de un tile de 8×8 solo puede usar 2 colores (ink + paper, de 15 posibles).

| Aspecto | Valor |
|---------|-------|
| Resolución | 256×192 |
| Unidad de restricción de color | 8×1 pixeles (fila dentro del tile) |
| Colores por unidad | 2 (ink + paper) |
| Colores totales paleta | 15 (fijos, no programables) |

### Qué significa para el PM

- Es un **color clash por fila de 8px**, similar al Spectrum pero con unidad más pequeña (8×1 vs 8×8). Esto da algo más de flexibilidad que el Spectrum pero menos libertad que el C64.
- El artista puede usar colores diferentes en cada fila del tile (8 filas = 8 pares de colores posibles por tile). Mejor que Spectrum (1 par por tile 8×8 completo).
- **En la práctica**: los fondos MSX1 tienen un look "rayado" cuando se intenta mezclar colores, con transiciones visibles cada 8 pixeles horizontales.
- **Paleta fija**: los 15 colores del TMS9918A no son programables. Lo que ves es lo que hay. No se puede ajustar la paleta como en CPC o C64. El artista debe diseñar dentro de estos colores concretos.
- El MSX2 (V9938) elimina esta restricción completamente con Screen 5 (256×212, 16 colores de 512 por pixel) y Screen 8 (256 colores). El salto de calidad visual es enorme.

---

## 3. Sistema de slots — Complejidad única

### Restricción: mapa de memoria fragmentado en slots/sub-slots

El Z80 del MSX ve 64 KB de espacio de direcciones, dividido en 4 páginas de 16 KB. Cada página puede mapearse a uno de 4 slots primarios, y cada slot puede subdividirse en 4 sub-slots (16 posibilidades por página).

| Página | Rango | Contenido típico |
|--------|-------|-----------------|
| 0 | 0x0000–0x3FFF | BIOS ROM (slot 0) |
| 1 | 0x4000–0x7FFF | Cartucho / RAM |
| 2 | 0x8000–0xBFFF | Cartucho / RAM |
| 3 | 0xC000–0xFFFF | RAM principal (siempre) |

### Qué significa para el PM

- **Es la restricción más "exótica" del MSX.** No tiene equivalente en CPC, Spectrum o C64. Un programador nuevo en MSX necesita ~1 semana solo para entender y manejar slots correctamente.
- **Fuente principal de bugs en desarrollo MSX.** Leer una dirección sin tener el slot correcto mapeado devuelve basura. Estos bugs son difíciles de diagnosticar porque dependen de la configuración de hardware del MSX concreto.
- **Fragmentación de hardware agrava el problema**: cada fabricante organizó los slots de forma diferente. Un cartucho puede estar en slot 1 o slot 2 según la máquina. El código robusto debe detectar en qué slot está.
- **MegaROMs añaden otra capa**: los cartuchos grandes (>32 KB) usan bank switching dentro del slot del cartucho. Cada mapper (Konami, ASCII, etc.) tiene un esquema diferente.
- **Estimación**: para un programador sin experiencia MSX, sumar 1-2 semanas al timeline solo por la curva de aprendizaje de slots. Para un programador con experiencia, es rutina.

### Restricción: acceso a RAM extra requiere mapper

Los MSX con más de 64 KB (128-512 KB en MSX2) usan un memory mapper para acceder a la RAM extra en bloques de 16 KB.

### Qué significa para el PM

- La RAM extra está ahí pero no es "transparente". Cada acceso a un bloque extra requiere programar el mapper.
- Almacenar datos grandes (gráficos de niveles, música) en RAM extra es viable pero el código de acceso añade complejidad y ciclos.
- Para juegos MSX1 (64 KB estándar), la RAM extra no es un factor. Para MSX2 (128 KB+), planificar qué datos van en mapper.

---

## 4. VRAM — Separada pero con acceso lento

### Restricción: la VRAM se accesa a través del VDP, no directamente

La VRAM del TMS9918A (16 KB) y del V9938 (128 KB) es memoria separada de la RAM principal. El Z80 no puede leer/escribir VRAM directamente: debe hacerlo a través de los puertos del VDP, byte a byte.

| Operación | Velocidad |
|-----------|-----------|
| Lectura VRAM (1 byte) | ~12 ciclos Z80 |
| Escritura VRAM (1 byte) | ~12 ciclos Z80 |
| Transferencia bloque 1 KB | ~12.000 ciclos (~3,3 ms) |

### Qué significa para el PM

- **Ventaja**: la VRAM no roba espacio de la RAM principal. Los 16 KB de VRAM son adicionales a los 64 KB de RAM.
- **Desventaja**: actualizar gráficos en pantalla es lento. Cada byte pasa por el cuello de botella del VDP.
- **Scrolling en MSX1 es costoso**: no hay scroll por hardware (el TMS9918A no lo soporta). Hacer scroll requiere reescribir grandes bloques de VRAM cada frame → muy pesado.
- **MSX2 tiene scroll por hardware** (registros del V9938) y comandos de copia VRAM-a-VRAM (blitter interno). Esto cambia radicalmente las posibilidades.
- **Regla para MSX1**: diseñar juegos flip-screen (cambio de pantalla completa) es mucho más viable que scroll suave. El scroll suave en MSX1 es posible pero consume la mayoría del frame.

---

## 5. Scroll — La gran carencia del MSX1

### Restricción: sin scroll por hardware en TMS9918A

El VDP del MSX1 no tiene registros de scroll. Todo scroll debe hacerse por software, reescribiendo la VRAM.

| Tipo de scroll | Viabilidad MSX1 | Viabilidad MSX2 |
|----------------|----------------|----------------|
| Flip-screen (pantalla completa) | Fácil | Fácil |
| Scroll por tiles (8px/step) | Viable, algo brusco | Trivial (HW) |
| Scroll fino (1px/step) | Muy costoso, 2-3 semanas | Fácil (registros V9938) |
| Scroll multidireccional | Extremadamente costoso | Viable (2 semanas) |

### Qué significa para el PM

- **MSX1: asumir juegos flip-screen por defecto.** El scroll suave es un lujo que consume la mayor parte del frame y requiere trucos avanzados.
- **MSX2: scroll es una feature estándar.** Los registros del V9938 dan scroll fino sin coste de CPU significativo.
- Si el cliente quiere un juego con scroll suave en MSX1, el PM debe advertir: +2-3 semanas de desarrollo, rendimiento comprometido, posible reducción de sprites/enemigos.
- Muchos juegos MSX1 exitosos (Konami incluida) usaron flip-screen o scroll por tiles a 8px. No es una limitación que impida buenos juegos; es una elección de diseño.

---

## 6. Sonido — Igual que CPC/Spectrum 128K

### Restricción: 3 canales AY-3-8910, compartidos música + SFX

Mismo chip y mismas restricciones que en CPC y Spectrum 128K.

| Aspecto | Valor |
|---------|-------|
| Canales | 3 onda cuadrada + 1 ruido (compartido) |
| Envolvente | 1 hardware (compartida entre canales) |
| Volumen | 16 niveles por canal |

### Qué significa para el PM

- Misma planificación que CPC: decidir split música/SFX (2+1 o 3+interrupt).
- **Herramienta de referencia**: Arkos Tracker (cross-platform con CPC y Spectrum 128K). Un mismo compositor puede cubrir las 3 plataformas Z80 con AY.
- **MSX-MUSIC (YM2413)**: expansión FM de 9 canales presente en MSX2+ y turboR. Si el target incluye estas máquinas, es un bonus significativo de audio. No planificar como base si el target es MSX1/MSX2 genérico.

---

## 7. Fragmentación de hardware — El precio del estándar abierto

### Restricción: cada fabricante implementó el estándar de forma diferente

A diferencia del Spectrum (1 fabricante), C64 (1 fabricante) o CPC (1 fabricante), el MSX tiene docenas de fabricantes con implementaciones diferentes:

| Variación | Impacto |
|-----------|---------|
| Distribución de slots | Código debe detectar dónde está |
| RAM (8-64 KB en MSX1) | Mínimo fiable: 64 KB (mayoría) pero existen 16/32 KB |
| Controladores de disco | Distintos (Philips, Sony, Panasonic) |
| Teclado | Layout varía por país/fabricante |
| Velocidad VDP | Varía ligeramente entre modelos |

### Qué significa para el PM

- **Testear en múltiples modelos (o emulador multi-modelo).** openMSX emula muchas variantes.
- **Target mínimo recomendado**: MSX1 con 64 KB RAM. Cubres ~90% de la base instalada.
- Los juegos en cartucho (ROM) son los más portables: no dependen de disco ni RAM extra. MegaROM es el formato ideal para distribución universal MSX.
- **Presupuestar 3-5 días extra** de testing de compatibilidad si se distribuye para hardware variado.
- Para distribución moderna (emulador), apuntar a un modelo específico popular (Sony HB-F9P, Philips MSX2 NMS 8250) y testear en 2-3 más.

---

## 8. Almacenamiento — Cartucho vs cinta vs disco

### Restricción: no hay formato único dominante

| Medio | Ventaja | Desventaja |
|-------|---------|-----------|
| Cartucho (ROM/MegaROM) | Instantáneo, portable | Caro de fabricar (hardware) |
| Cinta | Barato | Lento (1200-2400 baud), ~3-5 min carga |
| Disco 3,5" | Razonablemente rápido | No todos los MSX tienen disquetera |

### Qué significa para el PM

- **Para juegos MSX ambiciosos, el cartucho MegaROM es el formato rey.** Carga instantánea + hasta 512 KB de contenido. Es lo que usó Konami para sus títulos estrella (Metal Gear, Nemesis, etc.).
- El MegaROM requiere elegir un mapper (Konami, Konami SCC, ASCII 8KB, ASCII 16KB). Cada uno tiene características diferentes y el programador necesita ~1-2 semanas para implementar el bank switching.
- **El mapper Konami SCC** incluye un chip de sonido extra (5 canales de onda programable). Si se elige este mapper, se obtiene audio superior como bonus. Factor a considerar en la decisión técnica.
- Para distribución moderna (archivos ROM), no hay coste de fabricación. El MegaROM es la elección obvia.
- Los juegos de disco pueden cargar datos bajo demanda (niveles, gráficos) pero no todos los usuarios tienen disquetera. Si se elige disco, aceptar una base instalada menor.

---

## 9. Detección de colisiones — Hardware limitado

### Restricción: la detección de colisiones del TMS9918A no identifica qué sprites colisionan

El VDP tiene un flag de "colisión de sprites" que se activa cuando cualquier par de sprites se solapa. Pero no dice cuáles colisionaron.

### Qué significa para el PM

- **La detección hardware es casi inútil para juegos complejos.** Solo sirve para juegos con 2 sprites (jugador + 1 enemigo).
- En la práctica, toda la detección de colisiones se hace por software (comparar coordenadas X/Y de cada par de sprites). Esto es estándar y no añade mucha complejidad, pero consume ciclos.
- Con 10+ objetos activos, la detección por software (N² comparaciones) puede consumir ~500-1.500 ciclos/frame. Optimizable con bounding boxes y spatial partitioning.

---

## 10. Tabla resumen de restricciones

| Restricción | Impacto | Mitigación |
|-------------|---------|-----------|
| 4 sprites/scanline (MSX1) | Flickering con >4 alineados | Diseño vertical, rotación de prioridad |
| Sprites monocolor | Look "plano" | Overlay (gasta 2 slots) |
| Color clash 8×1 (Screen 2) | 2 colores por fila de tile | Diseño de paleta por zona |
| Paleta fija 15 colores | Sin ajuste de paleta | Diseñar dentro de los 15 colores |
| Sin scroll HW (MSX1) | Scroll suave muy costoso | Flip-screen o scroll por tiles |
| Sistema de slots | Complejidad de programación, bugs | +1-2 semanas curva aprendizaje |
| Fragmentación hardware | Testing complejo | MegaROM para portabilidad máxima |
| VRAM acceso lento (puerto) | Actualizar pantalla es costoso | Minimizar cambios por frame |
| Sin disco universal | No todos tienen disquetera | Cartucho como formato universal |
| Colisiones HW inútiles | Detección por software obligatoria | Budget de ciclos para N² checks |

---

## MSX1 vs MSX2 — Guía de decisión para el PM

| Factor | MSX1 | MSX2 |
|--------|------|------|
| Base instalada | Mayor (más máquinas) | Menor pero más capaz |
| Scroll | Software (costoso) | Hardware (trivial) |
| Colores | 15 fijos, 2 por fila 8px | 256 de 512, libre por pixel |
| Sprites/scanline | 4 | 8 |
| VRAM | 16 KB | 128 KB |
| Complejidad desarrollo | Media | Media-baja (más features HW) |
| Tiempo desarrollo similar | Base | -20-30% (hardware ayuda más) |

**Recomendación**: si el juego necesita scroll o más de 4 sprites/scanline, apuntar a MSX2. Si es flip-screen con pocos objetos, MSX1 maximiza audiencia.

---

## Checklist pre-producción MSX

1. [ ] ¿Target MSX1, MSX2, o ambos?
2. [ ] ¿Cuántos sprites por scanline necesita el diseño? (>4 en MSX1 = flickering aceptado)
3. [ ] ¿El juego necesita scroll? (MSX1 = flip-screen recomendado)
4. [ ] ¿Distribución en cartucho (MegaROM), disco o cinta?
5. [ ] ¿Qué mapper de MegaROM? (¿se quiere SCC para audio extra?)
6. [ ] ¿El programador tiene experiencia con el sistema de slots?
7. [ ] ¿Se ha definido el target mínimo de RAM (64 KB recomendado)?
8. [ ] ¿En cuántos modelos/fabricantes se va a testear?
