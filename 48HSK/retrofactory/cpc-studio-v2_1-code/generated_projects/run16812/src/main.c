#include <cpctelera.h>
#include "game.h"

void cpc_entry_wrapper(void) __naked {
    __asm
        .globl cpc_run_address
    cpc_run_address::
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
        game_render();
        cpct_waitVSYNC();
    }
}
