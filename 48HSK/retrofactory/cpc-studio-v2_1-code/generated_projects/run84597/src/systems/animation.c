#include "animation.h"

void animation_update_player(TPlayer* player) {
    player->frame++;
    
    switch (player->state) {
        case PLAYER_STATE_IDLE:
            if (player->frame >= 2) player->frame = 0;
            break;
        case PLAYER_STATE_RUNNING:
            if (player->frame >= 4) player->frame = 0;
            break;
        case PLAYER_STATE_JUMPING:
            if (player->frame >= 3) player->frame = 2;
            break;
        case PLAYER_STATE_ATTACKING:
            if (player->frame >= 3) {
                player->state = PLAYER_STATE_IDLE;
                player->frame = 0;
            }
            break;
        case PLAYER_STATE_HIT:
            if (player->frame >= 2) {
                player->state = PLAYER_STATE_IDLE;
                player->frame = 0;
            }
            break;
    }
}

void animation_update_enemy(TEnemy* enemy) {
    enemy->frame++;
    
    switch (enemy->state) {
        case ENEMY_STATE_WALKING:
            if (enemy->type == ENEMY_TYPE_ZOMBIE && enemy->frame >= 2) enemy->frame = 0;
            if (enemy->type == ENEMY_TYPE_HOUND && enemy->frame >= 3) enemy->frame = 0;
            break;
        case ENEMY_STATE_ATTACKING:
            if (enemy->frame >= 2) {
                enemy->state = ENEMY_STATE_WALKING;
                enemy->frame = 0;
            }
            break;
        case ENEMY_STATE_DYING:
            if (enemy->frame >= 2) enemy->frame = 2;
            break;
    }
}