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
   5A54                      58 _playerinit::
                             59 ;src/entities/player.c:17: if (!player) {
   5A54 21 03 00      [10]   60 	ld	hl, #2+1
   5A57 39            [11]   61 	add	hl, sp
   5A58 7E            [ 7]   62 	ld	a, (hl)
   5A59 2B            [ 6]   63 	dec	hl
   5A5A B6            [ 7]   64 	or	a,(hl)
                             65 ;src/entities/player.c:18: return;
   5A5B C8            [11]   66 	ret	Z
                             67 ;src/entities/player.c:21: player->x = 20;
   5A5C D1            [10]   68 	pop	de
   5A5D C1            [10]   69 	pop	bc
   5A5E C5            [11]   70 	push	bc
   5A5F D5            [11]   71 	push	de
   5A60 3E 14         [ 7]   72 	ld	a, #0x14
   5A62 02            [ 7]   73 	ld	(bc), a
                             74 ;src/entities/player.c:22: player->y = 120;
   5A63 69            [ 4]   75 	ld	l, c
   5A64 60            [ 4]   76 	ld	h, b
   5A65 23            [ 6]   77 	inc	hl
   5A66 36 78         [10]   78 	ld	(hl), #0x78
                             79 ;src/entities/player.c:23: player->vx = 0;
   5A68 59            [ 4]   80 	ld	e, c
   5A69 50            [ 4]   81 	ld	d, b
   5A6A 13            [ 6]   82 	inc	de
   5A6B 13            [ 6]   83 	inc	de
   5A6C AF            [ 4]   84 	xor	a, a
   5A6D 12            [ 7]   85 	ld	(de), a
                             86 ;src/entities/player.c:24: player->vy = 0;
   5A6E 59            [ 4]   87 	ld	e, c
   5A6F 50            [ 4]   88 	ld	d, b
   5A70 13            [ 6]   89 	inc	de
   5A71 13            [ 6]   90 	inc	de
   5A72 13            [ 6]   91 	inc	de
   5A73 AF            [ 4]   92 	xor	a, a
   5A74 12            [ 7]   93 	ld	(de), a
                             94 ;src/entities/player.c:25: player->w = 4;
   5A75 21 04 00      [10]   95 	ld	hl, #0x0004
   5A78 09            [11]   96 	add	hl, bc
   5A79 36 04         [10]   97 	ld	(hl), #0x04
                             98 ;src/entities/player.c:26: player->h = 16;
   5A7B 21 05 00      [10]   99 	ld	hl, #0x0005
   5A7E 09            [11]  100 	add	hl, bc
   5A7F 36 10         [10]  101 	ld	(hl), #0x10
                            102 ;src/entities/player.c:27: player->health = 3;
   5A81 21 06 00      [10]  103 	ld	hl, #0x0006
   5A84 09            [11]  104 	add	hl, bc
   5A85 36 03         [10]  105 	ld	(hl), #0x03
                            106 ;src/entities/player.c:28: player->facing_left = 0;
   5A87 21 07 00      [10]  107 	ld	hl, #0x0007
   5A8A 09            [11]  108 	add	hl, bc
   5A8B 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/player.c:29: player->jump_hold = 0;
   5A8D 21 08 00      [10]  111 	ld	hl, #0x0008
   5A90 09            [11]  112 	add	hl, bc
   5A91 36 00         [10]  113 	ld	(hl), #0x00
   5A93 C9            [10]  114 	ret
                            115 ;src/entities/player.c:32: void playerupdate(Player* player) {
                            116 ;	---------------------------------
                            117 ; Function playerupdate
                            118 ; ---------------------------------
   5A94                     119 _playerupdate::
   5A94 DD E5         [15]  120 	push	ix
   5A96 DD 21 00 00   [14]  121 	ld	ix,#0
   5A9A DD 39         [15]  122 	add	ix,sp
   5A9C 21 F2 FF      [10]  123 	ld	hl, #-14
   5A9F 39            [11]  124 	add	hl, sp
   5AA0 F9            [ 6]  125 	ld	sp, hl
                            126 ;src/entities/player.c:36: if (!player) {
   5AA1 DD 7E 05      [19]  127 	ld	a, 5 (ix)
   5AA4 DD B6 04      [19]  128 	or	a,4 (ix)
                            129 ;src/entities/player.c:37: return;
   5AA7 CA DB 5C      [10]  130 	jp	Z,00141$
                            131 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5AAA CD F3 4F      [17]  132 	call	_input_is_left_pressed
                            133 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5AAD DD 4E 04      [19]  134 	ld	c,4 (ix)
   5AB0 DD 46 05      [19]  135 	ld	b,5 (ix)
   5AB3 59            [ 4]  136 	ld	e, c
   5AB4 50            [ 4]  137 	ld	d, b
   5AB5 13            [ 6]  138 	inc	de
   5AB6 13            [ 6]  139 	inc	de
                            140 ;src/entities/player.c:42: player->facing_left = 1;
   5AB7 79            [ 4]  141 	ld	a, c
   5AB8 C6 07         [ 7]  142 	add	a, #0x07
   5ABA DD 77 FC      [19]  143 	ld	-4 (ix), a
   5ABD 78            [ 4]  144 	ld	a, b
   5ABE CE 00         [ 7]  145 	adc	a, #0x00
   5AC0 DD 77 FD      [19]  146 	ld	-3 (ix), a
                            147 ;src/entities/player.c:40: if (input_is_left_pressed()) {
   5AC3 7D            [ 4]  148 	ld	a, l
   5AC4 B7            [ 4]  149 	or	a, a
   5AC5 28 0E         [12]  150 	jr	Z,00116$
                            151 ;src/entities/player.c:41: player->vx = (i8)(player->vx - kplayeracceleration);
   5AC7 1A            [ 7]  152 	ld	a, (de)
   5AC8 C6 FF         [ 7]  153 	add	a, #0xff
   5ACA 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/player.c:42: player->facing_left = 1;
   5ACB DD 6E FC      [19]  156 	ld	l,-4 (ix)
   5ACE DD 66 FD      [19]  157 	ld	h,-3 (ix)
   5AD1 36 01         [10]  158 	ld	(hl), #0x01
   5AD3 18 55         [12]  159 	jr	00117$
   5AD5                     160 00116$:
                            161 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   5AD5 C5            [11]  162 	push	bc
   5AD6 D5            [11]  163 	push	de
   5AD7 CD FB 4F      [17]  164 	call	_input_is_right_pressed
   5ADA DD 75 FF      [19]  165 	ld	-1 (ix), l
   5ADD D1            [10]  166 	pop	de
   5ADE C1            [10]  167 	pop	bc
                            168 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5ADF 1A            [ 7]  169 	ld	a, (de)
                            170 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5AE0 6F            [ 4]  171 	ld	l,a
   5AE1 3C            [ 4]  172 	inc	a
   5AE2 DD 77 FE      [19]  173 	ld	-2 (ix), a
                            174 ;src/entities/player.c:43: } else if (input_is_right_pressed()) {
   5AE5 DD 7E FF      [19]  175 	ld	a, -1 (ix)
   5AE8 B7            [ 4]  176 	or	a, a
   5AE9 28 0E         [12]  177 	jr	Z,00113$
                            178 ;src/entities/player.c:44: player->vx = (i8)(player->vx + kplayeracceleration);
   5AEB DD 7E FE      [19]  179 	ld	a, -2 (ix)
   5AEE 12            [ 7]  180 	ld	(de), a
                            181 ;src/entities/player.c:45: player->facing_left = 0;
   5AEF DD 6E FC      [19]  182 	ld	l,-4 (ix)
   5AF2 DD 66 FD      [19]  183 	ld	h,-3 (ix)
   5AF5 36 00         [10]  184 	ld	(hl), #0x00
   5AF7 18 31         [12]  185 	jr	00117$
   5AF9                     186 00113$:
                            187 ;src/entities/player.c:46: } else if (player->vx > 0) {
   5AF9 AF            [ 4]  188 	xor	a, a
   5AFA 95            [ 4]  189 	sub	a, l
   5AFB E2 00 5B      [10]  190 	jp	PO, 00223$
   5AFE EE 80         [ 7]  191 	xor	a, #0x80
   5B00                     192 00223$:
   5B00 F2 14 5B      [10]  193 	jp	P, 00110$
                            194 ;src/entities/player.c:47: player->vx = (i8)(player->vx - kplayerdeceleration);
   5B03 7D            [ 4]  195 	ld	a, l
   5B04 C6 FF         [ 7]  196 	add	a, #0xff
   5B06 DD 77 FF      [19]  197 	ld	-1 (ix), a
   5B09 12            [ 7]  198 	ld	(de),a
                            199 ;src/entities/player.c:48: if (player->vx < 0) player->vx = 0;
   5B0A DD CB FF 7E   [20]  200 	bit	7, -1 (ix)
   5B0E 28 1A         [12]  201 	jr	Z,00117$
   5B10 AF            [ 4]  202 	xor	a, a
   5B11 12            [ 7]  203 	ld	(de), a
   5B12 18 16         [12]  204 	jr	00117$
   5B14                     205 00110$:
                            206 ;src/entities/player.c:49: } else if (player->vx < 0) {
   5B14 CB 7D         [ 8]  207 	bit	7, l
   5B16 28 12         [12]  208 	jr	Z,00117$
                            209 ;src/entities/player.c:50: player->vx = (i8)(player->vx + kplayerdeceleration);
   5B18 DD 7E FE      [19]  210 	ld	a, -2 (ix)
   5B1B 12            [ 7]  211 	ld	(de), a
                            212 ;src/entities/player.c:51: if (player->vx > 0) player->vx = 0;
   5B1C AF            [ 4]  213 	xor	a, a
   5B1D DD 96 FE      [19]  214 	sub	a, -2 (ix)
   5B20 E2 25 5B      [10]  215 	jp	PO, 00224$
   5B23 EE 80         [ 7]  216 	xor	a, #0x80
   5B25                     217 00224$:
   5B25 F2 2A 5B      [10]  218 	jp	P, 00117$
   5B28 AF            [ 4]  219 	xor	a, a
   5B29 12            [ 7]  220 	ld	(de), a
   5B2A                     221 00117$:
                            222 ;src/entities/player.c:54: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5B2A 1A            [ 7]  223 	ld	a, (de)
   5B2B 6F            [ 4]  224 	ld	l, a
   5B2C 3E 03         [ 7]  225 	ld	a, #0x03
   5B2E 95            [ 4]  226 	sub	a, l
   5B2F E2 34 5B      [10]  227 	jp	PO, 00225$
   5B32 EE 80         [ 7]  228 	xor	a, #0x80
   5B34                     229 00225$:
   5B34 F2 3A 5B      [10]  230 	jp	P, 00119$
   5B37 3E 03         [ 7]  231 	ld	a, #0x03
   5B39 12            [ 7]  232 	ld	(de), a
   5B3A                     233 00119$:
                            234 ;src/entities/player.c:55: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5B3A 1A            [ 7]  235 	ld	a, (de)
   5B3B EE 80         [ 7]  236 	xor	a, #0x80
   5B3D D6 7D         [ 7]  237 	sub	a, #0x7d
   5B3F 30 03         [12]  238 	jr	NC,00121$
   5B41 3E FD         [ 7]  239 	ld	a, #0xfd
   5B43 12            [ 7]  240 	ld	(de), a
   5B44                     241 00121$:
                            242 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5B44 C5            [11]  243 	push	bc
   5B45 D5            [11]  244 	push	de
   5B46 CD 1B 50      [17]  245 	call	_input_is_jump_just_pressed
   5B49 DD 75 FE      [19]  246 	ld	-2 (ix), l
   5B4C D1            [10]  247 	pop	de
   5B4D C1            [10]  248 	pop	bc
   5B4E 21 05 00      [10]  249 	ld	hl, #0x0005
   5B51 09            [11]  250 	add	hl,bc
   5B52 DD 75 FC      [19]  251 	ld	-4 (ix), l
   5B55 DD 74 FD      [19]  252 	ld	-3 (ix), h
   5B58 21 01 00      [10]  253 	ld	hl, #0x0001
   5B5B 09            [11]  254 	add	hl,bc
   5B5C DD 75 FA      [19]  255 	ld	-6 (ix), l
   5B5F DD 74 FB      [19]  256 	ld	-5 (ix), h
                            257 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5B62 21 03 00      [10]  258 	ld	hl, #0x0003
   5B65 09            [11]  259 	add	hl,bc
   5B66 DD 75 F8      [19]  260 	ld	-8 (ix), l
   5B69 DD 74 F9      [19]  261 	ld	-7 (ix), h
                            262 ;src/entities/player.c:59: player->jump_hold = 5;
   5B6C 21 08 00      [10]  263 	ld	hl, #0x0008
   5B6F 09            [11]  264 	add	hl,bc
   5B70 DD 75 F6      [19]  265 	ld	-10 (ix), l
   5B73 DD 74 F7      [19]  266 	ld	-9 (ix), h
                            267 ;src/entities/player.c:57: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5B76 DD 7E FE      [19]  268 	ld	a, -2 (ix)
   5B79 B7            [ 4]  269 	or	a, a
   5B7A 28 4E         [12]  270 	jr	Z,00123$
   5B7C DD 6E FC      [19]  271 	ld	l,-4 (ix)
   5B7F DD 66 FD      [19]  272 	ld	h,-3 (ix)
   5B82 7E            [ 7]  273 	ld	a, (hl)
   5B83 DD 6E FA      [19]  274 	ld	l,-6 (ix)
   5B86 DD 66 FB      [19]  275 	ld	h,-5 (ix)
   5B89 6E            [ 7]  276 	ld	l, (hl)
   5B8A DD 75 F4      [19]  277 	ld	-12 (ix), l
   5B8D DD 36 F5 00   [19]  278 	ld	-11 (ix), #0x00
   5B91 F5            [11]  279 	push	af
   5B92 0A            [ 7]  280 	ld	a, (bc)
   5B93 6F            [ 4]  281 	ld	l, a
   5B94 F1            [10]  282 	pop	af
   5B95 DD 75 F2      [19]  283 	ld	-14 (ix), l
   5B98 DD 36 F3 00   [19]  284 	ld	-13 (ix), #0x00
   5B9C C5            [11]  285 	push	bc
   5B9D D5            [11]  286 	push	de
   5B9E F5            [11]  287 	push	af
   5B9F 33            [ 6]  288 	inc	sp
   5BA0 DD 6E F4      [19]  289 	ld	l,-12 (ix)
   5BA3 DD 66 F5      [19]  290 	ld	h,-11 (ix)
   5BA6 E5            [11]  291 	push	hl
   5BA7 DD 6E F2      [19]  292 	ld	l,-14 (ix)
   5BAA DD 66 F3      [19]  293 	ld	h,-13 (ix)
   5BAD E5            [11]  294 	push	hl
   5BAE CD C7 4B      [17]  295 	call	_collision_is_on_ground_at
   5BB1 F1            [10]  296 	pop	af
   5BB2 F1            [10]  297 	pop	af
   5BB3 33            [ 6]  298 	inc	sp
   5BB4 D1            [10]  299 	pop	de
   5BB5 C1            [10]  300 	pop	bc
   5BB6 7D            [ 4]  301 	ld	a, l
   5BB7 B7            [ 4]  302 	or	a, a
   5BB8 28 10         [12]  303 	jr	Z,00123$
                            304 ;src/entities/player.c:58: player->vy = kplayerjumpvelocity;
   5BBA DD 6E F8      [19]  305 	ld	l,-8 (ix)
   5BBD DD 66 F9      [19]  306 	ld	h,-7 (ix)
   5BC0 36 FA         [10]  307 	ld	(hl), #0xfa
                            308 ;src/entities/player.c:59: player->jump_hold = 5;
   5BC2 DD 6E F6      [19]  309 	ld	l,-10 (ix)
   5BC5 DD 66 F7      [19]  310 	ld	h,-9 (ix)
   5BC8 36 05         [10]  311 	ld	(hl), #0x05
   5BCA                     312 00123$:
                            313 ;src/entities/player.c:62: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5BCA C5            [11]  314 	push	bc
   5BCB D5            [11]  315 	push	de
   5BCC CD 13 50      [17]  316 	call	_input_is_jump_pressed
   5BCF 7D            [ 4]  317 	ld	a, l
   5BD0 D1            [10]  318 	pop	de
   5BD1 C1            [10]  319 	pop	bc
   5BD2 B7            [ 4]  320 	or	a, a
   5BD3 28 31         [12]  321 	jr	Z,00126$
   5BD5 DD 6E F6      [19]  322 	ld	l,-10 (ix)
   5BD8 DD 66 F7      [19]  323 	ld	h,-9 (ix)
   5BDB 7E            [ 7]  324 	ld	a, (hl)
   5BDC B7            [ 4]  325 	or	a, a
   5BDD 28 27         [12]  326 	jr	Z,00126$
   5BDF DD 6E F8      [19]  327 	ld	l,-8 (ix)
   5BE2 DD 66 F9      [19]  328 	ld	h,-7 (ix)
   5BE5 6E            [ 7]  329 	ld	l, (hl)
   5BE6 CB 7D         [ 8]  330 	bit	7, l
   5BE8 28 1C         [12]  331 	jr	Z,00126$
                            332 ;src/entities/player.c:63: player->vy = (i8)(player->vy + kplayerjumpboost);
   5BEA 7D            [ 4]  333 	ld	a, l
   5BEB C6 FF         [ 7]  334 	add	a, #0xff
   5BED DD 6E F8      [19]  335 	ld	l,-8 (ix)
   5BF0 DD 66 F9      [19]  336 	ld	h,-7 (ix)
   5BF3 77            [ 7]  337 	ld	(hl), a
                            338 ;src/entities/player.c:64: player->jump_hold--;
   5BF4 DD 6E F6      [19]  339 	ld	l,-10 (ix)
   5BF7 DD 66 F7      [19]  340 	ld	h,-9 (ix)
   5BFA 7E            [ 7]  341 	ld	a, (hl)
   5BFB C6 FF         [ 7]  342 	add	a, #0xff
   5BFD DD 6E F6      [19]  343 	ld	l,-10 (ix)
   5C00 DD 66 F7      [19]  344 	ld	h,-9 (ix)
   5C03 77            [ 7]  345 	ld	(hl), a
   5C04 18 08         [12]  346 	jr	00127$
   5C06                     347 00126$:
                            348 ;src/entities/player.c:66: player->jump_hold = 0;
   5C06 DD 6E F6      [19]  349 	ld	l,-10 (ix)
   5C09 DD 66 F7      [19]  350 	ld	h,-9 (ix)
   5C0C 36 00         [10]  351 	ld	(hl), #0x00
   5C0E                     352 00127$:
                            353 ;src/entities/player.c:69: player->vy = (i8)(player->vy + kplayergravity);
   5C0E DD 6E F8      [19]  354 	ld	l,-8 (ix)
   5C11 DD 66 F9      [19]  355 	ld	h,-7 (ix)
   5C14 7E            [ 7]  356 	ld	a, (hl)
   5C15 3C            [ 4]  357 	inc	a
   5C16 DD 77 F2      [19]  358 	ld	-14 (ix), a
   5C19 DD 6E F8      [19]  359 	ld	l,-8 (ix)
   5C1C DD 66 F9      [19]  360 	ld	h,-7 (ix)
   5C1F DD 7E F2      [19]  361 	ld	a, -14 (ix)
   5C22 77            [ 7]  362 	ld	(hl), a
                            363 ;src/entities/player.c:70: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5C23 3E 04         [ 7]  364 	ld	a, #0x04
   5C25 DD 96 F2      [19]  365 	sub	a, -14 (ix)
   5C28 E2 2D 5C      [10]  366 	jp	PO, 00226$
   5C2B EE 80         [ 7]  367 	xor	a, #0x80
   5C2D                     368 00226$:
   5C2D F2 38 5C      [10]  369 	jp	P, 00131$
   5C30 DD 6E F8      [19]  370 	ld	l,-8 (ix)
   5C33 DD 66 F9      [19]  371 	ld	h,-7 (ix)
   5C36 36 04         [10]  372 	ld	(hl), #0x04
   5C38                     373 00131$:
                            374 ;src/entities/player.c:72: nextx = (i16)player->x + (i16)player->vx;
   5C38 0A            [ 7]  375 	ld	a, (bc)
   5C39 DD 77 F2      [19]  376 	ld	-14 (ix), a
   5C3C DD 36 F3 00   [19]  377 	ld	-13 (ix), #0x00
   5C40 1A            [ 7]  378 	ld	a, (de)
   5C41 5F            [ 4]  379 	ld	e, a
   5C42 17            [ 4]  380 	rla
   5C43 9F            [ 4]  381 	sbc	a, a
   5C44 57            [ 4]  382 	ld	d, a
   5C45 E1            [10]  383 	pop	hl
   5C46 E5            [11]  384 	push	hl
   5C47 19            [11]  385 	add	hl, de
                            386 ;src/entities/player.c:73: if (nextx < 0) {
   5C48 CB 7C         [ 8]  387 	bit	7, h
   5C4A 28 03         [12]  388 	jr	Z,00133$
                            389 ;src/entities/player.c:74: nextx = 0;
   5C4C 21 00 00      [10]  390 	ld	hl, #0x0000
   5C4F                     391 00133$:
                            392 ;src/entities/player.c:76: if (nextx > 76) {
   5C4F 3E 4C         [ 7]  393 	ld	a, #0x4c
   5C51 BD            [ 4]  394 	cp	a, l
   5C52 3E 00         [ 7]  395 	ld	a, #0x00
   5C54 9C            [ 4]  396 	sbc	a, h
   5C55 E2 5A 5C      [10]  397 	jp	PO, 00227$
   5C58 EE 80         [ 7]  398 	xor	a, #0x80
   5C5A                     399 00227$:
   5C5A F2 60 5C      [10]  400 	jp	P, 00135$
                            401 ;src/entities/player.c:77: nextx = 76;
   5C5D 21 4C 00      [10]  402 	ld	hl, #0x004c
   5C60                     403 00135$:
                            404 ;src/entities/player.c:79: player->x = (u8)nextx;
   5C60 DD 75 F2      [19]  405 	ld	-14 (ix), l
   5C63 7D            [ 4]  406 	ld	a, l
   5C64 02            [ 7]  407 	ld	(bc), a
                            408 ;src/entities/player.c:81: nexty = (i16)player->y + (i16)player->vy;
   5C65 DD 6E FA      [19]  409 	ld	l,-6 (ix)
   5C68 DD 66 FB      [19]  410 	ld	h,-5 (ix)
   5C6B 5E            [ 7]  411 	ld	e, (hl)
   5C6C 16 00         [ 7]  412 	ld	d, #0x00
   5C6E DD 6E F8      [19]  413 	ld	l,-8 (ix)
   5C71 DD 66 F9      [19]  414 	ld	h,-7 (ix)
   5C74 6E            [ 7]  415 	ld	l, (hl)
   5C75 7D            [ 4]  416 	ld	a, l
   5C76 17            [ 4]  417 	rla
   5C77 9F            [ 4]  418 	sbc	a, a
   5C78 67            [ 4]  419 	ld	h, a
   5C79 19            [11]  420 	add	hl, de
   5C7A E5            [11]  421 	push	hl
   5C7B FD E1         [14]  422 	pop	iy
                            423 ;src/entities/player.c:82: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5C7D DD 6E FC      [19]  424 	ld	l,-4 (ix)
   5C80 DD 66 FD      [19]  425 	ld	h,-3 (ix)
   5C83 66            [ 7]  426 	ld	h, (hl)
   5C84 DD 5E F2      [19]  427 	ld	e, -14 (ix)
   5C87 16 00         [ 7]  428 	ld	d, #0x00
   5C89 C5            [11]  429 	push	bc
   5C8A E5            [11]  430 	push	hl
   5C8B 33            [ 6]  431 	inc	sp
   5C8C FD E5         [15]  432 	push	iy
   5C8E D5            [11]  433 	push	de
   5C8F CD 46 4C      [17]  434 	call	_collision_clamp_y_at
   5C92 F1            [10]  435 	pop	af
   5C93 F1            [10]  436 	pop	af
   5C94 33            [ 6]  437 	inc	sp
   5C95 C1            [10]  438 	pop	bc
                            439 ;src/entities/player.c:83: if (nexty < 0) {
   5C96 CB 7C         [ 8]  440 	bit	7, h
   5C98 28 03         [12]  441 	jr	Z,00137$
                            442 ;src/entities/player.c:84: nexty = 0;
   5C9A 21 00 00      [10]  443 	ld	hl, #0x0000
   5C9D                     444 00137$:
                            445 ;src/entities/player.c:86: player->y = (u8)nexty;
   5C9D 5D            [ 4]  446 	ld	e, l
   5C9E DD 6E FA      [19]  447 	ld	l,-6 (ix)
   5CA1 DD 66 FB      [19]  448 	ld	h,-5 (ix)
   5CA4 73            [ 7]  449 	ld	(hl), e
                            450 ;src/entities/player.c:88: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5CA5 DD 6E FC      [19]  451 	ld	l,-4 (ix)
   5CA8 DD 66 FD      [19]  452 	ld	h,-3 (ix)
   5CAB 7E            [ 7]  453 	ld	a, (hl)
   5CAC 16 00         [ 7]  454 	ld	d, #0x00
   5CAE F5            [11]  455 	push	af
   5CAF 0A            [ 7]  456 	ld	a, (bc)
   5CB0 4F            [ 4]  457 	ld	c, a
   5CB1 F1            [10]  458 	pop	af
   5CB2 06 00         [ 7]  459 	ld	b, #0x00
   5CB4 F5            [11]  460 	push	af
   5CB5 33            [ 6]  461 	inc	sp
   5CB6 D5            [11]  462 	push	de
   5CB7 C5            [11]  463 	push	bc
   5CB8 CD C7 4B      [17]  464 	call	_collision_is_on_ground_at
   5CBB F1            [10]  465 	pop	af
   5CBC F1            [10]  466 	pop	af
   5CBD 33            [ 6]  467 	inc	sp
   5CBE 7D            [ 4]  468 	ld	a, l
   5CBF B7            [ 4]  469 	or	a, a
   5CC0 28 19         [12]  470 	jr	Z,00141$
   5CC2 DD 6E F8      [19]  471 	ld	l,-8 (ix)
   5CC5 DD 66 F9      [19]  472 	ld	h,-7 (ix)
   5CC8 4E            [ 7]  473 	ld	c, (hl)
   5CC9 AF            [ 4]  474 	xor	a, a
   5CCA 91            [ 4]  475 	sub	a, c
   5CCB E2 D0 5C      [10]  476 	jp	PO, 00228$
   5CCE EE 80         [ 7]  477 	xor	a, #0x80
   5CD0                     478 00228$:
   5CD0 F2 DB 5C      [10]  479 	jp	P, 00141$
                            480 ;src/entities/player.c:89: player->vy = 0;
   5CD3 DD 6E F8      [19]  481 	ld	l,-8 (ix)
   5CD6 DD 66 F9      [19]  482 	ld	h,-7 (ix)
   5CD9 36 00         [10]  483 	ld	(hl), #0x00
   5CDB                     484 00141$:
   5CDB DD F9         [10]  485 	ld	sp, ix
   5CDD DD E1         [14]  486 	pop	ix
   5CDF C9            [10]  487 	ret
                            488 ;src/entities/player.c:93: void playerrender(const Player* player) {
                            489 ;	---------------------------------
                            490 ; Function playerrender
                            491 ; ---------------------------------
   5CE0                     492 _playerrender::
   5CE0 DD E5         [15]  493 	push	ix
   5CE2 DD 21 00 00   [14]  494 	ld	ix,#0
   5CE6 DD 39         [15]  495 	add	ix,sp
   5CE8 3B            [ 6]  496 	dec	sp
                            497 ;src/entities/player.c:96: if (!player) {
   5CE9 DD 7E 05      [19]  498 	ld	a, 5 (ix)
   5CEC DD B6 04      [19]  499 	or	a,4 (ix)
                            500 ;src/entities/player.c:97: return;
   5CEF 28 43         [12]  501 	jr	Z,00103$
                            502 ;src/entities/player.c:100: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5CF1 DD 5E 04      [19]  503 	ld	e,4 (ix)
   5CF4 DD 56 05      [19]  504 	ld	d,5 (ix)
   5CF7 6B            [ 4]  505 	ld	l, e
   5CF8 62            [ 4]  506 	ld	h, d
   5CF9 23            [ 6]  507 	inc	hl
   5CFA 46            [ 7]  508 	ld	b, (hl)
   5CFB 1A            [ 7]  509 	ld	a, (de)
   5CFC D5            [11]  510 	push	de
   5CFD C5            [11]  511 	push	bc
   5CFE 33            [ 6]  512 	inc	sp
   5CFF F5            [11]  513 	push	af
   5D00 33            [ 6]  514 	inc	sp
   5D01 21 00 C0      [10]  515 	ld	hl, #0xc000
   5D04 E5            [11]  516 	push	hl
   5D05 CD CB 61      [17]  517 	call	_cpct_getScreenPtr
   5D08 4D            [ 4]  518 	ld	c, l
   5D09 44            [ 4]  519 	ld	b, h
   5D0A D1            [10]  520 	pop	de
                            521 ;src/entities/player.c:101: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
   5D0B D5            [11]  522 	push	de
   5D0C FD E1         [14]  523 	pop	iy
   5D0E FD 7E 05      [19]  524 	ld	a, 5 (iy)
   5D11 DD 77 FF      [19]  525 	ld	-1 (ix), a
   5D14 EB            [ 4]  526 	ex	de,hl
   5D15 11 04 00      [10]  527 	ld	de, #0x0004
   5D18 19            [11]  528 	add	hl, de
   5D19 56            [ 7]  529 	ld	d, (hl)
   5D1A C5            [11]  530 	push	bc
   5D1B D5            [11]  531 	push	de
   5D1C 21 06 06      [10]  532 	ld	hl, #0x0606
   5D1F E5            [11]  533 	push	hl
   5D20 CD D8 60      [17]  534 	call	_cpct_px2byteM0
   5D23 5D            [ 4]  535 	ld	e, l
   5D24 F1            [10]  536 	pop	af
   5D25 57            [ 4]  537 	ld	d, a
   5D26 C1            [10]  538 	pop	bc
   5D27 DD 7E FF      [19]  539 	ld	a, -1 (ix)
   5D2A F5            [11]  540 	push	af
   5D2B 33            [ 6]  541 	inc	sp
   5D2C D5            [11]  542 	push	de
   5D2D C5            [11]  543 	push	bc
   5D2E CD 12 61      [17]  544 	call	_cpct_drawSolidBox
   5D31 F1            [10]  545 	pop	af
   5D32 F1            [10]  546 	pop	af
   5D33 33            [ 6]  547 	inc	sp
   5D34                     548 00103$:
   5D34 33            [ 6]  549 	inc	sp
   5D35 DD E1         [14]  550 	pop	ix
   5D37 C9            [10]  551 	ret
                            552 	.area _CODE
                            553 	.area _INITIALIZER
                            554 	.area _CABS (ABS)
