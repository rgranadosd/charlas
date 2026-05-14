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
   518D                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   518D 21 03 00      [10]   57 	ld	hl, #2+1
   5190 39            [11]   58 	add	hl, sp
   5191 7E            [ 7]   59 	ld	a, (hl)
   5192 2B            [ 6]   60 	dec	hl
   5193 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   5194 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   5195 D1            [10]   65 	pop	de
   5196 C1            [10]   66 	pop	bc
   5197 C5            [11]   67 	push	bc
   5198 D5            [11]   68 	push	de
   5199 AF            [ 4]   69 	xor	a, a
   519A 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   519B 59            [ 4]   72 	ld	e, c
   519C 50            [ 4]   73 	ld	d, b
   519D 13            [ 6]   74 	inc	de
   519E AF            [ 4]   75 	xor	a, a
   519F 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   51A0 59            [ 4]   78 	ld	e, c
   51A1 50            [ 4]   79 	ld	d, b
   51A2 13            [ 6]   80 	inc	de
   51A3 13            [ 6]   81 	inc	de
   51A4 AF            [ 4]   82 	xor	a, a
   51A5 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   51A6 59            [ 4]   85 	ld	e, c
   51A7 50            [ 4]   86 	ld	d, b
   51A8 13            [ 6]   87 	inc	de
   51A9 13            [ 6]   88 	inc	de
   51AA 13            [ 6]   89 	inc	de
   51AB AF            [ 4]   90 	xor	a, a
   51AC 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   51AD 21 04 00      [10]   93 	ld	hl, #0x0004
   51B0 09            [11]   94 	add	hl, bc
   51B1 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   51B3 21 05 00      [10]   97 	ld	hl, #0x0005
   51B6 09            [11]   98 	add	hl, bc
   51B7 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   51B9 21 06 00      [10]  101 	ld	hl, #0x0006
   51BC 09            [11]  102 	add	hl, bc
   51BD 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   51BF 21 07 00      [10]  105 	ld	hl, #0x0007
   51C2 09            [11]  106 	add	hl, bc
   51C3 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   51C5 21 08 00      [10]  109 	ld	hl, #0x0008
   51C8 09            [11]  110 	add	hl, bc
   51C9 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:19: enemy->kind = 0;
   51CB 21 09 00      [10]  113 	ld	hl, #0x0009
   51CE 09            [11]  114 	add	hl, bc
   51CF 36 00         [10]  115 	ld	(hl), #0x00
   51D1 C9            [10]  116 	ret
                            117 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            118 ;	---------------------------------
                            119 ; Function enemyspawn
                            120 ; ---------------------------------
   51D2                     121 _enemyspawn::
   51D2 DD E5         [15]  122 	push	ix
   51D4 DD 21 00 00   [14]  123 	ld	ix,#0
   51D8 DD 39         [15]  124 	add	ix,sp
   51DA 21 F1 FF      [10]  125 	ld	hl, #-15
   51DD 39            [11]  126 	add	hl, sp
   51DE F9            [ 6]  127 	ld	sp, hl
                            128 ;src/entities/enemy.c:23: if (!enemy) {
   51DF DD 7E 05      [19]  129 	ld	a, 5 (ix)
   51E2 DD B6 04      [19]  130 	or	a,4 (ix)
                            131 ;src/entities/enemy.c:24: return;
   51E5 CA 68 53      [10]  132 	jp	Z,00109$
                            133 ;src/entities/enemy.c:27: enemy->x = x;
   51E8 DD 7E 04      [19]  134 	ld	a, 4 (ix)
   51EB DD 77 FE      [19]  135 	ld	-2 (ix), a
   51EE DD 7E 05      [19]  136 	ld	a, 5 (ix)
   51F1 DD 77 FF      [19]  137 	ld	-1 (ix), a
   51F4 DD 6E FE      [19]  138 	ld	l,-2 (ix)
   51F7 DD 66 FF      [19]  139 	ld	h,-1 (ix)
   51FA DD 7E 06      [19]  140 	ld	a, 6 (ix)
   51FD 77            [ 7]  141 	ld	(hl), a
                            142 ;src/entities/enemy.c:28: enemy->y = y;
   51FE DD 4E FE      [19]  143 	ld	c,-2 (ix)
   5201 DD 46 FF      [19]  144 	ld	b,-1 (ix)
   5204 03            [ 6]  145 	inc	bc
   5205 DD 7E 07      [19]  146 	ld	a, 7 (ix)
   5208 02            [ 7]  147 	ld	(bc), a
                            148 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   5209 DD 7E FE      [19]  149 	ld	a, -2 (ix)
   520C C6 02         [ 7]  150 	add	a, #0x02
   520E DD 77 FC      [19]  151 	ld	-4 (ix), a
   5211 DD 7E FF      [19]  152 	ld	a, -1 (ix)
   5214 CE 00         [ 7]  153 	adc	a, #0x00
   5216 DD 77 FD      [19]  154 	ld	-3 (ix), a
   5219 DD 7E 09      [19]  155 	ld	a, 9 (ix)
   521C B7            [ 4]  156 	or	a, a
   521D 28 04         [12]  157 	jr	Z,00111$
   521F 0E 01         [ 7]  158 	ld	c, #0x01
   5221 18 02         [12]  159 	jr	00112$
   5223                     160 00111$:
   5223 0E FF         [ 7]  161 	ld	c, #0xff
   5225                     162 00112$:
   5225 DD 6E FC      [19]  163 	ld	l,-4 (ix)
   5228 DD 66 FD      [19]  164 	ld	h,-3 (ix)
   522B 71            [ 7]  165 	ld	(hl), c
                            166 ;src/entities/enemy.c:30: enemy->vy = 0;
   522C DD 7E FE      [19]  167 	ld	a, -2 (ix)
   522F C6 03         [ 7]  168 	add	a, #0x03
   5231 DD 77 FA      [19]  169 	ld	-6 (ix), a
   5234 DD 7E FF      [19]  170 	ld	a, -1 (ix)
   5237 CE 00         [ 7]  171 	adc	a, #0x00
   5239 DD 77 FB      [19]  172 	ld	-5 (ix), a
   523C DD 6E FA      [19]  173 	ld	l,-6 (ix)
   523F DD 66 FB      [19]  174 	ld	h,-5 (ix)
   5242 36 00         [10]  175 	ld	(hl), #0x00
                            176 ;src/entities/enemy.c:31: enemy->active = 1;
   5244 DD 7E FE      [19]  177 	ld	a, -2 (ix)
   5247 C6 06         [ 7]  178 	add	a, #0x06
   5249 DD 77 F8      [19]  179 	ld	-8 (ix), a
   524C DD 7E FF      [19]  180 	ld	a, -1 (ix)
   524F CE 00         [ 7]  181 	adc	a, #0x00
   5251 DD 77 F9      [19]  182 	ld	-7 (ix), a
   5254 DD 6E F8      [19]  183 	ld	l,-8 (ix)
   5257 DD 66 F9      [19]  184 	ld	h,-7 (ix)
   525A 36 01         [10]  185 	ld	(hl), #0x01
                            186 ;src/entities/enemy.c:32: enemy->kind = kind;
   525C DD 7E FE      [19]  187 	ld	a, -2 (ix)
   525F C6 09         [ 7]  188 	add	a, #0x09
   5261 DD 77 F8      [19]  189 	ld	-8 (ix), a
   5264 DD 7E FF      [19]  190 	ld	a, -1 (ix)
   5267 CE 00         [ 7]  191 	adc	a, #0x00
   5269 DD 77 F9      [19]  192 	ld	-7 (ix), a
   526C DD 6E F8      [19]  193 	ld	l,-8 (ix)
   526F DD 66 F9      [19]  194 	ld	h,-7 (ix)
   5272 DD 7E 08      [19]  195 	ld	a, 8 (ix)
   5275 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/enemy.c:35: enemy->w = 5;
   5276 DD 7E FE      [19]  198 	ld	a, -2 (ix)
   5279 C6 04         [ 7]  199 	add	a, #0x04
   527B DD 77 F8      [19]  200 	ld	-8 (ix), a
   527E DD 7E FF      [19]  201 	ld	a, -1 (ix)
   5281 CE 00         [ 7]  202 	adc	a, #0x00
   5283 DD 77 F9      [19]  203 	ld	-7 (ix), a
                            204 ;src/entities/enemy.c:36: enemy->h = 14;
   5286 DD 7E FE      [19]  205 	ld	a, -2 (ix)
   5289 C6 05         [ 7]  206 	add	a, #0x05
   528B DD 77 F6      [19]  207 	ld	-10 (ix), a
   528E DD 7E FF      [19]  208 	ld	a, -1 (ix)
   5291 CE 00         [ 7]  209 	adc	a, #0x00
   5293 DD 77 F7      [19]  210 	ld	-9 (ix), a
                            211 ;src/entities/enemy.c:37: enemy->health = 2;
   5296 DD 7E FE      [19]  212 	ld	a, -2 (ix)
   5299 C6 07         [ 7]  213 	add	a, #0x07
   529B DD 77 F4      [19]  214 	ld	-12 (ix), a
   529E DD 7E FF      [19]  215 	ld	a, -1 (ix)
   52A1 CE 00         [ 7]  216 	adc	a, #0x00
   52A3 DD 77 F5      [19]  217 	ld	-11 (ix), a
                            218 ;src/entities/enemy.c:38: enemy->reward = 180;
   52A6 DD 7E FE      [19]  219 	ld	a, -2 (ix)
   52A9 C6 08         [ 7]  220 	add	a, #0x08
   52AB DD 77 FE      [19]  221 	ld	-2 (ix), a
   52AE DD 7E FF      [19]  222 	ld	a, -1 (ix)
   52B1 CE 00         [ 7]  223 	adc	a, #0x00
   52B3 DD 77 FF      [19]  224 	ld	-1 (ix), a
                            225 ;src/entities/enemy.c:34: if (kind == 1) {
   52B6 DD 7E 08      [19]  226 	ld	a, 8 (ix)
   52B9 3D            [ 4]  227 	dec	a
   52BA 20 48         [12]  228 	jr	NZ,00107$
                            229 ;src/entities/enemy.c:35: enemy->w = 5;
   52BC DD 6E F8      [19]  230 	ld	l,-8 (ix)
   52BF DD 66 F9      [19]  231 	ld	h,-7 (ix)
   52C2 36 05         [10]  232 	ld	(hl), #0x05
                            233 ;src/entities/enemy.c:36: enemy->h = 14;
   52C4 DD 6E F6      [19]  234 	ld	l,-10 (ix)
   52C7 DD 66 F7      [19]  235 	ld	h,-9 (ix)
   52CA 36 0E         [10]  236 	ld	(hl), #0x0e
                            237 ;src/entities/enemy.c:37: enemy->health = 2;
   52CC DD 6E F4      [19]  238 	ld	l,-12 (ix)
   52CF DD 66 F5      [19]  239 	ld	h,-11 (ix)
   52D2 36 02         [10]  240 	ld	(hl), #0x02
                            241 ;src/entities/enemy.c:38: enemy->reward = 180;
   52D4 DD 6E FE      [19]  242 	ld	l,-2 (ix)
   52D7 DD 66 FF      [19]  243 	ld	h,-1 (ix)
   52DA 36 B4         [10]  244 	ld	(hl), #0xb4
                            245 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   52DC DD 7E FC      [19]  246 	ld	a, -4 (ix)
   52DF DD 77 F2      [19]  247 	ld	-14 (ix), a
   52E2 DD 7E FD      [19]  248 	ld	a, -3 (ix)
   52E5 DD 77 F3      [19]  249 	ld	-13 (ix), a
   52E8 DD 7E 09      [19]  250 	ld	a, 9 (ix)
   52EB B7            [ 4]  251 	or	a, a
   52EC 28 06         [12]  252 	jr	Z,00113$
   52EE DD 36 F1 02   [19]  253 	ld	-15 (ix), #0x02
   52F2 18 04         [12]  254 	jr	00114$
   52F4                     255 00113$:
   52F4 DD 36 F1 FE   [19]  256 	ld	-15 (ix), #0xfe
   52F8                     257 00114$:
   52F8 DD 6E F2      [19]  258 	ld	l,-14 (ix)
   52FB DD 66 F3      [19]  259 	ld	h,-13 (ix)
   52FE DD 7E F1      [19]  260 	ld	a, -15 (ix)
   5301 77            [ 7]  261 	ld	(hl), a
   5302 18 64         [12]  262 	jr	00109$
   5304                     263 00107$:
                            264 ;src/entities/enemy.c:40: } else if (kind == 2) {
   5304 DD 7E 08      [19]  265 	ld	a, 8 (ix)
   5307 D6 02         [ 7]  266 	sub	a, #0x02
   5309 20 3D         [12]  267 	jr	NZ,00104$
                            268 ;src/entities/enemy.c:41: enemy->w = 6;
   530B DD 6E F8      [19]  269 	ld	l,-8 (ix)
   530E DD 66 F9      [19]  270 	ld	h,-7 (ix)
   5311 36 06         [10]  271 	ld	(hl), #0x06
                            272 ;src/entities/enemy.c:42: enemy->h = 10;
   5313 DD 6E F6      [19]  273 	ld	l,-10 (ix)
   5316 DD 66 F7      [19]  274 	ld	h,-9 (ix)
   5319 36 0A         [10]  275 	ld	(hl), #0x0a
                            276 ;src/entities/enemy.c:43: enemy->health = 1;
   531B DD 6E F4      [19]  277 	ld	l,-12 (ix)
   531E DD 66 F5      [19]  278 	ld	h,-11 (ix)
   5321 36 01         [10]  279 	ld	(hl), #0x01
                            280 ;src/entities/enemy.c:44: enemy->reward = 150;
   5323 DD 6E FE      [19]  281 	ld	l,-2 (ix)
   5326 DD 66 FF      [19]  282 	ld	h,-1 (ix)
   5329 36 96         [10]  283 	ld	(hl), #0x96
                            284 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   532B DD 4E FA      [19]  285 	ld	c,-6 (ix)
   532E DD 46 FB      [19]  286 	ld	b,-5 (ix)
   5331 DD 7E 09      [19]  287 	ld	a, 9 (ix)
   5334 B7            [ 4]  288 	or	a, a
   5335 28 04         [12]  289 	jr	Z,00115$
   5337 3E 01         [ 7]  290 	ld	a, #0x01
   5339 18 02         [12]  291 	jr	00116$
   533B                     292 00115$:
   533B 3E FF         [ 7]  293 	ld	a, #0xff
   533D                     294 00116$:
   533D 02            [ 7]  295 	ld	(bc), a
                            296 ;src/entities/enemy.c:46: enemy->vx = 1;
   533E DD 6E FC      [19]  297 	ld	l,-4 (ix)
   5341 DD 66 FD      [19]  298 	ld	h,-3 (ix)
   5344 36 01         [10]  299 	ld	(hl), #0x01
   5346 18 20         [12]  300 	jr	00109$
   5348                     301 00104$:
                            302 ;src/entities/enemy.c:48: enemy->w = 4;
   5348 DD 6E F8      [19]  303 	ld	l,-8 (ix)
   534B DD 66 F9      [19]  304 	ld	h,-7 (ix)
   534E 36 04         [10]  305 	ld	(hl), #0x04
                            306 ;src/entities/enemy.c:49: enemy->h = 16;
   5350 DD 6E F6      [19]  307 	ld	l,-10 (ix)
   5353 DD 66 F7      [19]  308 	ld	h,-9 (ix)
   5356 36 10         [10]  309 	ld	(hl), #0x10
                            310 ;src/entities/enemy.c:50: enemy->health = 1;
   5358 DD 6E F4      [19]  311 	ld	l,-12 (ix)
   535B DD 66 F5      [19]  312 	ld	h,-11 (ix)
   535E 36 01         [10]  313 	ld	(hl), #0x01
                            314 ;src/entities/enemy.c:51: enemy->reward = 100;
   5360 DD 6E FE      [19]  315 	ld	l,-2 (ix)
   5363 DD 66 FF      [19]  316 	ld	h,-1 (ix)
   5366 36 64         [10]  317 	ld	(hl), #0x64
   5368                     318 00109$:
   5368 DD F9         [10]  319 	ld	sp, ix
   536A DD E1         [14]  320 	pop	ix
   536C C9            [10]  321 	ret
                            322 ;src/entities/enemy.c:55: void enemyupdate(Enemy* enemy) {
                            323 ;	---------------------------------
                            324 ; Function enemyupdate
                            325 ; ---------------------------------
   536D                     326 _enemyupdate::
   536D DD E5         [15]  327 	push	ix
   536F DD 21 00 00   [14]  328 	ld	ix,#0
   5373 DD 39         [15]  329 	add	ix,sp
   5375 21 F6 FF      [10]  330 	ld	hl, #-10
   5378 39            [11]  331 	add	hl, sp
   5379 F9            [ 6]  332 	ld	sp, hl
                            333 ;src/entities/enemy.c:59: if (!enemy || !enemy->active) {
   537A DD 7E 05      [19]  334 	ld	a, 5 (ix)
   537D DD B6 04      [19]  335 	or	a,4 (ix)
   5380 CA 63 55      [10]  336 	jp	Z,00121$
   5383 DD 7E 04      [19]  337 	ld	a, 4 (ix)
   5386 DD 77 FE      [19]  338 	ld	-2 (ix), a
   5389 DD 7E 05      [19]  339 	ld	a, 5 (ix)
   538C DD 77 FF      [19]  340 	ld	-1 (ix), a
   538F DD 6E FE      [19]  341 	ld	l,-2 (ix)
   5392 DD 66 FF      [19]  342 	ld	h,-1 (ix)
   5395 11 06 00      [10]  343 	ld	de, #0x0006
   5398 19            [11]  344 	add	hl, de
   5399 7E            [ 7]  345 	ld	a, (hl)
   539A B7            [ 4]  346 	or	a, a
                            347 ;src/entities/enemy.c:60: return;
   539B CA 63 55      [10]  348 	jp	Z,00121$
                            349 ;src/entities/enemy.c:63: if (enemy->kind == 2) {
   539E DD 6E FE      [19]  350 	ld	l,-2 (ix)
   53A1 DD 66 FF      [19]  351 	ld	h,-1 (ix)
   53A4 11 09 00      [10]  352 	ld	de, #0x0009
   53A7 19            [11]  353 	add	hl, de
   53A8 7E            [ 7]  354 	ld	a, (hl)
   53A9 DD 77 FD      [19]  355 	ld	-3 (ix), a
                            356 ;src/entities/enemy.c:64: nextx = (i16)enemy->x + (i16)enemy->vx;
   53AC DD 6E FE      [19]  357 	ld	l,-2 (ix)
   53AF DD 66 FF      [19]  358 	ld	h,-1 (ix)
   53B2 4E            [ 7]  359 	ld	c, (hl)
   53B3 DD 7E FE      [19]  360 	ld	a, -2 (ix)
   53B6 C6 02         [ 7]  361 	add	a, #0x02
   53B8 DD 77 FB      [19]  362 	ld	-5 (ix), a
   53BB DD 7E FF      [19]  363 	ld	a, -1 (ix)
   53BE CE 00         [ 7]  364 	adc	a, #0x00
   53C0 DD 77 FC      [19]  365 	ld	-4 (ix), a
                            366 ;src/entities/enemy.c:65: nexty = (i16)enemy->y + (i16)enemy->vy;
   53C3 DD 7E FE      [19]  367 	ld	a, -2 (ix)
   53C6 C6 01         [ 7]  368 	add	a, #0x01
   53C8 DD 77 F9      [19]  369 	ld	-7 (ix), a
   53CB DD 7E FF      [19]  370 	ld	a, -1 (ix)
   53CE CE 00         [ 7]  371 	adc	a, #0x00
   53D0 DD 77 FA      [19]  372 	ld	-6 (ix), a
   53D3 DD 5E FE      [19]  373 	ld	e,-2 (ix)
   53D6 DD 56 FF      [19]  374 	ld	d,-1 (ix)
   53D9 13            [ 6]  375 	inc	de
   53DA 13            [ 6]  376 	inc	de
   53DB 13            [ 6]  377 	inc	de
                            378 ;src/entities/enemy.c:64: nextx = (i16)enemy->x + (i16)enemy->vx;
   53DC 06 00         [ 7]  379 	ld	b, #0x00
   53DE DD 6E FB      [19]  380 	ld	l,-5 (ix)
   53E1 DD 66 FC      [19]  381 	ld	h,-4 (ix)
   53E4 7E            [ 7]  382 	ld	a, (hl)
   53E5 DD 77 F8      [19]  383 	ld	-8 (ix), a
   53E8 6F            [ 4]  384 	ld	l, a
   53E9 DD 7E F8      [19]  385 	ld	a, -8 (ix)
   53EC 17            [ 4]  386 	rla
   53ED 9F            [ 4]  387 	sbc	a, a
   53EE 67            [ 4]  388 	ld	h, a
   53EF 09            [11]  389 	add	hl,bc
   53F0 4D            [ 4]  390 	ld	c, l
   53F1 44            [ 4]  391 	ld	b, h
                            392 ;src/entities/enemy.c:63: if (enemy->kind == 2) {
   53F2 DD 7E FD      [19]  393 	ld	a, -3 (ix)
   53F5 D6 02         [ 7]  394 	sub	a, #0x02
   53F7 C2 A0 54      [10]  395 	jp	NZ,00111$
                            396 ;src/entities/enemy.c:64: nextx = (i16)enemy->x + (i16)enemy->vx;
                            397 ;src/entities/enemy.c:65: nexty = (i16)enemy->y + (i16)enemy->vy;
   53FA DD 6E F9      [19]  398 	ld	l,-7 (ix)
   53FD DD 66 FA      [19]  399 	ld	h,-6 (ix)
   5400 6E            [ 7]  400 	ld	l, (hl)
   5401 DD 75 F6      [19]  401 	ld	-10 (ix), l
   5404 DD 36 F7 00   [19]  402 	ld	-9 (ix), #0x00
   5408 1A            [ 7]  403 	ld	a, (de)
   5409 6F            [ 4]  404 	ld	l, a
   540A 17            [ 4]  405 	rla
   540B 9F            [ 4]  406 	sbc	a, a
   540C 67            [ 4]  407 	ld	h, a
   540D DD 7E F6      [19]  408 	ld	a, -10 (ix)
   5410 85            [ 4]  409 	add	a, l
   5411 DD 77 F6      [19]  410 	ld	-10 (ix), a
   5414 DD 7E F7      [19]  411 	ld	a, -9 (ix)
   5417 8C            [ 4]  412 	adc	a, h
   5418 DD 77 F7      [19]  413 	ld	-9 (ix), a
                            414 ;src/entities/enemy.c:67: if (nextx < 8 || nextx > 72) {
   541B 79            [ 4]  415 	ld	a, c
   541C D6 08         [ 7]  416 	sub	a, #0x08
   541E 78            [ 4]  417 	ld	a, b
   541F 17            [ 4]  418 	rla
   5420 3F            [ 4]  419 	ccf
   5421 1F            [ 4]  420 	rra
   5422 DE 80         [ 7]  421 	sbc	a, #0x80
   5424 38 0E         [12]  422 	jr	C,00104$
   5426 3E 48         [ 7]  423 	ld	a, #0x48
   5428 B9            [ 4]  424 	cp	a, c
   5429 3E 00         [ 7]  425 	ld	a, #0x00
   542B 98            [ 4]  426 	sbc	a, b
   542C E2 31 54      [10]  427 	jp	PO, 00161$
   542F EE 80         [ 7]  428 	xor	a, #0x80
   5431                     429 00161$:
   5431 F2 4F 54      [10]  430 	jp	P, 00105$
   5434                     431 00104$:
                            432 ;src/entities/enemy.c:68: enemy->vx = (i8)(-enemy->vx);
   5434 AF            [ 4]  433 	xor	a, a
   5435 DD 96 F8      [19]  434 	sub	a, -8 (ix)
   5438 4F            [ 4]  435 	ld	c, a
   5439 DD 6E FB      [19]  436 	ld	l,-5 (ix)
   543C DD 66 FC      [19]  437 	ld	h,-4 (ix)
   543F 71            [ 7]  438 	ld	(hl), c
                            439 ;src/entities/enemy.c:69: nextx = (i16)enemy->x + (i16)enemy->vx;
   5440 DD 6E FE      [19]  440 	ld	l,-2 (ix)
   5443 DD 66 FF      [19]  441 	ld	h,-1 (ix)
   5446 6E            [ 7]  442 	ld	l, (hl)
   5447 26 00         [ 7]  443 	ld	h, #0x00
   5449 79            [ 4]  444 	ld	a, c
   544A 17            [ 4]  445 	rla
   544B 9F            [ 4]  446 	sbc	a, a
   544C 47            [ 4]  447 	ld	b, a
   544D 09            [11]  448 	add	hl,bc
   544E 4D            [ 4]  449 	ld	c, l
   544F                     450 00105$:
                            451 ;src/entities/enemy.c:71: if (nexty < 56 || nexty > 120) {
   544F DD 7E F6      [19]  452 	ld	a, -10 (ix)
   5452 D6 38         [ 7]  453 	sub	a, #0x38
   5454 DD 7E F7      [19]  454 	ld	a, -9 (ix)
   5457 17            [ 4]  455 	rla
   5458 3F            [ 4]  456 	ccf
   5459 1F            [ 4]  457 	rra
   545A DE 80         [ 7]  458 	sbc	a, #0x80
   545C 38 12         [12]  459 	jr	C,00107$
   545E 3E 78         [ 7]  460 	ld	a, #0x78
   5460 DD BE F6      [19]  461 	cp	a, -10 (ix)
   5463 3E 00         [ 7]  462 	ld	a, #0x00
   5465 DD 9E F7      [19]  463 	sbc	a, -9 (ix)
   5468 E2 6D 54      [10]  464 	jp	PO, 00162$
   546B EE 80         [ 7]  465 	xor	a, #0x80
   546D                     466 00162$:
   546D F2 8C 54      [10]  467 	jp	P, 00108$
   5470                     468 00107$:
                            469 ;src/entities/enemy.c:72: enemy->vy = (i8)(-enemy->vy);
   5470 1A            [ 7]  470 	ld	a, (de)
   5471 6F            [ 4]  471 	ld	l, a
   5472 AF            [ 4]  472 	xor	a, a
   5473 95            [ 4]  473 	sub	a, l
   5474 DD 77 F8      [19]  474 	ld	-8 (ix), a
   5477 12            [ 7]  475 	ld	(de),a
                            476 ;src/entities/enemy.c:73: nexty = (i16)enemy->y + (i16)enemy->vy;
   5478 DD 6E F9      [19]  477 	ld	l,-7 (ix)
   547B DD 66 FA      [19]  478 	ld	h,-6 (ix)
   547E 5E            [ 7]  479 	ld	e, (hl)
   547F 16 00         [ 7]  480 	ld	d, #0x00
   5481 DD 6E F8      [19]  481 	ld	l, -8 (ix)
   5484 DD 7E F8      [19]  482 	ld	a, -8 (ix)
   5487 17            [ 4]  483 	rla
   5488 9F            [ 4]  484 	sbc	a, a
   5489 67            [ 4]  485 	ld	h, a
   548A 19            [11]  486 	add	hl,de
   548B E3            [19]  487 	ex	(sp), hl
   548C                     488 00108$:
                            489 ;src/entities/enemy.c:76: enemy->x = (u8)nextx;
   548C DD 6E FE      [19]  490 	ld	l,-2 (ix)
   548F DD 66 FF      [19]  491 	ld	h,-1 (ix)
   5492 71            [ 7]  492 	ld	(hl), c
                            493 ;src/entities/enemy.c:77: enemy->y = (u8)nexty;
   5493 DD 4E F6      [19]  494 	ld	c, -10 (ix)
   5496 DD 6E F9      [19]  495 	ld	l,-7 (ix)
   5499 DD 66 FA      [19]  496 	ld	h,-6 (ix)
   549C 71            [ 7]  497 	ld	(hl), c
                            498 ;src/entities/enemy.c:78: return;
   549D C3 63 55      [10]  499 	jp	00121$
   54A0                     500 00111$:
                            501 ;src/entities/enemy.c:81: nextx = (i16)enemy->x + (i16)enemy->vx;
                            502 ;src/entities/enemy.c:82: if (nextx < 2) {
   54A0 79            [ 4]  503 	ld	a, c
   54A1 D6 02         [ 7]  504 	sub	a, #0x02
   54A3 78            [ 4]  505 	ld	a, b
   54A4 17            [ 4]  506 	rla
   54A5 3F            [ 4]  507 	ccf
   54A6 1F            [ 4]  508 	rra
   54A7 DE 80         [ 7]  509 	sbc	a, #0x80
   54A9 30 0B         [12]  510 	jr	NC,00113$
                            511 ;src/entities/enemy.c:83: nextx = 2;
   54AB 01 02 00      [10]  512 	ld	bc, #0x0002
                            513 ;src/entities/enemy.c:84: enemy->vx = 1;
   54AE DD 6E FB      [19]  514 	ld	l,-5 (ix)
   54B1 DD 66 FC      [19]  515 	ld	h,-4 (ix)
   54B4 36 01         [10]  516 	ld	(hl), #0x01
   54B6                     517 00113$:
                            518 ;src/entities/enemy.c:86: if (nextx > 74) {
   54B6 3E 4A         [ 7]  519 	ld	a, #0x4a
   54B8 B9            [ 4]  520 	cp	a, c
   54B9 3E 00         [ 7]  521 	ld	a, #0x00
   54BB 98            [ 4]  522 	sbc	a, b
   54BC E2 C1 54      [10]  523 	jp	PO, 00163$
   54BF EE 80         [ 7]  524 	xor	a, #0x80
   54C1                     525 00163$:
   54C1 F2 CF 54      [10]  526 	jp	P, 00115$
                            527 ;src/entities/enemy.c:87: nextx = 74;
   54C4 01 4A 00      [10]  528 	ld	bc, #0x004a
                            529 ;src/entities/enemy.c:88: enemy->vx = -1;
   54C7 DD 6E FB      [19]  530 	ld	l,-5 (ix)
   54CA DD 66 FC      [19]  531 	ld	h,-4 (ix)
   54CD 36 FF         [10]  532 	ld	(hl), #0xff
   54CF                     533 00115$:
                            534 ;src/entities/enemy.c:90: enemy->x = (u8)nextx;
   54CF DD 6E FE      [19]  535 	ld	l,-2 (ix)
   54D2 DD 66 FF      [19]  536 	ld	h,-1 (ix)
   54D5 71            [ 7]  537 	ld	(hl), c
                            538 ;src/entities/enemy.c:92: enemy->vy = (i8)(enemy->vy + 1);
   54D6 1A            [ 7]  539 	ld	a, (de)
   54D7 4F            [ 4]  540 	ld	c, a
   54D8 0C            [ 4]  541 	inc	c
   54D9 79            [ 4]  542 	ld	a, c
   54DA 12            [ 7]  543 	ld	(de), a
                            544 ;src/entities/enemy.c:93: if (enemy->vy > 3) enemy->vy = 3;
   54DB 3E 03         [ 7]  545 	ld	a, #0x03
   54DD 91            [ 4]  546 	sub	a, c
   54DE E2 E3 54      [10]  547 	jp	PO, 00164$
   54E1 EE 80         [ 7]  548 	xor	a, #0x80
   54E3                     549 00164$:
   54E3 F2 E9 54      [10]  550 	jp	P, 00117$
   54E6 3E 03         [ 7]  551 	ld	a, #0x03
   54E8 12            [ 7]  552 	ld	(de), a
   54E9                     553 00117$:
                            554 ;src/entities/enemy.c:94: nexty = (i16)enemy->y + (i16)enemy->vy;
   54E9 DD 6E F9      [19]  555 	ld	l,-7 (ix)
   54EC DD 66 FA      [19]  556 	ld	h,-6 (ix)
   54EF 4E            [ 7]  557 	ld	c, (hl)
   54F0 06 00         [ 7]  558 	ld	b, #0x00
   54F2 1A            [ 7]  559 	ld	a, (de)
   54F3 6F            [ 4]  560 	ld	l, a
   54F4 17            [ 4]  561 	rla
   54F5 9F            [ 4]  562 	sbc	a, a
   54F6 67            [ 4]  563 	ld	h, a
   54F7 09            [11]  564 	add	hl, bc
   54F8 E5            [11]  565 	push	hl
   54F9 FD E1         [14]  566 	pop	iy
                            567 ;src/entities/enemy.c:95: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   54FB DD 7E FE      [19]  568 	ld	a, -2 (ix)
   54FE C6 05         [ 7]  569 	add	a, #0x05
   5500 DD 77 F6      [19]  570 	ld	-10 (ix), a
   5503 DD 7E FF      [19]  571 	ld	a, -1 (ix)
   5506 CE 00         [ 7]  572 	adc	a, #0x00
   5508 DD 77 F7      [19]  573 	ld	-9 (ix), a
   550B E1            [10]  574 	pop	hl
   550C E5            [11]  575 	push	hl
   550D 7E            [ 7]  576 	ld	a, (hl)
   550E DD 6E FE      [19]  577 	ld	l,-2 (ix)
   5511 DD 66 FF      [19]  578 	ld	h,-1 (ix)
   5514 4E            [ 7]  579 	ld	c, (hl)
   5515 06 00         [ 7]  580 	ld	b, #0x00
   5517 D5            [11]  581 	push	de
   5518 F5            [11]  582 	push	af
   5519 33            [ 6]  583 	inc	sp
   551A FD E5         [15]  584 	push	iy
   551C C5            [11]  585 	push	bc
   551D CD BA 4A      [17]  586 	call	_collision_clamp_y_at
   5520 F1            [10]  587 	pop	af
   5521 F1            [10]  588 	pop	af
   5522 33            [ 6]  589 	inc	sp
   5523 4D            [ 4]  590 	ld	c, l
   5524 D1            [10]  591 	pop	de
                            592 ;src/entities/enemy.c:96: enemy->y = (u8)nexty;
   5525 DD 6E F9      [19]  593 	ld	l,-7 (ix)
   5528 DD 66 FA      [19]  594 	ld	h,-6 (ix)
   552B 71            [ 7]  595 	ld	(hl), c
                            596 ;src/entities/enemy.c:97: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   552C E1            [10]  597 	pop	hl
   552D E5            [11]  598 	push	hl
   552E 7E            [ 7]  599 	ld	a, (hl)
   552F 06 00         [ 7]  600 	ld	b, #0x00
   5531 DD 6E FE      [19]  601 	ld	l,-2 (ix)
   5534 DD 66 FF      [19]  602 	ld	h,-1 (ix)
   5537 6E            [ 7]  603 	ld	l, (hl)
   5538 DD 75 F6      [19]  604 	ld	-10 (ix), l
   553B DD 36 F7 00   [19]  605 	ld	-9 (ix), #0x00
   553F D5            [11]  606 	push	de
   5540 F5            [11]  607 	push	af
   5541 33            [ 6]  608 	inc	sp
   5542 C5            [11]  609 	push	bc
   5543 DD 6E F6      [19]  610 	ld	l,-10 (ix)
   5546 DD 66 F7      [19]  611 	ld	h,-9 (ix)
   5549 E5            [11]  612 	push	hl
   554A CD 3B 4A      [17]  613 	call	_collision_is_on_ground_at
   554D F1            [10]  614 	pop	af
   554E F1            [10]  615 	pop	af
   554F 33            [ 6]  616 	inc	sp
   5550 D1            [10]  617 	pop	de
   5551 7D            [ 4]  618 	ld	a, l
   5552 B7            [ 4]  619 	or	a, a
   5553 28 0E         [12]  620 	jr	Z,00121$
   5555 1A            [ 7]  621 	ld	a, (de)
   5556 4F            [ 4]  622 	ld	c, a
   5557 AF            [ 4]  623 	xor	a, a
   5558 91            [ 4]  624 	sub	a, c
   5559 E2 5E 55      [10]  625 	jp	PO, 00165$
   555C EE 80         [ 7]  626 	xor	a, #0x80
   555E                     627 00165$:
   555E F2 63 55      [10]  628 	jp	P, 00121$
                            629 ;src/entities/enemy.c:98: enemy->vy = 0;
   5561 AF            [ 4]  630 	xor	a, a
   5562 12            [ 7]  631 	ld	(de), a
   5563                     632 00121$:
   5563 DD F9         [10]  633 	ld	sp, ix
   5565 DD E1         [14]  634 	pop	ix
   5567 C9            [10]  635 	ret
                            636 ;src/entities/enemy.c:102: void enemyrender(const Enemy* enemy) {
                            637 ;	---------------------------------
                            638 ; Function enemyrender
                            639 ; ---------------------------------
   5568                     640 _enemyrender::
   5568 DD E5         [15]  641 	push	ix
   556A DD 21 00 00   [14]  642 	ld	ix,#0
   556E DD 39         [15]  643 	add	ix,sp
                            644 ;src/entities/enemy.c:105: if (!enemy || !enemy->active) {
   5570 DD 7E 05      [19]  645 	ld	a, 5 (ix)
   5573 DD B6 04      [19]  646 	or	a,4 (ix)
   5576 28 3C         [12]  647 	jr	Z,00104$
   5578 DD 4E 04      [19]  648 	ld	c,4 (ix)
   557B DD 46 05      [19]  649 	ld	b,5 (ix)
   557E C5            [11]  650 	push	bc
   557F FD E1         [14]  651 	pop	iy
   5581 FD 7E 06      [19]  652 	ld	a, 6 (iy)
   5584 B7            [ 4]  653 	or	a, a
                            654 ;src/entities/enemy.c:106: return;
   5585 28 2D         [12]  655 	jr	Z,00104$
                            656 ;src/entities/enemy.c:109: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5587 69            [ 4]  657 	ld	l, c
   5588 60            [ 4]  658 	ld	h, b
   5589 23            [ 6]  659 	inc	hl
   558A 56            [ 7]  660 	ld	d, (hl)
   558B 0A            [ 7]  661 	ld	a, (bc)
   558C C5            [11]  662 	push	bc
   558D 5F            [ 4]  663 	ld	e, a
   558E D5            [11]  664 	push	de
   558F 21 00 C0      [10]  665 	ld	hl, #0xc000
   5592 E5            [11]  666 	push	hl
   5593 CD 4E 5E      [17]  667 	call	_cpct_getScreenPtr
   5596 EB            [ 4]  668 	ex	de,hl
   5597 C1            [10]  669 	pop	bc
                            670 ;src/entities/enemy.c:110: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
   5598 C5            [11]  671 	push	bc
   5599 FD E1         [14]  672 	pop	iy
   559B FD 7E 05      [19]  673 	ld	a, 5 (iy)
   559E 69            [ 4]  674 	ld	l, c
   559F 60            [ 4]  675 	ld	h, b
   55A0 01 04 00      [10]  676 	ld	bc, #0x0004
   55A3 09            [11]  677 	add	hl, bc
   55A4 46            [ 7]  678 	ld	b, (hl)
   55A5 F5            [11]  679 	push	af
   55A6 33            [ 6]  680 	inc	sp
   55A7 C5            [11]  681 	push	bc
   55A8 33            [ 6]  682 	inc	sp
   55A9 3E 5C         [ 7]  683 	ld	a, #0x5c
   55AB F5            [11]  684 	push	af
   55AC 33            [ 6]  685 	inc	sp
   55AD D5            [11]  686 	push	de
   55AE CD 95 5D      [17]  687 	call	_cpct_drawSolidBox
   55B1 F1            [10]  688 	pop	af
   55B2 F1            [10]  689 	pop	af
   55B3 33            [ 6]  690 	inc	sp
   55B4                     691 00104$:
   55B4 DD E1         [14]  692 	pop	ix
   55B6 C9            [10]  693 	ret
                            694 ;src/entities/enemy.c:113: u8 enemydamage(Enemy* enemy, u8 damage) {
                            695 ;	---------------------------------
                            696 ; Function enemydamage
                            697 ; ---------------------------------
   55B7                     698 _enemydamage::
   55B7 DD E5         [15]  699 	push	ix
   55B9 DD 21 00 00   [14]  700 	ld	ix,#0
   55BD DD 39         [15]  701 	add	ix,sp
                            702 ;src/entities/enemy.c:114: if (!enemy || !enemy->active) {
   55BF DD 7E 05      [19]  703 	ld	a, 5 (ix)
   55C2 DD B6 04      [19]  704 	or	a,4 (ix)
   55C5 28 0F         [12]  705 	jr	Z,00101$
   55C7 DD 4E 04      [19]  706 	ld	c,4 (ix)
   55CA DD 46 05      [19]  707 	ld	b,5 (ix)
   55CD 21 06 00      [10]  708 	ld	hl, #0x0006
   55D0 09            [11]  709 	add	hl,bc
   55D1 EB            [ 4]  710 	ex	de,hl
   55D2 1A            [ 7]  711 	ld	a, (de)
   55D3 B7            [ 4]  712 	or	a, a
   55D4 20 04         [12]  713 	jr	NZ,00102$
   55D6                     714 00101$:
                            715 ;src/entities/enemy.c:115: return 0;
   55D6 2E 00         [ 7]  716 	ld	l, #0x00
   55D8 18 1A         [12]  717 	jr	00106$
   55DA                     718 00102$:
                            719 ;src/entities/enemy.c:118: if (damage >= enemy->health) {
   55DA 21 07 00      [10]  720 	ld	hl, #0x0007
   55DD 09            [11]  721 	add	hl, bc
   55DE 4E            [ 7]  722 	ld	c, (hl)
   55DF DD 7E 06      [19]  723 	ld	a, 6 (ix)
   55E2 91            [ 4]  724 	sub	a, c
   55E3 38 08         [12]  725 	jr	C,00105$
                            726 ;src/entities/enemy.c:119: enemy->health = 0;
   55E5 36 00         [10]  727 	ld	(hl), #0x00
                            728 ;src/entities/enemy.c:120: enemy->active = 0;
   55E7 AF            [ 4]  729 	xor	a, a
   55E8 12            [ 7]  730 	ld	(de), a
                            731 ;src/entities/enemy.c:121: return 1;
   55E9 2E 01         [ 7]  732 	ld	l, #0x01
   55EB 18 07         [12]  733 	jr	00106$
   55ED                     734 00105$:
                            735 ;src/entities/enemy.c:124: enemy->health = (u8)(enemy->health - damage);
   55ED 79            [ 4]  736 	ld	a, c
   55EE DD 96 06      [19]  737 	sub	a, 6 (ix)
   55F1 77            [ 7]  738 	ld	(hl), a
                            739 ;src/entities/enemy.c:125: return 0;
   55F2 2E 00         [ 7]  740 	ld	l, #0x00
   55F4                     741 00106$:
   55F4 DD E1         [14]  742 	pop	ix
   55F6 C9            [10]  743 	ret
                            744 	.area _CODE
                            745 	.area _INITIALIZER
                            746 	.area _CABS (ABS)
