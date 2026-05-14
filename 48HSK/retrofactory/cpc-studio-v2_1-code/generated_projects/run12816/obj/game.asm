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
	.ds 9
_g_enemies:
	.ds 54
_g_projectiles:
	.ds 60
_g_lives:
	.ds 1
_g_score:
	.ds 2
_g_timeleft:
	.ds 1
_g_weapon:
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
;src/game.c:32: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
;	---------------------------------
; Function rect_overlap
; ---------------------------------
_rect_overlap:
	push	ix
	ld	ix,#0
	add	ix,sp
;src/game.c:33: if (ax + aw <= bx) return 0;
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
;src/game.c:34: if (bx + bw <= ax) return 0;
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
;src/game.c:35: if (ay + ah <= by) return 0;
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
;src/game.c:36: if (by + bh <= ay) return 0;
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
;src/game.c:37: return 1;
	ld	l, #0x01
00109$:
	pop	ix
	ret
;src/game.c:40: static void spawn_wave(u8 wave) {
;	---------------------------------
; Function spawn_wave
; ---------------------------------
_spawn_wave:
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
;src/game.c:44: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	bc, #_g_enemies+0
	ld	e, #0x00
00111$:
;src/game.c:45: enemyinit(&g_enemies[i]);
	push	de
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, hl
	add	hl, de
	pop	de
	add	hl, bc
	push	bc
	push	de
	push	hl
	call	_enemyinit
	pop	af
	pop	de
	pop	bc
;src/game.c:44: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00111$
;src/game.c:48: if (wave == 0) count = 2;
	ld	a, 4 (ix)
	or	a, a
	jr	NZ,00106$
	ld	d, #0x02
	jr	00107$
00106$:
;src/game.c:49: else if (wave == 1) count = 3;
	ld	a, 4 (ix)
	dec	a
	jr	NZ,00103$
	ld	d, #0x03
	jr	00107$
00103$:
;src/game.c:50: else count = 4;
	ld	d, #0x04
00107$:
;src/game.c:52: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
	ld	a, #0x06
	sub	a, d
	jr	NC,00127$
	ld	d, #0x06
;src/game.c:54: for (i = 0; i < count; ++i) {
00127$:
	ld	e, #0x00
00114$:
	ld	a, e
	sub	a, d
	jr	NC,00110$
;src/game.c:55: enemyspawn(&g_enemies[i], (u8)(48 + (i * 10)), 112, (u8)((i & 1) ? 1 : 0));
	bit	0, e
	jr	Z,00118$
	ld	-1 (ix), #0x01
	jr	00119$
00118$:
	ld	-1 (ix), #0x00
00119$:
	push	de
	ld	a, e
	add	a, a
	add	a, a
	add	a, e
	add	a, a
	pop	de
	add	a, #0x30
	ld	-2 (ix), a
	push	de
	ld	d,#0x00
	ld	l, e
	ld	h, d
	add	hl, hl
	add	hl, hl
	add	hl, hl
	add	hl, de
	pop	de
	add	hl, bc
	push	hl
	pop	iy
	push	bc
	push	de
	ld	d, -1 (ix)
	ld	e,#0x70
	push	de
	ld	a, -2 (ix)
	push	af
	inc	sp
	push	iy
	call	_enemyspawn
	pop	af
	pop	af
	inc	sp
	pop	de
	pop	bc
;src/game.c:54: for (i = 0; i < count; ++i) {
	inc	e
	jr	00114$
00110$:
;src/game.c:58: g_aliveenemies = count;
	ld	hl,#_g_aliveenemies + 0
	ld	(hl), d
	ld	sp, ix
	pop	ix
	ret
;src/game.c:61: static void try_fire_projectile(void) {
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
;src/game.c:65: if (!input_is_shoot_just_pressed()) return;
	call	_input_is_shoot_just_pressed
	ld	-1 (ix), l
	ld	a, l
	or	a, a
	jp	Z,00110$
;src/game.c:66: if (g_shootcooldown) return;
	ld	a,(#_g_shootcooldown + 0)
	or	a, a
	jp	NZ,00110$
;src/game.c:68: dir = g_player.facing_left ? -3 : 3;
	ld	a, (#_g_player + 7)
	or	a, a
	jr	Z,00112$
	ld	c, #0xfd
	jr	00113$
00112$:
	ld	c, #0x03
00113$:
	ld	-6 (ix), c
;src/game.c:70: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	-5 (ix), #0x00
00108$:
;src/game.c:71: if (!g_projectiles[i].active) {
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
;src/game.c:72: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weapon);
	ld	a,(#_g_player + 1)
	ld	-1 (ix), a
	add	a, #0x06
	ld	-1 (ix), a
	ld	a,(#_g_player + 0)
	ld	-4 (ix), a
	inc	-4 (ix)
	inc	-4 (ix)
	ld	a, (_g_weapon)
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
;src/game.c:73: g_weapon ^= 1;
	ld	iy, #_g_weapon
	ld	a, 0 (iy)
	xor	a, #0x01
	ld	0 (iy), a
;src/game.c:74: g_shootcooldown = 10;
	ld	hl,#_g_shootcooldown + 0
	ld	(hl), #0x0a
;src/game.c:75: break;
	jr	00110$
00109$:
;src/game.c:70: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	-5 (ix)
	ld	a, -5 (ix)
	sub	a, #0x06
	jr	C,00108$
00110$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:80: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/game.c:83: cpct_disableFirmware();
	call	_cpct_disableFirmware
;src/game.c:84: cpct_setVideoMode(1);
	ld	l, #0x01
	call	_cpct_setVideoMode
;src/game.c:85: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:86: tilemap_init();
	call	_tilemap_init
;src/game.c:87: collision_init();
	call	_collision_init
;src/game.c:88: playerinit(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerinit
	pop	af
;src/game.c:89: hudinit();
	call	_hudinit
;src/game.c:91: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00102$:
;src/game.c:92: projectileinit(&g_projectiles[i]);
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
;src/game.c:91: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00102$
;src/game.c:95: g_lives = 3;
	ld	hl,#_g_lives + 0
	ld	(hl), #0x03
;src/game.c:96: g_score = 0;
	ld	hl, #0x0000
	ld	(_g_score), hl
;src/game.c:97: g_timeleft = 99;
	ld	iy, #_g_timeleft
	ld	0 (iy), #0x63
;src/game.c:98: g_weapon = 0;
	ld	iy, #_g_weapon
	ld	0 (iy), #0x00
;src/game.c:99: g_currentwave = 0;
	ld	iy, #_g_currentwave
	ld	0 (iy), #0x00
;src/game.c:100: g_wavecooldown = 1;
	ld	iy, #_g_wavecooldown
	ld	0 (iy), #0x01
;src/game.c:101: g_damagecooldown = 0;
	ld	iy, #_g_damagecooldown
	ld	0 (iy), #0x00
;src/game.c:102: g_shootcooldown = 0;
	ld	iy, #_g_shootcooldown
	ld	0 (iy), #0x00
;src/game.c:103: g_victory = 0;
	ld	iy, #_g_victory
	ld	0 (iy), #0x00
;src/game.c:104: g_gameover = 0;
	ld	iy, #_g_gameover
	ld	0 (iy), #0x00
;src/game.c:105: g_framecounter = 0;
	ld	l, #0x00
	ld	(_g_framecounter), hl
	ret
;src/game.c:108: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-16
	add	hl, sp
	ld	sp, hl
;src/game.c:112: input_update();
	call	_input_update
;src/game.c:114: if (g_gameover || g_victory) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jp	NZ,00165$
	ld	a,(#_g_victory + 0)
	or	a, a
;src/game.c:115: return;
	jp	NZ,00165$
;src/game.c:118: playerupdate(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerupdate
	pop	af
;src/game.c:119: try_fire_projectile();
	call	_try_fire_projectile
;src/game.c:121: if (g_shootcooldown) g_shootcooldown--;
	ld	iy, #_g_shootcooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00105$
	dec	0 (iy)
00105$:
;src/game.c:122: if (g_damagecooldown) g_damagecooldown--;
	ld	iy, #_g_damagecooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00170$
	dec	0 (iy)
;src/game.c:124: for (i = 0; i < MAX_PROJECTILES; ++i) {
00170$:
	ld	c, #0x00
00158$:
;src/game.c:125: projectileupdate(&g_projectiles[i]);
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
;src/game.c:124: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00158$
;src/game.c:128: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	c, #0x00
00160$:
;src/game.c:129: enemyupdate(&g_enemies[i]);
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, hl
	add	hl, bc
	ld	de, #_g_enemies
	add	hl, de
	push	bc
	push	hl
	call	_enemyupdate
	pop	af
	pop	bc
;src/game.c:128: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00160$
;src/game.c:132: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	-15 (ix), #0x00
00163$:
;src/game.c:133: if (!g_projectiles[i].active) continue;
	ld	c,-15 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	c, l
	ld	b, h
	ld	hl, #_g_projectiles
	add	hl,bc
	ld	-2 (ix), l
	ld	-1 (ix), h
	ld	a, -2 (ix)
	add	a, #0x06
	ld	-4 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-3 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	a, (hl)
	or	a, a
	jp	Z, 00122$
;src/game.c:134: for (j = 0; j < MAX_ENEMIES; ++j) {
	ld	-16 (ix), #0x00
00162$:
;src/game.c:135: if (!g_enemies[j].active) continue;
	ld	c,-16 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, hl
	add	hl, bc
	ld	c, l
	ld	b, h
	ld	hl, #_g_enemies
	add	hl,bc
	ld	-6 (ix), l
	ld	-5 (ix), h
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
	jp	Z, 00120$
;src/game.c:137: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	de, #0x0005
	add	hl, de
	ld	a, (hl)
	ld	-7 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	de, #0x0004
	add	hl, de
	ld	a, (hl)
	ld	-8 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	inc	hl
	ld	c, (hl)
	ld	-10 (ix), c
	ld	-9 (ix), #0x00
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	e, (hl)
	ld	d, #0x00
;src/game.c:136: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	bc, #0x0005
	add	hl, bc
	ld	b, (hl)
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	c, (hl)
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	inc	hl
	ld	l, (hl)
	ld	-12 (ix), l
	ld	-11 (ix), #0x00
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	l, (hl)
	ld	-14 (ix), l
	ld	-13 (ix), #0x00
	ld	h, -7 (ix)
	ld	l, -8 (ix)
	push	hl
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	push	hl
	push	de
	push	bc
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	push	hl
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	ld	a, l
	or	a, a
	jr	Z,00120$
;src/game.c:138: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	de, #0x0007
	add	hl, de
	ld	d, (hl)
	ld	c,-6 (ix)
	ld	b,-5 (ix)
	push	de
	inc	sp
	push	bc
	call	_enemydamage
	pop	af
	inc	sp
	ld	-14 (ix), l
	ld	a, l
	or	a, a
	jr	Z,00119$
;src/game.c:139: g_score = (u16)(g_score + g_enemies[j].reward);
	ld	a, -6 (ix)
	ld	-14 (ix), a
	ld	a, -5 (ix)
	ld	-13 (ix), a
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	ld	de, #0x0008
	add	hl, de
	ld	a, (hl)
	ld	-14 (ix), a
	ld	-14 (ix), a
	ld	-13 (ix), #0x00
	ld	hl, #_g_score
	ld	a, (hl)
	add	a, -14 (ix)
	ld	(hl), a
	inc	hl
	ld	a, (hl)
	adc	a, -13 (ix)
	ld	(hl), a
;src/game.c:140: if (g_aliveenemies) g_aliveenemies--;
	ld	iy, #_g_aliveenemies
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00119$
	dec	0 (iy)
00119$:
;src/game.c:142: g_projectiles[i].active = 0;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x00
;src/game.c:143: break;
	jr	00122$
00120$:
;src/game.c:134: for (j = 0; j < MAX_ENEMIES; ++j) {
	inc	-16 (ix)
	ld	a, -16 (ix)
	sub	a, #0x06
	jp	C, 00162$
00122$:
;src/game.c:132: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	-15 (ix)
	ld	a, -15 (ix)
	sub	a, #0x06
	jp	C, 00163$
;src/game.c:147: if (!g_damagecooldown) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jp	NZ, 00138$
;src/game.c:148: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	de, #_g_player + 4
	ld	-15 (ix), #0x00
00164$:
;src/game.c:149: if (!g_enemies[i].active) continue;
	ld	c,-15 (ix)
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, hl
	add	hl, bc
	ld	bc,#_g_enemies
	add	hl,bc
	ld	-14 (ix), l
	ld	-13 (ix), h
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	bc, #0x0006
	add	hl, bc
	ld	a, (hl)
	or	a, a
	jp	Z, 00130$
;src/game.c:151: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	bc, #0x0005
	add	hl, bc
	ld	a, (hl)
	ld	-12 (ix), a
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	bc, #0x0004
	add	hl, bc
	ld	c, (hl)
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	inc	hl
	ld	b, (hl)
	ld	-10 (ix), b
	ld	-9 (ix), #0x00
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	ld	b, (hl)
	ld	-14 (ix), b
	ld	-13 (ix), #0x00
;src/game.c:150: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	hl, #(_g_player + 0x0005) + 0
	ld	b, (hl)
	ld	a, (de)
	ld	-8 (ix), a
	ld	a, (#(_g_player + 0x0001) + 0)
	ld	-6 (ix), a
	ld	-5 (ix), #0x00
	ld	a, (#_g_player + 0)
	ld	-4 (ix), a
	ld	-3 (ix), #0x00
	push	de
	ld	a, -12 (ix)
	push	af
	inc	sp
	ld	a, c
	push	af
	inc	sp
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	push	hl
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	push	hl
	push	bc
	inc	sp
	ld	a, -8 (ix)
	push	af
	inc	sp
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	push	hl
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	pop	de
	ld	a, l
	or	a, a
	jr	Z,00130$
;src/game.c:152: if (g_lives) g_lives--;
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00127$
	dec	0 (iy)
00127$:
;src/game.c:153: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
;src/game.c:154: break;
	jr	00131$
00130$:
;src/game.c:148: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-15 (ix)
	ld	a, -15 (ix)
	sub	a, #0x06
	jp	C, 00164$
00131$:
;src/game.c:158: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jr	NZ,00138$
	ld	a, (#(_g_player + 0x0005) + 0)
	push	af
	ld	a, (de)
	ld	-14 (ix), a
	pop	af
	ld	hl, #(_g_player + 0x0001) + 0
	ld	c, (hl)
	ld	b, #0x00
	ld	hl, #_g_player + 0
	ld	e, (hl)
	ld	d, #0x00
	push	af
	inc	sp
	ld	a, -14 (ix)
	push	af
	inc	sp
	push	bc
	push	de
	call	_collision_is_on_trap
	pop	af
	pop	af
	pop	af
	ld	a, l
	or	a, a
	jr	Z,00138$
;src/game.c:159: if (g_lives) g_lives--;
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00133$
	dec	0 (iy)
00133$:
;src/game.c:160: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
00138$:
;src/game.c:164: if (g_lives == 0) {
	ld	a,(#_g_lives + 0)
	or	a, a
	jr	NZ,00140$
;src/game.c:165: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
00140$:
;src/game.c:168: if (g_aliveenemies == 0 && !g_gameover) {
	ld	a,(#_g_aliveenemies + 0)
	or	a, a
	jr	NZ,00150$
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	NZ,00150$
;src/game.c:169: if (g_currentwave < TOTAL_WAVES) {
	ld	a,(#_g_currentwave + 0)
	sub	a, #0x03
	jr	NC,00147$
;src/game.c:170: if (g_wavecooldown == 0) {
	ld	a,(#_g_wavecooldown + 0)
	or	a, a
	jr	NZ,00142$
;src/game.c:171: spawn_wave(g_currentwave);
	ld	a, (_g_currentwave)
	push	af
	inc	sp
	call	_spawn_wave
	inc	sp
;src/game.c:172: g_currentwave++;
	ld	hl, #_g_currentwave+0
	inc	(hl)
;src/game.c:173: g_wavecooldown = 100;
	ld	hl,#_g_wavecooldown + 0
	ld	(hl), #0x64
	jr	00150$
00142$:
;src/game.c:175: g_wavecooldown--;
	ld	hl, #_g_wavecooldown+0
	dec	(hl)
	jr	00150$
00147$:
;src/game.c:177: } else if (g_player.x >= tilemap_goal_x()) {
	ld	hl, #_g_player + 0
	ld	c, (hl)
	push	bc
	call	_tilemap_goal_x
	pop	bc
	ld	a, c
	sub	a, l
	jr	C,00150$
;src/game.c:178: g_victory = 1;
	ld	hl,#_g_victory + 0
	ld	(hl), #0x01
00150$:
;src/game.c:182: g_framecounter++;
	ld	iy, #_g_framecounter
	inc	0 (iy)
	jr	NZ,00302$
	inc	1 (iy)
00302$:
;src/game.c:183: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
	ld	hl, #0x0032
	push	hl
	ld	hl, (_g_framecounter)
	push	hl
	call	__moduint
	pop	af
	pop	af
	ld	a, h
	or	a,l
	jr	NZ,00153$
	ld	iy, #_g_timeleft
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00153$
;src/game.c:184: g_timeleft--;
	dec	0 (iy)
00153$:
;src/game.c:186: if (g_timeleft == 0 && !g_victory) {
	ld	a,(#_g_timeleft + 0)
	or	a, a
	jr	NZ,00156$
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	NZ,00156$
;src/game.c:187: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
00156$:
;src/game.c:190: hudupdate(g_lives, g_score, g_timeleft, g_weapon);
	ld	a, (_g_weapon)
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
00165$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:193: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/game.c:196: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:197: tilemap_render();
	call	_tilemap_render
;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00108$:
;src/game.c:200: projectilerender(&g_projectiles[i]);
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
;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00108$
;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	c, #0x00
00110$:
;src/game.c:204: enemyrender(&g_enemies[i]);
	ld	b,#0x00
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, hl
	add	hl, bc
	ld	de, #_g_enemies
	add	hl, de
	push	bc
	push	hl
	call	_enemyrender
	pop	af
	pop	bc
;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00110$
;src/game.c:207: playerrender(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerrender
	pop	af
;src/game.c:208: hudrender();
	call	_hudrender
;src/game.c:210: if (g_victory) {
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	Z,00106$
;src/game.c:211: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
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
00106$:
;src/game.c:212: } else if (g_gameover) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	ret	Z
;src/game.c:213: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
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
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
