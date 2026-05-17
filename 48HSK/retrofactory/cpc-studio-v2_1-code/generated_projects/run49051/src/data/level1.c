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
    23, 20, 14, 12, 11, 10, 0, 6, 21, 18, 30, 22, 7, 26, 28, 31
};
