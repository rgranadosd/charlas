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
   55A1                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   55A1 21 03 00      [10]   57 	ld	hl, #2+1
   55A4 39            [11]   58 	add	hl, sp
   55A5 7E            [ 7]   59 	ld	a, (hl)
   55A6 2B            [ 6]   60 	dec	hl
   55A7 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   55A8 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   55A9 D1            [10]   65 	pop	de
   55AA C1            [10]   66 	pop	bc
   55AB C5            [11]   67 	push	bc
   55AC D5            [11]   68 	push	de
   55AD AF            [ 4]   69 	xor	a, a
   55AE 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   55AF 59            [ 4]   72 	ld	e, c
   55B0 50            [ 4]   73 	ld	d, b
   55B1 13            [ 6]   74 	inc	de
   55B2 AF            [ 4]   75 	xor	a, a
   55B3 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   55B4 59            [ 4]   78 	ld	e, c
   55B5 50            [ 4]   79 	ld	d, b
   55B6 13            [ 6]   80 	inc	de
   55B7 13            [ 6]   81 	inc	de
   55B8 AF            [ 4]   82 	xor	a, a
   55B9 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   55BA 59            [ 4]   85 	ld	e, c
   55BB 50            [ 4]   86 	ld	d, b
   55BC 13            [ 6]   87 	inc	de
   55BD 13            [ 6]   88 	inc	de
   55BE 13            [ 6]   89 	inc	de
   55BF AF            [ 4]   90 	xor	a, a
   55C0 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   55C1 21 04 00      [10]   93 	ld	hl, #0x0004
   55C4 09            [11]   94 	add	hl, bc
   55C5 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   55C7 21 05 00      [10]   97 	ld	hl, #0x0005
   55CA 09            [11]   98 	add	hl, bc
   55CB 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   55CD 21 06 00      [10]  101 	ld	hl, #0x0006
   55D0 09            [11]  102 	add	hl, bc
   55D1 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   55D3 21 07 00      [10]  105 	ld	hl, #0x0007
   55D6 09            [11]  106 	add	hl, bc
   55D7 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   55D9 21 08 00      [10]  109 	ld	hl, #0x0008
   55DC 09            [11]  110 	add	hl, bc
   55DD 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   55DF 21 09 00      [10]  113 	ld	hl, #0x0009
   55E2 09            [11]  114 	add	hl, bc
   55E3 36 00         [10]  115 	ld	(hl), #0x00
   55E5 C9            [10]  116 	ret
   55E6                     117 _enemy_kind0_sprite:
   55E6 30                  118 	.db #0x30	; 48	'0'
   55E7 30                  119 	.db #0x30	; 48	'0'
   55E8 30                  120 	.db #0x30	; 48	'0'
   55E9 30                  121 	.db #0x30	; 48	'0'
   55EA 30                  122 	.db #0x30	; 48	'0'
   55EB 00                  123 	.db #0x00	; 0
   55EC 00                  124 	.db #0x00	; 0
   55ED 10                  125 	.db #0x10	; 16
   55EE 30                  126 	.db #0x30	; 48	'0'
   55EF 00                  127 	.db #0x00	; 0
   55F0 00                  128 	.db #0x00	; 0
   55F1 10                  129 	.db #0x10	; 16
   55F2 30                  130 	.db #0x30	; 48	'0'
   55F3 00                  131 	.db #0x00	; 0
   55F4 00                  132 	.db #0x00	; 0
   55F5 10                  133 	.db #0x10	; 16
   55F6 30                  134 	.db #0x30	; 48	'0'
   55F7 00                  135 	.db #0x00	; 0
   55F8 00                  136 	.db #0x00	; 0
   55F9 10                  137 	.db #0x10	; 16
   55FA 30                  138 	.db #0x30	; 48	'0'
   55FB 00                  139 	.db #0x00	; 0
   55FC 00                  140 	.db #0x00	; 0
   55FD 10                  141 	.db #0x10	; 16
   55FE 30                  142 	.db #0x30	; 48	'0'
   55FF 00                  143 	.db #0x00	; 0
   5600 00                  144 	.db #0x00	; 0
   5601 10                  145 	.db #0x10	; 16
   5602 30                  146 	.db #0x30	; 48	'0'
   5603 00                  147 	.db #0x00	; 0
   5604 00                  148 	.db #0x00	; 0
   5605 10                  149 	.db #0x10	; 16
   5606 30                  150 	.db #0x30	; 48	'0'
   5607 30                  151 	.db #0x30	; 48	'0'
   5608 30                  152 	.db #0x30	; 48	'0'
   5609 30                  153 	.db #0x30	; 48	'0'
   560A 30                  154 	.db #0x30	; 48	'0'
   560B 00                  155 	.db #0x00	; 0
   560C 00                  156 	.db #0x00	; 0
   560D 10                  157 	.db #0x10	; 16
   560E 30                  158 	.db #0x30	; 48	'0'
   560F 00                  159 	.db #0x00	; 0
   5610 00                  160 	.db #0x00	; 0
   5611 10                  161 	.db #0x10	; 16
   5612 30                  162 	.db #0x30	; 48	'0'
   5613 00                  163 	.db #0x00	; 0
   5614 00                  164 	.db #0x00	; 0
   5615 10                  165 	.db #0x10	; 16
   5616 30                  166 	.db #0x30	; 48	'0'
   5617 00                  167 	.db #0x00	; 0
   5618 00                  168 	.db #0x00	; 0
   5619 10                  169 	.db #0x10	; 16
   561A 30                  170 	.db #0x30	; 48	'0'
   561B 00                  171 	.db #0x00	; 0
   561C 00                  172 	.db #0x00	; 0
   561D 10                  173 	.db #0x10	; 16
   561E 30                  174 	.db #0x30	; 48	'0'
   561F 00                  175 	.db #0x00	; 0
   5620 00                  176 	.db #0x00	; 0
   5621 10                  177 	.db #0x10	; 16
   5622 30                  178 	.db #0x30	; 48	'0'
   5623 30                  179 	.db #0x30	; 48	'0'
   5624 30                  180 	.db #0x30	; 48	'0'
   5625 30                  181 	.db #0x30	; 48	'0'
   5626                     182 _enemy_kind1_sprite:
   5626 3F                  183 	.db #0x3f	; 63
   5627 3F                  184 	.db #0x3f	; 63
   5628 3F                  185 	.db #0x3f	; 63
   5629 3F                  186 	.db #0x3f	; 63
   562A 3F                  187 	.db #0x3f	; 63
   562B 2A                  188 	.db #0x2a	; 42
   562C 2A                  189 	.db #0x2a	; 42
   562D 00                  190 	.db #0x00	; 0
   562E 00                  191 	.db #0x00	; 0
   562F 15                  192 	.db #0x15	; 21
   5630 2A                  193 	.db #0x2a	; 42
   5631 2A                  194 	.db #0x2a	; 42
   5632 00                  195 	.db #0x00	; 0
   5633 00                  196 	.db #0x00	; 0
   5634 15                  197 	.db #0x15	; 21
   5635 2A                  198 	.db #0x2a	; 42
   5636 2A                  199 	.db #0x2a	; 42
   5637 00                  200 	.db #0x00	; 0
   5638 00                  201 	.db #0x00	; 0
   5639 15                  202 	.db #0x15	; 21
   563A 2A                  203 	.db #0x2a	; 42
   563B 2A                  204 	.db #0x2a	; 42
   563C 00                  205 	.db #0x00	; 0
   563D 00                  206 	.db #0x00	; 0
   563E 15                  207 	.db #0x15	; 21
   563F 2A                  208 	.db #0x2a	; 42
   5640 2A                  209 	.db #0x2a	; 42
   5641 00                  210 	.db #0x00	; 0
   5642 00                  211 	.db #0x00	; 0
   5643 15                  212 	.db #0x15	; 21
   5644 2A                  213 	.db #0x2a	; 42
   5645 2A                  214 	.db #0x2a	; 42
   5646 00                  215 	.db #0x00	; 0
   5647 00                  216 	.db #0x00	; 0
   5648 15                  217 	.db #0x15	; 21
   5649 3F                  218 	.db #0x3f	; 63
   564A 3F                  219 	.db #0x3f	; 63
   564B 3F                  220 	.db #0x3f	; 63
   564C 3F                  221 	.db #0x3f	; 63
   564D 3F                  222 	.db #0x3f	; 63
   564E 2A                  223 	.db #0x2a	; 42
   564F 2A                  224 	.db #0x2a	; 42
   5650 00                  225 	.db #0x00	; 0
   5651 00                  226 	.db #0x00	; 0
   5652 15                  227 	.db #0x15	; 21
   5653 2A                  228 	.db #0x2a	; 42
   5654 2A                  229 	.db #0x2a	; 42
   5655 00                  230 	.db #0x00	; 0
   5656 00                  231 	.db #0x00	; 0
   5657 15                  232 	.db #0x15	; 21
   5658 2A                  233 	.db #0x2a	; 42
   5659 2A                  234 	.db #0x2a	; 42
   565A 00                  235 	.db #0x00	; 0
   565B 00                  236 	.db #0x00	; 0
   565C 15                  237 	.db #0x15	; 21
   565D 2A                  238 	.db #0x2a	; 42
   565E 2A                  239 	.db #0x2a	; 42
   565F 00                  240 	.db #0x00	; 0
   5660 00                  241 	.db #0x00	; 0
   5661 15                  242 	.db #0x15	; 21
   5662 2A                  243 	.db #0x2a	; 42
   5663 2A                  244 	.db #0x2a	; 42
   5664 00                  245 	.db #0x00	; 0
   5665 00                  246 	.db #0x00	; 0
   5666 15                  247 	.db #0x15	; 21
   5667 3F                  248 	.db #0x3f	; 63
   5668 3F                  249 	.db #0x3f	; 63
   5669 3F                  250 	.db #0x3f	; 63
   566A 3F                  251 	.db #0x3f	; 63
   566B 3F                  252 	.db #0x3f	; 63
   566C                     253 _enemy_kind2_sprite:
   566C 0F                  254 	.db #0x0f	; 15
   566D 0F                  255 	.db #0x0f	; 15
   566E 0F                  256 	.db #0x0f	; 15
   566F 0F                  257 	.db #0x0f	; 15
   5670 0F                  258 	.db #0x0f	; 15
   5671 0F                  259 	.db #0x0f	; 15
   5672 0A                  260 	.db #0x0a	; 10
   5673 05                  261 	.db #0x05	; 5
   5674 00                  262 	.db #0x00	; 0
   5675 00                  263 	.db #0x00	; 0
   5676 00                  264 	.db #0x00	; 0
   5677 05                  265 	.db #0x05	; 5
   5678 0A                  266 	.db #0x0a	; 10
   5679 05                  267 	.db #0x05	; 5
   567A 00                  268 	.db #0x00	; 0
   567B 00                  269 	.db #0x00	; 0
   567C 00                  270 	.db #0x00	; 0
   567D 05                  271 	.db #0x05	; 5
   567E 0A                  272 	.db #0x0a	; 10
   567F 05                  273 	.db #0x05	; 5
   5680 00                  274 	.db #0x00	; 0
   5681 00                  275 	.db #0x00	; 0
   5682 00                  276 	.db #0x00	; 0
   5683 05                  277 	.db #0x05	; 5
   5684 0A                  278 	.db #0x0a	; 10
   5685 05                  279 	.db #0x05	; 5
   5686 00                  280 	.db #0x00	; 0
   5687 00                  281 	.db #0x00	; 0
   5688 00                  282 	.db #0x00	; 0
   5689 05                  283 	.db #0x05	; 5
   568A 0F                  284 	.db #0x0f	; 15
   568B 0F                  285 	.db #0x0f	; 15
   568C 0F                  286 	.db #0x0f	; 15
   568D 0F                  287 	.db #0x0f	; 15
   568E 0F                  288 	.db #0x0f	; 15
   568F 0F                  289 	.db #0x0f	; 15
   5690 0A                  290 	.db #0x0a	; 10
   5691 05                  291 	.db #0x05	; 5
   5692 00                  292 	.db #0x00	; 0
   5693 00                  293 	.db #0x00	; 0
   5694 00                  294 	.db #0x00	; 0
   5695 05                  295 	.db #0x05	; 5
   5696 0A                  296 	.db #0x0a	; 10
   5697 05                  297 	.db #0x05	; 5
   5698 00                  298 	.db #0x00	; 0
   5699 00                  299 	.db #0x00	; 0
   569A 00                  300 	.db #0x00	; 0
   569B 05                  301 	.db #0x05	; 5
   569C 0A                  302 	.db #0x0a	; 10
   569D 05                  303 	.db #0x05	; 5
   569E 00                  304 	.db #0x00	; 0
   569F 00                  305 	.db #0x00	; 0
   56A0 00                  306 	.db #0x00	; 0
   56A1 05                  307 	.db #0x05	; 5
   56A2 0F                  308 	.db #0x0f	; 15
   56A3 0F                  309 	.db #0x0f	; 15
   56A4 0F                  310 	.db #0x0f	; 15
   56A5 0F                  311 	.db #0x0f	; 15
   56A6 0F                  312 	.db #0x0f	; 15
   56A7 0F                  313 	.db #0x0f	; 15
   56A8                     314 _enemy_kind3_sprite:
   56A8 33                  315 	.db #0x33	; 51	'3'
   56A9 33                  316 	.db #0x33	; 51	'3'
   56AA 33                  317 	.db #0x33	; 51	'3'
   56AB 33                  318 	.db #0x33	; 51	'3'
   56AC 33                  319 	.db #0x33	; 51	'3'
   56AD 33                  320 	.db #0x33	; 51	'3'
   56AE 33                  321 	.db #0x33	; 51	'3'
   56AF 33                  322 	.db #0x33	; 51	'3'
   56B0 33                  323 	.db #0x33	; 51	'3'
   56B1 33                  324 	.db #0x33	; 51	'3'
   56B2 22                  325 	.db #0x22	; 34
   56B3 00                  326 	.db #0x00	; 0
   56B4 22                  327 	.db #0x22	; 34
   56B5 00                  328 	.db #0x00	; 0
   56B6 00                  329 	.db #0x00	; 0
   56B7 00                  330 	.db #0x00	; 0
   56B8 00                  331 	.db #0x00	; 0
   56B9 00                  332 	.db #0x00	; 0
   56BA 00                  333 	.db #0x00	; 0
   56BB 11                  334 	.db #0x11	; 17
   56BC 22                  335 	.db #0x22	; 34
   56BD 00                  336 	.db #0x00	; 0
   56BE 22                  337 	.db #0x22	; 34
   56BF 00                  338 	.db #0x00	; 0
   56C0 00                  339 	.db #0x00	; 0
   56C1 00                  340 	.db #0x00	; 0
   56C2 00                  341 	.db #0x00	; 0
   56C3 00                  342 	.db #0x00	; 0
   56C4 00                  343 	.db #0x00	; 0
   56C5 11                  344 	.db #0x11	; 17
   56C6 22                  345 	.db #0x22	; 34
   56C7 00                  346 	.db #0x00	; 0
   56C8 22                  347 	.db #0x22	; 34
   56C9 00                  348 	.db #0x00	; 0
   56CA 00                  349 	.db #0x00	; 0
   56CB 00                  350 	.db #0x00	; 0
   56CC 00                  351 	.db #0x00	; 0
   56CD 00                  352 	.db #0x00	; 0
   56CE 00                  353 	.db #0x00	; 0
   56CF 11                  354 	.db #0x11	; 17
   56D0 22                  355 	.db #0x22	; 34
   56D1 00                  356 	.db #0x00	; 0
   56D2 22                  357 	.db #0x22	; 34
   56D3 00                  358 	.db #0x00	; 0
   56D4 00                  359 	.db #0x00	; 0
   56D5 00                  360 	.db #0x00	; 0
   56D6 00                  361 	.db #0x00	; 0
   56D7 00                  362 	.db #0x00	; 0
   56D8 00                  363 	.db #0x00	; 0
   56D9 11                  364 	.db #0x11	; 17
   56DA 22                  365 	.db #0x22	; 34
   56DB 00                  366 	.db #0x00	; 0
   56DC 22                  367 	.db #0x22	; 34
   56DD 00                  368 	.db #0x00	; 0
   56DE 00                  369 	.db #0x00	; 0
   56DF 00                  370 	.db #0x00	; 0
   56E0 00                  371 	.db #0x00	; 0
   56E1 00                  372 	.db #0x00	; 0
   56E2 00                  373 	.db #0x00	; 0
   56E3 11                  374 	.db #0x11	; 17
   56E4 22                  375 	.db #0x22	; 34
   56E5 00                  376 	.db #0x00	; 0
   56E6 22                  377 	.db #0x22	; 34
   56E7 00                  378 	.db #0x00	; 0
   56E8 00                  379 	.db #0x00	; 0
   56E9 00                  380 	.db #0x00	; 0
   56EA 00                  381 	.db #0x00	; 0
   56EB 00                  382 	.db #0x00	; 0
   56EC 00                  383 	.db #0x00	; 0
   56ED 11                  384 	.db #0x11	; 17
   56EE 22                  385 	.db #0x22	; 34
   56EF 00                  386 	.db #0x00	; 0
   56F0 22                  387 	.db #0x22	; 34
   56F1 00                  388 	.db #0x00	; 0
   56F2 00                  389 	.db #0x00	; 0
   56F3 00                  390 	.db #0x00	; 0
   56F4 00                  391 	.db #0x00	; 0
   56F5 00                  392 	.db #0x00	; 0
   56F6 00                  393 	.db #0x00	; 0
   56F7 11                  394 	.db #0x11	; 17
   56F8 22                  395 	.db #0x22	; 34
   56F9 00                  396 	.db #0x00	; 0
   56FA 22                  397 	.db #0x22	; 34
   56FB 00                  398 	.db #0x00	; 0
   56FC 00                  399 	.db #0x00	; 0
   56FD 00                  400 	.db #0x00	; 0
   56FE 00                  401 	.db #0x00	; 0
   56FF 00                  402 	.db #0x00	; 0
   5700 00                  403 	.db #0x00	; 0
   5701 11                  404 	.db #0x11	; 17
   5702 33                  405 	.db #0x33	; 51	'3'
   5703 33                  406 	.db #0x33	; 51	'3'
   5704 33                  407 	.db #0x33	; 51	'3'
   5705 33                  408 	.db #0x33	; 51	'3'
   5706 33                  409 	.db #0x33	; 51	'3'
   5707 33                  410 	.db #0x33	; 51	'3'
   5708 33                  411 	.db #0x33	; 51	'3'
   5709 33                  412 	.db #0x33	; 51	'3'
   570A 33                  413 	.db #0x33	; 51	'3'
   570B 33                  414 	.db #0x33	; 51	'3'
   570C 22                  415 	.db #0x22	; 34
   570D 00                  416 	.db #0x00	; 0
   570E 22                  417 	.db #0x22	; 34
   570F 00                  418 	.db #0x00	; 0
   5710 00                  419 	.db #0x00	; 0
   5711 00                  420 	.db #0x00	; 0
   5712 00                  421 	.db #0x00	; 0
   5713 00                  422 	.db #0x00	; 0
   5714 00                  423 	.db #0x00	; 0
   5715 11                  424 	.db #0x11	; 17
   5716 22                  425 	.db #0x22	; 34
   5717 00                  426 	.db #0x00	; 0
   5718 22                  427 	.db #0x22	; 34
   5719 00                  428 	.db #0x00	; 0
   571A 00                  429 	.db #0x00	; 0
   571B 00                  430 	.db #0x00	; 0
   571C 00                  431 	.db #0x00	; 0
   571D 00                  432 	.db #0x00	; 0
   571E 00                  433 	.db #0x00	; 0
   571F 11                  434 	.db #0x11	; 17
   5720 22                  435 	.db #0x22	; 34
   5721 00                  436 	.db #0x00	; 0
   5722 22                  437 	.db #0x22	; 34
   5723 00                  438 	.db #0x00	; 0
   5724 00                  439 	.db #0x00	; 0
   5725 00                  440 	.db #0x00	; 0
   5726 00                  441 	.db #0x00	; 0
   5727 00                  442 	.db #0x00	; 0
   5728 00                  443 	.db #0x00	; 0
   5729 11                  444 	.db #0x11	; 17
   572A 22                  445 	.db #0x22	; 34
   572B 00                  446 	.db #0x00	; 0
   572C 22                  447 	.db #0x22	; 34
   572D 00                  448 	.db #0x00	; 0
   572E 00                  449 	.db #0x00	; 0
   572F 00                  450 	.db #0x00	; 0
   5730 00                  451 	.db #0x00	; 0
   5731 00                  452 	.db #0x00	; 0
   5732 00                  453 	.db #0x00	; 0
   5733 11                  454 	.db #0x11	; 17
   5734 22                  455 	.db #0x22	; 34
   5735 00                  456 	.db #0x00	; 0
   5736 22                  457 	.db #0x22	; 34
   5737 00                  458 	.db #0x00	; 0
   5738 00                  459 	.db #0x00	; 0
   5739 00                  460 	.db #0x00	; 0
   573A 00                  461 	.db #0x00	; 0
   573B 00                  462 	.db #0x00	; 0
   573C 00                  463 	.db #0x00	; 0
   573D 11                  464 	.db #0x11	; 17
   573E 22                  465 	.db #0x22	; 34
   573F 00                  466 	.db #0x00	; 0
   5740 22                  467 	.db #0x22	; 34
   5741 00                  468 	.db #0x00	; 0
   5742 00                  469 	.db #0x00	; 0
   5743 00                  470 	.db #0x00	; 0
   5744 00                  471 	.db #0x00	; 0
   5745 00                  472 	.db #0x00	; 0
   5746 00                  473 	.db #0x00	; 0
   5747 11                  474 	.db #0x11	; 17
   5748 22                  475 	.db #0x22	; 34
   5749 00                  476 	.db #0x00	; 0
   574A 22                  477 	.db #0x22	; 34
   574B 00                  478 	.db #0x00	; 0
   574C 00                  479 	.db #0x00	; 0
   574D 00                  480 	.db #0x00	; 0
   574E 00                  481 	.db #0x00	; 0
   574F 00                  482 	.db #0x00	; 0
   5750 00                  483 	.db #0x00	; 0
   5751 11                  484 	.db #0x11	; 17
   5752 33                  485 	.db #0x33	; 51	'3'
   5753 33                  486 	.db #0x33	; 51	'3'
   5754 33                  487 	.db #0x33	; 51	'3'
   5755 33                  488 	.db #0x33	; 51	'3'
   5756 33                  489 	.db #0x33	; 51	'3'
   5757 33                  490 	.db #0x33	; 51	'3'
   5758 33                  491 	.db #0x33	; 51	'3'
   5759 33                  492 	.db #0x33	; 51	'3'
   575A 33                  493 	.db #0x33	; 51	'3'
   575B 33                  494 	.db #0x33	; 51	'3'
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   575C                     499 _enemyspawn::
   575C DD E5         [15]  500 	push	ix
   575E DD 21 00 00   [14]  501 	ld	ix,#0
   5762 DD 39         [15]  502 	add	ix,sp
   5764 21 F1 FF      [10]  503 	ld	hl, #-15
   5767 39            [11]  504 	add	hl, sp
   5768 F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   5769 DD 7E 05      [19]  507 	ld	a, 5 (ix)
   576C DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   576F CA 2F 59      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   5772 DD 7E 04      [19]  512 	ld	a, 4 (ix)
   5775 DD 77 FE      [19]  513 	ld	-2 (ix), a
   5778 DD 7E 05      [19]  514 	ld	a, 5 (ix)
   577B DD 77 FF      [19]  515 	ld	-1 (ix), a
   577E DD 6E FE      [19]  516 	ld	l,-2 (ix)
   5781 DD 66 FF      [19]  517 	ld	h,-1 (ix)
   5784 DD 7E 06      [19]  518 	ld	a, 6 (ix)
   5787 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   5788 DD 4E FE      [19]  521 	ld	c,-2 (ix)
   578B DD 46 FF      [19]  522 	ld	b,-1 (ix)
   578E 03            [ 6]  523 	inc	bc
   578F DD 7E 07      [19]  524 	ld	a, 7 (ix)
   5792 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   5793 DD 7E FE      [19]  527 	ld	a, -2 (ix)
   5796 C6 02         [ 7]  528 	add	a, #0x02
   5798 DD 77 FC      [19]  529 	ld	-4 (ix), a
   579B DD 7E FF      [19]  530 	ld	a, -1 (ix)
   579E CE 00         [ 7]  531 	adc	a, #0x00
   57A0 DD 77 FD      [19]  532 	ld	-3 (ix), a
   57A3 DD 7E 09      [19]  533 	ld	a, 9 (ix)
   57A6 B7            [ 4]  534 	or	a, a
   57A7 28 04         [12]  535 	jr	Z,00114$
   57A9 0E 01         [ 7]  536 	ld	c, #0x01
   57AB 18 02         [12]  537 	jr	00115$
   57AD                     538 00114$:
   57AD 0E FF         [ 7]  539 	ld	c, #0xff
   57AF                     540 00115$:
   57AF DD 6E FC      [19]  541 	ld	l,-4 (ix)
   57B2 DD 66 FD      [19]  542 	ld	h,-3 (ix)
   57B5 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   57B6 DD 7E FE      [19]  545 	ld	a, -2 (ix)
   57B9 C6 03         [ 7]  546 	add	a, #0x03
   57BB DD 77 FA      [19]  547 	ld	-6 (ix), a
   57BE DD 7E FF      [19]  548 	ld	a, -1 (ix)
   57C1 CE 00         [ 7]  549 	adc	a, #0x00
   57C3 DD 77 FB      [19]  550 	ld	-5 (ix), a
   57C6 DD 6E FA      [19]  551 	ld	l,-6 (ix)
   57C9 DD 66 FB      [19]  552 	ld	h,-5 (ix)
   57CC 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   57CE DD 7E FE      [19]  555 	ld	a, -2 (ix)
   57D1 C6 06         [ 7]  556 	add	a, #0x06
   57D3 DD 77 F8      [19]  557 	ld	-8 (ix), a
   57D6 DD 7E FF      [19]  558 	ld	a, -1 (ix)
   57D9 CE 00         [ 7]  559 	adc	a, #0x00
   57DB DD 77 F9      [19]  560 	ld	-7 (ix), a
   57DE DD 6E F8      [19]  561 	ld	l,-8 (ix)
   57E1 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   57E4 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   57E6 DD 7E FE      [19]  565 	ld	a, -2 (ix)
   57E9 C6 09         [ 7]  566 	add	a, #0x09
   57EB DD 77 F8      [19]  567 	ld	-8 (ix), a
   57EE DD 7E FF      [19]  568 	ld	a, -1 (ix)
   57F1 CE 00         [ 7]  569 	adc	a, #0x00
   57F3 DD 77 F9      [19]  570 	ld	-7 (ix), a
   57F6 DD 6E F8      [19]  571 	ld	l,-8 (ix)
   57F9 DD 66 F9      [19]  572 	ld	h,-7 (ix)
   57FC DD 7E 08      [19]  573 	ld	a, 8 (ix)
   57FF 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   5800 DD 7E FE      [19]  576 	ld	a, -2 (ix)
   5803 C6 04         [ 7]  577 	add	a, #0x04
   5805 DD 77 F8      [19]  578 	ld	-8 (ix), a
   5808 DD 7E FF      [19]  579 	ld	a, -1 (ix)
   580B CE 00         [ 7]  580 	adc	a, #0x00
   580D DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   5810 DD 7E FE      [19]  583 	ld	a, -2 (ix)
   5813 C6 05         [ 7]  584 	add	a, #0x05
   5815 DD 77 F6      [19]  585 	ld	-10 (ix), a
   5818 DD 7E FF      [19]  586 	ld	a, -1 (ix)
   581B CE 00         [ 7]  587 	adc	a, #0x00
   581D DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   5820 DD 7E FE      [19]  590 	ld	a, -2 (ix)
   5823 C6 07         [ 7]  591 	add	a, #0x07
   5825 DD 77 F4      [19]  592 	ld	-12 (ix), a
   5828 DD 7E FF      [19]  593 	ld	a, -1 (ix)
   582B CE 00         [ 7]  594 	adc	a, #0x00
   582D DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   5830 DD 7E FE      [19]  597 	ld	a, -2 (ix)
   5833 C6 08         [ 7]  598 	add	a, #0x08
   5835 DD 77 FE      [19]  599 	ld	-2 (ix), a
   5838 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   583B CE 00         [ 7]  601 	adc	a, #0x00
   583D DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   5840 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   5843 3D            [ 4]  605 	dec	a
   5844 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   5846 DD 6E F8      [19]  608 	ld	l,-8 (ix)
   5849 DD 66 F9      [19]  609 	ld	h,-7 (ix)
   584C 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   584E DD 6E F6      [19]  612 	ld	l,-10 (ix)
   5851 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   5854 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   5856 DD 6E F4      [19]  616 	ld	l,-12 (ix)
   5859 DD 66 F5      [19]  617 	ld	h,-11 (ix)
   585C 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   585E DD 6E FE      [19]  620 	ld	l,-2 (ix)
   5861 DD 66 FF      [19]  621 	ld	h,-1 (ix)
   5864 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   5866 DD 7E FC      [19]  624 	ld	a, -4 (ix)
   5869 DD 77 F2      [19]  625 	ld	-14 (ix), a
   586C DD 7E FD      [19]  626 	ld	a, -3 (ix)
   586F DD 77 F3      [19]  627 	ld	-13 (ix), a
   5872 DD 7E 09      [19]  628 	ld	a, 9 (ix)
   5875 B7            [ 4]  629 	or	a, a
   5876 28 06         [12]  630 	jr	Z,00116$
   5878 DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   587C 18 04         [12]  632 	jr	00117$
   587E                     633 00116$:
   587E DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5882                     635 00117$:
   5882 DD 6E F2      [19]  636 	ld	l,-14 (ix)
   5885 DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5888 DD 7E F1      [19]  638 	ld	a, -15 (ix)
   588B 77            [ 7]  639 	ld	(hl), a
   588C C3 2F 59      [10]  640 	jp	00112$
   588F                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   588F DD 7E 08      [19]  643 	ld	a, 8 (ix)
   5892 D6 02         [ 7]  644 	sub	a, #0x02
   5894 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   5896 DD 6E F8      [19]  647 	ld	l,-8 (ix)
   5899 DD 66 F9      [19]  648 	ld	h,-7 (ix)
   589C 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   589E DD 6E F6      [19]  651 	ld	l,-10 (ix)
   58A1 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   58A4 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   58A6 DD 6E F4      [19]  655 	ld	l,-12 (ix)
   58A9 DD 66 F5      [19]  656 	ld	h,-11 (ix)
   58AC 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   58AE DD 6E FE      [19]  659 	ld	l,-2 (ix)
   58B1 DD 66 FF      [19]  660 	ld	h,-1 (ix)
   58B4 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   58B6 DD 4E FA      [19]  663 	ld	c,-6 (ix)
   58B9 DD 46 FB      [19]  664 	ld	b,-5 (ix)
   58BC DD 7E 09      [19]  665 	ld	a, 9 (ix)
   58BF B7            [ 4]  666 	or	a, a
   58C0 28 04         [12]  667 	jr	Z,00118$
   58C2 3E 01         [ 7]  668 	ld	a, #0x01
   58C4 18 02         [12]  669 	jr	00119$
   58C6                     670 00118$:
   58C6 3E FF         [ 7]  671 	ld	a, #0xff
   58C8                     672 00119$:
   58C8 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   58C9 DD 6E FC      [19]  675 	ld	l,-4 (ix)
   58CC DD 66 FD      [19]  676 	ld	h,-3 (ix)
   58CF 36 01         [10]  677 	ld	(hl), #0x01
   58D1 18 5C         [12]  678 	jr	00112$
   58D3                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   58D3 DD 7E 08      [19]  681 	ld	a, 8 (ix)
   58D6 D6 03         [ 7]  682 	sub	a, #0x03
   58D8 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   58DA DD 6E F8      [19]  685 	ld	l,-8 (ix)
   58DD DD 66 F9      [19]  686 	ld	h,-7 (ix)
   58E0 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   58E2 DD 6E F6      [19]  689 	ld	l,-10 (ix)
   58E5 DD 66 F7      [19]  690 	ld	h,-9 (ix)
   58E8 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   58EA DD 6E F4      [19]  693 	ld	l,-12 (ix)
   58ED DD 66 F5      [19]  694 	ld	h,-11 (ix)
   58F0 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   58F2 DD 6E FE      [19]  697 	ld	l,-2 (ix)
   58F5 DD 66 FF      [19]  698 	ld	h,-1 (ix)
   58F8 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   58FA DD 4E FC      [19]  701 	ld	c,-4 (ix)
   58FD DD 46 FD      [19]  702 	ld	b,-3 (ix)
   5900 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   5903 B7            [ 4]  704 	or	a, a
   5904 28 04         [12]  705 	jr	Z,00120$
   5906 3E 01         [ 7]  706 	ld	a, #0x01
   5908 18 02         [12]  707 	jr	00121$
   590A                     708 00120$:
   590A 3E FF         [ 7]  709 	ld	a, #0xff
   590C                     710 00121$:
   590C 02            [ 7]  711 	ld	(bc), a
   590D 18 20         [12]  712 	jr	00112$
   590F                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   590F DD 6E F8      [19]  715 	ld	l,-8 (ix)
   5912 DD 66 F9      [19]  716 	ld	h,-7 (ix)
   5915 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   5917 DD 6E F6      [19]  719 	ld	l,-10 (ix)
   591A DD 66 F7      [19]  720 	ld	h,-9 (ix)
   591D 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   591F DD 6E F4      [19]  723 	ld	l,-12 (ix)
   5922 DD 66 F5      [19]  724 	ld	h,-11 (ix)
   5925 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   5927 DD 6E FE      [19]  727 	ld	l,-2 (ix)
   592A DD 66 FF      [19]  728 	ld	h,-1 (ix)
   592D 36 64         [10]  729 	ld	(hl), #0x64
   592F                     730 00112$:
   592F DD F9         [10]  731 	ld	sp, ix
   5931 DD E1         [14]  732 	pop	ix
   5933 C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   5934                     738 _enemyupdate::
   5934 DD E5         [15]  739 	push	ix
   5936 DD 21 00 00   [14]  740 	ld	ix,#0
   593A DD 39         [15]  741 	add	ix,sp
   593C 21 F6 FF      [10]  742 	ld	hl, #-10
   593F 39            [11]  743 	add	hl, sp
   5940 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   5941 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   5944 DD B6 04      [19]  747 	or	a,4 (ix)
   5947 CA 3B 5B      [10]  748 	jp	Z,00121$
   594A DD 7E 04      [19]  749 	ld	a, 4 (ix)
   594D DD 77 FE      [19]  750 	ld	-2 (ix), a
   5950 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   5953 DD 77 FF      [19]  752 	ld	-1 (ix), a
   5956 DD 6E FE      [19]  753 	ld	l,-2 (ix)
   5959 DD 66 FF      [19]  754 	ld	h,-1 (ix)
   595C 11 06 00      [10]  755 	ld	de, #0x0006
   595F 19            [11]  756 	add	hl, de
   5960 7E            [ 7]  757 	ld	a, (hl)
   5961 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   5962 CA 3B 5B      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5965 DD 6E FE      [19]  762 	ld	l,-2 (ix)
   5968 DD 66 FF      [19]  763 	ld	h,-1 (ix)
   596B 11 09 00      [10]  764 	ld	de, #0x0009
   596E 19            [11]  765 	add	hl, de
   596F 7E            [ 7]  766 	ld	a, (hl)
   5970 DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5973 DD 6E FE      [19]  769 	ld	l,-2 (ix)
   5976 DD 66 FF      [19]  770 	ld	h,-1 (ix)
   5979 4E            [ 7]  771 	ld	c, (hl)
   597A DD 7E FE      [19]  772 	ld	a, -2 (ix)
   597D C6 02         [ 7]  773 	add	a, #0x02
   597F DD 77 FB      [19]  774 	ld	-5 (ix), a
   5982 DD 7E FF      [19]  775 	ld	a, -1 (ix)
   5985 CE 00         [ 7]  776 	adc	a, #0x00
   5987 DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   598A DD 7E FE      [19]  779 	ld	a, -2 (ix)
   598D C6 01         [ 7]  780 	add	a, #0x01
   598F DD 77 F9      [19]  781 	ld	-7 (ix), a
   5992 DD 7E FF      [19]  782 	ld	a, -1 (ix)
   5995 CE 00         [ 7]  783 	adc	a, #0x00
   5997 DD 77 FA      [19]  784 	ld	-6 (ix), a
   599A DD 5E FE      [19]  785 	ld	e,-2 (ix)
   599D DD 56 FF      [19]  786 	ld	d,-1 (ix)
   59A0 13            [ 6]  787 	inc	de
   59A1 13            [ 6]  788 	inc	de
   59A2 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   59A3 06 00         [ 7]  791 	ld	b, #0x00
   59A5 DD 6E FB      [19]  792 	ld	l,-5 (ix)
   59A8 DD 66 FC      [19]  793 	ld	h,-4 (ix)
   59AB 7E            [ 7]  794 	ld	a, (hl)
   59AC DD 77 F8      [19]  795 	ld	-8 (ix), a
   59AF 6F            [ 4]  796 	ld	l, a
   59B0 DD 7E F8      [19]  797 	ld	a, -8 (ix)
   59B3 17            [ 4]  798 	rla
   59B4 9F            [ 4]  799 	sbc	a, a
   59B5 67            [ 4]  800 	ld	h, a
   59B6 09            [11]  801 	add	hl,bc
   59B7 4D            [ 4]  802 	ld	c, l
   59B8 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   59B9 DD 7E FD      [19]  805 	ld	a, -3 (ix)
   59BC D6 02         [ 7]  806 	sub	a, #0x02
   59BE C2 67 5A      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   59C1 DD 6E F9      [19]  810 	ld	l,-7 (ix)
   59C4 DD 66 FA      [19]  811 	ld	h,-6 (ix)
   59C7 6E            [ 7]  812 	ld	l, (hl)
   59C8 DD 75 F6      [19]  813 	ld	-10 (ix), l
   59CB DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   59CF 1A            [ 7]  815 	ld	a, (de)
   59D0 6F            [ 4]  816 	ld	l, a
   59D1 17            [ 4]  817 	rla
   59D2 9F            [ 4]  818 	sbc	a, a
   59D3 67            [ 4]  819 	ld	h, a
   59D4 DD 7E F6      [19]  820 	ld	a, -10 (ix)
   59D7 85            [ 4]  821 	add	a, l
   59D8 DD 77 F6      [19]  822 	ld	-10 (ix), a
   59DB DD 7E F7      [19]  823 	ld	a, -9 (ix)
   59DE 8C            [ 4]  824 	adc	a, h
   59DF DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   59E2 79            [ 4]  827 	ld	a, c
   59E3 D6 08         [ 7]  828 	sub	a, #0x08
   59E5 78            [ 4]  829 	ld	a, b
   59E6 17            [ 4]  830 	rla
   59E7 3F            [ 4]  831 	ccf
   59E8 1F            [ 4]  832 	rra
   59E9 DE 80         [ 7]  833 	sbc	a, #0x80
   59EB 38 0E         [12]  834 	jr	C,00104$
   59ED 3E 48         [ 7]  835 	ld	a, #0x48
   59EF B9            [ 4]  836 	cp	a, c
   59F0 3E 00         [ 7]  837 	ld	a, #0x00
   59F2 98            [ 4]  838 	sbc	a, b
   59F3 E2 F8 59      [10]  839 	jp	PO, 00161$
   59F6 EE 80         [ 7]  840 	xor	a, #0x80
   59F8                     841 00161$:
   59F8 F2 16 5A      [10]  842 	jp	P, 00105$
   59FB                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   59FB AF            [ 4]  845 	xor	a, a
   59FC DD 96 F8      [19]  846 	sub	a, -8 (ix)
   59FF 4F            [ 4]  847 	ld	c, a
   5A00 DD 6E FB      [19]  848 	ld	l,-5 (ix)
   5A03 DD 66 FC      [19]  849 	ld	h,-4 (ix)
   5A06 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   5A07 DD 6E FE      [19]  852 	ld	l,-2 (ix)
   5A0A DD 66 FF      [19]  853 	ld	h,-1 (ix)
   5A0D 6E            [ 7]  854 	ld	l, (hl)
   5A0E 26 00         [ 7]  855 	ld	h, #0x00
   5A10 79            [ 4]  856 	ld	a, c
   5A11 17            [ 4]  857 	rla
   5A12 9F            [ 4]  858 	sbc	a, a
   5A13 47            [ 4]  859 	ld	b, a
   5A14 09            [11]  860 	add	hl,bc
   5A15 4D            [ 4]  861 	ld	c, l
   5A16                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   5A16 DD 7E F6      [19]  864 	ld	a, -10 (ix)
   5A19 D6 38         [ 7]  865 	sub	a, #0x38
   5A1B DD 7E F7      [19]  866 	ld	a, -9 (ix)
   5A1E 17            [ 4]  867 	rla
   5A1F 3F            [ 4]  868 	ccf
   5A20 1F            [ 4]  869 	rra
   5A21 DE 80         [ 7]  870 	sbc	a, #0x80
   5A23 38 12         [12]  871 	jr	C,00107$
   5A25 3E 78         [ 7]  872 	ld	a, #0x78
   5A27 DD BE F6      [19]  873 	cp	a, -10 (ix)
   5A2A 3E 00         [ 7]  874 	ld	a, #0x00
   5A2C DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   5A2F E2 34 5A      [10]  876 	jp	PO, 00162$
   5A32 EE 80         [ 7]  877 	xor	a, #0x80
   5A34                     878 00162$:
   5A34 F2 53 5A      [10]  879 	jp	P, 00108$
   5A37                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   5A37 1A            [ 7]  882 	ld	a, (de)
   5A38 6F            [ 4]  883 	ld	l, a
   5A39 AF            [ 4]  884 	xor	a, a
   5A3A 95            [ 4]  885 	sub	a, l
   5A3B DD 77 F8      [19]  886 	ld	-8 (ix), a
   5A3E 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   5A3F DD 6E F9      [19]  889 	ld	l,-7 (ix)
   5A42 DD 66 FA      [19]  890 	ld	h,-6 (ix)
   5A45 5E            [ 7]  891 	ld	e, (hl)
   5A46 16 00         [ 7]  892 	ld	d, #0x00
   5A48 DD 6E F8      [19]  893 	ld	l, -8 (ix)
   5A4B DD 7E F8      [19]  894 	ld	a, -8 (ix)
   5A4E 17            [ 4]  895 	rla
   5A4F 9F            [ 4]  896 	sbc	a, a
   5A50 67            [ 4]  897 	ld	h, a
   5A51 19            [11]  898 	add	hl,de
   5A52 E3            [19]  899 	ex	(sp), hl
   5A53                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   5A53 DD 6E FE      [19]  902 	ld	l,-2 (ix)
   5A56 DD 66 FF      [19]  903 	ld	h,-1 (ix)
   5A59 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   5A5A DD 4E F6      [19]  906 	ld	c, -10 (ix)
   5A5D DD 6E F9      [19]  907 	ld	l,-7 (ix)
   5A60 DD 66 FA      [19]  908 	ld	h,-6 (ix)
   5A63 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   5A64 C3 3B 5B      [10]  911 	jp	00121$
   5A67                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   5A67 79            [ 4]  915 	ld	a, c
   5A68 D6 02         [ 7]  916 	sub	a, #0x02
   5A6A 78            [ 4]  917 	ld	a, b
   5A6B 17            [ 4]  918 	rla
   5A6C 3F            [ 4]  919 	ccf
   5A6D 1F            [ 4]  920 	rra
   5A6E DE 80         [ 7]  921 	sbc	a, #0x80
   5A70 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   5A72 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   5A75 DD 6E FB      [19]  926 	ld	l,-5 (ix)
   5A78 DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5A7B 36 01         [10]  928 	ld	(hl), #0x01
   5A7D                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5A7D DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5A80 DD 66 FF      [19]  932 	ld	h,-1 (ix)
   5A83 23            [ 6]  933 	inc	hl
   5A84 23            [ 6]  934 	inc	hl
   5A85 23            [ 6]  935 	inc	hl
   5A86 23            [ 6]  936 	inc	hl
   5A87 6E            [ 7]  937 	ld	l, (hl)
   5A88 26 00         [ 7]  938 	ld	h, #0x00
   5A8A 3E 50         [ 7]  939 	ld	a, #0x50
   5A8C 95            [ 4]  940 	sub	a, l
   5A8D 6F            [ 4]  941 	ld	l, a
   5A8E 3E 00         [ 7]  942 	ld	a, #0x00
   5A90 9C            [ 4]  943 	sbc	a, h
   5A91 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5A92 7D            [ 4]  946 	ld	a, l
   5A93 91            [ 4]  947 	sub	a, c
   5A94 7C            [ 4]  948 	ld	a, h
   5A95 98            [ 4]  949 	sbc	a, b
   5A96 E2 9B 5A      [10]  950 	jp	PO, 00163$
   5A99 EE 80         [ 7]  951 	xor	a, #0x80
   5A9B                     952 00163$:
   5A9B F2 A7 5A      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5A9E 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5A9F DD 6E FB      [19]  957 	ld	l,-5 (ix)
   5AA2 DD 66 FC      [19]  958 	ld	h,-4 (ix)
   5AA5 36 FF         [10]  959 	ld	(hl), #0xff
   5AA7                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5AA7 DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5AAA DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5AAD 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5AAE 1A            [ 7]  966 	ld	a, (de)
   5AAF 4F            [ 4]  967 	ld	c, a
   5AB0 0C            [ 4]  968 	inc	c
   5AB1 79            [ 4]  969 	ld	a, c
   5AB2 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   5AB3 3E 03         [ 7]  972 	ld	a, #0x03
   5AB5 91            [ 4]  973 	sub	a, c
   5AB6 E2 BB 5A      [10]  974 	jp	PO, 00164$
   5AB9 EE 80         [ 7]  975 	xor	a, #0x80
   5ABB                     976 00164$:
   5ABB F2 C1 5A      [10]  977 	jp	P, 00117$
   5ABE 3E 03         [ 7]  978 	ld	a, #0x03
   5AC0 12            [ 7]  979 	ld	(de), a
   5AC1                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   5AC1 DD 6E F9      [19]  982 	ld	l,-7 (ix)
   5AC4 DD 66 FA      [19]  983 	ld	h,-6 (ix)
   5AC7 4E            [ 7]  984 	ld	c, (hl)
   5AC8 06 00         [ 7]  985 	ld	b, #0x00
   5ACA 1A            [ 7]  986 	ld	a, (de)
   5ACB 6F            [ 4]  987 	ld	l, a
   5ACC 17            [ 4]  988 	rla
   5ACD 9F            [ 4]  989 	sbc	a, a
   5ACE 67            [ 4]  990 	ld	h, a
   5ACF 09            [11]  991 	add	hl, bc
   5AD0 E5            [11]  992 	push	hl
   5AD1 FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5AD3 DD 7E FE      [19]  995 	ld	a, -2 (ix)
   5AD6 C6 05         [ 7]  996 	add	a, #0x05
   5AD8 DD 77 F6      [19]  997 	ld	-10 (ix), a
   5ADB DD 7E FF      [19]  998 	ld	a, -1 (ix)
   5ADE CE 00         [ 7]  999 	adc	a, #0x00
   5AE0 DD 77 F7      [19] 1000 	ld	-9 (ix), a
   5AE3 E1            [10] 1001 	pop	hl
   5AE4 E5            [11] 1002 	push	hl
   5AE5 7E            [ 7] 1003 	ld	a, (hl)
   5AE6 DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   5AE9 DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   5AEC 4E            [ 7] 1006 	ld	c, (hl)
   5AED 06 00         [ 7] 1007 	ld	b, #0x00
   5AEF D5            [11] 1008 	push	de
   5AF0 F5            [11] 1009 	push	af
   5AF1 33            [ 6] 1010 	inc	sp
   5AF2 FD E5         [15] 1011 	push	iy
   5AF4 C5            [11] 1012 	push	bc
   5AF5 CD 7A 4D      [17] 1013 	call	_collision_clamp_y_at
   5AF8 F1            [10] 1014 	pop	af
   5AF9 F1            [10] 1015 	pop	af
   5AFA 33            [ 6] 1016 	inc	sp
   5AFB 4D            [ 4] 1017 	ld	c, l
   5AFC D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5AFD DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   5B00 DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   5B03 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5B04 E1            [10] 1024 	pop	hl
   5B05 E5            [11] 1025 	push	hl
   5B06 7E            [ 7] 1026 	ld	a, (hl)
   5B07 06 00         [ 7] 1027 	ld	b, #0x00
   5B09 DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   5B0C DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   5B0F 6E            [ 7] 1030 	ld	l, (hl)
   5B10 DD 75 F6      [19] 1031 	ld	-10 (ix), l
   5B13 DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   5B17 D5            [11] 1033 	push	de
   5B18 F5            [11] 1034 	push	af
   5B19 33            [ 6] 1035 	inc	sp
   5B1A C5            [11] 1036 	push	bc
   5B1B DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5B1E DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5B21 E5            [11] 1039 	push	hl
   5B22 CD FB 4C      [17] 1040 	call	_collision_is_on_ground_at
   5B25 F1            [10] 1041 	pop	af
   5B26 F1            [10] 1042 	pop	af
   5B27 33            [ 6] 1043 	inc	sp
   5B28 D1            [10] 1044 	pop	de
   5B29 7D            [ 4] 1045 	ld	a, l
   5B2A B7            [ 4] 1046 	or	a, a
   5B2B 28 0E         [12] 1047 	jr	Z,00121$
   5B2D 1A            [ 7] 1048 	ld	a, (de)
   5B2E 4F            [ 4] 1049 	ld	c, a
   5B2F AF            [ 4] 1050 	xor	a, a
   5B30 91            [ 4] 1051 	sub	a, c
   5B31 E2 36 5B      [10] 1052 	jp	PO, 00165$
   5B34 EE 80         [ 7] 1053 	xor	a, #0x80
   5B36                    1054 00165$:
   5B36 F2 3B 5B      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5B39 AF            [ 4] 1057 	xor	a, a
   5B3A 12            [ 7] 1058 	ld	(de), a
   5B3B                    1059 00121$:
   5B3B DD F9         [10] 1060 	ld	sp, ix
   5B3D DD E1         [14] 1061 	pop	ix
   5B3F C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5B40                    1067 _enemyrender::
   5B40 DD E5         [15] 1068 	push	ix
   5B42 DD 21 00 00   [14] 1069 	ld	ix,#0
   5B46 DD 39         [15] 1070 	add	ix,sp
   5B48 F5            [11] 1071 	push	af
   5B49 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5B4A DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5B4D DD B6 04      [19] 1075 	or	a,4 (ix)
   5B50 CA CD 5B      [10] 1076 	jp	Z,00113$
   5B53 DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5B56 DD 46 05      [19] 1078 	ld	b,5 (ix)
   5B59 C5            [11] 1079 	push	bc
   5B5A FD E1         [14] 1080 	pop	iy
   5B5C FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5B5F B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5B60 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5B62 C5            [11] 1086 	push	bc
   5B63 FD E1         [14] 1087 	pop	iy
   5B65 FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5B68 FE 03         [ 7] 1089 	cp	a, #0x03
   5B6A 20 0A         [12] 1090 	jr	NZ,00111$
   5B6C DD 36 FE A8   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5B70 DD 36 FF 56   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5B74 18 23         [12] 1093 	jr	00112$
   5B76                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5B76 FE 02         [ 7] 1096 	cp	a, #0x02
   5B78 20 0A         [12] 1097 	jr	NZ,00108$
   5B7A DD 36 FE 6C   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5B7E DD 36 FF 56   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5B82 18 15         [12] 1100 	jr	00112$
   5B84                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5B84 3D            [ 4] 1103 	dec	a
   5B85 20 0A         [12] 1104 	jr	NZ,00105$
   5B87 DD 36 FE 26   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5B8B DD 36 FF 56   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5B8F 18 08         [12] 1107 	jr	00112$
   5B91                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5B91 DD 36 FE E6   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5B95 DD 36 FF 55   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5B99                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5B99 69            [ 4] 1114 	ld	l, c
   5B9A 60            [ 4] 1115 	ld	h, b
   5B9B 23            [ 6] 1116 	inc	hl
   5B9C 56            [ 7] 1117 	ld	d, (hl)
   5B9D 0A            [ 7] 1118 	ld	a, (bc)
   5B9E C5            [11] 1119 	push	bc
   5B9F 5F            [ 4] 1120 	ld	e, a
   5BA0 D5            [11] 1121 	push	de
   5BA1 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5BA4 E5            [11] 1123 	push	hl
   5BA5 CD BB 63      [17] 1124 	call	_cpct_getScreenPtr
   5BA8 EB            [ 4] 1125 	ex	de,hl
   5BA9 C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5BAA C5            [11] 1128 	push	bc
   5BAB FD E1         [14] 1129 	pop	iy
   5BAD FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5BB0 DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5BB3 69            [ 4] 1132 	ld	l, c
   5BB4 60            [ 4] 1133 	ld	h, b
   5BB5 01 04 00      [10] 1134 	ld	bc, #0x0004
   5BB8 09            [11] 1135 	add	hl, bc
   5BB9 4E            [ 7] 1136 	ld	c, (hl)
   5BBA D5            [11] 1137 	push	de
   5BBB FD E1         [14] 1138 	pop	iy
   5BBD DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5BC0 DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5BC3 DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5BC6 C5            [11] 1142 	push	bc
   5BC7 FD E5         [15] 1143 	push	iy
   5BC9 D5            [11] 1144 	push	de
   5BCA CD EC 61      [17] 1145 	call	_cpct_drawSprite
   5BCD                    1146 00113$:
   5BCD DD F9         [10] 1147 	ld	sp, ix
   5BCF DD E1         [14] 1148 	pop	ix
   5BD1 C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5BD2                    1154 _enemydamage::
   5BD2 DD E5         [15] 1155 	push	ix
   5BD4 DD 21 00 00   [14] 1156 	ld	ix,#0
   5BD8 DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5BDA DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5BDD DD B6 04      [19] 1160 	or	a,4 (ix)
   5BE0 28 0F         [12] 1161 	jr	Z,00101$
   5BE2 DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5BE5 DD 46 05      [19] 1163 	ld	b,5 (ix)
   5BE8 21 06 00      [10] 1164 	ld	hl, #0x0006
   5BEB 09            [11] 1165 	add	hl,bc
   5BEC EB            [ 4] 1166 	ex	de,hl
   5BED 1A            [ 7] 1167 	ld	a, (de)
   5BEE B7            [ 4] 1168 	or	a, a
   5BEF 20 04         [12] 1169 	jr	NZ,00102$
   5BF1                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5BF1 2E 00         [ 7] 1172 	ld	l, #0x00
   5BF3 18 1A         [12] 1173 	jr	00106$
   5BF5                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5BF5 21 07 00      [10] 1176 	ld	hl, #0x0007
   5BF8 09            [11] 1177 	add	hl, bc
   5BF9 4E            [ 7] 1178 	ld	c, (hl)
   5BFA DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5BFD 91            [ 4] 1180 	sub	a, c
   5BFE 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5C00 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5C02 AF            [ 4] 1185 	xor	a, a
   5C03 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5C04 2E 01         [ 7] 1188 	ld	l, #0x01
   5C06 18 07         [12] 1189 	jr	00106$
   5C08                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5C08 79            [ 4] 1192 	ld	a, c
   5C09 DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5C0C 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5C0D 2E 00         [ 7] 1196 	ld	l, #0x00
   5C0F                    1197 00106$:
   5C0F DD E1         [14] 1198 	pop	ix
   5C11 C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
