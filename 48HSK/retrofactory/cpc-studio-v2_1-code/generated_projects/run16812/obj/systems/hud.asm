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
	.globl _cpct_drawSolidBox
	.globl _cpct_drawSprite
	.globl _cpct_px2byteM0
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
;src/systems/hud.c:16: static const u8* hud_get_number_sprite(u8 digit) {
;	---------------------------------
; Function hud_get_number_sprite
; ---------------------------------
_hud_get_number_sprite:
;src/systems/hud.c:18: return _hud_dummy_sprite;
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
;src/systems/hud.c:21: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
;	---------------------------------
; Function hud_draw_digits
; ---------------------------------
_hud_draw_digits:
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/systems/hud.c:27: divisor = 1;
	ld	bc, #0x0001
;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
	ld	e, #0x01
00106$:
	ld	a, e
	sub	a, 6 (ix)
	jr	NC,00101$
;src/systems/hud.c:29: divisor *= 10;
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	c, l
	ld	b, h
;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
	inc	e
	jr	00106$
00101$:
;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
	ld	-1 (ix), #0x00
00109$:
	ld	a, -1 (ix)
	sub	a, 6 (ix)
	jp	NC, 00111$
;src/systems/hud.c:33: digit = (u8)(value / divisor);
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
;src/systems/hud.c:34: value = (u16)(value % divisor);
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
;src/systems/hud.c:36: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
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
;src/systems/hud.c:37: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
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
;src/systems/hud.c:39: if (divisor > 1) {
	ld	a, #0x01
	cp	a, c
	ld	a, #0x00
	sbc	a, b
	jr	NC,00110$
;src/systems/hud.c:40: divisor /= 10;
	ld	hl, #0x000a
	push	hl
	push	bc
	call	__divuint
	pop	af
	pop	af
	ld	c, l
	ld	b, h
00110$:
;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
	inc	-1 (ix)
	jp	00109$
00111$:
	inc	sp
	pop	ix
	ret
;src/systems/hud.c:45: void hudinit(void) {
;	---------------------------------
; Function hudinit
; ---------------------------------
_hudinit::
;src/systems/hud.c:46: currenthealth = 3;
	ld	hl,#_currenthealth + 0
	ld	(hl), #0x03
;src/systems/hud.c:47: currentscore  = 0;
	ld	hl, #0x0000
	ld	(_currentscore), hl
;src/systems/hud.c:48: currenttime   = 90;
	ld	hl,#_currenttime + 0
	ld	(hl), #0x5a
;src/systems/hud.c:49: currentlives  = 3;
	ld	hl,#_currentlives + 0
	ld	(hl), #0x03
;src/systems/hud.c:50: currentweapon = 0;
	ld	hl,#_currentweapon + 0
	ld	(hl), #0x00
	ret
;src/systems/hud.c:53: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
;	---------------------------------
; Function hudupdate
; ---------------------------------
_hudupdate::
;src/systems/hud.c:54: currenthealth = lives;
	ld	hl, #2+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currenthealth + 0),a
;src/systems/hud.c:55: currentscore  = score;
	ld	hl, #3+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentscore + 0),a
	ld	hl, #3+1
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentscore + 1),a
;src/systems/hud.c:56: currenttime   = time;
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currenttime + 0),a
;src/systems/hud.c:57: currentlives  = lives;
	ld	hl, #2+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentlives + 0),a
;src/systems/hud.c:58: currentweapon = weapon;
	ld	hl, #6+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentweapon + 0),a
	ret
;src/systems/hud.c:61: void hudrender(void) {
;	---------------------------------
; Function hudrender
; ---------------------------------
_hudrender::
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/systems/hud.c:68: for (i = 0; i < currenthealth && i < 5; ++i) {
	ld	c, #0x00
00115$:
	ld	hl, #_currenthealth
	ld	a,c
	cp	a,(hl)
	jr	NC,00101$
;src/systems/hud.c:69: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (u8)(i * 3), 2);
	cp	a,#0x05
	jr	NC,00101$
	add	a, a
	add	a, c
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
	pop	bc
;src/systems/hud.c:70: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), 2, 4);
	push	hl
	push	bc
	ld	de, #0x0606
	push	de
	call	_cpct_px2byteM0
	ld	d, l
	pop	bc
	pop	hl
	ld	e, l
	ld	b, h
	push	bc
	ld	hl, #0x0402
	push	hl
	push	de
	inc	sp
	ld	c,e
	push	bc
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/systems/hud.c:68: for (i = 0; i < currenthealth && i < 5; ++i) {
	inc	c
	jr	00115$
00101$:
;src/systems/hud.c:73: scorebar = (u8)(currentscore / 100);
	ld	hl, #0x0064
	push	hl
	ld	hl, (_currentscore)
	push	hl
	call	__divuint
	pop	af
	pop	af
	ld	c, l
;src/systems/hud.c:74: if (scorebar > 20) {
	ld	a, #0x14
	sub	a, c
	jr	NC,00103$
;src/systems/hud.c:75: scorebar = 20;
	ld	c, #0x14
00103$:
;src/systems/hud.c:77: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, 2);
	push	bc
	ld	hl, #0x0218
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	push	hl
	ld	hl, #0x0101
	push	hl
	call	_cpct_px2byteM0
	ld	b, l
	pop	de
	ld	a, b
	pop	bc
	ld	b, a
;src/systems/hud.c:70: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), 2, 4);
;src/systems/hud.c:78: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 20, 2);
	push	bc
	push	de
	ld	hl, #0x0214
	push	hl
	push	bc
	inc	sp
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	de
	pop	bc
