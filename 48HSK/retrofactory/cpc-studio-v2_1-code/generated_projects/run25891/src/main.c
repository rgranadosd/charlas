#include <cpctelera.h>
#include "game.h"

int main(void) {
    game_init();

    while (1) {
        game_update();
        game_render();
        cpct_waitVSYNC();
    }

    return 0;
}
