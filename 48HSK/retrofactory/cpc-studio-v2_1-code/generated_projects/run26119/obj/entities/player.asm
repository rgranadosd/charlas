;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module player
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _collision_is_on_ladder
	.globl _collision_clamp_y_at
	.globl _collision_is_on_ground_at
	.globl _input_is_jump_just_pressed
	.globl _input_is_jump_pressed
	.globl _input_is_down_pressed
	.globl _input_is_up_pressed
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
	ld	hl, #-16
	add	hl, sp
	ld	sp, hl
;src/entities/player.c:34: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:35: return;
	jp	Z,00160$
;src/entities/player.c:38: if (input_is_left_pressed()) {
	call	_input_is_left_pressed
;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	a, 4 (ix)
	ld	-4 (ix), a
	ld	a, 5 (ix)
	ld	-3 (ix), a
	ld	c,-4 (ix)
	ld	b,-3 (ix)
	inc	bc
	inc	bc
;src/entities/player.c:40: player->facing_left = 1;
	ld	a, -4 (ix)
	add	a, #0x07
	ld	-6 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
;src/entities/player.c:38: if (input_is_left_pressed()) {
	ld	a, l
	or	a, a
	jr	Z,00116$
;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
	ld	a, (bc)
	ld	e, a
	ld	hl,#_kplayeracceleration + 0
	ld	d, (hl)
	ld	a, e
	sub	a, d
	ld	(bc), a
;src/entities/player.c:40: player->facing_left = 1;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x01
	jr	00117$
00116$:
;src/entities/player.c:41: } else if (input_is_right_pressed()) {
	push	bc
	call	_input_is_right_pressed
	ld	d, l
	pop	bc
;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	a, (bc)
	ld	e, a
;src/entities/player.c:41: } else if (input_is_right_pressed()) {
	ld	a, d
	or	a, a
	jr	Z,00113$
;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
	ld	hl,#_kplayeracceleration + 0
	ld	d, (hl)
	ld	a, e
	add	a, d
	ld	(bc), a
;src/entities/player.c:43: player->facing_left = 0;
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x00
	jr	00117$
00113$:
;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
	ld	hl,#_kplayerdeceleration + 0
	ld	d, (hl)
;src/entities/player.c:44: } else if (player->vx > 0) {
	xor	a, a
	sub	a, e
	jp	PO, 00278$
	xor	a, #0x80
00278$:
	jp	P, 00110$
;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
	ld	a, e
	sub	a, d
	ld	e,a
	ld	(bc), a
;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
	bit	7, e
	jr	Z,00117$
	xor	a, a
	ld	(bc), a
	jr	00117$
00110$:
;src/entities/player.c:47: } else if (player->vx < 0) {
	bit	7, e
	jr	Z,00117$
;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
	ld	a, e
	add	a, d
	ld	e,a
	ld	(bc), a
;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
	xor	a, a
	sub	a, e
	jp	PO, 00279$
	xor	a, #0x80
00279$:
	jp	P, 00117$
	xor	a, a
	ld	(bc), a
00117$:
;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
	ld	a, (bc)
	ld	d, a
	ld	hl,#_kplayermovespeed + 0
	ld	e, (hl)
	ld	a, e
	sub	a, d
	jp	PO, 00280$
	xor	a, #0x80
00280$:
	jp	P, 00119$
	ld	a, e
	ld	(bc), a
00119$:
;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
	ld	a, (bc)
	ld	d, a
	ld	hl,#_kplayermovespeed + 0
	ld	e, (hl)
	ld	a,e
	ld	l,a
	rla
	sbc	a, a
	ld	h, a
	xor	a, a
	sub	a, l
	ld	-6 (ix), a
	ld	a, #0x00
	sbc	a, h
	ld	-5 (ix), a
	ld	a, d
	rla
	sbc	a, a
	ld	l, a
	ld	a, d
	sub	a, -6 (ix)
	ld	a, l
	sbc	a, -5 (ix)
	jp	PO, 00281$
	xor	a, #0x80
00281$:
	jp	P, 00121$
	xor	a, a
	sub	a, e
	ld	(bc), a
00121$:
;src/entities/player.c:55: player->on_ladder = collision_is_on_ladder((i16)player->x, (i16)player->y, player->w, player->h);
	ld	a, -4 (ix)
	add	a, #0x09
	ld	-6 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
	ld	a, -4 (ix)
	add	a, #0x05
	ld	-8 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	d, (hl)
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	e, (hl)
	ld	a, -4 (ix)
	add	a, #0x01
	ld	-10 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-9 (ix), a
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	l, (hl)
	ld	-2 (ix), l
	ld	-1 (ix), #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	l, (hl)
	ld	-12 (ix), l
	ld	-11 (ix), #0x00
	push	bc
	push	de
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	push	hl
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	push	hl
	call	_collision_is_on_ladder
	pop	af
	pop	af
	pop	af
	ld	e, l
	pop	bc
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), e
;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
	ld	a, -4 (ix)
	add	a, #0x03
	ld	-12 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-11 (ix), a
;src/entities/player.c:59: player->jump_hold = 5;
	ld	a, -4 (ix)
	add	a, #0x08
	ld	-2 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-1 (ix), a
;src/entities/player.c:57: if (!player->on_ladder && input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
	ld	a, e
	or	a, a
	jr	NZ,00123$
	push	bc
	call	_input_is_jump_just_pressed
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00123$
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	l, (hl)
	ld	-14 (ix), l
	ld	-13 (ix), #0x00
	push	bc
	push	af
	inc	sp
	push	de
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00123$
;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
	ld	hl,#_kplayerjumpvelocity + 0
	ld	e, (hl)
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), e
;src/entities/player.c:59: player->jump_hold = 5;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x05
00123$:
;src/entities/player.c:62: if (!player->on_ladder && input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	or	a, a
	jr	NZ,00127$
	push	bc
	call	_input_is_jump_pressed
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00127$
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	a, (hl)
	or	a, a
	jr	Z,00127$
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	e, (hl)
	bit	7, e
	jr	Z,00127$
;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
	ld	hl,#_kplayerjumpboost + 0
	ld	d, (hl)
	ld	a, e
	add	a, d
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), a
;src/entities/player.c:64: player->jump_hold--;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	e, (hl)
	dec	e
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), e
	jr	00128$
