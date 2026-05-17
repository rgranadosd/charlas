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
   51F7                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   51F7 21 03 00      [10]   58 	ld	hl, #2+1
   51FA 39            [11]   59 	add	hl, sp
   51FB 7E            [ 7]   60 	ld	a, (hl)
   51FC 2B            [ 6]   61 	dec	hl
   51FD B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   51FE C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   51FF D1            [10]   66 	pop	de
   5200 C1            [10]   67 	pop	bc
   5201 C5            [11]   68 	push	bc
   5202 D5            [11]   69 	push	de
   5203 AF            [ 4]   70 	xor	a, a
   5204 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   5205 59            [ 4]   73 	ld	e, c
   5206 50            [ 4]   74 	ld	d, b
   5207 13            [ 6]   75 	inc	de
   5208 AF            [ 4]   76 	xor	a, a
   5209 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   520A 59            [ 4]   79 	ld	e, c
   520B 50            [ 4]   80 	ld	d, b
   520C 13            [ 6]   81 	inc	de
   520D 13            [ 6]   82 	inc	de
   520E AF            [ 4]   83 	xor	a, a
   520F 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   5210 59            [ 4]   86 	ld	e, c
   5211 50            [ 4]   87 	ld	d, b
   5212 13            [ 6]   88 	inc	de
   5213 13            [ 6]   89 	inc	de
   5214 13            [ 6]   90 	inc	de
   5215 AF            [ 4]   91 	xor	a, a
   5216 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   5217 21 04 00      [10]   94 	ld	hl, #0x0004
   521A 09            [11]   95 	add	hl, bc
   521B 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   521D 21 05 00      [10]   98 	ld	hl, #0x0005
   5220 09            [11]   99 	add	hl, bc
   5221 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5223 21 06 00      [10]  102 	ld	hl, #0x0006
   5226 09            [11]  103 	add	hl, bc
   5227 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   5229 21 07 00      [10]  106 	ld	hl, #0x0007
   522C 09            [11]  107 	add	hl, bc
   522D 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   522F 21 08 00      [10]  110 	ld	hl, #0x0008
   5232 09            [11]  111 	add	hl, bc
   5233 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   5235 21 09 00      [10]  114 	ld	hl, #0x0009
   5238 09            [11]  115 	add	hl, bc
   5239 36 00         [10]  116 	ld	(hl), #0x00
   523B C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   523C                     122 _enemyspawn::
   523C DD E5         [15]  123 	push	ix
   523E DD 21 00 00   [14]  124 	ld	ix,#0
   5242 DD 39         [15]  125 	add	ix,sp
   5244 21 F1 FF      [10]  126 	ld	hl, #-15
   5247 39            [11]  127 	add	hl, sp
   5248 F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   5249 DD 7E 05      [19]  130 	ld	a, 5 (ix)
   524C DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   524F CA 0F 54      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   5252 DD 7E 04      [19]  135 	ld	a, 4 (ix)
   5255 DD 77 FE      [19]  136 	ld	-2 (ix), a
   5258 DD 7E 05      [19]  137 	ld	a, 5 (ix)
   525B DD 77 FF      [19]  138 	ld	-1 (ix), a
   525E DD 6E FE      [19]  139 	ld	l,-2 (ix)
   5261 DD 66 FF      [19]  140 	ld	h,-1 (ix)
   5264 DD 7E 06      [19]  141 	ld	a, 6 (ix)
   5267 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   5268 DD 4E FE      [19]  144 	ld	c,-2 (ix)
   526B DD 46 FF      [19]  145 	ld	b,-1 (ix)
   526E 03            [ 6]  146 	inc	bc
   526F DD 7E 07      [19]  147 	ld	a, 7 (ix)
   5272 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   5273 DD 7E FE      [19]  150 	ld	a, -2 (ix)
   5276 C6 02         [ 7]  151 	add	a, #0x02
   5278 DD 77 FC      [19]  152 	ld	-4 (ix), a
   527B DD 7E FF      [19]  153 	ld	a, -1 (ix)
   527E CE 00         [ 7]  154 	adc	a, #0x00
   5280 DD 77 FD      [19]  155 	ld	-3 (ix), a
   5283 DD 7E 09      [19]  156 	ld	a, 9 (ix)
   5286 B7            [ 4]  157 	or	a, a
   5287 28 04         [12]  158 	jr	Z,00114$
   5289 0E 01         [ 7]  159 	ld	c, #0x01
   528B 18 02         [12]  160 	jr	00115$
   528D                     161 00114$:
   528D 0E FF         [ 7]  162 	ld	c, #0xff
   528F                     163 00115$:
   528F DD 6E FC      [19]  164 	ld	l,-4 (ix)
   5292 DD 66 FD      [19]  165 	ld	h,-3 (ix)
   5295 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   5296 DD 7E FE      [19]  168 	ld	a, -2 (ix)
   5299 C6 03         [ 7]  169 	add	a, #0x03
   529B DD 77 FA      [19]  170 	ld	-6 (ix), a
   529E DD 7E FF      [19]  171 	ld	a, -1 (ix)
   52A1 CE 00         [ 7]  172 	adc	a, #0x00
   52A3 DD 77 FB      [19]  173 	ld	-5 (ix), a
   52A6 DD 6E FA      [19]  174 	ld	l,-6 (ix)
   52A9 DD 66 FB      [19]  175 	ld	h,-5 (ix)
   52AC 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   52AE DD 7E FE      [19]  178 	ld	a, -2 (ix)
   52B1 C6 06         [ 7]  179 	add	a, #0x06
   52B3 DD 77 F8      [19]  180 	ld	-8 (ix), a
   52B6 DD 7E FF      [19]  181 	ld	a, -1 (ix)
   52B9 CE 00         [ 7]  182 	adc	a, #0x00
   52BB DD 77 F9      [19]  183 	ld	-7 (ix), a
   52BE DD 6E F8      [19]  184 	ld	l,-8 (ix)
   52C1 DD 66 F9      [19]  185 	ld	h,-7 (ix)
   52C4 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52C6 DD 7E FE      [19]  188 	ld	a, -2 (ix)
   52C9 C6 09         [ 7]  189 	add	a, #0x09
   52CB DD 77 F8      [19]  190 	ld	-8 (ix), a
   52CE DD 7E FF      [19]  191 	ld	a, -1 (ix)
   52D1 CE 00         [ 7]  192 	adc	a, #0x00
   52D3 DD 77 F9      [19]  193 	ld	-7 (ix), a
   52D6 DD 6E F8      [19]  194 	ld	l,-8 (ix)
   52D9 DD 66 F9      [19]  195 	ld	h,-7 (ix)
   52DC DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52DF 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52E0 DD 7E FE      [19]  199 	ld	a, -2 (ix)
   52E3 C6 04         [ 7]  200 	add	a, #0x04
   52E5 DD 77 F8      [19]  201 	ld	-8 (ix), a
   52E8 DD 7E FF      [19]  202 	ld	a, -1 (ix)
   52EB CE 00         [ 7]  203 	adc	a, #0x00
   52ED DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52F0 DD 7E FE      [19]  206 	ld	a, -2 (ix)
   52F3 C6 05         [ 7]  207 	add	a, #0x05
   52F5 DD 77 F6      [19]  208 	ld	-10 (ix), a
   52F8 DD 7E FF      [19]  209 	ld	a, -1 (ix)
   52FB CE 00         [ 7]  210 	adc	a, #0x00
   52FD DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   5300 DD 7E FE      [19]  213 	ld	a, -2 (ix)
   5303 C6 07         [ 7]  214 	add	a, #0x07
   5305 DD 77 F4      [19]  215 	ld	-12 (ix), a
   5308 DD 7E FF      [19]  216 	ld	a, -1 (ix)
   530B CE 00         [ 7]  217 	adc	a, #0x00
   530D DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   5310 DD 7E FE      [19]  220 	ld	a, -2 (ix)
   5313 C6 08         [ 7]  221 	add	a, #0x08
   5315 DD 77 FE      [19]  222 	ld	-2 (ix), a
   5318 DD 7E FF      [19]  223 	ld	a, -1 (ix)
   531B CE 00         [ 7]  224 	adc	a, #0x00
   531D DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   5320 DD 7E 08      [19]  227 	ld	a, 8 (ix)
   5323 3D            [ 4]  228 	dec	a
   5324 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   5326 DD 6E F8      [19]  231 	ld	l,-8 (ix)
   5329 DD 66 F9      [19]  232 	ld	h,-7 (ix)
   532C 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   532E DD 6E F6      [19]  235 	ld	l,-10 (ix)
   5331 DD 66 F7      [19]  236 	ld	h,-9 (ix)
   5334 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   5336 DD 6E F4      [19]  239 	ld	l,-12 (ix)
   5339 DD 66 F5      [19]  240 	ld	h,-11 (ix)
   533C 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   533E DD 6E FE      [19]  243 	ld	l,-2 (ix)
   5341 DD 66 FF      [19]  244 	ld	h,-1 (ix)
   5344 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   5346 DD 7E FC      [19]  247 	ld	a, -4 (ix)
   5349 DD 77 F2      [19]  248 	ld	-14 (ix), a
   534C DD 7E FD      [19]  249 	ld	a, -3 (ix)
   534F DD 77 F3      [19]  250 	ld	-13 (ix), a
   5352 DD 7E 09      [19]  251 	ld	a, 9 (ix)
   5355 B7            [ 4]  252 	or	a, a
   5356 28 06         [12]  253 	jr	Z,00116$
   5358 DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   535C 18 04         [12]  255 	jr	00117$
   535E                     256 00116$:
   535E DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   5362                     258 00117$:
   5362 DD 6E F2      [19]  259 	ld	l,-14 (ix)
   5365 DD 66 F3      [19]  260 	ld	h,-13 (ix)
   5368 DD 7E F1      [19]  261 	ld	a, -15 (ix)
   536B 77            [ 7]  262 	ld	(hl), a
   536C C3 0F 54      [10]  263 	jp	00112$
   536F                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   536F DD 7E 08      [19]  266 	ld	a, 8 (ix)
   5372 D6 02         [ 7]  267 	sub	a, #0x02
   5374 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   5376 DD 6E F8      [19]  270 	ld	l,-8 (ix)
   5379 DD 66 F9      [19]  271 	ld	h,-7 (ix)
   537C 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   537E DD 6E F6      [19]  274 	ld	l,-10 (ix)
   5381 DD 66 F7      [19]  275 	ld	h,-9 (ix)
   5384 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   5386 DD 6E F4      [19]  278 	ld	l,-12 (ix)
   5389 DD 66 F5      [19]  279 	ld	h,-11 (ix)
   538C 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   538E DD 6E FE      [19]  282 	ld	l,-2 (ix)
   5391 DD 66 FF      [19]  283 	ld	h,-1 (ix)
   5394 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5396 DD 4E FA      [19]  286 	ld	c,-6 (ix)
   5399 DD 46 FB      [19]  287 	ld	b,-5 (ix)
   539C DD 7E 09      [19]  288 	ld	a, 9 (ix)
   539F B7            [ 4]  289 	or	a, a
   53A0 28 04         [12]  290 	jr	Z,00118$
   53A2 3E 01         [ 7]  291 	ld	a, #0x01
   53A4 18 02         [12]  292 	jr	00119$
   53A6                     293 00118$:
   53A6 3E FF         [ 7]  294 	ld	a, #0xff
   53A8                     295 00119$:
   53A8 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   53A9 DD 6E FC      [19]  298 	ld	l,-4 (ix)
   53AC DD 66 FD      [19]  299 	ld	h,-3 (ix)
   53AF 36 01         [10]  300 	ld	(hl), #0x01
   53B1 18 5C         [12]  301 	jr	00112$
   53B3                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   53B3 DD 7E 08      [19]  304 	ld	a, 8 (ix)
   53B6 D6 03         [ 7]  305 	sub	a, #0x03
   53B8 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   53BA DD 6E F8      [19]  308 	ld	l,-8 (ix)
   53BD DD 66 F9      [19]  309 	ld	h,-7 (ix)
   53C0 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   53C2 DD 6E F6      [19]  312 	ld	l,-10 (ix)
   53C5 DD 66 F7      [19]  313 	ld	h,-9 (ix)
   53C8 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53CA DD 6E F4      [19]  316 	ld	l,-12 (ix)
   53CD DD 66 F5      [19]  317 	ld	h,-11 (ix)
   53D0 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53D2 DD 6E FE      [19]  320 	ld	l,-2 (ix)
   53D5 DD 66 FF      [19]  321 	ld	h,-1 (ix)
   53D8 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53DA DD 4E FC      [19]  324 	ld	c,-4 (ix)
   53DD DD 46 FD      [19]  325 	ld	b,-3 (ix)
   53E0 DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53E3 B7            [ 4]  327 	or	a, a
   53E4 28 04         [12]  328 	jr	Z,00120$
   53E6 3E 01         [ 7]  329 	ld	a, #0x01
   53E8 18 02         [12]  330 	jr	00121$
   53EA                     331 00120$:
   53EA 3E FF         [ 7]  332 	ld	a, #0xff
   53EC                     333 00121$:
   53EC 02            [ 7]  334 	ld	(bc), a
   53ED 18 20         [12]  335 	jr	00112$
   53EF                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53EF DD 6E F8      [19]  338 	ld	l,-8 (ix)
   53F2 DD 66 F9      [19]  339 	ld	h,-7 (ix)
   53F5 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   53F7 DD 6E F6      [19]  342 	ld	l,-10 (ix)
   53FA DD 66 F7      [19]  343 	ld	h,-9 (ix)
   53FD 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   53FF DD 6E F4      [19]  346 	ld	l,-12 (ix)
   5402 DD 66 F5      [19]  347 	ld	h,-11 (ix)
   5405 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   5407 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   540A DD 66 FF      [19]  351 	ld	h,-1 (ix)
   540D 36 64         [10]  352 	ld	(hl), #0x64
   540F                     353 00112$:
   540F DD F9         [10]  354 	ld	sp, ix
   5411 DD E1         [14]  355 	pop	ix
   5413 C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   5414                     361 _enemyupdate::
   5414 DD E5         [15]  362 	push	ix
   5416 DD 21 00 00   [14]  363 	ld	ix,#0
   541A DD 39         [15]  364 	add	ix,sp
   541C 21 F6 FF      [10]  365 	ld	hl, #-10
   541F 39            [11]  366 	add	hl, sp
   5420 F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   5421 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   5424 DD B6 04      [19]  370 	or	a,4 (ix)
   5427 CA 1B 56      [10]  371 	jp	Z,00121$
   542A DD 7E 04      [19]  372 	ld	a, 4 (ix)
   542D DD 77 FE      [19]  373 	ld	-2 (ix), a
   5430 DD 7E 05      [19]  374 	ld	a, 5 (ix)
   5433 DD 77 FF      [19]  375 	ld	-1 (ix), a
   5436 DD 6E FE      [19]  376 	ld	l,-2 (ix)
   5439 DD 66 FF      [19]  377 	ld	h,-1 (ix)
   543C 11 06 00      [10]  378 	ld	de, #0x0006
   543F 19            [11]  379 	add	hl, de
   5440 7E            [ 7]  380 	ld	a, (hl)
   5441 B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   5442 CA 1B 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5445 DD 6E FE      [19]  385 	ld	l,-2 (ix)
   5448 DD 66 FF      [19]  386 	ld	h,-1 (ix)
   544B 11 09 00      [10]  387 	ld	de, #0x0009
   544E 19            [11]  388 	add	hl, de
   544F 7E            [ 7]  389 	ld	a, (hl)
   5450 DD 77 FD      [19]  390 	ld	-3 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5453 DD 6E FE      [19]  392 	ld	l,-2 (ix)
   5456 DD 66 FF      [19]  393 	ld	h,-1 (ix)
   5459 4E            [ 7]  394 	ld	c, (hl)
   545A DD 7E FE      [19]  395 	ld	a, -2 (ix)
   545D C6 02         [ 7]  396 	add	a, #0x02
   545F DD 77 FB      [19]  397 	ld	-5 (ix), a
   5462 DD 7E FF      [19]  398 	ld	a, -1 (ix)
   5465 CE 00         [ 7]  399 	adc	a, #0x00
   5467 DD 77 FC      [19]  400 	ld	-4 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   546A DD 7E FE      [19]  402 	ld	a, -2 (ix)
   546D C6 01         [ 7]  403 	add	a, #0x01
   546F DD 77 F9      [19]  404 	ld	-7 (ix), a
   5472 DD 7E FF      [19]  405 	ld	a, -1 (ix)
   5475 CE 00         [ 7]  406 	adc	a, #0x00
   5477 DD 77 FA      [19]  407 	ld	-6 (ix), a
   547A DD 5E FE      [19]  408 	ld	e,-2 (ix)
   547D DD 56 FF      [19]  409 	ld	d,-1 (ix)
   5480 13            [ 6]  410 	inc	de
   5481 13            [ 6]  411 	inc	de
   5482 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5483 06 00         [ 7]  414 	ld	b, #0x00
   5485 DD 6E FB      [19]  415 	ld	l,-5 (ix)
   5488 DD 66 FC      [19]  416 	ld	h,-4 (ix)
   548B 7E            [ 7]  417 	ld	a, (hl)
   548C DD 77 F8      [19]  418 	ld	-8 (ix), a
   548F 6F            [ 4]  419 	ld	l, a
   5490 DD 7E F8      [19]  420 	ld	a, -8 (ix)
   5493 17            [ 4]  421 	rla
   5494 9F            [ 4]  422 	sbc	a, a
   5495 67            [ 4]  423 	ld	h, a
   5496 09            [11]  424 	add	hl,bc
   5497 4D            [ 4]  425 	ld	c, l
   5498 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5499 DD 7E FD      [19]  428 	ld	a, -3 (ix)
   549C D6 02         [ 7]  429 	sub	a, #0x02
   549E C2 47 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   54A1 DD 6E F9      [19]  433 	ld	l,-7 (ix)
   54A4 DD 66 FA      [19]  434 	ld	h,-6 (ix)
   54A7 6E            [ 7]  435 	ld	l, (hl)
   54A8 DD 75 F6      [19]  436 	ld	-10 (ix), l
   54AB DD 36 F7 00   [19]  437 	ld	-9 (ix), #0x00
   54AF 1A            [ 7]  438 	ld	a, (de)
   54B0 6F            [ 4]  439 	ld	l, a
   54B1 17            [ 4]  440 	rla
   54B2 9F            [ 4]  441 	sbc	a, a
   54B3 67            [ 4]  442 	ld	h, a
   54B4 DD 7E F6      [19]  443 	ld	a, -10 (ix)
   54B7 85            [ 4]  444 	add	a, l
   54B8 DD 77 F6      [19]  445 	ld	-10 (ix), a
   54BB DD 7E F7      [19]  446 	ld	a, -9 (ix)
   54BE 8C            [ 4]  447 	adc	a, h
   54BF DD 77 F7      [19]  448 	ld	-9 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   54C2 79            [ 4]  450 	ld	a, c
   54C3 D6 08         [ 7]  451 	sub	a, #0x08
   54C5 78            [ 4]  452 	ld	a, b
   54C6 17            [ 4]  453 	rla
   54C7 3F            [ 4]  454 	ccf
   54C8 1F            [ 4]  455 	rra
   54C9 DE 80         [ 7]  456 	sbc	a, #0x80
   54CB 38 0E         [12]  457 	jr	C,00104$
   54CD 3E 48         [ 7]  458 	ld	a, #0x48
   54CF B9            [ 4]  459 	cp	a, c
   54D0 3E 00         [ 7]  460 	ld	a, #0x00
   54D2 98            [ 4]  461 	sbc	a, b
   54D3 E2 D8 54      [10]  462 	jp	PO, 00161$
   54D6 EE 80         [ 7]  463 	xor	a, #0x80
   54D8                     464 00161$:
   54D8 F2 F6 54      [10]  465 	jp	P, 00105$
   54DB                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   54DB AF            [ 4]  468 	xor	a, a
   54DC DD 96 F8      [19]  469 	sub	a, -8 (ix)
   54DF 4F            [ 4]  470 	ld	c, a
   54E0 DD 6E FB      [19]  471 	ld	l,-5 (ix)
   54E3 DD 66 FC      [19]  472 	ld	h,-4 (ix)
   54E6 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54E7 DD 6E FE      [19]  475 	ld	l,-2 (ix)
   54EA DD 66 FF      [19]  476 	ld	h,-1 (ix)
   54ED 6E            [ 7]  477 	ld	l, (hl)
   54EE 26 00         [ 7]  478 	ld	h, #0x00
   54F0 79            [ 4]  479 	ld	a, c
   54F1 17            [ 4]  480 	rla
   54F2 9F            [ 4]  481 	sbc	a, a
   54F3 47            [ 4]  482 	ld	b, a
   54F4 09            [11]  483 	add	hl,bc
   54F5 4D            [ 4]  484 	ld	c, l
   54F6                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   54F6 DD 7E F6      [19]  487 	ld	a, -10 (ix)
   54F9 D6 38         [ 7]  488 	sub	a, #0x38
   54FB DD 7E F7      [19]  489 	ld	a, -9 (ix)
   54FE 17            [ 4]  490 	rla
   54FF 3F            [ 4]  491 	ccf
   5500 1F            [ 4]  492 	rra
   5501 DE 80         [ 7]  493 	sbc	a, #0x80
   5503 38 12         [12]  494 	jr	C,00107$
   5505 3E 78         [ 7]  495 	ld	a, #0x78
   5507 DD BE F6      [19]  496 	cp	a, -10 (ix)
   550A 3E 00         [ 7]  497 	ld	a, #0x00
   550C DD 9E F7      [19]  498 	sbc	a, -9 (ix)
   550F E2 14 55      [10]  499 	jp	PO, 00162$
   5512 EE 80         [ 7]  500 	xor	a, #0x80
   5514                     501 00162$:
   5514 F2 33 55      [10]  502 	jp	P, 00108$
   5517                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5517 1A            [ 7]  505 	ld	a, (de)
   5518 6F            [ 4]  506 	ld	l, a
   5519 AF            [ 4]  507 	xor	a, a
   551A 95            [ 4]  508 	sub	a, l
   551B DD 77 F8      [19]  509 	ld	-8 (ix), a
   551E 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   551F DD 6E F9      [19]  512 	ld	l,-7 (ix)
   5522 DD 66 FA      [19]  513 	ld	h,-6 (ix)
   5525 5E            [ 7]  514 	ld	e, (hl)
   5526 16 00         [ 7]  515 	ld	d, #0x00
   5528 DD 6E F8      [19]  516 	ld	l, -8 (ix)
   552B DD 7E F8      [19]  517 	ld	a, -8 (ix)
   552E 17            [ 4]  518 	rla
   552F 9F            [ 4]  519 	sbc	a, a
   5530 67            [ 4]  520 	ld	h, a
   5531 19            [11]  521 	add	hl,de
   5532 E3            [19]  522 	ex	(sp), hl
   5533                     523 00108$:
                            524 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   5533 DD 6E FE      [19]  525 	ld	l,-2 (ix)
   5536 DD 66 FF      [19]  526 	ld	h,-1 (ix)
   5539 71            [ 7]  527 	ld	(hl), c
                            528 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   553A DD 4E F6      [19]  529 	ld	c, -10 (ix)
   553D DD 6E F9      [19]  530 	ld	l,-7 (ix)
   5540 DD 66 FA      [19]  531 	ld	h,-6 (ix)
   5543 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:84: return;
   5544 C3 1B 56      [10]  534 	jp	00121$
   5547                     535 00111$:
                            536 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            537 ;src/entities/enemy.c:88: if (nextx < 2) {
   5547 79            [ 4]  538 	ld	a, c
   5548 D6 02         [ 7]  539 	sub	a, #0x02
   554A 78            [ 4]  540 	ld	a, b
   554B 17            [ 4]  541 	rla
   554C 3F            [ 4]  542 	ccf
   554D 1F            [ 4]  543 	rra
   554E DE 80         [ 7]  544 	sbc	a, #0x80
   5550 30 0B         [12]  545 	jr	NC,00113$
                            546 ;src/entities/enemy.c:89: nextx = 2;
   5552 01 02 00      [10]  547 	ld	bc, #0x0002
                            548 ;src/entities/enemy.c:90: enemy->vx = 1;
   5555 DD 6E FB      [19]  549 	ld	l,-5 (ix)
   5558 DD 66 FC      [19]  550 	ld	h,-4 (ix)
   555B 36 01         [10]  551 	ld	(hl), #0x01
   555D                     552 00113$:
                            553 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   555D DD 6E FE      [19]  554 	ld	l,-2 (ix)
   5560 DD 66 FF      [19]  555 	ld	h,-1 (ix)
   5563 23            [ 6]  556 	inc	hl
   5564 23            [ 6]  557 	inc	hl
   5565 23            [ 6]  558 	inc	hl
   5566 23            [ 6]  559 	inc	hl
   5567 6E            [ 7]  560 	ld	l, (hl)
   5568 26 00         [ 7]  561 	ld	h, #0x00
   556A 3E 50         [ 7]  562 	ld	a, #0x50
   556C 95            [ 4]  563 	sub	a, l
   556D 6F            [ 4]  564 	ld	l, a
   556E 3E 00         [ 7]  565 	ld	a, #0x00
   5570 9C            [ 4]  566 	sbc	a, h
   5571 67            [ 4]  567 	ld	h, a
                            568 ;src/entities/enemy.c:94: if (nextx > maxx) {
   5572 7D            [ 4]  569 	ld	a, l
   5573 91            [ 4]  570 	sub	a, c
   5574 7C            [ 4]  571 	ld	a, h
   5575 98            [ 4]  572 	sbc	a, b
   5576 E2 7B 55      [10]  573 	jp	PO, 00163$
   5579 EE 80         [ 7]  574 	xor	a, #0x80
   557B                     575 00163$:
   557B F2 87 55      [10]  576 	jp	P, 00115$
                            577 ;src/entities/enemy.c:95: nextx = maxx;
   557E 4D            [ 4]  578 	ld	c, l
                            579 ;src/entities/enemy.c:96: enemy->vx = -1;
   557F DD 6E FB      [19]  580 	ld	l,-5 (ix)
   5582 DD 66 FC      [19]  581 	ld	h,-4 (ix)
   5585 36 FF         [10]  582 	ld	(hl), #0xff
   5587                     583 00115$:
                            584 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   5587 DD 6E FE      [19]  585 	ld	l,-2 (ix)
   558A DD 66 FF      [19]  586 	ld	h,-1 (ix)
   558D 71            [ 7]  587 	ld	(hl), c
                            588 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   558E 1A            [ 7]  589 	ld	a, (de)
   558F 4F            [ 4]  590 	ld	c, a
   5590 0C            [ 4]  591 	inc	c
   5591 79            [ 4]  592 	ld	a, c
   5592 12            [ 7]  593 	ld	(de), a
                            594 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   5593 3E 03         [ 7]  595 	ld	a, #0x03
   5595 91            [ 4]  596 	sub	a, c
   5596 E2 9B 55      [10]  597 	jp	PO, 00164$
   5599 EE 80         [ 7]  598 	xor	a, #0x80
   559B                     599 00164$:
   559B F2 A1 55      [10]  600 	jp	P, 00117$
   559E 3E 03         [ 7]  601 	ld	a, #0x03
   55A0 12            [ 7]  602 	ld	(de), a
   55A1                     603 00117$:
                            604 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   55A1 DD 6E F9      [19]  605 	ld	l,-7 (ix)
   55A4 DD 66 FA      [19]  606 	ld	h,-6 (ix)
   55A7 4E            [ 7]  607 	ld	c, (hl)
   55A8 06 00         [ 7]  608 	ld	b, #0x00
   55AA 1A            [ 7]  609 	ld	a, (de)
   55AB 6F            [ 4]  610 	ld	l, a
   55AC 17            [ 4]  611 	rla
   55AD 9F            [ 4]  612 	sbc	a, a
   55AE 67            [ 4]  613 	ld	h, a
   55AF 09            [11]  614 	add	hl, bc
   55B0 E5            [11]  615 	push	hl
   55B1 FD E1         [14]  616 	pop	iy
                            617 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   55B3 DD 7E FE      [19]  618 	ld	a, -2 (ix)
   55B6 C6 05         [ 7]  619 	add	a, #0x05
   55B8 DD 77 F6      [19]  620 	ld	-10 (ix), a
   55BB DD 7E FF      [19]  621 	ld	a, -1 (ix)
   55BE CE 00         [ 7]  622 	adc	a, #0x00
   55C0 DD 77 F7      [19]  623 	ld	-9 (ix), a
   55C3 E1            [10]  624 	pop	hl
   55C4 E5            [11]  625 	push	hl
   55C5 7E            [ 7]  626 	ld	a, (hl)
   55C6 DD 6E FE      [19]  627 	ld	l,-2 (ix)
   55C9 DD 66 FF      [19]  628 	ld	h,-1 (ix)
   55CC 4E            [ 7]  629 	ld	c, (hl)
   55CD 06 00         [ 7]  630 	ld	b, #0x00
   55CF D5            [11]  631 	push	de
   55D0 F5            [11]  632 	push	af
   55D1 33            [ 6]  633 	inc	sp
   55D2 FD E5         [15]  634 	push	iy
   55D4 C5            [11]  635 	push	bc
   55D5 CD 40 4C      [17]  636 	call	_collision_clamp_y_at
   55D8 F1            [10]  637 	pop	af
   55D9 F1            [10]  638 	pop	af
   55DA 33            [ 6]  639 	inc	sp
   55DB 4D            [ 4]  640 	ld	c, l
   55DC D1            [10]  641 	pop	de
                            642 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55DD DD 6E F9      [19]  643 	ld	l,-7 (ix)
   55E0 DD 66 FA      [19]  644 	ld	h,-6 (ix)
   55E3 71            [ 7]  645 	ld	(hl), c
                            646 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55E4 E1            [10]  647 	pop	hl
   55E5 E5            [11]  648 	push	hl
   55E6 7E            [ 7]  649 	ld	a, (hl)
   55E7 06 00         [ 7]  650 	ld	b, #0x00
   55E9 DD 6E FE      [19]  651 	ld	l,-2 (ix)
   55EC DD 66 FF      [19]  652 	ld	h,-1 (ix)
   55EF 6E            [ 7]  653 	ld	l, (hl)
   55F0 DD 75 F6      [19]  654 	ld	-10 (ix), l
   55F3 DD 36 F7 00   [19]  655 	ld	-9 (ix), #0x00
   55F7 D5            [11]  656 	push	de
   55F8 F5            [11]  657 	push	af
   55F9 33            [ 6]  658 	inc	sp
   55FA C5            [11]  659 	push	bc
   55FB DD 6E F6      [19]  660 	ld	l,-10 (ix)
   55FE DD 66 F7      [19]  661 	ld	h,-9 (ix)
   5601 E5            [11]  662 	push	hl
   5602 CD C1 4B      [17]  663 	call	_collision_is_on_ground_at
   5605 F1            [10]  664 	pop	af
   5606 F1            [10]  665 	pop	af
   5607 33            [ 6]  666 	inc	sp
   5608 D1            [10]  667 	pop	de
   5609 7D            [ 4]  668 	ld	a, l
   560A B7            [ 4]  669 	or	a, a
   560B 28 0E         [12]  670 	jr	Z,00121$
   560D 1A            [ 7]  671 	ld	a, (de)
   560E 4F            [ 4]  672 	ld	c, a
   560F AF            [ 4]  673 	xor	a, a
   5610 91            [ 4]  674 	sub	a, c
   5611 E2 16 56      [10]  675 	jp	PO, 00165$
   5614 EE 80         [ 7]  676 	xor	a, #0x80
   5616                     677 00165$:
   5616 F2 1B 56      [10]  678 	jp	P, 00121$
                            679 ;src/entities/enemy.c:107: enemy->vy = 0;
   5619 AF            [ 4]  680 	xor	a, a
   561A 12            [ 7]  681 	ld	(de), a
   561B                     682 00121$:
   561B DD F9         [10]  683 	ld	sp, ix
   561D DD E1         [14]  684 	pop	ix
   561F C9            [10]  685 	ret
                            686 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            687 ;	---------------------------------
                            688 ; Function enemyrender
                            689 ; ---------------------------------
   5620                     690 _enemyrender::
   5620 DD E5         [15]  691 	push	ix
   5622 DD 21 00 00   [14]  692 	ld	ix,#0
   5626 DD 39         [15]  693 	add	ix,sp
   5628 F5            [11]  694 	push	af
                            695 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5629 DD 7E 05      [19]  696 	ld	a, 5 (ix)
   562C DD B6 04      [19]  697 	or	a,4 (ix)
   562F CA AD 56      [10]  698 	jp	Z,00113$
   5632 DD 7E 04      [19]  699 	ld	a, 4 (ix)
   5635 DD 77 FE      [19]  700 	ld	-2 (ix), a
   5638 DD 7E 05      [19]  701 	ld	a, 5 (ix)
   563B DD 77 FF      [19]  702 	ld	-1 (ix), a
   563E E1            [10]  703 	pop	hl
   563F E5            [11]  704 	push	hl
   5640 11 06 00      [10]  705 	ld	de, #0x0006
   5643 19            [11]  706 	add	hl, de
   5644 7E            [ 7]  707 	ld	a, (hl)
   5645 B7            [ 4]  708 	or	a, a
                            709 ;src/entities/enemy.c:116: return;
   5646 28 65         [12]  710 	jr	Z,00113$
                            711 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   5648 E1            [10]  712 	pop	hl
   5649 E5            [11]  713 	push	hl
   564A 11 09 00      [10]  714 	ld	de, #0x0009
   564D 19            [11]  715 	add	hl, de
   564E 7E            [ 7]  716 	ld	a, (hl)
   564F FE 03         [ 7]  717 	cp	a, #0x03
   5651 20 0A         [12]  718 	jr	NZ,00111$
   5653 21 0C 0C      [10]  719 	ld	hl, #0x0c0c
   5656 E5            [11]  720 	push	hl
   5657 CD 6F 5D      [17]  721 	call	_cpct_px2byteM0
   565A 4D            [ 4]  722 	ld	c, l
   565B 18 23         [12]  723 	jr	00112$
   565D                     724 00111$:
                            725 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   565D FE 02         [ 7]  726 	cp	a, #0x02
   565F 20 0A         [12]  727 	jr	NZ,00108$
   5661 21 0A 0A      [10]  728 	ld	hl, #0x0a0a
   5664 E5            [11]  729 	push	hl
   5665 CD 6F 5D      [17]  730 	call	_cpct_px2byteM0
   5668 4D            [ 4]  731 	ld	c, l
   5669 18 15         [12]  732 	jr	00112$
   566B                     733 00108$:
                            734 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   566B 3D            [ 4]  735 	dec	a
   566C 20 0A         [12]  736 	jr	NZ,00105$
   566E 21 0E 0E      [10]  737 	ld	hl, #0x0e0e
   5671 E5            [11]  738 	push	hl
   5672 CD 6F 5D      [17]  739 	call	_cpct_px2byteM0
   5675 4D            [ 4]  740 	ld	c, l
   5676 18 08         [12]  741 	jr	00112$
   5678                     742 00105$:
                            743 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   5678 21 04 04      [10]  744 	ld	hl, #0x0404
   567B E5            [11]  745 	push	hl
   567C CD 6F 5D      [17]  746 	call	_cpct_px2byteM0
   567F 4D            [ 4]  747 	ld	c, l
   5680                     748 00112$:
                            749 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5680 E1            [10]  750 	pop	hl
   5681 E5            [11]  751 	push	hl
   5682 23            [ 6]  752 	inc	hl
   5683 46            [ 7]  753 	ld	b, (hl)
   5684 E1            [10]  754 	pop	hl
   5685 E5            [11]  755 	push	hl
   5686 56            [ 7]  756 	ld	d, (hl)
   5687 C5            [11]  757 	push	bc
   5688 4A            [ 4]  758 	ld	c, d
   5689 C5            [11]  759 	push	bc
   568A 21 00 C0      [10]  760 	ld	hl, #0xc000
   568D E5            [11]  761 	push	hl
   568E CD 62 5E      [17]  762 	call	_cpct_getScreenPtr
   5691 EB            [ 4]  763 	ex	de,hl
   5692 C1            [10]  764 	pop	bc
                            765 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   5693 E1            [10]  766 	pop	hl
   5694 E5            [11]  767 	push	hl
   5695 23            [ 6]  768 	inc	hl
   5696 23            [ 6]  769 	inc	hl
   5697 23            [ 6]  770 	inc	hl
   5698 23            [ 6]  771 	inc	hl
   5699 23            [ 6]  772 	inc	hl
   569A 46            [ 7]  773 	ld	b, (hl)
   569B E1            [10]  774 	pop	hl
   569C E5            [11]  775 	push	hl
   569D 23            [ 6]  776 	inc	hl
   569E 23            [ 6]  777 	inc	hl
   569F 23            [ 6]  778 	inc	hl
   56A0 23            [ 6]  779 	inc	hl
   56A1 7E            [ 7]  780 	ld	a, (hl)
   56A2 C5            [11]  781 	push	bc
   56A3 33            [ 6]  782 	inc	sp
   56A4 47            [ 4]  783 	ld	b, a
   56A5 C5            [11]  784 	push	bc
   56A6 D5            [11]  785 	push	de
   56A7 CD A9 5D      [17]  786 	call	_cpct_drawSolidBox
   56AA F1            [10]  787 	pop	af
   56AB F1            [10]  788 	pop	af
   56AC 33            [ 6]  789 	inc	sp
   56AD                     790 00113$:
   56AD DD F9         [10]  791 	ld	sp, ix
   56AF DD E1         [14]  792 	pop	ix
   56B1 C9            [10]  793 	ret
                            794 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            795 ;	---------------------------------
                            796 ; Function enemydamage
                            797 ; ---------------------------------
   56B2                     798 _enemydamage::
   56B2 DD E5         [15]  799 	push	ix
   56B4 DD 21 00 00   [14]  800 	ld	ix,#0
   56B8 DD 39         [15]  801 	add	ix,sp
                            802 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   56BA DD 7E 05      [19]  803 	ld	a, 5 (ix)
   56BD DD B6 04      [19]  804 	or	a,4 (ix)
   56C0 28 0F         [12]  805 	jr	Z,00101$
   56C2 DD 4E 04      [19]  806 	ld	c,4 (ix)
   56C5 DD 46 05      [19]  807 	ld	b,5 (ix)
   56C8 21 06 00      [10]  808 	ld	hl, #0x0006
   56CB 09            [11]  809 	add	hl,bc
   56CC EB            [ 4]  810 	ex	de,hl
   56CD 1A            [ 7]  811 	ld	a, (de)
   56CE B7            [ 4]  812 	or	a, a
   56CF 20 04         [12]  813 	jr	NZ,00102$
   56D1                     814 00101$:
                            815 ;src/entities/enemy.c:130: return 0;
   56D1 2E 00         [ 7]  816 	ld	l, #0x00
   56D3 18 1A         [12]  817 	jr	00106$
   56D5                     818 00102$:
                            819 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56D5 21 07 00      [10]  820 	ld	hl, #0x0007
   56D8 09            [11]  821 	add	hl, bc
   56D9 4E            [ 7]  822 	ld	c, (hl)
   56DA DD 7E 06      [19]  823 	ld	a, 6 (ix)
   56DD 91            [ 4]  824 	sub	a, c
   56DE 38 08         [12]  825 	jr	C,00105$
                            826 ;src/entities/enemy.c:134: enemy->health = 0;
   56E0 36 00         [10]  827 	ld	(hl), #0x00
                            828 ;src/entities/enemy.c:135: enemy->active = 0;
   56E2 AF            [ 4]  829 	xor	a, a
   56E3 12            [ 7]  830 	ld	(de), a
                            831 ;src/entities/enemy.c:136: return 1;
   56E4 2E 01         [ 7]  832 	ld	l, #0x01
   56E6 18 07         [12]  833 	jr	00106$
   56E8                     834 00105$:
                            835 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   56E8 79            [ 4]  836 	ld	a, c
   56E9 DD 96 06      [19]  837 	sub	a, 6 (ix)
   56EC 77            [ 7]  838 	ld	(hl), a
                            839 ;src/entities/enemy.c:140: return 0;
   56ED 2E 00         [ 7]  840 	ld	l, #0x00
   56EF                     841 00106$:
   56EF DD E1         [14]  842 	pop	ix
   56F1 C9            [10]  843 	ret
                            844 	.area _CODE
                            845 	.area _INITIALIZER
                            846 	.area _CABS (ABS)
