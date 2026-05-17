;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module enemy
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _collision_clamp_y_at
	.globl _collision_is_on_ground_at
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSolidBox
	.globl _cpct_px2byteM0
	.globl _enemyinit
	.globl _enemyspawn
	.globl _enemyupdate
	.globl _enemyrender
	.globl _enemydamage
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
;src/entities/enemy.c:5: void enemyinit(Enemy* enemy) {
;	---------------------------------
; Function enemyinit
; ---------------------------------
_enemyinit::
;src/entities/enemy.c:6: if (!enemy) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/enemy.c:7: return;
	ret	Z
;src/entities/enemy.c:10: enemy->x = 0;
	pop	de
	pop	bc
	push	bc
	push	de
	xor	a, a
	ld	(bc), a
;src/entities/enemy.c:11: enemy->y = 0;
	ld	e, c
	ld	d, b
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:12: enemy->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:13: enemy->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:14: enemy->w = 4;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x04
;src/entities/enemy.c:15: enemy->h = 16;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x10
;src/entities/enemy.c:16: enemy->active = 0;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x00
;src/entities/enemy.c:17: enemy->health = 1;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x01
;src/entities/enemy.c:18: enemy->reward = 100;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x64
;src/entities/enemy.c:19: enemy->kind = 0;
	ld	hl, #0x0009
	add	hl, bc
	ld	(hl), #0x00
	ret
;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
;	---------------------------------
; Function enemyspawn
; ---------------------------------
_enemyspawn::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-15
	add	hl, sp
	ld	sp, hl
;src/entities/enemy.c:23: if (!enemy) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/enemy.c:24: return;
	jp	Z,00112$
;src/entities/enemy.c:27: enemy->x = x;
	ld	a, 4 (ix)
	ld	-4 (ix), a
	ld	a, 5 (ix)
	ld	-3 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	a, 6 (ix)
	ld	(hl), a
;src/entities/enemy.c:28: enemy->y = y;
	ld	c,-4 (ix)
	ld	b,-3 (ix)
	inc	bc
	ld	a, 7 (ix)
	ld	(bc), a
;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
	ld	a, -4 (ix)
	add	a, #0x02
	ld	-2 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-1 (ix), a
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00114$
	ld	c, #0x01
	jr	00115$
00114$:
	ld	c, #0xff
00115$:
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), c
;src/entities/enemy.c:30: enemy->vy = 0;
	ld	a, -4 (ix)
	add	a, #0x03
	ld	-6 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x00
;src/entities/enemy.c:31: enemy->active = 1;
	ld	a, -4 (ix)
	add	a, #0x06
	ld	-15 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-14 (ix), a
	pop	hl
	push	hl
	ld	(hl), #0x01
;src/entities/enemy.c:32: enemy->kind = kind;
	ld	a, -4 (ix)
	add	a, #0x09
	ld	-15 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-14 (ix), a
	pop	hl
	push	hl
	ld	a, 8 (ix)
	ld	(hl), a
;src/entities/enemy.c:35: enemy->w = 5;
	ld	a, -4 (ix)
	add	a, #0x04
	ld	-15 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-14 (ix), a
;src/entities/enemy.c:36: enemy->h = 14;
	ld	a, -4 (ix)
	add	a, #0x05
	ld	-8 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
;src/entities/enemy.c:37: enemy->health = 2;
	ld	a, -4 (ix)
	add	a, #0x07
	ld	-13 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-12 (ix), a
;src/entities/enemy.c:38: enemy->reward = 180;
	ld	a, -4 (ix)
	add	a, #0x08
	ld	-4 (ix), a
	ld	a, -3 (ix)
	adc	a, #0x00
	ld	-3 (ix), a
;src/entities/enemy.c:34: if (kind == 1) {
	ld	a, 8 (ix)
	dec	a
	jr	NZ,00110$
;src/entities/enemy.c:35: enemy->w = 5;
	pop	hl
	push	hl
	ld	(hl), #0x05
;src/entities/enemy.c:36: enemy->h = 14;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x0e
;src/entities/enemy.c:37: enemy->health = 2;
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), #0x02
;src/entities/enemy.c:38: enemy->reward = 180;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0xb4
;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
	ld	a, -2 (ix)
	ld	-10 (ix), a
	ld	a, -1 (ix)
	ld	-9 (ix), a
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00116$
	ld	-11 (ix), #0x02
	jr	00117$
00116$:
	ld	-11 (ix), #0xfe
00117$:
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	a, -11 (ix)
	ld	(hl), a
	jp	00112$
00110$:
;src/entities/enemy.c:40: } else if (kind == 2) {
	ld	a, 8 (ix)
	sub	a, #0x02
	jr	NZ,00107$
;src/entities/enemy.c:41: enemy->w = 6;
	pop	hl
	push	hl
	ld	(hl), #0x06
;src/entities/enemy.c:42: enemy->h = 10;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x0a
;src/entities/enemy.c:43: enemy->health = 1;
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), #0x01
;src/entities/enemy.c:44: enemy->reward = 150;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x96
;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
	ld	c,-6 (ix)
	ld	b,-5 (ix)
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00118$
	ld	a, #0x01
	jr	00119$
