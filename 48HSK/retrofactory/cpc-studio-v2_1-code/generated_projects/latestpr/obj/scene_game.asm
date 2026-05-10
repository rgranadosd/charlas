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
;src/scene_game.c:83: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/scene_game.c:84: player_init();
	jp  _player_init
;src/scene_game.c:87: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
;src/scene_game.c:88: input_update();
	call	_input_update
;src/scene_game.c:89: player_update();
	jp  _player_update
;src/scene_game.c:92: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/scene_game.c:93: player_render();
	jp  _player_render
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
