---
title: "Restricciones de producción: Commodore 64"
platform: "commodore-64"
category: ["restrictions", "production", "graphics", "audio", "memory"]
audience: ["pm", "programmer", "artist", "musician", "technical-lead"]
keywords: ["C64", "VIC-II", "SID", "sprites", "raster", "multiplexado", "fastloader", "1541", "6510", "budget CPU"]
version: "1.0"
---

# Commodore 64 — Restricciones de producción

## Resumen

El C64 es la máquina 8-bit más potente en multimedia (VIC-II + SID), pero su CPU a ~1 MHz impone un presupuesto de ciclos estricto. Las restricciones no vienen tanto del hardware gráfico/sonoro (que es generoso) sino de la CPU lenta, el almacenamiento lentísimo y la complejidad de las técnicas avanzadas (multiplexado, raster IRQ).

---

## 1. CPU — El cuello de botella principal

### Restricción: ~1 MHz efectivo (0,985 MHz PAL)

El MOS 6510 corre a menos de 1 MHz real. Además, el VIC-II "roba" ciclos de CPU durante las badlines (líneas donde lee datos de carácter): 40 ciclos por badline, cada 8 líneas de pantalla.

| Concepto | Valor |
|----------|-------|
| Ciclos por frame (PAL) | 19.656 ciclos |
| Ciclos robados por VIC-II (badlines) | ~1.000 por frame |
| Ciclos disponibles (sin border tricks) | ~18.600 por frame |
| Tiempo por frame | 20 ms (50 Hz PAL) |

### Qué significa para el PM

- **Todo compite por los mismos ~18.600 ciclos/frame.** Música SID (~1.500-3.000 ciclos), lógica de juego, scroll, y multiplexado de sprites comparten el mismo presupuesto.
- Un juego con multiplexado + scroll + música puede consumir el 80-90% del frame solo en sistemas. Queda poco para lógica de juego compleja.
- **Regla práctica**: pide al programador un "budget de ciclos" antes de diseñar features. Si el frame ya está al 75%, añadir un sistema de partículas puede ser inviable.
- A diferencia de las máquinas Z80 (3,5-4 MHz), aquí cada instrucción extra duele mucho más. El 6510 compensa parcialmente con instrucciones que hacen más por ciclo (modo de direccionamiento zero page), pero el margen es estrecho.

---

## 2. Sprites — 8 por hardware, el multiplexado es complejo

### Restricción: 8 sprites simultáneos por frame

El VIC-II muestra 8 sprites. Si el juego necesita más (enemigos, balas, explosiones), hay que **multiplexar**: reprogramar registros del VIC-II mediante interrupciones de raster para reutilizar sprites en zonas inferiores de la pantalla.

| Técnica | Sprites visibles | Complejidad | Ciclos extra |
|---------|-----------------|-------------|-------------|
| Sin multiplexado | 8 | Baja | 0 |
| Multiplexado simple (zonas fijas) | 12-16 | Media | ~2.000-3.000/frame |
| Multiplexado avanzado (ordenamiento Y) | 16-24 | Alta | ~4.000-6.000/frame |

### Qué significa para el PM

- **8 sprites "gratis" no requieren planificación especial.** Es la zona de confort: si el juego puede funcionar con 8 objetos en pantalla, el desarrollo es rápido (~1 semana para el motor de sprites).
- **Más de 8 sprites = multiplexado obligatorio.** Esto añade 2-3 semanas de desarrollo y es una fuente de bugs visuales (flickering si sprites se cruzan en la misma banda vertical).
- El diseñador de juego debe **planificar verticalmente**: evitar que muchos sprites se alineen en la misma franja de scanlines. Un shoot'em up con oleadas de enemigos necesita diseño de patrones consciente del multiplexado.
- **Sprites expandidos (×2)** duplican tamaño visual pero siguen contando como 1 sprite. Útil para jefes o personajes grandes sin gastar sprites extra.

### Restricción: tamaño fijo 24×21 (standard) o 12×21 (multicolor)

Los sprites tienen tamaño fijo. Un personaje más grande que 24×21 requiere componer varios sprites (overlay), gastando slots del VIC-II.

| Personaje | Sprites necesarios | Impacto |
|-----------|-------------------|---------|
| Pequeño (24×21 o menos) | 1 | Sin problema |
| Medio (48×21) | 2 (overlay horizontal) | Reduce slots a 6 libres |
| Grande (48×42) | 4 (2×2 overlay) | Reduce slots a 4 libres |

