#include "game.h"
#include <cpctelera.h>
#include "systems/tilemap.h"
#include "systems/input.h"
#include "systems/collision.h"
#include "entities/player.h"
#include "entities/enemy.h"
#include "entities/projectile.h"
#include "systems/hud.h"
#include "data/level1.h"

/* ENTRY STUB: game.c is linked first (alphabetically before main.c),
 * so the very first bytes at 0x4000 are this JP.
 * DISC.BAS always calls CALL 16384 and this redirects to the real entry. */
void __game_entry_jp(void) __naked {
    __asm
        .globl cpc_run_address
        jp cpc_run_address
    __endasm;
}

#define MAX_ENEMIES 6
#define MAX_PROJECTILES 6
#define TOTAL_WAVES 3

static Player g_player;
static Enemy g_enemies[MAX_ENEMIES];
static Projectile g_projectiles[MAX_PROJECTILES];

/* Previous-frame positions for erase-redraw (no full-screen clear) */
static u8 prev_player_x = 4, prev_player_y = 104;
static u8 prev_enemy_x[MAX_ENEMIES], prev_enemy_y[MAX_ENEMIES];
static u8 prev_enemy_w[MAX_ENEMIES], prev_enemy_h[MAX_ENEMIES];
static u8 prev_enemy_act[MAX_ENEMIES];
static u8 prev_boss_x, prev_boss_y, prev_boss_act;
static u8 prev_proj_x[MAX_PROJECTILES], prev_proj_y[MAX_PROJECTILES];
static u8 prev_proj_w[MAX_PROJECTILES], prev_proj_h[MAX_PROJECTILES];
static u8 prev_proj_act[MAX_PROJECTILES];

static u8 g_lives;
static u16 g_score;
static u8 g_timeleft;
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
static Enemy g_boss;
static u8 g_bossactive;
static u8 g_bossphase;
static u8 g_weaponlevel;
static u8 g_pickuptaken;

/* Runtime diagnostics for movement pipeline (input -> movement -> possible reset). */
static u8 g_dbg_left;
static u8 g_dbg_right;
static u8 g_dbg_jump;
static u8 g_dbg_shoot;
static u8 g_dbg_move_raw;
static u8 g_dbg_move_net;
static u8 g_dbg_move_cancelled;
static u8 g_dbg_hit;
static i8 g_dbg_vx;

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
        u8 spawn_y;
        u8 spawn_x;
        if (wave == 0) type = 0;
        else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
        else type = (u8)((i == 0 || i == 3) ? 2 : 1);

        spawn_y = (type == 2) ? 84 : 112;
        /* spawn alejado del player (x=4..12), bien visible en pantalla */
        spawn_x = (u8)(36 + (i * 16));
        if (spawn_x > 68) spawn_x = 68;
        enemyspawn(&g_enemies[i], spawn_x, spawn_y, type, (u8)((i & 1) ? 1 : 0));
    }

    g_aliveenemies = count;
}

static void spawn_boss(void) {
    enemyinit(&g_boss);
    enemyspawn(&g_boss, 68, 112, 1, 0);
    g_boss.w = 10;
    g_boss.h = 18;
    g_boss.health = 10;
    g_boss.reward = 255; /* u8 max; score adds separately on kill */
    g_boss.kind = 3;
    g_boss.vx = -1;
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
            /* weapon_upgrade_active: pickup permanente que mejora el disparo */
            projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
            g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
            break;
        }
    }
}

static void register_player_hit(void) {
    if (g_lives) {
        g_lives--;
    }
    if (g_lives == 0) {
        g_gameover = 1;
        return;
    }

    reset_player_to_checkpoint();
    g_damagecooldown = 40;
}

