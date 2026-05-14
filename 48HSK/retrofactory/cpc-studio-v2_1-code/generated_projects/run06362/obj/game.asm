;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module game
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _playerrender
	.globl _playerupdate
	.globl _playerinit
	.globl _collision_init
	.globl _input_update
	.globl _tilemap_render
	.globl _tilemap_init
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
_g_player:
	.ds 6
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
;src/game.c:10: void game_init(void) {
;	---------------------------------
; Function game_init
; ---------------------------------
_game_init::
;src/game.c:11: cpct_disableFirmware();
	call	_cpct_disableFirmware
;src/game.c:12: cpct_setVideoMode(1);
	ld	l, #0x01
	call	_cpct_setVideoMode
;src/game.c:13: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:14: tilemap_init();
	call	_tilemap_init
;src/game.c:15: collision_init();
	call	_collision_init
;src/game.c:16: playerinit(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerinit
	pop	af
	ret
;src/game.c:19: void game_update(void) {
;	---------------------------------
; Function game_update
; ---------------------------------
_game_update::
;src/game.c:20: input_update();
	call	_input_update
;src/game.c:21: playerupdate(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerupdate
	pop	af
	ret
;src/game.c:24: void game_render(void) {
;	---------------------------------
; Function game_render
; ---------------------------------
_game_render::
;src/game.c:25: cpct_clearScreen(0x00);
	ld	hl, #0x4000
	push	hl
	xor	a, a
	push	af
	inc	sp
	ld	h, #0xc0
	push	hl
	call	_cpct_memset
;src/game.c:26: tilemap_render();
	call	_tilemap_render
;src/game.c:27: playerrender(&g_player);
	ld	hl, #_g_player
	push	hl
	call	_playerrender
	pop	af
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
