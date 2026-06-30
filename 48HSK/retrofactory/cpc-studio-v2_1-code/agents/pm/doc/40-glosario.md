---
title: "Glosario canónico 8-bit"
platform: ["amstrad-cpc", "zx-spectrum", "commodore-64", "msx"]
category: ["glossary", "reference"]
audience: ["pm", "programmer", "artist", "musician", "technical-lead"]
keywords: ["glosario", "definiciones", "terminología", "hardware", "producción", "sprites", "tiles", "scroll"]
version: "1.0"
---

# Glosario canónico — Desarrollo 8-bit

Definiciones de términos técnicos y de producción usados en el corpus. Organizados por categoría para facilitar la búsqueda semántica en RAG.

---

## Hardware y CPU

| Término | Definición |
|---------|-----------|
| **Z80** | CPU de 8 bits (Zilog) usada en CPC, Spectrum y MSX. 3,5-4 MHz según plataforma. Arquitectura CISC con registros de 8 y 16 bits, modos de direccionamiento ricos. |
| **6510** | CPU de 8 bits (MOS Technology) del C64. Compatible con 6502, corre a ~1 MHz. Menos registros que el Z80 pero instrucciones más rápidas por ciclo. |
| **Ciclo de reloj (clock cycle)** | Unidad mínima de tiempo del procesador. 1 MHz = 1 millón de ciclos/segundo. Cada instrucción consume entre 2 y 23 ciclos según complejidad. |
| **Frame** | Una imagen completa de pantalla. En PAL (50 Hz), un frame dura 20 ms. Todo el código del juego (lógica + gráficos + audio) debe ejecutarse dentro de ese tiempo para mantener fluidez. |
| **Framerate** | Velocidad de actualización del juego. 50 fps (cada frame) es ideal; 25 fps (cada 2 frames) es aceptable; <25 fps se percibe como lento. |
| **Budget de ciclos** | Presupuesto de ciclos de CPU disponibles por frame para todas las tareas del juego. El PM lo usa para decidir si una feature cabe. |
| **Badline** | (C64) Línea de escaneo donde el VIC-II roba 40 ciclos a la CPU para leer datos de carácter. Ocurre cada 8 líneas. Reduce los ciclos disponibles. |
| **Contención de memoria** | (Spectrum) La ULA roba ciclos de CPU al acceder a los primeros 16 KB de RAM (donde está la VRAM). Ralentiza ~30% el código que dibuja en pantalla. |
| **IRQ (Interrupt Request)** | Señal que interrumpe la CPU para ejecutar código urgente. En juegos se usa para sincronizar efectos con posiciones específicas de la pantalla. |
| **NMI (Non-Maskable Interrupt)** | Interrupción que no se puede desactivar. Usada para funciones críticas (reset, breakpoints de debug). |
| **Zero page** | (6502/6510) Los primeros 256 bytes de RAM (0x0000–0x00FF). Acceso más rápido que el resto de RAM. Los programadores de C64 la usan para variables frecuentes. |
| **Slot** | (MSX) Unidad de mapeado de memoria. El espacio de direcciones del Z80 se divide en 4 páginas de 16 KB, cada una asignable a un slot/sub-slot diferente. |
| **Bank switching** | Técnica para acceder a más memoria de la que el CPU puede direccionar directamente. Se "cambia" un bloque de memoria visible por otro. Usado en MegaROM (MSX), bancos de RAM (CPC 6128, Spectrum 128K). |
| **Memory mapper** | Dispositivo o registro que controla qué bloque de RAM o ROM está mapeado en cada zona del espacio de direcciones. |

---

## Vídeo y gráficos

