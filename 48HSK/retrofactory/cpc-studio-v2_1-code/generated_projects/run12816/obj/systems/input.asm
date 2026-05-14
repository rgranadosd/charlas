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
	.globl _input_is_jump_just_pressed
	.globl _input_is_shoot_pressed
	.globl _input_is_shoot_just_pressed
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
_ginputshoot:
	.ds 1
_gprevjump:
	.ds 1
_gprevshoot:
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
;src/systems/input.c:10: void input_update(void) {
;	---------------------------------
; Function input_update
; ---------------------------------
_input_update::
;src/systems/input.c:11: gprevjump = ginputjump;
	ld	a,(#_ginputjump + 0)
	ld	(#_gprevjump + 0),a
;src/systems/input.c:12: gprevshoot = ginputshoot;
	ld	a,(#_ginputshoot + 0)
	ld	(#_gprevshoot + 0),a
;src/systems/input.c:13: cpct_scanKeyboard_f();
	call	_cpct_scanKeyboard_f
;src/systems/input.c:14: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
	ld	hl, #0x0101
	call	_cpct_isKeyPressed
	ld	iy, #_ginputleft
	ld	0 (iy), l
;src/systems/input.c:15: ginputright = cpct_isKeyPressed(Key_CursorRight);
	ld	hl, #0x0200
	call	_cpct_isKeyPressed
	ld	iy, #_ginputright
	ld	0 (iy), l
;src/systems/input.c:16: ginputjump = cpct_isKeyPressed(Key_CursorUp);
	ld	hl, #0x0100
	call	_cpct_isKeyPressed
	ld	iy, #_ginputjump
	ld	0 (iy), l
;src/systems/input.c:17: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
	ld	hl, #0x0400
	call	_cpct_isKeyPressed
	ld	iy, #_ginputshoot
	ld	0 (iy), l
	ret
;src/systems/input.c:20: u8 input_is_left_pressed(void) {
;	---------------------------------
; Function input_is_left_pressed
; ---------------------------------
_input_is_left_pressed::
;src/systems/input.c:21: return ginputleft;
	ld	iy, #_ginputleft
	ld	l, 0 (iy)
	ret
;src/systems/input.c:24: u8 input_is_right_pressed(void) {
;	---------------------------------
; Function input_is_right_pressed
; ---------------------------------
_input_is_right_pressed::
;src/systems/input.c:25: return ginputright;
	ld	iy, #_ginputright
	ld	l, 0 (iy)
	ret
;src/systems/input.c:28: u8 input_is_jump_pressed(void) {
;	---------------------------------
; Function input_is_jump_pressed
; ---------------------------------
_input_is_jump_pressed::
;src/systems/input.c:29: return ginputjump;
	ld	iy, #_ginputjump
	ld	l, 0 (iy)
	ret
;src/systems/input.c:32: u8 input_is_jump_just_pressed(void) {
;	---------------------------------
; Function input_is_jump_just_pressed
; ---------------------------------
_input_is_jump_just_pressed::
;src/systems/input.c:33: return (u8)(ginputjump && !gprevjump);
	ld	a,(#_ginputjump + 0)
	or	a, a
	jr	Z,00103$
	ld	a,(#_gprevjump + 0)
	or	a, a
	jr	Z,00104$
00103$:
	ld	l, #0x00
	ret
00104$:
	ld	l, #0x01
	ret
;src/systems/input.c:36: u8 input_is_shoot_pressed(void) {
;	---------------------------------
; Function input_is_shoot_pressed
; ---------------------------------
_input_is_shoot_pressed::
;src/systems/input.c:37: return ginputshoot;
	ld	iy, #_ginputshoot
	ld	l, 0 (iy)
	ret
;src/systems/input.c:40: u8 input_is_shoot_just_pressed(void) {
;	---------------------------------
; Function input_is_shoot_just_pressed
; ---------------------------------
_input_is_shoot_just_pressed::
;src/systems/input.c:41: return (u8)(ginputshoot && !gprevshoot);
	ld	a,(#_ginputshoot + 0)
	or	a, a
	jr	Z,00103$
	ld	a,(#_gprevshoot + 0)
	or	a, a
	jr	Z,00104$
00103$:
	ld	l, #0x00
	ret
00104$:
	ld	l, #0x01
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
