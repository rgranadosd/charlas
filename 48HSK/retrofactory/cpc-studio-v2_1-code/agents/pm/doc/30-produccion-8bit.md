---
title: "Guía de producción cross-platform 8-bit"
platform: ["amstrad-cpc", "zx-spectrum", "commodore-64", "msx"]
category: ["production", "management", "estimation", "tools", "distribution"]
audience: ["pm", "technical-lead"]
keywords: ["producción", "equipo", "estimación", "riesgos", "pipeline", "herramientas", "distribución", "testing", "planificación", "milestone"]
version: "1.0"
---

# Guía de producción cross-platform 8-bit

## Resumen

Este documento cubre los aspectos de producción comunes a las 4 plataformas (CPC, Spectrum, C64, MSX): cómo estructurar un equipo, estimar tiempos, gestionar riesgos, montar el pipeline de herramientas, distribuir y testear. Es el documento que un PM lee primero para entender el contexto global antes de sumergirse en las fichas por plataforma.

---

## 1. Estructura de equipo típica

### Juego pequeño (1 persona, hobby/jam)

| Rol | Persona | Dedicación |
|-----|---------|-----------|
| Programador + artista + compositor | 1 | Parcial (noches/fines de semana) |

**Timeline**: 2-6 meses. La mayoría de juegos homebrew actuales se hacen así.

### Juego medio (2-3 personas)

| Rol | Persona | Dedicación |
|-----|---------|-----------|
| Programador principal | 1 | Alta |
| Artista gráfico | 1 | Media (puede ser parcial) |
| Compositor musical | 1 | Baja (entrega puntual) |

**Timeline**: 4-10 meses. Es el modelo más eficiente para un juego con ambición comercial (venta en eventos, Itch.io, distribución física).

### Juego ambicioso (equipo completo)

| Rol | Persona | Dedicación |
|-----|---------|-----------|
| Programador motor | 1 | Alta |
| Programador gameplay/tools | 1 | Alta |
| Artista de tiles/fondos | 1 | Media-alta |
| Artista de sprites/animación | 1 | Media |
| Compositor/sound designer | 1 | Baja-media |
| PM/Game designer | 1 | Media |

**Timeline**: 8-18 meses. Raro en homebrew; más habitual en equipos organizados (CPCRetroDev finalistas, etc.).

---

## 2. Fases de producción

### Fase 0 — Concepto (1-2 semanas)

| Entregable | Descripción |
|-----------|-------------|
| Documento de concepto | 1-2 páginas: género, plataforma target, mecánicas core, referencia visual |
| Análisis de viabilidad técnica | ¿La plataforma soporta lo que queremos? Budget de sprites, scroll, audio |
| Decisión de modo gráfico | CPC: Mode 0 vs 1. C64: Multicolor vs hi-res. MSX: Screen 1 vs 2. Spectrum: monocromo vs color |

### Fase 1 — Prototipo técnico (2-4 semanas)

| Entregable | Descripción |
|-----------|-------------|
| Motor mínimo funcionando | Sprites moviéndose, 1 fondo, controles |
| Prueba de rendimiento | ¿Quedan ciclos para lógica de juego? |
| Mapa de memoria | Distribución de los KB disponibles |
| Pipeline de arte validado | El artista puede exportar y ver su trabajo en emulador |

**Criterio de "go/no-go"**: si el prototipo no alcanza el framerate deseado, reducir alcance AHORA. No esperar a alfa.

### Fase 2 — Producción (60-70% del timeline)

| Actividad | Progreso típico |
|-----------|----------------|
| Programación de sistemas | Motor, scroll, colisiones, menús |
| Producción de arte | Tiles, sprites, pantallas, animaciones |
| Producción de audio | Música de niveles, SFX |
| Diseño de niveles | Mapas, encuentros, dificultad |
| Integración continua | Builds semanales testeables |

### Fase 3 — Alfa (2-4 semanas)

| Criterio | Descripción |
|---------|-------------|
| Feature complete | Todas las mecánicas implementadas |
| Contenido 80%+ | La mayoría de niveles/arte están |
| Música completa | Todos los temas compuestos |
| Bugs conocidos | Lista priorizada de bugs |

### Fase 4 — Beta y pulido (2-4 semanas)

| Actividad | Foco |
|-----------|------|
| Bugfixing | Estabilidad, crashes, glitches |
| Balanceo | Dificultad, fairness, curva |
| Optimización final | Exprimir ciclos, reducir flickering |
| Testing en hardware real | Si aplica |
| Pantalla de carga, créditos | Polish final |

### Fase 5 — Release (1-2 semanas)

