#include "game.h"
#include <cpctelera.h>

void game_init(void) {
    cpct_disableFirmware();
    cpct_setVideoMode(1);
    cpct_clearScreen(0x00);
}

void game_update(void) {
}

void game_render(void) {
}
