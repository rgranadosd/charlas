#include "enemy.h"
#include "../systems/collision.h"
#include <cpctelera.h>

#define MAX_ENEMIES 8

Enemy enemies[MAX_ENEMIES];

extern u8* const level1_collision_map;

extern const u8 level1_tilemap_width;

extern const u8 level1_tilemap_height;

void enemy_init(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        enemies[i].active = 0;
    }
}

void enemy_spawn(u8 type, u8 x, u8 y) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (!enemies[i].active) {
            enemies[i].x = x;
            enemies[i].y = y;
            enemies[i].type = type;
            enemies[i].health = 1;
            enemies[i].state = ENEMY_IDLE;
            enemies[i].frame = 0;
            enemies[i].active = 1;
            
            switch (type) {
                case ENEMY_ZOMBIE:
                    enemies[i].width = 16;
                    enemies[i].height = 24;
                    enemies[i].vx = -1;
                    break;
                case ENEMY_GARGOYLE:
                    enemies[i].width = 24;
                    enemies[i].height = 24;
                    enemies[i].vx = -1;
                    enemies[i].vy = 0;
                    break;
                case ENEMY_HELLHOUND:
                    enemies[i].width = 24;
                    enemies[i].height = 16;
                    enemies[i].vx = -3;
                    break;
            }
            return;
        }
    }
}

void enemy_update(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].active) {
            u8 new_x = enemies[i].x + enemies[i].vx;
            u8 new_y = enemies[i].y + enemies[i].vy;
            
            if (!collision_check_enemy_tilemap(new_x, enemies[i].y, enemies[i].width, enemies[i].height)) {
                enemies[i].x = new_x;
            }
            
            if (!collision_check_enemy_tilemap(enemies[i].x, new_y, enemies[i].width, enemies[i].height)) {
                enemies[i].y = new_y;
            }
            
            if (collision_check_player_enemy(&enemies[i])) {
                // Player takes damage
            }
        }
    }
}

void enemy_take_damage(u8 index, u8 damage) {
    if (index < MAX_ENEMIES && enemies[index].active) {
        enemies[index].health -= damage;
        if (enemies[index].health <= 0) {
            enemies[index].active = 0;
        }
    }
}

void enemy_render(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].active) {
            u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemies[i].x, enemies[i].y);
            cpct_drawSpriteMaskedAlignedTable(enemy_sprites[enemies[i].type], pvmem, 
                                            enemies[i].width, enemies[i].height, 
                                            enemy_masks[enemies[i].type]);
        }
    }
}