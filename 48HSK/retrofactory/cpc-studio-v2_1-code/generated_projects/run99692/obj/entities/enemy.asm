;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module enemy
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSolidBox
	.globl _enemyinit
	.globl _enemyupdate
	.globl _enemyrender
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
;src/entities/enemy.c:4: void enemyinit(Enemy* enemy) {
;	---------------------------------
; Function enemyinit
; ---------------------------------
_enemyinit::
;src/entities/enemy.c:5: if (!enemy) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/enemy.c:6: return;
	ret	Z
;src/entities/enemy.c:9: enemy->x = 0;
	pop	de
	pop	bc
	push	bc
	push	de
	xor	a, a
	ld	(bc), a
;src/entities/enemy.c:10: enemy->y = 0;
	ld	e, c
	ld	d, b
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:11: enemy->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:12: enemy->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:13: enemy->w = 4;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x04
;src/entities/enemy.c:14: enemy->h = 16;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x10
;src/entities/enemy.c:15: enemy->active = 0;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x00
	ret
;src/entities/enemy.c:18: void enemyupdate(Enemy* enemy) {
;	---------------------------------
; Function enemyupdate
; ---------------------------------
_enemyupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/enemy.c:19: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00104$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/enemy.c:20: return;
	jr	Z,00104$
;src/entities/enemy.c:23: enemy->x = (u8)(enemy->x + enemy->vx);
	ld	a, (bc)
	ld	e, a
	ld	l, c
	ld	h, b
	inc	hl
	inc	hl
	ld	d, (hl)
	ld	a, e
	add	a, d
	ld	(bc), a
;src/entities/enemy.c:24: enemy->y = (u8)(enemy->y + enemy->vy);
	ld	e, c
	ld	d, b
	inc	de
	ld	a, (de)
	ld	l, c
	ld	h, b
	inc	hl
	inc	hl
	inc	hl
	ld	c, (hl)
	add	a, c
	ld	(de), a
00104$:
	pop	ix
	ret
;src/entities/enemy.c:27: void enemyrender(const Enemy* enemy) {
;	---------------------------------
; Function enemyrender
; ---------------------------------
_enemyrender::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/enemy.c:30: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00104$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/enemy.c:31: return;
	jr	Z,00104$
;src/entities/enemy.c:34: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
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
;src/entities/enemy.c:35: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
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
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
