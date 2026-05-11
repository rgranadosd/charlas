;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module collision
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _collision_check_player_tilemap
	.globl _collision_check_enemy_tilemap
	.globl _collision_check_projectile_tilemap
	.globl _collision_check_player_enemy
	.globl _collision_check_projectile_enemy
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
;src/systems/collision.c:9: static u8 check_tile_collision(u8 x, u8 y, u8 width, u8 height) {
;	---------------------------------
; Function check_tile_collision
; ---------------------------------
_check_tile_collision:
	push	ix
	ld	ix,#0
	add	ix,sp
	push	af
	push	af
;src/systems/collision.c:10: u8 tile_x1 = x >> 3;
	ld	a, 4 (ix)
	rrca
	rrca
	rrca
	and	a, #0x1f
	ld	-1 (ix), a
;src/systems/collision.c:11: u8 tile_y1 = y >> 3;
	ld	a, 5 (ix)
	rrca
	rrca
	rrca
	and	a, #0x1f
	ld	-4 (ix), a
;src/systems/collision.c:12: u8 tile_x2 = (x + width - 1) >> 3;
	ld	c, 4 (ix)
	ld	b, #0x00
	ld	l, 6 (ix)
	ld	h, #0x00
	add	hl, bc
	dec	hl
	sra	h
	rr	l
	sra	h
	rr	l
	sra	h
	rr	l
	ld	-2 (ix), l
;src/systems/collision.c:13: u8 tile_y2 = (y + height - 1) >> 3;
	ld	c, 5 (ix)
	ld	b, #0x00
	ld	l, 7 (ix)
	ld	h, #0x00
	add	hl, bc
	dec	hl
	sra	h
	rr	l
	sra	h
	rr	l
	sra	h
	rr	l
	ld	-3 (ix), l
;src/systems/collision.c:15: for (u8 ty = tile_y1; ty <= tile_y2; ty++) {
00112$:
	ld	a, -3 (ix)
	sub	a, -4 (ix)
	jr	C,00107$
;src/systems/collision.c:16: for (u8 tx = tile_x1; tx <= tile_x2; tx++) {
	ld	c, -1 (ix)
00109$:
	ld	a, -2 (ix)
	sub	a, c
	jr	C,00113$
;src/systems/collision.c:17: if (ty < level1_tilemap_height && tx < level1_tilemap_width) {
	ld	hl,#_level1_tilemap_height + 0
	ld	a,-4 (ix)
	sub	a,(hl)
	jr	NC,00110$
	ld	hl,#_level1_tilemap_width + 0
	ld	e, (hl)
	ld	a, c
	sub	a, e
	jr	NC,00110$
;src/systems/collision.c:18: u8 tile = level1_collision_map[ty * level1_tilemap_width + tx];
	ld	h, -4 (ix)
	ld	l, #0x00
	ld	d, l
	ld	b, #0x08
00144$:
	add	hl, hl
	jr	NC,00145$
	add	hl, de
00145$:
	djnz	00144$
	ld	e, c
	ld	d, #0x00
	add	hl, de
	ld	de, (_level1_collision_map)
	add	hl, de
	ld	a, (hl)
;src/systems/collision.c:19: if (tile) return 1;
	or	a, a
	jr	Z,00110$
	ld	l, #0x01
	jr	00114$
00110$:
;src/systems/collision.c:16: for (u8 tx = tile_x1; tx <= tile_x2; tx++) {
	inc	c
	jr	00109$
00113$:
;src/systems/collision.c:15: for (u8 ty = tile_y1; ty <= tile_y2; ty++) {
	inc	-4 (ix)
	jr	00112$
00107$:
;src/systems/collision.c:23: return 0;
	ld	l, #0x00
00114$:
	ld	sp, ix
	pop	ix
	ret
;src/systems/collision.c:26: u8 collision_check_player_tilemap(u8 x, u8 y, u8 width, u8 height) {
;	---------------------------------
; Function collision_check_player_tilemap
; ---------------------------------
_collision_check_player_tilemap::
;src/systems/collision.c:27: return check_tile_collision(x, y, width, height);
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	call	_check_tile_collision
	pop	af
	pop	af
	ret
;src/systems/collision.c:30: u8 collision_check_enemy_tilemap(u8 x, u8 y, u8 width, u8 height) {
;	---------------------------------
; Function collision_check_enemy_tilemap
; ---------------------------------
_collision_check_enemy_tilemap::
;src/systems/collision.c:31: return check_tile_collision(x, y, width, height);
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	call	_check_tile_collision
	pop	af
	pop	af
	ret
;src/systems/collision.c:34: u8 collision_check_projectile_tilemap(u8 x, u8 y, u8 width, u8 height) {
;	---------------------------------
; Function collision_check_projectile_tilemap
; ---------------------------------
_collision_check_projectile_tilemap::
;src/systems/collision.c:35: return check_tile_collision(x, y, width, height);
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	ld	hl, #5+0
	add	hl, sp
	ld	a, (hl)
	push	af
	inc	sp
	call	_check_tile_collision
	pop	af
	pop	af
	ret
;src/systems/collision.c:38: u8 collision_check_player_enemy(Enemy* enemy) {
;	---------------------------------
; Function collision_check_player_enemy
; ---------------------------------
_collision_check_player_enemy::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-6
	add	hl, sp
	ld	sp, hl
;src/systems/collision.c:39: return (player.x < enemy->x + enemy->width &&
	ld	hl, #_player + 0
	ld	c, (hl)
	ld	a, 4 (ix)
	ld	-2 (ix), a
	ld	a, 5 (ix)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	b, (hl)
	ld	-4 (ix), b
	ld	-3 (ix), #0x00
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	inc	hl
	inc	hl
	ld	e, (hl)
	ld	d, #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	add	hl, de
	ld	-6 (ix), c
	ld	-5 (ix), #0x00
	ld	a, -6 (ix)
	sub	a, l
	ld	a, -5 (ix)
	sbc	a, h
	jp	PO, 00122$
	xor	a, #0x80
00122$:
	jp	P, 00103$
;src/systems/collision.c:40: player.x + player.width > enemy->x &&
	ld	hl, #_player + 2
	ld	c, (hl)
	ld	b, #0x00
	pop	hl
	push	hl
	add	hl, bc
	ld	a, -4 (ix)
	sub	a, l
	ld	a, -3 (ix)
	sbc	a, h
	jp	PO, 00123$
	xor	a, #0x80
00123$:
	jp	P, 00103$
;src/systems/collision.c:41: player.y < enemy->y + enemy->height &&
	ld	a,(#_player + 1)
	ld	-6 (ix), a
	ld	a, -2 (ix)
	ld	-4 (ix), a
	ld	a, -1 (ix)
	ld	-3 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	inc	hl
	ld	a, (hl)
	ld	-4 (ix), a
	ld	-4 (ix), a
	ld	-3 (ix), #0x00
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	-2 (ix), a
	ld	-2 (ix), a
	ld	-1 (ix), #0x00
	ld	a, -4 (ix)
	add	a, -2 (ix)
	ld	-2 (ix), a
	ld	a, -3 (ix)
	adc	a, -1 (ix)
	ld	-1 (ix), a
	ld	a, -6 (ix)
	ld	-6 (ix), a
	ld	-5 (ix), #0x00
	ld	a, -6 (ix)
	sub	a, -2 (ix)
	ld	a, -5 (ix)
	sbc	a, -1 (ix)
	jp	PO, 00124$
	xor	a, #0x80
00124$:
	jp	P, 00103$
;src/systems/collision.c:42: player.y + player.height > enemy->y);
	ld	a,(#_player + 3)
	ld	-2 (ix), a
	ld	-2 (ix), a
	ld	-1 (ix), #0x00
	ld	a, -6 (ix)
	add	a, -2 (ix)
	ld	-6 (ix), a
	ld	a, -5 (ix)
	adc	a, -1 (ix)
	ld	-5 (ix), a
	ld	a, -4 (ix)
	sub	a, -6 (ix)
	ld	a, -3 (ix)
	sbc	a, -5 (ix)
	jp	PO, 00125$
	xor	a, #0x80
00125$:
	jp	M, 00104$
00103$:
	ld	l, #0x00
	jr	00105$
00104$:
	ld	l, #0x01
00105$:
	ld	sp, ix
	pop	ix
	ret
;src/systems/collision.c:45: u8 collision_check_projectile_enemy(Projectile* projectile, Enemy* enemy) {
;	---------------------------------
; Function collision_check_projectile_enemy
; ---------------------------------
_collision_check_projectile_enemy::
	push	ix
	ld	ix,#0
	add	ix,sp
	ld	hl, #-8
	add	hl, sp
	ld	sp, hl
;src/systems/collision.c:46: return (projectile->x < enemy->x + enemy->width &&
	ld	a, 4 (ix)
	ld	-2 (ix), a
	ld	a, 5 (ix)
	ld	-1 (ix), a
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	c, (hl)
	ld	a, 6 (ix)
	ld	-6 (ix), a
	ld	a, 7 (ix)
	ld	-5 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	b, (hl)
	ld	-8 (ix), b
	ld	-7 (ix), #0x00
	pop	de
	pop	hl
	push	hl
	push	de
	inc	hl
	inc	hl
	ld	e, (hl)
	ld	d, #0x00
	pop	hl
	push	hl
	add	hl, de
	ld	-4 (ix), c
	ld	-3 (ix), #0x00
	ld	a, -4 (ix)
	sub	a, l
	ld	a, -3 (ix)
	sbc	a, h
	jp	PO, 00122$
	xor	a, #0x80
00122$:
	jp	P, 00103$
;src/systems/collision.c:47: projectile->x + projectile->width > enemy->x &&
	ld	l,-2 (ix)
	ld	h,-1 (ix)
	ld	de, #0x0004
	add	hl, de
	ld	c, (hl)
	ld	b, #0x00
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	add	hl, bc
	ld	a, -8 (ix)
	sub	a, l
	ld	a, -7 (ix)
	sbc	a, h
	jp	PO, 00123$
	xor	a, #0x80
00123$:
	jp	P, 00103$
;src/systems/collision.c:48: projectile->y < enemy->y + enemy->height &&
	ld	a, -2 (ix)
	ld	-4 (ix), a
	ld	a, -1 (ix)
	ld	-3 (ix), a
	ld	l,-4 (ix)
	ld	h,-3 (ix)
	inc	hl
	ld	a, (hl)
	ld	-4 (ix), a
	ld	a, -6 (ix)
	ld	-8 (ix), a
	ld	a, -5 (ix)
	ld	-7 (ix), a
	pop	hl
	push	hl
	inc	hl
	ld	a, (hl)
	ld	-8 (ix), a
	ld	-8 (ix), a
	ld	-7 (ix), #0x00
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	inc	hl
	inc	hl
	inc	hl
	ld	a, (hl)
	ld	-6 (ix), a
	ld	-6 (ix), a
	ld	-5 (ix), #0x00
	ld	a, -8 (ix)
	add	a, -6 (ix)
	ld	-6 (ix), a
	ld	a, -7 (ix)
	adc	a, -5 (ix)
	ld	-5 (ix), a
	ld	a, -4 (ix)
	ld	-4 (ix), a
	ld	-3 (ix), #0x00
	ld	a, -4 (ix)
	sub	a, -6 (ix)
	ld	a, -3 (ix)
	sbc	a, -5 (ix)
	jp	PO, 00124$
	xor	a, #0x80
00124$:
	jp	P, 00103$
;src/systems/collision.c:49: projectile->y + projectile->height > enemy->y);
	ld	a, -2 (ix)
	ld	-6 (ix), a
	ld	a, -1 (ix)
	ld	-5 (ix), a
	ld	l,-6 (ix)
	ld	h,-5 (ix)
	ld	de, #0x0005
	add	hl, de
	ld	a, (hl)
	ld	-6 (ix), a
	ld	-6 (ix), a
	ld	-5 (ix), #0x00
	ld	a, -4 (ix)
	add	a, -6 (ix)
	ld	-4 (ix), a
	ld	a, -3 (ix)
	adc	a, -5 (ix)
	ld	-3 (ix), a
	ld	a, -8 (ix)
	sub	a, -4 (ix)
	ld	a, -7 (ix)
	sbc	a, -3 (ix)
	jp	PO, 00125$
	xor	a, #0x80
00125$:
	jp	M, 00104$
00103$:
	ld	-4 (ix), #0x00
	jr	00105$
00104$:
	ld	-4 (ix), #0x01
00105$:
	ld	l, -4 (ix)
	ld	sp, ix
	pop	ix
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
