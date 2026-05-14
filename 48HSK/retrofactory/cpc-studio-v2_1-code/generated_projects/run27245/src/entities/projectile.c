#include "projectile.h"
#include "../systems/collision.h"
#include "../assets/sprite_player_weapons.h"
#include "../data/sprites/iteenemyprojectiles.h"

#define MAX_PROJECTILES 8

typedef struct {
    u8 active;
    ProjectileType type;
    u8 x, y;
    i8 vx, vy;
    u8 lifetime;
} Projectile;

static Projectile projectiles[MAX_PROJECTILES];

void projectile_spawn(u8 x, u8 y, u8 facing_left, ProjectileType type) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) {
            projectiles[i].active = 1;
            projectiles[i].type = type;
            projectiles[i].x = x;
            projectiles[i].y = y;
            projectiles[i].vx = facing_left ? -3 : 3;
            projectiles[i].vy = 0;
            projectiles[i].lifetime = 60;
            return;
        }
    }
}

void projectile_update(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) continue;
        
        projectiles[i].x += projectiles[i].vx;
        projectiles[i].y += projectiles[i].vy;
        projectiles[i].lifetime--;
        
        if (projectiles[i].lifetime == 0 || projectiles[i].x < 0 || projectiles[i].x > 160) {
            projectiles[i].active = 0;
        }
    }
}

void projectile_render(void) {
    for (u8 i = 0; i < MAX_PROJECTILES; i++) {
        if (!projectiles[i].active) continue;
        
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectiles[i].x, projectiles[i].y);
        const u8* sprite = projectiles[i].type == PROJECTILE_TYPE_PLAYER ? sprite_player_weapon_sword : sprite_enemy_projectile_arrow;
        cpct_drawSpriteMasked(sprite, pvmem, 8, 8);
    }
}