| Tarea | Descripción |
|-------|-------------|
| Build final master | Imagen de cinta/disco/cartucho definitiva |
| Testing de distribución | El archivo funciona en emuladores estándar |
| Packaging (si físico) | Carátula, manual, medio físico |
| Upload/distribución | Itch.io, pouet.net, foro de plataforma |
| Post-mortem | Qué funcionó, qué no, lecciones |

---

## 3. Estimación de tiempos

### Factores multiplicadores

| Factor | Multiplicador |
|--------|-------------|
| Programador sin experiencia en la plataforma | ×1,5–2,0 |
| Primera vez trabajando en equipo (coordinación) | ×1,2–1,3 |
| Scroll suave (vs flip-screen) | ×1,3–1,5 |
| Multiplataforma (2+ plataformas) | ×1,5–1,8 (no ×2; comparten diseño) |
| Juego con editor de niveles interno | ×1,2–1,3 |
| Distribución en hardware físico real | ×1,1–1,2 (testing + packaging) |

### Tabla de referencia rápida

| Tipo de juego | 1 persona (noches) | 1 persona (full-time) | Equipo 2-3 |
|--------------|--------------------|-----------------------|------------|
| Puzzle 1 pantalla | 1-2 meses | 2-4 semanas | 1-2 semanas |
| Plataformas flip-screen | 3-5 meses | 2-3 meses | 1-2 meses |
| Plataformas con scroll | 5-8 meses | 3-5 meses | 2-3 meses |
| Shoot'em up vertical | 4-7 meses | 3-4 meses | 2-3 meses |
| RPG/aventura | 8-14 meses | 5-8 meses | 4-6 meses |
| Demake/port de arcade | 4-6 meses | 2-4 meses | 2-3 meses |

### Anti-patrones de estimación

- **"Ya casi funciona, solo falta pulir"** — El último 10% de features consume el 30% del tiempo.
- **"El scroll se puede añadir después"** — El scroll afecta a toda la arquitectura. Es una decisión de día 1.
- **"La música se mete al final"** — Si el driver de audio consume 15% de CPU, hay que saberlo desde el prototipo.
- **"Solo son X niveles más"** — El contenido tiene coste fijo por unidad (arte + diseño + testing). N niveles ≈ N × coste.

---

## 4. Riesgos comunes y mitigación

### Riesgos técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Framerate insuficiente | Alta (si no se valida en prototipo) | Crítico | Prototipo técnico obligatorio antes de producción |
| RAM insuficiente para contenido | Media | Alto | Mapa de memoria en Fase 1, validar con contenido real |
| Bug de timing/raster (C64) | Media | Medio | +50% tiempo debug para features de raster |
| Color clash peor de lo esperado (Spectrum) | Media | Medio | Validar look visual con arte real en Fase 1 |
| Slots mal gestionados (MSX) | Alta (sin experiencia) | Alto | Programador con experiencia MSX, o +2 semanas |
| Scroll demasiado lento (MSX1/Spectrum) | Alta | Alto | Diseñar flip-screen como fallback |

### Riesgos de producción

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Abandono del proyecto (hobby) | Muy alta (>50%) | Total | Scope mínimo viable, releases incrementales |
| Artista/compositor desaparece | Media | Alto | Assets base propios, plan B con assets genéricos |
| Scope creep | Alta | Alto | Documento de alcance firmado, lista de "nice-to-have" separada |
| Contenido no cabe en medio de distribución | Media | Medio | Budget de KB desde Fase 0, tracking semanal |
| Hardware real se comporta diferente al emulador | Baja-media | Medio | Testing en HW real en Fase 3, no solo en release |

---

## 5. Pipeline de herramientas por plataforma

### Cross-platform (Z80: CPC, Spectrum, MSX)

| Función | Herramienta recomendada | Alternativas |
|---------|------------------------|-------------|
| Ensamblador | **Pasmo** | SJASM, RASM (CPC), Glass (MSX) |
| Compilador C | **z88dk** / **SDCC** | — |
| Tracker musical (AY) | **Arkos Tracker 2** | Vortex Tracker, WYZTracker |
| Editor de tiles genérico | **Tiled** (con exportador custom) | — |
| Control de versión | **Git** | — |
| Build system | **Make** / scripts | — |

### Amstrad CPC

| Función | Herramienta |
|---------|------------|
| Ensamblador específico | RASM (rápido, macros potentes) |
| Editor gráfico | RGAS, PixelPaint, ConvImgCPC |
| Emulador + debug | WinAPE (debug), Caprice32, Arnold |
| Generador de disco | iDSK, CPCDiskXP |
| Framework | CPCtelera (C + ASM mixto) |

### ZX Spectrum

| Función | Herramienta |
|---------|------------|
| Editor de sprites | SevenuP, Colorator |
| Emulador + debug | FUSE (con debugger), ZX Spin |
| Framework | z88dk, SP1 (sprite library) |
| Conversión de imagen | ZX-Paintbrush, Image2ZX |
| Generador de cinta/disco | Pasmo (output TAP), hdfmonkey (+3 disco) |

