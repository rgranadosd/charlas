#include <cpctelera.h>
#include "game.h"

void main(void) {
    cpct_disableFirmware();
    game_init();
    
    while (1) {
        game_update();
        game_render();
        cpct_waitVSYNC();
    }
}