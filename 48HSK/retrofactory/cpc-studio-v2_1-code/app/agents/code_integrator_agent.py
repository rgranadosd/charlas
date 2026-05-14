import json
import re
from pathlib import PurePosixPath

from app.services.c_codegen_service import (
    detect_c_generation_issues,
    render_c_array_decl,
    render_c_const_array,
    render_c_function_decl,
    render_c_function_def,
    render_c_include,
)
from app.services.contract_validation_service import normalize_asset_token
from app.services.llm_service import json_call

MAIN_C_PATH = "src/main.c"
GAME_H_PATH = "src/game.h"
GAME_C_PATH = "src/game.c"
HUD_H_PATH = "src/systems/hud.h"
HUD_C_PATH = "src/systems/hud.c"
PLAYER_H_PATH = "src/entities/player.h"
ENEMY_H_PATH = "src/entities/enemy.h"
ENEMY_C_PATH = "src/entities/enemy.c"
PROJECTILE_H_PATH = "src/entities/projectile.h"
PROJECTILE_C_PATH = "src/entities/projectile.c"
LEVEL1_H_PATH = "src/data/level1.h"
LEVEL1_C_PATH = "src/data/level1.c"
TILESET_BASE_H_PATH = "src/data/tileset/base.h"
TILESET_BASE_C_PATH = "src/data/tileset/base.c"
PLAYERKNIGHT_H_PATH = "src/data/sprites/playerknight.h"
PLAYERKNIGHT_C_PATH = "src/data/sprites/playerknight.c"
HEALTHBAR_H_PATH = "src/data/hud/healthbar.h"
HEALTHBAR_C_PATH = "src/data/hud/healthbar.c"
INPUT_H_PATH = "src/systems/input.h"
INPUT_C_PATH = "src/systems/input.c"
COLLISION_H_PATH = "src/systems/collision.h"
COLLISION_C_PATH = "src/systems/collision.c"
TILEMAP_H_PATH = "src/systems/tilemap.h"
TILEMAP_C_PATH = "src/systems/tilemap.c"
PLAYER_C_PATH = "src/entities/player.c"

PLAYABLE_RUNTIME_PROFILES = {"playable_slice", "vertical_slice"}

MANDATORY_RUNTIME_MODULES = {
    PLAYER_C_PATH,
    INPUT_C_PATH,
    COLLISION_C_PATH,
    TILEMAP_C_PATH,
}


def _build_game_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef GAME_H",
            "#define GAME_H",
            "",
            "void game_init(void);",
            "void game_update(void);",
            "void game_render(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_game_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("game.h"),
            render_c_include("<cpctelera.h>"),
            render_c_include("systems/tilemap.h"),
            render_c_include("systems/input.h"),
            render_c_include("systems/collision.h"),
            render_c_include("entities/player.h"),
            render_c_include("entities/enemy.h"),
            render_c_include("entities/projectile.h"),
            render_c_include("systems/hud.h"),
            "",
            "#define MAX_ENEMIES 6",
            "#define MAX_PROJECTILES 6",
            "#define TOTAL_WAVES 3",
            "",
            "static Player g_player;",
            "static Enemy g_enemies[MAX_ENEMIES];",
            "static Projectile g_projectiles[MAX_PROJECTILES];",
            "",
            "static u8 g_lives;",
            "static u16 g_score;",
            "static u8 g_timeleft;",
            "static u8 g_weapondisplay;",
            "static u8 g_currentwave;",
            "static u8 g_aliveenemies;",
            "static u8 g_wavecooldown;",
            "static u8 g_damagecooldown;",
            "static u8 g_shootcooldown;",
            "static u8 g_victory;",
            "static u8 g_gameover;",
            "static u16 g_framecounter;",
            "static u8 g_checkpointx;",
            "static u8 g_checkpointy;",
            "static u8 g_checkpointactive;",
            "static Enemy g_boss;",
            "static u8 g_bossactive;",
            "static u8 g_bossphase;",
            "static u8 g_weaponlevel;",
            "static u8 g_pickuptaken;",
            "",
            "static void reset_player_to_checkpoint(void) {",
            "    g_player.x = g_checkpointx;",
            "    g_player.y = g_checkpointy;",
            "    g_player.vx = 0;",
            "    g_player.vy = 0;",
            "}",
            "",
            "static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {",
            "    if (ax + aw <= bx) return 0;",
            "    if (bx + bw <= ax) return 0;",
            "    if (ay + ah <= by) return 0;",
            "    if (by + bh <= ay) return 0;",
            "    return 1;",
            "}",
            "",
            "static void spawn_wave(u8 wave) {",
            "    u8 i;",
            "    u8 count;",
            "",
            "    for (i = 0; i < MAX_ENEMIES; ++i) {",
            "        enemyinit(&g_enemies[i]);",
            "    }",
            "",
            "    if (wave == 0) count = 2;",
            "    else if (wave == 1) count = 3;",
            "    else count = 4;",
            "",
            "    if (count > MAX_ENEMIES) count = MAX_ENEMIES;",
            "",
            "    for (i = 0; i < count; ++i) {",
            "        u8 type;",
            "        u8 spawn_y;",
            "        if (wave == 0) type = 0;",
            "        else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);",
            "        else type = (u8)((i == 0 || i == 3) ? 2 : 1);",
            "",
            "        spawn_y = (type == 2) ? 84 : 112;",
            "        enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));",
            "    }",
            "",
            "    g_aliveenemies = count;",
            "}",
            "",
            "static void spawn_boss(void) {",
            "    enemyinit(&g_boss);",
            "    enemyspawn(&g_boss, 68, 112, 1, 0);",
            "    g_boss.w = 10;",
            "    g_boss.h = 18;",
            "    g_boss.health = 10;",
            "    g_boss.reward = 1500;",
            "    g_boss.kind = 3;",
            "    g_boss.vx = -1;",
            "    g_bossactive = 1;",
            "    g_bossphase = 0;",
            "}",
            "",
            "static void try_fire_projectile(void) {",
            "    u8 i;",
            "    i8 dir;",
            "",
            "    if (!input_is_shoot_just_pressed()) return;",
            "    if (g_shootcooldown) return;",
            "",
            "    dir = g_player.facing_left ? -3 : 3;",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        if (!g_projectiles[i].active) {",
            "            /* weapon_upgrade_active: pickup permanente que mejora el disparo */",
            "            projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);",
            "            g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;",
            "            break;",
            "        }",
            "    }",
            "}",
            "",
            "static void register_player_hit(void) {",
            "    if (g_lives) {",
            "        g_lives--;",
            "    }",
            "    if (g_lives == 0) {",
            "        g_gameover = 1;",
            "        return;",
            "    }",
            "",
            "    reset_player_to_checkpoint();",
            "    g_damagecooldown = 40;",
            "}",
            "",
            "void game_init(void) {",
            "    u8 i;",
            "",
            "    cpct_disableFirmware();",
            "    cpct_setVideoMode(1);",
            "    cpct_clearScreen(0x00);",
            "    tilemap_init();",
            "    collision_init();",
            "    playerinit(&g_player);",
            "    hudinit();",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        projectileinit(&g_projectiles[i]);",
            "    }",
            "",
            "    g_lives = 3;",
            "    g_score = 0;",
            "    g_timeleft = 99;",
            "    g_weapondisplay = 1;",
            "    g_currentwave = 0;",
            "    g_wavecooldown = 1;",
            "    g_damagecooldown = 0;",
            "    g_shootcooldown = 0;",
            "    g_victory = 0;",
            "    g_gameover = 0;",
            "    g_framecounter = 0;",
            "    g_checkpointx = 20;",
            "    g_checkpointy = 120;",
            "    g_checkpointactive = 0;",
            "    g_bossactive = 0;",
            "    g_weaponlevel = 0;",
            "    g_pickuptaken = 0;",
            "    enemyinit(&g_boss);",
            "}",
            "",
            "void game_update(void) {",
            "    u8 i;",
            "    u8 j;",
            "",
            "    input_update();",
            "",
            "    if (g_gameover || g_victory) {",
            "        hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);",
            "        return;",
            "    }",
            "",
            "    playerupdate(&g_player);",
            "    try_fire_projectile();",
            "",
            "    if (g_shootcooldown) g_shootcooldown--;",
            "    if (g_damagecooldown) g_damagecooldown--;",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        projectileupdate(&g_projectiles[i]);",
            "    }",
            "",
            "    for (i = 0; i < MAX_ENEMIES; ++i) {",
            "        enemyupdate(&g_enemies[i]);",
            "    }",
            "",
            "    if (g_bossactive) {",
            "        if (g_boss.health > 4) g_bossphase = 0;",
            "        else g_bossphase = 1;",
            "",
            "        g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));",
            "        enemyupdate(&g_boss);",
            "    }",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        if (!g_projectiles[i].active) continue;",
            "        for (j = 0; j < MAX_ENEMIES; ++j) {",
            "            if (!g_enemies[j].active) continue;",
            "            if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,",
            "                             (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;",
            "            if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {",
            "                g_score = (u16)(g_score + g_enemies[j].reward);",
            "                if (g_aliveenemies) g_aliveenemies--;",
            "            }",
            "            g_projectiles[i].active = 0;",
            "            break;",
            "        }",
            "",
            "        if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,",
            "                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {",
            "            g_projectiles[i].active = 0;",
            "            if (enemydamage(&g_boss, g_projectiles[i].damage)) {",
            "                g_bossactive = 0;",
            "                g_score = (u16)(g_score + g_boss.reward);",
            "                g_victory = 1;",
            "            }",
            "        }",
            "    }",
            "",
            "    if (!g_damagecooldown) {",
            "        for (i = 0; i < MAX_ENEMIES; ++i) {",
            "            if (!g_enemies[i].active) continue;",
            "            if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,",
            "                             (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {",
            "                register_player_hit();",
            "                break;",
            "            }",
            "        }",
            "",
            "        if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,",
            "                (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {",
            "            register_player_hit();",
            "        }",
            "",
            "        if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {",
            "            register_player_hit();",
            "        }",
            "    }",
            "",
            "    if (!g_checkpointactive && g_player.x >= 44) {",
            "        g_checkpointactive = 1;",
            "        g_checkpointx = 52;",
            "        g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);",
            "    }",
            "",
            "    if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {",
            "        g_pickuptaken = 1;",
            "        g_weaponlevel = 1;",
            "        g_score = (u16)(g_score + 100);",
            "    }",
            "",
            "    g_weapondisplay = (u8)(g_weaponlevel + 1);",
            "",
            "    if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {",
            "        if (g_currentwave < TOTAL_WAVES) {",
            "            if (g_wavecooldown == 0) {",
            "                spawn_wave(g_currentwave);",
            "                g_currentwave++;",
            "                g_wavecooldown = 90;",
            "            } else {",
            "                g_wavecooldown--;",
            "            }",
            "        } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {",
            "            spawn_boss();",
            "        }",
            "    }",
            "",
            "    g_framecounter++;",
            "    if ((g_framecounter % 50) == 0 && g_timeleft > 0) {",
            "        g_timeleft--;",
            "    }",
            "    if (g_timeleft == 0 && !g_victory) {",
            "        g_gameover = 1;",
            "    }",
            "",
            "    hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);",
            "}",
            "",
            "void game_render(void) {",
            "    u8 i;",
            "",
            "    cpct_clearScreen(0x00);",
            "    tilemap_render();",
            "",
            "    for (i = 0; i < MAX_PROJECTILES; ++i) {",
            "        projectilerender(&g_projectiles[i]);",
            "    }",
            "",
            "    for (i = 0; i < MAX_ENEMIES; ++i) {",
            "        enemyrender(&g_enemies[i]);",
            "    }",
            "",
            "    if (g_bossactive) {",
            "        enemyrender(&g_boss);",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x44, 32, 2);",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x5C, (u8)(g_boss.health * 3), 2);",
            "    }",
            "",
            "    if (!g_pickuptaken) {",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), 0xEE, 4, 4);",
            "    }",
            "    playerrender(&g_player);",
            "    hudrender();",
            "",
            "    if (g_victory) {",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x5A, 32, 12);",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);",
            "    } else if (g_gameover) {",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x44, 32, 12);",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);",
            "    } else if (g_checkpointactive) {",
            "        cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), 0x3A, 2, 8);",
            "    }",
            "}",
            "",
        ]
    )


