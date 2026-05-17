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
   56D9                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   56D9 21 03 00      [10]   60 	ld	hl, #2+1
   56DC 39            [11]   61 	add	hl, sp
   56DD 7E            [ 7]   62 	ld	a, (hl)
   56DE 2B            [ 6]   63 	dec	hl
   56DF B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   56E0 C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   56E1 D1            [10]   68 	pop	de
   56E2 C1            [10]   69 	pop	bc
   56E3 C5            [11]   70 	push	bc
   56E4 D5            [11]   71 	push	de
   56E5 3E 14         [ 7]   72 	ld	a, #0x14
   56E7 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   56E8 69            [ 4]   75 	ld	l, c
   56E9 60            [ 4]   76 	ld	h, b
   56EA 23            [ 6]   77 	inc	hl
   56EB 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   56ED 59            [ 4]   80 	ld	e, c
   56EE 50            [ 4]   81 	ld	d, b
   56EF 13            [ 6]   82 	inc	de
   56F0 13            [ 6]   83 	inc	de
   56F1 AF            [ 4]   84 	xor	a, a
   56F2 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   56F3 59            [ 4]   87 	ld	e, c
   56F4 50            [ 4]   88 	ld	d, b
   56F5 13            [ 6]   89 	inc	de
   56F6 13            [ 6]   90 	inc	de
   56F7 13            [ 6]   91 	inc	de
   56F8 AF            [ 4]   92 	xor	a, a
   56F9 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   56FA 21 04 00      [10]   95 	ld	hl, #0x0004
   56FD 09            [11]   96 	add	hl, bc
   56FE 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   5700 21 05 00      [10]   99 	ld	hl, #0x0005
   5703 09            [11]  100 	add	hl, bc
   5704 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   5706 21 06 00      [10]  103 	ld	hl, #0x0006
   5709 09            [11]  104 	add	hl, bc
   570A 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   570C 21 07 00      [10]  107 	ld	hl, #0x0007
   570F 09            [11]  108 	add	hl, bc
   5710 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   5712 21 08 00      [10]  111 	ld	hl, #0x0008
   5715 09            [11]  112 	add	hl, bc
   5716 36 00         [10]  113 	ld	(hl), #0x00
   5718 C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   5719                     119 _playerupdate::
   5719 DD E5         [15]  120 	push	ix
   571B DD 21 00 00   [14]  121 	ld	ix,#0
   571F DD 39         [15]  122 	add	ix,sp
   5721 21 F2 FF      [10]  123 	ld	hl, #-14
   5724 39            [11]  124 	add	hl, sp
   5725 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   5726 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   5729 DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   572C CA 60 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   572F CD D6 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5732 DD 4E 04      [19]  134 	ld	c,4 (ix)
   5735 DD 46 05      [19]  135 	ld	b,5 (ix)
   5738 59            [ 4]  136 	ld	e, c
   5739 50            [ 4]  137 	ld	d, b
   573A 13            [ 6]  138 	inc	de
   573B 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   573C 79            [ 4]  141 	ld	a, c
   573D C6 07         [ 7]  142 	add	a, #0x07
   573F DD 77 FE      [19]  143 	ld	-2 (ix), a
   5742 78            [ 4]  144 	ld	a, b
   5743 CE 00         [ 7]  145 	adc	a, #0x00
   5745 DD 77 FF      [19]  146 	ld	-1 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5748 7D            [ 4]  148 	ld	a, l
   5749 B7            [ 4]  149 	or	a, a
   574A 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   574C 1A            [ 7]  152 	ld	a, (de)
   574D C6 FF         [ 7]  153 	add	a, #0xff
   574F 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   5750 DD 6E FE      [19]  156 	ld	l,-2 (ix)
   5753 DD 66 FF      [19]  157 	ld	h,-1 (ix)
   5756 36 01         [10]  158 	ld	(hl), #0x01
   5758 18 55         [12]  159 	jr	00117$
   575A                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   575A C5            [11]  162 	push	bc
   575B D5            [11]  163 	push	de
   575C CD DE 4F      [17]  164 	call	_input_is_right_pressed
   575F DD 75 FD      [19]  165 	ld	-3 (ix), l
   5762 D1            [10]  166 	pop	de
   5763 C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5764 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5765 6F            [ 4]  171 	ld	l,a
   5766 3C            [ 4]  172 	inc	a
   5767 DD 77 FC      [19]  173 	ld	-4 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   576A DD 7E FD      [19]  175 	ld	a, -3 (ix)
   576D B7            [ 4]  176 	or	a, a
   576E 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5770 DD 7E FC      [19]  179 	ld	a, -4 (ix)
   5773 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   5774 DD 6E FE      [19]  182 	ld	l,-2 (ix)
   5777 DD 66 FF      [19]  183 	ld	h,-1 (ix)
   577A 36 00         [10]  184 	ld	(hl), #0x00
   577C 18 31         [12]  185 	jr	00117$
   577E                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   577E AF            [ 4]  188 	xor	a, a
   577F 95            [ 4]  189 	sub	a, l
   5780 E2 85 57      [10]  190 	jp	PO, 00223$
   5783 EE 80         [ 7]  191 	xor	a, #0x80
   5785                     192 00223$:
   5785 F2 99 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   5788 7D            [ 4]  195 	ld	a, l
   5789 C6 FF         [ 7]  196 	add	a, #0xff
   578B DD 77 FD      [19]  197 	ld	-3 (ix), a
   578E 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   578F DD CB FD 7E   [20]  200 	bit	7, -3 (ix)
   5793 28 1A         [12]  201 	jr	Z,00117$
   5795 AF            [ 4]  202 	xor	a, a
   5796 12            [ 7]  203 	ld	(de), a
   5797 18 16         [12]  204 	jr	00117$
   5799                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   5799 CB 7D         [ 8]  207 	bit	7, l
   579B 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   579D DD 7E FC      [19]  210 	ld	a, -4 (ix)
   57A0 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   57A1 AF            [ 4]  213 	xor	a, a
   57A2 DD 96 FC      [19]  214 	sub	a, -4 (ix)
   57A5 E2 AA 57      [10]  215 	jp	PO, 00224$
   57A8 EE 80         [ 7]  216 	xor	a, #0x80
   57AA                     217 00224$:
   57AA F2 AF 57      [10]  218 	jp	P, 00117$
   57AD AF            [ 4]  219 	xor	a, a
   57AE 12            [ 7]  220 	ld	(de), a
   57AF                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   57AF 1A            [ 7]  223 	ld	a, (de)
   57B0 6F            [ 4]  224 	ld	l, a
   57B1 3E 03         [ 7]  225 	ld	a, #0x03
   57B3 95            [ 4]  226 	sub	a, l
   57B4 E2 B9 57      [10]  227 	jp	PO, 00225$
   57B7 EE 80         [ 7]  228 	xor	a, #0x80
   57B9                     229 00225$:
   57B9 F2 BF 57      [10]  230 	jp	P, 00119$
   57BC 3E 03         [ 7]  231 	ld	a, #0x03
   57BE 12            [ 7]  232 	ld	(de), a
   57BF                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   57BF 1A            [ 7]  235 	ld	a, (de)
   57C0 EE 80         [ 7]  236 	xor	a, #0x80
   57C2 D6 7D         [ 7]  237 	sub	a, #0x7d
   57C4 30 03         [12]  238 	jr	NC,00121$
   57C6 3E FD         [ 7]  239 	ld	a, #0xfd
   57C8 12            [ 7]  240 	ld	(de), a
   57C9                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57C9 C5            [11]  243 	push	bc
   57CA D5            [11]  244 	push	de
   57CB CD FE 4F      [17]  245 	call	_input_is_jump_just_pressed
   57CE DD 75 FC      [19]  246 	ld	-4 (ix), l
   57D1 D1            [10]  247 	pop	de
   57D2 C1            [10]  248 	pop	bc
   57D3 21 05 00      [10]  249 	ld	hl, #0x0005
   57D6 09            [11]  250 	add	hl,bc
   57D7 DD 75 FE      [19]  251 	ld	-2 (ix), l
   57DA DD 74 FF      [19]  252 	ld	-1 (ix), h
   57DD 21 01 00      [10]  253 	ld	hl, #0x0001
   57E0 09            [11]  254 	add	hl,bc
   57E1 DD 75 FA      [19]  255 	ld	-6 (ix), l
   57E4 DD 74 FB      [19]  256 	ld	-5 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   57E7 21 03 00      [10]  258 	ld	hl, #0x0003
   57EA 09            [11]  259 	add	hl,bc
   57EB DD 75 F8      [19]  260 	ld	-8 (ix), l
   57EE DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   57F1 21 08 00      [10]  263 	ld	hl, #0x0008
   57F4 09            [11]  264 	add	hl,bc
   57F5 DD 75 F6      [19]  265 	ld	-10 (ix), l
   57F8 DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57FB DD 7E FC      [19]  268 	ld	a, -4 (ix)
   57FE B7            [ 4]  269 	or	a, a
   57FF 28 4E         [12]  270 	jr	Z,00123$
   5801 DD 6E FE      [19]  271 	ld	l,-2 (ix)
   5804 DD 66 FF      [19]  272 	ld	h,-1 (ix)
   5807 7E            [ 7]  273 	ld	a, (hl)
   5808 DD 6E FA      [19]  274 	ld	l,-6 (ix)
   580B DD 66 FB      [19]  275 	ld	h,-5 (ix)
   580E 6E            [ 7]  276 	ld	l, (hl)
   580F DD 75 F4      [19]  277 	ld	-12 (ix), l
   5812 DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   5816 F5            [11]  279 	push	af
   5817 0A            [ 7]  280 	ld	a, (bc)
   5818 6F            [ 4]  281 	ld	l, a
   5819 F1            [10]  282 	pop	af
   581A DD 75 F2      [19]  283 	ld	-14 (ix), l
   581D DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   5821 C5            [11]  285 	push	bc
   5822 D5            [11]  286 	push	de
   5823 F5            [11]  287 	push	af
   5824 33            [ 6]  288 	inc	sp
   5825 DD 6E F4      [19]  289 	ld	l,-12 (ix)
   5828 DD 66 F5      [19]  290 	ld	h,-11 (ix)
   582B E5            [11]  291 	push	hl
   582C DD 6E F2      [19]  292 	ld	l,-14 (ix)
   582F DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5832 E5            [11]  294 	push	hl
   5833 CD AA 4B      [17]  295 	call	_collision_is_on_ground_at
   5836 F1            [10]  296 	pop	af
   5837 F1            [10]  297 	pop	af
   5838 33            [ 6]  298 	inc	sp
   5839 D1            [10]  299 	pop	de
   583A C1            [10]  300 	pop	bc
   583B 7D            [ 4]  301 	ld	a, l
   583C B7            [ 4]  302 	or	a, a
   583D 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   583F DD 6E F8      [19]  305 	ld	l,-8 (ix)
   5842 DD 66 F9      [19]  306 	ld	h,-7 (ix)
   5845 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   5847 DD 6E F6      [19]  309 	ld	l,-10 (ix)
   584A DD 66 F7      [19]  310 	ld	h,-9 (ix)
   584D 36 05         [10]  311 	ld	(hl), #0x05
   584F                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   584F C5            [11]  314 	push	bc
   5850 D5            [11]  315 	push	de
   5851 CD F6 4F      [17]  316 	call	_input_is_jump_pressed
   5854 7D            [ 4]  317 	ld	a, l
   5855 D1            [10]  318 	pop	de
   5856 C1            [10]  319 	pop	bc
   5857 B7            [ 4]  320 	or	a, a
   5858 28 31         [12]  321 	jr	Z,00126$
   585A DD 6E F6      [19]  322 	ld	l,-10 (ix)
   585D DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5860 7E            [ 7]  324 	ld	a, (hl)
   5861 B7            [ 4]  325 	or	a, a
   5862 28 27         [12]  326 	jr	Z,00126$
   5864 DD 6E F8      [19]  327 	ld	l,-8 (ix)
   5867 DD 66 F9      [19]  328 	ld	h,-7 (ix)
   586A 6E            [ 7]  329 	ld	l, (hl)
   586B CB 7D         [ 8]  330 	bit	7, l
   586D 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   586F 7D            [ 4]  333 	ld	a, l
   5870 C6 FF         [ 7]  334 	add	a, #0xff
   5872 DD 6E F8      [19]  335 	ld	l,-8 (ix)
   5875 DD 66 F9      [19]  336 	ld	h,-7 (ix)
   5878 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   5879 DD 6E F6      [19]  339 	ld	l,-10 (ix)
   587C DD 66 F7      [19]  340 	ld	h,-9 (ix)
   587F 7E            [ 7]  341 	ld	a, (hl)
   5880 C6 FF         [ 7]  342 	add	a, #0xff
   5882 DD 6E F6      [19]  343 	ld	l,-10 (ix)
   5885 DD 66 F7      [19]  344 	ld	h,-9 (ix)
   5888 77            [ 7]  345 	ld	(hl), a
   5889 18 08         [12]  346 	jr	00127$
   588B                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   588B DD 6E F6      [19]  349 	ld	l,-10 (ix)
   588E DD 66 F7      [19]  350 	ld	h,-9 (ix)
   5891 36 00         [10]  351 	ld	(hl), #0x00
   5893                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   5893 DD 6E F8      [19]  354 	ld	l,-8 (ix)
   5896 DD 66 F9      [19]  355 	ld	h,-7 (ix)
   5899 7E            [ 7]  356 	ld	a, (hl)
   589A 3C            [ 4]  357 	inc	a
   589B DD 77 F2      [19]  358 	ld	-14 (ix), a
   589E DD 6E F8      [19]  359 	ld	l,-8 (ix)
   58A1 DD 66 F9      [19]  360 	ld	h,-7 (ix)
   58A4 DD 7E F2      [19]  361 	ld	a, -14 (ix)
   58A7 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58A8 3E 04         [ 7]  364 	ld	a, #0x04
   58AA DD 96 F2      [19]  365 	sub	a, -14 (ix)
   58AD E2 B2 58      [10]  366 	jp	PO, 00226$
   58B0 EE 80         [ 7]  367 	xor	a, #0x80
   58B2                     368 00226$:
   58B2 F2 BD 58      [10]  369 	jp	P, 00131$
   58B5 DD 6E F8      [19]  370 	ld	l,-8 (ix)
   58B8 DD 66 F9      [19]  371 	ld	h,-7 (ix)
   58BB 36 04         [10]  372 	ld	(hl), #0x04
   58BD                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   58BD 0A            [ 7]  375 	ld	a, (bc)
   58BE DD 77 F2      [19]  376 	ld	-14 (ix), a
   58C1 DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58C5 1A            [ 7]  378 	ld	a, (de)
   58C6 5F            [ 4]  379 	ld	e, a
   58C7 17            [ 4]  380 	rla
   58C8 9F            [ 4]  381 	sbc	a, a
   58C9 57            [ 4]  382 	ld	d, a
   58CA E1            [10]  383 	pop	hl
   58CB E5            [11]  384 	push	hl
   58CC 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   58CD CB 7C         [ 8]  387 	bit	7, h
   58CF 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   58D1 21 00 00      [10]  390 	ld	hl, #0x0000
   58D4                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   58D4 3E 4C         [ 7]  393 	ld	a, #0x4c
   58D6 BD            [ 4]  394 	cp	a, l
   58D7 3E 00         [ 7]  395 	ld	a, #0x00
   58D9 9C            [ 4]  396 	sbc	a, h
   58DA E2 DF 58      [10]  397 	jp	PO, 00227$
   58DD EE 80         [ 7]  398 	xor	a, #0x80
   58DF                     399 00227$:
   58DF F2 E5 58      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   58E2 21 4C 00      [10]  402 	ld	hl, #0x004c
   58E5                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   58E5 DD 75 F2      [19]  405 	ld	-14 (ix), l
   58E8 7D            [ 4]  406 	ld	a, l
   58E9 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   58EA DD 6E FA      [19]  409 	ld	l,-6 (ix)
   58ED DD 66 FB      [19]  410 	ld	h,-5 (ix)
   58F0 5E            [ 7]  411 	ld	e, (hl)
   58F1 16 00         [ 7]  412 	ld	d, #0x00
   58F3 DD 6E F8      [19]  413 	ld	l,-8 (ix)
   58F6 DD 66 F9      [19]  414 	ld	h,-7 (ix)
   58F9 6E            [ 7]  415 	ld	l, (hl)
   58FA 7D            [ 4]  416 	ld	a, l
   58FB 17            [ 4]  417 	rla
   58FC 9F            [ 4]  418 	sbc	a, a
   58FD 67            [ 4]  419 	ld	h, a
   58FE 19            [11]  420 	add	hl, de
   58FF E5            [11]  421 	push	hl
   5900 FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5902 DD 6E FE      [19]  424 	ld	l,-2 (ix)
   5905 DD 66 FF      [19]  425 	ld	h,-1 (ix)
   5908 66            [ 7]  426 	ld	h, (hl)
   5909 DD 5E F2      [19]  427 	ld	e, -14 (ix)
   590C 16 00         [ 7]  428 	ld	d, #0x00
   590E C5            [11]  429 	push	bc
   590F E5            [11]  430 	push	hl
   5910 33            [ 6]  431 	inc	sp
   5911 FD E5         [15]  432 	push	iy
   5913 D5            [11]  433 	push	de
   5914 CD 29 4C      [17]  434 	call	_collision_clamp_y_at
   5917 F1            [10]  435 	pop	af
   5918 F1            [10]  436 	pop	af
   5919 33            [ 6]  437 	inc	sp
   591A C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   591B CB 7C         [ 8]  440 	bit	7, h
   591D 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   591F 21 00 00      [10]  443 	ld	hl, #0x0000
   5922                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   5922 5D            [ 4]  446 	ld	e, l
   5923 DD 6E FA      [19]  447 	ld	l,-6 (ix)
   5926 DD 66 FB      [19]  448 	ld	h,-5 (ix)
   5929 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   592A DD 6E FE      [19]  451 	ld	l,-2 (ix)
   592D DD 66 FF      [19]  452 	ld	h,-1 (ix)
   5930 7E            [ 7]  453 	ld	a, (hl)
   5931 16 00         [ 7]  454 	ld	d, #0x00
   5933 F5            [11]  455 	push	af
   5934 0A            [ 7]  456 	ld	a, (bc)
   5935 4F            [ 4]  457 	ld	c, a
   5936 F1            [10]  458 	pop	af
   5937 06 00         [ 7]  459 	ld	b, #0x00
   5939 F5            [11]  460 	push	af
   593A 33            [ 6]  461 	inc	sp
   593B D5            [11]  462 	push	de
   593C C5            [11]  463 	push	bc
   593D CD AA 4B      [17]  464 	call	_collision_is_on_ground_at
   5940 F1            [10]  465 	pop	af
   5941 F1            [10]  466 	pop	af
   5942 33            [ 6]  467 	inc	sp
   5943 7D            [ 4]  468 	ld	a, l
   5944 B7            [ 4]  469 	or	a, a
   5945 28 19         [12]  470 	jr	Z,00141$
   5947 DD 6E F8      [19]  471 	ld	l,-8 (ix)
   594A DD 66 F9      [19]  472 	ld	h,-7 (ix)
   594D 4E            [ 7]  473 	ld	c, (hl)
   594E AF            [ 4]  474 	xor	a, a
   594F 91            [ 4]  475 	sub	a, c
   5950 E2 55 59      [10]  476 	jp	PO, 00228$
   5953 EE 80         [ 7]  477 	xor	a, #0x80
   5955                     478 00228$:
   5955 F2 60 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   5958 DD 6E F8      [19]  481 	ld	l,-8 (ix)
   595B DD 66 F9      [19]  482 	ld	h,-7 (ix)
   595E 36 00         [10]  483 	ld	(hl), #0x00
   5960                     484 00141$:
   5960 DD F9         [10]  485 	ld	sp, ix
   5962 DD E1         [14]  486 	pop	ix
   5964 C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   5965                     492 _playerrender::
   5965 DD E5         [15]  493 	push	ix
   5967 DD 21 00 00   [14]  494 	ld	ix,#0
   596B DD 39         [15]  495 	add	ix,sp
   596D 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   596E DD 7E 05      [19]  498 	ld	a, 5 (ix)
   5971 DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   5974 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5976 DD 5E 04      [19]  503 	ld	e,4 (ix)
   5979 DD 56 05      [19]  504 	ld	d,5 (ix)
   597C 6B            [ 4]  505 	ld	l, e
   597D 62            [ 4]  506 	ld	h, d
   597E 23            [ 6]  507 	inc	hl
   597F 46            [ 7]  508 	ld	b, (hl)
   5980 1A            [ 7]  509 	ld	a, (de)
   5981 D5            [11]  510 	push	de
   5982 C5            [11]  511 	push	bc
   5983 33            [ 6]  512 	inc	sp
   5984 F5            [11]  513 	push	af
   5985 33            [ 6]  514 	inc	sp
   5986 21 00 C0      [10]  515 	ld	hl, #0xc000
   5989 E5            [11]  516 	push	hl
   598A CD 49 5E      [17]  517 	call	_cpct_getScreenPtr
   598D 4D            [ 4]  518 	ld	c, l
   598E 44            [ 4]  519 	ld	b, h
   598F D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   5990 D5            [11]  522 	push	de
   5991 FD E1         [14]  523 	pop	iy
   5993 FD 7E 05      [19]  524 	ld	a, 5 (iy)
   5996 DD 77 FF      [19]  525 	ld	-1 (ix), a
   5999 EB            [ 4]  526 	ex	de,hl
   599A 11 04 00      [10]  527 	ld	de, #0x0004
   599D 19            [11]  528 	add	hl, de
   599E 56            [ 7]  529 	ld	d, (hl)
   599F C5            [11]  530 	push	bc
   59A0 D5            [11]  531 	push	de
   59A1 21 06 06      [10]  532 	ld	hl, #0x0606
   59A4 E5            [11]  533 	push	hl
   59A5 CD 56 5D      [17]  534 	call	_cpct_px2byteM0
   59A8 5D            [ 4]  535 	ld	e, l
   59A9 F1            [10]  536 	pop	af
   59AA 57            [ 4]  537 	ld	d, a
   59AB C1            [10]  538 	pop	bc
   59AC DD 7E FF      [19]  539 	ld	a, -1 (ix)
   59AF F5            [11]  540 	push	af
   59B0 33            [ 6]  541 	inc	sp
   59B1 D5            [11]  542 	push	de
   59B2 C5            [11]  543 	push	bc
   59B3 CD 90 5D      [17]  544 	call	_cpct_drawSolidBox
   59B6 F1            [10]  545 	pop	af
   59B7 F1            [10]  546 	pop	af
   59B8 33            [ 6]  547 	inc	sp
   59B9                     548 00103$:
   59B9 33            [ 6]  549 	inc	sp
   59BA DD E1         [14]  550 	pop	ix
   59BC C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
