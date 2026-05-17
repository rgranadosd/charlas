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
                             55 ;src/entities/player.c:17: void playerinit(Player* player) {
                             56 ;	---------------------------------
                             57 ; Function playerinit
                             58 ; ---------------------------------
   5C12                      59 _playerinit::
                             60 ;src/entities/player.c:18: if (!player) {
   5C12 21 03 00      [10]   61 	ld	hl, #2+1
   5C15 39            [11]   62 	add	hl, sp
   5C16 7E            [ 7]   63 	ld	a, (hl)
   5C17 2B            [ 6]   64 	dec	hl
   5C18 B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:19: return;
   5C19 C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:22: player->x = 20;
   5C1A D1            [10]   69 	pop	de
   5C1B C1            [10]   70 	pop	bc
   5C1C C5            [11]   71 	push	bc
   5C1D D5            [11]   72 	push	de
   5C1E 3E 14         [ 7]   73 	ld	a, #0x14
   5C20 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:23: player->y = 120;
   5C21 69            [ 4]   76 	ld	l, c
   5C22 60            [ 4]   77 	ld	h, b
   5C23 23            [ 6]   78 	inc	hl
   5C24 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:24: player->vx = 0;
   5C26 59            [ 4]   81 	ld	e, c
   5C27 50            [ 4]   82 	ld	d, b
   5C28 13            [ 6]   83 	inc	de
   5C29 13            [ 6]   84 	inc	de
   5C2A AF            [ 4]   85 	xor	a, a
   5C2B 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:25: player->vy = 0;
   5C2C 59            [ 4]   88 	ld	e, c
   5C2D 50            [ 4]   89 	ld	d, b
   5C2E 13            [ 6]   90 	inc	de
   5C2F 13            [ 6]   91 	inc	de
   5C30 13            [ 6]   92 	inc	de
   5C31 AF            [ 4]   93 	xor	a, a
   5C32 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:26: player->w = 4;
   5C33 21 04 00      [10]   96 	ld	hl, #0x0004
   5C36 09            [11]   97 	add	hl, bc
   5C37 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:27: player->h = 16;
   5C39 21 05 00      [10]  100 	ld	hl, #0x0005
   5C3C 09            [11]  101 	add	hl, bc
   5C3D 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:28: player->health = 3;
   5C3F 21 06 00      [10]  104 	ld	hl, #0x0006
   5C42 09            [11]  105 	add	hl, bc
   5C43 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:29: player->weapon = 0;
   5C45 21 07 00      [10]  108 	ld	hl, #0x0007
   5C48 09            [11]  109 	add	hl, bc
   5C49 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:30: player->facing_left = 0;
   5C4B 21 08 00      [10]  112 	ld	hl, #0x0008
   5C4E 09            [11]  113 	add	hl, bc
   5C4F 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:31: player->jump_hold = 0;
   5C51 21 09 00      [10]  116 	ld	hl, #0x0009
   5C54 09            [11]  117 	add	hl, bc
   5C55 36 00         [10]  118 	ld	(hl), #0x00
   5C57 C9            [10]  119 	ret
                            120 ;src/entities/player.c:34: void playerupdate(Player* player) {
                            121 ;	---------------------------------
                            122 ; Function playerupdate
                            123 ; ---------------------------------
   5C58                     124 _playerupdate::
   5C58 DD E5         [15]  125 	push	ix
   5C5A DD 21 00 00   [14]  126 	ld	ix,#0
   5C5E DD 39         [15]  127 	add	ix,sp
   5C60 21 F2 FF      [10]  128 	ld	hl, #-14
   5C63 39            [11]  129 	add	hl, sp
   5C64 F9            [ 6]  130 	ld	sp, hl
                            131 ;src/entities/player.c:38: if (!player) {
   5C65 DD 7E 05      [19]  132 	ld	a, 5 (ix)
   5C68 DD B6 04      [19]  133 	or	a,4 (ix)
                            134 ;src/entities/player.c:39: return;
   5C6B CA 9F 5E      [10]  135 	jp	Z,00141$
                            136 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5C6E CD 20 52      [17]  137 	call	_input_is_left_pressed
                            138 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5C71 DD 4E 04      [19]  139 	ld	c,4 (ix)
   5C74 DD 46 05      [19]  140 	ld	b,5 (ix)
   5C77 59            [ 4]  141 	ld	e, c
   5C78 50            [ 4]  142 	ld	d, b
   5C79 13            [ 6]  143 	inc	de
   5C7A 13            [ 6]  144 	inc	de
                            145 ;src/entities/player.c:44: player->facing_left = 1;
   5C7B 79            [ 4]  146 	ld	a, c
   5C7C C6 08         [ 7]  147 	add	a, #0x08
   5C7E DD 77 F8      [19]  148 	ld	-8 (ix), a
   5C81 78            [ 4]  149 	ld	a, b
   5C82 CE 00         [ 7]  150 	adc	a, #0x00
   5C84 DD 77 F9      [19]  151 	ld	-7 (ix), a
                            152 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5C87 7D            [ 4]  153 	ld	a, l
   5C88 B7            [ 4]  154 	or	a, a
   5C89 28 0E         [12]  155 	jr	Z,00116$
                            156 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5C8B 1A            [ 7]  157 	ld	a, (de)
   5C8C C6 FF         [ 7]  158 	add	a, #0xff
   5C8E 12            [ 7]  159 	ld	(de), a
                            160 ;src/entities/player.c:44: player->facing_left = 1;
   5C8F DD 6E F8      [19]  161 	ld	l,-8 (ix)
   5C92 DD 66 F9      [19]  162 	ld	h,-7 (ix)
   5C95 36 01         [10]  163 	ld	(hl), #0x01
   5C97 18 55         [12]  164 	jr	00117$
   5C99                     165 00116$:
                            166 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5C99 C5            [11]  167 	push	bc
   5C9A D5            [11]  168 	push	de
   5C9B CD 28 52      [17]  169 	call	_input_is_right_pressed
   5C9E DD 75 FF      [19]  170 	ld	-1 (ix), l
   5CA1 D1            [10]  171 	pop	de
   5CA2 C1            [10]  172 	pop	bc
                            173 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5CA3 1A            [ 7]  174 	ld	a, (de)
                            175 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5CA4 6F            [ 4]  176 	ld	l,a
   5CA5 3C            [ 4]  177 	inc	a
   5CA6 DD 77 FE      [19]  178 	ld	-2 (ix), a
                            179 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5CA9 DD 7E FF      [19]  180 	ld	a, -1 (ix)
   5CAC B7            [ 4]  181 	or	a, a
   5CAD 28 0E         [12]  182 	jr	Z,00113$
                            183 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5CAF DD 7E FE      [19]  184 	ld	a, -2 (ix)
   5CB2 12            [ 7]  185 	ld	(de), a
                            186 ;src/entities/player.c:47: player->facing_left = 0;
   5CB3 DD 6E F8      [19]  187 	ld	l,-8 (ix)
   5CB6 DD 66 F9      [19]  188 	ld	h,-7 (ix)
   5CB9 36 00         [10]  189 	ld	(hl), #0x00
   5CBB 18 31         [12]  190 	jr	00117$
   5CBD                     191 00113$:
                            192 ;src/entities/player.c:48: } else if (player->vx > 0) {
   5CBD AF            [ 4]  193 	xor	a, a
   5CBE 95            [ 4]  194 	sub	a, l
   5CBF E2 C4 5C      [10]  195 	jp	PO, 00223$
   5CC2 EE 80         [ 7]  196 	xor	a, #0x80
   5CC4                     197 00223$:
   5CC4 F2 D8 5C      [10]  198 	jp	P, 00110$
                            199 ;src/entities/player.c:49: player->vx = (i8)(player->vx - kplayerdeceleration);
   5CC7 7D            [ 4]  200 	ld	a, l
   5CC8 C6 FF         [ 7]  201 	add	a, #0xff
   5CCA DD 77 FF      [19]  202 	ld	-1 (ix), a
   5CCD 12            [ 7]  203 	ld	(de),a
                            204 ;src/entities/player.c:50: if (player->vx < 0) player->vx = 0;
   5CCE DD CB FF 7E   [20]  205 	bit	7, -1 (ix)
   5CD2 28 1A         [12]  206 	jr	Z,00117$
   5CD4 AF            [ 4]  207 	xor	a, a
   5CD5 12            [ 7]  208 	ld	(de), a
   5CD6 18 16         [12]  209 	jr	00117$
   5CD8                     210 00110$:
                            211 ;src/entities/player.c:51: } else if (player->vx < 0) {
   5CD8 CB 7D         [ 8]  212 	bit	7, l
   5CDA 28 12         [12]  213 	jr	Z,00117$
                            214 ;src/entities/player.c:52: player->vx = (i8)(player->vx + kplayerdeceleration);
   5CDC DD 7E FE      [19]  215 	ld	a, -2 (ix)
   5CDF 12            [ 7]  216 	ld	(de), a
                            217 ;src/entities/player.c:53: if (player->vx > 0) player->vx = 0;
   5CE0 AF            [ 4]  218 	xor	a, a
   5CE1 DD 96 FE      [19]  219 	sub	a, -2 (ix)
   5CE4 E2 E9 5C      [10]  220 	jp	PO, 00224$
   5CE7 EE 80         [ 7]  221 	xor	a, #0x80
   5CE9                     222 00224$:
   5CE9 F2 EE 5C      [10]  223 	jp	P, 00117$
   5CEC AF            [ 4]  224 	xor	a, a
   5CED 12            [ 7]  225 	ld	(de), a
   5CEE                     226 00117$:
                            227 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5CEE 1A            [ 7]  228 	ld	a, (de)
   5CEF 6F            [ 4]  229 	ld	l, a
   5CF0 3E 03         [ 7]  230 	ld	a, #0x03
   5CF2 95            [ 4]  231 	sub	a, l
   5CF3 E2 F8 5C      [10]  232 	jp	PO, 00225$
   5CF6 EE 80         [ 7]  233 	xor	a, #0x80
   5CF8                     234 00225$:
   5CF8 F2 FE 5C      [10]  235 	jp	P, 00119$
   5CFB 3E 03         [ 7]  236 	ld	a, #0x03
   5CFD 12            [ 7]  237 	ld	(de), a
   5CFE                     238 00119$:
                            239 ;src/entities/player.c:57: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5CFE 1A            [ 7]  240 	ld	a, (de)
   5CFF EE 80         [ 7]  241 	xor	a, #0x80
   5D01 D6 7D         [ 7]  242 	sub	a, #0x7d
   5D03 30 03         [12]  243 	jr	NC,00121$
   5D05 3E FD         [ 7]  244 	ld	a, #0xfd
   5D07 12            [ 7]  245 	ld	(de), a
   5D08                     246 00121$:
                            247 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5D08 C5            [11]  248 	push	bc
   5D09 D5            [11]  249 	push	de
   5D0A CD 48 52      [17]  250 	call	_input_is_jump_just_pressed
   5D0D DD 75 FE      [19]  251 	ld	-2 (ix), l
   5D10 D1            [10]  252 	pop	de
   5D11 C1            [10]  253 	pop	bc
   5D12 21 05 00      [10]  254 	ld	hl, #0x0005
   5D15 09            [11]  255 	add	hl,bc
   5D16 DD 75 F8      [19]  256 	ld	-8 (ix), l
   5D19 DD 74 F9      [19]  257 	ld	-7 (ix), h
   5D1C 21 01 00      [10]  258 	ld	hl, #0x0001
   5D1F 09            [11]  259 	add	hl,bc
   5D20 DD 75 FC      [19]  260 	ld	-4 (ix), l
   5D23 DD 74 FD      [19]  261 	ld	-3 (ix), h
                            262 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5D26 21 03 00      [10]  263 	ld	hl, #0x0003
   5D29 09            [11]  264 	add	hl,bc
   5D2A DD 75 FA      [19]  265 	ld	-6 (ix), l
   5D2D DD 74 FB      [19]  266 	ld	-5 (ix), h
                            267 ;src/entities/player.c:61: player->jump_hold = 5;
   5D30 21 09 00      [10]  268 	ld	hl, #0x0009
   5D33 09            [11]  269 	add	hl,bc
   5D34 DD 75 F6      [19]  270 	ld	-10 (ix), l
   5D37 DD 74 F7      [19]  271 	ld	-9 (ix), h
                            272 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5D3A DD 7E FE      [19]  273 	ld	a, -2 (ix)
   5D3D B7            [ 4]  274 	or	a, a
   5D3E 28 4E         [12]  275 	jr	Z,00123$
   5D40 DD 6E F8      [19]  276 	ld	l,-8 (ix)
   5D43 DD 66 F9      [19]  277 	ld	h,-7 (ix)
   5D46 7E            [ 7]  278 	ld	a, (hl)
   5D47 DD 6E FC      [19]  279 	ld	l,-4 (ix)
   5D4A DD 66 FD      [19]  280 	ld	h,-3 (ix)
   5D4D 6E            [ 7]  281 	ld	l, (hl)
   5D4E DD 75 F4      [19]  282 	ld	-12 (ix), l
   5D51 DD 36 F5 00   [19]  283 	ld	-11 (ix), #0x00
   5D55 F5            [11]  284 	push	af
   5D56 0A            [ 7]  285 	ld	a, (bc)
   5D57 6F            [ 4]  286 	ld	l, a
   5D58 F1            [10]  287 	pop	af
   5D59 DD 75 F2      [19]  288 	ld	-14 (ix), l
   5D5C DD 36 F3 00   [19]  289 	ld	-13 (ix), #0x00
   5D60 C5            [11]  290 	push	bc
   5D61 D5            [11]  291 	push	de
   5D62 F5            [11]  292 	push	af
   5D63 33            [ 6]  293 	inc	sp
   5D64 DD 6E F4      [19]  294 	ld	l,-12 (ix)
   5D67 DD 66 F5      [19]  295 	ld	h,-11 (ix)
   5D6A E5            [11]  296 	push	hl
   5D6B DD 6E F2      [19]  297 	ld	l,-14 (ix)
   5D6E DD 66 F3      [19]  298 	ld	h,-13 (ix)
   5D71 E5            [11]  299 	push	hl
   5D72 CD FB 4C      [17]  300 	call	_collision_is_on_ground_at
   5D75 F1            [10]  301 	pop	af
   5D76 F1            [10]  302 	pop	af
   5D77 33            [ 6]  303 	inc	sp
   5D78 D1            [10]  304 	pop	de
   5D79 C1            [10]  305 	pop	bc
   5D7A 7D            [ 4]  306 	ld	a, l
   5D7B B7            [ 4]  307 	or	a, a
   5D7C 28 10         [12]  308 	jr	Z,00123$
                            309 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5D7E DD 6E FA      [19]  310 	ld	l,-6 (ix)
   5D81 DD 66 FB      [19]  311 	ld	h,-5 (ix)
   5D84 36 FA         [10]  312 	ld	(hl), #0xfa
                            313 ;src/entities/player.c:61: player->jump_hold = 5;
   5D86 DD 6E F6      [19]  314 	ld	l,-10 (ix)
   5D89 DD 66 F7      [19]  315 	ld	h,-9 (ix)
   5D8C 36 05         [10]  316 	ld	(hl), #0x05
   5D8E                     317 00123$:
                            318 ;src/entities/player.c:64: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5D8E C5            [11]  319 	push	bc
   5D8F D5            [11]  320 	push	de
   5D90 CD 40 52      [17]  321 	call	_input_is_jump_pressed
   5D93 7D            [ 4]  322 	ld	a, l
   5D94 D1            [10]  323 	pop	de
   5D95 C1            [10]  324 	pop	bc
   5D96 B7            [ 4]  325 	or	a, a
   5D97 28 31         [12]  326 	jr	Z,00126$
   5D99 DD 6E F6      [19]  327 	ld	l,-10 (ix)
   5D9C DD 66 F7      [19]  328 	ld	h,-9 (ix)
   5D9F 7E            [ 7]  329 	ld	a, (hl)
   5DA0 B7            [ 4]  330 	or	a, a
   5DA1 28 27         [12]  331 	jr	Z,00126$
   5DA3 DD 6E FA      [19]  332 	ld	l,-6 (ix)
   5DA6 DD 66 FB      [19]  333 	ld	h,-5 (ix)
   5DA9 6E            [ 7]  334 	ld	l, (hl)
   5DAA CB 7D         [ 8]  335 	bit	7, l
   5DAC 28 1C         [12]  336 	jr	Z,00126$
                            337 ;src/entities/player.c:65: player->vy = (i8)(player->vy + kplayerjumpboost);
   5DAE 7D            [ 4]  338 	ld	a, l
   5DAF C6 FF         [ 7]  339 	add	a, #0xff
   5DB1 DD 6E FA      [19]  340 	ld	l,-6 (ix)
   5DB4 DD 66 FB      [19]  341 	ld	h,-5 (ix)
   5DB7 77            [ 7]  342 	ld	(hl), a
                            343 ;src/entities/player.c:66: player->jump_hold--;
   5DB8 DD 6E F6      [19]  344 	ld	l,-10 (ix)
   5DBB DD 66 F7      [19]  345 	ld	h,-9 (ix)
   5DBE 7E            [ 7]  346 	ld	a, (hl)
   5DBF C6 FF         [ 7]  347 	add	a, #0xff
   5DC1 DD 6E F6      [19]  348 	ld	l,-10 (ix)
   5DC4 DD 66 F7      [19]  349 	ld	h,-9 (ix)
   5DC7 77            [ 7]  350 	ld	(hl), a
   5DC8 18 08         [12]  351 	jr	00127$
   5DCA                     352 00126$:
                            353 ;src/entities/player.c:68: player->jump_hold = 0;
   5DCA DD 6E F6      [19]  354 	ld	l,-10 (ix)
   5DCD DD 66 F7      [19]  355 	ld	h,-9 (ix)
   5DD0 36 00         [10]  356 	ld	(hl), #0x00
   5DD2                     357 00127$:
                            358 ;src/entities/player.c:71: player->vy = (i8)(player->vy + kplayergravity);
   5DD2 DD 6E FA      [19]  359 	ld	l,-6 (ix)
   5DD5 DD 66 FB      [19]  360 	ld	h,-5 (ix)
   5DD8 7E            [ 7]  361 	ld	a, (hl)
   5DD9 3C            [ 4]  362 	inc	a
   5DDA DD 77 F2      [19]  363 	ld	-14 (ix), a
   5DDD DD 6E FA      [19]  364 	ld	l,-6 (ix)
   5DE0 DD 66 FB      [19]  365 	ld	h,-5 (ix)
   5DE3 DD 7E F2      [19]  366 	ld	a, -14 (ix)
   5DE6 77            [ 7]  367 	ld	(hl), a
                            368 ;src/entities/player.c:72: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5DE7 3E 04         [ 7]  369 	ld	a, #0x04
   5DE9 DD 96 F2      [19]  370 	sub	a, -14 (ix)
   5DEC E2 F1 5D      [10]  371 	jp	PO, 00226$
   5DEF EE 80         [ 7]  372 	xor	a, #0x80
   5DF1                     373 00226$:
   5DF1 F2 FC 5D      [10]  374 	jp	P, 00131$
   5DF4 DD 6E FA      [19]  375 	ld	l,-6 (ix)
   5DF7 DD 66 FB      [19]  376 	ld	h,-5 (ix)
   5DFA 36 04         [10]  377 	ld	(hl), #0x04
   5DFC                     378 00131$:
                            379 ;src/entities/player.c:74: nextx = (i16)player->x + (i16)player->vx;
   5DFC 0A            [ 7]  380 	ld	a, (bc)
   5DFD DD 77 F2      [19]  381 	ld	-14 (ix), a
   5E00 DD 36 F3 00   [19]  382 	ld	-13 (ix), #0x00
   5E04 1A            [ 7]  383 	ld	a, (de)
   5E05 5F            [ 4]  384 	ld	e, a
   5E06 17            [ 4]  385 	rla
   5E07 9F            [ 4]  386 	sbc	a, a
   5E08 57            [ 4]  387 	ld	d, a
   5E09 E1            [10]  388 	pop	hl
   5E0A E5            [11]  389 	push	hl
   5E0B 19            [11]  390 	add	hl, de
                            391 ;src/entities/player.c:75: if (nextx < 0) {
   5E0C CB 7C         [ 8]  392 	bit	7, h
   5E0E 28 03         [12]  393 	jr	Z,00133$
                            394 ;src/entities/player.c:76: nextx = 0;
   5E10 21 00 00      [10]  395 	ld	hl, #0x0000
   5E13                     396 00133$:
                            397 ;src/entities/player.c:78: if (nextx > 76) {
   5E13 3E 4C         [ 7]  398 	ld	a, #0x4c
   5E15 BD            [ 4]  399 	cp	a, l
   5E16 3E 00         [ 7]  400 	ld	a, #0x00
   5E18 9C            [ 4]  401 	sbc	a, h
   5E19 E2 1E 5E      [10]  402 	jp	PO, 00227$
   5E1C EE 80         [ 7]  403 	xor	a, #0x80
   5E1E                     404 00227$:
   5E1E F2 24 5E      [10]  405 	jp	P, 00135$
                            406 ;src/entities/player.c:79: nextx = 76;
   5E21 21 4C 00      [10]  407 	ld	hl, #0x004c
   5E24                     408 00135$:
                            409 ;src/entities/player.c:81: player->x = (u8)nextx;
   5E24 DD 75 F2      [19]  410 	ld	-14 (ix), l
   5E27 7D            [ 4]  411 	ld	a, l
   5E28 02            [ 7]  412 	ld	(bc), a
                            413 ;src/entities/player.c:83: nexty = (i16)player->y + (i16)player->vy;
   5E29 DD 6E FC      [19]  414 	ld	l,-4 (ix)
   5E2C DD 66 FD      [19]  415 	ld	h,-3 (ix)
   5E2F 5E            [ 7]  416 	ld	e, (hl)
   5E30 16 00         [ 7]  417 	ld	d, #0x00
   5E32 DD 6E FA      [19]  418 	ld	l,-6 (ix)
   5E35 DD 66 FB      [19]  419 	ld	h,-5 (ix)
   5E38 6E            [ 7]  420 	ld	l, (hl)
   5E39 7D            [ 4]  421 	ld	a, l
   5E3A 17            [ 4]  422 	rla
   5E3B 9F            [ 4]  423 	sbc	a, a
   5E3C 67            [ 4]  424 	ld	h, a
   5E3D 19            [11]  425 	add	hl, de
   5E3E E5            [11]  426 	push	hl
   5E3F FD E1         [14]  427 	pop	iy
                            428 ;src/entities/player.c:84: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5E41 DD 6E F8      [19]  429 	ld	l,-8 (ix)
   5E44 DD 66 F9      [19]  430 	ld	h,-7 (ix)
   5E47 66            [ 7]  431 	ld	h, (hl)
   5E48 DD 5E F2      [19]  432 	ld	e, -14 (ix)
   5E4B 16 00         [ 7]  433 	ld	d, #0x00
   5E4D C5            [11]  434 	push	bc
   5E4E E5            [11]  435 	push	hl
   5E4F 33            [ 6]  436 	inc	sp
   5E50 FD E5         [15]  437 	push	iy
   5E52 D5            [11]  438 	push	de
   5E53 CD 7A 4D      [17]  439 	call	_collision_clamp_y_at
   5E56 F1            [10]  440 	pop	af
   5E57 F1            [10]  441 	pop	af
   5E58 33            [ 6]  442 	inc	sp
   5E59 C1            [10]  443 	pop	bc
                            444 ;src/entities/player.c:85: if (nexty < 0) {
   5E5A CB 7C         [ 8]  445 	bit	7, h
   5E5C 28 03         [12]  446 	jr	Z,00137$
                            447 ;src/entities/player.c:86: nexty = 0;
   5E5E 21 00 00      [10]  448 	ld	hl, #0x0000
   5E61                     449 00137$:
                            450 ;src/entities/player.c:88: player->y = (u8)nexty;
   5E61 5D            [ 4]  451 	ld	e, l
   5E62 DD 6E FC      [19]  452 	ld	l,-4 (ix)
   5E65 DD 66 FD      [19]  453 	ld	h,-3 (ix)
   5E68 73            [ 7]  454 	ld	(hl), e
                            455 ;src/entities/player.c:90: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5E69 DD 6E F8      [19]  456 	ld	l,-8 (ix)
   5E6C DD 66 F9      [19]  457 	ld	h,-7 (ix)
   5E6F 7E            [ 7]  458 	ld	a, (hl)
   5E70 16 00         [ 7]  459 	ld	d, #0x00
   5E72 F5            [11]  460 	push	af
   5E73 0A            [ 7]  461 	ld	a, (bc)
   5E74 4F            [ 4]  462 	ld	c, a
   5E75 F1            [10]  463 	pop	af
   5E76 06 00         [ 7]  464 	ld	b, #0x00
   5E78 F5            [11]  465 	push	af
   5E79 33            [ 6]  466 	inc	sp
   5E7A D5            [11]  467 	push	de
   5E7B C5            [11]  468 	push	bc
   5E7C CD FB 4C      [17]  469 	call	_collision_is_on_ground_at
   5E7F F1            [10]  470 	pop	af
   5E80 F1            [10]  471 	pop	af
   5E81 33            [ 6]  472 	inc	sp
   5E82 7D            [ 4]  473 	ld	a, l
   5E83 B7            [ 4]  474 	or	a, a
   5E84 28 19         [12]  475 	jr	Z,00141$
   5E86 DD 6E FA      [19]  476 	ld	l,-6 (ix)
   5E89 DD 66 FB      [19]  477 	ld	h,-5 (ix)
   5E8C 4E            [ 7]  478 	ld	c, (hl)
   5E8D AF            [ 4]  479 	xor	a, a
   5E8E 91            [ 4]  480 	sub	a, c
   5E8F E2 94 5E      [10]  481 	jp	PO, 00228$
   5E92 EE 80         [ 7]  482 	xor	a, #0x80
   5E94                     483 00228$:
   5E94 F2 9F 5E      [10]  484 	jp	P, 00141$
                            485 ;src/entities/player.c:91: player->vy = 0;
   5E97 DD 6E FA      [19]  486 	ld	l,-6 (ix)
   5E9A DD 66 FB      [19]  487 	ld	h,-5 (ix)
   5E9D 36 00         [10]  488 	ld	(hl), #0x00
   5E9F                     489 00141$:
   5E9F DD F9         [10]  490 	ld	sp, ix
   5EA1 DD E1         [14]  491 	pop	ix
   5EA3 C9            [10]  492 	ret
                            493 ;src/entities/player.c:95: void playerrender(const Player* player) {
                            494 ;	---------------------------------
                            495 ; Function playerrender
                            496 ; ---------------------------------
   5EA4                     497 _playerrender::
   5EA4 DD E5         [15]  498 	push	ix
   5EA6 DD 21 00 00   [14]  499 	ld	ix,#0
   5EAA DD 39         [15]  500 	add	ix,sp
   5EAC 3B            [ 6]  501 	dec	sp
                            502 ;src/entities/player.c:98: if (!player) {
   5EAD DD 7E 05      [19]  503 	ld	a, 5 (ix)
   5EB0 DD B6 04      [19]  504 	or	a,4 (ix)
                            505 ;src/entities/player.c:99: return;
   5EB3 28 38         [12]  506 	jr	Z,00103$
                            507 ;src/entities/player.c:102: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5EB5 DD 5E 04      [19]  508 	ld	e,4 (ix)
   5EB8 DD 56 05      [19]  509 	ld	d,5 (ix)
   5EBB 6B            [ 4]  510 	ld	l, e
   5EBC 62            [ 4]  511 	ld	h, d
   5EBD 23            [ 6]  512 	inc	hl
   5EBE 46            [ 7]  513 	ld	b, (hl)
   5EBF 1A            [ 7]  514 	ld	a, (de)
   5EC0 D5            [11]  515 	push	de
   5EC1 C5            [11]  516 	push	bc
   5EC2 33            [ 6]  517 	inc	sp
   5EC3 F5            [11]  518 	push	af
   5EC4 33            [ 6]  519 	inc	sp
   5EC5 21 00 C0      [10]  520 	ld	hl, #0xc000
   5EC8 E5            [11]  521 	push	hl
   5EC9 CD BB 63      [17]  522 	call	_cpct_getScreenPtr
   5ECC 4D            [ 4]  523 	ld	c, l
   5ECD 44            [ 4]  524 	ld	b, h
   5ECE D1            [10]  525 	pop	de
                            526 ;src/entities/player.c:103: cpct_drawSprite((u8*)sprplayerknight_data, pvmem, player->w, player->h);
   5ECF D5            [11]  527 	push	de
   5ED0 FD E1         [14]  528 	pop	iy
   5ED2 FD 7E 05      [19]  529 	ld	a, 5 (iy)
   5ED5 DD 77 FF      [19]  530 	ld	-1 (ix), a
   5ED8 EB            [ 4]  531 	ex	de,hl
   5ED9 11 04 00      [10]  532 	ld	de, #0x0004
   5EDC 19            [11]  533 	add	hl, de
   5EDD 56            [ 7]  534 	ld	d, (hl)
   5EDE DD 7E FF      [19]  535 	ld	a, -1 (ix)
   5EE1 F5            [11]  536 	push	af
   5EE2 33            [ 6]  537 	inc	sp
   5EE3 D5            [11]  538 	push	de
   5EE4 33            [ 6]  539 	inc	sp
   5EE5 C5            [11]  540 	push	bc
   5EE6 21 21 55      [10]  541 	ld	hl, #_sprplayerknight_data
   5EE9 E5            [11]  542 	push	hl
   5EEA CD EC 61      [17]  543 	call	_cpct_drawSprite
   5EED                     544 00103$:
   5EED 33            [ 6]  545 	inc	sp
   5EEE DD E1         [14]  546 	pop	ix
   5EF0 C9            [10]  547 	ret
                            548 ;src/entities/player.c:106: u8 player_get_health(const Player* player) {
                            549 ;	---------------------------------
                            550 ; Function player_get_health
                            551 ; ---------------------------------
   5EF1                     552 _player_get_health::
                            553 ;src/entities/player.c:107: return player ? player->health : 0;
   5EF1 21 03 00      [10]  554 	ld	hl, #2+1
   5EF4 39            [11]  555 	add	hl, sp
   5EF5 7E            [ 7]  556 	ld	a, (hl)
   5EF6 2B            [ 6]  557 	dec	hl
   5EF7 B6            [ 7]  558 	or	a,(hl)
   5EF8 28 0A         [12]  559 	jr	Z,00103$
   5EFA C1            [10]  560 	pop	bc
   5EFB E1            [10]  561 	pop	hl
   5EFC E5            [11]  562 	push	hl
   5EFD C5            [11]  563 	push	bc
   5EFE 11 06 00      [10]  564 	ld	de, #0x0006
   5F01 19            [11]  565 	add	hl, de
   5F02 6E            [ 7]  566 	ld	l, (hl)
   5F03 C9            [10]  567 	ret
   5F04                     568 00103$:
   5F04 2E 00         [ 7]  569 	ld	l, #0x00
   5F06 C9            [10]  570 	ret
                            571 ;src/entities/player.c:110: u8 player_get_weapon(const Player* player) {
                            572 ;	---------------------------------
                            573 ; Function player_get_weapon
                            574 ; ---------------------------------
   5F07                     575 _player_get_weapon::
                            576 ;src/entities/player.c:111: return player ? player->weapon : 0;
   5F07 21 03 00      [10]  577 	ld	hl, #2+1
   5F0A 39            [11]  578 	add	hl, sp
   5F0B 7E            [ 7]  579 	ld	a, (hl)
   5F0C 2B            [ 6]  580 	dec	hl
   5F0D B6            [ 7]  581 	or	a,(hl)
   5F0E 28 0A         [12]  582 	jr	Z,00103$
   5F10 C1            [10]  583 	pop	bc
   5F11 E1            [10]  584 	pop	hl
   5F12 E5            [11]  585 	push	hl
   5F13 C5            [11]  586 	push	bc
   5F14 11 07 00      [10]  587 	ld	de, #0x0007
   5F17 19            [11]  588 	add	hl, de
   5F18 6E            [ 7]  589 	ld	l, (hl)
   5F19 C9            [10]  590 	ret
   5F1A                     591 00103$:
   5F1A 2E 00         [ 7]  592 	ld	l, #0x00
   5F1C C9            [10]  593 	ret
                            594 	.area _CODE
                            595 	.area _INITIALIZER
                            596 	.area _CABS (ABS)
