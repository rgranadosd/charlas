---
title: "Restricciones del ZX Spectrum y su impacto en produccion"
platform: "zx-spectrum"
category:
  - hardware
  - production
audience:
  - pm
  - programmer
  - technical-lead
keywords:
  - restricciones
  - color-clash
  - atributos
  - ula-contencion
  - beeper
  - 48k-vs-128k
  - sprites-software
  - scroll
  - tape-loading
  - multi-load
  - planificacion
  - pipeline-arte
version: "1.0"
---

# Restricciones del ZX Spectrum y su impacto en produccion

El ZX Spectrum es probablemente la maquina de 8 bits con las limitaciones
graficas mas severas, pero tambien la que genero las soluciones creativas
mas ingeniosas. Este documento analiza cada restriccion desde la optica de
un PM o technical lead que debe planificar un juego para Spectrum.

---

## 1. Color clash: LA restriccion central del Spectrum

### El sistema de atributos

La pantalla del Spectrum tiene una resolucion de 256 x 192 pixeles en
bitmap monocromo. El color se aplica mediante una capa de **atributos**
superpuesta al bitmap, donde cada celda de **8 x 8 pixeles** comparte
un unico atributo que define:

- **INK** (color de primer plano): 1 de 8 colores.
- **PAPER** (color de fondo): 1 de 8 colores.
- **BRIGHT**: 0 o 1 (version brillante del color).
- **FLASH**: 0 o 1 (parpadeo automatico INK/PAPER).

Esto significa que dentro de cada celda de 8x8, solo puede haber **2 colores**
(mas la variante BRIGHT). Cuando un sprite coloreado se mueve sobre un fondo
de color diferente, los atributos del fondo cambian al INK/PAPER del sprite,
creando un efecto visual conocido como **color clash** o "attribute clash".

### Por que es tan devastador

El color clash no es un defecto menor: es una distorsion visual que afecta
a la legibilidad del juego. Cuando un sprite rojo se mueve sobre un fondo
azul, las celdas de 8x8 que el sprite toca se "contaminan" con los colores
del sprite, creando un halo rectangular a su alrededor. Esto puede:

- Hacer que el fondo parezca corrupto.
- Dificultar distinguir al jugador de los enemigos.
- Ocultar proyectiles o power-ups sobre fondos complejos.

### Workarounds clasicos

| Tecnica                     | Descripcion                                       | Ejemplo conocido            |
|-----------------------------|---------------------------------------------------|-----------------------------|
| **Sprites monocromo**       | Sprites sin color propio; usan INK/PAPER del fondo| Knight Lore, Head Over Heels|
| **Fondo negro**             | PAPER negro en toda la zona de juego; el clash     | Jet Set Willy, Manic Miner |
|                             | existe pero es invisible (negro sobre negro)       |                             |
| **Sprites de 1 color**      | El sprite tiene un solo INK sobre fondo PAPER      | R-Type, Cobra              |
|                             | fijo; el clash se minimiza                         |                             |
| **Paleta cuidada**          | Elegir INK y PAPER para todo el nivel de modo que  | Batman (1986)              |
|                             | el clash sea poco perceptible                      |                             |
| **Scroll por atributos**    | Mover solo atributos y no el bitmap detallado      | Varios juegos Ultimate     |
| **Pre-shift sprites**       | Versiones del sprite desplazadas a nivel de pixel  | Multiples juegos           |
|                             | para alinear con celdas de atributos               |                             |
| **Resolucion reducida**     | Sprites de 16x16 o mayores para que el clash       | Juegos isometricos         |
|                             | afecte a menos celdas relativas al sprite          |                             |

### El enfoque artistico "Spectrum-native"

Los mejores juegos de Spectrum no intentan luchar contra el color clash, sino
que **disenan alrededor de el**. El estilo visual del Spectrum es
intrinsecamente monocromo con toques de color. Los juegos que intentan
replicar la estetica de CPC o C64 con colores abundantes suelen verse peor
que los que abrazan el monocromo con arte pixel detallado.

