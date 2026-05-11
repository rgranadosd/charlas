#include "player.h"
#include "../systems/input.h"
#include "../systems/collision.h"
#include "../systems/animation.h"
#include "../data/level1.h"

#define PLAYER_WIDTH  16
#define PLAYER_HEIGHT 24
#define PLAYER_SPEED  2
#define PLAYER_JUMP   -5
#define GRAVITY       0.5
#define MAX_FALL      4

static const u8* player_sprites[] = {
    (u8*)0x0000, (u8*)0x0040,
    (u8*)0x0080, (u8*)0x00C0, (u8*)0x0100, (u8*)0x0140,
    (u8*)0x0180, (u8*)0x01C0, (u8*)0x0200,
    (u8*)0x0240, (u8*)0x0280, (u8*)0x02C0
};

void player_init(TPlayer* player) {
    player->x = 20;
    player->y = 180;
    player->vx = 0;
    player->vy = 0;
    player->width = PLAYER_WIDTH;
    player->height = PLAYER_HEIGHT;
    player->state = PLAYER_STATE_IDLE;
    player->frame = 0;
    player->health = 3;
    player->invulnerability = 0;
    player->direction = PLAYER_DIR_RIGHT;
    player->attack_cooldown = 0;
}

void player_update(TPlayer* player) {
    if (player->invulnerability > 0) {
        player->invulnerability--;
    }
    
    if (player->attack_cooldown > 0) {
        player->attack_cooldown--;
    }
    
    if (input_left_pressed() && !input_right_pressed()) {
        player->vx = -PLAYER_SPEED;
        player->direction = PLAYER_DIR_LEFT;
        player->state = PLAYER_STATE_RUNNING;
    } else if (input_right_pressed() && !input_left_pressed()) {
        player->vx = PLAYER_SPEED;
        player->direction = PLAYER_DIR_RIGHT;
        player->state = PLAYER_STATE_RUNNING;
    } else {
        player->vx = 0;
        if (player->state != PLAYER_STATE_JUMPING && player->state != PLAYER_STATE_ATTACKING) {
            player->state = PLAYER_STATE_IDLE;
        }
    }
    
    if (input_jump_pressed() && player->vy == 0 && player->state != PLAYER_STATE_JUMPING) {
        player->vy = PLAYER_JUMP;
        player->state = PLAYER_STATE_JUMPING;
    }
    
    player->vy += GRAVITY;
    if (player->vy > MAX_FALL) {
        player->vy = MAX_FALL;
    }
    
    if (input_attack_pressed() && player->attack_cooldown == 0 && player->state != PLAYER_STATE_ATTACKING) {
        player->state = PLAYER_STATE_ATTACKING;
        player->frame = 0;
        player->attack_cooldown = 20;
    }
    
    i16 new_x = player->x + player->vx;
    i16 new_y = player->y + player->vy;
    
    if (!collision_check_tile(new_x, player->y, player->width, player->height)) {
        player->x = new_x;
    }
    
    if (!collision_check_tile(player->x, new_y, player->width, player->height)) {
        player->y = new_y;
    } else if (player->vy > 0) {
        player->vy = 0;
        if (player->state == PLAYER_STATE_JUMPING) {
            player->state = PLAYER_STATE_IDLE;
        }
    }
    
    animation_update_player(player);
}

void player_draw(TPlayer* player) {
    const u8* sprite = player_sprites[player->state * 3 + player->frame];
    u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
    
    if (player->direction == PLAYER_DIR_LEFT) {
        cpct_drawSpriteMaskedAlignedTable(sprite, pvmem, PLAYER_WIDTH, PLAYER_HEIGHT, g_mask_table);
    } else {
        cpct_drawSpriteMasked(sprite, pvmem, PLAYER_WIDTH, PLAYER_HEIGHT);
    }
}

void player_hit(TPlayer* player, u8 damage) {
    if (player->invulnerability == 0) {
        player->health -= damage;
        player->invulnerability = 30;
        player->state = PLAYER_STATE_HIT;
        player->frame = 0;
    }
}