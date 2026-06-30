---
title: "Restricciones del Amstrad CPC y su impacto en produccion"
platform: "amstrad-cpc"
category:
  - hardware
  - production
audience:
  - pm
  - programmer
  - technical-lead
keywords:
  - restricciones
  - modo-0
  - modo-1
  - sprites-software
  - vram
  - gate-array
  - ay-sound
  - bank-switching
  - planificacion
  - pipeline-arte
  - presupuesto-cpu
version: "1.0"
---

# Restricciones del Amstrad CPC y su impacto en produccion

Este documento recoge las limitaciones tecnicas mas relevantes del Amstrad CPC
desde la perspectiva de un PM o technical lead que necesita planificar un
proyecto de juego para esta plataforma. Cada seccion describe la restriccion,
la cuantifica cuando es posible y cierra con un bloque de impacto en
produccion.

---

## 1. Modo 0 vs Modo 1: el dilema color-resolucion

El Gate Array del CPC ofrece tres modos de video, pero en la practica los
juegos eligen entre dos:

| Modo   | Resolucion   | Colores simultaneos | Pixeles por byte |
|--------|-------------|---------------------|------------------|
| Modo 0 | 160 x 200   | 16 (de 27)          | 2                |
| Modo 1 | 320 x 200   | 4 (de 27)           | 4                |

### El trade-off en detalle

- **Modo 0** da 16 colores pero los pixeles son anchos (el doble que en
  Modo 1). Los graficos parecen "gordos"; los sprites pierden definicion en
  silueta pero ganan en degradados y sombras.
- **Modo 1** duplica la resolucion horizontal, pero solo permite 4 colores
  simultaneos. Los sprites son mas nitidos pero la paleta es muy limitada,
  y el artista debe recurrir a tramados (dithering) para simular tonos
  intermedios.

La decision de modo afecta a **todo** el pipeline grafico: tiles, sprites,
fuentes, pantallas de carga y HUD. Cambiar de modo a mitad de produccion
equivale a rehacer el 100 % del arte.

Algunos juegos mezclan modos (por ejemplo, HUD en Modo 1 y area de juego en
Modo 0) usando cambio de modo por linea de raster, pero esto consume ciclos
de CPU y requiere un programador experimentado en manejo de interrupciones
del Gate Array.

> **Que significa para el PM**
>
> - La eleccion de modo de video debe cerrarse en pre-produccion, antes de
>   que el artista empiece a producir assets. Un cambio posterior invalida
>   todo el arte existente.
> - Si el juego necesita graficos coloridos (plataformas, aventuras), se
>   elige Modo 0. Si necesita legibilidad y texto (estrategia, RPG), se
>   elige Modo 1.
> - La mezcla de modos por raster anade 2-4 semanas de trabajo tecnico y
>   aumenta el riesgo de bugs visuales. Solo es justificable si el diseno
>   lo exige.
> - El PM debe documentar la eleccion de modo como decision de diseno
>   inamovible en el GDD tecnico.

---

## 2. Sin sprites por hardware: el coste CPU de los sprites software

A diferencia del C64 o el MSX, el CPC **no tiene hardware de sprites**. Todo
sprite visible en pantalla se dibuja por software: el programa copia bloques
de bytes a la VRAM, gestionando mascaras de transparencia manualmente.

### Coste por sprite (estimaciones tipicas en Modo 0)

| Tamano sprite | Bytes en VRAM | Ciclos aprox. por frame | % de frame (50 Hz) |
|---------------|--------------|------------------------|---------------------|
| 8 x 8 px      | 32           | ~800                   | ~1 %                |
| 16 x 16 px    | 128          | ~3 200                 | ~4 %                |
| 24 x 24 px    | 288          | ~7 200                 | ~9 %                |
| 32 x 32 px    | 512          | ~12 800                | ~16 %               |

Un frame a 50 Hz dispone de ~80 000 ciclos utiles (ver seccion 8 sobre
throughput efectivo). Con 4 sprites de 16x16 ya se consume un 16 % del frame
solo en dibujo de sprites, sin contar borrado, logica ni scroll.

El borrado de sprites tambien consume tiempo: hay que restaurar el fondo que
habia debajo antes de dibujar la nueva posicion. Las tecnicas habituales son:

