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
	ret
;src/entities/enemy.c:21: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 move_right) {
;	---------------------------------
; Function enemyspawn
; ---------------------------------
_enemyspawn::
;src/entities/enemy.c:22: if (!enemy) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/enemy.c:23: return;
	ret	Z
;src/entities/enemy.c:26: enemy->x = x;
	pop	de
	pop	bc
	push	bc
	push	de
	ld	hl, #4+0
	add	hl, sp
	ld	a, (hl)
	ld	(bc), a
;src/entities/enemy.c:27: enemy->y = y;
	ld	e, c
	ld	d, b
	inc	de
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	ld	(de), a
;src/entities/enemy.c:28: enemy->vx = move_right ? 1 : -1;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	ld	hl, #6+0
	add	hl, sp
	ld	a, (hl)
	or	a, a
	jr	Z,00105$
	ld	a, #0x01
	jr	00106$
00105$:
	ld	a, #0xff
00106$:
	ld	(de), a
;src/entities/enemy.c:29: enemy->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:30: enemy->active = 1;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x01
;src/entities/enemy.c:31: enemy->health = 1;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x01
	ret
;src/entities/enemy.c:34: void enemyupdate(Enemy* enemy) {
;	---------------------------------
; Function enemyupdate
; ---------------------------------
_enemyupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-6
	add	hl, sp
	ld	sp, hl
;src/entities/enemy.c:38: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jp	Z,00113$
	ld	a, 4 (ix)
	ld	-2 (ix), a
	ld	a, 5 (ix)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
;src/entities/enemy.c:39: return;
	jp	Z,00113$
;src/entities/enemy.c:42: nextx = (i16)enemy->x + (i16)enemy->vx;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	c,-2 (ix)
	ld	b,-1 (ix)
	inc	bc
	inc	bc
	ld	a, (bc)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	add	hl,de
	ex	de,hl
;src/entities/enemy.c:43: if (nextx < 2) {
	ld	a, e
	sub	a, #0x02
	ld	a, d
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	NC,00105$
;src/entities/enemy.c:44: nextx = 2;
	ld	de, #0x0002
;src/entities/enemy.c:45: enemy->vx = 1;
	ld	a, #0x01
	ld	(bc), a
00105$:
;src/entities/enemy.c:47: if (nextx > 74) {
	ld	a, #0x4a
	cp	a, e
	ld	a, #0x00
	sbc	a, d
	jp	PO, 00139$
	xor	a, #0x80
00139$:
	jp	P, 00107$
;src/entities/enemy.c:48: nextx = 74;
	ld	de, #0x004a
;src/entities/enemy.c:49: enemy->vx = -1;
	ld	a, #0xff
	ld	(bc), a
00107$:
;src/entities/enemy.c:51: enemy->x = (u8)nextx;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), e
;src/entities/enemy.c:53: enemy->vy = (i8)(enemy->vy + 1);
	ld	e,-2 (ix)
	ld	d,-1 (ix)
	inc	de
	inc	de
	inc	de
	ld	a, (de)
	ld	c, a
	inc	c
	ld	a, c
	ld	(de), a
;src/entities/enemy.c:54: if (enemy->vy > 3) enemy->vy = 3;
	ld	a, #0x03
	sub	a, c
	jp	PO, 00140$
	xor	a, #0x80
00140$:
	jp	P, 00109$
	ld	a, #0x03
	ld	(de), a
00109$:
;src/entities/enemy.c:55: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	a, -2 (ix)
	add	a, #0x01
	ld	-4 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-3 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
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
;src/entities/enemy.c:56: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
	ld	a, -2 (ix)
	add	a, #0x05
	ld	-6 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
	pop	hl
	push	hl
	ld	a, (hl)
	ld	l,-2 (ix)
	ld	h,-1 (ix)
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
	pop	de
;src/entities/enemy.c:57: enemy->y = (u8)nexty;
	ld	c, l
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
;src/entities/enemy.c:58: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
	pop	hl
	push	hl
	ld	a, (hl)
	ld	b, #0x00
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	l, (hl)
	ld	-6 (ix), l
	ld	-5 (ix), #0x00
	push	de
	push	af
	inc	sp
	push	bc
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	pop	de
	ld	a, l
	or	a, a
	jr	Z,00113$
	ld	a, (de)
	ld	c, a
	xor	a, a
	sub	a, c
	jp	PO, 00141$
	xor	a, #0x80
00141$:
	jp	P, 00113$
;src/entities/enemy.c:59: enemy->vy = 0;
	xor	a, a
	ld	(de), a
00113$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:63: void enemyrender(const Enemy* enemy) {
;	---------------------------------
; Function enemyrender
; ---------------------------------
_enemyrender::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/enemy.c:66: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00104$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/enemy.c:67: return;
	jr	Z,00104$
;src/entities/enemy.c:70: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
	ld	l, c
	ld	h, b
	inc	hl
	ld	d, (hl)
	ld	a, (bc)
	push	bc
	ld	e, a
	push	de
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ex	de,hl
	pop	bc
;src/entities/enemy.c:71: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
	push	bc
	pop	iy
	ld	a, 5 (iy)
	ld	l, c
	ld	h, b
	ld	bc, #0x0004
	add	hl, bc
	ld	b, (hl)
	push	af
	inc	sp
	push	bc
	inc	sp
	ld	a, #0x5c
	push	af
	inc	sp
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00104$:
	pop	ix
	ret
;src/entities/enemy.c:74: u8 enemydamage(Enemy* enemy, u8 damage) {
;	---------------------------------
; Function enemydamage
; ---------------------------------
_enemydamage::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/enemy.c:75: if (!enemy || !enemy->active) {
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
;src/entities/enemy.c:76: return 0;
	ld	l, #0x00
	jr	00106$
00102$:
;src/entities/enemy.c:79: if (damage >= enemy->health) {
	ld	hl, #0x0007
	add	hl, bc
	ld	c, (hl)
	ld	a, 6 (ix)
	sub	a, c
	jr	C,00105$
;src/entities/enemy.c:80: enemy->health = 0;
	ld	(hl), #0x00
;src/entities/enemy.c:81: enemy->active = 0;
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:82: return 1;
	ld	l, #0x01
	jr	00106$
00105$:
;src/entities/enemy.c:85: enemy->health = (u8)(enemy->health - damage);
	ld	a, c
	sub	a, 6 (ix)
	ld	(hl), a
;src/entities/enemy.c:86: return 0;
	ld	l, #0x00
00106$:
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