> **Que significa para el PM**
>
> - El color clash debe tratarse como la **restriccion numero uno** en el
>   briefing artistico. El artista debe conocer el sistema de atributos
>   antes de dibujar un solo pixel.
> - El PM debe validar en pre-produccion cual de los workarounds se usara
>   (sprites monocromo, fondo negro, paleta controlada, etc.) y alinearlo
>   con la direccion de arte.
> - Un artista sin experiencia en Spectrum necesitara formacion especifica.
>   Prever 1 semana de onboarding con la herramienta de arte (SevenuP,
>   ZX Paintbrush) y tests en emulador.
> - Los mockups en papel o en Photoshop **no representan** el resultado
>   real. Todo mockup debe validarse en emulador (o hardware real) con
>   sprites en movimiento para evaluar el clash.
> - Los juegos isometricos (donde los sprites son mas grandes y el fondo
>   tiende a ser uniforme) manejan mejor el clash que los plataformas o
>   shooters.

---

## 2. Contencion de la ULA: el peaje del acceso a VRAM

### El mecanismo

La ULA (Uncommitted Logic Array) del Spectrum genera la senal de video
leyendo la VRAM, que ocupa las direcciones &4000-&5AFF (bitmap) y
&5800-&5AFF (atributos), dentro de los primeros 16 KB de RAM (&4000-&7FFF
en los modelos 48K/128K).

Cuando la ULA lee la VRAM, **detiene al Z80** insertando estados de espera.
Esto ocurre durante el tiempo de pantalla activa (192 lineas de display).

### Numeros

- El Z80 funciona a 3.5 MHz nominales.
- Durante cada linea de pantalla, la ULA roba ciclos al Z80 en un patron
  regular: 6 ciclos de cada 8 estan disponibles para la CPU, pero **solo
  cuando se accede a la RAM contended** (los primeros 16 KB: &4000-&7FFF).
- El resultado es una **perdida de ~30 % de rendimiento** para cualquier
  codigo o dato que resida en esa zona.
- La RAM alta (&8000-&FFFF) **no sufre contencion**. Codigo ejecutado desde
  ahi corre a plena velocidad.

### Implicaciones de layout de memoria

El programador debe organizar la memoria para minimizar la contencion:

| Zona           | Direcciones     | Contencion | Uso recomendado         |
|----------------|----------------|------------|--------------------------|
| &4000-&5AFF    | Bitmap pantalla | **Si**     | Solo VRAM                |
| &5B00-&7FFF    | RAM baja libre  | **Si**     | Datos poco accedidos     |
| &8000-&BFFF    | RAM alta baja   | No         | Codigo principal, sprites|
| &C000-&FFFF    | RAM alta alta   | No         | Datos criticos, buffers  |

Codigo que se ejecuta frecuentemente (game loop, rutinas de sprites) **debe**
residir en la RAM alta (&8000+) para evitar la penalizacion de contencion.

> **Que significa para el PM**
>
> - El lead tecnico debe entregar un **mapa de memoria** al inicio del
>   proyecto que coloque codigo critico fuera de la zona &4000-&7FFF.
> - Si el equipo no conoce el tema de contencion, el juego puede ser un
>   30 % mas lento de lo esperado sin causa aparente. El PM debe preguntar
>   activamente: "donde esta el codigo en memoria?".
> - Los benchmarks deben hacerse con display activo y codigo en posicion
>   final de memoria, no en posiciones temporales.
> - Prever en el cronograma una tarea de "optimizacion de layout de
>   memoria" al final de alpha, cuando ya se sabe que rutinas son las
>   mas criticas.

---

## 3. Beeper de 1 bit (48K): sonido a base de CPU

### El problema fundamental

El Spectrum 48K no tiene chip de sonido dedicado. El "sonido" se genera
toggling un bit del puerto &FE que controla el altavoz (beeper). Para
producir un tono, la CPU debe:

1. Activar el bit de altavoz.
2. Esperar un numero preciso de ciclos (que determina la frecuencia).
3. Desactivar el bit.
4. Repetir.

Mientras la CPU esta generando sonido, **no puede hacer nada mas**. No hay
interrupciones, no hay DMA, no hay buffer: es la CPU al 100 % dedicada al
beeper.

### Consumo de CPU

| Tipo de audio            | CPU consumida | Notas                          |
|--------------------------|--------------|--------------------------------|
| Silencio                 | 0 %          |                                |
| Tono simple (un canal)   | ~90-100 %    | CPU totalmente bloqueada       |
| Motor multi-canal (beeper engines) | ~70-95 % | Octode, Phaser1, etc. |
| Efecto de sonido corto   | 100 % durante duracion | 0.1 - 0.5 segundos tipico |

