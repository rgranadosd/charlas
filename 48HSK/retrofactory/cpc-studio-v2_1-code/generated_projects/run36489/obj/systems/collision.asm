;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module collision
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _tilemap_ground_y
	.globl _collision_init
	.globl _collision_is_on_ground
	.globl _collision_clamp_y_to_ground
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
;src/systems/collision.c:6: void collision_init(void) {
;	---------------------------------
; Function collision_init
; ---------------------------------
_collision_init::
;src/systems/collision.c:7: ggroundy = (i16)tilemap_ground_y();
	call	_tilemap_ground_y
	ld	iy, #_ggroundy
	ld	0 (iy), l
	ld	1 (iy), #0x00
	ret
;src/systems/collision.c:10: u8 collision_is_on_ground(i16 y, u8 h) {
;	---------------------------------
; Function collision_is_on_ground
; ---------------------------------
_collision_is_on_ground::
;src/systems/collision.c:12: feet = y + (i16)h;
	ld	hl, #4+0
	add	hl, sp
	ld	c, (hl)
	ld	b, #0x00
	ld	hl, #2
	add	hl, sp
	ld	a, (hl)
	inc	hl
	ld	h, (hl)
	ld	l, a
	add	hl, bc
	ld	c, l
	ld	b, h
;src/systems/collision.c:13: return (u8)(feet >= ggroundy);
	ld	hl, #_ggroundy
	ld	a, c
	sub	a, (hl)
	ld	a, b
	inc	hl
	sbc	a, (hl)
	jp	PO, 00103$
	xor	a, #0x80
00103$:
	rlca
	and	a,#0x01
	xor	a, #0x01
	ld	l, a
	ret
;src/systems/collision.c:16: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
;	---------------------------------
; Function collision_clamp_y_to_ground
; ---------------------------------
_collision_clamp_y_to_ground::
;src/systems/collision.c:18: maxy = ggroundy - (i16)h;
	ld	hl, #4+0
	add	hl, sp
	ld	c, (hl)
	ld	b, #0x00
	ld	iy, #_ggroundy
	ld	a, 0 (iy)
	sub	a, c
	ld	c, a
	ld	a, 1 (iy)
	sbc	a, b
	ld	b, a
;src/systems/collision.c:19: if (y > maxy) {
	ld	a, c
	ld	iy, #2
	add	iy, sp
	sub	a, 0 (iy)
	ld	a, b
	sbc	a, 1 (iy)
	jp	PO, 00109$
	xor	a, #0x80
00109$:
	jp	P, 00102$
;src/systems/collision.c:20: return maxy;
	ld	l, c
	ld	h, b
	ret
00102$:
;src/systems/collision.c:22: return y;
	pop	bc
	pop	hl
	push	hl
	push	bc
	ret
	.area _CODE
	.area _INITIALIZER
__xinit__ggroundy:
	.dw #0x00a0
	.area _CABS (ABS)
