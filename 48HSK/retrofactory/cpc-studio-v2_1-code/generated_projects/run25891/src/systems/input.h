#ifndef _INPUT_H_
#define _INPUT_H_

#include <cpctelera.h>

typedef struct {
    u8 left_pressed;
    u8 right_pressed;
    u8 up_pressed;
    u8 down_pressed;
    u8 fire1_pressed;
    u8 fire2_pressed;
    u8 left_held;
    u8 right_held;
    u8 up_held;
    u8 down_held;
    u8 fire1_held;
    u8 fire2_held;
} Input;

extern Input input;

extern cpct_keyID key_left, key_right, key_up, key_down, key_fire1, key_fire2;

extern cpct_keyID joy_left, joy_right, joy_up, joy_down, joy_fire1, joy_fire2;

void input_init(void);
void input_update(void);

#endif