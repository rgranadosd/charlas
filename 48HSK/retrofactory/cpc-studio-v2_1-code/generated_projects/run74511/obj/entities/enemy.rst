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
   51E6                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   51E6 21 03 00      [10]   58 	ld	hl, #2+1
   51E9 39            [11]   59 	add	hl, sp
   51EA 7E            [ 7]   60 	ld	a, (hl)
   51EB 2B            [ 6]   61 	dec	hl
   51EC B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   51ED C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   51EE D1            [10]   66 	pop	de
   51EF C1            [10]   67 	pop	bc
   51F0 C5            [11]   68 	push	bc
   51F1 D5            [11]   69 	push	de
   51F2 AF            [ 4]   70 	xor	a, a
   51F3 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   51F4 59            [ 4]   73 	ld	e, c
   51F5 50            [ 4]   74 	ld	d, b
   51F6 13            [ 6]   75 	inc	de
   51F7 AF            [ 4]   76 	xor	a, a
   51F8 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   51F9 59            [ 4]   79 	ld	e, c
   51FA 50            [ 4]   80 	ld	d, b
   51FB 13            [ 6]   81 	inc	de
   51FC 13            [ 6]   82 	inc	de
   51FD AF            [ 4]   83 	xor	a, a
   51FE 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   51FF 59            [ 4]   86 	ld	e, c
   5200 50            [ 4]   87 	ld	d, b
   5201 13            [ 6]   88 	inc	de
   5202 13            [ 6]   89 	inc	de
   5203 13            [ 6]   90 	inc	de
   5204 AF            [ 4]   91 	xor	a, a
   5205 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   5206 21 04 00      [10]   94 	ld	hl, #0x0004
   5209 09            [11]   95 	add	hl, bc
   520A 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   520C 21 05 00      [10]   98 	ld	hl, #0x0005
   520F 09            [11]   99 	add	hl, bc
   5210 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5212 21 06 00      [10]  102 	ld	hl, #0x0006
   5215 09            [11]  103 	add	hl, bc
   5216 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   5218 21 07 00      [10]  106 	ld	hl, #0x0007
   521B 09            [11]  107 	add	hl, bc
   521C 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   521E 21 08 00      [10]  110 	ld	hl, #0x0008
   5221 09            [11]  111 	add	hl, bc
   5222 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   5224 21 09 00      [10]  114 	ld	hl, #0x0009
   5227 09            [11]  115 	add	hl, bc
   5228 36 00         [10]  116 	ld	(hl), #0x00
   522A C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   522B                     122 _enemyspawn::
   522B DD E5         [15]  123 	push	ix
   522D DD 21 00 00   [14]  124 	ld	ix,#0
   5231 DD 39         [15]  125 	add	ix,sp
   5233 21 F1 FF      [10]  126 	ld	hl, #-15
   5236 39            [11]  127 	add	hl, sp
   5237 F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   5238 DD 7E 05      [19]  130 	ld	a, 5 (ix)
   523B DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   523E CA E6 53      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   5241 DD 7E 04      [19]  135 	ld	a, 4 (ix)
   5244 DD 77 FC      [19]  136 	ld	-4 (ix), a
   5247 DD 7E 05      [19]  137 	ld	a, 5 (ix)
   524A DD 77 FD      [19]  138 	ld	-3 (ix), a
   524D DD 6E FC      [19]  139 	ld	l,-4 (ix)
   5250 DD 66 FD      [19]  140 	ld	h,-3 (ix)
   5253 DD 7E 06      [19]  141 	ld	a, 6 (ix)
   5256 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   5257 DD 4E FC      [19]  144 	ld	c,-4 (ix)
   525A DD 46 FD      [19]  145 	ld	b,-3 (ix)
   525D 03            [ 6]  146 	inc	bc
   525E DD 7E 07      [19]  147 	ld	a, 7 (ix)
   5261 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   5262 DD 7E FC      [19]  150 	ld	a, -4 (ix)
   5265 C6 02         [ 7]  151 	add	a, #0x02
   5267 DD 77 FE      [19]  152 	ld	-2 (ix), a
   526A DD 7E FD      [19]  153 	ld	a, -3 (ix)
   526D CE 00         [ 7]  154 	adc	a, #0x00
   526F DD 77 FF      [19]  155 	ld	-1 (ix), a
   5272 DD 7E 09      [19]  156 	ld	a, 9 (ix)
   5275 B7            [ 4]  157 	or	a, a
   5276 28 04         [12]  158 	jr	Z,00114$
   5278 0E 01         [ 7]  159 	ld	c, #0x01
   527A 18 02         [12]  160 	jr	00115$
   527C                     161 00114$:
   527C 0E FF         [ 7]  162 	ld	c, #0xff
   527E                     163 00115$:
   527E DD 6E FE      [19]  164 	ld	l,-2 (ix)
   5281 DD 66 FF      [19]  165 	ld	h,-1 (ix)
   5284 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   5285 DD 7E FC      [19]  168 	ld	a, -4 (ix)
   5288 C6 03         [ 7]  169 	add	a, #0x03
   528A DD 77 FA      [19]  170 	ld	-6 (ix), a
   528D DD 7E FD      [19]  171 	ld	a, -3 (ix)
   5290 CE 00         [ 7]  172 	adc	a, #0x00
   5292 DD 77 FB      [19]  173 	ld	-5 (ix), a
   5295 DD 6E FA      [19]  174 	ld	l,-6 (ix)
   5298 DD 66 FB      [19]  175 	ld	h,-5 (ix)
   529B 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   529D DD 7E FC      [19]  178 	ld	a, -4 (ix)
   52A0 C6 06         [ 7]  179 	add	a, #0x06
   52A2 DD 77 F1      [19]  180 	ld	-15 (ix), a
   52A5 DD 7E FD      [19]  181 	ld	a, -3 (ix)
   52A8 CE 00         [ 7]  182 	adc	a, #0x00
   52AA DD 77 F2      [19]  183 	ld	-14 (ix), a
   52AD E1            [10]  184 	pop	hl
   52AE E5            [11]  185 	push	hl
   52AF 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52B1 DD 7E FC      [19]  188 	ld	a, -4 (ix)
   52B4 C6 09         [ 7]  189 	add	a, #0x09
   52B6 DD 77 F1      [19]  190 	ld	-15 (ix), a
   52B9 DD 7E FD      [19]  191 	ld	a, -3 (ix)
   52BC CE 00         [ 7]  192 	adc	a, #0x00
   52BE DD 77 F2      [19]  193 	ld	-14 (ix), a
   52C1 E1            [10]  194 	pop	hl
   52C2 E5            [11]  195 	push	hl
   52C3 DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52C6 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52C7 DD 7E FC      [19]  199 	ld	a, -4 (ix)
   52CA C6 04         [ 7]  200 	add	a, #0x04
   52CC DD 77 F1      [19]  201 	ld	-15 (ix), a
   52CF DD 7E FD      [19]  202 	ld	a, -3 (ix)
   52D2 CE 00         [ 7]  203 	adc	a, #0x00
   52D4 DD 77 F2      [19]  204 	ld	-14 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52D7 DD 7E FC      [19]  206 	ld	a, -4 (ix)
   52DA C6 05         [ 7]  207 	add	a, #0x05
   52DC DD 77 F8      [19]  208 	ld	-8 (ix), a
   52DF DD 7E FD      [19]  209 	ld	a, -3 (ix)
   52E2 CE 00         [ 7]  210 	adc	a, #0x00
   52E4 DD 77 F9      [19]  211 	ld	-7 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   52E7 DD 7E FC      [19]  213 	ld	a, -4 (ix)
   52EA C6 07         [ 7]  214 	add	a, #0x07
   52EC DD 77 F3      [19]  215 	ld	-13 (ix), a
   52EF DD 7E FD      [19]  216 	ld	a, -3 (ix)
   52F2 CE 00         [ 7]  217 	adc	a, #0x00
   52F4 DD 77 F4      [19]  218 	ld	-12 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   52F7 DD 7E FC      [19]  220 	ld	a, -4 (ix)
   52FA C6 08         [ 7]  221 	add	a, #0x08
   52FC DD 77 FC      [19]  222 	ld	-4 (ix), a
   52FF DD 7E FD      [19]  223 	ld	a, -3 (ix)
   5302 CE 00         [ 7]  224 	adc	a, #0x00
   5304 DD 77 FD      [19]  225 	ld	-3 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   5307 DD 7E 08      [19]  227 	ld	a, 8 (ix)
   530A 3D            [ 4]  228 	dec	a
   530B 20 45         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   530D E1            [10]  231 	pop	hl
   530E E5            [11]  232 	push	hl
   530F 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   5311 DD 6E F8      [19]  235 	ld	l,-8 (ix)
   5314 DD 66 F9      [19]  236 	ld	h,-7 (ix)
   5317 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   5319 DD 6E F3      [19]  239 	ld	l,-13 (ix)
   531C DD 66 F4      [19]  240 	ld	h,-12 (ix)
   531F 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   5321 DD 6E FC      [19]  243 	ld	l,-4 (ix)
   5324 DD 66 FD      [19]  244 	ld	h,-3 (ix)
   5327 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   5329 DD 7E FE      [19]  247 	ld	a, -2 (ix)
   532C DD 77 F6      [19]  248 	ld	-10 (ix), a
   532F DD 7E FF      [19]  249 	ld	a, -1 (ix)
   5332 DD 77 F7      [19]  250 	ld	-9 (ix), a
   5335 DD 7E 09      [19]  251 	ld	a, 9 (ix)
   5338 B7            [ 4]  252 	or	a, a
   5339 28 06         [12]  253 	jr	Z,00116$
   533B DD 36 F5 02   [19]  254 	ld	-11 (ix), #0x02
   533F 18 04         [12]  255 	jr	00117$
   5341                     256 00116$:
   5341 DD 36 F5 FE   [19]  257 	ld	-11 (ix), #0xfe
   5345                     258 00117$:
   5345 DD 6E F6      [19]  259 	ld	l,-10 (ix)
   5348 DD 66 F7      [19]  260 	ld	h,-9 (ix)
   534B DD 7E F5      [19]  261 	ld	a, -11 (ix)
   534E 77            [ 7]  262 	ld	(hl), a
   534F C3 E6 53      [10]  263 	jp	00112$
   5352                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   5352 DD 7E 08      [19]  266 	ld	a, 8 (ix)
   5355 D6 02         [ 7]  267 	sub	a, #0x02
   5357 20 39         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   5359 E1            [10]  270 	pop	hl
   535A E5            [11]  271 	push	hl
   535B 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   535D DD 6E F8      [19]  274 	ld	l,-8 (ix)
   5360 DD 66 F9      [19]  275 	ld	h,-7 (ix)
   5363 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   5365 DD 6E F3      [19]  278 	ld	l,-13 (ix)
   5368 DD 66 F4      [19]  279 	ld	h,-12 (ix)
   536B 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   536D DD 6E FC      [19]  282 	ld	l,-4 (ix)
   5370 DD 66 FD      [19]  283 	ld	h,-3 (ix)
   5373 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5375 DD 4E FA      [19]  286 	ld	c,-6 (ix)
   5378 DD 46 FB      [19]  287 	ld	b,-5 (ix)
   537B DD 7E 09      [19]  288 	ld	a, 9 (ix)
   537E B7            [ 4]  289 	or	a, a
   537F 28 04         [12]  290 	jr	Z,00118$
   5381 3E 01         [ 7]  291 	ld	a, #0x01
   5383 18 02         [12]  292 	jr	00119$
   5385                     293 00118$:
   5385 3E FF         [ 7]  294 	ld	a, #0xff
   5387                     295 00119$:
   5387 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   5388 DD 6E FE      [19]  298 	ld	l,-2 (ix)
   538B DD 66 FF      [19]  299 	ld	h,-1 (ix)
   538E 36 01         [10]  300 	ld	(hl), #0x01
   5390 18 54         [12]  301 	jr	00112$
   5392                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   5392 DD 7E 08      [19]  304 	ld	a, 8 (ix)
   5395 D6 03         [ 7]  305 	sub	a, #0x03
   5397 20 31         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   5399 E1            [10]  308 	pop	hl
   539A E5            [11]  309 	push	hl
   539B 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   539D DD 6E F8      [19]  312 	ld	l,-8 (ix)
   53A0 DD 66 F9      [19]  313 	ld	h,-7 (ix)
   53A3 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53A5 DD 6E F3      [19]  316 	ld	l,-13 (ix)
   53A8 DD 66 F4      [19]  317 	ld	h,-12 (ix)
   53AB 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53AD DD 6E FC      [19]  320 	ld	l,-4 (ix)
   53B0 DD 66 FD      [19]  321 	ld	h,-3 (ix)
   53B3 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53B5 DD 4E FE      [19]  324 	ld	c,-2 (ix)
   53B8 DD 46 FF      [19]  325 	ld	b,-1 (ix)
   53BB DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53BE B7            [ 4]  327 	or	a, a
   53BF 28 04         [12]  328 	jr	Z,00120$
   53C1 3E 01         [ 7]  329 	ld	a, #0x01
   53C3 18 02         [12]  330 	jr	00121$
   53C5                     331 00120$:
   53C5 3E FF         [ 7]  332 	ld	a, #0xff
   53C7                     333 00121$:
   53C7 02            [ 7]  334 	ld	(bc), a
   53C8 18 1C         [12]  335 	jr	00112$
   53CA                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53CA E1            [10]  338 	pop	hl
   53CB E5            [11]  339 	push	hl
   53CC 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   53CE DD 6E F8      [19]  342 	ld	l,-8 (ix)
   53D1 DD 66 F9      [19]  343 	ld	h,-7 (ix)
   53D4 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   53D6 DD 6E F3      [19]  346 	ld	l,-13 (ix)
   53D9 DD 66 F4      [19]  347 	ld	h,-12 (ix)
   53DC 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   53DE DD 6E FC      [19]  350 	ld	l,-4 (ix)
   53E1 DD 66 FD      [19]  351 	ld	h,-3 (ix)
   53E4 36 64         [10]  352 	ld	(hl), #0x64
   53E6                     353 00112$:
   53E6 DD F9         [10]  354 	ld	sp, ix
   53E8 DD E1         [14]  355 	pop	ix
   53EA C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   53EB                     361 _enemyupdate::
   53EB DD E5         [15]  362 	push	ix
   53ED DD 21 00 00   [14]  363 	ld	ix,#0
   53F1 DD 39         [15]  364 	add	ix,sp
   53F3 21 F6 FF      [10]  365 	ld	hl, #-10
   53F6 39            [11]  366 	add	hl, sp
   53F7 F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   53F8 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   53FB DD B6 04      [19]  370 	or	a,4 (ix)
   53FE CA F2 55      [10]  371 	jp	Z,00121$
   5401 DD 7E 04      [19]  372 	ld	a, 4 (ix)
   5404 DD 77 FB      [19]  373 	ld	-5 (ix), a
   5407 DD 7E 05      [19]  374 	ld	a, 5 (ix)
   540A DD 77 FC      [19]  375 	ld	-4 (ix), a
   540D DD 6E FB      [19]  376 	ld	l,-5 (ix)
   5410 DD 66 FC      [19]  377 	ld	h,-4 (ix)
   5413 11 06 00      [10]  378 	ld	de, #0x0006
   5416 19            [11]  379 	add	hl, de
   5417 7E            [ 7]  380 	ld	a, (hl)
   5418 B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   5419 CA F2 55      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   541C DD 6E FB      [19]  385 	ld	l,-5 (ix)
   541F DD 66 FC      [19]  386 	ld	h,-4 (ix)
   5422 11 09 00      [10]  387 	ld	de, #0x0009
   5425 19            [11]  388 	add	hl, de
   5426 7E            [ 7]  389 	ld	a, (hl)
   5427 DD 77 FF      [19]  390 	ld	-1 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   542A DD 6E FB      [19]  392 	ld	l,-5 (ix)
   542D DD 66 FC      [19]  393 	ld	h,-4 (ix)
   5430 4E            [ 7]  394 	ld	c, (hl)
   5431 DD 7E FB      [19]  395 	ld	a, -5 (ix)
   5434 C6 02         [ 7]  396 	add	a, #0x02
   5436 DD 77 FD      [19]  397 	ld	-3 (ix), a
   5439 DD 7E FC      [19]  398 	ld	a, -4 (ix)
   543C CE 00         [ 7]  399 	adc	a, #0x00
   543E DD 77 FE      [19]  400 	ld	-2 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5441 DD 7E FB      [19]  402 	ld	a, -5 (ix)
   5444 C6 01         [ 7]  403 	add	a, #0x01
   5446 DD 77 F9      [19]  404 	ld	-7 (ix), a
   5449 DD 7E FC      [19]  405 	ld	a, -4 (ix)
   544C CE 00         [ 7]  406 	adc	a, #0x00
   544E DD 77 FA      [19]  407 	ld	-6 (ix), a
   5451 DD 5E FB      [19]  408 	ld	e,-5 (ix)
   5454 DD 56 FC      [19]  409 	ld	d,-4 (ix)
   5457 13            [ 6]  410 	inc	de
   5458 13            [ 6]  411 	inc	de
   5459 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   545A 06 00         [ 7]  414 	ld	b, #0x00
   545C DD 6E FD      [19]  415 	ld	l,-3 (ix)
   545F DD 66 FE      [19]  416 	ld	h,-2 (ix)
   5462 7E            [ 7]  417 	ld	a, (hl)
   5463 DD 77 F8      [19]  418 	ld	-8 (ix), a
   5466 6F            [ 4]  419 	ld	l, a
   5467 DD 7E F8      [19]  420 	ld	a, -8 (ix)
   546A 17            [ 4]  421 	rla
   546B 9F            [ 4]  422 	sbc	a, a
   546C 67            [ 4]  423 	ld	h, a
   546D 09            [11]  424 	add	hl,bc
   546E 4D            [ 4]  425 	ld	c, l
   546F 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5470 DD 7E FF      [19]  428 	ld	a, -1 (ix)
   5473 D6 02         [ 7]  429 	sub	a, #0x02
   5475 C2 1E 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5478 DD 6E F9      [19]  433 	ld	l,-7 (ix)
   547B DD 66 FA      [19]  434 	ld	h,-6 (ix)
   547E 6E            [ 7]  435 	ld	l, (hl)
   547F DD 75 F6      [19]  436 	ld	-10 (ix), l
   5482 DD 36 F7 00   [19]  437 	ld	-9 (ix), #0x00
   5486 1A            [ 7]  438 	ld	a, (de)
   5487 6F            [ 4]  439 	ld	l, a
   5488 17            [ 4]  440 	rla
   5489 9F            [ 4]  441 	sbc	a, a
   548A 67            [ 4]  442 	ld	h, a
   548B DD 7E F6      [19]  443 	ld	a, -10 (ix)
   548E 85            [ 4]  444 	add	a, l
   548F DD 77 F6      [19]  445 	ld	-10 (ix), a
   5492 DD 7E F7      [19]  446 	ld	a, -9 (ix)
   5495 8C            [ 4]  447 	adc	a, h
   5496 DD 77 F7      [19]  448 	ld	-9 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   5499 79            [ 4]  450 	ld	a, c
   549A D6 08         [ 7]  451 	sub	a, #0x08
   549C 78            [ 4]  452 	ld	a, b
   549D 17            [ 4]  453 	rla
   549E 3F            [ 4]  454 	ccf
   549F 1F            [ 4]  455 	rra
   54A0 DE 80         [ 7]  456 	sbc	a, #0x80
   54A2 38 0E         [12]  457 	jr	C,00104$
   54A4 3E 48         [ 7]  458 	ld	a, #0x48
   54A6 B9            [ 4]  459 	cp	a, c
   54A7 3E 00         [ 7]  460 	ld	a, #0x00
   54A9 98            [ 4]  461 	sbc	a, b
   54AA E2 AF 54      [10]  462 	jp	PO, 00161$
   54AD EE 80         [ 7]  463 	xor	a, #0x80
   54AF                     464 00161$:
   54AF F2 CD 54      [10]  465 	jp	P, 00105$
   54B2                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   54B2 AF            [ 4]  468 	xor	a, a
   54B3 DD 96 F8      [19]  469 	sub	a, -8 (ix)
   54B6 4F            [ 4]  470 	ld	c, a
   54B7 DD 6E FD      [19]  471 	ld	l,-3 (ix)
   54BA DD 66 FE      [19]  472 	ld	h,-2 (ix)
   54BD 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54BE DD 6E FB      [19]  475 	ld	l,-5 (ix)
   54C1 DD 66 FC      [19]  476 	ld	h,-4 (ix)
   54C4 6E            [ 7]  477 	ld	l, (hl)
   54C5 26 00         [ 7]  478 	ld	h, #0x00
   54C7 79            [ 4]  479 	ld	a, c
   54C8 17            [ 4]  480 	rla
   54C9 9F            [ 4]  481 	sbc	a, a
   54CA 47            [ 4]  482 	ld	b, a
   54CB 09            [11]  483 	add	hl,bc
   54CC 4D            [ 4]  484 	ld	c, l
   54CD                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   54CD DD 7E F6      [19]  487 	ld	a, -10 (ix)
   54D0 D6 38         [ 7]  488 	sub	a, #0x38
   54D2 DD 7E F7      [19]  489 	ld	a, -9 (ix)
   54D5 17            [ 4]  490 	rla
   54D6 3F            [ 4]  491 	ccf
   54D7 1F            [ 4]  492 	rra
   54D8 DE 80         [ 7]  493 	sbc	a, #0x80
   54DA 38 12         [12]  494 	jr	C,00107$
   54DC 3E 78         [ 7]  495 	ld	a, #0x78
   54DE DD BE F6      [19]  496 	cp	a, -10 (ix)
   54E1 3E 00         [ 7]  497 	ld	a, #0x00
   54E3 DD 9E F7      [19]  498 	sbc	a, -9 (ix)
   54E6 E2 EB 54      [10]  499 	jp	PO, 00162$
   54E9 EE 80         [ 7]  500 	xor	a, #0x80
   54EB                     501 00162$:
   54EB F2 0A 55      [10]  502 	jp	P, 00108$
   54EE                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   54EE 1A            [ 7]  505 	ld	a, (de)
   54EF 6F            [ 4]  506 	ld	l, a
   54F0 AF            [ 4]  507 	xor	a, a
   54F1 95            [ 4]  508 	sub	a, l
   54F2 DD 77 F8      [19]  509 	ld	-8 (ix), a
   54F5 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   54F6 DD 6E F9      [19]  512 	ld	l,-7 (ix)
   54F9 DD 66 FA      [19]  513 	ld	h,-6 (ix)
   54FC 5E            [ 7]  514 	ld	e, (hl)
   54FD 16 00         [ 7]  515 	ld	d, #0x00
   54FF DD 6E F8      [19]  516 	ld	l, -8 (ix)
   5502 DD 7E F8      [19]  517 	ld	a, -8 (ix)
   5505 17            [ 4]  518 	rla
   5506 9F            [ 4]  519 	sbc	a, a
   5507 67            [ 4]  520 	ld	h, a
   5508 19            [11]  521 	add	hl,de
   5509 E3            [19]  522 	ex	(sp), hl
   550A                     523 00108$:
                            524 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   550A DD 6E FB      [19]  525 	ld	l,-5 (ix)
   550D DD 66 FC      [19]  526 	ld	h,-4 (ix)
   5510 71            [ 7]  527 	ld	(hl), c
                            528 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   5511 DD 4E F6      [19]  529 	ld	c, -10 (ix)
   5514 DD 6E F9      [19]  530 	ld	l,-7 (ix)
   5517 DD 66 FA      [19]  531 	ld	h,-6 (ix)
   551A 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:84: return;
   551B C3 F2 55      [10]  534 	jp	00121$
   551E                     535 00111$:
                            536 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            537 ;src/entities/enemy.c:88: if (nextx < 2) {
   551E 79            [ 4]  538 	ld	a, c
   551F D6 02         [ 7]  539 	sub	a, #0x02
   5521 78            [ 4]  540 	ld	a, b
   5522 17            [ 4]  541 	rla
   5523 3F            [ 4]  542 	ccf
   5524 1F            [ 4]  543 	rra
   5525 DE 80         [ 7]  544 	sbc	a, #0x80
   5527 30 0B         [12]  545 	jr	NC,00113$
                            546 ;src/entities/enemy.c:89: nextx = 2;
   5529 01 02 00      [10]  547 	ld	bc, #0x0002
                            548 ;src/entities/enemy.c:90: enemy->vx = 1;
   552C DD 6E FD      [19]  549 	ld	l,-3 (ix)
   552F DD 66 FE      [19]  550 	ld	h,-2 (ix)
   5532 36 01         [10]  551 	ld	(hl), #0x01
   5534                     552 00113$:
                            553 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   5534 DD 6E FB      [19]  554 	ld	l,-5 (ix)
   5537 DD 66 FC      [19]  555 	ld	h,-4 (ix)
   553A 23            [ 6]  556 	inc	hl
   553B 23            [ 6]  557 	inc	hl
   553C 23            [ 6]  558 	inc	hl
   553D 23            [ 6]  559 	inc	hl
   553E 6E            [ 7]  560 	ld	l, (hl)
   553F 26 00         [ 7]  561 	ld	h, #0x00
   5541 3E 50         [ 7]  562 	ld	a, #0x50
   5543 95            [ 4]  563 	sub	a, l
   5544 6F            [ 4]  564 	ld	l, a
   5545 3E 00         [ 7]  565 	ld	a, #0x00
   5547 9C            [ 4]  566 	sbc	a, h
   5548 67            [ 4]  567 	ld	h, a
                            568 ;src/entities/enemy.c:94: if (nextx > maxx) {
   5549 7D            [ 4]  569 	ld	a, l
   554A 91            [ 4]  570 	sub	a, c
   554B 7C            [ 4]  571 	ld	a, h
   554C 98            [ 4]  572 	sbc	a, b
   554D E2 52 55      [10]  573 	jp	PO, 00163$
   5550 EE 80         [ 7]  574 	xor	a, #0x80
   5552                     575 00163$:
   5552 F2 5E 55      [10]  576 	jp	P, 00115$
                            577 ;src/entities/enemy.c:95: nextx = maxx;
   5555 4D            [ 4]  578 	ld	c, l
                            579 ;src/entities/enemy.c:96: enemy->vx = -1;
   5556 DD 6E FD      [19]  580 	ld	l,-3 (ix)
   5559 DD 66 FE      [19]  581 	ld	h,-2 (ix)
   555C 36 FF         [10]  582 	ld	(hl), #0xff
   555E                     583 00115$:
                            584 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   555E DD 6E FB      [19]  585 	ld	l,-5 (ix)
   5561 DD 66 FC      [19]  586 	ld	h,-4 (ix)
   5564 71            [ 7]  587 	ld	(hl), c
                            588 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   5565 1A            [ 7]  589 	ld	a, (de)
   5566 4F            [ 4]  590 	ld	c, a
   5567 0C            [ 4]  591 	inc	c
   5568 79            [ 4]  592 	ld	a, c
   5569 12            [ 7]  593 	ld	(de), a
                            594 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   556A 3E 03         [ 7]  595 	ld	a, #0x03
   556C 91            [ 4]  596 	sub	a, c
   556D E2 72 55      [10]  597 	jp	PO, 00164$
   5570 EE 80         [ 7]  598 	xor	a, #0x80
   5572                     599 00164$:
   5572 F2 78 55      [10]  600 	jp	P, 00117$
   5575 3E 03         [ 7]  601 	ld	a, #0x03
   5577 12            [ 7]  602 	ld	(de), a
   5578                     603 00117$:
                            604 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   5578 DD 6E F9      [19]  605 	ld	l,-7 (ix)
   557B DD 66 FA      [19]  606 	ld	h,-6 (ix)
   557E 4E            [ 7]  607 	ld	c, (hl)
   557F 06 00         [ 7]  608 	ld	b, #0x00
   5581 1A            [ 7]  609 	ld	a, (de)
   5582 6F            [ 4]  610 	ld	l, a
   5583 17            [ 4]  611 	rla
   5584 9F            [ 4]  612 	sbc	a, a
   5585 67            [ 4]  613 	ld	h, a
   5586 09            [11]  614 	add	hl, bc
   5587 E5            [11]  615 	push	hl
   5588 FD E1         [14]  616 	pop	iy
                            617 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   558A DD 7E FB      [19]  618 	ld	a, -5 (ix)
   558D C6 05         [ 7]  619 	add	a, #0x05
   558F DD 77 F6      [19]  620 	ld	-10 (ix), a
   5592 DD 7E FC      [19]  621 	ld	a, -4 (ix)
   5595 CE 00         [ 7]  622 	adc	a, #0x00
   5597 DD 77 F7      [19]  623 	ld	-9 (ix), a
   559A E1            [10]  624 	pop	hl
   559B E5            [11]  625 	push	hl
   559C 7E            [ 7]  626 	ld	a, (hl)
   559D DD 6E FB      [19]  627 	ld	l,-5 (ix)
   55A0 DD 66 FC      [19]  628 	ld	h,-4 (ix)
   55A3 4E            [ 7]  629 	ld	c, (hl)
   55A4 06 00         [ 7]  630 	ld	b, #0x00
   55A6 D5            [11]  631 	push	de
   55A7 F5            [11]  632 	push	af
   55A8 33            [ 6]  633 	inc	sp
   55A9 FD E5         [15]  634 	push	iy
   55AB C5            [11]  635 	push	bc
   55AC CD 29 4C      [17]  636 	call	_collision_clamp_y_at
   55AF F1            [10]  637 	pop	af
   55B0 F1            [10]  638 	pop	af
   55B1 33            [ 6]  639 	inc	sp
   55B2 4D            [ 4]  640 	ld	c, l
   55B3 D1            [10]  641 	pop	de
                            642 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55B4 DD 6E F9      [19]  643 	ld	l,-7 (ix)
   55B7 DD 66 FA      [19]  644 	ld	h,-6 (ix)
   55BA 71            [ 7]  645 	ld	(hl), c
                            646 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55BB E1            [10]  647 	pop	hl
   55BC E5            [11]  648 	push	hl
   55BD 7E            [ 7]  649 	ld	a, (hl)
   55BE 06 00         [ 7]  650 	ld	b, #0x00
   55C0 DD 6E FB      [19]  651 	ld	l,-5 (ix)
   55C3 DD 66 FC      [19]  652 	ld	h,-4 (ix)
   55C6 6E            [ 7]  653 	ld	l, (hl)
   55C7 DD 75 F6      [19]  654 	ld	-10 (ix), l
   55CA DD 36 F7 00   [19]  655 	ld	-9 (ix), #0x00
   55CE D5            [11]  656 	push	de
   55CF F5            [11]  657 	push	af
   55D0 33            [ 6]  658 	inc	sp
   55D1 C5            [11]  659 	push	bc
   55D2 DD 6E F6      [19]  660 	ld	l,-10 (ix)
   55D5 DD 66 F7      [19]  661 	ld	h,-9 (ix)
   55D8 E5            [11]  662 	push	hl
   55D9 CD AA 4B      [17]  663 	call	_collision_is_on_ground_at
   55DC F1            [10]  664 	pop	af
   55DD F1            [10]  665 	pop	af
   55DE 33            [ 6]  666 	inc	sp
   55DF D1            [10]  667 	pop	de
   55E0 7D            [ 4]  668 	ld	a, l
   55E1 B7            [ 4]  669 	or	a, a
   55E2 28 0E         [12]  670 	jr	Z,00121$
   55E4 1A            [ 7]  671 	ld	a, (de)
   55E5 4F            [ 4]  672 	ld	c, a
   55E6 AF            [ 4]  673 	xor	a, a
   55E7 91            [ 4]  674 	sub	a, c
   55E8 E2 ED 55      [10]  675 	jp	PO, 00165$
   55EB EE 80         [ 7]  676 	xor	a, #0x80
   55ED                     677 00165$:
   55ED F2 F2 55      [10]  678 	jp	P, 00121$
                            679 ;src/entities/enemy.c:107: enemy->vy = 0;
   55F0 AF            [ 4]  680 	xor	a, a
   55F1 12            [ 7]  681 	ld	(de), a
   55F2                     682 00121$:
   55F2 DD F9         [10]  683 	ld	sp, ix
   55F4 DD E1         [14]  684 	pop	ix
   55F6 C9            [10]  685 	ret
                            686 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            687 ;	---------------------------------
                            688 ; Function enemyrender
                            689 ; ---------------------------------
   55F7                     690 _enemyrender::
   55F7 DD E5         [15]  691 	push	ix
   55F9 DD 21 00 00   [14]  692 	ld	ix,#0
   55FD DD 39         [15]  693 	add	ix,sp
   55FF F5            [11]  694 	push	af
                            695 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5600 DD 7E 05      [19]  696 	ld	a, 5 (ix)
   5603 DD B6 04      [19]  697 	or	a,4 (ix)
   5606 CA 84 56      [10]  698 	jp	Z,00113$
   5609 DD 7E 04      [19]  699 	ld	a, 4 (ix)
   560C DD 77 FE      [19]  700 	ld	-2 (ix), a
   560F DD 7E 05      [19]  701 	ld	a, 5 (ix)
   5612 DD 77 FF      [19]  702 	ld	-1 (ix), a
   5615 E1            [10]  703 	pop	hl
   5616 E5            [11]  704 	push	hl
   5617 11 06 00      [10]  705 	ld	de, #0x0006
   561A 19            [11]  706 	add	hl, de
   561B 7E            [ 7]  707 	ld	a, (hl)
   561C B7            [ 4]  708 	or	a, a
                            709 ;src/entities/enemy.c:116: return;
   561D 28 65         [12]  710 	jr	Z,00113$
                            711 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   561F E1            [10]  712 	pop	hl
   5620 E5            [11]  713 	push	hl
   5621 11 09 00      [10]  714 	ld	de, #0x0009
   5624 19            [11]  715 	add	hl, de
   5625 7E            [ 7]  716 	ld	a, (hl)
   5626 FE 03         [ 7]  717 	cp	a, #0x03
   5628 20 0A         [12]  718 	jr	NZ,00111$
   562A 21 0C 0C      [10]  719 	ld	hl, #0x0c0c
   562D E5            [11]  720 	push	hl
   562E CD 46 5D      [17]  721 	call	_cpct_px2byteM0
   5631 4D            [ 4]  722 	ld	c, l
   5632 18 23         [12]  723 	jr	00112$
   5634                     724 00111$:
                            725 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   5634 FE 02         [ 7]  726 	cp	a, #0x02
   5636 20 0A         [12]  727 	jr	NZ,00108$
   5638 21 0A 0A      [10]  728 	ld	hl, #0x0a0a
   563B E5            [11]  729 	push	hl
   563C CD 46 5D      [17]  730 	call	_cpct_px2byteM0
   563F 4D            [ 4]  731 	ld	c, l
   5640 18 15         [12]  732 	jr	00112$
   5642                     733 00108$:
                            734 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   5642 3D            [ 4]  735 	dec	a
   5643 20 0A         [12]  736 	jr	NZ,00105$
   5645 21 0E 0E      [10]  737 	ld	hl, #0x0e0e
   5648 E5            [11]  738 	push	hl
   5649 CD 46 5D      [17]  739 	call	_cpct_px2byteM0
   564C 4D            [ 4]  740 	ld	c, l
   564D 18 08         [12]  741 	jr	00112$
   564F                     742 00105$:
                            743 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   564F 21 04 04      [10]  744 	ld	hl, #0x0404
   5652 E5            [11]  745 	push	hl
   5653 CD 46 5D      [17]  746 	call	_cpct_px2byteM0
   5656 4D            [ 4]  747 	ld	c, l
   5657                     748 00112$:
                            749 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5657 E1            [10]  750 	pop	hl
   5658 E5            [11]  751 	push	hl
   5659 23            [ 6]  752 	inc	hl
   565A 46            [ 7]  753 	ld	b, (hl)
   565B E1            [10]  754 	pop	hl
   565C E5            [11]  755 	push	hl
   565D 56            [ 7]  756 	ld	d, (hl)
   565E C5            [11]  757 	push	bc
   565F 4A            [ 4]  758 	ld	c, d
   5660 C5            [11]  759 	push	bc
   5661 21 00 C0      [10]  760 	ld	hl, #0xc000
   5664 E5            [11]  761 	push	hl
   5665 CD 39 5E      [17]  762 	call	_cpct_getScreenPtr
   5668 EB            [ 4]  763 	ex	de,hl
   5669 C1            [10]  764 	pop	bc
                            765 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   566A E1            [10]  766 	pop	hl
   566B E5            [11]  767 	push	hl
   566C 23            [ 6]  768 	inc	hl
   566D 23            [ 6]  769 	inc	hl
   566E 23            [ 6]  770 	inc	hl
   566F 23            [ 6]  771 	inc	hl
   5670 23            [ 6]  772 	inc	hl
   5671 46            [ 7]  773 	ld	b, (hl)
   5672 E1            [10]  774 	pop	hl
   5673 E5            [11]  775 	push	hl
   5674 23            [ 6]  776 	inc	hl
   5675 23            [ 6]  777 	inc	hl
   5676 23            [ 6]  778 	inc	hl
   5677 23            [ 6]  779 	inc	hl
   5678 7E            [ 7]  780 	ld	a, (hl)
   5679 C5            [11]  781 	push	bc
   567A 33            [ 6]  782 	inc	sp
   567B 47            [ 4]  783 	ld	b, a
   567C C5            [11]  784 	push	bc
   567D D5            [11]  785 	push	de
   567E CD 80 5D      [17]  786 	call	_cpct_drawSolidBox
   5681 F1            [10]  787 	pop	af
   5682 F1            [10]  788 	pop	af
   5683 33            [ 6]  789 	inc	sp
   5684                     790 00113$:
   5684 DD F9         [10]  791 	ld	sp, ix
   5686 DD E1         [14]  792 	pop	ix
   5688 C9            [10]  793 	ret
                            794 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            795 ;	---------------------------------
                            796 ; Function enemydamage
                            797 ; ---------------------------------
   5689                     798 _enemydamage::
   5689 DD E5         [15]  799 	push	ix
   568B DD 21 00 00   [14]  800 	ld	ix,#0
   568F DD 39         [15]  801 	add	ix,sp
                            802 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   5691 DD 7E 05      [19]  803 	ld	a, 5 (ix)
   5694 DD B6 04      [19]  804 	or	a,4 (ix)
   5697 28 0F         [12]  805 	jr	Z,00101$
   5699 DD 4E 04      [19]  806 	ld	c,4 (ix)
   569C DD 46 05      [19]  807 	ld	b,5 (ix)
   569F 21 06 00      [10]  808 	ld	hl, #0x0006
   56A2 09            [11]  809 	add	hl,bc
   56A3 EB            [ 4]  810 	ex	de,hl
   56A4 1A            [ 7]  811 	ld	a, (de)
   56A5 B7            [ 4]  812 	or	a, a
   56A6 20 04         [12]  813 	jr	NZ,00102$
   56A8                     814 00101$:
                            815 ;src/entities/enemy.c:130: return 0;
   56A8 2E 00         [ 7]  816 	ld	l, #0x00
   56AA 18 1A         [12]  817 	jr	00106$
   56AC                     818 00102$:
                            819 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56AC 21 07 00      [10]  820 	ld	hl, #0x0007
   56AF 09            [11]  821 	add	hl, bc
   56B0 4E            [ 7]  822 	ld	c, (hl)
   56B1 DD 7E 06      [19]  823 	ld	a, 6 (ix)
   56B4 91            [ 4]  824 	sub	a, c
   56B5 38 08         [12]  825 	jr	C,00105$
                            826 ;src/entities/enemy.c:134: enemy->health = 0;
   56B7 36 00         [10]  827 	ld	(hl), #0x00
                            828 ;src/entities/enemy.c:135: enemy->active = 0;
   56B9 AF            [ 4]  829 	xor	a, a
   56BA 12            [ 7]  830 	ld	(de), a
                            831 ;src/entities/enemy.c:136: return 1;
   56BB 2E 01         [ 7]  832 	ld	l, #0x01
   56BD 18 07         [12]  833 	jr	00106$
   56BF                     834 00105$:
                            835 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   56BF 79            [ 4]  836 	ld	a, c
   56C0 DD 96 06      [19]  837 	sub	a, 6 (ix)
   56C3 77            [ 7]  838 	ld	(hl), a
                            839 ;src/entities/enemy.c:140: return 0;
   56C4 2E 00         [ 7]  840 	ld	l, #0x00
   56C6                     841 00106$:
   56C6 DD E1         [14]  842 	pop	ix
   56C8 C9            [10]  843 	ret
                            844 	.area _CODE
                            845 	.area _INITIALIZER
                            846 	.area _CABS (ABS)
