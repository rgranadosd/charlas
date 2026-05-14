#include "systems/input.h"

static u8 ginputleft;
static u8 ginputright;
static u8 ginputjump;

void input_update(void) {
    cpct_scanKeyboard_f();
    ginputleft = cpct_isKeyPressed(Key_CursorLeft);
    ginputright = cpct_isKeyPressed(Key_CursorRight);
    ginputjump = cpct_isKeyPressed(Key_CursorUp);
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
