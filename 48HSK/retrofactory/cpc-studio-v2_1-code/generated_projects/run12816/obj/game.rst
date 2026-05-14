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
                             31 	.globl _tilemap_render
                             32 	.globl _tilemap_init
                             33 	.globl _cpct_getScreenPtr
                             34 	.globl _cpct_setVideoMode
                             35 	.globl _cpct_drawSolidBox
                             36 	.globl _cpct_memset
                             37 	.globl _cpct_disableFirmware
                             38 	.globl _game_init
                             39 	.globl _game_update
                             40 	.globl _game_render
                             41 ;--------------------------------------------------------
                             42 ; special function registers
                             43 ;--------------------------------------------------------
                             44 ;--------------------------------------------------------
                             45 ; ram data
                             46 ;--------------------------------------------------------
                             47 	.area _DATA
   59F5                      48 _g_player:
   59F5                      49 	.ds 9
   59FE                      50 _g_enemies:
   59FE                      51 	.ds 54
   5A34                      52 _g_projectiles:
   5A34                      53 	.ds 60
   5A70                      54 _g_lives:
   5A70                      55 	.ds 1
   5A71                      56 _g_score:
   5A71                      57 	.ds 2
   5A73                      58 _g_timeleft:
   5A73                      59 	.ds 1
   5A74                      60 _g_weapon:
   5A74                      61 	.ds 1
   5A75                      62 _g_currentwave:
   5A75                      63 	.ds 1
   5A76                      64 _g_aliveenemies:
   5A76                      65 	.ds 1
   5A77                      66 _g_wavecooldown:
   5A77                      67 	.ds 1
   5A78                      68 _g_damagecooldown:
   5A78                      69 	.ds 1
   5A79                      70 _g_shootcooldown:
   5A79                      71 	.ds 1
   5A7A                      72 _g_victory:
   5A7A                      73 	.ds 1
   5A7B                      74 _g_gameover:
   5A7B                      75 	.ds 1
   5A7C                      76 _g_framecounter:
   5A7C                      77 	.ds 2
                             78 ;--------------------------------------------------------
                             79 ; ram data
                             80 ;--------------------------------------------------------
                             81 	.area _INITIALIZED
                             82 ;--------------------------------------------------------
                             83 ; absolute external ram data
                             84 ;--------------------------------------------------------
                             85 	.area _DABS (ABS)
                             86 ;--------------------------------------------------------
                             87 ; global & static initialisations
                             88 ;--------------------------------------------------------
                             89 	.area _HOME
                             90 	.area _GSINIT
                             91 	.area _GSFINAL
                             92 	.area _GSINIT
                             93 ;--------------------------------------------------------
                             94 ; Home
                             95 ;--------------------------------------------------------
                             96 	.area _HOME
                             97 	.area _HOME
                             98 ;--------------------------------------------------------
                             99 ; code
                            100 ;--------------------------------------------------------
                            101 	.area _CODE
                            102 ;src/game.c:32: static u8 rect_overlap(i16 ax, i16 ay, u8 aw, u8 ah, i16 bx, i16 by, u8 bw, u8 bh) {
                            103 ;	---------------------------------
                            104 ; Function rect_overlap
                            105 ; ---------------------------------
   4000                     106 _rect_overlap:
   4000 DD E5         [15]  107 	push	ix
   4002 DD 21 00 00   [14]  108 	ld	ix,#0
   4006 DD 39         [15]  109 	add	ix,sp
                            110 ;src/game.c:33: if (ax + aw <= bx) return 0;
   4008 DD 4E 08      [19]  111 	ld	c, 8 (ix)
   400B 06 00         [ 7]  112 	ld	b, #0x00
   400D DD 6E 04      [19]  113 	ld	l,4 (ix)
   4010 DD 66 05      [19]  114 	ld	h,5 (ix)
   4013 09            [11]  115 	add	hl, bc
   4014 DD 7E 0A      [19]  116 	ld	a, 10 (ix)
   4017 95            [ 4]  117 	sub	a, l
   4018 DD 7E 0B      [19]  118 	ld	a, 11 (ix)
   401B 9C            [ 4]  119 	sbc	a, h
   401C E2 21 40      [10]  120 	jp	PO, 00127$
   401F EE 80         [ 7]  121 	xor	a, #0x80
   4021                     122 00127$:
   4021 FA 28 40      [10]  123 	jp	M, 00102$
   4024 2E 00         [ 7]  124 	ld	l, #0x00
   4026 18 62         [12]  125 	jr	00109$
   4028                     126 00102$:
                            127 ;src/game.c:34: if (bx + bw <= ax) return 0;
   4028 DD 4E 0E      [19]  128 	ld	c, 14 (ix)
   402B 06 00         [ 7]  129 	ld	b, #0x00
   402D DD 6E 0A      [19]  130 	ld	l,10 (ix)
   4030 DD 66 0B      [19]  131 	ld	h,11 (ix)
   4033 09            [11]  132 	add	hl, bc
   4034 DD 7E 04      [19]  133 	ld	a, 4 (ix)
   4037 95            [ 4]  134 	sub	a, l
   4038 DD 7E 05      [19]  135 	ld	a, 5 (ix)
   403B 9C            [ 4]  136 	sbc	a, h
   403C E2 41 40      [10]  137 	jp	PO, 00128$
   403F EE 80         [ 7]  138 	xor	a, #0x80
   4041                     139 00128$:
   4041 FA 48 40      [10]  140 	jp	M, 00104$
   4044 2E 00         [ 7]  141 	ld	l, #0x00
   4046 18 42         [12]  142 	jr	00109$
   4048                     143 00104$:
                            144 ;src/game.c:35: if (ay + ah <= by) return 0;
   4048 DD 4E 09      [19]  145 	ld	c, 9 (ix)
   404B 06 00         [ 7]  146 	ld	b, #0x00
   404D DD 6E 06      [19]  147 	ld	l,6 (ix)
   4050 DD 66 07      [19]  148 	ld	h,7 (ix)
   4053 09            [11]  149 	add	hl, bc
   4054 DD 7E 0C      [19]  150 	ld	a, 12 (ix)
   4057 95            [ 4]  151 	sub	a, l
   4058 DD 7E 0D      [19]  152 	ld	a, 13 (ix)
   405B 9C            [ 4]  153 	sbc	a, h
   405C E2 61 40      [10]  154 	jp	PO, 00129$
   405F EE 80         [ 7]  155 	xor	a, #0x80
   4061                     156 00129$:
   4061 FA 68 40      [10]  157 	jp	M, 00106$
   4064 2E 00         [ 7]  158 	ld	l, #0x00
   4066 18 22         [12]  159 	jr	00109$
   4068                     160 00106$:
                            161 ;src/game.c:36: if (by + bh <= ay) return 0;
   4068 DD 4E 0F      [19]  162 	ld	c, 15 (ix)
   406B 06 00         [ 7]  163 	ld	b, #0x00
   406D DD 6E 0C      [19]  164 	ld	l,12 (ix)
   4070 DD 66 0D      [19]  165 	ld	h,13 (ix)
   4073 09            [11]  166 	add	hl, bc
   4074 DD 7E 06      [19]  167 	ld	a, 6 (ix)
   4077 95            [ 4]  168 	sub	a, l
   4078 DD 7E 07      [19]  169 	ld	a, 7 (ix)
   407B 9C            [ 4]  170 	sbc	a, h
   407C E2 81 40      [10]  171 	jp	PO, 00130$
   407F EE 80         [ 7]  172 	xor	a, #0x80
   4081                     173 00130$:
   4081 FA 88 40      [10]  174 	jp	M, 00108$
   4084 2E 00         [ 7]  175 	ld	l, #0x00
   4086 18 02         [12]  176 	jr	00109$
   4088                     177 00108$:
                            178 ;src/game.c:37: return 1;
   4088 2E 01         [ 7]  179 	ld	l, #0x01
   408A                     180 00109$:
   408A DD E1         [14]  181 	pop	ix
   408C C9            [10]  182 	ret
                            183 ;src/game.c:40: static void spawn_wave(u8 wave) {
                            184 ;	---------------------------------
                            185 ; Function spawn_wave
                            186 ; ---------------------------------
   408D                     187 _spawn_wave:
   408D DD E5         [15]  188 	push	ix
   408F DD 21 00 00   [14]  189 	ld	ix,#0
   4093 DD 39         [15]  190 	add	ix,sp
   4095 F5            [11]  191 	push	af
                            192 ;src/game.c:44: for (i = 0; i < MAX_ENEMIES; ++i) {
   4096 01 FE 59      [10]  193 	ld	bc, #_g_enemies+0
   4099 1E 00         [ 7]  194 	ld	e, #0x00
   409B                     195 00111$:
                            196 ;src/game.c:45: enemyinit(&g_enemies[i]);
   409B D5            [11]  197 	push	de
   409C 16 00         [ 7]  198 	ld	d,#0x00
   409E 6B            [ 4]  199 	ld	l, e
   409F 62            [ 4]  200 	ld	h, d
   40A0 29            [11]  201 	add	hl, hl
   40A1 29            [11]  202 	add	hl, hl
   40A2 29            [11]  203 	add	hl, hl
   40A3 19            [11]  204 	add	hl, de
   40A4 D1            [10]  205 	pop	de
   40A5 09            [11]  206 	add	hl, bc
   40A6 C5            [11]  207 	push	bc
   40A7 D5            [11]  208 	push	de
   40A8 E5            [11]  209 	push	hl
   40A9 CD AF 4F      [17]  210 	call	_enemyinit
   40AC F1            [10]  211 	pop	af
   40AD D1            [10]  212 	pop	de
   40AE C1            [10]  213 	pop	bc
                            214 ;src/game.c:44: for (i = 0; i < MAX_ENEMIES; ++i) {
   40AF 1C            [ 4]  215 	inc	e
   40B0 7B            [ 4]  216 	ld	a, e
   40B1 D6 06         [ 7]  217 	sub	a, #0x06
   40B3 38 E6         [12]  218 	jr	C,00111$
                            219 ;src/game.c:48: if (wave == 0) count = 2;
   40B5 DD 7E 04      [19]  220 	ld	a, 4 (ix)
   40B8 B7            [ 4]  221 	or	a, a
   40B9 20 04         [12]  222 	jr	NZ,00106$
   40BB 16 02         [ 7]  223 	ld	d, #0x02
   40BD 18 0C         [12]  224 	jr	00107$
   40BF                     225 00106$:
                            226 ;src/game.c:49: else if (wave == 1) count = 3;
   40BF DD 7E 04      [19]  227 	ld	a, 4 (ix)
   40C2 3D            [ 4]  228 	dec	a
   40C3 20 04         [12]  229 	jr	NZ,00103$
   40C5 16 03         [ 7]  230 	ld	d, #0x03
   40C7 18 02         [12]  231 	jr	00107$
   40C9                     232 00103$:
                            233 ;src/game.c:50: else count = 4;
   40C9 16 04         [ 7]  234 	ld	d, #0x04
   40CB                     235 00107$:
                            236 ;src/game.c:52: if (count > MAX_ENEMIES) count = MAX_ENEMIES;
   40CB 3E 06         [ 7]  237 	ld	a, #0x06
   40CD 92            [ 4]  238 	sub	a, d
   40CE 30 02         [12]  239 	jr	NC,00127$
   40D0 16 06         [ 7]  240 	ld	d, #0x06
                            241 ;src/game.c:54: for (i = 0; i < count; ++i) {
   40D2                     242 00127$:
   40D2 1E 00         [ 7]  243 	ld	e, #0x00
   40D4                     244 00114$:
   40D4 7B            [ 4]  245 	ld	a, e
   40D5 92            [ 4]  246 	sub	a, d
   40D6 30 42         [12]  247 	jr	NC,00110$
                            248 ;src/game.c:55: enemyspawn(&g_enemies[i], (u8)(48 + (i * 10)), 112, (u8)((i & 1) ? 1 : 0));
   40D8 CB 43         [ 8]  249 	bit	0, e
   40DA 28 06         [12]  250 	jr	Z,00118$
   40DC DD 36 FF 01   [19]  251 	ld	-1 (ix), #0x01
   40E0 18 04         [12]  252 	jr	00119$
   40E2                     253 00118$:
   40E2 DD 36 FF 00   [19]  254 	ld	-1 (ix), #0x00
   40E6                     255 00119$:
   40E6 D5            [11]  256 	push	de
   40E7 7B            [ 4]  257 	ld	a, e
   40E8 87            [ 4]  258 	add	a, a
   40E9 87            [ 4]  259 	add	a, a
   40EA 83            [ 4]  260 	add	a, e
   40EB 87            [ 4]  261 	add	a, a
   40EC D1            [10]  262 	pop	de
   40ED C6 30         [ 7]  263 	add	a, #0x30
   40EF DD 77 FE      [19]  264 	ld	-2 (ix), a
   40F2 D5            [11]  265 	push	de
   40F3 16 00         [ 7]  266 	ld	d,#0x00
   40F5 6B            [ 4]  267 	ld	l, e
   40F6 62            [ 4]  268 	ld	h, d
   40F7 29            [11]  269 	add	hl, hl
   40F8 29            [11]  270 	add	hl, hl
   40F9 29            [11]  271 	add	hl, hl
   40FA 19            [11]  272 	add	hl, de
   40FB D1            [10]  273 	pop	de
   40FC 09            [11]  274 	add	hl, bc
   40FD E5            [11]  275 	push	hl
   40FE FD E1         [14]  276 	pop	iy
   4100 C5            [11]  277 	push	bc
   4101 D5            [11]  278 	push	de
   4102 DD 56 FF      [19]  279 	ld	d, -1 (ix)
   4105 1E 70         [ 7]  280 	ld	e,#0x70
   4107 D5            [11]  281 	push	de
   4108 DD 7E FE      [19]  282 	ld	a, -2 (ix)
   410B F5            [11]  283 	push	af
   410C 33            [ 6]  284 	inc	sp
   410D FD E5         [15]  285 	push	iy
   410F CD EE 4F      [17]  286 	call	_enemyspawn
   4112 F1            [10]  287 	pop	af
   4113 F1            [10]  288 	pop	af
   4114 33            [ 6]  289 	inc	sp
   4115 D1            [10]  290 	pop	de
   4116 C1            [10]  291 	pop	bc
                            292 ;src/game.c:54: for (i = 0; i < count; ++i) {
   4117 1C            [ 4]  293 	inc	e
   4118 18 BA         [12]  294 	jr	00114$
   411A                     295 00110$:
                            296 ;src/game.c:58: g_aliveenemies = count;
   411A 21 76 5A      [10]  297 	ld	hl,#_g_aliveenemies + 0
   411D 72            [ 7]  298 	ld	(hl), d
   411E DD F9         [10]  299 	ld	sp, ix
   4120 DD E1         [14]  300 	pop	ix
   4122 C9            [10]  301 	ret
                            302 ;src/game.c:61: static void try_fire_projectile(void) {
                            303 ;	---------------------------------
                            304 ; Function try_fire_projectile
                            305 ; ---------------------------------
   4123                     306 _try_fire_projectile:
   4123 DD E5         [15]  307 	push	ix
   4125 DD 21 00 00   [14]  308 	ld	ix,#0
   4129 DD 39         [15]  309 	add	ix,sp
   412B 21 FA FF      [10]  310 	ld	hl, #-6
   412E 39            [11]  311 	add	hl, sp
   412F F9            [ 6]  312 	ld	sp, hl
                            313 ;src/game.c:65: if (!input_is_shoot_just_pressed()) return;
   4130 CD 0C 4B      [17]  314 	call	_input_is_shoot_just_pressed
   4133 DD 75 FF      [19]  315 	ld	-1 (ix), l
   4136 7D            [ 4]  316 	ld	a, l
   4137 B7            [ 4]  317 	or	a, a
   4138 CA C6 41      [10]  318 	jp	Z,00110$
                            319 ;src/game.c:66: if (g_shootcooldown) return;
   413B 3A 79 5A      [13]  320 	ld	a,(#_g_shootcooldown + 0)
   413E B7            [ 4]  321 	or	a, a
   413F C2 C6 41      [10]  322 	jp	NZ,00110$
                            323 ;src/game.c:68: dir = g_player.facing_left ? -3 : 3;
   4142 3A FC 59      [13]  324 	ld	a, (#_g_player + 7)
   4145 B7            [ 4]  325 	or	a, a
   4146 28 04         [12]  326 	jr	Z,00112$
   4148 0E FD         [ 7]  327 	ld	c, #0xfd
   414A 18 02         [12]  328 	jr	00113$
   414C                     329 00112$:
   414C 0E 03         [ 7]  330 	ld	c, #0x03
   414E                     331 00113$:
   414E DD 71 FA      [19]  332 	ld	-6 (ix), c
                            333 ;src/game.c:70: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4151 DD 36 FB 00   [19]  334 	ld	-5 (ix), #0x00
   4155                     335 00108$:
                            336 ;src/game.c:71: if (!g_projectiles[i].active) {
   4155 DD 4E FB      [19]  337 	ld	c,-5 (ix)
   4158 06 00         [ 7]  338 	ld	b,#0x00
   415A 69            [ 4]  339 	ld	l, c
   415B 60            [ 4]  340 	ld	h, b
   415C 29            [11]  341 	add	hl, hl
   415D 29            [11]  342 	add	hl, hl
   415E 09            [11]  343 	add	hl, bc
   415F 29            [11]  344 	add	hl, hl
   4160 01 34 5A      [10]  345 	ld	bc,#_g_projectiles
   4163 09            [11]  346 	add	hl,bc
   4164 DD 75 FD      [19]  347 	ld	-3 (ix), l
   4167 DD 74 FE      [19]  348 	ld	-2 (ix), h
   416A 11 06 00      [10]  349 	ld	de, #0x0006
   416D 19            [11]  350 	add	hl, de
   416E 7E            [ 7]  351 	ld	a, (hl)
   416F B7            [ 4]  352 	or	a, a
   4170 20 4A         [12]  353 	jr	NZ,00109$
                            354 ;src/game.c:72: projectilefire(&g_projectiles[i], (u8)(g_player.x + 2), (u8)(g_player.y + 6), dir, g_weapon);
   4172 3A F6 59      [13]  355 	ld	a,(#_g_player + 1)
   4175 DD 77 FF      [19]  356 	ld	-1 (ix), a
   4178 C6 06         [ 7]  357 	add	a, #0x06
   417A DD 77 FF      [19]  358 	ld	-1 (ix), a
   417D 3A F5 59      [13]  359 	ld	a,(#_g_player + 0)
   4180 DD 77 FC      [19]  360 	ld	-4 (ix), a
   4183 DD 34 FC      [23]  361 	inc	-4 (ix)
   4186 DD 34 FC      [23]  362 	inc	-4 (ix)
   4189 3A 74 5A      [13]  363 	ld	a, (_g_weapon)
   418C F5            [11]  364 	push	af
   418D 33            [ 6]  365 	inc	sp
   418E DD 66 FA      [19]  366 	ld	h, -6 (ix)
   4191 DD 6E FF      [19]  367 	ld	l, -1 (ix)
   4194 E5            [11]  368 	push	hl
   4195 DD 7E FC      [19]  369 	ld	a, -4 (ix)
   4198 F5            [11]  370 	push	af
   4199 33            [ 6]  371 	inc	sp
   419A DD 6E FD      [19]  372 	ld	l,-3 (ix)
   419D DD 66 FE      [19]  373 	ld	h,-2 (ix)
   41A0 E5            [11]  374 	push	hl
   41A1 CD 1E 56      [17]  375 	call	_projectilefire
   41A4 21 06 00      [10]  376 	ld	hl, #6
   41A7 39            [11]  377 	add	hl, sp
   41A8 F9            [ 6]  378 	ld	sp, hl
                            379 ;src/game.c:73: g_weapon ^= 1;
   41A9 FD 21 74 5A   [14]  380 	ld	iy, #_g_weapon
   41AD FD 7E 00      [19]  381 	ld	a, 0 (iy)
   41B0 EE 01         [ 7]  382 	xor	a, #0x01
   41B2 FD 77 00      [19]  383 	ld	0 (iy), a
                            384 ;src/game.c:74: g_shootcooldown = 10;
   41B5 21 79 5A      [10]  385 	ld	hl,#_g_shootcooldown + 0
   41B8 36 0A         [10]  386 	ld	(hl), #0x0a
                            387 ;src/game.c:75: break;
   41BA 18 0A         [12]  388 	jr	00110$
   41BC                     389 00109$:
                            390 ;src/game.c:70: for (i = 0; i < MAX_PROJECTILES; ++i) {
   41BC DD 34 FB      [23]  391 	inc	-5 (ix)
   41BF DD 7E FB      [19]  392 	ld	a, -5 (ix)
   41C2 D6 06         [ 7]  393 	sub	a, #0x06
   41C4 38 8F         [12]  394 	jr	C,00108$
   41C6                     395 00110$:
   41C6 DD F9         [10]  396 	ld	sp, ix
   41C8 DD E1         [14]  397 	pop	ix
   41CA C9            [10]  398 	ret
                            399 ;src/game.c:80: void game_init(void) {
                            400 ;	---------------------------------
                            401 ; Function game_init
                            402 ; ---------------------------------
   41CB                     403 _game_init::
                            404 ;src/game.c:83: cpct_disableFirmware();
   41CB CD 0C 59      [17]  405 	call	_cpct_disableFirmware
                            406 ;src/game.c:84: cpct_setVideoMode(1);
   41CE 2E 01         [ 7]  407 	ld	l, #0x01
   41D0 CD F0 58      [17]  408 	call	_cpct_setVideoMode
                            409 ;src/game.c:85: cpct_clearScreen(0x00);
   41D3 21 00 40      [10]  410 	ld	hl, #0x4000
   41D6 E5            [11]  411 	push	hl
   41D7 AF            [ 4]  412 	xor	a, a
   41D8 F5            [11]  413 	push	af
   41D9 33            [ 6]  414 	inc	sp
   41DA 26 C0         [ 7]  415 	ld	h, #0xc0
   41DC E5            [11]  416 	push	hl
   41DD CD FE 58      [17]  417 	call	_cpct_memset
                            418 ;src/game.c:86: tilemap_init();
   41E0 CD 1E 4B      [17]  419 	call	_tilemap_init
                            420 ;src/game.c:87: collision_init();
   41E3 CD A2 46      [17]  421 	call	_collision_init
                            422 ;src/game.c:88: playerinit(&g_player);
   41E6 21 F5 59      [10]  423 	ld	hl, #_g_player
   41E9 E5            [11]  424 	push	hl
   41EA CD DF 51      [17]  425 	call	_playerinit
   41ED F1            [10]  426 	pop	af
                            427 ;src/game.c:89: hudinit();
   41EE CD 83 49      [17]  428 	call	_hudinit
                            429 ;src/game.c:91: for (i = 0; i < MAX_PROJECTILES; ++i) {
   41F1 0E 00         [ 7]  430 	ld	c, #0x00
   41F3                     431 00102$:
                            432 ;src/game.c:92: projectileinit(&g_projectiles[i]);
   41F3 06 00         [ 7]  433 	ld	b,#0x00
   41F5 69            [ 4]  434 	ld	l, c
   41F6 60            [ 4]  435 	ld	h, b
   41F7 29            [11]  436 	add	hl, hl
   41F8 29            [11]  437 	add	hl, hl
   41F9 09            [11]  438 	add	hl, bc
   41FA 29            [11]  439 	add	hl, hl
   41FB 11 34 5A      [10]  440 	ld	de, #_g_projectiles
   41FE 19            [11]  441 	add	hl, de
   41FF C5            [11]  442 	push	bc
   4200 E5            [11]  443 	push	hl
   4201 CD D9 55      [17]  444 	call	_projectileinit
   4204 F1            [10]  445 	pop	af
   4205 C1            [10]  446 	pop	bc
                            447 ;src/game.c:91: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4206 0C            [ 4]  448 	inc	c
   4207 79            [ 4]  449 	ld	a, c
   4208 D6 06         [ 7]  450 	sub	a, #0x06
   420A 38 E7         [12]  451 	jr	C,00102$
                            452 ;src/game.c:95: g_lives = 3;
   420C 21 70 5A      [10]  453 	ld	hl,#_g_lives + 0
   420F 36 03         [10]  454 	ld	(hl), #0x03
                            455 ;src/game.c:96: g_score = 0;
   4211 21 00 00      [10]  456 	ld	hl, #0x0000
   4214 22 71 5A      [16]  457 	ld	(_g_score), hl
                            458 ;src/game.c:97: g_timeleft = 99;
   4217 FD 21 73 5A   [14]  459 	ld	iy, #_g_timeleft
   421B FD 36 00 63   [19]  460 	ld	0 (iy), #0x63
                            461 ;src/game.c:98: g_weapon = 0;
   421F FD 21 74 5A   [14]  462 	ld	iy, #_g_weapon
   4223 FD 36 00 00   [19]  463 	ld	0 (iy), #0x00
                            464 ;src/game.c:99: g_currentwave = 0;
   4227 FD 21 75 5A   [14]  465 	ld	iy, #_g_currentwave
   422B FD 36 00 00   [19]  466 	ld	0 (iy), #0x00
                            467 ;src/game.c:100: g_wavecooldown = 1;
   422F FD 21 77 5A   [14]  468 	ld	iy, #_g_wavecooldown
   4233 FD 36 00 01   [19]  469 	ld	0 (iy), #0x01
                            470 ;src/game.c:101: g_damagecooldown = 0;
   4237 FD 21 78 5A   [14]  471 	ld	iy, #_g_damagecooldown
   423B FD 36 00 00   [19]  472 	ld	0 (iy), #0x00
                            473 ;src/game.c:102: g_shootcooldown = 0;
   423F FD 21 79 5A   [14]  474 	ld	iy, #_g_shootcooldown
   4243 FD 36 00 00   [19]  475 	ld	0 (iy), #0x00
                            476 ;src/game.c:103: g_victory = 0;
   4247 FD 21 7A 5A   [14]  477 	ld	iy, #_g_victory
   424B FD 36 00 00   [19]  478 	ld	0 (iy), #0x00
                            479 ;src/game.c:104: g_gameover = 0;
   424F FD 21 7B 5A   [14]  480 	ld	iy, #_g_gameover
   4253 FD 36 00 00   [19]  481 	ld	0 (iy), #0x00
                            482 ;src/game.c:105: g_framecounter = 0;
   4257 2E 00         [ 7]  483 	ld	l, #0x00
   4259 22 7C 5A      [16]  484 	ld	(_g_framecounter), hl
   425C C9            [10]  485 	ret
                            486 ;src/game.c:108: void game_update(void) {
                            487 ;	---------------------------------
                            488 ; Function game_update
                            489 ; ---------------------------------
   425D                     490 _game_update::
   425D DD E5         [15]  491 	push	ix
   425F DD 21 00 00   [14]  492 	ld	ix,#0
   4263 DD 39         [15]  493 	add	ix,sp
   4265 21 F0 FF      [10]  494 	ld	hl, #-16
   4268 39            [11]  495 	add	hl, sp
   4269 F9            [ 6]  496 	ld	sp, hl
                            497 ;src/game.c:112: input_update();
   426A CD 96 4A      [17]  498 	call	_input_update
                            499 ;src/game.c:114: if (g_gameover || g_victory) {
   426D 3A 7B 5A      [13]  500 	ld	a,(#_g_gameover + 0)
   4270 B7            [ 4]  501 	or	a, a
   4271 C2 FD 45      [10]  502 	jp	NZ,00165$
   4274 3A 7A 5A      [13]  503 	ld	a,(#_g_victory + 0)
   4277 B7            [ 4]  504 	or	a, a
                            505 ;src/game.c:115: return;
   4278 C2 FD 45      [10]  506 	jp	NZ,00165$
                            507 ;src/game.c:118: playerupdate(&g_player);
   427B 21 F5 59      [10]  508 	ld	hl, #_g_player
   427E E5            [11]  509 	push	hl
   427F CD 26 52      [17]  510 	call	_playerupdate
   4282 F1            [10]  511 	pop	af
                            512 ;src/game.c:119: try_fire_projectile();
   4283 CD 23 41      [17]  513 	call	_try_fire_projectile
                            514 ;src/game.c:121: if (g_shootcooldown) g_shootcooldown--;
   4286 FD 21 79 5A   [14]  515 	ld	iy, #_g_shootcooldown
   428A FD 7E 00      [19]  516 	ld	a, 0 (iy)
   428D B7            [ 4]  517 	or	a, a
   428E 28 03         [12]  518 	jr	Z,00105$
   4290 FD 35 00      [23]  519 	dec	0 (iy)
   4293                     520 00105$:
                            521 ;src/game.c:122: if (g_damagecooldown) g_damagecooldown--;
   4293 FD 21 78 5A   [14]  522 	ld	iy, #_g_damagecooldown
   4297 FD 7E 00      [19]  523 	ld	a, 0 (iy)
   429A B7            [ 4]  524 	or	a, a
   429B 28 03         [12]  525 	jr	Z,00170$
   429D FD 35 00      [23]  526 	dec	0 (iy)
                            527 ;src/game.c:124: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42A0                     528 00170$:
   42A0 0E 00         [ 7]  529 	ld	c, #0x00
   42A2                     530 00158$:
                            531 ;src/game.c:125: projectileupdate(&g_projectiles[i]);
   42A2 06 00         [ 7]  532 	ld	b,#0x00
   42A4 69            [ 4]  533 	ld	l, c
   42A5 60            [ 4]  534 	ld	h, b
   42A6 29            [11]  535 	add	hl, hl
   42A7 29            [11]  536 	add	hl, hl
   42A8 09            [11]  537 	add	hl, bc
   42A9 29            [11]  538 	add	hl, hl
   42AA 11 34 5A      [10]  539 	ld	de, #_g_projectiles
   42AD 19            [11]  540 	add	hl, de
   42AE C5            [11]  541 	push	bc
   42AF E5            [11]  542 	push	hl
   42B0 CD A2 56      [17]  543 	call	_projectileupdate
   42B3 F1            [10]  544 	pop	af
   42B4 C1            [10]  545 	pop	bc
                            546 ;src/game.c:124: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42B5 0C            [ 4]  547 	inc	c
   42B6 79            [ 4]  548 	ld	a, c
   42B7 D6 06         [ 7]  549 	sub	a, #0x06
   42B9 38 E7         [12]  550 	jr	C,00158$
                            551 ;src/game.c:128: for (i = 0; i < MAX_ENEMIES; ++i) {
   42BB 0E 00         [ 7]  552 	ld	c, #0x00
   42BD                     553 00160$:
                            554 ;src/game.c:129: enemyupdate(&g_enemies[i]);
   42BD 06 00         [ 7]  555 	ld	b,#0x00
   42BF 69            [ 4]  556 	ld	l, c
   42C0 60            [ 4]  557 	ld	h, b
   42C1 29            [11]  558 	add	hl, hl
   42C2 29            [11]  559 	add	hl, hl
   42C3 29            [11]  560 	add	hl, hl
   42C4 09            [11]  561 	add	hl, bc
   42C5 11 FE 59      [10]  562 	ld	de, #_g_enemies
   42C8 19            [11]  563 	add	hl, de
   42C9 C5            [11]  564 	push	bc
   42CA E5            [11]  565 	push	hl
   42CB CD 30 50      [17]  566 	call	_enemyupdate
   42CE F1            [10]  567 	pop	af
   42CF C1            [10]  568 	pop	bc
                            569 ;src/game.c:128: for (i = 0; i < MAX_ENEMIES; ++i) {
   42D0 0C            [ 4]  570 	inc	c
   42D1 79            [ 4]  571 	ld	a, c
   42D2 D6 06         [ 7]  572 	sub	a, #0x06
   42D4 38 E7         [12]  573 	jr	C,00160$
                            574 ;src/game.c:132: for (i = 0; i < MAX_PROJECTILES; ++i) {
   42D6 DD 36 F1 00   [19]  575 	ld	-15 (ix), #0x00
   42DA                     576 00163$:
                            577 ;src/game.c:133: if (!g_projectiles[i].active) continue;
   42DA DD 4E F1      [19]  578 	ld	c,-15 (ix)
   42DD 06 00         [ 7]  579 	ld	b,#0x00
   42DF 69            [ 4]  580 	ld	l, c
   42E0 60            [ 4]  581 	ld	h, b
   42E1 29            [11]  582 	add	hl, hl
   42E2 29            [11]  583 	add	hl, hl
   42E3 09            [11]  584 	add	hl, bc
   42E4 29            [11]  585 	add	hl, hl
   42E5 4D            [ 4]  586 	ld	c, l
   42E6 44            [ 4]  587 	ld	b, h
   42E7 21 34 5A      [10]  588 	ld	hl, #_g_projectiles
   42EA 09            [11]  589 	add	hl,bc
   42EB DD 75 FE      [19]  590 	ld	-2 (ix), l
   42EE DD 74 FF      [19]  591 	ld	-1 (ix), h
   42F1 DD 7E FE      [19]  592 	ld	a, -2 (ix)
   42F4 C6 06         [ 7]  593 	add	a, #0x06
   42F6 DD 77 FC      [19]  594 	ld	-4 (ix), a
   42F9 DD 7E FF      [19]  595 	ld	a, -1 (ix)
   42FC CE 00         [ 7]  596 	adc	a, #0x00
   42FE DD 77 FD      [19]  597 	ld	-3 (ix), a
   4301 DD 6E FC      [19]  598 	ld	l,-4 (ix)
   4304 DD 66 FD      [19]  599 	ld	h,-3 (ix)
   4307 7E            [ 7]  600 	ld	a, (hl)
   4308 B7            [ 4]  601 	or	a, a
   4309 CA 35 44      [10]  602 	jp	Z, 00122$
                            603 ;src/game.c:134: for (j = 0; j < MAX_ENEMIES; ++j) {
   430C DD 36 F0 00   [19]  604 	ld	-16 (ix), #0x00
   4310                     605 00162$:
                            606 ;src/game.c:135: if (!g_enemies[j].active) continue;
   4310 DD 4E F0      [19]  607 	ld	c,-16 (ix)
   4313 06 00         [ 7]  608 	ld	b,#0x00
   4315 69            [ 4]  609 	ld	l, c
   4316 60            [ 4]  610 	ld	h, b
   4317 29            [11]  611 	add	hl, hl
   4318 29            [11]  612 	add	hl, hl
   4319 29            [11]  613 	add	hl, hl
   431A 09            [11]  614 	add	hl, bc
   431B 4D            [ 4]  615 	ld	c, l
   431C 44            [ 4]  616 	ld	b, h
   431D 21 FE 59      [10]  617 	ld	hl, #_g_enemies
   4320 09            [11]  618 	add	hl,bc
   4321 DD 75 FA      [19]  619 	ld	-6 (ix), l
   4324 DD 74 FB      [19]  620 	ld	-5 (ix), h
   4327 11 06 00      [10]  621 	ld	de, #0x0006
   432A 19            [11]  622 	add	hl, de
   432B 7E            [ 7]  623 	ld	a, (hl)
   432C B7            [ 4]  624 	or	a, a
   432D CA 2A 44      [10]  625 	jp	Z, 00120$
                            626 ;src/game.c:137: (i16)g_enemies[j].x, (i16)g_enemies[j].y, g_enemies[j].w, g_enemies[j].h)) continue;
   4330 DD 6E FA      [19]  627 	ld	l,-6 (ix)
   4333 DD 66 FB      [19]  628 	ld	h,-5 (ix)
   4336 11 05 00      [10]  629 	ld	de, #0x0005
   4339 19            [11]  630 	add	hl, de
   433A 7E            [ 7]  631 	ld	a, (hl)
   433B DD 77 F9      [19]  632 	ld	-7 (ix), a
   433E DD 6E FA      [19]  633 	ld	l,-6 (ix)
   4341 DD 66 FB      [19]  634 	ld	h,-5 (ix)
   4344 11 04 00      [10]  635 	ld	de, #0x0004
   4347 19            [11]  636 	add	hl, de
   4348 7E            [ 7]  637 	ld	a, (hl)
   4349 DD 77 F8      [19]  638 	ld	-8 (ix), a
   434C DD 6E FA      [19]  639 	ld	l,-6 (ix)
   434F DD 66 FB      [19]  640 	ld	h,-5 (ix)
   4352 23            [ 6]  641 	inc	hl
   4353 4E            [ 7]  642 	ld	c, (hl)
   4354 DD 71 F6      [19]  643 	ld	-10 (ix), c
   4357 DD 36 F7 00   [19]  644 	ld	-9 (ix), #0x00
   435B DD 6E FA      [19]  645 	ld	l,-6 (ix)
   435E DD 66 FB      [19]  646 	ld	h,-5 (ix)
   4361 5E            [ 7]  647 	ld	e, (hl)
   4362 16 00         [ 7]  648 	ld	d, #0x00
                            649 ;src/game.c:136: if (!rect_overlap((i16)g_projectiles[i].x, (i16)g_projectiles[i].y, g_projectiles[i].w, g_projectiles[i].h,
   4364 DD 6E FE      [19]  650 	ld	l,-2 (ix)
   4367 DD 66 FF      [19]  651 	ld	h,-1 (ix)
   436A 01 05 00      [10]  652 	ld	bc, #0x0005
   436D 09            [11]  653 	add	hl, bc
   436E 46            [ 7]  654 	ld	b, (hl)
   436F DD 6E FE      [19]  655 	ld	l,-2 (ix)
   4372 DD 66 FF      [19]  656 	ld	h,-1 (ix)
   4375 23            [ 6]  657 	inc	hl
   4376 23            [ 6]  658 	inc	hl
   4377 23            [ 6]  659 	inc	hl
   4378 23            [ 6]  660 	inc	hl
   4379 4E            [ 7]  661 	ld	c, (hl)
   437A DD 6E FE      [19]  662 	ld	l,-2 (ix)
   437D DD 66 FF      [19]  663 	ld	h,-1 (ix)
   4380 23            [ 6]  664 	inc	hl
   4381 6E            [ 7]  665 	ld	l, (hl)
   4382 DD 75 F4      [19]  666 	ld	-12 (ix), l
   4385 DD 36 F5 00   [19]  667 	ld	-11 (ix), #0x00
   4389 DD 6E FE      [19]  668 	ld	l,-2 (ix)
   438C DD 66 FF      [19]  669 	ld	h,-1 (ix)
   438F 6E            [ 7]  670 	ld	l, (hl)
   4390 DD 75 F2      [19]  671 	ld	-14 (ix), l
   4393 DD 36 F3 00   [19]  672 	ld	-13 (ix), #0x00
   4397 DD 66 F9      [19]  673 	ld	h, -7 (ix)
   439A DD 6E F8      [19]  674 	ld	l, -8 (ix)
   439D E5            [11]  675 	push	hl
   439E DD 6E F6      [19]  676 	ld	l,-10 (ix)
   43A1 DD 66 F7      [19]  677 	ld	h,-9 (ix)
   43A4 E5            [11]  678 	push	hl
   43A5 D5            [11]  679 	push	de
   43A6 C5            [11]  680 	push	bc
   43A7 DD 6E F4      [19]  681 	ld	l,-12 (ix)
   43AA DD 66 F5      [19]  682 	ld	h,-11 (ix)
   43AD E5            [11]  683 	push	hl
   43AE DD 6E F2      [19]  684 	ld	l,-14 (ix)
   43B1 DD 66 F3      [19]  685 	ld	h,-13 (ix)
   43B4 E5            [11]  686 	push	hl
   43B5 CD 00 40      [17]  687 	call	_rect_overlap
   43B8 FD 21 0C 00   [14]  688 	ld	iy, #12
   43BC FD 39         [15]  689 	add	iy, sp
   43BE FD F9         [10]  690 	ld	sp, iy
   43C0 7D            [ 4]  691 	ld	a, l
   43C1 B7            [ 4]  692 	or	a, a
   43C2 28 66         [12]  693 	jr	Z,00120$
                            694 ;src/game.c:138: if (enemydamage(&g_enemies[j], g_projectiles[i].damage)) {
   43C4 DD 6E FE      [19]  695 	ld	l,-2 (ix)
   43C7 DD 66 FF      [19]  696 	ld	h,-1 (ix)
   43CA 11 07 00      [10]  697 	ld	de, #0x0007
   43CD 19            [11]  698 	add	hl, de
   43CE 56            [ 7]  699 	ld	d, (hl)
   43CF DD 4E FA      [19]  700 	ld	c,-6 (ix)
   43D2 DD 46 FB      [19]  701 	ld	b,-5 (ix)
   43D5 D5            [11]  702 	push	de
   43D6 33            [ 6]  703 	inc	sp
   43D7 C5            [11]  704 	push	bc
   43D8 CD 9F 51      [17]  705 	call	_enemydamage
   43DB F1            [10]  706 	pop	af
   43DC 33            [ 6]  707 	inc	sp
   43DD DD 75 F2      [19]  708 	ld	-14 (ix), l
   43E0 7D            [ 4]  709 	ld	a, l
   43E1 B7            [ 4]  710 	or	a, a
   43E2 28 3C         [12]  711 	jr	Z,00119$
                            712 ;src/game.c:139: g_score = (u16)(g_score + g_enemies[j].reward);
   43E4 DD 7E FA      [19]  713 	ld	a, -6 (ix)
   43E7 DD 77 F2      [19]  714 	ld	-14 (ix), a
   43EA DD 7E FB      [19]  715 	ld	a, -5 (ix)
   43ED DD 77 F3      [19]  716 	ld	-13 (ix), a
   43F0 DD 6E F2      [19]  717 	ld	l,-14 (ix)
   43F3 DD 66 F3      [19]  718 	ld	h,-13 (ix)
   43F6 11 08 00      [10]  719 	ld	de, #0x0008
   43F9 19            [11]  720 	add	hl, de
   43FA 7E            [ 7]  721 	ld	a, (hl)
   43FB DD 77 F2      [19]  722 	ld	-14 (ix), a
   43FE DD 77 F2      [19]  723 	ld	-14 (ix), a
   4401 DD 36 F3 00   [19]  724 	ld	-13 (ix), #0x00
   4405 21 71 5A      [10]  725 	ld	hl, #_g_score
   4408 7E            [ 7]  726 	ld	a, (hl)
   4409 DD 86 F2      [19]  727 	add	a, -14 (ix)
   440C 77            [ 7]  728 	ld	(hl), a
   440D 23            [ 6]  729 	inc	hl
   440E 7E            [ 7]  730 	ld	a, (hl)
   440F DD 8E F3      [19]  731 	adc	a, -13 (ix)
   4412 77            [ 7]  732 	ld	(hl), a
                            733 ;src/game.c:140: if (g_aliveenemies) g_aliveenemies--;
   4413 FD 21 76 5A   [14]  734 	ld	iy, #_g_aliveenemies
   4417 FD 7E 00      [19]  735 	ld	a, 0 (iy)
   441A B7            [ 4]  736 	or	a, a
   441B 28 03         [12]  737 	jr	Z,00119$
   441D FD 35 00      [23]  738 	dec	0 (iy)
   4420                     739 00119$:
                            740 ;src/game.c:142: g_projectiles[i].active = 0;
   4420 DD 6E FC      [19]  741 	ld	l,-4 (ix)
   4423 DD 66 FD      [19]  742 	ld	h,-3 (ix)
   4426 36 00         [10]  743 	ld	(hl), #0x00
                            744 ;src/game.c:143: break;
   4428 18 0B         [12]  745 	jr	00122$
   442A                     746 00120$:
                            747 ;src/game.c:134: for (j = 0; j < MAX_ENEMIES; ++j) {
   442A DD 34 F0      [23]  748 	inc	-16 (ix)
   442D DD 7E F0      [19]  749 	ld	a, -16 (ix)
   4430 D6 06         [ 7]  750 	sub	a, #0x06
   4432 DA 10 43      [10]  751 	jp	C, 00162$
   4435                     752 00122$:
                            753 ;src/game.c:132: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4435 DD 34 F1      [23]  754 	inc	-15 (ix)
   4438 DD 7E F1      [19]  755 	ld	a, -15 (ix)
   443B D6 06         [ 7]  756 	sub	a, #0x06
   443D DA DA 42      [10]  757 	jp	C, 00163$
                            758 ;src/game.c:147: if (!g_damagecooldown) {
   4440 3A 78 5A      [13]  759 	ld	a,(#_g_damagecooldown + 0)
   4443 B7            [ 4]  760 	or	a, a
   4444 C2 59 45      [10]  761 	jp	NZ, 00138$
                            762 ;src/game.c:148: for (i = 0; i < MAX_ENEMIES; ++i) {
   4447 11 F9 59      [10]  763 	ld	de, #_g_player + 4
   444A DD 36 F1 00   [19]  764 	ld	-15 (ix), #0x00
   444E                     765 00164$:
                            766 ;src/game.c:149: if (!g_enemies[i].active) continue;
   444E DD 4E F1      [19]  767 	ld	c,-15 (ix)
   4451 06 00         [ 7]  768 	ld	b,#0x00
   4453 69            [ 4]  769 	ld	l, c
   4454 60            [ 4]  770 	ld	h, b
   4455 29            [11]  771 	add	hl, hl
   4456 29            [11]  772 	add	hl, hl
   4457 29            [11]  773 	add	hl, hl
   4458 09            [11]  774 	add	hl, bc
   4459 01 FE 59      [10]  775 	ld	bc,#_g_enemies
   445C 09            [11]  776 	add	hl,bc
   445D DD 75 F2      [19]  777 	ld	-14 (ix), l
   4460 DD 74 F3      [19]  778 	ld	-13 (ix), h
   4463 C1            [10]  779 	pop	bc
   4464 E1            [10]  780 	pop	hl
   4465 E5            [11]  781 	push	hl
   4466 C5            [11]  782 	push	bc
   4467 01 06 00      [10]  783 	ld	bc, #0x0006
   446A 09            [11]  784 	add	hl, bc
   446B 7E            [ 7]  785 	ld	a, (hl)
   446C B7            [ 4]  786 	or	a, a
   446D CA 0E 45      [10]  787 	jp	Z, 00130$
                            788 ;src/game.c:151: (i16)g_enemies[i].x, (i16)g_enemies[i].y, g_enemies[i].w, g_enemies[i].h)) {
   4470 C1            [10]  789 	pop	bc
   4471 E1            [10]  790 	pop	hl
   4472 E5            [11]  791 	push	hl
   4473 C5            [11]  792 	push	bc
   4474 01 05 00      [10]  793 	ld	bc, #0x0005
   4477 09            [11]  794 	add	hl, bc
   4478 7E            [ 7]  795 	ld	a, (hl)
   4479 DD 77 F4      [19]  796 	ld	-12 (ix), a
   447C C1            [10]  797 	pop	bc
   447D E1            [10]  798 	pop	hl
   447E E5            [11]  799 	push	hl
   447F C5            [11]  800 	push	bc
   4480 01 04 00      [10]  801 	ld	bc, #0x0004
   4483 09            [11]  802 	add	hl, bc
   4484 4E            [ 7]  803 	ld	c, (hl)
   4485 DD 6E F2      [19]  804 	ld	l,-14 (ix)
   4488 DD 66 F3      [19]  805 	ld	h,-13 (ix)
   448B 23            [ 6]  806 	inc	hl
   448C 46            [ 7]  807 	ld	b, (hl)
   448D DD 70 F6      [19]  808 	ld	-10 (ix), b
   4490 DD 36 F7 00   [19]  809 	ld	-9 (ix), #0x00
   4494 DD 6E F2      [19]  810 	ld	l,-14 (ix)
   4497 DD 66 F3      [19]  811 	ld	h,-13 (ix)
   449A 46            [ 7]  812 	ld	b, (hl)
   449B DD 70 F2      [19]  813 	ld	-14 (ix), b
   449E DD 36 F3 00   [19]  814 	ld	-13 (ix), #0x00
                            815 ;src/game.c:150: if (rect_overlap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h,
   44A2 21 FA 59      [10]  816 	ld	hl, #(_g_player + 0x0005) + 0
   44A5 46            [ 7]  817 	ld	b, (hl)
   44A6 1A            [ 7]  818 	ld	a, (de)
   44A7 DD 77 F8      [19]  819 	ld	-8 (ix), a
   44AA 3A F6 59      [13]  820 	ld	a, (#(_g_player + 0x0001) + 0)
   44AD DD 77 FA      [19]  821 	ld	-6 (ix), a
   44B0 DD 36 FB 00   [19]  822 	ld	-5 (ix), #0x00
   44B4 3A F5 59      [13]  823 	ld	a, (#_g_player + 0)
   44B7 DD 77 FC      [19]  824 	ld	-4 (ix), a
   44BA DD 36 FD 00   [19]  825 	ld	-3 (ix), #0x00
   44BE D5            [11]  826 	push	de
   44BF DD 7E F4      [19]  827 	ld	a, -12 (ix)
   44C2 F5            [11]  828 	push	af
   44C3 33            [ 6]  829 	inc	sp
   44C4 79            [ 4]  830 	ld	a, c
   44C5 F5            [11]  831 	push	af
   44C6 33            [ 6]  832 	inc	sp
   44C7 DD 6E F6      [19]  833 	ld	l,-10 (ix)
   44CA DD 66 F7      [19]  834 	ld	h,-9 (ix)
   44CD E5            [11]  835 	push	hl
   44CE DD 6E F2      [19]  836 	ld	l,-14 (ix)
   44D1 DD 66 F3      [19]  837 	ld	h,-13 (ix)
   44D4 E5            [11]  838 	push	hl
   44D5 C5            [11]  839 	push	bc
   44D6 33            [ 6]  840 	inc	sp
   44D7 DD 7E F8      [19]  841 	ld	a, -8 (ix)
   44DA F5            [11]  842 	push	af
   44DB 33            [ 6]  843 	inc	sp
   44DC DD 6E FA      [19]  844 	ld	l,-6 (ix)
   44DF DD 66 FB      [19]  845 	ld	h,-5 (ix)
   44E2 E5            [11]  846 	push	hl
   44E3 DD 6E FC      [19]  847 	ld	l,-4 (ix)
   44E6 DD 66 FD      [19]  848 	ld	h,-3 (ix)
   44E9 E5            [11]  849 	push	hl
   44EA CD 00 40      [17]  850 	call	_rect_overlap
   44ED FD 21 0C 00   [14]  851 	ld	iy, #12
   44F1 FD 39         [15]  852 	add	iy, sp
   44F3 FD F9         [10]  853 	ld	sp, iy
   44F5 D1            [10]  854 	pop	de
   44F6 7D            [ 4]  855 	ld	a, l
   44F7 B7            [ 4]  856 	or	a, a
   44F8 28 14         [12]  857 	jr	Z,00130$
                            858 ;src/game.c:152: if (g_lives) g_lives--;
   44FA FD 21 70 5A   [14]  859 	ld	iy, #_g_lives
   44FE FD 7E 00      [19]  860 	ld	a, 0 (iy)
   4501 B7            [ 4]  861 	or	a, a
   4502 28 03         [12]  862 	jr	Z,00127$
   4504 FD 35 00      [23]  863 	dec	0 (iy)
   4507                     864 00127$:
                            865 ;src/game.c:153: g_damagecooldown = 40;
   4507 21 78 5A      [10]  866 	ld	hl,#_g_damagecooldown + 0
   450A 36 28         [10]  867 	ld	(hl), #0x28
                            868 ;src/game.c:154: break;
   450C 18 0B         [12]  869 	jr	00131$
   450E                     870 00130$:
                            871 ;src/game.c:148: for (i = 0; i < MAX_ENEMIES; ++i) {
   450E DD 34 F1      [23]  872 	inc	-15 (ix)
   4511 DD 7E F1      [19]  873 	ld	a, -15 (ix)
   4514 D6 06         [ 7]  874 	sub	a, #0x06
   4516 DA 4E 44      [10]  875 	jp	C, 00164$
   4519                     876 00131$:
                            877 ;src/game.c:158: if (!g_damagecooldown && collision_is_on_trap((i16)g_player.x, (i16)g_player.y, g_player.w, g_player.h)) {
   4519 3A 78 5A      [13]  878 	ld	a,(#_g_damagecooldown + 0)
   451C B7            [ 4]  879 	or	a, a
   451D 20 3A         [12]  880 	jr	NZ,00138$
   451F 3A FA 59      [13]  881 	ld	a, (#(_g_player + 0x0005) + 0)
   4522 F5            [11]  882 	push	af
   4523 1A            [ 7]  883 	ld	a, (de)
   4524 DD 77 F2      [19]  884 	ld	-14 (ix), a
   4527 F1            [10]  885 	pop	af
   4528 21 F6 59      [10]  886 	ld	hl, #(_g_player + 0x0001) + 0
   452B 4E            [ 7]  887 	ld	c, (hl)
   452C 06 00         [ 7]  888 	ld	b, #0x00
   452E 21 F5 59      [10]  889 	ld	hl, #_g_player + 0
   4531 5E            [ 7]  890 	ld	e, (hl)
   4532 16 00         [ 7]  891 	ld	d, #0x00
   4534 F5            [11]  892 	push	af
   4535 33            [ 6]  893 	inc	sp
   4536 DD 7E F2      [19]  894 	ld	a, -14 (ix)
   4539 F5            [11]  895 	push	af
   453A 33            [ 6]  896 	inc	sp
   453B C5            [11]  897 	push	bc
   453C D5            [11]  898 	push	de
   453D CD F4 47      [17]  899 	call	_collision_is_on_trap
   4540 F1            [10]  900 	pop	af
   4541 F1            [10]  901 	pop	af
   4542 F1            [10]  902 	pop	af
   4543 7D            [ 4]  903 	ld	a, l
   4544 B7            [ 4]  904 	or	a, a
   4545 28 12         [12]  905 	jr	Z,00138$
                            906 ;src/game.c:159: if (g_lives) g_lives--;
   4547 FD 21 70 5A   [14]  907 	ld	iy, #_g_lives
   454B FD 7E 00      [19]  908 	ld	a, 0 (iy)
   454E B7            [ 4]  909 	or	a, a
   454F 28 03         [12]  910 	jr	Z,00133$
   4551 FD 35 00      [23]  911 	dec	0 (iy)
   4554                     912 00133$:
                            913 ;src/game.c:160: g_damagecooldown = 40;
   4554 21 78 5A      [10]  914 	ld	hl,#_g_damagecooldown + 0
   4557 36 28         [10]  915 	ld	(hl), #0x28
   4559                     916 00138$:
                            917 ;src/game.c:164: if (g_lives == 0) {
   4559 3A 70 5A      [13]  918 	ld	a,(#_g_lives + 0)
   455C B7            [ 4]  919 	or	a, a
   455D 20 05         [12]  920 	jr	NZ,00140$
                            921 ;src/game.c:165: g_gameover = 1;
   455F 21 7B 5A      [10]  922 	ld	hl,#_g_gameover + 0
   4562 36 01         [10]  923 	ld	(hl), #0x01
   4564                     924 00140$:
                            925 ;src/game.c:168: if (g_aliveenemies == 0 && !g_gameover) {
   4564 3A 76 5A      [13]  926 	ld	a,(#_g_aliveenemies + 0)
   4567 B7            [ 4]  927 	or	a, a
   4568 20 3F         [12]  928 	jr	NZ,00150$
   456A 3A 7B 5A      [13]  929 	ld	a,(#_g_gameover + 0)
   456D B7            [ 4]  930 	or	a, a
   456E 20 39         [12]  931 	jr	NZ,00150$
                            932 ;src/game.c:169: if (g_currentwave < TOTAL_WAVES) {
   4570 3A 75 5A      [13]  933 	ld	a,(#_g_currentwave + 0)
   4573 D6 03         [ 7]  934 	sub	a, #0x03
   4575 30 20         [12]  935 	jr	NC,00147$
                            936 ;src/game.c:170: if (g_wavecooldown == 0) {
   4577 3A 77 5A      [13]  937 	ld	a,(#_g_wavecooldown + 0)
   457A B7            [ 4]  938 	or	a, a
   457B 20 14         [12]  939 	jr	NZ,00142$
                            940 ;src/game.c:171: spawn_wave(g_currentwave);
   457D 3A 75 5A      [13]  941 	ld	a, (_g_currentwave)
   4580 F5            [11]  942 	push	af
   4581 33            [ 6]  943 	inc	sp
   4582 CD 8D 40      [17]  944 	call	_spawn_wave
   4585 33            [ 6]  945 	inc	sp
                            946 ;src/game.c:172: g_currentwave++;
   4586 21 75 5A      [10]  947 	ld	hl, #_g_currentwave+0
   4589 34            [11]  948 	inc	(hl)
                            949 ;src/game.c:173: g_wavecooldown = 100;
   458A 21 77 5A      [10]  950 	ld	hl,#_g_wavecooldown + 0
   458D 36 64         [10]  951 	ld	(hl), #0x64
   458F 18 18         [12]  952 	jr	00150$
   4591                     953 00142$:
                            954 ;src/game.c:175: g_wavecooldown--;
   4591 21 77 5A      [10]  955 	ld	hl, #_g_wavecooldown+0
   4594 35            [11]  956 	dec	(hl)
   4595 18 12         [12]  957 	jr	00150$
   4597                     958 00147$:
                            959 ;src/game.c:177: } else if (g_player.x >= tilemap_goal_x()) {
   4597 21 F5 59      [10]  960 	ld	hl, #_g_player + 0
   459A 4E            [ 7]  961 	ld	c, (hl)
   459B C5            [11]  962 	push	bc
   459C CD 69 4C      [17]  963 	call	_tilemap_goal_x
   459F C1            [10]  964 	pop	bc
   45A0 79            [ 4]  965 	ld	a, c
   45A1 95            [ 4]  966 	sub	a, l
   45A2 38 05         [12]  967 	jr	C,00150$
                            968 ;src/game.c:178: g_victory = 1;
   45A4 21 7A 5A      [10]  969 	ld	hl,#_g_victory + 0
   45A7 36 01         [10]  970 	ld	(hl), #0x01
   45A9                     971 00150$:
                            972 ;src/game.c:182: g_framecounter++;
   45A9 FD 21 7C 5A   [14]  973 	ld	iy, #_g_framecounter
   45AD FD 34 00      [23]  974 	inc	0 (iy)
   45B0 20 03         [12]  975 	jr	NZ,00302$
   45B2 FD 34 01      [23]  976 	inc	1 (iy)
   45B5                     977 00302$:
                            978 ;src/game.c:183: if ((g_framecounter % 50) == 0 && g_timeleft > 0) {
   45B5 21 32 00      [10]  979 	ld	hl, #0x0032
   45B8 E5            [11]  980 	push	hl
   45B9 2A 7C 5A      [16]  981 	ld	hl, (_g_framecounter)
   45BC E5            [11]  982 	push	hl
   45BD CD D3 58      [17]  983 	call	__moduint
   45C0 F1            [10]  984 	pop	af
   45C1 F1            [10]  985 	pop	af
   45C2 7C            [ 4]  986 	ld	a, h
   45C3 B5            [ 4]  987 	or	a,l
   45C4 20 0D         [12]  988 	jr	NZ,00153$
   45C6 FD 21 73 5A   [14]  989 	ld	iy, #_g_timeleft
   45CA FD 7E 00      [19]  990 	ld	a, 0 (iy)
   45CD B7            [ 4]  991 	or	a, a
   45CE 28 03         [12]  992 	jr	Z,00153$
                            993 ;src/game.c:184: g_timeleft--;
   45D0 FD 35 00      [23]  994 	dec	0 (iy)
   45D3                     995 00153$:
                            996 ;src/game.c:186: if (g_timeleft == 0 && !g_victory) {
   45D3 3A 73 5A      [13]  997 	ld	a,(#_g_timeleft + 0)
   45D6 B7            [ 4]  998 	or	a, a
   45D7 20 0B         [12]  999 	jr	NZ,00156$
   45D9 3A 7A 5A      [13] 1000 	ld	a,(#_g_victory + 0)
   45DC B7            [ 4] 1001 	or	a, a
   45DD 20 05         [12] 1002 	jr	NZ,00156$
                           1003 ;src/game.c:187: g_gameover = 1;
   45DF 21 7B 5A      [10] 1004 	ld	hl,#_g_gameover + 0
   45E2 36 01         [10] 1005 	ld	(hl), #0x01
   45E4                    1006 00156$:
                           1007 ;src/game.c:190: hudupdate(g_lives, g_score, g_timeleft, g_weapon);
   45E4 3A 74 5A      [13] 1008 	ld	a, (_g_weapon)
   45E7 F5            [11] 1009 	push	af
   45E8 33            [ 6] 1010 	inc	sp
   45E9 3A 73 5A      [13] 1011 	ld	a, (_g_timeleft)
   45EC F5            [11] 1012 	push	af
   45ED 33            [ 6] 1013 	inc	sp
   45EE 2A 71 5A      [16] 1014 	ld	hl, (_g_score)
   45F1 E5            [11] 1015 	push	hl
   45F2 3A 70 5A      [13] 1016 	ld	a, (_g_lives)
   45F5 F5            [11] 1017 	push	af
   45F6 33            [ 6] 1018 	inc	sp
   45F7 CD 9E 49      [17] 1019 	call	_hudupdate
   45FA F1            [10] 1020 	pop	af
   45FB F1            [10] 1021 	pop	af
   45FC 33            [ 6] 1022 	inc	sp
   45FD                    1023 00165$:
   45FD DD F9         [10] 1024 	ld	sp, ix
   45FF DD E1         [14] 1025 	pop	ix
   4601 C9            [10] 1026 	ret
                           1027 ;src/game.c:193: void game_render(void) {
                           1028 ;	---------------------------------
                           1029 ; Function game_render
                           1030 ; ---------------------------------
   4602                    1031 _game_render::
                           1032 ;src/game.c:196: cpct_clearScreen(0x00);
   4602 21 00 40      [10] 1033 	ld	hl, #0x4000
   4605 E5            [11] 1034 	push	hl
   4606 AF            [ 4] 1035 	xor	a, a
   4607 F5            [11] 1036 	push	af
   4608 33            [ 6] 1037 	inc	sp
   4609 26 C0         [ 7] 1038 	ld	h, #0xc0
   460B E5            [11] 1039 	push	hl
   460C CD FE 58      [17] 1040 	call	_cpct_memset
                           1041 ;src/game.c:197: tilemap_render();
   460F CD 4A 4B      [17] 1042 	call	_tilemap_render
                           1043 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4612 0E 00         [ 7] 1044 	ld	c, #0x00
   4614                    1045 00108$:
                           1046 ;src/game.c:200: projectilerender(&g_projectiles[i]);
   4614 06 00         [ 7] 1047 	ld	b,#0x00
   4616 69            [ 4] 1048 	ld	l, c
   4617 60            [ 4] 1049 	ld	h, b
   4618 29            [11] 1050 	add	hl, hl
   4619 29            [11] 1051 	add	hl, hl
   461A 09            [11] 1052 	add	hl, bc
   461B 29            [11] 1053 	add	hl, hl
   461C 11 34 5A      [10] 1054 	ld	de, #_g_projectiles
   461F 19            [11] 1055 	add	hl, de
   4620 C5            [11] 1056 	push	bc
   4621 E5            [11] 1057 	push	hl
   4622 CD 01 57      [17] 1058 	call	_projectilerender
   4625 F1            [10] 1059 	pop	af
   4626 C1            [10] 1060 	pop	bc
                           1061 ;src/game.c:199: for (i = 0; i < MAX_PROJECTILES; ++i) {
   4627 0C            [ 4] 1062 	inc	c
   4628 79            [ 4] 1063 	ld	a, c
   4629 D6 06         [ 7] 1064 	sub	a, #0x06
   462B 38 E7         [12] 1065 	jr	C,00108$
                           1066 ;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
   462D 0E 00         [ 7] 1067 	ld	c, #0x00
   462F                    1068 00110$:
                           1069 ;src/game.c:204: enemyrender(&g_enemies[i]);
   462F 06 00         [ 7] 1070 	ld	b,#0x00
   4631 69            [ 4] 1071 	ld	l, c
   4632 60            [ 4] 1072 	ld	h, b
   4633 29            [11] 1073 	add	hl, hl
   4634 29            [11] 1074 	add	hl, hl
   4635 29            [11] 1075 	add	hl, hl
   4636 09            [11] 1076 	add	hl, bc
   4637 11 FE 59      [10] 1077 	ld	de, #_g_enemies
   463A 19            [11] 1078 	add	hl, de
   463B C5            [11] 1079 	push	bc
   463C E5            [11] 1080 	push	hl
   463D CD 50 51      [17] 1081 	call	_enemyrender
   4640 F1            [10] 1082 	pop	af
   4641 C1            [10] 1083 	pop	bc
                           1084 ;src/game.c:203: for (i = 0; i < MAX_ENEMIES; ++i) {
   4642 0C            [ 4] 1085 	inc	c
   4643 79            [ 4] 1086 	ld	a, c
   4644 D6 06         [ 7] 1087 	sub	a, #0x06
   4646 38 E7         [12] 1088 	jr	C,00110$
                           1089 ;src/game.c:207: playerrender(&g_player);
   4648 21 F5 59      [10] 1090 	ld	hl, #_g_player
   464B E5            [11] 1091 	push	hl
   464C CD 94 55      [17] 1092 	call	_playerrender
   464F F1            [10] 1093 	pop	af
                           1094 ;src/game.c:208: hudrender();
   4650 CD CF 49      [17] 1095 	call	_hudrender
                           1096 ;src/game.c:210: if (g_victory) {
   4653 3A 7A 5A      [13] 1097 	ld	a,(#_g_victory + 0)
   4656 B7            [ 4] 1098 	or	a, a
   4657 28 1B         [12] 1099 	jr	Z,00106$
                           1100 ;src/game.c:211: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x5C, 24, 8);
   4659 21 1C 48      [10] 1101 	ld	hl, #0x481c
   465C E5            [11] 1102 	push	hl
   465D 21 00 C0      [10] 1103 	ld	hl, #0xc000
   4660 E5            [11] 1104 	push	hl
   4661 CD D5 59      [17] 1105 	call	_cpct_getScreenPtr
   4664 01 18 08      [10] 1106 	ld	bc, #0x0818
   4667 C5            [11] 1107 	push	bc
   4668 3E 5C         [ 7] 1108 	ld	a, #0x5c
   466A F5            [11] 1109 	push	af
   466B 33            [ 6] 1110 	inc	sp
   466C E5            [11] 1111 	push	hl
   466D CD 1C 59      [17] 1112 	call	_cpct_drawSolidBox
   4670 F1            [10] 1113 	pop	af
   4671 F1            [10] 1114 	pop	af
   4672 33            [ 6] 1115 	inc	sp
   4673 C9            [10] 1116 	ret
   4674                    1117 00106$:
                           1118 ;src/game.c:212: } else if (g_gameover) {
   4674 3A 7B 5A      [13] 1119 	ld	a,(#_g_gameover + 0)
   4677 B7            [ 4] 1120 	or	a, a
   4678 C8            [11] 1121 	ret	Z
                           1122 ;src/game.c:213: cpct_drawSolidBox(cpct_getScreenPtr(CPCT_VMEM_START, 28, 72), 0x4C, 24, 8);
   4679 21 1C 48      [10] 1123 	ld	hl, #0x481c
   467C E5            [11] 1124 	push	hl
   467D 21 00 C0      [10] 1125 	ld	hl, #0xc000
   4680 E5            [11] 1126 	push	hl
   4681 CD D5 59      [17] 1127 	call	_cpct_getScreenPtr
   4684 01 18 08      [10] 1128 	ld	bc, #0x0818
   4687 C5            [11] 1129 	push	bc
   4688 3E 4C         [ 7] 1130 	ld	a, #0x4c
   468A F5            [11] 1131 	push	af
   468B 33            [ 6] 1132 	inc	sp
   468C E5            [11] 1133 	push	hl
   468D CD 1C 59      [17] 1134 	call	_cpct_drawSolidBox
   4690 F1            [10] 1135 	pop	af
   4691 F1            [10] 1136 	pop	af
   4692 33            [ 6] 1137 	inc	sp
   4693 C9            [10] 1138 	ret
                           1139 	.area _CODE
                           1140 	.area _INITIALIZER
                           1141 	.area _CABS (ABS)
