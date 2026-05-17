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
	.ds 9
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
;src/game.c:41: static void reset_player_to_checkpoint(void) {
;	---------------------------------
; Function reset_player_to_checkpoint
; ---------------------------------
_reset_player_to_checkpoint:
;src/game.c:42: g_player.x = g_checkpointx;
	ld	hl, #_g_player
	ld	a,(#_g_checkpointx + 0)
	ld	(hl), a
;src/game.c:43: g_player.y = g_checkpointy;
	ld	hl, #(_g_player + 0x0001)
	ld	a,(#_g_checkpointy + 0)
	ld	(hl), a
;src/game.c:44: g_player.vx = 0;
	ld	hl, #(_g_player + 0x0002)
	ld	(hl), #0x00
;src/game.c:45: g_player.vy = 0;
	ld	hl, #(_g_player + 0x0003)
	ld	(hl), #0x00
	ret
;src/game.c:48: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
;	---------------------------------
; Function rect_overlap
; ---------------------------------
_rect_overlap:
	push	ix
	ld	ix,#0
	add	ix,sp
;src/game.c:49: if (ax + aw <= bx) return 0;
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
;src/game.c:50: if (bx + bw <= ax) return 0;
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
;src/game.c:51: if (ay + ah <= by) return 0;
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
;src/game.c:52: if (by + bh <= ay) return 0;
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
;src/game.c:53: return 1;
	ld	l, #0x01
00109$:
	pop	ix
	ret
;src/game.c:56: static void spawn_wave(u8 wave) {
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
;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	bc, #_g_enemies+0
	ld	e, #0x00
00117$:
;src/game.c:61: enemyinit(&g_enemies[i]);
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
;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	e
	ld	a, e
	sub	a, #0x06
	jr	C,00117$
;src/game.c:65: else if (wave == 1) count = 3;
	ld	a, 4 (ix)
	dec	a
	jr	NZ,00190$
	ld	a,#0x01
	jr	00191$
00190$:
	xor	a,a
00191$:
	ld	e, a
;src/game.c:64: if (wave == 0) count = 2;
	ld	a, 4 (ix)
	or	a, a
	jr	NZ,00106$
	ld	-5 (ix), #0x02
	jr	00107$
00106$:
;src/game.c:65: else if (wave == 1) count = 3;
	ld	a, e
	or	a, a
	jr	Z,00103$
	ld	-5 (ix), #0x03
	jr	00107$
00103$:
;src/game.c:66: else count = 4;
	ld	-5 (ix), #0x04
00107$:
;src/game.c:68: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
	ld	a, #0x06
	sub	a, -5 (ix)
	jr	NC,00148$
	ld	-5 (ix), #0x06
;src/game.c:70: for (i = 0; i < count; ++i) {
00148$:
	ld	-2 (ix), e
	ld	-4 (ix), #0x00
00120$:
	ld	a, -4 (ix)
	sub	a, -5 (ix)
	jp	NC, 00116$
;src/game.c:73: if (wave == 0) type = 0;
	ld	a, 4 (ix)
	or	a,a
	jr	NZ,00114$
	ld	e,a
	jr	00115$
00114$:
;src/game.c:74: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
	ld	a, -2 (ix)
	or	a, a
	jr	Z,00111$
	ld	a, -4 (ix)
	or	a, a
	jr	NZ,00124$
	ld	e, #0x01
	jr	00115$
00124$:
	ld	e, #0x00
	jr	00115$
00111$:
;src/game.c:75: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
	ld	a, -4 (ix)
	or	a, a
	jr	Z,00129$
	ld	a, -4 (ix)
	sub	a, #0x03
	jr	NZ,00126$
00129$:
	ld	e, #0x02
	jr	00127$
00126$:
	ld	e, #0x01
00127$:
00115$:
;src/game.c:77: spawn_y = (type == 2) ? 84 : 112;
	ld	a, e
	sub	a, #0x02
	jr	NZ,00131$
	ld	d, #0x54
	jr	00132$
00131$:
	ld	d, #0x70
00132$:
;src/game.c:78: enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));
	bit	0, -4 (ix)
	jr	Z,00133$
	ld	-1 (ix), #0x01
	jr	00134$
00133$:
	ld	-1 (ix), #0x00
00134$:
	ld	a, -4 (ix)
	rlca
	rlca
	rlca
	and	a, #0xf8
	add	a, #0x2e
	ld	-3 (ix), a
	push	de
	ld	e,-4 (ix)
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
	ld	a, -1 (ix)
	push	af
	inc	sp
	ld	a, e
	push	af
	inc	sp
	push	de
	inc	sp
	ld	a, -3 (ix)
	push	af
	inc	sp
	push	iy
	call	_enemyspawn
	ld	hl, #6
	add	hl, sp
	ld	sp, hl
	pop	bc
;src/game.c:70: for (i = 0; i < count; ++i) {
	inc	-4 (ix)
	jp	00120$
00116$:
;src/game.c:81: g_aliveenemies = count;
	ld	a, -5 (ix)
	ld	(#_g_aliveenemies + 0),a
	ld	sp, ix
	pop	ix
	ret
;src/game.c:84: static void spawn_boss(void) {
;	---------------------------------
; Function spawn_boss
; ---------------------------------
_spawn_boss:
;src/game.c:85: enemyinit(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyinit
	pop	af
;src/game.c:86: enemyspawn(&g_boss, 68, 112, 1, 0);
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
;src/game.c:87: g_boss.w = 10;
	ld	hl, #(_g_boss + 0x0004)
	ld	(hl), #0x0a
;src/game.c:88: g_boss.h = 18;
	ld	hl, #(_g_boss + 0x0005)
	ld	(hl), #0x12
;src/game.c:89: g_boss.health = 10;
	ld	hl, #(_g_boss + 0x0007)
	ld	(hl), #0x0a
;src/game.c:90: g_boss.reward = 1500;
	ld	hl, #(_g_boss + 0x0008)
	ld	(hl), #0xdc
;src/game.c:91: g_boss.kind = 3;
	ld	hl, #(_g_boss + 0x0009)
	ld	(hl), #0x03
;src/game.c:92: g_boss.vx = -1;
	ld	hl, #(_g_boss + 0x0002)
	ld	(hl), #0xff
;src/game.c:93: g_bossactive = 1;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x01
;src/game.c:94: g_bossphase = 0;
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x00
	ret
;src/game.c:97: static void try_fire_projectile(void) {
;	---------------------------------
; Function try_fire_projectile
; ---------------------------------
_try_fire_projectile:
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	dec	sp
;src/game.c:101: if (!input_is_shoot_just_pressed()) return;
	call	_input_is_shoot_just_pressed
	ld	a, l
	or	a, a
	jp	Z,00110$
;src/game.c:102: if (g_shootcooldown) return;
	ld	a,(#_g_shootcooldown + 0)
	or	a, a
	jp	NZ,00110$
;src/game.c:104: dir = g_player.facing_left ? -3 : 3;
	ld	a, (#_g_player + 7)
	or	a, a
	jr	Z,00112$
	ld	c, #0xfd
	jr	00113$
00112$:
	ld	c, #0x03
00113$:
;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	-1 (ix), #0x00
	ld	b, #0x00
00108$:
;src/game.c:107: if (!g_projectiles[i].active) {
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
;src/game.c:109: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
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
;src/game.c:110: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
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
;src/game.c:111: break;
	jr	00110$
00109$:
;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	b
	ld	-1 (ix), b
	ld	a, b
	sub	a, #0x06
	jr	C,00108$
00110$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:116: static void register_player_hit(void) {
;	---------------------------------
; Function register_player_hit
; ---------------------------------
_register_player_hit:
;src/game.c:117: if (g_lives) {
	ld	iy, #_g_lives
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00102$
;src/game.c:118: g_lives--;
	dec	0 (iy)
00102$:
;src/game.c:120: if (g_lives == 0) {
	ld	a,(#_g_lives + 0)
	or	a, a
	jr	NZ,00104$
;src/game.c:121: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
;src/game.c:122: return;
	ret
00104$:
;src/game.c:125: reset_player_to_checkpoint();
	call	_reset_player_to_checkpoint
;src/game.c:126: g_damagecooldown = 40;
	ld	hl,#_g_damagecooldown + 0
	ld	(hl), #0x28
	ret
;src/game.c:129: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/game.c:132: cpct_disableFirmware();
	call	_cpct_disableFirmware
;src/game.c:133: cpct_setVideoMode(0);
	ld	l, #0x00
	call	_cpct_setVideoMode
;src/game.c:134: cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
	ld	hl, #0x0010
	push	hl
	ld	hl, #_gpalette
	push	hl
	call	_cpct_setPalette
;src/game.c:135: cpct_setBorder(gpalette[0]);
	ld	hl, #_gpalette + 0
	ld	b, (hl)
	push	bc
	inc	sp
	ld	a, #0x10
	push	af
	inc	sp
	call	_cpct_setPALColour
;src/game.c:136: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:137: tilemap_init();
	call	_tilemap_init
;src/game.c:138: collision_init();
	call	_collision_init
;src/game.c:139: playerinit(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerinit
	pop	af
;src/game.c:140: hudinit();
	call	_hudinit
;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00102$:
;src/game.c:143: projectileinit(&g_projectiles[i]);
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
;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00102$
;src/game.c:146: g_lives = 3;
	ld	hl,#_g_lives + 0
	ld	(hl), #0x03
;src/game.c:147: g_score = 0;
	ld	hl, #0x0000
	ld	(_g_score), hl
;src/game.c:148: g_timeleft = 99;
	ld	iy, #_g_timeleft
	ld	0 (iy), #0x63
;src/game.c:149: g_weapondisplay = 1;
	ld	iy, #_g_weapondisplay
	ld	0 (iy), #0x01
;src/game.c:150: g_currentwave = 0;
	ld	iy, #_g_currentwave
	ld	0 (iy), #0x00
;src/game.c:151: g_wavecooldown = 1;
	ld	iy, #_g_wavecooldown
	ld	0 (iy), #0x01
;src/game.c:152: g_damagecooldown = 0;
	ld	iy, #_g_damagecooldown
	ld	0 (iy), #0x00
;src/game.c:153: g_shootcooldown = 0;
	ld	iy, #_g_shootcooldown
	ld	0 (iy), #0x00
;src/game.c:154: g_victory = 0;
	ld	iy, #_g_victory
	ld	0 (iy), #0x00
;src/game.c:155: g_gameover = 0;
	ld	iy, #_g_gameover
	ld	0 (iy), #0x00
;src/game.c:156: g_framecounter = 0;
	ld	l, #0x00
	ld	(_g_framecounter), hl
;src/game.c:157: g_checkpointx = 20;
	ld	hl,#_g_checkpointx + 0
	ld	(hl), #0x14
;src/game.c:158: g_checkpointy = 120;
	ld	hl,#_g_checkpointy + 0
	ld	(hl), #0x78
;src/game.c:159: g_checkpointactive = 0;
	ld	hl,#_g_checkpointactive + 0
	ld	(hl), #0x00
;src/game.c:160: g_bossactive = 0;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x00
;src/game.c:161: g_weaponlevel = 0;
	ld	hl,#_g_weaponlevel + 0
	ld	(hl), #0x00
;src/game.c:162: g_pickuptaken = 0;
	ld	hl,#_g_pickuptaken + 0
	ld	(hl), #0x00
;src/game.c:163: enemyinit(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyinit
	pop	af
	ret
;src/game.c:166: void game_update(void) {
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
;src/game.c:170: input_update();
	call	_input_update
;src/game.c:172: if (g_gameover || g_victory) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	NZ,00101$
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	Z,00102$
00101$:
;src/game.c:173: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
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
;src/game.c:174: return;
	jp	00181$
00102$:
;src/game.c:177: playerupdate(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerupdate
	pop	af
;src/game.c:178: try_fire_projectile();
	call	_try_fire_projectile
;src/game.c:180: if (g_shootcooldown) g_shootcooldown--;
	ld	iy, #_g_shootcooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00105$
	dec	0 (iy)
00105$:
;src/game.c:181: if (g_damagecooldown) g_damagecooldown--;
	ld	iy, #_g_damagecooldown
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00192$
	dec	0 (iy)
;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
00192$:
	ld	c, #0x00
00174$:
;src/game.c:184: projectileupdate(&g_projectiles[i]);
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
;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00174$
;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	c, #0x00
00176$:
;src/game.c:188: enemyupdate(&g_enemies[i]);
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
;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00176$
;src/game.c:191: if (g_bossactive) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00211$
;src/game.c:192: if (g_boss.health > 4) g_bossphase = 0;
	ld	hl, #_g_boss + 7
	ld	c, (hl)
	ld	a, #0x04
	sub	a, c
	jr	NC,00111$
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x00
	jr	00112$
00111$:
;src/game.c:193: else g_bossphase = 1;
	ld	hl,#_g_bossphase + 0
	ld	(hl), #0x01
00112$:
;src/game.c:195: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
	ld	a,(#_g_player + 0)
	ld	-1 (ix), a
	ld	-3 (ix), a
	ld	-2 (ix), #0x00
	ld	a, -3 (ix)
	add	a, #0x02
	ld	-3 (ix), a
	ld	a, -2 (ix)
	adc	a, #0x00
	ld	-2 (ix), a
	ld	hl, #_g_boss + 0
	ld	c, (hl)
	ld	b, #0x00
	ld	a, -3 (ix)
	sub	a, c
	ld	a, -2 (ix)
	sbc	a, b
	jp	PO, 00380$
	xor	a, #0x80
00380$:
	jp	P, 00183$
	ld	a,(#_g_bossphase + 0)
	or	a, a
	jr	Z,00185$
	ld	c, #0x02
	jr	00186$
00185$:
	ld	c, #0x01
00186$:
	xor	a, a
	sub	a, c
	ld	c, a
	jr	00184$
00183$:
	ld	a,(#_g_bossphase + 0)
	or	a, a
	jr	Z,00187$
	ld	c, #0x02
	jr	00188$
00187$:
	ld	c, #0x01
00188$:
00184$:
	ld	hl, #(_g_boss + 0x0002)
	ld	(hl), c
;src/game.c:196: enemyupdate(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyupdate
	pop	af
;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
00211$:
	ld	c, #0x00
00179$:
;src/game.c:200: if (!g_projectiles[i].active) continue;
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
	ld	-3 (ix), l
	ld	-2 (ix), h
	ld	a, (hl)
	or	a, a
	jp	Z, 00133$
;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
	ld	-24 (ix), #0x00
00178$:
;src/game.c:202: if (!g_enemies[j].active) continue;
	push	de
	ld	e,-24 (ix)
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
	ld	-9 (ix), a
	ld	a, #>(_g_enemies)
	adc	a, h
	ld	-8 (ix), a
	ld	l,-9 (ix)
	ld	h,-8 (ix)
	push	bc
	ld	bc, #0x0006
	add	hl, bc
	pop	bc
	ld	b, (hl)
;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	hl, #0x0005
	add	hl,de
	ld	-11 (ix), l
	ld	-10 (ix), h
	ld	hl, #0x0004
	add	hl,de
	ld	-13 (ix), l
	ld	-12 (ix), h
	ld	hl, #0x0001
	add	hl,de
	ld	-5 (ix), l
	ld	-4 (ix), h
;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
	ld	hl, #0x0007
	add	hl,de
	ld	-7 (ix), l
	ld	-6 (ix), h
;src/game.c:202: if (!g_enemies[j].active) continue;
	ld	a, b
	or	a, a
	jp	Z, 00125$
;src/game.c:204: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
	ld	l,-9 (ix)
	ld	h,-8 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	-1 (ix), a
	ld	l,-9 (ix)
	ld	h,-8 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	-14 (ix), a
	ld	l,-9 (ix)
	ld	h,-8 (ix)
	inc	hl
	ld	b, (hl)
	ld	-16 (ix), b
	ld	-15 (ix), #0x00
	ld	l,-9 (ix)
	ld	h,-8 (ix)
	ld	b, (hl)
	ld	-18 (ix), b
	ld	-17 (ix), #0x00
;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	l,-11 (ix)
	ld	h,-10 (ix)
	ld	a, (hl)
	ld	-19 (ix), a
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	b, (hl)
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	l, (hl)
	ld	-21 (ix), l
	ld	-20 (ix), #0x00
	ld	a, (de)
	ld	-23 (ix), a
	ld	-22 (ix), #0x00
	push	bc
	push	de
	ld	h, -1 (ix)
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
;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	ld	h, (hl)
	ld	l, -9 (ix)
	ld	b, -8 (ix)
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
;src/game.c:206: g_score = (u16)(g_score + g_enemies[j].reward);
	ld	l,-9 (ix)
	ld	h,-8 (ix)
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
;src/game.c:207: if (g_aliveenemies) g_aliveenemies--;
	ld	iy, #_g_aliveenemies
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00124$
	dec	0 (iy)
00124$:
;src/game.c:209: g_projectiles[i].active = 0;
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), #0x00
;src/game.c:210: break;
	jr	00126$
00125$:
;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
	inc	-24 (ix)
	ld	a, -24 (ix)
	sub	a, #0x06
	jp	C, 00178$
00126$:
;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jp	Z, 00133$
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	a, (hl)
	or	a, a
	jp	Z, 00133$
;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
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
;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
	ld	l,-11 (ix)
	ld	h,-10 (ix)
	push	af
	ld	a, (hl)
	ld	-19 (ix), a
	pop	af
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	push	af
	ld	a, (hl)
	ld	-18 (ix), a
	pop	af
	ld	l,-5 (ix)
	ld	h,-4 (ix)
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
;src/game.c:215: g_projectiles[i].active = 0;
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), #0x00
;src/game.c:216: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
	ld	l,-7 (ix)
	ld	h,-6 (ix)
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
;src/game.c:217: g_bossactive = 0;
	ld	hl,#_g_bossactive + 0
	ld	(hl), #0x00
;src/game.c:218: g_score = (u16)(g_score + g_boss.reward);
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
;src/game.c:219: g_victory = 1;
	ld	hl,#_g_victory + 0
	ld	(hl), #0x01
00133$:
;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jp	C, 00179$
;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
;src/game.c:224: if (!g_damagecooldown) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jp	NZ, 00149$
;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	-25 (ix), #0x00
00180$:
;src/game.c:226: if (!g_enemies[i].active) continue;
	ld	c,-25 (ix)
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
	ld	a, (hl)
	or	a, a
	jp	Z, 00139$
;src/game.c:228: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
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
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	de, #0x0004
	add	hl, de
	ld	e, (hl)
	pop	bc
	pop	hl
	push	hl
	push	bc
	inc	hl
	ld	c, (hl)
	ld	b, #0x00
	ld	l,-23 (ix)
	ld	h,-22 (ix)
	ld	d, (hl)
	ld	-23 (ix), d
	ld	-22 (ix), #0x00
;src/game.c:227: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#(_g_player + 0x0005) + 0)
	ld	-19 (ix), a
	ld	a,(#(_g_player + 0x0004) + 0)
	ld	-18 (ix), a
	ld	a, (#(_g_player + 0x0001) + 0)
	ld	-16 (ix), a
	ld	-15 (ix), #0x00
	ld	a, (#_g_player + 0)
	ld	-7 (ix), a
	ld	-6 (ix), #0x00
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
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	ld	a, l
	or	a, a
	jr	Z,00139$
;src/game.c:229: register_player_hit();
	call	_register_player_hit
;src/game.c:230: break;
	jr	00140$
00139$:
;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	-25 (ix)
	ld	a, -25 (ix)
	sub	a, #0x06
	jp	C, 00180$
00140$:
;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jr	NZ,00142$
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00142$
;src/game.c:235: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
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
;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
	ld	a,(#(_g_player + 0x0005) + 0)
	ld	-19 (ix), a
	ld	a,(#(_g_player + 0x0004) + 0)
	ld	-18 (ix), a
	ld	a, (#(_g_player + 0x0001) + 0)
	ld	-16 (ix), a
	ld	-15 (ix), #0x00
	ld	a, (#_g_player + 0)
	ld	-7 (ix), a
	ld	-6 (ix), #0x00
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
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	push	hl
	call	_rect_overlap
	ld	iy, #12
	add	iy, sp
	ld	sp, iy
	ld	a, l
	or	a, a
	jr	Z,00142$
;src/game.c:236: register_player_hit();
	call	_register_player_hit
00142$:
;src/game.c:239: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
	ld	a,(#_g_damagecooldown + 0)
	or	a, a
	jr	NZ,00149$
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
	jr	Z,00149$
;src/game.c:240: register_player_hit();
	call	_register_player_hit
00149$:
;src/game.c:244: if (!g_checkpointactive && g_player.x >= 44) {
	ld	iy, #_g_checkpointactive
	ld	a, 0 (iy)
	or	a, a
	jr	NZ,00151$
	ld	a, (#_g_player + 0)
	sub	a, #0x2c
	jr	C,00151$
;src/game.c:245: g_checkpointactive = 1;
	ld	0 (iy), #0x01
;src/game.c:246: g_checkpointx = 52;
	ld	hl,#_g_checkpointx + 0
	ld	(hl), #0x34
;src/game.c:247: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
	call	_tilemap_ground_y
	ld	c, l
	ld	hl, #(_g_player + 0x0005) + 0
	ld	b, (hl)
	ld	hl, #_g_checkpointy
	ld	a, c
	sub	a, b
	ld	(hl), a
00151$:
;src/game.c:250: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
	ld	a,(#_g_pickuptaken + 0)
	or	a, a
	jp	NZ, 00154$
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
	jr	Z,00154$
;src/game.c:251: g_pickuptaken = 1;
	ld	hl,#_g_pickuptaken + 0
	ld	(hl), #0x01
;src/game.c:252: g_weaponlevel = 1;
	ld	hl,#_g_weaponlevel + 0
	ld	(hl), #0x01
;src/game.c:253: g_score = (u16)(g_score + 100);
	ld	hl, #_g_score
	ld	a, (hl)
	add	a, #0x64
	ld	(hl), a
	inc	hl
	ld	a, (hl)
	adc	a, #0x00
	ld	(hl), a
00154$:
;src/game.c:256: g_weapondisplay = (u8)(g_weaponlevel + 1);
	ld	hl, #_g_weapondisplay
	ld	a,(#_g_weaponlevel + 0)
	inc	a
	ld	(hl), a
;src/game.c:258: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	NZ,00165$
	ld	a,(#_g_aliveenemies + 0)
	or	a, a
	jr	NZ,00165$
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	NZ,00165$
;src/game.c:259: if (g_currentwave < TOTAL_WAVES) {
	ld	a,(#_g_currentwave + 0)
	sub	a, #0x03
	jr	NC,00162$
;src/game.c:260: if (g_wavecooldown == 0) {
	ld	a,(#_g_wavecooldown + 0)
	or	a, a
	jr	NZ,00157$
;src/game.c:261: spawn_wave(g_currentwave);
	ld	a, (_g_currentwave)
	push	af
	inc	sp
	call	_spawn_wave
	inc	sp
;src/game.c:262: g_currentwave++;
	ld	hl, #_g_currentwave+0
	inc	(hl)
;src/game.c:263: g_wavecooldown = 90;
	ld	hl,#_g_wavecooldown + 0
	ld	(hl), #0x5a
	jr	00165$
00157$:
;src/game.c:265: g_wavecooldown--;
	ld	hl, #_g_wavecooldown+0
	dec	(hl)
	jr	00165$
00162$:
;src/game.c:267: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
	ld	hl, #_g_player + 0
	ld	c, (hl)
	push	bc
	call	_tilemap_goal_x
	pop	bc
	dec	l
	dec	l
	ld	a, c
	sub	a, l
	jr	C,00165$
;src/game.c:268: spawn_boss();
	call	_spawn_boss
00165$:
;src/game.c:272: g_framecounter++;
	ld	iy, #_g_framecounter
	inc	0 (iy)
	jr	NZ,00381$
	inc	1 (iy)
00381$:
;src/game.c:273: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
	ld	hl, #0x0032
	push	hl
	ld	hl, (_g_framecounter)
	push	hl
	call	__moduint
	pop	af
	pop	af
	ld	a, h
	or	a,l
	jr	NZ,00169$
	ld	iy, #_g_timeleft
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00169$
;src/game.c:274: g_timeleft--;
	dec	0 (iy)
00169$:
;src/game.c:276: if (g_timeleft == 0 && !g_victory) {
	ld	a,(#_g_timeleft + 0)
	or	a, a
	jr	NZ,00172$
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	NZ,00172$
;src/game.c:277: g_gameover = 1;
	ld	hl,#_g_gameover + 0
	ld	(hl), #0x01
00172$:
;src/game.c:280: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
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
00181$:
	ld	sp, ix
	pop	ix
	ret
;src/game.c:283: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/game.c:286: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:287: tilemap_render();
	call	_tilemap_render
;src/game.c:289: for (i = 0; i < MAX_PROJECTILES; ++i) {
	ld	c, #0x00
00115$:
;src/game.c:290: projectilerender(&g_projectiles[i]);
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
;src/game.c:289: for (i = 0; i < MAX_PROJECTILES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00115$
;src/game.c:293: for (i = 0; i < MAX_ENEMIES; ++i) {
	ld	c, #0x00
00117$:
;src/game.c:294: enemyrender(&g_enemies[i]);
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
;src/game.c:293: for (i = 0; i < MAX_ENEMIES; ++i) {
	inc	c
	ld	a, c
	sub	a, #0x06
	jr	C,00117$
;src/game.c:297: if (g_bossactive) {
	ld	a,(#_g_bossactive + 0)
	or	a, a
	jr	Z,00104$
;src/game.c:298: enemyrender(&g_boss);
	ld	hl, #_g_boss
	push	hl
	call	_enemyrender
;src/game.c:299: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(1, 1), 32, 2);
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
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0220
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/game.c:300: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
	ld	a, (#_g_boss + 7)
	ld	c, a
	add	a, a
	add	a, c
	ld	d, a
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
	ld	c, l
	ld	b, h
	pop	de
	ld	a, #0x02
	push	af
	inc	sp
	push	de
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00104$:
;src/game.c:303: if (!g_pickuptaken) {
	ld	a,(#_g_pickuptaken + 0)
	or	a, a
	jr	NZ,00106$
;src/game.c:304: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
	ld	hl, #0x0707
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	push	de
	call	_tilemap_ground_y
	pop	de
	ld	a, l
	add	a, #0xf8
	ld	b, a
	push	de
	push	bc
	inc	sp
	ld	a, #0x24
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0404
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00106$:
;src/game.c:306: playerrender(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerrender
	pop	af
;src/game.c:307: hudrender();
	call	_hudrender
;src/game.c:309: if (g_victory) {
	ld	a,(#_g_victory + 0)
	or	a, a
	jr	Z,00113$
;src/game.c:310: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
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
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0c20
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
;src/game.c:311: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(5, 5), 24, 8);
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
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0818
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
00113$:
;src/game.c:312: } else if (g_gameover) {
	ld	a,(#_g_gameover + 0)
	or	a, a
	jr	Z,00110$
;src/game.c:313: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
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
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0c20
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
;src/game.c:314: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(6, 6), 24, 8);
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
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0818
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
00110$:
;src/game.c:315: } else if (g_checkpointactive) {
	ld	a,(#_g_checkpointactive + 0)
	or	a, a
	ret	Z
;src/game.c:316: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
	ld	hl, #0x0909
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	ld	a,(#_g_checkpointy + 0)
	add	a, #0xf8
	ld	b, a
	push	de
	push	bc
	inc	sp
	ld	a, (_g_checkpointx)
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	c, l
	ld	b, h
	pop	de
	ld	hl, #0x0802
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
