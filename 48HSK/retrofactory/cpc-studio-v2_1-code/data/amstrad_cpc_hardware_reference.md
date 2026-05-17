# Amstrad CPC 464 — Referencia técnica para agentes

Fuente: TFG "Desarrollo de un motor de render 3D para Amstrad CPC 464" (Joan Albert Sirvent Jerez, UA, 2017)

---

## CPU

- **Zilog Z80 a 4 MHz** efectivos ~3.3 MHz (comparte bus con chip gráfico)
- Procesador de **8 bits**: operar con tipos > 1 byte (int16, float) multiplica el coste x3-x8
- **REGLA**: usar SIEMPRE `u8` e `i8`. Evitar `u16`/`i16` salvo donde sea imprescindible. NUNCA float.

---

## Memoria RAM (64 KB)

| Bloque | Rango | Uso |
|--------|-------|-----|
| 1 | 0x0000–0x3FFF | ROM firmware (lower ROM). Si está activa, la CPU lee ROM, no RAM. cpct_setVideoMode(0) la desactiva. |
| 2 | 0x4000–0x7FFF | RAM libre: código y datos del juego. El juego arranca en 0x4000. |
| 3 | 0x8000–0xBFFF | Variables del firmware + pila (stack crece hacia abajo desde 0xBFF0). cpct_disableFirmware() libera este bloque. |
| 4 | 0xC000–0xFFFF | **VRAM**: chip gráfico lee desde aquí. 0xC000–0xFE80 = 16000 bytes de pantalla visibles. |

**CPCT_VMEM_START = 0xC000**

---

## Modos gráficos

| Modo | Resolución | Colores simultáneos | Bytes por fila | px/byte |
|------|-----------|---------------------|----------------|---------|
| 0 | 160×200 px | **16** | 80 bytes | 2 px/byte |
| 1 | 320×200 px | 4 | 160 bytes (no es CPCtelera estándar) | 4 px/byte |
| 2 | 640×200 px | 2 | 320 bytes | 8 px/byte |

**Todos los modos usan la misma VRAM** (16000 bytes). **Se usa SIEMPRE el Modo 0** para juegos con colores.

Aspecto de píxel en Modo 0: **2:1** (píxel ladrillo, el doble de ancho que alto).

---

## Codificación de píxeles en Modo 0 (CRÍTICO para sprites)

En Modo 0, **1 byte = 2 píxeles adyacentes** con bits intercalados:

```
Byte:   [ bit7 | bit6 | bit5 | bit4 | bit3 | bit2 | bit1 | bit0 ]
        [  X.3 |  Y.3 |  X.2 |  Y.2 |  X.1 |  Y.1 |  X.0 |  Y.0 ]
         \_____pixel X (izquierda)_____/ \____pixel Y (derecha)____/
```

Donde X.3=bit3 del pen de pixel izquierdo, Y.3=bit3 del pen del pixel derecho, etc.

**Fórmula**: `byte = cpct_px2byteM0(pen_izquierdo, pen_derecho)`

### ⚠ TABLA DE CONVERSIÓN COMPLETA (pen_izquierdo × pen_derecho → byte hex)

```
       P0   P1   P2   P3   P4   P5   P6   P7   P8   P9  P10  P11  P12  P13  P14  P15
P0:  0x00 0x02 0x08 0x0A 0x20 0x22 0x28 0x2A 0x80 0x82 0x88 0x8A 0xA0 0xA2 0xA8 0xAA
P1:  0x04 0x06 0x0C 0x0E 0x24 0x26 0x2C 0x2E 0x84 0x86 0x8C 0x8E 0xA4 0xA6 0xAC 0xAE
P2:  0x10 0x12 0x18 0x1A 0x30 0x32 0x38 0x3A 0x90 0x92 0x98 0x9A 0xB0 0xB2 0xB8 0xBA
P3:  0x14 0x16 0x1C 0x1E 0x34 0x36 0x3C 0x3E 0x94 0x96 0x9C 0x9E 0xB4 0xB6 0xBC 0xBE
P4:  0x40 0x42 0x48 0x4A 0x60 0x62 0x68 0x6A 0xC0 0xC2 0xC8 0xCA 0xE0 0xE2 0xE8 0xEA
P5:  0x44 0x46 0x4C 0x4E 0x64 0x66 0x6C 0x6E 0xC4 0xC6 0xCC 0xCE 0xE4 0xE6 0xEC 0xEE
P6:  0x50 0x52 0x58 0x5A 0x70 0x72 0x78 0x7A 0xD0 0xD2 0xD8 0xDA 0xF0 0xF2 0xF8 0xFA
P7:  0x54 0x56 0x5C 0x5E 0x74 0x76 0x7C 0x7E 0xD4 0xD6 0xDC 0xDE 0xF4 0xF6 0xFC 0xFE
P8:  0x00 0x02 0x08 0x0A 0x20 0x22 0x28 0x2A 0x80 0x82 0x88 0x8A 0xA0 0xA2 0xA8 0xAA
P9:  0x04 0x06 0x0C 0x0E 0x24 0x26 0x2C 0x2E 0x84 0x86 0x8C 0x8E 0xA4 0xA6 0xAC 0xAE
P10: 0x10 0x12 0x18 0x1A 0x30 0x32 0x38 0x3A 0x90 0x92 0x98 0x9A 0xB0 0xB2 0xB8 0xBA
P11: 0x14 0x16 0x1C 0x1E 0x34 0x36 0x3C 0x3E 0x94 0x96 0x9C 0x9E 0xB4 0xB6 0xBC 0xBE
P12: 0x40 0x42 0x48 0x4A 0x60 0x62 0x68 0x6A 0xC0 0xC2 0xC8 0xCA 0xE0 0xE2 0xE8 0xEA
P13: 0x44 0x46 0x4C 0x4E 0x64 0x66 0x6C 0x6E 0xC4 0xC6 0xCC 0xCE 0xE4 0xE6 0xEC 0xEE
P14: 0x50 0x52 0x58 0x5A 0x70 0x72 0x78 0x7A 0xD0 0xD2 0xD8 0xDA 0xF0 0xF2 0xF8 0xFA
P15: 0x54 0x56 0x5C 0x5E 0x74 0x76 0x7C 0x7E 0xD4 0xD6 0xDC 0xDE 0xF4 0xF6 0xFC 0xFE
```

