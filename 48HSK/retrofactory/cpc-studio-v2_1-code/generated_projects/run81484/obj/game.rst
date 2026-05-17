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
                             11 	.globl ___game_entry_jp
                             12 	.globl _hudrender
                             13 	.globl _hudupdate
                             14 	.globl _hudinit
                             15 	.globl _projectilerender
                             16 	.globl _projectileupdate
                             17 	.globl _projectilefire
                             18 	.globl _projectileinit
                             19 	.globl _enemydamage
                             20 	.globl _enemyrender
                             21 	.globl _enemyupdate
                             22 	.globl _enemyspawn
                             23 	.globl _enemyinit
                             24 	.globl _playerrender
                             25 	.globl _playerupdate
                             26 	.globl _playerinit
                             27 	.globl _collision_is_on_trap
                             28 	.globl _collision_init
                             29 	.globl _input_is_shoot_just_pressed
                             30 	.globl _input_is_shoot_pressed
                             31 	.globl _input_is_jump_pressed
                             32 	.globl _input_is_right_pressed
                             33 	.globl _input_is_left_pressed
                             34 	.globl _input_update
                             35 	.globl _tilemap_goal_x
                             36 	.globl _tilemap_ground_y
                             37 	.globl _tilemap_render
                             38 	.globl _tilemap_init
                             39 	.globl _cpct_getScreenPtr
                             40 	.globl _cpct_setPALColour
                             41 	.globl _cpct_setPalette
                             42 	.globl _cpct_setVideoMode
                             43 	.globl _cpct_drawSolidBox
                             44 	.globl _cpct_px2byteM0
                             45 	.globl _cpct_memset
                             46 	.globl _cpct_disableFirmware
                             47 	.globl _game_init
                             48 	.globl _game_update
                             49 	.globl _game_render
                             50 ;--------------------------------------------------------
                             51 ; special function registers
                             52 ;--------------------------------------------------------
                             53 ;--------------------------------------------------------
                             54 ; ram data
                             55 ;--------------------------------------------------------
                             56 	.area _DATA
   6BD5                      57 _g_player:
   6BD5                      58 	.ds 10
   6BDF                      59 _g_enemies:
   6BDF                      60 	.ds 60
   6C1B                      61 _g_projectiles:
   6C1B                      62 	.ds 60
   6C57                      63 _prev_enemy_x:
   6C57                      64 	.ds 6
   6C5D                      65 _prev_enemy_y:
   6C5D                      66 	.ds 6
   6C63                      67 _prev_enemy_w:
   6C63                      68 	.ds 6
   6C69                      69 _prev_enemy_h:
   6C69                      70 	.ds 6
   6C6F                      71 _prev_enemy_act:
   6C6F                      72 	.ds 6
   6C75                      73 _prev_boss_x:
   6C75                      74 	.ds 1
   6C76                      75 _prev_boss_y:
   6C76                      76 	.ds 1
   6C77                      77 _prev_boss_act:
   6C77                      78 	.ds 1
   6C78                      79 _prev_proj_x:
   6C78                      80 	.ds 6
   6C7E                      81 _prev_proj_y:
   6C7E                      82 	.ds 6
   6C84                      83 _prev_proj_w:
   6C84                      84 	.ds 6
   6C8A                      85 _prev_proj_h:
   6C8A                      86 	.ds 6
   6C90                      87 _prev_proj_act:
   6C90                      88 	.ds 6
   6C96                      89 _g_lives:
   6C96                      90 	.ds 1
   6C97                      91 _g_score:
   6C97                      92 	.ds 2
   6C99                      93 _g_timeleft:
   6C99                      94 	.ds 1
   6C9A                      95 _g_weapondisplay:
   6C9A                      96 	.ds 1
   6C9B                      97 _g_currentwave:
   6C9B                      98 	.ds 1
   6C9C                      99 _g_aliveenemies:
   6C9C                     100 	.ds 1
   6C9D                     101 _g_wavecooldown:
   6C9D                     102 	.ds 1
   6C9E                     103 _g_damagecooldown:
   6C9E                     104 	.ds 1
   6C9F                     105 _g_shootcooldown:
   6C9F                     106 	.ds 1
   6CA0                     107 _g_victory:
   6CA0                     108 	.ds 1
   6CA1                     109 _g_gameover:
   6CA1                     110 	.ds 1
   6CA2                     111 _g_framecounter:
   6CA2                     112 	.ds 2
   6CA4                     113 _g_checkpointx:
   6CA4                     114 	.ds 1
   6CA5                     115 _g_checkpointy:
   6CA5                     116 	.ds 1
   6CA6                     117 _g_checkpointactive:
   6CA6                     118 	.ds 1
   6CA7                     119 _g_boss:
   6CA7                     120 	.ds 10
   6CB1                     121 _g_bossactive:
   6CB1                     122 	.ds 1
   6CB2                     123 _g_bossphase:
   6CB2                     124 	.ds 1
   6CB3                     125 _g_weaponlevel:
   6CB3                     126 	.ds 1
   6CB4                     127 _g_pickuptaken:
   6CB4                     128 	.ds 1
   6CB5                     129 _g_dbg_left:
   6CB5                     130 	.ds 1
   6CB6                     131 _g_dbg_right:
   6CB6                     132 	.ds 1
   6CB7                     133 _g_dbg_jump:
   6CB7                     134 	.ds 1
   6CB8                     135 _g_dbg_shoot:
   6CB8                     136 	.ds 1
   6CB9                     137 _g_dbg_move_raw:
   6CB9                     138 	.ds 1
   6CBA                     139 _g_dbg_move_net:
   6CBA                     140 	.ds 1
   6CBB                     141 _g_dbg_move_cancelled:
   6CBB                     142 	.ds 1
   6CBC                     143 _g_dbg_hit:
   6CBC                     144 	.ds 1
   6CBD                     145 _g_dbg_vx:
   6CBD                     146 	.ds 1
                            147 ;--------------------------------------------------------
                            148 ; ram data
                            149 ;--------------------------------------------------------
                            150 	.area _INITIALIZED
   6D8D                     151 _prev_player_x:
   6D8D                     152 	.ds 1
   6D8E                     153 _prev_player_y:
   6D8E                     154 	.ds 1
                            155 ;--------------------------------------------------------
                            156 ; absolute external ram data
                            157 ;--------------------------------------------------------
                            158 	.area _DABS (ABS)
                            159 ;--------------------------------------------------------
                            160 ; global & static initialisations
                            161 ;--------------------------------------------------------
                            162 	.area _HOME
                            163 	.area _GSINIT
                            164 	.area _GSFINAL
                            165 	.area _GSINIT
                            166 ;--------------------------------------------------------
                            167 ; Home
                            168 ;--------------------------------------------------------
                            169 	.area _HOME
                            170 	.area _HOME
                            171 ;--------------------------------------------------------
                            172 ; code
                            173 ;--------------------------------------------------------
                            174 	.area _CODE
                            175 ;src/game.c:15: void __game_entry_jp(void) __naked {
                            176 ;	---------------------------------
                            177 ; Function __game_entry_jp
                            178 ; ---------------------------------
   4000                     179 ___game_entry_jp::
                            180 ;src/game.c:19: __endasm;
                            181 	.globl	cpc_run_address
   4000 C3 69 52      [10]  182 	jp	cpc_run_address
                            183 ;src/game.c:72: static void reset_player_to_checkpoint(void) {
                            184 ;	---------------------------------
                            185 ; Function reset_player_to_checkpoint
                            186 ; ---------------------------------
   4003                     187 _reset_player_to_checkpoint:
                            188 ;src/game.c:73: g_player.x = g_checkpointx;
   4003 21 D5 6B      [10]  189 	ld	hl, #_g_player
   4006 3A A4 6C      [13]  190 	ld	a,(#_g_checkpointx + 0)
   4009 77            [ 7]  191 	ld	(hl), a
                            192 ;src/game.c:74: g_player.y = g_checkpointy;
   400A 21 D6 6B      [10]  193 	ld	hl, #(_g_player + 0x0001)
   400D 3A A5 6C      [13]  194 	ld	a,(#_g_checkpointy + 0)
   4010 77            [ 7]  195 	ld	(hl), a
                            196 ;src/game.c:75: g_player.vx = 0;
   4011 21 D7 6B      [10]  197 	ld	hl, #(_g_player + 0x0002)
   4014 36 00         [10]  198 	ld	(hl), #0x00
                            199 ;src/game.c:76: g_player.vy = 0;
   4016 21 D8 6B      [10]  200 	ld	hl, #(_g_player + 0x0003)
   4019 36 00         [10]  201 	ld	(hl), #0x00
   401B C9            [10]  202 	ret
                            203 ;src/game.c:79: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
                            204 ;	---------------------------------
                            205 ; Function rect_overlap
                            206 ; ---------------------------------
   401C                     207 _rect_overlap:
   401C DD E5         [15]  208 	push	ix
   401E DD 21 00 00   [14]  209 	ld	ix,#0
   4022 DD 39         [15]  210 	add	ix,sp
                            211 ;src/game.c:80: if (ax + aw <= bx) return 0;
   4024 DD 4E 08      [19]  212 	ld	c, 8 (ix)
   4027 06 00         [ 7]  213 	ld	b, #0x00
   4029 DD 6E 04      [19]  214 	ld	l,4 (ix)
   402C DD 66 05      [19]  215 	ld	h,5 (ix)
   402F 09            [11]  216 	add	hl, bc
   4030 DD 7E 0A      [19]  217 	ld	a, 10 (ix)
   4033 95            [ 4]  218 	sub	a, l
   4034 DD 7E 0B      [19]  219 	ld	a, 11 (ix)
   4037 9C            [ 4]  220 	sbc	a, h
   4038 E2 3D 40      [10]  221 	jp	PO, 00127$
   403B EE 80         [ 7]  222 	xor	a, #0x80
   403D                     223 00127$:
   403D FA 44 40      [10]  224 	jp	M, 00102$
   4040 2E 00         [ 7]  225 	ld	l, #0x00
   4042 18 62         [12]  226 	jr	00109$
   4044                     227 00102$:
                            228 ;src/game.c:81: if (bx + bw <= ax) return 0;
   4044 DD 4E 0E      [19]  229 	ld	c, 14 (ix)
   4047 06 00         [ 7]  230 	ld	b, #0x00
   4049 DD 6E 0A      [19]  231 	ld	l,10 (ix)
   404C DD 66 0B      [19]  232 	ld	h,11 (ix)
   404F 09            [11]  233 	add	hl, bc
   4050 DD 7E 04      [19]  234 	ld	a, 4 (ix)
   4053 95            [ 4]  235 	sub	a, l
   4054 DD 7E 05      [19]  236 	ld	a, 5 (ix)
   4057 9C            [ 4]  237 	sbc	a, h
   4058 E2 5D 40      [10]  238 	jp	PO, 00128$
   405B EE 80         [ 7]  239 	xor	a, #0x80
   405D                     240 00128$:
   405D FA 64 40      [10]  241 	jp	M, 00104$
   4060 2E 00         [ 7]  242 	ld	l, #0x00
   4062 18 42         [12]  243 	jr	00109$
   4064                     244 00104$:
                            245 ;src/game.c:82: if (ay + ah <= by) return 0;
   4064 DD 4E 09      [19]  246 	ld	c, 9 (ix)
   4067 06 00         [ 7]  247 	ld	b, #0x00
   4069 DD 6E 06      [19]  248 	ld	l,6 (ix)
   406C DD 66 07      [19]  249 	ld	h,7 (ix)
   406F 09            [11]  250 	add	hl, bc
   4070 DD 7E 0C      [19]  251 	ld	a, 12 (ix)
   4073 95            [ 4]  252 	sub	a, l
   4074 DD 7E 0D      [19]  253 	ld	a, 13 (ix)
   4077 9C            [ 4]  254 	sbc	a, h
   4078 E2 7D 40      [10]  255 	jp	PO, 00129$
   407B EE 80         [ 7]  256 	xor	a, #0x80
   407D                     257 00129$:
   407D FA 84 40      [10]  258 	jp	M, 00106$
   4080 2E 00         [ 7]  259 	ld	l, #0x00
   4082 18 22         [12]  260 	jr	00109$
   4084                     261 00106$:
                            262 ;src/game.c:83: if (by + bh <= ay) return 0;
   4084 DD 4E 0F      [19]  263 	ld	c, 15 (ix)
   4087 06 00         [ 7]  264 	ld	b, #0x00
   4089 DD 6E 0C      [19]  265 	ld	l,12 (ix)
   408C DD 66 0D      [19]  266 	ld	h,13 (ix)
   408F 09            [11]  267 	add	hl, bc
   4090 DD 7E 06      [19]  268 	ld	a, 6 (ix)
   4093 95            [ 4]  269 	sub	a, l
   4094 DD 7E 07      [19]  270 	ld	a, 7 (ix)
   4097 9C            [ 4]  271 	sbc	a, h
   4098 E2 9D 40      [10]  272 	jp	PO, 00130$
   409B EE 80         [ 7]  273 	xor	a, #0x80
   409D                     274 00130$:
   409D FA A4 40      [10]  275 	jp	M, 00108$
   40A0 2E 00         [ 7]  276 	ld	l, #0x00
   40A2 18 02         [12]  277 	jr	00109$
   40A4                     278 00108$:
                            279 ;src/game.c:84: return 1;
   40A4 2E 01         [ 7]  280 	ld	l, #0x01
   40A6                     281 00109$:
   40A6 DD E1         [14]  282 	pop	ix
   40A8 C9            [10]  283 	ret
                            284 ;src/game.c:87: static void spawn_wave(u8 wave) {
                            285 ;	---------------------------------
                            286 ; Function spawn_wave
                            287 ; ---------------------------------
   40A9                     288 _spawn_wave:
   40A9 DD E5         [15]  289 	push	ix
   40AB DD 21 00 00   [14]  290 	ld	ix,#0
   40AF DD 39         [15]  291 	add	ix,sp
   40B1 F5            [11]  292 	push	af
   40B2 F5            [11]  293 	push	af
   40B3 3B            [ 6]  294 	dec	sp
                            295 ;src/game.c:91: for (i = 0; i < MAX_ENEMIES; ++i) {
   40B4 01 DF 6B      [10]  296 	ld	bc, #_g_enemies+0
   40B7 1E 00         [ 7]  297 	ld	e, #0x00
   40B9                     298 00119$:
                            299 ;src/game.c:92: enemyinit(&g_enemies[i]);
   40B9 D5            [11]  300 	push	de
   40BA 16 00         [ 7]  301 	ld	d,#0x00
   40BC 6B            [ 4]  302 	ld	l, e
   40BD 62            [ 4]  303 	ld	h, d
   40BE 29            [11]  304 	add	hl, hl
   40BF 29            [11]  305 	add	hl, hl
   40C0 19            [11]  306 	add	hl, de
   40C1 29            [11]  307 	add	hl, hl
   40C2 D1            [10]  308 	pop	de
   40C3 09            [11]  309 	add	hl, bc
   40C4 C5            [11]  310 	push	bc
   40C5 D5            [11]  311 	push	de
   40C6 E5            [11]  312 	push	hl
   40C7 CD 18 5D      [17]  313 	call	_enemyinit
   40CA F1            [10]  314 	pop	af
   40CB D1            [10]  315 	pop	de
   40CC C1            [10]  316 	pop	bc
                            317 ;src/game.c:91: for (i = 0; i < MAX_ENEMIES; ++i) {
   40CD 1C            [ 4]  318 	inc	e
   40CE 7B            [ 4]  319 	ld	a, e
   40CF D6 06         [ 7]  320 	sub	a, #0x06
   40D1 38 E6         [12]  321 	jr	C,00119$
                            322 ;src/game.c:96: else if (wave == 1) count = 3;
   40D3 DD 7E 04      [19]  323 	ld	a, 4 (ix)
   40D6 3D            [ 4]  324 	dec	a
   40D7 20 04         [12]  325 	jr	NZ,00196$
   40D9 3E 01         [ 7]  326 	ld	a,#0x01
   40DB 18 01         [12]  327 	jr	00197$
   40DD                     328 00196$:
   40DD AF            [ 4]  329 	xor	a,a
   40DE                     330 00197$:
   40DE 5F            [ 4]  331 	ld	e, a
                            332 ;src/game.c:95: if (wave == 0) count = 2;
   40DF DD 7E 04      [19]  333 	ld	a, 4 (ix)
   40E2 B7            [ 4]  334 	or	a, a
   40E3 20 06         [12]  335 	jr	NZ,00106$
   40E5 DD 36 FD 02   [19]  336 	ld	-3 (ix), #0x02
   40E9 18 0E         [12]  337 	jr	00107$
   40EB                     338 00106$:
                            339 ;src/game.c:96: else if (wave == 1) count = 3;
   40EB 7B            [ 4]  340 	ld	a, e
   40EC B7            [ 4]  341 	or	a, a
   40ED 28 06         [12]  342 	jr	Z,00103$
   40EF DD 36 FD 03   [19]  343 	ld	-3 (ix), #0x03
   40F3 18 04         [12]  344 	jr	00107$
   40F5                     345 00103$:
                            346 ;src/game.c:97: else count = 4;
   40F5 DD 36 FD 04   [19]  347 	ld	-3 (ix), #0x04
   40F9                     348 00107$:
                            349 ;src/game.c:99: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F9 3E 06         [ 7]  350 	ld	a, #0x06
   40FB DD 96 FD      [19]  351 	sub	a, -3 (ix)
   40FE 30 04         [12]  352 	jr	NC,00151$
   4100 DD 36 FD 06   [19]  353 	ld	-3 (ix), #0x06
                            354 ;src/game.c:101: for (i = 0; i < count; ++i) {
   4104                     355 00151$:
   4104 DD 73 FF      [19]  356 	ld	-1 (ix), e
   4107 1E 00         [ 7]  357 	ld	e, #0x00
   4109                     358 00122$:
   4109 7B            [ 4]  359 	ld	a, e
   410A DD 96 FD      [19]  360 	sub	a, -3 (ix)
   410D D2 A0 41      [10]  361 	jp	NC, 00118$
                            362 ;src/game.c:105: if (wave == 0) type = 0;
   4110 DD 7E 04      [19]  363 	ld	a, 4 (ix)
   4113 B7            [ 4]  364 	or	a, a
   4114 20 06         [12]  365 	jr	NZ,00114$
   4116 DD 36 FC 00   [19]  366 	ld	-4 (ix), #0x00
   411A 18 27         [12]  367 	jr	00115$
   411C                     368 00114$:
                            369 ;src/game.c:106: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
   411C DD 7E FF      [19]  370 	ld	a, -1 (ix)
   411F B7            [ 4]  371 	or	a, a
   4120 28 0F         [12]  372 	jr	Z,00111$
   4122 7B            [ 4]  373 	ld	a, e
   4123 B7            [ 4]  374 	or	a, a
   4124 20 04         [12]  375 	jr	NZ,00126$
   4126 16 01         [ 7]  376 	ld	d, #0x01
   4128 18 02         [12]  377 	jr	00127$
   412A                     378 00126$:
   412A 16 00         [ 7]  379 	ld	d, #0x00
   412C                     380 00127$:
   412C DD 72 FC      [19]  381 	ld	-4 (ix), d
   412F 18 12         [12]  382 	jr	00115$
   4131                     383 00111$:
                            384 ;src/game.c:107: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   4131 7B            [ 4]  385 	ld	a, e
   4132 B7            [ 4]  386 	or	a, a
   4133 28 05         [12]  387 	jr	Z,00131$
   4135 7B            [ 4]  388 	ld	a, e
   4136 D6 03         [ 7]  389 	sub	a, #0x03
   4138 20 04         [12]  390 	jr	NZ,00128$
   413A                     391 00131$:
   413A 16 02         [ 7]  392 	ld	d, #0x02
   413C 18 02         [12]  393 	jr	00129$
   413E                     394 00128$:
   413E 16 01         [ 7]  395 	ld	d, #0x01
   4140                     396 00129$:
   4140 DD 72 FC      [19]  397 	ld	-4 (ix), d
   4143                     398 00115$:
                            399 ;src/game.c:109: spawn_y = (type == 2) ? 84 : 112;
   4143 DD 7E FC      [19]  400 	ld	a, -4 (ix)
   4146 D6 02         [ 7]  401 	sub	a, #0x02
   4148 20 04         [12]  402 	jr	NZ,00133$
   414A 16 54         [ 7]  403 	ld	d, #0x54
   414C 18 02         [12]  404 	jr	00134$
   414E                     405 00133$:
   414E 16 70         [ 7]  406 	ld	d, #0x70
   4150                     407 00134$:
   4150 DD 72 FB      [19]  408 	ld	-5 (ix), d
                            409 ;src/game.c:111: spawn_x = (u8)(36 + (i * 16));
   4153 7B            [ 4]  410 	ld	a, e
   4154 07            [ 4]  411 	rlca
   4155 07            [ 4]  412 	rlca
   4156 07            [ 4]  413 	rlca
   4157 07            [ 4]  414 	rlca
   4158 E6 F0         [ 7]  415 	and	a, #0xf0
   415A C6 24         [ 7]  416 	add	a, #0x24
   415C 57            [ 4]  417 	ld	d, a
                            418 ;src/game.c:112: if (spawn_x > 68) spawn_x = 68;
   415D 3E 44         [ 7]  419 	ld	a, #0x44
   415F 92            [ 4]  420 	sub	a, d
   4160 30 02         [12]  421 	jr	NC,00117$
   4162 16 44         [ 7]  422 	ld	d, #0x44
   4164                     423 00117$:
                            424 ;src/game.c:113: enemyspawn(&g_enemies[i], spawn_x, spawn_y, type, (u8)((i & 1) ? 1 : 0));
   4164 CB 43         [ 8]  425 	bit	0, e
   4166 28 06         [12]  426 	jr	Z,00135$
   4168 DD 36 FE 01   [19]  427 	ld	-2 (ix), #0x01
   416C 18 04         [12]  428 	jr	00136$
   416E                     429 00135$:
   416E DD 36 FE 00   [19]  430 	ld	-2 (ix), #0x00
   4172                     431 00136$:
   4172 D5            [11]  432 	push	de
   4173 16 00         [ 7]  433 	ld	d,#0x00
   4175 6B            [ 4]  434 	ld	l, e
   4176 62            [ 4]  435 	ld	h, d
   4177 29            [11]  436 	add	hl, hl
   4178 29            [11]  437 	add	hl, hl
   4179 19            [11]  438 	add	hl, de
   417A 29            [11]  439 	add	hl, hl
   417B D1            [10]  440 	pop	de
   417C 09            [11]  441 	add	hl, bc
   417D E5            [11]  442 	push	hl
   417E FD E1         [14]  443 	pop	iy
   4180 C5            [11]  444 	push	bc
   4181 D5            [11]  445 	push	de
   4182 DD 66 FE      [19]  446 	ld	h, -2 (ix)
   4185 DD 6E FC      [19]  447 	ld	l, -4 (ix)
   4188 E5            [11]  448 	push	hl
   4189 DD 7E FB      [19]  449 	ld	a, -5 (ix)
   418C F5            [11]  450 	push	af
   418D 33            [ 6]  451 	inc	sp
   418E D5            [11]  452 	push	de
   418F 33            [ 6]  453 	inc	sp
   4190 FD E5         [15]  454 	push	iy
   4192 CD D3 5E      [17]  455 	call	_enemyspawn
   4195 21 06 00      [10]  456 	ld	hl, #6
   4198 39            [11]  457 	add	hl, sp
   4199 F9            [ 6]  458 	ld	sp, hl
   419A D1            [10]  459 	pop	de
   419B C1            [10]  460 	pop	bc
                            461 ;src/game.c:101: for (i = 0; i < count; ++i) {
   419C 1C            [ 4]  462 	inc	e
   419D C3 09 41      [10]  463 	jp	00122$
   41A0                     464 00118$:
                            465 ;src/game.c:116: g_aliveenemies = count;
   41A0 DD 7E FD      [19]  466 	ld	a, -3 (ix)
   41A3 32 9C 6C      [13]  467 	ld	(#_g_aliveenemies + 0),a
   41A6 DD F9         [10]  468 	ld	sp, ix
   41A8 DD E1         [14]  469 	pop	ix
   41AA C9            [10]  470 	ret
                            471 ;src/game.c:119: static void spawn_boss(void) {
                            472 ;	---------------------------------
                            473 ; Function spawn_boss
                            474 ; ---------------------------------
   41AB                     475 _spawn_boss:
                            476 ;src/game.c:120: enemyinit(&g_boss);
   41AB 21 A7 6C      [10]  477 	ld	hl, #_g_boss
   41AE E5            [11]  478 	push	hl
   41AF CD 18 5D      [17]  479 	call	_enemyinit
   41B2 F1            [10]  480 	pop	af
                            481 ;src/game.c:121: enemyspawn(&g_boss, 68, 112, 1, 0);
   41B3 21 01 00      [10]  482 	ld	hl, #0x0001
   41B6 E5            [11]  483 	push	hl
   41B7 21 44 70      [10]  484 	ld	hl, #0x7044
   41BA E5            [11]  485 	push	hl
   41BB 21 A7 6C      [10]  486 	ld	hl, #_g_boss
   41BE E5            [11]  487 	push	hl
   41BF CD D3 5E      [17]  488 	call	_enemyspawn
   41C2 21 06 00      [10]  489 	ld	hl, #6
   41C5 39            [11]  490 	add	hl, sp
   41C6 F9            [ 6]  491 	ld	sp, hl
                            492 ;src/game.c:122: g_boss.w = 10;
   41C7 21 AB 6C      [10]  493 	ld	hl, #(_g_boss + 0x0004)
   41CA 36 0A         [10]  494 	ld	(hl), #0x0a
                            495 ;src/game.c:123: g_boss.h = 18;
   41CC 21 AC 6C      [10]  496 	ld	hl, #(_g_boss + 0x0005)
   41CF 36 12         [10]  497 	ld	(hl), #0x12
                            498 ;src/game.c:124: g_boss.health = 10;
   41D1 21 AE 6C      [10]  499 	ld	hl, #(_g_boss + 0x0007)
   41D4 36 0A         [10]  500 	ld	(hl), #0x0a
                            501 ;src/game.c:125: g_boss.reward = 255; /* u8 max; score adds separately on kill */
   41D6 21 AF 6C      [10]  502 	ld	hl, #(_g_boss + 0x0008)
   41D9 36 FF         [10]  503 	ld	(hl), #0xff
                            504 ;src/game.c:126: g_boss.kind = 3;
   41DB 21 B0 6C      [10]  505 	ld	hl, #(_g_boss + 0x0009)
   41DE 36 03         [10]  506 	ld	(hl), #0x03
                            507 ;src/game.c:127: g_boss.vx = -1;
   41E0 21 A9 6C      [10]  508 	ld	hl, #(_g_boss + 0x0002)
   41E3 36 FF         [10]  509 	ld	(hl), #0xff
                            510 ;src/game.c:128: g_bossactive = 1;
   41E5 21 B1 6C      [10]  511 	ld	hl,#_g_bossactive + 0
   41E8 36 01         [10]  512 	ld	(hl), #0x01
                            513 ;src/game.c:129: g_bossphase = 0;
   41EA 21 B2 6C      [10]  514 	ld	hl,#_g_bossphase + 0
   41ED 36 00         [10]  515 	ld	(hl), #0x00
   41EF C9            [10]  516 	ret
                            517 ;src/game.c:132: static void try_fire_projectile(void) {
                            518 ;	---------------------------------
                            519 ; Function try_fire_projectile
                            520 ; ---------------------------------
   41F0                     521 _try_fire_projectile:
   41F0 DD E5         [15]  522 	push	ix
   41F2 DD 21 00 00   [14]  523 	ld	ix,#0
   41F6 DD 39         [15]  524 	add	ix,sp
   41F8 F5            [11]  525 	push	af
   41F9 3B            [ 6]  526 	dec	sp
                            527 ;src/game.c:136: if (!input_is_shoot_just_pressed()) return;
   41FA CD 19 59      [17]  528 	call	_input_is_shoot_just_pressed
   41FD 7D            [ 4]  529 	ld	a, l
   41FE B7            [ 4]  530 	or	a, a
   41FF CA 91 42      [10]  531 	jp	Z,00110$
                            532 ;src/game.c:137: if (g_shootcooldown) return;
   4202 3A 9F 6C      [13]  533 	ld	a,(#_g_shootcooldown + 0)
   4205 B7            [ 4]  534 	or	a, a
   4206 C2 91 42      [10]  535 	jp	NZ,00110$
                            536 ;src/game.c:139: dir = g_player.facing_left ? -3 : 3;
   4209 3A DD 6B      [13]  537 	ld	a, (#_g_player + 8)
   420C B7            [ 4]  538 	or	a, a
   420D 28 04         [12]  539 	jr	Z,00112$
   420F 0E FD         [ 7]  540 	ld	c, #0xfd
   4211 18 02         [12]  541 	jr	00113$
   4213                     542 00112$:
   4213 0E 03         [ 7]  543 	ld	c, #0x03
   4215                     544 00113$:
                            545 ;src/game.c:141: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4215 DD 36 FF 00   [19]  546 	ld	-1 (ix), #0x00
   4219 06 00         [ 7]  547 	ld	b, #0x00
   421B                     548 00108$:
                            549 ;src/game.c:142: if (!g_projectiles[i].active) {
   421B 58            [ 4]  550 	ld	e,b
   421C 16 00         [ 7]  551 	ld	d,#0x00
   421E 6B            [ 4]  552 	ld	l, e
   421F 62            [ 4]  553 	ld	h, d
   4220 29            [11]  554 	add	hl, hl
   4221 29            [11]  555 	add	hl, hl
   4222 19            [11]  556 	add	hl, de
   4223 29            [11]  557 	add	hl, hl
   4224 11 1B 6C      [10]  558 	ld	de, #_g_projectiles
   4227 19            [11]  559 	add	hl, de
   4228 11 06 00      [10]  560 	ld	de, #0x0006
   422B 19            [11]  561 	add	hl, de
   422C 7E            [ 7]  562 	ld	a, (hl)
   422D B7            [ 4]  563 	or	a, a
   422E 20 58         [12]  564 	jr	NZ,00109$
                            565 ;src/game.c:144: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
   4230 3A B3 6C      [13]  566 	ld	a,(#_g_weaponlevel + 0)
   4233 B7            [ 4]  567 	or	a, a
   4234 28 06         [12]  568 	jr	Z,00114$
   4236 DD 36 FE 01   [19]  569 	ld	-2 (ix), #0x01
   423A 18 04         [12]  570 	jr	00115$
   423C                     571 00114$:
   423C DD 36 FE 00   [19]  572 	ld	-2 (ix), #0x00
   4240                     573 00115$:
   4240 3A D6 6B      [13]  574 	ld	a, (#_g_player + 1)
   4243 C6 06         [ 7]  575 	add	a, #0x06
   4245 DD 77 FD      [19]  576 	ld	-3 (ix), a
   4248 21 D5 6B      [10]  577 	ld	hl, #_g_player + 0
   424B 46            [ 7]  578 	ld	b, (hl)
   424C 04            [ 4]  579 	inc	b
   424D 04            [ 4]  580 	inc	b
   424E DD 5E FF      [19]  581 	ld	e,-1 (ix)
   4251 16 00         [ 7]  582 	ld	d,#0x00
   4253 6B            [ 4]  583 	ld	l, e
   4254 62            [ 4]  584 	ld	h, d
   4255 29            [11]  585 	add	hl, hl
   4256 29            [11]  586 	add	hl, hl
   4257 19            [11]  587 	add	hl, de
   4258 29            [11]  588 	add	hl, hl
   4259 11 1B 6C      [10]  589 	ld	de, #_g_projectiles
   425C 19            [11]  590 	add	hl, de
   425D EB            [ 4]  591 	ex	de,hl
   425E DD 7E FE      [19]  592 	ld	a, -2 (ix)
   4261 F5            [11]  593 	push	af
   4262 33            [ 6]  594 	inc	sp
   4263 79            [ 4]  595 	ld	a, c
   4264 F5            [11]  596 	push	af
   4265 33            [ 6]  597 	inc	sp
   4266 DD 7E FD      [19]  598 	ld	a, -3 (ix)
   4269 F5            [11]  599 	push	af
   426A 33            [ 6]  600 	inc	sp
   426B C5            [11]  601 	push	bc
   426C 33            [ 6]  602 	inc	sp
   426D D5            [11]  603 	push	de
   426E CD 59 67      [17]  604 	call	_projectilefire
   4271 21 06 00      [10]  605 	ld	hl, #6
   4274 39            [11]  606 	add	hl, sp
   4275 F9            [ 6]  607 	ld	sp, hl
                            608 ;src/game.c:145: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
   4276 3A B3 6C      [13]  609 	ld	a,(#_g_weaponlevel + 0)
   4279 B7            [ 4]  610 	or	a, a
   427A 28 04         [12]  611 	jr	Z,00116$
   427C 0E 04         [ 7]  612 	ld	c, #0x04
   427E 18 02         [12]  613 	jr	00117$
   4280                     614 00116$:
   4280 0E 08         [ 7]  615 	ld	c, #0x08
   4282                     616 00117$:
   4282 21 9F 6C      [10]  617 	ld	hl,#_g_shootcooldown + 0
   4285 71            [ 7]  618 	ld	(hl), c
                            619 ;src/game.c:146: break;
   4286 18 09         [12]  620 	jr	00110$
   4288                     621 00109$:
                            622 ;src/game.c:141: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4288 04            [ 4]  623 	inc	b
   4289 DD 70 FF      [19]  624 	ld	-1 (ix), b
   428C 78            [ 4]  625 	ld	a, b
   428D D6 06         [ 7]  626 	sub	a, #0x06
   428F 38 8A         [12]  627 	jr	C,00108$
   4291                     628 00110$:
   4291 DD F9         [10]  629 	ld	sp, ix
   4293 DD E1         [14]  630 	pop	ix
   4295 C9            [10]  631 	ret
                            632 ;src/game.c:151: static void register_player_hit(void) {
                            633 ;	---------------------------------
                            634 ; Function register_player_hit
                            635 ; ---------------------------------
   4296                     636 _register_player_hit:
                            637 ;src/game.c:152: if (g_lives) {
   4296 FD 21 96 6C   [14]  638 	ld	iy, #_g_lives
   429A FD 7E 00      [19]  639 	ld	a, 0 (iy)
   429D B7            [ 4]  640 	or	a, a
   429E 28 03         [12]  641 	jr	Z,00102$
                            642 ;src/game.c:153: g_lives--;
   42A0 FD 35 00      [23]  643 	dec	0 (iy)
   42A3                     644 00102$:
                            645 ;src/game.c:155: if (g_lives == 0) {
   42A3 3A 96 6C      [13]  646 	ld	a,(#_g_lives + 0)
   42A6 B7            [ 4]  647 	or	a, a
   42A7 20 06         [12]  648 	jr	NZ,00104$
                            649 ;src/game.c:156: g_gameover = 1;
   42A9 21 A1 6C      [10]  650 	ld	hl,#_g_gameover + 0
   42AC 36 01         [10]  651 	ld	(hl), #0x01
                            652 ;src/game.c:157: return;
   42AE C9            [10]  653 	ret
   42AF                     654 00104$:
                            655 ;src/game.c:160: reset_player_to_checkpoint();
   42AF CD 03 40      [17]  656 	call	_reset_player_to_checkpoint
                            657 ;src/game.c:161: g_damagecooldown = 40;
   42B2 21 9E 6C      [10]  658 	ld	hl,#_g_damagecooldown + 0
   42B5 36 28         [10]  659 	ld	(hl), #0x28
   42B7 C9            [10]  660 	ret
                            661 ;src/game.c:164: void game_init(void) {
                            662 ;	---------------------------------
                            663 ; Function game_init
                            664 ; ---------------------------------
   42B8                     665 _game_init::
                            666 ;src/game.c:167: cpct_setVideoMode(0);
   42B8 2E 00         [ 7]  667 	ld	l, #0x00
   42BA CD 73 6A      [17]  668 	call	_cpct_setVideoMode
                            669 ;src/game.c:168: cpct_disableFirmware();
   42BD CD AB 6A      [17]  670 	call	_cpct_disableFirmware
                            671 ;src/game.c:169: cpct_setPalette((u8*)gpalette, GPALETTE_SIZE);
   42C0 21 10 00      [10]  672 	ld	hl, #0x0010
   42C3 E5            [11]  673 	push	hl
   42C4 21 E8 5A      [10]  674 	ld	hl, #_gpalette
   42C7 E5            [11]  675 	push	hl
   42C8 CD 3E 69      [17]  676 	call	_cpct_setPalette
                            677 ;src/game.c:170: cpct_setBorder(gpalette[0]);
   42CB 21 E8 5A      [10]  678 	ld	hl, #_gpalette + 0
   42CE 46            [ 7]  679 	ld	b, (hl)
   42CF C5            [11]  680 	push	bc
   42D0 33            [ 6]  681 	inc	sp
   42D1 3E 10         [ 7]  682 	ld	a, #0x10
   42D3 F5            [11]  683 	push	af
   42D4 33            [ 6]  684 	inc	sp
   42D5 CD 55 69      [17]  685 	call	_cpct_setPALColour
                            686 ;src/game.c:171: cpct_clearScreen(0x00);
   42D8 21 00 40      [10]  687 	ld	hl, #0x4000
   42DB E5            [11]  688 	push	hl
   42DC AF            [ 4]  689 	xor	a, a
   42DD F5            [11]  690 	push	af
   42DE 33            [ 6]  691 	inc	sp
   42DF 26 C0         [ 7]  692 	ld	h, #0xc0
   42E1 E5            [11]  693 	push	hl
   42E2 CD 9D 6A      [17]  694 	call	_cpct_memset
                            695 ;src/game.c:172: tilemap_init();
   42E5 CD 2B 59      [17]  696 	call	_tilemap_init
                            697 ;src/game.c:173: collision_init();
   42E8 CD 92 52      [17]  698 	call	_collision_init
                            699 ;src/game.c:174: playerinit(&g_player);
   42EB 21 D5 6B      [10]  700 	ld	hl, #_g_player
   42EE E5            [11]  701 	push	hl
   42EF CD 89 63      [17]  702 	call	_playerinit
   42F2 F1            [10]  703 	pop	af
                            704 ;src/game.c:175: hudinit();
   42F3 CD 96 56      [17]  705 	call	_hudinit
                            706 ;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42F6 0E 00         [ 7]  707 	ld	c, #0x00
   42F8                     708 00102$:
                            709 ;src/game.c:178: projectileinit(&g_projectiles[i]);
   42F8 06 00         [ 7]  710 	ld	b,#0x00
   42FA 69            [ 4]  711 	ld	l, c
   42FB 60            [ 4]  712 	ld	h, b
   42FC 29            [11]  713 	add	hl, hl
   42FD 29            [11]  714 	add	hl, hl
   42FE 09            [11]  715 	add	hl, bc
   42FF 29            [11]  716 	add	hl, hl
   4300 11 1B 6C      [10]  717 	ld	de, #_g_projectiles
   4303 19            [11]  718 	add	hl, de
   4304 C5            [11]  719 	push	bc
   4305 E5            [11]  720 	push	hl
   4306 CD F2 66      [17]  721 	call	_projectileinit
   4309 F1            [10]  722 	pop	af
   430A C1            [10]  723 	pop	bc
                            724 ;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
   430B 0C            [ 4]  725 	inc	c
   430C 79            [ 4]  726 	ld	a, c
   430D D6 06         [ 7]  727 	sub	a, #0x06
   430F 38 E7         [12]  728 	jr	C,00102$
                            729 ;src/game.c:181: g_lives = 3;
   4311 21 96 6C      [10]  730 	ld	hl,#_g_lives + 0
   4314 36 03         [10]  731 	ld	(hl), #0x03
                            732 ;src/game.c:182: g_score = 0;
   4316 21 00 00      [10]  733 	ld	hl, #0x0000
   4319 22 97 6C      [16]  734 	ld	(_g_score), hl
                            735 ;src/game.c:183: g_timeleft = 99;
   431C FD 21 99 6C   [14]  736 	ld	iy, #_g_timeleft
   4320 FD 36 00 63   [19]  737 	ld	0 (iy), #0x63
                            738 ;src/game.c:184: g_weapondisplay = 1;
   4324 FD 21 9A 6C   [14]  739 	ld	iy, #_g_weapondisplay
   4328 FD 36 00 01   [19]  740 	ld	0 (iy), #0x01
                            741 ;src/game.c:185: g_currentwave = 0;
   432C FD 21 9B 6C   [14]  742 	ld	iy, #_g_currentwave
   4330 FD 36 00 00   [19]  743 	ld	0 (iy), #0x00
                            744 ;src/game.c:186: g_wavecooldown = 1;
   4334 FD 21 9D 6C   [14]  745 	ld	iy, #_g_wavecooldown
   4338 FD 36 00 01   [19]  746 	ld	0 (iy), #0x01
                            747 ;src/game.c:187: g_damagecooldown = 100;
   433C FD 21 9E 6C   [14]  748 	ld	iy, #_g_damagecooldown
   4340 FD 36 00 64   [19]  749 	ld	0 (iy), #0x64
                            750 ;src/game.c:188: g_shootcooldown = 0;
   4344 FD 21 9F 6C   [14]  751 	ld	iy, #_g_shootcooldown
   4348 FD 36 00 00   [19]  752 	ld	0 (iy), #0x00
                            753 ;src/game.c:189: g_victory = 0;
   434C FD 21 A0 6C   [14]  754 	ld	iy, #_g_victory
   4350 FD 36 00 00   [19]  755 	ld	0 (iy), #0x00
                            756 ;src/game.c:190: g_gameover = 0;
   4354 FD 21 A1 6C   [14]  757 	ld	iy, #_g_gameover
   4358 FD 36 00 00   [19]  758 	ld	0 (iy), #0x00
                            759 ;src/game.c:191: g_framecounter = 0;
   435C 2E 00         [ 7]  760 	ld	l, #0x00
   435E 22 A2 6C      [16]  761 	ld	(_g_framecounter), hl
                            762 ;src/game.c:192: g_checkpointx = 12;
   4361 21 A4 6C      [10]  763 	ld	hl,#_g_checkpointx + 0
   4364 36 0C         [10]  764 	ld	(hl), #0x0c
                            765 ;src/game.c:193: g_checkpointy = 104;
   4366 21 A5 6C      [10]  766 	ld	hl,#_g_checkpointy + 0
   4369 36 68         [10]  767 	ld	(hl), #0x68
                            768 ;src/game.c:194: g_checkpointactive = 0;
   436B 21 A6 6C      [10]  769 	ld	hl,#_g_checkpointactive + 0
   436E 36 00         [10]  770 	ld	(hl), #0x00
                            771 ;src/game.c:195: g_bossactive = 0;
   4370 21 B1 6C      [10]  772 	ld	hl,#_g_bossactive + 0
   4373 36 00         [10]  773 	ld	(hl), #0x00
                            774 ;src/game.c:196: g_weaponlevel = 0;
   4375 21 B3 6C      [10]  775 	ld	hl,#_g_weaponlevel + 0
   4378 36 00         [10]  776 	ld	(hl), #0x00
                            777 ;src/game.c:197: g_pickuptaken = 0;
   437A 21 B4 6C      [10]  778 	ld	hl,#_g_pickuptaken + 0
   437D 36 00         [10]  779 	ld	(hl), #0x00
                            780 ;src/game.c:198: g_dbg_left = 0;
   437F 21 B5 6C      [10]  781 	ld	hl,#_g_dbg_left + 0
   4382 36 00         [10]  782 	ld	(hl), #0x00
                            783 ;src/game.c:199: g_dbg_right = 0;
   4384 21 B6 6C      [10]  784 	ld	hl,#_g_dbg_right + 0
   4387 36 00         [10]  785 	ld	(hl), #0x00
                            786 ;src/game.c:200: g_dbg_jump = 0;
   4389 21 B7 6C      [10]  787 	ld	hl,#_g_dbg_jump + 0
   438C 36 00         [10]  788 	ld	(hl), #0x00
                            789 ;src/game.c:201: g_dbg_shoot = 0;
   438E 21 B8 6C      [10]  790 	ld	hl,#_g_dbg_shoot + 0
   4391 36 00         [10]  791 	ld	(hl), #0x00
                            792 ;src/game.c:202: g_dbg_move_raw = 0;
   4393 21 B9 6C      [10]  793 	ld	hl,#_g_dbg_move_raw + 0
   4396 36 00         [10]  794 	ld	(hl), #0x00
                            795 ;src/game.c:203: g_dbg_move_net = 0;
   4398 21 BA 6C      [10]  796 	ld	hl,#_g_dbg_move_net + 0
   439B 36 00         [10]  797 	ld	(hl), #0x00
                            798 ;src/game.c:204: g_dbg_move_cancelled = 0;
   439D 21 BB 6C      [10]  799 	ld	hl,#_g_dbg_move_cancelled + 0
   43A0 36 00         [10]  800 	ld	(hl), #0x00
                            801 ;src/game.c:205: g_dbg_hit = 0;
   43A2 21 BC 6C      [10]  802 	ld	hl,#_g_dbg_hit + 0
   43A5 36 00         [10]  803 	ld	(hl), #0x00
                            804 ;src/game.c:206: g_dbg_vx = 0;
   43A7 21 BD 6C      [10]  805 	ld	hl,#_g_dbg_vx + 0
   43AA 36 00         [10]  806 	ld	(hl), #0x00
                            807 ;src/game.c:207: enemyinit(&g_boss);
   43AC 21 A7 6C      [10]  808 	ld	hl, #_g_boss
   43AF E5            [11]  809 	push	hl
   43B0 CD 18 5D      [17]  810 	call	_enemyinit
   43B3 F1            [10]  811 	pop	af
   43B4 C9            [10]  812 	ret
                            813 ;src/game.c:210: void game_update(void) {
                            814 ;	---------------------------------
                            815 ; Function game_update
                            816 ; ---------------------------------
   43B5                     817 _game_update::
   43B5 DD E5         [15]  818 	push	ix
   43B7 DD 21 00 00   [14]  819 	ld	ix,#0
   43BB DD 39         [15]  820 	add	ix,sp
   43BD 21 E4 FF      [10]  821 	ld	hl, #-28
   43C0 39            [11]  822 	add	hl, sp
   43C1 F9            [ 6]  823 	ld	sp, hl
                            824 ;src/game.c:221: input_update();
   43C2 CD A1 57      [17]  825 	call	_input_update
                            826 ;src/game.c:223: left_pressed = input_is_left_pressed();
   43C5 CD D7 58      [17]  827 	call	_input_is_left_pressed
   43C8 4D            [ 4]  828 	ld	c, l
                            829 ;src/game.c:224: right_pressed = input_is_right_pressed();
   43C9 C5            [11]  830 	push	bc
   43CA CD DF 58      [17]  831 	call	_input_is_right_pressed
   43CD C1            [10]  832 	pop	bc
   43CE 45            [ 4]  833 	ld	b, l
                            834 ;src/game.c:225: jump_pressed = input_is_jump_pressed();
   43CF C5            [11]  835 	push	bc
   43D0 CD F7 58      [17]  836 	call	_input_is_jump_pressed
   43D3 5D            [ 4]  837 	ld	e, l
   43D4 D5            [11]  838 	push	de
   43D5 CD 11 59      [17]  839 	call	_input_is_shoot_pressed
   43D8 D1            [10]  840 	pop	de
   43D9 C1            [10]  841 	pop	bc
   43DA 55            [ 4]  842 	ld	d, l
                            843 ;src/game.c:228: g_dbg_left = left_pressed;
   43DB 21 B5 6C      [10]  844 	ld	hl,#_g_dbg_left + 0
   43DE 71            [ 7]  845 	ld	(hl), c
                            846 ;src/game.c:229: g_dbg_right = right_pressed;
   43DF 21 B6 6C      [10]  847 	ld	hl,#_g_dbg_right + 0
   43E2 70            [ 7]  848 	ld	(hl), b
                            849 ;src/game.c:230: g_dbg_jump = jump_pressed;
   43E3 21 B7 6C      [10]  850 	ld	hl,#_g_dbg_jump + 0
   43E6 73            [ 7]  851 	ld	(hl), e
                            852 ;src/game.c:231: g_dbg_shoot = shoot_pressed;
   43E7 21 B8 6C      [10]  853 	ld	hl,#_g_dbg_shoot + 0
   43EA 72            [ 7]  854 	ld	(hl), d
                            855 ;src/game.c:234: if (left_pressed && !right_pressed) {
   43EB 79            [ 4]  856 	ld	a, c
   43EC B7            [ 4]  857 	or	a, a
   43ED 28 13         [12]  858 	jr	Z,00112$
   43EF 78            [ 4]  859 	ld	a, b
   43F0 B7            [ 4]  860 	or	a, a
   43F1 20 0F         [12]  861 	jr	NZ,00112$
                            862 ;src/game.c:235: cpct_setBorder(gpalette[2]);
   43F3 21 EA 5A      [10]  863 	ld	hl, #_gpalette+2
   43F6 46            [ 7]  864 	ld	b, (hl)
   43F7 C5            [11]  865 	push	bc
   43F8 33            [ 6]  866 	inc	sp
   43F9 3E 10         [ 7]  867 	ld	a, #0x10
   43FB F5            [11]  868 	push	af
   43FC 33            [ 6]  869 	inc	sp
   43FD CD 55 69      [17]  870 	call	_cpct_setPALColour
   4400 18 4A         [12]  871 	jr	00113$
   4402                     872 00112$:
                            873 ;src/game.c:236: } else if (right_pressed && !left_pressed) {
   4402 78            [ 4]  874 	ld	a, b
   4403 B7            [ 4]  875 	or	a, a
   4404 28 13         [12]  876 	jr	Z,00108$
   4406 79            [ 4]  877 	ld	a, c
   4407 B7            [ 4]  878 	or	a, a
   4408 20 0F         [12]  879 	jr	NZ,00108$
                            880 ;src/game.c:237: cpct_setBorder(gpalette[14]);
   440A 21 F6 5A      [10]  881 	ld	hl, #_gpalette+14
   440D 46            [ 7]  882 	ld	b, (hl)
   440E C5            [11]  883 	push	bc
   440F 33            [ 6]  884 	inc	sp
   4410 3E 10         [ 7]  885 	ld	a, #0x10
   4412 F5            [11]  886 	push	af
   4413 33            [ 6]  887 	inc	sp
   4414 CD 55 69      [17]  888 	call	_cpct_setPALColour
   4417 18 33         [12]  889 	jr	00113$
   4419                     890 00108$:
                            891 ;src/game.c:238: } else if (jump_pressed) {
   4419 7B            [ 4]  892 	ld	a, e
   441A B7            [ 4]  893 	or	a, a
   441B 28 0F         [12]  894 	jr	Z,00105$
                            895 ;src/game.c:239: cpct_setBorder(gpalette[3]);
   441D 21 EB 5A      [10]  896 	ld	hl, #_gpalette+3
   4420 46            [ 7]  897 	ld	b, (hl)
   4421 C5            [11]  898 	push	bc
   4422 33            [ 6]  899 	inc	sp
   4423 3E 10         [ 7]  900 	ld	a, #0x10
   4425 F5            [11]  901 	push	af
   4426 33            [ 6]  902 	inc	sp
   4427 CD 55 69      [17]  903 	call	_cpct_setPALColour
   442A 18 20         [12]  904 	jr	00113$
   442C                     905 00105$:
                            906 ;src/game.c:240: } else if (shoot_pressed) {
   442C 7A            [ 4]  907 	ld	a, d
   442D B7            [ 4]  908 	or	a, a
   442E 28 0F         [12]  909 	jr	Z,00102$
                            910 ;src/game.c:241: cpct_setBorder(gpalette[6]);
   4430 21 EE 5A      [10]  911 	ld	hl, #_gpalette+6
   4433 46            [ 7]  912 	ld	b, (hl)
   4434 C5            [11]  913 	push	bc
   4435 33            [ 6]  914 	inc	sp
   4436 3E 10         [ 7]  915 	ld	a, #0x10
   4438 F5            [11]  916 	push	af
   4439 33            [ 6]  917 	inc	sp
   443A CD 55 69      [17]  918 	call	_cpct_setPALColour
   443D 18 0D         [12]  919 	jr	00113$
   443F                     920 00102$:
                            921 ;src/game.c:243: cpct_setBorder(gpalette[0]);
   443F 21 E8 5A      [10]  922 	ld	hl, #_gpalette+0
   4442 46            [ 7]  923 	ld	b, (hl)
   4443 C5            [11]  924 	push	bc
   4444 33            [ 6]  925 	inc	sp
   4445 3E 10         [ 7]  926 	ld	a, #0x10
   4447 F5            [11]  927 	push	af
   4448 33            [ 6]  928 	inc	sp
   4449 CD 55 69      [17]  929 	call	_cpct_setPALColour
   444C                     930 00113$:
                            931 ;src/game.c:246: if (g_gameover || g_victory) {
   444C 3A A1 6C      [13]  932 	ld	a,(#_g_gameover + 0)
   444F B7            [ 4]  933 	or	a, a
   4450 20 06         [12]  934 	jr	NZ,00115$
   4452 3A A0 6C      [13]  935 	ld	a,(#_g_victory + 0)
   4455 B7            [ 4]  936 	or	a, a
   4456 28 36         [12]  937 	jr	Z,00116$
   4458                     938 00115$:
                            939 ;src/game.c:247: g_dbg_move_raw = 0;
   4458 21 B9 6C      [10]  940 	ld	hl,#_g_dbg_move_raw + 0
   445B 36 00         [10]  941 	ld	(hl), #0x00
                            942 ;src/game.c:248: g_dbg_move_net = 0;
   445D 21 BA 6C      [10]  943 	ld	hl,#_g_dbg_move_net + 0
   4460 36 00         [10]  944 	ld	(hl), #0x00
                            945 ;src/game.c:249: g_dbg_move_cancelled = 0;
   4462 21 BB 6C      [10]  946 	ld	hl,#_g_dbg_move_cancelled + 0
   4465 36 00         [10]  947 	ld	(hl), #0x00
                            948 ;src/game.c:250: g_dbg_hit = 0;
   4467 21 BC 6C      [10]  949 	ld	hl,#_g_dbg_hit + 0
   446A 36 00         [10]  950 	ld	(hl), #0x00
                            951 ;src/game.c:251: g_dbg_vx = g_player.vx;
   446C 3A D7 6B      [13]  952 	ld	a, (#_g_player+2)
   446F 32 BD 6C      [13]  953 	ld	(#_g_dbg_vx + 0),a
                            954 ;src/game.c:252: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4472 3A 9A 6C      [13]  955 	ld	a, (_g_weapondisplay)
   4475 F5            [11]  956 	push	af
   4476 33            [ 6]  957 	inc	sp
   4477 3A 99 6C      [13]  958 	ld	a, (_g_timeleft)
   447A F5            [11]  959 	push	af
   447B 33            [ 6]  960 	inc	sp
   447C 2A 97 6C      [16]  961 	ld	hl, (_g_score)
   447F E5            [11]  962 	push	hl
   4480 3A 96 6C      [13]  963 	ld	a, (_g_lives)
   4483 F5            [11]  964 	push	af
   4484 33            [ 6]  965 	inc	sp
   4485 CD B1 56      [17]  966 	call	_hudupdate
   4488 F1            [10]  967 	pop	af
   4489 F1            [10]  968 	pop	af
   448A 33            [ 6]  969 	inc	sp
                            970 ;src/game.c:253: return;
   448B C3 18 4B      [10]  971 	jp	00195$
   448E                     972 00116$:
                            973 ;src/game.c:256: player_x_start = g_player.x;
   448E 3A D5 6B      [13]  974 	ld	a, (#_g_player+0)
   4491 DD 77 E6      [19]  975 	ld	-26 (ix), a
                            976 ;src/game.c:257: playerupdate(&g_player);
   4494 21 D5 6B      [10]  977 	ld	hl, #_g_player
   4497 E5            [11]  978 	push	hl
   4498 CD F9 63      [17]  979 	call	_playerupdate
   449B F1            [10]  980 	pop	af
                            981 ;src/game.c:258: player_x_after_move = g_player.x;
   449C 3A D5 6B      [13]  982 	ld	a,(#_g_player + 0)
   449F DD 77 E5      [19]  983 	ld	-27 (ix), a
                            984 ;src/game.c:259: g_dbg_vx = g_player.vx;
   44A2 3A D7 6B      [13]  985 	ld	a,(#_g_player + 2)
   44A5 32 BD 6C      [13]  986 	ld	(#_g_dbg_vx + 0),a
                            987 ;src/game.c:260: try_fire_projectile();
   44A8 CD F0 41      [17]  988 	call	_try_fire_projectile
                            989 ;src/game.c:262: if (g_shootcooldown) g_shootcooldown--;
   44AB FD 21 9F 6C   [14]  990 	ld	iy, #_g_shootcooldown
   44AF FD 7E 00      [19]  991 	ld	a, 0 (iy)
   44B2 B7            [ 4]  992 	or	a, a
   44B3 28 03         [12]  993 	jr	Z,00119$
   44B5 FD 35 00      [23]  994 	dec	0 (iy)
   44B8                     995 00119$:
                            996 ;src/game.c:263: if (g_damagecooldown) g_damagecooldown--;
   44B8 FD 21 9E 6C   [14]  997 	ld	iy, #_g_damagecooldown
   44BC FD 7E 00      [19]  998 	ld	a, 0 (iy)
   44BF B7            [ 4]  999 	or	a, a
   44C0 28 03         [12] 1000 	jr	Z,00215$
   44C2 FD 35 00      [23] 1001 	dec	0 (iy)
                           1002 ;src/game.c:265: for (i = 0; i < MAX_PROJECTILES; ++i) {
   44C5                    1003 00215$:
   44C5 DD 36 E8 00   [19] 1004 	ld	-24 (ix), #0x00
   44C9                    1005 00188$:
                           1006 ;src/game.c:266: projectileupdate(&g_projectiles[i]);
   44C9 DD 4E E8      [19] 1007 	ld	c,-24 (ix)
   44CC 06 00         [ 7] 1008 	ld	b,#0x00
   44CE 69            [ 4] 1009 	ld	l, c
   44CF 60            [ 4] 1010 	ld	h, b
   44D0 29            [11] 1011 	add	hl, hl
   44D1 29            [11] 1012 	add	hl, hl
   44D2 09            [11] 1013 	add	hl, bc
   44D3 29            [11] 1014 	add	hl, hl
   44D4 DD 75 FE      [19] 1015 	ld	-2 (ix), l
   44D7 DD 74 FF      [19] 1016 	ld	-1 (ix), h
   44DA 3E 1B         [ 7] 1017 	ld	a, #<(_g_projectiles)
   44DC DD 86 FE      [19] 1018 	add	a, -2 (ix)
   44DF DD 77 FE      [19] 1019 	ld	-2 (ix), a
   44E2 3E 6C         [ 7] 1020 	ld	a, #>(_g_projectiles)
   44E4 DD 8E FF      [19] 1021 	adc	a, -1 (ix)
   44E7 DD 77 FF      [19] 1022 	ld	-1 (ix), a
   44EA DD 6E FE      [19] 1023 	ld	l,-2 (ix)
   44ED DD 66 FF      [19] 1024 	ld	h,-1 (ix)
   44F0 E5            [11] 1025 	push	hl
   44F1 CD 10 68      [17] 1026 	call	_projectileupdate
   44F4 F1            [10] 1027 	pop	af
                           1028 ;src/game.c:265: for (i = 0; i < MAX_PROJECTILES; ++i) {
   44F5 DD 34 E8      [23] 1029 	inc	-24 (ix)
   44F8 DD 7E E8      [19] 1030 	ld	a, -24 (ix)
   44FB D6 06         [ 7] 1031 	sub	a, #0x06
   44FD 38 CA         [12] 1032 	jr	C,00188$
                           1033 ;src/game.c:269: for (i = 0; i < MAX_ENEMIES; ++i) {
   44FF DD 36 E8 00   [19] 1034 	ld	-24 (ix), #0x00
   4503                    1035 00190$:
                           1036 ;src/game.c:270: enemyupdate(&g_enemies[i]);
   4503 DD 4E E8      [19] 1037 	ld	c,-24 (ix)
   4506 06 00         [ 7] 1038 	ld	b,#0x00
   4508 69            [ 4] 1039 	ld	l, c
   4509 60            [ 4] 1040 	ld	h, b
   450A 29            [11] 1041 	add	hl, hl
   450B 29            [11] 1042 	add	hl, hl
   450C 09            [11] 1043 	add	hl, bc
   450D 29            [11] 1044 	add	hl, hl
   450E DD 75 FE      [19] 1045 	ld	-2 (ix), l
   4511 DD 74 FF      [19] 1046 	ld	-1 (ix), h
   4514 3E DF         [ 7] 1047 	ld	a, #<(_g_enemies)
   4516 DD 86 FE      [19] 1048 	add	a, -2 (ix)
   4519 DD 77 FE      [19] 1049 	ld	-2 (ix), a
   451C 3E 6B         [ 7] 1050 	ld	a, #>(_g_enemies)
   451E DD 8E FF      [19] 1051 	adc	a, -1 (ix)
   4521 DD 77 FF      [19] 1052 	ld	-1 (ix), a
   4524 DD 6E FE      [19] 1053 	ld	l,-2 (ix)
   4527 DD 66 FF      [19] 1054 	ld	h,-1 (ix)
   452A E5            [11] 1055 	push	hl
   452B CD AB 60      [17] 1056 	call	_enemyupdate
   452E F1            [10] 1057 	pop	af
                           1058 ;src/game.c:269: for (i = 0; i < MAX_ENEMIES; ++i) {
   452F DD 34 E8      [23] 1059 	inc	-24 (ix)
   4532 DD 7E E8      [19] 1060 	ld	a, -24 (ix)
   4535 D6 06         [ 7] 1061 	sub	a, #0x06
   4537 38 CA         [12] 1062 	jr	C,00190$
                           1063 ;src/game.c:273: if (g_bossactive) {
   4539 3A B1 6C      [13] 1064 	ld	a,(#_g_bossactive + 0)
   453C B7            [ 4] 1065 	or	a, a
   453D 28 71         [12] 1066 	jr	Z,00234$
                           1067 ;src/game.c:274: if (g_boss.health > 4) g_bossphase = 0;
   453F 21 AE 6C      [10] 1068 	ld	hl, #_g_boss + 7
   4542 4E            [ 7] 1069 	ld	c, (hl)
   4543 3E 04         [ 7] 1070 	ld	a, #0x04
   4545 91            [ 4] 1071 	sub	a, c
   4546 30 07         [12] 1072 	jr	NC,00125$
   4548 21 B2 6C      [10] 1073 	ld	hl,#_g_bossphase + 0
   454B 36 00         [10] 1074 	ld	(hl), #0x00
   454D 18 05         [12] 1075 	jr	00126$
   454F                    1076 00125$:
                           1077 ;src/game.c:275: else g_bossphase = 1;
   454F 21 B2 6C      [10] 1078 	ld	hl,#_g_bossphase + 0
   4552 36 01         [10] 1079 	ld	(hl), #0x01
   4554                    1080 00126$:
                           1081 ;src/game.c:277: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4554 3A D5 6B      [13] 1082 	ld	a,(#_g_player + 0)
   4557 DD 77 FE      [19] 1083 	ld	-2 (ix), a
   455A DD 77 FE      [19] 1084 	ld	-2 (ix), a
   455D DD 36 FF 00   [19] 1085 	ld	-1 (ix), #0x00
   4561 DD 7E FE      [19] 1086 	ld	a, -2 (ix)
   4564 C6 02         [ 7] 1087 	add	a, #0x02
   4566 DD 77 FE      [19] 1088 	ld	-2 (ix), a
   4569 DD 7E FF      [19] 1089 	ld	a, -1 (ix)
   456C CE 00         [ 7] 1090 	adc	a, #0x00
   456E DD 77 FF      [19] 1091 	ld	-1 (ix), a
   4571 21 A7 6C      [10] 1092 	ld	hl, #_g_boss + 0
   4574 4E            [ 7] 1093 	ld	c, (hl)
   4575 06 00         [ 7] 1094 	ld	b, #0x00
   4577 DD 7E FE      [19] 1095 	ld	a, -2 (ix)
   457A 91            [ 4] 1096 	sub	a, c
   457B DD 7E FF      [19] 1097 	ld	a, -1 (ix)
   457E 98            [ 4] 1098 	sbc	a, b
   457F E2 84 45      [10] 1099 	jp	PO, 00425$
   4582 EE 80         [ 7] 1100 	xor	a, #0x80
   4584                    1101 00425$:
   4584 F2 98 45      [10] 1102 	jp	P, 00197$
   4587 3A B2 6C      [13] 1103 	ld	a,(#_g_bossphase + 0)
   458A B7            [ 4] 1104 	or	a, a
   458B 28 04         [12] 1105 	jr	Z,00199$
   458D 0E 02         [ 7] 1106 	ld	c, #0x02
   458F 18 02         [12] 1107 	jr	00200$
   4591                    1108 00199$:
   4591 0E 01         [ 7] 1109 	ld	c, #0x01
   4593                    1110 00200$:
   4593 AF            [ 4] 1111 	xor	a, a
   4594 91            [ 4] 1112 	sub	a, c
   4595 4F            [ 4] 1113 	ld	c, a
   4596 18 0C         [12] 1114 	jr	00198$
   4598                    1115 00197$:
   4598 3A B2 6C      [13] 1116 	ld	a,(#_g_bossphase + 0)
   459B B7            [ 4] 1117 	or	a, a
   459C 28 04         [12] 1118 	jr	Z,00201$
   459E 0E 02         [ 7] 1119 	ld	c, #0x02
   45A0 18 02         [12] 1120 	jr	00202$
   45A2                    1121 00201$:
   45A2 0E 01         [ 7] 1122 	ld	c, #0x01
   45A4                    1123 00202$:
   45A4                    1124 00198$:
   45A4 21 A9 6C      [10] 1125 	ld	hl, #(_g_boss + 0x0002)
   45A7 71            [ 7] 1126 	ld	(hl), c
                           1127 ;src/game.c:278: enemyupdate(&g_boss);
   45A8 21 A7 6C      [10] 1128 	ld	hl, #_g_boss
   45AB E5            [11] 1129 	push	hl
   45AC CD AB 60      [17] 1130 	call	_enemyupdate
   45AF F1            [10] 1131 	pop	af
                           1132 ;src/game.c:281: for (i = 0; i < MAX_PROJECTILES; ++i) {
   45B0                    1133 00234$:
   45B0 0E 00         [ 7] 1134 	ld	c, #0x00
   45B2                    1135 00193$:
                           1136 ;src/game.c:282: if (!g_projectiles[i].active) continue;
   45B2 06 00         [ 7] 1137 	ld	b,#0x00
   45B4 69            [ 4] 1138 	ld	l, c
   45B5 60            [ 4] 1139 	ld	h, b
   45B6 29            [11] 1140 	add	hl, hl
   45B7 29            [11] 1141 	add	hl, hl
   45B8 09            [11] 1142 	add	hl, bc
   45B9 29            [11] 1143 	add	hl, hl
   45BA EB            [ 4] 1144 	ex	de,hl
   45BB 21 1B 6C      [10] 1145 	ld	hl, #_g_projectiles
   45BE 19            [11] 1146 	add	hl,de
   45BF EB            [ 4] 1147 	ex	de,hl
   45C0 21 06 00      [10] 1148 	ld	hl, #0x0006
   45C3 19            [11] 1149 	add	hl,de
   45C4 DD 75 FE      [19] 1150 	ld	-2 (ix), l
   45C7 DD 74 FF      [19] 1151 	ld	-1 (ix), h
   45CA 7E            [ 7] 1152 	ld	a, (hl)
   45CB B7            [ 4] 1153 	or	a, a
   45CC CA ED 47      [10] 1154 	jp	Z, 00147$
                           1155 ;src/game.c:283: for (j = 0; j < MAX_ENEMIES; ++j) {
   45CF DD 36 E7 00   [19] 1156 	ld	-25 (ix), #0x00
   45D3                    1157 00192$:
                           1158 ;src/game.c:284: if (!g_enemies[j].active) continue;
   45D3 D5            [11] 1159 	push	de
   45D4 DD 5E E7      [19] 1160 	ld	e,-25 (ix)
   45D7 16 00         [ 7] 1161 	ld	d,#0x00
   45D9 6B            [ 4] 1162 	ld	l, e
   45DA 62            [ 4] 1163 	ld	h, d
   45DB 29            [11] 1164 	add	hl, hl
   45DC 29            [11] 1165 	add	hl, hl
   45DD 19            [11] 1166 	add	hl, de
   45DE 29            [11] 1167 	add	hl, hl
   45DF D1            [10] 1168 	pop	de
   45E0 3E DF         [ 7] 1169 	ld	a, #<(_g_enemies)
   45E2 85            [ 4] 1170 	add	a, l
   45E3 DD 77 FC      [19] 1171 	ld	-4 (ix), a
   45E6 3E 6B         [ 7] 1172 	ld	a, #>(_g_enemies)
   45E8 8C            [ 4] 1173 	adc	a, h
   45E9 DD 77 FD      [19] 1174 	ld	-3 (ix), a
   45EC DD 6E FC      [19] 1175 	ld	l,-4 (ix)
   45EF DD 66 FD      [19] 1176 	ld	h,-3 (ix)
   45F2 C5            [11] 1177 	push	bc
   45F3 01 06 00      [10] 1178 	ld	bc, #0x0006
   45F6 09            [11] 1179 	add	hl, bc
   45F7 C1            [10] 1180 	pop	bc
   45F8 46            [ 7] 1181 	ld	b, (hl)
                           1182 ;src/game.c:285: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   45F9 21 05 00      [10] 1183 	ld	hl, #0x0005
   45FC 19            [11] 1184 	add	hl,de
   45FD DD 75 FA      [19] 1185 	ld	-6 (ix), l
   4600 DD 74 FB      [19] 1186 	ld	-5 (ix), h
   4603 21 04 00      [10] 1187 	ld	hl, #0x0004
   4606 19            [11] 1188 	add	hl,de
   4607 DD 75 F8      [19] 1189 	ld	-8 (ix), l
   460A DD 74 F9      [19] 1190 	ld	-7 (ix), h
   460D 21 01 00      [10] 1191 	ld	hl, #0x0001
   4610 19            [11] 1192 	add	hl,de
   4611 DD 75 F6      [19] 1193 	ld	-10 (ix), l
   4614 DD 74 F7      [19] 1194 	ld	-9 (ix), h
                           1195 ;src/game.c:287: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   4617 21 07 00      [10] 1196 	ld	hl, #0x0007
   461A 19            [11] 1197 	add	hl,de
   461B DD 75 F4      [19] 1198 	ld	-12 (ix), l
   461E DD 74 F5      [19] 1199 	ld	-11 (ix), h
                           1200 ;src/game.c:284: if (!g_enemies[j].active) continue;
   4621 78            [ 4] 1201 	ld	a, b
   4622 B7            [ 4] 1202 	or	a, a
   4623 CA 1B 47      [10] 1203 	jp	Z, 00139$
                           1204 ;src/game.c:286: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   4626 DD 6E FC      [19] 1205 	ld	l,-4 (ix)
   4629 DD 66 FD      [19] 1206 	ld	h,-3 (ix)
   462C 23            [ 6] 1207 	inc	hl
   462D 23            [ 6] 1208 	inc	hl
   462E 23            [ 6] 1209 	inc	hl
   462F 23            [ 6] 1210 	inc	hl
   4630 23            [ 6] 1211 	inc	hl
   4631 7E            [ 7] 1212 	ld	a, (hl)
   4632 DD 77 F3      [19] 1213 	ld	-13 (ix), a
   4635 DD 6E FC      [19] 1214 	ld	l,-4 (ix)
   4638 DD 66 FD      [19] 1215 	ld	h,-3 (ix)
   463B 23            [ 6] 1216 	inc	hl
   463C 23            [ 6] 1217 	inc	hl
   463D 23            [ 6] 1218 	inc	hl
   463E 23            [ 6] 1219 	inc	hl
   463F 7E            [ 7] 1220 	ld	a, (hl)
   4640 DD 77 F2      [19] 1221 	ld	-14 (ix), a
   4643 DD 6E FC      [19] 1222 	ld	l,-4 (ix)
   4646 DD 66 FD      [19] 1223 	ld	h,-3 (ix)
   4649 23            [ 6] 1224 	inc	hl
   464A 46            [ 7] 1225 	ld	b, (hl)
   464B DD 70 F0      [19] 1226 	ld	-16 (ix), b
   464E DD 36 F1 00   [19] 1227 	ld	-15 (ix), #0x00
   4652 DD 6E FC      [19] 1228 	ld	l,-4 (ix)
   4655 DD 66 FD      [19] 1229 	ld	h,-3 (ix)
   4658 46            [ 7] 1230 	ld	b, (hl)
   4659 DD 70 EE      [19] 1231 	ld	-18 (ix), b
   465C DD 36 EF 00   [19] 1232 	ld	-17 (ix), #0x00
                           1233 ;src/game.c:285: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4660 DD 6E FA      [19] 1234 	ld	l,-6 (ix)
   4663 DD 66 FB      [19] 1235 	ld	h,-5 (ix)
   4666 7E            [ 7] 1236 	ld	a, (hl)
   4667 DD 77 ED      [19] 1237 	ld	-19 (ix), a
   466A DD 6E F8      [19] 1238 	ld	l,-8 (ix)
   466D DD 66 F9      [19] 1239 	ld	h,-7 (ix)
   4670 46            [ 7] 1240 	ld	b, (hl)
   4671 DD 6E F6      [19] 1241 	ld	l,-10 (ix)
   4674 DD 66 F7      [19] 1242 	ld	h,-9 (ix)
   4677 6E            [ 7] 1243 	ld	l, (hl)
   4678 DD 75 EB      [19] 1244 	ld	-21 (ix), l
   467B DD 36 EC 00   [19] 1245 	ld	-20 (ix), #0x00
   467F 1A            [ 7] 1246 	ld	a, (de)
   4680 DD 77 E9      [19] 1247 	ld	-23 (ix), a
   4683 DD 36 EA 00   [19] 1248 	ld	-22 (ix), #0x00
   4687 C5            [11] 1249 	push	bc
   4688 D5            [11] 1250 	push	de
   4689 DD 66 F3      [19] 1251 	ld	h, -13 (ix)
   468C DD 6E F2      [19] 1252 	ld	l, -14 (ix)
   468F E5            [11] 1253 	push	hl
   4690 DD 6E F0      [19] 1254 	ld	l,-16 (ix)
   4693 DD 66 F1      [19] 1255 	ld	h,-15 (ix)
   4696 E5            [11] 1256 	push	hl
   4697 DD 6E EE      [19] 1257 	ld	l,-18 (ix)
   469A DD 66 EF      [19] 1258 	ld	h,-17 (ix)
   469D E5            [11] 1259 	push	hl
   469E DD 7E ED      [19] 1260 	ld	a, -19 (ix)
   46A1 F5            [11] 1261 	push	af
   46A2 33            [ 6] 1262 	inc	sp
   46A3 C5            [11] 1263 	push	bc
   46A4 33            [ 6] 1264 	inc	sp
   46A5 DD 6E EB      [19] 1265 	ld	l,-21 (ix)
   46A8 DD 66 EC      [19] 1266 	ld	h,-20 (ix)
   46AB E5            [11] 1267 	push	hl
   46AC DD 6E E9      [19] 1268 	ld	l,-23 (ix)
   46AF DD 66 EA      [19] 1269 	ld	h,-22 (ix)
   46B2 E5            [11] 1270 	push	hl
   46B3 CD 1C 40      [17] 1271 	call	_rect_overlap
   46B6 FD 21 0C 00   [14] 1272 	ld	iy, #12
   46BA FD 39         [15] 1273 	add	iy, sp
   46BC FD F9         [10] 1274 	ld	sp, iy
   46BE D1            [10] 1275 	pop	de
   46BF C1            [10] 1276 	pop	bc
   46C0 7D            [ 4] 1277 	ld	a, l
   46C1 B7            [ 4] 1278 	or	a, a
   46C2 28 57         [12] 1279 	jr	Z,00139$
                           1280 ;src/game.c:287: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   46C4 DD 6E F4      [19] 1281 	ld	l,-12 (ix)
   46C7 DD 66 F5      [19] 1282 	ld	h,-11 (ix)
   46CA 66            [ 7] 1283 	ld	h, (hl)
   46CB DD 6E FC      [19] 1284 	ld	l, -4 (ix)
   46CE DD 46 FD      [19] 1285 	ld	b, -3 (ix)
   46D1 C5            [11] 1286 	push	bc
   46D2 D5            [11] 1287 	push	de
   46D3 E5            [11] 1288 	push	hl
   46D4 33            [ 6] 1289 	inc	sp
   46D5 60            [ 4] 1290 	ld	h, b
   46D6 E5            [11] 1291 	push	hl
   46D7 CD 49 63      [17] 1292 	call	_enemydamage
   46DA F1            [10] 1293 	pop	af
   46DB 33            [ 6] 1294 	inc	sp
   46DC D1            [10] 1295 	pop	de
   46DD C1            [10] 1296 	pop	bc
   46DE 7D            [ 4] 1297 	ld	a, l
   46DF B7            [ 4] 1298 	or	a, a
   46E0 28 2F         [12] 1299 	jr	Z,00138$
                           1300 ;src/game.c:288: g_score = (u16)(g_score + g_enemies[j].reward);
   46E2 DD 6E FC      [19] 1301 	ld	l,-4 (ix)
   46E5 DD 66 FD      [19] 1302 	ld	h,-3 (ix)
   46E8 C5            [11] 1303 	push	bc
   46E9 01 08 00      [10] 1304 	ld	bc, #0x0008
   46EC 09            [11] 1305 	add	hl, bc
   46ED C1            [10] 1306 	pop	bc
   46EE 6E            [ 7] 1307 	ld	l, (hl)
   46EF DD 75 E9      [19] 1308 	ld	-23 (ix), l
   46F2 DD 36 EA 00   [19] 1309 	ld	-22 (ix), #0x00
   46F6 21 97 6C      [10] 1310 	ld	hl, #_g_score
   46F9 7E            [ 7] 1311 	ld	a, (hl)
   46FA DD 86 E9      [19] 1312 	add	a, -23 (ix)
   46FD 77            [ 7] 1313 	ld	(hl), a
   46FE 23            [ 6] 1314 	inc	hl
   46FF 7E            [ 7] 1315 	ld	a, (hl)
   4700 DD 8E EA      [19] 1316 	adc	a, -22 (ix)
   4703 77            [ 7] 1317 	ld	(hl), a
                           1318 ;src/game.c:289: if (g_aliveenemies) g_aliveenemies--;
   4704 FD 21 9C 6C   [14] 1319 	ld	iy, #_g_aliveenemies
   4708 FD 7E 00      [19] 1320 	ld	a, 0 (iy)
   470B B7            [ 4] 1321 	or	a, a
   470C 28 03         [12] 1322 	jr	Z,00138$
   470E FD 35 00      [23] 1323 	dec	0 (iy)
   4711                    1324 00138$:
                           1325 ;src/game.c:291: g_projectiles[i].active = 0;
   4711 DD 6E FE      [19] 1326 	ld	l,-2 (ix)
   4714 DD 66 FF      [19] 1327 	ld	h,-1 (ix)
   4717 36 00         [10] 1328 	ld	(hl), #0x00
                           1329 ;src/game.c:292: break;
   4719 18 0B         [12] 1330 	jr	00140$
   471B                    1331 00139$:
                           1332 ;src/game.c:283: for (j = 0; j < MAX_ENEMIES; ++j) {
   471B DD 34 E7      [23] 1333 	inc	-25 (ix)
   471E DD 7E E7      [19] 1334 	ld	a, -25 (ix)
   4721 D6 06         [ 7] 1335 	sub	a, #0x06
   4723 DA D3 45      [10] 1336 	jp	C, 00192$
   4726                    1337 00140$:
                           1338 ;src/game.c:295: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4726 3A B1 6C      [13] 1339 	ld	a,(#_g_bossactive + 0)
   4729 B7            [ 4] 1340 	or	a, a
   472A CA ED 47      [10] 1341 	jp	Z, 00147$
   472D DD 6E FE      [19] 1342 	ld	l,-2 (ix)
   4730 DD 66 FF      [19] 1343 	ld	h,-1 (ix)
   4733 7E            [ 7] 1344 	ld	a, (hl)
   4734 B7            [ 4] 1345 	or	a, a
   4735 CA ED 47      [10] 1346 	jp	Z, 00147$
                           1347 ;src/game.c:296: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   4738 21 AC 6C      [10] 1348 	ld	hl, #(_g_boss + 0x0005) + 0
   473B 46            [ 7] 1349 	ld	b, (hl)
   473C 3A AB 6C      [13] 1350 	ld	a, (#(_g_boss + 0x0004) + 0)
   473F 21 A8 6C      [10] 1351 	ld	hl, #(_g_boss + 0x0001) + 0
   4742 6E            [ 7] 1352 	ld	l, (hl)
   4743 DD 75 E9      [19] 1353 	ld	-23 (ix), l
   4746 DD 36 EA 00   [19] 1354 	ld	-22 (ix), #0x00
   474A 21 A7 6C      [10] 1355 	ld	hl, #_g_boss + 0
   474D 6E            [ 7] 1356 	ld	l, (hl)
   474E DD 75 EB      [19] 1357 	ld	-21 (ix), l
   4751 DD 36 EC 00   [19] 1358 	ld	-20 (ix), #0x00
                           1359 ;src/game.c:295: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4755 DD 6E FA      [19] 1360 	ld	l,-6 (ix)
   4758 DD 66 FB      [19] 1361 	ld	h,-5 (ix)
   475B F5            [11] 1362 	push	af
   475C 7E            [ 7] 1363 	ld	a, (hl)
   475D DD 77 ED      [19] 1364 	ld	-19 (ix), a
   4760 F1            [10] 1365 	pop	af
   4761 DD 6E F8      [19] 1366 	ld	l,-8 (ix)
   4764 DD 66 F9      [19] 1367 	ld	h,-7 (ix)
   4767 F5            [11] 1368 	push	af
   4768 7E            [ 7] 1369 	ld	a, (hl)
   4769 DD 77 EE      [19] 1370 	ld	-18 (ix), a
   476C F1            [10] 1371 	pop	af
   476D DD 6E F6      [19] 1372 	ld	l,-10 (ix)
   4770 DD 66 F7      [19] 1373 	ld	h,-9 (ix)
   4773 6E            [ 7] 1374 	ld	l, (hl)
   4774 DD 75 F0      [19] 1375 	ld	-16 (ix), l
   4777 DD 36 F1 00   [19] 1376 	ld	-15 (ix), #0x00
   477B F5            [11] 1377 	push	af
   477C 1A            [ 7] 1378 	ld	a, (de)
   477D 5F            [ 4] 1379 	ld	e, a
   477E F1            [10] 1380 	pop	af
   477F 16 00         [ 7] 1381 	ld	d, #0x00
   4781 C5            [11] 1382 	push	bc
   4782 C5            [11] 1383 	push	bc
   4783 33            [ 6] 1384 	inc	sp
   4784 F5            [11] 1385 	push	af
   4785 33            [ 6] 1386 	inc	sp
   4786 DD 6E E9      [19] 1387 	ld	l,-23 (ix)
   4789 DD 66 EA      [19] 1388 	ld	h,-22 (ix)
   478C E5            [11] 1389 	push	hl
   478D DD 6E EB      [19] 1390 	ld	l,-21 (ix)
   4790 DD 66 EC      [19] 1391 	ld	h,-20 (ix)
   4793 E5            [11] 1392 	push	hl
   4794 DD 66 ED      [19] 1393 	ld	h, -19 (ix)
   4797 DD 6E EE      [19] 1394 	ld	l, -18 (ix)
   479A E5            [11] 1395 	push	hl
   479B DD 6E F0      [19] 1396 	ld	l,-16 (ix)
   479E DD 66 F1      [19] 1397 	ld	h,-15 (ix)
   47A1 E5            [11] 1398 	push	hl
   47A2 D5            [11] 1399 	push	de
   47A3 CD 1C 40      [17] 1400 	call	_rect_overlap
   47A6 FD 21 0C 00   [14] 1401 	ld	iy, #12
   47AA FD 39         [15] 1402 	add	iy, sp
   47AC FD F9         [10] 1403 	ld	sp, iy
   47AE C1            [10] 1404 	pop	bc
   47AF 7D            [ 4] 1405 	ld	a, l
   47B0 B7            [ 4] 1406 	or	a, a
   47B1 28 3A         [12] 1407 	jr	Z,00147$
                           1408 ;src/game.c:297: g_projectiles[i].active = 0;
   47B3 DD 6E FE      [19] 1409 	ld	l,-2 (ix)
   47B6 DD 66 FF      [19] 1410 	ld	h,-1 (ix)
   47B9 36 00         [10] 1411 	ld	(hl), #0x00
                           1412 ;src/game.c:298: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   47BB DD 6E F4      [19] 1413 	ld	l,-12 (ix)
   47BE DD 66 F5      [19] 1414 	ld	h,-11 (ix)
   47C1 46            [ 7] 1415 	ld	b, (hl)
   47C2 11 A7 6C      [10] 1416 	ld	de, #_g_boss
   47C5 C5            [11] 1417 	push	bc
   47C6 C5            [11] 1418 	push	bc
   47C7 33            [ 6] 1419 	inc	sp
   47C8 D5            [11] 1420 	push	de
   47C9 CD 49 63      [17] 1421 	call	_enemydamage
   47CC F1            [10] 1422 	pop	af
   47CD 33            [ 6] 1423 	inc	sp
   47CE C1            [10] 1424 	pop	bc
   47CF 7D            [ 4] 1425 	ld	a, l
   47D0 B7            [ 4] 1426 	or	a, a
   47D1 28 1A         [12] 1427 	jr	Z,00147$
                           1428 ;src/game.c:299: g_bossactive = 0;
   47D3 21 B1 6C      [10] 1429 	ld	hl,#_g_bossactive + 0
   47D6 36 00         [10] 1430 	ld	(hl), #0x00
                           1431 ;src/game.c:300: g_score = (u16)(g_score + g_boss.reward);
   47D8 21 AF 6C      [10] 1432 	ld	hl, #_g_boss + 8
   47DB 5E            [ 7] 1433 	ld	e, (hl)
   47DC 16 00         [ 7] 1434 	ld	d, #0x00
   47DE 21 97 6C      [10] 1435 	ld	hl, #_g_score
   47E1 7E            [ 7] 1436 	ld	a, (hl)
   47E2 83            [ 4] 1437 	add	a, e
   47E3 77            [ 7] 1438 	ld	(hl), a
   47E4 23            [ 6] 1439 	inc	hl
   47E5 7E            [ 7] 1440 	ld	a, (hl)
   47E6 8A            [ 4] 1441 	adc	a, d
   47E7 77            [ 7] 1442 	ld	(hl), a
                           1443 ;src/game.c:301: g_victory = 1;
   47E8 21 A0 6C      [10] 1444 	ld	hl,#_g_victory + 0
   47EB 36 01         [10] 1445 	ld	(hl), #0x01
   47ED                    1446 00147$:
                           1447 ;src/game.c:281: for (i = 0; i < MAX_PROJECTILES; ++i) {
   47ED 0C            [ 4] 1448 	inc	c
   47EE 79            [ 4] 1449 	ld	a, c
   47EF D6 06         [ 7] 1450 	sub	a, #0x06
   47F1 DA B2 45      [10] 1451 	jp	C, 00193$
                           1452 ;src/game.c:306: lives_before_damage = g_lives;
   47F4 3A 96 6C      [13] 1453 	ld	a,(#_g_lives + 0)
   47F7 DD 77 E4      [19] 1454 	ld	-28 (ix), a
                           1455 ;src/game.c:308: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1456 ;src/game.c:307: if (!g_damagecooldown) {
   47FA 3A 9E 6C      [13] 1457 	ld	a,(#_g_damagecooldown + 0)
   47FD B7            [ 4] 1458 	or	a, a
   47FE C2 6B 49      [10] 1459 	jp	NZ, 00163$
                           1460 ;src/game.c:308: for (i = 0; i < MAX_ENEMIES; ++i) {
   4801 DD 36 E8 00   [19] 1461 	ld	-24 (ix), #0x00
   4805                    1462 00194$:
                           1463 ;src/game.c:309: if (!g_enemies[i].active) continue;
   4805 DD 4E E8      [19] 1464 	ld	c,-24 (ix)
   4808 06 00         [ 7] 1465 	ld	b,#0x00
   480A 69            [ 4] 1466 	ld	l, c
   480B 60            [ 4] 1467 	ld	h, b
   480C 29            [11] 1468 	add	hl, hl
   480D 29            [11] 1469 	add	hl, hl
   480E 09            [11] 1470 	add	hl, bc
   480F 29            [11] 1471 	add	hl, hl
   4810 01 DF 6B      [10] 1472 	ld	bc,#_g_enemies
   4813 09            [11] 1473 	add	hl,bc
   4814 DD 75 E9      [19] 1474 	ld	-23 (ix), l
   4817 DD 74 EA      [19] 1475 	ld	-22 (ix), h
   481A 11 06 00      [10] 1476 	ld	de, #0x0006
   481D 19            [11] 1477 	add	hl, de
   481E 7E            [ 7] 1478 	ld	a, (hl)
   481F B7            [ 4] 1479 	or	a, a
   4820 CA B5 48      [10] 1480 	jp	Z, 00153$
                           1481 ;src/game.c:311: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   4823 DD 7E E9      [19] 1482 	ld	a, -23 (ix)
   4826 DD 77 EB      [19] 1483 	ld	-21 (ix), a
   4829 DD 7E EA      [19] 1484 	ld	a, -22 (ix)
   482C DD 77 EC      [19] 1485 	ld	-20 (ix), a
   482F DD 6E EB      [19] 1486 	ld	l,-21 (ix)
   4832 DD 66 EC      [19] 1487 	ld	h,-20 (ix)
   4835 11 05 00      [10] 1488 	ld	de, #0x0005
   4838 19            [11] 1489 	add	hl, de
   4839 7E            [ 7] 1490 	ld	a, (hl)
   483A DD 77 EB      [19] 1491 	ld	-21 (ix), a
   483D DD 6E E9      [19] 1492 	ld	l,-23 (ix)
   4840 DD 66 EA      [19] 1493 	ld	h,-22 (ix)
   4843 11 04 00      [10] 1494 	ld	de, #0x0004
   4846 19            [11] 1495 	add	hl, de
   4847 5E            [ 7] 1496 	ld	e, (hl)
   4848 DD 6E E9      [19] 1497 	ld	l,-23 (ix)
   484B DD 66 EA      [19] 1498 	ld	h,-22 (ix)
   484E 23            [ 6] 1499 	inc	hl
   484F 4E            [ 7] 1500 	ld	c, (hl)
   4850 06 00         [ 7] 1501 	ld	b, #0x00
   4852 DD 6E E9      [19] 1502 	ld	l,-23 (ix)
   4855 DD 66 EA      [19] 1503 	ld	h,-22 (ix)
   4858 56            [ 7] 1504 	ld	d, (hl)
   4859 DD 72 E9      [19] 1505 	ld	-23 (ix), d
   485C DD 36 EA 00   [19] 1506 	ld	-22 (ix), #0x00
                           1507 ;src/game.c:310: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4860 3A DA 6B      [13] 1508 	ld	a,(#(_g_player + 0x0005) + 0)
   4863 DD 77 ED      [19] 1509 	ld	-19 (ix), a
   4866 3A D9 6B      [13] 1510 	ld	a,(#(_g_player + 0x0004) + 0)
   4869 DD 77 EE      [19] 1511 	ld	-18 (ix), a
   486C 3A D6 6B      [13] 1512 	ld	a, (#(_g_player + 0x0001) + 0)
   486F DD 77 F0      [19] 1513 	ld	-16 (ix), a
   4872 DD 36 F1 00   [19] 1514 	ld	-15 (ix), #0x00
   4876 3A D5 6B      [13] 1515 	ld	a, (#_g_player + 0)
   4879 DD 77 F4      [19] 1516 	ld	-12 (ix), a
   487C DD 36 F5 00   [19] 1517 	ld	-11 (ix), #0x00
   4880 DD 56 EB      [19] 1518 	ld	d, -21 (ix)
   4883 D5            [11] 1519 	push	de
   4884 C5            [11] 1520 	push	bc
   4885 DD 6E E9      [19] 1521 	ld	l,-23 (ix)
   4888 DD 66 EA      [19] 1522 	ld	h,-22 (ix)
   488B E5            [11] 1523 	push	hl
   488C DD 66 ED      [19] 1524 	ld	h, -19 (ix)
   488F DD 6E EE      [19] 1525 	ld	l, -18 (ix)
   4892 E5            [11] 1526 	push	hl
   4893 DD 6E F0      [19] 1527 	ld	l,-16 (ix)
   4896 DD 66 F1      [19] 1528 	ld	h,-15 (ix)
   4899 E5            [11] 1529 	push	hl
   489A DD 6E F4      [19] 1530 	ld	l,-12 (ix)
   489D DD 66 F5      [19] 1531 	ld	h,-11 (ix)
   48A0 E5            [11] 1532 	push	hl
   48A1 CD 1C 40      [17] 1533 	call	_rect_overlap
   48A4 FD 21 0C 00   [14] 1534 	ld	iy, #12
   48A8 FD 39         [15] 1535 	add	iy, sp
   48AA FD F9         [10] 1536 	ld	sp, iy
   48AC 7D            [ 4] 1537 	ld	a, l
   48AD B7            [ 4] 1538 	or	a, a
   48AE 28 05         [12] 1539 	jr	Z,00153$
                           1540 ;src/game.c:312: register_player_hit();
   48B0 CD 96 42      [17] 1541 	call	_register_player_hit
                           1542 ;src/game.c:313: break;
   48B3 18 0B         [12] 1543 	jr	00154$
   48B5                    1544 00153$:
                           1545 ;src/game.c:308: for (i = 0; i < MAX_ENEMIES; ++i) {
   48B5 DD 34 E8      [23] 1546 	inc	-24 (ix)
   48B8 DD 7E E8      [19] 1547 	ld	a, -24 (ix)
   48BB D6 06         [ 7] 1548 	sub	a, #0x06
   48BD DA 05 48      [10] 1549 	jp	C, 00194$
   48C0                    1550 00154$:
                           1551 ;src/game.c:317: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   48C0 3A 9E 6C      [13] 1552 	ld	a,(#_g_damagecooldown + 0)
   48C3 B7            [ 4] 1553 	or	a, a
   48C4 20 6E         [12] 1554 	jr	NZ,00156$
   48C6 3A B1 6C      [13] 1555 	ld	a,(#_g_bossactive + 0)
   48C9 B7            [ 4] 1556 	or	a, a
   48CA 28 68         [12] 1557 	jr	Z,00156$
                           1558 ;src/game.c:318: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   48CC 3A AC 6C      [13] 1559 	ld	a,(#(_g_boss + 0x0005) + 0)
   48CF DD 77 E9      [19] 1560 	ld	-23 (ix), a
   48D2 3A AB 6C      [13] 1561 	ld	a,(#(_g_boss + 0x0004) + 0)
   48D5 DD 77 EB      [19] 1562 	ld	-21 (ix), a
   48D8 21 A8 6C      [10] 1563 	ld	hl, #(_g_boss + 0x0001) + 0
   48DB 5E            [ 7] 1564 	ld	e, (hl)
   48DC 16 00         [ 7] 1565 	ld	d, #0x00
   48DE 21 A7 6C      [10] 1566 	ld	hl, #_g_boss + 0
   48E1 4E            [ 7] 1567 	ld	c, (hl)
   48E2 06 00         [ 7] 1568 	ld	b, #0x00
                           1569 ;src/game.c:317: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   48E4 3A DA 6B      [13] 1570 	ld	a,(#(_g_player + 0x0005) + 0)
   48E7 DD 77 ED      [19] 1571 	ld	-19 (ix), a
   48EA 3A D9 6B      [13] 1572 	ld	a,(#(_g_player + 0x0004) + 0)
   48ED DD 77 EE      [19] 1573 	ld	-18 (ix), a
   48F0 3A D6 6B      [13] 1574 	ld	a, (#(_g_player + 0x0001) + 0)
   48F3 DD 77 F0      [19] 1575 	ld	-16 (ix), a
   48F6 DD 36 F1 00   [19] 1576 	ld	-15 (ix), #0x00
   48FA 3A D5 6B      [13] 1577 	ld	a, (#_g_player + 0)
   48FD DD 77 F4      [19] 1578 	ld	-12 (ix), a
   4900 DD 36 F5 00   [19] 1579 	ld	-11 (ix), #0x00
   4904 DD 66 E9      [19] 1580 	ld	h, -23 (ix)
   4907 DD 6E EB      [19] 1581 	ld	l, -21 (ix)
   490A E5            [11] 1582 	push	hl
   490B D5            [11] 1583 	push	de
   490C C5            [11] 1584 	push	bc
   490D DD 66 ED      [19] 1585 	ld	h, -19 (ix)
   4910 DD 6E EE      [19] 1586 	ld	l, -18 (ix)
   4913 E5            [11] 1587 	push	hl
   4914 DD 6E F0      [19] 1588 	ld	l,-16 (ix)
   4917 DD 66 F1      [19] 1589 	ld	h,-15 (ix)
   491A E5            [11] 1590 	push	hl
   491B DD 6E F4      [19] 1591 	ld	l,-12 (ix)
   491E DD 66 F5      [19] 1592 	ld	h,-11 (ix)
   4921 E5            [11] 1593 	push	hl
   4922 CD 1C 40      [17] 1594 	call	_rect_overlap
   4925 FD 21 0C 00   [14] 1595 	ld	iy, #12
   4929 FD 39         [15] 1596 	add	iy, sp
   492B FD F9         [10] 1597 	ld	sp, iy
   492D 7D            [ 4] 1598 	ld	a, l
   492E B7            [ 4] 1599 	or	a, a
   492F 28 03         [12] 1600 	jr	Z,00156$
                           1601 ;src/game.c:319: register_player_hit();
   4931 CD 96 42      [17] 1602 	call	_register_player_hit
   4934                    1603 00156$:
                           1604 ;src/game.c:322: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   4934 3A 9E 6C      [13] 1605 	ld	a,(#_g_damagecooldown + 0)
   4937 B7            [ 4] 1606 	or	a, a
   4938 20 31         [12] 1607 	jr	NZ,00163$
   493A 3A DA 6B      [13] 1608 	ld	a, (#(_g_player + 0x0005) + 0)
   493D 21 D9 6B      [10] 1609 	ld	hl, #(_g_player + 0x0004) + 0
   4940 56            [ 7] 1610 	ld	d, (hl)
   4941 21 D6 6B      [10] 1611 	ld	hl, #(_g_player + 0x0001) + 0
   4944 4E            [ 7] 1612 	ld	c, (hl)
   4945 06 00         [ 7] 1613 	ld	b, #0x00
   4947 21 D5 6B      [10] 1614 	ld	hl, #_g_player + 0
   494A 6E            [ 7] 1615 	ld	l, (hl)
   494B DD 75 E9      [19] 1616 	ld	-23 (ix), l
   494E DD 36 EA 00   [19] 1617 	ld	-22 (ix), #0x00
   4952 F5            [11] 1618 	push	af
   4953 33            [ 6] 1619 	inc	sp
   4954 D5            [11] 1620 	push	de
   4955 33            [ 6] 1621 	inc	sp
   4956 C5            [11] 1622 	push	bc
   4957 DD 6E E9      [19] 1623 	ld	l,-23 (ix)
   495A DD 66 EA      [19] 1624 	ld	h,-22 (ix)
   495D E5            [11] 1625 	push	hl
   495E CD E3 53      [17] 1626 	call	_collision_is_on_trap
   4961 F1            [10] 1627 	pop	af
   4962 F1            [10] 1628 	pop	af
   4963 F1            [10] 1629 	pop	af
   4964 7D            [ 4] 1630 	ld	a, l
   4965 B7            [ 4] 1631 	or	a, a
   4966 28 03         [12] 1632 	jr	Z,00163$
                           1633 ;src/game.c:323: register_player_hit();
   4968 CD 96 42      [17] 1634 	call	_register_player_hit
   496B                    1635 00163$:
                           1636 ;src/game.c:327: g_dbg_move_raw = (u8)(player_x_after_move != player_x_start);
   496B DD 7E E6      [19] 1637 	ld	a, -26 (ix)
   496E DD 96 E5      [19] 1638 	sub	a, -27 (ix)
   4971 20 04         [12] 1639 	jr	NZ,00426$
   4973 3E 01         [ 7] 1640 	ld	a,#0x01
   4975 18 01         [12] 1641 	jr	00427$
   4977                    1642 00426$:
   4977 AF            [ 4] 1643 	xor	a,a
   4978                    1644 00427$:
   4978 EE 01         [ 7] 1645 	xor	a, #0x01
   497A 4F            [ 4] 1646 	ld	c, a
   497B 21 B9 6C      [10] 1647 	ld	hl,#_g_dbg_move_raw + 0
   497E 71            [ 7] 1648 	ld	(hl), c
                           1649 ;src/game.c:258: player_x_after_move = g_player.x;
   497F 21 D5 6B      [10] 1650 	ld	hl, #_g_player + 0
   4982 4E            [ 7] 1651 	ld	c, (hl)
                           1652 ;src/game.c:328: g_dbg_move_net = (u8)(g_player.x != player_x_start);
   4983 79            [ 4] 1653 	ld	a, c
   4984 DD 96 E6      [19] 1654 	sub	a, -26 (ix)
   4987 20 04         [12] 1655 	jr	NZ,00428$
   4989 3E 01         [ 7] 1656 	ld	a,#0x01
   498B 18 01         [12] 1657 	jr	00429$
   498D                    1658 00428$:
   498D AF            [ 4] 1659 	xor	a,a
   498E                    1660 00429$:
   498E EE 01         [ 7] 1661 	xor	a, #0x01
   4990 47            [ 4] 1662 	ld	b, a
   4991 21 BA 6C      [10] 1663 	ld	hl,#_g_dbg_move_net + 0
   4994 70            [ 7] 1664 	ld	(hl), b
                           1665 ;src/game.c:329: g_dbg_move_cancelled = (u8)(g_dbg_move_raw && !g_dbg_move_net);
   4995 3A B9 6C      [13] 1666 	ld	a,(#_g_dbg_move_raw + 0)
   4998 B7            [ 4] 1667 	or	a, a
   4999 28 06         [12] 1668 	jr	Z,00203$
   499B 3A BA 6C      [13] 1669 	ld	a,(#_g_dbg_move_net + 0)
   499E B7            [ 4] 1670 	or	a, a
   499F 28 04         [12] 1671 	jr	Z,00204$
   49A1                    1672 00203$:
   49A1 06 00         [ 7] 1673 	ld	b, #0x00
   49A3 18 02         [12] 1674 	jr	00205$
   49A5                    1675 00204$:
   49A5 06 01         [ 7] 1676 	ld	b, #0x01
   49A7                    1677 00205$:
   49A7 21 BB 6C      [10] 1678 	ld	hl,#_g_dbg_move_cancelled + 0
   49AA 70            [ 7] 1679 	ld	(hl), b
                           1680 ;src/game.c:330: g_dbg_hit = (u8)(g_lives < lives_before_damage);
   49AB 21 BC 6C      [10] 1681 	ld	hl, #_g_dbg_hit
   49AE 3A 96 6C      [13] 1682 	ld	a,(#_g_lives + 0)
   49B1 DD 96 E4      [19] 1683 	sub	a, -28 (ix)
   49B4 3E 00         [ 7] 1684 	ld	a, #0x00
   49B6 17            [ 4] 1685 	rla
   49B7 77            [ 7] 1686 	ld	(hl), a
                           1687 ;src/game.c:332: if (!g_checkpointactive && g_player.x >= 44) {
   49B8 FD 21 A6 6C   [14] 1688 	ld	iy, #_g_checkpointactive
   49BC FD 7E 00      [19] 1689 	ld	a, 0 (iy)
   49BF B7            [ 4] 1690 	or	a, a
   49C0 20 1C         [12] 1691 	jr	NZ,00165$
   49C2 79            [ 4] 1692 	ld	a, c
   49C3 D6 2C         [ 7] 1693 	sub	a, #0x2c
   49C5 38 17         [12] 1694 	jr	C,00165$
                           1695 ;src/game.c:333: g_checkpointactive = 1;
   49C7 FD 36 00 01   [19] 1696 	ld	0 (iy), #0x01
                           1697 ;src/game.c:334: g_checkpointx = 52;
   49CB 21 A4 6C      [10] 1698 	ld	hl,#_g_checkpointx + 0
   49CE 36 34         [10] 1699 	ld	(hl), #0x34
                           1700 ;src/game.c:335: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   49D0 CD 18 5A      [17] 1701 	call	_tilemap_ground_y
   49D3 4D            [ 4] 1702 	ld	c, l
   49D4 21 DA 6B      [10] 1703 	ld	hl, #(_g_player + 0x0005) + 0
   49D7 46            [ 7] 1704 	ld	b, (hl)
   49D8 21 A5 6C      [10] 1705 	ld	hl, #_g_checkpointy
   49DB 79            [ 4] 1706 	ld	a, c
   49DC 90            [ 4] 1707 	sub	a, b
   49DD 77            [ 7] 1708 	ld	(hl), a
   49DE                    1709 00165$:
                           1710 ;src/game.c:338: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
   49DE 3A B4 6C      [13] 1711 	ld	a,(#_g_pickuptaken + 0)
   49E1 B7            [ 4] 1712 	or	a, a
   49E2 C2 71 4A      [10] 1713 	jp	NZ, 00168$
   49E5 CD 18 5A      [17] 1714 	call	_tilemap_ground_y
   49E8 DD 75 E9      [19] 1715 	ld	-23 (ix), l
   49EB DD 75 E9      [19] 1716 	ld	-23 (ix), l
   49EE DD 36 EA 00   [19] 1717 	ld	-22 (ix), #0x00
   49F2 DD 7E E9      [19] 1718 	ld	a, -23 (ix)
   49F5 C6 F8         [ 7] 1719 	add	a, #0xf8
   49F7 DD 77 E9      [19] 1720 	ld	-23 (ix), a
   49FA DD 7E EA      [19] 1721 	ld	a, -22 (ix)
   49FD CE FF         [ 7] 1722 	adc	a, #0xff
   49FF DD 77 EA      [19] 1723 	ld	-22 (ix), a
   4A02 3A DA 6B      [13] 1724 	ld	a,(#(_g_player + 0x0005) + 0)
   4A05 DD 77 EB      [19] 1725 	ld	-21 (ix), a
   4A08 3A D9 6B      [13] 1726 	ld	a,(#(_g_player + 0x0004) + 0)
   4A0B DD 77 ED      [19] 1727 	ld	-19 (ix), a
   4A0E 3A D6 6B      [13] 1728 	ld	a,(#(_g_player + 0x0001) + 0)
   4A11 DD 77 EE      [19] 1729 	ld	-18 (ix), a
   4A14 DD 77 EE      [19] 1730 	ld	-18 (ix), a
   4A17 DD 36 EF 00   [19] 1731 	ld	-17 (ix), #0x00
   4A1B 3A D5 6B      [13] 1732 	ld	a,(#_g_player + 0)
   4A1E DD 77 F0      [19] 1733 	ld	-16 (ix), a
   4A21 DD 77 F0      [19] 1734 	ld	-16 (ix), a
   4A24 DD 36 F1 00   [19] 1735 	ld	-15 (ix), #0x00
   4A28 21 04 04      [10] 1736 	ld	hl, #0x0404
   4A2B E5            [11] 1737 	push	hl
   4A2C DD 6E E9      [19] 1738 	ld	l,-23 (ix)
   4A2F DD 66 EA      [19] 1739 	ld	h,-22 (ix)
   4A32 E5            [11] 1740 	push	hl
   4A33 21 24 00      [10] 1741 	ld	hl, #0x0024
   4A36 E5            [11] 1742 	push	hl
   4A37 DD 66 EB      [19] 1743 	ld	h, -21 (ix)
   4A3A DD 6E ED      [19] 1744 	ld	l, -19 (ix)
   4A3D E5            [11] 1745 	push	hl
   4A3E DD 6E EE      [19] 1746 	ld	l,-18 (ix)
   4A41 DD 66 EF      [19] 1747 	ld	h,-17 (ix)
   4A44 E5            [11] 1748 	push	hl
   4A45 DD 6E F0      [19] 1749 	ld	l,-16 (ix)
   4A48 DD 66 F1      [19] 1750 	ld	h,-15 (ix)
   4A4B E5            [11] 1751 	push	hl
   4A4C CD 1C 40      [17] 1752 	call	_rect_overlap
   4A4F FD 21 0C 00   [14] 1753 	ld	iy, #12
   4A53 FD 39         [15] 1754 	add	iy, sp
   4A55 FD F9         [10] 1755 	ld	sp, iy
   4A57 7D            [ 4] 1756 	ld	a, l
   4A58 B7            [ 4] 1757 	or	a, a
   4A59 28 16         [12] 1758 	jr	Z,00168$
                           1759 ;src/game.c:339: g_pickuptaken = 1;
   4A5B 21 B4 6C      [10] 1760 	ld	hl,#_g_pickuptaken + 0
   4A5E 36 01         [10] 1761 	ld	(hl), #0x01
                           1762 ;src/game.c:340: g_weaponlevel = 1;
   4A60 21 B3 6C      [10] 1763 	ld	hl,#_g_weaponlevel + 0
   4A63 36 01         [10] 1764 	ld	(hl), #0x01
                           1765 ;src/game.c:341: g_score = (u16)(g_score + 100);
   4A65 21 97 6C      [10] 1766 	ld	hl, #_g_score
   4A68 7E            [ 7] 1767 	ld	a, (hl)
   4A69 C6 64         [ 7] 1768 	add	a, #0x64
   4A6B 77            [ 7] 1769 	ld	(hl), a
   4A6C 23            [ 6] 1770 	inc	hl
   4A6D 7E            [ 7] 1771 	ld	a, (hl)
   4A6E CE 00         [ 7] 1772 	adc	a, #0x00
   4A70 77            [ 7] 1773 	ld	(hl), a
   4A71                    1774 00168$:
                           1775 ;src/game.c:344: g_weapondisplay = (u8)(g_weaponlevel + 1);
   4A71 21 9A 6C      [10] 1776 	ld	hl, #_g_weapondisplay
   4A74 3A B3 6C      [13] 1777 	ld	a,(#_g_weaponlevel + 0)
   4A77 3C            [ 4] 1778 	inc	a
   4A78 77            [ 7] 1779 	ld	(hl), a
                           1780 ;src/game.c:346: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   4A79 3A B1 6C      [13] 1781 	ld	a,(#_g_bossactive + 0)
   4A7C B7            [ 4] 1782 	or	a, a
   4A7D 20 45         [12] 1783 	jr	NZ,00179$
   4A7F 3A 9C 6C      [13] 1784 	ld	a,(#_g_aliveenemies + 0)
   4A82 B7            [ 4] 1785 	or	a, a
   4A83 20 3F         [12] 1786 	jr	NZ,00179$
   4A85 3A A1 6C      [13] 1787 	ld	a,(#_g_gameover + 0)
   4A88 B7            [ 4] 1788 	or	a, a
   4A89 20 39         [12] 1789 	jr	NZ,00179$
                           1790 ;src/game.c:347: if (g_currentwave < TOTAL_WAVES) {
   4A8B 3A 9B 6C      [13] 1791 	ld	a,(#_g_currentwave + 0)
   4A8E D6 03         [ 7] 1792 	sub	a, #0x03
   4A90 30 20         [12] 1793 	jr	NC,00176$
                           1794 ;src/game.c:348: if (g_wavecooldown == 0) {
   4A92 3A 9D 6C      [13] 1795 	ld	a,(#_g_wavecooldown + 0)
   4A95 B7            [ 4] 1796 	or	a, a
   4A96 20 14         [12] 1797 	jr	NZ,00171$
                           1798 ;src/game.c:349: spawn_wave(g_currentwave);
   4A98 3A 9B 6C      [13] 1799 	ld	a, (_g_currentwave)
   4A9B F5            [11] 1800 	push	af
   4A9C 33            [ 6] 1801 	inc	sp
   4A9D CD A9 40      [17] 1802 	call	_spawn_wave
   4AA0 33            [ 6] 1803 	inc	sp
                           1804 ;src/game.c:350: g_currentwave++;
   4AA1 21 9B 6C      [10] 1805 	ld	hl, #_g_currentwave+0
   4AA4 34            [11] 1806 	inc	(hl)
                           1807 ;src/game.c:351: g_wavecooldown = 90;
   4AA5 21 9D 6C      [10] 1808 	ld	hl,#_g_wavecooldown + 0
   4AA8 36 5A         [10] 1809 	ld	(hl), #0x5a
   4AAA 18 18         [12] 1810 	jr	00179$
   4AAC                    1811 00171$:
                           1812 ;src/game.c:353: g_wavecooldown--;
   4AAC 21 9D 6C      [10] 1813 	ld	hl, #_g_wavecooldown+0
   4AAF 35            [11] 1814 	dec	(hl)
   4AB0 18 12         [12] 1815 	jr	00179$
   4AB2                    1816 00176$:
                           1817 ;src/game.c:355: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   4AB2 21 D5 6B      [10] 1818 	ld	hl, #_g_player + 0
   4AB5 4E            [ 7] 1819 	ld	c, (hl)
   4AB6 C5            [11] 1820 	push	bc
   4AB7 CD BC 5A      [17] 1821 	call	_tilemap_goal_x
   4ABA C1            [10] 1822 	pop	bc
   4ABB 2D            [ 4] 1823 	dec	l
   4ABC 2D            [ 4] 1824 	dec	l
   4ABD 79            [ 4] 1825 	ld	a, c
   4ABE 95            [ 4] 1826 	sub	a, l
   4ABF 38 03         [12] 1827 	jr	C,00179$
                           1828 ;src/game.c:356: spawn_boss();
   4AC1 CD AB 41      [17] 1829 	call	_spawn_boss
   4AC4                    1830 00179$:
                           1831 ;src/game.c:360: g_framecounter++;
   4AC4 FD 21 A2 6C   [14] 1832 	ld	iy, #_g_framecounter
   4AC8 FD 34 00      [23] 1833 	inc	0 (iy)
   4ACB 20 03         [12] 1834 	jr	NZ,00430$
   4ACD FD 34 01      [23] 1835 	inc	1 (iy)
   4AD0                    1836 00430$:
                           1837 ;src/game.c:361: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   4AD0 21 32 00      [10] 1838 	ld	hl, #0x0032
   4AD3 E5            [11] 1839 	push	hl
   4AD4 2A A2 6C      [16] 1840 	ld	hl, (_g_framecounter)
   4AD7 E5            [11] 1841 	push	hl
   4AD8 CD 12 6A      [17] 1842 	call	__moduint
   4ADB F1            [10] 1843 	pop	af
   4ADC F1            [10] 1844 	pop	af
   4ADD 7C            [ 4] 1845 	ld	a, h
   4ADE B5            [ 4] 1846 	or	a,l
   4ADF 20 0D         [12] 1847 	jr	NZ,00183$
   4AE1 FD 21 99 6C   [14] 1848 	ld	iy, #_g_timeleft
   4AE5 FD 7E 00      [19] 1849 	ld	a, 0 (iy)
   4AE8 B7            [ 4] 1850 	or	a, a
   4AE9 28 03         [12] 1851 	jr	Z,00183$
                           1852 ;src/game.c:362: g_timeleft--;
   4AEB FD 35 00      [23] 1853 	dec	0 (iy)
   4AEE                    1854 00183$:
                           1855 ;src/game.c:364: if (g_timeleft == 0 && !g_victory) {
   4AEE 3A 99 6C      [13] 1856 	ld	a,(#_g_timeleft + 0)
   4AF1 B7            [ 4] 1857 	or	a, a
   4AF2 20 0B         [12] 1858 	jr	NZ,00186$
   4AF4 3A A0 6C      [13] 1859 	ld	a,(#_g_victory + 0)
   4AF7 B7            [ 4] 1860 	or	a, a
   4AF8 20 05         [12] 1861 	jr	NZ,00186$
                           1862 ;src/game.c:365: g_gameover = 1;
   4AFA 21 A1 6C      [10] 1863 	ld	hl,#_g_gameover + 0
   4AFD 36 01         [10] 1864 	ld	(hl), #0x01
   4AFF                    1865 00186$:
                           1866 ;src/game.c:368: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4AFF 3A 9A 6C      [13] 1867 	ld	a, (_g_weapondisplay)
   4B02 F5            [11] 1868 	push	af
   4B03 33            [ 6] 1869 	inc	sp
   4B04 3A 99 6C      [13] 1870 	ld	a, (_g_timeleft)
   4B07 F5            [11] 1871 	push	af
   4B08 33            [ 6] 1872 	inc	sp
   4B09 2A 97 6C      [16] 1873 	ld	hl, (_g_score)
   4B0C E5            [11] 1874 	push	hl
   4B0D 3A 96 6C      [13] 1875 	ld	a, (_g_lives)
   4B10 F5            [11] 1876 	push	af
   4B11 33            [ 6] 1877 	inc	sp
   4B12 CD B1 56      [17] 1878 	call	_hudupdate
   4B15 F1            [10] 1879 	pop	af
   4B16 F1            [10] 1880 	pop	af
   4B17 33            [ 6] 1881 	inc	sp
   4B18                    1882 00195$:
   4B18 DD F9         [10] 1883 	ld	sp, ix
   4B1A DD E1         [14] 1884 	pop	ix
   4B1C C9            [10] 1885 	ret
                           1886 ;src/game.c:371: void game_render(void) {
                           1887 ;	---------------------------------
                           1888 ; Function game_render
                           1889 ; ---------------------------------
   4B1D                    1890 _game_render::
   4B1D DD E5         [15] 1891 	push	ix
   4B1F DD 21 00 00   [14] 1892 	ld	ix,#0
   4B23 DD 39         [15] 1893 	add	ix,sp
   4B25 F5            [11] 1894 	push	af
   4B26 3B            [ 6] 1895 	dec	sp
                           1896 ;src/game.c:378: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_player_x, prev_player_y);
   4B27 3A 8E 6D      [13] 1897 	ld	a, (_prev_player_y)
   4B2A F5            [11] 1898 	push	af
   4B2B 33            [ 6] 1899 	inc	sp
   4B2C 3A 8D 6D      [13] 1900 	ld	a, (_prev_player_x)
   4B2F F5            [11] 1901 	push	af
   4B30 33            [ 6] 1902 	inc	sp
   4B31 21 00 C0      [10] 1903 	ld	hl, #0xc000
   4B34 E5            [11] 1904 	push	hl
   4B35 CD A5 6B      [17] 1905 	call	_cpct_getScreenPtr
   4B38 4D            [ 4] 1906 	ld	c, l
   4B39 44            [ 4] 1907 	ld	b, h
                           1908 ;src/game.c:379: cpct_drawSolidBox(pvmem, 0x00, g_player.w, g_player.h);
   4B3A 21 DA 6B      [10] 1909 	ld	hl, #_g_player + 5
   4B3D 56            [ 7] 1910 	ld	d, (hl)
   4B3E 3A D9 6B      [13] 1911 	ld	a, (#_g_player + 4)
   4B41 5F            [ 4] 1912 	ld	e, a
   4B42 D5            [11] 1913 	push	de
   4B43 AF            [ 4] 1914 	xor	a, a
   4B44 F5            [11] 1915 	push	af
   4B45 33            [ 6] 1916 	inc	sp
   4B46 C5            [11] 1917 	push	bc
   4B47 CD BB 6A      [17] 1918 	call	_cpct_drawSolidBox
   4B4A F1            [10] 1919 	pop	af
   4B4B F1            [10] 1920 	pop	af
   4B4C 33            [ 6] 1921 	inc	sp
                           1922 ;src/game.c:382: for (i = 0; i < MAX_ENEMIES; ++i) {
   4B4D DD 36 FD 00   [19] 1923 	ld	-3 (ix), #0x00
   4B51                    1924 00129$:
                           1925 ;src/game.c:383: if (prev_enemy_act[i]) {
   4B51 3E 6F         [ 7] 1926 	ld	a, #<(_prev_enemy_act)
   4B53 DD 86 FD      [19] 1927 	add	a, -3 (ix)
   4B56 4F            [ 4] 1928 	ld	c, a
   4B57 3E 6C         [ 7] 1929 	ld	a, #>(_prev_enemy_act)
   4B59 CE 00         [ 7] 1930 	adc	a, #0x00
   4B5B 47            [ 4] 1931 	ld	b, a
   4B5C 0A            [ 7] 1932 	ld	a, (bc)
   4B5D B7            [ 4] 1933 	or	a, a
   4B5E 28 63         [12] 1934 	jr	Z,00130$
                           1935 ;src/game.c:384: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_enemy_x[i], prev_enemy_y[i]);
   4B60 3E 5D         [ 7] 1936 	ld	a, #<(_prev_enemy_y)
   4B62 DD 86 FD      [19] 1937 	add	a, -3 (ix)
   4B65 DD 77 FE      [19] 1938 	ld	-2 (ix), a
   4B68 3E 6C         [ 7] 1939 	ld	a, #>(_prev_enemy_y)
   4B6A CE 00         [ 7] 1940 	adc	a, #0x00
   4B6C DD 77 FF      [19] 1941 	ld	-1 (ix), a
   4B6F DD 6E FE      [19] 1942 	ld	l,-2 (ix)
   4B72 DD 66 FF      [19] 1943 	ld	h,-1 (ix)
   4B75 4E            [ 7] 1944 	ld	c, (hl)
   4B76 DD 7E FD      [19] 1945 	ld	a, -3 (ix)
   4B79 C6 57         [ 7] 1946 	add	a, #<(_prev_enemy_x)
   4B7B DD 77 FE      [19] 1947 	ld	-2 (ix), a
   4B7E 3E 00         [ 7] 1948 	ld	a, #0x00
   4B80 CE 6C         [ 7] 1949 	adc	a, #>(_prev_enemy_x)
   4B82 DD 77 FF      [19] 1950 	ld	-1 (ix), a
   4B85 DD 6E FE      [19] 1951 	ld	l,-2 (ix)
   4B88 DD 66 FF      [19] 1952 	ld	h,-1 (ix)
   4B8B 46            [ 7] 1953 	ld	b, (hl)
   4B8C 79            [ 4] 1954 	ld	a, c
   4B8D F5            [11] 1955 	push	af
   4B8E 33            [ 6] 1956 	inc	sp
   4B8F C5            [11] 1957 	push	bc
   4B90 33            [ 6] 1958 	inc	sp
   4B91 21 00 C0      [10] 1959 	ld	hl, #0xc000
   4B94 E5            [11] 1960 	push	hl
   4B95 CD A5 6B      [17] 1961 	call	_cpct_getScreenPtr
   4B98 4D            [ 4] 1962 	ld	c, l
   4B99 44            [ 4] 1963 	ld	b, h
                           1964 ;src/game.c:385: cpct_drawSolidBox(pvmem, 0x00, prev_enemy_w[i], prev_enemy_h[i]);
   4B9A 3E 69         [ 7] 1965 	ld	a, #<(_prev_enemy_h)
   4B9C DD 86 FD      [19] 1966 	add	a, -3 (ix)
   4B9F 6F            [ 4] 1967 	ld	l, a
   4BA0 3E 6C         [ 7] 1968 	ld	a, #>(_prev_enemy_h)
   4BA2 CE 00         [ 7] 1969 	adc	a, #0x00
   4BA4 67            [ 4] 1970 	ld	h, a
   4BA5 7E            [ 7] 1971 	ld	a, (hl)
   4BA6 DD 77 FE      [19] 1972 	ld	-2 (ix), a
   4BA9 3E 63         [ 7] 1973 	ld	a, #<(_prev_enemy_w)
   4BAB DD 86 FD      [19] 1974 	add	a, -3 (ix)
   4BAE 6F            [ 4] 1975 	ld	l, a
   4BAF 3E 6C         [ 7] 1976 	ld	a, #>(_prev_enemy_w)
   4BB1 CE 00         [ 7] 1977 	adc	a, #0x00
   4BB3 67            [ 4] 1978 	ld	h, a
   4BB4 5E            [ 7] 1979 	ld	e, (hl)
   4BB5 DD 56 FE      [19] 1980 	ld	d, -2 (ix)
   4BB8 D5            [11] 1981 	push	de
   4BB9 AF            [ 4] 1982 	xor	a, a
   4BBA F5            [11] 1983 	push	af
   4BBB 33            [ 6] 1984 	inc	sp
   4BBC C5            [11] 1985 	push	bc
   4BBD CD BB 6A      [17] 1986 	call	_cpct_drawSolidBox
   4BC0 F1            [10] 1987 	pop	af
   4BC1 F1            [10] 1988 	pop	af
   4BC2 33            [ 6] 1989 	inc	sp
   4BC3                    1990 00130$:
                           1991 ;src/game.c:382: for (i = 0; i < MAX_ENEMIES; ++i) {
   4BC3 DD 34 FD      [23] 1992 	inc	-3 (ix)
   4BC6 DD 7E FD      [19] 1993 	ld	a, -3 (ix)
   4BC9 D6 06         [ 7] 1994 	sub	a, #0x06
   4BCB 38 84         [12] 1995 	jr	C,00129$
                           1996 ;src/game.c:390: if (prev_boss_act) {
   4BCD 3A 77 6C      [13] 1997 	ld	a,(#_prev_boss_act + 0)
   4BD0 B7            [ 4] 1998 	or	a, a
   4BD1 28 26         [12] 1999 	jr	Z,00164$
                           2000 ;src/game.c:391: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_boss_x, prev_boss_y);
   4BD3 3A 76 6C      [13] 2001 	ld	a, (_prev_boss_y)
   4BD6 F5            [11] 2002 	push	af
   4BD7 33            [ 6] 2003 	inc	sp
   4BD8 3A 75 6C      [13] 2004 	ld	a, (_prev_boss_x)
   4BDB F5            [11] 2005 	push	af
   4BDC 33            [ 6] 2006 	inc	sp
   4BDD 21 00 C0      [10] 2007 	ld	hl, #0xc000
   4BE0 E5            [11] 2008 	push	hl
   4BE1 CD A5 6B      [17] 2009 	call	_cpct_getScreenPtr
   4BE4 4D            [ 4] 2010 	ld	c, l
   4BE5 44            [ 4] 2011 	ld	b, h
                           2012 ;src/game.c:392: cpct_drawSolidBox(pvmem, 0x00, g_boss.w, g_boss.h);
   4BE6 21 AC 6C      [10] 2013 	ld	hl, #_g_boss + 5
   4BE9 56            [ 7] 2014 	ld	d, (hl)
   4BEA 3A AB 6C      [13] 2015 	ld	a, (#_g_boss + 4)
   4BED 5F            [ 4] 2016 	ld	e, a
   4BEE D5            [11] 2017 	push	de
   4BEF AF            [ 4] 2018 	xor	a, a
   4BF0 F5            [11] 2019 	push	af
   4BF1 33            [ 6] 2020 	inc	sp
   4BF2 C5            [11] 2021 	push	bc
   4BF3 CD BB 6A      [17] 2022 	call	_cpct_drawSolidBox
   4BF6 F1            [10] 2023 	pop	af
   4BF7 F1            [10] 2024 	pop	af
   4BF8 33            [ 6] 2025 	inc	sp
                           2026 ;src/game.c:396: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4BF9                    2027 00164$:
   4BF9 01 90 6C      [10] 2028 	ld	bc, #_prev_proj_act+0
   4BFC 1E 00         [ 7] 2029 	ld	e, #0x00
   4BFE                    2030 00131$:
                           2031 ;src/game.c:397: if (prev_proj_act[i]) {
   4BFE 6B            [ 4] 2032 	ld	l,e
   4BFF 26 00         [ 7] 2033 	ld	h,#0x00
   4C01 09            [11] 2034 	add	hl, bc
   4C02 7E            [ 7] 2035 	ld	a, (hl)
   4C03 B7            [ 4] 2036 	or	a, a
   4C04 28 48         [12] 2037 	jr	Z,00132$
                           2038 ;src/game.c:398: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, prev_proj_x[i], prev_proj_y[i]);
   4C06 21 7E 6C      [10] 2039 	ld	hl, #_prev_proj_y
   4C09 16 00         [ 7] 2040 	ld	d, #0x00
   4C0B 19            [11] 2041 	add	hl, de
   4C0C 56            [ 7] 2042 	ld	d, (hl)
   4C0D 3E 78         [ 7] 2043 	ld	a, #<(_prev_proj_x)
   4C0F 83            [ 4] 2044 	add	a, e
   4C10 6F            [ 4] 2045 	ld	l, a
   4C11 3E 6C         [ 7] 2046 	ld	a, #>(_prev_proj_x)
   4C13 CE 00         [ 7] 2047 	adc	a, #0x00
   4C15 67            [ 4] 2048 	ld	h, a
   4C16 7E            [ 7] 2049 	ld	a, (hl)
   4C17 C5            [11] 2050 	push	bc
   4C18 D5            [11] 2051 	push	de
   4C19 5F            [ 4] 2052 	ld	e, a
   4C1A D5            [11] 2053 	push	de
   4C1B 21 00 C0      [10] 2054 	ld	hl, #0xc000
   4C1E E5            [11] 2055 	push	hl
   4C1F CD A5 6B      [17] 2056 	call	_cpct_getScreenPtr
   4C22 D1            [10] 2057 	pop	de
   4C23 C1            [10] 2058 	pop	bc
   4C24 E5            [11] 2059 	push	hl
   4C25 FD E1         [14] 2060 	pop	iy
                           2061 ;src/game.c:399: cpct_drawSolidBox(pvmem, 0x00, prev_proj_w[i], prev_proj_h[i]);
   4C27 21 8A 6C      [10] 2062 	ld	hl, #_prev_proj_h
   4C2A 16 00         [ 7] 2063 	ld	d, #0x00
   4C2C 19            [11] 2064 	add	hl, de
   4C2D 7E            [ 7] 2065 	ld	a, (hl)
   4C2E DD 77 FE      [19] 2066 	ld	-2 (ix), a
   4C31 21 84 6C      [10] 2067 	ld	hl, #_prev_proj_w
   4C34 16 00         [ 7] 2068 	ld	d, #0x00
   4C36 19            [11] 2069 	add	hl, de
   4C37 56            [ 7] 2070 	ld	d, (hl)
   4C38 C5            [11] 2071 	push	bc
   4C39 D5            [11] 2072 	push	de
   4C3A DD 7E FE      [19] 2073 	ld	a, -2 (ix)
   4C3D F5            [11] 2074 	push	af
   4C3E 33            [ 6] 2075 	inc	sp
   4C3F D5            [11] 2076 	push	de
   4C40 33            [ 6] 2077 	inc	sp
   4C41 AF            [ 4] 2078 	xor	a, a
   4C42 F5            [11] 2079 	push	af
   4C43 33            [ 6] 2080 	inc	sp
   4C44 FD E5         [15] 2081 	push	iy
   4C46 CD BB 6A      [17] 2082 	call	_cpct_drawSolidBox
   4C49 F1            [10] 2083 	pop	af
   4C4A F1            [10] 2084 	pop	af
   4C4B 33            [ 6] 2085 	inc	sp
   4C4C D1            [10] 2086 	pop	de
   4C4D C1            [10] 2087 	pop	bc
   4C4E                    2088 00132$:
                           2089 ;src/game.c:396: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4C4E 1C            [ 4] 2090 	inc	e
   4C4F 7B            [ 4] 2091 	ld	a, e
   4C50 D6 06         [ 7] 2092 	sub	a, #0x06
   4C52 38 AA         [12] 2093 	jr	C,00131$
                           2094 ;src/game.c:404: tilemap_render();
   4C54 C5            [11] 2095 	push	bc
   4C55 CD 57 59      [17] 2096 	call	_tilemap_render
   4C58 21 D5 6B      [10] 2097 	ld	hl, #_g_player
   4C5B E5            [11] 2098 	push	hl
   4C5C CD 31 66      [17] 2099 	call	_playerrender
   4C5F F1            [10] 2100 	pop	af
   4C60 C1            [10] 2101 	pop	bc
                           2102 ;src/game.c:410: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4C61 1E 00         [ 7] 2103 	ld	e, #0x00
   4C63                    2104 00133$:
                           2105 ;src/game.c:411: projectilerender(&g_projectiles[i]);
   4C63 D5            [11] 2106 	push	de
   4C64 16 00         [ 7] 2107 	ld	d,#0x00
   4C66 6B            [ 4] 2108 	ld	l, e
   4C67 62            [ 4] 2109 	ld	h, d
   4C68 29            [11] 2110 	add	hl, hl
   4C69 29            [11] 2111 	add	hl, hl
   4C6A 19            [11] 2112 	add	hl, de
   4C6B 29            [11] 2113 	add	hl, hl
   4C6C D1            [10] 2114 	pop	de
   4C6D C5            [11] 2115 	push	bc
   4C6E 01 1B 6C      [10] 2116 	ld	bc, #_g_projectiles
   4C71 09            [11] 2117 	add	hl, bc
   4C72 D5            [11] 2118 	push	de
   4C73 E5            [11] 2119 	push	hl
   4C74 CD 6F 68      [17] 2120 	call	_projectilerender
   4C77 F1            [10] 2121 	pop	af
   4C78 D1            [10] 2122 	pop	de
   4C79 C1            [10] 2123 	pop	bc
                           2124 ;src/game.c:410: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4C7A 1C            [ 4] 2125 	inc	e
   4C7B 7B            [ 4] 2126 	ld	a, e
   4C7C D6 06         [ 7] 2127 	sub	a, #0x06
   4C7E 38 E3         [12] 2128 	jr	C,00133$
                           2129 ;src/game.c:414: for (i = 0; i < MAX_ENEMIES; ++i) {
   4C80 1E 00         [ 7] 2130 	ld	e, #0x00
   4C82                    2131 00135$:
                           2132 ;src/game.c:415: enemyrender(&g_enemies[i]);
   4C82 D5            [11] 2133 	push	de
   4C83 16 00         [ 7] 2134 	ld	d,#0x00
   4C85 6B            [ 4] 2135 	ld	l, e
   4C86 62            [ 4] 2136 	ld	h, d
   4C87 29            [11] 2137 	add	hl, hl
   4C88 29            [11] 2138 	add	hl, hl
   4C89 19            [11] 2139 	add	hl, de
   4C8A 29            [11] 2140 	add	hl, hl
   4C8B D1            [10] 2141 	pop	de
   4C8C C5            [11] 2142 	push	bc
   4C8D 01 DF 6B      [10] 2143 	ld	bc, #_g_enemies
   4C90 09            [11] 2144 	add	hl, bc
   4C91 D5            [11] 2145 	push	de
   4C92 E5            [11] 2146 	push	hl
   4C93 CD B7 62      [17] 2147 	call	_enemyrender
   4C96 F1            [10] 2148 	pop	af
   4C97 D1            [10] 2149 	pop	de
   4C98 C1            [10] 2150 	pop	bc
                           2151 ;src/game.c:414: for (i = 0; i < MAX_ENEMIES; ++i) {
   4C99 1C            [ 4] 2152 	inc	e
   4C9A 7B            [ 4] 2153 	ld	a, e
   4C9B D6 06         [ 7] 2154 	sub	a, #0x06
   4C9D 38 E3         [12] 2155 	jr	C,00135$
                           2156 ;src/game.c:418: if (g_bossactive) {
   4C9F 3A B1 6C      [13] 2157 	ld	a,(#_g_bossactive + 0)
   4CA2 B7            [ 4] 2158 	or	a, a
   4CA3 28 64         [12] 2159 	jr	Z,00112$
                           2160 ;src/game.c:419: enemyrender(&g_boss);
   4CA5 C5            [11] 2161 	push	bc
   4CA6 21 A7 6C      [10] 2162 	ld	hl, #_g_boss
   4CA9 E5            [11] 2163 	push	hl
   4CAA CD B7 62      [17] 2164 	call	_enemyrender
   4CAD 21 01 01      [10] 2165 	ld	hl, #0x0101
   4CB0 E3            [19] 2166 	ex	(sp),hl
   4CB1 CD 81 6A      [17] 2167 	call	_cpct_px2byteM0
   4CB4 55            [ 4] 2168 	ld	d, l
   4CB5 D5            [11] 2169 	push	de
   4CB6 21 18 0A      [10] 2170 	ld	hl, #0x0a18
   4CB9 E5            [11] 2171 	push	hl
   4CBA 21 00 C0      [10] 2172 	ld	hl, #0xc000
   4CBD E5            [11] 2173 	push	hl
   4CBE CD A5 6B      [17] 2174 	call	_cpct_getScreenPtr
   4CC1 D1            [10] 2175 	pop	de
   4CC2 C1            [10] 2176 	pop	bc
   4CC3 E5            [11] 2177 	push	hl
   4CC4 FD E1         [14] 2178 	pop	iy
   4CC6 C5            [11] 2179 	push	bc
   4CC7 21 20 02      [10] 2180 	ld	hl, #0x0220
   4CCA E5            [11] 2181 	push	hl
   4CCB D5            [11] 2182 	push	de
   4CCC 33            [ 6] 2183 	inc	sp
   4CCD FD E5         [15] 2184 	push	iy
   4CCF CD BB 6A      [17] 2185 	call	_cpct_drawSolidBox
   4CD2 F1            [10] 2186 	pop	af
   4CD3 F1            [10] 2187 	pop	af
   4CD4 33            [ 6] 2188 	inc	sp
   4CD5 C1            [10] 2189 	pop	bc
                           2190 ;src/game.c:421: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), cpct_px2byteM0(5, 5), (u8)(g_boss.health * 3), 2);
   4CD6 3A AE 6C      [13] 2191 	ld	a, (#_g_boss + 7)
   4CD9 5F            [ 4] 2192 	ld	e, a
   4CDA 87            [ 4] 2193 	add	a, a
   4CDB 83            [ 4] 2194 	add	a, e
   4CDC 57            [ 4] 2195 	ld	d, a
   4CDD C5            [11] 2196 	push	bc
   4CDE D5            [11] 2197 	push	de
   4CDF 21 05 05      [10] 2198 	ld	hl, #0x0505
   4CE2 E5            [11] 2199 	push	hl
   4CE3 CD 81 6A      [17] 2200 	call	_cpct_px2byteM0
   4CE6 5D            [ 4] 2201 	ld	e, l
   4CE7 F1            [10] 2202 	pop	af
   4CE8 57            [ 4] 2203 	ld	d, a
   4CE9 D5            [11] 2204 	push	de
   4CEA 21 18 0A      [10] 2205 	ld	hl, #0x0a18
   4CED E5            [11] 2206 	push	hl
   4CEE 21 00 C0      [10] 2207 	ld	hl, #0xc000
   4CF1 E5            [11] 2208 	push	hl
   4CF2 CD A5 6B      [17] 2209 	call	_cpct_getScreenPtr
   4CF5 D1            [10] 2210 	pop	de
   4CF6 C1            [10] 2211 	pop	bc
   4CF7 E5            [11] 2212 	push	hl
   4CF8 FD E1         [14] 2213 	pop	iy
   4CFA C5            [11] 2214 	push	bc
   4CFB 3E 02         [ 7] 2215 	ld	a, #0x02
   4CFD F5            [11] 2216 	push	af
   4CFE 33            [ 6] 2217 	inc	sp
   4CFF D5            [11] 2218 	push	de
   4D00 FD E5         [15] 2219 	push	iy
   4D02 CD BB 6A      [17] 2220 	call	_cpct_drawSolidBox
   4D05 F1            [10] 2221 	pop	af
   4D06 F1            [10] 2222 	pop	af
   4D07 33            [ 6] 2223 	inc	sp
   4D08 C1            [10] 2224 	pop	bc
   4D09                    2225 00112$:
                           2226 ;src/game.c:424: if (!g_pickuptaken) {
   4D09 3A B4 6C      [13] 2227 	ld	a,(#_g_pickuptaken + 0)
   4D0C B7            [ 4] 2228 	or	a, a
   4D0D 20 37         [12] 2229 	jr	NZ,00114$
                           2230 ;src/game.c:425: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), cpct_px2byteM0(7, 7), 4, 4);
   4D0F C5            [11] 2231 	push	bc
   4D10 21 07 07      [10] 2232 	ld	hl, #0x0707
   4D13 E5            [11] 2233 	push	hl
   4D14 CD 81 6A      [17] 2234 	call	_cpct_px2byteM0
   4D17 55            [ 4] 2235 	ld	d, l
   4D18 D5            [11] 2236 	push	de
   4D19 CD 18 5A      [17] 2237 	call	_tilemap_ground_y
   4D1C D1            [10] 2238 	pop	de
   4D1D C1            [10] 2239 	pop	bc
   4D1E 7D            [ 4] 2240 	ld	a, l
   4D1F C6 F8         [ 7] 2241 	add	a, #0xf8
   4D21 67            [ 4] 2242 	ld	h, a
   4D22 C5            [11] 2243 	push	bc
   4D23 D5            [11] 2244 	push	de
   4D24 E5            [11] 2245 	push	hl
   4D25 33            [ 6] 2246 	inc	sp
   4D26 3E 24         [ 7] 2247 	ld	a, #0x24
   4D28 F5            [11] 2248 	push	af
   4D29 33            [ 6] 2249 	inc	sp
   4D2A 21 00 C0      [10] 2250 	ld	hl, #0xc000
   4D2D E5            [11] 2251 	push	hl
   4D2E CD A5 6B      [17] 2252 	call	_cpct_getScreenPtr
   4D31 D1            [10] 2253 	pop	de
   4D32 C1            [10] 2254 	pop	bc
   4D33 E5            [11] 2255 	push	hl
   4D34 FD E1         [14] 2256 	pop	iy
   4D36 C5            [11] 2257 	push	bc
   4D37 21 04 04      [10] 2258 	ld	hl, #0x0404
   4D3A E5            [11] 2259 	push	hl
   4D3B D5            [11] 2260 	push	de
   4D3C 33            [ 6] 2261 	inc	sp
   4D3D FD E5         [15] 2262 	push	iy
   4D3F CD BB 6A      [17] 2263 	call	_cpct_drawSolidBox
   4D42 F1            [10] 2264 	pop	af
   4D43 F1            [10] 2265 	pop	af
   4D44 33            [ 6] 2266 	inc	sp
   4D45 C1            [10] 2267 	pop	bc
   4D46                    2268 00114$:
                           2269 ;src/game.c:428: hudrender();
   4D46 C5            [11] 2270 	push	bc
   4D47 CD E2 56      [17] 2271 	call	_hudrender
   4D4A C1            [10] 2272 	pop	bc
                           2273 ;src/game.c:430: if (g_victory) {
   4D4B 3A A0 6C      [13] 2274 	ld	a,(#_g_victory + 0)
   4D4E B7            [ 4] 2275 	or	a, a
   4D4F 28 54         [12] 2276 	jr	Z,00121$
                           2277 ;src/game.c:431: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(8, 8), 32, 12);
   4D51 C5            [11] 2278 	push	bc
   4D52 21 08 08      [10] 2279 	ld	hl, #0x0808
   4D55 E5            [11] 2280 	push	hl
   4D56 CD 81 6A      [17] 2281 	call	_cpct_px2byteM0
   4D59 55            [ 4] 2282 	ld	d, l
   4D5A D5            [11] 2283 	push	de
   4D5B 21 18 44      [10] 2284 	ld	hl, #0x4418
   4D5E E5            [11] 2285 	push	hl
   4D5F 21 00 C0      [10] 2286 	ld	hl, #0xc000
   4D62 E5            [11] 2287 	push	hl
   4D63 CD A5 6B      [17] 2288 	call	_cpct_getScreenPtr
   4D66 D1            [10] 2289 	pop	de
   4D67 C1            [10] 2290 	pop	bc
   4D68 E5            [11] 2291 	push	hl
   4D69 FD E1         [14] 2292 	pop	iy
   4D6B C5            [11] 2293 	push	bc
   4D6C 21 20 0C      [10] 2294 	ld	hl, #0x0c20
   4D6F E5            [11] 2295 	push	hl
   4D70 D5            [11] 2296 	push	de
   4D71 33            [ 6] 2297 	inc	sp
   4D72 FD E5         [15] 2298 	push	iy
   4D74 CD BB 6A      [17] 2299 	call	_cpct_drawSolidBox
   4D77 F1            [10] 2300 	pop	af
   4D78 33            [ 6] 2301 	inc	sp
   4D79 21 05 05      [10] 2302 	ld	hl,#0x0505
   4D7C E3            [19] 2303 	ex	(sp),hl
   4D7D CD 81 6A      [17] 2304 	call	_cpct_px2byteM0
   4D80 55            [ 4] 2305 	ld	d, l
   4D81 D5            [11] 2306 	push	de
   4D82 21 1C 48      [10] 2307 	ld	hl, #0x481c
   4D85 E5            [11] 2308 	push	hl
   4D86 21 00 C0      [10] 2309 	ld	hl, #0xc000
   4D89 E5            [11] 2310 	push	hl
   4D8A CD A5 6B      [17] 2311 	call	_cpct_getScreenPtr
   4D8D D1            [10] 2312 	pop	de
   4D8E C1            [10] 2313 	pop	bc
   4D8F E5            [11] 2314 	push	hl
   4D90 FD E1         [14] 2315 	pop	iy
   4D92 C5            [11] 2316 	push	bc
   4D93 21 18 08      [10] 2317 	ld	hl, #0x0818
   4D96 E5            [11] 2318 	push	hl
   4D97 D5            [11] 2319 	push	de
   4D98 33            [ 6] 2320 	inc	sp
   4D99 FD E5         [15] 2321 	push	iy
   4D9B CD BB 6A      [17] 2322 	call	_cpct_drawSolidBox
   4D9E F1            [10] 2323 	pop	af
   4D9F F1            [10] 2324 	pop	af
   4DA0 33            [ 6] 2325 	inc	sp
   4DA1 C1            [10] 2326 	pop	bc
   4DA2 C3 38 4E      [10] 2327 	jp	00122$
   4DA5                    2328 00121$:
                           2329 ;src/game.c:433: } else if (g_gameover) {
   4DA5 3A A1 6C      [13] 2330 	ld	a,(#_g_gameover + 0)
   4DA8 B7            [ 4] 2331 	or	a, a
   4DA9 28 53         [12] 2332 	jr	Z,00118$
                           2333 ;src/game.c:434: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), cpct_px2byteM0(1, 1), 32, 12);
   4DAB C5            [11] 2334 	push	bc
   4DAC 21 01 01      [10] 2335 	ld	hl, #0x0101
   4DAF E5            [11] 2336 	push	hl
   4DB0 CD 81 6A      [17] 2337 	call	_cpct_px2byteM0
   4DB3 55            [ 4] 2338 	ld	d, l
   4DB4 D5            [11] 2339 	push	de
   4DB5 21 18 44      [10] 2340 	ld	hl, #0x4418
   4DB8 E5            [11] 2341 	push	hl
   4DB9 21 00 C0      [10] 2342 	ld	hl, #0xc000
   4DBC E5            [11] 2343 	push	hl
   4DBD CD A5 6B      [17] 2344 	call	_cpct_getScreenPtr
   4DC0 D1            [10] 2345 	pop	de
   4DC1 C1            [10] 2346 	pop	bc
   4DC2 E5            [11] 2347 	push	hl
   4DC3 FD E1         [14] 2348 	pop	iy
   4DC5 C5            [11] 2349 	push	bc
   4DC6 21 20 0C      [10] 2350 	ld	hl, #0x0c20
   4DC9 E5            [11] 2351 	push	hl
   4DCA D5            [11] 2352 	push	de
   4DCB 33            [ 6] 2353 	inc	sp
   4DCC FD E5         [15] 2354 	push	iy
   4DCE CD BB 6A      [17] 2355 	call	_cpct_drawSolidBox
   4DD1 F1            [10] 2356 	pop	af
   4DD2 33            [ 6] 2357 	inc	sp
   4DD3 21 06 06      [10] 2358 	ld	hl,#0x0606
   4DD6 E3            [19] 2359 	ex	(sp),hl
   4DD7 CD 81 6A      [17] 2360 	call	_cpct_px2byteM0
   4DDA 55            [ 4] 2361 	ld	d, l
   4DDB D5            [11] 2362 	push	de
   4DDC 21 1C 48      [10] 2363 	ld	hl, #0x481c
   4DDF E5            [11] 2364 	push	hl
   4DE0 21 00 C0      [10] 2365 	ld	hl, #0xc000
   4DE3 E5            [11] 2366 	push	hl
   4DE4 CD A5 6B      [17] 2367 	call	_cpct_getScreenPtr
   4DE7 D1            [10] 2368 	pop	de
   4DE8 C1            [10] 2369 	pop	bc
   4DE9 E5            [11] 2370 	push	hl
   4DEA FD E1         [14] 2371 	pop	iy
   4DEC C5            [11] 2372 	push	bc
   4DED 21 18 08      [10] 2373 	ld	hl, #0x0818
   4DF0 E5            [11] 2374 	push	hl
   4DF1 D5            [11] 2375 	push	de
   4DF2 33            [ 6] 2376 	inc	sp
   4DF3 FD E5         [15] 2377 	push	iy
   4DF5 CD BB 6A      [17] 2378 	call	_cpct_drawSolidBox
   4DF8 F1            [10] 2379 	pop	af
   4DF9 F1            [10] 2380 	pop	af
   4DFA 33            [ 6] 2381 	inc	sp
   4DFB C1            [10] 2382 	pop	bc
   4DFC 18 3A         [12] 2383 	jr	00122$
   4DFE                    2384 00118$:
                           2385 ;src/game.c:436: } else if (g_checkpointactive) {
   4DFE 3A A6 6C      [13] 2386 	ld	a,(#_g_checkpointactive + 0)
   4E01 B7            [ 4] 2387 	or	a, a
   4E02 28 34         [12] 2388 	jr	Z,00122$
                           2389 ;src/game.c:437: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), cpct_px2byteM0(9, 9), 2, 8);
   4E04 C5            [11] 2390 	push	bc
   4E05 21 09 09      [10] 2391 	ld	hl, #0x0909
   4E08 E5            [11] 2392 	push	hl
   4E09 CD 81 6A      [17] 2393 	call	_cpct_px2byteM0
   4E0C 55            [ 4] 2394 	ld	d, l
   4E0D C1            [10] 2395 	pop	bc
   4E0E 3A A5 6C      [13] 2396 	ld	a,(#_g_checkpointy + 0)
   4E11 C6 F8         [ 7] 2397 	add	a, #0xf8
   4E13 C5            [11] 2398 	push	bc
   4E14 D5            [11] 2399 	push	de
   4E15 F5            [11] 2400 	push	af
   4E16 33            [ 6] 2401 	inc	sp
   4E17 3A A4 6C      [13] 2402 	ld	a, (_g_checkpointx)
   4E1A F5            [11] 2403 	push	af
   4E1B 33            [ 6] 2404 	inc	sp
   4E1C 21 00 C0      [10] 2405 	ld	hl, #0xc000
   4E1F E5            [11] 2406 	push	hl
   4E20 CD A5 6B      [17] 2407 	call	_cpct_getScreenPtr
   4E23 D1            [10] 2408 	pop	de
   4E24 C1            [10] 2409 	pop	bc
   4E25 E5            [11] 2410 	push	hl
   4E26 FD E1         [14] 2411 	pop	iy
   4E28 C5            [11] 2412 	push	bc
   4E29 21 02 08      [10] 2413 	ld	hl, #0x0802
   4E2C E5            [11] 2414 	push	hl
   4E2D D5            [11] 2415 	push	de
   4E2E 33            [ 6] 2416 	inc	sp
   4E2F FD E5         [15] 2417 	push	iy
   4E31 CD BB 6A      [17] 2418 	call	_cpct_drawSolidBox
   4E34 F1            [10] 2419 	pop	af
   4E35 F1            [10] 2420 	pop	af
   4E36 33            [ 6] 2421 	inc	sp
   4E37 C1            [10] 2422 	pop	bc
   4E38                    2423 00122$:
                           2424 ;src/game.c:441: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 0, 0), cpct_px2byteM0(0, 0), 40, 2);
   4E38 C5            [11] 2425 	push	bc
   4E39 21 00 00      [10] 2426 	ld	hl, #0x0000
   4E3C E5            [11] 2427 	push	hl
   4E3D CD 81 6A      [17] 2428 	call	_cpct_px2byteM0
   4E40 55            [ 4] 2429 	ld	d, l
   4E41 D5            [11] 2430 	push	de
   4E42 21 00 00      [10] 2431 	ld	hl, #0x0000
   4E45 E5            [11] 2432 	push	hl
   4E46 26 C0         [ 7] 2433 	ld	h, #0xc0
   4E48 E5            [11] 2434 	push	hl
   4E49 CD A5 6B      [17] 2435 	call	_cpct_getScreenPtr
   4E4C D1            [10] 2436 	pop	de
   4E4D C1            [10] 2437 	pop	bc
   4E4E E5            [11] 2438 	push	hl
   4E4F FD E1         [14] 2439 	pop	iy
   4E51 C5            [11] 2440 	push	bc
   4E52 21 28 02      [10] 2441 	ld	hl, #0x0228
   4E55 E5            [11] 2442 	push	hl
   4E56 D5            [11] 2443 	push	de
   4E57 33            [ 6] 2444 	inc	sp
   4E58 FD E5         [15] 2445 	push	iy
   4E5A CD BB 6A      [17] 2446 	call	_cpct_drawSolidBox
   4E5D F1            [10] 2447 	pop	af
   4E5E 33            [ 6] 2448 	inc	sp
   4E5F 21 06 06      [10] 2449 	ld	hl,#0x0606
   4E62 E3            [19] 2450 	ex	(sp),hl
   4E63 CD 81 6A      [17] 2451 	call	_cpct_px2byteM0
   4E66 55            [ 4] 2452 	ld	d, l
   4E67 C1            [10] 2453 	pop	bc
   4E68 21 D5 6B      [10] 2454 	ld	hl, #_g_player + 0
   4E6B 66            [ 7] 2455 	ld	h, (hl)
   4E6C C5            [11] 2456 	push	bc
   4E6D D5            [11] 2457 	push	de
   4E6E AF            [ 4] 2458 	xor	a, a
   4E6F F5            [11] 2459 	push	af
   4E70 33            [ 6] 2460 	inc	sp
   4E71 E5            [11] 2461 	push	hl
   4E72 33            [ 6] 2462 	inc	sp
   4E73 21 00 C0      [10] 2463 	ld	hl, #0xc000
   4E76 E5            [11] 2464 	push	hl
   4E77 CD A5 6B      [17] 2465 	call	_cpct_getScreenPtr
   4E7A D1            [10] 2466 	pop	de
   4E7B C1            [10] 2467 	pop	bc
   4E7C E5            [11] 2468 	push	hl
   4E7D FD E1         [14] 2469 	pop	iy
   4E7F C5            [11] 2470 	push	bc
   4E80 21 04 02      [10] 2471 	ld	hl, #0x0204
   4E83 E5            [11] 2472 	push	hl
   4E84 D5            [11] 2473 	push	de
   4E85 33            [ 6] 2474 	inc	sp
   4E86 FD E5         [15] 2475 	push	iy
   4E88 CD BB 6A      [17] 2476 	call	_cpct_drawSolidBox
   4E8B F1            [10] 2477 	pop	af
   4E8C 33            [ 6] 2478 	inc	sp
   4E8D 21 00 00      [10] 2479 	ld	hl,#0x0000
   4E90 E3            [19] 2480 	ex	(sp),hl
   4E91 CD 81 6A      [17] 2481 	call	_cpct_px2byteM0
   4E94 55            [ 4] 2482 	ld	d, l
   4E95 D5            [11] 2483 	push	de
   4E96 21 00 02      [10] 2484 	ld	hl, #0x0200
   4E99 E5            [11] 2485 	push	hl
   4E9A 26 C0         [ 7] 2486 	ld	h, #0xc0
   4E9C E5            [11] 2487 	push	hl
   4E9D CD A5 6B      [17] 2488 	call	_cpct_getScreenPtr
   4EA0 D1            [10] 2489 	pop	de
   4EA1 C1            [10] 2490 	pop	bc
   4EA2 E5            [11] 2491 	push	hl
   4EA3 FD E1         [14] 2492 	pop	iy
   4EA5 C5            [11] 2493 	push	bc
   4EA6 21 28 02      [10] 2494 	ld	hl, #0x0228
   4EA9 E5            [11] 2495 	push	hl
   4EAA D5            [11] 2496 	push	de
   4EAB 33            [ 6] 2497 	inc	sp
   4EAC FD E5         [15] 2498 	push	iy
   4EAE CD BB 6A      [17] 2499 	call	_cpct_drawSolidBox
   4EB1 F1            [10] 2500 	pop	af
   4EB2 F1            [10] 2501 	pop	af
   4EB3 33            [ 6] 2502 	inc	sp
   4EB4 C1            [10] 2503 	pop	bc
                           2504 ;src/game.c:447: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  0, 2), g_dbg_left           ? cpct_px2byteM0(2, 2)   : cpct_px2byteM0(0, 0), 4, 2);
   4EB5 3A B5 6C      [13] 2505 	ld	a,(#_g_dbg_left + 0)
   4EB8 B7            [ 4] 2506 	or	a, a
   4EB9 28 0C         [12] 2507 	jr	Z,00143$
   4EBB C5            [11] 2508 	push	bc
   4EBC 21 02 02      [10] 2509 	ld	hl, #0x0202
   4EBF E5            [11] 2510 	push	hl
   4EC0 CD 81 6A      [17] 2511 	call	_cpct_px2byteM0
   4EC3 55            [ 4] 2512 	ld	d, l
   4EC4 C1            [10] 2513 	pop	bc
   4EC5 18 0A         [12] 2514 	jr	00144$
   4EC7                    2515 00143$:
   4EC7 C5            [11] 2516 	push	bc
   4EC8 21 00 00      [10] 2517 	ld	hl, #0x0000
   4ECB E5            [11] 2518 	push	hl
   4ECC CD 81 6A      [17] 2519 	call	_cpct_px2byteM0
   4ECF 55            [ 4] 2520 	ld	d, l
   4ED0 C1            [10] 2521 	pop	bc
   4ED1                    2522 00144$:
   4ED1 C5            [11] 2523 	push	bc
   4ED2 D5            [11] 2524 	push	de
   4ED3 21 00 02      [10] 2525 	ld	hl, #0x0200
   4ED6 E5            [11] 2526 	push	hl
   4ED7 26 C0         [ 7] 2527 	ld	h, #0xc0
   4ED9 E5            [11] 2528 	push	hl
   4EDA CD A5 6B      [17] 2529 	call	_cpct_getScreenPtr
   4EDD D1            [10] 2530 	pop	de
   4EDE C1            [10] 2531 	pop	bc
   4EDF E5            [11] 2532 	push	hl
   4EE0 FD E1         [14] 2533 	pop	iy
   4EE2 C5            [11] 2534 	push	bc
   4EE3 21 04 02      [10] 2535 	ld	hl, #0x0204
   4EE6 E5            [11] 2536 	push	hl
   4EE7 D5            [11] 2537 	push	de
   4EE8 33            [ 6] 2538 	inc	sp
   4EE9 FD E5         [15] 2539 	push	iy
   4EEB CD BB 6A      [17] 2540 	call	_cpct_drawSolidBox
   4EEE F1            [10] 2541 	pop	af
   4EEF F1            [10] 2542 	pop	af
   4EF0 33            [ 6] 2543 	inc	sp
   4EF1 C1            [10] 2544 	pop	bc
                           2545 ;src/game.c:448: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  4, 2), g_dbg_right          ? cpct_px2byteM0(14, 14) : cpct_px2byteM0(0, 0), 4, 2);
   4EF2 3A B6 6C      [13] 2546 	ld	a,(#_g_dbg_right + 0)
   4EF5 B7            [ 4] 2547 	or	a, a
   4EF6 28 0C         [12] 2548 	jr	Z,00145$
   4EF8 C5            [11] 2549 	push	bc
   4EF9 21 0E 0E      [10] 2550 	ld	hl, #0x0e0e
   4EFC E5            [11] 2551 	push	hl
   4EFD CD 81 6A      [17] 2552 	call	_cpct_px2byteM0
   4F00 55            [ 4] 2553 	ld	d, l
   4F01 C1            [10] 2554 	pop	bc
   4F02 18 0A         [12] 2555 	jr	00146$
   4F04                    2556 00145$:
   4F04 C5            [11] 2557 	push	bc
   4F05 21 00 00      [10] 2558 	ld	hl, #0x0000
   4F08 E5            [11] 2559 	push	hl
   4F09 CD 81 6A      [17] 2560 	call	_cpct_px2byteM0
   4F0C 55            [ 4] 2561 	ld	d, l
   4F0D C1            [10] 2562 	pop	bc
   4F0E                    2563 00146$:
   4F0E C5            [11] 2564 	push	bc
   4F0F D5            [11] 2565 	push	de
   4F10 21 04 02      [10] 2566 	ld	hl, #0x0204
   4F13 E5            [11] 2567 	push	hl
   4F14 21 00 C0      [10] 2568 	ld	hl, #0xc000
   4F17 E5            [11] 2569 	push	hl
   4F18 CD A5 6B      [17] 2570 	call	_cpct_getScreenPtr
   4F1B D1            [10] 2571 	pop	de
   4F1C C1            [10] 2572 	pop	bc
   4F1D E5            [11] 2573 	push	hl
   4F1E FD E1         [14] 2574 	pop	iy
   4F20 C5            [11] 2575 	push	bc
   4F21 21 04 02      [10] 2576 	ld	hl, #0x0204
   4F24 E5            [11] 2577 	push	hl
   4F25 D5            [11] 2578 	push	de
   4F26 33            [ 6] 2579 	inc	sp
   4F27 FD E5         [15] 2580 	push	iy
   4F29 CD BB 6A      [17] 2581 	call	_cpct_drawSolidBox
   4F2C F1            [10] 2582 	pop	af
   4F2D F1            [10] 2583 	pop	af
   4F2E 33            [ 6] 2584 	inc	sp
   4F2F C1            [10] 2585 	pop	bc
                           2586 ;src/game.c:449: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START,  8, 2), g_dbg_jump           ? cpct_px2byteM0(3, 3)   : cpct_px2byteM0(0, 0), 4, 2);
   4F30 3A B7 6C      [13] 2587 	ld	a,(#_g_dbg_jump + 0)
   4F33 B7            [ 4] 2588 	or	a, a
   4F34 28 0C         [12] 2589 	jr	Z,00147$
   4F36 C5            [11] 2590 	push	bc
   4F37 21 03 03      [10] 2591 	ld	hl, #0x0303
   4F3A E5            [11] 2592 	push	hl
   4F3B CD 81 6A      [17] 2593 	call	_cpct_px2byteM0
   4F3E 55            [ 4] 2594 	ld	d, l
   4F3F C1            [10] 2595 	pop	bc
   4F40 18 0A         [12] 2596 	jr	00148$
   4F42                    2597 00147$:
   4F42 C5            [11] 2598 	push	bc
   4F43 21 00 00      [10] 2599 	ld	hl, #0x0000
   4F46 E5            [11] 2600 	push	hl
   4F47 CD 81 6A      [17] 2601 	call	_cpct_px2byteM0
   4F4A 55            [ 4] 2602 	ld	d, l
   4F4B C1            [10] 2603 	pop	bc
   4F4C                    2604 00148$:
   4F4C C5            [11] 2605 	push	bc
   4F4D D5            [11] 2606 	push	de
   4F4E 21 08 02      [10] 2607 	ld	hl, #0x0208
   4F51 E5            [11] 2608 	push	hl
   4F52 21 00 C0      [10] 2609 	ld	hl, #0xc000
   4F55 E5            [11] 2610 	push	hl
   4F56 CD A5 6B      [17] 2611 	call	_cpct_getScreenPtr
   4F59 D1            [10] 2612 	pop	de
   4F5A C1            [10] 2613 	pop	bc
   4F5B E5            [11] 2614 	push	hl
   4F5C FD E1         [14] 2615 	pop	iy
   4F5E C5            [11] 2616 	push	bc
   4F5F 21 04 02      [10] 2617 	ld	hl, #0x0204
   4F62 E5            [11] 2618 	push	hl
   4F63 D5            [11] 2619 	push	de
   4F64 33            [ 6] 2620 	inc	sp
   4F65 FD E5         [15] 2621 	push	iy
   4F67 CD BB 6A      [17] 2622 	call	_cpct_drawSolidBox
   4F6A F1            [10] 2623 	pop	af
   4F6B F1            [10] 2624 	pop	af
   4F6C 33            [ 6] 2625 	inc	sp
   4F6D C1            [10] 2626 	pop	bc
                           2627 ;src/game.c:450: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 12, 2), g_dbg_shoot          ? cpct_px2byteM0(6, 6)   : cpct_px2byteM0(0, 0), 4, 2);
   4F6E 3A B8 6C      [13] 2628 	ld	a,(#_g_dbg_shoot + 0)
   4F71 B7            [ 4] 2629 	or	a, a
   4F72 28 0C         [12] 2630 	jr	Z,00149$
   4F74 C5            [11] 2631 	push	bc
   4F75 21 06 06      [10] 2632 	ld	hl, #0x0606
   4F78 E5            [11] 2633 	push	hl
   4F79 CD 81 6A      [17] 2634 	call	_cpct_px2byteM0
   4F7C 55            [ 4] 2635 	ld	d, l
   4F7D C1            [10] 2636 	pop	bc
   4F7E 18 0A         [12] 2637 	jr	00150$
   4F80                    2638 00149$:
   4F80 C5            [11] 2639 	push	bc
   4F81 21 00 00      [10] 2640 	ld	hl, #0x0000
   4F84 E5            [11] 2641 	push	hl
   4F85 CD 81 6A      [17] 2642 	call	_cpct_px2byteM0
   4F88 55            [ 4] 2643 	ld	d, l
   4F89 C1            [10] 2644 	pop	bc
   4F8A                    2645 00150$:
   4F8A C5            [11] 2646 	push	bc
   4F8B D5            [11] 2647 	push	de
   4F8C 21 0C 02      [10] 2648 	ld	hl, #0x020c
   4F8F E5            [11] 2649 	push	hl
   4F90 21 00 C0      [10] 2650 	ld	hl, #0xc000
   4F93 E5            [11] 2651 	push	hl
   4F94 CD A5 6B      [17] 2652 	call	_cpct_getScreenPtr
   4F97 D1            [10] 2653 	pop	de
   4F98 C1            [10] 2654 	pop	bc
   4F99 E5            [11] 2655 	push	hl
   4F9A FD E1         [14] 2656 	pop	iy
   4F9C C5            [11] 2657 	push	bc
   4F9D 21 04 02      [10] 2658 	ld	hl, #0x0204
   4FA0 E5            [11] 2659 	push	hl
   4FA1 D5            [11] 2660 	push	de
   4FA2 33            [ 6] 2661 	inc	sp
   4FA3 FD E5         [15] 2662 	push	iy
   4FA5 CD BB 6A      [17] 2663 	call	_cpct_drawSolidBox
   4FA8 F1            [10] 2664 	pop	af
   4FA9 F1            [10] 2665 	pop	af
   4FAA 33            [ 6] 2666 	inc	sp
   4FAB C1            [10] 2667 	pop	bc
                           2668 ;src/game.c:451: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 16, 2), g_dbg_move_raw       ? cpct_px2byteM0(7, 7)   : cpct_px2byteM0(0, 0), 4, 2);
   4FAC 3A B9 6C      [13] 2669 	ld	a,(#_g_dbg_move_raw + 0)
   4FAF B7            [ 4] 2670 	or	a, a
   4FB0 28 0C         [12] 2671 	jr	Z,00151$
   4FB2 C5            [11] 2672 	push	bc
   4FB3 21 07 07      [10] 2673 	ld	hl, #0x0707
   4FB6 E5            [11] 2674 	push	hl
   4FB7 CD 81 6A      [17] 2675 	call	_cpct_px2byteM0
   4FBA 55            [ 4] 2676 	ld	d, l
   4FBB C1            [10] 2677 	pop	bc
   4FBC 18 0A         [12] 2678 	jr	00152$
   4FBE                    2679 00151$:
   4FBE C5            [11] 2680 	push	bc
   4FBF 21 00 00      [10] 2681 	ld	hl, #0x0000
   4FC2 E5            [11] 2682 	push	hl
   4FC3 CD 81 6A      [17] 2683 	call	_cpct_px2byteM0
   4FC6 55            [ 4] 2684 	ld	d, l
   4FC7 C1            [10] 2685 	pop	bc
   4FC8                    2686 00152$:
   4FC8 C5            [11] 2687 	push	bc
   4FC9 D5            [11] 2688 	push	de
   4FCA 21 10 02      [10] 2689 	ld	hl, #0x0210
   4FCD E5            [11] 2690 	push	hl
   4FCE 21 00 C0      [10] 2691 	ld	hl, #0xc000
   4FD1 E5            [11] 2692 	push	hl
   4FD2 CD A5 6B      [17] 2693 	call	_cpct_getScreenPtr
   4FD5 D1            [10] 2694 	pop	de
   4FD6 C1            [10] 2695 	pop	bc
   4FD7 E5            [11] 2696 	push	hl
   4FD8 FD E1         [14] 2697 	pop	iy
   4FDA C5            [11] 2698 	push	bc
   4FDB 21 04 02      [10] 2699 	ld	hl, #0x0204
   4FDE E5            [11] 2700 	push	hl
   4FDF D5            [11] 2701 	push	de
   4FE0 33            [ 6] 2702 	inc	sp
   4FE1 FD E5         [15] 2703 	push	iy
   4FE3 CD BB 6A      [17] 2704 	call	_cpct_drawSolidBox
   4FE6 F1            [10] 2705 	pop	af
   4FE7 F1            [10] 2706 	pop	af
   4FE8 33            [ 6] 2707 	inc	sp
   4FE9 C1            [10] 2708 	pop	bc
                           2709 ;src/game.c:452: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 20, 2), g_dbg_move_net       ? cpct_px2byteM0(9, 9)   : cpct_px2byteM0(0, 0), 4, 2);
   4FEA 3A BA 6C      [13] 2710 	ld	a,(#_g_dbg_move_net + 0)
   4FED B7            [ 4] 2711 	or	a, a
   4FEE 28 0C         [12] 2712 	jr	Z,00153$
   4FF0 C5            [11] 2713 	push	bc
   4FF1 21 09 09      [10] 2714 	ld	hl, #0x0909
   4FF4 E5            [11] 2715 	push	hl
   4FF5 CD 81 6A      [17] 2716 	call	_cpct_px2byteM0
   4FF8 55            [ 4] 2717 	ld	d, l
   4FF9 C1            [10] 2718 	pop	bc
   4FFA 18 0A         [12] 2719 	jr	00154$
   4FFC                    2720 00153$:
   4FFC C5            [11] 2721 	push	bc
   4FFD 21 00 00      [10] 2722 	ld	hl, #0x0000
   5000 E5            [11] 2723 	push	hl
   5001 CD 81 6A      [17] 2724 	call	_cpct_px2byteM0
   5004 55            [ 4] 2725 	ld	d, l
   5005 C1            [10] 2726 	pop	bc
   5006                    2727 00154$:
   5006 C5            [11] 2728 	push	bc
   5007 D5            [11] 2729 	push	de
   5008 21 14 02      [10] 2730 	ld	hl, #0x0214
   500B E5            [11] 2731 	push	hl
   500C 21 00 C0      [10] 2732 	ld	hl, #0xc000
   500F E5            [11] 2733 	push	hl
   5010 CD A5 6B      [17] 2734 	call	_cpct_getScreenPtr
   5013 D1            [10] 2735 	pop	de
   5014 C1            [10] 2736 	pop	bc
   5015 E5            [11] 2737 	push	hl
   5016 FD E1         [14] 2738 	pop	iy
   5018 C5            [11] 2739 	push	bc
   5019 21 04 02      [10] 2740 	ld	hl, #0x0204
   501C E5            [11] 2741 	push	hl
   501D D5            [11] 2742 	push	de
   501E 33            [ 6] 2743 	inc	sp
   501F FD E5         [15] 2744 	push	iy
   5021 CD BB 6A      [17] 2745 	call	_cpct_drawSolidBox
   5024 F1            [10] 2746 	pop	af
   5025 F1            [10] 2747 	pop	af
   5026 33            [ 6] 2748 	inc	sp
   5027 C1            [10] 2749 	pop	bc
                           2750 ;src/game.c:453: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 2), g_dbg_move_cancelled ? cpct_px2byteM0(12, 12) : cpct_px2byteM0(0, 0), 4, 2);
   5028 3A BB 6C      [13] 2751 	ld	a,(#_g_dbg_move_cancelled + 0)
   502B B7            [ 4] 2752 	or	a, a
   502C 28 0C         [12] 2753 	jr	Z,00155$
   502E C5            [11] 2754 	push	bc
   502F 21 0C 0C      [10] 2755 	ld	hl, #0x0c0c
   5032 E5            [11] 2756 	push	hl
   5033 CD 81 6A      [17] 2757 	call	_cpct_px2byteM0
   5036 55            [ 4] 2758 	ld	d, l
   5037 C1            [10] 2759 	pop	bc
   5038 18 0A         [12] 2760 	jr	00156$
   503A                    2761 00155$:
   503A C5            [11] 2762 	push	bc
   503B 21 00 00      [10] 2763 	ld	hl, #0x0000
   503E E5            [11] 2764 	push	hl
   503F CD 81 6A      [17] 2765 	call	_cpct_px2byteM0
   5042 55            [ 4] 2766 	ld	d, l
   5043 C1            [10] 2767 	pop	bc
   5044                    2768 00156$:
   5044 C5            [11] 2769 	push	bc
   5045 D5            [11] 2770 	push	de
   5046 21 18 02      [10] 2771 	ld	hl, #0x0218
   5049 E5            [11] 2772 	push	hl
   504A 21 00 C0      [10] 2773 	ld	hl, #0xc000
   504D E5            [11] 2774 	push	hl
   504E CD A5 6B      [17] 2775 	call	_cpct_getScreenPtr
   5051 D1            [10] 2776 	pop	de
   5052 C1            [10] 2777 	pop	bc
   5053 E5            [11] 2778 	push	hl
   5054 FD E1         [14] 2779 	pop	iy
   5056 C5            [11] 2780 	push	bc
   5057 21 04 02      [10] 2781 	ld	hl, #0x0204
   505A E5            [11] 2782 	push	hl
   505B D5            [11] 2783 	push	de
   505C 33            [ 6] 2784 	inc	sp
   505D FD E5         [15] 2785 	push	iy
   505F CD BB 6A      [17] 2786 	call	_cpct_drawSolidBox
   5062 F1            [10] 2787 	pop	af
   5063 F1            [10] 2788 	pop	af
   5064 33            [ 6] 2789 	inc	sp
   5065 C1            [10] 2790 	pop	bc
                           2791 ;src/game.c:454: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 2), g_dbg_hit            ? cpct_px2byteM0(15, 15) : cpct_px2byteM0(0, 0), 4, 2);
   5066 3A BC 6C      [13] 2792 	ld	a,(#_g_dbg_hit + 0)
   5069 B7            [ 4] 2793 	or	a, a
   506A 28 0C         [12] 2794 	jr	Z,00157$
   506C C5            [11] 2795 	push	bc
   506D 21 0F 0F      [10] 2796 	ld	hl, #0x0f0f
   5070 E5            [11] 2797 	push	hl
   5071 CD 81 6A      [17] 2798 	call	_cpct_px2byteM0
   5074 55            [ 4] 2799 	ld	d, l
   5075 C1            [10] 2800 	pop	bc
   5076 18 0A         [12] 2801 	jr	00158$
   5078                    2802 00157$:
   5078 C5            [11] 2803 	push	bc
   5079 21 00 00      [10] 2804 	ld	hl, #0x0000
   507C E5            [11] 2805 	push	hl
   507D CD 81 6A      [17] 2806 	call	_cpct_px2byteM0
   5080 55            [ 4] 2807 	ld	d, l
   5081 C1            [10] 2808 	pop	bc
   5082                    2809 00158$:
   5082 C5            [11] 2810 	push	bc
   5083 D5            [11] 2811 	push	de
   5084 21 1C 02      [10] 2812 	ld	hl, #0x021c
   5087 E5            [11] 2813 	push	hl
   5088 21 00 C0      [10] 2814 	ld	hl, #0xc000
   508B E5            [11] 2815 	push	hl
   508C CD A5 6B      [17] 2816 	call	_cpct_getScreenPtr
   508F D1            [10] 2817 	pop	de
   5090 C1            [10] 2818 	pop	bc
   5091 E5            [11] 2819 	push	hl
   5092 FD E1         [14] 2820 	pop	iy
   5094 C5            [11] 2821 	push	bc
   5095 21 04 02      [10] 2822 	ld	hl, #0x0204
   5098 E5            [11] 2823 	push	hl
   5099 D5            [11] 2824 	push	de
   509A 33            [ 6] 2825 	inc	sp
   509B FD E5         [15] 2826 	push	iy
   509D CD BB 6A      [17] 2827 	call	_cpct_drawSolidBox
   50A0 F1            [10] 2828 	pop	af
   50A1 33            [ 6] 2829 	inc	sp
   50A2 21 00 00      [10] 2830 	ld	hl,#0x0000
   50A5 E3            [19] 2831 	ex	(sp),hl
   50A6 CD 81 6A      [17] 2832 	call	_cpct_px2byteM0
   50A9 55            [ 4] 2833 	ld	d, l
   50AA D5            [11] 2834 	push	de
   50AB 21 00 04      [10] 2835 	ld	hl, #0x0400
   50AE E5            [11] 2836 	push	hl
   50AF 26 C0         [ 7] 2837 	ld	h, #0xc0
   50B1 E5            [11] 2838 	push	hl
   50B2 CD A5 6B      [17] 2839 	call	_cpct_getScreenPtr
   50B5 D1            [10] 2840 	pop	de
   50B6 C1            [10] 2841 	pop	bc
   50B7 E5            [11] 2842 	push	hl
   50B8 FD E1         [14] 2843 	pop	iy
   50BA C5            [11] 2844 	push	bc
   50BB 21 28 02      [10] 2845 	ld	hl, #0x0228
   50BE E5            [11] 2846 	push	hl
   50BF D5            [11] 2847 	push	de
   50C0 33            [ 6] 2848 	inc	sp
   50C1 FD E5         [15] 2849 	push	iy
   50C3 CD BB 6A      [17] 2850 	call	_cpct_drawSolidBox
   50C6 F1            [10] 2851 	pop	af
   50C7 33            [ 6] 2852 	inc	sp
   50C8 21 05 05      [10] 2853 	ld	hl,#0x0505
   50CB E3            [19] 2854 	ex	(sp),hl
   50CC CD 81 6A      [17] 2855 	call	_cpct_px2byteM0
   50CF 55            [ 4] 2856 	ld	d, l
   50D0 D5            [11] 2857 	push	de
   50D1 21 14 04      [10] 2858 	ld	hl, #0x0414
   50D4 E5            [11] 2859 	push	hl
   50D5 21 00 C0      [10] 2860 	ld	hl, #0xc000
   50D8 E5            [11] 2861 	push	hl
   50D9 CD A5 6B      [17] 2862 	call	_cpct_getScreenPtr
   50DC D1            [10] 2863 	pop	de
   50DD C1            [10] 2864 	pop	bc
   50DE E5            [11] 2865 	push	hl
   50DF FD E1         [14] 2866 	pop	iy
   50E1 C5            [11] 2867 	push	bc
   50E2 21 01 02      [10] 2868 	ld	hl, #0x0201
   50E5 E5            [11] 2869 	push	hl
   50E6 D5            [11] 2870 	push	de
   50E7 33            [ 6] 2871 	inc	sp
   50E8 FD E5         [15] 2872 	push	iy
   50EA CD BB 6A      [17] 2873 	call	_cpct_drawSolidBox
   50ED F1            [10] 2874 	pop	af
   50EE F1            [10] 2875 	pop	af
   50EF 33            [ 6] 2876 	inc	sp
   50F0 C1            [10] 2877 	pop	bc
                           2878 ;src/game.c:459: vx_mark_x = (i16)20 + ((i16)g_dbg_vx * 2);
   50F1 FD 21 BD 6C   [14] 2879 	ld	iy, #_g_dbg_vx
   50F5 FD 6E 00      [19] 2880 	ld	l, 0 (iy)
   50F8 FD 7E 00      [19] 2881 	ld	a, 0 (iy)
   50FB 17            [ 4] 2882 	rla
   50FC 9F            [ 4] 2883 	sbc	a, a
   50FD 67            [ 4] 2884 	ld	h, a
   50FE 29            [11] 2885 	add	hl, hl
   50FF 11 14 00      [10] 2886 	ld	de, #0x0014
   5102 19            [11] 2887 	add	hl, de
                           2888 ;src/game.c:460: if (vx_mark_x < 0) vx_mark_x = 0;
   5103 CB 7C         [ 8] 2889 	bit	7, h
   5105 28 03         [12] 2890 	jr	Z,00124$
   5107 21 00 00      [10] 2891 	ld	hl, #0x0000
   510A                    2892 00124$:
                           2893 ;src/game.c:461: if (vx_mark_x > 39) vx_mark_x = 39;
   510A 3E 27         [ 7] 2894 	ld	a, #0x27
   510C BD            [ 4] 2895 	cp	a, l
   510D 3E 00         [ 7] 2896 	ld	a, #0x00
   510F 9C            [ 4] 2897 	sbc	a, h
   5110 E2 15 51      [10] 2898 	jp	PO, 00281$
   5113 EE 80         [ 7] 2899 	xor	a, #0x80
   5115                    2900 00281$:
   5115 F2 1B 51      [10] 2901 	jp	P, 00126$
   5118 21 27 00      [10] 2902 	ld	hl, #0x0027
   511B                    2903 00126$:
                           2904 ;src/game.c:462: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, (u8)vx_mark_x, 4), cpct_px2byteM0(10, 10), 1, 2);
   511B E5            [11] 2905 	push	hl
   511C C5            [11] 2906 	push	bc
   511D 11 0A 0A      [10] 2907 	ld	de, #0x0a0a
   5120 D5            [11] 2908 	push	de
   5121 CD 81 6A      [17] 2909 	call	_cpct_px2byteM0
   5124 55            [ 4] 2910 	ld	d, l
   5125 C1            [10] 2911 	pop	bc
   5126 E1            [10] 2912 	pop	hl
   5127 65            [ 4] 2913 	ld	h, l
   5128 C5            [11] 2914 	push	bc
   5129 D5            [11] 2915 	push	de
   512A 3E 04         [ 7] 2916 	ld	a, #0x04
   512C F5            [11] 2917 	push	af
   512D 33            [ 6] 2918 	inc	sp
   512E E5            [11] 2919 	push	hl
   512F 33            [ 6] 2920 	inc	sp
   5130 21 00 C0      [10] 2921 	ld	hl, #0xc000
   5133 E5            [11] 2922 	push	hl
   5134 CD A5 6B      [17] 2923 	call	_cpct_getScreenPtr
   5137 D1            [10] 2924 	pop	de
   5138 C1            [10] 2925 	pop	bc
   5139 E5            [11] 2926 	push	hl
   513A FD E1         [14] 2927 	pop	iy
   513C C5            [11] 2928 	push	bc
   513D 21 01 02      [10] 2929 	ld	hl, #0x0201
   5140 E5            [11] 2930 	push	hl
   5141 D5            [11] 2931 	push	de
   5142 33            [ 6] 2932 	inc	sp
   5143 FD E5         [15] 2933 	push	iy
   5145 CD BB 6A      [17] 2934 	call	_cpct_drawSolidBox
   5148 F1            [10] 2935 	pop	af
   5149 F1            [10] 2936 	pop	af
   514A 33            [ 6] 2937 	inc	sp
   514B C1            [10] 2938 	pop	bc
                           2939 ;src/game.c:465: prev_player_x = g_player.x;
   514C 3A D5 6B      [13] 2940 	ld	a,(#_g_player + 0)
   514F 32 8D 6D      [13] 2941 	ld	(#_prev_player_x + 0),a
                           2942 ;src/game.c:466: prev_player_y = g_player.y;
   5152 3A D6 6B      [13] 2943 	ld	a,(#_g_player + 1)
   5155 32 8E 6D      [13] 2944 	ld	(#_prev_player_y + 0),a
                           2945 ;src/game.c:468: for (i = 0; i < MAX_ENEMIES; ++i) {
   5158 DD 36 FD 00   [19] 2946 	ld	-3 (ix), #0x00
   515C                    2947 00137$:
                           2948 ;src/game.c:469: prev_enemy_act[i] = g_enemies[i].active;
   515C 3E 6F         [ 7] 2949 	ld	a, #<(_prev_enemy_act)
   515E DD 86 FD      [19] 2950 	add	a, -3 (ix)
   5161 5F            [ 4] 2951 	ld	e, a
   5162 3E 6C         [ 7] 2952 	ld	a, #>(_prev_enemy_act)
   5164 CE 00         [ 7] 2953 	adc	a, #0x00
   5166 57            [ 4] 2954 	ld	d, a
   5167 D5            [11] 2955 	push	de
   5168 DD 5E FD      [19] 2956 	ld	e,-3 (ix)
   516B 16 00         [ 7] 2957 	ld	d,#0x00
   516D 6B            [ 4] 2958 	ld	l, e
   516E 62            [ 4] 2959 	ld	h, d
   516F 29            [11] 2960 	add	hl, hl
   5170 29            [11] 2961 	add	hl, hl
   5171 19            [11] 2962 	add	hl, de
   5172 29            [11] 2963 	add	hl, hl
   5173 D1            [10] 2964 	pop	de
   5174 FD 21 DF 6B   [14] 2965 	ld	iy, #_g_enemies
   5178 C5            [11] 2966 	push	bc
   5179 4D            [ 4] 2967 	ld	c, l
   517A 44            [ 4] 2968 	ld	b, h
   517B FD 09         [15] 2969 	add	iy, bc
   517D C1            [10] 2970 	pop	bc
   517E FD E5         [15] 2971 	push	iy
   5180 E1            [10] 2972 	pop	hl
   5181 C5            [11] 2973 	push	bc
   5182 01 06 00      [10] 2974 	ld	bc, #0x0006
   5185 09            [11] 2975 	add	hl, bc
   5186 C1            [10] 2976 	pop	bc
   5187 7E            [ 7] 2977 	ld	a, (hl)
   5188 12            [ 7] 2978 	ld	(de), a
                           2979 ;src/game.c:470: prev_enemy_x[i]   = g_enemies[i].x;
   5189 3E 57         [ 7] 2980 	ld	a, #<(_prev_enemy_x)
   518B DD 86 FD      [19] 2981 	add	a, -3 (ix)
   518E 5F            [ 4] 2982 	ld	e, a
   518F 3E 6C         [ 7] 2983 	ld	a, #>(_prev_enemy_x)
   5191 CE 00         [ 7] 2984 	adc	a, #0x00
   5193 57            [ 4] 2985 	ld	d, a
   5194 FD 7E 00      [19] 2986 	ld	a, 0 (iy)
   5197 12            [ 7] 2987 	ld	(de), a
                           2988 ;src/game.c:471: prev_enemy_y[i]   = g_enemies[i].y;
   5198 3E 5D         [ 7] 2989 	ld	a, #<(_prev_enemy_y)
   519A DD 86 FD      [19] 2990 	add	a, -3 (ix)
   519D 5F            [ 4] 2991 	ld	e, a
   519E 3E 6C         [ 7] 2992 	ld	a, #>(_prev_enemy_y)
   51A0 CE 00         [ 7] 2993 	adc	a, #0x00
   51A2 57            [ 4] 2994 	ld	d, a
   51A3 FD E5         [15] 2995 	push	iy
   51A5 E1            [10] 2996 	pop	hl
   51A6 23            [ 6] 2997 	inc	hl
   51A7 7E            [ 7] 2998 	ld	a, (hl)
   51A8 12            [ 7] 2999 	ld	(de), a
                           3000 ;src/game.c:472: prev_enemy_w[i]   = g_enemies[i].w;
   51A9 3E 63         [ 7] 3001 	ld	a, #<(_prev_enemy_w)
   51AB DD 86 FD      [19] 3002 	add	a, -3 (ix)
   51AE 5F            [ 4] 3003 	ld	e, a
   51AF 3E 6C         [ 7] 3004 	ld	a, #>(_prev_enemy_w)
   51B1 CE 00         [ 7] 3005 	adc	a, #0x00
   51B3 57            [ 4] 3006 	ld	d, a
   51B4 FD E5         [15] 3007 	push	iy
   51B6 E1            [10] 3008 	pop	hl
   51B7 23            [ 6] 3009 	inc	hl
   51B8 23            [ 6] 3010 	inc	hl
   51B9 23            [ 6] 3011 	inc	hl
   51BA 23            [ 6] 3012 	inc	hl
   51BB 7E            [ 7] 3013 	ld	a, (hl)
   51BC 12            [ 7] 3014 	ld	(de), a
                           3015 ;src/game.c:473: prev_enemy_h[i]   = g_enemies[i].h;
   51BD 3E 69         [ 7] 3016 	ld	a, #<(_prev_enemy_h)
   51BF DD 86 FD      [19] 3017 	add	a, -3 (ix)
   51C2 5F            [ 4] 3018 	ld	e, a
   51C3 3E 6C         [ 7] 3019 	ld	a, #>(_prev_enemy_h)
   51C5 CE 00         [ 7] 3020 	adc	a, #0x00
   51C7 57            [ 4] 3021 	ld	d, a
   51C8 FD 7E 05      [19] 3022 	ld	a, 5 (iy)
   51CB 12            [ 7] 3023 	ld	(de), a
                           3024 ;src/game.c:468: for (i = 0; i < MAX_ENEMIES; ++i) {
   51CC DD 34 FD      [23] 3025 	inc	-3 (ix)
   51CF DD 7E FD      [19] 3026 	ld	a, -3 (ix)
   51D2 D6 06         [ 7] 3027 	sub	a, #0x06
   51D4 38 86         [12] 3028 	jr	C,00137$
                           3029 ;src/game.c:476: prev_boss_act = g_bossactive;
   51D6 3A B1 6C      [13] 3030 	ld	a,(#_g_bossactive + 0)
   51D9 32 77 6C      [13] 3031 	ld	(#_prev_boss_act + 0),a
                           3032 ;src/game.c:477: prev_boss_x   = g_boss.x;
   51DC 3A A7 6C      [13] 3033 	ld	a, (#_g_boss+0)
   51DF 32 75 6C      [13] 3034 	ld	(#_prev_boss_x + 0),a
                           3035 ;src/game.c:478: prev_boss_y   = g_boss.y;
   51E2 3A A8 6C      [13] 3036 	ld	a, (#_g_boss+1)
   51E5 32 76 6C      [13] 3037 	ld	(#_prev_boss_y + 0),a
                           3038 ;src/game.c:480: for (i = 0; i < MAX_PROJECTILES; ++i) {
   51E8 DD 36 FD 00   [19] 3039 	ld	-3 (ix), #0x00
   51EC                    3040 00139$:
                           3041 ;src/game.c:481: prev_proj_act[i] = g_projectiles[i].active;
   51EC DD 7E FD      [19] 3042 	ld	a, -3 (ix)
   51EF 81            [ 4] 3043 	add	a, c
   51F0 5F            [ 4] 3044 	ld	e, a
   51F1 3E 00         [ 7] 3045 	ld	a, #0x00
   51F3 88            [ 4] 3046 	adc	a, b
   51F4 57            [ 4] 3047 	ld	d, a
   51F5 D5            [11] 3048 	push	de
   51F6 DD 5E FD      [19] 3049 	ld	e,-3 (ix)
   51F9 16 00         [ 7] 3050 	ld	d,#0x00
   51FB 6B            [ 4] 3051 	ld	l, e
   51FC 62            [ 4] 3052 	ld	h, d
   51FD 29            [11] 3053 	add	hl, hl
   51FE 29            [11] 3054 	add	hl, hl
   51FF 19            [11] 3055 	add	hl, de
   5200 29            [11] 3056 	add	hl, hl
   5201 D1            [10] 3057 	pop	de
   5202 FD 21 1B 6C   [14] 3058 	ld	iy, #_g_projectiles
   5206 C5            [11] 3059 	push	bc
   5207 4D            [ 4] 3060 	ld	c, l
   5208 44            [ 4] 3061 	ld	b, h
   5209 FD 09         [15] 3062 	add	iy, bc
   520B C1            [10] 3063 	pop	bc
   520C FD E5         [15] 3064 	push	iy
   520E E1            [10] 3065 	pop	hl
   520F C5            [11] 3066 	push	bc
   5210 01 06 00      [10] 3067 	ld	bc, #0x0006
   5213 09            [11] 3068 	add	hl, bc
   5214 C1            [10] 3069 	pop	bc
   5215 7E            [ 7] 3070 	ld	a, (hl)
   5216 12            [ 7] 3071 	ld	(de), a
                           3072 ;src/game.c:482: prev_proj_x[i]   = g_projectiles[i].x;
   5217 3E 78         [ 7] 3073 	ld	a, #<(_prev_proj_x)
   5219 DD 86 FD      [19] 3074 	add	a, -3 (ix)
   521C 5F            [ 4] 3075 	ld	e, a
   521D 3E 6C         [ 7] 3076 	ld	a, #>(_prev_proj_x)
   521F CE 00         [ 7] 3077 	adc	a, #0x00
   5221 57            [ 4] 3078 	ld	d, a
   5222 FD 7E 00      [19] 3079 	ld	a, 0 (iy)
   5225 12            [ 7] 3080 	ld	(de), a
                           3081 ;src/game.c:483: prev_proj_y[i]   = g_projectiles[i].y;
   5226 3E 7E         [ 7] 3082 	ld	a, #<(_prev_proj_y)
   5228 DD 86 FD      [19] 3083 	add	a, -3 (ix)
   522B 5F            [ 4] 3084 	ld	e, a
   522C 3E 6C         [ 7] 3085 	ld	a, #>(_prev_proj_y)
   522E CE 00         [ 7] 3086 	adc	a, #0x00
   5230 57            [ 4] 3087 	ld	d, a
   5231 FD E5         [15] 3088 	push	iy
   5233 E1            [10] 3089 	pop	hl
   5234 23            [ 6] 3090 	inc	hl
   5235 7E            [ 7] 3091 	ld	a, (hl)
   5236 12            [ 7] 3092 	ld	(de), a
                           3093 ;src/game.c:484: prev_proj_w[i]   = g_projectiles[i].w;
   5237 3E 84         [ 7] 3094 	ld	a, #<(_prev_proj_w)
   5239 DD 86 FD      [19] 3095 	add	a, -3 (ix)
   523C 5F            [ 4] 3096 	ld	e, a
   523D 3E 6C         [ 7] 3097 	ld	a, #>(_prev_proj_w)
   523F CE 00         [ 7] 3098 	adc	a, #0x00
   5241 57            [ 4] 3099 	ld	d, a
   5242 FD E5         [15] 3100 	push	iy
   5244 E1            [10] 3101 	pop	hl
   5245 23            [ 6] 3102 	inc	hl
   5246 23            [ 6] 3103 	inc	hl
   5247 23            [ 6] 3104 	inc	hl
   5248 23            [ 6] 3105 	inc	hl
   5249 7E            [ 7] 3106 	ld	a, (hl)
   524A 12            [ 7] 3107 	ld	(de), a
                           3108 ;src/game.c:485: prev_proj_h[i]   = g_projectiles[i].h;
   524B 3E 8A         [ 7] 3109 	ld	a, #<(_prev_proj_h)
   524D DD 86 FD      [19] 3110 	add	a, -3 (ix)
   5250 5F            [ 4] 3111 	ld	e, a
   5251 3E 6C         [ 7] 3112 	ld	a, #>(_prev_proj_h)
   5253 CE 00         [ 7] 3113 	adc	a, #0x00
   5255 57            [ 4] 3114 	ld	d, a
   5256 FD 7E 05      [19] 3115 	ld	a, 5 (iy)
   5259 12            [ 7] 3116 	ld	(de), a
                           3117 ;src/game.c:480: for (i = 0; i < MAX_PROJECTILES; ++i) {
   525A DD 34 FD      [23] 3118 	inc	-3 (ix)
   525D DD 7E FD      [19] 3119 	ld	a, -3 (ix)
   5260 D6 06         [ 7] 3120 	sub	a, #0x06
   5262 38 88         [12] 3121 	jr	C,00139$
   5264 DD F9         [10] 3122 	ld	sp, ix
   5266 DD E1         [14] 3123 	pop	ix
   5268 C9            [10] 3124 	ret
                           3125 	.area _CODE
                           3126 	.area _INITIALIZER
   6D96                    3127 __xinit__prev_player_x:
   6D96 04                 3128 	.db #0x04	; 4
   6D97                    3129 __xinit__prev_player_y:
   6D97 68                 3130 	.db #0x68	; 104	'h'
                           3131 	.area _CABS (ABS)
