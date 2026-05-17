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
   5DBC                      59 _playerinit::
                             60 ;src/entities/player.c:28: if (!player) {
   5DBC 21 03 00      [10]   61 	ld	hl, #2+1
   5DBF 39            [11]   62 	add	hl, sp
   5DC0 7E            [ 7]   63 	ld	a, (hl)
   5DC1 2B            [ 6]   64 	dec	hl
   5DC2 B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:29: return;
   5DC3 C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:32: player->x = 20;
   5DC4 D1            [10]   69 	pop	de
   5DC5 C1            [10]   70 	pop	bc
   5DC6 C5            [11]   71 	push	bc
   5DC7 D5            [11]   72 	push	de
   5DC8 3E 14         [ 7]   73 	ld	a, #0x14
   5DCA 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:33: player->y = 120;
   5DCB 69            [ 4]   76 	ld	l, c
   5DCC 60            [ 4]   77 	ld	h, b
   5DCD 23            [ 6]   78 	inc	hl
   5DCE 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:34: player->vx = 0;
   5DD0 59            [ 4]   81 	ld	e, c
   5DD1 50            [ 4]   82 	ld	d, b
   5DD2 13            [ 6]   83 	inc	de
   5DD3 13            [ 6]   84 	inc	de
   5DD4 AF            [ 4]   85 	xor	a, a
   5DD5 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:35: player->vy = 0;
   5DD6 59            [ 4]   88 	ld	e, c
   5DD7 50            [ 4]   89 	ld	d, b
   5DD8 13            [ 6]   90 	inc	de
   5DD9 13            [ 6]   91 	inc	de
   5DDA 13            [ 6]   92 	inc	de
   5DDB AF            [ 4]   93 	xor	a, a
   5DDC 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:36: player->w = 4;
   5DDD 21 04 00      [10]   96 	ld	hl, #0x0004
   5DE0 09            [11]   97 	add	hl, bc
   5DE1 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:37: player->h = 16;
   5DE3 21 05 00      [10]  100 	ld	hl, #0x0005
   5DE6 09            [11]  101 	add	hl, bc
   5DE7 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:38: player->health = 3;
   5DE9 21 06 00      [10]  104 	ld	hl, #0x0006
   5DEC 09            [11]  105 	add	hl, bc
   5DED 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:39: player->weapon = 0;
   5DEF 21 07 00      [10]  108 	ld	hl, #0x0007
   5DF2 09            [11]  109 	add	hl, bc
   5DF3 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:40: player->facing_left = 0;
   5DF5 21 08 00      [10]  112 	ld	hl, #0x0008
   5DF8 09            [11]  113 	add	hl, bc
   5DF9 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:41: player->jump_hold = 0;
   5DFB 21 09 00      [10]  116 	ld	hl, #0x0009
   5DFE 09            [11]  117 	add	hl, bc
   5DFF 36 00         [10]  118 	ld	(hl), #0x00
   5E01 C9            [10]  119 	ret
   5E02                     120 _player_sprite:
   5E02 F0                  121 	.db #0xf0	; 240
   5E03 F0                  122 	.db #0xf0	; 240
   5E04 F0                  123 	.db #0xf0	; 240
   5E05 F0                  124 	.db #0xf0	; 240
   5E06 F0                  125 	.db #0xf0	; 240
   5E07 00                  126 	.db #0x00	; 0
   5E08 F0                  127 	.db #0xf0	; 240
   5E09 F0                  128 	.db #0xf0	; 240
   5E0A F0                  129 	.db #0xf0	; 240
   5E0B 00                  130 	.db #0x00	; 0
   5E0C F0                  131 	.db #0xf0	; 240
   5E0D F0                  132 	.db #0xf0	; 240
   5E0E F0                  133 	.db #0xf0	; 240
   5E0F 00                  134 	.db #0x00	; 0
   5E10 F0                  135 	.db #0xf0	; 240
   5E11 F0                  136 	.db #0xf0	; 240
   5E12 F0                  137 	.db #0xf0	; 240
   5E13 00                  138 	.db #0x00	; 0
   5E14 F0                  139 	.db #0xf0	; 240
   5E15 F0                  140 	.db #0xf0	; 240
   5E16 F0                  141 	.db #0xf0	; 240
   5E17 00                  142 	.db #0x00	; 0
   5E18 F0                  143 	.db #0xf0	; 240
   5E19 F0                  144 	.db #0xf0	; 240
   5E1A F0                  145 	.db #0xf0	; 240
   5E1B 00                  146 	.db #0x00	; 0
   5E1C F0                  147 	.db #0xf0	; 240
   5E1D F0                  148 	.db #0xf0	; 240
   5E1E F0                  149 	.db #0xf0	; 240
   5E1F 00                  150 	.db #0x00	; 0
   5E20 F0                  151 	.db #0xf0	; 240
   5E21 F0                  152 	.db #0xf0	; 240
   5E22 F0                  153 	.db #0xf0	; 240
   5E23 F0                  154 	.db #0xf0	; 240
   5E24 F0                  155 	.db #0xf0	; 240
   5E25 F0                  156 	.db #0xf0	; 240
   5E26 F0                  157 	.db #0xf0	; 240
   5E27 00                  158 	.db #0x00	; 0
   5E28 F0                  159 	.db #0xf0	; 240
   5E29 F0                  160 	.db #0xf0	; 240
   5E2A F0                  161 	.db #0xf0	; 240
   5E2B 00                  162 	.db #0x00	; 0
   5E2C F0                  163 	.db #0xf0	; 240
   5E2D F0                  164 	.db #0xf0	; 240
   5E2E F0                  165 	.db #0xf0	; 240
   5E2F 00                  166 	.db #0x00	; 0
   5E30 F0                  167 	.db #0xf0	; 240
   5E31 F0                  168 	.db #0xf0	; 240
   5E32 F0                  169 	.db #0xf0	; 240
   5E33 00                  170 	.db #0x00	; 0
   5E34 F0                  171 	.db #0xf0	; 240
   5E35 F0                  172 	.db #0xf0	; 240
   5E36 F0                  173 	.db #0xf0	; 240
   5E37 00                  174 	.db #0x00	; 0
   5E38 F0                  175 	.db #0xf0	; 240
   5E39 F0                  176 	.db #0xf0	; 240
   5E3A F0                  177 	.db #0xf0	; 240
   5E3B 00                  178 	.db #0x00	; 0
   5E3C F0                  179 	.db #0xf0	; 240
   5E3D F0                  180 	.db #0xf0	; 240
   5E3E F0                  181 	.db #0xf0	; 240
   5E3F F0                  182 	.db #0xf0	; 240
   5E40 F0                  183 	.db #0xf0	; 240
   5E41 F0                  184 	.db #0xf0	; 240
                            185 ;src/entities/player.c:44: void playerupdate(Player* player) {
                            186 ;	---------------------------------
                            187 ; Function playerupdate
                            188 ; ---------------------------------
   5E42                     189 _playerupdate::
   5E42 DD E5         [15]  190 	push	ix
   5E44 DD 21 00 00   [14]  191 	ld	ix,#0
   5E48 DD 39         [15]  192 	add	ix,sp
   5E4A 21 F2 FF      [10]  193 	ld	hl, #-14
   5E4D 39            [11]  194 	add	hl, sp
   5E4E F9            [ 6]  195 	ld	sp, hl
                            196 ;src/entities/player.c:48: if (!player) {
   5E4F DD 7E 05      [19]  197 	ld	a, 5 (ix)
   5E52 DD B6 04      [19]  198 	or	a,4 (ix)
                            199 ;src/entities/player.c:49: return;
   5E55 CA 89 60      [10]  200 	jp	Z,00141$
                            201 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5E58 CD 8A 52      [17]  202 	call	_input_is_left_pressed
                            203 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5E5B DD 4E 04      [19]  204 	ld	c,4 (ix)
   5E5E DD 46 05      [19]  205 	ld	b,5 (ix)
   5E61 59            [ 4]  206 	ld	e, c
   5E62 50            [ 4]  207 	ld	d, b
   5E63 13            [ 6]  208 	inc	de
   5E64 13            [ 6]  209 	inc	de
                            210 ;src/entities/player.c:54: player->facing_left = 1;
   5E65 79            [ 4]  211 	ld	a, c
   5E66 C6 08         [ 7]  212 	add	a, #0x08
   5E68 DD 77 FE      [19]  213 	ld	-2 (ix), a
   5E6B 78            [ 4]  214 	ld	a, b
   5E6C CE 00         [ 7]  215 	adc	a, #0x00
   5E6E DD 77 FF      [19]  216 	ld	-1 (ix), a
                            217 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5E71 7D            [ 4]  218 	ld	a, l
   5E72 B7            [ 4]  219 	or	a, a
   5E73 28 0E         [12]  220 	jr	Z,00116$
                            221 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5E75 1A            [ 7]  222 	ld	a, (de)
   5E76 C6 FF         [ 7]  223 	add	a, #0xff
   5E78 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/player.c:54: player->facing_left = 1;
   5E79 DD 6E FE      [19]  226 	ld	l,-2 (ix)
   5E7C DD 66 FF      [19]  227 	ld	h,-1 (ix)
   5E7F 36 01         [10]  228 	ld	(hl), #0x01
   5E81 18 55         [12]  229 	jr	00117$
   5E83                     230 00116$:
                            231 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5E83 C5            [11]  232 	push	bc
   5E84 D5            [11]  233 	push	de
   5E85 CD 92 52      [17]  234 	call	_input_is_right_pressed
   5E88 DD 75 FD      [19]  235 	ld	-3 (ix), l
   5E8B D1            [10]  236 	pop	de
   5E8C C1            [10]  237 	pop	bc
                            238 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5E8D 1A            [ 7]  239 	ld	a, (de)
                            240 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5E8E 6F            [ 4]  241 	ld	l,a
   5E8F 3C            [ 4]  242 	inc	a
   5E90 DD 77 FC      [19]  243 	ld	-4 (ix), a
                            244 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5E93 DD 7E FD      [19]  245 	ld	a, -3 (ix)
   5E96 B7            [ 4]  246 	or	a, a
   5E97 28 0E         [12]  247 	jr	Z,00113$
                            248 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5E99 DD 7E FC      [19]  249 	ld	a, -4 (ix)
   5E9C 12            [ 7]  250 	ld	(de), a
                            251 ;src/entities/player.c:57: player->facing_left = 0;
   5E9D DD 6E FE      [19]  252 	ld	l,-2 (ix)
   5EA0 DD 66 FF      [19]  253 	ld	h,-1 (ix)
   5EA3 36 00         [10]  254 	ld	(hl), #0x00
   5EA5 18 31         [12]  255 	jr	00117$
   5EA7                     256 00113$:
                            257 ;src/entities/player.c:58: } else if (player->vx > 0) {
   5EA7 AF            [ 4]  258 	xor	a, a
   5EA8 95            [ 4]  259 	sub	a, l
   5EA9 E2 AE 5E      [10]  260 	jp	PO, 00223$
   5EAC EE 80         [ 7]  261 	xor	a, #0x80
   5EAE                     262 00223$:
   5EAE F2 C2 5E      [10]  263 	jp	P, 00110$
                            264 ;src/entities/player.c:59: player->vx = (i8)(player->vx - kplayerdeceleration);
   5EB1 7D            [ 4]  265 	ld	a, l
   5EB2 C6 FF         [ 7]  266 	add	a, #0xff
   5EB4 DD 77 FD      [19]  267 	ld	-3 (ix), a
   5EB7 12            [ 7]  268 	ld	(de),a
                            269 ;src/entities/player.c:60: if (player->vx < 0) player->vx = 0;
   5EB8 DD CB FD 7E   [20]  270 	bit	7, -3 (ix)
   5EBC 28 1A         [12]  271 	jr	Z,00117$
   5EBE AF            [ 4]  272 	xor	a, a
   5EBF 12            [ 7]  273 	ld	(de), a
   5EC0 18 16         [12]  274 	jr	00117$
   5EC2                     275 00110$:
                            276 ;src/entities/player.c:61: } else if (player->vx < 0) {
   5EC2 CB 7D         [ 8]  277 	bit	7, l
   5EC4 28 12         [12]  278 	jr	Z,00117$
                            279 ;src/entities/player.c:62: player->vx = (i8)(player->vx + kplayerdeceleration);
   5EC6 DD 7E FC      [19]  280 	ld	a, -4 (ix)
   5EC9 12            [ 7]  281 	ld	(de), a
                            282 ;src/entities/player.c:63: if (player->vx > 0) player->vx = 0;
   5ECA AF            [ 4]  283 	xor	a, a
   5ECB DD 96 FC      [19]  284 	sub	a, -4 (ix)
   5ECE E2 D3 5E      [10]  285 	jp	PO, 00224$
   5ED1 EE 80         [ 7]  286 	xor	a, #0x80
   5ED3                     287 00224$:
   5ED3 F2 D8 5E      [10]  288 	jp	P, 00117$
   5ED6 AF            [ 4]  289 	xor	a, a
   5ED7 12            [ 7]  290 	ld	(de), a
   5ED8                     291 00117$:
                            292 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5ED8 1A            [ 7]  293 	ld	a, (de)
   5ED9 6F            [ 4]  294 	ld	l, a
   5EDA 3E 03         [ 7]  295 	ld	a, #0x03
   5EDC 95            [ 4]  296 	sub	a, l
   5EDD E2 E2 5E      [10]  297 	jp	PO, 00225$
   5EE0 EE 80         [ 7]  298 	xor	a, #0x80
   5EE2                     299 00225$:
   5EE2 F2 E8 5E      [10]  300 	jp	P, 00119$
   5EE5 3E 03         [ 7]  301 	ld	a, #0x03
   5EE7 12            [ 7]  302 	ld	(de), a
   5EE8                     303 00119$:
                            304 ;src/entities/player.c:67: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5EE8 1A            [ 7]  305 	ld	a, (de)
   5EE9 EE 80         [ 7]  306 	xor	a, #0x80
   5EEB D6 7D         [ 7]  307 	sub	a, #0x7d
   5EED 30 03         [12]  308 	jr	NC,00121$
   5EEF 3E FD         [ 7]  309 	ld	a, #0xfd
   5EF1 12            [ 7]  310 	ld	(de), a
   5EF2                     311 00121$:
                            312 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5EF2 C5            [11]  313 	push	bc
   5EF3 D5            [11]  314 	push	de
   5EF4 CD B2 52      [17]  315 	call	_input_is_jump_just_pressed
   5EF7 DD 75 FC      [19]  316 	ld	-4 (ix), l
   5EFA D1            [10]  317 	pop	de
   5EFB C1            [10]  318 	pop	bc
   5EFC 21 05 00      [10]  319 	ld	hl, #0x0005
   5EFF 09            [11]  320 	add	hl,bc
   5F00 DD 75 FE      [19]  321 	ld	-2 (ix), l
   5F03 DD 74 FF      [19]  322 	ld	-1 (ix), h
   5F06 21 01 00      [10]  323 	ld	hl, #0x0001
   5F09 09            [11]  324 	add	hl,bc
   5F0A DD 75 FA      [19]  325 	ld	-6 (ix), l
   5F0D DD 74 FB      [19]  326 	ld	-5 (ix), h
                            327 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   5F10 21 03 00      [10]  328 	ld	hl, #0x0003
   5F13 09            [11]  329 	add	hl,bc
   5F14 DD 75 F8      [19]  330 	ld	-8 (ix), l
   5F17 DD 74 F9      [19]  331 	ld	-7 (ix), h
                            332 ;src/entities/player.c:71: player->jump_hold = 5;
   5F1A 21 09 00      [10]  333 	ld	hl, #0x0009
   5F1D 09            [11]  334 	add	hl,bc
   5F1E DD 75 F6      [19]  335 	ld	-10 (ix), l
   5F21 DD 74 F7      [19]  336 	ld	-9 (ix), h
                            337 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5F24 DD 7E FC      [19]  338 	ld	a, -4 (ix)
   5F27 B7            [ 4]  339 	or	a, a
   5F28 28 4E         [12]  340 	jr	Z,00123$
   5F2A DD 6E FE      [19]  341 	ld	l,-2 (ix)
   5F2D DD 66 FF      [19]  342 	ld	h,-1 (ix)
   5F30 7E            [ 7]  343 	ld	a, (hl)
   5F31 DD 6E FA      [19]  344 	ld	l,-6 (ix)
   5F34 DD 66 FB      [19]  345 	ld	h,-5 (ix)
   5F37 6E            [ 7]  346 	ld	l, (hl)
   5F38 DD 75 F4      [19]  347 	ld	-12 (ix), l
   5F3B DD 36 F5 00   [19]  348 	ld	-11 (ix), #0x00
   5F3F F5            [11]  349 	push	af
   5F40 0A            [ 7]  350 	ld	a, (bc)
   5F41 6F            [ 4]  351 	ld	l, a
   5F42 F1            [10]  352 	pop	af
   5F43 DD 75 F2      [19]  353 	ld	-14 (ix), l
   5F46 DD 36 F3 00   [19]  354 	ld	-13 (ix), #0x00
   5F4A C5            [11]  355 	push	bc
   5F4B D5            [11]  356 	push	de
   5F4C F5            [11]  357 	push	af
   5F4D 33            [ 6]  358 	inc	sp
   5F4E DD 6E F4      [19]  359 	ld	l,-12 (ix)
   5F51 DD 66 F5      [19]  360 	ld	h,-11 (ix)
   5F54 E5            [11]  361 	push	hl
   5F55 DD 6E F2      [19]  362 	ld	l,-14 (ix)
   5F58 DD 66 F3      [19]  363 	ld	h,-13 (ix)
   5F5B E5            [11]  364 	push	hl
   5F5C CD C1 4B      [17]  365 	call	_collision_is_on_ground_at
   5F5F F1            [10]  366 	pop	af
   5F60 F1            [10]  367 	pop	af
   5F61 33            [ 6]  368 	inc	sp
   5F62 D1            [10]  369 	pop	de
   5F63 C1            [10]  370 	pop	bc
   5F64 7D            [ 4]  371 	ld	a, l
   5F65 B7            [ 4]  372 	or	a, a
   5F66 28 10         [12]  373 	jr	Z,00123$
                            374 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   5F68 DD 6E F8      [19]  375 	ld	l,-8 (ix)
   5F6B DD 66 F9      [19]  376 	ld	h,-7 (ix)
   5F6E 36 FA         [10]  377 	ld	(hl), #0xfa
                            378 ;src/entities/player.c:71: player->jump_hold = 5;
   5F70 DD 6E F6      [19]  379 	ld	l,-10 (ix)
   5F73 DD 66 F7      [19]  380 	ld	h,-9 (ix)
   5F76 36 05         [10]  381 	ld	(hl), #0x05
   5F78                     382 00123$:
                            383 ;src/entities/player.c:74: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5F78 C5            [11]  384 	push	bc
   5F79 D5            [11]  385 	push	de
   5F7A CD AA 52      [17]  386 	call	_input_is_jump_pressed
   5F7D 7D            [ 4]  387 	ld	a, l
   5F7E D1            [10]  388 	pop	de
   5F7F C1            [10]  389 	pop	bc
   5F80 B7            [ 4]  390 	or	a, a
   5F81 28 31         [12]  391 	jr	Z,00126$
   5F83 DD 6E F6      [19]  392 	ld	l,-10 (ix)
   5F86 DD 66 F7      [19]  393 	ld	h,-9 (ix)
   5F89 7E            [ 7]  394 	ld	a, (hl)
   5F8A B7            [ 4]  395 	or	a, a
   5F8B 28 27         [12]  396 	jr	Z,00126$
   5F8D DD 6E F8      [19]  397 	ld	l,-8 (ix)
   5F90 DD 66 F9      [19]  398 	ld	h,-7 (ix)
   5F93 6E            [ 7]  399 	ld	l, (hl)
   5F94 CB 7D         [ 8]  400 	bit	7, l
   5F96 28 1C         [12]  401 	jr	Z,00126$
                            402 ;src/entities/player.c:75: player->vy = (i8)(player->vy + kplayerjumpboost);
   5F98 7D            [ 4]  403 	ld	a, l
   5F99 C6 FF         [ 7]  404 	add	a, #0xff
   5F9B DD 6E F8      [19]  405 	ld	l,-8 (ix)
   5F9E DD 66 F9      [19]  406 	ld	h,-7 (ix)
   5FA1 77            [ 7]  407 	ld	(hl), a
                            408 ;src/entities/player.c:76: player->jump_hold--;
   5FA2 DD 6E F6      [19]  409 	ld	l,-10 (ix)
   5FA5 DD 66 F7      [19]  410 	ld	h,-9 (ix)
   5FA8 7E            [ 7]  411 	ld	a, (hl)
   5FA9 C6 FF         [ 7]  412 	add	a, #0xff
   5FAB DD 6E F6      [19]  413 	ld	l,-10 (ix)
   5FAE DD 66 F7      [19]  414 	ld	h,-9 (ix)
   5FB1 77            [ 7]  415 	ld	(hl), a
   5FB2 18 08         [12]  416 	jr	00127$
   5FB4                     417 00126$:
                            418 ;src/entities/player.c:78: player->jump_hold = 0;
   5FB4 DD 6E F6      [19]  419 	ld	l,-10 (ix)
   5FB7 DD 66 F7      [19]  420 	ld	h,-9 (ix)
   5FBA 36 00         [10]  421 	ld	(hl), #0x00
   5FBC                     422 00127$:
                            423 ;src/entities/player.c:81: player->vy = (i8)(player->vy + kplayergravity);
   5FBC DD 6E F8      [19]  424 	ld	l,-8 (ix)
   5FBF DD 66 F9      [19]  425 	ld	h,-7 (ix)
   5FC2 7E            [ 7]  426 	ld	a, (hl)
   5FC3 3C            [ 4]  427 	inc	a
   5FC4 DD 77 F2      [19]  428 	ld	-14 (ix), a
   5FC7 DD 6E F8      [19]  429 	ld	l,-8 (ix)
   5FCA DD 66 F9      [19]  430 	ld	h,-7 (ix)
   5FCD DD 7E F2      [19]  431 	ld	a, -14 (ix)
   5FD0 77            [ 7]  432 	ld	(hl), a
                            433 ;src/entities/player.c:82: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5FD1 3E 04         [ 7]  434 	ld	a, #0x04
   5FD3 DD 96 F2      [19]  435 	sub	a, -14 (ix)
   5FD6 E2 DB 5F      [10]  436 	jp	PO, 00226$
   5FD9 EE 80         [ 7]  437 	xor	a, #0x80
   5FDB                     438 00226$:
   5FDB F2 E6 5F      [10]  439 	jp	P, 00131$
   5FDE DD 6E F8      [19]  440 	ld	l,-8 (ix)
   5FE1 DD 66 F9      [19]  441 	ld	h,-7 (ix)
   5FE4 36 04         [10]  442 	ld	(hl), #0x04
   5FE6                     443 00131$:
                            444 ;src/entities/player.c:84: nextx = (i16)player->x + (i16)player->vx;
   5FE6 0A            [ 7]  445 	ld	a, (bc)
   5FE7 DD 77 F2      [19]  446 	ld	-14 (ix), a
   5FEA DD 36 F3 00   [19]  447 	ld	-13 (ix), #0x00
   5FEE 1A            [ 7]  448 	ld	a, (de)
   5FEF 5F            [ 4]  449 	ld	e, a
   5FF0 17            [ 4]  450 	rla
   5FF1 9F            [ 4]  451 	sbc	a, a
   5FF2 57            [ 4]  452 	ld	d, a
   5FF3 E1            [10]  453 	pop	hl
   5FF4 E5            [11]  454 	push	hl
   5FF5 19            [11]  455 	add	hl, de
                            456 ;src/entities/player.c:85: if (nextx < 0) {
   5FF6 CB 7C         [ 8]  457 	bit	7, h
   5FF8 28 03         [12]  458 	jr	Z,00133$
                            459 ;src/entities/player.c:86: nextx = 0;
   5FFA 21 00 00      [10]  460 	ld	hl, #0x0000
   5FFD                     461 00133$:
                            462 ;src/entities/player.c:88: if (nextx > 76) {
   5FFD 3E 4C         [ 7]  463 	ld	a, #0x4c
   5FFF BD            [ 4]  464 	cp	a, l
   6000 3E 00         [ 7]  465 	ld	a, #0x00
   6002 9C            [ 4]  466 	sbc	a, h
   6003 E2 08 60      [10]  467 	jp	PO, 00227$
   6006 EE 80         [ 7]  468 	xor	a, #0x80
   6008                     469 00227$:
   6008 F2 0E 60      [10]  470 	jp	P, 00135$
                            471 ;src/entities/player.c:89: nextx = 76;
   600B 21 4C 00      [10]  472 	ld	hl, #0x004c
   600E                     473 00135$:
                            474 ;src/entities/player.c:91: player->x = (u8)nextx;
   600E DD 75 F2      [19]  475 	ld	-14 (ix), l
   6011 7D            [ 4]  476 	ld	a, l
   6012 02            [ 7]  477 	ld	(bc), a
                            478 ;src/entities/player.c:93: nexty = (i16)player->y + (i16)player->vy;
   6013 DD 6E FA      [19]  479 	ld	l,-6 (ix)
   6016 DD 66 FB      [19]  480 	ld	h,-5 (ix)
   6019 5E            [ 7]  481 	ld	e, (hl)
   601A 16 00         [ 7]  482 	ld	d, #0x00
   601C DD 6E F8      [19]  483 	ld	l,-8 (ix)
   601F DD 66 F9      [19]  484 	ld	h,-7 (ix)
   6022 6E            [ 7]  485 	ld	l, (hl)
   6023 7D            [ 4]  486 	ld	a, l
   6024 17            [ 4]  487 	rla
   6025 9F            [ 4]  488 	sbc	a, a
   6026 67            [ 4]  489 	ld	h, a
   6027 19            [11]  490 	add	hl, de
   6028 E5            [11]  491 	push	hl
   6029 FD E1         [14]  492 	pop	iy
                            493 ;src/entities/player.c:94: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   602B DD 6E FE      [19]  494 	ld	l,-2 (ix)
   602E DD 66 FF      [19]  495 	ld	h,-1 (ix)
   6031 66            [ 7]  496 	ld	h, (hl)
   6032 DD 5E F2      [19]  497 	ld	e, -14 (ix)
   6035 16 00         [ 7]  498 	ld	d, #0x00
   6037 C5            [11]  499 	push	bc
   6038 E5            [11]  500 	push	hl
   6039 33            [ 6]  501 	inc	sp
   603A FD E5         [15]  502 	push	iy
   603C D5            [11]  503 	push	de
   603D CD 40 4C      [17]  504 	call	_collision_clamp_y_at
   6040 F1            [10]  505 	pop	af
   6041 F1            [10]  506 	pop	af
   6042 33            [ 6]  507 	inc	sp
   6043 C1            [10]  508 	pop	bc
                            509 ;src/entities/player.c:95: if (nexty < 0) {
   6044 CB 7C         [ 8]  510 	bit	7, h
   6046 28 03         [12]  511 	jr	Z,00137$
                            512 ;src/entities/player.c:96: nexty = 0;
   6048 21 00 00      [10]  513 	ld	hl, #0x0000
   604B                     514 00137$:
                            515 ;src/entities/player.c:98: player->y = (u8)nexty;
   604B 5D            [ 4]  516 	ld	e, l
   604C DD 6E FA      [19]  517 	ld	l,-6 (ix)
   604F DD 66 FB      [19]  518 	ld	h,-5 (ix)
   6052 73            [ 7]  519 	ld	(hl), e
                            520 ;src/entities/player.c:100: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   6053 DD 6E FE      [19]  521 	ld	l,-2 (ix)
   6056 DD 66 FF      [19]  522 	ld	h,-1 (ix)
   6059 7E            [ 7]  523 	ld	a, (hl)
   605A 16 00         [ 7]  524 	ld	d, #0x00
   605C F5            [11]  525 	push	af
   605D 0A            [ 7]  526 	ld	a, (bc)
   605E 4F            [ 4]  527 	ld	c, a
   605F F1            [10]  528 	pop	af
   6060 06 00         [ 7]  529 	ld	b, #0x00
   6062 F5            [11]  530 	push	af
   6063 33            [ 6]  531 	inc	sp
   6064 D5            [11]  532 	push	de
   6065 C5            [11]  533 	push	bc
   6066 CD C1 4B      [17]  534 	call	_collision_is_on_ground_at
   6069 F1            [10]  535 	pop	af
   606A F1            [10]  536 	pop	af
   606B 33            [ 6]  537 	inc	sp
   606C 7D            [ 4]  538 	ld	a, l
   606D B7            [ 4]  539 	or	a, a
   606E 28 19         [12]  540 	jr	Z,00141$
   6070 DD 6E F8      [19]  541 	ld	l,-8 (ix)
   6073 DD 66 F9      [19]  542 	ld	h,-7 (ix)
   6076 4E            [ 7]  543 	ld	c, (hl)
   6077 AF            [ 4]  544 	xor	a, a
   6078 91            [ 4]  545 	sub	a, c
   6079 E2 7E 60      [10]  546 	jp	PO, 00228$
   607C EE 80         [ 7]  547 	xor	a, #0x80
   607E                     548 00228$:
   607E F2 89 60      [10]  549 	jp	P, 00141$
                            550 ;src/entities/player.c:101: player->vy = 0;
   6081 DD 6E F8      [19]  551 	ld	l,-8 (ix)
   6084 DD 66 F9      [19]  552 	ld	h,-7 (ix)
   6087 36 00         [10]  553 	ld	(hl), #0x00
   6089                     554 00141$:
   6089 DD F9         [10]  555 	ld	sp, ix
   608B DD E1         [14]  556 	pop	ix
   608D C9            [10]  557 	ret
                            558 ;src/entities/player.c:105: void playerrender(const Player* player) {
                            559 ;	---------------------------------
                            560 ; Function playerrender
                            561 ; ---------------------------------
   608E                     562 _playerrender::
   608E DD E5         [15]  563 	push	ix
   6090 DD 21 00 00   [14]  564 	ld	ix,#0
   6094 DD 39         [15]  565 	add	ix,sp
   6096 3B            [ 6]  566 	dec	sp
                            567 ;src/entities/player.c:108: if (!player) {
   6097 DD 7E 05      [19]  568 	ld	a, 5 (ix)
   609A DD B6 04      [19]  569 	or	a,4 (ix)
                            570 ;src/entities/player.c:109: return;
   609D 28 38         [12]  571 	jr	Z,00103$
                            572 ;src/entities/player.c:112: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   609F DD 5E 04      [19]  573 	ld	e,4 (ix)
   60A2 DD 56 05      [19]  574 	ld	d,5 (ix)
   60A5 6B            [ 4]  575 	ld	l, e
   60A6 62            [ 4]  576 	ld	h, d
   60A7 23            [ 6]  577 	inc	hl
   60A8 46            [ 7]  578 	ld	b, (hl)
   60A9 1A            [ 7]  579 	ld	a, (de)
   60AA D5            [11]  580 	push	de
   60AB C5            [11]  581 	push	bc
   60AC 33            [ 6]  582 	inc	sp
   60AD F5            [11]  583 	push	af
   60AE 33            [ 6]  584 	inc	sp
   60AF 21 00 C0      [10]  585 	ld	hl, #0xc000
   60B2 E5            [11]  586 	push	hl
   60B3 CD A5 65      [17]  587 	call	_cpct_getScreenPtr
   60B6 4D            [ 4]  588 	ld	c, l
   60B7 44            [ 4]  589 	ld	b, h
   60B8 D1            [10]  590 	pop	de
                            591 ;src/entities/player.c:113: cpct_drawSprite((u8*)player_sprite, pvmem, player->w, player->h);
   60B9 D5            [11]  592 	push	de
   60BA FD E1         [14]  593 	pop	iy
   60BC FD 7E 05      [19]  594 	ld	a, 5 (iy)
   60BF DD 77 FF      [19]  595 	ld	-1 (ix), a
   60C2 EB            [ 4]  596 	ex	de,hl
   60C3 11 04 00      [10]  597 	ld	de, #0x0004
   60C6 19            [11]  598 	add	hl, de
   60C7 56            [ 7]  599 	ld	d, (hl)
   60C8 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   60CB F5            [11]  601 	push	af
   60CC 33            [ 6]  602 	inc	sp
   60CD D5            [11]  603 	push	de
   60CE 33            [ 6]  604 	inc	sp
   60CF C5            [11]  605 	push	bc
   60D0 21 02 5E      [10]  606 	ld	hl, #_player_sprite
   60D3 E5            [11]  607 	push	hl
   60D4 CD D6 63      [17]  608 	call	_cpct_drawSprite
   60D7                     609 00103$:
   60D7 33            [ 6]  610 	inc	sp
   60D8 DD E1         [14]  611 	pop	ix
   60DA C9            [10]  612 	ret
                            613 ;src/entities/player.c:116: u8 player_get_health(const Player* player) {
                            614 ;	---------------------------------
                            615 ; Function player_get_health
                            616 ; ---------------------------------
   60DB                     617 _player_get_health::
                            618 ;src/entities/player.c:117: return player ? player->health : 0;
   60DB 21 03 00      [10]  619 	ld	hl, #2+1
   60DE 39            [11]  620 	add	hl, sp
   60DF 7E            [ 7]  621 	ld	a, (hl)
   60E0 2B            [ 6]  622 	dec	hl
   60E1 B6            [ 7]  623 	or	a,(hl)
   60E2 28 0A         [12]  624 	jr	Z,00103$
   60E4 C1            [10]  625 	pop	bc
   60E5 E1            [10]  626 	pop	hl
   60E6 E5            [11]  627 	push	hl
   60E7 C5            [11]  628 	push	bc
   60E8 11 06 00      [10]  629 	ld	de, #0x0006
   60EB 19            [11]  630 	add	hl, de
   60EC 6E            [ 7]  631 	ld	l, (hl)
   60ED C9            [10]  632 	ret
   60EE                     633 00103$:
   60EE 2E 00         [ 7]  634 	ld	l, #0x00
   60F0 C9            [10]  635 	ret
                            636 ;src/entities/player.c:120: u8 player_get_weapon(const Player* player) {
                            637 ;	---------------------------------
                            638 ; Function player_get_weapon
                            639 ; ---------------------------------
   60F1                     640 _player_get_weapon::
                            641 ;src/entities/player.c:121: return player ? player->weapon : 0;
   60F1 21 03 00      [10]  642 	ld	hl, #2+1
   60F4 39            [11]  643 	add	hl, sp
   60F5 7E            [ 7]  644 	ld	a, (hl)
   60F6 2B            [ 6]  645 	dec	hl
   60F7 B6            [ 7]  646 	or	a,(hl)
   60F8 28 0A         [12]  647 	jr	Z,00103$
   60FA C1            [10]  648 	pop	bc
   60FB E1            [10]  649 	pop	hl
   60FC E5            [11]  650 	push	hl
   60FD C5            [11]  651 	push	bc
   60FE 11 07 00      [10]  652 	ld	de, #0x0007
   6101 19            [11]  653 	add	hl, de
   6102 6E            [ 7]  654 	ld	l, (hl)
   6103 C9            [10]  655 	ret
   6104                     656 00103$:
   6104 2E 00         [ 7]  657 	ld	l, #0x00
   6106 C9            [10]  658 	ret
                            659 	.area _CODE
                            660 	.area _INITIALIZER
                            661 	.area _CABS (ABS)
