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
   562F                      57 _playerinit::
                             58 ;src/entities/player.c:15: if (!player) {
   562F 21 03 00      [10]   59 	ld	hl, #2+1
   5632 39            [11]   60 	add	hl, sp
   5633 7E            [ 7]   61 	ld	a, (hl)
   5634 2B            [ 6]   62 	dec	hl
   5635 B6            [ 7]   63 	or	a,(hl)
                             64 ;src/entities/player.c:16: return;
   5636 C8            [11]   65 	ret	Z
                             66 ;src/entities/player.c:19: player->x = 20;
   5637 D1            [10]   67 	pop	de
   5638 C1            [10]   68 	pop	bc
   5639 C5            [11]   69 	push	bc
   563A D5            [11]   70 	push	de
   563B 3E 14         [ 7]   71 	ld	a, #0x14
   563D 02            [ 7]   72 	ld	(bc), a
                             73 ;src/entities/player.c:20: player->y = 120;
   563E 69            [ 4]   74 	ld	l, c
   563F 60            [ 4]   75 	ld	h, b
   5640 23            [ 6]   76 	inc	hl
   5641 36 78         [10]   77 	ld	(hl), #0x78
                             78 ;src/entities/player.c:21: player->vx = 0;
   5643 59            [ 4]   79 	ld	e, c
   5644 50            [ 4]   80 	ld	d, b
   5645 13            [ 6]   81 	inc	de
   5646 13            [ 6]   82 	inc	de
   5647 AF            [ 4]   83 	xor	a, a
   5648 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/player.c:22: player->vy = 0;
   5649 59            [ 4]   86 	ld	e, c
   564A 50            [ 4]   87 	ld	d, b
   564B 13            [ 6]   88 	inc	de
   564C 13            [ 6]   89 	inc	de
   564D 13            [ 6]   90 	inc	de
   564E AF            [ 4]   91 	xor	a, a
   564F 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/player.c:23: player->w = 4;
   5650 21 04 00      [10]   94 	ld	hl, #0x0004
   5653 09            [11]   95 	add	hl, bc
   5654 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/player.c:24: player->h = 16;
   5656 21 05 00      [10]   98 	ld	hl, #0x0005
   5659 09            [11]   99 	add	hl, bc
   565A 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/player.c:25: player->health = 3;
   565C 21 06 00      [10]  102 	ld	hl, #0x0006
   565F 09            [11]  103 	add	hl, bc
   5660 36 03         [10]  104 	ld	(hl), #0x03
                            105 ;src/entities/player.c:26: player->facing_left = 0;
   5662 21 07 00      [10]  106 	ld	hl, #0x0007
   5665 09            [11]  107 	add	hl, bc
   5666 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/player.c:27: player->jump_hold = 0;
   5668 21 08 00      [10]  110 	ld	hl, #0x0008
   566B 09            [11]  111 	add	hl, bc
   566C 36 00         [10]  112 	ld	(hl), #0x00
   566E C9            [10]  113 	ret
   566F                     114 _kplayermovespeed:
   566F 03                  115 	.db #0x03	;  3
   5670                     116 _kplayeracceleration:
   5670 01                  117 	.db #0x01	;  1
   5671                     118 _kplayerdeceleration:
   5671 01                  119 	.db #0x01	;  1
   5672                     120 _kplayergravity:
   5672 01                  121 	.db #0x01	;  1
   5673                     122 _kplayermaxfall:
   5673 04                  123 	.db #0x04	;  4
   5674                     124 _kplayerjumpvelocity:
   5674 FA                  125 	.db #0xfa	; -6
   5675                     126 _kplayerjumpboost:
   5675 FF                  127 	.db #0xff	; -1
                            128 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            129 ;	---------------------------------
                            130 ; Function playerupdate
                            131 ; ---------------------------------
   5676                     132 _playerupdate::
   5676 DD E5         [15]  133 	push	ix
   5678 DD 21 00 00   [14]  134 	ld	ix,#0
   567C DD 39         [15]  135 	add	ix,sp
   567E 21 ED FF      [10]  136 	ld	hl, #-19
   5681 39            [11]  137 	add	hl, sp
   5682 F9            [ 6]  138 	ld	sp, hl
                            139 ;src/entities/player.c:34: if (!player) {
   5683 DD 7E 05      [19]  140 	ld	a, 5 (ix)
   5686 DD B6 04      [19]  141 	or	a,4 (ix)
                            142 ;src/entities/player.c:35: return;
   5689 CA DB 59      [10]  143 	jp	Z,00141$
                            144 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   568C CD 6B 4F      [17]  145 	call	_input_is_left_pressed
   568F 4D            [ 4]  146 	ld	c, l
                            147 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   5690 DD 7E 04      [19]  148 	ld	a, 4 (ix)
   5693 DD 77 FA      [19]  149 	ld	-6 (ix), a
   5696 DD 7E 05      [19]  150 	ld	a, 5 (ix)
   5699 DD 77 FB      [19]  151 	ld	-5 (ix), a
   569C DD 7E FA      [19]  152 	ld	a, -6 (ix)
   569F C6 02         [ 7]  153 	add	a, #0x02
   56A1 DD 77 FC      [19]  154 	ld	-4 (ix), a
   56A4 DD 7E FB      [19]  155 	ld	a, -5 (ix)
   56A7 CE 00         [ 7]  156 	adc	a, #0x00
   56A9 DD 77 FD      [19]  157 	ld	-3 (ix), a
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   56AC DD 7E FA      [19]  159 	ld	a, -6 (ix)
   56AF C6 07         [ 7]  160 	add	a, #0x07
   56B1 DD 77 FE      [19]  161 	ld	-2 (ix), a
   56B4 DD 7E FB      [19]  162 	ld	a, -5 (ix)
   56B7 CE 00         [ 7]  163 	adc	a, #0x00
   56B9 DD 77 FF      [19]  164 	ld	-1 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   56BC 79            [ 4]  166 	ld	a, c
   56BD B7            [ 4]  167 	or	a, a
   56BE 28 1E         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   56C0 DD 6E FC      [19]  170 	ld	l,-4 (ix)
   56C3 DD 66 FD      [19]  171 	ld	h,-3 (ix)
   56C6 4E            [ 7]  172 	ld	c, (hl)
   56C7 21 70 56      [10]  173 	ld	hl,#_kplayeracceleration + 0
   56CA 46            [ 7]  174 	ld	b, (hl)
   56CB 79            [ 4]  175 	ld	a, c
   56CC 90            [ 4]  176 	sub	a, b
   56CD DD 6E FC      [19]  177 	ld	l,-4 (ix)
   56D0 DD 66 FD      [19]  178 	ld	h,-3 (ix)
   56D3 77            [ 7]  179 	ld	(hl), a
                            180 ;src/entities/player.c:40: player->facing_left = 1;
   56D4 DD 6E FE      [19]  181 	ld	l,-2 (ix)
   56D7 DD 66 FF      [19]  182 	ld	h,-1 (ix)
   56DA 36 01         [10]  183 	ld	(hl), #0x01
   56DC 18 6B         [12]  184 	jr	00117$
   56DE                     185 00116$:
                            186 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   56DE CD 73 4F      [17]  187 	call	_input_is_right_pressed
   56E1 7D            [ 4]  188 	ld	a, l
                            189 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   56E2 DD 6E FC      [19]  190 	ld	l,-4 (ix)
   56E5 DD 66 FD      [19]  191 	ld	h,-3 (ix)
   56E8 4E            [ 7]  192 	ld	c, (hl)
                            193 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   56E9 B7            [ 4]  194 	or	a, a
   56EA 28 17         [12]  195 	jr	Z,00113$
                            196 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   56EC 21 70 56      [10]  197 	ld	hl,#_kplayeracceleration + 0
   56EF 5E            [ 7]  198 	ld	e, (hl)
   56F0 79            [ 4]  199 	ld	a, c
   56F1 83            [ 4]  200 	add	a, e
   56F2 DD 6E FC      [19]  201 	ld	l,-4 (ix)
   56F5 DD 66 FD      [19]  202 	ld	h,-3 (ix)
   56F8 77            [ 7]  203 	ld	(hl), a
                            204 ;src/entities/player.c:43: player->facing_left = 0;
   56F9 DD 6E FE      [19]  205 	ld	l,-2 (ix)
   56FC DD 66 FF      [19]  206 	ld	h,-1 (ix)
   56FF 36 00         [10]  207 	ld	(hl), #0x00
   5701 18 46         [12]  208 	jr	00117$
   5703                     209 00113$:
                            210 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5703 21 71 56      [10]  211 	ld	hl,#_kplayerdeceleration + 0
   5706 46            [ 7]  212 	ld	b, (hl)
                            213 ;src/entities/player.c:44: } else if (player->vx > 0) {
   5707 AF            [ 4]  214 	xor	a, a
   5708 91            [ 4]  215 	sub	a, c
   5709 E2 0E 57      [10]  216 	jp	PO, 00223$
   570C EE 80         [ 7]  217 	xor	a, #0x80
   570E                     218 00223$:
   570E F2 29 57      [10]  219 	jp	P, 00110$
                            220 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5711 79            [ 4]  221 	ld	a, c
   5712 90            [ 4]  222 	sub	a, b
   5713 4F            [ 4]  223 	ld	c, a
   5714 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   5717 DD 66 FD      [19]  225 	ld	h,-3 (ix)
   571A 71            [ 7]  226 	ld	(hl), c
                            227 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   571B CB 79         [ 8]  228 	bit	7, c
   571D 28 2A         [12]  229 	jr	Z,00117$
   571F DD 6E FC      [19]  230 	ld	l,-4 (ix)
   5722 DD 66 FD      [19]  231 	ld	h,-3 (ix)
   5725 36 00         [10]  232 	ld	(hl), #0x00
   5727 18 20         [12]  233 	jr	00117$
   5729                     234 00110$:
                            235 ;src/entities/player.c:47: } else if (player->vx < 0) {
   5729 CB 79         [ 8]  236 	bit	7, c
   572B 28 1C         [12]  237 	jr	Z,00117$
                            238 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   572D 79            [ 4]  239 	ld	a, c
   572E 80            [ 4]  240 	add	a, b
   572F 4F            [ 4]  241 	ld	c, a
   5730 DD 6E FC      [19]  242 	ld	l,-4 (ix)
   5733 DD 66 FD      [19]  243 	ld	h,-3 (ix)
   5736 71            [ 7]  244 	ld	(hl), c
                            245 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   5737 AF            [ 4]  246 	xor	a, a
   5738 91            [ 4]  247 	sub	a, c
   5739 E2 3E 57      [10]  248 	jp	PO, 00224$
   573C EE 80         [ 7]  249 	xor	a, #0x80
   573E                     250 00224$:
   573E F2 49 57      [10]  251 	jp	P, 00117$
   5741 DD 6E FC      [19]  252 	ld	l,-4 (ix)
   5744 DD 66 FD      [19]  253 	ld	h,-3 (ix)
   5747 36 00         [10]  254 	ld	(hl), #0x00
   5749                     255 00117$:
                            256 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5749 DD 6E FC      [19]  257 	ld	l,-4 (ix)
   574C DD 66 FD      [19]  258 	ld	h,-3 (ix)
   574F 46            [ 7]  259 	ld	b, (hl)
   5750 21 6F 56      [10]  260 	ld	hl,#_kplayermovespeed + 0
   5753 4E            [ 7]  261 	ld	c, (hl)
   5754 79            [ 4]  262 	ld	a, c
   5755 90            [ 4]  263 	sub	a, b
   5756 E2 5B 57      [10]  264 	jp	PO, 00225$
   5759 EE 80         [ 7]  265 	xor	a, #0x80
   575B                     266 00225$:
   575B F2 65 57      [10]  267 	jp	P, 00119$
   575E DD 6E FC      [19]  268 	ld	l,-4 (ix)
   5761 DD 66 FD      [19]  269 	ld	h,-3 (ix)
   5764 71            [ 7]  270 	ld	(hl), c
   5765                     271 00119$:
                            272 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5765 DD 6E FC      [19]  273 	ld	l,-4 (ix)
   5768 DD 66 FD      [19]  274 	ld	h,-3 (ix)
   576B 7E            [ 7]  275 	ld	a, (hl)
   576C DD 77 FE      [19]  276 	ld	-2 (ix), a
   576F 3A 6F 56      [13]  277 	ld	a,(#_kplayermovespeed + 0)
   5772 DD 77 F9      [19]  278 	ld	-7 (ix), a
   5775 DD 77 F7      [19]  279 	ld	-9 (ix), a
   5778 DD 7E F9      [19]  280 	ld	a, -7 (ix)
   577B 17            [ 4]  281 	rla
   577C 9F            [ 4]  282 	sbc	a, a
   577D DD 77 F8      [19]  283 	ld	-8 (ix), a
   5780 AF            [ 4]  284 	xor	a, a
   5781 DD 96 F7      [19]  285 	sub	a, -9 (ix)
   5784 DD 77 F7      [19]  286 	ld	-9 (ix), a
   5787 3E 00         [ 7]  287 	ld	a, #0x00
   5789 DD 9E F8      [19]  288 	sbc	a, -8 (ix)
   578C DD 77 F8      [19]  289 	ld	-8 (ix), a
   578F DD 7E FE      [19]  290 	ld	a, -2 (ix)
   5792 DD 77 FE      [19]  291 	ld	-2 (ix), a
   5795 17            [ 4]  292 	rla
   5796 9F            [ 4]  293 	sbc	a, a
   5797 DD 77 FF      [19]  294 	ld	-1 (ix), a
   579A DD 7E FE      [19]  295 	ld	a, -2 (ix)
   579D DD 96 F7      [19]  296 	sub	a, -9 (ix)
   57A0 DD 7E FF      [19]  297 	ld	a, -1 (ix)
   57A3 DD 9E F8      [19]  298 	sbc	a, -8 (ix)
   57A6 E2 AB 57      [10]  299 	jp	PO, 00226$
   57A9 EE 80         [ 7]  300 	xor	a, #0x80
   57AB                     301 00226$:
   57AB F2 BA 57      [10]  302 	jp	P, 00121$
   57AE AF            [ 4]  303 	xor	a, a
   57AF DD 96 F9      [19]  304 	sub	a, -7 (ix)
   57B2 4F            [ 4]  305 	ld	c, a
   57B3 DD 6E FC      [19]  306 	ld	l,-4 (ix)
   57B6 DD 66 FD      [19]  307 	ld	h,-3 (ix)
   57B9 71            [ 7]  308 	ld	(hl), c
   57BA                     309 00121$:
                            310 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57BA CD 93 4F      [17]  311 	call	_input_is_jump_just_pressed
   57BD DD 75 F7      [19]  312 	ld	-9 (ix), l
   57C0 DD 7E FA      [19]  313 	ld	a, -6 (ix)
   57C3 C6 05         [ 7]  314 	add	a, #0x05
   57C5 DD 77 FE      [19]  315 	ld	-2 (ix), a
   57C8 DD 7E FB      [19]  316 	ld	a, -5 (ix)
   57CB CE 00         [ 7]  317 	adc	a, #0x00
   57CD DD 77 FF      [19]  318 	ld	-1 (ix), a
   57D0 DD 7E FA      [19]  319 	ld	a, -6 (ix)
   57D3 C6 01         [ 7]  320 	add	a, #0x01
   57D5 DD 77 F5      [19]  321 	ld	-11 (ix), a
   57D8 DD 7E FB      [19]  322 	ld	a, -5 (ix)
   57DB CE 00         [ 7]  323 	adc	a, #0x00
   57DD DD 77 F6      [19]  324 	ld	-10 (ix), a
                            325 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   57E0 DD 7E FA      [19]  326 	ld	a, -6 (ix)
   57E3 C6 03         [ 7]  327 	add	a, #0x03
   57E5 DD 77 F3      [19]  328 	ld	-13 (ix), a
   57E8 DD 7E FB      [19]  329 	ld	a, -5 (ix)
   57EB CE 00         [ 7]  330 	adc	a, #0x00
   57ED DD 77 F4      [19]  331 	ld	-12 (ix), a
                            332 ;src/entities/player.c:57: player->jump_hold = 5;
   57F0 DD 7E FA      [19]  333 	ld	a, -6 (ix)
   57F3 C6 08         [ 7]  334 	add	a, #0x08
   57F5 DD 77 F1      [19]  335 	ld	-15 (ix), a
   57F8 DD 7E FB      [19]  336 	ld	a, -5 (ix)
   57FB CE 00         [ 7]  337 	adc	a, #0x00
   57FD DD 77 F2      [19]  338 	ld	-14 (ix), a
                            339 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5800 DD 7E F7      [19]  340 	ld	a, -9 (ix)
   5803 B7            [ 4]  341 	or	a, a
   5804 28 3A         [12]  342 	jr	Z,00123$
   5806 DD 6E FE      [19]  343 	ld	l,-2 (ix)
   5809 DD 66 FF      [19]  344 	ld	h,-1 (ix)
   580C 7E            [ 7]  345 	ld	a, (hl)
   580D DD 6E F5      [19]  346 	ld	l,-11 (ix)
   5810 DD 66 F6      [19]  347 	ld	h,-10 (ix)
   5813 4E            [ 7]  348 	ld	c, (hl)
   5814 06 00         [ 7]  349 	ld	b, #0x00
   5816 DD 6E FA      [19]  350 	ld	l,-6 (ix)
   5819 DD 66 FB      [19]  351 	ld	h,-5 (ix)
   581C 5E            [ 7]  352 	ld	e, (hl)
   581D 16 00         [ 7]  353 	ld	d, #0x00
   581F F5            [11]  354 	push	af
   5820 33            [ 6]  355 	inc	sp
   5821 C5            [11]  356 	push	bc
   5822 D5            [11]  357 	push	de
   5823 CD 3D 4B      [17]  358 	call	_collision_is_on_ground_at
   5826 F1            [10]  359 	pop	af
   5827 F1            [10]  360 	pop	af
   5828 33            [ 6]  361 	inc	sp
   5829 7D            [ 4]  362 	ld	a, l
   582A B7            [ 4]  363 	or	a, a
   582B 28 13         [12]  364 	jr	Z,00123$
                            365 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   582D 21 74 56      [10]  366 	ld	hl,#_kplayerjumpvelocity + 0
   5830 4E            [ 7]  367 	ld	c, (hl)
   5831 DD 6E F3      [19]  368 	ld	l,-13 (ix)
   5834 DD 66 F4      [19]  369 	ld	h,-12 (ix)
   5837 71            [ 7]  370 	ld	(hl), c
                            371 ;src/entities/player.c:57: player->jump_hold = 5;
   5838 DD 6E F1      [19]  372 	ld	l,-15 (ix)
   583B DD 66 F2      [19]  373 	ld	h,-14 (ix)
   583E 36 05         [10]  374 	ld	(hl), #0x05
   5840                     375 00123$:
                            376 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5840 CD 8B 4F      [17]  377 	call	_input_is_jump_pressed
   5843 DD 75 F7      [19]  378 	ld	-9 (ix), l
   5846 7D            [ 4]  379 	ld	a, l
   5847 B7            [ 4]  380 	or	a, a
   5848 28 41         [12]  381 	jr	Z,00126$
   584A DD 6E F1      [19]  382 	ld	l,-15 (ix)
   584D DD 66 F2      [19]  383 	ld	h,-14 (ix)
   5850 7E            [ 7]  384 	ld	a, (hl)
   5851 DD 77 F7      [19]  385 	ld	-9 (ix), a
   5854 B7            [ 4]  386 	or	a, a
   5855 28 34         [12]  387 	jr	Z,00126$
   5857 DD 6E F3      [19]  388 	ld	l,-13 (ix)
   585A DD 66 F4      [19]  389 	ld	h,-12 (ix)
   585D 7E            [ 7]  390 	ld	a, (hl)
   585E DD 77 F7      [19]  391 	ld	-9 (ix), a
   5861 DD CB F7 7E   [20]  392 	bit	7, -9 (ix)
   5865 28 24         [12]  393 	jr	Z,00126$
                            394 ;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
   5867 3A 75 56      [13]  395 	ld	a,(#_kplayerjumpboost + 0)
   586A DD 77 F9      [19]  396 	ld	-7 (ix), a
   586D DD 7E F7      [19]  397 	ld	a, -9 (ix)
   5870 DD 86 F9      [19]  398 	add	a, -7 (ix)
   5873 DD 6E F3      [19]  399 	ld	l,-13 (ix)
   5876 DD 66 F4      [19]  400 	ld	h,-12 (ix)
   5879 77            [ 7]  401 	ld	(hl), a
                            402 ;src/entities/player.c:62: player->jump_hold--;
   587A DD 6E F1      [19]  403 	ld	l,-15 (ix)
   587D DD 66 F2      [19]  404 	ld	h,-14 (ix)
   5880 4E            [ 7]  405 	ld	c, (hl)
   5881 0D            [ 4]  406 	dec	c
   5882 DD 6E F1      [19]  407 	ld	l,-15 (ix)
   5885 DD 66 F2      [19]  408 	ld	h,-14 (ix)
   5888 71            [ 7]  409 	ld	(hl), c
   5889 18 08         [12]  410 	jr	00127$
   588B                     411 00126$:
                            412 ;src/entities/player.c:64: player->jump_hold = 0;
   588B DD 6E F1      [19]  413 	ld	l,-15 (ix)
   588E DD 66 F2      [19]  414 	ld	h,-14 (ix)
   5891 36 00         [10]  415 	ld	(hl), #0x00
   5893                     416 00127$:
                            417 ;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
   5893 DD 6E F3      [19]  418 	ld	l,-13 (ix)
   5896 DD 66 F4      [19]  419 	ld	h,-12 (ix)
   5899 4E            [ 7]  420 	ld	c, (hl)
   589A 21 72 56      [10]  421 	ld	hl,#_kplayergravity + 0
   589D 46            [ 7]  422 	ld	b, (hl)
   589E 79            [ 4]  423 	ld	a, c
   589F 80            [ 4]  424 	add	a, b
   58A0 4F            [ 4]  425 	ld	c, a
   58A1 DD 6E F3      [19]  426 	ld	l,-13 (ix)
   58A4 DD 66 F4      [19]  427 	ld	h,-12 (ix)
   58A7 71            [ 7]  428 	ld	(hl), c
                            429 ;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58A8 21 73 56      [10]  430 	ld	hl,#_kplayermaxfall + 0
   58AB 46            [ 7]  431 	ld	b, (hl)
   58AC 78            [ 4]  432 	ld	a, b
   58AD 91            [ 4]  433 	sub	a, c
   58AE E2 B3 58      [10]  434 	jp	PO, 00227$
   58B1 EE 80         [ 7]  435 	xor	a, #0x80
   58B3                     436 00227$:
   58B3 F2 BD 58      [10]  437 	jp	P, 00131$
   58B6 DD 6E F3      [19]  438 	ld	l,-13 (ix)
   58B9 DD 66 F4      [19]  439 	ld	h,-12 (ix)
   58BC 70            [ 7]  440 	ld	(hl), b
   58BD                     441 00131$:
                            442 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   58BD DD 6E FA      [19]  443 	ld	l,-6 (ix)
   58C0 DD 66 FB      [19]  444 	ld	h,-5 (ix)
   58C3 4E            [ 7]  445 	ld	c, (hl)
   58C4 DD 71 F1      [19]  446 	ld	-15 (ix), c
   58C7 DD 36 F2 00   [19]  447 	ld	-14 (ix), #0x00
   58CB DD 6E FC      [19]  448 	ld	l,-4 (ix)
   58CE DD 66 FD      [19]  449 	ld	h,-3 (ix)
   58D1 7E            [ 7]  450 	ld	a, (hl)
   58D2 DD 77 F7      [19]  451 	ld	-9 (ix), a
   58D5 DD 77 F7      [19]  452 	ld	-9 (ix), a
   58D8 17            [ 4]  453 	rla
   58D9 9F            [ 4]  454 	sbc	a, a
   58DA DD 77 F8      [19]  455 	ld	-8 (ix), a
   58DD DD 7E F7      [19]  456 	ld	a, -9 (ix)
   58E0 DD 86 F1      [19]  457 	add	a, -15 (ix)
   58E3 DD 77 ED      [19]  458 	ld	-19 (ix), a
   58E6 DD 7E F8      [19]  459 	ld	a, -8 (ix)
   58E9 DD 8E F2      [19]  460 	adc	a, -14 (ix)
   58EC DD 77 EE      [19]  461 	ld	-18 (ix), a
                            462 ;src/entities/player.c:71: if (nextx < 0) {
   58EF DD CB EE 7E   [20]  463 	bit	7, -18 (ix)
   58F3 28 04         [12]  464 	jr	Z,00133$
                            465 ;src/entities/player.c:72: nextx = 0;
   58F5 21 00 00      [10]  466 	ld	hl, #0x0000
   58F8 E3            [19]  467 	ex	(sp), hl
   58F9                     468 00133$:
                            469 ;src/entities/player.c:74: if (nextx > 76) {
   58F9 3E 4C         [ 7]  470 	ld	a, #0x4c
   58FB DD BE ED      [19]  471 	cp	a, -19 (ix)
   58FE 3E 00         [ 7]  472 	ld	a, #0x00
   5900 DD 9E EE      [19]  473 	sbc	a, -18 (ix)
   5903 E2 08 59      [10]  474 	jp	PO, 00228$
   5906 EE 80         [ 7]  475 	xor	a, #0x80
   5908                     476 00228$:
   5908 F2 0F 59      [10]  477 	jp	P, 00135$
                            478 ;src/entities/player.c:75: nextx = 76;
   590B 21 4C 00      [10]  479 	ld	hl, #0x004c
   590E E3            [19]  480 	ex	(sp), hl
   590F                     481 00135$:
                            482 ;src/entities/player.c:77: player->x = (u8)nextx;
   590F DD 7E ED      [19]  483 	ld	a, -19 (ix)
   5912 DD 77 F1      [19]  484 	ld	-15 (ix), a
   5915 DD 6E FA      [19]  485 	ld	l,-6 (ix)
   5918 DD 66 FB      [19]  486 	ld	h,-5 (ix)
   591B DD 7E F1      [19]  487 	ld	a, -15 (ix)
   591E 77            [ 7]  488 	ld	(hl), a
                            489 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   591F DD 6E F5      [19]  490 	ld	l,-11 (ix)
   5922 DD 66 F6      [19]  491 	ld	h,-10 (ix)
   5925 4E            [ 7]  492 	ld	c, (hl)
   5926 DD 71 F7      [19]  493 	ld	-9 (ix), c
   5929 DD 36 F8 00   [19]  494 	ld	-8 (ix), #0x00
   592D DD 6E F3      [19]  495 	ld	l,-13 (ix)
   5930 DD 66 F4      [19]  496 	ld	h,-12 (ix)
   5933 7E            [ 7]  497 	ld	a, (hl)
   5934 DD 77 FC      [19]  498 	ld	-4 (ix), a
   5937 17            [ 4]  499 	rla
   5938 9F            [ 4]  500 	sbc	a, a
   5939 DD 77 FD      [19]  501 	ld	-3 (ix), a
   593C DD 7E FC      [19]  502 	ld	a, -4 (ix)
   593F DD 86 F7      [19]  503 	add	a, -9 (ix)
   5942 DD 77 F7      [19]  504 	ld	-9 (ix), a
   5945 DD 7E FD      [19]  505 	ld	a, -3 (ix)
   5948 DD 8E F8      [19]  506 	adc	a, -8 (ix)
   594B DD 77 F8      [19]  507 	ld	-8 (ix), a
                            508 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   594E DD 6E FE      [19]  509 	ld	l,-2 (ix)
   5951 DD 66 FF      [19]  510 	ld	h,-1 (ix)
   5954 7E            [ 7]  511 	ld	a, (hl)
   5955 DD 77 F9      [19]  512 	ld	-7 (ix), a
   5958 DD 7E F1      [19]  513 	ld	a, -15 (ix)
   595B DD 77 F1      [19]  514 	ld	-15 (ix), a
   595E DD 36 F2 00   [19]  515 	ld	-14 (ix), #0x00
   5962 DD 7E F9      [19]  516 	ld	a, -7 (ix)
   5965 F5            [11]  517 	push	af
   5966 33            [ 6]  518 	inc	sp
   5967 DD 6E F7      [19]  519 	ld	l,-9 (ix)
   596A DD 66 F8      [19]  520 	ld	h,-8 (ix)
   596D E5            [11]  521 	push	hl
   596E DD 6E F1      [19]  522 	ld	l,-15 (ix)
   5971 DD 66 F2      [19]  523 	ld	h,-14 (ix)
   5974 E5            [11]  524 	push	hl
   5975 CD BC 4B      [17]  525 	call	_collision_clamp_y_at
   5978 F1            [10]  526 	pop	af
   5979 F1            [10]  527 	pop	af
   597A 33            [ 6]  528 	inc	sp
   597B DD 74 F2      [19]  529 	ld	-14 (ix), h
   597E DD 75 F1      [19]  530 	ld	-15 (ix), l
   5981 DD 75 EF      [19]  531 	ld	-17 (ix), l
   5984 DD 7E F2      [19]  532 	ld	a, -14 (ix)
   5987 DD 77 F0      [19]  533 	ld	-16 (ix), a
                            534 ;src/entities/player.c:81: if (nexty < 0) {
   598A DD CB F0 7E   [20]  535 	bit	7, -16 (ix)
   598E 28 08         [12]  536 	jr	Z,00137$
                            537 ;src/entities/player.c:82: nexty = 0;
   5990 DD 36 EF 00   [19]  538 	ld	-17 (ix), #0x00
   5994 DD 36 F0 00   [19]  539 	ld	-16 (ix), #0x00
   5998                     540 00137$:
                            541 ;src/entities/player.c:84: player->y = (u8)nexty;
   5998 DD 4E EF      [19]  542 	ld	c, -17 (ix)
   599B DD 6E F5      [19]  543 	ld	l,-11 (ix)
   599E DD 66 F6      [19]  544 	ld	h,-10 (ix)
   59A1 71            [ 7]  545 	ld	(hl), c
                            546 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   59A2 DD 6E FE      [19]  547 	ld	l,-2 (ix)
   59A5 DD 66 FF      [19]  548 	ld	h,-1 (ix)
   59A8 7E            [ 7]  549 	ld	a, (hl)
   59A9 06 00         [ 7]  550 	ld	b, #0x00
   59AB DD 6E FA      [19]  551 	ld	l,-6 (ix)
   59AE DD 66 FB      [19]  552 	ld	h,-5 (ix)
   59B1 5E            [ 7]  553 	ld	e, (hl)
   59B2 16 00         [ 7]  554 	ld	d, #0x00
   59B4 F5            [11]  555 	push	af
   59B5 33            [ 6]  556 	inc	sp
   59B6 C5            [11]  557 	push	bc
   59B7 D5            [11]  558 	push	de
   59B8 CD 3D 4B      [17]  559 	call	_collision_is_on_ground_at
   59BB F1            [10]  560 	pop	af
   59BC F1            [10]  561 	pop	af
   59BD 33            [ 6]  562 	inc	sp
   59BE 7D            [ 4]  563 	ld	a, l
   59BF B7            [ 4]  564 	or	a, a
   59C0 28 19         [12]  565 	jr	Z,00141$
   59C2 DD 6E F3      [19]  566 	ld	l,-13 (ix)
   59C5 DD 66 F4      [19]  567 	ld	h,-12 (ix)
   59C8 4E            [ 7]  568 	ld	c, (hl)
   59C9 AF            [ 4]  569 	xor	a, a
   59CA 91            [ 4]  570 	sub	a, c
   59CB E2 D0 59      [10]  571 	jp	PO, 00229$
   59CE EE 80         [ 7]  572 	xor	a, #0x80
   59D0                     573 00229$:
   59D0 F2 DB 59      [10]  574 	jp	P, 00141$
                            575 ;src/entities/player.c:87: player->vy = 0;
   59D3 DD 6E F3      [19]  576 	ld	l,-13 (ix)
   59D6 DD 66 F4      [19]  577 	ld	h,-12 (ix)
   59D9 36 00         [10]  578 	ld	(hl), #0x00
   59DB                     579 00141$:
   59DB DD F9         [10]  580 	ld	sp, ix
   59DD DD E1         [14]  581 	pop	ix
   59DF C9            [10]  582 	ret
                            583 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            584 ;	---------------------------------
                            585 ; Function playerrender
                            586 ; ---------------------------------
   59E0                     587 _playerrender::
   59E0 DD E5         [15]  588 	push	ix
   59E2 DD 21 00 00   [14]  589 	ld	ix,#0
   59E6 DD 39         [15]  590 	add	ix,sp
                            591 ;src/entities/player.c:94: if (!player) {
   59E8 DD 7E 05      [19]  592 	ld	a, 5 (ix)
   59EB DD B6 04      [19]  593 	or	a,4 (ix)
                            594 ;src/entities/player.c:95: return;
   59EE 28 32         [12]  595 	jr	Z,00103$
                            596 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   59F0 DD 5E 04      [19]  597 	ld	e,4 (ix)
   59F3 DD 56 05      [19]  598 	ld	d,5 (ix)
   59F6 6B            [ 4]  599 	ld	l, e
   59F7 62            [ 4]  600 	ld	h, d
   59F8 23            [ 6]  601 	inc	hl
   59F9 46            [ 7]  602 	ld	b, (hl)
   59FA 1A            [ 7]  603 	ld	a, (de)
   59FB D5            [11]  604 	push	de
   59FC C5            [11]  605 	push	bc
   59FD 33            [ 6]  606 	inc	sp
   59FE F5            [11]  607 	push	af
   59FF 33            [ 6]  608 	inc	sp
   5A00 21 00 C0      [10]  609 	ld	hl, #0xc000
   5A03 E5            [11]  610 	push	hl
   5A04 CD 62 5E      [17]  611 	call	_cpct_getScreenPtr
   5A07 4D            [ 4]  612 	ld	c, l
   5A08 44            [ 4]  613 	ld	b, h
   5A09 D1            [10]  614 	pop	de
                            615 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   5A0A D5            [11]  616 	push	de
   5A0B FD E1         [14]  617 	pop	iy
   5A0D FD 7E 05      [19]  618 	ld	a, 5 (iy)
   5A10 EB            [ 4]  619 	ex	de,hl
   5A11 11 04 00      [10]  620 	ld	de, #0x0004
   5A14 19            [11]  621 	add	hl, de
   5A15 56            [ 7]  622 	ld	d, (hl)
   5A16 F5            [11]  623 	push	af
   5A17 33            [ 6]  624 	inc	sp
   5A18 1E 4F         [ 7]  625 	ld	e, #0x4f
   5A1A D5            [11]  626 	push	de
   5A1B C5            [11]  627 	push	bc
   5A1C CD A9 5D      [17]  628 	call	_cpct_drawSolidBox
   5A1F F1            [10]  629 	pop	af
   5A20 F1            [10]  630 	pop	af
   5A21 33            [ 6]  631 	inc	sp
   5A22                     632 00103$:
   5A22 DD E1         [14]  633 	pop	ix
   5A24 C9            [10]  634 	ret
                            635 	.area _CODE
                            636 	.area _INITIALIZER
                            637 	.area _CABS (ABS)
