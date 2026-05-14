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
                             35 	.globl _cpct_setVideoMode
                             36 	.globl _cpct_drawSolidBox
                             37 	.globl _cpct_memset
                             38 	.globl _cpct_disableFirmware
                             39 	.globl _game_init
                             40 	.globl _game_update
                             41 	.globl _game_render
                             42 ;--------------------------------------------------------
                             43 ; special function registers
                             44 ;--------------------------------------------------------
                             45 ;--------------------------------------------------------
                             46 ; ram data
                             47 ;--------------------------------------------------------
                             48 	.area _DATA
   5CD3                      49 _g_player:
   5CD3                      50 	.ds 9
   5CDC                      51 _g_enemies:
   5CDC                      52 	.ds 60
   5D18                      53 _g_projectiles:
   5D18                      54 	.ds 60
   5D54                      55 _g_lives:
   5D54                      56 	.ds 1
   5D55                      57 _g_score:
   5D55                      58 	.ds 2
   5D57                      59 _g_timeleft:
   5D57                      60 	.ds 1
   5D58                      61 _g_weapondisplay:
   5D58                      62 	.ds 1
   5D59                      63 _g_currentwave:
   5D59                      64 	.ds 1
   5D5A                      65 _g_aliveenemies:
   5D5A                      66 	.ds 1
   5D5B                      67 _g_wavecooldown:
   5D5B                      68 	.ds 1
   5D5C                      69 _g_damagecooldown:
   5D5C                      70 	.ds 1
   5D5D                      71 _g_shootcooldown:
   5D5D                      72 	.ds 1
   5D5E                      73 _g_victory:
   5D5E                      74 	.ds 1
   5D5F                      75 _g_gameover:
   5D5F                      76 	.ds 1
   5D60                      77 _g_framecounter:
   5D60                      78 	.ds 2
   5D62                      79 _g_checkpointx:
   5D62                      80 	.ds 1
   5D63                      81 _g_checkpointy:
   5D63                      82 	.ds 1
   5D64                      83 _g_checkpointactive:
   5D64                      84 	.ds 1
   5D65                      85 _g_boss:
   5D65                      86 	.ds 10
   5D6F                      87 _g_bossactive:
   5D6F                      88 	.ds 1
   5D70                      89 _g_bossphase:
   5D70                      90 	.ds 1
                             91 ;--------------------------------------------------------
                             92 ; ram data
                             93 ;--------------------------------------------------------
                             94 	.area _INITIALIZED
                             95 ;--------------------------------------------------------
                             96 ; absolute external ram data
                             97 ;--------------------------------------------------------
                             98 	.area _DABS (ABS)
                             99 ;--------------------------------------------------------
                            100 ; global & static initialisations
                            101 ;--------------------------------------------------------
                            102 	.area _HOME
                            103 	.area _GSINIT
                            104 	.area _GSFINAL
                            105 	.area _GSINIT
                            106 ;--------------------------------------------------------
                            107 ; Home
                            108 ;--------------------------------------------------------
                            109 	.area _HOME
                            110 	.area _HOME
                            111 ;--------------------------------------------------------
                            112 ; code
                            113 ;--------------------------------------------------------
                            114 	.area _CODE
                            115 ;src/game.c:38: static void reset_player_to_checkpoint(void) {
                            116 ;	---------------------------------
                            117 ; Function reset_player_to_checkpoint
                            118 ; ---------------------------------
   4000                     119 _reset_player_to_checkpoint:
                            120 ;src/game.c:39: g_player.x = g_checkpointx;
   4000 21 D3 5C      [10]  121 	ld	hl, #_g_player
   4003 3A 62 5D      [13]  122 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  123 	ld	(hl), a
                            124 ;src/game.c:40: g_player.y = g_checkpointy;
   4007 21 D4 5C      [10]  125 	ld	hl, #(_g_player + 0x0001)
   400A 3A 63 5D      [13]  126 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  127 	ld	(hl), a
                            128 ;src/game.c:41: g_player.vx = 0;
   400E 21 D5 5C      [10]  129 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  130 	ld	(hl), #0x00
                            131 ;src/game.c:42: g_player.vy = 0;
   4013 21 D6 5C      [10]  132 	ld	hl, #(_g_player + 0x0003)
   4016 36 00         [10]  133 	ld	(hl), #0x00
   4018 C9            [10]  134 	ret
                            135 ;src/game.c:45: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
                            136 ;	---------------------------------
                            137 ; Function rect_overlap
                            138 ; ---------------------------------
   4019                     139 _rect_overlap:
   4019 DD E5         [15]  140 	push	ix
   401B DD 21 00 00   [14]  141 	ld	ix,#0
   401F DD 39         [15]  142 	add	ix,sp
                            143 ;src/game.c:46: if (ax + aw <= bx) return 0;
   4021 DD 4E 08      [19]  144 	ld	c, 8 (ix)
   4024 06 00         [ 7]  145 	ld	b, #0x00
   4026 DD 6E 04      [19]  146 	ld	l,4 (ix)
   4029 DD 66 05      [19]  147 	ld	h,5 (ix)
   402C 09            [11]  148 	add	hl, bc
   402D DD 7E 0A      [19]  149 	ld	a, 10 (ix)
   4030 95            [ 4]  150 	sub	a, l
   4031 DD 7E 0B      [19]  151 	ld	a, 11 (ix)
   4034 9C            [ 4]  152 	sbc	a, h
   4035 E2 3A 40      [10]  153 	jp	PO, 00127$
   4038 EE 80         [ 7]  154 	xor	a, #0x80
   403A                     155 00127$:
   403A FA 41 40      [10]  156 	jp	M, 00102$
   403D 2E 00         [ 7]  157 	ld	l, #0x00
   403F 18 62         [12]  158 	jr	00109$
   4041                     159 00102$:
                            160 ;src/game.c:47: if (bx + bw <= ax) return 0;
   4041 DD 4E 0E      [19]  161 	ld	c, 14 (ix)
   4044 06 00         [ 7]  162 	ld	b, #0x00
   4046 DD 6E 0A      [19]  163 	ld	l,10 (ix)
   4049 DD 66 0B      [19]  164 	ld	h,11 (ix)
   404C 09            [11]  165 	add	hl, bc
   404D DD 7E 04      [19]  166 	ld	a, 4 (ix)
   4050 95            [ 4]  167 	sub	a, l
   4051 DD 7E 05      [19]  168 	ld	a, 5 (ix)
   4054 9C            [ 4]  169 	sbc	a, h
   4055 E2 5A 40      [10]  170 	jp	PO, 00128$
   4058 EE 80         [ 7]  171 	xor	a, #0x80
   405A                     172 00128$:
   405A FA 61 40      [10]  173 	jp	M, 00104$
   405D 2E 00         [ 7]  174 	ld	l, #0x00
   405F 18 42         [12]  175 	jr	00109$
   4061                     176 00104$:
                            177 ;src/game.c:48: if (ay + ah <= by) return 0;
   4061 DD 4E 09      [19]  178 	ld	c, 9 (ix)
   4064 06 00         [ 7]  179 	ld	b, #0x00
   4066 DD 6E 06      [19]  180 	ld	l,6 (ix)
   4069 DD 66 07      [19]  181 	ld	h,7 (ix)
   406C 09            [11]  182 	add	hl, bc
   406D DD 7E 0C      [19]  183 	ld	a, 12 (ix)
   4070 95            [ 4]  184 	sub	a, l
   4071 DD 7E 0D      [19]  185 	ld	a, 13 (ix)
   4074 9C            [ 4]  186 	sbc	a, h
   4075 E2 7A 40      [10]  187 	jp	PO, 00129$
   4078 EE 80         [ 7]  188 	xor	a, #0x80
   407A                     189 00129$:
   407A FA 81 40      [10]  190 	jp	M, 00106$
   407D 2E 00         [ 7]  191 	ld	l, #0x00
   407F 18 22         [12]  192 	jr	00109$
   4081                     193 00106$:
                            194 ;src/game.c:49: if (by + bh <= ay) return 0;
   4081 DD 4E 0F      [19]  195 	ld	c, 15 (ix)
   4084 06 00         [ 7]  196 	ld	b, #0x00
   4086 DD 6E 0C      [19]  197 	ld	l,12 (ix)
   4089 DD 66 0D      [19]  198 	ld	h,13 (ix)
   408C 09            [11]  199 	add	hl, bc
   408D DD 7E 06      [19]  200 	ld	a, 6 (ix)
   4090 95            [ 4]  201 	sub	a, l
   4091 DD 7E 07      [19]  202 	ld	a, 7 (ix)
   4094 9C            [ 4]  203 	sbc	a, h
   4095 E2 9A 40      [10]  204 	jp	PO, 00130$
   4098 EE 80         [ 7]  205 	xor	a, #0x80
   409A                     206 00130$:
   409A FA A1 40      [10]  207 	jp	M, 00108$
   409D 2E 00         [ 7]  208 	ld	l, #0x00
   409F 18 02         [12]  209 	jr	00109$
   40A1                     210 00108$:
                            211 ;src/game.c:50: return 1;
   40A1 2E 01         [ 7]  212 	ld	l, #0x01
   40A3                     213 00109$:
   40A3 DD E1         [14]  214 	pop	ix
   40A5 C9            [10]  215 	ret
                            216 ;src/game.c:53: static void spawn_wave(u8 wave) {
                            217 ;	---------------------------------
                            218 ; Function spawn_wave
                            219 ; ---------------------------------
   40A6                     220 _spawn_wave:
   40A6 DD E5         [15]  221 	push	ix
   40A8 DD 21 00 00   [14]  222 	ld	ix,#0
   40AC DD 39         [15]  223 	add	ix,sp
   40AE F5            [11]  224 	push	af
   40AF F5            [11]  225 	push	af
   40B0 3B            [ 6]  226 	dec	sp
                            227 ;src/game.c:57: for (i = 0; i < MAX_ENEMIES; ++i) {
   40B1 01 DC 5C      [10]  228 	ld	bc, #_g_enemies+0
   40B4 1E 00         [ 7]  229 	ld	e, #0x00
   40B6                     230 00117$:
                            231 ;src/game.c:58: enemyinit(&g_enemies[i]);
   40B6 D5            [11]  232 	push	de
   40B7 16 00         [ 7]  233 	ld	d,#0x00
   40B9 6B            [ 4]  234 	ld	l, e
   40BA 62            [ 4]  235 	ld	h, d
   40BB 29            [11]  236 	add	hl, hl
   40BC 29            [11]  237 	add	hl, hl
   40BD 19            [11]  238 	add	hl, de
   40BE 29            [11]  239 	add	hl, hl
   40BF D1            [10]  240 	pop	de
   40C0 09            [11]  241 	add	hl, bc
   40C1 C5            [11]  242 	push	bc
   40C2 D5            [11]  243 	push	de
   40C3 E5            [11]  244 	push	hl
   40C4 CD 2A 50      [17]  245 	call	_enemyinit
   40C7 F1            [10]  246 	pop	af
   40C8 D1            [10]  247 	pop	de
   40C9 C1            [10]  248 	pop	bc
                            249 ;src/game.c:57: for (i = 0; i < MAX_ENEMIES; ++i) {
   40CA 1C            [ 4]  250 	inc	e
   40CB 7B            [ 4]  251 	ld	a, e
   40CC D6 06         [ 7]  252 	sub	a, #0x06
   40CE 38 E6         [12]  253 	jr	C,00117$
                            254 ;src/game.c:62: else if (wave == 1) count = 3;
   40D0 DD 7E 04      [19]  255 	ld	a, 4 (ix)
   40D3 3D            [ 4]  256 	dec	a
   40D4 20 04         [12]  257 	jr	NZ,00190$
   40D6 3E 01         [ 7]  258 	ld	a,#0x01
   40D8 18 01         [12]  259 	jr	00191$
   40DA                     260 00190$:
   40DA AF            [ 4]  261 	xor	a,a
   40DB                     262 00191$:
   40DB 5F            [ 4]  263 	ld	e, a
                            264 ;src/game.c:61: if (wave == 0) count = 2;
   40DC DD 7E 04      [19]  265 	ld	a, 4 (ix)
   40DF B7            [ 4]  266 	or	a, a
   40E0 20 06         [12]  267 	jr	NZ,00106$
   40E2 DD 36 FB 02   [19]  268 	ld	-5 (ix), #0x02
   40E6 18 0E         [12]  269 	jr	00107$
   40E8                     270 00106$:
                            271 ;src/game.c:62: else if (wave == 1) count = 3;
   40E8 7B            [ 4]  272 	ld	a, e
   40E9 B7            [ 4]  273 	or	a, a
   40EA 28 06         [12]  274 	jr	Z,00103$
   40EC DD 36 FB 03   [19]  275 	ld	-5 (ix), #0x03
   40F0 18 04         [12]  276 	jr	00107$
   40F2                     277 00103$:
                            278 ;src/game.c:63: else count = 4;
   40F2 DD 36 FB 04   [19]  279 	ld	-5 (ix), #0x04
   40F6                     280 00107$:
                            281 ;src/game.c:65: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F6 3E 06         [ 7]  282 	ld	a, #0x06
   40F8 DD 96 FB      [19]  283 	sub	a, -5 (ix)
   40FB 30 04         [12]  284 	jr	NC,00148$
   40FD DD 36 FB 06   [19]  285 	ld	-5 (ix), #0x06
                            286 ;src/game.c:67: for (i = 0; i < count; ++i) {
   4101                     287 00148$:
   4101 DD 73 FF      [19]  288 	ld	-1 (ix), e
   4104 DD 36 FC 00   [19]  289 	ld	-4 (ix), #0x00
   4108                     290 00120$:
   4108 DD 7E FC      [19]  291 	ld	a, -4 (ix)
   410B DD 96 FB      [19]  292 	sub	a, -5 (ix)
   410E D2 9B 41      [10]  293 	jp	NC, 00116$
                            294 ;src/game.c:70: if (wave == 0) type = 0;
   4111 DD 7E 04      [19]  295 	ld	a, 4 (ix)
   4114 B7            [ 4]  296 	or	a,a
   4115 20 03         [12]  297 	jr	NZ,00114$
   4117 5F            [ 4]  298 	ld	e,a
   4118 18 27         [12]  299 	jr	00115$
   411A                     300 00114$:
                            301 ;src/game.c:71: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
   411A DD 7E FF      [19]  302 	ld	a, -1 (ix)
   411D B7            [ 4]  303 	or	a, a
   411E 28 0E         [12]  304 	jr	Z,00111$
   4120 DD 7E FC      [19]  305 	ld	a, -4 (ix)
   4123 B7            [ 4]  306 	or	a, a
   4124 20 04         [12]  307 	jr	NZ,00124$
   4126 1E 01         [ 7]  308 	ld	e, #0x01
   4128 18 17         [12]  309 	jr	00115$
   412A                     310 00124$:
   412A 1E 00         [ 7]  311 	ld	e, #0x00
   412C 18 13         [12]  312 	jr	00115$
   412E                     313 00111$:
                            314 ;src/game.c:72: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   412E DD 7E FC      [19]  315 	ld	a, -4 (ix)
   4131 B7            [ 4]  316 	or	a, a
   4132 28 07         [12]  317 	jr	Z,00129$
   4134 DD 7E FC      [19]  318 	ld	a, -4 (ix)
   4137 D6 03         [ 7]  319 	sub	a, #0x03
   4139 20 04         [12]  320 	jr	NZ,00126$
   413B                     321 00129$:
   413B 1E 02         [ 7]  322 	ld	e, #0x02
   413D 18 02         [12]  323 	jr	00127$
   413F                     324 00126$:
   413F 1E 01         [ 7]  325 	ld	e, #0x01
   4141                     326 00127$:
   4141                     327 00115$:
                            328 ;src/game.c:74: spawn_y = (type == 2) ? 84 : 112;
   4141 7B            [ 4]  329 	ld	a, e
   4142 D6 02         [ 7]  330 	sub	a, #0x02
   4144 20 04         [12]  331 	jr	NZ,00131$
   4146 16 54         [ 7]  332 	ld	d, #0x54
   4148 18 02         [12]  333 	jr	00132$
   414A                     334 00131$:
   414A 16 70         [ 7]  335 	ld	d, #0x70
   414C                     336 00132$:
                            337 ;src/game.c:75: enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));
   414C DD CB FC 46   [20]  338 	bit	0, -4 (ix)
   4150 28 06         [12]  339 	jr	Z,00133$
   4152 DD 36 FE 01   [19]  340 	ld	-2 (ix), #0x01
   4156 18 04         [12]  341 	jr	00134$
   4158                     342 00133$:
   4158 DD 36 FE 00   [19]  343 	ld	-2 (ix), #0x00
   415C                     344 00134$:
   415C DD 7E FC      [19]  345 	ld	a, -4 (ix)
   415F 07            [ 4]  346 	rlca
   4160 07            [ 4]  347 	rlca
   4161 07            [ 4]  348 	rlca
   4162 E6 F8         [ 7]  349 	and	a, #0xf8
   4164 C6 2E         [ 7]  350 	add	a, #0x2e
   4166 DD 77 FD      [19]  351 	ld	-3 (ix), a
   4169 D5            [11]  352 	push	de
   416A DD 5E FC      [19]  353 	ld	e,-4 (ix)
   416D 16 00         [ 7]  354 	ld	d,#0x00
   416F 6B            [ 4]  355 	ld	l, e
   4170 62            [ 4]  356 	ld	h, d
   4171 29            [11]  357 	add	hl, hl
   4172 29            [11]  358 	add	hl, hl
   4173 19            [11]  359 	add	hl, de
   4174 29            [11]  360 	add	hl, hl
   4175 D1            [10]  361 	pop	de
   4176 09            [11]  362 	add	hl, bc
   4177 E5            [11]  363 	push	hl
   4178 FD E1         [14]  364 	pop	iy
   417A C5            [11]  365 	push	bc
   417B DD 7E FE      [19]  366 	ld	a, -2 (ix)
   417E F5            [11]  367 	push	af
   417F 33            [ 6]  368 	inc	sp
   4180 7B            [ 4]  369 	ld	a, e
   4181 F5            [11]  370 	push	af
   4182 33            [ 6]  371 	inc	sp
   4183 D5            [11]  372 	push	de
   4184 33            [ 6]  373 	inc	sp
   4185 DD 7E FD      [19]  374 	ld	a, -3 (ix)
   4188 F5            [11]  375 	push	af
   4189 33            [ 6]  376 	inc	sp
   418A FD E5         [15]  377 	push	iy
   418C CD 6F 50      [17]  378 	call	_enemyspawn
   418F 21 06 00      [10]  379 	ld	hl, #6
   4192 39            [11]  380 	add	hl, sp
   4193 F9            [ 6]  381 	ld	sp, hl
   4194 C1            [10]  382 	pop	bc
                            383 ;src/game.c:67: for (i = 0; i < count; ++i) {
   4195 DD 34 FC      [23]  384 	inc	-4 (ix)
   4198 C3 08 41      [10]  385 	jp	00120$
   419B                     386 00116$:
                            387 ;src/game.c:78: g_aliveenemies = count;
   419B DD 7E FB      [19]  388 	ld	a, -5 (ix)
   419E 32 5A 5D      [13]  389 	ld	(#_g_aliveenemies + 0),a
   41A1 DD F9         [10]  390 	ld	sp, ix
   41A3 DD E1         [14]  391 	pop	ix
   41A5 C9            [10]  392 	ret
                            393 ;src/game.c:81: static void spawn_boss(void) {
                            394 ;	---------------------------------
                            395 ; Function spawn_boss
                            396 ; ---------------------------------
   41A6                     397 _spawn_boss:
                            398 ;src/game.c:82: enemyinit(&g_boss);
   41A6 21 65 5D      [10]  399 	ld	hl, #_g_boss
   41A9 E5            [11]  400 	push	hl
   41AA CD 2A 50      [17]  401 	call	_enemyinit
   41AD F1            [10]  402 	pop	af
                            403 ;src/game.c:83: enemyspawn(&g_boss, 68, 112, 1, 0);
   41AE 21 01 00      [10]  404 	ld	hl, #0x0001
   41B1 E5            [11]  405 	push	hl
   41B2 21 44 70      [10]  406 	ld	hl, #0x7044
   41B5 E5            [11]  407 	push	hl
   41B6 21 65 5D      [10]  408 	ld	hl, #_g_boss
   41B9 E5            [11]  409 	push	hl
   41BA CD 6F 50      [17]  410 	call	_enemyspawn
   41BD 21 06 00      [10]  411 	ld	hl, #6
   41C0 39            [11]  412 	add	hl, sp
   41C1 F9            [ 6]  413 	ld	sp, hl
                            414 ;src/game.c:84: g_boss.w = 10;
   41C2 21 69 5D      [10]  415 	ld	hl, #(_g_boss + 0x0004)
   41C5 36 0A         [10]  416 	ld	(hl), #0x0a
                            417 ;src/game.c:85: g_boss.h = 18;
   41C7 21 6A 5D      [10]  418 	ld	hl, #(_g_boss + 0x0005)
   41CA 36 12         [10]  419 	ld	(hl), #0x12
                            420 ;src/game.c:86: g_boss.health = 10;
   41CC 21 6C 5D      [10]  421 	ld	hl, #(_g_boss + 0x0007)
   41CF 36 0A         [10]  422 	ld	(hl), #0x0a
                            423 ;src/game.c:87: g_boss.reward = 1500;
   41D1 21 6D 5D      [10]  424 	ld	hl, #(_g_boss + 0x0008)
   41D4 36 DC         [10]  425 	ld	(hl), #0xdc
                            426 ;src/game.c:88: g_boss.kind = 3;
   41D6 21 6E 5D      [10]  427 	ld	hl, #(_g_boss + 0x0009)
   41D9 36 03         [10]  428 	ld	(hl), #0x03
                            429 ;src/game.c:89: g_boss.vx = -1;
   41DB 21 67 5D      [10]  430 	ld	hl, #(_g_boss + 0x0002)
   41DE 36 FF         [10]  431 	ld	(hl), #0xff
                            432 ;src/game.c:90: g_bossactive = 1;
   41E0 21 6F 5D      [10]  433 	ld	hl,#_g_bossactive + 0
   41E3 36 01         [10]  434 	ld	(hl), #0x01
                            435 ;src/game.c:91: g_bossphase = 0;
   41E5 21 70 5D      [10]  436 	ld	hl,#_g_bossphase + 0
   41E8 36 00         [10]  437 	ld	(hl), #0x00
   41EA C9            [10]  438 	ret
                            439 ;src/game.c:94: static void try_fire_projectile(void) {
                            440 ;	---------------------------------
                            441 ; Function try_fire_projectile
                            442 ; ---------------------------------
   41EB                     443 _try_fire_projectile:
   41EB DD E5         [15]  444 	push	ix
   41ED DD 21 00 00   [14]  445 	ld	ix,#0
   41F1 DD 39         [15]  446 	add	ix,sp
   41F3 21 FA FF      [10]  447 	ld	hl, #-6
   41F6 39            [11]  448 	add	hl, sp
   41F7 F9            [ 6]  449 	ld	sp, hl
                            450 ;src/game.c:98: if (!input_is_shoot_just_pressed()) return;
   41F8 CD 88 4E      [17]  451 	call	_input_is_shoot_just_pressed
   41FB DD 75 FF      [19]  452 	ld	-1 (ix), l
   41FE 7D            [ 4]  453 	ld	a, l
   41FF B7            [ 4]  454 	or	a, a
   4200 CA 7F 42      [10]  455 	jp	Z,00110$
                            456 ;src/game.c:99: if (g_shootcooldown) return;
   4203 3A 5D 5D      [13]  457 	ld	a,(#_g_shootcooldown + 0)
   4206 B7            [ 4]  458 	or	a, a
   4207 20 76         [12]  459 	jr	NZ,00110$
                            460 ;src/game.c:101: dir = g_player.facing_left ? -3 : 3;
   4209 3A DA 5C      [13]  461 	ld	a, (#_g_player + 7)
   420C B7            [ 4]  462 	or	a, a
   420D 28 04         [12]  463 	jr	Z,00112$
   420F 0E FD         [ 7]  464 	ld	c, #0xfd
   4211 18 02         [12]  465 	jr	00113$
   4213                     466 00112$:
   4213 0E 03         [ 7]  467 	ld	c, #0x03
   4215                     468 00113$:
   4215 DD 71 FA      [19]  469 	ld	-6 (ix), c
                            470 ;src/game.c:103: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4218 DD 36 FB 00   [19]  471 	ld	-5 (ix), #0x00
   421C                     472 00108$:
                            473 ;src/game.c:104: if (!g_projectiles[i].active) {
   421C DD 4E FB      [19]  474 	ld	c,-5 (ix)
   421F 06 00         [ 7]  475 	ld	b,#0x00
   4221 69            [ 4]  476 	ld	l, c
   4222 60            [ 4]  477 	ld	h, b
   4223 29            [11]  478 	add	hl, hl
   4224 29            [11]  479 	add	hl, hl
   4225 09            [11]  480 	add	hl, bc
   4226 29            [11]  481 	add	hl, hl
   4227 01 18 5D      [10]  482 	ld	bc,#_g_projectiles
   422A 09            [11]  483 	add	hl,bc
   422B DD 75 FD      [19]  484 	ld	-3 (ix), l
   422E DD 74 FE      [19]  485 	ld	-2 (ix), h
   4231 11 06 00      [10]  486 	ld	de, #0x0006
   4234 19            [11]  487 	add	hl, de
   4235 7E            [ 7]  488 	ld	a, (hl)
   4236 B7            [ 4]  489 	or	a, a
   4237 20 3C         [12]  490 	jr	NZ,00109$
                            491 ;src/game.c:105: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, 0);
   4239 3A D4 5C      [13]  492 	ld	a,(#_g_player + 1)
   423C DD 77 FF      [19]  493 	ld	-1 (ix), a
   423F C6 06         [ 7]  494 	add	a, #0x06
   4241 DD 77 FF      [19]  495 	ld	-1 (ix), a
   4244 3A D3 5C      [13]  496 	ld	a,(#_g_player + 0)
   4247 DD 77 FC      [19]  497 	ld	-4 (ix), a
   424A DD 34 FC      [23]  498 	inc	-4 (ix)
   424D DD 34 FC      [23]  499 	inc	-4 (ix)
   4250 AF            [ 4]  500 	xor	a, a
   4251 F5            [11]  501 	push	af
   4252 33            [ 6]  502 	inc	sp
   4253 DD 66 FA      [19]  503 	ld	h, -6 (ix)
   4256 DD 6E FF      [19]  504 	ld	l, -1 (ix)
   4259 E5            [11]  505 	push	hl
   425A DD 7E FC      [19]  506 	ld	a, -4 (ix)
   425D F5            [11]  507 	push	af
   425E 33            [ 6]  508 	inc	sp
   425F DD 6E FD      [19]  509 	ld	l,-3 (ix)
   4262 DD 66 FE      [19]  510 	ld	h,-2 (ix)
   4265 E5            [11]  511 	push	hl
   4266 CD BB 58      [17]  512 	call	_projectilefire
   4269 21 06 00      [10]  513 	ld	hl, #6
   426C 39            [11]  514 	add	hl, sp
   426D F9            [ 6]  515 	ld	sp, hl
                            516 ;src/game.c:106: g_shootcooldown = 8;
   426E 21 5D 5D      [10]  517 	ld	hl,#_g_shootcooldown + 0
   4271 36 08         [10]  518 	ld	(hl), #0x08
                            519 ;src/game.c:107: break;
   4273 18 0A         [12]  520 	jr	00110$
   4275                     521 00109$:
                            522 ;src/game.c:103: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4275 DD 34 FB      [23]  523 	inc	-5 (ix)
   4278 DD 7E FB      [19]  524 	ld	a, -5 (ix)
   427B D6 06         [ 7]  525 	sub	a, #0x06
   427D 38 9D         [12]  526 	jr	C,00108$
   427F                     527 00110$:
   427F DD F9         [10]  528 	ld	sp, ix
   4281 DD E1         [14]  529 	pop	ix
   4283 C9            [10]  530 	ret
                            531 ;src/game.c:112: static void register_player_hit(void) {
                            532 ;	---------------------------------
                            533 ; Function register_player_hit
                            534 ; ---------------------------------
   4284                     535 _register_player_hit:
                            536 ;src/game.c:113: if (g_lives) {
   4284 FD 21 54 5D   [14]  537 	ld	iy, #_g_lives
   4288 FD 7E 00      [19]  538 	ld	a, 0 (iy)
   428B B7            [ 4]  539 	or	a, a
   428C 28 03         [12]  540 	jr	Z,00102$
                            541 ;src/game.c:114: g_lives--;
   428E FD 35 00      [23]  542 	dec	0 (iy)
   4291                     543 00102$:
                            544 ;src/game.c:116: if (g_lives == 0) {
   4291 3A 54 5D      [13]  545 	ld	a,(#_g_lives + 0)
   4294 B7            [ 4]  546 	or	a, a
   4295 20 06         [12]  547 	jr	NZ,00104$
                            548 ;src/game.c:117: g_gameover = 1;
   4297 21 5F 5D      [10]  549 	ld	hl,#_g_gameover + 0
   429A 36 01         [10]  550 	ld	(hl), #0x01
                            551 ;src/game.c:118: return;
   429C C9            [10]  552 	ret
   429D                     553 00104$:
                            554 ;src/game.c:121: reset_player_to_checkpoint();
   429D CD 00 40      [17]  555 	call	_reset_player_to_checkpoint
                            556 ;src/game.c:122: g_damagecooldown = 40;
   42A0 21 5C 5D      [10]  557 	ld	hl,#_g_damagecooldown + 0
   42A3 36 28         [10]  558 	ld	(hl), #0x28
   42A5 C9            [10]  559 	ret
                            560 ;src/game.c:125: void game_init(void) {
                            561 ;	---------------------------------
                            562 ; Function game_init
                            563 ; ---------------------------------
   42A6                     564 _game_init::
                            565 ;src/game.c:128: cpct_disableFirmware();
   42A6 CD EA 5B      [17]  566 	call	_cpct_disableFirmware
                            567 ;src/game.c:129: cpct_setVideoMode(1);
   42A9 2E 01         [ 7]  568 	ld	l, #0x01
   42AB CD CE 5B      [17]  569 	call	_cpct_setVideoMode
                            570 ;src/game.c:130: cpct_clearScreen(0x00);
   42AE 21 00 40      [10]  571 	ld	hl, #0x4000
   42B1 E5            [11]  572 	push	hl
   42B2 AF            [ 4]  573 	xor	a, a
   42B3 F5            [11]  574 	push	af
   42B4 33            [ 6]  575 	inc	sp
   42B5 26 C0         [ 7]  576 	ld	h, #0xc0
   42B7 E5            [11]  577 	push	hl
   42B8 CD DC 5B      [17]  578 	call	_cpct_memset
                            579 ;src/game.c:131: tilemap_init();
   42BB CD 9A 4E      [17]  580 	call	_tilemap_init
                            581 ;src/game.c:132: collision_init();
   42BE CD DC 49      [17]  582 	call	_collision_init
                            583 ;src/game.c:133: playerinit(&g_player);
   42C1 21 D3 5C      [10]  584 	ld	hl, #_g_player
   42C4 E5            [11]  585 	push	hl
   42C5 CD 80 54      [17]  586 	call	_playerinit
   42C8 F1            [10]  587 	pop	af
                            588 ;src/game.c:134: hudinit();
   42C9 CD E2 4C      [17]  589 	call	_hudinit
                            590 ;src/game.c:136: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42CC 0E 00         [ 7]  591 	ld	c, #0x00
   42CE                     592 00102$:
                            593 ;src/game.c:137: projectileinit(&g_projectiles[i]);
   42CE 06 00         [ 7]  594 	ld	b,#0x00
   42D0 69            [ 4]  595 	ld	l, c
   42D1 60            [ 4]  596 	ld	h, b
   42D2 29            [11]  597 	add	hl, hl
   42D3 29            [11]  598 	add	hl, hl
   42D4 09            [11]  599 	add	hl, bc
   42D5 29            [11]  600 	add	hl, hl
   42D6 11 18 5D      [10]  601 	ld	de, #_g_projectiles
   42D9 19            [11]  602 	add	hl, de
   42DA C5            [11]  603 	push	bc
   42DB E5            [11]  604 	push	hl
   42DC CD 76 58      [17]  605 	call	_projectileinit
   42DF F1            [10]  606 	pop	af
   42E0 C1            [10]  607 	pop	bc
                            608 ;src/game.c:136: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42E1 0C            [ 4]  609 	inc	c
   42E2 79            [ 4]  610 	ld	a, c
   42E3 D6 06         [ 7]  611 	sub	a, #0x06
   42E5 38 E7         [12]  612 	jr	C,00102$
                            613 ;src/game.c:140: g_lives = 3;
   42E7 21 54 5D      [10]  614 	ld	hl,#_g_lives + 0
   42EA 36 03         [10]  615 	ld	(hl), #0x03
                            616 ;src/game.c:141: g_score = 0;
   42EC 21 00 00      [10]  617 	ld	hl, #0x0000
   42EF 22 55 5D      [16]  618 	ld	(_g_score), hl
                            619 ;src/game.c:142: g_timeleft = 99;
   42F2 FD 21 57 5D   [14]  620 	ld	iy, #_g_timeleft
   42F6 FD 36 00 63   [19]  621 	ld	0 (iy), #0x63
                            622 ;src/game.c:143: g_weapondisplay = 1;
   42FA FD 21 58 5D   [14]  623 	ld	iy, #_g_weapondisplay
   42FE FD 36 00 01   [19]  624 	ld	0 (iy), #0x01
                            625 ;src/game.c:144: g_currentwave = 0;
   4302 FD 21 59 5D   [14]  626 	ld	iy, #_g_currentwave
   4306 FD 36 00 00   [19]  627 	ld	0 (iy), #0x00
                            628 ;src/game.c:145: g_wavecooldown = 1;
   430A FD 21 5B 5D   [14]  629 	ld	iy, #_g_wavecooldown
   430E FD 36 00 01   [19]  630 	ld	0 (iy), #0x01
                            631 ;src/game.c:146: g_damagecooldown = 0;
   4312 FD 21 5C 5D   [14]  632 	ld	iy, #_g_damagecooldown
   4316 FD 36 00 00   [19]  633 	ld	0 (iy), #0x00
                            634 ;src/game.c:147: g_shootcooldown = 0;
   431A FD 21 5D 5D   [14]  635 	ld	iy, #_g_shootcooldown
   431E FD 36 00 00   [19]  636 	ld	0 (iy), #0x00
                            637 ;src/game.c:148: g_victory = 0;
   4322 FD 21 5E 5D   [14]  638 	ld	iy, #_g_victory
   4326 FD 36 00 00   [19]  639 	ld	0 (iy), #0x00
                            640 ;src/game.c:149: g_gameover = 0;
   432A FD 21 5F 5D   [14]  641 	ld	iy, #_g_gameover
   432E FD 36 00 00   [19]  642 	ld	0 (iy), #0x00
                            643 ;src/game.c:150: g_framecounter = 0;
   4332 2E 00         [ 7]  644 	ld	l, #0x00
   4334 22 60 5D      [16]  645 	ld	(_g_framecounter), hl
                            646 ;src/game.c:151: g_checkpointx = 20;
   4337 21 62 5D      [10]  647 	ld	hl,#_g_checkpointx + 0
   433A 36 14         [10]  648 	ld	(hl), #0x14
                            649 ;src/game.c:152: g_checkpointy = 120;
   433C 21 63 5D      [10]  650 	ld	hl,#_g_checkpointy + 0
   433F 36 78         [10]  651 	ld	(hl), #0x78
                            652 ;src/game.c:153: g_checkpointactive = 0;
   4341 21 64 5D      [10]  653 	ld	hl,#_g_checkpointactive + 0
   4344 36 00         [10]  654 	ld	(hl), #0x00
                            655 ;src/game.c:154: g_bossactive = 0;
   4346 21 6F 5D      [10]  656 	ld	hl,#_g_bossactive + 0
   4349 36 00         [10]  657 	ld	(hl), #0x00
                            658 ;src/game.c:155: enemyinit(&g_boss);
   434B 21 65 5D      [10]  659 	ld	hl, #_g_boss
   434E E5            [11]  660 	push	hl
   434F CD 2A 50      [17]  661 	call	_enemyinit
   4352 F1            [10]  662 	pop	af
   4353 C9            [10]  663 	ret
                            664 ;src/game.c:158: void game_update(void) {
                            665 ;	---------------------------------
                            666 ; Function game_update
                            667 ; ---------------------------------
   4354                     668 _game_update::
   4354 DD E5         [15]  669 	push	ix
   4356 DD 21 00 00   [14]  670 	ld	ix,#0
   435A DD 39         [15]  671 	add	ix,sp
   435C 21 E7 FF      [10]  672 	ld	hl, #-25
   435F 39            [11]  673 	add	hl, sp
   4360 F9            [ 6]  674 	ld	sp, hl
                            675 ;src/game.c:162: input_update();
   4361 CD F5 4D      [17]  676 	call	_input_update
                            677 ;src/game.c:164: if (g_gameover || g_victory) {
   4364 3A 5F 5D      [13]  678 	ld	a,(#_g_gameover + 0)
   4367 B7            [ 4]  679 	or	a, a
   4368 C2 C2 48      [10]  680 	jp	NZ,00178$
   436B 3A 5E 5D      [13]  681 	ld	a,(#_g_victory + 0)
   436E B7            [ 4]  682 	or	a, a
                            683 ;src/game.c:165: return;
   436F C2 C2 48      [10]  684 	jp	NZ,00178$
                            685 ;src/game.c:168: playerupdate(&g_player);
   4372 21 D3 5C      [10]  686 	ld	hl, #_g_player
   4375 E5            [11]  687 	push	hl
   4376 CD C7 54      [17]  688 	call	_playerupdate
   4379 F1            [10]  689 	pop	af
                            690 ;src/game.c:169: try_fire_projectile();
   437A CD EB 41      [17]  691 	call	_try_fire_projectile
                            692 ;src/game.c:171: if (g_shootcooldown) g_shootcooldown--;
   437D FD 21 5D 5D   [14]  693 	ld	iy, #_g_shootcooldown
   4381 FD 7E 00      [19]  694 	ld	a, 0 (iy)
   4384 B7            [ 4]  695 	or	a, a
   4385 28 03         [12]  696 	jr	Z,00105$
   4387 FD 35 00      [23]  697 	dec	0 (iy)
   438A                     698 00105$:
                            699 ;src/game.c:172: if (g_damagecooldown) g_damagecooldown--;
   438A FD 21 5C 5D   [14]  700 	ld	iy, #_g_damagecooldown
   438E FD 7E 00      [19]  701 	ld	a, 0 (iy)
   4391 B7            [ 4]  702 	or	a, a
   4392 28 03         [12]  703 	jr	Z,00189$
   4394 FD 35 00      [23]  704 	dec	0 (iy)
                            705 ;src/game.c:174: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4397                     706 00189$:
   4397 0E 00         [ 7]  707 	ld	c, #0x00
   4399                     708 00171$:
                            709 ;src/game.c:175: projectileupdate(&g_projectiles[i]);
   4399 06 00         [ 7]  710 	ld	b,#0x00
   439B 69            [ 4]  711 	ld	l, c
   439C 60            [ 4]  712 	ld	h, b
   439D 29            [11]  713 	add	hl, hl
   439E 29            [11]  714 	add	hl, hl
   439F 09            [11]  715 	add	hl, bc
   43A0 29            [11]  716 	add	hl, hl
   43A1 11 18 5D      [10]  717 	ld	de, #_g_projectiles
   43A4 19            [11]  718 	add	hl, de
   43A5 C5            [11]  719 	push	bc
   43A6 E5            [11]  720 	push	hl
   43A7 CD 79 59      [17]  721 	call	_projectileupdate
   43AA F1            [10]  722 	pop	af
   43AB C1            [10]  723 	pop	bc
                            724 ;src/game.c:174: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43AC 0C            [ 4]  725 	inc	c
   43AD 79            [ 4]  726 	ld	a, c
   43AE D6 06         [ 7]  727 	sub	a, #0x06
   43B0 38 E7         [12]  728 	jr	C,00171$
                            729 ;src/game.c:178: for (i = 0; i < MAX_ENEMIES; ++i) {
   43B2 0E 00         [ 7]  730 	ld	c, #0x00
   43B4                     731 00173$:
                            732 ;src/game.c:179: enemyupdate(&g_enemies[i]);
   43B4 06 00         [ 7]  733 	ld	b,#0x00
   43B6 69            [ 4]  734 	ld	l, c
   43B7 60            [ 4]  735 	ld	h, b
   43B8 29            [11]  736 	add	hl, hl
   43B9 29            [11]  737 	add	hl, hl
   43BA 09            [11]  738 	add	hl, bc
   43BB 29            [11]  739 	add	hl, hl
   43BC 11 DC 5C      [10]  740 	ld	de, #_g_enemies
   43BF 19            [11]  741 	add	hl, de
   43C0 C5            [11]  742 	push	bc
   43C1 E5            [11]  743 	push	hl
   43C2 CD F6 51      [17]  744 	call	_enemyupdate
   43C5 F1            [10]  745 	pop	af
   43C6 C1            [10]  746 	pop	bc
                            747 ;src/game.c:178: for (i = 0; i < MAX_ENEMIES; ++i) {
   43C7 0C            [ 4]  748 	inc	c
   43C8 79            [ 4]  749 	ld	a, c
   43C9 D6 06         [ 7]  750 	sub	a, #0x06
   43CB 38 E7         [12]  751 	jr	C,00173$
                            752 ;src/game.c:182: if (g_bossactive) {
   43CD 3A 6F 5D      [13]  753 	ld	a,(#_g_bossactive + 0)
   43D0 B7            [ 4]  754 	or	a, a
   43D1 28 71         [12]  755 	jr	Z,00208$
                            756 ;src/game.c:183: if (g_boss.health > 4) g_bossphase = 0;
   43D3 21 6C 5D      [10]  757 	ld	hl, #_g_boss + 7
   43D6 4E            [ 7]  758 	ld	c, (hl)
   43D7 3E 04         [ 7]  759 	ld	a, #0x04
   43D9 91            [ 4]  760 	sub	a, c
   43DA 30 07         [12]  761 	jr	NC,00111$
   43DC 21 70 5D      [10]  762 	ld	hl,#_g_bossphase + 0
   43DF 36 00         [10]  763 	ld	(hl), #0x00
   43E1 18 05         [12]  764 	jr	00112$
   43E3                     765 00111$:
                            766 ;src/game.c:184: else g_bossphase = 1;
   43E3 21 70 5D      [10]  767 	ld	hl,#_g_bossphase + 0
   43E6 36 01         [10]  768 	ld	(hl), #0x01
   43E8                     769 00112$:
                            770 ;src/game.c:186: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   43E8 3A D3 5C      [13]  771 	ld	a,(#_g_player + 0)
   43EB DD 77 F7      [19]  772 	ld	-9 (ix), a
   43EE DD 77 E9      [19]  773 	ld	-23 (ix), a
   43F1 DD 36 EA 00   [19]  774 	ld	-22 (ix), #0x00
   43F5 DD 7E E9      [19]  775 	ld	a, -23 (ix)
   43F8 C6 02         [ 7]  776 	add	a, #0x02
   43FA DD 77 E9      [19]  777 	ld	-23 (ix), a
   43FD DD 7E EA      [19]  778 	ld	a, -22 (ix)
   4400 CE 00         [ 7]  779 	adc	a, #0x00
   4402 DD 77 EA      [19]  780 	ld	-22 (ix), a
   4405 21 65 5D      [10]  781 	ld	hl, #_g_boss + 0
   4408 4E            [ 7]  782 	ld	c, (hl)
   4409 06 00         [ 7]  783 	ld	b, #0x00
   440B DD 7E E9      [19]  784 	ld	a, -23 (ix)
   440E 91            [ 4]  785 	sub	a, c
   440F DD 7E EA      [19]  786 	ld	a, -22 (ix)
   4412 98            [ 4]  787 	sbc	a, b
   4413 E2 18 44      [10]  788 	jp	PO, 00369$
   4416 EE 80         [ 7]  789 	xor	a, #0x80
   4418                     790 00369$:
   4418 F2 2C 44      [10]  791 	jp	P, 00180$
   441B 3A 70 5D      [13]  792 	ld	a,(#_g_bossphase + 0)
   441E B7            [ 4]  793 	or	a, a
   441F 28 04         [12]  794 	jr	Z,00182$
   4421 0E 02         [ 7]  795 	ld	c, #0x02
   4423 18 02         [12]  796 	jr	00183$
   4425                     797 00182$:
   4425 0E 01         [ 7]  798 	ld	c, #0x01
   4427                     799 00183$:
   4427 AF            [ 4]  800 	xor	a, a
   4428 91            [ 4]  801 	sub	a, c
   4429 4F            [ 4]  802 	ld	c, a
   442A 18 0C         [12]  803 	jr	00181$
   442C                     804 00180$:
   442C 3A 70 5D      [13]  805 	ld	a,(#_g_bossphase + 0)
   442F B7            [ 4]  806 	or	a, a
   4430 28 04         [12]  807 	jr	Z,00184$
   4432 0E 02         [ 7]  808 	ld	c, #0x02
   4434 18 02         [12]  809 	jr	00185$
   4436                     810 00184$:
   4436 0E 01         [ 7]  811 	ld	c, #0x01
   4438                     812 00185$:
   4438                     813 00181$:
   4438 21 67 5D      [10]  814 	ld	hl, #(_g_boss + 0x0002)
   443B 71            [ 7]  815 	ld	(hl), c
                            816 ;src/game.c:187: enemyupdate(&g_boss);
   443C 21 65 5D      [10]  817 	ld	hl, #_g_boss
   443F E5            [11]  818 	push	hl
   4440 CD F6 51      [17]  819 	call	_enemyupdate
   4443 F1            [10]  820 	pop	af
                            821 ;src/game.c:190: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4444                     822 00208$:
   4444 0E 00         [ 7]  823 	ld	c, #0x00
   4446                     824 00176$:
                            825 ;src/game.c:191: if (!g_projectiles[i].active) continue;
   4446 06 00         [ 7]  826 	ld	b,#0x00
   4448 69            [ 4]  827 	ld	l, c
   4449 60            [ 4]  828 	ld	h, b
   444A 29            [11]  829 	add	hl, hl
   444B 29            [11]  830 	add	hl, hl
   444C 09            [11]  831 	add	hl, bc
   444D 29            [11]  832 	add	hl, hl
   444E EB            [ 4]  833 	ex	de,hl
   444F 21 18 5D      [10]  834 	ld	hl, #_g_projectiles
   4452 19            [11]  835 	add	hl,de
   4453 EB            [ 4]  836 	ex	de,hl
   4454 21 06 00      [10]  837 	ld	hl, #0x0006
   4457 19            [11]  838 	add	hl,de
   4458 DD 75 E9      [19]  839 	ld	-23 (ix), l
   445B DD 74 EA      [19]  840 	ld	-22 (ix), h
   445E 7E            [ 7]  841 	ld	a, (hl)
   445F B7            [ 4]  842 	or	a, a
   4460 CA 81 46      [10]  843 	jp	Z, 00133$
                            844 ;src/game.c:192: for (j = 0; j < MAX_ENEMIES; ++j) {
   4463 DD 36 E7 00   [19]  845 	ld	-25 (ix), #0x00
   4467                     846 00175$:
                            847 ;src/game.c:193: if (!g_enemies[j].active) continue;
   4467 D5            [11]  848 	push	de
   4468 DD 5E E7      [19]  849 	ld	e,-25 (ix)
   446B 16 00         [ 7]  850 	ld	d,#0x00
   446D 6B            [ 4]  851 	ld	l, e
   446E 62            [ 4]  852 	ld	h, d
   446F 29            [11]  853 	add	hl, hl
   4470 29            [11]  854 	add	hl, hl
   4471 19            [11]  855 	add	hl, de
   4472 29            [11]  856 	add	hl, hl
   4473 D1            [10]  857 	pop	de
   4474 3E DC         [ 7]  858 	ld	a, #<(_g_enemies)
   4476 85            [ 4]  859 	add	a, l
   4477 DD 77 FE      [19]  860 	ld	-2 (ix), a
   447A 3E 5C         [ 7]  861 	ld	a, #>(_g_enemies)
   447C 8C            [ 4]  862 	adc	a, h
   447D DD 77 FF      [19]  863 	ld	-1 (ix), a
   4480 DD 6E FE      [19]  864 	ld	l,-2 (ix)
   4483 DD 66 FF      [19]  865 	ld	h,-1 (ix)
   4486 C5            [11]  866 	push	bc
   4487 01 06 00      [10]  867 	ld	bc, #0x0006
   448A 09            [11]  868 	add	hl, bc
   448B C1            [10]  869 	pop	bc
   448C 46            [ 7]  870 	ld	b, (hl)
                            871 ;src/game.c:194: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   448D 21 05 00      [10]  872 	ld	hl, #0x0005
   4490 19            [11]  873 	add	hl,de
   4491 DD 75 FC      [19]  874 	ld	-4 (ix), l
   4494 DD 74 FD      [19]  875 	ld	-3 (ix), h
   4497 21 04 00      [10]  876 	ld	hl, #0x0004
   449A 19            [11]  877 	add	hl,de
   449B DD 75 F0      [19]  878 	ld	-16 (ix), l
   449E DD 74 F1      [19]  879 	ld	-15 (ix), h
   44A1 21 01 00      [10]  880 	ld	hl, #0x0001
   44A4 19            [11]  881 	add	hl,de
   44A5 DD 75 EE      [19]  882 	ld	-18 (ix), l
   44A8 DD 74 EF      [19]  883 	ld	-17 (ix), h
                            884 ;src/game.c:196: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44AB 21 07 00      [10]  885 	ld	hl, #0x0007
   44AE 19            [11]  886 	add	hl,de
   44AF DD 75 EC      [19]  887 	ld	-20 (ix), l
   44B2 DD 74 ED      [19]  888 	ld	-19 (ix), h
                            889 ;src/game.c:193: if (!g_enemies[j].active) continue;
   44B5 78            [ 4]  890 	ld	a, b
   44B6 B7            [ 4]  891 	or	a, a
   44B7 CA AF 45      [10]  892 	jp	Z, 00125$
                            893 ;src/game.c:195: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   44BA DD 6E FE      [19]  894 	ld	l,-2 (ix)
   44BD DD 66 FF      [19]  895 	ld	h,-1 (ix)
   44C0 23            [ 6]  896 	inc	hl
   44C1 23            [ 6]  897 	inc	hl
   44C2 23            [ 6]  898 	inc	hl
   44C3 23            [ 6]  899 	inc	hl
   44C4 23            [ 6]  900 	inc	hl
   44C5 7E            [ 7]  901 	ld	a, (hl)
   44C6 DD 77 F7      [19]  902 	ld	-9 (ix), a
   44C9 DD 6E FE      [19]  903 	ld	l,-2 (ix)
   44CC DD 66 FF      [19]  904 	ld	h,-1 (ix)
   44CF 23            [ 6]  905 	inc	hl
   44D0 23            [ 6]  906 	inc	hl
   44D1 23            [ 6]  907 	inc	hl
   44D2 23            [ 6]  908 	inc	hl
   44D3 7E            [ 7]  909 	ld	a, (hl)
   44D4 DD 77 EB      [19]  910 	ld	-21 (ix), a
   44D7 DD 6E FE      [19]  911 	ld	l,-2 (ix)
   44DA DD 66 FF      [19]  912 	ld	h,-1 (ix)
   44DD 23            [ 6]  913 	inc	hl
   44DE 46            [ 7]  914 	ld	b, (hl)
   44DF DD 70 FA      [19]  915 	ld	-6 (ix), b
   44E2 DD 36 FB 00   [19]  916 	ld	-5 (ix), #0x00
   44E6 DD 6E FE      [19]  917 	ld	l,-2 (ix)
   44E9 DD 66 FF      [19]  918 	ld	h,-1 (ix)
   44EC 46            [ 7]  919 	ld	b, (hl)
   44ED DD 70 F8      [19]  920 	ld	-8 (ix), b
   44F0 DD 36 F9 00   [19]  921 	ld	-7 (ix), #0x00
                            922 ;src/game.c:194: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   44F4 DD 6E FC      [19]  923 	ld	l,-4 (ix)
   44F7 DD 66 FD      [19]  924 	ld	h,-3 (ix)
   44FA 7E            [ 7]  925 	ld	a, (hl)
   44FB DD 77 F6      [19]  926 	ld	-10 (ix), a
   44FE DD 6E F0      [19]  927 	ld	l,-16 (ix)
   4501 DD 66 F1      [19]  928 	ld	h,-15 (ix)
   4504 46            [ 7]  929 	ld	b, (hl)
   4505 DD 6E EE      [19]  930 	ld	l,-18 (ix)
   4508 DD 66 EF      [19]  931 	ld	h,-17 (ix)
   450B 6E            [ 7]  932 	ld	l, (hl)
   450C DD 75 F4      [19]  933 	ld	-12 (ix), l
   450F DD 36 F5 00   [19]  934 	ld	-11 (ix), #0x00
   4513 1A            [ 7]  935 	ld	a, (de)
   4514 DD 77 F2      [19]  936 	ld	-14 (ix), a
   4517 DD 36 F3 00   [19]  937 	ld	-13 (ix), #0x00
   451B C5            [11]  938 	push	bc
   451C D5            [11]  939 	push	de
   451D DD 66 F7      [19]  940 	ld	h, -9 (ix)
   4520 DD 6E EB      [19]  941 	ld	l, -21 (ix)
   4523 E5            [11]  942 	push	hl
   4524 DD 6E FA      [19]  943 	ld	l,-6 (ix)
   4527 DD 66 FB      [19]  944 	ld	h,-5 (ix)
   452A E5            [11]  945 	push	hl
   452B DD 6E F8      [19]  946 	ld	l,-8 (ix)
   452E DD 66 F9      [19]  947 	ld	h,-7 (ix)
   4531 E5            [11]  948 	push	hl
   4532 DD 7E F6      [19]  949 	ld	a, -10 (ix)
   4535 F5            [11]  950 	push	af
   4536 33            [ 6]  951 	inc	sp
   4537 C5            [11]  952 	push	bc
   4538 33            [ 6]  953 	inc	sp
   4539 DD 6E F4      [19]  954 	ld	l,-12 (ix)
   453C DD 66 F5      [19]  955 	ld	h,-11 (ix)
   453F E5            [11]  956 	push	hl
   4540 DD 6E F2      [19]  957 	ld	l,-14 (ix)
   4543 DD 66 F3      [19]  958 	ld	h,-13 (ix)
   4546 E5            [11]  959 	push	hl
   4547 CD 19 40      [17]  960 	call	_rect_overlap
   454A FD 21 0C 00   [14]  961 	ld	iy, #12
   454E FD 39         [15]  962 	add	iy, sp
   4550 FD F9         [10]  963 	ld	sp, iy
   4552 D1            [10]  964 	pop	de
   4553 C1            [10]  965 	pop	bc
   4554 7D            [ 4]  966 	ld	a, l
   4555 B7            [ 4]  967 	or	a, a
   4556 28 57         [12]  968 	jr	Z,00125$
                            969 ;src/game.c:196: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   4558 DD 6E EC      [19]  970 	ld	l,-20 (ix)
   455B DD 66 ED      [19]  971 	ld	h,-19 (ix)
   455E 66            [ 7]  972 	ld	h, (hl)
   455F DD 6E FE      [19]  973 	ld	l, -2 (ix)
   4562 DD 46 FF      [19]  974 	ld	b, -1 (ix)
   4565 C5            [11]  975 	push	bc
   4566 D5            [11]  976 	push	de
   4567 E5            [11]  977 	push	hl
   4568 33            [ 6]  978 	inc	sp
   4569 60            [ 4]  979 	ld	h, b
   456A E5            [11]  980 	push	hl
   456B CD 40 54      [17]  981 	call	_enemydamage
   456E F1            [10]  982 	pop	af
   456F 33            [ 6]  983 	inc	sp
   4570 D1            [10]  984 	pop	de
   4571 C1            [10]  985 	pop	bc
   4572 7D            [ 4]  986 	ld	a, l
   4573 B7            [ 4]  987 	or	a, a
   4574 28 2F         [12]  988 	jr	Z,00124$
                            989 ;src/game.c:197: g_score = (u16)(g_score + g_enemies[j].reward);
   4576 DD 6E FE      [19]  990 	ld	l,-2 (ix)
   4579 DD 66 FF      [19]  991 	ld	h,-1 (ix)
   457C C5            [11]  992 	push	bc
   457D 01 08 00      [10]  993 	ld	bc, #0x0008
   4580 09            [11]  994 	add	hl, bc
   4581 C1            [10]  995 	pop	bc
   4582 6E            [ 7]  996 	ld	l, (hl)
   4583 DD 75 F2      [19]  997 	ld	-14 (ix), l
   4586 DD 36 F3 00   [19]  998 	ld	-13 (ix), #0x00
   458A 21 55 5D      [10]  999 	ld	hl, #_g_score
   458D 7E            [ 7] 1000 	ld	a, (hl)
   458E DD 86 F2      [19] 1001 	add	a, -14 (ix)
   4591 77            [ 7] 1002 	ld	(hl), a
   4592 23            [ 6] 1003 	inc	hl
   4593 7E            [ 7] 1004 	ld	a, (hl)
   4594 DD 8E F3      [19] 1005 	adc	a, -13 (ix)
   4597 77            [ 7] 1006 	ld	(hl), a
                           1007 ;src/game.c:198: if (g_aliveenemies) g_aliveenemies--;
   4598 FD 21 5A 5D   [14] 1008 	ld	iy, #_g_aliveenemies
   459C FD 7E 00      [19] 1009 	ld	a, 0 (iy)
   459F B7            [ 4] 1010 	or	a, a
   45A0 28 03         [12] 1011 	jr	Z,00124$
   45A2 FD 35 00      [23] 1012 	dec	0 (iy)
   45A5                    1013 00124$:
                           1014 ;src/game.c:200: g_projectiles[i].active = 0;
   45A5 DD 6E E9      [19] 1015 	ld	l,-23 (ix)
   45A8 DD 66 EA      [19] 1016 	ld	h,-22 (ix)
   45AB 36 00         [10] 1017 	ld	(hl), #0x00
                           1018 ;src/game.c:201: break;
   45AD 18 0B         [12] 1019 	jr	00126$
   45AF                    1020 00125$:
                           1021 ;src/game.c:192: for (j = 0; j < MAX_ENEMIES; ++j) {
   45AF DD 34 E7      [23] 1022 	inc	-25 (ix)
   45B2 DD 7E E7      [19] 1023 	ld	a, -25 (ix)
   45B5 D6 06         [ 7] 1024 	sub	a, #0x06
   45B7 DA 67 44      [10] 1025 	jp	C, 00175$
   45BA                    1026 00126$:
                           1027 ;src/game.c:204: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   45BA 3A 6F 5D      [13] 1028 	ld	a,(#_g_bossactive + 0)
   45BD B7            [ 4] 1029 	or	a, a
   45BE CA 81 46      [10] 1030 	jp	Z, 00133$
   45C1 DD 6E E9      [19] 1031 	ld	l,-23 (ix)
   45C4 DD 66 EA      [19] 1032 	ld	h,-22 (ix)
   45C7 7E            [ 7] 1033 	ld	a, (hl)
   45C8 B7            [ 4] 1034 	or	a, a
   45C9 CA 81 46      [10] 1035 	jp	Z, 00133$
                           1036 ;src/game.c:205: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   45CC 21 6A 5D      [10] 1037 	ld	hl, #(_g_boss + 0x0005) + 0
   45CF 46            [ 7] 1038 	ld	b, (hl)
   45D0 3A 69 5D      [13] 1039 	ld	a, (#(_g_boss + 0x0004) + 0)
   45D3 21 66 5D      [10] 1040 	ld	hl, #(_g_boss + 0x0001) + 0
   45D6 6E            [ 7] 1041 	ld	l, (hl)
   45D7 DD 75 F2      [19] 1042 	ld	-14 (ix), l
   45DA DD 36 F3 00   [19] 1043 	ld	-13 (ix), #0x00
   45DE 21 65 5D      [10] 1044 	ld	hl, #_g_boss + 0
   45E1 6E            [ 7] 1045 	ld	l, (hl)
   45E2 DD 75 F4      [19] 1046 	ld	-12 (ix), l
   45E5 DD 36 F5 00   [19] 1047 	ld	-11 (ix), #0x00
                           1048 ;src/game.c:204: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   45E9 DD 6E FC      [19] 1049 	ld	l,-4 (ix)
   45EC DD 66 FD      [19] 1050 	ld	h,-3 (ix)
   45EF F5            [11] 1051 	push	af
   45F0 7E            [ 7] 1052 	ld	a, (hl)
   45F1 DD 77 F6      [19] 1053 	ld	-10 (ix), a
   45F4 F1            [10] 1054 	pop	af
   45F5 DD 6E F0      [19] 1055 	ld	l,-16 (ix)
   45F8 DD 66 F1      [19] 1056 	ld	h,-15 (ix)
   45FB F5            [11] 1057 	push	af
   45FC 7E            [ 7] 1058 	ld	a, (hl)
   45FD DD 77 F8      [19] 1059 	ld	-8 (ix), a
   4600 F1            [10] 1060 	pop	af
   4601 DD 6E EE      [19] 1061 	ld	l,-18 (ix)
   4604 DD 66 EF      [19] 1062 	ld	h,-17 (ix)
   4607 6E            [ 7] 1063 	ld	l, (hl)
   4608 DD 75 FA      [19] 1064 	ld	-6 (ix), l
   460B DD 36 FB 00   [19] 1065 	ld	-5 (ix), #0x00
   460F F5            [11] 1066 	push	af
   4610 1A            [ 7] 1067 	ld	a, (de)
   4611 5F            [ 4] 1068 	ld	e, a
   4612 F1            [10] 1069 	pop	af
   4613 16 00         [ 7] 1070 	ld	d, #0x00
   4615 C5            [11] 1071 	push	bc
   4616 C5            [11] 1072 	push	bc
   4617 33            [ 6] 1073 	inc	sp
   4618 F5            [11] 1074 	push	af
   4619 33            [ 6] 1075 	inc	sp
   461A DD 6E F2      [19] 1076 	ld	l,-14 (ix)
   461D DD 66 F3      [19] 1077 	ld	h,-13 (ix)
   4620 E5            [11] 1078 	push	hl
   4621 DD 6E F4      [19] 1079 	ld	l,-12 (ix)
   4624 DD 66 F5      [19] 1080 	ld	h,-11 (ix)
   4627 E5            [11] 1081 	push	hl
   4628 DD 66 F6      [19] 1082 	ld	h, -10 (ix)
   462B DD 6E F8      [19] 1083 	ld	l, -8 (ix)
   462E E5            [11] 1084 	push	hl
   462F DD 6E FA      [19] 1085 	ld	l,-6 (ix)
   4632 DD 66 FB      [19] 1086 	ld	h,-5 (ix)
   4635 E5            [11] 1087 	push	hl
   4636 D5            [11] 1088 	push	de
   4637 CD 19 40      [17] 1089 	call	_rect_overlap
   463A FD 21 0C 00   [14] 1090 	ld	iy, #12
   463E FD 39         [15] 1091 	add	iy, sp
   4640 FD F9         [10] 1092 	ld	sp, iy
   4642 C1            [10] 1093 	pop	bc
   4643 7D            [ 4] 1094 	ld	a, l
   4644 B7            [ 4] 1095 	or	a, a
   4645 28 3A         [12] 1096 	jr	Z,00133$
                           1097 ;src/game.c:206: g_projectiles[i].active = 0;
   4647 DD 6E E9      [19] 1098 	ld	l,-23 (ix)
   464A DD 66 EA      [19] 1099 	ld	h,-22 (ix)
   464D 36 00         [10] 1100 	ld	(hl), #0x00
                           1101 ;src/game.c:207: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   464F DD 6E EC      [19] 1102 	ld	l,-20 (ix)
   4652 DD 66 ED      [19] 1103 	ld	h,-19 (ix)
   4655 46            [ 7] 1104 	ld	b, (hl)
   4656 11 65 5D      [10] 1105 	ld	de, #_g_boss
   4659 C5            [11] 1106 	push	bc
   465A C5            [11] 1107 	push	bc
   465B 33            [ 6] 1108 	inc	sp
   465C D5            [11] 1109 	push	de
   465D CD 40 54      [17] 1110 	call	_enemydamage
   4660 F1            [10] 1111 	pop	af
   4661 33            [ 6] 1112 	inc	sp
   4662 C1            [10] 1113 	pop	bc
   4663 7D            [ 4] 1114 	ld	a, l
   4664 B7            [ 4] 1115 	or	a, a
   4665 28 1A         [12] 1116 	jr	Z,00133$
                           1117 ;src/game.c:208: g_bossactive = 0;
   4667 21 6F 5D      [10] 1118 	ld	hl,#_g_bossactive + 0
   466A 36 00         [10] 1119 	ld	(hl), #0x00
                           1120 ;src/game.c:209: g_score = (u16)(g_score + g_boss.reward);
   466C 21 6D 5D      [10] 1121 	ld	hl, #_g_boss + 8
   466F 5E            [ 7] 1122 	ld	e, (hl)
   4670 16 00         [ 7] 1123 	ld	d, #0x00
   4672 21 55 5D      [10] 1124 	ld	hl, #_g_score
   4675 7E            [ 7] 1125 	ld	a, (hl)
   4676 83            [ 4] 1126 	add	a, e
   4677 77            [ 7] 1127 	ld	(hl), a
   4678 23            [ 6] 1128 	inc	hl
   4679 7E            [ 7] 1129 	ld	a, (hl)
   467A 8A            [ 4] 1130 	adc	a, d
   467B 77            [ 7] 1131 	ld	(hl), a
                           1132 ;src/game.c:210: g_victory = 1;
   467C 21 5E 5D      [10] 1133 	ld	hl,#_g_victory + 0
   467F 36 01         [10] 1134 	ld	(hl), #0x01
   4681                    1135 00133$:
                           1136 ;src/game.c:190: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4681 0C            [ 4] 1137 	inc	c
   4682 79            [ 4] 1138 	ld	a, c
   4683 D6 06         [ 7] 1139 	sub	a, #0x06
   4685 DA 46 44      [10] 1140 	jp	C, 00176$
                           1141 ;src/game.c:216: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1142 ;src/game.c:215: if (!g_damagecooldown) {
   4688 3A 5C 5D      [13] 1143 	ld	a,(#_g_damagecooldown + 0)
   468B B7            [ 4] 1144 	or	a, a
   468C C2 F6 47      [10] 1145 	jp	NZ, 00149$
                           1146 ;src/game.c:216: for (i = 0; i < MAX_ENEMIES; ++i) {
   468F DD 36 E8 00   [19] 1147 	ld	-24 (ix), #0x00
   4693                    1148 00177$:
                           1149 ;src/game.c:217: if (!g_enemies[i].active) continue;
   4693 DD 4E E8      [19] 1150 	ld	c,-24 (ix)
   4696 06 00         [ 7] 1151 	ld	b,#0x00
   4698 69            [ 4] 1152 	ld	l, c
   4699 60            [ 4] 1153 	ld	h, b
   469A 29            [11] 1154 	add	hl, hl
   469B 29            [11] 1155 	add	hl, hl
   469C 09            [11] 1156 	add	hl, bc
   469D 29            [11] 1157 	add	hl, hl
   469E 4D            [ 4] 1158 	ld	c, l
   469F 44            [ 4] 1159 	ld	b, h
   46A0 21 DC 5C      [10] 1160 	ld	hl, #_g_enemies
   46A3 09            [11] 1161 	add	hl,bc
   46A4 DD 75 F2      [19] 1162 	ld	-14 (ix), l
   46A7 DD 74 F3      [19] 1163 	ld	-13 (ix), h
   46AA 11 06 00      [10] 1164 	ld	de, #0x0006
   46AD 19            [11] 1165 	add	hl, de
   46AE 7E            [ 7] 1166 	ld	a, (hl)
   46AF B7            [ 4] 1167 	or	a, a
   46B0 CA 40 47      [10] 1168 	jp	Z, 00139$
                           1169 ;src/game.c:219: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   46B3 DD 7E F2      [19] 1170 	ld	a, -14 (ix)
   46B6 DD 77 F4      [19] 1171 	ld	-12 (ix), a
   46B9 DD 7E F3      [19] 1172 	ld	a, -13 (ix)
   46BC DD 77 F5      [19] 1173 	ld	-11 (ix), a
   46BF DD 6E F4      [19] 1174 	ld	l,-12 (ix)
   46C2 DD 66 F5      [19] 1175 	ld	h,-11 (ix)
   46C5 11 05 00      [10] 1176 	ld	de, #0x0005
   46C8 19            [11] 1177 	add	hl, de
   46C9 7E            [ 7] 1178 	ld	a, (hl)
   46CA DD 77 F4      [19] 1179 	ld	-12 (ix), a
   46CD DD 6E F2      [19] 1180 	ld	l,-14 (ix)
   46D0 DD 66 F3      [19] 1181 	ld	h,-13 (ix)
   46D3 11 04 00      [10] 1182 	ld	de, #0x0004
   46D6 19            [11] 1183 	add	hl, de
   46D7 7E            [ 7] 1184 	ld	a, (hl)
   46D8 DD 77 F6      [19] 1185 	ld	-10 (ix), a
   46DB DD 6E F2      [19] 1186 	ld	l,-14 (ix)
   46DE DD 66 F3      [19] 1187 	ld	h,-13 (ix)
   46E1 23            [ 6] 1188 	inc	hl
   46E2 4E            [ 7] 1189 	ld	c, (hl)
   46E3 06 00         [ 7] 1190 	ld	b, #0x00
   46E5 DD 6E F2      [19] 1191 	ld	l,-14 (ix)
   46E8 DD 66 F3      [19] 1192 	ld	h,-13 (ix)
   46EB 5E            [ 7] 1193 	ld	e, (hl)
   46EC 16 00         [ 7] 1194 	ld	d, #0x00
                           1195 ;src/game.c:218: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   46EE 3A D8 5C      [13] 1196 	ld	a,(#(_g_player + 0x0005) + 0)
   46F1 DD 77 F2      [19] 1197 	ld	-14 (ix), a
   46F4 3A D7 5C      [13] 1198 	ld	a,(#(_g_player + 0x0004) + 0)
   46F7 DD 77 F8      [19] 1199 	ld	-8 (ix), a
   46FA 3A D4 5C      [13] 1200 	ld	a, (#(_g_player + 0x0001) + 0)
   46FD DD 77 FA      [19] 1201 	ld	-6 (ix), a
   4700 DD 36 FB 00   [19] 1202 	ld	-5 (ix), #0x00
   4704 3A D3 5C      [13] 1203 	ld	a, (#_g_player + 0)
   4707 DD 77 EC      [19] 1204 	ld	-20 (ix), a
   470A DD 36 ED 00   [19] 1205 	ld	-19 (ix), #0x00
   470E DD 66 F4      [19] 1206 	ld	h, -12 (ix)
   4711 DD 6E F6      [19] 1207 	ld	l, -10 (ix)
   4714 E5            [11] 1208 	push	hl
   4715 C5            [11] 1209 	push	bc
   4716 D5            [11] 1210 	push	de
   4717 DD 66 F2      [19] 1211 	ld	h, -14 (ix)
   471A DD 6E F8      [19] 1212 	ld	l, -8 (ix)
   471D E5            [11] 1213 	push	hl
   471E DD 6E FA      [19] 1214 	ld	l,-6 (ix)
   4721 DD 66 FB      [19] 1215 	ld	h,-5 (ix)
   4724 E5            [11] 1216 	push	hl
   4725 DD 6E EC      [19] 1217 	ld	l,-20 (ix)
   4728 DD 66 ED      [19] 1218 	ld	h,-19 (ix)
   472B E5            [11] 1219 	push	hl
   472C CD 19 40      [17] 1220 	call	_rect_overlap
   472F FD 21 0C 00   [14] 1221 	ld	iy, #12
   4733 FD 39         [15] 1222 	add	iy, sp
   4735 FD F9         [10] 1223 	ld	sp, iy
   4737 7D            [ 4] 1224 	ld	a, l
   4738 B7            [ 4] 1225 	or	a, a
   4739 28 05         [12] 1226 	jr	Z,00139$
                           1227 ;src/game.c:220: register_player_hit();
   473B CD 84 42      [17] 1228 	call	_register_player_hit
                           1229 ;src/game.c:221: break;
   473E 18 0B         [12] 1230 	jr	00140$
   4740                    1231 00139$:
                           1232 ;src/game.c:216: for (i = 0; i < MAX_ENEMIES; ++i) {
   4740 DD 34 E8      [23] 1233 	inc	-24 (ix)
   4743 DD 7E E8      [19] 1234 	ld	a, -24 (ix)
   4746 D6 06         [ 7] 1235 	sub	a, #0x06
   4748 DA 93 46      [10] 1236 	jp	C, 00177$
   474B                    1237 00140$:
                           1238 ;src/game.c:225: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   474B 3A 5C 5D      [13] 1239 	ld	a,(#_g_damagecooldown + 0)
   474E B7            [ 4] 1240 	or	a, a
   474F 20 6E         [12] 1241 	jr	NZ,00142$
   4751 3A 6F 5D      [13] 1242 	ld	a,(#_g_bossactive + 0)
   4754 B7            [ 4] 1243 	or	a, a
   4755 28 68         [12] 1244 	jr	Z,00142$
                           1245 ;src/game.c:226: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   4757 3A 6A 5D      [13] 1246 	ld	a,(#(_g_boss + 0x0005) + 0)
   475A DD 77 F2      [19] 1247 	ld	-14 (ix), a
   475D 3A 69 5D      [13] 1248 	ld	a,(#(_g_boss + 0x0004) + 0)
   4760 DD 77 F4      [19] 1249 	ld	-12 (ix), a
   4763 21 66 5D      [10] 1250 	ld	hl, #(_g_boss + 0x0001) + 0
   4766 5E            [ 7] 1251 	ld	e, (hl)
   4767 16 00         [ 7] 1252 	ld	d, #0x00
   4769 21 65 5D      [10] 1253 	ld	hl, #_g_boss + 0
   476C 4E            [ 7] 1254 	ld	c, (hl)
   476D 06 00         [ 7] 1255 	ld	b, #0x00
                           1256 ;src/game.c:225: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   476F 3A D8 5C      [13] 1257 	ld	a,(#(_g_player + 0x0005) + 0)
   4772 DD 77 F6      [19] 1258 	ld	-10 (ix), a
   4775 3A D7 5C      [13] 1259 	ld	a,(#(_g_player + 0x0004) + 0)
   4778 DD 77 F8      [19] 1260 	ld	-8 (ix), a
   477B 3A D4 5C      [13] 1261 	ld	a, (#(_g_player + 0x0001) + 0)
   477E DD 77 FA      [19] 1262 	ld	-6 (ix), a
   4781 DD 36 FB 00   [19] 1263 	ld	-5 (ix), #0x00
   4785 3A D3 5C      [13] 1264 	ld	a, (#_g_player + 0)
   4788 DD 77 EC      [19] 1265 	ld	-20 (ix), a
   478B DD 36 ED 00   [19] 1266 	ld	-19 (ix), #0x00
   478F DD 66 F2      [19] 1267 	ld	h, -14 (ix)
   4792 DD 6E F4      [19] 1268 	ld	l, -12 (ix)
   4795 E5            [11] 1269 	push	hl
   4796 D5            [11] 1270 	push	de
   4797 C5            [11] 1271 	push	bc
   4798 DD 66 F6      [19] 1272 	ld	h, -10 (ix)
   479B DD 6E F8      [19] 1273 	ld	l, -8 (ix)
   479E E5            [11] 1274 	push	hl
   479F DD 6E FA      [19] 1275 	ld	l,-6 (ix)
   47A2 DD 66 FB      [19] 1276 	ld	h,-5 (ix)
   47A5 E5            [11] 1277 	push	hl
   47A6 DD 6E EC      [19] 1278 	ld	l,-20 (ix)
   47A9 DD 66 ED      [19] 1279 	ld	h,-19 (ix)
   47AC E5            [11] 1280 	push	hl
   47AD CD 19 40      [17] 1281 	call	_rect_overlap
   47B0 FD 21 0C 00   [14] 1282 	ld	iy, #12
   47B4 FD 39         [15] 1283 	add	iy, sp
   47B6 FD F9         [10] 1284 	ld	sp, iy
   47B8 7D            [ 4] 1285 	ld	a, l
   47B9 B7            [ 4] 1286 	or	a, a
   47BA 28 03         [12] 1287 	jr	Z,00142$
                           1288 ;src/game.c:227: register_player_hit();
   47BC CD 84 42      [17] 1289 	call	_register_player_hit
   47BF                    1290 00142$:
                           1291 ;src/game.c:230: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   47BF 3A 5C 5D      [13] 1292 	ld	a,(#_g_damagecooldown + 0)
   47C2 B7            [ 4] 1293 	or	a, a
   47C3 20 31         [12] 1294 	jr	NZ,00149$
   47C5 3A D8 5C      [13] 1295 	ld	a, (#(_g_player + 0x0005) + 0)
   47C8 21 D7 5C      [10] 1296 	ld	hl, #(_g_player + 0x0004) + 0
   47CB 56            [ 7] 1297 	ld	d, (hl)
   47CC 21 D4 5C      [10] 1298 	ld	hl, #(_g_player + 0x0001) + 0
   47CF 4E            [ 7] 1299 	ld	c, (hl)
   47D0 06 00         [ 7] 1300 	ld	b, #0x00
   47D2 21 D3 5C      [10] 1301 	ld	hl, #_g_player + 0
   47D5 6E            [ 7] 1302 	ld	l, (hl)
   47D6 DD 75 F2      [19] 1303 	ld	-14 (ix), l
   47D9 DD 36 F3 00   [19] 1304 	ld	-13 (ix), #0x00
   47DD F5            [11] 1305 	push	af
   47DE 33            [ 6] 1306 	inc	sp
   47DF D5            [11] 1307 	push	de
   47E0 33            [ 6] 1308 	inc	sp
   47E1 C5            [11] 1309 	push	bc
   47E2 DD 6E F2      [19] 1310 	ld	l,-14 (ix)
   47E5 DD 66 F3      [19] 1311 	ld	h,-13 (ix)
   47E8 E5            [11] 1312 	push	hl
   47E9 CD 2E 4B      [17] 1313 	call	_collision_is_on_trap
   47EC F1            [10] 1314 	pop	af
   47ED F1            [10] 1315 	pop	af
   47EE F1            [10] 1316 	pop	af
   47EF 7D            [ 4] 1317 	ld	a, l
   47F0 B7            [ 4] 1318 	or	a, a
   47F1 28 03         [12] 1319 	jr	Z,00149$
                           1320 ;src/game.c:231: register_player_hit();
   47F3 CD 84 42      [17] 1321 	call	_register_player_hit
   47F6                    1322 00149$:
                           1323 ;src/game.c:235: if (!g_checkpointactive && g_player.x >= 44) {
   47F6 FD 21 64 5D   [14] 1324 	ld	iy, #_g_checkpointactive
   47FA FD 7E 00      [19] 1325 	ld	a, 0 (iy)
   47FD B7            [ 4] 1326 	or	a, a
   47FE 20 1E         [12] 1327 	jr	NZ,00151$
   4800 3A D3 5C      [13] 1328 	ld	a, (#_g_player + 0)
   4803 D6 2C         [ 7] 1329 	sub	a, #0x2c
   4805 38 17         [12] 1330 	jr	C,00151$
                           1331 ;src/game.c:236: g_checkpointactive = 1;
   4807 FD 36 00 01   [19] 1332 	ld	0 (iy), #0x01
                           1333 ;src/game.c:237: g_checkpointx = 44;
   480B 21 62 5D      [10] 1334 	ld	hl,#_g_checkpointx + 0
   480E 36 2C         [10] 1335 	ld	(hl), #0x2c
                           1336 ;src/game.c:238: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   4810 CD 47 4F      [17] 1337 	call	_tilemap_ground_y
   4813 4D            [ 4] 1338 	ld	c, l
   4814 21 D8 5C      [10] 1339 	ld	hl, #(_g_player + 0x0005) + 0
   4817 46            [ 7] 1340 	ld	b, (hl)
   4818 21 63 5D      [10] 1341 	ld	hl, #_g_checkpointy
   481B 79            [ 4] 1342 	ld	a, c
   481C 90            [ 4] 1343 	sub	a, b
   481D 77            [ 7] 1344 	ld	(hl), a
   481E                    1345 00151$:
                           1346 ;src/game.c:241: g_weapondisplay = 1;
   481E 21 58 5D      [10] 1347 	ld	hl,#_g_weapondisplay + 0
   4821 36 01         [10] 1348 	ld	(hl), #0x01
                           1349 ;src/game.c:243: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   4823 3A 6F 5D      [13] 1350 	ld	a,(#_g_bossactive + 0)
   4826 B7            [ 4] 1351 	or	a, a
   4827 20 45         [12] 1352 	jr	NZ,00162$
   4829 3A 5A 5D      [13] 1353 	ld	a,(#_g_aliveenemies + 0)
   482C B7            [ 4] 1354 	or	a, a
   482D 20 3F         [12] 1355 	jr	NZ,00162$
   482F 3A 5F 5D      [13] 1356 	ld	a,(#_g_gameover + 0)
   4832 B7            [ 4] 1357 	or	a, a
   4833 20 39         [12] 1358 	jr	NZ,00162$
                           1359 ;src/game.c:244: if (g_currentwave < TOTAL_WAVES) {
   4835 3A 59 5D      [13] 1360 	ld	a,(#_g_currentwave + 0)
   4838 D6 03         [ 7] 1361 	sub	a, #0x03
   483A 30 20         [12] 1362 	jr	NC,00159$
                           1363 ;src/game.c:245: if (g_wavecooldown == 0) {
   483C 3A 5B 5D      [13] 1364 	ld	a,(#_g_wavecooldown + 0)
   483F B7            [ 4] 1365 	or	a, a
   4840 20 14         [12] 1366 	jr	NZ,00154$
                           1367 ;src/game.c:246: spawn_wave(g_currentwave);
   4842 3A 59 5D      [13] 1368 	ld	a, (_g_currentwave)
   4845 F5            [11] 1369 	push	af
   4846 33            [ 6] 1370 	inc	sp
   4847 CD A6 40      [17] 1371 	call	_spawn_wave
   484A 33            [ 6] 1372 	inc	sp
                           1373 ;src/game.c:247: g_currentwave++;
   484B 21 59 5D      [10] 1374 	ld	hl, #_g_currentwave+0
   484E 34            [11] 1375 	inc	(hl)
                           1376 ;src/game.c:248: g_wavecooldown = 90;
   484F 21 5B 5D      [10] 1377 	ld	hl,#_g_wavecooldown + 0
   4852 36 5A         [10] 1378 	ld	(hl), #0x5a
   4854 18 18         [12] 1379 	jr	00162$
   4856                    1380 00154$:
                           1381 ;src/game.c:250: g_wavecooldown--;
   4856 21 5B 5D      [10] 1382 	ld	hl, #_g_wavecooldown+0
   4859 35            [11] 1383 	dec	(hl)
   485A 18 12         [12] 1384 	jr	00162$
   485C                    1385 00159$:
                           1386 ;src/game.c:252: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   485C 21 D3 5C      [10] 1387 	ld	hl, #_g_player + 0
   485F 4E            [ 7] 1388 	ld	c, (hl)
   4860 C5            [11] 1389 	push	bc
   4861 CD EB 4F      [17] 1390 	call	_tilemap_goal_x
   4864 C1            [10] 1391 	pop	bc
   4865 2D            [ 4] 1392 	dec	l
   4866 2D            [ 4] 1393 	dec	l
   4867 79            [ 4] 1394 	ld	a, c
   4868 95            [ 4] 1395 	sub	a, l
   4869 38 03         [12] 1396 	jr	C,00162$
                           1397 ;src/game.c:253: spawn_boss();
   486B CD A6 41      [17] 1398 	call	_spawn_boss
   486E                    1399 00162$:
                           1400 ;src/game.c:257: g_framecounter++;
   486E FD 21 60 5D   [14] 1401 	ld	iy, #_g_framecounter
   4872 FD 34 00      [23] 1402 	inc	0 (iy)
   4875 20 03         [12] 1403 	jr	NZ,00370$
   4877 FD 34 01      [23] 1404 	inc	1 (iy)
   487A                    1405 00370$:
                           1406 ;src/game.c:258: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   487A 21 32 00      [10] 1407 	ld	hl, #0x0032
   487D E5            [11] 1408 	push	hl
   487E 2A 60 5D      [16] 1409 	ld	hl, (_g_framecounter)
   4881 E5            [11] 1410 	push	hl
   4882 CD B1 5B      [17] 1411 	call	__moduint
   4885 F1            [10] 1412 	pop	af
   4886 F1            [10] 1413 	pop	af
   4887 7C            [ 4] 1414 	ld	a, h
   4888 B5            [ 4] 1415 	or	a,l
   4889 20 0D         [12] 1416 	jr	NZ,00166$
   488B FD 21 57 5D   [14] 1417 	ld	iy, #_g_timeleft
   488F FD 7E 00      [19] 1418 	ld	a, 0 (iy)
   4892 B7            [ 4] 1419 	or	a, a
   4893 28 03         [12] 1420 	jr	Z,00166$
                           1421 ;src/game.c:259: g_timeleft--;
   4895 FD 35 00      [23] 1422 	dec	0 (iy)
   4898                    1423 00166$:
                           1424 ;src/game.c:261: if (g_timeleft == 0 && !g_victory) {
   4898 3A 57 5D      [13] 1425 	ld	a,(#_g_timeleft + 0)
   489B B7            [ 4] 1426 	or	a, a
   489C 20 0B         [12] 1427 	jr	NZ,00169$
   489E 3A 5E 5D      [13] 1428 	ld	a,(#_g_victory + 0)
   48A1 B7            [ 4] 1429 	or	a, a
   48A2 20 05         [12] 1430 	jr	NZ,00169$
                           1431 ;src/game.c:262: g_gameover = 1;
   48A4 21 5F 5D      [10] 1432 	ld	hl,#_g_gameover + 0
   48A7 36 01         [10] 1433 	ld	(hl), #0x01
   48A9                    1434 00169$:
                           1435 ;src/game.c:265: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   48A9 3A 58 5D      [13] 1436 	ld	a, (_g_weapondisplay)
   48AC F5            [11] 1437 	push	af
   48AD 33            [ 6] 1438 	inc	sp
   48AE 3A 57 5D      [13] 1439 	ld	a, (_g_timeleft)
   48B1 F5            [11] 1440 	push	af
   48B2 33            [ 6] 1441 	inc	sp
   48B3 2A 55 5D      [16] 1442 	ld	hl, (_g_score)
   48B6 E5            [11] 1443 	push	hl
   48B7 3A 54 5D      [13] 1444 	ld	a, (_g_lives)
   48BA F5            [11] 1445 	push	af
   48BB 33            [ 6] 1446 	inc	sp
   48BC CD FD 4C      [17] 1447 	call	_hudupdate
   48BF F1            [10] 1448 	pop	af
   48C0 F1            [10] 1449 	pop	af
   48C1 33            [ 6] 1450 	inc	sp
   48C2                    1451 00178$:
   48C2 DD F9         [10] 1452 	ld	sp, ix
   48C4 DD E1         [14] 1453 	pop	ix
   48C6 C9            [10] 1454 	ret
                           1455 ;src/game.c:268: void game_render(void) {
                           1456 ;	---------------------------------
                           1457 ; Function game_render
                           1458 ; ---------------------------------
   48C7                    1459 _game_render::
                           1460 ;src/game.c:271: cpct_clearScreen(0x00);
   48C7 21 00 40      [10] 1461 	ld	hl, #0x4000
   48CA E5            [11] 1462 	push	hl
   48CB AF            [ 4] 1463 	xor	a, a
   48CC F5            [11] 1464 	push	af
   48CD 33            [ 6] 1465 	inc	sp
   48CE 26 C0         [ 7] 1466 	ld	h, #0xc0
   48D0 E5            [11] 1467 	push	hl
   48D1 CD DC 5B      [17] 1468 	call	_cpct_memset
                           1469 ;src/game.c:272: tilemap_render();
   48D4 CD C6 4E      [17] 1470 	call	_tilemap_render
                           1471 ;src/game.c:274: for (i = 0; i < MAX_PROJECTILES; ++i) {
   48D7 0E 00         [ 7] 1472 	ld	c, #0x00
   48D9                    1473 00113$:
                           1474 ;src/game.c:275: projectilerender(&g_projectiles[i]);
   48D9 06 00         [ 7] 1475 	ld	b,#0x00
   48DB 69            [ 4] 1476 	ld	l, c
   48DC 60            [ 4] 1477 	ld	h, b
   48DD 29            [11] 1478 	add	hl, hl
   48DE 29            [11] 1479 	add	hl, hl
   48DF 09            [11] 1480 	add	hl, bc
   48E0 29            [11] 1481 	add	hl, hl
   48E1 11 18 5D      [10] 1482 	ld	de, #_g_projectiles
   48E4 19            [11] 1483 	add	hl, de
   48E5 C5            [11] 1484 	push	bc
   48E6 E5            [11] 1485 	push	hl
   48E7 CD D8 59      [17] 1486 	call	_projectilerender
   48EA F1            [10] 1487 	pop	af
   48EB C1            [10] 1488 	pop	bc
                           1489 ;src/game.c:274: for (i = 0; i < MAX_PROJECTILES; ++i) {
   48EC 0C            [ 4] 1490 	inc	c
   48ED 79            [ 4] 1491 	ld	a, c
   48EE D6 06         [ 7] 1492 	sub	a, #0x06
   48F0 38 E7         [12] 1493 	jr	C,00113$
                           1494 ;src/game.c:278: for (i = 0; i < MAX_ENEMIES; ++i) {
   48F2 0E 00         [ 7] 1495 	ld	c, #0x00
   48F4                    1496 00115$:
                           1497 ;src/game.c:279: enemyrender(&g_enemies[i]);
   48F4 06 00         [ 7] 1498 	ld	b,#0x00
   48F6 69            [ 4] 1499 	ld	l, c
   48F7 60            [ 4] 1500 	ld	h, b
   48F8 29            [11] 1501 	add	hl, hl
   48F9 29            [11] 1502 	add	hl, hl
   48FA 09            [11] 1503 	add	hl, bc
   48FB 29            [11] 1504 	add	hl, hl
   48FC 11 DC 5C      [10] 1505 	ld	de, #_g_enemies
   48FF 19            [11] 1506 	add	hl, de
   4900 C5            [11] 1507 	push	bc
   4901 E5            [11] 1508 	push	hl
   4902 CD F1 53      [17] 1509 	call	_enemyrender
   4905 F1            [10] 1510 	pop	af
   4906 C1            [10] 1511 	pop	bc
                           1512 ;src/game.c:278: for (i = 0; i < MAX_ENEMIES; ++i) {
   4907 0C            [ 4] 1513 	inc	c
   4908 79            [ 4] 1514 	ld	a, c
   4909 D6 06         [ 7] 1515 	sub	a, #0x06
   490B 38 E7         [12] 1516 	jr	C,00115$
                           1517 ;src/game.c:282: if (g_bossactive) {
   490D 3A 6F 5D      [13] 1518 	ld	a,(#_g_bossactive + 0)
   4910 B7            [ 4] 1519 	or	a, a
   4911 28 45         [12] 1520 	jr	Z,00104$
                           1521 ;src/game.c:283: enemyrender(&g_boss);
   4913 21 65 5D      [10] 1522 	ld	hl, #_g_boss
   4916 E5            [11] 1523 	push	hl
   4917 CD F1 53      [17] 1524 	call	_enemyrender
                           1525 ;src/game.c:284: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x44, 32, 2);
   491A 21 18 0A      [10] 1526 	ld	hl, #0x0a18
   491D E3            [19] 1527 	ex	(sp),hl
   491E 21 00 C0      [10] 1528 	ld	hl, #0xc000
   4921 E5            [11] 1529 	push	hl
   4922 CD B3 5C      [17] 1530 	call	_cpct_getScreenPtr
   4925 01 20 02      [10] 1531 	ld	bc, #0x0220
   4928 C5            [11] 1532 	push	bc
   4929 3E 44         [ 7] 1533 	ld	a, #0x44
   492B F5            [11] 1534 	push	af
   492C 33            [ 6] 1535 	inc	sp
   492D E5            [11] 1536 	push	hl
   492E CD FA 5B      [17] 1537 	call	_cpct_drawSolidBox
   4931 F1            [10] 1538 	pop	af
   4932 F1            [10] 1539 	pop	af
   4933 33            [ 6] 1540 	inc	sp
                           1541 ;src/game.c:285: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x5C, (u8)(g_boss.health * 3), 2);
   4934 3A 6C 5D      [13] 1542 	ld	a, (#_g_boss + 7)
   4937 4F            [ 4] 1543 	ld	c, a
   4938 87            [ 4] 1544 	add	a, a
   4939 81            [ 4] 1545 	add	a, c
   493A 57            [ 4] 1546 	ld	d, a
   493B D5            [11] 1547 	push	de
   493C 21 18 0A      [10] 1548 	ld	hl, #0x0a18
   493F E5            [11] 1549 	push	hl
   4940 21 00 C0      [10] 1550 	ld	hl, #0xc000
   4943 E5            [11] 1551 	push	hl
   4944 CD B3 5C      [17] 1552 	call	_cpct_getScreenPtr
   4947 4D            [ 4] 1553 	ld	c, l
   4948 44            [ 4] 1554 	ld	b, h
   4949 D1            [10] 1555 	pop	de
   494A 3E 02         [ 7] 1556 	ld	a, #0x02
   494C F5            [11] 1557 	push	af
   494D 33            [ 6] 1558 	inc	sp
   494E 1E 5C         [ 7] 1559 	ld	e, #0x5c
   4950 D5            [11] 1560 	push	de
   4951 C5            [11] 1561 	push	bc
   4952 CD FA 5B      [17] 1562 	call	_cpct_drawSolidBox
   4955 F1            [10] 1563 	pop	af
   4956 F1            [10] 1564 	pop	af
   4957 33            [ 6] 1565 	inc	sp
   4958                    1566 00104$:
                           1567 ;src/game.c:288: playerrender(&g_player);
   4958 21 D3 5C      [10] 1568 	ld	hl, #_g_player
   495B E5            [11] 1569 	push	hl
   495C CD 31 58      [17] 1570 	call	_playerrender
   495F F1            [10] 1571 	pop	af
                           1572 ;src/game.c:289: hudrender();
   4960 CD 2E 4D      [17] 1573 	call	_hudrender
                           1574 ;src/game.c:291: if (g_victory) {
   4963 3A 5E 5D      [13] 1575 	ld	a,(#_g_victory + 0)
   4966 B7            [ 4] 1576 	or	a, a
   4967 28 1B         [12] 1577 	jr	Z,00111$
                           1578 ;src/game.c:292: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
   4969 21 1C 48      [10] 1579 	ld	hl, #0x481c
   496C E5            [11] 1580 	push	hl
   496D 21 00 C0      [10] 1581 	ld	hl, #0xc000
   4970 E5            [11] 1582 	push	hl
   4971 CD B3 5C      [17] 1583 	call	_cpct_getScreenPtr
   4974 01 18 08      [10] 1584 	ld	bc, #0x0818
   4977 C5            [11] 1585 	push	bc
   4978 3E 5C         [ 7] 1586 	ld	a, #0x5c
   497A F5            [11] 1587 	push	af
   497B 33            [ 6] 1588 	inc	sp
   497C E5            [11] 1589 	push	hl
   497D CD FA 5B      [17] 1590 	call	_cpct_drawSolidBox
   4980 F1            [10] 1591 	pop	af
   4981 F1            [10] 1592 	pop	af
   4982 33            [ 6] 1593 	inc	sp
   4983 C9            [10] 1594 	ret
   4984                    1595 00111$:
                           1596 ;src/game.c:293: } else if (g_gameover) {
   4984 3A 5F 5D      [13] 1597 	ld	a,(#_g_gameover + 0)
   4987 B7            [ 4] 1598 	or	a, a
   4988 28 1B         [12] 1599 	jr	Z,00108$
                           1600 ;src/game.c:294: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
   498A 21 1C 48      [10] 1601 	ld	hl, #0x481c
   498D E5            [11] 1602 	push	hl
   498E 21 00 C0      [10] 1603 	ld	hl, #0xc000
   4991 E5            [11] 1604 	push	hl
   4992 CD B3 5C      [17] 1605 	call	_cpct_getScreenPtr
   4995 01 18 08      [10] 1606 	ld	bc, #0x0818
   4998 C5            [11] 1607 	push	bc
   4999 3E 4C         [ 7] 1608 	ld	a, #0x4c
   499B F5            [11] 1609 	push	af
   499C 33            [ 6] 1610 	inc	sp
   499D E5            [11] 1611 	push	hl
   499E CD FA 5B      [17] 1612 	call	_cpct_drawSolidBox
   49A1 F1            [10] 1613 	pop	af
   49A2 F1            [10] 1614 	pop	af
   49A3 33            [ 6] 1615 	inc	sp
   49A4 C9            [10] 1616 	ret
   49A5                    1617 00108$:
                           1618 ;src/game.c:295: } else if (g_checkpointactive) {
   49A5 3A 64 5D      [13] 1619 	ld	a,(#_g_checkpointactive + 0)
   49A8 B7            [ 4] 1620 	or	a, a
   49A9 C8            [11] 1621 	ret	Z
                           1622 ;src/game.c:296: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), 0x3A, 2, 8);
   49AA 3A 63 5D      [13] 1623 	ld	a,(#_g_checkpointy + 0)
   49AD C6 F8         [ 7] 1624 	add	a, #0xf8
   49AF 47            [ 4] 1625 	ld	b, a
   49B0 C5            [11] 1626 	push	bc
   49B1 33            [ 6] 1627 	inc	sp
   49B2 3A 62 5D      [13] 1628 	ld	a, (_g_checkpointx)
   49B5 F5            [11] 1629 	push	af
   49B6 33            [ 6] 1630 	inc	sp
   49B7 21 00 C0      [10] 1631 	ld	hl, #0xc000
   49BA E5            [11] 1632 	push	hl
   49BB CD B3 5C      [17] 1633 	call	_cpct_getScreenPtr
   49BE 01 02 08      [10] 1634 	ld	bc, #0x0802
   49C1 C5            [11] 1635 	push	bc
   49C2 3E 3A         [ 7] 1636 	ld	a, #0x3a
   49C4 F5            [11] 1637 	push	af
   49C5 33            [ 6] 1638 	inc	sp
   49C6 E5            [11] 1639 	push	hl
   49C7 CD FA 5B      [17] 1640 	call	_cpct_drawSolidBox
   49CA F1            [10] 1641 	pop	af
   49CB F1            [10] 1642 	pop	af
   49CC 33            [ 6] 1643 	inc	sp
   49CD C9            [10] 1644 	ret
                           1645 	.area _CODE
                           1646 	.area _INITIALIZER
                           1647 	.area _CABS (ABS)
