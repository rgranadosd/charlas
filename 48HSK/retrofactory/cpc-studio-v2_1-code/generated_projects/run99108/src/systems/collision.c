#include "collision.h"
#include "../data/level1.h"
#include <cpctelera.h>

extern u8* const level1_collision_map;
extern const u8 level1_tilemap_width;
extern const u8 level1_tilemap_height;

static u8 check_tile_collision(u8 x, u8 y, u8 width, u8 height) {
    u8 tile_x1 = x >> 3;
    u8 tile_y1 = y >> 3;
    u8 tile_x2 = (x + width - 1) >> 3;
    u8 tile_y2 = (y + height - 1) >> 3;
    
    for (u8 ty = tile_y1; ty <= tile_y2; ty++) {
        for (u8 tx = tile_x1; tx <= tile_x2; tx++) {
            if (ty < level1_tilemap_height && tx < level1_tilemap_width) {
                u8 tile = level1_collision_map[ty * level1_tilemap_width + tx];
                if (tile) return 1;
            }
        }
    }
    return 0;
}

u8 collision_check_player_tilemap(u8 x, u8 y, u8 width, u8 height) {
    return check_tile_collision(x, y, width, height);
}

u8 collision_check_enemy_tilemap(u8 x, u8 y, u8 width, u8 height) {
    return check_tile_collision(x, y, width, height);
}

u8 collision_check_projectile_tilemap(u8 x, u8 y, u8 width, u8 height) {
    return check_tile_collision(x, y, width, height);
}

u8 collision_check_player_enemy(Enemy* enemy) {
    return (player.x < enemy->x + enemy->width &&
            player.x + player.width > enemy->x &&
            player.y < enemy->y + enemy->height &&
            player.y + player.height > enemy->y);
}

u8 collision_check_projectile_enemy(Projectile* projectile, Enemy* enemy) {
    return (projectile->x < enemy->x + enemy->width &&
            projectile->x + projectile->width > enemy->x &&
            projectile->y < enemy->y + enemy->height &&
            projectile->y + projectile->height > enemy->y);
}