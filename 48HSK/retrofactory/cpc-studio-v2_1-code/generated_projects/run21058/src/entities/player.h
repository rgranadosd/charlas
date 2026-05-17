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
    u8 health;
    u8 weapon;
    u8 facing_left;
    u8 jump_hold;
} Player;

void playerinit(Player* player);
void playerupdate(Player* player);
void playerrender(const Player* player);
u8 player_get_ammo(const Player* player);
u8 player_get_health(const Player* player);
u8 player_get_weapon(const Player* player);

#endif
