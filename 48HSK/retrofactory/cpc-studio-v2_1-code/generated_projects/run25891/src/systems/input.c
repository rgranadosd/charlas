#include "input.h"
#include <cpctelera.h>

Input input;

cpct_keyID key_left = Key_O;
cpct_keyID key_right = Key_P;
cpct_keyID key_up = Key_Q;
cpct_keyID key_down = Key_A;
cpct_keyID key_fire1 = Key_Space;
cpct_keyID key_fire2 = Key_Enter;

cpct_keyID joy_left = Joy0_Left;
cpct_keyID joy_right = Joy0_Right;
cpct_keyID joy_up = Joy0_Up;
cpct_keyID joy_down = Joy0_Down;
cpct_keyID joy_fire1 = Joy0_Fire1;
cpct_keyID joy_fire2 = Joy0_Fire2;

void input_init(void) {
    input.left_pressed = 0;
    input.right_pressed = 0;
    input.up_pressed = 0;
    input.down_pressed = 0;
    input.fire1_pressed = 0;
    input.fire2_pressed = 0;
    input.left_held = 0;
    input.right_held = 0;
    input.up_held = 0;
    input.down_held = 0;
    input.fire1_held = 0;
    input.fire2_held = 0;
}

void input_update(void) {
    cpct_scanKeyboard_f();
    cpct_scanJoystick(0);
    
    u8 left = cpct_isKeyPressed(key_left) || cpct_isJoystickPressed(joy_left);
    u8 right = cpct_isKeyPressed(key_right) || cpct_isJoystickPressed(joy_right);
    u8 up = cpct_isKeyPressed(key_up) || cpct_isJoystickPressed(joy_up);
    u8 down = cpct_isKeyPressed(key_down) || cpct_isJoystickPressed(joy_down);
    u8 fire1 = cpct_isKeyPressed(key_fire1) || cpct_isJoystickPressed(joy_fire1);
    u8 fire2 = cpct_isKeyPressed(key_fire2) || cpct_isJoystickPressed(joy_fire2);
    
    input.left_pressed = left && !input.left_held;
    input.right_pressed = right && !input.right_held;
    input.up_pressed = up && !input.up_held;
    input.down_pressed = down && !input.down_held;
    input.fire1_pressed = fire1 && !input.fire1_held;
    input.fire2_pressed = fire2 && !input.fire2_held;
    
    input.left_held = left;
    input.right_held = right;
    input.up_held = up;
    input.down_held = down;
    input.fire1_held = fire1;
    input.fire2_held = fire2;
}