**Valores de un solo pen (ambos píxeles iguales)**:
```
P0=0x00  P1=0x06  P2=0x18  P3=0x1E  P4=0x60  P5=0x66  P6=0x78  P7=0x7E
P8=0x00  P9=0x06  P10=0x18 P11=0x1E P12=0x60 P13=0x66 P14=0x78 P15=0x7E
```

**Nota**: Los pens 0-7 y 8-15 producen los mismos bytes (los bits altos del pen se ignoran en la codificación de 4 bits del Z80).

### ¿Cómo diseñar bytes de sprite?

Para cada fila del sprite, diseña los píxeles de 2 en 2 y usa la tabla:
```
Fila: [px0 px1] [px2 px3] [px4 px5] ... → bytes: tabla[px0][px1], tabla[px2][px3], ...
```

**Ejemplo** — sprite de 4 bytes ancho (8 píxeles CPC), fondo=pen0, contorno=pen6, relleno=pen11:
```
pen layout (8 px): [6 6 11 11 11 11 6 6]
bytes:             [T[6][6]=0x78, T[11][11]=0x1E, T[11][11]=0x1E, T[6][6]=0x78]
              hex: [0x78, 0x1E, 0x1E, 0x78]
```

---

## Paleta por defecto del juego (gpalette, nivel 1)

| Pen | HW color | Nombre | Uso típico |
|-----|----------|--------|-----------|
| 0 | 0x17 | HW_SKY_BLUE | Fondo / transparencia (NUNCA usar en sprites opacos) |
| 1 | 0x14 | HW_BLACK | Suelo, sombras |
| 2 | 0x0E | HW_ORANGE | Plataformas, trampas |
| 3 | 0x0C | HW_BRIGHT_RED | Trampas |
| 4 | 0x0B | HW_BRIGHT_WHITE | Contornos brillantes |
| 5 | 0x0A | HW_BRIGHT_YELLOW | Objetos, pickups |
| 6 | 0x00 | HW_WHITE | Relleno opaco, jugador |
| 7 | 0x06 | HW_CYAN | Enemigos, detalles |
| 8 | 0x15 | HW_BRIGHT_BLUE | HUD |
| 9 | 0x12 | HW_BRIGHT_GREEN | Checkpoint |
| 10 | 0x1E | HW_YELLOW | Pickups secundarios |
| 11 | 0x16 | HW_GREEN | Plataformas secundarias |
| 12 | 0x07 | HW_PINK | Efectos |
| 13 | 0x1A | HW_LIME | Proyectiles |
| 14 | 0x1C | HW_RED | Daño, boss |
| 15 | 0x1F | HW_PASTEL_BLUE | HUD secundario |

**PEN 0 = fondo**. `cpct_drawSprite` copia bytes sin transparencia. Si un sprite usa pen 0, esos píxeles se ven como fondo → sprite invisible en esas zonas. Usar pen 1 (negro, byte 0xC0) como fondo opaco de sprite.

---

## VRAM no lineal

El chip gráfico del CPC dibuja líneas NO consecutivamente: cada scanline está 0x800 bytes más lejos que la anterior, y cada 8 scanlines hace wrap de -0xF800+0x50.

