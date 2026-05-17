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
                             18 	.globl _cpct_hflipSpriteM0
                             19 	.globl _cpct_drawSprite
                             20 	.globl _playerinit
                             21 	.globl _playerupdate
                             22 	.globl _playerrender
                             23 	.globl _player_get_ammo
                             24 	.globl _player_get_health
                             25 	.globl _player_get_weapon
                             26 ;--------------------------------------------------------
                             27 ; special function registers
                             28 ;--------------------------------------------------------
                             29 ;--------------------------------------------------------
                             30 ; ram data
                             31 ;--------------------------------------------------------
                             32 	.area _DATA
   6CCC                      33 _gplayersprite:
   6CCC                      34 	.ds 192
   6D8C                      35 _gplayerspritefacingleft:
   6D8C                      36 	.ds 1
                             37 ;--------------------------------------------------------
                             38 ; ram data
                             39 ;--------------------------------------------------------
                             40 	.area _INITIALIZED
                             41 ;--------------------------------------------------------
                             42 ; absolute external ram data
                             43 ;--------------------------------------------------------
                             44 	.area _DABS (ABS)
                             45 ;--------------------------------------------------------
                             46 ; global & static initialisations
                             47 ;--------------------------------------------------------
                             48 	.area _HOME
                             49 	.area _GSINIT
                             50 	.area _GSFINAL
                             51 	.area _GSINIT
                             52 ;--------------------------------------------------------
                             53 ; Home
                             54 ;--------------------------------------------------------
                             55 	.area _HOME
                             56 	.area _HOME
                             57 ;--------------------------------------------------------
                             58 ; code
                             59 ;--------------------------------------------------------
                             60 	.area _CODE
                             61 ;src/entities/player.c:21: void playerinit(Player* player) {
                             62 ;	---------------------------------
                             63 ; Function playerinit
                             64 ; ---------------------------------
   6389                      65 _playerinit::
   6389 DD E5         [15]   66 	push	ix
   638B DD 21 00 00   [14]   67 	ld	ix,#0
   638F DD 39         [15]   68 	add	ix,sp
                             69 ;src/entities/player.c:23: if (!player) {
   6391 DD 7E 05      [19]   70 	ld	a, 5 (ix)
   6394 DD B6 04      [19]   71 	or	a,4 (ix)
                             72 ;src/entities/player.c:24: return;
   6397 28 5D         [12]   73 	jr	Z,00106$
                             74 ;src/entities/player.c:27: player->x = 4;
   6399 DD 4E 04      [19]   75 	ld	c,4 (ix)
   639C DD 46 05      [19]   76 	ld	b,5 (ix)
   639F 3E 04         [ 7]   77 	ld	a, #0x04
   63A1 02            [ 7]   78 	ld	(bc), a
                             79 ;src/entities/player.c:28: player->y = (u8)(104);  /* groundy(128) - h(24) = 104: feet at ground level */
   63A2 69            [ 4]   80 	ld	l, c
   63A3 60            [ 4]   81 	ld	h, b
   63A4 23            [ 6]   82 	inc	hl
   63A5 36 68         [10]   83 	ld	(hl), #0x68
                             84 ;src/entities/player.c:29: player->vx = 0;
   63A7 59            [ 4]   85 	ld	e, c
   63A8 50            [ 4]   86 	ld	d, b
   63A9 13            [ 6]   87 	inc	de
   63AA 13            [ 6]   88 	inc	de
   63AB AF            [ 4]   89 	xor	a, a
   63AC 12            [ 7]   90 	ld	(de), a
                             91 ;src/entities/player.c:30: player->vy = 0;
   63AD 59            [ 4]   92 	ld	e, c
   63AE 50            [ 4]   93 	ld	d, b
   63AF 13            [ 6]   94 	inc	de
   63B0 13            [ 6]   95 	inc	de
   63B1 13            [ 6]   96 	inc	de
   63B2 AF            [ 4]   97 	xor	a, a
   63B3 12            [ 7]   98 	ld	(de), a
                             99 ;src/entities/player.c:31: player->w = 8;
   63B4 21 04 00      [10]  100 	ld	hl, #0x0004
   63B7 09            [11]  101 	add	hl, bc
   63B8 36 08         [10]  102 	ld	(hl), #0x08
                            103 ;src/entities/player.c:32: player->h = 24;
   63BA 21 05 00      [10]  104 	ld	hl, #0x0005
   63BD 09            [11]  105 	add	hl, bc
   63BE 36 18         [10]  106 	ld	(hl), #0x18
                            107 ;src/entities/player.c:33: player->health = 3;
   63C0 21 06 00      [10]  108 	ld	hl, #0x0006
   63C3 09            [11]  109 	add	hl, bc
   63C4 36 03         [10]  110 	ld	(hl), #0x03
                            111 ;src/entities/player.c:34: player->weapon = 0;
   63C6 21 07 00      [10]  112 	ld	hl, #0x0007
   63C9 09            [11]  113 	add	hl, bc
   63CA 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:35: player->facing_left = 0;
   63CC 21 08 00      [10]  116 	ld	hl, #0x0008
   63CF 09            [11]  117 	add	hl, bc
   63D0 36 00         [10]  118 	ld	(hl), #0x00
                            119 ;src/entities/player.c:36: player->jump_hold = 0;
   63D2 21 09 00      [10]  120 	ld	hl, #0x0009
   63D5 09            [11]  121 	add	hl, bc
   63D6 36 00         [10]  122 	ld	(hl), #0x00
                            123 ;src/entities/player.c:37: for (index = 0; index < kplayerspritebytes; ++index) {
   63D8 0E 00         [ 7]  124 	ld	c, #0x00
   63DA                     125 00104$:
                            126 ;src/entities/player.c:38: gplayersprite[index] = sprplayerknight_data[index];
   63DA 3E CC         [ 7]  127 	ld	a, #<(_gplayersprite)
   63DC 81            [ 4]  128 	add	a, c
   63DD 5F            [ 4]  129 	ld	e, a
   63DE 3E 6C         [ 7]  130 	ld	a, #>(_gplayersprite)
   63E0 CE 00         [ 7]  131 	adc	a, #0x00
   63E2 57            [ 4]  132 	ld	d, a
   63E3 21 18 5C      [10]  133 	ld	hl, #_sprplayerknight_data
   63E6 06 00         [ 7]  134 	ld	b, #0x00
   63E8 09            [11]  135 	add	hl, bc
   63E9 7E            [ 7]  136 	ld	a, (hl)
   63EA 12            [ 7]  137 	ld	(de), a
                            138 ;src/entities/player.c:37: for (index = 0; index < kplayerspritebytes; ++index) {
   63EB 0C            [ 4]  139 	inc	c
   63EC 79            [ 4]  140 	ld	a, c
   63ED D6 C0         [ 7]  141 	sub	a, #0xc0
   63EF 38 E9         [12]  142 	jr	C,00104$
                            143 ;src/entities/player.c:40: gplayerspritefacingleft = 0;
   63F1 21 8C 6D      [10]  144 	ld	hl,#_gplayerspritefacingleft + 0
   63F4 36 00         [10]  145 	ld	(hl), #0x00
   63F6                     146 00106$:
   63F6 DD E1         [14]  147 	pop	ix
   63F8 C9            [10]  148 	ret
                            149 ;src/entities/player.c:43: void playerupdate(Player* player) {
                            150 ;	---------------------------------
                            151 ; Function playerupdate
                            152 ; ---------------------------------
   63F9                     153 _playerupdate::
   63F9 DD E5         [15]  154 	push	ix
   63FB DD 21 00 00   [14]  155 	ld	ix,#0
   63FF DD 39         [15]  156 	add	ix,sp
   6401 21 F2 FF      [10]  157 	ld	hl, #-14
   6404 39            [11]  158 	add	hl, sp
   6405 F9            [ 6]  159 	ld	sp, hl
                            160 ;src/entities/player.c:47: if (!player) {
   6406 DD 7E 05      [19]  161 	ld	a, 5 (ix)
   6409 DD B6 04      [19]  162 	or	a,4 (ix)
                            163 ;src/entities/player.c:48: return;
   640C CA 2C 66      [10]  164 	jp	Z,00141$
                            165 ;src/entities/player.c:51: if (input_is_left_pressed()) {
   640F CD D7 58      [17]  166 	call	_input_is_left_pressed
                            167 ;src/entities/player.c:52: player->vx = (i8)(player->vx - kplayeracceleration);
   6412 DD 4E 04      [19]  168 	ld	c,4 (ix)
   6415 DD 46 05      [19]  169 	ld	b,5 (ix)
   6418 59            [ 4]  170 	ld	e, c
   6419 50            [ 4]  171 	ld	d, b
   641A 13            [ 6]  172 	inc	de
   641B 13            [ 6]  173 	inc	de
                            174 ;src/entities/player.c:53: player->facing_left = 1;
   641C 79            [ 4]  175 	ld	a, c
   641D C6 08         [ 7]  176 	add	a, #0x08
   641F DD 77 F2      [19]  177 	ld	-14 (ix), a
   6422 78            [ 4]  178 	ld	a, b
   6423 CE 00         [ 7]  179 	adc	a, #0x00
   6425 DD 77 F3      [19]  180 	ld	-13 (ix), a
                            181 ;src/entities/player.c:51: if (input_is_left_pressed()) {
   6428 7D            [ 4]  182 	ld	a, l
   6429 B7            [ 4]  183 	or	a, a
   642A 28 0A         [12]  184 	jr	Z,00116$
                            185 ;src/entities/player.c:52: player->vx = (i8)(player->vx - kplayeracceleration);
   642C 1A            [ 7]  186 	ld	a, (de)
   642D C6 FE         [ 7]  187 	add	a, #0xfe
   642F 12            [ 7]  188 	ld	(de), a
                            189 ;src/entities/player.c:53: player->facing_left = 1;
   6430 E1            [10]  190 	pop	hl
   6431 E5            [11]  191 	push	hl
   6432 36 01         [10]  192 	ld	(hl), #0x01
   6434 18 52         [12]  193 	jr	00117$
   6436                     194 00116$:
                            195 ;src/entities/player.c:54: } else if (input_is_right_pressed()) {
   6436 C5            [11]  196 	push	bc
   6437 D5            [11]  197 	push	de
   6438 CD DF 58      [17]  198 	call	_input_is_right_pressed
   643B DD 75 FF      [19]  199 	ld	-1 (ix), l
   643E D1            [10]  200 	pop	de
   643F C1            [10]  201 	pop	bc
                            202 ;src/entities/player.c:65: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   6440 1A            [ 7]  203 	ld	a, (de)
                            204 ;src/entities/player.c:55: player->vx = (i8)(player->vx + kplayeracceleration);
   6441 6F            [ 4]  205 	ld	l,a
   6442 C6 02         [ 7]  206 	add	a, #0x02
   6444 DD 77 FE      [19]  207 	ld	-2 (ix), a
                            208 ;src/entities/player.c:54: } else if (input_is_right_pressed()) {
   6447 DD 7E FF      [19]  209 	ld	a, -1 (ix)
   644A B7            [ 4]  210 	or	a, a
   644B 28 0A         [12]  211 	jr	Z,00113$
                            212 ;src/entities/player.c:55: player->vx = (i8)(player->vx + kplayeracceleration);
   644D DD 7E FE      [19]  213 	ld	a, -2 (ix)
   6450 12            [ 7]  214 	ld	(de), a
                            215 ;src/entities/player.c:56: player->facing_left = 0;
   6451 E1            [10]  216 	pop	hl
   6452 E5            [11]  217 	push	hl
   6453 36 00         [10]  218 	ld	(hl), #0x00
   6455 18 31         [12]  219 	jr	00117$
   6457                     220 00113$:
                            221 ;src/entities/player.c:57: } else if (player->vx > 0) {
   6457 AF            [ 4]  222 	xor	a, a
   6458 95            [ 4]  223 	sub	a, l
   6459 E2 5E 64      [10]  224 	jp	PO, 00223$
   645C EE 80         [ 7]  225 	xor	a, #0x80
   645E                     226 00223$:
   645E F2 72 64      [10]  227 	jp	P, 00110$
                            228 ;src/entities/player.c:58: player->vx = (i8)(player->vx - kplayerdeceleration);
   6461 7D            [ 4]  229 	ld	a, l
   6462 C6 FE         [ 7]  230 	add	a, #0xfe
   6464 DD 77 FF      [19]  231 	ld	-1 (ix), a
   6467 12            [ 7]  232 	ld	(de),a
                            233 ;src/entities/player.c:59: if (player->vx < 0) player->vx = 0;
   6468 DD CB FF 7E   [20]  234 	bit	7, -1 (ix)
   646C 28 1A         [12]  235 	jr	Z,00117$
   646E AF            [ 4]  236 	xor	a, a
   646F 12            [ 7]  237 	ld	(de), a
   6470 18 16         [12]  238 	jr	00117$
   6472                     239 00110$:
                            240 ;src/entities/player.c:60: } else if (player->vx < 0) {
   6472 CB 7D         [ 8]  241 	bit	7, l
   6474 28 12         [12]  242 	jr	Z,00117$
                            243 ;src/entities/player.c:61: player->vx = (i8)(player->vx + kplayerdeceleration);
   6476 DD 7E FE      [19]  244 	ld	a, -2 (ix)
   6479 12            [ 7]  245 	ld	(de), a
                            246 ;src/entities/player.c:62: if (player->vx > 0) player->vx = 0;
   647A AF            [ 4]  247 	xor	a, a
   647B DD 96 FE      [19]  248 	sub	a, -2 (ix)
   647E E2 83 64      [10]  249 	jp	PO, 00224$
   6481 EE 80         [ 7]  250 	xor	a, #0x80
   6483                     251 00224$:
   6483 F2 88 64      [10]  252 	jp	P, 00117$
   6486 AF            [ 4]  253 	xor	a, a
   6487 12            [ 7]  254 	ld	(de), a
   6488                     255 00117$:
                            256 ;src/entities/player.c:65: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   6488 1A            [ 7]  257 	ld	a, (de)
   6489 6F            [ 4]  258 	ld	l, a
   648A 3E 02         [ 7]  259 	ld	a, #0x02
   648C 95            [ 4]  260 	sub	a, l
   648D E2 92 64      [10]  261 	jp	PO, 00225$
   6490 EE 80         [ 7]  262 	xor	a, #0x80
   6492                     263 00225$:
   6492 F2 98 64      [10]  264 	jp	P, 00119$
   6495 3E 02         [ 7]  265 	ld	a, #0x02
   6497 12            [ 7]  266 	ld	(de), a
   6498                     267 00119$:
                            268 ;src/entities/player.c:66: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   6498 1A            [ 7]  269 	ld	a, (de)
   6499 EE 80         [ 7]  270 	xor	a, #0x80
   649B D6 7E         [ 7]  271 	sub	a, #0x7e
   649D 30 03         [12]  272 	jr	NC,00121$
   649F 3E FE         [ 7]  273 	ld	a, #0xfe
   64A1 12            [ 7]  274 	ld	(de), a
   64A2                     275 00121$:
                            276 ;src/entities/player.c:68: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   64A2 C5            [11]  277 	push	bc
   64A3 D5            [11]  278 	push	de
   64A4 CD FF 58      [17]  279 	call	_input_is_jump_just_pressed
   64A7 DD 75 FE      [19]  280 	ld	-2 (ix), l
   64AA D1            [10]  281 	pop	de
   64AB C1            [10]  282 	pop	bc
   64AC 21 05 00      [10]  283 	ld	hl, #0x0005
   64AF 09            [11]  284 	add	hl,bc
   64B0 E3            [19]  285 	ex	(sp), hl
   64B1 21 01 00      [10]  286 	ld	hl, #0x0001
   64B4 09            [11]  287 	add	hl,bc
   64B5 DD 75 FC      [19]  288 	ld	-4 (ix), l
   64B8 DD 74 FD      [19]  289 	ld	-3 (ix), h
                            290 ;src/entities/player.c:69: player->vy = kplayerjumpvelocity;
   64BB 21 03 00      [10]  291 	ld	hl, #0x0003
   64BE 09            [11]  292 	add	hl,bc
   64BF DD 75 FA      [19]  293 	ld	-6 (ix), l
   64C2 DD 74 FB      [19]  294 	ld	-5 (ix), h
                            295 ;src/entities/player.c:70: player->jump_hold = 5;
   64C5 21 09 00      [10]  296 	ld	hl, #0x0009
   64C8 09            [11]  297 	add	hl,bc
   64C9 DD 75 F8      [19]  298 	ld	-8 (ix), l
   64CC DD 74 F9      [19]  299 	ld	-7 (ix), h
                            300 ;src/entities/player.c:68: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   64CF DD 7E FE      [19]  301 	ld	a, -2 (ix)
   64D2 B7            [ 4]  302 	or	a, a
   64D3 28 4A         [12]  303 	jr	Z,00123$
   64D5 E1            [10]  304 	pop	hl
   64D6 E5            [11]  305 	push	hl
   64D7 7E            [ 7]  306 	ld	a, (hl)
   64D8 DD 6E FC      [19]  307 	ld	l,-4 (ix)
   64DB DD 66 FD      [19]  308 	ld	h,-3 (ix)
   64DE 6E            [ 7]  309 	ld	l, (hl)
   64DF DD 75 F6      [19]  310 	ld	-10 (ix), l
   64E2 DD 36 F7 00   [19]  311 	ld	-9 (ix), #0x00
   64E6 F5            [11]  312 	push	af
   64E7 0A            [ 7]  313 	ld	a, (bc)
   64E8 6F            [ 4]  314 	ld	l, a
   64E9 F1            [10]  315 	pop	af
   64EA DD 75 F4      [19]  316 	ld	-12 (ix), l
   64ED DD 36 F5 00   [19]  317 	ld	-11 (ix), #0x00
   64F1 C5            [11]  318 	push	bc
   64F2 D5            [11]  319 	push	de
   64F3 F5            [11]  320 	push	af
   64F4 33            [ 6]  321 	inc	sp
   64F5 DD 6E F6      [19]  322 	ld	l,-10 (ix)
   64F8 DD 66 F7      [19]  323 	ld	h,-9 (ix)
   64FB E5            [11]  324 	push	hl
   64FC DD 6E F4      [19]  325 	ld	l,-12 (ix)
   64FF DD 66 F5      [19]  326 	ld	h,-11 (ix)
   6502 E5            [11]  327 	push	hl
   6503 CD CE 52      [17]  328 	call	_collision_is_on_ground_at
   6506 F1            [10]  329 	pop	af
   6507 F1            [10]  330 	pop	af
   6508 33            [ 6]  331 	inc	sp
   6509 D1            [10]  332 	pop	de
   650A C1            [10]  333 	pop	bc
   650B 7D            [ 4]  334 	ld	a, l
   650C B7            [ 4]  335 	or	a, a
   650D 28 10         [12]  336 	jr	Z,00123$
                            337 ;src/entities/player.c:69: player->vy = kplayerjumpvelocity;
   650F DD 6E FA      [19]  338 	ld	l,-6 (ix)
   6512 DD 66 FB      [19]  339 	ld	h,-5 (ix)
   6515 36 FA         [10]  340 	ld	(hl), #0xfa
                            341 ;src/entities/player.c:70: player->jump_hold = 5;
   6517 DD 6E F8      [19]  342 	ld	l,-8 (ix)
   651A DD 66 F9      [19]  343 	ld	h,-7 (ix)
   651D 36 05         [10]  344 	ld	(hl), #0x05
   651F                     345 00123$:
                            346 ;src/entities/player.c:73: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   651F C5            [11]  347 	push	bc
   6520 D5            [11]  348 	push	de
   6521 CD F7 58      [17]  349 	call	_input_is_jump_pressed
   6524 7D            [ 4]  350 	ld	a, l
   6525 D1            [10]  351 	pop	de
   6526 C1            [10]  352 	pop	bc
   6527 B7            [ 4]  353 	or	a, a
   6528 28 31         [12]  354 	jr	Z,00126$
   652A DD 6E F8      [19]  355 	ld	l,-8 (ix)
   652D DD 66 F9      [19]  356 	ld	h,-7 (ix)
   6530 7E            [ 7]  357 	ld	a, (hl)
   6531 B7            [ 4]  358 	or	a, a
   6532 28 27         [12]  359 	jr	Z,00126$
   6534 DD 6E FA      [19]  360 	ld	l,-6 (ix)
   6537 DD 66 FB      [19]  361 	ld	h,-5 (ix)
   653A 6E            [ 7]  362 	ld	l, (hl)
   653B CB 7D         [ 8]  363 	bit	7, l
   653D 28 1C         [12]  364 	jr	Z,00126$
                            365 ;src/entities/player.c:74: player->vy = (i8)(player->vy + kplayerjumpboost);
   653F 7D            [ 4]  366 	ld	a, l
   6540 C6 FF         [ 7]  367 	add	a, #0xff
   6542 DD 6E FA      [19]  368 	ld	l,-6 (ix)
   6545 DD 66 FB      [19]  369 	ld	h,-5 (ix)
   6548 77            [ 7]  370 	ld	(hl), a
                            371 ;src/entities/player.c:75: player->jump_hold--;
   6549 DD 6E F8      [19]  372 	ld	l,-8 (ix)
   654C DD 66 F9      [19]  373 	ld	h,-7 (ix)
   654F 7E            [ 7]  374 	ld	a, (hl)
   6550 C6 FF         [ 7]  375 	add	a, #0xff
   6552 DD 6E F8      [19]  376 	ld	l,-8 (ix)
   6555 DD 66 F9      [19]  377 	ld	h,-7 (ix)
   6558 77            [ 7]  378 	ld	(hl), a
   6559 18 08         [12]  379 	jr	00127$
   655B                     380 00126$:
                            381 ;src/entities/player.c:77: player->jump_hold = 0;
   655B DD 6E F8      [19]  382 	ld	l,-8 (ix)
   655E DD 66 F9      [19]  383 	ld	h,-7 (ix)
   6561 36 00         [10]  384 	ld	(hl), #0x00
   6563                     385 00127$:
                            386 ;src/entities/player.c:80: player->vy = (i8)(player->vy + kplayergravity);
   6563 DD 6E FA      [19]  387 	ld	l,-6 (ix)
   6566 DD 66 FB      [19]  388 	ld	h,-5 (ix)
   6569 7E            [ 7]  389 	ld	a, (hl)
   656A 3C            [ 4]  390 	inc	a
   656B DD 77 F4      [19]  391 	ld	-12 (ix), a
   656E DD 6E FA      [19]  392 	ld	l,-6 (ix)
   6571 DD 66 FB      [19]  393 	ld	h,-5 (ix)
   6574 DD 7E F4      [19]  394 	ld	a, -12 (ix)
   6577 77            [ 7]  395 	ld	(hl), a
                            396 ;src/entities/player.c:81: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   6578 3E 04         [ 7]  397 	ld	a, #0x04
   657A DD 96 F4      [19]  398 	sub	a, -12 (ix)
   657D E2 82 65      [10]  399 	jp	PO, 00226$
   6580 EE 80         [ 7]  400 	xor	a, #0x80
   6582                     401 00226$:
   6582 F2 8D 65      [10]  402 	jp	P, 00131$
   6585 DD 6E FA      [19]  403 	ld	l,-6 (ix)
   6588 DD 66 FB      [19]  404 	ld	h,-5 (ix)
   658B 36 04         [10]  405 	ld	(hl), #0x04
   658D                     406 00131$:
                            407 ;src/entities/player.c:83: nextx = (i16)player->x + (i16)player->vx;
   658D 0A            [ 7]  408 	ld	a, (bc)
   658E DD 77 F4      [19]  409 	ld	-12 (ix), a
   6591 DD 36 F5 00   [19]  410 	ld	-11 (ix), #0x00
   6595 1A            [ 7]  411 	ld	a, (de)
   6596 5F            [ 4]  412 	ld	e, a
   6597 17            [ 4]  413 	rla
   6598 9F            [ 4]  414 	sbc	a, a
   6599 57            [ 4]  415 	ld	d, a
   659A DD 6E F4      [19]  416 	ld	l,-12 (ix)
   659D DD 66 F5      [19]  417 	ld	h,-11 (ix)
   65A0 19            [11]  418 	add	hl, de
                            419 ;src/entities/player.c:84: if (nextx < 0) {
   65A1 CB 7C         [ 8]  420 	bit	7, h
   65A3 28 03         [12]  421 	jr	Z,00133$
                            422 ;src/entities/player.c:85: nextx = 0;
   65A5 21 00 00      [10]  423 	ld	hl, #0x0000
   65A8                     424 00133$:
                            425 ;src/entities/player.c:87: if (nextx > 72) {
   65A8 3E 48         [ 7]  426 	ld	a, #0x48
   65AA BD            [ 4]  427 	cp	a, l
   65AB 3E 00         [ 7]  428 	ld	a, #0x00
   65AD 9C            [ 4]  429 	sbc	a, h
   65AE E2 B3 65      [10]  430 	jp	PO, 00227$
   65B1 EE 80         [ 7]  431 	xor	a, #0x80
   65B3                     432 00227$:
   65B3 F2 B9 65      [10]  433 	jp	P, 00135$
                            434 ;src/entities/player.c:88: nextx = 72;
   65B6 21 48 00      [10]  435 	ld	hl, #0x0048
   65B9                     436 00135$:
                            437 ;src/entities/player.c:90: player->x = (u8)nextx;
   65B9 DD 75 F4      [19]  438 	ld	-12 (ix), l
   65BC 7D            [ 4]  439 	ld	a, l
   65BD 02            [ 7]  440 	ld	(bc), a
                            441 ;src/entities/player.c:92: nexty = (i16)player->y + (i16)player->vy;
   65BE DD 6E FC      [19]  442 	ld	l,-4 (ix)
   65C1 DD 66 FD      [19]  443 	ld	h,-3 (ix)
   65C4 5E            [ 7]  444 	ld	e, (hl)
   65C5 16 00         [ 7]  445 	ld	d, #0x00
   65C7 DD 6E FA      [19]  446 	ld	l,-6 (ix)
   65CA DD 66 FB      [19]  447 	ld	h,-5 (ix)
   65CD 6E            [ 7]  448 	ld	l, (hl)
   65CE 7D            [ 4]  449 	ld	a, l
   65CF 17            [ 4]  450 	rla
   65D0 9F            [ 4]  451 	sbc	a, a
   65D1 67            [ 4]  452 	ld	h, a
   65D2 19            [11]  453 	add	hl, de
   65D3 E5            [11]  454 	push	hl
   65D4 FD E1         [14]  455 	pop	iy
                            456 ;src/entities/player.c:93: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   65D6 E1            [10]  457 	pop	hl
   65D7 E5            [11]  458 	push	hl
   65D8 66            [ 7]  459 	ld	h, (hl)
   65D9 DD 5E F4      [19]  460 	ld	e, -12 (ix)
   65DC 16 00         [ 7]  461 	ld	d, #0x00
   65DE C5            [11]  462 	push	bc
   65DF E5            [11]  463 	push	hl
   65E0 33            [ 6]  464 	inc	sp
   65E1 FD E5         [15]  465 	push	iy
   65E3 D5            [11]  466 	push	de
   65E4 CD 4D 53      [17]  467 	call	_collision_clamp_y_at
   65E7 F1            [10]  468 	pop	af
   65E8 F1            [10]  469 	pop	af
   65E9 33            [ 6]  470 	inc	sp
   65EA C1            [10]  471 	pop	bc
                            472 ;src/entities/player.c:94: if (nexty < 0) {
   65EB CB 7C         [ 8]  473 	bit	7, h
   65ED 28 03         [12]  474 	jr	Z,00137$
                            475 ;src/entities/player.c:95: nexty = 0;
   65EF 21 00 00      [10]  476 	ld	hl, #0x0000
   65F2                     477 00137$:
                            478 ;src/entities/player.c:97: player->y = (u8)nexty;
   65F2 5D            [ 4]  479 	ld	e, l
   65F3 DD 6E FC      [19]  480 	ld	l,-4 (ix)
   65F6 DD 66 FD      [19]  481 	ld	h,-3 (ix)
   65F9 73            [ 7]  482 	ld	(hl), e
                            483 ;src/entities/player.c:99: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   65FA E1            [10]  484 	pop	hl
   65FB E5            [11]  485 	push	hl
   65FC 7E            [ 7]  486 	ld	a, (hl)
   65FD 16 00         [ 7]  487 	ld	d, #0x00
   65FF F5            [11]  488 	push	af
   6600 0A            [ 7]  489 	ld	a, (bc)
   6601 4F            [ 4]  490 	ld	c, a
   6602 F1            [10]  491 	pop	af
   6603 06 00         [ 7]  492 	ld	b, #0x00
   6605 F5            [11]  493 	push	af
   6606 33            [ 6]  494 	inc	sp
   6607 D5            [11]  495 	push	de
   6608 C5            [11]  496 	push	bc
   6609 CD CE 52      [17]  497 	call	_collision_is_on_ground_at
   660C F1            [10]  498 	pop	af
   660D F1            [10]  499 	pop	af
   660E 33            [ 6]  500 	inc	sp
   660F 7D            [ 4]  501 	ld	a, l
   6610 B7            [ 4]  502 	or	a, a
   6611 28 19         [12]  503 	jr	Z,00141$
   6613 DD 6E FA      [19]  504 	ld	l,-6 (ix)
   6616 DD 66 FB      [19]  505 	ld	h,-5 (ix)
   6619 4E            [ 7]  506 	ld	c, (hl)
   661A AF            [ 4]  507 	xor	a, a
   661B 91            [ 4]  508 	sub	a, c
   661C E2 21 66      [10]  509 	jp	PO, 00228$
   661F EE 80         [ 7]  510 	xor	a, #0x80
   6621                     511 00228$:
   6621 F2 2C 66      [10]  512 	jp	P, 00141$
                            513 ;src/entities/player.c:100: player->vy = 0;
   6624 DD 6E FA      [19]  514 	ld	l,-6 (ix)
   6627 DD 66 FB      [19]  515 	ld	h,-5 (ix)
   662A 36 00         [10]  516 	ld	(hl), #0x00
   662C                     517 00141$:
   662C DD F9         [10]  518 	ld	sp, ix
   662E DD E1         [14]  519 	pop	ix
   6630 C9            [10]  520 	ret
                            521 ;src/entities/player.c:104: void playerrender(const Player* player) {
                            522 ;	---------------------------------
                            523 ; Function playerrender
                            524 ; ---------------------------------
   6631                     525 _playerrender::
   6631 DD E5         [15]  526 	push	ix
   6633 DD 21 00 00   [14]  527 	ld	ix,#0
   6637 DD 39         [15]  528 	add	ix,sp
   6639 21 F9 FF      [10]  529 	ld	hl, #-7
   663C 39            [11]  530 	add	hl, sp
   663D F9            [ 6]  531 	ld	sp, hl
                            532 ;src/entities/player.c:107: if (!player) {
   663E DD 7E 05      [19]  533 	ld	a, 5 (ix)
   6641 DD B6 04      [19]  534 	or	a,4 (ix)
                            535 ;src/entities/player.c:108: return;
   6644 28 78         [12]  536 	jr	Z,00105$
                            537 ;src/entities/player.c:111: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   6646 DD 5E 04      [19]  538 	ld	e,4 (ix)
   6649 DD 56 05      [19]  539 	ld	d,5 (ix)
   664C 6B            [ 4]  540 	ld	l, e
   664D 62            [ 4]  541 	ld	h, d
   664E 23            [ 6]  542 	inc	hl
   664F 46            [ 7]  543 	ld	b, (hl)
   6650 1A            [ 7]  544 	ld	a, (de)
   6651 D5            [11]  545 	push	de
   6652 C5            [11]  546 	push	bc
   6653 33            [ 6]  547 	inc	sp
   6654 F5            [11]  548 	push	af
   6655 33            [ 6]  549 	inc	sp
   6656 21 00 C0      [10]  550 	ld	hl, #0xc000
   6659 E5            [11]  551 	push	hl
   665A CD A5 6B      [17]  552 	call	_cpct_getScreenPtr
   665D 4D            [ 4]  553 	ld	c, l
   665E 44            [ 4]  554 	ld	b, h
   665F D1            [10]  555 	pop	de
                            556 ;src/entities/player.c:112: if (player->facing_left != gplayerspritefacingleft) {
   6660 21 08 00      [10]  557 	ld	hl, #0x0008
   6663 19            [11]  558 	add	hl,de
   6664 DD 75 FE      [19]  559 	ld	-2 (ix), l
   6667 DD 74 FF      [19]  560 	ld	-1 (ix), h
   666A 7E            [ 7]  561 	ld	a, (hl)
   666B DD 77 FD      [19]  562 	ld	-3 (ix), a
                            563 ;src/entities/player.c:113: cpct_hflipSpriteM0(player->w, player->h, gplayersprite);
   666E 21 05 00      [10]  564 	ld	hl, #0x0005
   6671 19            [11]  565 	add	hl,de
   6672 DD 75 FB      [19]  566 	ld	-5 (ix), l
   6675 DD 74 FC      [19]  567 	ld	-4 (ix), h
   6678 21 04 00      [10]  568 	ld	hl, #0x0004
   667B 19            [11]  569 	add	hl,de
   667C E3            [19]  570 	ex	(sp), hl
                            571 ;src/entities/player.c:112: if (player->facing_left != gplayerspritefacingleft) {
   667D 3A 8C 6D      [13]  572 	ld	a,(#_gplayerspritefacingleft + 0)
   6680 DD 96 FD      [19]  573 	sub	a, -3 (ix)
   6683 28 22         [12]  574 	jr	Z,00104$
                            575 ;src/entities/player.c:113: cpct_hflipSpriteM0(player->w, player->h, gplayersprite);
   6685 DD 6E FB      [19]  576 	ld	l,-5 (ix)
   6688 DD 66 FC      [19]  577 	ld	h,-4 (ix)
   668B 5E            [ 7]  578 	ld	e, (hl)
   668C E1            [10]  579 	pop	hl
   668D E5            [11]  580 	push	hl
   668E 56            [ 7]  581 	ld	d, (hl)
   668F C5            [11]  582 	push	bc
   6690 21 CC 6C      [10]  583 	ld	hl, #_gplayersprite
   6693 E5            [11]  584 	push	hl
   6694 7B            [ 4]  585 	ld	a, e
   6695 F5            [11]  586 	push	af
   6696 33            [ 6]  587 	inc	sp
   6697 D5            [11]  588 	push	de
   6698 33            [ 6]  589 	inc	sp
   6699 CD 27 6A      [17]  590 	call	_cpct_hflipSpriteM0
   669C C1            [10]  591 	pop	bc
                            592 ;src/entities/player.c:114: gplayerspritefacingleft = player->facing_left;
   669D DD 6E FE      [19]  593 	ld	l,-2 (ix)
   66A0 DD 66 FF      [19]  594 	ld	h,-1 (ix)
   66A3 7E            [ 7]  595 	ld	a, (hl)
   66A4 32 8C 6D      [13]  596 	ld	(#_gplayerspritefacingleft + 0),a
   66A7                     597 00104$:
                            598 ;src/entities/player.c:116: cpct_drawSprite(gplayersprite, pvmem, player->w, player->h);
   66A7 DD 6E FB      [19]  599 	ld	l,-5 (ix)
   66AA DD 66 FC      [19]  600 	ld	h,-4 (ix)
   66AD 5E            [ 7]  601 	ld	e, (hl)
   66AE E1            [10]  602 	pop	hl
   66AF E5            [11]  603 	push	hl
   66B0 56            [ 7]  604 	ld	d, (hl)
   66B1 7B            [ 4]  605 	ld	a, e
   66B2 F5            [11]  606 	push	af
   66B3 33            [ 6]  607 	inc	sp
   66B4 D5            [11]  608 	push	de
   66B5 33            [ 6]  609 	inc	sp
   66B6 C5            [11]  610 	push	bc
   66B7 21 CC 6C      [10]  611 	ld	hl, #_gplayersprite
   66BA E5            [11]  612 	push	hl
   66BB CD 61 69      [17]  613 	call	_cpct_drawSprite
   66BE                     614 00105$:
   66BE DD F9         [10]  615 	ld	sp, ix
   66C0 DD E1         [14]  616 	pop	ix
   66C2 C9            [10]  617 	ret
                            618 ;src/entities/player.c:119: u8 player_get_ammo(const Player* player) {
                            619 ;	---------------------------------
                            620 ; Function player_get_ammo
                            621 ; ---------------------------------
   66C3                     622 _player_get_ammo::
                            623 ;src/entities/player.c:121: return 3;
   66C3 2E 03         [ 7]  624 	ld	l, #0x03
   66C5 C9            [10]  625 	ret
                            626 ;src/entities/player.c:124: u8 player_get_health(const Player* player) {
                            627 ;	---------------------------------
                            628 ; Function player_get_health
                            629 ; ---------------------------------
   66C6                     630 _player_get_health::
                            631 ;src/entities/player.c:125: return player ? player->health : 0;
   66C6 21 03 00      [10]  632 	ld	hl, #2+1
   66C9 39            [11]  633 	add	hl, sp
   66CA 7E            [ 7]  634 	ld	a, (hl)
   66CB 2B            [ 6]  635 	dec	hl
   66CC B6            [ 7]  636 	or	a,(hl)
   66CD 28 0A         [12]  637 	jr	Z,00103$
   66CF C1            [10]  638 	pop	bc
   66D0 E1            [10]  639 	pop	hl
   66D1 E5            [11]  640 	push	hl
   66D2 C5            [11]  641 	push	bc
   66D3 11 06 00      [10]  642 	ld	de, #0x0006
   66D6 19            [11]  643 	add	hl, de
   66D7 6E            [ 7]  644 	ld	l, (hl)
   66D8 C9            [10]  645 	ret
   66D9                     646 00103$:
   66D9 2E 00         [ 7]  647 	ld	l, #0x00
   66DB C9            [10]  648 	ret
                            649 ;src/entities/player.c:128: u8 player_get_weapon(const Player* player) {
                            650 ;	---------------------------------
                            651 ; Function player_get_weapon
                            652 ; ---------------------------------
   66DC                     653 _player_get_weapon::
                            654 ;src/entities/player.c:129: return player ? player->weapon : 0;
   66DC 21 03 00      [10]  655 	ld	hl, #2+1
   66DF 39            [11]  656 	add	hl, sp
   66E0 7E            [ 7]  657 	ld	a, (hl)
   66E1 2B            [ 6]  658 	dec	hl
   66E2 B6            [ 7]  659 	or	a,(hl)
   66E3 28 0A         [12]  660 	jr	Z,00103$
   66E5 C1            [10]  661 	pop	bc
   66E6 E1            [10]  662 	pop	hl
   66E7 E5            [11]  663 	push	hl
   66E8 C5            [11]  664 	push	bc
   66E9 11 07 00      [10]  665 	ld	de, #0x0007
   66EC 19            [11]  666 	add	hl, de
   66ED 6E            [ 7]  667 	ld	l, (hl)
   66EE C9            [10]  668 	ret
   66EF                     669 00103$:
   66EF 2E 00         [ 7]  670 	ld	l, #0x00
   66F1 C9            [10]  671 	ret
                            672 	.area _CODE
                            673 	.area _INITIALIZER
                            674 	.area _CABS (ABS)