- **Guardar fondo** (save-under): duplica el coste de memoria.
- **Dirty rectangles**: requiere logica adicional de gestion de zonas sucias.
- **Doble buffer**: necesita 16 KB extra de RAM para un segundo buffer de
  pantalla, algo prohibitivo en el 464 (64 KB totales).

### Sprites con mascara

Para transparencia, cada byte del sprite necesita un byte de mascara. La
rutina tipica es:

```
LD A,(fondo)       ; 7 ciclos
AND (mascara)      ; 7 ciclos
OR (sprite)        ; 7 ciclos
LD (pantalla),A    ; 7 ciclos
```

Esto duplica el tiempo respecto a un sprite opaco sin mascara.

> **Que significa para el PM**
>
> - El numero y tamano de sprites en pantalla es una **restriccion dura** que
>   debe fijarse en el GDD. No se puede prometer "enemigos ilimitados".
> - Regla de oro para presupuesto: reservar como maximo el 30-35 % del frame
>   para sprites (dibujo + borrado). Eso permite ~4-6 sprites de 16x16.
> - Cada sprite adicional tiene un coste lineal en CPU. Si el disenador pide
>   un sprite extra, el PM debe preguntar: "que quitamos?".
> - El artista debe trabajar con tamaños de sprite predefinidos y
>   estandarizados para que las rutinas de dibujo sean optimas.
> - Prever 1-2 semanas extra para optimizar rutinas de sprites en
>   ensamblador si el juego es action-heavy.

---

## 3. VRAM entrelazada: la complejidad del layout de pantalla

La memoria de video del CPC no es lineal. La pantalla de 16 KB se organiza
en 8 bloques de 2 KB cada uno, entrelazados:

```
Linea 0   -> direccion &C000
Linea 1   -> direccion &C800
Linea 2   -> direccion &D000
Linea 3   -> direccion &D800
Linea 4   -> direccion &E000
Linea 5   -> direccion &E800
Linea 6   -> direccion &F000
Linea 7   -> direccion &F800
Linea 8   -> direccion &C050
Linea 9   -> direccion &C850
...
```

Cada grupo de 8 lineas consecutivas en pantalla esta separado por 2 KB en
memoria. Para calcular la direccion de un pixel dado (x, y), hay que:

1. Determinar en que bloque de 8 lineas cae (y DIV 8).
2. Calcular el offset dentro del bloque (y MOD 8) * &800.
3. Sumar el desplazamiento horizontal.

### Impacto practico

- Las rutinas de dibujo de sprites no pueden simplemente incrementar un
  puntero para pasar a la siguiente linea; necesitan saltos de 2 KB.
- La solucion estandar es usar **tablas de lookup** de 200 entradas (una
  por linea de pantalla), que ocupan 400 bytes de RAM y eliminan el calculo
  en tiempo real.
- El scroll vertical requiere actualizar la base de pantalla por hardware
  (CRTC R12/R13), lo cual permite scroll a nivel de caracter (8 pixeles)
  sin coste, pero el scroll pixel a pixel exige redibujar.

> **Que significa para el PM**
>
> - La programacion de rutinas de video es mas compleja que en plataformas
>   con VRAM lineal. Factor de dificultad: x1.5 respecto a una maquina
>   con layout lineal.
> - Reservar tablas de lookup en memoria (400-800 bytes). En un 464 con
>   solo 64 KB, cada byte cuenta.
> - El scroll suave vertical es caro; el horizontal tambien requiere
>   programacion CRTC. El PM debe confirmar con el lead tecnico si el
>   genero del juego necesita scroll y de que tipo antes de comprometerse.
> - Si el equipo no tiene experiencia previa con CPC, prever una fase de
>   prototipado tecnico de 1-2 semanas solo para validar las rutinas de
>   video.

---

## 4. Contencion del Gate Array: ciclos robados por el hardware

El Gate Array del CPC es responsable de generar la senal de video, y para
ello accede a la RAM durante la visualizacion de la pantalla. El Z80 y el
Gate Array comparten el bus de memoria, y el Gate Array tiene prioridad.

### Mecanismo

Durante cada linea de pantalla visible, el Gate Array necesita leer 2 bytes
por microsegundo para alimentar la salida de video. El Z80 funciona a 4 MHz,
lo que significa 4 ciclos por microsegundo. Cuando el Gate Array accede a la
RAM, el Z80 es detenido insertando estados de espera (wait states).