| Término | Definición |
|---------|-----------|
| **VDP (Video Display Processor)** | Chip de vídeo separado de la CPU. En MSX: TMS9918A (MSX1) y V9938 (MSX2). Genera la imagen de vídeo independientemente de la CPU. |
| **VIC-II** | Chip de vídeo del C64 (MOS 6569 PAL / 6567 NTSC). Genera sprites, scroll y modos gráficos. El más capaz de las 4 plataformas. |
| **ULA** | (Spectrum) Uncommitted Logic Array. Genera la señal de vídeo a partir de la VRAM. No tiene capacidad de sprites ni scroll. |
| **Gate Array** | (CPC) Chip custom de Amstrad que gestiona vídeo, RAM y periféricos. Define los modos gráficos pero no tiene sprites ni scroll. |
| **VRAM** | Memoria de vídeo. Contiene los datos que el chip de vídeo lee para generar la imagen. En CPC/Spectrum es parte de la RAM principal; en C64 es la RAM principal vista por el VIC-II; en MSX es memoria separada. |
| **Scanline** | Una línea horizontal de la imagen de vídeo. La pantalla se dibuja de arriba a abajo, una scanline a la vez. Cada scanline tarda ~64 µs (PAL). |
| **Raster** | La posición actual del haz de electrones que dibuja la pantalla (en un CRT). "Raster IRQ" = interrupción sincronizada con una scanline específica. |
| **Sprite (hardware)** | Objeto gráfico independiente del fondo, movido por el chip de vídeo sin intervención de la CPU para dibujarlo. El VIC-II (C64) y TMS9918A (MSX) tienen sprites HW; CPC y Spectrum no. |
| **Sprite (software)** | Gráfico dibujado por la CPU directamente en la VRAM. Requiere borrar la posición anterior y redibujar en la nueva cada frame. Más lento que sprites HW. |
| **Tile** | Bloque gráfico reutilizable (típicamente 8×8 pixeles). Los fondos se construyen como una cuadrícula de tiles, ahorrando memoria (se almacena 1 copia del tile + un mapa de cuál va dónde). |
| **Tilemap** | Tabla que indica qué tile va en cada posición de la cuadrícula de pantalla. Mucho más compacto que almacenar cada pixel individualmente. |
| **Charset / Character set** | Conjunto de tiles que define los "caracteres" gráficos disponibles. En modo carácter (C64, MSX), la pantalla es un mapa de caracteres del charset. |
| **Color clash / attribute clash** | Artefacto visual que ocurre cuando dos objetos de diferente color se solapan dentro de una celda de atributos (8×8 en Spectrum, 4×8 en C64 multicolor, 8×1 en MSX). Solo un juego de colores puede existir por celda. |
| **Atributos** | (Spectrum/MSX) Bytes que definen los colores de cada celda de la pantalla, separados del bitmap. Cada atributo especifica ink+paper (Spectrum) o foreground+background (MSX). |
| **Multicolor** | (C64) Modo gráfico donde cada pixel tiene el doble de ancho (resolución 160×200) pero puede elegir entre 4 colores por celda, en vez de 2. |
| **Scroll fino (fine scroll)** | Desplazamiento suave de la pantalla en incrementos de 1 pixel. Requiere hardware dedicado (VIC-II, V9938) o mucho trabajo de CPU. |
| **Scroll grueso (coarse scroll)** | Desplazamiento de la pantalla en incrementos de 1 tile (8 pixeles). Más fácil de implementar que el fino. |
| **Flip-screen** | Diseño de juego donde la pantalla cambia completamente al llegar al borde. No hay scroll; cada pantalla es una escena independiente. Común en plataformas sin scroll HW. |
| **Double buffer** | Técnica que usa dos zonas de VRAM: mientras una se muestra, la otra se dibuja. Al terminar, se intercambian. Evita tearing y flickering. |
| **Flickering** | Parpadeo visual causado cuando un sprite no se puede dibujar en un frame (por límite de sprites/scanline en MSX) o cuando se borra/redibuja un sprite software demasiado lento. |
| **Multiplexado de sprites** | (C64) Técnica que reprograma los registros del VIC-II durante el dibujado de pantalla para reutilizar sprites HW en zonas inferiores. Permite >8 sprites visibles. |
| **Overlay de sprites** | Superponer 2+ sprites en la misma posición para obtener más colores. En MSX: 2 sprites monocolor = 1 bicolor. En C64: overlay para sprites más grandes. |
| **Border** | Zona del borde de pantalla (fuera del área de juego). En C64, se puede "abrir" el border con trucos de raster para dibujar en él. |
| **Split-screen** | Dividir la pantalla en dos zonas con configuraciones diferentes (ej: zona de scroll + panel de estado fijo). Se logra con raster IRQ. |
| **Paleta** | Conjunto de colores disponibles. CPC: 27 colores, 16 simultáneos. C64: 16 fijos. Spectrum: 15 (8×2 brillo). MSX1: 15 fijos. MSX2: 512, 16 simultáneos en Screen 5. |

---

## Audio

