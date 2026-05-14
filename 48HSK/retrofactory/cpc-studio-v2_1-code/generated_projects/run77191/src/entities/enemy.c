#include "enemy.h"
#include "../systems/collision.h"
#include "../data/assets/enemysprites.h"
#include <cpctelera.h>

#define MAX_ENEMIES 8

typedef struct {
    u8 active;
    EnemyType type;
    u8 x, y;
    u8 vx, vy;
    u8 health;
    u8 animation_frame;
    u8 animation_counter;
    u8 facing_left;
} Enemy;

static Enemy enemies[MAX_ENEMIES];

void enemy_spawn(EnemyType type, u8 x, u8 y) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (!enemies[i].active) {
            enemies[i].active = 1;
            enemies[i].type = type;
            enemies[i].x = x;
            enemies[i].y = y;
            enemies[i].vx = 0;
            enemies[i].vy = 0;
            enemies[i].health = 1;
            enemies[i].animation_frame = 0;
            enemies[i].animation_counter = 0;
            enemies[i].facing_left = 1;
            
            if (type == ENEMY_ZOMBIE) {
                enemies[i].health = 1;
                enemies[i].vx = 0x08;
            } else if (type == ENEMY_GOBLIN) {
                enemies[i].health = 1;
                enemies[i].vx = 0x10;
            }
            
            return;
        }
    }
}

void enemy_update_all(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].active) {
            // Simple AI
            if (enemies[i].type == ENEMY_ZOMBIE) {
                enemies[i].x += enemies[i].vx;
                enemies[i].animation_counter++;
                if (enemies[i].animation_counter >= 8) {
                    enemies[i].animation_counter = 0;
                    enemies[i].animation_frame++;
                    if (enemies[i].animation_frame >= 4) {
                        enemies[i].animation_frame = 0;
                    }
                }
            }
        }
    }
}

void enemy_render_all(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].active) {
            u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemies[i].x, enemies[i].y);
            
            if (enemies[i].type == ENEMY_ZOMBIE) {
                cpct_drawSpriteMaskedAlignedTable(
                    zombie_walk[enemies[i].animation_frame], 
                    pvmem, 12, 20, zombie_walk_mask
                );
            }
        }
    }
}

void enemy_clear_all(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        enemies[i].active = 0;
    }
}