### Numeros concretos

- **Durante la zona visible** (256 ciclos de la linea de 64 us): el Z80
  pierde aproximadamente 2 ciclos de cada 4 por contencion. Throughput
  efectivo: ~50 % del nominal.
- **Durante blanking horizontal y vertical**: sin contencion; el Z80
  funciona a velocidad completa.
- **Media ponderada por frame**: de los ~80 000 ciclos nominales por frame
  (a 50 Hz), el Z80 ejecuta efectivamente ~55 000-60 000 ciclos utiles,
  dependiendo de la configuracion CRTC.

Esto significa que la CPU "real" es mas cercana a un Z80 a 2.7-3 MHz
efectivos durante la visualizacion activa.

> **Que significa para el PM**
>
> - Los benchmarks de rendimiento no pueden hacerse con la pantalla apagada;
>   hay que medir siempre con display activo.
> - El presupuesto de ciclos por frame disponible para logica + graficos +
>   sonido es ~55 000-60 000, no los 80 000 nominales.
> - Las rutinas criticas (sprites, scroll) pueden programarse para ejecutar
>   durante el blanking vertical (~6 000 ciclos sin contencion) pero ese
>   tiempo es muy limitado.
> - Si un programador dice "funciona perfecto" pero ha testeado con la
>   pantalla desactivada, hay que pedir retest con display activo. La
>   diferencia puede ser del 25-30 %.

---

## 5. Sonido AY-3-8912: 3 canales para todo

El chip de sonido AY presente en todos los CPC ofrece:

- 3 canales de onda cuadrada (tonos).
- 1 generador de ruido (compartido con los 3 canales).
- Envolventes de volumen por hardware (limitadas a formas predefinidas).

### El problema de asignacion

Musica y efectos de sonido compiten por los mismos 3 canales. Las estrategias
habituales son:

| Estrategia            | Canales musica | Canales SFX | Pro                     | Contra                       |
|-----------------------|---------------|-------------|-------------------------|------------------------------|
| Musica prioritaria    | 3             | 0           | Musica completa         | Sin SFX durante gameplay     |
| Split fijo            | 2             | 1           | Equilibrio predecible   | Musica pierde un canal       |
| Robo de canal         | 2-3           | 1 (robado)  | Musica casi completa    | SFX interrumpe una voz       |
| Solo SFX en gameplay  | 0             | 3           | SFX ricos               | Sin musica en juego           |

La decision de split afecta directamente al compositor: si solo tiene 2
canales, debe adaptar sus arreglos. Y el disenador de SFX debe saber cuantos
efectos simultaneos puede tener.

### CPU para sonido

El driver de musica tipico (Arkos Tracker, WYZPlayer) consume entre 3 % y
8 % del frame, dependiendo de la complejidad de la partitura. Los efectos de
sonido anaden otro 1-2 % si usan el mismo driver.

> **Que significa para el PM**
>
> - La politica de canales (cuantos para musica, cuantos para SFX) debe
>   decidirse en pre-produccion y comunicarse a compositor y disenador de
>   sonido.
> - Si el juego necesita SFX constantes (shooter, accion), considerar
>   musica de 2 canales o silenciar musica durante gameplay.
> - El compositor debe componer **para el limite real de canales**, no
>   componer en 3 y luego "recortar". Eso produce musica que suena rota.
> - Anadir sonido digitalizado (samples PCM) es posible pero consume
>   enormes cantidades de CPU (~50 %+) y memoria. Solo viable para efectos
>   puntuales como voces en intro.

---

## 6. 178 KB por cara de disco: limitacion de tamano de juego

El formato de disco estandar del CPC (DATA format) permite almacenar
aproximadamente **178 KB por cara** de un disco de 3 pulgadas.

### Desglose tipico del espacio

| Componente          | Tamano tipico  | Notas                              |
|---------------------|---------------|-------------------------------------|
| Motor de juego      | 15-25 KB      | Codigo Z80 comprimido               |
| Graficos (tiles)    | 20-40 KB      | Depende del modo de video           |
| Sprites             | 10-30 KB      | Incluye mascaras                    |
| Mapas/niveles       | 15-40 KB      | Comprimidos con RLE o similares     |
| Musica              | 5-15 KB       | Depende del tracker usado           |
| SFX                 | 2-5 KB        | Definiciones de efectos             |
| Pantallas de carga  | 16 KB c/u     | Una pantalla = 16 KB sin comprimir  |
| **Total disponible**| **~178 KB**   | Por cara de disco                   |