### Qué significa para el PM

- Un jefe final de 4 sprites deja solo 4 para el jugador + balas + enemigos menores. El diseñador debe planificar los encuentros de jefe con un "sprite budget" explícito.
- Alternativa: usar gráficos de fondo (chars) para partes estáticas del jefe y sprites solo para las partes animadas.

---

## 3. Scroll — Hardware ayuda, pero consume CPU

### Restricción: scroll fino HW limitado a 0-7 px, el software hace el resto

El VIC-II da scroll fino de 0-7 pixeles gratis. Cada 8 pixeles el programador debe desplazar toda la pantalla en memoria (scroll grueso) y dibujar la nueva columna/fila.

| Tipo de scroll | Ciclos/frame | Complejidad |
|----------------|-------------|-------------|
| Scroll 1 dirección | ~3.000-5.000 | Media |
| Scroll 4 direcciones | ~6.000-10.000 | Alta |
| Parallax (2 capas) | ~8.000-12.000 | Muy alta |

### Qué significa para el PM

- Scroll de 1 dirección es estándar en C64 y relativamente económico (1-2 semanas).
- **Scroll multidireccional consume un tercio del frame.** Si además hay multiplexado + música, el presupuesto de CPU está al límite.
- El parallax (dos fondos a distinta velocidad) es una feature premium que puede requerir 3-4 semanas extra y forzar sacrificios en otros sistemas.
- **Regla**: no prometas scroll multidireccional + más de 12 sprites + música compleja sin validar con el programador que el budget de ciclos cierra.

---

## 4. Sonido SID — 3 canales para todo

### Restricción: 3 osciladores compartidos entre música y SFX

El SID tiene 3 canales. La música típica usa los 3. Los efectos de sonido necesitan al menos 1 canal. Conflicto inevitable.

| Estrategia | Música | SFX | Calidad percibida |
|-----------|--------|-----|-------------------|
| 2 canales música + 1 SFX dedicado | Media | Buena | Equilibrada |
| 3 canales música, SFX interrumpe | Alta | Irregular | Mejor música, peor UX |
| Música pausa durante SFX | Alta (cuando suena) | Buena | Inconsistente |

### Qué significa para el PM

- **El compositor debe saber desde el día 1 cuántos canales tiene.** Esta decisión afecta al diseño musical completo.
- Un juego con SFX frecuentes (disparo cada 0,5s) necesita 1 canal dedicado → música a 2 voces. El compositor debe diseñar para 2 canales desde el inicio, no adaptar una composición de 3.
- **Alternativa avanzada**: el "canal de SFX" puede alternar entre canales según qué nota está sonando (duck al canal menos audible). Esto requiere integración estrecha músico-programador (~1 semana extra).
- El driver de música SID consume ~1.500-3.000 ciclos/frame. Un driver complejo (con filtro, arpegios, vibrato) puede consumir 4.000+. Pide al compositor/programador que estime el coste antes de aprobar features musicales avanzadas.

### Restricción: diferencia SID 6581 vs 8580

El SID 6581 (C64 original/breadbin) y el 8580 (C64C) suenan diferente, especialmente el filtro. Una música optimizada para uno puede sonar mal en el otro.

### Qué significa para el PM

- Si el juego se distribuye en cartucho/disco para hardware real, debe sonar aceptable en ambas revisiones.
- El compositor debe testear en ambos (los emuladores modelan ambos).
- Presupuestar 2-3 días extra para ajuste de filtro "cross-SID".

---

## 5. Almacenamiento — El disco 1541 es una pesadilla

### Restricción: 400 bytes/s sin fastloader

La unidad de disco 1541 transfiere ~400 bytes por segundo en modo estándar (protocolo serial IEEE-488 por bit). Cargar 50 KB toma ~2 minutos.

| Solución | Velocidad | Complejidad | Compatibilidad |
|----------|-----------|-------------|---------------|
| Sin fastloader | 400 B/s | Ninguna | Total |
| Fastloader software | 3-5 KB/s | 2-3 semanas dev | Alta (la mayoría de 1541) |
| Fastloader + IRQ loader | 5-8 KB/s | 3-4 semanas | Media (problemas con clones) |
| Cartucho (EasyFlash, etc.) | Instantáneo | 1 semana integración | Solo con hardware |

