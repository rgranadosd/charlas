#include <cpctelera.h>
#include "game.h"

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