def _build_main_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("<cpctelera.h>"),
            render_c_include("game.h"),
            "",
            "void main(void) {",
            "    game_init();",
            "    while (1) {",
            "        game_update();",
            "        game_render();",
            "        cpct_waitVSYNC();",
            "    }",
            "}",
            "",
        ]
    )


def _build_player_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef ENTITIES_PLAYER_H",
            "#define ENTITIES_PLAYER_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "    u8 health;",
            "    u8 facing_left;",
            "    u8 jump_hold;",
            "} Player;",
            "",
            "void playerinit(Player* player);",
            "void playerupdate(Player* player);",
            "void playerrender(const Player* player);",
            "",
            "#endif",
            "",
        ]
    )


def _build_enemy_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef ENTITIES_ENEMY_H",
            "#define ENTITIES_ENEMY_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "    u8 active;",
            "    u8 health;",
            "    u8 reward;",
            "    u8 kind;",
            "} Enemy;",
            "",
            "void enemyinit(Enemy* enemy);",
            "void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right);",
            "void enemyupdate(Enemy* enemy);",
            "void enemyrender(const Enemy* enemy);",
            "u8 enemydamage(Enemy* enemy, u8 damage);",
            "",
            "#endif",
            "",
        ]
    )


def _build_projectile_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef ENTITIES_PROJECTILE_H",
            "#define ENTITIES_PROJECTILE_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "typedef struct {",
            "    u8 x;",
            "    u8 y;",
            "    i8 vx;",
            "    i8 vy;",
            "    u8 w;",
            "    u8 h;",
            "    u8 active;",
            "    u8 damage;",
            "    u8 lifetime;",
            "    u8 weapon;",
            "} Projectile;",
            "",
            "void projectileinit(Projectile* projectile);",
            "void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon);",
            "void projectileupdate(Projectile* projectile);",
            "void projectilerender(const Projectile* projectile);",
            "",
            "#endif",
            "",
        ]
    )


