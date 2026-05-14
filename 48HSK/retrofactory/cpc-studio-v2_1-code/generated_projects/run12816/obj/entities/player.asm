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
;src/entities/player.c:14: void playerinit(Player* player) {
;	---------------------------------
; Function playerinit
; ---------------------------------
_playerinit::
;src/entities/player.c:15: if (!player) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/player.c:16: return;
	ret	Z
;src/entities/player.c:19: player->x = 20;
	pop	de
	pop	bc
	push	bc
	push	de
	ld	a, #0x14
	ld	(bc), a
;src/entities/player.c:20: player->y = 120;
	ld	l, c
	ld	h, b
	inc	hl
	ld	(hl), #0x78
;src/entities/player.c:21: player->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:22: player->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:23: player->w = 4;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x04
;src/entities/player.c:24: player->h = 16;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x10
;src/entities/player.c:25: player->health = 3;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x03
;src/entities/player.c:26: player->facing_left = 0;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x00
;src/entities/player.c:27: player->jump_hold = 0;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x00
	ret
_kplayermovespeed:
	.db #0x03	;  3
_kplayeracceleration:
	.db #0x01	;  1
_kplayerdeceleration:
	.db #0x01	;  1
_kplayergravity:
	.db #0x01	;  1
_kplayermaxfall:
	.db #0x04	;  4
_kplayerjumpvelocity:
	.db #0xfa	; -6
_kplayerjumpboost:
	.db #0xff	; -1
;src/entities/player.c:30: void playerupdate(Player* player) {
;	---------------------------------
; Function playerupdate
; ---------------------------------
_playerupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-19
	add	hl, sp
	ld	sp, hl
;src/entities/player.c:34: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:35: return;
	jp	Z,00141$
;src/entities/player.c:38: if (input_is_left_pressed()) {
	call	_input_is_left_pressed
	ld	c, l
;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	a, 4 (ix)
	ld	-2 (ix), a
	ld	a, 5 (ix)
	ld	-1 (ix), a
	ld	a, -2 (ix)
	add	a, #0x02
	ld	-4 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-3 (ix), a
;src/entities/player.c:40: player->facing_left = 1;
	ld	a, -2 (ix)
	add	a, #0x07
	ld	-6 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
;src/entities/player.c:38: if (input_is_left_pressed()) {
	ld	a, c
	or	a, a
	jr	Z,00116$
;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	c, (hl)
	ld	hl,#_kplayeracceleration + 0
	ld	b, (hl)
	ld	a, c
	sub	a, b
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), a
;src/entities/player.c:40: player->facing_left = 1;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x01
	jr	00117$
00116$:
;src/entities/player.c:41: } else if (input_is_right_pressed()) {
	call	_input_is_right_pressed
	ld	a, l
;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	c, (hl)
;src/entities/player.c:41: } else if (input_is_right_pressed()) {
	or	a, a
	jr	Z,00113$
;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
	ld	hl,#_kplayeracceleration + 0
	ld	e, (hl)
	ld	a, c
	add	a, e
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), a
;src/entities/player.c:43: player->facing_left = 0;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x00
	jr	00117$
00113$:
;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
	ld	hl,#_kplayerdeceleration + 0
	ld	b, (hl)
;src/entities/player.c:44: } else if (player->vx > 0) {
	xor	a, a
	sub	a, c
	jp	PO, 00223$
	xor	a, #0x80
00223$:
	jp	P, 00110$
;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
	ld	a, c
	sub	a, b
	ld	c, a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
	bit	7, c
	jr	Z,00117$
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x00
	jr	00117$
00110$:
;src/entities/player.c:47: } else if (player->vx < 0) {
	bit	7, c
	jr	Z,00117$
;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
	ld	a, c
	add	a, b
	ld	c, a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
	xor	a, a
	sub	a, c
	jp	PO, 00224$
	xor	a, #0x80
00224$:
	jp	P, 00117$
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x00
00117$:
;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	b, (hl)
	ld	hl,#_kplayermovespeed + 0
	ld	c, (hl)
	ld	a, c
	sub	a, b
	jp	PO, 00225$
	xor	a, #0x80
00225$:
	jp	P, 00119$
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
00119$:
;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	a, (hl)
	ld	-6 (ix), a
	ld	a,(#_kplayermovespeed + 0)
	ld	-7 (ix), a
	ld	-9 (ix), a
	ld	a, -7 (ix)
	rla
	sbc	a, a
	ld	-8 (ix), a
	xor	a, a
	sub	a, -9 (ix)
	ld	-9 (ix), a
	ld	a, #0x00
	sbc	a, -8 (ix)
	ld	-8 (ix), a
	ld	a, -6 (ix)
	ld	-6 (ix), a
	rla
	sbc	a, a
	ld	-5 (ix), a
	ld	a, -6 (ix)
	sub	a, -9 (ix)
	ld	a, -5 (ix)
	sbc	a, -8 (ix)
	jp	PO, 00226$
	xor	a, #0x80
00226$:
	jp	P, 00121$
	xor	a, a
	sub	a, -7 (ix)
	ld	c, a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
00121$:
;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	call	_input_is_jump_just_pressed
	ld	-9 (ix), l
	ld	a, -2 (ix)
	add	a, #0x05
	ld	-6 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
	ld	a, -2 (ix)
	add	a, #0x01
	ld	-11 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-10 (ix), a
;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
	ld	a, -2 (ix)
	add	a, #0x03
	ld	-13 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-12 (ix), a
;src/entities/player.c:57: player->jump_hold = 5;
	ld	a, -2 (ix)
	add	a, #0x08
	ld	-15 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-14 (ix), a
;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	ld	a, -9 (ix)
	or	a, a
	jr	Z,00123$
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	ld	l,-11 (ix)
	ld	h,-10 (ix)
	ld	c, (hl)
	ld	b, #0x00
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	e, (hl)
	ld	d, #0x00
	push	af
	inc	sp
	push	bc
	push	de
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	ld	a, l
	or	a, a
	jr	Z,00123$
;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
	ld	hl,#_kplayerjumpvelocity + 0
	ld	c, (hl)
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), c
;src/entities/player.c:57: player->jump_hold = 5;
	ld	l,-15 (ix)
	ld	h,-14 (ix)
	ld	(hl), #0x05
00123$:
;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
	call	_input_is_jump_pressed
	ld	-9 (ix), l
	ld	a, l
	or	a, a
	jr	Z,00126$
	ld	l,-15 (ix)
	ld	h,-14 (ix)
	ld	a, (hl)
	ld	-9 (ix), a
	or	a, a
	jr	Z,00126$
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	a, (hl)
	ld	-9 (ix), a
	bit	7, -9 (ix)
	jr	Z,00126$
;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
	ld	a,(#_kplayerjumpboost + 0)
	ld	-7 (ix), a
	ld	a, -9 (ix)
	add	a, -7 (ix)
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), a
;src/entities/player.c:62: player->jump_hold--;
	ld	l,-15 (ix)
	ld	h,-14 (ix)
	ld	c, (hl)
	dec	c
	ld	l,-15 (ix)
	ld	h,-14 (ix)
	ld	(hl), c
	jr	00127$
00126$:
;src/entities/player.c:64: player->jump_hold = 0;
	ld	l,-15 (ix)
	ld	h,-14 (ix)
	ld	(hl), #0x00
00127$:
;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	c, (hl)
	ld	hl,#_kplayergravity + 0
	ld	b, (hl)
	ld	a, c
	add	a, b
	ld	c, a
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), c
;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
	ld	hl,#_kplayermaxfall + 0
	ld	b, (hl)
	ld	a, b
	sub	a, c
	jp	PO, 00227$
	xor	a, #0x80
00227$:
	jp	P, 00131$
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), b
00131$:
;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	c, (hl)
	ld	-15 (ix), c
	ld	-14 (ix), #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	a, (hl)
	ld	-9 (ix), a
	ld	-9 (ix), a
	rla
	sbc	a, a
	ld	-8 (ix), a
	ld	a, -9 (ix)
	add	a, -15 (ix)
	ld	-17 (ix), a
	ld	a, -8 (ix)
	adc	a, -14 (ix)
	ld	-16 (ix), a
