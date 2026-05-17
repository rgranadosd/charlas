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
   5765                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   5765 21 03 00      [10]   60 	ld	hl, #2+1
   5768 39            [11]   61 	add	hl, sp
   5769 7E            [ 7]   62 	ld	a, (hl)
   576A 2B            [ 6]   63 	dec	hl
   576B B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   576C C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   576D D1            [10]   68 	pop	de
   576E C1            [10]   69 	pop	bc
   576F C5            [11]   70 	push	bc
   5770 D5            [11]   71 	push	de
   5771 3E 14         [ 7]   72 	ld	a, #0x14
   5773 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   5774 69            [ 4]   75 	ld	l, c
   5775 60            [ 4]   76 	ld	h, b
   5776 23            [ 6]   77 	inc	hl
   5777 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   5779 59            [ 4]   80 	ld	e, c
   577A 50            [ 4]   81 	ld	d, b
   577B 13            [ 6]   82 	inc	de
   577C 13            [ 6]   83 	inc	de
   577D AF            [ 4]   84 	xor	a, a
   577E 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   577F 59            [ 4]   87 	ld	e, c
   5780 50            [ 4]   88 	ld	d, b
   5781 13            [ 6]   89 	inc	de
   5782 13            [ 6]   90 	inc	de
   5783 13            [ 6]   91 	inc	de
   5784 AF            [ 4]   92 	xor	a, a
   5785 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   5786 21 04 00      [10]   95 	ld	hl, #0x0004
   5789 09            [11]   96 	add	hl, bc
   578A 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   578C 21 05 00      [10]   99 	ld	hl, #0x0005
   578F 09            [11]  100 	add	hl, bc
   5790 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   5792 21 06 00      [10]  103 	ld	hl, #0x0006
   5795 09            [11]  104 	add	hl, bc
   5796 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   5798 21 07 00      [10]  107 	ld	hl, #0x0007
   579B 09            [11]  108 	add	hl, bc
   579C 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   579E 21 08 00      [10]  111 	ld	hl, #0x0008
   57A1 09            [11]  112 	add	hl, bc
   57A2 36 00         [10]  113 	ld	(hl), #0x00
   57A4 C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   57A5                     119 _playerupdate::
   57A5 DD E5         [15]  120 	push	ix
   57A7 DD 21 00 00   [14]  121 	ld	ix,#0
   57AB DD 39         [15]  122 	add	ix,sp
   57AD 21 F2 FF      [10]  123 	ld	hl, #-14
   57B0 39            [11]  124 	add	hl, sp
   57B1 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   57B2 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   57B5 DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   57B8 CA D7 59      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   57BB CD 61 50      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   57BE DD 4E 04      [19]  134 	ld	c,4 (ix)
   57C1 DD 46 05      [19]  135 	ld	b,5 (ix)
   57C4 59            [ 4]  136 	ld	e, c
   57C5 50            [ 4]  137 	ld	d, b
   57C6 13            [ 6]  138 	inc	de
   57C7 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   57C8 79            [ 4]  141 	ld	a, c
   57C9 C6 07         [ 7]  142 	add	a, #0x07
   57CB DD 77 F2      [19]  143 	ld	-14 (ix), a
   57CE 78            [ 4]  144 	ld	a, b
   57CF CE 00         [ 7]  145 	adc	a, #0x00
   57D1 DD 77 F3      [19]  146 	ld	-13 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   57D4 7D            [ 4]  148 	ld	a, l
   57D5 B7            [ 4]  149 	or	a, a
   57D6 28 0A         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   57D8 1A            [ 7]  152 	ld	a, (de)
   57D9 C6 FF         [ 7]  153 	add	a, #0xff
   57DB 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   57DC E1            [10]  156 	pop	hl
   57DD E5            [11]  157 	push	hl
   57DE 36 01         [10]  158 	ld	(hl), #0x01
   57E0 18 51         [12]  159 	jr	00117$
   57E2                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   57E2 C5            [11]  162 	push	bc
   57E3 D5            [11]  163 	push	de
   57E4 CD 69 50      [17]  164 	call	_input_is_right_pressed
   57E7 DD 75 FF      [19]  165 	ld	-1 (ix), l
   57EA D1            [10]  166 	pop	de
   57EB C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   57EC 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   57ED 6F            [ 4]  171 	ld	l,a
   57EE 3C            [ 4]  172 	inc	a
   57EF DD 77 FE      [19]  173 	ld	-2 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   57F2 DD 7E FF      [19]  175 	ld	a, -1 (ix)
   57F5 B7            [ 4]  176 	or	a, a
   57F6 28 0A         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   57F8 DD 7E FE      [19]  179 	ld	a, -2 (ix)
   57FB 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   57FC E1            [10]  182 	pop	hl
   57FD E5            [11]  183 	push	hl
   57FE 36 00         [10]  184 	ld	(hl), #0x00
   5800 18 31         [12]  185 	jr	00117$
   5802                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   5802 AF            [ 4]  188 	xor	a, a
   5803 95            [ 4]  189 	sub	a, l
   5804 E2 09 58      [10]  190 	jp	PO, 00223$
   5807 EE 80         [ 7]  191 	xor	a, #0x80
   5809                     192 00223$:
   5809 F2 1D 58      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   580C 7D            [ 4]  195 	ld	a, l
   580D C6 FF         [ 7]  196 	add	a, #0xff
   580F DD 77 FF      [19]  197 	ld	-1 (ix), a
   5812 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   5813 DD CB FF 7E   [20]  200 	bit	7, -1 (ix)
   5817 28 1A         [12]  201 	jr	Z,00117$
   5819 AF            [ 4]  202 	xor	a, a
   581A 12            [ 7]  203 	ld	(de), a
   581B 18 16         [12]  204 	jr	00117$
   581D                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   581D CB 7D         [ 8]  207 	bit	7, l
   581F 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   5821 DD 7E FE      [19]  210 	ld	a, -2 (ix)
   5824 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   5825 AF            [ 4]  213 	xor	a, a
   5826 DD 96 FE      [19]  214 	sub	a, -2 (ix)
   5829 E2 2E 58      [10]  215 	jp	PO, 00224$
   582C EE 80         [ 7]  216 	xor	a, #0x80
   582E                     217 00224$:
   582E F2 33 58      [10]  218 	jp	P, 00117$
   5831 AF            [ 4]  219 	xor	a, a
   5832 12            [ 7]  220 	ld	(de), a
   5833                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5833 1A            [ 7]  223 	ld	a, (de)
   5834 6F            [ 4]  224 	ld	l, a
   5835 3E 03         [ 7]  225 	ld	a, #0x03
   5837 95            [ 4]  226 	sub	a, l
   5838 E2 3D 58      [10]  227 	jp	PO, 00225$
   583B EE 80         [ 7]  228 	xor	a, #0x80
   583D                     229 00225$:
   583D F2 43 58      [10]  230 	jp	P, 00119$
   5840 3E 03         [ 7]  231 	ld	a, #0x03
   5842 12            [ 7]  232 	ld	(de), a
   5843                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5843 1A            [ 7]  235 	ld	a, (de)
   5844 EE 80         [ 7]  236 	xor	a, #0x80
   5846 D6 7D         [ 7]  237 	sub	a, #0x7d
   5848 30 03         [12]  238 	jr	NC,00121$
   584A 3E FD         [ 7]  239 	ld	a, #0xfd
   584C 12            [ 7]  240 	ld	(de), a
   584D                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   584D C5            [11]  243 	push	bc
   584E D5            [11]  244 	push	de
   584F CD 89 50      [17]  245 	call	_input_is_jump_just_pressed
   5852 DD 75 FE      [19]  246 	ld	-2 (ix), l
   5855 D1            [10]  247 	pop	de
   5856 C1            [10]  248 	pop	bc
   5857 21 05 00      [10]  249 	ld	hl, #0x0005
   585A 09            [11]  250 	add	hl,bc
   585B E3            [19]  251 	ex	(sp), hl
   585C 21 01 00      [10]  252 	ld	hl, #0x0001
   585F 09            [11]  253 	add	hl,bc
   5860 DD 75 FC      [19]  254 	ld	-4 (ix), l
   5863 DD 74 FD      [19]  255 	ld	-3 (ix), h
                            256 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5866 21 03 00      [10]  257 	ld	hl, #0x0003
   5869 09            [11]  258 	add	hl,bc
   586A DD 75 FA      [19]  259 	ld	-6 (ix), l
   586D DD 74 FB      [19]  260 	ld	-5 (ix), h
                            261 ;src/entities/player.c:59: player->jump_hold = 5;
   5870 21 08 00      [10]  262 	ld	hl, #0x0008
   5873 09            [11]  263 	add	hl,bc
   5874 DD 75 F8      [19]  264 	ld	-8 (ix), l
   5877 DD 74 F9      [19]  265 	ld	-7 (ix), h
                            266 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   587A DD 7E FE      [19]  267 	ld	a, -2 (ix)
   587D B7            [ 4]  268 	or	a, a
   587E 28 4A         [12]  269 	jr	Z,00123$
   5880 E1            [10]  270 	pop	hl
   5881 E5            [11]  271 	push	hl
   5882 7E            [ 7]  272 	ld	a, (hl)
   5883 DD 6E FC      [19]  273 	ld	l,-4 (ix)
   5886 DD 66 FD      [19]  274 	ld	h,-3 (ix)
   5889 6E            [ 7]  275 	ld	l, (hl)
   588A DD 75 F6      [19]  276 	ld	-10 (ix), l
   588D DD 36 F7 00   [19]  277 	ld	-9 (ix), #0x00
   5891 F5            [11]  278 	push	af
   5892 0A            [ 7]  279 	ld	a, (bc)
   5893 6F            [ 4]  280 	ld	l, a
   5894 F1            [10]  281 	pop	af
   5895 DD 75 F4      [19]  282 	ld	-12 (ix), l
   5898 DD 36 F5 00   [19]  283 	ld	-11 (ix), #0x00
   589C C5            [11]  284 	push	bc
   589D D5            [11]  285 	push	de
   589E F5            [11]  286 	push	af
   589F 33            [ 6]  287 	inc	sp
   58A0 DD 6E F6      [19]  288 	ld	l,-10 (ix)
   58A3 DD 66 F7      [19]  289 	ld	h,-9 (ix)
   58A6 E5            [11]  290 	push	hl
   58A7 DD 6E F4      [19]  291 	ld	l,-12 (ix)
   58AA DD 66 F5      [19]  292 	ld	h,-11 (ix)
   58AD E5            [11]  293 	push	hl
   58AE CD AE 4B      [17]  294 	call	_collision_is_on_ground_at
   58B1 F1            [10]  295 	pop	af
   58B2 F1            [10]  296 	pop	af
   58B3 33            [ 6]  297 	inc	sp
   58B4 D1            [10]  298 	pop	de
   58B5 C1            [10]  299 	pop	bc
   58B6 7D            [ 4]  300 	ld	a, l
   58B7 B7            [ 4]  301 	or	a, a
   58B8 28 10         [12]  302 	jr	Z,00123$
                            303 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   58BA DD 6E FA      [19]  304 	ld	l,-6 (ix)
   58BD DD 66 FB      [19]  305 	ld	h,-5 (ix)
   58C0 36 FA         [10]  306 	ld	(hl), #0xfa
                            307 ;src/entities/player.c:59: player->jump_hold = 5;
   58C2 DD 6E F8      [19]  308 	ld	l,-8 (ix)
   58C5 DD 66 F9      [19]  309 	ld	h,-7 (ix)
   58C8 36 05         [10]  310 	ld	(hl), #0x05
   58CA                     311 00123$:
                            312 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   58CA C5            [11]  313 	push	bc
   58CB D5            [11]  314 	push	de
   58CC CD 81 50      [17]  315 	call	_input_is_jump_pressed
   58CF 7D            [ 4]  316 	ld	a, l
   58D0 D1            [10]  317 	pop	de
   58D1 C1            [10]  318 	pop	bc
   58D2 B7            [ 4]  319 	or	a, a
   58D3 28 31         [12]  320 	jr	Z,00126$
   58D5 DD 6E F8      [19]  321 	ld	l,-8 (ix)
   58D8 DD 66 F9      [19]  322 	ld	h,-7 (ix)
   58DB 7E            [ 7]  323 	ld	a, (hl)
   58DC B7            [ 4]  324 	or	a, a
   58DD 28 27         [12]  325 	jr	Z,00126$
   58DF DD 6E FA      [19]  326 	ld	l,-6 (ix)
   58E2 DD 66 FB      [19]  327 	ld	h,-5 (ix)
   58E5 6E            [ 7]  328 	ld	l, (hl)
   58E6 CB 7D         [ 8]  329 	bit	7, l
   58E8 28 1C         [12]  330 	jr	Z,00126$
                            331 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   58EA 7D            [ 4]  332 	ld	a, l
   58EB C6 FF         [ 7]  333 	add	a, #0xff
   58ED DD 6E FA      [19]  334 	ld	l,-6 (ix)
   58F0 DD 66 FB      [19]  335 	ld	h,-5 (ix)
   58F3 77            [ 7]  336 	ld	(hl), a
                            337 ;src/entities/player.c:64: player->jump_hold--;
   58F4 DD 6E F8      [19]  338 	ld	l,-8 (ix)
   58F7 DD 66 F9      [19]  339 	ld	h,-7 (ix)
   58FA 7E            [ 7]  340 	ld	a, (hl)
   58FB C6 FF         [ 7]  341 	add	a, #0xff
   58FD DD 6E F8      [19]  342 	ld	l,-8 (ix)
   5900 DD 66 F9      [19]  343 	ld	h,-7 (ix)
   5903 77            [ 7]  344 	ld	(hl), a
   5904 18 08         [12]  345 	jr	00127$
   5906                     346 00126$:
                            347 ;src/entities/player.c:66: player->jump_hold = 0;
   5906 DD 6E F8      [19]  348 	ld	l,-8 (ix)
   5909 DD 66 F9      [19]  349 	ld	h,-7 (ix)
   590C 36 00         [10]  350 	ld	(hl), #0x00
   590E                     351 00127$:
                            352 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   590E DD 6E FA      [19]  353 	ld	l,-6 (ix)
   5911 DD 66 FB      [19]  354 	ld	h,-5 (ix)
   5914 7E            [ 7]  355 	ld	a, (hl)
   5915 3C            [ 4]  356 	inc	a
   5916 DD 77 F4      [19]  357 	ld	-12 (ix), a
   5919 DD 6E FA      [19]  358 	ld	l,-6 (ix)
   591C DD 66 FB      [19]  359 	ld	h,-5 (ix)
   591F DD 7E F4      [19]  360 	ld	a, -12 (ix)
   5922 77            [ 7]  361 	ld	(hl), a
                            362 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5923 3E 04         [ 7]  363 	ld	a, #0x04
   5925 DD 96 F4      [19]  364 	sub	a, -12 (ix)
   5928 E2 2D 59      [10]  365 	jp	PO, 00226$
   592B EE 80         [ 7]  366 	xor	a, #0x80
   592D                     367 00226$:
   592D F2 38 59      [10]  368 	jp	P, 00131$
   5930 DD 6E FA      [19]  369 	ld	l,-6 (ix)
   5933 DD 66 FB      [19]  370 	ld	h,-5 (ix)
   5936 36 04         [10]  371 	ld	(hl), #0x04
   5938                     372 00131$:
                            373 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   5938 0A            [ 7]  374 	ld	a, (bc)
   5939 DD 77 F4      [19]  375 	ld	-12 (ix), a
   593C DD 36 F5 00   [19]  376 	ld	-11 (ix), #0x00
   5940 1A            [ 7]  377 	ld	a, (de)
   5941 5F            [ 4]  378 	ld	e, a
   5942 17            [ 4]  379 	rla
   5943 9F            [ 4]  380 	sbc	a, a
   5944 57            [ 4]  381 	ld	d, a
   5945 DD 6E F4      [19]  382 	ld	l,-12 (ix)
   5948 DD 66 F5      [19]  383 	ld	h,-11 (ix)
   594B 19            [11]  384 	add	hl, de
                            385 ;src/entities/player.c:73: if (nextx < 0) {
   594C CB 7C         [ 8]  386 	bit	7, h
   594E 28 03         [12]  387 	jr	Z,00133$
                            388 ;src/entities/player.c:74: nextx = 0;
   5950 21 00 00      [10]  389 	ld	hl, #0x0000
   5953                     390 00133$:
                            391 ;src/entities/player.c:76: if (nextx > 76) {
   5953 3E 4C         [ 7]  392 	ld	a, #0x4c
   5955 BD            [ 4]  393 	cp	a, l
   5956 3E 00         [ 7]  394 	ld	a, #0x00
   5958 9C            [ 4]  395 	sbc	a, h
   5959 E2 5E 59      [10]  396 	jp	PO, 00227$
   595C EE 80         [ 7]  397 	xor	a, #0x80
   595E                     398 00227$:
   595E F2 64 59      [10]  399 	jp	P, 00135$
                            400 ;src/entities/player.c:77: nextx = 76;
   5961 21 4C 00      [10]  401 	ld	hl, #0x004c
   5964                     402 00135$:
                            403 ;src/entities/player.c:79: player->x = (u8)nextx;
   5964 DD 75 F4      [19]  404 	ld	-12 (ix), l
   5967 7D            [ 4]  405 	ld	a, l
   5968 02            [ 7]  406 	ld	(bc), a
                            407 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   5969 DD 6E FC      [19]  408 	ld	l,-4 (ix)
   596C DD 66 FD      [19]  409 	ld	h,-3 (ix)
   596F 5E            [ 7]  410 	ld	e, (hl)
   5970 16 00         [ 7]  411 	ld	d, #0x00
   5972 DD 6E FA      [19]  412 	ld	l,-6 (ix)
   5975 DD 66 FB      [19]  413 	ld	h,-5 (ix)
   5978 6E            [ 7]  414 	ld	l, (hl)
   5979 7D            [ 4]  415 	ld	a, l
   597A 17            [ 4]  416 	rla
   597B 9F            [ 4]  417 	sbc	a, a
   597C 67            [ 4]  418 	ld	h, a
   597D 19            [11]  419 	add	hl, de
   597E E5            [11]  420 	push	hl
   597F FD E1         [14]  421 	pop	iy
                            422 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5981 E1            [10]  423 	pop	hl
   5982 E5            [11]  424 	push	hl
   5983 66            [ 7]  425 	ld	h, (hl)
   5984 DD 5E F4      [19]  426 	ld	e, -12 (ix)
   5987 16 00         [ 7]  427 	ld	d, #0x00
   5989 C5            [11]  428 	push	bc
   598A E5            [11]  429 	push	hl
   598B 33            [ 6]  430 	inc	sp
   598C FD E5         [15]  431 	push	iy
   598E D5            [11]  432 	push	de
   598F CD 2D 4C      [17]  433 	call	_collision_clamp_y_at
   5992 F1            [10]  434 	pop	af
   5993 F1            [10]  435 	pop	af
   5994 33            [ 6]  436 	inc	sp
   5995 C1            [10]  437 	pop	bc
                            438 ;src/entities/player.c:83: if (nexty < 0) {
   5996 CB 7C         [ 8]  439 	bit	7, h
   5998 28 03         [12]  440 	jr	Z,00137$
                            441 ;src/entities/player.c:84: nexty = 0;
   599A 21 00 00      [10]  442 	ld	hl, #0x0000
   599D                     443 00137$:
                            444 ;src/entities/player.c:86: player->y = (u8)nexty;
   599D 5D            [ 4]  445 	ld	e, l
   599E DD 6E FC      [19]  446 	ld	l,-4 (ix)
   59A1 DD 66 FD      [19]  447 	ld	h,-3 (ix)
   59A4 73            [ 7]  448 	ld	(hl), e
                            449 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   59A5 E1            [10]  450 	pop	hl
   59A6 E5            [11]  451 	push	hl
   59A7 7E            [ 7]  452 	ld	a, (hl)
   59A8 16 00         [ 7]  453 	ld	d, #0x00
   59AA F5            [11]  454 	push	af
   59AB 0A            [ 7]  455 	ld	a, (bc)
   59AC 4F            [ 4]  456 	ld	c, a
   59AD F1            [10]  457 	pop	af
   59AE 06 00         [ 7]  458 	ld	b, #0x00
   59B0 F5            [11]  459 	push	af
   59B1 33            [ 6]  460 	inc	sp
   59B2 D5            [11]  461 	push	de
   59B3 C5            [11]  462 	push	bc
   59B4 CD AE 4B      [17]  463 	call	_collision_is_on_ground_at
   59B7 F1            [10]  464 	pop	af
   59B8 F1            [10]  465 	pop	af
   59B9 33            [ 6]  466 	inc	sp
   59BA 7D            [ 4]  467 	ld	a, l
   59BB B7            [ 4]  468 	or	a, a
   59BC 28 19         [12]  469 	jr	Z,00141$
   59BE DD 6E FA      [19]  470 	ld	l,-6 (ix)
   59C1 DD 66 FB      [19]  471 	ld	h,-5 (ix)
   59C4 4E            [ 7]  472 	ld	c, (hl)
   59C5 AF            [ 4]  473 	xor	a, a
   59C6 91            [ 4]  474 	sub	a, c
   59C7 E2 CC 59      [10]  475 	jp	PO, 00228$
   59CA EE 80         [ 7]  476 	xor	a, #0x80
   59CC                     477 00228$:
   59CC F2 D7 59      [10]  478 	jp	P, 00141$
                            479 ;src/entities/player.c:89: player->vy = 0;
   59CF DD 6E FA      [19]  480 	ld	l,-6 (ix)
   59D2 DD 66 FB      [19]  481 	ld	h,-5 (ix)
   59D5 36 00         [10]  482 	ld	(hl), #0x00
   59D7                     483 00141$:
   59D7 DD F9         [10]  484 	ld	sp, ix
   59D9 DD E1         [14]  485 	pop	ix
   59DB C9            [10]  486 	ret
                            487 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            488 ;	---------------------------------
                            489 ; Function playerrender
                            490 ; ---------------------------------
   59DC                     491 _playerrender::
   59DC DD E5         [15]  492 	push	ix
   59DE DD 21 00 00   [14]  493 	ld	ix,#0
   59E2 DD 39         [15]  494 	add	ix,sp
   59E4 3B            [ 6]  495 	dec	sp
                            496 ;src/entities/player.c:96: if (!player) {
   59E5 DD 7E 05      [19]  497 	ld	a, 5 (ix)
   59E8 DD B6 04      [19]  498 	or	a,4 (ix)
                            499 ;src/entities/player.c:97: return;
   59EB 28 43         [12]  500 	jr	Z,00103$
                            501 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   59ED DD 5E 04      [19]  502 	ld	e,4 (ix)
   59F0 DD 56 05      [19]  503 	ld	d,5 (ix)
   59F3 6B            [ 4]  504 	ld	l, e
   59F4 62            [ 4]  505 	ld	h, d
   59F5 23            [ 6]  506 	inc	hl
   59F6 46            [ 7]  507 	ld	b, (hl)
   59F7 1A            [ 7]  508 	ld	a, (de)
   59F8 D5            [11]  509 	push	de
   59F9 C5            [11]  510 	push	bc
   59FA 33            [ 6]  511 	inc	sp
   59FB F5            [11]  512 	push	af
   59FC 33            [ 6]  513 	inc	sp
   59FD 21 00 C0      [10]  514 	ld	hl, #0xc000
   5A00 E5            [11]  515 	push	hl
   5A01 CD A9 5E      [17]  516 	call	_cpct_getScreenPtr
   5A04 4D            [ 4]  517 	ld	c, l
   5A05 44            [ 4]  518 	ld	b, h
   5A06 D1            [10]  519 	pop	de
                            520 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   5A07 D5            [11]  521 	push	de
   5A08 FD E1         [14]  522 	pop	iy
   5A0A FD 7E 05      [19]  523 	ld	a, 5 (iy)
   5A0D DD 77 FF      [19]  524 	ld	-1 (ix), a
   5A10 EB            [ 4]  525 	ex	de,hl
   5A11 11 04 00      [10]  526 	ld	de, #0x0004
   5A14 19            [11]  527 	add	hl, de
   5A15 56            [ 7]  528 	ld	d, (hl)
   5A16 C5            [11]  529 	push	bc
   5A17 D5            [11]  530 	push	de
   5A18 21 06 06      [10]  531 	ld	hl, #0x0606
   5A1B E5            [11]  532 	push	hl
   5A1C CD B6 5D      [17]  533 	call	_cpct_px2byteM0
   5A1F 5D            [ 4]  534 	ld	e, l
   5A20 F1            [10]  535 	pop	af
   5A21 57            [ 4]  536 	ld	d, a
   5A22 C1            [10]  537 	pop	bc
   5A23 DD 7E FF      [19]  538 	ld	a, -1 (ix)
   5A26 F5            [11]  539 	push	af
   5A27 33            [ 6]  540 	inc	sp
   5A28 D5            [11]  541 	push	de
   5A29 C5            [11]  542 	push	bc
   5A2A CD F0 5D      [17]  543 	call	_cpct_drawSolidBox
   5A2D F1            [10]  544 	pop	af
   5A2E F1            [10]  545 	pop	af
   5A2F 33            [ 6]  546 	inc	sp
   5A30                     547 00103$:
   5A30 33            [ 6]  548 	inc	sp
   5A31 DD E1         [14]  549 	pop	ix
   5A33 C9            [10]  550 	ret
                            551 	.area _CODE
                            552 	.area _INITIALIZER
                            553 	.area _CABS (ABS)
