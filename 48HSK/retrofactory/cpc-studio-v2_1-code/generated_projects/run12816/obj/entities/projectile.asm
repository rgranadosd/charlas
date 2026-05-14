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
	.globl _projectilefire
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
;src/entities/projectile.c:16: projectile->damage = 1;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x01
;src/entities/projectile.c:17: projectile->lifetime = 0;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x00
;src/entities/projectile.c:18: projectile->weapon = 0;
	ld	hl, #0x0009
	add	hl, bc
	ld	(hl), #0x00
	ret
;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
;	---------------------------------
; Function projectilefire
; ---------------------------------
_projectilefire::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
;src/entities/projectile.c:22: if (!projectile) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/projectile.c:23: return;
	jr	Z,00106$
;src/entities/projectile.c:26: projectile->x = x;
	ld	e,4 (ix)
	ld	d,5 (ix)
	ld	a, 6 (ix)
	ld	(de), a
;src/entities/projectile.c:27: projectile->y = y;
	ld	c, e
	ld	b, d
	inc	bc
	ld	a, 7 (ix)
	ld	(bc), a
;src/entities/projectile.c:28: projectile->vx = dir;
	ld	c, e
	ld	b, d
	inc	bc
	inc	bc
	ld	a, 8 (ix)
	ld	(bc), a
;src/entities/projectile.c:29: projectile->vy = 0;
	ld	c, e
	ld	b, d
	inc	bc
	inc	bc
	inc	bc
	xor	a, a
	ld	(bc), a
;src/entities/projectile.c:30: projectile->weapon = weapon;
	ld	hl, #0x0009
	add	hl, de
	ld	a, 9 (ix)
	ld	(hl), a
;src/entities/projectile.c:31: projectile->active = 1;
	ld	hl, #0x0006
	add	hl, de
	ld	(hl), #0x01
;src/entities/projectile.c:34: projectile->w = 3;
	ld	hl, #0x0004
	add	hl, de
;src/entities/projectile.c:35: projectile->h = 2;
	ld	a, e
	add	a, #0x05
	ld	c, a
	ld	a, d
	adc	a, #0x00
	ld	b, a
;src/entities/projectile.c:36: projectile->damage = 1;
	ld	a, e
	add	a, #0x07
	ld	-2 (ix), a
	ld	a, d
	adc	a, #0x00
	ld	-1 (ix), a
;src/entities/projectile.c:37: projectile->lifetime = 45;
	ld	a, e
	add	a, #0x08
	ld	e, a
	ld	a, d
	adc	a, #0x00
	ld	d, a
;src/entities/projectile.c:33: if (weapon == 0) {
	ld	a, 9 (ix)
	or	a, a
	jr	NZ,00104$
;src/entities/projectile.c:34: projectile->w = 3;
	ld	(hl), #0x03
;src/entities/projectile.c:35: projectile->h = 2;
	ld	a, #0x02
	ld	(bc), a
;src/entities/projectile.c:36: projectile->damage = 1;
	pop	hl
	push	hl
	ld	(hl), #0x01
;src/entities/projectile.c:37: projectile->lifetime = 45;
	ld	a, #0x2d
	ld	(de), a
	jr	00106$
00104$:
;src/entities/projectile.c:39: projectile->w = 2;
	ld	(hl), #0x02
;src/entities/projectile.c:40: projectile->h = 3;
	ld	a, #0x03
	ld	(bc), a
;src/entities/projectile.c:41: projectile->damage = 2;
	pop	hl
	push	hl
	ld	(hl), #0x02
;src/entities/projectile.c:42: projectile->lifetime = 28;
	ld	a, #0x1c
	ld	(de), a
00106$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/projectile.c:46: void projectileupdate(Projectile* projectile) {
;	---------------------------------
; Function projectileupdate
; ---------------------------------
_projectileupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/entities/projectile.c:47: if (!projectile || !projectile->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00109$
	ld	e,4 (ix)
	ld	d,5 (ix)
	ld	iy, #0x0006
	add	iy, de
	ld	a, 0 (iy)
	or	a, a
;src/entities/projectile.c:48: return;
	jr	Z,00109$
;src/entities/projectile.c:51: projectile->x = (u8)(projectile->x + projectile->vx);
	ld	a, (de)
	ld	c, a
	ld	l, e
	ld	h, d
	inc	hl
	inc	hl
	ld	l, (hl)
	add	hl, bc
	ld	a, l
	ld	(de), a
;src/entities/projectile.c:52: projectile->y = (u8)(projectile->y + projectile->vy);
	ld	c, e
	ld	b, d
	inc	bc
	ld	a, (bc)
	ld	-1 (ix), a
	ld	l, e
	ld	h, d
	inc	hl
	inc	hl
	inc	hl
	ld	l, (hl)
	ld	a, -1 (ix)
	add	a, l
	ld	(bc), a
;src/entities/projectile.c:54: if (projectile->lifetime) {
	ld	hl, #0x0008
	add	hl,de
	ld	c, l
	ld	b, h
	ld	a, (bc)
	or	a, a
	jr	Z,00105$
;src/entities/projectile.c:55: projectile->lifetime--;
	add	a, #0xff
	ld	(bc), a
00105$:
;src/entities/projectile.c:58: if (projectile->x > 78 || projectile->lifetime == 0) {
	ld	a, (de)
	ld	e, a
	ld	a, #0x4e
	sub	a, e
	jr	C,00106$
	ld	a, (bc)
	or	a, a
	jr	NZ,00109$
00106$:
;src/entities/projectile.c:59: projectile->active = 0;
	ld	0 (iy), #0x00
00109$:
	inc	sp
	pop	ix
	ret
;src/entities/projectile.c:63: void projectilerender(const Projectile* projectile) {
;	---------------------------------
; Function projectilerender
; ---------------------------------
_projectilerender::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00104$
	ld	e,4 (ix)
	ld	d,5 (ix)
	push	de
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/projectile.c:67: return;
	jr	Z,00104$
;src/entities/projectile.c:70: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
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
;src/entities/projectile.c:71: cpct_drawSolidBox(pvmem, projectile->weapon ? 0x6B : 0x0F, projectile->w, projectile->h);
	push	de
	pop	iy
	ld	a, 5 (iy)
	ld	-1 (ix), a
	push	de
	pop	iy
	ld	a, 4 (iy)
	ld	-2 (ix), a
	ex	de,hl
	ld	de, #0x0009
	add	hl, de
	ld	a, (hl)
	or	a, a
	jr	Z,00106$
	ld	d, #0x6b
	jr	00107$
00106$:
	ld	d, #0x0f
00107$:
	ld	h, -1 (ix)
	ld	l, -2 (ix)
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00104$:
	ld	sp, ix
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
