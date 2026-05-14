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
   5D94                      49 _g_player:
   5D94                      50 	.ds 9
   5D9D                      51 _g_enemies:
   5D9D                      52 	.ds 60
   5DD9                      53 _g_projectiles:
   5DD9                      54 	.ds 60
   5E15                      55 _g_lives:
   5E15                      56 	.ds 1
   5E16                      57 _g_score:
   5E16                      58 	.ds 2
   5E18                      59 _g_timeleft:
   5E18                      60 	.ds 1
   5E19                      61 _g_weapondisplay:
   5E19                      62 	.ds 1
   5E1A                      63 _g_currentwave:
   5E1A                      64 	.ds 1
   5E1B                      65 _g_aliveenemies:
   5E1B                      66 	.ds 1
   5E1C                      67 _g_wavecooldown:
   5E1C                      68 	.ds 1
   5E1D                      69 _g_damagecooldown:
   5E1D                      70 	.ds 1
   5E1E                      71 _g_shootcooldown:
   5E1E                      72 	.ds 1
   5E1F                      73 _g_victory:
   5E1F                      74 	.ds 1
   5E20                      75 _g_gameover:
   5E20                      76 	.ds 1
   5E21                      77 _g_framecounter:
   5E21                      78 	.ds 2
   5E23                      79 _g_checkpointx:
   5E23                      80 	.ds 1
   5E24                      81 _g_checkpointy:
   5E24                      82 	.ds 1
   5E25                      83 _g_checkpointactive:
   5E25                      84 	.ds 1
   5E26                      85 _g_boss:
   5E26                      86 	.ds 10
   5E30                      87 _g_bossactive:
   5E30                      88 	.ds 1
   5E31                      89 _g_bossphase:
   5E31                      90 	.ds 1
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
   4000 21 94 5D      [10]  121 	ld	hl, #_g_player
   4003 3A 23 5E      [13]  122 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  123 	ld	(hl), a
                            124 ;src/game.c:40: g_player.y = g_checkpointy;
   4007 21 95 5D      [10]  125 	ld	hl, #(_g_player + 0x0001)
   400A 3A 24 5E      [13]  126 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  127 	ld	(hl), a
                            128 ;src/game.c:41: g_player.vx = 0;
   400E 21 96 5D      [10]  129 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  130 	ld	(hl), #0x00
                            131 ;src/game.c:42: g_player.vy = 0;
   4013 21 97 5D      [10]  132 	ld	hl, #(_g_player + 0x0003)
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
   40B1 01 9D 5D      [10]  228 	ld	bc, #_g_enemies+0
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
   40C4 CD 7C 50      [17]  245 	call	_enemyinit
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
   418C CD C1 50      [17]  378 	call	_enemyspawn
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
   419E 32 1B 5E      [13]  389 	ld	(#_g_aliveenemies + 0),a
   41A1 DD F9         [10]  390 	ld	sp, ix
   41A3 DD E1         [14]  391 	pop	ix
   41A5 C9            [10]  392 	ret
                            393 ;src/game.c:81: static void spawn_boss(void) {
                            394 ;	---------------------------------
                            395 ; Function spawn_boss
                            396 ; ---------------------------------
   41A6                     397 _spawn_boss:
                            398 ;src/game.c:82: enemyinit(&g_boss);
   41A6 21 26 5E      [10]  399 	ld	hl, #_g_boss
   41A9 E5            [11]  400 	push	hl
   41AA CD 7C 50      [17]  401 	call	_enemyinit
   41AD F1            [10]  402 	pop	af
                            403 ;src/game.c:83: enemyspawn(&g_boss, 68, 112, 1, 0);
   41AE 21 01 00      [10]  404 	ld	hl, #0x0001
   41B1 E5            [11]  405 	push	hl
   41B2 21 44 70      [10]  406 	ld	hl, #0x7044
   41B5 E5            [11]  407 	push	hl
   41B6 21 26 5E      [10]  408 	ld	hl, #_g_boss
   41B9 E5            [11]  409 	push	hl
   41BA CD C1 50      [17]  410 	call	_enemyspawn
   41BD 21 06 00      [10]  411 	ld	hl, #6
   41C0 39            [11]  412 	add	hl, sp
   41C1 F9            [ 6]  413 	ld	sp, hl
                            414 ;src/game.c:84: g_boss.w = 10;
   41C2 21 2A 5E      [10]  415 	ld	hl, #(_g_boss + 0x0004)
   41C5 36 0A         [10]  416 	ld	(hl), #0x0a
                            417 ;src/game.c:85: g_boss.h = 18;
   41C7 21 2B 5E      [10]  418 	ld	hl, #(_g_boss + 0x0005)
   41CA 36 12         [10]  419 	ld	(hl), #0x12
                            420 ;src/game.c:86: g_boss.health = 10;
   41CC 21 2D 5E      [10]  421 	ld	hl, #(_g_boss + 0x0007)
   41CF 36 0A         [10]  422 	ld	(hl), #0x0a
                            423 ;src/game.c:87: g_boss.reward = 1500;
   41D1 21 2E 5E      [10]  424 	ld	hl, #(_g_boss + 0x0008)
   41D4 36 DC         [10]  425 	ld	(hl), #0xdc
                            426 ;src/game.c:88: g_boss.kind = 3;
   41D6 21 2F 5E      [10]  427 	ld	hl, #(_g_boss + 0x0009)
   41D9 36 03         [10]  428 	ld	(hl), #0x03
                            429 ;src/game.c:89: g_boss.vx = -1;
   41DB 21 28 5E      [10]  430 	ld	hl, #(_g_boss + 0x0002)
   41DE 36 FF         [10]  431 	ld	(hl), #0xff
                            432 ;src/game.c:90: g_bossactive = 1;
   41E0 21 30 5E      [10]  433 	ld	hl,#_g_bossactive + 0
   41E3 36 01         [10]  434 	ld	(hl), #0x01
                            435 ;src/game.c:91: g_bossphase = 0;
   41E5 21 31 5E      [10]  436 	ld	hl,#_g_bossphase + 0
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
   41F8 CD D4 4E      [17]  451 	call	_input_is_shoot_just_pressed
   41FB DD 75 FF      [19]  452 	ld	-1 (ix), l
   41FE 7D            [ 4]  453 	ld	a, l
   41FF B7            [ 4]  454 	or	a, a
   4200 CA 7F 42      [10]  455 	jp	Z,00110$
                            456 ;src/game.c:99: if (g_shootcooldown) return;
   4203 3A 1E 5E      [13]  457 	ld	a,(#_g_shootcooldown + 0)
   4206 B7            [ 4]  458 	or	a, a
   4207 20 76         [12]  459 	jr	NZ,00110$
                            460 ;src/game.c:101: dir = g_player.facing_left ? -3 : 3;
   4209 3A 9B 5D      [13]  461 	ld	a, (#_g_player + 7)
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
   4227 01 D9 5D      [10]  482 	ld	bc,#_g_projectiles
   422A 09            [11]  483 	add	hl,bc
   422B DD 75 FD      [19]  484 	ld	-3 (ix), l
   422E DD 74 FE      [19]  485 	ld	-2 (ix), h
   4231 11 06 00      [10]  486 	ld	de, #0x0006
   4234 19            [11]  487 	add	hl, de
   4235 7E            [ 7]  488 	ld	a, (hl)
   4236 B7            [ 4]  489 	or	a, a
   4237 20 3C         [12]  490 	jr	NZ,00109$
                            491 ;src/game.c:105: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, 0);
   4239 3A 95 5D      [13]  492 	ld	a,(#_g_player + 1)
   423C DD 77 FF      [19]  493 	ld	-1 (ix), a
   423F C6 06         [ 7]  494 	add	a, #0x06
   4241 DD 77 FF      [19]  495 	ld	-1 (ix), a
   4244 3A 94 5D      [13]  496 	ld	a,(#_g_player + 0)
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
   4266 CD 83 59      [17]  512 	call	_projectilefire
   4269 21 06 00      [10]  513 	ld	hl, #6
   426C 39            [11]  514 	add	hl, sp
   426D F9            [ 6]  515 	ld	sp, hl
                            516 ;src/game.c:106: g_shootcooldown = 8;
   426E 21 1E 5E      [10]  517 	ld	hl,#_g_shootcooldown + 0
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
   4284 FD 21 15 5E   [14]  537 	ld	iy, #_g_lives
   4288 FD 7E 00      [19]  538 	ld	a, 0 (iy)
   428B B7            [ 4]  539 	or	a, a
   428C 28 03         [12]  540 	jr	Z,00102$
                            541 ;src/game.c:114: g_lives--;
   428E FD 35 00      [23]  542 	dec	0 (iy)
   4291                     543 00102$:
                            544 ;src/game.c:116: if (g_lives == 0) {
   4291 3A 15 5E      [13]  545 	ld	a,(#_g_lives + 0)
   4294 B7            [ 4]  546 	or	a, a
   4295 20 06         [12]  547 	jr	NZ,00104$
                            548 ;src/game.c:117: g_gameover = 1;
   4297 21 20 5E      [10]  549 	ld	hl,#_g_gameover + 0
   429A 36 01         [10]  550 	ld	(hl), #0x01
                            551 ;src/game.c:118: return;
   429C C9            [10]  552 	ret
   429D                     553 00104$:
                            554 ;src/game.c:121: reset_player_to_checkpoint();
   429D CD 00 40      [17]  555 	call	_reset_player_to_checkpoint
                            556 ;src/game.c:122: g_damagecooldown = 40;
   42A0 21 1D 5E      [10]  557 	ld	hl,#_g_damagecooldown + 0
   42A3 36 28         [10]  558 	ld	(hl), #0x28
   42A5 C9            [10]  559 	ret
                            560 ;src/game.c:125: void game_init(void) {
                            561 ;	---------------------------------
                            562 ; Function game_init
                            563 ; ---------------------------------
   42A6                     564 _game_init::
                            565 ;src/game.c:128: cpct_disableFirmware();
   42A6 CD AB 5C      [17]  566 	call	_cpct_disableFirmware
                            567 ;src/game.c:129: cpct_setVideoMode(1);
   42A9 2E 01         [ 7]  568 	ld	l, #0x01
   42AB CD 8F 5C      [17]  569 	call	_cpct_setVideoMode
                            570 ;src/game.c:130: cpct_clearScreen(0x00);
   42AE 21 00 40      [10]  571 	ld	hl, #0x4000
   42B1 E5            [11]  572 	push	hl
   42B2 AF            [ 4]  573 	xor	a, a
   42B3 F5            [11]  574 	push	af
   42B4 33            [ 6]  575 	inc	sp
   42B5 26 C0         [ 7]  576 	ld	h, #0xc0
   42B7 E5            [11]  577 	push	hl
   42B8 CD 9D 5C      [17]  578 	call	_cpct_memset
                            579 ;src/game.c:131: tilemap_init();
   42BB CD E6 4E      [17]  580 	call	_tilemap_init
                            581 ;src/game.c:132: collision_init();
   42BE CD 28 4A      [17]  582 	call	_collision_init
                            583 ;src/game.c:133: playerinit(&g_player);
   42C1 21 94 5D      [10]  584 	ld	hl, #_g_player
   42C4 E5            [11]  585 	push	hl
   42C5 CD 44 55      [17]  586 	call	_playerinit
   42C8 F1            [10]  587 	pop	af
                            588 ;src/game.c:134: hudinit();
   42C9 CD 2E 4D      [17]  589 	call	_hudinit
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
   42D6 11 D9 5D      [10]  601 	ld	de, #_g_projectiles
   42D9 19            [11]  602 	add	hl, de
   42DA C5            [11]  603 	push	bc
   42DB E5            [11]  604 	push	hl
   42DC CD 3E 59      [17]  605 	call	_projectileinit
   42DF F1            [10]  606 	pop	af
   42E0 C1            [10]  607 	pop	bc
                            608 ;src/game.c:136: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42E1 0C            [ 4]  609 	inc	c
   42E2 79            [ 4]  610 	ld	a, c
   42E3 D6 06         [ 7]  611 	sub	a, #0x06
   42E5 38 E7         [12]  612 	jr	C,00102$
                            613 ;src/game.c:140: g_lives = 3;
   42E7 21 15 5E      [10]  614 	ld	hl,#_g_lives + 0
   42EA 36 03         [10]  615 	ld	(hl), #0x03
                            616 ;src/game.c:141: g_score = 0;
   42EC 21 00 00      [10]  617 	ld	hl, #0x0000
   42EF 22 16 5E      [16]  618 	ld	(_g_score), hl
                            619 ;src/game.c:142: g_timeleft = 99;
   42F2 FD 21 18 5E   [14]  620 	ld	iy, #_g_timeleft
   42F6 FD 36 00 63   [19]  621 	ld	0 (iy), #0x63
                            622 ;src/game.c:143: g_weapondisplay = 1;
   42FA FD 21 19 5E   [14]  623 	ld	iy, #_g_weapondisplay
   42FE FD 36 00 01   [19]  624 	ld	0 (iy), #0x01
                            625 ;src/game.c:144: g_currentwave = 0;
   4302 FD 21 1A 5E   [14]  626 	ld	iy, #_g_currentwave
   4306 FD 36 00 00   [19]  627 	ld	0 (iy), #0x00
                            628 ;src/game.c:145: g_wavecooldown = 1;
   430A FD 21 1C 5E   [14]  629 	ld	iy, #_g_wavecooldown
   430E FD 36 00 01   [19]  630 	ld	0 (iy), #0x01
                            631 ;src/game.c:146: g_damagecooldown = 0;
   4312 FD 21 1D 5E   [14]  632 	ld	iy, #_g_damagecooldown
   4316 FD 36 00 00   [19]  633 	ld	0 (iy), #0x00
                            634 ;src/game.c:147: g_shootcooldown = 0;
   431A FD 21 1E 5E   [14]  635 	ld	iy, #_g_shootcooldown
   431E FD 36 00 00   [19]  636 	ld	0 (iy), #0x00
                            637 ;src/game.c:148: g_victory = 0;
   4322 FD 21 1F 5E   [14]  638 	ld	iy, #_g_victory
   4326 FD 36 00 00   [19]  639 	ld	0 (iy), #0x00
                            640 ;src/game.c:149: g_gameover = 0;
   432A FD 21 20 5E   [14]  641 	ld	iy, #_g_gameover
   432E FD 36 00 00   [19]  642 	ld	0 (iy), #0x00
                            643 ;src/game.c:150: g_framecounter = 0;
   4332 2E 00         [ 7]  644 	ld	l, #0x00
   4334 22 21 5E      [16]  645 	ld	(_g_framecounter), hl
                            646 ;src/game.c:151: g_checkpointx = 20;
   4337 21 23 5E      [10]  647 	ld	hl,#_g_checkpointx + 0
   433A 36 14         [10]  648 	ld	(hl), #0x14
                            649 ;src/game.c:152: g_checkpointy = 120;
   433C 21 24 5E      [10]  650 	ld	hl,#_g_checkpointy + 0
   433F 36 78         [10]  651 	ld	(hl), #0x78
                            652 ;src/game.c:153: g_checkpointactive = 0;
   4341 21 25 5E      [10]  653 	ld	hl,#_g_checkpointactive + 0
   4344 36 00         [10]  654 	ld	(hl), #0x00
                            655 ;src/game.c:154: g_bossactive = 0;
   4346 21 30 5E      [10]  656 	ld	hl,#_g_bossactive + 0
   4349 36 00         [10]  657 	ld	(hl), #0x00
                            658 ;src/game.c:155: enemyinit(&g_boss);
   434B 21 26 5E      [10]  659 	ld	hl, #_g_boss
   434E E5            [11]  660 	push	hl
   434F CD 7C 50      [17]  661 	call	_enemyinit
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
   4361 CD 41 4E      [17]  676 	call	_input_update
                            677 ;src/game.c:164: if (g_gameover || g_victory) {
   4364 3A 20 5E      [13]  678 	ld	a,(#_g_gameover + 0)
   4367 B7            [ 4]  679 	or	a, a
   4368 20 06         [12]  680 	jr	NZ,00101$
   436A 3A 1F 5E      [13]  681 	ld	a,(#_g_victory + 0)
   436D B7            [ 4]  682 	or	a, a
   436E 28 1C         [12]  683 	jr	Z,00102$
   4370                     684 00101$:
                            685 ;src/game.c:165: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4370 3A 19 5E      [13]  686 	ld	a, (_g_weapondisplay)
   4373 F5            [11]  687 	push	af
   4374 33            [ 6]  688 	inc	sp
   4375 3A 18 5E      [13]  689 	ld	a, (_g_timeleft)
   4378 F5            [11]  690 	push	af
   4379 33            [ 6]  691 	inc	sp
   437A 2A 16 5E      [16]  692 	ld	hl, (_g_score)
   437D E5            [11]  693 	push	hl
   437E 3A 15 5E      [13]  694 	ld	a, (_g_lives)
   4381 F5            [11]  695 	push	af
   4382 33            [ 6]  696 	inc	sp
   4383 CD 49 4D      [17]  697 	call	_hudupdate
   4386 F1            [10]  698 	pop	af
   4387 F1            [10]  699 	pop	af
   4388 33            [ 6]  700 	inc	sp
                            701 ;src/game.c:166: return;
   4389 C3 DC 48      [10]  702 	jp	00178$
   438C                     703 00102$:
                            704 ;src/game.c:169: playerupdate(&g_player);
   438C 21 94 5D      [10]  705 	ld	hl, #_g_player
   438F E5            [11]  706 	push	hl
   4390 CD 8B 55      [17]  707 	call	_playerupdate
   4393 F1            [10]  708 	pop	af
                            709 ;src/game.c:170: try_fire_projectile();
   4394 CD EB 41      [17]  710 	call	_try_fire_projectile
                            711 ;src/game.c:172: if (g_shootcooldown) g_shootcooldown--;
   4397 FD 21 1E 5E   [14]  712 	ld	iy, #_g_shootcooldown
   439B FD 7E 00      [19]  713 	ld	a, 0 (iy)
   439E B7            [ 4]  714 	or	a, a
   439F 28 03         [12]  715 	jr	Z,00105$
   43A1 FD 35 00      [23]  716 	dec	0 (iy)
   43A4                     717 00105$:
                            718 ;src/game.c:173: if (g_damagecooldown) g_damagecooldown--;
   43A4 FD 21 1D 5E   [14]  719 	ld	iy, #_g_damagecooldown
   43A8 FD 7E 00      [19]  720 	ld	a, 0 (iy)
   43AB B7            [ 4]  721 	or	a, a
   43AC 28 03         [12]  722 	jr	Z,00189$
   43AE FD 35 00      [23]  723 	dec	0 (iy)
                            724 ;src/game.c:175: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43B1                     725 00189$:
   43B1 0E 00         [ 7]  726 	ld	c, #0x00
   43B3                     727 00171$:
                            728 ;src/game.c:176: projectileupdate(&g_projectiles[i]);
   43B3 06 00         [ 7]  729 	ld	b,#0x00
   43B5 69            [ 4]  730 	ld	l, c
   43B6 60            [ 4]  731 	ld	h, b
   43B7 29            [11]  732 	add	hl, hl
   43B8 29            [11]  733 	add	hl, hl
   43B9 09            [11]  734 	add	hl, bc
   43BA 29            [11]  735 	add	hl, hl
   43BB 11 D9 5D      [10]  736 	ld	de, #_g_projectiles
   43BE 19            [11]  737 	add	hl, de
   43BF C5            [11]  738 	push	bc
   43C0 E5            [11]  739 	push	hl
   43C1 CD 3A 5A      [17]  740 	call	_projectileupdate
   43C4 F1            [10]  741 	pop	af
   43C5 C1            [10]  742 	pop	bc
                            743 ;src/game.c:175: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43C6 0C            [ 4]  744 	inc	c
   43C7 79            [ 4]  745 	ld	a, c
   43C8 D6 06         [ 7]  746 	sub	a, #0x06
   43CA 38 E7         [12]  747 	jr	C,00171$
                            748 ;src/game.c:179: for (i = 0; i < MAX_ENEMIES; ++i) {
   43CC 0E 00         [ 7]  749 	ld	c, #0x00
   43CE                     750 00173$:
                            751 ;src/game.c:180: enemyupdate(&g_enemies[i]);
   43CE 06 00         [ 7]  752 	ld	b,#0x00
   43D0 69            [ 4]  753 	ld	l, c
   43D1 60            [ 4]  754 	ld	h, b
   43D2 29            [11]  755 	add	hl, hl
   43D3 29            [11]  756 	add	hl, hl
   43D4 09            [11]  757 	add	hl, bc
   43D5 29            [11]  758 	add	hl, hl
   43D6 11 9D 5D      [10]  759 	ld	de, #_g_enemies
   43D9 19            [11]  760 	add	hl, de
   43DA C5            [11]  761 	push	bc
   43DB E5            [11]  762 	push	hl
   43DC CD 93 52      [17]  763 	call	_enemyupdate
   43DF F1            [10]  764 	pop	af
   43E0 C1            [10]  765 	pop	bc
                            766 ;src/game.c:179: for (i = 0; i < MAX_ENEMIES; ++i) {
   43E1 0C            [ 4]  767 	inc	c
   43E2 79            [ 4]  768 	ld	a, c
   43E3 D6 06         [ 7]  769 	sub	a, #0x06
   43E5 38 E7         [12]  770 	jr	C,00173$
                            771 ;src/game.c:183: if (g_bossactive) {
   43E7 3A 30 5E      [13]  772 	ld	a,(#_g_bossactive + 0)
   43EA B7            [ 4]  773 	or	a, a
   43EB 28 71         [12]  774 	jr	Z,00208$
                            775 ;src/game.c:184: if (g_boss.health > 4) g_bossphase = 0;
   43ED 21 2D 5E      [10]  776 	ld	hl, #_g_boss + 7
   43F0 4E            [ 7]  777 	ld	c, (hl)
   43F1 3E 04         [ 7]  778 	ld	a, #0x04
   43F3 91            [ 4]  779 	sub	a, c
   43F4 30 07         [12]  780 	jr	NC,00111$
   43F6 21 31 5E      [10]  781 	ld	hl,#_g_bossphase + 0
   43F9 36 00         [10]  782 	ld	(hl), #0x00
   43FB 18 05         [12]  783 	jr	00112$
   43FD                     784 00111$:
                            785 ;src/game.c:185: else g_bossphase = 1;
   43FD 21 31 5E      [10]  786 	ld	hl,#_g_bossphase + 0
   4400 36 01         [10]  787 	ld	(hl), #0x01
   4402                     788 00112$:
                            789 ;src/game.c:187: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4402 3A 94 5D      [13]  790 	ld	a,(#_g_player + 0)
   4405 DD 77 E9      [19]  791 	ld	-23 (ix), a
   4408 DD 77 EA      [19]  792 	ld	-22 (ix), a
   440B DD 36 EB 00   [19]  793 	ld	-21 (ix), #0x00
   440F DD 7E EA      [19]  794 	ld	a, -22 (ix)
   4412 C6 02         [ 7]  795 	add	a, #0x02
   4414 DD 77 EA      [19]  796 	ld	-22 (ix), a
   4417 DD 7E EB      [19]  797 	ld	a, -21 (ix)
   441A CE 00         [ 7]  798 	adc	a, #0x00
   441C DD 77 EB      [19]  799 	ld	-21 (ix), a
   441F 21 26 5E      [10]  800 	ld	hl, #_g_boss + 0
   4422 4E            [ 7]  801 	ld	c, (hl)
   4423 06 00         [ 7]  802 	ld	b, #0x00
   4425 DD 7E EA      [19]  803 	ld	a, -22 (ix)
   4428 91            [ 4]  804 	sub	a, c
   4429 DD 7E EB      [19]  805 	ld	a, -21 (ix)
   442C 98            [ 4]  806 	sbc	a, b
   442D E2 32 44      [10]  807 	jp	PO, 00369$
   4430 EE 80         [ 7]  808 	xor	a, #0x80
   4432                     809 00369$:
   4432 F2 46 44      [10]  810 	jp	P, 00180$
   4435 3A 31 5E      [13]  811 	ld	a,(#_g_bossphase + 0)
   4438 B7            [ 4]  812 	or	a, a
   4439 28 04         [12]  813 	jr	Z,00182$
   443B 0E 02         [ 7]  814 	ld	c, #0x02
   443D 18 02         [12]  815 	jr	00183$
   443F                     816 00182$:
   443F 0E 01         [ 7]  817 	ld	c, #0x01
   4441                     818 00183$:
   4441 AF            [ 4]  819 	xor	a, a
   4442 91            [ 4]  820 	sub	a, c
   4443 4F            [ 4]  821 	ld	c, a
   4444 18 0C         [12]  822 	jr	00181$
   4446                     823 00180$:
   4446 3A 31 5E      [13]  824 	ld	a,(#_g_bossphase + 0)
   4449 B7            [ 4]  825 	or	a, a
   444A 28 04         [12]  826 	jr	Z,00184$
   444C 0E 02         [ 7]  827 	ld	c, #0x02
   444E 18 02         [12]  828 	jr	00185$
   4450                     829 00184$:
   4450 0E 01         [ 7]  830 	ld	c, #0x01
   4452                     831 00185$:
   4452                     832 00181$:
   4452 21 28 5E      [10]  833 	ld	hl, #(_g_boss + 0x0002)
   4455 71            [ 7]  834 	ld	(hl), c
                            835 ;src/game.c:188: enemyupdate(&g_boss);
   4456 21 26 5E      [10]  836 	ld	hl, #_g_boss
   4459 E5            [11]  837 	push	hl
   445A CD 93 52      [17]  838 	call	_enemyupdate
   445D F1            [10]  839 	pop	af
                            840 ;src/game.c:191: for (i = 0; i < MAX_PROJECTILES; ++i) {
   445E                     841 00208$:
   445E 0E 00         [ 7]  842 	ld	c, #0x00
   4460                     843 00176$:
                            844 ;src/game.c:192: if (!g_projectiles[i].active) continue;
   4460 06 00         [ 7]  845 	ld	b,#0x00
   4462 69            [ 4]  846 	ld	l, c
   4463 60            [ 4]  847 	ld	h, b
   4464 29            [11]  848 	add	hl, hl
   4465 29            [11]  849 	add	hl, hl
   4466 09            [11]  850 	add	hl, bc
   4467 29            [11]  851 	add	hl, hl
   4468 EB            [ 4]  852 	ex	de,hl
   4469 21 D9 5D      [10]  853 	ld	hl, #_g_projectiles
   446C 19            [11]  854 	add	hl,de
   446D EB            [ 4]  855 	ex	de,hl
   446E 21 06 00      [10]  856 	ld	hl, #0x0006
   4471 19            [11]  857 	add	hl,de
   4472 DD 75 EA      [19]  858 	ld	-22 (ix), l
   4475 DD 74 EB      [19]  859 	ld	-21 (ix), h
   4478 7E            [ 7]  860 	ld	a, (hl)
   4479 B7            [ 4]  861 	or	a, a
   447A CA 9B 46      [10]  862 	jp	Z, 00133$
                            863 ;src/game.c:193: for (j = 0; j < MAX_ENEMIES; ++j) {
   447D DD 36 E8 00   [19]  864 	ld	-24 (ix), #0x00
   4481                     865 00175$:
                            866 ;src/game.c:194: if (!g_enemies[j].active) continue;
   4481 D5            [11]  867 	push	de
   4482 DD 5E E8      [19]  868 	ld	e,-24 (ix)
   4485 16 00         [ 7]  869 	ld	d,#0x00
   4487 6B            [ 4]  870 	ld	l, e
   4488 62            [ 4]  871 	ld	h, d
   4489 29            [11]  872 	add	hl, hl
   448A 29            [11]  873 	add	hl, hl
   448B 19            [11]  874 	add	hl, de
   448C 29            [11]  875 	add	hl, hl
   448D D1            [10]  876 	pop	de
   448E 3E 9D         [ 7]  877 	ld	a, #<(_g_enemies)
   4490 85            [ 4]  878 	add	a, l
   4491 DD 77 EC      [19]  879 	ld	-20 (ix), a
   4494 3E 5D         [ 7]  880 	ld	a, #>(_g_enemies)
   4496 8C            [ 4]  881 	adc	a, h
   4497 DD 77 ED      [19]  882 	ld	-19 (ix), a
   449A DD 6E EC      [19]  883 	ld	l,-20 (ix)
   449D DD 66 ED      [19]  884 	ld	h,-19 (ix)
   44A0 C5            [11]  885 	push	bc
   44A1 01 06 00      [10]  886 	ld	bc, #0x0006
   44A4 09            [11]  887 	add	hl, bc
   44A5 C1            [10]  888 	pop	bc
   44A6 46            [ 7]  889 	ld	b, (hl)
                            890 ;src/game.c:195: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   44A7 21 05 00      [10]  891 	ld	hl, #0x0005
   44AA 19            [11]  892 	add	hl,de
   44AB DD 75 FA      [19]  893 	ld	-6 (ix), l
   44AE DD 74 FB      [19]  894 	ld	-5 (ix), h
   44B1 21 04 00      [10]  895 	ld	hl, #0x0004
   44B4 19            [11]  896 	add	hl,de
   44B5 DD 75 F8      [19]  897 	ld	-8 (ix), l
   44B8 DD 74 F9      [19]  898 	ld	-7 (ix), h
   44BB 21 01 00      [10]  899 	ld	hl, #0x0001
   44BE 19            [11]  900 	add	hl,de
   44BF DD 75 F6      [19]  901 	ld	-10 (ix), l
   44C2 DD 74 F7      [19]  902 	ld	-9 (ix), h
                            903 ;src/game.c:197: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44C5 21 07 00      [10]  904 	ld	hl, #0x0007
   44C8 19            [11]  905 	add	hl,de
   44C9 DD 75 F4      [19]  906 	ld	-12 (ix), l
   44CC DD 74 F5      [19]  907 	ld	-11 (ix), h
                            908 ;src/game.c:194: if (!g_enemies[j].active) continue;
   44CF 78            [ 4]  909 	ld	a, b
   44D0 B7            [ 4]  910 	or	a, a
   44D1 CA C9 45      [10]  911 	jp	Z, 00125$
                            912 ;src/game.c:196: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   44D4 DD 6E EC      [19]  913 	ld	l,-20 (ix)
   44D7 DD 66 ED      [19]  914 	ld	h,-19 (ix)
   44DA 23            [ 6]  915 	inc	hl
   44DB 23            [ 6]  916 	inc	hl
   44DC 23            [ 6]  917 	inc	hl
   44DD 23            [ 6]  918 	inc	hl
   44DE 23            [ 6]  919 	inc	hl
   44DF 7E            [ 7]  920 	ld	a, (hl)
   44E0 DD 77 E9      [19]  921 	ld	-23 (ix), a
   44E3 DD 6E EC      [19]  922 	ld	l,-20 (ix)
   44E6 DD 66 ED      [19]  923 	ld	h,-19 (ix)
   44E9 23            [ 6]  924 	inc	hl
   44EA 23            [ 6]  925 	inc	hl
   44EB 23            [ 6]  926 	inc	hl
   44EC 23            [ 6]  927 	inc	hl
   44ED 7E            [ 7]  928 	ld	a, (hl)
   44EE DD 77 F3      [19]  929 	ld	-13 (ix), a
   44F1 DD 6E EC      [19]  930 	ld	l,-20 (ix)
   44F4 DD 66 ED      [19]  931 	ld	h,-19 (ix)
   44F7 23            [ 6]  932 	inc	hl
   44F8 46            [ 7]  933 	ld	b, (hl)
   44F9 DD 70 F1      [19]  934 	ld	-15 (ix), b
   44FC DD 36 F2 00   [19]  935 	ld	-14 (ix), #0x00
   4500 DD 6E EC      [19]  936 	ld	l,-20 (ix)
   4503 DD 66 ED      [19]  937 	ld	h,-19 (ix)
   4506 46            [ 7]  938 	ld	b, (hl)
   4507 DD 70 EF      [19]  939 	ld	-17 (ix), b
   450A DD 36 F0 00   [19]  940 	ld	-16 (ix), #0x00
                            941 ;src/game.c:195: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   450E DD 6E FA      [19]  942 	ld	l,-6 (ix)
   4511 DD 66 FB      [19]  943 	ld	h,-5 (ix)
   4514 7E            [ 7]  944 	ld	a, (hl)
   4515 DD 77 EE      [19]  945 	ld	-18 (ix), a
   4518 DD 6E F8      [19]  946 	ld	l,-8 (ix)
   451B DD 66 F9      [19]  947 	ld	h,-7 (ix)
   451E 46            [ 7]  948 	ld	b, (hl)
   451F DD 6E F6      [19]  949 	ld	l,-10 (ix)
   4522 DD 66 F7      [19]  950 	ld	h,-9 (ix)
   4525 6E            [ 7]  951 	ld	l, (hl)
   4526 DD 75 FE      [19]  952 	ld	-2 (ix), l
   4529 DD 36 FF 00   [19]  953 	ld	-1 (ix), #0x00
   452D 1A            [ 7]  954 	ld	a, (de)
   452E DD 77 FC      [19]  955 	ld	-4 (ix), a
   4531 DD 36 FD 00   [19]  956 	ld	-3 (ix), #0x00
   4535 C5            [11]  957 	push	bc
   4536 D5            [11]  958 	push	de
   4537 DD 66 E9      [19]  959 	ld	h, -23 (ix)
   453A DD 6E F3      [19]  960 	ld	l, -13 (ix)
   453D E5            [11]  961 	push	hl
   453E DD 6E F1      [19]  962 	ld	l,-15 (ix)
   4541 DD 66 F2      [19]  963 	ld	h,-14 (ix)
   4544 E5            [11]  964 	push	hl
   4545 DD 6E EF      [19]  965 	ld	l,-17 (ix)
   4548 DD 66 F0      [19]  966 	ld	h,-16 (ix)
   454B E5            [11]  967 	push	hl
   454C DD 7E EE      [19]  968 	ld	a, -18 (ix)
   454F F5            [11]  969 	push	af
   4550 33            [ 6]  970 	inc	sp
   4551 C5            [11]  971 	push	bc
   4552 33            [ 6]  972 	inc	sp
   4553 DD 6E FE      [19]  973 	ld	l,-2 (ix)
   4556 DD 66 FF      [19]  974 	ld	h,-1 (ix)
   4559 E5            [11]  975 	push	hl
   455A DD 6E FC      [19]  976 	ld	l,-4 (ix)
   455D DD 66 FD      [19]  977 	ld	h,-3 (ix)
   4560 E5            [11]  978 	push	hl
   4561 CD 19 40      [17]  979 	call	_rect_overlap
   4564 FD 21 0C 00   [14]  980 	ld	iy, #12
   4568 FD 39         [15]  981 	add	iy, sp
   456A FD F9         [10]  982 	ld	sp, iy
   456C D1            [10]  983 	pop	de
   456D C1            [10]  984 	pop	bc
   456E 7D            [ 4]  985 	ld	a, l
   456F B7            [ 4]  986 	or	a, a
   4570 28 57         [12]  987 	jr	Z,00125$
                            988 ;src/game.c:197: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   4572 DD 6E F4      [19]  989 	ld	l,-12 (ix)
   4575 DD 66 F5      [19]  990 	ld	h,-11 (ix)
   4578 66            [ 7]  991 	ld	h, (hl)
   4579 DD 6E EC      [19]  992 	ld	l, -20 (ix)
   457C DD 46 ED      [19]  993 	ld	b, -19 (ix)
   457F C5            [11]  994 	push	bc
   4580 D5            [11]  995 	push	de
   4581 E5            [11]  996 	push	hl
   4582 33            [ 6]  997 	inc	sp
   4583 60            [ 4]  998 	ld	h, b
   4584 E5            [11]  999 	push	hl
   4585 CD 04 55      [17] 1000 	call	_enemydamage
   4588 F1            [10] 1001 	pop	af
   4589 33            [ 6] 1002 	inc	sp
   458A D1            [10] 1003 	pop	de
   458B C1            [10] 1004 	pop	bc
   458C 7D            [ 4] 1005 	ld	a, l
   458D B7            [ 4] 1006 	or	a, a
   458E 28 2F         [12] 1007 	jr	Z,00124$
                           1008 ;src/game.c:198: g_score = (u16)(g_score + g_enemies[j].reward);
   4590 DD 6E EC      [19] 1009 	ld	l,-20 (ix)
   4593 DD 66 ED      [19] 1010 	ld	h,-19 (ix)
   4596 C5            [11] 1011 	push	bc
   4597 01 08 00      [10] 1012 	ld	bc, #0x0008
   459A 09            [11] 1013 	add	hl, bc
   459B C1            [10] 1014 	pop	bc
   459C 6E            [ 7] 1015 	ld	l, (hl)
   459D DD 75 FC      [19] 1016 	ld	-4 (ix), l
   45A0 DD 36 FD 00   [19] 1017 	ld	-3 (ix), #0x00
   45A4 21 16 5E      [10] 1018 	ld	hl, #_g_score
   45A7 7E            [ 7] 1019 	ld	a, (hl)
   45A8 DD 86 FC      [19] 1020 	add	a, -4 (ix)
   45AB 77            [ 7] 1021 	ld	(hl), a
   45AC 23            [ 6] 1022 	inc	hl
   45AD 7E            [ 7] 1023 	ld	a, (hl)
   45AE DD 8E FD      [19] 1024 	adc	a, -3 (ix)
   45B1 77            [ 7] 1025 	ld	(hl), a
                           1026 ;src/game.c:199: if (g_aliveenemies) g_aliveenemies--;
   45B2 FD 21 1B 5E   [14] 1027 	ld	iy, #_g_aliveenemies
   45B6 FD 7E 00      [19] 1028 	ld	a, 0 (iy)
   45B9 B7            [ 4] 1029 	or	a, a
   45BA 28 03         [12] 1030 	jr	Z,00124$
   45BC FD 35 00      [23] 1031 	dec	0 (iy)
   45BF                    1032 00124$:
                           1033 ;src/game.c:201: g_projectiles[i].active = 0;
   45BF DD 6E EA      [19] 1034 	ld	l,-22 (ix)
   45C2 DD 66 EB      [19] 1035 	ld	h,-21 (ix)
   45C5 36 00         [10] 1036 	ld	(hl), #0x00
                           1037 ;src/game.c:202: break;
   45C7 18 0B         [12] 1038 	jr	00126$
   45C9                    1039 00125$:
                           1040 ;src/game.c:193: for (j = 0; j < MAX_ENEMIES; ++j) {
   45C9 DD 34 E8      [23] 1041 	inc	-24 (ix)
   45CC DD 7E E8      [19] 1042 	ld	a, -24 (ix)
   45CF D6 06         [ 7] 1043 	sub	a, #0x06
   45D1 DA 81 44      [10] 1044 	jp	C, 00175$
   45D4                    1045 00126$:
                           1046 ;src/game.c:205: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   45D4 3A 30 5E      [13] 1047 	ld	a,(#_g_bossactive + 0)
   45D7 B7            [ 4] 1048 	or	a, a
   45D8 CA 9B 46      [10] 1049 	jp	Z, 00133$
   45DB DD 6E EA      [19] 1050 	ld	l,-22 (ix)
   45DE DD 66 EB      [19] 1051 	ld	h,-21 (ix)
   45E1 7E            [ 7] 1052 	ld	a, (hl)
   45E2 B7            [ 4] 1053 	or	a, a
   45E3 CA 9B 46      [10] 1054 	jp	Z, 00133$
                           1055 ;src/game.c:206: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   45E6 21 2B 5E      [10] 1056 	ld	hl, #(_g_boss + 0x0005) + 0
   45E9 46            [ 7] 1057 	ld	b, (hl)
   45EA 3A 2A 5E      [13] 1058 	ld	a, (#(_g_boss + 0x0004) + 0)
   45ED 21 27 5E      [10] 1059 	ld	hl, #(_g_boss + 0x0001) + 0
   45F0 6E            [ 7] 1060 	ld	l, (hl)
   45F1 DD 75 FC      [19] 1061 	ld	-4 (ix), l
   45F4 DD 36 FD 00   [19] 1062 	ld	-3 (ix), #0x00
   45F8 21 26 5E      [10] 1063 	ld	hl, #_g_boss + 0
   45FB 6E            [ 7] 1064 	ld	l, (hl)
   45FC DD 75 FE      [19] 1065 	ld	-2 (ix), l
   45FF DD 36 FF 00   [19] 1066 	ld	-1 (ix), #0x00
                           1067 ;src/game.c:205: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4603 DD 6E FA      [19] 1068 	ld	l,-6 (ix)
   4606 DD 66 FB      [19] 1069 	ld	h,-5 (ix)
   4609 F5            [11] 1070 	push	af
   460A 7E            [ 7] 1071 	ld	a, (hl)
   460B DD 77 EE      [19] 1072 	ld	-18 (ix), a
   460E F1            [10] 1073 	pop	af
   460F DD 6E F8      [19] 1074 	ld	l,-8 (ix)
   4612 DD 66 F9      [19] 1075 	ld	h,-7 (ix)
   4615 F5            [11] 1076 	push	af
   4616 7E            [ 7] 1077 	ld	a, (hl)
   4617 DD 77 EF      [19] 1078 	ld	-17 (ix), a
   461A F1            [10] 1079 	pop	af
   461B DD 6E F6      [19] 1080 	ld	l,-10 (ix)
   461E DD 66 F7      [19] 1081 	ld	h,-9 (ix)
   4621 6E            [ 7] 1082 	ld	l, (hl)
   4622 DD 75 F1      [19] 1083 	ld	-15 (ix), l
   4625 DD 36 F2 00   [19] 1084 	ld	-14 (ix), #0x00
   4629 F5            [11] 1085 	push	af
   462A 1A            [ 7] 1086 	ld	a, (de)
   462B 5F            [ 4] 1087 	ld	e, a
   462C F1            [10] 1088 	pop	af
   462D 16 00         [ 7] 1089 	ld	d, #0x00
   462F C5            [11] 1090 	push	bc
   4630 C5            [11] 1091 	push	bc
   4631 33            [ 6] 1092 	inc	sp
   4632 F5            [11] 1093 	push	af
   4633 33            [ 6] 1094 	inc	sp
   4634 DD 6E FC      [19] 1095 	ld	l,-4 (ix)
   4637 DD 66 FD      [19] 1096 	ld	h,-3 (ix)
   463A E5            [11] 1097 	push	hl
   463B DD 6E FE      [19] 1098 	ld	l,-2 (ix)
   463E DD 66 FF      [19] 1099 	ld	h,-1 (ix)
   4641 E5            [11] 1100 	push	hl
   4642 DD 66 EE      [19] 1101 	ld	h, -18 (ix)
   4645 DD 6E EF      [19] 1102 	ld	l, -17 (ix)
   4648 E5            [11] 1103 	push	hl
   4649 DD 6E F1      [19] 1104 	ld	l,-15 (ix)
   464C DD 66 F2      [19] 1105 	ld	h,-14 (ix)
   464F E5            [11] 1106 	push	hl
   4650 D5            [11] 1107 	push	de
   4651 CD 19 40      [17] 1108 	call	_rect_overlap
   4654 FD 21 0C 00   [14] 1109 	ld	iy, #12
   4658 FD 39         [15] 1110 	add	iy, sp
   465A FD F9         [10] 1111 	ld	sp, iy
   465C C1            [10] 1112 	pop	bc
   465D 7D            [ 4] 1113 	ld	a, l
   465E B7            [ 4] 1114 	or	a, a
   465F 28 3A         [12] 1115 	jr	Z,00133$
                           1116 ;src/game.c:207: g_projectiles[i].active = 0;
   4661 DD 6E EA      [19] 1117 	ld	l,-22 (ix)
   4664 DD 66 EB      [19] 1118 	ld	h,-21 (ix)
   4667 36 00         [10] 1119 	ld	(hl), #0x00
                           1120 ;src/game.c:208: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   4669 DD 6E F4      [19] 1121 	ld	l,-12 (ix)
   466C DD 66 F5      [19] 1122 	ld	h,-11 (ix)
   466F 46            [ 7] 1123 	ld	b, (hl)
   4670 11 26 5E      [10] 1124 	ld	de, #_g_boss
   4673 C5            [11] 1125 	push	bc
   4674 C5            [11] 1126 	push	bc
   4675 33            [ 6] 1127 	inc	sp
   4676 D5            [11] 1128 	push	de
   4677 CD 04 55      [17] 1129 	call	_enemydamage
   467A F1            [10] 1130 	pop	af
   467B 33            [ 6] 1131 	inc	sp
   467C C1            [10] 1132 	pop	bc
   467D 7D            [ 4] 1133 	ld	a, l
   467E B7            [ 4] 1134 	or	a, a
   467F 28 1A         [12] 1135 	jr	Z,00133$
                           1136 ;src/game.c:209: g_bossactive = 0;
   4681 21 30 5E      [10] 1137 	ld	hl,#_g_bossactive + 0
   4684 36 00         [10] 1138 	ld	(hl), #0x00
                           1139 ;src/game.c:210: g_score = (u16)(g_score + g_boss.reward);
   4686 21 2E 5E      [10] 1140 	ld	hl, #_g_boss + 8
   4689 5E            [ 7] 1141 	ld	e, (hl)
   468A 16 00         [ 7] 1142 	ld	d, #0x00
   468C 21 16 5E      [10] 1143 	ld	hl, #_g_score
   468F 7E            [ 7] 1144 	ld	a, (hl)
   4690 83            [ 4] 1145 	add	a, e
   4691 77            [ 7] 1146 	ld	(hl), a
   4692 23            [ 6] 1147 	inc	hl
   4693 7E            [ 7] 1148 	ld	a, (hl)
   4694 8A            [ 4] 1149 	adc	a, d
   4695 77            [ 7] 1150 	ld	(hl), a
                           1151 ;src/game.c:211: g_victory = 1;
   4696 21 1F 5E      [10] 1152 	ld	hl,#_g_victory + 0
   4699 36 01         [10] 1153 	ld	(hl), #0x01
   469B                    1154 00133$:
                           1155 ;src/game.c:191: for (i = 0; i < MAX_PROJECTILES; ++i) {
   469B 0C            [ 4] 1156 	inc	c
   469C 79            [ 4] 1157 	ld	a, c
   469D D6 06         [ 7] 1158 	sub	a, #0x06
   469F DA 60 44      [10] 1159 	jp	C, 00176$
                           1160 ;src/game.c:217: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1161 ;src/game.c:216: if (!g_damagecooldown) {
   46A2 3A 1D 5E      [13] 1162 	ld	a,(#_g_damagecooldown + 0)
   46A5 B7            [ 4] 1163 	or	a, a
   46A6 C2 10 48      [10] 1164 	jp	NZ, 00149$
                           1165 ;src/game.c:217: for (i = 0; i < MAX_ENEMIES; ++i) {
   46A9 DD 36 E7 00   [19] 1166 	ld	-25 (ix), #0x00
   46AD                    1167 00177$:
                           1168 ;src/game.c:218: if (!g_enemies[i].active) continue;
   46AD DD 4E E7      [19] 1169 	ld	c,-25 (ix)
   46B0 06 00         [ 7] 1170 	ld	b,#0x00
   46B2 69            [ 4] 1171 	ld	l, c
   46B3 60            [ 4] 1172 	ld	h, b
   46B4 29            [11] 1173 	add	hl, hl
   46B5 29            [11] 1174 	add	hl, hl
   46B6 09            [11] 1175 	add	hl, bc
   46B7 29            [11] 1176 	add	hl, hl
   46B8 4D            [ 4] 1177 	ld	c, l
   46B9 44            [ 4] 1178 	ld	b, h
   46BA 21 9D 5D      [10] 1179 	ld	hl, #_g_enemies
   46BD 09            [11] 1180 	add	hl,bc
   46BE DD 75 FC      [19] 1181 	ld	-4 (ix), l
   46C1 DD 74 FD      [19] 1182 	ld	-3 (ix), h
   46C4 11 06 00      [10] 1183 	ld	de, #0x0006
   46C7 19            [11] 1184 	add	hl, de
   46C8 7E            [ 7] 1185 	ld	a, (hl)
   46C9 B7            [ 4] 1186 	or	a, a
   46CA CA 5A 47      [10] 1187 	jp	Z, 00139$
                           1188 ;src/game.c:220: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   46CD DD 7E FC      [19] 1189 	ld	a, -4 (ix)
   46D0 DD 77 FE      [19] 1190 	ld	-2 (ix), a
   46D3 DD 7E FD      [19] 1191 	ld	a, -3 (ix)
   46D6 DD 77 FF      [19] 1192 	ld	-1 (ix), a
   46D9 DD 6E FE      [19] 1193 	ld	l,-2 (ix)
   46DC DD 66 FF      [19] 1194 	ld	h,-1 (ix)
   46DF 11 05 00      [10] 1195 	ld	de, #0x0005
   46E2 19            [11] 1196 	add	hl, de
   46E3 7E            [ 7] 1197 	ld	a, (hl)
   46E4 DD 77 FE      [19] 1198 	ld	-2 (ix), a
   46E7 DD 6E FC      [19] 1199 	ld	l,-4 (ix)
   46EA DD 66 FD      [19] 1200 	ld	h,-3 (ix)
   46ED 11 04 00      [10] 1201 	ld	de, #0x0004
   46F0 19            [11] 1202 	add	hl, de
   46F1 7E            [ 7] 1203 	ld	a, (hl)
   46F2 DD 77 EE      [19] 1204 	ld	-18 (ix), a
   46F5 DD 6E FC      [19] 1205 	ld	l,-4 (ix)
   46F8 DD 66 FD      [19] 1206 	ld	h,-3 (ix)
   46FB 23            [ 6] 1207 	inc	hl
   46FC 4E            [ 7] 1208 	ld	c, (hl)
   46FD 06 00         [ 7] 1209 	ld	b, #0x00
   46FF DD 6E FC      [19] 1210 	ld	l,-4 (ix)
   4702 DD 66 FD      [19] 1211 	ld	h,-3 (ix)
   4705 5E            [ 7] 1212 	ld	e, (hl)
   4706 16 00         [ 7] 1213 	ld	d, #0x00
                           1214 ;src/game.c:219: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4708 3A 99 5D      [13] 1215 	ld	a,(#(_g_player + 0x0005) + 0)
   470B DD 77 FC      [19] 1216 	ld	-4 (ix), a
   470E 3A 98 5D      [13] 1217 	ld	a,(#(_g_player + 0x0004) + 0)
   4711 DD 77 EF      [19] 1218 	ld	-17 (ix), a
   4714 3A 95 5D      [13] 1219 	ld	a, (#(_g_player + 0x0001) + 0)
   4717 DD 77 F1      [19] 1220 	ld	-15 (ix), a
   471A DD 36 F2 00   [19] 1221 	ld	-14 (ix), #0x00
   471E 3A 94 5D      [13] 1222 	ld	a, (#_g_player + 0)
   4721 DD 77 F4      [19] 1223 	ld	-12 (ix), a
   4724 DD 36 F5 00   [19] 1224 	ld	-11 (ix), #0x00
   4728 DD 66 FE      [19] 1225 	ld	h, -2 (ix)
   472B DD 6E EE      [19] 1226 	ld	l, -18 (ix)
   472E E5            [11] 1227 	push	hl
   472F C5            [11] 1228 	push	bc
   4730 D5            [11] 1229 	push	de
   4731 DD 66 FC      [19] 1230 	ld	h, -4 (ix)
   4734 DD 6E EF      [19] 1231 	ld	l, -17 (ix)
   4737 E5            [11] 1232 	push	hl
   4738 DD 6E F1      [19] 1233 	ld	l,-15 (ix)
   473B DD 66 F2      [19] 1234 	ld	h,-14 (ix)
   473E E5            [11] 1235 	push	hl
   473F DD 6E F4      [19] 1236 	ld	l,-12 (ix)
   4742 DD 66 F5      [19] 1237 	ld	h,-11 (ix)
   4745 E5            [11] 1238 	push	hl
   4746 CD 19 40      [17] 1239 	call	_rect_overlap
   4749 FD 21 0C 00   [14] 1240 	ld	iy, #12
   474D FD 39         [15] 1241 	add	iy, sp
   474F FD F9         [10] 1242 	ld	sp, iy
   4751 7D            [ 4] 1243 	ld	a, l
   4752 B7            [ 4] 1244 	or	a, a
   4753 28 05         [12] 1245 	jr	Z,00139$
                           1246 ;src/game.c:221: register_player_hit();
   4755 CD 84 42      [17] 1247 	call	_register_player_hit
                           1248 ;src/game.c:222: break;
   4758 18 0B         [12] 1249 	jr	00140$
   475A                    1250 00139$:
                           1251 ;src/game.c:217: for (i = 0; i < MAX_ENEMIES; ++i) {
   475A DD 34 E7      [23] 1252 	inc	-25 (ix)
   475D DD 7E E7      [19] 1253 	ld	a, -25 (ix)
   4760 D6 06         [ 7] 1254 	sub	a, #0x06
   4762 DA AD 46      [10] 1255 	jp	C, 00177$
   4765                    1256 00140$:
                           1257 ;src/game.c:226: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4765 3A 1D 5E      [13] 1258 	ld	a,(#_g_damagecooldown + 0)
   4768 B7            [ 4] 1259 	or	a, a
   4769 20 6E         [12] 1260 	jr	NZ,00142$
   476B 3A 30 5E      [13] 1261 	ld	a,(#_g_bossactive + 0)
   476E B7            [ 4] 1262 	or	a, a
   476F 28 68         [12] 1263 	jr	Z,00142$
                           1264 ;src/game.c:227: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   4771 3A 2B 5E      [13] 1265 	ld	a,(#(_g_boss + 0x0005) + 0)
   4774 DD 77 FC      [19] 1266 	ld	-4 (ix), a
   4777 3A 2A 5E      [13] 1267 	ld	a,(#(_g_boss + 0x0004) + 0)
   477A DD 77 FE      [19] 1268 	ld	-2 (ix), a
   477D 21 27 5E      [10] 1269 	ld	hl, #(_g_boss + 0x0001) + 0
   4780 5E            [ 7] 1270 	ld	e, (hl)
   4781 16 00         [ 7] 1271 	ld	d, #0x00
   4783 21 26 5E      [10] 1272 	ld	hl, #_g_boss + 0
   4786 4E            [ 7] 1273 	ld	c, (hl)
   4787 06 00         [ 7] 1274 	ld	b, #0x00
                           1275 ;src/game.c:226: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4789 3A 99 5D      [13] 1276 	ld	a,(#(_g_player + 0x0005) + 0)
   478C DD 77 EE      [19] 1277 	ld	-18 (ix), a
   478F 3A 98 5D      [13] 1278 	ld	a,(#(_g_player + 0x0004) + 0)
   4792 DD 77 EF      [19] 1279 	ld	-17 (ix), a
   4795 3A 95 5D      [13] 1280 	ld	a, (#(_g_player + 0x0001) + 0)
   4798 DD 77 F1      [19] 1281 	ld	-15 (ix), a
   479B DD 36 F2 00   [19] 1282 	ld	-14 (ix), #0x00
   479F 3A 94 5D      [13] 1283 	ld	a, (#_g_player + 0)
   47A2 DD 77 F4      [19] 1284 	ld	-12 (ix), a
   47A5 DD 36 F5 00   [19] 1285 	ld	-11 (ix), #0x00
   47A9 DD 66 FC      [19] 1286 	ld	h, -4 (ix)
   47AC DD 6E FE      [19] 1287 	ld	l, -2 (ix)
   47AF E5            [11] 1288 	push	hl
   47B0 D5            [11] 1289 	push	de
   47B1 C5            [11] 1290 	push	bc
   47B2 DD 66 EE      [19] 1291 	ld	h, -18 (ix)
   47B5 DD 6E EF      [19] 1292 	ld	l, -17 (ix)
   47B8 E5            [11] 1293 	push	hl
   47B9 DD 6E F1      [19] 1294 	ld	l,-15 (ix)
   47BC DD 66 F2      [19] 1295 	ld	h,-14 (ix)
   47BF E5            [11] 1296 	push	hl
   47C0 DD 6E F4      [19] 1297 	ld	l,-12 (ix)
   47C3 DD 66 F5      [19] 1298 	ld	h,-11 (ix)
   47C6 E5            [11] 1299 	push	hl
   47C7 CD 19 40      [17] 1300 	call	_rect_overlap
   47CA FD 21 0C 00   [14] 1301 	ld	iy, #12
   47CE FD 39         [15] 1302 	add	iy, sp
   47D0 FD F9         [10] 1303 	ld	sp, iy
   47D2 7D            [ 4] 1304 	ld	a, l
   47D3 B7            [ 4] 1305 	or	a, a
   47D4 28 03         [12] 1306 	jr	Z,00142$
                           1307 ;src/game.c:228: register_player_hit();
   47D6 CD 84 42      [17] 1308 	call	_register_player_hit
   47D9                    1309 00142$:
                           1310 ;src/game.c:231: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   47D9 3A 1D 5E      [13] 1311 	ld	a,(#_g_damagecooldown + 0)
   47DC B7            [ 4] 1312 	or	a, a
   47DD 20 31         [12] 1313 	jr	NZ,00149$
   47DF 3A 99 5D      [13] 1314 	ld	a, (#(_g_player + 0x0005) + 0)
   47E2 21 98 5D      [10] 1315 	ld	hl, #(_g_player + 0x0004) + 0
   47E5 56            [ 7] 1316 	ld	d, (hl)
   47E6 21 95 5D      [10] 1317 	ld	hl, #(_g_player + 0x0001) + 0
   47E9 4E            [ 7] 1318 	ld	c, (hl)
   47EA 06 00         [ 7] 1319 	ld	b, #0x00
   47EC 21 94 5D      [10] 1320 	ld	hl, #_g_player + 0
   47EF 6E            [ 7] 1321 	ld	l, (hl)
   47F0 DD 75 FC      [19] 1322 	ld	-4 (ix), l
   47F3 DD 36 FD 00   [19] 1323 	ld	-3 (ix), #0x00
   47F7 F5            [11] 1324 	push	af
   47F8 33            [ 6] 1325 	inc	sp
   47F9 D5            [11] 1326 	push	de
   47FA 33            [ 6] 1327 	inc	sp
   47FB C5            [11] 1328 	push	bc
   47FC DD 6E FC      [19] 1329 	ld	l,-4 (ix)
   47FF DD 66 FD      [19] 1330 	ld	h,-3 (ix)
   4802 E5            [11] 1331 	push	hl
   4803 CD 7A 4B      [17] 1332 	call	_collision_is_on_trap
   4806 F1            [10] 1333 	pop	af
   4807 F1            [10] 1334 	pop	af
   4808 F1            [10] 1335 	pop	af
   4809 7D            [ 4] 1336 	ld	a, l
   480A B7            [ 4] 1337 	or	a, a
   480B 28 03         [12] 1338 	jr	Z,00149$
                           1339 ;src/game.c:232: register_player_hit();
   480D CD 84 42      [17] 1340 	call	_register_player_hit
   4810                    1341 00149$:
                           1342 ;src/game.c:236: if (!g_checkpointactive && g_player.x >= 44) {
   4810 FD 21 25 5E   [14] 1343 	ld	iy, #_g_checkpointactive
   4814 FD 7E 00      [19] 1344 	ld	a, 0 (iy)
   4817 B7            [ 4] 1345 	or	a, a
   4818 20 1E         [12] 1346 	jr	NZ,00151$
   481A 3A 94 5D      [13] 1347 	ld	a, (#_g_player + 0)
   481D D6 2C         [ 7] 1348 	sub	a, #0x2c
   481F 38 17         [12] 1349 	jr	C,00151$
                           1350 ;src/game.c:237: g_checkpointactive = 1;
   4821 FD 36 00 01   [19] 1351 	ld	0 (iy), #0x01
                           1352 ;src/game.c:238: g_checkpointx = 52;
   4825 21 23 5E      [10] 1353 	ld	hl,#_g_checkpointx + 0
   4828 36 34         [10] 1354 	ld	(hl), #0x34
                           1355 ;src/game.c:239: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   482A CD 93 4F      [17] 1356 	call	_tilemap_ground_y
   482D 4D            [ 4] 1357 	ld	c, l
   482E 21 99 5D      [10] 1358 	ld	hl, #(_g_player + 0x0005) + 0
   4831 46            [ 7] 1359 	ld	b, (hl)
   4832 21 24 5E      [10] 1360 	ld	hl, #_g_checkpointy
   4835 79            [ 4] 1361 	ld	a, c
   4836 90            [ 4] 1362 	sub	a, b
   4837 77            [ 7] 1363 	ld	(hl), a
   4838                    1364 00151$:
                           1365 ;src/game.c:242: g_weapondisplay = 1;
   4838 21 19 5E      [10] 1366 	ld	hl,#_g_weapondisplay + 0
   483B 36 01         [10] 1367 	ld	(hl), #0x01
                           1368 ;src/game.c:244: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   483D 3A 30 5E      [13] 1369 	ld	a,(#_g_bossactive + 0)
   4840 B7            [ 4] 1370 	or	a, a
   4841 20 45         [12] 1371 	jr	NZ,00162$
   4843 3A 1B 5E      [13] 1372 	ld	a,(#_g_aliveenemies + 0)
   4846 B7            [ 4] 1373 	or	a, a
   4847 20 3F         [12] 1374 	jr	NZ,00162$
   4849 3A 20 5E      [13] 1375 	ld	a,(#_g_gameover + 0)
   484C B7            [ 4] 1376 	or	a, a
   484D 20 39         [12] 1377 	jr	NZ,00162$
                           1378 ;src/game.c:245: if (g_currentwave < TOTAL_WAVES) {
   484F 3A 1A 5E      [13] 1379 	ld	a,(#_g_currentwave + 0)
   4852 D6 03         [ 7] 1380 	sub	a, #0x03
   4854 30 20         [12] 1381 	jr	NC,00159$
                           1382 ;src/game.c:246: if (g_wavecooldown == 0) {
   4856 3A 1C 5E      [13] 1383 	ld	a,(#_g_wavecooldown + 0)
   4859 B7            [ 4] 1384 	or	a, a
   485A 20 14         [12] 1385 	jr	NZ,00154$
                           1386 ;src/game.c:247: spawn_wave(g_currentwave);
   485C 3A 1A 5E      [13] 1387 	ld	a, (_g_currentwave)
   485F F5            [11] 1388 	push	af
   4860 33            [ 6] 1389 	inc	sp
   4861 CD A6 40      [17] 1390 	call	_spawn_wave
   4864 33            [ 6] 1391 	inc	sp
                           1392 ;src/game.c:248: g_currentwave++;
   4865 21 1A 5E      [10] 1393 	ld	hl, #_g_currentwave+0
   4868 34            [11] 1394 	inc	(hl)
                           1395 ;src/game.c:249: g_wavecooldown = 90;
   4869 21 1C 5E      [10] 1396 	ld	hl,#_g_wavecooldown + 0
   486C 36 5A         [10] 1397 	ld	(hl), #0x5a
   486E 18 18         [12] 1398 	jr	00162$
   4870                    1399 00154$:
                           1400 ;src/game.c:251: g_wavecooldown--;
   4870 21 1C 5E      [10] 1401 	ld	hl, #_g_wavecooldown+0
   4873 35            [11] 1402 	dec	(hl)
   4874 18 12         [12] 1403 	jr	00162$
   4876                    1404 00159$:
                           1405 ;src/game.c:253: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   4876 21 94 5D      [10] 1406 	ld	hl, #_g_player + 0
   4879 4E            [ 7] 1407 	ld	c, (hl)
   487A C5            [11] 1408 	push	bc
   487B CD 37 50      [17] 1409 	call	_tilemap_goal_x
   487E C1            [10] 1410 	pop	bc
   487F 2D            [ 4] 1411 	dec	l
   4880 2D            [ 4] 1412 	dec	l
   4881 79            [ 4] 1413 	ld	a, c
   4882 95            [ 4] 1414 	sub	a, l
   4883 38 03         [12] 1415 	jr	C,00162$
                           1416 ;src/game.c:254: spawn_boss();
   4885 CD A6 41      [17] 1417 	call	_spawn_boss
   4888                    1418 00162$:
                           1419 ;src/game.c:258: g_framecounter++;
   4888 FD 21 21 5E   [14] 1420 	ld	iy, #_g_framecounter
   488C FD 34 00      [23] 1421 	inc	0 (iy)
   488F 20 03         [12] 1422 	jr	NZ,00370$
   4891 FD 34 01      [23] 1423 	inc	1 (iy)
   4894                    1424 00370$:
                           1425 ;src/game.c:259: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   4894 21 32 00      [10] 1426 	ld	hl, #0x0032
   4897 E5            [11] 1427 	push	hl
   4898 2A 21 5E      [16] 1428 	ld	hl, (_g_framecounter)
   489B E5            [11] 1429 	push	hl
   489C CD 72 5C      [17] 1430 	call	__moduint
   489F F1            [10] 1431 	pop	af
   48A0 F1            [10] 1432 	pop	af
   48A1 7C            [ 4] 1433 	ld	a, h
   48A2 B5            [ 4] 1434 	or	a,l
   48A3 20 0D         [12] 1435 	jr	NZ,00166$
   48A5 FD 21 18 5E   [14] 1436 	ld	iy, #_g_timeleft
   48A9 FD 7E 00      [19] 1437 	ld	a, 0 (iy)
   48AC B7            [ 4] 1438 	or	a, a
   48AD 28 03         [12] 1439 	jr	Z,00166$
                           1440 ;src/game.c:260: g_timeleft--;
   48AF FD 35 00      [23] 1441 	dec	0 (iy)
   48B2                    1442 00166$:
                           1443 ;src/game.c:262: if (g_timeleft == 0 && !g_victory) {
   48B2 3A 18 5E      [13] 1444 	ld	a,(#_g_timeleft + 0)
   48B5 B7            [ 4] 1445 	or	a, a
   48B6 20 0B         [12] 1446 	jr	NZ,00169$
   48B8 3A 1F 5E      [13] 1447 	ld	a,(#_g_victory + 0)
   48BB B7            [ 4] 1448 	or	a, a
   48BC 20 05         [12] 1449 	jr	NZ,00169$
                           1450 ;src/game.c:263: g_gameover = 1;
   48BE 21 20 5E      [10] 1451 	ld	hl,#_g_gameover + 0
   48C1 36 01         [10] 1452 	ld	(hl), #0x01
   48C3                    1453 00169$:
                           1454 ;src/game.c:266: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   48C3 3A 19 5E      [13] 1455 	ld	a, (_g_weapondisplay)
   48C6 F5            [11] 1456 	push	af
   48C7 33            [ 6] 1457 	inc	sp
   48C8 3A 18 5E      [13] 1458 	ld	a, (_g_timeleft)
   48CB F5            [11] 1459 	push	af
   48CC 33            [ 6] 1460 	inc	sp
   48CD 2A 16 5E      [16] 1461 	ld	hl, (_g_score)
   48D0 E5            [11] 1462 	push	hl
   48D1 3A 15 5E      [13] 1463 	ld	a, (_g_lives)
   48D4 F5            [11] 1464 	push	af
   48D5 33            [ 6] 1465 	inc	sp
   48D6 CD 49 4D      [17] 1466 	call	_hudupdate
   48D9 F1            [10] 1467 	pop	af
   48DA F1            [10] 1468 	pop	af
   48DB 33            [ 6] 1469 	inc	sp
   48DC                    1470 00178$:
   48DC DD F9         [10] 1471 	ld	sp, ix
   48DE DD E1         [14] 1472 	pop	ix
   48E0 C9            [10] 1473 	ret
                           1474 ;src/game.c:269: void game_render(void) {
                           1475 ;	---------------------------------
                           1476 ; Function game_render
                           1477 ; ---------------------------------
   48E1                    1478 _game_render::
                           1479 ;src/game.c:272: cpct_clearScreen(0x00);
   48E1 21 00 40      [10] 1480 	ld	hl, #0x4000
   48E4 E5            [11] 1481 	push	hl
   48E5 AF            [ 4] 1482 	xor	a, a
   48E6 F5            [11] 1483 	push	af
   48E7 33            [ 6] 1484 	inc	sp
   48E8 26 C0         [ 7] 1485 	ld	h, #0xc0
   48EA E5            [11] 1486 	push	hl
   48EB CD 9D 5C      [17] 1487 	call	_cpct_memset
                           1488 ;src/game.c:273: tilemap_render();
   48EE CD 12 4F      [17] 1489 	call	_tilemap_render
                           1490 ;src/game.c:275: for (i = 0; i < MAX_PROJECTILES; ++i) {
   48F1 0E 00         [ 7] 1491 	ld	c, #0x00
   48F3                    1492 00113$:
                           1493 ;src/game.c:276: projectilerender(&g_projectiles[i]);
   48F3 06 00         [ 7] 1494 	ld	b,#0x00
   48F5 69            [ 4] 1495 	ld	l, c
   48F6 60            [ 4] 1496 	ld	h, b
   48F7 29            [11] 1497 	add	hl, hl
   48F8 29            [11] 1498 	add	hl, hl
   48F9 09            [11] 1499 	add	hl, bc
   48FA 29            [11] 1500 	add	hl, hl
   48FB 11 D9 5D      [10] 1501 	ld	de, #_g_projectiles
   48FE 19            [11] 1502 	add	hl, de
   48FF C5            [11] 1503 	push	bc
   4900 E5            [11] 1504 	push	hl
   4901 CD 99 5A      [17] 1505 	call	_projectilerender
   4904 F1            [10] 1506 	pop	af
   4905 C1            [10] 1507 	pop	bc
                           1508 ;src/game.c:275: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4906 0C            [ 4] 1509 	inc	c
   4907 79            [ 4] 1510 	ld	a, c
   4908 D6 06         [ 7] 1511 	sub	a, #0x06
   490A 38 E7         [12] 1512 	jr	C,00113$
                           1513 ;src/game.c:279: for (i = 0; i < MAX_ENEMIES; ++i) {
   490C 0E 00         [ 7] 1514 	ld	c, #0x00
   490E                    1515 00115$:
                           1516 ;src/game.c:280: enemyrender(&g_enemies[i]);
   490E 06 00         [ 7] 1517 	ld	b,#0x00
   4910 69            [ 4] 1518 	ld	l, c
   4911 60            [ 4] 1519 	ld	h, b
   4912 29            [11] 1520 	add	hl, hl
   4913 29            [11] 1521 	add	hl, hl
   4914 09            [11] 1522 	add	hl, bc
   4915 29            [11] 1523 	add	hl, hl
   4916 11 9D 5D      [10] 1524 	ld	de, #_g_enemies
   4919 19            [11] 1525 	add	hl, de
   491A C5            [11] 1526 	push	bc
   491B E5            [11] 1527 	push	hl
   491C CD 8A 54      [17] 1528 	call	_enemyrender
   491F F1            [10] 1529 	pop	af
   4920 C1            [10] 1530 	pop	bc
                           1531 ;src/game.c:279: for (i = 0; i < MAX_ENEMIES; ++i) {
   4921 0C            [ 4] 1532 	inc	c
   4922 79            [ 4] 1533 	ld	a, c
   4923 D6 06         [ 7] 1534 	sub	a, #0x06
   4925 38 E7         [12] 1535 	jr	C,00115$
                           1536 ;src/game.c:283: if (g_bossactive) {
   4927 3A 30 5E      [13] 1537 	ld	a,(#_g_bossactive + 0)
   492A B7            [ 4] 1538 	or	a, a
   492B 28 45         [12] 1539 	jr	Z,00104$
                           1540 ;src/game.c:284: enemyrender(&g_boss);
   492D 21 26 5E      [10] 1541 	ld	hl, #_g_boss
   4930 E5            [11] 1542 	push	hl
   4931 CD 8A 54      [17] 1543 	call	_enemyrender
                           1544 ;src/game.c:285: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x44, 32, 2);
   4934 21 18 0A      [10] 1545 	ld	hl, #0x0a18
   4937 E3            [19] 1546 	ex	(sp),hl
   4938 21 00 C0      [10] 1547 	ld	hl, #0xc000
   493B E5            [11] 1548 	push	hl
   493C CD 74 5D      [17] 1549 	call	_cpct_getScreenPtr
   493F 01 20 02      [10] 1550 	ld	bc, #0x0220
   4942 C5            [11] 1551 	push	bc
   4943 3E 44         [ 7] 1552 	ld	a, #0x44
   4945 F5            [11] 1553 	push	af
   4946 33            [ 6] 1554 	inc	sp
   4947 E5            [11] 1555 	push	hl
   4948 CD BB 5C      [17] 1556 	call	_cpct_drawSolidBox
   494B F1            [10] 1557 	pop	af
   494C F1            [10] 1558 	pop	af
   494D 33            [ 6] 1559 	inc	sp
                           1560 ;src/game.c:286: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x5C, (u8)(g_boss.health * 3), 2);
   494E 3A 2D 5E      [13] 1561 	ld	a, (#_g_boss + 7)
   4951 4F            [ 4] 1562 	ld	c, a
   4952 87            [ 4] 1563 	add	a, a
   4953 81            [ 4] 1564 	add	a, c
   4954 57            [ 4] 1565 	ld	d, a
   4955 D5            [11] 1566 	push	de
   4956 21 18 0A      [10] 1567 	ld	hl, #0x0a18
   4959 E5            [11] 1568 	push	hl
   495A 21 00 C0      [10] 1569 	ld	hl, #0xc000
   495D E5            [11] 1570 	push	hl
   495E CD 74 5D      [17] 1571 	call	_cpct_getScreenPtr
   4961 4D            [ 4] 1572 	ld	c, l
   4962 44            [ 4] 1573 	ld	b, h
   4963 D1            [10] 1574 	pop	de
   4964 3E 02         [ 7] 1575 	ld	a, #0x02
   4966 F5            [11] 1576 	push	af
   4967 33            [ 6] 1577 	inc	sp
   4968 1E 5C         [ 7] 1578 	ld	e, #0x5c
   496A D5            [11] 1579 	push	de
   496B C5            [11] 1580 	push	bc
   496C CD BB 5C      [17] 1581 	call	_cpct_drawSolidBox
   496F F1            [10] 1582 	pop	af
   4970 F1            [10] 1583 	pop	af
   4971 33            [ 6] 1584 	inc	sp
   4972                    1585 00104$:
                           1586 ;src/game.c:289: playerrender(&g_player);
   4972 21 94 5D      [10] 1587 	ld	hl, #_g_player
   4975 E5            [11] 1588 	push	hl
   4976 CD F9 58      [17] 1589 	call	_playerrender
   4979 F1            [10] 1590 	pop	af
                           1591 ;src/game.c:290: hudrender();
   497A CD 7A 4D      [17] 1592 	call	_hudrender
                           1593 ;src/game.c:292: if (g_victory) {
   497D 3A 1F 5E      [13] 1594 	ld	a,(#_g_victory + 0)
   4980 B7            [ 4] 1595 	or	a, a
   4981 28 34         [12] 1596 	jr	Z,00111$
                           1597 ;src/game.c:293: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x5A, 32, 12);
   4983 21 18 44      [10] 1598 	ld	hl, #0x4418
   4986 E5            [11] 1599 	push	hl
   4987 21 00 C0      [10] 1600 	ld	hl, #0xc000
   498A E5            [11] 1601 	push	hl
   498B CD 74 5D      [17] 1602 	call	_cpct_getScreenPtr
   498E 01 20 0C      [10] 1603 	ld	bc, #0x0c20
   4991 C5            [11] 1604 	push	bc
   4992 3E 5A         [ 7] 1605 	ld	a, #0x5a
   4994 F5            [11] 1606 	push	af
   4995 33            [ 6] 1607 	inc	sp
   4996 E5            [11] 1608 	push	hl
   4997 CD BB 5C      [17] 1609 	call	_cpct_drawSolidBox
   499A F1            [10] 1610 	pop	af
                           1611 ;src/game.c:294: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
   499B 33            [ 6] 1612 	inc	sp
   499C 21 1C 48      [10] 1613 	ld	hl,#0x481c
   499F E3            [19] 1614 	ex	(sp),hl
   49A0 21 00 C0      [10] 1615 	ld	hl, #0xc000
   49A3 E5            [11] 1616 	push	hl
   49A4 CD 74 5D      [17] 1617 	call	_cpct_getScreenPtr
   49A7 01 18 08      [10] 1618 	ld	bc, #0x0818
   49AA C5            [11] 1619 	push	bc
   49AB 3E 5C         [ 7] 1620 	ld	a, #0x5c
   49AD F5            [11] 1621 	push	af
   49AE 33            [ 6] 1622 	inc	sp
   49AF E5            [11] 1623 	push	hl
   49B0 CD BB 5C      [17] 1624 	call	_cpct_drawSolidBox
   49B3 F1            [10] 1625 	pop	af
   49B4 F1            [10] 1626 	pop	af
   49B5 33            [ 6] 1627 	inc	sp
   49B6 C9            [10] 1628 	ret
   49B7                    1629 00111$:
                           1630 ;src/game.c:295: } else if (g_gameover) {
   49B7 3A 20 5E      [13] 1631 	ld	a,(#_g_gameover + 0)
   49BA B7            [ 4] 1632 	or	a, a
   49BB 28 34         [12] 1633 	jr	Z,00108$
                           1634 ;src/game.c:296: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x44, 32, 12);
   49BD 21 18 44      [10] 1635 	ld	hl, #0x4418
   49C0 E5            [11] 1636 	push	hl
   49C1 21 00 C0      [10] 1637 	ld	hl, #0xc000
   49C4 E5            [11] 1638 	push	hl
   49C5 CD 74 5D      [17] 1639 	call	_cpct_getScreenPtr
   49C8 01 20 0C      [10] 1640 	ld	bc, #0x0c20
   49CB C5            [11] 1641 	push	bc
   49CC 3E 44         [ 7] 1642 	ld	a, #0x44
   49CE F5            [11] 1643 	push	af
   49CF 33            [ 6] 1644 	inc	sp
   49D0 E5            [11] 1645 	push	hl
   49D1 CD BB 5C      [17] 1646 	call	_cpct_drawSolidBox
   49D4 F1            [10] 1647 	pop	af
                           1648 ;src/game.c:297: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
   49D5 33            [ 6] 1649 	inc	sp
   49D6 21 1C 48      [10] 1650 	ld	hl,#0x481c
   49D9 E3            [19] 1651 	ex	(sp),hl
   49DA 21 00 C0      [10] 1652 	ld	hl, #0xc000
   49DD E5            [11] 1653 	push	hl
   49DE CD 74 5D      [17] 1654 	call	_cpct_getScreenPtr
   49E1 01 18 08      [10] 1655 	ld	bc, #0x0818
   49E4 C5            [11] 1656 	push	bc
   49E5 3E 4C         [ 7] 1657 	ld	a, #0x4c
   49E7 F5            [11] 1658 	push	af
   49E8 33            [ 6] 1659 	inc	sp
   49E9 E5            [11] 1660 	push	hl
   49EA CD BB 5C      [17] 1661 	call	_cpct_drawSolidBox
   49ED F1            [10] 1662 	pop	af
   49EE F1            [10] 1663 	pop	af
   49EF 33            [ 6] 1664 	inc	sp
   49F0 C9            [10] 1665 	ret
   49F1                    1666 00108$:
                           1667 ;src/game.c:298: } else if (g_checkpointactive) {
   49F1 3A 25 5E      [13] 1668 	ld	a,(#_g_checkpointactive + 0)
   49F4 B7            [ 4] 1669 	or	a, a
   49F5 C8            [11] 1670 	ret	Z
                           1671 ;src/game.c:299: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), 0x3A, 2, 8);
   49F6 3A 24 5E      [13] 1672 	ld	a,(#_g_checkpointy + 0)
   49F9 C6 F8         [ 7] 1673 	add	a, #0xf8
   49FB 47            [ 4] 1674 	ld	b, a
   49FC C5            [11] 1675 	push	bc
   49FD 33            [ 6] 1676 	inc	sp
   49FE 3A 23 5E      [13] 1677 	ld	a, (_g_checkpointx)
   4A01 F5            [11] 1678 	push	af
   4A02 33            [ 6] 1679 	inc	sp
   4A03 21 00 C0      [10] 1680 	ld	hl, #0xc000
   4A06 E5            [11] 1681 	push	hl
   4A07 CD 74 5D      [17] 1682 	call	_cpct_getScreenPtr
   4A0A 01 02 08      [10] 1683 	ld	bc, #0x0802
   4A0D C5            [11] 1684 	push	bc
   4A0E 3E 3A         [ 7] 1685 	ld	a, #0x3a
   4A10 F5            [11] 1686 	push	af
   4A11 33            [ 6] 1687 	inc	sp
   4A12 E5            [11] 1688 	push	hl
   4A13 CD BB 5C      [17] 1689 	call	_cpct_drawSolidBox
   4A16 F1            [10] 1690 	pop	af
   4A17 F1            [10] 1691 	pop	af
   4A18 33            [ 6] 1692 	inc	sp
   4A19 C9            [10] 1693 	ret
                           1694 	.area _CODE
                           1695 	.area _INITIALIZER
                           1696 	.area _CABS (ABS)