Los "beeper engines" avanzados (como los de Tim Follin) pueden simular
multiples canales mediante alternancia rapida, pero la CPU sigue estando
mayoritariamente ocupada. Esto significa que **la musica beeper solo es
viable en pantallas de titulo o pausas**, no durante gameplay.

### Efecto en el gameplay

Durante el juego, los sonidos del beeper provocan **micro-pausas** visibles:
el juego se congela una fraccion de segundo mientras suena el efecto. Los
juegos clasicos del 48K minimizan esto usando:

- Efectos muy cortos (clicks, bleeps de < 50 ms).
- Sonido solo entre frames (durante el HALT).
- Prescindir de musica in-game completamente.

> **Que significa para el PM**
>
> - En el 48K, la musica in-game es **practicamente imposible** sin
>   congelar el juego. El GDD no debe prometer musica durante gameplay
>   si el target es 48K.
> - Los efectos de sonido deben ser **breves** (< 100 ms idealmente) para
>   minimizar el impacto visual de las micro-pausas.
> - El compositor/disenador de sonido debe entender que esta trabajando
>   con 1 bit, no con un chip de sonido real. La produccion de audio
>   para beeper es un arte muy especializado.
> - Si el juego requiere musica in-game, el target minimo debe ser el
>   **Spectrum 128K** (que incluye chip AY). Ver seccion 4.
> - En el presupuesto de tiempo del disenador de sonido, los efectos
>   beeper tardan mas en iterar que efectos AY porque cada prueba
>   requiere verificar que no causa stuttering visible.

---

## 4. 48K vs 128K: la decision de plataforma

### Diferencias clave

