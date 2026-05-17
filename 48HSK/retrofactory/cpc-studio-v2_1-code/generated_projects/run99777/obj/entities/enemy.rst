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
   554A                      56 _enemyinit::
                             57 ;src/entities/enemy.c:6: if (!enemy) {
   554A 21 03 00      [10]   58 	ld	hl, #2+1
   554D 39            [11]   59 	add	hl, sp
   554E 7E            [ 7]   60 	ld	a, (hl)
   554F 2B            [ 6]   61 	dec	hl
   5550 B6            [ 7]   62 	or	a,(hl)
                             63 ;src/entities/enemy.c:7: return;
   5551 C8            [11]   64 	ret	Z
                             65 ;src/entities/enemy.c:10: enemy->x = 0;
   5552 D1            [10]   66 	pop	de
   5553 C1            [10]   67 	pop	bc
   5554 C5            [11]   68 	push	bc
   5555 D5            [11]   69 	push	de
   5556 AF            [ 4]   70 	xor	a, a
   5557 02            [ 7]   71 	ld	(bc), a
                             72 ;src/entities/enemy.c:11: enemy->y = 0;
   5558 59            [ 4]   73 	ld	e, c
   5559 50            [ 4]   74 	ld	d, b
   555A 13            [ 6]   75 	inc	de
   555B AF            [ 4]   76 	xor	a, a
   555C 12            [ 7]   77 	ld	(de), a
                             78 ;src/entities/enemy.c:12: enemy->vx = 0;
   555D 59            [ 4]   79 	ld	e, c
   555E 50            [ 4]   80 	ld	d, b
   555F 13            [ 6]   81 	inc	de
   5560 13            [ 6]   82 	inc	de
   5561 AF            [ 4]   83 	xor	a, a
   5562 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/enemy.c:13: enemy->vy = 0;
   5563 59            [ 4]   86 	ld	e, c
   5564 50            [ 4]   87 	ld	d, b
   5565 13            [ 6]   88 	inc	de
   5566 13            [ 6]   89 	inc	de
   5567 13            [ 6]   90 	inc	de
   5568 AF            [ 4]   91 	xor	a, a
   5569 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/enemy.c:14: enemy->w = 4;
   556A 21 04 00      [10]   94 	ld	hl, #0x0004
   556D 09            [11]   95 	add	hl, bc
   556E 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/enemy.c:15: enemy->h = 16;
   5570 21 05 00      [10]   98 	ld	hl, #0x0005
   5573 09            [11]   99 	add	hl, bc
   5574 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/enemy.c:16: enemy->active = 0;
   5576 21 06 00      [10]  102 	ld	hl, #0x0006
   5579 09            [11]  103 	add	hl, bc
   557A 36 00         [10]  104 	ld	(hl), #0x00
                            105 ;src/entities/enemy.c:17: enemy->health = 1;
   557C 21 07 00      [10]  106 	ld	hl, #0x0007
   557F 09            [11]  107 	add	hl, bc
   5580 36 01         [10]  108 	ld	(hl), #0x01
                            109 ;src/entities/enemy.c:18: enemy->reward = 100;
   5582 21 08 00      [10]  110 	ld	hl, #0x0008
   5585 09            [11]  111 	add	hl, bc
   5586 36 64         [10]  112 	ld	(hl), #0x64
   5588 23            [ 6]  113 	inc	hl
   5589 36 00         [10]  114 	ld	(hl), #0x00
                            115 ;src/entities/enemy.c:19: enemy->kind = 0;
   558B 21 0A 00      [10]  116 	ld	hl, #0x000a
   558E 09            [11]  117 	add	hl, bc
   558F 36 00         [10]  118 	ld	(hl), #0x00
   5591 C9            [10]  119 	ret
                            120 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            121 ;	---------------------------------
                            122 ; Function enemyspawn
                            123 ; ---------------------------------
   5592                     124 _enemyspawn::
   5592 DD E5         [15]  125 	push	ix
   5594 DD 21 00 00   [14]  126 	ld	ix,#0
   5598 DD 39         [15]  127 	add	ix,sp
   559A 21 F1 FF      [10]  128 	ld	hl, #-15
   559D 39            [11]  129 	add	hl, sp
   559E F9            [ 6]  130 	ld	sp, hl
                            131 ;src/entities/enemy.c:23: if (!enemy) {
   559F DD 7E 05      [19]  132 	ld	a, 5 (ix)
   55A2 DD B6 04      [19]  133 	or	a,4 (ix)
                            134 ;src/entities/enemy.c:24: return;
   55A5 CA 71 57      [10]  135 	jp	Z,00112$
                            136 ;src/entities/enemy.c:27: enemy->x = x;
   55A8 DD 7E 04      [19]  137 	ld	a, 4 (ix)
   55AB DD 77 FE      [19]  138 	ld	-2 (ix), a
   55AE DD 7E 05      [19]  139 	ld	a, 5 (ix)
   55B1 DD 77 FF      [19]  140 	ld	-1 (ix), a
   55B4 DD 6E FE      [19]  141 	ld	l,-2 (ix)
   55B7 DD 66 FF      [19]  142 	ld	h,-1 (ix)
   55BA DD 7E 06      [19]  143 	ld	a, 6 (ix)
   55BD 77            [ 7]  144 	ld	(hl), a
                            145 ;src/entities/enemy.c:28: enemy->y = y;
   55BE DD 4E FE      [19]  146 	ld	c,-2 (ix)
   55C1 DD 46 FF      [19]  147 	ld	b,-1 (ix)
   55C4 03            [ 6]  148 	inc	bc
   55C5 DD 7E 07      [19]  149 	ld	a, 7 (ix)
   55C8 02            [ 7]  150 	ld	(bc), a
                            151 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   55C9 DD 7E FE      [19]  152 	ld	a, -2 (ix)
   55CC C6 02         [ 7]  153 	add	a, #0x02
   55CE DD 77 FC      [19]  154 	ld	-4 (ix), a
   55D1 DD 7E FF      [19]  155 	ld	a, -1 (ix)
   55D4 CE 00         [ 7]  156 	adc	a, #0x00
   55D6 DD 77 FD      [19]  157 	ld	-3 (ix), a
   55D9 DD 7E 09      [19]  158 	ld	a, 9 (ix)
   55DC B7            [ 4]  159 	or	a, a
   55DD 28 04         [12]  160 	jr	Z,00114$
   55DF 0E 01         [ 7]  161 	ld	c, #0x01
   55E1 18 02         [12]  162 	jr	00115$
   55E3                     163 00114$:
   55E3 0E FF         [ 7]  164 	ld	c, #0xff
   55E5                     165 00115$:
   55E5 DD 6E FC      [19]  166 	ld	l,-4 (ix)
   55E8 DD 66 FD      [19]  167 	ld	h,-3 (ix)
   55EB 71            [ 7]  168 	ld	(hl), c
                            169 ;src/entities/enemy.c:30: enemy->vy = 0;
   55EC DD 7E FE      [19]  170 	ld	a, -2 (ix)
   55EF C6 03         [ 7]  171 	add	a, #0x03
   55F1 DD 77 FA      [19]  172 	ld	-6 (ix), a
   55F4 DD 7E FF      [19]  173 	ld	a, -1 (ix)
   55F7 CE 00         [ 7]  174 	adc	a, #0x00
   55F9 DD 77 FB      [19]  175 	ld	-5 (ix), a
   55FC DD 6E FA      [19]  176 	ld	l,-6 (ix)
   55FF DD 66 FB      [19]  177 	ld	h,-5 (ix)
   5602 36 00         [10]  178 	ld	(hl), #0x00
                            179 ;src/entities/enemy.c:31: enemy->active = 1;
   5604 DD 7E FE      [19]  180 	ld	a, -2 (ix)
   5607 C6 06         [ 7]  181 	add	a, #0x06
   5609 DD 77 F8      [19]  182 	ld	-8 (ix), a
   560C DD 7E FF      [19]  183 	ld	a, -1 (ix)
   560F CE 00         [ 7]  184 	adc	a, #0x00
   5611 DD 77 F9      [19]  185 	ld	-7 (ix), a
   5614 DD 6E F8      [19]  186 	ld	l,-8 (ix)
   5617 DD 66 F9      [19]  187 	ld	h,-7 (ix)
   561A 36 01         [10]  188 	ld	(hl), #0x01
                            189 ;src/entities/enemy.c:32: enemy->kind = kind;
   561C DD 7E FE      [19]  190 	ld	a, -2 (ix)
   561F C6 0A         [ 7]  191 	add	a, #0x0a
   5621 DD 77 F8      [19]  192 	ld	-8 (ix), a
   5624 DD 7E FF      [19]  193 	ld	a, -1 (ix)
   5627 CE 00         [ 7]  194 	adc	a, #0x00
   5629 DD 77 F9      [19]  195 	ld	-7 (ix), a
   562C DD 6E F8      [19]  196 	ld	l,-8 (ix)
   562F DD 66 F9      [19]  197 	ld	h,-7 (ix)
   5632 DD 7E 08      [19]  198 	ld	a, 8 (ix)
   5635 77            [ 7]  199 	ld	(hl), a
                            200 ;src/entities/enemy.c:35: enemy->w = 5;
   5636 DD 7E FE      [19]  201 	ld	a, -2 (ix)
   5639 C6 04         [ 7]  202 	add	a, #0x04
   563B DD 77 F8      [19]  203 	ld	-8 (ix), a
   563E DD 7E FF      [19]  204 	ld	a, -1 (ix)
   5641 CE 00         [ 7]  205 	adc	a, #0x00
   5643 DD 77 F9      [19]  206 	ld	-7 (ix), a
                            207 ;src/entities/enemy.c:36: enemy->h = 14;
   5646 DD 7E FE      [19]  208 	ld	a, -2 (ix)
   5649 C6 05         [ 7]  209 	add	a, #0x05
   564B DD 77 F6      [19]  210 	ld	-10 (ix), a
   564E DD 7E FF      [19]  211 	ld	a, -1 (ix)
   5651 CE 00         [ 7]  212 	adc	a, #0x00
   5653 DD 77 F7      [19]  213 	ld	-9 (ix), a
                            214 ;src/entities/enemy.c:37: enemy->health = 2;
   5656 DD 7E FE      [19]  215 	ld	a, -2 (ix)
   5659 C6 07         [ 7]  216 	add	a, #0x07
   565B DD 77 F4      [19]  217 	ld	-12 (ix), a
   565E DD 7E FF      [19]  218 	ld	a, -1 (ix)
   5661 CE 00         [ 7]  219 	adc	a, #0x00
   5663 DD 77 F5      [19]  220 	ld	-11 (ix), a
                            221 ;src/entities/enemy.c:38: enemy->reward = 180;
   5666 DD 7E FE      [19]  222 	ld	a, -2 (ix)
   5669 C6 08         [ 7]  223 	add	a, #0x08
   566B DD 77 FE      [19]  224 	ld	-2 (ix), a
   566E DD 7E FF      [19]  225 	ld	a, -1 (ix)
   5671 CE 00         [ 7]  226 	adc	a, #0x00
   5673 DD 77 FF      [19]  227 	ld	-1 (ix), a
                            228 ;src/entities/enemy.c:34: if (kind == 1) {
   5676 DD 7E 08      [19]  229 	ld	a, 8 (ix)
   5679 3D            [ 4]  230 	dec	a
   567A 20 4C         [12]  231 	jr	NZ,00110$
                            232 ;src/entities/enemy.c:35: enemy->w = 5;
   567C DD 6E F8      [19]  233 	ld	l,-8 (ix)
   567F DD 66 F9      [19]  234 	ld	h,-7 (ix)
   5682 36 05         [10]  235 	ld	(hl), #0x05
                            236 ;src/entities/enemy.c:36: enemy->h = 14;
   5684 DD 6E F6      [19]  237 	ld	l,-10 (ix)
   5687 DD 66 F7      [19]  238 	ld	h,-9 (ix)
   568A 36 0E         [10]  239 	ld	(hl), #0x0e
                            240 ;src/entities/enemy.c:37: enemy->health = 2;
   568C DD 6E F4      [19]  241 	ld	l,-12 (ix)
   568F DD 66 F5      [19]  242 	ld	h,-11 (ix)
   5692 36 02         [10]  243 	ld	(hl), #0x02
                            244 ;src/entities/enemy.c:38: enemy->reward = 180;
   5694 DD 6E FE      [19]  245 	ld	l,-2 (ix)
   5697 DD 66 FF      [19]  246 	ld	h,-1 (ix)
   569A 36 B4         [10]  247 	ld	(hl), #0xb4
   569C 23            [ 6]  248 	inc	hl
   569D 36 00         [10]  249 	ld	(hl), #0x00
                            250 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   569F DD 7E FC      [19]  251 	ld	a, -4 (ix)
   56A2 DD 77 F2      [19]  252 	ld	-14 (ix), a
   56A5 DD 7E FD      [19]  253 	ld	a, -3 (ix)
   56A8 DD 77 F3      [19]  254 	ld	-13 (ix), a
   56AB DD 7E 09      [19]  255 	ld	a, 9 (ix)
   56AE B7            [ 4]  256 	or	a, a
   56AF 28 06         [12]  257 	jr	Z,00116$
   56B1 DD 36 F1 02   [19]  258 	ld	-15 (ix), #0x02
   56B5 18 04         [12]  259 	jr	00117$
   56B7                     260 00116$:
   56B7 DD 36 F1 FE   [19]  261 	ld	-15 (ix), #0xfe
   56BB                     262 00117$:
   56BB DD 6E F2      [19]  263 	ld	l,-14 (ix)
   56BE DD 66 F3      [19]  264 	ld	h,-13 (ix)
   56C1 DD 7E F1      [19]  265 	ld	a, -15 (ix)
   56C4 77            [ 7]  266 	ld	(hl), a
   56C5 C3 71 57      [10]  267 	jp	00112$
   56C8                     268 00110$:
                            269 ;src/entities/enemy.c:40: } else if (kind == 2) {
   56C8 DD 7E 08      [19]  270 	ld	a, 8 (ix)
   56CB D6 02         [ 7]  271 	sub	a, #0x02
   56CD 20 40         [12]  272 	jr	NZ,00107$
                            273 ;src/entities/enemy.c:41: enemy->w = 6;
   56CF DD 6E F8      [19]  274 	ld	l,-8 (ix)
   56D2 DD 66 F9      [19]  275 	ld	h,-7 (ix)
   56D5 36 06         [10]  276 	ld	(hl), #0x06
                            277 ;src/entities/enemy.c:42: enemy->h = 10;
   56D7 DD 6E F6      [19]  278 	ld	l,-10 (ix)
   56DA DD 66 F7      [19]  279 	ld	h,-9 (ix)
   56DD 36 0A         [10]  280 	ld	(hl), #0x0a
                            281 ;src/entities/enemy.c:43: enemy->health = 1;
   56DF DD 6E F4      [19]  282 	ld	l,-12 (ix)
   56E2 DD 66 F5      [19]  283 	ld	h,-11 (ix)
   56E5 36 01         [10]  284 	ld	(hl), #0x01
                            285 ;src/entities/enemy.c:44: enemy->reward = 150;
   56E7 DD 6E FE      [19]  286 	ld	l,-2 (ix)
   56EA DD 66 FF      [19]  287 	ld	h,-1 (ix)
   56ED 36 96         [10]  288 	ld	(hl), #0x96
   56EF 23            [ 6]  289 	inc	hl
   56F0 36 00         [10]  290 	ld	(hl), #0x00
                            291 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   56F2 DD 4E FA      [19]  292 	ld	c,-6 (ix)
   56F5 DD 46 FB      [19]  293 	ld	b,-5 (ix)
   56F8 DD 7E 09      [19]  294 	ld	a, 9 (ix)
   56FB B7            [ 4]  295 	or	a, a
   56FC 28 04         [12]  296 	jr	Z,00118$
   56FE 3E 01         [ 7]  297 	ld	a, #0x01
   5700 18 02         [12]  298 	jr	00119$
   5702                     299 00118$:
   5702 3E FF         [ 7]  300 	ld	a, #0xff
   5704                     301 00119$:
   5704 02            [ 7]  302 	ld	(bc), a
                            303 ;src/entities/enemy.c:46: enemy->vx = 1;
   5705 DD 6E FC      [19]  304 	ld	l,-4 (ix)
   5708 DD 66 FD      [19]  305 	ld	h,-3 (ix)
   570B 36 01         [10]  306 	ld	(hl), #0x01
   570D 18 62         [12]  307 	jr	00112$
   570F                     308 00107$:
                            309 ;src/entities/enemy.c:47: } else if (kind == 3) {
   570F DD 7E 08      [19]  310 	ld	a, 8 (ix)
   5712 D6 03         [ 7]  311 	sub	a, #0x03
   5714 20 38         [12]  312 	jr	NZ,00104$
                            313 ;src/entities/enemy.c:48: enemy->w = 10;
   5716 DD 6E F8      [19]  314 	ld	l,-8 (ix)
   5719 DD 66 F9      [19]  315 	ld	h,-7 (ix)
   571C 36 0A         [10]  316 	ld	(hl), #0x0a
                            317 ;src/entities/enemy.c:49: enemy->h = 18;
   571E DD 6E F6      [19]  318 	ld	l,-10 (ix)
   5721 DD 66 F7      [19]  319 	ld	h,-9 (ix)
   5724 36 12         [10]  320 	ld	(hl), #0x12
                            321 ;src/entities/enemy.c:50: enemy->health = 8;
   5726 DD 6E F4      [19]  322 	ld	l,-12 (ix)
   5729 DD 66 F5      [19]  323 	ld	h,-11 (ix)
   572C 36 08         [10]  324 	ld	(hl), #0x08
                            325 ;src/entities/enemy.c:51: enemy->reward = 800;
   572E DD 6E FE      [19]  326 	ld	l,-2 (ix)
   5731 DD 66 FF      [19]  327 	ld	h,-1 (ix)
   5734 36 20         [10]  328 	ld	(hl), #0x20
   5736 23            [ 6]  329 	inc	hl
   5737 36 03         [10]  330 	ld	(hl), #0x03
                            331 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   5739 DD 4E FC      [19]  332 	ld	c,-4 (ix)
   573C DD 46 FD      [19]  333 	ld	b,-3 (ix)
   573F DD 7E 09      [19]  334 	ld	a, 9 (ix)
   5742 B7            [ 4]  335 	or	a, a
   5743 28 04         [12]  336 	jr	Z,00120$
   5745 3E 01         [ 7]  337 	ld	a, #0x01
   5747 18 02         [12]  338 	jr	00121$
   5749                     339 00120$:
   5749 3E FF         [ 7]  340 	ld	a, #0xff
   574B                     341 00121$:
   574B 02            [ 7]  342 	ld	(bc), a
   574C 18 23         [12]  343 	jr	00112$
   574E                     344 00104$:
                            345 ;src/entities/enemy.c:54: enemy->w = 4;
   574E DD 6E F8      [19]  346 	ld	l,-8 (ix)
   5751 DD 66 F9      [19]  347 	ld	h,-7 (ix)
   5754 36 04         [10]  348 	ld	(hl), #0x04
                            349 ;src/entities/enemy.c:55: enemy->h = 16;
   5756 DD 6E F6      [19]  350 	ld	l,-10 (ix)
   5759 DD 66 F7      [19]  351 	ld	h,-9 (ix)
   575C 36 10         [10]  352 	ld	(hl), #0x10
                            353 ;src/entities/enemy.c:56: enemy->health = 1;
   575E DD 6E F4      [19]  354 	ld	l,-12 (ix)
   5761 DD 66 F5      [19]  355 	ld	h,-11 (ix)
   5764 36 01         [10]  356 	ld	(hl), #0x01
                            357 ;src/entities/enemy.c:57: enemy->reward = 100;
   5766 DD 6E FE      [19]  358 	ld	l,-2 (ix)
   5769 DD 66 FF      [19]  359 	ld	h,-1 (ix)
   576C 36 64         [10]  360 	ld	(hl), #0x64
   576E 23            [ 6]  361 	inc	hl
   576F 36 00         [10]  362 	ld	(hl), #0x00
   5771                     363 00112$:
   5771 DD F9         [10]  364 	ld	sp, ix
   5773 DD E1         [14]  365 	pop	ix
   5775 C9            [10]  366 	ret
                            367 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            368 ;	---------------------------------
                            369 ; Function enemyupdate
                            370 ; ---------------------------------
   5776                     371 _enemyupdate::
   5776 DD E5         [15]  372 	push	ix
   5778 DD 21 00 00   [14]  373 	ld	ix,#0
   577C DD 39         [15]  374 	add	ix,sp
   577E 21 F6 FF      [10]  375 	ld	hl, #-10
   5781 39            [11]  376 	add	hl, sp
   5782 F9            [ 6]  377 	ld	sp, hl
                            378 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   5783 DD 7E 05      [19]  379 	ld	a, 5 (ix)
   5786 DD B6 04      [19]  380 	or	a,4 (ix)
   5789 CA 7D 59      [10]  381 	jp	Z,00121$
   578C DD 7E 04      [19]  382 	ld	a, 4 (ix)
   578F DD 77 FE      [19]  383 	ld	-2 (ix), a
   5792 DD 7E 05      [19]  384 	ld	a, 5 (ix)
   5795 DD 77 FF      [19]  385 	ld	-1 (ix), a
   5798 DD 6E FE      [19]  386 	ld	l,-2 (ix)
   579B DD 66 FF      [19]  387 	ld	h,-1 (ix)
   579E 11 06 00      [10]  388 	ld	de, #0x0006
   57A1 19            [11]  389 	add	hl, de
   57A2 7E            [ 7]  390 	ld	a, (hl)
   57A3 B7            [ 4]  391 	or	a, a
                            392 ;src/entities/enemy.c:66: return;
   57A4 CA 7D 59      [10]  393 	jp	Z,00121$
                            394 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   57A7 DD 6E FE      [19]  395 	ld	l,-2 (ix)
   57AA DD 66 FF      [19]  396 	ld	h,-1 (ix)
   57AD 11 0A 00      [10]  397 	ld	de, #0x000a
   57B0 19            [11]  398 	add	hl, de
   57B1 7E            [ 7]  399 	ld	a, (hl)
   57B2 DD 77 FD      [19]  400 	ld	-3 (ix), a
                            401 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   57B5 DD 6E FE      [19]  402 	ld	l,-2 (ix)
   57B8 DD 66 FF      [19]  403 	ld	h,-1 (ix)
   57BB 4E            [ 7]  404 	ld	c, (hl)
   57BC DD 7E FE      [19]  405 	ld	a, -2 (ix)
   57BF C6 02         [ 7]  406 	add	a, #0x02
   57C1 DD 77 FB      [19]  407 	ld	-5 (ix), a
   57C4 DD 7E FF      [19]  408 	ld	a, -1 (ix)
   57C7 CE 00         [ 7]  409 	adc	a, #0x00
   57C9 DD 77 FC      [19]  410 	ld	-4 (ix), a
                            411 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   57CC DD 7E FE      [19]  412 	ld	a, -2 (ix)
   57CF C6 01         [ 7]  413 	add	a, #0x01
   57D1 DD 77 F9      [19]  414 	ld	-7 (ix), a
   57D4 DD 7E FF      [19]  415 	ld	a, -1 (ix)
   57D7 CE 00         [ 7]  416 	adc	a, #0x00
   57D9 DD 77 FA      [19]  417 	ld	-6 (ix), a
   57DC DD 5E FE      [19]  418 	ld	e,-2 (ix)
   57DF DD 56 FF      [19]  419 	ld	d,-1 (ix)
   57E2 13            [ 6]  420 	inc	de
   57E3 13            [ 6]  421 	inc	de
   57E4 13            [ 6]  422 	inc	de
                            423 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   57E5 06 00         [ 7]  424 	ld	b, #0x00
   57E7 DD 6E FB      [19]  425 	ld	l,-5 (ix)
   57EA DD 66 FC      [19]  426 	ld	h,-4 (ix)
   57ED 7E            [ 7]  427 	ld	a, (hl)
   57EE DD 77 F8      [19]  428 	ld	-8 (ix), a
   57F1 6F            [ 4]  429 	ld	l, a
   57F2 DD 7E F8      [19]  430 	ld	a, -8 (ix)
   57F5 17            [ 4]  431 	rla
   57F6 9F            [ 4]  432 	sbc	a, a
   57F7 67            [ 4]  433 	ld	h, a
   57F8 09            [11]  434 	add	hl,bc
   57F9 4D            [ 4]  435 	ld	c, l
   57FA 44            [ 4]  436 	ld	b, h
                            437 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   57FB DD 7E FD      [19]  438 	ld	a, -3 (ix)
   57FE D6 02         [ 7]  439 	sub	a, #0x02
   5800 C2 A9 58      [10]  440 	jp	NZ,00111$
                            441 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            442 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5803 DD 6E F9      [19]  443 	ld	l,-7 (ix)
   5806 DD 66 FA      [19]  444 	ld	h,-6 (ix)
   5809 6E            [ 7]  445 	ld	l, (hl)
   580A DD 75 F6      [19]  446 	ld	-10 (ix), l
   580D DD 36 F7 00   [19]  447 	ld	-9 (ix), #0x00
   5811 1A            [ 7]  448 	ld	a, (de)
   5812 6F            [ 4]  449 	ld	l, a
   5813 17            [ 4]  450 	rla
   5814 9F            [ 4]  451 	sbc	a, a
   5815 67            [ 4]  452 	ld	h, a
   5816 DD 7E F6      [19]  453 	ld	a, -10 (ix)
   5819 85            [ 4]  454 	add	a, l
   581A DD 77 F6      [19]  455 	ld	-10 (ix), a
   581D DD 7E F7      [19]  456 	ld	a, -9 (ix)
   5820 8C            [ 4]  457 	adc	a, h
   5821 DD 77 F7      [19]  458 	ld	-9 (ix), a
                            459 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   5824 79            [ 4]  460 	ld	a, c
   5825 D6 08         [ 7]  461 	sub	a, #0x08
   5827 78            [ 4]  462 	ld	a, b
   5828 17            [ 4]  463 	rla
   5829 3F            [ 4]  464 	ccf
   582A 1F            [ 4]  465 	rra
   582B DE 80         [ 7]  466 	sbc	a, #0x80
   582D 38 0E         [12]  467 	jr	C,00104$
   582F 3E 48         [ 7]  468 	ld	a, #0x48
   5831 B9            [ 4]  469 	cp	a, c
   5832 3E 00         [ 7]  470 	ld	a, #0x00
   5834 98            [ 4]  471 	sbc	a, b
   5835 E2 3A 58      [10]  472 	jp	PO, 00161$
   5838 EE 80         [ 7]  473 	xor	a, #0x80
   583A                     474 00161$:
   583A F2 58 58      [10]  475 	jp	P, 00105$
   583D                     476 00104$:
                            477 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   583D AF            [ 4]  478 	xor	a, a
   583E DD 96 F8      [19]  479 	sub	a, -8 (ix)
   5841 4F            [ 4]  480 	ld	c, a
   5842 DD 6E FB      [19]  481 	ld	l,-5 (ix)
   5845 DD 66 FC      [19]  482 	ld	h,-4 (ix)
   5848 71            [ 7]  483 	ld	(hl), c
                            484 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   5849 DD 6E FE      [19]  485 	ld	l,-2 (ix)
   584C DD 66 FF      [19]  486 	ld	h,-1 (ix)
   584F 6E            [ 7]  487 	ld	l, (hl)
   5850 26 00         [ 7]  488 	ld	h, #0x00
   5852 79            [ 4]  489 	ld	a, c
   5853 17            [ 4]  490 	rla
   5854 9F            [ 4]  491 	sbc	a, a
   5855 47            [ 4]  492 	ld	b, a
   5856 09            [11]  493 	add	hl,bc
   5857 4D            [ 4]  494 	ld	c, l
   5858                     495 00105$:
                            496 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   5858 DD 7E F6      [19]  497 	ld	a, -10 (ix)
   585B D6 38         [ 7]  498 	sub	a, #0x38
   585D DD 7E F7      [19]  499 	ld	a, -9 (ix)
   5860 17            [ 4]  500 	rla
   5861 3F            [ 4]  501 	ccf
   5862 1F            [ 4]  502 	rra
   5863 DE 80         [ 7]  503 	sbc	a, #0x80
   5865 38 12         [12]  504 	jr	C,00107$
   5867 3E 78         [ 7]  505 	ld	a, #0x78
   5869 DD BE F6      [19]  506 	cp	a, -10 (ix)
   586C 3E 00         [ 7]  507 	ld	a, #0x00
   586E DD 9E F7      [19]  508 	sbc	a, -9 (ix)
   5871 E2 76 58      [10]  509 	jp	PO, 00162$
   5874 EE 80         [ 7]  510 	xor	a, #0x80
   5876                     511 00162$:
   5876 F2 95 58      [10]  512 	jp	P, 00108$
   5879                     513 00107$:
                            514 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5879 1A            [ 7]  515 	ld	a, (de)
   587A 6F            [ 4]  516 	ld	l, a
   587B AF            [ 4]  517 	xor	a, a
   587C 95            [ 4]  518 	sub	a, l
   587D DD 77 F8      [19]  519 	ld	-8 (ix), a
   5880 12            [ 7]  520 	ld	(de),a
                            521 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   5881 DD 6E F9      [19]  522 	ld	l,-7 (ix)
   5884 DD 66 FA      [19]  523 	ld	h,-6 (ix)
   5887 5E            [ 7]  524 	ld	e, (hl)
   5888 16 00         [ 7]  525 	ld	d, #0x00
   588A DD 6E F8      [19]  526 	ld	l, -8 (ix)
   588D DD 7E F8      [19]  527 	ld	a, -8 (ix)
   5890 17            [ 4]  528 	rla
   5891 9F            [ 4]  529 	sbc	a, a
   5892 67            [ 4]  530 	ld	h, a
   5893 19            [11]  531 	add	hl,de
   5894 E3            [19]  532 	ex	(sp), hl
   5895                     533 00108$:
                            534 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   5895 DD 6E FE      [19]  535 	ld	l,-2 (ix)
   5898 DD 66 FF      [19]  536 	ld	h,-1 (ix)
   589B 71            [ 7]  537 	ld	(hl), c
                            538 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   589C DD 4E F6      [19]  539 	ld	c, -10 (ix)
   589F DD 6E F9      [19]  540 	ld	l,-7 (ix)
   58A2 DD 66 FA      [19]  541 	ld	h,-6 (ix)
   58A5 71            [ 7]  542 	ld	(hl), c
                            543 ;src/entities/enemy.c:84: return;
   58A6 C3 7D 59      [10]  544 	jp	00121$
   58A9                     545 00111$:
                            546 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            547 ;src/entities/enemy.c:88: if (nextx < 2) {
   58A9 79            [ 4]  548 	ld	a, c
   58AA D6 02         [ 7]  549 	sub	a, #0x02
   58AC 78            [ 4]  550 	ld	a, b
   58AD 17            [ 4]  551 	rla
   58AE 3F            [ 4]  552 	ccf
   58AF 1F            [ 4]  553 	rra
   58B0 DE 80         [ 7]  554 	sbc	a, #0x80
   58B2 30 0B         [12]  555 	jr	NC,00113$
                            556 ;src/entities/enemy.c:89: nextx = 2;
   58B4 01 02 00      [10]  557 	ld	bc, #0x0002
                            558 ;src/entities/enemy.c:90: enemy->vx = 1;
   58B7 DD 6E FB      [19]  559 	ld	l,-5 (ix)
   58BA DD 66 FC      [19]  560 	ld	h,-4 (ix)
   58BD 36 01         [10]  561 	ld	(hl), #0x01
   58BF                     562 00113$:
                            563 ;src/entities/enemy.c:93: i16 maxx = (i16)(80 - (i16)enemy->w);
   58BF DD 6E FE      [19]  564 	ld	l,-2 (ix)
   58C2 DD 66 FF      [19]  565 	ld	h,-1 (ix)
   58C5 23            [ 6]  566 	inc	hl
   58C6 23            [ 6]  567 	inc	hl
   58C7 23            [ 6]  568 	inc	hl
   58C8 23            [ 6]  569 	inc	hl
   58C9 6E            [ 7]  570 	ld	l, (hl)
   58CA 26 00         [ 7]  571 	ld	h, #0x00
   58CC 3E 50         [ 7]  572 	ld	a, #0x50
   58CE 95            [ 4]  573 	sub	a, l
   58CF 6F            [ 4]  574 	ld	l, a
   58D0 3E 00         [ 7]  575 	ld	a, #0x00
   58D2 9C            [ 4]  576 	sbc	a, h
   58D3 67            [ 4]  577 	ld	h, a
                            578 ;src/entities/enemy.c:94: if (nextx > maxx) {
   58D4 7D            [ 4]  579 	ld	a, l
   58D5 91            [ 4]  580 	sub	a, c
   58D6 7C            [ 4]  581 	ld	a, h
   58D7 98            [ 4]  582 	sbc	a, b
   58D8 E2 DD 58      [10]  583 	jp	PO, 00163$
   58DB EE 80         [ 7]  584 	xor	a, #0x80
   58DD                     585 00163$:
   58DD F2 E9 58      [10]  586 	jp	P, 00115$
                            587 ;src/entities/enemy.c:95: nextx = maxx;
   58E0 4D            [ 4]  588 	ld	c, l
                            589 ;src/entities/enemy.c:96: enemy->vx = -1;
   58E1 DD 6E FB      [19]  590 	ld	l,-5 (ix)
   58E4 DD 66 FC      [19]  591 	ld	h,-4 (ix)
   58E7 36 FF         [10]  592 	ld	(hl), #0xff
   58E9                     593 00115$:
                            594 ;src/entities/enemy.c:99: enemy->x = (u8)nextx;
   58E9 DD 6E FE      [19]  595 	ld	l,-2 (ix)
   58EC DD 66 FF      [19]  596 	ld	h,-1 (ix)
   58EF 71            [ 7]  597 	ld	(hl), c
                            598 ;src/entities/enemy.c:101: enemy->vy = (i8)(enemy->vy + 1);
   58F0 1A            [ 7]  599 	ld	a, (de)
   58F1 4F            [ 4]  600 	ld	c, a
   58F2 0C            [ 4]  601 	inc	c
   58F3 79            [ 4]  602 	ld	a, c
   58F4 12            [ 7]  603 	ld	(de), a
                            604 ;src/entities/enemy.c:102: if (enemy->vy > 3) enemy->vy = 3;
   58F5 3E 03         [ 7]  605 	ld	a, #0x03
   58F7 91            [ 4]  606 	sub	a, c
   58F8 E2 FD 58      [10]  607 	jp	PO, 00164$
   58FB EE 80         [ 7]  608 	xor	a, #0x80
   58FD                     609 00164$:
   58FD F2 03 59      [10]  610 	jp	P, 00117$
   5900 3E 03         [ 7]  611 	ld	a, #0x03
   5902 12            [ 7]  612 	ld	(de), a
   5903                     613 00117$:
                            614 ;src/entities/enemy.c:103: nexty = (i16)enemy->y + (i16)enemy->vy;
   5903 DD 6E F9      [19]  615 	ld	l,-7 (ix)
   5906 DD 66 FA      [19]  616 	ld	h,-6 (ix)
   5909 4E            [ 7]  617 	ld	c, (hl)
   590A 06 00         [ 7]  618 	ld	b, #0x00
   590C 1A            [ 7]  619 	ld	a, (de)
   590D 6F            [ 4]  620 	ld	l, a
   590E 17            [ 4]  621 	rla
   590F 9F            [ 4]  622 	sbc	a, a
   5910 67            [ 4]  623 	ld	h, a
   5911 09            [11]  624 	add	hl, bc
   5912 E5            [11]  625 	push	hl
   5913 FD E1         [14]  626 	pop	iy
                            627 ;src/entities/enemy.c:104: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5915 DD 7E FE      [19]  628 	ld	a, -2 (ix)
   5918 C6 05         [ 7]  629 	add	a, #0x05
   591A DD 77 F6      [19]  630 	ld	-10 (ix), a
   591D DD 7E FF      [19]  631 	ld	a, -1 (ix)
   5920 CE 00         [ 7]  632 	adc	a, #0x00
   5922 DD 77 F7      [19]  633 	ld	-9 (ix), a
   5925 E1            [10]  634 	pop	hl
   5926 E5            [11]  635 	push	hl
   5927 7E            [ 7]  636 	ld	a, (hl)
   5928 DD 6E FE      [19]  637 	ld	l,-2 (ix)
   592B DD 66 FF      [19]  638 	ld	h,-1 (ix)
   592E 4E            [ 7]  639 	ld	c, (hl)
   592F 06 00         [ 7]  640 	ld	b, #0x00
   5931 D5            [11]  641 	push	de
   5932 F5            [11]  642 	push	af
   5933 33            [ 6]  643 	inc	sp
   5934 FD E5         [15]  644 	push	iy
   5936 C5            [11]  645 	push	bc
   5937 CD 46 4C      [17]  646 	call	_collision_clamp_y_at
   593A F1            [10]  647 	pop	af
   593B F1            [10]  648 	pop	af
   593C 33            [ 6]  649 	inc	sp
   593D 4D            [ 4]  650 	ld	c, l
   593E D1            [10]  651 	pop	de
                            652 ;src/entities/enemy.c:105: enemy->y = (u8)nexty;
   593F DD 6E F9      [19]  653 	ld	l,-7 (ix)
   5942 DD 66 FA      [19]  654 	ld	h,-6 (ix)
   5945 71            [ 7]  655 	ld	(hl), c
                            656 ;src/entities/enemy.c:106: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5946 E1            [10]  657 	pop	hl
   5947 E5            [11]  658 	push	hl
   5948 7E            [ 7]  659 	ld	a, (hl)
   5949 06 00         [ 7]  660 	ld	b, #0x00
   594B DD 6E FE      [19]  661 	ld	l,-2 (ix)
   594E DD 66 FF      [19]  662 	ld	h,-1 (ix)
   5951 6E            [ 7]  663 	ld	l, (hl)
   5952 DD 75 F6      [19]  664 	ld	-10 (ix), l
   5955 DD 36 F7 00   [19]  665 	ld	-9 (ix), #0x00
   5959 D5            [11]  666 	push	de
   595A F5            [11]  667 	push	af
   595B 33            [ 6]  668 	inc	sp
   595C C5            [11]  669 	push	bc
   595D DD 6E F6      [19]  670 	ld	l,-10 (ix)
   5960 DD 66 F7      [19]  671 	ld	h,-9 (ix)
   5963 E5            [11]  672 	push	hl
   5964 CD C7 4B      [17]  673 	call	_collision_is_on_ground_at
   5967 F1            [10]  674 	pop	af
   5968 F1            [10]  675 	pop	af
   5969 33            [ 6]  676 	inc	sp
   596A D1            [10]  677 	pop	de
   596B 7D            [ 4]  678 	ld	a, l
   596C B7            [ 4]  679 	or	a, a
   596D 28 0E         [12]  680 	jr	Z,00121$
   596F 1A            [ 7]  681 	ld	a, (de)
   5970 4F            [ 4]  682 	ld	c, a
   5971 AF            [ 4]  683 	xor	a, a
   5972 91            [ 4]  684 	sub	a, c
   5973 E2 78 59      [10]  685 	jp	PO, 00165$
   5976 EE 80         [ 7]  686 	xor	a, #0x80
   5978                     687 00165$:
   5978 F2 7D 59      [10]  688 	jp	P, 00121$
                            689 ;src/entities/enemy.c:107: enemy->vy = 0;
   597B AF            [ 4]  690 	xor	a, a
   597C 12            [ 7]  691 	ld	(de), a
   597D                     692 00121$:
   597D DD F9         [10]  693 	ld	sp, ix
   597F DD E1         [14]  694 	pop	ix
   5981 C9            [10]  695 	ret
                            696 ;src/entities/enemy.c:111: void enemyrender(const Enemy* enemy) {
                            697 ;	---------------------------------
                            698 ; Function enemyrender
                            699 ; ---------------------------------
   5982                     700 _enemyrender::
   5982 DD E5         [15]  701 	push	ix
   5984 DD 21 00 00   [14]  702 	ld	ix,#0
   5988 DD 39         [15]  703 	add	ix,sp
   598A F5            [11]  704 	push	af
                            705 ;src/entities/enemy.c:115: if (!enemy || !enemy->active) {
   598B DD 7E 05      [19]  706 	ld	a, 5 (ix)
   598E DD B6 04      [19]  707 	or	a,4 (ix)
   5991 CA 0F 5A      [10]  708 	jp	Z,00113$
   5994 DD 7E 04      [19]  709 	ld	a, 4 (ix)
   5997 DD 77 FE      [19]  710 	ld	-2 (ix), a
   599A DD 7E 05      [19]  711 	ld	a, 5 (ix)
   599D DD 77 FF      [19]  712 	ld	-1 (ix), a
   59A0 E1            [10]  713 	pop	hl
   59A1 E5            [11]  714 	push	hl
   59A2 11 06 00      [10]  715 	ld	de, #0x0006
   59A5 19            [11]  716 	add	hl, de
   59A6 7E            [ 7]  717 	ld	a, (hl)
   59A7 B7            [ 4]  718 	or	a, a
                            719 ;src/entities/enemy.c:116: return;
   59A8 28 65         [12]  720 	jr	Z,00113$
                            721 ;src/entities/enemy.c:119: if (enemy->kind == 3) colour = cpct_px2byteM0(12, 12);
   59AA E1            [10]  722 	pop	hl
   59AB E5            [11]  723 	push	hl
   59AC 11 0A 00      [10]  724 	ld	de, #0x000a
   59AF 19            [11]  725 	add	hl, de
   59B0 7E            [ 7]  726 	ld	a, (hl)
   59B1 FE 03         [ 7]  727 	cp	a, #0x03
   59B3 20 0A         [12]  728 	jr	NZ,00111$
   59B5 21 0C 0C      [10]  729 	ld	hl, #0x0c0c
   59B8 E5            [11]  730 	push	hl
   59B9 CD D8 60      [17]  731 	call	_cpct_px2byteM0
   59BC 4D            [ 4]  732 	ld	c, l
   59BD 18 23         [12]  733 	jr	00112$
   59BF                     734 00111$:
                            735 ;src/entities/enemy.c:120: else if (enemy->kind == 2) colour = cpct_px2byteM0(10, 10);
   59BF FE 02         [ 7]  736 	cp	a, #0x02
   59C1 20 0A         [12]  737 	jr	NZ,00108$
   59C3 21 0A 0A      [10]  738 	ld	hl, #0x0a0a
   59C6 E5            [11]  739 	push	hl
   59C7 CD D8 60      [17]  740 	call	_cpct_px2byteM0
   59CA 4D            [ 4]  741 	ld	c, l
   59CB 18 15         [12]  742 	jr	00112$
   59CD                     743 00108$:
                            744 ;src/entities/enemy.c:121: else if (enemy->kind == 1) colour = cpct_px2byteM0(14, 14);
   59CD 3D            [ 4]  745 	dec	a
   59CE 20 0A         [12]  746 	jr	NZ,00105$
   59D0 21 0E 0E      [10]  747 	ld	hl, #0x0e0e
   59D3 E5            [11]  748 	push	hl
   59D4 CD D8 60      [17]  749 	call	_cpct_px2byteM0
   59D7 4D            [ 4]  750 	ld	c, l
   59D8 18 08         [12]  751 	jr	00112$
   59DA                     752 00105$:
                            753 ;src/entities/enemy.c:122: else colour = cpct_px2byteM0(4, 4);
   59DA 21 04 04      [10]  754 	ld	hl, #0x0404
   59DD E5            [11]  755 	push	hl
   59DE CD D8 60      [17]  756 	call	_cpct_px2byteM0
   59E1 4D            [ 4]  757 	ld	c, l
   59E2                     758 00112$:
                            759 ;src/entities/enemy.c:124: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   59E2 E1            [10]  760 	pop	hl
   59E3 E5            [11]  761 	push	hl
   59E4 23            [ 6]  762 	inc	hl
   59E5 46            [ 7]  763 	ld	b, (hl)
   59E6 E1            [10]  764 	pop	hl
   59E7 E5            [11]  765 	push	hl
   59E8 56            [ 7]  766 	ld	d, (hl)
   59E9 C5            [11]  767 	push	bc
   59EA 4A            [ 4]  768 	ld	c, d
   59EB C5            [11]  769 	push	bc
   59EC 21 00 C0      [10]  770 	ld	hl, #0xc000
   59EF E5            [11]  771 	push	hl
   59F0 CD CB 61      [17]  772 	call	_cpct_getScreenPtr
   59F3 EB            [ 4]  773 	ex	de,hl
   59F4 C1            [10]  774 	pop	bc
                            775 ;src/entities/enemy.c:125: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   59F5 E1            [10]  776 	pop	hl
   59F6 E5            [11]  777 	push	hl
   59F7 23            [ 6]  778 	inc	hl
   59F8 23            [ 6]  779 	inc	hl
   59F9 23            [ 6]  780 	inc	hl
   59FA 23            [ 6]  781 	inc	hl
   59FB 23            [ 6]  782 	inc	hl
   59FC 46            [ 7]  783 	ld	b, (hl)
   59FD E1            [10]  784 	pop	hl
   59FE E5            [11]  785 	push	hl
   59FF 23            [ 6]  786 	inc	hl
   5A00 23            [ 6]  787 	inc	hl
   5A01 23            [ 6]  788 	inc	hl
   5A02 23            [ 6]  789 	inc	hl
   5A03 7E            [ 7]  790 	ld	a, (hl)
   5A04 C5            [11]  791 	push	bc
   5A05 33            [ 6]  792 	inc	sp
   5A06 47            [ 4]  793 	ld	b, a
   5A07 C5            [11]  794 	push	bc
   5A08 D5            [11]  795 	push	de
   5A09 CD 12 61      [17]  796 	call	_cpct_drawSolidBox
   5A0C F1            [10]  797 	pop	af
   5A0D F1            [10]  798 	pop	af
   5A0E 33            [ 6]  799 	inc	sp
   5A0F                     800 00113$:
   5A0F DD F9         [10]  801 	ld	sp, ix
   5A11 DD E1         [14]  802 	pop	ix
   5A13 C9            [10]  803 	ret
                            804 ;src/entities/enemy.c:128: u8 enemydamage(Enemy* enemy, u8 damage) {
                            805 ;	---------------------------------
                            806 ; Function enemydamage
                            807 ; ---------------------------------
   5A14                     808 _enemydamage::
   5A14 DD E5         [15]  809 	push	ix
   5A16 DD 21 00 00   [14]  810 	ld	ix,#0
   5A1A DD 39         [15]  811 	add	ix,sp
                            812 ;src/entities/enemy.c:129: if (!enemy || !enemy->active) {
   5A1C DD 7E 05      [19]  813 	ld	a, 5 (ix)
   5A1F DD B6 04      [19]  814 	or	a,4 (ix)
   5A22 28 0F         [12]  815 	jr	Z,00101$
   5A24 DD 4E 04      [19]  816 	ld	c,4 (ix)
   5A27 DD 46 05      [19]  817 	ld	b,5 (ix)
   5A2A 21 06 00      [10]  818 	ld	hl, #0x0006
   5A2D 09            [11]  819 	add	hl,bc
   5A2E EB            [ 4]  820 	ex	de,hl
   5A2F 1A            [ 7]  821 	ld	a, (de)
   5A30 B7            [ 4]  822 	or	a, a
   5A31 20 04         [12]  823 	jr	NZ,00102$
   5A33                     824 00101$:
                            825 ;src/entities/enemy.c:130: return 0;
   5A33 2E 00         [ 7]  826 	ld	l, #0x00
   5A35 18 1A         [12]  827 	jr	00106$
   5A37                     828 00102$:
                            829 ;src/entities/enemy.c:133: if (damage >= enemy->health) {
   5A37 21 07 00      [10]  830 	ld	hl, #0x0007
   5A3A 09            [11]  831 	add	hl, bc
   5A3B 4E            [ 7]  832 	ld	c, (hl)
   5A3C DD 7E 06      [19]  833 	ld	a, 6 (ix)
   5A3F 91            [ 4]  834 	sub	a, c
   5A40 38 08         [12]  835 	jr	C,00105$
                            836 ;src/entities/enemy.c:134: enemy->health = 0;
   5A42 36 00         [10]  837 	ld	(hl), #0x00
                            838 ;src/entities/enemy.c:135: enemy->active = 0;
   5A44 AF            [ 4]  839 	xor	a, a
   5A45 12            [ 7]  840 	ld	(de), a
                            841 ;src/entities/enemy.c:136: return 1;
   5A46 2E 01         [ 7]  842 	ld	l, #0x01
   5A48 18 07         [12]  843 	jr	00106$
   5A4A                     844 00105$:
                            845 ;src/entities/enemy.c:139: enemy->health = (u8)(enemy->health - damage);
   5A4A 79            [ 4]  846 	ld	a, c
   5A4B DD 96 06      [19]  847 	sub	a, 6 (ix)
   5A4E 77            [ 7]  848 	ld	(hl), a
                            849 ;src/entities/enemy.c:140: return 0;
   5A4F 2E 00         [ 7]  850 	ld	l, #0x00
   5A51                     851 00106$:
   5A51 DD E1         [14]  852 	pop	ix
   5A53 C9            [10]  853 	ret
                            854 	.area _CODE
                            855 	.area _INITIALIZER
                            856 	.area _CABS (ABS)