00118$:
	ld	a, #0xff
00119$:
	ld	(bc), a
;src/entities/enemy.c:46: enemy->vx = 1;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x01
	jr	00112$
00107$:
;src/entities/enemy.c:47: } else if (kind == 3) {
	ld	a, 8 (ix)
	sub	a, #0x03
	jr	NZ,00104$
;src/entities/enemy.c:48: enemy->w = 10;
	pop	hl
	push	hl
	ld	(hl), #0x0a
;src/entities/enemy.c:49: enemy->h = 18;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x12
;src/entities/enemy.c:50: enemy->health = 8;
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), #0x08
;src/entities/enemy.c:51: enemy->reward = 800;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x20
;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
	ld	c,-2 (ix)
	ld	b,-1 (ix)
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00120$
	ld	a, #0x01
	jr	00121$
00120$:
	ld	a, #0xff
00121$:
	ld	(bc), a
	jr	00112$
00104$:
;src/entities/enemy.c:54: enemy->w = 4;
	pop	hl
	push	hl
	ld	(hl), #0x04
;src/entities/enemy.c:55: enemy->h = 16;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x10
;src/entities/enemy.c:56: enemy->health = 1;
	ld	l,-13 (ix)
	ld	h,-12 (ix)
	ld	(hl), #0x01
;src/entities/enemy.c:57: enemy->reward = 100;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x64
00112$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
;	---------------------------------
; Function enemyupdate
; ---------------------------------
_enemyupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-10
	add	hl, sp
	ld	sp, hl
;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jp	Z,00121$
	ld	a, 4 (ix)
	ld	-5 (ix), a
	ld	a, 5 (ix)
	ld	-4 (ix), a
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
;src/entities/enemy.c:66: return;
	jp	Z,00121$
