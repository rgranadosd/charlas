#include "data/level1.h"

const u16 level1tilemapwidth = 20;
const u16 level1tilemapheight = 18;

const u8 level1tilemap[] = {
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1
};

const u8 level1tileproperties[] = { 0, 1 };

const u8 gpalette16[16] = {
    0x54, 0x44, 0x55, 0x5C,
    0x58, 0x5D, 0x4C, 0x45,
    0x4D, 0x56, 0x46, 0x57,
    0x5E, 0x40, 0x5F, 0x4E
};