Un juego ambicioso con multiples niveles puede necesitar **2 caras de disco**
o incluso **2 discos**, lo que complica la logistica de carga y la experiencia
de usuario (pedir al jugador que de la vuelta al disco o cambie de disco).

### Compresion

Los datos se comprimen tipicamente con:

- **Exomizer** o **ZX0**: ratios de 40-60 % en graficos.
- **RLE** para mapas con muchas repeticiones.
- La descompresion tarda entre 0.5 y 2 segundos para un bloque de 16 KB,
  lo cual es aceptable durante pantallas de carga pero no durante gameplay.

> **Que significa para el PM**
>
> - El PM debe mantener un **presupuesto de espacio en disco** actualizado
>   durante toda la produccion (spreadsheet con tamanos por asset).
> - 178 KB es el techo duro por cara. Si el juego crece, hay que planificar
>   multi-carga (multi-load), lo que anade complejidad al loader y tiempos
>   de espera para el jugador.
> - Cada pantalla de carga sin comprimir ocupa 16 KB (~9 % del disco).
>   Considerar si realmente necesitamos pantallas de carga decorativas.
> - La compresion es obligatoria; el plan debe incluir tiempo para
>   integrar y testear el compresor/descompresor.
> - Para ediciones en cinta, el espacio es menos problema pero los tiempos
>   de carga son mucho mayores (~3 min para 48 KB). El PM debe decidir la
>   estructura de multi-load pensando en la paciencia del jugador.

---

## 7. Bank switching en el 6128: 128 KB con complejidad

El CPC 6128 dispone de 128 KB de RAM, pero el Z80 solo puede direccionar
64 KB a la vez. Los 64 KB extra se acceden mediante **bank switching**
controlado por el Gate Array.

### Modelo de memoria

```
&0000-&3FFF  (16 KB) - RAM baja / banco conmutable
&4000-&7FFF  (16 KB) - RAM central
&8000-&BFFF  (16 KB) - RAM alta
&C000-&FFFF  (16 KB) - VRAM / banco conmutable
```

El programador puede mapear bloques de 16 KB de la RAM extra en las
posiciones &4000-&7FFF o &C000-&FFFF, pero:

- El codigo que se ejecuta **no puede estar en el banco conmutado** (si
  conmutas la zona donde esta el PC, crash inmediato).
- Los datos en la RAM extra solo son accesibles cuando el banco
  correspondiente esta mapeado.
- Hay que gestionar cuidadosamente que banco esta activo en cada momento.

### Patrones de uso

- **Doble buffer**: un buffer de pantalla en la VRAM principal (&C000) y
  otro en la RAM extra. Se alterna cual es visible. Elimina flickering pero
  consume 16 KB extra.
- **Almacen de assets**: graficos, musica o mapas pre-cargados desde disco
  en los bancos extra, accesibles sin recarga de disco.
- **Codigo paginado**: rutinas que no se necesitan simultaneamente se colocan
  en bancos distintos (editor de niveles vs motor de juego).

### Compatibilidad con el 464/664

Si el juego debe funcionar en los tres modelos, el bank switching es
un **extra opcional**, no un requisito. Esto crea dos versiones de facto:
una version "base" para 464 (64 KB) y una version "mejorada" para 6128
(128 KB) con mas niveles, musica en memoria, o doble buffer.

> **Que significa para el PM**
>
> - Decision critica: soportar solo 6128 o ser compatible con 464?
>   - Solo 6128: mas memoria, pero excluyes ~40 % de la base instalada
>     (en la epoca).
>   - Compatible 464: mas mercado, pero el juego esta limitado a 64 KB.
>   - Hibrido: version base 464 + extras en 6128. Anade trabajo de testing
>     (dos configuraciones) y posibles bugs de compatibilidad.
> - Si se usa bank switching, el programador necesita un **mapa de memoria**
>   detallado que documente que hay en cada banco y cuando esta activo.
>   El PM debe exigir este documento.
> - El testing debe cubrir ambas configuraciones (464 y 6128) si se
>   busca compatibilidad. Doblar la matriz de test.
> - Estimar 1-2 semanas extra de desarrollo para implementar y depurar
>   bank switching correctamente.

