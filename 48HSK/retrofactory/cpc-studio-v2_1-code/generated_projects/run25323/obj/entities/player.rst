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
   5AFA                      59 _playerinit::
                             60 ;src/entities/player.c:18: if (!player) {
   5AFA 21 03 00      [10]   61 	ld	hl, #2+1
   5AFD 39            [11]   62 	add	hl, sp
   5AFE 7E            [ 7]   63 	ld	a, (hl)
   5AFF 2B            [ 6]   64 	dec	hl
   5B00 B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:19: return;
   5B01 C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:22: player->x = 20;
   5B02 D1            [10]   69 	pop	de
   5B03 C1            [10]   70 	pop	bc
   5B04 C5            [11]   71 	push	bc
   5B05 D5            [11]   72 	push	de
   5B06 3E 14         [ 7]   73 	ld	a, #0x14
   5B08 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:23: player->y = 120;
   5B09 69            [ 4]   76 	ld	l, c
   5B0A 60            [ 4]   77 	ld	h, b
   5B0B 23            [ 6]   78 	inc	hl
   5B0C 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:24: player->vx = 0;
   5B0E 59            [ 4]   81 	ld	e, c
   5B0F 50            [ 4]   82 	ld	d, b
   5B10 13            [ 6]   83 	inc	de
   5B11 13            [ 6]   84 	inc	de
   5B12 AF            [ 4]   85 	xor	a, a
   5B13 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:25: player->vy = 0;
   5B14 59            [ 4]   88 	ld	e, c
   5B15 50            [ 4]   89 	ld	d, b
   5B16 13            [ 6]   90 	inc	de
   5B17 13            [ 6]   91 	inc	de
   5B18 13            [ 6]   92 	inc	de
   5B19 AF            [ 4]   93 	xor	a, a
   5B1A 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:26: player->w = 4;
   5B1B 21 04 00      [10]   96 	ld	hl, #0x0004
   5B1E 09            [11]   97 	add	hl, bc
   5B1F 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:27: player->h = 16;
   5B21 21 05 00      [10]  100 	ld	hl, #0x0005
   5B24 09            [11]  101 	add	hl, bc
   5B25 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:28: player->health = 3;
   5B27 21 06 00      [10]  104 	ld	hl, #0x0006
   5B2A 09            [11]  105 	add	hl, bc
   5B2B 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:29: player->weapon = 0;
   5B2D 21 07 00      [10]  108 	ld	hl, #0x0007
   5B30 09            [11]  109 	add	hl, bc
   5B31 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:30: player->facing_left = 0;
   5B33 21 08 00      [10]  112 	ld	hl, #0x0008
   5B36 09            [11]  113 	add	hl, bc
   5B37 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:31: player->jump_hold = 0;
   5B39 21 09 00      [10]  116 	ld	hl, #0x0009
   5B3C 09            [11]  117 	add	hl, bc
   5B3D 36 00         [10]  118 	ld	(hl), #0x00
   5B3F C9            [10]  119 	ret
                            120 ;src/entities/player.c:34: void playerupdate(Player* player) {
                            121 ;	---------------------------------
                            122 ; Function playerupdate
                            123 ; ---------------------------------
   5B40                     124 _playerupdate::
   5B40 DD E5         [15]  125 	push	ix
   5B42 DD 21 00 00   [14]  126 	ld	ix,#0
   5B46 DD 39         [15]  127 	add	ix,sp
   5B48 21 F2 FF      [10]  128 	ld	hl, #-14
   5B4B 39            [11]  129 	add	hl, sp
   5B4C F9            [ 6]  130 	ld	sp, hl
                            131 ;src/entities/player.c:38: if (!player) {
   5B4D DD 7E 05      [19]  132 	ld	a, 5 (ix)
   5B50 DD B6 04      [19]  133 	or	a,4 (ix)
                            134 ;src/entities/player.c:39: return;
   5B53 CA 8B 5D      [10]  135 	jp	Z,00141$
                            136 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5B56 CD E8 50      [17]  137 	call	_input_is_left_pressed
                            138 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5B59 DD 4E 04      [19]  139 	ld	c,4 (ix)
   5B5C DD 46 05      [19]  140 	ld	b,5 (ix)
   5B5F 59            [ 4]  141 	ld	e, c
   5B60 50            [ 4]  142 	ld	d, b
   5B61 13            [ 6]  143 	inc	de
   5B62 13            [ 6]  144 	inc	de
                            145 ;src/entities/player.c:44: player->facing_left = 1;
   5B63 79            [ 4]  146 	ld	a, c
   5B64 C6 08         [ 7]  147 	add	a, #0x08
   5B66 DD 77 F4      [19]  148 	ld	-12 (ix), a
   5B69 78            [ 4]  149 	ld	a, b
   5B6A CE 00         [ 7]  150 	adc	a, #0x00
   5B6C DD 77 F5      [19]  151 	ld	-11 (ix), a
                            152 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5B6F 7D            [ 4]  153 	ld	a, l
   5B70 B7            [ 4]  154 	or	a, a
   5B71 28 0E         [12]  155 	jr	Z,00116$
                            156 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5B73 1A            [ 7]  157 	ld	a, (de)
   5B74 C6 FF         [ 7]  158 	add	a, #0xff
   5B76 12            [ 7]  159 	ld	(de), a
                            160 ;src/entities/player.c:44: player->facing_left = 1;
   5B77 DD 6E F4      [19]  161 	ld	l,-12 (ix)
   5B7A DD 66 F5      [19]  162 	ld	h,-11 (ix)
   5B7D 36 01         [10]  163 	ld	(hl), #0x01
   5B7F 18 55         [12]  164 	jr	00117$
   5B81                     165 00116$:
                            166 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5B81 C5            [11]  167 	push	bc
   5B82 D5            [11]  168 	push	de
   5B83 CD F0 50      [17]  169 	call	_input_is_right_pressed
   5B86 DD 75 F3      [19]  170 	ld	-13 (ix), l
   5B89 D1            [10]  171 	pop	de
   5B8A C1            [10]  172 	pop	bc
                            173 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5B8B 1A            [ 7]  174 	ld	a, (de)
                            175 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5B8C 6F            [ 4]  176 	ld	l,a
   5B8D 3C            [ 4]  177 	inc	a
   5B8E DD 77 F2      [19]  178 	ld	-14 (ix), a
                            179 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5B91 DD 7E F3      [19]  180 	ld	a, -13 (ix)
   5B94 B7            [ 4]  181 	or	a, a
   5B95 28 0E         [12]  182 	jr	Z,00113$
                            183 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5B97 DD 7E F2      [19]  184 	ld	a, -14 (ix)
   5B9A 12            [ 7]  185 	ld	(de), a
                            186 ;src/entities/player.c:47: player->facing_left = 0;
   5B9B DD 6E F4      [19]  187 	ld	l,-12 (ix)
   5B9E DD 66 F5      [19]  188 	ld	h,-11 (ix)
   5BA1 36 00         [10]  189 	ld	(hl), #0x00
   5BA3 18 31         [12]  190 	jr	00117$
   5BA5                     191 00113$:
                            192 ;src/entities/player.c:48: } else if (player->vx > 0) {
   5BA5 AF            [ 4]  193 	xor	a, a
   5BA6 95            [ 4]  194 	sub	a, l
   5BA7 E2 AC 5B      [10]  195 	jp	PO, 00223$
   5BAA EE 80         [ 7]  196 	xor	a, #0x80
   5BAC                     197 00223$:
   5BAC F2 C0 5B      [10]  198 	jp	P, 00110$
                            199 ;src/entities/player.c:49: player->vx = (i8)(player->vx - kplayerdeceleration);
   5BAF 7D            [ 4]  200 	ld	a, l
   5BB0 C6 FF         [ 7]  201 	add	a, #0xff
   5BB2 DD 77 F3      [19]  202 	ld	-13 (ix), a
   5BB5 12            [ 7]  203 	ld	(de),a
                            204 ;src/entities/player.c:50: if (player->vx < 0) player->vx = 0;
   5BB6 DD CB F3 7E   [20]  205 	bit	7, -13 (ix)
   5BBA 28 1A         [12]  206 	jr	Z,00117$
   5BBC AF            [ 4]  207 	xor	a, a
   5BBD 12            [ 7]  208 	ld	(de), a
   5BBE 18 16         [12]  209 	jr	00117$
   5BC0                     210 00110$:
                            211 ;src/entities/player.c:51: } else if (player->vx < 0) {
   5BC0 CB 7D         [ 8]  212 	bit	7, l
   5BC2 28 12         [12]  213 	jr	Z,00117$
                            214 ;src/entities/player.c:52: player->vx = (i8)(player->vx + kplayerdeceleration);
   5BC4 DD 7E F2      [19]  215 	ld	a, -14 (ix)
   5BC7 12            [ 7]  216 	ld	(de), a
                            217 ;src/entities/player.c:53: if (player->vx > 0) player->vx = 0;
   5BC8 AF            [ 4]  218 	xor	a, a
   5BC9 DD 96 F2      [19]  219 	sub	a, -14 (ix)
   5BCC E2 D1 5B      [10]  220 	jp	PO, 00224$
   5BCF EE 80         [ 7]  221 	xor	a, #0x80
   5BD1                     222 00224$:
   5BD1 F2 D6 5B      [10]  223 	jp	P, 00117$
   5BD4 AF            [ 4]  224 	xor	a, a
   5BD5 12            [ 7]  225 	ld	(de), a
   5BD6                     226 00117$:
                            227 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5BD6 1A            [ 7]  228 	ld	a, (de)
   5BD7 6F            [ 4]  229 	ld	l, a
   5BD8 3E 03         [ 7]  230 	ld	a, #0x03
   5BDA 95            [ 4]  231 	sub	a, l
   5BDB E2 E0 5B      [10]  232 	jp	PO, 00225$
   5BDE EE 80         [ 7]  233 	xor	a, #0x80
   5BE0                     234 00225$:
   5BE0 F2 E6 5B      [10]  235 	jp	P, 00119$
   5BE3 3E 03         [ 7]  236 	ld	a, #0x03
   5BE5 12            [ 7]  237 	ld	(de), a
   5BE6                     238 00119$:
                            239 ;src/entities/player.c:57: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5BE6 1A            [ 7]  240 	ld	a, (de)
   5BE7 EE 80         [ 7]  241 	xor	a, #0x80
   5BE9 D6 7D         [ 7]  242 	sub	a, #0x7d
   5BEB 30 03         [12]  243 	jr	NC,00121$
   5BED 3E FD         [ 7]  244 	ld	a, #0xfd
   5BEF 12            [ 7]  245 	ld	(de), a
   5BF0                     246 00121$:
                            247 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5BF0 C5            [11]  248 	push	bc
   5BF1 D5            [11]  249 	push	de
   5BF2 CD 10 51      [17]  250 	call	_input_is_jump_just_pressed
   5BF5 DD 75 F2      [19]  251 	ld	-14 (ix), l
   5BF8 D1            [10]  252 	pop	de
   5BF9 C1            [10]  253 	pop	bc
   5BFA 21 05 00      [10]  254 	ld	hl, #0x0005
   5BFD 09            [11]  255 	add	hl,bc
   5BFE DD 75 F4      [19]  256 	ld	-12 (ix), l
   5C01 DD 74 F5      [19]  257 	ld	-11 (ix), h
   5C04 21 01 00      [10]  258 	ld	hl, #0x0001
   5C07 09            [11]  259 	add	hl,bc
   5C08 DD 75 FE      [19]  260 	ld	-2 (ix), l
   5C0B DD 74 FF      [19]  261 	ld	-1 (ix), h
                            262 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5C0E 21 03 00      [10]  263 	ld	hl, #0x0003
   5C11 09            [11]  264 	add	hl,bc
   5C12 DD 75 FC      [19]  265 	ld	-4 (ix), l
   5C15 DD 74 FD      [19]  266 	ld	-3 (ix), h
                            267 ;src/entities/player.c:61: player->jump_hold = 5;
   5C18 21 09 00      [10]  268 	ld	hl, #0x0009
   5C1B 09            [11]  269 	add	hl,bc
   5C1C DD 75 FA      [19]  270 	ld	-6 (ix), l
   5C1F DD 74 FB      [19]  271 	ld	-5 (ix), h
                            272 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5C22 DD 7E F2      [19]  273 	ld	a, -14 (ix)
   5C25 B7            [ 4]  274 	or	a, a
   5C26 28 4E         [12]  275 	jr	Z,00123$
   5C28 DD 6E F4      [19]  276 	ld	l,-12 (ix)
   5C2B DD 66 F5      [19]  277 	ld	h,-11 (ix)
   5C2E 7E            [ 7]  278 	ld	a, (hl)
   5C2F DD 6E FE      [19]  279 	ld	l,-2 (ix)
   5C32 DD 66 FF      [19]  280 	ld	h,-1 (ix)
   5C35 6E            [ 7]  281 	ld	l, (hl)
   5C36 DD 75 F8      [19]  282 	ld	-8 (ix), l
   5C39 DD 36 F9 00   [19]  283 	ld	-7 (ix), #0x00
   5C3D F5            [11]  284 	push	af
   5C3E 0A            [ 7]  285 	ld	a, (bc)
   5C3F 6F            [ 4]  286 	ld	l, a
   5C40 F1            [10]  287 	pop	af
   5C41 DD 75 F6      [19]  288 	ld	-10 (ix), l
   5C44 DD 36 F7 00   [19]  289 	ld	-9 (ix), #0x00
   5C48 C5            [11]  290 	push	bc
   5C49 D5            [11]  291 	push	de
   5C4A F5            [11]  292 	push	af
   5C4B 33            [ 6]  293 	inc	sp
   5C4C DD 6E F8      [19]  294 	ld	l,-8 (ix)
   5C4F DD 66 F9      [19]  295 	ld	h,-7 (ix)
   5C52 E5            [11]  296 	push	hl
   5C53 DD 6E F6      [19]  297 	ld	l,-10 (ix)
   5C56 DD 66 F7      [19]  298 	ld	h,-9 (ix)
   5C59 E5            [11]  299 	push	hl
   5C5A CD C3 4B      [17]  300 	call	_collision_is_on_ground_at
   5C5D F1            [10]  301 	pop	af
   5C5E F1            [10]  302 	pop	af
   5C5F 33            [ 6]  303 	inc	sp
   5C60 D1            [10]  304 	pop	de
   5C61 C1            [10]  305 	pop	bc
   5C62 7D            [ 4]  306 	ld	a, l
   5C63 B7            [ 4]  307 	or	a, a
   5C64 28 10         [12]  308 	jr	Z,00123$
                            309 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5C66 DD 6E FC      [19]  310 	ld	l,-4 (ix)
   5C69 DD 66 FD      [19]  311 	ld	h,-3 (ix)
   5C6C 36 FA         [10]  312 	ld	(hl), #0xfa
                            313 ;src/entities/player.c:61: player->jump_hold = 5;
   5C6E DD 6E FA      [19]  314 	ld	l,-6 (ix)
   5C71 DD 66 FB      [19]  315 	ld	h,-5 (ix)
   5C74 36 05         [10]  316 	ld	(hl), #0x05
   5C76                     317 00123$:
                            318 ;src/entities/player.c:64: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5C76 C5            [11]  319 	push	bc
   5C77 D5            [11]  320 	push	de
   5C78 CD 08 51      [17]  321 	call	_input_is_jump_pressed
   5C7B 7D            [ 4]  322 	ld	a, l
   5C7C D1            [10]  323 	pop	de
   5C7D C1            [10]  324 	pop	bc
   5C7E B7            [ 4]  325 	or	a, a
   5C7F 28 31         [12]  326 	jr	Z,00126$
   5C81 DD 6E FA      [19]  327 	ld	l,-6 (ix)
   5C84 DD 66 FB      [19]  328 	ld	h,-5 (ix)
   5C87 7E            [ 7]  329 	ld	a, (hl)
   5C88 B7            [ 4]  330 	or	a, a
   5C89 28 27         [12]  331 	jr	Z,00126$
   5C8B DD 6E FC      [19]  332 	ld	l,-4 (ix)
   5C8E DD 66 FD      [19]  333 	ld	h,-3 (ix)
   5C91 6E            [ 7]  334 	ld	l, (hl)
   5C92 CB 7D         [ 8]  335 	bit	7, l
   5C94 28 1C         [12]  336 	jr	Z,00126$
                            337 ;src/entities/player.c:65: player->vy = (i8)(player->vy + kplayerjumpboost);
   5C96 7D            [ 4]  338 	ld	a, l
   5C97 C6 FF         [ 7]  339 	add	a, #0xff
   5C99 DD 6E FC      [19]  340 	ld	l,-4 (ix)
   5C9C DD 66 FD      [19]  341 	ld	h,-3 (ix)
   5C9F 77            [ 7]  342 	ld	(hl), a
                            343 ;src/entities/player.c:66: player->jump_hold--;
   5CA0 DD 6E FA      [19]  344 	ld	l,-6 (ix)
   5CA3 DD 66 FB      [19]  345 	ld	h,-5 (ix)
   5CA6 7E            [ 7]  346 	ld	a, (hl)
   5CA7 C6 FF         [ 7]  347 	add	a, #0xff
   5CA9 DD 6E FA      [19]  348 	ld	l,-6 (ix)
   5CAC DD 66 FB      [19]  349 	ld	h,-5 (ix)
   5CAF 77            [ 7]  350 	ld	(hl), a
   5CB0 18 08         [12]  351 	jr	00127$
   5CB2                     352 00126$:
                            353 ;src/entities/player.c:68: player->jump_hold = 0;
   5CB2 DD 6E FA      [19]  354 	ld	l,-6 (ix)
   5CB5 DD 66 FB      [19]  355 	ld	h,-5 (ix)
   5CB8 36 00         [10]  356 	ld	(hl), #0x00
   5CBA                     357 00127$:
                            358 ;src/entities/player.c:71: player->vy = (i8)(player->vy + kplayergravity);
   5CBA DD 6E FC      [19]  359 	ld	l,-4 (ix)
   5CBD DD 66 FD      [19]  360 	ld	h,-3 (ix)
   5CC0 7E            [ 7]  361 	ld	a, (hl)
   5CC1 3C            [ 4]  362 	inc	a
   5CC2 DD 77 F6      [19]  363 	ld	-10 (ix), a
   5CC5 DD 6E FC      [19]  364 	ld	l,-4 (ix)
   5CC8 DD 66 FD      [19]  365 	ld	h,-3 (ix)
   5CCB DD 7E F6      [19]  366 	ld	a, -10 (ix)
   5CCE 77            [ 7]  367 	ld	(hl), a
                            368 ;src/entities/player.c:72: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5CCF 3E 04         [ 7]  369 	ld	a, #0x04
   5CD1 DD 96 F6      [19]  370 	sub	a, -10 (ix)
   5CD4 E2 D9 5C      [10]  371 	jp	PO, 00226$
   5CD7 EE 80         [ 7]  372 	xor	a, #0x80
   5CD9                     373 00226$:
   5CD9 F2 E4 5C      [10]  374 	jp	P, 00131$
   5CDC DD 6E FC      [19]  375 	ld	l,-4 (ix)
   5CDF DD 66 FD      [19]  376 	ld	h,-3 (ix)
   5CE2 36 04         [10]  377 	ld	(hl), #0x04
   5CE4                     378 00131$:
                            379 ;src/entities/player.c:74: nextx = (i16)player->x + (i16)player->vx;
   5CE4 0A            [ 7]  380 	ld	a, (bc)
   5CE5 DD 77 F6      [19]  381 	ld	-10 (ix), a
   5CE8 DD 36 F7 00   [19]  382 	ld	-9 (ix), #0x00
   5CEC 1A            [ 7]  383 	ld	a, (de)
   5CED 5F            [ 4]  384 	ld	e, a
   5CEE 17            [ 4]  385 	rla
   5CEF 9F            [ 4]  386 	sbc	a, a
   5CF0 57            [ 4]  387 	ld	d, a
   5CF1 DD 6E F6      [19]  388 	ld	l,-10 (ix)
   5CF4 DD 66 F7      [19]  389 	ld	h,-9 (ix)
   5CF7 19            [11]  390 	add	hl, de
                            391 ;src/entities/player.c:75: if (nextx < 0) {
   5CF8 CB 7C         [ 8]  392 	bit	7, h
   5CFA 28 03         [12]  393 	jr	Z,00133$
                            394 ;src/entities/player.c:76: nextx = 0;
   5CFC 21 00 00      [10]  395 	ld	hl, #0x0000
   5CFF                     396 00133$:
                            397 ;src/entities/player.c:78: if (nextx > 76) {
   5CFF 3E 4C         [ 7]  398 	ld	a, #0x4c
   5D01 BD            [ 4]  399 	cp	a, l
   5D02 3E 00         [ 7]  400 	ld	a, #0x00
   5D04 9C            [ 4]  401 	sbc	a, h
   5D05 E2 0A 5D      [10]  402 	jp	PO, 00227$
   5D08 EE 80         [ 7]  403 	xor	a, #0x80
   5D0A                     404 00227$:
   5D0A F2 10 5D      [10]  405 	jp	P, 00135$
                            406 ;src/entities/player.c:79: nextx = 76;
   5D0D 21 4C 00      [10]  407 	ld	hl, #0x004c
   5D10                     408 00135$:
                            409 ;src/entities/player.c:81: player->x = (u8)nextx;
   5D10 DD 75 F6      [19]  410 	ld	-10 (ix), l
   5D13 7D            [ 4]  411 	ld	a, l
   5D14 02            [ 7]  412 	ld	(bc), a
                            413 ;src/entities/player.c:83: nexty = (i16)player->y + (i16)player->vy;
   5D15 DD 6E FE      [19]  414 	ld	l,-2 (ix)
   5D18 DD 66 FF      [19]  415 	ld	h,-1 (ix)
   5D1B 5E            [ 7]  416 	ld	e, (hl)
   5D1C 16 00         [ 7]  417 	ld	d, #0x00
   5D1E DD 6E FC      [19]  418 	ld	l,-4 (ix)
   5D21 DD 66 FD      [19]  419 	ld	h,-3 (ix)
   5D24 6E            [ 7]  420 	ld	l, (hl)
   5D25 7D            [ 4]  421 	ld	a, l
   5D26 17            [ 4]  422 	rla
   5D27 9F            [ 4]  423 	sbc	a, a
   5D28 67            [ 4]  424 	ld	h, a
   5D29 19            [11]  425 	add	hl, de
   5D2A E5            [11]  426 	push	hl
   5D2B FD E1         [14]  427 	pop	iy
                            428 ;src/entities/player.c:84: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5D2D DD 6E F4      [19]  429 	ld	l,-12 (ix)
   5D30 DD 66 F5      [19]  430 	ld	h,-11 (ix)
   5D33 66            [ 7]  431 	ld	h, (hl)
   5D34 DD 5E F6      [19]  432 	ld	e, -10 (ix)
   5D37 16 00         [ 7]  433 	ld	d, #0x00
   5D39 C5            [11]  434 	push	bc
   5D3A E5            [11]  435 	push	hl
   5D3B 33            [ 6]  436 	inc	sp
   5D3C FD E5         [15]  437 	push	iy
   5D3E D5            [11]  438 	push	de
   5D3F CD 42 4C      [17]  439 	call	_collision_clamp_y_at
   5D42 F1            [10]  440 	pop	af
   5D43 F1            [10]  441 	pop	af
   5D44 33            [ 6]  442 	inc	sp
   5D45 C1            [10]  443 	pop	bc
                            444 ;src/entities/player.c:85: if (nexty < 0) {
   5D46 CB 7C         [ 8]  445 	bit	7, h
   5D48 28 03         [12]  446 	jr	Z,00137$
                            447 ;src/entities/player.c:86: nexty = 0;
   5D4A 21 00 00      [10]  448 	ld	hl, #0x0000
   5D4D                     449 00137$:
                            450 ;src/entities/player.c:88: player->y = (u8)nexty;
   5D4D 5D            [ 4]  451 	ld	e, l
   5D4E DD 6E FE      [19]  452 	ld	l,-2 (ix)
   5D51 DD 66 FF      [19]  453 	ld	h,-1 (ix)
   5D54 73            [ 7]  454 	ld	(hl), e
                            455 ;src/entities/player.c:90: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5D55 DD 6E F4      [19]  456 	ld	l,-12 (ix)
   5D58 DD 66 F5      [19]  457 	ld	h,-11 (ix)
   5D5B 7E            [ 7]  458 	ld	a, (hl)
   5D5C 16 00         [ 7]  459 	ld	d, #0x00
   5D5E F5            [11]  460 	push	af
   5D5F 0A            [ 7]  461 	ld	a, (bc)
   5D60 4F            [ 4]  462 	ld	c, a
   5D61 F1            [10]  463 	pop	af
   5D62 06 00         [ 7]  464 	ld	b, #0x00
   5D64 F5            [11]  465 	push	af
   5D65 33            [ 6]  466 	inc	sp
   5D66 D5            [11]  467 	push	de
   5D67 C5            [11]  468 	push	bc
   5D68 CD C3 4B      [17]  469 	call	_collision_is_on_ground_at
   5D6B F1            [10]  470 	pop	af
   5D6C F1            [10]  471 	pop	af
   5D6D 33            [ 6]  472 	inc	sp
   5D6E 7D            [ 4]  473 	ld	a, l
   5D6F B7            [ 4]  474 	or	a, a
   5D70 28 19         [12]  475 	jr	Z,00141$
   5D72 DD 6E FC      [19]  476 	ld	l,-4 (ix)
   5D75 DD 66 FD      [19]  477 	ld	h,-3 (ix)
   5D78 4E            [ 7]  478 	ld	c, (hl)
   5D79 AF            [ 4]  479 	xor	a, a
   5D7A 91            [ 4]  480 	sub	a, c
   5D7B E2 80 5D      [10]  481 	jp	PO, 00228$
   5D7E EE 80         [ 7]  482 	xor	a, #0x80
   5D80                     483 00228$:
   5D80 F2 8B 5D      [10]  484 	jp	P, 00141$
                            485 ;src/entities/player.c:91: player->vy = 0;
   5D83 DD 6E FC      [19]  486 	ld	l,-4 (ix)
   5D86 DD 66 FD      [19]  487 	ld	h,-3 (ix)
   5D89 36 00         [10]  488 	ld	(hl), #0x00
   5D8B                     489 00141$:
   5D8B DD F9         [10]  490 	ld	sp, ix
   5D8D DD E1         [14]  491 	pop	ix
   5D8F C9            [10]  492 	ret
                            493 ;src/entities/player.c:95: void playerrender(const Player* player) {
                            494 ;	---------------------------------
                            495 ; Function playerrender
                            496 ; ---------------------------------
   5D90                     497 _playerrender::
   5D90 DD E5         [15]  498 	push	ix
   5D92 DD 21 00 00   [14]  499 	ld	ix,#0
   5D96 DD 39         [15]  500 	add	ix,sp
   5D98 3B            [ 6]  501 	dec	sp
                            502 ;src/entities/player.c:98: if (!player) {
   5D99 DD 7E 05      [19]  503 	ld	a, 5 (ix)
   5D9C DD B6 04      [19]  504 	or	a,4 (ix)
                            505 ;src/entities/player.c:99: return;
   5D9F 28 38         [12]  506 	jr	Z,00103$
                            507 ;src/entities/player.c:102: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5DA1 DD 5E 04      [19]  508 	ld	e,4 (ix)
   5DA4 DD 56 05      [19]  509 	ld	d,5 (ix)
   5DA7 6B            [ 4]  510 	ld	l, e
   5DA8 62            [ 4]  511 	ld	h, d
   5DA9 23            [ 6]  512 	inc	hl
   5DAA 46            [ 7]  513 	ld	b, (hl)
   5DAB 1A            [ 7]  514 	ld	a, (de)
   5DAC D5            [11]  515 	push	de
   5DAD C5            [11]  516 	push	bc
   5DAE 33            [ 6]  517 	inc	sp
   5DAF F5            [11]  518 	push	af
   5DB0 33            [ 6]  519 	inc	sp
   5DB1 21 00 C0      [10]  520 	ld	hl, #0xc000
   5DB4 E5            [11]  521 	push	hl
   5DB5 CD A7 62      [17]  522 	call	_cpct_getScreenPtr
   5DB8 4D            [ 4]  523 	ld	c, l
   5DB9 44            [ 4]  524 	ld	b, h
   5DBA D1            [10]  525 	pop	de
                            526 ;src/entities/player.c:103: cpct_drawSprite((u8*)sprplayerknight_data, pvmem, player->w, player->h);
   5DBB D5            [11]  527 	push	de
   5DBC FD E1         [14]  528 	pop	iy
   5DBE FD 7E 05      [19]  529 	ld	a, 5 (iy)
   5DC1 DD 77 FF      [19]  530 	ld	-1 (ix), a
   5DC4 EB            [ 4]  531 	ex	de,hl
   5DC5 11 04 00      [10]  532 	ld	de, #0x0004
   5DC8 19            [11]  533 	add	hl, de
   5DC9 56            [ 7]  534 	ld	d, (hl)
   5DCA DD 7E FF      [19]  535 	ld	a, -1 (ix)
   5DCD F5            [11]  536 	push	af
   5DCE 33            [ 6]  537 	inc	sp
   5DCF D5            [11]  538 	push	de
   5DD0 33            [ 6]  539 	inc	sp
   5DD1 C5            [11]  540 	push	bc
   5DD2 21 69 53      [10]  541 	ld	hl, #_sprplayerknight_data
   5DD5 E5            [11]  542 	push	hl
   5DD6 CD D8 60      [17]  543 	call	_cpct_drawSprite
   5DD9                     544 00103$:
   5DD9 33            [ 6]  545 	inc	sp
   5DDA DD E1         [14]  546 	pop	ix
   5DDC C9            [10]  547 	ret
                            548 ;src/entities/player.c:106: u8 player_get_health(const Player* player) {
                            549 ;	---------------------------------
                            550 ; Function player_get_health
                            551 ; ---------------------------------
   5DDD                     552 _player_get_health::
                            553 ;src/entities/player.c:107: return player ? player->health : 0;
   5DDD 21 03 00      [10]  554 	ld	hl, #2+1
   5DE0 39            [11]  555 	add	hl, sp
   5DE1 7E            [ 7]  556 	ld	a, (hl)
   5DE2 2B            [ 6]  557 	dec	hl
   5DE3 B6            [ 7]  558 	or	a,(hl)
   5DE4 28 0A         [12]  559 	jr	Z,00103$
   5DE6 C1            [10]  560 	pop	bc
   5DE7 E1            [10]  561 	pop	hl
   5DE8 E5            [11]  562 	push	hl
   5DE9 C5            [11]  563 	push	bc
   5DEA 11 06 00      [10]  564 	ld	de, #0x0006
   5DED 19            [11]  565 	add	hl, de
   5DEE 6E            [ 7]  566 	ld	l, (hl)
   5DEF C9            [10]  567 	ret
   5DF0                     568 00103$:
   5DF0 2E 00         [ 7]  569 	ld	l, #0x00
   5DF2 C9            [10]  570 	ret
                            571 ;src/entities/player.c:110: u8 player_get_weapon(const Player* player) {
                            572 ;	---------------------------------
                            573 ; Function player_get_weapon
                            574 ; ---------------------------------
   5DF3                     575 _player_get_weapon::
                            576 ;src/entities/player.c:111: return player ? player->weapon : 0;
   5DF3 21 03 00      [10]  577 	ld	hl, #2+1
   5DF6 39            [11]  578 	add	hl, sp
   5DF7 7E            [ 7]  579 	ld	a, (hl)
   5DF8 2B            [ 6]  580 	dec	hl
   5DF9 B6            [ 7]  581 	or	a,(hl)
   5DFA 28 0A         [12]  582 	jr	Z,00103$
   5DFC C1            [10]  583 	pop	bc
   5DFD E1            [10]  584 	pop	hl
   5DFE E5            [11]  585 	push	hl
   5DFF C5            [11]  586 	push	bc
   5E00 11 07 00      [10]  587 	ld	de, #0x0007
   5E03 19            [11]  588 	add	hl, de
   5E04 6E            [ 7]  589 	ld	l, (hl)
   5E05 C9            [10]  590 	ret
   5E06                     591 00103$:
   5E06 2E 00         [ 7]  592 	ld	l, #0x00
   5E08 C9            [10]  593 	ret
                            594 	.area _CODE
                            595 	.area _INITIALIZER
                            596 	.area _CABS (ABS)
