#include "enemy.h"
#include "../systems/collision.h"
#include "../systems/animation.h"
#include "../data/level1.h"

#define ZOMBIE_WIDTH  16
#define ZOMBIE_HEIGHT 24
#define ARCHER_WIDTH  16
#define ARCHER_HEIGHT 24
#define HOUND_WIDTH   24
#define HOUND_HEIGHT  16

static const u8* zombie_sprites[] = {
    (u8*)0x0400, (u8*)0x0440,
    (u8*)0x0480
};

static const u8* archer_sprites[] = {
    (u8*)0x0500, (u8*)0x0540,
    (u8*)0x0580
};

static const u8* hound_sprites[] = {
    (u8*)0x0600, (u8*)0x0640, (u8*)0x0680
};

void enemy_init(TEnemy* enemy, u8 type, i16 x, i16 y) {
    enemy->x = x;
    enemy->y = y;
    enemy->vx = 0;
    enemy->vy = 0;
    enemy->type = type;
    enemy->state = ENEMY_STATE_WALKING;
    enemy->frame = 0;
    enemy->health = 1;
    enemy->direction = ENEMY_DIR_LEFT;
    
    switch (type) {
        case ENEMY_TYPE_ZOMBIE:
            enemy->width = ZOMBIE_WIDTH;
            enemy->height = ZOMBIE_HEIGHT;
            enemy->vx = -1;
            break;
        case ENEMY_TYPE_ARCHER:
            enemy->width = ARCHER_WIDTH;
            enemy->height = ARCHER_HEIGHT;
            break;
        case ENEMY_TYPE_HOUND:
            enemy->width = HOUND_WIDTH;
            enemy->height = HOUND_HEIGHT;
            enemy->vx = -2;
            break;
    }
}

void enemy_update(TEnemy* enemy, TPlayer* player) {
    if (enemy->health <= 0) {
        enemy->state = ENEMY_STATE_DYING;
    }
    
    switch (enemy->type) {
        case ENEMY_TYPE_ZOMBIE:
            if (enemy->state == ENEMY_STATE_WALKING) {
                enemy->x += enemy->vx;
                if (enemy->x < 0 || enemy->x > 160 - enemy->width) {
                    enemy->vx = -enemy->vx;
                    enemy->direction = (enemy->vx > 0) ? ENEMY_DIR_RIGHT : ENEMY_DIR_LEFT;
                }
            }
            break;
        case ENEMY_TYPE_ARCHER:
            if (enemy->state == ENEMY_STATE_WALKING && cpct_rand() % 100 < 2) {
                enemy->state = ENEMY_STATE_ATTACKING;
                enemy->frame = 0;
            }
            break;
        case ENEMY_TYPE_HOUND:
            if (enemy->state == ENEMY_STATE_WALKING) {
                enemy->x += enemy->vx;
                if (enemy->x < 0 || enemy->x > 160 - enemy->width) {
                    enemy->vx = -enemy->vx;
                    enemy->direction = (enemy->vx > 0) ? ENEMY_DIR_RIGHT : ENEMY_DIR_LEFT;
                }
            }
            break;
    }
    
    animation_update_enemy(enemy);
}

void enemy_draw(TEnemy* enemy) {
    const u8* sprite = NULL;
    u8 width = 0, height = 0;
    
    switch (enemy->type) {
        case ENEMY_TYPE_ZOMBIE:
            sprite = zombie_sprites[enemy->state * 2 + enemy->frame];
            width = ZOMBIE_WIDTH;
            height = ZOMBIE_HEIGHT;
            break;
        case ENEMY_TYPE_ARCHER:
            sprite = archer_sprites[enemy->state * 2 + enemy->frame];
            width = ARCHER_WIDTH;
            height = ARCHER_HEIGHT;
            break;
        case ENEMY_TYPE_HOUND:
            sprite = hound_sprites[enemy->state * 2 + enemy->frame];
            width = HOUND_WIDTH;
            height = HOUND_HEIGHT;
            break;
    }
    
    if (sprite) {
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
        if (enemy->direction == ENEMY_DIR_LEFT) {
            cpct_drawSpriteMaskedAlignedTable(sprite, pvmem, width, height, g_mask_table);
        } else {
            cpct_drawSpriteMasked(sprite, pvmem, width, height);
        }
    }
}

void enemy_hit(TEnemy* enemy, u8 damage) {
    enemy->health -= damage;
    if (enemy->health <= 0) {
        enemy->state = ENEMY_STATE_DYING;
        enemy->frame = 0;
    }
}

void enemy_update_all(TEnemy* enemies, u8* count) {
    for (u8 i = 0; i < *count; i++) {
        if (enemies[i].health > 0) {
            enemy_update(&enemies[i], NULL);
        } else if (enemies[i].state == ENEMY_STATE_DYING) {
            if (enemies[i].frame >= 2) {
                for (u8 j = i; j < *count - 1; j++) {
                    enemies[j] = enemies[j + 1];
                }
                (*count)--;
                i--;
            }
        }
    }
}

void enemy_draw_all(TEnemy* enemies, u8 count) {
    for (u8 i = 0; i < count; i++) {
        enemy_draw(&enemies[i]);
    }
}

void enemy_spawn_update(void) {
    static u8 spawn_timer = 0;
    
    if (spawn_timer > 0) {
        spawn_timer--;
        return;
    }
    
    if (cpct_rand() % 100 < 5) {
        extern TEnemy enemies[MAX_ENEMIES];
        extern u8 enemy_count;
        
        if (enemy_count < MAX_ENEMIES) {
            u8 type = cpct_rand() % 3;
            i16 x = (cpct_rand() % 2) ? 0 : 160;
            i16 y = 180;
            
            enemy_init(&enemies[enemy_count], type, x, y);
            enemy_count++;
            spawn_timer = 60;
        }
    }
}