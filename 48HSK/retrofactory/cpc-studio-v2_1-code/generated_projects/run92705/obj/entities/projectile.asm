;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module projectile
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSolidBox
	.globl _projectileinit
	.globl _projectileupdate
	.globl _projectilerender
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
;src/entities/projectile.c:4: void projectileinit(Projectile* projectile) {
;	---------------------------------
; Function projectileinit
; ---------------------------------
_projectileinit::
;src/entities/projectile.c:5: if (!projectile) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/projectile.c:6: return;
	ret	Z
;src/entities/projectile.c:9: projectile->x = 0;
	pop	de
	pop	bc
	push	bc
	push	de
	xor	a, a
	ld	(bc), a
;src/entities/projectile.c:10: projectile->y = 0;
	ld	e, c
	ld	d, b
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:11: projectile->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:12: projectile->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:13: projectile->w = 2;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x02
;src/entities/projectile.c:14: projectile->h = 2;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x02
;src/entities/projectile.c:15: projectile->active = 0;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x00
	ret
;src/entities/projectile.c:18: void projectileupdate(Projectile* projectile) {
;	---------------------------------
; Function projectileupdate
; ---------------------------------
_projectileupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/projectile.c:19: if (!projectile || !projectile->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00104$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/projectile.c:20: return;
	jr	Z,00104$
;src/entities/projectile.c:23: projectile->x = (u8)(projectile->x + projectile->vx);
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
;src/entities/projectile.c:24: projectile->y = (u8)(projectile->y + projectile->vy);
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
;src/entities/projectile.c:27: void projectilerender(const Projectile* projectile) {
;	---------------------------------
; Function projectilerender
; ---------------------------------
_projectilerender::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/projectile.c:30: if (!projectile || !projectile->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00104$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/projectile.c:31: return;
	jr	Z,00104$
;src/entities/projectile.c:34: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
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
;src/entities/projectile.c:35: cpct_drawSolidBox(pvmem, 0x0F, projectile->w, projectile->h);
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
	ld	a, #0x0f
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
