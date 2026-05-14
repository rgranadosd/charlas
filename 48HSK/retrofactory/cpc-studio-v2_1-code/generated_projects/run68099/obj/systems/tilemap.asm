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
	.globl _tilemap_init
	.globl _tilemap_render
	.globl _tilemap_ground_y
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
;src/systems/tilemap.c:7: void tilemap_init(void) {
;	---------------------------------
; Function tilemap_init
; ---------------------------------
_tilemap_init::
;src/systems/tilemap.c:8: if (level1tilemapheight > 2) {
	ld	hl, (_level1tilemapheight)
	ld	a, #0x02
	cp	a, l
	ld	a, #0x00
	sbc	a, h
	jr	NC,00102$
;src/systems/tilemap.c:9: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
	ld	a, l
	add	a, #0xfe
	rlca
	rlca
	rlca
	and	a, #0xf8
	ld	(#_gtilegroundy + 0),a
	ret
00102$:
;src/systems/tilemap.c:11: gtilegroundy = 160;
	ld	hl,#_gtilegroundy + 0
	ld	(hl), #0xa0
	ret
;src/systems/tilemap.c:15: void tilemap_render(void) {
;	---------------------------------
; Function tilemap_render
; ---------------------------------
_tilemap_render::
;src/systems/tilemap.c:17: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
	ld	a, (_gtilegroundy)
	push	af
	inc	sp
	xor	a, a
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/tilemap.c:18: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
	ld	bc, #0x0850
	push	bc
	ld	a, #0x11
	push	af
	inc	sp
	push	hl
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
;src/systems/tilemap.c:21: u8 tilemap_ground_y(void) {
;	---------------------------------
; Function tilemap_ground_y
; ---------------------------------
_tilemap_ground_y::
;src/systems/tilemap.c:22: return gtilegroundy;
	ld	iy, #_gtilegroundy
	ld	l, 0 (iy)
	ret
	.area _CODE
	.area _INITIALIZER
__xinit__gtilegroundy:
	.db #0xa0	; 160
	.area _CABS (ABS)
