---
title: "Ficha híbrida: Commodore 64"
platform: "commodore-64"
category: ["hardware", "graphics", "audio", "memory", "storage"]
audience: ["pm", "programmer", "artist", "musician", "technical-lead"]
keywords: ["C64", "6510", "VIC-II", "SID", "sprites", "raster", "IRQ"]
version: "1.0"
---

# Commodore 64 — Ficha híbrida hardware + producción

## Resumen ejecutivo

El Commodore 64 (1982) es probablemente la máquina 8-bit más capaz en hardware multimedia. Su chip de vídeo **VIC-II** ofrece 8 sprites por hardware con detección de colisiones, scroll fino y modos multicolor. Su chip de sonido **SID** (6581/8580) es legendario: 3 osciladores con formas de onda seleccionables, filtro resonante analógico y ADSR. Es la plataforma de referencia para juegos ambiciosos y demoscene. Dominó en Norteamérica; importante también en Europa.

## Especificaciones hardware

| Componente | Detalle |
|-----------|---------|
| **CPU** | MOS 6510 @ ~1 MHz (0,985 MHz PAL) |
| **RAM** | 64 KB |
| **ROM** | 20 KB (BASIC + Kernal + Char ROM) |
| **Vídeo** | MOS VIC-II (6569 PAL / 6567 NTSC) |
| **Sonido** | MOS SID (6581 rev1 / 8580 rev2) |
| **Almacenamiento** | Datasette (cinta), disco 5¼" (1541), cartucho |

## Modos gráficos

| Modo | Resolución | Colores | Notas |
|------|-----------|---------|-------|
| Standard Character (texto) | 320×200 (40×25 chars) | 16 (1 global bg + 1 por char) | Modo por defecto |
| Multicolor Character | 160×200 | 4 por celda 4×8 (de 16) | Pixeles anchos (2:1) |
| Standard Bitmap | 320×200 | 2 por celda 8×8 | Hi-res, color clash similar a Spectrum |
| **Multicolor Bitmap** | 160×200 | 4 por celda 4×8 | El más usado para juegos gráficos |

**Impacto en producción:** el modo Multicolor Bitmap + sprites es la combinación habitual para juegos de acción. El artista trabaja en bloques de 4×8 con 4 colores por celda. A diferencia del Spectrum, el color clash se mitiga con los sprites (que tienen colores independientes del fondo).

## Sprites por hardware (VIC-II)

| Propiedad | Valor |
|-----------|-------|
| Sprites simultáneos | **8** (numerados 0-7) |
| Tamaño por sprite | 24×21 pixeles (standard) o 12×21 multicolor |
| Colores por sprite | 1 propio + 2 compartidos (multicolor) |
| Expansión | ×2 horizontal y/o vertical |
| Detección de colisiones | Hardware (sprite-sprite y sprite-fondo) |
| Multiplexado | Reprogramando registros VIC-II por rasterline se pueden tener **más de 8** en pantalla |

**Impacto en producción:** los sprites son la gran ventaja del C64. El programador no necesita borrar/redibujar: el VIC-II los compone sobre el fondo automáticamente. El multiplexado (técnica avanzada) requiere IRQs de raster, que añade complejidad pero permite 16-24+ sprites visibles.

## Scroll por hardware

El VIC-II ofrece **scroll fino** de 0-7 pixeles en X e Y a nivel de registro, combinado con scroll grueso (por carácter). Esto permite scroll suave con bajo coste de CPU: solo hay que mover 1 columna/fila de tiles por cada 8 pixeles.

**Impacto en producción:** los juegos de scroll lateral/vertical son la especialidad del C64. El programador necesita ~1 semana para un scroll básico (vs. ~3 semanas en Spectrum sin HW scroll).

## Sonido (SID)

| Propiedad | Valor |
|-----------|-------|
| Osciladores | 3 independientes |
| Formas de onda | Triángulo, diente de sierra, pulso (ancho variable), ruido |
| Envolvente ADSR | 1 por oscilador (Attack, Decay, Sustain, Release) |
| Filtro | Paso bajo, paso alto, paso banda (analógico, resonante) |
| Ring modulation | Sí (entre osciladores) |
| Sync | Sí (hard sync entre osciladores) |

**Impacto en producción:** el SID es un sintetizador completo. La música del C64 es la mejor de las 4 plataformas por lejos. Un compositor con experiencia en SID puede producir audio con calidad cercana a 16-bit. Herramienta principal: GoatTracker.

## RAM libre para el programador

| Segmento | Rango | Tamaño | Notas |
|----------|-------|--------|-------|
| BASIC free | `0x0800–0x9FFF` | 38 KB | Sin BASIC desactivado: hasta 51 KB |
| Char ROM / I/O | `0xD000–0xDFFF` | 4 KB | Banqueable |
| Kernal ROM | `0xE000–0xFFFF` | 8 KB | Desactivable |

Desactivando BASIC y Kernal: **~51 KB libres** (la mayor cantidad de las 4 plataformas).

## Almacenamiento y carga

| Medio | Velocidad | Tiempo carga (50 KB) |
|-------|-----------|---------------------|
| Datasette | 300 baud (estándar) | ~15 minutos (¡) |
| Datasette + turbo | ~3000 baud | ~2 minutos |
| Disco 1541 | ~400 bytes/s (estándar) | ~2 minutos |
| Disco 1541 + fastloader | ~4 KB/s | ~12 segundos |
| Cartucho | Instantáneo | — |

**Impacto en producción:** la unidad de disco 1541 es **lentísima** sin fastloader. Todo juego comercial serio incluía su propio fastloader. Los cartuchos (8-16 KB) dan carga instantánea pero limitan tamaño.

## Puntos fuertes para juegos

- **Sprites HW + scroll HW** = la mejor máquina 8-bit para acción/scroll.
- **SID** = el mejor sonido de la generación.
- 51 KB de RAM libre (máximo de las 4).
- Demoscene masiva: décadas de trucos y técnicas documentadas.
- Tooling moderno excelente (KickAssembler, SpritePad, GoatTracker, VICE).

## Puntos débiles

- CPU a **~1 MHz**: la más lenta (Z80 corre a 3,5-4 MHz). El 6510 compensa parcialmente con instrucciones más eficientes por ciclo.
- Set de instrucciones del 6510 más limitado que el Z80 (sin instrucciones de 16 bits, menos registros).
- Disco 1541 lento sin fastloader.
- Resolución multicolor es solo 160×200 (pixeles anchos).

## Estimación de esfuerzo (referencia PM)

| Tarea | Esfuerzo estimado (ASM, 1 persona) |
|-------|-------------------------------------|
| Motor de sprites (usando HW, 8 sprites) | 1 semana |
| Multiplexado de sprites (>8 en pantalla) | 2-3 semanas |
| Scroll suave (1 dirección, tiles) | 1-2 semanas |
| Scroll multidireccional | 3-4 semanas |
| Driver de música SID (player) | 1-2 semanas (o usar GoatTracker) |
| Fastloader de disco | 2-3 semanas |
| Juego sencillo completo (1 pantalla, sprites) | 1-2 meses |
| Juego medio (scroll, música, niveles) | 3-6 meses |
