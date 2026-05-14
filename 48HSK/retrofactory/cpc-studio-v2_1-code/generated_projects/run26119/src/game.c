#include "game.h"
#include <cpctelera.h>
#include "systems/tilemap.h"
#include "systems/input.h"
#include "systems/collision.h"
#include "entities/player.h"
#include "entities/enemy.h"
#include "entities/projectile.h"
#include "systems/hud.h"

#define MAX_ENEMIES 6
#define MAX_PROJECTILES 6
#define TOTAL_WAVES 3

static Player g_player;
static Enemy g_enemies[MAX_ENEMIES];
static Projectile g_projectiles[MAX_PROJECTILES];

static u8 g_lives;
static u16 g_score;
static u8 g_timeleft;
static u8 g_weaponlevel;
static u8 g_weapondisplay;
static u8 g_currentwave;
static u8 g_aliveenemies;
static u8 g_wavecooldown;
static u8 g_damagecooldown;
static u8 g_shootcooldown;
static u8 g_victory;
static u8 g_gameover;
static u16 g_framecounter;
static u8 g_checkpointx;
static u8 g_checkpointy;
static u8 g_checkpointactive;
static u8 g_hiddenrewardtaken;
static Enemy g_boss;
static u8 g_bossactive;
static u8 g_bossphase;

static void reset_player_to_checkpoint(void) {
    g_player.x = g_checkpointx;
    g_player.y = g_checkpointy;
    g_player.vx = 0;
    g_player.vy = 0;
}

static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
    if (ax + aw <= bx) return 0;
    if (bx + bw <= ax) return 0;
    if (ay + ah <= by) return 0;
    if (by + bh <= ay) return 0;
    return 1;
}

static void spawn_wave(u8 wave) {
    u8 i;
    u8 count;

    for (i = 0; i < MAX_ENEMIES; ++i) {
        enemyinit(&g_enemies[i]);
    }

    if (wave == 0) count = 2;
    else if (wave == 1) count = 3;
    else count = 4;

    if (count > MAX_ENEMIES) count = MAX_ENEMIES;

    for (i = 0; i < count; ++i) {
        u8 type;
        if (wave == 0) type = 0;
        else if (wave == 1) type = (u8)(i & 1);
        else type = (u8)((i == 0) ? 2 : (i & 1));
        enemyspawn(&g_enemies[i], (u8)(48 + (i * 10)), 112, type, (u8)((i & 1) ? 1 : 0));
    }

    g_aliveenemies = count;
}

static void spawn_boss(void) {
    enemyinit(&g_boss);
    enemyspawn(&g_boss, 64, 88, 1, 0);
    g_boss.w = 8;
    g_boss.h = 20;
    g_boss.health = 8;
    g_boss.reward = 1200;
    g_boss.kind = 3;
    g_bossactive = 1;
    g_bossphase = 0;
}

static void try_fire_projectile(void) {
    u8 i;
    i8 dir;

    if (!input_is_shoot_just_pressed()) return;
    if (g_shootcooldown) return;

    dir = g_player.facing_left ? -3 : 3;

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        if (!g_projectiles[i].active) {
            projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel);
            g_shootcooldown = 10;
            break;
        }
    }
}

void game_init(void) {
    u8 i;

    cpct_disableFirmware();
    cpct_setVideoMode(1);
    cpct_clearScreen(0x00);
    tilemap_init();
    collision_init();
    playerinit(&g_player);
    hudinit();

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        projectileinit(&g_projectiles[i]);
    }

    g_lives = 3;
    g_score = 0;
    g_timeleft = 99;
    g_weaponlevel = 0;
    g_weapondisplay = 0;
    g_currentwave = 0;
    g_wavecooldown = 1;
    g_damagecooldown = 0;
    g_shootcooldown = 0;
    g_victory = 0;
    g_gameover = 0;
    g_framecounter = 0;
    g_checkpointx = 20;
    g_checkpointy = 120;
    g_checkpointactive = 0;
    g_hiddenrewardtaken = 0;
    g_bossactive = 0;
    enemyinit(&g_boss);
}