def _build_enemy_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("entities/enemy.h"),
            render_c_include("systems/collision.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "void enemyinit(Enemy* enemy) {",
            "    if (!enemy) {",
            "        return;",
            "    }",
            "",
            "    enemy->x = 0;",
            "    enemy->y = 0;",
            "    enemy->vx = 0;",
            "    enemy->vy = 0;",
            "    enemy->w = 4;",
            "    enemy->h = 16;",
            "    enemy->active = 0;",
            "    enemy->health = 1;",
            "    enemy->reward = 100;",
            "    enemy->kind = 0;",
            "}",
            "",
            "void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {",
            "    if (!enemy) {",
            "        return;",
            "    }",
            "",
            "    enemy->x = x;",
            "    enemy->y = y;",
            "    enemy->vx = move_right ? 1 : -1;",
            "    enemy->vy = 0;",
            "    enemy->active = 1;",
            "    enemy->kind = kind;",
            "",
            "    if (kind == 1) {",
            "        enemy->w = 5;",
            "        enemy->h = 14;",
            "        enemy->health = 2;",
            "        enemy->reward = 180;",
            "        enemy->vx = move_right ? 2 : -2;",
            "    } else if (kind == 2) {",
            "        enemy->w = 6;",
            "        enemy->h = 10;",
            "        enemy->health = 1;",
            "        enemy->reward = 150;",
            "        enemy->vy = move_right ? 1 : -1;",
            "        enemy->vx = 1;",
            "    } else if (kind == 3) {",
            "        enemy->w = 10;",
            "        enemy->h = 18;",
            "        enemy->health = 8;",
            "        enemy->reward = 800;",
            "        enemy->vx = move_right ? 1 : -1;",
            "    } else {",
            "        enemy->w = 4;",
            "        enemy->h = 16;",
            "        enemy->health = 1;",
            "        enemy->reward = 100;",
            "    }",
            "}",
            "",
            "void enemyupdate(Enemy* enemy) {",
            "    i16 nextx;",
            "    i16 nexty;",
            "",
            "    if (!enemy || !enemy->active) {",
            "        return;",
            "    }",
            "",
            "    if (enemy->kind == 2) {",
            "        nextx = (i16)enemy->x + (i16)enemy->vx;",
            "        nexty = (i16)enemy->y + (i16)enemy->vy;",
            "",
            "        if (nextx < 8 || nextx > 72) {",
            "            enemy->vx = (i8)(-enemy->vx);",
            "            nextx = (i16)enemy->x + (i16)enemy->vx;",
            "        }",
            "        if (nexty < 56 || nexty > 120) {",
            "            enemy->vy = (i8)(-enemy->vy);",
            "            nexty = (i16)enemy->y + (i16)enemy->vy;",
            "        }",
            "",
            "        enemy->x = (u8)nextx;",
            "        enemy->y = (u8)nexty;",
            "        return;",
            "    }",
            "",
            "    nextx = (i16)enemy->x + (i16)enemy->vx;",
            "    if (nextx < 2) {",
            "        nextx = 2;",
            "        enemy->vx = 1;",
            "    }",
            "    if (nextx > 74) {",
            "        nextx = 74;",
            "        enemy->vx = -1;",
            "    }",
            "    enemy->x = (u8)nextx;",
            "",
            "    enemy->vy = (i8)(enemy->vy + 1);",
            "    if (enemy->vy > 3) enemy->vy = 3;",
            "    nexty = (i16)enemy->y + (i16)enemy->vy;",
            "    nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);",
            "    enemy->y = (u8)nexty;",
            "    if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {",
            "        enemy->vy = 0;",
            "    }",
            "}",
            "",
            "void enemyrender(const Enemy* enemy) {",
            "    u8* pvmem;",
            "    u8 colour;",
            "",
            "    if (!enemy || !enemy->active) {",
            "        return;",
            "    }",
            "",
            "    if (enemy->kind == 3) colour = 0x4C;",
            "    else if (enemy->kind == 2) colour = 0x5A;",
            "    else if (enemy->kind == 1) colour = 0x4E;",
            "    else colour = 0x5C;",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);",
            "    cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);",
            "}",
            "",
            "u8 enemydamage(Enemy* enemy, u8 damage) {",
            "    if (!enemy || !enemy->active) {",
            "        return 0;",
            "    }",
            "",
            "    if (damage >= enemy->health) {",
            "        enemy->health = 0;",
            "        enemy->active = 0;",
            "        return 1;",
            "    }",
            "",
            "    enemy->health = (u8)(enemy->health - damage);",
            "    return 0;",
            "}",
            "",
        ]
    )


def _build_projectile_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("entities/projectile.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "void projectileinit(Projectile* projectile) {",
            "    if (!projectile) {",
            "        return;",
            "    }",
            "",
            "    projectile->x = 0;",
            "    projectile->y = 0;",
            "    projectile->vx = 0;",
            "    projectile->vy = 0;",
            "    projectile->w = 2;",
            "    projectile->h = 2;",
            "    projectile->active = 0;",
            "    projectile->damage = 1;",
            "    projectile->lifetime = 0;",
            "    projectile->weapon = 0;",
            "}",
            "",
            "void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {",
            "    if (!projectile) {",
            "        return;",
            "    }",
            "",
            "    projectile->x = x;",
            "    projectile->y = y;",
            "    projectile->vx = dir;",
            "    projectile->vy = 0;",
            "    projectile->weapon = weapon;",
            "    projectile->active = 1;",
            "",
            "    if (weapon == 0) {",
            "        projectile->w = 3;",
            "        projectile->h = 2;",
            "        projectile->damage = 1;",
            "        projectile->lifetime = 45;",
            "    } else if (weapon == 1) {",
            "        projectile->w = 2;",
            "        projectile->h = 3;",
            "        projectile->damage = 2;",
            "        projectile->lifetime = 28;",
            "    } else {",
            "        projectile->w = 4;",
            "        projectile->h = 3;",
            "        projectile->damage = 3;",
            "        projectile->lifetime = 56;",
            "        projectile->vx = (i8)(dir > 0 ? 4 : -4);",
            "    }",
            "}",
            "",
            "void projectileupdate(Projectile* projectile) {",
            "    if (!projectile || !projectile->active) {",
            "        return;",
            "    }",
            "",
            "    projectile->x = (u8)(projectile->x + projectile->vx);",
            "    projectile->y = (u8)(projectile->y + projectile->vy);",
            "",
            "    if (projectile->lifetime) {",
            "        projectile->lifetime--;",
            "    }",
            "",
            "    if (projectile->x > 78 || projectile->lifetime == 0) {",
            "        projectile->active = 0;",
            "    }",
            "}",
            "",
            "void projectilerender(const Projectile* projectile) {",
            "    u8* pvmem;",
            "",
            "    if (!projectile || !projectile->active) {",
            "        return;",
            "    }",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);",
            "    cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? 0x0F : (projectile->weapon == 1 ? 0x6B : 0x5A), projectile->w, projectile->h);",
            "}",
            "",
        ]
    )


def _build_player_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("entities/player.h"),
            render_c_include("systems/input.h"),
            render_c_include("systems/collision.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "static const i8 kplayermovespeed = 3;",
            "static const i8 kplayeracceleration = 1;",
            "static const i8 kplayerdeceleration = 1;",
            "static const i8 kplayergravity = 1;",
            "static const i8 kplayermaxfall = 4;",
            "static const i8 kplayerjumpvelocity = -6;",
            "static const i8 kplayerjumpboost = -1;",
            "",
            "void playerinit(Player* player) {",
            "    if (!player) {",
            "        return;",
            "    }",
            "",
            "    player->x = 20;",
            "    player->y = 120;",
            "    player->vx = 0;",
            "    player->vy = 0;",
            "    player->w = 4;",
            "    player->h = 16;",
            "    player->health = 3;",
            "    player->facing_left = 0;",
            "    player->jump_hold = 0;",
            "}",
            "",
            "void playerupdate(Player* player) {",
            "    i16 nextx;",
            "    i16 nexty;",
            "",
            "    if (!player) {",
            "        return;",
            "    }",
            "",
            "    if (input_is_left_pressed()) {",
            "        player->vx = (i8)(player->vx - kplayeracceleration);",
            "        player->facing_left = 1;",
            "    } else if (input_is_right_pressed()) {",
            "        player->vx = (i8)(player->vx + kplayeracceleration);",
            "        player->facing_left = 0;",
            "    } else if (player->vx > 0) {",
            "        player->vx = (i8)(player->vx - kplayerdeceleration);",
            "        if (player->vx < 0) player->vx = 0;",
            "    } else if (player->vx < 0) {",
            "        player->vx = (i8)(player->vx + kplayerdeceleration);",
            "        if (player->vx > 0) player->vx = 0;",
            "    }",
            "",
            "    if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;",
            "    if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;",
            "",
            "    if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {",
            "        player->vy = kplayerjumpvelocity;",
            "        player->jump_hold = 5;",
            "    }",
            "",
            "    if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {",
            "        player->vy = (i8)(player->vy + kplayerjumpboost);",
            "        player->jump_hold--;",
            "    } else {",
            "        player->jump_hold = 0;",
            "    }",
            "",
            "    player->vy = (i8)(player->vy + kplayergravity);",
            "    if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;",
            "",
            "    nextx = (i16)player->x + (i16)player->vx;",
            "    if (nextx < 0) {",
            "        nextx = 0;",
            "    }",
            "    if (nextx > 76) {",
            "        nextx = 76;",
            "    }",
            "    player->x = (u8)nextx;",
            "",
            "    nexty = (i16)player->y + (i16)player->vy;",
            "    nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);",
            "    if (nexty < 0) {",
            "        nexty = 0;",
            "    }",
            "    player->y = (u8)nexty;",
            "",
            "    if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {",
            "        player->vy = 0;",
            "    }",
            "}",
            "",
            "void playerrender(const Player* player) {",
            "    u8* pvmem;",
            "",
            "    if (!player) {",
            "        return;",
            "    }",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);",
            "    cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);",
            "}",
            "",
        ]
    )


