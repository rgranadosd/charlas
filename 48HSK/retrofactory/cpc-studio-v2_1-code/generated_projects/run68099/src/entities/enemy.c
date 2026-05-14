#include "enemy.h"
#include "../systems/collision.h"

extern void hud_add_score(u16 points);

extern Enemy enemies[];
extern u8 enemy_count;

void enemy_init(Enemy *enemy, u8 type, u8 x, u8 y) {
    enemy->x = x;
    enemy->y = y;
    enemy->type = type;
    enemy->animation_state = 0;
    enemy->animation_frame = 0;
    
    switch (type) {
        case ENEMY_ZOMBIE:
            enemy->width = 16;
            enemy->height = 24;
            enemy->health = 1;
            enemy->speed_x = -1;
            break;
        default:
            enemy->width = 16;
            enemy->height = 24;
            enemy->health = 1;
            enemy->speed_x = -1;
            break;
    }
}

void enemy_update(Enemy *enemy) {
    enemy->x += enemy->speed_x;
    
    if (enemy->x < 0 || enemy->x > 160) {
        enemy->health = 0;
    }
    
    if (collision_check_tile(enemy->x, enemy->y + 1, enemy->width, enemy->height, 1) == 0) {
        enemy->y += 1;
    }
}

void enemy_render(Enemy *enemy) {
    u8 *pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
    cpct_drawSolidBox(pvmem, 0xC0, enemy->width, enemy->height);
}

void enemy_damage(Enemy *enemy, u8 damage) {
    enemy->health -= damage;
    if (enemy->health <= 0) {
        for (u8 i = 0; i < enemy_count; i++) {
            if (&enemies[i] == enemy) {
                for (u8 j = i; j < enemy_count - 1; j++) {
                    enemies[j] = enemies[j + 1];
                }
                enemy_count--;
                hud_add_score(100);
                break;
            }
        }
    }
}