| Caracteristica        | 48K                     | 128K                          |
|-----------------------|------------------------|-------------------------------|
| RAM                   | 48 KB                  | 128 KB (8 paginas de 16 KB)   |
| Sonido                | Beeper 1-bit           | Beeper + **AY-3-8912**        |
| ROM                   | 16 KB                  | 32 KB (2 ROMs)                |
| Salida video          | RF/compuesto           | RF/compuesto + RGB            |
| Editor BASIC          | 48 BASIC               | 128 BASIC (mejorado)          |
| Paginacion            | No                     | Si (8 paginas x 16 KB)        |
| Disco                 | Externo (Microdrive)   | +3: integrado (3")            |

### El dilema del PM

La base instalada del Spectrum estuvo historicamente dominada por el 48K.
Lanzar solo para 128K excluia a una parte significativa del mercado. Las
opciones son:

1. **Solo 48K**: maximo mercado, minimas capacidades. Sin musica AY,
   sin RAM extra.

2. **Solo 128K**: acceso a AY y 128 KB. Musica in-game, mas niveles en
   memoria, doble buffer posible. Pero se pierde una parte del mercado.

3. **Hibrido (lo mas comun)**: el juego funciona en 48K con sonido beeper
   y carga desde cinta. En 128K detecta automaticamente el hardware extra
   y activa musica AY, carga datos extra en los bancos de memoria y
   ofrece features adicionales (mas niveles, mejor sonido, carga mas
   rapida).

### Complejidad del enfoque hibrido

El enfoque hibrido suena ideal pero multiplica el trabajo:

- Dos motores de sonido (beeper + AY).
- Dos sistemas de carga (con y sin bancos extra).
- Testing en dos configuraciones distintas.
- Posibles bugs que solo aparecen en una de las dos versiones.
- El compositor crea dos versiones de cada pieza musical.

### Paginacion en 128K

Los 128 KB se organizan en 8 paginas de 16 KB. La pagina activa se mapea
en &C000-&FFFF. Solo una pagina es visible a la vez. Dos paginas
contienen VRAM (paginas 5 y 7), lo que permite doble buffer.

> **Que significa para el PM**
>
> - La decision 48K/128K/hibrido debe tomarse en **pre-produccion** y es
>   irreversible sin coste significativo.
> - El enfoque hibrido anade aproximadamente un **30-40 % de trabajo extra**
>   en sonido y un 15-20 % en testing respecto a una version unica.
> - Si el mercado objetivo es moderno (scena retro actual), el 128K es
>   el estandar de facto. Si es un juego de epoca historica, el 48K es
>   obligatorio.
> - El PM debe mantener una **matriz de features** clara que muestre que
>   tiene cada version: "48K: 5 niveles, beeper SFX, carga cinta. 128K:
>   10 niveles, musica AY, carga instantanea desde bancos".
> - Pedir al lead tecnico un prototipo temprano que valide la deteccion
>   de hardware y la paginacion antes de construir contenido sobre ello.

---

## 5. Sin sprites ni scroll por hardware

Al igual que el CPC, el Spectrum **no tiene hardware de sprites ni de
scroll**. Todo se hace por software, con el Z80 copiando bytes a la VRAM.

### Coste de sprites software en Spectrum

El coste es similar al CPC pero con dos diferencias:

1. **La CPU es mas lenta** (3.5 MHz vs 4 MHz del CPC).
2. **El color clash anade complejidad**: ademas de dibujar el bitmap del
   sprite, hay que gestionar la capa de atributos, lo que anade
   instrucciones extra.

| Tamano sprite | Bytes bitmap | Bytes atributos | Ciclos dibujo (aprox.) | % de frame (50 Hz) |
|---------------|-------------|----------------|------------------------|---------------------|
| 8 x 8 px      | 8           | 1              | ~600                   | ~1 %                |
| 16 x 16 px    | 32          | 4              | ~2 800                 | ~4 %                |
| 24 x 24 px    | 72          | 9-12           | ~6 500                 | ~9 %                |
| 32 x 32 px    | 128         | 16-20          | ~12 000                | ~17 %               |

Un frame a 50 Hz dispone de ~69 888 ciclos brutos (modelo 48K), de los
cuales ~50 000-55 000 son utiles tras contencion.

### Scroll software

El scroll horizontal pixel a pixel requiere desplazar (shift) cada byte de
la pantalla, lo que es extremadamente lento en el Z80. Las alternativas:

- **Scroll por caracter** (8 pixeles): mucho mas rapido, pero brusco.
- **Scroll por atributos**: se mueven solo los 768 bytes de atributos, dando
  una ilusion de movimiento en la capa de color.
- **Scroll de zona parcial**: solo scrollea una franja de la pantalla,
  reduciendo el volumen de datos.
- **Flip-screen**: no hay scroll; la pantalla cambia completamente al
  llegar al borde. Elimina el problema por completo.

> **Que significa para el PM**
>
> - Como en CPC, el numero de sprites en pantalla es un limite duro que
>   debe definirse en el GDD.
> - El scroll suave full-screen a 50 fps es **practicamente imposible** en
>   Spectrum. El PM no debe comprometer scroll suave sin validacion
>   tecnica previa.
> - Los generos que mejor encajan en Spectrum son los que usan flip-screen
>   (plataformas, aventuras), scroll parcial (shooters con scroll en una
>   franja) o pantalla fija (puzzles, estrategia).
> - Si el diseno del juego requiere scroll, prever un prototipo tecnico de
>   2-3 semanas para validar rendimiento antes de producir contenido.

---

## 6. Carga desde cinta: disenar para multi-load

### Velocidades de carga

| Metodo                      | Velocidad         | Tiempo para 48 KB |
|-----------------------------|-------------------|-------------------|
| Carga estandar ROM          | ~1 500 bps        | ~4 minutos        |
| Turbo loader tipico         | ~3 000-4 500 bps  | ~1.5-2 minutos    |
| Turbo loader agresivo       | ~6 000+ bps       | ~1 minuto         |
| Disco +3                    | ~30 KB/s          | ~1.5 segundos     |

### Multi-load: cuando el juego no cabe en memoria

Con 48 KB de RAM (de los cuales ~41 KB son utilizables tras descontar VRAM,
variables del sistema y stack), un juego con muchos niveles necesita cargar
datos desde cinta durante el juego (**multi-load**).

El multi-load implica:

1. El jugador completa un nivel o zona.
2. La pantalla muestra "CARGANDO NIVEL 2 - PULSE PLAY EN EL CASSETTE".
3. El jugador debe encontrar la posicion correcta en la cinta, pulsar play
   y esperar 1-4 minutos.
4. Si la carga falla (algo comun con cintas baratas), repetir.

### Alternativas de diseno

| Estrategia             | Pro                              | Contra                        |
|------------------------|----------------------------------|-------------------------------|
| Single-load            | Sin interrupciones               | Juego limitado a 41 KB        |
| Multi-load secuencial  | Mas contenido                    | Esperas de 2-4 min entre cargas|
| Multi-load con rewind  | Maximo contenido                 | El jugador debe rebobinar      |
| Compresion agresiva     | Mas en RAM                       | Tiempo de descompresion       |

### Diseno amigable con multi-load

Los mejores juegos de Spectrum disenan sus niveles para que el multi-load
sea tolerable:

- **Pantalla de "bien hecho"** que celebra el logro mientras carga.
- **Guardado de progreso** via codigo de nivel (no se pierde progreso).
- **Niveles sustanciales**: si el jugador va a esperar 3 minutos cargando,
  el nivel debe ofrecer al menos 10-15 minutos de juego.
- **Cargas al inicio de "mundos"**, no de cada nivel individual.

> **Que significa para el PM**
>
> - La estructura de niveles del GDD debe diseñarse con el **tiempo de
>   carga en mente**. No tiene sentido un nivel de 30 segundos que
>   requiere 3 minutos de carga.
> - El PM debe definir la estructura de multi-load como parte del diseno
>   de producto: cuantas cargas, en que puntos, que datos se cargan en
>   cada bloque.
> - Cada "bloque de carga" debe tener un tamano planificado en el
>   presupuesto de espacio (similar al presupuesto de disco del CPC).
> - Un turbo loader reduce los tiempos a la mitad pero anade complejidad
>   tecnica y riesgo de incompatibilidad con algunos modelos de cassette.
>   Decision a consensuar con el lead tecnico.
> - Para versiones en disco (+3 o +D), el multi-load es practicamente
>   instantaneo, pero el PM debe considerar que el publico en disco era
>   minoritario en la era Spectrum.
> - El testing de multi-load en cinta real es **critico** y lento. Prever
>   dias de QA especificos para esto (no emulador: cinta fisica).

---

## 7. Layout de pantalla: tercios entrelazados

### Estructura de la VRAM

La pantalla del Spectrum se divide en **3 tercios** de 64 lineas cada uno.
Dentro de cada tercio, las lineas estan entrelazadas en un patron similar
al del CPC:

```
Tercio 0 (lineas 0-63):
  Linea 0   -> &4000
  Linea 1   -> &4100
  Linea 2   -> &4200
  ...
  Linea 7   -> &4700
  Linea 8   -> &4020
  Linea 9   -> &4120
  ...

Tercio 1 (lineas 64-127):
  Linea 64  -> &4800
  ...

Tercio 2 (lineas 128-191):
  Linea 128 -> &5000
  ...
```

Dentro de cada tercio, las lineas se agrupan en bloques de 8, con las lineas
de cada bloque separadas por 256 bytes (&100). Los bloques dentro del tercio
estan separados por 32 bytes (&20).

### Impacto practico

- Las rutinas de dibujo necesitan **tablas de lookup** (192 entradas = 384
  bytes) o calculos complejos para convertir coordenadas (x, y) a
  direcciones de VRAM.
- El scroll vertical entre tercios es especialmente problematico: cruzar la
  frontera del tercio (linea 63 a 64, o linea 127 a 128) requiere un salto
  de &800 en lugar del patron habitual.
- La capa de atributos, en cambio, es **lineal**: 32 columnas x 24 filas =
  768 bytes en &5800-&5AFF. Esto simplifica las operaciones de color.

> **Que significa para el PM**
>
> - Como en el CPC, la VRAM no lineal anade complejidad a la programacion
>   de graficos. Factor similar: x1.5 de dificultad.
> - Las tablas de lookup ocupan ~384 bytes de RAM, que deben presupuestarse.
> - El programador necesita experiencia con el layout o tiempo para
>   aprenderlo. Si el equipo es nuevo en Spectrum, prever aprendizaje.
> - Las herramientas de arte para Spectrum (SevenuP, ZX Paintbrush) ya
>   gestionan este layout internamente; el artista no necesita preocuparse,
>   pero el programador si.
> - El dibujo de sprites que cruzan fronteras de tercio es mas lento por
>   la logica de cambio de base. Considerar si los sprites pueden evitar
>   esas zonas o si la rutina maneja el caso especial.

---

## 8. El borde: elemento de diseno con restricciones

### Que es el borde

El Spectrum muestra un **borde** alrededor de la pantalla principal de
256x192. Este borde ocupa una franja significativa de la pantalla visible
(especialmente en televisores de la epoca).

### Limitaciones del borde

- Solo puede tener **un unico color** en todo el borde a la vez.
- Se controla escribiendo en el puerto &FE (los 3 bits bajos).
- Cambiar el color del borde es instantaneo pero afecta a todo el borde.
- Usando cambios de color sincronizados con el raster, se pueden crear
  **franjas horizontales** de color en el borde (efecto "raster bars"),
  pero esto consume CPU.

### Usos del borde en diseno

| Uso                          | Descripcion                                  |
|------------------------------|----------------------------------------------|
| Indicador de estado          | Rojo = peligro, verde = seguro               |
| Feedback de dano             | Flash rojo al recibir golpe                  |
| Atmosfera                    | Color del borde acorde al nivel               |
| Carga visual                 | Franjas de colores durante carga de cinta     |
| Extension de pantalla        | Raster bars para simular pantalla mas grande  |
| Indicador de audio           | Cambio de color durante efectos de sonido     |

El efecto del borde durante la carga de cinta es **iconico** del Spectrum:
las franjas rojas, azules y amarillas que aparecen mientras se carga un
programa son en realidad el reflejo visual de los datos de audio de la cinta.

> **Que significa para el PM**
>
> - El borde es un recurso de diseno **gratuito** (sin coste de RAM o CPU
>   significativo para colores estaticos).
> - Usarlo para feedback de estado es una buena practica que no compite con
>   el presupuesto de sprites.
> - Los efectos de borde avanzados (raster bars) consumen CPU y requieren
>   sincronizacion de raster, lo que los hace costosos. Solo justificables
>   en pantallas de titulo o demos.
> - El disenador de UX debe incluir el borde en sus mockups, no ignorarlo.
>   Un borde negro en un juego colorido se siente "inacabado". Un borde
>   que cambia de color con el contexto anade polish sin coste tecnico.
> - En la documentacion de arte, especificar el color de borde por nivel
>   o estado del juego.

---

## Resumen de restricciones y decisiones de produccion

| Restriccion               | Decision requerida               | Cuando decidir    |
|---------------------------|----------------------------------|-------------------|
| Color clash (atributos)   | Estrategia de color (monocromo, fondo negro, paleta controlada) | Pre-produccion |
| Contencion ULA            | Layout de memoria                | Diseno tecnico    |
| Beeper 1-bit (48K)        | SFX minimos o target 128K       | Pre-produccion    |
| 48K vs 128K               | Modelo(s) soportado(s)           | Pre-produccion    |
| Sin sprites/scroll HW     | Max sprites, tipo de scroll      | Pre-produccion    |
| Carga desde cinta         | Estructura de multi-load         | Diseno de niveles |
| VRAM en tercios            | Tipo de scroll, herramientas     | Prototipado       |
| Color del borde            | Uso de diseno del borde          | Diseno visual     |

### Decision critica: Spectrum vs otras plataformas

Si el juego es multiplatforma (Spectrum + CPC + C64), el Spectrum suele ser
la version mas restrictiva por el color clash. Hay dos filosofias:

1. **Desarrollar primero para Spectrum** y portar "hacia arriba" anadiendo
   color en CPC/C64. Garantiza que el juego funciona en la maquina mas
   limitada.

2. **Desarrollar en la maquina "lead"** (normalmente CPC o C64) y adaptar
   a Spectrum recortando color. Riesgo: la version Spectrum puede parecer
   un port de segunda.

El PM debe tomar esta decision estrategica en funcion de cual es el mercado
principal y documentarla como politica del proyecto.

---

## Apendice: Checklist para el PM de un proyecto Spectrum

- [ ] Decidido el modelo target (48K / 128K / hibrido).
- [ ] Estrategia de color clash definida y validada con mockup en emulador.
- [ ] Mapa de memoria entregado por el lead tecnico (codigo en &8000+).
- [ ] Politica de sonido definida (beeper vs AY, split de canales en 128K).
- [ ] Estructura de multi-load documentada (bloques, tamanos, puntos de carga).
- [ ] Presupuesto de sprites por pantalla (numero y tamano maximo).
- [ ] Tipo de scroll decidido (flip-screen, caracter, parcial, ninguno).
- [ ] Color de borde por nivel/estado definido en la guia de arte.
- [ ] Turbo loader seleccionado (o carga estandar ROM).
- [ ] Matriz de compatibilidad: modelos Spectrum a testear (48K, 128K,
      +2, +2A, +3).