def _build_input_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_INPUT_H",
            "#define SYSTEMS_INPUT_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "void input_update(void);",
            "u8 input_is_left_pressed(void);",
            "u8 input_is_right_pressed(void);",
            "u8 input_is_up_pressed(void);",
            "u8 input_is_down_pressed(void);",
            "u8 input_is_jump_pressed(void);",
            "u8 input_is_jump_just_pressed(void);",
            "u8 input_is_shoot_pressed(void);",
            "u8 input_is_shoot_just_pressed(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_input_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("systems/input.h"),
            "",
            "static u8 ginputleft;",
            "static u8 ginputright;",
            "static u8 ginputup;",
            "static u8 ginputdown;",
            "static u8 ginputshoot;",
            "static u8 gprevjump;",
            "static u8 gprevshoot;",
            "",
            "void input_update(void) {",
            "    gprevjump = ginputup;",
            "    gprevshoot = ginputshoot;",
            "    cpct_scanKeyboard_f();",
            "    ginputleft = cpct_isKeyPressed(Key_CursorLeft);",
            "    ginputright = cpct_isKeyPressed(Key_CursorRight);",
            "    ginputup = cpct_isKeyPressed(Key_CursorUp);",
            "    ginputdown = cpct_isKeyPressed(Key_X);",
            "    ginputshoot = cpct_isKeyPressed(Key_CursorDown);",
            "}",
            "",
            "u8 input_is_left_pressed(void) {",
            "    return ginputleft;",
            "}",
            "",
            "u8 input_is_right_pressed(void) {",
            "    return ginputright;",
            "}",
            "",
            "u8 input_is_up_pressed(void) {",
            "    return ginputup;",
            "}",
            "",
            "u8 input_is_down_pressed(void) {",
            "    return ginputdown;",
            "}",
            "",
            "u8 input_is_jump_pressed(void) {",
            "    return ginputup;",
            "}",
            "",
            "u8 input_is_jump_just_pressed(void) {",
            "    return (u8)(ginputup && !gprevjump);",
            "}",
            "",
            "u8 input_is_shoot_pressed(void) {",
            "    return ginputshoot;",
            "}",
            "",
            "u8 input_is_shoot_just_pressed(void) {",
            "    return (u8)(ginputshoot && !gprevshoot);",
            "}",
            "",
        ]
    )


def _build_collision_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_COLLISION_H",
            "#define SYSTEMS_COLLISION_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "void collision_init(void);",
            "u8 collision_is_on_ground(i16 y, u8 h);",
            "u8 collision_is_on_ground_at(i16 x, i16 y, u8 h);",
            "i16 collision_clamp_y_to_ground(i16 y, u8 h);",
            "i16 collision_clamp_y_at(i16 x, i16 y, u8 h);",
            "u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h);",
            "u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h);",
            "",
            "#endif",
            "",
        ]
    )


def _build_collision_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("systems/collision.h"),
            render_c_include("systems/tilemap.h"),
            "",
            "static i16 ggroundy = 160;",
            "static i16 gplatformy = 255;",
            "",
            "void collision_init(void) {",
            "    ggroundy = (i16)tilemap_ground_y();",
            "    gplatformy = (i16)tilemap_platform_y_at(32);",
            "}",
            "",
            "u8 collision_is_on_ground(i16 y, u8 h) {",
            "    return collision_is_on_ground_at(0, y, h);",
            "}",
            "",
            "u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {",
            "    i16 feet;",
            "    i16 support;",
            "",
            "    support = (i16)tilemap_ground_y();",
            "    gplatformy = (i16)tilemap_platform_y_at(x);",
            "    if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {",
            "        support = gplatformy;",
            "    }",
            "",
            "    feet = y + (i16)h;",
            "    return (u8)(feet >= support);",
            "}",
            "",
            "i16 collision_clamp_y_to_ground(i16 y, u8 h) {",
            "    return collision_clamp_y_at(0, y, h);",
            "}",
            "",
            "i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {",
            "    i16 maxy;",
            "    i16 platformmaxy;",
            "",
            "    ggroundy = (i16)tilemap_ground_y();",
            "    maxy = ggroundy - (i16)h;",
            "    gplatformy = (i16)tilemap_platform_y_at(x);",
            "    if (gplatformy != 255) {",
            "        platformmaxy = gplatformy - (i16)h;",
            "        if (y > platformmaxy && y <= maxy) {",
            "            return platformmaxy;",
            "        }",
            "    }",
            "",
            "    if (y > maxy) {",
            "        return maxy;",
            "    }",
            "    return y;",
            "}",
            "",
            "u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {",
            "    return tilemap_is_trap(x, y, w, h);",
            "}",
            "",
            "u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {",
            "    return tilemap_is_ladder(x, y, w, h);",
            "}",
            "",
        ]
    )


def _build_tilemap_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_TILEMAP_H",
            "#define SYSTEMS_TILEMAP_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "void tilemap_init(void);",
            "void tilemap_render(void);",
            "u8 tilemap_ground_y(void);",
            "u8 tilemap_platform_y_at(i16 x);",
            "u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h);",
            "u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h);",
            "u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h);",
            "u8 tilemap_goal_x(void);",
            "",
            "#endif",
            "",
        ]
    )


def _build_tilemap_c_stub() -> str:
    return "\n".join(
        [
            render_c_include("systems/tilemap.h"),
            render_c_include("data/level1.h"),
            render_c_include("<cpctelera.h>"),
            "",
            "static u8 gtilegroundy = 160;",
            "static u8 gtileplatformy = 128;",
            "static u8 ggoalx = 72;",
            "",
            "void tilemap_init(void) {",
            "    if (level1tilemapheight > 2) {",
            "        gtilegroundy = (u8)((level1tilemapheight - 2) * 8);",
            "    } else {",
            "        gtilegroundy = 160;",
            "    }",
            "    gtileplatformy = (u8)(gtilegroundy - 24);",
            "    ggoalx = 72;",
            "}",
            "",
            "void tilemap_render(void) {",
            "    u8* pvmem;",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);",
            "    cpct_drawSolidBox(pvmem, 0x11, 80, 8);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);",
            "    cpct_drawSolidBox(pvmem, 0x33, 32, 4);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);",
            "    cpct_drawSolidBox(pvmem, 0x66, 16, 2);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);",
            "    cpct_drawSolidBox(pvmem, 0x5F, 2, 16);",
            "}",
            "",
            "u8 tilemap_ground_y(void) {",
            "    return gtilegroundy;",
            "}",
            "",
            "u8 tilemap_platform_y_at(i16 x) {",
            "    if (x >= 24 && x <= 56) {",
            "        return gtileplatformy;",
            "    }",
            "    return 255;",
            "}",
            "",
            "u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {",
            "    i16 left;",
            "    i16 right;",
            "    i16 feet;",
            "",
            "    left = x;",
            "    right = x + (i16)w;",
            "    feet = y + (i16)h;",
            "",
            "    if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {",
            "        return 1;",
            "    }",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {",
            "    (void)x;",
            "    (void)y;",
            "    (void)w;",
            "    (void)h;",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {",
            "    (void)x;",
            "    (void)y;",
            "    (void)w;",
            "    (void)h;",
            "    return 0;",
            "}",
            "",
            "u8 tilemap_goal_x(void) {",
            "    return ggoalx;",
            "}",
            "",
        ]
    )


def _build_level1_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef DATA_LEVEL1_H",
            "#define DATA_LEVEL1_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "extern const u8 level1tilemap[];",
            "extern const u8 level1tileproperties[];",
            "extern const u8 gpalette16[16];",
            "extern const u16 level1tilemapwidth;",
            "extern const u16 level1tilemapheight;",
            "",
            "#endif",
            "",
        ]
    )