00127$:
;src/entities/player.c:66: player->jump_hold = 0;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x00
00128$:
;src/entities/player.c:69: if (player->on_ladder) {
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	or	a, a
	jr	Z,00141$
;src/entities/player.c:70: if (input_is_up_pressed()) {
	push	bc
	call	_input_is_up_pressed
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00136$
;src/entities/player.c:71: player->vy = -2;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0xfe
	jr	00142$
00136$:
;src/entities/player.c:72: } else if (input_is_down_pressed()) {
	push	bc
	call	_input_is_down_pressed
	pop	bc
	ld	a, l
	or	a, a
	jr	Z,00133$
;src/entities/player.c:73: player->vy = 2;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x02
	jr	00142$
00133$:
;src/entities/player.c:75: player->vy = 0;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x00
	jr	00142$
00141$:
;src/entities/player.c:78: player->vy = (i8)(player->vy + kplayergravity);
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	e, (hl)
	ld	hl,#_kplayergravity + 0
	ld	d, (hl)
	ld	a, e
	add	a, d
	ld	d, a
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), d
;src/entities/player.c:79: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
	ld	hl,#_kplayermaxfall + 0
	ld	e, (hl)
	ld	a, e
	sub	a, d
	jp	PO, 00282$
	xor	a, #0x80
00282$:
	jp	P, 00142$
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), e
00142$:
;src/entities/player.c:82: nextx = (i16)player->x + (i16)player->vx;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	a, (bc)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	add	hl, de
;src/entities/player.c:83: if (nextx < 0) {
	bit	7, h
	jr	Z,00144$
;src/entities/player.c:84: nextx = 0;
	ld	hl, #0x0000
00144$:
;src/entities/player.c:86: if (nextx > 76) {
	ld	a, #0x4c
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jp	PO, 00283$
	xor	a, #0x80
00283$:
	jp	P, 00146$
;src/entities/player.c:87: nextx = 76;
	ld	hl, #0x004c
00146$:
;src/entities/player.c:89: player->x = (u8)nextx;
	ld	c, l
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
;src/entities/player.c:91: nexty = (i16)player->y + (i16)player->vy;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	c, (hl)
	ld	b, #0x00
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	l, (hl)
	ld	a, l
	rla
	sbc	a, a
	ld	h, a
	add	hl, bc
	inc	sp
	inc	sp
	push	hl
;src/entities/player.c:92: if (player->on_ladder) {
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	c, (hl)
;src/entities/player.c:55: player->on_ladder = collision_is_on_ladder((i16)player->x, (i16)player->y, player->w, player->h);
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	ld	-14 (ix), a
;src/entities/player.c:92: if (player->on_ladder) {
	ld	a, c
	or	a, a
	jr	Z,00152$
;src/entities/player.c:93: if (nexty < 40) nexty = 40;
	ld	a, -16 (ix)
	sub	a, #0x28
	ld	a, -15 (ix)
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	NC,00148$
	ld	hl, #0x0028
	ex	(sp), hl
00148$:
;src/entities/player.c:94: if (nexty > 160 - player->h) nexty = 160 - player->h;
	ld	c, -14 (ix)
	ld	b, #0x00
	ld	a, #0xa0
	sub	a, c
	ld	c, a
	ld	a, #0x00
	sbc	a, b
	ld	b, a
	ld	a, c
	sub	a, -16 (ix)
	ld	a, b
	sbc	a, -15 (ix)
	jp	PO, 00284$
	xor	a, #0x80
00284$:
	jp	P, 00153$
	inc	sp
	inc	sp
	push	bc
	jr	00153$
00152$:
;src/entities/player.c:96: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	c, (hl)
	ld	b, #0x00
	ld	a, -14 (ix)
	push	af
	inc	sp
	ld	l,-16 (ix)
	ld	h,-15 (ix)
	push	hl
	push	bc
	call	_collision_clamp_y_at
	pop	af
	pop	af
	inc	sp
	inc	sp
	inc	sp
	push	hl
00153$:
;src/entities/player.c:98: if (nexty < 0) {
	bit	7, -15 (ix)
	jr	Z,00155$
;src/entities/player.c:99: nexty = 0;
	ld	hl, #0x0000
	ex	(sp), hl
00155$:
;src/entities/player.c:101: player->y = (u8)nexty;
	ld	c, -16 (ix)
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), c
;src/entities/player.c:103: if (!player->on_ladder && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	or	a, a
	jr	NZ,00160$
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	c, (hl)
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	l, (hl)
	ld	h, #0x00
	ld	a, c
	push	af
	inc	sp
	push	de
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	ld	a, l
	or	a, a
	jr	Z,00160$
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	c, (hl)
	xor	a, a
	sub	a, c
	jp	PO, 00285$
	xor	a, #0x80
00285$:
	jp	P, 00160$
;src/entities/player.c:104: player->vy = 0;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x00
00160$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/player.c:108: void playerrender(const Player* player) {
;	---------------------------------
; Function playerrender
; ---------------------------------
_playerrender::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/player.c:111: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:112: return;
	jr	Z,00103$
;src/entities/player.c:115: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
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
;src/entities/player.c:116: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
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
