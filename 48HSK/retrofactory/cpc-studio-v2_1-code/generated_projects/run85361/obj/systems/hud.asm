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
_hudnumbers:
	.ds 20
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
;src/systems/hud.c:18: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
;	---------------------------------
; Function hud_draw_digits
; ---------------------------------
_hud_draw_digits:
	push	ix
	ld	ix,#0
	add	ix,sp
	dec	sp
;src/systems/hud.c:24: divisor = 1;
	ld	bc, #0x0001
;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
	ld	e, #0x01
00106$:
	ld	a, e
	sub	a, 6 (ix)
	jr	NC,00101$
;src/systems/hud.c:26: divisor *= 10;
	ld	l, c
	ld	h, b
	add	hl, hl
	add	hl, hl
	add	hl, bc
	add	hl, hl
	ld	c, l
	ld	b, h
;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
	inc	e
	jr	00106$
00101$:
;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
	ld	-1 (ix), #0x00
00109$:
	ld	a, -1 (ix)
	sub	a, 6 (ix)
	jr	NC,00111$
;src/systems/hud.c:30: digit = (u8)(value / divisor);
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
;src/systems/hud.c:31: value = (u16)(value % divisor);
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
;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
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
;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
	push	hl
	pop	iy
	ld	h, #0x00
	ld	l, e
	add	hl, hl
	ld	de, #_hudnumbers
	add	hl, de
	ld	e, (hl)
	inc	hl
	ld	d, (hl)
	push	bc
	ld	hl, #0x0808
	push	hl
	push	iy
	push	de
	call	_cpct_drawSprite
	pop	bc
;src/systems/hud.c:36: if (divisor > 1) {
	ld	a, #0x01
	cp	a, c
	ld	a, #0x00
	sbc	a, b
	jr	NC,00110$
;src/systems/hud.c:37: divisor /= 10;
	ld	hl, #0x000a
	push	hl
	push	bc
	call	__divuint
	pop	af
	pop	af
	ld	c, l
	ld	b, h
00110$:
;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
	inc	-1 (ix)
	jp	00109$
00111$:
	inc	sp
	pop	ix
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
;src/systems/hud.c:42: void hudinit(void) {
;	---------------------------------
; Function hudinit
; ---------------------------------
_hudinit::
;src/systems/hud.c:43: currenthealth = 3;
	ld	hl,#_currenthealth + 0
	ld	(hl), #0x03
;src/systems/hud.c:44: currentscore  = 0;
	ld	hl, #0x0000
	ld	(_currentscore), hl
;src/systems/hud.c:45: currenttime   = 90;
	ld	hl,#_currenttime + 0
	ld	(hl), #0x5a
;src/systems/hud.c:46: currentlives  = 3;
	ld	hl,#_currentlives + 0
	ld	(hl), #0x03
;src/systems/hud.c:47: currentweapon = 0;
	ld	hl,#_currentweapon + 0
	ld	(hl), #0x00
	ret
;src/systems/hud.c:50: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
;	---------------------------------
; Function hudupdate
; ---------------------------------
_hudupdate::
;src/systems/hud.c:51: currenthealth = lives;
	ld	hl, #2+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currenthealth + 0),a
;src/systems/hud.c:52: currentscore  = score;
	ld	hl, #3+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentscore + 0),a
	ld	hl, #3+1
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentscore + 1),a
;src/systems/hud.c:53: currenttime   = time;
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currenttime + 0),a
;src/systems/hud.c:54: currentlives  = lives;
	ld	hl, #2+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentlives + 0),a
;src/systems/hud.c:55: currentweapon = weapon;
	ld	hl, #6+0
	add	hl, sp
	ld	a, (hl)
	ld	(#_currentweapon + 0),a
	ret
;src/systems/hud.c:58: void hudrender(void) {
;	---------------------------------
; Function hudrender
; ---------------------------------
_hudrender::
;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
	ld	c, #0x00
00103$:
	ld	hl, #_currenthealth
;src/systems/hud.c:65: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);
	ld	a,c
	cp	a,(hl)
	jr	NC,00101$
	rlca
	rlca
	rlca
	and	a, #0xf8
	ld	b, a
	inc	b
	inc	b
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
;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
	inc	c
	jr	00103$
00101$:
;src/systems/hud.c:69: scoretemp = currentscore;
	ld	hl, (_currentscore)
;src/systems/hud.c:70: hud_draw_digits(scoretemp, 5, 88, 2);
	ld	bc, #0x0258
	push	bc
	ld	a, #0x05
	push	af
	inc	sp
	push	hl
	call	_hud_draw_digits
	pop	af
	pop	af
	inc	sp
;src/systems/hud.c:72: timetemp = currenttime;
	ld	hl,#_currenttime + 0
	ld	c, (hl)
;src/systems/hud.c:73: hud_draw_digits((u16)timetemp, 3, 56, 2);
	ld	b, #0x00
	ld	hl, #0x0238
	push	hl
	ld	a, #0x03
	push	af
	inc	sp
	push	bc
	call	_hud_draw_digits
	pop	af
;src/systems/hud.c:75: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
	inc	sp
	ld	hl,#0xb402
	ex	(sp),hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/hud.c:76: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
	ld	bc, #_hudlives+0
	ld	de, #0x0808
	push	de
	push	hl
	push	bc
	call	_cpct_drawSprite
;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
	ld	hl, #0xb40c
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/hud.c:79: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
	push	hl
	ld	a, #0x0a
	push	af
	inc	sp
	ld	a, (_currentlives)
	push	af
	inc	sp
	call	__moduchar
	pop	af
	pop	bc
	ld	h, #0x00
	add	hl, hl
	ld	de, #_hudnumbers
	add	hl, de
	ld	e, (hl)
	inc	hl
	ld	d, (hl)
	ld	hl, #0x0808
	push	hl
	push	bc
	push	de
	call	_cpct_drawSprite
;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
	ld	hl, #0xb446
	push	hl
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
;src/systems/hud.c:82: cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);
	push	hl
	ld	a, #0x0a
	push	af
	inc	sp
	ld	a, (_currentweapon)
	push	af
	inc	sp
	call	__moduchar
	pop	af
	pop	bc
	ld	h, #0x00
	add	hl, hl
	ld	de, #_hudnumbers
	add	hl, de
	ld	e, (hl)
	inc	hl
	ld	d, (hl)
	ld	hl, #0x0808
	push	hl
	push	bc
	push	de
	call	_cpct_drawSprite
	ret
	.area _CODE
	.area _INITIALIZER
__xinit__hudnumbers:
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.dw __hud_dummy_sprite
	.area _CABS (ABS)