def _build_level1_c_stub() -> str:
    return "\n".join(
        [
            '#include "data/level1.h"',
            "",
            "const u16 level1tilemapwidth = 20;",
            "const u16 level1tilemapheight = 18;",
            "",
            "const u8 level1tilemap[] = {",
            "    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,",
            "    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,",
            "    1, 1, 1, 1, 1, 1, 1, 1, 1, 1",
            "};",
            "",
            "const u8 level1tileproperties[] = { 0, 1 };",
            "",
            "const u8 gpalette16[16] = {",
            "    0x54, 0x44, 0x55, 0x5C,",
            "    0x58, 0x5D, 0x4C, 0x45,",
            "    0x4D, 0x56, 0x46, 0x57,",
            "    0x5E, 0x40, 0x5F, 0x4E",
            "};",
            "",
        ]
    )


def _build_fixed_asset_header(path: str, symbol: str) -> str:
    guard = _header_guard(path)
    return "\n".join(
        [
            f"#ifndef {guard}",
            f"#define {guard}",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            f"extern const u8 {symbol}[];",
            "",
            "#endif",
            "",
        ]
    )


def _build_fixed_asset_source(header_path: str, symbol: str) -> str:
    return "\n".join(
        [
            render_c_include(header_path),
            "",
            f"const u8 {symbol}[] = {{ 0x00 }};",
            "",
        ]
    )


def _build_hud_h_stub() -> str:
    return "\n".join(
        [
            "#ifndef SYSTEMS_HUD_H",
            "#define SYSTEMS_HUD_H",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            render_c_function_decl("void", "hudinit", []),
            render_c_function_decl(
                "void",
                "hudupdate",
                [("u8", "lives"), ("u16", "score"), ("u8", "time"), ("u8", "weapon")],
            ),
            render_c_function_decl("void", "hudrender", []),
            "",
            "#endif",
            "",
        ]
    )


def _build_hud_c_stub() -> str:
    return "\n".join(
        [
            '#include "systems/hud.h"',
            "",
            "static u8  currenthealth;",
            "static u16 currentscore;",
            "static u8  currenttime;",
            "static u8  currentlives;",
            "static u8  currentweapon;",
            "",
            "/* Fallback compile-clean sprites while real HUD assets are wired. */",
            "static const u8 _hud_dummy_sprite[64] = {0};",
            "static const u8* hudnumbers[10] = {",
            "    _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite,",
            "    _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite, _hud_dummy_sprite",
            "};",
            "static const u8 hudhealth[64] = {0};",
            "static const u8 hudlives[64] = {0};",
            "",
            "static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {",
            "    u8 i;",
            "    u8 digit;",
            "    u16 divisor;",
            "    u8* pvmem;",
            "",
            "    divisor = 1;",
            "    for (i = 1; i < digits; ++i) {",
            "        divisor *= 10;",
            "    }",
            "",
            "    for (i = 0; i < digits; ++i) {",
            "        digit = (u8)(value / divisor);",
            "        value = (u16)(value % divisor);",
            "",
            "        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);",
            "        cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);",
            "",
            "        if (divisor > 1) {",
            "            divisor /= 10;",
            "        }",
            "    }",
            "}",
            "",
            "void hudinit(void) {",
            "    currenthealth = 3;",
            "    currentscore  = 0;",
            "    currenttime   = 90;",
            "    currentlives  = 3;",
            "    currentweapon = 0;",
            "}",
            "",
            "void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {",
            "    currenthealth = lives;",
            "    currentscore  = score;",
            "    currenttime   = time;",
            "    currentlives  = lives;",
            "    currentweapon = weapon;",
            "}",
            "",
            "void hudrender(void) {",
            "    u8 i;",
            "    u8* pvmem;",
            "    u16 scoretemp;",
            "    u8 timetemp;",
            "",
            "    for (i = 0; i < currenthealth; ++i) {",
            "        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);",
            "        cpct_drawSprite((u8*)hudhealth, pvmem, 8, 8);",
            "    }",
            "",
            "    scoretemp = currentscore;",
            "    hud_draw_digits(scoretemp, 5, 88, 2);",
            "",
            "    timetemp = currenttime;",
            "    hud_draw_digits((u16)timetemp, 3, 56, 2);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);",
            "    cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);",
            "    cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);",
            "",
            "    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);",
            "    cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);",
            "}",
            "",
        ]
    )


def _header_guard(path: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]", "_", str(path).upper())
    return token or "ASSET_HEADER_H"


def _asset_token(value: str) -> str:
    normalized = normalize_asset_token(str(value))
    if normalized:
        return normalized
    fallback = "".join(ch for ch in str(value).lower() if ch.isalnum() or ch == "_")
    return fallback


def _asset_symbol_name(asset_name: str, target_path: str) -> str:
    token = _asset_token(asset_name)
    if not token:
        token = "".join(ch for ch in PurePosixPath(target_path).stem.lower() if ch.isalnum() or ch == "_")
    if not token:
        token = "asset"
    if not (token[0].isalpha() or token[0] == "_"):
        token = f"asset_{token}"
    return f"{token}_data"


def _build_asset_header_stub_with_symbol(path: str, symbol: str) -> str:
    guard = _header_guard(path)
    return "\n".join(
        [
            f"#ifndef {guard}",
            f"#define {guard}",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            render_c_array_decl("u8", symbol, None, qualifiers=["extern", "const"]),
            "",
            "#endif",
            "",
        ]
    )


def _build_asset_header_stub(path: str, asset_name: str) -> str:
    symbol = _asset_symbol_name(asset_name, path)
    return _build_asset_header_stub_with_symbol(path, symbol)


def _extract_declared_asset_symbol(content: str) -> str:
    match = re.search(r"extern\s+const\s+u8\s+([A-Za-z_][A-Za-z0-9_]*)\s*\[\s*\]\s*;", content)
    if not match:
        return ""
    return match.group(1)


def _sanitize_asset_headers(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    for path, content in list(normalized.items()):
        if not path.startswith("src/data/assets/") or not path.endswith(".h"):
            continue
        if not _is_allowed(path, allowed_files):
            continue

        text = str(content)
        lowered = text.lower()
        if "typedef struct" not in lowered and "typedef enum" not in lowered:
            continue

        symbol = _extract_declared_asset_symbol(text)
        if not symbol:
            symbol = _asset_symbol_name(PurePosixPath(path).stem, path)

        replacement = _build_asset_header_stub_with_symbol(path, symbol)
        if replacement != text:
            normalized[path] = replacement
            sanitized.append(path)

    return normalized, sorted(set(sanitized))


def _sanitize_enemy_source_files(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str]]:
    normalized = dict(files)
    sanitized: list[str] = []

    if not _is_allowed(ENEMY_C_PATH, allowed_files):
        return normalized, sanitized

    current = normalized.get(ENEMY_C_PATH)
    if not current:
        return normalized, sanitized

    enemy_c = str(current)
    enemy_h = str(normalized.get(ENEMY_H_PATH, ""))

    has_local_enemy_typedef = bool(
        re.search(r"typedef\s+struct\s*\{[\s\S]*?\}\s*Enemy\s*;", enemy_c)
    )
    uses_enemy_type = "EnemyType" in enemy_c
    header_declares_enemy_type = bool(
        re.search(r"typedef\s+enum[\s\S]*?EnemyType\s*;", enemy_h)
    )

    required_api_patterns = (
        r"\bvoid\s+enemyinit\s*\(\s*Enemy\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*\)",
        r"\bvoid\s+enemyupdate\s*\(\s*Enemy\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*\)",
        r"\bvoid\s+enemyrender\s*\(\s*const\s+Enemy\s*\*\s*[A-Za-z_][A-Za-z0-9_]*\s*\)",
    )
    has_required_api = all(re.search(pattern, enemy_c) for pattern in required_api_patterns)

    struct_match = re.search(r"typedef\s+struct\s*\{(?P<body>[\s\S]*?)\}\s*Enemy\s*;", enemy_h)
    declared_fields: set[str] = set()
    if struct_match:
        for line in struct_match.group("body").splitlines():
            cleaned = line.split("//", 1)[0].strip()
            if not cleaned:
                continue
            field_match = re.search(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^\]]*\])?\s*;\s*$", cleaned)
            if field_match:
                declared_fields.add(field_match.group(1))

    accessed_fields = set(re.findall(r"(?:->|\.)\s*([A-Za-z_][A-Za-z0-9_]*)", enemy_c))
    unknown_fields = sorted(name for name in accessed_fields if declared_fields and name not in declared_fields)

    should_replace = (
        has_local_enemy_typedef
        or (uses_enemy_type and not header_declares_enemy_type)
        or (not has_required_api)
        or bool(unknown_fields)
    )

    if should_replace:
        replacement = _build_enemy_c_stub()
        if replacement != enemy_c:
            normalized[ENEMY_C_PATH] = replacement
            sanitized.append(ENEMY_C_PATH)

    return normalized, sorted(set(sanitized))


