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
                             22 	.globl _player_get_ammo
                             23 	.globl _player_get_health
                             24 	.globl _player_get_weapon
                             25 ;--------------------------------------------------------
                             26 ; special function registers
                             27 ;--------------------------------------------------------
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _DATA
                             32 ;--------------------------------------------------------
                             33 ; ram data
                             34 ;--------------------------------------------------------
                             35 	.area _INITIALIZED
                             36 ;--------------------------------------------------------
                             37 ; absolute external ram data
                             38 ;--------------------------------------------------------
                             39 	.area _DABS (ABS)
                             40 ;--------------------------------------------------------
                             41 ; global & static initialisations
                             42 ;--------------------------------------------------------
                             43 	.area _HOME
                             44 	.area _GSINIT
                             45 	.area _GSFINAL
                             46 	.area _GSINIT
                             47 ;--------------------------------------------------------
                             48 ; Home
                             49 ;--------------------------------------------------------
                             50 	.area _HOME
                             51 	.area _HOME
                             52 ;--------------------------------------------------------
                             53 ; code
                             54 ;--------------------------------------------------------
                             55 	.area _CODE
                             56 ;src/entities/player.c:17: void playerinit(Player* player) {
                             57 ;	---------------------------------
                             58 ; Function playerinit
                             59 ; ---------------------------------
   5C8D                      60 _playerinit::
                             61 ;src/entities/player.c:18: if (!player) {
   5C8D 21 03 00      [10]   62 	ld	hl, #2+1
   5C90 39            [11]   63 	add	hl, sp
   5C91 7E            [ 7]   64 	ld	a, (hl)
   5C92 2B            [ 6]   65 	dec	hl
   5C93 B6            [ 7]   66 	or	a,(hl)
                             67 ;src/entities/player.c:19: return;
   5C94 C8            [11]   68 	ret	Z
                             69 ;src/entities/player.c:22: player->x = 20;
   5C95 D1            [10]   70 	pop	de
   5C96 C1            [10]   71 	pop	bc
   5C97 C5            [11]   72 	push	bc
   5C98 D5            [11]   73 	push	de
   5C99 3E 14         [ 7]   74 	ld	a, #0x14
   5C9B 02            [ 7]   75 	ld	(bc), a
                             76 ;src/entities/player.c:23: player->y = 120;
   5C9C 69            [ 4]   77 	ld	l, c
   5C9D 60            [ 4]   78 	ld	h, b
   5C9E 23            [ 6]   79 	inc	hl
   5C9F 36 78         [10]   80 	ld	(hl), #0x78
                             81 ;src/entities/player.c:24: player->vx = 0;
   5CA1 59            [ 4]   82 	ld	e, c
   5CA2 50            [ 4]   83 	ld	d, b
   5CA3 13            [ 6]   84 	inc	de
   5CA4 13            [ 6]   85 	inc	de
   5CA5 AF            [ 4]   86 	xor	a, a
   5CA6 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/player.c:25: player->vy = 0;
   5CA7 59            [ 4]   89 	ld	e, c
   5CA8 50            [ 4]   90 	ld	d, b
   5CA9 13            [ 6]   91 	inc	de
   5CAA 13            [ 6]   92 	inc	de
   5CAB 13            [ 6]   93 	inc	de
   5CAC AF            [ 4]   94 	xor	a, a
   5CAD 12            [ 7]   95 	ld	(de), a
                             96 ;src/entities/player.c:26: player->w = 4;
   5CAE 21 04 00      [10]   97 	ld	hl, #0x0004
   5CB1 09            [11]   98 	add	hl, bc
   5CB2 36 04         [10]   99 	ld	(hl), #0x04
                            100 ;src/entities/player.c:27: player->h = 16;
   5CB4 21 05 00      [10]  101 	ld	hl, #0x0005
   5CB7 09            [11]  102 	add	hl, bc
   5CB8 36 10         [10]  103 	ld	(hl), #0x10
                            104 ;src/entities/player.c:28: player->health = 3;
   5CBA 21 06 00      [10]  105 	ld	hl, #0x0006
   5CBD 09            [11]  106 	add	hl, bc
   5CBE 36 03         [10]  107 	ld	(hl), #0x03
                            108 ;src/entities/player.c:29: player->weapon = 0;
   5CC0 21 07 00      [10]  109 	ld	hl, #0x0007
   5CC3 09            [11]  110 	add	hl, bc
   5CC4 36 00         [10]  111 	ld	(hl), #0x00
                            112 ;src/entities/player.c:30: player->facing_left = 0;
   5CC6 21 08 00      [10]  113 	ld	hl, #0x0008
   5CC9 09            [11]  114 	add	hl, bc
   5CCA 36 00         [10]  115 	ld	(hl), #0x00
                            116 ;src/entities/player.c:31: player->jump_hold = 0;
   5CCC 21 09 00      [10]  117 	ld	hl, #0x0009
   5CCF 09            [11]  118 	add	hl, bc
   5CD0 36 00         [10]  119 	ld	(hl), #0x00
   5CD2 C9            [10]  120 	ret
                            121 ;src/entities/player.c:34: void playerupdate(Player* player) {
                            122 ;	---------------------------------
                            123 ; Function playerupdate
                            124 ; ---------------------------------
   5CD3                     125 _playerupdate::
   5CD3 DD E5         [15]  126 	push	ix
   5CD5 DD 21 00 00   [14]  127 	ld	ix,#0
   5CD9 DD 39         [15]  128 	add	ix,sp
   5CDB 21 F2 FF      [10]  129 	ld	hl, #-14
   5CDE 39            [11]  130 	add	hl, sp
   5CDF F9            [ 6]  131 	ld	sp, hl
                            132 ;src/entities/player.c:38: if (!player) {
   5CE0 DD 7E 05      [19]  133 	ld	a, 5 (ix)
   5CE3 DD B6 04      [19]  134 	or	a,4 (ix)
                            135 ;src/entities/player.c:39: return;
   5CE6 CA 1A 5F      [10]  136 	jp	Z,00141$
                            137 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5CE9 CD 9B 52      [17]  138 	call	_input_is_left_pressed
                            139 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5CEC DD 4E 04      [19]  140 	ld	c,4 (ix)
   5CEF DD 46 05      [19]  141 	ld	b,5 (ix)
   5CF2 59            [ 4]  142 	ld	e, c
   5CF3 50            [ 4]  143 	ld	d, b
   5CF4 13            [ 6]  144 	inc	de
   5CF5 13            [ 6]  145 	inc	de
                            146 ;src/entities/player.c:44: player->facing_left = 1;
   5CF6 79            [ 4]  147 	ld	a, c
   5CF7 C6 08         [ 7]  148 	add	a, #0x08
   5CF9 DD 77 FE      [19]  149 	ld	-2 (ix), a
   5CFC 78            [ 4]  150 	ld	a, b
   5CFD CE 00         [ 7]  151 	adc	a, #0x00
   5CFF DD 77 FF      [19]  152 	ld	-1 (ix), a
                            153 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5D02 7D            [ 4]  154 	ld	a, l
   5D03 B7            [ 4]  155 	or	a, a
   5D04 28 0E         [12]  156 	jr	Z,00116$
                            157 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5D06 1A            [ 7]  158 	ld	a, (de)
   5D07 C6 FF         [ 7]  159 	add	a, #0xff
   5D09 12            [ 7]  160 	ld	(de), a
                            161 ;src/entities/player.c:44: player->facing_left = 1;
   5D0A DD 6E FE      [19]  162 	ld	l,-2 (ix)
   5D0D DD 66 FF      [19]  163 	ld	h,-1 (ix)
   5D10 36 01         [10]  164 	ld	(hl), #0x01
   5D12 18 55         [12]  165 	jr	00117$
   5D14                     166 00116$:
                            167 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5D14 C5            [11]  168 	push	bc
   5D15 D5            [11]  169 	push	de
   5D16 CD A3 52      [17]  170 	call	_input_is_right_pressed
   5D19 DD 75 FD      [19]  171 	ld	-3 (ix), l
   5D1C D1            [10]  172 	pop	de
   5D1D C1            [10]  173 	pop	bc
                            174 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5D1E 1A            [ 7]  175 	ld	a, (de)
                            176 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5D1F 6F            [ 4]  177 	ld	l,a
   5D20 3C            [ 4]  178 	inc	a
   5D21 DD 77 FC      [19]  179 	ld	-4 (ix), a
                            180 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5D24 DD 7E FD      [19]  181 	ld	a, -3 (ix)
   5D27 B7            [ 4]  182 	or	a, a
   5D28 28 0E         [12]  183 	jr	Z,00113$
                            184 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5D2A DD 7E FC      [19]  185 	ld	a, -4 (ix)
   5D2D 12            [ 7]  186 	ld	(de), a
                            187 ;src/entities/player.c:47: player->facing_left = 0;
   5D2E DD 6E FE      [19]  188 	ld	l,-2 (ix)
   5D31 DD 66 FF      [19]  189 	ld	h,-1 (ix)
   5D34 36 00         [10]  190 	ld	(hl), #0x00
   5D36 18 31         [12]  191 	jr	00117$
   5D38                     192 00113$:
                            193 ;src/entities/player.c:48: } else if (player->vx > 0) {
   5D38 AF            [ 4]  194 	xor	a, a
   5D39 95            [ 4]  195 	sub	a, l
   5D3A E2 3F 5D      [10]  196 	jp	PO, 00223$
   5D3D EE 80         [ 7]  197 	xor	a, #0x80
   5D3F                     198 00223$:
   5D3F F2 53 5D      [10]  199 	jp	P, 00110$
                            200 ;src/entities/player.c:49: player->vx = (i8)(player->vx - kplayerdeceleration);
   5D42 7D            [ 4]  201 	ld	a, l
   5D43 C6 FF         [ 7]  202 	add	a, #0xff
   5D45 DD 77 FD      [19]  203 	ld	-3 (ix), a
   5D48 12            [ 7]  204 	ld	(de),a
                            205 ;src/entities/player.c:50: if (player->vx < 0) player->vx = 0;
   5D49 DD CB FD 7E   [20]  206 	bit	7, -3 (ix)
   5D4D 28 1A         [12]  207 	jr	Z,00117$
   5D4F AF            [ 4]  208 	xor	a, a
   5D50 12            [ 7]  209 	ld	(de), a
   5D51 18 16         [12]  210 	jr	00117$
   5D53                     211 00110$:
                            212 ;src/entities/player.c:51: } else if (player->vx < 0) {
   5D53 CB 7D         [ 8]  213 	bit	7, l
   5D55 28 12         [12]  214 	jr	Z,00117$
                            215 ;src/entities/player.c:52: player->vx = (i8)(player->vx + kplayerdeceleration);
   5D57 DD 7E FC      [19]  216 	ld	a, -4 (ix)
   5D5A 12            [ 7]  217 	ld	(de), a
                            218 ;src/entities/player.c:53: if (player->vx > 0) player->vx = 0;
   5D5B AF            [ 4]  219 	xor	a, a
   5D5C DD 96 FC      [19]  220 	sub	a, -4 (ix)
   5D5F E2 64 5D      [10]  221 	jp	PO, 00224$
   5D62 EE 80         [ 7]  222 	xor	a, #0x80
   5D64                     223 00224$:
   5D64 F2 69 5D      [10]  224 	jp	P, 00117$
   5D67 AF            [ 4]  225 	xor	a, a
   5D68 12            [ 7]  226 	ld	(de), a
   5D69                     227 00117$:
                            228 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5D69 1A            [ 7]  229 	ld	a, (de)
   5D6A 6F            [ 4]  230 	ld	l, a
   5D6B 3E 03         [ 7]  231 	ld	a, #0x03
   5D6D 95            [ 4]  232 	sub	a, l
   5D6E E2 73 5D      [10]  233 	jp	PO, 00225$
   5D71 EE 80         [ 7]  234 	xor	a, #0x80
   5D73                     235 00225$:
   5D73 F2 79 5D      [10]  236 	jp	P, 00119$
   5D76 3E 03         [ 7]  237 	ld	a, #0x03
   5D78 12            [ 7]  238 	ld	(de), a
   5D79                     239 00119$:
                            240 ;src/entities/player.c:57: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5D79 1A            [ 7]  241 	ld	a, (de)
   5D7A EE 80         [ 7]  242 	xor	a, #0x80
   5D7C D6 7D         [ 7]  243 	sub	a, #0x7d
   5D7E 30 03         [12]  244 	jr	NC,00121$
   5D80 3E FD         [ 7]  245 	ld	a, #0xfd
   5D82 12            [ 7]  246 	ld	(de), a
   5D83                     247 00121$:
                            248 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5D83 C5            [11]  249 	push	bc
   5D84 D5            [11]  250 	push	de
   5D85 CD C3 52      [17]  251 	call	_input_is_jump_just_pressed
   5D88 DD 75 FC      [19]  252 	ld	-4 (ix), l
   5D8B D1            [10]  253 	pop	de
   5D8C C1            [10]  254 	pop	bc
   5D8D 21 05 00      [10]  255 	ld	hl, #0x0005
   5D90 09            [11]  256 	add	hl,bc
   5D91 DD 75 FE      [19]  257 	ld	-2 (ix), l
   5D94 DD 74 FF      [19]  258 	ld	-1 (ix), h
   5D97 21 01 00      [10]  259 	ld	hl, #0x0001
   5D9A 09            [11]  260 	add	hl,bc
   5D9B DD 75 FA      [19]  261 	ld	-6 (ix), l
   5D9E DD 74 FB      [19]  262 	ld	-5 (ix), h
                            263 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5DA1 21 03 00      [10]  264 	ld	hl, #0x0003
   5DA4 09            [11]  265 	add	hl,bc
   5DA5 DD 75 F8      [19]  266 	ld	-8 (ix), l
   5DA8 DD 74 F9      [19]  267 	ld	-7 (ix), h
                            268 ;src/entities/player.c:61: player->jump_hold = 5;
   5DAB 21 09 00      [10]  269 	ld	hl, #0x0009
   5DAE 09            [11]  270 	add	hl,bc
   5DAF DD 75 F6      [19]  271 	ld	-10 (ix), l
   5DB2 DD 74 F7      [19]  272 	ld	-9 (ix), h
                            273 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5DB5 DD 7E FC      [19]  274 	ld	a, -4 (ix)
   5DB8 B7            [ 4]  275 	or	a, a
   5DB9 28 4E         [12]  276 	jr	Z,00123$
   5DBB DD 6E FE      [19]  277 	ld	l,-2 (ix)
   5DBE DD 66 FF      [19]  278 	ld	h,-1 (ix)
   5DC1 7E            [ 7]  279 	ld	a, (hl)
   5DC2 DD 6E FA      [19]  280 	ld	l,-6 (ix)
   5DC5 DD 66 FB      [19]  281 	ld	h,-5 (ix)
   5DC8 6E            [ 7]  282 	ld	l, (hl)
   5DC9 DD 75 F4      [19]  283 	ld	-12 (ix), l
   5DCC DD 36 F5 00   [19]  284 	ld	-11 (ix), #0x00
   5DD0 F5            [11]  285 	push	af
   5DD1 0A            [ 7]  286 	ld	a, (bc)
   5DD2 6F            [ 4]  287 	ld	l, a
   5DD3 F1            [10]  288 	pop	af
   5DD4 DD 75 F2      [19]  289 	ld	-14 (ix), l
   5DD7 DD 36 F3 00   [19]  290 	ld	-13 (ix), #0x00
   5DDB C5            [11]  291 	push	bc
   5DDC D5            [11]  292 	push	de
   5DDD F5            [11]  293 	push	af
   5DDE 33            [ 6]  294 	inc	sp
   5DDF DD 6E F4      [19]  295 	ld	l,-12 (ix)
   5DE2 DD 66 F5      [19]  296 	ld	h,-11 (ix)
   5DE5 E5            [11]  297 	push	hl
   5DE6 DD 6E F2      [19]  298 	ld	l,-14 (ix)
   5DE9 DD 66 F3      [19]  299 	ld	h,-13 (ix)
   5DEC E5            [11]  300 	push	hl
   5DED CD 08 4D      [17]  301 	call	_collision_is_on_ground_at
   5DF0 F1            [10]  302 	pop	af
   5DF1 F1            [10]  303 	pop	af
   5DF2 33            [ 6]  304 	inc	sp
   5DF3 D1            [10]  305 	pop	de
   5DF4 C1            [10]  306 	pop	bc
   5DF5 7D            [ 4]  307 	ld	a, l
   5DF6 B7            [ 4]  308 	or	a, a
   5DF7 28 10         [12]  309 	jr	Z,00123$
                            310 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5DF9 DD 6E F8      [19]  311 	ld	l,-8 (ix)
   5DFC DD 66 F9      [19]  312 	ld	h,-7 (ix)
   5DFF 36 FA         [10]  313 	ld	(hl), #0xfa
                            314 ;src/entities/player.c:61: player->jump_hold = 5;
   5E01 DD 6E F6      [19]  315 	ld	l,-10 (ix)
   5E04 DD 66 F7      [19]  316 	ld	h,-9 (ix)
   5E07 36 05         [10]  317 	ld	(hl), #0x05
   5E09                     318 00123$:
                            319 ;src/entities/player.c:64: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5E09 C5            [11]  320 	push	bc
   5E0A D5            [11]  321 	push	de
   5E0B CD BB 52      [17]  322 	call	_input_is_jump_pressed
   5E0E 7D            [ 4]  323 	ld	a, l
   5E0F D1            [10]  324 	pop	de
   5E10 C1            [10]  325 	pop	bc
   5E11 B7            [ 4]  326 	or	a, a
   5E12 28 31         [12]  327 	jr	Z,00126$
   5E14 DD 6E F6      [19]  328 	ld	l,-10 (ix)
   5E17 DD 66 F7      [19]  329 	ld	h,-9 (ix)
   5E1A 7E            [ 7]  330 	ld	a, (hl)
   5E1B B7            [ 4]  331 	or	a, a
   5E1C 28 27         [12]  332 	jr	Z,00126$
   5E1E DD 6E F8      [19]  333 	ld	l,-8 (ix)
   5E21 DD 66 F9      [19]  334 	ld	h,-7 (ix)
   5E24 6E            [ 7]  335 	ld	l, (hl)
   5E25 CB 7D         [ 8]  336 	bit	7, l
   5E27 28 1C         [12]  337 	jr	Z,00126$
                            338 ;src/entities/player.c:65: player->vy = (i8)(player->vy + kplayerjumpboost);
   5E29 7D            [ 4]  339 	ld	a, l
   5E2A C6 FF         [ 7]  340 	add	a, #0xff
   5E2C DD 6E F8      [19]  341 	ld	l,-8 (ix)
   5E2F DD 66 F9      [19]  342 	ld	h,-7 (ix)
   5E32 77            [ 7]  343 	ld	(hl), a
                            344 ;src/entities/player.c:66: player->jump_hold--;
   5E33 DD 6E F6      [19]  345 	ld	l,-10 (ix)
   5E36 DD 66 F7      [19]  346 	ld	h,-9 (ix)
   5E39 7E            [ 7]  347 	ld	a, (hl)
   5E3A C6 FF         [ 7]  348 	add	a, #0xff
   5E3C DD 6E F6      [19]  349 	ld	l,-10 (ix)
   5E3F DD 66 F7      [19]  350 	ld	h,-9 (ix)
   5E42 77            [ 7]  351 	ld	(hl), a
   5E43 18 08         [12]  352 	jr	00127$
   5E45                     353 00126$:
                            354 ;src/entities/player.c:68: player->jump_hold = 0;
   5E45 DD 6E F6      [19]  355 	ld	l,-10 (ix)
   5E48 DD 66 F7      [19]  356 	ld	h,-9 (ix)
   5E4B 36 00         [10]  357 	ld	(hl), #0x00
   5E4D                     358 00127$:
                            359 ;src/entities/player.c:71: player->vy = (i8)(player->vy + kplayergravity);
   5E4D DD 6E F8      [19]  360 	ld	l,-8 (ix)
   5E50 DD 66 F9      [19]  361 	ld	h,-7 (ix)
   5E53 7E            [ 7]  362 	ld	a, (hl)
   5E54 3C            [ 4]  363 	inc	a
   5E55 DD 77 F2      [19]  364 	ld	-14 (ix), a
   5E58 DD 6E F8      [19]  365 	ld	l,-8 (ix)
   5E5B DD 66 F9      [19]  366 	ld	h,-7 (ix)
   5E5E DD 7E F2      [19]  367 	ld	a, -14 (ix)
   5E61 77            [ 7]  368 	ld	(hl), a
                            369 ;src/entities/player.c:72: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5E62 3E 04         [ 7]  370 	ld	a, #0x04
   5E64 DD 96 F2      [19]  371 	sub	a, -14 (ix)
   5E67 E2 6C 5E      [10]  372 	jp	PO, 00226$
   5E6A EE 80         [ 7]  373 	xor	a, #0x80
   5E6C                     374 00226$:
   5E6C F2 77 5E      [10]  375 	jp	P, 00131$
   5E6F DD 6E F8      [19]  376 	ld	l,-8 (ix)
   5E72 DD 66 F9      [19]  377 	ld	h,-7 (ix)
   5E75 36 04         [10]  378 	ld	(hl), #0x04
   5E77                     379 00131$:
                            380 ;src/entities/player.c:74: nextx = (i16)player->x + (i16)player->vx;
   5E77 0A            [ 7]  381 	ld	a, (bc)
   5E78 DD 77 F2      [19]  382 	ld	-14 (ix), a
   5E7B DD 36 F3 00   [19]  383 	ld	-13 (ix), #0x00
   5E7F 1A            [ 7]  384 	ld	a, (de)
   5E80 5F            [ 4]  385 	ld	e, a
   5E81 17            [ 4]  386 	rla
   5E82 9F            [ 4]  387 	sbc	a, a
   5E83 57            [ 4]  388 	ld	d, a
   5E84 E1            [10]  389 	pop	hl
   5E85 E5            [11]  390 	push	hl
   5E86 19            [11]  391 	add	hl, de
                            392 ;src/entities/player.c:75: if (nextx < 0) {
   5E87 CB 7C         [ 8]  393 	bit	7, h
   5E89 28 03         [12]  394 	jr	Z,00133$
                            395 ;src/entities/player.c:76: nextx = 0;
   5E8B 21 00 00      [10]  396 	ld	hl, #0x0000
   5E8E                     397 00133$:
                            398 ;src/entities/player.c:78: if (nextx > 76) {
   5E8E 3E 4C         [ 7]  399 	ld	a, #0x4c
   5E90 BD            [ 4]  400 	cp	a, l
   5E91 3E 00         [ 7]  401 	ld	a, #0x00
   5E93 9C            [ 4]  402 	sbc	a, h
   5E94 E2 99 5E      [10]  403 	jp	PO, 00227$
   5E97 EE 80         [ 7]  404 	xor	a, #0x80
   5E99                     405 00227$:
   5E99 F2 9F 5E      [10]  406 	jp	P, 00135$
                            407 ;src/entities/player.c:79: nextx = 76;
   5E9C 21 4C 00      [10]  408 	ld	hl, #0x004c
   5E9F                     409 00135$:
                            410 ;src/entities/player.c:81: player->x = (u8)nextx;
   5E9F DD 75 F2      [19]  411 	ld	-14 (ix), l
   5EA2 7D            [ 4]  412 	ld	a, l
   5EA3 02            [ 7]  413 	ld	(bc), a
                            414 ;src/entities/player.c:83: nexty = (i16)player->y + (i16)player->vy;
   5EA4 DD 6E FA      [19]  415 	ld	l,-6 (ix)
   5EA7 DD 66 FB      [19]  416 	ld	h,-5 (ix)
   5EAA 5E            [ 7]  417 	ld	e, (hl)
   5EAB 16 00         [ 7]  418 	ld	d, #0x00
   5EAD DD 6E F8      [19]  419 	ld	l,-8 (ix)
   5EB0 DD 66 F9      [19]  420 	ld	h,-7 (ix)
   5EB3 6E            [ 7]  421 	ld	l, (hl)
   5EB4 7D            [ 4]  422 	ld	a, l
   5EB5 17            [ 4]  423 	rla
   5EB6 9F            [ 4]  424 	sbc	a, a
   5EB7 67            [ 4]  425 	ld	h, a
   5EB8 19            [11]  426 	add	hl, de
   5EB9 E5            [11]  427 	push	hl
   5EBA FD E1         [14]  428 	pop	iy
                            429 ;src/entities/player.c:84: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5EBC DD 6E FE      [19]  430 	ld	l,-2 (ix)
   5EBF DD 66 FF      [19]  431 	ld	h,-1 (ix)
   5EC2 66            [ 7]  432 	ld	h, (hl)
   5EC3 DD 5E F2      [19]  433 	ld	e, -14 (ix)
   5EC6 16 00         [ 7]  434 	ld	d, #0x00
   5EC8 C5            [11]  435 	push	bc
   5EC9 E5            [11]  436 	push	hl
   5ECA 33            [ 6]  437 	inc	sp
   5ECB FD E5         [15]  438 	push	iy
   5ECD D5            [11]  439 	push	de
   5ECE CD 87 4D      [17]  440 	call	_collision_clamp_y_at
   5ED1 F1            [10]  441 	pop	af
   5ED2 F1            [10]  442 	pop	af
   5ED3 33            [ 6]  443 	inc	sp
   5ED4 C1            [10]  444 	pop	bc
                            445 ;src/entities/player.c:85: if (nexty < 0) {
   5ED5 CB 7C         [ 8]  446 	bit	7, h
   5ED7 28 03         [12]  447 	jr	Z,00137$
                            448 ;src/entities/player.c:86: nexty = 0;
   5ED9 21 00 00      [10]  449 	ld	hl, #0x0000
   5EDC                     450 00137$:
                            451 ;src/entities/player.c:88: player->y = (u8)nexty;
   5EDC 5D            [ 4]  452 	ld	e, l
   5EDD DD 6E FA      [19]  453 	ld	l,-6 (ix)
   5EE0 DD 66 FB      [19]  454 	ld	h,-5 (ix)
   5EE3 73            [ 7]  455 	ld	(hl), e
                            456 ;src/entities/player.c:90: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5EE4 DD 6E FE      [19]  457 	ld	l,-2 (ix)
   5EE7 DD 66 FF      [19]  458 	ld	h,-1 (ix)
   5EEA 7E            [ 7]  459 	ld	a, (hl)
   5EEB 16 00         [ 7]  460 	ld	d, #0x00
   5EED F5            [11]  461 	push	af
   5EEE 0A            [ 7]  462 	ld	a, (bc)
   5EEF 4F            [ 4]  463 	ld	c, a
   5EF0 F1            [10]  464 	pop	af
   5EF1 06 00         [ 7]  465 	ld	b, #0x00
   5EF3 F5            [11]  466 	push	af
   5EF4 33            [ 6]  467 	inc	sp
   5EF5 D5            [11]  468 	push	de
   5EF6 C5            [11]  469 	push	bc
   5EF7 CD 08 4D      [17]  470 	call	_collision_is_on_ground_at
   5EFA F1            [10]  471 	pop	af
   5EFB F1            [10]  472 	pop	af
   5EFC 33            [ 6]  473 	inc	sp
   5EFD 7D            [ 4]  474 	ld	a, l
   5EFE B7            [ 4]  475 	or	a, a
   5EFF 28 19         [12]  476 	jr	Z,00141$
   5F01 DD 6E F8      [19]  477 	ld	l,-8 (ix)
   5F04 DD 66 F9      [19]  478 	ld	h,-7 (ix)
   5F07 4E            [ 7]  479 	ld	c, (hl)
   5F08 AF            [ 4]  480 	xor	a, a
   5F09 91            [ 4]  481 	sub	a, c
   5F0A E2 0F 5F      [10]  482 	jp	PO, 00228$
   5F0D EE 80         [ 7]  483 	xor	a, #0x80
   5F0F                     484 00228$:
   5F0F F2 1A 5F      [10]  485 	jp	P, 00141$
                            486 ;src/entities/player.c:91: player->vy = 0;
   5F12 DD 6E F8      [19]  487 	ld	l,-8 (ix)
   5F15 DD 66 F9      [19]  488 	ld	h,-7 (ix)
   5F18 36 00         [10]  489 	ld	(hl), #0x00
   5F1A                     490 00141$:
   5F1A DD F9         [10]  491 	ld	sp, ix
   5F1C DD E1         [14]  492 	pop	ix
   5F1E C9            [10]  493 	ret
                            494 ;src/entities/player.c:95: void playerrender(const Player* player) {
                            495 ;	---------------------------------
                            496 ; Function playerrender
                            497 ; ---------------------------------
   5F1F                     498 _playerrender::
   5F1F DD E5         [15]  499 	push	ix
   5F21 DD 21 00 00   [14]  500 	ld	ix,#0
   5F25 DD 39         [15]  501 	add	ix,sp
   5F27 3B            [ 6]  502 	dec	sp
                            503 ;src/entities/player.c:98: if (!player) {
   5F28 DD 7E 05      [19]  504 	ld	a, 5 (ix)
   5F2B DD B6 04      [19]  505 	or	a,4 (ix)
                            506 ;src/entities/player.c:99: return;
   5F2E 28 38         [12]  507 	jr	Z,00103$
                            508 ;src/entities/player.c:102: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5F30 DD 5E 04      [19]  509 	ld	e,4 (ix)
   5F33 DD 56 05      [19]  510 	ld	d,5 (ix)
   5F36 6B            [ 4]  511 	ld	l, e
   5F37 62            [ 4]  512 	ld	h, d
   5F38 23            [ 6]  513 	inc	hl
   5F39 46            [ 7]  514 	ld	b, (hl)
   5F3A 1A            [ 7]  515 	ld	a, (de)
   5F3B D5            [11]  516 	push	de
   5F3C C5            [11]  517 	push	bc
   5F3D 33            [ 6]  518 	inc	sp
   5F3E F5            [11]  519 	push	af
   5F3F 33            [ 6]  520 	inc	sp
   5F40 21 00 C0      [10]  521 	ld	hl, #0xc000
   5F43 E5            [11]  522 	push	hl
   5F44 CD 39 64      [17]  523 	call	_cpct_getScreenPtr
   5F47 4D            [ 4]  524 	ld	c, l
   5F48 44            [ 4]  525 	ld	b, h
   5F49 D1            [10]  526 	pop	de
                            527 ;src/entities/player.c:103: cpct_drawSprite((u8*)sprplayerknight_data, pvmem, player->w, player->h);
   5F4A D5            [11]  528 	push	de
   5F4B FD E1         [14]  529 	pop	iy
   5F4D FD 7E 05      [19]  530 	ld	a, 5 (iy)
   5F50 DD 77 FF      [19]  531 	ld	-1 (ix), a
   5F53 EB            [ 4]  532 	ex	de,hl
   5F54 11 04 00      [10]  533 	ld	de, #0x0004
   5F57 19            [11]  534 	add	hl, de
   5F58 56            [ 7]  535 	ld	d, (hl)
   5F59 DD 7E FF      [19]  536 	ld	a, -1 (ix)
   5F5C F5            [11]  537 	push	af
   5F5D 33            [ 6]  538 	inc	sp
   5F5E D5            [11]  539 	push	de
   5F5F 33            [ 6]  540 	inc	sp
   5F60 C5            [11]  541 	push	bc
   5F61 21 7C 55      [10]  542 	ld	hl, #_sprplayerknight_data
   5F64 E5            [11]  543 	push	hl
   5F65 CD 6A 62      [17]  544 	call	_cpct_drawSprite
   5F68                     545 00103$:
   5F68 33            [ 6]  546 	inc	sp
   5F69 DD E1         [14]  547 	pop	ix
   5F6B C9            [10]  548 	ret
                            549 ;src/entities/player.c:106: u8 player_get_ammo(const Player* player) {
                            550 ;	---------------------------------
                            551 ; Function player_get_ammo
                            552 ; ---------------------------------
   5F6C                     553 _player_get_ammo::
                            554 ;src/entities/player.c:108: return 3;
   5F6C 2E 03         [ 7]  555 	ld	l, #0x03
   5F6E C9            [10]  556 	ret
                            557 ;src/entities/player.c:111: u8 player_get_health(const Player* player) {
                            558 ;	---------------------------------
                            559 ; Function player_get_health
                            560 ; ---------------------------------
   5F6F                     561 _player_get_health::
                            562 ;src/entities/player.c:112: return player ? player->health : 0;
   5F6F 21 03 00      [10]  563 	ld	hl, #2+1
   5F72 39            [11]  564 	add	hl, sp
   5F73 7E            [ 7]  565 	ld	a, (hl)
   5F74 2B            [ 6]  566 	dec	hl
   5F75 B6            [ 7]  567 	or	a,(hl)
   5F76 28 0A         [12]  568 	jr	Z,00103$
   5F78 C1            [10]  569 	pop	bc
   5F79 E1            [10]  570 	pop	hl
   5F7A E5            [11]  571 	push	hl
   5F7B C5            [11]  572 	push	bc
   5F7C 11 06 00      [10]  573 	ld	de, #0x0006
   5F7F 19            [11]  574 	add	hl, de
   5F80 6E            [ 7]  575 	ld	l, (hl)
   5F81 C9            [10]  576 	ret
   5F82                     577 00103$:
   5F82 2E 00         [ 7]  578 	ld	l, #0x00
   5F84 C9            [10]  579 	ret
                            580 ;src/entities/player.c:115: u8 player_get_weapon(const Player* player) {
                            581 ;	---------------------------------
                            582 ; Function player_get_weapon
                            583 ; ---------------------------------
   5F85                     584 _player_get_weapon::
                            585 ;src/entities/player.c:116: return player ? player->weapon : 0;
   5F85 21 03 00      [10]  586 	ld	hl, #2+1
   5F88 39            [11]  587 	add	hl, sp
   5F89 7E            [ 7]  588 	ld	a, (hl)
   5F8A 2B            [ 6]  589 	dec	hl
   5F8B B6            [ 7]  590 	or	a,(hl)
   5F8C 28 0A         [12]  591 	jr	Z,00103$
   5F8E C1            [10]  592 	pop	bc
   5F8F E1            [10]  593 	pop	hl
   5F90 E5            [11]  594 	push	hl
   5F91 C5            [11]  595 	push	bc
   5F92 11 07 00      [10]  596 	ld	de, #0x0007
   5F95 19            [11]  597 	add	hl, de
   5F96 6E            [ 7]  598 	ld	l, (hl)
   5F97 C9            [10]  599 	ret
   5F98                     600 00103$:
   5F98 2E 00         [ 7]  601 	ld	l, #0x00
   5F9A C9            [10]  602 	ret
                            603 	.area _CODE
                            604 	.area _INITIALIZER
                            605 	.area _CABS (ABS)
