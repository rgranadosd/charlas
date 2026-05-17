;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module tilemap
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSolidBox
	.globl _cpct_px2byteM0
	.globl _tilemap_init
	.globl _tilemap_render
	.globl _tilemap_ground_y
	.globl _tilemap_platform_y_at
	.globl _tilemap_is_trap
	.globl _tilemap_is_ladder
	.globl _tilemap_is_hidden_zone
	.globl _tilemap_goal_x
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
_gtilegroundy:
	.ds 1
_gtileplatformy:
	.ds 1
_ggoalx:
	.ds 1
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
;src/systems/tilemap.c:9: void tilemap_init(void) {
;	---------------------------------
; Function tilemap_init
; ---------------------------------
_tilemap_init::
;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
	ld	hl, (_level1tilemapheight)
	ld	a, #0x02
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jr	NC,00102$
;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
	ld	a, l
	add	a, #0xfe
	rlca
	rlca
	rlca
	and	a, #0xf8
	ld	(#_gtilegroundy + 0),a
	jr	00103$
00102$:
;src/systems/tilemap.c:13: gtilegroundy = 160;
	ld	hl,#_gtilegroundy + 0
	ld	(hl), #0xa0
00103$:
;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
	ld	hl, #_gtileplatformy
	ld	a,(#_gtilegroundy + 0)
	add	a, #0xe8
	ld	(hl), a
;src/systems/tilemap.c:16: ggoalx = 72;
	ld	hl,#_ggoalx + 0
	ld	(hl), #0x48
	ret
;src/systems/tilemap.c:19: void tilemap_render(void) {
;	---------------------------------
; Function tilemap_render
; ---------------------------------
_tilemap_render::
;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
	ld	a, (_gtilegroundy)
	push	af
	inc	sp
	xor	a, a
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem,      cpct_px2byteM0(1, 1), 40, 8);
	push	hl
	ld	hl, #0x0101
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	push	bc
	pop	iy
	push	bc
	ld	hl, #0x0828
	push	hl
	push	de
	inc	sp
	push	iy
	call	_cpct_drawSolidBox
	pop	af
	inc	sp
	ld	hl,#0x0101
	ex	(sp),hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	ld	hl, #0x0028
	add	hl,bc
	ld	c, l
	ld	b, h
	ld	hl, #0x0828
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/systems/tilemap.c:25: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
	ld	a, (_gtileplatformy)
	ld	d,a
	ld	e,#0x18
	push	de
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/tilemap.c:26: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
	push	hl
	ld	hl, #0x0202
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	ld	hl, #0x0420
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/systems/tilemap.c:28: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
	ld	hl,#_gtilegroundy + 0
	ld	b, (hl)
	dec	b
	dec	b
	push	bc
	inc	sp
	ld	a, #0x38
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/tilemap.c:29: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
	push	hl
	ld	hl, #0x0303
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	ld	hl, #0x0210
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/systems/tilemap.c:31: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
	ld	a,(#_gtilegroundy + 0)
	add	a, #0xf0
	ld	b, a
	push	bc
	inc	sp
	ld	a, (_ggoalx)
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/tilemap.c:32: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
	push	hl
	ld	hl, #0x0505
	push	hl
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	ld	hl, #0x1002
	push	hl
	push	de
	inc	sp
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
;src/systems/tilemap.c:35: u8 tilemap_ground_y(void) {
;	---------------------------------
; Function tilemap_ground_y
; ---------------------------------
_tilemap_ground_y::
;src/systems/tilemap.c:36: return gtilegroundy;
	ld	iy, #_gtilegroundy
	ld	l, 0 (iy)
	ret
;src/systems/tilemap.c:39: u8 tilemap_platform_y_at(i16 x) {
;	---------------------------------
; Function tilemap_platform_y_at
; ---------------------------------
_tilemap_platform_y_at::
;src/systems/tilemap.c:40: if (x >= 24 && x <= 56) {
	ld	iy, #2
	add	iy, sp
	ld	a, 0 (iy)
	sub	a, #0x18
	ld	a, 1 (iy)
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	C,00102$
	ld	a, #0x38
	cp	a, 0 (iy)
	ld	a, #0x00
	sbc	a, 1 (iy)
	jp	PO, 00114$
	xor	a, #0x80
00114$:
	jp	M, 00102$
;src/systems/tilemap.c:41: return gtileplatformy;
	ld	iy, #_gtileplatformy
	ld	l, 0 (iy)
	ret
00102$:
;src/systems/tilemap.c:43: return 255;
	ld	l, #0xff
	ret
;src/systems/tilemap.c:46: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
;	---------------------------------
; Function tilemap_is_trap
; ---------------------------------
_tilemap_is_trap::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
;src/systems/tilemap.c:51: left = x;
	ld	c,4 (ix)
	ld	b,5 (ix)
;src/systems/tilemap.c:52: right = x + (i16)w;
	ld	l, 8 (ix)
	ld	h, #0x00
	add	hl, bc
	inc	sp
	inc	sp
	push	hl
;src/systems/tilemap.c:53: feet = y + (i16)h;
	ld	e, 9 (ix)
	ld	d, #0x00
	ld	l,6 (ix)
	ld	h,7 (ix)
	add	hl, de
	ex	de,hl
;src/systems/tilemap.c:55: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
	ld	iy, #_gtilegroundy
	ld	l, 0 (iy)
	ld	h, #0x00
	dec	hl
	dec	hl
	ld	a, e
	sub	a, l
	ld	a, d
	sbc	a, h
	jp	PO, 00119$
	xor	a, #0x80
00119$:
	jp	M, 00102$
	ld	a, c
	sub	a, #0x48
	ld	a, b
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	NC,00102$
	ld	a, #0x38
	cp	a, -2 (ix)
	ld	a, #0x00
	sbc	a, -1 (ix)
	jp	PO, 00120$
	xor	a, #0x80
00120$:
	jp	P, 00102$
;src/systems/tilemap.c:56: return 1;
	ld	l, #0x01
	jr	00105$
00102$:
;src/systems/tilemap.c:58: return 0;
	ld	l, #0x00
00105$:
	ld	sp, ix
	pop	ix
	ret
;src/systems/tilemap.c:61: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
;	---------------------------------
; Function tilemap_is_ladder
; ---------------------------------
_tilemap_is_ladder::
;src/systems/tilemap.c:66: return 0;
	ld	l, #0x00
	ret
;src/systems/tilemap.c:69: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
;	---------------------------------
; Function tilemap_is_hidden_zone
; ---------------------------------
_tilemap_is_hidden_zone::
;src/systems/tilemap.c:74: return 0;
	ld	l, #0x00
	ret
;src/systems/tilemap.c:77: u8 tilemap_goal_x(void) {
;	---------------------------------
; Function tilemap_goal_x
; ---------------------------------
_tilemap_goal_x::
;src/systems/tilemap.c:78: return ggoalx;
	ld	iy, #_ggoalx
	ld	l, 0 (iy)
	ret
	.area _CODE
	.area _INITIALIZER
__xinit__gtilegroundy:
	.db #0xa0	; 160
__xinit__gtileplatformy:
	.db #0x80	; 128
__xinit__ggoalx:
	.db #0x48	; 72	'H'
	.area _CABS (ABS)
