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
                             11 	.globl _collision_is_on_ladder
                             12 	.globl _collision_clamp_y_at
                             13 	.globl _collision_is_on_ground_at
                             14 	.globl _input_is_jump_just_pressed
                             15 	.globl _input_is_jump_pressed
                             16 	.globl _input_is_down_pressed
                             17 	.globl _input_is_up_pressed
                             18 	.globl _input_is_right_pressed
                             19 	.globl _input_is_left_pressed
                             20 	.globl _cpct_getScreenPtr
                             21 	.globl _cpct_drawSolidBox
                             22 	.globl _playerinit
                             23 	.globl _playerupdate
                             24 	.globl _playerrender
                             25 ;--------------------------------------------------------
                             26 ; special function registers
                             27 ;--------------------------------------------------------
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _DATA
                             32 ;--------------------------------------------------------
                             33 ; ram data
                             34 ;--------------------------------------------------------
                             35 	.area _INITIALIZED
                             36 ;--------------------------------------------------------
                             37 ; absolute external ram data
                             38 ;--------------------------------------------------------
                             39 	.area _DABS (ABS)
                             40 ;--------------------------------------------------------
                             41 ; global & static initialisations
                             42 ;--------------------------------------------------------
                             43 	.area _HOME
                             44 	.area _GSINIT
                             45 	.area _GSFINAL
                             46 	.area _GSINIT
                             47 ;--------------------------------------------------------
                             48 ; Home
                             49 ;--------------------------------------------------------
                             50 	.area _HOME
                             51 	.area _HOME
                             52 ;--------------------------------------------------------
                             53 ; code
                             54 ;--------------------------------------------------------
                             55 	.area _CODE
                             56 ;src/entities/player.c:14: void playerinit(Player* player) {
                             57 ;	---------------------------------
                             58 ; Function playerinit
                             59 ; ---------------------------------
   55F7                      60 _playerinit::
                             61 ;src/entities/player.c:15: if (!player) {
   55F7 21 03 00      [10]   62 	ld	hl, #2+1
   55FA 39            [11]   63 	add	hl, sp
   55FB 7E            [ 7]   64 	ld	a, (hl)
   55FC 2B            [ 6]   65 	dec	hl
   55FD B6            [ 7]   66 	or	a,(hl)
                             67 ;src/entities/player.c:16: return;
   55FE C8            [11]   68 	ret	Z
                             69 ;src/entities/player.c:19: player->x = 20;
   55FF D1            [10]   70 	pop	de
   5600 C1            [10]   71 	pop	bc
   5601 C5            [11]   72 	push	bc
   5602 D5            [11]   73 	push	de
   5603 3E 14         [ 7]   74 	ld	a, #0x14
   5605 02            [ 7]   75 	ld	(bc), a
                             76 ;src/entities/player.c:20: player->y = 120;
   5606 69            [ 4]   77 	ld	l, c
   5607 60            [ 4]   78 	ld	h, b
   5608 23            [ 6]   79 	inc	hl
   5609 36 78         [10]   80 	ld	(hl), #0x78
                             81 ;src/entities/player.c:21: player->vx = 0;
   560B 59            [ 4]   82 	ld	e, c
   560C 50            [ 4]   83 	ld	d, b
   560D 13            [ 6]   84 	inc	de
   560E 13            [ 6]   85 	inc	de
   560F AF            [ 4]   86 	xor	a, a
   5610 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/player.c:22: player->vy = 0;
   5611 59            [ 4]   89 	ld	e, c
   5612 50            [ 4]   90 	ld	d, b
   5613 13            [ 6]   91 	inc	de
   5614 13            [ 6]   92 	inc	de
   5615 13            [ 6]   93 	inc	de
   5616 AF            [ 4]   94 	xor	a, a
   5617 12            [ 7]   95 	ld	(de), a
                             96 ;src/entities/player.c:23: player->w = 4;
   5618 21 04 00      [10]   97 	ld	hl, #0x0004
   561B 09            [11]   98 	add	hl, bc
   561C 36 04         [10]   99 	ld	(hl), #0x04
                            100 ;src/entities/player.c:24: player->h = 16;
   561E 21 05 00      [10]  101 	ld	hl, #0x0005
   5621 09            [11]  102 	add	hl, bc
   5622 36 10         [10]  103 	ld	(hl), #0x10
                            104 ;src/entities/player.c:25: player->health = 3;
   5624 21 06 00      [10]  105 	ld	hl, #0x0006
   5627 09            [11]  106 	add	hl, bc
   5628 36 03         [10]  107 	ld	(hl), #0x03
                            108 ;src/entities/player.c:26: player->facing_left = 0;
   562A 21 07 00      [10]  109 	ld	hl, #0x0007
   562D 09            [11]  110 	add	hl, bc
   562E 36 00         [10]  111 	ld	(hl), #0x00
                            112 ;src/entities/player.c:27: player->jump_hold = 0;
   5630 21 08 00      [10]  113 	ld	hl, #0x0008
   5633 09            [11]  114 	add	hl, bc
   5634 36 00         [10]  115 	ld	(hl), #0x00
   5636 C9            [10]  116 	ret
   5637                     117 _kplayermovespeed:
   5637 03                  118 	.db #0x03	;  3
   5638                     119 _kplayeracceleration:
   5638 01                  120 	.db #0x01	;  1
   5639                     121 _kplayerdeceleration:
   5639 01                  122 	.db #0x01	;  1
   563A                     123 _kplayergravity:
   563A 01                  124 	.db #0x01	;  1
   563B                     125 _kplayermaxfall:
   563B 04                  126 	.db #0x04	;  4
   563C                     127 _kplayerjumpvelocity:
   563C FA                  128 	.db #0xfa	; -6
   563D                     129 _kplayerjumpboost:
   563D FF                  130 	.db #0xff	; -1
                            131 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            132 ;	---------------------------------
                            133 ; Function playerupdate
                            134 ; ---------------------------------
   563E                     135 _playerupdate::
   563E DD E5         [15]  136 	push	ix
   5640 DD 21 00 00   [14]  137 	ld	ix,#0
   5644 DD 39         [15]  138 	add	ix,sp
   5646 21 F0 FF      [10]  139 	ld	hl, #-16
   5649 39            [11]  140 	add	hl, sp
   564A F9            [ 6]  141 	ld	sp, hl
                            142 ;src/entities/player.c:34: if (!player) {
   564B DD 7E 05      [19]  143 	ld	a, 5 (ix)
   564E DD B6 04      [19]  144 	or	a,4 (ix)
                            145 ;src/entities/player.c:35: return;
   5651 CA CE 59      [10]  146 	jp	Z,00160$
                            147 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   5654 CD 69 4E      [17]  148 	call	_input_is_left_pressed
                            149 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   5657 DD 7E 04      [19]  150 	ld	a, 4 (ix)
   565A DD 77 FC      [19]  151 	ld	-4 (ix), a
   565D DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5660 DD 77 FD      [19]  153 	ld	-3 (ix), a
   5663 DD 4E FC      [19]  154 	ld	c,-4 (ix)
   5666 DD 46 FD      [19]  155 	ld	b,-3 (ix)
   5669 03            [ 6]  156 	inc	bc
   566A 03            [ 6]  157 	inc	bc
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   566B DD 7E FC      [19]  159 	ld	a, -4 (ix)
   566E C6 07         [ 7]  160 	add	a, #0x07
   5670 DD 77 FA      [19]  161 	ld	-6 (ix), a
   5673 DD 7E FD      [19]  162 	ld	a, -3 (ix)
   5676 CE 00         [ 7]  163 	adc	a, #0x00
   5678 DD 77 FB      [19]  164 	ld	-5 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   567B 7D            [ 4]  166 	ld	a, l
   567C B7            [ 4]  167 	or	a, a
   567D 28 13         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   567F 0A            [ 7]  170 	ld	a, (bc)
   5680 5F            [ 4]  171 	ld	e, a
   5681 21 38 56      [10]  172 	ld	hl,#_kplayeracceleration + 0
   5684 56            [ 7]  173 	ld	d, (hl)
   5685 7B            [ 4]  174 	ld	a, e
   5686 92            [ 4]  175 	sub	a, d
   5687 02            [ 7]  176 	ld	(bc), a
                            177 ;src/entities/player.c:40: player->facing_left = 1;
   5688 DD 6E FA      [19]  178 	ld	l,-6 (ix)
   568B DD 66 FB      [19]  179 	ld	h,-5 (ix)
   568E 36 01         [10]  180 	ld	(hl), #0x01
   5690 18 4B         [12]  181 	jr	00117$
   5692                     182 00116$:
                            183 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   5692 C5            [11]  184 	push	bc
   5693 CD 71 4E      [17]  185 	call	_input_is_right_pressed
   5696 55            [ 4]  186 	ld	d, l
   5697 C1            [10]  187 	pop	bc
                            188 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5698 0A            [ 7]  189 	ld	a, (bc)
   5699 5F            [ 4]  190 	ld	e, a
                            191 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   569A 7A            [ 4]  192 	ld	a, d
   569B B7            [ 4]  193 	or	a, a
   569C 28 11         [12]  194 	jr	Z,00113$
                            195 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   569E 21 38 56      [10]  196 	ld	hl,#_kplayeracceleration + 0
   56A1 56            [ 7]  197 	ld	d, (hl)
   56A2 7B            [ 4]  198 	ld	a, e
   56A3 82            [ 4]  199 	add	a, d
   56A4 02            [ 7]  200 	ld	(bc), a
                            201 ;src/entities/player.c:43: player->facing_left = 0;
   56A5 DD 6E FA      [19]  202 	ld	l,-6 (ix)
   56A8 DD 66 FB      [19]  203 	ld	h,-5 (ix)
   56AB 36 00         [10]  204 	ld	(hl), #0x00
   56AD 18 2E         [12]  205 	jr	00117$
   56AF                     206 00113$:
                            207 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   56AF 21 39 56      [10]  208 	ld	hl,#_kplayerdeceleration + 0
   56B2 56            [ 7]  209 	ld	d, (hl)
                            210 ;src/entities/player.c:44: } else if (player->vx > 0) {
   56B3 AF            [ 4]  211 	xor	a, a
   56B4 93            [ 4]  212 	sub	a, e
   56B5 E2 BA 56      [10]  213 	jp	PO, 00278$
   56B8 EE 80         [ 7]  214 	xor	a, #0x80
   56BA                     215 00278$:
   56BA F2 C9 56      [10]  216 	jp	P, 00110$
                            217 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   56BD 7B            [ 4]  218 	ld	a, e
   56BE 92            [ 4]  219 	sub	a, d
   56BF 5F            [ 4]  220 	ld	e,a
   56C0 02            [ 7]  221 	ld	(bc), a
                            222 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   56C1 CB 7B         [ 8]  223 	bit	7, e
   56C3 28 18         [12]  224 	jr	Z,00117$
   56C5 AF            [ 4]  225 	xor	a, a
   56C6 02            [ 7]  226 	ld	(bc), a
   56C7 18 14         [12]  227 	jr	00117$
   56C9                     228 00110$:
                            229 ;src/entities/player.c:47: } else if (player->vx < 0) {
   56C9 CB 7B         [ 8]  230 	bit	7, e
   56CB 28 10         [12]  231 	jr	Z,00117$
                            232 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   56CD 7B            [ 4]  233 	ld	a, e
   56CE 82            [ 4]  234 	add	a, d
   56CF 5F            [ 4]  235 	ld	e,a
   56D0 02            [ 7]  236 	ld	(bc), a
                            237 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   56D1 AF            [ 4]  238 	xor	a, a
   56D2 93            [ 4]  239 	sub	a, e
   56D3 E2 D8 56      [10]  240 	jp	PO, 00279$
   56D6 EE 80         [ 7]  241 	xor	a, #0x80
   56D8                     242 00279$:
   56D8 F2 DD 56      [10]  243 	jp	P, 00117$
   56DB AF            [ 4]  244 	xor	a, a
   56DC 02            [ 7]  245 	ld	(bc), a
   56DD                     246 00117$:
                            247 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   56DD 0A            [ 7]  248 	ld	a, (bc)
   56DE 57            [ 4]  249 	ld	d, a
   56DF 21 37 56      [10]  250 	ld	hl,#_kplayermovespeed + 0
   56E2 5E            [ 7]  251 	ld	e, (hl)
   56E3 7B            [ 4]  252 	ld	a, e
   56E4 92            [ 4]  253 	sub	a, d
   56E5 E2 EA 56      [10]  254 	jp	PO, 00280$
   56E8 EE 80         [ 7]  255 	xor	a, #0x80
   56EA                     256 00280$:
   56EA F2 EF 56      [10]  257 	jp	P, 00119$
   56ED 7B            [ 4]  258 	ld	a, e
   56EE 02            [ 7]  259 	ld	(bc), a
   56EF                     260 00119$:
                            261 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   56EF 0A            [ 7]  262 	ld	a, (bc)
   56F0 57            [ 4]  263 	ld	d, a
   56F1 21 37 56      [10]  264 	ld	hl,#_kplayermovespeed + 0
   56F4 5E            [ 7]  265 	ld	e, (hl)
   56F5 7B            [ 4]  266 	ld	a,e
   56F6 6F            [ 4]  267 	ld	l,a
   56F7 17            [ 4]  268 	rla
   56F8 9F            [ 4]  269 	sbc	a, a
   56F9 67            [ 4]  270 	ld	h, a
   56FA AF            [ 4]  271 	xor	a, a
   56FB 95            [ 4]  272 	sub	a, l
   56FC DD 77 FA      [19]  273 	ld	-6 (ix), a
   56FF 3E 00         [ 7]  274 	ld	a, #0x00
   5701 9C            [ 4]  275 	sbc	a, h
   5702 DD 77 FB      [19]  276 	ld	-5 (ix), a
   5705 7A            [ 4]  277 	ld	a, d
   5706 17            [ 4]  278 	rla
   5707 9F            [ 4]  279 	sbc	a, a
   5708 6F            [ 4]  280 	ld	l, a
   5709 7A            [ 4]  281 	ld	a, d
   570A DD 96 FA      [19]  282 	sub	a, -6 (ix)
   570D 7D            [ 4]  283 	ld	a, l
   570E DD 9E FB      [19]  284 	sbc	a, -5 (ix)
   5711 E2 16 57      [10]  285 	jp	PO, 00281$
   5714 EE 80         [ 7]  286 	xor	a, #0x80
   5716                     287 00281$:
   5716 F2 1C 57      [10]  288 	jp	P, 00121$
   5719 AF            [ 4]  289 	xor	a, a
   571A 93            [ 4]  290 	sub	a, e
   571B 02            [ 7]  291 	ld	(bc), a
   571C                     292 00121$:
                            293 ;src/entities/player.c:55: player->on_ladder = collision_is_on_ladder((i16)player->x, (i16)player->y, player->w, player->h);
   571C DD 7E FC      [19]  294 	ld	a, -4 (ix)
   571F C6 09         [ 7]  295 	add	a, #0x09
   5721 DD 77 FA      [19]  296 	ld	-6 (ix), a
   5724 DD 7E FD      [19]  297 	ld	a, -3 (ix)
   5727 CE 00         [ 7]  298 	adc	a, #0x00
   5729 DD 77 FB      [19]  299 	ld	-5 (ix), a
   572C DD 7E FC      [19]  300 	ld	a, -4 (ix)
   572F C6 05         [ 7]  301 	add	a, #0x05
   5731 DD 77 F8      [19]  302 	ld	-8 (ix), a
   5734 DD 7E FD      [19]  303 	ld	a, -3 (ix)
   5737 CE 00         [ 7]  304 	adc	a, #0x00
   5739 DD 77 F9      [19]  305 	ld	-7 (ix), a
   573C DD 6E F8      [19]  306 	ld	l,-8 (ix)
   573F DD 66 F9      [19]  307 	ld	h,-7 (ix)
   5742 56            [ 7]  308 	ld	d, (hl)
   5743 DD 6E FC      [19]  309 	ld	l,-4 (ix)
   5746 DD 66 FD      [19]  310 	ld	h,-3 (ix)
   5749 23            [ 6]  311 	inc	hl
   574A 23            [ 6]  312 	inc	hl
   574B 23            [ 6]  313 	inc	hl
   574C 23            [ 6]  314 	inc	hl
   574D 5E            [ 7]  315 	ld	e, (hl)
   574E DD 7E FC      [19]  316 	ld	a, -4 (ix)
   5751 C6 01         [ 7]  317 	add	a, #0x01
   5753 DD 77 F6      [19]  318 	ld	-10 (ix), a
   5756 DD 7E FD      [19]  319 	ld	a, -3 (ix)
   5759 CE 00         [ 7]  320 	adc	a, #0x00
   575B DD 77 F7      [19]  321 	ld	-9 (ix), a
   575E DD 6E F6      [19]  322 	ld	l,-10 (ix)
   5761 DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5764 6E            [ 7]  324 	ld	l, (hl)
   5765 DD 75 FE      [19]  325 	ld	-2 (ix), l
   5768 DD 36 FF 00   [19]  326 	ld	-1 (ix), #0x00
   576C DD 6E FC      [19]  327 	ld	l,-4 (ix)
   576F DD 66 FD      [19]  328 	ld	h,-3 (ix)
   5772 6E            [ 7]  329 	ld	l, (hl)
   5773 DD 75 F4      [19]  330 	ld	-12 (ix), l
   5776 DD 36 F5 00   [19]  331 	ld	-11 (ix), #0x00
   577A C5            [11]  332 	push	bc
   577B D5            [11]  333 	push	de
   577C DD 6E FE      [19]  334 	ld	l,-2 (ix)
   577F DD 66 FF      [19]  335 	ld	h,-1 (ix)
   5782 E5            [11]  336 	push	hl
   5783 DD 6E F4      [19]  337 	ld	l,-12 (ix)
   5786 DD 66 F5      [19]  338 	ld	h,-11 (ix)
   5789 E5            [11]  339 	push	hl
   578A CD 76 4B      [17]  340 	call	_collision_is_on_ladder
   578D F1            [10]  341 	pop	af
   578E F1            [10]  342 	pop	af
   578F F1            [10]  343 	pop	af
   5790 5D            [ 4]  344 	ld	e, l
   5791 C1            [10]  345 	pop	bc
   5792 DD 6E FA      [19]  346 	ld	l,-6 (ix)
   5795 DD 66 FB      [19]  347 	ld	h,-5 (ix)
   5798 73            [ 7]  348 	ld	(hl), e
                            349 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5799 DD 7E FC      [19]  350 	ld	a, -4 (ix)
   579C C6 03         [ 7]  351 	add	a, #0x03
   579E DD 77 F4      [19]  352 	ld	-12 (ix), a
   57A1 DD 7E FD      [19]  353 	ld	a, -3 (ix)
   57A4 CE 00         [ 7]  354 	adc	a, #0x00
   57A6 DD 77 F5      [19]  355 	ld	-11 (ix), a
                            356 ;src/entities/player.c:59: player->jump_hold = 5;
   57A9 DD 7E FC      [19]  357 	ld	a, -4 (ix)
   57AC C6 08         [ 7]  358 	add	a, #0x08
   57AE DD 77 FE      [19]  359 	ld	-2 (ix), a
   57B1 DD 7E FD      [19]  360 	ld	a, -3 (ix)
   57B4 CE 00         [ 7]  361 	adc	a, #0x00
   57B6 DD 77 FF      [19]  362 	ld	-1 (ix), a
                            363 ;src/entities/player.c:57: if (!player->on_ladder && input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57B9 7B            [ 4]  364 	ld	a, e
   57BA B7            [ 4]  365 	or	a, a
   57BB 20 50         [12]  366 	jr	NZ,00123$
   57BD C5            [11]  367 	push	bc
   57BE CD 91 4E      [17]  368 	call	_input_is_jump_just_pressed
   57C1 C1            [10]  369 	pop	bc
   57C2 7D            [ 4]  370 	ld	a, l
   57C3 B7            [ 4]  371 	or	a, a
   57C4 28 47         [12]  372 	jr	Z,00123$
   57C6 DD 6E F8      [19]  373 	ld	l,-8 (ix)
   57C9 DD 66 F9      [19]  374 	ld	h,-7 (ix)
   57CC 7E            [ 7]  375 	ld	a, (hl)
   57CD DD 6E F6      [19]  376 	ld	l,-10 (ix)
   57D0 DD 66 F7      [19]  377 	ld	h,-9 (ix)
   57D3 5E            [ 7]  378 	ld	e, (hl)
   57D4 16 00         [ 7]  379 	ld	d, #0x00
   57D6 DD 6E FC      [19]  380 	ld	l,-4 (ix)
   57D9 DD 66 FD      [19]  381 	ld	h,-3 (ix)
   57DC 6E            [ 7]  382 	ld	l, (hl)
   57DD DD 75 F2      [19]  383 	ld	-14 (ix), l
   57E0 DD 36 F3 00   [19]  384 	ld	-13 (ix), #0x00
   57E4 C5            [11]  385 	push	bc
   57E5 F5            [11]  386 	push	af
   57E6 33            [ 6]  387 	inc	sp
   57E7 D5            [11]  388 	push	de
   57E8 DD 6E F2      [19]  389 	ld	l,-14 (ix)
   57EB DD 66 F3      [19]  390 	ld	h,-13 (ix)
   57EE E5            [11]  391 	push	hl
   57EF CD 3B 4A      [17]  392 	call	_collision_is_on_ground_at
   57F2 F1            [10]  393 	pop	af
   57F3 F1            [10]  394 	pop	af
   57F4 33            [ 6]  395 	inc	sp
   57F5 C1            [10]  396 	pop	bc
   57F6 7D            [ 4]  397 	ld	a, l
   57F7 B7            [ 4]  398 	or	a, a
   57F8 28 13         [12]  399 	jr	Z,00123$
                            400 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   57FA 21 3C 56      [10]  401 	ld	hl,#_kplayerjumpvelocity + 0
   57FD 5E            [ 7]  402 	ld	e, (hl)
   57FE DD 6E F4      [19]  403 	ld	l,-12 (ix)
   5801 DD 66 F5      [19]  404 	ld	h,-11 (ix)
   5804 73            [ 7]  405 	ld	(hl), e
                            406 ;src/entities/player.c:59: player->jump_hold = 5;
   5805 DD 6E FE      [19]  407 	ld	l,-2 (ix)
   5808 DD 66 FF      [19]  408 	ld	h,-1 (ix)
   580B 36 05         [10]  409 	ld	(hl), #0x05
   580D                     410 00123$:
                            411 ;src/entities/player.c:62: if (!player->on_ladder && input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   580D DD 6E FA      [19]  412 	ld	l,-6 (ix)
   5810 DD 66 FB      [19]  413 	ld	h,-5 (ix)
   5813 7E            [ 7]  414 	ld	a, (hl)
   5814 B7            [ 4]  415 	or	a, a
   5815 20 3C         [12]  416 	jr	NZ,00127$
   5817 C5            [11]  417 	push	bc
   5818 CD 89 4E      [17]  418 	call	_input_is_jump_pressed
   581B C1            [10]  419 	pop	bc
   581C 7D            [ 4]  420 	ld	a, l
   581D B7            [ 4]  421 	or	a, a
   581E 28 33         [12]  422 	jr	Z,00127$
   5820 DD 6E FE      [19]  423 	ld	l,-2 (ix)
   5823 DD 66 FF      [19]  424 	ld	h,-1 (ix)
   5826 7E            [ 7]  425 	ld	a, (hl)
   5827 B7            [ 4]  426 	or	a, a
   5828 28 29         [12]  427 	jr	Z,00127$
   582A DD 6E F4      [19]  428 	ld	l,-12 (ix)
   582D DD 66 F5      [19]  429 	ld	h,-11 (ix)
   5830 5E            [ 7]  430 	ld	e, (hl)
   5831 CB 7B         [ 8]  431 	bit	7, e
   5833 28 1E         [12]  432 	jr	Z,00127$
                            433 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   5835 21 3D 56      [10]  434 	ld	hl,#_kplayerjumpboost + 0
   5838 56            [ 7]  435 	ld	d, (hl)
   5839 7B            [ 4]  436 	ld	a, e
   583A 82            [ 4]  437 	add	a, d
   583B DD 6E F4      [19]  438 	ld	l,-12 (ix)
   583E DD 66 F5      [19]  439 	ld	h,-11 (ix)
   5841 77            [ 7]  440 	ld	(hl), a
                            441 ;src/entities/player.c:64: player->jump_hold--;
   5842 DD 6E FE      [19]  442 	ld	l,-2 (ix)
   5845 DD 66 FF      [19]  443 	ld	h,-1 (ix)
   5848 5E            [ 7]  444 	ld	e, (hl)
   5849 1D            [ 4]  445 	dec	e
   584A DD 6E FE      [19]  446 	ld	l,-2 (ix)
   584D DD 66 FF      [19]  447 	ld	h,-1 (ix)
   5850 73            [ 7]  448 	ld	(hl), e
   5851 18 08         [12]  449 	jr	00128$
   5853                     450 00127$:
                            451 ;src/entities/player.c:66: player->jump_hold = 0;
   5853 DD 6E FE      [19]  452 	ld	l,-2 (ix)
   5856 DD 66 FF      [19]  453 	ld	h,-1 (ix)
   5859 36 00         [10]  454 	ld	(hl), #0x00
   585B                     455 00128$:
                            456 ;src/entities/player.c:69: if (player->on_ladder) {
   585B DD 6E FA      [19]  457 	ld	l,-6 (ix)
   585E DD 66 FB      [19]  458 	ld	h,-5 (ix)
   5861 7E            [ 7]  459 	ld	a, (hl)
   5862 B7            [ 4]  460 	or	a, a
   5863 28 30         [12]  461 	jr	Z,00141$
                            462 ;src/entities/player.c:70: if (input_is_up_pressed()) {
   5865 C5            [11]  463 	push	bc
   5866 CD 79 4E      [17]  464 	call	_input_is_up_pressed
   5869 C1            [10]  465 	pop	bc
   586A 7D            [ 4]  466 	ld	a, l
   586B B7            [ 4]  467 	or	a, a
   586C 28 0A         [12]  468 	jr	Z,00136$
                            469 ;src/entities/player.c:71: player->vy = -2;
   586E DD 6E F4      [19]  470 	ld	l,-12 (ix)
   5871 DD 66 F5      [19]  471 	ld	h,-11 (ix)
   5874 36 FE         [10]  472 	ld	(hl), #0xfe
   5876 18 47         [12]  473 	jr	00142$
   5878                     474 00136$:
                            475 ;src/entities/player.c:72: } else if (input_is_down_pressed()) {
   5878 C5            [11]  476 	push	bc
   5879 CD 81 4E      [17]  477 	call	_input_is_down_pressed
   587C C1            [10]  478 	pop	bc
   587D 7D            [ 4]  479 	ld	a, l
   587E B7            [ 4]  480 	or	a, a
   587F 28 0A         [12]  481 	jr	Z,00133$
                            482 ;src/entities/player.c:73: player->vy = 2;
   5881 DD 6E F4      [19]  483 	ld	l,-12 (ix)
   5884 DD 66 F5      [19]  484 	ld	h,-11 (ix)
   5887 36 02         [10]  485 	ld	(hl), #0x02
   5889 18 34         [12]  486 	jr	00142$
   588B                     487 00133$:
                            488 ;src/entities/player.c:75: player->vy = 0;
   588B DD 6E F4      [19]  489 	ld	l,-12 (ix)
   588E DD 66 F5      [19]  490 	ld	h,-11 (ix)
   5891 36 00         [10]  491 	ld	(hl), #0x00
   5893 18 2A         [12]  492 	jr	00142$
   5895                     493 00141$:
                            494 ;src/entities/player.c:78: player->vy = (i8)(player->vy + kplayergravity);
   5895 DD 6E F4      [19]  495 	ld	l,-12 (ix)
   5898 DD 66 F5      [19]  496 	ld	h,-11 (ix)
   589B 5E            [ 7]  497 	ld	e, (hl)
   589C 21 3A 56      [10]  498 	ld	hl,#_kplayergravity + 0
   589F 56            [ 7]  499 	ld	d, (hl)
   58A0 7B            [ 4]  500 	ld	a, e
   58A1 82            [ 4]  501 	add	a, d
   58A2 57            [ 4]  502 	ld	d, a
   58A3 DD 6E F4      [19]  503 	ld	l,-12 (ix)
   58A6 DD 66 F5      [19]  504 	ld	h,-11 (ix)
   58A9 72            [ 7]  505 	ld	(hl), d
                            506 ;src/entities/player.c:79: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58AA 21 3B 56      [10]  507 	ld	hl,#_kplayermaxfall + 0
   58AD 5E            [ 7]  508 	ld	e, (hl)
   58AE 7B            [ 4]  509 	ld	a, e
   58AF 92            [ 4]  510 	sub	a, d
   58B0 E2 B5 58      [10]  511 	jp	PO, 00282$
   58B3 EE 80         [ 7]  512 	xor	a, #0x80
   58B5                     513 00282$:
   58B5 F2 BF 58      [10]  514 	jp	P, 00142$
   58B8 DD 6E F4      [19]  515 	ld	l,-12 (ix)
   58BB DD 66 F5      [19]  516 	ld	h,-11 (ix)
   58BE 73            [ 7]  517 	ld	(hl), e
   58BF                     518 00142$:
                            519 ;src/entities/player.c:82: nextx = (i16)player->x + (i16)player->vx;
   58BF DD 6E FC      [19]  520 	ld	l,-4 (ix)
   58C2 DD 66 FD      [19]  521 	ld	h,-3 (ix)
   58C5 5E            [ 7]  522 	ld	e, (hl)
   58C6 16 00         [ 7]  523 	ld	d, #0x00
   58C8 0A            [ 7]  524 	ld	a, (bc)
   58C9 6F            [ 4]  525 	ld	l, a
   58CA 17            [ 4]  526 	rla
   58CB 9F            [ 4]  527 	sbc	a, a
   58CC 67            [ 4]  528 	ld	h, a
   58CD 19            [11]  529 	add	hl, de
                            530 ;src/entities/player.c:83: if (nextx < 0) {
   58CE CB 7C         [ 8]  531 	bit	7, h
   58D0 28 03         [12]  532 	jr	Z,00144$
                            533 ;src/entities/player.c:84: nextx = 0;
   58D2 21 00 00      [10]  534 	ld	hl, #0x0000
   58D5                     535 00144$:
                            536 ;src/entities/player.c:86: if (nextx > 76) {
   58D5 3E 4C         [ 7]  537 	ld	a, #0x4c
   58D7 BD            [ 4]  538 	cp	a, l
   58D8 3E 00         [ 7]  539 	ld	a, #0x00
   58DA 9C            [ 4]  540 	sbc	a, h
   58DB E2 E0 58      [10]  541 	jp	PO, 00283$
   58DE EE 80         [ 7]  542 	xor	a, #0x80
   58E0                     543 00283$:
   58E0 F2 E6 58      [10]  544 	jp	P, 00146$
                            545 ;src/entities/player.c:87: nextx = 76;
   58E3 21 4C 00      [10]  546 	ld	hl, #0x004c
   58E6                     547 00146$:
                            548 ;src/entities/player.c:89: player->x = (u8)nextx;
   58E6 4D            [ 4]  549 	ld	c, l
   58E7 DD 6E FC      [19]  550 	ld	l,-4 (ix)
   58EA DD 66 FD      [19]  551 	ld	h,-3 (ix)
   58ED 71            [ 7]  552 	ld	(hl), c
                            553 ;src/entities/player.c:91: nexty = (i16)player->y + (i16)player->vy;
   58EE DD 6E F6      [19]  554 	ld	l,-10 (ix)
   58F1 DD 66 F7      [19]  555 	ld	h,-9 (ix)
   58F4 4E            [ 7]  556 	ld	c, (hl)
   58F5 06 00         [ 7]  557 	ld	b, #0x00
   58F7 DD 6E F4      [19]  558 	ld	l,-12 (ix)
   58FA DD 66 F5      [19]  559 	ld	h,-11 (ix)
   58FD 6E            [ 7]  560 	ld	l, (hl)
   58FE 7D            [ 4]  561 	ld	a, l
   58FF 17            [ 4]  562 	rla
   5900 9F            [ 4]  563 	sbc	a, a
   5901 67            [ 4]  564 	ld	h, a
   5902 09            [11]  565 	add	hl, bc
   5903 33            [ 6]  566 	inc	sp
   5904 33            [ 6]  567 	inc	sp
   5905 E5            [11]  568 	push	hl
                            569 ;src/entities/player.c:92: if (player->on_ladder) {
   5906 DD 6E FA      [19]  570 	ld	l,-6 (ix)
   5909 DD 66 FB      [19]  571 	ld	h,-5 (ix)
   590C 4E            [ 7]  572 	ld	c, (hl)
                            573 ;src/entities/player.c:55: player->on_ladder = collision_is_on_ladder((i16)player->x, (i16)player->y, player->w, player->h);
   590D DD 6E F8      [19]  574 	ld	l,-8 (ix)
   5910 DD 66 F9      [19]  575 	ld	h,-7 (ix)
   5913 7E            [ 7]  576 	ld	a, (hl)
   5914 DD 77 F2      [19]  577 	ld	-14 (ix), a
                            578 ;src/entities/player.c:92: if (player->on_ladder) {
   5917 79            [ 4]  579 	ld	a, c
   5918 B7            [ 4]  580 	or	a, a
   5919 28 35         [12]  581 	jr	Z,00152$
                            582 ;src/entities/player.c:93: if (nexty < 40) nexty = 40;
   591B DD 7E F0      [19]  583 	ld	a, -16 (ix)
   591E D6 28         [ 7]  584 	sub	a, #0x28
   5920 DD 7E F1      [19]  585 	ld	a, -15 (ix)
   5923 17            [ 4]  586 	rla
   5924 3F            [ 4]  587 	ccf
   5925 1F            [ 4]  588 	rra
   5926 DE 80         [ 7]  589 	sbc	a, #0x80
   5928 30 04         [12]  590 	jr	NC,00148$
   592A 21 28 00      [10]  591 	ld	hl, #0x0028
   592D E3            [19]  592 	ex	(sp), hl
   592E                     593 00148$:
                            594 ;src/entities/player.c:94: if (nexty > 160 - player->h) nexty = 160 - player->h;
   592E DD 4E F2      [19]  595 	ld	c, -14 (ix)
   5931 06 00         [ 7]  596 	ld	b, #0x00
   5933 3E A0         [ 7]  597 	ld	a, #0xa0
   5935 91            [ 4]  598 	sub	a, c
   5936 4F            [ 4]  599 	ld	c, a
   5937 3E 00         [ 7]  600 	ld	a, #0x00
   5939 98            [ 4]  601 	sbc	a, b
   593A 47            [ 4]  602 	ld	b, a
   593B 79            [ 4]  603 	ld	a, c
   593C DD 96 F0      [19]  604 	sub	a, -16 (ix)
   593F 78            [ 4]  605 	ld	a, b
   5940 DD 9E F1      [19]  606 	sbc	a, -15 (ix)
   5943 E2 48 59      [10]  607 	jp	PO, 00284$
   5946 EE 80         [ 7]  608 	xor	a, #0x80
   5948                     609 00284$:
   5948 F2 6F 59      [10]  610 	jp	P, 00153$
   594B 33            [ 6]  611 	inc	sp
   594C 33            [ 6]  612 	inc	sp
   594D C5            [11]  613 	push	bc
   594E 18 1F         [12]  614 	jr	00153$
   5950                     615 00152$:
                            616 ;src/entities/player.c:96: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5950 DD 6E FC      [19]  617 	ld	l,-4 (ix)
   5953 DD 66 FD      [19]  618 	ld	h,-3 (ix)
   5956 4E            [ 7]  619 	ld	c, (hl)
   5957 06 00         [ 7]  620 	ld	b, #0x00
   5959 DD 7E F2      [19]  621 	ld	a, -14 (ix)
   595C F5            [11]  622 	push	af
   595D 33            [ 6]  623 	inc	sp
   595E DD 6E F0      [19]  624 	ld	l,-16 (ix)
   5961 DD 66 F1      [19]  625 	ld	h,-15 (ix)
   5964 E5            [11]  626 	push	hl
   5965 C5            [11]  627 	push	bc
   5966 CD BA 4A      [17]  628 	call	_collision_clamp_y_at
   5969 F1            [10]  629 	pop	af
   596A F1            [10]  630 	pop	af
   596B 33            [ 6]  631 	inc	sp
   596C 33            [ 6]  632 	inc	sp
   596D 33            [ 6]  633 	inc	sp
   596E E5            [11]  634 	push	hl
   596F                     635 00153$:
                            636 ;src/entities/player.c:98: if (nexty < 0) {
   596F DD CB F1 7E   [20]  637 	bit	7, -15 (ix)
   5973 28 04         [12]  638 	jr	Z,00155$
                            639 ;src/entities/player.c:99: nexty = 0;
   5975 21 00 00      [10]  640 	ld	hl, #0x0000
   5978 E3            [19]  641 	ex	(sp), hl
   5979                     642 00155$:
                            643 ;src/entities/player.c:101: player->y = (u8)nexty;
   5979 DD 4E F0      [19]  644 	ld	c, -16 (ix)
   597C DD 6E F6      [19]  645 	ld	l,-10 (ix)
   597F DD 66 F7      [19]  646 	ld	h,-9 (ix)
   5982 71            [ 7]  647 	ld	(hl), c
                            648 ;src/entities/player.c:103: if (!player->on_ladder && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5983 DD 6E FA      [19]  649 	ld	l,-6 (ix)
   5986 DD 66 FB      [19]  650 	ld	h,-5 (ix)
   5989 7E            [ 7]  651 	ld	a, (hl)
   598A B7            [ 4]  652 	or	a, a
   598B 20 41         [12]  653 	jr	NZ,00160$
   598D DD 6E F8      [19]  654 	ld	l,-8 (ix)
   5990 DD 66 F9      [19]  655 	ld	h,-7 (ix)
   5993 4E            [ 7]  656 	ld	c, (hl)
   5994 DD 6E F6      [19]  657 	ld	l,-10 (ix)
   5997 DD 66 F7      [19]  658 	ld	h,-9 (ix)
   599A 5E            [ 7]  659 	ld	e, (hl)
   599B 16 00         [ 7]  660 	ld	d, #0x00
   599D DD 6E FC      [19]  661 	ld	l,-4 (ix)
   59A0 DD 66 FD      [19]  662 	ld	h,-3 (ix)
   59A3 6E            [ 7]  663 	ld	l, (hl)
   59A4 26 00         [ 7]  664 	ld	h, #0x00
   59A6 79            [ 4]  665 	ld	a, c
   59A7 F5            [11]  666 	push	af
   59A8 33            [ 6]  667 	inc	sp
   59A9 D5            [11]  668 	push	de
   59AA E5            [11]  669 	push	hl
   59AB CD 3B 4A      [17]  670 	call	_collision_is_on_ground_at
   59AE F1            [10]  671 	pop	af
   59AF F1            [10]  672 	pop	af
   59B0 33            [ 6]  673 	inc	sp
   59B1 7D            [ 4]  674 	ld	a, l
   59B2 B7            [ 4]  675 	or	a, a
   59B3 28 19         [12]  676 	jr	Z,00160$
   59B5 DD 6E F4      [19]  677 	ld	l,-12 (ix)
   59B8 DD 66 F5      [19]  678 	ld	h,-11 (ix)
   59BB 4E            [ 7]  679 	ld	c, (hl)
   59BC AF            [ 4]  680 	xor	a, a
   59BD 91            [ 4]  681 	sub	a, c
   59BE E2 C3 59      [10]  682 	jp	PO, 00285$
   59C1 EE 80         [ 7]  683 	xor	a, #0x80
   59C3                     684 00285$:
   59C3 F2 CE 59      [10]  685 	jp	P, 00160$
                            686 ;src/entities/player.c:104: player->vy = 0;
   59C6 DD 6E F4      [19]  687 	ld	l,-12 (ix)
   59C9 DD 66 F5      [19]  688 	ld	h,-11 (ix)
   59CC 36 00         [10]  689 	ld	(hl), #0x00
   59CE                     690 00160$:
   59CE DD F9         [10]  691 	ld	sp, ix
   59D0 DD E1         [14]  692 	pop	ix
   59D2 C9            [10]  693 	ret
                            694 ;src/entities/player.c:108: void playerrender(const Player* player) {
                            695 ;	---------------------------------
                            696 ; Function playerrender
                            697 ; ---------------------------------
   59D3                     698 _playerrender::
   59D3 DD E5         [15]  699 	push	ix
   59D5 DD 21 00 00   [14]  700 	ld	ix,#0
   59D9 DD 39         [15]  701 	add	ix,sp
                            702 ;src/entities/player.c:111: if (!player) {
   59DB DD 7E 05      [19]  703 	ld	a, 5 (ix)
   59DE DD B6 04      [19]  704 	or	a,4 (ix)
                            705 ;src/entities/player.c:112: return;
   59E1 28 32         [12]  706 	jr	Z,00103$
                            707 ;src/entities/player.c:115: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   59E3 DD 5E 04      [19]  708 	ld	e,4 (ix)
   59E6 DD 56 05      [19]  709 	ld	d,5 (ix)
   59E9 6B            [ 4]  710 	ld	l, e
   59EA 62            [ 4]  711 	ld	h, d
   59EB 23            [ 6]  712 	inc	hl
   59EC 46            [ 7]  713 	ld	b, (hl)
   59ED 1A            [ 7]  714 	ld	a, (de)
   59EE D5            [11]  715 	push	de
   59EF C5            [11]  716 	push	bc
   59F0 33            [ 6]  717 	inc	sp
   59F1 F5            [11]  718 	push	af
   59F2 33            [ 6]  719 	inc	sp
   59F3 21 00 C0      [10]  720 	ld	hl, #0xc000
   59F6 E5            [11]  721 	push	hl
   59F7 CD 4E 5E      [17]  722 	call	_cpct_getScreenPtr
   59FA 4D            [ 4]  723 	ld	c, l
   59FB 44            [ 4]  724 	ld	b, h
   59FC D1            [10]  725 	pop	de
                            726 ;src/entities/player.c:116: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   59FD D5            [11]  727 	push	de
   59FE FD E1         [14]  728 	pop	iy
   5A00 FD 7E 05      [19]  729 	ld	a, 5 (iy)
   5A03 EB            [ 4]  730 	ex	de,hl
   5A04 11 04 00      [10]  731 	ld	de, #0x0004
   5A07 19            [11]  732 	add	hl, de
   5A08 56            [ 7]  733 	ld	d, (hl)
   5A09 F5            [11]  734 	push	af
   5A0A 33            [ 6]  735 	inc	sp
   5A0B 1E 4F         [ 7]  736 	ld	e, #0x4f
   5A0D D5            [11]  737 	push	de
   5A0E C5            [11]  738 	push	bc
   5A0F CD 95 5D      [17]  739 	call	_cpct_drawSolidBox
   5A12 F1            [10]  740 	pop	af
   5A13 F1            [10]  741 	pop	af
   5A14 33            [ 6]  742 	inc	sp
   5A15                     743 00103$:
   5A15 DD E1         [14]  744 	pop	ix
   5A17 C9            [10]  745 	ret
                            746 	.area _CODE
                            747 	.area _INITIALIZER
                            748 	.area _CABS (ABS)
