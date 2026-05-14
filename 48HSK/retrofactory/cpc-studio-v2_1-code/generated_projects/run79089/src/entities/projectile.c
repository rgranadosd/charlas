#include "projectile.h"
#include "../systems/collision.h"
#include "../data/tileset/projectilesprites.h"

Projectile projectiles[16];

void projectile_init(void) {
    for (u8 i = 0; i < 16; i++) {
        projectiles[i].active = 0;
    }
}

void projectile_fire(u8 x, u8 y, u8 type) {
    for (u8 i = 0; i < 16; i++) {
        if (!projectiles[i].active) {
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].type = type;
            projectiles[i].lifetime = 60;
            projectiles[i].active = 1;
            
            switch (type) {
                case LANCE:
                    projectiles[i].vx = 4;
                    projectiles[i].vy = 0;
                    break;
                case AXE:
                    projectiles[i].vx = 3;
                    projectiles[i].vy = -1;
                    break;
                case HOLY_FIRE:
                    projectiles[i].vx = 2;
                    projectiles[i].vy = 0;
                    break;
                case ARROW:
                    projectiles[i].vx = -3;
                    projectiles[i].vy = 0;
                    break;
            }
            return;
        }
    }
}

void projectile_update(void) {
    for (u8 i = 0; i < 16; i++) {
        if (!projectiles[i].active) continue;
        
        projectiles[i].x += projectiles[i].vx;
        projectiles[i].y += projectiles[i].vy;
        projectiles[i].lifetime--;
        
        if (projectiles[i].lifetime == 0 || projectiles[i].x > 160) {
            projectiles[i].active = 0;
            continue;
        }
        
        if (collision_check_projectile_enemy(i)) {
            projectiles[i].active = 0;
        }
    }
}

void projectile_render(void) {
    for (u8 i = 0; i < 16; i++) {
        if (!projectiles[i].active) continue;
        
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y);
        u8 sprite_frame = 0;
        
        switch (projectiles[i].type) {
            case LANCE:
                sprite_frame = 0;
                cpct_drawSprite(projectile_sprites[sprite_frame], pvmem, 4, 4);
                break;
            case AXE:
                sprite_frame = 1;
                cpct_drawSprite(projectile_sprites[sprite_frame], pvmem, 8, 8);
                break;
            case HOLY_FIRE:
                sprite_frame = 2;
                cpct_drawSprite(projectile_sprites[sprite_frame], pvmem, 6, 6);
                break;
            case ARROW:
                sprite_frame = 3;
                cpct_drawSprite(projectile_sprites[sprite_frame], pvmem, 4, 4);
                break;
        }
    }
}