def _build_asset_source_stub(path: str, header_path: str, asset_name: str) -> str:
    symbol = _asset_symbol_name(asset_name, path)

    if "level1tileproperties" in _asset_token(asset_name):
        array_decl = render_c_const_array("u8", "level1tileproperties", ["0x00", "0x01", "0x01", "0x00"])
    else:
        array_decl = render_c_const_array("u8", symbol, ["0x00"])

    return "\n".join(
        [
            render_c_include(header_path),
            "",
            array_decl,
            "",
        ]
    )


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _normalize_compile_profile(value: str) -> str:
    token = "".join(ch for ch in str(value).strip().lower() if ch.isalpha())
    profile_map = {
        "prototype": "prototype",
        "verticalslice": "vertical_slice",
        "playableslice": "playable_slice",
    }
    return profile_map.get(token, "playable_slice")


def _runtime_contract(tech_output: dict | None) -> dict:
    payload = _as_dict(tech_output)
    return _as_dict(payload.get("runtime_contract"))


def _runtime_compile_profile(tech_output: dict | None) -> str:
    runtime = _runtime_contract(tech_output)
    return _normalize_compile_profile(runtime.get("compile_profile", "playable_slice"))


def _normalize_src_path(path: str) -> str:
    candidate = str(path).strip().replace("\\", "/")
    if not candidate:
        return ""
    if candidate.startswith("./"):
        candidate = candidate[2:]
    if not candidate.startswith("src/"):
        return ""
    return PurePosixPath(candidate).as_posix()


def _runtime_critical_modules(tech_output: dict | None) -> set[str]:
    runtime = _runtime_contract(tech_output)
    critical: set[str] = set()

    for path in _as_list(runtime.get("critical_modules")):
        normalized = _normalize_src_path(path)
        if normalized and normalized.endswith(".c"):
            critical.add(normalized)

    return critical


def _runtime_modules_to_preserve(tech_output: dict | None) -> set[str]:
    preserved = set(MANDATORY_RUNTIME_MODULES)
    preserved.update(_runtime_critical_modules(tech_output))
    return {path for path in preserved if path.endswith(".c")}


def _preview_paths(paths: list[str], max_items: int = 8) -> str:
    if not paths:
        return ""
    ordered = sorted(paths)
    preview = ", ".join(ordered[:max_items])
    return preview + (", ..." if len(ordered) > max_items else "")


def _has_enriched_contract(tech_output: dict | None) -> bool:
    if not isinstance(tech_output, dict):
        return False
    return isinstance(tech_output.get("integration_blueprint"), dict) or isinstance(
        tech_output.get("module_contracts"), list
    )


def _collect_raw_src_files(payload: dict) -> list[str]:
    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return []

    result: list[str] = []
    for path in raw_files.keys():
        if not isinstance(path, str):
            continue
        normalized = _normalize_src_path(path)
        if normalized:
            result.append(normalized)
    return sorted(set(result))


def _extract_scaffold_allowed_files(tech_output: dict | None) -> set[str]:
    scaffold = _as_dict(_as_dict(tech_output).get("scaffold"))
    return {
        normalized
        for path in _as_list(scaffold.get("allowed_files"))
        for normalized in [_normalize_src_path(path)]
        if normalized
    }


def _extract_contract_owned_files(tech_output: dict | None) -> set[str]:
    payload = _as_dict(tech_output)
    owned: set[str] = set()

    integration_blueprint = _as_dict(payload.get("integration_blueprint"))
    owned.update(_as_list(integration_blueprint.get("owned_files")))
    owned.update(_as_list(integration_blueprint.get("planned_files")))
    owned.update(_as_list(integration_blueprint.get("integrated_modules")))

    raw_contract_files = integration_blueprint.get("files")
    if isinstance(raw_contract_files, dict):
        owned.update(str(path).strip() for path in raw_contract_files.keys())

    raw_module_contracts = payload.get("module_contracts")
    if isinstance(raw_module_contracts, list):
        for item in raw_module_contracts:
            data = _as_dict(item)
            owned.update(_as_list(data.get("owned_files")))
            owned.add(str(data.get("module", "")).strip())
            owned.add(str(data.get("header", "")).strip())

    normalized_owned = {
        normalized
        for path in owned
        for normalized in [_normalize_src_path(path)]
        if normalized and normalized != "src/scene_game.c"
    }

    return normalized_owned


def _extract_asset_file_map(tech_output: dict | None) -> dict[str, list[str]]:
    payload = _as_dict(tech_output)
    blueprint = _as_dict(payload.get("integration_blueprint"))
    raw_map = blueprint.get("asset_file_map")
    if not isinstance(raw_map, dict):
        return {}

    mapping: dict[str, list[str]] = {}
    for asset_name, files in raw_map.items():
        token = _asset_token(str(asset_name))
        if not token:
            continue
        normalized_files = [
            normalized
            for path in _as_list(files)
            for normalized in [_normalize_src_path(path)]
            if normalized
        ]
        if normalized_files:
            mapping[token] = sorted(set(normalized_files))

    return mapping


def _required_assets_for_integration(tech_output: dict | None) -> list[str]:
    payload = _as_dict(tech_output)
    runtime = _as_dict(payload.get("runtime_contract"))
    raw_module_contracts = payload.get("module_contracts")

    tracked_modules = set(_as_list(runtime.get("integrated_modules")))
    tracked_modules.update(_as_list(runtime.get("critical_modules")))

    required_assets: list[str] = []
    asset_contract = _as_dict(payload.get("asset_contract"))
    required_assets.extend(_as_list(asset_contract.get("required_assets")))

    if isinstance(raw_module_contracts, list):
        for item in raw_module_contracts:
            data = _as_dict(item)
            module_path = _normalize_src_path(str(data.get("module", "")))
            if not module_path:
                continue

            if data.get("integrated", True) or data.get("critical", False):
                tracked_modules.add(module_path)

        for item in raw_module_contracts:
            data = _as_dict(item)
            module_path = _normalize_src_path(str(data.get("module", "")))
            if module_path and module_path in tracked_modules:
                required_assets.extend(_as_list(data.get("required_assets")))

    cleaned: list[str] = []
    for asset in required_assets:
        token = _asset_token(asset)
        if token:
            cleaned.append(token)
    return list(dict.fromkeys(cleaned))


def ensure_required_asset_files(
    files: dict[str, str],
    tech_output: dict | None,
    allowed_files: set[str],
) -> dict[str, str]:
    normalized = dict(files)
    asset_file_map = _extract_asset_file_map(tech_output)
    required_assets = _required_assets_for_integration(tech_output)

    for asset in required_assets:
        for path in asset_file_map.get(asset, []):
            if not _is_allowed(path, allowed_files):
                continue

            if path.endswith(".c"):
                header_path = str(PurePosixPath(path).with_suffix(".h"))
                if _is_allowed(header_path, allowed_files) and header_path not in normalized:
                    normalized[header_path] = _build_asset_header_stub(header_path, asset)

            if path in normalized:
                continue

            if path.endswith(".h"):
                normalized[path] = _build_asset_header_stub(path, asset)
            elif path.endswith(".c"):
                header_path = str(PurePosixPath(path).with_suffix(".h"))
                normalized[path] = _build_asset_source_stub(path, header_path, asset)

    return normalized


