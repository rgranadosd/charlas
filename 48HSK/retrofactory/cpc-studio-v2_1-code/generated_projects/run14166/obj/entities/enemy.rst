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
   5427                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   5427 21 03 00      [10]   57 	ld	hl, #2+1
   542A 39            [11]   58 	add	hl, sp
   542B 7E            [ 7]   59 	ld	a, (hl)
   542C 2B            [ 6]   60 	dec	hl
   542D B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   542E C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   542F D1            [10]   65 	pop	de
   5430 C1            [10]   66 	pop	bc
   5431 C5            [11]   67 	push	bc
   5432 D5            [11]   68 	push	de
   5433 AF            [ 4]   69 	xor	a, a
   5434 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   5435 59            [ 4]   72 	ld	e, c
   5436 50            [ 4]   73 	ld	d, b
   5437 13            [ 6]   74 	inc	de
   5438 AF            [ 4]   75 	xor	a, a
   5439 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   543A 59            [ 4]   78 	ld	e, c
   543B 50            [ 4]   79 	ld	d, b
   543C 13            [ 6]   80 	inc	de
   543D 13            [ 6]   81 	inc	de
   543E AF            [ 4]   82 	xor	a, a
   543F 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   5440 59            [ 4]   85 	ld	e, c
   5441 50            [ 4]   86 	ld	d, b
   5442 13            [ 6]   87 	inc	de
   5443 13            [ 6]   88 	inc	de
   5444 13            [ 6]   89 	inc	de
   5445 AF            [ 4]   90 	xor	a, a
   5446 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   5447 21 04 00      [10]   93 	ld	hl, #0x0004
   544A 09            [11]   94 	add	hl, bc
   544B 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   544D 21 05 00      [10]   97 	ld	hl, #0x0005
   5450 09            [11]   98 	add	hl, bc
   5451 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   5453 21 06 00      [10]  101 	ld	hl, #0x0006
   5456 09            [11]  102 	add	hl, bc
   5457 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   5459 21 07 00      [10]  105 	ld	hl, #0x0007
   545C 09            [11]  106 	add	hl, bc
   545D 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   545F 21 08 00      [10]  109 	ld	hl, #0x0008
   5462 09            [11]  110 	add	hl, bc
   5463 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   5465 21 09 00      [10]  113 	ld	hl, #0x0009
   5468 09            [11]  114 	add	hl, bc
   5469 36 00         [10]  115 	ld	(hl), #0x00
   546B C9            [10]  116 	ret
   546C                     117 _enemy_kind0_sprite:
   546C 30                  118 	.db #0x30	; 48	'0'
   546D 30                  119 	.db #0x30	; 48	'0'
   546E 30                  120 	.db #0x30	; 48	'0'
   546F 30                  121 	.db #0x30	; 48	'0'
   5470 30                  122 	.db #0x30	; 48	'0'
   5471 00                  123 	.db #0x00	; 0
   5472 00                  124 	.db #0x00	; 0
   5473 10                  125 	.db #0x10	; 16
   5474 30                  126 	.db #0x30	; 48	'0'
   5475 00                  127 	.db #0x00	; 0
   5476 00                  128 	.db #0x00	; 0
   5477 10                  129 	.db #0x10	; 16
   5478 30                  130 	.db #0x30	; 48	'0'
   5479 00                  131 	.db #0x00	; 0
   547A 00                  132 	.db #0x00	; 0
   547B 10                  133 	.db #0x10	; 16
   547C 30                  134 	.db #0x30	; 48	'0'
   547D 00                  135 	.db #0x00	; 0
   547E 00                  136 	.db #0x00	; 0
   547F 10                  137 	.db #0x10	; 16
   5480 30                  138 	.db #0x30	; 48	'0'
   5481 00                  139 	.db #0x00	; 0
   5482 00                  140 	.db #0x00	; 0
   5483 10                  141 	.db #0x10	; 16
   5484 30                  142 	.db #0x30	; 48	'0'
   5485 00                  143 	.db #0x00	; 0
   5486 00                  144 	.db #0x00	; 0
   5487 10                  145 	.db #0x10	; 16
   5488 30                  146 	.db #0x30	; 48	'0'
   5489 00                  147 	.db #0x00	; 0
   548A 00                  148 	.db #0x00	; 0
   548B 10                  149 	.db #0x10	; 16
   548C 30                  150 	.db #0x30	; 48	'0'
   548D 30                  151 	.db #0x30	; 48	'0'
   548E 30                  152 	.db #0x30	; 48	'0'
   548F 30                  153 	.db #0x30	; 48	'0'
   5490 30                  154 	.db #0x30	; 48	'0'
   5491 00                  155 	.db #0x00	; 0
   5492 00                  156 	.db #0x00	; 0
   5493 10                  157 	.db #0x10	; 16
   5494 30                  158 	.db #0x30	; 48	'0'
   5495 00                  159 	.db #0x00	; 0
   5496 00                  160 	.db #0x00	; 0
   5497 10                  161 	.db #0x10	; 16
   5498 30                  162 	.db #0x30	; 48	'0'
   5499 00                  163 	.db #0x00	; 0
   549A 00                  164 	.db #0x00	; 0
   549B 10                  165 	.db #0x10	; 16
   549C 30                  166 	.db #0x30	; 48	'0'
   549D 00                  167 	.db #0x00	; 0
   549E 00                  168 	.db #0x00	; 0
   549F 10                  169 	.db #0x10	; 16
   54A0 30                  170 	.db #0x30	; 48	'0'
   54A1 00                  171 	.db #0x00	; 0
   54A2 00                  172 	.db #0x00	; 0
   54A3 10                  173 	.db #0x10	; 16
   54A4 30                  174 	.db #0x30	; 48	'0'
   54A5 00                  175 	.db #0x00	; 0
   54A6 00                  176 	.db #0x00	; 0
   54A7 10                  177 	.db #0x10	; 16
   54A8 30                  178 	.db #0x30	; 48	'0'
   54A9 30                  179 	.db #0x30	; 48	'0'
   54AA 30                  180 	.db #0x30	; 48	'0'
   54AB 30                  181 	.db #0x30	; 48	'0'
   54AC                     182 _enemy_kind1_sprite:
   54AC 3F                  183 	.db #0x3f	; 63
   54AD 3F                  184 	.db #0x3f	; 63
   54AE 3F                  185 	.db #0x3f	; 63
   54AF 3F                  186 	.db #0x3f	; 63
   54B0 3F                  187 	.db #0x3f	; 63
   54B1 2A                  188 	.db #0x2a	; 42
   54B2 2A                  189 	.db #0x2a	; 42
   54B3 00                  190 	.db #0x00	; 0
   54B4 00                  191 	.db #0x00	; 0
   54B5 15                  192 	.db #0x15	; 21
   54B6 2A                  193 	.db #0x2a	; 42
   54B7 2A                  194 	.db #0x2a	; 42
   54B8 00                  195 	.db #0x00	; 0
   54B9 00                  196 	.db #0x00	; 0
   54BA 15                  197 	.db #0x15	; 21
   54BB 2A                  198 	.db #0x2a	; 42
   54BC 2A                  199 	.db #0x2a	; 42
   54BD 00                  200 	.db #0x00	; 0
   54BE 00                  201 	.db #0x00	; 0
   54BF 15                  202 	.db #0x15	; 21
   54C0 2A                  203 	.db #0x2a	; 42
   54C1 2A                  204 	.db #0x2a	; 42
   54C2 00                  205 	.db #0x00	; 0
   54C3 00                  206 	.db #0x00	; 0
   54C4 15                  207 	.db #0x15	; 21
   54C5 2A                  208 	.db #0x2a	; 42
   54C6 2A                  209 	.db #0x2a	; 42
   54C7 00                  210 	.db #0x00	; 0
   54C8 00                  211 	.db #0x00	; 0
   54C9 15                  212 	.db #0x15	; 21
   54CA 2A                  213 	.db #0x2a	; 42
   54CB 2A                  214 	.db #0x2a	; 42
   54CC 00                  215 	.db #0x00	; 0
   54CD 00                  216 	.db #0x00	; 0
   54CE 15                  217 	.db #0x15	; 21
   54CF 3F                  218 	.db #0x3f	; 63
   54D0 3F                  219 	.db #0x3f	; 63
   54D1 3F                  220 	.db #0x3f	; 63
   54D2 3F                  221 	.db #0x3f	; 63
   54D3 3F                  222 	.db #0x3f	; 63
   54D4 2A                  223 	.db #0x2a	; 42
   54D5 2A                  224 	.db #0x2a	; 42
   54D6 00                  225 	.db #0x00	; 0
   54D7 00                  226 	.db #0x00	; 0
   54D8 15                  227 	.db #0x15	; 21
   54D9 2A                  228 	.db #0x2a	; 42
   54DA 2A                  229 	.db #0x2a	; 42
   54DB 00                  230 	.db #0x00	; 0
   54DC 00                  231 	.db #0x00	; 0
   54DD 15                  232 	.db #0x15	; 21
   54DE 2A                  233 	.db #0x2a	; 42
   54DF 2A                  234 	.db #0x2a	; 42
   54E0 00                  235 	.db #0x00	; 0
   54E1 00                  236 	.db #0x00	; 0
   54E2 15                  237 	.db #0x15	; 21
   54E3 2A                  238 	.db #0x2a	; 42
   54E4 2A                  239 	.db #0x2a	; 42
   54E5 00                  240 	.db #0x00	; 0
   54E6 00                  241 	.db #0x00	; 0
   54E7 15                  242 	.db #0x15	; 21
   54E8 2A                  243 	.db #0x2a	; 42
   54E9 2A                  244 	.db #0x2a	; 42
   54EA 00                  245 	.db #0x00	; 0
   54EB 00                  246 	.db #0x00	; 0
   54EC 15                  247 	.db #0x15	; 21
   54ED 3F                  248 	.db #0x3f	; 63
   54EE 3F                  249 	.db #0x3f	; 63
   54EF 3F                  250 	.db #0x3f	; 63
   54F0 3F                  251 	.db #0x3f	; 63
   54F1 3F                  252 	.db #0x3f	; 63
   54F2                     253 _enemy_kind2_sprite:
   54F2 0F                  254 	.db #0x0f	; 15
   54F3 0F                  255 	.db #0x0f	; 15
   54F4 0F                  256 	.db #0x0f	; 15
   54F5 0F                  257 	.db #0x0f	; 15
   54F6 0F                  258 	.db #0x0f	; 15
   54F7 0F                  259 	.db #0x0f	; 15
   54F8 0A                  260 	.db #0x0a	; 10
   54F9 05                  261 	.db #0x05	; 5
   54FA 00                  262 	.db #0x00	; 0
   54FB 00                  263 	.db #0x00	; 0
   54FC 00                  264 	.db #0x00	; 0
   54FD 05                  265 	.db #0x05	; 5
   54FE 0A                  266 	.db #0x0a	; 10
   54FF 05                  267 	.db #0x05	; 5
   5500 00                  268 	.db #0x00	; 0
   5501 00                  269 	.db #0x00	; 0
   5502 00                  270 	.db #0x00	; 0
   5503 05                  271 	.db #0x05	; 5
   5504 0A                  272 	.db #0x0a	; 10
   5505 05                  273 	.db #0x05	; 5
   5506 00                  274 	.db #0x00	; 0
   5507 00                  275 	.db #0x00	; 0
   5508 00                  276 	.db #0x00	; 0
   5509 05                  277 	.db #0x05	; 5
   550A 0A                  278 	.db #0x0a	; 10
   550B 05                  279 	.db #0x05	; 5
   550C 00                  280 	.db #0x00	; 0
   550D 00                  281 	.db #0x00	; 0
   550E 00                  282 	.db #0x00	; 0
   550F 05                  283 	.db #0x05	; 5
   5510 0F                  284 	.db #0x0f	; 15
   5511 0F                  285 	.db #0x0f	; 15
   5512 0F                  286 	.db #0x0f	; 15
   5513 0F                  287 	.db #0x0f	; 15
   5514 0F                  288 	.db #0x0f	; 15
   5515 0F                  289 	.db #0x0f	; 15
   5516 0A                  290 	.db #0x0a	; 10
   5517 05                  291 	.db #0x05	; 5
   5518 00                  292 	.db #0x00	; 0
   5519 00                  293 	.db #0x00	; 0
   551A 00                  294 	.db #0x00	; 0
   551B 05                  295 	.db #0x05	; 5
   551C 0A                  296 	.db #0x0a	; 10
   551D 05                  297 	.db #0x05	; 5
   551E 00                  298 	.db #0x00	; 0
   551F 00                  299 	.db #0x00	; 0
   5520 00                  300 	.db #0x00	; 0
   5521 05                  301 	.db #0x05	; 5
   5522 0A                  302 	.db #0x0a	; 10
   5523 05                  303 	.db #0x05	; 5
   5524 00                  304 	.db #0x00	; 0
   5525 00                  305 	.db #0x00	; 0
   5526 00                  306 	.db #0x00	; 0
   5527 05                  307 	.db #0x05	; 5
   5528 0F                  308 	.db #0x0f	; 15
   5529 0F                  309 	.db #0x0f	; 15
   552A 0F                  310 	.db #0x0f	; 15
   552B 0F                  311 	.db #0x0f	; 15
   552C 0F                  312 	.db #0x0f	; 15
   552D 0F                  313 	.db #0x0f	; 15
   552E                     314 _enemy_kind3_sprite:
   552E 33                  315 	.db #0x33	; 51	'3'
   552F 33                  316 	.db #0x33	; 51	'3'
   5530 33                  317 	.db #0x33	; 51	'3'
   5531 33                  318 	.db #0x33	; 51	'3'
   5532 33                  319 	.db #0x33	; 51	'3'
   5533 33                  320 	.db #0x33	; 51	'3'
   5534 33                  321 	.db #0x33	; 51	'3'
   5535 33                  322 	.db #0x33	; 51	'3'
   5536 33                  323 	.db #0x33	; 51	'3'
   5537 33                  324 	.db #0x33	; 51	'3'
   5538 22                  325 	.db #0x22	; 34
   5539 00                  326 	.db #0x00	; 0
   553A 22                  327 	.db #0x22	; 34
   553B 00                  328 	.db #0x00	; 0
   553C 00                  329 	.db #0x00	; 0
   553D 00                  330 	.db #0x00	; 0
   553E 00                  331 	.db #0x00	; 0
   553F 00                  332 	.db #0x00	; 0
   5540 00                  333 	.db #0x00	; 0
   5541 11                  334 	.db #0x11	; 17
   5542 22                  335 	.db #0x22	; 34
   5543 00                  336 	.db #0x00	; 0
   5544 22                  337 	.db #0x22	; 34
   5545 00                  338 	.db #0x00	; 0
   5546 00                  339 	.db #0x00	; 0
   5547 00                  340 	.db #0x00	; 0
   5548 00                  341 	.db #0x00	; 0
   5549 00                  342 	.db #0x00	; 0
   554A 00                  343 	.db #0x00	; 0
   554B 11                  344 	.db #0x11	; 17
   554C 22                  345 	.db #0x22	; 34
   554D 00                  346 	.db #0x00	; 0
   554E 22                  347 	.db #0x22	; 34
   554F 00                  348 	.db #0x00	; 0
   5550 00                  349 	.db #0x00	; 0
   5551 00                  350 	.db #0x00	; 0
   5552 00                  351 	.db #0x00	; 0
   5553 00                  352 	.db #0x00	; 0
   5554 00                  353 	.db #0x00	; 0
   5555 11                  354 	.db #0x11	; 17
   5556 22                  355 	.db #0x22	; 34
   5557 00                  356 	.db #0x00	; 0
   5558 22                  357 	.db #0x22	; 34
   5559 00                  358 	.db #0x00	; 0
   555A 00                  359 	.db #0x00	; 0
   555B 00                  360 	.db #0x00	; 0
   555C 00                  361 	.db #0x00	; 0
   555D 00                  362 	.db #0x00	; 0
   555E 00                  363 	.db #0x00	; 0
   555F 11                  364 	.db #0x11	; 17
   5560 22                  365 	.db #0x22	; 34
   5561 00                  366 	.db #0x00	; 0
   5562 22                  367 	.db #0x22	; 34
   5563 00                  368 	.db #0x00	; 0
   5564 00                  369 	.db #0x00	; 0
   5565 00                  370 	.db #0x00	; 0
   5566 00                  371 	.db #0x00	; 0
   5567 00                  372 	.db #0x00	; 0
   5568 00                  373 	.db #0x00	; 0
   5569 11                  374 	.db #0x11	; 17
   556A 22                  375 	.db #0x22	; 34
   556B 00                  376 	.db #0x00	; 0
   556C 22                  377 	.db #0x22	; 34
   556D 00                  378 	.db #0x00	; 0
   556E 00                  379 	.db #0x00	; 0
   556F 00                  380 	.db #0x00	; 0
   5570 00                  381 	.db #0x00	; 0
   5571 00                  382 	.db #0x00	; 0
   5572 00                  383 	.db #0x00	; 0
   5573 11                  384 	.db #0x11	; 17
   5574 22                  385 	.db #0x22	; 34
   5575 00                  386 	.db #0x00	; 0
   5576 22                  387 	.db #0x22	; 34
   5577 00                  388 	.db #0x00	; 0
   5578 00                  389 	.db #0x00	; 0
   5579 00                  390 	.db #0x00	; 0
   557A 00                  391 	.db #0x00	; 0
   557B 00                  392 	.db #0x00	; 0
   557C 00                  393 	.db #0x00	; 0
   557D 11                  394 	.db #0x11	; 17
   557E 22                  395 	.db #0x22	; 34
   557F 00                  396 	.db #0x00	; 0
   5580 22                  397 	.db #0x22	; 34
   5581 00                  398 	.db #0x00	; 0
   5582 00                  399 	.db #0x00	; 0
   5583 00                  400 	.db #0x00	; 0
   5584 00                  401 	.db #0x00	; 0
   5585 00                  402 	.db #0x00	; 0
   5586 00                  403 	.db #0x00	; 0
   5587 11                  404 	.db #0x11	; 17
   5588 33                  405 	.db #0x33	; 51	'3'
   5589 33                  406 	.db #0x33	; 51	'3'
   558A 33                  407 	.db #0x33	; 51	'3'
   558B 33                  408 	.db #0x33	; 51	'3'
   558C 33                  409 	.db #0x33	; 51	'3'
   558D 33                  410 	.db #0x33	; 51	'3'
   558E 33                  411 	.db #0x33	; 51	'3'
   558F 33                  412 	.db #0x33	; 51	'3'
   5590 33                  413 	.db #0x33	; 51	'3'
   5591 33                  414 	.db #0x33	; 51	'3'
   5592 22                  415 	.db #0x22	; 34
   5593 00                  416 	.db #0x00	; 0
   5594 22                  417 	.db #0x22	; 34
   5595 00                  418 	.db #0x00	; 0
   5596 00                  419 	.db #0x00	; 0
   5597 00                  420 	.db #0x00	; 0
   5598 00                  421 	.db #0x00	; 0
   5599 00                  422 	.db #0x00	; 0
   559A 00                  423 	.db #0x00	; 0
   559B 11                  424 	.db #0x11	; 17
   559C 22                  425 	.db #0x22	; 34
   559D 00                  426 	.db #0x00	; 0
   559E 22                  427 	.db #0x22	; 34
   559F 00                  428 	.db #0x00	; 0
   55A0 00                  429 	.db #0x00	; 0
   55A1 00                  430 	.db #0x00	; 0
   55A2 00                  431 	.db #0x00	; 0
   55A3 00                  432 	.db #0x00	; 0
   55A4 00                  433 	.db #0x00	; 0
   55A5 11                  434 	.db #0x11	; 17
   55A6 22                  435 	.db #0x22	; 34
   55A7 00                  436 	.db #0x00	; 0
   55A8 22                  437 	.db #0x22	; 34
   55A9 00                  438 	.db #0x00	; 0
   55AA 00                  439 	.db #0x00	; 0
   55AB 00                  440 	.db #0x00	; 0
   55AC 00                  441 	.db #0x00	; 0
   55AD 00                  442 	.db #0x00	; 0
   55AE 00                  443 	.db #0x00	; 0
   55AF 11                  444 	.db #0x11	; 17
   55B0 22                  445 	.db #0x22	; 34
   55B1 00                  446 	.db #0x00	; 0
   55B2 22                  447 	.db #0x22	; 34
   55B3 00                  448 	.db #0x00	; 0
   55B4 00                  449 	.db #0x00	; 0
   55B5 00                  450 	.db #0x00	; 0
   55B6 00                  451 	.db #0x00	; 0
   55B7 00                  452 	.db #0x00	; 0
   55B8 00                  453 	.db #0x00	; 0
   55B9 11                  454 	.db #0x11	; 17
   55BA 22                  455 	.db #0x22	; 34
   55BB 00                  456 	.db #0x00	; 0
   55BC 22                  457 	.db #0x22	; 34
   55BD 00                  458 	.db #0x00	; 0
   55BE 00                  459 	.db #0x00	; 0
   55BF 00                  460 	.db #0x00	; 0
   55C0 00                  461 	.db #0x00	; 0
   55C1 00                  462 	.db #0x00	; 0
   55C2 00                  463 	.db #0x00	; 0
   55C3 11                  464 	.db #0x11	; 17
   55C4 22                  465 	.db #0x22	; 34
   55C5 00                  466 	.db #0x00	; 0
   55C6 22                  467 	.db #0x22	; 34
   55C7 00                  468 	.db #0x00	; 0
   55C8 00                  469 	.db #0x00	; 0
   55C9 00                  470 	.db #0x00	; 0
   55CA 00                  471 	.db #0x00	; 0
   55CB 00                  472 	.db #0x00	; 0
   55CC 00                  473 	.db #0x00	; 0
   55CD 11                  474 	.db #0x11	; 17
   55CE 22                  475 	.db #0x22	; 34
   55CF 00                  476 	.db #0x00	; 0
   55D0 22                  477 	.db #0x22	; 34
   55D1 00                  478 	.db #0x00	; 0
   55D2 00                  479 	.db #0x00	; 0
   55D3 00                  480 	.db #0x00	; 0
   55D4 00                  481 	.db #0x00	; 0
   55D5 00                  482 	.db #0x00	; 0
   55D6 00                  483 	.db #0x00	; 0
   55D7 11                  484 	.db #0x11	; 17
   55D8 33                  485 	.db #0x33	; 51	'3'
   55D9 33                  486 	.db #0x33	; 51	'3'
   55DA 33                  487 	.db #0x33	; 51	'3'
   55DB 33                  488 	.db #0x33	; 51	'3'
   55DC 33                  489 	.db #0x33	; 51	'3'
   55DD 33                  490 	.db #0x33	; 51	'3'
   55DE 33                  491 	.db #0x33	; 51	'3'
   55DF 33                  492 	.db #0x33	; 51	'3'
   55E0 33                  493 	.db #0x33	; 51	'3'
   55E1 33                  494 	.db #0x33	; 51	'3'
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   55E2                     499 _enemyspawn::
   55E2 DD E5         [15]  500 	push	ix
   55E4 DD 21 00 00   [14]  501 	ld	ix,#0
   55E8 DD 39         [15]  502 	add	ix,sp
   55EA 21 F1 FF      [10]  503 	ld	hl, #-15
   55ED 39            [11]  504 	add	hl, sp
   55EE F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   55EF DD 7E 05      [19]  507 	ld	a, 5 (ix)
   55F2 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   55F5 CA B5 57      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   55F8 DD 7E 04      [19]  512 	ld	a, 4 (ix)
   55FB DD 77 FE      [19]  513 	ld	-2 (ix), a
   55FE DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5601 DD 77 FF      [19]  515 	ld	-1 (ix), a
   5604 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   5607 DD 66 FF      [19]  517 	ld	h,-1 (ix)
   560A DD 7E 06      [19]  518 	ld	a, 6 (ix)
   560D 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   560E DD 4E FE      [19]  521 	ld	c,-2 (ix)
   5611 DD 46 FF      [19]  522 	ld	b,-1 (ix)
   5614 03            [ 6]  523 	inc	bc
   5615 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   5618 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   5619 DD 7E FE      [19]  527 	ld	a, -2 (ix)
   561C C6 02         [ 7]  528 	add	a, #0x02
   561E DD 77 FC      [19]  529 	ld	-4 (ix), a
   5621 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5624 CE 00         [ 7]  531 	adc	a, #0x00
   5626 DD 77 FD      [19]  532 	ld	-3 (ix), a
   5629 DD 7E 09      [19]  533 	ld	a, 9 (ix)
   562C B7            [ 4]  534 	or	a, a
   562D 28 04         [12]  535 	jr	Z,00114$
   562F 0E 01         [ 7]  536 	ld	c, #0x01
   5631 18 02         [12]  537 	jr	00115$
   5633                     538 00114$:
   5633 0E FF         [ 7]  539 	ld	c, #0xff
   5635                     540 00115$:
   5635 DD 6E FC      [19]  541 	ld	l,-4 (ix)
   5638 DD 66 FD      [19]  542 	ld	h,-3 (ix)
   563B 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   563C DD 7E FE      [19]  545 	ld	a, -2 (ix)
   563F C6 03         [ 7]  546 	add	a, #0x03
   5641 DD 77 FA      [19]  547 	ld	-6 (ix), a
   5644 DD 7E FF      [19]  548 	ld	a, -1 (ix)
   5647 CE 00         [ 7]  549 	adc	a, #0x00
   5649 DD 77 FB      [19]  550 	ld	-5 (ix), a
   564C DD 6E FA      [19]  551 	ld	l,-6 (ix)
   564F DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5652 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   5654 DD 7E FE      [19]  555 	ld	a, -2 (ix)
   5657 C6 06         [ 7]  556 	add	a, #0x06
   5659 DD 77 F8      [19]  557 	ld	-8 (ix), a
   565C DD 7E FF      [19]  558 	ld	a, -1 (ix)
   565F CE 00         [ 7]  559 	adc	a, #0x00
   5661 DD 77 F9      [19]  560 	ld	-7 (ix), a
   5664 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   5667 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   566A 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   566C DD 7E FE      [19]  565 	ld	a, -2 (ix)
   566F C6 09         [ 7]  566 	add	a, #0x09
   5671 DD 77 F8      [19]  567 	ld	-8 (ix), a
   5674 DD 7E FF      [19]  568 	ld	a, -1 (ix)
   5677 CE 00         [ 7]  569 	adc	a, #0x00
   5679 DD 77 F9      [19]  570 	ld	-7 (ix), a
   567C DD 6E F8      [19]  571 	ld	l,-8 (ix)
   567F DD 66 F9      [19]  572 	ld	h,-7 (ix)
   5682 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   5685 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   5686 DD 7E FE      [19]  576 	ld	a, -2 (ix)
   5689 C6 04         [ 7]  577 	add	a, #0x04
   568B DD 77 F8      [19]  578 	ld	-8 (ix), a
   568E DD 7E FF      [19]  579 	ld	a, -1 (ix)
   5691 CE 00         [ 7]  580 	adc	a, #0x00
   5693 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   5696 DD 7E FE      [19]  583 	ld	a, -2 (ix)
   5699 C6 05         [ 7]  584 	add	a, #0x05
   569B DD 77 F6      [19]  585 	ld	-10 (ix), a
   569E DD 7E FF      [19]  586 	ld	a, -1 (ix)
   56A1 CE 00         [ 7]  587 	adc	a, #0x00
   56A3 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   56A6 DD 7E FE      [19]  590 	ld	a, -2 (ix)
   56A9 C6 07         [ 7]  591 	add	a, #0x07
   56AB DD 77 F4      [19]  592 	ld	-12 (ix), a
   56AE DD 7E FF      [19]  593 	ld	a, -1 (ix)
   56B1 CE 00         [ 7]  594 	adc	a, #0x00
   56B3 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   56B6 DD 7E FE      [19]  597 	ld	a, -2 (ix)
   56B9 C6 08         [ 7]  598 	add	a, #0x08
   56BB DD 77 FE      [19]  599 	ld	-2 (ix), a
   56BE DD 7E FF      [19]  600 	ld	a, -1 (ix)
   56C1 CE 00         [ 7]  601 	adc	a, #0x00
   56C3 DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   56C6 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   56C9 3D            [ 4]  605 	dec	a
   56CA 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   56CC DD 6E F8      [19]  608 	ld	l,-8 (ix)
   56CF DD 66 F9      [19]  609 	ld	h,-7 (ix)
   56D2 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   56D4 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   56D7 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   56DA 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   56DC DD 6E F4      [19]  616 	ld	l,-12 (ix)
   56DF DD 66 F5      [19]  617 	ld	h,-11 (ix)
   56E2 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   56E4 DD 6E FE      [19]  620 	ld	l,-2 (ix)
   56E7 DD 66 FF      [19]  621 	ld	h,-1 (ix)
   56EA 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   56EC DD 7E FC      [19]  624 	ld	a, -4 (ix)
   56EF DD 77 F2      [19]  625 	ld	-14 (ix), a
   56F2 DD 7E FD      [19]  626 	ld	a, -3 (ix)
   56F5 DD 77 F3      [19]  627 	ld	-13 (ix), a
   56F8 DD 7E 09      [19]  628 	ld	a, 9 (ix)
   56FB B7            [ 4]  629 	or	a, a
   56FC 28 06         [12]  630 	jr	Z,00116$
   56FE DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5702 18 04         [12]  632 	jr	00117$
   5704                     633 00116$:
   5704 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5708                     635 00117$:
   5708 DD 6E F2      [19]  636 	ld	l,-14 (ix)
   570B DD 66 F3      [19]  637 	ld	h,-13 (ix)
   570E DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5711 77            [ 7]  639 	ld	(hl), a
   5712 C3 B5 57      [10]  640 	jp	00112$
   5715                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   5715 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   5718 D6 02         [ 7]  644 	sub	a, #0x02
   571A 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   571C DD 6E F8      [19]  647 	ld	l,-8 (ix)
   571F DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5722 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5724 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   5727 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   572A 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   572C DD 6E F4      [19]  655 	ld	l,-12 (ix)
   572F DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5732 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5734 DD 6E FE      [19]  659 	ld	l,-2 (ix)
   5737 DD 66 FF      [19]  660 	ld	h,-1 (ix)
   573A 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   573C DD 4E FA      [19]  663 	ld	c,-6 (ix)
   573F DD 46 FB      [19]  664 	ld	b,-5 (ix)
   5742 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   5745 B7            [ 4]  666 	or	a, a
   5746 28 04         [12]  667 	jr	Z,00118$
   5748 3E 01         [ 7]  668 	ld	a, #0x01
   574A 18 02         [12]  669 	jr	00119$
   574C                     670 00118$:
   574C 3E FF         [ 7]  671 	ld	a, #0xff
   574E                     672 00119$:
   574E 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   574F DD 6E FC      [19]  675 	ld	l,-4 (ix)
   5752 DD 66 FD      [19]  676 	ld	h,-3 (ix)
   5755 36 01         [10]  677 	ld	(hl), #0x01
   5757 18 5C         [12]  678 	jr	00112$
   5759                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   5759 DD 7E 08      [19]  681 	ld	a, 8 (ix)
   575C D6 03         [ 7]  682 	sub	a, #0x03
   575E 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   5760 DD 6E F8      [19]  685 	ld	l,-8 (ix)
   5763 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   5766 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   5768 DD 6E F6      [19]  689 	ld	l,-10 (ix)
   576B DD 66 F7      [19]  690 	ld	h,-9 (ix)
   576E 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   5770 DD 6E F4      [19]  693 	ld	l,-12 (ix)
   5773 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   5776 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   5778 DD 6E FE      [19]  697 	ld	l,-2 (ix)
   577B DD 66 FF      [19]  698 	ld	h,-1 (ix)
   577E 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   5780 DD 4E FC      [19]  701 	ld	c,-4 (ix)
   5783 DD 46 FD      [19]  702 	ld	b,-3 (ix)
   5786 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   5789 B7            [ 4]  704 	or	a, a
   578A 28 04         [12]  705 	jr	Z,00120$
   578C 3E 01         [ 7]  706 	ld	a, #0x01
   578E 18 02         [12]  707 	jr	00121$
   5790                     708 00120$:
   5790 3E FF         [ 7]  709 	ld	a, #0xff
   5792                     710 00121$:
   5792 02            [ 7]  711 	ld	(bc), a
   5793 18 20         [12]  712 	jr	00112$
   5795                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   5795 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   5798 DD 66 F9      [19]  716 	ld	h,-7 (ix)
   579B 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   579D DD 6E F6      [19]  719 	ld	l,-10 (ix)
   57A0 DD 66 F7      [19]  720 	ld	h,-9 (ix)
   57A3 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   57A5 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   57A8 DD 66 F5      [19]  724 	ld	h,-11 (ix)
   57AB 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   57AD DD 6E FE      [19]  727 	ld	l,-2 (ix)
   57B0 DD 66 FF      [19]  728 	ld	h,-1 (ix)
   57B3 36 64         [10]  729 	ld	(hl), #0x64
   57B5                     730 00112$:
   57B5 DD F9         [10]  731 	ld	sp, ix
   57B7 DD E1         [14]  732 	pop	ix
   57B9 C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   57BA                     738 _enemyupdate::
   57BA DD E5         [15]  739 	push	ix
   57BC DD 21 00 00   [14]  740 	ld	ix,#0
   57C0 DD 39         [15]  741 	add	ix,sp
   57C2 21 F6 FF      [10]  742 	ld	hl, #-10
   57C5 39            [11]  743 	add	hl, sp
   57C6 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   57C7 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   57CA DD B6 04      [19]  747 	or	a,4 (ix)
   57CD CA A6 59      [10]  748 	jp	Z,00121$
   57D0 DD 7E 04      [19]  749 	ld	a, 4 (ix)
   57D3 DD 77 F6      [19]  750 	ld	-10 (ix), a
   57D6 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   57D9 DD 77 F7      [19]  752 	ld	-9 (ix), a
   57DC E1            [10]  753 	pop	hl
   57DD E5            [11]  754 	push	hl
   57DE 11 06 00      [10]  755 	ld	de, #0x0006
   57E1 19            [11]  756 	add	hl, de
   57E2 7E            [ 7]  757 	ld	a, (hl)
   57E3 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   57E4 CA A6 59      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   57E7 E1            [10]  762 	pop	hl
   57E8 E5            [11]  763 	push	hl
   57E9 11 09 00      [10]  764 	ld	de, #0x0009
   57EC 19            [11]  765 	add	hl, de
   57ED 7E            [ 7]  766 	ld	a, (hl)
   57EE DD 77 FF      [19]  767 	ld	-1 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   57F1 E1            [10]  769 	pop	hl
   57F2 E5            [11]  770 	push	hl
   57F3 4E            [ 7]  771 	ld	c, (hl)
   57F4 DD 7E F6      [19]  772 	ld	a, -10 (ix)
   57F7 C6 02         [ 7]  773 	add	a, #0x02
   57F9 DD 77 FD      [19]  774 	ld	-3 (ix), a
   57FC DD 7E F7      [19]  775 	ld	a, -9 (ix)
   57FF CE 00         [ 7]  776 	adc	a, #0x00
   5801 DD 77 FE      [19]  777 	ld	-2 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5804 DD 7E F6      [19]  779 	ld	a, -10 (ix)
   5807 C6 01         [ 7]  780 	add	a, #0x01
   5809 DD 77 FB      [19]  781 	ld	-5 (ix), a
   580C DD 7E F7      [19]  782 	ld	a, -9 (ix)
   580F CE 00         [ 7]  783 	adc	a, #0x00
   5811 DD 77 FC      [19]  784 	ld	-4 (ix), a
   5814 D1            [10]  785 	pop	de
   5815 D5            [11]  786 	push	de
   5816 13            [ 6]  787 	inc	de
   5817 13            [ 6]  788 	inc	de
   5818 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5819 06 00         [ 7]  791 	ld	b, #0x00
   581B DD 6E FD      [19]  792 	ld	l,-3 (ix)
   581E DD 66 FE      [19]  793 	ld	h,-2 (ix)
   5821 7E            [ 7]  794 	ld	a, (hl)
   5822 DD 77 FA      [19]  795 	ld	-6 (ix), a
   5825 6F            [ 4]  796 	ld	l, a
   5826 DD 7E FA      [19]  797 	ld	a, -6 (ix)
   5829 17            [ 4]  798 	rla
   582A 9F            [ 4]  799 	sbc	a, a
   582B 67            [ 4]  800 	ld	h, a
   582C 09            [11]  801 	add	hl,bc
   582D 4D            [ 4]  802 	ld	c, l
   582E 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   582F DD 7E FF      [19]  805 	ld	a, -1 (ix)
   5832 D6 02         [ 7]  806 	sub	a, #0x02
   5834 C2 DA 58      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5837 DD 6E FB      [19]  810 	ld	l,-5 (ix)
   583A DD 66 FC      [19]  811 	ld	h,-4 (ix)
   583D 6E            [ 7]  812 	ld	l, (hl)
   583E DD 75 F8      [19]  813 	ld	-8 (ix), l
   5841 DD 36 F9 00   [19]  814 	ld	-7 (ix), #0x00
   5845 1A            [ 7]  815 	ld	a, (de)
   5846 6F            [ 4]  816 	ld	l, a
   5847 17            [ 4]  817 	rla
   5848 9F            [ 4]  818 	sbc	a, a
   5849 67            [ 4]  819 	ld	h, a
   584A DD 7E F8      [19]  820 	ld	a, -8 (ix)
   584D 85            [ 4]  821 	add	a, l
   584E DD 77 F8      [19]  822 	ld	-8 (ix), a
   5851 DD 7E F9      [19]  823 	ld	a, -7 (ix)
   5854 8C            [ 4]  824 	adc	a, h
   5855 DD 77 F9      [19]  825 	ld	-7 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   5858 79            [ 4]  827 	ld	a, c
   5859 D6 08         [ 7]  828 	sub	a, #0x08
   585B 78            [ 4]  829 	ld	a, b
   585C 17            [ 4]  830 	rla
   585D 3F            [ 4]  831 	ccf
   585E 1F            [ 4]  832 	rra
   585F DE 80         [ 7]  833 	sbc	a, #0x80
   5861 38 0E         [12]  834 	jr	C,00104$
   5863 3E 48         [ 7]  835 	ld	a, #0x48
   5865 B9            [ 4]  836 	cp	a, c
   5866 3E 00         [ 7]  837 	ld	a, #0x00
   5868 98            [ 4]  838 	sbc	a, b
   5869 E2 6E 58      [10]  839 	jp	PO, 00161$
   586C EE 80         [ 7]  840 	xor	a, #0x80
   586E                     841 00161$:
   586E F2 88 58      [10]  842 	jp	P, 00105$
   5871                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   5871 AF            [ 4]  845 	xor	a, a
   5872 DD 96 FA      [19]  846 	sub	a, -6 (ix)
   5875 4F            [ 4]  847 	ld	c, a
   5876 DD 6E FD      [19]  848 	ld	l,-3 (ix)
   5879 DD 66 FE      [19]  849 	ld	h,-2 (ix)
   587C 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   587D E1            [10]  852 	pop	hl
   587E E5            [11]  853 	push	hl
   587F 6E            [ 7]  854 	ld	l, (hl)
   5880 26 00         [ 7]  855 	ld	h, #0x00
   5882 79            [ 4]  856 	ld	a, c
   5883 17            [ 4]  857 	rla
   5884 9F            [ 4]  858 	sbc	a, a
   5885 47            [ 4]  859 	ld	b, a
   5886 09            [11]  860 	add	hl,bc
   5887 4D            [ 4]  861 	ld	c, l
   5888                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   5888 DD 7E F8      [19]  864 	ld	a, -8 (ix)
   588B D6 38         [ 7]  865 	sub	a, #0x38
   588D DD 7E F9      [19]  866 	ld	a, -7 (ix)
   5890 17            [ 4]  867 	rla
   5891 3F            [ 4]  868 	ccf
   5892 1F            [ 4]  869 	rra
   5893 DE 80         [ 7]  870 	sbc	a, #0x80
   5895 38 12         [12]  871 	jr	C,00107$
   5897 3E 78         [ 7]  872 	ld	a, #0x78
   5899 DD BE F8      [19]  873 	cp	a, -8 (ix)
   589C 3E 00         [ 7]  874 	ld	a, #0x00
   589E DD 9E F9      [19]  875 	sbc	a, -7 (ix)
   58A1 E2 A6 58      [10]  876 	jp	PO, 00162$
   58A4 EE 80         [ 7]  877 	xor	a, #0x80
   58A6                     878 00162$:
   58A6 F2 CA 58      [10]  879 	jp	P, 00108$
   58A9                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   58A9 1A            [ 7]  882 	ld	a, (de)
   58AA 6F            [ 4]  883 	ld	l, a
   58AB AF            [ 4]  884 	xor	a, a
   58AC 95            [ 4]  885 	sub	a, l
   58AD DD 77 FA      [19]  886 	ld	-6 (ix), a
   58B0 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   58B1 DD 6E FB      [19]  889 	ld	l,-5 (ix)
   58B4 DD 66 FC      [19]  890 	ld	h,-4 (ix)
   58B7 5E            [ 7]  891 	ld	e, (hl)
   58B8 16 00         [ 7]  892 	ld	d, #0x00
   58BA DD 6E FA      [19]  893 	ld	l, -6 (ix)
   58BD DD 7E FA      [19]  894 	ld	a, -6 (ix)
   58C0 17            [ 4]  895 	rla
   58C1 9F            [ 4]  896 	sbc	a, a
   58C2 67            [ 4]  897 	ld	h, a
   58C3 19            [11]  898 	add	hl,de
   58C4 DD 75 F8      [19]  899 	ld	-8 (ix), l
   58C7 DD 74 F9      [19]  900 	ld	-7 (ix), h
   58CA                     901 00108$:
                            902 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   58CA E1            [10]  903 	pop	hl
   58CB E5            [11]  904 	push	hl
   58CC 71            [ 7]  905 	ld	(hl), c
                            906 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   58CD DD 4E F8      [19]  907 	ld	c, -8 (ix)
   58D0 DD 6E FB      [19]  908 	ld	l,-5 (ix)
   58D3 DD 66 FC      [19]  909 	ld	h,-4 (ix)
   58D6 71            [ 7]  910 	ld	(hl), c
                            911 ;src/entities/enemy.c:144: return;
   58D7 C3 A6 59      [10]  912 	jp	00121$
   58DA                     913 00111$:
                            914 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            915 ;src/entities/enemy.c:148: if (nextx < 2) {
   58DA 79            [ 4]  916 	ld	a, c
   58DB D6 02         [ 7]  917 	sub	a, #0x02
   58DD 78            [ 4]  918 	ld	a, b
   58DE 17            [ 4]  919 	rla
   58DF 3F            [ 4]  920 	ccf
   58E0 1F            [ 4]  921 	rra
   58E1 DE 80         [ 7]  922 	sbc	a, #0x80
   58E3 30 0B         [12]  923 	jr	NC,00113$
                            924 ;src/entities/enemy.c:149: nextx = 2;
   58E5 01 02 00      [10]  925 	ld	bc, #0x0002
                            926 ;src/entities/enemy.c:150: enemy->vx = 1;
   58E8 DD 6E FD      [19]  927 	ld	l,-3 (ix)
   58EB DD 66 FE      [19]  928 	ld	h,-2 (ix)
   58EE 36 01         [10]  929 	ld	(hl), #0x01
   58F0                     930 00113$:
                            931 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   58F0 E1            [10]  932 	pop	hl
   58F1 E5            [11]  933 	push	hl
   58F2 23            [ 6]  934 	inc	hl
   58F3 23            [ 6]  935 	inc	hl
   58F4 23            [ 6]  936 	inc	hl
   58F5 23            [ 6]  937 	inc	hl
   58F6 6E            [ 7]  938 	ld	l, (hl)
   58F7 26 00         [ 7]  939 	ld	h, #0x00
   58F9 3E 50         [ 7]  940 	ld	a, #0x50
   58FB 95            [ 4]  941 	sub	a, l
   58FC 6F            [ 4]  942 	ld	l, a
   58FD 3E 00         [ 7]  943 	ld	a, #0x00
   58FF 9C            [ 4]  944 	sbc	a, h
   5900 67            [ 4]  945 	ld	h, a
                            946 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5901 7D            [ 4]  947 	ld	a, l
   5902 91            [ 4]  948 	sub	a, c
   5903 7C            [ 4]  949 	ld	a, h
   5904 98            [ 4]  950 	sbc	a, b
   5905 E2 0A 59      [10]  951 	jp	PO, 00163$
   5908 EE 80         [ 7]  952 	xor	a, #0x80
   590A                     953 00163$:
   590A F2 16 59      [10]  954 	jp	P, 00115$
                            955 ;src/entities/enemy.c:155: nextx = maxx;
   590D 4D            [ 4]  956 	ld	c, l
                            957 ;src/entities/enemy.c:156: enemy->vx = -1;
   590E DD 6E FD      [19]  958 	ld	l,-3 (ix)
   5911 DD 66 FE      [19]  959 	ld	h,-2 (ix)
   5914 36 FF         [10]  960 	ld	(hl), #0xff
   5916                     961 00115$:
                            962 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5916 E1            [10]  963 	pop	hl
   5917 E5            [11]  964 	push	hl
   5918 71            [ 7]  965 	ld	(hl), c
                            966 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5919 1A            [ 7]  967 	ld	a, (de)
   591A 4F            [ 4]  968 	ld	c, a
   591B 0C            [ 4]  969 	inc	c
   591C 79            [ 4]  970 	ld	a, c
   591D 12            [ 7]  971 	ld	(de), a
                            972 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   591E 3E 03         [ 7]  973 	ld	a, #0x03
   5920 91            [ 4]  974 	sub	a, c
   5921 E2 26 59      [10]  975 	jp	PO, 00164$
   5924 EE 80         [ 7]  976 	xor	a, #0x80
   5926                     977 00164$:
   5926 F2 2C 59      [10]  978 	jp	P, 00117$
   5929 3E 03         [ 7]  979 	ld	a, #0x03
   592B 12            [ 7]  980 	ld	(de), a
   592C                     981 00117$:
                            982 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   592C DD 6E FB      [19]  983 	ld	l,-5 (ix)
   592F DD 66 FC      [19]  984 	ld	h,-4 (ix)
   5932 4E            [ 7]  985 	ld	c, (hl)
   5933 06 00         [ 7]  986 	ld	b, #0x00
   5935 1A            [ 7]  987 	ld	a, (de)
   5936 6F            [ 4]  988 	ld	l, a
   5937 17            [ 4]  989 	rla
   5938 9F            [ 4]  990 	sbc	a, a
   5939 67            [ 4]  991 	ld	h, a
   593A 09            [11]  992 	add	hl, bc
   593B E5            [11]  993 	push	hl
   593C FD E1         [14]  994 	pop	iy
                            995 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   593E DD 7E F6      [19]  996 	ld	a, -10 (ix)
   5941 C6 05         [ 7]  997 	add	a, #0x05
   5943 DD 77 F8      [19]  998 	ld	-8 (ix), a
   5946 DD 7E F7      [19]  999 	ld	a, -9 (ix)
   5949 CE 00         [ 7] 1000 	adc	a, #0x00
   594B DD 77 F9      [19] 1001 	ld	-7 (ix), a
   594E DD 6E F8      [19] 1002 	ld	l,-8 (ix)
   5951 DD 66 F9      [19] 1003 	ld	h,-7 (ix)
   5954 7E            [ 7] 1004 	ld	a, (hl)
   5955 E1            [10] 1005 	pop	hl
   5956 E5            [11] 1006 	push	hl
   5957 4E            [ 7] 1007 	ld	c, (hl)
   5958 06 00         [ 7] 1008 	ld	b, #0x00
   595A D5            [11] 1009 	push	de
   595B F5            [11] 1010 	push	af
   595C 33            [ 6] 1011 	inc	sp
   595D FD E5         [15] 1012 	push	iy
   595F C5            [11] 1013 	push	bc
   5960 CD 40 4C      [17] 1014 	call	_collision_clamp_y_at
   5963 F1            [10] 1015 	pop	af
   5964 F1            [10] 1016 	pop	af
   5965 33            [ 6] 1017 	inc	sp
   5966 4D            [ 4] 1018 	ld	c, l
   5967 D1            [10] 1019 	pop	de
                           1020 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5968 DD 6E FB      [19] 1021 	ld	l,-5 (ix)
   596B DD 66 FC      [19] 1022 	ld	h,-4 (ix)
   596E 71            [ 7] 1023 	ld	(hl), c
                           1024 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   596F DD 6E F8      [19] 1025 	ld	l,-8 (ix)
   5972 DD 66 F9      [19] 1026 	ld	h,-7 (ix)
   5975 7E            [ 7] 1027 	ld	a, (hl)
   5976 06 00         [ 7] 1028 	ld	b, #0x00
   5978 E1            [10] 1029 	pop	hl
   5979 E5            [11] 1030 	push	hl
   597A 6E            [ 7] 1031 	ld	l, (hl)
   597B DD 75 F8      [19] 1032 	ld	-8 (ix), l
   597E DD 36 F9 00   [19] 1033 	ld	-7 (ix), #0x00
   5982 D5            [11] 1034 	push	de
   5983 F5            [11] 1035 	push	af
   5984 33            [ 6] 1036 	inc	sp
   5985 C5            [11] 1037 	push	bc
   5986 DD 6E F8      [19] 1038 	ld	l,-8 (ix)
   5989 DD 66 F9      [19] 1039 	ld	h,-7 (ix)
   598C E5            [11] 1040 	push	hl
   598D CD C1 4B      [17] 1041 	call	_collision_is_on_ground_at
   5990 F1            [10] 1042 	pop	af
   5991 F1            [10] 1043 	pop	af
   5992 33            [ 6] 1044 	inc	sp
   5993 D1            [10] 1045 	pop	de
   5994 7D            [ 4] 1046 	ld	a, l
   5995 B7            [ 4] 1047 	or	a, a
   5996 28 0E         [12] 1048 	jr	Z,00121$
   5998 1A            [ 7] 1049 	ld	a, (de)
   5999 4F            [ 4] 1050 	ld	c, a
   599A AF            [ 4] 1051 	xor	a, a
   599B 91            [ 4] 1052 	sub	a, c
   599C E2 A1 59      [10] 1053 	jp	PO, 00165$
   599F EE 80         [ 7] 1054 	xor	a, #0x80
   59A1                    1055 00165$:
   59A1 F2 A6 59      [10] 1056 	jp	P, 00121$
                           1057 ;src/entities/enemy.c:167: enemy->vy = 0;
   59A4 AF            [ 4] 1058 	xor	a, a
   59A5 12            [ 7] 1059 	ld	(de), a
   59A6                    1060 00121$:
   59A6 DD F9         [10] 1061 	ld	sp, ix
   59A8 DD E1         [14] 1062 	pop	ix
   59AA C9            [10] 1063 	ret
                           1064 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1065 ;	---------------------------------
                           1066 ; Function enemyrender
                           1067 ; ---------------------------------
   59AB                    1068 _enemyrender::
   59AB DD E5         [15] 1069 	push	ix
   59AD DD 21 00 00   [14] 1070 	ld	ix,#0
   59B1 DD 39         [15] 1071 	add	ix,sp
   59B3 F5            [11] 1072 	push	af
   59B4 3B            [ 6] 1073 	dec	sp
                           1074 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   59B5 DD 7E 05      [19] 1075 	ld	a, 5 (ix)
   59B8 DD B6 04      [19] 1076 	or	a,4 (ix)
   59BB CA 38 5A      [10] 1077 	jp	Z,00113$
   59BE DD 4E 04      [19] 1078 	ld	c,4 (ix)
   59C1 DD 46 05      [19] 1079 	ld	b,5 (ix)
   59C4 C5            [11] 1080 	push	bc
   59C5 FD E1         [14] 1081 	pop	iy
   59C7 FD 7E 06      [19] 1082 	ld	a, 6 (iy)
   59CA B7            [ 4] 1083 	or	a, a
                           1084 ;src/entities/enemy.c:176: return;
   59CB 28 6B         [12] 1085 	jr	Z,00113$
                           1086 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   59CD C5            [11] 1087 	push	bc
   59CE FD E1         [14] 1088 	pop	iy
   59D0 FD 7E 09      [19] 1089 	ld	a, 9 (iy)
   59D3 FE 03         [ 7] 1090 	cp	a, #0x03
   59D5 20 0A         [12] 1091 	jr	NZ,00111$
   59D7 DD 36 FE 2E   [19] 1092 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   59DB DD 36 FF 55   [19] 1093 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   59DF 18 23         [12] 1094 	jr	00112$
   59E1                    1095 00111$:
                           1096 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   59E1 FE 02         [ 7] 1097 	cp	a, #0x02
   59E3 20 0A         [12] 1098 	jr	NZ,00108$
   59E5 DD 36 FE F2   [19] 1099 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   59E9 DD 36 FF 54   [19] 1100 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   59ED 18 15         [12] 1101 	jr	00112$
   59EF                    1102 00108$:
                           1103 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   59EF 3D            [ 4] 1104 	dec	a
   59F0 20 0A         [12] 1105 	jr	NZ,00105$
   59F2 DD 36 FE AC   [19] 1106 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   59F6 DD 36 FF 54   [19] 1107 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   59FA 18 08         [12] 1108 	jr	00112$
   59FC                    1109 00105$:
                           1110 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   59FC DD 36 FE 6C   [19] 1111 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5A00 DD 36 FF 54   [19] 1112 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5A04                    1113 00112$:
                           1114 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5A04 69            [ 4] 1115 	ld	l, c
   5A05 60            [ 4] 1116 	ld	h, b
   5A06 23            [ 6] 1117 	inc	hl
   5A07 56            [ 7] 1118 	ld	d, (hl)
   5A08 0A            [ 7] 1119 	ld	a, (bc)
   5A09 C5            [11] 1120 	push	bc
   5A0A 5F            [ 4] 1121 	ld	e, a
   5A0B D5            [11] 1122 	push	de
   5A0C 21 00 C0      [10] 1123 	ld	hl, #0xc000
   5A0F E5            [11] 1124 	push	hl
   5A10 CD 2A 62      [17] 1125 	call	_cpct_getScreenPtr
   5A13 EB            [ 4] 1126 	ex	de,hl
   5A14 C1            [10] 1127 	pop	bc
                           1128 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5A15 C5            [11] 1129 	push	bc
   5A16 FD E1         [14] 1130 	pop	iy
   5A18 FD 7E 05      [19] 1131 	ld	a, 5 (iy)
   5A1B DD 77 FD      [19] 1132 	ld	-3 (ix), a
   5A1E 69            [ 4] 1133 	ld	l, c
   5A1F 60            [ 4] 1134 	ld	h, b
   5A20 01 04 00      [10] 1135 	ld	bc, #0x0004
   5A23 09            [11] 1136 	add	hl, bc
   5A24 4E            [ 7] 1137 	ld	c, (hl)
   5A25 D5            [11] 1138 	push	de
   5A26 FD E1         [14] 1139 	pop	iy
   5A28 DD 5E FE      [19] 1140 	ld	e,-2 (ix)
   5A2B DD 56 FF      [19] 1141 	ld	d,-1 (ix)
   5A2E DD 46 FD      [19] 1142 	ld	b, -3 (ix)
   5A31 C5            [11] 1143 	push	bc
   5A32 FD E5         [15] 1144 	push	iy
   5A34 D5            [11] 1145 	push	de
   5A35 CD 5B 60      [17] 1146 	call	_cpct_drawSprite
   5A38                    1147 00113$:
   5A38 DD F9         [10] 1148 	ld	sp, ix
   5A3A DD E1         [14] 1149 	pop	ix
   5A3C C9            [10] 1150 	ret
                           1151 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1152 ;	---------------------------------
                           1153 ; Function enemydamage
                           1154 ; ---------------------------------
   5A3D                    1155 _enemydamage::
   5A3D DD E5         [15] 1156 	push	ix
   5A3F DD 21 00 00   [14] 1157 	ld	ix,#0
   5A43 DD 39         [15] 1158 	add	ix,sp
                           1159 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5A45 DD 7E 05      [19] 1160 	ld	a, 5 (ix)
   5A48 DD B6 04      [19] 1161 	or	a,4 (ix)
   5A4B 28 0F         [12] 1162 	jr	Z,00101$
   5A4D DD 4E 04      [19] 1163 	ld	c,4 (ix)
   5A50 DD 46 05      [19] 1164 	ld	b,5 (ix)
   5A53 21 06 00      [10] 1165 	ld	hl, #0x0006
   5A56 09            [11] 1166 	add	hl,bc
   5A57 EB            [ 4] 1167 	ex	de,hl
   5A58 1A            [ 7] 1168 	ld	a, (de)
   5A59 B7            [ 4] 1169 	or	a, a
   5A5A 20 04         [12] 1170 	jr	NZ,00102$
   5A5C                    1171 00101$:
                           1172 ;src/entities/enemy.c:190: return 0;
   5A5C 2E 00         [ 7] 1173 	ld	l, #0x00
   5A5E 18 1A         [12] 1174 	jr	00106$
   5A60                    1175 00102$:
                           1176 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5A60 21 07 00      [10] 1177 	ld	hl, #0x0007
   5A63 09            [11] 1178 	add	hl, bc
   5A64 4E            [ 7] 1179 	ld	c, (hl)
   5A65 DD 7E 06      [19] 1180 	ld	a, 6 (ix)
   5A68 91            [ 4] 1181 	sub	a, c
   5A69 38 08         [12] 1182 	jr	C,00105$
                           1183 ;src/entities/enemy.c:194: enemy->health = 0;
   5A6B 36 00         [10] 1184 	ld	(hl), #0x00
                           1185 ;src/entities/enemy.c:195: enemy->active = 0;
   5A6D AF            [ 4] 1186 	xor	a, a
   5A6E 12            [ 7] 1187 	ld	(de), a
                           1188 ;src/entities/enemy.c:196: return 1;
   5A6F 2E 01         [ 7] 1189 	ld	l, #0x01
   5A71 18 07         [12] 1190 	jr	00106$
   5A73                    1191 00105$:
                           1192 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5A73 79            [ 4] 1193 	ld	a, c
   5A74 DD 96 06      [19] 1194 	sub	a, 6 (ix)
   5A77 77            [ 7] 1195 	ld	(hl), a
                           1196 ;src/entities/enemy.c:200: return 0;
   5A78 2E 00         [ 7] 1197 	ld	l, #0x00
   5A7A                    1198 00106$:
   5A7A DD E1         [14] 1199 	pop	ix
   5A7C C9            [10] 1200 	ret
                           1201 	.area _CODE
                           1202 	.area _INITIALIZER
                           1203 	.area _CABS (ABS)
