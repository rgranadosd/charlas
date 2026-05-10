#include "game.h"
#include "systems/input.h"
#include "entities/player.h"

/* Auto-generated notes
Video mode: Mode 1

Gameplay:
Test gameplay spec

Art:
Test art spec

Tech:
Test implementation plan
*/

void game_init(void) {
    player_init();
}

void game_update(void) {
    input_update();
    player_update();
}

void game_render(void) {
    player_render();
}
