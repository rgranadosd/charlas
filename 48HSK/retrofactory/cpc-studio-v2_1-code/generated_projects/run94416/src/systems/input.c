#include "systems/input.h"

static u8 ginputleft;
static u8 ginputright;
static u8 ginputup;
static u8 ginputdown;
static u8 ginputshoot;
static u8 gprevjump;
static u8 gprevshoot;

void input_update(void) {
    gprevjump = ginputup;
    gprevshoot = ginputshoot;
    cpct_scanKeyboard_f();
    ginputleft = (u8)(cpct_isKeyPressed(Key_CursorLeft) || cpct_isKeyPressed(Key_A));
    ginputright = (u8)(cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_D));
    ginputup = (u8)(cpct_isKeyPressed(Key_CursorUp) || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Key_Z));
    ginputdown = (u8)(cpct_isKeyPressed(Key_CursorDown) || cpct_isKeyPressed(Key_S) || cpct_isKeyPressed(Key_X));
    ginputshoot = (u8)(cpct_isKeyPressed(Key_Space) || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Key_CursorDown));
}

u8 input_is_left_pressed(void) {
    return ginputleft;
}

u8 input_is_right_pressed(void) {
    return ginputright;
}

u8 input_is_up_pressed(void) {
    return ginputup;
}

u8 input_is_down_pressed(void) {
    return ginputdown;
}

u8 input_is_jump_pressed(void) {
    return ginputup;
}

u8 input_is_jump_just_pressed(void) {
    return (u8)(ginputup && !gprevjump);
}

u8 input_is_shoot_pressed(void) {
    return ginputshoot;
}

u8 input_is_shoot_just_pressed(void) {
    return (u8)(ginputshoot && !gprevshoot);
}