def normalize_files_payload(payload: dict, allowed_files: set[str]) -> dict[str, str]:
    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return {}

    normalized: dict[str, str] = {}
    for path, content in raw_files.items():
        if not isinstance(path, str):
            continue
        rel_path = _normalize_src_path(path)
        if not rel_path:
            continue
        if allowed_files and rel_path not in allowed_files:
            continue
        normalized[rel_path] = str(content)

    return normalized


def _normalize_files(payload: dict, allowed_files: set[str]) -> dict[str, str]:
    # Backward-compatible alias.
    return normalize_files_payload(payload, allowed_files)


def _is_allowed(path: str, allowed_files: set[str]) -> bool:
    return not allowed_files or path in allowed_files


def ensure_core_game_module(files: dict[str, str], allowed_files: set[str]) -> dict[str, str]:
    normalized = dict(files)

    if _is_allowed(GAME_H_PATH, allowed_files):
        normalized[GAME_H_PATH] = _build_game_h_stub()

    if _is_allowed(GAME_C_PATH, allowed_files):
        normalized[GAME_C_PATH] = _build_game_c_stub()

    if _is_allowed(MAIN_C_PATH, allowed_files):
        normalized[MAIN_C_PATH] = _build_main_c_stub()

    if _is_allowed(PLAYER_H_PATH, allowed_files):
        normalized[PLAYER_H_PATH] = _build_player_h_stub()

    if _is_allowed(PLAYER_C_PATH, allowed_files):
        normalized[PLAYER_C_PATH] = _build_player_c_stub()

    if _is_allowed(ENEMY_H_PATH, allowed_files):
        normalized[ENEMY_H_PATH] = _build_enemy_h_stub()

    if _is_allowed(ENEMY_C_PATH, allowed_files) and ENEMY_C_PATH not in normalized:
        normalized[ENEMY_C_PATH] = _build_enemy_c_stub()

    if _is_allowed(PROJECTILE_H_PATH, allowed_files):
        normalized[PROJECTILE_H_PATH] = _build_projectile_h_stub()

    if _is_allowed(PROJECTILE_C_PATH, allowed_files):
        normalized[PROJECTILE_C_PATH] = _build_projectile_c_stub()

    if _is_allowed(LEVEL1_H_PATH, allowed_files):
        normalized[LEVEL1_H_PATH] = _build_level1_h_stub()

    if _is_allowed(LEVEL1_C_PATH, allowed_files):
        normalized[LEVEL1_C_PATH] = _build_level1_c_stub()

    if _is_allowed(TILESET_BASE_H_PATH, allowed_files):
        normalized[TILESET_BASE_H_PATH] = _build_fixed_asset_header(TILESET_BASE_H_PATH, "tilesetbase_data")

    if _is_allowed(TILESET_BASE_C_PATH, allowed_files):
        normalized[TILESET_BASE_C_PATH] = _build_fixed_asset_source("data/tileset/base.h", "tilesetbase_data")

    if _is_allowed(PLAYERKNIGHT_H_PATH, allowed_files):
        normalized[PLAYERKNIGHT_H_PATH] = _build_fixed_asset_header(PLAYERKNIGHT_H_PATH, "sprplayerknight_data")

    if _is_allowed(PLAYERKNIGHT_C_PATH, allowed_files):
        normalized[PLAYERKNIGHT_C_PATH] = _build_fixed_asset_source(
            "data/sprites/playerknight.h", "sprplayerknight_data"
        )

    if _is_allowed(HEALTHBAR_H_PATH, allowed_files):
        normalized[HEALTHBAR_H_PATH] = _build_fixed_asset_header(HEALTHBAR_H_PATH, "hudhealthbar_data")

    if _is_allowed(HEALTHBAR_C_PATH, allowed_files):
        normalized[HEALTHBAR_C_PATH] = _build_fixed_asset_source("data/hud/healthbar.h", "hudhealthbar_data")

    if _is_allowed(HUD_H_PATH, allowed_files):
        normalized[HUD_H_PATH] = _build_hud_h_stub()

    if _is_allowed(HUD_C_PATH, allowed_files):
        normalized[HUD_C_PATH] = _build_hud_c_stub()

    if _is_allowed(INPUT_H_PATH, allowed_files):
        normalized[INPUT_H_PATH] = _build_input_h_stub()

    if _is_allowed(INPUT_C_PATH, allowed_files):
        normalized[INPUT_C_PATH] = _build_input_c_stub()

    if _is_allowed(COLLISION_H_PATH, allowed_files):
        normalized[COLLISION_H_PATH] = _build_collision_h_stub()

    if _is_allowed(COLLISION_C_PATH, allowed_files):
        normalized[COLLISION_C_PATH] = _build_collision_c_stub()

    if _is_allowed(TILEMAP_H_PATH, allowed_files):
        normalized[TILEMAP_H_PATH] = _build_tilemap_h_stub()

    if _is_allowed(TILEMAP_C_PATH, allowed_files):
        normalized[TILEMAP_C_PATH] = _build_tilemap_c_stub()

    # scene_game is no longer the central game loop module.
    normalized.pop("src/scene_game.c", None)

    return normalized


def _ensure_core_game_module(files: dict[str, str], allowed_files: set[str]) -> dict[str, str]:
    # Backward-compatible alias.
    return ensure_core_game_module(files, allowed_files)


def _enforce_compile_safe_c_files(
    files: dict[str, str],
    allowed_files: set[str],
    tech_output: dict | None,
) -> tuple[dict[str, str], list[str]]:
    compile_profile = _runtime_compile_profile(tech_output)
    if compile_profile in PLAYABLE_RUNTIME_PROFILES:
        # In playable/vertical slices we keep runtime gameplay modules instead of
        # collapsing to a compile-only core slice.
        return dict(files), []

    compile_safe_c = {
        MAIN_C_PATH,
        GAME_C_PATH,
        LEVEL1_C_PATH,
        TILESET_BASE_C_PATH,
        PLAYERKNIGHT_C_PATH,
        HEALTHBAR_C_PATH,
    }
    compile_safe_c.update(_runtime_modules_to_preserve(tech_output))

    if _is_allowed(HUD_C_PATH, allowed_files):
        compile_safe_c.add(HUD_C_PATH)

    normalized = dict(files)
    dropped: list[str] = []

    for path in sorted(list(normalized.keys())):
        if not path.endswith(".c"):
            continue
        if path in compile_safe_c:
            continue
        dropped.append(path)
        normalized.pop(path, None)

    return normalized, dropped


def _extract_issue_paths(issues: list[str]) -> list[str]:
    paths: set[str] = set()
    for issue in issues:
        candidate = str(issue).split(":", 1)[0].strip()
        normalized = _normalize_src_path(candidate)
        if normalized:
            paths.add(normalized)
    return sorted(paths)


def _build_generic_header_stub(path: str) -> str:
    guard = _header_guard(path)
    return "\n".join(
        [
            f"#ifndef {guard}",
            f"#define {guard}",
            "",
            render_c_include("<cpctelera.h>"),
            "",
            "#endif",
            "",
        ]
    )


def _build_generic_source_stub(path: str, files: dict[str, str]) -> str:
    header_path = str(PurePosixPath(path).with_suffix(".h"))
    lines = []
    if header_path in files:
        lines.append(render_c_include(header_path))
    else:
        lines.append(render_c_include("<cpctelera.h>"))
    lines.extend(["", f"/* compile-safe fallback stub for {PurePosixPath(path).name} */", ""])
    return "\n".join(lines)


