;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module game
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl ___game_entry_jp
	.globl _hudrender
	.globl _hudupdate
	.globl _hudinit
	.globl _projectilerender
	.globl _projectileupdate
	.globl _projectilefire
	.globl _projectileinit
	.globl _enemydamage
	.globl _enemyrender
	.globl _enemyupdate
	.globl _enemyspawn
	.globl _enemyinit
	.globl _playerrender
	.globl _playerupdate
	.globl _playerinit
	.globl _collision_is_on_trap
	.globl _collision_init
	.globl _input_is_shoot_just_pressed
	.globl _input_is_shoot_pressed
	.globl _input_is_jump_pressed
	.globl _input_is_right_pressed
	.globl _input_is_left_pressed
	.globl _input_update
	.globl _tilemap_goal_x
	.globl _tilemap_ground_y
	.globl _tilemap_render
	.globl _tilemap_init
	.globl _cpct_getScreenPtr
	.globl _cpct_setPALColour
	.globl _cpct_setPalette
	.globl _cpct_setVideoMode
	.globl _cpct_drawSolidBox
	.globl _cpct_px2byteM0
	.globl _cpct_memset
	.globl _cpct_disableFirmware
	.globl _game_init
	.globl _game_update
	.globl _game_render
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
_g_player:
	.ds 10
_g_enemies:
	.ds 60
_g_projectiles:
	.ds 60
_prev_enemy_x:
	.ds 6
_prev_enemy_y:
	.ds 6
_prev_enemy_w:
	.ds 6
_prev_enemy_h:
	.ds 6
_prev_enemy_act:
	.ds 6
_prev_boss_x:
	.ds 1
_prev_boss_y:
	.ds 1
_prev_boss_act:
	.ds 1
_prev_proj_x:
	.ds 6
_prev_proj_y:
	.ds 6
_prev_proj_w:
	.ds 6
_prev_proj_h:
	.ds 6
_prev_proj_act:
	.ds 6
_g_lives:
	.ds 1
_g_score:
	.ds 2
_g_timeleft:
	.ds 1
_g_weapondisplay:
	.ds 1
_g_currentwave:
	.ds 1
_g_aliveenemies:
	.ds 1
_g_wavecooldown:
	.ds 1
_g_damagecooldown:
	.ds 1
_g_shootcooldown:
	.ds 1
_g_victory:
	.ds 1
_g_gameover:
	.ds 1
_g_framecounter:
	.ds 2
_g_checkpointx:
	.ds 1
_g_checkpointy:
	.ds 1
_g_checkpointactive:
	.ds 1
_g_boss:
	.ds 10
_g_bossactive:
	.ds 1
_g_bossphase:
	.ds 1
_g_weaponlevel:
	.ds 1
_g_pickuptaken:
	.ds 1
_g_dbg_left:
	.ds 1
_g_dbg_right:
	.ds 1
_g_dbg_jump:
	.ds 1
_g_dbg_shoot:
	.ds 1
_g_dbg_move_raw:
	.ds 1
_g_dbg_move_net:
	.ds 1
_g_dbg_move_cancelled:
	.ds 1
_g_dbg_hit:
	.ds 1
_g_dbg_vx:
	.ds 1
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _INITIALIZED
_prev_player_x:
	.ds 1
