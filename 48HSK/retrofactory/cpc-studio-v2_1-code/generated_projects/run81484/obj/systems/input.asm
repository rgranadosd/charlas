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
	.globl _cpct_scanKeyboard
	.globl _input_update
	.globl _input_is_left_pressed
	.globl _input_is_right_pressed
	.globl _input_is_up_pressed
	.globl _input_is_down_pressed
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
_ginputup:
	.ds 1
_ginputdown:
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
;src/systems/input.c:12: void input_update(void) {
;	---------------------------------
; Function input_update
; ---------------------------------
_input_update::
;src/systems/input.c:13: gprevjump = ginputjump;
	ld	a,(#_ginputjump + 0)
	ld	(#_gprevjump + 0),a
;src/systems/input.c:14: gprevshoot = ginputshoot;
	ld	a,(#_ginputshoot + 0)
	ld	(#_gprevshoot + 0),a
;src/systems/input.c:15: cpct_scanKeyboard();
	call	_cpct_scanKeyboard
;src/systems/input.c:20: ginputleft  = (u8)(cpct_isKeyPressed(Key_CursorLeft)  || cpct_isKeyPressed(Key_O) || cpct_isKeyPressed(Key_A) || cpct_isKeyPressed(Joy0_Left));
	ld	hl, #0x0101
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00104$
	ld	hl, #0x0404
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00104$
	ld	hl, #0x2008
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00104$
	ld	hl, #0x0409
	call	_cpct_isKeyPressed
	ld	a, l
	or	a,a
	jr	NZ,00104$
	ld	c,a
	jr	00105$
00104$:
	ld	c, #0x01
00105$:
	ld	hl,#_ginputleft + 0
	ld	(hl), c
;src/systems/input.c:21: ginputright = (u8)(cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_P) || cpct_isKeyPressed(Key_D) || cpct_isKeyPressed(Joy0_Right));
	ld	hl, #0x0200
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00113$
	ld	hl, #0x0803
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00113$
	ld	hl, #0x2007
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00113$
	ld	hl, #0x0809
	call	_cpct_isKeyPressed
	ld	a, l
	or	a,a
	jr	NZ,00113$
	ld	c,a
	jr	00114$
00113$:
	ld	c, #0x01
00114$:
	ld	hl,#_ginputright + 0
	ld	(hl), c
;src/systems/input.c:22: ginputup    = (u8)(cpct_isKeyPressed(Key_CursorUp)    || cpct_isKeyPressed(Key_Q) || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Joy0_Up));
	ld	hl, #0x0100
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00122$
	ld	hl, #0x0808
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00122$
	ld	hl, #0x0807
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00122$
	ld	hl, #0x0109
	call	_cpct_isKeyPressed
	ld	a, l
	or	a,a
	jr	NZ,00122$
	ld	c,a
	jr	00123$
00122$:
	ld	c, #0x01
00123$:
	ld	hl,#_ginputup + 0
	ld	(hl), c
;src/systems/input.c:23: ginputdown  = (u8)(cpct_isKeyPressed(Key_CursorDown)  || cpct_isKeyPressed(Key_S) || cpct_isKeyPressed(Joy0_Down));
	ld	hl, #0x0400
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00131$
	ld	hl, #0x1007
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00131$
	ld	hl, #0x0209
	call	_cpct_isKeyPressed
	ld	a, l
	or	a,a
	jr	NZ,00131$
	ld	c,a
	jr	00132$
00131$:
	ld	c, #0x01
00132$:
	ld	hl,#_ginputdown + 0
	ld	(hl), c
;src/systems/input.c:24: ginputjump  = (u8)(cpct_isKeyPressed(Key_Space) || cpct_isKeyPressed(Key_Z) || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Joy0_Fire1));
	ld	hl, #0x8005
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00137$
	ld	hl, #0x8008
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00137$
	ld	hl, #0x8007
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00137$
	ld	hl, #0x1009
	call	_cpct_isKeyPressed
	ld	a, l
	or	a,a
	jr	NZ,00137$
	ld	c,a
	jr	00138$
00137$:
	ld	c, #0x01
00138$:
	ld	hl,#_ginputjump + 0
	ld	(hl), c
;src/systems/input.c:25: ginputshoot = (u8)(cpct_isKeyPressed(Key_Control) || cpct_isKeyPressed(Key_Return) || cpct_isKeyPressed(Key_CursorDown) || cpct_isKeyPressed(Joy0_Fire2) || cpct_isKeyPressed(Joy0_Fire3));
	ld	hl, #0x8002
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00146$
	ld	hl, #0x0402
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00146$
	ld	hl, #0x0400
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00146$
	ld	hl, #0x2009
	call	_cpct_isKeyPressed
	ld	a, l
	or	a, a
	jr	NZ,00146$
	ld	hl, #0x4009
	call	_cpct_isKeyPressed
	ld	a, l
	or	a,a
	jr	NZ,00146$
	ld	c,a
	jr	00147$
00146$:
	ld	c, #0x01
00147$:
	ld	hl,#_ginputshoot + 0
	ld	(hl), c
	ret
;src/systems/input.c:28: u8 input_is_left_pressed(void) {
;	---------------------------------
; Function input_is_left_pressed
; ---------------------------------
_input_is_left_pressed::
;src/systems/input.c:29: return ginputleft;
	ld	iy, #_ginputleft
	ld	l, 0 (iy)
	ret
;src/systems/input.c:32: u8 input_is_right_pressed(void) {
;	---------------------------------
; Function input_is_right_pressed
; ---------------------------------
_input_is_right_pressed::
;src/systems/input.c:33: return ginputright;
	ld	iy, #_ginputright
	ld	l, 0 (iy)
	ret
;src/systems/input.c:36: u8 input_is_up_pressed(void) {
;	---------------------------------
; Function input_is_up_pressed
; ---------------------------------
_input_is_up_pressed::
;src/systems/input.c:37: return ginputup;
	ld	iy, #_ginputup
	ld	l, 0 (iy)
	ret
;src/systems/input.c:40: u8 input_is_down_pressed(void) {
;	---------------------------------
; Function input_is_down_pressed
; ---------------------------------
_input_is_down_pressed::
;src/systems/input.c:41: return ginputdown;
	ld	iy, #_ginputdown
	ld	l, 0 (iy)
	ret
;src/systems/input.c:44: u8 input_is_jump_pressed(void) {
;	---------------------------------
; Function input_is_jump_pressed
; ---------------------------------
_input_is_jump_pressed::
;src/systems/input.c:45: return ginputjump;
	ld	iy, #_ginputjump
	ld	l, 0 (iy)
	ret
;src/systems/input.c:48: u8 input_is_jump_just_pressed(void) {
;	---------------------------------
; Function input_is_jump_just_pressed
; ---------------------------------
_input_is_jump_just_pressed::
;src/systems/input.c:49: return (u8)(ginputjump && !gprevjump);
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
;src/systems/input.c:52: u8 input_is_shoot_pressed(void) {
;	---------------------------------
; Function input_is_shoot_pressed
; ---------------------------------
_input_is_shoot_pressed::
;src/systems/input.c:53: return ginputshoot;
	ld	iy, #_ginputshoot
	ld	l, 0 (iy)
	ret
;src/systems/input.c:56: u8 input_is_shoot_just_pressed(void) {
;	---------------------------------
; Function input_is_shoot_just_pressed
; ---------------------------------
_input_is_shoot_just_pressed::
;src/systems/input.c:57: return (u8)(ginputshoot && !gprevshoot);
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
