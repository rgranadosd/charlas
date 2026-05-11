#include "input.h"

static u8 input_buffer[2] = {0};
static u8 buffer_index = 0;

void input_init(void) {
    cpct_scanKeyboard_f();
}

void input_update(void) {
    cpct_scanKeyboard_f();
    
    input_buffer[buffer_index] = 0;
    
    if (cpct_isKeyPressed(Key_CursorLeft)) input_buffer[buffer_index] |= 0x01;
    if (cpct_isKeyPressed(Key_CursorRight)) input_buffer[buffer_index] |= 0x02;
    if (cpct_isKeyPressed(Key_Space)) input_buffer[buffer_index] |= 0x04;
    if (cpct_isKeyPressed(Key_Alt)) input_buffer[buffer_index] |= 0x08;
    
    buffer_index = (buffer_index + 1) % 2;
}

u8 input_left_pressed(void) {
    return (input_buffer[0] & 0x01) || (input_buffer[1] & 0x01);
}

u8 input_right_pressed(void) {
    return (input_buffer[0] & 0x02) || (input_buffer[1] & 0x02);
}

u8 input_jump_pressed(void) {
    return (input_buffer[0] & 0x04) && !(input_buffer[1] & 0x04);
}

u8 input_attack_pressed(void) {
    return (input_buffer[0] & 0x08) && !(input_buffer[1] & 0x08);
}