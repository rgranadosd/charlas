#ifndef _INPUT_H_
#define _INPUT_H_

#include <cpctelera.h>

void input_init(void);
void input_update(void);
u8 input_left_pressed(void);
u8 input_right_pressed(void);
u8 input_jump_pressed(void);
u8 input_attack_pressed(void);

#endif