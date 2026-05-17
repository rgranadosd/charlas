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
   5EE6                      59 _playerinit::
                             60 ;src/entities/player.c:28: if (!player) {
   5EE6 21 03 00      [10]   61 	ld	hl, #2+1
   5EE9 39            [11]   62 	add	hl, sp
   5EEA 7E            [ 7]   63 	ld	a, (hl)
   5EEB 2B            [ 6]   64 	dec	hl
   5EEC B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:29: return;
   5EED C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:32: player->x = 20;
   5EEE D1            [10]   69 	pop	de
   5EEF C1            [10]   70 	pop	bc
   5EF0 C5            [11]   71 	push	bc
   5EF1 D5            [11]   72 	push	de
   5EF2 3E 14         [ 7]   73 	ld	a, #0x14
   5EF4 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:33: player->y = 120;
   5EF5 69            [ 4]   76 	ld	l, c
   5EF6 60            [ 4]   77 	ld	h, b
   5EF7 23            [ 6]   78 	inc	hl
   5EF8 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:34: player->vx = 0;
   5EFA 59            [ 4]   81 	ld	e, c
   5EFB 50            [ 4]   82 	ld	d, b
   5EFC 13            [ 6]   83 	inc	de
   5EFD 13            [ 6]   84 	inc	de
   5EFE AF            [ 4]   85 	xor	a, a
   5EFF 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:35: player->vy = 0;
   5F00 59            [ 4]   88 	ld	e, c
   5F01 50            [ 4]   89 	ld	d, b
   5F02 13            [ 6]   90 	inc	de
   5F03 13            [ 6]   91 	inc	de
   5F04 13            [ 6]   92 	inc	de
   5F05 AF            [ 4]   93 	xor	a, a
   5F06 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:36: player->w = 4;
   5F07 21 04 00      [10]   96 	ld	hl, #0x0004
   5F0A 09            [11]   97 	add	hl, bc
   5F0B 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:37: player->h = 16;
   5F0D 21 05 00      [10]  100 	ld	hl, #0x0005
   5F10 09            [11]  101 	add	hl, bc
   5F11 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:38: player->health = 3;
   5F13 21 06 00      [10]  104 	ld	hl, #0x0006
   5F16 09            [11]  105 	add	hl, bc
   5F17 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:39: player->weapon = 0;
   5F19 21 07 00      [10]  108 	ld	hl, #0x0007
   5F1C 09            [11]  109 	add	hl, bc
   5F1D 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:40: player->facing_left = 0;
   5F1F 21 08 00      [10]  112 	ld	hl, #0x0008
   5F22 09            [11]  113 	add	hl, bc
   5F23 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:41: player->jump_hold = 0;
   5F25 21 09 00      [10]  116 	ld	hl, #0x0009
   5F28 09            [11]  117 	add	hl, bc
   5F29 36 00         [10]  118 	ld	(hl), #0x00
   5F2B C9            [10]  119 	ret
   5F2C                     120 _player_sprite:
   5F2C F0                  121 	.db #0xf0	; 240
   5F2D F0                  122 	.db #0xf0	; 240
   5F2E F0                  123 	.db #0xf0	; 240
   5F2F F0                  124 	.db #0xf0	; 240
   5F30 F0                  125 	.db #0xf0	; 240
   5F31 00                  126 	.db #0x00	; 0
   5F32 F0                  127 	.db #0xf0	; 240
   5F33 F0                  128 	.db #0xf0	; 240
   5F34 F0                  129 	.db #0xf0	; 240
   5F35 00                  130 	.db #0x00	; 0
   5F36 F0                  131 	.db #0xf0	; 240
   5F37 F0                  132 	.db #0xf0	; 240
   5F38 F0                  133 	.db #0xf0	; 240
   5F39 00                  134 	.db #0x00	; 0
   5F3A F0                  135 	.db #0xf0	; 240
   5F3B F0                  136 	.db #0xf0	; 240
   5F3C F0                  137 	.db #0xf0	; 240
   5F3D 00                  138 	.db #0x00	; 0
   5F3E F0                  139 	.db #0xf0	; 240
   5F3F F0                  140 	.db #0xf0	; 240
   5F40 F0                  141 	.db #0xf0	; 240
   5F41 00                  142 	.db #0x00	; 0
   5F42 F0                  143 	.db #0xf0	; 240
   5F43 F0                  144 	.db #0xf0	; 240
   5F44 F0                  145 	.db #0xf0	; 240
   5F45 00                  146 	.db #0x00	; 0
   5F46 F0                  147 	.db #0xf0	; 240
   5F47 F0                  148 	.db #0xf0	; 240
   5F48 F0                  149 	.db #0xf0	; 240
   5F49 00                  150 	.db #0x00	; 0
   5F4A F0                  151 	.db #0xf0	; 240
   5F4B F0                  152 	.db #0xf0	; 240
   5F4C F0                  153 	.db #0xf0	; 240
   5F4D F0                  154 	.db #0xf0	; 240
   5F4E F0                  155 	.db #0xf0	; 240
   5F4F F0                  156 	.db #0xf0	; 240
   5F50 F0                  157 	.db #0xf0	; 240
   5F51 00                  158 	.db #0x00	; 0
   5F52 F0                  159 	.db #0xf0	; 240
   5F53 F0                  160 	.db #0xf0	; 240
   5F54 F0                  161 	.db #0xf0	; 240
   5F55 00                  162 	.db #0x00	; 0
   5F56 F0                  163 	.db #0xf0	; 240
   5F57 F0                  164 	.db #0xf0	; 240
   5F58 F0                  165 	.db #0xf0	; 240
   5F59 00                  166 	.db #0x00	; 0
   5F5A F0                  167 	.db #0xf0	; 240
   5F5B F0                  168 	.db #0xf0	; 240
   5F5C F0                  169 	.db #0xf0	; 240
   5F5D 00                  170 	.db #0x00	; 0
   5F5E F0                  171 	.db #0xf0	; 240
   5F5F F0                  172 	.db #0xf0	; 240
   5F60 F0                  173 	.db #0xf0	; 240
   5F61 00                  174 	.db #0x00	; 0
   5F62 F0                  175 	.db #0xf0	; 240
   5F63 F0                  176 	.db #0xf0	; 240
   5F64 F0                  177 	.db #0xf0	; 240
   5F65 00                  178 	.db #0x00	; 0
   5F66 F0                  179 	.db #0xf0	; 240
   5F67 F0                  180 	.db #0xf0	; 240
   5F68 F0                  181 	.db #0xf0	; 240
   5F69 F0                  182 	.db #0xf0	; 240
   5F6A F0                  183 	.db #0xf0	; 240
   5F6B F0                  184 	.db #0xf0	; 240
                            185 ;src/entities/player.c:44: void playerupdate(Player* player) {
                            186 ;	---------------------------------
                            187 ; Function playerupdate
                            188 ; ---------------------------------
   5F6C                     189 _playerupdate::
   5F6C DD E5         [15]  190 	push	ix
   5F6E DD 21 00 00   [14]  191 	ld	ix,#0
   5F72 DD 39         [15]  192 	add	ix,sp
   5F74 21 F2 FF      [10]  193 	ld	hl, #-14
   5F77 39            [11]  194 	add	hl, sp
   5F78 F9            [ 6]  195 	ld	sp, hl
                            196 ;src/entities/player.c:48: if (!player) {
   5F79 DD 7E 05      [19]  197 	ld	a, 5 (ix)
   5F7C DD B6 04      [19]  198 	or	a,4 (ix)
                            199 ;src/entities/player.c:49: return;
   5F7F CA B3 61      [10]  200 	jp	Z,00141$
                            201 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5F82 CD 8C 52      [17]  202 	call	_input_is_left_pressed
                            203 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5F85 DD 4E 04      [19]  204 	ld	c,4 (ix)
   5F88 DD 46 05      [19]  205 	ld	b,5 (ix)
   5F8B 59            [ 4]  206 	ld	e, c
   5F8C 50            [ 4]  207 	ld	d, b
   5F8D 13            [ 6]  208 	inc	de
   5F8E 13            [ 6]  209 	inc	de
                            210 ;src/entities/player.c:54: player->facing_left = 1;
   5F8F 79            [ 4]  211 	ld	a, c
   5F90 C6 08         [ 7]  212 	add	a, #0x08
   5F92 DD 77 FD      [19]  213 	ld	-3 (ix), a
   5F95 78            [ 4]  214 	ld	a, b
   5F96 CE 00         [ 7]  215 	adc	a, #0x00
   5F98 DD 77 FE      [19]  216 	ld	-2 (ix), a
                            217 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5F9B 7D            [ 4]  218 	ld	a, l
   5F9C B7            [ 4]  219 	or	a, a
   5F9D 28 0E         [12]  220 	jr	Z,00116$
                            221 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5F9F 1A            [ 7]  222 	ld	a, (de)
   5FA0 C6 FF         [ 7]  223 	add	a, #0xff
   5FA2 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/player.c:54: player->facing_left = 1;
   5FA3 DD 6E FD      [19]  226 	ld	l,-3 (ix)
   5FA6 DD 66 FE      [19]  227 	ld	h,-2 (ix)
   5FA9 36 01         [10]  228 	ld	(hl), #0x01
   5FAB 18 55         [12]  229 	jr	00117$
   5FAD                     230 00116$:
                            231 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5FAD C5            [11]  232 	push	bc
   5FAE D5            [11]  233 	push	de
   5FAF CD 94 52      [17]  234 	call	_input_is_right_pressed
   5FB2 DD 75 FF      [19]  235 	ld	-1 (ix), l
   5FB5 D1            [10]  236 	pop	de
   5FB6 C1            [10]  237 	pop	bc
                            238 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5FB7 1A            [ 7]  239 	ld	a, (de)
                            240 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5FB8 6F            [ 4]  241 	ld	l,a
   5FB9 3C            [ 4]  242 	inc	a
   5FBA DD 77 FC      [19]  243 	ld	-4 (ix), a
                            244 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5FBD DD 7E FF      [19]  245 	ld	a, -1 (ix)
   5FC0 B7            [ 4]  246 	or	a, a
   5FC1 28 0E         [12]  247 	jr	Z,00113$
                            248 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5FC3 DD 7E FC      [19]  249 	ld	a, -4 (ix)
   5FC6 12            [ 7]  250 	ld	(de), a
                            251 ;src/entities/player.c:57: player->facing_left = 0;
   5FC7 DD 6E FD      [19]  252 	ld	l,-3 (ix)
   5FCA DD 66 FE      [19]  253 	ld	h,-2 (ix)
   5FCD 36 00         [10]  254 	ld	(hl), #0x00
   5FCF 18 31         [12]  255 	jr	00117$
   5FD1                     256 00113$:
                            257 ;src/entities/player.c:58: } else if (player->vx > 0) {
   5FD1 AF            [ 4]  258 	xor	a, a
   5FD2 95            [ 4]  259 	sub	a, l
   5FD3 E2 D8 5F      [10]  260 	jp	PO, 00223$
   5FD6 EE 80         [ 7]  261 	xor	a, #0x80
   5FD8                     262 00223$:
   5FD8 F2 EC 5F      [10]  263 	jp	P, 00110$
                            264 ;src/entities/player.c:59: player->vx = (i8)(player->vx - kplayerdeceleration);
   5FDB 7D            [ 4]  265 	ld	a, l
   5FDC C6 FF         [ 7]  266 	add	a, #0xff
   5FDE DD 77 FF      [19]  267 	ld	-1 (ix), a
   5FE1 12            [ 7]  268 	ld	(de),a
                            269 ;src/entities/player.c:60: if (player->vx < 0) player->vx = 0;
   5FE2 DD CB FF 7E   [20]  270 	bit	7, -1 (ix)
   5FE6 28 1A         [12]  271 	jr	Z,00117$
   5FE8 AF            [ 4]  272 	xor	a, a
   5FE9 12            [ 7]  273 	ld	(de), a
   5FEA 18 16         [12]  274 	jr	00117$
   5FEC                     275 00110$:
                            276 ;src/entities/player.c:61: } else if (player->vx < 0) {
   5FEC CB 7D         [ 8]  277 	bit	7, l
   5FEE 28 12         [12]  278 	jr	Z,00117$
                            279 ;src/entities/player.c:62: player->vx = (i8)(player->vx + kplayerdeceleration);
   5FF0 DD 7E FC      [19]  280 	ld	a, -4 (ix)
   5FF3 12            [ 7]  281 	ld	(de), a
                            282 ;src/entities/player.c:63: if (player->vx > 0) player->vx = 0;
   5FF4 AF            [ 4]  283 	xor	a, a
   5FF5 DD 96 FC      [19]  284 	sub	a, -4 (ix)
   5FF8 E2 FD 5F      [10]  285 	jp	PO, 00224$
   5FFB EE 80         [ 7]  286 	xor	a, #0x80
   5FFD                     287 00224$:
   5FFD F2 02 60      [10]  288 	jp	P, 00117$
   6000 AF            [ 4]  289 	xor	a, a
   6001 12            [ 7]  290 	ld	(de), a
   6002                     291 00117$:
                            292 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   6002 1A            [ 7]  293 	ld	a, (de)
   6003 6F            [ 4]  294 	ld	l, a
   6004 3E 03         [ 7]  295 	ld	a, #0x03
   6006 95            [ 4]  296 	sub	a, l
   6007 E2 0C 60      [10]  297 	jp	PO, 00225$
   600A EE 80         [ 7]  298 	xor	a, #0x80
   600C                     299 00225$:
   600C F2 12 60      [10]  300 	jp	P, 00119$
   600F 3E 03         [ 7]  301 	ld	a, #0x03
   6011 12            [ 7]  302 	ld	(de), a
   6012                     303 00119$:
                            304 ;src/entities/player.c:67: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   6012 1A            [ 7]  305 	ld	a, (de)
   6013 EE 80         [ 7]  306 	xor	a, #0x80
   6015 D6 7D         [ 7]  307 	sub	a, #0x7d
   6017 30 03         [12]  308 	jr	NC,00121$
   6019 3E FD         [ 7]  309 	ld	a, #0xfd
   601B 12            [ 7]  310 	ld	(de), a
   601C                     311 00121$:
                            312 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   601C C5            [11]  313 	push	bc
   601D D5            [11]  314 	push	de
   601E CD B4 52      [17]  315 	call	_input_is_jump_just_pressed
   6021 DD 75 FC      [19]  316 	ld	-4 (ix), l
   6024 D1            [10]  317 	pop	de
   6025 C1            [10]  318 	pop	bc
   6026 21 05 00      [10]  319 	ld	hl, #0x0005
   6029 09            [11]  320 	add	hl,bc
   602A DD 75 FD      [19]  321 	ld	-3 (ix), l
   602D DD 74 FE      [19]  322 	ld	-2 (ix), h
   6030 21 01 00      [10]  323 	ld	hl, #0x0001
   6033 09            [11]  324 	add	hl,bc
   6034 DD 75 FA      [19]  325 	ld	-6 (ix), l
   6037 DD 74 FB      [19]  326 	ld	-5 (ix), h
                            327 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   603A 21 03 00      [10]  328 	ld	hl, #0x0003
   603D 09            [11]  329 	add	hl,bc
   603E DD 75 F8      [19]  330 	ld	-8 (ix), l
   6041 DD 74 F9      [19]  331 	ld	-7 (ix), h
                            332 ;src/entities/player.c:71: player->jump_hold = 5;
   6044 21 09 00      [10]  333 	ld	hl, #0x0009
   6047 09            [11]  334 	add	hl,bc
   6048 DD 75 F6      [19]  335 	ld	-10 (ix), l
   604B DD 74 F7      [19]  336 	ld	-9 (ix), h
                            337 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   604E DD 7E FC      [19]  338 	ld	a, -4 (ix)
   6051 B7            [ 4]  339 	or	a, a
   6052 28 4E         [12]  340 	jr	Z,00123$
   6054 DD 6E FD      [19]  341 	ld	l,-3 (ix)
   6057 DD 66 FE      [19]  342 	ld	h,-2 (ix)
   605A 7E            [ 7]  343 	ld	a, (hl)
   605B DD 6E FA      [19]  344 	ld	l,-6 (ix)
   605E DD 66 FB      [19]  345 	ld	h,-5 (ix)
   6061 6E            [ 7]  346 	ld	l, (hl)
   6062 DD 75 F4      [19]  347 	ld	-12 (ix), l
   6065 DD 36 F5 00   [19]  348 	ld	-11 (ix), #0x00
   6069 F5            [11]  349 	push	af
   606A 0A            [ 7]  350 	ld	a, (bc)
   606B 6F            [ 4]  351 	ld	l, a
   606C F1            [10]  352 	pop	af
   606D DD 75 F2      [19]  353 	ld	-14 (ix), l
   6070 DD 36 F3 00   [19]  354 	ld	-13 (ix), #0x00
   6074 C5            [11]  355 	push	bc
   6075 D5            [11]  356 	push	de
   6076 F5            [11]  357 	push	af
   6077 33            [ 6]  358 	inc	sp
   6078 DD 6E F4      [19]  359 	ld	l,-12 (ix)
   607B DD 66 F5      [19]  360 	ld	h,-11 (ix)
   607E E5            [11]  361 	push	hl
   607F DD 6E F2      [19]  362 	ld	l,-14 (ix)
   6082 DD 66 F3      [19]  363 	ld	h,-13 (ix)
   6085 E5            [11]  364 	push	hl
   6086 CD C3 4B      [17]  365 	call	_collision_is_on_ground_at
   6089 F1            [10]  366 	pop	af
   608A F1            [10]  367 	pop	af
   608B 33            [ 6]  368 	inc	sp
   608C D1            [10]  369 	pop	de
   608D C1            [10]  370 	pop	bc
   608E 7D            [ 4]  371 	ld	a, l
   608F B7            [ 4]  372 	or	a, a
   6090 28 10         [12]  373 	jr	Z,00123$
                            374 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   6092 DD 6E F8      [19]  375 	ld	l,-8 (ix)
   6095 DD 66 F9      [19]  376 	ld	h,-7 (ix)
   6098 36 FA         [10]  377 	ld	(hl), #0xfa
                            378 ;src/entities/player.c:71: player->jump_hold = 5;
   609A DD 6E F6      [19]  379 	ld	l,-10 (ix)
   609D DD 66 F7      [19]  380 	ld	h,-9 (ix)
   60A0 36 05         [10]  381 	ld	(hl), #0x05
   60A2                     382 00123$:
                            383 ;src/entities/player.c:74: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   60A2 C5            [11]  384 	push	bc
   60A3 D5            [11]  385 	push	de
   60A4 CD AC 52      [17]  386 	call	_input_is_jump_pressed
   60A7 7D            [ 4]  387 	ld	a, l
   60A8 D1            [10]  388 	pop	de
   60A9 C1            [10]  389 	pop	bc
   60AA B7            [ 4]  390 	or	a, a
   60AB 28 31         [12]  391 	jr	Z,00126$
   60AD DD 6E F6      [19]  392 	ld	l,-10 (ix)
   60B0 DD 66 F7      [19]  393 	ld	h,-9 (ix)
   60B3 7E            [ 7]  394 	ld	a, (hl)
   60B4 B7            [ 4]  395 	or	a, a
   60B5 28 27         [12]  396 	jr	Z,00126$
   60B7 DD 6E F8      [19]  397 	ld	l,-8 (ix)
   60BA DD 66 F9      [19]  398 	ld	h,-7 (ix)
   60BD 6E            [ 7]  399 	ld	l, (hl)
   60BE CB 7D         [ 8]  400 	bit	7, l
   60C0 28 1C         [12]  401 	jr	Z,00126$
                            402 ;src/entities/player.c:75: player->vy = (i8)(player->vy + kplayerjumpboost);
   60C2 7D            [ 4]  403 	ld	a, l
   60C3 C6 FF         [ 7]  404 	add	a, #0xff
   60C5 DD 6E F8      [19]  405 	ld	l,-8 (ix)
   60C8 DD 66 F9      [19]  406 	ld	h,-7 (ix)
   60CB 77            [ 7]  407 	ld	(hl), a
                            408 ;src/entities/player.c:76: player->jump_hold--;
   60CC DD 6E F6      [19]  409 	ld	l,-10 (ix)
   60CF DD 66 F7      [19]  410 	ld	h,-9 (ix)
   60D2 7E            [ 7]  411 	ld	a, (hl)
   60D3 C6 FF         [ 7]  412 	add	a, #0xff
   60D5 DD 6E F6      [19]  413 	ld	l,-10 (ix)
   60D8 DD 66 F7      [19]  414 	ld	h,-9 (ix)
   60DB 77            [ 7]  415 	ld	(hl), a
   60DC 18 08         [12]  416 	jr	00127$
   60DE                     417 00126$:
                            418 ;src/entities/player.c:78: player->jump_hold = 0;
   60DE DD 6E F6      [19]  419 	ld	l,-10 (ix)
   60E1 DD 66 F7      [19]  420 	ld	h,-9 (ix)
   60E4 36 00         [10]  421 	ld	(hl), #0x00
   60E6                     422 00127$:
                            423 ;src/entities/player.c:81: player->vy = (i8)(player->vy + kplayergravity);
   60E6 DD 6E F8      [19]  424 	ld	l,-8 (ix)
   60E9 DD 66 F9      [19]  425 	ld	h,-7 (ix)
   60EC 7E            [ 7]  426 	ld	a, (hl)
   60ED 3C            [ 4]  427 	inc	a
   60EE DD 77 F2      [19]  428 	ld	-14 (ix), a
   60F1 DD 6E F8      [19]  429 	ld	l,-8 (ix)
   60F4 DD 66 F9      [19]  430 	ld	h,-7 (ix)
   60F7 DD 7E F2      [19]  431 	ld	a, -14 (ix)
   60FA 77            [ 7]  432 	ld	(hl), a
                            433 ;src/entities/player.c:82: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   60FB 3E 04         [ 7]  434 	ld	a, #0x04
   60FD DD 96 F2      [19]  435 	sub	a, -14 (ix)
   6100 E2 05 61      [10]  436 	jp	PO, 00226$
   6103 EE 80         [ 7]  437 	xor	a, #0x80
   6105                     438 00226$:
   6105 F2 10 61      [10]  439 	jp	P, 00131$
   6108 DD 6E F8      [19]  440 	ld	l,-8 (ix)
   610B DD 66 F9      [19]  441 	ld	h,-7 (ix)
   610E 36 04         [10]  442 	ld	(hl), #0x04
   6110                     443 00131$:
                            444 ;src/entities/player.c:84: nextx = (i16)player->x + (i16)player->vx;
   6110 0A            [ 7]  445 	ld	a, (bc)
   6111 DD 77 F2      [19]  446 	ld	-14 (ix), a
   6114 DD 36 F3 00   [19]  447 	ld	-13 (ix), #0x00
   6118 1A            [ 7]  448 	ld	a, (de)
   6119 5F            [ 4]  449 	ld	e, a
   611A 17            [ 4]  450 	rla
   611B 9F            [ 4]  451 	sbc	a, a
   611C 57            [ 4]  452 	ld	d, a
   611D E1            [10]  453 	pop	hl
   611E E5            [11]  454 	push	hl
   611F 19            [11]  455 	add	hl, de
                            456 ;src/entities/player.c:85: if (nextx < 0) {
   6120 CB 7C         [ 8]  457 	bit	7, h
   6122 28 03         [12]  458 	jr	Z,00133$
                            459 ;src/entities/player.c:86: nextx = 0;
   6124 21 00 00      [10]  460 	ld	hl, #0x0000
   6127                     461 00133$:
                            462 ;src/entities/player.c:88: if (nextx > 76) {
   6127 3E 4C         [ 7]  463 	ld	a, #0x4c
   6129 BD            [ 4]  464 	cp	a, l
   612A 3E 00         [ 7]  465 	ld	a, #0x00
   612C 9C            [ 4]  466 	sbc	a, h
   612D E2 32 61      [10]  467 	jp	PO, 00227$
   6130 EE 80         [ 7]  468 	xor	a, #0x80
   6132                     469 00227$:
   6132 F2 38 61      [10]  470 	jp	P, 00135$
                            471 ;src/entities/player.c:89: nextx = 76;
   6135 21 4C 00      [10]  472 	ld	hl, #0x004c
   6138                     473 00135$:
                            474 ;src/entities/player.c:91: player->x = (u8)nextx;
   6138 DD 75 F2      [19]  475 	ld	-14 (ix), l
   613B 7D            [ 4]  476 	ld	a, l
   613C 02            [ 7]  477 	ld	(bc), a
                            478 ;src/entities/player.c:93: nexty = (i16)player->y + (i16)player->vy;
   613D DD 6E FA      [19]  479 	ld	l,-6 (ix)
   6140 DD 66 FB      [19]  480 	ld	h,-5 (ix)
   6143 5E            [ 7]  481 	ld	e, (hl)
   6144 16 00         [ 7]  482 	ld	d, #0x00
   6146 DD 6E F8      [19]  483 	ld	l,-8 (ix)
   6149 DD 66 F9      [19]  484 	ld	h,-7 (ix)
   614C 6E            [ 7]  485 	ld	l, (hl)
   614D 7D            [ 4]  486 	ld	a, l
   614E 17            [ 4]  487 	rla
   614F 9F            [ 4]  488 	sbc	a, a
   6150 67            [ 4]  489 	ld	h, a
   6151 19            [11]  490 	add	hl, de
   6152 E5            [11]  491 	push	hl
   6153 FD E1         [14]  492 	pop	iy
                            493 ;src/entities/player.c:94: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   6155 DD 6E FD      [19]  494 	ld	l,-3 (ix)
   6158 DD 66 FE      [19]  495 	ld	h,-2 (ix)
   615B 66            [ 7]  496 	ld	h, (hl)
   615C DD 5E F2      [19]  497 	ld	e, -14 (ix)
   615F 16 00         [ 7]  498 	ld	d, #0x00
   6161 C5            [11]  499 	push	bc
   6162 E5            [11]  500 	push	hl
   6163 33            [ 6]  501 	inc	sp
   6164 FD E5         [15]  502 	push	iy
   6166 D5            [11]  503 	push	de
   6167 CD 42 4C      [17]  504 	call	_collision_clamp_y_at
   616A F1            [10]  505 	pop	af
   616B F1            [10]  506 	pop	af
   616C 33            [ 6]  507 	inc	sp
   616D C1            [10]  508 	pop	bc
                            509 ;src/entities/player.c:95: if (nexty < 0) {
   616E CB 7C         [ 8]  510 	bit	7, h
   6170 28 03         [12]  511 	jr	Z,00137$
                            512 ;src/entities/player.c:96: nexty = 0;
   6172 21 00 00      [10]  513 	ld	hl, #0x0000
   6175                     514 00137$:
                            515 ;src/entities/player.c:98: player->y = (u8)nexty;
   6175 5D            [ 4]  516 	ld	e, l
   6176 DD 6E FA      [19]  517 	ld	l,-6 (ix)
   6179 DD 66 FB      [19]  518 	ld	h,-5 (ix)
   617C 73            [ 7]  519 	ld	(hl), e
                            520 ;src/entities/player.c:100: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   617D DD 6E FD      [19]  521 	ld	l,-3 (ix)
   6180 DD 66 FE      [19]  522 	ld	h,-2 (ix)
   6183 7E            [ 7]  523 	ld	a, (hl)
   6184 16 00         [ 7]  524 	ld	d, #0x00
   6186 F5            [11]  525 	push	af
   6187 0A            [ 7]  526 	ld	a, (bc)
   6188 4F            [ 4]  527 	ld	c, a
   6189 F1            [10]  528 	pop	af
   618A 06 00         [ 7]  529 	ld	b, #0x00
   618C F5            [11]  530 	push	af
   618D 33            [ 6]  531 	inc	sp
   618E D5            [11]  532 	push	de
   618F C5            [11]  533 	push	bc
   6190 CD C3 4B      [17]  534 	call	_collision_is_on_ground_at
   6193 F1            [10]  535 	pop	af
   6194 F1            [10]  536 	pop	af
   6195 33            [ 6]  537 	inc	sp
   6196 7D            [ 4]  538 	ld	a, l
   6197 B7            [ 4]  539 	or	a, a
   6198 28 19         [12]  540 	jr	Z,00141$
   619A DD 6E F8      [19]  541 	ld	l,-8 (ix)
   619D DD 66 F9      [19]  542 	ld	h,-7 (ix)
   61A0 4E            [ 7]  543 	ld	c, (hl)
   61A1 AF            [ 4]  544 	xor	a, a
   61A2 91            [ 4]  545 	sub	a, c
   61A3 E2 A8 61      [10]  546 	jp	PO, 00228$
   61A6 EE 80         [ 7]  547 	xor	a, #0x80
   61A8                     548 00228$:
   61A8 F2 B3 61      [10]  549 	jp	P, 00141$
                            550 ;src/entities/player.c:101: player->vy = 0;
   61AB DD 6E F8      [19]  551 	ld	l,-8 (ix)
   61AE DD 66 F9      [19]  552 	ld	h,-7 (ix)
   61B1 36 00         [10]  553 	ld	(hl), #0x00
   61B3                     554 00141$:
   61B3 DD F9         [10]  555 	ld	sp, ix
   61B5 DD E1         [14]  556 	pop	ix
   61B7 C9            [10]  557 	ret
                            558 ;src/entities/player.c:105: void playerrender(const Player* player) {
                            559 ;	---------------------------------
                            560 ; Function playerrender
                            561 ; ---------------------------------
   61B8                     562 _playerrender::
   61B8 DD E5         [15]  563 	push	ix
   61BA DD 21 00 00   [14]  564 	ld	ix,#0
   61BE DD 39         [15]  565 	add	ix,sp
   61C0 3B            [ 6]  566 	dec	sp
                            567 ;src/entities/player.c:108: if (!player) {
   61C1 DD 7E 05      [19]  568 	ld	a, 5 (ix)
   61C4 DD B6 04      [19]  569 	or	a,4 (ix)
                            570 ;src/entities/player.c:109: return;
   61C7 28 38         [12]  571 	jr	Z,00103$
                            572 ;src/entities/player.c:112: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   61C9 DD 5E 04      [19]  573 	ld	e,4 (ix)
   61CC DD 56 05      [19]  574 	ld	d,5 (ix)
   61CF 6B            [ 4]  575 	ld	l, e
   61D0 62            [ 4]  576 	ld	h, d
   61D1 23            [ 6]  577 	inc	hl
   61D2 46            [ 7]  578 	ld	b, (hl)
   61D3 1A            [ 7]  579 	ld	a, (de)
   61D4 D5            [11]  580 	push	de
   61D5 C5            [11]  581 	push	bc
   61D6 33            [ 6]  582 	inc	sp
   61D7 F5            [11]  583 	push	af
   61D8 33            [ 6]  584 	inc	sp
   61D9 21 00 C0      [10]  585 	ld	hl, #0xc000
   61DC E5            [11]  586 	push	hl
   61DD CD D6 66      [17]  587 	call	_cpct_getScreenPtr
   61E0 4D            [ 4]  588 	ld	c, l
   61E1 44            [ 4]  589 	ld	b, h
   61E2 D1            [10]  590 	pop	de
                            591 ;src/entities/player.c:113: cpct_drawSprite((u8*)player_sprite, pvmem, player->w, player->h);
   61E3 D5            [11]  592 	push	de
   61E4 FD E1         [14]  593 	pop	iy
   61E6 FD 7E 05      [19]  594 	ld	a, 5 (iy)
   61E9 DD 77 FF      [19]  595 	ld	-1 (ix), a
   61EC EB            [ 4]  596 	ex	de,hl
   61ED 11 04 00      [10]  597 	ld	de, #0x0004
   61F0 19            [11]  598 	add	hl, de
   61F1 56            [ 7]  599 	ld	d, (hl)
   61F2 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   61F5 F5            [11]  601 	push	af
   61F6 33            [ 6]  602 	inc	sp
   61F7 D5            [11]  603 	push	de
   61F8 33            [ 6]  604 	inc	sp
   61F9 C5            [11]  605 	push	bc
   61FA 21 2C 5F      [10]  606 	ld	hl, #_player_sprite
   61FD E5            [11]  607 	push	hl
   61FE CD 07 65      [17]  608 	call	_cpct_drawSprite
   6201                     609 00103$:
   6201 33            [ 6]  610 	inc	sp
   6202 DD E1         [14]  611 	pop	ix
   6204 C9            [10]  612 	ret
                            613 ;src/entities/player.c:116: u8 player_get_health(const Player* player) {
                            614 ;	---------------------------------
                            615 ; Function player_get_health
                            616 ; ---------------------------------
   6205                     617 _player_get_health::
                            618 ;src/entities/player.c:117: return player ? player->health : 0;
   6205 21 03 00      [10]  619 	ld	hl, #2+1
   6208 39            [11]  620 	add	hl, sp
   6209 7E            [ 7]  621 	ld	a, (hl)
   620A 2B            [ 6]  622 	dec	hl
   620B B6            [ 7]  623 	or	a,(hl)
   620C 28 0A         [12]  624 	jr	Z,00103$
   620E C1            [10]  625 	pop	bc
   620F E1            [10]  626 	pop	hl
   6210 E5            [11]  627 	push	hl
   6211 C5            [11]  628 	push	bc
   6212 11 06 00      [10]  629 	ld	de, #0x0006
   6215 19            [11]  630 	add	hl, de
   6216 6E            [ 7]  631 	ld	l, (hl)
   6217 C9            [10]  632 	ret
   6218                     633 00103$:
   6218 2E 00         [ 7]  634 	ld	l, #0x00
   621A C9            [10]  635 	ret
                            636 ;src/entities/player.c:120: u8 player_get_weapon(const Player* player) {
                            637 ;	---------------------------------
                            638 ; Function player_get_weapon
                            639 ; ---------------------------------
   621B                     640 _player_get_weapon::
                            641 ;src/entities/player.c:121: return player ? player->weapon : 0;
   621B 21 03 00      [10]  642 	ld	hl, #2+1
   621E 39            [11]  643 	add	hl, sp
   621F 7E            [ 7]  644 	ld	a, (hl)
   6220 2B            [ 6]  645 	dec	hl
   6221 B6            [ 7]  646 	or	a,(hl)
   6222 28 0A         [12]  647 	jr	Z,00103$
   6224 C1            [10]  648 	pop	bc
   6225 E1            [10]  649 	pop	hl
   6226 E5            [11]  650 	push	hl
   6227 C5            [11]  651 	push	bc
   6228 11 07 00      [10]  652 	ld	de, #0x0007
   622B 19            [11]  653 	add	hl, de
   622C 6E            [ 7]  654 	ld	l, (hl)
   622D C9            [10]  655 	ret
   622E                     656 00103$:
   622E 2E 00         [ 7]  657 	ld	l, #0x00
   6230 C9            [10]  658 	ret
                            659 	.area _CODE
                            660 	.area _INITIALIZER
                            661 	.area _CABS (ABS)
