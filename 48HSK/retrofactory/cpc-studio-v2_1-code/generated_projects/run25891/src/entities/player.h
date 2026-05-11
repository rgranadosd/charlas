#ifndef _PLAYER_H_
#define _PLAYER_H_

#include <cpctelera.h>

typedef struct {
    u8 x, y;
    u8 width, height;
    i8 vx, vy;
    u8 health;
    u8 lives;
    u8 ammo;
    u8 invulnerability_frames;
    u8 current_animation;
    u8 current_frame;
    u8 frame_counter;
    u8 facing_left;
    u8 is_attacking;
    u8 is_jumping;
    u8 is_crouching;
} Player;

extern Player player;

extern const u8* player_animations[];

extern const u8 player_animation_frames[];

extern const u8 player_animation_speeds[];

void player_init(void);
void player_update(void);
void player_draw(void);
void player_hurt(void);
void player_die(void);

#endif