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
   554C                      57 _playerinit::
                             58 ;src/entities/player.c:15: if (!player) {
   554C 21 03 00      [10]   59 	ld	hl, #2+1
   554F 39            [11]   60 	add	hl, sp
   5550 7E            [ 7]   61 	ld	a, (hl)
   5551 2B            [ 6]   62 	dec	hl
   5552 B6            [ 7]   63 	or	a,(hl)
                             64 ;src/entities/player.c:16: return;
   5553 C8            [11]   65 	ret	Z
                             66 ;src/entities/player.c:19: player->x = 20;
   5554 D1            [10]   67 	pop	de
   5555 C1            [10]   68 	pop	bc
   5556 C5            [11]   69 	push	bc
   5557 D5            [11]   70 	push	de
   5558 3E 14         [ 7]   71 	ld	a, #0x14
   555A 02            [ 7]   72 	ld	(bc), a
                             73 ;src/entities/player.c:20: player->y = 120;
   555B 69            [ 4]   74 	ld	l, c
   555C 60            [ 4]   75 	ld	h, b
   555D 23            [ 6]   76 	inc	hl
   555E 36 78         [10]   77 	ld	(hl), #0x78
                             78 ;src/entities/player.c:21: player->vx = 0;
   5560 59            [ 4]   79 	ld	e, c
   5561 50            [ 4]   80 	ld	d, b
   5562 13            [ 6]   81 	inc	de
   5563 13            [ 6]   82 	inc	de
   5564 AF            [ 4]   83 	xor	a, a
   5565 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/player.c:22: player->vy = 0;
   5566 59            [ 4]   86 	ld	e, c
   5567 50            [ 4]   87 	ld	d, b
   5568 13            [ 6]   88 	inc	de
   5569 13            [ 6]   89 	inc	de
   556A 13            [ 6]   90 	inc	de
   556B AF            [ 4]   91 	xor	a, a
   556C 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/player.c:23: player->w = 4;
   556D 21 04 00      [10]   94 	ld	hl, #0x0004
   5570 09            [11]   95 	add	hl, bc
   5571 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/player.c:24: player->h = 16;
   5573 21 05 00      [10]   98 	ld	hl, #0x0005
   5576 09            [11]   99 	add	hl, bc
   5577 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/player.c:25: player->health = 3;
   5579 21 06 00      [10]  102 	ld	hl, #0x0006
   557C 09            [11]  103 	add	hl, bc
   557D 36 03         [10]  104 	ld	(hl), #0x03
                            105 ;src/entities/player.c:26: player->facing_left = 0;
   557F 21 07 00      [10]  106 	ld	hl, #0x0007
   5582 09            [11]  107 	add	hl, bc
   5583 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/player.c:27: player->jump_hold = 0;
   5585 21 08 00      [10]  110 	ld	hl, #0x0008
   5588 09            [11]  111 	add	hl, bc
   5589 36 00         [10]  112 	ld	(hl), #0x00
   558B C9            [10]  113 	ret
   558C                     114 _kplayermovespeed:
   558C 03                  115 	.db #0x03	;  3
   558D                     116 _kplayeracceleration:
   558D 01                  117 	.db #0x01	;  1
   558E                     118 _kplayerdeceleration:
   558E 01                  119 	.db #0x01	;  1
   558F                     120 _kplayergravity:
   558F 01                  121 	.db #0x01	;  1
   5590                     122 _kplayermaxfall:
   5590 04                  123 	.db #0x04	;  4
   5591                     124 _kplayerjumpvelocity:
   5591 FA                  125 	.db #0xfa	; -6
   5592                     126 _kplayerjumpboost:
   5592 FF                  127 	.db #0xff	; -1
                            128 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            129 ;	---------------------------------
                            130 ; Function playerupdate
                            131 ; ---------------------------------
   5593                     132 _playerupdate::
   5593 DD E5         [15]  133 	push	ix
   5595 DD 21 00 00   [14]  134 	ld	ix,#0
   5599 DD 39         [15]  135 	add	ix,sp
   559B 21 ED FF      [10]  136 	ld	hl, #-19
   559E 39            [11]  137 	add	hl, sp
   559F F9            [ 6]  138 	ld	sp, hl
                            139 ;src/entities/player.c:34: if (!player) {
   55A0 DD 7E 05      [19]  140 	ld	a, 5 (ix)
   55A3 DD B6 04      [19]  141 	or	a,4 (ix)
                            142 ;src/entities/player.c:35: return;
   55A6 CA FC 58      [10]  143 	jp	Z,00141$
                            144 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   55A9 CD 90 4E      [17]  145 	call	_input_is_left_pressed
   55AC 4D            [ 4]  146 	ld	c, l
                            147 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   55AD DD 7E 04      [19]  148 	ld	a, 4 (ix)
   55B0 DD 77 FC      [19]  149 	ld	-4 (ix), a
   55B3 DD 7E 05      [19]  150 	ld	a, 5 (ix)
   55B6 DD 77 FD      [19]  151 	ld	-3 (ix), a
   55B9 DD 7E FC      [19]  152 	ld	a, -4 (ix)
   55BC C6 02         [ 7]  153 	add	a, #0x02
   55BE DD 77 FE      [19]  154 	ld	-2 (ix), a
   55C1 DD 7E FD      [19]  155 	ld	a, -3 (ix)
   55C4 CE 00         [ 7]  156 	adc	a, #0x00
   55C6 DD 77 FF      [19]  157 	ld	-1 (ix), a
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   55C9 DD 7E FC      [19]  159 	ld	a, -4 (ix)
   55CC C6 07         [ 7]  160 	add	a, #0x07
   55CE DD 77 FA      [19]  161 	ld	-6 (ix), a
   55D1 DD 7E FD      [19]  162 	ld	a, -3 (ix)
   55D4 CE 00         [ 7]  163 	adc	a, #0x00
   55D6 DD 77 FB      [19]  164 	ld	-5 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   55D9 79            [ 4]  166 	ld	a, c
   55DA B7            [ 4]  167 	or	a, a
   55DB 28 1E         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   55DD DD 6E FE      [19]  170 	ld	l,-2 (ix)
   55E0 DD 66 FF      [19]  171 	ld	h,-1 (ix)
   55E3 4E            [ 7]  172 	ld	c, (hl)
   55E4 21 8D 55      [10]  173 	ld	hl,#_kplayeracceleration + 0
   55E7 46            [ 7]  174 	ld	b, (hl)
   55E8 79            [ 4]  175 	ld	a, c
   55E9 90            [ 4]  176 	sub	a, b
   55EA DD 6E FE      [19]  177 	ld	l,-2 (ix)
   55ED DD 66 FF      [19]  178 	ld	h,-1 (ix)
   55F0 77            [ 7]  179 	ld	(hl), a
                            180 ;src/entities/player.c:40: player->facing_left = 1;
   55F1 DD 6E FA      [19]  181 	ld	l,-6 (ix)
   55F4 DD 66 FB      [19]  182 	ld	h,-5 (ix)
   55F7 36 01         [10]  183 	ld	(hl), #0x01
   55F9 18 6B         [12]  184 	jr	00117$
   55FB                     185 00116$:
                            186 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   55FB CD 98 4E      [17]  187 	call	_input_is_right_pressed
   55FE 7D            [ 4]  188 	ld	a, l
                            189 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   55FF DD 6E FE      [19]  190 	ld	l,-2 (ix)
   5602 DD 66 FF      [19]  191 	ld	h,-1 (ix)
   5605 4E            [ 7]  192 	ld	c, (hl)
                            193 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   5606 B7            [ 4]  194 	or	a, a
   5607 28 17         [12]  195 	jr	Z,00113$
                            196 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   5609 21 8D 55      [10]  197 	ld	hl,#_kplayeracceleration + 0
   560C 5E            [ 7]  198 	ld	e, (hl)
   560D 79            [ 4]  199 	ld	a, c
   560E 83            [ 4]  200 	add	a, e
   560F DD 6E FE      [19]  201 	ld	l,-2 (ix)
   5612 DD 66 FF      [19]  202 	ld	h,-1 (ix)
   5615 77            [ 7]  203 	ld	(hl), a
                            204 ;src/entities/player.c:43: player->facing_left = 0;
   5616 DD 6E FA      [19]  205 	ld	l,-6 (ix)
   5619 DD 66 FB      [19]  206 	ld	h,-5 (ix)
   561C 36 00         [10]  207 	ld	(hl), #0x00
   561E 18 46         [12]  208 	jr	00117$
   5620                     209 00113$:
                            210 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5620 21 8E 55      [10]  211 	ld	hl,#_kplayerdeceleration + 0
   5623 46            [ 7]  212 	ld	b, (hl)
                            213 ;src/entities/player.c:44: } else if (player->vx > 0) {
   5624 AF            [ 4]  214 	xor	a, a
   5625 91            [ 4]  215 	sub	a, c
   5626 E2 2B 56      [10]  216 	jp	PO, 00223$
   5629 EE 80         [ 7]  217 	xor	a, #0x80
   562B                     218 00223$:
   562B F2 46 56      [10]  219 	jp	P, 00110$
                            220 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   562E 79            [ 4]  221 	ld	a, c
   562F 90            [ 4]  222 	sub	a, b
   5630 4F            [ 4]  223 	ld	c, a
   5631 DD 6E FE      [19]  224 	ld	l,-2 (ix)
   5634 DD 66 FF      [19]  225 	ld	h,-1 (ix)
   5637 71            [ 7]  226 	ld	(hl), c
                            227 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   5638 CB 79         [ 8]  228 	bit	7, c
   563A 28 2A         [12]  229 	jr	Z,00117$
   563C DD 6E FE      [19]  230 	ld	l,-2 (ix)
   563F DD 66 FF      [19]  231 	ld	h,-1 (ix)
   5642 36 00         [10]  232 	ld	(hl), #0x00
   5644 18 20         [12]  233 	jr	00117$
   5646                     234 00110$:
                            235 ;src/entities/player.c:47: } else if (player->vx < 0) {
   5646 CB 79         [ 8]  236 	bit	7, c
   5648 28 1C         [12]  237 	jr	Z,00117$
                            238 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   564A 79            [ 4]  239 	ld	a, c
   564B 80            [ 4]  240 	add	a, b
   564C 4F            [ 4]  241 	ld	c, a
   564D DD 6E FE      [19]  242 	ld	l,-2 (ix)
   5650 DD 66 FF      [19]  243 	ld	h,-1 (ix)
   5653 71            [ 7]  244 	ld	(hl), c
                            245 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   5654 AF            [ 4]  246 	xor	a, a
   5655 91            [ 4]  247 	sub	a, c
   5656 E2 5B 56      [10]  248 	jp	PO, 00224$
   5659 EE 80         [ 7]  249 	xor	a, #0x80
   565B                     250 00224$:
   565B F2 66 56      [10]  251 	jp	P, 00117$
   565E DD 6E FE      [19]  252 	ld	l,-2 (ix)
   5661 DD 66 FF      [19]  253 	ld	h,-1 (ix)
   5664 36 00         [10]  254 	ld	(hl), #0x00
   5666                     255 00117$:
                            256 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5666 DD 6E FE      [19]  257 	ld	l,-2 (ix)
   5669 DD 66 FF      [19]  258 	ld	h,-1 (ix)
   566C 46            [ 7]  259 	ld	b, (hl)
   566D 21 8C 55      [10]  260 	ld	hl,#_kplayermovespeed + 0
   5670 4E            [ 7]  261 	ld	c, (hl)
   5671 79            [ 4]  262 	ld	a, c
   5672 90            [ 4]  263 	sub	a, b
   5673 E2 78 56      [10]  264 	jp	PO, 00225$
   5676 EE 80         [ 7]  265 	xor	a, #0x80
   5678                     266 00225$:
   5678 F2 82 56      [10]  267 	jp	P, 00119$
   567B DD 6E FE      [19]  268 	ld	l,-2 (ix)
   567E DD 66 FF      [19]  269 	ld	h,-1 (ix)
   5681 71            [ 7]  270 	ld	(hl), c
   5682                     271 00119$:
                            272 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5682 DD 6E FE      [19]  273 	ld	l,-2 (ix)
   5685 DD 66 FF      [19]  274 	ld	h,-1 (ix)
   5688 7E            [ 7]  275 	ld	a, (hl)
   5689 DD 77 FA      [19]  276 	ld	-6 (ix), a
   568C 3A 8C 55      [13]  277 	ld	a,(#_kplayermovespeed + 0)
   568F DD 77 F9      [19]  278 	ld	-7 (ix), a
   5692 DD 77 F7      [19]  279 	ld	-9 (ix), a
   5695 DD 7E F9      [19]  280 	ld	a, -7 (ix)
   5698 17            [ 4]  281 	rla
   5699 9F            [ 4]  282 	sbc	a, a
   569A DD 77 F8      [19]  283 	ld	-8 (ix), a
   569D AF            [ 4]  284 	xor	a, a
   569E DD 96 F7      [19]  285 	sub	a, -9 (ix)
   56A1 DD 77 F7      [19]  286 	ld	-9 (ix), a
   56A4 3E 00         [ 7]  287 	ld	a, #0x00
   56A6 DD 9E F8      [19]  288 	sbc	a, -8 (ix)
   56A9 DD 77 F8      [19]  289 	ld	-8 (ix), a
   56AC DD 7E FA      [19]  290 	ld	a, -6 (ix)
   56AF DD 77 FA      [19]  291 	ld	-6 (ix), a
   56B2 17            [ 4]  292 	rla
   56B3 9F            [ 4]  293 	sbc	a, a
   56B4 DD 77 FB      [19]  294 	ld	-5 (ix), a
   56B7 DD 7E FA      [19]  295 	ld	a, -6 (ix)
   56BA DD 96 F7      [19]  296 	sub	a, -9 (ix)
   56BD DD 7E FB      [19]  297 	ld	a, -5 (ix)
   56C0 DD 9E F8      [19]  298 	sbc	a, -8 (ix)
   56C3 E2 C8 56      [10]  299 	jp	PO, 00226$
   56C6 EE 80         [ 7]  300 	xor	a, #0x80
   56C8                     301 00226$:
   56C8 F2 D7 56      [10]  302 	jp	P, 00121$
   56CB AF            [ 4]  303 	xor	a, a
   56CC DD 96 F9      [19]  304 	sub	a, -7 (ix)
   56CF 4F            [ 4]  305 	ld	c, a
   56D0 DD 6E FE      [19]  306 	ld	l,-2 (ix)
   56D3 DD 66 FF      [19]  307 	ld	h,-1 (ix)
   56D6 71            [ 7]  308 	ld	(hl), c
   56D7                     309 00121$:
                            310 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   56D7 CD B8 4E      [17]  311 	call	_input_is_jump_just_pressed
   56DA DD 75 F7      [19]  312 	ld	-9 (ix), l
   56DD DD 7E FC      [19]  313 	ld	a, -4 (ix)
   56E0 C6 05         [ 7]  314 	add	a, #0x05
   56E2 DD 77 FA      [19]  315 	ld	-6 (ix), a
   56E5 DD 7E FD      [19]  316 	ld	a, -3 (ix)
   56E8 CE 00         [ 7]  317 	adc	a, #0x00
   56EA DD 77 FB      [19]  318 	ld	-5 (ix), a
   56ED DD 7E FC      [19]  319 	ld	a, -4 (ix)
   56F0 C6 01         [ 7]  320 	add	a, #0x01
   56F2 DD 77 F5      [19]  321 	ld	-11 (ix), a
   56F5 DD 7E FD      [19]  322 	ld	a, -3 (ix)
   56F8 CE 00         [ 7]  323 	adc	a, #0x00
   56FA DD 77 F6      [19]  324 	ld	-10 (ix), a
                            325 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   56FD DD 7E FC      [19]  326 	ld	a, -4 (ix)
   5700 C6 03         [ 7]  327 	add	a, #0x03
   5702 DD 77 F3      [19]  328 	ld	-13 (ix), a
   5705 DD 7E FD      [19]  329 	ld	a, -3 (ix)
   5708 CE 00         [ 7]  330 	adc	a, #0x00
   570A DD 77 F4      [19]  331 	ld	-12 (ix), a
                            332 ;src/entities/player.c:57: player->jump_hold = 5;
   570D DD 7E FC      [19]  333 	ld	a, -4 (ix)
   5710 C6 08         [ 7]  334 	add	a, #0x08
   5712 DD 77 F1      [19]  335 	ld	-15 (ix), a
   5715 DD 7E FD      [19]  336 	ld	a, -3 (ix)
   5718 CE 00         [ 7]  337 	adc	a, #0x00
   571A DD 77 F2      [19]  338 	ld	-14 (ix), a
                            339 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   571D DD 7E F7      [19]  340 	ld	a, -9 (ix)
   5720 B7            [ 4]  341 	or	a, a
   5721 28 3A         [12]  342 	jr	Z,00123$
   5723 DD 6E FA      [19]  343 	ld	l,-6 (ix)
   5726 DD 66 FB      [19]  344 	ld	h,-5 (ix)
   5729 7E            [ 7]  345 	ld	a, (hl)
   572A DD 6E F5      [19]  346 	ld	l,-11 (ix)
   572D DD 66 F6      [19]  347 	ld	h,-10 (ix)
   5730 4E            [ 7]  348 	ld	c, (hl)
   5731 06 00         [ 7]  349 	ld	b, #0x00
   5733 DD 6E FC      [19]  350 	ld	l,-4 (ix)
   5736 DD 66 FD      [19]  351 	ld	h,-3 (ix)
   5739 5E            [ 7]  352 	ld	e, (hl)
   573A 16 00         [ 7]  353 	ld	d, #0x00
   573C F5            [11]  354 	push	af
   573D 33            [ 6]  355 	inc	sp
   573E C5            [11]  356 	push	bc
   573F D5            [11]  357 	push	de
   5740 CD 62 4A      [17]  358 	call	_collision_is_on_ground_at
   5743 F1            [10]  359 	pop	af
   5744 F1            [10]  360 	pop	af
   5745 33            [ 6]  361 	inc	sp
   5746 7D            [ 4]  362 	ld	a, l
   5747 B7            [ 4]  363 	or	a, a
   5748 28 13         [12]  364 	jr	Z,00123$
                            365 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   574A 21 91 55      [10]  366 	ld	hl,#_kplayerjumpvelocity + 0
   574D 4E            [ 7]  367 	ld	c, (hl)
   574E DD 6E F3      [19]  368 	ld	l,-13 (ix)
   5751 DD 66 F4      [19]  369 	ld	h,-12 (ix)
   5754 71            [ 7]  370 	ld	(hl), c
                            371 ;src/entities/player.c:57: player->jump_hold = 5;
   5755 DD 6E F1      [19]  372 	ld	l,-15 (ix)
   5758 DD 66 F2      [19]  373 	ld	h,-14 (ix)
   575B 36 05         [10]  374 	ld	(hl), #0x05
   575D                     375 00123$:
                            376 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   575D CD B0 4E      [17]  377 	call	_input_is_jump_pressed
   5760 DD 75 F7      [19]  378 	ld	-9 (ix), l
   5763 7D            [ 4]  379 	ld	a, l
   5764 B7            [ 4]  380 	or	a, a
   5765 28 41         [12]  381 	jr	Z,00126$
   5767 DD 6E F1      [19]  382 	ld	l,-15 (ix)
   576A DD 66 F2      [19]  383 	ld	h,-14 (ix)
   576D 7E            [ 7]  384 	ld	a, (hl)
   576E DD 77 F7      [19]  385 	ld	-9 (ix), a
   5771 B7            [ 4]  386 	or	a, a
   5772 28 34         [12]  387 	jr	Z,00126$
   5774 DD 6E F3      [19]  388 	ld	l,-13 (ix)
   5777 DD 66 F4      [19]  389 	ld	h,-12 (ix)
   577A 7E            [ 7]  390 	ld	a, (hl)
   577B DD 77 F7      [19]  391 	ld	-9 (ix), a
   577E DD CB F7 7E   [20]  392 	bit	7, -9 (ix)
   5782 28 24         [12]  393 	jr	Z,00126$
                            394 ;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
   5784 3A 92 55      [13]  395 	ld	a,(#_kplayerjumpboost + 0)
   5787 DD 77 F9      [19]  396 	ld	-7 (ix), a
   578A DD 7E F7      [19]  397 	ld	a, -9 (ix)
   578D DD 86 F9      [19]  398 	add	a, -7 (ix)
   5790 DD 6E F3      [19]  399 	ld	l,-13 (ix)
   5793 DD 66 F4      [19]  400 	ld	h,-12 (ix)
   5796 77            [ 7]  401 	ld	(hl), a
                            402 ;src/entities/player.c:62: player->jump_hold--;
   5797 DD 6E F1      [19]  403 	ld	l,-15 (ix)
   579A DD 66 F2      [19]  404 	ld	h,-14 (ix)
   579D 4E            [ 7]  405 	ld	c, (hl)
   579E 0D            [ 4]  406 	dec	c
   579F DD 6E F1      [19]  407 	ld	l,-15 (ix)
   57A2 DD 66 F2      [19]  408 	ld	h,-14 (ix)
   57A5 71            [ 7]  409 	ld	(hl), c
   57A6 18 08         [12]  410 	jr	00127$
   57A8                     411 00126$:
                            412 ;src/entities/player.c:64: player->jump_hold = 0;
   57A8 DD 6E F1      [19]  413 	ld	l,-15 (ix)
   57AB DD 66 F2      [19]  414 	ld	h,-14 (ix)
   57AE 36 00         [10]  415 	ld	(hl), #0x00
   57B0                     416 00127$:
                            417 ;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
   57B0 DD 6E F3      [19]  418 	ld	l,-13 (ix)
   57B3 DD 66 F4      [19]  419 	ld	h,-12 (ix)
   57B6 4E            [ 7]  420 	ld	c, (hl)
   57B7 21 8F 55      [10]  421 	ld	hl,#_kplayergravity + 0
   57BA 46            [ 7]  422 	ld	b, (hl)
   57BB 79            [ 4]  423 	ld	a, c
   57BC 80            [ 4]  424 	add	a, b
   57BD 4F            [ 4]  425 	ld	c, a
   57BE DD 6E F3      [19]  426 	ld	l,-13 (ix)
   57C1 DD 66 F4      [19]  427 	ld	h,-12 (ix)
   57C4 71            [ 7]  428 	ld	(hl), c
                            429 ;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   57C5 21 90 55      [10]  430 	ld	hl,#_kplayermaxfall + 0
   57C8 46            [ 7]  431 	ld	b, (hl)
   57C9 78            [ 4]  432 	ld	a, b
   57CA 91            [ 4]  433 	sub	a, c
   57CB E2 D0 57      [10]  434 	jp	PO, 00227$
   57CE EE 80         [ 7]  435 	xor	a, #0x80
   57D0                     436 00227$:
   57D0 F2 DA 57      [10]  437 	jp	P, 00131$
   57D3 DD 6E F3      [19]  438 	ld	l,-13 (ix)
   57D6 DD 66 F4      [19]  439 	ld	h,-12 (ix)
   57D9 70            [ 7]  440 	ld	(hl), b
   57DA                     441 00131$:
                            442 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   57DA DD 6E FC      [19]  443 	ld	l,-4 (ix)
   57DD DD 66 FD      [19]  444 	ld	h,-3 (ix)
   57E0 4E            [ 7]  445 	ld	c, (hl)
   57E1 DD 71 F1      [19]  446 	ld	-15 (ix), c
   57E4 DD 36 F2 00   [19]  447 	ld	-14 (ix), #0x00
   57E8 DD 6E FE      [19]  448 	ld	l,-2 (ix)
   57EB DD 66 FF      [19]  449 	ld	h,-1 (ix)
   57EE 7E            [ 7]  450 	ld	a, (hl)
   57EF DD 77 F7      [19]  451 	ld	-9 (ix), a
   57F2 DD 77 F7      [19]  452 	ld	-9 (ix), a
   57F5 17            [ 4]  453 	rla
   57F6 9F            [ 4]  454 	sbc	a, a
   57F7 DD 77 F8      [19]  455 	ld	-8 (ix), a
   57FA DD 7E F7      [19]  456 	ld	a, -9 (ix)
   57FD DD 86 F1      [19]  457 	add	a, -15 (ix)
   5800 DD 77 EF      [19]  458 	ld	-17 (ix), a
   5803 DD 7E F8      [19]  459 	ld	a, -8 (ix)
   5806 DD 8E F2      [19]  460 	adc	a, -14 (ix)
   5809 DD 77 F0      [19]  461 	ld	-16 (ix), a
                            462 ;src/entities/player.c:71: if (nextx < 0) {
   580C DD CB F0 7E   [20]  463 	bit	7, -16 (ix)
   5810 28 08         [12]  464 	jr	Z,00133$
                            465 ;src/entities/player.c:72: nextx = 0;
   5812 DD 36 EF 00   [19]  466 	ld	-17 (ix), #0x00
   5816 DD 36 F0 00   [19]  467 	ld	-16 (ix), #0x00
   581A                     468 00133$:
                            469 ;src/entities/player.c:74: if (nextx > 76) {
   581A 3E 4C         [ 7]  470 	ld	a, #0x4c
   581C DD BE EF      [19]  471 	cp	a, -17 (ix)
   581F 3E 00         [ 7]  472 	ld	a, #0x00
   5821 DD 9E F0      [19]  473 	sbc	a, -16 (ix)
   5824 E2 29 58      [10]  474 	jp	PO, 00228$
   5827 EE 80         [ 7]  475 	xor	a, #0x80
   5829                     476 00228$:
   5829 F2 34 58      [10]  477 	jp	P, 00135$
                            478 ;src/entities/player.c:75: nextx = 76;
   582C DD 36 EF 4C   [19]  479 	ld	-17 (ix), #0x4c
   5830 DD 36 F0 00   [19]  480 	ld	-16 (ix), #0x00
   5834                     481 00135$:
                            482 ;src/entities/player.c:77: player->x = (u8)nextx;
   5834 DD 7E EF      [19]  483 	ld	a, -17 (ix)
   5837 DD 77 F1      [19]  484 	ld	-15 (ix), a
   583A DD 6E FC      [19]  485 	ld	l,-4 (ix)
   583D DD 66 FD      [19]  486 	ld	h,-3 (ix)
   5840 DD 7E F1      [19]  487 	ld	a, -15 (ix)
   5843 77            [ 7]  488 	ld	(hl), a
                            489 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   5844 DD 6E F5      [19]  490 	ld	l,-11 (ix)
   5847 DD 66 F6      [19]  491 	ld	h,-10 (ix)
   584A 4E            [ 7]  492 	ld	c, (hl)
   584B DD 71 F7      [19]  493 	ld	-9 (ix), c
   584E DD 36 F8 00   [19]  494 	ld	-8 (ix), #0x00
   5852 DD 6E F3      [19]  495 	ld	l,-13 (ix)
   5855 DD 66 F4      [19]  496 	ld	h,-12 (ix)
   5858 7E            [ 7]  497 	ld	a, (hl)
   5859 DD 77 FE      [19]  498 	ld	-2 (ix), a
   585C 17            [ 4]  499 	rla
   585D 9F            [ 4]  500 	sbc	a, a
   585E DD 77 FF      [19]  501 	ld	-1 (ix), a
   5861 DD 7E FE      [19]  502 	ld	a, -2 (ix)
   5864 DD 86 F7      [19]  503 	add	a, -9 (ix)
   5867 DD 77 F7      [19]  504 	ld	-9 (ix), a
   586A DD 7E FF      [19]  505 	ld	a, -1 (ix)
   586D DD 8E F8      [19]  506 	adc	a, -8 (ix)
   5870 DD 77 F8      [19]  507 	ld	-8 (ix), a
                            508 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5873 DD 6E FA      [19]  509 	ld	l,-6 (ix)
   5876 DD 66 FB      [19]  510 	ld	h,-5 (ix)
   5879 7E            [ 7]  511 	ld	a, (hl)
   587A DD 77 F9      [19]  512 	ld	-7 (ix), a
   587D DD 7E F1      [19]  513 	ld	a, -15 (ix)
   5880 DD 77 F1      [19]  514 	ld	-15 (ix), a
   5883 DD 36 F2 00   [19]  515 	ld	-14 (ix), #0x00
   5887 DD 7E F9      [19]  516 	ld	a, -7 (ix)
   588A F5            [11]  517 	push	af
   588B 33            [ 6]  518 	inc	sp
   588C DD 6E F7      [19]  519 	ld	l,-9 (ix)
   588F DD 66 F8      [19]  520 	ld	h,-8 (ix)
   5892 E5            [11]  521 	push	hl
   5893 DD 6E F1      [19]  522 	ld	l,-15 (ix)
   5896 DD 66 F2      [19]  523 	ld	h,-14 (ix)
   5899 E5            [11]  524 	push	hl
   589A CD E1 4A      [17]  525 	call	_collision_clamp_y_at
   589D F1            [10]  526 	pop	af
   589E F1            [10]  527 	pop	af
   589F 33            [ 6]  528 	inc	sp
   58A0 DD 74 F2      [19]  529 	ld	-14 (ix), h
   58A3 DD 75 F1      [19]  530 	ld	-15 (ix), l
   58A6 DD 75 ED      [19]  531 	ld	-19 (ix), l
   58A9 DD 7E F2      [19]  532 	ld	a, -14 (ix)
   58AC DD 77 EE      [19]  533 	ld	-18 (ix), a
                            534 ;src/entities/player.c:81: if (nexty < 0) {
   58AF DD CB EE 7E   [20]  535 	bit	7, -18 (ix)
   58B3 28 04         [12]  536 	jr	Z,00137$
                            537 ;src/entities/player.c:82: nexty = 0;
   58B5 21 00 00      [10]  538 	ld	hl, #0x0000
   58B8 E3            [19]  539 	ex	(sp), hl
   58B9                     540 00137$:
                            541 ;src/entities/player.c:84: player->y = (u8)nexty;
   58B9 DD 4E ED      [19]  542 	ld	c, -19 (ix)
   58BC DD 6E F5      [19]  543 	ld	l,-11 (ix)
   58BF DD 66 F6      [19]  544 	ld	h,-10 (ix)
   58C2 71            [ 7]  545 	ld	(hl), c
                            546 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   58C3 DD 6E FA      [19]  547 	ld	l,-6 (ix)
   58C6 DD 66 FB      [19]  548 	ld	h,-5 (ix)
   58C9 7E            [ 7]  549 	ld	a, (hl)
   58CA 06 00         [ 7]  550 	ld	b, #0x00
   58CC DD 6E FC      [19]  551 	ld	l,-4 (ix)
   58CF DD 66 FD      [19]  552 	ld	h,-3 (ix)
   58D2 5E            [ 7]  553 	ld	e, (hl)
   58D3 16 00         [ 7]  554 	ld	d, #0x00
   58D5 F5            [11]  555 	push	af
   58D6 33            [ 6]  556 	inc	sp
   58D7 C5            [11]  557 	push	bc
   58D8 D5            [11]  558 	push	de
   58D9 CD 62 4A      [17]  559 	call	_collision_is_on_ground_at
   58DC F1            [10]  560 	pop	af
   58DD F1            [10]  561 	pop	af
   58DE 33            [ 6]  562 	inc	sp
   58DF 7D            [ 4]  563 	ld	a, l
   58E0 B7            [ 4]  564 	or	a, a
   58E1 28 19         [12]  565 	jr	Z,00141$
   58E3 DD 6E F3      [19]  566 	ld	l,-13 (ix)
   58E6 DD 66 F4      [19]  567 	ld	h,-12 (ix)
   58E9 4E            [ 7]  568 	ld	c, (hl)
   58EA AF            [ 4]  569 	xor	a, a
   58EB 91            [ 4]  570 	sub	a, c
   58EC E2 F1 58      [10]  571 	jp	PO, 00229$
   58EF EE 80         [ 7]  572 	xor	a, #0x80
   58F1                     573 00229$:
   58F1 F2 FC 58      [10]  574 	jp	P, 00141$
                            575 ;src/entities/player.c:87: player->vy = 0;
   58F4 DD 6E F3      [19]  576 	ld	l,-13 (ix)
   58F7 DD 66 F4      [19]  577 	ld	h,-12 (ix)
   58FA 36 00         [10]  578 	ld	(hl), #0x00
   58FC                     579 00141$:
   58FC DD F9         [10]  580 	ld	sp, ix
   58FE DD E1         [14]  581 	pop	ix
   5900 C9            [10]  582 	ret
                            583 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            584 ;	---------------------------------
                            585 ; Function playerrender
                            586 ; ---------------------------------
   5901                     587 _playerrender::
   5901 DD E5         [15]  588 	push	ix
   5903 DD 21 00 00   [14]  589 	ld	ix,#0
   5907 DD 39         [15]  590 	add	ix,sp
                            591 ;src/entities/player.c:94: if (!player) {
   5909 DD 7E 05      [19]  592 	ld	a, 5 (ix)
   590C DD B6 04      [19]  593 	or	a,4 (ix)
                            594 ;src/entities/player.c:95: return;
   590F 28 32         [12]  595 	jr	Z,00103$
                            596 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5911 DD 5E 04      [19]  597 	ld	e,4 (ix)
   5914 DD 56 05      [19]  598 	ld	d,5 (ix)
   5917 6B            [ 4]  599 	ld	l, e
   5918 62            [ 4]  600 	ld	h, d
   5919 23            [ 6]  601 	inc	hl
   591A 46            [ 7]  602 	ld	b, (hl)
   591B 1A            [ 7]  603 	ld	a, (de)
   591C D5            [11]  604 	push	de
   591D C5            [11]  605 	push	bc
   591E 33            [ 6]  606 	inc	sp
   591F F5            [11]  607 	push	af
   5920 33            [ 6]  608 	inc	sp
   5921 21 00 C0      [10]  609 	ld	hl, #0xc000
   5924 E5            [11]  610 	push	hl
   5925 CD 7C 5D      [17]  611 	call	_cpct_getScreenPtr
   5928 4D            [ 4]  612 	ld	c, l
   5929 44            [ 4]  613 	ld	b, h
   592A D1            [10]  614 	pop	de
                            615 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   592B D5            [11]  616 	push	de
   592C FD E1         [14]  617 	pop	iy
   592E FD 7E 05      [19]  618 	ld	a, 5 (iy)
   5931 EB            [ 4]  619 	ex	de,hl
   5932 11 04 00      [10]  620 	ld	de, #0x0004
   5935 19            [11]  621 	add	hl, de
   5936 56            [ 7]  622 	ld	d, (hl)
   5937 F5            [11]  623 	push	af
   5938 33            [ 6]  624 	inc	sp
   5939 1E 4F         [ 7]  625 	ld	e, #0x4f
   593B D5            [11]  626 	push	de
   593C C5            [11]  627 	push	bc
   593D CD C3 5C      [17]  628 	call	_cpct_drawSolidBox
   5940 F1            [10]  629 	pop	af
   5941 F1            [10]  630 	pop	af
   5942 33            [ 6]  631 	inc	sp
   5943                     632 00103$:
   5943 DD E1         [14]  633 	pop	ix
   5945 C9            [10]  634 	ret
                            635 	.area _CODE
                            636 	.area _INITIALIZER
                            637 	.area _CABS (ABS)
