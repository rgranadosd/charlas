#include "player.h"
#include "../systems/input.h"
#include "../systems/collision.h"
#include <cpctelera.h>

Player player;

const u8 player_idle[2][16*32/8] = { /* Sprite data */ };
const u8 player_run[4][16*32/8] = { /* Sprite data */ };
const u8 player_jump[3][16*32/8] = { /* Sprite data */ };
const u8 player_crouch[2][16*32/8] = { /* Sprite data */ };
const u8 player_attack_melee[3][16*32/8] = { /* Sprite data */ };
const u8 player_attack_throw[3][16*32/8] = { /* Sprite data */ };
const u8 player_hurt[2][16*32/8] = { /* Sprite data */ };
const u8 player_death[4][16*32/8] = { /* Sprite data */ };

const u8* player_animations[] = {
    player_idle[0], player_run[0], player_jump[0], player_crouch[0],
    player_attack_melee[0], player_attack_throw[0], player_hurt[0], player_death[0]
};

const u8 player_animation_frames[] = {2, 4, 3, 2, 3, 3, 2, 4};
const u8 player_animation_speeds[] = {8, 4, 0, 0, 3, 3, 5, 8};

void player_init(void) {
    player.x = 16;
    player.y = 160;
    player.width = 16;
    player.height = 32;
    player.vx = 0;
    player.vy = 0;
    player.health = 3;
    player.lives = 3;
    player.ammo = 3;
    player.invulnerability_frames = 0;
    player.current_animation = 0;
    player.current_frame = 0;
    player.frame_counter = 0;
    player.facing_left = 0;
    player.is_attacking = 0;
    player.is_jumping = 0;
    player.is_crouching = 0;
}

void player_update(void) {
    if (player.invulnerability_frames > 0) {
        player.invulnerability_frames--;
    }
    
    if (player.is_attacking) {
        player.frame_counter++;
        if (player.frame_counter >= player_animation_speeds[player.current_animation]) {
            player.frame_counter = 0;
            player.current_frame++;
            if (player.current_frame >= player_animation_frames[player.current_animation]) {
                player.current_frame = 0;
                player.is_attacking = 0;
            }
        }
        return;
    }
    
    player.vx = 0;
    
    if (input.left_pressed) {
        player.vx = -2;
        player.facing_left = 1;
        player.current_animation = 1;
    } else if (input.right_pressed) {
        player.vx = 2;
        player.facing_left = 0;
        player.current_animation = 1;
    } else {
        player.current_animation = 0;
    }
    
    if (input.up_pressed && !player.is_jumping) {
        player.vy = -5;
        player.is_jumping = 1;
        player.current_animation = 2;
    }
    
    if (input.down_pressed) {
        player.is_crouching = 1;
        player.current_animation = 3;
    } else {
        player.is_crouching = 0;
    }
    
    if (input.fire1_pressed && !player.is_attacking) {
        player.is_attacking = 1;
        player.current_animation = 4;
        player.current_frame = 0;
        player.frame_counter = 0;
    }
    
    if (input.fire2_pressed && player.ammo > 0 && !player.is_attacking) {
        player.is_attacking = 1;
        player.current_animation = 5;
        player.current_frame = 0;
        player.frame_counter = 0;
        player.ammo--;
        projectile_create(player.x + (player.facing_left ? -8 : 8), player.y + 12, player.facing_left ? -4 : 4, 0, 0);
    }
    
    player.vy += 1;
    if (player.vy > 4) player.vy = 4;
    
    if (collision_check_tile(player.x + player.vx, player.y, player.width, player.height, 1)) {
        player.vx = 0;
    }
    
    if (collision_check_tile(player.x, player.y + player.vy, player.width, player.height, 1)) {
        if (player.vy > 0) {
            player.is_jumping = 0;
        }
        player.vy = 0;
    }
    
    player.x += player.vx;
    player.y += player.vy;
    
    if (player.x < 0) player.x = 0;
    if (player.x > (level1_tilemap_width * 8 - player.width)) player.x = level1_tilemap_width * 8 - player.width;
    
    player.frame_counter++;
    if (player.frame_counter >= player_animation_speeds[player.current_animation]) {
        player.frame_counter = 0;
        player.current_frame++;
        if (player.current_frame >= player_animation_frames[player.current_animation]) {
            player.current_frame = 0;
        }
    }
}

void player_draw(void) {
    const u8* sprite = player_animations[player.current_animation] + (player.current_frame * (16*32/8));
    cpct_drawSpriteMaskedAlignedTable(sprite, cpct_getScreenPtr(CPCT_VMEM_START, player.x, player.y), 16, 32, collision_mask_table);
}

void player_hurt(void) {
    if (player.invulnerability_frames == 0) {
        player.health--;
        player.invulnerability_frames = 30;
        player.current_animation = 6;
        player.current_frame = 0;
        player.frame_counter = 0;
        
        if (player.health == 0) {
            player_die();
        }
    }
}

void player_die(void) {
    player.lives--;
    if (player.lives == 0) {
        // Game over
    } else {
        player_init();
    }
}