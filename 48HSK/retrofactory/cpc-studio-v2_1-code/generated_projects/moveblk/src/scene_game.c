#include <cpctelera.h>
#include "game.h"
#include "systems/input.h"
#include "entities/player.h"

/* Auto-generated notes
Video mode: Mode 1

Gameplay:
Move block left/right

Art:
Simple solid block

Tech:
Keyboard input + VSYNC loop
*/

void game_init(void) {
    cpct_disableFirmware();
    cpct_setVideoMode(1);
    cpct_clearScreen(0x00);
    player_init();
}

void game_update(void) {
    input_update();
    player_update();
}

void game_render(void) {
    player_render();
}
