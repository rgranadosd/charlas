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
	.globl _cpct_drawSolidBox
	.globl _cpct_px2byteM0
	.globl _playerinit
	.globl _playerupdate
	.globl _playerrender
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
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
;src/entities/player.c:16: void playerinit(Player* player) {
;	---------------------------------
; Function playerinit
; ---------------------------------
_playerinit::
;src/entities/player.c:17: if (!player) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/player.c:18: return;
	ret	Z
;src/entities/player.c:21: player->x = 20;
	pop	de
	pop	bc
	push	bc
	push	de
	ld	a, #0x14
	ld	(bc), a
;src/entities/player.c:22: player->y = 120;
	ld	l, c
	ld	h, b
	inc	hl
	ld	(hl), #0x78
;src/entities/player.c:23: player->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:24: player->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:25: player->w = 4;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x04
;src/entities/player.c:26: player->h = 16;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x10
;src/entities/player.c:27: player->health = 3;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x03
;src/entities/player.c:28: player->facing_left = 0;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x00
;src/entities/player.c:29: player->jump_hold = 0;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x00
	ret
;src/entities/player.c:32: void playerupdate(Player* player) {
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
;src/entities/player.c:36: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:37: return;
	jp	Z,00141$
;src/entities/player.c:40: if (input_is_left_pressed()) {
	call	_input_is_left_pressed
;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	c,4 (ix)
	ld	b,5 (ix)
	ld	e, c
	ld	d, b
	inc	de
	inc	de
;src/entities/player.c:42: player->facing_left = 1;
	ld	a, c
	add	a, #0x07
	ld	-4 (ix), a
	ld	a, b
	adc	a, #0x00
	ld	-3 (ix), a
;src/entities/player.c:40: if (input_is_left_pressed()) {
	ld	a, l
	or	a, a
	jr	Z,00116$
;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	a, (de)
	add	a, #0xff
	ld	(de), a
;src/entities/player.c:42: player->facing_left = 1;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x01
	jr	00117$
00116$:
;src/entities/player.c:43: } else if (input_is_right_pressed()) {
	push	bc
	push	de
	call	_input_is_right_pressed
	ld	-1 (ix), l
	pop	de
	pop	bc
;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	a, (de)
;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
	ld	l,a
	inc	a
	ld	-2 (ix), a
;src/entities/player.c:43: } else if (input_is_right_pressed()) {
	ld	a, -1 (ix)
	or	a, a
	jr	Z,00113$
;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
	ld	a, -2 (ix)
	ld	(de), a
;src/entities/player.c:45: player->facing_left = 0;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x00
	jr	00117$
00113$:
;src/entities/player.c:46: } else if (player->vx > 0) {
	xor	a, a
	sub	a, l
	jp	PO, 00223$
	xor	a, #0x80
00223$:
	jp	P, 00110$
;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
	ld	a, l
	add	a, #0xff
	ld	-1 (ix), a
	ld	(de),a
;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
	bit	7, -1 (ix)
	jr	Z,00117$
	xor	a, a
	ld	(de), a
	jr	00117$
00110$:
;src/entities/player.c:49: } else if (player->vx < 0) {
	bit	7, l
	jr	Z,00117$
;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
	ld	a, -2 (ix)
	ld	(de), a
;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
	xor	a, a
	sub	a, -2 (ix)
	jp	PO, 00224$
	xor	a, #0x80
00224$:
	jp	P, 00117$
	xor	a, a
	ld	(de), a
00117$:
;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	a, (de)
	ld	l, a
	ld	a, #0x03
	sub	a, l
	jp	PO, 00225$
	xor	a, #0x80
00225$:
	jp	P, 00119$
	ld	a, #0x03
	ld	(de), a
00119$:
;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
	ld	a, (de)
	xor	a, #0x80
	sub	a, #0x7d
	jr	NC,00121$
	ld	a, #0xfd
	ld	(de), a
00121$:
;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	push	bc
	push	de
	call	_input_is_jump_just_pressed
	ld	-2 (ix), l
	pop	de
	pop	bc
	ld	hl, #0x0005
	add	hl,bc
	ld	-4 (ix), l
	ld	-3 (ix), h
	ld	hl, #0x0001
	add	hl,bc
	ld	-6 (ix), l
	ld	-5 (ix), h
;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
	ld	hl, #0x0003
	add	hl,bc
	ld	-8 (ix), l
	ld	-7 (ix), h
;src/entities/player.c:59: player->jump_hold = 5;
	ld	hl, #0x0008
	add	hl,bc
	ld	-10 (ix), l
	ld	-9 (ix), h
;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	ld	a, -2 (ix)
	or	a, a
	jr	Z,00123$
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	a, (hl)
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	l, (hl)
	ld	-12 (ix), l
	ld	-11 (ix), #0x00
	push	af
	ld	a, (bc)
	ld	l, a
	pop	af
	ld	-14 (ix), l
	ld	-13 (ix), #0x00
	push	bc
	push	de
	push	af
	inc	sp
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	push	hl
	ld	l,-14 (ix)
	ld	h,-13 (ix)
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
;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0xfa
;src/entities/player.c:59: player->jump_hold = 5;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), #0x05
00123$:
;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
	push	bc
	push	de
	call	_input_is_jump_pressed
	ld	a, l
	pop	de
	pop	bc
	or	a, a
	jr	Z,00126$
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	a, (hl)
	or	a, a
	jr	Z,00126$
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	l, (hl)
	bit	7, l
	jr	Z,00126$
;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
	ld	a, l
	add	a, #0xff
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), a
;src/entities/player.c:64: player->jump_hold--;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	a, (hl)
	add	a, #0xff
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), a
	jr	00127$
00126$:
;src/entities/player.c:66: player->jump_hold = 0;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), #0x00
00127$:
;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	inc	a
	ld	-14 (ix), a
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, -14 (ix)
	ld	(hl), a
