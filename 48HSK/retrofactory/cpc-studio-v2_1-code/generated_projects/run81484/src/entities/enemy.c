#include "entities/enemy.h"
#include "systems/collision.h"
#include <cpctelera.h>

/* kind0: 4 bytes x 16 rows = robot enemy
 * pen4=BRIGHT_WHITE outline, pen7=CYAN head, pen5=BRIGHT_YELLOW eyes, pen1=BLACK body
 * Byte encoding: cpct_px2byteM0(left_pen, right_pen) */
static const u8 enemy_kind0_sprite[] = {
    0x30, 0x30, 0x30, 0x30,  /* row 0: top border pen4+pen4 */
    0xB8, 0xFC, 0xFC, 0x74,  /* row 1: head pen4|7+7+7+7|4 */
    0xB8, 0xF8, 0xF4, 0x74,  /* row 2: eyes pen4|7+5+5|7|4 */
    0xB8, 0xFC, 0xFC, 0x74,  /* row 3: head */
    0x30, 0xFC, 0xFC, 0x30,  /* row 4: chin pen4|7+7+4 */
    0x90, 0x60, 0x90, 0x60,  /* row 5: shoulders pen4|1+4|1 */
    0x90, 0xC0, 0xC0, 0x60,  /* row 6: body pen4|1+1+1|4 */
    0x90, 0xC0, 0xC0, 0x60,  /* row 7: body */
    0x90, 0xC0, 0xC0, 0x60,  /* row 8: body */
    0x90, 0x90, 0x60, 0x60,  /* row 9: waist pen4|1+4|1+4 */
    0x30, 0x30, 0x30, 0x30,  /* row 10: belt pen4+4 */
    0x90, 0x90, 0x60, 0x60,  /* row 11: hips */
    0x60, 0x60, 0x60, 0x60,  /* row 12: legs pen1|4+1|4 */
    0x60, 0x60, 0x60, 0x60,  /* row 13: legs */
    0x60, 0x30, 0x30, 0x90,  /* row 14: ankles */
    0xC0, 0x30, 0x30, 0xC0,  /* row 15: feet pen1|4+4|1 */
};

/* kind1: 5 bytes x 14 rows = armored enemy
 * pen3=BRIGHT_RED corners, pen4=BRIGHT_WHITE outline, pen7=CYAN head,
 * pen5=BRIGHT_YELLOW eyes, pen1=BLACK body */
static const u8 enemy_kind1_sprite[] = {
    0x64, 0x30, 0x30, 0x30, 0x98,  /* row 0: top pen3|4+4+4|3 */
    0x64, 0xFC, 0xFC, 0xFC, 0x98,  /* row 1: head pen3|7+7+7|3 */
    0x64, 0x70, 0x30, 0x70, 0x98,  /* row 2: eyes pen3|7|5+5|7|3 */
    0x64, 0x30, 0x30, 0x30, 0x98,  /* row 3: head lower */
    0xCC, 0x30, 0x30, 0x30, 0xCC,  /* row 4: chin pen3+4+3 */
    0xC4, 0xC0, 0xCC, 0xC0, 0xC8,  /* row 5: shoulders */
    0xC4, 0xC0, 0xC0, 0xC0, 0xC8,  /* row 6: body */
    0xC4, 0xC0, 0xC0, 0xC0, 0xC8,  /* row 7: body */
    0xC4, 0xC4, 0xC0, 0xC8, 0xC8,  /* row 8: chest detail */
    0xC4, 0xC0, 0xCC, 0xC0, 0xC8,  /* row 9: waist */
    0xCC, 0xCC, 0xCC, 0xCC, 0xCC,  /* row 10: belt pen3+3 */
    0xC4, 0xC4, 0xCC, 0xC8, 0xC8,  /* row 11: hips */
    0xC8, 0xC8, 0xC0, 0xC4, 0xC4,  /* row 12: legs */
    0xC8, 0x98, 0x30, 0x64, 0xC4,  /* row 13: feet */
};

/* kind2: 6 bytes x 10 rows = flying bat enemy
 * pen7=CYAN outline, pen1=BLACK body, pen4=BRIGHT_WHITE wing accents */
static const u8 enemy_kind2_sprite[] = {
    0xFC, 0xFC, 0xFC, 0xFC, 0xFC, 0xFC,  /* row 0: top border pen7+7 */
    0xD4, 0xE8, 0xD4, 0xE8, 0xD4, 0xE8,  /* row 1: body upper pen7|1 */
    0xD4, 0xC0, 0xC0, 0xC0, 0xC0, 0xE8,  /* row 2: body pen7|1+1|7 */
    0xD4, 0x90, 0xC0, 0x60, 0xC0, 0xE8,  /* row 3: eyes pen7|4|1+1|7 */
    0xFC, 0xFC, 0xFC, 0xFC, 0xFC, 0xFC,  /* row 4: mid border */
    0xD4, 0x74, 0xB8, 0x74, 0xB8, 0xE8,  /* row 5: wings pen7|1|7+4|7|1|7 */
    0x90, 0x90, 0x60, 0x90, 0x60, 0x60,  /* row 6: wings spread pen4|1 */
    0x30, 0xC0, 0x30, 0x30, 0xC0, 0x30,  /* row 7: wing tips pen4+1+4 */
    0xFC, 0xD4, 0xFC, 0xFC, 0xE8, 0xFC,  /* row 8: tail pen7 */
    0xFC, 0xFC, 0xC0, 0xC0, 0xFC, 0xFC,  /* row 9: tail end */
};

/* kind3: 10 bytes x 18 rows = BOSS enemy
 * pen14=RED outline, pen1=BLACK body, pen3=BRIGHT_RED details, pen4=BRIGHT_WHITE eyes */
