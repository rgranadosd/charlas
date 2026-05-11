#ifndef _COLLISION_H_
#define _COLLISION_H_

#include <cpctelera.h>
#include "../entities/player.h"
#include "../entities/enemy.h"
#include "../entities/projectile.h"

u8 collision_check_tile(i16 x, i16 y, u8 width, u8 height);
void collision_check_all(TPlayer* player, TEnemy* enemies, u8* enemy_count, TProjectile* projectiles, u8* projectile_count);

#endif