;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module player
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
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
;src/entities/player.c:3: void player_init(void) {
;	---------------------------------
; Function player_init
; ---------------------------------
_player_init::
;src/entities/player.c:4: }
	ret
;src/entities/player.c:6: void player_update(void) {
;	---------------------------------
; Function player_update
; ---------------------------------
_player_update::
;src/entities/player.c:8: }
	ret
;src/entities/player.c:10: void player_render(void) {
;	---------------------------------
; Function player_render
; ---------------------------------
_player_render::
;src/entities/player.c:12: }
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
