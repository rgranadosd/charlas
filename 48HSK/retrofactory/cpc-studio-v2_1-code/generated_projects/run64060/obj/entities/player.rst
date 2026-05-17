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
   56E7                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   56E7 21 03 00      [10]   60 	ld	hl, #2+1
   56EA 39            [11]   61 	add	hl, sp
   56EB 7E            [ 7]   62 	ld	a, (hl)
   56EC 2B            [ 6]   63 	dec	hl
   56ED B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   56EE C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   56EF D1            [10]   68 	pop	de
   56F0 C1            [10]   69 	pop	bc
   56F1 C5            [11]   70 	push	bc
   56F2 D5            [11]   71 	push	de
   56F3 3E 14         [ 7]   72 	ld	a, #0x14
   56F5 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   56F6 69            [ 4]   75 	ld	l, c
   56F7 60            [ 4]   76 	ld	h, b
   56F8 23            [ 6]   77 	inc	hl
   56F9 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   56FB 59            [ 4]   80 	ld	e, c
   56FC 50            [ 4]   81 	ld	d, b
   56FD 13            [ 6]   82 	inc	de
   56FE 13            [ 6]   83 	inc	de
   56FF AF            [ 4]   84 	xor	a, a
   5700 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   5701 59            [ 4]   87 	ld	e, c
   5702 50            [ 4]   88 	ld	d, b
   5703 13            [ 6]   89 	inc	de
   5704 13            [ 6]   90 	inc	de
   5705 13            [ 6]   91 	inc	de
   5706 AF            [ 4]   92 	xor	a, a
   5707 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   5708 21 04 00      [10]   95 	ld	hl, #0x0004
   570B 09            [11]   96 	add	hl, bc
   570C 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   570E 21 05 00      [10]   99 	ld	hl, #0x0005
   5711 09            [11]  100 	add	hl, bc
   5712 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   5714 21 06 00      [10]  103 	ld	hl, #0x0006
   5717 09            [11]  104 	add	hl, bc
   5718 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   571A 21 07 00      [10]  107 	ld	hl, #0x0007
   571D 09            [11]  108 	add	hl, bc
   571E 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   5720 21 08 00      [10]  111 	ld	hl, #0x0008
   5723 09            [11]  112 	add	hl, bc
   5724 36 00         [10]  113 	ld	(hl), #0x00
   5726 C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   5727                     119 _playerupdate::
   5727 DD E5         [15]  120 	push	ix
   5729 DD 21 00 00   [14]  121 	ld	ix,#0
   572D DD 39         [15]  122 	add	ix,sp
   572F 21 F2 FF      [10]  123 	ld	hl, #-14
   5732 39            [11]  124 	add	hl, sp
   5733 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   5734 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   5737 DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   573A CA 6E 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   573D CD D6 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5740 DD 4E 04      [19]  134 	ld	c,4 (ix)
   5743 DD 46 05      [19]  135 	ld	b,5 (ix)
   5746 59            [ 4]  136 	ld	e, c
   5747 50            [ 4]  137 	ld	d, b
   5748 13            [ 6]  138 	inc	de
   5749 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   574A 79            [ 4]  141 	ld	a, c
   574B C6 07         [ 7]  142 	add	a, #0x07
   574D DD 77 FE      [19]  143 	ld	-2 (ix), a
   5750 78            [ 4]  144 	ld	a, b
   5751 CE 00         [ 7]  145 	adc	a, #0x00
   5753 DD 77 FF      [19]  146 	ld	-1 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5756 7D            [ 4]  148 	ld	a, l
   5757 B7            [ 4]  149 	or	a, a
   5758 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   575A 1A            [ 7]  152 	ld	a, (de)
   575B C6 FF         [ 7]  153 	add	a, #0xff
   575D 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   575E DD 6E FE      [19]  156 	ld	l,-2 (ix)
   5761 DD 66 FF      [19]  157 	ld	h,-1 (ix)
   5764 36 01         [10]  158 	ld	(hl), #0x01
   5766 18 55         [12]  159 	jr	00117$
   5768                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   5768 C5            [11]  162 	push	bc
   5769 D5            [11]  163 	push	de
   576A CD DE 4F      [17]  164 	call	_input_is_right_pressed
   576D DD 75 FA      [19]  165 	ld	-6 (ix), l
   5770 D1            [10]  166 	pop	de
   5771 C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5772 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5773 6F            [ 4]  171 	ld	l,a
   5774 3C            [ 4]  172 	inc	a
   5775 DD 77 FD      [19]  173 	ld	-3 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   5778 DD 7E FA      [19]  175 	ld	a, -6 (ix)
   577B B7            [ 4]  176 	or	a, a
   577C 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   577E DD 7E FD      [19]  179 	ld	a, -3 (ix)
   5781 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   5782 DD 6E FE      [19]  182 	ld	l,-2 (ix)
   5785 DD 66 FF      [19]  183 	ld	h,-1 (ix)
   5788 36 00         [10]  184 	ld	(hl), #0x00
   578A 18 31         [12]  185 	jr	00117$
   578C                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   578C AF            [ 4]  188 	xor	a, a
   578D 95            [ 4]  189 	sub	a, l
   578E E2 93 57      [10]  190 	jp	PO, 00223$
   5791 EE 80         [ 7]  191 	xor	a, #0x80
   5793                     192 00223$:
   5793 F2 A7 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   5796 7D            [ 4]  195 	ld	a, l
   5797 C6 FF         [ 7]  196 	add	a, #0xff
   5799 DD 77 FA      [19]  197 	ld	-6 (ix), a
   579C 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   579D DD CB FA 7E   [20]  200 	bit	7, -6 (ix)
   57A1 28 1A         [12]  201 	jr	Z,00117$
   57A3 AF            [ 4]  202 	xor	a, a
   57A4 12            [ 7]  203 	ld	(de), a
   57A5 18 16         [12]  204 	jr	00117$
   57A7                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   57A7 CB 7D         [ 8]  207 	bit	7, l
   57A9 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   57AB DD 7E FD      [19]  210 	ld	a, -3 (ix)
   57AE 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   57AF AF            [ 4]  213 	xor	a, a
   57B0 DD 96 FD      [19]  214 	sub	a, -3 (ix)
   57B3 E2 B8 57      [10]  215 	jp	PO, 00224$
   57B6 EE 80         [ 7]  216 	xor	a, #0x80
   57B8                     217 00224$:
   57B8 F2 BD 57      [10]  218 	jp	P, 00117$
   57BB AF            [ 4]  219 	xor	a, a
   57BC 12            [ 7]  220 	ld	(de), a
   57BD                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   57BD 1A            [ 7]  223 	ld	a, (de)
   57BE 6F            [ 4]  224 	ld	l, a
   57BF 3E 03         [ 7]  225 	ld	a, #0x03
   57C1 95            [ 4]  226 	sub	a, l
   57C2 E2 C7 57      [10]  227 	jp	PO, 00225$
   57C5 EE 80         [ 7]  228 	xor	a, #0x80
   57C7                     229 00225$:
   57C7 F2 CD 57      [10]  230 	jp	P, 00119$
   57CA 3E 03         [ 7]  231 	ld	a, #0x03
   57CC 12            [ 7]  232 	ld	(de), a
   57CD                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   57CD 1A            [ 7]  235 	ld	a, (de)
   57CE EE 80         [ 7]  236 	xor	a, #0x80
   57D0 D6 7D         [ 7]  237 	sub	a, #0x7d
   57D2 30 03         [12]  238 	jr	NC,00121$
   57D4 3E FD         [ 7]  239 	ld	a, #0xfd
   57D6 12            [ 7]  240 	ld	(de), a
   57D7                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57D7 C5            [11]  243 	push	bc
   57D8 D5            [11]  244 	push	de
   57D9 CD FE 4F      [17]  245 	call	_input_is_jump_just_pressed
   57DC DD 75 FD      [19]  246 	ld	-3 (ix), l
   57DF D1            [10]  247 	pop	de
   57E0 C1            [10]  248 	pop	bc
   57E1 21 05 00      [10]  249 	ld	hl, #0x0005
   57E4 09            [11]  250 	add	hl,bc
   57E5 DD 75 FE      [19]  251 	ld	-2 (ix), l
   57E8 DD 74 FF      [19]  252 	ld	-1 (ix), h
   57EB 21 01 00      [10]  253 	ld	hl, #0x0001
   57EE 09            [11]  254 	add	hl,bc
   57EF DD 75 FB      [19]  255 	ld	-5 (ix), l
   57F2 DD 74 FC      [19]  256 	ld	-4 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   57F5 21 03 00      [10]  258 	ld	hl, #0x0003
   57F8 09            [11]  259 	add	hl,bc
   57F9 DD 75 F8      [19]  260 	ld	-8 (ix), l
   57FC DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   57FF 21 08 00      [10]  263 	ld	hl, #0x0008
   5802 09            [11]  264 	add	hl,bc
   5803 DD 75 F6      [19]  265 	ld	-10 (ix), l
   5806 DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5809 DD 7E FD      [19]  268 	ld	a, -3 (ix)
   580C B7            [ 4]  269 	or	a, a
   580D 28 4E         [12]  270 	jr	Z,00123$
   580F DD 6E FE      [19]  271 	ld	l,-2 (ix)
   5812 DD 66 FF      [19]  272 	ld	h,-1 (ix)
   5815 7E            [ 7]  273 	ld	a, (hl)
   5816 DD 6E FB      [19]  274 	ld	l,-5 (ix)
   5819 DD 66 FC      [19]  275 	ld	h,-4 (ix)
   581C 6E            [ 7]  276 	ld	l, (hl)
   581D DD 75 F4      [19]  277 	ld	-12 (ix), l
   5820 DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   5824 F5            [11]  279 	push	af
   5825 0A            [ 7]  280 	ld	a, (bc)
   5826 6F            [ 4]  281 	ld	l, a
   5827 F1            [10]  282 	pop	af
   5828 DD 75 F2      [19]  283 	ld	-14 (ix), l
   582B DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   582F C5            [11]  285 	push	bc
   5830 D5            [11]  286 	push	de
   5831 F5            [11]  287 	push	af
   5832 33            [ 6]  288 	inc	sp
   5833 DD 6E F4      [19]  289 	ld	l,-12 (ix)
   5836 DD 66 F5      [19]  290 	ld	h,-11 (ix)
   5839 E5            [11]  291 	push	hl
   583A DD 6E F2      [19]  292 	ld	l,-14 (ix)
   583D DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5840 E5            [11]  294 	push	hl
   5841 CD AA 4B      [17]  295 	call	_collision_is_on_ground_at
   5844 F1            [10]  296 	pop	af
   5845 F1            [10]  297 	pop	af
   5846 33            [ 6]  298 	inc	sp
   5847 D1            [10]  299 	pop	de
   5848 C1            [10]  300 	pop	bc
   5849 7D            [ 4]  301 	ld	a, l
   584A B7            [ 4]  302 	or	a, a
   584B 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   584D DD 6E F8      [19]  305 	ld	l,-8 (ix)
   5850 DD 66 F9      [19]  306 	ld	h,-7 (ix)
   5853 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   5855 DD 6E F6      [19]  309 	ld	l,-10 (ix)
   5858 DD 66 F7      [19]  310 	ld	h,-9 (ix)
   585B 36 05         [10]  311 	ld	(hl), #0x05
   585D                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   585D C5            [11]  314 	push	bc
   585E D5            [11]  315 	push	de
   585F CD F6 4F      [17]  316 	call	_input_is_jump_pressed
   5862 7D            [ 4]  317 	ld	a, l
   5863 D1            [10]  318 	pop	de
   5864 C1            [10]  319 	pop	bc
   5865 B7            [ 4]  320 	or	a, a
   5866 28 31         [12]  321 	jr	Z,00126$
   5868 DD 6E F6      [19]  322 	ld	l,-10 (ix)
   586B DD 66 F7      [19]  323 	ld	h,-9 (ix)
   586E 7E            [ 7]  324 	ld	a, (hl)
   586F B7            [ 4]  325 	or	a, a
   5870 28 27         [12]  326 	jr	Z,00126$
   5872 DD 6E F8      [19]  327 	ld	l,-8 (ix)
   5875 DD 66 F9      [19]  328 	ld	h,-7 (ix)
   5878 6E            [ 7]  329 	ld	l, (hl)
   5879 CB 7D         [ 8]  330 	bit	7, l
   587B 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   587D 7D            [ 4]  333 	ld	a, l
   587E C6 FF         [ 7]  334 	add	a, #0xff
   5880 DD 6E F8      [19]  335 	ld	l,-8 (ix)
   5883 DD 66 F9      [19]  336 	ld	h,-7 (ix)
   5886 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   5887 DD 6E F6      [19]  339 	ld	l,-10 (ix)
   588A DD 66 F7      [19]  340 	ld	h,-9 (ix)
   588D 7E            [ 7]  341 	ld	a, (hl)
   588E C6 FF         [ 7]  342 	add	a, #0xff
   5890 DD 6E F6      [19]  343 	ld	l,-10 (ix)
   5893 DD 66 F7      [19]  344 	ld	h,-9 (ix)
   5896 77            [ 7]  345 	ld	(hl), a
   5897 18 08         [12]  346 	jr	00127$
   5899                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   5899 DD 6E F6      [19]  349 	ld	l,-10 (ix)
   589C DD 66 F7      [19]  350 	ld	h,-9 (ix)
   589F 36 00         [10]  351 	ld	(hl), #0x00
   58A1                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   58A1 DD 6E F8      [19]  354 	ld	l,-8 (ix)
   58A4 DD 66 F9      [19]  355 	ld	h,-7 (ix)
   58A7 7E            [ 7]  356 	ld	a, (hl)
   58A8 3C            [ 4]  357 	inc	a
   58A9 DD 77 F2      [19]  358 	ld	-14 (ix), a
   58AC DD 6E F8      [19]  359 	ld	l,-8 (ix)
   58AF DD 66 F9      [19]  360 	ld	h,-7 (ix)
   58B2 DD 7E F2      [19]  361 	ld	a, -14 (ix)
   58B5 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58B6 3E 04         [ 7]  364 	ld	a, #0x04
   58B8 DD 96 F2      [19]  365 	sub	a, -14 (ix)
   58BB E2 C0 58      [10]  366 	jp	PO, 00226$
   58BE EE 80         [ 7]  367 	xor	a, #0x80
   58C0                     368 00226$:
   58C0 F2 CB 58      [10]  369 	jp	P, 00131$
   58C3 DD 6E F8      [19]  370 	ld	l,-8 (ix)
   58C6 DD 66 F9      [19]  371 	ld	h,-7 (ix)
   58C9 36 04         [10]  372 	ld	(hl), #0x04
   58CB                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   58CB 0A            [ 7]  375 	ld	a, (bc)
   58CC DD 77 F2      [19]  376 	ld	-14 (ix), a
   58CF DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58D3 1A            [ 7]  378 	ld	a, (de)
   58D4 5F            [ 4]  379 	ld	e, a
   58D5 17            [ 4]  380 	rla
   58D6 9F            [ 4]  381 	sbc	a, a
   58D7 57            [ 4]  382 	ld	d, a
   58D8 E1            [10]  383 	pop	hl
   58D9 E5            [11]  384 	push	hl
   58DA 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   58DB CB 7C         [ 8]  387 	bit	7, h
   58DD 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   58DF 21 00 00      [10]  390 	ld	hl, #0x0000
   58E2                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   58E2 3E 4C         [ 7]  393 	ld	a, #0x4c
   58E4 BD            [ 4]  394 	cp	a, l
   58E5 3E 00         [ 7]  395 	ld	a, #0x00
   58E7 9C            [ 4]  396 	sbc	a, h
   58E8 E2 ED 58      [10]  397 	jp	PO, 00227$
   58EB EE 80         [ 7]  398 	xor	a, #0x80
   58ED                     399 00227$:
   58ED F2 F3 58      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   58F0 21 4C 00      [10]  402 	ld	hl, #0x004c
   58F3                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   58F3 DD 75 F2      [19]  405 	ld	-14 (ix), l
   58F6 7D            [ 4]  406 	ld	a, l
   58F7 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   58F8 DD 6E FB      [19]  409 	ld	l,-5 (ix)
   58FB DD 66 FC      [19]  410 	ld	h,-4 (ix)
   58FE 5E            [ 7]  411 	ld	e, (hl)
   58FF 16 00         [ 7]  412 	ld	d, #0x00
   5901 DD 6E F8      [19]  413 	ld	l,-8 (ix)
   5904 DD 66 F9      [19]  414 	ld	h,-7 (ix)
   5907 6E            [ 7]  415 	ld	l, (hl)
   5908 7D            [ 4]  416 	ld	a, l
   5909 17            [ 4]  417 	rla
   590A 9F            [ 4]  418 	sbc	a, a
   590B 67            [ 4]  419 	ld	h, a
   590C 19            [11]  420 	add	hl, de
   590D E5            [11]  421 	push	hl
   590E FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5910 DD 6E FE      [19]  424 	ld	l,-2 (ix)
   5913 DD 66 FF      [19]  425 	ld	h,-1 (ix)
   5916 66            [ 7]  426 	ld	h, (hl)
   5917 DD 5E F2      [19]  427 	ld	e, -14 (ix)
   591A 16 00         [ 7]  428 	ld	d, #0x00
   591C C5            [11]  429 	push	bc
   591D E5            [11]  430 	push	hl
   591E 33            [ 6]  431 	inc	sp
   591F FD E5         [15]  432 	push	iy
   5921 D5            [11]  433 	push	de
   5922 CD 29 4C      [17]  434 	call	_collision_clamp_y_at
   5925 F1            [10]  435 	pop	af
   5926 F1            [10]  436 	pop	af
   5927 33            [ 6]  437 	inc	sp
   5928 C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   5929 CB 7C         [ 8]  440 	bit	7, h
   592B 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   592D 21 00 00      [10]  443 	ld	hl, #0x0000
   5930                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   5930 5D            [ 4]  446 	ld	e, l
   5931 DD 6E FB      [19]  447 	ld	l,-5 (ix)
   5934 DD 66 FC      [19]  448 	ld	h,-4 (ix)
   5937 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5938 DD 6E FE      [19]  451 	ld	l,-2 (ix)
   593B DD 66 FF      [19]  452 	ld	h,-1 (ix)
   593E 7E            [ 7]  453 	ld	a, (hl)
   593F 16 00         [ 7]  454 	ld	d, #0x00
   5941 F5            [11]  455 	push	af
   5942 0A            [ 7]  456 	ld	a, (bc)
   5943 4F            [ 4]  457 	ld	c, a
   5944 F1            [10]  458 	pop	af
   5945 06 00         [ 7]  459 	ld	b, #0x00
   5947 F5            [11]  460 	push	af
   5948 33            [ 6]  461 	inc	sp
   5949 D5            [11]  462 	push	de
   594A C5            [11]  463 	push	bc
   594B CD AA 4B      [17]  464 	call	_collision_is_on_ground_at
   594E F1            [10]  465 	pop	af
   594F F1            [10]  466 	pop	af
   5950 33            [ 6]  467 	inc	sp
   5951 7D            [ 4]  468 	ld	a, l
   5952 B7            [ 4]  469 	or	a, a
   5953 28 19         [12]  470 	jr	Z,00141$
   5955 DD 6E F8      [19]  471 	ld	l,-8 (ix)
   5958 DD 66 F9      [19]  472 	ld	h,-7 (ix)
   595B 4E            [ 7]  473 	ld	c, (hl)
   595C AF            [ 4]  474 	xor	a, a
   595D 91            [ 4]  475 	sub	a, c
   595E E2 63 59      [10]  476 	jp	PO, 00228$
   5961 EE 80         [ 7]  477 	xor	a, #0x80
   5963                     478 00228$:
   5963 F2 6E 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   5966 DD 6E F8      [19]  481 	ld	l,-8 (ix)
   5969 DD 66 F9      [19]  482 	ld	h,-7 (ix)
   596C 36 00         [10]  483 	ld	(hl), #0x00
   596E                     484 00141$:
   596E DD F9         [10]  485 	ld	sp, ix
   5970 DD E1         [14]  486 	pop	ix
   5972 C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   5973                     492 _playerrender::
   5973 DD E5         [15]  493 	push	ix
   5975 DD 21 00 00   [14]  494 	ld	ix,#0
   5979 DD 39         [15]  495 	add	ix,sp
   597B 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   597C DD 7E 05      [19]  498 	ld	a, 5 (ix)
   597F DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   5982 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5984 DD 5E 04      [19]  503 	ld	e,4 (ix)
   5987 DD 56 05      [19]  504 	ld	d,5 (ix)
   598A 6B            [ 4]  505 	ld	l, e
   598B 62            [ 4]  506 	ld	h, d
   598C 23            [ 6]  507 	inc	hl
   598D 46            [ 7]  508 	ld	b, (hl)
   598E 1A            [ 7]  509 	ld	a, (de)
   598F D5            [11]  510 	push	de
   5990 C5            [11]  511 	push	bc
   5991 33            [ 6]  512 	inc	sp
   5992 F5            [11]  513 	push	af
   5993 33            [ 6]  514 	inc	sp
   5994 21 00 C0      [10]  515 	ld	hl, #0xc000
   5997 E5            [11]  516 	push	hl
   5998 CD 57 5E      [17]  517 	call	_cpct_getScreenPtr
   599B 4D            [ 4]  518 	ld	c, l
   599C 44            [ 4]  519 	ld	b, h
   599D D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   599E D5            [11]  522 	push	de
   599F FD E1         [14]  523 	pop	iy
   59A1 FD 7E 05      [19]  524 	ld	a, 5 (iy)
   59A4 DD 77 FF      [19]  525 	ld	-1 (ix), a
   59A7 EB            [ 4]  526 	ex	de,hl
   59A8 11 04 00      [10]  527 	ld	de, #0x0004
   59AB 19            [11]  528 	add	hl, de
   59AC 56            [ 7]  529 	ld	d, (hl)
   59AD C5            [11]  530 	push	bc
   59AE D5            [11]  531 	push	de
   59AF 21 06 06      [10]  532 	ld	hl, #0x0606
   59B2 E5            [11]  533 	push	hl
   59B3 CD 64 5D      [17]  534 	call	_cpct_px2byteM0
   59B6 5D            [ 4]  535 	ld	e, l
   59B7 F1            [10]  536 	pop	af
   59B8 57            [ 4]  537 	ld	d, a
   59B9 C1            [10]  538 	pop	bc
   59BA DD 7E FF      [19]  539 	ld	a, -1 (ix)
   59BD F5            [11]  540 	push	af
   59BE 33            [ 6]  541 	inc	sp
   59BF D5            [11]  542 	push	de
   59C0 C5            [11]  543 	push	bc
   59C1 CD 9E 5D      [17]  544 	call	_cpct_drawSolidBox
   59C4 F1            [10]  545 	pop	af
   59C5 F1            [10]  546 	pop	af
   59C6 33            [ 6]  547 	inc	sp
   59C7                     548 00103$:
   59C7 33            [ 6]  549 	inc	sp
   59C8 DD E1         [14]  550 	pop	ix
   59CA C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
