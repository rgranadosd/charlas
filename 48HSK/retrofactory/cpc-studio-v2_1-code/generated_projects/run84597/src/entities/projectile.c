#include "projectile.h"
#include "../systems/collision.h"

#define LANCE_WIDTH  8
#define LANCE_HEIGHT 4
#define ARROW_WIDTH  8
#define ARROW_HEIGHT 2

static const u8* lance_sprite = (u8*)0x0700;
static const u8* arrow_sprite = (u8*)0x0720;

void projectile_init(TProjectile* projectile, u8 type, i16 x, i16 y, i16 vx, i16 vy) {
    projectile->x = x;
    projectile->y = y;
    projectile->vx = vx;
    projectile->vy = vy;
    projectile->type = type;
    projectile->lifetime = 60;
    projectile->active = 1;
    
    switch (type) {
        case PROJECTILE_TYPE_LANCE:
            projectile->width = LANCE_WIDTH;
            projectile->height = LANCE_HEIGHT;
            break;
        case PROJECTILE_TYPE_ARROW:
            projectile->width = ARROW_WIDTH;
            projectile->height = ARROW_HEIGHT;
            break;
    }
}

void projectile_update(TProjectile* projectile) {
    if (!projectile->active) return;
    
    projectile->x += projectile->vx;
    projectile->y += projectile->vy;
    projectile->lifetime--;
    
    if (projectile->lifetime <= 0 || 
        projectile->x < 0 || projectile->x > 160 - projectile->width ||
        projectile->y < 0 || projectile->y > 200 - projectile->height ||
        collision_check_tile(projectile->x, projectile->y, projectile->width, projectile->height)) {
        projectile->active = 0;
    }
}

void projectile_draw(TProjectile* projectile) {
    if (!projectile->active) return;
    
    const u8* sprite = NULL;
    u8 width = 0, height = 0;
    
    switch (projectile->type) {
        case PROJECTILE_TYPE_LANCE:
            sprite = lance_sprite;
            width = LANCE_WIDTH;
            height = LANCE_HEIGHT;
            break;
        case PROJECTILE_TYPE_ARROW:
            sprite = arrow_sprite;
            width = ARROW_WIDTH;
            height = ARROW_HEIGHT;
            break;
    }
    
    if (sprite) {
        u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
        cpct_drawSpriteMasked(sprite, pvmem, width, height);
    }
}

void projectile_update_all(TProjectile* projectiles, u8* count) {
    for (u8 i = 0; i < *count; i++) {
        if (projectiles[i].active) {
            projectile_update(&projectiles[i]);
        } else {
            for (u8 j = i; j < *count - 1; j++) {
                projectiles[j] = projectiles[j + 1];
            }
            (*count)--;
            i--;
        }
    }
}

void projectile_draw_all(TProjectile* projectiles, u8 count) {
    for (u8 i = 0; i < count; i++) {
        projectile_draw(&projectiles[i]);
    }
}