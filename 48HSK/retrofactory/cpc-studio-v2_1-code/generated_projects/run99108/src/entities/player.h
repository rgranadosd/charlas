#ifndef _PLAYER_H_
#define _PLAYER_H_

#include <types.h>

typedef struct {
    u8 x, y;
    u8 width, height;
    i8 vx, vy;
    u8 health;
    u8 lives;
    u8 invulnerability_frames;
    u8 current_weapon;
    u8 state;
    u8 frame;
    u8 facing_left;
} Player;

extern Player player;

enum PlayerState {
    PLAYER_IDLE,
    PLAYER_RUNNING,
    PLAYER_JUMPING,
    PLAYER_CROUCHING,
    PLAYER_SHOOTING,
    PLAYER_DAMAGED
};

enum WeaponType {
    WEAPON_LANCE,
    WEAPON_DAGGER,
    WEAPON_FIREBALL
};

void player_init(void);
void player_update(void);
void player_render(void);
void player_shoot(void);
void player_take_damage(void);

#endif