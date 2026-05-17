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
   56F2                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   56F2 21 03 00      [10]   60 	ld	hl, #2+1
   56F5 39            [11]   61 	add	hl, sp
   56F6 7E            [ 7]   62 	ld	a, (hl)
   56F7 2B            [ 6]   63 	dec	hl
   56F8 B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   56F9 C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   56FA D1            [10]   68 	pop	de
   56FB C1            [10]   69 	pop	bc
   56FC C5            [11]   70 	push	bc
   56FD D5            [11]   71 	push	de
   56FE 3E 14         [ 7]   72 	ld	a, #0x14
   5700 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   5701 69            [ 4]   75 	ld	l, c
   5702 60            [ 4]   76 	ld	h, b
   5703 23            [ 6]   77 	inc	hl
   5704 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   5706 59            [ 4]   80 	ld	e, c
   5707 50            [ 4]   81 	ld	d, b
   5708 13            [ 6]   82 	inc	de
   5709 13            [ 6]   83 	inc	de
   570A AF            [ 4]   84 	xor	a, a
   570B 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   570C 59            [ 4]   87 	ld	e, c
   570D 50            [ 4]   88 	ld	d, b
   570E 13            [ 6]   89 	inc	de
   570F 13            [ 6]   90 	inc	de
   5710 13            [ 6]   91 	inc	de
   5711 AF            [ 4]   92 	xor	a, a
   5712 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   5713 21 04 00      [10]   95 	ld	hl, #0x0004
   5716 09            [11]   96 	add	hl, bc
   5717 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   5719 21 05 00      [10]   99 	ld	hl, #0x0005
   571C 09            [11]  100 	add	hl, bc
   571D 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   571F 21 06 00      [10]  103 	ld	hl, #0x0006
   5722 09            [11]  104 	add	hl, bc
   5723 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   5725 21 07 00      [10]  107 	ld	hl, #0x0007
   5728 09            [11]  108 	add	hl, bc
   5729 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   572B 21 08 00      [10]  111 	ld	hl, #0x0008
   572E 09            [11]  112 	add	hl, bc
   572F 36 00         [10]  113 	ld	(hl), #0x00
   5731 C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   5732                     119 _playerupdate::
   5732 DD E5         [15]  120 	push	ix
   5734 DD 21 00 00   [14]  121 	ld	ix,#0
   5738 DD 39         [15]  122 	add	ix,sp
   573A 21 F2 FF      [10]  123 	ld	hl, #-14
   573D 39            [11]  124 	add	hl, sp
   573E F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   573F DD 7E 05      [19]  127 	ld	a, 5 (ix)
   5742 DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   5745 CA 79 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5748 CD ED 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   574B DD 4E 04      [19]  134 	ld	c,4 (ix)
   574E DD 46 05      [19]  135 	ld	b,5 (ix)
   5751 59            [ 4]  136 	ld	e, c
   5752 50            [ 4]  137 	ld	d, b
   5753 13            [ 6]  138 	inc	de
   5754 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   5755 79            [ 4]  141 	ld	a, c
   5756 C6 07         [ 7]  142 	add	a, #0x07
   5758 DD 77 FD      [19]  143 	ld	-3 (ix), a
   575B 78            [ 4]  144 	ld	a, b
   575C CE 00         [ 7]  145 	adc	a, #0x00
   575E DD 77 FE      [19]  146 	ld	-2 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5761 7D            [ 4]  148 	ld	a, l
   5762 B7            [ 4]  149 	or	a, a
   5763 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5765 1A            [ 7]  152 	ld	a, (de)
   5766 C6 FF         [ 7]  153 	add	a, #0xff
   5768 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   5769 DD 6E FD      [19]  156 	ld	l,-3 (ix)
   576C DD 66 FE      [19]  157 	ld	h,-2 (ix)
   576F 36 01         [10]  158 	ld	(hl), #0x01
   5771 18 55         [12]  159 	jr	00117$
   5773                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   5773 C5            [11]  162 	push	bc
   5774 D5            [11]  163 	push	de
   5775 CD F5 4F      [17]  164 	call	_input_is_right_pressed
   5778 DD 75 FF      [19]  165 	ld	-1 (ix), l
   577B D1            [10]  166 	pop	de
   577C C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   577D 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   577E 6F            [ 4]  171 	ld	l,a
   577F 3C            [ 4]  172 	inc	a
   5780 DD 77 FC      [19]  173 	ld	-4 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   5783 DD 7E FF      [19]  175 	ld	a, -1 (ix)
   5786 B7            [ 4]  176 	or	a, a
   5787 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5789 DD 7E FC      [19]  179 	ld	a, -4 (ix)
   578C 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   578D DD 6E FD      [19]  182 	ld	l,-3 (ix)
   5790 DD 66 FE      [19]  183 	ld	h,-2 (ix)
   5793 36 00         [10]  184 	ld	(hl), #0x00
   5795 18 31         [12]  185 	jr	00117$
   5797                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   5797 AF            [ 4]  188 	xor	a, a
   5798 95            [ 4]  189 	sub	a, l
   5799 E2 9E 57      [10]  190 	jp	PO, 00223$
   579C EE 80         [ 7]  191 	xor	a, #0x80
   579E                     192 00223$:
   579E F2 B2 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   57A1 7D            [ 4]  195 	ld	a, l
   57A2 C6 FF         [ 7]  196 	add	a, #0xff
   57A4 DD 77 FF      [19]  197 	ld	-1 (ix), a
   57A7 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   57A8 DD CB FF 7E   [20]  200 	bit	7, -1 (ix)
   57AC 28 1A         [12]  201 	jr	Z,00117$
   57AE AF            [ 4]  202 	xor	a, a
   57AF 12            [ 7]  203 	ld	(de), a
   57B0 18 16         [12]  204 	jr	00117$
   57B2                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   57B2 CB 7D         [ 8]  207 	bit	7, l
   57B4 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   57B6 DD 7E FC      [19]  210 	ld	a, -4 (ix)
   57B9 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   57BA AF            [ 4]  213 	xor	a, a
   57BB DD 96 FC      [19]  214 	sub	a, -4 (ix)
   57BE E2 C3 57      [10]  215 	jp	PO, 00224$
   57C1 EE 80         [ 7]  216 	xor	a, #0x80
   57C3                     217 00224$:
   57C3 F2 C8 57      [10]  218 	jp	P, 00117$
   57C6 AF            [ 4]  219 	xor	a, a
   57C7 12            [ 7]  220 	ld	(de), a
   57C8                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   57C8 1A            [ 7]  223 	ld	a, (de)
   57C9 6F            [ 4]  224 	ld	l, a
   57CA 3E 03         [ 7]  225 	ld	a, #0x03
   57CC 95            [ 4]  226 	sub	a, l
   57CD E2 D2 57      [10]  227 	jp	PO, 00225$
   57D0 EE 80         [ 7]  228 	xor	a, #0x80
   57D2                     229 00225$:
   57D2 F2 D8 57      [10]  230 	jp	P, 00119$
   57D5 3E 03         [ 7]  231 	ld	a, #0x03
   57D7 12            [ 7]  232 	ld	(de), a
   57D8                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   57D8 1A            [ 7]  235 	ld	a, (de)
   57D9 EE 80         [ 7]  236 	xor	a, #0x80
   57DB D6 7D         [ 7]  237 	sub	a, #0x7d
   57DD 30 03         [12]  238 	jr	NC,00121$
   57DF 3E FD         [ 7]  239 	ld	a, #0xfd
   57E1 12            [ 7]  240 	ld	(de), a
   57E2                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57E2 C5            [11]  243 	push	bc
   57E3 D5            [11]  244 	push	de
   57E4 CD 15 50      [17]  245 	call	_input_is_jump_just_pressed
   57E7 DD 75 FC      [19]  246 	ld	-4 (ix), l
   57EA D1            [10]  247 	pop	de
   57EB C1            [10]  248 	pop	bc
   57EC 21 05 00      [10]  249 	ld	hl, #0x0005
   57EF 09            [11]  250 	add	hl,bc
   57F0 DD 75 FD      [19]  251 	ld	-3 (ix), l
   57F3 DD 74 FE      [19]  252 	ld	-2 (ix), h
   57F6 21 01 00      [10]  253 	ld	hl, #0x0001
   57F9 09            [11]  254 	add	hl,bc
   57FA DD 75 FA      [19]  255 	ld	-6 (ix), l
   57FD DD 74 FB      [19]  256 	ld	-5 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5800 21 03 00      [10]  258 	ld	hl, #0x0003
   5803 09            [11]  259 	add	hl,bc
   5804 DD 75 F8      [19]  260 	ld	-8 (ix), l
   5807 DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   580A 21 08 00      [10]  263 	ld	hl, #0x0008
   580D 09            [11]  264 	add	hl,bc
   580E DD 75 F6      [19]  265 	ld	-10 (ix), l
   5811 DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5814 DD 7E FC      [19]  268 	ld	a, -4 (ix)
   5817 B7            [ 4]  269 	or	a, a
   5818 28 4E         [12]  270 	jr	Z,00123$
   581A DD 6E FD      [19]  271 	ld	l,-3 (ix)
   581D DD 66 FE      [19]  272 	ld	h,-2 (ix)
   5820 7E            [ 7]  273 	ld	a, (hl)
   5821 DD 6E FA      [19]  274 	ld	l,-6 (ix)
   5824 DD 66 FB      [19]  275 	ld	h,-5 (ix)
   5827 6E            [ 7]  276 	ld	l, (hl)
   5828 DD 75 F4      [19]  277 	ld	-12 (ix), l
   582B DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   582F F5            [11]  279 	push	af
   5830 0A            [ 7]  280 	ld	a, (bc)
   5831 6F            [ 4]  281 	ld	l, a
   5832 F1            [10]  282 	pop	af
   5833 DD 75 F2      [19]  283 	ld	-14 (ix), l
   5836 DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   583A C5            [11]  285 	push	bc
   583B D5            [11]  286 	push	de
   583C F5            [11]  287 	push	af
   583D 33            [ 6]  288 	inc	sp
   583E DD 6E F4      [19]  289 	ld	l,-12 (ix)
   5841 DD 66 F5      [19]  290 	ld	h,-11 (ix)
   5844 E5            [11]  291 	push	hl
   5845 DD 6E F2      [19]  292 	ld	l,-14 (ix)
   5848 DD 66 F3      [19]  293 	ld	h,-13 (ix)
   584B E5            [11]  294 	push	hl
   584C CD C1 4B      [17]  295 	call	_collision_is_on_ground_at
   584F F1            [10]  296 	pop	af
   5850 F1            [10]  297 	pop	af
   5851 33            [ 6]  298 	inc	sp
   5852 D1            [10]  299 	pop	de
   5853 C1            [10]  300 	pop	bc
   5854 7D            [ 4]  301 	ld	a, l
   5855 B7            [ 4]  302 	or	a, a
   5856 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5858 DD 6E F8      [19]  305 	ld	l,-8 (ix)
   585B DD 66 F9      [19]  306 	ld	h,-7 (ix)
   585E 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   5860 DD 6E F6      [19]  309 	ld	l,-10 (ix)
   5863 DD 66 F7      [19]  310 	ld	h,-9 (ix)
   5866 36 05         [10]  311 	ld	(hl), #0x05
   5868                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5868 C5            [11]  314 	push	bc
   5869 D5            [11]  315 	push	de
   586A CD 0D 50      [17]  316 	call	_input_is_jump_pressed
   586D 7D            [ 4]  317 	ld	a, l
   586E D1            [10]  318 	pop	de
   586F C1            [10]  319 	pop	bc
   5870 B7            [ 4]  320 	or	a, a
   5871 28 31         [12]  321 	jr	Z,00126$
   5873 DD 6E F6      [19]  322 	ld	l,-10 (ix)
   5876 DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5879 7E            [ 7]  324 	ld	a, (hl)
   587A B7            [ 4]  325 	or	a, a
   587B 28 27         [12]  326 	jr	Z,00126$
   587D DD 6E F8      [19]  327 	ld	l,-8 (ix)
   5880 DD 66 F9      [19]  328 	ld	h,-7 (ix)
   5883 6E            [ 7]  329 	ld	l, (hl)
   5884 CB 7D         [ 8]  330 	bit	7, l
   5886 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   5888 7D            [ 4]  333 	ld	a, l
   5889 C6 FF         [ 7]  334 	add	a, #0xff
   588B DD 6E F8      [19]  335 	ld	l,-8 (ix)
   588E DD 66 F9      [19]  336 	ld	h,-7 (ix)
   5891 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   5892 DD 6E F6      [19]  339 	ld	l,-10 (ix)
   5895 DD 66 F7      [19]  340 	ld	h,-9 (ix)
   5898 7E            [ 7]  341 	ld	a, (hl)
   5899 C6 FF         [ 7]  342 	add	a, #0xff
   589B DD 6E F6      [19]  343 	ld	l,-10 (ix)
   589E DD 66 F7      [19]  344 	ld	h,-9 (ix)
   58A1 77            [ 7]  345 	ld	(hl), a
   58A2 18 08         [12]  346 	jr	00127$
   58A4                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   58A4 DD 6E F6      [19]  349 	ld	l,-10 (ix)
   58A7 DD 66 F7      [19]  350 	ld	h,-9 (ix)
   58AA 36 00         [10]  351 	ld	(hl), #0x00
   58AC                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   58AC DD 6E F8      [19]  354 	ld	l,-8 (ix)
   58AF DD 66 F9      [19]  355 	ld	h,-7 (ix)
   58B2 7E            [ 7]  356 	ld	a, (hl)
   58B3 3C            [ 4]  357 	inc	a
   58B4 DD 77 F2      [19]  358 	ld	-14 (ix), a
   58B7 DD 6E F8      [19]  359 	ld	l,-8 (ix)
   58BA DD 66 F9      [19]  360 	ld	h,-7 (ix)
   58BD DD 7E F2      [19]  361 	ld	a, -14 (ix)
   58C0 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58C1 3E 04         [ 7]  364 	ld	a, #0x04
   58C3 DD 96 F2      [19]  365 	sub	a, -14 (ix)
   58C6 E2 CB 58      [10]  366 	jp	PO, 00226$
   58C9 EE 80         [ 7]  367 	xor	a, #0x80
   58CB                     368 00226$:
   58CB F2 D6 58      [10]  369 	jp	P, 00131$
   58CE DD 6E F8      [19]  370 	ld	l,-8 (ix)
   58D1 DD 66 F9      [19]  371 	ld	h,-7 (ix)
   58D4 36 04         [10]  372 	ld	(hl), #0x04
   58D6                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   58D6 0A            [ 7]  375 	ld	a, (bc)
   58D7 DD 77 F2      [19]  376 	ld	-14 (ix), a
   58DA DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58DE 1A            [ 7]  378 	ld	a, (de)
   58DF 5F            [ 4]  379 	ld	e, a
   58E0 17            [ 4]  380 	rla
   58E1 9F            [ 4]  381 	sbc	a, a
   58E2 57            [ 4]  382 	ld	d, a
   58E3 E1            [10]  383 	pop	hl
   58E4 E5            [11]  384 	push	hl
   58E5 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   58E6 CB 7C         [ 8]  387 	bit	7, h
   58E8 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   58EA 21 00 00      [10]  390 	ld	hl, #0x0000
   58ED                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   58ED 3E 4C         [ 7]  393 	ld	a, #0x4c
   58EF BD            [ 4]  394 	cp	a, l
   58F0 3E 00         [ 7]  395 	ld	a, #0x00
   58F2 9C            [ 4]  396 	sbc	a, h
   58F3 E2 F8 58      [10]  397 	jp	PO, 00227$
   58F6 EE 80         [ 7]  398 	xor	a, #0x80
   58F8                     399 00227$:
   58F8 F2 FE 58      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   58FB 21 4C 00      [10]  402 	ld	hl, #0x004c
   58FE                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   58FE DD 75 F2      [19]  405 	ld	-14 (ix), l
   5901 7D            [ 4]  406 	ld	a, l
   5902 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   5903 DD 6E FA      [19]  409 	ld	l,-6 (ix)
   5906 DD 66 FB      [19]  410 	ld	h,-5 (ix)
   5909 5E            [ 7]  411 	ld	e, (hl)
   590A 16 00         [ 7]  412 	ld	d, #0x00
   590C DD 6E F8      [19]  413 	ld	l,-8 (ix)
   590F DD 66 F9      [19]  414 	ld	h,-7 (ix)
   5912 6E            [ 7]  415 	ld	l, (hl)
   5913 7D            [ 4]  416 	ld	a, l
   5914 17            [ 4]  417 	rla
   5915 9F            [ 4]  418 	sbc	a, a
   5916 67            [ 4]  419 	ld	h, a
   5917 19            [11]  420 	add	hl, de
   5918 E5            [11]  421 	push	hl
   5919 FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   591B DD 6E FD      [19]  424 	ld	l,-3 (ix)
   591E DD 66 FE      [19]  425 	ld	h,-2 (ix)
   5921 66            [ 7]  426 	ld	h, (hl)
   5922 DD 5E F2      [19]  427 	ld	e, -14 (ix)
   5925 16 00         [ 7]  428 	ld	d, #0x00
   5927 C5            [11]  429 	push	bc
   5928 E5            [11]  430 	push	hl
   5929 33            [ 6]  431 	inc	sp
   592A FD E5         [15]  432 	push	iy
   592C D5            [11]  433 	push	de
   592D CD 40 4C      [17]  434 	call	_collision_clamp_y_at
   5930 F1            [10]  435 	pop	af
   5931 F1            [10]  436 	pop	af
   5932 33            [ 6]  437 	inc	sp
   5933 C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   5934 CB 7C         [ 8]  440 	bit	7, h
   5936 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   5938 21 00 00      [10]  443 	ld	hl, #0x0000
   593B                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   593B 5D            [ 4]  446 	ld	e, l
   593C DD 6E FA      [19]  447 	ld	l,-6 (ix)
   593F DD 66 FB      [19]  448 	ld	h,-5 (ix)
   5942 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5943 DD 6E FD      [19]  451 	ld	l,-3 (ix)
   5946 DD 66 FE      [19]  452 	ld	h,-2 (ix)
   5949 7E            [ 7]  453 	ld	a, (hl)
   594A 16 00         [ 7]  454 	ld	d, #0x00
   594C F5            [11]  455 	push	af
   594D 0A            [ 7]  456 	ld	a, (bc)
   594E 4F            [ 4]  457 	ld	c, a
   594F F1            [10]  458 	pop	af
   5950 06 00         [ 7]  459 	ld	b, #0x00
   5952 F5            [11]  460 	push	af
   5953 33            [ 6]  461 	inc	sp
   5954 D5            [11]  462 	push	de
   5955 C5            [11]  463 	push	bc
   5956 CD C1 4B      [17]  464 	call	_collision_is_on_ground_at
   5959 F1            [10]  465 	pop	af
   595A F1            [10]  466 	pop	af
   595B 33            [ 6]  467 	inc	sp
   595C 7D            [ 4]  468 	ld	a, l
   595D B7            [ 4]  469 	or	a, a
   595E 28 19         [12]  470 	jr	Z,00141$
   5960 DD 6E F8      [19]  471 	ld	l,-8 (ix)
   5963 DD 66 F9      [19]  472 	ld	h,-7 (ix)
   5966 4E            [ 7]  473 	ld	c, (hl)
   5967 AF            [ 4]  474 	xor	a, a
   5968 91            [ 4]  475 	sub	a, c
   5969 E2 6E 59      [10]  476 	jp	PO, 00228$
   596C EE 80         [ 7]  477 	xor	a, #0x80
   596E                     478 00228$:
   596E F2 79 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   5971 DD 6E F8      [19]  481 	ld	l,-8 (ix)
   5974 DD 66 F9      [19]  482 	ld	h,-7 (ix)
   5977 36 00         [10]  483 	ld	(hl), #0x00
   5979                     484 00141$:
   5979 DD F9         [10]  485 	ld	sp, ix
   597B DD E1         [14]  486 	pop	ix
   597D C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   597E                     492 _playerrender::
   597E DD E5         [15]  493 	push	ix
   5980 DD 21 00 00   [14]  494 	ld	ix,#0
   5984 DD 39         [15]  495 	add	ix,sp
   5986 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   5987 DD 7E 05      [19]  498 	ld	a, 5 (ix)
   598A DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   598D 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   598F DD 5E 04      [19]  503 	ld	e,4 (ix)
   5992 DD 56 05      [19]  504 	ld	d,5 (ix)
   5995 6B            [ 4]  505 	ld	l, e
   5996 62            [ 4]  506 	ld	h, d
   5997 23            [ 6]  507 	inc	hl
   5998 46            [ 7]  508 	ld	b, (hl)
   5999 1A            [ 7]  509 	ld	a, (de)
   599A D5            [11]  510 	push	de
   599B C5            [11]  511 	push	bc
   599C 33            [ 6]  512 	inc	sp
   599D F5            [11]  513 	push	af
   599E 33            [ 6]  514 	inc	sp
   599F 21 00 C0      [10]  515 	ld	hl, #0xc000
   59A2 E5            [11]  516 	push	hl
   59A3 CD 62 5E      [17]  517 	call	_cpct_getScreenPtr
   59A6 4D            [ 4]  518 	ld	c, l
   59A7 44            [ 4]  519 	ld	b, h
   59A8 D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   59A9 D5            [11]  522 	push	de
   59AA FD E1         [14]  523 	pop	iy
   59AC FD 7E 05      [19]  524 	ld	a, 5 (iy)
   59AF DD 77 FF      [19]  525 	ld	-1 (ix), a
   59B2 EB            [ 4]  526 	ex	de,hl
   59B3 11 04 00      [10]  527 	ld	de, #0x0004
   59B6 19            [11]  528 	add	hl, de
   59B7 56            [ 7]  529 	ld	d, (hl)
   59B8 C5            [11]  530 	push	bc
   59B9 D5            [11]  531 	push	de
   59BA 21 06 06      [10]  532 	ld	hl, #0x0606
   59BD E5            [11]  533 	push	hl
   59BE CD 6F 5D      [17]  534 	call	_cpct_px2byteM0
   59C1 5D            [ 4]  535 	ld	e, l
   59C2 F1            [10]  536 	pop	af
   59C3 57            [ 4]  537 	ld	d, a
   59C4 C1            [10]  538 	pop	bc
   59C5 DD 7E FF      [19]  539 	ld	a, -1 (ix)
   59C8 F5            [11]  540 	push	af
   59C9 33            [ 6]  541 	inc	sp
   59CA D5            [11]  542 	push	de
   59CB C5            [11]  543 	push	bc
   59CC CD A9 5D      [17]  544 	call	_cpct_drawSolidBox
   59CF F1            [10]  545 	pop	af
   59D0 F1            [10]  546 	pop	af
   59D1 33            [ 6]  547 	inc	sp
   59D2                     548 00103$:
   59D2 33            [ 6]  549 	inc	sp
   59D3 DD E1         [14]  550 	pop	ix
   59D5 C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
