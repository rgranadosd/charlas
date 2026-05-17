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
                             39 	.globl _cpct_memset
                             40 	.globl _cpct_disableFirmware
                             41 	.globl _game_init
                             42 	.globl _game_update
                             43 	.globl _game_render
                             44 ;--------------------------------------------------------
                             45 ; special function registers
                             46 ;--------------------------------------------------------
                             47 ;--------------------------------------------------------
                             48 ; ram data
                             49 ;--------------------------------------------------------
                             50 	.area _DATA
   5EB8                      51 _g_player:
   5EB8                      52 	.ds 9
   5EC1                      53 _g_enemies:
   5EC1                      54 	.ds 60
   5EFD                      55 _g_projectiles:
   5EFD                      56 	.ds 60
   5F39                      57 _g_lives:
   5F39                      58 	.ds 1
   5F3A                      59 _g_score:
   5F3A                      60 	.ds 2
   5F3C                      61 _g_timeleft:
   5F3C                      62 	.ds 1
   5F3D                      63 _g_weapondisplay:
   5F3D                      64 	.ds 1
   5F3E                      65 _g_currentwave:
   5F3E                      66 	.ds 1
   5F3F                      67 _g_aliveenemies:
   5F3F                      68 	.ds 1
   5F40                      69 _g_wavecooldown:
   5F40                      70 	.ds 1
   5F41                      71 _g_damagecooldown:
   5F41                      72 	.ds 1
   5F42                      73 _g_shootcooldown:
   5F42                      74 	.ds 1
   5F43                      75 _g_victory:
   5F43                      76 	.ds 1
   5F44                      77 _g_gameover:
   5F44                      78 	.ds 1
   5F45                      79 _g_framecounter:
   5F45                      80 	.ds 2
   5F47                      81 _g_checkpointx:
   5F47                      82 	.ds 1
   5F48                      83 _g_checkpointy:
   5F48                      84 	.ds 1
   5F49                      85 _g_checkpointactive:
   5F49                      86 	.ds 1
   5F4A                      87 _g_boss:
   5F4A                      88 	.ds 10
   5F54                      89 _g_bossactive:
   5F54                      90 	.ds 1
   5F55                      91 _g_bossphase:
   5F55                      92 	.ds 1
   5F56                      93 _g_weaponlevel:
   5F56                      94 	.ds 1
   5F57                      95 _g_pickuptaken:
   5F57                      96 	.ds 1
                             97 ;--------------------------------------------------------
                             98 ; ram data
                             99 ;--------------------------------------------------------
                            100 	.area _INITIALIZED
                            101 ;--------------------------------------------------------
                            102 ; absolute external ram data
                            103 ;--------------------------------------------------------
                            104 	.area _DABS (ABS)
                            105 ;--------------------------------------------------------
                            106 ; global & static initialisations
                            107 ;--------------------------------------------------------
                            108 	.area _HOME
                            109 	.area _GSINIT
                            110 	.area _GSFINAL
                            111 	.area _GSINIT
                            112 ;--------------------------------------------------------
                            113 ; Home
                            114 ;--------------------------------------------------------
                            115 	.area _HOME
                            116 	.area _HOME
                            117 ;--------------------------------------------------------
                            118 ; code
                            119 ;--------------------------------------------------------
                            120 	.area _CODE
                            121 ;src/game.c:41: static void reset_player_to_checkpoint(void) {
                            122 ;	---------------------------------
                            123 ; Function reset_player_to_checkpoint
                            124 ; ---------------------------------
   4000                     125 _reset_player_to_checkpoint:
                            126 ;src/game.c:42: g_player.x = g_checkpointx;
   4000 21 B8 5E      [10]  127 	ld	hl, #_g_player
   4003 3A 47 5F      [13]  128 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  129 	ld	(hl), a
                            130 ;src/game.c:43: g_player.y = g_checkpointy;
   4007 21 B9 5E      [10]  131 	ld	hl, #(_g_player + 0x0001)
   400A 3A 48 5F      [13]  132 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  133 	ld	(hl), a
                            134 ;src/game.c:44: g_player.vx = 0;
   400E 21 BA 5E      [10]  135 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  136 	ld	(hl), #0x00
                            137 ;src/game.c:45: g_player.vy = 0;
   4013 21 BB 5E      [10]  138 	ld	hl, #(_g_player + 0x0003)
   4016 36 00         [10]  139 	ld	(hl), #0x00
   4018 C9            [10]  140 	ret
                            141 ;src/game.c:48: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
                            142 ;	---------------------------------
                            143 ; Function rect_overlap
                            144 ; ---------------------------------
   4019                     145 _rect_overlap:
   4019 DD E5         [15]  146 	push	ix
   401B DD 21 00 00   [14]  147 	ld	ix,#0
   401F DD 39         [15]  148 	add	ix,sp
                            149 ;src/game.c:49: if (ax + aw <= bx) return 0;
   4021 DD 4E 08      [19]  150 	ld	c, 8 (ix)
   4024 06 00         [ 7]  151 	ld	b, #0x00
   4026 DD 6E 04      [19]  152 	ld	l,4 (ix)
   4029 DD 66 05      [19]  153 	ld	h,5 (ix)
   402C 09            [11]  154 	add	hl, bc
   402D DD 7E 0A      [19]  155 	ld	a, 10 (ix)
   4030 95            [ 4]  156 	sub	a, l
   4031 DD 7E 0B      [19]  157 	ld	a, 11 (ix)
   4034 9C            [ 4]  158 	sbc	a, h
   4035 E2 3A 40      [10]  159 	jp	PO, 00127$
   4038 EE 80         [ 7]  160 	xor	a, #0x80
   403A                     161 00127$:
   403A FA 41 40      [10]  162 	jp	M, 00102$
   403D 2E 00         [ 7]  163 	ld	l, #0x00
   403F 18 62         [12]  164 	jr	00109$
   4041                     165 00102$:
                            166 ;src/game.c:50: if (bx + bw <= ax) return 0;
   4041 DD 4E 0E      [19]  167 	ld	c, 14 (ix)
   4044 06 00         [ 7]  168 	ld	b, #0x00
   4046 DD 6E 0A      [19]  169 	ld	l,10 (ix)
   4049 DD 66 0B      [19]  170 	ld	h,11 (ix)
   404C 09            [11]  171 	add	hl, bc
   404D DD 7E 04      [19]  172 	ld	a, 4 (ix)
   4050 95            [ 4]  173 	sub	a, l
   4051 DD 7E 05      [19]  174 	ld	a, 5 (ix)
   4054 9C            [ 4]  175 	sbc	a, h
   4055 E2 5A 40      [10]  176 	jp	PO, 00128$
   4058 EE 80         [ 7]  177 	xor	a, #0x80
   405A                     178 00128$:
   405A FA 61 40      [10]  179 	jp	M, 00104$
   405D 2E 00         [ 7]  180 	ld	l, #0x00
   405F 18 42         [12]  181 	jr	00109$
   4061                     182 00104$:
                            183 ;src/game.c:51: if (ay + ah <= by) return 0;
   4061 DD 4E 09      [19]  184 	ld	c, 9 (ix)
   4064 06 00         [ 7]  185 	ld	b, #0x00
   4066 DD 6E 06      [19]  186 	ld	l,6 (ix)
   4069 DD 66 07      [19]  187 	ld	h,7 (ix)
   406C 09            [11]  188 	add	hl, bc
   406D DD 7E 0C      [19]  189 	ld	a, 12 (ix)
   4070 95            [ 4]  190 	sub	a, l
   4071 DD 7E 0D      [19]  191 	ld	a, 13 (ix)
   4074 9C            [ 4]  192 	sbc	a, h
   4075 E2 7A 40      [10]  193 	jp	PO, 00129$
   4078 EE 80         [ 7]  194 	xor	a, #0x80
   407A                     195 00129$:
   407A FA 81 40      [10]  196 	jp	M, 00106$
   407D 2E 00         [ 7]  197 	ld	l, #0x00
   407F 18 22         [12]  198 	jr	00109$
   4081                     199 00106$:
                            200 ;src/game.c:52: if (by + bh <= ay) return 0;
   4081 DD 4E 0F      [19]  201 	ld	c, 15 (ix)
   4084 06 00         [ 7]  202 	ld	b, #0x00
   4086 DD 6E 0C      [19]  203 	ld	l,12 (ix)
   4089 DD 66 0D      [19]  204 	ld	h,13 (ix)
   408C 09            [11]  205 	add	hl, bc
   408D DD 7E 06      [19]  206 	ld	a, 6 (ix)
   4090 95            [ 4]  207 	sub	a, l
   4091 DD 7E 07      [19]  208 	ld	a, 7 (ix)
   4094 9C            [ 4]  209 	sbc	a, h
   4095 E2 9A 40      [10]  210 	jp	PO, 00130$
   4098 EE 80         [ 7]  211 	xor	a, #0x80
   409A                     212 00130$:
   409A FA A1 40      [10]  213 	jp	M, 00108$
   409D 2E 00         [ 7]  214 	ld	l, #0x00
   409F 18 02         [12]  215 	jr	00109$
   40A1                     216 00108$:
                            217 ;src/game.c:53: return 1;
   40A1 2E 01         [ 7]  218 	ld	l, #0x01
   40A3                     219 00109$:
   40A3 DD E1         [14]  220 	pop	ix
   40A5 C9            [10]  221 	ret
                            222 ;src/game.c:56: static void spawn_wave(u8 wave) {
                            223 ;	---------------------------------
                            224 ; Function spawn_wave
                            225 ; ---------------------------------
   40A6                     226 _spawn_wave:
   40A6 DD E5         [15]  227 	push	ix
   40A8 DD 21 00 00   [14]  228 	ld	ix,#0
   40AC DD 39         [15]  229 	add	ix,sp
   40AE F5            [11]  230 	push	af
   40AF F5            [11]  231 	push	af
   40B0 3B            [ 6]  232 	dec	sp
                            233 ;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
   40B1 01 C1 5E      [10]  234 	ld	bc, #_g_enemies+0
   40B4 1E 00         [ 7]  235 	ld	e, #0x00
   40B6                     236 00117$:
                            237 ;src/game.c:61: enemyinit(&g_enemies[i]);
   40B6 D5            [11]  238 	push	de
   40B7 16 00         [ 7]  239 	ld	d,#0x00
   40B9 6B            [ 4]  240 	ld	l, e
   40BA 62            [ 4]  241 	ld	h, d
   40BB 29            [11]  242 	add	hl, hl
   40BC 29            [11]  243 	add	hl, hl
   40BD 19            [11]  244 	add	hl, de
   40BE 29            [11]  245 	add	hl, hl
   40BF D1            [10]  246 	pop	de
   40C0 09            [11]  247 	add	hl, bc
   40C1 C5            [11]  248 	push	bc
   40C2 D5            [11]  249 	push	de
   40C3 E5            [11]  250 	push	hl
   40C4 CD 72 51      [17]  251 	call	_enemyinit
   40C7 F1            [10]  252 	pop	af
   40C8 D1            [10]  253 	pop	de
   40C9 C1            [10]  254 	pop	bc
                            255 ;src/game.c:60: for (i = 0; i < MAX_ENEMIES; ++i) {
   40CA 1C            [ 4]  256 	inc	e
   40CB 7B            [ 4]  257 	ld	a, e
   40CC D6 06         [ 7]  258 	sub	a, #0x06
   40CE 38 E6         [12]  259 	jr	C,00117$
                            260 ;src/game.c:65: else if (wave == 1) count = 3;
   40D0 DD 7E 04      [19]  261 	ld	a, 4 (ix)
   40D3 3D            [ 4]  262 	dec	a
   40D4 20 04         [12]  263 	jr	NZ,00190$
   40D6 3E 01         [ 7]  264 	ld	a,#0x01
   40D8 18 01         [12]  265 	jr	00191$
   40DA                     266 00190$:
   40DA AF            [ 4]  267 	xor	a,a
   40DB                     268 00191$:
   40DB 5F            [ 4]  269 	ld	e, a
                            270 ;src/game.c:64: if (wave == 0) count = 2;
   40DC DD 7E 04      [19]  271 	ld	a, 4 (ix)
   40DF B7            [ 4]  272 	or	a, a
   40E0 20 06         [12]  273 	jr	NZ,00106$
   40E2 DD 36 FB 02   [19]  274 	ld	-5 (ix), #0x02
   40E6 18 0E         [12]  275 	jr	00107$
   40E8                     276 00106$:
                            277 ;src/game.c:65: else if (wave == 1) count = 3;
   40E8 7B            [ 4]  278 	ld	a, e
   40E9 B7            [ 4]  279 	or	a, a
   40EA 28 06         [12]  280 	jr	Z,00103$
   40EC DD 36 FB 03   [19]  281 	ld	-5 (ix), #0x03
   40F0 18 04         [12]  282 	jr	00107$
   40F2                     283 00103$:
                            284 ;src/game.c:66: else count = 4;
   40F2 DD 36 FB 04   [19]  285 	ld	-5 (ix), #0x04
   40F6                     286 00107$:
                            287 ;src/game.c:68: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F6 3E 06         [ 7]  288 	ld	a, #0x06
   40F8 DD 96 FB      [19]  289 	sub	a, -5 (ix)
   40FB 30 04         [12]  290 	jr	NC,00148$
   40FD DD 36 FB 06   [19]  291 	ld	-5 (ix), #0x06
                            292 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4101                     293 00148$:
   4101 DD 73 FF      [19]  294 	ld	-1 (ix), e
   4104 DD 36 FC 00   [19]  295 	ld	-4 (ix), #0x00
   4108                     296 00120$:
   4108 DD 7E FC      [19]  297 	ld	a, -4 (ix)
   410B DD 96 FB      [19]  298 	sub	a, -5 (ix)
   410E D2 9B 41      [10]  299 	jp	NC, 00116$
                            300 ;src/game.c:73: if (wave == 0) type = 0;
   4111 DD 7E 04      [19]  301 	ld	a, 4 (ix)
   4114 B7            [ 4]  302 	or	a,a
   4115 20 03         [12]  303 	jr	NZ,00114$
   4117 5F            [ 4]  304 	ld	e,a
   4118 18 27         [12]  305 	jr	00115$
   411A                     306 00114$:
                            307 ;src/game.c:74: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
   411A DD 7E FF      [19]  308 	ld	a, -1 (ix)
   411D B7            [ 4]  309 	or	a, a
   411E 28 0E         [12]  310 	jr	Z,00111$
   4120 DD 7E FC      [19]  311 	ld	a, -4 (ix)
   4123 B7            [ 4]  312 	or	a, a
   4124 20 04         [12]  313 	jr	NZ,00124$
   4126 1E 01         [ 7]  314 	ld	e, #0x01
   4128 18 17         [12]  315 	jr	00115$
   412A                     316 00124$:
   412A 1E 00         [ 7]  317 	ld	e, #0x00
   412C 18 13         [12]  318 	jr	00115$
   412E                     319 00111$:
                            320 ;src/game.c:75: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   412E DD 7E FC      [19]  321 	ld	a, -4 (ix)
   4131 B7            [ 4]  322 	or	a, a
   4132 28 07         [12]  323 	jr	Z,00129$
   4134 DD 7E FC      [19]  324 	ld	a, -4 (ix)
   4137 D6 03         [ 7]  325 	sub	a, #0x03
   4139 20 04         [12]  326 	jr	NZ,00126$
   413B                     327 00129$:
   413B 1E 02         [ 7]  328 	ld	e, #0x02
   413D 18 02         [12]  329 	jr	00127$
   413F                     330 00126$:
   413F 1E 01         [ 7]  331 	ld	e, #0x01
   4141                     332 00127$:
   4141                     333 00115$:
                            334 ;src/game.c:77: spawn_y = (type == 2) ? 84 : 112;
   4141 7B            [ 4]  335 	ld	a, e
   4142 D6 02         [ 7]  336 	sub	a, #0x02
   4144 20 04         [12]  337 	jr	NZ,00131$
   4146 16 54         [ 7]  338 	ld	d, #0x54
   4148 18 02         [12]  339 	jr	00132$
   414A                     340 00131$:
   414A 16 70         [ 7]  341 	ld	d, #0x70
   414C                     342 00132$:
                            343 ;src/game.c:78: enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));
   414C DD CB FC 46   [20]  344 	bit	0, -4 (ix)
   4150 28 06         [12]  345 	jr	Z,00133$
   4152 DD 36 FE 01   [19]  346 	ld	-2 (ix), #0x01
   4156 18 04         [12]  347 	jr	00134$
   4158                     348 00133$:
   4158 DD 36 FE 00   [19]  349 	ld	-2 (ix), #0x00
   415C                     350 00134$:
   415C DD 7E FC      [19]  351 	ld	a, -4 (ix)
   415F 07            [ 4]  352 	rlca
   4160 07            [ 4]  353 	rlca
   4161 07            [ 4]  354 	rlca
   4162 E6 F8         [ 7]  355 	and	a, #0xf8
   4164 C6 2E         [ 7]  356 	add	a, #0x2e
   4166 DD 77 FD      [19]  357 	ld	-3 (ix), a
   4169 D5            [11]  358 	push	de
   416A DD 5E FC      [19]  359 	ld	e,-4 (ix)
   416D 16 00         [ 7]  360 	ld	d,#0x00
   416F 6B            [ 4]  361 	ld	l, e
   4170 62            [ 4]  362 	ld	h, d
   4171 29            [11]  363 	add	hl, hl
   4172 29            [11]  364 	add	hl, hl
   4173 19            [11]  365 	add	hl, de
   4174 29            [11]  366 	add	hl, hl
   4175 D1            [10]  367 	pop	de
   4176 09            [11]  368 	add	hl, bc
   4177 E5            [11]  369 	push	hl
   4178 FD E1         [14]  370 	pop	iy
   417A C5            [11]  371 	push	bc
   417B DD 7E FE      [19]  372 	ld	a, -2 (ix)
   417E F5            [11]  373 	push	af
   417F 33            [ 6]  374 	inc	sp
   4180 7B            [ 4]  375 	ld	a, e
   4181 F5            [11]  376 	push	af
   4182 33            [ 6]  377 	inc	sp
   4183 D5            [11]  378 	push	de
   4184 33            [ 6]  379 	inc	sp
   4185 DD 7E FD      [19]  380 	ld	a, -3 (ix)
   4188 F5            [11]  381 	push	af
   4189 33            [ 6]  382 	inc	sp
   418A FD E5         [15]  383 	push	iy
   418C CD B7 51      [17]  384 	call	_enemyspawn
   418F 21 06 00      [10]  385 	ld	hl, #6
   4192 39            [11]  386 	add	hl, sp
   4193 F9            [ 6]  387 	ld	sp, hl
   4194 C1            [10]  388 	pop	bc
                            389 ;src/game.c:70: for (i = 0; i < count; ++i) {
   4195 DD 34 FC      [23]  390 	inc	-4 (ix)
   4198 C3 08 41      [10]  391 	jp	00120$
   419B                     392 00116$:
                            393 ;src/game.c:81: g_aliveenemies = count;
   419B DD 7E FB      [19]  394 	ld	a, -5 (ix)
   419E 32 3F 5F      [13]  395 	ld	(#_g_aliveenemies + 0),a
   41A1 DD F9         [10]  396 	ld	sp, ix
   41A3 DD E1         [14]  397 	pop	ix
   41A5 C9            [10]  398 	ret
                            399 ;src/game.c:84: static void spawn_boss(void) {
                            400 ;	---------------------------------
                            401 ; Function spawn_boss
                            402 ; ---------------------------------
   41A6                     403 _spawn_boss:
                            404 ;src/game.c:85: enemyinit(&g_boss);
   41A6 21 4A 5F      [10]  405 	ld	hl, #_g_boss
   41A9 E5            [11]  406 	push	hl
   41AA CD 72 51      [17]  407 	call	_enemyinit
   41AD F1            [10]  408 	pop	af
                            409 ;src/game.c:86: enemyspawn(&g_boss, 68, 112, 1, 0);
   41AE 21 01 00      [10]  410 	ld	hl, #0x0001
   41B1 E5            [11]  411 	push	hl
   41B2 21 44 70      [10]  412 	ld	hl, #0x7044
   41B5 E5            [11]  413 	push	hl
   41B6 21 4A 5F      [10]  414 	ld	hl, #_g_boss
   41B9 E5            [11]  415 	push	hl
   41BA CD B7 51      [17]  416 	call	_enemyspawn
   41BD 21 06 00      [10]  417 	ld	hl, #6
   41C0 39            [11]  418 	add	hl, sp
   41C1 F9            [ 6]  419 	ld	sp, hl
                            420 ;src/game.c:87: g_boss.w = 10;
   41C2 21 4E 5F      [10]  421 	ld	hl, #(_g_boss + 0x0004)
   41C5 36 0A         [10]  422 	ld	(hl), #0x0a
                            423 ;src/game.c:88: g_boss.h = 18;
   41C7 21 4F 5F      [10]  424 	ld	hl, #(_g_boss + 0x0005)
   41CA 36 12         [10]  425 	ld	(hl), #0x12
                            426 ;src/game.c:89: g_boss.health = 10;
   41CC 21 51 5F      [10]  427 	ld	hl, #(_g_boss + 0x0007)
   41CF 36 0A         [10]  428 	ld	(hl), #0x0a
                            429 ;src/game.c:90: g_boss.reward = 1500;
   41D1 21 52 5F      [10]  430 	ld	hl, #(_g_boss + 0x0008)
   41D4 36 DC         [10]  431 	ld	(hl), #0xdc
                            432 ;src/game.c:91: g_boss.kind = 3;
   41D6 21 53 5F      [10]  433 	ld	hl, #(_g_boss + 0x0009)
   41D9 36 03         [10]  434 	ld	(hl), #0x03
                            435 ;src/game.c:92: g_boss.vx = -1;
   41DB 21 4C 5F      [10]  436 	ld	hl, #(_g_boss + 0x0002)
   41DE 36 FF         [10]  437 	ld	(hl), #0xff
                            438 ;src/game.c:93: g_bossactive = 1;
   41E0 21 54 5F      [10]  439 	ld	hl,#_g_bossactive + 0
   41E3 36 01         [10]  440 	ld	(hl), #0x01
                            441 ;src/game.c:94: g_bossphase = 0;
   41E5 21 55 5F      [10]  442 	ld	hl,#_g_bossphase + 0
   41E8 36 00         [10]  443 	ld	(hl), #0x00
   41EA C9            [10]  444 	ret
                            445 ;src/game.c:97: static void try_fire_projectile(void) {
                            446 ;	---------------------------------
                            447 ; Function try_fire_projectile
                            448 ; ---------------------------------
   41EB                     449 _try_fire_projectile:
   41EB DD E5         [15]  450 	push	ix
   41ED DD 21 00 00   [14]  451 	ld	ix,#0
   41F1 DD 39         [15]  452 	add	ix,sp
   41F3 F5            [11]  453 	push	af
   41F4 3B            [ 6]  454 	dec	sp
                            455 ;src/game.c:101: if (!input_is_shoot_just_pressed()) return;
   41F5 CD C5 4F      [17]  456 	call	_input_is_shoot_just_pressed
   41F8 7D            [ 4]  457 	ld	a, l
   41F9 B7            [ 4]  458 	or	a, a
   41FA CA 8C 42      [10]  459 	jp	Z,00110$
                            460 ;src/game.c:102: if (g_shootcooldown) return;
   41FD 3A 42 5F      [13]  461 	ld	a,(#_g_shootcooldown + 0)
   4200 B7            [ 4]  462 	or	a, a
   4201 C2 8C 42      [10]  463 	jp	NZ,00110$
                            464 ;src/game.c:104: dir = g_player.facing_left ? -3 : 3;
   4204 3A BF 5E      [13]  465 	ld	a, (#_g_player + 7)
   4207 B7            [ 4]  466 	or	a, a
   4208 28 04         [12]  467 	jr	Z,00112$
   420A 0E FD         [ 7]  468 	ld	c, #0xfd
   420C 18 02         [12]  469 	jr	00113$
   420E                     470 00112$:
   420E 0E 03         [ 7]  471 	ld	c, #0x03
   4210                     472 00113$:
                            473 ;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4210 DD 36 FF 00   [19]  474 	ld	-1 (ix), #0x00
   4214 06 00         [ 7]  475 	ld	b, #0x00
   4216                     476 00108$:
                            477 ;src/game.c:107: if (!g_projectiles[i].active) {
   4216 58            [ 4]  478 	ld	e,b
   4217 16 00         [ 7]  479 	ld	d,#0x00
   4219 6B            [ 4]  480 	ld	l, e
   421A 62            [ 4]  481 	ld	h, d
   421B 29            [11]  482 	add	hl, hl
   421C 29            [11]  483 	add	hl, hl
   421D 19            [11]  484 	add	hl, de
   421E 29            [11]  485 	add	hl, hl
   421F 11 FD 5E      [10]  486 	ld	de, #_g_projectiles
   4222 19            [11]  487 	add	hl, de
   4223 11 06 00      [10]  488 	ld	de, #0x0006
   4226 19            [11]  489 	add	hl, de
   4227 7E            [ 7]  490 	ld	a, (hl)
   4228 B7            [ 4]  491 	or	a, a
   4229 20 58         [12]  492 	jr	NZ,00109$
                            493 ;src/game.c:109: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
   422B 3A 56 5F      [13]  494 	ld	a,(#_g_weaponlevel + 0)
   422E B7            [ 4]  495 	or	a, a
   422F 28 06         [12]  496 	jr	Z,00114$
   4231 DD 36 FE 01   [19]  497 	ld	-2 (ix), #0x01
   4235 18 04         [12]  498 	jr	00115$
   4237                     499 00114$:
   4237 DD 36 FE 00   [19]  500 	ld	-2 (ix), #0x00
   423B                     501 00115$:
   423B 3A B9 5E      [13]  502 	ld	a, (#_g_player + 1)
   423E C6 06         [ 7]  503 	add	a, #0x06
   4240 DD 77 FD      [19]  504 	ld	-3 (ix), a
   4243 21 B8 5E      [10]  505 	ld	hl, #_g_player + 0
   4246 46            [ 7]  506 	ld	b, (hl)
   4247 04            [ 4]  507 	inc	b
   4248 04            [ 4]  508 	inc	b
   4249 DD 5E FF      [19]  509 	ld	e,-1 (ix)
   424C 16 00         [ 7]  510 	ld	d,#0x00
   424E 6B            [ 4]  511 	ld	l, e
   424F 62            [ 4]  512 	ld	h, d
   4250 29            [11]  513 	add	hl, hl
   4251 29            [11]  514 	add	hl, hl
   4252 19            [11]  515 	add	hl, de
   4253 29            [11]  516 	add	hl, hl
   4254 11 FD 5E      [10]  517 	ld	de, #_g_projectiles
   4257 19            [11]  518 	add	hl, de
   4258 EB            [ 4]  519 	ex	de,hl
   4259 DD 7E FE      [19]  520 	ld	a, -2 (ix)
   425C F5            [11]  521 	push	af
   425D 33            [ 6]  522 	inc	sp
   425E 79            [ 4]  523 	ld	a, c
   425F F5            [11]  524 	push	af
   4260 33            [ 6]  525 	inc	sp
   4261 DD 7E FD      [19]  526 	ld	a, -3 (ix)
   4264 F5            [11]  527 	push	af
   4265 33            [ 6]  528 	inc	sp
   4266 C5            [11]  529 	push	bc
   4267 33            [ 6]  530 	inc	sp
   4268 D5            [11]  531 	push	de
   4269 CD 84 5A      [17]  532 	call	_projectilefire
   426C 21 06 00      [10]  533 	ld	hl, #6
   426F 39            [11]  534 	add	hl, sp
   4270 F9            [ 6]  535 	ld	sp, hl
                            536 ;src/game.c:110: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
   4271 3A 56 5F      [13]  537 	ld	a,(#_g_weaponlevel + 0)
   4274 B7            [ 4]  538 	or	a, a
   4275 28 04         [12]  539 	jr	Z,00116$
   4277 0E 04         [ 7]  540 	ld	c, #0x04
   4279 18 02         [12]  541 	jr	00117$
   427B                     542 00116$:
   427B 0E 08         [ 7]  543 	ld	c, #0x08
   427D                     544 00117$:
   427D 21 42 5F      [10]  545 	ld	hl,#_g_shootcooldown + 0
   4280 71            [ 7]  546 	ld	(hl), c
                            547 ;src/game.c:111: break;
   4281 18 09         [12]  548 	jr	00110$
   4283                     549 00109$:
                            550 ;src/game.c:106: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4283 04            [ 4]  551 	inc	b
   4284 DD 70 FF      [19]  552 	ld	-1 (ix), b
   4287 78            [ 4]  553 	ld	a, b
   4288 D6 06         [ 7]  554 	sub	a, #0x06
   428A 38 8A         [12]  555 	jr	C,00108$
   428C                     556 00110$:
   428C DD F9         [10]  557 	ld	sp, ix
   428E DD E1         [14]  558 	pop	ix
   4290 C9            [10]  559 	ret
                            560 ;src/game.c:116: static void register_player_hit(void) {
                            561 ;	---------------------------------
                            562 ; Function register_player_hit
                            563 ; ---------------------------------
   4291                     564 _register_player_hit:
                            565 ;src/game.c:117: if (g_lives) {
   4291 FD 21 39 5F   [14]  566 	ld	iy, #_g_lives
   4295 FD 7E 00      [19]  567 	ld	a, 0 (iy)
   4298 B7            [ 4]  568 	or	a, a
   4299 28 03         [12]  569 	jr	Z,00102$
                            570 ;src/game.c:118: g_lives--;
   429B FD 35 00      [23]  571 	dec	0 (iy)
   429E                     572 00102$:
                            573 ;src/game.c:120: if (g_lives == 0) {
   429E 3A 39 5F      [13]  574 	ld	a,(#_g_lives + 0)
   42A1 B7            [ 4]  575 	or	a, a
   42A2 20 06         [12]  576 	jr	NZ,00104$
                            577 ;src/game.c:121: g_gameover = 1;
   42A4 21 44 5F      [10]  578 	ld	hl,#_g_gameover + 0
   42A7 36 01         [10]  579 	ld	(hl), #0x01
                            580 ;src/game.c:122: return;
   42A9 C9            [10]  581 	ret
   42AA                     582 00104$:
                            583 ;src/game.c:125: reset_player_to_checkpoint();
   42AA CD 00 40      [17]  584 	call	_reset_player_to_checkpoint
                            585 ;src/game.c:126: g_damagecooldown = 40;
   42AD 21 41 5F      [10]  586 	ld	hl,#_g_damagecooldown + 0
   42B0 36 28         [10]  587 	ld	(hl), #0x28
   42B2 C9            [10]  588 	ret
                            589 ;src/game.c:129: void game_init(void) {
                            590 ;	---------------------------------
                            591 ; Function game_init
                            592 ; ---------------------------------
   42B3                     593 _game_init::
                            594 ;src/game.c:132: cpct_disableFirmware();
   42B3 CD CF 5D      [17]  595 	call	_cpct_disableFirmware
                            596 ;src/game.c:133: cpct_setVideoMode(1);
   42B6 2E 01         [ 7]  597 	ld	l, #0x01
   42B8 CD B3 5D      [17]  598 	call	_cpct_setVideoMode
                            599 ;src/game.c:134: cpct_setPalette((u8*)gpalette16, 16);
   42BB 21 10 00      [10]  600 	ld	hl, #0x0010
   42BE E5            [11]  601 	push	hl
   42BF 21 54 51      [10]  602 	ld	hl, #_gpalette16
   42C2 E5            [11]  603 	push	hl
   42C3 CD C2 5C      [17]  604 	call	_cpct_setPalette
                            605 ;src/game.c:135: cpct_setBorder(gpalette16[0]);
   42C6 21 54 51      [10]  606 	ld	hl, #_gpalette16 + 0
   42C9 46            [ 7]  607 	ld	b, (hl)
   42CA C5            [11]  608 	push	bc
   42CB 33            [ 6]  609 	inc	sp
   42CC 3E 10         [ 7]  610 	ld	a, #0x10
   42CE F5            [11]  611 	push	af
   42CF 33            [ 6]  612 	inc	sp
   42D0 CD D9 5C      [17]  613 	call	_cpct_setPALColour
                            614 ;src/game.c:136: cpct_clearScreen(0x00);
   42D3 21 00 40      [10]  615 	ld	hl, #0x4000
   42D6 E5            [11]  616 	push	hl
   42D7 AF            [ 4]  617 	xor	a, a
   42D8 F5            [11]  618 	push	af
   42D9 33            [ 6]  619 	inc	sp
   42DA 26 C0         [ 7]  620 	ld	h, #0xc0
   42DC E5            [11]  621 	push	hl
   42DD CD C1 5D      [17]  622 	call	_cpct_memset
                            623 ;src/game.c:137: tilemap_init();
   42E0 CD D7 4F      [17]  624 	call	_tilemap_init
                            625 ;src/game.c:138: collision_init();
   42E3 CD 1B 4B      [17]  626 	call	_collision_init
                            627 ;src/game.c:139: playerinit(&g_player);
   42E6 21 B8 5E      [10]  628 	ld	hl, #_g_player
   42E9 E5            [11]  629 	push	hl
   42EA CD 45 56      [17]  630 	call	_playerinit
   42ED F1            [10]  631 	pop	af
                            632 ;src/game.c:140: hudinit();
   42EE CD 21 4E      [17]  633 	call	_hudinit
                            634 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42F1 0E 00         [ 7]  635 	ld	c, #0x00
   42F3                     636 00102$:
                            637 ;src/game.c:143: projectileinit(&g_projectiles[i]);
   42F3 06 00         [ 7]  638 	ld	b,#0x00
   42F5 69            [ 4]  639 	ld	l, c
   42F6 60            [ 4]  640 	ld	h, b
   42F7 29            [11]  641 	add	hl, hl
   42F8 29            [11]  642 	add	hl, hl
   42F9 09            [11]  643 	add	hl, bc
   42FA 29            [11]  644 	add	hl, hl
   42FB 11 FD 5E      [10]  645 	ld	de, #_g_projectiles
   42FE 19            [11]  646 	add	hl, de
   42FF C5            [11]  647 	push	bc
   4300 E5            [11]  648 	push	hl
   4301 CD 3F 5A      [17]  649 	call	_projectileinit
   4304 F1            [10]  650 	pop	af
   4305 C1            [10]  651 	pop	bc
                            652 ;src/game.c:142: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4306 0C            [ 4]  653 	inc	c
   4307 79            [ 4]  654 	ld	a, c
   4308 D6 06         [ 7]  655 	sub	a, #0x06
   430A 38 E7         [12]  656 	jr	C,00102$
                            657 ;src/game.c:146: g_lives = 3;
   430C 21 39 5F      [10]  658 	ld	hl,#_g_lives + 0
   430F 36 03         [10]  659 	ld	(hl), #0x03
                            660 ;src/game.c:147: g_score = 0;
   4311 21 00 00      [10]  661 	ld	hl, #0x0000
   4314 22 3A 5F      [16]  662 	ld	(_g_score), hl
                            663 ;src/game.c:148: g_timeleft = 99;
   4317 FD 21 3C 5F   [14]  664 	ld	iy, #_g_timeleft
   431B FD 36 00 63   [19]  665 	ld	0 (iy), #0x63
                            666 ;src/game.c:149: g_weapondisplay = 1;
   431F FD 21 3D 5F   [14]  667 	ld	iy, #_g_weapondisplay
   4323 FD 36 00 01   [19]  668 	ld	0 (iy), #0x01
                            669 ;src/game.c:150: g_currentwave = 0;
   4327 FD 21 3E 5F   [14]  670 	ld	iy, #_g_currentwave
   432B FD 36 00 00   [19]  671 	ld	0 (iy), #0x00
                            672 ;src/game.c:151: g_wavecooldown = 1;
   432F FD 21 40 5F   [14]  673 	ld	iy, #_g_wavecooldown
   4333 FD 36 00 01   [19]  674 	ld	0 (iy), #0x01
                            675 ;src/game.c:152: g_damagecooldown = 0;
   4337 FD 21 41 5F   [14]  676 	ld	iy, #_g_damagecooldown
   433B FD 36 00 00   [19]  677 	ld	0 (iy), #0x00
                            678 ;src/game.c:153: g_shootcooldown = 0;
   433F FD 21 42 5F   [14]  679 	ld	iy, #_g_shootcooldown
   4343 FD 36 00 00   [19]  680 	ld	0 (iy), #0x00
                            681 ;src/game.c:154: g_victory = 0;
   4347 FD 21 43 5F   [14]  682 	ld	iy, #_g_victory
   434B FD 36 00 00   [19]  683 	ld	0 (iy), #0x00
                            684 ;src/game.c:155: g_gameover = 0;
   434F FD 21 44 5F   [14]  685 	ld	iy, #_g_gameover
   4353 FD 36 00 00   [19]  686 	ld	0 (iy), #0x00
                            687 ;src/game.c:156: g_framecounter = 0;
   4357 2E 00         [ 7]  688 	ld	l, #0x00
   4359 22 45 5F      [16]  689 	ld	(_g_framecounter), hl
                            690 ;src/game.c:157: g_checkpointx = 20;
   435C 21 47 5F      [10]  691 	ld	hl,#_g_checkpointx + 0
   435F 36 14         [10]  692 	ld	(hl), #0x14
                            693 ;src/game.c:158: g_checkpointy = 120;
   4361 21 48 5F      [10]  694 	ld	hl,#_g_checkpointy + 0
   4364 36 78         [10]  695 	ld	(hl), #0x78
                            696 ;src/game.c:159: g_checkpointactive = 0;
   4366 21 49 5F      [10]  697 	ld	hl,#_g_checkpointactive + 0
   4369 36 00         [10]  698 	ld	(hl), #0x00
                            699 ;src/game.c:160: g_bossactive = 0;
   436B 21 54 5F      [10]  700 	ld	hl,#_g_bossactive + 0
   436E 36 00         [10]  701 	ld	(hl), #0x00
                            702 ;src/game.c:161: g_weaponlevel = 0;
   4370 21 56 5F      [10]  703 	ld	hl,#_g_weaponlevel + 0
   4373 36 00         [10]  704 	ld	(hl), #0x00
                            705 ;src/game.c:162: g_pickuptaken = 0;
   4375 21 57 5F      [10]  706 	ld	hl,#_g_pickuptaken + 0
   4378 36 00         [10]  707 	ld	(hl), #0x00
                            708 ;src/game.c:163: enemyinit(&g_boss);
   437A 21 4A 5F      [10]  709 	ld	hl, #_g_boss
   437D E5            [11]  710 	push	hl
   437E CD 72 51      [17]  711 	call	_enemyinit
   4381 F1            [10]  712 	pop	af
   4382 C9            [10]  713 	ret
                            714 ;src/game.c:166: void game_update(void) {
                            715 ;	---------------------------------
                            716 ; Function game_update
                            717 ; ---------------------------------
   4383                     718 _game_update::
   4383 DD E5         [15]  719 	push	ix
   4385 DD 21 00 00   [14]  720 	ld	ix,#0
   4389 DD 39         [15]  721 	add	ix,sp
   438B 21 E7 FF      [10]  722 	ld	hl, #-25
   438E 39            [11]  723 	add	hl, sp
   438F F9            [ 6]  724 	ld	sp, hl
                            725 ;src/game.c:170: input_update();
   4390 CD 32 4F      [17]  726 	call	_input_update
                            727 ;src/game.c:172: if (g_gameover || g_victory) {
   4393 3A 44 5F      [13]  728 	ld	a,(#_g_gameover + 0)
   4396 B7            [ 4]  729 	or	a, a
   4397 20 06         [12]  730 	jr	NZ,00101$
   4399 3A 43 5F      [13]  731 	ld	a,(#_g_victory + 0)
   439C B7            [ 4]  732 	or	a, a
   439D 28 1C         [12]  733 	jr	Z,00102$
   439F                     734 00101$:
                            735 ;src/game.c:173: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   439F 3A 3D 5F      [13]  736 	ld	a, (_g_weapondisplay)
   43A2 F5            [11]  737 	push	af
   43A3 33            [ 6]  738 	inc	sp
   43A4 3A 3C 5F      [13]  739 	ld	a, (_g_timeleft)
   43A7 F5            [11]  740 	push	af
   43A8 33            [ 6]  741 	inc	sp
   43A9 2A 3A 5F      [16]  742 	ld	hl, (_g_score)
   43AC E5            [11]  743 	push	hl
   43AD 3A 39 5F      [13]  744 	ld	a, (_g_lives)
   43B0 F5            [11]  745 	push	af
   43B1 33            [ 6]  746 	inc	sp
   43B2 CD 3C 4E      [17]  747 	call	_hudupdate
   43B5 F1            [10]  748 	pop	af
   43B6 F1            [10]  749 	pop	af
   43B7 33            [ 6]  750 	inc	sp
                            751 ;src/game.c:174: return;
   43B8 C3 A6 49      [10]  752 	jp	00181$
   43BB                     753 00102$:
                            754 ;src/game.c:177: playerupdate(&g_player);
   43BB 21 B8 5E      [10]  755 	ld	hl, #_g_player
   43BE E5            [11]  756 	push	hl
   43BF CD 8C 56      [17]  757 	call	_playerupdate
   43C2 F1            [10]  758 	pop	af
                            759 ;src/game.c:178: try_fire_projectile();
   43C3 CD EB 41      [17]  760 	call	_try_fire_projectile
                            761 ;src/game.c:180: if (g_shootcooldown) g_shootcooldown--;
   43C6 FD 21 42 5F   [14]  762 	ld	iy, #_g_shootcooldown
   43CA FD 7E 00      [19]  763 	ld	a, 0 (iy)
   43CD B7            [ 4]  764 	or	a, a
   43CE 28 03         [12]  765 	jr	Z,00105$
   43D0 FD 35 00      [23]  766 	dec	0 (iy)
   43D3                     767 00105$:
                            768 ;src/game.c:181: if (g_damagecooldown) g_damagecooldown--;
   43D3 FD 21 41 5F   [14]  769 	ld	iy, #_g_damagecooldown
   43D7 FD 7E 00      [19]  770 	ld	a, 0 (iy)
   43DA B7            [ 4]  771 	or	a, a
   43DB 28 03         [12]  772 	jr	Z,00192$
   43DD FD 35 00      [23]  773 	dec	0 (iy)
                            774 ;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43E0                     775 00192$:
   43E0 0E 00         [ 7]  776 	ld	c, #0x00
   43E2                     777 00174$:
                            778 ;src/game.c:184: projectileupdate(&g_projectiles[i]);
   43E2 06 00         [ 7]  779 	ld	b,#0x00
   43E4 69            [ 4]  780 	ld	l, c
   43E5 60            [ 4]  781 	ld	h, b
   43E6 29            [11]  782 	add	hl, hl
   43E7 29            [11]  783 	add	hl, hl
   43E8 09            [11]  784 	add	hl, bc
   43E9 29            [11]  785 	add	hl, hl
   43EA 11 FD 5E      [10]  786 	ld	de, #_g_projectiles
   43ED 19            [11]  787 	add	hl, de
   43EE C5            [11]  788 	push	bc
   43EF E5            [11]  789 	push	hl
   43F0 CD 3B 5B      [17]  790 	call	_projectileupdate
   43F3 F1            [10]  791 	pop	af
   43F4 C1            [10]  792 	pop	bc
                            793 ;src/game.c:183: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43F5 0C            [ 4]  794 	inc	c
   43F6 79            [ 4]  795 	ld	a, c
   43F7 D6 06         [ 7]  796 	sub	a, #0x06
   43F9 38 E7         [12]  797 	jr	C,00174$
                            798 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   43FB 0E 00         [ 7]  799 	ld	c, #0x00
   43FD                     800 00176$:
                            801 ;src/game.c:188: enemyupdate(&g_enemies[i]);
   43FD 06 00         [ 7]  802 	ld	b,#0x00
   43FF 69            [ 4]  803 	ld	l, c
   4400 60            [ 4]  804 	ld	h, b
   4401 29            [11]  805 	add	hl, hl
   4402 29            [11]  806 	add	hl, hl
   4403 09            [11]  807 	add	hl, bc
   4404 29            [11]  808 	add	hl, hl
   4405 11 C1 5E      [10]  809 	ld	de, #_g_enemies
   4408 19            [11]  810 	add	hl, de
   4409 C5            [11]  811 	push	bc
   440A E5            [11]  812 	push	hl
   440B CD 7F 53      [17]  813 	call	_enemyupdate
   440E F1            [10]  814 	pop	af
   440F C1            [10]  815 	pop	bc
                            816 ;src/game.c:187: for (i = 0; i < MAX_ENEMIES; ++i) {
   4410 0C            [ 4]  817 	inc	c
   4411 79            [ 4]  818 	ld	a, c
   4412 D6 06         [ 7]  819 	sub	a, #0x06
   4414 38 E7         [12]  820 	jr	C,00176$
                            821 ;src/game.c:191: if (g_bossactive) {
   4416 3A 54 5F      [13]  822 	ld	a,(#_g_bossactive + 0)
   4419 B7            [ 4]  823 	or	a, a
   441A 28 71         [12]  824 	jr	Z,00211$
                            825 ;src/game.c:192: if (g_boss.health > 4) g_bossphase = 0;
   441C 21 51 5F      [10]  826 	ld	hl, #_g_boss + 7
   441F 4E            [ 7]  827 	ld	c, (hl)
   4420 3E 04         [ 7]  828 	ld	a, #0x04
   4422 91            [ 4]  829 	sub	a, c
   4423 30 07         [12]  830 	jr	NC,00111$
   4425 21 55 5F      [10]  831 	ld	hl,#_g_bossphase + 0
   4428 36 00         [10]  832 	ld	(hl), #0x00
   442A 18 05         [12]  833 	jr	00112$
   442C                     834 00111$:
                            835 ;src/game.c:193: else g_bossphase = 1;
   442C 21 55 5F      [10]  836 	ld	hl,#_g_bossphase + 0
   442F 36 01         [10]  837 	ld	(hl), #0x01
   4431                     838 00112$:
                            839 ;src/game.c:195: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4431 3A B8 5E      [13]  840 	ld	a,(#_g_player + 0)
   4434 DD 77 EB      [19]  841 	ld	-21 (ix), a
   4437 DD 77 E9      [19]  842 	ld	-23 (ix), a
   443A DD 36 EA 00   [19]  843 	ld	-22 (ix), #0x00
   443E DD 7E E9      [19]  844 	ld	a, -23 (ix)
   4441 C6 02         [ 7]  845 	add	a, #0x02
   4443 DD 77 E9      [19]  846 	ld	-23 (ix), a
   4446 DD 7E EA      [19]  847 	ld	a, -22 (ix)
   4449 CE 00         [ 7]  848 	adc	a, #0x00
   444B DD 77 EA      [19]  849 	ld	-22 (ix), a
   444E 21 4A 5F      [10]  850 	ld	hl, #_g_boss + 0
   4451 4E            [ 7]  851 	ld	c, (hl)
   4452 06 00         [ 7]  852 	ld	b, #0x00
   4454 DD 7E E9      [19]  853 	ld	a, -23 (ix)
   4457 91            [ 4]  854 	sub	a, c
   4458 DD 7E EA      [19]  855 	ld	a, -22 (ix)
   445B 98            [ 4]  856 	sbc	a, b
   445C E2 61 44      [10]  857 	jp	PO, 00380$
   445F EE 80         [ 7]  858 	xor	a, #0x80
   4461                     859 00380$:
   4461 F2 75 44      [10]  860 	jp	P, 00183$
   4464 3A 55 5F      [13]  861 	ld	a,(#_g_bossphase + 0)
   4467 B7            [ 4]  862 	or	a, a
   4468 28 04         [12]  863 	jr	Z,00185$
   446A 0E 02         [ 7]  864 	ld	c, #0x02
   446C 18 02         [12]  865 	jr	00186$
   446E                     866 00185$:
   446E 0E 01         [ 7]  867 	ld	c, #0x01
   4470                     868 00186$:
   4470 AF            [ 4]  869 	xor	a, a
   4471 91            [ 4]  870 	sub	a, c
   4472 4F            [ 4]  871 	ld	c, a
   4473 18 0C         [12]  872 	jr	00184$
   4475                     873 00183$:
   4475 3A 55 5F      [13]  874 	ld	a,(#_g_bossphase + 0)
   4478 B7            [ 4]  875 	or	a, a
   4479 28 04         [12]  876 	jr	Z,00187$
   447B 0E 02         [ 7]  877 	ld	c, #0x02
   447D 18 02         [12]  878 	jr	00188$
   447F                     879 00187$:
   447F 0E 01         [ 7]  880 	ld	c, #0x01
   4481                     881 00188$:
   4481                     882 00184$:
   4481 21 4C 5F      [10]  883 	ld	hl, #(_g_boss + 0x0002)
   4484 71            [ 7]  884 	ld	(hl), c
                            885 ;src/game.c:196: enemyupdate(&g_boss);
   4485 21 4A 5F      [10]  886 	ld	hl, #_g_boss
   4488 E5            [11]  887 	push	hl
   4489 CD 7F 53      [17]  888 	call	_enemyupdate
   448C F1            [10]  889 	pop	af
                            890 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   448D                     891 00211$:
   448D 0E 00         [ 7]  892 	ld	c, #0x00
   448F                     893 00179$:
                            894 ;src/game.c:200: if (!g_projectiles[i].active) continue;
   448F 06 00         [ 7]  895 	ld	b,#0x00
   4491 69            [ 4]  896 	ld	l, c
   4492 60            [ 4]  897 	ld	h, b
   4493 29            [11]  898 	add	hl, hl
   4494 29            [11]  899 	add	hl, hl
   4495 09            [11]  900 	add	hl, bc
   4496 29            [11]  901 	add	hl, hl
   4497 EB            [ 4]  902 	ex	de,hl
   4498 21 FD 5E      [10]  903 	ld	hl, #_g_projectiles
   449B 19            [11]  904 	add	hl,de
   449C EB            [ 4]  905 	ex	de,hl
   449D 21 06 00      [10]  906 	ld	hl, #0x0006
   44A0 19            [11]  907 	add	hl,de
   44A1 DD 75 E9      [19]  908 	ld	-23 (ix), l
   44A4 DD 74 EA      [19]  909 	ld	-22 (ix), h
   44A7 7E            [ 7]  910 	ld	a, (hl)
   44A8 B7            [ 4]  911 	or	a, a
   44A9 CA CA 46      [10]  912 	jp	Z, 00133$
                            913 ;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
   44AC DD 36 E7 00   [19]  914 	ld	-25 (ix), #0x00
   44B0                     915 00178$:
                            916 ;src/game.c:202: if (!g_enemies[j].active) continue;
   44B0 D5            [11]  917 	push	de
   44B1 DD 5E E7      [19]  918 	ld	e,-25 (ix)
   44B4 16 00         [ 7]  919 	ld	d,#0x00
   44B6 6B            [ 4]  920 	ld	l, e
   44B7 62            [ 4]  921 	ld	h, d
   44B8 29            [11]  922 	add	hl, hl
   44B9 29            [11]  923 	add	hl, hl
   44BA 19            [11]  924 	add	hl, de
   44BB 29            [11]  925 	add	hl, hl
   44BC D1            [10]  926 	pop	de
   44BD 3E C1         [ 7]  927 	ld	a, #<(_g_enemies)
   44BF 85            [ 4]  928 	add	a, l
   44C0 DD 77 FE      [19]  929 	ld	-2 (ix), a
   44C3 3E 5E         [ 7]  930 	ld	a, #>(_g_enemies)
   44C5 8C            [ 4]  931 	adc	a, h
   44C6 DD 77 FF      [19]  932 	ld	-1 (ix), a
   44C9 DD 6E FE      [19]  933 	ld	l,-2 (ix)
   44CC DD 66 FF      [19]  934 	ld	h,-1 (ix)
   44CF C5            [11]  935 	push	bc
   44D0 01 06 00      [10]  936 	ld	bc, #0x0006
   44D3 09            [11]  937 	add	hl, bc
   44D4 C1            [10]  938 	pop	bc
   44D5 46            [ 7]  939 	ld	b, (hl)
                            940 ;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   44D6 21 05 00      [10]  941 	ld	hl, #0x0005
   44D9 19            [11]  942 	add	hl,de
   44DA DD 75 F2      [19]  943 	ld	-14 (ix), l
   44DD DD 74 F3      [19]  944 	ld	-13 (ix), h
   44E0 21 04 00      [10]  945 	ld	hl, #0x0004
   44E3 19            [11]  946 	add	hl,de
   44E4 DD 75 F0      [19]  947 	ld	-16 (ix), l
   44E7 DD 74 F1      [19]  948 	ld	-15 (ix), h
   44EA 21 01 00      [10]  949 	ld	hl, #0x0001
   44ED 19            [11]  950 	add	hl,de
   44EE DD 75 F6      [19]  951 	ld	-10 (ix), l
   44F1 DD 74 F7      [19]  952 	ld	-9 (ix), h
                            953 ;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44F4 21 07 00      [10]  954 	ld	hl, #0x0007
   44F7 19            [11]  955 	add	hl,de
   44F8 DD 75 F4      [19]  956 	ld	-12 (ix), l
   44FB DD 74 F5      [19]  957 	ld	-11 (ix), h
                            958 ;src/game.c:202: if (!g_enemies[j].active) continue;
   44FE 78            [ 4]  959 	ld	a, b
   44FF B7            [ 4]  960 	or	a, a
   4500 CA F8 45      [10]  961 	jp	Z, 00125$
                            962 ;src/game.c:204: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   4503 DD 6E FE      [19]  963 	ld	l,-2 (ix)
   4506 DD 66 FF      [19]  964 	ld	h,-1 (ix)
   4509 23            [ 6]  965 	inc	hl
   450A 23            [ 6]  966 	inc	hl
   450B 23            [ 6]  967 	inc	hl
   450C 23            [ 6]  968 	inc	hl
   450D 23            [ 6]  969 	inc	hl
   450E 7E            [ 7]  970 	ld	a, (hl)
   450F DD 77 EB      [19]  971 	ld	-21 (ix), a
   4512 DD 6E FE      [19]  972 	ld	l,-2 (ix)
   4515 DD 66 FF      [19]  973 	ld	h,-1 (ix)
   4518 23            [ 6]  974 	inc	hl
   4519 23            [ 6]  975 	inc	hl
   451A 23            [ 6]  976 	inc	hl
   451B 23            [ 6]  977 	inc	hl
   451C 7E            [ 7]  978 	ld	a, (hl)
   451D DD 77 FD      [19]  979 	ld	-3 (ix), a
   4520 DD 6E FE      [19]  980 	ld	l,-2 (ix)
   4523 DD 66 FF      [19]  981 	ld	h,-1 (ix)
   4526 23            [ 6]  982 	inc	hl
   4527 46            [ 7]  983 	ld	b, (hl)
   4528 DD 70 FB      [19]  984 	ld	-5 (ix), b
   452B DD 36 FC 00   [19]  985 	ld	-4 (ix), #0x00
   452F DD 6E FE      [19]  986 	ld	l,-2 (ix)
   4532 DD 66 FF      [19]  987 	ld	h,-1 (ix)
   4535 46            [ 7]  988 	ld	b, (hl)
   4536 DD 70 F9      [19]  989 	ld	-7 (ix), b
   4539 DD 36 FA 00   [19]  990 	ld	-6 (ix), #0x00
                            991 ;src/game.c:203: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   453D DD 6E F2      [19]  992 	ld	l,-14 (ix)
   4540 DD 66 F3      [19]  993 	ld	h,-13 (ix)
   4543 7E            [ 7]  994 	ld	a, (hl)
   4544 DD 77 F8      [19]  995 	ld	-8 (ix), a
   4547 DD 6E F0      [19]  996 	ld	l,-16 (ix)
   454A DD 66 F1      [19]  997 	ld	h,-15 (ix)
   454D 46            [ 7]  998 	ld	b, (hl)
   454E DD 6E F6      [19]  999 	ld	l,-10 (ix)
   4551 DD 66 F7      [19] 1000 	ld	h,-9 (ix)
   4554 6E            [ 7] 1001 	ld	l, (hl)
   4555 DD 75 EE      [19] 1002 	ld	-18 (ix), l
   4558 DD 36 EF 00   [19] 1003 	ld	-17 (ix), #0x00
   455C 1A            [ 7] 1004 	ld	a, (de)
   455D DD 77 EC      [19] 1005 	ld	-20 (ix), a
   4560 DD 36 ED 00   [19] 1006 	ld	-19 (ix), #0x00
   4564 C5            [11] 1007 	push	bc
   4565 D5            [11] 1008 	push	de
   4566 DD 66 EB      [19] 1009 	ld	h, -21 (ix)
   4569 DD 6E FD      [19] 1010 	ld	l, -3 (ix)
   456C E5            [11] 1011 	push	hl
   456D DD 6E FB      [19] 1012 	ld	l,-5 (ix)
   4570 DD 66 FC      [19] 1013 	ld	h,-4 (ix)
   4573 E5            [11] 1014 	push	hl
   4574 DD 6E F9      [19] 1015 	ld	l,-7 (ix)
   4577 DD 66 FA      [19] 1016 	ld	h,-6 (ix)
   457A E5            [11] 1017 	push	hl
   457B DD 7E F8      [19] 1018 	ld	a, -8 (ix)
   457E F5            [11] 1019 	push	af
   457F 33            [ 6] 1020 	inc	sp
   4580 C5            [11] 1021 	push	bc
   4581 33            [ 6] 1022 	inc	sp
   4582 DD 6E EE      [19] 1023 	ld	l,-18 (ix)
   4585 DD 66 EF      [19] 1024 	ld	h,-17 (ix)
   4588 E5            [11] 1025 	push	hl
   4589 DD 6E EC      [19] 1026 	ld	l,-20 (ix)
   458C DD 66 ED      [19] 1027 	ld	h,-19 (ix)
   458F E5            [11] 1028 	push	hl
   4590 CD 19 40      [17] 1029 	call	_rect_overlap
   4593 FD 21 0C 00   [14] 1030 	ld	iy, #12
   4597 FD 39         [15] 1031 	add	iy, sp
   4599 FD F9         [10] 1032 	ld	sp, iy
   459B D1            [10] 1033 	pop	de
   459C C1            [10] 1034 	pop	bc
   459D 7D            [ 4] 1035 	ld	a, l
   459E B7            [ 4] 1036 	or	a, a
   459F 28 57         [12] 1037 	jr	Z,00125$
                           1038 ;src/game.c:205: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   45A1 DD 6E F4      [19] 1039 	ld	l,-12 (ix)
   45A4 DD 66 F5      [19] 1040 	ld	h,-11 (ix)
   45A7 66            [ 7] 1041 	ld	h, (hl)
   45A8 DD 6E FE      [19] 1042 	ld	l, -2 (ix)
   45AB DD 46 FF      [19] 1043 	ld	b, -1 (ix)
   45AE C5            [11] 1044 	push	bc
   45AF D5            [11] 1045 	push	de
   45B0 E5            [11] 1046 	push	hl
   45B1 33            [ 6] 1047 	inc	sp
   45B2 60            [ 4] 1048 	ld	h, b
   45B3 E5            [11] 1049 	push	hl
   45B4 CD 05 56      [17] 1050 	call	_enemydamage
   45B7 F1            [10] 1051 	pop	af
   45B8 33            [ 6] 1052 	inc	sp
   45B9 D1            [10] 1053 	pop	de
   45BA C1            [10] 1054 	pop	bc
   45BB 7D            [ 4] 1055 	ld	a, l
   45BC B7            [ 4] 1056 	or	a, a
   45BD 28 2F         [12] 1057 	jr	Z,00124$
                           1058 ;src/game.c:206: g_score = (u16)(g_score + g_enemies[j].reward);
   45BF DD 6E FE      [19] 1059 	ld	l,-2 (ix)
   45C2 DD 66 FF      [19] 1060 	ld	h,-1 (ix)
   45C5 C5            [11] 1061 	push	bc
   45C6 01 08 00      [10] 1062 	ld	bc, #0x0008
   45C9 09            [11] 1063 	add	hl, bc
   45CA C1            [10] 1064 	pop	bc
   45CB 6E            [ 7] 1065 	ld	l, (hl)
   45CC DD 75 EC      [19] 1066 	ld	-20 (ix), l
   45CF DD 36 ED 00   [19] 1067 	ld	-19 (ix), #0x00
   45D3 21 3A 5F      [10] 1068 	ld	hl, #_g_score
   45D6 7E            [ 7] 1069 	ld	a, (hl)
   45D7 DD 86 EC      [19] 1070 	add	a, -20 (ix)
   45DA 77            [ 7] 1071 	ld	(hl), a
   45DB 23            [ 6] 1072 	inc	hl
   45DC 7E            [ 7] 1073 	ld	a, (hl)
   45DD DD 8E ED      [19] 1074 	adc	a, -19 (ix)
   45E0 77            [ 7] 1075 	ld	(hl), a
                           1076 ;src/game.c:207: if (g_aliveenemies) g_aliveenemies--;
   45E1 FD 21 3F 5F   [14] 1077 	ld	iy, #_g_aliveenemies
   45E5 FD 7E 00      [19] 1078 	ld	a, 0 (iy)
   45E8 B7            [ 4] 1079 	or	a, a
   45E9 28 03         [12] 1080 	jr	Z,00124$
   45EB FD 35 00      [23] 1081 	dec	0 (iy)
   45EE                    1082 00124$:
                           1083 ;src/game.c:209: g_projectiles[i].active = 0;
   45EE DD 6E E9      [19] 1084 	ld	l,-23 (ix)
   45F1 DD 66 EA      [19] 1085 	ld	h,-22 (ix)
   45F4 36 00         [10] 1086 	ld	(hl), #0x00
                           1087 ;src/game.c:210: break;
   45F6 18 0B         [12] 1088 	jr	00126$
   45F8                    1089 00125$:
                           1090 ;src/game.c:201: for (j = 0; j < MAX_ENEMIES; ++j) {
   45F8 DD 34 E7      [23] 1091 	inc	-25 (ix)
   45FB DD 7E E7      [19] 1092 	ld	a, -25 (ix)
   45FE D6 06         [ 7] 1093 	sub	a, #0x06
   4600 DA B0 44      [10] 1094 	jp	C, 00178$
   4603                    1095 00126$:
                           1096 ;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4603 3A 54 5F      [13] 1097 	ld	a,(#_g_bossactive + 0)
   4606 B7            [ 4] 1098 	or	a, a
   4607 CA CA 46      [10] 1099 	jp	Z, 00133$
   460A DD 6E E9      [19] 1100 	ld	l,-23 (ix)
   460D DD 66 EA      [19] 1101 	ld	h,-22 (ix)
   4610 7E            [ 7] 1102 	ld	a, (hl)
   4611 B7            [ 4] 1103 	or	a, a
   4612 CA CA 46      [10] 1104 	jp	Z, 00133$
                           1105 ;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   4615 21 4F 5F      [10] 1106 	ld	hl, #(_g_boss + 0x0005) + 0
   4618 46            [ 7] 1107 	ld	b, (hl)
   4619 3A 4E 5F      [13] 1108 	ld	a, (#(_g_boss + 0x0004) + 0)
   461C 21 4B 5F      [10] 1109 	ld	hl, #(_g_boss + 0x0001) + 0
   461F 6E            [ 7] 1110 	ld	l, (hl)
   4620 DD 75 EC      [19] 1111 	ld	-20 (ix), l
   4623 DD 36 ED 00   [19] 1112 	ld	-19 (ix), #0x00
   4627 21 4A 5F      [10] 1113 	ld	hl, #_g_boss + 0
   462A 6E            [ 7] 1114 	ld	l, (hl)
   462B DD 75 EE      [19] 1115 	ld	-18 (ix), l
   462E DD 36 EF 00   [19] 1116 	ld	-17 (ix), #0x00
                           1117 ;src/game.c:213: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4632 DD 6E F2      [19] 1118 	ld	l,-14 (ix)
   4635 DD 66 F3      [19] 1119 	ld	h,-13 (ix)
   4638 F5            [11] 1120 	push	af
   4639 7E            [ 7] 1121 	ld	a, (hl)
   463A DD 77 F8      [19] 1122 	ld	-8 (ix), a
   463D F1            [10] 1123 	pop	af
   463E DD 6E F0      [19] 1124 	ld	l,-16 (ix)
   4641 DD 66 F1      [19] 1125 	ld	h,-15 (ix)
   4644 F5            [11] 1126 	push	af
   4645 7E            [ 7] 1127 	ld	a, (hl)
   4646 DD 77 F9      [19] 1128 	ld	-7 (ix), a
   4649 F1            [10] 1129 	pop	af
   464A DD 6E F6      [19] 1130 	ld	l,-10 (ix)
   464D DD 66 F7      [19] 1131 	ld	h,-9 (ix)
   4650 6E            [ 7] 1132 	ld	l, (hl)
   4651 DD 75 FB      [19] 1133 	ld	-5 (ix), l
   4654 DD 36 FC 00   [19] 1134 	ld	-4 (ix), #0x00
   4658 F5            [11] 1135 	push	af
   4659 1A            [ 7] 1136 	ld	a, (de)
   465A 5F            [ 4] 1137 	ld	e, a
   465B F1            [10] 1138 	pop	af
   465C 16 00         [ 7] 1139 	ld	d, #0x00
   465E C5            [11] 1140 	push	bc
   465F C5            [11] 1141 	push	bc
   4660 33            [ 6] 1142 	inc	sp
   4661 F5            [11] 1143 	push	af
   4662 33            [ 6] 1144 	inc	sp
   4663 DD 6E EC      [19] 1145 	ld	l,-20 (ix)
   4666 DD 66 ED      [19] 1146 	ld	h,-19 (ix)
   4669 E5            [11] 1147 	push	hl
   466A DD 6E EE      [19] 1148 	ld	l,-18 (ix)
   466D DD 66 EF      [19] 1149 	ld	h,-17 (ix)
   4670 E5            [11] 1150 	push	hl
   4671 DD 66 F8      [19] 1151 	ld	h, -8 (ix)
   4674 DD 6E F9      [19] 1152 	ld	l, -7 (ix)
   4677 E5            [11] 1153 	push	hl
   4678 DD 6E FB      [19] 1154 	ld	l,-5 (ix)
   467B DD 66 FC      [19] 1155 	ld	h,-4 (ix)
   467E E5            [11] 1156 	push	hl
   467F D5            [11] 1157 	push	de
   4680 CD 19 40      [17] 1158 	call	_rect_overlap
   4683 FD 21 0C 00   [14] 1159 	ld	iy, #12
   4687 FD 39         [15] 1160 	add	iy, sp
   4689 FD F9         [10] 1161 	ld	sp, iy
   468B C1            [10] 1162 	pop	bc
   468C 7D            [ 4] 1163 	ld	a, l
   468D B7            [ 4] 1164 	or	a, a
   468E 28 3A         [12] 1165 	jr	Z,00133$
                           1166 ;src/game.c:215: g_projectiles[i].active = 0;
   4690 DD 6E E9      [19] 1167 	ld	l,-23 (ix)
   4693 DD 66 EA      [19] 1168 	ld	h,-22 (ix)
   4696 36 00         [10] 1169 	ld	(hl), #0x00
                           1170 ;src/game.c:216: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   4698 DD 6E F4      [19] 1171 	ld	l,-12 (ix)
   469B DD 66 F5      [19] 1172 	ld	h,-11 (ix)
   469E 46            [ 7] 1173 	ld	b, (hl)
   469F 11 4A 5F      [10] 1174 	ld	de, #_g_boss
   46A2 C5            [11] 1175 	push	bc
   46A3 C5            [11] 1176 	push	bc
   46A4 33            [ 6] 1177 	inc	sp
   46A5 D5            [11] 1178 	push	de
   46A6 CD 05 56      [17] 1179 	call	_enemydamage
   46A9 F1            [10] 1180 	pop	af
   46AA 33            [ 6] 1181 	inc	sp
   46AB C1            [10] 1182 	pop	bc
   46AC 7D            [ 4] 1183 	ld	a, l
   46AD B7            [ 4] 1184 	or	a, a
   46AE 28 1A         [12] 1185 	jr	Z,00133$
                           1186 ;src/game.c:217: g_bossactive = 0;
   46B0 21 54 5F      [10] 1187 	ld	hl,#_g_bossactive + 0
   46B3 36 00         [10] 1188 	ld	(hl), #0x00
                           1189 ;src/game.c:218: g_score = (u16)(g_score + g_boss.reward);
   46B5 21 52 5F      [10] 1190 	ld	hl, #_g_boss + 8
   46B8 5E            [ 7] 1191 	ld	e, (hl)
   46B9 16 00         [ 7] 1192 	ld	d, #0x00
   46BB 21 3A 5F      [10] 1193 	ld	hl, #_g_score
   46BE 7E            [ 7] 1194 	ld	a, (hl)
   46BF 83            [ 4] 1195 	add	a, e
   46C0 77            [ 7] 1196 	ld	(hl), a
   46C1 23            [ 6] 1197 	inc	hl
   46C2 7E            [ 7] 1198 	ld	a, (hl)
   46C3 8A            [ 4] 1199 	adc	a, d
   46C4 77            [ 7] 1200 	ld	(hl), a
                           1201 ;src/game.c:219: g_victory = 1;
   46C5 21 43 5F      [10] 1202 	ld	hl,#_g_victory + 0
   46C8 36 01         [10] 1203 	ld	(hl), #0x01
   46CA                    1204 00133$:
                           1205 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   46CA 0C            [ 4] 1206 	inc	c
   46CB 79            [ 4] 1207 	ld	a, c
   46CC D6 06         [ 7] 1208 	sub	a, #0x06
   46CE DA 8F 44      [10] 1209 	jp	C, 00179$
                           1210 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1211 ;src/game.c:224: if (!g_damagecooldown) {
   46D1 3A 41 5F      [13] 1212 	ld	a,(#_g_damagecooldown + 0)
   46D4 B7            [ 4] 1213 	or	a, a
   46D5 C2 44 48      [10] 1214 	jp	NZ, 00149$
                           1215 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   46D8 DD 36 E8 00   [19] 1216 	ld	-24 (ix), #0x00
   46DC                    1217 00180$:
                           1218 ;src/game.c:226: if (!g_enemies[i].active) continue;
   46DC DD 4E E8      [19] 1219 	ld	c,-24 (ix)
   46DF 06 00         [ 7] 1220 	ld	b,#0x00
   46E1 69            [ 4] 1221 	ld	l, c
   46E2 60            [ 4] 1222 	ld	h, b
   46E3 29            [11] 1223 	add	hl, hl
   46E4 29            [11] 1224 	add	hl, hl
   46E5 09            [11] 1225 	add	hl, bc
   46E6 29            [11] 1226 	add	hl, hl
   46E7 4D            [ 4] 1227 	ld	c, l
   46E8 44            [ 4] 1228 	ld	b, h
   46E9 21 C1 5E      [10] 1229 	ld	hl, #_g_enemies
   46EC 09            [11] 1230 	add	hl,bc
   46ED DD 75 EC      [19] 1231 	ld	-20 (ix), l
   46F0 DD 74 ED      [19] 1232 	ld	-19 (ix), h
   46F3 11 06 00      [10] 1233 	ld	de, #0x0006
   46F6 19            [11] 1234 	add	hl, de
   46F7 7E            [ 7] 1235 	ld	a, (hl)
   46F8 B7            [ 4] 1236 	or	a, a
   46F9 CA 8E 47      [10] 1237 	jp	Z, 00139$
                           1238 ;src/game.c:228: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   46FC DD 7E EC      [19] 1239 	ld	a, -20 (ix)
   46FF DD 77 EE      [19] 1240 	ld	-18 (ix), a
   4702 DD 7E ED      [19] 1241 	ld	a, -19 (ix)
   4705 DD 77 EF      [19] 1242 	ld	-17 (ix), a
   4708 DD 6E EE      [19] 1243 	ld	l,-18 (ix)
   470B DD 66 EF      [19] 1244 	ld	h,-17 (ix)
   470E 11 05 00      [10] 1245 	ld	de, #0x0005
   4711 19            [11] 1246 	add	hl, de
   4712 7E            [ 7] 1247 	ld	a, (hl)
   4713 DD 77 EE      [19] 1248 	ld	-18 (ix), a
   4716 DD 6E EC      [19] 1249 	ld	l,-20 (ix)
   4719 DD 66 ED      [19] 1250 	ld	h,-19 (ix)
   471C 11 04 00      [10] 1251 	ld	de, #0x0004
   471F 19            [11] 1252 	add	hl, de
   4720 5E            [ 7] 1253 	ld	e, (hl)
   4721 DD 6E EC      [19] 1254 	ld	l,-20 (ix)
   4724 DD 66 ED      [19] 1255 	ld	h,-19 (ix)
   4727 23            [ 6] 1256 	inc	hl
   4728 4E            [ 7] 1257 	ld	c, (hl)
   4729 06 00         [ 7] 1258 	ld	b, #0x00
   472B DD 6E EC      [19] 1259 	ld	l,-20 (ix)
   472E DD 66 ED      [19] 1260 	ld	h,-19 (ix)
   4731 56            [ 7] 1261 	ld	d, (hl)
   4732 DD 72 EC      [19] 1262 	ld	-20 (ix), d
   4735 DD 36 ED 00   [19] 1263 	ld	-19 (ix), #0x00
                           1264 ;src/game.c:227: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4739 3A BD 5E      [13] 1265 	ld	a,(#(_g_player + 0x0005) + 0)
   473C DD 77 F8      [19] 1266 	ld	-8 (ix), a
   473F 3A BC 5E      [13] 1267 	ld	a,(#(_g_player + 0x0004) + 0)
   4742 DD 77 F9      [19] 1268 	ld	-7 (ix), a
   4745 3A B9 5E      [13] 1269 	ld	a, (#(_g_player + 0x0001) + 0)
   4748 DD 77 FB      [19] 1270 	ld	-5 (ix), a
   474B DD 36 FC 00   [19] 1271 	ld	-4 (ix), #0x00
   474F 3A B8 5E      [13] 1272 	ld	a, (#_g_player + 0)
   4752 DD 77 F4      [19] 1273 	ld	-12 (ix), a
   4755 DD 36 F5 00   [19] 1274 	ld	-11 (ix), #0x00
   4759 DD 56 EE      [19] 1275 	ld	d, -18 (ix)
   475C D5            [11] 1276 	push	de
   475D C5            [11] 1277 	push	bc
   475E DD 6E EC      [19] 1278 	ld	l,-20 (ix)
   4761 DD 66 ED      [19] 1279 	ld	h,-19 (ix)
   4764 E5            [11] 1280 	push	hl
   4765 DD 66 F8      [19] 1281 	ld	h, -8 (ix)
   4768 DD 6E F9      [19] 1282 	ld	l, -7 (ix)
   476B E5            [11] 1283 	push	hl
   476C DD 6E FB      [19] 1284 	ld	l,-5 (ix)
   476F DD 66 FC      [19] 1285 	ld	h,-4 (ix)
   4772 E5            [11] 1286 	push	hl
   4773 DD 6E F4      [19] 1287 	ld	l,-12 (ix)
   4776 DD 66 F5      [19] 1288 	ld	h,-11 (ix)
   4779 E5            [11] 1289 	push	hl
   477A CD 19 40      [17] 1290 	call	_rect_overlap
   477D FD 21 0C 00   [14] 1291 	ld	iy, #12
   4781 FD 39         [15] 1292 	add	iy, sp
   4783 FD F9         [10] 1293 	ld	sp, iy
   4785 7D            [ 4] 1294 	ld	a, l
   4786 B7            [ 4] 1295 	or	a, a
   4787 28 05         [12] 1296 	jr	Z,00139$
                           1297 ;src/game.c:229: register_player_hit();
   4789 CD 91 42      [17] 1298 	call	_register_player_hit
                           1299 ;src/game.c:230: break;
   478C 18 0B         [12] 1300 	jr	00140$
   478E                    1301 00139$:
                           1302 ;src/game.c:225: for (i = 0; i < MAX_ENEMIES; ++i) {
   478E DD 34 E8      [23] 1303 	inc	-24 (ix)
   4791 DD 7E E8      [19] 1304 	ld	a, -24 (ix)
   4794 D6 06         [ 7] 1305 	sub	a, #0x06
   4796 DA DC 46      [10] 1306 	jp	C, 00180$
   4799                    1307 00140$:
                           1308 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4799 3A 41 5F      [13] 1309 	ld	a,(#_g_damagecooldown + 0)
   479C B7            [ 4] 1310 	or	a, a
   479D 20 6E         [12] 1311 	jr	NZ,00142$
   479F 3A 54 5F      [13] 1312 	ld	a,(#_g_bossactive + 0)
   47A2 B7            [ 4] 1313 	or	a, a
   47A3 28 68         [12] 1314 	jr	Z,00142$
                           1315 ;src/game.c:235: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   47A5 3A 4F 5F      [13] 1316 	ld	a,(#(_g_boss + 0x0005) + 0)
   47A8 DD 77 EC      [19] 1317 	ld	-20 (ix), a
   47AB 3A 4E 5F      [13] 1318 	ld	a,(#(_g_boss + 0x0004) + 0)
   47AE DD 77 EE      [19] 1319 	ld	-18 (ix), a
   47B1 21 4B 5F      [10] 1320 	ld	hl, #(_g_boss + 0x0001) + 0
   47B4 5E            [ 7] 1321 	ld	e, (hl)
   47B5 16 00         [ 7] 1322 	ld	d, #0x00
   47B7 21 4A 5F      [10] 1323 	ld	hl, #_g_boss + 0
   47BA 4E            [ 7] 1324 	ld	c, (hl)
   47BB 06 00         [ 7] 1325 	ld	b, #0x00
                           1326 ;src/game.c:234: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   47BD 3A BD 5E      [13] 1327 	ld	a,(#(_g_player + 0x0005) + 0)
   47C0 DD 77 F8      [19] 1328 	ld	-8 (ix), a
   47C3 3A BC 5E      [13] 1329 	ld	a,(#(_g_player + 0x0004) + 0)
   47C6 DD 77 F9      [19] 1330 	ld	-7 (ix), a
   47C9 3A B9 5E      [13] 1331 	ld	a, (#(_g_player + 0x0001) + 0)
   47CC DD 77 FB      [19] 1332 	ld	-5 (ix), a
   47CF DD 36 FC 00   [19] 1333 	ld	-4 (ix), #0x00
   47D3 3A B8 5E      [13] 1334 	ld	a, (#_g_player + 0)
   47D6 DD 77 F4      [19] 1335 	ld	-12 (ix), a
   47D9 DD 36 F5 00   [19] 1336 	ld	-11 (ix), #0x00
   47DD DD 66 EC      [19] 1337 	ld	h, -20 (ix)
   47E0 DD 6E EE      [19] 1338 	ld	l, -18 (ix)
   47E3 E5            [11] 1339 	push	hl
   47E4 D5            [11] 1340 	push	de
   47E5 C5            [11] 1341 	push	bc
   47E6 DD 66 F8      [19] 1342 	ld	h, -8 (ix)
   47E9 DD 6E F9      [19] 1343 	ld	l, -7 (ix)
   47EC E5            [11] 1344 	push	hl
   47ED DD 6E FB      [19] 1345 	ld	l,-5 (ix)
   47F0 DD 66 FC      [19] 1346 	ld	h,-4 (ix)
   47F3 E5            [11] 1347 	push	hl
   47F4 DD 6E F4      [19] 1348 	ld	l,-12 (ix)
   47F7 DD 66 F5      [19] 1349 	ld	h,-11 (ix)
   47FA E5            [11] 1350 	push	hl
   47FB CD 19 40      [17] 1351 	call	_rect_overlap
   47FE FD 21 0C 00   [14] 1352 	ld	iy, #12
   4802 FD 39         [15] 1353 	add	iy, sp
   4804 FD F9         [10] 1354 	ld	sp, iy
   4806 7D            [ 4] 1355 	ld	a, l
   4807 B7            [ 4] 1356 	or	a, a
   4808 28 03         [12] 1357 	jr	Z,00142$
                           1358 ;src/game.c:236: register_player_hit();
   480A CD 91 42      [17] 1359 	call	_register_player_hit
   480D                    1360 00142$:
                           1361 ;src/game.c:239: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   480D 3A 41 5F      [13] 1362 	ld	a,(#_g_damagecooldown + 0)
   4810 B7            [ 4] 1363 	or	a, a
   4811 20 31         [12] 1364 	jr	NZ,00149$
   4813 3A BD 5E      [13] 1365 	ld	a, (#(_g_player + 0x0005) + 0)
   4816 21 BC 5E      [10] 1366 	ld	hl, #(_g_player + 0x0004) + 0
   4819 56            [ 7] 1367 	ld	d, (hl)
   481A 21 B9 5E      [10] 1368 	ld	hl, #(_g_player + 0x0001) + 0
   481D 4E            [ 7] 1369 	ld	c, (hl)
   481E 06 00         [ 7] 1370 	ld	b, #0x00
   4820 21 B8 5E      [10] 1371 	ld	hl, #_g_player + 0
   4823 6E            [ 7] 1372 	ld	l, (hl)
   4824 DD 75 EC      [19] 1373 	ld	-20 (ix), l
   4827 DD 36 ED 00   [19] 1374 	ld	-19 (ix), #0x00
   482B F5            [11] 1375 	push	af
   482C 33            [ 6] 1376 	inc	sp
   482D D5            [11] 1377 	push	de
   482E 33            [ 6] 1378 	inc	sp
   482F C5            [11] 1379 	push	bc
   4830 DD 6E EC      [19] 1380 	ld	l,-20 (ix)
   4833 DD 66 ED      [19] 1381 	ld	h,-19 (ix)
   4836 E5            [11] 1382 	push	hl
   4837 CD 6D 4C      [17] 1383 	call	_collision_is_on_trap
   483A F1            [10] 1384 	pop	af
   483B F1            [10] 1385 	pop	af
   483C F1            [10] 1386 	pop	af
   483D 7D            [ 4] 1387 	ld	a, l
   483E B7            [ 4] 1388 	or	a, a
   483F 28 03         [12] 1389 	jr	Z,00149$
                           1390 ;src/game.c:240: register_player_hit();
   4841 CD 91 42      [17] 1391 	call	_register_player_hit
   4844                    1392 00149$:
                           1393 ;src/game.c:244: if (!g_checkpointactive && g_player.x >= 44) {
   4844 FD 21 49 5F   [14] 1394 	ld	iy, #_g_checkpointactive
   4848 FD 7E 00      [19] 1395 	ld	a, 0 (iy)
   484B B7            [ 4] 1396 	or	a, a
   484C 20 1E         [12] 1397 	jr	NZ,00151$
   484E 3A B8 5E      [13] 1398 	ld	a, (#_g_player + 0)
   4851 D6 2C         [ 7] 1399 	sub	a, #0x2c
   4853 38 17         [12] 1400 	jr	C,00151$
                           1401 ;src/game.c:245: g_checkpointactive = 1;
   4855 FD 36 00 01   [19] 1402 	ld	0 (iy), #0x01
                           1403 ;src/game.c:246: g_checkpointx = 52;
   4859 21 47 5F      [10] 1404 	ld	hl,#_g_checkpointx + 0
   485C 36 34         [10] 1405 	ld	(hl), #0x34
                           1406 ;src/game.c:247: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   485E CD 84 50      [17] 1407 	call	_tilemap_ground_y
   4861 4D            [ 4] 1408 	ld	c, l
   4862 21 BD 5E      [10] 1409 	ld	hl, #(_g_player + 0x0005) + 0
   4865 46            [ 7] 1410 	ld	b, (hl)
   4866 21 48 5F      [10] 1411 	ld	hl, #_g_checkpointy
   4869 79            [ 4] 1412 	ld	a, c
   486A 90            [ 4] 1413 	sub	a, b
   486B 77            [ 7] 1414 	ld	(hl), a
   486C                    1415 00151$:
                           1416 ;src/game.c:250: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
   486C 3A 57 5F      [13] 1417 	ld	a,(#_g_pickuptaken + 0)
   486F B7            [ 4] 1418 	or	a, a
   4870 C2 FF 48      [10] 1419 	jp	NZ, 00154$
   4873 CD 84 50      [17] 1420 	call	_tilemap_ground_y
   4876 DD 75 EC      [19] 1421 	ld	-20 (ix), l
   4879 DD 75 EC      [19] 1422 	ld	-20 (ix), l
   487C DD 36 ED 00   [19] 1423 	ld	-19 (ix), #0x00
   4880 DD 7E EC      [19] 1424 	ld	a, -20 (ix)
   4883 C6 F8         [ 7] 1425 	add	a, #0xf8
   4885 DD 77 EC      [19] 1426 	ld	-20 (ix), a
   4888 DD 7E ED      [19] 1427 	ld	a, -19 (ix)
   488B CE FF         [ 7] 1428 	adc	a, #0xff
   488D DD 77 ED      [19] 1429 	ld	-19 (ix), a
   4890 3A BD 5E      [13] 1430 	ld	a,(#(_g_player + 0x0005) + 0)
   4893 DD 77 EE      [19] 1431 	ld	-18 (ix), a
   4896 3A BC 5E      [13] 1432 	ld	a,(#(_g_player + 0x0004) + 0)
   4899 DD 77 F8      [19] 1433 	ld	-8 (ix), a
   489C 3A B9 5E      [13] 1434 	ld	a,(#(_g_player + 0x0001) + 0)
   489F DD 77 F9      [19] 1435 	ld	-7 (ix), a
   48A2 DD 77 F9      [19] 1436 	ld	-7 (ix), a
   48A5 DD 36 FA 00   [19] 1437 	ld	-6 (ix), #0x00
   48A9 3A B8 5E      [13] 1438 	ld	a,(#_g_player + 0)
   48AC DD 77 FB      [19] 1439 	ld	-5 (ix), a
   48AF DD 77 FB      [19] 1440 	ld	-5 (ix), a
   48B2 DD 36 FC 00   [19] 1441 	ld	-4 (ix), #0x00
   48B6 21 04 04      [10] 1442 	ld	hl, #0x0404
   48B9 E5            [11] 1443 	push	hl
   48BA DD 6E EC      [19] 1444 	ld	l,-20 (ix)
   48BD DD 66 ED      [19] 1445 	ld	h,-19 (ix)
   48C0 E5            [11] 1446 	push	hl
   48C1 21 24 00      [10] 1447 	ld	hl, #0x0024
   48C4 E5            [11] 1448 	push	hl
   48C5 DD 66 EE      [19] 1449 	ld	h, -18 (ix)
   48C8 DD 6E F8      [19] 1450 	ld	l, -8 (ix)
   48CB E5            [11] 1451 	push	hl
   48CC DD 6E F9      [19] 1452 	ld	l,-7 (ix)
   48CF DD 66 FA      [19] 1453 	ld	h,-6 (ix)
   48D2 E5            [11] 1454 	push	hl
   48D3 DD 6E FB      [19] 1455 	ld	l,-5 (ix)
   48D6 DD 66 FC      [19] 1456 	ld	h,-4 (ix)
   48D9 E5            [11] 1457 	push	hl
   48DA CD 19 40      [17] 1458 	call	_rect_overlap
   48DD FD 21 0C 00   [14] 1459 	ld	iy, #12
   48E1 FD 39         [15] 1460 	add	iy, sp
   48E3 FD F9         [10] 1461 	ld	sp, iy
   48E5 7D            [ 4] 1462 	ld	a, l
   48E6 B7            [ 4] 1463 	or	a, a
   48E7 28 16         [12] 1464 	jr	Z,00154$
                           1465 ;src/game.c:251: g_pickuptaken = 1;
   48E9 21 57 5F      [10] 1466 	ld	hl,#_g_pickuptaken + 0
   48EC 36 01         [10] 1467 	ld	(hl), #0x01
                           1468 ;src/game.c:252: g_weaponlevel = 1;
   48EE 21 56 5F      [10] 1469 	ld	hl,#_g_weaponlevel + 0
   48F1 36 01         [10] 1470 	ld	(hl), #0x01
                           1471 ;src/game.c:253: g_score = (u16)(g_score + 100);
   48F3 21 3A 5F      [10] 1472 	ld	hl, #_g_score
   48F6 7E            [ 7] 1473 	ld	a, (hl)
   48F7 C6 64         [ 7] 1474 	add	a, #0x64
   48F9 77            [ 7] 1475 	ld	(hl), a
   48FA 23            [ 6] 1476 	inc	hl
   48FB 7E            [ 7] 1477 	ld	a, (hl)
   48FC CE 00         [ 7] 1478 	adc	a, #0x00
   48FE 77            [ 7] 1479 	ld	(hl), a
   48FF                    1480 00154$:
                           1481 ;src/game.c:256: g_weapondisplay = (u8)(g_weaponlevel + 1);
   48FF 21 3D 5F      [10] 1482 	ld	hl, #_g_weapondisplay
   4902 3A 56 5F      [13] 1483 	ld	a,(#_g_weaponlevel + 0)
   4905 3C            [ 4] 1484 	inc	a
   4906 77            [ 7] 1485 	ld	(hl), a
                           1486 ;src/game.c:258: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   4907 3A 54 5F      [13] 1487 	ld	a,(#_g_bossactive + 0)
   490A B7            [ 4] 1488 	or	a, a
   490B 20 45         [12] 1489 	jr	NZ,00165$
   490D 3A 3F 5F      [13] 1490 	ld	a,(#_g_aliveenemies + 0)
   4910 B7            [ 4] 1491 	or	a, a
   4911 20 3F         [12] 1492 	jr	NZ,00165$
   4913 3A 44 5F      [13] 1493 	ld	a,(#_g_gameover + 0)
   4916 B7            [ 4] 1494 	or	a, a
   4917 20 39         [12] 1495 	jr	NZ,00165$
                           1496 ;src/game.c:259: if (g_currentwave < TOTAL_WAVES) {
   4919 3A 3E 5F      [13] 1497 	ld	a,(#_g_currentwave + 0)
   491C D6 03         [ 7] 1498 	sub	a, #0x03
   491E 30 20         [12] 1499 	jr	NC,00162$
                           1500 ;src/game.c:260: if (g_wavecooldown == 0) {
   4920 3A 40 5F      [13] 1501 	ld	a,(#_g_wavecooldown + 0)
   4923 B7            [ 4] 1502 	or	a, a
   4924 20 14         [12] 1503 	jr	NZ,00157$
                           1504 ;src/game.c:261: spawn_wave(g_currentwave);
   4926 3A 3E 5F      [13] 1505 	ld	a, (_g_currentwave)
   4929 F5            [11] 1506 	push	af
   492A 33            [ 6] 1507 	inc	sp
   492B CD A6 40      [17] 1508 	call	_spawn_wave
   492E 33            [ 6] 1509 	inc	sp
                           1510 ;src/game.c:262: g_currentwave++;
   492F 21 3E 5F      [10] 1511 	ld	hl, #_g_currentwave+0
   4932 34            [11] 1512 	inc	(hl)
                           1513 ;src/game.c:263: g_wavecooldown = 90;
   4933 21 40 5F      [10] 1514 	ld	hl,#_g_wavecooldown + 0
   4936 36 5A         [10] 1515 	ld	(hl), #0x5a
   4938 18 18         [12] 1516 	jr	00165$
   493A                    1517 00157$:
                           1518 ;src/game.c:265: g_wavecooldown--;
   493A 21 40 5F      [10] 1519 	ld	hl, #_g_wavecooldown+0
   493D 35            [11] 1520 	dec	(hl)
   493E 18 12         [12] 1521 	jr	00165$
   4940                    1522 00162$:
                           1523 ;src/game.c:267: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   4940 21 B8 5E      [10] 1524 	ld	hl, #_g_player + 0
   4943 4E            [ 7] 1525 	ld	c, (hl)
   4944 C5            [11] 1526 	push	bc
   4945 CD 28 51      [17] 1527 	call	_tilemap_goal_x
   4948 C1            [10] 1528 	pop	bc
   4949 2D            [ 4] 1529 	dec	l
   494A 2D            [ 4] 1530 	dec	l
   494B 79            [ 4] 1531 	ld	a, c
   494C 95            [ 4] 1532 	sub	a, l
   494D 38 03         [12] 1533 	jr	C,00165$
                           1534 ;src/game.c:268: spawn_boss();
   494F CD A6 41      [17] 1535 	call	_spawn_boss
   4952                    1536 00165$:
                           1537 ;src/game.c:272: g_framecounter++;
   4952 FD 21 45 5F   [14] 1538 	ld	iy, #_g_framecounter
   4956 FD 34 00      [23] 1539 	inc	0 (iy)
   4959 20 03         [12] 1540 	jr	NZ,00381$
   495B FD 34 01      [23] 1541 	inc	1 (iy)
   495E                    1542 00381$:
                           1543 ;src/game.c:273: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   495E 21 32 00      [10] 1544 	ld	hl, #0x0032
   4961 E5            [11] 1545 	push	hl
   4962 2A 45 5F      [16] 1546 	ld	hl, (_g_framecounter)
   4965 E5            [11] 1547 	push	hl
   4966 CD 96 5D      [17] 1548 	call	__moduint
   4969 F1            [10] 1549 	pop	af
   496A F1            [10] 1550 	pop	af
   496B 7C            [ 4] 1551 	ld	a, h
   496C B5            [ 4] 1552 	or	a,l
   496D 20 0D         [12] 1553 	jr	NZ,00169$
   496F FD 21 3C 5F   [14] 1554 	ld	iy, #_g_timeleft
   4973 FD 7E 00      [19] 1555 	ld	a, 0 (iy)
   4976 B7            [ 4] 1556 	or	a, a
   4977 28 03         [12] 1557 	jr	Z,00169$
                           1558 ;src/game.c:274: g_timeleft--;
   4979 FD 35 00      [23] 1559 	dec	0 (iy)
   497C                    1560 00169$:
                           1561 ;src/game.c:276: if (g_timeleft == 0 && !g_victory) {
   497C 3A 3C 5F      [13] 1562 	ld	a,(#_g_timeleft + 0)
   497F B7            [ 4] 1563 	or	a, a
   4980 20 0B         [12] 1564 	jr	NZ,00172$
   4982 3A 43 5F      [13] 1565 	ld	a,(#_g_victory + 0)
   4985 B7            [ 4] 1566 	or	a, a
   4986 20 05         [12] 1567 	jr	NZ,00172$
                           1568 ;src/game.c:277: g_gameover = 1;
   4988 21 44 5F      [10] 1569 	ld	hl,#_g_gameover + 0
   498B 36 01         [10] 1570 	ld	(hl), #0x01
   498D                    1571 00172$:
                           1572 ;src/game.c:280: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   498D 3A 3D 5F      [13] 1573 	ld	a, (_g_weapondisplay)
   4990 F5            [11] 1574 	push	af
   4991 33            [ 6] 1575 	inc	sp
   4992 3A 3C 5F      [13] 1576 	ld	a, (_g_timeleft)
   4995 F5            [11] 1577 	push	af
   4996 33            [ 6] 1578 	inc	sp
   4997 2A 3A 5F      [16] 1579 	ld	hl, (_g_score)
   499A E5            [11] 1580 	push	hl
   499B 3A 39 5F      [13] 1581 	ld	a, (_g_lives)
   499E F5            [11] 1582 	push	af
   499F 33            [ 6] 1583 	inc	sp
   49A0 CD 3C 4E      [17] 1584 	call	_hudupdate
   49A3 F1            [10] 1585 	pop	af
   49A4 F1            [10] 1586 	pop	af
   49A5 33            [ 6] 1587 	inc	sp
   49A6                    1588 00181$:
   49A6 DD F9         [10] 1589 	ld	sp, ix
   49A8 DD E1         [14] 1590 	pop	ix
   49AA C9            [10] 1591 	ret
                           1592 ;src/game.c:283: void game_render(void) {
                           1593 ;	---------------------------------
                           1594 ; Function game_render
                           1595 ; ---------------------------------
   49AB                    1596 _game_render::
                           1597 ;src/game.c:286: cpct_clearScreen(0x00);
   49AB 21 00 40      [10] 1598 	ld	hl, #0x4000
   49AE E5            [11] 1599 	push	hl
   49AF AF            [ 4] 1600 	xor	a, a
   49B0 F5            [11] 1601 	push	af
   49B1 33            [ 6] 1602 	inc	sp
   49B2 26 C0         [ 7] 1603 	ld	h, #0xc0
   49B4 E5            [11] 1604 	push	hl
   49B5 CD C1 5D      [17] 1605 	call	_cpct_memset
                           1606 ;src/game.c:287: tilemap_render();
   49B8 CD 03 50      [17] 1607 	call	_tilemap_render
                           1608 ;src/game.c:289: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49BB 0E 00         [ 7] 1609 	ld	c, #0x00
   49BD                    1610 00115$:
                           1611 ;src/game.c:290: projectilerender(&g_projectiles[i]);
   49BD 06 00         [ 7] 1612 	ld	b,#0x00
   49BF 69            [ 4] 1613 	ld	l, c
   49C0 60            [ 4] 1614 	ld	h, b
   49C1 29            [11] 1615 	add	hl, hl
   49C2 29            [11] 1616 	add	hl, hl
   49C3 09            [11] 1617 	add	hl, bc
   49C4 29            [11] 1618 	add	hl, hl
   49C5 11 FD 5E      [10] 1619 	ld	de, #_g_projectiles
   49C8 19            [11] 1620 	add	hl, de
   49C9 C5            [11] 1621 	push	bc
   49CA E5            [11] 1622 	push	hl
   49CB CD 9A 5B      [17] 1623 	call	_projectilerender
   49CE F1            [10] 1624 	pop	af
   49CF C1            [10] 1625 	pop	bc
                           1626 ;src/game.c:289: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49D0 0C            [ 4] 1627 	inc	c
   49D1 79            [ 4] 1628 	ld	a, c
   49D2 D6 06         [ 7] 1629 	sub	a, #0x06
   49D4 38 E7         [12] 1630 	jr	C,00115$
                           1631 ;src/game.c:293: for (i = 0; i < MAX_ENEMIES; ++i) {
   49D6 0E 00         [ 7] 1632 	ld	c, #0x00
   49D8                    1633 00117$:
                           1634 ;src/game.c:294: enemyrender(&g_enemies[i]);
   49D8 06 00         [ 7] 1635 	ld	b,#0x00
   49DA 69            [ 4] 1636 	ld	l, c
   49DB 60            [ 4] 1637 	ld	h, b
   49DC 29            [11] 1638 	add	hl, hl
   49DD 29            [11] 1639 	add	hl, hl
   49DE 09            [11] 1640 	add	hl, bc
   49DF 29            [11] 1641 	add	hl, hl
   49E0 11 C1 5E      [10] 1642 	ld	de, #_g_enemies
   49E3 19            [11] 1643 	add	hl, de
   49E4 C5            [11] 1644 	push	bc
   49E5 E5            [11] 1645 	push	hl
   49E6 CD 8B 55      [17] 1646 	call	_enemyrender
   49E9 F1            [10] 1647 	pop	af
   49EA C1            [10] 1648 	pop	bc
                           1649 ;src/game.c:293: for (i = 0; i < MAX_ENEMIES; ++i) {
   49EB 0C            [ 4] 1650 	inc	c
   49EC 79            [ 4] 1651 	ld	a, c
   49ED D6 06         [ 7] 1652 	sub	a, #0x06
   49EF 38 E7         [12] 1653 	jr	C,00117$
                           1654 ;src/game.c:297: if (g_bossactive) {
   49F1 3A 54 5F      [13] 1655 	ld	a,(#_g_bossactive + 0)
   49F4 B7            [ 4] 1656 	or	a, a
   49F5 28 45         [12] 1657 	jr	Z,00104$
                           1658 ;src/game.c:298: enemyrender(&g_boss);
   49F7 21 4A 5F      [10] 1659 	ld	hl, #_g_boss
   49FA E5            [11] 1660 	push	hl
   49FB CD 8B 55      [17] 1661 	call	_enemyrender
                           1662 ;src/game.c:299: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x44, 32, 2);
   49FE 21 18 0A      [10] 1663 	ld	hl, #0x0a18
   4A01 E3            [19] 1664 	ex	(sp),hl
   4A02 21 00 C0      [10] 1665 	ld	hl, #0xc000
   4A05 E5            [11] 1666 	push	hl
   4A06 CD 98 5E      [17] 1667 	call	_cpct_getScreenPtr
   4A09 01 20 02      [10] 1668 	ld	bc, #0x0220
   4A0C C5            [11] 1669 	push	bc
   4A0D 3E 44         [ 7] 1670 	ld	a, #0x44
   4A0F F5            [11] 1671 	push	af
   4A10 33            [ 6] 1672 	inc	sp
   4A11 E5            [11] 1673 	push	hl
   4A12 CD DF 5D      [17] 1674 	call	_cpct_drawSolidBox
   4A15 F1            [10] 1675 	pop	af
   4A16 F1            [10] 1676 	pop	af
   4A17 33            [ 6] 1677 	inc	sp
                           1678 ;src/game.c:300: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x5C, (u8)(g_boss.health * 3), 2);
   4A18 3A 51 5F      [13] 1679 	ld	a, (#_g_boss + 7)
   4A1B 4F            [ 4] 1680 	ld	c, a
   4A1C 87            [ 4] 1681 	add	a, a
   4A1D 81            [ 4] 1682 	add	a, c
   4A1E 57            [ 4] 1683 	ld	d, a
   4A1F D5            [11] 1684 	push	de
   4A20 21 18 0A      [10] 1685 	ld	hl, #0x0a18
   4A23 E5            [11] 1686 	push	hl
   4A24 21 00 C0      [10] 1687 	ld	hl, #0xc000
   4A27 E5            [11] 1688 	push	hl
   4A28 CD 98 5E      [17] 1689 	call	_cpct_getScreenPtr
   4A2B 4D            [ 4] 1690 	ld	c, l
   4A2C 44            [ 4] 1691 	ld	b, h
   4A2D D1            [10] 1692 	pop	de
   4A2E 3E 02         [ 7] 1693 	ld	a, #0x02
   4A30 F5            [11] 1694 	push	af
   4A31 33            [ 6] 1695 	inc	sp
   4A32 1E 5C         [ 7] 1696 	ld	e, #0x5c
   4A34 D5            [11] 1697 	push	de
   4A35 C5            [11] 1698 	push	bc
   4A36 CD DF 5D      [17] 1699 	call	_cpct_drawSolidBox
   4A39 F1            [10] 1700 	pop	af
   4A3A F1            [10] 1701 	pop	af
   4A3B 33            [ 6] 1702 	inc	sp
   4A3C                    1703 00104$:
                           1704 ;src/game.c:303: if (!g_pickuptaken) {
   4A3C 3A 57 5F      [13] 1705 	ld	a,(#_g_pickuptaken + 0)
   4A3F B7            [ 4] 1706 	or	a, a
   4A40 20 23         [12] 1707 	jr	NZ,00106$
                           1708 ;src/game.c:304: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), 0xEE, 4, 4);
   4A42 CD 84 50      [17] 1709 	call	_tilemap_ground_y
   4A45 7D            [ 4] 1710 	ld	a, l
   4A46 C6 F8         [ 7] 1711 	add	a, #0xf8
   4A48 47            [ 4] 1712 	ld	b, a
   4A49 C5            [11] 1713 	push	bc
   4A4A 33            [ 6] 1714 	inc	sp
   4A4B 3E 24         [ 7] 1715 	ld	a, #0x24
   4A4D F5            [11] 1716 	push	af
   4A4E 33            [ 6] 1717 	inc	sp
   4A4F 21 00 C0      [10] 1718 	ld	hl, #0xc000
   4A52 E5            [11] 1719 	push	hl
   4A53 CD 98 5E      [17] 1720 	call	_cpct_getScreenPtr
   4A56 01 04 04      [10] 1721 	ld	bc, #0x0404
   4A59 C5            [11] 1722 	push	bc
   4A5A 3E EE         [ 7] 1723 	ld	a, #0xee
   4A5C F5            [11] 1724 	push	af
   4A5D 33            [ 6] 1725 	inc	sp
   4A5E E5            [11] 1726 	push	hl
   4A5F CD DF 5D      [17] 1727 	call	_cpct_drawSolidBox
   4A62 F1            [10] 1728 	pop	af
   4A63 F1            [10] 1729 	pop	af
   4A64 33            [ 6] 1730 	inc	sp
   4A65                    1731 00106$:
                           1732 ;src/game.c:306: playerrender(&g_player);
   4A65 21 B8 5E      [10] 1733 	ld	hl, #_g_player
   4A68 E5            [11] 1734 	push	hl
   4A69 CD FA 59      [17] 1735 	call	_playerrender
   4A6C F1            [10] 1736 	pop	af
                           1737 ;src/game.c:307: hudrender();
   4A6D CD 6D 4E      [17] 1738 	call	_hudrender
                           1739 ;src/game.c:309: if (g_victory) {
   4A70 3A 43 5F      [13] 1740 	ld	a,(#_g_victory + 0)
   4A73 B7            [ 4] 1741 	or	a, a
   4A74 28 34         [12] 1742 	jr	Z,00113$
                           1743 ;src/game.c:310: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x5A, 32, 12);
   4A76 21 18 44      [10] 1744 	ld	hl, #0x4418
   4A79 E5            [11] 1745 	push	hl
   4A7A 21 00 C0      [10] 1746 	ld	hl, #0xc000
   4A7D E5            [11] 1747 	push	hl
   4A7E CD 98 5E      [17] 1748 	call	_cpct_getScreenPtr
   4A81 01 20 0C      [10] 1749 	ld	bc, #0x0c20
   4A84 C5            [11] 1750 	push	bc
   4A85 3E 5A         [ 7] 1751 	ld	a, #0x5a
   4A87 F5            [11] 1752 	push	af
   4A88 33            [ 6] 1753 	inc	sp
   4A89 E5            [11] 1754 	push	hl
   4A8A CD DF 5D      [17] 1755 	call	_cpct_drawSolidBox
   4A8D F1            [10] 1756 	pop	af
                           1757 ;src/game.c:311: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
   4A8E 33            [ 6] 1758 	inc	sp
   4A8F 21 1C 48      [10] 1759 	ld	hl,#0x481c
   4A92 E3            [19] 1760 	ex	(sp),hl
   4A93 21 00 C0      [10] 1761 	ld	hl, #0xc000
   4A96 E5            [11] 1762 	push	hl
   4A97 CD 98 5E      [17] 1763 	call	_cpct_getScreenPtr
   4A9A 01 18 08      [10] 1764 	ld	bc, #0x0818
   4A9D C5            [11] 1765 	push	bc
   4A9E 3E 5C         [ 7] 1766 	ld	a, #0x5c
   4AA0 F5            [11] 1767 	push	af
   4AA1 33            [ 6] 1768 	inc	sp
   4AA2 E5            [11] 1769 	push	hl
   4AA3 CD DF 5D      [17] 1770 	call	_cpct_drawSolidBox
   4AA6 F1            [10] 1771 	pop	af
   4AA7 F1            [10] 1772 	pop	af
   4AA8 33            [ 6] 1773 	inc	sp
   4AA9 C9            [10] 1774 	ret
   4AAA                    1775 00113$:
                           1776 ;src/game.c:312: } else if (g_gameover) {
   4AAA 3A 44 5F      [13] 1777 	ld	a,(#_g_gameover + 0)
   4AAD B7            [ 4] 1778 	or	a, a
   4AAE 28 34         [12] 1779 	jr	Z,00110$
                           1780 ;src/game.c:313: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x44, 32, 12);
   4AB0 21 18 44      [10] 1781 	ld	hl, #0x4418
   4AB3 E5            [11] 1782 	push	hl
   4AB4 21 00 C0      [10] 1783 	ld	hl, #0xc000
   4AB7 E5            [11] 1784 	push	hl
   4AB8 CD 98 5E      [17] 1785 	call	_cpct_getScreenPtr
   4ABB 01 20 0C      [10] 1786 	ld	bc, #0x0c20
   4ABE C5            [11] 1787 	push	bc
   4ABF 3E 44         [ 7] 1788 	ld	a, #0x44
   4AC1 F5            [11] 1789 	push	af
   4AC2 33            [ 6] 1790 	inc	sp
   4AC3 E5            [11] 1791 	push	hl
   4AC4 CD DF 5D      [17] 1792 	call	_cpct_drawSolidBox
   4AC7 F1            [10] 1793 	pop	af
                           1794 ;src/game.c:314: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
   4AC8 33            [ 6] 1795 	inc	sp
   4AC9 21 1C 48      [10] 1796 	ld	hl,#0x481c
   4ACC E3            [19] 1797 	ex	(sp),hl
   4ACD 21 00 C0      [10] 1798 	ld	hl, #0xc000
   4AD0 E5            [11] 1799 	push	hl
   4AD1 CD 98 5E      [17] 1800 	call	_cpct_getScreenPtr
   4AD4 01 18 08      [10] 1801 	ld	bc, #0x0818
   4AD7 C5            [11] 1802 	push	bc
   4AD8 3E 4C         [ 7] 1803 	ld	a, #0x4c
   4ADA F5            [11] 1804 	push	af
   4ADB 33            [ 6] 1805 	inc	sp
   4ADC E5            [11] 1806 	push	hl
   4ADD CD DF 5D      [17] 1807 	call	_cpct_drawSolidBox
   4AE0 F1            [10] 1808 	pop	af
   4AE1 F1            [10] 1809 	pop	af
   4AE2 33            [ 6] 1810 	inc	sp
   4AE3 C9            [10] 1811 	ret
   4AE4                    1812 00110$:
                           1813 ;src/game.c:315: } else if (g_checkpointactive) {
   4AE4 3A 49 5F      [13] 1814 	ld	a,(#_g_checkpointactive + 0)
   4AE7 B7            [ 4] 1815 	or	a, a
   4AE8 C8            [11] 1816 	ret	Z
                           1817 ;src/game.c:316: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), 0x3A, 2, 8);
   4AE9 3A 48 5F      [13] 1818 	ld	a,(#_g_checkpointy + 0)
   4AEC C6 F8         [ 7] 1819 	add	a, #0xf8
   4AEE 47            [ 4] 1820 	ld	b, a
   4AEF C5            [11] 1821 	push	bc
   4AF0 33            [ 6] 1822 	inc	sp
   4AF1 3A 47 5F      [13] 1823 	ld	a, (_g_checkpointx)
   4AF4 F5            [11] 1824 	push	af
   4AF5 33            [ 6] 1825 	inc	sp
   4AF6 21 00 C0      [10] 1826 	ld	hl, #0xc000
   4AF9 E5            [11] 1827 	push	hl
   4AFA CD 98 5E      [17] 1828 	call	_cpct_getScreenPtr
   4AFD 01 02 08      [10] 1829 	ld	bc, #0x0802
   4B00 C5            [11] 1830 	push	bc
   4B01 3E 3A         [ 7] 1831 	ld	a, #0x3a
   4B03 F5            [11] 1832 	push	af
   4B04 33            [ 6] 1833 	inc	sp
   4B05 E5            [11] 1834 	push	hl
   4B06 CD DF 5D      [17] 1835 	call	_cpct_drawSolidBox
   4B09 F1            [10] 1836 	pop	af
   4B0A F1            [10] 1837 	pop	af
   4B0B 33            [ 6] 1838 	inc	sp
   4B0C C9            [10] 1839 	ret
                           1840 	.area _CODE
                           1841 	.area _INITIALIZER
                           1842 	.area _CABS (ABS)