| Término | Definición |
|---------|-----------|
| **AY-3-8910 / AY-3-8912** | Chip de sonido (General Instrument) de 3 canales de onda cuadrada + generador de ruido. Usado en CPC, Spectrum 128K y MSX. El 8910 y 8912 son funcionalmente idénticos (diferencia en pines I/O). |
| **SID (6581/8580)** | Chip de sonido del C64. 3 osciladores con 4 formas de onda, filtro analógico resonante y ADSR por canal. Considerado el mejor sonido 8-bit. |
| **Canal** | Una "voz" independiente del chip de sonido. El AY tiene 3; el SID tiene 3. La música y los SFX compiten por los canales disponibles. |
| **Onda cuadrada** | Forma de onda básica del AY: solo dos niveles (on/off). Sonido "chiptune" reconocible. |
| **ADSR** | Envolvente de sonido: Attack (subida), Decay (bajada inicial), Sustain (nivel sostenido), Release (apagado). Define cómo evoluciona el volumen de una nota en el tiempo. |
| **Tracker** | Software para componer música chip-tune. Muestra las notas en columnas verticales (canales) con notación propia. Ejemplos: Arkos Tracker, GoatTracker. |
| **Beeper** | (Spectrum 48K) Altavoz de 1 bit sin chip de sonido. El software genera sonido toggling el bit rápidamente. Consume 100% CPU mientras suena. |
| **PSG (Programmable Sound Generator)** | Nombre genérico para chips de sonido como el AY. "PSG" y "AY" se usan indistintamente en contexto MSX. |
| **SFX (Sound Effects)** | Efectos de sonido del juego (disparos, saltos, explosiones). Compiten con la música por los canales disponibles. |
| **Driver de música** | Código que reproduce datos musicales (notas, efectos) en el chip de sonido. Se ejecuta 1 vez por frame (~50 veces/segundo). Consume ciclos de CPU. |
| **Filtro** | (SID) Circuito analógico que modifica el timbre del sonido. Paso bajo, paso alto, paso banda. La "magia" del sonido C64. |
| **Ring modulation** | (SID) Técnica que multiplica dos osciladores entre sí, creando timbres metálicos/inarmónicos. |
| **MSX-MUSIC (YM2413)** | Chip FM de 9 canales (OPLL). Expansión de audio en MSX2+ y turboR. Síntesis FM vs. onda cuadrada del AY. |
| **SCC** | (MSX) Sound Creative Chip de Konami. 5 canales de onda programable (32 muestras por onda). Incluido en ciertos cartuchos MegaROM Konami. Superior al AY. |

---

## Almacenamiento

| Término | Definición |
|---------|-----------|
| **Cinta (tape/cassette)** | Medio de almacenamiento magnético. Lento (1200-2400 baud) pero barato. Requiere pantallas de carga para disimular la espera. |
| **Turbo loader** | Cargador personalizado que transfiere datos de cinta más rápido que el estándar del sistema (2-4× más rápido). |
| **Disco (floppy disk)** | Medio magnético con acceso aleatorio. Más rápido que cinta. CPC usa 3" (178 KB/cara), Spectrum +3 usa 3" (180 KB/cara), C64 usa 5¼" (170 KB/cara), MSX usa 3,5" (360-720 KB). |
| **Fastloader** | (C64) Software que acelera la transferencia desde la unidad de disco 1541. Imprescindible para experiencia de juego aceptable (400 B/s → 3-8 KB/s). |
| **Cartucho (cartridge)** | Medio ROM de carga instantánea. Se inserta en el slot de expansión. Capacidad desde 8 KB hasta 512+ KB (MegaROM). |
| **MegaROM** | (MSX) Cartucho con bank switching que permite más de 32 KB de ROM. Mappers: Konami, Konami SCC, ASCII 8K, ASCII 16K. Hasta 512 KB o más. |
| **ROM** | Read-Only Memory. Memoria que no se puede modificar en ejecución. Contiene el sistema operativo y/o el juego (en cartucho). |
| **RAM** | Random Access Memory. Memoria lectura/escritura donde reside el código del juego (si se carga desde cinta/disco) y los datos variables. |
| **Imagen de disco (.dsk/.d64)** | Archivo que contiene una copia sector-a-sector de un disco. Formato estándar para distribución digital en emuladores. |

---

## Producción y gestión

