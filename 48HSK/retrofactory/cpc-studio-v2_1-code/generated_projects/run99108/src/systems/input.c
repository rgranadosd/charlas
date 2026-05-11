#include "input.h"
#include <cpctelera.h>

Input input;

u8 jump_debounce = 0;
u8 shoot_debounce = 0;

void input_init(void) {
    input.left_pressed = 0;
    input.right_pressed = 0;
    input.jump_pressed = 0;
    input.shoot_pressed = 0;
    input.weapon_change_pressed = 0;
}

void input_update(void) {
    cpct_scanKeyboard_f();
    
    input.left_pressed = cpct_isKeyPressed(Key_CursorLeft);
    input.right_pressed = cpct_isKeyPressed(Key_CursorRight);
    
    if (jump_debounce > 0) jump_debounce--;
    if (shoot_debounce > 0) shoot_debounce--;
    
    if (cpct_isKeyPressed(Key_CursorUp) && jump_debounce == 0) {
        input.jump_pressed = 1;
        jump_debounce = 2;
    } else {
        input.jump_pressed = 0;
    }
    
    if (cpct_isKeyPressed(Key_Space) && shoot_debounce == 0) {
        input.shoot_pressed = 1;
        shoot_debounce = 3;
    } else {
        input.shoot_pressed = 0;
    }
    
    input.weapon_change_pressed = cpct_isKeyPressed(Key_Control);
}