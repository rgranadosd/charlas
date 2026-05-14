                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module enemy
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _collision_clamp_y_at
                             12 	.globl _collision_is_on_ground_at
                             13 	.globl _cpct_getScreenPtr
                             14 	.globl _cpct_drawSolidBox
                             15 	.globl _enemyinit
                             16 	.globl _enemyspawn
                             17 	.globl _enemyupdate
                             18 	.globl _enemyrender
                             19 	.globl _enemydamage
                             20 ;--------------------------------------------------------
                             21 ; special function registers
                             22 ;--------------------------------------------------------
                             23 ;--------------------------------------------------------
                             24 ; ram data
                             25 ;--------------------------------------------------------
                             26 	.area _DATA
                             27 ;--------------------------------------------------------
                             28 ; ram data
                             29 ;--------------------------------------------------------
                             30 	.area _INITIALIZED
                             31 ;--------------------------------------------------------
                             32 ; absolute external ram data
                             33 ;--------------------------------------------------------
                             34 	.area _DABS (ABS)
                             35 ;--------------------------------------------------------
                             36 ; global & static initialisations
                             37 ;--------------------------------------------------------
                             38 	.area _HOME
                             39 	.area _GSINIT
                             40 	.area _GSFINAL
                             41 	.area _GSINIT
                             42 ;--------------------------------------------------------
                             43 ; Home
                             44 ;--------------------------------------------------------
                             45 	.area _HOME
                             46 	.area _HOME
                             47 ;--------------------------------------------------------
                             48 ; code
                             49 ;--------------------------------------------------------
                             50 	.area _CODE
                             51 ;src/entities/enemy.c:5: void enemyinit(Enemy* enemy) {
                             52 ;	---------------------------------
                             53 ; Function enemyinit
                             54 ; ---------------------------------
   515D                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   515D 21 03 00      [10]   57 	ld	hl, #2+1
   5160 39            [11]   58 	add	hl, sp
   5161 7E            [ 7]   59 	ld	a, (hl)
   5162 2B            [ 6]   60 	dec	hl
   5163 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   5164 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   5165 D1            [10]   65 	pop	de
   5166 C1            [10]   66 	pop	bc
   5167 C5            [11]   67 	push	bc
   5168 D5            [11]   68 	push	de
   5169 AF            [ 4]   69 	xor	a, a
   516A 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   516B 59            [ 4]   72 	ld	e, c
   516C 50            [ 4]   73 	ld	d, b
   516D 13            [ 6]   74 	inc	de
   516E AF            [ 4]   75 	xor	a, a
   516F 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   5170 59            [ 4]   78 	ld	e, c
   5171 50            [ 4]   79 	ld	d, b
   5172 13            [ 6]   80 	inc	de
   5173 13            [ 6]   81 	inc	de
   5174 AF            [ 4]   82 	xor	a, a
   5175 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   5176 59            [ 4]   85 	ld	e, c
   5177 50            [ 4]   86 	ld	d, b
   5178 13            [ 6]   87 	inc	de
   5179 13            [ 6]   88 	inc	de
   517A 13            [ 6]   89 	inc	de
   517B AF            [ 4]   90 	xor	a, a
   517C 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   517D 21 04 00      [10]   93 	ld	hl, #0x0004
   5180 09            [11]   94 	add	hl, bc
   5181 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   5183 21 05 00      [10]   97 	ld	hl, #0x0005
   5186 09            [11]   98 	add	hl, bc
   5187 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   5189 21 06 00      [10]  101 	ld	hl, #0x0006
   518C 09            [11]  102 	add	hl, bc
   518D 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   518F 21 07 00      [10]  105 	ld	hl, #0x0007
   5192 09            [11]  106 	add	hl, bc
   5193 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   5195 21 08 00      [10]  109 	ld	hl, #0x0008
   5198 09            [11]  110 	add	hl, bc
   5199 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:19: enemy->kind = 0;
   519B 21 09 00      [10]  113 	ld	hl, #0x0009
   519E 09            [11]  114 	add	hl, bc
   519F 36 00         [10]  115 	ld	(hl), #0x00
   51A1 C9            [10]  116 	ret
                            117 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            118 ;	---------------------------------
                            119 ; Function enemyspawn
                            120 ; ---------------------------------
   51A2                     121 _enemyspawn::
   51A2 DD E5         [15]  122 	push	ix
   51A4 DD 21 00 00   [14]  123 	ld	ix,#0
   51A8 DD 39         [15]  124 	add	ix,sp
   51AA 21 F1 FF      [10]  125 	ld	hl, #-15
   51AD 39            [11]  126 	add	hl, sp
   51AE F9            [ 6]  127 	ld	sp, hl
                            128 ;src/entities/enemy.c:23: if (!enemy) {
   51AF DD 7E 05      [19]  129 	ld	a, 5 (ix)
   51B2 DD B6 04      [19]  130 	or	a,4 (ix)
                            131 ;src/entities/enemy.c:24: return;
   51B5 CA 75 53      [10]  132 	jp	Z,00112$
                            133 ;src/entities/enemy.c:27: enemy->x = x;
   51B8 DD 7E 04      [19]  134 	ld	a, 4 (ix)
   51BB DD 77 FE      [19]  135 	ld	-2 (ix), a
   51BE DD 7E 05      [19]  136 	ld	a, 5 (ix)
   51C1 DD 77 FF      [19]  137 	ld	-1 (ix), a
   51C4 DD 6E FE      [19]  138 	ld	l,-2 (ix)
   51C7 DD 66 FF      [19]  139 	ld	h,-1 (ix)
   51CA DD 7E 06      [19]  140 	ld	a, 6 (ix)
   51CD 77            [ 7]  141 	ld	(hl), a
                            142 ;src/entities/enemy.c:28: enemy->y = y;
   51CE DD 4E FE      [19]  143 	ld	c,-2 (ix)
   51D1 DD 46 FF      [19]  144 	ld	b,-1 (ix)
   51D4 03            [ 6]  145 	inc	bc
   51D5 DD 7E 07      [19]  146 	ld	a, 7 (ix)
   51D8 02            [ 7]  147 	ld	(bc), a
                            148 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   51D9 DD 7E FE      [19]  149 	ld	a, -2 (ix)
   51DC C6 02         [ 7]  150 	add	a, #0x02
   51DE DD 77 FC      [19]  151 	ld	-4 (ix), a
   51E1 DD 7E FF      [19]  152 	ld	a, -1 (ix)
   51E4 CE 00         [ 7]  153 	adc	a, #0x00
   51E6 DD 77 FD      [19]  154 	ld	-3 (ix), a
   51E9 DD 7E 09      [19]  155 	ld	a, 9 (ix)
   51EC B7            [ 4]  156 	or	a, a
   51ED 28 04         [12]  157 	jr	Z,00114$
   51EF 0E 01         [ 7]  158 	ld	c, #0x01
   51F1 18 02         [12]  159 	jr	00115$
   51F3                     160 00114$:
   51F3 0E FF         [ 7]  161 	ld	c, #0xff
   51F5                     162 00115$:
   51F5 DD 6E FC      [19]  163 	ld	l,-4 (ix)
   51F8 DD 66 FD      [19]  164 	ld	h,-3 (ix)
   51FB 71            [ 7]  165 	ld	(hl), c
                            166 ;src/entities/enemy.c:30: enemy->vy = 0;
   51FC DD 7E FE      [19]  167 	ld	a, -2 (ix)
   51FF C6 03         [ 7]  168 	add	a, #0x03
   5201 DD 77 FA      [19]  169 	ld	-6 (ix), a
   5204 DD 7E FF      [19]  170 	ld	a, -1 (ix)
   5207 CE 00         [ 7]  171 	adc	a, #0x00
   5209 DD 77 FB      [19]  172 	ld	-5 (ix), a
   520C DD 6E FA      [19]  173 	ld	l,-6 (ix)
   520F DD 66 FB      [19]  174 	ld	h,-5 (ix)
   5212 36 00         [10]  175 	ld	(hl), #0x00
                            176 ;src/entities/enemy.c:31: enemy->active = 1;
   5214 DD 7E FE      [19]  177 	ld	a, -2 (ix)
   5217 C6 06         [ 7]  178 	add	a, #0x06
   5219 DD 77 F8      [19]  179 	ld	-8 (ix), a
   521C DD 7E FF      [19]  180 	ld	a, -1 (ix)
   521F CE 00         [ 7]  181 	adc	a, #0x00
   5221 DD 77 F9      [19]  182 	ld	-7 (ix), a
   5224 DD 6E F8      [19]  183 	ld	l,-8 (ix)
   5227 DD 66 F9      [19]  184 	ld	h,-7 (ix)
   522A 36 01         [10]  185 	ld	(hl), #0x01
                            186 ;src/entities/enemy.c:32: enemy->kind = kind;
   522C DD 7E FE      [19]  187 	ld	a, -2 (ix)
   522F C6 09         [ 7]  188 	add	a, #0x09
   5231 DD 77 F8      [19]  189 	ld	-8 (ix), a
   5234 DD 7E FF      [19]  190 	ld	a, -1 (ix)
   5237 CE 00         [ 7]  191 	adc	a, #0x00
   5239 DD 77 F9      [19]  192 	ld	-7 (ix), a
   523C DD 6E F8      [19]  193 	ld	l,-8 (ix)
   523F DD 66 F9      [19]  194 	ld	h,-7 (ix)
   5242 DD 7E 08      [19]  195 	ld	a, 8 (ix)
   5245 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/enemy.c:35: enemy->w = 5;
   5246 DD 7E FE      [19]  198 	ld	a, -2 (ix)
   5249 C6 04         [ 7]  199 	add	a, #0x04
   524B DD 77 F8      [19]  200 	ld	-8 (ix), a
   524E DD 7E FF      [19]  201 	ld	a, -1 (ix)
   5251 CE 00         [ 7]  202 	adc	a, #0x00
   5253 DD 77 F9      [19]  203 	ld	-7 (ix), a
                            204 ;src/entities/enemy.c:36: enemy->h = 14;
   5256 DD 7E FE      [19]  205 	ld	a, -2 (ix)
   5259 C6 05         [ 7]  206 	add	a, #0x05
   525B DD 77 F6      [19]  207 	ld	-10 (ix), a
   525E DD 7E FF      [19]  208 	ld	a, -1 (ix)
   5261 CE 00         [ 7]  209 	adc	a, #0x00
   5263 DD 77 F7      [19]  210 	ld	-9 (ix), a
                            211 ;src/entities/enemy.c:37: enemy->health = 2;
   5266 DD 7E FE      [19]  212 	ld	a, -2 (ix)
   5269 C6 07         [ 7]  213 	add	a, #0x07
   526B DD 77 F4      [19]  214 	ld	-12 (ix), a
   526E DD 7E FF      [19]  215 	ld	a, -1 (ix)
   5271 CE 00         [ 7]  216 	adc	a, #0x00
   5273 DD 77 F5      [19]  217 	ld	-11 (ix), a
                            218 ;src/entities/enemy.c:38: enemy->reward = 180;
   5276 DD 7E FE      [19]  219 	ld	a, -2 (ix)
   5279 C6 08         [ 7]  220 	add	a, #0x08
   527B DD 77 FE      [19]  221 	ld	-2 (ix), a
   527E DD 7E FF      [19]  222 	ld	a, -1 (ix)
   5281 CE 00         [ 7]  223 	adc	a, #0x00
   5283 DD 77 FF      [19]  224 	ld	-1 (ix), a
                            225 ;src/entities/enemy.c:34: if (kind == 1) {
   5286 DD 7E 08      [19]  226 	ld	a, 8 (ix)
   5289 3D            [ 4]  227 	dec	a
   528A 20 49         [12]  228 	jr	NZ,00110$
                            229 ;src/entities/enemy.c:35: enemy->w = 5;
   528C DD 6E F8      [19]  230 	ld	l,-8 (ix)
   528F DD 66 F9      [19]  231 	ld	h,-7 (ix)
   5292 36 05         [10]  232 	ld	(hl), #0x05
                            233 ;src/entities/enemy.c:36: enemy->h = 14;
   5294 DD 6E F6      [19]  234 	ld	l,-10 (ix)
   5297 DD 66 F7      [19]  235 	ld	h,-9 (ix)
   529A 36 0E         [10]  236 	ld	(hl), #0x0e
                            237 ;src/entities/enemy.c:37: enemy->health = 2;
   529C DD 6E F4      [19]  238 	ld	l,-12 (ix)
   529F DD 66 F5      [19]  239 	ld	h,-11 (ix)
   52A2 36 02         [10]  240 	ld	(hl), #0x02
                            241 ;src/entities/enemy.c:38: enemy->reward = 180;
   52A4 DD 6E FE      [19]  242 	ld	l,-2 (ix)
   52A7 DD 66 FF      [19]  243 	ld	h,-1 (ix)
   52AA 36 B4         [10]  244 	ld	(hl), #0xb4
                            245 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   52AC DD 7E FC      [19]  246 	ld	a, -4 (ix)
   52AF DD 77 F2      [19]  247 	ld	-14 (ix), a
   52B2 DD 7E FD      [19]  248 	ld	a, -3 (ix)
   52B5 DD 77 F3      [19]  249 	ld	-13 (ix), a
   52B8 DD 7E 09      [19]  250 	ld	a, 9 (ix)
   52BB B7            [ 4]  251 	or	a, a
   52BC 28 06         [12]  252 	jr	Z,00116$
   52BE DD 36 F1 02   [19]  253 	ld	-15 (ix), #0x02
   52C2 18 04         [12]  254 	jr	00117$
   52C4                     255 00116$:
   52C4 DD 36 F1 FE   [19]  256 	ld	-15 (ix), #0xfe
   52C8                     257 00117$:
   52C8 DD 6E F2      [19]  258 	ld	l,-14 (ix)
   52CB DD 66 F3      [19]  259 	ld	h,-13 (ix)
   52CE DD 7E F1      [19]  260 	ld	a, -15 (ix)
   52D1 77            [ 7]  261 	ld	(hl), a
   52D2 C3 75 53      [10]  262 	jp	00112$
   52D5                     263 00110$:
                            264 ;src/entities/enemy.c:40: } else if (kind == 2) {
   52D5 DD 7E 08      [19]  265 	ld	a, 8 (ix)
   52D8 D6 02         [ 7]  266 	sub	a, #0x02
   52DA 20 3D         [12]  267 	jr	NZ,00107$
                            268 ;src/entities/enemy.c:41: enemy->w = 6;
   52DC DD 6E F8      [19]  269 	ld	l,-8 (ix)
   52DF DD 66 F9      [19]  270 	ld	h,-7 (ix)
   52E2 36 06         [10]  271 	ld	(hl), #0x06
                            272 ;src/entities/enemy.c:42: enemy->h = 10;
   52E4 DD 6E F6      [19]  273 	ld	l,-10 (ix)
   52E7 DD 66 F7      [19]  274 	ld	h,-9 (ix)
   52EA 36 0A         [10]  275 	ld	(hl), #0x0a
                            276 ;src/entities/enemy.c:43: enemy->health = 1;
   52EC DD 6E F4      [19]  277 	ld	l,-12 (ix)
   52EF DD 66 F5      [19]  278 	ld	h,-11 (ix)
   52F2 36 01         [10]  279 	ld	(hl), #0x01
                            280 ;src/entities/enemy.c:44: enemy->reward = 150;
   52F4 DD 6E FE      [19]  281 	ld	l,-2 (ix)
   52F7 DD 66 FF      [19]  282 	ld	h,-1 (ix)
   52FA 36 96         [10]  283 	ld	(hl), #0x96
                            284 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   52FC DD 4E FA      [19]  285 	ld	c,-6 (ix)
   52FF DD 46 FB      [19]  286 	ld	b,-5 (ix)
   5302 DD 7E 09      [19]  287 	ld	a, 9 (ix)
   5305 B7            [ 4]  288 	or	a, a
   5306 28 04         [12]  289 	jr	Z,00118$
   5308 3E 01         [ 7]  290 	ld	a, #0x01
   530A 18 02         [12]  291 	jr	00119$
   530C                     292 00118$:
   530C 3E FF         [ 7]  293 	ld	a, #0xff
   530E                     294 00119$:
   530E 02            [ 7]  295 	ld	(bc), a
                            296 ;src/entities/enemy.c:46: enemy->vx = 1;
   530F DD 6E FC      [19]  297 	ld	l,-4 (ix)
   5312 DD 66 FD      [19]  298 	ld	h,-3 (ix)
   5315 36 01         [10]  299 	ld	(hl), #0x01
   5317 18 5C         [12]  300 	jr	00112$
   5319                     301 00107$:
                            302 ;src/entities/enemy.c:47: } else if (kind == 3) {
   5319 DD 7E 08      [19]  303 	ld	a, 8 (ix)
   531C D6 03         [ 7]  304 	sub	a, #0x03
   531E 20 35         [12]  305 	jr	NZ,00104$
                            306 ;src/entities/enemy.c:48: enemy->w = 10;
   5320 DD 6E F8      [19]  307 	ld	l,-8 (ix)
   5323 DD 66 F9      [19]  308 	ld	h,-7 (ix)
   5326 36 0A         [10]  309 	ld	(hl), #0x0a
                            310 ;src/entities/enemy.c:49: enemy->h = 18;
   5328 DD 6E F6      [19]  311 	ld	l,-10 (ix)
   532B DD 66 F7      [19]  312 	ld	h,-9 (ix)
   532E 36 12         [10]  313 	ld	(hl), #0x12
                            314 ;src/entities/enemy.c:50: enemy->health = 8;
   5330 DD 6E F4      [19]  315 	ld	l,-12 (ix)
   5333 DD 66 F5      [19]  316 	ld	h,-11 (ix)
   5336 36 08         [10]  317 	ld	(hl), #0x08
                            318 ;src/entities/enemy.c:51: enemy->reward = 800;
   5338 DD 6E FE      [19]  319 	ld	l,-2 (ix)
   533B DD 66 FF      [19]  320 	ld	h,-1 (ix)
   533E 36 20         [10]  321 	ld	(hl), #0x20
                            322 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   5340 DD 4E FC      [19]  323 	ld	c,-4 (ix)
   5343 DD 46 FD      [19]  324 	ld	b,-3 (ix)
   5346 DD 7E 09      [19]  325 	ld	a, 9 (ix)
   5349 B7            [ 4]  326 	or	a, a
   534A 28 04         [12]  327 	jr	Z,00120$
   534C 3E 01         [ 7]  328 	ld	a, #0x01
   534E 18 02         [12]  329 	jr	00121$
   5350                     330 00120$:
   5350 3E FF         [ 7]  331 	ld	a, #0xff
   5352                     332 00121$:
   5352 02            [ 7]  333 	ld	(bc), a
   5353 18 20         [12]  334 	jr	00112$
   5355                     335 00104$:
                            336 ;src/entities/enemy.c:54: enemy->w = 4;
   5355 DD 6E F8      [19]  337 	ld	l,-8 (ix)
   5358 DD 66 F9      [19]  338 	ld	h,-7 (ix)
   535B 36 04         [10]  339 	ld	(hl), #0x04
                            340 ;src/entities/enemy.c:55: enemy->h = 16;
   535D DD 6E F6      [19]  341 	ld	l,-10 (ix)
   5360 DD 66 F7      [19]  342 	ld	h,-9 (ix)
   5363 36 10         [10]  343 	ld	(hl), #0x10
                            344 ;src/entities/enemy.c:56: enemy->health = 1;
   5365 DD 6E F4      [19]  345 	ld	l,-12 (ix)
   5368 DD 66 F5      [19]  346 	ld	h,-11 (ix)
   536B 36 01         [10]  347 	ld	(hl), #0x01
                            348 ;src/entities/enemy.c:57: enemy->reward = 100;
   536D DD 6E FE      [19]  349 	ld	l,-2 (ix)
   5370 DD 66 FF      [19]  350 	ld	h,-1 (ix)
   5373 36 64         [10]  351 	ld	(hl), #0x64
   5375                     352 00112$:
   5375 DD F9         [10]  353 	ld	sp, ix
   5377 DD E1         [14]  354 	pop	ix
   5379 C9            [10]  355 	ret
                            356 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            357 ;	---------------------------------
                            358 ; Function enemyupdate
                            359 ; ---------------------------------
   537A                     360 _enemyupdate::
   537A DD E5         [15]  361 	push	ix
   537C DD 21 00 00   [14]  362 	ld	ix,#0
   5380 DD 39         [15]  363 	add	ix,sp
   5382 21 F6 FF      [10]  364 	ld	hl, #-10
   5385 39            [11]  365 	add	hl, sp
   5386 F9            [ 6]  366 	ld	sp, hl
                            367 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   5387 DD 7E 05      [19]  368 	ld	a, 5 (ix)
   538A DD B6 04      [19]  369 	or	a,4 (ix)
   538D CA 70 55      [10]  370 	jp	Z,00121$
   5390 DD 7E 04      [19]  371 	ld	a, 4 (ix)
   5393 DD 77 FE      [19]  372 	ld	-2 (ix), a
   5396 DD 7E 05      [19]  373 	ld	a, 5 (ix)
   5399 DD 77 FF      [19]  374 	ld	-1 (ix), a
   539C DD 6E FE      [19]  375 	ld	l,-2 (ix)
   539F DD 66 FF      [19]  376 	ld	h,-1 (ix)
   53A2 11 06 00      [10]  377 	ld	de, #0x0006
   53A5 19            [11]  378 	add	hl, de
   53A6 7E            [ 7]  379 	ld	a, (hl)
   53A7 B7            [ 4]  380 	or	a, a
                            381 ;src/entities/enemy.c:66: return;
   53A8 CA 70 55      [10]  382 	jp	Z,00121$
                            383 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   53AB DD 6E FE      [19]  384 	ld	l,-2 (ix)
   53AE DD 66 FF      [19]  385 	ld	h,-1 (ix)
   53B1 11 09 00      [10]  386 	ld	de, #0x0009
   53B4 19            [11]  387 	add	hl, de
   53B5 7E            [ 7]  388 	ld	a, (hl)
   53B6 DD 77 FB      [19]  389 	ld	-5 (ix), a
                            390 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   53B9 DD 6E FE      [19]  391 	ld	l,-2 (ix)
   53BC DD 66 FF      [19]  392 	ld	h,-1 (ix)
   53BF 4E            [ 7]  393 	ld	c, (hl)
   53C0 DD 7E FE      [19]  394 	ld	a, -2 (ix)
   53C3 C6 02         [ 7]  395 	add	a, #0x02
   53C5 DD 77 FC      [19]  396 	ld	-4 (ix), a
   53C8 DD 7E FF      [19]  397 	ld	a, -1 (ix)
   53CB CE 00         [ 7]  398 	adc	a, #0x00
   53CD DD 77 FD      [19]  399 	ld	-3 (ix), a
                            400 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   53D0 DD 7E FE      [19]  401 	ld	a, -2 (ix)
   53D3 C6 01         [ 7]  402 	add	a, #0x01
   53D5 DD 77 F9      [19]  403 	ld	-7 (ix), a
   53D8 DD 7E FF      [19]  404 	ld	a, -1 (ix)
   53DB CE 00         [ 7]  405 	adc	a, #0x00
   53DD DD 77 FA      [19]  406 	ld	-6 (ix), a
   53E0 DD 5E FE      [19]  407 	ld	e,-2 (ix)
   53E3 DD 56 FF      [19]  408 	ld	d,-1 (ix)
   53E6 13            [ 6]  409 	inc	de
   53E7 13            [ 6]  410 	inc	de
   53E8 13            [ 6]  411 	inc	de
                            412 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   53E9 06 00         [ 7]  413 	ld	b, #0x00
   53EB DD 6E FC      [19]  414 	ld	l,-4 (ix)
   53EE DD 66 FD      [19]  415 	ld	h,-3 (ix)
   53F1 7E            [ 7]  416 	ld	a, (hl)
   53F2 DD 77 F8      [19]  417 	ld	-8 (ix), a
   53F5 6F            [ 4]  418 	ld	l, a
   53F6 DD 7E F8      [19]  419 	ld	a, -8 (ix)
   53F9 17            [ 4]  420 	rla
   53FA 9F            [ 4]  421 	sbc	a, a
   53FB 67            [ 4]  422 	ld	h, a
   53FC 09            [11]  423 	add	hl,bc
   53FD 4D            [ 4]  424 	ld	c, l
   53FE 44            [ 4]  425 	ld	b, h
                            426 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   53FF DD 7E FB      [19]  427 	ld	a, -5 (ix)
   5402 D6 02         [ 7]  428 	sub	a, #0x02
   5404 C2 AD 54      [10]  429 	jp	NZ,00111$
                            430 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            431 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5407 DD 6E F9      [19]  432 	ld	l,-7 (ix)
   540A DD 66 FA      [19]  433 	ld	h,-6 (ix)
   540D 6E            [ 7]  434 	ld	l, (hl)
   540E DD 75 F6      [19]  435 	ld	-10 (ix), l
   5411 DD 36 F7 00   [19]  436 	ld	-9 (ix), #0x00
   5415 1A            [ 7]  437 	ld	a, (de)
   5416 6F            [ 4]  438 	ld	l, a
   5417 17            [ 4]  439 	rla
   5418 9F            [ 4]  440 	sbc	a, a
   5419 67            [ 4]  441 	ld	h, a
   541A DD 7E F6      [19]  442 	ld	a, -10 (ix)
   541D 85            [ 4]  443 	add	a, l
   541E DD 77 F6      [19]  444 	ld	-10 (ix), a
   5421 DD 7E F7      [19]  445 	ld	a, -9 (ix)
   5424 8C            [ 4]  446 	adc	a, h
   5425 DD 77 F7      [19]  447 	ld	-9 (ix), a
                            448 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   5428 79            [ 4]  449 	ld	a, c
   5429 D6 08         [ 7]  450 	sub	a, #0x08
   542B 78            [ 4]  451 	ld	a, b
   542C 17            [ 4]  452 	rla
   542D 3F            [ 4]  453 	ccf
   542E 1F            [ 4]  454 	rra
   542F DE 80         [ 7]  455 	sbc	a, #0x80
   5431 38 0E         [12]  456 	jr	C,00104$
   5433 3E 48         [ 7]  457 	ld	a, #0x48
   5435 B9            [ 4]  458 	cp	a, c
   5436 3E 00         [ 7]  459 	ld	a, #0x00
   5438 98            [ 4]  460 	sbc	a, b
   5439 E2 3E 54      [10]  461 	jp	PO, 00161$
   543C EE 80         [ 7]  462 	xor	a, #0x80
   543E                     463 00161$:
   543E F2 5C 54      [10]  464 	jp	P, 00105$
   5441                     465 00104$:
                            466 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   5441 AF            [ 4]  467 	xor	a, a
   5442 DD 96 F8      [19]  468 	sub	a, -8 (ix)
   5445 4F            [ 4]  469 	ld	c, a
   5446 DD 6E FC      [19]  470 	ld	l,-4 (ix)
   5449 DD 66 FD      [19]  471 	ld	h,-3 (ix)
   544C 71            [ 7]  472 	ld	(hl), c
                            473 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   544D DD 6E FE      [19]  474 	ld	l,-2 (ix)
   5450 DD 66 FF      [19]  475 	ld	h,-1 (ix)
   5453 6E            [ 7]  476 	ld	l, (hl)
   5454 26 00         [ 7]  477 	ld	h, #0x00
   5456 79            [ 4]  478 	ld	a, c
   5457 17            [ 4]  479 	rla
   5458 9F            [ 4]  480 	sbc	a, a
   5459 47            [ 4]  481 	ld	b, a
   545A 09            [11]  482 	add	hl,bc
   545B 4D            [ 4]  483 	ld	c, l
   545C                     484 00105$:
                            485 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   545C DD 7E F6      [19]  486 	ld	a, -10 (ix)
   545F D6 38         [ 7]  487 	sub	a, #0x38
   5461 DD 7E F7      [19]  488 	ld	a, -9 (ix)
   5464 17            [ 4]  489 	rla
   5465 3F            [ 4]  490 	ccf
   5466 1F            [ 4]  491 	rra
   5467 DE 80         [ 7]  492 	sbc	a, #0x80
   5469 38 12         [12]  493 	jr	C,00107$
   546B 3E 78         [ 7]  494 	ld	a, #0x78
   546D DD BE F6      [19]  495 	cp	a, -10 (ix)
   5470 3E 00         [ 7]  496 	ld	a, #0x00
   5472 DD 9E F7      [19]  497 	sbc	a, -9 (ix)
   5475 E2 7A 54      [10]  498 	jp	PO, 00162$
   5478 EE 80         [ 7]  499 	xor	a, #0x80
   547A                     500 00162$:
   547A F2 99 54      [10]  501 	jp	P, 00108$
   547D                     502 00107$:
                            503 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   547D 1A            [ 7]  504 	ld	a, (de)
   547E 6F            [ 4]  505 	ld	l, a
   547F AF            [ 4]  506 	xor	a, a
   5480 95            [ 4]  507 	sub	a, l
   5481 DD 77 F8      [19]  508 	ld	-8 (ix), a
   5484 12            [ 7]  509 	ld	(de),a
                            510 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5485 DD 6E F9      [19]  511 	ld	l,-7 (ix)
   5488 DD 66 FA      [19]  512 	ld	h,-6 (ix)
   548B 5E            [ 7]  513 	ld	e, (hl)
   548C 16 00         [ 7]  514 	ld	d, #0x00
   548E DD 6E F8      [19]  515 	ld	l, -8 (ix)
   5491 DD 7E F8      [19]  516 	ld	a, -8 (ix)
   5494 17            [ 4]  517 	rla
   5495 9F            [ 4]  518 	sbc	a, a
   5496 67            [ 4]  519 	ld	h, a
   5497 19            [11]  520 	add	hl,de
   5498 E3            [19]  521 	ex	(sp), hl
   5499                     522 00108$:
                            523 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   5499 DD 6E FE      [19]  524 	ld	l,-2 (ix)
   549C DD 66 FF      [19]  525 	ld	h,-1 (ix)
   549F 71            [ 7]  526 	ld	(hl), c
                            527 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   54A0 DD 4E F6      [19]  528 	ld	c, -10 (ix)
   54A3 DD 6E F9      [19]  529 	ld	l,-7 (ix)
   54A6 DD 66 FA      [19]  530 	ld	h,-6 (ix)
   54A9 71            [ 7]  531 	ld	(hl), c
                            532 ;src/entities/enemy.c:84: return;
   54AA C3 70 55      [10]  533 	jp	00121$
   54AD                     534 00111$:
                            535 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            536 ;src/entities/enemy.c:88: if (nextx < 2) {
   54AD 79            [ 4]  537 	ld	a, c
   54AE D6 02         [ 7]  538 	sub	a, #0x02
   54B0 78            [ 4]  539 	ld	a, b
   54B1 17            [ 4]  540 	rla
   54B2 3F            [ 4]  541 	ccf
   54B3 1F            [ 4]  542 	rra
   54B4 DE 80         [ 7]  543 	sbc	a, #0x80
   54B6 30 0B         [12]  544 	jr	NC,00113$
                            545 ;src/entities/enemy.c:89: nextx = 2;
   54B8 01 02 00      [10]  546 	ld	bc, #0x0002
                            547 ;src/entities/enemy.c:90: enemy->vx = 1;
   54BB DD 6E FC      [19]  548 	ld	l,-4 (ix)
   54BE DD 66 FD      [19]  549 	ld	h,-3 (ix)
   54C1 36 01         [10]  550 	ld	(hl), #0x01
   54C3                     551 00113$:
                            552 ;src/entities/enemy.c:92: if (nextx > 74) {
   54C3 3E 4A         [ 7]  553 	ld	a, #0x4a
   54C5 B9            [ 4]  554 	cp	a, c
   54C6 3E 00         [ 7]  555 	ld	a, #0x00
   54C8 98            [ 4]  556 	sbc	a, b
   54C9 E2 CE 54      [10]  557 	jp	PO, 00163$
   54CC EE 80         [ 7]  558 	xor	a, #0x80
   54CE                     559 00163$:
   54CE F2 DC 54      [10]  560 	jp	P, 00115$
                            561 ;src/entities/enemy.c:93: nextx = 74;
   54D1 01 4A 00      [10]  562 	ld	bc, #0x004a
                            563 ;src/entities/enemy.c:94: enemy->vx = -1;
   54D4 DD 6E FC      [19]  564 	ld	l,-4 (ix)
   54D7 DD 66 FD      [19]  565 	ld	h,-3 (ix)
   54DA 36 FF         [10]  566 	ld	(hl), #0xff
   54DC                     567 00115$:
                            568 ;src/entities/enemy.c:96: enemy->x = (u8)nextx;
   54DC DD 6E FE      [19]  569 	ld	l,-2 (ix)
   54DF DD 66 FF      [19]  570 	ld	h,-1 (ix)
   54E2 71            [ 7]  571 	ld	(hl), c
                            572 ;src/entities/enemy.c:98: enemy->vy = (i8)(enemy->vy + 1);
   54E3 1A            [ 7]  573 	ld	a, (de)
   54E4 4F            [ 4]  574 	ld	c, a
   54E5 0C            [ 4]  575 	inc	c
   54E6 79            [ 4]  576 	ld	a, c
   54E7 12            [ 7]  577 	ld	(de), a
                            578 ;src/entities/enemy.c:99: if (enemy->vy > 3) enemy->vy = 3;
   54E8 3E 03         [ 7]  579 	ld	a, #0x03
   54EA 91            [ 4]  580 	sub	a, c
   54EB E2 F0 54      [10]  581 	jp	PO, 00164$
   54EE EE 80         [ 7]  582 	xor	a, #0x80
   54F0                     583 00164$:
   54F0 F2 F6 54      [10]  584 	jp	P, 00117$
   54F3 3E 03         [ 7]  585 	ld	a, #0x03
   54F5 12            [ 7]  586 	ld	(de), a
   54F6                     587 00117$:
                            588 ;src/entities/enemy.c:100: nexty = (i16)enemy->y + (i16)enemy->vy;
   54F6 DD 6E F9      [19]  589 	ld	l,-7 (ix)
   54F9 DD 66 FA      [19]  590 	ld	h,-6 (ix)
   54FC 4E            [ 7]  591 	ld	c, (hl)
   54FD 06 00         [ 7]  592 	ld	b, #0x00
   54FF 1A            [ 7]  593 	ld	a, (de)
   5500 6F            [ 4]  594 	ld	l, a
   5501 17            [ 4]  595 	rla
   5502 9F            [ 4]  596 	sbc	a, a
   5503 67            [ 4]  597 	ld	h, a
   5504 09            [11]  598 	add	hl, bc
   5505 E5            [11]  599 	push	hl
   5506 FD E1         [14]  600 	pop	iy
                            601 ;src/entities/enemy.c:101: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5508 DD 7E FE      [19]  602 	ld	a, -2 (ix)
   550B C6 05         [ 7]  603 	add	a, #0x05
   550D DD 77 F6      [19]  604 	ld	-10 (ix), a
   5510 DD 7E FF      [19]  605 	ld	a, -1 (ix)
   5513 CE 00         [ 7]  606 	adc	a, #0x00
   5515 DD 77 F7      [19]  607 	ld	-9 (ix), a
   5518 E1            [10]  608 	pop	hl
   5519 E5            [11]  609 	push	hl
   551A 7E            [ 7]  610 	ld	a, (hl)
   551B DD 6E FE      [19]  611 	ld	l,-2 (ix)
   551E DD 66 FF      [19]  612 	ld	h,-1 (ix)
   5521 4E            [ 7]  613 	ld	c, (hl)
   5522 06 00         [ 7]  614 	ld	b, #0x00
   5524 D5            [11]  615 	push	de
   5525 F5            [11]  616 	push	af
   5526 33            [ 6]  617 	inc	sp
   5527 FD E5         [15]  618 	push	iy
   5529 C5            [11]  619 	push	bc
   552A CD BC 4B      [17]  620 	call	_collision_clamp_y_at
   552D F1            [10]  621 	pop	af
   552E F1            [10]  622 	pop	af
   552F 33            [ 6]  623 	inc	sp
   5530 4D            [ 4]  624 	ld	c, l
   5531 D1            [10]  625 	pop	de
                            626 ;src/entities/enemy.c:102: enemy->y = (u8)nexty;
   5532 DD 6E F9      [19]  627 	ld	l,-7 (ix)
   5535 DD 66 FA      [19]  628 	ld	h,-6 (ix)
   5538 71            [ 7]  629 	ld	(hl), c
                            630 ;src/entities/enemy.c:103: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5539 E1            [10]  631 	pop	hl
   553A E5            [11]  632 	push	hl
   553B 7E            [ 7]  633 	ld	a, (hl)
   553C 06 00         [ 7]  634 	ld	b, #0x00
   553E DD 6E FE      [19]  635 	ld	l,-2 (ix)
   5541 DD 66 FF      [19]  636 	ld	h,-1 (ix)
   5544 6E            [ 7]  637 	ld	l, (hl)
   5545 DD 75 F6      [19]  638 	ld	-10 (ix), l
   5548 DD 36 F7 00   [19]  639 	ld	-9 (ix), #0x00
   554C D5            [11]  640 	push	de
   554D F5            [11]  641 	push	af
   554E 33            [ 6]  642 	inc	sp
   554F C5            [11]  643 	push	bc
   5550 DD 6E F6      [19]  644 	ld	l,-10 (ix)
   5553 DD 66 F7      [19]  645 	ld	h,-9 (ix)
   5556 E5            [11]  646 	push	hl
   5557 CD 3D 4B      [17]  647 	call	_collision_is_on_ground_at
   555A F1            [10]  648 	pop	af
   555B F1            [10]  649 	pop	af
   555C 33            [ 6]  650 	inc	sp
   555D D1            [10]  651 	pop	de
   555E 7D            [ 4]  652 	ld	a, l
   555F B7            [ 4]  653 	or	a, a
   5560 28 0E         [12]  654 	jr	Z,00121$
   5562 1A            [ 7]  655 	ld	a, (de)
   5563 4F            [ 4]  656 	ld	c, a
   5564 AF            [ 4]  657 	xor	a, a
   5565 91            [ 4]  658 	sub	a, c
   5566 E2 6B 55      [10]  659 	jp	PO, 00165$
   5569 EE 80         [ 7]  660 	xor	a, #0x80
   556B                     661 00165$:
   556B F2 70 55      [10]  662 	jp	P, 00121$
                            663 ;src/entities/enemy.c:104: enemy->vy = 0;
   556E AF            [ 4]  664 	xor	a, a
   556F 12            [ 7]  665 	ld	(de), a
   5570                     666 00121$:
   5570 DD F9         [10]  667 	ld	sp, ix
   5572 DD E1         [14]  668 	pop	ix
   5574 C9            [10]  669 	ret
                            670 ;src/entities/enemy.c:108: void enemyrender(const Enemy* enemy) {
                            671 ;	---------------------------------
                            672 ; Function enemyrender
                            673 ; ---------------------------------
   5575                     674 _enemyrender::
   5575 DD E5         [15]  675 	push	ix
   5577 DD 21 00 00   [14]  676 	ld	ix,#0
   557B DD 39         [15]  677 	add	ix,sp
   557D 3B            [ 6]  678 	dec	sp
                            679 ;src/entities/enemy.c:112: if (!enemy || !enemy->active) {
   557E DD 7E 05      [19]  680 	ld	a, 5 (ix)
   5581 DD B6 04      [19]  681 	or	a,4 (ix)
   5584 28 65         [12]  682 	jr	Z,00113$
   5586 DD 4E 04      [19]  683 	ld	c,4 (ix)
   5589 DD 46 05      [19]  684 	ld	b,5 (ix)
   558C C5            [11]  685 	push	bc
   558D FD E1         [14]  686 	pop	iy
   558F FD 7E 06      [19]  687 	ld	a, 6 (iy)
   5592 B7            [ 4]  688 	or	a, a
                            689 ;src/entities/enemy.c:113: return;
   5593 28 56         [12]  690 	jr	Z,00113$
                            691 ;src/entities/enemy.c:116: if (enemy->kind == 3) colour = 0x4C;
   5595 C5            [11]  692 	push	bc
   5596 FD E1         [14]  693 	pop	iy
   5598 FD 7E 09      [19]  694 	ld	a, 9 (iy)
   559B FE 03         [ 7]  695 	cp	a, #0x03
   559D 20 04         [12]  696 	jr	NZ,00111$
   559F 1E 4C         [ 7]  697 	ld	e, #0x4c
   55A1 18 11         [12]  698 	jr	00112$
   55A3                     699 00111$:
                            700 ;src/entities/enemy.c:117: else if (enemy->kind == 2) colour = 0x5A;
   55A3 FE 02         [ 7]  701 	cp	a, #0x02
   55A5 20 04         [12]  702 	jr	NZ,00108$
   55A7 1E 5A         [ 7]  703 	ld	e, #0x5a
   55A9 18 09         [12]  704 	jr	00112$
   55AB                     705 00108$:
                            706 ;src/entities/enemy.c:118: else if (enemy->kind == 1) colour = 0x4E;
   55AB 3D            [ 4]  707 	dec	a
   55AC 20 04         [12]  708 	jr	NZ,00105$
   55AE 1E 4E         [ 7]  709 	ld	e, #0x4e
   55B0 18 02         [12]  710 	jr	00112$
   55B2                     711 00105$:
                            712 ;src/entities/enemy.c:119: else colour = 0x5C;
   55B2 1E 5C         [ 7]  713 	ld	e, #0x5c
   55B4                     714 00112$:
                            715 ;src/entities/enemy.c:121: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   55B4 69            [ 4]  716 	ld	l, c
   55B5 60            [ 4]  717 	ld	h, b
   55B6 23            [ 6]  718 	inc	hl
   55B7 56            [ 7]  719 	ld	d, (hl)
   55B8 0A            [ 7]  720 	ld	a, (bc)
   55B9 C5            [11]  721 	push	bc
   55BA D5            [11]  722 	push	de
   55BB 5F            [ 4]  723 	ld	e, a
   55BC D5            [11]  724 	push	de
   55BD 21 00 C0      [10]  725 	ld	hl, #0xc000
   55C0 E5            [11]  726 	push	hl
   55C1 CD 62 5E      [17]  727 	call	_cpct_getScreenPtr
   55C4 D1            [10]  728 	pop	de
   55C5 C1            [10]  729 	pop	bc
   55C6 E5            [11]  730 	push	hl
   55C7 FD E1         [14]  731 	pop	iy
                            732 ;src/entities/enemy.c:122: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   55C9 69            [ 4]  733 	ld	l, c
   55CA 60            [ 4]  734 	ld	h, b
   55CB 23            [ 6]  735 	inc	hl
   55CC 23            [ 6]  736 	inc	hl
   55CD 23            [ 6]  737 	inc	hl
   55CE 23            [ 6]  738 	inc	hl
   55CF 23            [ 6]  739 	inc	hl
   55D0 7E            [ 7]  740 	ld	a, (hl)
   55D1 DD 77 FF      [19]  741 	ld	-1 (ix), a
   55D4 69            [ 4]  742 	ld	l, c
   55D5 60            [ 4]  743 	ld	h, b
   55D6 01 04 00      [10]  744 	ld	bc, #0x0004
   55D9 09            [11]  745 	add	hl, bc
   55DA 56            [ 7]  746 	ld	d, (hl)
   55DB FD E5         [15]  747 	push	iy
   55DD C1            [10]  748 	pop	bc
   55DE DD 7E FF      [19]  749 	ld	a, -1 (ix)
   55E1 F5            [11]  750 	push	af
   55E2 33            [ 6]  751 	inc	sp
   55E3 D5            [11]  752 	push	de
   55E4 C5            [11]  753 	push	bc
   55E5 CD A9 5D      [17]  754 	call	_cpct_drawSolidBox
   55E8 F1            [10]  755 	pop	af
   55E9 F1            [10]  756 	pop	af
   55EA 33            [ 6]  757 	inc	sp
   55EB                     758 00113$:
   55EB 33            [ 6]  759 	inc	sp
   55EC DD E1         [14]  760 	pop	ix
   55EE C9            [10]  761 	ret
                            762 ;src/entities/enemy.c:125: u8 enemydamage(Enemy* enemy, u8 damage) {
                            763 ;	---------------------------------
                            764 ; Function enemydamage
                            765 ; ---------------------------------
   55EF                     766 _enemydamage::
   55EF DD E5         [15]  767 	push	ix
   55F1 DD 21 00 00   [14]  768 	ld	ix,#0
   55F5 DD 39         [15]  769 	add	ix,sp
                            770 ;src/entities/enemy.c:126: if (!enemy || !enemy->active) {
   55F7 DD 7E 05      [19]  771 	ld	a, 5 (ix)
   55FA DD B6 04      [19]  772 	or	a,4 (ix)
   55FD 28 0F         [12]  773 	jr	Z,00101$
   55FF DD 4E 04      [19]  774 	ld	c,4 (ix)
   5602 DD 46 05      [19]  775 	ld	b,5 (ix)
   5605 21 06 00      [10]  776 	ld	hl, #0x0006
   5608 09            [11]  777 	add	hl,bc
   5609 EB            [ 4]  778 	ex	de,hl
   560A 1A            [ 7]  779 	ld	a, (de)
   560B B7            [ 4]  780 	or	a, a
   560C 20 04         [12]  781 	jr	NZ,00102$
   560E                     782 00101$:
                            783 ;src/entities/enemy.c:127: return 0;
   560E 2E 00         [ 7]  784 	ld	l, #0x00
   5610 18 1A         [12]  785 	jr	00106$
   5612                     786 00102$:
                            787 ;src/entities/enemy.c:130: if (damage >= enemy->health) {
   5612 21 07 00      [10]  788 	ld	hl, #0x0007
   5615 09            [11]  789 	add	hl, bc
   5616 4E            [ 7]  790 	ld	c, (hl)
   5617 DD 7E 06      [19]  791 	ld	a, 6 (ix)
   561A 91            [ 4]  792 	sub	a, c
   561B 38 08         [12]  793 	jr	C,00105$
                            794 ;src/entities/enemy.c:131: enemy->health = 0;
   561D 36 00         [10]  795 	ld	(hl), #0x00
                            796 ;src/entities/enemy.c:132: enemy->active = 0;
   561F AF            [ 4]  797 	xor	a, a
   5620 12            [ 7]  798 	ld	(de), a
                            799 ;src/entities/enemy.c:133: return 1;
   5621 2E 01         [ 7]  800 	ld	l, #0x01
   5623 18 07         [12]  801 	jr	00106$
   5625                     802 00105$:
                            803 ;src/entities/enemy.c:136: enemy->health = (u8)(enemy->health - damage);
   5625 79            [ 4]  804 	ld	a, c
   5626 DD 96 06      [19]  805 	sub	a, 6 (ix)
   5629 77            [ 7]  806 	ld	(hl), a
                            807 ;src/entities/enemy.c:137: return 0;
   562A 2E 00         [ 7]  808 	ld	l, #0x00
   562C                     809 00106$:
   562C DD E1         [14]  810 	pop	ix
   562E C9            [10]  811 	ret
                            812 	.area _CODE
                            813 	.area _INITIALIZER
                            814 	.area _CABS (ABS)
