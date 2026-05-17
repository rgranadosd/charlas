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
   51F0                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   51F0 21 03 00      [10]   58 	ld	hl, #2+1
   51F3 39            [11]   59 	add	hl, sp
   51F4 7E            [ 7]   60 	ld	a, (hl)
   51F5 2B            [ 6]   61 	dec	hl
   51F6 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   51F7 C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   51F8 D1            [10]   66 	pop	de
   51F9 C1            [10]   67 	pop	bc
   51FA C5            [11]   68 	push	bc
   51FB D5            [11]   69 	push	de
   51FC AF            [ 4]   70 	xor	a, a
   51FD 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   51FE 59            [ 4]   73 	ld	e, c
   51FF 50            [ 4]   74 	ld	d, b
   5200 13            [ 6]   75 	inc	de
   5201 AF            [ 4]   76 	xor	a, a
   5202 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   5203 59            [ 4]   79 	ld	e, c
   5204 50            [ 4]   80 	ld	d, b
   5205 13            [ 6]   81 	inc	de
   5206 13            [ 6]   82 	inc	de
   5207 AF            [ 4]   83 	xor	a, a
   5208 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   5209 59            [ 4]   86 	ld	e, c
   520A 50            [ 4]   87 	ld	d, b
   520B 13            [ 6]   88 	inc	de
   520C 13            [ 6]   89 	inc	de
   520D 13            [ 6]   90 	inc	de
   520E AF            [ 4]   91 	xor	a, a
   520F 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   5210 21 04 00      [10]   94 	ld	hl, #0x0004
   5213 09            [11]   95 	add	hl, bc
   5214 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   5216 21 05 00      [10]   98 	ld	hl, #0x0005
   5219 09            [11]   99 	add	hl, bc
   521A 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   521C 21 06 00      [10]  102 	ld	hl, #0x0006
   521F 09            [11]  103 	add	hl, bc
   5220 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   5222 21 07 00      [10]  106 	ld	hl, #0x0007
   5225 09            [11]  107 	add	hl, bc
   5226 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   5228 21 08 00      [10]  110 	ld	hl, #0x0008
   522B 09            [11]  111 	add	hl, bc
   522C 36 64         [10]  112 	ld	(hl), #0x64
                            113 ;src/entities/enemy.c:19: enemy->kind = 0;
   522E 21 09 00      [10]  114 	ld	hl, #0x0009
   5231 09            [11]  115 	add	hl, bc
   5232 36 00         [10]  116 	ld	(hl), #0x00
   5234 C9            [10]  117 	ret
                            118 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            119 ;	---------------------------------
                            120 ; Function enemyspawn
                            121 ; ---------------------------------
   5235                     122 _enemyspawn::
   5235 DD E5         [15]  123 	push	ix
   5237 DD 21 00 00   [14]  124 	ld	ix,#0
   523B DD 39         [15]  125 	add	ix,sp
   523D 21 F1 FF      [10]  126 	ld	hl, #-15
   5240 39            [11]  127 	add	hl, sp
   5241 F9            [ 6]  128 	ld	sp, hl
                            129 ;src/entities/enemy.c:23: if (!enemy) {
   5242 DD 7E 05      [19]  130 	ld	a, 5 (ix)
   5245 DD B6 04      [19]  131 	or	a,4 (ix)
                            132 ;src/entities/enemy.c:24: return;
   5248 CA 08 54      [10]  133 	jp	Z,00112$
                            134 ;src/entities/enemy.c:27: enemy->x = x;
   524B DD 7E 04      [19]  135 	ld	a, 4 (ix)
   524E DD 77 FE      [19]  136 	ld	-2 (ix), a
   5251 DD 7E 05      [19]  137 	ld	a, 5 (ix)
   5254 DD 77 FF      [19]  138 	ld	-1 (ix), a
   5257 DD 6E FE      [19]  139 	ld	l,-2 (ix)
   525A DD 66 FF      [19]  140 	ld	h,-1 (ix)
   525D DD 7E 06      [19]  141 	ld	a, 6 (ix)
   5260 77            [ 7]  142 	ld	(hl), a
                            143 ;src/entities/enemy.c:28: enemy->y = y;
   5261 DD 4E FE      [19]  144 	ld	c,-2 (ix)
   5264 DD 46 FF      [19]  145 	ld	b,-1 (ix)
   5267 03            [ 6]  146 	inc	bc
   5268 DD 7E 07      [19]  147 	ld	a, 7 (ix)
   526B 02            [ 7]  148 	ld	(bc), a
                            149 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   526C DD 7E FE      [19]  150 	ld	a, -2 (ix)
   526F C6 02         [ 7]  151 	add	a, #0x02
   5271 DD 77 FC      [19]  152 	ld	-4 (ix), a
   5274 DD 7E FF      [19]  153 	ld	a, -1 (ix)
   5277 CE 00         [ 7]  154 	adc	a, #0x00
   5279 DD 77 FD      [19]  155 	ld	-3 (ix), a
   527C DD 7E 09      [19]  156 	ld	a, 9 (ix)
   527F B7            [ 4]  157 	or	a, a
   5280 28 04         [12]  158 	jr	Z,00114$
   5282 0E 01         [ 7]  159 	ld	c, #0x01
   5284 18 02         [12]  160 	jr	00115$
   5286                     161 00114$:
   5286 0E FF         [ 7]  162 	ld	c, #0xff
   5288                     163 00115$:
   5288 DD 6E FC      [19]  164 	ld	l,-4 (ix)
   528B DD 66 FD      [19]  165 	ld	h,-3 (ix)
   528E 71            [ 7]  166 	ld	(hl), c
                            167 ;src/entities/enemy.c:30: enemy->vy = 0;
   528F DD 7E FE      [19]  168 	ld	a, -2 (ix)
   5292 C6 03         [ 7]  169 	add	a, #0x03
   5294 DD 77 FA      [19]  170 	ld	-6 (ix), a
   5297 DD 7E FF      [19]  171 	ld	a, -1 (ix)
   529A CE 00         [ 7]  172 	adc	a, #0x00
   529C DD 77 FB      [19]  173 	ld	-5 (ix), a
   529F DD 6E FA      [19]  174 	ld	l,-6 (ix)
   52A2 DD 66 FB      [19]  175 	ld	h,-5 (ix)
   52A5 36 00         [10]  176 	ld	(hl), #0x00
                            177 ;src/entities/enemy.c:31: enemy->active = 1;
   52A7 DD 7E FE      [19]  178 	ld	a, -2 (ix)
   52AA C6 06         [ 7]  179 	add	a, #0x06
   52AC DD 77 F8      [19]  180 	ld	-8 (ix), a
   52AF DD 7E FF      [19]  181 	ld	a, -1 (ix)
   52B2 CE 00         [ 7]  182 	adc	a, #0x00
   52B4 DD 77 F9      [19]  183 	ld	-7 (ix), a
   52B7 DD 6E F8      [19]  184 	ld	l,-8 (ix)
   52BA DD 66 F9      [19]  185 	ld	h,-7 (ix)
   52BD 36 01         [10]  186 	ld	(hl), #0x01
                            187 ;src/entities/enemy.c:32: enemy->kind = kind;
   52BF DD 7E FE      [19]  188 	ld	a, -2 (ix)
   52C2 C6 09         [ 7]  189 	add	a, #0x09
   52C4 DD 77 F8      [19]  190 	ld	-8 (ix), a
   52C7 DD 7E FF      [19]  191 	ld	a, -1 (ix)
   52CA CE 00         [ 7]  192 	adc	a, #0x00
   52CC DD 77 F9      [19]  193 	ld	-7 (ix), a
   52CF DD 6E F8      [19]  194 	ld	l,-8 (ix)
   52D2 DD 66 F9      [19]  195 	ld	h,-7 (ix)
   52D5 DD 7E 08      [19]  196 	ld	a, 8 (ix)
   52D8 77            [ 7]  197 	ld	(hl), a
                            198 ;src/entities/enemy.c:35: enemy->w = 5;
   52D9 DD 7E FE      [19]  199 	ld	a, -2 (ix)
   52DC C6 04         [ 7]  200 	add	a, #0x04
   52DE DD 77 F8      [19]  201 	ld	-8 (ix), a
   52E1 DD 7E FF      [19]  202 	ld	a, -1 (ix)
   52E4 CE 00         [ 7]  203 	adc	a, #0x00
   52E6 DD 77 F9      [19]  204 	ld	-7 (ix), a
                            205 ;src/entities/enemy.c:36: enemy->h = 14;
   52E9 DD 7E FE      [19]  206 	ld	a, -2 (ix)
   52EC C6 05         [ 7]  207 	add	a, #0x05
   52EE DD 77 F6      [19]  208 	ld	-10 (ix), a
   52F1 DD 7E FF      [19]  209 	ld	a, -1 (ix)
   52F4 CE 00         [ 7]  210 	adc	a, #0x00
   52F6 DD 77 F7      [19]  211 	ld	-9 (ix), a
                            212 ;src/entities/enemy.c:37: enemy->health = 2;
   52F9 DD 7E FE      [19]  213 	ld	a, -2 (ix)
   52FC C6 07         [ 7]  214 	add	a, #0x07
   52FE DD 77 F4      [19]  215 	ld	-12 (ix), a
   5301 DD 7E FF      [19]  216 	ld	a, -1 (ix)
   5304 CE 00         [ 7]  217 	adc	a, #0x00
   5306 DD 77 F5      [19]  218 	ld	-11 (ix), a
                            219 ;src/entities/enemy.c:38: enemy->reward = 180;
   5309 DD 7E FE      [19]  220 	ld	a, -2 (ix)
   530C C6 08         [ 7]  221 	add	a, #0x08
   530E DD 77 FE      [19]  222 	ld	-2 (ix), a
   5311 DD 7E FF      [19]  223 	ld	a, -1 (ix)
   5314 CE 00         [ 7]  224 	adc	a, #0x00
   5316 DD 77 FF      [19]  225 	ld	-1 (ix), a
                            226 ;src/entities/enemy.c:34: if (kind == 1) {
   5319 DD 7E 08      [19]  227 	ld	a, 8 (ix)
   531C 3D            [ 4]  228 	dec	a
   531D 20 49         [12]  229 	jr	NZ,00110$
                            230 ;src/entities/enemy.c:35: enemy->w = 5;
   531F DD 6E F8      [19]  231 	ld	l,-8 (ix)
   5322 DD 66 F9      [19]  232 	ld	h,-7 (ix)
   5325 36 05         [10]  233 	ld	(hl), #0x05
                            234 ;src/entities/enemy.c:36: enemy->h = 14;
   5327 DD 6E F6      [19]  235 	ld	l,-10 (ix)
   532A DD 66 F7      [19]  236 	ld	h,-9 (ix)
   532D 36 0E         [10]  237 	ld	(hl), #0x0e
                            238 ;src/entities/enemy.c:37: enemy->health = 2;
   532F DD 6E F4      [19]  239 	ld	l,-12 (ix)
   5332 DD 66 F5      [19]  240 	ld	h,-11 (ix)
   5335 36 02         [10]  241 	ld	(hl), #0x02
                            242 ;src/entities/enemy.c:38: enemy->reward = 180;
   5337 DD 6E FE      [19]  243 	ld	l,-2 (ix)
   533A DD 66 FF      [19]  244 	ld	h,-1 (ix)
   533D 36 B4         [10]  245 	ld	(hl), #0xb4
                            246 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   533F DD 7E FC      [19]  247 	ld	a, -4 (ix)
   5342 DD 77 F2      [19]  248 	ld	-14 (ix), a
   5345 DD 7E FD      [19]  249 	ld	a, -3 (ix)
   5348 DD 77 F3      [19]  250 	ld	-13 (ix), a
   534B DD 7E 09      [19]  251 	ld	a, 9 (ix)
   534E B7            [ 4]  252 	or	a, a
   534F 28 06         [12]  253 	jr	Z,00116$
   5351 DD 36 F1 02   [19]  254 	ld	-15 (ix), #0x02
   5355 18 04         [12]  255 	jr	00117$
   5357                     256 00116$:
   5357 DD 36 F1 FE   [19]  257 	ld	-15 (ix), #0xfe
   535B                     258 00117$:
   535B DD 6E F2      [19]  259 	ld	l,-14 (ix)
   535E DD 66 F3      [19]  260 	ld	h,-13 (ix)
   5361 DD 7E F1      [19]  261 	ld	a, -15 (ix)
   5364 77            [ 7]  262 	ld	(hl), a
   5365 C3 08 54      [10]  263 	jp	00112$
   5368                     264 00110$:
                            265 ;src/entities/enemy.c:40: } else if (kind == 2) {
   5368 DD 7E 08      [19]  266 	ld	a, 8 (ix)
   536B D6 02         [ 7]  267 	sub	a, #0x02
   536D 20 3D         [12]  268 	jr	NZ,00107$
                            269 ;src/entities/enemy.c:41: enemy->w = 6;
   536F DD 6E F8      [19]  270 	ld	l,-8 (ix)
   5372 DD 66 F9      [19]  271 	ld	h,-7 (ix)
   5375 36 06         [10]  272 	ld	(hl), #0x06
                            273 ;src/entities/enemy.c:42: enemy->h = 10;
   5377 DD 6E F6      [19]  274 	ld	l,-10 (ix)
   537A DD 66 F7      [19]  275 	ld	h,-9 (ix)
   537D 36 0A         [10]  276 	ld	(hl), #0x0a
                            277 ;src/entities/enemy.c:43: enemy->health = 1;
   537F DD 6E F4      [19]  278 	ld	l,-12 (ix)
   5382 DD 66 F5      [19]  279 	ld	h,-11 (ix)
   5385 36 01         [10]  280 	ld	(hl), #0x01
                            281 ;src/entities/enemy.c:44: enemy->reward = 150;
   5387 DD 6E FE      [19]  282 	ld	l,-2 (ix)
   538A DD 66 FF      [19]  283 	ld	h,-1 (ix)
   538D 36 96         [10]  284 	ld	(hl), #0x96
                            285 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   538F DD 4E FA      [19]  286 	ld	c,-6 (ix)
   5392 DD 46 FB      [19]  287 	ld	b,-5 (ix)
   5395 DD 7E 09      [19]  288 	ld	a, 9 (ix)
   5398 B7            [ 4]  289 	or	a, a
   5399 28 04         [12]  290 	jr	Z,00118$
   539B 3E 01         [ 7]  291 	ld	a, #0x01
   539D 18 02         [12]  292 	jr	00119$
   539F                     293 00118$:
   539F 3E FF         [ 7]  294 	ld	a, #0xff
   53A1                     295 00119$:
   53A1 02            [ 7]  296 	ld	(bc), a
                            297 ;src/entities/enemy.c:46: enemy->vx = 1;
   53A2 DD 6E FC      [19]  298 	ld	l,-4 (ix)
   53A5 DD 66 FD      [19]  299 	ld	h,-3 (ix)
   53A8 36 01         [10]  300 	ld	(hl), #0x01
   53AA 18 5C         [12]  301 	jr	00112$
   53AC                     302 00107$:
                            303 ;src/entities/enemy.c:47: } else if (kind == 3) {
   53AC DD 7E 08      [19]  304 	ld	a, 8 (ix)
   53AF D6 03         [ 7]  305 	sub	a, #0x03
   53B1 20 35         [12]  306 	jr	NZ,00104$
                            307 ;src/entities/enemy.c:48: enemy->w = 10;
   53B3 DD 6E F8      [19]  308 	ld	l,-8 (ix)
   53B6 DD 66 F9      [19]  309 	ld	h,-7 (ix)
   53B9 36 0A         [10]  310 	ld	(hl), #0x0a
                            311 ;src/entities/enemy.c:49: enemy->h = 18;
   53BB DD 6E F6      [19]  312 	ld	l,-10 (ix)
   53BE DD 66 F7      [19]  313 	ld	h,-9 (ix)
   53C1 36 12         [10]  314 	ld	(hl), #0x12
                            315 ;src/entities/enemy.c:50: enemy->health = 8;
   53C3 DD 6E F4      [19]  316 	ld	l,-12 (ix)
   53C6 DD 66 F5      [19]  317 	ld	h,-11 (ix)
   53C9 36 08         [10]  318 	ld	(hl), #0x08
                            319 ;src/entities/enemy.c:51: enemy->reward = 800;
   53CB DD 6E FE      [19]  320 	ld	l,-2 (ix)
   53CE DD 66 FF      [19]  321 	ld	h,-1 (ix)
   53D1 36 20         [10]  322 	ld	(hl), #0x20
                            323 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   53D3 DD 4E FC      [19]  324 	ld	c,-4 (ix)
   53D6 DD 46 FD      [19]  325 	ld	b,-3 (ix)
   53D9 DD 7E 09      [19]  326 	ld	a, 9 (ix)
   53DC B7            [ 4]  327 	or	a, a
   53DD 28 04         [12]  328 	jr	Z,00120$
   53DF 3E 01         [ 7]  329 	ld	a, #0x01
   53E1 18 02         [12]  330 	jr	00121$
   53E3                     331 00120$:
   53E3 3E FF         [ 7]  332 	ld	a, #0xff
   53E5                     333 00121$:
   53E5 02            [ 7]  334 	ld	(bc), a
   53E6 18 20         [12]  335 	jr	00112$
   53E8                     336 00104$:
                            337 ;src/entities/enemy.c:54: enemy->w = 4;
   53E8 DD 6E F8      [19]  338 	ld	l,-8 (ix)
   53EB DD 66 F9      [19]  339 	ld	h,-7 (ix)
   53EE 36 04         [10]  340 	ld	(hl), #0x04
                            341 ;src/entities/enemy.c:55: enemy->h = 16;
   53F0 DD 6E F6      [19]  342 	ld	l,-10 (ix)
   53F3 DD 66 F7      [19]  343 	ld	h,-9 (ix)
   53F6 36 10         [10]  344 	ld	(hl), #0x10
                            345 ;src/entities/enemy.c:56: enemy->health = 1;
   53F8 DD 6E F4      [19]  346 	ld	l,-12 (ix)
   53FB DD 66 F5      [19]  347 	ld	h,-11 (ix)
   53FE 36 01         [10]  348 	ld	(hl), #0x01
                            349 ;src/entities/enemy.c:57: enemy->reward = 100;
   5400 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   5403 DD 66 FF      [19]  351 	ld	h,-1 (ix)
   5406 36 64         [10]  352 	ld	(hl), #0x64
   5408                     353 00112$:
   5408 DD F9         [10]  354 	ld	sp, ix
   540A DD E1         [14]  355 	pop	ix
   540C C9            [10]  356 	ret
                            357 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            358 ;	---------------------------------
                            359 ; Function enemyupdate
                            360 ; ---------------------------------
   540D                     361 _enemyupdate::
   540D DD E5         [15]  362 	push	ix
   540F DD 21 00 00   [14]  363 	ld	ix,#0
   5413 DD 39         [15]  364 	add	ix,sp
   5415 21 F6 FF      [10]  365 	ld	hl, #-10
   5418 39            [11]  366 	add	hl, sp
   5419 F9            [ 6]  367 	ld	sp, hl
                            368 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   541A DD 7E 05      [19]  369 	ld	a, 5 (ix)
   541D DD B6 04      [19]  370 	or	a,4 (ix)
   5420 CA 14 56      [10]  371 	jp	Z,00121$
   5423 DD 7E 04      [19]  372 	ld	a, 4 (ix)
   5426 DD 77 FE      [19]  373 	ld	-2 (ix), a
   5429 DD 7E 05      [19]  374 	ld	a, 5 (ix)
   542C DD 77 FF      [19]  375 	ld	-1 (ix), a
   542F DD 6E FE      [19]  376 	ld	l,-2 (ix)
   5432 DD 66 FF      [19]  377 	ld	h,-1 (ix)
   5435 11 06 00      [10]  378 	ld	de, #0x0006
   5438 19            [11]  379 	add	hl, de
   5439 7E            [ 7]  380 	ld	a, (hl)
   543A B7            [ 4]  381 	or	a, a
                            382 ;src/entities/enemy.c:66: return;
   543B CA 14 56      [10]  383 	jp	Z,00121$
                            384 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   543E DD 6E FE      [19]  385 	ld	l,-2 (ix)
   5441 DD 66 FF      [19]  386 	ld	h,-1 (ix)
   5444 11 09 00      [10]  387 	ld	de, #0x0009
   5447 19            [11]  388 	add	hl, de
   5448 7E            [ 7]  389 	ld	a, (hl)
   5449 DD 77 FD      [19]  390 	ld	-3 (ix), a
                            391 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   544C DD 6E FE      [19]  392 	ld	l,-2 (ix)
   544F DD 66 FF      [19]  393 	ld	h,-1 (ix)
   5452 4E            [ 7]  394 	ld	c, (hl)
   5453 DD 7E FE      [19]  395 	ld	a, -2 (ix)
   5456 C6 02         [ 7]  396 	add	a, #0x02
   5458 DD 77 FB      [19]  397 	ld	-5 (ix), a
   545B DD 7E FF      [19]  398 	ld	a, -1 (ix)
   545E CE 00         [ 7]  399 	adc	a, #0x00
   5460 DD 77 FC      [19]  400 	ld	-4 (ix), a
                            401 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5463 DD 7E FE      [19]  402 	ld	a, -2 (ix)
   5466 C6 01         [ 7]  403 	add	a, #0x01
   5468 DD 77 F9      [19]  404 	ld	-7 (ix), a
   546B DD 7E FF      [19]  405 	ld	a, -1 (ix)
   546E CE 00         [ 7]  406 	adc	a, #0x00
   5470 DD 77 FA      [19]  407 	ld	-6 (ix), a
   5473 DD 5E FE      [19]  408 	ld	e,-2 (ix)
   5476 DD 56 FF      [19]  409 	ld	d,-1 (ix)
   5479 13            [ 6]  410 	inc	de
   547A 13            [ 6]  411 	inc	de
   547B 13            [ 6]  412 	inc	de
                            413 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   547C 06 00         [ 7]  414 	ld	b, #0x00
   547E DD 6E FB      [19]  415 	ld	l,-5 (ix)
   5481 DD 66 FC      [19]  416 	ld	h,-4 (ix)
   5484 7E            [ 7]  417 	ld	a, (hl)
   5485 DD 77 F8      [19]  418 	ld	-8 (ix), a
   5488 6F            [ 4]  419 	ld	l, a
   5489 DD 7E F8      [19]  420 	ld	a, -8 (ix)
   548C 17            [ 4]  421 	rla
   548D 9F            [ 4]  422 	sbc	a, a
   548E 67            [ 4]  423 	ld	h, a
   548F 09            [11]  424 	add	hl,bc
   5490 4D            [ 4]  425 	ld	c, l
   5491 44            [ 4]  426 	ld	b, h
                            427 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5492 DD 7E FD      [19]  428 	ld	a, -3 (ix)
   5495 D6 02         [ 7]  429 	sub	a, #0x02
   5497 C2 40 55      [10]  430 	jp	NZ,00111$
                            431 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            432 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   549A DD 6E F9      [19]  433 	ld	l,-7 (ix)
   549D DD 66 FA      [19]  434 	ld	h,-6 (ix)
   54A0 6E            [ 7]  435 	ld	l, (hl)
   54A1 DD 75 F6      [19]  436 	ld	-10 (ix), l
   54A4 DD 36 F7 00   [19]  437 	ld	-9 (ix), #0x00
   54A8 1A            [ 7]  438 	ld	a, (de)
   54A9 6F            [ 4]  439 	ld	l, a
   54AA 17            [ 4]  440 	rla
   54AB 9F            [ 4]  441 	sbc	a, a
   54AC 67            [ 4]  442 	ld	h, a
   54AD DD 7E F6      [19]  443 	ld	a, -10 (ix)
   54B0 85            [ 4]  444 	add	a, l
   54B1 DD 77 F6      [19]  445 	ld	-10 (ix), a
   54B4 DD 7E F7      [19]  446 	ld	a, -9 (ix)
   54B7 8C            [ 4]  447 	adc	a, h
   54B8 DD 77 F7      [19]  448 	ld	-9 (ix), a
                            449 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   54BB 79            [ 4]  450 	ld	a, c
   54BC D6 08         [ 7]  451 	sub	a, #0x08
   54BE 78            [ 4]  452 	ld	a, b
   54BF 17            [ 4]  453 	rla
   54C0 3F            [ 4]  454 	ccf
   54C1 1F            [ 4]  455 	rra
   54C2 DE 80         [ 7]  456 	sbc	a, #0x80
   54C4 38 0E         [12]  457 	jr	C,00104$
   54C6 3E 48         [ 7]  458 	ld	a, #0x48
   54C8 B9            [ 4]  459 	cp	a, c
   54C9 3E 00         [ 7]  460 	ld	a, #0x00
   54CB 98            [ 4]  461 	sbc	a, b
   54CC E2 D1 54      [10]  462 	jp	PO, 00161$
   54CF EE 80         [ 7]  463 	xor	a, #0x80
   54D1                     464 00161$:
   54D1 F2 EF 54      [10]  465 	jp	P, 00105$
   54D4                     466 00104$:
                            467 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   54D4 AF            [ 4]  468 	xor	a, a
   54D5 DD 96 F8      [19]  469 	sub	a, -8 (ix)
   54D8 4F            [ 4]  470 	ld	c, a
   54D9 DD 6E FB      [19]  471 	ld	l,-5 (ix)
   54DC DD 66 FC      [19]  472 	ld	h,-4 (ix)
   54DF 71            [ 7]  473 	ld	(hl), c
                            474 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   54E0 DD 6E FE      [19]  475 	ld	l,-2 (ix)
   54E3 DD 66 FF      [19]  476 	ld	h,-1 (ix)
   54E6 6E            [ 7]  477 	ld	l, (hl)
   54E7 26 00         [ 7]  478 	ld	h, #0x00
   54E9 79            [ 4]  479 	ld	a, c
   54EA 17            [ 4]  480 	rla
   54EB 9F            [ 4]  481 	sbc	a, a
   54EC 47            [ 4]  482 	ld	b, a
   54ED 09            [11]  483 	add	hl,bc
   54EE 4D            [ 4]  484 	ld	c, l
   54EF                     485 00105$:
                            486 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   54EF DD 7E F6      [19]  487 	ld	a, -10 (ix)
   54F2 D6 38         [ 7]  488 	sub	a, #0x38
   54F4 DD 7E F7      [19]  489 	ld	a, -9 (ix)
   54F7 17            [ 4]  490 	rla
   54F8 3F            [ 4]  491 	ccf
   54F9 1F            [ 4]  492 	rra
   54FA DE 80         [ 7]  493 	sbc	a, #0x80
   54FC 38 12         [12]  494 	jr	C,00107$
   54FE 3E 78         [ 7]  495 	ld	a, #0x78
   5500 DD BE F6      [19]  496 	cp	a, -10 (ix)
   5503 3E 00         [ 7]  497 	ld	a, #0x00
   5505 DD 9E F7      [19]  498 	sbc	a, -9 (ix)
   5508 E2 0D 55      [10]  499 	jp	PO, 00162$
   550B EE 80         [ 7]  500 	xor	a, #0x80
   550D                     501 00162$:
   550D F2 2C 55      [10]  502 	jp	P, 00108$
   5510                     503 00107$:
                            504 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5510 1A            [ 7]  505 	ld	a, (de)
   5511 6F            [ 4]  506 	ld	l, a
   5512 AF            [ 4]  507 	xor	a, a
   5513 95            [ 4]  508 	sub	a, l
   5514 DD 77 F8      [19]  509 	ld	-8 (ix), a
   5517 12            [ 7]  510 	ld	(de),a
                            511 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5518 DD 6E F9      [19]  512 	ld	l,-7 (ix)
   551B DD 66 FA      [19]  513 	ld	h,-6 (ix)
   551E 5E            [ 7]  514 	ld	e, (hl)
   551F 16 00         [ 7]  515 	ld	d, #0x00
   5521 DD 6E F8      [19]  516 	ld	l, -8 (ix)
   5524 DD 7E F8      [19]  517 	ld	a, -8 (ix)
   5527 17            [ 4]  518 	rla
   5528 9F            [ 4]  519 	sbc	a, a
   5529 67            [ 4]  520 	ld	h, a
   552A 19            [11]  521 	add	hl,de
   552B E3            [19]  522 	ex	(sp), hl
   552C                     523 00108$:
                            524 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   552C DD 6E FE      [19]  525 	ld	l,-2 (ix)
   552F DD 66 FF      [19]  526 	ld	h,-1 (ix)
   5532 71            [ 7]  527 	ld	(hl), c
                            528 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   5533 DD 4E F6      [19]  529 	ld	c, -10 (ix)
   5536 DD 6E F9      [19]  530 	ld	l,-7 (ix)
   5539 DD 66 FA      [19]  531 	ld	h,-6 (ix)
   553C 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:84: return;
   553D C3 14 56      [10]  534 	jp	00121$
   5540                     535 00111$:
                            536 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            537 ;src/entities/enemy.c:88: if (nextx < 2) {
   5540 79            [ 4]  538 	ld	a, c
   5541 D6 02         [ 7]  539 	sub	a, #0x02
   5543 78            [ 4]  540 	ld	a, b
   5544 17            [ 4]  541 	rla
   5545 3F            [ 4]  542 	ccf
   5546 1F            [ 4]  543 	rra
   5547 DE 80         [ 7]  544 	sbc	a, #0x80
   5549 30 0B         [12]  545 	jr	NC,00113$
                            546 ;src/entities/enemy.c:89: nextx = 2;
   554B 01 02 00      [10]  547 	ld	bc, #0x0002
                            548 ;src/entities/enemy.c:90: enemy->vx = 1;
   554E DD 6E FB      [19]  549 	ld	l,-5 (ix)
   5551 DD 66 FC      [19]  550 	ld	h,-4 (ix)
   5554 36 01         [10]  551 	ld	(hl), #0x01
   5556                     552 00113$:
                            553 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   5556 DD 6E FE      [19]  554 	ld	l,-2 (ix)
   5559 DD 66 FF      [19]  555 	ld	h,-1 (ix)
   555C 23            [ 6]  556 	inc	hl
   555D 23            [ 6]  557 	inc	hl
   555E 23            [ 6]  558 	inc	hl
   555F 23            [ 6]  559 	inc	hl
   5560 6E            [ 7]  560 	ld	l, (hl)
   5561 26 00         [ 7]  561 	ld	h, #0x00
   5563 3E 50         [ 7]  562 	ld	a, #0x50
   5565 95            [ 4]  563 	sub	a, l
   5566 6F            [ 4]  564 	ld	l, a
   5567 3E 00         [ 7]  565 	ld	a, #0x00
   5569 9C            [ 4]  566 	sbc	a, h
   556A 67            [ 4]  567 	ld	h, a
                            568 ;src/entities/enemy.c:94: if (nextx > maxx) {
   556B 7D            [ 4]  569 	ld	a, l
   556C 91            [ 4]  570 	sub	a, c
   556D 7C            [ 4]  571 	ld	a, h
   556E 98            [ 4]  572 	sbc	a, b
   556F E2 74 55      [10]  573 	jp	PO, 00163$
   5572 EE 80         [ 7]  574 	xor	a, #0x80
   5574                     575 00163$:
   5574 F2 80 55      [10]  576 	jp	P, 00115$
                            577 ;src/entities/enemy.c:95: nextx = maxx;
   5577 4D            [ 4]  578 	ld	c, l
                            579 ;src/entities/enemy.c:96: enemy->vx = -1;
   5578 DD 6E FB      [19]  580 	ld	l,-5 (ix)
   557B DD 66 FC      [19]  581 	ld	h,-4 (ix)
   557E 36 FF         [10]  582 	ld	(hl), #0xff
   5580                     583 00115$:
                            584 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   5580 DD 6E FE      [19]  585 	ld	l,-2 (ix)
   5583 DD 66 FF      [19]  586 	ld	h,-1 (ix)
   5586 71            [ 7]  587 	ld	(hl), c
                            588 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   5587 1A            [ 7]  589 	ld	a, (de)
   5588 4F            [ 4]  590 	ld	c, a
   5589 0C            [ 4]  591 	inc	c
   558A 79            [ 4]  592 	ld	a, c
   558B 12            [ 7]  593 	ld	(de), a
                            594 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   558C 3E 03         [ 7]  595 	ld	a, #0x03
   558E 91            [ 4]  596 	sub	a, c
   558F E2 94 55      [10]  597 	jp	PO, 00164$
   5592 EE 80         [ 7]  598 	xor	a, #0x80
   5594                     599 00164$:
   5594 F2 9A 55      [10]  600 	jp	P, 00117$
   5597 3E 03         [ 7]  601 	ld	a, #0x03
   5599 12            [ 7]  602 	ld	(de), a
   559A                     603 00117$:
                            604 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   559A DD 6E F9      [19]  605 	ld	l,-7 (ix)
   559D DD 66 FA      [19]  606 	ld	h,-6 (ix)
   55A0 4E            [ 7]  607 	ld	c, (hl)
   55A1 06 00         [ 7]  608 	ld	b, #0x00
   55A3 1A            [ 7]  609 	ld	a, (de)
   55A4 6F            [ 4]  610 	ld	l, a
   55A5 17            [ 4]  611 	rla
   55A6 9F            [ 4]  612 	sbc	a, a
   55A7 67            [ 4]  613 	ld	h, a
   55A8 09            [11]  614 	add	hl, bc
   55A9 E5            [11]  615 	push	hl
   55AA FD E1         [14]  616 	pop	iy
                            617 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   55AC DD 7E FE      [19]  618 	ld	a, -2 (ix)
   55AF C6 05         [ 7]  619 	add	a, #0x05
   55B1 DD 77 F6      [19]  620 	ld	-10 (ix), a
   55B4 DD 7E FF      [19]  621 	ld	a, -1 (ix)
   55B7 CE 00         [ 7]  622 	adc	a, #0x00
   55B9 DD 77 F7      [19]  623 	ld	-9 (ix), a
   55BC E1            [10]  624 	pop	hl
   55BD E5            [11]  625 	push	hl
   55BE 7E            [ 7]  626 	ld	a, (hl)
   55BF DD 6E FE      [19]  627 	ld	l,-2 (ix)
   55C2 DD 66 FF      [19]  628 	ld	h,-1 (ix)
   55C5 4E            [ 7]  629 	ld	c, (hl)
   55C6 06 00         [ 7]  630 	ld	b, #0x00
   55C8 D5            [11]  631 	push	de
   55C9 F5            [11]  632 	push	af
   55CA 33            [ 6]  633 	inc	sp
   55CB FD E5         [15]  634 	push	iy
   55CD C5            [11]  635 	push	bc
   55CE CD 36 4C      [17]  636 	call	_collision_clamp_y_at
   55D1 F1            [10]  637 	pop	af
   55D2 F1            [10]  638 	pop	af
   55D3 33            [ 6]  639 	inc	sp
   55D4 4D            [ 4]  640 	ld	c, l
   55D5 D1            [10]  641 	pop	de
                            642 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   55D6 DD 6E F9      [19]  643 	ld	l,-7 (ix)
   55D9 DD 66 FA      [19]  644 	ld	h,-6 (ix)
   55DC 71            [ 7]  645 	ld	(hl), c
                            646 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   55DD E1            [10]  647 	pop	hl
   55DE E5            [11]  648 	push	hl
   55DF 7E            [ 7]  649 	ld	a, (hl)
   55E0 06 00         [ 7]  650 	ld	b, #0x00
   55E2 DD 6E FE      [19]  651 	ld	l,-2 (ix)
   55E5 DD 66 FF      [19]  652 	ld	h,-1 (ix)
   55E8 6E            [ 7]  653 	ld	l, (hl)
   55E9 DD 75 F6      [19]  654 	ld	-10 (ix), l
   55EC DD 36 F7 00   [19]  655 	ld	-9 (ix), #0x00
   55F0 D5            [11]  656 	push	de
   55F1 F5            [11]  657 	push	af
   55F2 33            [ 6]  658 	inc	sp
   55F3 C5            [11]  659 	push	bc
   55F4 DD 6E F6      [19]  660 	ld	l,-10 (ix)
   55F7 DD 66 F7      [19]  661 	ld	h,-9 (ix)
   55FA E5            [11]  662 	push	hl
   55FB CD B7 4B      [17]  663 	call	_collision_is_on_ground_at
   55FE F1            [10]  664 	pop	af
   55FF F1            [10]  665 	pop	af
   5600 33            [ 6]  666 	inc	sp
   5601 D1            [10]  667 	pop	de
   5602 7D            [ 4]  668 	ld	a, l
   5603 B7            [ 4]  669 	or	a, a
   5604 28 0E         [12]  670 	jr	Z,00121$
   5606 1A            [ 7]  671 	ld	a, (de)
   5607 4F            [ 4]  672 	ld	c, a
   5608 AF            [ 4]  673 	xor	a, a
   5609 91            [ 4]  674 	sub	a, c
   560A E2 0F 56      [10]  675 	jp	PO, 00165$
   560D EE 80         [ 7]  676 	xor	a, #0x80
   560F                     677 00165$:
   560F F2 14 56      [10]  678 	jp	P, 00121$
                            679 ;src/entities/enemy.c:107: enemy->vy = 0;
   5612 AF            [ 4]  680 	xor	a, a
   5613 12            [ 7]  681 	ld	(de), a
   5614                     682 00121$:
   5614 DD F9         [10]  683 	ld	sp, ix
   5616 DD E1         [14]  684 	pop	ix
   5618 C9            [10]  685 	ret
                            686 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            687 ;	---------------------------------
                            688 ; Function enemyrender
                            689 ; ---------------------------------
   5619                     690 _enemyrender::
   5619 DD E5         [15]  691 	push	ix
   561B DD 21 00 00   [14]  692 	ld	ix,#0
   561F DD 39         [15]  693 	add	ix,sp
   5621 F5            [11]  694 	push	af
                            695 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5622 DD 7E 05      [19]  696 	ld	a, 5 (ix)
   5625 DD B6 04      [19]  697 	or	a,4 (ix)
   5628 CA A6 56      [10]  698 	jp	Z,00113$
   562B DD 7E 04      [19]  699 	ld	a, 4 (ix)
   562E DD 77 FE      [19]  700 	ld	-2 (ix), a
   5631 DD 7E 05      [19]  701 	ld	a, 5 (ix)
   5634 DD 77 FF      [19]  702 	ld	-1 (ix), a
   5637 E1            [10]  703 	pop	hl
   5638 E5            [11]  704 	push	hl
   5639 11 06 00      [10]  705 	ld	de, #0x0006
   563C 19            [11]  706 	add	hl, de
   563D 7E            [ 7]  707 	ld	a, (hl)
   563E B7            [ 4]  708 	or	a, a
                            709 ;src/entities/enemy.c:116: return;
   563F 28 65         [12]  710 	jr	Z,00113$
                            711 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   5641 E1            [10]  712 	pop	hl
   5642 E5            [11]  713 	push	hl
   5643 11 09 00      [10]  714 	ld	de, #0x0009
   5646 19            [11]  715 	add	hl, de
   5647 7E            [ 7]  716 	ld	a, (hl)
   5648 FE 03         [ 7]  717 	cp	a, #0x03
   564A 20 0A         [12]  718 	jr	NZ,00111$
   564C 21 0C 0C      [10]  719 	ld	hl, #0x0c0c
   564F E5            [11]  720 	push	hl
   5650 CD 60 5D      [17]  721 	call	_cpct_px2byteM0
   5653 4D            [ 4]  722 	ld	c, l
   5654 18 23         [12]  723 	jr	00112$
   5656                     724 00111$:
                            725 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   5656 FE 02         [ 7]  726 	cp	a, #0x02
   5658 20 0A         [12]  727 	jr	NZ,00108$
   565A 21 0A 0A      [10]  728 	ld	hl, #0x0a0a
   565D E5            [11]  729 	push	hl
   565E CD 60 5D      [17]  730 	call	_cpct_px2byteM0
   5661 4D            [ 4]  731 	ld	c, l
   5662 18 15         [12]  732 	jr	00112$
   5664                     733 00108$:
                            734 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   5664 3D            [ 4]  735 	dec	a
   5665 20 0A         [12]  736 	jr	NZ,00105$
   5667 21 0E 0E      [10]  737 	ld	hl, #0x0e0e
   566A E5            [11]  738 	push	hl
   566B CD 60 5D      [17]  739 	call	_cpct_px2byteM0
   566E 4D            [ 4]  740 	ld	c, l
   566F 18 08         [12]  741 	jr	00112$
   5671                     742 00105$:
                            743 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   5671 21 04 04      [10]  744 	ld	hl, #0x0404
   5674 E5            [11]  745 	push	hl
   5675 CD 60 5D      [17]  746 	call	_cpct_px2byteM0
   5678 4D            [ 4]  747 	ld	c, l
   5679                     748 00112$:
                            749 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5679 E1            [10]  750 	pop	hl
   567A E5            [11]  751 	push	hl
   567B 23            [ 6]  752 	inc	hl
   567C 46            [ 7]  753 	ld	b, (hl)
   567D E1            [10]  754 	pop	hl
   567E E5            [11]  755 	push	hl
   567F 56            [ 7]  756 	ld	d, (hl)
   5680 C5            [11]  757 	push	bc
   5681 4A            [ 4]  758 	ld	c, d
   5682 C5            [11]  759 	push	bc
   5683 21 00 C0      [10]  760 	ld	hl, #0xc000
   5686 E5            [11]  761 	push	hl
   5687 CD 53 5E      [17]  762 	call	_cpct_getScreenPtr
   568A EB            [ 4]  763 	ex	de,hl
   568B C1            [10]  764 	pop	bc
                            765 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   568C E1            [10]  766 	pop	hl
   568D E5            [11]  767 	push	hl
   568E 23            [ 6]  768 	inc	hl
   568F 23            [ 6]  769 	inc	hl
   5690 23            [ 6]  770 	inc	hl
   5691 23            [ 6]  771 	inc	hl
   5692 23            [ 6]  772 	inc	hl
   5693 46            [ 7]  773 	ld	b, (hl)
   5694 E1            [10]  774 	pop	hl
   5695 E5            [11]  775 	push	hl
   5696 23            [ 6]  776 	inc	hl
   5697 23            [ 6]  777 	inc	hl
   5698 23            [ 6]  778 	inc	hl
   5699 23            [ 6]  779 	inc	hl
   569A 7E            [ 7]  780 	ld	a, (hl)
   569B C5            [11]  781 	push	bc
   569C 33            [ 6]  782 	inc	sp
   569D 47            [ 4]  783 	ld	b, a
   569E C5            [11]  784 	push	bc
   569F D5            [11]  785 	push	de
   56A0 CD 9A 5D      [17]  786 	call	_cpct_drawSolidBox
   56A3 F1            [10]  787 	pop	af
   56A4 F1            [10]  788 	pop	af
   56A5 33            [ 6]  789 	inc	sp
   56A6                     790 00113$:
   56A6 DD F9         [10]  791 	ld	sp, ix
   56A8 DD E1         [14]  792 	pop	ix
   56AA C9            [10]  793 	ret
                            794 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            795 ;	---------------------------------
                            796 ; Function enemydamage
                            797 ; ---------------------------------
   56AB                     798 _enemydamage::
   56AB DD E5         [15]  799 	push	ix
   56AD DD 21 00 00   [14]  800 	ld	ix,#0
   56B1 DD 39         [15]  801 	add	ix,sp
                            802 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   56B3 DD 7E 05      [19]  803 	ld	a, 5 (ix)
   56B6 DD B6 04      [19]  804 	or	a,4 (ix)
   56B9 28 0F         [12]  805 	jr	Z,00101$
   56BB DD 4E 04      [19]  806 	ld	c,4 (ix)
   56BE DD 46 05      [19]  807 	ld	b,5 (ix)
   56C1 21 06 00      [10]  808 	ld	hl, #0x0006
   56C4 09            [11]  809 	add	hl,bc
   56C5 EB            [ 4]  810 	ex	de,hl
   56C6 1A            [ 7]  811 	ld	a, (de)
   56C7 B7            [ 4]  812 	or	a, a
   56C8 20 04         [12]  813 	jr	NZ,00102$
   56CA                     814 00101$:
                            815 ;src/entities/enemy.c:130: return 0;
   56CA 2E 00         [ 7]  816 	ld	l, #0x00
   56CC 18 1A         [12]  817 	jr	00106$
   56CE                     818 00102$:
                            819 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   56CE 21 07 00      [10]  820 	ld	hl, #0x0007
   56D1 09            [11]  821 	add	hl, bc
   56D2 4E            [ 7]  822 	ld	c, (hl)
   56D3 DD 7E 06      [19]  823 	ld	a, 6 (ix)
   56D6 91            [ 4]  824 	sub	a, c
   56D7 38 08         [12]  825 	jr	C,00105$
                            826 ;src/entities/enemy.c:134: enemy->health = 0;
   56D9 36 00         [10]  827 	ld	(hl), #0x00
                            828 ;src/entities/enemy.c:135: enemy->active = 0;
   56DB AF            [ 4]  829 	xor	a, a
   56DC 12            [ 7]  830 	ld	(de), a
                            831 ;src/entities/enemy.c:136: return 1;
   56DD 2E 01         [ 7]  832 	ld	l, #0x01
   56DF 18 07         [12]  833 	jr	00106$
   56E1                     834 00105$:
                            835 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   56E1 79            [ 4]  836 	ld	a, c
   56E2 DD 96 06      [19]  837 	sub	a, 6 (ix)
   56E5 77            [ 7]  838 	ld	(hl), a
                            839 ;src/entities/enemy.c:140: return 0;
   56E6 2E 00         [ 7]  840 	ld	l, #0x00
   56E8                     841 00106$:
   56E8 DD E1         [14]  842 	pop	ix
   56EA C9            [10]  843 	ret
                            844 	.area _CODE
                            845 	.area _INITIALIZER
                            846 	.area _CABS (ABS)
