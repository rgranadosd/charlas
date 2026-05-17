;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module enemy
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _collision_clamp_y_at
	.globl _collision_is_on_ground_at
	.globl _cpct_getScreenPtr
	.globl _cpct_drawSprite
	.globl _enemyinit
	.globl _enemyspawn
	.globl _enemyupdate
	.globl _enemyrender
	.globl _enemydamage
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
;src/entities/enemy.c:65: void enemyinit(Enemy* enemy) {
;	---------------------------------
; Function enemyinit
; ---------------------------------
_enemyinit::
;src/entities/enemy.c:66: if (!enemy) {
	ld	hl, #2+1
	add	hl, sp
	ld	a, (hl)
	dec	hl
	or	a,(hl)
;src/entities/enemy.c:67: return;
	ret	Z
;src/entities/enemy.c:70: enemy->x = 0;
	pop	de
	pop	bc
	push	bc
	push	de
	xor	a, a
	ld	(bc), a
;src/entities/enemy.c:71: enemy->y = 0;
	ld	e, c
	ld	d, b
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:72: enemy->vx = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:73: enemy->vy = 0;
	ld	e, c
	ld	d, b
	inc	de
	inc	de
	inc	de
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:74: enemy->w = 4;
	ld	hl, #0x0004
	add	hl, bc
	ld	(hl), #0x04
;src/entities/enemy.c:75: enemy->h = 16;
	ld	hl, #0x0005
	add	hl, bc
	ld	(hl), #0x10
;src/entities/enemy.c:76: enemy->active = 0;
	ld	hl, #0x0006
	add	hl, bc
	ld	(hl), #0x00
;src/entities/enemy.c:77: enemy->health = 1;
	ld	hl, #0x0007
	add	hl, bc
	ld	(hl), #0x01
;src/entities/enemy.c:78: enemy->reward = 100;
	ld	hl, #0x0008
	add	hl, bc
	ld	(hl), #0x64
;src/entities/enemy.c:79: enemy->kind = 0;
	ld	hl, #0x0009
	add	hl, bc
	ld	(hl), #0x00
	ret
_enemy_kind0_sprite:
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
	.db #0x30	; 48	'0'
_enemy_kind1_sprite:
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x2a	; 42
	.db #0x2a	; 42
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x15	; 21
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
	.db #0x3f	; 63
_enemy_kind2_sprite:
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0a	; 10
	.db #0x05	; 5
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x05	; 5
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
	.db #0x0f	; 15
_enemy_kind3_sprite:
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x11	; 17
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
	.db #0x33	; 51	'3'
;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
;	---------------------------------
; Function enemyspawn
; ---------------------------------
_enemyspawn::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-15
	add	hl, sp
	ld	sp, hl
;src/entities/enemy.c:83: if (!enemy) {
	ld	a, 5 (ix)
	or	a,4 (ix)
;src/entities/enemy.c:84: return;
	jp	Z,00112$
;src/entities/enemy.c:87: enemy->x = x;
	ld	a, 4 (ix)
	ld	-2 (ix), a
	ld	a, 5 (ix)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	a, 6 (ix)
	ld	(hl), a
;src/entities/enemy.c:88: enemy->y = y;
	ld	c,-2 (ix)
	ld	b,-1 (ix)
	inc	bc
	ld	a, 7 (ix)
	ld	(bc), a
;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
	ld	a, -2 (ix)
	add	a, #0x02
	ld	-4 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-3 (ix), a
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00114$
	ld	c, #0x01
	jr	00115$
00114$:
	ld	c, #0xff
00115$:
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), c
;src/entities/enemy.c:90: enemy->vy = 0;
	ld	a, -2 (ix)
	add	a, #0x03
	ld	-6 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-5 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	(hl), #0x00
;src/entities/enemy.c:91: enemy->active = 1;
	ld	a, -2 (ix)
	add	a, #0x06
	ld	-8 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x01
;src/entities/enemy.c:92: enemy->kind = kind;
	ld	a, -2 (ix)
	add	a, #0x09
	ld	-8 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, 8 (ix)
	ld	(hl), a
;src/entities/enemy.c:95: enemy->w = 5;
	ld	a, -2 (ix)
	add	a, #0x04
	ld	-8 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
;src/entities/enemy.c:96: enemy->h = 14;
	ld	a, -2 (ix)
	add	a, #0x05
	ld	-10 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-9 (ix), a
;src/entities/enemy.c:97: enemy->health = 2;
	ld	a, -2 (ix)
	add	a, #0x07
	ld	-12 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-11 (ix), a
;src/entities/enemy.c:98: enemy->reward = 180;
	ld	a, -2 (ix)
	add	a, #0x08
	ld	-2 (ix), a
	ld	a, -1 (ix)
	adc	a, #0x00
	ld	-1 (ix), a
;src/entities/enemy.c:94: if (kind == 1) {
	ld	a, 8 (ix)
	dec	a
	jr	NZ,00110$
;src/entities/enemy.c:95: enemy->w = 5;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x05
;src/entities/enemy.c:96: enemy->h = 14;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), #0x0e
;src/entities/enemy.c:97: enemy->health = 2;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x02
;src/entities/enemy.c:98: enemy->reward = 180;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0xb4
;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
	ld	a, -4 (ix)
	ld	-14 (ix), a
	ld	a, -3 (ix)
	ld	-13 (ix), a
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00116$
	ld	-15 (ix), #0x02
	jr	00117$
00116$:
	ld	-15 (ix), #0xfe
00117$:
	ld	l,-14 (ix)
	ld	h,-13 (ix)
	ld	a, -15 (ix)
	ld	(hl), a
	jp	00112$
00110$:
;src/entities/enemy.c:100: } else if (kind == 2) {
	ld	a, 8 (ix)
	sub	a, #0x02
	jr	NZ,00107$
;src/entities/enemy.c:101: enemy->w = 6;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x06
;src/entities/enemy.c:102: enemy->h = 10;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), #0x0a
;src/entities/enemy.c:103: enemy->health = 1;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x01
;src/entities/enemy.c:104: enemy->reward = 150;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x96
;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
	ld	c,-6 (ix)
	ld	b,-5 (ix)
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00118$
	ld	a, #0x01
	jr	00119$
00118$:
	ld	a, #0xff
00119$:
	ld	(bc), a
;src/entities/enemy.c:106: enemy->vx = 1;
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	ld	(hl), #0x01
	jr	00112$
00107$:
;src/entities/enemy.c:107: } else if (kind == 3) {
	ld	a, 8 (ix)
	sub	a, #0x03
	jr	NZ,00104$
;src/entities/enemy.c:108: enemy->w = 10;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x0a
;src/entities/enemy.c:109: enemy->h = 18;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), #0x12
;src/entities/enemy.c:110: enemy->health = 8;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x08
;src/entities/enemy.c:111: enemy->reward = 800;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x20
;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
	ld	c,-4 (ix)
	ld	b,-3 (ix)
	ld	a, 9 (ix)
	or	a, a
	jr	Z,00120$
	ld	a, #0x01
	jr	00121$
