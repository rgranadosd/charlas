;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module game
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_setVideoMode
	.globl _cpct_memset
	.globl _cpct_disableFirmware
	.globl _game_init
	.globl _game_update
	.globl _game_render
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
;src/game.c:4: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/game.c:5: cpct_disableFirmware();
	call	_cpct_disableFirmware
;src/game.c:6: cpct_setVideoMode(1);
	ld	l, #0x01
	call	_cpct_setVideoMode
;src/game.c:7: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
	ret
;src/game.c:10: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
;src/game.c:11: }
	ret
;src/game.c:13: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/game.c:14: }
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
