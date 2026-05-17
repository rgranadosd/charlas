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
                             19 	.globl _cpct_px2byteM0
                             20 	.globl _playerinit
                             21 	.globl _playerupdate
                             22 	.globl _playerrender
                             23 ;--------------------------------------------------------
                             24 ; special function registers
                             25 ;--------------------------------------------------------
                             26 ;--------------------------------------------------------
                             27 ; ram data
                             28 ;--------------------------------------------------------
                             29 	.area _DATA
                             30 ;--------------------------------------------------------
                             31 ; ram data
                             32 ;--------------------------------------------------------
                             33 	.area _INITIALIZED
                             34 ;--------------------------------------------------------
                             35 ; absolute external ram data
                             36 ;--------------------------------------------------------
                             37 	.area _DABS (ABS)
                             38 ;--------------------------------------------------------
                             39 ; global & static initialisations
                             40 ;--------------------------------------------------------
                             41 	.area _HOME
                             42 	.area _GSINIT
                             43 	.area _GSFINAL
                             44 	.area _GSINIT
                             45 ;--------------------------------------------------------
                             46 ; Home
                             47 ;--------------------------------------------------------
                             48 	.area _HOME
                             49 	.area _HOME
                             50 ;--------------------------------------------------------
                             51 ; code
                             52 ;--------------------------------------------------------
                             53 	.area _CODE
                             54 ;src/entities/player.c:14: void playerinit(Player* player) {
                             55 ;	---------------------------------
                             56 ; Function playerinit
                             57 ; ---------------------------------
   56EB                      58 _playerinit::
                             59 ;src/entities/player.c:15: if (!player) {
   56EB 21 03 00      [10]   60 	ld	hl, #2+1
   56EE 39            [11]   61 	add	hl, sp
   56EF 7E            [ 7]   62 	ld	a, (hl)
   56F0 2B            [ 6]   63 	dec	hl
   56F1 B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:16: return;
   56F2 C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:19: player->x = 20;
   56F3 D1            [10]   68 	pop	de
   56F4 C1            [10]   69 	pop	bc
   56F5 C5            [11]   70 	push	bc
   56F6 D5            [11]   71 	push	de
   56F7 3E 14         [ 7]   72 	ld	a, #0x14
   56F9 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:20: player->y = 120;
   56FA 69            [ 4]   75 	ld	l, c
   56FB 60            [ 4]   76 	ld	h, b
   56FC 23            [ 6]   77 	inc	hl
   56FD 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:21: player->vx = 0;
   56FF 59            [ 4]   80 	ld	e, c
   5700 50            [ 4]   81 	ld	d, b
   5701 13            [ 6]   82 	inc	de
   5702 13            [ 6]   83 	inc	de
   5703 AF            [ 4]   84 	xor	a, a
   5704 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:22: player->vy = 0;
   5705 59            [ 4]   87 	ld	e, c
   5706 50            [ 4]   88 	ld	d, b
   5707 13            [ 6]   89 	inc	de
   5708 13            [ 6]   90 	inc	de
   5709 13            [ 6]   91 	inc	de
   570A AF            [ 4]   92 	xor	a, a
   570B 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:23: player->w = 4;
   570C 21 04 00      [10]   95 	ld	hl, #0x0004
   570F 09            [11]   96 	add	hl, bc
   5710 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:24: player->h = 16;
   5712 21 05 00      [10]   99 	ld	hl, #0x0005
   5715 09            [11]  100 	add	hl, bc
   5716 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:25: player->health = 3;
   5718 21 06 00      [10]  103 	ld	hl, #0x0006
   571B 09            [11]  104 	add	hl, bc
   571C 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:26: player->facing_left = 0;
   571E 21 07 00      [10]  107 	ld	hl, #0x0007
   5721 09            [11]  108 	add	hl, bc
   5722 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:27: player->jump_hold = 0;
   5724 21 08 00      [10]  111 	ld	hl, #0x0008
   5727 09            [11]  112 	add	hl, bc
   5728 36 00         [10]  113 	ld	(hl), #0x00
   572A C9            [10]  114 	ret
                            115 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   572B                     119 _playerupdate::
   572B DD E5         [15]  120 	push	ix
   572D DD 21 00 00   [14]  121 	ld	ix,#0
   5731 DD 39         [15]  122 	add	ix,sp
   5733 21 F2 FF      [10]  123 	ld	hl, #-14
   5736 39            [11]  124 	add	hl, sp
   5737 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:34: if (!player) {
   5738 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   573B DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:35: return;
   573E CA 72 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   5741 CD E3 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:39: player->vx = (i8)(player->vx - KPLAYERACCELERATION);
   5744 DD 4E 04      [19]  134 	ld	c,4 (ix)
   5747 DD 46 05      [19]  135 	ld	b,5 (ix)
   574A 59            [ 4]  136 	ld	e, c
   574B 50            [ 4]  137 	ld	d, b
   574C 13            [ 6]  138 	inc	de
   574D 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:40: player->facing_left = 1;
   574E 79            [ 4]  141 	ld	a, c
   574F C6 07         [ 7]  142 	add	a, #0x07
   5751 DD 77 FE      [19]  143 	ld	-2 (ix), a
   5754 78            [ 4]  144 	ld	a, b
   5755 CE 00         [ 7]  145 	adc	a, #0x00
   5757 DD 77 FF      [19]  146 	ld	-1 (ix), a
                            147 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   575A 7D            [ 4]  148 	ld	a, l
   575B B7            [ 4]  149 	or	a, a
   575C 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:39: player->vx = (i8)(player->vx - KPLAYERACCELERATION);
   575E 1A            [ 7]  152 	ld	a, (de)
   575F C6 FF         [ 7]  153 	add	a, #0xff
   5761 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:40: player->facing_left = 1;
   5762 DD 6E FE      [19]  156 	ld	l,-2 (ix)
   5765 DD 66 FF      [19]  157 	ld	h,-1 (ix)
   5768 36 01         [10]  158 	ld	(hl), #0x01
   576A 18 55         [12]  159 	jr	00117$
   576C                     160 00116$:
                            161 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   576C C5            [11]  162 	push	bc
   576D D5            [11]  163 	push	de
   576E CD EB 4F      [17]  164 	call	_input_is_right_pressed
   5771 DD 75 FD      [19]  165 	ld	-3 (ix), l
   5774 D1            [10]  166 	pop	de
   5775 C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:52: if (player->vx > KPLAYERMOVESPEED) player->vx = KPLAYERMOVESPEED;
   5776 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:42: player->vx = (i8)(player->vx + KPLAYERACCELERATION);
   5777 6F            [ 4]  171 	ld	l,a
   5778 3C            [ 4]  172 	inc	a
   5779 DD 77 FC      [19]  173 	ld	-4 (ix), a
                            174 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   577C DD 7E FD      [19]  175 	ld	a, -3 (ix)
   577F B7            [ 4]  176 	or	a, a
   5780 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:42: player->vx = (i8)(player->vx + KPLAYERACCELERATION);
   5782 DD 7E FC      [19]  179 	ld	a, -4 (ix)
   5785 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:43: player->facing_left = 0;
   5786 DD 6E FE      [19]  182 	ld	l,-2 (ix)
   5789 DD 66 FF      [19]  183 	ld	h,-1 (ix)
   578C 36 00         [10]  184 	ld	(hl), #0x00
   578E 18 31         [12]  185 	jr	00117$
   5790                     186 00113$:
                            187 ;src/entities/player.c:44: } else if (player->vx > 0) {
   5790 AF            [ 4]  188 	xor	a, a
   5791 95            [ 4]  189 	sub	a, l
   5792 E2 97 57      [10]  190 	jp	PO, 00223$
   5795 EE 80         [ 7]  191 	xor	a, #0x80
   5797                     192 00223$:
   5797 F2 AB 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:45: player->vx = (i8)(player->vx - KPLAYERDECELERATION);
   579A 7D            [ 4]  195 	ld	a, l
   579B C6 FF         [ 7]  196 	add	a, #0xff
   579D DD 77 FD      [19]  197 	ld	-3 (ix), a
   57A0 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   57A1 DD CB FD 7E   [20]  200 	bit	7, -3 (ix)
   57A5 28 1A         [12]  201 	jr	Z,00117$
   57A7 AF            [ 4]  202 	xor	a, a
   57A8 12            [ 7]  203 	ld	(de), a
   57A9 18 16         [12]  204 	jr	00117$
   57AB                     205 00110$:
                            206 ;src/entities/player.c:47: } else if (player->vx < 0) {
   57AB CB 7D         [ 8]  207 	bit	7, l
   57AD 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:48: player->vx = (i8)(player->vx + KPLAYERDECELERATION);
   57AF DD 7E FC      [19]  210 	ld	a, -4 (ix)
   57B2 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   57B3 AF            [ 4]  213 	xor	a, a
   57B4 DD 96 FC      [19]  214 	sub	a, -4 (ix)
   57B7 E2 BC 57      [10]  215 	jp	PO, 00224$
   57BA EE 80         [ 7]  216 	xor	a, #0x80
   57BC                     217 00224$:
   57BC F2 C1 57      [10]  218 	jp	P, 00117$
   57BF AF            [ 4]  219 	xor	a, a
   57C0 12            [ 7]  220 	ld	(de), a
   57C1                     221 00117$:
                            222 ;src/entities/player.c:52: if (player->vx > KPLAYERMOVESPEED) player->vx = KPLAYERMOVESPEED;
   57C1 1A            [ 7]  223 	ld	a, (de)
   57C2 6F            [ 4]  224 	ld	l, a
   57C3 3E 03         [ 7]  225 	ld	a, #0x03
   57C5 95            [ 4]  226 	sub	a, l
   57C6 E2 CB 57      [10]  227 	jp	PO, 00225$
   57C9 EE 80         [ 7]  228 	xor	a, #0x80
   57CB                     229 00225$:
   57CB F2 D1 57      [10]  230 	jp	P, 00119$
   57CE 3E 03         [ 7]  231 	ld	a, #0x03
   57D0 12            [ 7]  232 	ld	(de), a
   57D1                     233 00119$:
                            234 ;src/entities/player.c:53: if (player->vx < -KPLAYERMOVESPEED) player->vx = (i8)(-KPLAYERMOVESPEED);
   57D1 1A            [ 7]  235 	ld	a, (de)
   57D2 EE 80         [ 7]  236 	xor	a, #0x80
   57D4 D6 7D         [ 7]  237 	sub	a, #0x7d
   57D6 30 03         [12]  238 	jr	NC,00121$
   57D8 3E FD         [ 7]  239 	ld	a, #0xfd
   57DA 12            [ 7]  240 	ld	(de), a
   57DB                     241 00121$:
                            242 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57DB C5            [11]  243 	push	bc
   57DC D5            [11]  244 	push	de
   57DD CD 0B 50      [17]  245 	call	_input_is_jump_just_pressed
   57E0 DD 75 FC      [19]  246 	ld	-4 (ix), l
   57E3 D1            [10]  247 	pop	de
   57E4 C1            [10]  248 	pop	bc
   57E5 21 05 00      [10]  249 	ld	hl, #0x0005
   57E8 09            [11]  250 	add	hl,bc
   57E9 DD 75 FE      [19]  251 	ld	-2 (ix), l
   57EC DD 74 FF      [19]  252 	ld	-1 (ix), h
   57EF 21 01 00      [10]  253 	ld	hl, #0x0001
   57F2 09            [11]  254 	add	hl,bc
   57F3 DD 75 FA      [19]  255 	ld	-6 (ix), l
   57F6 DD 74 FB      [19]  256 	ld	-5 (ix), h
                            257 ;src/entities/player.c:56: player->vy = KPLAYERJUMPVELOCITY;
   57F9 21 03 00      [10]  258 	ld	hl, #0x0003
   57FC 09            [11]  259 	add	hl,bc
   57FD DD 75 F8      [19]  260 	ld	-8 (ix), l
   5800 DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:57: player->jump_hold = 5;
   5803 21 08 00      [10]  263 	ld	hl, #0x0008
   5806 09            [11]  264 	add	hl,bc
   5807 DD 75 F6      [19]  265 	ld	-10 (ix), l
   580A DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   580D DD 7E FC      [19]  268 	ld	a, -4 (ix)
   5810 B7            [ 4]  269 	or	a, a
   5811 28 4E         [12]  270 	jr	Z,00123$
   5813 DD 6E FE      [19]  271 	ld	l,-2 (ix)
   5816 DD 66 FF      [19]  272 	ld	h,-1 (ix)
   5819 7E            [ 7]  273 	ld	a, (hl)
   581A DD 6E FA      [19]  274 	ld	l,-6 (ix)
   581D DD 66 FB      [19]  275 	ld	h,-5 (ix)
   5820 6E            [ 7]  276 	ld	l, (hl)
   5821 DD 75 F4      [19]  277 	ld	-12 (ix), l
   5824 DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   5828 F5            [11]  279 	push	af
   5829 0A            [ 7]  280 	ld	a, (bc)
   582A 6F            [ 4]  281 	ld	l, a
   582B F1            [10]  282 	pop	af
   582C DD 75 F2      [19]  283 	ld	-14 (ix), l
   582F DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   5833 C5            [11]  285 	push	bc
   5834 D5            [11]  286 	push	de
   5835 F5            [11]  287 	push	af
   5836 33            [ 6]  288 	inc	sp
   5837 DD 6E F4      [19]  289 	ld	l,-12 (ix)
   583A DD 66 F5      [19]  290 	ld	h,-11 (ix)
   583D E5            [11]  291 	push	hl
   583E DD 6E F2      [19]  292 	ld	l,-14 (ix)
   5841 DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5844 E5            [11]  294 	push	hl
   5845 CD B7 4B      [17]  295 	call	_collision_is_on_ground_at
   5848 F1            [10]  296 	pop	af
   5849 F1            [10]  297 	pop	af
   584A 33            [ 6]  298 	inc	sp
   584B D1            [10]  299 	pop	de
   584C C1            [10]  300 	pop	bc
   584D 7D            [ 4]  301 	ld	a, l
   584E B7            [ 4]  302 	or	a, a
   584F 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:56: player->vy = KPLAYERJUMPVELOCITY;
   5851 DD 6E F8      [19]  305 	ld	l,-8 (ix)
   5854 DD 66 F9      [19]  306 	ld	h,-7 (ix)
   5857 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:57: player->jump_hold = 5;
   5859 DD 6E F6      [19]  309 	ld	l,-10 (ix)
   585C DD 66 F7      [19]  310 	ld	h,-9 (ix)
   585F 36 05         [10]  311 	ld	(hl), #0x05
   5861                     312 00123$:
                            313 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5861 C5            [11]  314 	push	bc
   5862 D5            [11]  315 	push	de
   5863 CD 03 50      [17]  316 	call	_input_is_jump_pressed
   5866 7D            [ 4]  317 	ld	a, l
   5867 D1            [10]  318 	pop	de
   5868 C1            [10]  319 	pop	bc
   5869 B7            [ 4]  320 	or	a, a
   586A 28 31         [12]  321 	jr	Z,00126$
   586C DD 6E F6      [19]  322 	ld	l,-10 (ix)
   586F DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5872 7E            [ 7]  324 	ld	a, (hl)
   5873 B7            [ 4]  325 	or	a, a
   5874 28 27         [12]  326 	jr	Z,00126$
   5876 DD 6E F8      [19]  327 	ld	l,-8 (ix)
   5879 DD 66 F9      [19]  328 	ld	h,-7 (ix)
   587C 6E            [ 7]  329 	ld	l, (hl)
   587D CB 7D         [ 8]  330 	bit	7, l
   587F 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:61: player->vy = (i8)(player->vy + KPLAYERJUMPBOOST);
   5881 7D            [ 4]  333 	ld	a, l
   5882 C6 FF         [ 7]  334 	add	a, #0xff
   5884 DD 6E F8      [19]  335 	ld	l,-8 (ix)
   5887 DD 66 F9      [19]  336 	ld	h,-7 (ix)
   588A 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:62: player->jump_hold--;
   588B DD 6E F6      [19]  339 	ld	l,-10 (ix)
   588E DD 66 F7      [19]  340 	ld	h,-9 (ix)
   5891 7E            [ 7]  341 	ld	a, (hl)
   5892 C6 FF         [ 7]  342 	add	a, #0xff
   5894 DD 6E F6      [19]  343 	ld	l,-10 (ix)
   5897 DD 66 F7      [19]  344 	ld	h,-9 (ix)
   589A 77            [ 7]  345 	ld	(hl), a
   589B 18 08         [12]  346 	jr	00127$
   589D                     347 00126$:
                            348 ;src/entities/player.c:64: player->jump_hold = 0;
   589D DD 6E F6      [19]  349 	ld	l,-10 (ix)
   58A0 DD 66 F7      [19]  350 	ld	h,-9 (ix)
   58A3 36 00         [10]  351 	ld	(hl), #0x00
   58A5                     352 00127$:
                            353 ;src/entities/player.c:67: player->vy = (i8)(player->vy + KPLAYERGRAVITY);
   58A5 DD 6E F8      [19]  354 	ld	l,-8 (ix)
   58A8 DD 66 F9      [19]  355 	ld	h,-7 (ix)
   58AB 7E            [ 7]  356 	ld	a, (hl)
   58AC 3C            [ 4]  357 	inc	a
   58AD DD 77 F2      [19]  358 	ld	-14 (ix), a
   58B0 DD 6E F8      [19]  359 	ld	l,-8 (ix)
   58B3 DD 66 F9      [19]  360 	ld	h,-7 (ix)
   58B6 DD 7E F2      [19]  361 	ld	a, -14 (ix)
   58B9 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:68: if (player->vy > KPLAYERMAXFALL) player->vy = KPLAYERMAXFALL;
   58BA 3E 04         [ 7]  364 	ld	a, #0x04
   58BC DD 96 F2      [19]  365 	sub	a, -14 (ix)
   58BF E2 C4 58      [10]  366 	jp	PO, 00226$
   58C2 EE 80         [ 7]  367 	xor	a, #0x80
   58C4                     368 00226$:
   58C4 F2 CF 58      [10]  369 	jp	P, 00131$
   58C7 DD 6E F8      [19]  370 	ld	l,-8 (ix)
   58CA DD 66 F9      [19]  371 	ld	h,-7 (ix)
   58CD 36 04         [10]  372 	ld	(hl), #0x04
   58CF                     373 00131$:
                            374 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   58CF 0A            [ 7]  375 	ld	a, (bc)
   58D0 DD 77 F2      [19]  376 	ld	-14 (ix), a
   58D3 DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58D7 1A            [ 7]  378 	ld	a, (de)
   58D8 5F            [ 4]  379 	ld	e, a
   58D9 17            [ 4]  380 	rla
   58DA 9F            [ 4]  381 	sbc	a, a
   58DB 57            [ 4]  382 	ld	d, a
   58DC E1            [10]  383 	pop	hl
   58DD E5            [11]  384 	push	hl
   58DE 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:71: if (nextx < 0) {
   58DF CB 7C         [ 8]  387 	bit	7, h
   58E1 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:72: nextx = 0;
   58E3 21 00 00      [10]  390 	ld	hl, #0x0000
   58E6                     391 00133$:
                            392 ;src/entities/player.c:74: if (nextx > 76) {
   58E6 3E 4C         [ 7]  393 	ld	a, #0x4c
   58E8 BD            [ 4]  394 	cp	a, l
   58E9 3E 00         [ 7]  395 	ld	a, #0x00
   58EB 9C            [ 4]  396 	sbc	a, h
   58EC E2 F1 58      [10]  397 	jp	PO, 00227$
   58EF EE 80         [ 7]  398 	xor	a, #0x80
   58F1                     399 00227$:
   58F1 F2 F7 58      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:75: nextx = 76;
   58F4 21 4C 00      [10]  402 	ld	hl, #0x004c
   58F7                     403 00135$:
                            404 ;src/entities/player.c:77: player->x = (u8)nextx;
   58F7 DD 75 F2      [19]  405 	ld	-14 (ix), l
   58FA 7D            [ 4]  406 	ld	a, l
   58FB 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   58FC DD 6E FA      [19]  409 	ld	l,-6 (ix)
   58FF DD 66 FB      [19]  410 	ld	h,-5 (ix)
   5902 5E            [ 7]  411 	ld	e, (hl)
   5903 16 00         [ 7]  412 	ld	d, #0x00
   5905 DD 6E F8      [19]  413 	ld	l,-8 (ix)
   5908 DD 66 F9      [19]  414 	ld	h,-7 (ix)
   590B 6E            [ 7]  415 	ld	l, (hl)
   590C 7D            [ 4]  416 	ld	a, l
   590D 17            [ 4]  417 	rla
   590E 9F            [ 4]  418 	sbc	a, a
   590F 67            [ 4]  419 	ld	h, a
   5910 19            [11]  420 	add	hl, de
   5911 E5            [11]  421 	push	hl
   5912 FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5914 DD 6E FE      [19]  424 	ld	l,-2 (ix)
   5917 DD 66 FF      [19]  425 	ld	h,-1 (ix)
   591A 66            [ 7]  426 	ld	h, (hl)
   591B DD 5E F2      [19]  427 	ld	e, -14 (ix)
   591E 16 00         [ 7]  428 	ld	d, #0x00
   5920 C5            [11]  429 	push	bc
   5921 E5            [11]  430 	push	hl
   5922 33            [ 6]  431 	inc	sp
   5923 FD E5         [15]  432 	push	iy
   5925 D5            [11]  433 	push	de
   5926 CD 36 4C      [17]  434 	call	_collision_clamp_y_at
   5929 F1            [10]  435 	pop	af
   592A F1            [10]  436 	pop	af
   592B 33            [ 6]  437 	inc	sp
   592C C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:81: if (nexty < 0) {
   592D CB 7C         [ 8]  440 	bit	7, h
   592F 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:82: nexty = 0;
   5931 21 00 00      [10]  443 	ld	hl, #0x0000
   5934                     444 00137$:
                            445 ;src/entities/player.c:84: player->y = (u8)nexty;
   5934 5D            [ 4]  446 	ld	e, l
   5935 DD 6E FA      [19]  447 	ld	l,-6 (ix)
   5938 DD 66 FB      [19]  448 	ld	h,-5 (ix)
   593B 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   593C DD 6E FE      [19]  451 	ld	l,-2 (ix)
   593F DD 66 FF      [19]  452 	ld	h,-1 (ix)
   5942 7E            [ 7]  453 	ld	a, (hl)
   5943 16 00         [ 7]  454 	ld	d, #0x00
   5945 F5            [11]  455 	push	af
   5946 0A            [ 7]  456 	ld	a, (bc)
   5947 4F            [ 4]  457 	ld	c, a
   5948 F1            [10]  458 	pop	af
   5949 06 00         [ 7]  459 	ld	b, #0x00
   594B F5            [11]  460 	push	af
   594C 33            [ 6]  461 	inc	sp
   594D D5            [11]  462 	push	de
   594E C5            [11]  463 	push	bc
   594F CD B7 4B      [17]  464 	call	_collision_is_on_ground_at
   5952 F1            [10]  465 	pop	af
   5953 F1            [10]  466 	pop	af
   5954 33            [ 6]  467 	inc	sp
   5955 7D            [ 4]  468 	ld	a, l
   5956 B7            [ 4]  469 	or	a, a
   5957 28 19         [12]  470 	jr	Z,00141$
   5959 DD 6E F8      [19]  471 	ld	l,-8 (ix)
   595C DD 66 F9      [19]  472 	ld	h,-7 (ix)
   595F 4E            [ 7]  473 	ld	c, (hl)
   5960 AF            [ 4]  474 	xor	a, a
   5961 91            [ 4]  475 	sub	a, c
   5962 E2 67 59      [10]  476 	jp	PO, 00228$
   5965 EE 80         [ 7]  477 	xor	a, #0x80
   5967                     478 00228$:
   5967 F2 72 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:87: player->vy = 0;
   596A DD 6E F8      [19]  481 	ld	l,-8 (ix)
   596D DD 66 F9      [19]  482 	ld	h,-7 (ix)
   5970 36 00         [10]  483 	ld	(hl), #0x00
   5972                     484 00141$:
   5972 DD F9         [10]  485 	ld	sp, ix
   5974 DD E1         [14]  486 	pop	ix
   5976 C9            [10]  487 	ret
                            488 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   5977                     492 _playerrender::
   5977 DD E5         [15]  493 	push	ix
   5979 DD 21 00 00   [14]  494 	ld	ix,#0
   597D DD 39         [15]  495 	add	ix,sp
   597F 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:94: if (!player) {
   5980 DD 7E 05      [19]  498 	ld	a, 5 (ix)
   5983 DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:95: return;
   5986 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5988 DD 5E 04      [19]  503 	ld	e,4 (ix)
   598B DD 56 05      [19]  504 	ld	d,5 (ix)
   598E 6B            [ 4]  505 	ld	l, e
   598F 62            [ 4]  506 	ld	h, d
   5990 23            [ 6]  507 	inc	hl
   5991 46            [ 7]  508 	ld	b, (hl)
   5992 1A            [ 7]  509 	ld	a, (de)
   5993 D5            [11]  510 	push	de
   5994 C5            [11]  511 	push	bc
   5995 33            [ 6]  512 	inc	sp
   5996 F5            [11]  513 	push	af
   5997 33            [ 6]  514 	inc	sp
   5998 21 00 C0      [10]  515 	ld	hl, #0xc000
   599B E5            [11]  516 	push	hl
   599C CD 53 5E      [17]  517 	call	_cpct_getScreenPtr
   599F 4D            [ 4]  518 	ld	c, l
   59A0 44            [ 4]  519 	ld	b, h
   59A1 D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   59A2 D5            [11]  522 	push	de
   59A3 FD E1         [14]  523 	pop	iy
   59A5 FD 7E 05      [19]  524 	ld	a, 5 (iy)
   59A8 DD 77 FF      [19]  525 	ld	-1 (ix), a
   59AB EB            [ 4]  526 	ex	de,hl
   59AC 11 04 00      [10]  527 	ld	de, #0x0004
   59AF 19            [11]  528 	add	hl, de
   59B0 56            [ 7]  529 	ld	d, (hl)
   59B1 C5            [11]  530 	push	bc
   59B2 D5            [11]  531 	push	de
   59B3 21 06 06      [10]  532 	ld	hl, #0x0606
   59B6 E5            [11]  533 	push	hl
   59B7 CD 60 5D      [17]  534 	call	_cpct_px2byteM0
   59BA 5D            [ 4]  535 	ld	e, l
   59BB F1            [10]  536 	pop	af
   59BC 57            [ 4]  537 	ld	d, a
   59BD C1            [10]  538 	pop	bc
   59BE DD 7E FF      [19]  539 	ld	a, -1 (ix)
   59C1 F5            [11]  540 	push	af
   59C2 33            [ 6]  541 	inc	sp
   59C3 D5            [11]  542 	push	de
   59C4 C5            [11]  543 	push	bc
   59C5 CD 9A 5D      [17]  544 	call	_cpct_drawSolidBox
   59C8 F1            [10]  545 	pop	af
   59C9 F1            [10]  546 	pop	af
   59CA 33            [ 6]  547 	inc	sp
   59CB                     548 00103$:
   59CB 33            [ 6]  549 	inc	sp
   59CC DD E1         [14]  550 	pop	ix
   59CE C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