| Término | Definición |
|---------|-----------|
| **Scope** | Alcance del proyecto: cuántos niveles, enemigos, features, etc. se van a implementar. Definirlo es la tarea más importante del PM. |
| **Scope creep** | Crecimiento no controlado del alcance durante el desarrollo. Enemigo nº1 de los proyectos 8-bit (donde cada KB y cada ciclo cuentan). |
| **Mapa de memoria** | Documento que muestra cómo se distribuye la RAM disponible entre los diferentes sistemas del juego (código, datos, gráficos, audio, buffers). |
| **Feature** | Funcionalidad o característica del juego (scroll, system de vidas, boss, cutscene). Cada feature tiene un coste en ciclos, memoria y tiempo de desarrollo. |
| **Prototipo técnico** | Build temprana que valida que las features técnicas clave funcionan con rendimiento aceptable antes de producir contenido. |
| **Build** | Versión compilada y ejecutable del juego en un momento dado. Se genera frecuentemente para testeo. |
| **Milestone** | Punto de control del proyecto con entregables definidos. Ejemplo: "Alfa = feature complete". |
| **Pipeline** | Flujo de trabajo que transforma assets originales en datos finales integrados en el juego. Ej: "PSD → pixel art → exportar binario → integrar en build". |
| **Post-mortem** | Análisis retrospectivo al terminar un proyecto: qué funcionó, qué falló, lecciones para el futuro. |
| **Jam (game jam)** | Competición de desarrollo de juegos con límite de tiempo (48h, 1 semana, etc.). Las jams retro (CPCRetroDev, MSXdev) son anuales con meses de plazo. |
| **Homebrew** | Juego creado por aficionados/independientes para hardware retro, fuera del circuito comercial original. La escena homebrew 8-bit está muy activa en 2024-2026. |
| **Demoscene** | Comunidad que crea demostraciones audiovisuales (demos) para hardware retro, empujando los límites técnicos. Fuente de técnicas de programación avanzadas. |
| **Emulador** | Software que reproduce el comportamiento del hardware original en un PC moderno. Herramienta principal de desarrollo y testing. |
| **Cross-assembler / Cross-compiler** | Ensamblador o compilador que corre en PC moderno pero genera código para la plataforma retro target. Ej: Pasmo (Z80), KickAssembler (6510). |

---

## Técnicas de programación

| Término | Definición |
|---------|-----------|
| **ASM (Assembly / Ensamblador)** | Lenguaje de programación de bajo nivel, una instrucción por operación del CPU. Obligatorio para rendimiento óptimo en 8-bit. |
| **Tabla precalculada (lookup table / LUT)** | Array de valores calculados en tiempo de compilación para evitar cálculos en tiempo real. Ej: tabla de senos, tabla de direcciones de línea de VRAM. Cambia CPU por RAM. |
| **Unrolled loop (bucle desenrollado)** | Repetir el cuerpo del bucle N veces en código (en vez de iterar) para eliminar el overhead de la instrucción de salto. Consume más espacio de código pero es más rápido. |
| **Self-modifying code** | Código que se modifica a sí mismo en ejecución (cambia instrucciones o datos inline). Técnica avanzada para ganar velocidad. Dificulta el debug. |
| **Rastertime** | Medición de cuántos ciclos/scanlines consume una rutina. Se visualiza cambiando el color del borde durante la ejecución: cuanto más borde coloreado, más tiempo consume. |
| **Double buffer** | Usar dos buffers de pantalla y alternar entre ellos: uno se muestra mientras el otro se actualiza. Evita que el jugador vea gráficos a medio dibujar. |
| **Interleaving** | Organización no secuencial de datos en memoria (ej: líneas de VRAM en CPC entrelazadas cada 2048 bytes). Requiere tablas de direcciones para navegar. |
| **Compresión** | Reducir el tamaño de datos (gráficos, mapas, música) para que quepan en menos memoria o medio. Se descomprimen en RAM en tiempo de carga. Tipos comunes: RLE, LZ77/LZSS, Huffman. |
| **RLE (Run-Length Encoding)** | Compresión simple: en vez de "AAAABBCC" almacena "4A2B2C". Efectiva para gráficos con áreas de color sólido. |
| **Streaming** | Cargar datos bajo demanda durante el juego (desde disco) en vez de todo al inicio. Permite juegos más grandes que la RAM disponible. |

---

## Acrónimos frecuentes

| Acrónimo | Significado |
|----------|-----------|
| ASM | Assembly (lenguaje ensamblador) |
| CPU | Central Processing Unit |
| RAM | Random Access Memory |
| ROM | Read-Only Memory |
| VRAM | Video RAM |
| VDP | Video Display Processor |
| PSG | Programmable Sound Generator |
| SID | Sound Interface Device |
| IRQ | Interrupt Request |
| NMI | Non-Maskable Interrupt |
| DMA | Direct Memory Access |
| ADSR | Attack-Decay-Sustain-Release |
| SFX | Sound Effects |
| HW | Hardware |
| SW | Software |
| KB | Kilobyte (1024 bytes) |
| PAL | Phase Alternating Line (sistema TV europeo, 50 Hz) |
| NTSC | National Television System Committee (sistema TV americano/japonés, 60 Hz) |
| CRT | Cathode Ray Tube (tubo de imagen, las TVs originales) |
| PM | Project Manager / Product Manager |
| LUT | Look-Up Table |
| RLE | Run-Length Encoding |
| FPS | Frames Per Second |