;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
	ld	a, #0x04
	sub	a, -14 (ix)
	jp	PO, 00226$
	xor	a, #0x80
00226$:
	jp	P, 00131$
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x04
00131$:
;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
	ld	a, (bc)
	ld	-14 (ix), a
	ld	-13 (ix), #0x00
	ld	a, (de)
	ld	e, a
	rla
	sbc	a, a
	ld	d, a
	pop	hl
	push	hl
	add	hl, de
;src/entities/player.c:73: if (nextx < 0) {
	bit	7, h
	jr	Z,00133$
;src/entities/player.c:74: nextx = 0;
	ld	hl, #0x0000
00133$:
;src/entities/player.c:76: if (nextx > 76) {
	ld	a, #0x4c
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jp	PO, 00227$
	xor	a, #0x80
00227$:
	jp	P, 00135$
;src/entities/player.c:77: nextx = 76;
	ld	hl, #0x004c
00135$:
;src/entities/player.c:79: player->x = (u8)nextx;
	ld	-14 (ix), l
	ld	a, l
	ld	(bc), a
;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	l, (hl)
	ld	a, l
	rla
	sbc	a, a
	ld	h, a
	add	hl, de
	push	hl
	pop	iy
;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	h, (hl)
	ld	e, -14 (ix)
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
;src/entities/player.c:83: if (nexty < 0) {
	bit	7, h
	jr	Z,00137$
;src/entities/player.c:84: nexty = 0;
	ld	hl, #0x0000
00137$:
;src/entities/player.c:86: player->y = (u8)nexty;
	ld	e, l
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), e
;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
	ld	l,-4 (ix)
	ld	h,-3 (ix)
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
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	c, (hl)
	xor	a, a
	sub	a, c
	jp	PO, 00228$
	xor	a, #0x80
00228$:
	jp	P, 00141$
;src/entities/player.c:89: player->vy = 0;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x00
00141$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/player.c:93: void playerrender(const Player* player) {
;	---------------------------------
; Function playerrender
; ---------------------------------
_playerrender::
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/entities/player.c:96: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:97: return;
	jr	Z,00103$
;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
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
;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
	push	de
	pop	iy
	ld	a, 5 (iy)
	ld	-1 (ix), a
	ex	de,hl
	ld	de, #0x0004
	add	hl, de
	ld	d, (hl)
	push	bc
	push	de
	ld	hl, #0x0606
	push	hl
	call	_cpct_px2byteM0
	ld	e, l
	pop	af
	ld	d, a
	pop	bc
	ld	a, -1 (ix)
	push	af
	inc	sp
	push	de
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00103$:
	inc	sp
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
