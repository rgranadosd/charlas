#include "projectile.h"
#include "../systems/collision.h"
#include "../data/sprites/itesprojectiles.h"
#include <cpctelera.h>

#define MAX_PROJECTILES 8

Projectile projectiles[MAX_PROJECTILES];

void projectile_init(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        projectiles[i].active = 0;
    }
}

void projectile_fire(u8 x, u8 y, u8 facing_left, u8 type) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) {
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].type = type;
            projectiles[i].active = 1;
            projectiles[i].lifetime = 60;
            
            switch (type) {
                case PROJECTILE_ARROW:
                    projectiles[i].width = 2;
                    projectiles[i].height = 2;
                    projectiles[i].speed_x = facing_left ? -3 : 3;
                    projectiles[i].speed_y = 0;
                    break;
                case PROJECTILE_LANCE:
                    projectiles[i].width = 4;
                    projectiles[i].height = 2;
                    projectiles[i].speed_x = facing_left ? -4 : 4;
                    projectiles[i].speed_y = 0;
                    break;
                case PROJECTILE_MAGIC_ORB:
                    projectiles[i].width = 2;
                    projectiles[i].height = 2;
                    projectiles[i].speed_x = facing_left ? -2 : 2;
                    projectiles[i].speed_y = 1;
                    break;
            }
            break;
        }
    }
}

void projectile_update(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) continue;
        
        projectiles[i].x += projectiles[i].speed_x;
        projectiles[i].y += projectiles[i].speed_y;
        projectiles[i].lifetime--;
        
        if (projectiles[i].lifetime == 0 || 
            collision_check_entity_tilemap(projectiles[i].x, projectiles[i].y, 
                                         projectiles[i].width, projectiles[i].height)) {
            projectile_destroy(i);
        }
    }
}

void projectile_render(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) continue;
        
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y);
        
        switch (projectiles[i].type) {
            case PROJECTILE_ARROW:
                cpct_drawSprite(itesprojectiles_arrow, pvmem, 2, 2);
                break;
            case PROJECTILE_LANCE:
                cpct_drawSprite(itesprojectiles_lance, pvmem, 4, 2);
                break;
            case PROJECTILE_MAGIC_ORB:
                cpct_drawSprite(itesprojectiles_magic_orb[(cpct_frameCounter >> 2) % 2], pvmem, 2, 2);
                break;
        }
    }
}

void projectile_destroy(u8 index) {
    projectiles[index].active = 0;
}