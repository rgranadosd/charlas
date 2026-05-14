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
   44D0                      56 _playerinit::
                             57 ;src/entities/player.c:11: if (!player) {
   44D0 21 03 00      [10]   58 	ld	hl, #2+1
   44D3 39            [11]   59 	add	hl, sp
   44D4 7E            [ 7]   60 	ld	a, (hl)
   44D5 2B            [ 6]   61 	dec	hl
   44D6 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/player.c:12: return;
   44D7 C8            [11]   64 	ret	Z
                             65 ;src/entities/player.c:15: player->x = 20;
   44D8 D1            [10]   66 	pop	de
   44D9 C1            [10]   67 	pop	bc
   44DA C5            [11]   68 	push	bc
   44DB D5            [11]   69 	push	de
   44DC 3E 14         [ 7]   70 	ld	a, #0x14
   44DE 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/player.c:16: player->y = 120;
   44DF 69            [ 4]   73 	ld	l, c
   44E0 60            [ 4]   74 	ld	h, b
   44E1 23            [ 6]   75 	inc	hl
   44E2 36 78         [10]   76 	ld	(hl), #0x78
                             77 ;src/entities/player.c:17: player->vx = 0;
   44E4 59            [ 4]   78 	ld	e, c
   44E5 50            [ 4]   79 	ld	d, b
   44E6 13            [ 6]   80 	inc	de
   44E7 13            [ 6]   81 	inc	de
   44E8 AF            [ 4]   82 	xor	a, a
   44E9 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/player.c:18: player->vy = 0;
   44EA 59            [ 4]   85 	ld	e, c
   44EB 50            [ 4]   86 	ld	d, b
   44EC 13            [ 6]   87 	inc	de
   44ED 13            [ 6]   88 	inc	de
   44EE 13            [ 6]   89 	inc	de
   44EF AF            [ 4]   90 	xor	a, a
   44F0 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/player.c:19: player->w = 4;
   44F1 21 04 00      [10]   93 	ld	hl, #0x0004
   44F4 09            [11]   94 	add	hl, bc
   44F5 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/player.c:20: player->h = 16;
   44F7 21 05 00      [10]   97 	ld	hl, #0x0005
   44FA 09            [11]   98 	add	hl, bc
   44FB 36 10         [10]   99 	ld	(hl), #0x10
   44FD C9            [10]  100 	ret
   44FE                     101 _kplayermovespeed:
   44FE 02                  102 	.db #0x02	;  2
   44FF                     103 _kplayergravity:
   44FF 01                  104 	.db #0x01	;  1
   4500                     105 _kplayerjumpvelocity:
   4500 FB                  106 	.db #0xfb	; -5
                            107 ;src/entities/player.c:23: void playerupdate(Player* player) {
                            108 ;	---------------------------------
                            109 ; Function playerupdate
                            110 ; ---------------------------------
   4501                     111 _playerupdate::
   4501 DD E5         [15]  112 	push	ix
   4503 DD 21 00 00   [14]  113 	ld	ix,#0
   4507 DD 39         [15]  114 	add	ix,sp
   4509 21 F8 FF      [10]  115 	ld	hl, #-8
   450C 39            [11]  116 	add	hl, sp
   450D F9            [ 6]  117 	ld	sp, hl
                            118 ;src/entities/player.c:27: if (!player) {
   450E DD 7E 05      [19]  119 	ld	a, 5 (ix)
   4511 DD B6 04      [19]  120 	or	a,4 (ix)
                            121 ;src/entities/player.c:28: return;
   4514 CA 3E 46      [10]  122 	jp	Z,00120$
                            123 ;src/entities/player.c:31: player->vx = 0;
   4517 DD 7E 04      [19]  124 	ld	a, 4 (ix)
   451A DD 77 FE      [19]  125 	ld	-2 (ix), a
   451D DD 7E 05      [19]  126 	ld	a, 5 (ix)
   4520 DD 77 FF      [19]  127 	ld	-1 (ix), a
   4523 DD 7E FE      [19]  128 	ld	a, -2 (ix)
   4526 C6 02         [ 7]  129 	add	a, #0x02
   4528 DD 77 FC      [19]  130 	ld	-4 (ix), a
   452B DD 7E FF      [19]  131 	ld	a, -1 (ix)
   452E CE 00         [ 7]  132 	adc	a, #0x00
   4530 DD 77 FD      [19]  133 	ld	-3 (ix), a
   4533 DD 6E FC      [19]  134 	ld	l,-4 (ix)
   4536 DD 66 FD      [19]  135 	ld	h,-3 (ix)
   4539 36 00         [10]  136 	ld	(hl), #0x00
                            137 ;src/entities/player.c:32: if (input_is_left_pressed()) {
   453B CD 2D 43      [17]  138 	call	_input_is_left_pressed
   453E 7D            [ 4]  139 	ld	a, l
   453F B7            [ 4]  140 	or	a, a
   4540 28 10         [12]  141 	jr	Z,00106$
                            142 ;src/entities/player.c:33: player->vx = (i8)(-kplayermovespeed);
   4542 21 FE 44      [10]  143 	ld	hl,#_kplayermovespeed + 0
   4545 4E            [ 7]  144 	ld	c, (hl)
   4546 AF            [ 4]  145 	xor	a, a
   4547 91            [ 4]  146 	sub	a, c
   4548 4F            [ 4]  147 	ld	c, a
   4549 DD 6E FC      [19]  148 	ld	l,-4 (ix)
   454C DD 66 FD      [19]  149 	ld	h,-3 (ix)
   454F 71            [ 7]  150 	ld	(hl), c
   4550 18 12         [12]  151 	jr	00107$
   4552                     152 00106$:
                            153 ;src/entities/player.c:34: } else if (input_is_right_pressed()) {
   4552 CD 35 43      [17]  154 	call	_input_is_right_pressed
   4555 7D            [ 4]  155 	ld	a, l
   4556 B7            [ 4]  156 	or	a, a
   4557 28 0B         [12]  157 	jr	Z,00107$
                            158 ;src/entities/player.c:35: player->vx = kplayermovespeed;
   4559 21 FE 44      [10]  159 	ld	hl,#_kplayermovespeed + 0
   455C 4E            [ 7]  160 	ld	c, (hl)
   455D DD 6E FC      [19]  161 	ld	l,-4 (ix)
   4560 DD 66 FD      [19]  162 	ld	h,-3 (ix)
   4563 71            [ 7]  163 	ld	(hl), c
   4564                     164 00107$:
                            165 ;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
   4564 CD 3D 43      [17]  166 	call	_input_is_jump_pressed
   4567 DD 7E FE      [19]  167 	ld	a, -2 (ix)
   456A C6 05         [ 7]  168 	add	a, #0x05
   456C DD 77 FA      [19]  169 	ld	-6 (ix), a
   456F DD 7E FF      [19]  170 	ld	a, -1 (ix)
   4572 CE 00         [ 7]  171 	adc	a, #0x00
   4574 DD 77 FB      [19]  172 	ld	-5 (ix), a
   4577 DD 7E FE      [19]  173 	ld	a, -2 (ix)
   457A C6 01         [ 7]  174 	add	a, #0x01
   457C DD 77 F8      [19]  175 	ld	-8 (ix), a
   457F DD 7E FF      [19]  176 	ld	a, -1 (ix)
   4582 CE 00         [ 7]  177 	adc	a, #0x00
   4584 DD 77 F9      [19]  178 	ld	-7 (ix), a
                            179 ;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
   4587 DD 5E FE      [19]  180 	ld	e,-2 (ix)
   458A DD 56 FF      [19]  181 	ld	d,-1 (ix)
   458D 13            [ 6]  182 	inc	de
   458E 13            [ 6]  183 	inc	de
   458F 13            [ 6]  184 	inc	de
                            185 ;src/entities/player.c:38: if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
   4590 7D            [ 4]  186 	ld	a, l
   4591 B7            [ 4]  187 	or	a, a
   4592 28 1E         [12]  188 	jr	Z,00109$
   4594 DD 6E FA      [19]  189 	ld	l,-6 (ix)
   4597 DD 66 FB      [19]  190 	ld	h,-5 (ix)
   459A 7E            [ 7]  191 	ld	a, (hl)
   459B E1            [10]  192 	pop	hl
   459C E5            [11]  193 	push	hl
   459D 4E            [ 7]  194 	ld	c, (hl)
   459E 06 00         [ 7]  195 	ld	b, #0x00
   45A0 D5            [11]  196 	push	de
   45A1 F5            [11]  197 	push	af
   45A2 33            [ 6]  198 	inc	sp
   45A3 C5            [11]  199 	push	bc
   45A4 CD 66 40      [17]  200 	call	_collision_is_on_ground
   45A7 F1            [10]  201 	pop	af
   45A8 33            [ 6]  202 	inc	sp
   45A9 D1            [10]  203 	pop	de
   45AA 7D            [ 4]  204 	ld	a, l
   45AB B7            [ 4]  205 	or	a, a
   45AC 28 04         [12]  206 	jr	Z,00109$
                            207 ;src/entities/player.c:39: player->vy = kplayerjumpvelocity;
   45AE 3A 00 45      [13]  208 	ld	a,(#_kplayerjumpvelocity + 0)
   45B1 12            [ 7]  209 	ld	(de), a
   45B2                     210 00109$:
                            211 ;src/entities/player.c:42: player->vy = (i8)(player->vy + kplayergravity);
   45B2 1A            [ 7]  212 	ld	a, (de)
   45B3 4F            [ 4]  213 	ld	c, a
   45B4 21 FF 44      [10]  214 	ld	hl,#_kplayergravity + 0
   45B7 46            [ 7]  215 	ld	b, (hl)
   45B8 79            [ 4]  216 	ld	a, c
   45B9 80            [ 4]  217 	add	a, b
   45BA 12            [ 7]  218 	ld	(de), a
                            219 ;src/entities/player.c:44: nextx = (i16)player->x + (i16)player->vx;
   45BB DD 6E FE      [19]  220 	ld	l,-2 (ix)
   45BE DD 66 FF      [19]  221 	ld	h,-1 (ix)
   45C1 4E            [ 7]  222 	ld	c, (hl)
   45C2 06 00         [ 7]  223 	ld	b, #0x00
   45C4 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   45C7 DD 66 FD      [19]  225 	ld	h,-3 (ix)
   45CA 6E            [ 7]  226 	ld	l, (hl)
   45CB 7D            [ 4]  227 	ld	a, l
   45CC 17            [ 4]  228 	rla
   45CD 9F            [ 4]  229 	sbc	a, a
   45CE 67            [ 4]  230 	ld	h, a
   45CF 09            [11]  231 	add	hl, bc
                            232 ;src/entities/player.c:45: if (nextx < 0) {
   45D0 CB 7C         [ 8]  233 	bit	7, h
   45D2 28 03         [12]  234 	jr	Z,00112$
                            235 ;src/entities/player.c:46: nextx = 0;
   45D4 21 00 00      [10]  236 	ld	hl, #0x0000
   45D7                     237 00112$:
                            238 ;src/entities/player.c:48: if (nextx > 76) {
   45D7 3E 4C         [ 7]  239 	ld	a, #0x4c
   45D9 BD            [ 4]  240 	cp	a, l
   45DA 3E 00         [ 7]  241 	ld	a, #0x00
   45DC 9C            [ 4]  242 	sbc	a, h
   45DD E2 E2 45      [10]  243 	jp	PO, 00162$
   45E0 EE 80         [ 7]  244 	xor	a, #0x80
   45E2                     245 00162$:
   45E2 F2 E8 45      [10]  246 	jp	P, 00114$
                            247 ;src/entities/player.c:49: nextx = 76;
   45E5 21 4C 00      [10]  248 	ld	hl, #0x004c
   45E8                     249 00114$:
                            250 ;src/entities/player.c:51: player->x = (u8)nextx;
   45E8 4D            [ 4]  251 	ld	c, l
   45E9 DD 6E FE      [19]  252 	ld	l,-2 (ix)
   45EC DD 66 FF      [19]  253 	ld	h,-1 (ix)
   45EF 71            [ 7]  254 	ld	(hl), c
                            255 ;src/entities/player.c:53: nexty = (i16)player->y + (i16)player->vy;
   45F0 E1            [10]  256 	pop	hl
   45F1 E5            [11]  257 	push	hl
   45F2 4E            [ 7]  258 	ld	c, (hl)
   45F3 06 00         [ 7]  259 	ld	b, #0x00
   45F5 1A            [ 7]  260 	ld	a, (de)
   45F6 6F            [ 4]  261 	ld	l, a
   45F7 17            [ 4]  262 	rla
   45F8 9F            [ 4]  263 	sbc	a, a
   45F9 67            [ 4]  264 	ld	h, a
   45FA 09            [11]  265 	add	hl,bc
   45FB 4D            [ 4]  266 	ld	c, l
   45FC 44            [ 4]  267 	ld	b, h
                            268 ;src/entities/player.c:54: nexty = collision_clamp_y_to_ground(nexty, player->h);
   45FD DD 6E FA      [19]  269 	ld	l,-6 (ix)
   4600 DD 66 FB      [19]  270 	ld	h,-5 (ix)
   4603 66            [ 7]  271 	ld	h, (hl)
   4604 D5            [11]  272 	push	de
   4605 E5            [11]  273 	push	hl
   4606 33            [ 6]  274 	inc	sp
   4607 C5            [11]  275 	push	bc
   4608 CD 8C 40      [17]  276 	call	_collision_clamp_y_to_ground
   460B F1            [10]  277 	pop	af
   460C 33            [ 6]  278 	inc	sp
   460D D1            [10]  279 	pop	de
                            280 ;src/entities/player.c:55: if (nexty < 0) {
   460E CB 7C         [ 8]  281 	bit	7, h
   4610 28 03         [12]  282 	jr	Z,00116$
                            283 ;src/entities/player.c:56: nexty = 0;
   4612 21 00 00      [10]  284 	ld	hl, #0x0000
   4615                     285 00116$:
                            286 ;src/entities/player.c:58: player->y = (u8)nexty;
   4615 4D            [ 4]  287 	ld	c, l
   4616 E1            [10]  288 	pop	hl
   4617 E5            [11]  289 	push	hl
   4618 71            [ 7]  290 	ld	(hl), c
                            291 ;src/entities/player.c:60: if (collision_is_on_ground((i16)player->y, player->h) && player->vy > 0) {
   4619 DD 6E FA      [19]  292 	ld	l,-6 (ix)
   461C DD 66 FB      [19]  293 	ld	h,-5 (ix)
   461F 66            [ 7]  294 	ld	h, (hl)
   4620 06 00         [ 7]  295 	ld	b, #0x00
   4622 D5            [11]  296 	push	de
   4623 E5            [11]  297 	push	hl
   4624 33            [ 6]  298 	inc	sp
   4625 C5            [11]  299 	push	bc
   4626 CD 66 40      [17]  300 	call	_collision_is_on_ground
   4629 F1            [10]  301 	pop	af
   462A 33            [ 6]  302 	inc	sp
   462B D1            [10]  303 	pop	de
   462C 7D            [ 4]  304 	ld	a, l
   462D B7            [ 4]  305 	or	a, a
   462E 28 0E         [12]  306 	jr	Z,00120$
   4630 1A            [ 7]  307 	ld	a, (de)
   4631 4F            [ 4]  308 	ld	c, a
   4632 AF            [ 4]  309 	xor	a, a
   4633 91            [ 4]  310 	sub	a, c
   4634 E2 39 46      [10]  311 	jp	PO, 00163$
   4637 EE 80         [ 7]  312 	xor	a, #0x80
   4639                     313 00163$:
   4639 F2 3E 46      [10]  314 	jp	P, 00120$
                            315 ;src/entities/player.c:61: player->vy = 0;
   463C AF            [ 4]  316 	xor	a, a
   463D 12            [ 7]  317 	ld	(de), a
   463E                     318 00120$:
   463E DD F9         [10]  319 	ld	sp, ix
   4640 DD E1         [14]  320 	pop	ix
   4642 C9            [10]  321 	ret
                            322 ;src/entities/player.c:65: void playerrender(const Player* player) {
                            323 ;	---------------------------------
                            324 ; Function playerrender
                            325 ; ---------------------------------
   4643                     326 _playerrender::
   4643 DD E5         [15]  327 	push	ix
   4645 DD 21 00 00   [14]  328 	ld	ix,#0
   4649 DD 39         [15]  329 	add	ix,sp
                            330 ;src/entities/player.c:68: if (!player) {
   464B DD 7E 05      [19]  331 	ld	a, 5 (ix)
   464E DD B6 04      [19]  332 	or	a,4 (ix)
                            333 ;src/entities/player.c:69: return;
   4651 28 32         [12]  334 	jr	Z,00103$
                            335 ;src/entities/player.c:72: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   4653 DD 5E 04      [19]  336 	ld	e,4 (ix)
   4656 DD 56 05      [19]  337 	ld	d,5 (ix)
   4659 6B            [ 4]  338 	ld	l, e
   465A 62            [ 4]  339 	ld	h, d
   465B 23            [ 6]  340 	inc	hl
   465C 46            [ 7]  341 	ld	b, (hl)
   465D 1A            [ 7]  342 	ld	a, (de)
   465E D5            [11]  343 	push	de
   465F C5            [11]  344 	push	bc
   4660 33            [ 6]  345 	inc	sp
   4661 F5            [11]  346 	push	af
   4662 33            [ 6]  347 	inc	sp
   4663 21 00 C0      [10]  348 	ld	hl, #0xc000
   4666 E5            [11]  349 	push	hl
   4667 CD AC 49      [17]  350 	call	_cpct_getScreenPtr
   466A 4D            [ 4]  351 	ld	c, l
   466B 44            [ 4]  352 	ld	b, h
   466C D1            [10]  353 	pop	de
                            354 ;src/entities/player.c:73: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   466D D5            [11]  355 	push	de
   466E FD E1         [14]  356 	pop	iy
   4670 FD 7E 05      [19]  357 	ld	a, 5 (iy)
   4673 EB            [ 4]  358 	ex	de,hl
   4674 11 04 00      [10]  359 	ld	de, #0x0004
   4677 19            [11]  360 	add	hl, de
   4678 56            [ 7]  361 	ld	d, (hl)
   4679 F5            [11]  362 	push	af
   467A 33            [ 6]  363 	inc	sp
   467B 1E 4F         [ 7]  364 	ld	e, #0x4f
   467D D5            [11]  365 	push	de
   467E C5            [11]  366 	push	bc
   467F CD F3 48      [17]  367 	call	_cpct_drawSolidBox
   4682 F1            [10]  368 	pop	af
   4683 F1            [10]  369 	pop	af
   4684 33            [ 6]  370 	inc	sp
   4685                     371 00103$:
   4685 DD E1         [14]  372 	pop	ix
   4687 C9            [10]  373 	ret
                            374 	.area _CODE
                            375 	.area _INITIALIZER
                            376 	.area _CABS (ABS)
