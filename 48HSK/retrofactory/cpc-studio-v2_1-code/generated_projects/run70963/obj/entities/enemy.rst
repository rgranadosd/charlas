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
   51E1                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   51E1 21 03 00      [10]   58 	ld	hl, #2+1
   51E4 39            [11]   59 	add	hl, sp
   51E5 7E            [ 7]   60 	ld	a, (hl)
   51E6 2B            [ 6]   61 	dec	hl
   51E7 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   51E8 C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   51E9 D1            [10]   66 	pop	de
   51EA C1            [10]   67 	pop	bc
   51EB C5            [11]   68 	push	bc
   51EC D5            [11]   69 	push	de
   51ED AF            [ 4]   70 	xor	a, a
   51EE 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   51EF 59            [ 4]   73 	ld	e, c
   51F0 50            [ 4]   74 	ld	d, b
   51F1 13            [ 6]   75 	inc	de
   51F2 AF            [ 4]   76 	xor	a, a
   51F3 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   51F4 59            [ 4]   79 	ld	e, c
   51F5 50            [ 4]   80 	ld	d, b
   51F6 13            [ 6]   81 	inc	de
   51F7 13            [ 6]   82 	inc	de
   51F8 AF            [ 4]   83 	xor	a, a
   51F9 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   51FA 59            [ 4]   86 	ld	e, c
   51FB 50            [ 4]   87 	ld	d, b
   51FC 13            [ 6]   88 	inc	de
   51FD 13            [ 6]   89 	inc	de
   51FE 13            [ 6]   90 	inc	de
   51FF AF            [ 4]   91 	xor	a, a
   5200 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   5201 21 04 00      [10]   94 	ld	hl, #0x0004
   5204 09            [11]   95 	add	hl, bc
   5205 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   5207 21 05 00      [10]   98 	ld	hl, #0x0005
   520A 09            [11]   99 	add	hl, bc
   520B 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   520D 21 06 00      [10]  102 	ld	hl, #0x0006
   5210 09            [11]  103 	add	hl, bc
   5211 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   5213 21 07 00      [10]  106 	ld	hl, #0x0007
   5216 09            [11]  107 	add	hl, bc
   5217 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   5219 21 08 00      [10]  110 	ld	hl, #0x0008
   521C 09            [11]  111 	add	hl, bc
   521D 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   521F 21 09 00      [10]  114 	ld	hl, #0x0009
   5222 09            [11]  115 	add	hl, bc
   5223 36 00         [10]  116 	ld	(hl), #0x00
   5225 C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   5226                     122 _enemyspawn::
   5226 DD E5         [15]  123 	push	ix
   5228 DD 21 00 00   [14]  124 	ld	ix,#0
   522C DD 39         [15]  125 	add	ix,sp
   522E 21 F1 FF      [10]  126 	ld	hl, #-15
   5231 39            [11]  127 	add	hl, sp
   5232 F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   5233 DD 7E 05      [19]  130 	ld	a, 5 (ix)
   5236 DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   5239 CA F9 53      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   523C DD 7E 04      [19]  135 	ld	a, 4 (ix)
   523F DD 77 FE      [19]  136 	ld	-2 (ix), a
   5242 DD 7E 05      [19]  137 	ld	a, 5 (ix)
   5245 DD 77 FF      [19]  138 	ld	-1 (ix), a
   5248 DD 6E FE      [19]  139 	ld	l,-2 (ix)
   524B DD 66 FF      [19]  140 	ld	h,-1 (ix)
   524E DD 7E 06      [19]  141 	ld	a, 6 (ix)
   5251 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   5252 DD 4E FE      [19]  144 	ld	c,-2 (ix)
   5255 DD 46 FF      [19]  145 	ld	b,-1 (ix)
   5258 03            [ 6]  146 	inc	bc
   5259 DD 7E 07      [19]  147 	ld	a, 7 (ix)
   525C 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   525D DD 7E FE      [19]  150 	ld	a, -2 (ix)
   5260 C6 02         [ 7]  151 	add	a, #0x02
   5262 DD 77 FC      [19]  152 	ld	-4 (ix), a
   5265 DD 7E FF      [19]  153 	ld	a, -1 (ix)
   5268 CE 00         [ 7]  154 	adc	a, #0x00
   526A DD 77 FD      [19]  155 	ld	-3 (ix), a
   526D DD 7E 09      [19]  156 	ld	a, 9 (ix)
   5270 B7            [ 4]  157 	or	a, a
   5271 28 04         [12]  158 	jr	Z,00114$
   5273 0E 01         [ 7]  159 	ld	c, #0x01
   5275 18 02         [12]  160 	jr	00115$
   5277                     161 00114$:
   5277 0E FF         [ 7]  162 	ld	c, #0xff
   5279                     163 00115$:
   5279 DD 6E FC      [19]  164 	ld	l,-4 (ix)
   527C DD 66 FD      [19]  165 	ld	h,-3 (ix)
   527F 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   5280 DD 7E FE      [19]  168 	ld	a, -2 (ix)
   5283 C6 03         [ 7]  169 	add	a, #0x03
   5285 DD 77 FA      [19]  170 	ld	-6 (ix), a
   5288 DD 7E FF      [19]  171 	ld	a, -1 (ix)
   528B CE 00         [ 7]  172 	adc	a, #0x00
   528D DD 77 FB      [19]  173 	ld	-5 (ix), a
   5290 DD 6E FA      [19]  174 	ld	l,-6 (ix)
   5293 DD 66 FB      [19]  175 	ld	h,-5 (ix)
   5296 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   5298 DD 7E FE      [19]  178 	ld	a, -2 (ix)
   529B C6 06         [ 7]  179 	add	a, #0x06
   529D DD 77 F8      [19]  180 	ld	-8 (ix), a
   52A0 DD 7E FF      [19]  181 	ld	a, -1 (ix)
   52A3 CE 00         [ 7]  182 	adc	a, #0x00
   52A5 DD 77 F9      [19]  183 	ld	-7 (ix), a
   52A8 DD 6E F8      [19]  184 	ld	l,-8 (ix)
   52AB DD 66 F9      [19]  185 	ld	h,-7 (ix)
   52AE 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52B0 DD 7E FE      [19]  188 	ld	a, -2 (ix)
   52B3 C6 09         [ 7]  189 	add	a, #0x09
   52B5 DD 77 F8      [19]  190 	ld	-8 (ix), a
   52B8 DD 7E FF      [19]  191 	ld	a, -1 (ix)
   52BB CE 00         [ 7]  192 	adc	a, #0x00
   52BD DD 77 F9      [19]  193 	ld	-7 (ix), a
   52C0 DD 6E F8      [19]  194 	ld	l,-8 (ix)
   52C3 DD 66 F9      [19]  195 	ld	h,-7 (ix)
   52C6 DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52C9 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52CA DD 7E FE      [19]  199 	ld	a, -2 (ix)
   52CD C6 04         [ 7]  200 	add	a, #0x04
   52CF DD 77 F8      [19]  201 	ld	-8 (ix), a
   52D2 DD 7E FF      [19]  202 	ld	a, -1 (ix)
   52D5 CE 00         [ 7]  203 	adc	a, #0x00
   52D7 DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52DA DD 7E FE      [19]  206 	ld	a, -2 (ix)
   52DD C6 05         [ 7]  207 	add	a, #0x05
   52DF DD 77 F6      [19]  208 	ld	-10 (ix), a
   52E2 DD 7E FF      [19]  209 	ld	a, -1 (ix)
   52E5 CE 00         [ 7]  210 	adc	a, #0x00
   52E7 DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   52EA DD 7E FE      [19]  213 	ld	a, -2 (ix)
   52ED C6 07         [ 7]  214 	add	a, #0x07
   52EF DD 77 F4      [19]  215 	ld	-12 (ix), a
   52F2 DD 7E FF      [19]  216 	ld	a, -1 (ix)
   52F5 CE 00         [ 7]  217 	adc	a, #0x00
   52F7 DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   52FA DD 7E FE      [19]  220 	ld	a, -2 (ix)
   52FD C6 08         [ 7]  221 	add	a, #0x08
   52FF DD 77 FE      [19]  222 	ld	-2 (ix), a
   5302 DD 7E FF      [19]  223 	ld	a, -1 (ix)
   5305 CE 00         [ 7]  224 	adc	a, #0x00
   5307 DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   530A DD 7E 08      [19]  227 	ld	a, 8 (ix)
   530D 3D            [ 4]  228 	dec	a
   530E 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   5310 DD 6E F8      [19]  231 	ld	l,-8 (ix)
   5313 DD 66 F9      [19]  232 	ld	h,-7 (ix)
   5316 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   5318 DD 6E F6      [19]  235 	ld	l,-10 (ix)
   531B DD 66 F7      [19]  236 	ld	h,-9 (ix)
   531E 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   5320 DD 6E F4      [19]  239 	ld	l,-12 (ix)
   5323 DD 66 F5      [19]  240 	ld	h,-11 (ix)
   5326 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   5328 DD 6E FE      [19]  243 	ld	l,-2 (ix)
   532B DD 66 FF      [19]  244 	ld	h,-1 (ix)
   532E 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   5330 DD 7E FC      [19]  247 	ld	a, -4 (ix)
   5333 DD 77 F2      [19]  248 	ld	-14 (ix), a
   5336 DD 7E FD      [19]  249 	ld	a, -3 (ix)
   5339 DD 77 F3      [19]  250 	ld	-13 (ix), a
   533C DD 7E 09      [19]  251 	ld	a, 9 (ix)
   533F B7            [ 4]  252 	or	a, a
   5340 28 06         [12]  253 	jr	Z,00116$
   5342 DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   5346 18 04         [12]  255 	jr	00117$
   5348                     256 00116$:
   5348 DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   534C                     258 00117$:
   534C DD 6E F2      [19]  259 	ld	l,-14 (ix)
   534F DD 66 F3      [19]  260 	ld	h,-13 (ix)
   5352 DD 7E F1      [19]  261 	ld	a, -15 (ix)
   5355 77            [ 7]  262 	ld	(hl), a
   5356 C3 F9 53      [10]  263 	jp	00112$
   5359                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   5359 DD 7E 08      [19]  266 	ld	a, 8 (ix)
   535C D6 02         [ 7]  267 	sub	a, #0x02
   535E 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   5360 DD 6E F8      [19]  270 	ld	l,-8 (ix)
   5363 DD 66 F9      [19]  271 	ld	h,-7 (ix)
   5366 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   5368 DD 6E F6      [19]  274 	ld	l,-10 (ix)
   536B DD 66 F7      [19]  275 	ld	h,-9 (ix)
   536E 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   5370 DD 6E F4      [19]  278 	ld	l,-12 (ix)
   5373 DD 66 F5      [19]  279 	ld	h,-11 (ix)
   5376 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   5378 DD 6E FE      [19]  282 	ld	l,-2 (ix)
   537B DD 66 FF      [19]  283 	ld	h,-1 (ix)
   537E 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5380 DD 4E FA      [19]  286 	ld	c,-6 (ix)
   5383 DD 46 FB      [19]  287 	ld	b,-5 (ix)
   5386 DD 7E 09      [19]  288 	ld	a, 9 (ix)
   5389 B7            [ 4]  289 	or	a, a
   538A 28 04         [12]  290 	jr	Z,00118$
   538C 3E 01         [ 7]  291 	ld	a, #0x01
   538E 18 02         [12]  292 	jr	00119$
   5390                     293 00118$:
   5390 3E FF         [ 7]  294 	ld	a, #0xff
   5392                     295 00119$:
   5392 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   5393 DD 6E FC      [19]  298 	ld	l,-4 (ix)
   5396 DD 66 FD      [19]  299 	ld	h,-3 (ix)
   5399 36 01         [10]  300 	ld	(hl), #0x01
   539B 18 5C         [12]  301 	jr	00112$
   539D                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   539D DD 7E 08      [19]  304 	ld	a, 8 (ix)
   53A0 D6 03         [ 7]  305 	sub	a, #0x03
   53A2 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   53A4 DD 6E F8      [19]  308 	ld	l,-8 (ix)
   53A7 DD 66 F9      [19]  309 	ld	h,-7 (ix)
   53AA 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   53AC DD 6E F6      [19]  312 	ld	l,-10 (ix)
   53AF DD 66 F7      [19]  313 	ld	h,-9 (ix)
   53B2 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53B4 DD 6E F4      [19]  316 	ld	l,-12 (ix)
   53B7 DD 66 F5      [19]  317 	ld	h,-11 (ix)
   53BA 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53BC DD 6E FE      [19]  320 	ld	l,-2 (ix)
   53BF DD 66 FF      [19]  321 	ld	h,-1 (ix)
   53C2 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53C4 DD 4E FC      [19]  324 	ld	c,-4 (ix)
   53C7 DD 46 FD      [19]  325 	ld	b,-3 (ix)
   53CA DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53CD B7            [ 4]  327 	or	a, a
   53CE 28 04         [12]  328 	jr	Z,00120$
   53D0 3E 01         [ 7]  329 	ld	a, #0x01
   53D2 18 02         [12]  330 	jr	00121$
   53D4                     331 00120$:
   53D4 3E FF         [ 7]  332 	ld	a, #0xff
   53D6                     333 00121$:
   53D6 02            [ 7]  334 	ld	(bc), a
   53D7 18 20         [12]  335 	jr	00112$
   53D9                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53D9 DD 6E F8      [19]  338 	ld	l,-8 (ix)
   53DC DD 66 F9      [19]  339 	ld	h,-7 (ix)
   53DF 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   53E1 DD 6E F6      [19]  342 	ld	l,-10 (ix)
   53E4 DD 66 F7      [19]  343 	ld	h,-9 (ix)
   53E7 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   53E9 DD 6E F4      [19]  346 	ld	l,-12 (ix)
   53EC DD 66 F5      [19]  347 	ld	h,-11 (ix)
   53EF 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   53F1 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   53F4 DD 66 FF      [19]  351 	ld	h,-1 (ix)
   53F7 36 64         [10]  352 	ld	(hl), #0x64
   53F9                     353 00112$:
   53F9 DD F9         [10]  354 	ld	sp, ix
   53FB DD E1         [14]  355 	pop	ix
   53FD C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   53FE                     361 _enemyupdate::
   53FE DD E5         [15]  362 	push	ix
   5400 DD 21 00 00   [14]  363 	ld	ix,#0
   5404 DD 39         [15]  364 	add	ix,sp
   5406 21 F6 FF      [10]  365 	ld	hl, #-10
   5409 39            [11]  366 	add	hl, sp
   540A F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   540B DD 7E 05      [19]  369 	ld	a, 5 (ix)
   540E DD B6 04      [19]  370 	or	a,4 (ix)
   5411 CA 05 56      [10]  371 	jp	Z,00121$
   5414 DD 7E 04      [19]  372 	ld	a, 4 (ix)
   5417 DD 77 FE      [19]  373 	ld	-2 (ix), a
   541A DD 7E 05      [19]  374 	ld	a, 5 (ix)
   541D DD 77 FF      [19]  375 	ld	-1 (ix), a
   5420 DD 6E FE      [19]  376 	ld	l,-2 (ix)
   5423 DD 66 FF      [19]  377 	ld	h,-1 (ix)
   5426 11 06 00      [10]  378 	ld	de, #0x0006
   5429 19            [11]  379 	add	hl, de
   542A 7E            [ 7]  380 	ld	a, (hl)
   542B B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   542C CA 05 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   542F DD 6E FE      [19]  385 	ld	l,-2 (ix)
   5432 DD 66 FF      [19]  386 	ld	h,-1 (ix)
   5435 11 09 00      [10]  387 	ld	de, #0x0009
   5438 19            [11]  388 	add	hl, de
   5439 7E            [ 7]  389 	ld	a, (hl)
   543A DD 77 FD      [19]  390 	ld	-3 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   543D DD 6E FE      [19]  392 	ld	l,-2 (ix)
   5440 DD 66 FF      [19]  393 	ld	h,-1 (ix)
   5443 4E            [ 7]  394 	ld	c, (hl)
   5444 DD 7E FE      [19]  395 	ld	a, -2 (ix)
   5447 C6 02         [ 7]  396 	add	a, #0x02
   5449 DD 77 FB      [19]  397 	ld	-5 (ix), a
   544C DD 7E FF      [19]  398 	ld	a, -1 (ix)
   544F CE 00         [ 7]  399 	adc	a, #0x00
   5451 DD 77 FC      [19]  400 	ld	-4 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5454 DD 7E FE      [19]  402 	ld	a, -2 (ix)
   5457 C6 01         [ 7]  403 	add	a, #0x01
   5459 DD 77 F9      [19]  404 	ld	-7 (ix), a
   545C DD 7E FF      [19]  405 	ld	a, -1 (ix)
   545F CE 00         [ 7]  406 	adc	a, #0x00
   5461 DD 77 FA      [19]  407 	ld	-6 (ix), a
   5464 DD 5E FE      [19]  408 	ld	e,-2 (ix)
   5467 DD 56 FF      [19]  409 	ld	d,-1 (ix)
   546A 13            [ 6]  410 	inc	de
   546B 13            [ 6]  411 	inc	de
   546C 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   546D 06 00         [ 7]  414 	ld	b, #0x00
   546F DD 6E FB      [19]  415 	ld	l,-5 (ix)
   5472 DD 66 FC      [19]  416 	ld	h,-4 (ix)
   5475 7E            [ 7]  417 	ld	a, (hl)
   5476 DD 77 F8      [19]  418 	ld	-8 (ix), a
   5479 6F            [ 4]  419 	ld	l, a
   547A DD 7E F8      [19]  420 	ld	a, -8 (ix)
   547D 17            [ 4]  421 	rla
   547E 9F            [ 4]  422 	sbc	a, a
   547F 67            [ 4]  423 	ld	h, a
   5480 09            [11]  424 	add	hl,bc
   5481 4D            [ 4]  425 	ld	c, l
   5482 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5483 DD 7E FD      [19]  428 	ld	a, -3 (ix)
   5486 D6 02         [ 7]  429 	sub	a, #0x02
   5488 C2 31 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   548B DD 6E F9      [19]  433 	ld	l,-7 (ix)
   548E DD 66 FA      [19]  434 	ld	h,-6 (ix)
   5491 6E            [ 7]  435 	ld	l, (hl)
   5492 DD 75 F6      [19]  436 	ld	-10 (ix), l
   5495 DD 36 F7 00   [19]  437 	ld	-9 (ix), #0x00
   5499 1A            [ 7]  438 	ld	a, (de)
   549A 6F            [ 4]  439 	ld	l, a
   549B 17            [ 4]  440 	rla
   549C 9F            [ 4]  441 	sbc	a, a
   549D 67            [ 4]  442 	ld	h, a
   549E DD 7E F6      [19]  443 	ld	a, -10 (ix)
   54A1 85            [ 4]  444 	add	a, l
   54A2 DD 77 F6      [19]  445 	ld	-10 (ix), a
   54A5 DD 7E F7      [19]  446 	ld	a, -9 (ix)
   54A8 8C            [ 4]  447 	adc	a, h
   54A9 DD 77 F7      [19]  448 	ld	-9 (ix), a
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
   54C6 DD 96 F8      [19]  469 	sub	a, -8 (ix)
   54C9 4F            [ 4]  470 	ld	c, a
   54CA DD 6E FB      [19]  471 	ld	l,-5 (ix)
   54CD DD 66 FC      [19]  472 	ld	h,-4 (ix)
   54D0 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54D1 DD 6E FE      [19]  475 	ld	l,-2 (ix)
   54D4 DD 66 FF      [19]  476 	ld	h,-1 (ix)
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
   54E0 DD 7E F6      [19]  487 	ld	a, -10 (ix)
   54E3 D6 38         [ 7]  488 	sub	a, #0x38
   54E5 DD 7E F7      [19]  489 	ld	a, -9 (ix)
   54E8 17            [ 4]  490 	rla
   54E9 3F            [ 4]  491 	ccf
   54EA 1F            [ 4]  492 	rra
   54EB DE 80         [ 7]  493 	sbc	a, #0x80
   54ED 38 12         [12]  494 	jr	C,00107$
   54EF 3E 78         [ 7]  495 	ld	a, #0x78
   54F1 DD BE F6      [19]  496 	cp	a, -10 (ix)
   54F4 3E 00         [ 7]  497 	ld	a, #0x00
   54F6 DD 9E F7      [19]  498 	sbc	a, -9 (ix)
   54F9 E2 FE 54      [10]  499 	jp	PO, 00162$
   54FC EE 80         [ 7]  500 	xor	a, #0x80
   54FE                     501 00162$:
   54FE F2 1D 55      [10]  502 	jp	P, 00108$
   5501                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5501 1A            [ 7]  505 	ld	a, (de)
   5502 6F            [ 4]  506 	ld	l, a
   5503 AF            [ 4]  507 	xor	a, a
   5504 95            [ 4]  508 	sub	a, l
   5505 DD 77 F8      [19]  509 	ld	-8 (ix), a
   5508 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5509 DD 6E F9      [19]  512 	ld	l,-7 (ix)
   550C DD 66 FA      [19]  513 	ld	h,-6 (ix)
   550F 5E            [ 7]  514 	ld	e, (hl)
   5510 16 00         [ 7]  515 	ld	d, #0x00
   5512 DD 6E F8      [19]  516 	ld	l, -8 (ix)
   5515 DD 7E F8      [19]  517 	ld	a, -8 (ix)
   5518 17            [ 4]  518 	rla
   5519 9F            [ 4]  519 	sbc	a, a
   551A 67            [ 4]  520 	ld	h, a
   551B 19            [11]  521 	add	hl,de
   551C E3            [19]  522 	ex	(sp), hl
   551D                     523 00108$:
                            524 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   551D DD 6E FE      [19]  525 	ld	l,-2 (ix)
   5520 DD 66 FF      [19]  526 	ld	h,-1 (ix)
   5523 71            [ 7]  527 	ld	(hl), c
                            528 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   5524 DD 4E F6      [19]  529 	ld	c, -10 (ix)
   5527 DD 6E F9      [19]  530 	ld	l,-7 (ix)
   552A DD 66 FA      [19]  531 	ld	h,-6 (ix)
   552D 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:84: return;
   552E C3 05 56      [10]  534 	jp	00121$
   5531                     535 00111$:
                            536 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            537 ;src/entities/enemy.c:88: if (nextx < 2) {
   5531 79            [ 4]  538 	ld	a, c
   5532 D6 02         [ 7]  539 	sub	a, #0x02
   5534 78            [ 4]  540 	ld	a, b
   5535 17            [ 4]  541 	rla
   5536 3F            [ 4]  542 	ccf
   5537 1F            [ 4]  543 	rra
   5538 DE 80         [ 7]  544 	sbc	a, #0x80
   553A 30 0B         [12]  545 	jr	NC,00113$
                            546 ;src/entities/enemy.c:89: nextx = 2;
   553C 01 02 00      [10]  547 	ld	bc, #0x0002
                            548 ;src/entities/enemy.c:90: enemy->vx = 1;
   553F DD 6E FB      [19]  549 	ld	l,-5 (ix)
   5542 DD 66 FC      [19]  550 	ld	h,-4 (ix)
   5545 36 01         [10]  551 	ld	(hl), #0x01
   5547                     552 00113$:
                            553 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   5547 DD 6E FE      [19]  554 	ld	l,-2 (ix)
   554A DD 66 FF      [19]  555 	ld	h,-1 (ix)
   554D 23            [ 6]  556 	inc	hl
   554E 23            [ 6]  557 	inc	hl
   554F 23            [ 6]  558 	inc	hl
   5550 23            [ 6]  559 	inc	hl
   5551 6E            [ 7]  560 	ld	l, (hl)
   5552 26 00         [ 7]  561 	ld	h, #0x00
   5554 3E 50         [ 7]  562 	ld	a, #0x50
   5556 95            [ 4]  563 	sub	a, l
   5557 6F            [ 4]  564 	ld	l, a
   5558 3E 00         [ 7]  565 	ld	a, #0x00
   555A 9C            [ 4]  566 	sbc	a, h
   555B 67            [ 4]  567 	ld	h, a
                            568 ;src/entities/enemy.c:94: if (nextx > maxx) {
   555C 7D            [ 4]  569 	ld	a, l
   555D 91            [ 4]  570 	sub	a, c
   555E 7C            [ 4]  571 	ld	a, h
   555F 98            [ 4]  572 	sbc	a, b
   5560 E2 65 55      [10]  573 	jp	PO, 00163$
   5563 EE 80         [ 7]  574 	xor	a, #0x80
   5565                     575 00163$:
   5565 F2 71 55      [10]  576 	jp	P, 00115$
                            577 ;src/entities/enemy.c:95: nextx = maxx;
   5568 4D            [ 4]  578 	ld	c, l
                            579 ;src/entities/enemy.c:96: enemy->vx = -1;
   5569 DD 6E FB      [19]  580 	ld	l,-5 (ix)
   556C DD 66 FC      [19]  581 	ld	h,-4 (ix)
   556F 36 FF         [10]  582 	ld	(hl), #0xff
   5571                     583 00115$:
                            584 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   5571 DD 6E FE      [19]  585 	ld	l,-2 (ix)
   5574 DD 66 FF      [19]  586 	ld	h,-1 (ix)
   5577 71            [ 7]  587 	ld	(hl), c
                            588 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   5578 1A            [ 7]  589 	ld	a, (de)
   5579 4F            [ 4]  590 	ld	c, a
   557A 0C            [ 4]  591 	inc	c
   557B 79            [ 4]  592 	ld	a, c
   557C 12            [ 7]  593 	ld	(de), a
                            594 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   557D 3E 03         [ 7]  595 	ld	a, #0x03
   557F 91            [ 4]  596 	sub	a, c
   5580 E2 85 55      [10]  597 	jp	PO, 00164$
   5583 EE 80         [ 7]  598 	xor	a, #0x80
   5585                     599 00164$:
   5585 F2 8B 55      [10]  600 	jp	P, 00117$
   5588 3E 03         [ 7]  601 	ld	a, #0x03
   558A 12            [ 7]  602 	ld	(de), a
   558B                     603 00117$:
                            604 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   558B DD 6E F9      [19]  605 	ld	l,-7 (ix)
   558E DD 66 FA      [19]  606 	ld	h,-6 (ix)
   5591 4E            [ 7]  607 	ld	c, (hl)
   5592 06 00         [ 7]  608 	ld	b, #0x00
   5594 1A            [ 7]  609 	ld	a, (de)
   5595 6F            [ 4]  610 	ld	l, a
   5596 17            [ 4]  611 	rla
   5597 9F            [ 4]  612 	sbc	a, a
   5598 67            [ 4]  613 	ld	h, a
   5599 09            [11]  614 	add	hl, bc
   559A E5            [11]  615 	push	hl
   559B FD E1         [14]  616 	pop	iy
                            617 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   559D DD 7E FE      [19]  618 	ld	a, -2 (ix)
   55A0 C6 05         [ 7]  619 	add	a, #0x05
   55A2 DD 77 F6      [19]  620 	ld	-10 (ix), a
   55A5 DD 7E FF      [19]  621 	ld	a, -1 (ix)
   55A8 CE 00         [ 7]  622 	adc	a, #0x00
   55AA DD 77 F7      [19]  623 	ld	-9 (ix), a
   55AD E1            [10]  624 	pop	hl
   55AE E5            [11]  625 	push	hl
   55AF 7E            [ 7]  626 	ld	a, (hl)
   55B0 DD 6E FE      [19]  627 	ld	l,-2 (ix)
   55B3 DD 66 FF      [19]  628 	ld	h,-1 (ix)
   55B6 4E            [ 7]  629 	ld	c, (hl)
   55B7 06 00         [ 7]  630 	ld	b, #0x00
   55B9 D5            [11]  631 	push	de
   55BA F5            [11]  632 	push	af
   55BB 33            [ 6]  633 	inc	sp
   55BC FD E5         [15]  634 	push	iy
   55BE C5            [11]  635 	push	bc
   55BF CD 29 4C      [17]  636 	call	_collision_clamp_y_at
   55C2 F1            [10]  637 	pop	af
   55C3 F1            [10]  638 	pop	af
   55C4 33            [ 6]  639 	inc	sp
   55C5 4D            [ 4]  640 	ld	c, l
   55C6 D1            [10]  641 	pop	de
                            642 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55C7 DD 6E F9      [19]  643 	ld	l,-7 (ix)
   55CA DD 66 FA      [19]  644 	ld	h,-6 (ix)
   55CD 71            [ 7]  645 	ld	(hl), c
                            646 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55CE E1            [10]  647 	pop	hl
   55CF E5            [11]  648 	push	hl
   55D0 7E            [ 7]  649 	ld	a, (hl)
   55D1 06 00         [ 7]  650 	ld	b, #0x00
   55D3 DD 6E FE      [19]  651 	ld	l,-2 (ix)
   55D6 DD 66 FF      [19]  652 	ld	h,-1 (ix)
   55D9 6E            [ 7]  653 	ld	l, (hl)
   55DA DD 75 F6      [19]  654 	ld	-10 (ix), l
   55DD DD 36 F7 00   [19]  655 	ld	-9 (ix), #0x00
   55E1 D5            [11]  656 	push	de
   55E2 F5            [11]  657 	push	af
   55E3 33            [ 6]  658 	inc	sp
   55E4 C5            [11]  659 	push	bc
   55E5 DD 6E F6      [19]  660 	ld	l,-10 (ix)
   55E8 DD 66 F7      [19]  661 	ld	h,-9 (ix)
   55EB E5            [11]  662 	push	hl
   55EC CD AA 4B      [17]  663 	call	_collision_is_on_ground_at
   55EF F1            [10]  664 	pop	af
   55F0 F1            [10]  665 	pop	af
   55F1 33            [ 6]  666 	inc	sp
   55F2 D1            [10]  667 	pop	de
   55F3 7D            [ 4]  668 	ld	a, l
   55F4 B7            [ 4]  669 	or	a, a
   55F5 28 0E         [12]  670 	jr	Z,00121$
   55F7 1A            [ 7]  671 	ld	a, (de)
   55F8 4F            [ 4]  672 	ld	c, a
   55F9 AF            [ 4]  673 	xor	a, a
   55FA 91            [ 4]  674 	sub	a, c
   55FB E2 00 56      [10]  675 	jp	PO, 00165$
   55FE EE 80         [ 7]  676 	xor	a, #0x80
   5600                     677 00165$:
   5600 F2 05 56      [10]  678 	jp	P, 00121$
                            679 ;src/entities/enemy.c:107: enemy->vy = 0;
   5603 AF            [ 4]  680 	xor	a, a
   5604 12            [ 7]  681 	ld	(de), a
   5605                     682 00121$:
   5605 DD F9         [10]  683 	ld	sp, ix
   5607 DD E1         [14]  684 	pop	ix
   5609 C9            [10]  685 	ret
                            686 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            687 ;	---------------------------------
                            688 ; Function enemyrender
                            689 ; ---------------------------------
   560A                     690 _enemyrender::
   560A DD E5         [15]  691 	push	ix
   560C DD 21 00 00   [14]  692 	ld	ix,#0
   5610 DD 39         [15]  693 	add	ix,sp
   5612 F5            [11]  694 	push	af
                            695 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5613 DD 7E 05      [19]  696 	ld	a, 5 (ix)
   5616 DD B6 04      [19]  697 	or	a,4 (ix)
   5619 CA 97 56      [10]  698 	jp	Z,00113$
   561C DD 7E 04      [19]  699 	ld	a, 4 (ix)
   561F DD 77 FE      [19]  700 	ld	-2 (ix), a
   5622 DD 7E 05      [19]  701 	ld	a, 5 (ix)
   5625 DD 77 FF      [19]  702 	ld	-1 (ix), a
   5628 E1            [10]  703 	pop	hl
   5629 E5            [11]  704 	push	hl
   562A 11 06 00      [10]  705 	ld	de, #0x0006
   562D 19            [11]  706 	add	hl, de
   562E 7E            [ 7]  707 	ld	a, (hl)
   562F B7            [ 4]  708 	or	a, a
                            709 ;src/entities/enemy.c:116: return;
   5630 28 65         [12]  710 	jr	Z,00113$
                            711 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   5632 E1            [10]  712 	pop	hl
   5633 E5            [11]  713 	push	hl
   5634 11 09 00      [10]  714 	ld	de, #0x0009
   5637 19            [11]  715 	add	hl, de
   5638 7E            [ 7]  716 	ld	a, (hl)
   5639 FE 03         [ 7]  717 	cp	a, #0x03
   563B 20 0A         [12]  718 	jr	NZ,00111$
   563D 21 0C 0C      [10]  719 	ld	hl, #0x0c0c
   5640 E5            [11]  720 	push	hl
   5641 CD 59 5D      [17]  721 	call	_cpct_px2byteM0
   5644 4D            [ 4]  722 	ld	c, l
   5645 18 23         [12]  723 	jr	00112$
   5647                     724 00111$:
                            725 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   5647 FE 02         [ 7]  726 	cp	a, #0x02
   5649 20 0A         [12]  727 	jr	NZ,00108$
   564B 21 0A 0A      [10]  728 	ld	hl, #0x0a0a
   564E E5            [11]  729 	push	hl
   564F CD 59 5D      [17]  730 	call	_cpct_px2byteM0
   5652 4D            [ 4]  731 	ld	c, l
   5653 18 15         [12]  732 	jr	00112$
   5655                     733 00108$:
                            734 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   5655 3D            [ 4]  735 	dec	a
   5656 20 0A         [12]  736 	jr	NZ,00105$
   5658 21 0E 0E      [10]  737 	ld	hl, #0x0e0e
   565B E5            [11]  738 	push	hl
   565C CD 59 5D      [17]  739 	call	_cpct_px2byteM0
   565F 4D            [ 4]  740 	ld	c, l
   5660 18 08         [12]  741 	jr	00112$
   5662                     742 00105$:
                            743 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   5662 21 04 04      [10]  744 	ld	hl, #0x0404
   5665 E5            [11]  745 	push	hl
   5666 CD 59 5D      [17]  746 	call	_cpct_px2byteM0
   5669 4D            [ 4]  747 	ld	c, l
   566A                     748 00112$:
                            749 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   566A E1            [10]  750 	pop	hl
   566B E5            [11]  751 	push	hl
   566C 23            [ 6]  752 	inc	hl
   566D 46            [ 7]  753 	ld	b, (hl)
   566E E1            [10]  754 	pop	hl
   566F E5            [11]  755 	push	hl
   5670 56            [ 7]  756 	ld	d, (hl)
   5671 C5            [11]  757 	push	bc
   5672 4A            [ 4]  758 	ld	c, d
   5673 C5            [11]  759 	push	bc
   5674 21 00 C0      [10]  760 	ld	hl, #0xc000
   5677 E5            [11]  761 	push	hl
   5678 CD 4C 5E      [17]  762 	call	_cpct_getScreenPtr
   567B EB            [ 4]  763 	ex	de,hl
   567C C1            [10]  764 	pop	bc
                            765 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   567D E1            [10]  766 	pop	hl
   567E E5            [11]  767 	push	hl
   567F 23            [ 6]  768 	inc	hl
   5680 23            [ 6]  769 	inc	hl
   5681 23            [ 6]  770 	inc	hl
   5682 23            [ 6]  771 	inc	hl
   5683 23            [ 6]  772 	inc	hl
   5684 46            [ 7]  773 	ld	b, (hl)
   5685 E1            [10]  774 	pop	hl
   5686 E5            [11]  775 	push	hl
   5687 23            [ 6]  776 	inc	hl
   5688 23            [ 6]  777 	inc	hl
   5689 23            [ 6]  778 	inc	hl
   568A 23            [ 6]  779 	inc	hl
   568B 7E            [ 7]  780 	ld	a, (hl)
   568C C5            [11]  781 	push	bc
   568D 33            [ 6]  782 	inc	sp
   568E 47            [ 4]  783 	ld	b, a
   568F C5            [11]  784 	push	bc
   5690 D5            [11]  785 	push	de
   5691 CD 93 5D      [17]  786 	call	_cpct_drawSolidBox
   5694 F1            [10]  787 	pop	af
   5695 F1            [10]  788 	pop	af
   5696 33            [ 6]  789 	inc	sp
   5697                     790 00113$:
   5697 DD F9         [10]  791 	ld	sp, ix
   5699 DD E1         [14]  792 	pop	ix
   569B C9            [10]  793 	ret
                            794 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            795 ;	---------------------------------
                            796 ; Function enemydamage
                            797 ; ---------------------------------
   569C                     798 _enemydamage::
   569C DD E5         [15]  799 	push	ix
   569E DD 21 00 00   [14]  800 	ld	ix,#0
   56A2 DD 39         [15]  801 	add	ix,sp
                            802 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   56A4 DD 7E 05      [19]  803 	ld	a, 5 (ix)
   56A7 DD B6 04      [19]  804 	or	a,4 (ix)
   56AA 28 0F         [12]  805 	jr	Z,00101$
   56AC DD 4E 04      [19]  806 	ld	c,4 (ix)
   56AF DD 46 05      [19]  807 	ld	b,5 (ix)
   56B2 21 06 00      [10]  808 	ld	hl, #0x0006
   56B5 09            [11]  809 	add	hl,bc
   56B6 EB            [ 4]  810 	ex	de,hl
   56B7 1A            [ 7]  811 	ld	a, (de)
   56B8 B7            [ 4]  812 	or	a, a
   56B9 20 04         [12]  813 	jr	NZ,00102$
   56BB                     814 00101$:
                            815 ;src/entities/enemy.c:130: return 0;
   56BB 2E 00         [ 7]  816 	ld	l, #0x00
   56BD 18 1A         [12]  817 	jr	00106$
   56BF                     818 00102$:
                            819 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56BF 21 07 00      [10]  820 	ld	hl, #0x0007
   56C2 09            [11]  821 	add	hl, bc
   56C3 4E            [ 7]  822 	ld	c, (hl)
   56C4 DD 7E 06      [19]  823 	ld	a, 6 (ix)
   56C7 91            [ 4]  824 	sub	a, c
   56C8 38 08         [12]  825 	jr	C,00105$
                            826 ;src/entities/enemy.c:134: enemy->health = 0;
   56CA 36 00         [10]  827 	ld	(hl), #0x00
                            828 ;src/entities/enemy.c:135: enemy->active = 0;
   56CC AF            [ 4]  829 	xor	a, a
   56CD 12            [ 7]  830 	ld	(de), a
                            831 ;src/entities/enemy.c:136: return 1;
   56CE 2E 01         [ 7]  832 	ld	l, #0x01
   56D0 18 07         [12]  833 	jr	00106$
   56D2                     834 00105$:
                            835 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   56D2 79            [ 4]  836 	ld	a, c
   56D3 DD 96 06      [19]  837 	sub	a, 6 (ix)
   56D6 77            [ 7]  838 	ld	(hl), a
                            839 ;src/entities/enemy.c:140: return 0;
   56D7 2E 00         [ 7]  840 	ld	l, #0x00
   56D9                     841 00106$:
   56D9 DD E1         [14]  842 	pop	ix
   56DB C9            [10]  843 	ret
                            844 	.area _CODE
                            845 	.area _INITIALIZER
                            846 	.area _CABS (ABS)
