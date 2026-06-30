---
title: "Ficha híbrida: MSX"
platform: "msx"
category: ["hardware", "graphics", "audio", "memory", "storage"]
audience: ["pm", "programmer", "artist", "technical-lead"]
keywords: ["MSX", "MSX2", "Z80", "TMS9918A", "V9938", "AY-3-8910", "slots", "VDP"]
version: "1.0"
---

# MSX — Ficha híbrida hardware + producción

## Resumen ejecutivo

MSX (1983) es un estándar abierto creado por Microsoft y ASCII Corporation, no una máquina única. Múltiples fabricantes (Sony, Philips, Panasonic, Toshiba, etc.) produjeron MSX compatibles. Usa Z80, VDP TMS9918A (con sprites por hardware) y AY de sonido. Fue popular en Japón, España, Holanda, Brasil y Oriente Medio. El MSX2 (1985) mejoró significativamente el vídeo con el V9938.

## Especificaciones hardware (MSX1)

| Componente | Detalle |
|-----------|---------|
| **CPU** | Zilog Z80A @ 3,58 MHz |
| **RAM** | 64 KB (mínimo según estándar: 8 KB; la mayoría tienen 64 KB) |
| **ROM** | 32 KB (BIOS + BASIC) |
| **Vídeo** | Texas Instruments TMS9918A (VDP) |
| **Sonido** | General Instrument AY-3-8910 (3 canales + ruido) |
| **Almacenamiento** | Cinta, cartucho, disco (con interfaz) |
| **Slots** | 4 slots primarios (expansión de hardware/ROM/RAM) |

## Modos gráficos (MSX1 — TMS9918A)

| Modo | Resolución | Colores | Notas |
|------|-----------|---------|-------|
| **Screen 1** (Pattern) | 256×192 | 2 por bloque 8×1 (de 15) | Texto/tiles coloreados |
| **Screen 2** (Bitmap) | 256×192 | 2 por bloque 8×1 (de 15) | Bitmap con restricción de color por fila de 8 px |
| Screen 3 (Multicolor) | 64×48 bloques de 4×4 | 15 | Bloques grandes, poco útil para juegos |

**MSX2 (V9938):** añade Screen 5 (256×212, 16 colores por pixel de 256), Screen 7 (512×212, 16 colores), Screen 8 (256×212, 256 colores) y scroll por hardware. El salto MSX1→MSX2 es enorme para juegos.

## Sprites por hardware (TMS9918A)

| Propiedad | Valor |
|-----------|-------|
| Sprites simultáneos | **32** definidos, **4 por scanline** (el 5to desaparece) |
| Tamaño por sprite | 8×8 o 16×16 pixeles |
| Colores por sprite | **1** (monocolor, de 15) |
| Detección de colisiones | Hardware (flag de colisión, no por par) |
| Expansión | ×2 (magnification) |

**Impacto en producción:** 32 sprites suena bien, pero el límite de **4 por scanline** es la restricción real. Si 5 sprites se alinean horizontalmente, el 5to desaparece (flickering). El diseñador debe evitar alinear más de 4 sprites en la misma fila. El MSX2 sube a 8 por scanline.

## Sistema de slots

El MSX usa un sistema de **slots** para mapear ROM, RAM y periféricos en el espacio de direcciones del Z80 (64 KB). Hay 4 slots primarios, cada uno subdivisible en 4 sub-slots (16 posibles). Cada página de 16 KB del mapa de memoria puede apuntar a un slot diferente.

**Impacto en producción:** los slots son un concepto único del MSX. El programador debe gestionar qué slot está mapeado en cada página. Esto complica el acceso a ROM de cartucho, RAM extra y dispositivos. Es una fuente de bugs frecuente para novatos. Estimar 1 semana extra de aprendizaje para un programador nuevo en MSX.

## Sonido

Igual que CPC y Spectrum 128K: **AY-3-8910** (variante 8910 vs. 8912 del CPC, funcionalmente idénticos), 3 canales de onda cuadrada + ruido.

El MSX2 no mejora el sonido base, pero existe el **MSX-MUSIC** (OPLL/YM2413, FM synthesis de 9 canales) como expansión estándar en algunos MSX2+ y turboR.

## RAM libre para el programador

| Modelo | RAM total | Libre aprox. |
|--------|-----------|-------------|
| MSX1 (64 KB) | 64 KB | **~28 KB** (en BASIC; en ASM puro: ~48 KB desactivando BASIC) |
| MSX2 (128 KB+) | 128-512 KB | Variable, con mapper de memoria |

La VRAM del TMS9918A es **separada** (16 KB propios, no roba RAM principal). En MSX2 la VRAM del V9938 es 128 KB separada. Esto es una ventaja sobre CPC y Spectrum donde la VRAM consume RAM.

## Almacenamiento y carga

| Medio | Velocidad | Capacidad |
|-------|-----------|-----------|
| Cinta | 1200-2400 baud | Variable |
| Cartucho (ROM) | Instantáneo | 8-512 KB (MegaROMs) |
| Disco 3,5" | ~15 KB/s | 360-720 KB |

**MegaROMs**: cartuchos con bank switching que permiten hasta 512 KB (o más) de ROM. Es el formato preferido para juegos MSX ambiciosos: carga instantánea + mucho contenido.

## Puntos fuertes para juegos

- **Sprites por hardware** (32 definidos) con detección de colisiones.
- **VRAM separada**: la RAM principal queda libre para código y datos.
- **MegaROMs**: carga instantánea y hasta 512 KB de contenido.
- Estándar abierto: el código corre en cualquier MSX compatible.
- Comunidad homebrew activa (MSXdev anual, MSX.org).
- El MSX2 es un salto cualitativo enorme (256 colores, scroll HW, 128 KB VRAM).

## Puntos débiles

- **4 sprites por scanline** (MSX1): flickering con más de 4 sprites alineados.
- Sprites monocolor (MSX1): comparado con los multicolor del C64.
- Sistema de **slots** complejo para novatos.
- Screen 2 tiene restricción de color (2 por fila de 8px por bloque) → variante del color clash.
- Fragmentación de hardware: distintos fabricantes, distintas expansiones.

## Estimación de esfuerzo (referencia PM)

| Tarea | Esfuerzo estimado (ASM, 1 persona) |
|-------|-------------------------------------|
| Motor de sprites (usando HW, gestión scanline) | 1-2 semanas |
| Scroll por tiles (MSX1, software) | 2-3 semanas |
| Scroll por hardware (MSX2, V9938) | 1 semana |
| Gestión de slots/páginas | 1 semana de aprendizaje + integración |
| Motor MegaROM (bank switching) | 1-2 semanas |
| Juego sencillo completo (MSX1) | 2-3 meses |
| Juego medio (MSX2, scroll, niveles) | 4-7 meses |
