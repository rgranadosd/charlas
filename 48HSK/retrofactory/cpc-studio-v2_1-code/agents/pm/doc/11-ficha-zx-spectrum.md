---
title: "Ficha híbrida: ZX Spectrum"
platform: "zx-spectrum"
category: ["hardware", "graphics", "audio", "memory", "storage"]
audience: ["pm", "programmer", "artist", "technical-lead"]
keywords: ["Spectrum", "Z80", "48K", "128K", "ULA", "atributos", "color clash", "beeper"]
version: "1.0"
---

# ZX Spectrum — Ficha híbrida hardware + producción

## Resumen ejecutivo

El ZX Spectrum (1982) fue la máquina 8-bit más popular en Reino Unido y España. CPU Z80 a 3,5 MHz, sistema de color basado en atributos 8×8 (famoso "color clash") y sonido beeper monocanal (mejorado a AY en el 128K). Su enorme base instalada y la simplicidad de su arquitectura lo convierten en la plataforma con más catálogo homebrew y la más accesible para empezar.

## Especificaciones hardware

| Componente | Detalle |
|-----------|---------|
| **CPU** | Zilog Z80A @ 3,5 MHz |
| **RAM** | 48 KB (48K) / 128 KB (128K) |
| **ROM** | 16 KB (48K) / 32 KB (128K) |
| **Vídeo** | ULA (Uncommitted Logic Array), sin sprites HW |
| **Sonido** | Beeper 1-bit (48K) / AY-3-8912 (128K) |
| **Almacenamiento** | Cinta (estándar), Microdrive, disco (con interfaz) |
| **Resolución display** | 50 Hz PAL |

## Modo gráfico (único)

| Resolución | Colores | Atributos | Bytes VRAM |
|-----------|---------|-----------|-----------|
| 256×192 | 8 colores × 2 tonos (normal/bright) = 15 | 1 byte por celda 8×8 (ink + paper + bright + flash) | 6912 bytes (6144 bitmap + 768 atributos) |

**Solo hay un modo gráfico.** La resolución es fija. Cada celda de 8×8 pixeles comparte 1 color de tinta (ink) y 1 de fondo (paper). Si dos objetos de distinto color se solapan en la misma celda 8×8, uno de los dos pierde su color → **color clash**.

**Impacto en producción:** el color clash es LA restricción central del diseño visual en Spectrum. Obliga a decisiones estéticas tempranas: monocromo (muchos juegos), sprites de 1 color sobre fondo negro, o diseño muy cuidadoso de la rejilla 8×8. El artista necesita entender los atributos desde el día 1.

## Organización de memoria de vídeo

La VRAM (6912 bytes) está en `0x4000–0x5AFF`. El bitmap está organizado en tercios (cada tercio cubre 64 líneas), y dentro de cada tercio las líneas están entrelazadas por carácter (similar al CPC). Los atributos de color están contiguos al final (`0x5800–0x5AFF`).

## Sonido

**48K — Beeper**: un altavoz de 1 bit controlado por software. No tiene chip de sonido: el programador genera ondas toggling un bit del puerto `0xFE`. Esto consume CPU al 100% mientras suena. Aun así se han logrado motores de beeper de 2-3 canales pseudo-simultáneos (usando PWM por software).

**128K — AY-3-8912**: 3 canales de onda cuadrada + ruido, igual que el CPC/MSX. Dos mundos completamente distintos de audio.

**Impacto en producción:** para 48K hay que decidir si la música suena durante el juego (bloquea CPU) o solo en menús. Para 128K, el motor de música AY es estándar. Un juego multiplataforma 48K+128K necesita dos drivers de sonido.

## Almacenamiento y carga

| Medio | Velocidad | Tiempo carga típico (48 KB) |
|-------|-----------|---------------------------|
| Cinta (estándar) | 1500 baud | ~5-6 minutos |
| Cinta (turbo loader) | 3000-4000 baud | ~2-3 minutos |
| Microdrive | ~15 KB/s | ~3 segundos (poco fiable) |
| Disco +3 | ~10 KB/s | ~5 segundos |

## RAM libre para el programador

| Modelo | RAM total | Ocupada por sistema | Libre aprox. |
|--------|-----------|--------------------|--------------| 
| 48K | 48 KB | ~6,75 KB (VRAM) + ~256 bytes (sys vars) | **~41 KB** |
| 128K | 128 KB | ~7 KB | **~41 KB** + 80 KB en bancos (5 bancos de 16 KB) |

El 128K permite paginar bancos de 16 KB para datos, gráficos extra o doble buffer de pantalla (banco 5 y 7 son los dos buffers de vídeo).

## Puntos fuertes para juegos

- **Enorme base instalada** y catálogo: más fácil encontrar referencias y código ejemplo.
- Arquitectura simple: la curva de aprendizaje es la más baja de las 4 plataformas.
- VRAM compacta (6912 bytes): borrar/repintar pantalla es rápido.
- Comunidad homebrew **muy activa** (ZX Dev, WOS, Spectrum Next).
- Mucha tooling moderna (FUSE, Pasmo, z88dk).

## Puntos débiles

- **Color clash**: la restricción visual más dura de las 4 plataformas.
- **Sin sprites por hardware**: como el CPC, todo es software.
- Z80 a 3,5 MHz: el más lento de los Z80 de las 4 plataformas (CPC=4 MHz, MSX=3,58 MHz).
- Beeper del 48K es muy limitado para música en juego.
- Contención de memoria: la ULA roba ciclos de CPU al acceder a la VRAM (primeros 16 KB), ralentizando ~30% el código que dibuja en pantalla.

## Estimación de esfuerzo (referencia PM)

| Tarea | Esfuerzo estimado (ASM, 1 persona) |
|-------|-------------------------------------|
| Motor de sprites software (16×16, monocromo) | 1-2 semanas |
| Motor de sprites con gestión de atributos | 3-4 semanas |
| Scroll por tiles (pantalla completa) | 2-3 semanas |
| Motor de beeper (48K, 1 canal) | 1 semana |
| Motor de beeper multicanal (48K) | 3-4 semanas |
| Juego sencillo completo (flip-screen) | 1-2 meses |
| Juego medio (scroll, varios niveles) | 3-6 meses |
