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
                             15 	.globl _cpct_px2byteM0
                             16 	.globl _enemyinit
                             17 	.globl _enemyspawn
                             18 	.globl _enemyupdate
                             19 	.globl _enemyrender
                             20 	.globl _enemydamage
                             21 ;--------------------------------------------------------
                             22 ; special function registers
                             23 ;--------------------------------------------------------
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _DATA
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _INITIALIZED
                             32 ;--------------------------------------------------------
                             33 ; absolute external ram data
                             34 ;--------------------------------------------------------
                             35 	.area _DABS (ABS)
                             36 ;--------------------------------------------------------
                             37 ; global & static initialisations
                             38 ;--------------------------------------------------------
                             39 	.area _HOME
                             40 	.area _GSINIT
                             41 	.area _GSFINAL
                             42 	.area _GSINIT
                             43 ;--------------------------------------------------------
                             44 ; Home
                             45 ;--------------------------------------------------------
                             46 	.area _HOME
                             47 	.area _HOME
                             48 ;--------------------------------------------------------
                             49 ; code
                             50 ;--------------------------------------------------------
                             51 	.area _CODE
                             52 ;src/entities/enemy.c:5: void enemyinit(Enemy* enemy) {
                             53 ;	---------------------------------
                             54 ; Function enemyinit
                             55 ; ---------------------------------
   526A                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   526A 21 03 00      [10]   58 	ld	hl, #2+1
   526D 39            [11]   59 	add	hl, sp
   526E 7E            [ 7]   60 	ld	a, (hl)
   526F 2B            [ 6]   61 	dec	hl
   5270 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   5271 C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   5272 D1            [10]   66 	pop	de
   5273 C1            [10]   67 	pop	bc
   5274 C5            [11]   68 	push	bc
   5275 D5            [11]   69 	push	de
   5276 AF            [ 4]   70 	xor	a, a
   5277 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   5278 59            [ 4]   73 	ld	e, c
   5279 50            [ 4]   74 	ld	d, b
   527A 13            [ 6]   75 	inc	de
   527B AF            [ 4]   76 	xor	a, a
   527C 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   527D 59            [ 4]   79 	ld	e, c
   527E 50            [ 4]   80 	ld	d, b
   527F 13            [ 6]   81 	inc	de
   5280 13            [ 6]   82 	inc	de
   5281 AF            [ 4]   83 	xor	a, a
   5282 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   5283 59            [ 4]   86 	ld	e, c
   5284 50            [ 4]   87 	ld	d, b
   5285 13            [ 6]   88 	inc	de
   5286 13            [ 6]   89 	inc	de
   5287 13            [ 6]   90 	inc	de
   5288 AF            [ 4]   91 	xor	a, a
   5289 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   528A 21 04 00      [10]   94 	ld	hl, #0x0004
   528D 09            [11]   95 	add	hl, bc
   528E 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   5290 21 05 00      [10]   98 	ld	hl, #0x0005
   5293 09            [11]   99 	add	hl, bc
   5294 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5296 21 06 00      [10]  102 	ld	hl, #0x0006
   5299 09            [11]  103 	add	hl, bc
   529A 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   529C 21 07 00      [10]  106 	ld	hl, #0x0007
   529F 09            [11]  107 	add	hl, bc
   52A0 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   52A2 21 08 00      [10]  110 	ld	hl, #0x0008
   52A5 09            [11]  111 	add	hl, bc
   52A6 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   52A8 21 09 00      [10]  114 	ld	hl, #0x0009
   52AB 09            [11]  115 	add	hl, bc
   52AC 36 00         [10]  116 	ld	(hl), #0x00
   52AE C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   52AF                     122 _enemyspawn::
   52AF DD E5         [15]  123 	push	ix
   52B1 DD 21 00 00   [14]  124 	ld	ix,#0
   52B5 DD 39         [15]  125 	add	ix,sp
   52B7 21 F1 FF      [10]  126 	ld	hl, #-15
   52BA 39            [11]  127 	add	hl, sp
   52BB F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   52BC DD 7E 05      [19]  130 	ld	a, 5 (ix)
   52BF DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   52C2 CA 82 54      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   52C5 DD 7E 04      [19]  135 	ld	a, 4 (ix)
   52C8 DD 77 FE      [19]  136 	ld	-2 (ix), a
   52CB DD 7E 05      [19]  137 	ld	a, 5 (ix)
   52CE DD 77 FF      [19]  138 	ld	-1 (ix), a
   52D1 DD 6E FE      [19]  139 	ld	l,-2 (ix)
   52D4 DD 66 FF      [19]  140 	ld	h,-1 (ix)
   52D7 DD 7E 06      [19]  141 	ld	a, 6 (ix)
   52DA 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   52DB DD 4E FE      [19]  144 	ld	c,-2 (ix)
   52DE DD 46 FF      [19]  145 	ld	b,-1 (ix)
   52E1 03            [ 6]  146 	inc	bc
   52E2 DD 7E 07      [19]  147 	ld	a, 7 (ix)
   52E5 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   52E6 DD 7E FE      [19]  150 	ld	a, -2 (ix)
   52E9 C6 02         [ 7]  151 	add	a, #0x02
   52EB DD 77 FC      [19]  152 	ld	-4 (ix), a
   52EE DD 7E FF      [19]  153 	ld	a, -1 (ix)
   52F1 CE 00         [ 7]  154 	adc	a, #0x00
   52F3 DD 77 FD      [19]  155 	ld	-3 (ix), a
   52F6 DD 7E 09      [19]  156 	ld	a, 9 (ix)
   52F9 B7            [ 4]  157 	or	a, a
   52FA 28 04         [12]  158 	jr	Z,00114$
   52FC 0E 01         [ 7]  159 	ld	c, #0x01
   52FE 18 02         [12]  160 	jr	00115$
   5300                     161 00114$:
   5300 0E FF         [ 7]  162 	ld	c, #0xff
   5302                     163 00115$:
   5302 DD 6E FC      [19]  164 	ld	l,-4 (ix)
   5305 DD 66 FD      [19]  165 	ld	h,-3 (ix)
   5308 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   5309 DD 7E FE      [19]  168 	ld	a, -2 (ix)
   530C C6 03         [ 7]  169 	add	a, #0x03
   530E DD 77 FA      [19]  170 	ld	-6 (ix), a
   5311 DD 7E FF      [19]  171 	ld	a, -1 (ix)
   5314 CE 00         [ 7]  172 	adc	a, #0x00
   5316 DD 77 FB      [19]  173 	ld	-5 (ix), a
   5319 DD 6E FA      [19]  174 	ld	l,-6 (ix)
   531C DD 66 FB      [19]  175 	ld	h,-5 (ix)
   531F 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   5321 DD 7E FE      [19]  178 	ld	a, -2 (ix)
   5324 C6 06         [ 7]  179 	add	a, #0x06
   5326 DD 77 F8      [19]  180 	ld	-8 (ix), a
   5329 DD 7E FF      [19]  181 	ld	a, -1 (ix)
   532C CE 00         [ 7]  182 	adc	a, #0x00
   532E DD 77 F9      [19]  183 	ld	-7 (ix), a
   5331 DD 6E F8      [19]  184 	ld	l,-8 (ix)
   5334 DD 66 F9      [19]  185 	ld	h,-7 (ix)
   5337 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   5339 DD 7E FE      [19]  188 	ld	a, -2 (ix)
   533C C6 09         [ 7]  189 	add	a, #0x09
   533E DD 77 F8      [19]  190 	ld	-8 (ix), a
   5341 DD 7E FF      [19]  191 	ld	a, -1 (ix)
   5344 CE 00         [ 7]  192 	adc	a, #0x00
   5346 DD 77 F9      [19]  193 	ld	-7 (ix), a
   5349 DD 6E F8      [19]  194 	ld	l,-8 (ix)
   534C DD 66 F9      [19]  195 	ld	h,-7 (ix)
   534F DD 7E 08      [19]  196 	ld	a, 8 (ix)
   5352 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   5353 DD 7E FE      [19]  199 	ld	a, -2 (ix)
   5356 C6 04         [ 7]  200 	add	a, #0x04
   5358 DD 77 F8      [19]  201 	ld	-8 (ix), a
   535B DD 7E FF      [19]  202 	ld	a, -1 (ix)
   535E CE 00         [ 7]  203 	adc	a, #0x00
   5360 DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   5363 DD 7E FE      [19]  206 	ld	a, -2 (ix)
   5366 C6 05         [ 7]  207 	add	a, #0x05
   5368 DD 77 F6      [19]  208 	ld	-10 (ix), a
   536B DD 7E FF      [19]  209 	ld	a, -1 (ix)
   536E CE 00         [ 7]  210 	adc	a, #0x00
   5370 DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   5373 DD 7E FE      [19]  213 	ld	a, -2 (ix)
   5376 C6 07         [ 7]  214 	add	a, #0x07
   5378 DD 77 F4      [19]  215 	ld	-12 (ix), a
   537B DD 7E FF      [19]  216 	ld	a, -1 (ix)
   537E CE 00         [ 7]  217 	adc	a, #0x00
   5380 DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   5383 DD 7E FE      [19]  220 	ld	a, -2 (ix)
   5386 C6 08         [ 7]  221 	add	a, #0x08
   5388 DD 77 FE      [19]  222 	ld	-2 (ix), a
   538B DD 7E FF      [19]  223 	ld	a, -1 (ix)
   538E CE 00         [ 7]  224 	adc	a, #0x00
   5390 DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   5393 DD 7E 08      [19]  227 	ld	a, 8 (ix)
   5396 3D            [ 4]  228 	dec	a
   5397 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   5399 DD 6E F8      [19]  231 	ld	l,-8 (ix)
   539C DD 66 F9      [19]  232 	ld	h,-7 (ix)
   539F 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   53A1 DD 6E F6      [19]  235 	ld	l,-10 (ix)
   53A4 DD 66 F7      [19]  236 	ld	h,-9 (ix)
   53A7 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   53A9 DD 6E F4      [19]  239 	ld	l,-12 (ix)
   53AC DD 66 F5      [19]  240 	ld	h,-11 (ix)
   53AF 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   53B1 DD 6E FE      [19]  243 	ld	l,-2 (ix)
   53B4 DD 66 FF      [19]  244 	ld	h,-1 (ix)
   53B7 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   53B9 DD 7E FC      [19]  247 	ld	a, -4 (ix)
   53BC DD 77 F2      [19]  248 	ld	-14 (ix), a
   53BF DD 7E FD      [19]  249 	ld	a, -3 (ix)
   53C2 DD 77 F3      [19]  250 	ld	-13 (ix), a
   53C5 DD 7E 09      [19]  251 	ld	a, 9 (ix)
   53C8 B7            [ 4]  252 	or	a, a
   53C9 28 06         [12]  253 	jr	Z,00116$
   53CB DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   53CF 18 04         [12]  255 	jr	00117$
   53D1                     256 00116$:
   53D1 DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   53D5                     258 00117$:
   53D5 DD 6E F2      [19]  259 	ld	l,-14 (ix)
   53D8 DD 66 F3      [19]  260 	ld	h,-13 (ix)
   53DB DD 7E F1      [19]  261 	ld	a, -15 (ix)
   53DE 77            [ 7]  262 	ld	(hl), a
   53DF C3 82 54      [10]  263 	jp	00112$
   53E2                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   53E2 DD 7E 08      [19]  266 	ld	a, 8 (ix)
   53E5 D6 02         [ 7]  267 	sub	a, #0x02
   53E7 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   53E9 DD 6E F8      [19]  270 	ld	l,-8 (ix)
   53EC DD 66 F9      [19]  271 	ld	h,-7 (ix)
   53EF 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   53F1 DD 6E F6      [19]  274 	ld	l,-10 (ix)
   53F4 DD 66 F7      [19]  275 	ld	h,-9 (ix)
   53F7 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   53F9 DD 6E F4      [19]  278 	ld	l,-12 (ix)
   53FC DD 66 F5      [19]  279 	ld	h,-11 (ix)
   53FF 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   5401 DD 6E FE      [19]  282 	ld	l,-2 (ix)
   5404 DD 66 FF      [19]  283 	ld	h,-1 (ix)
   5407 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5409 DD 4E FA      [19]  286 	ld	c,-6 (ix)
   540C DD 46 FB      [19]  287 	ld	b,-5 (ix)
   540F DD 7E 09      [19]  288 	ld	a, 9 (ix)
   5412 B7            [ 4]  289 	or	a, a
   5413 28 04         [12]  290 	jr	Z,00118$
   5415 3E 01         [ 7]  291 	ld	a, #0x01
   5417 18 02         [12]  292 	jr	00119$
   5419                     293 00118$:
   5419 3E FF         [ 7]  294 	ld	a, #0xff
   541B                     295 00119$:
   541B 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   541C DD 6E FC      [19]  298 	ld	l,-4 (ix)
   541F DD 66 FD      [19]  299 	ld	h,-3 (ix)
   5422 36 01         [10]  300 	ld	(hl), #0x01
   5424 18 5C         [12]  301 	jr	00112$
   5426                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   5426 DD 7E 08      [19]  304 	ld	a, 8 (ix)
   5429 D6 03         [ 7]  305 	sub	a, #0x03
   542B 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   542D DD 6E F8      [19]  308 	ld	l,-8 (ix)
   5430 DD 66 F9      [19]  309 	ld	h,-7 (ix)
   5433 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   5435 DD 6E F6      [19]  312 	ld	l,-10 (ix)
   5438 DD 66 F7      [19]  313 	ld	h,-9 (ix)
   543B 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   543D DD 6E F4      [19]  316 	ld	l,-12 (ix)
   5440 DD 66 F5      [19]  317 	ld	h,-11 (ix)
   5443 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   5445 DD 6E FE      [19]  320 	ld	l,-2 (ix)
   5448 DD 66 FF      [19]  321 	ld	h,-1 (ix)
   544B 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   544D DD 4E FC      [19]  324 	ld	c,-4 (ix)
   5450 DD 46 FD      [19]  325 	ld	b,-3 (ix)
   5453 DD 7E 09      [19]  326 	ld	a, 9 (ix)
   5456 B7            [ 4]  327 	or	a, a
   5457 28 04         [12]  328 	jr	Z,00120$
   5459 3E 01         [ 7]  329 	ld	a, #0x01
   545B 18 02         [12]  330 	jr	00121$
   545D                     331 00120$:
   545D 3E FF         [ 7]  332 	ld	a, #0xff
   545F                     333 00121$:
   545F 02            [ 7]  334 	ld	(bc), a
   5460 18 20         [12]  335 	jr	00112$
   5462                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   5462 DD 6E F8      [19]  338 	ld	l,-8 (ix)
   5465 DD 66 F9      [19]  339 	ld	h,-7 (ix)
   5468 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   546A DD 6E F6      [19]  342 	ld	l,-10 (ix)
   546D DD 66 F7      [19]  343 	ld	h,-9 (ix)
   5470 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   5472 DD 6E F4      [19]  346 	ld	l,-12 (ix)
   5475 DD 66 F5      [19]  347 	ld	h,-11 (ix)
   5478 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   547A DD 6E FE      [19]  350 	ld	l,-2 (ix)
   547D DD 66 FF      [19]  351 	ld	h,-1 (ix)
   5480 36 64         [10]  352 	ld	(hl), #0x64
   5482                     353 00112$:
   5482 DD F9         [10]  354 	ld	sp, ix
   5484 DD E1         [14]  355 	pop	ix
   5486 C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   5487                     361 _enemyupdate::
   5487 DD E5         [15]  362 	push	ix
   5489 DD 21 00 00   [14]  363 	ld	ix,#0
   548D DD 39         [15]  364 	add	ix,sp
   548F 21 F6 FF      [10]  365 	ld	hl, #-10
   5492 39            [11]  366 	add	hl, sp
   5493 F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   5494 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   5497 DD B6 04      [19]  370 	or	a,4 (ix)
   549A CA 8E 56      [10]  371 	jp	Z,00121$
   549D DD 7E 04      [19]  372 	ld	a, 4 (ix)
   54A0 DD 77 FE      [19]  373 	ld	-2 (ix), a
   54A3 DD 7E 05      [19]  374 	ld	a, 5 (ix)
   54A6 DD 77 FF      [19]  375 	ld	-1 (ix), a
   54A9 DD 6E FE      [19]  376 	ld	l,-2 (ix)
   54AC DD 66 FF      [19]  377 	ld	h,-1 (ix)
   54AF 11 06 00      [10]  378 	ld	de, #0x0006
   54B2 19            [11]  379 	add	hl, de
   54B3 7E            [ 7]  380 	ld	a, (hl)
   54B4 B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   54B5 CA 8E 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   54B8 DD 6E FE      [19]  385 	ld	l,-2 (ix)
   54BB DD 66 FF      [19]  386 	ld	h,-1 (ix)
   54BE 11 09 00      [10]  387 	ld	de, #0x0009
   54C1 19            [11]  388 	add	hl, de
   54C2 7E            [ 7]  389 	ld	a, (hl)
   54C3 DD 77 FD      [19]  390 	ld	-3 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   54C6 DD 6E FE      [19]  392 	ld	l,-2 (ix)
   54C9 DD 66 FF      [19]  393 	ld	h,-1 (ix)
   54CC 4E            [ 7]  394 	ld	c, (hl)
   54CD DD 7E FE      [19]  395 	ld	a, -2 (ix)
   54D0 C6 02         [ 7]  396 	add	a, #0x02
   54D2 DD 77 FB      [19]  397 	ld	-5 (ix), a
   54D5 DD 7E FF      [19]  398 	ld	a, -1 (ix)
   54D8 CE 00         [ 7]  399 	adc	a, #0x00
   54DA DD 77 FC      [19]  400 	ld	-4 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   54DD DD 7E FE      [19]  402 	ld	a, -2 (ix)
   54E0 C6 01         [ 7]  403 	add	a, #0x01
   54E2 DD 77 F9      [19]  404 	ld	-7 (ix), a
   54E5 DD 7E FF      [19]  405 	ld	a, -1 (ix)
   54E8 CE 00         [ 7]  406 	adc	a, #0x00
   54EA DD 77 FA      [19]  407 	ld	-6 (ix), a
   54ED DD 5E FE      [19]  408 	ld	e,-2 (ix)
   54F0 DD 56 FF      [19]  409 	ld	d,-1 (ix)
   54F3 13            [ 6]  410 	inc	de
   54F4 13            [ 6]  411 	inc	de
   54F5 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   54F6 06 00         [ 7]  414 	ld	b, #0x00
   54F8 DD 6E FB      [19]  415 	ld	l,-5 (ix)
   54FB DD 66 FC      [19]  416 	ld	h,-4 (ix)
   54FE 7E            [ 7]  417 	ld	a, (hl)
   54FF DD 77 F8      [19]  418 	ld	-8 (ix), a
   5502 6F            [ 4]  419 	ld	l, a
   5503 DD 7E F8      [19]  420 	ld	a, -8 (ix)
   5506 17            [ 4]  421 	rla
   5507 9F            [ 4]  422 	sbc	a, a
   5508 67            [ 4]  423 	ld	h, a
   5509 09            [11]  424 	add	hl,bc
   550A 4D            [ 4]  425 	ld	c, l
   550B 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   550C DD 7E FD      [19]  428 	ld	a, -3 (ix)
   550F D6 02         [ 7]  429 	sub	a, #0x02
   5511 C2 BA 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5514 DD 6E F9      [19]  433 	ld	l,-7 (ix)
   5517 DD 66 FA      [19]  434 	ld	h,-6 (ix)
   551A 6E            [ 7]  435 	ld	l, (hl)
   551B DD 75 F6      [19]  436 	ld	-10 (ix), l
   551E DD 36 F7 00   [19]  437 	ld	-9 (ix), #0x00
   5522 1A            [ 7]  438 	ld	a, (de)
   5523 6F            [ 4]  439 	ld	l, a
   5524 17            [ 4]  440 	rla
   5525 9F            [ 4]  441 	sbc	a, a
   5526 67            [ 4]  442 	ld	h, a
   5527 DD 7E F6      [19]  443 	ld	a, -10 (ix)
   552A 85            [ 4]  444 	add	a, l
   552B DD 77 F6      [19]  445 	ld	-10 (ix), a
   552E DD 7E F7      [19]  446 	ld	a, -9 (ix)
   5531 8C            [ 4]  447 	adc	a, h
   5532 DD 77 F7      [19]  448 	ld	-9 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   5535 79            [ 4]  450 	ld	a, c
   5536 D6 08         [ 7]  451 	sub	a, #0x08
   5538 78            [ 4]  452 	ld	a, b
   5539 17            [ 4]  453 	rla
   553A 3F            [ 4]  454 	ccf
   553B 1F            [ 4]  455 	rra
   553C DE 80         [ 7]  456 	sbc	a, #0x80
   553E 38 0E         [12]  457 	jr	C,00104$
   5540 3E 48         [ 7]  458 	ld	a, #0x48
   5542 B9            [ 4]  459 	cp	a, c
   5543 3E 00         [ 7]  460 	ld	a, #0x00
   5545 98            [ 4]  461 	sbc	a, b
   5546 E2 4B 55      [10]  462 	jp	PO, 00161$
   5549 EE 80         [ 7]  463 	xor	a, #0x80
   554B                     464 00161$:
   554B F2 69 55      [10]  465 	jp	P, 00105$
   554E                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   554E AF            [ 4]  468 	xor	a, a
   554F DD 96 F8      [19]  469 	sub	a, -8 (ix)
   5552 4F            [ 4]  470 	ld	c, a
   5553 DD 6E FB      [19]  471 	ld	l,-5 (ix)
   5556 DD 66 FC      [19]  472 	ld	h,-4 (ix)
   5559 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   555A DD 6E FE      [19]  475 	ld	l,-2 (ix)
   555D DD 66 FF      [19]  476 	ld	h,-1 (ix)
   5560 6E            [ 7]  477 	ld	l, (hl)
   5561 26 00         [ 7]  478 	ld	h, #0x00
   5563 79            [ 4]  479 	ld	a, c
   5564 17            [ 4]  480 	rla
   5565 9F            [ 4]  481 	sbc	a, a
   5566 47            [ 4]  482 	ld	b, a
   5567 09            [11]  483 	add	hl,bc
   5568 4D            [ 4]  484 	ld	c, l
   5569                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   5569 DD 7E F6      [19]  487 	ld	a, -10 (ix)
   556C D6 38         [ 7]  488 	sub	a, #0x38
   556E DD 7E F7      [19]  489 	ld	a, -9 (ix)
   5571 17            [ 4]  490 	rla
   5572 3F            [ 4]  491 	ccf
   5573 1F            [ 4]  492 	rra
   5574 DE 80         [ 7]  493 	sbc	a, #0x80
   5576 38 12         [12]  494 	jr	C,00107$
   5578 3E 78         [ 7]  495 	ld	a, #0x78
   557A DD BE F6      [19]  496 	cp	a, -10 (ix)
   557D 3E 00         [ 7]  497 	ld	a, #0x00
   557F DD 9E F7      [19]  498 	sbc	a, -9 (ix)
   5582 E2 87 55      [10]  499 	jp	PO, 00162$
   5585 EE 80         [ 7]  500 	xor	a, #0x80
   5587                     501 00162$:
   5587 F2 A6 55      [10]  502 	jp	P, 00108$
   558A                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   558A 1A            [ 7]  505 	ld	a, (de)
   558B 6F            [ 4]  506 	ld	l, a
   558C AF            [ 4]  507 	xor	a, a
   558D 95            [ 4]  508 	sub	a, l
   558E DD 77 F8      [19]  509 	ld	-8 (ix), a
   5591 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5592 DD 6E F9      [19]  512 	ld	l,-7 (ix)
   5595 DD 66 FA      [19]  513 	ld	h,-6 (ix)
   5598 5E            [ 7]  514 	ld	e, (hl)
   5599 16 00         [ 7]  515 	ld	d, #0x00
   559B DD 6E F8      [19]  516 	ld	l, -8 (ix)
   559E DD 7E F8      [19]  517 	ld	a, -8 (ix)
   55A1 17            [ 4]  518 	rla
   55A2 9F            [ 4]  519 	sbc	a, a
   55A3 67            [ 4]  520 	ld	h, a
   55A4 19            [11]  521 	add	hl,de
   55A5 E3            [19]  522 	ex	(sp), hl
   55A6                     523 00108$:
                            524 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   55A6 DD 6E FE      [19]  525 	ld	l,-2 (ix)
   55A9 DD 66 FF      [19]  526 	ld	h,-1 (ix)
   55AC 71            [ 7]  527 	ld	(hl), c
                            528 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   55AD DD 4E F6      [19]  529 	ld	c, -10 (ix)
   55B0 DD 6E F9      [19]  530 	ld	l,-7 (ix)
   55B3 DD 66 FA      [19]  531 	ld	h,-6 (ix)
   55B6 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:84: return;
   55B7 C3 8E 56      [10]  534 	jp	00121$
   55BA                     535 00111$:
                            536 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            537 ;src/entities/enemy.c:88: if (nextx < 2) {
   55BA 79            [ 4]  538 	ld	a, c
   55BB D6 02         [ 7]  539 	sub	a, #0x02
   55BD 78            [ 4]  540 	ld	a, b
   55BE 17            [ 4]  541 	rla
   55BF 3F            [ 4]  542 	ccf
   55C0 1F            [ 4]  543 	rra
   55C1 DE 80         [ 7]  544 	sbc	a, #0x80
   55C3 30 0B         [12]  545 	jr	NC,00113$
                            546 ;src/entities/enemy.c:89: nextx = 2;
   55C5 01 02 00      [10]  547 	ld	bc, #0x0002
                            548 ;src/entities/enemy.c:90: enemy->vx = 1;
   55C8 DD 6E FB      [19]  549 	ld	l,-5 (ix)
   55CB DD 66 FC      [19]  550 	ld	h,-4 (ix)
   55CE 36 01         [10]  551 	ld	(hl), #0x01
   55D0                     552 00113$:
                            553 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   55D0 DD 6E FE      [19]  554 	ld	l,-2 (ix)
   55D3 DD 66 FF      [19]  555 	ld	h,-1 (ix)
   55D6 23            [ 6]  556 	inc	hl
   55D7 23            [ 6]  557 	inc	hl
   55D8 23            [ 6]  558 	inc	hl
   55D9 23            [ 6]  559 	inc	hl
   55DA 6E            [ 7]  560 	ld	l, (hl)
   55DB 26 00         [ 7]  561 	ld	h, #0x00
   55DD 3E 50         [ 7]  562 	ld	a, #0x50
   55DF 95            [ 4]  563 	sub	a, l
   55E0 6F            [ 4]  564 	ld	l, a
   55E1 3E 00         [ 7]  565 	ld	a, #0x00
   55E3 9C            [ 4]  566 	sbc	a, h
   55E4 67            [ 4]  567 	ld	h, a
                            568 ;src/entities/enemy.c:94: if (nextx > maxx) {
   55E5 7D            [ 4]  569 	ld	a, l
   55E6 91            [ 4]  570 	sub	a, c
   55E7 7C            [ 4]  571 	ld	a, h
   55E8 98            [ 4]  572 	sbc	a, b
   55E9 E2 EE 55      [10]  573 	jp	PO, 00163$
   55EC EE 80         [ 7]  574 	xor	a, #0x80
   55EE                     575 00163$:
   55EE F2 FA 55      [10]  576 	jp	P, 00115$
                            577 ;src/entities/enemy.c:95: nextx = maxx;
   55F1 4D            [ 4]  578 	ld	c, l
                            579 ;src/entities/enemy.c:96: enemy->vx = -1;
   55F2 DD 6E FB      [19]  580 	ld	l,-5 (ix)
   55F5 DD 66 FC      [19]  581 	ld	h,-4 (ix)
   55F8 36 FF         [10]  582 	ld	(hl), #0xff
   55FA                     583 00115$:
                            584 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   55FA DD 6E FE      [19]  585 	ld	l,-2 (ix)
   55FD DD 66 FF      [19]  586 	ld	h,-1 (ix)
   5600 71            [ 7]  587 	ld	(hl), c
                            588 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   5601 1A            [ 7]  589 	ld	a, (de)
   5602 4F            [ 4]  590 	ld	c, a
   5603 0C            [ 4]  591 	inc	c
   5604 79            [ 4]  592 	ld	a, c
   5605 12            [ 7]  593 	ld	(de), a
                            594 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   5606 3E 03         [ 7]  595 	ld	a, #0x03
   5608 91            [ 4]  596 	sub	a, c
   5609 E2 0E 56      [10]  597 	jp	PO, 00164$
   560C EE 80         [ 7]  598 	xor	a, #0x80
   560E                     599 00164$:
   560E F2 14 56      [10]  600 	jp	P, 00117$
   5611 3E 03         [ 7]  601 	ld	a, #0x03
   5613 12            [ 7]  602 	ld	(de), a
   5614                     603 00117$:
                            604 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   5614 DD 6E F9      [19]  605 	ld	l,-7 (ix)
   5617 DD 66 FA      [19]  606 	ld	h,-6 (ix)
   561A 4E            [ 7]  607 	ld	c, (hl)
   561B 06 00         [ 7]  608 	ld	b, #0x00
   561D 1A            [ 7]  609 	ld	a, (de)
   561E 6F            [ 4]  610 	ld	l, a
   561F 17            [ 4]  611 	rla
   5620 9F            [ 4]  612 	sbc	a, a
   5621 67            [ 4]  613 	ld	h, a
   5622 09            [11]  614 	add	hl, bc
   5623 E5            [11]  615 	push	hl
   5624 FD E1         [14]  616 	pop	iy
                            617 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5626 DD 7E FE      [19]  618 	ld	a, -2 (ix)
   5629 C6 05         [ 7]  619 	add	a, #0x05
   562B DD 77 F6      [19]  620 	ld	-10 (ix), a
   562E DD 7E FF      [19]  621 	ld	a, -1 (ix)
   5631 CE 00         [ 7]  622 	adc	a, #0x00
   5633 DD 77 F7      [19]  623 	ld	-9 (ix), a
   5636 E1            [10]  624 	pop	hl
   5637 E5            [11]  625 	push	hl
   5638 7E            [ 7]  626 	ld	a, (hl)
   5639 DD 6E FE      [19]  627 	ld	l,-2 (ix)
   563C DD 66 FF      [19]  628 	ld	h,-1 (ix)
   563F 4E            [ 7]  629 	ld	c, (hl)
   5640 06 00         [ 7]  630 	ld	b, #0x00
   5642 D5            [11]  631 	push	de
   5643 F5            [11]  632 	push	af
   5644 33            [ 6]  633 	inc	sp
   5645 FD E5         [15]  634 	push	iy
   5647 C5            [11]  635 	push	bc
   5648 CD 2D 4C      [17]  636 	call	_collision_clamp_y_at
   564B F1            [10]  637 	pop	af
   564C F1            [10]  638 	pop	af
   564D 33            [ 6]  639 	inc	sp
   564E 4D            [ 4]  640 	ld	c, l
   564F D1            [10]  641 	pop	de
                            642 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   5650 DD 6E F9      [19]  643 	ld	l,-7 (ix)
   5653 DD 66 FA      [19]  644 	ld	h,-6 (ix)
   5656 71            [ 7]  645 	ld	(hl), c
                            646 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5657 E1            [10]  647 	pop	hl
   5658 E5            [11]  648 	push	hl
   5659 7E            [ 7]  649 	ld	a, (hl)
   565A 06 00         [ 7]  650 	ld	b, #0x00
   565C DD 6E FE      [19]  651 	ld	l,-2 (ix)
   565F DD 66 FF      [19]  652 	ld	h,-1 (ix)
   5662 6E            [ 7]  653 	ld	l, (hl)
   5663 DD 75 F6      [19]  654 	ld	-10 (ix), l
   5666 DD 36 F7 00   [19]  655 	ld	-9 (ix), #0x00
   566A D5            [11]  656 	push	de
   566B F5            [11]  657 	push	af
   566C 33            [ 6]  658 	inc	sp
   566D C5            [11]  659 	push	bc
   566E DD 6E F6      [19]  660 	ld	l,-10 (ix)
   5671 DD 66 F7      [19]  661 	ld	h,-9 (ix)
   5674 E5            [11]  662 	push	hl
   5675 CD AE 4B      [17]  663 	call	_collision_is_on_ground_at
   5678 F1            [10]  664 	pop	af
   5679 F1            [10]  665 	pop	af
   567A 33            [ 6]  666 	inc	sp
   567B D1            [10]  667 	pop	de
   567C 7D            [ 4]  668 	ld	a, l
   567D B7            [ 4]  669 	or	a, a
   567E 28 0E         [12]  670 	jr	Z,00121$
   5680 1A            [ 7]  671 	ld	a, (de)
   5681 4F            [ 4]  672 	ld	c, a
   5682 AF            [ 4]  673 	xor	a, a
   5683 91            [ 4]  674 	sub	a, c
   5684 E2 89 56      [10]  675 	jp	PO, 00165$
   5687 EE 80         [ 7]  676 	xor	a, #0x80
   5689                     677 00165$:
   5689 F2 8E 56      [10]  678 	jp	P, 00121$
                            679 ;src/entities/enemy.c:107: enemy->vy = 0;
   568C AF            [ 4]  680 	xor	a, a
   568D 12            [ 7]  681 	ld	(de), a
   568E                     682 00121$:
   568E DD F9         [10]  683 	ld	sp, ix
   5690 DD E1         [14]  684 	pop	ix
   5692 C9            [10]  685 	ret
                            686 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            687 ;	---------------------------------
                            688 ; Function enemyrender
                            689 ; ---------------------------------
   5693                     690 _enemyrender::
   5693 DD E5         [15]  691 	push	ix
   5695 DD 21 00 00   [14]  692 	ld	ix,#0
   5699 DD 39         [15]  693 	add	ix,sp
   569B F5            [11]  694 	push	af
                            695 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   569C DD 7E 05      [19]  696 	ld	a, 5 (ix)
   569F DD B6 04      [19]  697 	or	a,4 (ix)
   56A2 CA 20 57      [10]  698 	jp	Z,00113$
   56A5 DD 7E 04      [19]  699 	ld	a, 4 (ix)
   56A8 DD 77 FE      [19]  700 	ld	-2 (ix), a
   56AB DD 7E 05      [19]  701 	ld	a, 5 (ix)
   56AE DD 77 FF      [19]  702 	ld	-1 (ix), a
   56B1 E1            [10]  703 	pop	hl
   56B2 E5            [11]  704 	push	hl
   56B3 11 06 00      [10]  705 	ld	de, #0x0006
   56B6 19            [11]  706 	add	hl, de
   56B7 7E            [ 7]  707 	ld	a, (hl)
   56B8 B7            [ 4]  708 	or	a, a
                            709 ;src/entities/enemy.c:116: return;
   56B9 28 65         [12]  710 	jr	Z,00113$
                            711 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   56BB E1            [10]  712 	pop	hl
   56BC E5            [11]  713 	push	hl
   56BD 11 09 00      [10]  714 	ld	de, #0x0009
   56C0 19            [11]  715 	add	hl, de
   56C1 7E            [ 7]  716 	ld	a, (hl)
   56C2 FE 03         [ 7]  717 	cp	a, #0x03
   56C4 20 0A         [12]  718 	jr	NZ,00111$
   56C6 21 0C 0C      [10]  719 	ld	hl, #0x0c0c
   56C9 E5            [11]  720 	push	hl
   56CA CD B6 5D      [17]  721 	call	_cpct_px2byteM0
   56CD 4D            [ 4]  722 	ld	c, l
   56CE 18 23         [12]  723 	jr	00112$
   56D0                     724 00111$:
                            725 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   56D0 FE 02         [ 7]  726 	cp	a, #0x02
   56D2 20 0A         [12]  727 	jr	NZ,00108$
   56D4 21 0A 0A      [10]  728 	ld	hl, #0x0a0a
   56D7 E5            [11]  729 	push	hl
   56D8 CD B6 5D      [17]  730 	call	_cpct_px2byteM0
   56DB 4D            [ 4]  731 	ld	c, l
   56DC 18 15         [12]  732 	jr	00112$
   56DE                     733 00108$:
                            734 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   56DE 3D            [ 4]  735 	dec	a
   56DF 20 0A         [12]  736 	jr	NZ,00105$
   56E1 21 0E 0E      [10]  737 	ld	hl, #0x0e0e
   56E4 E5            [11]  738 	push	hl
   56E5 CD B6 5D      [17]  739 	call	_cpct_px2byteM0
   56E8 4D            [ 4]  740 	ld	c, l
   56E9 18 08         [12]  741 	jr	00112$
   56EB                     742 00105$:
                            743 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   56EB 21 04 04      [10]  744 	ld	hl, #0x0404
   56EE E5            [11]  745 	push	hl
   56EF CD B6 5D      [17]  746 	call	_cpct_px2byteM0
   56F2 4D            [ 4]  747 	ld	c, l
   56F3                     748 00112$:
                            749 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   56F3 E1            [10]  750 	pop	hl
   56F4 E5            [11]  751 	push	hl
   56F5 23            [ 6]  752 	inc	hl
   56F6 46            [ 7]  753 	ld	b, (hl)
   56F7 E1            [10]  754 	pop	hl
   56F8 E5            [11]  755 	push	hl
   56F9 56            [ 7]  756 	ld	d, (hl)
   56FA C5            [11]  757 	push	bc
   56FB 4A            [ 4]  758 	ld	c, d
   56FC C5            [11]  759 	push	bc
   56FD 21 00 C0      [10]  760 	ld	hl, #0xc000
   5700 E5            [11]  761 	push	hl
   5701 CD A9 5E      [17]  762 	call	_cpct_getScreenPtr
   5704 EB            [ 4]  763 	ex	de,hl
   5705 C1            [10]  764 	pop	bc
                            765 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   5706 E1            [10]  766 	pop	hl
   5707 E5            [11]  767 	push	hl
   5708 23            [ 6]  768 	inc	hl
   5709 23            [ 6]  769 	inc	hl
   570A 23            [ 6]  770 	inc	hl
   570B 23            [ 6]  771 	inc	hl
   570C 23            [ 6]  772 	inc	hl
   570D 46            [ 7]  773 	ld	b, (hl)
   570E E1            [10]  774 	pop	hl
   570F E5            [11]  775 	push	hl
   5710 23            [ 6]  776 	inc	hl
   5711 23            [ 6]  777 	inc	hl
   5712 23            [ 6]  778 	inc	hl
   5713 23            [ 6]  779 	inc	hl
   5714 7E            [ 7]  780 	ld	a, (hl)
   5715 C5            [11]  781 	push	bc
   5716 33            [ 6]  782 	inc	sp
   5717 47            [ 4]  783 	ld	b, a
   5718 C5            [11]  784 	push	bc
   5719 D5            [11]  785 	push	de
   571A CD F0 5D      [17]  786 	call	_cpct_drawSolidBox
   571D F1            [10]  787 	pop	af
   571E F1            [10]  788 	pop	af
   571F 33            [ 6]  789 	inc	sp
   5720                     790 00113$:
   5720 DD F9         [10]  791 	ld	sp, ix
   5722 DD E1         [14]  792 	pop	ix
   5724 C9            [10]  793 	ret
                            794 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            795 ;	---------------------------------
                            796 ; Function enemydamage
                            797 ; ---------------------------------
   5725                     798 _enemydamage::
   5725 DD E5         [15]  799 	push	ix
   5727 DD 21 00 00   [14]  800 	ld	ix,#0
   572B DD 39         [15]  801 	add	ix,sp
                            802 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   572D DD 7E 05      [19]  803 	ld	a, 5 (ix)
   5730 DD B6 04      [19]  804 	or	a,4 (ix)
   5733 28 0F         [12]  805 	jr	Z,00101$
   5735 DD 4E 04      [19]  806 	ld	c,4 (ix)
   5738 DD 46 05      [19]  807 	ld	b,5 (ix)
   573B 21 06 00      [10]  808 	ld	hl, #0x0006
   573E 09            [11]  809 	add	hl,bc
   573F EB            [ 4]  810 	ex	de,hl
   5740 1A            [ 7]  811 	ld	a, (de)
   5741 B7            [ 4]  812 	or	a, a
   5742 20 04         [12]  813 	jr	NZ,00102$
   5744                     814 00101$:
                            815 ;src/entities/enemy.c:130: return 0;
   5744 2E 00         [ 7]  816 	ld	l, #0x00
   5746 18 1A         [12]  817 	jr	00106$
   5748                     818 00102$:
                            819 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   5748 21 07 00      [10]  820 	ld	hl, #0x0007
   574B 09            [11]  821 	add	hl, bc
   574C 4E            [ 7]  822 	ld	c, (hl)
   574D DD 7E 06      [19]  823 	ld	a, 6 (ix)
   5750 91            [ 4]  824 	sub	a, c
   5751 38 08         [12]  825 	jr	C,00105$
                            826 ;src/entities/enemy.c:134: enemy->health = 0;
   5753 36 00         [10]  827 	ld	(hl), #0x00
                            828 ;src/entities/enemy.c:135: enemy->active = 0;
   5755 AF            [ 4]  829 	xor	a, a
   5756 12            [ 7]  830 	ld	(de), a
                            831 ;src/entities/enemy.c:136: return 1;
   5757 2E 01         [ 7]  832 	ld	l, #0x01
   5759 18 07         [12]  833 	jr	00106$
   575B                     834 00105$:
                            835 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   575B 79            [ 4]  836 	ld	a, c
   575C DD 96 06      [19]  837 	sub	a, 6 (ix)
   575F 77            [ 7]  838 	ld	(hl), a
                            839 ;src/entities/enemy.c:140: return 0;
   5760 2E 00         [ 7]  840 	ld	l, #0x00
   5762                     841 00106$:
   5762 DD E1         [14]  842 	pop	ix
   5764 C9            [10]  843 	ret
                            844 	.area _CODE
                            845 	.area _INITIALIZER
                            846 	.area _CABS (ABS)
