#include "collision.h"
#include "../data/level1.h"
#include "../game.h"

#define TILE_SIZE 4

u8 collision_check_tile(i16 x, i16 y, u8 width, u8 height) {
    u8 tile_x1 = x / TILE_SIZE;
    u8 tile_y1 = y / TILE_SIZE;
    u8 tile_x2 = (x + width - 1) / TILE_SIZE;
    u8 tile_y2 = (y + height - 1) / TILE_SIZE;
    
    for (u8 tx = tile_x1; tx <= tile_x2; tx++) {
        for (u8 ty = tile_y1; ty <= tile_y2; ty++) {
            if (tilemap_get_collision(tx, ty)) {
                return 1;
            }
        }
    }
    return 0;
}

void collision_check_all(TPlayer* player, TEnemy* enemies, u8* enemy_count, TProjectile* projectiles, u8* projectile_count) {
    for (u8 i = 0; i < *enemy_count; i++) {
        if (enemies[i].health > 0 && player->invulnerability == 0) {
            if (player->x < enemies[i].x + enemies[i].width &&
                player->x + player->width > enemies[i].x &&
                player->y < enemies[i].y + enemies[i].height &&
                player->y + player->height > enemies[i].y) {
                player_hit(player, 1);
            }
        }
    }
    
    if (player->state == PLAYER_STATE_ATTACKING && player->frame == 1) {
        for (u8 i = 0; i < *enemy_count; i++) {
            if (enemies[i].health > 0) {
                i16 attack_x = player->x + (player->direction == PLAYER_DIR_RIGHT ? player->width : -8);
                if (attack_x < enemies[i].x + enemies[i].width &&
                    attack_x + 8 > enemies[i].x &&
                    player->y < enemies[i].y + enemies[i].height &&
                    player->y + player->height > enemies[i].y) {
                    enemy_hit(&enemies[i], 1);
                    add_score(100);
                }
            }
        }
    }
    
    for (u8 i = 0; i < *projectile_count; i++) {
        if (projectiles[i].active && projectiles[i].type == PROJECTILE_TYPE_ARROW && player->invulnerability == 0) {
            if (projectiles[i].x < player->x + player->width &&
                projectiles[i].x + projectiles[i].width > player->x &&
                projectiles[i].y < player->y + player->height &&
                projectiles[i].y + projectiles[i].height > player->y) {
                player_hit(player, 1);
                projectiles[i].active = 0;
            }
        }
    }
}