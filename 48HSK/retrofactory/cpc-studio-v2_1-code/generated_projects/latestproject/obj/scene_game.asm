;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module scene_game
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _player_render
	.globl _player_update
	.globl _player_init
	.globl _input_update
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
;src/scene_game.c:18: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/scene_game.c:19: player_init();
	jp  _player_init
;src/scene_game.c:22: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
;src/scene_game.c:23: input_update();
	call	_input_update
;src/scene_game.c:24: player_update();
	jp  _player_update
;src/scene_game.c:27: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/scene_game.c:28: player_render();
	jp  _player_render
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