static const u8 enemy_kind3_sprite[] = {
    0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F,  /* row 0: top pen14+14 */
    0x95, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x6A,  /* row 1: body */
    0x95, 0xCC, 0xC0, 0xC0, 0xCC, 0xC8, 0xC4, 0xC0, 0xCC, 0x6A,  /* row 2: shoulder detail pen3 */
    0x95, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x6A,  /* row 3: body */
    0x95, 0x90, 0xC0, 0x60, 0xC0, 0x60, 0xC0, 0xC0, 0x90, 0x6A,  /* row 4: eyes pen4 */
    0x95, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x6A,  /* row 5: body */
    0x3F, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x3F,  /* row 6: face frame */
    0x3F, 0x95, 0xCC, 0xC0, 0xCC, 0xCC, 0xC0, 0xCC, 0x6A, 0x3F,  /* row 7: jaw pen3 teeth */
    0x3F, 0x3F, 0x95, 0xC0, 0x6A, 0x95, 0xC0, 0x6A, 0x3F, 0x3F,  /* row 8: chin */
    0x95, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x6A,  /* row 9: body */
    0x95, 0xC8, 0xC0, 0xC0, 0xC4, 0xC8, 0xC0, 0xC0, 0xC4, 0x6A,  /* row 10: chest detail */
    0x95, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x6A,  /* row 11: body */
    0x95, 0xC0, 0x3F, 0x3F, 0x3F, 0x3F, 0xC0, 0xC0, 0xC0, 0x6A,  /* row 12: arm */
    0x95, 0x6A, 0x3F, 0x3F, 0x3F, 0x3F, 0x95, 0xC0, 0xC0, 0x6A,  /* row 13: arm */
    0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3F,  /* row 14: belt */
    0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x3F,  /* row 15: hips */
    0x6A, 0x6A, 0x6A, 0x6A, 0x6A, 0x95, 0x95, 0x95, 0x95, 0x95,  /* row 16: legs */
    0xC0, 0x3F, 0xC0, 0x3F, 0xC0, 0xC0, 0x3F, 0xC0, 0x3F, 0xC0,  /* row 17: feet */
};

void enemyinit(Enemy* enemy) {
    if (!enemy) {
        return;
    }

    enemy->x = 0;
    enemy->y = 0;
    enemy->vx = 0;
    enemy->vy = 0;
    enemy->w = 4;
    enemy->h = 16;
    enemy->active = 0;
    enemy->health = 1;
    enemy->reward = 100;
    enemy->kind = 0;
}

void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
    if (!enemy) {
        return;
    }

    enemy->x = x;
    enemy->y = y;
    enemy->vx = move_right ? 1 : -1;
    enemy->vy = 0;
    enemy->active = 1;
    enemy->kind = kind;

    if (kind == 1) {
        enemy->w = 5;
        enemy->h = 14;
        enemy->health = 2;
        enemy->reward = 180;
        enemy->vx = move_right ? 2 : -2;
    } else if (kind == 2) {
        enemy->w = 6;
        enemy->h = 10;
        enemy->health = 1;
        enemy->reward = 150;
        enemy->vy = move_right ? 1 : -1;
        enemy->vx = 1;
    } else if (kind == 3) {
        enemy->w = 10;
        enemy->h = 18;
        enemy->health = 8;
        enemy->reward = 800;
        enemy->vx = move_right ? 1 : -1;
    } else {
        enemy->w = 4;
        enemy->h = 16;
        enemy->health = 1;
        enemy->reward = 100;
    }
}

void enemyupdate(Enemy* enemy) {
    i16 nextx;
    i16 nexty;

    if (!enemy || !enemy->active) {
        return;
    }

    if (enemy->kind == 2) {
        nextx = (i16)enemy->x + (i16)enemy->vx;
        nexty = (i16)enemy->y + (i16)enemy->vy;

        if (nextx < 8 || nextx > 72) {
            enemy->vx = (i8)(-enemy->vx);
            nextx = (i16)enemy->x + (i16)enemy->vx;
        }
        if (nexty < 56 || nexty > 120) {
            enemy->vy = (i8)(-enemy->vy);
            nexty = (i16)enemy->y + (i16)enemy->vy;
        }

        enemy->x = (u8)nextx;
        enemy->y = (u8)nexty;
        return;
    }

    nextx = (i16)enemy->x + (i16)enemy->vx;
    if (nextx < 2) {
        nextx = 2;
        enemy->vx = 1;
    }
    {
        i16 maxx = (i16)(80 - (i16)enemy->w);
        if (nextx > maxx) {
            nextx = maxx;
            enemy->vx = -1;
        }
    }
    enemy->x = (u8)nextx;

    enemy->vy = (i8)(enemy->vy + 1);
    if (enemy->vy > 3) enemy->vy = 3;
    nexty = (i16)enemy->y + (i16)enemy->vy;
    nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
    enemy->y = (u8)nexty;
    if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
        enemy->vy = 0;
    }
}

void enemyrender(const Enemy* enemy) {
    u8* pvmem;
    const u8* sprite;

    if (!enemy || !enemy->active) {
        return;
    }

    if (enemy->kind == 3) sprite = enemy_kind3_sprite;
    else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
    else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
    else sprite = enemy_kind0_sprite;

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
    cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
}

u8 enemydamage(Enemy* enemy, u8 damage) {
    if (!enemy || !enemy->active) {
        return 0;
    }

    if (damage >= enemy->health) {
        enemy->health = 0;
        enemy->active = 0;
        return 1;
    }

    enemy->health = (u8)(enemy->health - damage);
    return 0;
}
