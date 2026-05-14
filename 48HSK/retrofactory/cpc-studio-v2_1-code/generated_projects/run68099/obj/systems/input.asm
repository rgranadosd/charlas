;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module input
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_isKeyPressed
	.globl _cpct_scanKeyboard_f
	.globl _input_update
	.globl _input_is_left_pressed
	.globl _input_is_right_pressed
	.globl _input_is_jump_pressed
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
_ginputleft:
	.ds 1
_ginputright:
	.ds 1
_ginputjump:
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
;src/systems/input.c:7: void input_update(void) {
;	---------------------------------
; Function input_update
; ---------------------------------
_input_update::
;src/systems/input.c:8: cpct_scanKeyboard_f();
	call	_cpct_scanKeyboard_f
;src/systems/input.c:9: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
	ld	hl, #0x0101
	call	_cpct_isKeyPressed
	ld	iy, #_ginputleft
	ld	0 (iy), l
;src/systems/input.c:10: ginputright = cpct_isKeyPressed(Key_CursorRight);
	ld	hl, #0x0200
	call	_cpct_isKeyPressed
	ld	iy, #_ginputright
	ld	0 (iy), l
;src/systems/input.c:11: ginputjump = cpct_isKeyPressed(Key_CursorUp);
	ld	hl, #0x0100
	call	_cpct_isKeyPressed
	ld	iy, #_ginputjump
	ld	0 (iy), l
	ret
;src/systems/input.c:14: u8 input_is_left_pressed(void) {
;	---------------------------------
; Function input_is_left_pressed
; ---------------------------------
_input_is_left_pressed::
;src/systems/input.c:15: return ginputleft;
	ld	iy, #_ginputleft
	ld	l, 0 (iy)
	ret
;src/systems/input.c:18: u8 input_is_right_pressed(void) {
;	---------------------------------
; Function input_is_right_pressed
; ---------------------------------
_input_is_right_pressed::
;src/systems/input.c:19: return ginputright;
	ld	iy, #_ginputright
	ld	l, 0 (iy)
	ret
;src/systems/input.c:22: u8 input_is_jump_pressed(void) {
;	---------------------------------
; Function input_is_jump_pressed
; ---------------------------------
_input_is_jump_pressed::
;src/systems/input.c:23: return ginputjump;
	ld	iy, #_ginputjump
	ld	l, 0 (iy)
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