**REGLA**: Usar siempre `cpct_getScreenPtr(CPCT_VMEM_START, x_bytes, y_pixels)` para calcular punteros VRAM. NUNCA calcular offsets manualmente.

`cpct_drawSprite` y `cpct_drawSolidBox` manejan internamente la no-linealidad.

---

## Coordenadas en Modo 0

- `cpct_getScreenPtr(base, x, y)`: **x en BYTES** (0–79), **y en píxeles/filas** (0–199)
- Pantalla = 80 bytes ancho × 200 filas alto
- Sprite de ancho W bytes empieza en x → ocupa columnas [x, x+W-1]
- **Condición límite**: x + W ≤ 79 (o 80 si va hasta el borde exacto). Si x+W > 80 → corrupción VRAM.

---

## Timings críticos de render

| Operación | Tiempo aprox. |
|-----------|--------------|
| `cpct_clearScreen(color)` | ~21ms (usa LDIR optimizado) |
| `cpct_clearScreen_f8(color)` | ~21ms (borra 8 bytes/iter) |
| `cpct_drawSolidBox(width=40, height=200)` | ~46ms |
| Dos `cpct_drawSolidBox(40, 200)` para pantalla completa | **~92ms = 4.6 frames → TEARING** |
| `cpct_drawSprite(8 bytes × 24 rows)` | ~0.5ms |
| Un frame completo a 50Hz | 20ms |

**REGLA**: Para limpiar la pantalla entera cada frame → `cpct_clearScreen_f8(0x0000)`.

---

## Control de input

### Teclado CPC (hardware directo)
```c
cpct_scanKeyboard();  // SIEMPRE esto, NUNCA cpct_scanKeyboard_f() con firmware deshabilitado
cpct_isKeyPressed(Key_CursorLeft);  // Teclas cursor del CPC
cpct_isKeyPressed(Key_A);           // Letras del CPC
```

### Joystick / Caprice32 en macOS
En Caprice32 con `joystick_emulation=1` en cap32.cfg, las flechas del PC van al **puerto joystick**, no al teclado cursor del CPC:
```c
// CORRECTO: leer AMBOS (teclado CPC + joystick emulado)
left  = cpct_isKeyPressed(Key_CursorLeft)  || cpct_isKeyPressed(Key_A) || cpct_isKeyPressed(Joy0_Left);
right = cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_D) || cpct_isKeyPressed(Joy0_Right);
jump  = cpct_isKeyPressed(Key_CursorUp)    || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Joy0_Up);
shoot = cpct_isKeyPressed(Key_Space)       || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Joy0_Fire1);
```

`cap32.cfg` debe tener `joystick_emulation=1`.

---

## Inicialización obligatoria (orden fijo)

```c
cpct_setVideoMode(0);       // 1. PRIMERO: desactiva lower ROM
cpct_disableFirmware();     // 2. SEGUNDO: parchea 0x0038 (ahora sí funciona)
cpct_setPalette(pal, 16);   // 3. Configurar paleta
cpct_setBorder(pal[0]);     // 4. Borde = color de fondo
cpct_clearScreen_f8(0x0000);// 5. Limpiar VRAM
```

Si el orden 1-2 está invertido → crash silencioso, 0 FPS, juego no arranca.

---

## Entry point y link order

- `game.c` se enlaza ANTES que `main.c` (orden alfabético → `g < m`)
- La dirección 0x4000 contiene el inicio de `game.c`, NO `cpc_run_address`
- **SOLUCIÓN**: Primera función de `game.c` debe ser el JP stub:
  ```c
  void __game_entry_jp(void) __naked {
      __asm
          .globl cpc_run_address
          jp cpc_run_address
      __endasm;
  }
  ```
- `DISC.BAS` siempre `CALL 16384` (0x4000). NUNCA una dirección calculada en tiempo de build.

---

## Sprites: reglas de diseño

1. Cada byte = 2 píxeles. Sprite de W bytes = W×2 píxeles CPC.
2. Usar la tabla de conversión pen→byte para todos los bytes. NUNCA usar el valor del pen directamente.
3. Pen 0 = fondo (invisible) → usar pen 1 (0xC0 = negro sólido) como fill opaco.
4. Valores clave: pen4+pen4=0x30 (BRIGHT_WHITE), pen1+pen1=0xC0 (BLACK), pen6+pen6=0x3C (WHITE).
5. Mínimo visible: 4 bytes × 8 filas (8 px × 8 px CPC).
6. Jugador recomendado: 8 bytes × 24 filas (16 px × 24 px CPC).
7. Tamaños declarados (w, h) deben coincidir EXACTAMENTE con los bytes del array: `total = w * h`.
8. `cpct_drawSprite(sprite, pvmem, w, h)`: w en bytes, h en filas.
