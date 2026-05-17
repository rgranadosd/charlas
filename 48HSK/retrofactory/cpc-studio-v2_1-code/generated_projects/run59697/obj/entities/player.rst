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
   5B93 CA C7 5D      [10]  200 	jp	Z,00141$
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
   5BA6 DD 77 FE      [19]  213 	ld	-2 (ix), a
   5BA9 78            [ 4]  214 	ld	a, b
   5BAA CE 00         [ 7]  215 	adc	a, #0x00
   5BAC DD 77 FF      [19]  216 	ld	-1 (ix), a
                            217 ;src/entities/player.c:52: if (input_is_left_pressed()) {
   5BAF 7D            [ 4]  218 	ld	a, l
   5BB0 B7            [ 4]  219 	or	a, a
   5BB1 28 0E         [12]  220 	jr	Z,00116$
                            221 ;src/entities/player.c:53: player->vx = (i8)(player->vx - kplayeracceleration);
   5BB3 1A            [ 7]  222 	ld	a, (de)
   5BB4 C6 FF         [ 7]  223 	add	a, #0xff
   5BB6 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/player.c:54: player->facing_left = 1;
   5BB7 DD 6E FE      [19]  226 	ld	l,-2 (ix)
   5BBA DD 66 FF      [19]  227 	ld	h,-1 (ix)
   5BBD 36 01         [10]  228 	ld	(hl), #0x01
   5BBF 18 55         [12]  229 	jr	00117$
   5BC1                     230 00116$:
                            231 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5BC1 C5            [11]  232 	push	bc
   5BC2 D5            [11]  233 	push	de
   5BC3 CD 10 51      [17]  234 	call	_input_is_right_pressed
   5BC6 DD 75 FD      [19]  235 	ld	-3 (ix), l
   5BC9 D1            [10]  236 	pop	de
   5BCA C1            [10]  237 	pop	bc
                            238 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5BCB 1A            [ 7]  239 	ld	a, (de)
                            240 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5BCC 6F            [ 4]  241 	ld	l,a
   5BCD 3C            [ 4]  242 	inc	a
   5BCE DD 77 FC      [19]  243 	ld	-4 (ix), a
                            244 ;src/entities/player.c:55: } else if (input_is_right_pressed()) {
   5BD1 DD 7E FD      [19]  245 	ld	a, -3 (ix)
   5BD4 B7            [ 4]  246 	or	a, a
   5BD5 28 0E         [12]  247 	jr	Z,00113$
                            248 ;src/entities/player.c:56: player->vx = (i8)(player->vx + kplayeracceleration);
   5BD7 DD 7E FC      [19]  249 	ld	a, -4 (ix)
   5BDA 12            [ 7]  250 	ld	(de), a
                            251 ;src/entities/player.c:57: player->facing_left = 0;
   5BDB DD 6E FE      [19]  252 	ld	l,-2 (ix)
   5BDE DD 66 FF      [19]  253 	ld	h,-1 (ix)
   5BE1 36 00         [10]  254 	ld	(hl), #0x00
   5BE3 18 31         [12]  255 	jr	00117$
   5BE5                     256 00113$:
                            257 ;src/entities/player.c:58: } else if (player->vx > 0) {
   5BE5 AF            [ 4]  258 	xor	a, a
   5BE6 95            [ 4]  259 	sub	a, l
   5BE7 E2 EC 5B      [10]  260 	jp	PO, 00223$
   5BEA EE 80         [ 7]  261 	xor	a, #0x80
   5BEC                     262 00223$:
   5BEC F2 00 5C      [10]  263 	jp	P, 00110$
                            264 ;src/entities/player.c:59: player->vx = (i8)(player->vx - kplayerdeceleration);
   5BEF 7D            [ 4]  265 	ld	a, l
   5BF0 C6 FF         [ 7]  266 	add	a, #0xff
   5BF2 DD 77 FD      [19]  267 	ld	-3 (ix), a
   5BF5 12            [ 7]  268 	ld	(de),a
                            269 ;src/entities/player.c:60: if (player->vx < 0) player->vx = 0;
   5BF6 DD CB FD 7E   [20]  270 	bit	7, -3 (ix)
   5BFA 28 1A         [12]  271 	jr	Z,00117$
   5BFC AF            [ 4]  272 	xor	a, a
   5BFD 12            [ 7]  273 	ld	(de), a
   5BFE 18 16         [12]  274 	jr	00117$
   5C00                     275 00110$:
                            276 ;src/entities/player.c:61: } else if (player->vx < 0) {
   5C00 CB 7D         [ 8]  277 	bit	7, l
   5C02 28 12         [12]  278 	jr	Z,00117$
                            279 ;src/entities/player.c:62: player->vx = (i8)(player->vx + kplayerdeceleration);
   5C04 DD 7E FC      [19]  280 	ld	a, -4 (ix)
   5C07 12            [ 7]  281 	ld	(de), a
                            282 ;src/entities/player.c:63: if (player->vx > 0) player->vx = 0;
   5C08 AF            [ 4]  283 	xor	a, a
   5C09 DD 96 FC      [19]  284 	sub	a, -4 (ix)
   5C0C E2 11 5C      [10]  285 	jp	PO, 00224$
   5C0F EE 80         [ 7]  286 	xor	a, #0x80
   5C11                     287 00224$:
   5C11 F2 16 5C      [10]  288 	jp	P, 00117$
   5C14 AF            [ 4]  289 	xor	a, a
   5C15 12            [ 7]  290 	ld	(de), a
   5C16                     291 00117$:
                            292 ;src/entities/player.c:66: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5C16 1A            [ 7]  293 	ld	a, (de)
   5C17 6F            [ 4]  294 	ld	l, a
   5C18 3E 03         [ 7]  295 	ld	a, #0x03
   5C1A 95            [ 4]  296 	sub	a, l
   5C1B E2 20 5C      [10]  297 	jp	PO, 00225$
   5C1E EE 80         [ 7]  298 	xor	a, #0x80
   5C20                     299 00225$:
   5C20 F2 26 5C      [10]  300 	jp	P, 00119$
   5C23 3E 03         [ 7]  301 	ld	a, #0x03
   5C25 12            [ 7]  302 	ld	(de), a
   5C26                     303 00119$:
                            304 ;src/entities/player.c:67: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5C26 1A            [ 7]  305 	ld	a, (de)
   5C27 EE 80         [ 7]  306 	xor	a, #0x80
   5C29 D6 7D         [ 7]  307 	sub	a, #0x7d
   5C2B 30 03         [12]  308 	jr	NC,00121$
   5C2D 3E FD         [ 7]  309 	ld	a, #0xfd
   5C2F 12            [ 7]  310 	ld	(de), a
   5C30                     311 00121$:
                            312 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5C30 C5            [11]  313 	push	bc
   5C31 D5            [11]  314 	push	de
   5C32 CD 30 51      [17]  315 	call	_input_is_jump_just_pressed
   5C35 DD 75 FC      [19]  316 	ld	-4 (ix), l
   5C38 D1            [10]  317 	pop	de
   5C39 C1            [10]  318 	pop	bc
   5C3A 21 05 00      [10]  319 	ld	hl, #0x0005
   5C3D 09            [11]  320 	add	hl,bc
   5C3E DD 75 FE      [19]  321 	ld	-2 (ix), l
   5C41 DD 74 FF      [19]  322 	ld	-1 (ix), h
   5C44 21 01 00      [10]  323 	ld	hl, #0x0001
   5C47 09            [11]  324 	add	hl,bc
   5C48 DD 75 FA      [19]  325 	ld	-6 (ix), l
   5C4B DD 74 FB      [19]  326 	ld	-5 (ix), h
                            327 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   5C4E 21 03 00      [10]  328 	ld	hl, #0x0003
   5C51 09            [11]  329 	add	hl,bc
   5C52 DD 75 F8      [19]  330 	ld	-8 (ix), l
   5C55 DD 74 F9      [19]  331 	ld	-7 (ix), h
                            332 ;src/entities/player.c:71: player->jump_hold = 5;
   5C58 21 09 00      [10]  333 	ld	hl, #0x0009
   5C5B 09            [11]  334 	add	hl,bc
   5C5C DD 75 F6      [19]  335 	ld	-10 (ix), l
   5C5F DD 74 F7      [19]  336 	ld	-9 (ix), h
                            337 ;src/entities/player.c:69: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5C62 DD 7E FC      [19]  338 	ld	a, -4 (ix)
   5C65 B7            [ 4]  339 	or	a, a
   5C66 28 4E         [12]  340 	jr	Z,00123$
   5C68 DD 6E FE      [19]  341 	ld	l,-2 (ix)
   5C6B DD 66 FF      [19]  342 	ld	h,-1 (ix)
   5C6E 7E            [ 7]  343 	ld	a, (hl)
   5C6F DD 6E FA      [19]  344 	ld	l,-6 (ix)
   5C72 DD 66 FB      [19]  345 	ld	h,-5 (ix)
   5C75 6E            [ 7]  346 	ld	l, (hl)
   5C76 DD 75 F4      [19]  347 	ld	-12 (ix), l
   5C79 DD 36 F5 00   [19]  348 	ld	-11 (ix), #0x00
   5C7D F5            [11]  349 	push	af
   5C7E 0A            [ 7]  350 	ld	a, (bc)
   5C7F 6F            [ 4]  351 	ld	l, a
   5C80 F1            [10]  352 	pop	af
   5C81 DD 75 F2      [19]  353 	ld	-14 (ix), l
   5C84 DD 36 F3 00   [19]  354 	ld	-13 (ix), #0x00
   5C88 C5            [11]  355 	push	bc
   5C89 D5            [11]  356 	push	de
   5C8A F5            [11]  357 	push	af
   5C8B 33            [ 6]  358 	inc	sp
   5C8C DD 6E F4      [19]  359 	ld	l,-12 (ix)
   5C8F DD 66 F5      [19]  360 	ld	h,-11 (ix)
   5C92 E5            [11]  361 	push	hl
   5C93 DD 6E F2      [19]  362 	ld	l,-14 (ix)
   5C96 DD 66 F3      [19]  363 	ld	h,-13 (ix)
   5C99 E5            [11]  364 	push	hl
   5C9A CD C3 4B      [17]  365 	call	_collision_is_on_ground_at
   5C9D F1            [10]  366 	pop	af
   5C9E F1            [10]  367 	pop	af
   5C9F 33            [ 6]  368 	inc	sp
   5CA0 D1            [10]  369 	pop	de
   5CA1 C1            [10]  370 	pop	bc
   5CA2 7D            [ 4]  371 	ld	a, l
   5CA3 B7            [ 4]  372 	or	a, a
   5CA4 28 10         [12]  373 	jr	Z,00123$
                            374 ;src/entities/player.c:70: player->vy = kplayerjumpvelocity;
   5CA6 DD 6E F8      [19]  375 	ld	l,-8 (ix)
   5CA9 DD 66 F9      [19]  376 	ld	h,-7 (ix)
   5CAC 36 FA         [10]  377 	ld	(hl), #0xfa
                            378 ;src/entities/player.c:71: player->jump_hold = 5;
   5CAE DD 6E F6      [19]  379 	ld	l,-10 (ix)
   5CB1 DD 66 F7      [19]  380 	ld	h,-9 (ix)
   5CB4 36 05         [10]  381 	ld	(hl), #0x05
   5CB6                     382 00123$:
                            383 ;src/entities/player.c:74: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5CB6 C5            [11]  384 	push	bc
   5CB7 D5            [11]  385 	push	de
   5CB8 CD 28 51      [17]  386 	call	_input_is_jump_pressed
   5CBB 7D            [ 4]  387 	ld	a, l
   5CBC D1            [10]  388 	pop	de
   5CBD C1            [10]  389 	pop	bc
   5CBE B7            [ 4]  390 	or	a, a
   5CBF 28 31         [12]  391 	jr	Z,00126$
   5CC1 DD 6E F6      [19]  392 	ld	l,-10 (ix)
   5CC4 DD 66 F7      [19]  393 	ld	h,-9 (ix)
   5CC7 7E            [ 7]  394 	ld	a, (hl)
   5CC8 B7            [ 4]  395 	or	a, a
   5CC9 28 27         [12]  396 	jr	Z,00126$
   5CCB DD 6E F8      [19]  397 	ld	l,-8 (ix)
   5CCE DD 66 F9      [19]  398 	ld	h,-7 (ix)
   5CD1 6E            [ 7]  399 	ld	l, (hl)
   5CD2 CB 7D         [ 8]  400 	bit	7, l
   5CD4 28 1C         [12]  401 	jr	Z,00126$
                            402 ;src/entities/player.c:75: player->vy = (i8)(player->vy + kplayerjumpboost);
   5CD6 7D            [ 4]  403 	ld	a, l
   5CD7 C6 FF         [ 7]  404 	add	a, #0xff
   5CD9 DD 6E F8      [19]  405 	ld	l,-8 (ix)
   5CDC DD 66 F9      [19]  406 	ld	h,-7 (ix)
   5CDF 77            [ 7]  407 	ld	(hl), a
                            408 ;src/entities/player.c:76: player->jump_hold--;
   5CE0 DD 6E F6      [19]  409 	ld	l,-10 (ix)
   5CE3 DD 66 F7      [19]  410 	ld	h,-9 (ix)
   5CE6 7E            [ 7]  411 	ld	a, (hl)
   5CE7 C6 FF         [ 7]  412 	add	a, #0xff
   5CE9 DD 6E F6      [19]  413 	ld	l,-10 (ix)
   5CEC DD 66 F7      [19]  414 	ld	h,-9 (ix)
   5CEF 77            [ 7]  415 	ld	(hl), a
   5CF0 18 08         [12]  416 	jr	00127$
   5CF2                     417 00126$:
                            418 ;src/entities/player.c:78: player->jump_hold = 0;
   5CF2 DD 6E F6      [19]  419 	ld	l,-10 (ix)
   5CF5 DD 66 F7      [19]  420 	ld	h,-9 (ix)
   5CF8 36 00         [10]  421 	ld	(hl), #0x00
   5CFA                     422 00127$:
                            423 ;src/entities/player.c:81: player->vy = (i8)(player->vy + kplayergravity);
   5CFA DD 6E F8      [19]  424 	ld	l,-8 (ix)
   5CFD DD 66 F9      [19]  425 	ld	h,-7 (ix)
   5D00 7E            [ 7]  426 	ld	a, (hl)
   5D01 3C            [ 4]  427 	inc	a
   5D02 DD 77 F2      [19]  428 	ld	-14 (ix), a
   5D05 DD 6E F8      [19]  429 	ld	l,-8 (ix)
   5D08 DD 66 F9      [19]  430 	ld	h,-7 (ix)
   5D0B DD 7E F2      [19]  431 	ld	a, -14 (ix)
   5D0E 77            [ 7]  432 	ld	(hl), a
                            433 ;src/entities/player.c:82: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5D0F 3E 04         [ 7]  434 	ld	a, #0x04
   5D11 DD 96 F2      [19]  435 	sub	a, -14 (ix)
   5D14 E2 19 5D      [10]  436 	jp	PO, 00226$
   5D17 EE 80         [ 7]  437 	xor	a, #0x80
   5D19                     438 00226$:
   5D19 F2 24 5D      [10]  439 	jp	P, 00131$
   5D1C DD 6E F8      [19]  440 	ld	l,-8 (ix)
   5D1F DD 66 F9      [19]  441 	ld	h,-7 (ix)
   5D22 36 04         [10]  442 	ld	(hl), #0x04
   5D24                     443 00131$:
                            444 ;src/entities/player.c:84: nextx = (i16)player->x + (i16)player->vx;
   5D24 0A            [ 7]  445 	ld	a, (bc)
   5D25 DD 77 F2      [19]  446 	ld	-14 (ix), a
   5D28 DD 36 F3 00   [19]  447 	ld	-13 (ix), #0x00
   5D2C 1A            [ 7]  448 	ld	a, (de)
   5D2D 5F            [ 4]  449 	ld	e, a
   5D2E 17            [ 4]  450 	rla
   5D2F 9F            [ 4]  451 	sbc	a, a
   5D30 57            [ 4]  452 	ld	d, a
   5D31 E1            [10]  453 	pop	hl
   5D32 E5            [11]  454 	push	hl
   5D33 19            [11]  455 	add	hl, de
                            456 ;src/entities/player.c:85: if (nextx < 0) {
   5D34 CB 7C         [ 8]  457 	bit	7, h
   5D36 28 03         [12]  458 	jr	Z,00133$
                            459 ;src/entities/player.c:86: nextx = 0;
   5D38 21 00 00      [10]  460 	ld	hl, #0x0000
   5D3B                     461 00133$:
                            462 ;src/entities/player.c:88: if (nextx > 76) {
   5D3B 3E 4C         [ 7]  463 	ld	a, #0x4c
   5D3D BD            [ 4]  464 	cp	a, l
   5D3E 3E 00         [ 7]  465 	ld	a, #0x00
   5D40 9C            [ 4]  466 	sbc	a, h
   5D41 E2 46 5D      [10]  467 	jp	PO, 00227$
   5D44 EE 80         [ 7]  468 	xor	a, #0x80
   5D46                     469 00227$:
   5D46 F2 4C 5D      [10]  470 	jp	P, 00135$
                            471 ;src/entities/player.c:89: nextx = 76;
   5D49 21 4C 00      [10]  472 	ld	hl, #0x004c
   5D4C                     473 00135$:
                            474 ;src/entities/player.c:91: player->x = (u8)nextx;
   5D4C DD 75 F2      [19]  475 	ld	-14 (ix), l
   5D4F 7D            [ 4]  476 	ld	a, l
   5D50 02            [ 7]  477 	ld	(bc), a
                            478 ;src/entities/player.c:93: nexty = (i16)player->y + (i16)player->vy;
   5D51 DD 6E FA      [19]  479 	ld	l,-6 (ix)
   5D54 DD 66 FB      [19]  480 	ld	h,-5 (ix)
   5D57 5E            [ 7]  481 	ld	e, (hl)
   5D58 16 00         [ 7]  482 	ld	d, #0x00
   5D5A DD 6E F8      [19]  483 	ld	l,-8 (ix)
   5D5D DD 66 F9      [19]  484 	ld	h,-7 (ix)
   5D60 6E            [ 7]  485 	ld	l, (hl)
   5D61 7D            [ 4]  486 	ld	a, l
   5D62 17            [ 4]  487 	rla
   5D63 9F            [ 4]  488 	sbc	a, a
   5D64 67            [ 4]  489 	ld	h, a
   5D65 19            [11]  490 	add	hl, de
   5D66 E5            [11]  491 	push	hl
   5D67 FD E1         [14]  492 	pop	iy
                            493 ;src/entities/player.c:94: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5D69 DD 6E FE      [19]  494 	ld	l,-2 (ix)
   5D6C DD 66 FF      [19]  495 	ld	h,-1 (ix)
   5D6F 66            [ 7]  496 	ld	h, (hl)
   5D70 DD 5E F2      [19]  497 	ld	e, -14 (ix)
   5D73 16 00         [ 7]  498 	ld	d, #0x00
   5D75 C5            [11]  499 	push	bc
   5D76 E5            [11]  500 	push	hl
   5D77 33            [ 6]  501 	inc	sp
   5D78 FD E5         [15]  502 	push	iy
   5D7A D5            [11]  503 	push	de
   5D7B CD 42 4C      [17]  504 	call	_collision_clamp_y_at
   5D7E F1            [10]  505 	pop	af
   5D7F F1            [10]  506 	pop	af
   5D80 33            [ 6]  507 	inc	sp
   5D81 C1            [10]  508 	pop	bc
                            509 ;src/entities/player.c:95: if (nexty < 0) {
   5D82 CB 7C         [ 8]  510 	bit	7, h
   5D84 28 03         [12]  511 	jr	Z,00137$
                            512 ;src/entities/player.c:96: nexty = 0;
   5D86 21 00 00      [10]  513 	ld	hl, #0x0000
   5D89                     514 00137$:
                            515 ;src/entities/player.c:98: player->y = (u8)nexty;
   5D89 5D            [ 4]  516 	ld	e, l
   5D8A DD 6E FA      [19]  517 	ld	l,-6 (ix)
   5D8D DD 66 FB      [19]  518 	ld	h,-5 (ix)
   5D90 73            [ 7]  519 	ld	(hl), e
                            520 ;src/entities/player.c:100: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5D91 DD 6E FE      [19]  521 	ld	l,-2 (ix)
   5D94 DD 66 FF      [19]  522 	ld	h,-1 (ix)
   5D97 7E            [ 7]  523 	ld	a, (hl)
   5D98 16 00         [ 7]  524 	ld	d, #0x00
   5D9A F5            [11]  525 	push	af
   5D9B 0A            [ 7]  526 	ld	a, (bc)
   5D9C 4F            [ 4]  527 	ld	c, a
   5D9D F1            [10]  528 	pop	af
   5D9E 06 00         [ 7]  529 	ld	b, #0x00
   5DA0 F5            [11]  530 	push	af
   5DA1 33            [ 6]  531 	inc	sp
   5DA2 D5            [11]  532 	push	de
   5DA3 C5            [11]  533 	push	bc
   5DA4 CD C3 4B      [17]  534 	call	_collision_is_on_ground_at
   5DA7 F1            [10]  535 	pop	af
   5DA8 F1            [10]  536 	pop	af
   5DA9 33            [ 6]  537 	inc	sp
   5DAA 7D            [ 4]  538 	ld	a, l
   5DAB B7            [ 4]  539 	or	a, a
   5DAC 28 19         [12]  540 	jr	Z,00141$
   5DAE DD 6E F8      [19]  541 	ld	l,-8 (ix)
   5DB1 DD 66 F9      [19]  542 	ld	h,-7 (ix)
   5DB4 4E            [ 7]  543 	ld	c, (hl)
   5DB5 AF            [ 4]  544 	xor	a, a
   5DB6 91            [ 4]  545 	sub	a, c
   5DB7 E2 BC 5D      [10]  546 	jp	PO, 00228$
   5DBA EE 80         [ 7]  547 	xor	a, #0x80
   5DBC                     548 00228$:
   5DBC F2 C7 5D      [10]  549 	jp	P, 00141$
                            550 ;src/entities/player.c:101: player->vy = 0;
   5DBF DD 6E F8      [19]  551 	ld	l,-8 (ix)
   5DC2 DD 66 F9      [19]  552 	ld	h,-7 (ix)
   5DC5 36 00         [10]  553 	ld	(hl), #0x00
   5DC7                     554 00141$:
   5DC7 DD F9         [10]  555 	ld	sp, ix
   5DC9 DD E1         [14]  556 	pop	ix
   5DCB C9            [10]  557 	ret
                            558 ;src/entities/player.c:105: void playerrender(const Player* player) {
                            559 ;	---------------------------------
                            560 ; Function playerrender
                            561 ; ---------------------------------
   5DCC                     562 _playerrender::
   5DCC DD E5         [15]  563 	push	ix
   5DCE DD 21 00 00   [14]  564 	ld	ix,#0
   5DD2 DD 39         [15]  565 	add	ix,sp
   5DD4 3B            [ 6]  566 	dec	sp
                            567 ;src/entities/player.c:108: if (!player) {
   5DD5 DD 7E 05      [19]  568 	ld	a, 5 (ix)
   5DD8 DD B6 04      [19]  569 	or	a,4 (ix)
                            570 ;src/entities/player.c:109: return;
   5DDB 28 38         [12]  571 	jr	Z,00103$
                            572 ;src/entities/player.c:112: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5DDD DD 5E 04      [19]  573 	ld	e,4 (ix)
   5DE0 DD 56 05      [19]  574 	ld	d,5 (ix)
   5DE3 6B            [ 4]  575 	ld	l, e
   5DE4 62            [ 4]  576 	ld	h, d
   5DE5 23            [ 6]  577 	inc	hl
   5DE6 46            [ 7]  578 	ld	b, (hl)
   5DE7 1A            [ 7]  579 	ld	a, (de)
   5DE8 D5            [11]  580 	push	de
   5DE9 C5            [11]  581 	push	bc
   5DEA 33            [ 6]  582 	inc	sp
   5DEB F5            [11]  583 	push	af
   5DEC 33            [ 6]  584 	inc	sp
   5DED 21 00 C0      [10]  585 	ld	hl, #0xc000
   5DF0 E5            [11]  586 	push	hl
   5DF1 CD EA 62      [17]  587 	call	_cpct_getScreenPtr
   5DF4 4D            [ 4]  588 	ld	c, l
   5DF5 44            [ 4]  589 	ld	b, h
   5DF6 D1            [10]  590 	pop	de
                            591 ;src/entities/player.c:113: cpct_drawSprite((u8*)player_sprite, pvmem, player->w, player->h);
   5DF7 D5            [11]  592 	push	de
   5DF8 FD E1         [14]  593 	pop	iy
   5DFA FD 7E 05      [19]  594 	ld	a, 5 (iy)
   5DFD DD 77 FF      [19]  595 	ld	-1 (ix), a
   5E00 EB            [ 4]  596 	ex	de,hl
   5E01 11 04 00      [10]  597 	ld	de, #0x0004
   5E04 19            [11]  598 	add	hl, de
   5E05 56            [ 7]  599 	ld	d, (hl)
   5E06 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   5E09 F5            [11]  601 	push	af
   5E0A 33            [ 6]  602 	inc	sp
   5E0B D5            [11]  603 	push	de
   5E0C 33            [ 6]  604 	inc	sp
   5E0D C5            [11]  605 	push	bc
   5E0E 21 40 5B      [10]  606 	ld	hl, #_player_sprite
   5E11 E5            [11]  607 	push	hl
   5E12 CD 1B 61      [17]  608 	call	_cpct_drawSprite
   5E15                     609 00103$:
   5E15 33            [ 6]  610 	inc	sp
   5E16 DD E1         [14]  611 	pop	ix
   5E18 C9            [10]  612 	ret
                            613 ;src/entities/player.c:116: u8 player_get_health(const Player* player) {
                            614 ;	---------------------------------
                            615 ; Function player_get_health
                            616 ; ---------------------------------
   5E19                     617 _player_get_health::
                            618 ;src/entities/player.c:117: return player ? player->health : 0;
   5E19 21 03 00      [10]  619 	ld	hl, #2+1
   5E1C 39            [11]  620 	add	hl, sp
   5E1D 7E            [ 7]  621 	ld	a, (hl)
   5E1E 2B            [ 6]  622 	dec	hl
   5E1F B6            [ 7]  623 	or	a,(hl)
   5E20 28 0A         [12]  624 	jr	Z,00103$
   5E22 C1            [10]  625 	pop	bc
   5E23 E1            [10]  626 	pop	hl
   5E24 E5            [11]  627 	push	hl
   5E25 C5            [11]  628 	push	bc
   5E26 11 06 00      [10]  629 	ld	de, #0x0006
   5E29 19            [11]  630 	add	hl, de
   5E2A 6E            [ 7]  631 	ld	l, (hl)
   5E2B C9            [10]  632 	ret
   5E2C                     633 00103$:
   5E2C 2E 00         [ 7]  634 	ld	l, #0x00
   5E2E C9            [10]  635 	ret
                            636 ;src/entities/player.c:120: u8 player_get_weapon(const Player* player) {
                            637 ;	---------------------------------
                            638 ; Function player_get_weapon
                            639 ; ---------------------------------
   5E2F                     640 _player_get_weapon::
                            641 ;src/entities/player.c:121: return player ? player->weapon : 0;
   5E2F 21 03 00      [10]  642 	ld	hl, #2+1
   5E32 39            [11]  643 	add	hl, sp
   5E33 7E            [ 7]  644 	ld	a, (hl)
   5E34 2B            [ 6]  645 	dec	hl
   5E35 B6            [ 7]  646 	or	a,(hl)
   5E36 28 0A         [12]  647 	jr	Z,00103$
   5E38 C1            [10]  648 	pop	bc
   5E39 E1            [10]  649 	pop	hl
   5E3A E5            [11]  650 	push	hl
   5E3B C5            [11]  651 	push	bc
   5E3C 11 07 00      [10]  652 	ld	de, #0x0007
   5E3F 19            [11]  653 	add	hl, de
   5E40 6E            [ 7]  654 	ld	l, (hl)
   5E41 C9            [10]  655 	ret
   5E42                     656 00103$:
   5E42 2E 00         [ 7]  657 	ld	l, #0x00
   5E44 C9            [10]  658 	ret
                            659 	.area _CODE
                            660 	.area _INITIALIZER
                            661 	.area _CABS (ABS)