---

## 8. Throughput efectivo: 4 MHz que no lo son

El Z80A del CPC funciona a 4 MHz nominales, pero la velocidad real de
ejecucion es significativamente menor debido a la contencion del Gate Array
(ver seccion 4).

### Calculo de throughput real

| Concepto                     | Ciclos por frame (50 Hz) |
|------------------------------|-------------------------|
| Ciclos nominales (4 MHz)     | 79 872                  |
| Perdidos por contencion      | ~19 000-24 000          |
| **Ciclos utiles efectivos**  | **~55 000-60 000**      |

### Comparacion con otras plataformas

| Plataforma       | CPU            | MHz nominal | MHz efectivo (aprox.) |
|------------------|----------------|------------|----------------------|
| **CPC**          | Z80A           | 4.0        | ~2.7-3.0             |
| ZX Spectrum      | Z80A           | 3.5        | ~2.5 (con contencion)|
| Commodore 64     | 6510 (6502)    | ~1.0       | ~1.0 (sin contencion)|
| MSX              | Z80A           | 3.58       | ~3.58 (sin contencion en TMS9918)|

El CPC tiene la CPU mas rapida en papel, pero la contencion lo nivela.
Sigue siendo mas rapido que el C64 en bruto, pero el C64 compensa con
sprites y scroll por hardware.

### Presupuesto de frame tipico para un juego de accion

| Tarea                 | Ciclos estimados | % del frame util |
|-----------------------|-----------------|------------------|
| Lectura de input      | 1 000           | ~2 %             |
| Logica de juego       | 8 000-12 000    | ~15-20 %         |
| IA enemigos           | 5 000-8 000     | ~9-14 %          |
| Dibujo de sprites     | 12 000-18 000   | ~22-30 %         |
| Borrado de sprites    | 8 000-12 000    | ~14-20 %         |
| Scroll/actualizacion  | 5 000-10 000    | ~9-17 %          |
| Sonido (driver)       | 3 000-5 000     | ~5-8 %           |
| **Total**             | **42 000-66 000** | **76-110 %**   |

Cuando el total supera el 100 %, el juego no puede mantener 50 fps y cae a
25 fps (un frame si, uno no) o presenta slowdowns.

> **Que significa para el PM**
>
> - Los 4 MHz del CPC son enganosos. El throughput real es un ~70 % del
>   nominal. Todo calculo de rendimiento debe usar los ciclos utiles.
> - Un juego de accion que quiera correr a 50 fps tiene un margen
>   **extremadamente ajustado**. La mayoria de juegos CPC comerciales
>   corren a 25 fps o incluso 16.7 fps (un frame de cada 3).
> - El PM debe establecer un **target de framerate** consensuado con el
>   equipo tecnico desde el inicio: 50, 25 o variable. Esto afecta
>   directamente a cuantos sprites, cuanto scroll y cuanta IA son viables.
> - Cualquier feature nueva que anada ciclos al loop principal debe
>   evaluarse contra el presupuesto de frame. Si no cabe, algo tiene que
>   salir.
> - Optimizar en ensamblador puro es casi obligatorio para las rutinas
>   criticas. Codigo en C o BASIC no es viable para el game loop.

---

## Resumen de restricciones y decisiones de produccion

| Restriccion               | Decision requerida            | Cuando decidir    |
|---------------------------|-------------------------------|-------------------|
| Modo 0 vs Modo 1          | Modo de video                 | Pre-produccion    |
| Sin sprites hardware      | Max sprites y tamano          | Pre-produccion    |
| VRAM entrelazada           | Tipo de scroll                | Prototipado       |
| Contencion Gate Array      | Target framerate              | Pre-produccion    |
| 3 canales AY               | Split musica/SFX              | Pre-produccion    |
| 178 KB por disco           | Estructura de multi-load      | Diseno de niveles |
| Bank switching 6128        | Modelos soportados            | Pre-produccion    |
| Throughput efectivo         | Alcance de features           | Continuo          |

Estas decisiones deben quedar documentadas en un **documento de restricciones
tecnicas** que firmen PM, lead tecnico y director de arte. Cualquier cambio
posterior debe pasar por un analisis de impacto formal.
