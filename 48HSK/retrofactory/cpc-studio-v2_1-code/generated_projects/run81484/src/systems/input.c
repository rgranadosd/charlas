#include "systems/input.h"

static u8 ginputleft;
static u8 ginputright;
static u8 ginputup;
static u8 ginputdown;
static u8 ginputjump;
static u8 ginputshoot;
static u8 gprevjump;
static u8 gprevshoot;

void input_update(void) {
    gprevjump = ginputjump;
    gprevshoot = ginputshoot;
    cpct_scanKeyboard();
    /* Robust mapping for emulator and real CPC:
       - Movement: Cursor keys, QAOP/WASD variants and Joy0 directions.
       - Jump: Space/Z/X or Joy0 fire1.
       - Shoot: Control/Return/CursorDown or Joy0 fire2/fire3. */
    ginputleft  = (u8)(cpct_isKeyPressed(Key_CursorLeft)  || cpct_isKeyPressed(Key_O) || cpct_isKeyPressed(Key_A) || cpct_isKeyPressed(Joy0_Left));
    ginputright = (u8)(cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_P) || cpct_isKeyPressed(Key_D) || cpct_isKeyPressed(Joy0_Right));
    ginputup    = (u8)(cpct_isKeyPressed(Key_CursorUp)    || cpct_isKeyPressed(Key_Q) || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Joy0_Up));
    ginputdown  = (u8)(cpct_isKeyPressed(Key_CursorDown)  || cpct_isKeyPressed(Key_S) || cpct_isKeyPressed(Joy0_Down));
    ginputjump  = (u8)(cpct_isKeyPressed(Key_Space) || cpct_isKeyPressed(Key_Z) || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Joy0_Fire1));
    ginputshoot = (u8)(cpct_isKeyPressed(Key_Control) || cpct_isKeyPressed(Key_Return) || cpct_isKeyPressed(Key_CursorDown) || cpct_isKeyPressed(Joy0_Fire2) || cpct_isKeyPressed(Joy0_Fire3));
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
