#include "projectile.h"
#include "../systems/collision.h"
#include "../data/sprites/itesprojectiles.h"
#include <cpctelera.h>

ProjectileEntity projectiles[MAX_PROJECTILES];
const u8 max_projectiles = MAX_PROJECTILES;

void projectile_init(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        projectiles[i].active = 0;
    }
}

void projectile_fire(u8 x, u8 y, u8 facing_left, ProjectileType type) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) {
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].width = PROJECTILE_WIDTH;
            projectiles[i].height = PROJECTILE_HEIGHT;
            projectiles[i].facing_left = facing_left;
            projectiles[i].type = type;
            projectiles[i].active = 1;
            
            switch (type) {
                case PLAYER_DAGGER:
                    projectiles[i].speed = 4;
                    projectiles[i].damage = 1;
                    projectiles[i].lifetime = 60;
                    break;
                case ENEMY_ARROW:
                    projectiles[i].speed = 2;
                    projectiles[i].damage = 1;
                    projectiles[i].lifetime = 120;
                    break;
            }
            break;
        }
    }
}

void projectile_update(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) continue;
        
        if (projectiles[i].facing_left) {
            projectiles[i].x -= projectiles[i].speed;
        } else {
            projectiles[i].x += projectiles[i].speed;
        }
        
        projectiles[i].lifetime--;
        if (projectiles[i].lifetime == 0) {
            projectiles[i].active = 0;
        }
        
        // Simple collision with screen edges
        if (projectiles[i].x < 8 || projectiles[i].x > 152) {
            projectiles[i].active = 0;
        }
    }
}

void projectile_render(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) continue;
        
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y);
        
        switch (projectiles[i].type) {
            case PLAYER_DAGGER:
                cpct_drawSpriteMasked(spr_dagger, pvmem, 4, 8);
                break;
            case ENEMY_ARROW:
                cpct_drawSpriteMasked(spr_arrow, pvmem, 4, 16);
                break;
        }
    }
}

void projectile_destroy(u8 index) {
    if (index < MAX_PROJECTILES) {
        projectiles[index].active = 0;
    }
}