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
   5172                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   5172 21 03 00      [10]   57 	ld	hl, #2+1
   5175 39            [11]   58 	add	hl, sp
   5176 7E            [ 7]   59 	ld	a, (hl)
   5177 2B            [ 6]   60 	dec	hl
   5178 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   5179 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   517A D1            [10]   65 	pop	de
   517B C1            [10]   66 	pop	bc
   517C C5            [11]   67 	push	bc
   517D D5            [11]   68 	push	de
   517E AF            [ 4]   69 	xor	a, a
   517F 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   5180 59            [ 4]   72 	ld	e, c
   5181 50            [ 4]   73 	ld	d, b
   5182 13            [ 6]   74 	inc	de
   5183 AF            [ 4]   75 	xor	a, a
   5184 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   5185 59            [ 4]   78 	ld	e, c
   5186 50            [ 4]   79 	ld	d, b
   5187 13            [ 6]   80 	inc	de
   5188 13            [ 6]   81 	inc	de
   5189 AF            [ 4]   82 	xor	a, a
   518A 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   518B 59            [ 4]   85 	ld	e, c
   518C 50            [ 4]   86 	ld	d, b
   518D 13            [ 6]   87 	inc	de
   518E 13            [ 6]   88 	inc	de
   518F 13            [ 6]   89 	inc	de
   5190 AF            [ 4]   90 	xor	a, a
   5191 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   5192 21 04 00      [10]   93 	ld	hl, #0x0004
   5195 09            [11]   94 	add	hl, bc
   5196 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   5198 21 05 00      [10]   97 	ld	hl, #0x0005
   519B 09            [11]   98 	add	hl, bc
   519C 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   519E 21 06 00      [10]  101 	ld	hl, #0x0006
   51A1 09            [11]  102 	add	hl, bc
   51A2 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   51A4 21 07 00      [10]  105 	ld	hl, #0x0007
   51A7 09            [11]  106 	add	hl, bc
   51A8 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   51AA 21 08 00      [10]  109 	ld	hl, #0x0008
   51AD 09            [11]  110 	add	hl, bc
   51AE 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:19: enemy->kind = 0;
   51B0 21 09 00      [10]  113 	ld	hl, #0x0009
   51B3 09            [11]  114 	add	hl, bc
   51B4 36 00         [10]  115 	ld	(hl), #0x00
   51B6 C9            [10]  116 	ret
                            117 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            118 ;	---------------------------------
                            119 ; Function enemyspawn
                            120 ; ---------------------------------
   51B7                     121 _enemyspawn::
   51B7 DD E5         [15]  122 	push	ix
   51B9 DD 21 00 00   [14]  123 	ld	ix,#0
   51BD DD 39         [15]  124 	add	ix,sp
   51BF 21 F1 FF      [10]  125 	ld	hl, #-15
   51C2 39            [11]  126 	add	hl, sp
   51C3 F9            [ 6]  127 	ld	sp, hl
                            128 ;src/entities/enemy.c:23: if (!enemy) {
   51C4 DD 7E 05      [19]  129 	ld	a, 5 (ix)
   51C7 DD B6 04      [19]  130 	or	a,4 (ix)
                            131 ;src/entities/enemy.c:24: return;
   51CA CA 7A 53      [10]  132 	jp	Z,00112$
                            133 ;src/entities/enemy.c:27: enemy->x = x;
   51CD DD 7E 04      [19]  134 	ld	a, 4 (ix)
   51D0 DD 77 F9      [19]  135 	ld	-7 (ix), a
   51D3 DD 7E 05      [19]  136 	ld	a, 5 (ix)
   51D6 DD 77 FA      [19]  137 	ld	-6 (ix), a
   51D9 DD 6E F9      [19]  138 	ld	l,-7 (ix)
   51DC DD 66 FA      [19]  139 	ld	h,-6 (ix)
   51DF DD 7E 06      [19]  140 	ld	a, 6 (ix)
   51E2 77            [ 7]  141 	ld	(hl), a
                            142 ;src/entities/enemy.c:28: enemy->y = y;
   51E3 DD 4E F9      [19]  143 	ld	c,-7 (ix)
   51E6 DD 46 FA      [19]  144 	ld	b,-6 (ix)
   51E9 03            [ 6]  145 	inc	bc
   51EA DD 7E 07      [19]  146 	ld	a, 7 (ix)
   51ED 02            [ 7]  147 	ld	(bc), a
                            148 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   51EE DD 7E F9      [19]  149 	ld	a, -7 (ix)
   51F1 C6 02         [ 7]  150 	add	a, #0x02
   51F3 DD 77 F7      [19]  151 	ld	-9 (ix), a
   51F6 DD 7E FA      [19]  152 	ld	a, -6 (ix)
   51F9 CE 00         [ 7]  153 	adc	a, #0x00
   51FB DD 77 F8      [19]  154 	ld	-8 (ix), a
   51FE DD 7E 09      [19]  155 	ld	a, 9 (ix)
   5201 B7            [ 4]  156 	or	a, a
   5202 28 04         [12]  157 	jr	Z,00114$
   5204 0E 01         [ 7]  158 	ld	c, #0x01
   5206 18 02         [12]  159 	jr	00115$
   5208                     160 00114$:
   5208 0E FF         [ 7]  161 	ld	c, #0xff
   520A                     162 00115$:
   520A DD 6E F7      [19]  163 	ld	l,-9 (ix)
   520D DD 66 F8      [19]  164 	ld	h,-8 (ix)
   5210 71            [ 7]  165 	ld	(hl), c
                            166 ;src/entities/enemy.c:30: enemy->vy = 0;
   5211 DD 7E F9      [19]  167 	ld	a, -7 (ix)
   5214 C6 03         [ 7]  168 	add	a, #0x03
   5216 DD 77 F5      [19]  169 	ld	-11 (ix), a
   5219 DD 7E FA      [19]  170 	ld	a, -6 (ix)
   521C CE 00         [ 7]  171 	adc	a, #0x00
   521E DD 77 F6      [19]  172 	ld	-10 (ix), a
   5221 DD 6E F5      [19]  173 	ld	l,-11 (ix)
   5224 DD 66 F6      [19]  174 	ld	h,-10 (ix)
   5227 36 00         [10]  175 	ld	(hl), #0x00
                            176 ;src/entities/enemy.c:31: enemy->active = 1;
   5229 DD 7E F9      [19]  177 	ld	a, -7 (ix)
   522C C6 06         [ 7]  178 	add	a, #0x06
   522E DD 77 F3      [19]  179 	ld	-13 (ix), a
   5231 DD 7E FA      [19]  180 	ld	a, -6 (ix)
   5234 CE 00         [ 7]  181 	adc	a, #0x00
   5236 DD 77 F4      [19]  182 	ld	-12 (ix), a
   5239 DD 6E F3      [19]  183 	ld	l,-13 (ix)
   523C DD 66 F4      [19]  184 	ld	h,-12 (ix)
   523F 36 01         [10]  185 	ld	(hl), #0x01
                            186 ;src/entities/enemy.c:32: enemy->kind = kind;
   5241 DD 7E F9      [19]  187 	ld	a, -7 (ix)
   5244 C6 09         [ 7]  188 	add	a, #0x09
   5246 DD 77 F3      [19]  189 	ld	-13 (ix), a
   5249 DD 7E FA      [19]  190 	ld	a, -6 (ix)
   524C CE 00         [ 7]  191 	adc	a, #0x00
   524E DD 77 F4      [19]  192 	ld	-12 (ix), a
   5251 DD 6E F3      [19]  193 	ld	l,-13 (ix)
   5254 DD 66 F4      [19]  194 	ld	h,-12 (ix)
   5257 DD 7E 08      [19]  195 	ld	a, 8 (ix)
   525A 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/enemy.c:35: enemy->w = 5;
   525B DD 7E F9      [19]  198 	ld	a, -7 (ix)
   525E C6 04         [ 7]  199 	add	a, #0x04
   5260 DD 77 F3      [19]  200 	ld	-13 (ix), a
   5263 DD 7E FA      [19]  201 	ld	a, -6 (ix)
   5266 CE 00         [ 7]  202 	adc	a, #0x00
   5268 DD 77 F4      [19]  203 	ld	-12 (ix), a
                            204 ;src/entities/enemy.c:36: enemy->h = 14;
   526B DD 7E F9      [19]  205 	ld	a, -7 (ix)
   526E C6 05         [ 7]  206 	add	a, #0x05
   5270 DD 77 F1      [19]  207 	ld	-15 (ix), a
   5273 DD 7E FA      [19]  208 	ld	a, -6 (ix)
   5276 CE 00         [ 7]  209 	adc	a, #0x00
   5278 DD 77 F2      [19]  210 	ld	-14 (ix), a
                            211 ;src/entities/enemy.c:37: enemy->health = 2;
   527B DD 7E F9      [19]  212 	ld	a, -7 (ix)
   527E C6 07         [ 7]  213 	add	a, #0x07
   5280 DD 77 FE      [19]  214 	ld	-2 (ix), a
   5283 DD 7E FA      [19]  215 	ld	a, -6 (ix)
   5286 CE 00         [ 7]  216 	adc	a, #0x00
   5288 DD 77 FF      [19]  217 	ld	-1 (ix), a
                            218 ;src/entities/enemy.c:38: enemy->reward = 180;
   528B DD 7E F9      [19]  219 	ld	a, -7 (ix)
   528E C6 08         [ 7]  220 	add	a, #0x08
   5290 DD 77 F9      [19]  221 	ld	-7 (ix), a
   5293 DD 7E FA      [19]  222 	ld	a, -6 (ix)
   5296 CE 00         [ 7]  223 	adc	a, #0x00
   5298 DD 77 FA      [19]  224 	ld	-6 (ix), a
                            225 ;src/entities/enemy.c:34: if (kind == 1) {
   529B DD 7E 08      [19]  226 	ld	a, 8 (ix)
   529E 3D            [ 4]  227 	dec	a
   529F 20 45         [12]  228 	jr	NZ,00110$
                            229 ;src/entities/enemy.c:35: enemy->w = 5;
   52A1 DD 6E F3      [19]  230 	ld	l,-13 (ix)
   52A4 DD 66 F4      [19]  231 	ld	h,-12 (ix)
   52A7 36 05         [10]  232 	ld	(hl), #0x05
                            233 ;src/entities/enemy.c:36: enemy->h = 14;
   52A9 E1            [10]  234 	pop	hl
   52AA E5            [11]  235 	push	hl
   52AB 36 0E         [10]  236 	ld	(hl), #0x0e
                            237 ;src/entities/enemy.c:37: enemy->health = 2;
   52AD DD 6E FE      [19]  238 	ld	l,-2 (ix)
   52B0 DD 66 FF      [19]  239 	ld	h,-1 (ix)
   52B3 36 02         [10]  240 	ld	(hl), #0x02
                            241 ;src/entities/enemy.c:38: enemy->reward = 180;
   52B5 DD 6E F9      [19]  242 	ld	l,-7 (ix)
   52B8 DD 66 FA      [19]  243 	ld	h,-6 (ix)
   52BB 36 B4         [10]  244 	ld	(hl), #0xb4
                            245 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   52BD DD 7E F7      [19]  246 	ld	a, -9 (ix)
   52C0 DD 77 FC      [19]  247 	ld	-4 (ix), a
   52C3 DD 7E F8      [19]  248 	ld	a, -8 (ix)
   52C6 DD 77 FD      [19]  249 	ld	-3 (ix), a
   52C9 DD 7E 09      [19]  250 	ld	a, 9 (ix)
   52CC B7            [ 4]  251 	or	a, a
   52CD 28 06         [12]  252 	jr	Z,00116$
   52CF DD 36 FB 02   [19]  253 	ld	-5 (ix), #0x02
   52D3 18 04         [12]  254 	jr	00117$
   52D5                     255 00116$:
   52D5 DD 36 FB FE   [19]  256 	ld	-5 (ix), #0xfe
   52D9                     257 00117$:
   52D9 DD 6E FC      [19]  258 	ld	l,-4 (ix)
   52DC DD 66 FD      [19]  259 	ld	h,-3 (ix)
   52DF DD 7E FB      [19]  260 	ld	a, -5 (ix)
   52E2 77            [ 7]  261 	ld	(hl), a
   52E3 C3 7A 53      [10]  262 	jp	00112$
   52E6                     263 00110$:
                            264 ;src/entities/enemy.c:40: } else if (kind == 2) {
   52E6 DD 7E 08      [19]  265 	ld	a, 8 (ix)
   52E9 D6 02         [ 7]  266 	sub	a, #0x02
   52EB 20 39         [12]  267 	jr	NZ,00107$
                            268 ;src/entities/enemy.c:41: enemy->w = 6;
   52ED DD 6E F3      [19]  269 	ld	l,-13 (ix)
   52F0 DD 66 F4      [19]  270 	ld	h,-12 (ix)
   52F3 36 06         [10]  271 	ld	(hl), #0x06
                            272 ;src/entities/enemy.c:42: enemy->h = 10;
   52F5 E1            [10]  273 	pop	hl
   52F6 E5            [11]  274 	push	hl
   52F7 36 0A         [10]  275 	ld	(hl), #0x0a
                            276 ;src/entities/enemy.c:43: enemy->health = 1;
   52F9 DD 6E FE      [19]  277 	ld	l,-2 (ix)
   52FC DD 66 FF      [19]  278 	ld	h,-1 (ix)
   52FF 36 01         [10]  279 	ld	(hl), #0x01
                            280 ;src/entities/enemy.c:44: enemy->reward = 150;
   5301 DD 6E F9      [19]  281 	ld	l,-7 (ix)
   5304 DD 66 FA      [19]  282 	ld	h,-6 (ix)
   5307 36 96         [10]  283 	ld	(hl), #0x96
                            284 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5309 DD 4E F5      [19]  285 	ld	c,-11 (ix)
   530C DD 46 F6      [19]  286 	ld	b,-10 (ix)
   530F DD 7E 09      [19]  287 	ld	a, 9 (ix)
   5312 B7            [ 4]  288 	or	a, a
   5313 28 04         [12]  289 	jr	Z,00118$
   5315 3E 01         [ 7]  290 	ld	a, #0x01
   5317 18 02         [12]  291 	jr	00119$
   5319                     292 00118$:
   5319 3E FF         [ 7]  293 	ld	a, #0xff
   531B                     294 00119$:
   531B 02            [ 7]  295 	ld	(bc), a
                            296 ;src/entities/enemy.c:46: enemy->vx = 1;
   531C DD 6E F7      [19]  297 	ld	l,-9 (ix)
   531F DD 66 F8      [19]  298 	ld	h,-8 (ix)
   5322 36 01         [10]  299 	ld	(hl), #0x01
   5324 18 54         [12]  300 	jr	00112$
   5326                     301 00107$:
                            302 ;src/entities/enemy.c:47: } else if (kind == 3) {
   5326 DD 7E 08      [19]  303 	ld	a, 8 (ix)
   5329 D6 03         [ 7]  304 	sub	a, #0x03
   532B 20 31         [12]  305 	jr	NZ,00104$
                            306 ;src/entities/enemy.c:48: enemy->w = 10;
   532D DD 6E F3      [19]  307 	ld	l,-13 (ix)
   5330 DD 66 F4      [19]  308 	ld	h,-12 (ix)
   5333 36 0A         [10]  309 	ld	(hl), #0x0a
                            310 ;src/entities/enemy.c:49: enemy->h = 18;
   5335 E1            [10]  311 	pop	hl
   5336 E5            [11]  312 	push	hl
   5337 36 12         [10]  313 	ld	(hl), #0x12
                            314 ;src/entities/enemy.c:50: enemy->health = 8;
   5339 DD 6E FE      [19]  315 	ld	l,-2 (ix)
   533C DD 66 FF      [19]  316 	ld	h,-1 (ix)
   533F 36 08         [10]  317 	ld	(hl), #0x08
                            318 ;src/entities/enemy.c:51: enemy->reward = 800;
   5341 DD 6E F9      [19]  319 	ld	l,-7 (ix)
   5344 DD 66 FA      [19]  320 	ld	h,-6 (ix)
   5347 36 20         [10]  321 	ld	(hl), #0x20
                            322 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   5349 DD 4E F7      [19]  323 	ld	c,-9 (ix)
   534C DD 46 F8      [19]  324 	ld	b,-8 (ix)
   534F DD 7E 09      [19]  325 	ld	a, 9 (ix)
   5352 B7            [ 4]  326 	or	a, a
   5353 28 04         [12]  327 	jr	Z,00120$
   5355 3E 01         [ 7]  328 	ld	a, #0x01
   5357 18 02         [12]  329 	jr	00121$
   5359                     330 00120$:
   5359 3E FF         [ 7]  331 	ld	a, #0xff
   535B                     332 00121$:
   535B 02            [ 7]  333 	ld	(bc), a
   535C 18 1C         [12]  334 	jr	00112$
   535E                     335 00104$:
                            336 ;src/entities/enemy.c:54: enemy->w = 4;
   535E DD 6E F3      [19]  337 	ld	l,-13 (ix)
   5361 DD 66 F4      [19]  338 	ld	h,-12 (ix)
   5364 36 04         [10]  339 	ld	(hl), #0x04
                            340 ;src/entities/enemy.c:55: enemy->h = 16;
   5366 E1            [10]  341 	pop	hl
   5367 E5            [11]  342 	push	hl
   5368 36 10         [10]  343 	ld	(hl), #0x10
                            344 ;src/entities/enemy.c:56: enemy->health = 1;
   536A DD 6E FE      [19]  345 	ld	l,-2 (ix)
   536D DD 66 FF      [19]  346 	ld	h,-1 (ix)
   5370 36 01         [10]  347 	ld	(hl), #0x01
                            348 ;src/entities/enemy.c:57: enemy->reward = 100;
   5372 DD 6E F9      [19]  349 	ld	l,-7 (ix)
   5375 DD 66 FA      [19]  350 	ld	h,-6 (ix)
   5378 36 64         [10]  351 	ld	(hl), #0x64
   537A                     352 00112$:
   537A DD F9         [10]  353 	ld	sp, ix
   537C DD E1         [14]  354 	pop	ix
   537E C9            [10]  355 	ret
                            356 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            357 ;	---------------------------------
                            358 ; Function enemyupdate
                            359 ; ---------------------------------
   537F                     360 _enemyupdate::
   537F DD E5         [15]  361 	push	ix
   5381 DD 21 00 00   [14]  362 	ld	ix,#0
   5385 DD 39         [15]  363 	add	ix,sp
   5387 21 F6 FF      [10]  364 	ld	hl, #-10
   538A 39            [11]  365 	add	hl, sp
   538B F9            [ 6]  366 	ld	sp, hl
                            367 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   538C DD 7E 05      [19]  368 	ld	a, 5 (ix)
   538F DD B6 04      [19]  369 	or	a,4 (ix)
   5392 CA 86 55      [10]  370 	jp	Z,00121$
   5395 DD 7E 04      [19]  371 	ld	a, 4 (ix)
   5398 DD 77 FE      [19]  372 	ld	-2 (ix), a
   539B DD 7E 05      [19]  373 	ld	a, 5 (ix)
   539E DD 77 FF      [19]  374 	ld	-1 (ix), a
   53A1 DD 6E FE      [19]  375 	ld	l,-2 (ix)
   53A4 DD 66 FF      [19]  376 	ld	h,-1 (ix)
   53A7 11 06 00      [10]  377 	ld	de, #0x0006
   53AA 19            [11]  378 	add	hl, de
   53AB 7E            [ 7]  379 	ld	a, (hl)
   53AC B7            [ 4]  380 	or	a, a
                            381 ;src/entities/enemy.c:66: return;
   53AD CA 86 55      [10]  382 	jp	Z,00121$
                            383 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   53B0 DD 6E FE      [19]  384 	ld	l,-2 (ix)
   53B3 DD 66 FF      [19]  385 	ld	h,-1 (ix)
   53B6 11 09 00      [10]  386 	ld	de, #0x0009
   53B9 19            [11]  387 	add	hl, de
   53BA 7E            [ 7]  388 	ld	a, (hl)
   53BB DD 77 FD      [19]  389 	ld	-3 (ix), a
                            390 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   53BE DD 6E FE      [19]  391 	ld	l,-2 (ix)
   53C1 DD 66 FF      [19]  392 	ld	h,-1 (ix)
   53C4 4E            [ 7]  393 	ld	c, (hl)
   53C5 DD 7E FE      [19]  394 	ld	a, -2 (ix)
   53C8 C6 02         [ 7]  395 	add	a, #0x02
   53CA DD 77 FB      [19]  396 	ld	-5 (ix), a
   53CD DD 7E FF      [19]  397 	ld	a, -1 (ix)
   53D0 CE 00         [ 7]  398 	adc	a, #0x00
   53D2 DD 77 FC      [19]  399 	ld	-4 (ix), a
                            400 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   53D5 DD 7E FE      [19]  401 	ld	a, -2 (ix)
   53D8 C6 01         [ 7]  402 	add	a, #0x01
   53DA DD 77 F9      [19]  403 	ld	-7 (ix), a
   53DD DD 7E FF      [19]  404 	ld	a, -1 (ix)
   53E0 CE 00         [ 7]  405 	adc	a, #0x00
   53E2 DD 77 FA      [19]  406 	ld	-6 (ix), a
   53E5 DD 5E FE      [19]  407 	ld	e,-2 (ix)
   53E8 DD 56 FF      [19]  408 	ld	d,-1 (ix)
   53EB 13            [ 6]  409 	inc	de
   53EC 13            [ 6]  410 	inc	de
   53ED 13            [ 6]  411 	inc	de
                            412 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   53EE 06 00         [ 7]  413 	ld	b, #0x00
   53F0 DD 6E FB      [19]  414 	ld	l,-5 (ix)
   53F3 DD 66 FC      [19]  415 	ld	h,-4 (ix)
   53F6 7E            [ 7]  416 	ld	a, (hl)
   53F7 DD 77 F8      [19]  417 	ld	-8 (ix), a
   53FA 6F            [ 4]  418 	ld	l, a
   53FB DD 7E F8      [19]  419 	ld	a, -8 (ix)
   53FE 17            [ 4]  420 	rla
   53FF 9F            [ 4]  421 	sbc	a, a
   5400 67            [ 4]  422 	ld	h, a
   5401 09            [11]  423 	add	hl,bc
   5402 4D            [ 4]  424 	ld	c, l
   5403 44            [ 4]  425 	ld	b, h
                            426 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5404 DD 7E FD      [19]  427 	ld	a, -3 (ix)
   5407 D6 02         [ 7]  428 	sub	a, #0x02
   5409 C2 B2 54      [10]  429 	jp	NZ,00111$
                            430 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            431 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   540C DD 6E F9      [19]  432 	ld	l,-7 (ix)
   540F DD 66 FA      [19]  433 	ld	h,-6 (ix)
   5412 6E            [ 7]  434 	ld	l, (hl)
   5413 DD 75 F6      [19]  435 	ld	-10 (ix), l
   5416 DD 36 F7 00   [19]  436 	ld	-9 (ix), #0x00
   541A 1A            [ 7]  437 	ld	a, (de)
   541B 6F            [ 4]  438 	ld	l, a
   541C 17            [ 4]  439 	rla
   541D 9F            [ 4]  440 	sbc	a, a
   541E 67            [ 4]  441 	ld	h, a
   541F DD 7E F6      [19]  442 	ld	a, -10 (ix)
   5422 85            [ 4]  443 	add	a, l
   5423 DD 77 F6      [19]  444 	ld	-10 (ix), a
   5426 DD 7E F7      [19]  445 	ld	a, -9 (ix)
   5429 8C            [ 4]  446 	adc	a, h
   542A DD 77 F7      [19]  447 	ld	-9 (ix), a
                            448 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   542D 79            [ 4]  449 	ld	a, c
   542E D6 08         [ 7]  450 	sub	a, #0x08
   5430 78            [ 4]  451 	ld	a, b
   5431 17            [ 4]  452 	rla
   5432 3F            [ 4]  453 	ccf
   5433 1F            [ 4]  454 	rra
   5434 DE 80         [ 7]  455 	sbc	a, #0x80
   5436 38 0E         [12]  456 	jr	C,00104$
   5438 3E 48         [ 7]  457 	ld	a, #0x48
   543A B9            [ 4]  458 	cp	a, c
   543B 3E 00         [ 7]  459 	ld	a, #0x00
   543D 98            [ 4]  460 	sbc	a, b
   543E E2 43 54      [10]  461 	jp	PO, 00161$
   5441 EE 80         [ 7]  462 	xor	a, #0x80
   5443                     463 00161$:
   5443 F2 61 54      [10]  464 	jp	P, 00105$
   5446                     465 00104$:
                            466 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   5446 AF            [ 4]  467 	xor	a, a
   5447 DD 96 F8      [19]  468 	sub	a, -8 (ix)
   544A 4F            [ 4]  469 	ld	c, a
   544B DD 6E FB      [19]  470 	ld	l,-5 (ix)
   544E DD 66 FC      [19]  471 	ld	h,-4 (ix)
   5451 71            [ 7]  472 	ld	(hl), c
                            473 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   5452 DD 6E FE      [19]  474 	ld	l,-2 (ix)
   5455 DD 66 FF      [19]  475 	ld	h,-1 (ix)
   5458 6E            [ 7]  476 	ld	l, (hl)
   5459 26 00         [ 7]  477 	ld	h, #0x00
   545B 79            [ 4]  478 	ld	a, c
   545C 17            [ 4]  479 	rla
   545D 9F            [ 4]  480 	sbc	a, a
   545E 47            [ 4]  481 	ld	b, a
   545F 09            [11]  482 	add	hl,bc
   5460 4D            [ 4]  483 	ld	c, l
   5461                     484 00105$:
                            485 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   5461 DD 7E F6      [19]  486 	ld	a, -10 (ix)
   5464 D6 38         [ 7]  487 	sub	a, #0x38
   5466 DD 7E F7      [19]  488 	ld	a, -9 (ix)
   5469 17            [ 4]  489 	rla
   546A 3F            [ 4]  490 	ccf
   546B 1F            [ 4]  491 	rra
   546C DE 80         [ 7]  492 	sbc	a, #0x80
   546E 38 12         [12]  493 	jr	C,00107$
   5470 3E 78         [ 7]  494 	ld	a, #0x78
   5472 DD BE F6      [19]  495 	cp	a, -10 (ix)
   5475 3E 00         [ 7]  496 	ld	a, #0x00
   5477 DD 9E F7      [19]  497 	sbc	a, -9 (ix)
   547A E2 7F 54      [10]  498 	jp	PO, 00162$
   547D EE 80         [ 7]  499 	xor	a, #0x80
   547F                     500 00162$:
   547F F2 9E 54      [10]  501 	jp	P, 00108$
   5482                     502 00107$:
                            503 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5482 1A            [ 7]  504 	ld	a, (de)
   5483 6F            [ 4]  505 	ld	l, a
   5484 AF            [ 4]  506 	xor	a, a
   5485 95            [ 4]  507 	sub	a, l
   5486 DD 77 F8      [19]  508 	ld	-8 (ix), a
   5489 12            [ 7]  509 	ld	(de),a
                            510 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   548A DD 6E F9      [19]  511 	ld	l,-7 (ix)
   548D DD 66 FA      [19]  512 	ld	h,-6 (ix)
   5490 5E            [ 7]  513 	ld	e, (hl)
   5491 16 00         [ 7]  514 	ld	d, #0x00
   5493 DD 6E F8      [19]  515 	ld	l, -8 (ix)
   5496 DD 7E F8      [19]  516 	ld	a, -8 (ix)
   5499 17            [ 4]  517 	rla
   549A 9F            [ 4]  518 	sbc	a, a
   549B 67            [ 4]  519 	ld	h, a
   549C 19            [11]  520 	add	hl,de
   549D E3            [19]  521 	ex	(sp), hl
   549E                     522 00108$:
                            523 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   549E DD 6E FE      [19]  524 	ld	l,-2 (ix)
   54A1 DD 66 FF      [19]  525 	ld	h,-1 (ix)
   54A4 71            [ 7]  526 	ld	(hl), c
                            527 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   54A5 DD 4E F6      [19]  528 	ld	c, -10 (ix)
   54A8 DD 6E F9      [19]  529 	ld	l,-7 (ix)
   54AB DD 66 FA      [19]  530 	ld	h,-6 (ix)
   54AE 71            [ 7]  531 	ld	(hl), c
                            532 ;src/entities/enemy.c:84: return;
   54AF C3 86 55      [10]  533 	jp	00121$
   54B2                     534 00111$:
                            535 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            536 ;src/entities/enemy.c:88: if (nextx < 2) {
   54B2 79            [ 4]  537 	ld	a, c
   54B3 D6 02         [ 7]  538 	sub	a, #0x02
   54B5 78            [ 4]  539 	ld	a, b
   54B6 17            [ 4]  540 	rla
   54B7 3F            [ 4]  541 	ccf
   54B8 1F            [ 4]  542 	rra
   54B9 DE 80         [ 7]  543 	sbc	a, #0x80
   54BB 30 0B         [12]  544 	jr	NC,00113$
                            545 ;src/entities/enemy.c:89: nextx = 2;
   54BD 01 02 00      [10]  546 	ld	bc, #0x0002
                            547 ;src/entities/enemy.c:90: enemy->vx = 1;
   54C0 DD 6E FB      [19]  548 	ld	l,-5 (ix)
   54C3 DD 66 FC      [19]  549 	ld	h,-4 (ix)
   54C6 36 01         [10]  550 	ld	(hl), #0x01
   54C8                     551 00113$:
                            552 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   54C8 DD 6E FE      [19]  553 	ld	l,-2 (ix)
   54CB DD 66 FF      [19]  554 	ld	h,-1 (ix)
   54CE 23            [ 6]  555 	inc	hl
   54CF 23            [ 6]  556 	inc	hl
   54D0 23            [ 6]  557 	inc	hl
   54D1 23            [ 6]  558 	inc	hl
   54D2 6E            [ 7]  559 	ld	l, (hl)
   54D3 26 00         [ 7]  560 	ld	h, #0x00
   54D5 3E 50         [ 7]  561 	ld	a, #0x50
   54D7 95            [ 4]  562 	sub	a, l
   54D8 6F            [ 4]  563 	ld	l, a
   54D9 3E 00         [ 7]  564 	ld	a, #0x00
   54DB 9C            [ 4]  565 	sbc	a, h
   54DC 67            [ 4]  566 	ld	h, a
                            567 ;src/entities/enemy.c:94: if (nextx > maxx) {
   54DD 7D            [ 4]  568 	ld	a, l
   54DE 91            [ 4]  569 	sub	a, c
   54DF 7C            [ 4]  570 	ld	a, h
   54E0 98            [ 4]  571 	sbc	a, b
   54E1 E2 E6 54      [10]  572 	jp	PO, 00163$
   54E4 EE 80         [ 7]  573 	xor	a, #0x80
   54E6                     574 00163$:
   54E6 F2 F2 54      [10]  575 	jp	P, 00115$
                            576 ;src/entities/enemy.c:95: nextx = maxx;
   54E9 4D            [ 4]  577 	ld	c, l
                            578 ;src/entities/enemy.c:96: enemy->vx = -1;
   54EA DD 6E FB      [19]  579 	ld	l,-5 (ix)
   54ED DD 66 FC      [19]  580 	ld	h,-4 (ix)
   54F0 36 FF         [10]  581 	ld	(hl), #0xff
   54F2                     582 00115$:
                            583 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   54F2 DD 6E FE      [19]  584 	ld	l,-2 (ix)
   54F5 DD 66 FF      [19]  585 	ld	h,-1 (ix)
   54F8 71            [ 7]  586 	ld	(hl), c
                            587 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   54F9 1A            [ 7]  588 	ld	a, (de)
   54FA 4F            [ 4]  589 	ld	c, a
   54FB 0C            [ 4]  590 	inc	c
   54FC 79            [ 4]  591 	ld	a, c
   54FD 12            [ 7]  592 	ld	(de), a
                            593 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   54FE 3E 03         [ 7]  594 	ld	a, #0x03
   5500 91            [ 4]  595 	sub	a, c
   5501 E2 06 55      [10]  596 	jp	PO, 00164$
   5504 EE 80         [ 7]  597 	xor	a, #0x80
   5506                     598 00164$:
   5506 F2 0C 55      [10]  599 	jp	P, 00117$
   5509 3E 03         [ 7]  600 	ld	a, #0x03
   550B 12            [ 7]  601 	ld	(de), a
   550C                     602 00117$:
                            603 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   550C DD 6E F9      [19]  604 	ld	l,-7 (ix)
   550F DD 66 FA      [19]  605 	ld	h,-6 (ix)
   5512 4E            [ 7]  606 	ld	c, (hl)
   5513 06 00         [ 7]  607 	ld	b, #0x00
   5515 1A            [ 7]  608 	ld	a, (de)
   5516 6F            [ 4]  609 	ld	l, a
   5517 17            [ 4]  610 	rla
   5518 9F            [ 4]  611 	sbc	a, a
   5519 67            [ 4]  612 	ld	h, a
   551A 09            [11]  613 	add	hl, bc
   551B E5            [11]  614 	push	hl
   551C FD E1         [14]  615 	pop	iy
                            616 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   551E DD 7E FE      [19]  617 	ld	a, -2 (ix)
   5521 C6 05         [ 7]  618 	add	a, #0x05
   5523 DD 77 F6      [19]  619 	ld	-10 (ix), a
   5526 DD 7E FF      [19]  620 	ld	a, -1 (ix)
   5529 CE 00         [ 7]  621 	adc	a, #0x00
   552B DD 77 F7      [19]  622 	ld	-9 (ix), a
   552E E1            [10]  623 	pop	hl
   552F E5            [11]  624 	push	hl
   5530 7E            [ 7]  625 	ld	a, (hl)
   5531 DD 6E FE      [19]  626 	ld	l,-2 (ix)
   5534 DD 66 FF      [19]  627 	ld	h,-1 (ix)
   5537 4E            [ 7]  628 	ld	c, (hl)
   5538 06 00         [ 7]  629 	ld	b, #0x00
   553A D5            [11]  630 	push	de
   553B F5            [11]  631 	push	af
   553C 33            [ 6]  632 	inc	sp
   553D FD E5         [15]  633 	push	iy
   553F C5            [11]  634 	push	bc
   5540 CD D6 4B      [17]  635 	call	_collision_clamp_y_at
   5543 F1            [10]  636 	pop	af
   5544 F1            [10]  637 	pop	af
   5545 33            [ 6]  638 	inc	sp
   5546 4D            [ 4]  639 	ld	c, l
   5547 D1            [10]  640 	pop	de
                            641 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   5548 DD 6E F9      [19]  642 	ld	l,-7 (ix)
   554B DD 66 FA      [19]  643 	ld	h,-6 (ix)
   554E 71            [ 7]  644 	ld	(hl), c
                            645 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   554F E1            [10]  646 	pop	hl
   5550 E5            [11]  647 	push	hl
   5551 7E            [ 7]  648 	ld	a, (hl)
   5552 06 00         [ 7]  649 	ld	b, #0x00
   5554 DD 6E FE      [19]  650 	ld	l,-2 (ix)
   5557 DD 66 FF      [19]  651 	ld	h,-1 (ix)
   555A 6E            [ 7]  652 	ld	l, (hl)
   555B DD 75 F6      [19]  653 	ld	-10 (ix), l
   555E DD 36 F7 00   [19]  654 	ld	-9 (ix), #0x00
   5562 D5            [11]  655 	push	de
   5563 F5            [11]  656 	push	af
   5564 33            [ 6]  657 	inc	sp
   5565 C5            [11]  658 	push	bc
   5566 DD 6E F6      [19]  659 	ld	l,-10 (ix)
   5569 DD 66 F7      [19]  660 	ld	h,-9 (ix)
   556C E5            [11]  661 	push	hl
   556D CD 57 4B      [17]  662 	call	_collision_is_on_ground_at
   5570 F1            [10]  663 	pop	af
   5571 F1            [10]  664 	pop	af
   5572 33            [ 6]  665 	inc	sp
   5573 D1            [10]  666 	pop	de
   5574 7D            [ 4]  667 	ld	a, l
   5575 B7            [ 4]  668 	or	a, a
   5576 28 0E         [12]  669 	jr	Z,00121$
   5578 1A            [ 7]  670 	ld	a, (de)
   5579 4F            [ 4]  671 	ld	c, a
   557A AF            [ 4]  672 	xor	a, a
   557B 91            [ 4]  673 	sub	a, c
   557C E2 81 55      [10]  674 	jp	PO, 00165$
   557F EE 80         [ 7]  675 	xor	a, #0x80
   5581                     676 00165$:
   5581 F2 86 55      [10]  677 	jp	P, 00121$
                            678 ;src/entities/enemy.c:107: enemy->vy = 0;
   5584 AF            [ 4]  679 	xor	a, a
   5585 12            [ 7]  680 	ld	(de), a
   5586                     681 00121$:
   5586 DD F9         [10]  682 	ld	sp, ix
   5588 DD E1         [14]  683 	pop	ix
   558A C9            [10]  684 	ret
                            685 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            686 ;	---------------------------------
                            687 ; Function enemyrender
                            688 ; ---------------------------------
   558B                     689 _enemyrender::
   558B DD E5         [15]  690 	push	ix
   558D DD 21 00 00   [14]  691 	ld	ix,#0
   5591 DD 39         [15]  692 	add	ix,sp
   5593 3B            [ 6]  693 	dec	sp
                            694 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   5594 DD 7E 05      [19]  695 	ld	a, 5 (ix)
   5597 DD B6 04      [19]  696 	or	a,4 (ix)
   559A 28 65         [12]  697 	jr	Z,00113$
   559C DD 4E 04      [19]  698 	ld	c,4 (ix)
   559F DD 46 05      [19]  699 	ld	b,5 (ix)
   55A2 C5            [11]  700 	push	bc
   55A3 FD E1         [14]  701 	pop	iy
   55A5 FD 7E 06      [19]  702 	ld	a, 6 (iy)
   55A8 B7            [ 4]  703 	or	a, a
                            704 ;src/entities/enemy.c:116: return;
   55A9 28 56         [12]  705 	jr	Z,00113$
                            706 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = 0x4C;
   55AB C5            [11]  707 	push	bc
   55AC FD E1         [14]  708 	pop	iy
   55AE FD 7E 09      [19]  709 	ld	a, 9 (iy)
   55B1 FE 03         [ 7]  710 	cp	a, #0x03
   55B3 20 04         [12]  711 	jr	NZ,00111$
   55B5 1E 4C         [ 7]  712 	ld	e, #0x4c
   55B7 18 11         [12]  713 	jr	00112$
   55B9                     714 00111$:
                            715 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = 0x5A;
   55B9 FE 02         [ 7]  716 	cp	a, #0x02
   55BB 20 04         [12]  717 	jr	NZ,00108$
   55BD 1E 5A         [ 7]  718 	ld	e, #0x5a
   55BF 18 09         [12]  719 	jr	00112$
   55C1                     720 00108$:
                            721 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = 0x4E;
   55C1 3D            [ 4]  722 	dec	a
   55C2 20 04         [12]  723 	jr	NZ,00105$
   55C4 1E 4E         [ 7]  724 	ld	e, #0x4e
   55C6 18 02         [12]  725 	jr	00112$
   55C8                     726 00105$:
                            727 ;src/entities/enemy.c:122: else colour = 0x5C;
   55C8 1E 5C         [ 7]  728 	ld	e, #0x5c
   55CA                     729 00112$:
                            730 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   55CA 69            [ 4]  731 	ld	l, c
   55CB 60            [ 4]  732 	ld	h, b
   55CC 23            [ 6]  733 	inc	hl
   55CD 56            [ 7]  734 	ld	d, (hl)
   55CE 0A            [ 7]  735 	ld	a, (bc)
   55CF C5            [11]  736 	push	bc
   55D0 D5            [11]  737 	push	de
   55D1 5F            [ 4]  738 	ld	e, a
   55D2 D5            [11]  739 	push	de
   55D3 21 00 C0      [10]  740 	ld	hl, #0xc000
   55D6 E5            [11]  741 	push	hl
   55D7 CD 98 5E      [17]  742 	call	_cpct_getScreenPtr
   55DA D1            [10]  743 	pop	de
   55DB C1            [10]  744 	pop	bc
   55DC E5            [11]  745 	push	hl
   55DD FD E1         [14]  746 	pop	iy
                            747 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   55DF 69            [ 4]  748 	ld	l, c
   55E0 60            [ 4]  749 	ld	h, b
   55E1 23            [ 6]  750 	inc	hl
   55E2 23            [ 6]  751 	inc	hl
   55E3 23            [ 6]  752 	inc	hl
   55E4 23            [ 6]  753 	inc	hl
   55E5 23            [ 6]  754 	inc	hl
   55E6 7E            [ 7]  755 	ld	a, (hl)
   55E7 DD 77 FF      [19]  756 	ld	-1 (ix), a
   55EA 69            [ 4]  757 	ld	l, c
   55EB 60            [ 4]  758 	ld	h, b
   55EC 01 04 00      [10]  759 	ld	bc, #0x0004
   55EF 09            [11]  760 	add	hl, bc
   55F0 56            [ 7]  761 	ld	d, (hl)
   55F1 FD E5         [15]  762 	push	iy
   55F3 C1            [10]  763 	pop	bc
   55F4 DD 7E FF      [19]  764 	ld	a, -1 (ix)
   55F7 F5            [11]  765 	push	af
   55F8 33            [ 6]  766 	inc	sp
   55F9 D5            [11]  767 	push	de
   55FA C5            [11]  768 	push	bc
   55FB CD DF 5D      [17]  769 	call	_cpct_drawSolidBox
   55FE F1            [10]  770 	pop	af
   55FF F1            [10]  771 	pop	af
   5600 33            [ 6]  772 	inc	sp
   5601                     773 00113$:
   5601 33            [ 6]  774 	inc	sp
   5602 DD E1         [14]  775 	pop	ix
   5604 C9            [10]  776 	ret
                            777 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            778 ;	---------------------------------
                            779 ; Function enemydamage
                            780 ; ---------------------------------
   5605                     781 _enemydamage::
   5605 DD E5         [15]  782 	push	ix
   5607 DD 21 00 00   [14]  783 	ld	ix,#0
   560B DD 39         [15]  784 	add	ix,sp
                            785 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   560D DD 7E 05      [19]  786 	ld	a, 5 (ix)
   5610 DD B6 04      [19]  787 	or	a,4 (ix)
   5613 28 0F         [12]  788 	jr	Z,00101$
   5615 DD 4E 04      [19]  789 	ld	c,4 (ix)
   5618 DD 46 05      [19]  790 	ld	b,5 (ix)
   561B 21 06 00      [10]  791 	ld	hl, #0x0006
   561E 09            [11]  792 	add	hl,bc
   561F EB            [ 4]  793 	ex	de,hl
   5620 1A            [ 7]  794 	ld	a, (de)
   5621 B7            [ 4]  795 	or	a, a
   5622 20 04         [12]  796 	jr	NZ,00102$
   5624                     797 00101$:
                            798 ;src/entities/enemy.c:130: return 0;
   5624 2E 00         [ 7]  799 	ld	l, #0x00
   5626 18 1A         [12]  800 	jr	00106$
   5628                     801 00102$:
                            802 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   5628 21 07 00      [10]  803 	ld	hl, #0x0007
   562B 09            [11]  804 	add	hl, bc
   562C 4E            [ 7]  805 	ld	c, (hl)
   562D DD 7E 06      [19]  806 	ld	a, 6 (ix)
   5630 91            [ 4]  807 	sub	a, c
   5631 38 08         [12]  808 	jr	C,00105$
                            809 ;src/entities/enemy.c:134: enemy->health = 0;
   5633 36 00         [10]  810 	ld	(hl), #0x00
                            811 ;src/entities/enemy.c:135: enemy->active = 0;
   5635 AF            [ 4]  812 	xor	a, a
   5636 12            [ 7]  813 	ld	(de), a
                            814 ;src/entities/enemy.c:136: return 1;
   5637 2E 01         [ 7]  815 	ld	l, #0x01
   5639 18 07         [12]  816 	jr	00106$
   563B                     817 00105$:
                            818 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   563B 79            [ 4]  819 	ld	a, c
   563C DD 96 06      [19]  820 	sub	a, 6 (ix)
   563F 77            [ 7]  821 	ld	(hl), a
                            822 ;src/entities/enemy.c:140: return 0;
   5640 2E 00         [ 7]  823 	ld	l, #0x00
   5642                     824 00106$:
   5642 DD E1         [14]  825 	pop	ix
   5644 C9            [10]  826 	ret
                            827 	.area _CODE
                            828 	.area _INITIALIZER
                            829 	.area _CABS (ABS)
