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
                             14 	.globl _cpct_drawSprite
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
                             51 ;src/entities/enemy.c:65: void enemyinit(Enemy* enemy) {
                             52 ;	---------------------------------
                             53 ; Function enemyinit
                             54 ; ---------------------------------
   5527                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   5527 21 03 00      [10]   57 	ld	hl, #2+1
   552A 39            [11]   58 	add	hl, sp
   552B 7E            [ 7]   59 	ld	a, (hl)
   552C 2B            [ 6]   60 	dec	hl
   552D B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   552E C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   552F D1            [10]   65 	pop	de
   5530 C1            [10]   66 	pop	bc
   5531 C5            [11]   67 	push	bc
   5532 D5            [11]   68 	push	de
   5533 AF            [ 4]   69 	xor	a, a
   5534 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   5535 59            [ 4]   72 	ld	e, c
   5536 50            [ 4]   73 	ld	d, b
   5537 13            [ 6]   74 	inc	de
   5538 AF            [ 4]   75 	xor	a, a
   5539 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   553A 59            [ 4]   78 	ld	e, c
   553B 50            [ 4]   79 	ld	d, b
   553C 13            [ 6]   80 	inc	de
   553D 13            [ 6]   81 	inc	de
   553E AF            [ 4]   82 	xor	a, a
   553F 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   5540 59            [ 4]   85 	ld	e, c
   5541 50            [ 4]   86 	ld	d, b
   5542 13            [ 6]   87 	inc	de
   5543 13            [ 6]   88 	inc	de
   5544 13            [ 6]   89 	inc	de
   5545 AF            [ 4]   90 	xor	a, a
   5546 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   5547 21 04 00      [10]   93 	ld	hl, #0x0004
   554A 09            [11]   94 	add	hl, bc
   554B 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   554D 21 05 00      [10]   97 	ld	hl, #0x0005
   5550 09            [11]   98 	add	hl, bc
   5551 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   5553 21 06 00      [10]  101 	ld	hl, #0x0006
   5556 09            [11]  102 	add	hl, bc
   5557 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   5559 21 07 00      [10]  105 	ld	hl, #0x0007
   555C 09            [11]  106 	add	hl, bc
   555D 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   555F 21 08 00      [10]  109 	ld	hl, #0x0008
   5562 09            [11]  110 	add	hl, bc
   5563 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   5565 21 09 00      [10]  113 	ld	hl, #0x0009
   5568 09            [11]  114 	add	hl, bc
   5569 36 00         [10]  115 	ld	(hl), #0x00
   556B C9            [10]  116 	ret
   556C                     117 _enemy_kind0_sprite:
   556C 30                  118 	.db #0x30	; 48	'0'
   556D 30                  119 	.db #0x30	; 48	'0'
   556E 30                  120 	.db #0x30	; 48	'0'
   556F 30                  121 	.db #0x30	; 48	'0'
   5570 30                  122 	.db #0x30	; 48	'0'
   5571 00                  123 	.db #0x00	; 0
   5572 00                  124 	.db #0x00	; 0
   5573 10                  125 	.db #0x10	; 16
   5574 30                  126 	.db #0x30	; 48	'0'
   5575 00                  127 	.db #0x00	; 0
   5576 00                  128 	.db #0x00	; 0
   5577 10                  129 	.db #0x10	; 16
   5578 30                  130 	.db #0x30	; 48	'0'
   5579 00                  131 	.db #0x00	; 0
   557A 00                  132 	.db #0x00	; 0
   557B 10                  133 	.db #0x10	; 16
   557C 30                  134 	.db #0x30	; 48	'0'
   557D 00                  135 	.db #0x00	; 0
   557E 00                  136 	.db #0x00	; 0
   557F 10                  137 	.db #0x10	; 16
   5580 30                  138 	.db #0x30	; 48	'0'
   5581 00                  139 	.db #0x00	; 0
   5582 00                  140 	.db #0x00	; 0
   5583 10                  141 	.db #0x10	; 16
   5584 30                  142 	.db #0x30	; 48	'0'
   5585 00                  143 	.db #0x00	; 0
   5586 00                  144 	.db #0x00	; 0
   5587 10                  145 	.db #0x10	; 16
   5588 30                  146 	.db #0x30	; 48	'0'
   5589 00                  147 	.db #0x00	; 0
   558A 00                  148 	.db #0x00	; 0
   558B 10                  149 	.db #0x10	; 16
   558C 30                  150 	.db #0x30	; 48	'0'
   558D 30                  151 	.db #0x30	; 48	'0'
   558E 30                  152 	.db #0x30	; 48	'0'
   558F 30                  153 	.db #0x30	; 48	'0'
   5590 30                  154 	.db #0x30	; 48	'0'
   5591 00                  155 	.db #0x00	; 0
   5592 00                  156 	.db #0x00	; 0
   5593 10                  157 	.db #0x10	; 16
   5594 30                  158 	.db #0x30	; 48	'0'
   5595 00                  159 	.db #0x00	; 0
   5596 00                  160 	.db #0x00	; 0
   5597 10                  161 	.db #0x10	; 16
   5598 30                  162 	.db #0x30	; 48	'0'
   5599 00                  163 	.db #0x00	; 0
   559A 00                  164 	.db #0x00	; 0
   559B 10                  165 	.db #0x10	; 16
   559C 30                  166 	.db #0x30	; 48	'0'
   559D 00                  167 	.db #0x00	; 0
   559E 00                  168 	.db #0x00	; 0
   559F 10                  169 	.db #0x10	; 16
   55A0 30                  170 	.db #0x30	; 48	'0'
   55A1 00                  171 	.db #0x00	; 0
   55A2 00                  172 	.db #0x00	; 0
   55A3 10                  173 	.db #0x10	; 16
   55A4 30                  174 	.db #0x30	; 48	'0'
   55A5 00                  175 	.db #0x00	; 0
   55A6 00                  176 	.db #0x00	; 0
   55A7 10                  177 	.db #0x10	; 16
   55A8 30                  178 	.db #0x30	; 48	'0'
   55A9 30                  179 	.db #0x30	; 48	'0'
   55AA 30                  180 	.db #0x30	; 48	'0'
   55AB 30                  181 	.db #0x30	; 48	'0'
   55AC                     182 _enemy_kind1_sprite:
   55AC 3F                  183 	.db #0x3f	; 63
   55AD 3F                  184 	.db #0x3f	; 63
   55AE 3F                  185 	.db #0x3f	; 63
   55AF 3F                  186 	.db #0x3f	; 63
   55B0 3F                  187 	.db #0x3f	; 63
   55B1 2A                  188 	.db #0x2a	; 42
   55B2 2A                  189 	.db #0x2a	; 42
   55B3 00                  190 	.db #0x00	; 0
   55B4 00                  191 	.db #0x00	; 0
   55B5 15                  192 	.db #0x15	; 21
   55B6 2A                  193 	.db #0x2a	; 42
   55B7 2A                  194 	.db #0x2a	; 42
   55B8 00                  195 	.db #0x00	; 0
   55B9 00                  196 	.db #0x00	; 0
   55BA 15                  197 	.db #0x15	; 21
   55BB 2A                  198 	.db #0x2a	; 42
   55BC 2A                  199 	.db #0x2a	; 42
   55BD 00                  200 	.db #0x00	; 0
   55BE 00                  201 	.db #0x00	; 0
   55BF 15                  202 	.db #0x15	; 21
   55C0 2A                  203 	.db #0x2a	; 42
   55C1 2A                  204 	.db #0x2a	; 42
   55C2 00                  205 	.db #0x00	; 0
   55C3 00                  206 	.db #0x00	; 0
   55C4 15                  207 	.db #0x15	; 21
   55C5 2A                  208 	.db #0x2a	; 42
   55C6 2A                  209 	.db #0x2a	; 42
   55C7 00                  210 	.db #0x00	; 0
   55C8 00                  211 	.db #0x00	; 0
   55C9 15                  212 	.db #0x15	; 21
   55CA 2A                  213 	.db #0x2a	; 42
   55CB 2A                  214 	.db #0x2a	; 42
   55CC 00                  215 	.db #0x00	; 0
   55CD 00                  216 	.db #0x00	; 0
   55CE 15                  217 	.db #0x15	; 21
   55CF 3F                  218 	.db #0x3f	; 63
   55D0 3F                  219 	.db #0x3f	; 63
   55D1 3F                  220 	.db #0x3f	; 63
   55D2 3F                  221 	.db #0x3f	; 63
   55D3 3F                  222 	.db #0x3f	; 63
   55D4 2A                  223 	.db #0x2a	; 42
   55D5 2A                  224 	.db #0x2a	; 42
   55D6 00                  225 	.db #0x00	; 0
   55D7 00                  226 	.db #0x00	; 0
   55D8 15                  227 	.db #0x15	; 21
   55D9 2A                  228 	.db #0x2a	; 42
   55DA 2A                  229 	.db #0x2a	; 42
   55DB 00                  230 	.db #0x00	; 0
   55DC 00                  231 	.db #0x00	; 0
   55DD 15                  232 	.db #0x15	; 21
   55DE 2A                  233 	.db #0x2a	; 42
   55DF 2A                  234 	.db #0x2a	; 42
   55E0 00                  235 	.db #0x00	; 0
   55E1 00                  236 	.db #0x00	; 0
   55E2 15                  237 	.db #0x15	; 21
   55E3 2A                  238 	.db #0x2a	; 42
   55E4 2A                  239 	.db #0x2a	; 42
   55E5 00                  240 	.db #0x00	; 0
   55E6 00                  241 	.db #0x00	; 0
   55E7 15                  242 	.db #0x15	; 21
   55E8 2A                  243 	.db #0x2a	; 42
   55E9 2A                  244 	.db #0x2a	; 42
   55EA 00                  245 	.db #0x00	; 0
   55EB 00                  246 	.db #0x00	; 0
   55EC 15                  247 	.db #0x15	; 21
   55ED 3F                  248 	.db #0x3f	; 63
   55EE 3F                  249 	.db #0x3f	; 63
   55EF 3F                  250 	.db #0x3f	; 63
   55F0 3F                  251 	.db #0x3f	; 63
   55F1 3F                  252 	.db #0x3f	; 63
   55F2                     253 _enemy_kind2_sprite:
   55F2 0F                  254 	.db #0x0f	; 15
   55F3 0F                  255 	.db #0x0f	; 15
   55F4 0F                  256 	.db #0x0f	; 15
   55F5 0F                  257 	.db #0x0f	; 15
   55F6 0F                  258 	.db #0x0f	; 15
   55F7 0F                  259 	.db #0x0f	; 15
   55F8 0A                  260 	.db #0x0a	; 10
   55F9 05                  261 	.db #0x05	; 5
   55FA 00                  262 	.db #0x00	; 0
   55FB 00                  263 	.db #0x00	; 0
   55FC 00                  264 	.db #0x00	; 0
   55FD 05                  265 	.db #0x05	; 5
   55FE 0A                  266 	.db #0x0a	; 10
   55FF 05                  267 	.db #0x05	; 5
   5600 00                  268 	.db #0x00	; 0
   5601 00                  269 	.db #0x00	; 0
   5602 00                  270 	.db #0x00	; 0
   5603 05                  271 	.db #0x05	; 5
   5604 0A                  272 	.db #0x0a	; 10
   5605 05                  273 	.db #0x05	; 5
   5606 00                  274 	.db #0x00	; 0
   5607 00                  275 	.db #0x00	; 0
   5608 00                  276 	.db #0x00	; 0
   5609 05                  277 	.db #0x05	; 5
   560A 0A                  278 	.db #0x0a	; 10
   560B 05                  279 	.db #0x05	; 5
   560C 00                  280 	.db #0x00	; 0
   560D 00                  281 	.db #0x00	; 0
   560E 00                  282 	.db #0x00	; 0
   560F 05                  283 	.db #0x05	; 5
   5610 0F                  284 	.db #0x0f	; 15
   5611 0F                  285 	.db #0x0f	; 15
   5612 0F                  286 	.db #0x0f	; 15
   5613 0F                  287 	.db #0x0f	; 15
   5614 0F                  288 	.db #0x0f	; 15
   5615 0F                  289 	.db #0x0f	; 15
   5616 0A                  290 	.db #0x0a	; 10
   5617 05                  291 	.db #0x05	; 5
   5618 00                  292 	.db #0x00	; 0
   5619 00                  293 	.db #0x00	; 0
   561A 00                  294 	.db #0x00	; 0
   561B 05                  295 	.db #0x05	; 5
   561C 0A                  296 	.db #0x0a	; 10
   561D 05                  297 	.db #0x05	; 5
   561E 00                  298 	.db #0x00	; 0
   561F 00                  299 	.db #0x00	; 0
   5620 00                  300 	.db #0x00	; 0
   5621 05                  301 	.db #0x05	; 5
   5622 0A                  302 	.db #0x0a	; 10
   5623 05                  303 	.db #0x05	; 5
   5624 00                  304 	.db #0x00	; 0
   5625 00                  305 	.db #0x00	; 0
   5626 00                  306 	.db #0x00	; 0
   5627 05                  307 	.db #0x05	; 5
   5628 0F                  308 	.db #0x0f	; 15
   5629 0F                  309 	.db #0x0f	; 15
   562A 0F                  310 	.db #0x0f	; 15
   562B 0F                  311 	.db #0x0f	; 15
   562C 0F                  312 	.db #0x0f	; 15
   562D 0F                  313 	.db #0x0f	; 15
   562E                     314 _enemy_kind3_sprite:
   562E 33                  315 	.db #0x33	; 51	'3'
   562F 33                  316 	.db #0x33	; 51	'3'
   5630 33                  317 	.db #0x33	; 51	'3'
   5631 33                  318 	.db #0x33	; 51	'3'
   5632 33                  319 	.db #0x33	; 51	'3'
   5633 33                  320 	.db #0x33	; 51	'3'
   5634 33                  321 	.db #0x33	; 51	'3'
   5635 33                  322 	.db #0x33	; 51	'3'
   5636 33                  323 	.db #0x33	; 51	'3'
   5637 33                  324 	.db #0x33	; 51	'3'
   5638 22                  325 	.db #0x22	; 34
   5639 00                  326 	.db #0x00	; 0
   563A 22                  327 	.db #0x22	; 34
   563B 00                  328 	.db #0x00	; 0
   563C 00                  329 	.db #0x00	; 0
   563D 00                  330 	.db #0x00	; 0
   563E 00                  331 	.db #0x00	; 0
   563F 00                  332 	.db #0x00	; 0
   5640 00                  333 	.db #0x00	; 0
   5641 11                  334 	.db #0x11	; 17
   5642 22                  335 	.db #0x22	; 34
   5643 00                  336 	.db #0x00	; 0
   5644 22                  337 	.db #0x22	; 34
   5645 00                  338 	.db #0x00	; 0
   5646 00                  339 	.db #0x00	; 0
   5647 00                  340 	.db #0x00	; 0
   5648 00                  341 	.db #0x00	; 0
   5649 00                  342 	.db #0x00	; 0
   564A 00                  343 	.db #0x00	; 0
   564B 11                  344 	.db #0x11	; 17
   564C 22                  345 	.db #0x22	; 34
   564D 00                  346 	.db #0x00	; 0
   564E 22                  347 	.db #0x22	; 34
   564F 00                  348 	.db #0x00	; 0
   5650 00                  349 	.db #0x00	; 0
   5651 00                  350 	.db #0x00	; 0
   5652 00                  351 	.db #0x00	; 0
   5653 00                  352 	.db #0x00	; 0
   5654 00                  353 	.db #0x00	; 0
   5655 11                  354 	.db #0x11	; 17
   5656 22                  355 	.db #0x22	; 34
   5657 00                  356 	.db #0x00	; 0
   5658 22                  357 	.db #0x22	; 34
   5659 00                  358 	.db #0x00	; 0
   565A 00                  359 	.db #0x00	; 0
   565B 00                  360 	.db #0x00	; 0
   565C 00                  361 	.db #0x00	; 0
   565D 00                  362 	.db #0x00	; 0
   565E 00                  363 	.db #0x00	; 0
   565F 11                  364 	.db #0x11	; 17
   5660 22                  365 	.db #0x22	; 34
   5661 00                  366 	.db #0x00	; 0
   5662 22                  367 	.db #0x22	; 34
   5663 00                  368 	.db #0x00	; 0
   5664 00                  369 	.db #0x00	; 0
   5665 00                  370 	.db #0x00	; 0
   5666 00                  371 	.db #0x00	; 0
   5667 00                  372 	.db #0x00	; 0
   5668 00                  373 	.db #0x00	; 0
   5669 11                  374 	.db #0x11	; 17
   566A 22                  375 	.db #0x22	; 34
   566B 00                  376 	.db #0x00	; 0
   566C 22                  377 	.db #0x22	; 34
   566D 00                  378 	.db #0x00	; 0
   566E 00                  379 	.db #0x00	; 0
   566F 00                  380 	.db #0x00	; 0
   5670 00                  381 	.db #0x00	; 0
   5671 00                  382 	.db #0x00	; 0
   5672 00                  383 	.db #0x00	; 0
   5673 11                  384 	.db #0x11	; 17
   5674 22                  385 	.db #0x22	; 34
   5675 00                  386 	.db #0x00	; 0
   5676 22                  387 	.db #0x22	; 34
   5677 00                  388 	.db #0x00	; 0
   5678 00                  389 	.db #0x00	; 0
   5679 00                  390 	.db #0x00	; 0
   567A 00                  391 	.db #0x00	; 0
   567B 00                  392 	.db #0x00	; 0
   567C 00                  393 	.db #0x00	; 0
   567D 11                  394 	.db #0x11	; 17
   567E 22                  395 	.db #0x22	; 34
   567F 00                  396 	.db #0x00	; 0
   5680 22                  397 	.db #0x22	; 34
   5681 00                  398 	.db #0x00	; 0
   5682 00                  399 	.db #0x00	; 0
   5683 00                  400 	.db #0x00	; 0
   5684 00                  401 	.db #0x00	; 0
   5685 00                  402 	.db #0x00	; 0
   5686 00                  403 	.db #0x00	; 0
   5687 11                  404 	.db #0x11	; 17
   5688 33                  405 	.db #0x33	; 51	'3'
   5689 33                  406 	.db #0x33	; 51	'3'
   568A 33                  407 	.db #0x33	; 51	'3'
   568B 33                  408 	.db #0x33	; 51	'3'
   568C 33                  409 	.db #0x33	; 51	'3'
   568D 33                  410 	.db #0x33	; 51	'3'
   568E 33                  411 	.db #0x33	; 51	'3'
   568F 33                  412 	.db #0x33	; 51	'3'
   5690 33                  413 	.db #0x33	; 51	'3'
   5691 33                  414 	.db #0x33	; 51	'3'
   5692 22                  415 	.db #0x22	; 34
   5693 00                  416 	.db #0x00	; 0
   5694 22                  417 	.db #0x22	; 34
   5695 00                  418 	.db #0x00	; 0
   5696 00                  419 	.db #0x00	; 0
   5697 00                  420 	.db #0x00	; 0
   5698 00                  421 	.db #0x00	; 0
   5699 00                  422 	.db #0x00	; 0
   569A 00                  423 	.db #0x00	; 0
   569B 11                  424 	.db #0x11	; 17
   569C 22                  425 	.db #0x22	; 34
   569D 00                  426 	.db #0x00	; 0
   569E 22                  427 	.db #0x22	; 34
   569F 00                  428 	.db #0x00	; 0
   56A0 00                  429 	.db #0x00	; 0
   56A1 00                  430 	.db #0x00	; 0
   56A2 00                  431 	.db #0x00	; 0
   56A3 00                  432 	.db #0x00	; 0
   56A4 00                  433 	.db #0x00	; 0
   56A5 11                  434 	.db #0x11	; 17
   56A6 22                  435 	.db #0x22	; 34
   56A7 00                  436 	.db #0x00	; 0
   56A8 22                  437 	.db #0x22	; 34
   56A9 00                  438 	.db #0x00	; 0
   56AA 00                  439 	.db #0x00	; 0
   56AB 00                  440 	.db #0x00	; 0
   56AC 00                  441 	.db #0x00	; 0
   56AD 00                  442 	.db #0x00	; 0
   56AE 00                  443 	.db #0x00	; 0
   56AF 11                  444 	.db #0x11	; 17
   56B0 22                  445 	.db #0x22	; 34
   56B1 00                  446 	.db #0x00	; 0
   56B2 22                  447 	.db #0x22	; 34
   56B3 00                  448 	.db #0x00	; 0
   56B4 00                  449 	.db #0x00	; 0
   56B5 00                  450 	.db #0x00	; 0
   56B6 00                  451 	.db #0x00	; 0
   56B7 00                  452 	.db #0x00	; 0
   56B8 00                  453 	.db #0x00	; 0
   56B9 11                  454 	.db #0x11	; 17
   56BA 22                  455 	.db #0x22	; 34
   56BB 00                  456 	.db #0x00	; 0
   56BC 22                  457 	.db #0x22	; 34
   56BD 00                  458 	.db #0x00	; 0
   56BE 00                  459 	.db #0x00	; 0
   56BF 00                  460 	.db #0x00	; 0
   56C0 00                  461 	.db #0x00	; 0
   56C1 00                  462 	.db #0x00	; 0
   56C2 00                  463 	.db #0x00	; 0
   56C3 11                  464 	.db #0x11	; 17
   56C4 22                  465 	.db #0x22	; 34
   56C5 00                  466 	.db #0x00	; 0
   56C6 22                  467 	.db #0x22	; 34
   56C7 00                  468 	.db #0x00	; 0
   56C8 00                  469 	.db #0x00	; 0
   56C9 00                  470 	.db #0x00	; 0
   56CA 00                  471 	.db #0x00	; 0
   56CB 00                  472 	.db #0x00	; 0
   56CC 00                  473 	.db #0x00	; 0
   56CD 11                  474 	.db #0x11	; 17
   56CE 22                  475 	.db #0x22	; 34
   56CF 00                  476 	.db #0x00	; 0
   56D0 22                  477 	.db #0x22	; 34
   56D1 00                  478 	.db #0x00	; 0
   56D2 00                  479 	.db #0x00	; 0
   56D3 00                  480 	.db #0x00	; 0
   56D4 00                  481 	.db #0x00	; 0
   56D5 00                  482 	.db #0x00	; 0
   56D6 00                  483 	.db #0x00	; 0
   56D7 11                  484 	.db #0x11	; 17
   56D8 33                  485 	.db #0x33	; 51	'3'
   56D9 33                  486 	.db #0x33	; 51	'3'
   56DA 33                  487 	.db #0x33	; 51	'3'
   56DB 33                  488 	.db #0x33	; 51	'3'
   56DC 33                  489 	.db #0x33	; 51	'3'
   56DD 33                  490 	.db #0x33	; 51	'3'
   56DE 33                  491 	.db #0x33	; 51	'3'
   56DF 33                  492 	.db #0x33	; 51	'3'
   56E0 33                  493 	.db #0x33	; 51	'3'
   56E1 33                  494 	.db #0x33	; 51	'3'
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   56E2                     499 _enemyspawn::
   56E2 DD E5         [15]  500 	push	ix
   56E4 DD 21 00 00   [14]  501 	ld	ix,#0
   56E8 DD 39         [15]  502 	add	ix,sp
   56EA 21 F1 FF      [10]  503 	ld	hl, #-15
   56ED 39            [11]  504 	add	hl, sp
   56EE F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   56EF DD 7E 05      [19]  507 	ld	a, 5 (ix)
   56F2 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   56F5 CA B5 58      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   56F8 DD 7E 04      [19]  512 	ld	a, 4 (ix)
   56FB DD 77 FE      [19]  513 	ld	-2 (ix), a
   56FE DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5701 DD 77 FF      [19]  515 	ld	-1 (ix), a
   5704 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   5707 DD 66 FF      [19]  517 	ld	h,-1 (ix)
   570A DD 7E 06      [19]  518 	ld	a, 6 (ix)
   570D 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   570E DD 4E FE      [19]  521 	ld	c,-2 (ix)
   5711 DD 46 FF      [19]  522 	ld	b,-1 (ix)
   5714 03            [ 6]  523 	inc	bc
   5715 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   5718 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   5719 DD 7E FE      [19]  527 	ld	a, -2 (ix)
   571C C6 02         [ 7]  528 	add	a, #0x02
   571E DD 77 FC      [19]  529 	ld	-4 (ix), a
   5721 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5724 CE 00         [ 7]  531 	adc	a, #0x00
   5726 DD 77 FD      [19]  532 	ld	-3 (ix), a
   5729 DD 7E 09      [19]  533 	ld	a, 9 (ix)
   572C B7            [ 4]  534 	or	a, a
   572D 28 04         [12]  535 	jr	Z,00114$
   572F 0E 01         [ 7]  536 	ld	c, #0x01
   5731 18 02         [12]  537 	jr	00115$
   5733                     538 00114$:
   5733 0E FF         [ 7]  539 	ld	c, #0xff
   5735                     540 00115$:
   5735 DD 6E FC      [19]  541 	ld	l,-4 (ix)
   5738 DD 66 FD      [19]  542 	ld	h,-3 (ix)
   573B 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   573C DD 7E FE      [19]  545 	ld	a, -2 (ix)
   573F C6 03         [ 7]  546 	add	a, #0x03
   5741 DD 77 FA      [19]  547 	ld	-6 (ix), a
   5744 DD 7E FF      [19]  548 	ld	a, -1 (ix)
   5747 CE 00         [ 7]  549 	adc	a, #0x00
   5749 DD 77 FB      [19]  550 	ld	-5 (ix), a
   574C DD 6E FA      [19]  551 	ld	l,-6 (ix)
   574F DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5752 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   5754 DD 7E FE      [19]  555 	ld	a, -2 (ix)
   5757 C6 06         [ 7]  556 	add	a, #0x06
   5759 DD 77 F8      [19]  557 	ld	-8 (ix), a
   575C DD 7E FF      [19]  558 	ld	a, -1 (ix)
   575F CE 00         [ 7]  559 	adc	a, #0x00
   5761 DD 77 F9      [19]  560 	ld	-7 (ix), a
   5764 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   5767 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   576A 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   576C DD 7E FE      [19]  565 	ld	a, -2 (ix)
   576F C6 09         [ 7]  566 	add	a, #0x09
   5771 DD 77 F8      [19]  567 	ld	-8 (ix), a
   5774 DD 7E FF      [19]  568 	ld	a, -1 (ix)
   5777 CE 00         [ 7]  569 	adc	a, #0x00
   5779 DD 77 F9      [19]  570 	ld	-7 (ix), a
   577C DD 6E F8      [19]  571 	ld	l,-8 (ix)
   577F DD 66 F9      [19]  572 	ld	h,-7 (ix)
   5782 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   5785 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   5786 DD 7E FE      [19]  576 	ld	a, -2 (ix)
   5789 C6 04         [ 7]  577 	add	a, #0x04
   578B DD 77 F8      [19]  578 	ld	-8 (ix), a
   578E DD 7E FF      [19]  579 	ld	a, -1 (ix)
   5791 CE 00         [ 7]  580 	adc	a, #0x00
   5793 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   5796 DD 7E FE      [19]  583 	ld	a, -2 (ix)
   5799 C6 05         [ 7]  584 	add	a, #0x05
   579B DD 77 F6      [19]  585 	ld	-10 (ix), a
   579E DD 7E FF      [19]  586 	ld	a, -1 (ix)
   57A1 CE 00         [ 7]  587 	adc	a, #0x00
   57A3 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   57A6 DD 7E FE      [19]  590 	ld	a, -2 (ix)
   57A9 C6 07         [ 7]  591 	add	a, #0x07
   57AB DD 77 F4      [19]  592 	ld	-12 (ix), a
   57AE DD 7E FF      [19]  593 	ld	a, -1 (ix)
   57B1 CE 00         [ 7]  594 	adc	a, #0x00
   57B3 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   57B6 DD 7E FE      [19]  597 	ld	a, -2 (ix)
   57B9 C6 08         [ 7]  598 	add	a, #0x08
   57BB DD 77 FE      [19]  599 	ld	-2 (ix), a
   57BE DD 7E FF      [19]  600 	ld	a, -1 (ix)
   57C1 CE 00         [ 7]  601 	adc	a, #0x00
   57C3 DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   57C6 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   57C9 3D            [ 4]  605 	dec	a
   57CA 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   57CC DD 6E F8      [19]  608 	ld	l,-8 (ix)
   57CF DD 66 F9      [19]  609 	ld	h,-7 (ix)
   57D2 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   57D4 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   57D7 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   57DA 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   57DC DD 6E F4      [19]  616 	ld	l,-12 (ix)
   57DF DD 66 F5      [19]  617 	ld	h,-11 (ix)
   57E2 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   57E4 DD 6E FE      [19]  620 	ld	l,-2 (ix)
   57E7 DD 66 FF      [19]  621 	ld	h,-1 (ix)
   57EA 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   57EC DD 7E FC      [19]  624 	ld	a, -4 (ix)
   57EF DD 77 F2      [19]  625 	ld	-14 (ix), a
   57F2 DD 7E FD      [19]  626 	ld	a, -3 (ix)
   57F5 DD 77 F3      [19]  627 	ld	-13 (ix), a
   57F8 DD 7E 09      [19]  628 	ld	a, 9 (ix)
   57FB B7            [ 4]  629 	or	a, a
   57FC 28 06         [12]  630 	jr	Z,00116$
   57FE DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5802 18 04         [12]  632 	jr	00117$
   5804                     633 00116$:
   5804 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5808                     635 00117$:
   5808 DD 6E F2      [19]  636 	ld	l,-14 (ix)
   580B DD 66 F3      [19]  637 	ld	h,-13 (ix)
   580E DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5811 77            [ 7]  639 	ld	(hl), a
   5812 C3 B5 58      [10]  640 	jp	00112$
   5815                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   5815 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   5818 D6 02         [ 7]  644 	sub	a, #0x02
   581A 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   581C DD 6E F8      [19]  647 	ld	l,-8 (ix)
   581F DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5822 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5824 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   5827 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   582A 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   582C DD 6E F4      [19]  655 	ld	l,-12 (ix)
   582F DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5832 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5834 DD 6E FE      [19]  659 	ld	l,-2 (ix)
   5837 DD 66 FF      [19]  660 	ld	h,-1 (ix)
   583A 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   583C DD 4E FA      [19]  663 	ld	c,-6 (ix)
   583F DD 46 FB      [19]  664 	ld	b,-5 (ix)
   5842 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   5845 B7            [ 4]  666 	or	a, a
   5846 28 04         [12]  667 	jr	Z,00118$
   5848 3E 01         [ 7]  668 	ld	a, #0x01
   584A 18 02         [12]  669 	jr	00119$
   584C                     670 00118$:
   584C 3E FF         [ 7]  671 	ld	a, #0xff
   584E                     672 00119$:
   584E 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   584F DD 6E FC      [19]  675 	ld	l,-4 (ix)
   5852 DD 66 FD      [19]  676 	ld	h,-3 (ix)
   5855 36 01         [10]  677 	ld	(hl), #0x01
   5857 18 5C         [12]  678 	jr	00112$
   5859                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   5859 DD 7E 08      [19]  681 	ld	a, 8 (ix)
   585C D6 03         [ 7]  682 	sub	a, #0x03
   585E 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   5860 DD 6E F8      [19]  685 	ld	l,-8 (ix)
   5863 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   5866 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   5868 DD 6E F6      [19]  689 	ld	l,-10 (ix)
   586B DD 66 F7      [19]  690 	ld	h,-9 (ix)
   586E 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   5870 DD 6E F4      [19]  693 	ld	l,-12 (ix)
   5873 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   5876 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   5878 DD 6E FE      [19]  697 	ld	l,-2 (ix)
   587B DD 66 FF      [19]  698 	ld	h,-1 (ix)
   587E 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   5880 DD 4E FC      [19]  701 	ld	c,-4 (ix)
   5883 DD 46 FD      [19]  702 	ld	b,-3 (ix)
   5886 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   5889 B7            [ 4]  704 	or	a, a
   588A 28 04         [12]  705 	jr	Z,00120$
   588C 3E 01         [ 7]  706 	ld	a, #0x01
   588E 18 02         [12]  707 	jr	00121$
   5890                     708 00120$:
   5890 3E FF         [ 7]  709 	ld	a, #0xff
   5892                     710 00121$:
   5892 02            [ 7]  711 	ld	(bc), a
   5893 18 20         [12]  712 	jr	00112$
   5895                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   5895 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   5898 DD 66 F9      [19]  716 	ld	h,-7 (ix)
   589B 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   589D DD 6E F6      [19]  719 	ld	l,-10 (ix)
   58A0 DD 66 F7      [19]  720 	ld	h,-9 (ix)
   58A3 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   58A5 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   58A8 DD 66 F5      [19]  724 	ld	h,-11 (ix)
   58AB 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   58AD DD 6E FE      [19]  727 	ld	l,-2 (ix)
   58B0 DD 66 FF      [19]  728 	ld	h,-1 (ix)
   58B3 36 64         [10]  729 	ld	(hl), #0x64
   58B5                     730 00112$:
   58B5 DD F9         [10]  731 	ld	sp, ix
   58B7 DD E1         [14]  732 	pop	ix
   58B9 C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   58BA                     738 _enemyupdate::
   58BA DD E5         [15]  739 	push	ix
   58BC DD 21 00 00   [14]  740 	ld	ix,#0
   58C0 DD 39         [15]  741 	add	ix,sp
   58C2 21 F6 FF      [10]  742 	ld	hl, #-10
   58C5 39            [11]  743 	add	hl, sp
   58C6 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   58C7 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   58CA DD B6 04      [19]  747 	or	a,4 (ix)
   58CD CA C1 5A      [10]  748 	jp	Z,00121$
   58D0 DD 7E 04      [19]  749 	ld	a, 4 (ix)
   58D3 DD 77 FE      [19]  750 	ld	-2 (ix), a
   58D6 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   58D9 DD 77 FF      [19]  752 	ld	-1 (ix), a
   58DC DD 6E FE      [19]  753 	ld	l,-2 (ix)
   58DF DD 66 FF      [19]  754 	ld	h,-1 (ix)
   58E2 11 06 00      [10]  755 	ld	de, #0x0006
   58E5 19            [11]  756 	add	hl, de
   58E6 7E            [ 7]  757 	ld	a, (hl)
   58E7 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   58E8 CA C1 5A      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   58EB DD 6E FE      [19]  762 	ld	l,-2 (ix)
   58EE DD 66 FF      [19]  763 	ld	h,-1 (ix)
   58F1 11 09 00      [10]  764 	ld	de, #0x0009
   58F4 19            [11]  765 	add	hl, de
   58F5 7E            [ 7]  766 	ld	a, (hl)
   58F6 DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   58F9 DD 6E FE      [19]  769 	ld	l,-2 (ix)
   58FC DD 66 FF      [19]  770 	ld	h,-1 (ix)
   58FF 4E            [ 7]  771 	ld	c, (hl)
   5900 DD 7E FE      [19]  772 	ld	a, -2 (ix)
   5903 C6 02         [ 7]  773 	add	a, #0x02
   5905 DD 77 FB      [19]  774 	ld	-5 (ix), a
   5908 DD 7E FF      [19]  775 	ld	a, -1 (ix)
   590B CE 00         [ 7]  776 	adc	a, #0x00
   590D DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5910 DD 7E FE      [19]  779 	ld	a, -2 (ix)
   5913 C6 01         [ 7]  780 	add	a, #0x01
   5915 DD 77 F9      [19]  781 	ld	-7 (ix), a
   5918 DD 7E FF      [19]  782 	ld	a, -1 (ix)
   591B CE 00         [ 7]  783 	adc	a, #0x00
   591D DD 77 FA      [19]  784 	ld	-6 (ix), a
   5920 DD 5E FE      [19]  785 	ld	e,-2 (ix)
   5923 DD 56 FF      [19]  786 	ld	d,-1 (ix)
   5926 13            [ 6]  787 	inc	de
   5927 13            [ 6]  788 	inc	de
   5928 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5929 06 00         [ 7]  791 	ld	b, #0x00
   592B DD 6E FB      [19]  792 	ld	l,-5 (ix)
   592E DD 66 FC      [19]  793 	ld	h,-4 (ix)
   5931 7E            [ 7]  794 	ld	a, (hl)
   5932 DD 77 F8      [19]  795 	ld	-8 (ix), a
   5935 6F            [ 4]  796 	ld	l, a
   5936 DD 7E F8      [19]  797 	ld	a, -8 (ix)
   5939 17            [ 4]  798 	rla
   593A 9F            [ 4]  799 	sbc	a, a
   593B 67            [ 4]  800 	ld	h, a
   593C 09            [11]  801 	add	hl,bc
   593D 4D            [ 4]  802 	ld	c, l
   593E 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   593F DD 7E FD      [19]  805 	ld	a, -3 (ix)
   5942 D6 02         [ 7]  806 	sub	a, #0x02
   5944 C2 ED 59      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5947 DD 6E F9      [19]  810 	ld	l,-7 (ix)
   594A DD 66 FA      [19]  811 	ld	h,-6 (ix)
   594D 6E            [ 7]  812 	ld	l, (hl)
   594E DD 75 F6      [19]  813 	ld	-10 (ix), l
   5951 DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   5955 1A            [ 7]  815 	ld	a, (de)
   5956 6F            [ 4]  816 	ld	l, a
   5957 17            [ 4]  817 	rla
   5958 9F            [ 4]  818 	sbc	a, a
   5959 67            [ 4]  819 	ld	h, a
   595A DD 7E F6      [19]  820 	ld	a, -10 (ix)
   595D 85            [ 4]  821 	add	a, l
   595E DD 77 F6      [19]  822 	ld	-10 (ix), a
   5961 DD 7E F7      [19]  823 	ld	a, -9 (ix)
   5964 8C            [ 4]  824 	adc	a, h
   5965 DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   5968 79            [ 4]  827 	ld	a, c
   5969 D6 08         [ 7]  828 	sub	a, #0x08
   596B 78            [ 4]  829 	ld	a, b
   596C 17            [ 4]  830 	rla
   596D 3F            [ 4]  831 	ccf
   596E 1F            [ 4]  832 	rra
   596F DE 80         [ 7]  833 	sbc	a, #0x80
   5971 38 0E         [12]  834 	jr	C,00104$
   5973 3E 48         [ 7]  835 	ld	a, #0x48
   5975 B9            [ 4]  836 	cp	a, c
   5976 3E 00         [ 7]  837 	ld	a, #0x00
   5978 98            [ 4]  838 	sbc	a, b
   5979 E2 7E 59      [10]  839 	jp	PO, 00161$
   597C EE 80         [ 7]  840 	xor	a, #0x80
   597E                     841 00161$:
   597E F2 9C 59      [10]  842 	jp	P, 00105$
   5981                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   5981 AF            [ 4]  845 	xor	a, a
   5982 DD 96 F8      [19]  846 	sub	a, -8 (ix)
   5985 4F            [ 4]  847 	ld	c, a
   5986 DD 6E FB      [19]  848 	ld	l,-5 (ix)
   5989 DD 66 FC      [19]  849 	ld	h,-4 (ix)
   598C 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   598D DD 6E FE      [19]  852 	ld	l,-2 (ix)
   5990 DD 66 FF      [19]  853 	ld	h,-1 (ix)
   5993 6E            [ 7]  854 	ld	l, (hl)
   5994 26 00         [ 7]  855 	ld	h, #0x00
   5996 79            [ 4]  856 	ld	a, c
   5997 17            [ 4]  857 	rla
   5998 9F            [ 4]  858 	sbc	a, a
   5999 47            [ 4]  859 	ld	b, a
   599A 09            [11]  860 	add	hl,bc
   599B 4D            [ 4]  861 	ld	c, l
   599C                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   599C DD 7E F6      [19]  864 	ld	a, -10 (ix)
   599F D6 38         [ 7]  865 	sub	a, #0x38
   59A1 DD 7E F7      [19]  866 	ld	a, -9 (ix)
   59A4 17            [ 4]  867 	rla
   59A5 3F            [ 4]  868 	ccf
   59A6 1F            [ 4]  869 	rra
   59A7 DE 80         [ 7]  870 	sbc	a, #0x80
   59A9 38 12         [12]  871 	jr	C,00107$
   59AB 3E 78         [ 7]  872 	ld	a, #0x78
   59AD DD BE F6      [19]  873 	cp	a, -10 (ix)
   59B0 3E 00         [ 7]  874 	ld	a, #0x00
   59B2 DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   59B5 E2 BA 59      [10]  876 	jp	PO, 00162$
   59B8 EE 80         [ 7]  877 	xor	a, #0x80
   59BA                     878 00162$:
   59BA F2 D9 59      [10]  879 	jp	P, 00108$
   59BD                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   59BD 1A            [ 7]  882 	ld	a, (de)
   59BE 6F            [ 4]  883 	ld	l, a
   59BF AF            [ 4]  884 	xor	a, a
   59C0 95            [ 4]  885 	sub	a, l
   59C1 DD 77 F8      [19]  886 	ld	-8 (ix), a
   59C4 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   59C5 DD 6E F9      [19]  889 	ld	l,-7 (ix)
   59C8 DD 66 FA      [19]  890 	ld	h,-6 (ix)
   59CB 5E            [ 7]  891 	ld	e, (hl)
   59CC 16 00         [ 7]  892 	ld	d, #0x00
   59CE DD 6E F8      [19]  893 	ld	l, -8 (ix)
   59D1 DD 7E F8      [19]  894 	ld	a, -8 (ix)
   59D4 17            [ 4]  895 	rla
   59D5 9F            [ 4]  896 	sbc	a, a
   59D6 67            [ 4]  897 	ld	h, a
   59D7 19            [11]  898 	add	hl,de
   59D8 E3            [19]  899 	ex	(sp), hl
   59D9                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   59D9 DD 6E FE      [19]  902 	ld	l,-2 (ix)
   59DC DD 66 FF      [19]  903 	ld	h,-1 (ix)
   59DF 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   59E0 DD 4E F6      [19]  906 	ld	c, -10 (ix)
   59E3 DD 6E F9      [19]  907 	ld	l,-7 (ix)
   59E6 DD 66 FA      [19]  908 	ld	h,-6 (ix)
   59E9 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   59EA C3 C1 5A      [10]  911 	jp	00121$
   59ED                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   59ED 79            [ 4]  915 	ld	a, c
   59EE D6 02         [ 7]  916 	sub	a, #0x02
   59F0 78            [ 4]  917 	ld	a, b
   59F1 17            [ 4]  918 	rla
   59F2 3F            [ 4]  919 	ccf
   59F3 1F            [ 4]  920 	rra
   59F4 DE 80         [ 7]  921 	sbc	a, #0x80
   59F6 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   59F8 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   59FB DD 6E FB      [19]  926 	ld	l,-5 (ix)
   59FE DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5A01 36 01         [10]  928 	ld	(hl), #0x01
   5A03                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5A03 DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5A06 DD 66 FF      [19]  932 	ld	h,-1 (ix)
   5A09 23            [ 6]  933 	inc	hl
   5A0A 23            [ 6]  934 	inc	hl
   5A0B 23            [ 6]  935 	inc	hl
   5A0C 23            [ 6]  936 	inc	hl
   5A0D 6E            [ 7]  937 	ld	l, (hl)
   5A0E 26 00         [ 7]  938 	ld	h, #0x00
   5A10 3E 50         [ 7]  939 	ld	a, #0x50
   5A12 95            [ 4]  940 	sub	a, l
   5A13 6F            [ 4]  941 	ld	l, a
   5A14 3E 00         [ 7]  942 	ld	a, #0x00
   5A16 9C            [ 4]  943 	sbc	a, h
   5A17 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5A18 7D            [ 4]  946 	ld	a, l
   5A19 91            [ 4]  947 	sub	a, c
   5A1A 7C            [ 4]  948 	ld	a, h
   5A1B 98            [ 4]  949 	sbc	a, b
   5A1C E2 21 5A      [10]  950 	jp	PO, 00163$
   5A1F EE 80         [ 7]  951 	xor	a, #0x80
   5A21                     952 00163$:
   5A21 F2 2D 5A      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5A24 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5A25 DD 6E FB      [19]  957 	ld	l,-5 (ix)
   5A28 DD 66 FC      [19]  958 	ld	h,-4 (ix)
   5A2B 36 FF         [10]  959 	ld	(hl), #0xff
   5A2D                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5A2D DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5A30 DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5A33 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5A34 1A            [ 7]  966 	ld	a, (de)
   5A35 4F            [ 4]  967 	ld	c, a
   5A36 0C            [ 4]  968 	inc	c
   5A37 79            [ 4]  969 	ld	a, c
   5A38 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   5A39 3E 03         [ 7]  972 	ld	a, #0x03
   5A3B 91            [ 4]  973 	sub	a, c
   5A3C E2 41 5A      [10]  974 	jp	PO, 00164$
   5A3F EE 80         [ 7]  975 	xor	a, #0x80
   5A41                     976 00164$:
   5A41 F2 47 5A      [10]  977 	jp	P, 00117$
   5A44 3E 03         [ 7]  978 	ld	a, #0x03
   5A46 12            [ 7]  979 	ld	(de), a
   5A47                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   5A47 DD 6E F9      [19]  982 	ld	l,-7 (ix)
   5A4A DD 66 FA      [19]  983 	ld	h,-6 (ix)
   5A4D 4E            [ 7]  984 	ld	c, (hl)
   5A4E 06 00         [ 7]  985 	ld	b, #0x00
   5A50 1A            [ 7]  986 	ld	a, (de)
   5A51 6F            [ 4]  987 	ld	l, a
   5A52 17            [ 4]  988 	rla
   5A53 9F            [ 4]  989 	sbc	a, a
   5A54 67            [ 4]  990 	ld	h, a
   5A55 09            [11]  991 	add	hl, bc
   5A56 E5            [11]  992 	push	hl
   5A57 FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5A59 DD 7E FE      [19]  995 	ld	a, -2 (ix)
   5A5C C6 05         [ 7]  996 	add	a, #0x05
   5A5E DD 77 F6      [19]  997 	ld	-10 (ix), a
   5A61 DD 7E FF      [19]  998 	ld	a, -1 (ix)
   5A64 CE 00         [ 7]  999 	adc	a, #0x00
   5A66 DD 77 F7      [19] 1000 	ld	-9 (ix), a
   5A69 E1            [10] 1001 	pop	hl
   5A6A E5            [11] 1002 	push	hl
   5A6B 7E            [ 7] 1003 	ld	a, (hl)
   5A6C DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   5A6F DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   5A72 4E            [ 7] 1006 	ld	c, (hl)
   5A73 06 00         [ 7] 1007 	ld	b, #0x00
   5A75 D5            [11] 1008 	push	de
   5A76 F5            [11] 1009 	push	af
   5A77 33            [ 6] 1010 	inc	sp
   5A78 FD E5         [15] 1011 	push	iy
   5A7A C5            [11] 1012 	push	bc
   5A7B CD 40 4C      [17] 1013 	call	_collision_clamp_y_at
   5A7E F1            [10] 1014 	pop	af
   5A7F F1            [10] 1015 	pop	af
   5A80 33            [ 6] 1016 	inc	sp
   5A81 4D            [ 4] 1017 	ld	c, l
   5A82 D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5A83 DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   5A86 DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   5A89 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5A8A E1            [10] 1024 	pop	hl
   5A8B E5            [11] 1025 	push	hl
   5A8C 7E            [ 7] 1026 	ld	a, (hl)
   5A8D 06 00         [ 7] 1027 	ld	b, #0x00
   5A8F DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   5A92 DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   5A95 6E            [ 7] 1030 	ld	l, (hl)
   5A96 DD 75 F6      [19] 1031 	ld	-10 (ix), l
   5A99 DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   5A9D D5            [11] 1033 	push	de
   5A9E F5            [11] 1034 	push	af
   5A9F 33            [ 6] 1035 	inc	sp
   5AA0 C5            [11] 1036 	push	bc
   5AA1 DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5AA4 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5AA7 E5            [11] 1039 	push	hl
   5AA8 CD C1 4B      [17] 1040 	call	_collision_is_on_ground_at
   5AAB F1            [10] 1041 	pop	af
   5AAC F1            [10] 1042 	pop	af
   5AAD 33            [ 6] 1043 	inc	sp
   5AAE D1            [10] 1044 	pop	de
   5AAF 7D            [ 4] 1045 	ld	a, l
   5AB0 B7            [ 4] 1046 	or	a, a
   5AB1 28 0E         [12] 1047 	jr	Z,00121$
   5AB3 1A            [ 7] 1048 	ld	a, (de)
   5AB4 4F            [ 4] 1049 	ld	c, a
   5AB5 AF            [ 4] 1050 	xor	a, a
   5AB6 91            [ 4] 1051 	sub	a, c
   5AB7 E2 BC 5A      [10] 1052 	jp	PO, 00165$
   5ABA EE 80         [ 7] 1053 	xor	a, #0x80
   5ABC                    1054 00165$:
   5ABC F2 C1 5A      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5ABF AF            [ 4] 1057 	xor	a, a
   5AC0 12            [ 7] 1058 	ld	(de), a
   5AC1                    1059 00121$:
   5AC1 DD F9         [10] 1060 	ld	sp, ix
   5AC3 DD E1         [14] 1061 	pop	ix
   5AC5 C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5AC6                    1067 _enemyrender::
   5AC6 DD E5         [15] 1068 	push	ix
   5AC8 DD 21 00 00   [14] 1069 	ld	ix,#0
   5ACC DD 39         [15] 1070 	add	ix,sp
   5ACE F5            [11] 1071 	push	af
   5ACF 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5AD0 DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5AD3 DD B6 04      [19] 1075 	or	a,4 (ix)
   5AD6 CA 53 5B      [10] 1076 	jp	Z,00113$
   5AD9 DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5ADC DD 46 05      [19] 1078 	ld	b,5 (ix)
   5ADF C5            [11] 1079 	push	bc
   5AE0 FD E1         [14] 1080 	pop	iy
   5AE2 FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5AE5 B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5AE6 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5AE8 C5            [11] 1086 	push	bc
   5AE9 FD E1         [14] 1087 	pop	iy
   5AEB FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5AEE FE 03         [ 7] 1089 	cp	a, #0x03
   5AF0 20 0A         [12] 1090 	jr	NZ,00111$
   5AF2 DD 36 FE 2E   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5AF6 DD 36 FF 56   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5AFA 18 23         [12] 1093 	jr	00112$
   5AFC                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5AFC FE 02         [ 7] 1096 	cp	a, #0x02
   5AFE 20 0A         [12] 1097 	jr	NZ,00108$
   5B00 DD 36 FE F2   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5B04 DD 36 FF 55   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5B08 18 15         [12] 1100 	jr	00112$
   5B0A                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5B0A 3D            [ 4] 1103 	dec	a
   5B0B 20 0A         [12] 1104 	jr	NZ,00105$
   5B0D DD 36 FE AC   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5B11 DD 36 FF 55   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5B15 18 08         [12] 1107 	jr	00112$
   5B17                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5B17 DD 36 FE 6C   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5B1B DD 36 FF 55   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5B1F                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5B1F 69            [ 4] 1114 	ld	l, c
   5B20 60            [ 4] 1115 	ld	h, b
   5B21 23            [ 6] 1116 	inc	hl
   5B22 56            [ 7] 1117 	ld	d, (hl)
   5B23 0A            [ 7] 1118 	ld	a, (bc)
   5B24 C5            [11] 1119 	push	bc
   5B25 5F            [ 4] 1120 	ld	e, a
   5B26 D5            [11] 1121 	push	de
   5B27 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5B2A E5            [11] 1123 	push	hl
   5B2B CD 41 63      [17] 1124 	call	_cpct_getScreenPtr
   5B2E EB            [ 4] 1125 	ex	de,hl
   5B2F C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5B30 C5            [11] 1128 	push	bc
   5B31 FD E1         [14] 1129 	pop	iy
   5B33 FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5B36 DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5B39 69            [ 4] 1132 	ld	l, c
   5B3A 60            [ 4] 1133 	ld	h, b
   5B3B 01 04 00      [10] 1134 	ld	bc, #0x0004
   5B3E 09            [11] 1135 	add	hl, bc
   5B3F 4E            [ 7] 1136 	ld	c, (hl)
   5B40 D5            [11] 1137 	push	de
   5B41 FD E1         [14] 1138 	pop	iy
   5B43 DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5B46 DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5B49 DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5B4C C5            [11] 1142 	push	bc
   5B4D FD E5         [15] 1143 	push	iy
   5B4F D5            [11] 1144 	push	de
   5B50 CD 72 61      [17] 1145 	call	_cpct_drawSprite
   5B53                    1146 00113$:
   5B53 DD F9         [10] 1147 	ld	sp, ix
   5B55 DD E1         [14] 1148 	pop	ix
   5B57 C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5B58                    1154 _enemydamage::
   5B58 DD E5         [15] 1155 	push	ix
   5B5A DD 21 00 00   [14] 1156 	ld	ix,#0
   5B5E DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5B60 DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5B63 DD B6 04      [19] 1160 	or	a,4 (ix)
   5B66 28 0F         [12] 1161 	jr	Z,00101$
   5B68 DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5B6B DD 46 05      [19] 1163 	ld	b,5 (ix)
   5B6E 21 06 00      [10] 1164 	ld	hl, #0x0006
   5B71 09            [11] 1165 	add	hl,bc
   5B72 EB            [ 4] 1166 	ex	de,hl
   5B73 1A            [ 7] 1167 	ld	a, (de)
   5B74 B7            [ 4] 1168 	or	a, a
   5B75 20 04         [12] 1169 	jr	NZ,00102$
   5B77                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5B77 2E 00         [ 7] 1172 	ld	l, #0x00
   5B79 18 1A         [12] 1173 	jr	00106$
   5B7B                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5B7B 21 07 00      [10] 1176 	ld	hl, #0x0007
   5B7E 09            [11] 1177 	add	hl, bc
   5B7F 4E            [ 7] 1178 	ld	c, (hl)
   5B80 DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5B83 91            [ 4] 1180 	sub	a, c
   5B84 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5B86 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5B88 AF            [ 4] 1185 	xor	a, a
   5B89 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5B8A 2E 01         [ 7] 1188 	ld	l, #0x01
   5B8C 18 07         [12] 1189 	jr	00106$
   5B8E                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5B8E 79            [ 4] 1192 	ld	a, c
   5B8F DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5B92 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5B93 2E 00         [ 7] 1196 	ld	l, #0x00
   5B95                    1197 00106$:
   5B95 DD E1         [14] 1198 	pop	ix
   5B97 C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
