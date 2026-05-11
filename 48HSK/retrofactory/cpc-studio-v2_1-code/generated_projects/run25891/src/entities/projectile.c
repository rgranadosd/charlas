#include "projectile.h"
#include "../systems/collision.h"
#include "../entities/enemy.h"
#include "../entities/player.h"
#include <cpctelera.h>

Projectile projectiles[10];

const u8 player_dagger_sprite[16*8/8] = { /* Sprite data */ };
const u8 bone_arrow_sprite[16*8/8] = { /* Sprite data */ };
const u8 imp_fireball_sprite[8*8/8] = { /* Sprite data */ };

void projectile_init(void) {
    for (u8 i = 0; i < 10; i++) {
        projectiles[i].active = 0;
    }
}

void projectile_create(u8 x, u8 y, i8 vx, i8 vy, u8 is_enemy) {
    for (u8 i = 0; i < 10; i++) {
        if (!projectiles[i].active) {
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].vx = vx;
            projectiles[i].vy = vy;
            projectiles[i].lifetime = 60;
            projectiles[i].active = 1;
            projectiles[i].is_enemy = is_enemy;
            
            if (is_enemy) {
                if (vx == 0) {
                    projectiles[i].width = 16;
                    projectiles[i].height = 8;
                } else {
                    projectiles[i].width = 8;
                    projectiles[i].height = 8;
                }
            } else {
                projectiles[i].width = 16;
                projectiles[i].height = 8;
            }
            return;
        }
    }
}

void projectile_update(void) {
    for (u8 i = 0; i < 10; i++) {
        if (projectiles[i].active) {
            projectiles[i].x += projectiles[i].vx;
            projectiles[i].y += projectiles[i].vy;
            projectiles[i].lifetime--;
            
            if (projectiles[i].lifetime == 0 || 
                collision_check_tile(projectiles[i].x, projectiles[i].y, projectiles[i].width, projectiles[i].height, 1)) {
                projectiles[i].active = 0;
                continue;
            }
            
            if (projectiles[i].is_enemy) {
                if (collision_check_entity(projectiles[i].x, projectiles[i].y, projectiles[i].width, projectiles[i].height, 
                                        player.x, player.y, player.width, player.height)) {
                    player_hurt();
                    projectiles[i].active = 0;
                }
            } else {
                for (u8 j = 0; j < 10; j++) {
                    if (enemies[j].active && 
                        collision_check_entity(projectiles[i].x, projectiles[i].y, projectiles[i].width, projectiles[i].height, 
                                            enemies[j].x, enemies[j].y, enemies[j].width, enemies[j].height)) {
                        enemy_hurt(j, 1);
                        projectiles[i].active = 0;
                        break;
                    }
                }
            }
        }
    }
}

void projectile_draw(void) {
    for (u8 i = 0; i < 10; i++) {
        if (projectiles[i].active) {
            const u8* sprite = projectiles[i].is_enemy ? 
                (projectiles[i].width == 16 ? bone_arrow_sprite : imp_fireball_sprite) : 
                player_dagger_sprite;
            cpct_drawSprite(sprite, cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y), 
                          projectiles[i].width, projectiles[i].height);
        }
    }
}