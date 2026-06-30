# CPC / CPCtelera Known Bugs and Gotchas

Estas son lecciones aprendidas reales del proyecto retrostudio.
El agente experto debe recuperarlas cuando detecte síntomas similares.

---

## BUG-001: Encoding de píxeles en modo 0 — los bytes están invertidos

**Síntoma:** Sprites o `cpct_drawSolidBox` producen píxeles invisibles o del color
equivocado, aunque la paleta esté correctamente configurada. Los objetos parecen
pintarse con el color del fondo.

**Causa raíz:** En CPC modo 0 los 4 bits del índice de pen se reparten de forma
intercalada entre los 8 bits del byte de vídeo. NO es un nibble simple.

**Codificación CORRECTA para dos píxeles del mismo pen (modo 0):**

| pen | byte correcto | pen | byte correcto |
|-----|---------------|-----|---------------|
|  0  | `0x00`        |  8  | `0xC0`        |
|  1  | `0x03`        |  9  | `0xC3`        |
|  2  | `0x0C`        | 10  | `0xCC`        |
|  3  | `0x0F`        | 11  | `0xCF`        |
|  4  | `0x30`        | 12  | `0xF0`        |
|  5  | `0x33`        | 13  | `0xF3`        |
|  6  | `0x3C`        | 14  | `0xFC`        |
|  7  | `0x3F`        | 15  | `0xFF`        |

**Fórmula de cálculo (Python):**
```python
def mode0_pen_byte(pen: int) -> int:
    b = 0
    if pen & 0x08: b |= 0xC0  # pen_bit3 -> byte bits 7,6
    if pen & 0x04: b |= 0x30  # pen_bit2 -> byte bits 5,4
    if pen & 0x02: b |= 0x0C  # pen_bit1 -> byte bits 3,2
    if pen & 0x01: b |= 0x03  # pen_bit0 -> byte bits 1,0
    return b
```

**Error clásico:** usar `0xC0` para pen 1 (se creía "pen 1 = bit alto") cuando en
realidad `0xC0` descodifica como pen 8. Si la paleta solo define pens 0-3,
pen 8 queda sin definir y hereda el color del fondo → objeto invisible.

**Cuándo se aplica:** `cpct_drawSolidBox`, cualquier array de sprite creado a mano,
inicialización de buffers de vídeo con `cpct_memset`.

**Funciones CPCtelera seguras que evitan este error:**
- `cpct_px2byteM0(p0, p1)` — convierte dos pen a byte en tiempo de compilación
- `cpct_drawSprite` con sprites generados por herramientas (Img2CPC, etc.)
- `cpct_drawStringM0` — maneja el encoding internamente

**Regla del agente:** Si una entidad usa `cpct_drawSolidBox` con modo 0 y el byte
no coincide con la tabla anterior, marcar como **error crítico de visibilidad**.

---

## BUG-002: `cpct_clearScreen` es demasiado lento para el bucle principal

**Síntoma:** Flickering severo, pantalla que parpadea cada frame.

**Causa raíz:** `cpct_clearScreen` rellena 16 KB con `cpct_memset`. A 4 MHz Z80
eso tarda ~18 ms — casi un frame completo a 50 Hz (20 ms). Si además dibujas
sprites, el tiempo total supera el frame y la imagen parpadea.

**Solución:** Erase/draw por entidad:
```c
// Erase anterior (pen 0 = fondo)
cpct_drawSolidBox(pvmem_prev, 0x00, w, h);
// Update physics
// Draw nuevo
cpct_drawSolidBox(pvmem_new, pen_byte, w, h);
```
Coste: solo los bytes del sprite, no los 16 KB.

---

## BUG-003: Variables declaradas después de sentencias (C89 / SDCC)

**Síntoma:** Error de compilación SDCC: `syntax error: token -> 'u8'`

**Causa raíz:** SDCC compila en modo C89. Las variables DEBEN declararse al inicio
del bloque, antes de cualquier sentencia o llamada a función.

**Incorrecto:**
```c
cpct_disableFirmware();
u8* pvmem = cpct_getScreenPtr(...);  // ERROR: declaración tras sentencia
```

**Correcto:**
```c
u8* pvmem;                           // declaración primero
cpct_disableFirmware();
pvmem = cpct_getScreenPtr(...);
```

---

## BUG-004: `cpct_getScreenPtr` usa coordenadas en BYTES, no píxeles

**Síntoma:** Sprite dibujado en posición incorrecta (desplazado o fuera de pantalla).

**Causa raíz:** El parámetro `x` de `cpct_getScreenPtr(CPCT_VMEM_START, x, y)` es
en BYTES (0-79 para modo 0 de 80 bytes de ancho), no en píxeles (0-159).

**Modo 0:** 1 byte = 2 píxeles. Si quieres x=80 píxeles → pasas x=40 bytes.

---

## BUG-005: `cpct_drawStringM0` — primer argumento es `void*` no `const char*`

**Síntoma:** Warning SDCC o comportamiento inesperado.

**Causa raíz:** La firma real es `cpct_drawStringM0(void* string, void* pvmem, ...)`.
Declarar el buffer como `const u8[]` puede generar un warning de cast.

**Solución:** Declarar sin `const`:
```c
u8 g_score_txt[] = "00000";  // correcto
// NO: const u8 g_score_txt[] = ...
```

---

## BUG-006: `cpct_setPalette` con menos de 16 pens — pens no definidos heredan valores

**Síntoma:** Sprites que usan pens > N aparecen del color equivocado.

**Causa raíz:** Si llamas `cpct_setPalette(g_palette, 4)`, solo defines pens 0-3.
Los pens 4-15 mantienen el valor de hardware previo (estado del firmware antes de
`cpct_disableFirmware`). Ese valor puede coincidir con el fondo → objeto invisible.

**Solución:** O defines todos los pens que uses, o usas solo pens 0-3 con
sprites correctamente codificados (ver BUG-001).