### Qué significa para el PM

- **Todo juego comercial serio necesita fastloader.** Sin él, los tiempos de carga destruyen la experiencia.
- Desarrollar un fastloader propio requiere 2-3 semanas de un programador experimentado. Alternativa: usar un loader existente (Krill's Loader, SpinDle) que reduce a ~1 semana de integración.
- **El fastloader consume RAM** (~1-2 KB de código residente en el C64 + espacio en la 1541). Este espacio no está disponible para el juego.
- Los niveles del juego deben diseñarse considerando la velocidad de carga. Un nivel que requiere 30 KB de datos nuevos tardará ~4 segundos con fastloader. Diseñar transiciones que disimulen la carga.
- **Cartucho** elimina el problema pero limita distribución (necesita hardware especial). Para distribución digital moderna (emuladores), los formatos .crt (cartucho) o .d64 (disco con fastloader integrado) son ambos viables.

### Restricción: 170 KB por lado del disco (340 KB total)

Un disco 1541 almacena ~170 KB por cara. Un juego grande necesita doble cara o múltiples discos.

### Qué significa para el PM

- 170 KB parece poco, pero para juegos 8-bit es generoso. La mayoría de juegos caben en un lado.
- Juegos ambiciosos (RPGs, aventuras gráficas) pueden necesitar disco doble cara o "flip disk" → estimar pantalla de "por favor, dé la vuelta al disco".
- La compresión es esencial: tiles y sprites se almacenan comprimidos y se descomprimen en RAM. Estimar ~30% de ahorro con compresión básica (RLE/LZ).

---

## 6. RAM — 64 KB parecen mucho, pero...

### Restricción: espacio de direcciones compartido con I/O y ROM

El 6510 mapea ROM (BASIC, Kernal, Char ROM) e I/O (VIC-II, SID, CIA) en el mismo espacio de 64 KB que la RAM. Para acceder a toda la RAM hay que desactivar ROMs, pero entonces se pierden las rutinas del sistema.

| Configuración | RAM libre | Notas |
|--------------|-----------|-------|
| BASIC + Kernal activos | ~38 KB | Modo por defecto |
| Solo Kernal | ~51 KB | Lo habitual en juegos |
| Todo desactivado | ~60 KB | Extremo, necesita handler de IRQ propio |

### Qué significa para el PM

- **51 KB es el máximo práctico** para juegos. Es la mayor cantidad de las 4 plataformas.
- Pero esos 51 KB deben contener: código del juego, motor de sprites, motor de scroll, driver de música, fastloader, datos de nivel actuales, sprites en memoria, charset. Se llena rápido.
- **Mapa de memoria obligatorio**: el programador debe entregar un mapa de memoria al inicio del proyecto mostrando cómo se distribuyen los 51 KB. Este documento es crítico para planificación.
- Los datos de sprites del VIC-II deben estar en un banco de 16 KB específico (el VIC-II solo "ve" 16 KB a la vez, configurable entre 4 bancos). Esto restringe dónde se pueden colocar los gráficos.
- **Bancos VIC-II**: los sprites y charsets deben residir en el banco activo del VIC-II. Cambiar de banco es posible pero requiere sincronización con el raster.

---

## 7. Color y gráficos de fondo

### Restricción: modo multicolor = 160×200 (pixeles anchos 2:1)

El modo más usado para juegos (multicolor bitmap/chars) tiene pixeles de doble ancho: resolución real de 160×200. Los sprites multicolor también tienen pixeles anchos (12×21 real).

### Qué significa para el PM

- El artista debe diseñar para pixeles anchos (aspect ratio 2:1). Herramientas como SpritePad muestran la proporción correcta.
- Los gráficos parecen "gordos" comparados con hi-res (320×200). Es un look distintivo del C64.
- El modo hi-res (320×200) existe pero con solo 2 colores por celda 8×8 → color clash similar al Spectrum. Casi ningún juego de acción lo usa.

### Restricción: 4 colores por celda 4×8 en modo multicolor

En multicolor character/bitmap, cada celda de 4×8 pixeles puede usar 4 colores: 1 fondo global + 3 por celda.

### Qué significa para el PM

- Menos restrictivo que el Spectrum (que limita a 2 colores por 8×8), pero el artista aún debe planificar paletas por zona.
- Los sprites (colores independientes) mitigan el problema: el jugador y enemigos se ven bien sobre cualquier fondo porque sus colores no dependen de la celda.
- **Consejo para el artista**: diseñar el fondo con paleta coherente por zona y confiar en los sprites para los elementos que cruzan múltiples zonas de color.

---

## 8. Raster IRQ — La técnica maestra y su coste

### Restricción: las técnicas avanzadas del C64 requieren interrupciones sincronizadas con el raster

El multiplexado de sprites, los border tricks, el parallax y los efectos de color cycling dependen de programar interrupciones (IRQ) que se disparan en scanlines específicas del VIC-II.

| Técnica | Raster IRQs necesarias | Complejidad | Riesgo de bugs |
|---------|----------------------|-------------|---------------|
| Multiplexado 12-16 sprites | 3-6 | Media | Medio |
| Split-screen (scroll + panel) | 1-2 | Baja | Bajo |
| Border opening | 1-2 por borde | Media | Bajo |
| Parallax por raster | 10-20+ | Muy alta | Alto |

### Qué significa para el PM

- **Toda técnica avanzada del C64 depende de raster IRQ.** Un programador sin experiencia en IRQ tardará 2-3 semanas solo en aprenderlas. Factor de riesgo.
- Las IRQs son frágiles: un ciclo de más y el efecto "se rompe" visualmente (glitches de 1 frame). Debugging es difícil.
- **Estimar 50% más tiempo de debug** para features basadas en raster IRQ comparado con código secuencial.
- La estabilización de raster (conseguir que la IRQ se dispare en el ciclo exacto) es un arte en sí mismo. Existen técnicas documentadas (doble IRQ, timer CIA) pero requieren experiencia.

---

## 9. Compatibilidad de hardware

### Restricción: variantes del C64 (breadbin, C64C, SX-64, C128 en modo C64)

| Variante | Diferencia clave |
|----------|-----------------|
| C64 "breadbin" (1982) | SID 6581, VIC-II 6569 (PAL) |
| C64C (1986+) | SID 8580, mismo VIC-II | 
| SX-64 (portátil) | Sin datasette, monitor integrado |
| C128 en modo C64 | Compatible, 2 MHz disponible en modo C128 |

### Qué significa para el PM

- El 99% de los juegos son compatibles con todas las variantes.
- El único problema práctico es el SID (6581 vs 8580): testear audio en ambos.
- Para distribución moderna (emuladores), la compatibilidad no es problema.
- Para hardware real (eventos retro, carreras de hardware), testear en al menos breadbin + C64C.

---

## 10. Tabla resumen de restricciones

| Restricción | Impacto | Mitigación |
|-------------|---------|-----------|
| CPU ~1 MHz | Todo compite por ciclos | Budget de ciclos, código optimizado |
| 8 sprites HW | Multiplexado si >8 | Diseño vertical, zona management |
| Sprite tamaño fijo 24×21 | Personajes grandes gastan slots | Overlay + fondo |
| Disco 1541 lento | Tiempos de carga | Fastloader obligatorio |
| 3 canales SID | Música vs SFX | Canal dedicado SFX desde día 1 |
| 170 KB/cara disco | Juegos grandes = multi-cara | Compresión + streaming niveles |
| Modo multicolor 160×200 | Pixeles anchos | Diseño para aspect ratio 2:1 |
| Raster IRQ frágil | Bugs visuales | +50% tiempo debug |
| VIC-II banco 16 KB | Gráficos deben estar en banco activo | Mapa de memoria cuidadoso |
| SID 6581 vs 8580 | Audio diferente | Testear ambos, 2-3 días ajuste |

---

## Checklist pre-producción C64

1. [ ] ¿Cuántos sprites simultáneos necesita el juego? (>8 = multiplexado obligatorio)
2. [ ] ¿Scroll de 1 dirección o multidireccional?
3. [ ] ¿Cuántos canales para música vs SFX?
4. [ ] ¿Distribución en disco (necesita fastloader) o cartucho?
5. [ ] ¿El programador tiene experiencia con raster IRQ?
6. [ ] ¿Se ha definido el mapa de memoria (51 KB)?
7. [ ] ¿El artista diseña para pixeles anchos (multicolor)?
8. [ ] ¿El compositor testea en SID 6581 y 8580?
