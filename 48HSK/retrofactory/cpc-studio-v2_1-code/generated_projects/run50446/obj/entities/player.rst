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
   5B98                      59 _playerinit::
                             60 ;src/entities/player.c:18: if (!player) {
   5B98 21 03 00      [10]   61 	ld	hl, #2+1
   5B9B 39            [11]   62 	add	hl, sp
   5B9C 7E            [ 7]   63 	ld	a, (hl)
   5B9D 2B            [ 6]   64 	dec	hl
   5B9E B6            [ 7]   65 	or	a,(hl)
                             66 ;src/entities/player.c:19: return;
   5B9F C8            [11]   67 	ret	Z
                             68 ;src/entities/player.c:22: player->x = 20;
   5BA0 D1            [10]   69 	pop	de
   5BA1 C1            [10]   70 	pop	bc
   5BA2 C5            [11]   71 	push	bc
   5BA3 D5            [11]   72 	push	de
   5BA4 3E 14         [ 7]   73 	ld	a, #0x14
   5BA6 02            [ 7]   74 	ld	(bc), a
                             75 ;src/entities/player.c:23: player->y = 120;
   5BA7 69            [ 4]   76 	ld	l, c
   5BA8 60            [ 4]   77 	ld	h, b
   5BA9 23            [ 6]   78 	inc	hl
   5BAA 36 78         [10]   79 	ld	(hl), #0x78
                             80 ;src/entities/player.c:24: player->vx = 0;
   5BAC 59            [ 4]   81 	ld	e, c
   5BAD 50            [ 4]   82 	ld	d, b
   5BAE 13            [ 6]   83 	inc	de
   5BAF 13            [ 6]   84 	inc	de
   5BB0 AF            [ 4]   85 	xor	a, a
   5BB1 12            [ 7]   86 	ld	(de), a
                             87 ;src/entities/player.c:25: player->vy = 0;
   5BB2 59            [ 4]   88 	ld	e, c
   5BB3 50            [ 4]   89 	ld	d, b
   5BB4 13            [ 6]   90 	inc	de
   5BB5 13            [ 6]   91 	inc	de
   5BB6 13            [ 6]   92 	inc	de
   5BB7 AF            [ 4]   93 	xor	a, a
   5BB8 12            [ 7]   94 	ld	(de), a
                             95 ;src/entities/player.c:26: player->w = 4;
   5BB9 21 04 00      [10]   96 	ld	hl, #0x0004
   5BBC 09            [11]   97 	add	hl, bc
   5BBD 36 04         [10]   98 	ld	(hl), #0x04
                             99 ;src/entities/player.c:27: player->h = 16;
   5BBF 21 05 00      [10]  100 	ld	hl, #0x0005
   5BC2 09            [11]  101 	add	hl, bc
   5BC3 36 10         [10]  102 	ld	(hl), #0x10
                            103 ;src/entities/player.c:28: player->health = 3;
   5BC5 21 06 00      [10]  104 	ld	hl, #0x0006
   5BC8 09            [11]  105 	add	hl, bc
   5BC9 36 03         [10]  106 	ld	(hl), #0x03
                            107 ;src/entities/player.c:29: player->weapon = 0;
   5BCB 21 07 00      [10]  108 	ld	hl, #0x0007
   5BCE 09            [11]  109 	add	hl, bc
   5BCF 36 00         [10]  110 	ld	(hl), #0x00
                            111 ;src/entities/player.c:30: player->facing_left = 0;
   5BD1 21 08 00      [10]  112 	ld	hl, #0x0008
   5BD4 09            [11]  113 	add	hl, bc
   5BD5 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/player.c:31: player->jump_hold = 0;
   5BD7 21 09 00      [10]  116 	ld	hl, #0x0009
   5BDA 09            [11]  117 	add	hl, bc
   5BDB 36 00         [10]  118 	ld	(hl), #0x00
   5BDD C9            [10]  119 	ret
                            120 ;src/entities/player.c:34: void playerupdate(Player* player) {
                            121 ;	---------------------------------
                            122 ; Function playerupdate
                            123 ; ---------------------------------
   5BDE                     124 _playerupdate::
   5BDE DD E5         [15]  125 	push	ix
   5BE0 DD 21 00 00   [14]  126 	ld	ix,#0
   5BE4 DD 39         [15]  127 	add	ix,sp
   5BE6 21 F2 FF      [10]  128 	ld	hl, #-14
   5BE9 39            [11]  129 	add	hl, sp
   5BEA F9            [ 6]  130 	ld	sp, hl
                            131 ;src/entities/player.c:38: if (!player) {
   5BEB DD 7E 05      [19]  132 	ld	a, 5 (ix)
   5BEE DD B6 04      [19]  133 	or	a,4 (ix)
                            134 ;src/entities/player.c:39: return;
   5BF1 CA 25 5E      [10]  135 	jp	Z,00141$
                            136 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5BF4 CD E6 50      [17]  137 	call	_input_is_left_pressed
                            138 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5BF7 DD 4E 04      [19]  139 	ld	c,4 (ix)
   5BFA DD 46 05      [19]  140 	ld	b,5 (ix)
   5BFD 59            [ 4]  141 	ld	e, c
   5BFE 50            [ 4]  142 	ld	d, b
   5BFF 13            [ 6]  143 	inc	de
   5C00 13            [ 6]  144 	inc	de
                            145 ;src/entities/player.c:44: player->facing_left = 1;
   5C01 79            [ 4]  146 	ld	a, c
   5C02 C6 08         [ 7]  147 	add	a, #0x08
   5C04 DD 77 FE      [19]  148 	ld	-2 (ix), a
   5C07 78            [ 4]  149 	ld	a, b
   5C08 CE 00         [ 7]  150 	adc	a, #0x00
   5C0A DD 77 FF      [19]  151 	ld	-1 (ix), a
                            152 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5C0D 7D            [ 4]  153 	ld	a, l
   5C0E B7            [ 4]  154 	or	a, a
   5C0F 28 0E         [12]  155 	jr	Z,00116$
                            156 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5C11 1A            [ 7]  157 	ld	a, (de)
   5C12 C6 FF         [ 7]  158 	add	a, #0xff
   5C14 12            [ 7]  159 	ld	(de), a
                            160 ;src/entities/player.c:44: player->facing_left = 1;
   5C15 DD 6E FE      [19]  161 	ld	l,-2 (ix)
   5C18 DD 66 FF      [19]  162 	ld	h,-1 (ix)
   5C1B 36 01         [10]  163 	ld	(hl), #0x01
   5C1D 18 55         [12]  164 	jr	00117$
   5C1F                     165 00116$:
                            166 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5C1F C5            [11]  167 	push	bc
   5C20 D5            [11]  168 	push	de
   5C21 CD EE 50      [17]  169 	call	_input_is_right_pressed
   5C24 DD 75 FD      [19]  170 	ld	-3 (ix), l
   5C27 D1            [10]  171 	pop	de
   5C28 C1            [10]  172 	pop	bc
                            173 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5C29 1A            [ 7]  174 	ld	a, (de)
                            175 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5C2A 6F            [ 4]  176 	ld	l,a
   5C2B 3C            [ 4]  177 	inc	a
   5C2C DD 77 FC      [19]  178 	ld	-4 (ix), a
                            179 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5C2F DD 7E FD      [19]  180 	ld	a, -3 (ix)
   5C32 B7            [ 4]  181 	or	a, a
   5C33 28 0E         [12]  182 	jr	Z,00113$
                            183 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5C35 DD 7E FC      [19]  184 	ld	a, -4 (ix)
   5C38 12            [ 7]  185 	ld	(de), a
                            186 ;src/entities/player.c:47: player->facing_left = 0;
   5C39 DD 6E FE      [19]  187 	ld	l,-2 (ix)
   5C3C DD 66 FF      [19]  188 	ld	h,-1 (ix)
   5C3F 36 00         [10]  189 	ld	(hl), #0x00
   5C41 18 31         [12]  190 	jr	00117$
   5C43                     191 00113$:
                            192 ;src/entities/player.c:48: } else if (player->vx > 0) {
   5C43 AF            [ 4]  193 	xor	a, a
   5C44 95            [ 4]  194 	sub	a, l
   5C45 E2 4A 5C      [10]  195 	jp	PO, 00223$
   5C48 EE 80         [ 7]  196 	xor	a, #0x80
   5C4A                     197 00223$:
   5C4A F2 5E 5C      [10]  198 	jp	P, 00110$
                            199 ;src/entities/player.c:49: player->vx = (i8)(player->vx - kplayerdeceleration);
   5C4D 7D            [ 4]  200 	ld	a, l
   5C4E C6 FF         [ 7]  201 	add	a, #0xff
   5C50 DD 77 FD      [19]  202 	ld	-3 (ix), a
   5C53 12            [ 7]  203 	ld	(de),a
                            204 ;src/entities/player.c:50: if (player->vx < 0) player->vx = 0;
   5C54 DD CB FD 7E   [20]  205 	bit	7, -3 (ix)
   5C58 28 1A         [12]  206 	jr	Z,00117$
   5C5A AF            [ 4]  207 	xor	a, a
   5C5B 12            [ 7]  208 	ld	(de), a
   5C5C 18 16         [12]  209 	jr	00117$
   5C5E                     210 00110$:
                            211 ;src/entities/player.c:51: } else if (player->vx < 0) {
   5C5E CB 7D         [ 8]  212 	bit	7, l
   5C60 28 12         [12]  213 	jr	Z,00117$
                            214 ;src/entities/player.c:52: player->vx = (i8)(player->vx + kplayerdeceleration);
   5C62 DD 7E FC      [19]  215 	ld	a, -4 (ix)
   5C65 12            [ 7]  216 	ld	(de), a
                            217 ;src/entities/player.c:53: if (player->vx > 0) player->vx = 0;
   5C66 AF            [ 4]  218 	xor	a, a
   5C67 DD 96 FC      [19]  219 	sub	a, -4 (ix)
   5C6A E2 6F 5C      [10]  220 	jp	PO, 00224$
   5C6D EE 80         [ 7]  221 	xor	a, #0x80
   5C6F                     222 00224$:
   5C6F F2 74 5C      [10]  223 	jp	P, 00117$
   5C72 AF            [ 4]  224 	xor	a, a
   5C73 12            [ 7]  225 	ld	(de), a
   5C74                     226 00117$:
                            227 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5C74 1A            [ 7]  228 	ld	a, (de)
   5C75 6F            [ 4]  229 	ld	l, a
   5C76 3E 03         [ 7]  230 	ld	a, #0x03
   5C78 95            [ 4]  231 	sub	a, l
   5C79 E2 7E 5C      [10]  232 	jp	PO, 00225$
   5C7C EE 80         [ 7]  233 	xor	a, #0x80
   5C7E                     234 00225$:
   5C7E F2 84 5C      [10]  235 	jp	P, 00119$
   5C81 3E 03         [ 7]  236 	ld	a, #0x03
   5C83 12            [ 7]  237 	ld	(de), a
   5C84                     238 00119$:
                            239 ;src/entities/player.c:57: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5C84 1A            [ 7]  240 	ld	a, (de)
   5C85 EE 80         [ 7]  241 	xor	a, #0x80
   5C87 D6 7D         [ 7]  242 	sub	a, #0x7d
   5C89 30 03         [12]  243 	jr	NC,00121$
   5C8B 3E FD         [ 7]  244 	ld	a, #0xfd
   5C8D 12            [ 7]  245 	ld	(de), a
   5C8E                     246 00121$:
                            247 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5C8E C5            [11]  248 	push	bc
   5C8F D5            [11]  249 	push	de
   5C90 CD 0E 51      [17]  250 	call	_input_is_jump_just_pressed
   5C93 DD 75 FC      [19]  251 	ld	-4 (ix), l
   5C96 D1            [10]  252 	pop	de
   5C97 C1            [10]  253 	pop	bc
   5C98 21 05 00      [10]  254 	ld	hl, #0x0005
   5C9B 09            [11]  255 	add	hl,bc
   5C9C DD 75 FE      [19]  256 	ld	-2 (ix), l
   5C9F DD 74 FF      [19]  257 	ld	-1 (ix), h
   5CA2 21 01 00      [10]  258 	ld	hl, #0x0001
   5CA5 09            [11]  259 	add	hl,bc
   5CA6 DD 75 FA      [19]  260 	ld	-6 (ix), l
   5CA9 DD 74 FB      [19]  261 	ld	-5 (ix), h
                            262 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5CAC 21 03 00      [10]  263 	ld	hl, #0x0003
   5CAF 09            [11]  264 	add	hl,bc
   5CB0 DD 75 F8      [19]  265 	ld	-8 (ix), l
   5CB3 DD 74 F9      [19]  266 	ld	-7 (ix), h
                            267 ;src/entities/player.c:61: player->jump_hold = 5;
   5CB6 21 09 00      [10]  268 	ld	hl, #0x0009
   5CB9 09            [11]  269 	add	hl,bc
   5CBA DD 75 F6      [19]  270 	ld	-10 (ix), l
   5CBD DD 74 F7      [19]  271 	ld	-9 (ix), h
                            272 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5CC0 DD 7E FC      [19]  273 	ld	a, -4 (ix)
   5CC3 B7            [ 4]  274 	or	a, a
   5CC4 28 4E         [12]  275 	jr	Z,00123$
   5CC6 DD 6E FE      [19]  276 	ld	l,-2 (ix)
   5CC9 DD 66 FF      [19]  277 	ld	h,-1 (ix)
   5CCC 7E            [ 7]  278 	ld	a, (hl)
   5CCD DD 6E FA      [19]  279 	ld	l,-6 (ix)
   5CD0 DD 66 FB      [19]  280 	ld	h,-5 (ix)
   5CD3 6E            [ 7]  281 	ld	l, (hl)
   5CD4 DD 75 F4      [19]  282 	ld	-12 (ix), l
   5CD7 DD 36 F5 00   [19]  283 	ld	-11 (ix), #0x00
   5CDB F5            [11]  284 	push	af
   5CDC 0A            [ 7]  285 	ld	a, (bc)
   5CDD 6F            [ 4]  286 	ld	l, a
   5CDE F1            [10]  287 	pop	af
   5CDF DD 75 F2      [19]  288 	ld	-14 (ix), l
   5CE2 DD 36 F3 00   [19]  289 	ld	-13 (ix), #0x00
   5CE6 C5            [11]  290 	push	bc
   5CE7 D5            [11]  291 	push	de
   5CE8 F5            [11]  292 	push	af
   5CE9 33            [ 6]  293 	inc	sp
   5CEA DD 6E F4      [19]  294 	ld	l,-12 (ix)
   5CED DD 66 F5      [19]  295 	ld	h,-11 (ix)
   5CF0 E5            [11]  296 	push	hl
   5CF1 DD 6E F2      [19]  297 	ld	l,-14 (ix)
   5CF4 DD 66 F3      [19]  298 	ld	h,-13 (ix)
   5CF7 E5            [11]  299 	push	hl
   5CF8 CD C1 4B      [17]  300 	call	_collision_is_on_ground_at
   5CFB F1            [10]  301 	pop	af
   5CFC F1            [10]  302 	pop	af
   5CFD 33            [ 6]  303 	inc	sp
   5CFE D1            [10]  304 	pop	de
   5CFF C1            [10]  305 	pop	bc
   5D00 7D            [ 4]  306 	ld	a, l
   5D01 B7            [ 4]  307 	or	a, a
   5D02 28 10         [12]  308 	jr	Z,00123$
                            309 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5D04 DD 6E F8      [19]  310 	ld	l,-8 (ix)
   5D07 DD 66 F9      [19]  311 	ld	h,-7 (ix)
   5D0A 36 FA         [10]  312 	ld	(hl), #0xfa
                            313 ;src/entities/player.c:61: player->jump_hold = 5;
   5D0C DD 6E F6      [19]  314 	ld	l,-10 (ix)
   5D0F DD 66 F7      [19]  315 	ld	h,-9 (ix)
   5D12 36 05         [10]  316 	ld	(hl), #0x05
   5D14                     317 00123$:
                            318 ;src/entities/player.c:64: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5D14 C5            [11]  319 	push	bc
   5D15 D5            [11]  320 	push	de
   5D16 CD 06 51      [17]  321 	call	_input_is_jump_pressed
   5D19 7D            [ 4]  322 	ld	a, l
   5D1A D1            [10]  323 	pop	de
   5D1B C1            [10]  324 	pop	bc
   5D1C B7            [ 4]  325 	or	a, a
   5D1D 28 31         [12]  326 	jr	Z,00126$
   5D1F DD 6E F6      [19]  327 	ld	l,-10 (ix)
   5D22 DD 66 F7      [19]  328 	ld	h,-9 (ix)
   5D25 7E            [ 7]  329 	ld	a, (hl)
   5D26 B7            [ 4]  330 	or	a, a
   5D27 28 27         [12]  331 	jr	Z,00126$
   5D29 DD 6E F8      [19]  332 	ld	l,-8 (ix)
   5D2C DD 66 F9      [19]  333 	ld	h,-7 (ix)
   5D2F 6E            [ 7]  334 	ld	l, (hl)
   5D30 CB 7D         [ 8]  335 	bit	7, l
   5D32 28 1C         [12]  336 	jr	Z,00126$
                            337 ;src/entities/player.c:65: player->vy = (i8)(player->vy + kplayerjumpboost);
   5D34 7D            [ 4]  338 	ld	a, l
   5D35 C6 FF         [ 7]  339 	add	a, #0xff
   5D37 DD 6E F8      [19]  340 	ld	l,-8 (ix)
   5D3A DD 66 F9      [19]  341 	ld	h,-7 (ix)
   5D3D 77            [ 7]  342 	ld	(hl), a
                            343 ;src/entities/player.c:66: player->jump_hold--;
   5D3E DD 6E F6      [19]  344 	ld	l,-10 (ix)
   5D41 DD 66 F7      [19]  345 	ld	h,-9 (ix)
   5D44 7E            [ 7]  346 	ld	a, (hl)
   5D45 C6 FF         [ 7]  347 	add	a, #0xff
   5D47 DD 6E F6      [19]  348 	ld	l,-10 (ix)
   5D4A DD 66 F7      [19]  349 	ld	h,-9 (ix)
   5D4D 77            [ 7]  350 	ld	(hl), a
   5D4E 18 08         [12]  351 	jr	00127$
   5D50                     352 00126$:
                            353 ;src/entities/player.c:68: player->jump_hold = 0;
   5D50 DD 6E F6      [19]  354 	ld	l,-10 (ix)
   5D53 DD 66 F7      [19]  355 	ld	h,-9 (ix)
   5D56 36 00         [10]  356 	ld	(hl), #0x00
   5D58                     357 00127$:
                            358 ;src/entities/player.c:71: player->vy = (i8)(player->vy + kplayergravity);
   5D58 DD 6E F8      [19]  359 	ld	l,-8 (ix)
   5D5B DD 66 F9      [19]  360 	ld	h,-7 (ix)
   5D5E 7E            [ 7]  361 	ld	a, (hl)
   5D5F 3C            [ 4]  362 	inc	a
   5D60 DD 77 F2      [19]  363 	ld	-14 (ix), a
   5D63 DD 6E F8      [19]  364 	ld	l,-8 (ix)
   5D66 DD 66 F9      [19]  365 	ld	h,-7 (ix)
   5D69 DD 7E F2      [19]  366 	ld	a, -14 (ix)
   5D6C 77            [ 7]  367 	ld	(hl), a
                            368 ;src/entities/player.c:72: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5D6D 3E 04         [ 7]  369 	ld	a, #0x04
   5D6F DD 96 F2      [19]  370 	sub	a, -14 (ix)
   5D72 E2 77 5D      [10]  371 	jp	PO, 00226$
   5D75 EE 80         [ 7]  372 	xor	a, #0x80
   5D77                     373 00226$:
   5D77 F2 82 5D      [10]  374 	jp	P, 00131$
   5D7A DD 6E F8      [19]  375 	ld	l,-8 (ix)
   5D7D DD 66 F9      [19]  376 	ld	h,-7 (ix)
   5D80 36 04         [10]  377 	ld	(hl), #0x04
   5D82                     378 00131$:
                            379 ;src/entities/player.c:74: nextx = (i16)player->x + (i16)player->vx;
   5D82 0A            [ 7]  380 	ld	a, (bc)
   5D83 DD 77 F2      [19]  381 	ld	-14 (ix), a
   5D86 DD 36 F3 00   [19]  382 	ld	-13 (ix), #0x00
   5D8A 1A            [ 7]  383 	ld	a, (de)
   5D8B 5F            [ 4]  384 	ld	e, a
   5D8C 17            [ 4]  385 	rla
   5D8D 9F            [ 4]  386 	sbc	a, a
   5D8E 57            [ 4]  387 	ld	d, a
   5D8F E1            [10]  388 	pop	hl
   5D90 E5            [11]  389 	push	hl
   5D91 19            [11]  390 	add	hl, de
                            391 ;src/entities/player.c:75: if (nextx < 0) {
   5D92 CB 7C         [ 8]  392 	bit	7, h
   5D94 28 03         [12]  393 	jr	Z,00133$
                            394 ;src/entities/player.c:76: nextx = 0;
   5D96 21 00 00      [10]  395 	ld	hl, #0x0000
   5D99                     396 00133$:
                            397 ;src/entities/player.c:78: if (nextx > 76) {
   5D99 3E 4C         [ 7]  398 	ld	a, #0x4c
   5D9B BD            [ 4]  399 	cp	a, l
   5D9C 3E 00         [ 7]  400 	ld	a, #0x00
   5D9E 9C            [ 4]  401 	sbc	a, h
   5D9F E2 A4 5D      [10]  402 	jp	PO, 00227$
   5DA2 EE 80         [ 7]  403 	xor	a, #0x80
   5DA4                     404 00227$:
   5DA4 F2 AA 5D      [10]  405 	jp	P, 00135$
                            406 ;src/entities/player.c:79: nextx = 76;
   5DA7 21 4C 00      [10]  407 	ld	hl, #0x004c
   5DAA                     408 00135$:
                            409 ;src/entities/player.c:81: player->x = (u8)nextx;
   5DAA DD 75 F2      [19]  410 	ld	-14 (ix), l
   5DAD 7D            [ 4]  411 	ld	a, l
   5DAE 02            [ 7]  412 	ld	(bc), a
                            413 ;src/entities/player.c:83: nexty = (i16)player->y + (i16)player->vy;
   5DAF DD 6E FA      [19]  414 	ld	l,-6 (ix)
   5DB2 DD 66 FB      [19]  415 	ld	h,-5 (ix)
   5DB5 5E            [ 7]  416 	ld	e, (hl)
   5DB6 16 00         [ 7]  417 	ld	d, #0x00
   5DB8 DD 6E F8      [19]  418 	ld	l,-8 (ix)
   5DBB DD 66 F9      [19]  419 	ld	h,-7 (ix)
   5DBE 6E            [ 7]  420 	ld	l, (hl)
   5DBF 7D            [ 4]  421 	ld	a, l
   5DC0 17            [ 4]  422 	rla
   5DC1 9F            [ 4]  423 	sbc	a, a
   5DC2 67            [ 4]  424 	ld	h, a
   5DC3 19            [11]  425 	add	hl, de
   5DC4 E5            [11]  426 	push	hl
   5DC5 FD E1         [14]  427 	pop	iy
                            428 ;src/entities/player.c:84: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5DC7 DD 6E FE      [19]  429 	ld	l,-2 (ix)
   5DCA DD 66 FF      [19]  430 	ld	h,-1 (ix)
   5DCD 66            [ 7]  431 	ld	h, (hl)
   5DCE DD 5E F2      [19]  432 	ld	e, -14 (ix)
   5DD1 16 00         [ 7]  433 	ld	d, #0x00
   5DD3 C5            [11]  434 	push	bc
   5DD4 E5            [11]  435 	push	hl
   5DD5 33            [ 6]  436 	inc	sp
   5DD6 FD E5         [15]  437 	push	iy
   5DD8 D5            [11]  438 	push	de
   5DD9 CD 40 4C      [17]  439 	call	_collision_clamp_y_at
   5DDC F1            [10]  440 	pop	af
   5DDD F1            [10]  441 	pop	af
   5DDE 33            [ 6]  442 	inc	sp
   5DDF C1            [10]  443 	pop	bc
                            444 ;src/entities/player.c:85: if (nexty < 0) {
   5DE0 CB 7C         [ 8]  445 	bit	7, h
   5DE2 28 03         [12]  446 	jr	Z,00137$
                            447 ;src/entities/player.c:86: nexty = 0;
   5DE4 21 00 00      [10]  448 	ld	hl, #0x0000
   5DE7                     449 00137$:
                            450 ;src/entities/player.c:88: player->y = (u8)nexty;
   5DE7 5D            [ 4]  451 	ld	e, l
   5DE8 DD 6E FA      [19]  452 	ld	l,-6 (ix)
   5DEB DD 66 FB      [19]  453 	ld	h,-5 (ix)
   5DEE 73            [ 7]  454 	ld	(hl), e
                            455 ;src/entities/player.c:90: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5DEF DD 6E FE      [19]  456 	ld	l,-2 (ix)
   5DF2 DD 66 FF      [19]  457 	ld	h,-1 (ix)
   5DF5 7E            [ 7]  458 	ld	a, (hl)
   5DF6 16 00         [ 7]  459 	ld	d, #0x00
   5DF8 F5            [11]  460 	push	af
   5DF9 0A            [ 7]  461 	ld	a, (bc)
   5DFA 4F            [ 4]  462 	ld	c, a
   5DFB F1            [10]  463 	pop	af
   5DFC 06 00         [ 7]  464 	ld	b, #0x00
   5DFE F5            [11]  465 	push	af
   5DFF 33            [ 6]  466 	inc	sp
   5E00 D5            [11]  467 	push	de
   5E01 C5            [11]  468 	push	bc
   5E02 CD C1 4B      [17]  469 	call	_collision_is_on_ground_at
   5E05 F1            [10]  470 	pop	af
   5E06 F1            [10]  471 	pop	af
   5E07 33            [ 6]  472 	inc	sp
   5E08 7D            [ 4]  473 	ld	a, l
   5E09 B7            [ 4]  474 	or	a, a
   5E0A 28 19         [12]  475 	jr	Z,00141$
   5E0C DD 6E F8      [19]  476 	ld	l,-8 (ix)
   5E0F DD 66 F9      [19]  477 	ld	h,-7 (ix)
   5E12 4E            [ 7]  478 	ld	c, (hl)
   5E13 AF            [ 4]  479 	xor	a, a
   5E14 91            [ 4]  480 	sub	a, c
   5E15 E2 1A 5E      [10]  481 	jp	PO, 00228$
   5E18 EE 80         [ 7]  482 	xor	a, #0x80
   5E1A                     483 00228$:
   5E1A F2 25 5E      [10]  484 	jp	P, 00141$
                            485 ;src/entities/player.c:91: player->vy = 0;
   5E1D DD 6E F8      [19]  486 	ld	l,-8 (ix)
   5E20 DD 66 F9      [19]  487 	ld	h,-7 (ix)
   5E23 36 00         [10]  488 	ld	(hl), #0x00
   5E25                     489 00141$:
   5E25 DD F9         [10]  490 	ld	sp, ix
   5E27 DD E1         [14]  491 	pop	ix
   5E29 C9            [10]  492 	ret
                            493 ;src/entities/player.c:95: void playerrender(const Player* player) {
                            494 ;	---------------------------------
                            495 ; Function playerrender
                            496 ; ---------------------------------
   5E2A                     497 _playerrender::
   5E2A DD E5         [15]  498 	push	ix
   5E2C DD 21 00 00   [14]  499 	ld	ix,#0
   5E30 DD 39         [15]  500 	add	ix,sp
   5E32 3B            [ 6]  501 	dec	sp
                            502 ;src/entities/player.c:98: if (!player) {
   5E33 DD 7E 05      [19]  503 	ld	a, 5 (ix)
   5E36 DD B6 04      [19]  504 	or	a,4 (ix)
                            505 ;src/entities/player.c:99: return;
   5E39 28 38         [12]  506 	jr	Z,00103$
                            507 ;src/entities/player.c:102: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5E3B DD 5E 04      [19]  508 	ld	e,4 (ix)
   5E3E DD 56 05      [19]  509 	ld	d,5 (ix)
   5E41 6B            [ 4]  510 	ld	l, e
   5E42 62            [ 4]  511 	ld	h, d
   5E43 23            [ 6]  512 	inc	hl
   5E44 46            [ 7]  513 	ld	b, (hl)
   5E45 1A            [ 7]  514 	ld	a, (de)
   5E46 D5            [11]  515 	push	de
   5E47 C5            [11]  516 	push	bc
   5E48 33            [ 6]  517 	inc	sp
   5E49 F5            [11]  518 	push	af
   5E4A 33            [ 6]  519 	inc	sp
   5E4B 21 00 C0      [10]  520 	ld	hl, #0xc000
   5E4E E5            [11]  521 	push	hl
   5E4F CD 41 63      [17]  522 	call	_cpct_getScreenPtr
   5E52 4D            [ 4]  523 	ld	c, l
   5E53 44            [ 4]  524 	ld	b, h
   5E54 D1            [10]  525 	pop	de
                            526 ;src/entities/player.c:103: cpct_drawSprite((u8*)sprplayerknight_data, pvmem, player->w, player->h);
   5E55 D5            [11]  527 	push	de
   5E56 FD E1         [14]  528 	pop	iy
   5E58 FD 7E 05      [19]  529 	ld	a, 5 (iy)
   5E5B DD 77 FF      [19]  530 	ld	-1 (ix), a
   5E5E EB            [ 4]  531 	ex	de,hl
   5E5F 11 04 00      [10]  532 	ld	de, #0x0004
   5E62 19            [11]  533 	add	hl, de
   5E63 56            [ 7]  534 	ld	d, (hl)
   5E64 DD 7E FF      [19]  535 	ld	a, -1 (ix)
   5E67 F5            [11]  536 	push	af
   5E68 33            [ 6]  537 	inc	sp
   5E69 D5            [11]  538 	push	de
   5E6A 33            [ 6]  539 	inc	sp
   5E6B C5            [11]  540 	push	bc
   5E6C 21 67 54      [10]  541 	ld	hl, #_sprplayerknight_data
   5E6F E5            [11]  542 	push	hl
   5E70 CD 72 61      [17]  543 	call	_cpct_drawSprite
   5E73                     544 00103$:
   5E73 33            [ 6]  545 	inc	sp
   5E74 DD E1         [14]  546 	pop	ix
   5E76 C9            [10]  547 	ret
                            548 ;src/entities/player.c:106: u8 player_get_health(const Player* player) {
                            549 ;	---------------------------------
                            550 ; Function player_get_health
                            551 ; ---------------------------------
   5E77                     552 _player_get_health::
                            553 ;src/entities/player.c:107: return player ? player->health : 0;
   5E77 21 03 00      [10]  554 	ld	hl, #2+1
   5E7A 39            [11]  555 	add	hl, sp
   5E7B 7E            [ 7]  556 	ld	a, (hl)
   5E7C 2B            [ 6]  557 	dec	hl
   5E7D B6            [ 7]  558 	or	a,(hl)
   5E7E 28 0A         [12]  559 	jr	Z,00103$
   5E80 C1            [10]  560 	pop	bc
   5E81 E1            [10]  561 	pop	hl
   5E82 E5            [11]  562 	push	hl
   5E83 C5            [11]  563 	push	bc
   5E84 11 06 00      [10]  564 	ld	de, #0x0006
   5E87 19            [11]  565 	add	hl, de
   5E88 6E            [ 7]  566 	ld	l, (hl)
   5E89 C9            [10]  567 	ret
   5E8A                     568 00103$:
   5E8A 2E 00         [ 7]  569 	ld	l, #0x00
   5E8C C9            [10]  570 	ret
                            571 ;src/entities/player.c:110: u8 player_get_weapon(const Player* player) {
                            572 ;	---------------------------------
                            573 ; Function player_get_weapon
                            574 ; ---------------------------------
   5E8D                     575 _player_get_weapon::
                            576 ;src/entities/player.c:111: return player ? player->weapon : 0;
   5E8D 21 03 00      [10]  577 	ld	hl, #2+1
   5E90 39            [11]  578 	add	hl, sp
   5E91 7E            [ 7]  579 	ld	a, (hl)
   5E92 2B            [ 6]  580 	dec	hl
   5E93 B6            [ 7]  581 	or	a,(hl)
   5E94 28 0A         [12]  582 	jr	Z,00103$
   5E96 C1            [10]  583 	pop	bc
   5E97 E1            [10]  584 	pop	hl
   5E98 E5            [11]  585 	push	hl
   5E99 C5            [11]  586 	push	bc
   5E9A 11 07 00      [10]  587 	ld	de, #0x0007
   5E9D 19            [11]  588 	add	hl, de
   5E9E 6E            [ 7]  589 	ld	l, (hl)
   5E9F C9            [10]  590 	ret
   5EA0                     591 00103$:
   5EA0 2E 00         [ 7]  592 	ld	l, #0x00
   5EA2 C9            [10]  593 	ret
                            594 	.area _CODE
                            595 	.area _INITIALIZER
                            596 	.area _CABS (ABS)