def _fallback_stub_for_path(path: str, files: dict[str, str]) -> str:
    stub_builders: dict[str, callable] = {
        MAIN_C_PATH: _build_main_c_stub,
        GAME_H_PATH: _build_game_h_stub,
        GAME_C_PATH: _build_game_c_stub,
        PLAYER_H_PATH: _build_player_h_stub,
        PLAYER_C_PATH: _build_player_c_stub,
        ENEMY_H_PATH: _build_enemy_h_stub,
        ENEMY_C_PATH: _build_enemy_c_stub,
        PROJECTILE_H_PATH: _build_projectile_h_stub,
        PROJECTILE_C_PATH: _build_projectile_c_stub,
        INPUT_H_PATH: _build_input_h_stub,
        INPUT_C_PATH: _build_input_c_stub,
        COLLISION_H_PATH: _build_collision_h_stub,
        COLLISION_C_PATH: _build_collision_c_stub,
        TILEMAP_H_PATH: _build_tilemap_h_stub,
        TILEMAP_C_PATH: _build_tilemap_c_stub,
        LEVEL1_H_PATH: _build_level1_h_stub,
        LEVEL1_C_PATH: _build_level1_c_stub,
        TILESET_BASE_H_PATH: lambda: _build_fixed_asset_header(TILESET_BASE_H_PATH, "tilesetbase_data"),
        TILESET_BASE_C_PATH: lambda: _build_fixed_asset_source("data/tileset/base.h", "tilesetbase_data"),
        PLAYERKNIGHT_H_PATH: lambda: _build_fixed_asset_header(PLAYERKNIGHT_H_PATH, "sprplayerknight_data"),
        PLAYERKNIGHT_C_PATH: lambda: _build_fixed_asset_source("data/sprites/playerknight.h", "sprplayerknight_data"),
        HEALTHBAR_H_PATH: lambda: _build_fixed_asset_header(HEALTHBAR_H_PATH, "hudhealthbar_data"),
        HEALTHBAR_C_PATH: lambda: _build_fixed_asset_source("data/hud/healthbar.h", "hudhealthbar_data"),
        HUD_H_PATH: _build_hud_h_stub,
        HUD_C_PATH: _build_hud_c_stub,
    }

    builder = stub_builders.get(path)
    if builder:
        return builder()

    if path.endswith(".h"):
        return _build_generic_header_stub(path)
    if path.endswith(".c"):
        return _build_generic_source_stub(path, files)
    return ""


def _repair_invalid_generated_files(
    files: dict[str, str],
    allowed_files: set[str],
) -> tuple[dict[str, str], list[str], list[str]]:
    repaired = dict(files)
    repaired_paths: list[str] = []
    remaining_issues = detect_c_generation_issues(repaired)

    for _ in range(2):
        if not remaining_issues:
            break

        issue_paths = _extract_issue_paths(remaining_issues)
        changed = False

        for path in issue_paths:
            if not _is_allowed(path, allowed_files):
                continue

            replacement = _fallback_stub_for_path(path, repaired)
            if not replacement:
                continue

            if repaired.get(path) == replacement:
                continue

            repaired[path] = replacement
            repaired_paths.append(path)
            changed = True

        if not changed:
            break

        remaining_issues = detect_c_generation_issues(repaired)

    return repaired, sorted(set(repaired_paths)), remaining_issues


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
    tech_output: dict | None = None,
) -> dict:
    blocks = []
    if orchestrator_output:
        blocks.append("Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2))
    if narrative_output:
        blocks.append("Narrative JSON:\n" + json.dumps(narrative_output, ensure_ascii=False, indent=2))
    if design_output:
        blocks.append("Design JSON:\n" + json.dumps(design_output, ensure_ascii=False, indent=2))
    if art_output:
        blocks.append("Art JSON:\n" + json.dumps(art_output, ensure_ascii=False, indent=2))
    if tech_output:
        blocks.append("Tech JSON:\n" + json.dumps(tech_output, ensure_ascii=False, indent=2))

    payload = json_call("code_integrator", user_request, "\n\n".join(blocks))

    contract_mode = _has_enriched_contract(tech_output)
    scaffold_allowed_files = _extract_scaffold_allowed_files(tech_output)
    contract_owned_files = _extract_contract_owned_files(tech_output) if contract_mode else set()

    if contract_mode and contract_owned_files:
        allowed_files = set(contract_owned_files)
        if scaffold_allowed_files:
            allowed_files = allowed_files.intersection(scaffold_allowed_files)
    else:
        allowed_files = set(scaffold_allowed_files)

    raw_src_files = _collect_raw_src_files(payload)
    compile_profile = _runtime_compile_profile(tech_output)

    files = normalize_files_payload(payload, allowed_files)
    files_before_core = dict(files)
    files = ensure_core_game_module(files, allowed_files)
    files = ensure_required_asset_files(files, tech_output, allowed_files)
    files, sanitized_asset_headers = _sanitize_asset_headers(files, allowed_files)
    files, sanitized_enemy_sources = _sanitize_enemy_source_files(files, allowed_files)
    files, dropped_unsafe_c = _enforce_compile_safe_c_files(files, allowed_files, tech_output)
    files, repaired_invalid_files, prebuild_validation_errors = _repair_invalid_generated_files(files, allowed_files)

    if not files:
        if contract_mode and contract_owned_files:
            expected_preview = _preview_paths(sorted(contract_owned_files))
            notes = (
                "CodeIntegratorAgent returned no valid contract-owned files. "
                f"Expected owned files: {expected_preview}."
            )
        elif contract_mode:
            notes = (
                "CodeIntegratorAgent returned no valid files. "
                "Contract metadata exists but owned_files are missing; scaffold fallback also produced no files."
            )
        else:
            notes = "CodeIntegratorAgent returned no valid scaffold files."

        return {
            "files": {},
            "integration_notes": notes,
            "prebuild_validation_errors": [],
        }

    notes_parts: list[str] = []
    if contract_mode:
        notes_parts.append(
            f"Contract mode enabled. Accepted {len(files_before_core)} of {len(raw_src_files)} generated files."
        )

        if contract_owned_files:
            outside_contract = sorted(path for path in raw_src_files if path not in contract_owned_files)
            if outside_contract:
                notes_parts.append(
                    "Rejected "
                    f"{len(outside_contract)} files outside owned contract files: "
                    f"{_preview_paths(outside_contract)}."
                )

            expected_contract_files = sorted(
                path for path in contract_owned_files if path.endswith(".c") or path.endswith(".h")
            )
            missing_expected = sorted(path for path in expected_contract_files if path not in files)
            if missing_expected:
                notes_parts.append(
                    "Missing "
                    f"{len(missing_expected)} expected contract files: "
                    f"{_preview_paths(missing_expected)}."
                )
        else:
            notes_parts.append(
                "Contract metadata exists but owned_files are empty; fallback to scaffold.allowed_files was used."
            )

        injected = len(files) - len(files_before_core)
        if injected > 0:
            notes_parts.append(
                f"Injected {injected} core files allowed by contract/scaffold policy."
            )

        if dropped_unsafe_c:
            notes_parts.append(
                "Omitted "
                f"{len(dropped_unsafe_c)} non-core C file(s) to keep compile-only slice stable: "
                f"{_preview_paths(dropped_unsafe_c)}."
            )
            if compile_profile in PLAYABLE_RUNTIME_PROFILES:
                notes_parts.append(
                    "Runtime compile profile is playable/vertical, so C-file pruning was skipped."
                )
    else:
        notes_parts.append(f"Generated {len(files)} valid source files.")

    if repaired_invalid_files:
        notes_parts.append(
            "Repaired "
            f"{len(repaired_invalid_files)} file(s) with deterministic compile-safe stubs: "
            f"{_preview_paths(repaired_invalid_files)}."
        )

    if sanitized_asset_headers:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_asset_headers)} asset header(s) to data-only declarations: "
            f"{_preview_paths(sanitized_asset_headers)}."
        )

    if sanitized_enemy_sources:
        notes_parts.append(
            "Sanitized "
            f"{len(sanitized_enemy_sources)} enemy source file(s) to remove invalid type coupling: "
            f"{_preview_paths(sanitized_enemy_sources)}."
        )

    if prebuild_validation_errors:
        preview = " | ".join(prebuild_validation_errors[:3])
        notes_parts.append(
            "Pre-build C validation failed with "
            f"{len(prebuild_validation_errors)} issue(s): {preview}"
            f"{' | ...' if len(prebuild_validation_errors) > 3 else ''}."
        )

    integration_notes = " ".join(part for part in notes_parts if part).strip()

    return {
        "files": files,
        "integration_notes": integration_notes,
        "prebuild_validation_errors": prebuild_validation_errors,
    }
