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
	.globl _cpct_drawSprite
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
;src/entities/projectile.c:17: void projectileinit(Projectile* projectile) {
;	---------------------------------
; Function projectileinit
; ---------------------------------
_projectileinit::
;src/entities/projectile.c:18: if (!projectile) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/projectile.c:19: return;
	ret	Z
;src/entities/projectile.c:22: projectile->x = 0;
	pop	de
	pop	bc
	push	bc
	push	de
	xor	a, a
	ld	(bc), a
;src/entities/projectile.c:23: projectile->y = 0;
	ld	e, c
	ld	d, b
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:24: projectile->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:25: projectile->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:26: projectile->w = 2;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x02
;src/entities/projectile.c:27: projectile->h = 2;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x02
;src/entities/projectile.c:28: projectile->active = 0;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x00
;src/entities/projectile.c:29: projectile->damage = 1;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x01
;src/entities/projectile.c:30: projectile->lifetime = 0;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x00
;src/entities/projectile.c:31: projectile->weapon = 0;
	ld	hl, #0x0009
	add	hl, bc
	ld	(hl), #0x00
	ret
_projectile_basic_sprite:
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
_projectile_up_sprite:
	.db #0xcf	; 207
	.db #0xcf	; 207
	.db #0xcf	; 207
	.db #0xcf	; 207
	.db #0xcf	; 207
	.db #0xcf	; 207
_projectile_special_sprite:
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
	.db #0xf0	; 240
;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
;	---------------------------------
; Function projectilefire
; ---------------------------------
_projectilefire::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	push	af
;src/entities/projectile.c:35: if (!projectile) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/projectile.c:36: return;
	jp	Z,00109$
;src/entities/projectile.c:39: projectile->x = x;
	ld	c,4 (ix)
	ld	b,5 (ix)
	ld	a, 6 (ix)
	ld	(bc), a
;src/entities/projectile.c:40: projectile->y = y;
	ld	e, c
	ld	d, b
	inc	de
	ld	a, 7 (ix)
	ld	(de), a
;src/entities/projectile.c:41: projectile->vx = dir;
	ld	hl, #0x0002
	add	hl,bc
	ld	-2 (ix), l
	ld	-1 (ix), h
	ld	a, 8 (ix)
	ld	(hl), a
;src/entities/projectile.c:42: projectile->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/projectile.c:43: projectile->weapon = weapon;
	ld	hl, #0x0009
	add	hl, bc
	ld	a, 9 (ix)
	ld	(hl), a
;src/entities/projectile.c:44: projectile->active = 1;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x01
;src/entities/projectile.c:47: projectile->w = 3;
	ld	hl, #0x0004
	add	hl, bc
;src/entities/projectile.c:48: projectile->h = 2;
	ld	a, c
	add	a, #0x05
	ld	e, a
	ld	a, b
	adc	a, #0x00
	ld	d, a
;src/entities/projectile.c:49: projectile->damage = 1;
	ld	a, c
	add	a, #0x07
	ld	-4 (ix), a
	ld	a, b
	adc	a, #0x00
	ld	-3 (ix), a
;src/entities/projectile.c:50: projectile->lifetime = 45;
	ld	a, c
	add	a, #0x08
	ld	c, a
	ld	a, b
	adc	a, #0x00
	ld	b, a
;src/entities/projectile.c:46: if (weapon == 0) {
	ld	a, 9 (ix)
	or	a, a
	jr	NZ,00107$
;src/entities/projectile.c:47: projectile->w = 3;
	ld	(hl), #0x03
;src/entities/projectile.c:48: projectile->h = 2;
	ld	a, #0x02
	ld	(de), a
;src/entities/projectile.c:49: projectile->damage = 1;
	pop	hl
	push	hl
	ld	(hl), #0x01
;src/entities/projectile.c:50: projectile->lifetime = 45;
	ld	a, #0x2d
	ld	(bc), a
	jr	00109$
00107$:
;src/entities/projectile.c:51: } else if (weapon == 1) {
	ld	a, 9 (ix)
	dec	a
	jr	NZ,00104$
;src/entities/projectile.c:52: projectile->w = 2;
	ld	(hl), #0x02
;src/entities/projectile.c:53: projectile->h = 3;
	ld	a, #0x03
	ld	(de), a
;src/entities/projectile.c:54: projectile->damage = 2;
	pop	hl
	push	hl
	ld	(hl), #0x02
;src/entities/projectile.c:55: projectile->lifetime = 28;
	ld	a, #0x1c
	ld	(bc), a
	jr	00109$
00104$:
;src/entities/projectile.c:57: projectile->w = 4;
	ld	(hl), #0x04
;src/entities/projectile.c:58: projectile->h = 3;
	ld	a, #0x03
	ld	(de), a
;src/entities/projectile.c:59: projectile->damage = 3;
	pop	hl
	push	hl
	ld	(hl), #0x03
;src/entities/projectile.c:60: projectile->lifetime = 56;
	ld	a, #0x38
	ld	(bc), a
;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
	pop	de
	pop	bc
	push	bc
	push	de
	xor	a, a
	sub	a, 8 (ix)
	jp	PO, 00131$
	xor	a, #0x80
00131$:
	jp	P, 00111$
	ld	a, #0x04
	jr	00112$
00111$:
	ld	a, #0xfc
00112$:
	ld	(bc), a
00109$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
;	---------------------------------
; Function projectileupdate
; ---------------------------------
_projectileupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00109$
	ld	e,4 (ix)
	ld	d,5 (ix)
	ld	iy, #0x0006
	add	iy, de
	ld	a, 0 (iy)
	or	a, a
;src/entities/projectile.c:67: return;
	jr	Z,00109$
;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
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
;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
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
;src/entities/projectile.c:73: if (projectile->lifetime) {
	ld	hl, #0x0008
	add	hl,de
	ld	c, l
	ld	b, h
	ld	a, (bc)
	or	a, a
	jr	Z,00105$
;src/entities/projectile.c:74: projectile->lifetime--;
	add	a, #0xff
	ld	(bc), a
00105$:
;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
	ld	a, (de)
	ld	e, a
	ld	a, #0x4e
	sub	a, e
	jr	C,00106$
	ld	a, (bc)
	or	a, a
	jr	NZ,00109$
00106$:
;src/entities/projectile.c:78: projectile->active = 0;
	ld	0 (iy), #0x00
00109$:
	inc	sp
	pop	ix
	ret
;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
;	---------------------------------
; Function projectilerender
; ---------------------------------
_projectilerender::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	dec	sp
;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00110$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/projectile.c:87: return;
	jr	Z,00110$
;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
	push	bc
	pop	iy
	ld	a, 9 (iy)
	or	a, a
	jr	NZ,00108$
	ld	-2 (ix), #<(_projectile_basic_sprite)
	ld	-1 (ix), #>(_projectile_basic_sprite)
	jr	00109$
00108$:
;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
	dec	a
	jr	NZ,00105$
	ld	-2 (ix), #<(_projectile_up_sprite)
	ld	-1 (ix), #>(_projectile_up_sprite)
	jr	00109$
00105$:
;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
	ld	-2 (ix), #<(_projectile_special_sprite)
	ld	-1 (ix), #>(_projectile_special_sprite)
00109$:
;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
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
;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
	push	bc
	pop	iy
	ld	a, 5 (iy)
	ld	-3 (ix), a
	ld	l, c
	ld	h, b
	ld	bc, #0x0004
	add	hl, bc
	ld	c, (hl)
	push	de
	pop	iy
	ld	e,-2 (ix)
	ld	d,-1 (ix)
	ld	b, -3 (ix)
	push	bc
	push	iy
	push	de
	call	_cpct_drawSprite
00110$:
	ld	sp, ix
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
