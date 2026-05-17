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
   51E5                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   51E5 21 03 00      [10]   58 	ld	hl, #2+1
   51E8 39            [11]   59 	add	hl, sp
   51E9 7E            [ 7]   60 	ld	a, (hl)
   51EA 2B            [ 6]   61 	dec	hl
   51EB B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   51EC C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   51ED D1            [10]   66 	pop	de
   51EE C1            [10]   67 	pop	bc
   51EF C5            [11]   68 	push	bc
   51F0 D5            [11]   69 	push	de
   51F1 AF            [ 4]   70 	xor	a, a
   51F2 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   51F3 59            [ 4]   73 	ld	e, c
   51F4 50            [ 4]   74 	ld	d, b
   51F5 13            [ 6]   75 	inc	de
   51F6 AF            [ 4]   76 	xor	a, a
   51F7 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   51F8 59            [ 4]   79 	ld	e, c
   51F9 50            [ 4]   80 	ld	d, b
   51FA 13            [ 6]   81 	inc	de
   51FB 13            [ 6]   82 	inc	de
   51FC AF            [ 4]   83 	xor	a, a
   51FD 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   51FE 59            [ 4]   86 	ld	e, c
   51FF 50            [ 4]   87 	ld	d, b
   5200 13            [ 6]   88 	inc	de
   5201 13            [ 6]   89 	inc	de
   5202 13            [ 6]   90 	inc	de
   5203 AF            [ 4]   91 	xor	a, a
   5204 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   5205 21 04 00      [10]   94 	ld	hl, #0x0004
   5208 09            [11]   95 	add	hl, bc
   5209 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   520B 21 05 00      [10]   98 	ld	hl, #0x0005
   520E 09            [11]   99 	add	hl, bc
   520F 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5211 21 06 00      [10]  102 	ld	hl, #0x0006
   5214 09            [11]  103 	add	hl, bc
   5215 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   5217 21 07 00      [10]  106 	ld	hl, #0x0007
   521A 09            [11]  107 	add	hl, bc
   521B 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   521D 21 08 00      [10]  110 	ld	hl, #0x0008
   5220 09            [11]  111 	add	hl, bc
   5221 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   5223 21 09 00      [10]  114 	ld	hl, #0x0009
   5226 09            [11]  115 	add	hl, bc
   5227 36 00         [10]  116 	ld	(hl), #0x00
   5229 C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   522A                     122 _enemyspawn::
   522A DD E5         [15]  123 	push	ix
   522C DD 21 00 00   [14]  124 	ld	ix,#0
   5230 DD 39         [15]  125 	add	ix,sp
   5232 21 F1 FF      [10]  126 	ld	hl, #-15
   5235 39            [11]  127 	add	hl, sp
   5236 F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   5237 DD 7E 05      [19]  130 	ld	a, 5 (ix)
   523A DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   523D CA FD 53      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   5240 DD 7E 04      [19]  135 	ld	a, 4 (ix)
   5243 DD 77 FE      [19]  136 	ld	-2 (ix), a
   5246 DD 7E 05      [19]  137 	ld	a, 5 (ix)
   5249 DD 77 FF      [19]  138 	ld	-1 (ix), a
   524C DD 6E FE      [19]  139 	ld	l,-2 (ix)
   524F DD 66 FF      [19]  140 	ld	h,-1 (ix)
   5252 DD 7E 06      [19]  141 	ld	a, 6 (ix)
   5255 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   5256 DD 4E FE      [19]  144 	ld	c,-2 (ix)
   5259 DD 46 FF      [19]  145 	ld	b,-1 (ix)
   525C 03            [ 6]  146 	inc	bc
   525D DD 7E 07      [19]  147 	ld	a, 7 (ix)
   5260 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   5261 DD 7E FE      [19]  150 	ld	a, -2 (ix)
   5264 C6 02         [ 7]  151 	add	a, #0x02
   5266 DD 77 FC      [19]  152 	ld	-4 (ix), a
   5269 DD 7E FF      [19]  153 	ld	a, -1 (ix)
   526C CE 00         [ 7]  154 	adc	a, #0x00
   526E DD 77 FD      [19]  155 	ld	-3 (ix), a
   5271 DD 7E 09      [19]  156 	ld	a, 9 (ix)
   5274 B7            [ 4]  157 	or	a, a
   5275 28 04         [12]  158 	jr	Z,00114$
   5277 0E 01         [ 7]  159 	ld	c, #0x01
   5279 18 02         [12]  160 	jr	00115$
   527B                     161 00114$:
   527B 0E FF         [ 7]  162 	ld	c, #0xff
   527D                     163 00115$:
   527D DD 6E FC      [19]  164 	ld	l,-4 (ix)
   5280 DD 66 FD      [19]  165 	ld	h,-3 (ix)
   5283 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   5284 DD 7E FE      [19]  168 	ld	a, -2 (ix)
   5287 C6 03         [ 7]  169 	add	a, #0x03
   5289 DD 77 FA      [19]  170 	ld	-6 (ix), a
   528C DD 7E FF      [19]  171 	ld	a, -1 (ix)
   528F CE 00         [ 7]  172 	adc	a, #0x00
   5291 DD 77 FB      [19]  173 	ld	-5 (ix), a
   5294 DD 6E FA      [19]  174 	ld	l,-6 (ix)
   5297 DD 66 FB      [19]  175 	ld	h,-5 (ix)
   529A 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   529C DD 7E FE      [19]  178 	ld	a, -2 (ix)
   529F C6 06         [ 7]  179 	add	a, #0x06
   52A1 DD 77 F8      [19]  180 	ld	-8 (ix), a
   52A4 DD 7E FF      [19]  181 	ld	a, -1 (ix)
   52A7 CE 00         [ 7]  182 	adc	a, #0x00
   52A9 DD 77 F9      [19]  183 	ld	-7 (ix), a
   52AC DD 6E F8      [19]  184 	ld	l,-8 (ix)
   52AF DD 66 F9      [19]  185 	ld	h,-7 (ix)
   52B2 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52B4 DD 7E FE      [19]  188 	ld	a, -2 (ix)
   52B7 C6 09         [ 7]  189 	add	a, #0x09
   52B9 DD 77 F8      [19]  190 	ld	-8 (ix), a
   52BC DD 7E FF      [19]  191 	ld	a, -1 (ix)
   52BF CE 00         [ 7]  192 	adc	a, #0x00
   52C1 DD 77 F9      [19]  193 	ld	-7 (ix), a
   52C4 DD 6E F8      [19]  194 	ld	l,-8 (ix)
   52C7 DD 66 F9      [19]  195 	ld	h,-7 (ix)
   52CA DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52CD 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52CE DD 7E FE      [19]  199 	ld	a, -2 (ix)
   52D1 C6 04         [ 7]  200 	add	a, #0x04
   52D3 DD 77 F8      [19]  201 	ld	-8 (ix), a
   52D6 DD 7E FF      [19]  202 	ld	a, -1 (ix)
   52D9 CE 00         [ 7]  203 	adc	a, #0x00
   52DB DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52DE DD 7E FE      [19]  206 	ld	a, -2 (ix)
   52E1 C6 05         [ 7]  207 	add	a, #0x05
   52E3 DD 77 F6      [19]  208 	ld	-10 (ix), a
   52E6 DD 7E FF      [19]  209 	ld	a, -1 (ix)
   52E9 CE 00         [ 7]  210 	adc	a, #0x00
   52EB DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   52EE DD 7E FE      [19]  213 	ld	a, -2 (ix)
   52F1 C6 07         [ 7]  214 	add	a, #0x07
   52F3 DD 77 F4      [19]  215 	ld	-12 (ix), a
   52F6 DD 7E FF      [19]  216 	ld	a, -1 (ix)
   52F9 CE 00         [ 7]  217 	adc	a, #0x00
   52FB DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   52FE DD 7E FE      [19]  220 	ld	a, -2 (ix)
   5301 C6 08         [ 7]  221 	add	a, #0x08
   5303 DD 77 FE      [19]  222 	ld	-2 (ix), a
   5306 DD 7E FF      [19]  223 	ld	a, -1 (ix)
   5309 CE 00         [ 7]  224 	adc	a, #0x00
   530B DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   530E DD 7E 08      [19]  227 	ld	a, 8 (ix)
   5311 3D            [ 4]  228 	dec	a
   5312 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   5314 DD 6E F8      [19]  231 	ld	l,-8 (ix)
   5317 DD 66 F9      [19]  232 	ld	h,-7 (ix)
   531A 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   531C DD 6E F6      [19]  235 	ld	l,-10 (ix)
   531F DD 66 F7      [19]  236 	ld	h,-9 (ix)
   5322 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   5324 DD 6E F4      [19]  239 	ld	l,-12 (ix)
   5327 DD 66 F5      [19]  240 	ld	h,-11 (ix)
   532A 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   532C DD 6E FE      [19]  243 	ld	l,-2 (ix)
   532F DD 66 FF      [19]  244 	ld	h,-1 (ix)
   5332 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   5334 DD 7E FC      [19]  247 	ld	a, -4 (ix)
   5337 DD 77 F2      [19]  248 	ld	-14 (ix), a
   533A DD 7E FD      [19]  249 	ld	a, -3 (ix)
   533D DD 77 F3      [19]  250 	ld	-13 (ix), a
   5340 DD 7E 09      [19]  251 	ld	a, 9 (ix)
   5343 B7            [ 4]  252 	or	a, a
   5344 28 06         [12]  253 	jr	Z,00116$
   5346 DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   534A 18 04         [12]  255 	jr	00117$
   534C                     256 00116$:
   534C DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   5350                     258 00117$:
   5350 DD 6E F2      [19]  259 	ld	l,-14 (ix)
   5353 DD 66 F3      [19]  260 	ld	h,-13 (ix)
   5356 DD 7E F1      [19]  261 	ld	a, -15 (ix)
   5359 77            [ 7]  262 	ld	(hl), a
   535A C3 FD 53      [10]  263 	jp	00112$
   535D                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   535D DD 7E 08      [19]  266 	ld	a, 8 (ix)
   5360 D6 02         [ 7]  267 	sub	a, #0x02
   5362 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   5364 DD 6E F8      [19]  270 	ld	l,-8 (ix)
   5367 DD 66 F9      [19]  271 	ld	h,-7 (ix)
   536A 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   536C DD 6E F6      [19]  274 	ld	l,-10 (ix)
   536F DD 66 F7      [19]  275 	ld	h,-9 (ix)
   5372 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   5374 DD 6E F4      [19]  278 	ld	l,-12 (ix)
   5377 DD 66 F5      [19]  279 	ld	h,-11 (ix)
   537A 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   537C DD 6E FE      [19]  282 	ld	l,-2 (ix)
   537F DD 66 FF      [19]  283 	ld	h,-1 (ix)
   5382 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5384 DD 4E FA      [19]  286 	ld	c,-6 (ix)
   5387 DD 46 FB      [19]  287 	ld	b,-5 (ix)
   538A DD 7E 09      [19]  288 	ld	a, 9 (ix)
   538D B7            [ 4]  289 	or	a, a
   538E 28 04         [12]  290 	jr	Z,00118$
   5390 3E 01         [ 7]  291 	ld	a, #0x01
   5392 18 02         [12]  292 	jr	00119$
   5394                     293 00118$:
   5394 3E FF         [ 7]  294 	ld	a, #0xff
   5396                     295 00119$:
   5396 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   5397 DD 6E FC      [19]  298 	ld	l,-4 (ix)
   539A DD 66 FD      [19]  299 	ld	h,-3 (ix)
   539D 36 01         [10]  300 	ld	(hl), #0x01
   539F 18 5C         [12]  301 	jr	00112$
   53A1                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   53A1 DD 7E 08      [19]  304 	ld	a, 8 (ix)
   53A4 D6 03         [ 7]  305 	sub	a, #0x03
   53A6 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   53A8 DD 6E F8      [19]  308 	ld	l,-8 (ix)
   53AB DD 66 F9      [19]  309 	ld	h,-7 (ix)
   53AE 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   53B0 DD 6E F6      [19]  312 	ld	l,-10 (ix)
   53B3 DD 66 F7      [19]  313 	ld	h,-9 (ix)
   53B6 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53B8 DD 6E F4      [19]  316 	ld	l,-12 (ix)
   53BB DD 66 F5      [19]  317 	ld	h,-11 (ix)
   53BE 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53C0 DD 6E FE      [19]  320 	ld	l,-2 (ix)
   53C3 DD 66 FF      [19]  321 	ld	h,-1 (ix)
   53C6 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53C8 DD 4E FC      [19]  324 	ld	c,-4 (ix)
   53CB DD 46 FD      [19]  325 	ld	b,-3 (ix)
   53CE DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53D1 B7            [ 4]  327 	or	a, a
   53D2 28 04         [12]  328 	jr	Z,00120$
   53D4 3E 01         [ 7]  329 	ld	a, #0x01
   53D6 18 02         [12]  330 	jr	00121$
   53D8                     331 00120$:
   53D8 3E FF         [ 7]  332 	ld	a, #0xff
   53DA                     333 00121$:
   53DA 02            [ 7]  334 	ld	(bc), a
   53DB 18 20         [12]  335 	jr	00112$
   53DD                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53DD DD 6E F8      [19]  338 	ld	l,-8 (ix)
   53E0 DD 66 F9      [19]  339 	ld	h,-7 (ix)
   53E3 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   53E5 DD 6E F6      [19]  342 	ld	l,-10 (ix)
   53E8 DD 66 F7      [19]  343 	ld	h,-9 (ix)
   53EB 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   53ED DD 6E F4      [19]  346 	ld	l,-12 (ix)
   53F0 DD 66 F5      [19]  347 	ld	h,-11 (ix)
   53F3 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   53F5 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   53F8 DD 66 FF      [19]  351 	ld	h,-1 (ix)
   53FB 36 64         [10]  352 	ld	(hl), #0x64
   53FD                     353 00112$:
   53FD DD F9         [10]  354 	ld	sp, ix
   53FF DD E1         [14]  355 	pop	ix
   5401 C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   5402                     361 _enemyupdate::
   5402 DD E5         [15]  362 	push	ix
   5404 DD 21 00 00   [14]  363 	ld	ix,#0
   5408 DD 39         [15]  364 	add	ix,sp
   540A 21 F6 FF      [10]  365 	ld	hl, #-10
   540D 39            [11]  366 	add	hl, sp
   540E F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   540F DD 7E 05      [19]  369 	ld	a, 5 (ix)
   5412 DD B6 04      [19]  370 	or	a,4 (ix)
   5415 CA 02 56      [10]  371 	jp	Z,00121$
   5418 DD 7E 04      [19]  372 	ld	a, 4 (ix)
   541B DD 77 FB      [19]  373 	ld	-5 (ix), a
   541E DD 7E 05      [19]  374 	ld	a, 5 (ix)
   5421 DD 77 FC      [19]  375 	ld	-4 (ix), a
   5424 DD 6E FB      [19]  376 	ld	l,-5 (ix)
   5427 DD 66 FC      [19]  377 	ld	h,-4 (ix)
   542A 11 06 00      [10]  378 	ld	de, #0x0006
   542D 19            [11]  379 	add	hl, de
   542E 7E            [ 7]  380 	ld	a, (hl)
   542F B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   5430 CA 02 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5433 DD 6E FB      [19]  385 	ld	l,-5 (ix)
   5436 DD 66 FC      [19]  386 	ld	h,-4 (ix)
   5439 11 09 00      [10]  387 	ld	de, #0x0009
   543C 19            [11]  388 	add	hl, de
   543D 7E            [ 7]  389 	ld	a, (hl)
   543E DD 77 FA      [19]  390 	ld	-6 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5441 DD 6E FB      [19]  392 	ld	l,-5 (ix)
   5444 DD 66 FC      [19]  393 	ld	h,-4 (ix)
   5447 4E            [ 7]  394 	ld	c, (hl)
   5448 DD 7E FB      [19]  395 	ld	a, -5 (ix)
   544B C6 02         [ 7]  396 	add	a, #0x02
   544D DD 77 F8      [19]  397 	ld	-8 (ix), a
   5450 DD 7E FC      [19]  398 	ld	a, -4 (ix)
   5453 CE 00         [ 7]  399 	adc	a, #0x00
   5455 DD 77 F9      [19]  400 	ld	-7 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5458 DD 7E FB      [19]  402 	ld	a, -5 (ix)
   545B C6 01         [ 7]  403 	add	a, #0x01
   545D DD 77 F6      [19]  404 	ld	-10 (ix), a
   5460 DD 7E FC      [19]  405 	ld	a, -4 (ix)
   5463 CE 00         [ 7]  406 	adc	a, #0x00
   5465 DD 77 F7      [19]  407 	ld	-9 (ix), a
   5468 DD 5E FB      [19]  408 	ld	e,-5 (ix)
   546B DD 56 FC      [19]  409 	ld	d,-4 (ix)
   546E 13            [ 6]  410 	inc	de
   546F 13            [ 6]  411 	inc	de
   5470 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5471 06 00         [ 7]  414 	ld	b, #0x00
   5473 DD 6E F8      [19]  415 	ld	l,-8 (ix)
   5476 DD 66 F9      [19]  416 	ld	h,-7 (ix)
   5479 7E            [ 7]  417 	ld	a, (hl)
   547A DD 77 FF      [19]  418 	ld	-1 (ix), a
   547D 6F            [ 4]  419 	ld	l, a
   547E DD 7E FF      [19]  420 	ld	a, -1 (ix)
   5481 17            [ 4]  421 	rla
   5482 9F            [ 4]  422 	sbc	a, a
   5483 67            [ 4]  423 	ld	h, a
   5484 09            [11]  424 	add	hl,bc
   5485 4D            [ 4]  425 	ld	c, l
   5486 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5487 DD 7E FA      [19]  428 	ld	a, -6 (ix)
   548A D6 02         [ 7]  429 	sub	a, #0x02
   548C C2 2E 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   548F E1            [10]  433 	pop	hl
   5490 E5            [11]  434 	push	hl
   5491 6E            [ 7]  435 	ld	l, (hl)
   5492 DD 75 FD      [19]  436 	ld	-3 (ix), l
   5495 DD 36 FE 00   [19]  437 	ld	-2 (ix), #0x00
   5499 1A            [ 7]  438 	ld	a, (de)
   549A 6F            [ 4]  439 	ld	l, a
   549B 17            [ 4]  440 	rla
   549C 9F            [ 4]  441 	sbc	a, a
   549D 67            [ 4]  442 	ld	h, a
   549E DD 7E FD      [19]  443 	ld	a, -3 (ix)
   54A1 85            [ 4]  444 	add	a, l
   54A2 DD 77 FD      [19]  445 	ld	-3 (ix), a
   54A5 DD 7E FE      [19]  446 	ld	a, -2 (ix)
   54A8 8C            [ 4]  447 	adc	a, h
   54A9 DD 77 FE      [19]  448 	ld	-2 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   54AC 79            [ 4]  450 	ld	a, c
   54AD D6 08         [ 7]  451 	sub	a, #0x08
   54AF 78            [ 4]  452 	ld	a, b
   54B0 17            [ 4]  453 	rla
   54B1 3F            [ 4]  454 	ccf
   54B2 1F            [ 4]  455 	rra
   54B3 DE 80         [ 7]  456 	sbc	a, #0x80
   54B5 38 0E         [12]  457 	jr	C,00104$
   54B7 3E 48         [ 7]  458 	ld	a, #0x48
   54B9 B9            [ 4]  459 	cp	a, c
   54BA 3E 00         [ 7]  460 	ld	a, #0x00
   54BC 98            [ 4]  461 	sbc	a, b
   54BD E2 C2 54      [10]  462 	jp	PO, 00161$
   54C0 EE 80         [ 7]  463 	xor	a, #0x80
   54C2                     464 00161$:
   54C2 F2 E0 54      [10]  465 	jp	P, 00105$
   54C5                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   54C5 AF            [ 4]  468 	xor	a, a
   54C6 DD 96 FF      [19]  469 	sub	a, -1 (ix)
   54C9 4F            [ 4]  470 	ld	c, a
   54CA DD 6E F8      [19]  471 	ld	l,-8 (ix)
   54CD DD 66 F9      [19]  472 	ld	h,-7 (ix)
   54D0 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54D1 DD 6E FB      [19]  475 	ld	l,-5 (ix)
   54D4 DD 66 FC      [19]  476 	ld	h,-4 (ix)
   54D7 6E            [ 7]  477 	ld	l, (hl)
   54D8 26 00         [ 7]  478 	ld	h, #0x00
   54DA 79            [ 4]  479 	ld	a, c
   54DB 17            [ 4]  480 	rla
   54DC 9F            [ 4]  481 	sbc	a, a
   54DD 47            [ 4]  482 	ld	b, a
   54DE 09            [11]  483 	add	hl,bc
   54DF 4D            [ 4]  484 	ld	c, l
   54E0                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   54E0 DD 7E FD      [19]  487 	ld	a, -3 (ix)
   54E3 D6 38         [ 7]  488 	sub	a, #0x38
   54E5 DD 7E FE      [19]  489 	ld	a, -2 (ix)
   54E8 17            [ 4]  490 	rla
   54E9 3F            [ 4]  491 	ccf
   54EA 1F            [ 4]  492 	rra
   54EB DE 80         [ 7]  493 	sbc	a, #0x80
   54ED 38 12         [12]  494 	jr	C,00107$
   54EF 3E 78         [ 7]  495 	ld	a, #0x78
   54F1 DD BE FD      [19]  496 	cp	a, -3 (ix)
   54F4 3E 00         [ 7]  497 	ld	a, #0x00
   54F6 DD 9E FE      [19]  498 	sbc	a, -2 (ix)
   54F9 E2 FE 54      [10]  499 	jp	PO, 00162$
   54FC EE 80         [ 7]  500 	xor	a, #0x80
   54FE                     501 00162$:
   54FE F2 1E 55      [10]  502 	jp	P, 00108$
   5501                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5501 1A            [ 7]  505 	ld	a, (de)
   5502 6F            [ 4]  506 	ld	l, a
   5503 AF            [ 4]  507 	xor	a, a
   5504 95            [ 4]  508 	sub	a, l
   5505 DD 77 FF      [19]  509 	ld	-1 (ix), a
   5508 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5509 E1            [10]  512 	pop	hl
   550A E5            [11]  513 	push	hl
   550B 5E            [ 7]  514 	ld	e, (hl)
   550C 16 00         [ 7]  515 	ld	d, #0x00
   550E DD 6E FF      [19]  516 	ld	l, -1 (ix)
   5511 DD 7E FF      [19]  517 	ld	a, -1 (ix)
   5514 17            [ 4]  518 	rla
   5515 9F            [ 4]  519 	sbc	a, a
   5516 67            [ 4]  520 	ld	h, a
   5517 19            [11]  521 	add	hl,de
   5518 DD 75 FD      [19]  522 	ld	-3 (ix), l
   551B DD 74 FE      [19]  523 	ld	-2 (ix), h
   551E                     524 00108$:
                            525 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   551E DD 6E FB      [19]  526 	ld	l,-5 (ix)
   5521 DD 66 FC      [19]  527 	ld	h,-4 (ix)
   5524 71            [ 7]  528 	ld	(hl), c
                            529 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   5525 DD 4E FD      [19]  530 	ld	c, -3 (ix)
   5528 E1            [10]  531 	pop	hl
   5529 E5            [11]  532 	push	hl
   552A 71            [ 7]  533 	ld	(hl), c
                            534 ;src/entities/enemy.c:84: return;
   552B C3 02 56      [10]  535 	jp	00121$
   552E                     536 00111$:
                            537 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            538 ;src/entities/enemy.c:88: if (nextx < 2) {
   552E 79            [ 4]  539 	ld	a, c
   552F D6 02         [ 7]  540 	sub	a, #0x02
   5531 78            [ 4]  541 	ld	a, b
   5532 17            [ 4]  542 	rla
   5533 3F            [ 4]  543 	ccf
   5534 1F            [ 4]  544 	rra
   5535 DE 80         [ 7]  545 	sbc	a, #0x80
   5537 30 0B         [12]  546 	jr	NC,00113$
                            547 ;src/entities/enemy.c:89: nextx = 2;
   5539 01 02 00      [10]  548 	ld	bc, #0x0002
                            549 ;src/entities/enemy.c:90: enemy->vx = 1;
   553C DD 6E F8      [19]  550 	ld	l,-8 (ix)
   553F DD 66 F9      [19]  551 	ld	h,-7 (ix)
   5542 36 01         [10]  552 	ld	(hl), #0x01
   5544                     553 00113$:
                            554 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   5544 DD 6E FB      [19]  555 	ld	l,-5 (ix)
   5547 DD 66 FC      [19]  556 	ld	h,-4 (ix)
   554A 23            [ 6]  557 	inc	hl
   554B 23            [ 6]  558 	inc	hl
   554C 23            [ 6]  559 	inc	hl
   554D 23            [ 6]  560 	inc	hl
   554E 6E            [ 7]  561 	ld	l, (hl)
   554F 26 00         [ 7]  562 	ld	h, #0x00
   5551 3E 50         [ 7]  563 	ld	a, #0x50
   5553 95            [ 4]  564 	sub	a, l
   5554 6F            [ 4]  565 	ld	l, a
   5555 3E 00         [ 7]  566 	ld	a, #0x00
   5557 9C            [ 4]  567 	sbc	a, h
   5558 67            [ 4]  568 	ld	h, a
                            569 ;src/entities/enemy.c:94: if (nextx > maxx) {
   5559 7D            [ 4]  570 	ld	a, l
   555A 91            [ 4]  571 	sub	a, c
   555B 7C            [ 4]  572 	ld	a, h
   555C 98            [ 4]  573 	sbc	a, b
   555D E2 62 55      [10]  574 	jp	PO, 00163$
   5560 EE 80         [ 7]  575 	xor	a, #0x80
   5562                     576 00163$:
   5562 F2 6E 55      [10]  577 	jp	P, 00115$
                            578 ;src/entities/enemy.c:95: nextx = maxx;
   5565 4D            [ 4]  579 	ld	c, l
                            580 ;src/entities/enemy.c:96: enemy->vx = -1;
   5566 DD 6E F8      [19]  581 	ld	l,-8 (ix)
   5569 DD 66 F9      [19]  582 	ld	h,-7 (ix)
   556C 36 FF         [10]  583 	ld	(hl), #0xff
   556E                     584 00115$:
                            585 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   556E DD 6E FB      [19]  586 	ld	l,-5 (ix)
   5571 DD 66 FC      [19]  587 	ld	h,-4 (ix)
   5574 71            [ 7]  588 	ld	(hl), c
                            589 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   5575 1A            [ 7]  590 	ld	a, (de)
   5576 4F            [ 4]  591 	ld	c, a
   5577 0C            [ 4]  592 	inc	c
   5578 79            [ 4]  593 	ld	a, c
   5579 12            [ 7]  594 	ld	(de), a
                            595 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   557A 3E 03         [ 7]  596 	ld	a, #0x03
   557C 91            [ 4]  597 	sub	a, c
   557D E2 82 55      [10]  598 	jp	PO, 00164$
   5580 EE 80         [ 7]  599 	xor	a, #0x80
   5582                     600 00164$:
   5582 F2 88 55      [10]  601 	jp	P, 00117$
   5585 3E 03         [ 7]  602 	ld	a, #0x03
   5587 12            [ 7]  603 	ld	(de), a
   5588                     604 00117$:
                            605 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   5588 E1            [10]  606 	pop	hl
   5589 E5            [11]  607 	push	hl
   558A 4E            [ 7]  608 	ld	c, (hl)
   558B 06 00         [ 7]  609 	ld	b, #0x00
   558D 1A            [ 7]  610 	ld	a, (de)
   558E 6F            [ 4]  611 	ld	l, a
   558F 17            [ 4]  612 	rla
   5590 9F            [ 4]  613 	sbc	a, a
   5591 67            [ 4]  614 	ld	h, a
   5592 09            [11]  615 	add	hl, bc
   5593 E5            [11]  616 	push	hl
   5594 FD E1         [14]  617 	pop	iy
                            618 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5596 DD 7E FB      [19]  619 	ld	a, -5 (ix)
   5599 C6 05         [ 7]  620 	add	a, #0x05
   559B DD 77 FD      [19]  621 	ld	-3 (ix), a
   559E DD 7E FC      [19]  622 	ld	a, -4 (ix)
   55A1 CE 00         [ 7]  623 	adc	a, #0x00
   55A3 DD 77 FE      [19]  624 	ld	-2 (ix), a
   55A6 DD 6E FD      [19]  625 	ld	l,-3 (ix)
   55A9 DD 66 FE      [19]  626 	ld	h,-2 (ix)
   55AC 7E            [ 7]  627 	ld	a, (hl)
   55AD DD 6E FB      [19]  628 	ld	l,-5 (ix)
   55B0 DD 66 FC      [19]  629 	ld	h,-4 (ix)
   55B3 4E            [ 7]  630 	ld	c, (hl)
   55B4 06 00         [ 7]  631 	ld	b, #0x00
   55B6 D5            [11]  632 	push	de
   55B7 F5            [11]  633 	push	af
   55B8 33            [ 6]  634 	inc	sp
   55B9 FD E5         [15]  635 	push	iy
   55BB C5            [11]  636 	push	bc
   55BC CD 29 4C      [17]  637 	call	_collision_clamp_y_at
   55BF F1            [10]  638 	pop	af
   55C0 F1            [10]  639 	pop	af
   55C1 33            [ 6]  640 	inc	sp
   55C2 4D            [ 4]  641 	ld	c, l
   55C3 D1            [10]  642 	pop	de
                            643 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55C4 E1            [10]  644 	pop	hl
   55C5 E5            [11]  645 	push	hl
   55C6 71            [ 7]  646 	ld	(hl), c
                            647 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55C7 DD 6E FD      [19]  648 	ld	l,-3 (ix)
   55CA DD 66 FE      [19]  649 	ld	h,-2 (ix)
   55CD 7E            [ 7]  650 	ld	a, (hl)
   55CE 06 00         [ 7]  651 	ld	b, #0x00
   55D0 DD 6E FB      [19]  652 	ld	l,-5 (ix)
   55D3 DD 66 FC      [19]  653 	ld	h,-4 (ix)
   55D6 6E            [ 7]  654 	ld	l, (hl)
   55D7 DD 75 FD      [19]  655 	ld	-3 (ix), l
   55DA DD 36 FE 00   [19]  656 	ld	-2 (ix), #0x00
   55DE D5            [11]  657 	push	de
   55DF F5            [11]  658 	push	af
   55E0 33            [ 6]  659 	inc	sp
   55E1 C5            [11]  660 	push	bc
   55E2 DD 6E FD      [19]  661 	ld	l,-3 (ix)
   55E5 DD 66 FE      [19]  662 	ld	h,-2 (ix)
   55E8 E5            [11]  663 	push	hl
   55E9 CD AA 4B      [17]  664 	call	_collision_is_on_ground_at
   55EC F1            [10]  665 	pop	af
   55ED F1            [10]  666 	pop	af
   55EE 33            [ 6]  667 	inc	sp
   55EF D1            [10]  668 	pop	de
   55F0 7D            [ 4]  669 	ld	a, l
   55F1 B7            [ 4]  670 	or	a, a
   55F2 28 0E         [12]  671 	jr	Z,00121$
   55F4 1A            [ 7]  672 	ld	a, (de)
   55F5 4F            [ 4]  673 	ld	c, a
   55F6 AF            [ 4]  674 	xor	a, a
   55F7 91            [ 4]  675 	sub	a, c
   55F8 E2 FD 55      [10]  676 	jp	PO, 00165$
   55FB EE 80         [ 7]  677 	xor	a, #0x80
   55FD                     678 00165$:
   55FD F2 02 56      [10]  679 	jp	P, 00121$
                            680 ;src/entities/enemy.c:107: enemy->vy = 0;
   5600 AF            [ 4]  681 	xor	a, a
   5601 12            [ 7]  682 	ld	(de), a
   5602                     683 00121$:
   5602 DD F9         [10]  684 	ld	sp, ix
   5604 DD E1         [14]  685 	pop	ix
   5606 C9            [10]  686 	ret
                            687 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            688 ;	---------------------------------
                            689 ; Function enemyrender
                            690 ; ---------------------------------
   5607                     691 _enemyrender::
   5607 DD E5         [15]  692 	push	ix
   5609 DD 21 00 00   [14]  693 	ld	ix,#0
   560D DD 39         [15]  694 	add	ix,sp
   560F F5            [11]  695 	push	af
                            696 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5610 DD 7E 05      [19]  697 	ld	a, 5 (ix)
   5613 DD B6 04      [19]  698 	or	a,4 (ix)
   5616 CA 94 56      [10]  699 	jp	Z,00113$
   5619 DD 7E 04      [19]  700 	ld	a, 4 (ix)
   561C DD 77 FE      [19]  701 	ld	-2 (ix), a
   561F DD 7E 05      [19]  702 	ld	a, 5 (ix)
   5622 DD 77 FF      [19]  703 	ld	-1 (ix), a
   5625 E1            [10]  704 	pop	hl
   5626 E5            [11]  705 	push	hl
   5627 11 06 00      [10]  706 	ld	de, #0x0006
   562A 19            [11]  707 	add	hl, de
   562B 7E            [ 7]  708 	ld	a, (hl)
   562C B7            [ 4]  709 	or	a, a
                            710 ;src/entities/enemy.c:116: return;
   562D 28 65         [12]  711 	jr	Z,00113$
                            712 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   562F E1            [10]  713 	pop	hl
   5630 E5            [11]  714 	push	hl
   5631 11 09 00      [10]  715 	ld	de, #0x0009
   5634 19            [11]  716 	add	hl, de
   5635 7E            [ 7]  717 	ld	a, (hl)
   5636 FE 03         [ 7]  718 	cp	a, #0x03
   5638 20 0A         [12]  719 	jr	NZ,00111$
   563A 21 0C 0C      [10]  720 	ld	hl, #0x0c0c
   563D E5            [11]  721 	push	hl
   563E CD 56 5D      [17]  722 	call	_cpct_px2byteM0
   5641 4D            [ 4]  723 	ld	c, l
   5642 18 23         [12]  724 	jr	00112$
   5644                     725 00111$:
                            726 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   5644 FE 02         [ 7]  727 	cp	a, #0x02
   5646 20 0A         [12]  728 	jr	NZ,00108$
   5648 21 0A 0A      [10]  729 	ld	hl, #0x0a0a
   564B E5            [11]  730 	push	hl
   564C CD 56 5D      [17]  731 	call	_cpct_px2byteM0
   564F 4D            [ 4]  732 	ld	c, l
   5650 18 15         [12]  733 	jr	00112$
   5652                     734 00108$:
                            735 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   5652 3D            [ 4]  736 	dec	a
   5653 20 0A         [12]  737 	jr	NZ,00105$
   5655 21 0E 0E      [10]  738 	ld	hl, #0x0e0e
   5658 E5            [11]  739 	push	hl
   5659 CD 56 5D      [17]  740 	call	_cpct_px2byteM0
   565C 4D            [ 4]  741 	ld	c, l
   565D 18 08         [12]  742 	jr	00112$
   565F                     743 00105$:
                            744 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   565F 21 04 04      [10]  745 	ld	hl, #0x0404
   5662 E5            [11]  746 	push	hl
   5663 CD 56 5D      [17]  747 	call	_cpct_px2byteM0
   5666 4D            [ 4]  748 	ld	c, l
   5667                     749 00112$:
                            750 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5667 E1            [10]  751 	pop	hl
   5668 E5            [11]  752 	push	hl
   5669 23            [ 6]  753 	inc	hl
   566A 46            [ 7]  754 	ld	b, (hl)
   566B E1            [10]  755 	pop	hl
   566C E5            [11]  756 	push	hl
   566D 56            [ 7]  757 	ld	d, (hl)
   566E C5            [11]  758 	push	bc
   566F 4A            [ 4]  759 	ld	c, d
   5670 C5            [11]  760 	push	bc
   5671 21 00 C0      [10]  761 	ld	hl, #0xc000
   5674 E5            [11]  762 	push	hl
   5675 CD 49 5E      [17]  763 	call	_cpct_getScreenPtr
   5678 EB            [ 4]  764 	ex	de,hl
   5679 C1            [10]  765 	pop	bc
                            766 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   567A E1            [10]  767 	pop	hl
   567B E5            [11]  768 	push	hl
   567C 23            [ 6]  769 	inc	hl
   567D 23            [ 6]  770 	inc	hl
   567E 23            [ 6]  771 	inc	hl
   567F 23            [ 6]  772 	inc	hl
   5680 23            [ 6]  773 	inc	hl
   5681 46            [ 7]  774 	ld	b, (hl)
   5682 E1            [10]  775 	pop	hl
   5683 E5            [11]  776 	push	hl
   5684 23            [ 6]  777 	inc	hl
   5685 23            [ 6]  778 	inc	hl
   5686 23            [ 6]  779 	inc	hl
   5687 23            [ 6]  780 	inc	hl
   5688 7E            [ 7]  781 	ld	a, (hl)
   5689 C5            [11]  782 	push	bc
   568A 33            [ 6]  783 	inc	sp
   568B 47            [ 4]  784 	ld	b, a
   568C C5            [11]  785 	push	bc
   568D D5            [11]  786 	push	de
   568E CD 90 5D      [17]  787 	call	_cpct_drawSolidBox
   5691 F1            [10]  788 	pop	af
   5692 F1            [10]  789 	pop	af
   5693 33            [ 6]  790 	inc	sp
   5694                     791 00113$:
   5694 DD F9         [10]  792 	ld	sp, ix
   5696 DD E1         [14]  793 	pop	ix
   5698 C9            [10]  794 	ret
                            795 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            796 ;	---------------------------------
                            797 ; Function enemydamage
                            798 ; ---------------------------------
   5699                     799 _enemydamage::
   5699 DD E5         [15]  800 	push	ix
   569B DD 21 00 00   [14]  801 	ld	ix,#0
   569F DD 39         [15]  802 	add	ix,sp
                            803 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   56A1 DD 7E 05      [19]  804 	ld	a, 5 (ix)
   56A4 DD B6 04      [19]  805 	or	a,4 (ix)
   56A7 28 0F         [12]  806 	jr	Z,00101$
   56A9 DD 4E 04      [19]  807 	ld	c,4 (ix)
   56AC DD 46 05      [19]  808 	ld	b,5 (ix)
   56AF 21 06 00      [10]  809 	ld	hl, #0x0006
   56B2 09            [11]  810 	add	hl,bc
   56B3 EB            [ 4]  811 	ex	de,hl
   56B4 1A            [ 7]  812 	ld	a, (de)
   56B5 B7            [ 4]  813 	or	a, a
   56B6 20 04         [12]  814 	jr	NZ,00102$
   56B8                     815 00101$:
                            816 ;src/entities/enemy.c:130: return 0;
   56B8 2E 00         [ 7]  817 	ld	l, #0x00
   56BA 18 1A         [12]  818 	jr	00106$
   56BC                     819 00102$:
                            820 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56BC 21 07 00      [10]  821 	ld	hl, #0x0007
   56BF 09            [11]  822 	add	hl, bc
   56C0 4E            [ 7]  823 	ld	c, (hl)
   56C1 DD 7E 06      [19]  824 	ld	a, 6 (ix)
   56C4 91            [ 4]  825 	sub	a, c
   56C5 38 08         [12]  826 	jr	C,00105$
                            827 ;src/entities/enemy.c:134: enemy->health = 0;
   56C7 36 00         [10]  828 	ld	(hl), #0x00
                            829 ;src/entities/enemy.c:135: enemy->active = 0;
   56C9 AF            [ 4]  830 	xor	a, a
   56CA 12            [ 7]  831 	ld	(de), a
                            832 ;src/entities/enemy.c:136: return 1;
   56CB 2E 01         [ 7]  833 	ld	l, #0x01
   56CD 18 07         [12]  834 	jr	00106$
   56CF                     835 00105$:
                            836 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   56CF 79            [ 4]  837 	ld	a, c
   56D0 DD 96 06      [19]  838 	sub	a, 6 (ix)
   56D3 77            [ 7]  839 	ld	(hl), a
                            840 ;src/entities/enemy.c:140: return 0;
   56D4 2E 00         [ 7]  841 	ld	l, #0x00
   56D6                     842 00106$:
   56D6 DD E1         [14]  843 	pop	ix
   56D8 C9            [10]  844 	ret
                            845 	.area _CODE
                            846 	.area _INITIALIZER
                            847 	.area _CABS (ABS)