00120$:
	ld	a, #0xff
00121$:
	ld	(bc), a
	jr	00112$
00104$:
;src/entities/enemy.c:114: enemy->w = 4;
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	(hl), #0x04
;src/entities/enemy.c:115: enemy->h = 16;
	ld	l,-10 (ix)
	ld	h,-9 (ix)
	ld	(hl), #0x10
;src/entities/enemy.c:116: enemy->health = 1;
	ld	l,-12 (ix)
	ld	h,-11 (ix)
	ld	(hl), #0x01
;src/entities/enemy.c:117: enemy->reward = 100;
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	(hl), #0x64
00112$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
;	---------------------------------
; Function enemyupdate
; ---------------------------------
_enemyupdate::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-10
	add	hl, sp
	ld	sp, hl
;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jp	Z,00121$
	ld	a, 4 (ix)
	ld	-10 (ix), a
	ld	a, 5 (ix)
	ld	-9 (ix), a
	pop	hl
	push	hl
	ld	de, #0x0006
	add	hl, de
	ld	a, (hl)
	or	a, a
;src/entities/enemy.c:126: return;
	jp	Z,00121$
;src/entities/enemy.c:129: if (enemy->kind == 2) {
	pop	hl
	push	hl
	ld	de, #0x0009
	add	hl, de
	ld	a, (hl)
	ld	-1 (ix), a
;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
	pop	hl
	push	hl
	ld	c, (hl)
	ld	a, -10 (ix)
	add	a, #0x02
	ld	-3 (ix), a
	ld	a, -9 (ix)
	adc	a, #0x00
	ld	-2 (ix), a
;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	a, -10 (ix)
	add	a, #0x01
	ld	-5 (ix), a
	ld	a, -9 (ix)
	adc	a, #0x00
	ld	-4 (ix), a
	pop	de
	push	de
	inc	de
	inc	de
	inc	de
;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
	ld	b, #0x00
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	a, (hl)
	ld	-6 (ix), a
	ld	l, a
	ld	a, -6 (ix)
	rla
	sbc	a, a
	ld	h, a
	add	hl,bc
	ld	c, l
	ld	b, h
;src/entities/enemy.c:129: if (enemy->kind == 2) {
	ld	a, -1 (ix)
	sub	a, #0x02
	jp	NZ,00111$
;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	l, (hl)
	ld	-8 (ix), l
	ld	-7 (ix), #0x00
	ld	a, (de)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	ld	a, -8 (ix)
	add	a, l
	ld	-8 (ix), a
	ld	a, -7 (ix)
	adc	a, h
	ld	-7 (ix), a
;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
	ld	a, c
	sub	a, #0x08
	ld	a, b
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	C,00104$
	ld	a, #0x48
	cp	a, c
	ld	a, #0x00
	sbc	a, b
	jp	PO, 00161$
	xor	a, #0x80
00161$:
	jp	P, 00105$
00104$:
;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
	xor	a, a
	sub	a, -6 (ix)
	ld	c, a
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), c
;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
	pop	hl
	push	hl
	ld	l, (hl)
	ld	h, #0x00
	ld	a, c
	rla
	sbc	a, a
	ld	b, a
	add	hl,bc
	ld	c, l
00105$:
;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
	ld	a, -8 (ix)
	sub	a, #0x38
	ld	a, -7 (ix)
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	C,00107$
	ld	a, #0x78
	cp	a, -8 (ix)
	ld	a, #0x00
	sbc	a, -7 (ix)
	jp	PO, 00162$
	xor	a, #0x80
00162$:
	jp	P, 00108$
00107$:
;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
	ld	a, (de)
	ld	l, a
	xor	a, a
	sub	a, l
	ld	-6 (ix), a
	ld	(de),a
;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	e, (hl)
	ld	d, #0x00
	ld	l, -6 (ix)
	ld	a, -6 (ix)
	rla
	sbc	a, a
	ld	h, a
	add	hl,de
	ld	-8 (ix), l
	ld	-7 (ix), h
00108$:
;src/entities/enemy.c:142: enemy->x = (u8)nextx;
	pop	hl
	push	hl
	ld	(hl), c
;src/entities/enemy.c:143: enemy->y = (u8)nexty;
	ld	c, -8 (ix)
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	(hl), c
;src/entities/enemy.c:144: return;
	jp	00121$
00111$:
;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
;src/entities/enemy.c:148: if (nextx < 2) {
	ld	a, c
	sub	a, #0x02
	ld	a, b
	rla
	ccf
	rra
	sbc	a, #0x80
	jr	NC,00113$
;src/entities/enemy.c:149: nextx = 2;
	ld	bc, #0x0002
;src/entities/enemy.c:150: enemy->vx = 1;
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), #0x01
00113$:
;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
	pop	hl
	push	hl
	inc	hl
	inc	hl
	inc	hl
	inc	hl
	ld	l, (hl)
	ld	h, #0x00
	ld	a, #0x50
	sub	a, l
	ld	l, a
	ld	a, #0x00
	sbc	a, h
	ld	h, a
;src/entities/enemy.c:154: if (nextx > maxx) {
	ld	a, l
	sub	a, c
	ld	a, h
	sbc	a, b
	jp	PO, 00163$
	xor	a, #0x80
00163$:
	jp	P, 00115$
;src/entities/enemy.c:155: nextx = maxx;
	ld	c, l
;src/entities/enemy.c:156: enemy->vx = -1;
	ld	l,-3 (ix)
	ld	h,-2 (ix)
	ld	(hl), #0xff
00115$:
;src/entities/enemy.c:159: enemy->x = (u8)nextx;
	pop	hl
	push	hl
	ld	(hl), c
;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
	ld	a, (de)
	ld	c, a
	inc	c
	ld	a, c
	ld	(de), a
;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
	ld	a, #0x03
	sub	a, c
	jp	PO, 00164$
	xor	a, #0x80
00164$:
	jp	P, 00117$
	ld	a, #0x03
	ld	(de), a
00117$:
;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	c, (hl)
	ld	b, #0x00
	ld	a, (de)
	ld	l, a
	rla
	sbc	a, a
	ld	h, a
	add	hl, bc
	push	hl
	pop	iy
;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
	ld	a, -10 (ix)
	add	a, #0x05
	ld	-8 (ix), a
	ld	a, -9 (ix)
	adc	a, #0x00
	ld	-7 (ix), a
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	pop	hl
	push	hl
	ld	c, (hl)
	ld	b, #0x00
	push	de
	push	af
	inc	sp
	push	iy
	push	bc
	call	_collision_clamp_y_at
	pop	af
	pop	af
	inc	sp
	ld	c, l
	pop	de
;src/entities/enemy.c:165: enemy->y = (u8)nexty;
	ld	l,-5 (ix)
	ld	h,-4 (ix)
	ld	(hl), c
;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	ld	a, (hl)
	ld	b, #0x00
	pop	hl
	push	hl
	ld	l, (hl)
	ld	-8 (ix), l
	ld	-7 (ix), #0x00
	push	de
	push	af
	inc	sp
	push	bc
	ld	l,-8 (ix)
	ld	h,-7 (ix)
	push	hl
	call	_collision_is_on_ground_at
	pop	af
	pop	af
	inc	sp
	pop	de
	ld	a, l
	or	a, a
	jr	Z,00121$
	ld	a, (de)
	ld	c, a
	xor	a, a
	sub	a, c
	jp	PO, 00165$
	xor	a, #0x80
00165$:
	jp	P, 00121$
;src/entities/enemy.c:167: enemy->vy = 0;
	xor	a, a
	ld	(de), a
00121$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
;	---------------------------------
; Function enemyrender
; ---------------------------------
_enemyrender::
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	dec	sp
;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jp	Z,00113$
	ld	c,4 (ix)
	ld	b,5 (ix)
	push	bc
	pop	iy
	ld	a, 6 (iy)
	or	a, a
;src/entities/enemy.c:176: return;
	jr	Z,00113$
;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
	push	bc
	pop	iy
	ld	a, 9 (iy)
	cp	a, #0x03
	jr	NZ,00111$
	ld	-2 (ix), #<(_enemy_kind3_sprite)
	ld	-1 (ix), #>(_enemy_kind3_sprite)
	jr	00112$
00111$:
;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
	cp	a, #0x02
	jr	NZ,00108$
	ld	-2 (ix), #<(_enemy_kind2_sprite)
	ld	-1 (ix), #>(_enemy_kind2_sprite)
	jr	00112$
00108$:
;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
	dec	a
	jr	NZ,00105$
	ld	-2 (ix), #<(_enemy_kind1_sprite)
	ld	-1 (ix), #>(_enemy_kind1_sprite)
	jr	00112$
00105$:
;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
	ld	-2 (ix), #<(_enemy_kind0_sprite)
	ld	-1 (ix), #>(_enemy_kind0_sprite)
00112$:
;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
	ld	l, c
	ld	h, b
	inc	hl
	ld	d, (hl)
	ld	a, (bc)
	push	bc
	ld	e, a
	push	de
	ld	hl, #0xc000
	push	hl
	call	_cpct_getScreenPtr
	ex	de,hl
	pop	bc
;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
	push	bc
	pop	iy
	ld	a, 5 (iy)
	ld	-3 (ix), a
	ld	l, c
	ld	h, b
	ld	bc, #0x0004
	add	hl, bc
	ld	c, (hl)
	push	de
	pop	iy
	ld	e,-2 (ix)
	ld	d,-1 (ix)
	ld	b, -3 (ix)
	push	bc
	push	iy
	push	de
	call	_cpct_drawSprite
00113$:
	ld	sp, ix
	pop	ix
	ret
;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
;	---------------------------------
; Function enemydamage
; ---------------------------------
_enemydamage::
	push	ix
	ld	ix,#0
	add	ix,sp
;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
	ld	a, 5 (ix)
	or	a,4 (ix)
	jr	Z,00101$
	ld	c,4 (ix)
	ld	b,5 (ix)
	ld	hl, #0x0006
	add	hl,bc
	ex	de,hl
	ld	a, (de)
	or	a, a
	jr	NZ,00102$
00101$:
;src/entities/enemy.c:190: return 0;
	ld	l, #0x00
	jr	00106$
00102$:
;src/entities/enemy.c:193: if (damage >= enemy->health) {
	ld	hl, #0x0007
	add	hl, bc
	ld	c, (hl)
	ld	a, 6 (ix)
	sub	a, c
	jr	C,00105$
;src/entities/enemy.c:194: enemy->health = 0;
	ld	(hl), #0x00
;src/entities/enemy.c:195: enemy->active = 0;
	xor	a, a
	ld	(de), a
;src/entities/enemy.c:196: return 1;
	ld	l, #0x01
	jr	00106$
00105$:
;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
	ld	a, c
	sub	a, 6 (ix)
	ld	(hl), a
;src/entities/enemy.c:200: return 0;
	ld	l, #0x00
00106$:
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