;src/entities/enemy.c:69: if (enemy->kind == 2) {
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	de, #0x0009
	add	hl, de
	ld	a, (hl)
	ld	-1 (ix), a
;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	c, (hl)
	ld	a, -5 (ix)
	add	a, #0x02
	ld	-3 (ix), a
	ld	a, -4 (ix)
	adc	a, #0x00
	ld	-2 (ix), a
;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	a, -5 (ix)
	add	a, #0x01
	ld	-7 (ix), a
	ld	a, -4 (ix)
	adc	a, #0x00
	ld	-6 (ix), a
	ld	e,-5 (ix)
	ld	d,-4 (ix)
	inc	de
	inc	de
	inc	de
;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
	ld	b, #0x00
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	a, (hl)
	ld	-8 (ix), a
	ld	l, a
	ld	a, -8 (ix)
	rla
	sbc	a, a
	ld	h, a
	add	hl,bc
	ld	c, l
	ld	b, h
;src/entities/enemy.c:69: if (enemy->kind == 2) {
	ld	a, -1 (ix)
	sub	a, #0x02
	jp	NZ,00111$
;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	ld	l, (hl)
	ld	-10 (ix), l
	ld	-9 (ix), #0x00
	ld	a, (de)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	ld	a, -10 (ix)
	add	a, l
	ld	-10 (ix), a
	ld	a, -9 (ix)
	adc	a, h
	ld	-9 (ix), a
;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
	ld	a, c
	sub	a, #0x08
	ld	a, b
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	C,00104$
	ld	a, #0x48
	cp	a, c
	ld	a, #0x00
	sbc	a, b
	jp	PO, 00161$
	xor	a, #0x80
00161$:
	jp	P, 00105$
00104$:
;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
	xor	a, a
	sub	a, -8 (ix)
	ld	c, a
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), c
;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	l, (hl)
	ld	h, #0x00
	ld	a, c
	rla
	sbc	a, a
	ld	b, a
	add	hl,bc
	ld	c, l
00105$:
;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
	ld	a, -10 (ix)
	sub	a, #0x38
	ld	a, -9 (ix)
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	C,00107$
	ld	a, #0x78
	cp	a, -10 (ix)
	ld	a, #0x00
	sbc	a, -9 (ix)
	jp	PO, 00162$
	xor	a, #0x80
00162$:
	jp	P, 00108$
00107$:
;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
	ld	a, (de)
	ld	l, a
	xor	a, a
	sub	a, l
	ld	-8 (ix), a
	ld	(de),a
;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	l, -8 (ix)
	ld	a, -8 (ix)
	rla
	sbc	a, a
	ld	h, a
	add	hl,de
	ex	(sp), hl
00108$:
;src/entities/enemy.c:82: enemy->x = (u8)nextx;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	(hl), c
;src/entities/enemy.c:83: enemy->y = (u8)nexty;
	ld	c, -10 (ix)
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	ld	(hl), c
;src/entities/enemy.c:84: return;
	jp	00121$
00111$:
;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
;src/entities/enemy.c:88: if (nextx < 2) {
	ld	a, c
	sub	a, #0x02
	ld	a, b
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	NC,00113$
;src/entities/enemy.c:89: nextx = 2;
	ld	bc, #0x0002
;src/entities/enemy.c:90: enemy->vx = 1;
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), #0x01
00113$:
;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	l, (hl)
	ld	h, #0x00
	ld	a, #0x50
	sub	a, l
	ld	l, a
	ld	a, #0x00
	sbc	a, h
	ld	h, a
;src/entities/enemy.c:94: if (nextx > maxx) {
	ld	a, l
	sub	a, c
	ld	a, h
	sbc	a, b
	jp	PO, 00163$
	xor	a, #0x80
00163$:
	jp	P, 00115$
;src/entities/enemy.c:95: nextx = maxx;
	ld	c, l
;src/entities/enemy.c:96: enemy->vx = -1;
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), #0xff
00115$:
;src/entities/enemy.c:99: enemy->x = (u8)nextx;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	(hl), c
;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
	ld	a, (de)
	ld	c, a
	inc	c
	ld	a, c
	ld	(de), a
;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
	ld	a, #0x03
	sub	a, c
	jp	PO, 00164$
	xor	a, #0x80
00164$:
	jp	P, 00117$
	ld	a, #0x03
	ld	(de), a
00117$:
;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	ld	c, (hl)
	ld	b, #0x00
	ld	a, (de)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	add	hl, bc
	push	hl
	pop	iy
;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
	ld	a, -5 (ix)
	add	a, #0x05
	ld	-10 (ix), a
	ld	a, -4 (ix)
	adc	a, #0x00
	ld	-9 (ix), a
	pop	hl
	push	hl
	ld	a, (hl)
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	c, (hl)
	ld	b, #0x00
	push	de
	push	af
	inc	sp
	push	iy
	push	bc
	call	_collision_clamp_y_at
	pop	af
	pop	af
	inc	sp
	ld	c, l
	pop	de
;src/entities/enemy.c:105: enemy->y = (u8)nexty;
	ld	l,-7 (ix)
	ld	h,-6 (ix)
	ld	(hl), c
;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
	pop	hl
	push	hl
	ld	a, (hl)
	ld	b, #0x00
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	l, (hl)
	ld	-10 (ix), l
	ld	-9 (ix), #0x00
	push	de
	push	af
	inc	sp
	push	bc
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	pop	de
	ld	a, l
	or	a, a
	jr	Z,00121$
	ld	a, (de)
	ld	c, a
	xor	a, a
	sub	a, c
	jp	PO, 00165$
	xor	a, #0x80
00165$:
	jp	P, 00121$
;src/entities/enemy.c:107: enemy->vy = 0;
	xor	a, a
	ld	(de), a
00121$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
;	---------------------------------
; Function enemyrender
; ---------------------------------
_enemyrender::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jp	Z,00113$
	ld	a, 4 (ix)
	ld	-2 (ix), a
	ld	a, 5 (ix)
	ld	-1 (ix), a
	pop	hl
	push	hl
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
;src/entities/enemy.c:116: return;
	jr	Z,00113$
;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
	pop	hl
	push	hl
	ld	de, #0x0009
	add	hl, de
	ld	a, (hl)
	cp	a, #0x03
	jr	NZ,00111$
	ld	hl, #0x0c0c
	push	hl
	call	_cpct_px2byteM0
	ld	c, l
	jr	00112$
00111$:
;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
	cp	a, #0x02
	jr	NZ,00108$
	ld	hl, #0x0a0a
	push	hl
	call	_cpct_px2byteM0
	ld	c, l
	jr	00112$
00108$:
;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
	dec	a
	jr	NZ,00105$
	ld	hl, #0x0e0e
	push	hl
	call	_cpct_px2byteM0
	ld	c, l
	jr	00112$
00105$:
;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
	ld	hl, #0x0404
	push	hl
	call	_cpct_px2byteM0
	ld	c, l
00112$:
;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
	pop	hl
	push	hl
	inc	hl
	ld	b, (hl)
	pop	hl
	push	hl
	ld	d, (hl)
	push	bc
	ld	c, d
	push	bc
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ex	de,hl
	pop	bc
;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
	pop	hl
	push	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	b, (hl)
	pop	hl
	push	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	push	bc
	inc	sp
	ld	b, a
	push	bc
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00113$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
;	---------------------------------
; Function enemydamage
; ---------------------------------
_enemydamage::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00101$
	ld	c,4 (ix)
	ld	b,5 (ix)
	ld	hl, #0x0006
	add	hl,bc
	ex	de,hl
	ld	a, (de)
	or	a, a
	jr	NZ,00102$
00101$:
;src/entities/enemy.c:130: return 0;
	ld	l, #0x00
	jr	00106$
00102$:
;src/entities/enemy.c:133: if (damage >= enemy->health) {
	ld	hl, #0x0007
	add	hl, bc
	ld	c, (hl)
	ld	a, 6 (ix)
	sub	a, c
	jr	C,00105$
;src/entities/enemy.c:134: enemy->health = 0;
	ld	(hl), #0x00
;src/entities/enemy.c:135: enemy->active = 0;
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:136: return 1;
	ld	l, #0x01
	jr	00106$
00105$:
;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
	ld	a, c
	sub	a, 6 (ix)
	ld	(hl), a
;src/entities/enemy.c:140: return 0;
	ld	l, #0x00
00106$:
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
