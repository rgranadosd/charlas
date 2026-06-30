---
title: "Ficha híbrida: Amstrad CPC"
platform: "amstrad-cpc"
category: ["hardware", "graphics", "audio", "memory", "storage"]
audience: ["pm", "programmer", "artist", "technical-lead"]
keywords: ["CPC", "Z80", "464", "6128", "Gate Array", "AY-3-8912", "Mode 0", "Mode 1"]
version: "1.0"
---

# Amstrad CPC — Ficha híbrida hardware + producción

## Resumen ejecutivo

El Amstrad CPC (1984) es una máquina Z80 con una paleta de color generosa (27 colores), sonido AY de 3 canales y un diseño de vídeo basado en la CPU (sin sprites por hardware). Fue muy popular en Europa continental, especialmente España y Francia. Su punto fuerte para juegos es el color; su punto débil es que todo el movimiento de sprites recae en el procesador.

## Especificaciones hardware

| Componente | Detalle |
|-----------|---------|
| **CPU** | Zilog Z80A @ 4 MHz |
| **RAM** | 64 KB (CPC 464) / 128 KB (CPC 6128) |
| **ROM** | 32 KB (BASIC + firmware) |
| **Vídeo** | Gate Array (Amstrad custom), sin chip de vídeo dedicado |
| **Sonido** | General Instrument AY-3-8912 (3 canales + ruido) |
| **Almacenamiento** | Cinta (464), disco 3" (6128), ambos en el 664 |
| **Resolución display** | 50 Hz PAL, 160 o 200 líneas útiles |

## Modos gráficos

| Modo | Resolución | Colores simultáneos | Bytes por línea | Uso típico |
|------|-----------|---------------------|-----------------|------------|
| **Mode 0** | 160×200 | 16 de 27 | 80 | Juegos (más color, pixeles gordos) |
| **Mode 1** | 320×200 | 4 de 27 | 80 | Juegos con más detalle, aventuras |
| **Mode 2** | 640×200 | 2 de 27 | 80 | Texto, procesadores de texto |

**Impacto en producción:** Mode 0 da un look "colorido pero tosco" (pixeles anchos de 2:1). Mode 1 equilibra detalle y color. La elección de modo se fija al inicio del proyecto y afecta a todo el pipeline de arte.

## Organización de memoria de vídeo

La VRAM del CPC es peculiar: ocupa 16 KB de la RAM principal (direcciones `0xC000–0xFFFF` por defecto) y las líneas NO son contiguas en memoria. Cada línea de 80 bytes está separada de la siguiente por 2048 bytes (8 bloques de 200 líneas entrelazadas). Esto complica el cálculo de direcciones para dibujar sprites.

**Impacto en producción:** el entrelazado de líneas hace que dibujar sprites sea ~20% más lento que en una disposición lineal. Los programadores necesitan tablas precalculadas de direcciones de línea. Esto se estima al planificar: una rutina de sprites robusta puede llevar 2-3 semanas de desarrollo en ASM.

## Sonido

- **AY-3-8912**: 3 canales de onda cuadrada + 1 canal de ruido (compartido).
- Registro de volumen por canal con envolvente hardware simple.
- Sin capacidad de muestreo (samples) por hardware; se pueden hacer por software consumiendo CPU.

**Impacto en producción:** la música compite con los efectos de sonido por los 3 canales. El compositor suele reservar 1 canal para SFX dinámicos. Usar samples por software bloquea la CPU durante la reproducción.

## Almacenamiento y carga

| Medio | Velocidad | Capacidad | Tiempo carga típico (48 KB) |
|-------|-----------|-----------|---------------------------|
| Cinta (464) | 2000 baud | ~540 KB (C90) | ~4-5 minutos |
| Disco 3" (6128) | ~10 KB/s | 178 KB por cara (360 KB total) | ~5 segundos |

**Impacto en producción:** los juegos de cinta necesitan pantallas de carga, cargadores multi-parte y diseño "por bloques". Los juegos de disco pueden cargar niveles bajo demanda.

## RAM libre para el programador

| Modelo | RAM total | Ocupada por sistema | Libre aprox. |
|--------|-----------|--------------------|--------------| 
| CPC 464 | 64 KB | ~16 KB (VRAM) + ~1 KB (firmware vars) | **~42 KB** |
| CPC 6128 | 128 KB | ~17 KB | **~42 KB** base + 64 KB en bancos extra |

Con los bancos extra del 6128 se pueden almacenar gráficos, datos de niveles o código paginado. El acceso a bancos requiere gestión manual (`OUT` al Gate Array).

## Puntos fuertes para juegos

- Paleta de 27 colores (la más amplia de las 4 plataformas 8-bit principales).
- Mode 0 con 16 colores simultáneos: ideal para juegos coloridos.
- Disco 3" integrado en el 6128: carga rápida sin hardware adicional.
- Comunidad homebrew activa (CPCRetroDev anual).

## Puntos débiles

- **Sin sprites por hardware**: todo movimiento es software. Mover un sprite grande (24×32) consume ~10-15% del frame en ASM optimizado.
- Entrelazado de VRAM complica el código de dibujo.
- El disco 3" es propietario (caro, frágil, 178 KB/cara).
- Menor base instalada que Spectrum o C64 (pero fuerte en España y Francia).

## Estimación de esfuerzo (referencia PM)

| Tarea | Esfuerzo estimado (ASM, 1 persona) |
|-------|-------------------------------------|
| Motor de sprites software (16×16, 4 dirs) | 2-3 semanas |
| Scroll por tiles (mapa grande) | 2-4 semanas |
| Motor de música AY (player) | 1-2 semanas (o usar Arkos Tracker) |
| Pipeline de arte (herramientas + assets base) | 1-2 semanas |
| Juego sencillo completo (1 pantalla, sin scroll) | 2-3 meses |
| Juego medio (scroll, varios niveles, menús) | 4-8 meses |
