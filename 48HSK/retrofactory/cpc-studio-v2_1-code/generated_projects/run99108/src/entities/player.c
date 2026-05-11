#include "player.h"
#include "projectile.h"
#include "../systems/input.h"
#include "../systems/collision.h"
#include <cpctelera.h>

Player player;

extern u8* const level1_collision_map;

extern const u8 level1_tilemap_width;

extern const u8 level1_tilemap_height;

void player_init(void) {
    player.x = 20;
    player.y = 184;
    player.width = 24;
    player.height = 32;
    player.vx = 0;
    player.vy = 0;
    player.health = 3;
    player.lives = 3;
    player.invulnerability_frames = 0;
    player.current_weapon = WEAPON_LANCE;
    player.state = PLAYER_IDLE;
    player.frame = 0;
    player.facing_left = 0;
}

void player_update(void) {
    if (player.invulnerability_frames > 0) {
        player.invulnerability_frames--;
    }
    
    player.vx = 0;
    
    if (input.left_pressed) {
        player.vx = -2;
        player.facing_left = 1;
    } else if (input.right_pressed) {
        player.vx = 2;
        player.facing_left = 0;
    }
    
    if (input.jump_pressed && !player.vy) {
        player.vy = -4;
        player.state = PLAYER_JUMPING;
    }
    
    if (input.shoot_pressed) {
        player_shoot();
    }
    
    player.vy += 1;
    if (player.vy > 4) player.vy = 4;
    
    u8 new_x = player.x + player.vx;
    u8 new_y = player.y + player.vy;
    
    if (collision_check_player_tilemap(new_x, player.y, player.width, player.height)) {
        player.vx = 0;
    } else {
        player.x = new_x;
    }
    
    if (collision_check_player_tilemap(player.x, new_y, player.width, player.height)) {
        if (player.vy > 0) {
            player.vy = 0;
            player.state = PLAYER_IDLE;
        }
    } else {
        player.y = new_y;
    }
    
    if (player.vx != 0 && player.state != PLAYER_JUMPING) {
        player.state = PLAYER_RUNNING;
    } else if (player.vx == 0 && player.state != PLAYER_JUMPING) {
        player.state = PLAYER_IDLE;
    }
}

void player_shoot(void) {
    if (player.state != PLAYER_SHOOTING) {
        player.state = PLAYER_SHOOTING;
        projectile_create(player.x + (player.facing_left ? -8 : 16), player.y + 12, 
                         player.facing_left ? -4 : 4, 0, player.current_weapon);
    }
}

void player_take_damage(void) {
    if (player.invulnerability_frames == 0) {
        player.health--;
        player.invulnerability_frames = 50;
        if (player.health == 0) {
            player.lives--;
            player.health = 3;
            if (player.lives == 0) {
                // Game over
            } else {
                player.x = 20;
                player.y = 184;
            }
        }
    }
}

void player_render(void) {
    u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player.x, player.y);
    cpct_drawSpriteMaskedAlignedTable(player_sprite, pvmem, player.width, player.height, player_sprite_mask);
}