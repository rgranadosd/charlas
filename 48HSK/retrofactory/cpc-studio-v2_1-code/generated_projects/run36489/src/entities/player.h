#ifndef ENTITIES_PLAYER_H
#define ENTITIES_PLAYER_H

#include <cpctelera.h>

typedef struct {
    u8 x;
    u8 y;
    i8 vx;
    i8 vy;
    u8 w;
    u8 h;
} Player;

void playerinit(Player* player);
void playerupdate(Player* player);
void playerrender(const Player* player);

#endif
