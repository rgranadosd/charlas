#include "projectile.h"
#include "../systems/collision.h"
#include <cpctelera.h>

#define MAX_PROJECTILES 8

Projectile projectiles[MAX_PROJECTILES];

extern u8* const level1_collision_map;

extern const u8 level1_tilemap_width;

extern const u8 level1_tilemap_height;

void projectile_init(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        projectiles[i].active = 0;
    }
}

void projectile_create(u8 x, u8 y, i8 vx, i8 vy, u8 type) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) {
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].vx = vx;
            projectiles[i].vy = vy;
            projectiles[i].type = type;
            projectiles[i].active = 1;
            projectiles[i].range = 0;
            
            switch (type) {
                case PROJECTILE_LANCE:
                    projectiles[i].width = 16;
                    projectiles[i].height = 8;
                    break;
                case PROJECTILE_DAGGER:
                    projectiles[i].width = 8;
                    projectiles[i].height = 8;
                    break;
                case PROJECTILE_FIREBALL:
                    projectiles[i].width = 16;
                    projectiles[i].height = 16;
                    break;
                case PROJECTILE_ENEMY_ARROW:
                    projectiles[i].width = 8;
                    projectiles[i].height = 4;
                    break;
            }
            return;
        }
    }
}

void projectile_update(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) {
            projectiles[i].x += projectiles[i].vx;
            projectiles[i].y += projectiles[i].vy;
            projectiles[i].range++;
            
            if (projectiles[i].range > 100 || 
                collision_check_projectile_tilemap(projectiles[i].x, projectiles[i].y, 
                                                projectiles[i].width, projectiles[i].height)) {
                projectiles[i].active = 0;
            }
            
            for (u8 j = 0; j < MAX_ENEMIES; j++) {
                if (enemies[j].active && collision_check_projectile_enemy(&projectiles[i], &enemies[j])) {
                    enemy_take_damage(j, 1);
                    projectiles[i].active = 0;
                    break;
                }
            }
        }
    }
}

void projectile_render(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) {
            u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y);
            cpct_drawSprite(projectile_sprites[projectiles[i].type], pvmem, 
                          projectiles[i].width, projectiles[i].height);
        }
    }
}