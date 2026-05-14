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
   4483                      56 _playerinit::
                             57 ;src/entities/player.c:11: if (!player) {
   4483 21 03 00      [10]   58 	ld	hl, #2+1
   4486 39            [11]   59 	add	hl, sp
   4487 7E            [ 7]   60 	ld	a, (hl)
   4488 2B            [ 6]   61 	dec	hl
   4489 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/player.c:12: return;
   448A C8            [11]   64 	ret	Z
                             65 ;src/entities/player.c:15: player->x = 20;
   448B D1            [10]   66 	pop	de
   448C C1            [10]   67 	pop	bc
   448D C5            [11]   68 	push	bc
   448E D5            [11]   69 	push	de
   448F 3E 14         [ 7]   70 	ld	a, #0x14
   4491 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/player.c:16: player->y = 120;
   4492 69            [ 4]   73 	ld	l, c
   4493 60            [ 4]   74 	ld	h, b
   4494 23            [ 6]   75 	inc	hl
   4495 36 78         [10]   76 	ld	(hl), #0x78
                             77 ;src/entities/player.c:17: player->vx = 0;
   4497 59            [ 4]   78 	ld	e, c
   4498 50            [ 4]   79 	ld	d, b
   4499 13            [ 6]   80 	inc	de
   449A 13            [ 6]   81 	inc	de
   449B AF            [ 4]   82 	xor	a, a
   449C 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/player.c:18: player->vy = 0;
   449D 59            [ 4]   85 	ld	e, c
   449E 50            [ 4]   86 	ld	d, b
   449F 13            [ 6]   87 	inc	de
   44A0 13            [ 6]   88 	inc	de
   44A1 13            [ 6]   89 	inc	de
   44A2 AF            [ 4]   90 	xor	a, a
   44A3 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/player.c:19: player->w = 4;
   44A4 21 04 00      [10]   93 	ld	hl, #0x0004
   44A7 09            [11]   94 	add	hl, bc
   44A8 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/player.c:20: player->h = 16;
   44AA 21 05 00      [10]   97 	ld	hl, #0x0005
   44AD 09            [11]   98 	add	hl, bc
   44AE 36 10         [10]   99 	ld	(hl), #0x10
   44B0 C9            [10]  100 	ret
   44B1                     101 _kplayermovespeed:
   44B1 02                  102 	.db #0x02	;  2
   44B2                     103 _kplayergravity:
   44B2 01                  104 	.db #0x01	;  1
   44B3                     105 _kplayerjumpvelocity:
   44B3 FB                  106 	.db #0xfb	; -5
                            107 ;src/entities/player.c:23: void playerupdate(Player* player) {
                            108 ;	---------------------------------
                            109 ; Function playerupdate
                            110 ; ---------------------------------
   44B4                     111 _playerupdate::
   44B4 DD E5         [15]  112 	push	ix
   44B6 DD 21 00 00   [14]  113 	ld	ix,#0
   44BA DD 39         [15]  114 	add	ix,sp
   44BC 21 F8 FF      [10]  115 	ld	hl, #-8
   44BF 39            [11]  116 	add	hl, sp
   44C0 F9            [ 6]  117 	ld	sp, hl
                            118 ;src/entities/player.c:27: if (!player) {
   44C1 DD 7E 05      [19]  119 	ld	a, 5 (ix)
   44C4 DD B6 04      [19]  120 	or	a,4 (ix)
                            121 ;src/entities/player.c:28: return;
   44C7 CA F1 45      [10]  122 	jp	Z,00120$
                            123 ;src/entities/player.c:31: player->vx = 0;
   44CA DD 7E 04      [19]  124 	ld	a, 4 (ix)
   44CD DD 77 FE      [19]  125 	ld	-2 (ix), a
   44D0 DD 7E 05      [19]  126 	ld	a, 5 (ix)
   44D3 DD 77 FF      [19]  127 	ld	-1 (ix), a
   44D6 DD 7E FE      [19]  128 	ld	a, -2 (ix)
   44D9 C6 02         [ 7]  129 	add	a, #0x02
   44DB DD 77 FC      [19]  130 	ld	-4 (ix), a
   44DE DD 7E FF      [19]  131 	ld	a, -1 (ix)
   44E1 CE 00         [ 7]  132 	adc	a, #0x00
   44E3 DD 77 FD      [19]  133 	ld	-3 (ix), a
   44E6 DD 6E FC      [19]  134 	ld	l,-4 (ix)
   44E9 DD 66 FD      [19]  135 	ld	h,-3 (ix)
   44EC 36 00         [10]  136 	ld	(hl), #0x00
                            137 ;src/entities/player.c:32: if (input_is_left_pressed()) {
   44EE CD 2D 43      [17]  138 	call	_input_is_left_pressed
   44F1 7D            [ 4]  139 	ld	a, l
   44F2 B7            [ 4]  140 	or	a, a
   44F3 28 10         [12]  141 	jr	Z,00106$
                            142 ;src/entities/player.c:33: player->vx = (i8)(-kplayermovespeed);
   44F5 21 B1 44      [10]  143 	ld	hl,#_kplayermovespeed + 0
   44F8 4E            [ 7]  144 	ld	c, (hl)
   44F9 AF            [ 4]  145 	xor	a, a
   44FA 91            [ 4]  146 	sub	a, c
   44FB 4F            [ 4]  147 	ld	c, a
   44FC DD 6E FC      [19]  148 	ld	l,-4 (ix)
   44FF DD 66 FD      [19]  149 	ld	h,-3 (ix)
   4502 71            [ 7]  150 	ld	(hl), c
   4503 18 12         [12]  151 	jr	00107$
   4505                     152 00106$:
                            153 ;src/entities/player.c:34: } else if (input_is_right_pressed()) {
   4505 CD 35 43      [17]  154 	call	_input_is_right_pressed
   4508 7D            [ 4]  155 	ld	a, l
   4509 B7            [ 4]  156 	or	a, a
   450A 28 0B         [12]  157 	jr	Z,00107$
                            158 ;src/entities/player.c:35: player->vx = kplayermovespeed;
   450C 21 B1 44      [10]  159 	ld	hl,#_kplayermovespeed + 0
   450F 4E            [ 7]  160 	ld	c, (hl)
   4510 DD 6E FC      [19]  161 	ld	l,-4 (ix)
   4513 DD 66 FD      [19]  162 	ld	h,-3 (ix)
   4516 71            [ 7]  163 	ld	(hl), c
   4517                     164 00107$:
                            165 ;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
   4517 CD 3D 43      [17]  166 	call	_input_is_jump_pressed
   451A DD 7E FE      [19]  167 	ld	a, -2 (ix)
   451D C6 05         [ 7]  168 	add	a, #0x05
   451F DD 77 FA      [19]  169 	ld	-6 (ix), a
   4522 DD 7E FF      [19]  170 	ld	a, -1 (ix)
   4525 CE 00         [ 7]  171 	adc	a, #0x00
   4527 DD 77 FB      [19]  172 	ld	-5 (ix), a
   452A DD 7E FE      [19]  173 	ld	a, -2 (ix)
   452D C6 01         [ 7]  174 	add	a, #0x01
   452F DD 77 F8      [19]  175 	ld	-8 (ix), a
   4532 DD 7E FF      [19]  176 	ld	a, -1 (ix)
   4535 CE 00         [ 7]  177 	adc	a, #0x00
   4537 DD 77 F9      [19]  178 	ld	-7 (ix), a
                            179 ;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
   453A DD 5E FE      [19]  180 	ld	e,-2 (ix)
   453D DD 56 FF      [19]  181 	ld	d,-1 (ix)
   4540 13            [ 6]  182 	inc	de
   4541 13            [ 6]  183 	inc	de
   4542 13            [ 6]  184 	inc	de
                            185 ;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
   4543 7D            [ 4]  186 	ld	a, l
   4544 B7            [ 4]  187 	or	a, a
   4545 28 1E         [12]  188 	jr	Z,00109$
   4547 DD 6E FA      [19]  189 	ld	l,-6 (ix)
   454A DD 66 FB      [19]  190 	ld	h,-5 (ix)
   454D 7E            [ 7]  191 	ld	a, (hl)
   454E E1            [10]  192 	pop	hl
   454F E5            [11]  193 	push	hl
   4550 4E            [ 7]  194 	ld	c, (hl)
   4551 06 00         [ 7]  195 	ld	b, #0x00
   4553 D5            [11]  196 	push	de
   4554 F5            [11]  197 	push	af
   4555 33            [ 6]  198 	inc	sp
   4556 C5            [11]  199 	push	bc
   4557 CD 66 40      [17]  200 	call	_collision_is_on_ground
   455A F1            [10]  201 	pop	af
   455B 33            [ 6]  202 	inc	sp
   455C D1            [10]  203 	pop	de
   455D 7D            [ 4]  204 	ld	a, l
   455E B7            [ 4]  205 	or	a, a
   455F 28 04         [12]  206 	jr	Z,00109$
                            207 ;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
   4561 3A B3 44      [13]  208 	ld	a,(#_kplayerjumpvelocity + 0)
   4564 12            [ 7]  209 	ld	(de), a
   4565                     210 00109$:
                            211 ;src/entities/player.c:42: player->vy = (i8)(player->vy + kplayergravity);
   4565 1A            [ 7]  212 	ld	a, (de)
   4566 4F            [ 4]  213 	ld	c, a
   4567 21 B2 44      [10]  214 	ld	hl,#_kplayergravity + 0
   456A 46            [ 7]  215 	ld	b, (hl)
   456B 79            [ 4]  216 	ld	a, c
   456C 80            [ 4]  217 	add	a, b
   456D 12            [ 7]  218 	ld	(de), a
                            219 ;src/entities/player.c:44: nextx = (i16)player->x + (i16)player->vx;
   456E DD 6E FE      [19]  220 	ld	l,-2 (ix)
   4571 DD 66 FF      [19]  221 	ld	h,-1 (ix)
   4574 4E            [ 7]  222 	ld	c, (hl)
   4575 06 00         [ 7]  223 	ld	b, #0x00
   4577 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   457A DD 66 FD      [19]  225 	ld	h,-3 (ix)
   457D 6E            [ 7]  226 	ld	l, (hl)
   457E 7D            [ 4]  227 	ld	a, l
   457F 17            [ 4]  228 	rla
   4580 9F            [ 4]  229 	sbc	a, a
   4581 67            [ 4]  230 	ld	h, a
   4582 09            [11]  231 	add	hl, bc
                            232 ;src/entities/player.c:45: if (nextx < 0) {
   4583 CB 7C         [ 8]  233 	bit	7, h
   4585 28 03         [12]  234 	jr	Z,00112$
                            235 ;src/entities/player.c:46: nextx = 0;
   4587 21 00 00      [10]  236 	ld	hl, #0x0000
   458A                     237 00112$:
                            238 ;src/entities/player.c:48: if (nextx > 76) {
   458A 3E 4C         [ 7]  239 	ld	a, #0x4c
   458C BD            [ 4]  240 	cp	a, l
   458D 3E 00         [ 7]  241 	ld	a, #0x00
   458F 9C            [ 4]  242 	sbc	a, h
   4590 E2 95 45      [10]  243 	jp	PO, 00162$
   4593 EE 80         [ 7]  244 	xor	a, #0x80
   4595                     245 00162$:
   4595 F2 9B 45      [10]  246 	jp	P, 00114$
                            247 ;src/entities/player.c:49: nextx = 76;
   4598 21 4C 00      [10]  248 	ld	hl, #0x004c
   459B                     249 00114$:
                            250 ;src/entities/player.c:51: player->x = (u8)nextx;
   459B 4D            [ 4]  251 	ld	c, l
   459C DD 6E FE      [19]  252 	ld	l,-2 (ix)
   459F DD 66 FF      [19]  253 	ld	h,-1 (ix)
   45A2 71            [ 7]  254 	ld	(hl), c
                            255 ;src/entities/player.c:53: nexty = (i16)player->y + (i16)player->vy;
   45A3 E1            [10]  256 	pop	hl
   45A4 E5            [11]  257 	push	hl
   45A5 4E            [ 7]  258 	ld	c, (hl)
   45A6 06 00         [ 7]  259 	ld	b, #0x00
   45A8 1A            [ 7]  260 	ld	a, (de)
   45A9 6F            [ 4]  261 	ld	l, a
   45AA 17            [ 4]  262 	rla
   45AB 9F            [ 4]  263 	sbc	a, a
   45AC 67            [ 4]  264 	ld	h, a
   45AD 09            [11]  265 	add	hl,bc
   45AE 4D            [ 4]  266 	ld	c, l
   45AF 44            [ 4]  267 	ld	b, h
                            268 ;src/entities/player.c:54: nexty = collision_clamp_y_to_ground(nexty, player->h);
   45B0 DD 6E FA      [19]  269 	ld	l,-6 (ix)
   45B3 DD 66 FB      [19]  270 	ld	h,-5 (ix)
   45B6 66            [ 7]  271 	ld	h, (hl)
   45B7 D5            [11]  272 	push	de
   45B8 E5            [11]  273 	push	hl
   45B9 33            [ 6]  274 	inc	sp
   45BA C5            [11]  275 	push	bc
   45BB CD 8C 40      [17]  276 	call	_collision_clamp_y_to_ground
   45BE F1            [10]  277 	pop	af
   45BF 33            [ 6]  278 	inc	sp
   45C0 D1            [10]  279 	pop	de
                            280 ;src/entities/player.c:55: if (nexty < 0) {
   45C1 CB 7C         [ 8]  281 	bit	7, h
   45C3 28 03         [12]  282 	jr	Z,00116$
                            283 ;src/entities/player.c:56: nexty = 0;
   45C5 21 00 00      [10]  284 	ld	hl, #0x0000
   45C8                     285 00116$:
                            286 ;src/entities/player.c:58: player->y = (u8)nexty;
   45C8 4D            [ 4]  287 	ld	c, l
   45C9 E1            [10]  288 	pop	hl
   45CA E5            [11]  289 	push	hl
   45CB 71            [ 7]  290 	ld	(hl), c
                            291 ;src/entities/player.c:60: if (collision_is_on_ground((i16)player->y, player->h) && player->vy > 0) {
   45CC DD 6E FA      [19]  292 	ld	l,-6 (ix)
   45CF DD 66 FB      [19]  293 	ld	h,-5 (ix)
   45D2 66            [ 7]  294 	ld	h, (hl)
   45D3 06 00         [ 7]  295 	ld	b, #0x00
   45D5 D5            [11]  296 	push	de
   45D6 E5            [11]  297 	push	hl
   45D7 33            [ 6]  298 	inc	sp
   45D8 C5            [11]  299 	push	bc
   45D9 CD 66 40      [17]  300 	call	_collision_is_on_ground
   45DC F1            [10]  301 	pop	af
   45DD 33            [ 6]  302 	inc	sp
   45DE D1            [10]  303 	pop	de
   45DF 7D            [ 4]  304 	ld	a, l
   45E0 B7            [ 4]  305 	or	a, a
   45E1 28 0E         [12]  306 	jr	Z,00120$
   45E3 1A            [ 7]  307 	ld	a, (de)
   45E4 4F            [ 4]  308 	ld	c, a
   45E5 AF            [ 4]  309 	xor	a, a
   45E6 91            [ 4]  310 	sub	a, c
   45E7 E2 EC 45      [10]  311 	jp	PO, 00163$
   45EA EE 80         [ 7]  312 	xor	a, #0x80
   45EC                     313 00163$:
   45EC F2 F1 45      [10]  314 	jp	P, 00120$
                            315 ;src/entities/player.c:61: player->vy = 0;
   45EF AF            [ 4]  316 	xor	a, a
   45F0 12            [ 7]  317 	ld	(de), a
   45F1                     318 00120$:
   45F1 DD F9         [10]  319 	ld	sp, ix
   45F3 DD E1         [14]  320 	pop	ix
   45F5 C9            [10]  321 	ret
                            322 ;src/entities/player.c:65: void playerrender(const Player* player) {
                            323 ;	---------------------------------
                            324 ; Function playerrender
                            325 ; ---------------------------------
   45F6                     326 _playerrender::
   45F6 DD E5         [15]  327 	push	ix
   45F8 DD 21 00 00   [14]  328 	ld	ix,#0
   45FC DD 39         [15]  329 	add	ix,sp
                            330 ;src/entities/player.c:68: if (!player) {
   45FE DD 7E 05      [19]  331 	ld	a, 5 (ix)
   4601 DD B6 04      [19]  332 	or	a,4 (ix)
                            333 ;src/entities/player.c:69: return;
   4604 28 32         [12]  334 	jr	Z,00103$
                            335 ;src/entities/player.c:72: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   4606 DD 5E 04      [19]  336 	ld	e,4 (ix)
   4609 DD 56 05      [19]  337 	ld	d,5 (ix)
   460C 6B            [ 4]  338 	ld	l, e
   460D 62            [ 4]  339 	ld	h, d
   460E 23            [ 6]  340 	inc	hl
   460F 46            [ 7]  341 	ld	b, (hl)
   4610 1A            [ 7]  342 	ld	a, (de)
   4611 D5            [11]  343 	push	de
   4612 C5            [11]  344 	push	bc
   4613 33            [ 6]  345 	inc	sp
   4614 F5            [11]  346 	push	af
   4615 33            [ 6]  347 	inc	sp
   4616 21 00 C0      [10]  348 	ld	hl, #0xc000
   4619 E5            [11]  349 	push	hl
   461A CD A5 48      [17]  350 	call	_cpct_getScreenPtr
   461D 4D            [ 4]  351 	ld	c, l
   461E 44            [ 4]  352 	ld	b, h
   461F D1            [10]  353 	pop	de
                            354 ;src/entities/player.c:73: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   4620 D5            [11]  355 	push	de
   4621 FD E1         [14]  356 	pop	iy
   4623 FD 7E 05      [19]  357 	ld	a, 5 (iy)
   4626 EB            [ 4]  358 	ex	de,hl
   4627 11 04 00      [10]  359 	ld	de, #0x0004
   462A 19            [11]  360 	add	hl, de
   462B 56            [ 7]  361 	ld	d, (hl)
   462C F5            [11]  362 	push	af
   462D 33            [ 6]  363 	inc	sp
   462E 1E 4F         [ 7]  364 	ld	e, #0x4f
   4630 D5            [11]  365 	push	de
   4631 C5            [11]  366 	push	bc
   4632 CD EC 47      [17]  367 	call	_cpct_drawSolidBox
   4635 F1            [10]  368 	pop	af
   4636 F1            [10]  369 	pop	af
   4637 33            [ 6]  370 	inc	sp
   4638                     371 00103$:
   4638 DD E1         [14]  372 	pop	ix
   463A C9            [10]  373 	ret
                            374 	.area _CODE
                            375 	.area _INITIALIZER
                            376 	.area _CABS (ABS)
