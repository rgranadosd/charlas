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
                             54 ;src/entities/player.c:16: void playerinit(Player* player) {
                             55 ;	---------------------------------
                             56 ; Function playerinit
                             57 ; ---------------------------------
   56DC                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   56DC 21 03 00      [10]   60 	ld	hl, #2+1
   56DF 39            [11]   61 	add	hl, sp
   56E0 7E            [ 7]   62 	ld	a, (hl)
   56E1 2B            [ 6]   63 	dec	hl
   56E2 B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   56E3 C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   56E4 D1            [10]   68 	pop	de
   56E5 C1            [10]   69 	pop	bc
   56E6 C5            [11]   70 	push	bc
   56E7 D5            [11]   71 	push	de
   56E8 3E 14         [ 7]   72 	ld	a, #0x14
   56EA 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   56EB 69            [ 4]   75 	ld	l, c
   56EC 60            [ 4]   76 	ld	h, b
   56ED 23            [ 6]   77 	inc	hl
   56EE 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   56F0 59            [ 4]   80 	ld	e, c
   56F1 50            [ 4]   81 	ld	d, b
   56F2 13            [ 6]   82 	inc	de
   56F3 13            [ 6]   83 	inc	de
   56F4 AF            [ 4]   84 	xor	a, a
   56F5 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   56F6 59            [ 4]   87 	ld	e, c
   56F7 50            [ 4]   88 	ld	d, b
   56F8 13            [ 6]   89 	inc	de
   56F9 13            [ 6]   90 	inc	de
   56FA 13            [ 6]   91 	inc	de
   56FB AF            [ 4]   92 	xor	a, a
   56FC 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   56FD 21 04 00      [10]   95 	ld	hl, #0x0004
   5700 09            [11]   96 	add	hl, bc
   5701 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   5703 21 05 00      [10]   99 	ld	hl, #0x0005
   5706 09            [11]  100 	add	hl, bc
   5707 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   5709 21 06 00      [10]  103 	ld	hl, #0x0006
   570C 09            [11]  104 	add	hl, bc
   570D 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   570F 21 07 00      [10]  107 	ld	hl, #0x0007
   5712 09            [11]  108 	add	hl, bc
   5713 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   5715 21 08 00      [10]  111 	ld	hl, #0x0008
   5718 09            [11]  112 	add	hl, bc
   5719 36 00         [10]  113 	ld	(hl), #0x00
   571B C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   571C                     119 _playerupdate::
   571C DD E5         [15]  120 	push	ix
   571E DD 21 00 00   [14]  121 	ld	ix,#0
   5722 DD 39         [15]  122 	add	ix,sp
   5724 21 F2 FF      [10]  123 	ld	hl, #-14
   5727 39            [11]  124 	add	hl, sp
   5728 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   5729 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   572C DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   572F CA 63 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5732 CD D6 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5735 DD 4E 04      [19]  134 	ld	c,4 (ix)
   5738 DD 46 05      [19]  135 	ld	b,5 (ix)
   573B 59            [ 4]  136 	ld	e, c
   573C 50            [ 4]  137 	ld	d, b
   573D 13            [ 6]  138 	inc	de
   573E 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   573F 79            [ 4]  141 	ld	a, c
   5740 C6 07         [ 7]  142 	add	a, #0x07
   5742 DD 77 FE      [19]  143 	ld	-2 (ix), a
   5745 78            [ 4]  144 	ld	a, b
   5746 CE 00         [ 7]  145 	adc	a, #0x00
   5748 DD 77 FF      [19]  146 	ld	-1 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   574B 7D            [ 4]  148 	ld	a, l
   574C B7            [ 4]  149 	or	a, a
   574D 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   574F 1A            [ 7]  152 	ld	a, (de)
   5750 C6 FF         [ 7]  153 	add	a, #0xff
   5752 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   5753 DD 6E FE      [19]  156 	ld	l,-2 (ix)
   5756 DD 66 FF      [19]  157 	ld	h,-1 (ix)
   5759 36 01         [10]  158 	ld	(hl), #0x01
   575B 18 55         [12]  159 	jr	00117$
   575D                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   575D C5            [11]  162 	push	bc
   575E D5            [11]  163 	push	de
   575F CD DE 4F      [17]  164 	call	_input_is_right_pressed
   5762 DD 75 FD      [19]  165 	ld	-3 (ix), l
   5765 D1            [10]  166 	pop	de
   5766 C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5767 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5768 6F            [ 4]  171 	ld	l,a
   5769 3C            [ 4]  172 	inc	a
   576A DD 77 FC      [19]  173 	ld	-4 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   576D DD 7E FD      [19]  175 	ld	a, -3 (ix)
   5770 B7            [ 4]  176 	or	a, a
   5771 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5773 DD 7E FC      [19]  179 	ld	a, -4 (ix)
   5776 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   5777 DD 6E FE      [19]  182 	ld	l,-2 (ix)
   577A DD 66 FF      [19]  183 	ld	h,-1 (ix)
   577D 36 00         [10]  184 	ld	(hl), #0x00
   577F 18 31         [12]  185 	jr	00117$
   5781                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   5781 AF            [ 4]  188 	xor	a, a
   5782 95            [ 4]  189 	sub	a, l
   5783 E2 88 57      [10]  190 	jp	PO, 00223$
   5786 EE 80         [ 7]  191 	xor	a, #0x80
   5788                     192 00223$:
   5788 F2 9C 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   578B 7D            [ 4]  195 	ld	a, l
   578C C6 FF         [ 7]  196 	add	a, #0xff
   578E DD 77 FD      [19]  197 	ld	-3 (ix), a
   5791 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   5792 DD CB FD 7E   [20]  200 	bit	7, -3 (ix)
   5796 28 1A         [12]  201 	jr	Z,00117$
   5798 AF            [ 4]  202 	xor	a, a
   5799 12            [ 7]  203 	ld	(de), a
   579A 18 16         [12]  204 	jr	00117$
   579C                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   579C CB 7D         [ 8]  207 	bit	7, l
   579E 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   57A0 DD 7E FC      [19]  210 	ld	a, -4 (ix)
   57A3 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   57A4 AF            [ 4]  213 	xor	a, a
   57A5 DD 96 FC      [19]  214 	sub	a, -4 (ix)
   57A8 E2 AD 57      [10]  215 	jp	PO, 00224$
   57AB EE 80         [ 7]  216 	xor	a, #0x80
   57AD                     217 00224$:
   57AD F2 B2 57      [10]  218 	jp	P, 00117$
   57B0 AF            [ 4]  219 	xor	a, a
   57B1 12            [ 7]  220 	ld	(de), a
   57B2                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   57B2 1A            [ 7]  223 	ld	a, (de)
   57B3 6F            [ 4]  224 	ld	l, a
   57B4 3E 03         [ 7]  225 	ld	a, #0x03
   57B6 95            [ 4]  226 	sub	a, l
   57B7 E2 BC 57      [10]  227 	jp	PO, 00225$
   57BA EE 80         [ 7]  228 	xor	a, #0x80
   57BC                     229 00225$:
   57BC F2 C2 57      [10]  230 	jp	P, 00119$
   57BF 3E 03         [ 7]  231 	ld	a, #0x03
   57C1 12            [ 7]  232 	ld	(de), a
   57C2                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   57C2 1A            [ 7]  235 	ld	a, (de)
   57C3 EE 80         [ 7]  236 	xor	a, #0x80
   57C5 D6 7D         [ 7]  237 	sub	a, #0x7d
   57C7 30 03         [12]  238 	jr	NC,00121$
   57C9 3E FD         [ 7]  239 	ld	a, #0xfd
   57CB 12            [ 7]  240 	ld	(de), a
   57CC                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57CC C5            [11]  243 	push	bc
   57CD D5            [11]  244 	push	de
   57CE CD FE 4F      [17]  245 	call	_input_is_jump_just_pressed
   57D1 DD 75 FC      [19]  246 	ld	-4 (ix), l
   57D4 D1            [10]  247 	pop	de
   57D5 C1            [10]  248 	pop	bc
   57D6 21 05 00      [10]  249 	ld	hl, #0x0005
   57D9 09            [11]  250 	add	hl,bc
   57DA DD 75 FE      [19]  251 	ld	-2 (ix), l
   57DD DD 74 FF      [19]  252 	ld	-1 (ix), h
   57E0 21 01 00      [10]  253 	ld	hl, #0x0001
   57E3 09            [11]  254 	add	hl,bc
   57E4 DD 75 FA      [19]  255 	ld	-6 (ix), l
   57E7 DD 74 FB      [19]  256 	ld	-5 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   57EA 21 03 00      [10]  258 	ld	hl, #0x0003
   57ED 09            [11]  259 	add	hl,bc
   57EE DD 75 F8      [19]  260 	ld	-8 (ix), l
   57F1 DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   57F4 21 08 00      [10]  263 	ld	hl, #0x0008
   57F7 09            [11]  264 	add	hl,bc
   57F8 DD 75 F6      [19]  265 	ld	-10 (ix), l
   57FB DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57FE DD 7E FC      [19]  268 	ld	a, -4 (ix)
   5801 B7            [ 4]  269 	or	a, a
   5802 28 4E         [12]  270 	jr	Z,00123$
   5804 DD 6E FE      [19]  271 	ld	l,-2 (ix)
   5807 DD 66 FF      [19]  272 	ld	h,-1 (ix)
   580A 7E            [ 7]  273 	ld	a, (hl)
   580B DD 6E FA      [19]  274 	ld	l,-6 (ix)
   580E DD 66 FB      [19]  275 	ld	h,-5 (ix)
   5811 6E            [ 7]  276 	ld	l, (hl)
   5812 DD 75 F4      [19]  277 	ld	-12 (ix), l
   5815 DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   5819 F5            [11]  279 	push	af
   581A 0A            [ 7]  280 	ld	a, (bc)
   581B 6F            [ 4]  281 	ld	l, a
   581C F1            [10]  282 	pop	af
   581D DD 75 F2      [19]  283 	ld	-14 (ix), l
   5820 DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   5824 C5            [11]  285 	push	bc
   5825 D5            [11]  286 	push	de
   5826 F5            [11]  287 	push	af
   5827 33            [ 6]  288 	inc	sp
   5828 DD 6E F4      [19]  289 	ld	l,-12 (ix)
   582B DD 66 F5      [19]  290 	ld	h,-11 (ix)
   582E E5            [11]  291 	push	hl
   582F DD 6E F2      [19]  292 	ld	l,-14 (ix)
   5832 DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5835 E5            [11]  294 	push	hl
   5836 CD AA 4B      [17]  295 	call	_collision_is_on_ground_at
   5839 F1            [10]  296 	pop	af
   583A F1            [10]  297 	pop	af
   583B 33            [ 6]  298 	inc	sp
   583C D1            [10]  299 	pop	de
   583D C1            [10]  300 	pop	bc
   583E 7D            [ 4]  301 	ld	a, l
   583F B7            [ 4]  302 	or	a, a
   5840 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5842 DD 6E F8      [19]  305 	ld	l,-8 (ix)
   5845 DD 66 F9      [19]  306 	ld	h,-7 (ix)
   5848 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   584A DD 6E F6      [19]  309 	ld	l,-10 (ix)
   584D DD 66 F7      [19]  310 	ld	h,-9 (ix)
   5850 36 05         [10]  311 	ld	(hl), #0x05
   5852                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5852 C5            [11]  314 	push	bc
   5853 D5            [11]  315 	push	de
   5854 CD F6 4F      [17]  316 	call	_input_is_jump_pressed
   5857 7D            [ 4]  317 	ld	a, l
   5858 D1            [10]  318 	pop	de
   5859 C1            [10]  319 	pop	bc
   585A B7            [ 4]  320 	or	a, a
   585B 28 31         [12]  321 	jr	Z,00126$
   585D DD 6E F6      [19]  322 	ld	l,-10 (ix)
   5860 DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5863 7E            [ 7]  324 	ld	a, (hl)
   5864 B7            [ 4]  325 	or	a, a
   5865 28 27         [12]  326 	jr	Z,00126$
   5867 DD 6E F8      [19]  327 	ld	l,-8 (ix)
   586A DD 66 F9      [19]  328 	ld	h,-7 (ix)
   586D 6E            [ 7]  329 	ld	l, (hl)
   586E CB 7D         [ 8]  330 	bit	7, l
   5870 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   5872 7D            [ 4]  333 	ld	a, l
   5873 C6 FF         [ 7]  334 	add	a, #0xff
   5875 DD 6E F8      [19]  335 	ld	l,-8 (ix)
   5878 DD 66 F9      [19]  336 	ld	h,-7 (ix)
   587B 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   587C DD 6E F6      [19]  339 	ld	l,-10 (ix)
   587F DD 66 F7      [19]  340 	ld	h,-9 (ix)
   5882 7E            [ 7]  341 	ld	a, (hl)
   5883 C6 FF         [ 7]  342 	add	a, #0xff
   5885 DD 6E F6      [19]  343 	ld	l,-10 (ix)
   5888 DD 66 F7      [19]  344 	ld	h,-9 (ix)
   588B 77            [ 7]  345 	ld	(hl), a
   588C 18 08         [12]  346 	jr	00127$
   588E                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   588E DD 6E F6      [19]  349 	ld	l,-10 (ix)
   5891 DD 66 F7      [19]  350 	ld	h,-9 (ix)
   5894 36 00         [10]  351 	ld	(hl), #0x00
   5896                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   5896 DD 6E F8      [19]  354 	ld	l,-8 (ix)
   5899 DD 66 F9      [19]  355 	ld	h,-7 (ix)
   589C 7E            [ 7]  356 	ld	a, (hl)
   589D 3C            [ 4]  357 	inc	a
   589E DD 77 F2      [19]  358 	ld	-14 (ix), a
   58A1 DD 6E F8      [19]  359 	ld	l,-8 (ix)
   58A4 DD 66 F9      [19]  360 	ld	h,-7 (ix)
   58A7 DD 7E F2      [19]  361 	ld	a, -14 (ix)
   58AA 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58AB 3E 04         [ 7]  364 	ld	a, #0x04
   58AD DD 96 F2      [19]  365 	sub	a, -14 (ix)
   58B0 E2 B5 58      [10]  366 	jp	PO, 00226$
   58B3 EE 80         [ 7]  367 	xor	a, #0x80
   58B5                     368 00226$:
   58B5 F2 C0 58      [10]  369 	jp	P, 00131$
   58B8 DD 6E F8      [19]  370 	ld	l,-8 (ix)
   58BB DD 66 F9      [19]  371 	ld	h,-7 (ix)
   58BE 36 04         [10]  372 	ld	(hl), #0x04
   58C0                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   58C0 0A            [ 7]  375 	ld	a, (bc)
   58C1 DD 77 F2      [19]  376 	ld	-14 (ix), a
   58C4 DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58C8 1A            [ 7]  378 	ld	a, (de)
   58C9 5F            [ 4]  379 	ld	e, a
   58CA 17            [ 4]  380 	rla
   58CB 9F            [ 4]  381 	sbc	a, a
   58CC 57            [ 4]  382 	ld	d, a
   58CD E1            [10]  383 	pop	hl
   58CE E5            [11]  384 	push	hl
   58CF 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   58D0 CB 7C         [ 8]  387 	bit	7, h
   58D2 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   58D4 21 00 00      [10]  390 	ld	hl, #0x0000
   58D7                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   58D7 3E 4C         [ 7]  393 	ld	a, #0x4c
   58D9 BD            [ 4]  394 	cp	a, l
   58DA 3E 00         [ 7]  395 	ld	a, #0x00
   58DC 9C            [ 4]  396 	sbc	a, h
   58DD E2 E2 58      [10]  397 	jp	PO, 00227$
   58E0 EE 80         [ 7]  398 	xor	a, #0x80
   58E2                     399 00227$:
   58E2 F2 E8 58      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   58E5 21 4C 00      [10]  402 	ld	hl, #0x004c
   58E8                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   58E8 DD 75 F2      [19]  405 	ld	-14 (ix), l
   58EB 7D            [ 4]  406 	ld	a, l
   58EC 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   58ED DD 6E FA      [19]  409 	ld	l,-6 (ix)
   58F0 DD 66 FB      [19]  410 	ld	h,-5 (ix)
   58F3 5E            [ 7]  411 	ld	e, (hl)
   58F4 16 00         [ 7]  412 	ld	d, #0x00
   58F6 DD 6E F8      [19]  413 	ld	l,-8 (ix)
   58F9 DD 66 F9      [19]  414 	ld	h,-7 (ix)
   58FC 6E            [ 7]  415 	ld	l, (hl)
   58FD 7D            [ 4]  416 	ld	a, l
   58FE 17            [ 4]  417 	rla
   58FF 9F            [ 4]  418 	sbc	a, a
   5900 67            [ 4]  419 	ld	h, a
   5901 19            [11]  420 	add	hl, de
   5902 E5            [11]  421 	push	hl
   5903 FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5905 DD 6E FE      [19]  424 	ld	l,-2 (ix)
   5908 DD 66 FF      [19]  425 	ld	h,-1 (ix)
   590B 66            [ 7]  426 	ld	h, (hl)
   590C DD 5E F2      [19]  427 	ld	e, -14 (ix)
   590F 16 00         [ 7]  428 	ld	d, #0x00
   5911 C5            [11]  429 	push	bc
   5912 E5            [11]  430 	push	hl
   5913 33            [ 6]  431 	inc	sp
   5914 FD E5         [15]  432 	push	iy
   5916 D5            [11]  433 	push	de
   5917 CD 29 4C      [17]  434 	call	_collision_clamp_y_at
   591A F1            [10]  435 	pop	af
   591B F1            [10]  436 	pop	af
   591C 33            [ 6]  437 	inc	sp
   591D C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   591E CB 7C         [ 8]  440 	bit	7, h
   5920 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   5922 21 00 00      [10]  443 	ld	hl, #0x0000
   5925                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   5925 5D            [ 4]  446 	ld	e, l
   5926 DD 6E FA      [19]  447 	ld	l,-6 (ix)
   5929 DD 66 FB      [19]  448 	ld	h,-5 (ix)
   592C 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   592D DD 6E FE      [19]  451 	ld	l,-2 (ix)
   5930 DD 66 FF      [19]  452 	ld	h,-1 (ix)
   5933 7E            [ 7]  453 	ld	a, (hl)
   5934 16 00         [ 7]  454 	ld	d, #0x00
   5936 F5            [11]  455 	push	af
   5937 0A            [ 7]  456 	ld	a, (bc)
   5938 4F            [ 4]  457 	ld	c, a
   5939 F1            [10]  458 	pop	af
   593A 06 00         [ 7]  459 	ld	b, #0x00
   593C F5            [11]  460 	push	af
   593D 33            [ 6]  461 	inc	sp
   593E D5            [11]  462 	push	de
   593F C5            [11]  463 	push	bc
   5940 CD AA 4B      [17]  464 	call	_collision_is_on_ground_at
   5943 F1            [10]  465 	pop	af
   5944 F1            [10]  466 	pop	af
   5945 33            [ 6]  467 	inc	sp
   5946 7D            [ 4]  468 	ld	a, l
   5947 B7            [ 4]  469 	or	a, a
   5948 28 19         [12]  470 	jr	Z,00141$
   594A DD 6E F8      [19]  471 	ld	l,-8 (ix)
   594D DD 66 F9      [19]  472 	ld	h,-7 (ix)
   5950 4E            [ 7]  473 	ld	c, (hl)
   5951 AF            [ 4]  474 	xor	a, a
   5952 91            [ 4]  475 	sub	a, c
   5953 E2 58 59      [10]  476 	jp	PO, 00228$
   5956 EE 80         [ 7]  477 	xor	a, #0x80
   5958                     478 00228$:
   5958 F2 63 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   595B DD 6E F8      [19]  481 	ld	l,-8 (ix)
   595E DD 66 F9      [19]  482 	ld	h,-7 (ix)
   5961 36 00         [10]  483 	ld	(hl), #0x00
   5963                     484 00141$:
   5963 DD F9         [10]  485 	ld	sp, ix
   5965 DD E1         [14]  486 	pop	ix
   5967 C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   5968                     492 _playerrender::
   5968 DD E5         [15]  493 	push	ix
   596A DD 21 00 00   [14]  494 	ld	ix,#0
   596E DD 39         [15]  495 	add	ix,sp
   5970 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   5971 DD 7E 05      [19]  498 	ld	a, 5 (ix)
   5974 DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   5977 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5979 DD 5E 04      [19]  503 	ld	e,4 (ix)
   597C DD 56 05      [19]  504 	ld	d,5 (ix)
   597F 6B            [ 4]  505 	ld	l, e
   5980 62            [ 4]  506 	ld	h, d
   5981 23            [ 6]  507 	inc	hl
   5982 46            [ 7]  508 	ld	b, (hl)
   5983 1A            [ 7]  509 	ld	a, (de)
   5984 D5            [11]  510 	push	de
   5985 C5            [11]  511 	push	bc
   5986 33            [ 6]  512 	inc	sp
   5987 F5            [11]  513 	push	af
   5988 33            [ 6]  514 	inc	sp
   5989 21 00 C0      [10]  515 	ld	hl, #0xc000
   598C E5            [11]  516 	push	hl
   598D CD 4C 5E      [17]  517 	call	_cpct_getScreenPtr
   5990 4D            [ 4]  518 	ld	c, l
   5991 44            [ 4]  519 	ld	b, h
   5992 D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   5993 D5            [11]  522 	push	de
   5994 FD E1         [14]  523 	pop	iy
   5996 FD 7E 05      [19]  524 	ld	a, 5 (iy)
   5999 DD 77 FF      [19]  525 	ld	-1 (ix), a
   599C EB            [ 4]  526 	ex	de,hl
   599D 11 04 00      [10]  527 	ld	de, #0x0004
   59A0 19            [11]  528 	add	hl, de
   59A1 56            [ 7]  529 	ld	d, (hl)
   59A2 C5            [11]  530 	push	bc
   59A3 D5            [11]  531 	push	de
   59A4 21 06 06      [10]  532 	ld	hl, #0x0606
   59A7 E5            [11]  533 	push	hl
   59A8 CD 59 5D      [17]  534 	call	_cpct_px2byteM0
   59AB 5D            [ 4]  535 	ld	e, l
   59AC F1            [10]  536 	pop	af
   59AD 57            [ 4]  537 	ld	d, a
   59AE C1            [10]  538 	pop	bc
   59AF DD 7E FF      [19]  539 	ld	a, -1 (ix)
   59B2 F5            [11]  540 	push	af
   59B3 33            [ 6]  541 	inc	sp
   59B4 D5            [11]  542 	push	de
   59B5 C5            [11]  543 	push	bc
   59B6 CD 93 5D      [17]  544 	call	_cpct_drawSolidBox
   59B9 F1            [10]  545 	pop	af
   59BA F1            [10]  546 	pop	af
   59BB 33            [ 6]  547 	inc	sp
   59BC                     548 00103$:
   59BC 33            [ 6]  549 	inc	sp
   59BD DD E1         [14]  550 	pop	ix
   59BF C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
