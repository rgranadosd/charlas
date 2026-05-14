                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module player
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _collision_clamp_y_to_ground
                             12 	.globl _collision_is_on_ground
                             13 	.globl _input_is_jump_pressed
                             14 	.globl _input_is_right_pressed
                             15 	.globl _input_is_left_pressed
                             16 	.globl _cpct_getScreenPtr
                             17 	.globl _cpct_drawSolidBox
                             18 	.globl _playerinit
                             19 	.globl _playerupdate
                             20 	.globl _playerrender
                             21 ;--------------------------------------------------------
                             22 ; special function registers
                             23 ;--------------------------------------------------------
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _DATA
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _INITIALIZED
                             32 ;--------------------------------------------------------
                             33 ; absolute external ram data
                             34 ;--------------------------------------------------------
                             35 	.area _DABS (ABS)
                             36 ;--------------------------------------------------------
                             37 ; global & static initialisations
                             38 ;--------------------------------------------------------
                             39 	.area _HOME
                             40 	.area _GSINIT
                             41 	.area _GSFINAL
                             42 	.area _GSINIT
                             43 ;--------------------------------------------------------
                             44 ; Home
                             45 ;--------------------------------------------------------
                             46 	.area _HOME
                             47 	.area _HOME
                             48 ;--------------------------------------------------------
                             49 ; code
                             50 ;--------------------------------------------------------
                             51 	.area _CODE
                             52 ;src/entities/player.c:10: void playerinit(Player* player) {
                             53 ;	---------------------------------
                             54 ; Function playerinit
                             55 ; ---------------------------------
   447F                      56 _playerinit::
                             57 ;src/entities/player.c:11: if (!player) {
   447F 21 03 00      [10]   58 	ld	hl, #2+1
   4482 39            [11]   59 	add	hl, sp
   4483 7E            [ 7]   60 	ld	a, (hl)
   4484 2B            [ 6]   61 	dec	hl
   4485 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/player.c:12: return;
   4486 C8            [11]   64 	ret	Z
                             65 ;src/entities/player.c:15: player->x = 20;
   4487 D1            [10]   66 	pop	de
   4488 C1            [10]   67 	pop	bc
   4489 C5            [11]   68 	push	bc
   448A D5            [11]   69 	push	de
   448B 3E 14         [ 7]   70 	ld	a, #0x14
   448D 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/player.c:16: player->y = 120;
   448E 69            [ 4]   73 	ld	l, c
   448F 60            [ 4]   74 	ld	h, b
   4490 23            [ 6]   75 	inc	hl
   4491 36 78         [10]   76 	ld	(hl), #0x78
                             77 ;src/entities/player.c:17: player->vx = 0;
   4493 59            [ 4]   78 	ld	e, c
   4494 50            [ 4]   79 	ld	d, b
   4495 13            [ 6]   80 	inc	de
   4496 13            [ 6]   81 	inc	de
   4497 AF            [ 4]   82 	xor	a, a
   4498 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/player.c:18: player->vy = 0;
   4499 59            [ 4]   85 	ld	e, c
   449A 50            [ 4]   86 	ld	d, b
   449B 13            [ 6]   87 	inc	de
   449C 13            [ 6]   88 	inc	de
   449D 13            [ 6]   89 	inc	de
   449E AF            [ 4]   90 	xor	a, a
   449F 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/player.c:19: player->w = 4;
   44A0 21 04 00      [10]   93 	ld	hl, #0x0004
   44A3 09            [11]   94 	add	hl, bc
   44A4 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/player.c:20: player->h = 16;
   44A6 21 05 00      [10]   97 	ld	hl, #0x0005
   44A9 09            [11]   98 	add	hl, bc
   44AA 36 10         [10]   99 	ld	(hl), #0x10
   44AC C9            [10]  100 	ret
   44AD                     101 _kplayermovespeed:
   44AD 02                  102 	.db #0x02	;  2
   44AE                     103 _kplayergravity:
   44AE 01                  104 	.db #0x01	;  1
   44AF                     105 _kplayerjumpvelocity:
   44AF FB                  106 	.db #0xfb	; -5
                            107 ;src/entities/player.c:23: void playerupdate(Player* player) {
                            108 ;	---------------------------------
                            109 ; Function playerupdate
                            110 ; ---------------------------------
   44B0                     111 _playerupdate::
   44B0 DD E5         [15]  112 	push	ix
   44B2 DD 21 00 00   [14]  113 	ld	ix,#0
   44B6 DD 39         [15]  114 	add	ix,sp
   44B8 21 F8 FF      [10]  115 	ld	hl, #-8
   44BB 39            [11]  116 	add	hl, sp
   44BC F9            [ 6]  117 	ld	sp, hl
                            118 ;src/entities/player.c:27: if (!player) {
   44BD DD 7E 05      [19]  119 	ld	a, 5 (ix)
   44C0 DD B6 04      [19]  120 	or	a,4 (ix)
                            121 ;src/entities/player.c:28: return;
   44C3 CA ED 45      [10]  122 	jp	Z,00120$
                            123 ;src/entities/player.c:31: player->vx = 0;
   44C6 DD 7E 04      [19]  124 	ld	a, 4 (ix)
   44C9 DD 77 FE      [19]  125 	ld	-2 (ix), a
   44CC DD 7E 05      [19]  126 	ld	a, 5 (ix)
   44CF DD 77 FF      [19]  127 	ld	-1 (ix), a
   44D2 DD 7E FE      [19]  128 	ld	a, -2 (ix)
   44D5 C6 02         [ 7]  129 	add	a, #0x02
   44D7 DD 77 FC      [19]  130 	ld	-4 (ix), a
   44DA DD 7E FF      [19]  131 	ld	a, -1 (ix)
   44DD CE 00         [ 7]  132 	adc	a, #0x00
   44DF DD 77 FD      [19]  133 	ld	-3 (ix), a
   44E2 DD 6E FC      [19]  134 	ld	l,-4 (ix)
   44E5 DD 66 FD      [19]  135 	ld	h,-3 (ix)
   44E8 36 00         [10]  136 	ld	(hl), #0x00
                            137 ;src/entities/player.c:32: if (input_is_left_pressed()) {
   44EA CD 2D 43      [17]  138 	call	_input_is_left_pressed
   44ED 7D            [ 4]  139 	ld	a, l
   44EE B7            [ 4]  140 	or	a, a
   44EF 28 10         [12]  141 	jr	Z,00106$
                            142 ;src/entities/player.c:33: player->vx = (i8)(-kplayermovespeed);
   44F1 21 AD 44      [10]  143 	ld	hl,#_kplayermovespeed + 0
   44F4 4E            [ 7]  144 	ld	c, (hl)
   44F5 AF            [ 4]  145 	xor	a, a
   44F6 91            [ 4]  146 	sub	a, c
   44F7 4F            [ 4]  147 	ld	c, a
   44F8 DD 6E FC      [19]  148 	ld	l,-4 (ix)
   44FB DD 66 FD      [19]  149 	ld	h,-3 (ix)
   44FE 71            [ 7]  150 	ld	(hl), c
   44FF 18 12         [12]  151 	jr	00107$
   4501                     152 00106$:
                            153 ;src/entities/player.c:34: } else if (input_is_right_pressed()) {
   4501 CD 35 43      [17]  154 	call	_input_is_right_pressed
   4504 7D            [ 4]  155 	ld	a, l
   4505 B7            [ 4]  156 	or	a, a
   4506 28 0B         [12]  157 	jr	Z,00107$
                            158 ;src/entities/player.c:35: player->vx = kplayermovespeed;
   4508 21 AD 44      [10]  159 	ld	hl,#_kplayermovespeed + 0
   450B 4E            [ 7]  160 	ld	c, (hl)
   450C DD 6E FC      [19]  161 	ld	l,-4 (ix)
   450F DD 66 FD      [19]  162 	ld	h,-3 (ix)
   4512 71            [ 7]  163 	ld	(hl), c
   4513                     164 00107$:
                            165 ;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
   4513 CD 3D 43      [17]  166 	call	_input_is_jump_pressed
   4516 DD 7E FE      [19]  167 	ld	a, -2 (ix)
   4519 C6 05         [ 7]  168 	add	a, #0x05
   451B DD 77 FA      [19]  169 	ld	-6 (ix), a
   451E DD 7E FF      [19]  170 	ld	a, -1 (ix)
   4521 CE 00         [ 7]  171 	adc	a, #0x00
   4523 DD 77 FB      [19]  172 	ld	-5 (ix), a
   4526 DD 7E FE      [19]  173 	ld	a, -2 (ix)
   4529 C6 01         [ 7]  174 	add	a, #0x01
   452B DD 77 F8      [19]  175 	ld	-8 (ix), a
   452E DD 7E FF      [19]  176 	ld	a, -1 (ix)
   4531 CE 00         [ 7]  177 	adc	a, #0x00
   4533 DD 77 F9      [19]  178 	ld	-7 (ix), a
                            179 ;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
   4536 DD 5E FE      [19]  180 	ld	e,-2 (ix)
   4539 DD 56 FF      [19]  181 	ld	d,-1 (ix)
   453C 13            [ 6]  182 	inc	de
   453D 13            [ 6]  183 	inc	de
   453E 13            [ 6]  184 	inc	de
                            185 ;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
   453F 7D            [ 4]  186 	ld	a, l
   4540 B7            [ 4]  187 	or	a, a
   4541 28 1E         [12]  188 	jr	Z,00109$
   4543 DD 6E FA      [19]  189 	ld	l,-6 (ix)
   4546 DD 66 FB      [19]  190 	ld	h,-5 (ix)
   4549 7E            [ 7]  191 	ld	a, (hl)
   454A E1            [10]  192 	pop	hl
   454B E5            [11]  193 	push	hl
   454C 4E            [ 7]  194 	ld	c, (hl)
   454D 06 00         [ 7]  195 	ld	b, #0x00
   454F D5            [11]  196 	push	de
   4550 F5            [11]  197 	push	af
   4551 33            [ 6]  198 	inc	sp
   4552 C5            [11]  199 	push	bc
   4553 CD 66 40      [17]  200 	call	_collision_is_on_ground
   4556 F1            [10]  201 	pop	af
   4557 33            [ 6]  202 	inc	sp
   4558 D1            [10]  203 	pop	de
   4559 7D            [ 4]  204 	ld	a, l
   455A B7            [ 4]  205 	or	a, a
   455B 28 04         [12]  206 	jr	Z,00109$
                            207 ;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
   455D 3A AF 44      [13]  208 	ld	a,(#_kplayerjumpvelocity + 0)
   4560 12            [ 7]  209 	ld	(de), a
   4561                     210 00109$:
                            211 ;src/entities/player.c:42: player->vy = (i8)(player->vy + kplayergravity);
   4561 1A            [ 7]  212 	ld	a, (de)
   4562 4F            [ 4]  213 	ld	c, a
   4563 21 AE 44      [10]  214 	ld	hl,#_kplayergravity + 0
   4566 46            [ 7]  215 	ld	b, (hl)
   4567 79            [ 4]  216 	ld	a, c
   4568 80            [ 4]  217 	add	a, b
   4569 12            [ 7]  218 	ld	(de), a
                            219 ;src/entities/player.c:44: nextx = (i16)player->x + (i16)player->vx;
   456A DD 6E FE      [19]  220 	ld	l,-2 (ix)
   456D DD 66 FF      [19]  221 	ld	h,-1 (ix)
   4570 4E            [ 7]  222 	ld	c, (hl)
   4571 06 00         [ 7]  223 	ld	b, #0x00
   4573 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   4576 DD 66 FD      [19]  225 	ld	h,-3 (ix)
   4579 6E            [ 7]  226 	ld	l, (hl)
   457A 7D            [ 4]  227 	ld	a, l
   457B 17            [ 4]  228 	rla
   457C 9F            [ 4]  229 	sbc	a, a
   457D 67            [ 4]  230 	ld	h, a
   457E 09            [11]  231 	add	hl, bc
                            232 ;src/entities/player.c:45: if (nextx < 0) {
   457F CB 7C         [ 8]  233 	bit	7, h
   4581 28 03         [12]  234 	jr	Z,00112$
                            235 ;src/entities/player.c:46: nextx = 0;
   4583 21 00 00      [10]  236 	ld	hl, #0x0000
   4586                     237 00112$:
                            238 ;src/entities/player.c:48: if (nextx > 76) {
   4586 3E 4C         [ 7]  239 	ld	a, #0x4c
   4588 BD            [ 4]  240 	cp	a, l
   4589 3E 00         [ 7]  241 	ld	a, #0x00
   458B 9C            [ 4]  242 	sbc	a, h
   458C E2 91 45      [10]  243 	jp	PO, 00162$
   458F EE 80         [ 7]  244 	xor	a, #0x80
   4591                     245 00162$:
   4591 F2 97 45      [10]  246 	jp	P, 00114$
                            247 ;src/entities/player.c:49: nextx = 76;
   4594 21 4C 00      [10]  248 	ld	hl, #0x004c
   4597                     249 00114$:
                            250 ;src/entities/player.c:51: player->x = (u8)nextx;
   4597 4D            [ 4]  251 	ld	c, l
   4598 DD 6E FE      [19]  252 	ld	l,-2 (ix)
   459B DD 66 FF      [19]  253 	ld	h,-1 (ix)
   459E 71            [ 7]  254 	ld	(hl), c
                            255 ;src/entities/player.c:53: nexty = (i16)player->y + (i16)player->vy;
   459F E1            [10]  256 	pop	hl
   45A0 E5            [11]  257 	push	hl
   45A1 4E            [ 7]  258 	ld	c, (hl)
   45A2 06 00         [ 7]  259 	ld	b, #0x00
   45A4 1A            [ 7]  260 	ld	a, (de)
   45A5 6F            [ 4]  261 	ld	l, a
   45A6 17            [ 4]  262 	rla
   45A7 9F            [ 4]  263 	sbc	a, a
   45A8 67            [ 4]  264 	ld	h, a
   45A9 09            [11]  265 	add	hl,bc
   45AA 4D            [ 4]  266 	ld	c, l
   45AB 44            [ 4]  267 	ld	b, h
                            268 ;src/entities/player.c:54: nexty = collision_clamp_y_to_ground(nexty, player->h);
   45AC DD 6E FA      [19]  269 	ld	l,-6 (ix)
   45AF DD 66 FB      [19]  270 	ld	h,-5 (ix)
   45B2 66            [ 7]  271 	ld	h, (hl)
   45B3 D5            [11]  272 	push	de
   45B4 E5            [11]  273 	push	hl
   45B5 33            [ 6]  274 	inc	sp
   45B6 C5            [11]  275 	push	bc
   45B7 CD 8C 40      [17]  276 	call	_collision_clamp_y_to_ground
   45BA F1            [10]  277 	pop	af
   45BB 33            [ 6]  278 	inc	sp
   45BC D1            [10]  279 	pop	de
                            280 ;src/entities/player.c:55: if (nexty < 0) {
   45BD CB 7C         [ 8]  281 	bit	7, h
   45BF 28 03         [12]  282 	jr	Z,00116$
                            283 ;src/entities/player.c:56: nexty = 0;
   45C1 21 00 00      [10]  284 	ld	hl, #0x0000
   45C4                     285 00116$:
                            286 ;src/entities/player.c:58: player->y = (u8)nexty;
   45C4 4D            [ 4]  287 	ld	c, l
   45C5 E1            [10]  288 	pop	hl
   45C6 E5            [11]  289 	push	hl
   45C7 71            [ 7]  290 	ld	(hl), c
                            291 ;src/entities/player.c:60: if (collision_is_on_ground((i16)player->y, player->h) && player->vy > 0) {
   45C8 DD 6E FA      [19]  292 	ld	l,-6 (ix)
   45CB DD 66 FB      [19]  293 	ld	h,-5 (ix)
   45CE 66            [ 7]  294 	ld	h, (hl)
   45CF 06 00         [ 7]  295 	ld	b, #0x00
   45D1 D5            [11]  296 	push	de
   45D2 E5            [11]  297 	push	hl
   45D3 33            [ 6]  298 	inc	sp
   45D4 C5            [11]  299 	push	bc
   45D5 CD 66 40      [17]  300 	call	_collision_is_on_ground
   45D8 F1            [10]  301 	pop	af
   45D9 33            [ 6]  302 	inc	sp
   45DA D1            [10]  303 	pop	de
   45DB 7D            [ 4]  304 	ld	a, l
   45DC B7            [ 4]  305 	or	a, a
   45DD 28 0E         [12]  306 	jr	Z,00120$
   45DF 1A            [ 7]  307 	ld	a, (de)
   45E0 4F            [ 4]  308 	ld	c, a
   45E1 AF            [ 4]  309 	xor	a, a
   45E2 91            [ 4]  310 	sub	a, c
   45E3 E2 E8 45      [10]  311 	jp	PO, 00163$
   45E6 EE 80         [ 7]  312 	xor	a, #0x80
   45E8                     313 00163$:
   45E8 F2 ED 45      [10]  314 	jp	P, 00120$
                            315 ;src/entities/player.c:61: player->vy = 0;
   45EB AF            [ 4]  316 	xor	a, a
   45EC 12            [ 7]  317 	ld	(de), a
   45ED                     318 00120$:
   45ED DD F9         [10]  319 	ld	sp, ix
   45EF DD E1         [14]  320 	pop	ix
   45F1 C9            [10]  321 	ret
                            322 ;src/entities/player.c:65: void playerrender(const Player* player) {
                            323 ;	---------------------------------
                            324 ; Function playerrender
                            325 ; ---------------------------------
   45F2                     326 _playerrender::
   45F2 DD E5         [15]  327 	push	ix
   45F4 DD 21 00 00   [14]  328 	ld	ix,#0
   45F8 DD 39         [15]  329 	add	ix,sp
                            330 ;src/entities/player.c:68: if (!player) {
   45FA DD 7E 05      [19]  331 	ld	a, 5 (ix)
   45FD DD B6 04      [19]  332 	or	a,4 (ix)
                            333 ;src/entities/player.c:69: return;
   4600 28 32         [12]  334 	jr	Z,00103$
                            335 ;src/entities/player.c:72: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   4602 DD 5E 04      [19]  336 	ld	e,4 (ix)
   4605 DD 56 05      [19]  337 	ld	d,5 (ix)
   4608 6B            [ 4]  338 	ld	l, e
   4609 62            [ 4]  339 	ld	h, d
   460A 23            [ 6]  340 	inc	hl
   460B 46            [ 7]  341 	ld	b, (hl)
   460C 1A            [ 7]  342 	ld	a, (de)
   460D D5            [11]  343 	push	de
   460E C5            [11]  344 	push	bc
   460F 33            [ 6]  345 	inc	sp
   4610 F5            [11]  346 	push	af
   4611 33            [ 6]  347 	inc	sp
   4612 21 00 C0      [10]  348 	ld	hl, #0xc000
   4615 E5            [11]  349 	push	hl
   4616 CD A1 48      [17]  350 	call	_cpct_getScreenPtr
   4619 4D            [ 4]  351 	ld	c, l
   461A 44            [ 4]  352 	ld	b, h
   461B D1            [10]  353 	pop	de
                            354 ;src/entities/player.c:73: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   461C D5            [11]  355 	push	de
   461D FD E1         [14]  356 	pop	iy
   461F FD 7E 05      [19]  357 	ld	a, 5 (iy)
   4622 EB            [ 4]  358 	ex	de,hl
   4623 11 04 00      [10]  359 	ld	de, #0x0004
   4626 19            [11]  360 	add	hl, de
   4627 56            [ 7]  361 	ld	d, (hl)
   4628 F5            [11]  362 	push	af
   4629 33            [ 6]  363 	inc	sp
   462A 1E 4F         [ 7]  364 	ld	e, #0x4f
   462C D5            [11]  365 	push	de
   462D C5            [11]  366 	push	bc
   462E CD E8 47      [17]  367 	call	_cpct_drawSolidBox
   4631 F1            [10]  368 	pop	af
   4632 F1            [10]  369 	pop	af
   4633 33            [ 6]  370 	inc	sp
   4634                     371 00103$:
   4634 DD E1         [14]  372 	pop	ix
   4636 C9            [10]  373 	ret
                            374 	.area _CODE
                            375 	.area _INITIALIZER
                            376 	.area _CABS (ABS)