void game_init(void) {
    u8 i;

    cpct_setVideoMode(0);
    cpct_disableFirmware();
    cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
    cpct_setBorder(gpalette[0]);
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
    g_weapondisplay = 1;
    g_currentwave = 0;
    g_wavecooldown = 1;
    g_damagecooldown = 100;
    g_shootcooldown = 0;
    g_victory = 0;
    g_gameover = 0;
    g_framecounter = 0;
    g_checkpointx = 12;
    g_checkpointy = 104;
    g_checkpointactive = 0;
    g_bossactive = 0;
    g_weaponlevel = 0;
    g_pickuptaken = 0;
    g_dbg_left = 0;
    g_dbg_right = 0;
    g_dbg_jump = 0;
    g_dbg_shoot = 0;
    g_dbg_move_raw = 0;
    g_dbg_move_net = 0;
    g_dbg_move_cancelled = 0;
    g_dbg_hit = 0;
    g_dbg_vx = 0;
    enemyinit(&g_boss);
}

void game_update(void) {
    u8 i;
    u8 j;
    u8 left_pressed;
    u8 right_pressed;
    u8 jump_pressed;
    u8 shoot_pressed;
    u8 player_x_start;
    u8 player_x_after_move;
    u8 lives_before_damage;

    input_update();

    left_pressed = input_is_left_pressed();
    right_pressed = input_is_right_pressed();
    jump_pressed = input_is_jump_pressed();
    shoot_pressed = input_is_shoot_pressed();

    g_dbg_left = left_pressed;
    g_dbg_right = right_pressed;
    g_dbg_jump = jump_pressed;
    g_dbg_shoot = shoot_pressed;

    /* Border colors by action so "input detected" is not confused with movement. */
    if (left_pressed && !right_pressed) {
        cpct_setBorder(gpalette[2]);
    } else if (right_pressed && !left_pressed) {
        cpct_setBorder(gpalette[14]);
    } else if (jump_pressed) {
        cpct_setBorder(gpalette[3]);
    } else if (shoot_pressed) {
        cpct_setBorder(gpalette[6]);
    } else {
        cpct_setBorder(gpalette[0]);
    }

    if (g_gameover || g_victory) {
        g_dbg_move_raw = 0;
        g_dbg_move_net = 0;
        g_dbg_move_cancelled = 0;
        g_dbg_hit = 0;
        g_dbg_vx = g_player.vx;
        hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
        return;
    }

    player_x_start = g_player.x;
    playerupdate(&g_player);
    player_x_after_move = g_player.x;
    g_dbg_vx = g_player.vx;
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

        g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
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

    lives_before_damage = g_lives;
    if (!g_damagecooldown) {
        for (i = 0; i < MAX_ENEMIES; ++i) {
            if (!g_enemies[i].active) continue;
            if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
                             (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
                register_player_hit();
                break;
            }
        }

        if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
            register_player_hit();
        }

        if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
            register_player_hit();
        }
    }

    g_dbg_move_raw = (u8)(player_x_after_move != player_x_start);
    g_dbg_move_net = (u8)(g_player.x != player_x_start);
    g_dbg_move_cancelled = (u8)(g_dbg_move_raw && !g_dbg_move_net);
    g_dbg_hit = (u8)(g_lives < lives_before_damage);

    if (!g_checkpointactive && g_player.x >= 44) {
        g_checkpointactive = 1;
        g_checkpointx = 52;
        g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
    }

    if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
        g_pickuptaken = 1;
        g_weaponlevel = 1;
        g_score = (u16)(g_score + 100);
    }

    g_weapondisplay = (u8)(g_weaponlevel + 1);

    if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
        if (g_currentwave < TOTAL_WAVES) {
            if (g_wavecooldown == 0) {
                spawn_wave(g_currentwave);
                g_currentwave++;
                g_wavecooldown = 90;
            } else {
                g_wavecooldown--;
            }
        } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
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
    u8* pvmem;
    i16 vx_mark_x;

    /* --- ERASE sprites at previous positions (sky = 0x00) --- */
    /* Player */
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_player_x, prev_player_y);
    cpct_drawSolidBox(pvmem, 0x00, g_player.w, g_player.h);

    /* Enemies */
    for (i = 0; i < MAX_ENEMIES; ++i) {
        if (prev_enemy_act[i]) {
            pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_enemy_x[i], prev_enemy_y[i]);
            cpct_drawSolidBox(pvmem, 0x00, prev_enemy_w[i], prev_enemy_h[i]);
        }
    }

    /* Boss */
    if (prev_boss_act) {
        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_boss_x, prev_boss_y);
        cpct_drawSolidBox(pvmem, 0x00, g_boss.w, g_boss.h);
    }

    /* Projectiles */
    for (i = 0; i < MAX_PROJECTILES; ++i) {
        if (prev_proj_act[i]) {
            pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_proj_x[i], prev_proj_y[i]);
            cpct_drawSolidBox(pvmem, 0x00, prev_proj_w[i], prev_proj_h[i]);
        }
    }

    /* Restore static background (cheap: ~5 drawSolidBox calls) */
    tilemap_render();

    /* --- DRAW sprites at current positions --- */
    /* Player drawn FIRST: beam still above y=104 at this point (~4ms elapsed, beam at ~y=40) */
    playerrender(&g_player);

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        projectilerender(&g_projectiles[i]);
    }

    for (i = 0; i < MAX_ENEMIES; ++i) {
        enemyrender(&g_enemies[i]);
    }

    if (g_bossactive) {
        enemyrender(&g_boss);
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(1, 1), 32, 2);
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
    }

    if (!g_pickuptaken) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
    }

    hudrender();

    if (g_victory) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(5, 5), 24, 8);
    } else if (g_gameover) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(6, 6), 24, 8);
    } else if (g_checkpointactive) {
        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
    }

     /* Movement diagnostic bar: shows player X even if sprite motion is hard to perceive. */
    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 0, 0), cpct_px2byteM0(0, 0), 40, 2);
    cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_player.x, 0), cpct_px2byteM0(6, 6), 4, 2);

     /* Deep diagnostics row (y=2):
         L,R,J,S,MoveRaw,MoveNet,CancelledByReset,HitThisFrame. */
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 0, 2), cpct_px2byteM0(0, 0), 40, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  0, 2), g_dbg_left           ? cpct_px2byteM0(2, 2)   : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  4, 2), g_dbg_right          ? cpct_px2byteM0(14, 14) : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  8, 2), g_dbg_jump           ? cpct_px2byteM0(3, 3)   : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 12, 2), g_dbg_shoot          ? cpct_px2byteM0(6, 6)   : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 16, 2), g_dbg_move_raw       ? cpct_px2byteM0(7, 7)   : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 20, 2), g_dbg_move_net       ? cpct_px2byteM0(9, 9)   : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 2), g_dbg_move_cancelled ? cpct_px2byteM0(12, 12) : cpct_px2byteM0(0, 0), 4, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 2), g_dbg_hit            ? cpct_px2byteM0(15, 15) : cpct_px2byteM0(0, 0), 4, 2);

     /* Velocity marker (y=4): center at x=20, moves with vx sign and magnitude. */
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 0, 4), cpct_px2byteM0(0, 0), 40, 2);
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 20, 4), cpct_px2byteM0(5, 5), 1, 2);
     vx_mark_x = (i16)20 + ((i16)g_dbg_vx * 2);
     if (vx_mark_x < 0) vx_mark_x = 0;
     if (vx_mark_x > 39) vx_mark_x = 39;
     cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, (u8)vx_mark_x, 4), cpct_px2byteM0(10, 10), 1, 2);

    /* --- SAVE current positions for next frame erase --- */
    prev_player_x = g_player.x;
    prev_player_y = g_player.y;

    for (i = 0; i < MAX_ENEMIES; ++i) {
        prev_enemy_act[i] = g_enemies[i].active;
        prev_enemy_x[i]   = g_enemies[i].x;
        prev_enemy_y[i]   = g_enemies[i].y;
        prev_enemy_w[i]   = g_enemies[i].w;
        prev_enemy_h[i]   = g_enemies[i].h;
    }

    prev_boss_act = g_bossactive;
    prev_boss_x   = g_boss.x;
    prev_boss_y   = g_boss.y;

    for (i = 0; i < MAX_PROJECTILES; ++i) {
        prev_proj_act[i] = g_projectiles[i].active;
        prev_proj_x[i]   = g_projectiles[i].x;
        prev_proj_y[i]   = g_projectiles[i].y;
        prev_proj_w[i]   = g_projectiles[i].w;
        prev_proj_h[i]   = g_projectiles[i].h;
    }
}