;src/systems/hud.c:79: if (scorebar) {
	ld	a, c
	or	a, a
	jr	Z,00105$
;src/systems/hud.c:80: cpct_drawSolidBox(pvmem, cpct_px2byteM0(14, 14), scorebar, 2);
	push	bc
	push	de
	ld	hl, #0x0e0e
	push	hl
	call	_cpct_px2byteM0
	ld	h, l
	pop	de
	pop	bc
	ld	b, #0x02
	push	bc
	push	hl
	inc	sp
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00105$:
;src/systems/hud.c:83: timebar = (u8)(currenttime / 5);
	ld	a, #0x05
	push	af
	inc	sp
	ld	a, (_currenttime)
	push	af
	inc	sp
	call	__divuchar
	pop	af
	ld	c, l
;src/systems/hud.c:84: if (timebar > 19) {
	ld	a, #0x13
	sub	a, c
	jr	NC,00107$
;src/systems/hud.c:85: timebar = 19;
	ld	c, #0x13
00107$:
;src/systems/hud.c:87: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, 2);
	push	bc
	ld	hl, #0x0238
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	push	hl
	ld	hl, #0x0101
	push	hl
	call	_cpct_px2byteM0
	ld	b, l
	pop	de
	ld	a, b
	pop	bc
	ld	b, a
;src/systems/hud.c:70: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), 2, 4);
;src/systems/hud.c:88: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 20, 2);
	push	bc
	push	de
	ld	hl, #0x0214
	push	hl
	push	bc
	inc	sp
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	de
	pop	bc
;src/systems/hud.c:89: if (timebar) {
	ld	a, c
	or	a, a
	jr	Z,00109$
;src/systems/hud.c:90: cpct_drawSolidBox(pvmem, cpct_px2byteM0(9, 9), timebar, 2);
	push	bc
	push	de
	ld	hl, #0x0909
	push	hl
	call	_cpct_px2byteM0
	ld	h, l
	pop	de
	pop	bc
	ld	b, #0x02
	push	bc
	push	hl
	inc	sp
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
00109$:
;src/systems/hud.c:93: weaponboxes = currentweapon;
	ld	hl,#_currentweapon + 0
	ld	c, (hl)
;src/systems/hud.c:94: if (weaponboxes > 3) {
	ld	a, #0x03
	sub	a, c
	jr	NC,00131$
;src/systems/hud.c:95: weaponboxes = 3;
	ld	c, #0x03
;src/systems/hud.c:97: for (i = 0; i < weaponboxes; ++i) {
00131$:
	ld	b, #0x00
00118$:
;src/systems/hud.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (u8)(72 + (i * 2)), 6);
	ld	a,b
	cp	a,c
	jr	NC,00120$
	add	a, a
	add	a, #0x48
	ld	d, a
	push	bc
	ld	a, #0x06
	push	af
	inc	sp
	push	de
	inc	sp
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	push	hl
	ld	hl, #0x0b0b
	push	hl
	call	_cpct_px2byteM0
	ld	-1 (ix), l
	pop	de
	ld	hl, #0x0301
	push	hl
	ld	a, -1 (ix)
	push	af
	inc	sp
	push	de
	call	_cpct_drawSolidBox
	pop	af
	pop	af
	inc	sp
	pop	bc
;src/systems/hud.c:97: for (i = 0; i < weaponboxes; ++i) {
	inc	b
	jr	00118$
00120$:
	inc	sp
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
