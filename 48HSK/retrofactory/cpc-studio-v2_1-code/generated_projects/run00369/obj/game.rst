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
   5E82                      49 _g_player:
   5E82                      50 	.ds 9
   5E8B                      51 _g_enemies:
   5E8B                      52 	.ds 60
   5EC7                      53 _g_projectiles:
   5EC7                      54 	.ds 60
   5F03                      55 _g_lives:
   5F03                      56 	.ds 1
   5F04                      57 _g_score:
   5F04                      58 	.ds 2
   5F06                      59 _g_timeleft:
   5F06                      60 	.ds 1
   5F07                      61 _g_weapondisplay:
   5F07                      62 	.ds 1
   5F08                      63 _g_currentwave:
   5F08                      64 	.ds 1
   5F09                      65 _g_aliveenemies:
   5F09                      66 	.ds 1
   5F0A                      67 _g_wavecooldown:
   5F0A                      68 	.ds 1
   5F0B                      69 _g_damagecooldown:
   5F0B                      70 	.ds 1
   5F0C                      71 _g_shootcooldown:
   5F0C                      72 	.ds 1
   5F0D                      73 _g_victory:
   5F0D                      74 	.ds 1
   5F0E                      75 _g_gameover:
   5F0E                      76 	.ds 1
   5F0F                      77 _g_framecounter:
   5F0F                      78 	.ds 2
   5F11                      79 _g_checkpointx:
   5F11                      80 	.ds 1
   5F12                      81 _g_checkpointy:
   5F12                      82 	.ds 1
   5F13                      83 _g_checkpointactive:
   5F13                      84 	.ds 1
   5F14                      85 _g_boss:
   5F14                      86 	.ds 10
   5F1E                      87 _g_bossactive:
   5F1E                      88 	.ds 1
   5F1F                      89 _g_bossphase:
   5F1F                      90 	.ds 1
   5F20                      91 _g_weaponlevel:
   5F20                      92 	.ds 1
   5F21                      93 _g_pickuptaken:
   5F21                      94 	.ds 1
                             95 ;--------------------------------------------------------
                             96 ; ram data
                             97 ;--------------------------------------------------------
                             98 	.area _INITIALIZED
                             99 ;--------------------------------------------------------
                            100 ; absolute external ram data
                            101 ;--------------------------------------------------------
                            102 	.area _DABS (ABS)
                            103 ;--------------------------------------------------------
                            104 ; global & static initialisations
                            105 ;--------------------------------------------------------
                            106 	.area _HOME
                            107 	.area _GSINIT
                            108 	.area _GSFINAL
                            109 	.area _GSINIT
                            110 ;--------------------------------------------------------
                            111 ; Home
                            112 ;--------------------------------------------------------
                            113 	.area _HOME
                            114 	.area _HOME
                            115 ;--------------------------------------------------------
                            116 ; code
                            117 ;--------------------------------------------------------
                            118 	.area _CODE
                            119 ;src/game.c:40: static void reset_player_to_checkpoint(void) {
                            120 ;	---------------------------------
                            121 ; Function reset_player_to_checkpoint
                            122 ; ---------------------------------
   4000                     123 _reset_player_to_checkpoint:
                            124 ;src/game.c:41: g_player.x = g_checkpointx;
   4000 21 82 5E      [10]  125 	ld	hl, #_g_player
   4003 3A 11 5F      [13]  126 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  127 	ld	(hl), a
                            128 ;src/game.c:42: g_player.y = g_checkpointy;
   4007 21 83 5E      [10]  129 	ld	hl, #(_g_player + 0x0001)
   400A 3A 12 5F      [13]  130 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  131 	ld	(hl), a
                            132 ;src/game.c:43: g_player.vx = 0;
   400E 21 84 5E      [10]  133 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  134 	ld	(hl), #0x00
                            135 ;src/game.c:44: g_player.vy = 0;
   4013 21 85 5E      [10]  136 	ld	hl, #(_g_player + 0x0003)
   4016 36 00         [10]  137 	ld	(hl), #0x00
   4018 C9            [10]  138 	ret
                            139 ;src/game.c:47: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
                            140 ;	---------------------------------
                            141 ; Function rect_overlap
                            142 ; ---------------------------------
   4019                     143 _rect_overlap:
   4019 DD E5         [15]  144 	push	ix
   401B DD 21 00 00   [14]  145 	ld	ix,#0
   401F DD 39         [15]  146 	add	ix,sp
                            147 ;src/game.c:48: if (ax + aw <= bx) return 0;
   4021 DD 4E 08      [19]  148 	ld	c, 8 (ix)
   4024 06 00         [ 7]  149 	ld	b, #0x00
   4026 DD 6E 04      [19]  150 	ld	l,4 (ix)
   4029 DD 66 05      [19]  151 	ld	h,5 (ix)
   402C 09            [11]  152 	add	hl, bc
   402D DD 7E 0A      [19]  153 	ld	a, 10 (ix)
   4030 95            [ 4]  154 	sub	a, l
   4031 DD 7E 0B      [19]  155 	ld	a, 11 (ix)
   4034 9C            [ 4]  156 	sbc	a, h
   4035 E2 3A 40      [10]  157 	jp	PO, 00127$
   4038 EE 80         [ 7]  158 	xor	a, #0x80
   403A                     159 00127$:
   403A FA 41 40      [10]  160 	jp	M, 00102$
   403D 2E 00         [ 7]  161 	ld	l, #0x00
   403F 18 62         [12]  162 	jr	00109$
   4041                     163 00102$:
                            164 ;src/game.c:49: if (bx + bw <= ax) return 0;
   4041 DD 4E 0E      [19]  165 	ld	c, 14 (ix)
   4044 06 00         [ 7]  166 	ld	b, #0x00
   4046 DD 6E 0A      [19]  167 	ld	l,10 (ix)
   4049 DD 66 0B      [19]  168 	ld	h,11 (ix)
   404C 09            [11]  169 	add	hl, bc
   404D DD 7E 04      [19]  170 	ld	a, 4 (ix)
   4050 95            [ 4]  171 	sub	a, l
   4051 DD 7E 05      [19]  172 	ld	a, 5 (ix)
   4054 9C            [ 4]  173 	sbc	a, h
   4055 E2 5A 40      [10]  174 	jp	PO, 00128$
   4058 EE 80         [ 7]  175 	xor	a, #0x80
   405A                     176 00128$:
   405A FA 61 40      [10]  177 	jp	M, 00104$
   405D 2E 00         [ 7]  178 	ld	l, #0x00
   405F 18 42         [12]  179 	jr	00109$
   4061                     180 00104$:
                            181 ;src/game.c:50: if (ay + ah <= by) return 0;
   4061 DD 4E 09      [19]  182 	ld	c, 9 (ix)
   4064 06 00         [ 7]  183 	ld	b, #0x00
   4066 DD 6E 06      [19]  184 	ld	l,6 (ix)
   4069 DD 66 07      [19]  185 	ld	h,7 (ix)
   406C 09            [11]  186 	add	hl, bc
   406D DD 7E 0C      [19]  187 	ld	a, 12 (ix)
   4070 95            [ 4]  188 	sub	a, l
   4071 DD 7E 0D      [19]  189 	ld	a, 13 (ix)
   4074 9C            [ 4]  190 	sbc	a, h
   4075 E2 7A 40      [10]  191 	jp	PO, 00129$
   4078 EE 80         [ 7]  192 	xor	a, #0x80
   407A                     193 00129$:
   407A FA 81 40      [10]  194 	jp	M, 00106$
   407D 2E 00         [ 7]  195 	ld	l, #0x00
   407F 18 22         [12]  196 	jr	00109$
   4081                     197 00106$:
                            198 ;src/game.c:51: if (by + bh <= ay) return 0;
   4081 DD 4E 0F      [19]  199 	ld	c, 15 (ix)
   4084 06 00         [ 7]  200 	ld	b, #0x00
   4086 DD 6E 0C      [19]  201 	ld	l,12 (ix)
   4089 DD 66 0D      [19]  202 	ld	h,13 (ix)
   408C 09            [11]  203 	add	hl, bc
   408D DD 7E 06      [19]  204 	ld	a, 6 (ix)
   4090 95            [ 4]  205 	sub	a, l
   4091 DD 7E 07      [19]  206 	ld	a, 7 (ix)
   4094 9C            [ 4]  207 	sbc	a, h
   4095 E2 9A 40      [10]  208 	jp	PO, 00130$
   4098 EE 80         [ 7]  209 	xor	a, #0x80
   409A                     210 00130$:
   409A FA A1 40      [10]  211 	jp	M, 00108$
   409D 2E 00         [ 7]  212 	ld	l, #0x00
   409F 18 02         [12]  213 	jr	00109$
   40A1                     214 00108$:
                            215 ;src/game.c:52: return 1;
   40A1 2E 01         [ 7]  216 	ld	l, #0x01
   40A3                     217 00109$:
   40A3 DD E1         [14]  218 	pop	ix
   40A5 C9            [10]  219 	ret
                            220 ;src/game.c:55: static void spawn_wave(u8 wave) {
                            221 ;	---------------------------------
                            222 ; Function spawn_wave
                            223 ; ---------------------------------
   40A6                     224 _spawn_wave:
   40A6 DD E5         [15]  225 	push	ix
   40A8 DD 21 00 00   [14]  226 	ld	ix,#0
   40AC DD 39         [15]  227 	add	ix,sp
   40AE F5            [11]  228 	push	af
   40AF F5            [11]  229 	push	af
   40B0 3B            [ 6]  230 	dec	sp
                            231 ;src/game.c:59: for (i = 0; i < MAX_ENEMIES; ++i) {
   40B1 01 8B 5E      [10]  232 	ld	bc, #_g_enemies+0
   40B4 1E 00         [ 7]  233 	ld	e, #0x00
   40B6                     234 00117$:
                            235 ;src/game.c:60: enemyinit(&g_enemies[i]);
   40B6 D5            [11]  236 	push	de
   40B7 16 00         [ 7]  237 	ld	d,#0x00
   40B9 6B            [ 4]  238 	ld	l, e
   40BA 62            [ 4]  239 	ld	h, d
   40BB 29            [11]  240 	add	hl, hl
   40BC 29            [11]  241 	add	hl, hl
   40BD 19            [11]  242 	add	hl, de
   40BE 29            [11]  243 	add	hl, hl
   40BF D1            [10]  244 	pop	de
   40C0 09            [11]  245 	add	hl, bc
   40C1 C5            [11]  246 	push	bc
   40C2 D5            [11]  247 	push	de
   40C3 E5            [11]  248 	push	hl
   40C4 CD 5D 51      [17]  249 	call	_enemyinit
   40C7 F1            [10]  250 	pop	af
   40C8 D1            [10]  251 	pop	de
   40C9 C1            [10]  252 	pop	bc
                            253 ;src/game.c:59: for (i = 0; i < MAX_ENEMIES; ++i) {
   40CA 1C            [ 4]  254 	inc	e
   40CB 7B            [ 4]  255 	ld	a, e
   40CC D6 06         [ 7]  256 	sub	a, #0x06
   40CE 38 E6         [12]  257 	jr	C,00117$
                            258 ;src/game.c:64: else if (wave == 1) count = 3;
   40D0 DD 7E 04      [19]  259 	ld	a, 4 (ix)
   40D3 3D            [ 4]  260 	dec	a
   40D4 20 04         [12]  261 	jr	NZ,00190$
   40D6 3E 01         [ 7]  262 	ld	a,#0x01
   40D8 18 01         [12]  263 	jr	00191$
   40DA                     264 00190$:
   40DA AF            [ 4]  265 	xor	a,a
   40DB                     266 00191$:
   40DB 5F            [ 4]  267 	ld	e, a
                            268 ;src/game.c:63: if (wave == 0) count = 2;
   40DC DD 7E 04      [19]  269 	ld	a, 4 (ix)
   40DF B7            [ 4]  270 	or	a, a
   40E0 20 06         [12]  271 	jr	NZ,00106$
   40E2 DD 36 FC 02   [19]  272 	ld	-4 (ix), #0x02
   40E6 18 0E         [12]  273 	jr	00107$
   40E8                     274 00106$:
                            275 ;src/game.c:64: else if (wave == 1) count = 3;
   40E8 7B            [ 4]  276 	ld	a, e
   40E9 B7            [ 4]  277 	or	a, a
   40EA 28 06         [12]  278 	jr	Z,00103$
   40EC DD 36 FC 03   [19]  279 	ld	-4 (ix), #0x03
   40F0 18 04         [12]  280 	jr	00107$
   40F2                     281 00103$:
                            282 ;src/game.c:65: else count = 4;
   40F2 DD 36 FC 04   [19]  283 	ld	-4 (ix), #0x04
   40F6                     284 00107$:
                            285 ;src/game.c:67: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F6 3E 06         [ 7]  286 	ld	a, #0x06
   40F8 DD 96 FC      [19]  287 	sub	a, -4 (ix)
   40FB 30 04         [12]  288 	jr	NC,00148$
   40FD DD 36 FC 06   [19]  289 	ld	-4 (ix), #0x06
                            290 ;src/game.c:69: for (i = 0; i < count; ++i) {
   4101                     291 00148$:
   4101 DD 73 FF      [19]  292 	ld	-1 (ix), e
   4104 DD 36 FB 00   [19]  293 	ld	-5 (ix), #0x00
   4108                     294 00120$:
   4108 DD 7E FB      [19]  295 	ld	a, -5 (ix)
   410B DD 96 FC      [19]  296 	sub	a, -4 (ix)
   410E D2 9B 41      [10]  297 	jp	NC, 00116$
                            298 ;src/game.c:72: if (wave == 0) type = 0;
   4111 DD 7E 04      [19]  299 	ld	a, 4 (ix)
   4114 B7            [ 4]  300 	or	a,a
   4115 20 03         [12]  301 	jr	NZ,00114$
   4117 5F            [ 4]  302 	ld	e,a
   4118 18 27         [12]  303 	jr	00115$
   411A                     304 00114$:
                            305 ;src/game.c:73: else if (wave == 1) type = (u8)((i == 0) ? 1 : 0);
   411A DD 7E FF      [19]  306 	ld	a, -1 (ix)
   411D B7            [ 4]  307 	or	a, a
   411E 28 0E         [12]  308 	jr	Z,00111$
   4120 DD 7E FB      [19]  309 	ld	a, -5 (ix)
   4123 B7            [ 4]  310 	or	a, a
   4124 20 04         [12]  311 	jr	NZ,00124$
   4126 1E 01         [ 7]  312 	ld	e, #0x01
   4128 18 17         [12]  313 	jr	00115$
   412A                     314 00124$:
   412A 1E 00         [ 7]  315 	ld	e, #0x00
   412C 18 13         [12]  316 	jr	00115$
   412E                     317 00111$:
                            318 ;src/game.c:74: else type = (u8)((i == 0 || i == 3) ? 2 : 1);
   412E DD 7E FB      [19]  319 	ld	a, -5 (ix)
   4131 B7            [ 4]  320 	or	a, a
   4132 28 07         [12]  321 	jr	Z,00129$
   4134 DD 7E FB      [19]  322 	ld	a, -5 (ix)
   4137 D6 03         [ 7]  323 	sub	a, #0x03
   4139 20 04         [12]  324 	jr	NZ,00126$
   413B                     325 00129$:
   413B 1E 02         [ 7]  326 	ld	e, #0x02
   413D 18 02         [12]  327 	jr	00127$
   413F                     328 00126$:
   413F 1E 01         [ 7]  329 	ld	e, #0x01
   4141                     330 00127$:
   4141                     331 00115$:
                            332 ;src/game.c:76: spawn_y = (type == 2) ? 84 : 112;
   4141 7B            [ 4]  333 	ld	a, e
   4142 D6 02         [ 7]  334 	sub	a, #0x02
   4144 20 04         [12]  335 	jr	NZ,00131$
   4146 16 54         [ 7]  336 	ld	d, #0x54
   4148 18 02         [12]  337 	jr	00132$
   414A                     338 00131$:
   414A 16 70         [ 7]  339 	ld	d, #0x70
   414C                     340 00132$:
                            341 ;src/game.c:77: enemyspawn(&g_enemies[i], (u8)(46 + (i * 8)), spawn_y, type, (u8)((i & 1) ? 1 : 0));
   414C DD CB FB 46   [20]  342 	bit	0, -5 (ix)
   4150 28 06         [12]  343 	jr	Z,00133$
   4152 DD 36 FE 01   [19]  344 	ld	-2 (ix), #0x01
   4156 18 04         [12]  345 	jr	00134$
   4158                     346 00133$:
   4158 DD 36 FE 00   [19]  347 	ld	-2 (ix), #0x00
   415C                     348 00134$:
   415C DD 7E FB      [19]  349 	ld	a, -5 (ix)
   415F 07            [ 4]  350 	rlca
   4160 07            [ 4]  351 	rlca
   4161 07            [ 4]  352 	rlca
   4162 E6 F8         [ 7]  353 	and	a, #0xf8
   4164 C6 2E         [ 7]  354 	add	a, #0x2e
   4166 DD 77 FD      [19]  355 	ld	-3 (ix), a
   4169 D5            [11]  356 	push	de
   416A DD 5E FB      [19]  357 	ld	e,-5 (ix)
   416D 16 00         [ 7]  358 	ld	d,#0x00
   416F 6B            [ 4]  359 	ld	l, e
   4170 62            [ 4]  360 	ld	h, d
   4171 29            [11]  361 	add	hl, hl
   4172 29            [11]  362 	add	hl, hl
   4173 19            [11]  363 	add	hl, de
   4174 29            [11]  364 	add	hl, hl
   4175 D1            [10]  365 	pop	de
   4176 09            [11]  366 	add	hl, bc
   4177 E5            [11]  367 	push	hl
   4178 FD E1         [14]  368 	pop	iy
   417A C5            [11]  369 	push	bc
   417B DD 7E FE      [19]  370 	ld	a, -2 (ix)
   417E F5            [11]  371 	push	af
   417F 33            [ 6]  372 	inc	sp
   4180 7B            [ 4]  373 	ld	a, e
   4181 F5            [11]  374 	push	af
   4182 33            [ 6]  375 	inc	sp
   4183 D5            [11]  376 	push	de
   4184 33            [ 6]  377 	inc	sp
   4185 DD 7E FD      [19]  378 	ld	a, -3 (ix)
   4188 F5            [11]  379 	push	af
   4189 33            [ 6]  380 	inc	sp
   418A FD E5         [15]  381 	push	iy
   418C CD A2 51      [17]  382 	call	_enemyspawn
   418F 21 06 00      [10]  383 	ld	hl, #6
   4192 39            [11]  384 	add	hl, sp
   4193 F9            [ 6]  385 	ld	sp, hl
   4194 C1            [10]  386 	pop	bc
                            387 ;src/game.c:69: for (i = 0; i < count; ++i) {
   4195 DD 34 FB      [23]  388 	inc	-5 (ix)
   4198 C3 08 41      [10]  389 	jp	00120$
   419B                     390 00116$:
                            391 ;src/game.c:80: g_aliveenemies = count;
   419B DD 7E FC      [19]  392 	ld	a, -4 (ix)
   419E 32 09 5F      [13]  393 	ld	(#_g_aliveenemies + 0),a
   41A1 DD F9         [10]  394 	ld	sp, ix
   41A3 DD E1         [14]  395 	pop	ix
   41A5 C9            [10]  396 	ret
                            397 ;src/game.c:83: static void spawn_boss(void) {
                            398 ;	---------------------------------
                            399 ; Function spawn_boss
                            400 ; ---------------------------------
   41A6                     401 _spawn_boss:
                            402 ;src/game.c:84: enemyinit(&g_boss);
   41A6 21 14 5F      [10]  403 	ld	hl, #_g_boss
   41A9 E5            [11]  404 	push	hl
   41AA CD 5D 51      [17]  405 	call	_enemyinit
   41AD F1            [10]  406 	pop	af
                            407 ;src/game.c:85: enemyspawn(&g_boss, 68, 112, 1, 0);
   41AE 21 01 00      [10]  408 	ld	hl, #0x0001
   41B1 E5            [11]  409 	push	hl
   41B2 21 44 70      [10]  410 	ld	hl, #0x7044
   41B5 E5            [11]  411 	push	hl
   41B6 21 14 5F      [10]  412 	ld	hl, #_g_boss
   41B9 E5            [11]  413 	push	hl
   41BA CD A2 51      [17]  414 	call	_enemyspawn
   41BD 21 06 00      [10]  415 	ld	hl, #6
   41C0 39            [11]  416 	add	hl, sp
   41C1 F9            [ 6]  417 	ld	sp, hl
                            418 ;src/game.c:86: g_boss.w = 10;
   41C2 21 18 5F      [10]  419 	ld	hl, #(_g_boss + 0x0004)
   41C5 36 0A         [10]  420 	ld	(hl), #0x0a
                            421 ;src/game.c:87: g_boss.h = 18;
   41C7 21 19 5F      [10]  422 	ld	hl, #(_g_boss + 0x0005)
   41CA 36 12         [10]  423 	ld	(hl), #0x12
                            424 ;src/game.c:88: g_boss.health = 10;
   41CC 21 1B 5F      [10]  425 	ld	hl, #(_g_boss + 0x0007)
   41CF 36 0A         [10]  426 	ld	(hl), #0x0a
                            427 ;src/game.c:89: g_boss.reward = 1500;
   41D1 21 1C 5F      [10]  428 	ld	hl, #(_g_boss + 0x0008)
   41D4 36 DC         [10]  429 	ld	(hl), #0xdc
                            430 ;src/game.c:90: g_boss.kind = 3;
   41D6 21 1D 5F      [10]  431 	ld	hl, #(_g_boss + 0x0009)
   41D9 36 03         [10]  432 	ld	(hl), #0x03
                            433 ;src/game.c:91: g_boss.vx = -1;
   41DB 21 16 5F      [10]  434 	ld	hl, #(_g_boss + 0x0002)
   41DE 36 FF         [10]  435 	ld	(hl), #0xff
                            436 ;src/game.c:92: g_bossactive = 1;
   41E0 21 1E 5F      [10]  437 	ld	hl,#_g_bossactive + 0
   41E3 36 01         [10]  438 	ld	(hl), #0x01
                            439 ;src/game.c:93: g_bossphase = 0;
   41E5 21 1F 5F      [10]  440 	ld	hl,#_g_bossphase + 0
   41E8 36 00         [10]  441 	ld	(hl), #0x00
   41EA C9            [10]  442 	ret
                            443 ;src/game.c:96: static void try_fire_projectile(void) {
                            444 ;	---------------------------------
                            445 ; Function try_fire_projectile
                            446 ; ---------------------------------
   41EB                     447 _try_fire_projectile:
   41EB DD E5         [15]  448 	push	ix
   41ED DD 21 00 00   [14]  449 	ld	ix,#0
   41F1 DD 39         [15]  450 	add	ix,sp
   41F3 F5            [11]  451 	push	af
   41F4 3B            [ 6]  452 	dec	sp
                            453 ;src/game.c:100: if (!input_is_shoot_just_pressed()) return;
   41F5 CD AD 4F      [17]  454 	call	_input_is_shoot_just_pressed
   41F8 7D            [ 4]  455 	ld	a, l
   41F9 B7            [ 4]  456 	or	a, a
   41FA CA 8C 42      [10]  457 	jp	Z,00110$
                            458 ;src/game.c:101: if (g_shootcooldown) return;
   41FD 3A 0C 5F      [13]  459 	ld	a,(#_g_shootcooldown + 0)
   4200 B7            [ 4]  460 	or	a, a
   4201 C2 8C 42      [10]  461 	jp	NZ,00110$
                            462 ;src/game.c:103: dir = g_player.facing_left ? -3 : 3;
   4204 3A 89 5E      [13]  463 	ld	a, (#_g_player + 7)
   4207 B7            [ 4]  464 	or	a, a
   4208 28 04         [12]  465 	jr	Z,00112$
   420A 0E FD         [ 7]  466 	ld	c, #0xfd
   420C 18 02         [12]  467 	jr	00113$
   420E                     468 00112$:
   420E 0E 03         [ 7]  469 	ld	c, #0x03
   4210                     470 00113$:
                            471 ;src/game.c:105: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4210 DD 36 FD 00   [19]  472 	ld	-3 (ix), #0x00
   4214 06 00         [ 7]  473 	ld	b, #0x00
   4216                     474 00108$:
                            475 ;src/game.c:106: if (!g_projectiles[i].active) {
   4216 58            [ 4]  476 	ld	e,b
   4217 16 00         [ 7]  477 	ld	d,#0x00
   4219 6B            [ 4]  478 	ld	l, e
   421A 62            [ 4]  479 	ld	h, d
   421B 29            [11]  480 	add	hl, hl
   421C 29            [11]  481 	add	hl, hl
   421D 19            [11]  482 	add	hl, de
   421E 29            [11]  483 	add	hl, hl
   421F 11 C7 5E      [10]  484 	ld	de, #_g_projectiles
   4222 19            [11]  485 	add	hl, de
   4223 11 06 00      [10]  486 	ld	de, #0x0006
   4226 19            [11]  487 	add	hl, de
   4227 7E            [ 7]  488 	ld	a, (hl)
   4228 B7            [ 4]  489 	or	a, a
   4229 20 58         [12]  490 	jr	NZ,00109$
                            491 ;src/game.c:108: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel > 0 ? 1 : 0);
   422B 3A 20 5F      [13]  492 	ld	a,(#_g_weaponlevel + 0)
   422E B7            [ 4]  493 	or	a, a
   422F 28 06         [12]  494 	jr	Z,00114$
   4231 DD 36 FF 01   [19]  495 	ld	-1 (ix), #0x01
   4235 18 04         [12]  496 	jr	00115$
   4237                     497 00114$:
   4237 DD 36 FF 00   [19]  498 	ld	-1 (ix), #0x00
   423B                     499 00115$:
   423B 3A 83 5E      [13]  500 	ld	a, (#_g_player + 1)
   423E C6 06         [ 7]  501 	add	a, #0x06
   4240 DD 77 FE      [19]  502 	ld	-2 (ix), a
   4243 21 82 5E      [10]  503 	ld	hl, #_g_player + 0
   4246 46            [ 7]  504 	ld	b, (hl)
   4247 04            [ 4]  505 	inc	b
   4248 04            [ 4]  506 	inc	b
   4249 DD 5E FD      [19]  507 	ld	e,-3 (ix)
   424C 16 00         [ 7]  508 	ld	d,#0x00
   424E 6B            [ 4]  509 	ld	l, e
   424F 62            [ 4]  510 	ld	h, d
   4250 29            [11]  511 	add	hl, hl
   4251 29            [11]  512 	add	hl, hl
   4252 19            [11]  513 	add	hl, de
   4253 29            [11]  514 	add	hl, hl
   4254 11 C7 5E      [10]  515 	ld	de, #_g_projectiles
   4257 19            [11]  516 	add	hl, de
   4258 EB            [ 4]  517 	ex	de,hl
   4259 DD 7E FF      [19]  518 	ld	a, -1 (ix)
   425C F5            [11]  519 	push	af
   425D 33            [ 6]  520 	inc	sp
   425E 79            [ 4]  521 	ld	a, c
   425F F5            [11]  522 	push	af
   4260 33            [ 6]  523 	inc	sp
   4261 DD 7E FE      [19]  524 	ld	a, -2 (ix)
   4264 F5            [11]  525 	push	af
   4265 33            [ 6]  526 	inc	sp
   4266 C5            [11]  527 	push	bc
   4267 33            [ 6]  528 	inc	sp
   4268 D5            [11]  529 	push	de
   4269 CD 6A 5A      [17]  530 	call	_projectilefire
   426C 21 06 00      [10]  531 	ld	hl, #6
   426F 39            [11]  532 	add	hl, sp
   4270 F9            [ 6]  533 	ld	sp, hl
                            534 ;src/game.c:109: g_shootcooldown = g_weaponlevel > 0 ? 4 : 8;
   4271 3A 20 5F      [13]  535 	ld	a,(#_g_weaponlevel + 0)
   4274 B7            [ 4]  536 	or	a, a
   4275 28 04         [12]  537 	jr	Z,00116$
   4277 0E 04         [ 7]  538 	ld	c, #0x04
   4279 18 02         [12]  539 	jr	00117$
   427B                     540 00116$:
   427B 0E 08         [ 7]  541 	ld	c, #0x08
   427D                     542 00117$:
   427D 21 0C 5F      [10]  543 	ld	hl,#_g_shootcooldown + 0
   4280 71            [ 7]  544 	ld	(hl), c
                            545 ;src/game.c:110: break;
   4281 18 09         [12]  546 	jr	00110$
   4283                     547 00109$:
                            548 ;src/game.c:105: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4283 04            [ 4]  549 	inc	b
   4284 DD 70 FD      [19]  550 	ld	-3 (ix), b
   4287 78            [ 4]  551 	ld	a, b
   4288 D6 06         [ 7]  552 	sub	a, #0x06
   428A 38 8A         [12]  553 	jr	C,00108$
   428C                     554 00110$:
   428C DD F9         [10]  555 	ld	sp, ix
   428E DD E1         [14]  556 	pop	ix
   4290 C9            [10]  557 	ret
                            558 ;src/game.c:115: static void register_player_hit(void) {
                            559 ;	---------------------------------
                            560 ; Function register_player_hit
                            561 ; ---------------------------------
   4291                     562 _register_player_hit:
                            563 ;src/game.c:116: if (g_lives) {
   4291 FD 21 03 5F   [14]  564 	ld	iy, #_g_lives
   4295 FD 7E 00      [19]  565 	ld	a, 0 (iy)
   4298 B7            [ 4]  566 	or	a, a
   4299 28 03         [12]  567 	jr	Z,00102$
                            568 ;src/game.c:117: g_lives--;
   429B FD 35 00      [23]  569 	dec	0 (iy)
   429E                     570 00102$:
                            571 ;src/game.c:119: if (g_lives == 0) {
   429E 3A 03 5F      [13]  572 	ld	a,(#_g_lives + 0)
   42A1 B7            [ 4]  573 	or	a, a
   42A2 20 06         [12]  574 	jr	NZ,00104$
                            575 ;src/game.c:120: g_gameover = 1;
   42A4 21 0E 5F      [10]  576 	ld	hl,#_g_gameover + 0
   42A7 36 01         [10]  577 	ld	(hl), #0x01
                            578 ;src/game.c:121: return;
   42A9 C9            [10]  579 	ret
   42AA                     580 00104$:
                            581 ;src/game.c:124: reset_player_to_checkpoint();
   42AA CD 00 40      [17]  582 	call	_reset_player_to_checkpoint
                            583 ;src/game.c:125: g_damagecooldown = 40;
   42AD 21 0B 5F      [10]  584 	ld	hl,#_g_damagecooldown + 0
   42B0 36 28         [10]  585 	ld	(hl), #0x28
   42B2 C9            [10]  586 	ret
                            587 ;src/game.c:128: void game_init(void) {
                            588 ;	---------------------------------
                            589 ; Function game_init
                            590 ; ---------------------------------
   42B3                     591 _game_init::
                            592 ;src/game.c:131: cpct_disableFirmware();
   42B3 CD 99 5D      [17]  593 	call	_cpct_disableFirmware
                            594 ;src/game.c:132: cpct_setVideoMode(1);
   42B6 2E 01         [ 7]  595 	ld	l, #0x01
   42B8 CD 7D 5D      [17]  596 	call	_cpct_setVideoMode
                            597 ;src/game.c:133: cpct_clearScreen(0x00);
   42BB 21 00 40      [10]  598 	ld	hl, #0x4000
   42BE E5            [11]  599 	push	hl
   42BF AF            [ 4]  600 	xor	a, a
   42C0 F5            [11]  601 	push	af
   42C1 33            [ 6]  602 	inc	sp
   42C2 26 C0         [ 7]  603 	ld	h, #0xc0
   42C4 E5            [11]  604 	push	hl
   42C5 CD 8B 5D      [17]  605 	call	_cpct_memset
                            606 ;src/game.c:134: tilemap_init();
   42C8 CD BF 4F      [17]  607 	call	_tilemap_init
                            608 ;src/game.c:135: collision_init();
   42CB CD 01 4B      [17]  609 	call	_collision_init
                            610 ;src/game.c:136: playerinit(&g_player);
   42CE 21 82 5E      [10]  611 	ld	hl, #_g_player
   42D1 E5            [11]  612 	push	hl
   42D2 CD 2F 56      [17]  613 	call	_playerinit
   42D5 F1            [10]  614 	pop	af
                            615 ;src/game.c:137: hudinit();
   42D6 CD 07 4E      [17]  616 	call	_hudinit
                            617 ;src/game.c:139: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42D9 0E 00         [ 7]  618 	ld	c, #0x00
   42DB                     619 00102$:
                            620 ;src/game.c:140: projectileinit(&g_projectiles[i]);
   42DB 06 00         [ 7]  621 	ld	b,#0x00
   42DD 69            [ 4]  622 	ld	l, c
   42DE 60            [ 4]  623 	ld	h, b
   42DF 29            [11]  624 	add	hl, hl
   42E0 29            [11]  625 	add	hl, hl
   42E1 09            [11]  626 	add	hl, bc
   42E2 29            [11]  627 	add	hl, hl
   42E3 11 C7 5E      [10]  628 	ld	de, #_g_projectiles
   42E6 19            [11]  629 	add	hl, de
   42E7 C5            [11]  630 	push	bc
   42E8 E5            [11]  631 	push	hl
   42E9 CD 25 5A      [17]  632 	call	_projectileinit
   42EC F1            [10]  633 	pop	af
   42ED C1            [10]  634 	pop	bc
                            635 ;src/game.c:139: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42EE 0C            [ 4]  636 	inc	c
   42EF 79            [ 4]  637 	ld	a, c
   42F0 D6 06         [ 7]  638 	sub	a, #0x06
   42F2 38 E7         [12]  639 	jr	C,00102$
                            640 ;src/game.c:143: g_lives = 3;
   42F4 21 03 5F      [10]  641 	ld	hl,#_g_lives + 0
   42F7 36 03         [10]  642 	ld	(hl), #0x03
                            643 ;src/game.c:144: g_score = 0;
   42F9 21 00 00      [10]  644 	ld	hl, #0x0000
   42FC 22 04 5F      [16]  645 	ld	(_g_score), hl
                            646 ;src/game.c:145: g_timeleft = 99;
   42FF FD 21 06 5F   [14]  647 	ld	iy, #_g_timeleft
   4303 FD 36 00 63   [19]  648 	ld	0 (iy), #0x63
                            649 ;src/game.c:146: g_weapondisplay = 1;
   4307 FD 21 07 5F   [14]  650 	ld	iy, #_g_weapondisplay
   430B FD 36 00 01   [19]  651 	ld	0 (iy), #0x01
                            652 ;src/game.c:147: g_currentwave = 0;
   430F FD 21 08 5F   [14]  653 	ld	iy, #_g_currentwave
   4313 FD 36 00 00   [19]  654 	ld	0 (iy), #0x00
                            655 ;src/game.c:148: g_wavecooldown = 1;
   4317 FD 21 0A 5F   [14]  656 	ld	iy, #_g_wavecooldown
   431B FD 36 00 01   [19]  657 	ld	0 (iy), #0x01
                            658 ;src/game.c:149: g_damagecooldown = 0;
   431F FD 21 0B 5F   [14]  659 	ld	iy, #_g_damagecooldown
   4323 FD 36 00 00   [19]  660 	ld	0 (iy), #0x00
                            661 ;src/game.c:150: g_shootcooldown = 0;
   4327 FD 21 0C 5F   [14]  662 	ld	iy, #_g_shootcooldown
   432B FD 36 00 00   [19]  663 	ld	0 (iy), #0x00
                            664 ;src/game.c:151: g_victory = 0;
   432F FD 21 0D 5F   [14]  665 	ld	iy, #_g_victory
   4333 FD 36 00 00   [19]  666 	ld	0 (iy), #0x00
                            667 ;src/game.c:152: g_gameover = 0;
   4337 FD 21 0E 5F   [14]  668 	ld	iy, #_g_gameover
   433B FD 36 00 00   [19]  669 	ld	0 (iy), #0x00
                            670 ;src/game.c:153: g_framecounter = 0;
   433F 2E 00         [ 7]  671 	ld	l, #0x00
   4341 22 0F 5F      [16]  672 	ld	(_g_framecounter), hl
                            673 ;src/game.c:154: g_checkpointx = 20;
   4344 21 11 5F      [10]  674 	ld	hl,#_g_checkpointx + 0
   4347 36 14         [10]  675 	ld	(hl), #0x14
                            676 ;src/game.c:155: g_checkpointy = 120;
   4349 21 12 5F      [10]  677 	ld	hl,#_g_checkpointy + 0
   434C 36 78         [10]  678 	ld	(hl), #0x78
                            679 ;src/game.c:156: g_checkpointactive = 0;
   434E 21 13 5F      [10]  680 	ld	hl,#_g_checkpointactive + 0
   4351 36 00         [10]  681 	ld	(hl), #0x00
                            682 ;src/game.c:157: g_bossactive = 0;
   4353 21 1E 5F      [10]  683 	ld	hl,#_g_bossactive + 0
   4356 36 00         [10]  684 	ld	(hl), #0x00
                            685 ;src/game.c:158: g_weaponlevel = 0;
   4358 21 20 5F      [10]  686 	ld	hl,#_g_weaponlevel + 0
   435B 36 00         [10]  687 	ld	(hl), #0x00
                            688 ;src/game.c:159: g_pickuptaken = 0;
   435D 21 21 5F      [10]  689 	ld	hl,#_g_pickuptaken + 0
   4360 36 00         [10]  690 	ld	(hl), #0x00
                            691 ;src/game.c:160: enemyinit(&g_boss);
   4362 21 14 5F      [10]  692 	ld	hl, #_g_boss
   4365 E5            [11]  693 	push	hl
   4366 CD 5D 51      [17]  694 	call	_enemyinit
   4369 F1            [10]  695 	pop	af
   436A C9            [10]  696 	ret
                            697 ;src/game.c:163: void game_update(void) {
                            698 ;	---------------------------------
                            699 ; Function game_update
                            700 ; ---------------------------------
   436B                     701 _game_update::
   436B DD E5         [15]  702 	push	ix
   436D DD 21 00 00   [14]  703 	ld	ix,#0
   4371 DD 39         [15]  704 	add	ix,sp
   4373 21 E7 FF      [10]  705 	ld	hl, #-25
   4376 39            [11]  706 	add	hl, sp
   4377 F9            [ 6]  707 	ld	sp, hl
                            708 ;src/game.c:167: input_update();
   4378 CD 1A 4F      [17]  709 	call	_input_update
                            710 ;src/game.c:169: if (g_gameover || g_victory) {
   437B 3A 0E 5F      [13]  711 	ld	a,(#_g_gameover + 0)
   437E B7            [ 4]  712 	or	a, a
   437F 20 06         [12]  713 	jr	NZ,00101$
   4381 3A 0D 5F      [13]  714 	ld	a,(#_g_victory + 0)
   4384 B7            [ 4]  715 	or	a, a
   4385 28 1C         [12]  716 	jr	Z,00102$
   4387                     717 00101$:
                            718 ;src/game.c:170: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4387 3A 07 5F      [13]  719 	ld	a, (_g_weapondisplay)
   438A F5            [11]  720 	push	af
   438B 33            [ 6]  721 	inc	sp
   438C 3A 06 5F      [13]  722 	ld	a, (_g_timeleft)
   438F F5            [11]  723 	push	af
   4390 33            [ 6]  724 	inc	sp
   4391 2A 04 5F      [16]  725 	ld	hl, (_g_score)
   4394 E5            [11]  726 	push	hl
   4395 3A 03 5F      [13]  727 	ld	a, (_g_lives)
   4398 F5            [11]  728 	push	af
   4399 33            [ 6]  729 	inc	sp
   439A CD 22 4E      [17]  730 	call	_hudupdate
   439D F1            [10]  731 	pop	af
   439E F1            [10]  732 	pop	af
   439F 33            [ 6]  733 	inc	sp
                            734 ;src/game.c:171: return;
   43A0 C3 8C 49      [10]  735 	jp	00181$
   43A3                     736 00102$:
                            737 ;src/game.c:174: playerupdate(&g_player);
   43A3 21 82 5E      [10]  738 	ld	hl, #_g_player
   43A6 E5            [11]  739 	push	hl
   43A7 CD 76 56      [17]  740 	call	_playerupdate
   43AA F1            [10]  741 	pop	af
                            742 ;src/game.c:175: try_fire_projectile();
   43AB CD EB 41      [17]  743 	call	_try_fire_projectile
                            744 ;src/game.c:177: if (g_shootcooldown) g_shootcooldown--;
   43AE FD 21 0C 5F   [14]  745 	ld	iy, #_g_shootcooldown
   43B2 FD 7E 00      [19]  746 	ld	a, 0 (iy)
   43B5 B7            [ 4]  747 	or	a, a
   43B6 28 03         [12]  748 	jr	Z,00105$
   43B8 FD 35 00      [23]  749 	dec	0 (iy)
   43BB                     750 00105$:
                            751 ;src/game.c:178: if (g_damagecooldown) g_damagecooldown--;
   43BB FD 21 0B 5F   [14]  752 	ld	iy, #_g_damagecooldown
   43BF FD 7E 00      [19]  753 	ld	a, 0 (iy)
   43C2 B7            [ 4]  754 	or	a, a
   43C3 28 03         [12]  755 	jr	Z,00192$
   43C5 FD 35 00      [23]  756 	dec	0 (iy)
                            757 ;src/game.c:180: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43C8                     758 00192$:
   43C8 0E 00         [ 7]  759 	ld	c, #0x00
   43CA                     760 00174$:
                            761 ;src/game.c:181: projectileupdate(&g_projectiles[i]);
   43CA 06 00         [ 7]  762 	ld	b,#0x00
   43CC 69            [ 4]  763 	ld	l, c
   43CD 60            [ 4]  764 	ld	h, b
   43CE 29            [11]  765 	add	hl, hl
   43CF 29            [11]  766 	add	hl, hl
   43D0 09            [11]  767 	add	hl, bc
   43D1 29            [11]  768 	add	hl, hl
   43D2 11 C7 5E      [10]  769 	ld	de, #_g_projectiles
   43D5 19            [11]  770 	add	hl, de
   43D6 C5            [11]  771 	push	bc
   43D7 E5            [11]  772 	push	hl
   43D8 CD 28 5B      [17]  773 	call	_projectileupdate
   43DB F1            [10]  774 	pop	af
   43DC C1            [10]  775 	pop	bc
                            776 ;src/game.c:180: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43DD 0C            [ 4]  777 	inc	c
   43DE 79            [ 4]  778 	ld	a, c
   43DF D6 06         [ 7]  779 	sub	a, #0x06
   43E1 38 E7         [12]  780 	jr	C,00174$
                            781 ;src/game.c:184: for (i = 0; i < MAX_ENEMIES; ++i) {
   43E3 0E 00         [ 7]  782 	ld	c, #0x00
   43E5                     783 00176$:
                            784 ;src/game.c:185: enemyupdate(&g_enemies[i]);
   43E5 06 00         [ 7]  785 	ld	b,#0x00
   43E7 69            [ 4]  786 	ld	l, c
   43E8 60            [ 4]  787 	ld	h, b
   43E9 29            [11]  788 	add	hl, hl
   43EA 29            [11]  789 	add	hl, hl
   43EB 09            [11]  790 	add	hl, bc
   43EC 29            [11]  791 	add	hl, hl
   43ED 11 8B 5E      [10]  792 	ld	de, #_g_enemies
   43F0 19            [11]  793 	add	hl, de
   43F1 C5            [11]  794 	push	bc
   43F2 E5            [11]  795 	push	hl
   43F3 CD 7A 53      [17]  796 	call	_enemyupdate
   43F6 F1            [10]  797 	pop	af
   43F7 C1            [10]  798 	pop	bc
                            799 ;src/game.c:184: for (i = 0; i < MAX_ENEMIES; ++i) {
   43F8 0C            [ 4]  800 	inc	c
   43F9 79            [ 4]  801 	ld	a, c
   43FA D6 06         [ 7]  802 	sub	a, #0x06
   43FC 38 E7         [12]  803 	jr	C,00176$
                            804 ;src/game.c:188: if (g_bossactive) {
   43FE 3A 1E 5F      [13]  805 	ld	a,(#_g_bossactive + 0)
   4401 B7            [ 4]  806 	or	a, a
   4402 28 71         [12]  807 	jr	Z,00211$
                            808 ;src/game.c:189: if (g_boss.health > 4) g_bossphase = 0;
   4404 21 1B 5F      [10]  809 	ld	hl, #_g_boss + 7
   4407 4E            [ 7]  810 	ld	c, (hl)
   4408 3E 04         [ 7]  811 	ld	a, #0x04
   440A 91            [ 4]  812 	sub	a, c
   440B 30 07         [12]  813 	jr	NC,00111$
   440D 21 1F 5F      [10]  814 	ld	hl,#_g_bossphase + 0
   4410 36 00         [10]  815 	ld	(hl), #0x00
   4412 18 05         [12]  816 	jr	00112$
   4414                     817 00111$:
                            818 ;src/game.c:190: else g_bossphase = 1;
   4414 21 1F 5F      [10]  819 	ld	hl,#_g_bossphase + 0
   4417 36 01         [10]  820 	ld	(hl), #0x01
   4419                     821 00112$:
                            822 ;src/game.c:192: g_boss.vx = (i8)(g_player.x + 2 < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   4419 3A 82 5E      [13]  823 	ld	a,(#_g_player + 0)
   441C DD 77 F9      [19]  824 	ld	-7 (ix), a
   441F DD 77 F7      [19]  825 	ld	-9 (ix), a
   4422 DD 36 F8 00   [19]  826 	ld	-8 (ix), #0x00
   4426 DD 7E F7      [19]  827 	ld	a, -9 (ix)
   4429 C6 02         [ 7]  828 	add	a, #0x02
   442B DD 77 F7      [19]  829 	ld	-9 (ix), a
   442E DD 7E F8      [19]  830 	ld	a, -8 (ix)
   4431 CE 00         [ 7]  831 	adc	a, #0x00
   4433 DD 77 F8      [19]  832 	ld	-8 (ix), a
   4436 21 14 5F      [10]  833 	ld	hl, #_g_boss + 0
   4439 4E            [ 7]  834 	ld	c, (hl)
   443A 06 00         [ 7]  835 	ld	b, #0x00
   443C DD 7E F7      [19]  836 	ld	a, -9 (ix)
   443F 91            [ 4]  837 	sub	a, c
   4440 DD 7E F8      [19]  838 	ld	a, -8 (ix)
   4443 98            [ 4]  839 	sbc	a, b
   4444 E2 49 44      [10]  840 	jp	PO, 00380$
   4447 EE 80         [ 7]  841 	xor	a, #0x80
   4449                     842 00380$:
   4449 F2 5D 44      [10]  843 	jp	P, 00183$
   444C 3A 1F 5F      [13]  844 	ld	a,(#_g_bossphase + 0)
   444F B7            [ 4]  845 	or	a, a
   4450 28 04         [12]  846 	jr	Z,00185$
   4452 0E 02         [ 7]  847 	ld	c, #0x02
   4454 18 02         [12]  848 	jr	00186$
   4456                     849 00185$:
   4456 0E 01         [ 7]  850 	ld	c, #0x01
   4458                     851 00186$:
   4458 AF            [ 4]  852 	xor	a, a
   4459 91            [ 4]  853 	sub	a, c
   445A 4F            [ 4]  854 	ld	c, a
   445B 18 0C         [12]  855 	jr	00184$
   445D                     856 00183$:
   445D 3A 1F 5F      [13]  857 	ld	a,(#_g_bossphase + 0)
   4460 B7            [ 4]  858 	or	a, a
   4461 28 04         [12]  859 	jr	Z,00187$
   4463 0E 02         [ 7]  860 	ld	c, #0x02
   4465 18 02         [12]  861 	jr	00188$
   4467                     862 00187$:
   4467 0E 01         [ 7]  863 	ld	c, #0x01
   4469                     864 00188$:
   4469                     865 00184$:
   4469 21 16 5F      [10]  866 	ld	hl, #(_g_boss + 0x0002)
   446C 71            [ 7]  867 	ld	(hl), c
                            868 ;src/game.c:193: enemyupdate(&g_boss);
   446D 21 14 5F      [10]  869 	ld	hl, #_g_boss
   4470 E5            [11]  870 	push	hl
   4471 CD 7A 53      [17]  871 	call	_enemyupdate
   4474 F1            [10]  872 	pop	af
                            873 ;src/game.c:196: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4475                     874 00211$:
   4475 0E 00         [ 7]  875 	ld	c, #0x00
   4477                     876 00179$:
                            877 ;src/game.c:197: if (!g_projectiles[i].active) continue;
   4477 06 00         [ 7]  878 	ld	b,#0x00
   4479 69            [ 4]  879 	ld	l, c
   447A 60            [ 4]  880 	ld	h, b
   447B 29            [11]  881 	add	hl, hl
   447C 29            [11]  882 	add	hl, hl
   447D 09            [11]  883 	add	hl, bc
   447E 29            [11]  884 	add	hl, hl
   447F EB            [ 4]  885 	ex	de,hl
   4480 21 C7 5E      [10]  886 	ld	hl, #_g_projectiles
   4483 19            [11]  887 	add	hl,de
   4484 EB            [ 4]  888 	ex	de,hl
   4485 21 06 00      [10]  889 	ld	hl, #0x0006
   4488 19            [11]  890 	add	hl,de
   4489 DD 75 F7      [19]  891 	ld	-9 (ix), l
   448C DD 74 F8      [19]  892 	ld	-8 (ix), h
   448F 7E            [ 7]  893 	ld	a, (hl)
   4490 B7            [ 4]  894 	or	a, a
   4491 CA B2 46      [10]  895 	jp	Z, 00133$
                            896 ;src/game.c:198: for (j = 0; j < MAX_ENEMIES; ++j) {
   4494 DD 36 E7 00   [19]  897 	ld	-25 (ix), #0x00
   4498                     898 00178$:
                            899 ;src/game.c:199: if (!g_enemies[j].active) continue;
   4498 D5            [11]  900 	push	de
   4499 DD 5E E7      [19]  901 	ld	e,-25 (ix)
   449C 16 00         [ 7]  902 	ld	d,#0x00
   449E 6B            [ 4]  903 	ld	l, e
   449F 62            [ 4]  904 	ld	h, d
   44A0 29            [11]  905 	add	hl, hl
   44A1 29            [11]  906 	add	hl, hl
   44A2 19            [11]  907 	add	hl, de
   44A3 29            [11]  908 	add	hl, hl
   44A4 D1            [10]  909 	pop	de
   44A5 3E 8B         [ 7]  910 	ld	a, #<(_g_enemies)
   44A7 85            [ 4]  911 	add	a, l
   44A8 DD 77 FC      [19]  912 	ld	-4 (ix), a
   44AB 3E 5E         [ 7]  913 	ld	a, #>(_g_enemies)
   44AD 8C            [ 4]  914 	adc	a, h
   44AE DD 77 FD      [19]  915 	ld	-3 (ix), a
   44B1 DD 6E FC      [19]  916 	ld	l,-4 (ix)
   44B4 DD 66 FD      [19]  917 	ld	h,-3 (ix)
   44B7 C5            [11]  918 	push	bc
   44B8 01 06 00      [10]  919 	ld	bc, #0x0006
   44BB 09            [11]  920 	add	hl, bc
   44BC C1            [10]  921 	pop	bc
   44BD 46            [ 7]  922 	ld	b, (hl)
                            923 ;src/game.c:200: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   44BE 21 05 00      [10]  924 	ld	hl, #0x0005
   44C1 19            [11]  925 	add	hl,de
   44C2 DD 75 FA      [19]  926 	ld	-6 (ix), l
   44C5 DD 74 FB      [19]  927 	ld	-5 (ix), h
   44C8 21 04 00      [10]  928 	ld	hl, #0x0004
   44CB 19            [11]  929 	add	hl,de
   44CC DD 75 FE      [19]  930 	ld	-2 (ix), l
   44CF DD 74 FF      [19]  931 	ld	-1 (ix), h
   44D2 21 01 00      [10]  932 	ld	hl, #0x0001
   44D5 19            [11]  933 	add	hl,de
   44D6 DD 75 F5      [19]  934 	ld	-11 (ix), l
   44D9 DD 74 F6      [19]  935 	ld	-10 (ix), h
                            936 ;src/game.c:202: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44DC 21 07 00      [10]  937 	ld	hl, #0x0007
   44DF 19            [11]  938 	add	hl,de
   44E0 DD 75 F3      [19]  939 	ld	-13 (ix), l
   44E3 DD 74 F4      [19]  940 	ld	-12 (ix), h
                            941 ;src/game.c:199: if (!g_enemies[j].active) continue;
   44E6 78            [ 4]  942 	ld	a, b
   44E7 B7            [ 4]  943 	or	a, a
   44E8 CA E0 45      [10]  944 	jp	Z, 00125$
                            945 ;src/game.c:201: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   44EB DD 6E FC      [19]  946 	ld	l,-4 (ix)
   44EE DD 66 FD      [19]  947 	ld	h,-3 (ix)
   44F1 23            [ 6]  948 	inc	hl
   44F2 23            [ 6]  949 	inc	hl
   44F3 23            [ 6]  950 	inc	hl
   44F4 23            [ 6]  951 	inc	hl
   44F5 23            [ 6]  952 	inc	hl
   44F6 7E            [ 7]  953 	ld	a, (hl)
   44F7 DD 77 F9      [19]  954 	ld	-7 (ix), a
   44FA DD 6E FC      [19]  955 	ld	l,-4 (ix)
   44FD DD 66 FD      [19]  956 	ld	h,-3 (ix)
   4500 23            [ 6]  957 	inc	hl
   4501 23            [ 6]  958 	inc	hl
   4502 23            [ 6]  959 	inc	hl
   4503 23            [ 6]  960 	inc	hl
   4504 7E            [ 7]  961 	ld	a, (hl)
   4505 DD 77 F2      [19]  962 	ld	-14 (ix), a
   4508 DD 6E FC      [19]  963 	ld	l,-4 (ix)
   450B DD 66 FD      [19]  964 	ld	h,-3 (ix)
   450E 23            [ 6]  965 	inc	hl
   450F 46            [ 7]  966 	ld	b, (hl)
   4510 DD 70 F0      [19]  967 	ld	-16 (ix), b
   4513 DD 36 F1 00   [19]  968 	ld	-15 (ix), #0x00
   4517 DD 6E FC      [19]  969 	ld	l,-4 (ix)
   451A DD 66 FD      [19]  970 	ld	h,-3 (ix)
   451D 46            [ 7]  971 	ld	b, (hl)
   451E DD 70 EE      [19]  972 	ld	-18 (ix), b
   4521 DD 36 EF 00   [19]  973 	ld	-17 (ix), #0x00
                            974 ;src/game.c:200: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4525 DD 6E FA      [19]  975 	ld	l,-6 (ix)
   4528 DD 66 FB      [19]  976 	ld	h,-5 (ix)
   452B 7E            [ 7]  977 	ld	a, (hl)
   452C DD 77 ED      [19]  978 	ld	-19 (ix), a
   452F DD 6E FE      [19]  979 	ld	l,-2 (ix)
   4532 DD 66 FF      [19]  980 	ld	h,-1 (ix)
   4535 46            [ 7]  981 	ld	b, (hl)
   4536 DD 6E F5      [19]  982 	ld	l,-11 (ix)
   4539 DD 66 F6      [19]  983 	ld	h,-10 (ix)
   453C 6E            [ 7]  984 	ld	l, (hl)
   453D DD 75 EB      [19]  985 	ld	-21 (ix), l
   4540 DD 36 EC 00   [19]  986 	ld	-20 (ix), #0x00
   4544 1A            [ 7]  987 	ld	a, (de)
   4545 DD 77 E9      [19]  988 	ld	-23 (ix), a
   4548 DD 36 EA 00   [19]  989 	ld	-22 (ix), #0x00
   454C C5            [11]  990 	push	bc
   454D D5            [11]  991 	push	de
   454E DD 66 F9      [19]  992 	ld	h, -7 (ix)
   4551 DD 6E F2      [19]  993 	ld	l, -14 (ix)
   4554 E5            [11]  994 	push	hl
   4555 DD 6E F0      [19]  995 	ld	l,-16 (ix)
   4558 DD 66 F1      [19]  996 	ld	h,-15 (ix)
   455B E5            [11]  997 	push	hl
   455C DD 6E EE      [19]  998 	ld	l,-18 (ix)
   455F DD 66 EF      [19]  999 	ld	h,-17 (ix)
   4562 E5            [11] 1000 	push	hl
   4563 DD 7E ED      [19] 1001 	ld	a, -19 (ix)
   4566 F5            [11] 1002 	push	af
   4567 33            [ 6] 1003 	inc	sp
   4568 C5            [11] 1004 	push	bc
   4569 33            [ 6] 1005 	inc	sp
   456A DD 6E EB      [19] 1006 	ld	l,-21 (ix)
   456D DD 66 EC      [19] 1007 	ld	h,-20 (ix)
   4570 E5            [11] 1008 	push	hl
   4571 DD 6E E9      [19] 1009 	ld	l,-23 (ix)
   4574 DD 66 EA      [19] 1010 	ld	h,-22 (ix)
   4577 E5            [11] 1011 	push	hl
   4578 CD 19 40      [17] 1012 	call	_rect_overlap
   457B FD 21 0C 00   [14] 1013 	ld	iy, #12
   457F FD 39         [15] 1014 	add	iy, sp
   4581 FD F9         [10] 1015 	ld	sp, iy
   4583 D1            [10] 1016 	pop	de
   4584 C1            [10] 1017 	pop	bc
   4585 7D            [ 4] 1018 	ld	a, l
   4586 B7            [ 4] 1019 	or	a, a
   4587 28 57         [12] 1020 	jr	Z,00125$
                           1021 ;src/game.c:202: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   4589 DD 6E F3      [19] 1022 	ld	l,-13 (ix)
   458C DD 66 F4      [19] 1023 	ld	h,-12 (ix)
   458F 66            [ 7] 1024 	ld	h, (hl)
   4590 DD 6E FC      [19] 1025 	ld	l, -4 (ix)
   4593 DD 46 FD      [19] 1026 	ld	b, -3 (ix)
   4596 C5            [11] 1027 	push	bc
   4597 D5            [11] 1028 	push	de
   4598 E5            [11] 1029 	push	hl
   4599 33            [ 6] 1030 	inc	sp
   459A 60            [ 4] 1031 	ld	h, b
   459B E5            [11] 1032 	push	hl
   459C CD EF 55      [17] 1033 	call	_enemydamage
   459F F1            [10] 1034 	pop	af
   45A0 33            [ 6] 1035 	inc	sp
   45A1 D1            [10] 1036 	pop	de
   45A2 C1            [10] 1037 	pop	bc
   45A3 7D            [ 4] 1038 	ld	a, l
   45A4 B7            [ 4] 1039 	or	a, a
   45A5 28 2F         [12] 1040 	jr	Z,00124$
                           1041 ;src/game.c:203: g_score = (u16)(g_score + g_enemies[j].reward);
   45A7 DD 6E FC      [19] 1042 	ld	l,-4 (ix)
   45AA DD 66 FD      [19] 1043 	ld	h,-3 (ix)
   45AD C5            [11] 1044 	push	bc
   45AE 01 08 00      [10] 1045 	ld	bc, #0x0008
   45B1 09            [11] 1046 	add	hl, bc
   45B2 C1            [10] 1047 	pop	bc
   45B3 6E            [ 7] 1048 	ld	l, (hl)
   45B4 DD 75 E9      [19] 1049 	ld	-23 (ix), l
   45B7 DD 36 EA 00   [19] 1050 	ld	-22 (ix), #0x00
   45BB 21 04 5F      [10] 1051 	ld	hl, #_g_score
   45BE 7E            [ 7] 1052 	ld	a, (hl)
   45BF DD 86 E9      [19] 1053 	add	a, -23 (ix)
   45C2 77            [ 7] 1054 	ld	(hl), a
   45C3 23            [ 6] 1055 	inc	hl
   45C4 7E            [ 7] 1056 	ld	a, (hl)
   45C5 DD 8E EA      [19] 1057 	adc	a, -22 (ix)
   45C8 77            [ 7] 1058 	ld	(hl), a
                           1059 ;src/game.c:204: if (g_aliveenemies) g_aliveenemies--;
   45C9 FD 21 09 5F   [14] 1060 	ld	iy, #_g_aliveenemies
   45CD FD 7E 00      [19] 1061 	ld	a, 0 (iy)
   45D0 B7            [ 4] 1062 	or	a, a
   45D1 28 03         [12] 1063 	jr	Z,00124$
   45D3 FD 35 00      [23] 1064 	dec	0 (iy)
   45D6                    1065 00124$:
                           1066 ;src/game.c:206: g_projectiles[i].active = 0;
   45D6 DD 6E F7      [19] 1067 	ld	l,-9 (ix)
   45D9 DD 66 F8      [19] 1068 	ld	h,-8 (ix)
   45DC 36 00         [10] 1069 	ld	(hl), #0x00
                           1070 ;src/game.c:207: break;
   45DE 18 0B         [12] 1071 	jr	00126$
   45E0                    1072 00125$:
                           1073 ;src/game.c:198: for (j = 0; j < MAX_ENEMIES; ++j) {
   45E0 DD 34 E7      [23] 1074 	inc	-25 (ix)
   45E3 DD 7E E7      [19] 1075 	ld	a, -25 (ix)
   45E6 D6 06         [ 7] 1076 	sub	a, #0x06
   45E8 DA 98 44      [10] 1077 	jp	C, 00178$
   45EB                    1078 00126$:
                           1079 ;src/game.c:210: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   45EB 3A 1E 5F      [13] 1080 	ld	a,(#_g_bossactive + 0)
   45EE B7            [ 4] 1081 	or	a, a
   45EF CA B2 46      [10] 1082 	jp	Z, 00133$
   45F2 DD 6E F7      [19] 1083 	ld	l,-9 (ix)
   45F5 DD 66 F8      [19] 1084 	ld	h,-8 (ix)
   45F8 7E            [ 7] 1085 	ld	a, (hl)
   45F9 B7            [ 4] 1086 	or	a, a
   45FA CA B2 46      [10] 1087 	jp	Z, 00133$
                           1088 ;src/game.c:211: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   45FD 21 19 5F      [10] 1089 	ld	hl, #(_g_boss + 0x0005) + 0
   4600 46            [ 7] 1090 	ld	b, (hl)
   4601 3A 18 5F      [13] 1091 	ld	a, (#(_g_boss + 0x0004) + 0)
   4604 21 15 5F      [10] 1092 	ld	hl, #(_g_boss + 0x0001) + 0
   4607 6E            [ 7] 1093 	ld	l, (hl)
   4608 DD 75 E9      [19] 1094 	ld	-23 (ix), l
   460B DD 36 EA 00   [19] 1095 	ld	-22 (ix), #0x00
   460F 21 14 5F      [10] 1096 	ld	hl, #_g_boss + 0
   4612 6E            [ 7] 1097 	ld	l, (hl)
   4613 DD 75 EB      [19] 1098 	ld	-21 (ix), l
   4616 DD 36 EC 00   [19] 1099 	ld	-20 (ix), #0x00
                           1100 ;src/game.c:210: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   461A DD 6E FA      [19] 1101 	ld	l,-6 (ix)
   461D DD 66 FB      [19] 1102 	ld	h,-5 (ix)
   4620 F5            [11] 1103 	push	af
   4621 7E            [ 7] 1104 	ld	a, (hl)
   4622 DD 77 ED      [19] 1105 	ld	-19 (ix), a
   4625 F1            [10] 1106 	pop	af
   4626 DD 6E FE      [19] 1107 	ld	l,-2 (ix)
   4629 DD 66 FF      [19] 1108 	ld	h,-1 (ix)
   462C F5            [11] 1109 	push	af
   462D 7E            [ 7] 1110 	ld	a, (hl)
   462E DD 77 EE      [19] 1111 	ld	-18 (ix), a
   4631 F1            [10] 1112 	pop	af
   4632 DD 6E F5      [19] 1113 	ld	l,-11 (ix)
   4635 DD 66 F6      [19] 1114 	ld	h,-10 (ix)
   4638 6E            [ 7] 1115 	ld	l, (hl)
   4639 DD 75 F0      [19] 1116 	ld	-16 (ix), l
   463C DD 36 F1 00   [19] 1117 	ld	-15 (ix), #0x00
   4640 F5            [11] 1118 	push	af
   4641 1A            [ 7] 1119 	ld	a, (de)
   4642 5F            [ 4] 1120 	ld	e, a
   4643 F1            [10] 1121 	pop	af
   4644 16 00         [ 7] 1122 	ld	d, #0x00
   4646 C5            [11] 1123 	push	bc
   4647 C5            [11] 1124 	push	bc
   4648 33            [ 6] 1125 	inc	sp
   4649 F5            [11] 1126 	push	af
   464A 33            [ 6] 1127 	inc	sp
   464B DD 6E E9      [19] 1128 	ld	l,-23 (ix)
   464E DD 66 EA      [19] 1129 	ld	h,-22 (ix)
   4651 E5            [11] 1130 	push	hl
   4652 DD 6E EB      [19] 1131 	ld	l,-21 (ix)
   4655 DD 66 EC      [19] 1132 	ld	h,-20 (ix)
   4658 E5            [11] 1133 	push	hl
   4659 DD 66 ED      [19] 1134 	ld	h, -19 (ix)
   465C DD 6E EE      [19] 1135 	ld	l, -18 (ix)
   465F E5            [11] 1136 	push	hl
   4660 DD 6E F0      [19] 1137 	ld	l,-16 (ix)
   4663 DD 66 F1      [19] 1138 	ld	h,-15 (ix)
   4666 E5            [11] 1139 	push	hl
   4667 D5            [11] 1140 	push	de
   4668 CD 19 40      [17] 1141 	call	_rect_overlap
   466B FD 21 0C 00   [14] 1142 	ld	iy, #12
   466F FD 39         [15] 1143 	add	iy, sp
   4671 FD F9         [10] 1144 	ld	sp, iy
   4673 C1            [10] 1145 	pop	bc
   4674 7D            [ 4] 1146 	ld	a, l
   4675 B7            [ 4] 1147 	or	a, a
   4676 28 3A         [12] 1148 	jr	Z,00133$
                           1149 ;src/game.c:212: g_projectiles[i].active = 0;
   4678 DD 6E F7      [19] 1150 	ld	l,-9 (ix)
   467B DD 66 F8      [19] 1151 	ld	h,-8 (ix)
   467E 36 00         [10] 1152 	ld	(hl), #0x00
                           1153 ;src/game.c:213: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   4680 DD 6E F3      [19] 1154 	ld	l,-13 (ix)
   4683 DD 66 F4      [19] 1155 	ld	h,-12 (ix)
   4686 46            [ 7] 1156 	ld	b, (hl)
   4687 11 14 5F      [10] 1157 	ld	de, #_g_boss
   468A C5            [11] 1158 	push	bc
   468B C5            [11] 1159 	push	bc
   468C 33            [ 6] 1160 	inc	sp
   468D D5            [11] 1161 	push	de
   468E CD EF 55      [17] 1162 	call	_enemydamage
   4691 F1            [10] 1163 	pop	af
   4692 33            [ 6] 1164 	inc	sp
   4693 C1            [10] 1165 	pop	bc
   4694 7D            [ 4] 1166 	ld	a, l
   4695 B7            [ 4] 1167 	or	a, a
   4696 28 1A         [12] 1168 	jr	Z,00133$
                           1169 ;src/game.c:214: g_bossactive = 0;
   4698 21 1E 5F      [10] 1170 	ld	hl,#_g_bossactive + 0
   469B 36 00         [10] 1171 	ld	(hl), #0x00
                           1172 ;src/game.c:215: g_score = (u16)(g_score + g_boss.reward);
   469D 21 1C 5F      [10] 1173 	ld	hl, #_g_boss + 8
   46A0 5E            [ 7] 1174 	ld	e, (hl)
   46A1 16 00         [ 7] 1175 	ld	d, #0x00
   46A3 21 04 5F      [10] 1176 	ld	hl, #_g_score
   46A6 7E            [ 7] 1177 	ld	a, (hl)
   46A7 83            [ 4] 1178 	add	a, e
   46A8 77            [ 7] 1179 	ld	(hl), a
   46A9 23            [ 6] 1180 	inc	hl
   46AA 7E            [ 7] 1181 	ld	a, (hl)
   46AB 8A            [ 4] 1182 	adc	a, d
   46AC 77            [ 7] 1183 	ld	(hl), a
                           1184 ;src/game.c:216: g_victory = 1;
   46AD 21 0D 5F      [10] 1185 	ld	hl,#_g_victory + 0
   46B0 36 01         [10] 1186 	ld	(hl), #0x01
   46B2                    1187 00133$:
                           1188 ;src/game.c:196: for (i = 0; i < MAX_PROJECTILES; ++i) {
   46B2 0C            [ 4] 1189 	inc	c
   46B3 79            [ 4] 1190 	ld	a, c
   46B4 D6 06         [ 7] 1191 	sub	a, #0x06
   46B6 DA 77 44      [10] 1192 	jp	C, 00179$
                           1193 ;src/game.c:222: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1194 ;src/game.c:221: if (!g_damagecooldown) {
   46B9 3A 0B 5F      [13] 1195 	ld	a,(#_g_damagecooldown + 0)
   46BC B7            [ 4] 1196 	or	a, a
   46BD C2 2A 48      [10] 1197 	jp	NZ, 00149$
                           1198 ;src/game.c:222: for (i = 0; i < MAX_ENEMIES; ++i) {
   46C0 DD 36 E8 00   [19] 1199 	ld	-24 (ix), #0x00
   46C4                    1200 00180$:
                           1201 ;src/game.c:223: if (!g_enemies[i].active) continue;
   46C4 DD 4E E8      [19] 1202 	ld	c,-24 (ix)
   46C7 06 00         [ 7] 1203 	ld	b,#0x00
   46C9 69            [ 4] 1204 	ld	l, c
   46CA 60            [ 4] 1205 	ld	h, b
   46CB 29            [11] 1206 	add	hl, hl
   46CC 29            [11] 1207 	add	hl, hl
   46CD 09            [11] 1208 	add	hl, bc
   46CE 29            [11] 1209 	add	hl, hl
   46CF 01 8B 5E      [10] 1210 	ld	bc,#_g_enemies
   46D2 09            [11] 1211 	add	hl,bc
   46D3 DD 75 E9      [19] 1212 	ld	-23 (ix), l
   46D6 DD 74 EA      [19] 1213 	ld	-22 (ix), h
   46D9 C1            [10] 1214 	pop	bc
   46DA E1            [10] 1215 	pop	hl
   46DB E5            [11] 1216 	push	hl
   46DC C5            [11] 1217 	push	bc
   46DD 11 06 00      [10] 1218 	ld	de, #0x0006
   46E0 19            [11] 1219 	add	hl, de
   46E1 7E            [ 7] 1220 	ld	a, (hl)
   46E2 B7            [ 4] 1221 	or	a, a
   46E3 CA 74 47      [10] 1222 	jp	Z, 00139$
                           1223 ;src/game.c:225: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   46E6 DD 7E E9      [19] 1224 	ld	a, -23 (ix)
   46E9 DD 77 EB      [19] 1225 	ld	-21 (ix), a
   46EC DD 7E EA      [19] 1226 	ld	a, -22 (ix)
   46EF DD 77 EC      [19] 1227 	ld	-20 (ix), a
   46F2 DD 6E EB      [19] 1228 	ld	l,-21 (ix)
   46F5 DD 66 EC      [19] 1229 	ld	h,-20 (ix)
   46F8 11 05 00      [10] 1230 	ld	de, #0x0005
   46FB 19            [11] 1231 	add	hl, de
   46FC 7E            [ 7] 1232 	ld	a, (hl)
   46FD DD 77 EB      [19] 1233 	ld	-21 (ix), a
   4700 C1            [10] 1234 	pop	bc
   4701 E1            [10] 1235 	pop	hl
   4702 E5            [11] 1236 	push	hl
   4703 C5            [11] 1237 	push	bc
   4704 11 04 00      [10] 1238 	ld	de, #0x0004
   4707 19            [11] 1239 	add	hl, de
   4708 5E            [ 7] 1240 	ld	e, (hl)
   4709 C1            [10] 1241 	pop	bc
   470A E1            [10] 1242 	pop	hl
   470B E5            [11] 1243 	push	hl
   470C C5            [11] 1244 	push	bc
   470D 23            [ 6] 1245 	inc	hl
   470E 4E            [ 7] 1246 	ld	c, (hl)
   470F 06 00         [ 7] 1247 	ld	b, #0x00
   4711 DD 6E E9      [19] 1248 	ld	l,-23 (ix)
   4714 DD 66 EA      [19] 1249 	ld	h,-22 (ix)
   4717 56            [ 7] 1250 	ld	d, (hl)
   4718 DD 72 E9      [19] 1251 	ld	-23 (ix), d
   471B DD 36 EA 00   [19] 1252 	ld	-22 (ix), #0x00
                           1253 ;src/game.c:224: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   471F 3A 87 5E      [13] 1254 	ld	a,(#(_g_player + 0x0005) + 0)
   4722 DD 77 ED      [19] 1255 	ld	-19 (ix), a
   4725 3A 86 5E      [13] 1256 	ld	a,(#(_g_player + 0x0004) + 0)
   4728 DD 77 EE      [19] 1257 	ld	-18 (ix), a
   472B 3A 83 5E      [13] 1258 	ld	a, (#(_g_player + 0x0001) + 0)
   472E DD 77 F0      [19] 1259 	ld	-16 (ix), a
   4731 DD 36 F1 00   [19] 1260 	ld	-15 (ix), #0x00
   4735 3A 82 5E      [13] 1261 	ld	a, (#_g_player + 0)
   4738 DD 77 F3      [19] 1262 	ld	-13 (ix), a
   473B DD 36 F4 00   [19] 1263 	ld	-12 (ix), #0x00
   473F DD 56 EB      [19] 1264 	ld	d, -21 (ix)
   4742 D5            [11] 1265 	push	de
   4743 C5            [11] 1266 	push	bc
   4744 DD 6E E9      [19] 1267 	ld	l,-23 (ix)
   4747 DD 66 EA      [19] 1268 	ld	h,-22 (ix)
   474A E5            [11] 1269 	push	hl
   474B DD 66 ED      [19] 1270 	ld	h, -19 (ix)
   474E DD 6E EE      [19] 1271 	ld	l, -18 (ix)
   4751 E5            [11] 1272 	push	hl
   4752 DD 6E F0      [19] 1273 	ld	l,-16 (ix)
   4755 DD 66 F1      [19] 1274 	ld	h,-15 (ix)
   4758 E5            [11] 1275 	push	hl
   4759 DD 6E F3      [19] 1276 	ld	l,-13 (ix)
   475C DD 66 F4      [19] 1277 	ld	h,-12 (ix)
   475F E5            [11] 1278 	push	hl
   4760 CD 19 40      [17] 1279 	call	_rect_overlap
   4763 FD 21 0C 00   [14] 1280 	ld	iy, #12
   4767 FD 39         [15] 1281 	add	iy, sp
   4769 FD F9         [10] 1282 	ld	sp, iy
   476B 7D            [ 4] 1283 	ld	a, l
   476C B7            [ 4] 1284 	or	a, a
   476D 28 05         [12] 1285 	jr	Z,00139$
                           1286 ;src/game.c:226: register_player_hit();
   476F CD 91 42      [17] 1287 	call	_register_player_hit
                           1288 ;src/game.c:227: break;
   4772 18 0B         [12] 1289 	jr	00140$
   4774                    1290 00139$:
                           1291 ;src/game.c:222: for (i = 0; i < MAX_ENEMIES; ++i) {
   4774 DD 34 E8      [23] 1292 	inc	-24 (ix)
   4777 DD 7E E8      [19] 1293 	ld	a, -24 (ix)
   477A D6 06         [ 7] 1294 	sub	a, #0x06
   477C DA C4 46      [10] 1295 	jp	C, 00180$
   477F                    1296 00140$:
                           1297 ;src/game.c:231: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   477F 3A 0B 5F      [13] 1298 	ld	a,(#_g_damagecooldown + 0)
   4782 B7            [ 4] 1299 	or	a, a
   4783 20 6E         [12] 1300 	jr	NZ,00142$
   4785 3A 1E 5F      [13] 1301 	ld	a,(#_g_bossactive + 0)
   4788 B7            [ 4] 1302 	or	a, a
   4789 28 68         [12] 1303 	jr	Z,00142$
                           1304 ;src/game.c:232: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   478B 3A 19 5F      [13] 1305 	ld	a,(#(_g_boss + 0x0005) + 0)
   478E DD 77 E9      [19] 1306 	ld	-23 (ix), a
   4791 3A 18 5F      [13] 1307 	ld	a,(#(_g_boss + 0x0004) + 0)
   4794 DD 77 EB      [19] 1308 	ld	-21 (ix), a
   4797 21 15 5F      [10] 1309 	ld	hl, #(_g_boss + 0x0001) + 0
   479A 5E            [ 7] 1310 	ld	e, (hl)
   479B 16 00         [ 7] 1311 	ld	d, #0x00
   479D 21 14 5F      [10] 1312 	ld	hl, #_g_boss + 0
   47A0 4E            [ 7] 1313 	ld	c, (hl)
   47A1 06 00         [ 7] 1314 	ld	b, #0x00
                           1315 ;src/game.c:231: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   47A3 3A 87 5E      [13] 1316 	ld	a,(#(_g_player + 0x0005) + 0)
   47A6 DD 77 ED      [19] 1317 	ld	-19 (ix), a
   47A9 3A 86 5E      [13] 1318 	ld	a,(#(_g_player + 0x0004) + 0)
   47AC DD 77 EE      [19] 1319 	ld	-18 (ix), a
   47AF 3A 83 5E      [13] 1320 	ld	a, (#(_g_player + 0x0001) + 0)
   47B2 DD 77 F0      [19] 1321 	ld	-16 (ix), a
   47B5 DD 36 F1 00   [19] 1322 	ld	-15 (ix), #0x00
   47B9 3A 82 5E      [13] 1323 	ld	a, (#_g_player + 0)
   47BC DD 77 F3      [19] 1324 	ld	-13 (ix), a
   47BF DD 36 F4 00   [19] 1325 	ld	-12 (ix), #0x00
   47C3 DD 66 E9      [19] 1326 	ld	h, -23 (ix)
   47C6 DD 6E EB      [19] 1327 	ld	l, -21 (ix)
   47C9 E5            [11] 1328 	push	hl
   47CA D5            [11] 1329 	push	de
   47CB C5            [11] 1330 	push	bc
   47CC DD 66 ED      [19] 1331 	ld	h, -19 (ix)
   47CF DD 6E EE      [19] 1332 	ld	l, -18 (ix)
   47D2 E5            [11] 1333 	push	hl
   47D3 DD 6E F0      [19] 1334 	ld	l,-16 (ix)
   47D6 DD 66 F1      [19] 1335 	ld	h,-15 (ix)
   47D9 E5            [11] 1336 	push	hl
   47DA DD 6E F3      [19] 1337 	ld	l,-13 (ix)
   47DD DD 66 F4      [19] 1338 	ld	h,-12 (ix)
   47E0 E5            [11] 1339 	push	hl
   47E1 CD 19 40      [17] 1340 	call	_rect_overlap
   47E4 FD 21 0C 00   [14] 1341 	ld	iy, #12
   47E8 FD 39         [15] 1342 	add	iy, sp
   47EA FD F9         [10] 1343 	ld	sp, iy
   47EC 7D            [ 4] 1344 	ld	a, l
   47ED B7            [ 4] 1345 	or	a, a
   47EE 28 03         [12] 1346 	jr	Z,00142$
                           1347 ;src/game.c:233: register_player_hit();
   47F0 CD 91 42      [17] 1348 	call	_register_player_hit
   47F3                    1349 00142$:
                           1350 ;src/game.c:236: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   47F3 3A 0B 5F      [13] 1351 	ld	a,(#_g_damagecooldown + 0)
   47F6 B7            [ 4] 1352 	or	a, a
   47F7 20 31         [12] 1353 	jr	NZ,00149$
   47F9 3A 87 5E      [13] 1354 	ld	a, (#(_g_player + 0x0005) + 0)
   47FC 21 86 5E      [10] 1355 	ld	hl, #(_g_player + 0x0004) + 0
   47FF 56            [ 7] 1356 	ld	d, (hl)
   4800 21 83 5E      [10] 1357 	ld	hl, #(_g_player + 0x0001) + 0
   4803 4E            [ 7] 1358 	ld	c, (hl)
   4804 06 00         [ 7] 1359 	ld	b, #0x00
   4806 21 82 5E      [10] 1360 	ld	hl, #_g_player + 0
   4809 6E            [ 7] 1361 	ld	l, (hl)
   480A DD 75 E9      [19] 1362 	ld	-23 (ix), l
   480D DD 36 EA 00   [19] 1363 	ld	-22 (ix), #0x00
   4811 F5            [11] 1364 	push	af
   4812 33            [ 6] 1365 	inc	sp
   4813 D5            [11] 1366 	push	de
   4814 33            [ 6] 1367 	inc	sp
   4815 C5            [11] 1368 	push	bc
   4816 DD 6E E9      [19] 1369 	ld	l,-23 (ix)
   4819 DD 66 EA      [19] 1370 	ld	h,-22 (ix)
   481C E5            [11] 1371 	push	hl
   481D CD 53 4C      [17] 1372 	call	_collision_is_on_trap
   4820 F1            [10] 1373 	pop	af
   4821 F1            [10] 1374 	pop	af
   4822 F1            [10] 1375 	pop	af
   4823 7D            [ 4] 1376 	ld	a, l
   4824 B7            [ 4] 1377 	or	a, a
   4825 28 03         [12] 1378 	jr	Z,00149$
                           1379 ;src/game.c:237: register_player_hit();
   4827 CD 91 42      [17] 1380 	call	_register_player_hit
   482A                    1381 00149$:
                           1382 ;src/game.c:241: if (!g_checkpointactive && g_player.x >= 44) {
   482A FD 21 13 5F   [14] 1383 	ld	iy, #_g_checkpointactive
   482E FD 7E 00      [19] 1384 	ld	a, 0 (iy)
   4831 B7            [ 4] 1385 	or	a, a
   4832 20 1E         [12] 1386 	jr	NZ,00151$
   4834 3A 82 5E      [13] 1387 	ld	a, (#_g_player + 0)
   4837 D6 2C         [ 7] 1388 	sub	a, #0x2c
   4839 38 17         [12] 1389 	jr	C,00151$
                           1390 ;src/game.c:242: g_checkpointactive = 1;
   483B FD 36 00 01   [19] 1391 	ld	0 (iy), #0x01
                           1392 ;src/game.c:243: g_checkpointx = 52;
   483F 21 11 5F      [10] 1393 	ld	hl,#_g_checkpointx + 0
   4842 36 34         [10] 1394 	ld	(hl), #0x34
                           1395 ;src/game.c:244: g_checkpointy = (u8)(tilemap_ground_y() - g_player.h);
   4844 CD 6C 50      [17] 1396 	call	_tilemap_ground_y
   4847 4D            [ 4] 1397 	ld	c, l
   4848 21 87 5E      [10] 1398 	ld	hl, #(_g_player + 0x0005) + 0
   484B 46            [ 7] 1399 	ld	b, (hl)
   484C 21 12 5F      [10] 1400 	ld	hl, #_g_checkpointy
   484F 79            [ 4] 1401 	ld	a, c
   4850 90            [ 4] 1402 	sub	a, b
   4851 77            [ 7] 1403 	ld	(hl), a
   4852                    1404 00151$:
                           1405 ;src/game.c:247: if (!g_pickuptaken && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h, (i16)36, (i16)(tilemap_ground_y() - 8), 4, 4)) {
   4852 3A 21 5F      [13] 1406 	ld	a,(#_g_pickuptaken + 0)
   4855 B7            [ 4] 1407 	or	a, a
   4856 C2 E5 48      [10] 1408 	jp	NZ, 00154$
   4859 CD 6C 50      [17] 1409 	call	_tilemap_ground_y
   485C DD 75 E9      [19] 1410 	ld	-23 (ix), l
   485F DD 75 E9      [19] 1411 	ld	-23 (ix), l
   4862 DD 36 EA 00   [19] 1412 	ld	-22 (ix), #0x00
   4866 DD 7E E9      [19] 1413 	ld	a, -23 (ix)
   4869 C6 F8         [ 7] 1414 	add	a, #0xf8
   486B DD 77 E9      [19] 1415 	ld	-23 (ix), a
   486E DD 7E EA      [19] 1416 	ld	a, -22 (ix)
   4871 CE FF         [ 7] 1417 	adc	a, #0xff
   4873 DD 77 EA      [19] 1418 	ld	-22 (ix), a
   4876 3A 87 5E      [13] 1419 	ld	a,(#(_g_player + 0x0005) + 0)
   4879 DD 77 EB      [19] 1420 	ld	-21 (ix), a
   487C 3A 86 5E      [13] 1421 	ld	a,(#(_g_player + 0x0004) + 0)
   487F DD 77 ED      [19] 1422 	ld	-19 (ix), a
   4882 3A 83 5E      [13] 1423 	ld	a,(#(_g_player + 0x0001) + 0)
   4885 DD 77 EE      [19] 1424 	ld	-18 (ix), a
   4888 DD 77 EE      [19] 1425 	ld	-18 (ix), a
   488B DD 36 EF 00   [19] 1426 	ld	-17 (ix), #0x00
   488F 3A 82 5E      [13] 1427 	ld	a,(#_g_player + 0)
   4892 DD 77 F0      [19] 1428 	ld	-16 (ix), a
   4895 DD 77 F0      [19] 1429 	ld	-16 (ix), a
   4898 DD 36 F1 00   [19] 1430 	ld	-15 (ix), #0x00
   489C 21 04 04      [10] 1431 	ld	hl, #0x0404
   489F E5            [11] 1432 	push	hl
   48A0 DD 6E E9      [19] 1433 	ld	l,-23 (ix)
   48A3 DD 66 EA      [19] 1434 	ld	h,-22 (ix)
   48A6 E5            [11] 1435 	push	hl
   48A7 21 24 00      [10] 1436 	ld	hl, #0x0024
   48AA E5            [11] 1437 	push	hl
   48AB DD 66 EB      [19] 1438 	ld	h, -21 (ix)
   48AE DD 6E ED      [19] 1439 	ld	l, -19 (ix)
   48B1 E5            [11] 1440 	push	hl
   48B2 DD 6E EE      [19] 1441 	ld	l,-18 (ix)
   48B5 DD 66 EF      [19] 1442 	ld	h,-17 (ix)
   48B8 E5            [11] 1443 	push	hl
   48B9 DD 6E F0      [19] 1444 	ld	l,-16 (ix)
   48BC DD 66 F1      [19] 1445 	ld	h,-15 (ix)
   48BF E5            [11] 1446 	push	hl
   48C0 CD 19 40      [17] 1447 	call	_rect_overlap
   48C3 FD 21 0C 00   [14] 1448 	ld	iy, #12
   48C7 FD 39         [15] 1449 	add	iy, sp
   48C9 FD F9         [10] 1450 	ld	sp, iy
   48CB 7D            [ 4] 1451 	ld	a, l
   48CC B7            [ 4] 1452 	or	a, a
   48CD 28 16         [12] 1453 	jr	Z,00154$
                           1454 ;src/game.c:248: g_pickuptaken = 1;
   48CF 21 21 5F      [10] 1455 	ld	hl,#_g_pickuptaken + 0
   48D2 36 01         [10] 1456 	ld	(hl), #0x01
                           1457 ;src/game.c:249: g_weaponlevel = 1;
   48D4 21 20 5F      [10] 1458 	ld	hl,#_g_weaponlevel + 0
   48D7 36 01         [10] 1459 	ld	(hl), #0x01
                           1460 ;src/game.c:250: g_score = (u16)(g_score + 100);
   48D9 21 04 5F      [10] 1461 	ld	hl, #_g_score
   48DC 7E            [ 7] 1462 	ld	a, (hl)
   48DD C6 64         [ 7] 1463 	add	a, #0x64
   48DF 77            [ 7] 1464 	ld	(hl), a
   48E0 23            [ 6] 1465 	inc	hl
   48E1 7E            [ 7] 1466 	ld	a, (hl)
   48E2 CE 00         [ 7] 1467 	adc	a, #0x00
   48E4 77            [ 7] 1468 	ld	(hl), a
   48E5                    1469 00154$:
                           1470 ;src/game.c:253: g_weapondisplay = (u8)(g_weaponlevel + 1);
   48E5 21 07 5F      [10] 1471 	ld	hl, #_g_weapondisplay
   48E8 3A 20 5F      [13] 1472 	ld	a,(#_g_weaponlevel + 0)
   48EB 3C            [ 4] 1473 	inc	a
   48EC 77            [ 7] 1474 	ld	(hl), a
                           1475 ;src/game.c:255: if (!g_bossactive && g_aliveenemies == 0 && !g_gameover) {
   48ED 3A 1E 5F      [13] 1476 	ld	a,(#_g_bossactive + 0)
   48F0 B7            [ 4] 1477 	or	a, a
   48F1 20 45         [12] 1478 	jr	NZ,00165$
   48F3 3A 09 5F      [13] 1479 	ld	a,(#_g_aliveenemies + 0)
   48F6 B7            [ 4] 1480 	or	a, a
   48F7 20 3F         [12] 1481 	jr	NZ,00165$
   48F9 3A 0E 5F      [13] 1482 	ld	a,(#_g_gameover + 0)
   48FC B7            [ 4] 1483 	or	a, a
   48FD 20 39         [12] 1484 	jr	NZ,00165$
                           1485 ;src/game.c:256: if (g_currentwave < TOTAL_WAVES) {
   48FF 3A 08 5F      [13] 1486 	ld	a,(#_g_currentwave + 0)
   4902 D6 03         [ 7] 1487 	sub	a, #0x03
   4904 30 20         [12] 1488 	jr	NC,00162$
                           1489 ;src/game.c:257: if (g_wavecooldown == 0) {
   4906 3A 0A 5F      [13] 1490 	ld	a,(#_g_wavecooldown + 0)
   4909 B7            [ 4] 1491 	or	a, a
   490A 20 14         [12] 1492 	jr	NZ,00157$
                           1493 ;src/game.c:258: spawn_wave(g_currentwave);
   490C 3A 08 5F      [13] 1494 	ld	a, (_g_currentwave)
   490F F5            [11] 1495 	push	af
   4910 33            [ 6] 1496 	inc	sp
   4911 CD A6 40      [17] 1497 	call	_spawn_wave
   4914 33            [ 6] 1498 	inc	sp
                           1499 ;src/game.c:259: g_currentwave++;
   4915 21 08 5F      [10] 1500 	ld	hl, #_g_currentwave+0
   4918 34            [11] 1501 	inc	(hl)
                           1502 ;src/game.c:260: g_wavecooldown = 90;
   4919 21 0A 5F      [10] 1503 	ld	hl,#_g_wavecooldown + 0
   491C 36 5A         [10] 1504 	ld	(hl), #0x5a
   491E 18 18         [12] 1505 	jr	00165$
   4920                    1506 00157$:
                           1507 ;src/game.c:262: g_wavecooldown--;
   4920 21 0A 5F      [10] 1508 	ld	hl, #_g_wavecooldown+0
   4923 35            [11] 1509 	dec	(hl)
   4924 18 12         [12] 1510 	jr	00165$
   4926                    1511 00162$:
                           1512 ;src/game.c:264: } else if (g_player.x >= (u8)(tilemap_goal_x() - 2)) {
   4926 21 82 5E      [10] 1513 	ld	hl, #_g_player + 0
   4929 4E            [ 7] 1514 	ld	c, (hl)
   492A C5            [11] 1515 	push	bc
   492B CD 10 51      [17] 1516 	call	_tilemap_goal_x
   492E C1            [10] 1517 	pop	bc
   492F 2D            [ 4] 1518 	dec	l
   4930 2D            [ 4] 1519 	dec	l
   4931 79            [ 4] 1520 	ld	a, c
   4932 95            [ 4] 1521 	sub	a, l
   4933 38 03         [12] 1522 	jr	C,00165$
                           1523 ;src/game.c:265: spawn_boss();
   4935 CD A6 41      [17] 1524 	call	_spawn_boss
   4938                    1525 00165$:
                           1526 ;src/game.c:269: g_framecounter++;
   4938 FD 21 0F 5F   [14] 1527 	ld	iy, #_g_framecounter
   493C FD 34 00      [23] 1528 	inc	0 (iy)
   493F 20 03         [12] 1529 	jr	NZ,00381$
   4941 FD 34 01      [23] 1530 	inc	1 (iy)
   4944                    1531 00381$:
                           1532 ;src/game.c:270: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   4944 21 32 00      [10] 1533 	ld	hl, #0x0032
   4947 E5            [11] 1534 	push	hl
   4948 2A 0F 5F      [16] 1535 	ld	hl, (_g_framecounter)
   494B E5            [11] 1536 	push	hl
   494C CD 60 5D      [17] 1537 	call	__moduint
   494F F1            [10] 1538 	pop	af
   4950 F1            [10] 1539 	pop	af
   4951 7C            [ 4] 1540 	ld	a, h
   4952 B5            [ 4] 1541 	or	a,l
   4953 20 0D         [12] 1542 	jr	NZ,00169$
   4955 FD 21 06 5F   [14] 1543 	ld	iy, #_g_timeleft
   4959 FD 7E 00      [19] 1544 	ld	a, 0 (iy)
   495C B7            [ 4] 1545 	or	a, a
   495D 28 03         [12] 1546 	jr	Z,00169$
                           1547 ;src/game.c:271: g_timeleft--;
   495F FD 35 00      [23] 1548 	dec	0 (iy)
   4962                    1549 00169$:
                           1550 ;src/game.c:273: if (g_timeleft == 0 && !g_victory) {
   4962 3A 06 5F      [13] 1551 	ld	a,(#_g_timeleft + 0)
   4965 B7            [ 4] 1552 	or	a, a
   4966 20 0B         [12] 1553 	jr	NZ,00172$
   4968 3A 0D 5F      [13] 1554 	ld	a,(#_g_victory + 0)
   496B B7            [ 4] 1555 	or	a, a
   496C 20 05         [12] 1556 	jr	NZ,00172$
                           1557 ;src/game.c:274: g_gameover = 1;
   496E 21 0E 5F      [10] 1558 	ld	hl,#_g_gameover + 0
   4971 36 01         [10] 1559 	ld	(hl), #0x01
   4973                    1560 00172$:
                           1561 ;src/game.c:277: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4973 3A 07 5F      [13] 1562 	ld	a, (_g_weapondisplay)
   4976 F5            [11] 1563 	push	af
   4977 33            [ 6] 1564 	inc	sp
   4978 3A 06 5F      [13] 1565 	ld	a, (_g_timeleft)
   497B F5            [11] 1566 	push	af
   497C 33            [ 6] 1567 	inc	sp
   497D 2A 04 5F      [16] 1568 	ld	hl, (_g_score)
   4980 E5            [11] 1569 	push	hl
   4981 3A 03 5F      [13] 1570 	ld	a, (_g_lives)
   4984 F5            [11] 1571 	push	af
   4985 33            [ 6] 1572 	inc	sp
   4986 CD 22 4E      [17] 1573 	call	_hudupdate
   4989 F1            [10] 1574 	pop	af
   498A F1            [10] 1575 	pop	af
   498B 33            [ 6] 1576 	inc	sp
   498C                    1577 00181$:
   498C DD F9         [10] 1578 	ld	sp, ix
   498E DD E1         [14] 1579 	pop	ix
   4990 C9            [10] 1580 	ret
                           1581 ;src/game.c:280: void game_render(void) {
                           1582 ;	---------------------------------
                           1583 ; Function game_render
                           1584 ; ---------------------------------
   4991                    1585 _game_render::
                           1586 ;src/game.c:283: cpct_clearScreen(0x00);
   4991 21 00 40      [10] 1587 	ld	hl, #0x4000
   4994 E5            [11] 1588 	push	hl
   4995 AF            [ 4] 1589 	xor	a, a
   4996 F5            [11] 1590 	push	af
   4997 33            [ 6] 1591 	inc	sp
   4998 26 C0         [ 7] 1592 	ld	h, #0xc0
   499A E5            [11] 1593 	push	hl
   499B CD 8B 5D      [17] 1594 	call	_cpct_memset
                           1595 ;src/game.c:284: tilemap_render();
   499E CD EB 4F      [17] 1596 	call	_tilemap_render
                           1597 ;src/game.c:286: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49A1 0E 00         [ 7] 1598 	ld	c, #0x00
   49A3                    1599 00115$:
                           1600 ;src/game.c:287: projectilerender(&g_projectiles[i]);
   49A3 06 00         [ 7] 1601 	ld	b,#0x00
   49A5 69            [ 4] 1602 	ld	l, c
   49A6 60            [ 4] 1603 	ld	h, b
   49A7 29            [11] 1604 	add	hl, hl
   49A8 29            [11] 1605 	add	hl, hl
   49A9 09            [11] 1606 	add	hl, bc
   49AA 29            [11] 1607 	add	hl, hl
   49AB 11 C7 5E      [10] 1608 	ld	de, #_g_projectiles
   49AE 19            [11] 1609 	add	hl, de
   49AF C5            [11] 1610 	push	bc
   49B0 E5            [11] 1611 	push	hl
   49B1 CD 87 5B      [17] 1612 	call	_projectilerender
   49B4 F1            [10] 1613 	pop	af
   49B5 C1            [10] 1614 	pop	bc
                           1615 ;src/game.c:286: for (i = 0; i < MAX_PROJECTILES; ++i) {
   49B6 0C            [ 4] 1616 	inc	c
   49B7 79            [ 4] 1617 	ld	a, c
   49B8 D6 06         [ 7] 1618 	sub	a, #0x06
   49BA 38 E7         [12] 1619 	jr	C,00115$
                           1620 ;src/game.c:290: for (i = 0; i < MAX_ENEMIES; ++i) {
   49BC 0E 00         [ 7] 1621 	ld	c, #0x00
   49BE                    1622 00117$:
                           1623 ;src/game.c:291: enemyrender(&g_enemies[i]);
   49BE 06 00         [ 7] 1624 	ld	b,#0x00
   49C0 69            [ 4] 1625 	ld	l, c
   49C1 60            [ 4] 1626 	ld	h, b
   49C2 29            [11] 1627 	add	hl, hl
   49C3 29            [11] 1628 	add	hl, hl
   49C4 09            [11] 1629 	add	hl, bc
   49C5 29            [11] 1630 	add	hl, hl
   49C6 11 8B 5E      [10] 1631 	ld	de, #_g_enemies
   49C9 19            [11] 1632 	add	hl, de
   49CA C5            [11] 1633 	push	bc
   49CB E5            [11] 1634 	push	hl
   49CC CD 75 55      [17] 1635 	call	_enemyrender
   49CF F1            [10] 1636 	pop	af
   49D0 C1            [10] 1637 	pop	bc
                           1638 ;src/game.c:290: for (i = 0; i < MAX_ENEMIES; ++i) {
   49D1 0C            [ 4] 1639 	inc	c
   49D2 79            [ 4] 1640 	ld	a, c
   49D3 D6 06         [ 7] 1641 	sub	a, #0x06
   49D5 38 E7         [12] 1642 	jr	C,00117$
                           1643 ;src/game.c:294: if (g_bossactive) {
   49D7 3A 1E 5F      [13] 1644 	ld	a,(#_g_bossactive + 0)
   49DA B7            [ 4] 1645 	or	a, a
   49DB 28 45         [12] 1646 	jr	Z,00104$
                           1647 ;src/game.c:295: enemyrender(&g_boss);
   49DD 21 14 5F      [10] 1648 	ld	hl, #_g_boss
   49E0 E5            [11] 1649 	push	hl
   49E1 CD 75 55      [17] 1650 	call	_enemyrender
                           1651 ;src/game.c:296: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x44, 32, 2);
   49E4 21 18 0A      [10] 1652 	ld	hl, #0x0a18
   49E7 E3            [19] 1653 	ex	(sp),hl
   49E8 21 00 C0      [10] 1654 	ld	hl, #0xc000
   49EB E5            [11] 1655 	push	hl
   49EC CD 62 5E      [17] 1656 	call	_cpct_getScreenPtr
   49EF 01 20 02      [10] 1657 	ld	bc, #0x0220
   49F2 C5            [11] 1658 	push	bc
   49F3 3E 44         [ 7] 1659 	ld	a, #0x44
   49F5 F5            [11] 1660 	push	af
   49F6 33            [ 6] 1661 	inc	sp
   49F7 E5            [11] 1662 	push	hl
   49F8 CD A9 5D      [17] 1663 	call	_cpct_drawSolidBox
   49FB F1            [10] 1664 	pop	af
   49FC F1            [10] 1665 	pop	af
   49FD 33            [ 6] 1666 	inc	sp
                           1667 ;src/game.c:297: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 10), 0x5C, (u8)(g_boss.health * 3), 2);
   49FE 3A 1B 5F      [13] 1668 	ld	a, (#_g_boss + 7)
   4A01 4F            [ 4] 1669 	ld	c, a
   4A02 87            [ 4] 1670 	add	a, a
   4A03 81            [ 4] 1671 	add	a, c
   4A04 57            [ 4] 1672 	ld	d, a
   4A05 D5            [11] 1673 	push	de
   4A06 21 18 0A      [10] 1674 	ld	hl, #0x0a18
   4A09 E5            [11] 1675 	push	hl
   4A0A 21 00 C0      [10] 1676 	ld	hl, #0xc000
   4A0D E5            [11] 1677 	push	hl
   4A0E CD 62 5E      [17] 1678 	call	_cpct_getScreenPtr
   4A11 4D            [ 4] 1679 	ld	c, l
   4A12 44            [ 4] 1680 	ld	b, h
   4A13 D1            [10] 1681 	pop	de
   4A14 3E 02         [ 7] 1682 	ld	a, #0x02
   4A16 F5            [11] 1683 	push	af
   4A17 33            [ 6] 1684 	inc	sp
   4A18 1E 5C         [ 7] 1685 	ld	e, #0x5c
   4A1A D5            [11] 1686 	push	de
   4A1B C5            [11] 1687 	push	bc
   4A1C CD A9 5D      [17] 1688 	call	_cpct_drawSolidBox
   4A1F F1            [10] 1689 	pop	af
   4A20 F1            [10] 1690 	pop	af
   4A21 33            [ 6] 1691 	inc	sp
   4A22                    1692 00104$:
                           1693 ;src/game.c:300: if (!g_pickuptaken) {
   4A22 3A 21 5F      [13] 1694 	ld	a,(#_g_pickuptaken + 0)
   4A25 B7            [ 4] 1695 	or	a, a
   4A26 20 23         [12] 1696 	jr	NZ,00106$
                           1697 ;src/game.c:301: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 36, (u8)(tilemap_ground_y() - 8)), 0xEE, 4, 4);
   4A28 CD 6C 50      [17] 1698 	call	_tilemap_ground_y
   4A2B 7D            [ 4] 1699 	ld	a, l
   4A2C C6 F8         [ 7] 1700 	add	a, #0xf8
   4A2E 47            [ 4] 1701 	ld	b, a
   4A2F C5            [11] 1702 	push	bc
   4A30 33            [ 6] 1703 	inc	sp
   4A31 3E 24         [ 7] 1704 	ld	a, #0x24
   4A33 F5            [11] 1705 	push	af
   4A34 33            [ 6] 1706 	inc	sp
   4A35 21 00 C0      [10] 1707 	ld	hl, #0xc000
   4A38 E5            [11] 1708 	push	hl
   4A39 CD 62 5E      [17] 1709 	call	_cpct_getScreenPtr
   4A3C 01 04 04      [10] 1710 	ld	bc, #0x0404
   4A3F C5            [11] 1711 	push	bc
   4A40 3E EE         [ 7] 1712 	ld	a, #0xee
   4A42 F5            [11] 1713 	push	af
   4A43 33            [ 6] 1714 	inc	sp
   4A44 E5            [11] 1715 	push	hl
   4A45 CD A9 5D      [17] 1716 	call	_cpct_drawSolidBox
   4A48 F1            [10] 1717 	pop	af
   4A49 F1            [10] 1718 	pop	af
   4A4A 33            [ 6] 1719 	inc	sp
   4A4B                    1720 00106$:
                           1721 ;src/game.c:303: playerrender(&g_player);
   4A4B 21 82 5E      [10] 1722 	ld	hl, #_g_player
   4A4E E5            [11] 1723 	push	hl
   4A4F CD E0 59      [17] 1724 	call	_playerrender
   4A52 F1            [10] 1725 	pop	af
                           1726 ;src/game.c:304: hudrender();
   4A53 CD 53 4E      [17] 1727 	call	_hudrender
                           1728 ;src/game.c:306: if (g_victory) {
   4A56 3A 0D 5F      [13] 1729 	ld	a,(#_g_victory + 0)
   4A59 B7            [ 4] 1730 	or	a, a
   4A5A 28 34         [12] 1731 	jr	Z,00113$
                           1732 ;src/game.c:307: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x5A, 32, 12);
   4A5C 21 18 44      [10] 1733 	ld	hl, #0x4418
   4A5F E5            [11] 1734 	push	hl
   4A60 21 00 C0      [10] 1735 	ld	hl, #0xc000
   4A63 E5            [11] 1736 	push	hl
   4A64 CD 62 5E      [17] 1737 	call	_cpct_getScreenPtr
   4A67 01 20 0C      [10] 1738 	ld	bc, #0x0c20
   4A6A C5            [11] 1739 	push	bc
   4A6B 3E 5A         [ 7] 1740 	ld	a, #0x5a
   4A6D F5            [11] 1741 	push	af
   4A6E 33            [ 6] 1742 	inc	sp
   4A6F E5            [11] 1743 	push	hl
   4A70 CD A9 5D      [17] 1744 	call	_cpct_drawSolidBox
   4A73 F1            [10] 1745 	pop	af
                           1746 ;src/game.c:308: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
   4A74 33            [ 6] 1747 	inc	sp
   4A75 21 1C 48      [10] 1748 	ld	hl,#0x481c
   4A78 E3            [19] 1749 	ex	(sp),hl
   4A79 21 00 C0      [10] 1750 	ld	hl, #0xc000
   4A7C E5            [11] 1751 	push	hl
   4A7D CD 62 5E      [17] 1752 	call	_cpct_getScreenPtr
   4A80 01 18 08      [10] 1753 	ld	bc, #0x0818
   4A83 C5            [11] 1754 	push	bc
   4A84 3E 5C         [ 7] 1755 	ld	a, #0x5c
   4A86 F5            [11] 1756 	push	af
   4A87 33            [ 6] 1757 	inc	sp
   4A88 E5            [11] 1758 	push	hl
   4A89 CD A9 5D      [17] 1759 	call	_cpct_drawSolidBox
   4A8C F1            [10] 1760 	pop	af
   4A8D F1            [10] 1761 	pop	af
   4A8E 33            [ 6] 1762 	inc	sp
   4A8F C9            [10] 1763 	ret
   4A90                    1764 00113$:
                           1765 ;src/game.c:309: } else if (g_gameover) {
   4A90 3A 0E 5F      [13] 1766 	ld	a,(#_g_gameover + 0)
   4A93 B7            [ 4] 1767 	or	a, a
   4A94 28 34         [12] 1768 	jr	Z,00110$
                           1769 ;src/game.c:310: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 24, 68), 0x44, 32, 12);
   4A96 21 18 44      [10] 1770 	ld	hl, #0x4418
   4A99 E5            [11] 1771 	push	hl
   4A9A 21 00 C0      [10] 1772 	ld	hl, #0xc000
   4A9D E5            [11] 1773 	push	hl
   4A9E CD 62 5E      [17] 1774 	call	_cpct_getScreenPtr
   4AA1 01 20 0C      [10] 1775 	ld	bc, #0x0c20
   4AA4 C5            [11] 1776 	push	bc
   4AA5 3E 44         [ 7] 1777 	ld	a, #0x44
   4AA7 F5            [11] 1778 	push	af
   4AA8 33            [ 6] 1779 	inc	sp
   4AA9 E5            [11] 1780 	push	hl
   4AAA CD A9 5D      [17] 1781 	call	_cpct_drawSolidBox
   4AAD F1            [10] 1782 	pop	af
                           1783 ;src/game.c:311: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
   4AAE 33            [ 6] 1784 	inc	sp
   4AAF 21 1C 48      [10] 1785 	ld	hl,#0x481c
   4AB2 E3            [19] 1786 	ex	(sp),hl
   4AB3 21 00 C0      [10] 1787 	ld	hl, #0xc000
   4AB6 E5            [11] 1788 	push	hl
   4AB7 CD 62 5E      [17] 1789 	call	_cpct_getScreenPtr
   4ABA 01 18 08      [10] 1790 	ld	bc, #0x0818
   4ABD C5            [11] 1791 	push	bc
   4ABE 3E 4C         [ 7] 1792 	ld	a, #0x4c
   4AC0 F5            [11] 1793 	push	af
   4AC1 33            [ 6] 1794 	inc	sp
   4AC2 E5            [11] 1795 	push	hl
   4AC3 CD A9 5D      [17] 1796 	call	_cpct_drawSolidBox
   4AC6 F1            [10] 1797 	pop	af
   4AC7 F1            [10] 1798 	pop	af
   4AC8 33            [ 6] 1799 	inc	sp
   4AC9 C9            [10] 1800 	ret
   4ACA                    1801 00110$:
                           1802 ;src/game.c:312: } else if (g_checkpointactive) {
   4ACA 3A 13 5F      [13] 1803 	ld	a,(#_g_checkpointactive + 0)
   4ACD B7            [ 4] 1804 	or	a, a
   4ACE C8            [11] 1805 	ret	Z
                           1806 ;src/game.c:313: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, g_checkpointx, (u8)(g_checkpointy - 8)), 0x3A, 2, 8);
   4ACF 3A 12 5F      [13] 1807 	ld	a,(#_g_checkpointy + 0)
   4AD2 C6 F8         [ 7] 1808 	add	a, #0xf8
   4AD4 47            [ 4] 1809 	ld	b, a
   4AD5 C5            [11] 1810 	push	bc
   4AD6 33            [ 6] 1811 	inc	sp
   4AD7 3A 11 5F      [13] 1812 	ld	a, (_g_checkpointx)
   4ADA F5            [11] 1813 	push	af
   4ADB 33            [ 6] 1814 	inc	sp
   4ADC 21 00 C0      [10] 1815 	ld	hl, #0xc000
   4ADF E5            [11] 1816 	push	hl
   4AE0 CD 62 5E      [17] 1817 	call	_cpct_getScreenPtr
   4AE3 01 02 08      [10] 1818 	ld	bc, #0x0802
   4AE6 C5            [11] 1819 	push	bc
   4AE7 3E 3A         [ 7] 1820 	ld	a, #0x3a
   4AE9 F5            [11] 1821 	push	af
   4AEA 33            [ 6] 1822 	inc	sp
   4AEB E5            [11] 1823 	push	hl
   4AEC CD A9 5D      [17] 1824 	call	_cpct_drawSolidBox
   4AEF F1            [10] 1825 	pop	af
   4AF0 F1            [10] 1826 	pop	af
   4AF1 33            [ 6] 1827 	inc	sp
   4AF2 C9            [10] 1828 	ret
                           1829 	.area _CODE
                           1830 	.area _INITIALIZER
                           1831 	.area _CABS (ABS)
