#ifndef _COLLISION_H_
#define _COLLISION_H_

#include <types.h>
#include "../entities/player.h"
#include "../entities/enemy.h"
#include "../entities/projectile.h"

u8 collision_check_player_tilemap(u8 x, u8 y, u8 width, u8 height);
u8 collision_check_enemy_tilemap(u8 x, u8 y, u8 width, u8 height);
u8 collision_check_projectile_tilemap(u8 x, u8 y, u8 width, u8 height);
u8 collision_check_player_enemy(Enemy* enemy);
u8 collision_check_projectile_enemy(Projectile* projectile, Enemy* enemy);

#endif