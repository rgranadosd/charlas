#include <cpctelera.h>
#include "game.h"

void cpc_entry_wrapper(void) __naked {
    __asm
        .globl cpc_run_address
        .globl s__INITIALIZER
        .globl s__INITIALIZED
        .globl l__INITIALIZER
    cpc_run_address::
        di
        ld sp, #0xBFF0
        ld bc, #l__INITIALIZER
        ld a, b
        or c
        jr z, 00001$
        ld de, #s__INITIALIZED
        ld hl, #s__INITIALIZER
        ldir
00001$:
        call _main
        ret
    __endasm;
}

void main(void) {
    /* Force a known-good stack pointer below firmware RAM (--no-std-crt0). */
    __asm
        di
        ld sp, #0xBFF0
    __endasm;

    game_init();
    while (1) {
        game_update();
        cpct_waitVSYNC();  /* sync BEFORE clear+draw: beam is at top when we start clearing */
        game_render();
    }
}
