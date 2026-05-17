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
   6371                      52 _g_player:
   6371                      53 	.ds 10
   637B                      54 _g_enemies:
   637B                      55 	.ds 60
   63B7                      56 _g_projectiles:
   63B7                      57 	.ds 60
   63F3                      58 _g_lives:
   63F3                      59 	.ds 1
   63F4                      60 _g_score:
   63F4                      61 	.ds 2
   63F6                      62 _g_timeleft:
   63F6                      63 	.ds 1
   63F7                      64 _g_weapondisplay:
   63F7                      65 	.ds 1
   63F8                      66 _g_currentwave:
   63F8                      67 	.ds 1
   63F9                      68 _g_aliveenemies:
   63F9                      69 	.ds 1
   63FA                      70 _g_wavecooldown:
   63FA                      71 	.ds 1
   63FB                      72 _g_damagecooldown:
   63FB                      73 	.ds 1
   63FC                      74 _g_shootcooldown:
   63FC                      75 	.ds 1
   63FD                      76 _g_victory:
   63FD                      77 	.ds 1
   63FE                      78 _g_gameover:
   63FE                      79 	.ds 1
   63FF                      80 _g_framecounter:
   63FF                      81 	.ds 2
   6401                      82 _g_checkpointx:
   6401                      83 	.ds 1
   6402                      84 _g_checkpointy:
   6402                      85 	.ds 1
   6403                      86 _g_checkpointactive:
   6403                      87 	.ds 1
   6404                      88 _g_boss:
   6404                      89 	.ds 10
   640E                      90 _g_bossactive:
   640E                      91 	.ds 1
   640F                      92 _g_bossphase:
   640F                      93 	.ds 1
   6410                      94 _g_weaponlevel:
   6410                      95 	.ds 1
   6411                      96 _g_pickuptaken:
   6411                      97 	.ds 1
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
   4000 21 71 63      [10]  128 	ld	hl, #_g_player
   4003 3A 01 64      [13]  129 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  130 	ld	(hl), a
                            131 ;src/game.c:43: g_player.y = g_checkpointy;
   4007 21 72 63      [10]  132 	ld	hl, #(_g_player + 0x0001)
   400A 3A 02 64      [13]  133 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  134 	ld	(hl), a
                            135 ;src/game.c:44: g_player.vx = 0;
   400E 21 73 63      [10]  136 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  137 	ld	(hl), #0x00
                            138 ;src/game.c:45: g_player.vy = 0;
   4013 21 74 63      [10]  139 	ld	hl, #(_g_player + 0x0003)
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
   40B1 01 7B 63      [10]  235 	ld	bc, #_g_enemies+0
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
   40C4 CD 27 55      [17]  252 	call	_enemyinit
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
   40E2 DD 36 FB 02   [19]  275 	ld	-5 (ix), #0x02
   40E6 18 0E         [12]  276 	jr	00107$
   40E8                     277 00106$:
                            278 ;src/game.c:65: else if (wave == 1) count = 3;
   40E8 7B            [ 4]  279 	ld	a, e
   40E9 B7            [ 4]  280 	or	a, a
   40EA 28 06         [12]  281 	jr	Z,00103$
   40EC DD 36 FB 03   [19]  282 	ld	-5 (ix), #0x03
   40F0 18 04         [12]  283 	jr	00107$
   40F2                     284 00103$:
                            285 ;src/game.c:66: else count = 4;
   40F2 DD 36 FB 04   [19]  286 	ld	-5 (ix), #0x04
   40F6                     287 00107$:
                            288 ;src/game.c:68: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F6 3E 06         [ 7]  289 	ld	a, #0x06
   40F8 DD 96 FB      [19]  290 	sub	a, -5 (ix)
   40FB 30 04         [12]  291 	jr	NC,00148$
   40FD DD 36 FB 06   [19]  292 	ld	-5 (ix), #0x06
                            293 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4101                     294 00148$:
   4101 DD 73 FF      [19]  295 	ld	-1 (ix), e
   4104 DD 36 FC 00   [19]  296 	ld	-4 (ix), #0x00
   4108                     297 00120$:
   4108 DD 7E FC      [19]  298 	ld	a, -4 (ix)
   410B DD 96 FB      [19]  299 	sub	a, -5 (ix)
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
   4120 DD 7E FC      [19]  312 	ld	a, -4 (ix)
   4123 B7            [ 4]  313 	or	a, a
   4124 20 04         [12]  314 	jr	NZ,00124$
   4126 1E 01         [ 7]  315 	ld	e, #0x01
   4128 18 17         [12]  316 	jr	00115$
   412A                     317 00124$:
   412A 1E 00         [ 7]  318 	ld	e, #0x00
   412C 18 13         [12]  319 	jr	00115$
   412E                     320 00111$:
                            321 ;src/game.c:75: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   412E DD 7E FC      [19]  322 	ld	a, -4 (ix)
   4131 B7            [ 4]  323 	or	a, a
   4132 28 07         [12]  324 	jr	Z,00129$
   4134 DD 7E FC      [19]  325 	ld	a, -4 (ix)
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
   414C DD CB FC 46   [20]  345 	bit	0, -4 (ix)
   4150 28 06         [12]  346 	jr	Z,00133$
   4152 DD 36 FE 01   [19]  347 	ld	-2 (ix), #0x01
   4156 18 04         [12]  348 	jr	00134$
   4158                     349 00133$:
   4158 DD 36 FE 00   [19]  350 	ld	-2 (ix), #0x00
   415C                     351 00134$:
   415C DD 7E FC      [19]  352 	ld	a, -4 (ix)
   415F 07            [ 4]  353 	rlca
   4160 07            [ 4]  354 	rlca
   4161 07            [ 4]  355 	rlca
   4162 E6 F8         [ 7]  356 	and	a, #0xf8
   4164 C6 2E         [ 7]  357 	add	a, #0x2e
   4166 DD 77 FD      [19]  358 	ld	-3 (ix), a
   4169 D5            [11]  359 	push	de
   416A DD 5E FC      [19]  360 	ld	e,-4 (ix)
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
   418C CD E2 56      [17]  385 	call	_enemyspawn
   418F 21 06 00      [10]  386 	ld	hl, #6
   4192 39            [11]  387 	add	hl, sp
   4193 F9            [ 6]  388 	ld	sp, hl
   4194 C1            [10]  389 	pop	bc
                            390 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4195 DD 34 FC      [23]  391 	inc	-4 (ix)
   4198 C3 08 41      [10]  392 	jp	00120$
   419B                     393 00116$:
                            394 ;src/game.c:81: g_aliveenemies = count;
   419B DD 7E FB      [19]  395 	ld	a, -5 (ix)
   419E 32 F9 63      [13]  396 	ld	(#_g_aliveenemies + 0),a
   41A1 DD F9         [10]  397 	ld	sp, ix
   41A3 DD E1         [14]  398 	pop	ix
   41A5 C9            [10]  399 	ret
                            400 ;src/game.c:84: static void spawn_boss(void) {
                            401 ;	---------------------------------
                            402 ; Function spawn_boss
                            403 ; ---------------------------------
   41A6                     404 _spawn_boss:
                            405 ;src/game.c:85: enemyinit(&g_boss);
   41A6 21 04 64      [10]  406 	ld	hl, #_g_boss
   41A9 E5            [11]  407 	push	hl
   41AA CD 27 55      [17]  408 	call	_enemyinit
   41AD F1            [10]  409 	pop	af
                            410 ;src/game.c:86: enemyspawn(&g_boss, 68, 112, 1, 0);
   41AE 21 01 00      [10]  411 	ld	hl, #0x0001
   41B1 E5            [11]  412 	push	hl
   41B2 21 44 70      [10]  413 	ld	hl, #0x7044
   41B5 E5            [11]  414 	push	hl
   41B6 21 04 64      [10]  415 	ld	hl, #_g_boss
   41B9 E5            [11]  416 	push	hl
   41BA CD E2 56      [17]  417 	call	_enemyspawn
   41BD 21 06 00      [10]  418 	ld	hl, #6
   41C0 39            [11]  419 	add	hl, sp
   41C1 F9            [ 6]  420 	ld	sp, hl
                            421 ;src/game.c:87: g_boss.w = 10;
   41C2 21 08 64      [10]  422 	ld	hl, #(_g_boss + 0x0004)
   41C5 36 0A         [10]  423 	ld	(hl), #0x0a
                            424 ;src/game.c:88: g_boss.h = 18;
   41C7 21 09 64      [10]  425 	ld	hl, #(_g_boss + 0x0005)
   41CA 36 12         [10]  426 	ld	(hl), #0x12
                            427 ;src/game.c:89: g_boss.health = 10;
   41CC 21 0B 64      [10]  428 	ld	hl, #(_g_boss + 0x0007)
   41CF 36 0A         [10]  429 	ld	(hl), #0x0a
                            430 ;src/game.c:90: g_boss.reward = 1500;
   41D1 21 0C 64      [10]  431 	ld	hl, #(_g_boss + 0x0008)
   41D4 36 DC         [10]  432 	ld	(hl), #0xdc
                            433 ;src/game.c:91: g_boss.kind = 3;
   41D6 21 0D 64      [10]  434 	ld	hl, #(_g_boss + 0x0009)
   41D9 36 03         [10]  435 	ld	(hl), #0x03
                            436 ;src/game.c:92: g_boss.vx = -1;
   41DB 21 06 64      [10]  437 	ld	hl, #(_g_boss + 0x0002)
   41DE 36 FF         [10]  438 	ld	(hl), #0xff
                            439 ;src/game.c:93: g_bossactive = 1;
   41E0 21 0E 64      [10]  440 	ld	hl,#_g_bossactive + 0
   41E3 36 01         [10]  441 	ld	(hl), #0x01
                            442 ;src/game.c:94: g_bossphase = 0;
   41E5 21 0F 64      [10]  443 	ld	hl,#_g_bossphase + 0
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
   41F5 CD 28 51      [17]  457 	call	_input_is_shoot_just_pressed
   41F8 7D            [ 4]  458 	ld	a, l
   41F9 B7            [ 4]  459 	or	a, a
   41FA CA 8C 42      [10]  460 	jp	Z,00110$
                            461 ;src/game.c:102: if (g_shootcooldown) return;
   41FD 3A FC 63      [13]  462 	ld	a,(#_g_shootcooldown + 0)
   4200 B7            [ 4]  463 	or	a, a
   4201 C2 8C 42      [10]  464 	jp	NZ,00110$
                            465 ;src/game.c:104: dir = g_player.facing_left ? -3 : 3;
   4204 3A 79 63      [13]  466 	ld	a, (#_g_player + 8)
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
   421F 11 B7 63      [10]  487 	ld	de, #_g_projectiles
   4222 19            [11]  488 	add	hl, de
   4223 11 06 00      [10]  489 	ld	de, #0x0006
   4226 19            [11]  490 	add	hl, de
   4227 7E            [ 7]  491 	ld	a, (hl)
   4228 B7            [ 4]  492 	or	a, a
   4229 20 58         [12]  493 	jr	NZ,00109$
                            494 ;src/game.c:109: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
   422B 3A 10 64      [13]  495 	ld	a,(#_g_weaponlevel + 0)
   422E B7            [ 4]  496 	or	a, a
   422F 28 06         [12]  497 	jr	Z,00114$
   4231 DD 36 FE 01   [19]  498 	ld	-2 (ix), #0x01
   4235 18 04         [12]  499 	jr	00115$
   4237                     500 00114$:
   4237 DD 36 FE 00   [19]  501 	ld	-2 (ix), #0x00
   423B                     502 00115$:
   423B 3A 72 63      [13]  503 	ld	a, (#_g_player + 1)
   423E C6 06         [ 7]  504 	add	a, #0x06
   4240 DD 77 FD      [19]  505 	ld	-3 (ix), a
   4243 21 71 63      [10]  506 	ld	hl, #_g_player + 0
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
   4254 11 B7 63      [10]  518 	ld	de, #_g_projectiles
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
   4269 CD 00 5F      [17]  533 	call	_projectilefire
   426C 21 06 00      [10]  534 	ld	hl, #6
   426F 39            [11]  535 	add	hl, sp
   4270 F9            [ 6]  536 	ld	sp, hl
                            537 ;src/game.c:110: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
   4271 3A 10 64      [13]  538 	ld	a,(#_g_weaponlevel + 0)
   4274 B7            [ 4]  539 	or	a, a
   4275 28 04         [12]  540 	jr	Z,00116$
   4277 0E 04         [ 7]  541 	ld	c, #0x04
   4279 18 02         [12]  542 	jr	00117$
   427B                     543 00116$:
   427B 0E 08         [ 7]  544 	ld	c, #0x08
   427D                     545 00117$:
   427D 21 FC 63      [10]  546 	ld	hl,#_g_shootcooldown + 0
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
   4291 FD 21 F3 63   [14]  567 	ld	iy, #_g_lives
   4295 FD 7E 00      [19]  568 	ld	a, 0 (iy)
   4298 B7            [ 4]  569 	or	a, a
   4299 28 03         [12]  570 	jr	Z,00102$
                            571 ;src/game.c:118: g_lives--;
   429B FD 35 00      [23]  572 	dec	0 (iy)
   429E                     573 00102$:
                            574 ;src/game.c:120: if (g_lives == 0) {
   429E 3A F3 63      [13]  575 	ld	a,(#_g_lives + 0)
   42A1 B7            [ 4]  576 	or	a, a
   42A2 20 06         [12]  577 	jr	NZ,00104$
                            578 ;src/game.c:121: g_gameover = 1;
   42A4 21 FE 63      [10]  579 	ld	hl,#_g_gameover + 0
   42A7 36 01         [10]  580 	ld	(hl), #0x01
                            581 ;src/game.c:122: return;
   42A9 C9            [10]  582 	ret
   42AA                     583 00104$:
                            584 ;src/game.c:125: reset_player_to_checkpoint();
   42AA CD 00 40      [17]  585 	call	_reset_player_to_checkpoint
                            586 ;src/game.c:126: g_damagecooldown = 40;
   42AD 21 FB 63      [10]  587 	ld	hl,#_g_damagecooldown + 0
   42B0 36 28         [10]  588 	ld	(hl), #0x28
   42B2 C9            [10]  589 	ret
                            590 ;src/game.c:129: void game_init(void) {
                            591 ;	---------------------------------
                            592 ; Function game_init
                            593 ; ---------------------------------
   42B3                     594 _game_init::
                            595 ;src/game.c:132: cpct_disableFirmware();
   42B3 CD 78 62      [17]  596 	call	_cpct_disableFirmware
                            597 ;src/game.c:133: cpct_setVideoMode(0);
   42B6 2E 00         [ 7]  598 	ld	l, #0x00
   42B8 CD 40 62      [17]  599 	call	_cpct_setVideoMode
                            600 ;src/game.c:134: cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
   42BB 21 10 00      [10]  601 	ld	hl, #0x0010
   42BE E5            [11]  602 	push	hl
   42BF 21 D7 52      [10]  603 	ld	hl, #_gpalette
   42C2 E5            [11]  604 	push	hl
   42C3 CD 4F 61      [17]  605 	call	_cpct_setPalette
                            606 ;src/game.c:135: cpct_setBorder(gpalette[0]);
   42C6 21 D7 52      [10]  607 	ld	hl, #_gpalette + 0
   42C9 46            [ 7]  608 	ld	b, (hl)
   42CA C5            [11]  609 	push	bc
   42CB 33            [ 6]  610 	inc	sp
   42CC 3E 10         [ 7]  611 	ld	a, #0x10
   42CE F5            [11]  612 	push	af
   42CF 33            [ 6]  613 	inc	sp
   42D0 CD 66 61      [17]  614 	call	_cpct_setPALColour
                            615 ;src/game.c:136: cpct_clearScreen(0x00);
   42D3 21 00 40      [10]  616 	ld	hl, #0x4000
   42D6 E5            [11]  617 	push	hl
   42D7 AF            [ 4]  618 	xor	a, a
   42D8 F5            [11]  619 	push	af
   42D9 33            [ 6]  620 	inc	sp
   42DA 26 C0         [ 7]  621 	ld	h, #0xc0
   42DC E5            [11]  622 	push	hl
   42DD CD 6A 62      [17]  623 	call	_cpct_memset
                            624 ;src/game.c:137: tilemap_init();
   42E0 CD 3A 51      [17]  625 	call	_tilemap_init
                            626 ;src/game.c:138: collision_init();
   42E3 CD 85 4B      [17]  627 	call	_collision_init
                            628 ;src/game.c:139: playerinit(&g_player);
   42E6 21 71 63      [10]  629 	ld	hl, #_g_player
   42E9 E5            [11]  630 	push	hl
   42EA CD 98 5B      [17]  631 	call	_playerinit
   42ED F1            [10]  632 	pop	af
                            633 ;src/game.c:140: hudinit();
   42EE CD 8A 4F      [17]  634 	call	_hudinit
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
   42FB 11 B7 63      [10]  646 	ld	de, #_g_projectiles
   42FE 19            [11]  647 	add	hl, de
   42FF C5            [11]  648 	push	bc
   4300 E5            [11]  649 	push	hl
   4301 CD A3 5E      [17]  650 	call	_projectileinit
   4304 F1            [10]  651 	pop	af
   4305 C1            [10]  652 	pop	bc
                            653 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4306 0C            [ 4]  654 	inc	c
   4307 79            [ 4]  655 	ld	a, c
   4308 D6 06         [ 7]  656 	sub	a, #0x06
   430A 38 E7         [12]  657 	jr	C,00102$
                            658 ;src/game.c:146: g_lives = 3;
   430C 21 F3 63      [10]  659 	ld	hl,#_g_lives + 0
   430F 36 03         [10]  660 	ld	(hl), #0x03
                            661 ;src/game.c:147: g_score = 0;
   4311 21 00 00      [10]  662 	ld	hl, #0x0000
   4314 22 F4 63      [16]  663 	ld	(_g_score), hl
                            664 ;src/game.c:148: g_timeleft = 99;
   4317 FD 21 F6 63   [14]  665 	ld	iy, #_g_timeleft
   431B FD 36 00 63   [19]  666 	ld	0 (iy), #0x63
                            667 ;src/game.c:149: g_weapondisplay = 1;
   431F FD 21 F7 63   [14]  668 	ld	iy, #_g_weapondisplay
   4323 FD 36 00 01   [19]  669 	ld	0 (iy), #0x01
                            670 ;src/game.c:150: g_currentwave = 0;
   4327 FD 21 F8 63   [14]  671 	ld	iy, #_g_currentwave
   432B FD 36 00 00   [19]  672 	ld	0 (iy), #0x00
                            673 ;src/game.c:151: g_wavecooldown = 1;
   432F FD 21 FA 63   [14]  674 	ld	iy, #_g_wavecooldown
   4333 FD 36 00 01   [19]  675 	ld	0 (iy), #0x01
                            676 ;src/game.c:152: g_damagecooldown = 0;
   4337 FD 21 FB 63   [14]  677 	ld	iy, #_g_damagecooldown
   433B FD 36 00 00   [19]  678 	ld	0 (iy), #0x00
                            679 ;src/game.c:153: g_shootcooldown = 0;
   433F FD 21 FC 63   [14]  680 	ld	iy, #_g_shootcooldown
   4343 FD 36 00 00   [19]  681 	ld	0 (iy), #0x00
                            682 ;src/game.c:154: g_victory = 0;
   4347 FD 21 FD 63   [14]  683 	ld	iy, #_g_victory
   434B FD 36 00 00   [19]  684 	ld	0 (iy), #0x00
                            685 ;src/game.c:155: g_gameover = 0;
   434F FD 21 FE 63   [14]  686 	ld	iy, #_g_gameover
   4353 FD 36 00 00   [19]  687 	ld	0 (iy), #0x00
                            688 ;src/game.c:156: g_framecounter = 0;
   4357 2E 00         [ 7]  689 	ld	l, #0x00
   4359 22 FF 63      [16]  690 	ld	(_g_framecounter), hl
                            691 ;src/game.c:157: g_checkpointx = 20;
   435C 21 01 64      [10]  692 	ld	hl,#_g_checkpointx + 0
   435F 36 14         [10]  693 	ld	(hl), #0x14
                            694 ;src/game.c:158: g_checkpointy = 120;
   4361 21 02 64      [10]  695 	ld	hl,#_g_checkpointy + 0
   4364 36 78         [10]  696 	ld	(hl), #0x78
                            697 ;src/game.c:159: g_checkpointactive = 0;
   4366 21 03 64      [10]  698 	ld	hl,#_g_checkpointactive + 0
   4369 36 00         [10]  699 	ld	(hl), #0x00
                            700 ;src/game.c:160: g_bossactive = 0;
   436B 21 0E 64      [10]  701 	ld	hl,#_g_bossactive + 0
   436E 36 00         [10]  702 	ld	(hl), #0x00
                            703 ;src/game.c:161: g_weaponlevel = 0;
   4370 21 10 64      [10]  704 	ld	hl,#_g_weaponlevel + 0
   4373 36 00         [10]  705 	ld	(hl), #0x00
                            706 ;src/game.c:162: g_pickuptaken = 0;
   4375 21 11 64      [10]  707 	ld	hl,#_g_pickuptaken + 0
   4378 36 00         [10]  708 	ld	(hl), #0x00
                            709 ;src/game.c:163: enemyinit(&g_boss);
   437A 21 04 64      [10]  710 	ld	hl, #_g_boss
   437D E5            [11]  711 	push	hl
   437E CD 27 55      [17]  712 	call	_enemyinit
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
   4390 CD 95 50      [17]  727 	call	_input_update
                            728 ;src/game.c:172: if (g_gameover || g_victory) {
   4393 3A FE 63      [13]  729 	ld	a,(#_g_gameover + 0)
   4396 B7            [ 4]  730 	or	a, a
   4397 20 06         [12]  731 	jr	NZ,00101$
   4399 3A FD 63      [13]  732 	ld	a,(#_g_victory + 0)
   439C B7            [ 4]  733 	or	a, a
   439D 28 1C         [12]  734 	jr	Z,00102$
   439F                     735 00101$:
                            736 ;src/game.c:173: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   439F 3A F7 63      [13]  737 	ld	a, (_g_weapondisplay)
   43A2 F5            [11]  738 	push	af
   43A3 33            [ 6]  739 	inc	sp
   43A4 3A F6 63      [13]  740 	ld	a, (_g_timeleft)
   43A7 F5            [11]  741 	push	af
   43A8 33            [ 6]  742 	inc	sp
   43A9 2A F4 63      [16]  743 	ld	hl, (_g_score)
   43AC E5            [11]  744 	push	hl
   43AD 3A F3 63      [13]  745 	ld	a, (_g_lives)
   43B0 F5            [11]  746 	push	af
   43B1 33            [ 6]  747 	inc	sp
   43B2 CD A5 4F      [17]  748 	call	_hudupdate
   43B5 F1            [10]  749 	pop	af
   43B6 F1            [10]  750 	pop	af
   43B7 33            [ 6]  751 	inc	sp
                            752 ;src/game.c:174: return;
   43B8 C3 A4 49      [10]  753 	jp	00181$
   43BB                     754 00102$:
                            755 ;src/game.c:177: playerupdate(&g_player);
   43BB 21 71 63      [10]  756 	ld	hl, #_g_player
   43BE E5            [11]  757 	push	hl
   43BF CD DE 5B      [17]  758 	call	_playerupdate
   43C2 F1            [10]  759 	pop	af
                            760 ;src/game.c:178: try_fire_projectile();
   43C3 CD EB 41      [17]  761 	call	_try_fire_projectile
                            762 ;src/game.c:180: if (g_shootcooldown) g_shootcooldown--;
   43C6 FD 21 FC 63   [14]  763 	ld	iy, #_g_shootcooldown
   43CA FD 7E 00      [19]  764 	ld	a, 0 (iy)
   43CD B7            [ 4]  765 	or	a, a
   43CE 28 03         [12]  766 	jr	Z,00105$
   43D0 FD 35 00      [23]  767 	dec	0 (iy)
   43D3                     768 00105$:
                            769 ;src/game.c:181: if (g_damagecooldown) g_damagecooldown--;
   43D3 FD 21 FB 63   [14]  770 	ld	iy, #_g_damagecooldown
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
   43EA 11 B7 63      [10]  787 	ld	de, #_g_projectiles
   43ED 19            [11]  788 	add	hl, de
   43EE C5            [11]  789 	push	bc
   43EF E5            [11]  790 	push	hl
   43F0 CD B7 5F      [17]  791 	call	_projectileupdate
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
   4405 11 7B 63      [10]  810 	ld	de, #_g_enemies
   4408 19            [11]  811 	add	hl, de
   4409 C5            [11]  812 	push	bc
   440A E5            [11]  813 	push	hl
   440B CD BA 58      [17]  814 	call	_enemyupdate
   440E F1            [10]  815 	pop	af
   440F C1            [10]  816 	pop	bc
                            817 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   4410 0C            [ 4]  818 	inc	c
   4411 79            [ 4]  819 	ld	a, c
   4412 D6 06         [ 7]  820 	sub	a, #0x06
   4414 38 E7         [12]  821 	jr	C,00176$
                            822 ;src/game.c:191: if (g_bossactive) {
   4416 3A 0E 64      [13]  823 	ld	a,(#_g_bossactive + 0)
   4419 B7            [ 4]  824 	or	a, a
   441A 28 71         [12]  825 	jr	Z,00211$
                            826 ;src/game.c:192: if (g_boss.health > 4) g_bossphase = 0;
   441C 21 0B 64      [10]  827 	ld	hl, #_g_boss + 7
   441F 4E            [ 7]  828 	ld	c, (hl)
   4420 3E 04         [ 7]  829 	ld	a, #0x04
   4422 91            [ 4]  830 	sub	a, c
   4423 30 07         [12]  831 	jr	NC,00111$
   4425 21 0F 64      [10]  832 	ld	hl,#_g_bossphase + 0
   4428 36 00         [10]  833 	ld	(hl), #0x00
   442A 18 05         [12]  834 	jr	00112$
   442C                     835 00111$:
                            836 ;src/game.c:193: else g_bossphase = 1;
   442C 21 0F 64      [10]  837 	ld	hl,#_g_bossphase + 0
   442F 36 01         [10]  838 	ld	(hl), #0x01
   4431                     839 00112$:
                            840 ;src/game.c:195: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4431 3A 71 63      [13]  841 	ld	a,(#_g_player + 0)
   4434 DD 77 EF      [19]  842 	ld	-17 (ix), a
   4437 DD 77 ED      [19]  843 	ld	-19 (ix), a
   443A DD 36 EE 00   [19]  844 	ld	-18 (ix), #0x00
   443E DD 7E ED      [19]  845 	ld	a, -19 (ix)
   4441 C6 02         [ 7]  846 	add	a, #0x02
   4443 DD 77 ED      [19]  847 	ld	-19 (ix), a
   4446 DD 7E EE      [19]  848 	ld	a, -18 (ix)
   4449 CE 00         [ 7]  849 	adc	a, #0x00
   444B DD 77 EE      [19]  850 	ld	-18 (ix), a
   444E 21 04 64      [10]  851 	ld	hl, #_g_boss + 0
   4451 4E            [ 7]  852 	ld	c, (hl)
   4452 06 00         [ 7]  853 	ld	b, #0x00
   4454 DD 7E ED      [19]  854 	ld	a, -19 (ix)
   4457 91            [ 4]  855 	sub	a, c
   4458 DD 7E EE      [19]  856 	ld	a, -18 (ix)
   445B 98            [ 4]  857 	sbc	a, b
   445C E2 61 44      [10]  858 	jp	PO, 00380$
   445F EE 80         [ 7]  859 	xor	a, #0x80
   4461                     860 00380$:
   4461 F2 75 44      [10]  861 	jp	P, 00183$
   4464 3A 0F 64      [13]  862 	ld	a,(#_g_bossphase + 0)
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
   4475 3A 0F 64      [13]  875 	ld	a,(#_g_bossphase + 0)
   4478 B7            [ 4]  876 	or	a, a
   4479 28 04         [12]  877 	jr	Z,00187$
   447B 0E 02         [ 7]  878 	ld	c, #0x02
   447D 18 02         [12]  879 	jr	00188$
   447F                     880 00187$:
   447F 0E 01         [ 7]  881 	ld	c, #0x01
   4481                     882 00188$:
   4481                     883 00184$:
   4481 21 06 64      [10]  884 	ld	hl, #(_g_boss + 0x0002)
   4484 71            [ 7]  885 	ld	(hl), c
                            886 ;src/game.c:196: enemyupdate(&g_boss);
   4485 21 04 64      [10]  887 	ld	hl, #_g_boss
   4488 E5            [11]  888 	push	hl
   4489 CD BA 58      [17]  889 	call	_enemyupdate
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
   4498 21 B7 63      [10]  904 	ld	hl, #_g_projectiles
   449B 19            [11]  905 	add	hl,de
   449C EB            [ 4]  906 	ex	de,hl
   449D 21 06 00      [10]  907 	ld	hl, #0x0006
   44A0 19            [11]  908 	add	hl,de
   44A1 DD 75 ED      [19]  909 	ld	-19 (ix), l
   44A4 DD 74 EE      [19]  910 	ld	-18 (ix), h
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
   44BD 3E 7B         [ 7]  928 	ld	a, #<(_g_enemies)
   44BF 85            [ 4]  929 	add	a, l
   44C0 DD 77 FE      [19]  930 	ld	-2 (ix), a
   44C3 3E 63         [ 7]  931 	ld	a, #>(_g_enemies)
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
   450F DD 77 EF      [19]  972 	ld	-17 (ix), a
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
   4555 DD 75 EB      [19] 1003 	ld	-21 (ix), l
   4558 DD 36 EC 00   [19] 1004 	ld	-20 (ix), #0x00
   455C 1A            [ 7] 1005 	ld	a, (de)
   455D DD 77 E9      [19] 1006 	ld	-23 (ix), a
   4560 DD 36 EA 00   [19] 1007 	ld	-22 (ix), #0x00
   4564 C5            [11] 1008 	push	bc
   4565 D5            [11] 1009 	push	de
   4566 DD 66 EF      [19] 1010 	ld	h, -17 (ix)
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
   4582 DD 6E EB      [19] 1024 	ld	l,-21 (ix)
   4585 DD 66 EC      [19] 1025 	ld	h,-20 (ix)
   4588 E5            [11] 1026 	push	hl
   4589 DD 6E E9      [19] 1027 	ld	l,-23 (ix)
   458C DD 66 EA      [19] 1028 	ld	h,-22 (ix)
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
   45B4 CD 58 5B      [17] 1051 	call	_enemydamage
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
   45CC DD 75 E9      [19] 1067 	ld	-23 (ix), l
   45CF DD 36 EA 00   [19] 1068 	ld	-22 (ix), #0x00
   45D3 21 F4 63      [10] 1069 	ld	hl, #_g_score
   45D6 7E            [ 7] 1070 	ld	a, (hl)
   45D7 DD 86 E9      [19] 1071 	add	a, -23 (ix)
   45DA 77            [ 7] 1072 	ld	(hl), a
   45DB 23            [ 6] 1073 	inc	hl
   45DC 7E            [ 7] 1074 	ld	a, (hl)
   45DD DD 8E EA      [19] 1075 	adc	a, -22 (ix)
   45E0 77            [ 7] 1076 	ld	(hl), a
                           1077 ;src/game.c:207: if (g_aliveenemies) g_aliveenemies--;
   45E1 FD 21 F9 63   [14] 1078 	ld	iy, #_g_aliveenemies
   45E5 FD 7E 00      [19] 1079 	ld	a, 0 (iy)
   45E8 B7            [ 4] 1080 	or	a, a
   45E9 28 03         [12] 1081 	jr	Z,00124$
   45EB FD 35 00      [23] 1082 	dec	0 (iy)
   45EE                    1083 00124$:
                           1084 ;src/game.c:209: g_projectiles[i].active = 0;
   45EE DD 6E ED      [19] 1085 	ld	l,-19 (ix)
   45F1 DD 66 EE      [19] 1086 	ld	h,-18 (ix)
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
   4603 3A 0E 64      [13] 1098 	ld	a,(#_g_bossactive + 0)
   4606 B7            [ 4] 1099 	or	a, a
   4607 CA CA 46      [10] 1100 	jp	Z, 00133$
   460A DD 6E ED      [19] 1101 	ld	l,-19 (ix)
   460D DD 66 EE      [19] 1102 	ld	h,-18 (ix)
   4610 7E            [ 7] 1103 	ld	a, (hl)
   4611 B7            [ 4] 1104 	or	a, a
   4612 CA CA 46      [10] 1105 	jp	Z, 00133$
                           1106 ;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   4615 21 09 64      [10] 1107 	ld	hl, #(_g_boss + 0x0005) + 0
   4618 46            [ 7] 1108 	ld	b, (hl)
   4619 3A 08 64      [13] 1109 	ld	a, (#(_g_boss + 0x0004) + 0)
   461C 21 05 64      [10] 1110 	ld	hl, #(_g_boss + 0x0001) + 0
   461F 6E            [ 7] 1111 	ld	l, (hl)
   4620 DD 75 E9      [19] 1112 	ld	-23 (ix), l
   4623 DD 36 EA 00   [19] 1113 	ld	-22 (ix), #0x00
   4627 21 04 64      [10] 1114 	ld	hl, #_g_boss + 0
   462A 6E            [ 7] 1115 	ld	l, (hl)
   462B DD 75 EB      [19] 1116 	ld	-21 (ix), l
   462E DD 36 EC 00   [19] 1117 	ld	-20 (ix), #0x00
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
   4663 DD 6E E9      [19] 1146 	ld	l,-23 (ix)
   4666 DD 66 EA      [19] 1147 	ld	h,-22 (ix)
   4669 E5            [11] 1148 	push	hl
   466A DD 6E EB      [19] 1149 	ld	l,-21 (ix)
   466D DD 66 EC      [19] 1150 	ld	h,-20 (ix)
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
   4690 DD 6E ED      [19] 1168 	ld	l,-19 (ix)
   4693 DD 66 EE      [19] 1169 	ld	h,-18 (ix)
   4696 36 00         [10] 1170 	ld	(hl), #0x00
                           1171 ;src/game.c:216: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   4698 DD 6E F6      [19] 1172 	ld	l,-10 (ix)
   469B DD 66 F7      [19] 1173 	ld	h,-9 (ix)
   469E 46            [ 7] 1174 	ld	b, (hl)
   469F 11 04 64      [10] 1175 	ld	de, #_g_boss
   46A2 C5            [11] 1176 	push	bc
   46A3 C5            [11] 1177 	push	bc
   46A4 33            [ 6] 1178 	inc	sp
   46A5 D5            [11] 1179 	push	de
   46A6 CD 58 5B      [17] 1180 	call	_enemydamage
   46A9 F1            [10] 1181 	pop	af
   46AA 33            [ 6] 1182 	inc	sp
   46AB C1            [10] 1183 	pop	bc
   46AC 7D            [ 4] 1184 	ld	a, l
   46AD B7            [ 4] 1185 	or	a, a
   46AE 28 1A         [12] 1186 	jr	Z,00133$
                           1187 ;src/game.c:217: g_bossactive = 0;
   46B0 21 0E 64      [10] 1188 	ld	hl,#_g_bossactive + 0
   46B3 36 00         [10] 1189 	ld	(hl), #0x00
                           1190 ;src/game.c:218: g_score = (u16)(g_score + g_boss.reward);
   46B5 21 0C 64      [10] 1191 	ld	hl, #_g_boss + 8
   46B8 5E            [ 7] 1192 	ld	e, (hl)
   46B9 16 00         [ 7] 1193 	ld	d, #0x00
   46BB 21 F4 63      [10] 1194 	ld	hl, #_g_score
   46BE 7E            [ 7] 1195 	ld	a, (hl)
   46BF 83            [ 4] 1196 	add	a, e
   46C0 77            [ 7] 1197 	ld	(hl), a
   46C1 23            [ 6] 1198 	inc	hl
   46C2 7E            [ 7] 1199 	ld	a, (hl)
   46C3 8A            [ 4] 1200 	adc	a, d
   46C4 77            [ 7] 1201 	ld	(hl), a
                           1202 ;src/game.c:219: g_victory = 1;
   46C5 21 FD 63      [10] 1203 	ld	hl,#_g_victory + 0
   46C8 36 01         [10] 1204 	ld	(hl), #0x01
   46CA                    1205 00133$:
                           1206 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   46CA 0C            [ 4] 1207 	inc	c
   46CB 79            [ 4] 1208 	ld	a, c
   46CC D6 06         [ 7] 1209 	sub	a, #0x06
   46CE DA 8F 44      [10] 1210 	jp	C, 00179$
                           1211 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1212 ;src/game.c:224: if (!g_damagecooldown) {
   46D1 3A FB 63      [13] 1213 	ld	a,(#_g_damagecooldown + 0)
   46D4 B7            [ 4] 1214 	or	a, a
   46D5 C2 42 48      [10] 1215 	jp	NZ, 00149$
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
   46E7 01 7B 63      [10] 1228 	ld	bc,#_g_enemies
   46EA 09            [11] 1229 	add	hl,bc
   46EB DD 75 E9      [19] 1230 	ld	-23 (ix), l
   46EE DD 74 EA      [19] 1231 	ld	-22 (ix), h
   46F1 C1            [10] 1232 	pop	bc
   46F2 E1            [10] 1233 	pop	hl
   46F3 E5            [11] 1234 	push	hl
   46F4 C5            [11] 1235 	push	bc
   46F5 11 06 00      [10] 1236 	ld	de, #0x0006
   46F8 19            [11] 1237 	add	hl, de
   46F9 7E            [ 7] 1238 	ld	a, (hl)
   46FA B7            [ 4] 1239 	or	a, a
   46FB CA 8C 47      [10] 1240 	jp	Z, 00139$
                           1241 ;src/game.c:228: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   46FE DD 7E E9      [19] 1242 	ld	a, -23 (ix)
   4701 DD 77 EB      [19] 1243 	ld	-21 (ix), a
   4704 DD 7E EA      [19] 1244 	ld	a, -22 (ix)
   4707 DD 77 EC      [19] 1245 	ld	-20 (ix), a
   470A DD 6E EB      [19] 1246 	ld	l,-21 (ix)
   470D DD 66 EC      [19] 1247 	ld	h,-20 (ix)
   4710 11 05 00      [10] 1248 	ld	de, #0x0005
   4713 19            [11] 1249 	add	hl, de
   4714 7E            [ 7] 1250 	ld	a, (hl)
   4715 DD 77 EB      [19] 1251 	ld	-21 (ix), a
   4718 C1            [10] 1252 	pop	bc
   4719 E1            [10] 1253 	pop	hl
   471A E5            [11] 1254 	push	hl
   471B C5            [11] 1255 	push	bc
   471C 11 04 00      [10] 1256 	ld	de, #0x0004
   471F 19            [11] 1257 	add	hl, de
   4720 5E            [ 7] 1258 	ld	e, (hl)
   4721 C1            [10] 1259 	pop	bc
   4722 E1            [10] 1260 	pop	hl
   4723 E5            [11] 1261 	push	hl
   4724 C5            [11] 1262 	push	bc
   4725 23            [ 6] 1263 	inc	hl
   4726 4E            [ 7] 1264 	ld	c, (hl)
   4727 06 00         [ 7] 1265 	ld	b, #0x00
   4729 DD 6E E9      [19] 1266 	ld	l,-23 (ix)
   472C DD 66 EA      [19] 1267 	ld	h,-22 (ix)
   472F 56            [ 7] 1268 	ld	d, (hl)
   4730 DD 72 E9      [19] 1269 	ld	-23 (ix), d
   4733 DD 36 EA 00   [19] 1270 	ld	-22 (ix), #0x00
                           1271 ;src/game.c:227: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4737 3A 76 63      [13] 1272 	ld	a,(#(_g_player + 0x0005) + 0)
   473A DD 77 F0      [19] 1273 	ld	-16 (ix), a
   473D 3A 75 63      [13] 1274 	ld	a,(#(_g_player + 0x0004) + 0)
   4740 DD 77 F1      [19] 1275 	ld	-15 (ix), a
   4743 3A 72 63      [13] 1276 	ld	a, (#(_g_player + 0x0001) + 0)
   4746 DD 77 F3      [19] 1277 	ld	-13 (ix), a
   4749 DD 36 F4 00   [19] 1278 	ld	-12 (ix), #0x00
   474D 3A 71 63      [13] 1279 	ld	a, (#_g_player + 0)
   4750 DD 77 F6      [19] 1280 	ld	-10 (ix), a
   4753 DD 36 F7 00   [19] 1281 	ld	-9 (ix), #0x00
   4757 DD 56 EB      [19] 1282 	ld	d, -21 (ix)
   475A D5            [11] 1283 	push	de
   475B C5            [11] 1284 	push	bc
   475C DD 6E E9      [19] 1285 	ld	l,-23 (ix)
   475F DD 66 EA      [19] 1286 	ld	h,-22 (ix)
   4762 E5            [11] 1287 	push	hl
   4763 DD 66 F0      [19] 1288 	ld	h, -16 (ix)
   4766 DD 6E F1      [19] 1289 	ld	l, -15 (ix)
   4769 E5            [11] 1290 	push	hl
   476A DD 6E F3      [19] 1291 	ld	l,-13 (ix)
   476D DD 66 F4      [19] 1292 	ld	h,-12 (ix)
   4770 E5            [11] 1293 	push	hl
   4771 DD 6E F6      [19] 1294 	ld	l,-10 (ix)
   4774 DD 66 F7      [19] 1295 	ld	h,-9 (ix)
   4777 E5            [11] 1296 	push	hl
   4778 CD 19 40      [17] 1297 	call	_rect_overlap
   477B FD 21 0C 00   [14] 1298 	ld	iy, #12
   477F FD 39         [15] 1299 	add	iy, sp
   4781 FD F9         [10] 1300 	ld	sp, iy
   4783 7D            [ 4] 1301 	ld	a, l
   4784 B7            [ 4] 1302 	or	a, a
   4785 28 05         [12] 1303 	jr	Z,00139$
                           1304 ;src/game.c:229: register_player_hit();
   4787 CD 91 42      [17] 1305 	call	_register_player_hit
                           1306 ;src/game.c:230: break;
   478A 18 0B         [12] 1307 	jr	00140$
   478C                    1308 00139$:
                           1309 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   478C DD 34 E8      [23] 1310 	inc	-24 (ix)
   478F DD 7E E8      [19] 1311 	ld	a, -24 (ix)
   4792 D6 06         [ 7] 1312 	sub	a, #0x06
   4794 DA DC 46      [10] 1313 	jp	C, 00180$
   4797                    1314 00140$:
                           1315 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4797 3A FB 63      [13] 1316 	ld	a,(#_g_damagecooldown + 0)
   479A B7            [ 4] 1317 	or	a, a
   479B 20 6E         [12] 1318 	jr	NZ,00142$
   479D 3A 0E 64      [13] 1319 	ld	a,(#_g_bossactive + 0)
   47A0 B7            [ 4] 1320 	or	a, a
   47A1 28 68         [12] 1321 	jr	Z,00142$
                           1322 ;src/game.c:235: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   47A3 3A 09 64      [13] 1323 	ld	a,(#(_g_boss + 0x0005) + 0)
   47A6 DD 77 E9      [19] 1324 	ld	-23 (ix), a
   47A9 3A 08 64      [13] 1325 	ld	a,(#(_g_boss + 0x0004) + 0)
   47AC DD 77 EB      [19] 1326 	ld	-21 (ix), a
   47AF 21 05 64      [10] 1327 	ld	hl, #(_g_boss + 0x0001) + 0
   47B2 5E            [ 7] 1328 	ld	e, (hl)
   47B3 16 00         [ 7] 1329 	ld	d, #0x00
   47B5 21 04 64      [10] 1330 	ld	hl, #_g_boss + 0
   47B8 4E            [ 7] 1331 	ld	c, (hl)
   47B9 06 00         [ 7] 1332 	ld	b, #0x00
                           1333 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   47BB 3A 76 63      [13] 1334 	ld	a,(#(_g_player + 0x0005) + 0)
   47BE DD 77 F0      [19] 1335 	ld	-16 (ix), a
   47C1 3A 75 63      [13] 1336 	ld	a,(#(_g_player + 0x0004) + 0)
   47C4 DD 77 F1      [19] 1337 	ld	-15 (ix), a
   47C7 3A 72 63      [13] 1338 	ld	a, (#(_g_player + 0x0001) + 0)
   47CA DD 77 F3      [19] 1339 	ld	-13 (ix), a
   47CD DD 36 F4 00   [19] 1340 	ld	-12 (ix), #0x00
   47D1 3A 71 63      [13] 1341 	ld	a, (#_g_player + 0)
   47D4 DD 77 F6      [19] 1342 	ld	-10 (ix), a
   47D7 DD 36 F7 00   [19] 1343 	ld	-9 (ix), #0x00
   47DB DD 66 E9      [19] 1344 	ld	h, -23 (ix)
   47DE DD 6E EB      [19] 1345 	ld	l, -21 (ix)
   47E1 E5            [11] 1346 	push	hl
   47E2 D5            [11] 1347 	push	de
   47E3 C5            [11] 1348 	push	bc
   47E4 DD 66 F0      [19] 1349 	ld	h, -16 (ix)
   47E7 DD 6E F1      [19] 1350 	ld	l, -15 (ix)
   47EA E5            [11] 1351 	push	hl
   47EB DD 6E F3      [19] 1352 	ld	l,-13 (ix)
   47EE DD 66 F4      [19] 1353 	ld	h,-12 (ix)
   47F1 E5            [11] 1354 	push	hl
   47F2 DD 6E F6      [19] 1355 	ld	l,-10 (ix)
   47F5 DD 66 F7      [19] 1356 	ld	h,-9 (ix)
   47F8 E5            [11] 1357 	push	hl
   47F9 CD 19 40      [17] 1358 	call	_rect_overlap
   47FC FD 21 0C 00   [14] 1359 	ld	iy, #12
   4800 FD 39         [15] 1360 	add	iy, sp
   4802 FD F9         [10] 1361 	ld	sp, iy
   4804 7D            [ 4] 1362 	ld	a, l
   4805 B7            [ 4] 1363 	or	a, a
   4806 28 03         [12] 1364 	jr	Z,00142$
                           1365 ;src/game.c:236: register_player_hit();
   4808 CD 91 42      [17] 1366 	call	_register_player_hit
   480B                    1367 00142$:
                           1368 ;src/game.c:239: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   480B 3A FB 63      [13] 1369 	ld	a,(#_g_damagecooldown + 0)
   480E B7            [ 4] 1370 	or	a, a
   480F 20 31         [12] 1371 	jr	NZ,00149$
   4811 3A 76 63      [13] 1372 	ld	a, (#(_g_player + 0x0005) + 0)
   4814 21 75 63      [10] 1373 	ld	hl, #(_g_player + 0x0004) + 0
   4817 56            [ 7] 1374 	ld	d, (hl)
   4818 21 72 63      [10] 1375 	ld	hl, #(_g_player + 0x0001) + 0
   481B 4E            [ 7] 1376 	ld	c, (hl)
   481C 06 00         [ 7] 1377 	ld	b, #0x00
   481E 21 71 63      [10] 1378 	ld	hl, #_g_player + 0
   4821 6E            [ 7] 1379 	ld	l, (hl)
   4822 DD 75 E9      [19] 1380 	ld	-23 (ix), l
   4825 DD 36 EA 00   [19] 1381 	ld	-22 (ix), #0x00
   4829 F5            [11] 1382 	push	af
   482A 33            [ 6] 1383 	inc	sp
   482B D5            [11] 1384 	push	de
   482C 33            [ 6] 1385 	inc	sp
   482D C5            [11] 1386 	push	bc
   482E DD 6E E9      [19] 1387 	ld	l,-23 (ix)
   4831 DD 66 EA      [19] 1388 	ld	h,-22 (ix)
   4834 E5            [11] 1389 	push	hl
   4835 CD D7 4C      [17] 1390 	call	_collision_is_on_trap
   4838 F1            [10] 1391 	pop	af
   4839 F1            [10] 1392 	pop	af
   483A F1            [10] 1393 	pop	af
   483B 7D            [ 4] 1394 	ld	a, l
   483C B7            [ 4] 1395 	or	a, a
   483D 28 03         [12] 1396 	jr	Z,00149$
                           1397 ;src/game.c:240: register_player_hit();
   483F CD 91 42      [17] 1398 	call	_register_player_hit
   4842                    1399 00149$:
                           1400 ;src/game.c:244: if (!g_checkpointactive && g_player.x >= 44) {
   4842 FD 21 03 64   [14] 1401 	ld	iy, #_g_checkpointactive
   4846 FD 7E 00      [19] 1402 	ld	a, 0 (iy)
   4849 B7            [ 4] 1403 	or	a, a
   484A 20 1E         [12] 1404 	jr	NZ,00151$
   484C 3A 71 63      [13] 1405 	ld	a, (#_g_player + 0)
   484F D6 2C         [ 7] 1406 	sub	a, #0x2c
   4851 38 17         [12] 1407 	jr	C,00151$
                           1408 ;src/game.c:245: g_checkpointactive = 1;
   4853 FD 36 00 01   [19] 1409 	ld	0 (iy), #0x01
                           1410 ;src/game.c:246: g_checkpointx = 52;
   4857 21 01 64      [10] 1411 	ld	hl,#_g_checkpointx + 0
   485A 36 34         [10] 1412 	ld	(hl), #0x34
                           1413 ;src/game.c:247: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   485C CD 07 52      [17] 1414 	call	_tilemap_ground_y
   485F 4D            [ 4] 1415 	ld	c, l
   4860 21 76 63      [10] 1416 	ld	hl, #(_g_player + 0x0005) + 0
   4863 46            [ 7] 1417 	ld	b, (hl)
   4864 21 02 64      [10] 1418 	ld	hl, #_g_checkpointy
   4867 79            [ 4] 1419 	ld	a, c
   4868 90            [ 4] 1420 	sub	a, b
   4869 77            [ 7] 1421 	ld	(hl), a
   486A                    1422 00151$:
                           1423 ;src/game.c:250: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
   486A 3A 11 64      [13] 1424 	ld	a,(#_g_pickuptaken + 0)
   486D B7            [ 4] 1425 	or	a, a
   486E C2 FD 48      [10] 1426 	jp	NZ, 00154$
   4871 CD 07 52      [17] 1427 	call	_tilemap_ground_y
   4874 DD 75 E9      [19] 1428 	ld	-23 (ix), l
   4877 DD 75 E9      [19] 1429 	ld	-23 (ix), l
   487A DD 36 EA 00   [19] 1430 	ld	-22 (ix), #0x00
   487E DD 7E E9      [19] 1431 	ld	a, -23 (ix)
   4881 C6 F8         [ 7] 1432 	add	a, #0xf8
   4883 DD 77 E9      [19] 1433 	ld	-23 (ix), a
   4886 DD 7E EA      [19] 1434 	ld	a, -22 (ix)
   4889 CE FF         [ 7] 1435 	adc	a, #0xff
   488B DD 77 EA      [19] 1436 	ld	-22 (ix), a
   488E 3A 76 63      [13] 1437 	ld	a,(#(_g_player + 0x0005) + 0)
   4891 DD 77 EB      [19] 1438 	ld	-21 (ix), a
   4894 3A 75 63      [13] 1439 	ld	a,(#(_g_player + 0x0004) + 0)
   4897 DD 77 F0      [19] 1440 	ld	-16 (ix), a
   489A 3A 72 63      [13] 1441 	ld	a,(#(_g_player + 0x0001) + 0)
   489D DD 77 F1      [19] 1442 	ld	-15 (ix), a
   48A0 DD 77 F1      [19] 1443 	ld	-15 (ix), a
   48A3 DD 36 F2 00   [19] 1444 	ld	-14 (ix), #0x00
   48A7 3A 71 63      [13] 1445 	ld	a,(#_g_player + 0)
   48AA DD 77 F3      [19] 1446 	ld	-13 (ix), a
   48AD DD 77 F3      [19] 1447 	ld	-13 (ix), a
   48B0 DD 36 F4 00   [19] 1448 	ld	-12 (ix), #0x00
   48B4 21 04 04      [10] 1449 	ld	hl, #0x0404
   48B7 E5            [11] 1450 	push	hl
   48B8 DD 6E E9      [19] 1451 	ld	l,-23 (ix)
   48BB DD 66 EA      [19] 1452 	ld	h,-22 (ix)
   48BE E5            [11] 1453 	push	hl
   48BF 21 24 00      [10] 1454 	ld	hl, #0x0024
   48C2 E5            [11] 1455 	push	hl
   48C3 DD 66 EB      [19] 1456 	ld	h, -21 (ix)
   48C6 DD 6E F0      [19] 1457 	ld	l, -16 (ix)
   48C9 E5            [11] 1458 	push	hl
   48CA DD 6E F1      [19] 1459 	ld	l,-15 (ix)
   48CD DD 66 F2      [19] 1460 	ld	h,-14 (ix)
   48D0 E5            [11] 1461 	push	hl
   48D1 DD 6E F3      [19] 1462 	ld	l,-13 (ix)
   48D4 DD 66 F4      [19] 1463 	ld	h,-12 (ix)
   48D7 E5            [11] 1464 	push	hl
   48D8 CD 19 40      [17] 1465 	call	_rect_overlap
   48DB FD 21 0C 00   [14] 1466 	ld	iy, #12
   48DF FD 39         [15] 1467 	add	iy, sp
   48E1 FD F9         [10] 1468 	ld	sp, iy
   48E3 7D            [ 4] 1469 	ld	a, l
   48E4 B7            [ 4] 1470 	or	a, a
   48E5 28 16         [12] 1471 	jr	Z,00154$
                           1472 ;src/game.c:251: g_pickuptaken = 1;
   48E7 21 11 64      [10] 1473 	ld	hl,#_g_pickuptaken + 0
   48EA 36 01         [10] 1474 	ld	(hl), #0x01
                           1475 ;src/game.c:252: g_weaponlevel = 1;
   48EC 21 10 64      [10] 1476 	ld	hl,#_g_weaponlevel + 0
   48EF 36 01         [10] 1477 	ld	(hl), #0x01
                           1478 ;src/game.c:253: g_score = (u16)(g_score + 100);
   48F1 21 F4 63      [10] 1479 	ld	hl, #_g_score
   48F4 7E            [ 7] 1480 	ld	a, (hl)
   48F5 C6 64         [ 7] 1481 	add	a, #0x64
   48F7 77            [ 7] 1482 	ld	(hl), a
   48F8 23            [ 6] 1483 	inc	hl
   48F9 7E            [ 7] 1484 	ld	a, (hl)
   48FA CE 00         [ 7] 1485 	adc	a, #0x00
   48FC 77            [ 7] 1486 	ld	(hl), a
   48FD                    1487 00154$:
                           1488 ;src/game.c:256: g_weapondisplay = (u8)(g_weaponlevel + 1);
   48FD 21 F7 63      [10] 1489 	ld	hl, #_g_weapondisplay
   4900 3A 10 64      [13] 1490 	ld	a,(#_g_weaponlevel + 0)
   4903 3C            [ 4] 1491 	inc	a
   4904 77            [ 7] 1492 	ld	(hl), a
                           1493 ;src/game.c:258: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   4905 3A 0E 64      [13] 1494 	ld	a,(#_g_bossactive + 0)
   4908 B7            [ 4] 1495 	or	a, a
   4909 20 45         [12] 1496 	jr	NZ,00165$
   490B 3A F9 63      [13] 1497 	ld	a,(#_g_aliveenemies + 0)
   490E B7            [ 4] 1498 	or	a, a
   490F 20 3F         [12] 1499 	jr	NZ,00165$
   4911 3A FE 63      [13] 1500 	ld	a,(#_g_gameover + 0)
   4914 B7            [ 4] 1501 	or	a, a
   4915 20 39         [12] 1502 	jr	NZ,00165$
                           1503 ;src/game.c:259: if (g_currentwave < TOTAL_WAVES) {
   4917 3A F8 63      [13] 1504 	ld	a,(#_g_currentwave + 0)
   491A D6 03         [ 7] 1505 	sub	a, #0x03
   491C 30 20         [12] 1506 	jr	NC,00162$
                           1507 ;src/game.c:260: if (g_wavecooldown == 0) {
   491E 3A FA 63      [13] 1508 	ld	a,(#_g_wavecooldown + 0)
   4921 B7            [ 4] 1509 	or	a, a
   4922 20 14         [12] 1510 	jr	NZ,00157$
                           1511 ;src/game.c:261: spawn_wave(g_currentwave);
   4924 3A F8 63      [13] 1512 	ld	a, (_g_currentwave)
   4927 F5            [11] 1513 	push	af
   4928 33            [ 6] 1514 	inc	sp
   4929 CD A6 40      [17] 1515 	call	_spawn_wave
   492C 33            [ 6] 1516 	inc	sp
                           1517 ;src/game.c:262: g_currentwave++;
   492D 21 F8 63      [10] 1518 	ld	hl, #_g_currentwave+0
   4930 34            [11] 1519 	inc	(hl)
                           1520 ;src/game.c:263: g_wavecooldown = 90;
   4931 21 FA 63      [10] 1521 	ld	hl,#_g_wavecooldown + 0
   4934 36 5A         [10] 1522 	ld	(hl), #0x5a
   4936 18 18         [12] 1523 	jr	00165$
   4938                    1524 00157$:
                           1525 ;src/game.c:265: g_wavecooldown--;
   4938 21 FA 63      [10] 1526 	ld	hl, #_g_wavecooldown+0
   493B 35            [11] 1527 	dec	(hl)
   493C 18 12         [12] 1528 	jr	00165$
   493E                    1529 00162$:
                           1530 ;src/game.c:267: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   493E 21 71 63      [10] 1531 	ld	hl, #_g_player + 0
   4941 4E            [ 7] 1532 	ld	c, (hl)
   4942 C5            [11] 1533 	push	bc
   4943 CD AB 52      [17] 1534 	call	_tilemap_goal_x
   4946 C1            [10] 1535 	pop	bc
   4947 2D            [ 4] 1536 	dec	l
   4948 2D            [ 4] 1537 	dec	l
   4949 79            [ 4] 1538 	ld	a, c
   494A 95            [ 4] 1539 	sub	a, l
   494B 38 03         [12] 1540 	jr	C,00165$
                           1541 ;src/game.c:268: spawn_boss();
   494D CD A6 41      [17] 1542 	call	_spawn_boss
   4950                    1543 00165$:
                           1544 ;src/game.c:272: g_framecounter++;
   4950 FD 21 FF 63   [14] 1545 	ld	iy, #_g_framecounter
   4954 FD 34 00      [23] 1546 	inc	0 (iy)
   4957 20 03         [12] 1547 	jr	NZ,00381$
   4959 FD 34 01      [23] 1548 	inc	1 (iy)
   495C                    1549 00381$:
                           1550 ;src/game.c:273: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   495C 21 32 00      [10] 1551 	ld	hl, #0x0032
   495F E5            [11] 1552 	push	hl
   4960 2A FF 63      [16] 1553 	ld	hl, (_g_framecounter)
   4963 E5            [11] 1554 	push	hl
   4964 CD 23 62      [17] 1555 	call	__moduint
   4967 F1            [10] 1556 	pop	af
   4968 F1            [10] 1557 	pop	af
   4969 7C            [ 4] 1558 	ld	a, h
   496A B5            [ 4] 1559 	or	a,l
   496B 20 0D         [12] 1560 	jr	NZ,00169$
   496D FD 21 F6 63   [14] 1561 	ld	iy, #_g_timeleft
   4971 FD 7E 00      [19] 1562 	ld	a, 0 (iy)
   4974 B7            [ 4] 1563 	or	a, a
   4975 28 03         [12] 1564 	jr	Z,00169$
                           1565 ;src/game.c:274: g_timeleft--;
   4977 FD 35 00      [23] 1566 	dec	0 (iy)
   497A                    1567 00169$:
                           1568 ;src/game.c:276: if (g_timeleft == 0 && !g_victory) {
   497A 3A F6 63      [13] 1569 	ld	a,(#_g_timeleft + 0)
   497D B7            [ 4] 1570 	or	a, a
   497E 20 0B         [12] 1571 	jr	NZ,00172$
   4980 3A FD 63      [13] 1572 	ld	a,(#_g_victory + 0)
   4983 B7            [ 4] 1573 	or	a, a
   4984 20 05         [12] 1574 	jr	NZ,00172$
                           1575 ;src/game.c:277: g_gameover = 1;
   4986 21 FE 63      [10] 1576 	ld	hl,#_g_gameover + 0
   4989 36 01         [10] 1577 	ld	(hl), #0x01
   498B                    1578 00172$:
                           1579 ;src/game.c:280: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   498B 3A F7 63      [13] 1580 	ld	a, (_g_weapondisplay)
   498E F5            [11] 1581 	push	af
   498F 33            [ 6] 1582 	inc	sp
   4990 3A F6 63      [13] 1583 	ld	a, (_g_timeleft)
   4993 F5            [11] 1584 	push	af
   4994 33            [ 6] 1585 	inc	sp
   4995 2A F4 63      [16] 1586 	ld	hl, (_g_score)
   4998 E5            [11] 1587 	push	hl
   4999 3A F3 63      [13] 1588 	ld	a, (_g_lives)
   499C F5            [11] 1589 	push	af
   499D 33            [ 6] 1590 	inc	sp
   499E CD A5 4F      [17] 1591 	call	_hudupdate
   49A1 F1            [10] 1592 	pop	af
   49A2 F1            [10] 1593 	pop	af
   49A3 33            [ 6] 1594 	inc	sp
   49A4                    1595 00181$:
   49A4 DD F9         [10] 1596 	ld	sp, ix
   49A6 DD E1         [14] 1597 	pop	ix
   49A8 C9            [10] 1598 	ret
                           1599 ;src/game.c:283: void game_render(void) {
                           1600 ;	---------------------------------
                           1601 ; Function game_render
                           1602 ; ---------------------------------
   49A9                    1603 _game_render::
                           1604 ;src/game.c:286: cpct_clearScreen(0x00);
   49A9 21 00 40      [10] 1605 	ld	hl, #0x4000
   49AC E5            [11] 1606 	push	hl
   49AD AF            [ 4] 1607 	xor	a, a
   49AE F5            [11] 1608 	push	af
   49AF 33            [ 6] 1609 	inc	sp
   49B0 26 C0         [ 7] 1610 	ld	h, #0xc0
   49B2 E5            [11] 1611 	push	hl
   49B3 CD 6A 62      [17] 1612 	call	_cpct_memset
                           1613 ;src/game.c:287: tilemap_render();
   49B6 CD 66 51      [17] 1614 	call	_tilemap_render
                           1615 ;src/game.c:289: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49B9 0E 00         [ 7] 1616 	ld	c, #0x00
   49BB                    1617 00115$:
                           1618 ;src/game.c:290: projectilerender(&g_projectiles[i]);
   49BB 06 00         [ 7] 1619 	ld	b,#0x00
   49BD 69            [ 4] 1620 	ld	l, c
   49BE 60            [ 4] 1621 	ld	h, b
   49BF 29            [11] 1622 	add	hl, hl
   49C0 29            [11] 1623 	add	hl, hl
   49C1 09            [11] 1624 	add	hl, bc
   49C2 29            [11] 1625 	add	hl, hl
   49C3 11 B7 63      [10] 1626 	ld	de, #_g_projectiles
   49C6 19            [11] 1627 	add	hl, de
   49C7 C5            [11] 1628 	push	bc
   49C8 E5            [11] 1629 	push	hl
   49C9 CD 16 60      [17] 1630 	call	_projectilerender
   49CC F1            [10] 1631 	pop	af
   49CD C1            [10] 1632 	pop	bc
                           1633 ;src/game.c:289: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49CE 0C            [ 4] 1634 	inc	c
   49CF 79            [ 4] 1635 	ld	a, c
   49D0 D6 06         [ 7] 1636 	sub	a, #0x06
   49D2 38 E7         [12] 1637 	jr	C,00115$
                           1638 ;src/game.c:293: for (i = 0; i < MAX_ENEMIES; ++i) {
   49D4 0E 00         [ 7] 1639 	ld	c, #0x00
   49D6                    1640 00117$:
                           1641 ;src/game.c:294: enemyrender(&g_enemies[i]);
   49D6 06 00         [ 7] 1642 	ld	b,#0x00
   49D8 69            [ 4] 1643 	ld	l, c
   49D9 60            [ 4] 1644 	ld	h, b
   49DA 29            [11] 1645 	add	hl, hl
   49DB 29            [11] 1646 	add	hl, hl
   49DC 09            [11] 1647 	add	hl, bc
   49DD 29            [11] 1648 	add	hl, hl
   49DE 11 7B 63      [10] 1649 	ld	de, #_g_enemies
   49E1 19            [11] 1650 	add	hl, de
   49E2 C5            [11] 1651 	push	bc
   49E3 E5            [11] 1652 	push	hl
   49E4 CD C6 5A      [17] 1653 	call	_enemyrender
   49E7 F1            [10] 1654 	pop	af
   49E8 C1            [10] 1655 	pop	bc
                           1656 ;src/game.c:293: for (i = 0; i < MAX_ENEMIES; ++i) {
   49E9 0C            [ 4] 1657 	inc	c
   49EA 79            [ 4] 1658 	ld	a, c
   49EB D6 06         [ 7] 1659 	sub	a, #0x06
   49ED 38 E7         [12] 1660 	jr	C,00117$
                           1661 ;src/game.c:297: if (g_bossactive) {
   49EF 3A 0E 64      [13] 1662 	ld	a,(#_g_bossactive + 0)
   49F2 B7            [ 4] 1663 	or	a, a
   49F3 28 58         [12] 1664 	jr	Z,00104$
                           1665 ;src/game.c:298: enemyrender(&g_boss);
   49F5 21 04 64      [10] 1666 	ld	hl, #_g_boss
   49F8 E5            [11] 1667 	push	hl
   49F9 CD C6 5A      [17] 1668 	call	_enemyrender
                           1669 ;src/game.c:299: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(1, 1), 32, 2);
   49FC 21 01 01      [10] 1670 	ld	hl, #0x0101
   49FF E3            [19] 1671 	ex	(sp),hl
   4A00 CD 4E 62      [17] 1672 	call	_cpct_px2byteM0
   4A03 55            [ 4] 1673 	ld	d, l
   4A04 D5            [11] 1674 	push	de
   4A05 21 18 0A      [10] 1675 	ld	hl, #0x0a18
   4A08 E5            [11] 1676 	push	hl
   4A09 21 00 C0      [10] 1677 	ld	hl, #0xc000
   4A0C E5            [11] 1678 	push	hl
   4A0D CD 41 63      [17] 1679 	call	_cpct_getScreenPtr
   4A10 4D            [ 4] 1680 	ld	c, l
   4A11 44            [ 4] 1681 	ld	b, h
   4A12 D1            [10] 1682 	pop	de
   4A13 21 20 02      [10] 1683 	ld	hl, #0x0220
   4A16 E5            [11] 1684 	push	hl
   4A17 D5            [11] 1685 	push	de
   4A18 33            [ 6] 1686 	inc	sp
   4A19 C5            [11] 1687 	push	bc
   4A1A CD 88 62      [17] 1688 	call	_cpct_drawSolidBox
   4A1D F1            [10] 1689 	pop	af
   4A1E F1            [10] 1690 	pop	af
   4A1F 33            [ 6] 1691 	inc	sp
                           1692 ;src/game.c:300: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
   4A20 3A 0B 64      [13] 1693 	ld	a, (#_g_boss + 7)
   4A23 4F            [ 4] 1694 	ld	c, a
   4A24 87            [ 4] 1695 	add	a, a
   4A25 81            [ 4] 1696 	add	a, c
   4A26 57            [ 4] 1697 	ld	d, a
   4A27 D5            [11] 1698 	push	de
   4A28 21 05 05      [10] 1699 	ld	hl, #0x0505
   4A2B E5            [11] 1700 	push	hl
   4A2C CD 4E 62      [17] 1701 	call	_cpct_px2byteM0
   4A2F 5D            [ 4] 1702 	ld	e, l
   4A30 F1            [10] 1703 	pop	af
   4A31 57            [ 4] 1704 	ld	d, a
   4A32 D5            [11] 1705 	push	de
   4A33 21 18 0A      [10] 1706 	ld	hl, #0x0a18
   4A36 E5            [11] 1707 	push	hl
   4A37 21 00 C0      [10] 1708 	ld	hl, #0xc000
   4A3A E5            [11] 1709 	push	hl
   4A3B CD 41 63      [17] 1710 	call	_cpct_getScreenPtr
   4A3E 4D            [ 4] 1711 	ld	c, l
   4A3F 44            [ 4] 1712 	ld	b, h
   4A40 D1            [10] 1713 	pop	de
   4A41 3E 02         [ 7] 1714 	ld	a, #0x02
   4A43 F5            [11] 1715 	push	af
   4A44 33            [ 6] 1716 	inc	sp
   4A45 D5            [11] 1717 	push	de
   4A46 C5            [11] 1718 	push	bc
   4A47 CD 88 62      [17] 1719 	call	_cpct_drawSolidBox
   4A4A F1            [10] 1720 	pop	af
   4A4B F1            [10] 1721 	pop	af
   4A4C 33            [ 6] 1722 	inc	sp
   4A4D                    1723 00104$:
                           1724 ;src/game.c:303: if (!g_pickuptaken) {
   4A4D 3A 11 64      [13] 1725 	ld	a,(#_g_pickuptaken + 0)
   4A50 B7            [ 4] 1726 	or	a, a
   4A51 20 2F         [12] 1727 	jr	NZ,00106$
                           1728 ;src/game.c:304: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
   4A53 21 07 07      [10] 1729 	ld	hl, #0x0707
   4A56 E5            [11] 1730 	push	hl
   4A57 CD 4E 62      [17] 1731 	call	_cpct_px2byteM0
   4A5A 55            [ 4] 1732 	ld	d, l
   4A5B D5            [11] 1733 	push	de
   4A5C CD 07 52      [17] 1734 	call	_tilemap_ground_y
   4A5F D1            [10] 1735 	pop	de
   4A60 7D            [ 4] 1736 	ld	a, l
   4A61 C6 F8         [ 7] 1737 	add	a, #0xf8
   4A63 47            [ 4] 1738 	ld	b, a
   4A64 D5            [11] 1739 	push	de
   4A65 C5            [11] 1740 	push	bc
   4A66 33            [ 6] 1741 	inc	sp
   4A67 3E 24         [ 7] 1742 	ld	a, #0x24
   4A69 F5            [11] 1743 	push	af
   4A6A 33            [ 6] 1744 	inc	sp
   4A6B 21 00 C0      [10] 1745 	ld	hl, #0xc000
   4A6E E5            [11] 1746 	push	hl
   4A6F CD 41 63      [17] 1747 	call	_cpct_getScreenPtr
   4A72 4D            [ 4] 1748 	ld	c, l
   4A73 44            [ 4] 1749 	ld	b, h
   4A74 D1            [10] 1750 	pop	de
   4A75 21 04 04      [10] 1751 	ld	hl, #0x0404
   4A78 E5            [11] 1752 	push	hl
   4A79 D5            [11] 1753 	push	de
   4A7A 33            [ 6] 1754 	inc	sp
   4A7B C5            [11] 1755 	push	bc
   4A7C CD 88 62      [17] 1756 	call	_cpct_drawSolidBox
   4A7F F1            [10] 1757 	pop	af
   4A80 F1            [10] 1758 	pop	af
   4A81 33            [ 6] 1759 	inc	sp
   4A82                    1760 00106$:
                           1761 ;src/game.c:306: playerrender(&g_player);
   4A82 21 71 63      [10] 1762 	ld	hl, #_g_player
   4A85 E5            [11] 1763 	push	hl
   4A86 CD 2A 5E      [17] 1764 	call	_playerrender
   4A89 F1            [10] 1765 	pop	af
                           1766 ;src/game.c:307: hudrender();
   4A8A CD D6 4F      [17] 1767 	call	_hudrender
                           1768 ;src/game.c:309: if (g_victory) {
   4A8D 3A FD 63      [13] 1769 	ld	a,(#_g_victory + 0)
   4A90 B7            [ 4] 1770 	or	a, a
   4A91 28 48         [12] 1771 	jr	Z,00113$
                           1772 ;src/game.c:310: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
   4A93 21 08 08      [10] 1773 	ld	hl, #0x0808
   4A96 E5            [11] 1774 	push	hl
   4A97 CD 4E 62      [17] 1775 	call	_cpct_px2byteM0
   4A9A 55            [ 4] 1776 	ld	d, l
   4A9B D5            [11] 1777 	push	de
   4A9C 21 18 44      [10] 1778 	ld	hl, #0x4418
   4A9F E5            [11] 1779 	push	hl
   4AA0 21 00 C0      [10] 1780 	ld	hl, #0xc000
   4AA3 E5            [11] 1781 	push	hl
   4AA4 CD 41 63      [17] 1782 	call	_cpct_getScreenPtr
   4AA7 4D            [ 4] 1783 	ld	c, l
   4AA8 44            [ 4] 1784 	ld	b, h
   4AA9 D1            [10] 1785 	pop	de
   4AAA 21 20 0C      [10] 1786 	ld	hl, #0x0c20
   4AAD E5            [11] 1787 	push	hl
   4AAE D5            [11] 1788 	push	de
   4AAF 33            [ 6] 1789 	inc	sp
   4AB0 C5            [11] 1790 	push	bc
   4AB1 CD 88 62      [17] 1791 	call	_cpct_drawSolidBox
   4AB4 F1            [10] 1792 	pop	af
                           1793 ;src/game.c:311: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(5, 5), 24, 8);
   4AB5 33            [ 6] 1794 	inc	sp
   4AB6 21 05 05      [10] 1795 	ld	hl,#0x0505
   4AB9 E3            [19] 1796 	ex	(sp),hl
   4ABA CD 4E 62      [17] 1797 	call	_cpct_px2byteM0
   4ABD 55            [ 4] 1798 	ld	d, l
   4ABE D5            [11] 1799 	push	de
   4ABF 21 1C 48      [10] 1800 	ld	hl, #0x481c
   4AC2 E5            [11] 1801 	push	hl
   4AC3 21 00 C0      [10] 1802 	ld	hl, #0xc000
   4AC6 E5            [11] 1803 	push	hl
   4AC7 CD 41 63      [17] 1804 	call	_cpct_getScreenPtr
   4ACA 4D            [ 4] 1805 	ld	c, l
   4ACB 44            [ 4] 1806 	ld	b, h
   4ACC D1            [10] 1807 	pop	de
   4ACD 21 18 08      [10] 1808 	ld	hl, #0x0818
   4AD0 E5            [11] 1809 	push	hl
   4AD1 D5            [11] 1810 	push	de
   4AD2 33            [ 6] 1811 	inc	sp
   4AD3 C5            [11] 1812 	push	bc
   4AD4 CD 88 62      [17] 1813 	call	_cpct_drawSolidBox
   4AD7 F1            [10] 1814 	pop	af
   4AD8 F1            [10] 1815 	pop	af
   4AD9 33            [ 6] 1816 	inc	sp
   4ADA C9            [10] 1817 	ret
   4ADB                    1818 00113$:
                           1819 ;src/game.c:312: } else if (g_gameover) {
   4ADB 3A FE 63      [13] 1820 	ld	a,(#_g_gameover + 0)
   4ADE B7            [ 4] 1821 	or	a, a
   4ADF 28 48         [12] 1822 	jr	Z,00110$
                           1823 ;src/game.c:313: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
   4AE1 21 01 01      [10] 1824 	ld	hl, #0x0101
   4AE4 E5            [11] 1825 	push	hl
   4AE5 CD 4E 62      [17] 1826 	call	_cpct_px2byteM0
   4AE8 55            [ 4] 1827 	ld	d, l
   4AE9 D5            [11] 1828 	push	de
   4AEA 21 18 44      [10] 1829 	ld	hl, #0x4418
   4AED E5            [11] 1830 	push	hl
   4AEE 21 00 C0      [10] 1831 	ld	hl, #0xc000
   4AF1 E5            [11] 1832 	push	hl
   4AF2 CD 41 63      [17] 1833 	call	_cpct_getScreenPtr
   4AF5 4D            [ 4] 1834 	ld	c, l
   4AF6 44            [ 4] 1835 	ld	b, h
   4AF7 D1            [10] 1836 	pop	de
   4AF8 21 20 0C      [10] 1837 	ld	hl, #0x0c20
   4AFB E5            [11] 1838 	push	hl
   4AFC D5            [11] 1839 	push	de
   4AFD 33            [ 6] 1840 	inc	sp
   4AFE C5            [11] 1841 	push	bc
   4AFF CD 88 62      [17] 1842 	call	_cpct_drawSolidBox
   4B02 F1            [10] 1843 	pop	af
                           1844 ;src/game.c:314: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(6, 6), 24, 8);
   4B03 33            [ 6] 1845 	inc	sp
   4B04 21 06 06      [10] 1846 	ld	hl,#0x0606
   4B07 E3            [19] 1847 	ex	(sp),hl
   4B08 CD 4E 62      [17] 1848 	call	_cpct_px2byteM0
   4B0B 55            [ 4] 1849 	ld	d, l
   4B0C D5            [11] 1850 	push	de
   4B0D 21 1C 48      [10] 1851 	ld	hl, #0x481c
   4B10 E5            [11] 1852 	push	hl
   4B11 21 00 C0      [10] 1853 	ld	hl, #0xc000
   4B14 E5            [11] 1854 	push	hl
   4B15 CD 41 63      [17] 1855 	call	_cpct_getScreenPtr
   4B18 4D            [ 4] 1856 	ld	c, l
   4B19 44            [ 4] 1857 	ld	b, h
   4B1A D1            [10] 1858 	pop	de
   4B1B 21 18 08      [10] 1859 	ld	hl, #0x0818
   4B1E E5            [11] 1860 	push	hl
   4B1F D5            [11] 1861 	push	de
   4B20 33            [ 6] 1862 	inc	sp
   4B21 C5            [11] 1863 	push	bc
   4B22 CD 88 62      [17] 1864 	call	_cpct_drawSolidBox
   4B25 F1            [10] 1865 	pop	af
   4B26 F1            [10] 1866 	pop	af
   4B27 33            [ 6] 1867 	inc	sp
   4B28 C9            [10] 1868 	ret
   4B29                    1869 00110$:
                           1870 ;src/game.c:315: } else if (g_checkpointactive) {
   4B29 3A 03 64      [13] 1871 	ld	a,(#_g_checkpointactive + 0)
   4B2C B7            [ 4] 1872 	or	a, a
   4B2D C8            [11] 1873 	ret	Z
                           1874 ;src/game.c:316: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
   4B2E 21 09 09      [10] 1875 	ld	hl, #0x0909
   4B31 E5            [11] 1876 	push	hl
   4B32 CD 4E 62      [17] 1877 	call	_cpct_px2byteM0
   4B35 55            [ 4] 1878 	ld	d, l
   4B36 3A 02 64      [13] 1879 	ld	a,(#_g_checkpointy + 0)
   4B39 C6 F8         [ 7] 1880 	add	a, #0xf8
   4B3B 47            [ 4] 1881 	ld	b, a
   4B3C D5            [11] 1882 	push	de
   4B3D C5            [11] 1883 	push	bc
   4B3E 33            [ 6] 1884 	inc	sp
   4B3F 3A 01 64      [13] 1885 	ld	a, (_g_checkpointx)
   4B42 F5            [11] 1886 	push	af
   4B43 33            [ 6] 1887 	inc	sp
   4B44 21 00 C0      [10] 1888 	ld	hl, #0xc000
   4B47 E5            [11] 1889 	push	hl
   4B48 CD 41 63      [17] 1890 	call	_cpct_getScreenPtr
   4B4B 4D            [ 4] 1891 	ld	c, l
   4B4C 44            [ 4] 1892 	ld	b, h
   4B4D D1            [10] 1893 	pop	de
   4B4E 21 02 08      [10] 1894 	ld	hl, #0x0802
   4B51 E5            [11] 1895 	push	hl
   4B52 D5            [11] 1896 	push	de
   4B53 33            [ 6] 1897 	inc	sp
   4B54 C5            [11] 1898 	push	bc
   4B55 CD 88 62      [17] 1899 	call	_cpct_drawSolidBox
   4B58 F1            [10] 1900 	pop	af
   4B59 F1            [10] 1901 	pop	af
   4B5A 33            [ 6] 1902 	inc	sp
   4B5B C9            [10] 1903 	ret
                           1904 	.area _CODE
                           1905 	.area _INITIALIZER
                           1906 	.area _CABS (ABS)
