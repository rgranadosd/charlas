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
   61FB                      52 _g_player:
   61FB                      53 	.ds 9
   6204                      54 _g_enemies:
   6204                      55 	.ds 66
   6246                      56 _g_projectiles:
   6246                      57 	.ds 60
   6282                      58 _g_lives:
   6282                      59 	.ds 1
   6283                      60 _g_score:
   6283                      61 	.ds 2
   6285                      62 _g_timeleft:
   6285                      63 	.ds 1
   6286                      64 _g_weapondisplay:
   6286                      65 	.ds 1
   6287                      66 _g_currentwave:
   6287                      67 	.ds 1
   6288                      68 _g_aliveenemies:
   6288                      69 	.ds 1
   6289                      70 _g_wavecooldown:
   6289                      71 	.ds 1
   628A                      72 _g_damagecooldown:
   628A                      73 	.ds 1
   628B                      74 _g_shootcooldown:
   628B                      75 	.ds 1
   628C                      76 _g_victory:
   628C                      77 	.ds 1
   628D                      78 _g_gameover:
   628D                      79 	.ds 1
   628E                      80 _g_framecounter:
   628E                      81 	.ds 2
   6290                      82 _g_checkpointx:
   6290                      83 	.ds 1
   6291                      84 _g_checkpointy:
   6291                      85 	.ds 1
   6292                      86 _g_checkpointactive:
   6292                      87 	.ds 1
   6293                      88 _g_boss:
   6293                      89 	.ds 11
   629E                      90 _g_bossactive:
   629E                      91 	.ds 1
   629F                      92 _g_bossphase:
   629F                      93 	.ds 1
   62A0                      94 _g_weaponlevel:
   62A0                      95 	.ds 1
   62A1                      96 _g_pickuptaken:
   62A1                      97 	.ds 1
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
   4000 21 FB 61      [10]  128 	ld	hl, #_g_player
   4003 3A 90 62      [13]  129 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  130 	ld	(hl), a
                            131 ;src/game.c:43: g_player.y = g_checkpointy;
   4007 21 FC 61      [10]  132 	ld	hl, #(_g_player + 0x0001)
   400A 3A 91 62      [13]  133 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  134 	ld	(hl), a
                            135 ;src/game.c:44: g_player.vx = 0;
   400E 21 FD 61      [10]  136 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  137 	ld	(hl), #0x00
                            138 ;src/game.c:45: g_player.vy = 0;
   4013 21 FE 61      [10]  139 	ld	hl, #(_g_player + 0x0003)
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
   40B1 01 04 62      [10]  235 	ld	bc, #_g_enemies+0
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
   40BF 19            [11]  247 	add	hl, de
   40C0 D1            [10]  248 	pop	de
   40C1 09            [11]  249 	add	hl, bc
   40C2 C5            [11]  250 	push	bc
   40C3 D5            [11]  251 	push	de
   40C4 E5            [11]  252 	push	hl
   40C5 CD 4A 55      [17]  253 	call	_enemyinit
   40C8 F1            [10]  254 	pop	af
   40C9 D1            [10]  255 	pop	de
   40CA C1            [10]  256 	pop	bc
                            257 ;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
   40CB 1C            [ 4]  258 	inc	e
   40CC 7B            [ 4]  259 	ld	a, e
   40CD D6 06         [ 7]  260 	sub	a, #0x06
   40CF 38 E5         [12]  261 	jr	C,00117$
                            262 ;src/game.c:65: else if (wave == 1) count = 3;
   40D1 DD 7E 04      [19]  263 	ld	a, 4 (ix)
   40D4 3D            [ 4]  264 	dec	a
   40D5 20 04         [12]  265 	jr	NZ,00190$
   40D7 3E 01         [ 7]  266 	ld	a,#0x01
   40D9 18 01         [12]  267 	jr	00191$
   40DB                     268 00190$:
   40DB AF            [ 4]  269 	xor	a,a
   40DC                     270 00191$:
   40DC 5F            [ 4]  271 	ld	e, a
                            272 ;src/game.c:64: if (wave == 0) count = 2;
   40DD DD 7E 04      [19]  273 	ld	a, 4 (ix)
   40E0 B7            [ 4]  274 	or	a, a
   40E1 20 06         [12]  275 	jr	NZ,00106$
   40E3 DD 36 FB 02   [19]  276 	ld	-5 (ix), #0x02
   40E7 18 0E         [12]  277 	jr	00107$
   40E9                     278 00106$:
                            279 ;src/game.c:65: else if (wave == 1) count = 3;
   40E9 7B            [ 4]  280 	ld	a, e
   40EA B7            [ 4]  281 	or	a, a
   40EB 28 06         [12]  282 	jr	Z,00103$
   40ED DD 36 FB 03   [19]  283 	ld	-5 (ix), #0x03
   40F1 18 04         [12]  284 	jr	00107$
   40F3                     285 00103$:
                            286 ;src/game.c:66: else count = 4;
   40F3 DD 36 FB 04   [19]  287 	ld	-5 (ix), #0x04
   40F7                     288 00107$:
                            289 ;src/game.c:68: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F7 3E 06         [ 7]  290 	ld	a, #0x06
   40F9 DD 96 FB      [19]  291 	sub	a, -5 (ix)
   40FC 30 04         [12]  292 	jr	NC,00148$
   40FE DD 36 FB 06   [19]  293 	ld	-5 (ix), #0x06
                            294 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4102                     295 00148$:
   4102 DD 73 FF      [19]  296 	ld	-1 (ix), e
   4105 DD 36 FC 00   [19]  297 	ld	-4 (ix), #0x00
   4109                     298 00120$:
   4109 DD 7E FC      [19]  299 	ld	a, -4 (ix)
   410C DD 96 FB      [19]  300 	sub	a, -5 (ix)
   410F D2 9D 41      [10]  301 	jp	NC, 00116$
                            302 ;src/game.c:73: if (wave == 0) type = 0;
   4112 DD 7E 04      [19]  303 	ld	a, 4 (ix)
   4115 B7            [ 4]  304 	or	a,a
   4116 20 03         [12]  305 	jr	NZ,00114$
   4118 5F            [ 4]  306 	ld	e,a
   4119 18 27         [12]  307 	jr	00115$
   411B                     308 00114$:
                            309 ;src/game.c:74: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
   411B DD 7E FF      [19]  310 	ld	a, -1 (ix)
   411E B7            [ 4]  311 	or	a, a
   411F 28 0E         [12]  312 	jr	Z,00111$
   4121 DD 7E FC      [19]  313 	ld	a, -4 (ix)
   4124 B7            [ 4]  314 	or	a, a
   4125 20 04         [12]  315 	jr	NZ,00124$
   4127 1E 01         [ 7]  316 	ld	e, #0x01
   4129 18 17         [12]  317 	jr	00115$
   412B                     318 00124$:
   412B 1E 00         [ 7]  319 	ld	e, #0x00
   412D 18 13         [12]  320 	jr	00115$
   412F                     321 00111$:
                            322 ;src/game.c:75: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   412F DD 7E FC      [19]  323 	ld	a, -4 (ix)
   4132 B7            [ 4]  324 	or	a, a
   4133 28 07         [12]  325 	jr	Z,00129$
   4135 DD 7E FC      [19]  326 	ld	a, -4 (ix)
   4138 D6 03         [ 7]  327 	sub	a, #0x03
   413A 20 04         [12]  328 	jr	NZ,00126$
   413C                     329 00129$:
   413C 1E 02         [ 7]  330 	ld	e, #0x02
   413E 18 02         [12]  331 	jr	00127$
   4140                     332 00126$:
   4140 1E 01         [ 7]  333 	ld	e, #0x01
   4142                     334 00127$:
   4142                     335 00115$:
                            336 ;src/game.c:77: spawn_y = (type == 2) ? 84 : 112;
   4142 7B            [ 4]  337 	ld	a, e
   4143 D6 02         [ 7]  338 	sub	a, #0x02
   4145 20 04         [12]  339 	jr	NZ,00131$
   4147 16 54         [ 7]  340 	ld	d, #0x54
   4149 18 02         [12]  341 	jr	00132$
   414B                     342 00131$:
   414B 16 70         [ 7]  343 	ld	d, #0x70
   414D                     344 00132$:
                            345 ;src/game.c:78: enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));
   414D DD CB FC 46   [20]  346 	bit	0, -4 (ix)
   4151 28 06         [12]  347 	jr	Z,00133$
   4153 DD 36 FE 01   [19]  348 	ld	-2 (ix), #0x01
   4157 18 04         [12]  349 	jr	00134$
   4159                     350 00133$:
   4159 DD 36 FE 00   [19]  351 	ld	-2 (ix), #0x00
   415D                     352 00134$:
   415D DD 7E FC      [19]  353 	ld	a, -4 (ix)
   4160 07            [ 4]  354 	rlca
   4161 07            [ 4]  355 	rlca
   4162 07            [ 4]  356 	rlca
   4163 E6 F8         [ 7]  357 	and	a, #0xf8
   4165 C6 2E         [ 7]  358 	add	a, #0x2e
   4167 DD 77 FD      [19]  359 	ld	-3 (ix), a
   416A D5            [11]  360 	push	de
   416B DD 5E FC      [19]  361 	ld	e,-4 (ix)
   416E 16 00         [ 7]  362 	ld	d,#0x00
   4170 6B            [ 4]  363 	ld	l, e
   4171 62            [ 4]  364 	ld	h, d
   4172 29            [11]  365 	add	hl, hl
   4173 29            [11]  366 	add	hl, hl
   4174 19            [11]  367 	add	hl, de
   4175 29            [11]  368 	add	hl, hl
   4176 19            [11]  369 	add	hl, de
   4177 D1            [10]  370 	pop	de
   4178 09            [11]  371 	add	hl, bc
   4179 E5            [11]  372 	push	hl
   417A FD E1         [14]  373 	pop	iy
   417C C5            [11]  374 	push	bc
   417D DD 7E FE      [19]  375 	ld	a, -2 (ix)
   4180 F5            [11]  376 	push	af
   4181 33            [ 6]  377 	inc	sp
   4182 7B            [ 4]  378 	ld	a, e
   4183 F5            [11]  379 	push	af
   4184 33            [ 6]  380 	inc	sp
   4185 D5            [11]  381 	push	de
   4186 33            [ 6]  382 	inc	sp
   4187 DD 7E FD      [19]  383 	ld	a, -3 (ix)
   418A F5            [11]  384 	push	af
   418B 33            [ 6]  385 	inc	sp
   418C FD E5         [15]  386 	push	iy
   418E CD 92 55      [17]  387 	call	_enemyspawn
   4191 21 06 00      [10]  388 	ld	hl, #6
   4194 39            [11]  389 	add	hl, sp
   4195 F9            [ 6]  390 	ld	sp, hl
   4196 C1            [10]  391 	pop	bc
                            392 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4197 DD 34 FC      [23]  393 	inc	-4 (ix)
   419A C3 09 41      [10]  394 	jp	00120$
   419D                     395 00116$:
                            396 ;src/game.c:81: g_aliveenemies = count;
   419D DD 7E FB      [19]  397 	ld	a, -5 (ix)
   41A0 32 88 62      [13]  398 	ld	(#_g_aliveenemies + 0),a
   41A3 DD F9         [10]  399 	ld	sp, ix
   41A5 DD E1         [14]  400 	pop	ix
   41A7 C9            [10]  401 	ret
                            402 ;src/game.c:84: static void spawn_boss(void) {
                            403 ;	---------------------------------
                            404 ; Function spawn_boss
                            405 ; ---------------------------------
   41A8                     406 _spawn_boss:
                            407 ;src/game.c:85: enemyinit(&g_boss);
   41A8 21 93 62      [10]  408 	ld	hl, #_g_boss
   41AB E5            [11]  409 	push	hl
   41AC CD 4A 55      [17]  410 	call	_enemyinit
   41AF F1            [10]  411 	pop	af
                            412 ;src/game.c:86: enemyspawn(&g_boss, 68, 112, 1, 0);
   41B0 21 01 00      [10]  413 	ld	hl, #0x0001
   41B3 E5            [11]  414 	push	hl
   41B4 21 44 70      [10]  415 	ld	hl, #0x7044
   41B7 E5            [11]  416 	push	hl
   41B8 21 93 62      [10]  417 	ld	hl, #_g_boss
   41BB E5            [11]  418 	push	hl
   41BC CD 92 55      [17]  419 	call	_enemyspawn
   41BF 21 06 00      [10]  420 	ld	hl, #6
   41C2 39            [11]  421 	add	hl, sp
   41C3 F9            [ 6]  422 	ld	sp, hl
                            423 ;src/game.c:87: g_boss.w = 10;
   41C4 21 97 62      [10]  424 	ld	hl, #(_g_boss + 0x0004)
   41C7 36 0A         [10]  425 	ld	(hl), #0x0a
                            426 ;src/game.c:88: g_boss.h = 18;
   41C9 21 98 62      [10]  427 	ld	hl, #(_g_boss + 0x0005)
   41CC 36 12         [10]  428 	ld	(hl), #0x12
                            429 ;src/game.c:89: g_boss.health = 10;
   41CE 21 9A 62      [10]  430 	ld	hl, #(_g_boss + 0x0007)
   41D1 36 0A         [10]  431 	ld	(hl), #0x0a
                            432 ;src/game.c:90: g_boss.reward = 1500;
   41D3 21 DC 05      [10]  433 	ld	hl, #0x05dc
   41D6 22 9B 62      [16]  434 	ld	((_g_boss + 0x0008)), hl
                            435 ;src/game.c:91: g_boss.kind = 3;
   41D9 21 9D 62      [10]  436 	ld	hl, #(_g_boss + 0x000a)
   41DC 36 03         [10]  437 	ld	(hl), #0x03
                            438 ;src/game.c:92: g_boss.vx = -1;
   41DE 21 95 62      [10]  439 	ld	hl, #(_g_boss + 0x0002)
   41E1 36 FF         [10]  440 	ld	(hl), #0xff
                            441 ;src/game.c:93: g_bossactive = 1;
   41E3 21 9E 62      [10]  442 	ld	hl,#_g_bossactive + 0
   41E6 36 01         [10]  443 	ld	(hl), #0x01
                            444 ;src/game.c:94: g_bossphase = 0;
   41E8 21 9F 62      [10]  445 	ld	hl,#_g_bossphase + 0
   41EB 36 00         [10]  446 	ld	(hl), #0x00
   41ED C9            [10]  447 	ret
                            448 ;src/game.c:97: static void try_fire_projectile(void) {
                            449 ;	---------------------------------
                            450 ; Function try_fire_projectile
                            451 ; ---------------------------------
   41EE                     452 _try_fire_projectile:
   41EE DD E5         [15]  453 	push	ix
   41F0 DD 21 00 00   [14]  454 	ld	ix,#0
   41F4 DD 39         [15]  455 	add	ix,sp
   41F6 F5            [11]  456 	push	af
   41F7 3B            [ 6]  457 	dec	sp
                            458 ;src/game.c:101: if (!input_is_shoot_just_pressed()) return;
   41F8 CD 35 50      [17]  459 	call	_input_is_shoot_just_pressed
   41FB 7D            [ 4]  460 	ld	a, l
   41FC B7            [ 4]  461 	or	a, a
   41FD CA 8F 42      [10]  462 	jp	Z,00110$
                            463 ;src/game.c:102: if (g_shootcooldown) return;
   4200 3A 8B 62      [13]  464 	ld	a,(#_g_shootcooldown + 0)
   4203 B7            [ 4]  465 	or	a, a
   4204 C2 8F 42      [10]  466 	jp	NZ,00110$
                            467 ;src/game.c:104: dir = g_player.facing_left ? -3 : 3;
   4207 3A 02 62      [13]  468 	ld	a, (#_g_player + 7)
   420A B7            [ 4]  469 	or	a, a
   420B 28 04         [12]  470 	jr	Z,00112$
   420D 0E FD         [ 7]  471 	ld	c, #0xfd
   420F 18 02         [12]  472 	jr	00113$
   4211                     473 00112$:
   4211 0E 03         [ 7]  474 	ld	c, #0x03
   4213                     475 00113$:
                            476 ;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4213 DD 36 FF 00   [19]  477 	ld	-1 (ix), #0x00
   4217 06 00         [ 7]  478 	ld	b, #0x00
   4219                     479 00108$:
                            480 ;src/game.c:107: if (!g_projectiles[i].active) {
   4219 58            [ 4]  481 	ld	e,b
   421A 16 00         [ 7]  482 	ld	d,#0x00
   421C 6B            [ 4]  483 	ld	l, e
   421D 62            [ 4]  484 	ld	h, d
   421E 29            [11]  485 	add	hl, hl
   421F 29            [11]  486 	add	hl, hl
   4220 19            [11]  487 	add	hl, de
   4221 29            [11]  488 	add	hl, hl
   4222 11 46 62      [10]  489 	ld	de, #_g_projectiles
   4225 19            [11]  490 	add	hl, de
   4226 11 06 00      [10]  491 	ld	de, #0x0006
   4229 19            [11]  492 	add	hl, de
   422A 7E            [ 7]  493 	ld	a, (hl)
   422B B7            [ 4]  494 	or	a, a
   422C 20 58         [12]  495 	jr	NZ,00109$
                            496 ;src/game.c:109: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
   422E 3A A0 62      [13]  497 	ld	a,(#_g_weaponlevel + 0)
   4231 B7            [ 4]  498 	or	a, a
   4232 28 06         [12]  499 	jr	Z,00114$
   4234 DD 36 FE 01   [19]  500 	ld	-2 (ix), #0x01
   4238 18 04         [12]  501 	jr	00115$
   423A                     502 00114$:
   423A DD 36 FE 00   [19]  503 	ld	-2 (ix), #0x00
   423E                     504 00115$:
   423E 3A FC 61      [13]  505 	ld	a, (#_g_player + 1)
   4241 C6 06         [ 7]  506 	add	a, #0x06
   4243 DD 77 FD      [19]  507 	ld	-3 (ix), a
   4246 21 FB 61      [10]  508 	ld	hl, #_g_player + 0
   4249 46            [ 7]  509 	ld	b, (hl)
   424A 04            [ 4]  510 	inc	b
   424B 04            [ 4]  511 	inc	b
   424C DD 5E FF      [19]  512 	ld	e,-1 (ix)
   424F 16 00         [ 7]  513 	ld	d,#0x00
   4251 6B            [ 4]  514 	ld	l, e
   4252 62            [ 4]  515 	ld	h, d
   4253 29            [11]  516 	add	hl, hl
   4254 29            [11]  517 	add	hl, hl
   4255 19            [11]  518 	add	hl, de
   4256 29            [11]  519 	add	hl, hl
   4257 11 46 62      [10]  520 	ld	de, #_g_projectiles
   425A 19            [11]  521 	add	hl, de
   425B EB            [ 4]  522 	ex	de,hl
   425C DD 7E FE      [19]  523 	ld	a, -2 (ix)
   425F F5            [11]  524 	push	af
   4260 33            [ 6]  525 	inc	sp
   4261 79            [ 4]  526 	ld	a, c
   4262 F5            [11]  527 	push	af
   4263 33            [ 6]  528 	inc	sp
   4264 DD 7E FD      [19]  529 	ld	a, -3 (ix)
   4267 F5            [11]  530 	push	af
   4268 33            [ 6]  531 	inc	sp
   4269 C5            [11]  532 	push	bc
   426A 33            [ 6]  533 	inc	sp
   426B D5            [11]  534 	push	de
   426C CD 7D 5D      [17]  535 	call	_projectilefire
   426F 21 06 00      [10]  536 	ld	hl, #6
   4272 39            [11]  537 	add	hl, sp
   4273 F9            [ 6]  538 	ld	sp, hl
                            539 ;src/game.c:110: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
   4274 3A A0 62      [13]  540 	ld	a,(#_g_weaponlevel + 0)
   4277 B7            [ 4]  541 	or	a, a
   4278 28 04         [12]  542 	jr	Z,00116$
   427A 0E 04         [ 7]  543 	ld	c, #0x04
   427C 18 02         [12]  544 	jr	00117$
   427E                     545 00116$:
   427E 0E 08         [ 7]  546 	ld	c, #0x08
   4280                     547 00117$:
   4280 21 8B 62      [10]  548 	ld	hl,#_g_shootcooldown + 0
   4283 71            [ 7]  549 	ld	(hl), c
                            550 ;src/game.c:111: break;
   4284 18 09         [12]  551 	jr	00110$
   4286                     552 00109$:
                            553 ;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4286 04            [ 4]  554 	inc	b
   4287 DD 70 FF      [19]  555 	ld	-1 (ix), b
   428A 78            [ 4]  556 	ld	a, b
   428B D6 06         [ 7]  557 	sub	a, #0x06
   428D 38 8A         [12]  558 	jr	C,00108$
   428F                     559 00110$:
   428F DD F9         [10]  560 	ld	sp, ix
   4291 DD E1         [14]  561 	pop	ix
   4293 C9            [10]  562 	ret
                            563 ;src/game.c:116: static void register_player_hit(void) {
                            564 ;	---------------------------------
                            565 ; Function register_player_hit
                            566 ; ---------------------------------
   4294                     567 _register_player_hit:
                            568 ;src/game.c:117: if (g_lives) {
   4294 FD 21 82 62   [14]  569 	ld	iy, #_g_lives
   4298 FD 7E 00      [19]  570 	ld	a, 0 (iy)
   429B B7            [ 4]  571 	or	a, a
   429C 28 03         [12]  572 	jr	Z,00102$
                            573 ;src/game.c:118: g_lives--;
   429E FD 35 00      [23]  574 	dec	0 (iy)
   42A1                     575 00102$:
                            576 ;src/game.c:120: if (g_lives == 0) {
   42A1 3A 82 62      [13]  577 	ld	a,(#_g_lives + 0)
   42A4 B7            [ 4]  578 	or	a, a
   42A5 20 06         [12]  579 	jr	NZ,00104$
                            580 ;src/game.c:121: g_gameover = 1;
   42A7 21 8D 62      [10]  581 	ld	hl,#_g_gameover + 0
   42AA 36 01         [10]  582 	ld	(hl), #0x01
                            583 ;src/game.c:122: return;
   42AC C9            [10]  584 	ret
   42AD                     585 00104$:
                            586 ;src/game.c:125: reset_player_to_checkpoint();
   42AD CD 00 40      [17]  587 	call	_reset_player_to_checkpoint
                            588 ;src/game.c:126: g_damagecooldown = 40;
   42B0 21 8A 62      [10]  589 	ld	hl,#_g_damagecooldown + 0
   42B3 36 28         [10]  590 	ld	(hl), #0x28
   42B5 C9            [10]  591 	ret
                            592 ;src/game.c:129: void game_init(void) {
                            593 ;	---------------------------------
                            594 ; Function game_init
                            595 ; ---------------------------------
   42B6                     596 _game_init::
                            597 ;src/game.c:132: cpct_disableFirmware();
   42B6 CD 02 61      [17]  598 	call	_cpct_disableFirmware
                            599 ;src/game.c:133: cpct_setVideoMode(0);
   42B9 2E 00         [ 7]  600 	ld	l, #0x00
   42BB CD CA 60      [17]  601 	call	_cpct_setVideoMode
                            602 ;src/game.c:134: cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
   42BE 21 10 00      [10]  603 	ld	hl, #0x0010
   42C1 E5            [11]  604 	push	hl
   42C2 21 E4 51      [10]  605 	ld	hl, #_gpalette
   42C5 E5            [11]  606 	push	hl
   42C6 CD D9 5F      [17]  607 	call	_cpct_setPalette
                            608 ;src/game.c:135: cpct_setBorder(gpalette[0]);
   42C9 21 E4 51      [10]  609 	ld	hl, #_gpalette + 0
   42CC 46            [ 7]  610 	ld	b, (hl)
   42CD C5            [11]  611 	push	bc
   42CE 33            [ 6]  612 	inc	sp
   42CF 3E 10         [ 7]  613 	ld	a, #0x10
   42D1 F5            [11]  614 	push	af
   42D2 33            [ 6]  615 	inc	sp
   42D3 CD F0 5F      [17]  616 	call	_cpct_setPALColour
                            617 ;src/game.c:136: cpct_clearScreen(0x00);
   42D6 21 00 40      [10]  618 	ld	hl, #0x4000
   42D9 E5            [11]  619 	push	hl
   42DA AF            [ 4]  620 	xor	a, a
   42DB F5            [11]  621 	push	af
   42DC 33            [ 6]  622 	inc	sp
   42DD 26 C0         [ 7]  623 	ld	h, #0xc0
   42DF E5            [11]  624 	push	hl
   42E0 CD F4 60      [17]  625 	call	_cpct_memset
                            626 ;src/game.c:137: tilemap_init();
   42E3 CD 47 50      [17]  627 	call	_tilemap_init
                            628 ;src/game.c:138: collision_init();
   42E6 CD 8B 4B      [17]  629 	call	_collision_init
                            630 ;src/game.c:139: playerinit(&g_player);
   42E9 21 FB 61      [10]  631 	ld	hl, #_g_player
   42EC E5            [11]  632 	push	hl
   42ED CD 54 5A      [17]  633 	call	_playerinit
   42F0 F1            [10]  634 	pop	af
                            635 ;src/game.c:140: hudinit();
   42F1 CD 97 4E      [17]  636 	call	_hudinit
                            637 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42F4 0E 00         [ 7]  638 	ld	c, #0x00
   42F6                     639 00102$:
                            640 ;src/game.c:143: projectileinit(&g_projectiles[i]);
   42F6 06 00         [ 7]  641 	ld	b,#0x00
   42F8 69            [ 4]  642 	ld	l, c
   42F9 60            [ 4]  643 	ld	h, b
   42FA 29            [11]  644 	add	hl, hl
   42FB 29            [11]  645 	add	hl, hl
   42FC 09            [11]  646 	add	hl, bc
   42FD 29            [11]  647 	add	hl, hl
   42FE 11 46 62      [10]  648 	ld	de, #_g_projectiles
   4301 19            [11]  649 	add	hl, de
   4302 C5            [11]  650 	push	bc
   4303 E5            [11]  651 	push	hl
   4304 CD 38 5D      [17]  652 	call	_projectileinit
   4307 F1            [10]  653 	pop	af
   4308 C1            [10]  654 	pop	bc
                            655 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4309 0C            [ 4]  656 	inc	c
   430A 79            [ 4]  657 	ld	a, c
   430B D6 06         [ 7]  658 	sub	a, #0x06
   430D 38 E7         [12]  659 	jr	C,00102$
                            660 ;src/game.c:146: g_lives = 3;
   430F 21 82 62      [10]  661 	ld	hl,#_g_lives + 0
   4312 36 03         [10]  662 	ld	(hl), #0x03
                            663 ;src/game.c:147: g_score = 0;
   4314 21 00 00      [10]  664 	ld	hl, #0x0000
   4317 22 83 62      [16]  665 	ld	(_g_score), hl
                            666 ;src/game.c:148: g_timeleft = 99;
   431A FD 21 85 62   [14]  667 	ld	iy, #_g_timeleft
   431E FD 36 00 63   [19]  668 	ld	0 (iy), #0x63
                            669 ;src/game.c:149: g_weapondisplay = 1;
   4322 FD 21 86 62   [14]  670 	ld	iy, #_g_weapondisplay
   4326 FD 36 00 01   [19]  671 	ld	0 (iy), #0x01
                            672 ;src/game.c:150: g_currentwave = 0;
   432A FD 21 87 62   [14]  673 	ld	iy, #_g_currentwave
   432E FD 36 00 00   [19]  674 	ld	0 (iy), #0x00
                            675 ;src/game.c:151: g_wavecooldown = 1;
   4332 FD 21 89 62   [14]  676 	ld	iy, #_g_wavecooldown
   4336 FD 36 00 01   [19]  677 	ld	0 (iy), #0x01
                            678 ;src/game.c:152: g_damagecooldown = 0;
   433A FD 21 8A 62   [14]  679 	ld	iy, #_g_damagecooldown
   433E FD 36 00 00   [19]  680 	ld	0 (iy), #0x00
                            681 ;src/game.c:153: g_shootcooldown = 0;
   4342 FD 21 8B 62   [14]  682 	ld	iy, #_g_shootcooldown
   4346 FD 36 00 00   [19]  683 	ld	0 (iy), #0x00
                            684 ;src/game.c:154: g_victory = 0;
   434A FD 21 8C 62   [14]  685 	ld	iy, #_g_victory
   434E FD 36 00 00   [19]  686 	ld	0 (iy), #0x00
                            687 ;src/game.c:155: g_gameover = 0;
   4352 FD 21 8D 62   [14]  688 	ld	iy, #_g_gameover
   4356 FD 36 00 00   [19]  689 	ld	0 (iy), #0x00
                            690 ;src/game.c:156: g_framecounter = 0;
   435A 2E 00         [ 7]  691 	ld	l, #0x00
   435C 22 8E 62      [16]  692 	ld	(_g_framecounter), hl
                            693 ;src/game.c:157: g_checkpointx = 20;
   435F 21 90 62      [10]  694 	ld	hl,#_g_checkpointx + 0
   4362 36 14         [10]  695 	ld	(hl), #0x14
                            696 ;src/game.c:158: g_checkpointy = 120;
   4364 21 91 62      [10]  697 	ld	hl,#_g_checkpointy + 0
   4367 36 78         [10]  698 	ld	(hl), #0x78
                            699 ;src/game.c:159: g_checkpointactive = 0;
   4369 21 92 62      [10]  700 	ld	hl,#_g_checkpointactive + 0
   436C 36 00         [10]  701 	ld	(hl), #0x00
                            702 ;src/game.c:160: g_bossactive = 0;
   436E 21 9E 62      [10]  703 	ld	hl,#_g_bossactive + 0
   4371 36 00         [10]  704 	ld	(hl), #0x00
                            705 ;src/game.c:161: g_weaponlevel = 0;
   4373 21 A0 62      [10]  706 	ld	hl,#_g_weaponlevel + 0
   4376 36 00         [10]  707 	ld	(hl), #0x00
                            708 ;src/game.c:162: g_pickuptaken = 0;
   4378 21 A1 62      [10]  709 	ld	hl,#_g_pickuptaken + 0
   437B 36 00         [10]  710 	ld	(hl), #0x00
                            711 ;src/game.c:163: enemyinit(&g_boss);
   437D 21 93 62      [10]  712 	ld	hl, #_g_boss
   4380 E5            [11]  713 	push	hl
   4381 CD 4A 55      [17]  714 	call	_enemyinit
   4384 F1            [10]  715 	pop	af
   4385 C9            [10]  716 	ret
                            717 ;src/game.c:166: void game_update(void) {
                            718 ;	---------------------------------
                            719 ; Function game_update
                            720 ; ---------------------------------
   4386                     721 _game_update::
   4386 DD E5         [15]  722 	push	ix
   4388 DD 21 00 00   [14]  723 	ld	ix,#0
   438C DD 39         [15]  724 	add	ix,sp
   438E 21 E7 FF      [10]  725 	ld	hl, #-25
   4391 39            [11]  726 	add	hl, sp
   4392 F9            [ 6]  727 	ld	sp, hl
                            728 ;src/game.c:170: input_update();
   4393 CD A2 4F      [17]  729 	call	_input_update
                            730 ;src/game.c:172: if (g_gameover || g_victory) {
   4396 3A 8D 62      [13]  731 	ld	a,(#_g_gameover + 0)
   4399 B7            [ 4]  732 	or	a, a
   439A 20 06         [12]  733 	jr	NZ,00101$
   439C 3A 8C 62      [13]  734 	ld	a,(#_g_victory + 0)
   439F B7            [ 4]  735 	or	a, a
   43A0 28 1C         [12]  736 	jr	Z,00102$
   43A2                     737 00101$:
                            738 ;src/game.c:173: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   43A2 3A 86 62      [13]  739 	ld	a, (_g_weapondisplay)
   43A5 F5            [11]  740 	push	af
   43A6 33            [ 6]  741 	inc	sp
   43A7 3A 85 62      [13]  742 	ld	a, (_g_timeleft)
   43AA F5            [11]  743 	push	af
   43AB 33            [ 6]  744 	inc	sp
   43AC 2A 83 62      [16]  745 	ld	hl, (_g_score)
   43AF E5            [11]  746 	push	hl
   43B0 3A 82 62      [13]  747 	ld	a, (_g_lives)
   43B3 F5            [11]  748 	push	af
   43B4 33            [ 6]  749 	inc	sp
   43B5 CD B2 4E      [17]  750 	call	_hudupdate
   43B8 F1            [10]  751 	pop	af
   43B9 F1            [10]  752 	pop	af
   43BA 33            [ 6]  753 	inc	sp
                            754 ;src/game.c:174: return;
   43BB C3 A9 49      [10]  755 	jp	00181$
   43BE                     756 00102$:
                            757 ;src/game.c:177: playerupdate(&g_player);
   43BE 21 FB 61      [10]  758 	ld	hl, #_g_player
   43C1 E5            [11]  759 	push	hl
   43C2 CD 94 5A      [17]  760 	call	_playerupdate
   43C5 F1            [10]  761 	pop	af
                            762 ;src/game.c:178: try_fire_projectile();
   43C6 CD EE 41      [17]  763 	call	_try_fire_projectile
                            764 ;src/game.c:180: if (g_shootcooldown) g_shootcooldown--;
   43C9 FD 21 8B 62   [14]  765 	ld	iy, #_g_shootcooldown
   43CD FD 7E 00      [19]  766 	ld	a, 0 (iy)
   43D0 B7            [ 4]  767 	or	a, a
   43D1 28 03         [12]  768 	jr	Z,00105$
   43D3 FD 35 00      [23]  769 	dec	0 (iy)
   43D6                     770 00105$:
                            771 ;src/game.c:181: if (g_damagecooldown) g_damagecooldown--;
   43D6 FD 21 8A 62   [14]  772 	ld	iy, #_g_damagecooldown
   43DA FD 7E 00      [19]  773 	ld	a, 0 (iy)
   43DD B7            [ 4]  774 	or	a, a
   43DE 28 03         [12]  775 	jr	Z,00192$
   43E0 FD 35 00      [23]  776 	dec	0 (iy)
                            777 ;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43E3                     778 00192$:
   43E3 0E 00         [ 7]  779 	ld	c, #0x00
   43E5                     780 00174$:
                            781 ;src/game.c:184: projectileupdate(&g_projectiles[i]);
   43E5 06 00         [ 7]  782 	ld	b,#0x00
   43E7 69            [ 4]  783 	ld	l, c
   43E8 60            [ 4]  784 	ld	h, b
   43E9 29            [11]  785 	add	hl, hl
   43EA 29            [11]  786 	add	hl, hl
   43EB 09            [11]  787 	add	hl, bc
   43EC 29            [11]  788 	add	hl, hl
   43ED 11 46 62      [10]  789 	ld	de, #_g_projectiles
   43F0 19            [11]  790 	add	hl, de
   43F1 C5            [11]  791 	push	bc
   43F2 E5            [11]  792 	push	hl
   43F3 CD 3B 5E      [17]  793 	call	_projectileupdate
   43F6 F1            [10]  794 	pop	af
   43F7 C1            [10]  795 	pop	bc
                            796 ;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43F8 0C            [ 4]  797 	inc	c
   43F9 79            [ 4]  798 	ld	a, c
   43FA D6 06         [ 7]  799 	sub	a, #0x06
   43FC 38 E7         [12]  800 	jr	C,00174$
                            801 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   43FE 0E 00         [ 7]  802 	ld	c, #0x00
   4400                     803 00176$:
                            804 ;src/game.c:188: enemyupdate(&g_enemies[i]);
   4400 06 00         [ 7]  805 	ld	b,#0x00
   4402 69            [ 4]  806 	ld	l, c
   4403 60            [ 4]  807 	ld	h, b
   4404 29            [11]  808 	add	hl, hl
   4405 29            [11]  809 	add	hl, hl
   4406 09            [11]  810 	add	hl, bc
   4407 29            [11]  811 	add	hl, hl
   4408 09            [11]  812 	add	hl, bc
   4409 11 04 62      [10]  813 	ld	de, #_g_enemies
   440C 19            [11]  814 	add	hl, de
   440D C5            [11]  815 	push	bc
   440E E5            [11]  816 	push	hl
   440F CD 76 57      [17]  817 	call	_enemyupdate
   4412 F1            [10]  818 	pop	af
   4413 C1            [10]  819 	pop	bc
                            820 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   4414 0C            [ 4]  821 	inc	c
   4415 79            [ 4]  822 	ld	a, c
   4416 D6 06         [ 7]  823 	sub	a, #0x06
   4418 38 E6         [12]  824 	jr	C,00176$
                            825 ;src/game.c:191: if (g_bossactive) {
   441A 3A 9E 62      [13]  826 	ld	a,(#_g_bossactive + 0)
   441D B7            [ 4]  827 	or	a, a
   441E 28 71         [12]  828 	jr	Z,00211$
                            829 ;src/game.c:192: if (g_boss.health > 4) g_bossphase = 0;
   4420 21 9A 62      [10]  830 	ld	hl, #_g_boss + 7
   4423 4E            [ 7]  831 	ld	c, (hl)
   4424 3E 04         [ 7]  832 	ld	a, #0x04
   4426 91            [ 4]  833 	sub	a, c
   4427 30 07         [12]  834 	jr	NC,00111$
   4429 21 9F 62      [10]  835 	ld	hl,#_g_bossphase + 0
   442C 36 00         [10]  836 	ld	(hl), #0x00
   442E 18 05         [12]  837 	jr	00112$
   4430                     838 00111$:
                            839 ;src/game.c:193: else g_bossphase = 1;
   4430 21 9F 62      [10]  840 	ld	hl,#_g_bossphase + 0
   4433 36 01         [10]  841 	ld	(hl), #0x01
   4435                     842 00112$:
                            843 ;src/game.c:195: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4435 3A FB 61      [13]  844 	ld	a,(#_g_player + 0)
   4438 DD 77 FF      [19]  845 	ld	-1 (ix), a
   443B DD 77 FD      [19]  846 	ld	-3 (ix), a
   443E DD 36 FE 00   [19]  847 	ld	-2 (ix), #0x00
   4442 DD 7E FD      [19]  848 	ld	a, -3 (ix)
   4445 C6 02         [ 7]  849 	add	a, #0x02
   4447 DD 77 FD      [19]  850 	ld	-3 (ix), a
   444A DD 7E FE      [19]  851 	ld	a, -2 (ix)
   444D CE 00         [ 7]  852 	adc	a, #0x00
   444F DD 77 FE      [19]  853 	ld	-2 (ix), a
   4452 21 93 62      [10]  854 	ld	hl, #_g_boss + 0
   4455 4E            [ 7]  855 	ld	c, (hl)
   4456 06 00         [ 7]  856 	ld	b, #0x00
   4458 DD 7E FD      [19]  857 	ld	a, -3 (ix)
   445B 91            [ 4]  858 	sub	a, c
   445C DD 7E FE      [19]  859 	ld	a, -2 (ix)
   445F 98            [ 4]  860 	sbc	a, b
   4460 E2 65 44      [10]  861 	jp	PO, 00380$
   4463 EE 80         [ 7]  862 	xor	a, #0x80
   4465                     863 00380$:
   4465 F2 79 44      [10]  864 	jp	P, 00183$
   4468 3A 9F 62      [13]  865 	ld	a,(#_g_bossphase + 0)
   446B B7            [ 4]  866 	or	a, a
   446C 28 04         [12]  867 	jr	Z,00185$
   446E 0E 02         [ 7]  868 	ld	c, #0x02
   4470 18 02         [12]  869 	jr	00186$
   4472                     870 00185$:
   4472 0E 01         [ 7]  871 	ld	c, #0x01
   4474                     872 00186$:
   4474 AF            [ 4]  873 	xor	a, a
   4475 91            [ 4]  874 	sub	a, c
   4476 4F            [ 4]  875 	ld	c, a
   4477 18 0C         [12]  876 	jr	00184$
   4479                     877 00183$:
   4479 3A 9F 62      [13]  878 	ld	a,(#_g_bossphase + 0)
   447C B7            [ 4]  879 	or	a, a
   447D 28 04         [12]  880 	jr	Z,00187$
   447F 0E 02         [ 7]  881 	ld	c, #0x02
   4481 18 02         [12]  882 	jr	00188$
   4483                     883 00187$:
   4483 0E 01         [ 7]  884 	ld	c, #0x01
   4485                     885 00188$:
   4485                     886 00184$:
   4485 21 95 62      [10]  887 	ld	hl, #(_g_boss + 0x0002)
   4488 71            [ 7]  888 	ld	(hl), c
                            889 ;src/game.c:196: enemyupdate(&g_boss);
   4489 21 93 62      [10]  890 	ld	hl, #_g_boss
   448C E5            [11]  891 	push	hl
   448D CD 76 57      [17]  892 	call	_enemyupdate
   4490 F1            [10]  893 	pop	af
                            894 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4491                     895 00211$:
   4491 0E 00         [ 7]  896 	ld	c, #0x00
   4493                     897 00179$:
                            898 ;src/game.c:200: if (!g_projectiles[i].active) continue;
   4493 06 00         [ 7]  899 	ld	b,#0x00
   4495 69            [ 4]  900 	ld	l, c
   4496 60            [ 4]  901 	ld	h, b
   4497 29            [11]  902 	add	hl, hl
   4498 29            [11]  903 	add	hl, hl
   4499 09            [11]  904 	add	hl, bc
   449A 29            [11]  905 	add	hl, hl
   449B EB            [ 4]  906 	ex	de,hl
   449C 21 46 62      [10]  907 	ld	hl, #_g_projectiles
   449F 19            [11]  908 	add	hl,de
   44A0 EB            [ 4]  909 	ex	de,hl
   44A1 21 06 00      [10]  910 	ld	hl, #0x0006
   44A4 19            [11]  911 	add	hl,de
   44A5 DD 75 FD      [19]  912 	ld	-3 (ix), l
   44A8 DD 74 FE      [19]  913 	ld	-2 (ix), h
   44AB 7E            [ 7]  914 	ld	a, (hl)
   44AC B7            [ 4]  915 	or	a, a
   44AD CA CE 46      [10]  916 	jp	Z, 00133$
                            917 ;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
   44B0 DD 36 E7 00   [19]  918 	ld	-25 (ix), #0x00
   44B4                     919 00178$:
                            920 ;src/game.c:202: if (!g_enemies[j].active) continue;
   44B4 D5            [11]  921 	push	de
   44B5 DD 5E E7      [19]  922 	ld	e,-25 (ix)
   44B8 16 00         [ 7]  923 	ld	d,#0x00
   44BA 6B            [ 4]  924 	ld	l, e
   44BB 62            [ 4]  925 	ld	h, d
   44BC 29            [11]  926 	add	hl, hl
   44BD 29            [11]  927 	add	hl, hl
   44BE 19            [11]  928 	add	hl, de
   44BF 29            [11]  929 	add	hl, hl
   44C0 19            [11]  930 	add	hl, de
   44C1 D1            [10]  931 	pop	de
   44C2 3E 04         [ 7]  932 	ld	a, #<(_g_enemies)
   44C4 85            [ 4]  933 	add	a, l
   44C5 DD 77 FB      [19]  934 	ld	-5 (ix), a
   44C8 3E 62         [ 7]  935 	ld	a, #>(_g_enemies)
   44CA 8C            [ 4]  936 	adc	a, h
   44CB DD 77 FC      [19]  937 	ld	-4 (ix), a
   44CE DD 6E FB      [19]  938 	ld	l,-5 (ix)
   44D1 DD 66 FC      [19]  939 	ld	h,-4 (ix)
   44D4 C5            [11]  940 	push	bc
   44D5 01 06 00      [10]  941 	ld	bc, #0x0006
   44D8 09            [11]  942 	add	hl, bc
   44D9 C1            [10]  943 	pop	bc
   44DA 46            [ 7]  944 	ld	b, (hl)
                            945 ;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   44DB 21 05 00      [10]  946 	ld	hl, #0x0005
   44DE 19            [11]  947 	add	hl,de
   44DF DD 75 F9      [19]  948 	ld	-7 (ix), l
   44E2 DD 74 FA      [19]  949 	ld	-6 (ix), h
   44E5 21 04 00      [10]  950 	ld	hl, #0x0004
   44E8 19            [11]  951 	add	hl,de
   44E9 DD 75 F7      [19]  952 	ld	-9 (ix), l
   44EC DD 74 F8      [19]  953 	ld	-8 (ix), h
   44EF 21 01 00      [10]  954 	ld	hl, #0x0001
   44F2 19            [11]  955 	add	hl,de
   44F3 DD 75 F5      [19]  956 	ld	-11 (ix), l
   44F6 DD 74 F6      [19]  957 	ld	-10 (ix), h
                            958 ;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44F9 21 07 00      [10]  959 	ld	hl, #0x0007
   44FC 19            [11]  960 	add	hl,de
   44FD DD 75 F3      [19]  961 	ld	-13 (ix), l
   4500 DD 74 F4      [19]  962 	ld	-12 (ix), h
                            963 ;src/game.c:202: if (!g_enemies[j].active) continue;
   4503 78            [ 4]  964 	ld	a, b
   4504 B7            [ 4]  965 	or	a, a
   4505 CA FE 45      [10]  966 	jp	Z, 00125$
                            967 ;src/game.c:204: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   4508 DD 6E FB      [19]  968 	ld	l,-5 (ix)
   450B DD 66 FC      [19]  969 	ld	h,-4 (ix)
   450E 23            [ 6]  970 	inc	hl
   450F 23            [ 6]  971 	inc	hl
   4510 23            [ 6]  972 	inc	hl
   4511 23            [ 6]  973 	inc	hl
   4512 23            [ 6]  974 	inc	hl
   4513 7E            [ 7]  975 	ld	a, (hl)
   4514 DD 77 FF      [19]  976 	ld	-1 (ix), a
   4517 DD 6E FB      [19]  977 	ld	l,-5 (ix)
   451A DD 66 FC      [19]  978 	ld	h,-4 (ix)
   451D 23            [ 6]  979 	inc	hl
   451E 23            [ 6]  980 	inc	hl
   451F 23            [ 6]  981 	inc	hl
   4520 23            [ 6]  982 	inc	hl
   4521 7E            [ 7]  983 	ld	a, (hl)
   4522 DD 77 F2      [19]  984 	ld	-14 (ix), a
   4525 DD 6E FB      [19]  985 	ld	l,-5 (ix)
   4528 DD 66 FC      [19]  986 	ld	h,-4 (ix)
   452B 23            [ 6]  987 	inc	hl
   452C 46            [ 7]  988 	ld	b, (hl)
   452D DD 70 F0      [19]  989 	ld	-16 (ix), b
   4530 DD 36 F1 00   [19]  990 	ld	-15 (ix), #0x00
   4534 DD 6E FB      [19]  991 	ld	l,-5 (ix)
   4537 DD 66 FC      [19]  992 	ld	h,-4 (ix)
   453A 46            [ 7]  993 	ld	b, (hl)
   453B DD 70 EE      [19]  994 	ld	-18 (ix), b
   453E DD 36 EF 00   [19]  995 	ld	-17 (ix), #0x00
                            996 ;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4542 DD 6E F9      [19]  997 	ld	l,-7 (ix)
   4545 DD 66 FA      [19]  998 	ld	h,-6 (ix)
   4548 7E            [ 7]  999 	ld	a, (hl)
   4549 DD 77 ED      [19] 1000 	ld	-19 (ix), a
   454C DD 6E F7      [19] 1001 	ld	l,-9 (ix)
   454F DD 66 F8      [19] 1002 	ld	h,-8 (ix)
   4552 46            [ 7] 1003 	ld	b, (hl)
   4553 DD 6E F5      [19] 1004 	ld	l,-11 (ix)
   4556 DD 66 F6      [19] 1005 	ld	h,-10 (ix)
   4559 6E            [ 7] 1006 	ld	l, (hl)
   455A DD 75 EB      [19] 1007 	ld	-21 (ix), l
   455D DD 36 EC 00   [19] 1008 	ld	-20 (ix), #0x00
   4561 1A            [ 7] 1009 	ld	a, (de)
   4562 DD 77 E9      [19] 1010 	ld	-23 (ix), a
   4565 DD 36 EA 00   [19] 1011 	ld	-22 (ix), #0x00
   4569 C5            [11] 1012 	push	bc
   456A D5            [11] 1013 	push	de
   456B DD 66 FF      [19] 1014 	ld	h, -1 (ix)
   456E DD 6E F2      [19] 1015 	ld	l, -14 (ix)
   4571 E5            [11] 1016 	push	hl
   4572 DD 6E F0      [19] 1017 	ld	l,-16 (ix)
   4575 DD 66 F1      [19] 1018 	ld	h,-15 (ix)
   4578 E5            [11] 1019 	push	hl
   4579 DD 6E EE      [19] 1020 	ld	l,-18 (ix)
   457C DD 66 EF      [19] 1021 	ld	h,-17 (ix)
   457F E5            [11] 1022 	push	hl
   4580 DD 7E ED      [19] 1023 	ld	a, -19 (ix)
   4583 F5            [11] 1024 	push	af
   4584 33            [ 6] 1025 	inc	sp
   4585 C5            [11] 1026 	push	bc
   4586 33            [ 6] 1027 	inc	sp
   4587 DD 6E EB      [19] 1028 	ld	l,-21 (ix)
   458A DD 66 EC      [19] 1029 	ld	h,-20 (ix)
   458D E5            [11] 1030 	push	hl
   458E DD 6E E9      [19] 1031 	ld	l,-23 (ix)
   4591 DD 66 EA      [19] 1032 	ld	h,-22 (ix)
   4594 E5            [11] 1033 	push	hl
   4595 CD 19 40      [17] 1034 	call	_rect_overlap
   4598 FD 21 0C 00   [14] 1035 	ld	iy, #12
   459C FD 39         [15] 1036 	add	iy, sp
   459E FD F9         [10] 1037 	ld	sp, iy
   45A0 D1            [10] 1038 	pop	de
   45A1 C1            [10] 1039 	pop	bc
   45A2 7D            [ 4] 1040 	ld	a, l
   45A3 B7            [ 4] 1041 	or	a, a
   45A4 28 58         [12] 1042 	jr	Z,00125$
                           1043 ;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   45A6 DD 6E F3      [19] 1044 	ld	l,-13 (ix)
   45A9 DD 66 F4      [19] 1045 	ld	h,-12 (ix)
   45AC 66            [ 7] 1046 	ld	h, (hl)
   45AD DD 6E FB      [19] 1047 	ld	l, -5 (ix)
   45B0 DD 46 FC      [19] 1048 	ld	b, -4 (ix)
   45B3 C5            [11] 1049 	push	bc
   45B4 D5            [11] 1050 	push	de
   45B5 E5            [11] 1051 	push	hl
   45B6 33            [ 6] 1052 	inc	sp
   45B7 60            [ 4] 1053 	ld	h, b
   45B8 E5            [11] 1054 	push	hl
   45B9 CD 14 5A      [17] 1055 	call	_enemydamage
   45BC F1            [10] 1056 	pop	af
   45BD 33            [ 6] 1057 	inc	sp
   45BE D1            [10] 1058 	pop	de
   45BF C1            [10] 1059 	pop	bc
   45C0 7D            [ 4] 1060 	ld	a, l
   45C1 B7            [ 4] 1061 	or	a, a
   45C2 28 30         [12] 1062 	jr	Z,00124$
                           1063 ;src/game.c:206: g_score = (u16)(g_score + g_enemies[j].reward);
   45C4 DD 6E FB      [19] 1064 	ld	l,-5 (ix)
   45C7 DD 66 FC      [19] 1065 	ld	h,-4 (ix)
   45CA C5            [11] 1066 	push	bc
   45CB 01 08 00      [10] 1067 	ld	bc, #0x0008
   45CE 09            [11] 1068 	add	hl, bc
   45CF C1            [10] 1069 	pop	bc
   45D0 7E            [ 7] 1070 	ld	a, (hl)
   45D1 DD 77 E9      [19] 1071 	ld	-23 (ix), a
   45D4 23            [ 6] 1072 	inc	hl
   45D5 7E            [ 7] 1073 	ld	a, (hl)
   45D6 DD 77 EA      [19] 1074 	ld	-22 (ix), a
   45D9 21 83 62      [10] 1075 	ld	hl, #_g_score
   45DC 7E            [ 7] 1076 	ld	a, (hl)
   45DD DD 86 E9      [19] 1077 	add	a, -23 (ix)
   45E0 77            [ 7] 1078 	ld	(hl), a
   45E1 23            [ 6] 1079 	inc	hl
   45E2 7E            [ 7] 1080 	ld	a, (hl)
   45E3 DD 8E EA      [19] 1081 	adc	a, -22 (ix)
   45E6 77            [ 7] 1082 	ld	(hl), a
                           1083 ;src/game.c:207: if (g_aliveenemies) g_aliveenemies--;
   45E7 FD 21 88 62   [14] 1084 	ld	iy, #_g_aliveenemies
   45EB FD 7E 00      [19] 1085 	ld	a, 0 (iy)
   45EE B7            [ 4] 1086 	or	a, a
   45EF 28 03         [12] 1087 	jr	Z,00124$
   45F1 FD 35 00      [23] 1088 	dec	0 (iy)
   45F4                    1089 00124$:
                           1090 ;src/game.c:209: g_projectiles[i].active = 0;
   45F4 DD 6E FD      [19] 1091 	ld	l,-3 (ix)
   45F7 DD 66 FE      [19] 1092 	ld	h,-2 (ix)
   45FA 36 00         [10] 1093 	ld	(hl), #0x00
                           1094 ;src/game.c:210: break;
   45FC 18 0B         [12] 1095 	jr	00126$
   45FE                    1096 00125$:
                           1097 ;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
   45FE DD 34 E7      [23] 1098 	inc	-25 (ix)
   4601 DD 7E E7      [19] 1099 	ld	a, -25 (ix)
   4604 D6 06         [ 7] 1100 	sub	a, #0x06
   4606 DA B4 44      [10] 1101 	jp	C, 00178$
   4609                    1102 00126$:
                           1103 ;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4609 3A 9E 62      [13] 1104 	ld	a,(#_g_bossactive + 0)
   460C B7            [ 4] 1105 	or	a, a
   460D CA CE 46      [10] 1106 	jp	Z, 00133$
   4610 DD 6E FD      [19] 1107 	ld	l,-3 (ix)
   4613 DD 66 FE      [19] 1108 	ld	h,-2 (ix)
   4616 7E            [ 7] 1109 	ld	a, (hl)
   4617 B7            [ 4] 1110 	or	a, a
   4618 CA CE 46      [10] 1111 	jp	Z, 00133$
                           1112 ;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   461B 21 98 62      [10] 1113 	ld	hl, #(_g_boss + 0x0005) + 0
   461E 46            [ 7] 1114 	ld	b, (hl)
   461F 3A 97 62      [13] 1115 	ld	a, (#(_g_boss + 0x0004) + 0)
   4622 21 94 62      [10] 1116 	ld	hl, #(_g_boss + 0x0001) + 0
   4625 6E            [ 7] 1117 	ld	l, (hl)
   4626 DD 75 E9      [19] 1118 	ld	-23 (ix), l
   4629 DD 36 EA 00   [19] 1119 	ld	-22 (ix), #0x00
   462D 21 93 62      [10] 1120 	ld	hl, #_g_boss + 0
   4630 6E            [ 7] 1121 	ld	l, (hl)
   4631 DD 75 EB      [19] 1122 	ld	-21 (ix), l
   4634 DD 36 EC 00   [19] 1123 	ld	-20 (ix), #0x00
                           1124 ;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4638 DD 6E F9      [19] 1125 	ld	l,-7 (ix)
   463B DD 66 FA      [19] 1126 	ld	h,-6 (ix)
   463E F5            [11] 1127 	push	af
   463F 7E            [ 7] 1128 	ld	a, (hl)
   4640 DD 77 ED      [19] 1129 	ld	-19 (ix), a
   4643 F1            [10] 1130 	pop	af
   4644 DD 6E F7      [19] 1131 	ld	l,-9 (ix)
   4647 DD 66 F8      [19] 1132 	ld	h,-8 (ix)
   464A F5            [11] 1133 	push	af
   464B 7E            [ 7] 1134 	ld	a, (hl)
   464C DD 77 EE      [19] 1135 	ld	-18 (ix), a
   464F F1            [10] 1136 	pop	af
   4650 DD 6E F5      [19] 1137 	ld	l,-11 (ix)
   4653 DD 66 F6      [19] 1138 	ld	h,-10 (ix)
   4656 6E            [ 7] 1139 	ld	l, (hl)
   4657 DD 75 F0      [19] 1140 	ld	-16 (ix), l
   465A DD 36 F1 00   [19] 1141 	ld	-15 (ix), #0x00
   465E F5            [11] 1142 	push	af
   465F 1A            [ 7] 1143 	ld	a, (de)
   4660 5F            [ 4] 1144 	ld	e, a
   4661 F1            [10] 1145 	pop	af
   4662 16 00         [ 7] 1146 	ld	d, #0x00
   4664 C5            [11] 1147 	push	bc
   4665 C5            [11] 1148 	push	bc
   4666 33            [ 6] 1149 	inc	sp
   4667 F5            [11] 1150 	push	af
   4668 33            [ 6] 1151 	inc	sp
   4669 DD 6E E9      [19] 1152 	ld	l,-23 (ix)
   466C DD 66 EA      [19] 1153 	ld	h,-22 (ix)
   466F E5            [11] 1154 	push	hl
   4670 DD 6E EB      [19] 1155 	ld	l,-21 (ix)
   4673 DD 66 EC      [19] 1156 	ld	h,-20 (ix)
   4676 E5            [11] 1157 	push	hl
   4677 DD 66 ED      [19] 1158 	ld	h, -19 (ix)
   467A DD 6E EE      [19] 1159 	ld	l, -18 (ix)
   467D E5            [11] 1160 	push	hl
   467E DD 6E F0      [19] 1161 	ld	l,-16 (ix)
   4681 DD 66 F1      [19] 1162 	ld	h,-15 (ix)
   4684 E5            [11] 1163 	push	hl
   4685 D5            [11] 1164 	push	de
   4686 CD 19 40      [17] 1165 	call	_rect_overlap
   4689 FD 21 0C 00   [14] 1166 	ld	iy, #12
   468D FD 39         [15] 1167 	add	iy, sp
   468F FD F9         [10] 1168 	ld	sp, iy
   4691 C1            [10] 1169 	pop	bc
   4692 7D            [ 4] 1170 	ld	a, l
   4693 B7            [ 4] 1171 	or	a, a
   4694 28 38         [12] 1172 	jr	Z,00133$
                           1173 ;src/game.c:215: g_projectiles[i].active = 0;
   4696 DD 6E FD      [19] 1174 	ld	l,-3 (ix)
   4699 DD 66 FE      [19] 1175 	ld	h,-2 (ix)
   469C 36 00         [10] 1176 	ld	(hl), #0x00
                           1177 ;src/game.c:216: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   469E DD 6E F3      [19] 1178 	ld	l,-13 (ix)
   46A1 DD 66 F4      [19] 1179 	ld	h,-12 (ix)
   46A4 46            [ 7] 1180 	ld	b, (hl)
   46A5 11 93 62      [10] 1181 	ld	de, #_g_boss
   46A8 C5            [11] 1182 	push	bc
   46A9 C5            [11] 1183 	push	bc
   46AA 33            [ 6] 1184 	inc	sp
   46AB D5            [11] 1185 	push	de
   46AC CD 14 5A      [17] 1186 	call	_enemydamage
   46AF F1            [10] 1187 	pop	af
   46B0 33            [ 6] 1188 	inc	sp
   46B1 C1            [10] 1189 	pop	bc
   46B2 7D            [ 4] 1190 	ld	a, l
   46B3 B7            [ 4] 1191 	or	a, a
   46B4 28 18         [12] 1192 	jr	Z,00133$
                           1193 ;src/game.c:217: g_bossactive = 0;
   46B6 21 9E 62      [10] 1194 	ld	hl,#_g_bossactive + 0
   46B9 36 00         [10] 1195 	ld	(hl), #0x00
                           1196 ;src/game.c:218: g_score = (u16)(g_score + g_boss.reward);
   46BB ED 5B 9B 62   [20] 1197 	ld	de, (#_g_boss + 8)
   46BF 21 83 62      [10] 1198 	ld	hl, #_g_score
   46C2 7E            [ 7] 1199 	ld	a, (hl)
   46C3 83            [ 4] 1200 	add	a, e
   46C4 77            [ 7] 1201 	ld	(hl), a
   46C5 23            [ 6] 1202 	inc	hl
   46C6 7E            [ 7] 1203 	ld	a, (hl)
   46C7 8A            [ 4] 1204 	adc	a, d
   46C8 77            [ 7] 1205 	ld	(hl), a
                           1206 ;src/game.c:219: g_victory = 1;
   46C9 21 8C 62      [10] 1207 	ld	hl,#_g_victory + 0
   46CC 36 01         [10] 1208 	ld	(hl), #0x01
   46CE                    1209 00133$:
                           1210 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   46CE 0C            [ 4] 1211 	inc	c
   46CF 79            [ 4] 1212 	ld	a, c
   46D0 D6 06         [ 7] 1213 	sub	a, #0x06
   46D2 DA 93 44      [10] 1214 	jp	C, 00179$
                           1215 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1216 ;src/game.c:224: if (!g_damagecooldown) {
   46D5 3A 8A 62      [13] 1217 	ld	a,(#_g_damagecooldown + 0)
   46D8 B7            [ 4] 1218 	or	a, a
   46D9 C2 47 48      [10] 1219 	jp	NZ, 00149$
                           1220 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   46DC DD 36 E8 00   [19] 1221 	ld	-24 (ix), #0x00
   46E0                    1222 00180$:
                           1223 ;src/game.c:226: if (!g_enemies[i].active) continue;
   46E0 DD 4E E8      [19] 1224 	ld	c,-24 (ix)
   46E3 06 00         [ 7] 1225 	ld	b,#0x00
   46E5 69            [ 4] 1226 	ld	l, c
   46E6 60            [ 4] 1227 	ld	h, b
   46E7 29            [11] 1228 	add	hl, hl
   46E8 29            [11] 1229 	add	hl, hl
   46E9 09            [11] 1230 	add	hl, bc
   46EA 29            [11] 1231 	add	hl, hl
   46EB 09            [11] 1232 	add	hl, bc
   46EC 01 04 62      [10] 1233 	ld	bc,#_g_enemies
   46EF 09            [11] 1234 	add	hl,bc
   46F0 DD 75 E9      [19] 1235 	ld	-23 (ix), l
   46F3 DD 74 EA      [19] 1236 	ld	-22 (ix), h
   46F6 C1            [10] 1237 	pop	bc
   46F7 E1            [10] 1238 	pop	hl
   46F8 E5            [11] 1239 	push	hl
   46F9 C5            [11] 1240 	push	bc
   46FA 11 06 00      [10] 1241 	ld	de, #0x0006
   46FD 19            [11] 1242 	add	hl, de
   46FE 7E            [ 7] 1243 	ld	a, (hl)
   46FF B7            [ 4] 1244 	or	a, a
   4700 CA 91 47      [10] 1245 	jp	Z, 00139$
                           1246 ;src/game.c:228: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   4703 DD 7E E9      [19] 1247 	ld	a, -23 (ix)
   4706 DD 77 EB      [19] 1248 	ld	-21 (ix), a
   4709 DD 7E EA      [19] 1249 	ld	a, -22 (ix)
   470C DD 77 EC      [19] 1250 	ld	-20 (ix), a
   470F DD 6E EB      [19] 1251 	ld	l,-21 (ix)
   4712 DD 66 EC      [19] 1252 	ld	h,-20 (ix)
   4715 11 05 00      [10] 1253 	ld	de, #0x0005
   4718 19            [11] 1254 	add	hl, de
   4719 7E            [ 7] 1255 	ld	a, (hl)
   471A DD 77 EB      [19] 1256 	ld	-21 (ix), a
   471D C1            [10] 1257 	pop	bc
   471E E1            [10] 1258 	pop	hl
   471F E5            [11] 1259 	push	hl
   4720 C5            [11] 1260 	push	bc
   4721 11 04 00      [10] 1261 	ld	de, #0x0004
   4724 19            [11] 1262 	add	hl, de
   4725 5E            [ 7] 1263 	ld	e, (hl)
   4726 C1            [10] 1264 	pop	bc
   4727 E1            [10] 1265 	pop	hl
   4728 E5            [11] 1266 	push	hl
   4729 C5            [11] 1267 	push	bc
   472A 23            [ 6] 1268 	inc	hl
   472B 4E            [ 7] 1269 	ld	c, (hl)
   472C 06 00         [ 7] 1270 	ld	b, #0x00
   472E DD 6E E9      [19] 1271 	ld	l,-23 (ix)
   4731 DD 66 EA      [19] 1272 	ld	h,-22 (ix)
   4734 56            [ 7] 1273 	ld	d, (hl)
   4735 DD 72 E9      [19] 1274 	ld	-23 (ix), d
   4738 DD 36 EA 00   [19] 1275 	ld	-22 (ix), #0x00
                           1276 ;src/game.c:227: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   473C 3A 00 62      [13] 1277 	ld	a,(#(_g_player + 0x0005) + 0)
   473F DD 77 ED      [19] 1278 	ld	-19 (ix), a
   4742 3A FF 61      [13] 1279 	ld	a,(#(_g_player + 0x0004) + 0)
   4745 DD 77 EE      [19] 1280 	ld	-18 (ix), a
   4748 3A FC 61      [13] 1281 	ld	a, (#(_g_player + 0x0001) + 0)
   474B DD 77 F0      [19] 1282 	ld	-16 (ix), a
   474E DD 36 F1 00   [19] 1283 	ld	-15 (ix), #0x00
   4752 3A FB 61      [13] 1284 	ld	a, (#_g_player + 0)
   4755 DD 77 F3      [19] 1285 	ld	-13 (ix), a
   4758 DD 36 F4 00   [19] 1286 	ld	-12 (ix), #0x00
   475C DD 56 EB      [19] 1287 	ld	d, -21 (ix)
   475F D5            [11] 1288 	push	de
   4760 C5            [11] 1289 	push	bc
   4761 DD 6E E9      [19] 1290 	ld	l,-23 (ix)
   4764 DD 66 EA      [19] 1291 	ld	h,-22 (ix)
   4767 E5            [11] 1292 	push	hl
   4768 DD 66 ED      [19] 1293 	ld	h, -19 (ix)
   476B DD 6E EE      [19] 1294 	ld	l, -18 (ix)
   476E E5            [11] 1295 	push	hl
   476F DD 6E F0      [19] 1296 	ld	l,-16 (ix)
   4772 DD 66 F1      [19] 1297 	ld	h,-15 (ix)
   4775 E5            [11] 1298 	push	hl
   4776 DD 6E F3      [19] 1299 	ld	l,-13 (ix)
   4779 DD 66 F4      [19] 1300 	ld	h,-12 (ix)
   477C E5            [11] 1301 	push	hl
   477D CD 19 40      [17] 1302 	call	_rect_overlap
   4780 FD 21 0C 00   [14] 1303 	ld	iy, #12
   4784 FD 39         [15] 1304 	add	iy, sp
   4786 FD F9         [10] 1305 	ld	sp, iy
   4788 7D            [ 4] 1306 	ld	a, l
   4789 B7            [ 4] 1307 	or	a, a
   478A 28 05         [12] 1308 	jr	Z,00139$
                           1309 ;src/game.c:229: register_player_hit();
   478C CD 94 42      [17] 1310 	call	_register_player_hit
                           1311 ;src/game.c:230: break;
   478F 18 0B         [12] 1312 	jr	00140$
   4791                    1313 00139$:
                           1314 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   4791 DD 34 E8      [23] 1315 	inc	-24 (ix)
   4794 DD 7E E8      [19] 1316 	ld	a, -24 (ix)
   4797 D6 06         [ 7] 1317 	sub	a, #0x06
   4799 DA E0 46      [10] 1318 	jp	C, 00180$
   479C                    1319 00140$:
                           1320 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   479C 3A 8A 62      [13] 1321 	ld	a,(#_g_damagecooldown + 0)
   479F B7            [ 4] 1322 	or	a, a
   47A0 20 6E         [12] 1323 	jr	NZ,00142$
   47A2 3A 9E 62      [13] 1324 	ld	a,(#_g_bossactive + 0)
   47A5 B7            [ 4] 1325 	or	a, a
   47A6 28 68         [12] 1326 	jr	Z,00142$
                           1327 ;src/game.c:235: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   47A8 3A 98 62      [13] 1328 	ld	a,(#(_g_boss + 0x0005) + 0)
   47AB DD 77 E9      [19] 1329 	ld	-23 (ix), a
   47AE 3A 97 62      [13] 1330 	ld	a,(#(_g_boss + 0x0004) + 0)
   47B1 DD 77 EB      [19] 1331 	ld	-21 (ix), a
   47B4 21 94 62      [10] 1332 	ld	hl, #(_g_boss + 0x0001) + 0
   47B7 5E            [ 7] 1333 	ld	e, (hl)
   47B8 16 00         [ 7] 1334 	ld	d, #0x00
   47BA 21 93 62      [10] 1335 	ld	hl, #_g_boss + 0
   47BD 4E            [ 7] 1336 	ld	c, (hl)
   47BE 06 00         [ 7] 1337 	ld	b, #0x00
                           1338 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   47C0 3A 00 62      [13] 1339 	ld	a,(#(_g_player + 0x0005) + 0)
   47C3 DD 77 ED      [19] 1340 	ld	-19 (ix), a
   47C6 3A FF 61      [13] 1341 	ld	a,(#(_g_player + 0x0004) + 0)
   47C9 DD 77 EE      [19] 1342 	ld	-18 (ix), a
   47CC 3A FC 61      [13] 1343 	ld	a, (#(_g_player + 0x0001) + 0)
   47CF DD 77 F0      [19] 1344 	ld	-16 (ix), a
   47D2 DD 36 F1 00   [19] 1345 	ld	-15 (ix), #0x00
   47D6 3A FB 61      [13] 1346 	ld	a, (#_g_player + 0)
   47D9 DD 77 F3      [19] 1347 	ld	-13 (ix), a
   47DC DD 36 F4 00   [19] 1348 	ld	-12 (ix), #0x00
   47E0 DD 66 E9      [19] 1349 	ld	h, -23 (ix)
   47E3 DD 6E EB      [19] 1350 	ld	l, -21 (ix)
   47E6 E5            [11] 1351 	push	hl
   47E7 D5            [11] 1352 	push	de
   47E8 C5            [11] 1353 	push	bc
   47E9 DD 66 ED      [19] 1354 	ld	h, -19 (ix)
   47EC DD 6E EE      [19] 1355 	ld	l, -18 (ix)
   47EF E5            [11] 1356 	push	hl
   47F0 DD 6E F0      [19] 1357 	ld	l,-16 (ix)
   47F3 DD 66 F1      [19] 1358 	ld	h,-15 (ix)
   47F6 E5            [11] 1359 	push	hl
   47F7 DD 6E F3      [19] 1360 	ld	l,-13 (ix)
   47FA DD 66 F4      [19] 1361 	ld	h,-12 (ix)
   47FD E5            [11] 1362 	push	hl
   47FE CD 19 40      [17] 1363 	call	_rect_overlap
   4801 FD 21 0C 00   [14] 1364 	ld	iy, #12
   4805 FD 39         [15] 1365 	add	iy, sp
   4807 FD F9         [10] 1366 	ld	sp, iy
   4809 7D            [ 4] 1367 	ld	a, l
   480A B7            [ 4] 1368 	or	a, a
   480B 28 03         [12] 1369 	jr	Z,00142$
                           1370 ;src/game.c:236: register_player_hit();
   480D CD 94 42      [17] 1371 	call	_register_player_hit
   4810                    1372 00142$:
                           1373 ;src/game.c:239: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   4810 3A 8A 62      [13] 1374 	ld	a,(#_g_damagecooldown + 0)
   4813 B7            [ 4] 1375 	or	a, a
   4814 20 31         [12] 1376 	jr	NZ,00149$
   4816 3A 00 62      [13] 1377 	ld	a, (#(_g_player + 0x0005) + 0)
   4819 21 FF 61      [10] 1378 	ld	hl, #(_g_player + 0x0004) + 0
   481C 56            [ 7] 1379 	ld	d, (hl)
   481D 21 FC 61      [10] 1380 	ld	hl, #(_g_player + 0x0001) + 0
   4820 4E            [ 7] 1381 	ld	c, (hl)
   4821 06 00         [ 7] 1382 	ld	b, #0x00
   4823 21 FB 61      [10] 1383 	ld	hl, #_g_player + 0
   4826 6E            [ 7] 1384 	ld	l, (hl)
   4827 DD 75 E9      [19] 1385 	ld	-23 (ix), l
   482A DD 36 EA 00   [19] 1386 	ld	-22 (ix), #0x00
   482E F5            [11] 1387 	push	af
   482F 33            [ 6] 1388 	inc	sp
   4830 D5            [11] 1389 	push	de
   4831 33            [ 6] 1390 	inc	sp
   4832 C5            [11] 1391 	push	bc
   4833 DD 6E E9      [19] 1392 	ld	l,-23 (ix)
   4836 DD 66 EA      [19] 1393 	ld	h,-22 (ix)
   4839 E5            [11] 1394 	push	hl
   483A CD DD 4C      [17] 1395 	call	_collision_is_on_trap
   483D F1            [10] 1396 	pop	af
   483E F1            [10] 1397 	pop	af
   483F F1            [10] 1398 	pop	af
   4840 7D            [ 4] 1399 	ld	a, l
   4841 B7            [ 4] 1400 	or	a, a
   4842 28 03         [12] 1401 	jr	Z,00149$
                           1402 ;src/game.c:240: register_player_hit();
   4844 CD 94 42      [17] 1403 	call	_register_player_hit
   4847                    1404 00149$:
                           1405 ;src/game.c:244: if (!g_checkpointactive && g_player.x >= 44) {
   4847 FD 21 92 62   [14] 1406 	ld	iy, #_g_checkpointactive
   484B FD 7E 00      [19] 1407 	ld	a, 0 (iy)
   484E B7            [ 4] 1408 	or	a, a
   484F 20 1E         [12] 1409 	jr	NZ,00151$
   4851 3A FB 61      [13] 1410 	ld	a, (#_g_player + 0)
   4854 D6 2C         [ 7] 1411 	sub	a, #0x2c
   4856 38 17         [12] 1412 	jr	C,00151$
                           1413 ;src/game.c:245: g_checkpointactive = 1;
   4858 FD 36 00 01   [19] 1414 	ld	0 (iy), #0x01
                           1415 ;src/game.c:246: g_checkpointx = 52;
   485C 21 90 62      [10] 1416 	ld	hl,#_g_checkpointx + 0
   485F 36 34         [10] 1417 	ld	(hl), #0x34
                           1418 ;src/game.c:247: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   4861 CD 14 51      [17] 1419 	call	_tilemap_ground_y
   4864 4D            [ 4] 1420 	ld	c, l
   4865 21 00 62      [10] 1421 	ld	hl, #(_g_player + 0x0005) + 0
   4868 46            [ 7] 1422 	ld	b, (hl)
   4869 21 91 62      [10] 1423 	ld	hl, #_g_checkpointy
   486C 79            [ 4] 1424 	ld	a, c
   486D 90            [ 4] 1425 	sub	a, b
   486E 77            [ 7] 1426 	ld	(hl), a
   486F                    1427 00151$:
                           1428 ;src/game.c:250: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
   486F 3A A1 62      [13] 1429 	ld	a,(#_g_pickuptaken + 0)
   4872 B7            [ 4] 1430 	or	a, a
   4873 C2 02 49      [10] 1431 	jp	NZ, 00154$
   4876 CD 14 51      [17] 1432 	call	_tilemap_ground_y
   4879 DD 75 E9      [19] 1433 	ld	-23 (ix), l
   487C DD 75 E9      [19] 1434 	ld	-23 (ix), l
   487F DD 36 EA 00   [19] 1435 	ld	-22 (ix), #0x00
   4883 DD 7E E9      [19] 1436 	ld	a, -23 (ix)
   4886 C6 F8         [ 7] 1437 	add	a, #0xf8
   4888 DD 77 E9      [19] 1438 	ld	-23 (ix), a
   488B DD 7E EA      [19] 1439 	ld	a, -22 (ix)
   488E CE FF         [ 7] 1440 	adc	a, #0xff
   4890 DD 77 EA      [19] 1441 	ld	-22 (ix), a
   4893 3A 00 62      [13] 1442 	ld	a,(#(_g_player + 0x0005) + 0)
   4896 DD 77 EB      [19] 1443 	ld	-21 (ix), a
   4899 3A FF 61      [13] 1444 	ld	a,(#(_g_player + 0x0004) + 0)
   489C DD 77 ED      [19] 1445 	ld	-19 (ix), a
   489F 3A FC 61      [13] 1446 	ld	a,(#(_g_player + 0x0001) + 0)
   48A2 DD 77 EE      [19] 1447 	ld	-18 (ix), a
   48A5 DD 77 EE      [19] 1448 	ld	-18 (ix), a
   48A8 DD 36 EF 00   [19] 1449 	ld	-17 (ix), #0x00
   48AC 3A FB 61      [13] 1450 	ld	a,(#_g_player + 0)
   48AF DD 77 F0      [19] 1451 	ld	-16 (ix), a
   48B2 DD 77 F0      [19] 1452 	ld	-16 (ix), a
   48B5 DD 36 F1 00   [19] 1453 	ld	-15 (ix), #0x00
   48B9 21 04 04      [10] 1454 	ld	hl, #0x0404
   48BC E5            [11] 1455 	push	hl
   48BD DD 6E E9      [19] 1456 	ld	l,-23 (ix)
   48C0 DD 66 EA      [19] 1457 	ld	h,-22 (ix)
   48C3 E5            [11] 1458 	push	hl
   48C4 21 24 00      [10] 1459 	ld	hl, #0x0024
   48C7 E5            [11] 1460 	push	hl
   48C8 DD 66 EB      [19] 1461 	ld	h, -21 (ix)
   48CB DD 6E ED      [19] 1462 	ld	l, -19 (ix)
   48CE E5            [11] 1463 	push	hl
   48CF DD 6E EE      [19] 1464 	ld	l,-18 (ix)
   48D2 DD 66 EF      [19] 1465 	ld	h,-17 (ix)
   48D5 E5            [11] 1466 	push	hl
   48D6 DD 6E F0      [19] 1467 	ld	l,-16 (ix)
   48D9 DD 66 F1      [19] 1468 	ld	h,-15 (ix)
   48DC E5            [11] 1469 	push	hl
   48DD CD 19 40      [17] 1470 	call	_rect_overlap
   48E0 FD 21 0C 00   [14] 1471 	ld	iy, #12
   48E4 FD 39         [15] 1472 	add	iy, sp
   48E6 FD F9         [10] 1473 	ld	sp, iy
   48E8 7D            [ 4] 1474 	ld	a, l
   48E9 B7            [ 4] 1475 	or	a, a
   48EA 28 16         [12] 1476 	jr	Z,00154$
                           1477 ;src/game.c:251: g_pickuptaken = 1;
   48EC 21 A1 62      [10] 1478 	ld	hl,#_g_pickuptaken + 0
   48EF 36 01         [10] 1479 	ld	(hl), #0x01
                           1480 ;src/game.c:252: g_weaponlevel = 1;
   48F1 21 A0 62      [10] 1481 	ld	hl,#_g_weaponlevel + 0
   48F4 36 01         [10] 1482 	ld	(hl), #0x01
                           1483 ;src/game.c:253: g_score = (u16)(g_score + 100);
   48F6 21 83 62      [10] 1484 	ld	hl, #_g_score
   48F9 7E            [ 7] 1485 	ld	a, (hl)
   48FA C6 64         [ 7] 1486 	add	a, #0x64
   48FC 77            [ 7] 1487 	ld	(hl), a
   48FD 23            [ 6] 1488 	inc	hl
   48FE 7E            [ 7] 1489 	ld	a, (hl)
   48FF CE 00         [ 7] 1490 	adc	a, #0x00
   4901 77            [ 7] 1491 	ld	(hl), a
   4902                    1492 00154$:
                           1493 ;src/game.c:256: g_weapondisplay = (u8)(g_weaponlevel + 1);
   4902 21 86 62      [10] 1494 	ld	hl, #_g_weapondisplay
   4905 3A A0 62      [13] 1495 	ld	a,(#_g_weaponlevel + 0)
   4908 3C            [ 4] 1496 	inc	a
   4909 77            [ 7] 1497 	ld	(hl), a
                           1498 ;src/game.c:258: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   490A 3A 9E 62      [13] 1499 	ld	a,(#_g_bossactive + 0)
   490D B7            [ 4] 1500 	or	a, a
   490E 20 45         [12] 1501 	jr	NZ,00165$
   4910 3A 88 62      [13] 1502 	ld	a,(#_g_aliveenemies + 0)
   4913 B7            [ 4] 1503 	or	a, a
   4914 20 3F         [12] 1504 	jr	NZ,00165$
   4916 3A 8D 62      [13] 1505 	ld	a,(#_g_gameover + 0)
   4919 B7            [ 4] 1506 	or	a, a
   491A 20 39         [12] 1507 	jr	NZ,00165$
                           1508 ;src/game.c:259: if (g_currentwave < TOTAL_WAVES) {
   491C 3A 87 62      [13] 1509 	ld	a,(#_g_currentwave + 0)
   491F D6 03         [ 7] 1510 	sub	a, #0x03
   4921 30 20         [12] 1511 	jr	NC,00162$
                           1512 ;src/game.c:260: if (g_wavecooldown == 0) {
   4923 3A 89 62      [13] 1513 	ld	a,(#_g_wavecooldown + 0)
   4926 B7            [ 4] 1514 	or	a, a
   4927 20 14         [12] 1515 	jr	NZ,00157$
                           1516 ;src/game.c:261: spawn_wave(g_currentwave);
   4929 3A 87 62      [13] 1517 	ld	a, (_g_currentwave)
   492C F5            [11] 1518 	push	af
   492D 33            [ 6] 1519 	inc	sp
   492E CD A6 40      [17] 1520 	call	_spawn_wave
   4931 33            [ 6] 1521 	inc	sp
                           1522 ;src/game.c:262: g_currentwave++;
   4932 21 87 62      [10] 1523 	ld	hl, #_g_currentwave+0
   4935 34            [11] 1524 	inc	(hl)
                           1525 ;src/game.c:263: g_wavecooldown = 90;
   4936 21 89 62      [10] 1526 	ld	hl,#_g_wavecooldown + 0
   4939 36 5A         [10] 1527 	ld	(hl), #0x5a
   493B 18 18         [12] 1528 	jr	00165$
   493D                    1529 00157$:
                           1530 ;src/game.c:265: g_wavecooldown--;
   493D 21 89 62      [10] 1531 	ld	hl, #_g_wavecooldown+0
   4940 35            [11] 1532 	dec	(hl)
   4941 18 12         [12] 1533 	jr	00165$
   4943                    1534 00162$:
                           1535 ;src/game.c:267: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   4943 21 FB 61      [10] 1536 	ld	hl, #_g_player + 0
   4946 4E            [ 7] 1537 	ld	c, (hl)
   4947 C5            [11] 1538 	push	bc
   4948 CD B8 51      [17] 1539 	call	_tilemap_goal_x
   494B C1            [10] 1540 	pop	bc
   494C 2D            [ 4] 1541 	dec	l
   494D 2D            [ 4] 1542 	dec	l
   494E 79            [ 4] 1543 	ld	a, c
   494F 95            [ 4] 1544 	sub	a, l
   4950 38 03         [12] 1545 	jr	C,00165$
                           1546 ;src/game.c:268: spawn_boss();
   4952 CD A8 41      [17] 1547 	call	_spawn_boss
   4955                    1548 00165$:
                           1549 ;src/game.c:272: g_framecounter++;
   4955 FD 21 8E 62   [14] 1550 	ld	iy, #_g_framecounter
   4959 FD 34 00      [23] 1551 	inc	0 (iy)
   495C 20 03         [12] 1552 	jr	NZ,00381$
   495E FD 34 01      [23] 1553 	inc	1 (iy)
   4961                    1554 00381$:
                           1555 ;src/game.c:273: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   4961 21 32 00      [10] 1556 	ld	hl, #0x0032
   4964 E5            [11] 1557 	push	hl
   4965 2A 8E 62      [16] 1558 	ld	hl, (_g_framecounter)
   4968 E5            [11] 1559 	push	hl
   4969 CD AD 60      [17] 1560 	call	__moduint
   496C F1            [10] 1561 	pop	af
   496D F1            [10] 1562 	pop	af
   496E 7C            [ 4] 1563 	ld	a, h
   496F B5            [ 4] 1564 	or	a,l
   4970 20 0D         [12] 1565 	jr	NZ,00169$
   4972 FD 21 85 62   [14] 1566 	ld	iy, #_g_timeleft
   4976 FD 7E 00      [19] 1567 	ld	a, 0 (iy)
   4979 B7            [ 4] 1568 	or	a, a
   497A 28 03         [12] 1569 	jr	Z,00169$
                           1570 ;src/game.c:274: g_timeleft--;
   497C FD 35 00      [23] 1571 	dec	0 (iy)
   497F                    1572 00169$:
                           1573 ;src/game.c:276: if (g_timeleft == 0 && !g_victory) {
   497F 3A 85 62      [13] 1574 	ld	a,(#_g_timeleft + 0)
   4982 B7            [ 4] 1575 	or	a, a
   4983 20 0B         [12] 1576 	jr	NZ,00172$
   4985 3A 8C 62      [13] 1577 	ld	a,(#_g_victory + 0)
   4988 B7            [ 4] 1578 	or	a, a
   4989 20 05         [12] 1579 	jr	NZ,00172$
                           1580 ;src/game.c:277: g_gameover = 1;
   498B 21 8D 62      [10] 1581 	ld	hl,#_g_gameover + 0
   498E 36 01         [10] 1582 	ld	(hl), #0x01
   4990                    1583 00172$:
                           1584 ;src/game.c:280: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4990 3A 86 62      [13] 1585 	ld	a, (_g_weapondisplay)
   4993 F5            [11] 1586 	push	af
   4994 33            [ 6] 1587 	inc	sp
   4995 3A 85 62      [13] 1588 	ld	a, (_g_timeleft)
   4998 F5            [11] 1589 	push	af
   4999 33            [ 6] 1590 	inc	sp
   499A 2A 83 62      [16] 1591 	ld	hl, (_g_score)
   499D E5            [11] 1592 	push	hl
   499E 3A 82 62      [13] 1593 	ld	a, (_g_lives)
   49A1 F5            [11] 1594 	push	af
   49A2 33            [ 6] 1595 	inc	sp
   49A3 CD B2 4E      [17] 1596 	call	_hudupdate
   49A6 F1            [10] 1597 	pop	af
   49A7 F1            [10] 1598 	pop	af
   49A8 33            [ 6] 1599 	inc	sp
   49A9                    1600 00181$:
   49A9 DD F9         [10] 1601 	ld	sp, ix
   49AB DD E1         [14] 1602 	pop	ix
   49AD C9            [10] 1603 	ret
                           1604 ;src/game.c:283: void game_render(void) {
                           1605 ;	---------------------------------
                           1606 ; Function game_render
                           1607 ; ---------------------------------
   49AE                    1608 _game_render::
                           1609 ;src/game.c:286: cpct_clearScreen(0x00);
   49AE 21 00 40      [10] 1610 	ld	hl, #0x4000
   49B1 E5            [11] 1611 	push	hl
   49B2 AF            [ 4] 1612 	xor	a, a
   49B3 F5            [11] 1613 	push	af
   49B4 33            [ 6] 1614 	inc	sp
   49B5 26 C0         [ 7] 1615 	ld	h, #0xc0
   49B7 E5            [11] 1616 	push	hl
   49B8 CD F4 60      [17] 1617 	call	_cpct_memset
                           1618 ;src/game.c:288: tilemap_render();
   49BB CD 73 50      [17] 1619 	call	_tilemap_render
                           1620 ;src/game.c:290: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49BE 0E 00         [ 7] 1621 	ld	c, #0x00
   49C0                    1622 00115$:
                           1623 ;src/game.c:291: projectilerender(&g_projectiles[i]);
   49C0 06 00         [ 7] 1624 	ld	b,#0x00
   49C2 69            [ 4] 1625 	ld	l, c
   49C3 60            [ 4] 1626 	ld	h, b
   49C4 29            [11] 1627 	add	hl, hl
   49C5 29            [11] 1628 	add	hl, hl
   49C6 09            [11] 1629 	add	hl, bc
   49C7 29            [11] 1630 	add	hl, hl
   49C8 11 46 62      [10] 1631 	ld	de, #_g_projectiles
   49CB 19            [11] 1632 	add	hl, de
   49CC C5            [11] 1633 	push	bc
   49CD E5            [11] 1634 	push	hl
   49CE CD 9A 5E      [17] 1635 	call	_projectilerender
   49D1 F1            [10] 1636 	pop	af
   49D2 C1            [10] 1637 	pop	bc
                           1638 ;src/game.c:290: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49D3 0C            [ 4] 1639 	inc	c
   49D4 79            [ 4] 1640 	ld	a, c
   49D5 D6 06         [ 7] 1641 	sub	a, #0x06
   49D7 38 E7         [12] 1642 	jr	C,00115$
                           1643 ;src/game.c:294: for (i = 0; i < MAX_ENEMIES; ++i) {
   49D9 0E 00         [ 7] 1644 	ld	c, #0x00
   49DB                    1645 00117$:
                           1646 ;src/game.c:295: enemyrender(&g_enemies[i]);
   49DB 06 00         [ 7] 1647 	ld	b,#0x00
   49DD 69            [ 4] 1648 	ld	l, c
   49DE 60            [ 4] 1649 	ld	h, b
   49DF 29            [11] 1650 	add	hl, hl
   49E0 29            [11] 1651 	add	hl, hl
   49E1 09            [11] 1652 	add	hl, bc
   49E2 29            [11] 1653 	add	hl, hl
   49E3 09            [11] 1654 	add	hl, bc
   49E4 11 04 62      [10] 1655 	ld	de, #_g_enemies
   49E7 19            [11] 1656 	add	hl, de
   49E8 C5            [11] 1657 	push	bc
   49E9 E5            [11] 1658 	push	hl
   49EA CD 82 59      [17] 1659 	call	_enemyrender
   49ED F1            [10] 1660 	pop	af
   49EE C1            [10] 1661 	pop	bc
                           1662 ;src/game.c:294: for (i = 0; i < MAX_ENEMIES; ++i) {
   49EF 0C            [ 4] 1663 	inc	c
   49F0 79            [ 4] 1664 	ld	a, c
   49F1 D6 06         [ 7] 1665 	sub	a, #0x06
   49F3 38 E6         [12] 1666 	jr	C,00117$
                           1667 ;src/game.c:298: if (g_bossactive) {
   49F5 3A 9E 62      [13] 1668 	ld	a,(#_g_bossactive + 0)
   49F8 B7            [ 4] 1669 	or	a, a
   49F9 28 58         [12] 1670 	jr	Z,00104$
                           1671 ;src/game.c:299: enemyrender(&g_boss);
   49FB 21 93 62      [10] 1672 	ld	hl, #_g_boss
   49FE E5            [11] 1673 	push	hl
   49FF CD 82 59      [17] 1674 	call	_enemyrender
                           1675 ;src/game.c:300: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(1, 1), 32, 2);
   4A02 21 01 01      [10] 1676 	ld	hl, #0x0101
   4A05 E3            [19] 1677 	ex	(sp),hl
   4A06 CD D8 60      [17] 1678 	call	_cpct_px2byteM0
   4A09 55            [ 4] 1679 	ld	d, l
   4A0A D5            [11] 1680 	push	de
   4A0B 21 18 0A      [10] 1681 	ld	hl, #0x0a18
   4A0E E5            [11] 1682 	push	hl
   4A0F 21 00 C0      [10] 1683 	ld	hl, #0xc000
   4A12 E5            [11] 1684 	push	hl
   4A13 CD CB 61      [17] 1685 	call	_cpct_getScreenPtr
   4A16 4D            [ 4] 1686 	ld	c, l
   4A17 44            [ 4] 1687 	ld	b, h
   4A18 D1            [10] 1688 	pop	de
   4A19 21 20 02      [10] 1689 	ld	hl, #0x0220
   4A1C E5            [11] 1690 	push	hl
   4A1D D5            [11] 1691 	push	de
   4A1E 33            [ 6] 1692 	inc	sp
   4A1F C5            [11] 1693 	push	bc
   4A20 CD 12 61      [17] 1694 	call	_cpct_drawSolidBox
   4A23 F1            [10] 1695 	pop	af
   4A24 F1            [10] 1696 	pop	af
   4A25 33            [ 6] 1697 	inc	sp
                           1698 ;src/game.c:301: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
   4A26 3A 9A 62      [13] 1699 	ld	a, (#_g_boss + 7)
   4A29 4F            [ 4] 1700 	ld	c, a
   4A2A 87            [ 4] 1701 	add	a, a
   4A2B 81            [ 4] 1702 	add	a, c
   4A2C 57            [ 4] 1703 	ld	d, a
   4A2D D5            [11] 1704 	push	de
   4A2E 21 05 05      [10] 1705 	ld	hl, #0x0505
   4A31 E5            [11] 1706 	push	hl
   4A32 CD D8 60      [17] 1707 	call	_cpct_px2byteM0
   4A35 5D            [ 4] 1708 	ld	e, l
   4A36 F1            [10] 1709 	pop	af
   4A37 57            [ 4] 1710 	ld	d, a
   4A38 D5            [11] 1711 	push	de
   4A39 21 18 0A      [10] 1712 	ld	hl, #0x0a18
   4A3C E5            [11] 1713 	push	hl
   4A3D 21 00 C0      [10] 1714 	ld	hl, #0xc000
   4A40 E5            [11] 1715 	push	hl
   4A41 CD CB 61      [17] 1716 	call	_cpct_getScreenPtr
   4A44 4D            [ 4] 1717 	ld	c, l
   4A45 44            [ 4] 1718 	ld	b, h
   4A46 D1            [10] 1719 	pop	de
   4A47 3E 02         [ 7] 1720 	ld	a, #0x02
   4A49 F5            [11] 1721 	push	af
   4A4A 33            [ 6] 1722 	inc	sp
   4A4B D5            [11] 1723 	push	de
   4A4C C5            [11] 1724 	push	bc
   4A4D CD 12 61      [17] 1725 	call	_cpct_drawSolidBox
   4A50 F1            [10] 1726 	pop	af
   4A51 F1            [10] 1727 	pop	af
   4A52 33            [ 6] 1728 	inc	sp
   4A53                    1729 00104$:
                           1730 ;src/game.c:304: if (!g_pickuptaken) {
   4A53 3A A1 62      [13] 1731 	ld	a,(#_g_pickuptaken + 0)
   4A56 B7            [ 4] 1732 	or	a, a
   4A57 20 2F         [12] 1733 	jr	NZ,00106$
                           1734 ;src/game.c:305: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
   4A59 21 07 07      [10] 1735 	ld	hl, #0x0707
   4A5C E5            [11] 1736 	push	hl
   4A5D CD D8 60      [17] 1737 	call	_cpct_px2byteM0
   4A60 55            [ 4] 1738 	ld	d, l
   4A61 D5            [11] 1739 	push	de
   4A62 CD 14 51      [17] 1740 	call	_tilemap_ground_y
   4A65 D1            [10] 1741 	pop	de
   4A66 7D            [ 4] 1742 	ld	a, l
   4A67 C6 F8         [ 7] 1743 	add	a, #0xf8
   4A69 47            [ 4] 1744 	ld	b, a
   4A6A D5            [11] 1745 	push	de
   4A6B C5            [11] 1746 	push	bc
   4A6C 33            [ 6] 1747 	inc	sp
   4A6D 3E 24         [ 7] 1748 	ld	a, #0x24
   4A6F F5            [11] 1749 	push	af
   4A70 33            [ 6] 1750 	inc	sp
   4A71 21 00 C0      [10] 1751 	ld	hl, #0xc000
   4A74 E5            [11] 1752 	push	hl
   4A75 CD CB 61      [17] 1753 	call	_cpct_getScreenPtr
   4A78 4D            [ 4] 1754 	ld	c, l
   4A79 44            [ 4] 1755 	ld	b, h
   4A7A D1            [10] 1756 	pop	de
   4A7B 21 04 04      [10] 1757 	ld	hl, #0x0404
   4A7E E5            [11] 1758 	push	hl
   4A7F D5            [11] 1759 	push	de
   4A80 33            [ 6] 1760 	inc	sp
   4A81 C5            [11] 1761 	push	bc
   4A82 CD 12 61      [17] 1762 	call	_cpct_drawSolidBox
   4A85 F1            [10] 1763 	pop	af
   4A86 F1            [10] 1764 	pop	af
   4A87 33            [ 6] 1765 	inc	sp
   4A88                    1766 00106$:
                           1767 ;src/game.c:307: playerrender(&g_player);
   4A88 21 FB 61      [10] 1768 	ld	hl, #_g_player
   4A8B E5            [11] 1769 	push	hl
   4A8C CD E0 5C      [17] 1770 	call	_playerrender
   4A8F F1            [10] 1771 	pop	af
                           1772 ;src/game.c:308: hudrender();
   4A90 CD E3 4E      [17] 1773 	call	_hudrender
                           1774 ;src/game.c:310: if (g_victory) {
   4A93 3A 8C 62      [13] 1775 	ld	a,(#_g_victory + 0)
   4A96 B7            [ 4] 1776 	or	a, a
   4A97 28 48         [12] 1777 	jr	Z,00113$
                           1778 ;src/game.c:311: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
   4A99 21 08 08      [10] 1779 	ld	hl, #0x0808
   4A9C E5            [11] 1780 	push	hl
   4A9D CD D8 60      [17] 1781 	call	_cpct_px2byteM0
   4AA0 55            [ 4] 1782 	ld	d, l
   4AA1 D5            [11] 1783 	push	de
   4AA2 21 18 44      [10] 1784 	ld	hl, #0x4418
   4AA5 E5            [11] 1785 	push	hl
   4AA6 21 00 C0      [10] 1786 	ld	hl, #0xc000
   4AA9 E5            [11] 1787 	push	hl
   4AAA CD CB 61      [17] 1788 	call	_cpct_getScreenPtr
   4AAD 4D            [ 4] 1789 	ld	c, l
   4AAE 44            [ 4] 1790 	ld	b, h
   4AAF D1            [10] 1791 	pop	de
   4AB0 21 20 0C      [10] 1792 	ld	hl, #0x0c20
   4AB3 E5            [11] 1793 	push	hl
   4AB4 D5            [11] 1794 	push	de
   4AB5 33            [ 6] 1795 	inc	sp
   4AB6 C5            [11] 1796 	push	bc
   4AB7 CD 12 61      [17] 1797 	call	_cpct_drawSolidBox
   4ABA F1            [10] 1798 	pop	af
                           1799 ;src/game.c:312: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(5, 5), 24, 8);
   4ABB 33            [ 6] 1800 	inc	sp
   4ABC 21 05 05      [10] 1801 	ld	hl,#0x0505
   4ABF E3            [19] 1802 	ex	(sp),hl
   4AC0 CD D8 60      [17] 1803 	call	_cpct_px2byteM0
   4AC3 55            [ 4] 1804 	ld	d, l
   4AC4 D5            [11] 1805 	push	de
   4AC5 21 1C 48      [10] 1806 	ld	hl, #0x481c
   4AC8 E5            [11] 1807 	push	hl
   4AC9 21 00 C0      [10] 1808 	ld	hl, #0xc000
   4ACC E5            [11] 1809 	push	hl
   4ACD CD CB 61      [17] 1810 	call	_cpct_getScreenPtr
   4AD0 4D            [ 4] 1811 	ld	c, l
   4AD1 44            [ 4] 1812 	ld	b, h
   4AD2 D1            [10] 1813 	pop	de
   4AD3 21 18 08      [10] 1814 	ld	hl, #0x0818
   4AD6 E5            [11] 1815 	push	hl
   4AD7 D5            [11] 1816 	push	de
   4AD8 33            [ 6] 1817 	inc	sp
   4AD9 C5            [11] 1818 	push	bc
   4ADA CD 12 61      [17] 1819 	call	_cpct_drawSolidBox
   4ADD F1            [10] 1820 	pop	af
   4ADE F1            [10] 1821 	pop	af
   4ADF 33            [ 6] 1822 	inc	sp
   4AE0 C9            [10] 1823 	ret
   4AE1                    1824 00113$:
                           1825 ;src/game.c:313: } else if (g_gameover) {
   4AE1 3A 8D 62      [13] 1826 	ld	a,(#_g_gameover + 0)
   4AE4 B7            [ 4] 1827 	or	a, a
   4AE5 28 48         [12] 1828 	jr	Z,00110$
                           1829 ;src/game.c:314: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
   4AE7 21 01 01      [10] 1830 	ld	hl, #0x0101
   4AEA E5            [11] 1831 	push	hl
   4AEB CD D8 60      [17] 1832 	call	_cpct_px2byteM0
   4AEE 55            [ 4] 1833 	ld	d, l
   4AEF D5            [11] 1834 	push	de
   4AF0 21 18 44      [10] 1835 	ld	hl, #0x4418
   4AF3 E5            [11] 1836 	push	hl
   4AF4 21 00 C0      [10] 1837 	ld	hl, #0xc000
   4AF7 E5            [11] 1838 	push	hl
   4AF8 CD CB 61      [17] 1839 	call	_cpct_getScreenPtr
   4AFB 4D            [ 4] 1840 	ld	c, l
   4AFC 44            [ 4] 1841 	ld	b, h
   4AFD D1            [10] 1842 	pop	de
   4AFE 21 20 0C      [10] 1843 	ld	hl, #0x0c20
   4B01 E5            [11] 1844 	push	hl
   4B02 D5            [11] 1845 	push	de
   4B03 33            [ 6] 1846 	inc	sp
   4B04 C5            [11] 1847 	push	bc
   4B05 CD 12 61      [17] 1848 	call	_cpct_drawSolidBox
   4B08 F1            [10] 1849 	pop	af
                           1850 ;src/game.c:315: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), cpct_px2byteM0(6, 6), 24, 8);
   4B09 33            [ 6] 1851 	inc	sp
   4B0A 21 06 06      [10] 1852 	ld	hl,#0x0606
   4B0D E3            [19] 1853 	ex	(sp),hl
   4B0E CD D8 60      [17] 1854 	call	_cpct_px2byteM0
   4B11 55            [ 4] 1855 	ld	d, l
   4B12 D5            [11] 1856 	push	de
   4B13 21 1C 48      [10] 1857 	ld	hl, #0x481c
   4B16 E5            [11] 1858 	push	hl
   4B17 21 00 C0      [10] 1859 	ld	hl, #0xc000
   4B1A E5            [11] 1860 	push	hl
   4B1B CD CB 61      [17] 1861 	call	_cpct_getScreenPtr
   4B1E 4D            [ 4] 1862 	ld	c, l
   4B1F 44            [ 4] 1863 	ld	b, h
   4B20 D1            [10] 1864 	pop	de
   4B21 21 18 08      [10] 1865 	ld	hl, #0x0818
   4B24 E5            [11] 1866 	push	hl
   4B25 D5            [11] 1867 	push	de
   4B26 33            [ 6] 1868 	inc	sp
   4B27 C5            [11] 1869 	push	bc
   4B28 CD 12 61      [17] 1870 	call	_cpct_drawSolidBox
   4B2B F1            [10] 1871 	pop	af
   4B2C F1            [10] 1872 	pop	af
   4B2D 33            [ 6] 1873 	inc	sp
   4B2E C9            [10] 1874 	ret
   4B2F                    1875 00110$:
                           1876 ;src/game.c:316: } else if (g_checkpointactive) {
   4B2F 3A 92 62      [13] 1877 	ld	a,(#_g_checkpointactive + 0)
   4B32 B7            [ 4] 1878 	or	a, a
   4B33 C8            [11] 1879 	ret	Z
                           1880 ;src/game.c:317: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
   4B34 21 09 09      [10] 1881 	ld	hl, #0x0909
   4B37 E5            [11] 1882 	push	hl
   4B38 CD D8 60      [17] 1883 	call	_cpct_px2byteM0
   4B3B 55            [ 4] 1884 	ld	d, l
   4B3C 3A 91 62      [13] 1885 	ld	a,(#_g_checkpointy + 0)
   4B3F C6 F8         [ 7] 1886 	add	a, #0xf8
   4B41 47            [ 4] 1887 	ld	b, a
   4B42 D5            [11] 1888 	push	de
   4B43 C5            [11] 1889 	push	bc
   4B44 33            [ 6] 1890 	inc	sp
   4B45 3A 90 62      [13] 1891 	ld	a, (_g_checkpointx)
   4B48 F5            [11] 1892 	push	af
   4B49 33            [ 6] 1893 	inc	sp
   4B4A 21 00 C0      [10] 1894 	ld	hl, #0xc000
   4B4D E5            [11] 1895 	push	hl
   4B4E CD CB 61      [17] 1896 	call	_cpct_getScreenPtr
   4B51 4D            [ 4] 1897 	ld	c, l
   4B52 44            [ 4] 1898 	ld	b, h
   4B53 D1            [10] 1899 	pop	de
   4B54 21 02 08      [10] 1900 	ld	hl, #0x0802
   4B57 E5            [11] 1901 	push	hl
   4B58 D5            [11] 1902 	push	de
   4B59 33            [ 6] 1903 	inc	sp
   4B5A C5            [11] 1904 	push	bc
   4B5B CD 12 61      [17] 1905 	call	_cpct_drawSolidBox
   4B5E F1            [10] 1906 	pop	af
   4B5F F1            [10] 1907 	pop	af
   4B60 33            [ 6] 1908 	inc	sp
   4B61 C9            [10] 1909 	ret
                           1910 	.area _CODE
                           1911 	.area _INITIALIZER
                           1912 	.area _CABS (ABS)