;src/entities/player.c:71: if (nextx < 0) {
	bit	7, -16 (ix)
	jr	Z,00133$
;src/entities/player.c:72: nextx = 0;
	ld	-17 (ix), #0x00
	ld	-16 (ix), #0x00
00133$:
;src/entities/player.c:74: if (nextx > 76) {
	ld	a, #0x4c
	cp	a, -17 (ix)
	ld	a, #0x00
	sbc	a, -16 (ix)
	jp	PO, 00228$
	xor	a, #0x80
00228$:
	jp	P, 00135$
;src/entities/player.c:75: nextx = 76;
	ld	-17 (ix), #0x4c
	ld	-16 (ix), #0x00
00135$:
;src/entities/player.c:77: player->x = (u8)nextx;
	ld	a, -17 (ix)
	ld	-15 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	a, -15 (ix)
	ld	(hl), a
;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
	ld	l,-11 (ix)
	ld	h,-10 (ix)
	ld	c, (hl)
	ld	-9 (ix), c
	ld	-8 (ix), #0x00
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	a, (hl)
	ld	-4 (ix), a
	rla
	sbc	a, a
	ld	-3 (ix), a
	ld	a, -4 (ix)
	add	a, -9 (ix)
	ld	-9 (ix), a
	ld	a, -3 (ix)
	adc	a, -8 (ix)
	ld	-8 (ix), a
;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	ld	-7 (ix), a
	ld	a, -15 (ix)
	ld	-15 (ix), a
	ld	-14 (ix), #0x00
	ld	a, -7 (ix)
	push	af
	inc	sp
	ld	l,-9 (ix)
	ld	h,-8 (ix)
	push	hl
	ld	l,-15 (ix)
	ld	h,-14 (ix)
	push	hl
	call	_collision_clamp_y_at
	pop	af
	pop	af
	inc	sp
	ld	-14 (ix), h
	ld	-15 (ix), l
	ld	-19 (ix), l
	ld	a, -14 (ix)
	ld	-18 (ix), a
;src/entities/player.c:81: if (nexty < 0) {
	bit	7, -18 (ix)
	jr	Z,00137$
;src/entities/player.c:82: nexty = 0;
	ld	hl, #0x0000
	ex	(sp), hl
00137$:
;src/entities/player.c:84: player->y = (u8)nexty;
	ld	c, -19 (ix)
	ld	l,-11 (ix)
	ld	h,-10 (ix)
	ld	(hl), c
;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	ld	b, #0x00
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	e, (hl)
	ld	d, #0x00
	push	af
	inc	sp
	push	bc
	push	de
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	ld	a, l
	or	a, a
	jr	Z,00141$
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	c, (hl)
	xor	a, a
	sub	a, c
	jp	PO, 00229$
	xor	a, #0x80
00229$:
	jp	P, 00141$
;src/entities/player.c:87: player->vy = 0;
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), #0x00
00141$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/player.c:91: void playerrender(const Player* player) {
;	---------------------------------
; Function playerrender
; ---------------------------------
_playerrender::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/player.c:94: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:95: return;
	jr	Z,00103$
;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
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
;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
	push	de
	pop	iy
	ld	a, 5 (iy)
	ex	de,hl
	ld	de, #0x0004
	add	hl, de
	ld	d, (hl)
	push	af
	inc	sp
	ld	e, #0x4f
	push	de
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00103$:
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
