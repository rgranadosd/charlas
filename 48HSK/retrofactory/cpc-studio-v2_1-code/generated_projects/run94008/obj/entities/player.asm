;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module player
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _collision_clamp_y_to_ground
	.globl _collision_is_on_ground
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
;src/entities/player.c:10: void playerinit(Player* player) {
;	---------------------------------
; Function playerinit
; ---------------------------------
_playerinit::
;src/entities/player.c:11: if (!player) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/player.c:12: return;
	ret	Z
;src/entities/player.c:15: player->x = 20;
	pop	de
	pop	bc
	push	bc
	push	de
	ld	a, #0x14
	ld	(bc), a
;src/entities/player.c:16: player->y = 120;
	ld	l, c
	ld	h, b
	inc	hl
	ld	(hl), #0x78
;src/entities/player.c:17: player->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:18: player->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/player.c:19: player->w = 4;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x04
;src/entities/player.c:20: player->h = 16;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x10
	ret
_kplayermovespeed:
	.db #0x02	;  2
_kplayergravity:
	.db #0x01	;  1
_kplayerjumpvelocity:
	.db #0xfb	; -5
;src/entities/player.c:23: void playerupdate(Player* player) {
;	---------------------------------
; Function playerupdate
; ---------------------------------
_playerupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-8
	add	hl, sp
	ld	sp, hl
;src/entities/player.c:27: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:28: return;
	jp	Z,00120$
;src/entities/player.c:31: player->vx = 0;
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
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x00
;src/entities/player.c:32: if (input_is_left_pressed()) {
	call	_input_is_left_pressed
	ld	a, l
	or	a, a
	jr	Z,00106$
;src/entities/player.c:33: player->vx = (i8)(-kplayermovespeed);
	ld	hl,#_kplayermovespeed + 0
	ld	c, (hl)
	xor	a, a
	sub	a, c
	ld	c, a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
	jr	00107$
00106$:
;src/entities/player.c:34: } else if (input_is_right_pressed()) {
	call	_input_is_right_pressed
	ld	a, l
	or	a, a
	jr	Z,00107$
;src/entities/player.c:35: player->vx = kplayermovespeed;
	ld	hl,#_kplayermovespeed + 0
	ld	c, (hl)
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
00107$:
;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
	call	_input_is_jump_pressed
	ld	a, -2 (ix)
	add	a, #0x05
	ld	-6 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
	ld	a, -2 (ix)
	add	a, #0x01
	ld	-8 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
	ld	e,-2 (ix)
	ld	d,-1 (ix)
	inc	de
	inc	de
	inc	de
;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
	ld	a, l
	or	a, a
	jr	Z,00109$
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	a, (hl)
	pop	hl
	push	hl
	ld	c, (hl)
	ld	b, #0x00
	push	de
	push	af
	inc	sp
	push	bc
	call	_collision_is_on_ground
	pop	af
	inc	sp
	pop	de
	ld	a, l
	or	a, a
	jr	Z,00109$
;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
	ld	a,(#_kplayerjumpvelocity + 0)
	ld	(de), a
00109$:
;src/entities/player.c:42: player->vy = (i8)(player->vy + kplayergravity);
	ld	a, (de)
	ld	c, a
	ld	hl,#_kplayergravity + 0
	ld	b, (hl)
	ld	a, c
	add	a, b
	ld	(de), a
;src/entities/player.c:44: nextx = (i16)player->x + (i16)player->vx;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	c, (hl)
	ld	b, #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	l, (hl)
	ld	a, l
	rla
	sbc	a, a
	ld	h, a
	add	hl, bc
;src/entities/player.c:45: if (nextx < 0) {
	bit	7, h
	jr	Z,00112$
;src/entities/player.c:46: nextx = 0;
	ld	hl, #0x0000
00112$:
;src/entities/player.c:48: if (nextx > 76) {
	ld	a, #0x4c
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jp	PO, 00162$
	xor	a, #0x80
00162$:
	jp	P, 00114$
;src/entities/player.c:49: nextx = 76;
	ld	hl, #0x004c
00114$:
;src/entities/player.c:51: player->x = (u8)nextx;
	ld	c, l
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), c
;src/entities/player.c:53: nexty = (i16)player->y + (i16)player->vy;
	pop	hl
	push	hl
	ld	c, (hl)
	ld	b, #0x00
	ld	a, (de)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	add	hl,bc
	ld	c, l
	ld	b, h
;src/entities/player.c:54: nexty = collision_clamp_y_to_ground(nexty, player->h);
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	h, (hl)
	push	de
	push	hl
	inc	sp
	push	bc
	call	_collision_clamp_y_to_ground
	pop	af
	inc	sp
	pop	de
;src/entities/player.c:55: if (nexty < 0) {
	bit	7, h
	jr	Z,00116$
;src/entities/player.c:56: nexty = 0;
	ld	hl, #0x0000
00116$:
;src/entities/player.c:58: player->y = (u8)nexty;
	ld	c, l
	pop	hl
	push	hl
	ld	(hl), c
;src/entities/player.c:60: if (collision_is_on_ground((i16)player->y, player->h) && player->vy > 0) {
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	h, (hl)
	ld	b, #0x00
	push	de
	push	hl
	inc	sp
	push	bc
	call	_collision_is_on_ground
	pop	af
	inc	sp
	pop	de
	ld	a, l
	or	a, a
	jr	Z,00120$
	ld	a, (de)
	ld	c, a
	xor	a, a
	sub	a, c
	jp	PO, 00163$
	xor	a, #0x80
00163$:
	jp	P, 00120$
;src/entities/player.c:61: player->vy = 0;
	xor	a, a
	ld	(de), a
00120$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/player.c:65: void playerrender(const Player* player) {
;	---------------------------------
; Function playerrender
; ---------------------------------
_playerrender::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/player.c:68: if (!player) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/player.c:69: return;
	jr	Z,00103$
;src/entities/player.c:72: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
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
;src/entities/player.c:73: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
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
