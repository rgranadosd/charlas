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
   5A7D                      59 _playerinit::
                             60 ;src/entities/player.c:18: if (!player) {
   5A7D 21 03 00      [10]   61 	ld	hl, #2+1
   5A80 39            [11]   62 	add	hl, sp
   5A81 7E            [ 7]   63 	ld	a, (hl)
   5A82 2B            [ 6]   64 	dec	hl
   5A83 B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:19: return;
   5A84 C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:22: player->x = 20;
   5A85 D1            [10]   69 	pop	de
   5A86 C1            [10]   70 	pop	bc
   5A87 C5            [11]   71 	push	bc
   5A88 D5            [11]   72 	push	de
   5A89 3E 14         [ 7]   73 	ld	a, #0x14
   5A8B 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:23: player->y = 120;
   5A8C 69            [ 4]   76 	ld	l, c
   5A8D 60            [ 4]   77 	ld	h, b
   5A8E 23            [ 6]   78 	inc	hl
   5A8F 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:24: player->vx = 0;
   5A91 59            [ 4]   81 	ld	e, c
   5A92 50            [ 4]   82 	ld	d, b
   5A93 13            [ 6]   83 	inc	de
   5A94 13            [ 6]   84 	inc	de
   5A95 AF            [ 4]   85 	xor	a, a
   5A96 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:25: player->vy = 0;
   5A97 59            [ 4]   88 	ld	e, c
   5A98 50            [ 4]   89 	ld	d, b
   5A99 13            [ 6]   90 	inc	de
   5A9A 13            [ 6]   91 	inc	de
   5A9B 13            [ 6]   92 	inc	de
   5A9C AF            [ 4]   93 	xor	a, a
   5A9D 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:26: player->w = 4;
   5A9E 21 04 00      [10]   96 	ld	hl, #0x0004
   5AA1 09            [11]   97 	add	hl, bc
   5AA2 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:27: player->h = 16;
   5AA4 21 05 00      [10]  100 	ld	hl, #0x0005
   5AA7 09            [11]  101 	add	hl, bc
   5AA8 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:28: player->health = 3;
   5AAA 21 06 00      [10]  104 	ld	hl, #0x0006
   5AAD 09            [11]  105 	add	hl, bc
   5AAE 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:29: player->weapon = 0;
   5AB0 21 07 00      [10]  108 	ld	hl, #0x0007
   5AB3 09            [11]  109 	add	hl, bc
   5AB4 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:30: player->facing_left = 0;
   5AB6 21 08 00      [10]  112 	ld	hl, #0x0008
   5AB9 09            [11]  113 	add	hl, bc
   5ABA 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:31: player->jump_hold = 0;
   5ABC 21 09 00      [10]  116 	ld	hl, #0x0009
   5ABF 09            [11]  117 	add	hl, bc
   5AC0 36 00         [10]  118 	ld	(hl), #0x00
   5AC2 C9            [10]  119 	ret
                            120 ;src/entities/player.c:34: void playerupdate(Player* player) {
                            121 ;	---------------------------------
                            122 ; Function playerupdate
                            123 ; ---------------------------------
   5AC3                     124 _playerupdate::
   5AC3 DD E5         [15]  125 	push	ix
   5AC5 DD 21 00 00   [14]  126 	ld	ix,#0
   5AC9 DD 39         [15]  127 	add	ix,sp
   5ACB 21 F2 FF      [10]  128 	ld	hl, #-14
   5ACE 39            [11]  129 	add	hl, sp
   5ACF F9            [ 6]  130 	ld	sp, hl
                            131 ;src/entities/player.c:38: if (!player) {
   5AD0 DD 7E 05      [19]  132 	ld	a, 5 (ix)
   5AD3 DD B6 04      [19]  133 	or	a,4 (ix)
                            134 ;src/entities/player.c:39: return;
   5AD6 CA 0E 5D      [10]  135 	jp	Z,00141$
                            136 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5AD9 CD E6 50      [17]  137 	call	_input_is_left_pressed
                            138 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5ADC DD 4E 04      [19]  139 	ld	c,4 (ix)
   5ADF DD 46 05      [19]  140 	ld	b,5 (ix)
   5AE2 59            [ 4]  141 	ld	e, c
   5AE3 50            [ 4]  142 	ld	d, b
   5AE4 13            [ 6]  143 	inc	de
   5AE5 13            [ 6]  144 	inc	de
                            145 ;src/entities/player.c:44: player->facing_left = 1;
   5AE6 79            [ 4]  146 	ld	a, c
   5AE7 C6 08         [ 7]  147 	add	a, #0x08
   5AE9 DD 77 FE      [19]  148 	ld	-2 (ix), a
   5AEC 78            [ 4]  149 	ld	a, b
   5AED CE 00         [ 7]  150 	adc	a, #0x00
   5AEF DD 77 FF      [19]  151 	ld	-1 (ix), a
                            152 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5AF2 7D            [ 4]  153 	ld	a, l
   5AF3 B7            [ 4]  154 	or	a, a
   5AF4 28 0E         [12]  155 	jr	Z,00116$
                            156 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5AF6 1A            [ 7]  157 	ld	a, (de)
   5AF7 C6 FF         [ 7]  158 	add	a, #0xff
   5AF9 12            [ 7]  159 	ld	(de), a
                            160 ;src/entities/player.c:44: player->facing_left = 1;
   5AFA DD 6E FE      [19]  161 	ld	l,-2 (ix)
   5AFD DD 66 FF      [19]  162 	ld	h,-1 (ix)
   5B00 36 01         [10]  163 	ld	(hl), #0x01
   5B02 18 55         [12]  164 	jr	00117$
   5B04                     165 00116$:
                            166 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5B04 C5            [11]  167 	push	bc
   5B05 D5            [11]  168 	push	de
   5B06 CD EE 50      [17]  169 	call	_input_is_right_pressed
   5B09 DD 75 FD      [19]  170 	ld	-3 (ix), l
   5B0C D1            [10]  171 	pop	de
   5B0D C1            [10]  172 	pop	bc
                            173 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5B0E 1A            [ 7]  174 	ld	a, (de)
                            175 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5B0F 6F            [ 4]  176 	ld	l,a
   5B10 3C            [ 4]  177 	inc	a
   5B11 DD 77 FC      [19]  178 	ld	-4 (ix), a
                            179 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5B14 DD 7E FD      [19]  180 	ld	a, -3 (ix)
   5B17 B7            [ 4]  181 	or	a, a
   5B18 28 0E         [12]  182 	jr	Z,00113$
                            183 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5B1A DD 7E FC      [19]  184 	ld	a, -4 (ix)
   5B1D 12            [ 7]  185 	ld	(de), a
                            186 ;src/entities/player.c:47: player->facing_left = 0;
   5B1E DD 6E FE      [19]  187 	ld	l,-2 (ix)
   5B21 DD 66 FF      [19]  188 	ld	h,-1 (ix)
   5B24 36 00         [10]  189 	ld	(hl), #0x00
   5B26 18 31         [12]  190 	jr	00117$
   5B28                     191 00113$:
                            192 ;src/entities/player.c:48: } else if (player->vx > 0) {
   5B28 AF            [ 4]  193 	xor	a, a
   5B29 95            [ 4]  194 	sub	a, l
   5B2A E2 2F 5B      [10]  195 	jp	PO, 00223$
   5B2D EE 80         [ 7]  196 	xor	a, #0x80
   5B2F                     197 00223$:
   5B2F F2 43 5B      [10]  198 	jp	P, 00110$
                            199 ;src/entities/player.c:49: player->vx = (i8)(player->vx - kplayerdeceleration);
   5B32 7D            [ 4]  200 	ld	a, l
   5B33 C6 FF         [ 7]  201 	add	a, #0xff
   5B35 DD 77 FD      [19]  202 	ld	-3 (ix), a
   5B38 12            [ 7]  203 	ld	(de),a
                            204 ;src/entities/player.c:50: if (player->vx < 0) player->vx = 0;
   5B39 DD CB FD 7E   [20]  205 	bit	7, -3 (ix)
   5B3D 28 1A         [12]  206 	jr	Z,00117$
   5B3F AF            [ 4]  207 	xor	a, a
   5B40 12            [ 7]  208 	ld	(de), a
   5B41 18 16         [12]  209 	jr	00117$
   5B43                     210 00110$:
                            211 ;src/entities/player.c:51: } else if (player->vx < 0) {
   5B43 CB 7D         [ 8]  212 	bit	7, l
   5B45 28 12         [12]  213 	jr	Z,00117$
                            214 ;src/entities/player.c:52: player->vx = (i8)(player->vx + kplayerdeceleration);
   5B47 DD 7E FC      [19]  215 	ld	a, -4 (ix)
   5B4A 12            [ 7]  216 	ld	(de), a
                            217 ;src/entities/player.c:53: if (player->vx > 0) player->vx = 0;
   5B4B AF            [ 4]  218 	xor	a, a
   5B4C DD 96 FC      [19]  219 	sub	a, -4 (ix)
   5B4F E2 54 5B      [10]  220 	jp	PO, 00224$
   5B52 EE 80         [ 7]  221 	xor	a, #0x80
   5B54                     222 00224$:
   5B54 F2 59 5B      [10]  223 	jp	P, 00117$
   5B57 AF            [ 4]  224 	xor	a, a
   5B58 12            [ 7]  225 	ld	(de), a
   5B59                     226 00117$:
                            227 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5B59 1A            [ 7]  228 	ld	a, (de)
   5B5A 6F            [ 4]  229 	ld	l, a
   5B5B 3E 03         [ 7]  230 	ld	a, #0x03
   5B5D 95            [ 4]  231 	sub	a, l
   5B5E E2 63 5B      [10]  232 	jp	PO, 00225$
   5B61 EE 80         [ 7]  233 	xor	a, #0x80
   5B63                     234 00225$:
   5B63 F2 69 5B      [10]  235 	jp	P, 00119$
   5B66 3E 03         [ 7]  236 	ld	a, #0x03
   5B68 12            [ 7]  237 	ld	(de), a
   5B69                     238 00119$:
                            239 ;src/entities/player.c:57: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5B69 1A            [ 7]  240 	ld	a, (de)
   5B6A EE 80         [ 7]  241 	xor	a, #0x80
   5B6C D6 7D         [ 7]  242 	sub	a, #0x7d
   5B6E 30 03         [12]  243 	jr	NC,00121$
   5B70 3E FD         [ 7]  244 	ld	a, #0xfd
   5B72 12            [ 7]  245 	ld	(de), a
   5B73                     246 00121$:
                            247 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5B73 C5            [11]  248 	push	bc
   5B74 D5            [11]  249 	push	de
   5B75 CD 0E 51      [17]  250 	call	_input_is_jump_just_pressed
   5B78 DD 75 FC      [19]  251 	ld	-4 (ix), l
   5B7B D1            [10]  252 	pop	de
   5B7C C1            [10]  253 	pop	bc
   5B7D 21 05 00      [10]  254 	ld	hl, #0x0005
   5B80 09            [11]  255 	add	hl,bc
   5B81 DD 75 FE      [19]  256 	ld	-2 (ix), l
   5B84 DD 74 FF      [19]  257 	ld	-1 (ix), h
   5B87 21 01 00      [10]  258 	ld	hl, #0x0001
   5B8A 09            [11]  259 	add	hl,bc
   5B8B DD 75 FA      [19]  260 	ld	-6 (ix), l
   5B8E DD 74 FB      [19]  261 	ld	-5 (ix), h
                            262 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5B91 21 03 00      [10]  263 	ld	hl, #0x0003
   5B94 09            [11]  264 	add	hl,bc
   5B95 DD 75 F8      [19]  265 	ld	-8 (ix), l
   5B98 DD 74 F9      [19]  266 	ld	-7 (ix), h
                            267 ;src/entities/player.c:61: player->jump_hold = 5;
   5B9B 21 09 00      [10]  268 	ld	hl, #0x0009
   5B9E 09            [11]  269 	add	hl,bc
   5B9F DD 75 F6      [19]  270 	ld	-10 (ix), l
   5BA2 DD 74 F7      [19]  271 	ld	-9 (ix), h
                            272 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5BA5 DD 7E FC      [19]  273 	ld	a, -4 (ix)
   5BA8 B7            [ 4]  274 	or	a, a
   5BA9 28 4E         [12]  275 	jr	Z,00123$
   5BAB DD 6E FE      [19]  276 	ld	l,-2 (ix)
   5BAE DD 66 FF      [19]  277 	ld	h,-1 (ix)
   5BB1 7E            [ 7]  278 	ld	a, (hl)
   5BB2 DD 6E FA      [19]  279 	ld	l,-6 (ix)
   5BB5 DD 66 FB      [19]  280 	ld	h,-5 (ix)
   5BB8 6E            [ 7]  281 	ld	l, (hl)
   5BB9 DD 75 F2      [19]  282 	ld	-14 (ix), l
   5BBC DD 36 F3 00   [19]  283 	ld	-13 (ix), #0x00
   5BC0 F5            [11]  284 	push	af
   5BC1 0A            [ 7]  285 	ld	a, (bc)
   5BC2 6F            [ 4]  286 	ld	l, a
   5BC3 F1            [10]  287 	pop	af
   5BC4 DD 75 F4      [19]  288 	ld	-12 (ix), l
   5BC7 DD 36 F5 00   [19]  289 	ld	-11 (ix), #0x00
   5BCB C5            [11]  290 	push	bc
   5BCC D5            [11]  291 	push	de
   5BCD F5            [11]  292 	push	af
   5BCE 33            [ 6]  293 	inc	sp
   5BCF DD 6E F2      [19]  294 	ld	l,-14 (ix)
   5BD2 DD 66 F3      [19]  295 	ld	h,-13 (ix)
   5BD5 E5            [11]  296 	push	hl
   5BD6 DD 6E F4      [19]  297 	ld	l,-12 (ix)
   5BD9 DD 66 F5      [19]  298 	ld	h,-11 (ix)
   5BDC E5            [11]  299 	push	hl
   5BDD CD C1 4B      [17]  300 	call	_collision_is_on_ground_at
   5BE0 F1            [10]  301 	pop	af
   5BE1 F1            [10]  302 	pop	af
   5BE2 33            [ 6]  303 	inc	sp
   5BE3 D1            [10]  304 	pop	de
   5BE4 C1            [10]  305 	pop	bc
   5BE5 7D            [ 4]  306 	ld	a, l
   5BE6 B7            [ 4]  307 	or	a, a
   5BE7 28 10         [12]  308 	jr	Z,00123$
                            309 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5BE9 DD 6E F8      [19]  310 	ld	l,-8 (ix)
   5BEC DD 66 F9      [19]  311 	ld	h,-7 (ix)
   5BEF 36 FA         [10]  312 	ld	(hl), #0xfa
                            313 ;src/entities/player.c:61: player->jump_hold = 5;
   5BF1 DD 6E F6      [19]  314 	ld	l,-10 (ix)
   5BF4 DD 66 F7      [19]  315 	ld	h,-9 (ix)
   5BF7 36 05         [10]  316 	ld	(hl), #0x05
   5BF9                     317 00123$:
                            318 ;src/entities/player.c:64: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5BF9 C5            [11]  319 	push	bc
   5BFA D5            [11]  320 	push	de
   5BFB CD 06 51      [17]  321 	call	_input_is_jump_pressed
   5BFE 7D            [ 4]  322 	ld	a, l
   5BFF D1            [10]  323 	pop	de
   5C00 C1            [10]  324 	pop	bc
   5C01 B7            [ 4]  325 	or	a, a
   5C02 28 31         [12]  326 	jr	Z,00126$
   5C04 DD 6E F6      [19]  327 	ld	l,-10 (ix)
   5C07 DD 66 F7      [19]  328 	ld	h,-9 (ix)
   5C0A 7E            [ 7]  329 	ld	a, (hl)
   5C0B B7            [ 4]  330 	or	a, a
   5C0C 28 27         [12]  331 	jr	Z,00126$
   5C0E DD 6E F8      [19]  332 	ld	l,-8 (ix)
   5C11 DD 66 F9      [19]  333 	ld	h,-7 (ix)
   5C14 6E            [ 7]  334 	ld	l, (hl)
   5C15 CB 7D         [ 8]  335 	bit	7, l
   5C17 28 1C         [12]  336 	jr	Z,00126$
                            337 ;src/entities/player.c:65: player->vy = (i8)(player->vy + kplayerjumpboost);
   5C19 7D            [ 4]  338 	ld	a, l
   5C1A C6 FF         [ 7]  339 	add	a, #0xff
   5C1C DD 6E F8      [19]  340 	ld	l,-8 (ix)
   5C1F DD 66 F9      [19]  341 	ld	h,-7 (ix)
   5C22 77            [ 7]  342 	ld	(hl), a
                            343 ;src/entities/player.c:66: player->jump_hold--;
   5C23 DD 6E F6      [19]  344 	ld	l,-10 (ix)
   5C26 DD 66 F7      [19]  345 	ld	h,-9 (ix)
   5C29 7E            [ 7]  346 	ld	a, (hl)
   5C2A C6 FF         [ 7]  347 	add	a, #0xff
   5C2C DD 6E F6      [19]  348 	ld	l,-10 (ix)
   5C2F DD 66 F7      [19]  349 	ld	h,-9 (ix)
   5C32 77            [ 7]  350 	ld	(hl), a
   5C33 18 08         [12]  351 	jr	00127$
   5C35                     352 00126$:
                            353 ;src/entities/player.c:68: player->jump_hold = 0;
   5C35 DD 6E F6      [19]  354 	ld	l,-10 (ix)
   5C38 DD 66 F7      [19]  355 	ld	h,-9 (ix)
   5C3B 36 00         [10]  356 	ld	(hl), #0x00
   5C3D                     357 00127$:
                            358 ;src/entities/player.c:71: player->vy = (i8)(player->vy + kplayergravity);
   5C3D DD 6E F8      [19]  359 	ld	l,-8 (ix)
   5C40 DD 66 F9      [19]  360 	ld	h,-7 (ix)
   5C43 7E            [ 7]  361 	ld	a, (hl)
   5C44 3C            [ 4]  362 	inc	a
   5C45 DD 77 F4      [19]  363 	ld	-12 (ix), a
   5C48 DD 6E F8      [19]  364 	ld	l,-8 (ix)
   5C4B DD 66 F9      [19]  365 	ld	h,-7 (ix)
   5C4E DD 7E F4      [19]  366 	ld	a, -12 (ix)
   5C51 77            [ 7]  367 	ld	(hl), a
                            368 ;src/entities/player.c:72: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5C52 3E 04         [ 7]  369 	ld	a, #0x04
   5C54 DD 96 F4      [19]  370 	sub	a, -12 (ix)
   5C57 E2 5C 5C      [10]  371 	jp	PO, 00226$
   5C5A EE 80         [ 7]  372 	xor	a, #0x80
   5C5C                     373 00226$:
   5C5C F2 67 5C      [10]  374 	jp	P, 00131$
   5C5F DD 6E F8      [19]  375 	ld	l,-8 (ix)
   5C62 DD 66 F9      [19]  376 	ld	h,-7 (ix)
   5C65 36 04         [10]  377 	ld	(hl), #0x04
   5C67                     378 00131$:
                            379 ;src/entities/player.c:74: nextx = (i16)player->x + (i16)player->vx;
   5C67 0A            [ 7]  380 	ld	a, (bc)
   5C68 DD 77 F4      [19]  381 	ld	-12 (ix), a
   5C6B DD 36 F5 00   [19]  382 	ld	-11 (ix), #0x00
   5C6F 1A            [ 7]  383 	ld	a, (de)
   5C70 5F            [ 4]  384 	ld	e, a
   5C71 17            [ 4]  385 	rla
   5C72 9F            [ 4]  386 	sbc	a, a
   5C73 57            [ 4]  387 	ld	d, a
   5C74 DD 6E F4      [19]  388 	ld	l,-12 (ix)
   5C77 DD 66 F5      [19]  389 	ld	h,-11 (ix)
   5C7A 19            [11]  390 	add	hl, de
                            391 ;src/entities/player.c:75: if (nextx < 0) {
   5C7B CB 7C         [ 8]  392 	bit	7, h
   5C7D 28 03         [12]  393 	jr	Z,00133$
                            394 ;src/entities/player.c:76: nextx = 0;
   5C7F 21 00 00      [10]  395 	ld	hl, #0x0000
   5C82                     396 00133$:
                            397 ;src/entities/player.c:78: if (nextx > 76) {
   5C82 3E 4C         [ 7]  398 	ld	a, #0x4c
   5C84 BD            [ 4]  399 	cp	a, l
   5C85 3E 00         [ 7]  400 	ld	a, #0x00
   5C87 9C            [ 4]  401 	sbc	a, h
   5C88 E2 8D 5C      [10]  402 	jp	PO, 00227$
   5C8B EE 80         [ 7]  403 	xor	a, #0x80
   5C8D                     404 00227$:
   5C8D F2 93 5C      [10]  405 	jp	P, 00135$
                            406 ;src/entities/player.c:79: nextx = 76;
   5C90 21 4C 00      [10]  407 	ld	hl, #0x004c
   5C93                     408 00135$:
                            409 ;src/entities/player.c:81: player->x = (u8)nextx;
   5C93 DD 75 F4      [19]  410 	ld	-12 (ix), l
   5C96 7D            [ 4]  411 	ld	a, l
   5C97 02            [ 7]  412 	ld	(bc), a
                            413 ;src/entities/player.c:83: nexty = (i16)player->y + (i16)player->vy;
   5C98 DD 6E FA      [19]  414 	ld	l,-6 (ix)
   5C9B DD 66 FB      [19]  415 	ld	h,-5 (ix)
   5C9E 5E            [ 7]  416 	ld	e, (hl)
   5C9F 16 00         [ 7]  417 	ld	d, #0x00
   5CA1 DD 6E F8      [19]  418 	ld	l,-8 (ix)
   5CA4 DD 66 F9      [19]  419 	ld	h,-7 (ix)
   5CA7 6E            [ 7]  420 	ld	l, (hl)
   5CA8 7D            [ 4]  421 	ld	a, l
   5CA9 17            [ 4]  422 	rla
   5CAA 9F            [ 4]  423 	sbc	a, a
   5CAB 67            [ 4]  424 	ld	h, a
   5CAC 19            [11]  425 	add	hl, de
   5CAD E5            [11]  426 	push	hl
   5CAE FD E1         [14]  427 	pop	iy
                            428 ;src/entities/player.c:84: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5CB0 DD 6E FE      [19]  429 	ld	l,-2 (ix)
   5CB3 DD 66 FF      [19]  430 	ld	h,-1 (ix)
   5CB6 66            [ 7]  431 	ld	h, (hl)
   5CB7 DD 5E F4      [19]  432 	ld	e, -12 (ix)
   5CBA 16 00         [ 7]  433 	ld	d, #0x00
   5CBC C5            [11]  434 	push	bc
   5CBD E5            [11]  435 	push	hl
   5CBE 33            [ 6]  436 	inc	sp
   5CBF FD E5         [15]  437 	push	iy
   5CC1 D5            [11]  438 	push	de
   5CC2 CD 40 4C      [17]  439 	call	_collision_clamp_y_at
   5CC5 F1            [10]  440 	pop	af
   5CC6 F1            [10]  441 	pop	af
   5CC7 33            [ 6]  442 	inc	sp
   5CC8 C1            [10]  443 	pop	bc
                            444 ;src/entities/player.c:85: if (nexty < 0) {
   5CC9 CB 7C         [ 8]  445 	bit	7, h
   5CCB 28 03         [12]  446 	jr	Z,00137$
                            447 ;src/entities/player.c:86: nexty = 0;
   5CCD 21 00 00      [10]  448 	ld	hl, #0x0000
   5CD0                     449 00137$:
                            450 ;src/entities/player.c:88: player->y = (u8)nexty;
   5CD0 5D            [ 4]  451 	ld	e, l
   5CD1 DD 6E FA      [19]  452 	ld	l,-6 (ix)
   5CD4 DD 66 FB      [19]  453 	ld	h,-5 (ix)
   5CD7 73            [ 7]  454 	ld	(hl), e
                            455 ;src/entities/player.c:90: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5CD8 DD 6E FE      [19]  456 	ld	l,-2 (ix)
   5CDB DD 66 FF      [19]  457 	ld	h,-1 (ix)
   5CDE 7E            [ 7]  458 	ld	a, (hl)
   5CDF 16 00         [ 7]  459 	ld	d, #0x00
   5CE1 F5            [11]  460 	push	af
   5CE2 0A            [ 7]  461 	ld	a, (bc)
   5CE3 4F            [ 4]  462 	ld	c, a
   5CE4 F1            [10]  463 	pop	af
   5CE5 06 00         [ 7]  464 	ld	b, #0x00
   5CE7 F5            [11]  465 	push	af
   5CE8 33            [ 6]  466 	inc	sp
   5CE9 D5            [11]  467 	push	de
   5CEA C5            [11]  468 	push	bc
   5CEB CD C1 4B      [17]  469 	call	_collision_is_on_ground_at
   5CEE F1            [10]  470 	pop	af
   5CEF F1            [10]  471 	pop	af
   5CF0 33            [ 6]  472 	inc	sp
   5CF1 7D            [ 4]  473 	ld	a, l
   5CF2 B7            [ 4]  474 	or	a, a
   5CF3 28 19         [12]  475 	jr	Z,00141$
   5CF5 DD 6E F8      [19]  476 	ld	l,-8 (ix)
   5CF8 DD 66 F9      [19]  477 	ld	h,-7 (ix)
   5CFB 4E            [ 7]  478 	ld	c, (hl)
   5CFC AF            [ 4]  479 	xor	a, a
   5CFD 91            [ 4]  480 	sub	a, c
   5CFE E2 03 5D      [10]  481 	jp	PO, 00228$
   5D01 EE 80         [ 7]  482 	xor	a, #0x80
   5D03                     483 00228$:
   5D03 F2 0E 5D      [10]  484 	jp	P, 00141$
                            485 ;src/entities/player.c:91: player->vy = 0;
   5D06 DD 6E F8      [19]  486 	ld	l,-8 (ix)
   5D09 DD 66 F9      [19]  487 	ld	h,-7 (ix)
   5D0C 36 00         [10]  488 	ld	(hl), #0x00
   5D0E                     489 00141$:
   5D0E DD F9         [10]  490 	ld	sp, ix
   5D10 DD E1         [14]  491 	pop	ix
   5D12 C9            [10]  492 	ret
                            493 ;src/entities/player.c:95: void playerrender(const Player* player) {
                            494 ;	---------------------------------
                            495 ; Function playerrender
                            496 ; ---------------------------------
   5D13                     497 _playerrender::
   5D13 DD E5         [15]  498 	push	ix
   5D15 DD 21 00 00   [14]  499 	ld	ix,#0
   5D19 DD 39         [15]  500 	add	ix,sp
   5D1B 3B            [ 6]  501 	dec	sp
                            502 ;src/entities/player.c:98: if (!player) {
   5D1C DD 7E 05      [19]  503 	ld	a, 5 (ix)
   5D1F DD B6 04      [19]  504 	or	a,4 (ix)
                            505 ;src/entities/player.c:99: return;
   5D22 28 38         [12]  506 	jr	Z,00103$
                            507 ;src/entities/player.c:102: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5D24 DD 5E 04      [19]  508 	ld	e,4 (ix)
   5D27 DD 56 05      [19]  509 	ld	d,5 (ix)
   5D2A 6B            [ 4]  510 	ld	l, e
   5D2B 62            [ 4]  511 	ld	h, d
   5D2C 23            [ 6]  512 	inc	hl
   5D2D 46            [ 7]  513 	ld	b, (hl)
   5D2E 1A            [ 7]  514 	ld	a, (de)
   5D2F D5            [11]  515 	push	de
   5D30 C5            [11]  516 	push	bc
   5D31 33            [ 6]  517 	inc	sp
   5D32 F5            [11]  518 	push	af
   5D33 33            [ 6]  519 	inc	sp
   5D34 21 00 C0      [10]  520 	ld	hl, #0xc000
   5D37 E5            [11]  521 	push	hl
   5D38 CD 2A 62      [17]  522 	call	_cpct_getScreenPtr
   5D3B 4D            [ 4]  523 	ld	c, l
   5D3C 44            [ 4]  524 	ld	b, h
   5D3D D1            [10]  525 	pop	de
                            526 ;src/entities/player.c:103: cpct_drawSprite((u8*)sprplayerknight_data, pvmem, player->w, player->h);
   5D3E D5            [11]  527 	push	de
   5D3F FD E1         [14]  528 	pop	iy
   5D41 FD 7E 05      [19]  529 	ld	a, 5 (iy)
   5D44 DD 77 FF      [19]  530 	ld	-1 (ix), a
   5D47 EB            [ 4]  531 	ex	de,hl
   5D48 11 04 00      [10]  532 	ld	de, #0x0004
   5D4B 19            [11]  533 	add	hl, de
   5D4C 56            [ 7]  534 	ld	d, (hl)
   5D4D DD 7E FF      [19]  535 	ld	a, -1 (ix)
   5D50 F5            [11]  536 	push	af
   5D51 33            [ 6]  537 	inc	sp
   5D52 D5            [11]  538 	push	de
   5D53 33            [ 6]  539 	inc	sp
   5D54 C5            [11]  540 	push	bc
   5D55 21 27 53      [10]  541 	ld	hl, #_sprplayerknight_data
   5D58 E5            [11]  542 	push	hl
   5D59 CD 5B 60      [17]  543 	call	_cpct_drawSprite
   5D5C                     544 00103$:
   5D5C 33            [ 6]  545 	inc	sp
   5D5D DD E1         [14]  546 	pop	ix
   5D5F C9            [10]  547 	ret
                            548 ;src/entities/player.c:106: u8 player_get_health(const Player* player) {
                            549 ;	---------------------------------
                            550 ; Function player_get_health
                            551 ; ---------------------------------
   5D60                     552 _player_get_health::
                            553 ;src/entities/player.c:107: return player ? player->health : 0;
   5D60 21 03 00      [10]  554 	ld	hl, #2+1
   5D63 39            [11]  555 	add	hl, sp
   5D64 7E            [ 7]  556 	ld	a, (hl)
   5D65 2B            [ 6]  557 	dec	hl
   5D66 B6            [ 7]  558 	or	a,(hl)
   5D67 28 0A         [12]  559 	jr	Z,00103$
   5D69 C1            [10]  560 	pop	bc
   5D6A E1            [10]  561 	pop	hl
   5D6B E5            [11]  562 	push	hl
   5D6C C5            [11]  563 	push	bc
   5D6D 11 06 00      [10]  564 	ld	de, #0x0006
   5D70 19            [11]  565 	add	hl, de
   5D71 6E            [ 7]  566 	ld	l, (hl)
   5D72 C9            [10]  567 	ret
   5D73                     568 00103$:
   5D73 2E 00         [ 7]  569 	ld	l, #0x00
   5D75 C9            [10]  570 	ret
                            571 ;src/entities/player.c:110: u8 player_get_weapon(const Player* player) {
                            572 ;	---------------------------------
                            573 ; Function player_get_weapon
                            574 ; ---------------------------------
   5D76                     575 _player_get_weapon::
                            576 ;src/entities/player.c:111: return player ? player->weapon : 0;
   5D76 21 03 00      [10]  577 	ld	hl, #2+1
   5D79 39            [11]  578 	add	hl, sp
   5D7A 7E            [ 7]  579 	ld	a, (hl)
   5D7B 2B            [ 6]  580 	dec	hl
   5D7C B6            [ 7]  581 	or	a,(hl)
   5D7D 28 0A         [12]  582 	jr	Z,00103$
   5D7F C1            [10]  583 	pop	bc
   5D80 E1            [10]  584 	pop	hl
   5D81 E5            [11]  585 	push	hl
   5D82 C5            [11]  586 	push	bc
   5D83 11 07 00      [10]  587 	ld	de, #0x0007
   5D86 19            [11]  588 	add	hl, de
   5D87 6E            [ 7]  589 	ld	l, (hl)
   5D88 C9            [10]  590 	ret
   5D89                     591 00103$:
   5D89 2E 00         [ 7]  592 	ld	l, #0x00
   5D8B C9            [10]  593 	ret
                            594 	.area _CODE
                            595 	.area _INITIALIZER
                            596 	.area _CABS (ABS)
