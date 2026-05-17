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
   561C                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   561C 21 03 00      [10]   57 	ld	hl, #2+1
   561F 39            [11]   58 	add	hl, sp
   5620 7E            [ 7]   59 	ld	a, (hl)
   5621 2B            [ 6]   60 	dec	hl
   5622 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   5623 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   5624 D1            [10]   65 	pop	de
   5625 C1            [10]   66 	pop	bc
   5626 C5            [11]   67 	push	bc
   5627 D5            [11]   68 	push	de
   5628 AF            [ 4]   69 	xor	a, a
   5629 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   562A 59            [ 4]   72 	ld	e, c
   562B 50            [ 4]   73 	ld	d, b
   562C 13            [ 6]   74 	inc	de
   562D AF            [ 4]   75 	xor	a, a
   562E 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   562F 59            [ 4]   78 	ld	e, c
   5630 50            [ 4]   79 	ld	d, b
   5631 13            [ 6]   80 	inc	de
   5632 13            [ 6]   81 	inc	de
   5633 AF            [ 4]   82 	xor	a, a
   5634 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   5635 59            [ 4]   85 	ld	e, c
   5636 50            [ 4]   86 	ld	d, b
   5637 13            [ 6]   87 	inc	de
   5638 13            [ 6]   88 	inc	de
   5639 13            [ 6]   89 	inc	de
   563A AF            [ 4]   90 	xor	a, a
   563B 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   563C 21 04 00      [10]   93 	ld	hl, #0x0004
   563F 09            [11]   94 	add	hl, bc
   5640 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   5642 21 05 00      [10]   97 	ld	hl, #0x0005
   5645 09            [11]   98 	add	hl, bc
   5646 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   5648 21 06 00      [10]  101 	ld	hl, #0x0006
   564B 09            [11]  102 	add	hl, bc
   564C 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   564E 21 07 00      [10]  105 	ld	hl, #0x0007
   5651 09            [11]  106 	add	hl, bc
   5652 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   5654 21 08 00      [10]  109 	ld	hl, #0x0008
   5657 09            [11]  110 	add	hl, bc
   5658 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   565A 21 09 00      [10]  113 	ld	hl, #0x0009
   565D 09            [11]  114 	add	hl, bc
   565E 36 00         [10]  115 	ld	(hl), #0x00
   5660 C9            [10]  116 	ret
   5661                     117 _enemy_kind0_sprite:
   5661 30                  118 	.db #0x30	; 48	'0'
   5662 30                  119 	.db #0x30	; 48	'0'
   5663 30                  120 	.db #0x30	; 48	'0'
   5664 30                  121 	.db #0x30	; 48	'0'
   5665 30                  122 	.db #0x30	; 48	'0'
   5666 00                  123 	.db #0x00	; 0
   5667 00                  124 	.db #0x00	; 0
   5668 10                  125 	.db #0x10	; 16
   5669 30                  126 	.db #0x30	; 48	'0'
   566A 00                  127 	.db #0x00	; 0
   566B 00                  128 	.db #0x00	; 0
   566C 10                  129 	.db #0x10	; 16
   566D 30                  130 	.db #0x30	; 48	'0'
   566E 00                  131 	.db #0x00	; 0
   566F 00                  132 	.db #0x00	; 0
   5670 10                  133 	.db #0x10	; 16
   5671 30                  134 	.db #0x30	; 48	'0'
   5672 00                  135 	.db #0x00	; 0
   5673 00                  136 	.db #0x00	; 0
   5674 10                  137 	.db #0x10	; 16
   5675 30                  138 	.db #0x30	; 48	'0'
   5676 00                  139 	.db #0x00	; 0
   5677 00                  140 	.db #0x00	; 0
   5678 10                  141 	.db #0x10	; 16
   5679 30                  142 	.db #0x30	; 48	'0'
   567A 00                  143 	.db #0x00	; 0
   567B 00                  144 	.db #0x00	; 0
   567C 10                  145 	.db #0x10	; 16
   567D 30                  146 	.db #0x30	; 48	'0'
   567E 00                  147 	.db #0x00	; 0
   567F 00                  148 	.db #0x00	; 0
   5680 10                  149 	.db #0x10	; 16
   5681 30                  150 	.db #0x30	; 48	'0'
   5682 30                  151 	.db #0x30	; 48	'0'
   5683 30                  152 	.db #0x30	; 48	'0'
   5684 30                  153 	.db #0x30	; 48	'0'
   5685 30                  154 	.db #0x30	; 48	'0'
   5686 00                  155 	.db #0x00	; 0
   5687 00                  156 	.db #0x00	; 0
   5688 10                  157 	.db #0x10	; 16
   5689 30                  158 	.db #0x30	; 48	'0'
   568A 00                  159 	.db #0x00	; 0
   568B 00                  160 	.db #0x00	; 0
   568C 10                  161 	.db #0x10	; 16
   568D 30                  162 	.db #0x30	; 48	'0'
   568E 00                  163 	.db #0x00	; 0
   568F 00                  164 	.db #0x00	; 0
   5690 10                  165 	.db #0x10	; 16
   5691 30                  166 	.db #0x30	; 48	'0'
   5692 00                  167 	.db #0x00	; 0
   5693 00                  168 	.db #0x00	; 0
   5694 10                  169 	.db #0x10	; 16
   5695 30                  170 	.db #0x30	; 48	'0'
   5696 00                  171 	.db #0x00	; 0
   5697 00                  172 	.db #0x00	; 0
   5698 10                  173 	.db #0x10	; 16
   5699 30                  174 	.db #0x30	; 48	'0'
   569A 00                  175 	.db #0x00	; 0
   569B 00                  176 	.db #0x00	; 0
   569C 10                  177 	.db #0x10	; 16
   569D 30                  178 	.db #0x30	; 48	'0'
   569E 30                  179 	.db #0x30	; 48	'0'
   569F 30                  180 	.db #0x30	; 48	'0'
   56A0 30                  181 	.db #0x30	; 48	'0'
   56A1                     182 _enemy_kind1_sprite:
   56A1 3F                  183 	.db #0x3f	; 63
   56A2 3F                  184 	.db #0x3f	; 63
   56A3 3F                  185 	.db #0x3f	; 63
   56A4 3F                  186 	.db #0x3f	; 63
   56A5 3F                  187 	.db #0x3f	; 63
   56A6 2A                  188 	.db #0x2a	; 42
   56A7 2A                  189 	.db #0x2a	; 42
   56A8 00                  190 	.db #0x00	; 0
   56A9 00                  191 	.db #0x00	; 0
   56AA 15                  192 	.db #0x15	; 21
   56AB 2A                  193 	.db #0x2a	; 42
   56AC 2A                  194 	.db #0x2a	; 42
   56AD 00                  195 	.db #0x00	; 0
   56AE 00                  196 	.db #0x00	; 0
   56AF 15                  197 	.db #0x15	; 21
   56B0 2A                  198 	.db #0x2a	; 42
   56B1 2A                  199 	.db #0x2a	; 42
   56B2 00                  200 	.db #0x00	; 0
   56B3 00                  201 	.db #0x00	; 0
   56B4 15                  202 	.db #0x15	; 21
   56B5 2A                  203 	.db #0x2a	; 42
   56B6 2A                  204 	.db #0x2a	; 42
   56B7 00                  205 	.db #0x00	; 0
   56B8 00                  206 	.db #0x00	; 0
   56B9 15                  207 	.db #0x15	; 21
   56BA 2A                  208 	.db #0x2a	; 42
   56BB 2A                  209 	.db #0x2a	; 42
   56BC 00                  210 	.db #0x00	; 0
   56BD 00                  211 	.db #0x00	; 0
   56BE 15                  212 	.db #0x15	; 21
   56BF 2A                  213 	.db #0x2a	; 42
   56C0 2A                  214 	.db #0x2a	; 42
   56C1 00                  215 	.db #0x00	; 0
   56C2 00                  216 	.db #0x00	; 0
   56C3 15                  217 	.db #0x15	; 21
   56C4 3F                  218 	.db #0x3f	; 63
   56C5 3F                  219 	.db #0x3f	; 63
   56C6 3F                  220 	.db #0x3f	; 63
   56C7 3F                  221 	.db #0x3f	; 63
   56C8 3F                  222 	.db #0x3f	; 63
   56C9 2A                  223 	.db #0x2a	; 42
   56CA 2A                  224 	.db #0x2a	; 42
   56CB 00                  225 	.db #0x00	; 0
   56CC 00                  226 	.db #0x00	; 0
   56CD 15                  227 	.db #0x15	; 21
   56CE 2A                  228 	.db #0x2a	; 42
   56CF 2A                  229 	.db #0x2a	; 42
   56D0 00                  230 	.db #0x00	; 0
   56D1 00                  231 	.db #0x00	; 0
   56D2 15                  232 	.db #0x15	; 21
   56D3 2A                  233 	.db #0x2a	; 42
   56D4 2A                  234 	.db #0x2a	; 42
   56D5 00                  235 	.db #0x00	; 0
   56D6 00                  236 	.db #0x00	; 0
   56D7 15                  237 	.db #0x15	; 21
   56D8 2A                  238 	.db #0x2a	; 42
   56D9 2A                  239 	.db #0x2a	; 42
   56DA 00                  240 	.db #0x00	; 0
   56DB 00                  241 	.db #0x00	; 0
   56DC 15                  242 	.db #0x15	; 21
   56DD 2A                  243 	.db #0x2a	; 42
   56DE 2A                  244 	.db #0x2a	; 42
   56DF 00                  245 	.db #0x00	; 0
   56E0 00                  246 	.db #0x00	; 0
   56E1 15                  247 	.db #0x15	; 21
   56E2 3F                  248 	.db #0x3f	; 63
   56E3 3F                  249 	.db #0x3f	; 63
   56E4 3F                  250 	.db #0x3f	; 63
   56E5 3F                  251 	.db #0x3f	; 63
   56E6 3F                  252 	.db #0x3f	; 63
   56E7                     253 _enemy_kind2_sprite:
   56E7 0F                  254 	.db #0x0f	; 15
   56E8 0F                  255 	.db #0x0f	; 15
   56E9 0F                  256 	.db #0x0f	; 15
   56EA 0F                  257 	.db #0x0f	; 15
   56EB 0F                  258 	.db #0x0f	; 15
   56EC 0F                  259 	.db #0x0f	; 15
   56ED 0A                  260 	.db #0x0a	; 10
   56EE 05                  261 	.db #0x05	; 5
   56EF 00                  262 	.db #0x00	; 0
   56F0 00                  263 	.db #0x00	; 0
   56F1 00                  264 	.db #0x00	; 0
   56F2 05                  265 	.db #0x05	; 5
   56F3 0A                  266 	.db #0x0a	; 10
   56F4 05                  267 	.db #0x05	; 5
   56F5 00                  268 	.db #0x00	; 0
   56F6 00                  269 	.db #0x00	; 0
   56F7 00                  270 	.db #0x00	; 0
   56F8 05                  271 	.db #0x05	; 5
   56F9 0A                  272 	.db #0x0a	; 10
   56FA 05                  273 	.db #0x05	; 5
   56FB 00                  274 	.db #0x00	; 0
   56FC 00                  275 	.db #0x00	; 0
   56FD 00                  276 	.db #0x00	; 0
   56FE 05                  277 	.db #0x05	; 5
   56FF 0A                  278 	.db #0x0a	; 10
   5700 05                  279 	.db #0x05	; 5
   5701 00                  280 	.db #0x00	; 0
   5702 00                  281 	.db #0x00	; 0
   5703 00                  282 	.db #0x00	; 0
   5704 05                  283 	.db #0x05	; 5
   5705 0F                  284 	.db #0x0f	; 15
   5706 0F                  285 	.db #0x0f	; 15
   5707 0F                  286 	.db #0x0f	; 15
   5708 0F                  287 	.db #0x0f	; 15
   5709 0F                  288 	.db #0x0f	; 15
   570A 0F                  289 	.db #0x0f	; 15
   570B 0A                  290 	.db #0x0a	; 10
   570C 05                  291 	.db #0x05	; 5
   570D 00                  292 	.db #0x00	; 0
   570E 00                  293 	.db #0x00	; 0
   570F 00                  294 	.db #0x00	; 0
   5710 05                  295 	.db #0x05	; 5
   5711 0A                  296 	.db #0x0a	; 10
   5712 05                  297 	.db #0x05	; 5
   5713 00                  298 	.db #0x00	; 0
   5714 00                  299 	.db #0x00	; 0
   5715 00                  300 	.db #0x00	; 0
   5716 05                  301 	.db #0x05	; 5
   5717 0A                  302 	.db #0x0a	; 10
   5718 05                  303 	.db #0x05	; 5
   5719 00                  304 	.db #0x00	; 0
   571A 00                  305 	.db #0x00	; 0
   571B 00                  306 	.db #0x00	; 0
   571C 05                  307 	.db #0x05	; 5
   571D 0F                  308 	.db #0x0f	; 15
   571E 0F                  309 	.db #0x0f	; 15
   571F 0F                  310 	.db #0x0f	; 15
   5720 0F                  311 	.db #0x0f	; 15
   5721 0F                  312 	.db #0x0f	; 15
   5722 0F                  313 	.db #0x0f	; 15
   5723                     314 _enemy_kind3_sprite:
   5723 33                  315 	.db #0x33	; 51	'3'
   5724 33                  316 	.db #0x33	; 51	'3'
   5725 33                  317 	.db #0x33	; 51	'3'
   5726 33                  318 	.db #0x33	; 51	'3'
   5727 33                  319 	.db #0x33	; 51	'3'
   5728 33                  320 	.db #0x33	; 51	'3'
   5729 33                  321 	.db #0x33	; 51	'3'
   572A 33                  322 	.db #0x33	; 51	'3'
   572B 33                  323 	.db #0x33	; 51	'3'
   572C 33                  324 	.db #0x33	; 51	'3'
   572D 22                  325 	.db #0x22	; 34
   572E 00                  326 	.db #0x00	; 0
   572F 22                  327 	.db #0x22	; 34
   5730 00                  328 	.db #0x00	; 0
   5731 00                  329 	.db #0x00	; 0
   5732 00                  330 	.db #0x00	; 0
   5733 00                  331 	.db #0x00	; 0
   5734 00                  332 	.db #0x00	; 0
   5735 00                  333 	.db #0x00	; 0
   5736 11                  334 	.db #0x11	; 17
   5737 22                  335 	.db #0x22	; 34
   5738 00                  336 	.db #0x00	; 0
   5739 22                  337 	.db #0x22	; 34
   573A 00                  338 	.db #0x00	; 0
   573B 00                  339 	.db #0x00	; 0
   573C 00                  340 	.db #0x00	; 0
   573D 00                  341 	.db #0x00	; 0
   573E 00                  342 	.db #0x00	; 0
   573F 00                  343 	.db #0x00	; 0
   5740 11                  344 	.db #0x11	; 17
   5741 22                  345 	.db #0x22	; 34
   5742 00                  346 	.db #0x00	; 0
   5743 22                  347 	.db #0x22	; 34
   5744 00                  348 	.db #0x00	; 0
   5745 00                  349 	.db #0x00	; 0
   5746 00                  350 	.db #0x00	; 0
   5747 00                  351 	.db #0x00	; 0
   5748 00                  352 	.db #0x00	; 0
   5749 00                  353 	.db #0x00	; 0
   574A 11                  354 	.db #0x11	; 17
   574B 22                  355 	.db #0x22	; 34
   574C 00                  356 	.db #0x00	; 0
   574D 22                  357 	.db #0x22	; 34
   574E 00                  358 	.db #0x00	; 0
   574F 00                  359 	.db #0x00	; 0
   5750 00                  360 	.db #0x00	; 0
   5751 00                  361 	.db #0x00	; 0
   5752 00                  362 	.db #0x00	; 0
   5753 00                  363 	.db #0x00	; 0
   5754 11                  364 	.db #0x11	; 17
   5755 22                  365 	.db #0x22	; 34
   5756 00                  366 	.db #0x00	; 0
   5757 22                  367 	.db #0x22	; 34
   5758 00                  368 	.db #0x00	; 0
   5759 00                  369 	.db #0x00	; 0
   575A 00                  370 	.db #0x00	; 0
   575B 00                  371 	.db #0x00	; 0
   575C 00                  372 	.db #0x00	; 0
   575D 00                  373 	.db #0x00	; 0
   575E 11                  374 	.db #0x11	; 17
   575F 22                  375 	.db #0x22	; 34
   5760 00                  376 	.db #0x00	; 0
   5761 22                  377 	.db #0x22	; 34
   5762 00                  378 	.db #0x00	; 0
   5763 00                  379 	.db #0x00	; 0
   5764 00                  380 	.db #0x00	; 0
   5765 00                  381 	.db #0x00	; 0
   5766 00                  382 	.db #0x00	; 0
   5767 00                  383 	.db #0x00	; 0
   5768 11                  384 	.db #0x11	; 17
   5769 22                  385 	.db #0x22	; 34
   576A 00                  386 	.db #0x00	; 0
   576B 22                  387 	.db #0x22	; 34
   576C 00                  388 	.db #0x00	; 0
   576D 00                  389 	.db #0x00	; 0
   576E 00                  390 	.db #0x00	; 0
   576F 00                  391 	.db #0x00	; 0
   5770 00                  392 	.db #0x00	; 0
   5771 00                  393 	.db #0x00	; 0
   5772 11                  394 	.db #0x11	; 17
   5773 22                  395 	.db #0x22	; 34
   5774 00                  396 	.db #0x00	; 0
   5775 22                  397 	.db #0x22	; 34
   5776 00                  398 	.db #0x00	; 0
   5777 00                  399 	.db #0x00	; 0
   5778 00                  400 	.db #0x00	; 0
   5779 00                  401 	.db #0x00	; 0
   577A 00                  402 	.db #0x00	; 0
   577B 00                  403 	.db #0x00	; 0
   577C 11                  404 	.db #0x11	; 17
   577D 33                  405 	.db #0x33	; 51	'3'
   577E 33                  406 	.db #0x33	; 51	'3'
   577F 33                  407 	.db #0x33	; 51	'3'
   5780 33                  408 	.db #0x33	; 51	'3'
   5781 33                  409 	.db #0x33	; 51	'3'
   5782 33                  410 	.db #0x33	; 51	'3'
   5783 33                  411 	.db #0x33	; 51	'3'
   5784 33                  412 	.db #0x33	; 51	'3'
   5785 33                  413 	.db #0x33	; 51	'3'
   5786 33                  414 	.db #0x33	; 51	'3'
   5787 22                  415 	.db #0x22	; 34
   5788 00                  416 	.db #0x00	; 0
   5789 22                  417 	.db #0x22	; 34
   578A 00                  418 	.db #0x00	; 0
   578B 00                  419 	.db #0x00	; 0
   578C 00                  420 	.db #0x00	; 0
   578D 00                  421 	.db #0x00	; 0
   578E 00                  422 	.db #0x00	; 0
   578F 00                  423 	.db #0x00	; 0
   5790 11                  424 	.db #0x11	; 17
   5791 22                  425 	.db #0x22	; 34
   5792 00                  426 	.db #0x00	; 0
   5793 22                  427 	.db #0x22	; 34
   5794 00                  428 	.db #0x00	; 0
   5795 00                  429 	.db #0x00	; 0
   5796 00                  430 	.db #0x00	; 0
   5797 00                  431 	.db #0x00	; 0
   5798 00                  432 	.db #0x00	; 0
   5799 00                  433 	.db #0x00	; 0
   579A 11                  434 	.db #0x11	; 17
   579B 22                  435 	.db #0x22	; 34
   579C 00                  436 	.db #0x00	; 0
   579D 22                  437 	.db #0x22	; 34
   579E 00                  438 	.db #0x00	; 0
   579F 00                  439 	.db #0x00	; 0
   57A0 00                  440 	.db #0x00	; 0
   57A1 00                  441 	.db #0x00	; 0
   57A2 00                  442 	.db #0x00	; 0
   57A3 00                  443 	.db #0x00	; 0
   57A4 11                  444 	.db #0x11	; 17
   57A5 22                  445 	.db #0x22	; 34
   57A6 00                  446 	.db #0x00	; 0
   57A7 22                  447 	.db #0x22	; 34
   57A8 00                  448 	.db #0x00	; 0
   57A9 00                  449 	.db #0x00	; 0
   57AA 00                  450 	.db #0x00	; 0
   57AB 00                  451 	.db #0x00	; 0
   57AC 00                  452 	.db #0x00	; 0
   57AD 00                  453 	.db #0x00	; 0
   57AE 11                  454 	.db #0x11	; 17
   57AF 22                  455 	.db #0x22	; 34
   57B0 00                  456 	.db #0x00	; 0
   57B1 22                  457 	.db #0x22	; 34
   57B2 00                  458 	.db #0x00	; 0
   57B3 00                  459 	.db #0x00	; 0
   57B4 00                  460 	.db #0x00	; 0
   57B5 00                  461 	.db #0x00	; 0
   57B6 00                  462 	.db #0x00	; 0
   57B7 00                  463 	.db #0x00	; 0
   57B8 11                  464 	.db #0x11	; 17
   57B9 22                  465 	.db #0x22	; 34
   57BA 00                  466 	.db #0x00	; 0
   57BB 22                  467 	.db #0x22	; 34
   57BC 00                  468 	.db #0x00	; 0
   57BD 00                  469 	.db #0x00	; 0
   57BE 00                  470 	.db #0x00	; 0
   57BF 00                  471 	.db #0x00	; 0
   57C0 00                  472 	.db #0x00	; 0
   57C1 00                  473 	.db #0x00	; 0
   57C2 11                  474 	.db #0x11	; 17
   57C3 22                  475 	.db #0x22	; 34
   57C4 00                  476 	.db #0x00	; 0
   57C5 22                  477 	.db #0x22	; 34
   57C6 00                  478 	.db #0x00	; 0
   57C7 00                  479 	.db #0x00	; 0
   57C8 00                  480 	.db #0x00	; 0
   57C9 00                  481 	.db #0x00	; 0
   57CA 00                  482 	.db #0x00	; 0
   57CB 00                  483 	.db #0x00	; 0
   57CC 11                  484 	.db #0x11	; 17
   57CD 33                  485 	.db #0x33	; 51	'3'
   57CE 33                  486 	.db #0x33	; 51	'3'
   57CF 33                  487 	.db #0x33	; 51	'3'
   57D0 33                  488 	.db #0x33	; 51	'3'
   57D1 33                  489 	.db #0x33	; 51	'3'
   57D2 33                  490 	.db #0x33	; 51	'3'
   57D3 33                  491 	.db #0x33	; 51	'3'
   57D4 33                  492 	.db #0x33	; 51	'3'
   57D5 33                  493 	.db #0x33	; 51	'3'
   57D6 33                  494 	.db #0x33	; 51	'3'
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   57D7                     499 _enemyspawn::
   57D7 DD E5         [15]  500 	push	ix
   57D9 DD 21 00 00   [14]  501 	ld	ix,#0
   57DD DD 39         [15]  502 	add	ix,sp
   57DF 21 F1 FF      [10]  503 	ld	hl, #-15
   57E2 39            [11]  504 	add	hl, sp
   57E3 F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   57E4 DD 7E 05      [19]  507 	ld	a, 5 (ix)
   57E7 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   57EA CA AA 59      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   57ED DD 7E 04      [19]  512 	ld	a, 4 (ix)
   57F0 DD 77 FE      [19]  513 	ld	-2 (ix), a
   57F3 DD 7E 05      [19]  514 	ld	a, 5 (ix)
   57F6 DD 77 FF      [19]  515 	ld	-1 (ix), a
   57F9 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   57FC DD 66 FF      [19]  517 	ld	h,-1 (ix)
   57FF DD 7E 06      [19]  518 	ld	a, 6 (ix)
   5802 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   5803 DD 4E FE      [19]  521 	ld	c,-2 (ix)
   5806 DD 46 FF      [19]  522 	ld	b,-1 (ix)
   5809 03            [ 6]  523 	inc	bc
   580A DD 7E 07      [19]  524 	ld	a, 7 (ix)
   580D 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   580E DD 7E FE      [19]  527 	ld	a, -2 (ix)
   5811 C6 02         [ 7]  528 	add	a, #0x02
   5813 DD 77 FC      [19]  529 	ld	-4 (ix), a
   5816 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5819 CE 00         [ 7]  531 	adc	a, #0x00
   581B DD 77 FD      [19]  532 	ld	-3 (ix), a
   581E DD 7E 09      [19]  533 	ld	a, 9 (ix)
   5821 B7            [ 4]  534 	or	a, a
   5822 28 04         [12]  535 	jr	Z,00114$
   5824 0E 01         [ 7]  536 	ld	c, #0x01
   5826 18 02         [12]  537 	jr	00115$
   5828                     538 00114$:
   5828 0E FF         [ 7]  539 	ld	c, #0xff
   582A                     540 00115$:
   582A DD 6E FC      [19]  541 	ld	l,-4 (ix)
   582D DD 66 FD      [19]  542 	ld	h,-3 (ix)
   5830 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   5831 DD 7E FE      [19]  545 	ld	a, -2 (ix)
   5834 C6 03         [ 7]  546 	add	a, #0x03
   5836 DD 77 FA      [19]  547 	ld	-6 (ix), a
   5839 DD 7E FF      [19]  548 	ld	a, -1 (ix)
   583C CE 00         [ 7]  549 	adc	a, #0x00
   583E DD 77 FB      [19]  550 	ld	-5 (ix), a
   5841 DD 6E FA      [19]  551 	ld	l,-6 (ix)
   5844 DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5847 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   5849 DD 7E FE      [19]  555 	ld	a, -2 (ix)
   584C C6 06         [ 7]  556 	add	a, #0x06
   584E DD 77 F8      [19]  557 	ld	-8 (ix), a
   5851 DD 7E FF      [19]  558 	ld	a, -1 (ix)
   5854 CE 00         [ 7]  559 	adc	a, #0x00
   5856 DD 77 F9      [19]  560 	ld	-7 (ix), a
   5859 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   585C DD 66 F9      [19]  562 	ld	h,-7 (ix)
   585F 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   5861 DD 7E FE      [19]  565 	ld	a, -2 (ix)
   5864 C6 09         [ 7]  566 	add	a, #0x09
   5866 DD 77 F8      [19]  567 	ld	-8 (ix), a
   5869 DD 7E FF      [19]  568 	ld	a, -1 (ix)
   586C CE 00         [ 7]  569 	adc	a, #0x00
   586E DD 77 F9      [19]  570 	ld	-7 (ix), a
   5871 DD 6E F8      [19]  571 	ld	l,-8 (ix)
   5874 DD 66 F9      [19]  572 	ld	h,-7 (ix)
   5877 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   587A 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   587B DD 7E FE      [19]  576 	ld	a, -2 (ix)
   587E C6 04         [ 7]  577 	add	a, #0x04
   5880 DD 77 F8      [19]  578 	ld	-8 (ix), a
   5883 DD 7E FF      [19]  579 	ld	a, -1 (ix)
   5886 CE 00         [ 7]  580 	adc	a, #0x00
   5888 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   588B DD 7E FE      [19]  583 	ld	a, -2 (ix)
   588E C6 05         [ 7]  584 	add	a, #0x05
   5890 DD 77 F6      [19]  585 	ld	-10 (ix), a
   5893 DD 7E FF      [19]  586 	ld	a, -1 (ix)
   5896 CE 00         [ 7]  587 	adc	a, #0x00
   5898 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   589B DD 7E FE      [19]  590 	ld	a, -2 (ix)
   589E C6 07         [ 7]  591 	add	a, #0x07
   58A0 DD 77 F4      [19]  592 	ld	-12 (ix), a
   58A3 DD 7E FF      [19]  593 	ld	a, -1 (ix)
   58A6 CE 00         [ 7]  594 	adc	a, #0x00
   58A8 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   58AB DD 7E FE      [19]  597 	ld	a, -2 (ix)
   58AE C6 08         [ 7]  598 	add	a, #0x08
   58B0 DD 77 FE      [19]  599 	ld	-2 (ix), a
   58B3 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   58B6 CE 00         [ 7]  601 	adc	a, #0x00
   58B8 DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   58BB DD 7E 08      [19]  604 	ld	a, 8 (ix)
   58BE 3D            [ 4]  605 	dec	a
   58BF 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   58C1 DD 6E F8      [19]  608 	ld	l,-8 (ix)
   58C4 DD 66 F9      [19]  609 	ld	h,-7 (ix)
   58C7 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   58C9 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   58CC DD 66 F7      [19]  613 	ld	h,-9 (ix)
   58CF 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   58D1 DD 6E F4      [19]  616 	ld	l,-12 (ix)
   58D4 DD 66 F5      [19]  617 	ld	h,-11 (ix)
   58D7 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   58D9 DD 6E FE      [19]  620 	ld	l,-2 (ix)
   58DC DD 66 FF      [19]  621 	ld	h,-1 (ix)
   58DF 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   58E1 DD 7E FC      [19]  624 	ld	a, -4 (ix)
   58E4 DD 77 F2      [19]  625 	ld	-14 (ix), a
   58E7 DD 7E FD      [19]  626 	ld	a, -3 (ix)
   58EA DD 77 F3      [19]  627 	ld	-13 (ix), a
   58ED DD 7E 09      [19]  628 	ld	a, 9 (ix)
   58F0 B7            [ 4]  629 	or	a, a
   58F1 28 06         [12]  630 	jr	Z,00116$
   58F3 DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   58F7 18 04         [12]  632 	jr	00117$
   58F9                     633 00116$:
   58F9 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   58FD                     635 00117$:
   58FD DD 6E F2      [19]  636 	ld	l,-14 (ix)
   5900 DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5903 DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5906 77            [ 7]  639 	ld	(hl), a
   5907 C3 AA 59      [10]  640 	jp	00112$
   590A                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   590A DD 7E 08      [19]  643 	ld	a, 8 (ix)
   590D D6 02         [ 7]  644 	sub	a, #0x02
   590F 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   5911 DD 6E F8      [19]  647 	ld	l,-8 (ix)
   5914 DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5917 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5919 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   591C DD 66 F7      [19]  652 	ld	h,-9 (ix)
   591F 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   5921 DD 6E F4      [19]  655 	ld	l,-12 (ix)
   5924 DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5927 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5929 DD 6E FE      [19]  659 	ld	l,-2 (ix)
   592C DD 66 FF      [19]  660 	ld	h,-1 (ix)
   592F 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   5931 DD 4E FA      [19]  663 	ld	c,-6 (ix)
   5934 DD 46 FB      [19]  664 	ld	b,-5 (ix)
   5937 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   593A B7            [ 4]  666 	or	a, a
   593B 28 04         [12]  667 	jr	Z,00118$
   593D 3E 01         [ 7]  668 	ld	a, #0x01
   593F 18 02         [12]  669 	jr	00119$
   5941                     670 00118$:
   5941 3E FF         [ 7]  671 	ld	a, #0xff
   5943                     672 00119$:
   5943 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   5944 DD 6E FC      [19]  675 	ld	l,-4 (ix)
   5947 DD 66 FD      [19]  676 	ld	h,-3 (ix)
   594A 36 01         [10]  677 	ld	(hl), #0x01
   594C 18 5C         [12]  678 	jr	00112$
   594E                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   594E DD 7E 08      [19]  681 	ld	a, 8 (ix)
   5951 D6 03         [ 7]  682 	sub	a, #0x03
   5953 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   5955 DD 6E F8      [19]  685 	ld	l,-8 (ix)
   5958 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   595B 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   595D DD 6E F6      [19]  689 	ld	l,-10 (ix)
   5960 DD 66 F7      [19]  690 	ld	h,-9 (ix)
   5963 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   5965 DD 6E F4      [19]  693 	ld	l,-12 (ix)
   5968 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   596B 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   596D DD 6E FE      [19]  697 	ld	l,-2 (ix)
   5970 DD 66 FF      [19]  698 	ld	h,-1 (ix)
   5973 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   5975 DD 4E FC      [19]  701 	ld	c,-4 (ix)
   5978 DD 46 FD      [19]  702 	ld	b,-3 (ix)
   597B DD 7E 09      [19]  703 	ld	a, 9 (ix)
   597E B7            [ 4]  704 	or	a, a
   597F 28 04         [12]  705 	jr	Z,00120$
   5981 3E 01         [ 7]  706 	ld	a, #0x01
   5983 18 02         [12]  707 	jr	00121$
   5985                     708 00120$:
   5985 3E FF         [ 7]  709 	ld	a, #0xff
   5987                     710 00121$:
   5987 02            [ 7]  711 	ld	(bc), a
   5988 18 20         [12]  712 	jr	00112$
   598A                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   598A DD 6E F8      [19]  715 	ld	l,-8 (ix)
   598D DD 66 F9      [19]  716 	ld	h,-7 (ix)
   5990 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   5992 DD 6E F6      [19]  719 	ld	l,-10 (ix)
   5995 DD 66 F7      [19]  720 	ld	h,-9 (ix)
   5998 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   599A DD 6E F4      [19]  723 	ld	l,-12 (ix)
   599D DD 66 F5      [19]  724 	ld	h,-11 (ix)
   59A0 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   59A2 DD 6E FE      [19]  727 	ld	l,-2 (ix)
   59A5 DD 66 FF      [19]  728 	ld	h,-1 (ix)
   59A8 36 64         [10]  729 	ld	(hl), #0x64
   59AA                     730 00112$:
   59AA DD F9         [10]  731 	ld	sp, ix
   59AC DD E1         [14]  732 	pop	ix
   59AE C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   59AF                     738 _enemyupdate::
   59AF DD E5         [15]  739 	push	ix
   59B1 DD 21 00 00   [14]  740 	ld	ix,#0
   59B5 DD 39         [15]  741 	add	ix,sp
   59B7 21 F6 FF      [10]  742 	ld	hl, #-10
   59BA 39            [11]  743 	add	hl, sp
   59BB F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   59BC DD 7E 05      [19]  746 	ld	a, 5 (ix)
   59BF DD B6 04      [19]  747 	or	a,4 (ix)
   59C2 CA B6 5B      [10]  748 	jp	Z,00121$
   59C5 DD 7E 04      [19]  749 	ld	a, 4 (ix)
   59C8 DD 77 FE      [19]  750 	ld	-2 (ix), a
   59CB DD 7E 05      [19]  751 	ld	a, 5 (ix)
   59CE DD 77 FF      [19]  752 	ld	-1 (ix), a
   59D1 DD 6E FE      [19]  753 	ld	l,-2 (ix)
   59D4 DD 66 FF      [19]  754 	ld	h,-1 (ix)
   59D7 11 06 00      [10]  755 	ld	de, #0x0006
   59DA 19            [11]  756 	add	hl, de
   59DB 7E            [ 7]  757 	ld	a, (hl)
   59DC B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   59DD CA B6 5B      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   59E0 DD 6E FE      [19]  762 	ld	l,-2 (ix)
   59E3 DD 66 FF      [19]  763 	ld	h,-1 (ix)
   59E6 11 09 00      [10]  764 	ld	de, #0x0009
   59E9 19            [11]  765 	add	hl, de
   59EA 7E            [ 7]  766 	ld	a, (hl)
   59EB DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   59EE DD 6E FE      [19]  769 	ld	l,-2 (ix)
   59F1 DD 66 FF      [19]  770 	ld	h,-1 (ix)
   59F4 4E            [ 7]  771 	ld	c, (hl)
   59F5 DD 7E FE      [19]  772 	ld	a, -2 (ix)
   59F8 C6 02         [ 7]  773 	add	a, #0x02
   59FA DD 77 FB      [19]  774 	ld	-5 (ix), a
   59FD DD 7E FF      [19]  775 	ld	a, -1 (ix)
   5A00 CE 00         [ 7]  776 	adc	a, #0x00
   5A02 DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5A05 DD 7E FE      [19]  779 	ld	a, -2 (ix)
   5A08 C6 01         [ 7]  780 	add	a, #0x01
   5A0A DD 77 F9      [19]  781 	ld	-7 (ix), a
   5A0D DD 7E FF      [19]  782 	ld	a, -1 (ix)
   5A10 CE 00         [ 7]  783 	adc	a, #0x00
   5A12 DD 77 FA      [19]  784 	ld	-6 (ix), a
   5A15 DD 5E FE      [19]  785 	ld	e,-2 (ix)
   5A18 DD 56 FF      [19]  786 	ld	d,-1 (ix)
   5A1B 13            [ 6]  787 	inc	de
   5A1C 13            [ 6]  788 	inc	de
   5A1D 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5A1E 06 00         [ 7]  791 	ld	b, #0x00
   5A20 DD 6E FB      [19]  792 	ld	l,-5 (ix)
   5A23 DD 66 FC      [19]  793 	ld	h,-4 (ix)
   5A26 7E            [ 7]  794 	ld	a, (hl)
   5A27 DD 77 F8      [19]  795 	ld	-8 (ix), a
   5A2A 6F            [ 4]  796 	ld	l, a
   5A2B DD 7E F8      [19]  797 	ld	a, -8 (ix)
   5A2E 17            [ 4]  798 	rla
   5A2F 9F            [ 4]  799 	sbc	a, a
   5A30 67            [ 4]  800 	ld	h, a
   5A31 09            [11]  801 	add	hl,bc
   5A32 4D            [ 4]  802 	ld	c, l
   5A33 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5A34 DD 7E FD      [19]  805 	ld	a, -3 (ix)
   5A37 D6 02         [ 7]  806 	sub	a, #0x02
   5A39 C2 E2 5A      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5A3C DD 6E F9      [19]  810 	ld	l,-7 (ix)
   5A3F DD 66 FA      [19]  811 	ld	h,-6 (ix)
   5A42 6E            [ 7]  812 	ld	l, (hl)
   5A43 DD 75 F6      [19]  813 	ld	-10 (ix), l
   5A46 DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   5A4A 1A            [ 7]  815 	ld	a, (de)
   5A4B 6F            [ 4]  816 	ld	l, a
   5A4C 17            [ 4]  817 	rla
   5A4D 9F            [ 4]  818 	sbc	a, a
   5A4E 67            [ 4]  819 	ld	h, a
   5A4F DD 7E F6      [19]  820 	ld	a, -10 (ix)
   5A52 85            [ 4]  821 	add	a, l
   5A53 DD 77 F6      [19]  822 	ld	-10 (ix), a
   5A56 DD 7E F7      [19]  823 	ld	a, -9 (ix)
   5A59 8C            [ 4]  824 	adc	a, h
   5A5A DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   5A5D 79            [ 4]  827 	ld	a, c
   5A5E D6 08         [ 7]  828 	sub	a, #0x08
   5A60 78            [ 4]  829 	ld	a, b
   5A61 17            [ 4]  830 	rla
   5A62 3F            [ 4]  831 	ccf
   5A63 1F            [ 4]  832 	rra
   5A64 DE 80         [ 7]  833 	sbc	a, #0x80
   5A66 38 0E         [12]  834 	jr	C,00104$
   5A68 3E 48         [ 7]  835 	ld	a, #0x48
   5A6A B9            [ 4]  836 	cp	a, c
   5A6B 3E 00         [ 7]  837 	ld	a, #0x00
   5A6D 98            [ 4]  838 	sbc	a, b
   5A6E E2 73 5A      [10]  839 	jp	PO, 00161$
   5A71 EE 80         [ 7]  840 	xor	a, #0x80
   5A73                     841 00161$:
   5A73 F2 91 5A      [10]  842 	jp	P, 00105$
   5A76                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   5A76 AF            [ 4]  845 	xor	a, a
   5A77 DD 96 F8      [19]  846 	sub	a, -8 (ix)
   5A7A 4F            [ 4]  847 	ld	c, a
   5A7B DD 6E FB      [19]  848 	ld	l,-5 (ix)
   5A7E DD 66 FC      [19]  849 	ld	h,-4 (ix)
   5A81 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   5A82 DD 6E FE      [19]  852 	ld	l,-2 (ix)
   5A85 DD 66 FF      [19]  853 	ld	h,-1 (ix)
   5A88 6E            [ 7]  854 	ld	l, (hl)
   5A89 26 00         [ 7]  855 	ld	h, #0x00
   5A8B 79            [ 4]  856 	ld	a, c
   5A8C 17            [ 4]  857 	rla
   5A8D 9F            [ 4]  858 	sbc	a, a
   5A8E 47            [ 4]  859 	ld	b, a
   5A8F 09            [11]  860 	add	hl,bc
   5A90 4D            [ 4]  861 	ld	c, l
   5A91                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   5A91 DD 7E F6      [19]  864 	ld	a, -10 (ix)
   5A94 D6 38         [ 7]  865 	sub	a, #0x38
   5A96 DD 7E F7      [19]  866 	ld	a, -9 (ix)
   5A99 17            [ 4]  867 	rla
   5A9A 3F            [ 4]  868 	ccf
   5A9B 1F            [ 4]  869 	rra
   5A9C DE 80         [ 7]  870 	sbc	a, #0x80
   5A9E 38 12         [12]  871 	jr	C,00107$
   5AA0 3E 78         [ 7]  872 	ld	a, #0x78
   5AA2 DD BE F6      [19]  873 	cp	a, -10 (ix)
   5AA5 3E 00         [ 7]  874 	ld	a, #0x00
   5AA7 DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   5AAA E2 AF 5A      [10]  876 	jp	PO, 00162$
   5AAD EE 80         [ 7]  877 	xor	a, #0x80
   5AAF                     878 00162$:
   5AAF F2 CE 5A      [10]  879 	jp	P, 00108$
   5AB2                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   5AB2 1A            [ 7]  882 	ld	a, (de)
   5AB3 6F            [ 4]  883 	ld	l, a
   5AB4 AF            [ 4]  884 	xor	a, a
   5AB5 95            [ 4]  885 	sub	a, l
   5AB6 DD 77 F8      [19]  886 	ld	-8 (ix), a
   5AB9 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   5ABA DD 6E F9      [19]  889 	ld	l,-7 (ix)
   5ABD DD 66 FA      [19]  890 	ld	h,-6 (ix)
   5AC0 5E            [ 7]  891 	ld	e, (hl)
   5AC1 16 00         [ 7]  892 	ld	d, #0x00
   5AC3 DD 6E F8      [19]  893 	ld	l, -8 (ix)
   5AC6 DD 7E F8      [19]  894 	ld	a, -8 (ix)
   5AC9 17            [ 4]  895 	rla
   5ACA 9F            [ 4]  896 	sbc	a, a
   5ACB 67            [ 4]  897 	ld	h, a
   5ACC 19            [11]  898 	add	hl,de
   5ACD E3            [19]  899 	ex	(sp), hl
   5ACE                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   5ACE DD 6E FE      [19]  902 	ld	l,-2 (ix)
   5AD1 DD 66 FF      [19]  903 	ld	h,-1 (ix)
   5AD4 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   5AD5 DD 4E F6      [19]  906 	ld	c, -10 (ix)
   5AD8 DD 6E F9      [19]  907 	ld	l,-7 (ix)
   5ADB DD 66 FA      [19]  908 	ld	h,-6 (ix)
   5ADE 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   5ADF C3 B6 5B      [10]  911 	jp	00121$
   5AE2                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   5AE2 79            [ 4]  915 	ld	a, c
   5AE3 D6 02         [ 7]  916 	sub	a, #0x02
   5AE5 78            [ 4]  917 	ld	a, b
   5AE6 17            [ 4]  918 	rla
   5AE7 3F            [ 4]  919 	ccf
   5AE8 1F            [ 4]  920 	rra
   5AE9 DE 80         [ 7]  921 	sbc	a, #0x80
   5AEB 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   5AED 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   5AF0 DD 6E FB      [19]  926 	ld	l,-5 (ix)
   5AF3 DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5AF6 36 01         [10]  928 	ld	(hl), #0x01
   5AF8                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5AF8 DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5AFB DD 66 FF      [19]  932 	ld	h,-1 (ix)
   5AFE 23            [ 6]  933 	inc	hl
   5AFF 23            [ 6]  934 	inc	hl
   5B00 23            [ 6]  935 	inc	hl
   5B01 23            [ 6]  936 	inc	hl
   5B02 6E            [ 7]  937 	ld	l, (hl)
   5B03 26 00         [ 7]  938 	ld	h, #0x00
   5B05 3E 50         [ 7]  939 	ld	a, #0x50
   5B07 95            [ 4]  940 	sub	a, l
   5B08 6F            [ 4]  941 	ld	l, a
   5B09 3E 00         [ 7]  942 	ld	a, #0x00
   5B0B 9C            [ 4]  943 	sbc	a, h
   5B0C 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5B0D 7D            [ 4]  946 	ld	a, l
   5B0E 91            [ 4]  947 	sub	a, c
   5B0F 7C            [ 4]  948 	ld	a, h
   5B10 98            [ 4]  949 	sbc	a, b
   5B11 E2 16 5B      [10]  950 	jp	PO, 00163$
   5B14 EE 80         [ 7]  951 	xor	a, #0x80
   5B16                     952 00163$:
   5B16 F2 22 5B      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5B19 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5B1A DD 6E FB      [19]  957 	ld	l,-5 (ix)
   5B1D DD 66 FC      [19]  958 	ld	h,-4 (ix)
   5B20 36 FF         [10]  959 	ld	(hl), #0xff
   5B22                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5B22 DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5B25 DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5B28 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5B29 1A            [ 7]  966 	ld	a, (de)
   5B2A 4F            [ 4]  967 	ld	c, a
   5B2B 0C            [ 4]  968 	inc	c
   5B2C 79            [ 4]  969 	ld	a, c
   5B2D 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   5B2E 3E 03         [ 7]  972 	ld	a, #0x03
   5B30 91            [ 4]  973 	sub	a, c
   5B31 E2 36 5B      [10]  974 	jp	PO, 00164$
   5B34 EE 80         [ 7]  975 	xor	a, #0x80
   5B36                     976 00164$:
   5B36 F2 3C 5B      [10]  977 	jp	P, 00117$
   5B39 3E 03         [ 7]  978 	ld	a, #0x03
   5B3B 12            [ 7]  979 	ld	(de), a
   5B3C                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   5B3C DD 6E F9      [19]  982 	ld	l,-7 (ix)
   5B3F DD 66 FA      [19]  983 	ld	h,-6 (ix)
   5B42 4E            [ 7]  984 	ld	c, (hl)
   5B43 06 00         [ 7]  985 	ld	b, #0x00
   5B45 1A            [ 7]  986 	ld	a, (de)
   5B46 6F            [ 4]  987 	ld	l, a
   5B47 17            [ 4]  988 	rla
   5B48 9F            [ 4]  989 	sbc	a, a
   5B49 67            [ 4]  990 	ld	h, a
   5B4A 09            [11]  991 	add	hl, bc
   5B4B E5            [11]  992 	push	hl
   5B4C FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5B4E DD 7E FE      [19]  995 	ld	a, -2 (ix)
   5B51 C6 05         [ 7]  996 	add	a, #0x05
   5B53 DD 77 F6      [19]  997 	ld	-10 (ix), a
   5B56 DD 7E FF      [19]  998 	ld	a, -1 (ix)
   5B59 CE 00         [ 7]  999 	adc	a, #0x00
   5B5B DD 77 F7      [19] 1000 	ld	-9 (ix), a
   5B5E E1            [10] 1001 	pop	hl
   5B5F E5            [11] 1002 	push	hl
   5B60 7E            [ 7] 1003 	ld	a, (hl)
   5B61 DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   5B64 DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   5B67 4E            [ 7] 1006 	ld	c, (hl)
   5B68 06 00         [ 7] 1007 	ld	b, #0x00
   5B6A D5            [11] 1008 	push	de
   5B6B F5            [11] 1009 	push	af
   5B6C 33            [ 6] 1010 	inc	sp
   5B6D FD E5         [15] 1011 	push	iy
   5B6F C5            [11] 1012 	push	bc
   5B70 CD 87 4D      [17] 1013 	call	_collision_clamp_y_at
   5B73 F1            [10] 1014 	pop	af
   5B74 F1            [10] 1015 	pop	af
   5B75 33            [ 6] 1016 	inc	sp
   5B76 4D            [ 4] 1017 	ld	c, l
   5B77 D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5B78 DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   5B7B DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   5B7E 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5B7F E1            [10] 1024 	pop	hl
   5B80 E5            [11] 1025 	push	hl
   5B81 7E            [ 7] 1026 	ld	a, (hl)
   5B82 06 00         [ 7] 1027 	ld	b, #0x00
   5B84 DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   5B87 DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   5B8A 6E            [ 7] 1030 	ld	l, (hl)
   5B8B DD 75 F6      [19] 1031 	ld	-10 (ix), l
   5B8E DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   5B92 D5            [11] 1033 	push	de
   5B93 F5            [11] 1034 	push	af
   5B94 33            [ 6] 1035 	inc	sp
   5B95 C5            [11] 1036 	push	bc
   5B96 DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5B99 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5B9C E5            [11] 1039 	push	hl
   5B9D CD 08 4D      [17] 1040 	call	_collision_is_on_ground_at
   5BA0 F1            [10] 1041 	pop	af
   5BA1 F1            [10] 1042 	pop	af
   5BA2 33            [ 6] 1043 	inc	sp
   5BA3 D1            [10] 1044 	pop	de
   5BA4 7D            [ 4] 1045 	ld	a, l
   5BA5 B7            [ 4] 1046 	or	a, a
   5BA6 28 0E         [12] 1047 	jr	Z,00121$
   5BA8 1A            [ 7] 1048 	ld	a, (de)
   5BA9 4F            [ 4] 1049 	ld	c, a
   5BAA AF            [ 4] 1050 	xor	a, a
   5BAB 91            [ 4] 1051 	sub	a, c
   5BAC E2 B1 5B      [10] 1052 	jp	PO, 00165$
   5BAF EE 80         [ 7] 1053 	xor	a, #0x80
   5BB1                    1054 00165$:
   5BB1 F2 B6 5B      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5BB4 AF            [ 4] 1057 	xor	a, a
   5BB5 12            [ 7] 1058 	ld	(de), a
   5BB6                    1059 00121$:
   5BB6 DD F9         [10] 1060 	ld	sp, ix
   5BB8 DD E1         [14] 1061 	pop	ix
   5BBA C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5BBB                    1067 _enemyrender::
   5BBB DD E5         [15] 1068 	push	ix
   5BBD DD 21 00 00   [14] 1069 	ld	ix,#0
   5BC1 DD 39         [15] 1070 	add	ix,sp
   5BC3 F5            [11] 1071 	push	af
   5BC4 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5BC5 DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5BC8 DD B6 04      [19] 1075 	or	a,4 (ix)
   5BCB CA 48 5C      [10] 1076 	jp	Z,00113$
   5BCE DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5BD1 DD 46 05      [19] 1078 	ld	b,5 (ix)
   5BD4 C5            [11] 1079 	push	bc
   5BD5 FD E1         [14] 1080 	pop	iy
   5BD7 FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5BDA B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5BDB 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5BDD C5            [11] 1086 	push	bc
   5BDE FD E1         [14] 1087 	pop	iy
   5BE0 FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5BE3 FE 03         [ 7] 1089 	cp	a, #0x03
   5BE5 20 0A         [12] 1090 	jr	NZ,00111$
   5BE7 DD 36 FE 23   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5BEB DD 36 FF 57   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5BEF 18 23         [12] 1093 	jr	00112$
   5BF1                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5BF1 FE 02         [ 7] 1096 	cp	a, #0x02
   5BF3 20 0A         [12] 1097 	jr	NZ,00108$
   5BF5 DD 36 FE E7   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5BF9 DD 36 FF 56   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5BFD 18 15         [12] 1100 	jr	00112$
   5BFF                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5BFF 3D            [ 4] 1103 	dec	a
   5C00 20 0A         [12] 1104 	jr	NZ,00105$
   5C02 DD 36 FE A1   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5C06 DD 36 FF 56   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5C0A 18 08         [12] 1107 	jr	00112$
   5C0C                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5C0C DD 36 FE 61   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5C10 DD 36 FF 56   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5C14                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5C14 69            [ 4] 1114 	ld	l, c
   5C15 60            [ 4] 1115 	ld	h, b
   5C16 23            [ 6] 1116 	inc	hl
   5C17 56            [ 7] 1117 	ld	d, (hl)
   5C18 0A            [ 7] 1118 	ld	a, (bc)
   5C19 C5            [11] 1119 	push	bc
   5C1A 5F            [ 4] 1120 	ld	e, a
   5C1B D5            [11] 1121 	push	de
   5C1C 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5C1F E5            [11] 1123 	push	hl
   5C20 CD 39 64      [17] 1124 	call	_cpct_getScreenPtr
   5C23 EB            [ 4] 1125 	ex	de,hl
   5C24 C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5C25 C5            [11] 1128 	push	bc
   5C26 FD E1         [14] 1129 	pop	iy
   5C28 FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5C2B DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5C2E 69            [ 4] 1132 	ld	l, c
   5C2F 60            [ 4] 1133 	ld	h, b
   5C30 01 04 00      [10] 1134 	ld	bc, #0x0004
   5C33 09            [11] 1135 	add	hl, bc
   5C34 4E            [ 7] 1136 	ld	c, (hl)
   5C35 D5            [11] 1137 	push	de
   5C36 FD E1         [14] 1138 	pop	iy
   5C38 DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5C3B DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5C3E DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5C41 C5            [11] 1142 	push	bc
   5C42 FD E5         [15] 1143 	push	iy
   5C44 D5            [11] 1144 	push	de
   5C45 CD 6A 62      [17] 1145 	call	_cpct_drawSprite
   5C48                    1146 00113$:
   5C48 DD F9         [10] 1147 	ld	sp, ix
   5C4A DD E1         [14] 1148 	pop	ix
   5C4C C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5C4D                    1154 _enemydamage::
   5C4D DD E5         [15] 1155 	push	ix
   5C4F DD 21 00 00   [14] 1156 	ld	ix,#0
   5C53 DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5C55 DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5C58 DD B6 04      [19] 1160 	or	a,4 (ix)
   5C5B 28 0F         [12] 1161 	jr	Z,00101$
   5C5D DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5C60 DD 46 05      [19] 1163 	ld	b,5 (ix)
   5C63 21 06 00      [10] 1164 	ld	hl, #0x0006
   5C66 09            [11] 1165 	add	hl,bc
   5C67 EB            [ 4] 1166 	ex	de,hl
   5C68 1A            [ 7] 1167 	ld	a, (de)
   5C69 B7            [ 4] 1168 	or	a, a
   5C6A 20 04         [12] 1169 	jr	NZ,00102$
   5C6C                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5C6C 2E 00         [ 7] 1172 	ld	l, #0x00
   5C6E 18 1A         [12] 1173 	jr	00106$
   5C70                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5C70 21 07 00      [10] 1176 	ld	hl, #0x0007
   5C73 09            [11] 1177 	add	hl, bc
   5C74 4E            [ 7] 1178 	ld	c, (hl)
   5C75 DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5C78 91            [ 4] 1180 	sub	a, c
   5C79 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5C7B 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5C7D AF            [ 4] 1185 	xor	a, a
   5C7E 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5C7F 2E 01         [ 7] 1188 	ld	l, #0x01
   5C81 18 07         [12] 1189 	jr	00106$
   5C83                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5C83 79            [ 4] 1192 	ld	a, c
   5C84 DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5C87 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5C88 2E 00         [ 7] 1196 	ld	l, #0x00
   5C8A                    1197 00106$:
   5C8A DD E1         [14] 1198 	pop	ix
   5C8C C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
