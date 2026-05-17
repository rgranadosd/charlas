#include "data/level1.h"

const u16 level1tilemapwidth = 20;
const u16 level1tilemapheight = 18;

const u8 level1tilemap[] = {
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1
};

const u8 level1tileproperties[] = { 0, 1 };

const u8 gpalette[GPALETTE_SIZE] = {
    0, 1, 2, 3, 6, 7, 9, 10, 11, 12, 13, 15, 16, 18, 24, 26
};
