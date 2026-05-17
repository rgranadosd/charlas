;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module hud
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSprite
	.globl _hudinit
	.globl _hudupdate
	.globl _hudrender
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
_currenthealth:
	.ds 1
_currentscore:
	.ds 2
_currenttime:
	.ds 1
_currentlives:
	.ds 1
_currentweapon:
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
;src/systems/hud.c:13: static const u8* hud_get_number_sprite(u8 n) {
;	---------------------------------
; Function hud_get_number_sprite
; ---------------------------------
_hud_get_number_sprite:
;src/systems/hud.c:15: return _hud_dummy_sprite;
	ld	hl, #__hud_dummy_sprite
	ret
__hud_dummy_sprite:
	.db #0x00	; 0
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
;src/systems/hud.c:20: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
;	---------------------------------
; Function hud_draw_digits
; ---------------------------------
_hud_draw_digits:
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/systems/hud.c:26: divisor = 1;
	ld	bc, #0x0001
;src/systems/hud.c:27: for (i = 1; i < digits; ++i) {
	ld	e, #0x01
00106$:
	ld	a, e
	sub	a, 6 (ix)
	jr	NC,00101$
;src/systems/hud.c:28: divisor *= 10;
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	c, l
	ld	b, h
;src/systems/hud.c:27: for (i = 1; i < digits; ++i) {
	inc	e
	jr	00106$
00101$:
;src/systems/hud.c:31: for (i = 0; i < digits; ++i) {
	ld	-1 (ix), #0x00
00109$:
	ld	a, -1 (ix)
	sub	a, 6 (ix)
	jp	NC, 00111$
;src/systems/hud.c:32: digit = (u8)(value / divisor);
	push	bc
	push	bc
	ld	l,4 (ix)
	ld	h,5 (ix)
	push	hl
	call	__divuint
	pop	af
	pop	af
	ld	e, l
	pop	bc
;src/systems/hud.c:33: value = (u16)(value % divisor);
	push	bc
	push	de
	push	bc
	ld	l,4 (ix)
	ld	h,5 (ix)
	push	hl
	call	__moduint
	pop	af
	pop	af
	pop	de
	pop	bc
	ld	4 (ix), l
	ld	5 (ix), h
;src/systems/hud.c:35: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
	ld	a, -1 (ix)
	rlca
	rlca
	rlca
	and	a, #0xf8
	ld	d, a
	ld	a, 7 (ix)
	add	a, d
	ld	d, a
	push	bc
	push	de
	ld	a, 8 (ix)
	push	af
	inc	sp
	push	de
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	pop	de
	pop	bc
;src/systems/hud.c:36: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
	push	hl
	push	bc
	ld	a, e
	push	af
	inc	sp
	call	_hud_get_number_sprite
	inc	sp
	ex	de,hl
	pop	bc
	pop	hl
	push	de
	pop	iy
	push	bc
	ld	de, #0x0808
	push	de
	push	hl
	push	iy
	call	_cpct_drawSprite
	pop	bc
;src/systems/hud.c:38: if (divisor > 1) {
	ld	a, #0x01
	cp	a, c
	ld	a, #0x00
	sbc	a, b
	jr	NC,00110$
;src/systems/hud.c:39: divisor /= 10;
	ld	hl, #0x000a
	push	hl
	push	bc
	call	__divuint
	pop	af
	pop	af
	ld	c, l
	ld	b, h
00110$:
;src/systems/hud.c:31: for (i = 0; i < digits; ++i) {
	inc	-1 (ix)
	jp	00109$
00111$:
	inc	sp
	pop	ix
	ret
_hudhealth:
	.db #0x00	; 0
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
_hudlives:
	.db #0x00	; 0
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
	.db 0x00
;src/systems/hud.c:44: void hudinit(void) {
;	---------------------------------
; Function hudinit
; ---------------------------------
_hudinit::
;src/systems/hud.c:45: currenthealth = 3;
	ld	hl,#_currenthealth + 0
	ld	(hl), #0x03
;src/systems/hud.c:46: currentscore  = 0;
	ld	hl, #0x0000
	ld	(_currentscore), hl
;src/systems/hud.c:47: currenttime   = 90;
	ld	hl,#_currenttime + 0
	ld	(hl), #0x5a
;src/systems/hud.c:48: currentlives  = 3;
	ld	hl,#_currentlives + 0
	ld	(hl), #0x03
;src/systems/hud.c:49: currentweapon = 0;
	ld	hl,#_currentweapon + 0
	ld	(hl), #0x00
	ret
;src/systems/hud.c:52: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
;	---------------------------------
; Function hudupdate
; ---------------------------------
_hudupdate::
;src/systems/hud.c:53: currenthealth = lives;
	ld	hl, #2+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currenthealth + 0),a
;src/systems/hud.c:54: currentscore  = score;
	ld	hl, #3+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentscore + 0),a
	ld	hl, #3+1
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentscore + 1),a
;src/systems/hud.c:55: currenttime   = time;
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currenttime + 0),a
;src/systems/hud.c:56: currentlives  = lives;
	ld	hl, #2+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentlives + 0),a
;src/systems/hud.c:57: currentweapon = weapon;
	ld	hl, #6+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentweapon + 0),a
	ret
;src/systems/hud.c:60: void hudrender(void) {
;	---------------------------------
; Function hudrender
; ---------------------------------
_hudrender::
;src/systems/hud.c:66: for (i = 0; i < currenthealth; ++i) {
	ld	c, #0x00
00103$:
	ld	hl, #_currenthealth
;src/systems/hud.c:67: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
	ld	a,c
	cp	a,(hl)
	jr	NC,00101$
	rlca
	rlca
	rlca
	and	a, #0xf8
	ld	b, a
	push	bc
	ld	a, #0x02
	push	af
	inc	sp
	push	bc
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ld	de, #0x0808
	push	de
	push	hl
	ld	hl, #_hudhealth
	push	hl
	call	_cpct_drawSprite
	pop	bc
;src/systems/hud.c:66: for (i = 0; i < currenthealth; ++i) {
	inc	c
	jr	00103$
00101$:
;src/systems/hud.c:71: scoretemp = currentscore;
	ld	hl, (_currentscore)
;src/systems/hud.c:72: hud_draw_digits(scoretemp, 4, 24, 2);
	ld	bc, #0x0218
	push	bc
	ld	a, #0x04
	push	af
	inc	sp
	push	hl
	call	_hud_draw_digits
	pop	af
	pop	af
	inc	sp
;src/systems/hud.c:74: timetemp = currenttime;
	ld	hl,#_currenttime + 0
	ld	c, (hl)
;src/systems/hud.c:75: hud_draw_digits((u16)timetemp, 3, 56, 2);
	ld	b, #0x00
	ld	hl, #0x0238
	push	hl
	ld	a, #0x03
	push	af
	inc	sp
	push	bc
	call	_hud_draw_digits
	pop	af
;src/systems/hud.c:77: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
	inc	sp
	ld	hl,#0xb402
	ex	(sp),hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/hud.c:78: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
	ld	bc, #_hudlives+0
	ld	de, #0x0808
	push	de
	push	hl
	push	bc
	call	_cpct_drawSprite
;src/systems/hud.c:80: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
	ld	hl, #0xb40c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/hud.c:81: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);
	push	hl
	ld	a, #0x0a
	push	af
	inc	sp
	ld	a, (_currentlives)
	push	af
	inc	sp
	call	__moduchar
	pop	af
	ld	d, l
	push	de
	inc	sp
	call	_hud_get_number_sprite
	inc	sp
	pop	bc
	ld	de, #0x0808
	push	de
	push	bc
	push	hl
	call	_cpct_drawSprite
;src/systems/hud.c:83: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
	ld	hl, #0xb446
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/hud.c:84: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
	push	hl
	ld	a, #0x0a
	push	af
	inc	sp
	ld	a, (_currentweapon)
	push	af
	inc	sp
	call	__moduchar
	pop	af
	ld	d, l
	push	de
	inc	sp
	call	_hud_get_number_sprite
	inc	sp
	pop	bc
	ld	de, #0x0808
	push	de
	push	bc
	push	hl
	call	_cpct_drawSprite
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
