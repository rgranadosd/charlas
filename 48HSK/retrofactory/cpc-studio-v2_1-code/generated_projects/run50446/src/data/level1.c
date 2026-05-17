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
    20, 4, 21, 28, 12, 5, 22, 6, 23, 30, 0, 14, 7, 18, 10, 11
};
