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
   5206                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   5206 21 03 00      [10]   58 	ld	hl, #2+1
   5209 39            [11]   59 	add	hl, sp
   520A 7E            [ 7]   60 	ld	a, (hl)
   520B 2B            [ 6]   61 	dec	hl
   520C B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   520D C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   520E D1            [10]   66 	pop	de
   520F C1            [10]   67 	pop	bc
   5210 C5            [11]   68 	push	bc
   5211 D5            [11]   69 	push	de
   5212 AF            [ 4]   70 	xor	a, a
   5213 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   5214 59            [ 4]   73 	ld	e, c
   5215 50            [ 4]   74 	ld	d, b
   5216 13            [ 6]   75 	inc	de
   5217 AF            [ 4]   76 	xor	a, a
   5218 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   5219 59            [ 4]   79 	ld	e, c
   521A 50            [ 4]   80 	ld	d, b
   521B 13            [ 6]   81 	inc	de
   521C 13            [ 6]   82 	inc	de
   521D AF            [ 4]   83 	xor	a, a
   521E 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   521F 59            [ 4]   86 	ld	e, c
   5220 50            [ 4]   87 	ld	d, b
   5221 13            [ 6]   88 	inc	de
   5222 13            [ 6]   89 	inc	de
   5223 13            [ 6]   90 	inc	de
   5224 AF            [ 4]   91 	xor	a, a
   5225 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   5226 21 04 00      [10]   94 	ld	hl, #0x0004
   5229 09            [11]   95 	add	hl, bc
   522A 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   522C 21 05 00      [10]   98 	ld	hl, #0x0005
   522F 09            [11]   99 	add	hl, bc
   5230 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5232 21 06 00      [10]  102 	ld	hl, #0x0006
   5235 09            [11]  103 	add	hl, bc
   5236 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   5238 21 07 00      [10]  106 	ld	hl, #0x0007
   523B 09            [11]  107 	add	hl, bc
   523C 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   523E 21 08 00      [10]  110 	ld	hl, #0x0008
   5241 09            [11]  111 	add	hl, bc
   5242 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   5244 21 09 00      [10]  114 	ld	hl, #0x0009
   5247 09            [11]  115 	add	hl, bc
   5248 36 00         [10]  116 	ld	(hl), #0x00
   524A C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   524B                     122 _enemyspawn::
   524B DD E5         [15]  123 	push	ix
   524D DD 21 00 00   [14]  124 	ld	ix,#0
   5251 DD 39         [15]  125 	add	ix,sp
   5253 21 F1 FF      [10]  126 	ld	hl, #-15
   5256 39            [11]  127 	add	hl, sp
   5257 F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   5258 DD 7E 05      [19]  130 	ld	a, 5 (ix)
   525B DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   525E CA 1E 54      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   5261 DD 7E 04      [19]  135 	ld	a, 4 (ix)
   5264 DD 77 FE      [19]  136 	ld	-2 (ix), a
   5267 DD 7E 05      [19]  137 	ld	a, 5 (ix)
   526A DD 77 FF      [19]  138 	ld	-1 (ix), a
   526D DD 6E FE      [19]  139 	ld	l,-2 (ix)
   5270 DD 66 FF      [19]  140 	ld	h,-1 (ix)
   5273 DD 7E 06      [19]  141 	ld	a, 6 (ix)
   5276 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   5277 DD 4E FE      [19]  144 	ld	c,-2 (ix)
   527A DD 46 FF      [19]  145 	ld	b,-1 (ix)
   527D 03            [ 6]  146 	inc	bc
   527E DD 7E 07      [19]  147 	ld	a, 7 (ix)
   5281 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   5282 DD 7E FE      [19]  150 	ld	a, -2 (ix)
   5285 C6 02         [ 7]  151 	add	a, #0x02
   5287 DD 77 FC      [19]  152 	ld	-4 (ix), a
   528A DD 7E FF      [19]  153 	ld	a, -1 (ix)
   528D CE 00         [ 7]  154 	adc	a, #0x00
   528F DD 77 FD      [19]  155 	ld	-3 (ix), a
   5292 DD 7E 09      [19]  156 	ld	a, 9 (ix)
   5295 B7            [ 4]  157 	or	a, a
   5296 28 04         [12]  158 	jr	Z,00114$
   5298 0E 01         [ 7]  159 	ld	c, #0x01
   529A 18 02         [12]  160 	jr	00115$
   529C                     161 00114$:
   529C 0E FF         [ 7]  162 	ld	c, #0xff
   529E                     163 00115$:
   529E DD 6E FC      [19]  164 	ld	l,-4 (ix)
   52A1 DD 66 FD      [19]  165 	ld	h,-3 (ix)
   52A4 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   52A5 DD 7E FE      [19]  168 	ld	a, -2 (ix)
   52A8 C6 03         [ 7]  169 	add	a, #0x03
   52AA DD 77 FA      [19]  170 	ld	-6 (ix), a
   52AD DD 7E FF      [19]  171 	ld	a, -1 (ix)
   52B0 CE 00         [ 7]  172 	adc	a, #0x00
   52B2 DD 77 FB      [19]  173 	ld	-5 (ix), a
   52B5 DD 6E FA      [19]  174 	ld	l,-6 (ix)
   52B8 DD 66 FB      [19]  175 	ld	h,-5 (ix)
   52BB 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   52BD DD 7E FE      [19]  178 	ld	a, -2 (ix)
   52C0 C6 06         [ 7]  179 	add	a, #0x06
   52C2 DD 77 F8      [19]  180 	ld	-8 (ix), a
   52C5 DD 7E FF      [19]  181 	ld	a, -1 (ix)
   52C8 CE 00         [ 7]  182 	adc	a, #0x00
   52CA DD 77 F9      [19]  183 	ld	-7 (ix), a
   52CD DD 6E F8      [19]  184 	ld	l,-8 (ix)
   52D0 DD 66 F9      [19]  185 	ld	h,-7 (ix)
   52D3 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52D5 DD 7E FE      [19]  188 	ld	a, -2 (ix)
   52D8 C6 09         [ 7]  189 	add	a, #0x09
   52DA DD 77 F8      [19]  190 	ld	-8 (ix), a
   52DD DD 7E FF      [19]  191 	ld	a, -1 (ix)
   52E0 CE 00         [ 7]  192 	adc	a, #0x00
   52E2 DD 77 F9      [19]  193 	ld	-7 (ix), a
   52E5 DD 6E F8      [19]  194 	ld	l,-8 (ix)
   52E8 DD 66 F9      [19]  195 	ld	h,-7 (ix)
   52EB DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52EE 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52EF DD 7E FE      [19]  199 	ld	a, -2 (ix)
   52F2 C6 04         [ 7]  200 	add	a, #0x04
   52F4 DD 77 F8      [19]  201 	ld	-8 (ix), a
   52F7 DD 7E FF      [19]  202 	ld	a, -1 (ix)
   52FA CE 00         [ 7]  203 	adc	a, #0x00
   52FC DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52FF DD 7E FE      [19]  206 	ld	a, -2 (ix)
   5302 C6 05         [ 7]  207 	add	a, #0x05
   5304 DD 77 F6      [19]  208 	ld	-10 (ix), a
   5307 DD 7E FF      [19]  209 	ld	a, -1 (ix)
   530A CE 00         [ 7]  210 	adc	a, #0x00
   530C DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   530F DD 7E FE      [19]  213 	ld	a, -2 (ix)
   5312 C6 07         [ 7]  214 	add	a, #0x07
   5314 DD 77 F4      [19]  215 	ld	-12 (ix), a
   5317 DD 7E FF      [19]  216 	ld	a, -1 (ix)
   531A CE 00         [ 7]  217 	adc	a, #0x00
   531C DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   531F DD 7E FE      [19]  220 	ld	a, -2 (ix)
   5322 C6 08         [ 7]  221 	add	a, #0x08
   5324 DD 77 FE      [19]  222 	ld	-2 (ix), a
   5327 DD 7E FF      [19]  223 	ld	a, -1 (ix)
   532A CE 00         [ 7]  224 	adc	a, #0x00
   532C DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   532F DD 7E 08      [19]  227 	ld	a, 8 (ix)
   5332 3D            [ 4]  228 	dec	a
   5333 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   5335 DD 6E F8      [19]  231 	ld	l,-8 (ix)
   5338 DD 66 F9      [19]  232 	ld	h,-7 (ix)
   533B 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   533D DD 6E F6      [19]  235 	ld	l,-10 (ix)
   5340 DD 66 F7      [19]  236 	ld	h,-9 (ix)
   5343 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   5345 DD 6E F4      [19]  239 	ld	l,-12 (ix)
   5348 DD 66 F5      [19]  240 	ld	h,-11 (ix)
   534B 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   534D DD 6E FE      [19]  243 	ld	l,-2 (ix)
   5350 DD 66 FF      [19]  244 	ld	h,-1 (ix)
   5353 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   5355 DD 7E FC      [19]  247 	ld	a, -4 (ix)
   5358 DD 77 F2      [19]  248 	ld	-14 (ix), a
   535B DD 7E FD      [19]  249 	ld	a, -3 (ix)
   535E DD 77 F3      [19]  250 	ld	-13 (ix), a
   5361 DD 7E 09      [19]  251 	ld	a, 9 (ix)
   5364 B7            [ 4]  252 	or	a, a
   5365 28 06         [12]  253 	jr	Z,00116$
   5367 DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   536B 18 04         [12]  255 	jr	00117$
   536D                     256 00116$:
   536D DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   5371                     258 00117$:
   5371 DD 6E F2      [19]  259 	ld	l,-14 (ix)
   5374 DD 66 F3      [19]  260 	ld	h,-13 (ix)
   5377 DD 7E F1      [19]  261 	ld	a, -15 (ix)
   537A 77            [ 7]  262 	ld	(hl), a
   537B C3 1E 54      [10]  263 	jp	00112$
   537E                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   537E DD 7E 08      [19]  266 	ld	a, 8 (ix)
   5381 D6 02         [ 7]  267 	sub	a, #0x02
   5383 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   5385 DD 6E F8      [19]  270 	ld	l,-8 (ix)
   5388 DD 66 F9      [19]  271 	ld	h,-7 (ix)
   538B 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   538D DD 6E F6      [19]  274 	ld	l,-10 (ix)
   5390 DD 66 F7      [19]  275 	ld	h,-9 (ix)
   5393 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   5395 DD 6E F4      [19]  278 	ld	l,-12 (ix)
   5398 DD 66 F5      [19]  279 	ld	h,-11 (ix)
   539B 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   539D DD 6E FE      [19]  282 	ld	l,-2 (ix)
   53A0 DD 66 FF      [19]  283 	ld	h,-1 (ix)
   53A3 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   53A5 DD 4E FA      [19]  286 	ld	c,-6 (ix)
   53A8 DD 46 FB      [19]  287 	ld	b,-5 (ix)
   53AB DD 7E 09      [19]  288 	ld	a, 9 (ix)
   53AE B7            [ 4]  289 	or	a, a
   53AF 28 04         [12]  290 	jr	Z,00118$
   53B1 3E 01         [ 7]  291 	ld	a, #0x01
   53B3 18 02         [12]  292 	jr	00119$
   53B5                     293 00118$:
   53B5 3E FF         [ 7]  294 	ld	a, #0xff
   53B7                     295 00119$:
   53B7 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   53B8 DD 6E FC      [19]  298 	ld	l,-4 (ix)
   53BB DD 66 FD      [19]  299 	ld	h,-3 (ix)
   53BE 36 01         [10]  300 	ld	(hl), #0x01
   53C0 18 5C         [12]  301 	jr	00112$
   53C2                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   53C2 DD 7E 08      [19]  304 	ld	a, 8 (ix)
   53C5 D6 03         [ 7]  305 	sub	a, #0x03
   53C7 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   53C9 DD 6E F8      [19]  308 	ld	l,-8 (ix)
   53CC DD 66 F9      [19]  309 	ld	h,-7 (ix)
   53CF 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   53D1 DD 6E F6      [19]  312 	ld	l,-10 (ix)
   53D4 DD 66 F7      [19]  313 	ld	h,-9 (ix)
   53D7 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53D9 DD 6E F4      [19]  316 	ld	l,-12 (ix)
   53DC DD 66 F5      [19]  317 	ld	h,-11 (ix)
   53DF 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53E1 DD 6E FE      [19]  320 	ld	l,-2 (ix)
   53E4 DD 66 FF      [19]  321 	ld	h,-1 (ix)
   53E7 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53E9 DD 4E FC      [19]  324 	ld	c,-4 (ix)
   53EC DD 46 FD      [19]  325 	ld	b,-3 (ix)
   53EF DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53F2 B7            [ 4]  327 	or	a, a
   53F3 28 04         [12]  328 	jr	Z,00120$
   53F5 3E 01         [ 7]  329 	ld	a, #0x01
   53F7 18 02         [12]  330 	jr	00121$
   53F9                     331 00120$:
   53F9 3E FF         [ 7]  332 	ld	a, #0xff
   53FB                     333 00121$:
   53FB 02            [ 7]  334 	ld	(bc), a
   53FC 18 20         [12]  335 	jr	00112$
   53FE                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53FE DD 6E F8      [19]  338 	ld	l,-8 (ix)
   5401 DD 66 F9      [19]  339 	ld	h,-7 (ix)
   5404 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   5406 DD 6E F6      [19]  342 	ld	l,-10 (ix)
   5409 DD 66 F7      [19]  343 	ld	h,-9 (ix)
   540C 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   540E DD 6E F4      [19]  346 	ld	l,-12 (ix)
   5411 DD 66 F5      [19]  347 	ld	h,-11 (ix)
   5414 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   5416 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   5419 DD 66 FF      [19]  351 	ld	h,-1 (ix)
   541C 36 64         [10]  352 	ld	(hl), #0x64
   541E                     353 00112$:
   541E DD F9         [10]  354 	ld	sp, ix
   5420 DD E1         [14]  355 	pop	ix
   5422 C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   5423                     361 _enemyupdate::
   5423 DD E5         [15]  362 	push	ix
   5425 DD 21 00 00   [14]  363 	ld	ix,#0
   5429 DD 39         [15]  364 	add	ix,sp
   542B 21 F6 FF      [10]  365 	ld	hl, #-10
   542E 39            [11]  366 	add	hl, sp
   542F F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   5430 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   5433 DD B6 04      [19]  370 	or	a,4 (ix)
   5436 CA 37 56      [10]  371 	jp	Z,00121$
   5439 DD 7E 04      [19]  372 	ld	a, 4 (ix)
   543C DD 77 FC      [19]  373 	ld	-4 (ix), a
   543F DD 7E 05      [19]  374 	ld	a, 5 (ix)
   5442 DD 77 FD      [19]  375 	ld	-3 (ix), a
   5445 DD 6E FC      [19]  376 	ld	l,-4 (ix)
   5448 DD 66 FD      [19]  377 	ld	h,-3 (ix)
   544B 11 06 00      [10]  378 	ld	de, #0x0006
   544E 19            [11]  379 	add	hl, de
   544F 7E            [ 7]  380 	ld	a, (hl)
   5450 B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   5451 CA 37 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5454 DD 6E FC      [19]  385 	ld	l,-4 (ix)
   5457 DD 66 FD      [19]  386 	ld	h,-3 (ix)
   545A 11 09 00      [10]  387 	ld	de, #0x0009
   545D 19            [11]  388 	add	hl, de
   545E 7E            [ 7]  389 	ld	a, (hl)
   545F DD 77 FB      [19]  390 	ld	-5 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5462 DD 6E FC      [19]  392 	ld	l,-4 (ix)
   5465 DD 66 FD      [19]  393 	ld	h,-3 (ix)
   5468 4E            [ 7]  394 	ld	c, (hl)
   5469 DD 7E FC      [19]  395 	ld	a, -4 (ix)
   546C C6 02         [ 7]  396 	add	a, #0x02
   546E DD 77 F9      [19]  397 	ld	-7 (ix), a
   5471 DD 7E FD      [19]  398 	ld	a, -3 (ix)
   5474 CE 00         [ 7]  399 	adc	a, #0x00
   5476 DD 77 FA      [19]  400 	ld	-6 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5479 DD 7E FC      [19]  402 	ld	a, -4 (ix)
   547C C6 01         [ 7]  403 	add	a, #0x01
   547E DD 77 F7      [19]  404 	ld	-9 (ix), a
   5481 DD 7E FD      [19]  405 	ld	a, -3 (ix)
   5484 CE 00         [ 7]  406 	adc	a, #0x00
   5486 DD 77 F8      [19]  407 	ld	-8 (ix), a
   5489 DD 5E FC      [19]  408 	ld	e,-4 (ix)
   548C DD 56 FD      [19]  409 	ld	d,-3 (ix)
   548F 13            [ 6]  410 	inc	de
   5490 13            [ 6]  411 	inc	de
   5491 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5492 06 00         [ 7]  414 	ld	b, #0x00
   5494 DD 6E F9      [19]  415 	ld	l,-7 (ix)
   5497 DD 66 FA      [19]  416 	ld	h,-6 (ix)
   549A 7E            [ 7]  417 	ld	a, (hl)
   549B DD 77 F6      [19]  418 	ld	-10 (ix), a
   549E 6F            [ 4]  419 	ld	l, a
   549F DD 7E F6      [19]  420 	ld	a, -10 (ix)
   54A2 17            [ 4]  421 	rla
   54A3 9F            [ 4]  422 	sbc	a, a
   54A4 67            [ 4]  423 	ld	h, a
   54A5 09            [11]  424 	add	hl,bc
   54A6 4D            [ 4]  425 	ld	c, l
   54A7 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   54A8 DD 7E FB      [19]  428 	ld	a, -5 (ix)
   54AB D6 02         [ 7]  429 	sub	a, #0x02
   54AD C2 5B 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   54B0 DD 6E F7      [19]  433 	ld	l,-9 (ix)
   54B3 DD 66 F8      [19]  434 	ld	h,-8 (ix)
   54B6 6E            [ 7]  435 	ld	l, (hl)
   54B7 DD 75 FE      [19]  436 	ld	-2 (ix), l
   54BA DD 36 FF 00   [19]  437 	ld	-1 (ix), #0x00
   54BE 1A            [ 7]  438 	ld	a, (de)
   54BF 6F            [ 4]  439 	ld	l, a
   54C0 17            [ 4]  440 	rla
   54C1 9F            [ 4]  441 	sbc	a, a
   54C2 67            [ 4]  442 	ld	h, a
   54C3 DD 7E FE      [19]  443 	ld	a, -2 (ix)
   54C6 85            [ 4]  444 	add	a, l
   54C7 DD 77 FE      [19]  445 	ld	-2 (ix), a
   54CA DD 7E FF      [19]  446 	ld	a, -1 (ix)
   54CD 8C            [ 4]  447 	adc	a, h
   54CE DD 77 FF      [19]  448 	ld	-1 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   54D1 79            [ 4]  450 	ld	a, c
   54D2 D6 08         [ 7]  451 	sub	a, #0x08
   54D4 78            [ 4]  452 	ld	a, b
   54D5 17            [ 4]  453 	rla
   54D6 3F            [ 4]  454 	ccf
   54D7 1F            [ 4]  455 	rra
   54D8 DE 80         [ 7]  456 	sbc	a, #0x80
   54DA 38 0E         [12]  457 	jr	C,00104$
   54DC 3E 48         [ 7]  458 	ld	a, #0x48
   54DE B9            [ 4]  459 	cp	a, c
   54DF 3E 00         [ 7]  460 	ld	a, #0x00
   54E1 98            [ 4]  461 	sbc	a, b
   54E2 E2 E7 54      [10]  462 	jp	PO, 00161$
   54E5 EE 80         [ 7]  463 	xor	a, #0x80
   54E7                     464 00161$:
   54E7 F2 05 55      [10]  465 	jp	P, 00105$
   54EA                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   54EA AF            [ 4]  468 	xor	a, a
   54EB DD 96 F6      [19]  469 	sub	a, -10 (ix)
   54EE 4F            [ 4]  470 	ld	c, a
   54EF DD 6E F9      [19]  471 	ld	l,-7 (ix)
   54F2 DD 66 FA      [19]  472 	ld	h,-6 (ix)
   54F5 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54F6 DD 6E FC      [19]  475 	ld	l,-4 (ix)
   54F9 DD 66 FD      [19]  476 	ld	h,-3 (ix)
   54FC 6E            [ 7]  477 	ld	l, (hl)
   54FD 26 00         [ 7]  478 	ld	h, #0x00
   54FF 79            [ 4]  479 	ld	a, c
   5500 17            [ 4]  480 	rla
   5501 9F            [ 4]  481 	sbc	a, a
   5502 47            [ 4]  482 	ld	b, a
   5503 09            [11]  483 	add	hl,bc
   5504 4D            [ 4]  484 	ld	c, l
   5505                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   5505 DD 7E FE      [19]  487 	ld	a, -2 (ix)
   5508 D6 38         [ 7]  488 	sub	a, #0x38
   550A DD 7E FF      [19]  489 	ld	a, -1 (ix)
   550D 17            [ 4]  490 	rla
   550E 3F            [ 4]  491 	ccf
   550F 1F            [ 4]  492 	rra
   5510 DE 80         [ 7]  493 	sbc	a, #0x80
   5512 38 12         [12]  494 	jr	C,00107$
   5514 3E 78         [ 7]  495 	ld	a, #0x78
   5516 DD BE FE      [19]  496 	cp	a, -2 (ix)
   5519 3E 00         [ 7]  497 	ld	a, #0x00
   551B DD 9E FF      [19]  498 	sbc	a, -1 (ix)
   551E E2 23 55      [10]  499 	jp	PO, 00162$
   5521 EE 80         [ 7]  500 	xor	a, #0x80
   5523                     501 00162$:
   5523 F2 47 55      [10]  502 	jp	P, 00108$
   5526                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5526 1A            [ 7]  505 	ld	a, (de)
   5527 6F            [ 4]  506 	ld	l, a
   5528 AF            [ 4]  507 	xor	a, a
   5529 95            [ 4]  508 	sub	a, l
   552A DD 77 F6      [19]  509 	ld	-10 (ix), a
   552D 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   552E DD 6E F7      [19]  512 	ld	l,-9 (ix)
   5531 DD 66 F8      [19]  513 	ld	h,-8 (ix)
   5534 5E            [ 7]  514 	ld	e, (hl)
   5535 16 00         [ 7]  515 	ld	d, #0x00
   5537 DD 6E F6      [19]  516 	ld	l, -10 (ix)
   553A DD 7E F6      [19]  517 	ld	a, -10 (ix)
   553D 17            [ 4]  518 	rla
   553E 9F            [ 4]  519 	sbc	a, a
   553F 67            [ 4]  520 	ld	h, a
   5540 19            [11]  521 	add	hl,de
   5541 DD 75 FE      [19]  522 	ld	-2 (ix), l
   5544 DD 74 FF      [19]  523 	ld	-1 (ix), h
   5547                     524 00108$:
                            525 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   5547 DD 6E FC      [19]  526 	ld	l,-4 (ix)
   554A DD 66 FD      [19]  527 	ld	h,-3 (ix)
   554D 71            [ 7]  528 	ld	(hl), c
                            529 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   554E DD 4E FE      [19]  530 	ld	c, -2 (ix)
   5551 DD 6E F7      [19]  531 	ld	l,-9 (ix)
   5554 DD 66 F8      [19]  532 	ld	h,-8 (ix)
   5557 71            [ 7]  533 	ld	(hl), c
                            534 ;src/entities/enemy.c:84: return;
   5558 C3 37 56      [10]  535 	jp	00121$
   555B                     536 00111$:
                            537 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            538 ;src/entities/enemy.c:88: if (nextx < 2) {
   555B 79            [ 4]  539 	ld	a, c
   555C D6 02         [ 7]  540 	sub	a, #0x02
   555E 78            [ 4]  541 	ld	a, b
   555F 17            [ 4]  542 	rla
   5560 3F            [ 4]  543 	ccf
   5561 1F            [ 4]  544 	rra
   5562 DE 80         [ 7]  545 	sbc	a, #0x80
   5564 30 0B         [12]  546 	jr	NC,00113$
                            547 ;src/entities/enemy.c:89: nextx = 2;
   5566 01 02 00      [10]  548 	ld	bc, #0x0002
                            549 ;src/entities/enemy.c:90: enemy->vx = 1;
   5569 DD 6E F9      [19]  550 	ld	l,-7 (ix)
   556C DD 66 FA      [19]  551 	ld	h,-6 (ix)
   556F 36 01         [10]  552 	ld	(hl), #0x01
   5571                     553 00113$:
                            554 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   5571 DD 6E FC      [19]  555 	ld	l,-4 (ix)
   5574 DD 66 FD      [19]  556 	ld	h,-3 (ix)
   5577 23            [ 6]  557 	inc	hl
   5578 23            [ 6]  558 	inc	hl
   5579 23            [ 6]  559 	inc	hl
   557A 23            [ 6]  560 	inc	hl
   557B 6E            [ 7]  561 	ld	l, (hl)
   557C 26 00         [ 7]  562 	ld	h, #0x00
   557E 3E 50         [ 7]  563 	ld	a, #0x50
   5580 95            [ 4]  564 	sub	a, l
   5581 6F            [ 4]  565 	ld	l, a
   5582 3E 00         [ 7]  566 	ld	a, #0x00
   5584 9C            [ 4]  567 	sbc	a, h
   5585 67            [ 4]  568 	ld	h, a
                            569 ;src/entities/enemy.c:94: if (nextx > maxx) {
   5586 7D            [ 4]  570 	ld	a, l
   5587 91            [ 4]  571 	sub	a, c
   5588 7C            [ 4]  572 	ld	a, h
   5589 98            [ 4]  573 	sbc	a, b
   558A E2 8F 55      [10]  574 	jp	PO, 00163$
   558D EE 80         [ 7]  575 	xor	a, #0x80
   558F                     576 00163$:
   558F F2 9B 55      [10]  577 	jp	P, 00115$
                            578 ;src/entities/enemy.c:95: nextx = maxx;
   5592 4D            [ 4]  579 	ld	c, l
                            580 ;src/entities/enemy.c:96: enemy->vx = -1;
   5593 DD 6E F9      [19]  581 	ld	l,-7 (ix)
   5596 DD 66 FA      [19]  582 	ld	h,-6 (ix)
   5599 36 FF         [10]  583 	ld	(hl), #0xff
   559B                     584 00115$:
                            585 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   559B DD 6E FC      [19]  586 	ld	l,-4 (ix)
   559E DD 66 FD      [19]  587 	ld	h,-3 (ix)
   55A1 71            [ 7]  588 	ld	(hl), c
                            589 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   55A2 1A            [ 7]  590 	ld	a, (de)
   55A3 4F            [ 4]  591 	ld	c, a
   55A4 0C            [ 4]  592 	inc	c
   55A5 79            [ 4]  593 	ld	a, c
   55A6 12            [ 7]  594 	ld	(de), a
                            595 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   55A7 3E 03         [ 7]  596 	ld	a, #0x03
   55A9 91            [ 4]  597 	sub	a, c
   55AA E2 AF 55      [10]  598 	jp	PO, 00164$
   55AD EE 80         [ 7]  599 	xor	a, #0x80
   55AF                     600 00164$:
   55AF F2 B5 55      [10]  601 	jp	P, 00117$
   55B2 3E 03         [ 7]  602 	ld	a, #0x03
   55B4 12            [ 7]  603 	ld	(de), a
   55B5                     604 00117$:
                            605 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   55B5 DD 6E F7      [19]  606 	ld	l,-9 (ix)
   55B8 DD 66 F8      [19]  607 	ld	h,-8 (ix)
   55BB 4E            [ 7]  608 	ld	c, (hl)
   55BC 06 00         [ 7]  609 	ld	b, #0x00
   55BE 1A            [ 7]  610 	ld	a, (de)
   55BF 6F            [ 4]  611 	ld	l, a
   55C0 17            [ 4]  612 	rla
   55C1 9F            [ 4]  613 	sbc	a, a
   55C2 67            [ 4]  614 	ld	h, a
   55C3 09            [11]  615 	add	hl, bc
   55C4 E5            [11]  616 	push	hl
   55C5 FD E1         [14]  617 	pop	iy
                            618 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   55C7 DD 7E FC      [19]  619 	ld	a, -4 (ix)
   55CA C6 05         [ 7]  620 	add	a, #0x05
   55CC DD 77 FE      [19]  621 	ld	-2 (ix), a
   55CF DD 7E FD      [19]  622 	ld	a, -3 (ix)
   55D2 CE 00         [ 7]  623 	adc	a, #0x00
   55D4 DD 77 FF      [19]  624 	ld	-1 (ix), a
   55D7 DD 6E FE      [19]  625 	ld	l,-2 (ix)
   55DA DD 66 FF      [19]  626 	ld	h,-1 (ix)
   55DD 7E            [ 7]  627 	ld	a, (hl)
   55DE DD 6E FC      [19]  628 	ld	l,-4 (ix)
   55E1 DD 66 FD      [19]  629 	ld	h,-3 (ix)
   55E4 4E            [ 7]  630 	ld	c, (hl)
   55E5 06 00         [ 7]  631 	ld	b, #0x00
   55E7 D5            [11]  632 	push	de
   55E8 F5            [11]  633 	push	af
   55E9 33            [ 6]  634 	inc	sp
   55EA FD E5         [15]  635 	push	iy
   55EC C5            [11]  636 	push	bc
   55ED CD 42 4C      [17]  637 	call	_collision_clamp_y_at
   55F0 F1            [10]  638 	pop	af
   55F1 F1            [10]  639 	pop	af
   55F2 33            [ 6]  640 	inc	sp
   55F3 4D            [ 4]  641 	ld	c, l
   55F4 D1            [10]  642 	pop	de
                            643 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55F5 DD 6E F7      [19]  644 	ld	l,-9 (ix)
   55F8 DD 66 F8      [19]  645 	ld	h,-8 (ix)
   55FB 71            [ 7]  646 	ld	(hl), c
                            647 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55FC DD 6E FE      [19]  648 	ld	l,-2 (ix)
   55FF DD 66 FF      [19]  649 	ld	h,-1 (ix)
   5602 7E            [ 7]  650 	ld	a, (hl)
   5603 06 00         [ 7]  651 	ld	b, #0x00
   5605 DD 6E FC      [19]  652 	ld	l,-4 (ix)
   5608 DD 66 FD      [19]  653 	ld	h,-3 (ix)
   560B 6E            [ 7]  654 	ld	l, (hl)
   560C DD 75 FE      [19]  655 	ld	-2 (ix), l
   560F DD 36 FF 00   [19]  656 	ld	-1 (ix), #0x00
   5613 D5            [11]  657 	push	de
   5614 F5            [11]  658 	push	af
   5615 33            [ 6]  659 	inc	sp
   5616 C5            [11]  660 	push	bc
   5617 DD 6E FE      [19]  661 	ld	l,-2 (ix)
   561A DD 66 FF      [19]  662 	ld	h,-1 (ix)
   561D E5            [11]  663 	push	hl
   561E CD C3 4B      [17]  664 	call	_collision_is_on_ground_at
   5621 F1            [10]  665 	pop	af
   5622 F1            [10]  666 	pop	af
   5623 33            [ 6]  667 	inc	sp
   5624 D1            [10]  668 	pop	de
   5625 7D            [ 4]  669 	ld	a, l
   5626 B7            [ 4]  670 	or	a, a
   5627 28 0E         [12]  671 	jr	Z,00121$
   5629 1A            [ 7]  672 	ld	a, (de)
   562A 4F            [ 4]  673 	ld	c, a
   562B AF            [ 4]  674 	xor	a, a
   562C 91            [ 4]  675 	sub	a, c
   562D E2 32 56      [10]  676 	jp	PO, 00165$
   5630 EE 80         [ 7]  677 	xor	a, #0x80
   5632                     678 00165$:
   5632 F2 37 56      [10]  679 	jp	P, 00121$
                            680 ;src/entities/enemy.c:107: enemy->vy = 0;
   5635 AF            [ 4]  681 	xor	a, a
   5636 12            [ 7]  682 	ld	(de), a
   5637                     683 00121$:
   5637 DD F9         [10]  684 	ld	sp, ix
   5639 DD E1         [14]  685 	pop	ix
   563B C9            [10]  686 	ret
                            687 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            688 ;	---------------------------------
                            689 ; Function enemyrender
                            690 ; ---------------------------------
   563C                     691 _enemyrender::
   563C DD E5         [15]  692 	push	ix
   563E DD 21 00 00   [14]  693 	ld	ix,#0
   5642 DD 39         [15]  694 	add	ix,sp
   5644 F5            [11]  695 	push	af
                            696 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5645 DD 7E 05      [19]  697 	ld	a, 5 (ix)
   5648 DD B6 04      [19]  698 	or	a,4 (ix)
   564B CA C9 56      [10]  699 	jp	Z,00113$
   564E DD 7E 04      [19]  700 	ld	a, 4 (ix)
   5651 DD 77 FE      [19]  701 	ld	-2 (ix), a
   5654 DD 7E 05      [19]  702 	ld	a, 5 (ix)
   5657 DD 77 FF      [19]  703 	ld	-1 (ix), a
   565A E1            [10]  704 	pop	hl
   565B E5            [11]  705 	push	hl
   565C 11 06 00      [10]  706 	ld	de, #0x0006
   565F 19            [11]  707 	add	hl, de
   5660 7E            [ 7]  708 	ld	a, (hl)
   5661 B7            [ 4]  709 	or	a, a
                            710 ;src/entities/enemy.c:116: return;
   5662 28 65         [12]  711 	jr	Z,00113$
                            712 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   5664 E1            [10]  713 	pop	hl
   5665 E5            [11]  714 	push	hl
   5666 11 09 00      [10]  715 	ld	de, #0x0009
   5669 19            [11]  716 	add	hl, de
   566A 7E            [ 7]  717 	ld	a, (hl)
   566B FE 03         [ 7]  718 	cp	a, #0x03
   566D 20 0A         [12]  719 	jr	NZ,00111$
   566F 21 0C 0C      [10]  720 	ld	hl, #0x0c0c
   5672 E5            [11]  721 	push	hl
   5673 CD 8B 5D      [17]  722 	call	_cpct_px2byteM0
   5676 4D            [ 4]  723 	ld	c, l
   5677 18 23         [12]  724 	jr	00112$
   5679                     725 00111$:
                            726 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   5679 FE 02         [ 7]  727 	cp	a, #0x02
   567B 20 0A         [12]  728 	jr	NZ,00108$
   567D 21 0A 0A      [10]  729 	ld	hl, #0x0a0a
   5680 E5            [11]  730 	push	hl
   5681 CD 8B 5D      [17]  731 	call	_cpct_px2byteM0
   5684 4D            [ 4]  732 	ld	c, l
   5685 18 15         [12]  733 	jr	00112$
   5687                     734 00108$:
                            735 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   5687 3D            [ 4]  736 	dec	a
   5688 20 0A         [12]  737 	jr	NZ,00105$
   568A 21 0E 0E      [10]  738 	ld	hl, #0x0e0e
   568D E5            [11]  739 	push	hl
   568E CD 8B 5D      [17]  740 	call	_cpct_px2byteM0
   5691 4D            [ 4]  741 	ld	c, l
   5692 18 08         [12]  742 	jr	00112$
   5694                     743 00105$:
                            744 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   5694 21 04 04      [10]  745 	ld	hl, #0x0404
   5697 E5            [11]  746 	push	hl
   5698 CD 8B 5D      [17]  747 	call	_cpct_px2byteM0
   569B 4D            [ 4]  748 	ld	c, l
   569C                     749 00112$:
                            750 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   569C E1            [10]  751 	pop	hl
   569D E5            [11]  752 	push	hl
   569E 23            [ 6]  753 	inc	hl
   569F 46            [ 7]  754 	ld	b, (hl)
   56A0 E1            [10]  755 	pop	hl
   56A1 E5            [11]  756 	push	hl
   56A2 56            [ 7]  757 	ld	d, (hl)
   56A3 C5            [11]  758 	push	bc
   56A4 4A            [ 4]  759 	ld	c, d
   56A5 C5            [11]  760 	push	bc
   56A6 21 00 C0      [10]  761 	ld	hl, #0xc000
   56A9 E5            [11]  762 	push	hl
   56AA CD 7E 5E      [17]  763 	call	_cpct_getScreenPtr
   56AD EB            [ 4]  764 	ex	de,hl
   56AE C1            [10]  765 	pop	bc
                            766 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   56AF E1            [10]  767 	pop	hl
   56B0 E5            [11]  768 	push	hl
   56B1 23            [ 6]  769 	inc	hl
   56B2 23            [ 6]  770 	inc	hl
   56B3 23            [ 6]  771 	inc	hl
   56B4 23            [ 6]  772 	inc	hl
   56B5 23            [ 6]  773 	inc	hl
   56B6 46            [ 7]  774 	ld	b, (hl)
   56B7 E1            [10]  775 	pop	hl
   56B8 E5            [11]  776 	push	hl
   56B9 23            [ 6]  777 	inc	hl
   56BA 23            [ 6]  778 	inc	hl
   56BB 23            [ 6]  779 	inc	hl
   56BC 23            [ 6]  780 	inc	hl
   56BD 7E            [ 7]  781 	ld	a, (hl)
   56BE C5            [11]  782 	push	bc
   56BF 33            [ 6]  783 	inc	sp
   56C0 47            [ 4]  784 	ld	b, a
   56C1 C5            [11]  785 	push	bc
   56C2 D5            [11]  786 	push	de
   56C3 CD C5 5D      [17]  787 	call	_cpct_drawSolidBox
   56C6 F1            [10]  788 	pop	af
   56C7 F1            [10]  789 	pop	af
   56C8 33            [ 6]  790 	inc	sp
   56C9                     791 00113$:
   56C9 DD F9         [10]  792 	ld	sp, ix
   56CB DD E1         [14]  793 	pop	ix
   56CD C9            [10]  794 	ret
                            795 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            796 ;	---------------------------------
                            797 ; Function enemydamage
                            798 ; ---------------------------------
   56CE                     799 _enemydamage::
   56CE DD E5         [15]  800 	push	ix
   56D0 DD 21 00 00   [14]  801 	ld	ix,#0
   56D4 DD 39         [15]  802 	add	ix,sp
                            803 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   56D6 DD 7E 05      [19]  804 	ld	a, 5 (ix)
   56D9 DD B6 04      [19]  805 	or	a,4 (ix)
   56DC 28 0F         [12]  806 	jr	Z,00101$
   56DE DD 4E 04      [19]  807 	ld	c,4 (ix)
   56E1 DD 46 05      [19]  808 	ld	b,5 (ix)
   56E4 21 06 00      [10]  809 	ld	hl, #0x0006
   56E7 09            [11]  810 	add	hl,bc
   56E8 EB            [ 4]  811 	ex	de,hl
   56E9 1A            [ 7]  812 	ld	a, (de)
   56EA B7            [ 4]  813 	or	a, a
   56EB 20 04         [12]  814 	jr	NZ,00102$
   56ED                     815 00101$:
                            816 ;src/entities/enemy.c:130: return 0;
   56ED 2E 00         [ 7]  817 	ld	l, #0x00
   56EF 18 1A         [12]  818 	jr	00106$
   56F1                     819 00102$:
                            820 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56F1 21 07 00      [10]  821 	ld	hl, #0x0007
   56F4 09            [11]  822 	add	hl, bc
   56F5 4E            [ 7]  823 	ld	c, (hl)
   56F6 DD 7E 06      [19]  824 	ld	a, 6 (ix)
   56F9 91            [ 4]  825 	sub	a, c
   56FA 38 08         [12]  826 	jr	C,00105$
                            827 ;src/entities/enemy.c:134: enemy->health = 0;
   56FC 36 00         [10]  828 	ld	(hl), #0x00
                            829 ;src/entities/enemy.c:135: enemy->active = 0;
   56FE AF            [ 4]  830 	xor	a, a
   56FF 12            [ 7]  831 	ld	(de), a
                            832 ;src/entities/enemy.c:136: return 1;
   5700 2E 01         [ 7]  833 	ld	l, #0x01
   5702 18 07         [12]  834 	jr	00106$
   5704                     835 00105$:
                            836 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   5704 79            [ 4]  837 	ld	a, c
   5705 DD 96 06      [19]  838 	sub	a, 6 (ix)
   5708 77            [ 7]  839 	ld	(hl), a
                            840 ;src/entities/enemy.c:140: return 0;
   5709 2E 00         [ 7]  841 	ld	l, #0x00
   570B                     842 00106$:
   570B DD E1         [14]  843 	pop	ix
   570D C9            [10]  844 	ret
                            845 	.area _CODE
                            846 	.area _INITIALIZER
                            847 	.area _CABS (ABS)
