#include "tilemap.h"
#include "../data/level1.h"

#define TILEMAP_WIDTH  40
#define TILEMAP_HEIGHT 50
#define TILE_SIZE      4

static u8 tilemap[TILEMAP_HEIGHT][TILEMAP_WIDTH];
static u8 collision_map[TILEMAP_HEIGHT][TILEMAP_WIDTH];

static const u8* tileset = (u8*)0x0800;

void tilemap_init(void) {
    for (u8 y = 0; y < TILEMAP_HEIGHT; y++) {
        for (u8 x = 0; x < TILEMAP_WIDTH; x++) {
            tilemap[y][x] = level1_tilemap[y * TILEMAP_WIDTH + x];
            collision_map[y][x] = level1_collision[y * TILEMAP_WIDTH + x];
        }
    }
}

u8 tilemap_get_collision(u8 x, u8 y) {
    if (x >= TILEMAP_WIDTH || y >= TILEMAP_HEIGHT) return 1;
    return collision_map[y][x];
}

void tilemap_draw(void) {
    u8* pvmem = CPCT_VMEM_START;
    for (u8 y = 0; y < 25; y++) {
        for (u8 x = 0; x < 40; x++) {
            cpct_drawTileAligned2x4_f(tilemap[y] + x, pvmem, TILEMAP_WIDTH, TILE_SIZE, tileset);
            pvmem += 2;
        }
    }
}