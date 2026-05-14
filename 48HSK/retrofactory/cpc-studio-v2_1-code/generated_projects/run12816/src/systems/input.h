#ifndef SYSTEMS_INPUT_H
#define SYSTEMS_INPUT_H

#include <cpctelera.h>

void input_update(void);
u8 input_is_left_pressed(void);
u8 input_is_right_pressed(void);
u8 input_is_jump_pressed(void);
u8 input_is_jump_just_pressed(void);
u8 input_is_shoot_pressed(void);
u8 input_is_shoot_just_pressed(void);

#endif
