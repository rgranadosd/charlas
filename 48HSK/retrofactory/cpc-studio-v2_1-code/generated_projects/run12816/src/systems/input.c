#include "systems/input.h"

static u8 ginputleft;
static u8 ginputright;
static u8 ginputjump;
static u8 ginputshoot;
static u8 gprevjump;
static u8 gprevshoot;

void input_update(void) {
    gprevjump = ginputjump;
    gprevshoot = ginputshoot;
    cpct_scanKeyboard_f();
    ginputleft = cpct_isKeyPressed(Key_CursorLeft);
    ginputright = cpct_isKeyPressed(Key_CursorRight);
    ginputjump = cpct_isKeyPressed(Key_CursorUp);
    ginputshoot = cpct_isKeyPressed(Key_CursorDown);
}

u8 input_is_left_pressed(void) {
    return ginputleft;
}

u8 input_is_right_pressed(void) {
    return ginputright;
}

u8 input_is_jump_pressed(void) {
    return ginputjump;
}

u8 input_is_jump_just_pressed(void) {
    return (u8)(ginputjump && !gprevjump);
}

u8 input_is_shoot_pressed(void) {
    return ginputshoot;
}

u8 input_is_shoot_just_pressed(void) {
    return (u8)(ginputshoot && !gprevshoot);
}
