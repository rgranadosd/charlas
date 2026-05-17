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
;src/main.c:10: __endasm;
	.globl	cpc_run_address
	    cpc_run_address::
	call	_main
	ret
;src/main.c:13: void main(void) {
;	---------------------------------
; Function main
; ---------------------------------
_main::
;src/main.c:18: __endasm;
	di
	ld	sp, #0xBFF0
;src/main.c:20: game_init();
	call	_game_init
;src/main.c:21: while (1) {
00102$:
;src/main.c:22: game_update();
	call	_game_update
;src/main.c:23: game_render();
	call	_game_render
;src/main.c:24: cpct_waitVSYNC();
	call	_cpct_waitVSYNC
	jr	00102$
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
