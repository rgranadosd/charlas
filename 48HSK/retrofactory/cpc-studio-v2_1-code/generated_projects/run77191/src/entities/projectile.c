#include "projectile.h"
#include "../systems/collision.h"
#include "../data/tileset/projectilesprites.h"
#include <cpctelera.h>

#define MAX_PROJECTILES 8

typedef struct {
    u8 active;
    ProjectileType type;
    u8 x, y;
    u8 vx, vy;
    u8 lifetime;
    u8 facing_left;
} Projectile;

static Projectile projectiles[MAX_PROJECTILES];

void projectile_spawn(u8 x, u8 y, u8 facing_left, ProjectileType type) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) {
            projectiles[i].active = 1;
            projectiles[i].type = type;
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].facing_left = facing_left;
            projectiles[i].lifetime = 60;
            
            if (type == PROJECTILE_LANCE) {
                projectiles[i].vx = facing_left ? -0x40 : 0x40;
                projectiles[i].vy = 0;
            }
            
            return;
        }
    }
}

void projectile_update_all(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) {
            projectiles[i].x += projectiles[i].vx;
            projectiles[i].y += projectiles[i].vy;
            projectiles[i].lifetime--;
            
            if (projectiles[i].lifetime == 0) {
                projectiles[i].active = 0;
            }
        }
    }
}

void projectile_render_all(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (projectiles[i].active) {
            u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y);
            
            if (projectiles[i].type == PROJECTILE_LANCE) {
                if (projectiles[i].facing_left) {
                    cpct_drawSpriteMaskedAlignedTable(
                        lance_left, 
                        pvmem, 8, 4, lance_left_mask
                    );
                } else {
                    cpct_drawSpriteMaskedAlignedTable(
                        lance_right, 
                        pvmem, 8, 4, lance_right_mask
                    );
                }
            }
        }
    }
}

void projectile_clear_all(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        projectiles[i].active = 0;
    }
}