_prev_player_y:
	.ds 1
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area _DABS (ABS)
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area _HOME
	.area _GSINIT
	.area _GSFINAL
	.area _GSINIT
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area _HOME
	.area _HOME
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area _CODE
;src/game.c:15: void __game_entry_jp(void) __naked {
;	---------------------------------
; Function __game_entry_jp
; ---------------------------------
___game_entry_jp::
;src/game.c:19: __endasm;
	.globl	cpc_run_address
	jp	cpc_run_address
;src/game.c:72: static void reset_player_to_checkpoint(void) {
;	---------------------------------
; Function reset_player_to_checkpoint
; ---------------------------------
_reset_player_to_checkpoint:
;src/game.c:73: g_player.x = g_checkpointx;
	ld	hl, #_g_player
	ld	a,(#_g_checkpointx + 0)
	ld	(hl), a
;src/game.c:74: g_player.y = g_checkpointy;
	ld	hl, #(_g_player + 0x0001)
	ld	a,(#_g_checkpointy + 0)
	ld	(hl), a
;src/game.c:75: g_player.vx = 0;
	ld	hl, #(_g_player + 0x0002)
	ld	(hl), #0x00
;src/game.c:76: g_player.vy = 0;
	ld	hl, #(_g_player + 0x0003)
	ld	(hl), #0x00
	ret
;src/game.c:79: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
;	---------------------------------
; Function rect_overlap
; ---------------------------------
_rect_overlap:
	push	ix
	ld	ix,#0
	add	ix,sp
;src/game.c:80: if (ax + aw <= bx) return 0;
	ld	c, 8 (ix)
	ld	b, #0x00
	ld	l,4 (ix)
	ld	h,5 (ix)
	add	hl, bc
	ld	a, 10 (ix)
	sub	a, l
	ld	a, 11 (ix)
	sbc	a, h
	jp	PO, 00127$
	xor	a, #0x80
00127$:
	jp	M, 00102$
	ld	l, #0x00
	jr	00109$
00102$:
;src/game.c:81: if (bx + bw <= ax) return 0;
	ld	c, 14 (ix)
	ld	b, #0x00
	ld	l,10 (ix)
	ld	h,11 (ix)
	add	hl, bc
	ld	a, 4 (ix)
	sub	a, l
	ld	a, 5 (ix)
	sbc	a, h
	jp	PO, 00128$
	xor	a, #0x80
00128$:
	jp	M, 00104$
	ld	l, #0x00
	jr	00109$
00104$:
;src/game.c:82: if (ay + ah <= by) return 0;
	ld	c, 9 (ix)
	ld	b, #0x00
	ld	l,6 (ix)
	ld	h,7 (ix)
	add	hl, bc
	ld	a, 12 (ix)
	sub	a, l
	ld	a, 13 (ix)
	sbc	a, h
	jp	PO, 00129$
	xor	a, #0x80
00129$:
	jp	M, 00106$
	ld	l, #0x00
	jr	00109$
00106$:
;src/game.c:83: if (by + bh <= ay) return 0;
	ld	c, 15 (ix)
	ld	b, #0x00
	ld	l,12 (ix)
	ld	h,13 (ix)
	add	hl, bc
	ld	a, 6 (ix)
	sub	a, l
	ld	a, 7 (ix)
	sbc	a, h
	jp	PO, 00130$
	xor	a, #0x80
00130$:
	jp	M, 00108$
	ld	l, #0x00
	jr	00109$
00108$:
;src/game.c:84: return 1;
	ld	l, #0x01
00109$:
	pop	ix
	ret
;src/game.c:87: static void spawn_wave(u8 wave) {
;	---------------------------------
; Function spawn_wave
; ---------------------------------
_spawn_wave:
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	push	af
	dec	sp
;src/game.c:91: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	bc, #_g_enemies+0
	ld	e, #0x00
00119$:
;src/game.c:92: enemyinit(&g_enemies[i]);
	push	de
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	add	hl, bc
	push	bc
	push	de
	push	hl
	call	_enemyinit
	pop	af
	pop	de
	pop	bc
;src/game.c:91: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00119$
;src/game.c:96: else if (wave == 1) count = 3;
	ld	a, 4 (ix)
	dec	a
	jr	NZ,00196$
	ld	a,#0x01
	jr	00197$
00196$:
	xor	a,a
00197$:
	ld	e, a
;src/game.c:95: if (wave == 0) count = 2;
	ld	a, 4 (ix)
	or	a, a
	jr	NZ,00106$
	ld	-3 (ix), #0x02
	jr	00107$
00106$:
;src/game.c:96: else if (wave == 1) count = 3;
	ld	a, e
	or	a, a
	jr	Z,00103$
	ld	-3 (ix), #0x03
	jr	00107$
00103$:
;src/game.c:97: else count = 4;
	ld	-3 (ix), #0x04
00107$:
;src/game.c:99: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
	ld	a, #0x06
	sub	a, -3 (ix)
	jr	NC,00151$
	ld	-3 (ix), #0x06
;src/game.c:101: for (i = 0; i < count; ++i) {
00151$:
	ld	-1 (ix), e
	ld	e, #0x00
00122$:
	ld	a, e
	sub	a, -3 (ix)
	jp	NC, 00118$
;src/game.c:105: if (wave == 0) type = 0;
	ld	a, 4 (ix)
	or	a, a
	jr	NZ,00114$
	ld	-4 (ix), #0x00
	jr	00115$
00114$:
;src/game.c:106: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
	ld	a, -1 (ix)
	or	a, a
	jr	Z,00111$
	ld	a, e
	or	a, a
	jr	NZ,00126$
	ld	d, #0x01
	jr	00127$
00126$:
	ld	d, #0x00
00127$:
	ld	-4 (ix), d
	jr	00115$
00111$:
;src/game.c:107: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
	ld	a, e
	or	a, a
	jr	Z,00131$
	ld	a, e
	sub	a, #0x03
	jr	NZ,00128$
00131$:
	ld	d, #0x02
	jr	00129$
00128$:
	ld	d, #0x01
00129$:
	ld	-4 (ix), d
00115$:
;src/game.c:109: spawn_y = (type == 2) ? 84 : 112;
	ld	a, -4 (ix)
	sub	a, #0x02
	jr	NZ,00133$
	ld	d, #0x54
	jr	00134$
00133$:
	ld	d, #0x70
00134$:
	ld	-5 (ix), d
;src/game.c:111: spawn_x = (u8)(36 + (i * 16));
	ld	a, e
	rlca
	rlca
	rlca
	rlca
	and	a, #0xf0
	add	a, #0x24
	ld	d, a
;src/game.c:112: if (spawn_x > 68) spawn_x = 68;
	ld	a, #0x44
	sub	a, d
	jr	NC,00117$
	ld	d, #0x44
00117$:
;src/game.c:113: enemyspawn(&g_enemies[i], spawn_x, spawn_y, type, (u8)((i & 1) ? 1 : 0));
	bit	0, e
	jr	Z,00135$
	ld	-2 (ix), #0x01
	jr	00136$
00135$:
	ld	-2 (ix), #0x00
00136$:
	push	de
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	add	hl, bc
	push	hl
	pop	iy
	push	bc
	push	de
	ld	h, -2 (ix)
	ld	l, -4 (ix)
	push	hl
	ld	a, -5 (ix)
	push	af
	inc	sp
	push	de
	inc	sp
	push	iy
	call	_enemyspawn
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
	pop	de
	pop	bc
;src/game.c:101: for (i = 0; i < count; ++i) {
	inc	e
	jp	00122$
00118$:
;src/game.c:116: g_aliveenemies = count;
	ld	a, -3 (ix)
	ld	(#_g_aliveenemies + 0),a
	ld	sp, ix
	pop	ix
	ret
;src/game.c:119: static void spawn_boss(void) {
;	---------------------------------
; Function spawn_boss
; ---------------------------------
_spawn_boss:
;src/game.c:120: enemyinit(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyinit
	pop	af
;src/game.c:121: enemyspawn(&g_boss, 68, 112, 1, 0);
	ld	hl, #0x0001
	push	hl
	ld	hl, #0x7044
	push	hl
	ld	hl, #_g_boss
	push	hl
	call	_enemyspawn
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
;src/game.c:122: g_boss.w = 10;
	ld	hl, #(_g_boss + 0x0004)
	ld	(hl), #0x0a
;src/game.c:123: g_boss.h = 18;
	ld	hl, #(_g_boss + 0x0005)
	ld	(hl), #0x12
;src/game.c:124: g_boss.health = 10;
	ld	hl, #(_g_boss + 0x0007)
	ld	(hl), #0x0a
;src/game.c:125: g_boss.reward = 255; /* u8 max; score adds separately on kill */
	ld	hl, #(_g_boss + 0x0008)
	ld	(hl), #0xff
;src/game.c:126: g_boss.kind = 3;
	ld	hl, #(_g_boss + 0x0009)
	ld	(hl), #0x03
;src/game.c:127: g_boss.vx = -1;
	ld	hl, #(_g_boss + 0x0002)
	ld	(hl), #0xff
;src/game.c:128: g_bossactive = 1;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x01
;src/game.c:129: g_bossphase = 0;
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x00
	ret
;src/game.c:132: static void try_fire_projectile(void) {
;	---------------------------------
; Function try_fire_projectile
; ---------------------------------
_try_fire_projectile:
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	dec	sp
;src/game.c:136: if (!input_is_shoot_just_pressed()) return;
	call	_input_is_shoot_just_pressed
	ld	a, l
	or	a, a
	jp	Z,00110$
;src/game.c:137: if (g_shootcooldown) return;
	ld	a,(#_g_shootcooldown + 0)
	or	a, a
	jp	NZ,00110$
;src/game.c:139: dir = g_player.facing_left ? -3 : 3;
	ld	a, (#_g_player + 8)
	or	a, a
	jr	Z,00112$
	ld	c, #0xfd
	jr	00113$
00112$:
	ld	c, #0x03
00113$:
;src/game.c:141: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	-1 (ix), #0x00
	ld	b, #0x00
00108$:
;src/game.c:142: if (!g_projectiles[i].active) {
	ld	e,b
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	ld	de, #_g_projectiles
	add	hl, de
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
	jr	NZ,00109$
;src/game.c:144: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
	ld	a,(#_g_weaponlevel + 0)
	or	a, a
	jr	Z,00114$
	ld	-2 (ix), #0x01
	jr	00115$
00114$:
	ld	-2 (ix), #0x00
00115$:
	ld	a, (#_g_player + 1)
	add	a, #0x06
	ld	-3 (ix), a
	ld	hl, #_g_player + 0
	ld	b, (hl)
	inc	b
	inc	b
	ld	e,-1 (ix)
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	ld	de, #_g_projectiles
	add	hl, de
	ex	de,hl
	ld	a, -2 (ix)
	push	af
	inc	sp
	ld	a, c
	push	af
	inc	sp
	ld	a, -3 (ix)
	push	af
	inc	sp
	push	bc
	inc	sp
	push	de
	call	_projectilefire
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
;src/game.c:145: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
	ld	a,(#_g_weaponlevel + 0)
	or	a, a
	jr	Z,00116$
	ld	c, #0x04
	jr	00117$
00116$:
	ld	c, #0x08
00117$:
	ld	hl,#_g_shootcooldown + 0
	ld	(hl), c
;src/game.c:146: break;
	jr	00110$
00109$:
;src/game.c:141: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	b
	ld	-1 (ix), b
	ld	a, b
	sub	a, #0x06
	jr	C,00108$
00110$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:151: static void register_player_hit(void) {
;	---------------------------------
; Function register_player_hit
; ---------------------------------
_register_player_hit:
;src/game.c:152: if (g_lives) {
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00102$
;src/game.c:153: g_lives--;
	dec	0 (iy)
00102$:
;src/game.c:155: if (g_lives == 0) {
	ld	a,(#_g_lives + 0)
	or	a, a
	jr	NZ,00104$
;src/game.c:156: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
;src/game.c:157: return;
	ret
00104$:
;src/game.c:160: reset_player_to_checkpoint();
	call	_reset_player_to_checkpoint
;src/game.c:161: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
	ret
;src/game.c:164: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/game.c:167: cpct_setVideoMode(0);
	ld	l, #0x00
	call	_cpct_setVideoMode
;src/game.c:168: cpct_disableFirmware();
	call	_cpct_disableFirmware
;src/game.c:169: cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
	ld	hl, #0x0010
	push	hl
	ld	hl, #_gpalette
	push	hl
	call	_cpct_setPalette
;src/game.c:170: cpct_setBorder(gpalette[0]);
	ld	hl, #_gpalette + 0
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
;src/game.c:171: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:172: tilemap_init();
	call	_tilemap_init
;src/game.c:173: collision_init();
	call	_collision_init
;src/game.c:174: playerinit(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerinit
	pop	af
;src/game.c:175: hudinit();
	call	_hudinit
;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00102$:
;src/game.c:178: projectileinit(&g_projectiles[i]);
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	de, #_g_projectiles
	add	hl, de
	push	bc
	push	hl
	call	_projectileinit
	pop	af
	pop	bc
;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00102$
;src/game.c:181: g_lives = 3;
	ld	hl,#_g_lives + 0
	ld	(hl), #0x03
;src/game.c:182: g_score = 0;
	ld	hl, #0x0000
	ld	(_g_score), hl
;src/game.c:183: g_timeleft = 99;
	ld	iy, #_g_timeleft
	ld	0 (iy), #0x63
;src/game.c:184: g_weapondisplay = 1;
	ld	iy, #_g_weapondisplay
	ld	0 (iy), #0x01
;src/game.c:185: g_currentwave = 0;
	ld	iy, #_g_currentwave
	ld	0 (iy), #0x00
;src/game.c:186: g_wavecooldown = 1;
	ld	iy, #_g_wavecooldown
	ld	0 (iy), #0x01
;src/game.c:187: g_damagecooldown = 100;
	ld	iy, #_g_damagecooldown
	ld	0 (iy), #0x64
;src/game.c:188: g_shootcooldown = 0;
	ld	iy, #_g_shootcooldown
	ld	0 (iy), #0x00
;src/game.c:189: g_victory = 0;
	ld	iy, #_g_victory
	ld	0 (iy), #0x00
;src/game.c:190: g_gameover = 0;
	ld	iy, #_g_gameover
	ld	0 (iy), #0x00
;src/game.c:191: g_framecounter = 0;
	ld	l, #0x00
	ld	(_g_framecounter), hl
;src/game.c:192: g_checkpointx = 12;
	ld	hl,#_g_checkpointx + 0
	ld	(hl), #0x0c
;src/game.c:193: g_checkpointy = 104;
	ld	hl,#_g_checkpointy + 0
	ld	(hl), #0x68
;src/game.c:194: g_checkpointactive = 0;
	ld	hl,#_g_checkpointactive + 0
	ld	(hl), #0x00
;src/game.c:195: g_bossactive = 0;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x00
;src/game.c:196: g_weaponlevel = 0;
	ld	hl,#_g_weaponlevel + 0
	ld	(hl), #0x00
;src/game.c:197: g_pickuptaken = 0;
	ld	hl,#_g_pickuptaken + 0
	ld	(hl), #0x00
;src/game.c:198: g_dbg_left = 0;
	ld	hl,#_g_dbg_left + 0
	ld	(hl), #0x00
;src/game.c:199: g_dbg_right = 0;
	ld	hl,#_g_dbg_right + 0
	ld	(hl), #0x00
;src/game.c:200: g_dbg_jump = 0;
	ld	hl,#_g_dbg_jump + 0
	ld	(hl), #0x00
;src/game.c:201: g_dbg_shoot = 0;
	ld	hl,#_g_dbg_shoot + 0
	ld	(hl), #0x00
;src/game.c:202: g_dbg_move_raw = 0;
	ld	hl,#_g_dbg_move_raw + 0
	ld	(hl), #0x00
;src/game.c:203: g_dbg_move_net = 0;
	ld	hl,#_g_dbg_move_net + 0
	ld	(hl), #0x00
;src/game.c:204: g_dbg_move_cancelled = 0;
	ld	hl,#_g_dbg_move_cancelled + 0
	ld	(hl), #0x00
;src/game.c:205: g_dbg_hit = 0;
	ld	hl,#_g_dbg_hit + 0
	ld	(hl), #0x00
;src/game.c:206: g_dbg_vx = 0;
	ld	hl,#_g_dbg_vx + 0
	ld	(hl), #0x00
;src/game.c:207: enemyinit(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyinit
	pop	af
	ret
;src/game.c:210: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-28
	add	hl, sp
	ld	sp, hl
;src/game.c:221: input_update();
	call	_input_update
;src/game.c:223: left_pressed = input_is_left_pressed();
	call	_input_is_left_pressed
	ld	c, l
;src/game.c:224: right_pressed = input_is_right_pressed();
	push	bc
	call	_input_is_right_pressed
	pop	bc
	ld	b, l
;src/game.c:225: jump_pressed = input_is_jump_pressed();
	push	bc
	call	_input_is_jump_pressed
	ld	e, l
	push	de
	call	_input_is_shoot_pressed
	pop	de
	pop	bc
	ld	d, l
;src/game.c:228: g_dbg_left = left_pressed;
	ld	hl,#_g_dbg_left + 0
	ld	(hl), c
;src/game.c:229: g_dbg_right = right_pressed;
	ld	hl,#_g_dbg_right + 0
	ld	(hl), b
;src/game.c:230: g_dbg_jump = jump_pressed;
	ld	hl,#_g_dbg_jump + 0
	ld	(hl), e
;src/game.c:231: g_dbg_shoot = shoot_pressed;
	ld	hl,#_g_dbg_shoot + 0
	ld	(hl), d
;src/game.c:234: if (left_pressed && !right_pressed) {
	ld	a, c
	or	a, a
	jr	Z,00112$
	ld	a, b
	or	a, a
	jr	NZ,00112$
;src/game.c:235: cpct_setBorder(gpalette[2]);
	ld	hl, #_gpalette+2
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
	jr	00113$
00112$:
;src/game.c:236: } else if (right_pressed && !left_pressed) {
	ld	a, b
	or	a, a
	jr	Z,00108$
	ld	a, c
	or	a, a
	jr	NZ,00108$
;src/game.c:237: cpct_setBorder(gpalette[14]);
	ld	hl, #_gpalette+14
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
	jr	00113$
00108$:
;src/game.c:238: } else if (jump_pressed) {
	ld	a, e
	or	a, a
	jr	Z,00105$
;src/game.c:239: cpct_setBorder(gpalette[3]);
	ld	hl, #_gpalette+3
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
	jr	00113$
00105$:
;src/game.c:240: } else if (shoot_pressed) {
	ld	a, d
	or	a, a
	jr	Z,00102$
;src/game.c:241: cpct_setBorder(gpalette[6]);
	ld	hl, #_gpalette+6
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
	jr	00113$
00102$:
;src/game.c:243: cpct_setBorder(gpalette[0]);
	ld	hl, #_gpalette+0
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
00113$:
;src/game.c:246: if (g_gameover || g_victory) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	NZ,00115$
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	Z,00116$
00115$:
;src/game.c:247: g_dbg_move_raw = 0;
	ld	hl,#_g_dbg_move_raw + 0
	ld	(hl), #0x00
;src/game.c:248: g_dbg_move_net = 0;
	ld	hl,#_g_dbg_move_net + 0
	ld	(hl), #0x00
;src/game.c:249: g_dbg_move_cancelled = 0;
	ld	hl,#_g_dbg_move_cancelled + 0
	ld	(hl), #0x00
;src/game.c:250: g_dbg_hit = 0;
	ld	hl,#_g_dbg_hit + 0
	ld	(hl), #0x00
;src/game.c:251: g_dbg_vx = g_player.vx;
	ld	a, (#_g_player+2)
	ld	(#_g_dbg_vx + 0),a
;src/game.c:252: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
	ld	a, (_g_weapondisplay)
	push	af
	inc	sp
	ld	a, (_g_timeleft)
	push	af
	inc	sp
	ld	hl, (_g_score)
	push	hl
	ld	a, (_g_lives)
	push	af
	inc	sp
	call	_hudupdate
	pop	af
	pop	af
	inc	sp
;src/game.c:253: return;
	jp	00195$
00116$:
;src/game.c:256: player_x_start = g_player.x;
	ld	a, (#_g_player+0)
	ld	-26 (ix), a
;src/game.c:257: playerupdate(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerupdate
	pop	af
;src/game.c:258: player_x_after_move = g_player.x;
	ld	a,(#_g_player + 0)
	ld	-27 (ix), a
;src/game.c:259: g_dbg_vx = g_player.vx;
	ld	a,(#_g_player + 2)
	ld	(#_g_dbg_vx + 0),a
;src/game.c:260: try_fire_projectile();
	call	_try_fire_projectile
;src/game.c:262: if (g_shootcooldown) g_shootcooldown--;
	ld	iy, #_g_shootcooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00119$
	dec	0 (iy)
00119$:
;src/game.c:263: if (g_damagecooldown) g_damagecooldown--;
	ld	iy, #_g_damagecooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00215$
	dec	0 (iy)
;src/game.c:265: for (i = 0; i < MAX_PROJECTILES; ++i) {
00215$:
	ld	-24 (ix), #0x00
00188$:
;src/game.c:266: projectileupdate(&g_projectiles[i]);
	ld	c,-24 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	-2 (ix), l
	ld	-1 (ix), h
	ld	a, #<(_g_projectiles)
	add	a, -2 (ix)
	ld	-2 (ix), a
	ld	a, #>(_g_projectiles)
	adc	a, -1 (ix)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	push	hl
	call	_projectileupdate
	pop	af
;src/game.c:265: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	-24 (ix)
	ld	a, -24 (ix)
	sub	a, #0x06
	jr	C,00188$
;src/game.c:269: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	-24 (ix), #0x00
00190$:
;src/game.c:270: enemyupdate(&g_enemies[i]);
	ld	c,-24 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	-2 (ix), l
	ld	-1 (ix), h
	ld	a, #<(_g_enemies)
	add	a, -2 (ix)
	ld	-2 (ix), a
	ld	a, #>(_g_enemies)
	adc	a, -1 (ix)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	push	hl
	call	_enemyupdate
	pop	af
;src/game.c:269: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-24 (ix)
	ld	a, -24 (ix)
	sub	a, #0x06
	jr	C,00190$
;src/game.c:273: if (g_bossactive) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00234$
;src/game.c:274: if (g_boss.health > 4) g_bossphase = 0;
	ld	hl, #_g_boss + 7
	ld	c, (hl)
	ld	a, #0x04
	sub	a, c
	jr	NC,00125$
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x00
	jr	00126$
00125$:
;src/game.c:275: else g_bossphase = 1;
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x01
00126$:
;src/game.c:277: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
	ld	a,(#_g_player + 0)
	ld	-2 (ix), a
	ld	-2 (ix), a
	ld	-1 (ix), #0x00
	ld	a, -2 (ix)
	add	a, #0x02
	ld	-2 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-1 (ix), a
	ld	hl, #_g_boss + 0
	ld	c, (hl)
	ld	b, #0x00
	ld	a, -2 (ix)
	sub	a, c
	ld	a, -1 (ix)
	sbc	a, b
	jp	PO, 00425$
	xor	a, #0x80
00425$:
	jp	P, 00197$
	ld	a,(#_g_bossphase + 0)
	or	a, a
	jr	Z,00199$
	ld	c, #0x02
	jr	00200$
00199$:
	ld	c, #0x01
00200$:
	xor	a, a
	sub	a, c
	ld	c, a
	jr	00198$
00197$:
	ld	a,(#_g_bossphase + 0)
	or	a, a
	jr	Z,00201$
	ld	c, #0x02
	jr	00202$
00201$:
	ld	c, #0x01
00202$:
00198$:
	ld	hl, #(_g_boss + 0x0002)
	ld	(hl), c
;src/game.c:278: enemyupdate(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyupdate
	pop	af
;src/game.c:281: for (i = 0; i < MAX_PROJECTILES; ++i) {
00234$:
	ld	c, #0x00
00193$:
;src/game.c:282: if (!g_projectiles[i].active) continue;
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ex	de,hl
	ld	hl, #_g_projectiles
	add	hl,de
	ex	de,hl
	ld	hl, #0x0006
	add	hl,de
	ld	-2 (ix), l
	ld	-1 (ix), h
	ld	a, (hl)
	or	a, a
	jp	Z, 00147$
;src/game.c:283: for (j = 0; j < MAX_ENEMIES; ++j) {
	ld	-25 (ix), #0x00
00192$:
;src/game.c:284: if (!g_enemies[j].active) continue;
	push	de
	ld	e,-25 (ix)
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	ld	a, #<(_g_enemies)
	add	a, l
	ld	-4 (ix), a
	ld	a, #>(_g_enemies)
	adc	a, h
	ld	-3 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	push	bc
	ld	bc, #0x0006
	add	hl, bc
	pop	bc
	ld	b, (hl)
;src/game.c:285: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	hl, #0x0005
	add	hl,de
	ld	-6 (ix), l
	ld	-5 (ix), h
	ld	hl, #0x0004
	add	hl,de
	ld	-8 (ix), l
	ld	-7 (ix), h
	ld	hl, #0x0001
	add	hl,de
	ld	-10 (ix), l
	ld	-9 (ix), h
;src/game.c:287: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
	ld	hl, #0x0007
	add	hl,de
	ld	-12 (ix), l
	ld	-11 (ix), h
;src/game.c:284: if (!g_enemies[j].active) continue;
	ld	a, b
	or	a, a
	jp	Z, 00139$
;src/game.c:286: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	-13 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	-14 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	inc	hl
	ld	b, (hl)
	ld	-16 (ix), b
	ld	-15 (ix), #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	b, (hl)
	ld	-18 (ix), b
	ld	-17 (ix), #0x00
;src/game.c:285: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	ld	-19 (ix), a
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	b, (hl)
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	l, (hl)
	ld	-21 (ix), l
	ld	-20 (ix), #0x00
	ld	a, (de)
	ld	-23 (ix), a
	ld	-22 (ix), #0x00
	push	bc
	push	de
	ld	h, -13 (ix)
	ld	l, -14 (ix)
	push	hl
	ld	l,-16 (ix)
	ld	h,-15 (ix)
	push	hl
	ld	l,-18 (ix)
	ld	h,-17 (ix)
	push	hl
	ld	a, -19 (ix)
	push	af
	inc	sp
	push	bc
	inc	sp
	ld	l,-21 (ix)
	ld	h,-20 (ix)
	push	hl
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	pop	de
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00139$
;src/game.c:287: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	h, (hl)
	ld	l, -4 (ix)
	ld	b, -3 (ix)
	push	bc
	push	de
	push	hl
	inc	sp
	ld	h, b
	push	hl
	call	_enemydamage
	pop	af
	inc	sp
	pop	de
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00138$
;src/game.c:288: g_score = (u16)(g_score + g_enemies[j].reward);
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	push	bc
	ld	bc, #0x0008
	add	hl, bc
	pop	bc
	ld	l, (hl)
	ld	-23 (ix), l
	ld	-22 (ix), #0x00
	ld	hl, #_g_score
	ld	a, (hl)
	add	a, -23 (ix)
	ld	(hl), a
	inc	hl
	ld	a, (hl)
	adc	a, -22 (ix)
	ld	(hl), a
;src/game.c:289: if (g_aliveenemies) g_aliveenemies--;
	ld	iy, #_g_aliveenemies
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00138$
	dec	0 (iy)
00138$:
;src/game.c:291: g_projectiles[i].active = 0;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x00
;src/game.c:292: break;
	jr	00140$
00139$:
;src/game.c:283: for (j = 0; j < MAX_ENEMIES; ++j) {
	inc	-25 (ix)
	ld	a, -25 (ix)
	sub	a, #0x06
	jp	C, 00192$
00140$:
;src/game.c:295: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jp	Z, 00147$
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	a, (hl)
	or	a, a
	jp	Z, 00147$
;src/game.c:296: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
	ld	hl, #(_g_boss + 0x0005) + 0
	ld	b, (hl)
	ld	a, (#(_g_boss + 0x0004) + 0)
	ld	hl, #(_g_boss + 0x0001) + 0
	ld	l, (hl)
	ld	-23 (ix), l
	ld	-22 (ix), #0x00
	ld	hl, #_g_boss + 0
	ld	l, (hl)
	ld	-21 (ix), l
	ld	-20 (ix), #0x00
;src/game.c:295: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	push	af
	ld	a, (hl)
	ld	-19 (ix), a
	pop	af
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	push	af
	ld	a, (hl)
	ld	-18 (ix), a
	pop	af
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	l, (hl)
	ld	-16 (ix), l
	ld	-15 (ix), #0x00
	push	af
	ld	a, (de)
	ld	e, a
	pop	af
	ld	d, #0x00
	push	bc
	push	bc
	inc	sp
	push	af
	inc	sp
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	push	hl
	ld	l,-21 (ix)
	ld	h,-20 (ix)
	push	hl
	ld	h, -19 (ix)
	ld	l, -18 (ix)
	push	hl
	ld	l,-16 (ix)
	ld	h,-15 (ix)
	push	hl
	push	de
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00147$
;src/game.c:297: g_projectiles[i].active = 0;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x00
;src/game.c:298: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	b, (hl)
	ld	de, #_g_boss
	push	bc
	push	bc
	inc	sp
	push	de
	call	_enemydamage
	pop	af
	inc	sp
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00147$
;src/game.c:299: g_bossactive = 0;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x00
;src/game.c:300: g_score = (u16)(g_score + g_boss.reward);
	ld	hl, #_g_boss + 8
	ld	e, (hl)
	ld	d, #0x00
	ld	hl, #_g_score
	ld	a, (hl)
	add	a, e
	ld	(hl), a
	inc	hl
	ld	a, (hl)
	adc	a, d
	ld	(hl), a
;src/game.c:301: g_victory = 1;
	ld	hl,#_g_victory + 0
	ld	(hl), #0x01
00147$:
;src/game.c:281: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jp	C, 00193$
;src/game.c:306: lives_before_damage = g_lives;
	ld	a,(#_g_lives + 0)
	ld	-28 (ix), a
;src/game.c:308: for (i = 0; i < MAX_ENEMIES; ++i) {
;src/game.c:307: if (!g_damagecooldown) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jp	NZ, 00163$
;src/game.c:308: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	-24 (ix), #0x00
00194$:
;src/game.c:309: if (!g_enemies[i].active) continue;
	ld	c,-24 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	bc,#_g_enemies
	add	hl,bc
	ld	-23 (ix), l
	ld	-22 (ix), h
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
	jp	Z, 00153$
;src/game.c:311: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
	ld	a, -23 (ix)
	ld	-21 (ix), a
	ld	a, -22 (ix)
	ld	-20 (ix), a
	ld	l,-21 (ix)
	ld	h,-20 (ix)
	ld	de, #0x0005
	add	hl, de
	ld	a, (hl)
	ld	-21 (ix), a
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	ld	de, #0x0004
	add	hl, de
	ld	e, (hl)
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	inc	hl
	ld	c, (hl)
	ld	b, #0x00
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	ld	d, (hl)
	ld	-23 (ix), d
	ld	-22 (ix), #0x00
;src/game.c:310: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#(_g_player + 0x0005) + 0)
	ld	-19 (ix), a
	ld	a,(#(_g_player + 0x0004) + 0)
	ld	-18 (ix), a
	ld	a, (#(_g_player + 0x0001) + 0)
	ld	-16 (ix), a
	ld	-15 (ix), #0x00
	ld	a, (#_g_player + 0)
	ld	-12 (ix), a
	ld	-11 (ix), #0x00
	ld	d, -21 (ix)
	push	de
	push	bc
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	push	hl
	ld	h, -19 (ix)
	ld	l, -18 (ix)
	push	hl
	ld	l,-16 (ix)
	ld	h,-15 (ix)
	push	hl
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	ld	a, l
	or	a, a
	jr	Z,00153$
;src/game.c:312: register_player_hit();
	call	_register_player_hit
;src/game.c:313: break;
	jr	00154$
00153$:
;src/game.c:308: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-24 (ix)
	ld	a, -24 (ix)
	sub	a, #0x06
	jp	C, 00194$
00154$:
;src/game.c:317: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jr	NZ,00156$
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00156$
;src/game.c:318: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
	ld	a,(#(_g_boss + 0x0005) + 0)
	ld	-23 (ix), a
	ld	a,(#(_g_boss + 0x0004) + 0)
	ld	-21 (ix), a
	ld	hl, #(_g_boss + 0x0001) + 0
	ld	e, (hl)
	ld	d, #0x00
	ld	hl, #_g_boss + 0
	ld	c, (hl)
	ld	b, #0x00
;src/game.c:317: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#(_g_player + 0x0005) + 0)
	ld	-19 (ix), a
	ld	a,(#(_g_player + 0x0004) + 0)
	ld	-18 (ix), a
	ld	a, (#(_g_player + 0x0001) + 0)
	ld	-16 (ix), a
	ld	-15 (ix), #0x00
	ld	a, (#_g_player + 0)
	ld	-12 (ix), a
	ld	-11 (ix), #0x00
	ld	h, -23 (ix)
	ld	l, -21 (ix)
	push	hl
	push	de
	push	bc
	ld	h, -19 (ix)
	ld	l, -18 (ix)
	push	hl
	ld	l,-16 (ix)
	ld	h,-15 (ix)
	push	hl
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	ld	a, l
	or	a, a
	jr	Z,00156$
;src/game.c:319: register_player_hit();
	call	_register_player_hit
00156$:
;src/game.c:322: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jr	NZ,00163$
	ld	a, (#(_g_player + 0x0005) + 0)
	ld	hl, #(_g_player + 0x0004) + 0
	ld	d, (hl)
	ld	hl, #(_g_player + 0x0001) + 0
	ld	c, (hl)
	ld	b, #0x00
	ld	hl, #_g_player + 0
	ld	l, (hl)
	ld	-23 (ix), l
	ld	-22 (ix), #0x00
	push	af
	inc	sp
	push	de
	inc	sp
	push	bc
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	push	hl
	call	_collision_is_on_trap
	pop	af
	pop	af
	pop	af
	ld	a, l
	or	a, a
	jr	Z,00163$
;src/game.c:323: register_player_hit();
	call	_register_player_hit
00163$:
;src/game.c:327: g_dbg_move_raw = (u8)(player_x_after_move != player_x_start);
	ld	a, -26 (ix)
	sub	a, -27 (ix)
	jr	NZ,00426$
	ld	a,#0x01
	jr	00427$
00426$:
	xor	a,a
00427$:
	xor	a, #0x01
	ld	c, a
	ld	hl,#_g_dbg_move_raw + 0
	ld	(hl), c
;src/game.c:258: player_x_after_move = g_player.x;
	ld	hl, #_g_player + 0
	ld	c, (hl)
;src/game.c:328: g_dbg_move_net = (u8)(g_player.x != player_x_start);
	ld	a, c
	sub	a, -26 (ix)
	jr	NZ,00428$
	ld	a,#0x01
	jr	00429$
00428$:
	xor	a,a
00429$:
	xor	a, #0x01
	ld	b, a
	ld	hl,#_g_dbg_move_net + 0
	ld	(hl), b
;src/game.c:329: g_dbg_move_cancelled = (u8)(g_dbg_move_raw && !g_dbg_move_net);
	ld	a,(#_g_dbg_move_raw + 0)
	or	a, a
	jr	Z,00203$
	ld	a,(#_g_dbg_move_net + 0)
	or	a, a
	jr	Z,00204$
00203$:
	ld	b, #0x00
	jr	00205$
00204$:
	ld	b, #0x01
00205$:
	ld	hl,#_g_dbg_move_cancelled + 0
	ld	(hl), b
;src/game.c:330: g_dbg_hit = (u8)(g_lives < lives_before_damage);
	ld	hl, #_g_dbg_hit
	ld	a,(#_g_lives + 0)
	sub	a, -28 (ix)
	ld	a, #0x00
	rla
	ld	(hl), a
;src/game.c:332: if (!g_checkpointactive && g_player.x >= 44) {
	ld	iy, #_g_checkpointactive
	ld	a, 0 (iy)
	or	a, a
	jr	NZ,00165$
	ld	a, c
	sub	a, #0x2c
	jr	C,00165$
;src/game.c:333: g_checkpointactive = 1;
	ld	0 (iy), #0x01
;src/game.c:334: g_checkpointx = 52;
	ld	hl,#_g_checkpointx + 0
	ld	(hl), #0x34
;src/game.c:335: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
	call	_tilemap_ground_y
	ld	c, l
	ld	hl, #(_g_player + 0x0005) + 0
	ld	b, (hl)
	ld	hl, #_g_checkpointy
	ld	a, c
	sub	a, b
	ld	(hl), a
00165$:
;src/game.c:338: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
	ld	a,(#_g_pickuptaken + 0)
	or	a, a
	jp	NZ, 00168$
	call	_tilemap_ground_y
	ld	-23 (ix), l
	ld	-23 (ix), l
	ld	-22 (ix), #0x00
	ld	a, -23 (ix)
	add	a, #0xf8
	ld	-23 (ix), a
	ld	a, -22 (ix)
	adc	a, #0xff
	ld	-22 (ix), a
	ld	a,(#(_g_player + 0x0005) + 0)
	ld	-21 (ix), a
	ld	a,(#(_g_player + 0x0004) + 0)
	ld	-19 (ix), a
	ld	a,(#(_g_player + 0x0001) + 0)
	ld	-18 (ix), a
	ld	-18 (ix), a
	ld	-17 (ix), #0x00
	ld	a,(#_g_player + 0)
	ld	-16 (ix), a
	ld	-16 (ix), a
	ld	-15 (ix), #0x00
	ld	hl, #0x0404
	push	hl
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	push	hl
	ld	hl, #0x0024
	push	hl
	ld	h, -21 (ix)
	ld	l, -19 (ix)
	push	hl
	ld	l,-18 (ix)
	ld	h,-17 (ix)
	push	hl
	ld	l,-16 (ix)
	ld	h,-15 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	ld	a, l
	or	a, a
	jr	Z,00168$
;src/game.c:339: g_pickuptaken = 1;
	ld	hl,#_g_pickuptaken + 0
	ld	(hl), #0x01
;src/game.c:340: g_weaponlevel = 1;
	ld	hl,#_g_weaponlevel + 0
	ld	(hl), #0x01
;src/game.c:341: g_score = (u16)(g_score + 100);
	ld	hl, #_g_score
	ld	a, (hl)
	add	a, #0x64
	ld	(hl), a
	inc	hl
	ld	a, (hl)
	adc	a, #0x00
	ld	(hl), a
00168$:
;src/game.c:344: g_weapondisplay = (u8)(g_weaponlevel + 1);
	ld	hl, #_g_weapondisplay
	ld	a,(#_g_weaponlevel + 0)
	inc	a
	ld	(hl), a
;src/game.c:346: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	NZ,00179$
	ld	a,(#_g_aliveenemies + 0)
	or	a, a
	jr	NZ,00179$
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	NZ,00179$
;src/game.c:347: if (g_currentwave < TOTAL_WAVES) {
	ld	a,(#_g_currentwave + 0)
	sub	a, #0x03
	jr	NC,00176$
;src/game.c:348: if (g_wavecooldown == 0) {
	ld	a,(#_g_wavecooldown + 0)
	or	a, a
	jr	NZ,00171$
;src/game.c:349: spawn_wave(g_currentwave);
	ld	a, (_g_currentwave)
	push	af
	inc	sp
	call	_spawn_wave
	inc	sp
;src/game.c:350: g_currentwave++;
	ld	hl, #_g_currentwave+0
	inc	(hl)
;src/game.c:351: g_wavecooldown = 90;
	ld	hl,#_g_wavecooldown + 0
	ld	(hl), #0x5a
	jr	00179$
00171$:
;src/game.c:353: g_wavecooldown--;
	ld	hl, #_g_wavecooldown+0
	dec	(hl)
	jr	00179$
00176$:
;src/game.c:355: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
	ld	hl, #_g_player + 0
	ld	c, (hl)
	push	bc
	call	_tilemap_goal_x
	pop	bc
	dec	l
	dec	l
	ld	a, c
	sub	a, l
	jr	C,00179$
;src/game.c:356: spawn_boss();
	call	_spawn_boss
00179$:
;src/game.c:360: g_framecounter++;
	ld	iy, #_g_framecounter
	inc	0 (iy)
	jr	NZ,00430$
	inc	1 (iy)
00430$:
;src/game.c:361: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
	ld	hl, #0x0032
	push	hl
	ld	hl, (_g_framecounter)
	push	hl
	call	__moduint
	pop	af
	pop	af
	ld	a, h
	or	a,l
	jr	NZ,00183$
	ld	iy, #_g_timeleft
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00183$
;src/game.c:362: g_timeleft--;
	dec	0 (iy)
00183$:
;src/game.c:364: if (g_timeleft == 0 && !g_victory) {
	ld	a,(#_g_timeleft + 0)
	or	a, a
	jr	NZ,00186$
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	NZ,00186$
;src/game.c:365: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
00186$:
;src/game.c:368: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
	ld	a, (_g_weapondisplay)
	push	af
	inc	sp
	ld	a, (_g_timeleft)
	push	af
	inc	sp
	ld	hl, (_g_score)
	push	hl
	ld	a, (_g_lives)
	push	af
	inc	sp
	call	_hudupdate
	pop	af
	pop	af
	inc	sp
00195$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:371: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	dec	sp
;src/game.c:378: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_player_x, prev_player_y);
	ld	a, (_prev_player_y)
	push	af
	inc	sp
	ld	a, (_prev_player_x)
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	c, l
	ld	b, h
;src/game.c:379: cpct_drawSolidBox(pvmem, 0x00, g_player.w, g_player.h);
	ld	hl, #_g_player + 5
	ld	d, (hl)
	ld	a, (#_g_player + 4)
	ld	e, a
	push	de
	xor	a, a
	push	af
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/game.c:382: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	-3 (ix), #0x00
00129$:
;src/game.c:383: if (prev_enemy_act[i]) {
	ld	a, #<(_prev_enemy_act)
	add	a, -3 (ix)
	ld	c, a
	ld	a, #>(_prev_enemy_act)
	adc	a, #0x00
	ld	b, a
	ld	a, (bc)
	or	a, a
	jr	Z,00130$
;src/game.c:384: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_enemy_x[i], prev_enemy_y[i]);
	ld	a, #<(_prev_enemy_y)
	add	a, -3 (ix)
	ld	-2 (ix), a
	ld	a, #>(_prev_enemy_y)
	adc	a, #0x00
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	c, (hl)
	ld	a, -3 (ix)
	add	a, #<(_prev_enemy_x)
	ld	-2 (ix), a
	ld	a, #0x00
	adc	a, #>(_prev_enemy_x)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	b, (hl)
	ld	a, c
	push	af
	inc	sp
	push	bc
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	c, l
	ld	b, h
;src/game.c:385: cpct_drawSolidBox(pvmem, 0x00, prev_enemy_w[i], prev_enemy_h[i]);
	ld	a, #<(_prev_enemy_h)
	add	a, -3 (ix)
	ld	l, a
	ld	a, #>(_prev_enemy_h)
	adc	a, #0x00
	ld	h, a
	ld	a, (hl)
	ld	-2 (ix), a
	ld	a, #<(_prev_enemy_w)
	add	a, -3 (ix)
	ld	l, a
	ld	a, #>(_prev_enemy_w)
	adc	a, #0x00
	ld	h, a
	ld	e, (hl)
	ld	d, -2 (ix)
	push	de
	xor	a, a
	push	af
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00130$:
;src/game.c:382: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-3 (ix)
	ld	a, -3 (ix)
	sub	a, #0x06
	jr	C,00129$
;src/game.c:390: if (prev_boss_act) {
	ld	a,(#_prev_boss_act + 0)
	or	a, a
	jr	Z,00164$
;src/game.c:391: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_boss_x, prev_boss_y);
	ld	a, (_prev_boss_y)
	push	af
	inc	sp
	ld	a, (_prev_boss_x)
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	c, l
	ld	b, h
;src/game.c:392: cpct_drawSolidBox(pvmem, 0x00, g_boss.w, g_boss.h);
	ld	hl, #_g_boss + 5
	ld	d, (hl)
	ld	a, (#_g_boss + 4)
	ld	e, a
	push	de
	xor	a, a
	push	af
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/game.c:396: for (i = 0; i < MAX_PROJECTILES; ++i) {
00164$:
	ld	bc, #_prev_proj_act+0
	ld	e, #0x00
00131$:
;src/game.c:397: if (prev_proj_act[i]) {
	ld	l,e
	ld	h,#0x00
	add	hl, bc
	ld	a, (hl)
	or	a, a
	jr	Z,00132$
;src/game.c:398: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_proj_x[i], prev_proj_y[i]);
	ld	hl, #_prev_proj_y
	ld	d, #0x00
	add	hl, de
	ld	d, (hl)
	ld	a, #<(_prev_proj_x)
	add	a, e
	ld	l, a
	ld	a, #>(_prev_proj_x)
	adc	a, #0x00
	ld	h, a
	ld	a, (hl)
	push	bc
	push	de
	ld	e, a
	push	de
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
;src/game.c:399: cpct_drawSolidBox(pvmem, 0x00, prev_proj_w[i], prev_proj_h[i]);
	ld	hl, #_prev_proj_h
	ld	d, #0x00
	add	hl, de
	ld	a, (hl)
	ld	-2 (ix), a
	ld	hl, #_prev_proj_w
	ld	d, #0x00
	add	hl, de
	ld	d, (hl)
	push	bc
	push	de
	ld	a, -2 (ix)
	push	af
	inc	sp
	push	de
	inc	sp
	xor	a, a
	push	af
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	de
	pop	bc
00132$:
;src/game.c:396: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00131$
;src/game.c:404: tilemap_render();
	push	bc
	call	_tilemap_render
	ld	hl, #_g_player
	push	hl
	call	_playerrender
	pop	af
	pop	bc
;src/game.c:410: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	e, #0x00
00133$:
;src/game.c:411: projectilerender(&g_projectiles[i]);
	push	de
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	push	bc
	ld	bc, #_g_projectiles
	add	hl, bc
	push	de
	push	hl
	call	_projectilerender
	pop	af
	pop	de
	pop	bc
;src/game.c:410: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00133$
;src/game.c:414: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	e, #0x00
00135$:
;src/game.c:415: enemyrender(&g_enemies[i]);
	push	de
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	push	bc
	ld	bc, #_g_enemies
	add	hl, bc
	push	de
	push	hl
	call	_enemyrender
	pop	af
	pop	de
	pop	bc
;src/game.c:414: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00135$
;src/game.c:418: if (g_bossactive) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00112$
;src/game.c:419: enemyrender(&g_boss);
	push	bc
	ld	hl, #_g_boss
	push	hl
	call	_enemyrender
	ld	hl, #0x0101
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x0a18
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0220
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:421: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
	ld	a, (#_g_boss + 7)
	ld	e, a
	add	a, a
	add	a, e
	ld	d, a
	push	bc
	push	de
	ld	hl, #0x0505
	push	hl
	call	_cpct_px2byteM0
	ld	e, l
	pop	af
	ld	d, a
	push	de
	ld	hl, #0x0a18
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	a, #0x02
	push	af
	inc	sp
	push	de
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
00112$:
;src/game.c:424: if (!g_pickuptaken) {
	ld	a,(#_g_pickuptaken + 0)
	or	a, a
	jr	NZ,00114$
;src/game.c:425: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
	push	bc
	ld	hl, #0x0707
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	call	_tilemap_ground_y
	pop	de
	pop	bc
	ld	a, l
	add	a, #0xf8
	ld	h, a
	push	bc
	push	de
	push	hl
	inc	sp
	ld	a, #0x24
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0404
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
00114$:
;src/game.c:428: hudrender();
	push	bc
	call	_hudrender
	pop	bc
;src/game.c:430: if (g_victory) {
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	Z,00121$
;src/game.c:431: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
	push	bc
	ld	hl, #0x0808
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x4418
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0c20
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0505
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x481c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0818
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
	jp	00122$
00121$:
;src/game.c:433: } else if (g_gameover) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	Z,00118$
;src/game.c:434: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
	push	bc
	ld	hl, #0x0101
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x4418
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0c20
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0606
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x481c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0818
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
	jr	00122$
00118$:
;src/game.c:436: } else if (g_checkpointactive) {
	ld	a,(#_g_checkpointactive + 0)
	or	a, a
	jr	Z,00122$
;src/game.c:437: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
	push	bc
	ld	hl, #0x0909
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	ld	a,(#_g_checkpointy + 0)
	add	a, #0xf8
	push	bc
	push	de
	push	af
	inc	sp
	ld	a, (_g_checkpointx)
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0802
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
00122$:
;src/game.c:441: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 0, 0), cpct_px2byteM0(0, 0), 40, 2);
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x0000
	push	hl
	ld	h, #0xc0
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0228
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0606
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	ld	hl, #_g_player + 0
	ld	h, (hl)
	push	bc
	push	de
	xor	a, a
	push	af
	inc	sp
	push	hl
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0000
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x0200
	push	hl
	ld	h, #0xc0
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0228
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:447: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  0, 2), g_dbg_left           ? cpct_px2byteM0(2, 2)   : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_left + 0)
	or	a, a
	jr	Z,00143$
	push	bc
	ld	hl, #0x0202
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00144$
00143$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00144$:
	push	bc
	push	de
	ld	hl, #0x0200
	push	hl
	ld	h, #0xc0
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:448: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  4, 2), g_dbg_right          ? cpct_px2byteM0(14, 14) : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_right + 0)
	or	a, a
	jr	Z,00145$
	push	bc
	ld	hl, #0x0e0e
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00146$
00145$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00146$:
	push	bc
	push	de
	ld	hl, #0x0204
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:449: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  8, 2), g_dbg_jump           ? cpct_px2byteM0(3, 3)   : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_jump + 0)
	or	a, a
	jr	Z,00147$
	push	bc
	ld	hl, #0x0303
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00148$
00147$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00148$:
	push	bc
	push	de
	ld	hl, #0x0208
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:450: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 12, 2), g_dbg_shoot          ? cpct_px2byteM0(6, 6)   : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_shoot + 0)
	or	a, a
	jr	Z,00149$
	push	bc
	ld	hl, #0x0606
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00150$
00149$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00150$:
	push	bc
	push	de
	ld	hl, #0x020c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:451: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 16, 2), g_dbg_move_raw       ? cpct_px2byteM0(7, 7)   : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_move_raw + 0)
	or	a, a
	jr	Z,00151$
	push	bc
	ld	hl, #0x0707
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00152$
00151$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00152$:
	push	bc
	push	de
	ld	hl, #0x0210
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:452: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 20, 2), g_dbg_move_net       ? cpct_px2byteM0(9, 9)   : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_move_net + 0)
	or	a, a
	jr	Z,00153$
	push	bc
	ld	hl, #0x0909
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00154$
00153$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00154$:
	push	bc
	push	de
	ld	hl, #0x0214
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:453: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 2), g_dbg_move_cancelled ? cpct_px2byteM0(12, 12) : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_move_cancelled + 0)
	or	a, a
	jr	Z,00155$
	push	bc
	ld	hl, #0x0c0c
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00156$
00155$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00156$:
	push	bc
	push	de
	ld	hl, #0x0218
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:454: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 2), g_dbg_hit            ? cpct_px2byteM0(15, 15) : cpct_px2byteM0(0, 0), 4, 2);
	ld	a,(#_g_dbg_hit + 0)
	or	a, a
	jr	Z,00157$
	push	bc
	ld	hl, #0x0f0f
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	jr	00158$
00157$:
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
00158$:
	push	bc
	push	de
	ld	hl, #0x021c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0204
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0000
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x0400
	push	hl
	ld	h, #0xc0
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0228
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0505
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	ld	hl, #0x0414
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0201
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:459: vx_mark_x = (i16)20 + ((i16)g_dbg_vx * 2);
	ld	iy, #_g_dbg_vx
	ld	l, 0 (iy)
	ld	a, 0 (iy)
	rla
	sbc	a, a
	ld	h, a
	add	hl, hl
	ld	de, #0x0014
	add	hl, de
;src/game.c:460: if (vx_mark_x < 0) vx_mark_x = 0;
	bit	7, h
	jr	Z,00124$
	ld	hl, #0x0000
00124$:
;src/game.c:461: if (vx_mark_x > 39) vx_mark_x = 39;
	ld	a, #0x27
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jp	PO, 00281$
	xor	a, #0x80
00281$:
	jp	P, 00126$
	ld	hl, #0x0027
00126$:
;src/game.c:462: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, (u8)vx_mark_x, 4), cpct_px2byteM0(10, 10), 1, 2);
	push	hl
	push	bc
	ld	de, #0x0a0a
	push	de
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	pop	hl
	ld	h, l
	push	bc
	push	de
	ld	a, #0x04
	push	af
	inc	sp
	push	hl
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
	push	hl
	pop	iy
	push	bc
	ld	hl, #0x0201
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/game.c:465: prev_player_x = g_player.x;
	ld	a,(#_g_player + 0)
	ld	(#_prev_player_x + 0),a
;src/game.c:466: prev_player_y = g_player.y;
	ld	a,(#_g_player + 1)
	ld	(#_prev_player_y + 0),a
;src/game.c:468: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	-3 (ix), #0x00
00137$:
;src/game.c:469: prev_enemy_act[i] = g_enemies[i].active;
	ld	a, #<(_prev_enemy_act)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_enemy_act)
	adc	a, #0x00
	ld	d, a
	push	de
	ld	e,-3 (ix)
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	ld	iy, #_g_enemies
	push	bc
	ld	c, l
	ld	b, h
	add	iy, bc
	pop	bc
	push	iy
	pop	hl
	push	bc
	ld	bc, #0x0006
	add	hl, bc
	pop	bc
	ld	a, (hl)
	ld	(de), a
;src/game.c:470: prev_enemy_x[i]   = g_enemies[i].x;
	ld	a, #<(_prev_enemy_x)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_enemy_x)
	adc	a, #0x00
	ld	d, a
	ld	a, 0 (iy)
	ld	(de), a
;src/game.c:471: prev_enemy_y[i]   = g_enemies[i].y;
	ld	a, #<(_prev_enemy_y)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_enemy_y)
	adc	a, #0x00
	ld	d, a
	push	iy
	pop	hl
	inc	hl
	ld	a, (hl)
	ld	(de), a
;src/game.c:472: prev_enemy_w[i]   = g_enemies[i].w;
	ld	a, #<(_prev_enemy_w)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_enemy_w)
	adc	a, #0x00
	ld	d, a
	push	iy
	pop	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	(de), a
;src/game.c:473: prev_enemy_h[i]   = g_enemies[i].h;
	ld	a, #<(_prev_enemy_h)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_enemy_h)
	adc	a, #0x00
	ld	d, a
	ld	a, 5 (iy)
	ld	(de), a
;src/game.c:468: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-3 (ix)
	ld	a, -3 (ix)
	sub	a, #0x06
	jr	C,00137$
;src/game.c:476: prev_boss_act = g_bossactive;
	ld	a,(#_g_bossactive + 0)
	ld	(#_prev_boss_act + 0),a
;src/game.c:477: prev_boss_x   = g_boss.x;
	ld	a, (#_g_boss+0)
	ld	(#_prev_boss_x + 0),a
;src/game.c:478: prev_boss_y   = g_boss.y;
	ld	a, (#_g_boss+1)
	ld	(#_prev_boss_y + 0),a
;src/game.c:480: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	-3 (ix), #0x00
00139$:
;src/game.c:481: prev_proj_act[i] = g_projectiles[i].active;
	ld	a, -3 (ix)
	add	a, c
	ld	e, a
	ld	a, #0x00
	adc	a, b
	ld	d, a
	push	de
	ld	e,-3 (ix)
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, de
	add	hl, hl
	pop	de
	ld	iy, #_g_projectiles
	push	bc
	ld	c, l
	ld	b, h
	add	iy, bc
	pop	bc
	push	iy
	pop	hl
	push	bc
	ld	bc, #0x0006
	add	hl, bc
	pop	bc
	ld	a, (hl)
	ld	(de), a
;src/game.c:482: prev_proj_x[i]   = g_projectiles[i].x;
	ld	a, #<(_prev_proj_x)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_proj_x)
	adc	a, #0x00
	ld	d, a
	ld	a, 0 (iy)
	ld	(de), a
;src/game.c:483: prev_proj_y[i]   = g_projectiles[i].y;
	ld	a, #<(_prev_proj_y)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_proj_y)
	adc	a, #0x00
	ld	d, a
	push	iy
	pop	hl
	inc	hl
	ld	a, (hl)
	ld	(de), a
;src/game.c:484: prev_proj_w[i]   = g_projectiles[i].w;
	ld	a, #<(_prev_proj_w)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_proj_w)
	adc	a, #0x00
	ld	d, a
	push	iy
	pop	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	(de), a
;src/game.c:485: prev_proj_h[i]   = g_projectiles[i].h;
	ld	a, #<(_prev_proj_h)
	add	a, -3 (ix)
	ld	e, a
	ld	a, #>(_prev_proj_h)
	adc	a, #0x00
	ld	d, a
	ld	a, 5 (iy)
	ld	(de), a
;src/game.c:480: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	-3 (ix)
	ld	a, -3 (ix)
	sub	a, #0x06
	jr	C,00139$
	ld	sp, ix
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
__xinit__prev_player_x:
	.db #0x04	; 4
__xinit__prev_player_y:
	.db #0x68	; 104	'h'
	.area _CABS (ABS)
