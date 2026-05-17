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
   5AFA                      59 _playerinit::
                             60 ;src/entities/player.c:28: if (!player) {
   5AFA 21 03 00      [10]   61 	ld	hl, #2+1
   5AFD 39            [11]   62 	add	hl, sp
   5AFE 7E            [ 7]   63 	ld	a, (hl)
   5AFF 2B            [ 6]   64 	dec	hl
   5B00 B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:29: return;
   5B01 C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:32: player->x = 20;
   5B02 D1            [10]   69 	pop	de
   5B03 C1            [10]   70 	pop	bc
   5B04 C5            [11]   71 	push	bc
   5B05 D5            [11]   72 	push	de
   5B06 3E 14         [ 7]   73 	ld	a, #0x14
   5B08 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:33: player->y = 120;
   5B09 69            [ 4]   76 	ld	l, c
   5B0A 60            [ 4]   77 	ld	h, b
   5B0B 23            [ 6]   78 	inc	hl
   5B0C 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:34: player->vx = 0;
   5B0E 59            [ 4]   81 	ld	e, c
   5B0F 50            [ 4]   82 	ld	d, b
   5B10 13            [ 6]   83 	inc	de
   5B11 13            [ 6]   84 	inc	de
   5B12 AF            [ 4]   85 	xor	a, a
   5B13 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:35: player->vy = 0;
   5B14 59            [ 4]   88 	ld	e, c
   5B15 50            [ 4]   89 	ld	d, b
   5B16 13            [ 6]   90 	inc	de
   5B17 13            [ 6]   91 	inc	de
   5B18 13            [ 6]   92 	inc	de
   5B19 AF            [ 4]   93 	xor	a, a
   5B1A 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:36: player->w = 4;
   5B1B 21 04 00      [10]   96 	ld	hl, #0x0004
   5B1E 09            [11]   97 	add	hl, bc
   5B1F 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:37: player->h = 16;
   5B21 21 05 00      [10]  100 	ld	hl, #0x0005
   5B24 09            [11]  101 	add	hl, bc
   5B25 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:38: player->health = 3;
   5B27 21 06 00      [10]  104 	ld	hl, #0x0006
   5B2A 09            [11]  105 	add	hl, bc
   5B2B 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:39: player->weapon = 0;
   5B2D 21 07 00      [10]  108 	ld	hl, #0x0007
   5B30 09            [11]  109 	add	hl, bc
   5B31 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:40: player->facing_left = 0;
   5B33 21 08 00      [10]  112 	ld	hl, #0x0008
   5B36 09            [11]  113 	add	hl, bc
   5B37 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:41: player->jump_hold = 0;
   5B39 21 09 00      [10]  116 	ld	hl, #0x0009
   5B3C 09            [11]  117 	add	hl, bc
   5B3D 36 00         [10]  118 	ld	(hl), #0x00
   5B3F C9            [10]  119 	ret
   5B40                     120 _player_sprite:
   5B40 3C                  121 	.db #0x3c	; 60
   5B41 3C                  122 	.db #0x3c	; 60
   5B42 3C                  123 	.db #0x3c	; 60
   5B43 3C                  124 	.db #0x3c	; 60
   5B44 28                  125 	.db #0x28	; 40
   5B45 28                  126 	.db #0x28	; 40
   5B46 00                  127 	.db #0x00	; 0
   5B47 14                  128 	.db #0x14	; 20
   5B48 28                  129 	.db #0x28	; 40
   5B49 28                  130 	.db #0x28	; 40
   5B4A 00                  131 	.db #0x00	; 0
   5B4B 14                  132 	.db #0x14	; 20
   5B4C 28                  133 	.db #0x28	; 40
   5B4D 28                  134 	.db #0x28	; 40
   5B4E 00                  135 	.db #0x00	; 0
   5B4F 14                  136 	.db #0x14	; 20
   5B50 28                  137 	.db #0x28	; 40
   5B51 28                  138 	.db #0x28	; 40
   5B52 00                  139 	.db #0x00	; 0
   5B53 14                  140 	.db #0x14	; 20
   5B54 28                  141 	.db #0x28	; 40
   5B55 28                  142 	.db #0x28	; 40
   5B56 00                  143 	.db #0x00	; 0
   5B57 14                  144 	.db #0x14	; 20
   5B58 28                  145 	.db #0x28	; 40
   5B59 28                  146 	.db #0x28	; 40
   5B5A 00                  147 	.db #0x00	; 0
   5B5B 14                  148 	.db #0x14	; 20
   5B5C 28                  149 	.db #0x28	; 40
   5B5D 28                  150 	.db #0x28	; 40
   5B5E 00                  151 	.db #0x00	; 0
   5B5F 14                  152 	.db #0x14	; 20
   5B60 3C                  153 	.db #0x3c	; 60
   5B61 3C                  154 	.db #0x3c	; 60
   5B62 3C                  155 	.db #0x3c	; 60
   5B63 3C                  156 	.db #0x3c	; 60
   5B64 28                  157 	.db #0x28	; 40
   5B65 28                  158 	.db #0x28	; 40
   5B66 00                  159 	.db #0x00	; 0
   5B67 14                  160 	.db #0x14	; 20
   5B68 28                  161 	.db #0x28	; 40
   5B69 28                  162 	.db #0x28	; 40
   5B6A 00                  163 	.db #0x00	; 0
   5B6B 14                  164 	.db #0x14	; 20
   5B6C 28                  165 	.db #0x28	; 40
   5B6D 28                  166 	.db #0x28	; 40
   5B6E 00                  167 	.db #0x00	; 0
   5B6F 14                  168 	.db #0x14	; 20
   5B70 28                  169 	.db #0x28	; 40
   5B71 28                  170 	.db #0x28	; 40
   5B72 00                  171 	.db #0x00	; 0
   5B73 14                  172 	.db #0x14	; 20
   5B74 28                  173 	.db #0x28	; 40
   5B75 28                  174 	.db #0x28	; 40
   5B76 00                  175 	.db #0x00	; 0
   5B77 14                  176 	.db #0x14	; 20
   5B78 28                  177 	.db #0x28	; 40
   5B79 28                  178 	.db #0x28	; 40
   5B7A 00                  179 	.db #0x00	; 0
   5B7B 14                  180 	.db #0x14	; 20
   5B7C 3C                  181 	.db #0x3c	; 60
   5B7D 3C                  182 	.db #0x3c	; 60
   5B7E 3C                  183 	.db #0x3c	; 60
   5B7F 3C                  184 	.db #0x3c	; 60
                            185 ;src/entities/player.c:44: void playerupdate(Player* player) {
                            186 ;	---------------------------------
                            187 ; Function playerupdate
                            188 ; ---------------------------------
   5B80                     189 _playerupdate::
   5B80 DD E5         [15]  190 	push	ix
   5B82 DD 21 00 00   [14]  191 	ld	ix,#0
   5B86 DD 39         [15]  192 	add	ix,sp
   5B88 21 F2 FF      [10]  193 	ld	hl, #-14
   5B8B 39            [11]  194 	add	hl, sp
   5B8C F9            [ 6]  195 	ld	sp, hl
                            196 ;src/entities/player.c:48: if (!player) {
   5B8D DD 7E 05      [19]  197 	ld	a, 5 (ix)
   5B90 DD B6 04      [19]  198 	or	a,4 (ix)
                            199 ;src/entities/player.c:49: return;
   5B93 CA B2 5D      [10]  200 	jp	Z,00141$
                            201 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5B96 CD 08 51      [17]  202 	call	_input_is_left_pressed
                            203 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5B99 DD 4E 04      [19]  204 	ld	c,4 (ix)
   5B9C DD 46 05      [19]  205 	ld	b,5 (ix)
   5B9F 59            [ 4]  206 	ld	e, c
   5BA0 50            [ 4]  207 	ld	d, b
   5BA1 13            [ 6]  208 	inc	de
   5BA2 13            [ 6]  209 	inc	de
                            210 ;src/entities/player.c:54: player->facing_left = 1;
   5BA3 79            [ 4]  211 	ld	a, c
   5BA4 C6 08         [ 7]  212 	add	a, #0x08
   5BA6 DD 77 F2      [19]  213 	ld	-14 (ix), a
   5BA9 78            [ 4]  214 	ld	a, b
   5BAA CE 00         [ 7]  215 	adc	a, #0x00
   5BAC DD 77 F3      [19]  216 	ld	-13 (ix), a
                            217 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5BAF 7D            [ 4]  218 	ld	a, l
   5BB0 B7            [ 4]  219 	or	a, a
   5BB1 28 0A         [12]  220 	jr	Z,00116$
                            221 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5BB3 1A            [ 7]  222 	ld	a, (de)
   5BB4 C6 FF         [ 7]  223 	add	a, #0xff
   5BB6 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/player.c:54: player->facing_left = 1;
   5BB7 E1            [10]  226 	pop	hl
   5BB8 E5            [11]  227 	push	hl
   5BB9 36 01         [10]  228 	ld	(hl), #0x01
   5BBB 18 51         [12]  229 	jr	00117$
   5BBD                     230 00116$:
                            231 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5BBD C5            [11]  232 	push	bc
   5BBE D5            [11]  233 	push	de
   5BBF CD 10 51      [17]  234 	call	_input_is_right_pressed
   5BC2 DD 75 F4      [19]  235 	ld	-12 (ix), l
   5BC5 D1            [10]  236 	pop	de
   5BC6 C1            [10]  237 	pop	bc
                            238 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5BC7 1A            [ 7]  239 	ld	a, (de)
                            240 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5BC8 6F            [ 4]  241 	ld	l,a
   5BC9 3C            [ 4]  242 	inc	a
   5BCA DD 77 F5      [19]  243 	ld	-11 (ix), a
                            244 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5BCD DD 7E F4      [19]  245 	ld	a, -12 (ix)
   5BD0 B7            [ 4]  246 	or	a, a
   5BD1 28 0A         [12]  247 	jr	Z,00113$
                            248 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5BD3 DD 7E F5      [19]  249 	ld	a, -11 (ix)
   5BD6 12            [ 7]  250 	ld	(de), a
                            251 ;src/entities/player.c:57: player->facing_left = 0;
   5BD7 E1            [10]  252 	pop	hl
   5BD8 E5            [11]  253 	push	hl
   5BD9 36 00         [10]  254 	ld	(hl), #0x00
   5BDB 18 31         [12]  255 	jr	00117$
   5BDD                     256 00113$:
                            257 ;src/entities/player.c:58: } else if (player->vx > 0) {
   5BDD AF            [ 4]  258 	xor	a, a
   5BDE 95            [ 4]  259 	sub	a, l
   5BDF E2 E4 5B      [10]  260 	jp	PO, 00223$
   5BE2 EE 80         [ 7]  261 	xor	a, #0x80
   5BE4                     262 00223$:
   5BE4 F2 F8 5B      [10]  263 	jp	P, 00110$
                            264 ;src/entities/player.c:59: player->vx = (i8)(player->vx - kplayerdeceleration);
   5BE7 7D            [ 4]  265 	ld	a, l
   5BE8 C6 FF         [ 7]  266 	add	a, #0xff
   5BEA DD 77 F4      [19]  267 	ld	-12 (ix), a
   5BED 12            [ 7]  268 	ld	(de),a
                            269 ;src/entities/player.c:60: if (player->vx < 0) player->vx = 0;
   5BEE DD CB F4 7E   [20]  270 	bit	7, -12 (ix)
   5BF2 28 1A         [12]  271 	jr	Z,00117$
   5BF4 AF            [ 4]  272 	xor	a, a
   5BF5 12            [ 7]  273 	ld	(de), a
   5BF6 18 16         [12]  274 	jr	00117$
   5BF8                     275 00110$:
                            276 ;src/entities/player.c:61: } else if (player->vx < 0) {
   5BF8 CB 7D         [ 8]  277 	bit	7, l
   5BFA 28 12         [12]  278 	jr	Z,00117$
                            279 ;src/entities/player.c:62: player->vx = (i8)(player->vx + kplayerdeceleration);
   5BFC DD 7E F5      [19]  280 	ld	a, -11 (ix)
   5BFF 12            [ 7]  281 	ld	(de), a
                            282 ;src/entities/player.c:63: if (player->vx > 0) player->vx = 0;
   5C00 AF            [ 4]  283 	xor	a, a
   5C01 DD 96 F5      [19]  284 	sub	a, -11 (ix)
   5C04 E2 09 5C      [10]  285 	jp	PO, 00224$
   5C07 EE 80         [ 7]  286 	xor	a, #0x80
   5C09                     287 00224$:
   5C09 F2 0E 5C      [10]  288 	jp	P, 00117$
   5C0C AF            [ 4]  289 	xor	a, a
   5C0D 12            [ 7]  290 	ld	(de), a
   5C0E                     291 00117$:
                            292 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5C0E 1A            [ 7]  293 	ld	a, (de)
   5C0F 6F            [ 4]  294 	ld	l, a
   5C10 3E 03         [ 7]  295 	ld	a, #0x03
   5C12 95            [ 4]  296 	sub	a, l
   5C13 E2 18 5C      [10]  297 	jp	PO, 00225$
   5C16 EE 80         [ 7]  298 	xor	a, #0x80
   5C18                     299 00225$:
   5C18 F2 1E 5C      [10]  300 	jp	P, 00119$
   5C1B 3E 03         [ 7]  301 	ld	a, #0x03
   5C1D 12            [ 7]  302 	ld	(de), a
   5C1E                     303 00119$:
                            304 ;src/entities/player.c:67: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5C1E 1A            [ 7]  305 	ld	a, (de)
   5C1F EE 80         [ 7]  306 	xor	a, #0x80
   5C21 D6 7D         [ 7]  307 	sub	a, #0x7d
   5C23 30 03         [12]  308 	jr	NC,00121$
   5C25 3E FD         [ 7]  309 	ld	a, #0xfd
   5C27 12            [ 7]  310 	ld	(de), a
   5C28                     311 00121$:
                            312 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5C28 C5            [11]  313 	push	bc
   5C29 D5            [11]  314 	push	de
   5C2A CD 30 51      [17]  315 	call	_input_is_jump_just_pressed
   5C2D DD 75 F5      [19]  316 	ld	-11 (ix), l
   5C30 D1            [10]  317 	pop	de
   5C31 C1            [10]  318 	pop	bc
   5C32 21 05 00      [10]  319 	ld	hl, #0x0005
   5C35 09            [11]  320 	add	hl,bc
   5C36 E3            [19]  321 	ex	(sp), hl
   5C37 21 01 00      [10]  322 	ld	hl, #0x0001
   5C3A 09            [11]  323 	add	hl,bc
   5C3B DD 75 FE      [19]  324 	ld	-2 (ix), l
   5C3E DD 74 FF      [19]  325 	ld	-1 (ix), h
                            326 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   5C41 21 03 00      [10]  327 	ld	hl, #0x0003
   5C44 09            [11]  328 	add	hl,bc
   5C45 DD 75 FC      [19]  329 	ld	-4 (ix), l
   5C48 DD 74 FD      [19]  330 	ld	-3 (ix), h
                            331 ;src/entities/player.c:71: player->jump_hold = 5;
   5C4B 21 09 00      [10]  332 	ld	hl, #0x0009
   5C4E 09            [11]  333 	add	hl,bc
   5C4F DD 75 FA      [19]  334 	ld	-6 (ix), l
   5C52 DD 74 FB      [19]  335 	ld	-5 (ix), h
                            336 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5C55 DD 7E F5      [19]  337 	ld	a, -11 (ix)
   5C58 B7            [ 4]  338 	or	a, a
   5C59 28 4A         [12]  339 	jr	Z,00123$
   5C5B E1            [10]  340 	pop	hl
   5C5C E5            [11]  341 	push	hl
   5C5D 7E            [ 7]  342 	ld	a, (hl)
   5C5E DD 6E FE      [19]  343 	ld	l,-2 (ix)
   5C61 DD 66 FF      [19]  344 	ld	h,-1 (ix)
   5C64 6E            [ 7]  345 	ld	l, (hl)
   5C65 DD 75 F8      [19]  346 	ld	-8 (ix), l
   5C68 DD 36 F9 00   [19]  347 	ld	-7 (ix), #0x00
   5C6C F5            [11]  348 	push	af
   5C6D 0A            [ 7]  349 	ld	a, (bc)
   5C6E 6F            [ 4]  350 	ld	l, a
   5C6F F1            [10]  351 	pop	af
   5C70 DD 75 F6      [19]  352 	ld	-10 (ix), l
   5C73 DD 36 F7 00   [19]  353 	ld	-9 (ix), #0x00
   5C77 C5            [11]  354 	push	bc
   5C78 D5            [11]  355 	push	de
   5C79 F5            [11]  356 	push	af
   5C7A 33            [ 6]  357 	inc	sp
   5C7B DD 6E F8      [19]  358 	ld	l,-8 (ix)
   5C7E DD 66 F9      [19]  359 	ld	h,-7 (ix)
   5C81 E5            [11]  360 	push	hl
   5C82 DD 6E F6      [19]  361 	ld	l,-10 (ix)
   5C85 DD 66 F7      [19]  362 	ld	h,-9 (ix)
   5C88 E5            [11]  363 	push	hl
   5C89 CD C3 4B      [17]  364 	call	_collision_is_on_ground_at
   5C8C F1            [10]  365 	pop	af
   5C8D F1            [10]  366 	pop	af
   5C8E 33            [ 6]  367 	inc	sp
   5C8F D1            [10]  368 	pop	de
   5C90 C1            [10]  369 	pop	bc
   5C91 7D            [ 4]  370 	ld	a, l
   5C92 B7            [ 4]  371 	or	a, a
   5C93 28 10         [12]  372 	jr	Z,00123$
                            373 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   5C95 DD 6E FC      [19]  374 	ld	l,-4 (ix)
   5C98 DD 66 FD      [19]  375 	ld	h,-3 (ix)
   5C9B 36 FA         [10]  376 	ld	(hl), #0xfa
                            377 ;src/entities/player.c:71: player->jump_hold = 5;
   5C9D DD 6E FA      [19]  378 	ld	l,-6 (ix)
   5CA0 DD 66 FB      [19]  379 	ld	h,-5 (ix)
   5CA3 36 05         [10]  380 	ld	(hl), #0x05
   5CA5                     381 00123$:
                            382 ;src/entities/player.c:74: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5CA5 C5            [11]  383 	push	bc
   5CA6 D5            [11]  384 	push	de
   5CA7 CD 28 51      [17]  385 	call	_input_is_jump_pressed
   5CAA 7D            [ 4]  386 	ld	a, l
   5CAB D1            [10]  387 	pop	de
   5CAC C1            [10]  388 	pop	bc
   5CAD B7            [ 4]  389 	or	a, a
   5CAE 28 31         [12]  390 	jr	Z,00126$
   5CB0 DD 6E FA      [19]  391 	ld	l,-6 (ix)
   5CB3 DD 66 FB      [19]  392 	ld	h,-5 (ix)
   5CB6 7E            [ 7]  393 	ld	a, (hl)
   5CB7 B7            [ 4]  394 	or	a, a
   5CB8 28 27         [12]  395 	jr	Z,00126$
   5CBA DD 6E FC      [19]  396 	ld	l,-4 (ix)
   5CBD DD 66 FD      [19]  397 	ld	h,-3 (ix)
   5CC0 6E            [ 7]  398 	ld	l, (hl)
   5CC1 CB 7D         [ 8]  399 	bit	7, l
   5CC3 28 1C         [12]  400 	jr	Z,00126$
                            401 ;src/entities/player.c:75: player->vy = (i8)(player->vy + kplayerjumpboost);
   5CC5 7D            [ 4]  402 	ld	a, l
   5CC6 C6 FF         [ 7]  403 	add	a, #0xff
   5CC8 DD 6E FC      [19]  404 	ld	l,-4 (ix)
   5CCB DD 66 FD      [19]  405 	ld	h,-3 (ix)
   5CCE 77            [ 7]  406 	ld	(hl), a
                            407 ;src/entities/player.c:76: player->jump_hold--;
   5CCF DD 6E FA      [19]  408 	ld	l,-6 (ix)
   5CD2 DD 66 FB      [19]  409 	ld	h,-5 (ix)
   5CD5 7E            [ 7]  410 	ld	a, (hl)
   5CD6 C6 FF         [ 7]  411 	add	a, #0xff
   5CD8 DD 6E FA      [19]  412 	ld	l,-6 (ix)
   5CDB DD 66 FB      [19]  413 	ld	h,-5 (ix)
   5CDE 77            [ 7]  414 	ld	(hl), a
   5CDF 18 08         [12]  415 	jr	00127$
   5CE1                     416 00126$:
                            417 ;src/entities/player.c:78: player->jump_hold = 0;
   5CE1 DD 6E FA      [19]  418 	ld	l,-6 (ix)
   5CE4 DD 66 FB      [19]  419 	ld	h,-5 (ix)
   5CE7 36 00         [10]  420 	ld	(hl), #0x00
   5CE9                     421 00127$:
                            422 ;src/entities/player.c:81: player->vy = (i8)(player->vy + kplayergravity);
   5CE9 DD 6E FC      [19]  423 	ld	l,-4 (ix)
   5CEC DD 66 FD      [19]  424 	ld	h,-3 (ix)
   5CEF 7E            [ 7]  425 	ld	a, (hl)
   5CF0 3C            [ 4]  426 	inc	a
   5CF1 DD 77 F6      [19]  427 	ld	-10 (ix), a
   5CF4 DD 6E FC      [19]  428 	ld	l,-4 (ix)
   5CF7 DD 66 FD      [19]  429 	ld	h,-3 (ix)
   5CFA DD 7E F6      [19]  430 	ld	a, -10 (ix)
   5CFD 77            [ 7]  431 	ld	(hl), a
                            432 ;src/entities/player.c:82: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5CFE 3E 04         [ 7]  433 	ld	a, #0x04
   5D00 DD 96 F6      [19]  434 	sub	a, -10 (ix)
   5D03 E2 08 5D      [10]  435 	jp	PO, 00226$
   5D06 EE 80         [ 7]  436 	xor	a, #0x80
   5D08                     437 00226$:
   5D08 F2 13 5D      [10]  438 	jp	P, 00131$
   5D0B DD 6E FC      [19]  439 	ld	l,-4 (ix)
   5D0E DD 66 FD      [19]  440 	ld	h,-3 (ix)
   5D11 36 04         [10]  441 	ld	(hl), #0x04
   5D13                     442 00131$:
                            443 ;src/entities/player.c:84: nextx = (i16)player->x + (i16)player->vx;
   5D13 0A            [ 7]  444 	ld	a, (bc)
   5D14 DD 77 F6      [19]  445 	ld	-10 (ix), a
   5D17 DD 36 F7 00   [19]  446 	ld	-9 (ix), #0x00
   5D1B 1A            [ 7]  447 	ld	a, (de)
   5D1C 5F            [ 4]  448 	ld	e, a
   5D1D 17            [ 4]  449 	rla
   5D1E 9F            [ 4]  450 	sbc	a, a
   5D1F 57            [ 4]  451 	ld	d, a
   5D20 DD 6E F6      [19]  452 	ld	l,-10 (ix)
   5D23 DD 66 F7      [19]  453 	ld	h,-9 (ix)
   5D26 19            [11]  454 	add	hl, de
                            455 ;src/entities/player.c:85: if (nextx < 0) {
   5D27 CB 7C         [ 8]  456 	bit	7, h
   5D29 28 03         [12]  457 	jr	Z,00133$
                            458 ;src/entities/player.c:86: nextx = 0;
   5D2B 21 00 00      [10]  459 	ld	hl, #0x0000
   5D2E                     460 00133$:
                            461 ;src/entities/player.c:88: if (nextx > 76) {
   5D2E 3E 4C         [ 7]  462 	ld	a, #0x4c
   5D30 BD            [ 4]  463 	cp	a, l
   5D31 3E 00         [ 7]  464 	ld	a, #0x00
   5D33 9C            [ 4]  465 	sbc	a, h
   5D34 E2 39 5D      [10]  466 	jp	PO, 00227$
   5D37 EE 80         [ 7]  467 	xor	a, #0x80
   5D39                     468 00227$:
   5D39 F2 3F 5D      [10]  469 	jp	P, 00135$
                            470 ;src/entities/player.c:89: nextx = 76;
   5D3C 21 4C 00      [10]  471 	ld	hl, #0x004c
   5D3F                     472 00135$:
                            473 ;src/entities/player.c:91: player->x = (u8)nextx;
   5D3F DD 75 F6      [19]  474 	ld	-10 (ix), l
   5D42 7D            [ 4]  475 	ld	a, l
   5D43 02            [ 7]  476 	ld	(bc), a
                            477 ;src/entities/player.c:93: nexty = (i16)player->y + (i16)player->vy;
   5D44 DD 6E FE      [19]  478 	ld	l,-2 (ix)
   5D47 DD 66 FF      [19]  479 	ld	h,-1 (ix)
   5D4A 5E            [ 7]  480 	ld	e, (hl)
   5D4B 16 00         [ 7]  481 	ld	d, #0x00
   5D4D DD 6E FC      [19]  482 	ld	l,-4 (ix)
   5D50 DD 66 FD      [19]  483 	ld	h,-3 (ix)
   5D53 6E            [ 7]  484 	ld	l, (hl)
   5D54 7D            [ 4]  485 	ld	a, l
   5D55 17            [ 4]  486 	rla
   5D56 9F            [ 4]  487 	sbc	a, a
   5D57 67            [ 4]  488 	ld	h, a
   5D58 19            [11]  489 	add	hl, de
   5D59 E5            [11]  490 	push	hl
   5D5A FD E1         [14]  491 	pop	iy
                            492 ;src/entities/player.c:94: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5D5C E1            [10]  493 	pop	hl
   5D5D E5            [11]  494 	push	hl
   5D5E 66            [ 7]  495 	ld	h, (hl)
   5D5F DD 5E F6      [19]  496 	ld	e, -10 (ix)
   5D62 16 00         [ 7]  497 	ld	d, #0x00
   5D64 C5            [11]  498 	push	bc
   5D65 E5            [11]  499 	push	hl
   5D66 33            [ 6]  500 	inc	sp
   5D67 FD E5         [15]  501 	push	iy
   5D69 D5            [11]  502 	push	de
   5D6A CD 42 4C      [17]  503 	call	_collision_clamp_y_at
   5D6D F1            [10]  504 	pop	af
   5D6E F1            [10]  505 	pop	af
   5D6F 33            [ 6]  506 	inc	sp
   5D70 C1            [10]  507 	pop	bc
                            508 ;src/entities/player.c:95: if (nexty < 0) {
   5D71 CB 7C         [ 8]  509 	bit	7, h
   5D73 28 03         [12]  510 	jr	Z,00137$
                            511 ;src/entities/player.c:96: nexty = 0;
   5D75 21 00 00      [10]  512 	ld	hl, #0x0000
   5D78                     513 00137$:
                            514 ;src/entities/player.c:98: player->y = (u8)nexty;
   5D78 5D            [ 4]  515 	ld	e, l
   5D79 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   5D7C DD 66 FF      [19]  517 	ld	h,-1 (ix)
   5D7F 73            [ 7]  518 	ld	(hl), e
                            519 ;src/entities/player.c:100: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5D80 E1            [10]  520 	pop	hl
   5D81 E5            [11]  521 	push	hl
   5D82 7E            [ 7]  522 	ld	a, (hl)
   5D83 16 00         [ 7]  523 	ld	d, #0x00
   5D85 F5            [11]  524 	push	af
   5D86 0A            [ 7]  525 	ld	a, (bc)
   5D87 4F            [ 4]  526 	ld	c, a
   5D88 F1            [10]  527 	pop	af
   5D89 06 00         [ 7]  528 	ld	b, #0x00
   5D8B F5            [11]  529 	push	af
   5D8C 33            [ 6]  530 	inc	sp
   5D8D D5            [11]  531 	push	de
   5D8E C5            [11]  532 	push	bc
   5D8F CD C3 4B      [17]  533 	call	_collision_is_on_ground_at
   5D92 F1            [10]  534 	pop	af
   5D93 F1            [10]  535 	pop	af
   5D94 33            [ 6]  536 	inc	sp
   5D95 7D            [ 4]  537 	ld	a, l
   5D96 B7            [ 4]  538 	or	a, a
   5D97 28 19         [12]  539 	jr	Z,00141$
   5D99 DD 6E FC      [19]  540 	ld	l,-4 (ix)
   5D9C DD 66 FD      [19]  541 	ld	h,-3 (ix)
   5D9F 4E            [ 7]  542 	ld	c, (hl)
   5DA0 AF            [ 4]  543 	xor	a, a
   5DA1 91            [ 4]  544 	sub	a, c
   5DA2 E2 A7 5D      [10]  545 	jp	PO, 00228$
   5DA5 EE 80         [ 7]  546 	xor	a, #0x80
   5DA7                     547 00228$:
   5DA7 F2 B2 5D      [10]  548 	jp	P, 00141$
                            549 ;src/entities/player.c:101: player->vy = 0;
   5DAA DD 6E FC      [19]  550 	ld	l,-4 (ix)
   5DAD DD 66 FD      [19]  551 	ld	h,-3 (ix)
   5DB0 36 00         [10]  552 	ld	(hl), #0x00
   5DB2                     553 00141$:
   5DB2 DD F9         [10]  554 	ld	sp, ix
   5DB4 DD E1         [14]  555 	pop	ix
   5DB6 C9            [10]  556 	ret
                            557 ;src/entities/player.c:105: void playerrender(const Player* player) {
                            558 ;	---------------------------------
                            559 ; Function playerrender
                            560 ; ---------------------------------
   5DB7                     561 _playerrender::
   5DB7 DD E5         [15]  562 	push	ix
   5DB9 DD 21 00 00   [14]  563 	ld	ix,#0
   5DBD DD 39         [15]  564 	add	ix,sp
   5DBF 3B            [ 6]  565 	dec	sp
                            566 ;src/entities/player.c:108: if (!player) {
   5DC0 DD 7E 05      [19]  567 	ld	a, 5 (ix)
   5DC3 DD B6 04      [19]  568 	or	a,4 (ix)
                            569 ;src/entities/player.c:109: return;
   5DC6 28 38         [12]  570 	jr	Z,00103$
                            571 ;src/entities/player.c:112: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5DC8 DD 5E 04      [19]  572 	ld	e,4 (ix)
   5DCB DD 56 05      [19]  573 	ld	d,5 (ix)
   5DCE 6B            [ 4]  574 	ld	l, e
   5DCF 62            [ 4]  575 	ld	h, d
   5DD0 23            [ 6]  576 	inc	hl
   5DD1 46            [ 7]  577 	ld	b, (hl)
   5DD2 1A            [ 7]  578 	ld	a, (de)
   5DD3 D5            [11]  579 	push	de
   5DD4 C5            [11]  580 	push	bc
   5DD5 33            [ 6]  581 	inc	sp
   5DD6 F5            [11]  582 	push	af
   5DD7 33            [ 6]  583 	inc	sp
   5DD8 21 00 C0      [10]  584 	ld	hl, #0xc000
   5DDB E5            [11]  585 	push	hl
   5DDC CD CE 62      [17]  586 	call	_cpct_getScreenPtr
   5DDF 4D            [ 4]  587 	ld	c, l
   5DE0 44            [ 4]  588 	ld	b, h
   5DE1 D1            [10]  589 	pop	de
                            590 ;src/entities/player.c:113: cpct_drawSprite((u8*)player_sprite, pvmem, player->w, player->h);
   5DE2 D5            [11]  591 	push	de
   5DE3 FD E1         [14]  592 	pop	iy
   5DE5 FD 7E 05      [19]  593 	ld	a, 5 (iy)
   5DE8 DD 77 FF      [19]  594 	ld	-1 (ix), a
   5DEB EB            [ 4]  595 	ex	de,hl
   5DEC 11 04 00      [10]  596 	ld	de, #0x0004
   5DEF 19            [11]  597 	add	hl, de
   5DF0 56            [ 7]  598 	ld	d, (hl)
   5DF1 DD 7E FF      [19]  599 	ld	a, -1 (ix)
   5DF4 F5            [11]  600 	push	af
   5DF5 33            [ 6]  601 	inc	sp
   5DF6 D5            [11]  602 	push	de
   5DF7 33            [ 6]  603 	inc	sp
   5DF8 C5            [11]  604 	push	bc
   5DF9 21 40 5B      [10]  605 	ld	hl, #_player_sprite
   5DFC E5            [11]  606 	push	hl
   5DFD CD FF 60      [17]  607 	call	_cpct_drawSprite
   5E00                     608 00103$:
   5E00 33            [ 6]  609 	inc	sp
   5E01 DD E1         [14]  610 	pop	ix
   5E03 C9            [10]  611 	ret
                            612 ;src/entities/player.c:116: u8 player_get_health(const Player* player) {
                            613 ;	---------------------------------
                            614 ; Function player_get_health
                            615 ; ---------------------------------
   5E04                     616 _player_get_health::
                            617 ;src/entities/player.c:117: return player ? player->health : 0;
   5E04 21 03 00      [10]  618 	ld	hl, #2+1
   5E07 39            [11]  619 	add	hl, sp
   5E08 7E            [ 7]  620 	ld	a, (hl)
   5E09 2B            [ 6]  621 	dec	hl
   5E0A B6            [ 7]  622 	or	a,(hl)
   5E0B 28 0A         [12]  623 	jr	Z,00103$
   5E0D C1            [10]  624 	pop	bc
   5E0E E1            [10]  625 	pop	hl
   5E0F E5            [11]  626 	push	hl
   5E10 C5            [11]  627 	push	bc
   5E11 11 06 00      [10]  628 	ld	de, #0x0006
   5E14 19            [11]  629 	add	hl, de
   5E15 6E            [ 7]  630 	ld	l, (hl)
   5E16 C9            [10]  631 	ret
   5E17                     632 00103$:
   5E17 2E 00         [ 7]  633 	ld	l, #0x00
   5E19 C9            [10]  634 	ret
                            635 ;src/entities/player.c:120: u8 player_get_weapon(const Player* player) {
                            636 ;	---------------------------------
                            637 ; Function player_get_weapon
                            638 ; ---------------------------------
   5E1A                     639 _player_get_weapon::
                            640 ;src/entities/player.c:121: return player ? player->weapon : 0;
   5E1A 21 03 00      [10]  641 	ld	hl, #2+1
   5E1D 39            [11]  642 	add	hl, sp
   5E1E 7E            [ 7]  643 	ld	a, (hl)
   5E1F 2B            [ 6]  644 	dec	hl
   5E20 B6            [ 7]  645 	or	a,(hl)
   5E21 28 0A         [12]  646 	jr	Z,00103$
   5E23 C1            [10]  647 	pop	bc
   5E24 E1            [10]  648 	pop	hl
   5E25 E5            [11]  649 	push	hl
   5E26 C5            [11]  650 	push	bc
   5E27 11 07 00      [10]  651 	ld	de, #0x0007
   5E2A 19            [11]  652 	add	hl, de
   5E2B 6E            [ 7]  653 	ld	l, (hl)
   5E2C C9            [10]  654 	ret
   5E2D                     655 00103$:
   5E2D 2E 00         [ 7]  656 	ld	l, #0x00
   5E2F C9            [10]  657 	ret
                            658 	.area _CODE
                            659 	.area _INITIALIZER
                            660 	.area _CABS (ABS)
