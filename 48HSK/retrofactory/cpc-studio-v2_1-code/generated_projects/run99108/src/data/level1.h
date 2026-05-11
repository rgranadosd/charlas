#ifndef _LEVEL1_H_
#define _LEVEL1_H_

#include <types.h>

extern const u8 level1_tilemap[];
extern const u8 level1_tilemap_width;
extern const u8 level1_tilemap_height;
extern u8* const level1_collision_map;

extern const u8 tilemap_tiles[];
extern const u8 player_sprite[];
extern const u8 player_sprite_mask[];
extern const u8 enemy_sprites[][24*24/8];
extern const u8 enemy_masks[][24*24/8];
extern const u8 projectile_sprites[][16*16/8];
extern const u8 hud_heart_full[];
extern const u8 hud_life_icon[];
extern const u8 hud_weapon_icons[][8];

#endif