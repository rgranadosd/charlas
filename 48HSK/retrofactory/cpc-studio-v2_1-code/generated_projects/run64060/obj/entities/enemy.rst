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
   51EC                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   51EC 21 03 00      [10]   58 	ld	hl, #2+1
   51EF 39            [11]   59 	add	hl, sp
   51F0 7E            [ 7]   60 	ld	a, (hl)
   51F1 2B            [ 6]   61 	dec	hl
   51F2 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   51F3 C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   51F4 D1            [10]   66 	pop	de
   51F5 C1            [10]   67 	pop	bc
   51F6 C5            [11]   68 	push	bc
   51F7 D5            [11]   69 	push	de
   51F8 AF            [ 4]   70 	xor	a, a
   51F9 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   51FA 59            [ 4]   73 	ld	e, c
   51FB 50            [ 4]   74 	ld	d, b
   51FC 13            [ 6]   75 	inc	de
   51FD AF            [ 4]   76 	xor	a, a
   51FE 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   51FF 59            [ 4]   79 	ld	e, c
   5200 50            [ 4]   80 	ld	d, b
   5201 13            [ 6]   81 	inc	de
   5202 13            [ 6]   82 	inc	de
   5203 AF            [ 4]   83 	xor	a, a
   5204 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   5205 59            [ 4]   86 	ld	e, c
   5206 50            [ 4]   87 	ld	d, b
   5207 13            [ 6]   88 	inc	de
   5208 13            [ 6]   89 	inc	de
   5209 13            [ 6]   90 	inc	de
   520A AF            [ 4]   91 	xor	a, a
   520B 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   520C 21 04 00      [10]   94 	ld	hl, #0x0004
   520F 09            [11]   95 	add	hl, bc
   5210 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   5212 21 05 00      [10]   98 	ld	hl, #0x0005
   5215 09            [11]   99 	add	hl, bc
   5216 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5218 21 06 00      [10]  102 	ld	hl, #0x0006
   521B 09            [11]  103 	add	hl, bc
   521C 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   521E 21 07 00      [10]  106 	ld	hl, #0x0007
   5221 09            [11]  107 	add	hl, bc
   5222 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   5224 21 08 00      [10]  110 	ld	hl, #0x0008
   5227 09            [11]  111 	add	hl, bc
   5228 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   522A 21 09 00      [10]  114 	ld	hl, #0x0009
   522D 09            [11]  115 	add	hl, bc
   522E 36 00         [10]  116 	ld	(hl), #0x00
   5230 C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   5231                     122 _enemyspawn::
   5231 DD E5         [15]  123 	push	ix
   5233 DD 21 00 00   [14]  124 	ld	ix,#0
   5237 DD 39         [15]  125 	add	ix,sp
   5239 21 F1 FF      [10]  126 	ld	hl, #-15
   523C 39            [11]  127 	add	hl, sp
   523D F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   523E DD 7E 05      [19]  130 	ld	a, 5 (ix)
   5241 DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   5244 CA 04 54      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   5247 DD 7E 04      [19]  135 	ld	a, 4 (ix)
   524A DD 77 FE      [19]  136 	ld	-2 (ix), a
   524D DD 7E 05      [19]  137 	ld	a, 5 (ix)
   5250 DD 77 FF      [19]  138 	ld	-1 (ix), a
   5253 DD 6E FE      [19]  139 	ld	l,-2 (ix)
   5256 DD 66 FF      [19]  140 	ld	h,-1 (ix)
   5259 DD 7E 06      [19]  141 	ld	a, 6 (ix)
   525C 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   525D DD 4E FE      [19]  144 	ld	c,-2 (ix)
   5260 DD 46 FF      [19]  145 	ld	b,-1 (ix)
   5263 03            [ 6]  146 	inc	bc
   5264 DD 7E 07      [19]  147 	ld	a, 7 (ix)
   5267 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   5268 DD 7E FE      [19]  150 	ld	a, -2 (ix)
   526B C6 02         [ 7]  151 	add	a, #0x02
   526D DD 77 FC      [19]  152 	ld	-4 (ix), a
   5270 DD 7E FF      [19]  153 	ld	a, -1 (ix)
   5273 CE 00         [ 7]  154 	adc	a, #0x00
   5275 DD 77 FD      [19]  155 	ld	-3 (ix), a
   5278 DD 7E 09      [19]  156 	ld	a, 9 (ix)
   527B B7            [ 4]  157 	or	a, a
   527C 28 04         [12]  158 	jr	Z,00114$
   527E 0E 01         [ 7]  159 	ld	c, #0x01
   5280 18 02         [12]  160 	jr	00115$
   5282                     161 00114$:
   5282 0E FF         [ 7]  162 	ld	c, #0xff
   5284                     163 00115$:
   5284 DD 6E FC      [19]  164 	ld	l,-4 (ix)
   5287 DD 66 FD      [19]  165 	ld	h,-3 (ix)
   528A 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   528B DD 7E FE      [19]  168 	ld	a, -2 (ix)
   528E C6 03         [ 7]  169 	add	a, #0x03
   5290 DD 77 FA      [19]  170 	ld	-6 (ix), a
   5293 DD 7E FF      [19]  171 	ld	a, -1 (ix)
   5296 CE 00         [ 7]  172 	adc	a, #0x00
   5298 DD 77 FB      [19]  173 	ld	-5 (ix), a
   529B DD 6E FA      [19]  174 	ld	l,-6 (ix)
   529E DD 66 FB      [19]  175 	ld	h,-5 (ix)
   52A1 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   52A3 DD 7E FE      [19]  178 	ld	a, -2 (ix)
   52A6 C6 06         [ 7]  179 	add	a, #0x06
   52A8 DD 77 F8      [19]  180 	ld	-8 (ix), a
   52AB DD 7E FF      [19]  181 	ld	a, -1 (ix)
   52AE CE 00         [ 7]  182 	adc	a, #0x00
   52B0 DD 77 F9      [19]  183 	ld	-7 (ix), a
   52B3 DD 6E F8      [19]  184 	ld	l,-8 (ix)
   52B6 DD 66 F9      [19]  185 	ld	h,-7 (ix)
   52B9 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52BB DD 7E FE      [19]  188 	ld	a, -2 (ix)
   52BE C6 09         [ 7]  189 	add	a, #0x09
   52C0 DD 77 F8      [19]  190 	ld	-8 (ix), a
   52C3 DD 7E FF      [19]  191 	ld	a, -1 (ix)
   52C6 CE 00         [ 7]  192 	adc	a, #0x00
   52C8 DD 77 F9      [19]  193 	ld	-7 (ix), a
   52CB DD 6E F8      [19]  194 	ld	l,-8 (ix)
   52CE DD 66 F9      [19]  195 	ld	h,-7 (ix)
   52D1 DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52D4 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52D5 DD 7E FE      [19]  199 	ld	a, -2 (ix)
   52D8 C6 04         [ 7]  200 	add	a, #0x04
   52DA DD 77 F8      [19]  201 	ld	-8 (ix), a
   52DD DD 7E FF      [19]  202 	ld	a, -1 (ix)
   52E0 CE 00         [ 7]  203 	adc	a, #0x00
   52E2 DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52E5 DD 7E FE      [19]  206 	ld	a, -2 (ix)
   52E8 C6 05         [ 7]  207 	add	a, #0x05
   52EA DD 77 F6      [19]  208 	ld	-10 (ix), a
   52ED DD 7E FF      [19]  209 	ld	a, -1 (ix)
   52F0 CE 00         [ 7]  210 	adc	a, #0x00
   52F2 DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   52F5 DD 7E FE      [19]  213 	ld	a, -2 (ix)
   52F8 C6 07         [ 7]  214 	add	a, #0x07
   52FA DD 77 F4      [19]  215 	ld	-12 (ix), a
   52FD DD 7E FF      [19]  216 	ld	a, -1 (ix)
   5300 CE 00         [ 7]  217 	adc	a, #0x00
   5302 DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   5305 DD 7E FE      [19]  220 	ld	a, -2 (ix)
   5308 C6 08         [ 7]  221 	add	a, #0x08
   530A DD 77 FE      [19]  222 	ld	-2 (ix), a
   530D DD 7E FF      [19]  223 	ld	a, -1 (ix)
   5310 CE 00         [ 7]  224 	adc	a, #0x00
   5312 DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   5315 DD 7E 08      [19]  227 	ld	a, 8 (ix)
   5318 3D            [ 4]  228 	dec	a
   5319 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   531B DD 6E F8      [19]  231 	ld	l,-8 (ix)
   531E DD 66 F9      [19]  232 	ld	h,-7 (ix)
   5321 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   5323 DD 6E F6      [19]  235 	ld	l,-10 (ix)
   5326 DD 66 F7      [19]  236 	ld	h,-9 (ix)
   5329 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   532B DD 6E F4      [19]  239 	ld	l,-12 (ix)
   532E DD 66 F5      [19]  240 	ld	h,-11 (ix)
   5331 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   5333 DD 6E FE      [19]  243 	ld	l,-2 (ix)
   5336 DD 66 FF      [19]  244 	ld	h,-1 (ix)
   5339 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   533B DD 7E FC      [19]  247 	ld	a, -4 (ix)
   533E DD 77 F2      [19]  248 	ld	-14 (ix), a
   5341 DD 7E FD      [19]  249 	ld	a, -3 (ix)
   5344 DD 77 F3      [19]  250 	ld	-13 (ix), a
   5347 DD 7E 09      [19]  251 	ld	a, 9 (ix)
   534A B7            [ 4]  252 	or	a, a
   534B 28 06         [12]  253 	jr	Z,00116$
   534D DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   5351 18 04         [12]  255 	jr	00117$
   5353                     256 00116$:
   5353 DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   5357                     258 00117$:
   5357 DD 6E F2      [19]  259 	ld	l,-14 (ix)
   535A DD 66 F3      [19]  260 	ld	h,-13 (ix)
   535D DD 7E F1      [19]  261 	ld	a, -15 (ix)
   5360 77            [ 7]  262 	ld	(hl), a
   5361 C3 04 54      [10]  263 	jp	00112$
   5364                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   5364 DD 7E 08      [19]  266 	ld	a, 8 (ix)
   5367 D6 02         [ 7]  267 	sub	a, #0x02
   5369 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   536B DD 6E F8      [19]  270 	ld	l,-8 (ix)
   536E DD 66 F9      [19]  271 	ld	h,-7 (ix)
   5371 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   5373 DD 6E F6      [19]  274 	ld	l,-10 (ix)
   5376 DD 66 F7      [19]  275 	ld	h,-9 (ix)
   5379 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   537B DD 6E F4      [19]  278 	ld	l,-12 (ix)
   537E DD 66 F5      [19]  279 	ld	h,-11 (ix)
   5381 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   5383 DD 6E FE      [19]  282 	ld	l,-2 (ix)
   5386 DD 66 FF      [19]  283 	ld	h,-1 (ix)
   5389 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   538B DD 4E FA      [19]  286 	ld	c,-6 (ix)
   538E DD 46 FB      [19]  287 	ld	b,-5 (ix)
   5391 DD 7E 09      [19]  288 	ld	a, 9 (ix)
   5394 B7            [ 4]  289 	or	a, a
   5395 28 04         [12]  290 	jr	Z,00118$
   5397 3E 01         [ 7]  291 	ld	a, #0x01
   5399 18 02         [12]  292 	jr	00119$
   539B                     293 00118$:
   539B 3E FF         [ 7]  294 	ld	a, #0xff
   539D                     295 00119$:
   539D 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   539E DD 6E FC      [19]  298 	ld	l,-4 (ix)
   53A1 DD 66 FD      [19]  299 	ld	h,-3 (ix)
   53A4 36 01         [10]  300 	ld	(hl), #0x01
   53A6 18 5C         [12]  301 	jr	00112$
   53A8                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   53A8 DD 7E 08      [19]  304 	ld	a, 8 (ix)
   53AB D6 03         [ 7]  305 	sub	a, #0x03
   53AD 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   53AF DD 6E F8      [19]  308 	ld	l,-8 (ix)
   53B2 DD 66 F9      [19]  309 	ld	h,-7 (ix)
   53B5 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   53B7 DD 6E F6      [19]  312 	ld	l,-10 (ix)
   53BA DD 66 F7      [19]  313 	ld	h,-9 (ix)
   53BD 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53BF DD 6E F4      [19]  316 	ld	l,-12 (ix)
   53C2 DD 66 F5      [19]  317 	ld	h,-11 (ix)
   53C5 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53C7 DD 6E FE      [19]  320 	ld	l,-2 (ix)
   53CA DD 66 FF      [19]  321 	ld	h,-1 (ix)
   53CD 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53CF DD 4E FC      [19]  324 	ld	c,-4 (ix)
   53D2 DD 46 FD      [19]  325 	ld	b,-3 (ix)
   53D5 DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53D8 B7            [ 4]  327 	or	a, a
   53D9 28 04         [12]  328 	jr	Z,00120$
   53DB 3E 01         [ 7]  329 	ld	a, #0x01
   53DD 18 02         [12]  330 	jr	00121$
   53DF                     331 00120$:
   53DF 3E FF         [ 7]  332 	ld	a, #0xff
   53E1                     333 00121$:
   53E1 02            [ 7]  334 	ld	(bc), a
   53E2 18 20         [12]  335 	jr	00112$
   53E4                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53E4 DD 6E F8      [19]  338 	ld	l,-8 (ix)
   53E7 DD 66 F9      [19]  339 	ld	h,-7 (ix)
   53EA 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   53EC DD 6E F6      [19]  342 	ld	l,-10 (ix)
   53EF DD 66 F7      [19]  343 	ld	h,-9 (ix)
   53F2 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   53F4 DD 6E F4      [19]  346 	ld	l,-12 (ix)
   53F7 DD 66 F5      [19]  347 	ld	h,-11 (ix)
   53FA 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   53FC DD 6E FE      [19]  350 	ld	l,-2 (ix)
   53FF DD 66 FF      [19]  351 	ld	h,-1 (ix)
   5402 36 64         [10]  352 	ld	(hl), #0x64
   5404                     353 00112$:
   5404 DD F9         [10]  354 	ld	sp, ix
   5406 DD E1         [14]  355 	pop	ix
   5408 C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   5409                     361 _enemyupdate::
   5409 DD E5         [15]  362 	push	ix
   540B DD 21 00 00   [14]  363 	ld	ix,#0
   540F DD 39         [15]  364 	add	ix,sp
   5411 21 F6 FF      [10]  365 	ld	hl, #-10
   5414 39            [11]  366 	add	hl, sp
   5415 F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   5416 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   5419 DD B6 04      [19]  370 	or	a,4 (ix)
   541C CA 10 56      [10]  371 	jp	Z,00121$
   541F DD 7E 04      [19]  372 	ld	a, 4 (ix)
   5422 DD 77 FB      [19]  373 	ld	-5 (ix), a
   5425 DD 7E 05      [19]  374 	ld	a, 5 (ix)
   5428 DD 77 FC      [19]  375 	ld	-4 (ix), a
   542B DD 6E FB      [19]  376 	ld	l,-5 (ix)
   542E DD 66 FC      [19]  377 	ld	h,-4 (ix)
   5431 11 06 00      [10]  378 	ld	de, #0x0006
   5434 19            [11]  379 	add	hl, de
   5435 7E            [ 7]  380 	ld	a, (hl)
   5436 B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   5437 CA 10 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   543A DD 6E FB      [19]  385 	ld	l,-5 (ix)
   543D DD 66 FC      [19]  386 	ld	h,-4 (ix)
   5440 11 09 00      [10]  387 	ld	de, #0x0009
   5443 19            [11]  388 	add	hl, de
   5444 7E            [ 7]  389 	ld	a, (hl)
   5445 DD 77 FF      [19]  390 	ld	-1 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5448 DD 6E FB      [19]  392 	ld	l,-5 (ix)
   544B DD 66 FC      [19]  393 	ld	h,-4 (ix)
   544E 4E            [ 7]  394 	ld	c, (hl)
   544F DD 7E FB      [19]  395 	ld	a, -5 (ix)
   5452 C6 02         [ 7]  396 	add	a, #0x02
   5454 DD 77 FD      [19]  397 	ld	-3 (ix), a
   5457 DD 7E FC      [19]  398 	ld	a, -4 (ix)
   545A CE 00         [ 7]  399 	adc	a, #0x00
   545C DD 77 FE      [19]  400 	ld	-2 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   545F DD 7E FB      [19]  402 	ld	a, -5 (ix)
   5462 C6 01         [ 7]  403 	add	a, #0x01
   5464 DD 77 F9      [19]  404 	ld	-7 (ix), a
   5467 DD 7E FC      [19]  405 	ld	a, -4 (ix)
   546A CE 00         [ 7]  406 	adc	a, #0x00
   546C DD 77 FA      [19]  407 	ld	-6 (ix), a
   546F DD 5E FB      [19]  408 	ld	e,-5 (ix)
   5472 DD 56 FC      [19]  409 	ld	d,-4 (ix)
   5475 13            [ 6]  410 	inc	de
   5476 13            [ 6]  411 	inc	de
   5477 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5478 06 00         [ 7]  414 	ld	b, #0x00
   547A DD 6E FD      [19]  415 	ld	l,-3 (ix)
   547D DD 66 FE      [19]  416 	ld	h,-2 (ix)
   5480 7E            [ 7]  417 	ld	a, (hl)
   5481 DD 77 F8      [19]  418 	ld	-8 (ix), a
   5484 6F            [ 4]  419 	ld	l, a
   5485 DD 7E F8      [19]  420 	ld	a, -8 (ix)
   5488 17            [ 4]  421 	rla
   5489 9F            [ 4]  422 	sbc	a, a
   548A 67            [ 4]  423 	ld	h, a
   548B 09            [11]  424 	add	hl,bc
   548C 4D            [ 4]  425 	ld	c, l
   548D 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   548E DD 7E FF      [19]  428 	ld	a, -1 (ix)
   5491 D6 02         [ 7]  429 	sub	a, #0x02
   5493 C2 3C 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5496 DD 6E F9      [19]  433 	ld	l,-7 (ix)
   5499 DD 66 FA      [19]  434 	ld	h,-6 (ix)
   549C 6E            [ 7]  435 	ld	l, (hl)
   549D DD 75 F6      [19]  436 	ld	-10 (ix), l
   54A0 DD 36 F7 00   [19]  437 	ld	-9 (ix), #0x00
   54A4 1A            [ 7]  438 	ld	a, (de)
   54A5 6F            [ 4]  439 	ld	l, a
   54A6 17            [ 4]  440 	rla
   54A7 9F            [ 4]  441 	sbc	a, a
   54A8 67            [ 4]  442 	ld	h, a
   54A9 DD 7E F6      [19]  443 	ld	a, -10 (ix)
   54AC 85            [ 4]  444 	add	a, l
   54AD DD 77 F6      [19]  445 	ld	-10 (ix), a
   54B0 DD 7E F7      [19]  446 	ld	a, -9 (ix)
   54B3 8C            [ 4]  447 	adc	a, h
   54B4 DD 77 F7      [19]  448 	ld	-9 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   54B7 79            [ 4]  450 	ld	a, c
   54B8 D6 08         [ 7]  451 	sub	a, #0x08
   54BA 78            [ 4]  452 	ld	a, b
   54BB 17            [ 4]  453 	rla
   54BC 3F            [ 4]  454 	ccf
   54BD 1F            [ 4]  455 	rra
   54BE DE 80         [ 7]  456 	sbc	a, #0x80
   54C0 38 0E         [12]  457 	jr	C,00104$
   54C2 3E 48         [ 7]  458 	ld	a, #0x48
   54C4 B9            [ 4]  459 	cp	a, c
   54C5 3E 00         [ 7]  460 	ld	a, #0x00
   54C7 98            [ 4]  461 	sbc	a, b
   54C8 E2 CD 54      [10]  462 	jp	PO, 00161$
   54CB EE 80         [ 7]  463 	xor	a, #0x80
   54CD                     464 00161$:
   54CD F2 EB 54      [10]  465 	jp	P, 00105$
   54D0                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   54D0 AF            [ 4]  468 	xor	a, a
   54D1 DD 96 F8      [19]  469 	sub	a, -8 (ix)
   54D4 4F            [ 4]  470 	ld	c, a
   54D5 DD 6E FD      [19]  471 	ld	l,-3 (ix)
   54D8 DD 66 FE      [19]  472 	ld	h,-2 (ix)
   54DB 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54DC DD 6E FB      [19]  475 	ld	l,-5 (ix)
   54DF DD 66 FC      [19]  476 	ld	h,-4 (ix)
   54E2 6E            [ 7]  477 	ld	l, (hl)
   54E3 26 00         [ 7]  478 	ld	h, #0x00
   54E5 79            [ 4]  479 	ld	a, c
   54E6 17            [ 4]  480 	rla
   54E7 9F            [ 4]  481 	sbc	a, a
   54E8 47            [ 4]  482 	ld	b, a
   54E9 09            [11]  483 	add	hl,bc
   54EA 4D            [ 4]  484 	ld	c, l
   54EB                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   54EB DD 7E F6      [19]  487 	ld	a, -10 (ix)
   54EE D6 38         [ 7]  488 	sub	a, #0x38
   54F0 DD 7E F7      [19]  489 	ld	a, -9 (ix)
   54F3 17            [ 4]  490 	rla
   54F4 3F            [ 4]  491 	ccf
   54F5 1F            [ 4]  492 	rra
   54F6 DE 80         [ 7]  493 	sbc	a, #0x80
   54F8 38 12         [12]  494 	jr	C,00107$
   54FA 3E 78         [ 7]  495 	ld	a, #0x78
   54FC DD BE F6      [19]  496 	cp	a, -10 (ix)
   54FF 3E 00         [ 7]  497 	ld	a, #0x00
   5501 DD 9E F7      [19]  498 	sbc	a, -9 (ix)
   5504 E2 09 55      [10]  499 	jp	PO, 00162$
   5507 EE 80         [ 7]  500 	xor	a, #0x80
   5509                     501 00162$:
   5509 F2 28 55      [10]  502 	jp	P, 00108$
   550C                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   550C 1A            [ 7]  505 	ld	a, (de)
   550D 6F            [ 4]  506 	ld	l, a
   550E AF            [ 4]  507 	xor	a, a
   550F 95            [ 4]  508 	sub	a, l
   5510 DD 77 F8      [19]  509 	ld	-8 (ix), a
   5513 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5514 DD 6E F9      [19]  512 	ld	l,-7 (ix)
   5517 DD 66 FA      [19]  513 	ld	h,-6 (ix)
   551A 5E            [ 7]  514 	ld	e, (hl)
   551B 16 00         [ 7]  515 	ld	d, #0x00
   551D DD 6E F8      [19]  516 	ld	l, -8 (ix)
   5520 DD 7E F8      [19]  517 	ld	a, -8 (ix)
   5523 17            [ 4]  518 	rla
   5524 9F            [ 4]  519 	sbc	a, a
   5525 67            [ 4]  520 	ld	h, a
   5526 19            [11]  521 	add	hl,de
   5527 E3            [19]  522 	ex	(sp), hl
   5528                     523 00108$:
                            524 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   5528 DD 6E FB      [19]  525 	ld	l,-5 (ix)
   552B DD 66 FC      [19]  526 	ld	h,-4 (ix)
   552E 71            [ 7]  527 	ld	(hl), c
                            528 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   552F DD 4E F6      [19]  529 	ld	c, -10 (ix)
   5532 DD 6E F9      [19]  530 	ld	l,-7 (ix)
   5535 DD 66 FA      [19]  531 	ld	h,-6 (ix)
   5538 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:84: return;
   5539 C3 10 56      [10]  534 	jp	00121$
   553C                     535 00111$:
                            536 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            537 ;src/entities/enemy.c:88: if (nextx < 2) {
   553C 79            [ 4]  538 	ld	a, c
   553D D6 02         [ 7]  539 	sub	a, #0x02
   553F 78            [ 4]  540 	ld	a, b
   5540 17            [ 4]  541 	rla
   5541 3F            [ 4]  542 	ccf
   5542 1F            [ 4]  543 	rra
   5543 DE 80         [ 7]  544 	sbc	a, #0x80
   5545 30 0B         [12]  545 	jr	NC,00113$
                            546 ;src/entities/enemy.c:89: nextx = 2;
   5547 01 02 00      [10]  547 	ld	bc, #0x0002
                            548 ;src/entities/enemy.c:90: enemy->vx = 1;
   554A DD 6E FD      [19]  549 	ld	l,-3 (ix)
   554D DD 66 FE      [19]  550 	ld	h,-2 (ix)
   5550 36 01         [10]  551 	ld	(hl), #0x01
   5552                     552 00113$:
                            553 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   5552 DD 6E FB      [19]  554 	ld	l,-5 (ix)
   5555 DD 66 FC      [19]  555 	ld	h,-4 (ix)
   5558 23            [ 6]  556 	inc	hl
   5559 23            [ 6]  557 	inc	hl
   555A 23            [ 6]  558 	inc	hl
   555B 23            [ 6]  559 	inc	hl
   555C 6E            [ 7]  560 	ld	l, (hl)
   555D 26 00         [ 7]  561 	ld	h, #0x00
   555F 3E 50         [ 7]  562 	ld	a, #0x50
   5561 95            [ 4]  563 	sub	a, l
   5562 6F            [ 4]  564 	ld	l, a
   5563 3E 00         [ 7]  565 	ld	a, #0x00
   5565 9C            [ 4]  566 	sbc	a, h
   5566 67            [ 4]  567 	ld	h, a
                            568 ;src/entities/enemy.c:94: if (nextx > maxx) {
   5567 7D            [ 4]  569 	ld	a, l
   5568 91            [ 4]  570 	sub	a, c
   5569 7C            [ 4]  571 	ld	a, h
   556A 98            [ 4]  572 	sbc	a, b
   556B E2 70 55      [10]  573 	jp	PO, 00163$
   556E EE 80         [ 7]  574 	xor	a, #0x80
   5570                     575 00163$:
   5570 F2 7C 55      [10]  576 	jp	P, 00115$
                            577 ;src/entities/enemy.c:95: nextx = maxx;
   5573 4D            [ 4]  578 	ld	c, l
                            579 ;src/entities/enemy.c:96: enemy->vx = -1;
   5574 DD 6E FD      [19]  580 	ld	l,-3 (ix)
   5577 DD 66 FE      [19]  581 	ld	h,-2 (ix)
   557A 36 FF         [10]  582 	ld	(hl), #0xff
   557C                     583 00115$:
                            584 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   557C DD 6E FB      [19]  585 	ld	l,-5 (ix)
   557F DD 66 FC      [19]  586 	ld	h,-4 (ix)
   5582 71            [ 7]  587 	ld	(hl), c
                            588 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   5583 1A            [ 7]  589 	ld	a, (de)
   5584 4F            [ 4]  590 	ld	c, a
   5585 0C            [ 4]  591 	inc	c
   5586 79            [ 4]  592 	ld	a, c
   5587 12            [ 7]  593 	ld	(de), a
                            594 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   5588 3E 03         [ 7]  595 	ld	a, #0x03
   558A 91            [ 4]  596 	sub	a, c
   558B E2 90 55      [10]  597 	jp	PO, 00164$
   558E EE 80         [ 7]  598 	xor	a, #0x80
   5590                     599 00164$:
   5590 F2 96 55      [10]  600 	jp	P, 00117$
   5593 3E 03         [ 7]  601 	ld	a, #0x03
   5595 12            [ 7]  602 	ld	(de), a
   5596                     603 00117$:
                            604 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   5596 DD 6E F9      [19]  605 	ld	l,-7 (ix)
   5599 DD 66 FA      [19]  606 	ld	h,-6 (ix)
   559C 4E            [ 7]  607 	ld	c, (hl)
   559D 06 00         [ 7]  608 	ld	b, #0x00
   559F 1A            [ 7]  609 	ld	a, (de)
   55A0 6F            [ 4]  610 	ld	l, a
   55A1 17            [ 4]  611 	rla
   55A2 9F            [ 4]  612 	sbc	a, a
   55A3 67            [ 4]  613 	ld	h, a
   55A4 09            [11]  614 	add	hl, bc
   55A5 E5            [11]  615 	push	hl
   55A6 FD E1         [14]  616 	pop	iy
                            617 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   55A8 DD 7E FB      [19]  618 	ld	a, -5 (ix)
   55AB C6 05         [ 7]  619 	add	a, #0x05
   55AD DD 77 F6      [19]  620 	ld	-10 (ix), a
   55B0 DD 7E FC      [19]  621 	ld	a, -4 (ix)
   55B3 CE 00         [ 7]  622 	adc	a, #0x00
   55B5 DD 77 F7      [19]  623 	ld	-9 (ix), a
   55B8 E1            [10]  624 	pop	hl
   55B9 E5            [11]  625 	push	hl
   55BA 7E            [ 7]  626 	ld	a, (hl)
   55BB DD 6E FB      [19]  627 	ld	l,-5 (ix)
   55BE DD 66 FC      [19]  628 	ld	h,-4 (ix)
   55C1 4E            [ 7]  629 	ld	c, (hl)
   55C2 06 00         [ 7]  630 	ld	b, #0x00
   55C4 D5            [11]  631 	push	de
   55C5 F5            [11]  632 	push	af
   55C6 33            [ 6]  633 	inc	sp
   55C7 FD E5         [15]  634 	push	iy
   55C9 C5            [11]  635 	push	bc
   55CA CD 29 4C      [17]  636 	call	_collision_clamp_y_at
   55CD F1            [10]  637 	pop	af
   55CE F1            [10]  638 	pop	af
   55CF 33            [ 6]  639 	inc	sp
   55D0 4D            [ 4]  640 	ld	c, l
   55D1 D1            [10]  641 	pop	de
                            642 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55D2 DD 6E F9      [19]  643 	ld	l,-7 (ix)
   55D5 DD 66 FA      [19]  644 	ld	h,-6 (ix)
   55D8 71            [ 7]  645 	ld	(hl), c
                            646 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55D9 E1            [10]  647 	pop	hl
   55DA E5            [11]  648 	push	hl
   55DB 7E            [ 7]  649 	ld	a, (hl)
   55DC 06 00         [ 7]  650 	ld	b, #0x00
   55DE DD 6E FB      [19]  651 	ld	l,-5 (ix)
   55E1 DD 66 FC      [19]  652 	ld	h,-4 (ix)
   55E4 6E            [ 7]  653 	ld	l, (hl)
   55E5 DD 75 F6      [19]  654 	ld	-10 (ix), l
   55E8 DD 36 F7 00   [19]  655 	ld	-9 (ix), #0x00
   55EC D5            [11]  656 	push	de
   55ED F5            [11]  657 	push	af
   55EE 33            [ 6]  658 	inc	sp
   55EF C5            [11]  659 	push	bc
   55F0 DD 6E F6      [19]  660 	ld	l,-10 (ix)
   55F3 DD 66 F7      [19]  661 	ld	h,-9 (ix)
   55F6 E5            [11]  662 	push	hl
   55F7 CD AA 4B      [17]  663 	call	_collision_is_on_ground_at
   55FA F1            [10]  664 	pop	af
   55FB F1            [10]  665 	pop	af
   55FC 33            [ 6]  666 	inc	sp
   55FD D1            [10]  667 	pop	de
   55FE 7D            [ 4]  668 	ld	a, l
   55FF B7            [ 4]  669 	or	a, a
   5600 28 0E         [12]  670 	jr	Z,00121$
   5602 1A            [ 7]  671 	ld	a, (de)
   5603 4F            [ 4]  672 	ld	c, a
   5604 AF            [ 4]  673 	xor	a, a
   5605 91            [ 4]  674 	sub	a, c
   5606 E2 0B 56      [10]  675 	jp	PO, 00165$
   5609 EE 80         [ 7]  676 	xor	a, #0x80
   560B                     677 00165$:
   560B F2 10 56      [10]  678 	jp	P, 00121$
                            679 ;src/entities/enemy.c:107: enemy->vy = 0;
   560E AF            [ 4]  680 	xor	a, a
   560F 12            [ 7]  681 	ld	(de), a
   5610                     682 00121$:
   5610 DD F9         [10]  683 	ld	sp, ix
   5612 DD E1         [14]  684 	pop	ix
   5614 C9            [10]  685 	ret
                            686 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            687 ;	---------------------------------
                            688 ; Function enemyrender
                            689 ; ---------------------------------
   5615                     690 _enemyrender::
   5615 DD E5         [15]  691 	push	ix
   5617 DD 21 00 00   [14]  692 	ld	ix,#0
   561B DD 39         [15]  693 	add	ix,sp
   561D F5            [11]  694 	push	af
                            695 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   561E DD 7E 05      [19]  696 	ld	a, 5 (ix)
   5621 DD B6 04      [19]  697 	or	a,4 (ix)
   5624 CA A2 56      [10]  698 	jp	Z,00113$
   5627 DD 7E 04      [19]  699 	ld	a, 4 (ix)
   562A DD 77 FE      [19]  700 	ld	-2 (ix), a
   562D DD 7E 05      [19]  701 	ld	a, 5 (ix)
   5630 DD 77 FF      [19]  702 	ld	-1 (ix), a
   5633 E1            [10]  703 	pop	hl
   5634 E5            [11]  704 	push	hl
   5635 11 06 00      [10]  705 	ld	de, #0x0006
   5638 19            [11]  706 	add	hl, de
   5639 7E            [ 7]  707 	ld	a, (hl)
   563A B7            [ 4]  708 	or	a, a
                            709 ;src/entities/enemy.c:116: return;
   563B 28 65         [12]  710 	jr	Z,00113$
                            711 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   563D E1            [10]  712 	pop	hl
   563E E5            [11]  713 	push	hl
   563F 11 09 00      [10]  714 	ld	de, #0x0009
   5642 19            [11]  715 	add	hl, de
   5643 7E            [ 7]  716 	ld	a, (hl)
   5644 FE 03         [ 7]  717 	cp	a, #0x03
   5646 20 0A         [12]  718 	jr	NZ,00111$
   5648 21 0C 0C      [10]  719 	ld	hl, #0x0c0c
   564B E5            [11]  720 	push	hl
   564C CD 64 5D      [17]  721 	call	_cpct_px2byteM0
   564F 4D            [ 4]  722 	ld	c, l
   5650 18 23         [12]  723 	jr	00112$
   5652                     724 00111$:
                            725 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   5652 FE 02         [ 7]  726 	cp	a, #0x02
   5654 20 0A         [12]  727 	jr	NZ,00108$
   5656 21 0A 0A      [10]  728 	ld	hl, #0x0a0a
   5659 E5            [11]  729 	push	hl
   565A CD 64 5D      [17]  730 	call	_cpct_px2byteM0
   565D 4D            [ 4]  731 	ld	c, l
   565E 18 15         [12]  732 	jr	00112$
   5660                     733 00108$:
                            734 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   5660 3D            [ 4]  735 	dec	a
   5661 20 0A         [12]  736 	jr	NZ,00105$
   5663 21 0E 0E      [10]  737 	ld	hl, #0x0e0e
   5666 E5            [11]  738 	push	hl
   5667 CD 64 5D      [17]  739 	call	_cpct_px2byteM0
   566A 4D            [ 4]  740 	ld	c, l
   566B 18 08         [12]  741 	jr	00112$
   566D                     742 00105$:
                            743 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   566D 21 04 04      [10]  744 	ld	hl, #0x0404
   5670 E5            [11]  745 	push	hl
   5671 CD 64 5D      [17]  746 	call	_cpct_px2byteM0
   5674 4D            [ 4]  747 	ld	c, l
   5675                     748 00112$:
                            749 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5675 E1            [10]  750 	pop	hl
   5676 E5            [11]  751 	push	hl
   5677 23            [ 6]  752 	inc	hl
   5678 46            [ 7]  753 	ld	b, (hl)
   5679 E1            [10]  754 	pop	hl
   567A E5            [11]  755 	push	hl
   567B 56            [ 7]  756 	ld	d, (hl)
   567C C5            [11]  757 	push	bc
   567D 4A            [ 4]  758 	ld	c, d
   567E C5            [11]  759 	push	bc
   567F 21 00 C0      [10]  760 	ld	hl, #0xc000
   5682 E5            [11]  761 	push	hl
   5683 CD 57 5E      [17]  762 	call	_cpct_getScreenPtr
   5686 EB            [ 4]  763 	ex	de,hl
   5687 C1            [10]  764 	pop	bc
                            765 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   5688 E1            [10]  766 	pop	hl
   5689 E5            [11]  767 	push	hl
   568A 23            [ 6]  768 	inc	hl
   568B 23            [ 6]  769 	inc	hl
   568C 23            [ 6]  770 	inc	hl
   568D 23            [ 6]  771 	inc	hl
   568E 23            [ 6]  772 	inc	hl
   568F 46            [ 7]  773 	ld	b, (hl)
   5690 E1            [10]  774 	pop	hl
   5691 E5            [11]  775 	push	hl
   5692 23            [ 6]  776 	inc	hl
   5693 23            [ 6]  777 	inc	hl
   5694 23            [ 6]  778 	inc	hl
   5695 23            [ 6]  779 	inc	hl
   5696 7E            [ 7]  780 	ld	a, (hl)
   5697 C5            [11]  781 	push	bc
   5698 33            [ 6]  782 	inc	sp
   5699 47            [ 4]  783 	ld	b, a
   569A C5            [11]  784 	push	bc
   569B D5            [11]  785 	push	de
   569C CD 9E 5D      [17]  786 	call	_cpct_drawSolidBox
   569F F1            [10]  787 	pop	af
   56A0 F1            [10]  788 	pop	af
   56A1 33            [ 6]  789 	inc	sp
   56A2                     790 00113$:
   56A2 DD F9         [10]  791 	ld	sp, ix
   56A4 DD E1         [14]  792 	pop	ix
   56A6 C9            [10]  793 	ret
                            794 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            795 ;	---------------------------------
                            796 ; Function enemydamage
                            797 ; ---------------------------------
   56A7                     798 _enemydamage::
   56A7 DD E5         [15]  799 	push	ix
   56A9 DD 21 00 00   [14]  800 	ld	ix,#0
   56AD DD 39         [15]  801 	add	ix,sp
                            802 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   56AF DD 7E 05      [19]  803 	ld	a, 5 (ix)
   56B2 DD B6 04      [19]  804 	or	a,4 (ix)
   56B5 28 0F         [12]  805 	jr	Z,00101$
   56B7 DD 4E 04      [19]  806 	ld	c,4 (ix)
   56BA DD 46 05      [19]  807 	ld	b,5 (ix)
   56BD 21 06 00      [10]  808 	ld	hl, #0x0006
   56C0 09            [11]  809 	add	hl,bc
   56C1 EB            [ 4]  810 	ex	de,hl
   56C2 1A            [ 7]  811 	ld	a, (de)
   56C3 B7            [ 4]  812 	or	a, a
   56C4 20 04         [12]  813 	jr	NZ,00102$
   56C6                     814 00101$:
                            815 ;src/entities/enemy.c:130: return 0;
   56C6 2E 00         [ 7]  816 	ld	l, #0x00
   56C8 18 1A         [12]  817 	jr	00106$
   56CA                     818 00102$:
                            819 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56CA 21 07 00      [10]  820 	ld	hl, #0x0007
   56CD 09            [11]  821 	add	hl, bc
   56CE 4E            [ 7]  822 	ld	c, (hl)
   56CF DD 7E 06      [19]  823 	ld	a, 6 (ix)
   56D2 91            [ 4]  824 	sub	a, c
   56D3 38 08         [12]  825 	jr	C,00105$
                            826 ;src/entities/enemy.c:134: enemy->health = 0;
   56D5 36 00         [10]  827 	ld	(hl), #0x00
                            828 ;src/entities/enemy.c:135: enemy->active = 0;
   56D7 AF            [ 4]  829 	xor	a, a
   56D8 12            [ 7]  830 	ld	(de), a
                            831 ;src/entities/enemy.c:136: return 1;
   56D9 2E 01         [ 7]  832 	ld	l, #0x01
   56DB 18 07         [12]  833 	jr	00106$
   56DD                     834 00105$:
                            835 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   56DD 79            [ 4]  836 	ld	a, c
   56DE DD 96 06      [19]  837 	sub	a, 6 (ix)
   56E1 77            [ 7]  838 	ld	(hl), a
                            839 ;src/entities/enemy.c:140: return 0;
   56E2 2E 00         [ 7]  840 	ld	l, #0x00
   56E4                     841 00106$:
   56E4 DD E1         [14]  842 	pop	ix
   56E6 C9            [10]  843 	ret
                            844 	.area _CODE
                            845 	.area _INITIALIZER
                            846 	.area _CABS (ABS)
