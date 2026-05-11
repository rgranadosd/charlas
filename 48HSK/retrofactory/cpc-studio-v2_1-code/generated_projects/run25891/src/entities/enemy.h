#ifndef _ENEMY_H_
#define _ENEMY_H_

#include <cpctelera.h>

typedef enum { ENEMY_ZOMBIE, ENEMY_SKELETON, ENEMY_GHOUL, ENEMY_IMP } EnemyType;

typedef struct {
    u8 x, y;
    u8 width, height;
    i8 vx, vy;
    u8 health;
    u8 type;
    u8 current_animation;
    u8 current_frame;
    u8 frame_counter;
    u8 active;
    u8 facing_left;
} Enemy;

extern Enemy enemies[10];

extern const u8* enemy_animations[];

extern const u8 enemy_animation_frames[];

extern const u8 enemy_animation_speeds[];

void enemy_init(void);
void enemy_update(void);
void enemy_draw(void);
void enemy_create(u8 x, u8 y, EnemyType type);
void enemy_hurt(u8 index, u8 damage);

#endif