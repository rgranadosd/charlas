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
                             11 	.globl _collision_clamp_y_at
                             12 	.globl _collision_is_on_ground_at
                             13 	.globl _input_is_jump_just_pressed
                             14 	.globl _input_is_jump_pressed
                             15 	.globl _input_is_right_pressed
                             16 	.globl _input_is_left_pressed
                             17 	.globl _cpct_getScreenPtr
                             18 	.globl _cpct_drawSolidBox
                             19 	.globl _playerinit
                             20 	.globl _playerupdate
                             21 	.globl _playerrender
                             22 ;--------------------------------------------------------
                             23 ; special function registers
                             24 ;--------------------------------------------------------
                             25 ;--------------------------------------------------------
                             26 ; ram data
                             27 ;--------------------------------------------------------
                             28 	.area _DATA
                             29 ;--------------------------------------------------------
                             30 ; ram data
                             31 ;--------------------------------------------------------
                             32 	.area _INITIALIZED
                             33 ;--------------------------------------------------------
                             34 ; absolute external ram data
                             35 ;--------------------------------------------------------
                             36 	.area _DABS (ABS)
                             37 ;--------------------------------------------------------
                             38 ; global & static initialisations
                             39 ;--------------------------------------------------------
                             40 	.area _HOME
                             41 	.area _GSINIT
                             42 	.area _GSFINAL
                             43 	.area _GSINIT
                             44 ;--------------------------------------------------------
                             45 ; Home
                             46 ;--------------------------------------------------------
                             47 	.area _HOME
                             48 	.area _HOME
                             49 ;--------------------------------------------------------
                             50 ; code
                             51 ;--------------------------------------------------------
                             52 	.area _CODE
                             53 ;src/entities/player.c:14: void playerinit(Player* player) {
                             54 ;	---------------------------------
                             55 ; Function playerinit
                             56 ; ---------------------------------
   5480                      57 _playerinit::
                             58 ;src/entities/player.c:15: if (!player) {
   5480 21 03 00      [10]   59 	ld	hl, #2+1
   5483 39            [11]   60 	add	hl, sp
   5484 7E            [ 7]   61 	ld	a, (hl)
   5485 2B            [ 6]   62 	dec	hl
   5486 B6            [ 7]   63 	or	a,(hl)
                             64 ;src/entities/player.c:16: return;
   5487 C8            [11]   65 	ret	Z
                             66 ;src/entities/player.c:19: player->x = 20;
   5488 D1            [10]   67 	pop	de
   5489 C1            [10]   68 	pop	bc
   548A C5            [11]   69 	push	bc
   548B D5            [11]   70 	push	de
   548C 3E 14         [ 7]   71 	ld	a, #0x14
   548E 02            [ 7]   72 	ld	(bc), a
                             73 ;src/entities/player.c:20: player->y = 120;
   548F 69            [ 4]   74 	ld	l, c
   5490 60            [ 4]   75 	ld	h, b
   5491 23            [ 6]   76 	inc	hl
   5492 36 78         [10]   77 	ld	(hl), #0x78
                             78 ;src/entities/player.c:21: player->vx = 0;
   5494 59            [ 4]   79 	ld	e, c
   5495 50            [ 4]   80 	ld	d, b
   5496 13            [ 6]   81 	inc	de
   5497 13            [ 6]   82 	inc	de
   5498 AF            [ 4]   83 	xor	a, a
   5499 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/player.c:22: player->vy = 0;
   549A 59            [ 4]   86 	ld	e, c
   549B 50            [ 4]   87 	ld	d, b
   549C 13            [ 6]   88 	inc	de
   549D 13            [ 6]   89 	inc	de
   549E 13            [ 6]   90 	inc	de
   549F AF            [ 4]   91 	xor	a, a
   54A0 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/player.c:23: player->w = 4;
   54A1 21 04 00      [10]   94 	ld	hl, #0x0004
   54A4 09            [11]   95 	add	hl, bc
   54A5 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/player.c:24: player->h = 16;
   54A7 21 05 00      [10]   98 	ld	hl, #0x0005
   54AA 09            [11]   99 	add	hl, bc
   54AB 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/player.c:25: player->health = 3;
   54AD 21 06 00      [10]  102 	ld	hl, #0x0006
   54B0 09            [11]  103 	add	hl, bc
   54B1 36 03         [10]  104 	ld	(hl), #0x03
                            105 ;src/entities/player.c:26: player->facing_left = 0;
   54B3 21 07 00      [10]  106 	ld	hl, #0x0007
   54B6 09            [11]  107 	add	hl, bc
   54B7 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/player.c:27: player->jump_hold = 0;
   54B9 21 08 00      [10]  110 	ld	hl, #0x0008
   54BC 09            [11]  111 	add	hl, bc
   54BD 36 00         [10]  112 	ld	(hl), #0x00
   54BF C9            [10]  113 	ret
   54C0                     114 _kplayermovespeed:
   54C0 03                  115 	.db #0x03	;  3
   54C1                     116 _kplayeracceleration:
   54C1 01                  117 	.db #0x01	;  1
   54C2                     118 _kplayerdeceleration:
   54C2 01                  119 	.db #0x01	;  1
   54C3                     120 _kplayergravity:
   54C3 01                  121 	.db #0x01	;  1
   54C4                     122 _kplayermaxfall:
   54C4 04                  123 	.db #0x04	;  4
   54C5                     124 _kplayerjumpvelocity:
   54C5 FA                  125 	.db #0xfa	; -6
   54C6                     126 _kplayerjumpboost:
   54C6 FF                  127 	.db #0xff	; -1
                            128 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            129 ;	---------------------------------
                            130 ; Function playerupdate
                            131 ; ---------------------------------
   54C7                     132 _playerupdate::
   54C7 DD E5         [15]  133 	push	ix
   54C9 DD 21 00 00   [14]  134 	ld	ix,#0
   54CD DD 39         [15]  135 	add	ix,sp
   54CF 21 ED FF      [10]  136 	ld	hl, #-19
   54D2 39            [11]  137 	add	hl, sp
   54D3 F9            [ 6]  138 	ld	sp, hl
                            139 ;src/entities/player.c:34: if (!player) {
   54D4 DD 7E 05      [19]  140 	ld	a, 5 (ix)
   54D7 DD B6 04      [19]  141 	or	a,4 (ix)
                            142 ;src/entities/player.c:35: return;
   54DA CA 2C 58      [10]  143 	jp	Z,00141$
                            144 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   54DD CD 46 4E      [17]  145 	call	_input_is_left_pressed
   54E0 4D            [ 4]  146 	ld	c, l
                            147 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   54E1 DD 7E 04      [19]  148 	ld	a, 4 (ix)
   54E4 DD 77 FE      [19]  149 	ld	-2 (ix), a
   54E7 DD 7E 05      [19]  150 	ld	a, 5 (ix)
   54EA DD 77 FF      [19]  151 	ld	-1 (ix), a
   54ED DD 7E FE      [19]  152 	ld	a, -2 (ix)
   54F0 C6 02         [ 7]  153 	add	a, #0x02
   54F2 DD 77 FC      [19]  154 	ld	-4 (ix), a
   54F5 DD 7E FF      [19]  155 	ld	a, -1 (ix)
   54F8 CE 00         [ 7]  156 	adc	a, #0x00
   54FA DD 77 FD      [19]  157 	ld	-3 (ix), a
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   54FD DD 7E FE      [19]  159 	ld	a, -2 (ix)
   5500 C6 07         [ 7]  160 	add	a, #0x07
   5502 DD 77 FA      [19]  161 	ld	-6 (ix), a
   5505 DD 7E FF      [19]  162 	ld	a, -1 (ix)
   5508 CE 00         [ 7]  163 	adc	a, #0x00
   550A DD 77 FB      [19]  164 	ld	-5 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   550D 79            [ 4]  166 	ld	a, c
   550E B7            [ 4]  167 	or	a, a
   550F 28 1E         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   5511 DD 6E FC      [19]  170 	ld	l,-4 (ix)
   5514 DD 66 FD      [19]  171 	ld	h,-3 (ix)
   5517 4E            [ 7]  172 	ld	c, (hl)
   5518 21 C1 54      [10]  173 	ld	hl,#_kplayeracceleration + 0
   551B 46            [ 7]  174 	ld	b, (hl)
   551C 79            [ 4]  175 	ld	a, c
   551D 90            [ 4]  176 	sub	a, b
   551E DD 6E FC      [19]  177 	ld	l,-4 (ix)
   5521 DD 66 FD      [19]  178 	ld	h,-3 (ix)
   5524 77            [ 7]  179 	ld	(hl), a
                            180 ;src/entities/player.c:40: player->facing_left = 1;
   5525 DD 6E FA      [19]  181 	ld	l,-6 (ix)
   5528 DD 66 FB      [19]  182 	ld	h,-5 (ix)
   552B 36 01         [10]  183 	ld	(hl), #0x01
   552D 18 6B         [12]  184 	jr	00117$
   552F                     185 00116$:
                            186 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   552F CD 4E 4E      [17]  187 	call	_input_is_right_pressed
   5532 7D            [ 4]  188 	ld	a, l
                            189 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5533 DD 6E FC      [19]  190 	ld	l,-4 (ix)
   5536 DD 66 FD      [19]  191 	ld	h,-3 (ix)
   5539 4E            [ 7]  192 	ld	c, (hl)
                            193 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   553A B7            [ 4]  194 	or	a, a
   553B 28 17         [12]  195 	jr	Z,00113$
                            196 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   553D 21 C1 54      [10]  197 	ld	hl,#_kplayeracceleration + 0
   5540 5E            [ 7]  198 	ld	e, (hl)
   5541 79            [ 4]  199 	ld	a, c
   5542 83            [ 4]  200 	add	a, e
   5543 DD 6E FC      [19]  201 	ld	l,-4 (ix)
   5546 DD 66 FD      [19]  202 	ld	h,-3 (ix)
   5549 77            [ 7]  203 	ld	(hl), a
                            204 ;src/entities/player.c:43: player->facing_left = 0;
   554A DD 6E FA      [19]  205 	ld	l,-6 (ix)
   554D DD 66 FB      [19]  206 	ld	h,-5 (ix)
   5550 36 00         [10]  207 	ld	(hl), #0x00
   5552 18 46         [12]  208 	jr	00117$
   5554                     209 00113$:
                            210 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5554 21 C2 54      [10]  211 	ld	hl,#_kplayerdeceleration + 0
   5557 46            [ 7]  212 	ld	b, (hl)
                            213 ;src/entities/player.c:44: } else if (player->vx > 0) {
   5558 AF            [ 4]  214 	xor	a, a
   5559 91            [ 4]  215 	sub	a, c
   555A E2 5F 55      [10]  216 	jp	PO, 00223$
   555D EE 80         [ 7]  217 	xor	a, #0x80
   555F                     218 00223$:
   555F F2 7A 55      [10]  219 	jp	P, 00110$
                            220 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5562 79            [ 4]  221 	ld	a, c
   5563 90            [ 4]  222 	sub	a, b
   5564 4F            [ 4]  223 	ld	c, a
   5565 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   5568 DD 66 FD      [19]  225 	ld	h,-3 (ix)
   556B 71            [ 7]  226 	ld	(hl), c
                            227 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   556C CB 79         [ 8]  228 	bit	7, c
   556E 28 2A         [12]  229 	jr	Z,00117$
   5570 DD 6E FC      [19]  230 	ld	l,-4 (ix)
   5573 DD 66 FD      [19]  231 	ld	h,-3 (ix)
   5576 36 00         [10]  232 	ld	(hl), #0x00
   5578 18 20         [12]  233 	jr	00117$
   557A                     234 00110$:
                            235 ;src/entities/player.c:47: } else if (player->vx < 0) {
   557A CB 79         [ 8]  236 	bit	7, c
   557C 28 1C         [12]  237 	jr	Z,00117$
                            238 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   557E 79            [ 4]  239 	ld	a, c
   557F 80            [ 4]  240 	add	a, b
   5580 4F            [ 4]  241 	ld	c, a
   5581 DD 6E FC      [19]  242 	ld	l,-4 (ix)
   5584 DD 66 FD      [19]  243 	ld	h,-3 (ix)
   5587 71            [ 7]  244 	ld	(hl), c
                            245 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   5588 AF            [ 4]  246 	xor	a, a
   5589 91            [ 4]  247 	sub	a, c
   558A E2 8F 55      [10]  248 	jp	PO, 00224$
   558D EE 80         [ 7]  249 	xor	a, #0x80
   558F                     250 00224$:
   558F F2 9A 55      [10]  251 	jp	P, 00117$
   5592 DD 6E FC      [19]  252 	ld	l,-4 (ix)
   5595 DD 66 FD      [19]  253 	ld	h,-3 (ix)
   5598 36 00         [10]  254 	ld	(hl), #0x00
   559A                     255 00117$:
                            256 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   559A DD 6E FC      [19]  257 	ld	l,-4 (ix)
   559D DD 66 FD      [19]  258 	ld	h,-3 (ix)
   55A0 46            [ 7]  259 	ld	b, (hl)
   55A1 21 C0 54      [10]  260 	ld	hl,#_kplayermovespeed + 0
   55A4 4E            [ 7]  261 	ld	c, (hl)
   55A5 79            [ 4]  262 	ld	a, c
   55A6 90            [ 4]  263 	sub	a, b
   55A7 E2 AC 55      [10]  264 	jp	PO, 00225$
   55AA EE 80         [ 7]  265 	xor	a, #0x80
   55AC                     266 00225$:
   55AC F2 B6 55      [10]  267 	jp	P, 00119$
   55AF DD 6E FC      [19]  268 	ld	l,-4 (ix)
   55B2 DD 66 FD      [19]  269 	ld	h,-3 (ix)
   55B5 71            [ 7]  270 	ld	(hl), c
   55B6                     271 00119$:
                            272 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   55B6 DD 6E FC      [19]  273 	ld	l,-4 (ix)
   55B9 DD 66 FD      [19]  274 	ld	h,-3 (ix)
   55BC 7E            [ 7]  275 	ld	a, (hl)
   55BD DD 77 FA      [19]  276 	ld	-6 (ix), a
   55C0 3A C0 54      [13]  277 	ld	a,(#_kplayermovespeed + 0)
   55C3 DD 77 F9      [19]  278 	ld	-7 (ix), a
   55C6 DD 77 F7      [19]  279 	ld	-9 (ix), a
   55C9 DD 7E F9      [19]  280 	ld	a, -7 (ix)
   55CC 17            [ 4]  281 	rla
   55CD 9F            [ 4]  282 	sbc	a, a
   55CE DD 77 F8      [19]  283 	ld	-8 (ix), a
   55D1 AF            [ 4]  284 	xor	a, a
   55D2 DD 96 F7      [19]  285 	sub	a, -9 (ix)
   55D5 DD 77 F7      [19]  286 	ld	-9 (ix), a
   55D8 3E 00         [ 7]  287 	ld	a, #0x00
   55DA DD 9E F8      [19]  288 	sbc	a, -8 (ix)
   55DD DD 77 F8      [19]  289 	ld	-8 (ix), a
   55E0 DD 7E FA      [19]  290 	ld	a, -6 (ix)
   55E3 DD 77 FA      [19]  291 	ld	-6 (ix), a
   55E6 17            [ 4]  292 	rla
   55E7 9F            [ 4]  293 	sbc	a, a
   55E8 DD 77 FB      [19]  294 	ld	-5 (ix), a
   55EB DD 7E FA      [19]  295 	ld	a, -6 (ix)
   55EE DD 96 F7      [19]  296 	sub	a, -9 (ix)
   55F1 DD 7E FB      [19]  297 	ld	a, -5 (ix)
   55F4 DD 9E F8      [19]  298 	sbc	a, -8 (ix)
   55F7 E2 FC 55      [10]  299 	jp	PO, 00226$
   55FA EE 80         [ 7]  300 	xor	a, #0x80
   55FC                     301 00226$:
   55FC F2 0B 56      [10]  302 	jp	P, 00121$
   55FF AF            [ 4]  303 	xor	a, a
   5600 DD 96 F9      [19]  304 	sub	a, -7 (ix)
   5603 4F            [ 4]  305 	ld	c, a
   5604 DD 6E FC      [19]  306 	ld	l,-4 (ix)
   5607 DD 66 FD      [19]  307 	ld	h,-3 (ix)
   560A 71            [ 7]  308 	ld	(hl), c
   560B                     309 00121$:
                            310 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   560B CD 6E 4E      [17]  311 	call	_input_is_jump_just_pressed
   560E DD 75 F7      [19]  312 	ld	-9 (ix), l
   5611 DD 7E FE      [19]  313 	ld	a, -2 (ix)
   5614 C6 05         [ 7]  314 	add	a, #0x05
   5616 DD 77 FA      [19]  315 	ld	-6 (ix), a
   5619 DD 7E FF      [19]  316 	ld	a, -1 (ix)
   561C CE 00         [ 7]  317 	adc	a, #0x00
   561E DD 77 FB      [19]  318 	ld	-5 (ix), a
   5621 DD 7E FE      [19]  319 	ld	a, -2 (ix)
   5624 C6 01         [ 7]  320 	add	a, #0x01
   5626 DD 77 F5      [19]  321 	ld	-11 (ix), a
   5629 DD 7E FF      [19]  322 	ld	a, -1 (ix)
   562C CE 00         [ 7]  323 	adc	a, #0x00
   562E DD 77 F6      [19]  324 	ld	-10 (ix), a
                            325 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   5631 DD 7E FE      [19]  326 	ld	a, -2 (ix)
   5634 C6 03         [ 7]  327 	add	a, #0x03
   5636 DD 77 F3      [19]  328 	ld	-13 (ix), a
   5639 DD 7E FF      [19]  329 	ld	a, -1 (ix)
   563C CE 00         [ 7]  330 	adc	a, #0x00
   563E DD 77 F4      [19]  331 	ld	-12 (ix), a
                            332 ;src/entities/player.c:57: player->jump_hold = 5;
   5641 DD 7E FE      [19]  333 	ld	a, -2 (ix)
   5644 C6 08         [ 7]  334 	add	a, #0x08
   5646 DD 77 F1      [19]  335 	ld	-15 (ix), a
   5649 DD 7E FF      [19]  336 	ld	a, -1 (ix)
   564C CE 00         [ 7]  337 	adc	a, #0x00
   564E DD 77 F2      [19]  338 	ld	-14 (ix), a
                            339 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5651 DD 7E F7      [19]  340 	ld	a, -9 (ix)
   5654 B7            [ 4]  341 	or	a, a
   5655 28 3A         [12]  342 	jr	Z,00123$
   5657 DD 6E FA      [19]  343 	ld	l,-6 (ix)
   565A DD 66 FB      [19]  344 	ld	h,-5 (ix)
   565D 7E            [ 7]  345 	ld	a, (hl)
   565E DD 6E F5      [19]  346 	ld	l,-11 (ix)
   5661 DD 66 F6      [19]  347 	ld	h,-10 (ix)
   5664 4E            [ 7]  348 	ld	c, (hl)
   5665 06 00         [ 7]  349 	ld	b, #0x00
   5667 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   566A DD 66 FF      [19]  351 	ld	h,-1 (ix)
   566D 5E            [ 7]  352 	ld	e, (hl)
   566E 16 00         [ 7]  353 	ld	d, #0x00
   5670 F5            [11]  354 	push	af
   5671 33            [ 6]  355 	inc	sp
   5672 C5            [11]  356 	push	bc
   5673 D5            [11]  357 	push	de
   5674 CD 18 4A      [17]  358 	call	_collision_is_on_ground_at
   5677 F1            [10]  359 	pop	af
   5678 F1            [10]  360 	pop	af
   5679 33            [ 6]  361 	inc	sp
   567A 7D            [ 4]  362 	ld	a, l
   567B B7            [ 4]  363 	or	a, a
   567C 28 13         [12]  364 	jr	Z,00123$
                            365 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   567E 21 C5 54      [10]  366 	ld	hl,#_kplayerjumpvelocity + 0
   5681 4E            [ 7]  367 	ld	c, (hl)
   5682 DD 6E F3      [19]  368 	ld	l,-13 (ix)
   5685 DD 66 F4      [19]  369 	ld	h,-12 (ix)
   5688 71            [ 7]  370 	ld	(hl), c
                            371 ;src/entities/player.c:57: player->jump_hold = 5;
   5689 DD 6E F1      [19]  372 	ld	l,-15 (ix)
   568C DD 66 F2      [19]  373 	ld	h,-14 (ix)
   568F 36 05         [10]  374 	ld	(hl), #0x05
   5691                     375 00123$:
                            376 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5691 CD 66 4E      [17]  377 	call	_input_is_jump_pressed
   5694 DD 75 F7      [19]  378 	ld	-9 (ix), l
   5697 7D            [ 4]  379 	ld	a, l
   5698 B7            [ 4]  380 	or	a, a
   5699 28 41         [12]  381 	jr	Z,00126$
   569B DD 6E F1      [19]  382 	ld	l,-15 (ix)
   569E DD 66 F2      [19]  383 	ld	h,-14 (ix)
   56A1 7E            [ 7]  384 	ld	a, (hl)
   56A2 DD 77 F7      [19]  385 	ld	-9 (ix), a
   56A5 B7            [ 4]  386 	or	a, a
   56A6 28 34         [12]  387 	jr	Z,00126$
   56A8 DD 6E F3      [19]  388 	ld	l,-13 (ix)
   56AB DD 66 F4      [19]  389 	ld	h,-12 (ix)
   56AE 7E            [ 7]  390 	ld	a, (hl)
   56AF DD 77 F7      [19]  391 	ld	-9 (ix), a
   56B2 DD CB F7 7E   [20]  392 	bit	7, -9 (ix)
   56B6 28 24         [12]  393 	jr	Z,00126$
                            394 ;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
   56B8 3A C6 54      [13]  395 	ld	a,(#_kplayerjumpboost + 0)
   56BB DD 77 F9      [19]  396 	ld	-7 (ix), a
   56BE DD 7E F7      [19]  397 	ld	a, -9 (ix)
   56C1 DD 86 F9      [19]  398 	add	a, -7 (ix)
   56C4 DD 6E F3      [19]  399 	ld	l,-13 (ix)
   56C7 DD 66 F4      [19]  400 	ld	h,-12 (ix)
   56CA 77            [ 7]  401 	ld	(hl), a
                            402 ;src/entities/player.c:62: player->jump_hold--;
   56CB DD 6E F1      [19]  403 	ld	l,-15 (ix)
   56CE DD 66 F2      [19]  404 	ld	h,-14 (ix)
   56D1 4E            [ 7]  405 	ld	c, (hl)
   56D2 0D            [ 4]  406 	dec	c
   56D3 DD 6E F1      [19]  407 	ld	l,-15 (ix)
   56D6 DD 66 F2      [19]  408 	ld	h,-14 (ix)
   56D9 71            [ 7]  409 	ld	(hl), c
   56DA 18 08         [12]  410 	jr	00127$
   56DC                     411 00126$:
                            412 ;src/entities/player.c:64: player->jump_hold = 0;
   56DC DD 6E F1      [19]  413 	ld	l,-15 (ix)
   56DF DD 66 F2      [19]  414 	ld	h,-14 (ix)
   56E2 36 00         [10]  415 	ld	(hl), #0x00
   56E4                     416 00127$:
                            417 ;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
   56E4 DD 6E F3      [19]  418 	ld	l,-13 (ix)
   56E7 DD 66 F4      [19]  419 	ld	h,-12 (ix)
   56EA 4E            [ 7]  420 	ld	c, (hl)
   56EB 21 C3 54      [10]  421 	ld	hl,#_kplayergravity + 0
   56EE 46            [ 7]  422 	ld	b, (hl)
   56EF 79            [ 4]  423 	ld	a, c
   56F0 80            [ 4]  424 	add	a, b
   56F1 4F            [ 4]  425 	ld	c, a
   56F2 DD 6E F3      [19]  426 	ld	l,-13 (ix)
   56F5 DD 66 F4      [19]  427 	ld	h,-12 (ix)
   56F8 71            [ 7]  428 	ld	(hl), c
                            429 ;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   56F9 21 C4 54      [10]  430 	ld	hl,#_kplayermaxfall + 0
   56FC 46            [ 7]  431 	ld	b, (hl)
   56FD 78            [ 4]  432 	ld	a, b
   56FE 91            [ 4]  433 	sub	a, c
   56FF E2 04 57      [10]  434 	jp	PO, 00227$
   5702 EE 80         [ 7]  435 	xor	a, #0x80
   5704                     436 00227$:
   5704 F2 0E 57      [10]  437 	jp	P, 00131$
   5707 DD 6E F3      [19]  438 	ld	l,-13 (ix)
   570A DD 66 F4      [19]  439 	ld	h,-12 (ix)
   570D 70            [ 7]  440 	ld	(hl), b
   570E                     441 00131$:
                            442 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   570E DD 6E FE      [19]  443 	ld	l,-2 (ix)
   5711 DD 66 FF      [19]  444 	ld	h,-1 (ix)
   5714 4E            [ 7]  445 	ld	c, (hl)
   5715 DD 71 F1      [19]  446 	ld	-15 (ix), c
   5718 DD 36 F2 00   [19]  447 	ld	-14 (ix), #0x00
   571C DD 6E FC      [19]  448 	ld	l,-4 (ix)
   571F DD 66 FD      [19]  449 	ld	h,-3 (ix)
   5722 7E            [ 7]  450 	ld	a, (hl)
   5723 DD 77 F7      [19]  451 	ld	-9 (ix), a
   5726 DD 77 F7      [19]  452 	ld	-9 (ix), a
   5729 17            [ 4]  453 	rla
   572A 9F            [ 4]  454 	sbc	a, a
   572B DD 77 F8      [19]  455 	ld	-8 (ix), a
   572E DD 7E F7      [19]  456 	ld	a, -9 (ix)
   5731 DD 86 F1      [19]  457 	add	a, -15 (ix)
   5734 DD 77 ED      [19]  458 	ld	-19 (ix), a
   5737 DD 7E F8      [19]  459 	ld	a, -8 (ix)
   573A DD 8E F2      [19]  460 	adc	a, -14 (ix)
   573D DD 77 EE      [19]  461 	ld	-18 (ix), a
                            462 ;src/entities/player.c:71: if (nextx < 0) {
   5740 DD CB EE 7E   [20]  463 	bit	7, -18 (ix)
   5744 28 04         [12]  464 	jr	Z,00133$
                            465 ;src/entities/player.c:72: nextx = 0;
   5746 21 00 00      [10]  466 	ld	hl, #0x0000
   5749 E3            [19]  467 	ex	(sp), hl
   574A                     468 00133$:
                            469 ;src/entities/player.c:74: if (nextx > 76) {
   574A 3E 4C         [ 7]  470 	ld	a, #0x4c
   574C DD BE ED      [19]  471 	cp	a, -19 (ix)
   574F 3E 00         [ 7]  472 	ld	a, #0x00
   5751 DD 9E EE      [19]  473 	sbc	a, -18 (ix)
   5754 E2 59 57      [10]  474 	jp	PO, 00228$
   5757 EE 80         [ 7]  475 	xor	a, #0x80
   5759                     476 00228$:
   5759 F2 60 57      [10]  477 	jp	P, 00135$
                            478 ;src/entities/player.c:75: nextx = 76;
   575C 21 4C 00      [10]  479 	ld	hl, #0x004c
   575F E3            [19]  480 	ex	(sp), hl
   5760                     481 00135$:
                            482 ;src/entities/player.c:77: player->x = (u8)nextx;
   5760 DD 7E ED      [19]  483 	ld	a, -19 (ix)
   5763 DD 77 F1      [19]  484 	ld	-15 (ix), a
   5766 DD 6E FE      [19]  485 	ld	l,-2 (ix)
   5769 DD 66 FF      [19]  486 	ld	h,-1 (ix)
   576C DD 7E F1      [19]  487 	ld	a, -15 (ix)
   576F 77            [ 7]  488 	ld	(hl), a
                            489 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   5770 DD 6E F5      [19]  490 	ld	l,-11 (ix)
   5773 DD 66 F6      [19]  491 	ld	h,-10 (ix)
   5776 4E            [ 7]  492 	ld	c, (hl)
   5777 DD 71 F7      [19]  493 	ld	-9 (ix), c
   577A DD 36 F8 00   [19]  494 	ld	-8 (ix), #0x00
   577E DD 6E F3      [19]  495 	ld	l,-13 (ix)
   5781 DD 66 F4      [19]  496 	ld	h,-12 (ix)
   5784 7E            [ 7]  497 	ld	a, (hl)
   5785 DD 77 FC      [19]  498 	ld	-4 (ix), a
   5788 17            [ 4]  499 	rla
   5789 9F            [ 4]  500 	sbc	a, a
   578A DD 77 FD      [19]  501 	ld	-3 (ix), a
   578D DD 7E FC      [19]  502 	ld	a, -4 (ix)
   5790 DD 86 F7      [19]  503 	add	a, -9 (ix)
   5793 DD 77 F7      [19]  504 	ld	-9 (ix), a
   5796 DD 7E FD      [19]  505 	ld	a, -3 (ix)
   5799 DD 8E F8      [19]  506 	adc	a, -8 (ix)
   579C DD 77 F8      [19]  507 	ld	-8 (ix), a
                            508 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   579F DD 6E FA      [19]  509 	ld	l,-6 (ix)
   57A2 DD 66 FB      [19]  510 	ld	h,-5 (ix)
   57A5 7E            [ 7]  511 	ld	a, (hl)
   57A6 DD 77 F9      [19]  512 	ld	-7 (ix), a
   57A9 DD 7E F1      [19]  513 	ld	a, -15 (ix)
   57AC DD 77 F1      [19]  514 	ld	-15 (ix), a
   57AF DD 36 F2 00   [19]  515 	ld	-14 (ix), #0x00
   57B3 DD 7E F9      [19]  516 	ld	a, -7 (ix)
   57B6 F5            [11]  517 	push	af
   57B7 33            [ 6]  518 	inc	sp
   57B8 DD 6E F7      [19]  519 	ld	l,-9 (ix)
   57BB DD 66 F8      [19]  520 	ld	h,-8 (ix)
   57BE E5            [11]  521 	push	hl
   57BF DD 6E F1      [19]  522 	ld	l,-15 (ix)
   57C2 DD 66 F2      [19]  523 	ld	h,-14 (ix)
   57C5 E5            [11]  524 	push	hl
   57C6 CD 97 4A      [17]  525 	call	_collision_clamp_y_at
   57C9 F1            [10]  526 	pop	af
   57CA F1            [10]  527 	pop	af
   57CB 33            [ 6]  528 	inc	sp
   57CC DD 74 F2      [19]  529 	ld	-14 (ix), h
   57CF DD 75 F1      [19]  530 	ld	-15 (ix), l
   57D2 DD 75 EF      [19]  531 	ld	-17 (ix), l
   57D5 DD 7E F2      [19]  532 	ld	a, -14 (ix)
   57D8 DD 77 F0      [19]  533 	ld	-16 (ix), a
                            534 ;src/entities/player.c:81: if (nexty < 0) {
   57DB DD CB F0 7E   [20]  535 	bit	7, -16 (ix)
   57DF 28 08         [12]  536 	jr	Z,00137$
                            537 ;src/entities/player.c:82: nexty = 0;
   57E1 DD 36 EF 00   [19]  538 	ld	-17 (ix), #0x00
   57E5 DD 36 F0 00   [19]  539 	ld	-16 (ix), #0x00
   57E9                     540 00137$:
                            541 ;src/entities/player.c:84: player->y = (u8)nexty;
   57E9 DD 4E EF      [19]  542 	ld	c, -17 (ix)
   57EC DD 6E F5      [19]  543 	ld	l,-11 (ix)
   57EF DD 66 F6      [19]  544 	ld	h,-10 (ix)
   57F2 71            [ 7]  545 	ld	(hl), c
                            546 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   57F3 DD 6E FA      [19]  547 	ld	l,-6 (ix)
   57F6 DD 66 FB      [19]  548 	ld	h,-5 (ix)
   57F9 7E            [ 7]  549 	ld	a, (hl)
   57FA 06 00         [ 7]  550 	ld	b, #0x00
   57FC DD 6E FE      [19]  551 	ld	l,-2 (ix)
   57FF DD 66 FF      [19]  552 	ld	h,-1 (ix)
   5802 5E            [ 7]  553 	ld	e, (hl)
   5803 16 00         [ 7]  554 	ld	d, #0x00
   5805 F5            [11]  555 	push	af
   5806 33            [ 6]  556 	inc	sp
   5807 C5            [11]  557 	push	bc
   5808 D5            [11]  558 	push	de
   5809 CD 18 4A      [17]  559 	call	_collision_is_on_ground_at
   580C F1            [10]  560 	pop	af
   580D F1            [10]  561 	pop	af
   580E 33            [ 6]  562 	inc	sp
   580F 7D            [ 4]  563 	ld	a, l
   5810 B7            [ 4]  564 	or	a, a
   5811 28 19         [12]  565 	jr	Z,00141$
   5813 DD 6E F3      [19]  566 	ld	l,-13 (ix)
   5816 DD 66 F4      [19]  567 	ld	h,-12 (ix)
   5819 4E            [ 7]  568 	ld	c, (hl)
   581A AF            [ 4]  569 	xor	a, a
   581B 91            [ 4]  570 	sub	a, c
   581C E2 21 58      [10]  571 	jp	PO, 00229$
   581F EE 80         [ 7]  572 	xor	a, #0x80
   5821                     573 00229$:
   5821 F2 2C 58      [10]  574 	jp	P, 00141$
                            575 ;src/entities/player.c:87: player->vy = 0;
   5824 DD 6E F3      [19]  576 	ld	l,-13 (ix)
   5827 DD 66 F4      [19]  577 	ld	h,-12 (ix)
   582A 36 00         [10]  578 	ld	(hl), #0x00
   582C                     579 00141$:
   582C DD F9         [10]  580 	ld	sp, ix
   582E DD E1         [14]  581 	pop	ix
   5830 C9            [10]  582 	ret
                            583 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            584 ;	---------------------------------
                            585 ; Function playerrender
                            586 ; ---------------------------------
   5831                     587 _playerrender::
   5831 DD E5         [15]  588 	push	ix
   5833 DD 21 00 00   [14]  589 	ld	ix,#0
   5837 DD 39         [15]  590 	add	ix,sp
                            591 ;src/entities/player.c:94: if (!player) {
   5839 DD 7E 05      [19]  592 	ld	a, 5 (ix)
   583C DD B6 04      [19]  593 	or	a,4 (ix)
                            594 ;src/entities/player.c:95: return;
   583F 28 32         [12]  595 	jr	Z,00103$
                            596 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5841 DD 5E 04      [19]  597 	ld	e,4 (ix)
   5844 DD 56 05      [19]  598 	ld	d,5 (ix)
   5847 6B            [ 4]  599 	ld	l, e
   5848 62            [ 4]  600 	ld	h, d
   5849 23            [ 6]  601 	inc	hl
   584A 46            [ 7]  602 	ld	b, (hl)
   584B 1A            [ 7]  603 	ld	a, (de)
   584C D5            [11]  604 	push	de
   584D C5            [11]  605 	push	bc
   584E 33            [ 6]  606 	inc	sp
   584F F5            [11]  607 	push	af
   5850 33            [ 6]  608 	inc	sp
   5851 21 00 C0      [10]  609 	ld	hl, #0xc000
   5854 E5            [11]  610 	push	hl
   5855 CD B3 5C      [17]  611 	call	_cpct_getScreenPtr
   5858 4D            [ 4]  612 	ld	c, l
   5859 44            [ 4]  613 	ld	b, h
   585A D1            [10]  614 	pop	de
                            615 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   585B D5            [11]  616 	push	de
   585C FD E1         [14]  617 	pop	iy
   585E FD 7E 05      [19]  618 	ld	a, 5 (iy)
   5861 EB            [ 4]  619 	ex	de,hl
   5862 11 04 00      [10]  620 	ld	de, #0x0004
   5865 19            [11]  621 	add	hl, de
   5866 56            [ 7]  622 	ld	d, (hl)
   5867 F5            [11]  623 	push	af
   5868 33            [ 6]  624 	inc	sp
   5869 1E 4F         [ 7]  625 	ld	e, #0x4f
   586B D5            [11]  626 	push	de
   586C C5            [11]  627 	push	bc
   586D CD FA 5B      [17]  628 	call	_cpct_drawSolidBox
   5870 F1            [10]  629 	pop	af
   5871 F1            [10]  630 	pop	af
   5872 33            [ 6]  631 	inc	sp
   5873                     632 00103$:
   5873 DD E1         [14]  633 	pop	ix
   5875 C9            [10]  634 	ret
                            635 	.area _CODE
                            636 	.area _INITIALIZER
                            637 	.area _CABS (ABS)
