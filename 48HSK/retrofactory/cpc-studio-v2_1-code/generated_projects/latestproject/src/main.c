#include "game.h"

void main(void) {
    game_init();
    while (1) {
        game_update();
        game_render();
    }
}