### Commodore 64

| Función | Herramienta |
|---------|------------|
| Ensamblador | **KickAssembler** (Java, macros, scripting) |
| Compilador C | cc65 |
| Editor sprites/chars | SpritePad, CharPad |
| Tracker musical | **GoatTracker** |
| Emulador + debug | **VICE** (el más completo) |
| Editor de mapa de memoria | C64 Debugger (visual) |
| Generador de disco/cartucho | c1541, EasyFlash tools |

### MSX

| Función | Herramienta |
|---------|------------|
| Ensamblador | Glass, SJASM+ |
| Compilador C | SDCC + fusion-c / MSXgl |
| Editor de tiles | nMSXtiles, MSX Pixel Tools |
| Emulador + debug | **openMSX** (con debugger) |
| Tracker musical | Arkos Tracker 2, TriloTracker |
| Generador de ROM | openMSX-debugger, MSX Hex Tool |

---

## 6. Pipeline de arte — Flujo general

```
Concepto (papel/digital) 
  → Pixel art en editor de PC (Aseprite, ProMotion, herramienta específica)
  → Exportar a formato de plataforma (conversor)
  → Validar en emulador (¿respeta restricciones de color?)
  → Integrar en build (incluir en binario/ROM)
  → Testear in-game
```

### Errores comunes del pipeline de arte

| Error | Consecuencia | Prevención |
|-------|-------------|-----------|
| Artista dibuja sin restricciones de color | Conversión destruye el arte | Template/paleta obligatoria desde día 1 |
| Assets en formato PC (PNG 24-bit) sin conversión | No se pueden integrar | Conversor automático en el build |
| Sprites demasiado grandes | No caben en memoria o gastan slots | Tamaño máximo definido en documento de arte |
| Tiles no reutilizables | Mapa de nivel enorme, no cabe | Guía de diseño de tileset con reutilización |
| Animaciones con muchos frames | Memoria insuficiente | Máximo de frames por animación (3-4 típico) |

---

## 7. Pipeline de audio

```
Composición en tracker (PC)
  → Exportar a formato de plataforma (binary/player)
  → Integrar player en código
  → Testear rendimiento (ciclos consumidos)
  → Ajustar para hardware real (SID 6581/8580, etc.)
```

### Decisiones tempranas de audio

| Decisión | Cuándo | Impacto |
|----------|--------|---------|
| Canales para música vs SFX | Fase 0 | Diseño musical completo |
| ¿Música durante gameplay? (Spectrum 48K) | Fase 0 | Arquitectura de código |
| ¿Samples por software? | Fase 1 | Budget CPU |
| Formato del player | Fase 1 | RAM consumida (~1-3 KB) |

---

## 8. Distribución

### Formatos digitales (emuladores, everdrive)

| Plataforma | Formato | Extensión |
|-----------|---------|-----------|
| CPC | Disco | .dsk |
| CPC | Cinta | .cdt |
| Spectrum | Cinta | .tap, .tzx |
| Spectrum | Disco +3 | .dsk |
| Spectrum | Snapshot | .sna, .z80 |
| C64 | Disco | .d64 |
| C64 | Cartucho | .crt |
| C64 | Programa | .prg |
| MSX | ROM/MegaROM | .rom |
| MSX | Disco | .dsk |
| MSX | Cinta | .cas |

### Canales de distribución (2024-2026)

| Canal | Tipo | Audiencia |
|-------|------|-----------|
| **Itch.io** | Digital, gratis/pago | Global, descubrimiento fácil |
| **Pouet.net** | Digital, gratis (demos) | Demoscene |
| Foro de plataforma (CPCWiki, WOS, CSDb, MSX.org) | Digital, gratis | Comunidad específica |
| **Competiciones** (CPCRetroDev, ZX Dev, MSXdev) | Digital | Visibilidad + premios |
| Distribución física (Poly.Play, RGCD, Bitmap Soft) | Física, pago | Coleccionistas, eventos |
| Everdrive/MiSTer | Digital, hardware real | Hardware enthusiasts |

### Distribución física — Consideraciones

| Aspecto | Detalle |
|---------|---------|
| Coste producción cartucho | ~8-15 € por unidad (pedido mínimo ~50-100) |
| Coste producción cinta | ~3-5 € por unidad |
| Coste producción disco | ~5-8 € por unidad |
| Packaging (caja + manual) | ~5-10 € por unidad |
| PVP habitual | 15-30 € (cinta), 25-50 € (cartucho) |
| Break-even típico | 50-100 unidades vendidas |

---

## 9. Testing

### Niveles de testing

