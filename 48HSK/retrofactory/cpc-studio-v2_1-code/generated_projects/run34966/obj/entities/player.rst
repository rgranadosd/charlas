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
   570E                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   570E 21 03 00      [10]   60 	ld	hl, #2+1
   5711 39            [11]   61 	add	hl, sp
   5712 7E            [ 7]   62 	ld	a, (hl)
   5713 2B            [ 6]   63 	dec	hl
   5714 B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   5715 C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   5716 D1            [10]   68 	pop	de
   5717 C1            [10]   69 	pop	bc
   5718 C5            [11]   70 	push	bc
   5719 D5            [11]   71 	push	de
   571A 3E 14         [ 7]   72 	ld	a, #0x14
   571C 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   571D 69            [ 4]   75 	ld	l, c
   571E 60            [ 4]   76 	ld	h, b
   571F 23            [ 6]   77 	inc	hl
   5720 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   5722 59            [ 4]   80 	ld	e, c
   5723 50            [ 4]   81 	ld	d, b
   5724 13            [ 6]   82 	inc	de
   5725 13            [ 6]   83 	inc	de
   5726 AF            [ 4]   84 	xor	a, a
   5727 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   5728 59            [ 4]   87 	ld	e, c
   5729 50            [ 4]   88 	ld	d, b
   572A 13            [ 6]   89 	inc	de
   572B 13            [ 6]   90 	inc	de
   572C 13            [ 6]   91 	inc	de
   572D AF            [ 4]   92 	xor	a, a
   572E 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   572F 21 04 00      [10]   95 	ld	hl, #0x0004
   5732 09            [11]   96 	add	hl, bc
   5733 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   5735 21 05 00      [10]   99 	ld	hl, #0x0005
   5738 09            [11]  100 	add	hl, bc
   5739 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   573B 21 06 00      [10]  103 	ld	hl, #0x0006
   573E 09            [11]  104 	add	hl, bc
   573F 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   5741 21 07 00      [10]  107 	ld	hl, #0x0007
   5744 09            [11]  108 	add	hl, bc
   5745 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   5747 21 08 00      [10]  111 	ld	hl, #0x0008
   574A 09            [11]  112 	add	hl, bc
   574B 36 00         [10]  113 	ld	(hl), #0x00
   574D C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   574E                     119 _playerupdate::
   574E DD E5         [15]  120 	push	ix
   5750 DD 21 00 00   [14]  121 	ld	ix,#0
   5754 DD 39         [15]  122 	add	ix,sp
   5756 21 F2 FF      [10]  123 	ld	hl, #-14
   5759 39            [11]  124 	add	hl, sp
   575A F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   575B DD 7E 05      [19]  127 	ld	a, 5 (ix)
   575E DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   5761 CA 95 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5764 CD EF 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5767 DD 4E 04      [19]  134 	ld	c,4 (ix)
   576A DD 46 05      [19]  135 	ld	b,5 (ix)
   576D 59            [ 4]  136 	ld	e, c
   576E 50            [ 4]  137 	ld	d, b
   576F 13            [ 6]  138 	inc	de
   5770 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   5771 79            [ 4]  141 	ld	a, c
   5772 C6 07         [ 7]  142 	add	a, #0x07
   5774 DD 77 F8      [19]  143 	ld	-8 (ix), a
   5777 78            [ 4]  144 	ld	a, b
   5778 CE 00         [ 7]  145 	adc	a, #0x00
   577A DD 77 F9      [19]  146 	ld	-7 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   577D 7D            [ 4]  148 	ld	a, l
   577E B7            [ 4]  149 	or	a, a
   577F 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5781 1A            [ 7]  152 	ld	a, (de)
   5782 C6 FF         [ 7]  153 	add	a, #0xff
   5784 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   5785 DD 6E F8      [19]  156 	ld	l,-8 (ix)
   5788 DD 66 F9      [19]  157 	ld	h,-7 (ix)
   578B 36 01         [10]  158 	ld	(hl), #0x01
   578D 18 55         [12]  159 	jr	00117$
   578F                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   578F C5            [11]  162 	push	bc
   5790 D5            [11]  163 	push	de
   5791 CD F7 4F      [17]  164 	call	_input_is_right_pressed
   5794 DD 75 FF      [19]  165 	ld	-1 (ix), l
   5797 D1            [10]  166 	pop	de
   5798 C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5799 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   579A 6F            [ 4]  171 	ld	l,a
   579B 3C            [ 4]  172 	inc	a
   579C DD 77 FE      [19]  173 	ld	-2 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   579F DD 7E FF      [19]  175 	ld	a, -1 (ix)
   57A2 B7            [ 4]  176 	or	a, a
   57A3 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   57A5 DD 7E FE      [19]  179 	ld	a, -2 (ix)
   57A8 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   57A9 DD 6E F8      [19]  182 	ld	l,-8 (ix)
   57AC DD 66 F9      [19]  183 	ld	h,-7 (ix)
   57AF 36 00         [10]  184 	ld	(hl), #0x00
   57B1 18 31         [12]  185 	jr	00117$
   57B3                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   57B3 AF            [ 4]  188 	xor	a, a
   57B4 95            [ 4]  189 	sub	a, l
   57B5 E2 BA 57      [10]  190 	jp	PO, 00223$
   57B8 EE 80         [ 7]  191 	xor	a, #0x80
   57BA                     192 00223$:
   57BA F2 CE 57      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   57BD 7D            [ 4]  195 	ld	a, l
   57BE C6 FF         [ 7]  196 	add	a, #0xff
   57C0 DD 77 FF      [19]  197 	ld	-1 (ix), a
   57C3 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   57C4 DD CB FF 7E   [20]  200 	bit	7, -1 (ix)
   57C8 28 1A         [12]  201 	jr	Z,00117$
   57CA AF            [ 4]  202 	xor	a, a
   57CB 12            [ 7]  203 	ld	(de), a
   57CC 18 16         [12]  204 	jr	00117$
   57CE                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   57CE CB 7D         [ 8]  207 	bit	7, l
   57D0 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   57D2 DD 7E FE      [19]  210 	ld	a, -2 (ix)
   57D5 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   57D6 AF            [ 4]  213 	xor	a, a
   57D7 DD 96 FE      [19]  214 	sub	a, -2 (ix)
   57DA E2 DF 57      [10]  215 	jp	PO, 00224$
   57DD EE 80         [ 7]  216 	xor	a, #0x80
   57DF                     217 00224$:
   57DF F2 E4 57      [10]  218 	jp	P, 00117$
   57E2 AF            [ 4]  219 	xor	a, a
   57E3 12            [ 7]  220 	ld	(de), a
   57E4                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   57E4 1A            [ 7]  223 	ld	a, (de)
   57E5 6F            [ 4]  224 	ld	l, a
   57E6 3E 03         [ 7]  225 	ld	a, #0x03
   57E8 95            [ 4]  226 	sub	a, l
   57E9 E2 EE 57      [10]  227 	jp	PO, 00225$
   57EC EE 80         [ 7]  228 	xor	a, #0x80
   57EE                     229 00225$:
   57EE F2 F4 57      [10]  230 	jp	P, 00119$
   57F1 3E 03         [ 7]  231 	ld	a, #0x03
   57F3 12            [ 7]  232 	ld	(de), a
   57F4                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   57F4 1A            [ 7]  235 	ld	a, (de)
   57F5 EE 80         [ 7]  236 	xor	a, #0x80
   57F7 D6 7D         [ 7]  237 	sub	a, #0x7d
   57F9 30 03         [12]  238 	jr	NC,00121$
   57FB 3E FD         [ 7]  239 	ld	a, #0xfd
   57FD 12            [ 7]  240 	ld	(de), a
   57FE                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57FE C5            [11]  243 	push	bc
   57FF D5            [11]  244 	push	de
   5800 CD 17 50      [17]  245 	call	_input_is_jump_just_pressed
   5803 DD 75 FE      [19]  246 	ld	-2 (ix), l
   5806 D1            [10]  247 	pop	de
   5807 C1            [10]  248 	pop	bc
   5808 21 05 00      [10]  249 	ld	hl, #0x0005
   580B 09            [11]  250 	add	hl,bc
   580C DD 75 F8      [19]  251 	ld	-8 (ix), l
   580F DD 74 F9      [19]  252 	ld	-7 (ix), h
   5812 21 01 00      [10]  253 	ld	hl, #0x0001
   5815 09            [11]  254 	add	hl,bc
   5816 DD 75 FC      [19]  255 	ld	-4 (ix), l
   5819 DD 74 FD      [19]  256 	ld	-3 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   581C 21 03 00      [10]  258 	ld	hl, #0x0003
   581F 09            [11]  259 	add	hl,bc
   5820 DD 75 FA      [19]  260 	ld	-6 (ix), l
   5823 DD 74 FB      [19]  261 	ld	-5 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   5826 21 08 00      [10]  263 	ld	hl, #0x0008
   5829 09            [11]  264 	add	hl,bc
   582A DD 75 F6      [19]  265 	ld	-10 (ix), l
   582D DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5830 DD 7E FE      [19]  268 	ld	a, -2 (ix)
   5833 B7            [ 4]  269 	or	a, a
   5834 28 4E         [12]  270 	jr	Z,00123$
   5836 DD 6E F8      [19]  271 	ld	l,-8 (ix)
   5839 DD 66 F9      [19]  272 	ld	h,-7 (ix)
   583C 7E            [ 7]  273 	ld	a, (hl)
   583D DD 6E FC      [19]  274 	ld	l,-4 (ix)
   5840 DD 66 FD      [19]  275 	ld	h,-3 (ix)
   5843 6E            [ 7]  276 	ld	l, (hl)
   5844 DD 75 F4      [19]  277 	ld	-12 (ix), l
   5847 DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   584B F5            [11]  279 	push	af
   584C 0A            [ 7]  280 	ld	a, (bc)
   584D 6F            [ 4]  281 	ld	l, a
   584E F1            [10]  282 	pop	af
   584F DD 75 F2      [19]  283 	ld	-14 (ix), l
   5852 DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   5856 C5            [11]  285 	push	bc
   5857 D5            [11]  286 	push	de
   5858 F5            [11]  287 	push	af
   5859 33            [ 6]  288 	inc	sp
   585A DD 6E F4      [19]  289 	ld	l,-12 (ix)
   585D DD 66 F5      [19]  290 	ld	h,-11 (ix)
   5860 E5            [11]  291 	push	hl
   5861 DD 6E F2      [19]  292 	ld	l,-14 (ix)
   5864 DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5867 E5            [11]  294 	push	hl
   5868 CD C3 4B      [17]  295 	call	_collision_is_on_ground_at
   586B F1            [10]  296 	pop	af
   586C F1            [10]  297 	pop	af
   586D 33            [ 6]  298 	inc	sp
   586E D1            [10]  299 	pop	de
   586F C1            [10]  300 	pop	bc
   5870 7D            [ 4]  301 	ld	a, l
   5871 B7            [ 4]  302 	or	a, a
   5872 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5874 DD 6E FA      [19]  305 	ld	l,-6 (ix)
   5877 DD 66 FB      [19]  306 	ld	h,-5 (ix)
   587A 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   587C DD 6E F6      [19]  309 	ld	l,-10 (ix)
   587F DD 66 F7      [19]  310 	ld	h,-9 (ix)
   5882 36 05         [10]  311 	ld	(hl), #0x05
   5884                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5884 C5            [11]  314 	push	bc
   5885 D5            [11]  315 	push	de
   5886 CD 0F 50      [17]  316 	call	_input_is_jump_pressed
   5889 7D            [ 4]  317 	ld	a, l
   588A D1            [10]  318 	pop	de
   588B C1            [10]  319 	pop	bc
   588C B7            [ 4]  320 	or	a, a
   588D 28 31         [12]  321 	jr	Z,00126$
   588F DD 6E F6      [19]  322 	ld	l,-10 (ix)
   5892 DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5895 7E            [ 7]  324 	ld	a, (hl)
   5896 B7            [ 4]  325 	or	a, a
   5897 28 27         [12]  326 	jr	Z,00126$
   5899 DD 6E FA      [19]  327 	ld	l,-6 (ix)
   589C DD 66 FB      [19]  328 	ld	h,-5 (ix)
   589F 6E            [ 7]  329 	ld	l, (hl)
   58A0 CB 7D         [ 8]  330 	bit	7, l
   58A2 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   58A4 7D            [ 4]  333 	ld	a, l
   58A5 C6 FF         [ 7]  334 	add	a, #0xff
   58A7 DD 6E FA      [19]  335 	ld	l,-6 (ix)
   58AA DD 66 FB      [19]  336 	ld	h,-5 (ix)
   58AD 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   58AE DD 6E F6      [19]  339 	ld	l,-10 (ix)
   58B1 DD 66 F7      [19]  340 	ld	h,-9 (ix)
   58B4 7E            [ 7]  341 	ld	a, (hl)
   58B5 C6 FF         [ 7]  342 	add	a, #0xff
   58B7 DD 6E F6      [19]  343 	ld	l,-10 (ix)
   58BA DD 66 F7      [19]  344 	ld	h,-9 (ix)
   58BD 77            [ 7]  345 	ld	(hl), a
   58BE 18 08         [12]  346 	jr	00127$
   58C0                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   58C0 DD 6E F6      [19]  349 	ld	l,-10 (ix)
   58C3 DD 66 F7      [19]  350 	ld	h,-9 (ix)
   58C6 36 00         [10]  351 	ld	(hl), #0x00
   58C8                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   58C8 DD 6E FA      [19]  354 	ld	l,-6 (ix)
   58CB DD 66 FB      [19]  355 	ld	h,-5 (ix)
   58CE 7E            [ 7]  356 	ld	a, (hl)
   58CF 3C            [ 4]  357 	inc	a
   58D0 DD 77 F2      [19]  358 	ld	-14 (ix), a
   58D3 DD 6E FA      [19]  359 	ld	l,-6 (ix)
   58D6 DD 66 FB      [19]  360 	ld	h,-5 (ix)
   58D9 DD 7E F2      [19]  361 	ld	a, -14 (ix)
   58DC 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58DD 3E 04         [ 7]  364 	ld	a, #0x04
   58DF DD 96 F2      [19]  365 	sub	a, -14 (ix)
   58E2 E2 E7 58      [10]  366 	jp	PO, 00226$
   58E5 EE 80         [ 7]  367 	xor	a, #0x80
   58E7                     368 00226$:
   58E7 F2 F2 58      [10]  369 	jp	P, 00131$
   58EA DD 6E FA      [19]  370 	ld	l,-6 (ix)
   58ED DD 66 FB      [19]  371 	ld	h,-5 (ix)
   58F0 36 04         [10]  372 	ld	(hl), #0x04
   58F2                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   58F2 0A            [ 7]  375 	ld	a, (bc)
   58F3 DD 77 F2      [19]  376 	ld	-14 (ix), a
   58F6 DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   58FA 1A            [ 7]  378 	ld	a, (de)
   58FB 5F            [ 4]  379 	ld	e, a
   58FC 17            [ 4]  380 	rla
   58FD 9F            [ 4]  381 	sbc	a, a
   58FE 57            [ 4]  382 	ld	d, a
   58FF E1            [10]  383 	pop	hl
   5900 E5            [11]  384 	push	hl
   5901 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   5902 CB 7C         [ 8]  387 	bit	7, h
   5904 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   5906 21 00 00      [10]  390 	ld	hl, #0x0000
   5909                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   5909 3E 4C         [ 7]  393 	ld	a, #0x4c
   590B BD            [ 4]  394 	cp	a, l
   590C 3E 00         [ 7]  395 	ld	a, #0x00
   590E 9C            [ 4]  396 	sbc	a, h
   590F E2 14 59      [10]  397 	jp	PO, 00227$
   5912 EE 80         [ 7]  398 	xor	a, #0x80
   5914                     399 00227$:
   5914 F2 1A 59      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   5917 21 4C 00      [10]  402 	ld	hl, #0x004c
   591A                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   591A DD 75 F2      [19]  405 	ld	-14 (ix), l
   591D 7D            [ 4]  406 	ld	a, l
   591E 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   591F DD 6E FC      [19]  409 	ld	l,-4 (ix)
   5922 DD 66 FD      [19]  410 	ld	h,-3 (ix)
   5925 5E            [ 7]  411 	ld	e, (hl)
   5926 16 00         [ 7]  412 	ld	d, #0x00
   5928 DD 6E FA      [19]  413 	ld	l,-6 (ix)
   592B DD 66 FB      [19]  414 	ld	h,-5 (ix)
   592E 6E            [ 7]  415 	ld	l, (hl)
   592F 7D            [ 4]  416 	ld	a, l
   5930 17            [ 4]  417 	rla
   5931 9F            [ 4]  418 	sbc	a, a
   5932 67            [ 4]  419 	ld	h, a
   5933 19            [11]  420 	add	hl, de
   5934 E5            [11]  421 	push	hl
   5935 FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5937 DD 6E F8      [19]  424 	ld	l,-8 (ix)
   593A DD 66 F9      [19]  425 	ld	h,-7 (ix)
   593D 66            [ 7]  426 	ld	h, (hl)
   593E DD 5E F2      [19]  427 	ld	e, -14 (ix)
   5941 16 00         [ 7]  428 	ld	d, #0x00
   5943 C5            [11]  429 	push	bc
   5944 E5            [11]  430 	push	hl
   5945 33            [ 6]  431 	inc	sp
   5946 FD E5         [15]  432 	push	iy
   5948 D5            [11]  433 	push	de
   5949 CD 42 4C      [17]  434 	call	_collision_clamp_y_at
   594C F1            [10]  435 	pop	af
   594D F1            [10]  436 	pop	af
   594E 33            [ 6]  437 	inc	sp
   594F C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   5950 CB 7C         [ 8]  440 	bit	7, h
   5952 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   5954 21 00 00      [10]  443 	ld	hl, #0x0000
   5957                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   5957 5D            [ 4]  446 	ld	e, l
   5958 DD 6E FC      [19]  447 	ld	l,-4 (ix)
   595B DD 66 FD      [19]  448 	ld	h,-3 (ix)
   595E 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   595F DD 6E F8      [19]  451 	ld	l,-8 (ix)
   5962 DD 66 F9      [19]  452 	ld	h,-7 (ix)
   5965 7E            [ 7]  453 	ld	a, (hl)
   5966 16 00         [ 7]  454 	ld	d, #0x00
   5968 F5            [11]  455 	push	af
   5969 0A            [ 7]  456 	ld	a, (bc)
   596A 4F            [ 4]  457 	ld	c, a
   596B F1            [10]  458 	pop	af
   596C 06 00         [ 7]  459 	ld	b, #0x00
   596E F5            [11]  460 	push	af
   596F 33            [ 6]  461 	inc	sp
   5970 D5            [11]  462 	push	de
   5971 C5            [11]  463 	push	bc
   5972 CD C3 4B      [17]  464 	call	_collision_is_on_ground_at
   5975 F1            [10]  465 	pop	af
   5976 F1            [10]  466 	pop	af
   5977 33            [ 6]  467 	inc	sp
   5978 7D            [ 4]  468 	ld	a, l
   5979 B7            [ 4]  469 	or	a, a
   597A 28 19         [12]  470 	jr	Z,00141$
   597C DD 6E FA      [19]  471 	ld	l,-6 (ix)
   597F DD 66 FB      [19]  472 	ld	h,-5 (ix)
   5982 4E            [ 7]  473 	ld	c, (hl)
   5983 AF            [ 4]  474 	xor	a, a
   5984 91            [ 4]  475 	sub	a, c
   5985 E2 8A 59      [10]  476 	jp	PO, 00228$
   5988 EE 80         [ 7]  477 	xor	a, #0x80
   598A                     478 00228$:
   598A F2 95 59      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   598D DD 6E FA      [19]  481 	ld	l,-6 (ix)
   5990 DD 66 FB      [19]  482 	ld	h,-5 (ix)
   5993 36 00         [10]  483 	ld	(hl), #0x00
   5995                     484 00141$:
   5995 DD F9         [10]  485 	ld	sp, ix
   5997 DD E1         [14]  486 	pop	ix
   5999 C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   599A                     492 _playerrender::
   599A DD E5         [15]  493 	push	ix
   599C DD 21 00 00   [14]  494 	ld	ix,#0
   59A0 DD 39         [15]  495 	add	ix,sp
   59A2 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   59A3 DD 7E 05      [19]  498 	ld	a, 5 (ix)
   59A6 DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   59A9 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   59AB DD 5E 04      [19]  503 	ld	e,4 (ix)
   59AE DD 56 05      [19]  504 	ld	d,5 (ix)
   59B1 6B            [ 4]  505 	ld	l, e
   59B2 62            [ 4]  506 	ld	h, d
   59B3 23            [ 6]  507 	inc	hl
   59B4 46            [ 7]  508 	ld	b, (hl)
   59B5 1A            [ 7]  509 	ld	a, (de)
   59B6 D5            [11]  510 	push	de
   59B7 C5            [11]  511 	push	bc
   59B8 33            [ 6]  512 	inc	sp
   59B9 F5            [11]  513 	push	af
   59BA 33            [ 6]  514 	inc	sp
   59BB 21 00 C0      [10]  515 	ld	hl, #0xc000
   59BE E5            [11]  516 	push	hl
   59BF CD 7E 5E      [17]  517 	call	_cpct_getScreenPtr
   59C2 4D            [ 4]  518 	ld	c, l
   59C3 44            [ 4]  519 	ld	b, h
   59C4 D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   59C5 D5            [11]  522 	push	de
   59C6 FD E1         [14]  523 	pop	iy
   59C8 FD 7E 05      [19]  524 	ld	a, 5 (iy)
   59CB DD 77 FF      [19]  525 	ld	-1 (ix), a
   59CE EB            [ 4]  526 	ex	de,hl
   59CF 11 04 00      [10]  527 	ld	de, #0x0004
   59D2 19            [11]  528 	add	hl, de
   59D3 56            [ 7]  529 	ld	d, (hl)
   59D4 C5            [11]  530 	push	bc
   59D5 D5            [11]  531 	push	de
   59D6 21 06 06      [10]  532 	ld	hl, #0x0606
   59D9 E5            [11]  533 	push	hl
   59DA CD 8B 5D      [17]  534 	call	_cpct_px2byteM0
   59DD 5D            [ 4]  535 	ld	e, l
   59DE F1            [10]  536 	pop	af
   59DF 57            [ 4]  537 	ld	d, a
   59E0 C1            [10]  538 	pop	bc
   59E1 DD 7E FF      [19]  539 	ld	a, -1 (ix)
   59E4 F5            [11]  540 	push	af
   59E5 33            [ 6]  541 	inc	sp
   59E6 D5            [11]  542 	push	de
   59E7 C5            [11]  543 	push	bc
   59E8 CD C5 5D      [17]  544 	call	_cpct_drawSolidBox
   59EB F1            [10]  545 	pop	af
   59EC F1            [10]  546 	pop	af
   59ED 33            [ 6]  547 	inc	sp
   59EE                     548 00103$:
   59EE 33            [ 6]  549 	inc	sp
   59EF DD E1         [14]  550 	pop	ix
   59F1 C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
