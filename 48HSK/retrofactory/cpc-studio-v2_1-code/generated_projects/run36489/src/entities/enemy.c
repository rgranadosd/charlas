#include "enemy.h"
#include "../systems/collision.h"
#include "../data/sprites/itesenemies.h"
#include <cpctelera.h>

#define MAX_ENEMIES 8

Enemy enemies[MAX_ENEMIES];
u8 enemy_count = 0;

void enemy_init(void) {
    enemy_count = 0;
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        enemies[i].state = ENEMY_DEATH;
    }
}

void enemy_spawn(u8 x, u8 y, u8 type) {
    if (enemy_count >= MAX_ENEMIES) return;
    
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].state == ENEMY_DEATH) {
            enemies[i].x = x;
            enemies[i].y = y;
            enemies[i].type = type;
            enemies[i].state = ENEMY_IDLE;
            enemies[i].facing_left = 1;
            
            switch (type) {
                case ENEMY_ZOMBIE:
                    enemies[i].width = 4;
                    enemies[i].height = 8;
                    enemies[i].speed_x = 1;
                    enemies[i].health = 1;
                    enemies[i].patrol_left = x - 20;
                    enemies[i].patrol_right = x + 20;
                    break;
                case ENEMY_SKELETON_ARCHER:
                    enemies[i].width = 4;
                    enemies[i].height = 8;
                    enemies[i].speed_x = 0;
                    enemies[i].health = 2;
                    break;
                case ENEMY_FLYING_HARPY:
                    enemies[i].width = 4;
                    enemies[i].height = 4;
                    enemies[i].speed_x = 1;
                    enemies[i].speed_y = 1;
                    enemies[i].health = 1;
                    break;
            }
            enemy_count++;
            break;
        }
    }
}

void enemy_update_zombie(u8 index) {
    Enemy* e = &enemies[index];
    
    if (e->x <= e->patrol_left) e->facing_left = 0;
    if (e->x >= e->patrol_right) e->facing_left = 1;
    
    e->speed_x = e->facing_left ? -1 : 1;
    e->x += e->speed_x;
    
    if (cpct_rand() % 60 == 0) {
        e->state = ENEMY_ATTACK;
    }
}

void enemy_update_skeleton_archer(u8 index) {
    Enemy* e = &enemies[index];
    
    if (cpct_rand() % 120 == 0) {
        e->state = ENEMY_ATTACK;
    }
}

void enemy_update_flying_harpy(u8 index) {
    Enemy* e = &enemies[index];
    
    e->x += e->speed_x;
    e->y += e->speed_y;
    
    if (e->x <= 0 || e->x >= 160 - e->width) e->speed_x = -e->speed_x;
    if (e->y <= 0 || e->y >= 200 - e->height) e->speed_y = -e->speed_y;
    
    if (cpct_rand() % 90 == 0) {
        e->state = ENEMY_ATTACK;
    }
}

void enemy_update(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].state == ENEMY_DEATH) continue;
        
        switch (enemies[i].type) {
            case ENEMY_ZOMBIE:
                enemy_update_zombie(i);
                break;
            case ENEMY_SKELETON_ARCHER:
                enemy_update_skeleton_archer(i);
                break;
            case ENEMY_FLYING_HARPY:
                enemy_update_flying_harpy(i);
                break;
        }
    }
}

void enemy_render(void) {
    for (u8 i = 0; i < MAX_ENEMIES; i++) {
        if (enemies[i].state == ENEMY_DEATH) continue;
        
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemies[i].x, enemies[i].y);
        
        switch (enemies[i].type) {
            case ENEMY_ZOMBIE:
                cpct_drawSprite(itesenemies_zombie_walk[(cpct_frameCounter >> 3) % 2], pvmem, 4, 8);
                break;
            case ENEMY_SKELETON_ARCHER:
                cpct_drawSprite(itesenemies_skeleton_idle, pvmem, 4, 8);
                break;
            case ENEMY_FLYING_HARPY:
                cpct_drawSprite(itesenemies_harpy_fly[(cpct_frameCounter >> 3) % 2], pvmem, 4, 4);
                break;
        }
    }
}

void enemy_damage(u8 index) {
    if (enemies[index].state == ENEMY_HURT || enemies[index].state == ENEMY_DEATH) return;
    
    enemies[index].health--;
    if (enemies[index].health == 0) {
        enemy_kill(index);
    } else {
        enemies[index].state = ENEMY_HURT;
    }
}

void enemy_kill(u8 index) {
    enemies[index].state = ENEMY_DEATH;
    enemy_count--;
}