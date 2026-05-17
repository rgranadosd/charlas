;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module main
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _main
	.globl _cpc_entry_wrapper
	.globl _game_render
	.globl _game_update
	.globl _game_init
	.globl _cpct_waitVSYNC
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
;src/main.c:4: void cpc_entry_wrapper(void) __naked {
;	---------------------------------
; Function cpc_entry_wrapper
; ---------------------------------
_cpc_entry_wrapper::
;src/main.c:23: __endasm;
	.globl	cpc_run_address
	.globl	s__INITIALIZER
	.globl	s__INITIALIZED
	.globl	l__INITIALIZER
	    cpc_run_address::
	di
	ld	sp, #0xBFF0
	ld	bc, #l__INITIALIZER
	ld	a, b
	or	c
	jr	z, 00001$
	ld	de, #s__INITIALIZED
	ld	hl, #s__INITIALIZER
	ldir
	00001$:
	call	_main
	ret
;src/main.c:26: void main(void) {
;	---------------------------------
; Function main
; ---------------------------------
_main::
;src/main.c:31: __endasm;
	di
	ld	sp, #0xBFF0
;src/main.c:33: game_init();
	call	_game_init
;src/main.c:34: while (1) {
00102$:
;src/main.c:35: game_update();
	call	_game_update
;src/main.c:36: cpct_waitVSYNC();  /* sync BEFORE clear+draw: beam is at top when we start clearing */
	call	_cpct_waitVSYNC
;src/main.c:37: game_render();
	call	_game_render
	jr	00102$
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