| Nivel | Qué valida | Herramienta |
|-------|-----------|------------|
| **Build automático** | Compila sin errores | Make + CI (GitHub Actions) |
| **Emulador rápido** | Funcionalidad básica | Emulador principal de la plataforma |
| **Emulador con ciclos exactos** | Timing, rendering correcto | VICE (C64), FUSE (Spec), WinAPE (CPC), openMSX |
| **Hardware real** | Bugs específicos de HW | Máquina real + everdrive/carga |
| **Playtest humano** | Jugabilidad, dificultad, bugs de diseño | Beta-testers |

### Cuándo testear en hardware real

- **Obligatorio** si se distribuye en medio físico.
- **Muy recomendable** para juegos con timing crítico (raster IRQ en C64, border effects).
- **Opcional** para distribución solo digital si el emulador es preciso (VICE y openMSX son excelentes).
- **Spectrum**: FUSE es muy preciso pero el hardware real puede revelar contención ULA no emulada.
- **CPC**: WinAPE es fiable; Caprice32 menos (no usar para validar timing).
- **C64**: VICE ciclo-exacto es prácticamente idéntico al HW real. Diferencias raras.
- **MSX**: openMSX es excelente, pero la fragmentación de modelos hace que HW real sea más importante aquí.

---

## 10. Métricas de seguimiento

| Métrica | Cómo medir | Frecuencia |
|---------|-----------|-----------|
| **Ciclos libres por frame** | Medición en emulador (rastertime) | Semanal |
| **Bytes libres de RAM** | Mapa de memoria actualizado | Semanal |
| **Bytes libres de medio** | Tamaño del binario vs capacidad del medio | Semanal |
| **Framerate** | Visual en emulador (border flash technique) | Cada build |
| **Assets producidos vs planificados** | Tracking en spreadsheet o kanban | Semanal |
| **Bugs abiertos** | Bug tracker (GitHub Issues, Trello) | Continuo |

---

## 11. Lecciones aprendidas (post-mortems comunitarios)

Patrones extraídos de post-mortems de CPCRetroDev, ZX Dev, MSXdev y CSDb (2018-2025):

| Lección | Frecuencia | Categoría |
|---------|-----------|-----------|
| "Subestimamos el scroll" | Muy alta | Estimación |
| "El contenido (niveles) fue lo más lento" | Alta | Producción |
| "Debimos probar en HW real antes" | Media | Testing |
| "El scope inicial era demasiado ambicioso" | Muy alta | Scope |
| "La integración arte-código nos retrasó" | Media | Pipeline |
| "El audio se dejó para el final y se nota" | Alta | Planificación |
| "El emulador no mostró un bug que sí aparecía en HW" | Baja-media | Testing |
| "Tener un build jugable pronto motivó al equipo" | Alta | Motivación |
| "Las tools propias nos ahorraron mucho tiempo" | Media | Productividad |

---

## 12. Comparativa rápida de plataformas (decisión PM)

| Factor | CPC | Spectrum | C64 | MSX |
|--------|-----|----------|-----|-----|
| Facilidad de entrada | Media | **Alta** | Media | Media |
| Color | **Mejor** (27, 16 simult.) | Peor (color clash) | Bueno (multicolor) | Medio (15 fijos) |
| Sprites HW | No | No | **Sí (8)** | Sí (32/4 scan) |
| Scroll HW | No | No | **Sí** | No (MSX1) / Sí (MSX2) |
| Audio | AY (3ch) | Beeper/AY | **SID (3ch+filtro)** | AY (3ch) |
| RAM útil | ~42 KB | ~41 KB | **~51 KB** | ~28-48 KB |
| Comunidad activa | Media | **Grande** | **Grande** | Media |
| Herramientas modernas | Buenas | **Muy buenas** | **Muy buenas** | Buenas |
| Competiciones | CPCRetroDev | ZX Dev | Reset64 | MSXdev |
| Ideal para | Color, Mode 0 | Homebrew rápido | Acción/scroll | Cartuchos/RPG |

---

## Checklist general pre-producción

1. [ ] Plataforma(s) target definida(s)
2. [ ] Modo gráfico elegido (afecta a todo el pipeline de arte)
3. [ ] ¿Scroll o flip-screen? (afecta a arquitectura completa)
4. [ ] Budget de sprites / objetos en pantalla
5. [ ] Split audio: canales música vs SFX
6. [ ] Medio de distribución (cinta/disco/cartucho/digital)
7. [ ] Mapa de memoria preliminar
8. [ ] Pipeline de herramientas validado (cada rol puede producir y ver output)
9. [ ] Prototipo técnico con framerate aceptable
10. [ ] Documento de alcance con "must-have" vs "nice-to-have"
11. [ ] Plan de testing (emuladores + HW real si aplica)
12. [ ] Milestone de "build jugable" antes del 30% del timeline
