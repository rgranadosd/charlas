#include "projectile.h"
#include "../systems/collision.h"
#include <cpctelera.h>

#define MAX_PROJECTILES 4

Projectile projectiles[MAX_PROJECTILES];

extern u8 spr_lance[2][8 * 8 / 4];

extern void enemy_take_damage(u8 index, u8 damage);

extern u8 enemy_get_active_count(void);

extern Enemy enemies[];

void projectile_init(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        projectiles[i].active = 0;
    }
}

void projectile_fire(u8 x, u8 y, u8 direction) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) {
            projectiles[i].x = x << 8;
            projectiles[i].y = y << 8;
            projectiles[i].vx = (direction == 1) ? 0x40 : -0x40;
            projectiles[i].vy = 0;
            projectiles[i].type = PLAYER_LANCE;
            projectiles[i].active = 1;
            projectiles[i].anim_frame = 0;
            return;
        }
    }
}

void projectile_update_all(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) {
            projectiles[i].x += projectiles[i].vx;
            projectiles[i].y += projectiles[i].vy;
            
            if (collision_check_tile(projectiles[i].x >> 8, projectiles[i].y >> 8, 8, 8) & COLLISION_SOLID) {
                projectiles[i].active = 0;
                continue;
            }
            
            for (u8 j = 0; j < MAX_ENEMIES; j++) {
                if (enemies[j].active && collision_check_entity(
                    projectiles[i].x >> 8, projectiles[i].y >> 8, 8, 8,
                    enemies[j].x >> 8, enemies[j].y >> 8, 16, 24)) {
                    enemy_take_damage(j, 1);
                    projectiles[i].active = 0;
                    break;
                }
            }
            
            if (projectiles[i].x >> 8 > 160 || projectiles[i].x >> 8 < 0) {
                projectiles[i].active = 0;
            }
        }
    }
}

void projectile_render_all(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) {
            u8* pvmem = cpct_getScreenPtr(cpct_getScreenBuffer(), projectiles[i].x >> 8, projectiles[i].y >> 8);
            u8* sprite = spr_lance[projectiles[i].anim_frame];
            cpct_drawSpriteMaskedAlignedTable(sprite, pvmem, 8, 8, cpct_transparentMaskTable0M0);
        }
    }
}

u8 projectile_get_active_count(void) {
    u8 count = 0;
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) count++;
    }
    return count;
}