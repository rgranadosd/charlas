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
                             18 	.globl _cpct_drawSprite
                             19 	.globl _playerinit
                             20 	.globl _playerupdate
                             21 	.globl _playerrender
                             22 	.globl _player_get_health
                             23 	.globl _player_get_weapon
                             24 ;--------------------------------------------------------
                             25 ; special function registers
                             26 ;--------------------------------------------------------
                             27 ;--------------------------------------------------------
                             28 ; ram data
                             29 ;--------------------------------------------------------
                             30 	.area _DATA
                             31 ;--------------------------------------------------------
                             32 ; ram data
                             33 ;--------------------------------------------------------
                             34 	.area _INITIALIZED
                             35 ;--------------------------------------------------------
                             36 ; absolute external ram data
                             37 ;--------------------------------------------------------
                             38 	.area _DABS (ABS)
                             39 ;--------------------------------------------------------
                             40 ; global & static initialisations
                             41 ;--------------------------------------------------------
                             42 	.area _HOME
                             43 	.area _GSINIT
                             44 	.area _GSFINAL
                             45 	.area _GSINIT
                             46 ;--------------------------------------------------------
                             47 ; Home
                             48 ;--------------------------------------------------------
                             49 	.area _HOME
                             50 	.area _HOME
                             51 ;--------------------------------------------------------
                             52 ; code
                             53 ;--------------------------------------------------------
                             54 	.area _CODE
                             55 ;src/entities/player.c:27: void playerinit(Player* player) {
                             56 ;	---------------------------------
                             57 ; Function playerinit
                             58 ; ---------------------------------
   5F44                      59 _playerinit::
                             60 ;src/entities/player.c:28: if (!player) {
   5F44 21 03 00      [10]   61 	ld	hl, #2+1
   5F47 39            [11]   62 	add	hl, sp
   5F48 7E            [ 7]   63 	ld	a, (hl)
   5F49 2B            [ 6]   64 	dec	hl
   5F4A B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:29: return;
   5F4B C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:32: player->x = 20;
   5F4C D1            [10]   69 	pop	de
   5F4D C1            [10]   70 	pop	bc
   5F4E C5            [11]   71 	push	bc
   5F4F D5            [11]   72 	push	de
   5F50 3E 14         [ 7]   73 	ld	a, #0x14
   5F52 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:33: player->y = 120;
   5F53 69            [ 4]   76 	ld	l, c
   5F54 60            [ 4]   77 	ld	h, b
   5F55 23            [ 6]   78 	inc	hl
   5F56 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:34: player->vx = 0;
   5F58 59            [ 4]   81 	ld	e, c
   5F59 50            [ 4]   82 	ld	d, b
   5F5A 13            [ 6]   83 	inc	de
   5F5B 13            [ 6]   84 	inc	de
   5F5C AF            [ 4]   85 	xor	a, a
   5F5D 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:35: player->vy = 0;
   5F5E 59            [ 4]   88 	ld	e, c
   5F5F 50            [ 4]   89 	ld	d, b
   5F60 13            [ 6]   90 	inc	de
   5F61 13            [ 6]   91 	inc	de
   5F62 13            [ 6]   92 	inc	de
   5F63 AF            [ 4]   93 	xor	a, a
   5F64 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:36: player->w = 4;
   5F65 21 04 00      [10]   96 	ld	hl, #0x0004
   5F68 09            [11]   97 	add	hl, bc
   5F69 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:37: player->h = 16;
   5F6B 21 05 00      [10]  100 	ld	hl, #0x0005
   5F6E 09            [11]  101 	add	hl, bc
   5F6F 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:38: player->health = 3;
   5F71 21 06 00      [10]  104 	ld	hl, #0x0006
   5F74 09            [11]  105 	add	hl, bc
   5F75 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:39: player->weapon = 0;
   5F77 21 07 00      [10]  108 	ld	hl, #0x0007
   5F7A 09            [11]  109 	add	hl, bc
   5F7B 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:40: player->facing_left = 0;
   5F7D 21 08 00      [10]  112 	ld	hl, #0x0008
   5F80 09            [11]  113 	add	hl, bc
   5F81 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:41: player->jump_hold = 0;
   5F83 21 09 00      [10]  116 	ld	hl, #0x0009
   5F86 09            [11]  117 	add	hl, bc
   5F87 36 00         [10]  118 	ld	(hl), #0x00
   5F89 C9            [10]  119 	ret
   5F8A                     120 _player_sprite:
   5F8A 3C                  121 	.db #0x3c	; 60
   5F8B 3C                  122 	.db #0x3c	; 60
   5F8C 3C                  123 	.db #0x3c	; 60
   5F8D 3C                  124 	.db #0x3c	; 60
   5F8E 28                  125 	.db #0x28	; 40
   5F8F 28                  126 	.db #0x28	; 40
   5F90 00                  127 	.db #0x00	; 0
   5F91 14                  128 	.db #0x14	; 20
   5F92 28                  129 	.db #0x28	; 40
   5F93 28                  130 	.db #0x28	; 40
   5F94 00                  131 	.db #0x00	; 0
   5F95 14                  132 	.db #0x14	; 20
   5F96 28                  133 	.db #0x28	; 40
   5F97 28                  134 	.db #0x28	; 40
   5F98 00                  135 	.db #0x00	; 0
   5F99 14                  136 	.db #0x14	; 20
   5F9A 28                  137 	.db #0x28	; 40
   5F9B 28                  138 	.db #0x28	; 40
   5F9C 00                  139 	.db #0x00	; 0
   5F9D 14                  140 	.db #0x14	; 20
   5F9E 28                  141 	.db #0x28	; 40
   5F9F 28                  142 	.db #0x28	; 40
   5FA0 00                  143 	.db #0x00	; 0
   5FA1 14                  144 	.db #0x14	; 20
   5FA2 28                  145 	.db #0x28	; 40
   5FA3 28                  146 	.db #0x28	; 40
   5FA4 00                  147 	.db #0x00	; 0
   5FA5 14                  148 	.db #0x14	; 20
   5FA6 28                  149 	.db #0x28	; 40
   5FA7 28                  150 	.db #0x28	; 40
   5FA8 00                  151 	.db #0x00	; 0
   5FA9 14                  152 	.db #0x14	; 20
   5FAA 3C                  153 	.db #0x3c	; 60
   5FAB 3C                  154 	.db #0x3c	; 60
   5FAC 3C                  155 	.db #0x3c	; 60
   5FAD 3C                  156 	.db #0x3c	; 60
   5FAE 28                  157 	.db #0x28	; 40
   5FAF 28                  158 	.db #0x28	; 40
   5FB0 00                  159 	.db #0x00	; 0
   5FB1 14                  160 	.db #0x14	; 20
   5FB2 28                  161 	.db #0x28	; 40
   5FB3 28                  162 	.db #0x28	; 40
   5FB4 00                  163 	.db #0x00	; 0
   5FB5 14                  164 	.db #0x14	; 20
   5FB6 28                  165 	.db #0x28	; 40
   5FB7 28                  166 	.db #0x28	; 40
   5FB8 00                  167 	.db #0x00	; 0
   5FB9 14                  168 	.db #0x14	; 20
   5FBA 28                  169 	.db #0x28	; 40
   5FBB 28                  170 	.db #0x28	; 40
   5FBC 00                  171 	.db #0x00	; 0
   5FBD 14                  172 	.db #0x14	; 20
   5FBE 28                  173 	.db #0x28	; 40
   5FBF 28                  174 	.db #0x28	; 40
   5FC0 00                  175 	.db #0x00	; 0
   5FC1 14                  176 	.db #0x14	; 20
   5FC2 28                  177 	.db #0x28	; 40
   5FC3 28                  178 	.db #0x28	; 40
   5FC4 00                  179 	.db #0x00	; 0
   5FC5 14                  180 	.db #0x14	; 20
   5FC6 3C                  181 	.db #0x3c	; 60
   5FC7 3C                  182 	.db #0x3c	; 60
   5FC8 3C                  183 	.db #0x3c	; 60
   5FC9 3C                  184 	.db #0x3c	; 60
                            185 ;src/entities/player.c:44: void playerupdate(Player* player) {
                            186 ;	---------------------------------
                            187 ; Function playerupdate
                            188 ; ---------------------------------
   5FCA                     189 _playerupdate::
   5FCA DD E5         [15]  190 	push	ix
   5FCC DD 21 00 00   [14]  191 	ld	ix,#0
   5FD0 DD 39         [15]  192 	add	ix,sp
   5FD2 21 F2 FF      [10]  193 	ld	hl, #-14
   5FD5 39            [11]  194 	add	hl, sp
   5FD6 F9            [ 6]  195 	ld	sp, hl
                            196 ;src/entities/player.c:48: if (!player) {
   5FD7 DD 7E 05      [19]  197 	ld	a, 5 (ix)
   5FDA DD B6 04      [19]  198 	or	a,4 (ix)
                            199 ;src/entities/player.c:49: return;
   5FDD CA 11 62      [10]  200 	jp	Z,00141$
                            201 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5FE0 CD 06 51      [17]  202 	call	_input_is_left_pressed
                            203 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5FE3 DD 4E 04      [19]  204 	ld	c,4 (ix)
   5FE6 DD 46 05      [19]  205 	ld	b,5 (ix)
   5FE9 59            [ 4]  206 	ld	e, c
   5FEA 50            [ 4]  207 	ld	d, b
   5FEB 13            [ 6]  208 	inc	de
   5FEC 13            [ 6]  209 	inc	de
                            210 ;src/entities/player.c:54: player->facing_left = 1;
   5FED 79            [ 4]  211 	ld	a, c
   5FEE C6 08         [ 7]  212 	add	a, #0x08
   5FF0 DD 77 FD      [19]  213 	ld	-3 (ix), a
   5FF3 78            [ 4]  214 	ld	a, b
   5FF4 CE 00         [ 7]  215 	adc	a, #0x00
   5FF6 DD 77 FE      [19]  216 	ld	-2 (ix), a
                            217 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5FF9 7D            [ 4]  218 	ld	a, l
   5FFA B7            [ 4]  219 	or	a, a
   5FFB 28 0E         [12]  220 	jr	Z,00116$
                            221 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5FFD 1A            [ 7]  222 	ld	a, (de)
   5FFE C6 FF         [ 7]  223 	add	a, #0xff
   6000 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/player.c:54: player->facing_left = 1;
   6001 DD 6E FD      [19]  226 	ld	l,-3 (ix)
   6004 DD 66 FE      [19]  227 	ld	h,-2 (ix)
   6007 36 01         [10]  228 	ld	(hl), #0x01
   6009 18 55         [12]  229 	jr	00117$
   600B                     230 00116$:
                            231 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   600B C5            [11]  232 	push	bc
   600C D5            [11]  233 	push	de
   600D CD 0E 51      [17]  234 	call	_input_is_right_pressed
   6010 DD 75 FF      [19]  235 	ld	-1 (ix), l
   6013 D1            [10]  236 	pop	de
   6014 C1            [10]  237 	pop	bc
                            238 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   6015 1A            [ 7]  239 	ld	a, (de)
                            240 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   6016 6F            [ 4]  241 	ld	l,a
   6017 3C            [ 4]  242 	inc	a
   6018 DD 77 FC      [19]  243 	ld	-4 (ix), a
                            244 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   601B DD 7E FF      [19]  245 	ld	a, -1 (ix)
   601E B7            [ 4]  246 	or	a, a
   601F 28 0E         [12]  247 	jr	Z,00113$
                            248 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   6021 DD 7E FC      [19]  249 	ld	a, -4 (ix)
   6024 12            [ 7]  250 	ld	(de), a
                            251 ;src/entities/player.c:57: player->facing_left = 0;
   6025 DD 6E FD      [19]  252 	ld	l,-3 (ix)
   6028 DD 66 FE      [19]  253 	ld	h,-2 (ix)
   602B 36 00         [10]  254 	ld	(hl), #0x00
   602D 18 31         [12]  255 	jr	00117$
   602F                     256 00113$:
                            257 ;src/entities/player.c:58: } else if (player->vx > 0) {
   602F AF            [ 4]  258 	xor	a, a
   6030 95            [ 4]  259 	sub	a, l
   6031 E2 36 60      [10]  260 	jp	PO, 00223$
   6034 EE 80         [ 7]  261 	xor	a, #0x80
   6036                     262 00223$:
   6036 F2 4A 60      [10]  263 	jp	P, 00110$
                            264 ;src/entities/player.c:59: player->vx = (i8)(player->vx - kplayerdeceleration);
   6039 7D            [ 4]  265 	ld	a, l
   603A C6 FF         [ 7]  266 	add	a, #0xff
   603C DD 77 FF      [19]  267 	ld	-1 (ix), a
   603F 12            [ 7]  268 	ld	(de),a
                            269 ;src/entities/player.c:60: if (player->vx < 0) player->vx = 0;
   6040 DD CB FF 7E   [20]  270 	bit	7, -1 (ix)
   6044 28 1A         [12]  271 	jr	Z,00117$
   6046 AF            [ 4]  272 	xor	a, a
   6047 12            [ 7]  273 	ld	(de), a
   6048 18 16         [12]  274 	jr	00117$
   604A                     275 00110$:
                            276 ;src/entities/player.c:61: } else if (player->vx < 0) {
   604A CB 7D         [ 8]  277 	bit	7, l
   604C 28 12         [12]  278 	jr	Z,00117$
                            279 ;src/entities/player.c:62: player->vx = (i8)(player->vx + kplayerdeceleration);
   604E DD 7E FC      [19]  280 	ld	a, -4 (ix)
   6051 12            [ 7]  281 	ld	(de), a
                            282 ;src/entities/player.c:63: if (player->vx > 0) player->vx = 0;
   6052 AF            [ 4]  283 	xor	a, a
   6053 DD 96 FC      [19]  284 	sub	a, -4 (ix)
   6056 E2 5B 60      [10]  285 	jp	PO, 00224$
   6059 EE 80         [ 7]  286 	xor	a, #0x80
   605B                     287 00224$:
   605B F2 60 60      [10]  288 	jp	P, 00117$
   605E AF            [ 4]  289 	xor	a, a
   605F 12            [ 7]  290 	ld	(de), a
   6060                     291 00117$:
                            292 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   6060 1A            [ 7]  293 	ld	a, (de)
   6061 6F            [ 4]  294 	ld	l, a
   6062 3E 03         [ 7]  295 	ld	a, #0x03
   6064 95            [ 4]  296 	sub	a, l
   6065 E2 6A 60      [10]  297 	jp	PO, 00225$
   6068 EE 80         [ 7]  298 	xor	a, #0x80
   606A                     299 00225$:
   606A F2 70 60      [10]  300 	jp	P, 00119$
   606D 3E 03         [ 7]  301 	ld	a, #0x03
   606F 12            [ 7]  302 	ld	(de), a
   6070                     303 00119$:
                            304 ;src/entities/player.c:67: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   6070 1A            [ 7]  305 	ld	a, (de)
   6071 EE 80         [ 7]  306 	xor	a, #0x80
   6073 D6 7D         [ 7]  307 	sub	a, #0x7d
   6075 30 03         [12]  308 	jr	NC,00121$
   6077 3E FD         [ 7]  309 	ld	a, #0xfd
   6079 12            [ 7]  310 	ld	(de), a
   607A                     311 00121$:
                            312 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   607A C5            [11]  313 	push	bc
   607B D5            [11]  314 	push	de
   607C CD 2E 51      [17]  315 	call	_input_is_jump_just_pressed
   607F DD 75 FC      [19]  316 	ld	-4 (ix), l
   6082 D1            [10]  317 	pop	de
   6083 C1            [10]  318 	pop	bc
   6084 21 05 00      [10]  319 	ld	hl, #0x0005
   6087 09            [11]  320 	add	hl,bc
   6088 DD 75 FD      [19]  321 	ld	-3 (ix), l
   608B DD 74 FE      [19]  322 	ld	-2 (ix), h
   608E 21 01 00      [10]  323 	ld	hl, #0x0001
   6091 09            [11]  324 	add	hl,bc
   6092 DD 75 FA      [19]  325 	ld	-6 (ix), l
   6095 DD 74 FB      [19]  326 	ld	-5 (ix), h
                            327 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   6098 21 03 00      [10]  328 	ld	hl, #0x0003
   609B 09            [11]  329 	add	hl,bc
   609C DD 75 F8      [19]  330 	ld	-8 (ix), l
   609F DD 74 F9      [19]  331 	ld	-7 (ix), h
                            332 ;src/entities/player.c:71: player->jump_hold = 5;
   60A2 21 09 00      [10]  333 	ld	hl, #0x0009
   60A5 09            [11]  334 	add	hl,bc
   60A6 DD 75 F6      [19]  335 	ld	-10 (ix), l
   60A9 DD 74 F7      [19]  336 	ld	-9 (ix), h
                            337 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   60AC DD 7E FC      [19]  338 	ld	a, -4 (ix)
   60AF B7            [ 4]  339 	or	a, a
   60B0 28 4E         [12]  340 	jr	Z,00123$
   60B2 DD 6E FD      [19]  341 	ld	l,-3 (ix)
   60B5 DD 66 FE      [19]  342 	ld	h,-2 (ix)
   60B8 7E            [ 7]  343 	ld	a, (hl)
   60B9 DD 6E FA      [19]  344 	ld	l,-6 (ix)
   60BC DD 66 FB      [19]  345 	ld	h,-5 (ix)
   60BF 6E            [ 7]  346 	ld	l, (hl)
   60C0 DD 75 F4      [19]  347 	ld	-12 (ix), l
   60C3 DD 36 F5 00   [19]  348 	ld	-11 (ix), #0x00
   60C7 F5            [11]  349 	push	af
   60C8 0A            [ 7]  350 	ld	a, (bc)
   60C9 6F            [ 4]  351 	ld	l, a
   60CA F1            [10]  352 	pop	af
   60CB DD 75 F2      [19]  353 	ld	-14 (ix), l
   60CE DD 36 F3 00   [19]  354 	ld	-13 (ix), #0x00
   60D2 C5            [11]  355 	push	bc
   60D3 D5            [11]  356 	push	de
   60D4 F5            [11]  357 	push	af
   60D5 33            [ 6]  358 	inc	sp
   60D6 DD 6E F4      [19]  359 	ld	l,-12 (ix)
   60D9 DD 66 F5      [19]  360 	ld	h,-11 (ix)
   60DC E5            [11]  361 	push	hl
   60DD DD 6E F2      [19]  362 	ld	l,-14 (ix)
   60E0 DD 66 F3      [19]  363 	ld	h,-13 (ix)
   60E3 E5            [11]  364 	push	hl
   60E4 CD C1 4B      [17]  365 	call	_collision_is_on_ground_at
   60E7 F1            [10]  366 	pop	af
   60E8 F1            [10]  367 	pop	af
   60E9 33            [ 6]  368 	inc	sp
   60EA D1            [10]  369 	pop	de
   60EB C1            [10]  370 	pop	bc
   60EC 7D            [ 4]  371 	ld	a, l
   60ED B7            [ 4]  372 	or	a, a
   60EE 28 10         [12]  373 	jr	Z,00123$
                            374 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   60F0 DD 6E F8      [19]  375 	ld	l,-8 (ix)
   60F3 DD 66 F9      [19]  376 	ld	h,-7 (ix)
   60F6 36 FA         [10]  377 	ld	(hl), #0xfa
                            378 ;src/entities/player.c:71: player->jump_hold = 5;
   60F8 DD 6E F6      [19]  379 	ld	l,-10 (ix)
   60FB DD 66 F7      [19]  380 	ld	h,-9 (ix)
   60FE 36 05         [10]  381 	ld	(hl), #0x05
   6100                     382 00123$:
                            383 ;src/entities/player.c:74: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   6100 C5            [11]  384 	push	bc
   6101 D5            [11]  385 	push	de
   6102 CD 26 51      [17]  386 	call	_input_is_jump_pressed
   6105 7D            [ 4]  387 	ld	a, l
   6106 D1            [10]  388 	pop	de
   6107 C1            [10]  389 	pop	bc
   6108 B7            [ 4]  390 	or	a, a
   6109 28 31         [12]  391 	jr	Z,00126$
   610B DD 6E F6      [19]  392 	ld	l,-10 (ix)
   610E DD 66 F7      [19]  393 	ld	h,-9 (ix)
   6111 7E            [ 7]  394 	ld	a, (hl)
   6112 B7            [ 4]  395 	or	a, a
   6113 28 27         [12]  396 	jr	Z,00126$
   6115 DD 6E F8      [19]  397 	ld	l,-8 (ix)
   6118 DD 66 F9      [19]  398 	ld	h,-7 (ix)
   611B 6E            [ 7]  399 	ld	l, (hl)
   611C CB 7D         [ 8]  400 	bit	7, l
   611E 28 1C         [12]  401 	jr	Z,00126$
                            402 ;src/entities/player.c:75: player->vy = (i8)(player->vy + kplayerjumpboost);
   6120 7D            [ 4]  403 	ld	a, l
   6121 C6 FF         [ 7]  404 	add	a, #0xff
   6123 DD 6E F8      [19]  405 	ld	l,-8 (ix)
   6126 DD 66 F9      [19]  406 	ld	h,-7 (ix)
   6129 77            [ 7]  407 	ld	(hl), a
                            408 ;src/entities/player.c:76: player->jump_hold--;
   612A DD 6E F6      [19]  409 	ld	l,-10 (ix)
   612D DD 66 F7      [19]  410 	ld	h,-9 (ix)
   6130 7E            [ 7]  411 	ld	a, (hl)
   6131 C6 FF         [ 7]  412 	add	a, #0xff
   6133 DD 6E F6      [19]  413 	ld	l,-10 (ix)
   6136 DD 66 F7      [19]  414 	ld	h,-9 (ix)
   6139 77            [ 7]  415 	ld	(hl), a
   613A 18 08         [12]  416 	jr	00127$
   613C                     417 00126$:
                            418 ;src/entities/player.c:78: player->jump_hold = 0;
   613C DD 6E F6      [19]  419 	ld	l,-10 (ix)
   613F DD 66 F7      [19]  420 	ld	h,-9 (ix)
   6142 36 00         [10]  421 	ld	(hl), #0x00
   6144                     422 00127$:
                            423 ;src/entities/player.c:81: player->vy = (i8)(player->vy + kplayergravity);
   6144 DD 6E F8      [19]  424 	ld	l,-8 (ix)
   6147 DD 66 F9      [19]  425 	ld	h,-7 (ix)
   614A 7E            [ 7]  426 	ld	a, (hl)
   614B 3C            [ 4]  427 	inc	a
   614C DD 77 F2      [19]  428 	ld	-14 (ix), a
   614F DD 6E F8      [19]  429 	ld	l,-8 (ix)
   6152 DD 66 F9      [19]  430 	ld	h,-7 (ix)
   6155 DD 7E F2      [19]  431 	ld	a, -14 (ix)
   6158 77            [ 7]  432 	ld	(hl), a
                            433 ;src/entities/player.c:82: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   6159 3E 04         [ 7]  434 	ld	a, #0x04
   615B DD 96 F2      [19]  435 	sub	a, -14 (ix)
   615E E2 63 61      [10]  436 	jp	PO, 00226$
   6161 EE 80         [ 7]  437 	xor	a, #0x80
   6163                     438 00226$:
   6163 F2 6E 61      [10]  439 	jp	P, 00131$
   6166 DD 6E F8      [19]  440 	ld	l,-8 (ix)
   6169 DD 66 F9      [19]  441 	ld	h,-7 (ix)
   616C 36 04         [10]  442 	ld	(hl), #0x04
   616E                     443 00131$:
                            444 ;src/entities/player.c:84: nextx = (i16)player->x + (i16)player->vx;
   616E 0A            [ 7]  445 	ld	a, (bc)
   616F DD 77 F2      [19]  446 	ld	-14 (ix), a
   6172 DD 36 F3 00   [19]  447 	ld	-13 (ix), #0x00
   6176 1A            [ 7]  448 	ld	a, (de)
   6177 5F            [ 4]  449 	ld	e, a
   6178 17            [ 4]  450 	rla
   6179 9F            [ 4]  451 	sbc	a, a
   617A 57            [ 4]  452 	ld	d, a
   617B E1            [10]  453 	pop	hl
   617C E5            [11]  454 	push	hl
   617D 19            [11]  455 	add	hl, de
                            456 ;src/entities/player.c:85: if (nextx < 0) {
   617E CB 7C         [ 8]  457 	bit	7, h
   6180 28 03         [12]  458 	jr	Z,00133$
                            459 ;src/entities/player.c:86: nextx = 0;
   6182 21 00 00      [10]  460 	ld	hl, #0x0000
   6185                     461 00133$:
                            462 ;src/entities/player.c:88: if (nextx > 76) {
   6185 3E 4C         [ 7]  463 	ld	a, #0x4c
   6187 BD            [ 4]  464 	cp	a, l
   6188 3E 00         [ 7]  465 	ld	a, #0x00
   618A 9C            [ 4]  466 	sbc	a, h
   618B E2 90 61      [10]  467 	jp	PO, 00227$
   618E EE 80         [ 7]  468 	xor	a, #0x80
   6190                     469 00227$:
   6190 F2 96 61      [10]  470 	jp	P, 00135$
                            471 ;src/entities/player.c:89: nextx = 76;
   6193 21 4C 00      [10]  472 	ld	hl, #0x004c
   6196                     473 00135$:
                            474 ;src/entities/player.c:91: player->x = (u8)nextx;
   6196 DD 75 F2      [19]  475 	ld	-14 (ix), l
   6199 7D            [ 4]  476 	ld	a, l
   619A 02            [ 7]  477 	ld	(bc), a
                            478 ;src/entities/player.c:93: nexty = (i16)player->y + (i16)player->vy;
   619B DD 6E FA      [19]  479 	ld	l,-6 (ix)
   619E DD 66 FB      [19]  480 	ld	h,-5 (ix)
   61A1 5E            [ 7]  481 	ld	e, (hl)
   61A2 16 00         [ 7]  482 	ld	d, #0x00
   61A4 DD 6E F8      [19]  483 	ld	l,-8 (ix)
   61A7 DD 66 F9      [19]  484 	ld	h,-7 (ix)
   61AA 6E            [ 7]  485 	ld	l, (hl)
   61AB 7D            [ 4]  486 	ld	a, l
   61AC 17            [ 4]  487 	rla
   61AD 9F            [ 4]  488 	sbc	a, a
   61AE 67            [ 4]  489 	ld	h, a
   61AF 19            [11]  490 	add	hl, de
   61B0 E5            [11]  491 	push	hl
   61B1 FD E1         [14]  492 	pop	iy
                            493 ;src/entities/player.c:94: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   61B3 DD 6E FD      [19]  494 	ld	l,-3 (ix)
   61B6 DD 66 FE      [19]  495 	ld	h,-2 (ix)
   61B9 66            [ 7]  496 	ld	h, (hl)
   61BA DD 5E F2      [19]  497 	ld	e, -14 (ix)
   61BD 16 00         [ 7]  498 	ld	d, #0x00
   61BF C5            [11]  499 	push	bc
   61C0 E5            [11]  500 	push	hl
   61C1 33            [ 6]  501 	inc	sp
   61C2 FD E5         [15]  502 	push	iy
   61C4 D5            [11]  503 	push	de
   61C5 CD 40 4C      [17]  504 	call	_collision_clamp_y_at
   61C8 F1            [10]  505 	pop	af
   61C9 F1            [10]  506 	pop	af
   61CA 33            [ 6]  507 	inc	sp
   61CB C1            [10]  508 	pop	bc
                            509 ;src/entities/player.c:95: if (nexty < 0) {
   61CC CB 7C         [ 8]  510 	bit	7, h
   61CE 28 03         [12]  511 	jr	Z,00137$
                            512 ;src/entities/player.c:96: nexty = 0;
   61D0 21 00 00      [10]  513 	ld	hl, #0x0000
   61D3                     514 00137$:
                            515 ;src/entities/player.c:98: player->y = (u8)nexty;
   61D3 5D            [ 4]  516 	ld	e, l
   61D4 DD 6E FA      [19]  517 	ld	l,-6 (ix)
   61D7 DD 66 FB      [19]  518 	ld	h,-5 (ix)
   61DA 73            [ 7]  519 	ld	(hl), e
                            520 ;src/entities/player.c:100: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   61DB DD 6E FD      [19]  521 	ld	l,-3 (ix)
   61DE DD 66 FE      [19]  522 	ld	h,-2 (ix)
   61E1 7E            [ 7]  523 	ld	a, (hl)
   61E2 16 00         [ 7]  524 	ld	d, #0x00
   61E4 F5            [11]  525 	push	af
   61E5 0A            [ 7]  526 	ld	a, (bc)
   61E6 4F            [ 4]  527 	ld	c, a
   61E7 F1            [10]  528 	pop	af
   61E8 06 00         [ 7]  529 	ld	b, #0x00
   61EA F5            [11]  530 	push	af
   61EB 33            [ 6]  531 	inc	sp
   61EC D5            [11]  532 	push	de
   61ED C5            [11]  533 	push	bc
   61EE CD C1 4B      [17]  534 	call	_collision_is_on_ground_at
   61F1 F1            [10]  535 	pop	af
   61F2 F1            [10]  536 	pop	af
   61F3 33            [ 6]  537 	inc	sp
   61F4 7D            [ 4]  538 	ld	a, l
   61F5 B7            [ 4]  539 	or	a, a
   61F6 28 19         [12]  540 	jr	Z,00141$
   61F8 DD 6E F8      [19]  541 	ld	l,-8 (ix)
   61FB DD 66 F9      [19]  542 	ld	h,-7 (ix)
   61FE 4E            [ 7]  543 	ld	c, (hl)
   61FF AF            [ 4]  544 	xor	a, a
   6200 91            [ 4]  545 	sub	a, c
   6201 E2 06 62      [10]  546 	jp	PO, 00228$
   6204 EE 80         [ 7]  547 	xor	a, #0x80
   6206                     548 00228$:
   6206 F2 11 62      [10]  549 	jp	P, 00141$
                            550 ;src/entities/player.c:101: player->vy = 0;
   6209 DD 6E F8      [19]  551 	ld	l,-8 (ix)
   620C DD 66 F9      [19]  552 	ld	h,-7 (ix)
   620F 36 00         [10]  553 	ld	(hl), #0x00
   6211                     554 00141$:
   6211 DD F9         [10]  555 	ld	sp, ix
   6213 DD E1         [14]  556 	pop	ix
   6215 C9            [10]  557 	ret
                            558 ;src/entities/player.c:105: void playerrender(const Player* player) {
                            559 ;	---------------------------------
                            560 ; Function playerrender
                            561 ; ---------------------------------
   6216                     562 _playerrender::
   6216 DD E5         [15]  563 	push	ix
   6218 DD 21 00 00   [14]  564 	ld	ix,#0
   621C DD 39         [15]  565 	add	ix,sp
   621E 3B            [ 6]  566 	dec	sp
                            567 ;src/entities/player.c:108: if (!player) {
   621F DD 7E 05      [19]  568 	ld	a, 5 (ix)
   6222 DD B6 04      [19]  569 	or	a,4 (ix)
                            570 ;src/entities/player.c:109: return;
   6225 28 38         [12]  571 	jr	Z,00103$
                            572 ;src/entities/player.c:112: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   6227 DD 5E 04      [19]  573 	ld	e,4 (ix)
   622A DD 56 05      [19]  574 	ld	d,5 (ix)
   622D 6B            [ 4]  575 	ld	l, e
   622E 62            [ 4]  576 	ld	h, d
   622F 23            [ 6]  577 	inc	hl
   6230 46            [ 7]  578 	ld	b, (hl)
   6231 1A            [ 7]  579 	ld	a, (de)
   6232 D5            [11]  580 	push	de
   6233 C5            [11]  581 	push	bc
   6234 33            [ 6]  582 	inc	sp
   6235 F5            [11]  583 	push	af
   6236 33            [ 6]  584 	inc	sp
   6237 21 00 C0      [10]  585 	ld	hl, #0xc000
   623A E5            [11]  586 	push	hl
   623B CD 2D 67      [17]  587 	call	_cpct_getScreenPtr
   623E 4D            [ 4]  588 	ld	c, l
   623F 44            [ 4]  589 	ld	b, h
   6240 D1            [10]  590 	pop	de
                            591 ;src/entities/player.c:113: cpct_drawSprite((u8*)player_sprite, pvmem, player->w, player->h);
   6241 D5            [11]  592 	push	de
   6242 FD E1         [14]  593 	pop	iy
   6244 FD 7E 05      [19]  594 	ld	a, 5 (iy)
   6247 DD 77 FF      [19]  595 	ld	-1 (ix), a
   624A EB            [ 4]  596 	ex	de,hl
   624B 11 04 00      [10]  597 	ld	de, #0x0004
   624E 19            [11]  598 	add	hl, de
   624F 56            [ 7]  599 	ld	d, (hl)
   6250 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   6253 F5            [11]  601 	push	af
   6254 33            [ 6]  602 	inc	sp
   6255 D5            [11]  603 	push	de
   6256 33            [ 6]  604 	inc	sp
   6257 C5            [11]  605 	push	bc
   6258 21 8A 5F      [10]  606 	ld	hl, #_player_sprite
   625B E5            [11]  607 	push	hl
   625C CD 5E 65      [17]  608 	call	_cpct_drawSprite
   625F                     609 00103$:
   625F 33            [ 6]  610 	inc	sp
   6260 DD E1         [14]  611 	pop	ix
   6262 C9            [10]  612 	ret
                            613 ;src/entities/player.c:116: u8 player_get_health(const Player* player) {
                            614 ;	---------------------------------
                            615 ; Function player_get_health
                            616 ; ---------------------------------
   6263                     617 _player_get_health::
                            618 ;src/entities/player.c:117: return player ? player->health : 0;
   6263 21 03 00      [10]  619 	ld	hl, #2+1
   6266 39            [11]  620 	add	hl, sp
   6267 7E            [ 7]  621 	ld	a, (hl)
   6268 2B            [ 6]  622 	dec	hl
   6269 B6            [ 7]  623 	or	a,(hl)
   626A 28 0A         [12]  624 	jr	Z,00103$
   626C C1            [10]  625 	pop	bc
   626D E1            [10]  626 	pop	hl
   626E E5            [11]  627 	push	hl
   626F C5            [11]  628 	push	bc
   6270 11 06 00      [10]  629 	ld	de, #0x0006
   6273 19            [11]  630 	add	hl, de
   6274 6E            [ 7]  631 	ld	l, (hl)
   6275 C9            [10]  632 	ret
   6276                     633 00103$:
   6276 2E 00         [ 7]  634 	ld	l, #0x00
   6278 C9            [10]  635 	ret
                            636 ;src/entities/player.c:120: u8 player_get_weapon(const Player* player) {
                            637 ;	---------------------------------
                            638 ; Function player_get_weapon
                            639 ; ---------------------------------
   6279                     640 _player_get_weapon::
                            641 ;src/entities/player.c:121: return player ? player->weapon : 0;
   6279 21 03 00      [10]  642 	ld	hl, #2+1
   627C 39            [11]  643 	add	hl, sp
   627D 7E            [ 7]  644 	ld	a, (hl)
   627E 2B            [ 6]  645 	dec	hl
   627F B6            [ 7]  646 	or	a,(hl)
   6280 28 0A         [12]  647 	jr	Z,00103$
   6282 C1            [10]  648 	pop	bc
   6283 E1            [10]  649 	pop	hl
   6284 E5            [11]  650 	push	hl
   6285 C5            [11]  651 	push	bc
   6286 11 07 00      [10]  652 	ld	de, #0x0007
   6289 19            [11]  653 	add	hl, de
   628A 6E            [ 7]  654 	ld	l, (hl)
   628B C9            [10]  655 	ret
   628C                     656 00103$:
   628C 2E 00         [ 7]  657 	ld	l, #0x00
   628E C9            [10]  658 	ret
                            659 	.area _CODE
                            660 	.area _INITIALIZER
                            661 	.area _CABS (ABS)
