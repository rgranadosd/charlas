#ifndef _ANIMATION_H_
#define _ANIMATION_H_

#include <cpctelera.h>
#include "../entities/player.h"
#include "../entities/enemy.h"

void animation_update_player(TPlayer* player);
void animation_update_enemy(TEnemy* enemy);

#endif