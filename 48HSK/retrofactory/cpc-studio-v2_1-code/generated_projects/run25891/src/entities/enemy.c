#include "enemy.h"
#include "../systems/collision.h"
#include "../data/level1.h"
#include <cpctelera.h>

Enemy enemies[10];

const u8 zombie_idle[2][16*32/8] = { /* Sprite data */ };
const u8 zombie_walk[4][16*32/8] = { /* Sprite data */ };
const u8 skeleton_idle[1][16*32/8] = { /* Sprite data */ };
const u8 skeleton_shoot[3][16*32/8] = { /* Sprite data */ };
const u8 ghoul_idle[2][16*32/8] = { /* Sprite data */ };
const u8 ghoul_jump[3][16*32/8] = { /* Sprite data */ };
const u8 imp_fly[4][16*16/8] = { /* Sprite data */ };

const u8* enemy_animations[] = {
    zombie_idle[0], zombie_walk[0], skeleton_idle[0], skeleton_shoot[0],
    ghoul_idle[0], ghoul_jump[0], imp_fly[0]
};

const u8 enemy_animation_frames[] = {2, 4, 1, 3, 2, 3, 4};
const u8 enemy_animation_speeds[] = {10, 8, 0, 6, 10, 0, 6};

void enemy_init(void) {
    for (u8 i = 0; i < 10; i++) {
        enemies[i].active = 0;
    }
    
    for (u8 i = 0; i < level1_spawn_points_count; i++) {
        if (level1_spawn_points[i].type != 0) { // 0 = player
            enemy_create(level1_spawn_points[i].x, level1_spawn_points[i].y, level1_spawn_points[i].type - 1);
        }
    }
}

void enemy_create(u8 x, u8 y, EnemyType type) {
    for (u8 i = 0; i < 10; i++) {
        if (!enemies[i].active) {
            enemies[i].x = x;
            enemies[i].y = y;
            enemies[i].type = type;
            enemies[i].health = type == ENEMY_GHOUL || type == ENEMY_IMP ? 2 : 1;
            enemies[i].active = 1;
            enemies[i].current_animation = type * 2;
            enemies[i].current_frame = 0;
            enemies[i].frame_counter = 0;
            enemies[i].facing_left = 1;
            
            if (type == ENEMY_ZOMBIE) {
                enemies[i].width = 16;
                enemies[i].height = 32;
                enemies[i].vx = -1;
            } else if (type == ENEMY_SKELETON) {
                enemies[i].width = 16;
                enemies[i].height = 32;
                enemies[i].vx = 0;
            } else if (type == ENEMY_GHOUL) {
                enemies[i].width = 16;
                enemies[i].height = 32;
                enemies[i].vx = -1;
                enemies[i].vy = -4;
            } else if (type == ENEMY_IMP) {
                enemies[i].width = 16;
                enemies[i].height = 16;
                enemies[i].vx = -2;
            }
            return;
        }
    }
}

void enemy_update(void) {
    for (u8 i = 0; i < 10; i++) {
        if (enemies[i].active) {
            if (enemies[i].type == ENEMY_ZOMBIE) {
                enemies[i].vx = enemies[i].facing_left ? -1 : 1;
                
                if (collision_check_tile(enemies[i].x + enemies[i].vx, enemies[i].y, enemies[i].width, enemies[i].height, 1)) {
                    enemies[i].facing_left = !enemies[i].facing_left;
                }
                
                enemies[i].x += enemies[i].vx;
                
                enemies[i].frame_counter++;
                if (enemies[i].frame_counter >= enemy_animation_speeds[enemies[i].current_animation]) {
                    enemies[i].frame_counter = 0;
                    enemies[i].current_frame++;
                    if (enemies[i].current_frame >= enemy_animation_frames[enemies[i].current_animation]) {
                        enemies[i].current_frame = 0;
                    }
                }
            } else if (enemies[i].type == ENEMY_SKELETON) {
                enemies[i].frame_counter++;
                if (enemies[i].frame_counter >= 60) {
                    enemies[i].frame_counter = 0;
                    enemies[i].current_animation = 3;
                    enemies[i].current_frame = 0;
                    projectile_create(enemies[i].x, enemies[i].y + 12, enemies[i].facing_left ? -3 : 3, 0, 1);
                }
            } else if (enemies[i].type == ENEMY_GHOUL) {
                enemies[i].vy += 1;
                if (enemies[i].vy > 4) enemies[i].vy = 4;
                
                if (collision_check_tile(enemies[i].x, enemies[i].y + enemies[i].vy, enemies[i].width, enemies[i].height, 1)) {
                    enemies[i].vy = 0;
                }
                
                enemies[i].x += enemies[i].vx;
                enemies[i].y += enemies[i].vy;
                
                enemies[i].frame_counter++;
                if (enemies[i].frame_counter >= enemy_animation_speeds[enemies[i].current_animation]) {
                    enemies[i].frame_counter = 0;
                    enemies[i].current_frame++;
                    if (enemies[i].current_frame >= enemy_animation_frames[enemies[i].current_animation]) {
                        enemies[i].current_frame = 0;
                    }
                }
            } else if (enemies[i].type == ENEMY_IMP) {
                enemies[i].x += enemies[i].vx;
                
                if (enemies[i].x < 0 || enemies[i].x > 160) {
                    enemies[i].active = 0;
                }
                
                enemies[i].frame_counter++;
                if (enemies[i].frame_counter >= 30) {
                    enemies[i].frame_counter = 0;
                    projectile_create(enemies[i].x, enemies[i].y + 4, enemies[i].facing_left ? -3 : 3, 0, 1);
                }
            }
        }
    }
}

void enemy_draw(void) {
    for (u8 i = 0; i < 10; i++) {
        if (enemies[i].active) {
            u8 animation_index = enemies[i].type * 2 + (enemies[i].current_animation % 2);
            const u8* sprite = enemy_animations[animation_index] + (enemies[i].current_frame * (enemies[i].width * enemies[i].height / 8));
            cpct_drawSpriteMaskedAlignedTable(sprite, cpct_getScreenPtr(CPCT_VMEM_START, enemies[i].x, enemies[i].y), enemies[i].width, enemies[i].height, collision_mask_table);
        }
    }
}

void enemy_hurt(u8 index, u8 damage) {
    if (index < 10 && enemies[index].active) {
        enemies[index].health -= damage;
        if (enemies[index].health <= 0) {
            enemies[index].active = 0;
        }
    }
}