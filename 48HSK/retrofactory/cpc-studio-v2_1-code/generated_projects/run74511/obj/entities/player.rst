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
   56C9                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   56C9 21 03 00      [10]   60 	ld	hl, #2+1
   56CC 39            [11]   61 	add	hl, sp
   56CD 7E            [ 7]   62 	ld	a, (hl)
   56CE 2B            [ 6]   63 	dec	hl
   56CF B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   56D0 C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   56D1 D1            [10]   68 	pop	de
   56D2 C1            [10]   69 	pop	bc
   56D3 C5            [11]   70 	push	bc
   56D4 D5            [11]   71 	push	de
   56D5 3E 14         [ 7]   72 	ld	a, #0x14
   56D7 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   56D8 69            [ 4]   75 	ld	l, c
   56D9 60            [ 4]   76 	ld	h, b
   56DA 23            [ 6]   77 	inc	hl
   56DB 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   56DD 59            [ 4]   80 	ld	e, c
   56DE 50            [ 4]   81 	ld	d, b
   56DF 13            [ 6]   82 	inc	de
   56E0 13            [ 6]   83 	inc	de
   56E1 AF            [ 4]   84 	xor	a, a
   56E2 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   56E3 59            [ 4]   87 	ld	e, c
   56E4 50            [ 4]   88 	ld	d, b
   56E5 13            [ 6]   89 	inc	de
   56E6 13            [ 6]   90 	inc	de
   56E7 13            [ 6]   91 	inc	de
   56E8 AF            [ 4]   92 	xor	a, a
   56E9 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   56EA 21 04 00      [10]   95 	ld	hl, #0x0004
   56ED 09            [11]   96 	add	hl, bc
   56EE 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   56F0 21 05 00      [10]   99 	ld	hl, #0x0005
   56F3 09            [11]  100 	add	hl, bc
   56F4 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   56F6 21 06 00      [10]  103 	ld	hl, #0x0006
   56F9 09            [11]  104 	add	hl, bc
   56FA 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   56FC 21 07 00      [10]  107 	ld	hl, #0x0007
   56FF 09            [11]  108 	add	hl, bc
   5700 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   5702 21 08 00      [10]  111 	ld	hl, #0x0008
   5705 09            [11]  112 	add	hl, bc
   5706 36 00         [10]  113 	ld	(hl), #0x00
   5708 C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   5709                     119 _playerupdate::
   5709 DD E5         [15]  120 	push	ix
   570B DD 21 00 00   [14]  121 	ld	ix,#0
   570F DD 39         [15]  122 	add	ix,sp
   5711 21 F2 FF      [10]  123 	ld	hl, #-14
   5714 39            [11]  124 	add	hl, sp
   5715 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   5716 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   5719 DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   571C CA 50 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   571F CD D6 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5722 DD 4E 04      [19]  134 	ld	c,4 (ix)
   5725 DD 46 05      [19]  135 	ld	b,5 (ix)
   5728 59            [ 4]  136 	ld	e, c
   5729 50            [ 4]  137 	ld	d, b
   572A 13            [ 6]  138 	inc	de
   572B 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   572C 79            [ 4]  141 	ld	a, c
   572D C6 07         [ 7]  142 	add	a, #0x07
   572F DD 77 FE      [19]  143 	ld	-2 (ix), a
   5732 78            [ 4]  144 	ld	a, b
   5733 CE 00         [ 7]  145 	adc	a, #0x00
   5735 DD 77 FF      [19]  146 	ld	-1 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5738 7D            [ 4]  148 	ld	a, l
   5739 B7            [ 4]  149 	or	a, a
   573A 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   573C 1A            [ 7]  152 	ld	a, (de)
   573D C6 FF         [ 7]  153 	add	a, #0xff
   573F 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   5740 DD 6E FE      [19]  156 	ld	l,-2 (ix)
   5743 DD 66 FF      [19]  157 	ld	h,-1 (ix)
   5746 36 01         [10]  158 	ld	(hl), #0x01
   5748 18 55         [12]  159 	jr	00117$
   574A                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   574A C5            [11]  162 	push	bc
   574B D5            [11]  163 	push	de
   574C CD DE 4F      [17]  164 	call	_input_is_right_pressed
   574F DD 75 FD      [19]  165 	ld	-3 (ix), l
   5752 D1            [10]  166 	pop	de
   5753 C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5754 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5755 6F            [ 4]  171 	ld	l,a
   5756 3C            [ 4]  172 	inc	a
   5757 DD 77 FC      [19]  173 	ld	-4 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   575A DD 7E FD      [19]  175 	ld	a, -3 (ix)
   575D B7            [ 4]  176 	or	a, a
   575E 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5760 DD 7E FC      [19]  179 	ld	a, -4 (ix)
   5763 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   5764 DD 6E FE      [19]  182 	ld	l,-2 (ix)
   5767 DD 66 FF      [19]  183 	ld	h,-1 (ix)
   576A 36 00         [10]  184 	ld	(hl), #0x00
   576C 18 31         [12]  185 	jr	00117$
   576E                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   576E AF            [ 4]  188 	xor	a, a
   576F 95            [ 4]  189 	sub	a, l
   5770 E2 75 57      [10]  190 	jp	PO, 00223$
   5773 EE 80         [ 7]  191 	xor	a, #0x80
   5775                     192 00223$:
   5775 F2 89 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   5778 7D            [ 4]  195 	ld	a, l
   5779 C6 FF         [ 7]  196 	add	a, #0xff
   577B DD 77 FD      [19]  197 	ld	-3 (ix), a
   577E 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   577F DD CB FD 7E   [20]  200 	bit	7, -3 (ix)
   5783 28 1A         [12]  201 	jr	Z,00117$
   5785 AF            [ 4]  202 	xor	a, a
   5786 12            [ 7]  203 	ld	(de), a
   5787 18 16         [12]  204 	jr	00117$
   5789                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   5789 CB 7D         [ 8]  207 	bit	7, l
   578B 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   578D DD 7E FC      [19]  210 	ld	a, -4 (ix)
   5790 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   5791 AF            [ 4]  213 	xor	a, a
   5792 DD 96 FC      [19]  214 	sub	a, -4 (ix)
   5795 E2 9A 57      [10]  215 	jp	PO, 00224$
   5798 EE 80         [ 7]  216 	xor	a, #0x80
   579A                     217 00224$:
   579A F2 9F 57      [10]  218 	jp	P, 00117$
   579D AF            [ 4]  219 	xor	a, a
   579E 12            [ 7]  220 	ld	(de), a
   579F                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   579F 1A            [ 7]  223 	ld	a, (de)
   57A0 6F            [ 4]  224 	ld	l, a
   57A1 3E 03         [ 7]  225 	ld	a, #0x03
   57A3 95            [ 4]  226 	sub	a, l
   57A4 E2 A9 57      [10]  227 	jp	PO, 00225$
   57A7 EE 80         [ 7]  228 	xor	a, #0x80
   57A9                     229 00225$:
   57A9 F2 AF 57      [10]  230 	jp	P, 00119$
   57AC 3E 03         [ 7]  231 	ld	a, #0x03
   57AE 12            [ 7]  232 	ld	(de), a
   57AF                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   57AF 1A            [ 7]  235 	ld	a, (de)
   57B0 EE 80         [ 7]  236 	xor	a, #0x80
   57B2 D6 7D         [ 7]  237 	sub	a, #0x7d
   57B4 30 03         [12]  238 	jr	NC,00121$
   57B6 3E FD         [ 7]  239 	ld	a, #0xfd
   57B8 12            [ 7]  240 	ld	(de), a
   57B9                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57B9 C5            [11]  243 	push	bc
   57BA D5            [11]  244 	push	de
   57BB CD FE 4F      [17]  245 	call	_input_is_jump_just_pressed
   57BE DD 75 FC      [19]  246 	ld	-4 (ix), l
   57C1 D1            [10]  247 	pop	de
   57C2 C1            [10]  248 	pop	bc
   57C3 21 05 00      [10]  249 	ld	hl, #0x0005
   57C6 09            [11]  250 	add	hl,bc
   57C7 DD 75 FE      [19]  251 	ld	-2 (ix), l
   57CA DD 74 FF      [19]  252 	ld	-1 (ix), h
   57CD 21 01 00      [10]  253 	ld	hl, #0x0001
   57D0 09            [11]  254 	add	hl,bc
   57D1 DD 75 FA      [19]  255 	ld	-6 (ix), l
   57D4 DD 74 FB      [19]  256 	ld	-5 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   57D7 21 03 00      [10]  258 	ld	hl, #0x0003
   57DA 09            [11]  259 	add	hl,bc
   57DB DD 75 F8      [19]  260 	ld	-8 (ix), l
   57DE DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   57E1 21 08 00      [10]  263 	ld	hl, #0x0008
   57E4 09            [11]  264 	add	hl,bc
   57E5 DD 75 F6      [19]  265 	ld	-10 (ix), l
   57E8 DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57EB DD 7E FC      [19]  268 	ld	a, -4 (ix)
   57EE B7            [ 4]  269 	or	a, a
   57EF 28 4E         [12]  270 	jr	Z,00123$
   57F1 DD 6E FE      [19]  271 	ld	l,-2 (ix)
   57F4 DD 66 FF      [19]  272 	ld	h,-1 (ix)
   57F7 7E            [ 7]  273 	ld	a, (hl)
   57F8 DD 6E FA      [19]  274 	ld	l,-6 (ix)
   57FB DD 66 FB      [19]  275 	ld	h,-5 (ix)
   57FE 6E            [ 7]  276 	ld	l, (hl)
   57FF DD 75 F4      [19]  277 	ld	-12 (ix), l
   5802 DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   5806 F5            [11]  279 	push	af
   5807 0A            [ 7]  280 	ld	a, (bc)
   5808 6F            [ 4]  281 	ld	l, a
   5809 F1            [10]  282 	pop	af
   580A DD 75 F2      [19]  283 	ld	-14 (ix), l
   580D DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   5811 C5            [11]  285 	push	bc
   5812 D5            [11]  286 	push	de
   5813 F5            [11]  287 	push	af
   5814 33            [ 6]  288 	inc	sp
   5815 DD 6E F4      [19]  289 	ld	l,-12 (ix)
   5818 DD 66 F5      [19]  290 	ld	h,-11 (ix)
   581B E5            [11]  291 	push	hl
   581C DD 6E F2      [19]  292 	ld	l,-14 (ix)
   581F DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5822 E5            [11]  294 	push	hl
   5823 CD AA 4B      [17]  295 	call	_collision_is_on_ground_at
   5826 F1            [10]  296 	pop	af
   5827 F1            [10]  297 	pop	af
   5828 33            [ 6]  298 	inc	sp
   5829 D1            [10]  299 	pop	de
   582A C1            [10]  300 	pop	bc
   582B 7D            [ 4]  301 	ld	a, l
   582C B7            [ 4]  302 	or	a, a
   582D 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   582F DD 6E F8      [19]  305 	ld	l,-8 (ix)
   5832 DD 66 F9      [19]  306 	ld	h,-7 (ix)
   5835 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   5837 DD 6E F6      [19]  309 	ld	l,-10 (ix)
   583A DD 66 F7      [19]  310 	ld	h,-9 (ix)
   583D 36 05         [10]  311 	ld	(hl), #0x05
   583F                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   583F C5            [11]  314 	push	bc
   5840 D5            [11]  315 	push	de
   5841 CD F6 4F      [17]  316 	call	_input_is_jump_pressed
   5844 7D            [ 4]  317 	ld	a, l
   5845 D1            [10]  318 	pop	de
   5846 C1            [10]  319 	pop	bc
   5847 B7            [ 4]  320 	or	a, a
   5848 28 31         [12]  321 	jr	Z,00126$
   584A DD 6E F6      [19]  322 	ld	l,-10 (ix)
   584D DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5850 7E            [ 7]  324 	ld	a, (hl)
   5851 B7            [ 4]  325 	or	a, a
   5852 28 27         [12]  326 	jr	Z,00126$
   5854 DD 6E F8      [19]  327 	ld	l,-8 (ix)
   5857 DD 66 F9      [19]  328 	ld	h,-7 (ix)
   585A 6E            [ 7]  329 	ld	l, (hl)
   585B CB 7D         [ 8]  330 	bit	7, l
   585D 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   585F 7D            [ 4]  333 	ld	a, l
   5860 C6 FF         [ 7]  334 	add	a, #0xff
   5862 DD 6E F8      [19]  335 	ld	l,-8 (ix)
   5865 DD 66 F9      [19]  336 	ld	h,-7 (ix)
   5868 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   5869 DD 6E F6      [19]  339 	ld	l,-10 (ix)
   586C DD 66 F7      [19]  340 	ld	h,-9 (ix)
   586F 7E            [ 7]  341 	ld	a, (hl)
   5870 C6 FF         [ 7]  342 	add	a, #0xff
   5872 DD 6E F6      [19]  343 	ld	l,-10 (ix)
   5875 DD 66 F7      [19]  344 	ld	h,-9 (ix)
   5878 77            [ 7]  345 	ld	(hl), a
   5879 18 08         [12]  346 	jr	00127$
   587B                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   587B DD 6E F6      [19]  349 	ld	l,-10 (ix)
   587E DD 66 F7      [19]  350 	ld	h,-9 (ix)
   5881 36 00         [10]  351 	ld	(hl), #0x00
   5883                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   5883 DD 6E F8      [19]  354 	ld	l,-8 (ix)
   5886 DD 66 F9      [19]  355 	ld	h,-7 (ix)
   5889 7E            [ 7]  356 	ld	a, (hl)
   588A 3C            [ 4]  357 	inc	a
   588B DD 77 F2      [19]  358 	ld	-14 (ix), a
   588E DD 6E F8      [19]  359 	ld	l,-8 (ix)
   5891 DD 66 F9      [19]  360 	ld	h,-7 (ix)
   5894 DD 7E F2      [19]  361 	ld	a, -14 (ix)
   5897 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5898 3E 04         [ 7]  364 	ld	a, #0x04
   589A DD 96 F2      [19]  365 	sub	a, -14 (ix)
   589D E2 A2 58      [10]  366 	jp	PO, 00226$
   58A0 EE 80         [ 7]  367 	xor	a, #0x80
   58A2                     368 00226$:
   58A2 F2 AD 58      [10]  369 	jp	P, 00131$
   58A5 DD 6E F8      [19]  370 	ld	l,-8 (ix)
   58A8 DD 66 F9      [19]  371 	ld	h,-7 (ix)
   58AB 36 04         [10]  372 	ld	(hl), #0x04
   58AD                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   58AD 0A            [ 7]  375 	ld	a, (bc)
   58AE DD 77 F2      [19]  376 	ld	-14 (ix), a
   58B1 DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58B5 1A            [ 7]  378 	ld	a, (de)
   58B6 5F            [ 4]  379 	ld	e, a
   58B7 17            [ 4]  380 	rla
   58B8 9F            [ 4]  381 	sbc	a, a
   58B9 57            [ 4]  382 	ld	d, a
   58BA E1            [10]  383 	pop	hl
   58BB E5            [11]  384 	push	hl
   58BC 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   58BD CB 7C         [ 8]  387 	bit	7, h
   58BF 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   58C1 21 00 00      [10]  390 	ld	hl, #0x0000
   58C4                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   58C4 3E 4C         [ 7]  393 	ld	a, #0x4c
   58C6 BD            [ 4]  394 	cp	a, l
   58C7 3E 00         [ 7]  395 	ld	a, #0x00
   58C9 9C            [ 4]  396 	sbc	a, h
   58CA E2 CF 58      [10]  397 	jp	PO, 00227$
   58CD EE 80         [ 7]  398 	xor	a, #0x80
   58CF                     399 00227$:
   58CF F2 D5 58      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   58D2 21 4C 00      [10]  402 	ld	hl, #0x004c
   58D5                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   58D5 DD 75 F2      [19]  405 	ld	-14 (ix), l
   58D8 7D            [ 4]  406 	ld	a, l
   58D9 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   58DA DD 6E FA      [19]  409 	ld	l,-6 (ix)
   58DD DD 66 FB      [19]  410 	ld	h,-5 (ix)
   58E0 5E            [ 7]  411 	ld	e, (hl)
   58E1 16 00         [ 7]  412 	ld	d, #0x00
   58E3 DD 6E F8      [19]  413 	ld	l,-8 (ix)
   58E6 DD 66 F9      [19]  414 	ld	h,-7 (ix)
   58E9 6E            [ 7]  415 	ld	l, (hl)
   58EA 7D            [ 4]  416 	ld	a, l
   58EB 17            [ 4]  417 	rla
   58EC 9F            [ 4]  418 	sbc	a, a
   58ED 67            [ 4]  419 	ld	h, a
   58EE 19            [11]  420 	add	hl, de
   58EF E5            [11]  421 	push	hl
   58F0 FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   58F2 DD 6E FE      [19]  424 	ld	l,-2 (ix)
   58F5 DD 66 FF      [19]  425 	ld	h,-1 (ix)
   58F8 66            [ 7]  426 	ld	h, (hl)
   58F9 DD 5E F2      [19]  427 	ld	e, -14 (ix)
   58FC 16 00         [ 7]  428 	ld	d, #0x00
   58FE C5            [11]  429 	push	bc
   58FF E5            [11]  430 	push	hl
   5900 33            [ 6]  431 	inc	sp
   5901 FD E5         [15]  432 	push	iy
   5903 D5            [11]  433 	push	de
   5904 CD 29 4C      [17]  434 	call	_collision_clamp_y_at
   5907 F1            [10]  435 	pop	af
   5908 F1            [10]  436 	pop	af
   5909 33            [ 6]  437 	inc	sp
   590A C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   590B CB 7C         [ 8]  440 	bit	7, h
   590D 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   590F 21 00 00      [10]  443 	ld	hl, #0x0000
   5912                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   5912 5D            [ 4]  446 	ld	e, l
   5913 DD 6E FA      [19]  447 	ld	l,-6 (ix)
   5916 DD 66 FB      [19]  448 	ld	h,-5 (ix)
   5919 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   591A DD 6E FE      [19]  451 	ld	l,-2 (ix)
   591D DD 66 FF      [19]  452 	ld	h,-1 (ix)
   5920 7E            [ 7]  453 	ld	a, (hl)
   5921 16 00         [ 7]  454 	ld	d, #0x00
   5923 F5            [11]  455 	push	af
   5924 0A            [ 7]  456 	ld	a, (bc)
   5925 4F            [ 4]  457 	ld	c, a
   5926 F1            [10]  458 	pop	af
   5927 06 00         [ 7]  459 	ld	b, #0x00
   5929 F5            [11]  460 	push	af
   592A 33            [ 6]  461 	inc	sp
   592B D5            [11]  462 	push	de
   592C C5            [11]  463 	push	bc
   592D CD AA 4B      [17]  464 	call	_collision_is_on_ground_at
   5930 F1            [10]  465 	pop	af
   5931 F1            [10]  466 	pop	af
   5932 33            [ 6]  467 	inc	sp
   5933 7D            [ 4]  468 	ld	a, l
   5934 B7            [ 4]  469 	or	a, a
   5935 28 19         [12]  470 	jr	Z,00141$
   5937 DD 6E F8      [19]  471 	ld	l,-8 (ix)
   593A DD 66 F9      [19]  472 	ld	h,-7 (ix)
   593D 4E            [ 7]  473 	ld	c, (hl)
   593E AF            [ 4]  474 	xor	a, a
   593F 91            [ 4]  475 	sub	a, c
   5940 E2 45 59      [10]  476 	jp	PO, 00228$
   5943 EE 80         [ 7]  477 	xor	a, #0x80
   5945                     478 00228$:
   5945 F2 50 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   5948 DD 6E F8      [19]  481 	ld	l,-8 (ix)
   594B DD 66 F9      [19]  482 	ld	h,-7 (ix)
   594E 36 00         [10]  483 	ld	(hl), #0x00
   5950                     484 00141$:
   5950 DD F9         [10]  485 	ld	sp, ix
   5952 DD E1         [14]  486 	pop	ix
   5954 C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   5955                     492 _playerrender::
   5955 DD E5         [15]  493 	push	ix
   5957 DD 21 00 00   [14]  494 	ld	ix,#0
   595B DD 39         [15]  495 	add	ix,sp
   595D 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   595E DD 7E 05      [19]  498 	ld	a, 5 (ix)
   5961 DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   5964 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5966 DD 5E 04      [19]  503 	ld	e,4 (ix)
   5969 DD 56 05      [19]  504 	ld	d,5 (ix)
   596C 6B            [ 4]  505 	ld	l, e
   596D 62            [ 4]  506 	ld	h, d
   596E 23            [ 6]  507 	inc	hl
   596F 46            [ 7]  508 	ld	b, (hl)
   5970 1A            [ 7]  509 	ld	a, (de)
   5971 D5            [11]  510 	push	de
   5972 C5            [11]  511 	push	bc
   5973 33            [ 6]  512 	inc	sp
   5974 F5            [11]  513 	push	af
   5975 33            [ 6]  514 	inc	sp
   5976 21 00 C0      [10]  515 	ld	hl, #0xc000
   5979 E5            [11]  516 	push	hl
   597A CD 39 5E      [17]  517 	call	_cpct_getScreenPtr
   597D 4D            [ 4]  518 	ld	c, l
   597E 44            [ 4]  519 	ld	b, h
   597F D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   5980 D5            [11]  522 	push	de
   5981 FD E1         [14]  523 	pop	iy
   5983 FD 7E 05      [19]  524 	ld	a, 5 (iy)
   5986 DD 77 FF      [19]  525 	ld	-1 (ix), a
   5989 EB            [ 4]  526 	ex	de,hl
   598A 11 04 00      [10]  527 	ld	de, #0x0004
   598D 19            [11]  528 	add	hl, de
   598E 56            [ 7]  529 	ld	d, (hl)
   598F C5            [11]  530 	push	bc
   5990 D5            [11]  531 	push	de
   5991 21 06 06      [10]  532 	ld	hl, #0x0606
   5994 E5            [11]  533 	push	hl
   5995 CD 46 5D      [17]  534 	call	_cpct_px2byteM0
   5998 5D            [ 4]  535 	ld	e, l
   5999 F1            [10]  536 	pop	af
   599A 57            [ 4]  537 	ld	d, a
   599B C1            [10]  538 	pop	bc
   599C DD 7E FF      [19]  539 	ld	a, -1 (ix)
   599F F5            [11]  540 	push	af
   59A0 33            [ 6]  541 	inc	sp
   59A1 D5            [11]  542 	push	de
   59A2 C5            [11]  543 	push	bc
   59A3 CD 80 5D      [17]  544 	call	_cpct_drawSolidBox
   59A6 F1            [10]  545 	pop	af
   59A7 F1            [10]  546 	pop	af
   59A8 33            [ 6]  547 	inc	sp
   59A9                     548 00103$:
   59A9 33            [ 6]  549 	inc	sp
   59AA DD E1         [14]  550 	pop	ix
   59AC C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