void game_update(void) {
    u8 i;
    u8 j;

    input_update();

    if (g_gameover || g_victory) {
        return;
    }

    playerupdate(&g_player);
    try_fire_projectile();

    if (g_shootcooldown) g_shootcooldown--;
    if (g_damagecooldown) g_damagecooldown--;

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        projectileupdate(&g_projectiles[i]);
    }

    for (i = 0; i < MAX_ENEMIES; ++i) {
        enemyupdate(&g_enemies[i]);
    }

    if (g_bossactive) {
        if (g_boss.health > 4) g_bossphase = 0;
        else g_bossphase = 1;

        g_boss.vx = (i8)(g_player.x < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
        enemyupdate(&g_boss);
    }

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        if (!g_projectiles[i].active) continue;
        for (j = 0; j < MAX_ENEMIES; ++j) {
            if (!g_enemies[j].active) continue;
            if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
                             (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
            if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
                g_score = (u16)(g_score + g_enemies[j].reward);
                if (g_aliveenemies) g_aliveenemies--;
            }
            g_projectiles[i].active = 0;
            break;
        }

        if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
            g_projectiles[i].active = 0;
            if (enemydamage(&g_boss, g_projectiles[i].damage)) {
                g_bossactive = 0;
                g_score = (u16)(g_score + g_boss.reward);
                g_victory = 1;
            }
        }
    }

    if (!g_damagecooldown) {
        for (i = 0; i < MAX_ENEMIES; ++i) {
            if (!g_enemies[i].active) continue;
            if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
                             (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
                if (g_lives) g_lives--;
                g_damagecooldown = 40;
                break;
            }
        }

        if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
            if (g_lives) g_lives--;
            g_damagecooldown = 40;
        }

        if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
            if (g_lives) g_lives--;
            g_damagecooldown = 40;
        }
    }

    if (g_lives == 0) {
        if (g_checkpointactive) {
            g_lives = 2;
            reset_player_to_checkpoint();
            g_damagecooldown = 50;
        } else {
            g_gameover = 1;
        }
    }

    if (!g_checkpointactive && g_player.x >= 44) {
        g_checkpointactive = 1;
        g_checkpointx = 44;
        g_checkpointy = 120;
    }

    if (!g_hiddenrewardtaken && tilemap_is_hidden_zone((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
        g_hiddenrewardtaken = 1;
        if (g_lives < 5) g_lives++;
        if (g_weaponlevel < 2) g_weaponlevel++;
        g_score = (u16)(g_score + 250);
    }

    if (g_score >= 800 && g_weaponlevel < 1) g_weaponlevel = 1;
    if (g_score >= 1600 && g_weaponlevel < 2) g_weaponlevel = 2;
    g_weapondisplay = (u8)(g_weaponlevel + 1);

    if (g_aliveenemies == 0 && !g_gameover) {
        if (g_currentwave < TOTAL_WAVES) {
            if (g_wavecooldown == 0) {
                spawn_wave(g_currentwave);
                g_currentwave++;
                g_wavecooldown = 100;
            } else {
                g_wavecooldown--;
            }
        } else if (!g_bossactive && g_player.x >= tilemap_goal_x()) {
            spawn_boss();
        }
    }

    g_framecounter++;
    if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
        g_timeleft--;
    }
    if (g_timeleft == 0 && !g_victory) {
        g_gameover = 1;
    }

    hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
}

void game_render(void) {
    u8 i;

    cpct_clearScreen(0x00);
    tilemap_render();

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        projectilerender(&g_projectiles[i]);
    }

    for (i = 0; i < MAX_ENEMIES; ++i) {
        enemyrender(&g_enemies[i]);
    }

    if (g_bossactive) {
        enemyrender(&g_boss);
    }

    playerrender(&g_player);
    hudrender();

    if (g_victory) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
    } else if (g_gameover) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
    } else if (g_checkpointactive) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 44, 150), 0x3A, 2, 10);
    }
}
