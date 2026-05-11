#ifndef _INPUT_H_
#define _INPUT_H_

#include <types.h>

typedef struct {
    u8 left_pressed;
    u8 right_pressed;
    u8 jump_pressed;
    u8 shoot_pressed;
    u8 weapon_change_pressed;
} Input;

extern Input input;

void input_init(void);
void input_update(void);

#endif