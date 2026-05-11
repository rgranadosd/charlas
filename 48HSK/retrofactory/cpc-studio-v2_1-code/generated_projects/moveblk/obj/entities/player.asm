;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module player
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSolidBox
	.globl _cpct_isKeyPressed
	.globl _player_init
	.globl _player_update
	.globl _player_render
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
_px:
	.ds 1
_py:
	.ds 1
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
;src/entities/player.c:7: void player_init(void) {
;	---------------------------------
; Function player_init
; ---------------------------------
_player_init::
;src/entities/player.c:8: px = 20;
	ld	hl,#_px + 0
	ld	(hl), #0x14
;src/entities/player.c:9: py = 80;
	ld	hl,#_py + 0
	ld	(hl), #0x50
	ret
;src/entities/player.c:12: void player_update(void) {
;	---------------------------------
; Function player_update
; ---------------------------------
_player_update::
;src/entities/player.c:13: if (cpct_isKeyPressed(Key_CursorLeft) && px > 0)
	ld	hl, #0x0101
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	Z,00102$
	ld	iy, #_px
	ld	a, 0 (iy)
	or	a, a
	jr	Z,00102$
;src/entities/player.c:14: px -= 2;
	dec	0 (iy)
	dec	0 (iy)
00102$:
;src/entities/player.c:16: if (cpct_isKeyPressed(Key_CursorRight) && px < 70)
	ld	hl, #0x0200
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	ret	Z
	ld	iy, #_px
	ld	a, 0 (iy)
	sub	a, #0x46
	ret	NC
;src/entities/player.c:17: px += 2;
	inc	0 (iy)
	inc	0 (iy)
	ret
;src/entities/player.c:20: void player_render(void) {
;	---------------------------------
; Function player_render
; ---------------------------------
_player_render::
;src/entities/player.c:23: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, py);
	ld	a, (_py)
	push	af
	inc	sp
	xor	a, a
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/entities/player.c:24: cpct_drawSolidBox(pvmem, 0x00, 80, 8);
	ld	bc, #0x0850
	push	bc
	xor	a, a
	push	af
	inc	sp
	push	hl
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
;src/entities/player.c:26: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, px, py);
	ld	a, (_py)
	push	af
	inc	sp
	ld	a, (_px)
	push	af
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/entities/player.c:27: cpct_drawSolidBox(pvmem, 0xF0, 4, 8);
	ld	bc, #0x0804
	push	bc
	ld	a, #0xf0
	push	af
	inc	sp
	push	hl
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
