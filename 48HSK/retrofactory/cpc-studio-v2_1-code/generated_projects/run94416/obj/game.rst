                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module game
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _hudrender
                             12 	.globl _hudupdate
                             13 	.globl _hudinit
                             14 	.globl _projectilerender
                             15 	.globl _projectileupdate
                             16 	.globl _projectilefire
                             17 	.globl _projectileinit
                             18 	.globl _enemydamage
                             19 	.globl _enemyrender
                             20 	.globl _enemyupdate
                             21 	.globl _enemyspawn
                             22 	.globl _enemyinit
                             23 	.globl _playerrender
                             24 	.globl _playerupdate
                             25 	.globl _playerinit
                             26 	.globl _collision_is_on_trap
                             27 	.globl _collision_init
                             28 	.globl _input_is_shoot_just_pressed
                             29 	.globl _input_update
                             30 	.globl _tilemap_goal_x
                             31 	.globl _tilemap_ground_y
                             32 	.globl _tilemap_render
                             33 	.globl _tilemap_init
                             34 	.globl _cpct_getScreenPtr
                             35 	.globl _cpct_setPALColour
                             36 	.globl _cpct_setPalette
                             37 	.globl _cpct_setVideoMode
                             38 	.globl _cpct_drawSolidBox
                             39 	.globl _cpct_px2byteM0
                             40 	.globl _cpct_memset
                             41 	.globl _cpct_disableFirmware
                             42 	.globl _game_init
                             43 	.globl _game_update
                             44 	.globl _game_render
                             45 ;--------------------------------------------------------
                             46 ; special function registers
                             47 ;--------------------------------------------------------
                             48 ;--------------------------------------------------------
                             49 ; ram data
                             50 ;--------------------------------------------------------
                             51 	.area _DATA
   6469                      52 _g_player:
   6469                      53 	.ds 10
   6473                      54 _g_enemies:
   6473                      55 	.ds 60
   64AF                      56 _g_projectiles:
   64AF                      57 	.ds 60
   64EB                      58 _g_lives:
   64EB                      59 	.ds 1
   64EC                      60 _g_score:
   64EC                      61 	.ds 2
   64EE                      62 _g_timeleft:
   64EE                      63 	.ds 1
   64EF                      64 _g_weapondisplay:
   64EF                      65 	.ds 1
   64F0                      66 _g_currentwave:
   64F0                      67 	.ds 1
   64F1                      68 _g_aliveenemies:
   64F1                      69 	.ds 1
   64F2                      70 _g_wavecooldown:
   64F2                      71 	.ds 1
   64F3                      72 _g_damagecooldown:
   64F3                      73 	.ds 1
   64F4                      74 _g_shootcooldown:
   64F4                      75 	.ds 1
   64F5                      76 _g_victory:
   64F5                      77 	.ds 1
   64F6                      78 _g_gameover:
   64F6                      79 	.ds 1
   64F7                      80 _g_framecounter:
   64F7                      81 	.ds 2
   64F9                      82 _g_checkpointx:
   64F9                      83 	.ds 1
   64FA                      84 _g_checkpointy:
   64FA                      85 	.ds 1
   64FB                      86 _g_checkpointactive:
   64FB                      87 	.ds 1
   64FC                      88 _g_boss:
   64FC                      89 	.ds 10
   6506                      90 _g_bossactive:
   6506                      91 	.ds 1
   6507                      92 _g_bossphase:
   6507                      93 	.ds 1
   6508                      94 _g_weaponlevel:
   6508                      95 	.ds 1
   6509                      96 _g_pickuptaken:
   6509                      97 	.ds 1
                             98 ;--------------------------------------------------------
                             99 ; ram data
                            100 ;--------------------------------------------------------
                            101 	.area _INITIALIZED
                            102 ;--------------------------------------------------------
                            103 ; absolute external ram data
                            104 ;--------------------------------------------------------
                            105 	.area _DABS (ABS)
                            106 ;--------------------------------------------------------
                            107 ; global & static initialisations
                            108 ;--------------------------------------------------------
                            109 	.area _HOME
                            110 	.area _GSINIT
                            111 	.area _GSFINAL
                            112 	.area _GSINIT
                            113 ;--------------------------------------------------------
                            114 ; Home
                            115 ;--------------------------------------------------------
                            116 	.area _HOME
                            117 	.area _HOME
                            118 ;--------------------------------------------------------
                            119 ; code
                            120 ;--------------------------------------------------------
                            121 	.area _CODE
                            122 ;src/game.c:41: static void reset_player_to_checkpoint(void) {
                            123 ;	---------------------------------
                            124 ; Function reset_player_to_checkpoint
                            125 ; ---------------------------------
   4000                     126 _reset_player_to_checkpoint:
                            127 ;src/game.c:42: g_player.x = g_checkpointx;
   4000 21 69 64      [10]  128 	ld	hl, #_g_player
   4003 3A F9 64      [13]  129 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  130 	ld	(hl), a
                            131 ;src/game.c:43: g_player.y = g_checkpointy;
   4007 21 6A 64      [10]  132 	ld	hl, #(_g_player + 0x0001)
   400A 3A FA 64      [13]  133 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  134 	ld	(hl), a
                            135 ;src/game.c:44: g_player.vx = 0;
   400E 21 6B 64      [10]  136 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  137 	ld	(hl), #0x00
                            138 ;src/game.c:45: g_player.vy = 0;
   4013 21 6C 64      [10]  139 	ld	hl, #(_g_player + 0x0003)
   4016 36 00         [10]  140 	ld	(hl), #0x00
   4018 C9            [10]  141 	ret
                            142 ;src/game.c:48: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
                            143 ;	---------------------------------
                            144 ; Function rect_overlap
                            145 ; ---------------------------------
   4019                     146 _rect_overlap:
   4019 DD E5         [15]  147 	push	ix
   401B DD 21 00 00   [14]  148 	ld	ix,#0
   401F DD 39         [15]  149 	add	ix,sp
                            150 ;src/game.c:49: if (ax + aw <= bx) return 0;
   4021 DD 4E 08      [19]  151 	ld	c, 8 (ix)
   4024 06 00         [ 7]  152 	ld	b, #0x00
   4026 DD 6E 04      [19]  153 	ld	l,4 (ix)
   4029 DD 66 05      [19]  154 	ld	h,5 (ix)
   402C 09            [11]  155 	add	hl, bc
   402D DD 7E 0A      [19]  156 	ld	a, 10 (ix)
   4030 95            [ 4]  157 	sub	a, l
   4031 DD 7E 0B      [19]  158 	ld	a, 11 (ix)
   4034 9C            [ 4]  159 	sbc	a, h
   4035 E2 3A 40      [10]  160 	jp	PO, 00127$
   4038 EE 80         [ 7]  161 	xor	a, #0x80
   403A                     162 00127$:
   403A FA 41 40      [10]  163 	jp	M, 00102$
   403D 2E 00         [ 7]  164 	ld	l, #0x00
   403F 18 62         [12]  165 	jr	00109$
   4041                     166 00102$:
                            167 ;src/game.c:50: if (bx + bw <= ax) return 0;
   4041 DD 4E 0E      [19]  168 	ld	c, 14 (ix)
   4044 06 00         [ 7]  169 	ld	b, #0x00
   4046 DD 6E 0A      [19]  170 	ld	l,10 (ix)
   4049 DD 66 0B      [19]  171 	ld	h,11 (ix)
   404C 09            [11]  172 	add	hl, bc
   404D DD 7E 04      [19]  173 	ld	a, 4 (ix)
   4050 95            [ 4]  174 	sub	a, l
   4051 DD 7E 05      [19]  175 	ld	a, 5 (ix)
   4054 9C            [ 4]  176 	sbc	a, h
   4055 E2 5A 40      [10]  177 	jp	PO, 00128$
   4058 EE 80         [ 7]  178 	xor	a, #0x80
   405A                     179 00128$:
   405A FA 61 40      [10]  180 	jp	M, 00104$
   405D 2E 00         [ 7]  181 	ld	l, #0x00
   405F 18 42         [12]  182 	jr	00109$
   4061                     183 00104$:
                            184 ;src/game.c:51: if (ay + ah <= by) return 0;
   4061 DD 4E 09      [19]  185 	ld	c, 9 (ix)
   4064 06 00         [ 7]  186 	ld	b, #0x00
   4066 DD 6E 06      [19]  187 	ld	l,6 (ix)
   4069 DD 66 07      [19]  188 	ld	h,7 (ix)
   406C 09            [11]  189 	add	hl, bc
   406D DD 7E 0C      [19]  190 	ld	a, 12 (ix)
   4070 95            [ 4]  191 	sub	a, l
   4071 DD 7E 0D      [19]  192 	ld	a, 13 (ix)
   4074 9C            [ 4]  193 	sbc	a, h
   4075 E2 7A 40      [10]  194 	jp	PO, 00129$
   4078 EE 80         [ 7]  195 	xor	a, #0x80
   407A                     196 00129$:
   407A FA 81 40      [10]  197 	jp	M, 00106$
   407D 2E 00         [ 7]  198 	ld	l, #0x00
   407F 18 22         [12]  199 	jr	00109$
   4081                     200 00106$:
                            201 ;src/game.c:52: if (by + bh <= ay) return 0;
   4081 DD 4E 0F      [19]  202 	ld	c, 15 (ix)
   4084 06 00         [ 7]  203 	ld	b, #0x00
   4086 DD 6E 0C      [19]  204 	ld	l,12 (ix)
   4089 DD 66 0D      [19]  205 	ld	h,13 (ix)
   408C 09            [11]  206 	add	hl, bc
   408D DD 7E 06      [19]  207 	ld	a, 6 (ix)
   4090 95            [ 4]  208 	sub	a, l
   4091 DD 7E 07      [19]  209 	ld	a, 7 (ix)
   4094 9C            [ 4]  210 	sbc	a, h
   4095 E2 9A 40      [10]  211 	jp	PO, 00130$
   4098 EE 80         [ 7]  212 	xor	a, #0x80
   409A                     213 00130$:
   409A FA A1 40      [10]  214 	jp	M, 00108$
   409D 2E 00         [ 7]  215 	ld	l, #0x00
   409F 18 02         [12]  216 	jr	00109$
   40A1                     217 00108$:
                            218 ;src/game.c:53: return 1;
   40A1 2E 01         [ 7]  219 	ld	l, #0x01
   40A3                     220 00109$:
   40A3 DD E1         [14]  221 	pop	ix
   40A5 C9            [10]  222 	ret
                            223 ;src/game.c:56: static void spawn_wave(u8 wave) {
                            224 ;	---------------------------------
                            225 ; Function spawn_wave
                            226 ; ---------------------------------
   40A6                     227 _spawn_wave:
   40A6 DD E5         [15]  228 	push	ix
   40A8 DD 21 00 00   [14]  229 	ld	ix,#0
   40AC DD 39         [15]  230 	add	ix,sp
   40AE F5            [11]  231 	push	af
   40AF F5            [11]  232 	push	af
   40B0 3B            [ 6]  233 	dec	sp
                            234 ;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
   40B1 01 73 64      [10]  235 	ld	bc, #_g_enemies+0
   40B4 1E 00         [ 7]  236 	ld	e, #0x00
   40B6                     237 00117$:
                            238 ;src/game.c:61: enemyinit(&g_enemies[i]);
   40B6 D5            [11]  239 	push	de
   40B7 16 00         [ 7]  240 	ld	d,#0x00
   40B9 6B            [ 4]  241 	ld	l, e
   40BA 62            [ 4]  242 	ld	h, d
   40BB 29            [11]  243 	add	hl, hl
   40BC 29            [11]  244 	add	hl, hl
   40BD 19            [11]  245 	add	hl, de
   40BE 29            [11]  246 	add	hl, hl
   40BF D1            [10]  247 	pop	de
   40C0 09            [11]  248 	add	hl, bc
   40C1 C5            [11]  249 	push	bc
   40C2 D5            [11]  250 	push	de
   40C3 E5            [11]  251 	push	hl
   40C4 CD 1C 56      [17]  252 	call	_enemyinit
   40C7 F1            [10]  253 	pop	af
   40C8 D1            [10]  254 	pop	de
   40C9 C1            [10]  255 	pop	bc
                            256 ;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
   40CA 1C            [ 4]  257 	inc	e
   40CB 7B            [ 4]  258 	ld	a, e
   40CC D6 06         [ 7]  259 	sub	a, #0x06
   40CE 38 E6         [12]  260 	jr	C,00117$
                            261 ;src/game.c:65: else if (wave == 1) count = 3;
   40D0 DD 7E 04      [19]  262 	ld	a, 4 (ix)
   40D3 3D            [ 4]  263 	dec	a
   40D4 20 04         [12]  264 	jr	NZ,00190$
   40D6 3E 01         [ 7]  265 	ld	a,#0x01
   40D8 18 01         [12]  266 	jr	00191$
   40DA                     267 00190$:
   40DA AF            [ 4]  268 	xor	a,a
   40DB                     269 00191$:
   40DB 5F            [ 4]  270 	ld	e, a
                            271 ;src/game.c:64: if (wave == 0) count = 2;
   40DC DD 7E 04      [19]  272 	ld	a, 4 (ix)
   40DF B7            [ 4]  273 	or	a, a
   40E0 20 06         [12]  274 	jr	NZ,00106$
   40E2 DD 36 FC 02   [19]  275 	ld	-4 (ix), #0x02
   40E6 18 0E         [12]  276 	jr	00107$
   40E8                     277 00106$:
                            278 ;src/game.c:65: else if (wave == 1) count = 3;
   40E8 7B            [ 4]  279 	ld	a, e
   40E9 B7            [ 4]  280 	or	a, a
   40EA 28 06         [12]  281 	jr	Z,00103$
   40EC DD 36 FC 03   [19]  282 	ld	-4 (ix), #0x03
   40F0 18 04         [12]  283 	jr	00107$
   40F2                     284 00103$:
                            285 ;src/game.c:66: else count = 4;
   40F2 DD 36 FC 04   [19]  286 	ld	-4 (ix), #0x04
   40F6                     287 00107$:
                            288 ;src/game.c:68: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F6 3E 06         [ 7]  289 	ld	a, #0x06
   40F8 DD 96 FC      [19]  290 	sub	a, -4 (ix)
   40FB 30 04         [12]  291 	jr	NC,00148$
   40FD DD 36 FC 06   [19]  292 	ld	-4 (ix), #0x06
                            293 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4101                     294 00148$:
   4101 DD 73 FF      [19]  295 	ld	-1 (ix), e
   4104 DD 36 FB 00   [19]  296 	ld	-5 (ix), #0x00
   4108                     297 00120$:
   4108 DD 7E FB      [19]  298 	ld	a, -5 (ix)
   410B DD 96 FC      [19]  299 	sub	a, -4 (ix)
   410E D2 9B 41      [10]  300 	jp	NC, 00116$
                            301 ;src/game.c:73: if (wave == 0) type = 0;
   4111 DD 7E 04      [19]  302 	ld	a, 4 (ix)
   4114 B7            [ 4]  303 	or	a,a
   4115 20 03         [12]  304 	jr	NZ,00114$
   4117 5F            [ 4]  305 	ld	e,a
   4118 18 27         [12]  306 	jr	00115$
   411A                     307 00114$:
                            308 ;src/game.c:74: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
   411A DD 7E FF      [19]  309 	ld	a, -1 (ix)
   411D B7            [ 4]  310 	or	a, a
   411E 28 0E         [12]  311 	jr	Z,00111$
   4120 DD 7E FB      [19]  312 	ld	a, -5 (ix)
   4123 B7            [ 4]  313 	or	a, a
   4124 20 04         [12]  314 	jr	NZ,00124$
   4126 1E 01         [ 7]  315 	ld	e, #0x01
   4128 18 17         [12]  316 	jr	00115$
   412A                     317 00124$:
   412A 1E 00         [ 7]  318 	ld	e, #0x00
   412C 18 13         [12]  319 	jr	00115$
   412E                     320 00111$:
                            321 ;src/game.c:75: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   412E DD 7E FB      [19]  322 	ld	a, -5 (ix)
   4131 B7            [ 4]  323 	or	a, a
   4132 28 07         [12]  324 	jr	Z,00129$
   4134 DD 7E FB      [19]  325 	ld	a, -5 (ix)
   4137 D6 03         [ 7]  326 	sub	a, #0x03
   4139 20 04         [12]  327 	jr	NZ,00126$
   413B                     328 00129$:
   413B 1E 02         [ 7]  329 	ld	e, #0x02
   413D 18 02         [12]  330 	jr	00127$
   413F                     331 00126$:
   413F 1E 01         [ 7]  332 	ld	e, #0x01
   4141                     333 00127$:
   4141                     334 00115$:
                            335 ;src/game.c:77: spawn_y = (type == 2) ? 84 : 112;
   4141 7B            [ 4]  336 	ld	a, e
   4142 D6 02         [ 7]  337 	sub	a, #0x02
   4144 20 04         [12]  338 	jr	NZ,00131$
   4146 16 54         [ 7]  339 	ld	d, #0x54
   4148 18 02         [12]  340 	jr	00132$
   414A                     341 00131$:
   414A 16 70         [ 7]  342 	ld	d, #0x70
   414C                     343 00132$:
                            344 ;src/game.c:78: enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));
   414C DD CB FB 46   [20]  345 	bit	0, -5 (ix)
   4150 28 06         [12]  346 	jr	Z,00133$
   4152 DD 36 FE 01   [19]  347 	ld	-2 (ix), #0x01
   4156 18 04         [12]  348 	jr	00134$
   4158                     349 00133$:
   4158 DD 36 FE 00   [19]  350 	ld	-2 (ix), #0x00
   415C                     351 00134$:
   415C DD 7E FB      [19]  352 	ld	a, -5 (ix)
   415F 07            [ 4]  353 	rlca
   4160 07            [ 4]  354 	rlca
   4161 07            [ 4]  355 	rlca
   4162 E6 F8         [ 7]  356 	and	a, #0xf8
   4164 C6 2E         [ 7]  357 	add	a, #0x2e
   4166 DD 77 FD      [19]  358 	ld	-3 (ix), a
   4169 D5            [11]  359 	push	de
   416A DD 5E FB      [19]  360 	ld	e,-5 (ix)
   416D 16 00         [ 7]  361 	ld	d,#0x00
   416F 6B            [ 4]  362 	ld	l, e
   4170 62            [ 4]  363 	ld	h, d
   4171 29            [11]  364 	add	hl, hl
   4172 29            [11]  365 	add	hl, hl
   4173 19            [11]  366 	add	hl, de
   4174 29            [11]  367 	add	hl, hl
   4175 D1            [10]  368 	pop	de
   4176 09            [11]  369 	add	hl, bc
   4177 E5            [11]  370 	push	hl
   4178 FD E1         [14]  371 	pop	iy
   417A C5            [11]  372 	push	bc
   417B DD 7E FE      [19]  373 	ld	a, -2 (ix)
   417E F5            [11]  374 	push	af
   417F 33            [ 6]  375 	inc	sp
   4180 7B            [ 4]  376 	ld	a, e
   4181 F5            [11]  377 	push	af
   4182 33            [ 6]  378 	inc	sp
   4183 D5            [11]  379 	push	de
   4184 33            [ 6]  380 	inc	sp
   4185 DD 7E FD      [19]  381 	ld	a, -3 (ix)
   4188 F5            [11]  382 	push	af
   4189 33            [ 6]  383 	inc	sp
   418A FD E5         [15]  384 	push	iy
   418C CD D7 57      [17]  385 	call	_enemyspawn
   418F 21 06 00      [10]  386 	ld	hl, #6
   4192 39            [11]  387 	add	hl, sp
   4193 F9            [ 6]  388 	ld	sp, hl
   4194 C1            [10]  389 	pop	bc
                            390 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4195 DD 34 FB      [23]  391 	inc	-5 (ix)
   4198 C3 08 41      [10]  392 	jp	00120$
   419B                     393 00116$:
                            394 ;src/game.c:81: g_aliveenemies = count;
   419B DD 7E FC      [19]  395 	ld	a, -4 (ix)
   419E 32 F1 64      [13]  396 	ld	(#_g_aliveenemies + 0),a
   41A1 DD F9         [10]  397 	ld	sp, ix
   41A3 DD E1         [14]  398 	pop	ix
   41A5 C9            [10]  399 	ret
                            400 ;src/game.c:84: static void spawn_boss(void) {
                            401 ;	---------------------------------
                            402 ; Function spawn_boss
                            403 ; ---------------------------------
   41A6                     404 _spawn_boss:
                            405 ;src/game.c:85: enemyinit(&g_boss);
   41A6 21 FC 64      [10]  406 	ld	hl, #_g_boss
   41A9 E5            [11]  407 	push	hl
   41AA CD 1C 56      [17]  408 	call	_enemyinit
   41AD F1            [10]  409 	pop	af
                            410 ;src/game.c:86: enemyspawn(&g_boss, 68, 112, 1, 0);
   41AE 21 01 00      [10]  411 	ld	hl, #0x0001
   41B1 E5            [11]  412 	push	hl
   41B2 21 44 70      [10]  413 	ld	hl, #0x7044
   41B5 E5            [11]  414 	push	hl
   41B6 21 FC 64      [10]  415 	ld	hl, #_g_boss
   41B9 E5            [11]  416 	push	hl
   41BA CD D7 57      [17]  417 	call	_enemyspawn
   41BD 21 06 00      [10]  418 	ld	hl, #6
   41C0 39            [11]  419 	add	hl, sp
   41C1 F9            [ 6]  420 	ld	sp, hl
                            421 ;src/game.c:87: g_boss.w = 10;
   41C2 21 00 65      [10]  422 	ld	hl, #(_g_boss + 0x0004)
   41C5 36 0A         [10]  423 	ld	(hl), #0x0a
                            424 ;src/game.c:88: g_boss.h = 18;
   41C7 21 01 65      [10]  425 	ld	hl, #(_g_boss + 0x0005)
   41CA 36 12         [10]  426 	ld	(hl), #0x12
                            427 ;src/game.c:89: g_boss.health = 10;
   41CC 21 03 65      [10]  428 	ld	hl, #(_g_boss + 0x0007)
   41CF 36 0A         [10]  429 	ld	(hl), #0x0a
                            430 ;src/game.c:90: g_boss.reward = 1500;
   41D1 21 04 65      [10]  431 	ld	hl, #(_g_boss + 0x0008)
   41D4 36 DC         [10]  432 	ld	(hl), #0xdc
                            433 ;src/game.c:91: g_boss.kind = 3;
   41D6 21 05 65      [10]  434 	ld	hl, #(_g_boss + 0x0009)
   41D9 36 03         [10]  435 	ld	(hl), #0x03
                            436 ;src/game.c:92: g_boss.vx = -1;
   41DB 21 FE 64      [10]  437 	ld	hl, #(_g_boss + 0x0002)
   41DE 36 FF         [10]  438 	ld	(hl), #0xff
                            439 ;src/game.c:93: g_bossactive = 1;
   41E0 21 06 65      [10]  440 	ld	hl,#_g_bossactive + 0
   41E3 36 01         [10]  441 	ld	(hl), #0x01
                            442 ;src/game.c:94: g_bossphase = 0;
   41E5 21 07 65      [10]  443 	ld	hl,#_g_bossphase + 0
   41E8 36 00         [10]  444 	ld	(hl), #0x00
   41EA C9            [10]  445 	ret
                            446 ;src/game.c:97: static void try_fire_projectile(void) {
                            447 ;	---------------------------------
                            448 ; Function try_fire_projectile
                            449 ; ---------------------------------
   41EB                     450 _try_fire_projectile:
   41EB DD E5         [15]  451 	push	ix
   41ED DD 21 00 00   [14]  452 	ld	ix,#0
   41F1 DD 39         [15]  453 	add	ix,sp
   41F3 F5            [11]  454 	push	af
   41F4 3B            [ 6]  455 	dec	sp
                            456 ;src/game.c:101: if (!input_is_shoot_just_pressed()) return;
   41F5 CD DD 52      [17]  457 	call	_input_is_shoot_just_pressed
   41F8 7D            [ 4]  458 	ld	a, l
   41F9 B7            [ 4]  459 	or	a, a
   41FA CA 8C 42      [10]  460 	jp	Z,00110$
                            461 ;src/game.c:102: if (g_shootcooldown) return;
   41FD 3A F4 64      [13]  462 	ld	a,(#_g_shootcooldown + 0)
   4200 B7            [ 4]  463 	or	a, a
   4201 C2 8C 42      [10]  464 	jp	NZ,00110$
                            465 ;src/game.c:104: dir = g_player.facing_left ? -3 : 3;
   4204 3A 71 64      [13]  466 	ld	a, (#_g_player + 8)
   4207 B7            [ 4]  467 	or	a, a
   4208 28 04         [12]  468 	jr	Z,00112$
   420A 0E FD         [ 7]  469 	ld	c, #0xfd
   420C 18 02         [12]  470 	jr	00113$
   420E                     471 00112$:
   420E 0E 03         [ 7]  472 	ld	c, #0x03
   4210                     473 00113$:
                            474 ;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4210 DD 36 FF 00   [19]  475 	ld	-1 (ix), #0x00
   4214 06 00         [ 7]  476 	ld	b, #0x00
   4216                     477 00108$:
                            478 ;src/game.c:107: if (!g_projectiles[i].active) {
   4216 58            [ 4]  479 	ld	e,b
   4217 16 00         [ 7]  480 	ld	d,#0x00
   4219 6B            [ 4]  481 	ld	l, e
   421A 62            [ 4]  482 	ld	h, d
   421B 29            [11]  483 	add	hl, hl
   421C 29            [11]  484 	add	hl, hl
   421D 19            [11]  485 	add	hl, de
   421E 29            [11]  486 	add	hl, hl
   421F 11 AF 64      [10]  487 	ld	de, #_g_projectiles
   4222 19            [11]  488 	add	hl, de
   4223 11 06 00      [10]  489 	ld	de, #0x0006
   4226 19            [11]  490 	add	hl, de
   4227 7E            [ 7]  491 	ld	a, (hl)
   4228 B7            [ 4]  492 	or	a, a
   4229 20 58         [12]  493 	jr	NZ,00109$
                            494 ;src/game.c:109: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
   422B 3A 08 65      [13]  495 	ld	a,(#_g_weaponlevel + 0)
   422E B7            [ 4]  496 	or	a, a
   422F 28 06         [12]  497 	jr	Z,00114$
   4231 DD 36 FE 01   [19]  498 	ld	-2 (ix), #0x01
   4235 18 04         [12]  499 	jr	00115$
   4237                     500 00114$:
   4237 DD 36 FE 00   [19]  501 	ld	-2 (ix), #0x00
   423B                     502 00115$:
   423B 3A 6A 64      [13]  503 	ld	a, (#_g_player + 1)
   423E C6 06         [ 7]  504 	add	a, #0x06
   4240 DD 77 FD      [19]  505 	ld	-3 (ix), a
   4243 21 69 64      [10]  506 	ld	hl, #_g_player + 0
   4246 46            [ 7]  507 	ld	b, (hl)
   4247 04            [ 4]  508 	inc	b
   4248 04            [ 4]  509 	inc	b
   4249 DD 5E FF      [19]  510 	ld	e,-1 (ix)
   424C 16 00         [ 7]  511 	ld	d,#0x00
   424E 6B            [ 4]  512 	ld	l, e
   424F 62            [ 4]  513 	ld	h, d
   4250 29            [11]  514 	add	hl, hl
   4251 29            [11]  515 	add	hl, hl
   4252 19            [11]  516 	add	hl, de
   4253 29            [11]  517 	add	hl, hl
   4254 11 AF 64      [10]  518 	ld	de, #_g_projectiles
   4257 19            [11]  519 	add	hl, de
   4258 EB            [ 4]  520 	ex	de,hl
   4259 DD 7E FE      [19]  521 	ld	a, -2 (ix)
   425C F5            [11]  522 	push	af
   425D 33            [ 6]  523 	inc	sp
   425E 79            [ 4]  524 	ld	a, c
   425F F5            [11]  525 	push	af
   4260 33            [ 6]  526 	inc	sp
   4261 DD 7E FD      [19]  527 	ld	a, -3 (ix)
   4264 F5            [11]  528 	push	af
   4265 33            [ 6]  529 	inc	sp
   4266 C5            [11]  530 	push	bc
   4267 33            [ 6]  531 	inc	sp
   4268 D5            [11]  532 	push	de
   4269 CD F8 5F      [17]  533 	call	_projectilefire
   426C 21 06 00      [10]  534 	ld	hl, #6
   426F 39            [11]  535 	add	hl, sp
   4270 F9            [ 6]  536 	ld	sp, hl
                            537 ;src/game.c:110: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
   4271 3A 08 65      [13]  538 	ld	a,(#_g_weaponlevel + 0)
   4274 B7            [ 4]  539 	or	a, a
   4275 28 04         [12]  540 	jr	Z,00116$
   4277 0E 04         [ 7]  541 	ld	c, #0x04
   4279 18 02         [12]  542 	jr	00117$
   427B                     543 00116$:
   427B 0E 08         [ 7]  544 	ld	c, #0x08
   427D                     545 00117$:
   427D 21 F4 64      [10]  546 	ld	hl,#_g_shootcooldown + 0
   4280 71            [ 7]  547 	ld	(hl), c
                            548 ;src/game.c:111: break;
   4281 18 09         [12]  549 	jr	00110$
   4283                     550 00109$:
                            551 ;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4283 04            [ 4]  552 	inc	b
   4284 DD 70 FF      [19]  553 	ld	-1 (ix), b
   4287 78            [ 4]  554 	ld	a, b
   4288 D6 06         [ 7]  555 	sub	a, #0x06
   428A 38 8A         [12]  556 	jr	C,00108$
   428C                     557 00110$:
   428C DD F9         [10]  558 	ld	sp, ix
   428E DD E1         [14]  559 	pop	ix
   4290 C9            [10]  560 	ret
                            561 ;src/game.c:116: static void register_player_hit(void) {
                            562 ;	---------------------------------
                            563 ; Function register_player_hit
                            564 ; ---------------------------------
   4291                     565 _register_player_hit:
                            566 ;src/game.c:117: if (g_lives) {
   4291 FD 21 EB 64   [14]  567 	ld	iy, #_g_lives
   4295 FD 7E 00      [19]  568 	ld	a, 0 (iy)
   4298 B7            [ 4]  569 	or	a, a
   4299 28 03         [12]  570 	jr	Z,00102$
                            571 ;src/game.c:118: g_lives--;
   429B FD 35 00      [23]  572 	dec	0 (iy)
   429E                     573 00102$:
                            574 ;src/game.c:120: if (g_lives == 0) {
   429E 3A EB 64      [13]  575 	ld	a,(#_g_lives + 0)
   42A1 B7            [ 4]  576 	or	a, a
   42A2 20 06         [12]  577 	jr	NZ,00104$
                            578 ;src/game.c:121: g_gameover = 1;
   42A4 21 F6 64      [10]  579 	ld	hl,#_g_gameover + 0
   42A7 36 01         [10]  580 	ld	(hl), #0x01
                            581 ;src/game.c:122: return;
   42A9 C9            [10]  582 	ret
   42AA                     583 00104$:
                            584 ;src/game.c:125: reset_player_to_checkpoint();
   42AA CD 00 40      [17]  585 	call	_reset_player_to_checkpoint
                            586 ;src/game.c:126: g_damagecooldown = 40;
   42AD 21 F3 64      [10]  587 	ld	hl,#_g_damagecooldown + 0
   42B0 36 28         [10]  588 	ld	(hl), #0x28
   42B2 C9            [10]  589 	ret
                            590 ;src/game.c:129: void game_init(void) {
                            591 ;	---------------------------------
                            592 ; Function game_init
                            593 ; ---------------------------------
   42B3                     594 _game_init::
                            595 ;src/game.c:132: cpct_disableFirmware();
   42B3 CD 70 63      [17]  596 	call	_cpct_disableFirmware
                            597 ;src/game.c:133: cpct_setVideoMode(0);
   42B6 2E 00         [ 7]  598 	ld	l, #0x00
   42B8 CD 38 63      [17]  599 	call	_cpct_setVideoMode
                            600 ;src/game.c:134: cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
   42BB 21 10 00      [10]  601 	ld	hl, #0x0010
   42BE E5            [11]  602 	push	hl
   42BF 21 8C 54      [10]  603 	ld	hl, #_gpalette
   42C2 E5            [11]  604 	push	hl
   42C3 CD 47 62      [17]  605 	call	_cpct_setPalette
                            606 ;src/game.c:135: cpct_setBorder(gpalette[0]);
   42C6 21 8C 54      [10]  607 	ld	hl, #_gpalette + 0
   42C9 46            [ 7]  608 	ld	b, (hl)
   42CA C5            [11]  609 	push	bc
   42CB 33            [ 6]  610 	inc	sp
   42CC 3E 10         [ 7]  611 	ld	a, #0x10
   42CE F5            [11]  612 	push	af
   42CF 33            [ 6]  613 	inc	sp
   42D0 CD 5E 62      [17]  614 	call	_cpct_setPALColour
                            615 ;src/game.c:136: cpct_clearScreen(0x00);
   42D3 21 00 40      [10]  616 	ld	hl, #0x4000
   42D6 E5            [11]  617 	push	hl
   42D7 AF            [ 4]  618 	xor	a, a
   42D8 F5            [11]  619 	push	af
   42D9 33            [ 6]  620 	inc	sp
   42DA 26 C0         [ 7]  621 	ld	h, #0xc0
   42DC E5            [11]  622 	push	hl
   42DD CD 62 63      [17]  623 	call	_cpct_memset
                            624 ;src/game.c:137: tilemap_init();
   42E0 CD EF 52      [17]  625 	call	_tilemap_init
                            626 ;src/game.c:138: collision_init();
   42E3 CD CC 4C      [17]  627 	call	_collision_init
                            628 ;src/game.c:139: playerinit(&g_player);
   42E6 21 69 64      [10]  629 	ld	hl, #_g_player
   42E9 E5            [11]  630 	push	hl
   42EA CD 8D 5C      [17]  631 	call	_playerinit
   42ED F1            [10]  632 	pop	af
                            633 ;src/game.c:140: hudinit();
   42EE CD D1 50      [17]  634 	call	_hudinit
                            635 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42F1 0E 00         [ 7]  636 	ld	c, #0x00
   42F3                     637 00102$:
                            638 ;src/game.c:143: projectileinit(&g_projectiles[i]);
   42F3 06 00         [ 7]  639 	ld	b,#0x00
   42F5 69            [ 4]  640 	ld	l, c
   42F6 60            [ 4]  641 	ld	h, b
   42F7 29            [11]  642 	add	hl, hl
   42F8 29            [11]  643 	add	hl, hl
   42F9 09            [11]  644 	add	hl, bc
   42FA 29            [11]  645 	add	hl, hl
   42FB 11 AF 64      [10]  646 	ld	de, #_g_projectiles
   42FE 19            [11]  647 	add	hl, de
   42FF C5            [11]  648 	push	bc
   4300 E5            [11]  649 	push	hl
   4301 CD 9B 5F      [17]  650 	call	_projectileinit
   4304 F1            [10]  651 	pop	af
   4305 C1            [10]  652 	pop	bc
                            653 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4306 0C            [ 4]  654 	inc	c
   4307 79            [ 4]  655 	ld	a, c
   4308 D6 06         [ 7]  656 	sub	a, #0x06
   430A 38 E7         [12]  657 	jr	C,00102$
                            658 ;src/game.c:146: g_lives = 3;
   430C 21 EB 64      [10]  659 	ld	hl,#_g_lives + 0
   430F 36 03         [10]  660 	ld	(hl), #0x03
                            661 ;src/game.c:147: g_score = 0;
   4311 21 00 00      [10]  662 	ld	hl, #0x0000
   4314 22 EC 64      [16]  663 	ld	(_g_score), hl
                            664 ;src/game.c:148: g_timeleft = 99;
   4317 FD 21 EE 64   [14]  665 	ld	iy, #_g_timeleft
   431B FD 36 00 63   [19]  666 	ld	0 (iy), #0x63
                            667 ;src/game.c:149: g_weapondisplay = 1;
   431F FD 21 EF 64   [14]  668 	ld	iy, #_g_weapondisplay
   4323 FD 36 00 01   [19]  669 	ld	0 (iy), #0x01
                            670 ;src/game.c:150: g_currentwave = 0;
   4327 FD 21 F0 64   [14]  671 	ld	iy, #_g_currentwave
   432B FD 36 00 00   [19]  672 	ld	0 (iy), #0x00
                            673 ;src/game.c:151: g_wavecooldown = 1;
   432F FD 21 F2 64   [14]  674 	ld	iy, #_g_wavecooldown
   4333 FD 36 00 01   [19]  675 	ld	0 (iy), #0x01
                            676 ;src/game.c:152: g_damagecooldown = 0;
   4337 FD 21 F3 64   [14]  677 	ld	iy, #_g_damagecooldown
   433B FD 36 00 00   [19]  678 	ld	0 (iy), #0x00
                            679 ;src/game.c:153: g_shootcooldown = 0;
   433F FD 21 F4 64   [14]  680 	ld	iy, #_g_shootcooldown
   4343 FD 36 00 00   [19]  681 	ld	0 (iy), #0x00
                            682 ;src/game.c:154: g_victory = 0;
   4347 FD 21 F5 64   [14]  683 	ld	iy, #_g_victory
   434B FD 36 00 00   [19]  684 	ld	0 (iy), #0x00
                            685 ;src/game.c:155: g_gameover = 0;
   434F FD 21 F6 64   [14]  686 	ld	iy, #_g_gameover
   4353 FD 36 00 00   [19]  687 	ld	0 (iy), #0x00
                            688 ;src/game.c:156: g_framecounter = 0;
   4357 2E 00         [ 7]  689 	ld	l, #0x00
   4359 22 F7 64      [16]  690 	ld	(_g_framecounter), hl
                            691 ;src/game.c:157: g_checkpointx = 20;
   435C 21 F9 64      [10]  692 	ld	hl,#_g_checkpointx + 0
   435F 36 14         [10]  693 	ld	(hl), #0x14
                            694 ;src/game.c:158: g_checkpointy = 120;
   4361 21 FA 64      [10]  695 	ld	hl,#_g_checkpointy + 0
   4364 36 78         [10]  696 	ld	(hl), #0x78
                            697 ;src/game.c:159: g_checkpointactive = 0;
   4366 21 FB 64      [10]  698 	ld	hl,#_g_checkpointactive + 0
   4369 36 00         [10]  699 	ld	(hl), #0x00
                            700 ;src/game.c:160: g_bossactive = 0;
   436B 21 06 65      [10]  701 	ld	hl,#_g_bossactive + 0
   436E 36 00         [10]  702 	ld	(hl), #0x00
                            703 ;src/game.c:161: g_weaponlevel = 0;
   4370 21 08 65      [10]  704 	ld	hl,#_g_weaponlevel + 0
   4373 36 00         [10]  705 	ld	(hl), #0x00
                            706 ;src/game.c:162: g_pickuptaken = 0;
   4375 21 09 65      [10]  707 	ld	hl,#_g_pickuptaken + 0
   4378 36 00         [10]  708 	ld	(hl), #0x00
                            709 ;src/game.c:163: enemyinit(&g_boss);
   437A 21 FC 64      [10]  710 	ld	hl, #_g_boss
   437D E5            [11]  711 	push	hl
   437E CD 1C 56      [17]  712 	call	_enemyinit
   4381 F1            [10]  713 	pop	af
   4382 C9            [10]  714 	ret
                            715 ;src/game.c:166: void game_update(void) {
                            716 ;	---------------------------------
                            717 ; Function game_update
                            718 ; ---------------------------------
   4383                     719 _game_update::
   4383 DD E5         [15]  720 	push	ix
   4385 DD 21 00 00   [14]  721 	ld	ix,#0
   4389 DD 39         [15]  722 	add	ix,sp
   438B 21 E7 FF      [10]  723 	ld	hl, #-25
   438E 39            [11]  724 	add	hl, sp
   438F F9            [ 6]  725 	ld	sp, hl
                            726 ;src/game.c:170: input_update();
   4390 CD DC 51      [17]  727 	call	_input_update
                            728 ;src/game.c:172: if (g_gameover || g_victory) {
   4393 3A F6 64      [13]  729 	ld	a,(#_g_gameover + 0)
   4396 B7            [ 4]  730 	or	a, a
   4397 20 06         [12]  731 	jr	NZ,00101$
   4399 3A F5 64      [13]  732 	ld	a,(#_g_victory + 0)
   439C B7            [ 4]  733 	or	a, a
   439D 28 1C         [12]  734 	jr	Z,00102$
   439F                     735 00101$:
                            736 ;src/game.c:173: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   439F 3A EF 64      [13]  737 	ld	a, (_g_weapondisplay)
   43A2 F5            [11]  738 	push	af
   43A3 33            [ 6]  739 	inc	sp
   43A4 3A EE 64      [13]  740 	ld	a, (_g_timeleft)
   43A7 F5            [11]  741 	push	af
   43A8 33            [ 6]  742 	inc	sp
   43A9 2A EC 64      [16]  743 	ld	hl, (_g_score)
   43AC E5            [11]  744 	push	hl
   43AD 3A EB 64      [13]  745 	ld	a, (_g_lives)
   43B0 F5            [11]  746 	push	af
   43B1 33            [ 6]  747 	inc	sp
   43B2 CD EC 50      [17]  748 	call	_hudupdate
   43B5 F1            [10]  749 	pop	af
   43B6 F1            [10]  750 	pop	af
   43B7 33            [ 6]  751 	inc	sp
                            752 ;src/game.c:174: return;
   43B8 C3 A6 49      [10]  753 	jp	00181$
   43BB                     754 00102$:
                            755 ;src/game.c:177: playerupdate(&g_player);
   43BB 21 69 64      [10]  756 	ld	hl, #_g_player
   43BE E5            [11]  757 	push	hl
   43BF CD D3 5C      [17]  758 	call	_playerupdate
   43C2 F1            [10]  759 	pop	af
                            760 ;src/game.c:178: try_fire_projectile();
   43C3 CD EB 41      [17]  761 	call	_try_fire_projectile
                            762 ;src/game.c:180: if (g_shootcooldown) g_shootcooldown--;
   43C6 FD 21 F4 64   [14]  763 	ld	iy, #_g_shootcooldown
   43CA FD 7E 00      [19]  764 	ld	a, 0 (iy)
   43CD B7            [ 4]  765 	or	a, a
   43CE 28 03         [12]  766 	jr	Z,00105$
   43D0 FD 35 00      [23]  767 	dec	0 (iy)
   43D3                     768 00105$:
                            769 ;src/game.c:181: if (g_damagecooldown) g_damagecooldown--;
   43D3 FD 21 F3 64   [14]  770 	ld	iy, #_g_damagecooldown
   43D7 FD 7E 00      [19]  771 	ld	a, 0 (iy)
   43DA B7            [ 4]  772 	or	a, a
   43DB 28 03         [12]  773 	jr	Z,00192$
   43DD FD 35 00      [23]  774 	dec	0 (iy)
                            775 ;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43E0                     776 00192$:
   43E0 0E 00         [ 7]  777 	ld	c, #0x00
   43E2                     778 00174$:
                            779 ;src/game.c:184: projectileupdate(&g_projectiles[i]);
   43E2 06 00         [ 7]  780 	ld	b,#0x00
   43E4 69            [ 4]  781 	ld	l, c
   43E5 60            [ 4]  782 	ld	h, b
   43E6 29            [11]  783 	add	hl, hl
   43E7 29            [11]  784 	add	hl, hl
   43E8 09            [11]  785 	add	hl, bc
   43E9 29            [11]  786 	add	hl, hl
   43EA 11 AF 64      [10]  787 	ld	de, #_g_projectiles
   43ED 19            [11]  788 	add	hl, de
   43EE C5            [11]  789 	push	bc
   43EF E5            [11]  790 	push	hl
   43F0 CD AF 60      [17]  791 	call	_projectileupdate
   43F3 F1            [10]  792 	pop	af
   43F4 C1            [10]  793 	pop	bc
                            794 ;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43F5 0C            [ 4]  795 	inc	c
   43F6 79            [ 4]  796 	ld	a, c
   43F7 D6 06         [ 7]  797 	sub	a, #0x06
   43F9 38 E7         [12]  798 	jr	C,00174$
                            799 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   43FB 0E 00         [ 7]  800 	ld	c, #0x00
   43FD                     801 00176$:
                            802 ;src/game.c:188: enemyupdate(&g_enemies[i]);
   43FD 06 00         [ 7]  803 	ld	b,#0x00
   43FF 69            [ 4]  804 	ld	l, c
   4400 60            [ 4]  805 	ld	h, b
   4401 29            [11]  806 	add	hl, hl
   4402 29            [11]  807 	add	hl, hl
   4403 09            [11]  808 	add	hl, bc
   4404 29            [11]  809 	add	hl, hl
   4405 11 73 64      [10]  810 	ld	de, #_g_enemies
   4408 19            [11]  811 	add	hl, de
   4409 C5            [11]  812 	push	bc
   440A E5            [11]  813 	push	hl
   440B CD AF 59      [17]  814 	call	_enemyupdate
   440E F1            [10]  815 	pop	af
   440F C1            [10]  816 	pop	bc
                            817 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   4410 0C            [ 4]  818 	inc	c
   4411 79            [ 4]  819 	ld	a, c
   4412 D6 06         [ 7]  820 	sub	a, #0x06
   4414 38 E7         [12]  821 	jr	C,00176$
                            822 ;src/game.c:191: if (g_bossactive) {
   4416 3A 06 65      [13]  823 	ld	a,(#_g_bossactive + 0)
   4419 B7            [ 4]  824 	or	a, a
   441A 28 71         [12]  825 	jr	Z,00211$
                            826 ;src/game.c:192: if (g_boss.health > 4) g_bossphase = 0;
   441C 21 03 65      [10]  827 	ld	hl, #_g_boss + 7
   441F 4E            [ 7]  828 	ld	c, (hl)
   4420 3E 04         [ 7]  829 	ld	a, #0x04
   4422 91            [ 4]  830 	sub	a, c
   4423 30 07         [12]  831 	jr	NC,00111$
   4425 21 07 65      [10]  832 	ld	hl,#_g_bossphase + 0
   4428 36 00         [10]  833 	ld	(hl), #0x00
   442A 18 05         [12]  834 	jr	00112$
   442C                     835 00111$:
                            836 ;src/game.c:193: else g_bossphase = 1;
   442C 21 07 65      [10]  837 	ld	hl,#_g_bossphase + 0
   442F 36 01         [10]  838 	ld	(hl), #0x01
   4431                     839 00112$:
                            840 ;src/game.c:195: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4431 3A 69 64      [13]  841 	ld	a,(#_g_player + 0)
   4434 DD 77 EB      [19]  842 	ld	-21 (ix), a
   4437 DD 77 E9      [19]  843 	ld	-23 (ix), a
   443A DD 36 EA 00   [19]  844 	ld	-22 (ix), #0x00
   443E DD 7E E9      [19]  845 	ld	a, -23 (ix)
   4441 C6 02         [ 7]  846 	add	a, #0x02
   4443 DD 77 E9      [19]  847 	ld	-23 (ix), a
   4446 DD 7E EA      [19]  848 	ld	a, -22 (ix)
   4449 CE 00         [ 7]  849 	adc	a, #0x00
   444B DD 77 EA      [19]  850 	ld	-22 (ix), a
   444E 21 FC 64      [10]  851 	ld	hl, #_g_boss + 0
   4451 4E            [ 7]  852 	ld	c, (hl)
   4452 06 00         [ 7]  853 	ld	b, #0x00
   4454 DD 7E E9      [19]  854 	ld	a, -23 (ix)
   4457 91            [ 4]  855 	sub	a, c
   4458 DD 7E EA      [19]  856 	ld	a, -22 (ix)
   445B 98            [ 4]  857 	sbc	a, b
   445C E2 61 44      [10]  858 	jp	PO, 00380$
   445F EE 80         [ 7]  859 	xor	a, #0x80
   4461                     860 00380$:
   4461 F2 75 44      [10]  861 	jp	P, 00183$
   4464 3A 07 65      [13]  862 	ld	a,(#_g_bossphase + 0)
   4467 B7            [ 4]  863 	or	a, a
   4468 28 04         [12]  864 	jr	Z,00185$
   446A 0E 02         [ 7]  865 	ld	c, #0x02
   446C 18 02         [12]  866 	jr	00186$
   446E                     867 00185$:
   446E 0E 01         [ 7]  868 	ld	c, #0x01
   4470                     869 00186$:
   4470 AF            [ 4]  870 	xor	a, a
   4471 91            [ 4]  871 	sub	a, c
   4472 4F            [ 4]  872 	ld	c, a
   4473 18 0C         [12]  873 	jr	00184$
   4475                     874 00183$:
   4475 3A 07 65      [13]  875 	ld	a,(#_g_bossphase + 0)
   4478 B7            [ 4]  876 	or	a, a
   4479 28 04         [12]  877 	jr	Z,00187$
   447B 0E 02         [ 7]  878 	ld	c, #0x02
   447D 18 02         [12]  879 	jr	00188$
   447F                     880 00187$:
   447F 0E 01         [ 7]  881 	ld	c, #0x01
   4481                     882 00188$:
   4481                     883 00184$:
   4481 21 FE 64      [10]  884 	ld	hl, #(_g_boss + 0x0002)
   4484 71            [ 7]  885 	ld	(hl), c
                            886 ;src/game.c:196: enemyupdate(&g_boss);
   4485 21 FC 64      [10]  887 	ld	hl, #_g_boss
   4488 E5            [11]  888 	push	hl
   4489 CD AF 59      [17]  889 	call	_enemyupdate
   448C F1            [10]  890 	pop	af
                            891 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   448D                     892 00211$:
   448D 0E 00         [ 7]  893 	ld	c, #0x00
   448F                     894 00179$:
                            895 ;src/game.c:200: if (!g_projectiles[i].active) continue;
   448F 06 00         [ 7]  896 	ld	b,#0x00
   4491 69            [ 4]  897 	ld	l, c
   4492 60            [ 4]  898 	ld	h, b
   4493 29            [11]  899 	add	hl, hl
   4494 29            [11]  900 	add	hl, hl
   4495 09            [11]  901 	add	hl, bc
   4496 29            [11]  902 	add	hl, hl
   4497 EB            [ 4]  903 	ex	de,hl
   4498 21 AF 64      [10]  904 	ld	hl, #_g_projectiles
   449B 19            [11]  905 	add	hl,de
   449C EB            [ 4]  906 	ex	de,hl
   449D 21 06 00      [10]  907 	ld	hl, #0x0006
   44A0 19            [11]  908 	add	hl,de
   44A1 DD 75 E9      [19]  909 	ld	-23 (ix), l
   44A4 DD 74 EA      [19]  910 	ld	-22 (ix), h
   44A7 7E            [ 7]  911 	ld	a, (hl)
   44A8 B7            [ 4]  912 	or	a, a
   44A9 CA CA 46      [10]  913 	jp	Z, 00133$
                            914 ;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
   44AC DD 36 E7 00   [19]  915 	ld	-25 (ix), #0x00
   44B0                     916 00178$:
                            917 ;src/game.c:202: if (!g_enemies[j].active) continue;
   44B0 D5            [11]  918 	push	de
   44B1 DD 5E E7      [19]  919 	ld	e,-25 (ix)
   44B4 16 00         [ 7]  920 	ld	d,#0x00
   44B6 6B            [ 4]  921 	ld	l, e
   44B7 62            [ 4]  922 	ld	h, d
   44B8 29            [11]  923 	add	hl, hl
   44B9 29            [11]  924 	add	hl, hl
   44BA 19            [11]  925 	add	hl, de
   44BB 29            [11]  926 	add	hl, hl
   44BC D1            [10]  927 	pop	de
   44BD 3E 73         [ 7]  928 	ld	a, #<(_g_enemies)
   44BF 85            [ 4]  929 	add	a, l
   44C0 DD 77 FE      [19]  930 	ld	-2 (ix), a
   44C3 3E 64         [ 7]  931 	ld	a, #>(_g_enemies)
   44C5 8C            [ 4]  932 	adc	a, h
   44C6 DD 77 FF      [19]  933 	ld	-1 (ix), a
   44C9 DD 6E FE      [19]  934 	ld	l,-2 (ix)
   44CC DD 66 FF      [19]  935 	ld	h,-1 (ix)
   44CF C5            [11]  936 	push	bc
   44D0 01 06 00      [10]  937 	ld	bc, #0x0006
   44D3 09            [11]  938 	add	hl, bc
   44D4 C1            [10]  939 	pop	bc
   44D5 46            [ 7]  940 	ld	b, (hl)
                            941 ;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   44D6 21 05 00      [10]  942 	ld	hl, #0x0005
   44D9 19            [11]  943 	add	hl,de
   44DA DD 75 FC      [19]  944 	ld	-4 (ix), l
   44DD DD 74 FD      [19]  945 	ld	-3 (ix), h
   44E0 21 04 00      [10]  946 	ld	hl, #0x0004
   44E3 19            [11]  947 	add	hl,de
   44E4 DD 75 FA      [19]  948 	ld	-6 (ix), l
   44E7 DD 74 FB      [19]  949 	ld	-5 (ix), h
   44EA 21 01 00      [10]  950 	ld	hl, #0x0001
   44ED 19            [11]  951 	add	hl,de
   44EE DD 75 F8      [19]  952 	ld	-8 (ix), l
   44F1 DD 74 F9      [19]  953 	ld	-7 (ix), h
                            954 ;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44F4 21 07 00      [10]  955 	ld	hl, #0x0007
   44F7 19            [11]  956 	add	hl,de
   44F8 DD 75 F6      [19]  957 	ld	-10 (ix), l
   44FB DD 74 F7      [19]  958 	ld	-9 (ix), h
                            959 ;src/game.c:202: if (!g_enemies[j].active) continue;
   44FE 78            [ 4]  960 	ld	a, b
   44FF B7            [ 4]  961 	or	a, a
   4500 CA F8 45      [10]  962 	jp	Z, 00125$
                            963 ;src/game.c:204: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   4503 DD 6E FE      [19]  964 	ld	l,-2 (ix)
   4506 DD 66 FF      [19]  965 	ld	h,-1 (ix)
   4509 23            [ 6]  966 	inc	hl
   450A 23            [ 6]  967 	inc	hl
   450B 23            [ 6]  968 	inc	hl
   450C 23            [ 6]  969 	inc	hl
   450D 23            [ 6]  970 	inc	hl
   450E 7E            [ 7]  971 	ld	a, (hl)
   450F DD 77 EB      [19]  972 	ld	-21 (ix), a
   4512 DD 6E FE      [19]  973 	ld	l,-2 (ix)
   4515 DD 66 FF      [19]  974 	ld	h,-1 (ix)
   4518 23            [ 6]  975 	inc	hl
   4519 23            [ 6]  976 	inc	hl
   451A 23            [ 6]  977 	inc	hl
   451B 23            [ 6]  978 	inc	hl
   451C 7E            [ 7]  979 	ld	a, (hl)
   451D DD 77 F5      [19]  980 	ld	-11 (ix), a
   4520 DD 6E FE      [19]  981 	ld	l,-2 (ix)
   4523 DD 66 FF      [19]  982 	ld	h,-1 (ix)
   4526 23            [ 6]  983 	inc	hl
   4527 46            [ 7]  984 	ld	b, (hl)
   4528 DD 70 F3      [19]  985 	ld	-13 (ix), b
   452B DD 36 F4 00   [19]  986 	ld	-12 (ix), #0x00
   452F DD 6E FE      [19]  987 	ld	l,-2 (ix)
   4532 DD 66 FF      [19]  988 	ld	h,-1 (ix)
   4535 46            [ 7]  989 	ld	b, (hl)
   4536 DD 70 F1      [19]  990 	ld	-15 (ix), b
   4539 DD 36 F2 00   [19]  991 	ld	-14 (ix), #0x00
                            992 ;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   453D DD 6E FC      [19]  993 	ld	l,-4 (ix)
   4540 DD 66 FD      [19]  994 	ld	h,-3 (ix)
   4543 7E            [ 7]  995 	ld	a, (hl)
   4544 DD 77 F0      [19]  996 	ld	-16 (ix), a
   4547 DD 6E FA      [19]  997 	ld	l,-6 (ix)
   454A DD 66 FB      [19]  998 	ld	h,-5 (ix)
   454D 46            [ 7]  999 	ld	b, (hl)
   454E DD 6E F8      [19] 1000 	ld	l,-8 (ix)
   4551 DD 66 F9      [19] 1001 	ld	h,-7 (ix)
   4554 6E            [ 7] 1002 	ld	l, (hl)
   4555 DD 75 EE      [19] 1003 	ld	-18 (ix), l
   4558 DD 36 EF 00   [19] 1004 	ld	-17 (ix), #0x00
   455C 1A            [ 7] 1005 	ld	a, (de)
   455D DD 77 EC      [19] 1006 	ld	-20 (ix), a
   4560 DD 36 ED 00   [19] 1007 	ld	-19 (ix), #0x00
   4564 C5            [11] 1008 	push	bc
   4565 D5            [11] 1009 	push	de
   4566 DD 66 EB      [19] 1010 	ld	h, -21 (ix)
   4569 DD 6E F5      [19] 1011 	ld	l, -11 (ix)
   456C E5            [11] 1012 	push	hl
   456D DD 6E F3      [19] 1013 	ld	l,-13 (ix)
   4570 DD 66 F4      [19] 1014 	ld	h,-12 (ix)
   4573 E5            [11] 1015 	push	hl
   4574 DD 6E F1      [19] 1016 	ld	l,-15 (ix)
   4577 DD 66 F2      [19] 1017 	ld	h,-14 (ix)
   457A E5            [11] 1018 	push	hl
   457B DD 7E F0      [19] 1019 	ld	a, -16 (ix)
   457E F5            [11] 1020 	push	af
   457F 33            [ 6] 1021 	inc	sp
   4580 C5            [11] 1022 	push	bc
   4581 33            [ 6] 1023 	inc	sp
   4582 DD 6E EE      [19] 1024 	ld	l,-18 (ix)
   4585 DD 66 EF      [19] 1025 	ld	h,-17 (ix)
   4588 E5            [11] 1026 	push	hl
   4589 DD 6E EC      [19] 1027 	ld	l,-20 (ix)
   458C DD 66 ED      [19] 1028 	ld	h,-19 (ix)
   458F E5            [11] 1029 	push	hl
   4590 CD 19 40      [17] 1030 	call	_rect_overlap
   4593 FD 21 0C 00   [14] 1031 	ld	iy, #12
   4597 FD 39         [15] 1032 	add	iy, sp
   4599 FD F9         [10] 1033 	ld	sp, iy
   459B D1            [10] 1034 	pop	de
   459C C1            [10] 1035 	pop	bc
   459D 7D            [ 4] 1036 	ld	a, l
   459E B7            [ 4] 1037 	or	a, a
   459F 28 57         [12] 1038 	jr	Z,00125$
                           1039 ;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   45A1 DD 6E F6      [19] 1040 	ld	l,-10 (ix)
   45A4 DD 66 F7      [19] 1041 	ld	h,-9 (ix)
   45A7 66            [ 7] 1042 	ld	h, (hl)
   45A8 DD 6E FE      [19] 1043 	ld	l, -2 (ix)
   45AB DD 46 FF      [19] 1044 	ld	b, -1 (ix)
   45AE C5            [11] 1045 	push	bc
   45AF D5            [11] 1046 	push	de
   45B0 E5            [11] 1047 	push	hl
   45B1 33            [ 6] 1048 	inc	sp
   45B2 60            [ 4] 1049 	ld	h, b
   45B3 E5            [11] 1050 	push	hl
   45B4 CD 4D 5C      [17] 1051 	call	_enemydamage
   45B7 F1            [10] 1052 	pop	af
   45B8 33            [ 6] 1053 	inc	sp
   45B9 D1            [10] 1054 	pop	de
   45BA C1            [10] 1055 	pop	bc
   45BB 7D            [ 4] 1056 	ld	a, l
   45BC B7            [ 4] 1057 	or	a, a
   45BD 28 2F         [12] 1058 	jr	Z,00124$
                           1059 ;src/game.c:206: g_score = (u16)(g_score + g_enemies[j].reward);
   45BF DD 6E FE      [19] 1060 	ld	l,-2 (ix)
   45C2 DD 66 FF      [19] 1061 	ld	h,-1 (ix)
   45C5 C5            [11] 1062 	push	bc
   45C6 01 08 00      [10] 1063 	ld	bc, #0x0008
   45C9 09            [11] 1064 	add	hl, bc
   45CA C1            [10] 1065 	pop	bc
   45CB 6E            [ 7] 1066 	ld	l, (hl)
   45CC DD 75 EC      [19] 1067 	ld	-20 (ix), l
   45CF DD 36 ED 00   [19] 1068 	ld	-19 (ix), #0x00
   45D3 21 EC 64      [10] 1069 	ld	hl, #_g_score
   45D6 7E            [ 7] 1070 	ld	a, (hl)
   45D7 DD 86 EC      [19] 1071 	add	a, -20 (ix)
   45DA 77            [ 7] 1072 	ld	(hl), a
   45DB 23            [ 6] 1073 	inc	hl
   45DC 7E            [ 7] 1074 	ld	a, (hl)
   45DD DD 8E ED      [19] 1075 	adc	a, -19 (ix)
   45E0 77            [ 7] 1076 	ld	(hl), a
                           1077 ;src/game.c:207: if (g_aliveenemies) g_aliveenemies--;
   45E1 FD 21 F1 64   [14] 1078 	ld	iy, #_g_aliveenemies
   45E5 FD 7E 00      [19] 1079 	ld	a, 0 (iy)
   45E8 B7            [ 4] 1080 	or	a, a
   45E9 28 03         [12] 1081 	jr	Z,00124$
   45EB FD 35 00      [23] 1082 	dec	0 (iy)
   45EE                    1083 00124$:
                           1084 ;src/game.c:209: g_projectiles[i].active = 0;
   45EE DD 6E E9      [19] 1085 	ld	l,-23 (ix)
   45F1 DD 66 EA      [19] 1086 	ld	h,-22 (ix)
   45F4 36 00         [10] 1087 	ld	(hl), #0x00
                           1088 ;src/game.c:210: break;
   45F6 18 0B         [12] 1089 	jr	00126$
   45F8                    1090 00125$:
                           1091 ;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
   45F8 DD 34 E7      [23] 1092 	inc	-25 (ix)
   45FB DD 7E E7      [19] 1093 	ld	a, -25 (ix)
   45FE D6 06         [ 7] 1094 	sub	a, #0x06
   4600 DA B0 44      [10] 1095 	jp	C, 00178$
   4603                    1096 00126$:
                           1097 ;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4603 3A 06 65      [13] 1098 	ld	a,(#_g_bossactive + 0)
   4606 B7            [ 4] 1099 	or	a, a
   4607 CA CA 46      [10] 1100 	jp	Z, 00133$
   460A DD 6E E9      [19] 1101 	ld	l,-23 (ix)
   460D DD 66 EA      [19] 1102 	ld	h,-22 (ix)
   4610 7E            [ 7] 1103 	ld	a, (hl)
   4611 B7            [ 4] 1104 	or	a, a
   4612 CA CA 46      [10] 1105 	jp	Z, 00133$
                           1106 ;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   4615 21 01 65      [10] 1107 	ld	hl, #(_g_boss + 0x0005) + 0
   4618 46            [ 7] 1108 	ld	b, (hl)
   4619 3A 00 65      [13] 1109 	ld	a, (#(_g_boss + 0x0004) + 0)
   461C 21 FD 64      [10] 1110 	ld	hl, #(_g_boss + 0x0001) + 0
   461F 6E            [ 7] 1111 	ld	l, (hl)
   4620 DD 75 EC      [19] 1112 	ld	-20 (ix), l
   4623 DD 36 ED 00   [19] 1113 	ld	-19 (ix), #0x00
   4627 21 FC 64      [10] 1114 	ld	hl, #_g_boss + 0
   462A 6E            [ 7] 1115 	ld	l, (hl)
   462B DD 75 EE      [19] 1116 	ld	-18 (ix), l
   462E DD 36 EF 00   [19] 1117 	ld	-17 (ix), #0x00
                           1118 ;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4632 DD 6E FC      [19] 1119 	ld	l,-4 (ix)
   4635 DD 66 FD      [19] 1120 	ld	h,-3 (ix)
   4638 F5            [11] 1121 	push	af
   4639 7E            [ 7] 1122 	ld	a, (hl)
   463A DD 77 F0      [19] 1123 	ld	-16 (ix), a
   463D F1            [10] 1124 	pop	af
   463E DD 6E FA      [19] 1125 	ld	l,-6 (ix)
   4641 DD 66 FB      [19] 1126 	ld	h,-5 (ix)
   4644 F5            [11] 1127 	push	af
   4645 7E            [ 7] 1128 	ld	a, (hl)
   4646 DD 77 F1      [19] 1129 	ld	-15 (ix), a
   4649 F1            [10] 1130 	pop	af
   464A DD 6E F8      [19] 1131 	ld	l,-8 (ix)
   464D DD 66 F9      [19] 1132 	ld	h,-7 (ix)
   4650 6E            [ 7] 1133 	ld	l, (hl)
   4651 DD 75 F3      [19] 1134 	ld	-13 (ix), l
   4654 DD 36 F4 00   [19] 1135 	ld	-12 (ix), #0x00
   4658 F5            [11] 1136 	push	af
   4659 1A            [ 7] 1137 	ld	a, (de)
   465A 5F            [ 4] 1138 	ld	e, a
   465B F1            [10] 1139 	pop	af
   465C 16 00         [ 7] 1140 	ld	d, #0x00
   465E C5            [11] 1141 	push	bc
   465F C5            [11] 1142 	push	bc
   4660 33            [ 6] 1143 	inc	sp
   4661 F5            [11] 1144 	push	af
   4662 33            [ 6] 1145 	inc	sp
   4663 DD 6E EC      [19] 1146 	ld	l,-20 (ix)
   4666 DD 66 ED      [19] 1147 	ld	h,-19 (ix)
   4669 E5            [11] 1148 	push	hl
   466A DD 6E EE      [19] 1149 	ld	l,-18 (ix)
   466D DD 66 EF      [19] 1150 	ld	h,-17 (ix)
   4670 E5            [11] 1151 	push	hl
   4671 DD 66 F0      [19] 1152 	ld	h, -16 (ix)
   4674 DD 6E F1      [19] 1153 	ld	l, -15 (ix)
   4677 E5            [11] 1154 	push	hl
   4678 DD 6E F3      [19] 1155 	ld	l,-13 (ix)
   467B DD 66 F4      [19] 1156 	ld	h,-12 (ix)
   467E E5            [11] 1157 	push	hl
   467F D5            [11] 1158 	push	de
   4680 CD 19 40      [17] 1159 	call	_rect_overlap
   4683 FD 21 0C 00   [14] 1160 	ld	iy, #12
   4687 FD 39         [15] 1161 	add	iy, sp
   4689 FD F9         [10] 1162 	ld	sp, iy
   468B C1            [10] 1163 	pop	bc
   468C 7D            [ 4] 1164 	ld	a, l
   468D B7            [ 4] 1165 	or	a, a
   468E 28 3A         [12] 1166 	jr	Z,00133$
                           1167 ;src/game.c:215: g_projectiles[i].active = 0;
   4690 DD 6E E9      [19] 1168 	ld	l,-23 (ix)
   4693 DD 66 EA      [19] 1169 	ld	h,-22 (ix)
   4696 36 00         [10] 1170 	ld	(hl), #0x00
                           1171 ;src/game.c:216: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   4698 DD 6E F6      [19] 1172 	ld	l,-10 (ix)
   469B DD 66 F7      [19] 1173 	ld	h,-9 (ix)
   469E 46            [ 7] 1174 	ld	b, (hl)
   469F 11 FC 64      [10] 1175 	ld	de, #_g_boss
   46A2 C5            [11] 1176 	push	bc
   46A3 C5            [11] 1177 	push	bc
   46A4 33            [ 6] 1178 	inc	sp
   46A5 D5            [11] 1179 	push	de
   46A6 CD 4D 5C      [17] 1180 	call	_enemydamage
   46A9 F1            [10] 1181 	pop	af
   46AA 33            [ 6] 1182 	inc	sp
   46AB C1            [10] 1183 	pop	bc
   46AC 7D            [ 4] 1184 	ld	a, l
   46AD B7            [ 4] 1185 	or	a, a
   46AE 28 1A         [12] 1186 	jr	Z,00133$
                           1187 ;src/game.c:217: g_bossactive = 0;
   46B0 21 06 65      [10] 1188 	ld	hl,#_g_bossactive + 0
   46B3 36 00         [10] 1189 	ld	(hl), #0x00
                           1190 ;src/game.c:218: g_score = (u16)(g_score + g_boss.reward);
   46B5 21 04 65      [10] 1191 	ld	hl, #_g_boss + 8
   46B8 5E            [ 7] 1192 	ld	e, (hl)
   46B9 16 00         [ 7] 1193 	ld	d, #0x00
   46BB 21 EC 64      [10] 1194 	ld	hl, #_g_score
   46BE 7E            [ 7] 1195 	ld	a, (hl)
   46BF 83            [ 4] 1196 	add	a, e
   46C0 77            [ 7] 1197 	ld	(hl), a
   46C1 23            [ 6] 1198 	inc	hl
   46C2 7E            [ 7] 1199 	ld	a, (hl)
   46C3 8A            [ 4] 1200 	adc	a, d
   46C4 77            [ 7] 1201 	ld	(hl), a
                           1202 ;src/game.c:219: g_victory = 1;
   46C5 21 F5 64      [10] 1203 	ld	hl,#_g_victory + 0
   46C8 36 01         [10] 1204 	ld	(hl), #0x01
   46CA                    1205 00133$:
                           1206 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   46CA 0C            [ 4] 1207 	inc	c
   46CB 79            [ 4] 1208 	ld	a, c
   46CC D6 06         [ 7] 1209 	sub	a, #0x06
   46CE DA 8F 44      [10] 1210 	jp	C, 00179$
                           1211 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1212 ;src/game.c:224: if (!g_damagecooldown) {
   46D1 3A F3 64      [13] 1213 	ld	a,(#_g_damagecooldown + 0)
   46D4 B7            [ 4] 1214 	or	a, a
   46D5 C2 44 48      [10] 1215 	jp	NZ, 00149$
                           1216 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   46D8 DD 36 E8 00   [19] 1217 	ld	-24 (ix), #0x00
   46DC                    1218 00180$:
                           1219 ;src/game.c:226: if (!g_enemies[i].active) continue;
   46DC DD 4E E8      [19] 1220 	ld	c,-24 (ix)
   46DF 06 00         [ 7] 1221 	ld	b,#0x00
   46E1 69            [ 4] 1222 	ld	l, c
   46E2 60            [ 4] 1223 	ld	h, b
   46E3 29            [11] 1224 	add	hl, hl
   46E4 29            [11] 1225 	add	hl, hl
   46E5 09            [11] 1226 	add	hl, bc
   46E6 29            [11] 1227 	add	hl, hl
   46E7 4D            [ 4] 1228 	ld	c, l
   46E8 44            [ 4] 1229 	ld	b, h
   46E9 21 73 64      [10] 1230 	ld	hl, #_g_enemies
   46EC 09            [11] 1231 	add	hl,bc
   46ED DD 75 EC      [19] 1232 	ld	-20 (ix), l
   46F0 DD 74 ED      [19] 1233 	ld	-19 (ix), h
   46F3 11 06 00      [10] 1234 	ld	de, #0x0006
   46F6 19            [11] 1235 	add	hl, de
   46F7 7E            [ 7] 1236 	ld	a, (hl)
   46F8 B7            [ 4] 1237 	or	a, a
   46F9 CA 8E 47      [10] 1238 	jp	Z, 00139$
                           1239 ;src/game.c:228: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   46FC DD 7E EC      [19] 1240 	ld	a, -20 (ix)
   46FF DD 77 EE      [19] 1241 	ld	-18 (ix), a
   4702 DD 7E ED      [19] 1242 	ld	a, -19 (ix)
   4705 DD 77 EF      [19] 1243 	ld	-17 (ix), a
   4708 DD 6E EE      [19] 1244 	ld	l,-18 (ix)
   470B DD 66 EF      [19] 1245 	ld	h,-17 (ix)
   470E 11 05 00      [10] 1246 	ld	de, #0x0005
   4711 19            [11] 1247 	add	hl, de
   4712 7E            [ 7] 1248 	ld	a, (hl)
   4713 DD 77 EE      [19] 1249 	ld	-18 (ix), a
   4716 DD 6E EC      [19] 1250 	ld	l,-20 (ix)
   4719 DD 66 ED      [19] 1251 	ld	h,-19 (ix)
   471C 11 04 00      [10] 1252 	ld	de, #0x0004
   471F 19            [11] 1253 	add	hl, de
   4720 5E            [ 7] 1254 	ld	e, (hl)
   4721 DD 6E EC      [19] 1255 	ld	l,-20 (ix)
   4724 DD 66 ED      [19] 1256 	ld	h,-19 (ix)
   4727 23            [ 6] 1257 	inc	hl
   4728 4E            [ 7] 1258 	ld	c, (hl)
   4729 06 00         [ 7] 1259 	ld	b, #0x00
   472B DD 6E EC      [19] 1260 	ld	l,-20 (ix)
   472E DD 66 ED      [19] 1261 	ld	h,-19 (ix)
   4731 56            [ 7] 1262 	ld	d, (hl)
   4732 DD 72 EC      [19] 1263 	ld	-20 (ix), d
   4735 DD 36 ED 00   [19] 1264 	ld	-19 (ix), #0x00
                           1265 ;src/game.c:227: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4739 3A 6E 64      [13] 1266 	ld	a,(#(_g_player + 0x0005) + 0)
   473C DD 77 F0      [19] 1267 	ld	-16 (ix), a
   473F 3A 6D 64      [13] 1268 	ld	a,(#(_g_player + 0x0004) + 0)
   4742 DD 77 F1      [19] 1269 	ld	-15 (ix), a
   4745 3A 6A 64      [13] 1270 	ld	a, (#(_g_player + 0x0001) + 0)
   4748 DD 77 F3      [19] 1271 	ld	-13 (ix), a
   474B DD 36 F4 00   [19] 1272 	ld	-12 (ix), #0x00
   474F 3A 69 64      [13] 1273 	ld	a, (#_g_player + 0)
   4752 DD 77 F6      [19] 1274 	ld	-10 (ix), a
   4755 DD 36 F7 00   [19] 1275 	ld	-9 (ix), #0x00
   4759 DD 56 EE      [19] 1276 	ld	d, -18 (ix)
   475C D5            [11] 1277 	push	de
   475D C5            [11] 1278 	push	bc
   475E DD 6E EC      [19] 1279 	ld	l,-20 (ix)
   4761 DD 66 ED      [19] 1280 	ld	h,-19 (ix)
   4764 E5            [11] 1281 	push	hl
   4765 DD 66 F0      [19] 1282 	ld	h, -16 (ix)
   4768 DD 6E F1      [19] 1283 	ld	l, -15 (ix)
   476B E5            [11] 1284 	push	hl
   476C DD 6E F3      [19] 1285 	ld	l,-13 (ix)
   476F DD 66 F4      [19] 1286 	ld	h,-12 (ix)
   4772 E5            [11] 1287 	push	hl
   4773 DD 6E F6      [19] 1288 	ld	l,-10 (ix)
   4776 DD 66 F7      [19] 1289 	ld	h,-9 (ix)
   4779 E5            [11] 1290 	push	hl
   477A CD 19 40      [17] 1291 	call	_rect_overlap
   477D FD 21 0C 00   [14] 1292 	ld	iy, #12
   4781 FD 39         [15] 1293 	add	iy, sp
   4783 FD F9         [10] 1294 	ld	sp, iy
   4785 7D            [ 4] 1295 	ld	a, l
   4786 B7            [ 4] 1296 	or	a, a
   4787 28 05         [12] 1297 	jr	Z,00139$
                           1298 ;src/game.c:229: register_player_hit();
   4789 CD 91 42      [17] 1299 	call	_register_player_hit
                           1300 ;src/game.c:230: break;
   478C 18 0B         [12] 1301 	jr	00140$
   478E                    1302 00139$:
                           1303 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   478E DD 34 E8      [23] 1304 	inc	-24 (ix)
   4791 DD 7E E8      [19] 1305 	ld	a, -24 (ix)
   4794 D6 06         [ 7] 1306 	sub	a, #0x06
   4796 DA DC 46      [10] 1307 	jp	C, 00180$
   4799                    1308 00140$:
                           1309 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4799 3A F3 64      [13] 1310 	ld	a,(#_g_damagecooldown + 0)
   479C B7            [ 4] 1311 	or	a, a
   479D 20 6E         [12] 1312 	jr	NZ,00142$
   479F 3A 06 65      [13] 1313 	ld	a,(#_g_bossactive + 0)
   47A2 B7            [ 4] 1314 	or	a, a
   47A3 28 68         [12] 1315 	jr	Z,00142$
                           1316 ;src/game.c:235: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   47A5 3A 01 65      [13] 1317 	ld	a,(#(_g_boss + 0x0005) + 0)
   47A8 DD 77 EC      [19] 1318 	ld	-20 (ix), a
   47AB 3A 00 65      [13] 1319 	ld	a,(#(_g_boss + 0x0004) + 0)
   47AE DD 77 EE      [19] 1320 	ld	-18 (ix), a
   47B1 21 FD 64      [10] 1321 	ld	hl, #(_g_boss + 0x0001) + 0
   47B4 5E            [ 7] 1322 	ld	e, (hl)
   47B5 16 00         [ 7] 1323 	ld	d, #0x00
   47B7 21 FC 64      [10] 1324 	ld	hl, #_g_boss + 0
   47BA 4E            [ 7] 1325 	ld	c, (hl)
   47BB 06 00         [ 7] 1326 	ld	b, #0x00
                           1327 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   47BD 3A 6E 64      [13] 1328 	ld	a,(#(_g_player + 0x0005) + 0)
   47C0 DD 77 F0      [19] 1329 	ld	-16 (ix), a
   47C3 3A 6D 64      [13] 1330 	ld	a,(#(_g_player + 0x0004) + 0)
   47C6 DD 77 F1      [19] 1331 	ld	-15 (ix), a
   47C9 3A 6A 64      [13] 1332 	ld	a, (#(_g_player + 0x0001) + 0)
   47CC DD 77 F3      [19] 1333 	ld	-13 (ix), a
   47CF DD 36 F4 00   [19] 1334 	ld	-12 (ix), #0x00
   47D3 3A 69 64      [13] 1335 	ld	a, (#_g_player + 0)
   47D6 DD 77 F6      [19] 1336 	ld	-10 (ix), a
   47D9 DD 36 F7 00   [19] 1337 	ld	-9 (ix), #0x00
   47DD DD 66 EC      [19] 1338 	ld	h, -20 (ix)
   47E0 DD 6E EE      [19] 1339 	ld	l, -18 (ix)
   47E3 E5            [11] 1340 	push	hl
   47E4 D5            [11] 1341 	push	de
   47E5 C5            [11] 1342 	push	bc
   47E6 DD 66 F0      [19] 1343 	ld	h, -16 (ix)
   47E9 DD 6E F1      [19] 1344 	ld	l, -15 (ix)
   47EC E5            [11] 1345 	push	hl
   47ED DD 6E F3      [19] 1346 	ld	l,-13 (ix)
   47F0 DD 66 F4      [19] 1347 	ld	h,-12 (ix)
   47F3 E5            [11] 1348 	push	hl
   47F4 DD 6E F6      [19] 1349 	ld	l,-10 (ix)
   47F7 DD 66 F7      [19] 1350 	ld	h,-9 (ix)
   47FA E5            [11] 1351 	push	hl
   47FB CD 19 40      [17] 1352 	call	_rect_overlap
   47FE FD 21 0C 00   [14] 1353 	ld	iy, #12
   4802 FD 39         [15] 1354 	add	iy, sp
   4804 FD F9         [10] 1355 	ld	sp, iy
   4806 7D            [ 4] 1356 	ld	a, l
   4807 B7            [ 4] 1357 	or	a, a
   4808 28 03         [12] 1358 	jr	Z,00142$
                           1359 ;src/game.c:236: register_player_hit();
   480A CD 91 42      [17] 1360 	call	_register_player_hit
   480D                    1361 00142$:
                           1362 ;src/game.c:239: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   480D 3A F3 64      [13] 1363 	ld	a,(#_g_damagecooldown + 0)
   4810 B7            [ 4] 1364 	or	a, a
   4811 20 31         [12] 1365 	jr	NZ,00149$
   4813 3A 6E 64      [13] 1366 	ld	a, (#(_g_player + 0x0005) + 0)
   4816 21 6D 64      [10] 1367 	ld	hl, #(_g_player + 0x0004) + 0
   4819 56            [ 7] 1368 	ld	d, (hl)
   481A 21 6A 64      [10] 1369 	ld	hl, #(_g_player + 0x0001) + 0
   481D 4E            [ 7] 1370 	ld	c, (hl)
   481E 06 00         [ 7] 1371 	ld	b, #0x00
   4820 21 69 64      [10] 1372 	ld	hl, #_g_player + 0
   4823 6E            [ 7] 1373 	ld	l, (hl)
   4824 DD 75 EC      [19] 1374 	ld	-20 (ix), l
   4827 DD 36 ED 00   [19] 1375 	ld	-19 (ix), #0x00
   482B F5            [11] 1376 	push	af
   482C 33            [ 6] 1377 	inc	sp
   482D D5            [11] 1378 	push	de
   482E 33            [ 6] 1379 	inc	sp
   482F C5            [11] 1380 	push	bc
   4830 DD 6E EC      [19] 1381 	ld	l,-20 (ix)
   4833 DD 66 ED      [19] 1382 	ld	h,-19 (ix)
   4836 E5            [11] 1383 	push	hl
   4837 CD 1E 4E      [17] 1384 	call	_collision_is_on_trap
   483A F1            [10] 1385 	pop	af
   483B F1            [10] 1386 	pop	af
   483C F1            [10] 1387 	pop	af
   483D 7D            [ 4] 1388 	ld	a, l
   483E B7            [ 4] 1389 	or	a, a
   483F 28 03         [12] 1390 	jr	Z,00149$
                           1391 ;src/game.c:240: register_player_hit();
   4841 CD 91 42      [17] 1392 	call	_register_player_hit
   4844                    1393 00149$:
                           1394 ;src/game.c:244: if (!g_checkpointactive && g_player.x >= 44) {
   4844 FD 21 FB 64   [14] 1395 	ld	iy, #_g_checkpointactive
   4848 FD 7E 00      [19] 1396 	ld	a, 0 (iy)
   484B B7            [ 4] 1397 	or	a, a
   484C 20 1E         [12] 1398 	jr	NZ,00151$
   484E 3A 69 64      [13] 1399 	ld	a, (#_g_player + 0)
   4851 D6 2C         [ 7] 1400 	sub	a, #0x2c
   4853 38 17         [12] 1401 	jr	C,00151$
                           1402 ;src/game.c:245: g_checkpointactive = 1;
   4855 FD 36 00 01   [19] 1403 	ld	0 (iy), #0x01
                           1404 ;src/game.c:246: g_checkpointx = 52;
   4859 21 F9 64      [10] 1405 	ld	hl,#_g_checkpointx + 0
   485C 36 34         [10] 1406 	ld	(hl), #0x34
                           1407 ;src/game.c:247: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   485E CD BC 53      [17] 1408 	call	_tilemap_ground_y
   4861 4D            [ 4] 1409 	ld	c, l
   4862 21 6E 64      [10] 1410 	ld	hl, #(_g_player + 0x0005) + 0
   4865 46            [ 7] 1411 	ld	b, (hl)
   4866 21 FA 64      [10] 1412 	ld	hl, #_g_checkpointy
   4869 79            [ 4] 1413 	ld	a, c
   486A 90            [ 4] 1414 	sub	a, b
   486B 77            [ 7] 1415 	ld	(hl), a
   486C                    1416 00151$:
                           1417 ;src/game.c:250: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
   486C 3A 09 65      [13] 1418 	ld	a,(#_g_pickuptaken + 0)
   486F B7            [ 4] 1419 	or	a, a
   4870 C2 FF 48      [10] 1420 	jp	NZ, 00154$
   4873 CD BC 53      [17] 1421 	call	_tilemap_ground_y
   4876 DD 75 EC      [19] 1422 	ld	-20 (ix), l
   4879 DD 75 EC      [19] 1423 	ld	-20 (ix), l
   487C DD 36 ED 00   [19] 1424 	ld	-19 (ix), #0x00
   4880 DD 7E EC      [19] 1425 	ld	a, -20 (ix)
   4883 C6 F8         [ 7] 1426 	add	a, #0xf8
   4885 DD 77 EC      [19] 1427 	ld	-20 (ix), a
   4888 DD 7E ED      [19] 1428 	ld	a, -19 (ix)
   488B CE FF         [ 7] 1429 	adc	a, #0xff
   488D DD 77 ED      [19] 1430 	ld	-19 (ix), a
   4890 3A 6E 64      [13] 1431 	ld	a,(#(_g_player + 0x0005) + 0)
   4893 DD 77 EE      [19] 1432 	ld	-18 (ix), a
   4896 3A 6D 64      [13] 1433 	ld	a,(#(_g_player + 0x0004) + 0)
   4899 DD 77 F0      [19] 1434 	ld	-16 (ix), a
   489C 3A 6A 64      [13] 1435 	ld	a,(#(_g_player + 0x0001) + 0)
   489F DD 77 F1      [19] 1436 	ld	-15 (ix), a
   48A2 DD 77 F1      [19] 1437 	ld	-15 (ix), a
   48A5 DD 36 F2 00   [19] 1438 	ld	-14 (ix), #0x00
   48A9 3A 69 64      [13] 1439 	ld	a,(#_g_player + 0)
   48AC DD 77 F3      [19] 1440 	ld	-13 (ix), a
   48AF DD 77 F3      [19] 1441 	ld	-13 (ix), a
   48B2 DD 36 F4 00   [19] 1442 	ld	-12 (ix), #0x00
   48B6 21 04 04      [10] 1443 	ld	hl, #0x0404
   48B9 E5            [11] 1444 	push	hl
   48BA DD 6E EC      [19] 1445 	ld	l,-20 (ix)
   48BD DD 66 ED      [19] 1446 	ld	h,-19 (ix)
   48C0 E5            [11] 1447 	push	hl
   48C1 21 24 00      [10] 1448 	ld	hl, #0x0024
   48C4 E5            [11] 1449 	push	hl
   48C5 DD 66 EE      [19] 1450 	ld	h, -18 (ix)
   48C8 DD 6E F0      [19] 1451 	ld	l, -16 (ix)
   48CB E5            [11] 1452 	push	hl
   48CC DD 6E F1      [19] 1453 	ld	l,-15 (ix)
   48CF DD 66 F2      [19] 1454 	ld	h,-14 (ix)
   48D2 E5            [11] 1455 	push	hl
   48D3 DD 6E F3      [19] 1456 	ld	l,-13 (ix)
   48D6 DD 66 F4      [19] 1457 	ld	h,-12 (ix)
   48D9 E5            [11] 1458 	push	hl
   48DA CD 19 40      [17] 1459 	call	_rect_overlap
   48DD FD 21 0C 00   [14] 1460 	ld	iy, #12
   48E1 FD 39         [15] 1461 	add	iy, sp
   48E3 FD F9         [10] 1462 	ld	sp, iy
   48E5 7D            [ 4] 1463 	ld	a, l
   48E6 B7            [ 4] 1464 	or	a, a
   48E7 28 16         [12] 1465 	jr	Z,00154$
                           1466 ;src/game.c:251: g_pickuptaken = 1;
   48E9 21 09 65      [10] 1467 	ld	hl,#_g_pickuptaken + 0
   48EC 36 01         [10] 1468 	ld	(hl), #0x01
                           1469 ;src/game.c:252: g_weaponlevel = 1;
   48EE 21 08 65      [10] 1470 	ld	hl,#_g_weaponlevel + 0
   48F1 36 01         [10] 1471 	ld	(hl), #0x01
                           1472 ;src/game.c:253: g_score = (u16)(g_score + 100);
   48F3 21 EC 64      [10] 1473 	ld	hl, #_g_score
   48F6 7E            [ 7] 1474 	ld	a, (hl)
   48F7 C6 64         [ 7] 1475 	add	a, #0x64
   48F9 77            [ 7] 1476 	ld	(hl), a
   48FA 23            [ 6] 1477 	inc	hl
   48FB 7E            [ 7] 1478 	ld	a, (hl)
   48FC CE 00         [ 7] 1479 	adc	a, #0x00
   48FE 77            [ 7] 1480 	ld	(hl), a
   48FF                    1481 00154$:
                           1482 ;src/game.c:256: g_weapondisplay = (u8)(g_weaponlevel + 1);
   48FF 21 EF 64      [10] 1483 	ld	hl, #_g_weapondisplay
   4902 3A 08 65      [13] 1484 	ld	a,(#_g_weaponlevel + 0)
   4905 3C            [ 4] 1485 	inc	a
   4906 77            [ 7] 1486 	ld	(hl), a
                           1487 ;src/game.c:258: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   4907 3A 06 65      [13] 1488 	ld	a,(#_g_bossactive + 0)
   490A B7            [ 4] 1489 	or	a, a
   490B 20 45         [12] 1490 	jr	NZ,00165$
   490D 3A F1 64      [13] 1491 	ld	a,(#_g_aliveenemies + 0)
   4910 B7            [ 4] 1492 	or	a, a
   4911 20 3F         [12] 1493 	jr	NZ,00165$
   4913 3A F6 64      [13] 1494 	ld	a,(#_g_gameover + 0)
   4916 B7            [ 4] 1495 	or	a, a
   4917 20 39         [12] 1496 	jr	NZ,00165$
                           1497 ;src/game.c:259: if (g_currentwave < TOTAL_WAVES) {
   4919 3A F0 64      [13] 1498 	ld	a,(#_g_currentwave + 0)
   491C D6 03         [ 7] 1499 	sub	a, #0x03
   491E 30 20         [12] 1500 	jr	NC,00162$
                           1501 ;src/game.c:260: if (g_wavecooldown == 0) {
   4920 3A F2 64      [13] 1502 	ld	a,(#_g_wavecooldown + 0)
   4923 B7            [ 4] 1503 	or	a, a
   4924 20 14         [12] 1504 	jr	NZ,00157$
                           1505 ;src/game.c:261: spawn_wave(g_currentwave);
   4926 3A F0 64      [13] 1506 	ld	a, (_g_currentwave)
   4929 F5            [11] 1507 	push	af
   492A 33            [ 6] 1508 	inc	sp
   492B CD A6 40      [17] 1509 	call	_spawn_wave
   492E 33            [ 6] 1510 	inc	sp
                           1511 ;src/game.c:262: g_currentwave++;
   492F 21 F0 64      [10] 1512 	ld	hl, #_g_currentwave+0
   4932 34            [11] 1513 	inc	(hl)
                           1514 ;src/game.c:263: g_wavecooldown = 90;
   4933 21 F2 64      [10] 1515 	ld	hl,#_g_wavecooldown + 0
   4936 36 5A         [10] 1516 	ld	(hl), #0x5a
   4938 18 18         [12] 1517 	jr	00165$
   493A                    1518 00157$:
                           1519 ;src/game.c:265: g_wavecooldown--;
   493A 21 F2 64      [10] 1520 	ld	hl, #_g_wavecooldown+0
   493D 35            [11] 1521 	dec	(hl)
   493E 18 12         [12] 1522 	jr	00165$
   4940                    1523 00162$:
                           1524 ;src/game.c:267: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   4940 21 69 64      [10] 1525 	ld	hl, #_g_player + 0
   4943 4E            [ 7] 1526 	ld	c, (hl)
   4944 C5            [11] 1527 	push	bc
   4945 CD 60 54      [17] 1528 	call	_tilemap_goal_x
   4948 C1            [10] 1529 	pop	bc
   4949 2D            [ 4] 1530 	dec	l
   494A 2D            [ 4] 1531 	dec	l
   494B 79            [ 4] 1532 	ld	a, c
   494C 95            [ 4] 1533 	sub	a, l
   494D 38 03         [12] 1534 	jr	C,00165$
                           1535 ;src/game.c:268: spawn_boss();
   494F CD A6 41      [17] 1536 	call	_spawn_boss
   4952                    1537 00165$:
                           1538 ;src/game.c:272: g_framecounter++;
   4952 FD 21 F7 64   [14] 1539 	ld	iy, #_g_framecounter
   4956 FD 34 00      [23] 1540 	inc	0 (iy)
   4959 20 03         [12] 1541 	jr	NZ,00381$
   495B FD 34 01      [23] 1542 	inc	1 (iy)
   495E                    1543 00381$:
                           1544 ;src/game.c:273: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   495E 21 32 00      [10] 1545 	ld	hl, #0x0032
   4961 E5            [11] 1546 	push	hl
   4962 2A F7 64      [16] 1547 	ld	hl, (_g_framecounter)
   4965 E5            [11] 1548 	push	hl
   4966 CD 1B 63      [17] 1549 	call	__moduint
   4969 F1            [10] 1550 	pop	af
   496A F1            [10] 1551 	pop	af
   496B 7C            [ 4] 1552 	ld	a, h
   496C B5            [ 4] 1553 	or	a,l
   496D 20 0D         [12] 1554 	jr	NZ,00169$
   496F FD 21 EE 64   [14] 1555 	ld	iy, #_g_timeleft
   4973 FD 7E 00      [19] 1556 	ld	a, 0 (iy)
   4976 B7            [ 4] 1557 	or	a, a
   4977 28 03         [12] 1558 	jr	Z,00169$
                           1559 ;src/game.c:274: g_timeleft--;
   4979 FD 35 00      [23] 1560 	dec	0 (iy)
   497C                    1561 00169$:
                           1562 ;src/game.c:276: if (g_timeleft == 0 && !g_victory) {
   497C 3A EE 64      [13] 1563 	ld	a,(#_g_timeleft + 0)
   497F B7            [ 4] 1564 	or	a, a
   4980 20 0B         [12] 1565 	jr	NZ,00172$
   4982 3A F5 64      [13] 1566 	ld	a,(#_g_victory + 0)
   4985 B7            [ 4] 1567 	or	a, a
   4986 20 05         [12] 1568 	jr	NZ,00172$
                           1569 ;src/game.c:277: g_gameover = 1;
   4988 21 F6 64      [10] 1570 	ld	hl,#_g_gameover + 0
   498B 36 01         [10] 1571 	ld	(hl), #0x01
   498D                    1572 00172$:
                           1573 ;src/game.c:280: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   498D 3A EF 64      [13] 1574 	ld	a, (_g_weapondisplay)
   4990 F5            [11] 1575 	push	af
   4991 33            [ 6] 1576 	inc	sp
   4992 3A EE 64      [13] 1577 	ld	a, (_g_timeleft)
   4995 F5            [11] 1578 	push	af
   4996 33            [ 6] 1579 	inc	sp
   4997 2A EC 64      [16] 1580 	ld	hl, (_g_score)
   499A E5            [11] 1581 	push	hl
   499B 3A EB 64      [13] 1582 	ld	a, (_g_lives)
   499E F5            [11] 1583 	push	af
   499F 33            [ 6] 1584 	inc	sp
   49A0 CD EC 50      [17] 1585 	call	_hudupdate
   49A3 F1            [10] 1586 	pop	af
   49A4 F1            [10] 1587 	pop	af
   49A5 33            [ 6] 1588 	inc	sp
   49A6                    1589 00181$:
   49A6 DD F9         [10] 1590 	ld	sp, ix
   49A8 DD E1         [14] 1591 	pop	ix
   49AA C9            [10] 1592 	ret
                           1593 ;src/game.c:283: void game_render(void) {
                           1594 ;	---------------------------------
                           1595 ; Function game_render
                           1596 ; ---------------------------------
   49AB                    1597 _game_render::
   49AB DD E5         [15] 1598 	push	ix
   49AD DD 21 00 00   [14] 1599 	ld	ix,#0
   49B1 DD 39         [15] 1600 	add	ix,sp
   49B3 F5            [11] 1601 	push	af
   49B4 F5            [11] 1602 	push	af
                           1603 ;src/game.c:286: cpct_drawSolidBox(CPCT_VMEM_START, cpct_px2byteM0(0, 0), 80, 200);
   49B5 21 00 00      [10] 1604 	ld	hl, #0x0000
   49B8 E5            [11] 1605 	push	hl
   49B9 CD 46 63      [17] 1606 	call	_cpct_px2byteM0
   49BC 45            [ 4] 1607 	ld	b, l
   49BD 21 50 C8      [10] 1608 	ld	hl, #0xc850
   49C0 E5            [11] 1609 	push	hl
   49C1 C5            [11] 1610 	push	bc
   49C2 33            [ 6] 1611 	inc	sp
   49C3 21 00 C0      [10] 1612 	ld	hl, #0xc000
   49C6 E5            [11] 1613 	push	hl
   49C7 CD 80 63      [17] 1614 	call	_cpct_drawSolidBox
   49CA F1            [10] 1615 	pop	af
   49CB F1            [10] 1616 	pop	af
   49CC 33            [ 6] 1617 	inc	sp
                           1618 ;src/game.c:287: tilemap_render();
   49CD CD 1B 53      [17] 1619 	call	_tilemap_render
                           1620 ;src/game.c:288: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 60, 18), cpct_px2byteM0(5, 5), 6, 10);
   49D0 21 05 05      [10] 1621 	ld	hl, #0x0505
   49D3 E5            [11] 1622 	push	hl
   49D4 CD 46 63      [17] 1623 	call	_cpct_px2byteM0
   49D7 55            [ 4] 1624 	ld	d, l
   49D8 D5            [11] 1625 	push	de
   49D9 21 3C 12      [10] 1626 	ld	hl, #0x123c
   49DC E5            [11] 1627 	push	hl
   49DD 21 00 C0      [10] 1628 	ld	hl, #0xc000
   49E0 E5            [11] 1629 	push	hl
   49E1 CD 39 64      [17] 1630 	call	_cpct_getScreenPtr
   49E4 4D            [ 4] 1631 	ld	c, l
   49E5 44            [ 4] 1632 	ld	b, h
   49E6 D1            [10] 1633 	pop	de
   49E7 21 06 0A      [10] 1634 	ld	hl, #0x0a06
   49EA E5            [11] 1635 	push	hl
   49EB D5            [11] 1636 	push	de
   49EC 33            [ 6] 1637 	inc	sp
   49ED C5            [11] 1638 	push	bc
   49EE CD 80 63      [17] 1639 	call	_cpct_drawSolidBox
   49F1 F1            [10] 1640 	pop	af
                           1641 ;src/game.c:289: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 58, 20), cpct_px2byteM0(8, 8), 2, 6);
   49F2 33            [ 6] 1642 	inc	sp
   49F3 21 08 08      [10] 1643 	ld	hl,#0x0808
   49F6 E3            [19] 1644 	ex	(sp),hl
   49F7 CD 46 63      [17] 1645 	call	_cpct_px2byteM0
   49FA 55            [ 4] 1646 	ld	d, l
   49FB D5            [11] 1647 	push	de
   49FC 21 3A 14      [10] 1648 	ld	hl, #0x143a
   49FF E5            [11] 1649 	push	hl
   4A00 21 00 C0      [10] 1650 	ld	hl, #0xc000
   4A03 E5            [11] 1651 	push	hl
   4A04 CD 39 64      [17] 1652 	call	_cpct_getScreenPtr
   4A07 4D            [ 4] 1653 	ld	c, l
   4A08 44            [ 4] 1654 	ld	b, h
   4A09 D1            [10] 1655 	pop	de
   4A0A 21 02 06      [10] 1656 	ld	hl, #0x0602
   4A0D E5            [11] 1657 	push	hl
   4A0E D5            [11] 1658 	push	de
   4A0F 33            [ 6] 1659 	inc	sp
   4A10 C5            [11] 1660 	push	bc
   4A11 CD 80 63      [17] 1661 	call	_cpct_drawSolidBox
   4A14 F1            [10] 1662 	pop	af
   4A15 F1            [10] 1663 	pop	af
   4A16 33            [ 6] 1664 	inc	sp
                           1665 ;src/game.c:291: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4A17 DD 36 FC 00   [19] 1666 	ld	-4 (ix), #0x00
   4A1B                    1667 00119$:
                           1668 ;src/game.c:292: if (g_projectiles[i].active) {
   4A1B DD 4E FC      [19] 1669 	ld	c,-4 (ix)
   4A1E 06 00         [ 7] 1670 	ld	b,#0x00
   4A20 69            [ 4] 1671 	ld	l, c
   4A21 60            [ 4] 1672 	ld	h, b
   4A22 29            [11] 1673 	add	hl, hl
   4A23 29            [11] 1674 	add	hl, hl
   4A24 09            [11] 1675 	add	hl, bc
   4A25 29            [11] 1676 	add	hl, hl
   4A26 01 AF 64      [10] 1677 	ld	bc,#_g_projectiles
   4A29 09            [11] 1678 	add	hl,bc
   4A2A 4D            [ 4] 1679 	ld	c, l
   4A2B 44            [ 4] 1680 	ld	b, h
   4A2C C5            [11] 1681 	push	bc
   4A2D FD E1         [14] 1682 	pop	iy
   4A2F FD 7E 06      [19] 1683 	ld	a, 6 (iy)
   4A32 B7            [ 4] 1684 	or	a, a
   4A33 28 46         [12] 1685 	jr	Z,00102$
                           1686 ;src/game.c:293: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_projectiles[i].x, g_projectiles[i].y), cpct_px2byteM0(11, 11), g_projectiles[i].w, g_projectiles[i].h);
   4A35 69            [ 4] 1687 	ld	l, c
   4A36 60            [ 4] 1688 	ld	h, b
   4A37 11 05 00      [10] 1689 	ld	de, #0x0005
   4A3A 19            [11] 1690 	add	hl, de
   4A3B 7E            [ 7] 1691 	ld	a, (hl)
   4A3C DD 77 FF      [19] 1692 	ld	-1 (ix), a
   4A3F 69            [ 4] 1693 	ld	l, c
   4A40 60            [ 4] 1694 	ld	h, b
   4A41 11 04 00      [10] 1695 	ld	de, #0x0004
   4A44 19            [11] 1696 	add	hl, de
   4A45 7E            [ 7] 1697 	ld	a, (hl)
   4A46 DD 77 FE      [19] 1698 	ld	-2 (ix), a
   4A49 C5            [11] 1699 	push	bc
   4A4A 21 0B 0B      [10] 1700 	ld	hl, #0x0b0b
   4A4D E5            [11] 1701 	push	hl
   4A4E CD 46 63      [17] 1702 	call	_cpct_px2byteM0
   4A51 5D            [ 4] 1703 	ld	e, l
   4A52 C1            [10] 1704 	pop	bc
   4A53 69            [ 4] 1705 	ld	l, c
   4A54 60            [ 4] 1706 	ld	h, b
   4A55 23            [ 6] 1707 	inc	hl
   4A56 56            [ 7] 1708 	ld	d, (hl)
   4A57 0A            [ 7] 1709 	ld	a, (bc)
   4A58 C5            [11] 1710 	push	bc
   4A59 D5            [11] 1711 	push	de
   4A5A 5F            [ 4] 1712 	ld	e, a
   4A5B D5            [11] 1713 	push	de
   4A5C 21 00 C0      [10] 1714 	ld	hl, #0xc000
   4A5F E5            [11] 1715 	push	hl
   4A60 CD 39 64      [17] 1716 	call	_cpct_getScreenPtr
   4A63 D1            [10] 1717 	pop	de
   4A64 C1            [10] 1718 	pop	bc
   4A65 E5            [11] 1719 	push	hl
   4A66 FD E1         [14] 1720 	pop	iy
   4A68 C5            [11] 1721 	push	bc
   4A69 DD 7E FF      [19] 1722 	ld	a, -1 (ix)
   4A6C F5            [11] 1723 	push	af
   4A6D 33            [ 6] 1724 	inc	sp
   4A6E DD 56 FE      [19] 1725 	ld	d, -2 (ix)
   4A71 D5            [11] 1726 	push	de
   4A72 FD E5         [15] 1727 	push	iy
   4A74 CD 80 63      [17] 1728 	call	_cpct_drawSolidBox
   4A77 F1            [10] 1729 	pop	af
   4A78 F1            [10] 1730 	pop	af
   4A79 33            [ 6] 1731 	inc	sp
   4A7A C1            [10] 1732 	pop	bc
   4A7B                    1733 00102$:
                           1734 ;src/game.c:295: projectilerender(&g_projectiles[i]);
   4A7B C5            [11] 1735 	push	bc
   4A7C CD 0E 61      [17] 1736 	call	_projectilerender
   4A7F F1            [10] 1737 	pop	af
                           1738 ;src/game.c:291: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4A80 DD 34 FC      [23] 1739 	inc	-4 (ix)
   4A83 DD 7E FC      [19] 1740 	ld	a, -4 (ix)
   4A86 D6 06         [ 7] 1741 	sub	a, #0x06
   4A88 38 91         [12] 1742 	jr	C,00119$
                           1743 ;src/game.c:298: for (i = 0; i < MAX_ENEMIES; ++i) {
   4A8A DD 36 FC 00   [19] 1744 	ld	-4 (ix), #0x00
   4A8E                    1745 00121$:
                           1746 ;src/game.c:299: if (g_enemies[i].active) {
   4A8E DD 4E FC      [19] 1747 	ld	c,-4 (ix)
   4A91 06 00         [ 7] 1748 	ld	b,#0x00
   4A93 69            [ 4] 1749 	ld	l, c
   4A94 60            [ 4] 1750 	ld	h, b
   4A95 29            [11] 1751 	add	hl, hl
   4A96 29            [11] 1752 	add	hl, hl
   4A97 09            [11] 1753 	add	hl, bc
   4A98 29            [11] 1754 	add	hl, hl
   4A99 01 73 64      [10] 1755 	ld	bc,#_g_enemies
   4A9C 09            [11] 1756 	add	hl,bc
   4A9D EB            [ 4] 1757 	ex	de,hl
   4A9E D5            [11] 1758 	push	de
   4A9F FD E1         [14] 1759 	pop	iy
   4AA1 FD 7E 06      [19] 1760 	ld	a, 6 (iy)
   4AA4 B7            [ 4] 1761 	or	a, a
   4AA5 28 45         [12] 1762 	jr	Z,00105$
                           1763 ;src/game.c:300: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_enemies[i].x, g_enemies[i].y), cpct_px2byteM0(4, 4), g_enemies[i].w, g_enemies[i].h);
   4AA7 D5            [11] 1764 	push	de
   4AA8 FD E1         [14] 1765 	pop	iy
   4AAA FD 7E 05      [19] 1766 	ld	a, 5 (iy)
   4AAD DD 77 FE      [19] 1767 	ld	-2 (ix), a
   4AB0 D5            [11] 1768 	push	de
   4AB1 FD E1         [14] 1769 	pop	iy
   4AB3 FD 7E 04      [19] 1770 	ld	a, 4 (iy)
   4AB6 DD 77 FF      [19] 1771 	ld	-1 (ix), a
   4AB9 D5            [11] 1772 	push	de
   4ABA 21 04 04      [10] 1773 	ld	hl, #0x0404
   4ABD E5            [11] 1774 	push	hl
   4ABE CD 46 63      [17] 1775 	call	_cpct_px2byteM0
   4AC1 DD 75 FD      [19] 1776 	ld	-3 (ix), l
   4AC4 D1            [10] 1777 	pop	de
   4AC5 6B            [ 4] 1778 	ld	l, e
   4AC6 62            [ 4] 1779 	ld	h, d
   4AC7 23            [ 6] 1780 	inc	hl
   4AC8 46            [ 7] 1781 	ld	b, (hl)
   4AC9 1A            [ 7] 1782 	ld	a, (de)
   4ACA D5            [11] 1783 	push	de
   4ACB C5            [11] 1784 	push	bc
   4ACC 33            [ 6] 1785 	inc	sp
   4ACD F5            [11] 1786 	push	af
   4ACE 33            [ 6] 1787 	inc	sp
   4ACF 21 00 C0      [10] 1788 	ld	hl, #0xc000
   4AD2 E5            [11] 1789 	push	hl
   4AD3 CD 39 64      [17] 1790 	call	_cpct_getScreenPtr
   4AD6 4D            [ 4] 1791 	ld	c, l
   4AD7 44            [ 4] 1792 	ld	b, h
   4AD8 DD 66 FE      [19] 1793 	ld	h, -2 (ix)
   4ADB DD 6E FF      [19] 1794 	ld	l, -1 (ix)
   4ADE E5            [11] 1795 	push	hl
   4ADF DD 7E FD      [19] 1796 	ld	a, -3 (ix)
   4AE2 F5            [11] 1797 	push	af
   4AE3 33            [ 6] 1798 	inc	sp
   4AE4 C5            [11] 1799 	push	bc
   4AE5 CD 80 63      [17] 1800 	call	_cpct_drawSolidBox
   4AE8 F1            [10] 1801 	pop	af
   4AE9 F1            [10] 1802 	pop	af
   4AEA 33            [ 6] 1803 	inc	sp
   4AEB D1            [10] 1804 	pop	de
   4AEC                    1805 00105$:
                           1806 ;src/game.c:302: enemyrender(&g_enemies[i]);
   4AEC D5            [11] 1807 	push	de
   4AED CD BB 5B      [17] 1808 	call	_enemyrender
   4AF0 F1            [10] 1809 	pop	af
                           1810 ;src/game.c:298: for (i = 0; i < MAX_ENEMIES; ++i) {
   4AF1 DD 34 FC      [23] 1811 	inc	-4 (ix)
   4AF4 DD 7E FC      [19] 1812 	ld	a, -4 (ix)
   4AF7 D6 06         [ 7] 1813 	sub	a, #0x06
   4AF9 38 93         [12] 1814 	jr	C,00121$
                           1815 ;src/game.c:305: if (g_bossactive) {
   4AFB 3A 06 65      [13] 1816 	ld	a,(#_g_bossactive + 0)
   4AFE B7            [ 4] 1817 	or	a, a
   4AFF 28 58         [12] 1818 	jr	Z,00108$
                           1819 ;src/game.c:306: enemyrender(&g_boss);
   4B01 21 FC 64      [10] 1820 	ld	hl, #_g_boss
   4B04 E5            [11] 1821 	push	hl
   4B05 CD BB 5B      [17] 1822 	call	_enemyrender
                           1823 ;src/game.c:307: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(1, 1), 32, 2);
   4B08 21 01 01      [10] 1824 	ld	hl, #0x0101
   4B0B E3            [19] 1825 	ex	(sp),hl
   4B0C CD 46 63      [17] 1826 	call	_cpct_px2byteM0
   4B0F 4D            [ 4] 1827 	ld	c, l
   4B10 C5            [11] 1828 	push	bc
   4B11 21 18 0A      [10] 1829 	ld	hl, #0x0a18
   4B14 E5            [11] 1830 	push	hl
   4B15 21 00 C0      [10] 1831 	ld	hl, #0xc000
   4B18 E5            [11] 1832 	push	hl
   4B19 CD 39 64      [17] 1833 	call	_cpct_getScreenPtr
   4B1C C1            [10] 1834 	pop	bc
   4B1D 11 20 02      [10] 1835 	ld	de, #0x0220
   4B20 D5            [11] 1836 	push	de
   4B21 79            [ 4] 1837 	ld	a, c
   4B22 F5            [11] 1838 	push	af
   4B23 33            [ 6] 1839 	inc	sp
   4B24 E5            [11] 1840 	push	hl
   4B25 CD 80 63      [17] 1841 	call	_cpct_drawSolidBox
   4B28 F1            [10] 1842 	pop	af
   4B29 F1            [10] 1843 	pop	af
   4B2A 33            [ 6] 1844 	inc	sp
                           1845 ;src/game.c:308: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
   4B2B 3A 03 65      [13] 1846 	ld	a, (#_g_boss + 7)
   4B2E 4F            [ 4] 1847 	ld	c, a
   4B2F 87            [ 4] 1848 	add	a, a
   4B30 81            [ 4] 1849 	add	a, c
   4B31 67            [ 4] 1850 	ld	h, a
   4B32 E5            [11] 1851 	push	hl
   4B33 01 05 05      [10] 1852 	ld	bc, #0x0505
   4B36 C5            [11] 1853 	push	bc
   4B37 CD 46 63      [17] 1854 	call	_cpct_px2byteM0
   4B3A 45            [ 4] 1855 	ld	b, l
   4B3B C5            [11] 1856 	push	bc
   4B3C 11 18 0A      [10] 1857 	ld	de, #0x0a18
   4B3F D5            [11] 1858 	push	de
   4B40 11 00 C0      [10] 1859 	ld	de, #0xc000
   4B43 D5            [11] 1860 	push	de
   4B44 CD 39 64      [17] 1861 	call	_cpct_getScreenPtr
   4B47 EB            [ 4] 1862 	ex	de,hl
   4B48 C1            [10] 1863 	pop	bc
   4B49 E1            [10] 1864 	pop	hl
   4B4A 3E 02         [ 7] 1865 	ld	a, #0x02
   4B4C F5            [11] 1866 	push	af
   4B4D 33            [ 6] 1867 	inc	sp
   4B4E E5            [11] 1868 	push	hl
   4B4F 33            [ 6] 1869 	inc	sp
   4B50 C5            [11] 1870 	push	bc
   4B51 33            [ 6] 1871 	inc	sp
   4B52 D5            [11] 1872 	push	de
   4B53 CD 80 63      [17] 1873 	call	_cpct_drawSolidBox
   4B56 F1            [10] 1874 	pop	af
   4B57 F1            [10] 1875 	pop	af
   4B58 33            [ 6] 1876 	inc	sp
   4B59                    1877 00108$:
                           1878 ;src/game.c:311: if (!g_pickuptaken) {
   4B59 3A 09 65      [13] 1879 	ld	a,(#_g_pickuptaken + 0)
   4B5C B7            [ 4] 1880 	or	a, a
   4B5D 20 2E         [12] 1881 	jr	NZ,00110$
                           1882 ;src/game.c:312: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
   4B5F 21 07 07      [10] 1883 	ld	hl, #0x0707
   4B62 E5            [11] 1884 	push	hl
   4B63 CD 46 63      [17] 1885 	call	_cpct_px2byteM0
   4B66 4D            [ 4] 1886 	ld	c, l
   4B67 C5            [11] 1887 	push	bc
   4B68 CD BC 53      [17] 1888 	call	_tilemap_ground_y
   4B6B C1            [10] 1889 	pop	bc
   4B6C 7D            [ 4] 1890 	ld	a, l
   4B6D C6 F8         [ 7] 1891 	add	a, #0xf8
   4B6F 47            [ 4] 1892 	ld	b, a
   4B70 C5            [11] 1893 	push	bc
   4B71 C5            [11] 1894 	push	bc
   4B72 33            [ 6] 1895 	inc	sp
   4B73 3E 24         [ 7] 1896 	ld	a, #0x24
   4B75 F5            [11] 1897 	push	af
   4B76 33            [ 6] 1898 	inc	sp
   4B77 21 00 C0      [10] 1899 	ld	hl, #0xc000
   4B7A E5            [11] 1900 	push	hl
   4B7B CD 39 64      [17] 1901 	call	_cpct_getScreenPtr
   4B7E C1            [10] 1902 	pop	bc
   4B7F 11 04 04      [10] 1903 	ld	de, #0x0404
   4B82 D5            [11] 1904 	push	de
   4B83 79            [ 4] 1905 	ld	a, c
   4B84 F5            [11] 1906 	push	af
   4B85 33            [ 6] 1907 	inc	sp
   4B86 E5            [11] 1908 	push	hl
   4B87 CD 80 63      [17] 1909 	call	_cpct_drawSolidBox
   4B8A F1            [10] 1910 	pop	af
   4B8B F1            [10] 1911 	pop	af
   4B8C 33            [ 6] 1912 	inc	sp
   4B8D                    1913 00110$:
                           1914 ;src/game.c:314: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_player.x, g_player.y), cpct_px2byteM0(6, 6), g_player.w, g_player.h);
   4B8D 21 6E 64      [10] 1915 	ld	hl, #_g_player + 5
   4B90 4E            [ 7] 1916 	ld	c, (hl)
   4B91 21 6D 64      [10] 1917 	ld	hl, #_g_player + 4
   4B94 46            [ 7] 1918 	ld	b, (hl)
   4B95 C5            [11] 1919 	push	bc
   4B96 21 06 06      [10] 1920 	ld	hl, #0x0606
   4B99 E5            [11] 1921 	push	hl
   4B9A CD 46 63      [17] 1922 	call	_cpct_px2byteM0
   4B9D DD 75 FD      [19] 1923 	ld	-3 (ix), l
   4BA0 C1            [10] 1924 	pop	bc
   4BA1 21 6A 64      [10] 1925 	ld	hl, #_g_player + 1
   4BA4 56            [ 7] 1926 	ld	d, (hl)
   4BA5 3A 69 64      [13] 1927 	ld	a, (#_g_player + 0)
   4BA8 C5            [11] 1928 	push	bc
   4BA9 5F            [ 4] 1929 	ld	e, a
   4BAA D5            [11] 1930 	push	de
   4BAB 21 00 C0      [10] 1931 	ld	hl, #0xc000
   4BAE E5            [11] 1932 	push	hl
   4BAF CD 39 64      [17] 1933 	call	_cpct_getScreenPtr
   4BB2 EB            [ 4] 1934 	ex	de,hl
   4BB3 C1            [10] 1935 	pop	bc
   4BB4 79            [ 4] 1936 	ld	a, c
   4BB5 F5            [11] 1937 	push	af
   4BB6 33            [ 6] 1938 	inc	sp
   4BB7 C5            [11] 1939 	push	bc
   4BB8 33            [ 6] 1940 	inc	sp
   4BB9 DD 7E FD      [19] 1941 	ld	a, -3 (ix)
   4BBC F5            [11] 1942 	push	af
   4BBD 33            [ 6] 1943 	inc	sp
   4BBE D5            [11] 1944 	push	de
   4BBF CD 80 63      [17] 1945 	call	_cpct_drawSolidBox
   4BC2 F1            [10] 1946 	pop	af
                           1947 ;src/game.c:315: playerrender(&g_player);
   4BC3 33            [ 6] 1948 	inc	sp
   4BC4 21 69 64      [10] 1949 	ld	hl,#_g_player
   4BC7 E3            [19] 1950 	ex	(sp),hl
   4BC8 CD 1F 5F      [17] 1951 	call	_playerrender
   4BCB F1            [10] 1952 	pop	af
                           1953 ;src/game.c:316: hudrender();
   4BCC CD 1D 51      [17] 1954 	call	_hudrender
                           1955 ;src/game.c:318: if (g_victory) {
   4BCF 3A F5 64      [13] 1956 	ld	a,(#_g_victory + 0)
   4BD2 B7            [ 4] 1957 	or	a, a
   4BD3 28 48         [12] 1958 	jr	Z,00117$
                           1959 ;src/game.c:319: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
   4BD5 21 08 08      [10] 1960 	ld	hl, #0x0808
   4BD8 E5            [11] 1961 	push	hl
   4BD9 CD 46 63      [17] 1962 	call	_cpct_px2byteM0
   4BDC 4D            [ 4] 1963 	ld	c, l
   4BDD C5            [11] 1964 	push	bc
   4BDE 21 18 44      [10] 1965 	ld	hl, #0x4418
   4BE1 E5            [11] 1966 	push	hl
   4BE2 21 00 C0      [10] 1967 	ld	hl, #0xc000
   4BE5 E5            [11] 1968 	push	hl
   4BE6 CD 39 64      [17] 1969 	call	_cpct_getScreenPtr
   4BE9 C1            [10] 1970 	pop	bc
   4BEA 11 20 0C      [10] 1971 	ld	de, #0x0c20
   4BED D5            [11] 1972 	push	de
   4BEE 79            [ 4] 1973 	ld	a, c
   4BEF F5            [11] 1974 	push	af
   4BF0 33            [ 6] 1975 	inc	sp
   4BF1 E5            [11] 1976 	push	hl
   4BF2 CD 80 63      [17] 1977 	call	_cpct_drawSolidBox
   4BF5 F1            [10] 1978 	pop	af
                           1979 ;src/game.c:320: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(5, 5), 24, 8);
   4BF6 33            [ 6] 1980 	inc	sp
   4BF7 21 05 05      [10] 1981 	ld	hl,#0x0505
   4BFA E3            [19] 1982 	ex	(sp),hl
   4BFB CD 46 63      [17] 1983 	call	_cpct_px2byteM0
   4BFE 4D            [ 4] 1984 	ld	c, l
   4BFF C5            [11] 1985 	push	bc
   4C00 21 1C 48      [10] 1986 	ld	hl, #0x481c
   4C03 E5            [11] 1987 	push	hl
   4C04 21 00 C0      [10] 1988 	ld	hl, #0xc000
   4C07 E5            [11] 1989 	push	hl
   4C08 CD 39 64      [17] 1990 	call	_cpct_getScreenPtr
   4C0B C1            [10] 1991 	pop	bc
   4C0C 11 18 08      [10] 1992 	ld	de, #0x0818
   4C0F D5            [11] 1993 	push	de
   4C10 79            [ 4] 1994 	ld	a, c
   4C11 F5            [11] 1995 	push	af
   4C12 33            [ 6] 1996 	inc	sp
   4C13 E5            [11] 1997 	push	hl
   4C14 CD 80 63      [17] 1998 	call	_cpct_drawSolidBox
   4C17 F1            [10] 1999 	pop	af
   4C18 F1            [10] 2000 	pop	af
   4C19 33            [ 6] 2001 	inc	sp
   4C1A C3 9E 4C      [10] 2002 	jp	00123$
   4C1D                    2003 00117$:
                           2004 ;src/game.c:321: } else if (g_gameover) {
   4C1D 3A F6 64      [13] 2005 	ld	a,(#_g_gameover + 0)
   4C20 B7            [ 4] 2006 	or	a, a
   4C21 28 49         [12] 2007 	jr	Z,00114$
                           2008 ;src/game.c:322: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
   4C23 21 01 01      [10] 2009 	ld	hl, #0x0101
   4C26 E5            [11] 2010 	push	hl
   4C27 CD 46 63      [17] 2011 	call	_cpct_px2byteM0
   4C2A 55            [ 4] 2012 	ld	d, l
   4C2B D5            [11] 2013 	push	de
   4C2C 21 18 44      [10] 2014 	ld	hl, #0x4418
   4C2F E5            [11] 2015 	push	hl
   4C30 21 00 C0      [10] 2016 	ld	hl, #0xc000
   4C33 E5            [11] 2017 	push	hl
   4C34 CD 39 64      [17] 2018 	call	_cpct_getScreenPtr
   4C37 4D            [ 4] 2019 	ld	c, l
   4C38 44            [ 4] 2020 	ld	b, h
   4C39 D1            [10] 2021 	pop	de
   4C3A 21 20 0C      [10] 2022 	ld	hl, #0x0c20
   4C3D E5            [11] 2023 	push	hl
   4C3E D5            [11] 2024 	push	de
   4C3F 33            [ 6] 2025 	inc	sp
   4C40 C5            [11] 2026 	push	bc
   4C41 CD 80 63      [17] 2027 	call	_cpct_drawSolidBox
   4C44 F1            [10] 2028 	pop	af
                           2029 ;src/game.c:323: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(6, 6), 24, 8);
   4C45 33            [ 6] 2030 	inc	sp
   4C46 21 06 06      [10] 2031 	ld	hl,#0x0606
   4C49 E3            [19] 2032 	ex	(sp),hl
   4C4A CD 46 63      [17] 2033 	call	_cpct_px2byteM0
   4C4D 55            [ 4] 2034 	ld	d, l
   4C4E D5            [11] 2035 	push	de
   4C4F 21 1C 48      [10] 2036 	ld	hl, #0x481c
   4C52 E5            [11] 2037 	push	hl
   4C53 21 00 C0      [10] 2038 	ld	hl, #0xc000
   4C56 E5            [11] 2039 	push	hl
   4C57 CD 39 64      [17] 2040 	call	_cpct_getScreenPtr
   4C5A 4D            [ 4] 2041 	ld	c, l
   4C5B 44            [ 4] 2042 	ld	b, h
   4C5C D1            [10] 2043 	pop	de
   4C5D 21 18 08      [10] 2044 	ld	hl, #0x0818
   4C60 E5            [11] 2045 	push	hl
   4C61 D5            [11] 2046 	push	de
   4C62 33            [ 6] 2047 	inc	sp
   4C63 C5            [11] 2048 	push	bc
   4C64 CD 80 63      [17] 2049 	call	_cpct_drawSolidBox
   4C67 F1            [10] 2050 	pop	af
   4C68 F1            [10] 2051 	pop	af
   4C69 33            [ 6] 2052 	inc	sp
   4C6A 18 32         [12] 2053 	jr	00123$
   4C6C                    2054 00114$:
                           2055 ;src/game.c:324: } else if (g_checkpointactive) {
   4C6C 3A FB 64      [13] 2056 	ld	a,(#_g_checkpointactive + 0)
   4C6F B7            [ 4] 2057 	or	a, a
   4C70 28 2C         [12] 2058 	jr	Z,00123$
                           2059 ;src/game.c:325: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
   4C72 21 09 09      [10] 2060 	ld	hl, #0x0909
   4C75 E5            [11] 2061 	push	hl
   4C76 CD 46 63      [17] 2062 	call	_cpct_px2byteM0
   4C79 4D            [ 4] 2063 	ld	c, l
   4C7A 3A FA 64      [13] 2064 	ld	a,(#_g_checkpointy + 0)
   4C7D C6 F8         [ 7] 2065 	add	a, #0xf8
   4C7F 47            [ 4] 2066 	ld	b, a
   4C80 C5            [11] 2067 	push	bc
   4C81 C5            [11] 2068 	push	bc
   4C82 33            [ 6] 2069 	inc	sp
   4C83 3A F9 64      [13] 2070 	ld	a, (_g_checkpointx)
   4C86 F5            [11] 2071 	push	af
   4C87 33            [ 6] 2072 	inc	sp
   4C88 21 00 C0      [10] 2073 	ld	hl, #0xc000
   4C8B E5            [11] 2074 	push	hl
   4C8C CD 39 64      [17] 2075 	call	_cpct_getScreenPtr
   4C8F C1            [10] 2076 	pop	bc
   4C90 11 02 08      [10] 2077 	ld	de, #0x0802
   4C93 D5            [11] 2078 	push	de
   4C94 79            [ 4] 2079 	ld	a, c
   4C95 F5            [11] 2080 	push	af
   4C96 33            [ 6] 2081 	inc	sp
   4C97 E5            [11] 2082 	push	hl
   4C98 CD 80 63      [17] 2083 	call	_cpct_drawSolidBox
   4C9B F1            [10] 2084 	pop	af
   4C9C F1            [10] 2085 	pop	af
   4C9D 33            [ 6] 2086 	inc	sp
   4C9E                    2087 00123$:
   4C9E DD F9         [10] 2088 	ld	sp, ix
   4CA0 DD E1         [14] 2089 	pop	ix
   4CA2 C9            [10] 2090 	ret
                           2091 	.area _CODE
                           2092 	.area _INITIALIZER
                           2093 	.area _CABS (ABS)
