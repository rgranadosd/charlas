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
                             31 	.globl _tilemap_is_hidden_zone
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
   5E6E                      49 _g_player:
   5E6E                      50 	.ds 10
   5E78                      51 _g_enemies:
   5E78                      52 	.ds 60
   5EB4                      53 _g_projectiles:
   5EB4                      54 	.ds 60
   5EF0                      55 _g_lives:
   5EF0                      56 	.ds 1
   5EF1                      57 _g_score:
   5EF1                      58 	.ds 2
   5EF3                      59 _g_timeleft:
   5EF3                      60 	.ds 1
   5EF4                      61 _g_weaponlevel:
   5EF4                      62 	.ds 1
   5EF5                      63 _g_weapondisplay:
   5EF5                      64 	.ds 1
   5EF6                      65 _g_currentwave:
   5EF6                      66 	.ds 1
   5EF7                      67 _g_aliveenemies:
   5EF7                      68 	.ds 1
   5EF8                      69 _g_wavecooldown:
   5EF8                      70 	.ds 1
   5EF9                      71 _g_damagecooldown:
   5EF9                      72 	.ds 1
   5EFA                      73 _g_shootcooldown:
   5EFA                      74 	.ds 1
   5EFB                      75 _g_victory:
   5EFB                      76 	.ds 1
   5EFC                      77 _g_gameover:
   5EFC                      78 	.ds 1
   5EFD                      79 _g_framecounter:
   5EFD                      80 	.ds 2
   5EFF                      81 _g_checkpointx:
   5EFF                      82 	.ds 1
   5F00                      83 _g_checkpointy:
   5F00                      84 	.ds 1
   5F01                      85 _g_checkpointactive:
   5F01                      86 	.ds 1
   5F02                      87 _g_hiddenrewardtaken:
   5F02                      88 	.ds 1
   5F03                      89 _g_boss:
   5F03                      90 	.ds 10
   5F0D                      91 _g_bossactive:
   5F0D                      92 	.ds 1
   5F0E                      93 _g_bossphase:
   5F0E                      94 	.ds 1
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
   4000 21 6E 5E      [10]  125 	ld	hl, #_g_player
   4003 3A FF 5E      [13]  126 	ld	a,(#_g_checkpointx + 0)
   4006 77            [ 7]  127 	ld	(hl), a
                            128 ;src/game.c:42: g_player.y = g_checkpointy;
   4007 21 6F 5E      [10]  129 	ld	hl, #(_g_player + 0x0001)
   400A 3A 00 5F      [13]  130 	ld	a,(#_g_checkpointy + 0)
   400D 77            [ 7]  131 	ld	(hl), a
                            132 ;src/game.c:43: g_player.vx = 0;
   400E 21 70 5E      [10]  133 	ld	hl, #(_g_player + 0x0002)
   4011 36 00         [10]  134 	ld	(hl), #0x00
                            135 ;src/game.c:44: g_player.vy = 0;
   4013 21 71 5E      [10]  136 	ld	hl, #(_g_player + 0x0003)
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
                            230 ;src/game.c:59: for (i = 0; i < MAX_ENEMIES; ++i) {
   40B0 01 78 5E      [10]  231 	ld	bc, #_g_enemies+0
   40B3 1E 00         [ 7]  232 	ld	e, #0x00
   40B5                     233 00117$:
                            234 ;src/game.c:60: enemyinit(&g_enemies[i]);
   40B5 D5            [11]  235 	push	de
   40B6 16 00         [ 7]  236 	ld	d,#0x00
   40B8 6B            [ 4]  237 	ld	l, e
   40B9 62            [ 4]  238 	ld	h, d
   40BA 29            [11]  239 	add	hl, hl
   40BB 29            [11]  240 	add	hl, hl
   40BC 19            [11]  241 	add	hl, de
   40BD 29            [11]  242 	add	hl, hl
   40BE D1            [10]  243 	pop	de
   40BF 09            [11]  244 	add	hl, bc
   40C0 C5            [11]  245 	push	bc
   40C1 D5            [11]  246 	push	de
   40C2 E5            [11]  247 	push	hl
   40C3 CD 8D 51      [17]  248 	call	_enemyinit
   40C6 F1            [10]  249 	pop	af
   40C7 D1            [10]  250 	pop	de
   40C8 C1            [10]  251 	pop	bc
                            252 ;src/game.c:59: for (i = 0; i < MAX_ENEMIES; ++i) {
   40C9 1C            [ 4]  253 	inc	e
   40CA 7B            [ 4]  254 	ld	a, e
   40CB D6 06         [ 7]  255 	sub	a, #0x06
   40CD 38 E6         [12]  256 	jr	C,00117$
                            257 ;src/game.c:64: else if (wave == 1) count = 3;
   40CF DD 7E 04      [19]  258 	ld	a, 4 (ix)
   40D2 3D            [ 4]  259 	dec	a
   40D3 20 04         [12]  260 	jr	NZ,00174$
   40D5 3E 01         [ 7]  261 	ld	a,#0x01
   40D7 18 01         [12]  262 	jr	00175$
   40D9                     263 00174$:
   40D9 AF            [ 4]  264 	xor	a,a
   40DA                     265 00175$:
   40DA 5F            [ 4]  266 	ld	e, a
                            267 ;src/game.c:63: if (wave == 0) count = 2;
   40DB DD 7E 04      [19]  268 	ld	a, 4 (ix)
   40DE B7            [ 4]  269 	or	a, a
   40DF 20 06         [12]  270 	jr	NZ,00106$
   40E1 DD 36 FC 02   [19]  271 	ld	-4 (ix), #0x02
   40E5 18 0E         [12]  272 	jr	00107$
   40E7                     273 00106$:
                            274 ;src/game.c:64: else if (wave == 1) count = 3;
   40E7 7B            [ 4]  275 	ld	a, e
   40E8 B7            [ 4]  276 	or	a, a
   40E9 28 06         [12]  277 	jr	Z,00103$
   40EB DD 36 FC 03   [19]  278 	ld	-4 (ix), #0x03
   40EF 18 04         [12]  279 	jr	00107$
   40F1                     280 00103$:
                            281 ;src/game.c:65: else count = 4;
   40F1 DD 36 FC 04   [19]  282 	ld	-4 (ix), #0x04
   40F5                     283 00107$:
                            284 ;src/game.c:67: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40F5 3E 06         [ 7]  285 	ld	a, #0x06
   40F7 DD 96 FC      [19]  286 	sub	a, -4 (ix)
   40FA 30 04         [12]  287 	jr	NC,00138$
   40FC DD 36 FC 06   [19]  288 	ld	-4 (ix), #0x06
                            289 ;src/game.c:69: for (i = 0; i < count; ++i) {
   4100                     290 00138$:
   4100 DD 73 FF      [19]  291 	ld	-1 (ix), e
   4103 1E 00         [ 7]  292 	ld	e, #0x00
   4105                     293 00120$:
   4105 7B            [ 4]  294 	ld	a, e
   4106 DD 96 FC      [19]  295 	sub	a, -4 (ix)
   4109 30 65         [12]  296 	jr	NC,00116$
                            297 ;src/game.c:72: else if (wave == 1) type = (u8)(i & 1);
   410B 7B            [ 4]  298 	ld	a, e
   410C E6 01         [ 7]  299 	and	a, #0x01
   410E 6F            [ 4]  300 	ld	l, a
                            301 ;src/game.c:71: if (wave == 0) type = 0;
   410F DD 7E 04      [19]  302 	ld	a, 4 (ix)
   4112 B7            [ 4]  303 	or	a,a
   4113 20 03         [12]  304 	jr	NZ,00114$
   4115 57            [ 4]  305 	ld	d,a
   4116 18 12         [12]  306 	jr	00115$
   4118                     307 00114$:
                            308 ;src/game.c:72: else if (wave == 1) type = (u8)(i & 1);
   4118 DD 7E FF      [19]  309 	ld	a, -1 (ix)
   411B B7            [ 4]  310 	or	a, a
   411C 28 03         [12]  311 	jr	Z,00111$
   411E 55            [ 4]  312 	ld	d, l
   411F 18 09         [12]  313 	jr	00115$
   4121                     314 00111$:
                            315 ;src/game.c:73: else type = (u8)((i == 0) ? 2 : (i & 1));
   4121 7B            [ 4]  316 	ld	a, e
   4122 B7            [ 4]  317 	or	a, a
   4123 20 04         [12]  318 	jr	NZ,00124$
   4125 16 02         [ 7]  319 	ld	d, #0x02
   4127 18 01         [12]  320 	jr	00125$
   4129                     321 00124$:
   4129 55            [ 4]  322 	ld	d, l
   412A                     323 00125$:
   412A                     324 00115$:
                            325 ;src/game.c:74: enemyspawn(&g_enemies[i], (u8)(48 + (i * 10)), 112, type, (u8)((i & 1) ? 1 : 0));
   412A 7D            [ 4]  326 	ld	a, l
   412B B7            [ 4]  327 	or	a, a
   412C 28 06         [12]  328 	jr	Z,00126$
   412E DD 36 FE 01   [19]  329 	ld	-2 (ix), #0x01
   4132 18 04         [12]  330 	jr	00127$
   4134                     331 00126$:
   4134 DD 36 FE 00   [19]  332 	ld	-2 (ix), #0x00
   4138                     333 00127$:
   4138 D5            [11]  334 	push	de
   4139 7B            [ 4]  335 	ld	a, e
   413A 87            [ 4]  336 	add	a, a
   413B 87            [ 4]  337 	add	a, a
   413C 83            [ 4]  338 	add	a, e
   413D 87            [ 4]  339 	add	a, a
   413E D1            [10]  340 	pop	de
   413F C6 30         [ 7]  341 	add	a, #0x30
   4141 DD 77 FD      [19]  342 	ld	-3 (ix), a
   4144 D5            [11]  343 	push	de
   4145 16 00         [ 7]  344 	ld	d,#0x00
   4147 6B            [ 4]  345 	ld	l, e
   4148 62            [ 4]  346 	ld	h, d
   4149 29            [11]  347 	add	hl, hl
   414A 29            [11]  348 	add	hl, hl
   414B 19            [11]  349 	add	hl, de
   414C 29            [11]  350 	add	hl, hl
   414D D1            [10]  351 	pop	de
   414E 09            [11]  352 	add	hl, bc
   414F E5            [11]  353 	push	hl
   4150 FD E1         [14]  354 	pop	iy
   4152 C5            [11]  355 	push	bc
   4153 D5            [11]  356 	push	de
   4154 DD 7E FE      [19]  357 	ld	a, -2 (ix)
   4157 F5            [11]  358 	push	af
   4158 33            [ 6]  359 	inc	sp
   4159 1E 70         [ 7]  360 	ld	e, #0x70
   415B D5            [11]  361 	push	de
   415C DD 7E FD      [19]  362 	ld	a, -3 (ix)
   415F F5            [11]  363 	push	af
   4160 33            [ 6]  364 	inc	sp
   4161 FD E5         [15]  365 	push	iy
   4163 CD D2 51      [17]  366 	call	_enemyspawn
   4166 21 06 00      [10]  367 	ld	hl, #6
   4169 39            [11]  368 	add	hl, sp
   416A F9            [ 6]  369 	ld	sp, hl
   416B D1            [10]  370 	pop	de
   416C C1            [10]  371 	pop	bc
                            372 ;src/game.c:69: for (i = 0; i < count; ++i) {
   416D 1C            [ 4]  373 	inc	e
   416E 18 95         [12]  374 	jr	00120$
   4170                     375 00116$:
                            376 ;src/game.c:77: g_aliveenemies = count;
   4170 DD 7E FC      [19]  377 	ld	a, -4 (ix)
   4173 32 F7 5E      [13]  378 	ld	(#_g_aliveenemies + 0),a
   4176 DD F9         [10]  379 	ld	sp, ix
   4178 DD E1         [14]  380 	pop	ix
   417A C9            [10]  381 	ret
                            382 ;src/game.c:80: static void spawn_boss(void) {
                            383 ;	---------------------------------
                            384 ; Function spawn_boss
                            385 ; ---------------------------------
   417B                     386 _spawn_boss:
                            387 ;src/game.c:81: enemyinit(&g_boss);
   417B 21 03 5F      [10]  388 	ld	hl, #_g_boss
   417E E5            [11]  389 	push	hl
   417F CD 8D 51      [17]  390 	call	_enemyinit
                            391 ;src/game.c:82: enemyspawn(&g_boss, 64, 88, 1, 0);
   4182 21 01 00      [10]  392 	ld	hl, #0x0001
   4185 E3            [19]  393 	ex	(sp),hl
   4186 21 40 58      [10]  394 	ld	hl, #0x5840
   4189 E5            [11]  395 	push	hl
   418A 21 03 5F      [10]  396 	ld	hl, #_g_boss
   418D E5            [11]  397 	push	hl
   418E CD D2 51      [17]  398 	call	_enemyspawn
   4191 21 06 00      [10]  399 	ld	hl, #6
   4194 39            [11]  400 	add	hl, sp
   4195 F9            [ 6]  401 	ld	sp, hl
                            402 ;src/game.c:83: g_boss.w = 8;
   4196 21 07 5F      [10]  403 	ld	hl, #(_g_boss + 0x0004)
   4199 36 08         [10]  404 	ld	(hl), #0x08
                            405 ;src/game.c:84: g_boss.h = 20;
   419B 21 08 5F      [10]  406 	ld	hl, #(_g_boss + 0x0005)
   419E 36 14         [10]  407 	ld	(hl), #0x14
                            408 ;src/game.c:85: g_boss.health = 8;
   41A0 21 0A 5F      [10]  409 	ld	hl, #(_g_boss + 0x0007)
   41A3 36 08         [10]  410 	ld	(hl), #0x08
                            411 ;src/game.c:86: g_boss.reward = 1200;
   41A5 21 0B 5F      [10]  412 	ld	hl, #(_g_boss + 0x0008)
   41A8 36 B0         [10]  413 	ld	(hl), #0xb0
                            414 ;src/game.c:87: g_boss.kind = 3;
   41AA 21 0C 5F      [10]  415 	ld	hl, #(_g_boss + 0x0009)
   41AD 36 03         [10]  416 	ld	(hl), #0x03
                            417 ;src/game.c:88: g_bossactive = 1;
   41AF 21 0D 5F      [10]  418 	ld	hl,#_g_bossactive + 0
   41B2 36 01         [10]  419 	ld	(hl), #0x01
                            420 ;src/game.c:89: g_bossphase = 0;
   41B4 21 0E 5F      [10]  421 	ld	hl,#_g_bossphase + 0
   41B7 36 00         [10]  422 	ld	(hl), #0x00
   41B9 C9            [10]  423 	ret
                            424 ;src/game.c:92: static void try_fire_projectile(void) {
                            425 ;	---------------------------------
                            426 ; Function try_fire_projectile
                            427 ; ---------------------------------
   41BA                     428 _try_fire_projectile:
   41BA DD E5         [15]  429 	push	ix
   41BC DD 21 00 00   [14]  430 	ld	ix,#0
   41C0 DD 39         [15]  431 	add	ix,sp
   41C2 21 FA FF      [10]  432 	ld	hl, #-6
   41C5 39            [11]  433 	add	hl, sp
   41C6 F9            [ 6]  434 	ld	sp, hl
                            435 ;src/game.c:96: if (!input_is_shoot_just_pressed()) return;
   41C7 CD AB 4E      [17]  436 	call	_input_is_shoot_just_pressed
   41CA DD 75 FF      [19]  437 	ld	-1 (ix), l
   41CD 7D            [ 4]  438 	ld	a, l
   41CE B7            [ 4]  439 	or	a, a
   41CF CA 50 42      [10]  440 	jp	Z,00110$
                            441 ;src/game.c:97: if (g_shootcooldown) return;
   41D2 3A FA 5E      [13]  442 	ld	a,(#_g_shootcooldown + 0)
   41D5 B7            [ 4]  443 	or	a, a
   41D6 20 78         [12]  444 	jr	NZ,00110$
                            445 ;src/game.c:99: dir = g_player.facing_left ? -3 : 3;
   41D8 3A 75 5E      [13]  446 	ld	a, (#_g_player + 7)
   41DB B7            [ 4]  447 	or	a, a
   41DC 28 04         [12]  448 	jr	Z,00112$
   41DE 0E FD         [ 7]  449 	ld	c, #0xfd
   41E0 18 02         [12]  450 	jr	00113$
   41E2                     451 00112$:
   41E2 0E 03         [ 7]  452 	ld	c, #0x03
   41E4                     453 00113$:
   41E4 DD 71 FA      [19]  454 	ld	-6 (ix), c
                            455 ;src/game.c:101: for (i = 0; i < MAX_PROJECTILES; ++i) {
   41E7 DD 36 FB 00   [19]  456 	ld	-5 (ix), #0x00
   41EB                     457 00108$:
                            458 ;src/game.c:102: if (!g_projectiles[i].active) {
   41EB DD 4E FB      [19]  459 	ld	c,-5 (ix)
   41EE 06 00         [ 7]  460 	ld	b,#0x00
   41F0 69            [ 4]  461 	ld	l, c
   41F1 60            [ 4]  462 	ld	h, b
   41F2 29            [11]  463 	add	hl, hl
   41F3 29            [11]  464 	add	hl, hl
   41F4 09            [11]  465 	add	hl, bc
   41F5 29            [11]  466 	add	hl, hl
   41F6 01 B4 5E      [10]  467 	ld	bc,#_g_projectiles
   41F9 09            [11]  468 	add	hl,bc
   41FA DD 75 FD      [19]  469 	ld	-3 (ix), l
   41FD DD 74 FE      [19]  470 	ld	-2 (ix), h
   4200 11 06 00      [10]  471 	ld	de, #0x0006
   4203 19            [11]  472 	add	hl, de
   4204 7E            [ 7]  473 	ld	a, (hl)
   4205 B7            [ 4]  474 	or	a, a
   4206 20 3E         [12]  475 	jr	NZ,00109$
                            476 ;src/game.c:103: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weaponlevel);
   4208 3A 6F 5E      [13]  477 	ld	a,(#_g_player + 1)
   420B DD 77 FF      [19]  478 	ld	-1 (ix), a
   420E C6 06         [ 7]  479 	add	a, #0x06
   4210 DD 77 FF      [19]  480 	ld	-1 (ix), a
   4213 3A 6E 5E      [13]  481 	ld	a,(#_g_player + 0)
   4216 DD 77 FC      [19]  482 	ld	-4 (ix), a
   4219 DD 34 FC      [23]  483 	inc	-4 (ix)
   421C DD 34 FC      [23]  484 	inc	-4 (ix)
   421F 3A F4 5E      [13]  485 	ld	a, (_g_weaponlevel)
   4222 F5            [11]  486 	push	af
   4223 33            [ 6]  487 	inc	sp
   4224 DD 66 FA      [19]  488 	ld	h, -6 (ix)
   4227 DD 6E FF      [19]  489 	ld	l, -1 (ix)
   422A E5            [11]  490 	push	hl
   422B DD 7E FC      [19]  491 	ld	a, -4 (ix)
   422E F5            [11]  492 	push	af
   422F 33            [ 6]  493 	inc	sp
   4230 DD 6E FD      [19]  494 	ld	l,-3 (ix)
   4233 DD 66 FE      [19]  495 	ld	h,-2 (ix)
   4236 E5            [11]  496 	push	hl
   4237 CD 5D 5A      [17]  497 	call	_projectilefire
   423A 21 06 00      [10]  498 	ld	hl, #6
   423D 39            [11]  499 	add	hl, sp
   423E F9            [ 6]  500 	ld	sp, hl
                            501 ;src/game.c:104: g_shootcooldown = 10;
   423F 21 FA 5E      [10]  502 	ld	hl,#_g_shootcooldown + 0
   4242 36 0A         [10]  503 	ld	(hl), #0x0a
                            504 ;src/game.c:105: break;
   4244 18 0A         [12]  505 	jr	00110$
   4246                     506 00109$:
                            507 ;src/game.c:101: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4246 DD 34 FB      [23]  508 	inc	-5 (ix)
   4249 DD 7E FB      [19]  509 	ld	a, -5 (ix)
   424C D6 06         [ 7]  510 	sub	a, #0x06
   424E 38 9B         [12]  511 	jr	C,00108$
   4250                     512 00110$:
   4250 DD F9         [10]  513 	ld	sp, ix
   4252 DD E1         [14]  514 	pop	ix
   4254 C9            [10]  515 	ret
                            516 ;src/game.c:110: void game_init(void) {
                            517 ;	---------------------------------
                            518 ; Function game_init
                            519 ; ---------------------------------
   4255                     520 _game_init::
                            521 ;src/game.c:113: cpct_disableFirmware();
   4255 CD 85 5D      [17]  522 	call	_cpct_disableFirmware
                            523 ;src/game.c:114: cpct_setVideoMode(1);
   4258 2E 01         [ 7]  524 	ld	l, #0x01
   425A CD 69 5D      [17]  525 	call	_cpct_setVideoMode
                            526 ;src/game.c:115: cpct_clearScreen(0x00);
   425D 21 00 40      [10]  527 	ld	hl, #0x4000
   4260 E5            [11]  528 	push	hl
   4261 AF            [ 4]  529 	xor	a, a
   4262 F5            [11]  530 	push	af
   4263 33            [ 6]  531 	inc	sp
   4264 26 C0         [ 7]  532 	ld	h, #0xc0
   4266 E5            [11]  533 	push	hl
   4267 CD 77 5D      [17]  534 	call	_cpct_memset
                            535 ;src/game.c:116: tilemap_init();
   426A CD BD 4E      [17]  536 	call	_tilemap_init
                            537 ;src/game.c:117: collision_init();
   426D CD FF 49      [17]  538 	call	_collision_init
                            539 ;src/game.c:118: playerinit(&g_player);
   4270 21 6E 5E      [10]  540 	ld	hl, #_g_player
   4273 E5            [11]  541 	push	hl
   4274 CD F7 55      [17]  542 	call	_playerinit
   4277 F1            [10]  543 	pop	af
                            544 ;src/game.c:119: hudinit();
   4278 CD 05 4D      [17]  545 	call	_hudinit
                            546 ;src/game.c:121: for (i = 0; i < MAX_PROJECTILES; ++i) {
   427B 0E 00         [ 7]  547 	ld	c, #0x00
   427D                     548 00102$:
                            549 ;src/game.c:122: projectileinit(&g_projectiles[i]);
   427D 06 00         [ 7]  550 	ld	b,#0x00
   427F 69            [ 4]  551 	ld	l, c
   4280 60            [ 4]  552 	ld	h, b
   4281 29            [11]  553 	add	hl, hl
   4282 29            [11]  554 	add	hl, hl
   4283 09            [11]  555 	add	hl, bc
   4284 29            [11]  556 	add	hl, hl
   4285 11 B4 5E      [10]  557 	ld	de, #_g_projectiles
   4288 19            [11]  558 	add	hl, de
   4289 C5            [11]  559 	push	bc
   428A E5            [11]  560 	push	hl
   428B CD 18 5A      [17]  561 	call	_projectileinit
   428E F1            [10]  562 	pop	af
   428F C1            [10]  563 	pop	bc
                            564 ;src/game.c:121: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4290 0C            [ 4]  565 	inc	c
   4291 79            [ 4]  566 	ld	a, c
   4292 D6 06         [ 7]  567 	sub	a, #0x06
   4294 38 E7         [12]  568 	jr	C,00102$
                            569 ;src/game.c:125: g_lives = 3;
   4296 21 F0 5E      [10]  570 	ld	hl,#_g_lives + 0
   4299 36 03         [10]  571 	ld	(hl), #0x03
                            572 ;src/game.c:126: g_score = 0;
   429B 21 00 00      [10]  573 	ld	hl, #0x0000
   429E 22 F1 5E      [16]  574 	ld	(_g_score), hl
                            575 ;src/game.c:127: g_timeleft = 99;
   42A1 FD 21 F3 5E   [14]  576 	ld	iy, #_g_timeleft
   42A5 FD 36 00 63   [19]  577 	ld	0 (iy), #0x63
                            578 ;src/game.c:128: g_weaponlevel = 0;
   42A9 FD 21 F4 5E   [14]  579 	ld	iy, #_g_weaponlevel
   42AD FD 36 00 00   [19]  580 	ld	0 (iy), #0x00
                            581 ;src/game.c:129: g_weapondisplay = 0;
   42B1 FD 21 F5 5E   [14]  582 	ld	iy, #_g_weapondisplay
   42B5 FD 36 00 00   [19]  583 	ld	0 (iy), #0x00
                            584 ;src/game.c:130: g_currentwave = 0;
   42B9 FD 21 F6 5E   [14]  585 	ld	iy, #_g_currentwave
   42BD FD 36 00 00   [19]  586 	ld	0 (iy), #0x00
                            587 ;src/game.c:131: g_wavecooldown = 1;
   42C1 FD 21 F8 5E   [14]  588 	ld	iy, #_g_wavecooldown
   42C5 FD 36 00 01   [19]  589 	ld	0 (iy), #0x01
                            590 ;src/game.c:132: g_damagecooldown = 0;
   42C9 FD 21 F9 5E   [14]  591 	ld	iy, #_g_damagecooldown
   42CD FD 36 00 00   [19]  592 	ld	0 (iy), #0x00
                            593 ;src/game.c:133: g_shootcooldown = 0;
   42D1 FD 21 FA 5E   [14]  594 	ld	iy, #_g_shootcooldown
   42D5 FD 36 00 00   [19]  595 	ld	0 (iy), #0x00
                            596 ;src/game.c:134: g_victory = 0;
   42D9 FD 21 FB 5E   [14]  597 	ld	iy, #_g_victory
   42DD FD 36 00 00   [19]  598 	ld	0 (iy), #0x00
                            599 ;src/game.c:135: g_gameover = 0;
   42E1 FD 21 FC 5E   [14]  600 	ld	iy, #_g_gameover
   42E5 FD 36 00 00   [19]  601 	ld	0 (iy), #0x00
                            602 ;src/game.c:136: g_framecounter = 0;
   42E9 2E 00         [ 7]  603 	ld	l, #0x00
   42EB 22 FD 5E      [16]  604 	ld	(_g_framecounter), hl
                            605 ;src/game.c:137: g_checkpointx = 20;
   42EE 21 FF 5E      [10]  606 	ld	hl,#_g_checkpointx + 0
   42F1 36 14         [10]  607 	ld	(hl), #0x14
                            608 ;src/game.c:138: g_checkpointy = 120;
   42F3 21 00 5F      [10]  609 	ld	hl,#_g_checkpointy + 0
   42F6 36 78         [10]  610 	ld	(hl), #0x78
                            611 ;src/game.c:139: g_checkpointactive = 0;
   42F8 21 01 5F      [10]  612 	ld	hl,#_g_checkpointactive + 0
   42FB 36 00         [10]  613 	ld	(hl), #0x00
                            614 ;src/game.c:140: g_hiddenrewardtaken = 0;
   42FD 21 02 5F      [10]  615 	ld	hl,#_g_hiddenrewardtaken + 0
   4300 36 00         [10]  616 	ld	(hl), #0x00
                            617 ;src/game.c:141: g_bossactive = 0;
   4302 21 0D 5F      [10]  618 	ld	hl,#_g_bossactive + 0
   4305 36 00         [10]  619 	ld	(hl), #0x00
                            620 ;src/game.c:142: enemyinit(&g_boss);
   4307 21 03 5F      [10]  621 	ld	hl, #_g_boss
   430A E5            [11]  622 	push	hl
   430B CD 8D 51      [17]  623 	call	_enemyinit
   430E F1            [10]  624 	pop	af
   430F C9            [10]  625 	ret
                            626 ;src/game.c:145: void game_update(void) {
                            627 ;	---------------------------------
                            628 ; Function game_update
                            629 ; ---------------------------------
   4310                     630 _game_update::
   4310 DD E5         [15]  631 	push	ix
   4312 DD 21 00 00   [14]  632 	ld	ix,#0
   4316 DD 39         [15]  633 	add	ix,sp
   4318 21 E7 FF      [10]  634 	ld	hl, #-25
   431B 39            [11]  635 	add	hl, sp
   431C F9            [ 6]  636 	ld	sp, hl
                            637 ;src/game.c:149: input_update();
   431D CD 18 4E      [17]  638 	call	_input_update
                            639 ;src/game.c:151: if (g_gameover || g_victory) {
   4320 3A FC 5E      [13]  640 	ld	a,(#_g_gameover + 0)
   4323 B7            [ 4]  641 	or	a, a
   4324 C2 2B 49      [10]  642 	jp	NZ,00202$
   4327 3A FB 5E      [13]  643 	ld	a,(#_g_victory + 0)
   432A B7            [ 4]  644 	or	a, a
                            645 ;src/game.c:152: return;
   432B C2 2B 49      [10]  646 	jp	NZ,00202$
                            647 ;src/game.c:155: playerupdate(&g_player);
   432E 21 6E 5E      [10]  648 	ld	hl, #_g_player
   4331 E5            [11]  649 	push	hl
   4332 CD 3E 56      [17]  650 	call	_playerupdate
   4335 F1            [10]  651 	pop	af
                            652 ;src/game.c:156: try_fire_projectile();
   4336 CD BA 41      [17]  653 	call	_try_fire_projectile
                            654 ;src/game.c:158: if (g_shootcooldown) g_shootcooldown--;
   4339 FD 21 FA 5E   [14]  655 	ld	iy, #_g_shootcooldown
   433D FD 7E 00      [19]  656 	ld	a, 0 (iy)
   4340 B7            [ 4]  657 	or	a, a
   4341 28 03         [12]  658 	jr	Z,00105$
   4343 FD 35 00      [23]  659 	dec	0 (iy)
   4346                     660 00105$:
                            661 ;src/game.c:159: if (g_damagecooldown) g_damagecooldown--;
   4346 FD 21 F9 5E   [14]  662 	ld	iy, #_g_damagecooldown
   434A FD 7E 00      [19]  663 	ld	a, 0 (iy)
   434D B7            [ 4]  664 	or	a, a
   434E 28 03         [12]  665 	jr	Z,00213$
   4350 FD 35 00      [23]  666 	dec	0 (iy)
                            667 ;src/game.c:161: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4353                     668 00213$:
   4353 0E 00         [ 7]  669 	ld	c, #0x00
   4355                     670 00195$:
                            671 ;src/game.c:162: projectileupdate(&g_projectiles[i]);
   4355 06 00         [ 7]  672 	ld	b,#0x00
   4357 69            [ 4]  673 	ld	l, c
   4358 60            [ 4]  674 	ld	h, b
   4359 29            [11]  675 	add	hl, hl
   435A 29            [11]  676 	add	hl, hl
   435B 09            [11]  677 	add	hl, bc
   435C 29            [11]  678 	add	hl, hl
   435D 11 B4 5E      [10]  679 	ld	de, #_g_projectiles
   4360 19            [11]  680 	add	hl, de
   4361 C5            [11]  681 	push	bc
   4362 E5            [11]  682 	push	hl
   4363 CD 14 5B      [17]  683 	call	_projectileupdate
   4366 F1            [10]  684 	pop	af
   4367 C1            [10]  685 	pop	bc
                            686 ;src/game.c:161: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4368 0C            [ 4]  687 	inc	c
   4369 79            [ 4]  688 	ld	a, c
   436A D6 06         [ 7]  689 	sub	a, #0x06
   436C 38 E7         [12]  690 	jr	C,00195$
                            691 ;src/game.c:165: for (i = 0; i < MAX_ENEMIES; ++i) {
   436E 0E 00         [ 7]  692 	ld	c, #0x00
   4370                     693 00197$:
                            694 ;src/game.c:166: enemyupdate(&g_enemies[i]);
   4370 06 00         [ 7]  695 	ld	b,#0x00
   4372 69            [ 4]  696 	ld	l, c
   4373 60            [ 4]  697 	ld	h, b
   4374 29            [11]  698 	add	hl, hl
   4375 29            [11]  699 	add	hl, hl
   4376 09            [11]  700 	add	hl, bc
   4377 29            [11]  701 	add	hl, hl
   4378 11 78 5E      [10]  702 	ld	de, #_g_enemies
   437B 19            [11]  703 	add	hl, de
   437C C5            [11]  704 	push	bc
   437D E5            [11]  705 	push	hl
   437E CD 6D 53      [17]  706 	call	_enemyupdate
   4381 F1            [10]  707 	pop	af
   4382 C1            [10]  708 	pop	bc
                            709 ;src/game.c:165: for (i = 0; i < MAX_ENEMIES; ++i) {
   4383 0C            [ 4]  710 	inc	c
   4384 79            [ 4]  711 	ld	a, c
   4385 D6 06         [ 7]  712 	sub	a, #0x06
   4387 38 E7         [12]  713 	jr	C,00197$
                            714 ;src/game.c:169: if (g_bossactive) {
   4389 3A 0D 5F      [13]  715 	ld	a,(#_g_bossactive + 0)
   438C B7            [ 4]  716 	or	a, a
   438D 28 48         [12]  717 	jr	Z,00232$
                            718 ;src/game.c:170: if (g_boss.health > 4) g_bossphase = 0;
   438F 21 0A 5F      [10]  719 	ld	hl, #_g_boss + 7
   4392 4E            [ 7]  720 	ld	c, (hl)
   4393 3E 04         [ 7]  721 	ld	a, #0x04
   4395 91            [ 4]  722 	sub	a, c
   4396 30 07         [12]  723 	jr	NC,00111$
   4398 21 0E 5F      [10]  724 	ld	hl,#_g_bossphase + 0
   439B 36 00         [10]  725 	ld	(hl), #0x00
   439D 18 05         [12]  726 	jr	00112$
   439F                     727 00111$:
                            728 ;src/game.c:171: else g_bossphase = 1;
   439F 21 0E 5F      [10]  729 	ld	hl,#_g_bossphase + 0
   43A2 36 01         [10]  730 	ld	(hl), #0x01
   43A4                     731 00112$:
                            732 ;src/game.c:173: g_boss.vx = (i8)(g_player.x < g_boss.x ? -(g_bossphase ? 2 : 1) : (g_bossphase ? 2 : 1));
   43A4 3A 6E 5E      [13]  733 	ld	a, (#_g_player + 0)
   43A7 21 03 5F      [10]  734 	ld	hl, #_g_boss + 0
   43AA 4E            [ 7]  735 	ld	c, (hl)
   43AB 91            [ 4]  736 	sub	a, c
   43AC 30 11         [12]  737 	jr	NC,00204$
   43AE 3A 0E 5F      [13]  738 	ld	a,(#_g_bossphase + 0)
   43B1 B7            [ 4]  739 	or	a, a
   43B2 28 04         [12]  740 	jr	Z,00206$
   43B4 0E 02         [ 7]  741 	ld	c, #0x02
   43B6 18 02         [12]  742 	jr	00207$
   43B8                     743 00206$:
   43B8 0E 01         [ 7]  744 	ld	c, #0x01
   43BA                     745 00207$:
   43BA AF            [ 4]  746 	xor	a, a
   43BB 91            [ 4]  747 	sub	a, c
   43BC 4F            [ 4]  748 	ld	c, a
   43BD 18 0C         [12]  749 	jr	00205$
   43BF                     750 00204$:
   43BF 3A 0E 5F      [13]  751 	ld	a,(#_g_bossphase + 0)
   43C2 B7            [ 4]  752 	or	a, a
   43C3 28 04         [12]  753 	jr	Z,00208$
   43C5 0E 02         [ 7]  754 	ld	c, #0x02
   43C7 18 02         [12]  755 	jr	00209$
   43C9                     756 00208$:
   43C9 0E 01         [ 7]  757 	ld	c, #0x01
   43CB                     758 00209$:
   43CB                     759 00205$:
   43CB 21 05 5F      [10]  760 	ld	hl, #(_g_boss + 0x0002)
   43CE 71            [ 7]  761 	ld	(hl), c
                            762 ;src/game.c:174: enemyupdate(&g_boss);
   43CF 21 03 5F      [10]  763 	ld	hl, #_g_boss
   43D2 E5            [11]  764 	push	hl
   43D3 CD 6D 53      [17]  765 	call	_enemyupdate
   43D6 F1            [10]  766 	pop	af
                            767 ;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
   43D7                     768 00232$:
   43D7 0E 00         [ 7]  769 	ld	c, #0x00
   43D9                     770 00200$:
                            771 ;src/game.c:178: if (!g_projectiles[i].active) continue;
   43D9 06 00         [ 7]  772 	ld	b,#0x00
   43DB 69            [ 4]  773 	ld	l, c
   43DC 60            [ 4]  774 	ld	h, b
   43DD 29            [11]  775 	add	hl, hl
   43DE 29            [11]  776 	add	hl, hl
   43DF 09            [11]  777 	add	hl, bc
   43E0 29            [11]  778 	add	hl, hl
   43E1 EB            [ 4]  779 	ex	de,hl
   43E2 21 B4 5E      [10]  780 	ld	hl, #_g_projectiles
   43E5 19            [11]  781 	add	hl,de
   43E6 EB            [ 4]  782 	ex	de,hl
   43E7 21 06 00      [10]  783 	ld	hl, #0x0006
   43EA 19            [11]  784 	add	hl,de
   43EB DD 75 FE      [19]  785 	ld	-2 (ix), l
   43EE DD 74 FF      [19]  786 	ld	-1 (ix), h
   43F1 7E            [ 7]  787 	ld	a, (hl)
   43F2 B7            [ 4]  788 	or	a, a
   43F3 CA 14 46      [10]  789 	jp	Z, 00133$
                            790 ;src/game.c:179: for (j = 0; j < MAX_ENEMIES; ++j) {
   43F6 DD 36 E7 00   [19]  791 	ld	-25 (ix), #0x00
   43FA                     792 00199$:
                            793 ;src/game.c:180: if (!g_enemies[j].active) continue;
   43FA D5            [11]  794 	push	de
   43FB DD 5E E7      [19]  795 	ld	e,-25 (ix)
   43FE 16 00         [ 7]  796 	ld	d,#0x00
   4400 6B            [ 4]  797 	ld	l, e
   4401 62            [ 4]  798 	ld	h, d
   4402 29            [11]  799 	add	hl, hl
   4403 29            [11]  800 	add	hl, hl
   4404 19            [11]  801 	add	hl, de
   4405 29            [11]  802 	add	hl, hl
   4406 D1            [10]  803 	pop	de
   4407 3E 78         [ 7]  804 	ld	a, #<(_g_enemies)
   4409 85            [ 4]  805 	add	a, l
   440A DD 77 FC      [19]  806 	ld	-4 (ix), a
   440D 3E 5E         [ 7]  807 	ld	a, #>(_g_enemies)
   440F 8C            [ 4]  808 	adc	a, h
   4410 DD 77 FD      [19]  809 	ld	-3 (ix), a
   4413 DD 6E FC      [19]  810 	ld	l,-4 (ix)
   4416 DD 66 FD      [19]  811 	ld	h,-3 (ix)
   4419 C5            [11]  812 	push	bc
   441A 01 06 00      [10]  813 	ld	bc, #0x0006
   441D 09            [11]  814 	add	hl, bc
   441E C1            [10]  815 	pop	bc
   441F 46            [ 7]  816 	ld	b, (hl)
                            817 ;src/game.c:181: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4420 21 05 00      [10]  818 	ld	hl, #0x0005
   4423 19            [11]  819 	add	hl,de
   4424 DD 75 FA      [19]  820 	ld	-6 (ix), l
   4427 DD 74 FB      [19]  821 	ld	-5 (ix), h
   442A 21 04 00      [10]  822 	ld	hl, #0x0004
   442D 19            [11]  823 	add	hl,de
   442E DD 75 F8      [19]  824 	ld	-8 (ix), l
   4431 DD 74 F9      [19]  825 	ld	-7 (ix), h
   4434 21 01 00      [10]  826 	ld	hl, #0x0001
   4437 19            [11]  827 	add	hl,de
   4438 DD 75 F6      [19]  828 	ld	-10 (ix), l
   443B DD 74 F7      [19]  829 	ld	-9 (ix), h
                            830 ;src/game.c:183: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   443E 21 07 00      [10]  831 	ld	hl, #0x0007
   4441 19            [11]  832 	add	hl,de
   4442 DD 75 F4      [19]  833 	ld	-12 (ix), l
   4445 DD 74 F5      [19]  834 	ld	-11 (ix), h
                            835 ;src/game.c:180: if (!g_enemies[j].active) continue;
   4448 78            [ 4]  836 	ld	a, b
   4449 B7            [ 4]  837 	or	a, a
   444A CA 42 45      [10]  838 	jp	Z, 00125$
                            839 ;src/game.c:182: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   444D DD 6E FC      [19]  840 	ld	l,-4 (ix)
   4450 DD 66 FD      [19]  841 	ld	h,-3 (ix)
   4453 23            [ 6]  842 	inc	hl
   4454 23            [ 6]  843 	inc	hl
   4455 23            [ 6]  844 	inc	hl
   4456 23            [ 6]  845 	inc	hl
   4457 23            [ 6]  846 	inc	hl
   4458 7E            [ 7]  847 	ld	a, (hl)
   4459 DD 77 F3      [19]  848 	ld	-13 (ix), a
   445C DD 6E FC      [19]  849 	ld	l,-4 (ix)
   445F DD 66 FD      [19]  850 	ld	h,-3 (ix)
   4462 23            [ 6]  851 	inc	hl
   4463 23            [ 6]  852 	inc	hl
   4464 23            [ 6]  853 	inc	hl
   4465 23            [ 6]  854 	inc	hl
   4466 7E            [ 7]  855 	ld	a, (hl)
   4467 DD 77 F2      [19]  856 	ld	-14 (ix), a
   446A DD 6E FC      [19]  857 	ld	l,-4 (ix)
   446D DD 66 FD      [19]  858 	ld	h,-3 (ix)
   4470 23            [ 6]  859 	inc	hl
   4471 46            [ 7]  860 	ld	b, (hl)
   4472 DD 70 F0      [19]  861 	ld	-16 (ix), b
   4475 DD 36 F1 00   [19]  862 	ld	-15 (ix), #0x00
   4479 DD 6E FC      [19]  863 	ld	l,-4 (ix)
   447C DD 66 FD      [19]  864 	ld	h,-3 (ix)
   447F 46            [ 7]  865 	ld	b, (hl)
   4480 DD 70 EE      [19]  866 	ld	-18 (ix), b
   4483 DD 36 EF 00   [19]  867 	ld	-17 (ix), #0x00
                            868 ;src/game.c:181: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4487 DD 6E FA      [19]  869 	ld	l,-6 (ix)
   448A DD 66 FB      [19]  870 	ld	h,-5 (ix)
   448D 7E            [ 7]  871 	ld	a, (hl)
   448E DD 77 ED      [19]  872 	ld	-19 (ix), a
   4491 DD 6E F8      [19]  873 	ld	l,-8 (ix)
   4494 DD 66 F9      [19]  874 	ld	h,-7 (ix)
   4497 46            [ 7]  875 	ld	b, (hl)
   4498 DD 6E F6      [19]  876 	ld	l,-10 (ix)
   449B DD 66 F7      [19]  877 	ld	h,-9 (ix)
   449E 6E            [ 7]  878 	ld	l, (hl)
   449F DD 75 EB      [19]  879 	ld	-21 (ix), l
   44A2 DD 36 EC 00   [19]  880 	ld	-20 (ix), #0x00
   44A6 1A            [ 7]  881 	ld	a, (de)
   44A7 DD 77 E9      [19]  882 	ld	-23 (ix), a
   44AA DD 36 EA 00   [19]  883 	ld	-22 (ix), #0x00
   44AE C5            [11]  884 	push	bc
   44AF D5            [11]  885 	push	de
   44B0 DD 66 F3      [19]  886 	ld	h, -13 (ix)
   44B3 DD 6E F2      [19]  887 	ld	l, -14 (ix)
   44B6 E5            [11]  888 	push	hl
   44B7 DD 6E F0      [19]  889 	ld	l,-16 (ix)
   44BA DD 66 F1      [19]  890 	ld	h,-15 (ix)
   44BD E5            [11]  891 	push	hl
   44BE DD 6E EE      [19]  892 	ld	l,-18 (ix)
   44C1 DD 66 EF      [19]  893 	ld	h,-17 (ix)
   44C4 E5            [11]  894 	push	hl
   44C5 DD 7E ED      [19]  895 	ld	a, -19 (ix)
   44C8 F5            [11]  896 	push	af
   44C9 33            [ 6]  897 	inc	sp
   44CA C5            [11]  898 	push	bc
   44CB 33            [ 6]  899 	inc	sp
   44CC DD 6E EB      [19]  900 	ld	l,-21 (ix)
   44CF DD 66 EC      [19]  901 	ld	h,-20 (ix)
   44D2 E5            [11]  902 	push	hl
   44D3 DD 6E E9      [19]  903 	ld	l,-23 (ix)
   44D6 DD 66 EA      [19]  904 	ld	h,-22 (ix)
   44D9 E5            [11]  905 	push	hl
   44DA CD 19 40      [17]  906 	call	_rect_overlap
   44DD FD 21 0C 00   [14]  907 	ld	iy, #12
   44E1 FD 39         [15]  908 	add	iy, sp
   44E3 FD F9         [10]  909 	ld	sp, iy
   44E5 D1            [10]  910 	pop	de
   44E6 C1            [10]  911 	pop	bc
   44E7 7D            [ 4]  912 	ld	a, l
   44E8 B7            [ 4]  913 	or	a, a
   44E9 28 57         [12]  914 	jr	Z,00125$
                            915 ;src/game.c:183: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   44EB DD 6E F4      [19]  916 	ld	l,-12 (ix)
   44EE DD 66 F5      [19]  917 	ld	h,-11 (ix)
   44F1 66            [ 7]  918 	ld	h, (hl)
   44F2 DD 6E FC      [19]  919 	ld	l, -4 (ix)
   44F5 DD 46 FD      [19]  920 	ld	b, -3 (ix)
   44F8 C5            [11]  921 	push	bc
   44F9 D5            [11]  922 	push	de
   44FA E5            [11]  923 	push	hl
   44FB 33            [ 6]  924 	inc	sp
   44FC 60            [ 4]  925 	ld	h, b
   44FD E5            [11]  926 	push	hl
   44FE CD B7 55      [17]  927 	call	_enemydamage
   4501 F1            [10]  928 	pop	af
   4502 33            [ 6]  929 	inc	sp
   4503 D1            [10]  930 	pop	de
   4504 C1            [10]  931 	pop	bc
   4505 7D            [ 4]  932 	ld	a, l
   4506 B7            [ 4]  933 	or	a, a
   4507 28 2F         [12]  934 	jr	Z,00124$
                            935 ;src/game.c:184: g_score = (u16)(g_score + g_enemies[j].reward);
   4509 DD 6E FC      [19]  936 	ld	l,-4 (ix)
   450C DD 66 FD      [19]  937 	ld	h,-3 (ix)
   450F C5            [11]  938 	push	bc
   4510 01 08 00      [10]  939 	ld	bc, #0x0008
   4513 09            [11]  940 	add	hl, bc
   4514 C1            [10]  941 	pop	bc
   4515 6E            [ 7]  942 	ld	l, (hl)
   4516 DD 75 E9      [19]  943 	ld	-23 (ix), l
   4519 DD 36 EA 00   [19]  944 	ld	-22 (ix), #0x00
   451D 21 F1 5E      [10]  945 	ld	hl, #_g_score
   4520 7E            [ 7]  946 	ld	a, (hl)
   4521 DD 86 E9      [19]  947 	add	a, -23 (ix)
   4524 77            [ 7]  948 	ld	(hl), a
   4525 23            [ 6]  949 	inc	hl
   4526 7E            [ 7]  950 	ld	a, (hl)
   4527 DD 8E EA      [19]  951 	adc	a, -22 (ix)
   452A 77            [ 7]  952 	ld	(hl), a
                            953 ;src/game.c:185: if (g_aliveenemies) g_aliveenemies--;
   452B FD 21 F7 5E   [14]  954 	ld	iy, #_g_aliveenemies
   452F FD 7E 00      [19]  955 	ld	a, 0 (iy)
   4532 B7            [ 4]  956 	or	a, a
   4533 28 03         [12]  957 	jr	Z,00124$
   4535 FD 35 00      [23]  958 	dec	0 (iy)
   4538                     959 00124$:
                            960 ;src/game.c:187: g_projectiles[i].active = 0;
   4538 DD 6E FE      [19]  961 	ld	l,-2 (ix)
   453B DD 66 FF      [19]  962 	ld	h,-1 (ix)
   453E 36 00         [10]  963 	ld	(hl), #0x00
                            964 ;src/game.c:188: break;
   4540 18 0B         [12]  965 	jr	00126$
   4542                     966 00125$:
                            967 ;src/game.c:179: for (j = 0; j < MAX_ENEMIES; ++j) {
   4542 DD 34 E7      [23]  968 	inc	-25 (ix)
   4545 DD 7E E7      [19]  969 	ld	a, -25 (ix)
   4548 D6 06         [ 7]  970 	sub	a, #0x06
   454A DA FA 43      [10]  971 	jp	C, 00199$
   454D                     972 00126$:
                            973 ;src/game.c:191: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   454D 3A 0D 5F      [13]  974 	ld	a,(#_g_bossactive + 0)
   4550 B7            [ 4]  975 	or	a, a
   4551 CA 14 46      [10]  976 	jp	Z, 00133$
   4554 DD 6E FE      [19]  977 	ld	l,-2 (ix)
   4557 DD 66 FF      [19]  978 	ld	h,-1 (ix)
   455A 7E            [ 7]  979 	ld	a, (hl)
   455B B7            [ 4]  980 	or	a, a
   455C CA 14 46      [10]  981 	jp	Z, 00133$
                            982 ;src/game.c:192: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   455F 21 08 5F      [10]  983 	ld	hl, #(_g_boss + 0x0005) + 0
   4562 46            [ 7]  984 	ld	b, (hl)
   4563 3A 07 5F      [13]  985 	ld	a, (#(_g_boss + 0x0004) + 0)
   4566 21 04 5F      [10]  986 	ld	hl, #(_g_boss + 0x0001) + 0
   4569 6E            [ 7]  987 	ld	l, (hl)
   456A DD 75 E9      [19]  988 	ld	-23 (ix), l
   456D DD 36 EA 00   [19]  989 	ld	-22 (ix), #0x00
   4571 21 03 5F      [10]  990 	ld	hl, #_g_boss + 0
   4574 6E            [ 7]  991 	ld	l, (hl)
   4575 DD 75 EB      [19]  992 	ld	-21 (ix), l
   4578 DD 36 EC 00   [19]  993 	ld	-20 (ix), #0x00
                            994 ;src/game.c:191: if (g_bossactive && g_projectiles[i].active && rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   457C DD 6E FA      [19]  995 	ld	l,-6 (ix)
   457F DD 66 FB      [19]  996 	ld	h,-5 (ix)
   4582 F5            [11]  997 	push	af
   4583 7E            [ 7]  998 	ld	a, (hl)
   4584 DD 77 ED      [19]  999 	ld	-19 (ix), a
   4587 F1            [10] 1000 	pop	af
   4588 DD 6E F8      [19] 1001 	ld	l,-8 (ix)
   458B DD 66 F9      [19] 1002 	ld	h,-7 (ix)
   458E F5            [11] 1003 	push	af
   458F 7E            [ 7] 1004 	ld	a, (hl)
   4590 DD 77 EE      [19] 1005 	ld	-18 (ix), a
   4593 F1            [10] 1006 	pop	af
   4594 DD 6E F6      [19] 1007 	ld	l,-10 (ix)
   4597 DD 66 F7      [19] 1008 	ld	h,-9 (ix)
   459A 6E            [ 7] 1009 	ld	l, (hl)
   459B DD 75 F0      [19] 1010 	ld	-16 (ix), l
   459E DD 36 F1 00   [19] 1011 	ld	-15 (ix), #0x00
   45A2 F5            [11] 1012 	push	af
   45A3 1A            [ 7] 1013 	ld	a, (de)
   45A4 5F            [ 4] 1014 	ld	e, a
   45A5 F1            [10] 1015 	pop	af
   45A6 16 00         [ 7] 1016 	ld	d, #0x00
   45A8 C5            [11] 1017 	push	bc
   45A9 C5            [11] 1018 	push	bc
   45AA 33            [ 6] 1019 	inc	sp
   45AB F5            [11] 1020 	push	af
   45AC 33            [ 6] 1021 	inc	sp
   45AD DD 6E E9      [19] 1022 	ld	l,-23 (ix)
   45B0 DD 66 EA      [19] 1023 	ld	h,-22 (ix)
   45B3 E5            [11] 1024 	push	hl
   45B4 DD 6E EB      [19] 1025 	ld	l,-21 (ix)
   45B7 DD 66 EC      [19] 1026 	ld	h,-20 (ix)
   45BA E5            [11] 1027 	push	hl
   45BB DD 66 ED      [19] 1028 	ld	h, -19 (ix)
   45BE DD 6E EE      [19] 1029 	ld	l, -18 (ix)
   45C1 E5            [11] 1030 	push	hl
   45C2 DD 6E F0      [19] 1031 	ld	l,-16 (ix)
   45C5 DD 66 F1      [19] 1032 	ld	h,-15 (ix)
   45C8 E5            [11] 1033 	push	hl
   45C9 D5            [11] 1034 	push	de
   45CA CD 19 40      [17] 1035 	call	_rect_overlap
   45CD FD 21 0C 00   [14] 1036 	ld	iy, #12
   45D1 FD 39         [15] 1037 	add	iy, sp
   45D3 FD F9         [10] 1038 	ld	sp, iy
   45D5 C1            [10] 1039 	pop	bc
   45D6 7D            [ 4] 1040 	ld	a, l
   45D7 B7            [ 4] 1041 	or	a, a
   45D8 28 3A         [12] 1042 	jr	Z,00133$
                           1043 ;src/game.c:193: g_projectiles[i].active = 0;
   45DA DD 6E FE      [19] 1044 	ld	l,-2 (ix)
   45DD DD 66 FF      [19] 1045 	ld	h,-1 (ix)
   45E0 36 00         [10] 1046 	ld	(hl), #0x00
                           1047 ;src/game.c:194: if (enemydamage(&g_boss, g_projectiles[i].damage)) {
   45E2 DD 6E F4      [19] 1048 	ld	l,-12 (ix)
   45E5 DD 66 F5      [19] 1049 	ld	h,-11 (ix)
   45E8 46            [ 7] 1050 	ld	b, (hl)
   45E9 11 03 5F      [10] 1051 	ld	de, #_g_boss
   45EC C5            [11] 1052 	push	bc
   45ED C5            [11] 1053 	push	bc
   45EE 33            [ 6] 1054 	inc	sp
   45EF D5            [11] 1055 	push	de
   45F0 CD B7 55      [17] 1056 	call	_enemydamage
   45F3 F1            [10] 1057 	pop	af
   45F4 33            [ 6] 1058 	inc	sp
   45F5 C1            [10] 1059 	pop	bc
   45F6 7D            [ 4] 1060 	ld	a, l
   45F7 B7            [ 4] 1061 	or	a, a
   45F8 28 1A         [12] 1062 	jr	Z,00133$
                           1063 ;src/game.c:195: g_bossactive = 0;
   45FA 21 0D 5F      [10] 1064 	ld	hl,#_g_bossactive + 0
   45FD 36 00         [10] 1065 	ld	(hl), #0x00
                           1066 ;src/game.c:196: g_score = (u16)(g_score + g_boss.reward);
   45FF 21 0B 5F      [10] 1067 	ld	hl, #_g_boss + 8
   4602 5E            [ 7] 1068 	ld	e, (hl)
   4603 16 00         [ 7] 1069 	ld	d, #0x00
   4605 21 F1 5E      [10] 1070 	ld	hl, #_g_score
   4608 7E            [ 7] 1071 	ld	a, (hl)
   4609 83            [ 4] 1072 	add	a, e
   460A 77            [ 7] 1073 	ld	(hl), a
   460B 23            [ 6] 1074 	inc	hl
   460C 7E            [ 7] 1075 	ld	a, (hl)
   460D 8A            [ 4] 1076 	adc	a, d
   460E 77            [ 7] 1077 	ld	(hl), a
                           1078 ;src/game.c:197: g_victory = 1;
   460F 21 FB 5E      [10] 1079 	ld	hl,#_g_victory + 0
   4612 36 01         [10] 1080 	ld	(hl), #0x01
   4614                    1081 00133$:
                           1082 ;src/game.c:177: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4614 0C            [ 4] 1083 	inc	c
   4615 79            [ 4] 1084 	ld	a, c
   4616 D6 06         [ 7] 1085 	sub	a, #0x06
   4618 DA D9 43      [10] 1086 	jp	C, 00200$
                           1087 ;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
                           1088 ;src/game.c:202: if (!g_damagecooldown) {
   461B 3A F9 5E      [13] 1089 	ld	a,(#_g_damagecooldown + 0)
   461E B7            [ 4] 1090 	or	a, a
   461F C2 A8 47      [10] 1091 	jp	NZ, 00155$
                           1092 ;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
   4622 DD 36 E8 00   [19] 1093 	ld	-24 (ix), #0x00
   4626                    1094 00201$:
                           1095 ;src/game.c:204: if (!g_enemies[i].active) continue;
   4626 DD 4E E8      [19] 1096 	ld	c,-24 (ix)
   4629 06 00         [ 7] 1097 	ld	b,#0x00
   462B 69            [ 4] 1098 	ld	l, c
   462C 60            [ 4] 1099 	ld	h, b
   462D 29            [11] 1100 	add	hl, hl
   462E 29            [11] 1101 	add	hl, hl
   462F 09            [11] 1102 	add	hl, bc
   4630 29            [11] 1103 	add	hl, hl
   4631 01 78 5E      [10] 1104 	ld	bc,#_g_enemies
   4634 09            [11] 1105 	add	hl,bc
   4635 DD 75 E9      [19] 1106 	ld	-23 (ix), l
   4638 DD 74 EA      [19] 1107 	ld	-22 (ix), h
   463B C1            [10] 1108 	pop	bc
   463C E1            [10] 1109 	pop	hl
   463D E5            [11] 1110 	push	hl
   463E C5            [11] 1111 	push	bc
   463F 11 06 00      [10] 1112 	ld	de, #0x0006
   4642 19            [11] 1113 	add	hl, de
   4643 4E            [ 7] 1114 	ld	c, (hl)
   4644 79            [ 4] 1115 	ld	a, c
   4645 B7            [ 4] 1116 	or	a, a
   4646 CA D3 46      [10] 1117 	jp	Z, 00141$
                           1118 ;src/game.c:206: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   4649 C1            [10] 1119 	pop	bc
   464A E1            [10] 1120 	pop	hl
   464B E5            [11] 1121 	push	hl
   464C C5            [11] 1122 	push	bc
   464D 11 05 00      [10] 1123 	ld	de, #0x0005
   4650 19            [11] 1124 	add	hl, de
   4651 7E            [ 7] 1125 	ld	a, (hl)
   4652 DD 77 EB      [19] 1126 	ld	-21 (ix), a
   4655 C1            [10] 1127 	pop	bc
   4656 E1            [10] 1128 	pop	hl
   4657 E5            [11] 1129 	push	hl
   4658 C5            [11] 1130 	push	bc
   4659 11 04 00      [10] 1131 	ld	de, #0x0004
   465C 19            [11] 1132 	add	hl, de
   465D 7E            [ 7] 1133 	ld	a, (hl)
   465E DD 77 ED      [19] 1134 	ld	-19 (ix), a
   4661 C1            [10] 1135 	pop	bc
   4662 E1            [10] 1136 	pop	hl
   4663 E5            [11] 1137 	push	hl
   4664 C5            [11] 1138 	push	bc
   4665 23            [ 6] 1139 	inc	hl
   4666 5E            [ 7] 1140 	ld	e, (hl)
   4667 16 00         [ 7] 1141 	ld	d, #0x00
   4669 DD 6E E9      [19] 1142 	ld	l,-23 (ix)
   466C DD 66 EA      [19] 1143 	ld	h,-22 (ix)
   466F 4E            [ 7] 1144 	ld	c, (hl)
   4670 06 00         [ 7] 1145 	ld	b, #0x00
                           1146 ;src/game.c:205: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4672 3A 73 5E      [13] 1147 	ld	a,(#(_g_player + 0x0005) + 0)
   4675 DD 77 E9      [19] 1148 	ld	-23 (ix), a
   4678 3A 72 5E      [13] 1149 	ld	a,(#(_g_player + 0x0004) + 0)
   467B DD 77 EE      [19] 1150 	ld	-18 (ix), a
   467E 3A 6F 5E      [13] 1151 	ld	a, (#(_g_player + 0x0001) + 0)
   4681 DD 77 F0      [19] 1152 	ld	-16 (ix), a
   4684 DD 36 F1 00   [19] 1153 	ld	-15 (ix), #0x00
   4688 3A 6E 5E      [13] 1154 	ld	a, (#_g_player + 0)
   468B DD 77 F4      [19] 1155 	ld	-12 (ix), a
   468E DD 36 F5 00   [19] 1156 	ld	-11 (ix), #0x00
   4692 DD 66 EB      [19] 1157 	ld	h, -21 (ix)
   4695 DD 6E ED      [19] 1158 	ld	l, -19 (ix)
   4698 E5            [11] 1159 	push	hl
   4699 D5            [11] 1160 	push	de
   469A C5            [11] 1161 	push	bc
   469B DD 66 E9      [19] 1162 	ld	h, -23 (ix)
   469E DD 6E EE      [19] 1163 	ld	l, -18 (ix)
   46A1 E5            [11] 1164 	push	hl
   46A2 DD 6E F0      [19] 1165 	ld	l,-16 (ix)
   46A5 DD 66 F1      [19] 1166 	ld	h,-15 (ix)
   46A8 E5            [11] 1167 	push	hl
   46A9 DD 6E F4      [19] 1168 	ld	l,-12 (ix)
   46AC DD 66 F5      [19] 1169 	ld	h,-11 (ix)
   46AF E5            [11] 1170 	push	hl
   46B0 CD 19 40      [17] 1171 	call	_rect_overlap
   46B3 FD 21 0C 00   [14] 1172 	ld	iy, #12
   46B7 FD 39         [15] 1173 	add	iy, sp
   46B9 FD F9         [10] 1174 	ld	sp, iy
   46BB 7D            [ 4] 1175 	ld	a, l
   46BC B7            [ 4] 1176 	or	a, a
   46BD 28 14         [12] 1177 	jr	Z,00141$
                           1178 ;src/game.c:207: if (g_lives) g_lives--;
   46BF FD 21 F0 5E   [14] 1179 	ld	iy, #_g_lives
   46C3 FD 7E 00      [19] 1180 	ld	a, 0 (iy)
   46C6 B7            [ 4] 1181 	or	a, a
   46C7 28 03         [12] 1182 	jr	Z,00138$
   46C9 FD 35 00      [23] 1183 	dec	0 (iy)
   46CC                    1184 00138$:
                           1185 ;src/game.c:208: g_damagecooldown = 40;
   46CC 21 F9 5E      [10] 1186 	ld	hl,#_g_damagecooldown + 0
   46CF 36 28         [10] 1187 	ld	(hl), #0x28
                           1188 ;src/game.c:209: break;
   46D1 18 0B         [12] 1189 	jr	00142$
   46D3                    1190 00141$:
                           1191 ;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
   46D3 DD 34 E8      [23] 1192 	inc	-24 (ix)
   46D6 DD 7E E8      [19] 1193 	ld	a, -24 (ix)
   46D9 D6 06         [ 7] 1194 	sub	a, #0x06
   46DB DA 26 46      [10] 1195 	jp	C, 00201$
   46DE                    1196 00142$:
                           1197 ;src/game.c:213: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   46DE 3A F9 5E      [13] 1198 	ld	a,(#_g_damagecooldown + 0)
   46E1 B7            [ 4] 1199 	or	a, a
   46E2 C2 62 47      [10] 1200 	jp	NZ, 00146$
   46E5 3A 0D 5F      [13] 1201 	ld	a,(#_g_bossactive + 0)
   46E8 B7            [ 4] 1202 	or	a, a
   46E9 28 77         [12] 1203 	jr	Z,00146$
                           1204 ;src/game.c:214: (i16)g_boss.x, (i16)g_boss.y, g_boss.w, g_boss.h)) {
   46EB 3A 08 5F      [13] 1205 	ld	a,(#(_g_boss + 0x0005) + 0)
   46EE DD 77 E9      [19] 1206 	ld	-23 (ix), a
   46F1 3A 07 5F      [13] 1207 	ld	a,(#(_g_boss + 0x0004) + 0)
   46F4 DD 77 EB      [19] 1208 	ld	-21 (ix), a
   46F7 21 04 5F      [10] 1209 	ld	hl, #(_g_boss + 0x0001) + 0
   46FA 5E            [ 7] 1210 	ld	e, (hl)
   46FB 16 00         [ 7] 1211 	ld	d, #0x00
   46FD 21 03 5F      [10] 1212 	ld	hl, #_g_boss + 0
   4700 4E            [ 7] 1213 	ld	c, (hl)
   4701 06 00         [ 7] 1214 	ld	b, #0x00
                           1215 ;src/game.c:213: if (!g_damagecooldown && g_bossactive && rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   4703 3A 73 5E      [13] 1216 	ld	a,(#(_g_player + 0x0005) + 0)
   4706 DD 77 ED      [19] 1217 	ld	-19 (ix), a
   4709 3A 72 5E      [13] 1218 	ld	a,(#(_g_player + 0x0004) + 0)
   470C DD 77 EE      [19] 1219 	ld	-18 (ix), a
   470F 3A 6F 5E      [13] 1220 	ld	a, (#(_g_player + 0x0001) + 0)
   4712 DD 77 F0      [19] 1221 	ld	-16 (ix), a
   4715 DD 36 F1 00   [19] 1222 	ld	-15 (ix), #0x00
   4719 3A 6E 5E      [13] 1223 	ld	a, (#_g_player + 0)
   471C DD 77 F4      [19] 1224 	ld	-12 (ix), a
   471F DD 36 F5 00   [19] 1225 	ld	-11 (ix), #0x00
   4723 DD 66 E9      [19] 1226 	ld	h, -23 (ix)
   4726 DD 6E EB      [19] 1227 	ld	l, -21 (ix)
   4729 E5            [11] 1228 	push	hl
   472A D5            [11] 1229 	push	de
   472B C5            [11] 1230 	push	bc
   472C DD 66 ED      [19] 1231 	ld	h, -19 (ix)
   472F DD 6E EE      [19] 1232 	ld	l, -18 (ix)
   4732 E5            [11] 1233 	push	hl
   4733 DD 6E F0      [19] 1234 	ld	l,-16 (ix)
   4736 DD 66 F1      [19] 1235 	ld	h,-15 (ix)
   4739 E5            [11] 1236 	push	hl
   473A DD 6E F4      [19] 1237 	ld	l,-12 (ix)
   473D DD 66 F5      [19] 1238 	ld	h,-11 (ix)
   4740 E5            [11] 1239 	push	hl
   4741 CD 19 40      [17] 1240 	call	_rect_overlap
   4744 FD 21 0C 00   [14] 1241 	ld	iy, #12
   4748 FD 39         [15] 1242 	add	iy, sp
   474A FD F9         [10] 1243 	ld	sp, iy
   474C 7D            [ 4] 1244 	ld	a, l
   474D B7            [ 4] 1245 	or	a, a
   474E 28 12         [12] 1246 	jr	Z,00146$
                           1247 ;src/game.c:215: if (g_lives) g_lives--;
   4750 FD 21 F0 5E   [14] 1248 	ld	iy, #_g_lives
   4754 FD 7E 00      [19] 1249 	ld	a, 0 (iy)
   4757 B7            [ 4] 1250 	or	a, a
   4758 28 03         [12] 1251 	jr	Z,00144$
   475A FD 35 00      [23] 1252 	dec	0 (iy)
   475D                    1253 00144$:
                           1254 ;src/game.c:216: g_damagecooldown = 40;
   475D 21 F9 5E      [10] 1255 	ld	hl,#_g_damagecooldown + 0
   4760 36 28         [10] 1256 	ld	(hl), #0x28
   4762                    1257 00146$:
                           1258 ;src/game.c:219: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   4762 3A F9 5E      [13] 1259 	ld	a,(#_g_damagecooldown + 0)
   4765 B7            [ 4] 1260 	or	a, a
   4766 20 40         [12] 1261 	jr	NZ,00155$
   4768 3A 73 5E      [13] 1262 	ld	a, (#(_g_player + 0x0005) + 0)
   476B 21 72 5E      [10] 1263 	ld	hl, #(_g_player + 0x0004) + 0
   476E 56            [ 7] 1264 	ld	d, (hl)
   476F 21 6F 5E      [10] 1265 	ld	hl, #(_g_player + 0x0001) + 0
   4772 4E            [ 7] 1266 	ld	c, (hl)
   4773 06 00         [ 7] 1267 	ld	b, #0x00
   4775 21 6E 5E      [10] 1268 	ld	hl, #_g_player + 0
   4778 6E            [ 7] 1269 	ld	l, (hl)
   4779 DD 75 E9      [19] 1270 	ld	-23 (ix), l
   477C DD 36 EA 00   [19] 1271 	ld	-22 (ix), #0x00
   4780 F5            [11] 1272 	push	af
   4781 33            [ 6] 1273 	inc	sp
   4782 D5            [11] 1274 	push	de
   4783 33            [ 6] 1275 	inc	sp
   4784 C5            [11] 1276 	push	bc
   4785 DD 6E E9      [19] 1277 	ld	l,-23 (ix)
   4788 DD 66 EA      [19] 1278 	ld	h,-22 (ix)
   478B E5            [11] 1279 	push	hl
   478C CD 51 4B      [17] 1280 	call	_collision_is_on_trap
   478F F1            [10] 1281 	pop	af
   4790 F1            [10] 1282 	pop	af
   4791 F1            [10] 1283 	pop	af
   4792 7D            [ 4] 1284 	ld	a, l
   4793 B7            [ 4] 1285 	or	a, a
   4794 28 12         [12] 1286 	jr	Z,00155$
                           1287 ;src/game.c:220: if (g_lives) g_lives--;
   4796 FD 21 F0 5E   [14] 1288 	ld	iy, #_g_lives
   479A FD 7E 00      [19] 1289 	ld	a, 0 (iy)
   479D B7            [ 4] 1290 	or	a, a
   479E 28 03         [12] 1291 	jr	Z,00150$
   47A0 FD 35 00      [23] 1292 	dec	0 (iy)
   47A3                    1293 00150$:
                           1294 ;src/game.c:221: g_damagecooldown = 40;
   47A3 21 F9 5E      [10] 1295 	ld	hl,#_g_damagecooldown + 0
   47A6 36 28         [10] 1296 	ld	(hl), #0x28
   47A8                    1297 00155$:
                           1298 ;src/game.c:225: if (g_lives == 0) {
   47A8 3A F0 5E      [13] 1299 	ld	a,(#_g_lives + 0)
   47AB B7            [ 4] 1300 	or	a, a
   47AC 20 1A         [12] 1301 	jr	NZ,00160$
                           1302 ;src/game.c:226: if (g_checkpointactive) {
   47AE 3A 01 5F      [13] 1303 	ld	a,(#_g_checkpointactive + 0)
   47B1 B7            [ 4] 1304 	or	a, a
   47B2 28 0F         [12] 1305 	jr	Z,00157$
                           1306 ;src/game.c:227: g_lives = 2;
   47B4 21 F0 5E      [10] 1307 	ld	hl,#_g_lives + 0
   47B7 36 02         [10] 1308 	ld	(hl), #0x02
                           1309 ;src/game.c:228: reset_player_to_checkpoint();
   47B9 CD 00 40      [17] 1310 	call	_reset_player_to_checkpoint
                           1311 ;src/game.c:229: g_damagecooldown = 50;
   47BC 21 F9 5E      [10] 1312 	ld	hl,#_g_damagecooldown + 0
   47BF 36 32         [10] 1313 	ld	(hl), #0x32
   47C1 18 05         [12] 1314 	jr	00160$
   47C3                    1315 00157$:
                           1316 ;src/game.c:231: g_gameover = 1;
   47C3 21 FC 5E      [10] 1317 	ld	hl,#_g_gameover + 0
   47C6 36 01         [10] 1318 	ld	(hl), #0x01
   47C8                    1319 00160$:
                           1320 ;src/game.c:235: if (!g_checkpointactive && g_player.x >= 44) {
   47C8 FD 21 01 5F   [14] 1321 	ld	iy, #_g_checkpointactive
   47CC FD 7E 00      [19] 1322 	ld	a, 0 (iy)
   47CF B7            [ 4] 1323 	or	a, a
   47D0 20 15         [12] 1324 	jr	NZ,00162$
   47D2 3A 6E 5E      [13] 1325 	ld	a, (#_g_player + 0)
   47D5 D6 2C         [ 7] 1326 	sub	a, #0x2c
   47D7 38 0E         [12] 1327 	jr	C,00162$
                           1328 ;src/game.c:236: g_checkpointactive = 1;
   47D9 FD 36 00 01   [19] 1329 	ld	0 (iy), #0x01
                           1330 ;src/game.c:237: g_checkpointx = 44;
   47DD 21 FF 5E      [10] 1331 	ld	hl,#_g_checkpointx + 0
   47E0 36 2C         [10] 1332 	ld	(hl), #0x2c
                           1333 ;src/game.c:238: g_checkpointy = 120;
   47E2 21 00 5F      [10] 1334 	ld	hl,#_g_checkpointy + 0
   47E5 36 78         [10] 1335 	ld	(hl), #0x78
   47E7                    1336 00162$:
                           1337 ;src/game.c:241: if (!g_hiddenrewardtaken && tilemap_is_hidden_zone((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   47E7 3A 02 5F      [13] 1338 	ld	a,(#_g_hiddenrewardtaken + 0)
   47EA B7            [ 4] 1339 	or	a, a
   47EB 20 5B         [12] 1340 	jr	NZ,00169$
   47ED 3A 73 5E      [13] 1341 	ld	a, (#(_g_player + 0x0005) + 0)
   47F0 21 72 5E      [10] 1342 	ld	hl, #(_g_player + 0x0004) + 0
   47F3 56            [ 7] 1343 	ld	d, (hl)
   47F4 21 6F 5E      [10] 1344 	ld	hl, #(_g_player + 0x0001) + 0
   47F7 4E            [ 7] 1345 	ld	c, (hl)
   47F8 06 00         [ 7] 1346 	ld	b, #0x00
   47FA 21 6E 5E      [10] 1347 	ld	hl, #_g_player + 0
   47FD 6E            [ 7] 1348 	ld	l, (hl)
   47FE DD 75 E9      [19] 1349 	ld	-23 (ix), l
   4801 DD 36 EA 00   [19] 1350 	ld	-22 (ix), #0x00
   4805 F5            [11] 1351 	push	af
   4806 33            [ 6] 1352 	inc	sp
   4807 D5            [11] 1353 	push	de
   4808 33            [ 6] 1354 	inc	sp
   4809 C5            [11] 1355 	push	bc
   480A DD 6E E9      [19] 1356 	ld	l,-23 (ix)
   480D DD 66 EA      [19] 1357 	ld	h,-22 (ix)
   4810 E5            [11] 1358 	push	hl
   4811 CD E4 50      [17] 1359 	call	_tilemap_is_hidden_zone
   4814 F1            [10] 1360 	pop	af
   4815 F1            [10] 1361 	pop	af
   4816 F1            [10] 1362 	pop	af
   4817 7D            [ 4] 1363 	ld	a, l
   4818 B7            [ 4] 1364 	or	a, a
   4819 28 2D         [12] 1365 	jr	Z,00169$
                           1366 ;src/game.c:242: g_hiddenrewardtaken = 1;
   481B 21 02 5F      [10] 1367 	ld	hl,#_g_hiddenrewardtaken + 0
   481E 36 01         [10] 1368 	ld	(hl), #0x01
                           1369 ;src/game.c:243: if (g_lives < 5) g_lives++;
   4820 FD 21 F0 5E   [14] 1370 	ld	iy, #_g_lives
   4824 FD 7E 00      [19] 1371 	ld	a, 0 (iy)
   4827 D6 05         [ 7] 1372 	sub	a, #0x05
   4829 30 03         [12] 1373 	jr	NC,00165$
   482B FD 34 00      [23] 1374 	inc	0 (iy)
   482E                    1375 00165$:
                           1376 ;src/game.c:244: if (g_weaponlevel < 2) g_weaponlevel++;
   482E FD 21 F4 5E   [14] 1377 	ld	iy, #_g_weaponlevel
   4832 FD 7E 00      [19] 1378 	ld	a, 0 (iy)
   4835 D6 02         [ 7] 1379 	sub	a, #0x02
   4837 30 03         [12] 1380 	jr	NC,00167$
   4839 FD 34 00      [23] 1381 	inc	0 (iy)
   483C                    1382 00167$:
                           1383 ;src/game.c:245: g_score = (u16)(g_score + 250);
   483C 21 F1 5E      [10] 1384 	ld	hl, #_g_score
   483F 7E            [ 7] 1385 	ld	a, (hl)
   4840 C6 FA         [ 7] 1386 	add	a, #0xfa
   4842 77            [ 7] 1387 	ld	(hl), a
   4843 23            [ 6] 1388 	inc	hl
   4844 7E            [ 7] 1389 	ld	a, (hl)
   4845 CE 00         [ 7] 1390 	adc	a, #0x00
   4847 77            [ 7] 1391 	ld	(hl), a
   4848                    1392 00169$:
                           1393 ;src/game.c:248: if (g_score >= 800 && g_weaponlevel < 1) g_weaponlevel = 1;
   4848 FD 21 F1 5E   [14] 1394 	ld	iy, #_g_score
   484C FD 7E 00      [19] 1395 	ld	a, 0 (iy)
   484F D6 20         [ 7] 1396 	sub	a, #0x20
   4851 FD 7E 01      [19] 1397 	ld	a, 1 (iy)
   4854 DE 03         [ 7] 1398 	sbc	a, #0x03
   4856 38 0F         [12] 1399 	jr	C,00172$
   4858 FD 21 F4 5E   [14] 1400 	ld	iy, #_g_weaponlevel
   485C FD 7E 00      [19] 1401 	ld	a, 0 (iy)
   485F D6 01         [ 7] 1402 	sub	a, #0x01
   4861 30 04         [12] 1403 	jr	NC,00172$
   4863 FD 36 00 01   [19] 1404 	ld	0 (iy), #0x01
   4867                    1405 00172$:
                           1406 ;src/game.c:249: if (g_score >= 1600 && g_weaponlevel < 2) g_weaponlevel = 2;
   4867 FD 21 F1 5E   [14] 1407 	ld	iy, #_g_score
   486B FD 7E 00      [19] 1408 	ld	a, 0 (iy)
   486E D6 40         [ 7] 1409 	sub	a, #0x40
   4870 FD 7E 01      [19] 1410 	ld	a, 1 (iy)
   4873 DE 06         [ 7] 1411 	sbc	a, #0x06
   4875 38 0F         [12] 1412 	jr	C,00175$
   4877 FD 21 F4 5E   [14] 1413 	ld	iy, #_g_weaponlevel
   487B FD 7E 00      [19] 1414 	ld	a, 0 (iy)
   487E D6 02         [ 7] 1415 	sub	a, #0x02
   4880 30 04         [12] 1416 	jr	NC,00175$
   4882 FD 36 00 02   [19] 1417 	ld	0 (iy), #0x02
   4886                    1418 00175$:
                           1419 ;src/game.c:250: g_weapondisplay = (u8)(g_weaponlevel + 1);
   4886 21 F5 5E      [10] 1420 	ld	hl, #_g_weapondisplay
   4889 3A F4 5E      [13] 1421 	ld	a,(#_g_weaponlevel + 0)
   488C 3C            [ 4] 1422 	inc	a
   488D 77            [ 7] 1423 	ld	(hl), a
                           1424 ;src/game.c:252: if (g_aliveenemies == 0 && !g_gameover) {
   488E 3A F7 5E      [13] 1425 	ld	a,(#_g_aliveenemies + 0)
   4891 B7            [ 4] 1426 	or	a, a
   4892 20 43         [12] 1427 	jr	NZ,00187$
   4894 3A FC 5E      [13] 1428 	ld	a,(#_g_gameover + 0)
   4897 B7            [ 4] 1429 	or	a, a
   4898 20 3D         [12] 1430 	jr	NZ,00187$
                           1431 ;src/game.c:253: if (g_currentwave < TOTAL_WAVES) {
   489A 3A F6 5E      [13] 1432 	ld	a,(#_g_currentwave + 0)
   489D D6 03         [ 7] 1433 	sub	a, #0x03
   489F 30 20         [12] 1434 	jr	NC,00184$
                           1435 ;src/game.c:254: if (g_wavecooldown == 0) {
   48A1 3A F8 5E      [13] 1436 	ld	a,(#_g_wavecooldown + 0)
   48A4 B7            [ 4] 1437 	or	a, a
   48A5 20 14         [12] 1438 	jr	NZ,00178$
                           1439 ;src/game.c:255: spawn_wave(g_currentwave);
   48A7 3A F6 5E      [13] 1440 	ld	a, (_g_currentwave)
   48AA F5            [11] 1441 	push	af
   48AB 33            [ 6] 1442 	inc	sp
   48AC CD A6 40      [17] 1443 	call	_spawn_wave
   48AF 33            [ 6] 1444 	inc	sp
                           1445 ;src/game.c:256: g_currentwave++;
   48B0 21 F6 5E      [10] 1446 	ld	hl, #_g_currentwave+0
   48B3 34            [11] 1447 	inc	(hl)
                           1448 ;src/game.c:257: g_wavecooldown = 100;
   48B4 21 F8 5E      [10] 1449 	ld	hl,#_g_wavecooldown + 0
   48B7 36 64         [10] 1450 	ld	(hl), #0x64
   48B9 18 1C         [12] 1451 	jr	00187$
   48BB                    1452 00178$:
                           1453 ;src/game.c:259: g_wavecooldown--;
   48BB 21 F8 5E      [10] 1454 	ld	hl, #_g_wavecooldown+0
   48BE 35            [11] 1455 	dec	(hl)
   48BF 18 16         [12] 1456 	jr	00187$
   48C1                    1457 00184$:
                           1458 ;src/game.c:261: } else if (!g_bossactive && g_player.x >= tilemap_goal_x()) {
   48C1 3A 0D 5F      [13] 1459 	ld	a,(#_g_bossactive + 0)
   48C4 B7            [ 4] 1460 	or	a, a
   48C5 20 10         [12] 1461 	jr	NZ,00187$
   48C7 21 6E 5E      [10] 1462 	ld	hl, #_g_player + 0
   48CA 4E            [ 7] 1463 	ld	c, (hl)
   48CB C5            [11] 1464 	push	bc
   48CC CD 49 51      [17] 1465 	call	_tilemap_goal_x
   48CF C1            [10] 1466 	pop	bc
   48D0 79            [ 4] 1467 	ld	a, c
   48D1 95            [ 4] 1468 	sub	a, l
   48D2 38 03         [12] 1469 	jr	C,00187$
                           1470 ;src/game.c:262: spawn_boss();
   48D4 CD 7B 41      [17] 1471 	call	_spawn_boss
   48D7                    1472 00187$:
                           1473 ;src/game.c:266: g_framecounter++;
   48D7 FD 21 FD 5E   [14] 1474 	ld	iy, #_g_framecounter
   48DB FD 34 00      [23] 1475 	inc	0 (iy)
   48DE 20 03         [12] 1476 	jr	NZ,00445$
   48E0 FD 34 01      [23] 1477 	inc	1 (iy)
   48E3                    1478 00445$:
                           1479 ;src/game.c:267: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   48E3 21 32 00      [10] 1480 	ld	hl, #0x0032
   48E6 E5            [11] 1481 	push	hl
   48E7 2A FD 5E      [16] 1482 	ld	hl, (_g_framecounter)
   48EA E5            [11] 1483 	push	hl
   48EB CD 4C 5D      [17] 1484 	call	__moduint
   48EE F1            [10] 1485 	pop	af
   48EF F1            [10] 1486 	pop	af
   48F0 7C            [ 4] 1487 	ld	a, h
   48F1 B5            [ 4] 1488 	or	a,l
   48F2 20 0D         [12] 1489 	jr	NZ,00190$
   48F4 FD 21 F3 5E   [14] 1490 	ld	iy, #_g_timeleft
   48F8 FD 7E 00      [19] 1491 	ld	a, 0 (iy)
   48FB B7            [ 4] 1492 	or	a, a
   48FC 28 03         [12] 1493 	jr	Z,00190$
                           1494 ;src/game.c:268: g_timeleft--;
   48FE FD 35 00      [23] 1495 	dec	0 (iy)
   4901                    1496 00190$:
                           1497 ;src/game.c:270: if (g_timeleft == 0 && !g_victory) {
   4901 3A F3 5E      [13] 1498 	ld	a,(#_g_timeleft + 0)
   4904 B7            [ 4] 1499 	or	a, a
   4905 20 0B         [12] 1500 	jr	NZ,00193$
   4907 3A FB 5E      [13] 1501 	ld	a,(#_g_victory + 0)
   490A B7            [ 4] 1502 	or	a, a
   490B 20 05         [12] 1503 	jr	NZ,00193$
                           1504 ;src/game.c:271: g_gameover = 1;
   490D 21 FC 5E      [10] 1505 	ld	hl,#_g_gameover + 0
   4910 36 01         [10] 1506 	ld	(hl), #0x01
   4912                    1507 00193$:
                           1508 ;src/game.c:274: hudupdate(g_lives, g_score, g_timeleft, g_weapondisplay);
   4912 3A F5 5E      [13] 1509 	ld	a, (_g_weapondisplay)
   4915 F5            [11] 1510 	push	af
   4916 33            [ 6] 1511 	inc	sp
   4917 3A F3 5E      [13] 1512 	ld	a, (_g_timeleft)
   491A F5            [11] 1513 	push	af
   491B 33            [ 6] 1514 	inc	sp
   491C 2A F1 5E      [16] 1515 	ld	hl, (_g_score)
   491F E5            [11] 1516 	push	hl
   4920 3A F0 5E      [13] 1517 	ld	a, (_g_lives)
   4923 F5            [11] 1518 	push	af
   4924 33            [ 6] 1519 	inc	sp
   4925 CD 20 4D      [17] 1520 	call	_hudupdate
   4928 F1            [10] 1521 	pop	af
   4929 F1            [10] 1522 	pop	af
   492A 33            [ 6] 1523 	inc	sp
   492B                    1524 00202$:
   492B DD F9         [10] 1525 	ld	sp, ix
   492D DD E1         [14] 1526 	pop	ix
   492F C9            [10] 1527 	ret
                           1528 ;src/game.c:277: void game_render(void) {
                           1529 ;	---------------------------------
                           1530 ; Function game_render
                           1531 ; ---------------------------------
   4930                    1532 _game_render::
                           1533 ;src/game.c:280: cpct_clearScreen(0x00);
   4930 21 00 40      [10] 1534 	ld	hl, #0x4000
   4933 E5            [11] 1535 	push	hl
   4934 AF            [ 4] 1536 	xor	a, a
   4935 F5            [11] 1537 	push	af
   4936 33            [ 6] 1538 	inc	sp
   4937 26 C0         [ 7] 1539 	ld	h, #0xc0
   4939 E5            [11] 1540 	push	hl
   493A CD 77 5D      [17] 1541 	call	_cpct_memset
                           1542 ;src/game.c:281: tilemap_render();
   493D CD EE 4E      [17] 1543 	call	_tilemap_render
                           1544 ;src/game.c:283: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4940 0E 00         [ 7] 1545 	ld	c, #0x00
   4942                    1546 00113$:
                           1547 ;src/game.c:284: projectilerender(&g_projectiles[i]);
   4942 06 00         [ 7] 1548 	ld	b,#0x00
   4944 69            [ 4] 1549 	ld	l, c
   4945 60            [ 4] 1550 	ld	h, b
   4946 29            [11] 1551 	add	hl, hl
   4947 29            [11] 1552 	add	hl, hl
   4948 09            [11] 1553 	add	hl, bc
   4949 29            [11] 1554 	add	hl, hl
   494A 11 B4 5E      [10] 1555 	ld	de, #_g_projectiles
   494D 19            [11] 1556 	add	hl, de
   494E C5            [11] 1557 	push	bc
   494F E5            [11] 1558 	push	hl
   4950 CD 73 5B      [17] 1559 	call	_projectilerender
   4953 F1            [10] 1560 	pop	af
   4954 C1            [10] 1561 	pop	bc
                           1562 ;src/game.c:283: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4955 0C            [ 4] 1563 	inc	c
   4956 79            [ 4] 1564 	ld	a, c
   4957 D6 06         [ 7] 1565 	sub	a, #0x06
   4959 38 E7         [12] 1566 	jr	C,00113$
                           1567 ;src/game.c:287: for (i = 0; i < MAX_ENEMIES; ++i) {
   495B 0E 00         [ 7] 1568 	ld	c, #0x00
   495D                    1569 00115$:
                           1570 ;src/game.c:288: enemyrender(&g_enemies[i]);
   495D 06 00         [ 7] 1571 	ld	b,#0x00
   495F 69            [ 4] 1572 	ld	l, c
   4960 60            [ 4] 1573 	ld	h, b
   4961 29            [11] 1574 	add	hl, hl
   4962 29            [11] 1575 	add	hl, hl
   4963 09            [11] 1576 	add	hl, bc
   4964 29            [11] 1577 	add	hl, hl
   4965 11 78 5E      [10] 1578 	ld	de, #_g_enemies
   4968 19            [11] 1579 	add	hl, de
   4969 C5            [11] 1580 	push	bc
   496A E5            [11] 1581 	push	hl
   496B CD 68 55      [17] 1582 	call	_enemyrender
   496E F1            [10] 1583 	pop	af
   496F C1            [10] 1584 	pop	bc
                           1585 ;src/game.c:287: for (i = 0; i < MAX_ENEMIES; ++i) {
   4970 0C            [ 4] 1586 	inc	c
   4971 79            [ 4] 1587 	ld	a, c
   4972 D6 06         [ 7] 1588 	sub	a, #0x06
   4974 38 E7         [12] 1589 	jr	C,00115$
                           1590 ;src/game.c:291: if (g_bossactive) {
   4976 3A 0D 5F      [13] 1591 	ld	a,(#_g_bossactive + 0)
   4979 B7            [ 4] 1592 	or	a, a
   497A 28 08         [12] 1593 	jr	Z,00104$
                           1594 ;src/game.c:292: enemyrender(&g_boss);
   497C 21 03 5F      [10] 1595 	ld	hl, #_g_boss
   497F E5            [11] 1596 	push	hl
   4980 CD 68 55      [17] 1597 	call	_enemyrender
   4983 F1            [10] 1598 	pop	af
   4984                    1599 00104$:
                           1600 ;src/game.c:295: playerrender(&g_player);
   4984 21 6E 5E      [10] 1601 	ld	hl, #_g_player
   4987 E5            [11] 1602 	push	hl
   4988 CD D3 59      [17] 1603 	call	_playerrender
   498B F1            [10] 1604 	pop	af
                           1605 ;src/game.c:296: hudrender();
   498C CD 51 4D      [17] 1606 	call	_hudrender
                           1607 ;src/game.c:298: if (g_victory) {
   498F 3A FB 5E      [13] 1608 	ld	a,(#_g_victory + 0)
   4992 B7            [ 4] 1609 	or	a, a
   4993 28 1B         [12] 1610 	jr	Z,00111$
                           1611 ;src/game.c:299: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
   4995 21 1C 48      [10] 1612 	ld	hl, #0x481c
   4998 E5            [11] 1613 	push	hl
   4999 21 00 C0      [10] 1614 	ld	hl, #0xc000
   499C E5            [11] 1615 	push	hl
   499D CD 4E 5E      [17] 1616 	call	_cpct_getScreenPtr
   49A0 01 18 08      [10] 1617 	ld	bc, #0x0818
   49A3 C5            [11] 1618 	push	bc
   49A4 3E 5C         [ 7] 1619 	ld	a, #0x5c
   49A6 F5            [11] 1620 	push	af
   49A7 33            [ 6] 1621 	inc	sp
   49A8 E5            [11] 1622 	push	hl
   49A9 CD 95 5D      [17] 1623 	call	_cpct_drawSolidBox
   49AC F1            [10] 1624 	pop	af
   49AD F1            [10] 1625 	pop	af
   49AE 33            [ 6] 1626 	inc	sp
   49AF C9            [10] 1627 	ret
   49B0                    1628 00111$:
                           1629 ;src/game.c:300: } else if (g_gameover) {
   49B0 3A FC 5E      [13] 1630 	ld	a,(#_g_gameover + 0)
   49B3 B7            [ 4] 1631 	or	a, a
   49B4 28 1B         [12] 1632 	jr	Z,00108$
                           1633 ;src/game.c:301: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
   49B6 21 1C 48      [10] 1634 	ld	hl, #0x481c
   49B9 E5            [11] 1635 	push	hl
   49BA 21 00 C0      [10] 1636 	ld	hl, #0xc000
   49BD E5            [11] 1637 	push	hl
   49BE CD 4E 5E      [17] 1638 	call	_cpct_getScreenPtr
   49C1 01 18 08      [10] 1639 	ld	bc, #0x0818
   49C4 C5            [11] 1640 	push	bc
   49C5 3E 4C         [ 7] 1641 	ld	a, #0x4c
   49C7 F5            [11] 1642 	push	af
   49C8 33            [ 6] 1643 	inc	sp
   49C9 E5            [11] 1644 	push	hl
   49CA CD 95 5D      [17] 1645 	call	_cpct_drawSolidBox
   49CD F1            [10] 1646 	pop	af
   49CE F1            [10] 1647 	pop	af
   49CF 33            [ 6] 1648 	inc	sp
   49D0 C9            [10] 1649 	ret
   49D1                    1650 00108$:
                           1651 ;src/game.c:302: } else if (g_checkpointactive) {
   49D1 3A 01 5F      [13] 1652 	ld	a,(#_g_checkpointactive + 0)
   49D4 B7            [ 4] 1653 	or	a, a
   49D5 C8            [11] 1654 	ret	Z
                           1655 ;src/game.c:303: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 44, 150), 0x3A, 2, 10);
   49D6 21 2C 96      [10] 1656 	ld	hl, #0x962c
   49D9 E5            [11] 1657 	push	hl
   49DA 21 00 C0      [10] 1658 	ld	hl, #0xc000
   49DD E5            [11] 1659 	push	hl
   49DE CD 4E 5E      [17] 1660 	call	_cpct_getScreenPtr
   49E1 01 02 0A      [10] 1661 	ld	bc, #0x0a02
   49E4 C5            [11] 1662 	push	bc
   49E5 3E 3A         [ 7] 1663 	ld	a, #0x3a
   49E7 F5            [11] 1664 	push	af
   49E8 33            [ 6] 1665 	inc	sp
   49E9 E5            [11] 1666 	push	hl
   49EA CD 95 5D      [17] 1667 	call	_cpct_drawSolidBox
   49ED F1            [10] 1668 	pop	af
   49EE F1            [10] 1669 	pop	af
   49EF 33            [ 6] 1670 	inc	sp
   49F0 C9            [10] 1671 	ret
                           1672 	.area _CODE
                           1673 	.area _INITIALIZER
                           1674 	.area _CABS (ABS)
