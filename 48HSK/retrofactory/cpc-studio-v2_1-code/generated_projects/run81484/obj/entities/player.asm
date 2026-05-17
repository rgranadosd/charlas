;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module player
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _collision_clamp_y_at
	.globl _collision_is_on_ground_at
	.globl _input_is_jump_just_pressed
	.globl _input_is_jump_pressed
	.globl _input_is_right_pressed
	.globl _input_is_left_pressed
	.globl _cpct_getScreenPtr
	.globl _cpct_hflipSpriteM0
	.globl _cpct_drawSprite
	.globl _playerinit
	.globl _playerupdate
	.globl _playerrender
	.globl _player_get_ammo
	.globl _player_get_health
	.globl _player_get_weapon
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
_gplayersprite:
	.ds 192
_gplayerspritefacingleft:
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
;src/entities/player.c:21: void playerinit(Player* player) {
;	---------------------------------
; Function playerinit
; ---------------------------------
_playerinit::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/player.c:23: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:24: return;
	jr	Z,00106$
;src/entities/player.c:27: player->x = 4;
	ld	c,4 (ix)
	ld	b,5 (ix)
	ld	a, #0x04
	ld	(bc), a
;src/entities/player.c:28: player->y = (u8)(104);  /* groundy(128) - h(24) = 104: feet at ground level */
	ld	l, c
	ld	h, b
	inc	hl
	ld	(hl), #0x68
;src/entities/player.c:29: player->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:30: player->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:31: player->w = 8;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x08
;src/entities/player.c:32: player->h = 24;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x18
;src/entities/player.c:33: player->health = 3;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x03
;src/entities/player.c:34: player->weapon = 0;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x00
;src/entities/player.c:35: player->facing_left = 0;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x00
;src/entities/player.c:36: player->jump_hold = 0;
	ld	hl, #0x0009
	add	hl, bc
	ld	(hl), #0x00
;src/entities/player.c:37: for (index = 0; index < kplayerspritebytes; ++index) {
	ld	c, #0x00
00104$:
;src/entities/player.c:38: gplayersprite[index] = sprplayerknight_data[index];
	ld	a, #<(_gplayersprite)
	add	a, c
	ld	e, a
	ld	a, #>(_gplayersprite)
	adc	a, #0x00
	ld	d, a
	ld	hl, #_sprplayerknight_data
	ld	b, #0x00
	add	hl, bc
	ld	a, (hl)
	ld	(de), a
;src/entities/player.c:37: for (index = 0; index < kplayerspritebytes; ++index) {
	inc	c
	ld	a, c
	sub	a, #0xc0
	jr	C,00104$
;src/entities/player.c:40: gplayerspritefacingleft = 0;
	ld	hl,#_gplayerspritefacingleft + 0
	ld	(hl), #0x00
00106$:
	pop	ix
	ret
;src/entities/player.c:43: void playerupdate(Player* player) {
;	---------------------------------
; Function playerupdate
; ---------------------------------
_playerupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-14
	add	hl, sp
	ld	sp, hl
;src/entities/player.c:47: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:48: return;
	jp	Z,00141$
;src/entities/player.c:51: if (input_is_left_pressed()) {
	call	_input_is_left_pressed
;src/entities/player.c:52: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	c,4 (ix)
	ld	b,5 (ix)
	ld	e, c
	ld	d, b
	inc	de
	inc	de
;src/entities/player.c:53: player->facing_left = 1;
	ld	a, c
	add	a, #0x08
	ld	-14 (ix), a
	ld	a, b
	adc	a, #0x00
	ld	-13 (ix), a
;src/entities/player.c:51: if (input_is_left_pressed()) {
	ld	a, l
	or	a, a
	jr	Z,00116$
;src/entities/player.c:52: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	a, (de)
	add	a, #0xfe
	ld	(de), a
;src/entities/player.c:53: player->facing_left = 1;
	pop	hl
	push	hl
	ld	(hl), #0x01
	jr	00117$
00116$:
;src/entities/player.c:54: } else if (input_is_right_pressed()) {
	push	bc
	push	de
	call	_input_is_right_pressed
	ld	-1 (ix), l
	pop	de
	pop	bc
;src/entities/player.c:65: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	a, (de)
;src/entities/player.c:55: player->vx = (i8)(player->vx + kplayeracceleration);
	ld	l,a
	add	a, #0x02
	ld	-2 (ix), a
;src/entities/player.c:54: } else if (input_is_right_pressed()) {
	ld	a, -1 (ix)
	or	a, a
	jr	Z,00113$
;src/entities/player.c:55: player->vx = (i8)(player->vx + kplayeracceleration);
	ld	a, -2 (ix)
	ld	(de), a
;src/entities/player.c:56: player->facing_left = 0;
	pop	hl
	push	hl
	ld	(hl), #0x00
	jr	00117$
00113$:
;src/entities/player.c:57: } else if (player->vx > 0) {
	xor	a, a
	sub	a, l
	jp	PO, 00223$
	xor	a, #0x80
00223$:
	jp	P, 00110$
;src/entities/player.c:58: player->vx = (i8)(player->vx - kplayerdeceleration);
	ld	a, l
	add	a, #0xfe
	ld	-1 (ix), a
	ld	(de),a
;src/entities/player.c:59: if (player->vx < 0) player->vx = 0;
	bit	7, -1 (ix)
	jr	Z,00117$
	xor	a, a
	ld	(de), a
	jr	00117$
00110$:
;src/entities/player.c:60: } else if (player->vx < 0) {
	bit	7, l
	jr	Z,00117$
;src/entities/player.c:61: player->vx = (i8)(player->vx + kplayerdeceleration);
	ld	a, -2 (ix)
	ld	(de), a
;src/entities/player.c:62: if (player->vx > 0) player->vx = 0;
	xor	a, a
	sub	a, -2 (ix)
	jp	PO, 00224$
	xor	a, #0x80
00224$:
	jp	P, 00117$
	xor	a, a
	ld	(de), a
00117$:
;src/entities/player.c:65: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	a, (de)
	ld	l, a
	ld	a, #0x02
	sub	a, l
	jp	PO, 00225$
	xor	a, #0x80
00225$:
	jp	P, 00119$
	ld	a, #0x02
	ld	(de), a
00119$:
;src/entities/player.c:66: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
	ld	a, (de)
	xor	a, #0x80
	sub	a, #0x7e
	jr	NC,00121$
	ld	a, #0xfe
	ld	(de), a
00121$:
;src/entities/player.c:68: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	push	bc
	push	de
	call	_input_is_jump_just_pressed
	ld	-2 (ix), l
	pop	de
	pop	bc
	ld	hl, #0x0005
	add	hl,bc
	ex	(sp), hl
	ld	hl, #0x0001
	add	hl,bc
	ld	-4 (ix), l
	ld	-3 (ix), h
;src/entities/player.c:69: player->vy = kplayerjumpvelocity;
	ld	hl, #0x0003
	add	hl,bc
	ld	-6 (ix), l
	ld	-5 (ix), h
;src/entities/player.c:70: player->jump_hold = 5;
	ld	hl, #0x0009
	add	hl,bc
	ld	-8 (ix), l
	ld	-7 (ix), h
;src/entities/player.c:68: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	ld	a, -2 (ix)
	or	a, a
	jr	Z,00123$
	pop	hl
	push	hl
	ld	a, (hl)
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	l, (hl)
	ld	-10 (ix), l
	ld	-9 (ix), #0x00
	push	af
	ld	a, (bc)
	ld	l, a
	pop	af
	ld	-12 (ix), l
	ld	-11 (ix), #0x00
	push	bc
	push	de
	push	af
	inc	sp
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	push	hl
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	pop	de
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00123$
;src/entities/player.c:69: player->vy = kplayerjumpvelocity;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0xfa
;src/entities/player.c:70: player->jump_hold = 5;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x05
00123$:
;src/entities/player.c:73: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
	push	bc
	push	de
	call	_input_is_jump_pressed
	ld	a, l
	pop	de
	pop	bc
	or	a, a
	jr	Z,00126$
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	or	a, a
	jr	Z,00126$
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	l, (hl)
	bit	7, l
	jr	Z,00126$
;src/entities/player.c:74: player->vy = (i8)(player->vy + kplayerjumpboost);
	ld	a, l
	add	a, #0xff
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), a
;src/entities/player.c:75: player->jump_hold--;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	add	a, #0xff
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), a
	jr	00127$
00126$:
;src/entities/player.c:77: player->jump_hold = 0;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x00
00127$:
;src/entities/player.c:80: player->vy = (i8)(player->vy + kplayergravity);
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	inc	a
	ld	-12 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, -12 (ix)
	ld	(hl), a
;src/entities/player.c:81: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
	ld	a, #0x04
	sub	a, -12 (ix)
	jp	PO, 00226$
	xor	a, #0x80
00226$:
	jp	P, 00131$
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x04
00131$:
;src/entities/player.c:83: nextx = (i16)player->x + (i16)player->vx;
	ld	a, (bc)
	ld	-12 (ix), a
	ld	-11 (ix), #0x00
	ld	a, (de)
	ld	e, a
	rla
	sbc	a, a
	ld	d, a
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	add	hl, de
;src/entities/player.c:84: if (nextx < 0) {
	bit	7, h
	jr	Z,00133$
;src/entities/player.c:85: nextx = 0;
	ld	hl, #0x0000
00133$:
;src/entities/player.c:87: if (nextx > 72) {
	ld	a, #0x48
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jp	PO, 00227$
	xor	a, #0x80
00227$:
	jp	P, 00135$
;src/entities/player.c:88: nextx = 72;
	ld	hl, #0x0048
00135$:
;src/entities/player.c:90: player->x = (u8)nextx;
	ld	-12 (ix), l
	ld	a, l
	ld	(bc), a
;src/entities/player.c:92: nexty = (i16)player->y + (i16)player->vy;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	l, (hl)
	ld	a, l
	rla
	sbc	a, a
	ld	h, a
	add	hl, de
	push	hl
	pop	iy
;src/entities/player.c:93: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
	pop	hl
	push	hl
	ld	h, (hl)
	ld	e, -12 (ix)
	ld	d, #0x00
	push	bc
	push	hl
	inc	sp
	push	iy
	push	de
	call	_collision_clamp_y_at
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/entities/player.c:94: if (nexty < 0) {
	bit	7, h
	jr	Z,00137$
;src/entities/player.c:95: nexty = 0;
	ld	hl, #0x0000
00137$:
;src/entities/player.c:97: player->y = (u8)nexty;
	ld	e, l
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), e
;src/entities/player.c:99: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
	pop	hl
	push	hl
	ld	a, (hl)
	ld	d, #0x00
	push	af
	ld	a, (bc)
	ld	c, a
	pop	af
	ld	b, #0x00
	push	af
	inc	sp
	push	de
	push	bc
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	ld	a, l
	or	a, a
	jr	Z,00141$
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	c, (hl)
	xor	a, a
	sub	a, c
	jp	PO, 00228$
	xor	a, #0x80
00228$:
	jp	P, 00141$
;src/entities/player.c:100: player->vy = 0;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x00
00141$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/player.c:104: void playerrender(const Player* player) {
;	---------------------------------
; Function playerrender
; ---------------------------------
_playerrender::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-7
	add	hl, sp
	ld	sp, hl
;src/entities/player.c:107: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:108: return;
	jr	Z,00105$
;src/entities/player.c:111: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
	ld	e,4 (ix)
	ld	d,5 (ix)
	ld	l, e
	ld	h, d
	inc	hl
	ld	b, (hl)
	ld	a, (de)
	push	de
	push	bc
	inc	sp
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	c, l
	ld	b, h
	pop	de
;src/entities/player.c:112: if (player->facing_left != gplayerspritefacingleft) {
	ld	hl, #0x0008
	add	hl,de
	ld	-2 (ix), l
	ld	-1 (ix), h
	ld	a, (hl)
	ld	-3 (ix), a
;src/entities/player.c:113: cpct_hflipSpriteM0(player->w, player->h, gplayersprite);
	ld	hl, #0x0005
	add	hl,de
	ld	-5 (ix), l
	ld	-4 (ix), h
	ld	hl, #0x0004
	add	hl,de
	ex	(sp), hl
;src/entities/player.c:112: if (player->facing_left != gplayerspritefacingleft) {
	ld	a,(#_gplayerspritefacingleft + 0)
	sub	a, -3 (ix)
	jr	Z,00104$
;src/entities/player.c:113: cpct_hflipSpriteM0(player->w, player->h, gplayersprite);
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	e, (hl)
	pop	hl
	push	hl
	ld	d, (hl)
	push	bc
	ld	hl, #_gplayersprite
	push	hl
	ld	a, e
	push	af
	inc	sp
	push	de
	inc	sp
	call	_cpct_hflipSpriteM0
	pop	bc
;src/entities/player.c:114: gplayerspritefacingleft = player->facing_left;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	a, (hl)
	ld	(#_gplayerspritefacingleft + 0),a
00104$:
;src/entities/player.c:116: cpct_drawSprite(gplayersprite, pvmem, player->w, player->h);
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	e, (hl)
	pop	hl
	push	hl
	ld	d, (hl)
	ld	a, e
	push	af
	inc	sp
	push	de
	inc	sp
	push	bc
	ld	hl, #_gplayersprite
	push	hl
	call	_cpct_drawSprite
00105$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/player.c:119: u8 player_get_ammo(const Player* player) {
;	---------------------------------
; Function player_get_ammo
; ---------------------------------
_player_get_ammo::
;src/entities/player.c:121: return 3;
	ld	l, #0x03
	ret
;src/entities/player.c:124: u8 player_get_health(const Player* player) {
;	---------------------------------
; Function player_get_health
; ---------------------------------
_player_get_health::
;src/entities/player.c:125: return player ? player->health : 0;
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
	jr	Z,00103$
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	de, #0x0006
	add	hl, de
	ld	l, (hl)
	ret
00103$:
	ld	l, #0x00
	ret
;src/entities/player.c:128: u8 player_get_weapon(const Player* player) {
;	---------------------------------
; Function player_get_weapon
; ---------------------------------
_player_get_weapon::
;src/entities/player.c:129: return player ? player->weapon : 0;
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
	jr	Z,00103$
	pop	bc
	pop	hl
	push	hl
	push	bc
	ld	de, #0x0007
	add	hl, de
	ld	l, (hl)
	ret
00103$:
	ld	l, #0x00
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
