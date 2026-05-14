;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module game
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
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
	.globl _input_update
	.globl _tilemap_goal_x
	.globl _tilemap_is_hidden_zone
	.globl _tilemap_render
	.globl _tilemap_init
	.globl _cpct_getScreenPtr
	.globl _cpct_setVideoMode
	.globl _cpct_drawSolidBox
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
_g_lives:
	.ds 1
_g_score:
	.ds 2
_g_timeleft:
	.ds 1
_g_weaponlevel:
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
_g_hiddenrewardtaken:
	.ds 1
_g_boss:
	.ds 10
_g_bossactive:
	.ds 1
_g_bossphase:
	.ds 1
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _INITIALIZED
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
;src/game.c:40: static void reset_player_to_checkpoint(void) {
;	---------------------------------
; Function reset_player_to_checkpoint
; ---------------------------------
_reset_player_to_checkpoint:
;src/game.c:41: g_player.x = g_checkpointx;
	ld	hl, #_g_player
	ld	a,(#_g_checkpointx + 0)
	ld	(hl), a
;src/game.c:42: g_player.y = g_checkpointy;
	ld	hl, #(_g_player + 0x0001)
	ld	a,(#_g_checkpointy + 0)
	ld	(hl), a
;src/game.c:43: g_player.vx = 0;
	ld	hl, #(_g_player + 0x0002)
	ld	(hl), #0x00
;src/game.c:44: g_player.vy = 0;
	ld	hl, #(_g_player + 0x0003)
	ld	(hl), #0x00
	ret
;src/game.c:47: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
;	---------------------------------
; Function rect_overlap
; ---------------------------------
_rect_overlap:
	push	ix
	ld	ix,#0
	add	ix,sp
;src/game.c:48: if (ax + aw <= bx) return 0;
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
;src/game.c:49: if (bx + bw <= ax) return 0;
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
;src/game.c:50: if (ay + ah <= by) return 0;
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
;src/game.c:51: if (by + bh <= ay) return 0;
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
;src/game.c:52: return 1;
	ld	l, #0x01
00109$:
	pop	ix
	ret
;src/game.c:55: static void spawn_wave(u8 wave) {
;	---------------------------------
; Function spawn_wave
; ---------------------------------
_spawn_wave:
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	push	af
;src/game.c:59: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	bc, #_g_enemies+0
	ld	e, #0x00
00117$:
;src/game.c:60: enemyinit(&g_enemies[i]);
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
;src/game.c:59: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00117$
;src/game.c:64: else if (wave == 1) count = 3;
	ld	a, 4 (ix)
	dec	a
	jr	NZ,00174$
	ld	a,#0x01
	jr	00175$
00174$:
	xor	a,a
00175$:
	ld	e, a
;src/game.c:63: if (wave == 0) count = 2;
	ld	a, 4 (ix)
	or	a, a
	jr	NZ,00106$
	ld	-4 (ix), #0x02
	jr	00107$
00106$:
;src/game.c:64: else if (wave == 1) count = 3;
	ld	a, e
	or	a, a
	jr	Z,00103$
	ld	-4 (ix), #0x03
	jr	00107$
00103$:
;src/game.c:65: else count = 4;
	ld	-4 (ix), #0x04
00107$:
;src/game.c:67: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
	ld	a, #0x06
	sub	a, -4 (ix)
	jr	NC,00138$
	ld	-4 (ix), #0x06
;src/game.c:69: for (i = 0; i < count; ++i) {
00138$:
	ld	-1 (ix), e
	ld	e, #0x00
00120$:
	ld	a, e
	sub	a, -4 (ix)
	jr	NC,00116$
;src/game.c:72: else if (wave == 1) type = (u8)(i & 1);
	ld	a, e
	and	a, #0x01
	ld	l, a
;src/game.c:71: if (wave == 0) type = 0;
	ld	a, 4 (ix)
	or	a,a
	jr	NZ,00114$
	ld	d,a
	jr	00115$
00114$:
;src/game.c:72: else if (wave == 1) type = (u8)(i & 1);
	ld	a, -1 (ix)
	or	a, a
	jr	Z,00111$
	ld	d, l
	jr	00115$
00111$:
;src/game.c:73: else type = (u8)((i == 0) ? 2 : (i & 1));
	ld	a, e
	or	a, a
	jr	NZ,00124$
	ld	d, #0x02
	jr	00125$
00124$:
	ld	d, l
00125$:
00115$:
;src/game.c:74: enemyspawn(&g_enemies[i], (u8)(48 + (i * 10)), 112, type, (u8)((i & 1) ? 1 : 0));
	ld	a, l
	or	a, a
	jr	Z,00126$
	ld	-2 (ix), #0x01
	jr	00127$
00126$:
	ld	-2 (ix), #0x00
00127$:
	push	de
	ld	a, e
	add	a, a
	add	a, a
	add	a, e
	add	a, a
	pop	de
	add	a, #0x30
	ld	-3 (ix), a
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
	ld	a, -2 (ix)
	push	af
	inc	sp
	ld	e, #0x70
	push	de
	ld	a, -3 (ix)
	push	af
	inc	sp
	push	iy
	call	_enemyspawn
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
	pop	de
	pop	bc
;src/game.c:69: for (i = 0; i < count; ++i) {
	inc	e
	jr	00120$
00116$:
;src/game.c:77: g_aliveenemies = count;
	ld	a, -4 (ix)
	ld	(#_g_aliveenemies + 0),a
	ld	sp, ix
	pop	ix
	ret
;src/game.c:80: static void spawn_boss(void) {
;	---------------------------------
; Function spawn_boss
; ---------------------------------
_spawn_boss:
;src/game.c:81: enemyinit(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyinit
;src/game.c:82: enemyspawn(&g_boss, 64, 88, 1, 0);
	ld	hl, #0x0001
	ex	(sp),hl
	ld	hl, #0x5840
	push	hl
	ld	hl, #_g_boss
	push	hl
	call	_enemyspawn
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
;src/game.c:83: g_boss.w = 8;
	ld	hl, #(_g_boss + 0x0004)
	ld	(hl), #0x08
;src/game.c:84: g_boss.h = 20;
	ld	hl, #(_g_boss + 0x0005)
	ld	(hl), #0x14
;src/game.c:85: g_boss.health = 8;
	ld	hl, #(_g_boss + 0x0007)
	ld	(hl), #0x08
;src/game.c:86: g_boss.reward = 1200;
	ld	hl, #(_g_boss + 0x0008)
	ld	(hl), #0xb0
;src/game.c:87: g_boss.kind = 3;
	ld	hl, #(_g_boss + 0x0009)
	ld	(hl), #0x03
;src/game.c:88: g_bossactive = 1;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x01
;src/game.c:89: g_bossphase = 0;
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x00
	ret
;src/game.c:92: static void try_fire_projectile(void) {
;	---------------------------------
; Function try_fire_projectile
; ---------------------------------
_try_fire_projectile:
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-6
	add	hl, sp
	ld	sp, hl
;src/game.c:96: if (!input_is_shoot_just_pressed()) return;
	call	_input_is_shoot_just_pressed
	ld	-1 (ix), l
	ld	a, l
	or	a, a
	jp	Z,00110$
;src/game.c:97: if (g_shootcooldown) return;
	ld	a,(#_g_shootcooldown + 0)
	or	a, a
	jr	NZ,00110$
;src/game.c:99: dir = g_player.facing_left ? -3 : 3;
	ld	a, (#_g_player + 7)
	or	a, a
	jr	Z,00112$
	ld	c, #0xfd
	jr	00113$
00112$:
	ld	c, #0x03
00113$:
	ld	-6 (ix), c
;src/game.c:101: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	-5 (ix), #0x00
00108$:
;src/game.c:102: if (!g_projectiles[i].active) {
	ld	c,-5 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	bc,#_g_projectiles
	add	hl,bc
	ld	-3 (ix), l
	ld	-2 (ix), h
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
	jr	NZ,00109$
;src/game.c:103: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel);
	ld	a,(#_g_player + 1)
	ld	-1 (ix), a
	add	a, #0x06
	ld	-1 (ix), a
	ld	a,(#_g_player + 0)
	ld	-4 (ix), a
	inc	-4 (ix)
	inc	-4 (ix)
	ld	a, (_g_weaponlevel)
	push	af
	inc	sp
	ld	h, -6 (ix)
	ld	l, -1 (ix)
	push	hl
	ld	a, -4 (ix)
	push	af
	inc	sp
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	push	hl
	call	_projectilefire
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
;src/game.c:104: g_shootcooldown = 10;
	ld	hl,#_g_shootcooldown + 0
	ld	(hl), #0x0a
;src/game.c:105: break;
	jr	00110$
00109$:
;src/game.c:101: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	-5 (ix)
	ld	a, -5 (ix)
	sub	a, #0x06
	jr	C,00108$
00110$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:110: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/game.c:113: cpct_disableFirmware();
	call	_cpct_disableFirmware
;src/game.c:114: cpct_setVideoMode(1);
	ld	l, #0x01
	call	_cpct_setVideoMode
;src/game.c:115: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:116: tilemap_init();
	call	_tilemap_init
;src/game.c:117: collision_init();
	call	_collision_init
;src/game.c:118: playerinit(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerinit
	pop	af
;src/game.c:119: hudinit();
	call	_hudinit
;src/game.c:121: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00102$:
;src/game.c:122: projectileinit(&g_projectiles[i]);
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
;src/game.c:121: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00102$
;src/game.c:125: g_lives = 3;
	ld	hl,#_g_lives + 0
	ld	(hl), #0x03
;src/game.c:126: g_score = 0;
	ld	hl, #0x0000
	ld	(_g_score), hl
;src/game.c:127: g_timeleft = 99;
	ld	iy, #_g_timeleft
	ld	0 (iy), #0x63
;src/game.c:128: g_weaponlevel = 0;
	ld	iy, #_g_weaponlevel
	ld	0 (iy), #0x00
;src/game.c:129: g_weapondisplay = 0;
	ld	iy, #_g_weapondisplay
	ld	0 (iy), #0x00
;src/game.c:130: g_currentwave = 0;
	ld	iy, #_g_currentwave
	ld	0 (iy), #0x00
;src/game.c:131: g_wavecooldown = 1;
	ld	iy, #_g_wavecooldown
	ld	0 (iy), #0x01
;src/game.c:132: g_damagecooldown = 0;
	ld	iy, #_g_damagecooldown
	ld	0 (iy), #0x00
;src/game.c:133: g_shootcooldown = 0;
	ld	iy, #_g_shootcooldown
	ld	0 (iy), #0x00
;src/game.c:134: g_victory = 0;
	ld	iy, #_g_victory
	ld	0 (iy), #0x00
;src/game.c:135: g_gameover = 0;
	ld	iy, #_g_gameover
	ld	0 (iy), #0x00
;src/game.c:136: g_framecounter = 0;
	ld	l, #0x00
	ld	(_g_framecounter), hl
;src/game.c:137: g_checkpointx = 20;
	ld	hl,#_g_checkpointx + 0
	ld	(hl), #0x14
;src/game.c:138: g_checkpointy = 120;
	ld	hl,#_g_checkpointy + 0
	ld	(hl), #0x78
;src/game.c:139: g_checkpointactive = 0;
	ld	hl,#_g_checkpointactive + 0
	ld	(hl), #0x00
;src/game.c:140: g_hiddenrewardtaken = 0;
	ld	hl,#_g_hiddenrewardtaken + 0
	ld	(hl), #0x00
;src/game.c:141: g_bossactive = 0;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x00
;src/game.c:142: enemyinit(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyinit
	pop	af
	ret
;src/game.c:145: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-25
	add	hl, sp
	ld	sp, hl
;src/game.c:149: input_update();
	call	_input_update
;src/game.c:151: if (g_gameover || g_victory) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jp	NZ,00202$
	ld	a,(#_g_victory + 0)
	or	a, a
;src/game.c:152: return;
	jp	NZ,00202$
;src/game.c:155: playerupdate(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerupdate
	pop	af
;src/game.c:156: try_fire_projectile();
	call	_try_fire_projectile
;src/game.c:158: if (g_shootcooldown) g_shootcooldown--;
	ld	iy, #_g_shootcooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00105$
	dec	0 (iy)
00105$:
;src/game.c:159: if (g_damagecooldown) g_damagecooldown--;
	ld	iy, #_g_damagecooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00213$
	dec	0 (iy)
;src/game.c:161: for (i = 0; i < MAX_PROJECTILES; ++i) {
00213$:
	ld	c, #0x00
00195$:
;src/game.c:162: projectileupdate(&g_projectiles[i]);
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
	call	_projectileupdate
	pop	af
	pop	bc
;src/game.c:161: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00195$
;src/game.c:165: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	c, #0x00
00197$:
;src/game.c:166: enemyupdate(&g_enemies[i]);
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	de, #_g_enemies
	add	hl, de
	push	bc
	push	hl
	call	_enemyupdate
	pop	af
	pop	bc
;src/game.c:165: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00197$
;src/game.c:169: if (g_bossactive) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00232$
;src/game.c:170: if (g_boss.health > 4) g_bossphase = 0;
	ld	hl, #_g_boss + 7
	ld	c, (hl)
	ld	a, #0x04
	sub	a, c
	jr	NC,00111$
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x00
	jr	00112$
00111$:
;src/game.c:171: else g_bossphase = 1;
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x01
00112$:
;src/game.c:173: g_boss.vx = (i8)(g_player.x < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
	ld	a, (#_g_player + 0)
	ld	hl, #_g_boss + 0
	ld	c, (hl)
	sub	a, c
	jr	NC,00204$
	ld	a,(#_g_bossphase + 0)
	or	a, a
	jr	Z,00206$
	ld	c, #0x02
	jr	00207$
00206$:
	ld	c, #0x01
00207$:
	xor	a, a
	sub	a, c
	ld	c, a
	jr	00205$
00204$:
	ld	a,(#_g_bossphase + 0)
	or	a, a
	jr	Z,00208$
	ld	c, #0x02
	jr	00209$
00208$:
	ld	c, #0x01
00209$:
00205$:
	ld	hl, #(_g_boss + 0x0002)
	ld	(hl), c
;src/game.c:174: enemyupdate(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyupdate
	pop	af
;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
00232$:
	ld	c, #0x00
00200$:
;src/game.c:178: if (!g_projectiles[i].active) continue;
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
	jp	Z, 00133$
;src/game.c:179: for (j = 0; j < MAX_ENEMIES; ++j) {
	ld	-25 (ix), #0x00
00199$:
;src/game.c:180: if (!g_enemies[j].active) continue;
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
;src/game.c:181: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
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
;src/game.c:183: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
	ld	hl, #0x0007
	add	hl,de
	ld	-12 (ix), l
	ld	-11 (ix), h
;src/game.c:180: if (!g_enemies[j].active) continue;
	ld	a, b
	or	a, a
	jp	Z, 00125$
;src/game.c:182: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
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
;src/game.c:181: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
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
	jr	Z,00125$
;src/game.c:183: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
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
	jr	Z,00124$
;src/game.c:184: g_score = (u16)(g_score + g_enemies[j].reward);
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
;src/game.c:185: if (g_aliveenemies) g_aliveenemies--;
	ld	iy, #_g_aliveenemies
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00124$
	dec	0 (iy)
00124$:
;src/game.c:187: g_projectiles[i].active = 0;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x00
;src/game.c:188: break;
	jr	00126$
00125$:
;src/game.c:179: for (j = 0; j < MAX_ENEMIES; ++j) {
	inc	-25 (ix)
	ld	a, -25 (ix)
	sub	a, #0x06
	jp	C, 00199$
00126$:
;src/game.c:191: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jp	Z, 00133$
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	a, (hl)
	or	a, a
	jp	Z, 00133$
;src/game.c:192: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
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
;src/game.c:191: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
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
	jr	Z,00133$
;src/game.c:193: g_projectiles[i].active = 0;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x00
;src/game.c:194: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
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
	jr	Z,00133$
;src/game.c:195: g_bossactive = 0;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x00
;src/game.c:196: g_score = (u16)(g_score + g_boss.reward);
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
;src/game.c:197: g_victory = 1;
	ld	hl,#_g_victory + 0
	ld	(hl), #0x01
00133$:
;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jp	C, 00200$
;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
;src/game.c:202: if (!g_damagecooldown) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jp	NZ, 00155$
;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	-24 (ix), #0x00
00201$:
;src/game.c:204: if (!g_enemies[i].active) continue;
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
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	de, #0x0006
	add	hl, de
	ld	c, (hl)
	ld	a, c
	or	a, a
	jp	Z, 00141$
;src/game.c:206: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	de, #0x0005
	add	hl, de
	ld	a, (hl)
	ld	-21 (ix), a
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	de, #0x0004
	add	hl, de
	ld	a, (hl)
	ld	-19 (ix), a
	pop	bc
	pop	hl
	push	hl
	push	bc
	inc	hl
	ld	e, (hl)
	ld	d, #0x00
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	ld	c, (hl)
	ld	b, #0x00
;src/game.c:205: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#(_g_player + 0x0005) + 0)
	ld	-23 (ix), a
	ld	a,(#(_g_player + 0x0004) + 0)
	ld	-18 (ix), a
	ld	a, (#(_g_player + 0x0001) + 0)
	ld	-16 (ix), a
	ld	-15 (ix), #0x00
	ld	a, (#_g_player + 0)
	ld	-12 (ix), a
	ld	-11 (ix), #0x00
	ld	h, -21 (ix)
	ld	l, -19 (ix)
	push	hl
	push	de
	push	bc
	ld	h, -23 (ix)
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
	jr	Z,00141$
;src/game.c:207: if (g_lives) g_lives--;
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00138$
	dec	0 (iy)
00138$:
;src/game.c:208: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
;src/game.c:209: break;
	jr	00142$
00141$:
;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-24 (ix)
	ld	a, -24 (ix)
	sub	a, #0x06
	jp	C, 00201$
00142$:
;src/game.c:213: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jp	NZ, 00146$
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00146$
;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
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
;src/game.c:213: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
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
	jr	Z,00146$
;src/game.c:215: if (g_lives) g_lives--;
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00144$
	dec	0 (iy)
00144$:
;src/game.c:216: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
00146$:
;src/game.c:219: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jr	NZ,00155$
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
	jr	Z,00155$
;src/game.c:220: if (g_lives) g_lives--;
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00150$
	dec	0 (iy)
00150$:
;src/game.c:221: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
00155$:
;src/game.c:225: if (g_lives == 0) {
	ld	a,(#_g_lives + 0)
	or	a, a
	jr	NZ,00160$
;src/game.c:226: if (g_checkpointactive) {
	ld	a,(#_g_checkpointactive + 0)
	or	a, a
	jr	Z,00157$
;src/game.c:227: g_lives = 2;
	ld	hl,#_g_lives + 0
	ld	(hl), #0x02
;src/game.c:228: reset_player_to_checkpoint();
	call	_reset_player_to_checkpoint
;src/game.c:229: g_damagecooldown = 50;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x32
	jr	00160$
00157$:
;src/game.c:231: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
00160$:
;src/game.c:235: if (!g_checkpointactive && g_player.x >= 44) {
	ld	iy, #_g_checkpointactive
	ld	a, 0 (iy)
	or	a, a
	jr	NZ,00162$
	ld	a, (#_g_player + 0)
	sub	a, #0x2c
	jr	C,00162$
;src/game.c:236: g_checkpointactive = 1;
	ld	0 (iy), #0x01
;src/game.c:237: g_checkpointx = 44;
	ld	hl,#_g_checkpointx + 0
	ld	(hl), #0x2c
;src/game.c:238: g_checkpointy = 120;
	ld	hl,#_g_checkpointy + 0
	ld	(hl), #0x78
00162$:
;src/game.c:241: if (!g_hiddenrewardtaken && tilemap_is_hidden_zone((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
	ld	a,(#_g_hiddenrewardtaken + 0)
	or	a, a
	jr	NZ,00169$
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
	call	_tilemap_is_hidden_zone
	pop	af
	pop	af
	pop	af
	ld	a, l
	or	a, a
	jr	Z,00169$
;src/game.c:242: g_hiddenrewardtaken = 1;
	ld	hl,#_g_hiddenrewardtaken + 0
	ld	(hl), #0x01
;src/game.c:243: if (g_lives < 5) g_lives++;
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	sub	a, #0x05
	jr	NC,00165$
	inc	0 (iy)
00165$:
;src/game.c:244: if (g_weaponlevel < 2) g_weaponlevel++;
	ld	iy, #_g_weaponlevel
	ld	a, 0 (iy)
	sub	a, #0x02
	jr	NC,00167$
	inc	0 (iy)
00167$:
;src/game.c:245: g_score = (u16)(g_score + 250);
	ld	hl, #_g_score
	ld	a, (hl)
	add	a, #0xfa
	ld	(hl), a
	inc	hl
	ld	a, (hl)
	adc	a, #0x00
	ld	(hl), a
00169$:
;src/game.c:248: if (g_score >= 800 && g_weaponlevel < 1) g_weaponlevel = 1;
	ld	iy, #_g_score
	ld	a, 0 (iy)
	sub	a, #0x20
	ld	a, 1 (iy)
	sbc	a, #0x03
	jr	C,00172$
	ld	iy, #_g_weaponlevel
	ld	a, 0 (iy)
	sub	a, #0x01
	jr	NC,00172$
	ld	0 (iy), #0x01
00172$:
;src/game.c:249: if (g_score >= 1600 && g_weaponlevel < 2) g_weaponlevel = 2;
	ld	iy, #_g_score
	ld	a, 0 (iy)
	sub	a, #0x40
	ld	a, 1 (iy)
	sbc	a, #0x06
	jr	C,00175$
	ld	iy, #_g_weaponlevel
	ld	a, 0 (iy)
	sub	a, #0x02
	jr	NC,00175$
	ld	0 (iy), #0x02
00175$:
;src/game.c:250: g_weapondisplay = (u8)(g_weaponlevel + 1);
	ld	hl, #_g_weapondisplay
	ld	a,(#_g_weaponlevel + 0)
	inc	a
	ld	(hl), a
;src/game.c:252: if (g_aliveenemies == 0 && !g_gameover) {
	ld	a,(#_g_aliveenemies + 0)
	or	a, a
	jr	NZ,00187$
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	NZ,00187$
;src/game.c:253: if (g_currentwave < TOTAL_WAVES) {
	ld	a,(#_g_currentwave + 0)
	sub	a, #0x03
	jr	NC,00184$
;src/game.c:254: if (g_wavecooldown == 0) {
	ld	a,(#_g_wavecooldown + 0)
	or	a, a
	jr	NZ,00178$
;src/game.c:255: spawn_wave(g_currentwave);
	ld	a, (_g_currentwave)
	push	af
	inc	sp
	call	_spawn_wave
	inc	sp
;src/game.c:256: g_currentwave++;
	ld	hl, #_g_currentwave+0
	inc	(hl)
;src/game.c:257: g_wavecooldown = 100;
	ld	hl,#_g_wavecooldown + 0
	ld	(hl), #0x64
	jr	00187$
00178$:
;src/game.c:259: g_wavecooldown--;
	ld	hl, #_g_wavecooldown+0
	dec	(hl)
	jr	00187$
00184$:
;src/game.c:261: } else if (!g_bossactive && g_player.x >= tilemap_goal_x()) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	NZ,00187$
	ld	hl, #_g_player + 0
	ld	c, (hl)
	push	bc
	call	_tilemap_goal_x
	pop	bc
	ld	a, c
	sub	a, l
	jr	C,00187$
;src/game.c:262: spawn_boss();
	call	_spawn_boss
00187$:
;src/game.c:266: g_framecounter++;
	ld	iy, #_g_framecounter
	inc	0 (iy)
	jr	NZ,00445$
	inc	1 (iy)
00445$:
;src/game.c:267: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
	ld	hl, #0x0032
	push	hl
	ld	hl, (_g_framecounter)
	push	hl
	call	__moduint
	pop	af
	pop	af
	ld	a, h
	or	a,l
	jr	NZ,00190$
	ld	iy, #_g_timeleft
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00190$
;src/game.c:268: g_timeleft--;
	dec	0 (iy)
00190$:
;src/game.c:270: if (g_timeleft == 0 && !g_victory) {
	ld	a,(#_g_timeleft + 0)
	or	a, a
	jr	NZ,00193$
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	NZ,00193$
;src/game.c:271: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
00193$:
;src/game.c:274: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
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
00202$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:277: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/game.c:280: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:281: tilemap_render();
	call	_tilemap_render
;src/game.c:283: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00113$:
;src/game.c:284: projectilerender(&g_projectiles[i]);
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
	call	_projectilerender
	pop	af
	pop	bc
;src/game.c:283: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00113$
;src/game.c:287: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	c, #0x00
00115$:
;src/game.c:288: enemyrender(&g_enemies[i]);
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	de, #_g_enemies
	add	hl, de
	push	bc
	push	hl
	call	_enemyrender
	pop	af
	pop	bc
;src/game.c:287: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00115$
;src/game.c:291: if (g_bossactive) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00104$
;src/game.c:292: enemyrender(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyrender
	pop	af
00104$:
;src/game.c:295: playerrender(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerrender
	pop	af
;src/game.c:296: hudrender();
	call	_hudrender
;src/game.c:298: if (g_victory) {
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	Z,00111$
;src/game.c:299: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
	ld	hl, #0x481c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	bc, #0x0818
	push	bc
	ld	a, #0x5c
	push	af
	inc	sp
	push	hl
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
00111$:
;src/game.c:300: } else if (g_gameover) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	Z,00108$
;src/game.c:301: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
	ld	hl, #0x481c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	bc, #0x0818
	push	bc
	ld	a, #0x4c
	push	af
	inc	sp
	push	hl
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
00108$:
;src/game.c:302: } else if (g_checkpointactive) {
	ld	a,(#_g_checkpointactive + 0)
	or	a, a
	ret	Z
;src/game.c:303: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 44, 150), 0x3A, 2, 10);
	ld	hl, #0x962c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	bc, #0x0a02
	push	bc
	ld	a, #0x3a
	push	af
	inc	sp
	push	hl
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
