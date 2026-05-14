#include "game.h"
#include <cpctelera.h>
#include "systems/tilemap.h"
#include "systems/input.h"
#include "systems/collision.h"
#include "entities/player.h"

static Player g_player;

void game_init(void) {
    cpct_disableFirmware();
    cpct_setVideoMode(1);
    cpct_clearScreen(0x00);
    tilemap_init();
    collision_init();
    playerinit(&g_player);
}

void game_update(void) {
    input_update();
    playerupdate(&g_player);
}

void game_render(void) {
    cpct_clearScreen(0x00);
    tilemap_render();
    playerrender(&g_player);
}
