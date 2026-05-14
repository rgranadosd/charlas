#include "projectile.h"
#include "../systems/collision.h"

extern Projectile projectiles[];
extern u8 projectile_count;
extern Enemy enemies[];
extern u8 enemy_count;

extern void enemy_damage(Enemy *enemy, u8 damage);

extern void hud_add_score(u16 points);

void projectile_init(Projectile *projectile, u8 type, u8 x, u8 y, i8 speed_x, i8 speed_y) {
    projectile->x = x;
    projectile->y = y;
    projectile->speed_x = speed_x;
    projectile->speed_y = speed_y;
    projectile->type = type;
    projectile->lifetime = 60;
    
    switch (type) {
        case PROJECTILE_LANCE:
            projectile->width = 16;
            projectile->height = 8;
            projectile->damage = 1;
            break;
        default:
            projectile->width = 8;
            projectile->height = 8;
            projectile->damage = 1;
            break;
    }
}

void projectile_update(Projectile *projectile) {
    projectile->x += projectile->speed_x;
    projectile->y += projectile->speed_y;
    projectile->lifetime--;
    
    if (projectile->lifetime == 0 || projectile->x < 0 || projectile->x > 160) {
        projectile_destroy(projectile);
        return;
    }
    
    for (u8 i = 0; i < enemy_count; i++) {
        if (projectile->x < enemies[i].x + enemies[i].width &&
            projectile->x + projectile->width > enemies[i].x &&
            projectile->y < enemies[i].y + enemies[i].height &&
            projectile->y + projectile->height > enemies[i].y) {
            enemy_damage(&enemies[i], projectile->damage);
            projectile_destroy(projectile);
            return;
        }
    }
}

void projectile_render(Projectile *projectile) {
    u8 *pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
    cpct_drawSolidBox(pvmem, 0xFF, projectile->width, projectile->height);
}

void projectile_destroy(Projectile *projectile) {
    for (u8 i = 0; i < projectile_count; i++) {
        if (&projectiles[i] == projectile) {
            for (u8 j = i; j < projectile_count - 1; j++) {
                projectiles[j] = projectiles[j + 1];
            }
            projectile_count--;
            break;
        }
    }
}