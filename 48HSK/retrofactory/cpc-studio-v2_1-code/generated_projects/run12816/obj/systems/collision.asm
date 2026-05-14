;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module collision
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _tilemap_is_trap
	.globl _tilemap_platform_y_at
	.globl _tilemap_ground_y
	.globl _collision_init
	.globl _collision_is_on_ground
	.globl _collision_is_on_ground_at
	.globl _collision_clamp_y_to_ground
	.globl _collision_clamp_y_at
	.globl _collision_is_on_trap
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
_ggroundy:
	.ds 2
_gplatformy:
	.ds 2
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
;src/systems/collision.c:7: void collision_init(void) {
;	---------------------------------
; Function collision_init
; ---------------------------------
_collision_init::
;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
	call	_tilemap_ground_y
	ld	iy, #_ggroundy
	ld	0 (iy), l
	ld	1 (iy), #0x00
;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
	ld	hl, #0x0020
	push	hl
	call	_tilemap_platform_y_at
	pop	af
	ld	iy, #_gplatformy
	ld	0 (iy), l
	ld	1 (iy), #0x00
	ret
;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
;	---------------------------------
; Function collision_is_on_ground
; ---------------------------------
_collision_is_on_ground::
;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
	ld	hl, #4+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #3
	add	hl, sp
	ld	c, (hl)
	inc	hl
	ld	b, (hl)
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	ret
;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
;	---------------------------------
; Function collision_is_on_ground_at
; ---------------------------------
_collision_is_on_ground_at::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
	call	_tilemap_ground_y
	ld	c, l
	ld	b, #0x00
;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
	push	bc
	ld	l,4 (ix)
	ld	h,5 (ix)
	push	hl
	call	_tilemap_platform_y_at
	pop	af
	pop	bc
	ld	iy, #_gplatformy
	ld	0 (iy), l
	ld	1 (iy), #0x00
;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
	ld	e, 8 (ix)
	ld	d, #0x00
	ld	a, 6 (ix)
	add	a, e
	ld	e, a
	ld	a, 7 (ix)
	adc	a, d
	ld	d, a
	ld	a, 0 (iy)
	inc	a
	or	a, 1 (iy)
	jr	Z,00102$
	ld	hl, (_gplatformy)
	inc	hl
	inc	hl
	ld	a, l
	sub	a, e
	ld	a, h
	sbc	a, d
	jp	PO, 00115$
	xor	a, #0x80
00115$:
	jp	M, 00102$
;src/systems/collision.c:23: support = gplatformy;
	ld	bc, (_gplatformy)
00102$:
;src/systems/collision.c:26: feet = y + (i16)h;
;src/systems/collision.c:27: return (u8)(feet >= support);
	ld	a, e
	sub	a, c
	ld	a, d
	sbc	a, b
	jp	PO, 00116$
	xor	a, #0x80
00116$:
	rlca
	and	a,#0x01
	xor	a, #0x01
	ld	l, a
	pop	ix
	ret
;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
;	---------------------------------
; Function collision_clamp_y_to_ground
; ---------------------------------
_collision_clamp_y_to_ground::
;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
	ld	hl, #4+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #3
	add	hl, sp
	ld	c, (hl)
	inc	hl
	ld	b, (hl)
	push	bc
	ld	hl, #0x0000
	push	hl
	call	_collision_clamp_y_at
	pop	af
	pop	af
	inc	sp
	ret
;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
;	---------------------------------
; Function collision_clamp_y_at
; ---------------------------------
_collision_clamp_y_at::
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
	call	_tilemap_ground_y
	ld	iy, #_ggroundy
	ld	0 (iy), l
	ld	1 (iy), #0x00
;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
	ld	c, 8 (ix)
	ld	b, #0x00
	ld	a, 0 (iy)
	sub	a, c
	ld	e, a
	ld	a, 1 (iy)
	sbc	a, b
	ld	d, a
;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
	push	bc
	push	de
	ld	l,4 (ix)
	ld	h,5 (ix)
	push	hl
	call	_tilemap_platform_y_at
	pop	af
	pop	de
	pop	bc
	ld	iy, #_gplatformy
	ld	0 (iy), l
	ld	1 (iy), #0x00
;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
	ld	a, e
	sub	a, 6 (ix)
	ld	a, d
	sbc	a, 7 (ix)
	jp	PO, 00126$
	xor	a, #0x80
00126$:
	rlca
	and	a,#0x01
	ld	-1 (ix), a
;src/systems/collision.c:41: if (gplatformy != 255) {
	ld	iy, #_gplatformy
	ld	a, 0 (iy)
	inc	a
	or	a, 1 (iy)
	jr	Z,00105$
;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
	ld	a, 0 (iy)
	sub	a, c
	ld	c, a
	ld	a, 1 (iy)
	sbc	a, b
	ld	b, a
;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
	ld	a, c
	sub	a, 6 (ix)
	ld	a, b
	sbc	a, 7 (ix)
	jp	PO, 00128$
	xor	a, #0x80
00128$:
	jp	P, 00105$
	bit	0, -1 (ix)
	jr	NZ,00105$
;src/systems/collision.c:44: return platformmaxy;
	ld	l, c
	ld	h, b
	jr	00108$
00105$:
;src/systems/collision.c:48: if (y > maxy) {
	bit	0, -1 (ix)
	jr	Z,00107$
;src/systems/collision.c:49: return maxy;
	ex	de,hl
	jr	00108$
00107$:
;src/systems/collision.c:51: return y;
	ld	l,6 (ix)
	ld	h,7 (ix)
00108$:
	inc	sp
	pop	ix
	ret
;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
;	---------------------------------
; Function collision_is_on_trap
; ---------------------------------
_collision_is_on_trap::
;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
	ld	hl, #7+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #7+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #6
	add	hl, sp
	ld	c, (hl)
	inc	hl
	ld	b, (hl)
	push	bc
	ld	hl, #6
	add	hl, sp
	ld	c, (hl)
	inc	hl
	ld	b, (hl)
	push	bc
	call	_tilemap_is_trap
	pop	af
	pop	af
	pop	af
	ret
	.area _CODE
	.area _INITIALIZER
__xinit__ggroundy:
	.dw #0x00a0
__xinit__gplatformy:
	.dw #0x00ff
	.area _CABS (ABS)
