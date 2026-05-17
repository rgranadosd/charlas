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
   5489                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   5489 21 03 00      [10]   57 	ld	hl, #2+1
   548C 39            [11]   58 	add	hl, sp
   548D 7E            [ 7]   59 	ld	a, (hl)
   548E 2B            [ 6]   60 	dec	hl
   548F B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   5490 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   5491 D1            [10]   65 	pop	de
   5492 C1            [10]   66 	pop	bc
   5493 C5            [11]   67 	push	bc
   5494 D5            [11]   68 	push	de
   5495 AF            [ 4]   69 	xor	a, a
   5496 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   5497 59            [ 4]   72 	ld	e, c
   5498 50            [ 4]   73 	ld	d, b
   5499 13            [ 6]   74 	inc	de
   549A AF            [ 4]   75 	xor	a, a
   549B 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   549C 59            [ 4]   78 	ld	e, c
   549D 50            [ 4]   79 	ld	d, b
   549E 13            [ 6]   80 	inc	de
   549F 13            [ 6]   81 	inc	de
   54A0 AF            [ 4]   82 	xor	a, a
   54A1 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   54A2 59            [ 4]   85 	ld	e, c
   54A3 50            [ 4]   86 	ld	d, b
   54A4 13            [ 6]   87 	inc	de
   54A5 13            [ 6]   88 	inc	de
   54A6 13            [ 6]   89 	inc	de
   54A7 AF            [ 4]   90 	xor	a, a
   54A8 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   54A9 21 04 00      [10]   93 	ld	hl, #0x0004
   54AC 09            [11]   94 	add	hl, bc
   54AD 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   54AF 21 05 00      [10]   97 	ld	hl, #0x0005
   54B2 09            [11]   98 	add	hl, bc
   54B3 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   54B5 21 06 00      [10]  101 	ld	hl, #0x0006
   54B8 09            [11]  102 	add	hl, bc
   54B9 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   54BB 21 07 00      [10]  105 	ld	hl, #0x0007
   54BE 09            [11]  106 	add	hl, bc
   54BF 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   54C1 21 08 00      [10]  109 	ld	hl, #0x0008
   54C4 09            [11]  110 	add	hl, bc
   54C5 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   54C7 21 09 00      [10]  113 	ld	hl, #0x0009
   54CA 09            [11]  114 	add	hl, bc
   54CB 36 00         [10]  115 	ld	(hl), #0x00
   54CD C9            [10]  116 	ret
   54CE                     117 _enemy_kind0_sprite:
   54CE 30                  118 	.db #0x30	; 48	'0'
   54CF 30                  119 	.db #0x30	; 48	'0'
   54D0 30                  120 	.db #0x30	; 48	'0'
   54D1 30                  121 	.db #0x30	; 48	'0'
   54D2 30                  122 	.db #0x30	; 48	'0'
   54D3 00                  123 	.db #0x00	; 0
   54D4 00                  124 	.db #0x00	; 0
   54D5 10                  125 	.db #0x10	; 16
   54D6 30                  126 	.db #0x30	; 48	'0'
   54D7 00                  127 	.db #0x00	; 0
   54D8 00                  128 	.db #0x00	; 0
   54D9 10                  129 	.db #0x10	; 16
   54DA 30                  130 	.db #0x30	; 48	'0'
   54DB 00                  131 	.db #0x00	; 0
   54DC 00                  132 	.db #0x00	; 0
   54DD 10                  133 	.db #0x10	; 16
   54DE 30                  134 	.db #0x30	; 48	'0'
   54DF 00                  135 	.db #0x00	; 0
   54E0 00                  136 	.db #0x00	; 0
   54E1 10                  137 	.db #0x10	; 16
   54E2 30                  138 	.db #0x30	; 48	'0'
   54E3 00                  139 	.db #0x00	; 0
   54E4 00                  140 	.db #0x00	; 0
   54E5 10                  141 	.db #0x10	; 16
   54E6 30                  142 	.db #0x30	; 48	'0'
   54E7 00                  143 	.db #0x00	; 0
   54E8 00                  144 	.db #0x00	; 0
   54E9 10                  145 	.db #0x10	; 16
   54EA 30                  146 	.db #0x30	; 48	'0'
   54EB 00                  147 	.db #0x00	; 0
   54EC 00                  148 	.db #0x00	; 0
   54ED 10                  149 	.db #0x10	; 16
   54EE 30                  150 	.db #0x30	; 48	'0'
   54EF 30                  151 	.db #0x30	; 48	'0'
   54F0 30                  152 	.db #0x30	; 48	'0'
   54F1 30                  153 	.db #0x30	; 48	'0'
   54F2 30                  154 	.db #0x30	; 48	'0'
   54F3 00                  155 	.db #0x00	; 0
   54F4 00                  156 	.db #0x00	; 0
   54F5 10                  157 	.db #0x10	; 16
   54F6 30                  158 	.db #0x30	; 48	'0'
   54F7 00                  159 	.db #0x00	; 0
   54F8 00                  160 	.db #0x00	; 0
   54F9 10                  161 	.db #0x10	; 16
   54FA 30                  162 	.db #0x30	; 48	'0'
   54FB 00                  163 	.db #0x00	; 0
   54FC 00                  164 	.db #0x00	; 0
   54FD 10                  165 	.db #0x10	; 16
   54FE 30                  166 	.db #0x30	; 48	'0'
   54FF 00                  167 	.db #0x00	; 0
   5500 00                  168 	.db #0x00	; 0
   5501 10                  169 	.db #0x10	; 16
   5502 30                  170 	.db #0x30	; 48	'0'
   5503 00                  171 	.db #0x00	; 0
   5504 00                  172 	.db #0x00	; 0
   5505 10                  173 	.db #0x10	; 16
   5506 30                  174 	.db #0x30	; 48	'0'
   5507 00                  175 	.db #0x00	; 0
   5508 00                  176 	.db #0x00	; 0
   5509 10                  177 	.db #0x10	; 16
   550A 30                  178 	.db #0x30	; 48	'0'
   550B 30                  179 	.db #0x30	; 48	'0'
   550C 30                  180 	.db #0x30	; 48	'0'
   550D 30                  181 	.db #0x30	; 48	'0'
   550E                     182 _enemy_kind1_sprite:
   550E 3F                  183 	.db #0x3f	; 63
   550F 3F                  184 	.db #0x3f	; 63
   5510 3F                  185 	.db #0x3f	; 63
   5511 3F                  186 	.db #0x3f	; 63
   5512 3F                  187 	.db #0x3f	; 63
   5513 2A                  188 	.db #0x2a	; 42
   5514 2A                  189 	.db #0x2a	; 42
   5515 00                  190 	.db #0x00	; 0
   5516 00                  191 	.db #0x00	; 0
   5517 15                  192 	.db #0x15	; 21
   5518 2A                  193 	.db #0x2a	; 42
   5519 2A                  194 	.db #0x2a	; 42
   551A 00                  195 	.db #0x00	; 0
   551B 00                  196 	.db #0x00	; 0
   551C 15                  197 	.db #0x15	; 21
   551D 2A                  198 	.db #0x2a	; 42
   551E 2A                  199 	.db #0x2a	; 42
   551F 00                  200 	.db #0x00	; 0
   5520 00                  201 	.db #0x00	; 0
   5521 15                  202 	.db #0x15	; 21
   5522 2A                  203 	.db #0x2a	; 42
   5523 2A                  204 	.db #0x2a	; 42
   5524 00                  205 	.db #0x00	; 0
   5525 00                  206 	.db #0x00	; 0
   5526 15                  207 	.db #0x15	; 21
   5527 2A                  208 	.db #0x2a	; 42
   5528 2A                  209 	.db #0x2a	; 42
   5529 00                  210 	.db #0x00	; 0
   552A 00                  211 	.db #0x00	; 0
   552B 15                  212 	.db #0x15	; 21
   552C 2A                  213 	.db #0x2a	; 42
   552D 2A                  214 	.db #0x2a	; 42
   552E 00                  215 	.db #0x00	; 0
   552F 00                  216 	.db #0x00	; 0
   5530 15                  217 	.db #0x15	; 21
   5531 3F                  218 	.db #0x3f	; 63
   5532 3F                  219 	.db #0x3f	; 63
   5533 3F                  220 	.db #0x3f	; 63
   5534 3F                  221 	.db #0x3f	; 63
   5535 3F                  222 	.db #0x3f	; 63
   5536 2A                  223 	.db #0x2a	; 42
   5537 2A                  224 	.db #0x2a	; 42
   5538 00                  225 	.db #0x00	; 0
   5539 00                  226 	.db #0x00	; 0
   553A 15                  227 	.db #0x15	; 21
   553B 2A                  228 	.db #0x2a	; 42
   553C 2A                  229 	.db #0x2a	; 42
   553D 00                  230 	.db #0x00	; 0
   553E 00                  231 	.db #0x00	; 0
   553F 15                  232 	.db #0x15	; 21
   5540 2A                  233 	.db #0x2a	; 42
   5541 2A                  234 	.db #0x2a	; 42
   5542 00                  235 	.db #0x00	; 0
   5543 00                  236 	.db #0x00	; 0
   5544 15                  237 	.db #0x15	; 21
   5545 2A                  238 	.db #0x2a	; 42
   5546 2A                  239 	.db #0x2a	; 42
   5547 00                  240 	.db #0x00	; 0
   5548 00                  241 	.db #0x00	; 0
   5549 15                  242 	.db #0x15	; 21
   554A 2A                  243 	.db #0x2a	; 42
   554B 2A                  244 	.db #0x2a	; 42
   554C 00                  245 	.db #0x00	; 0
   554D 00                  246 	.db #0x00	; 0
   554E 15                  247 	.db #0x15	; 21
   554F 3F                  248 	.db #0x3f	; 63
   5550 3F                  249 	.db #0x3f	; 63
   5551 3F                  250 	.db #0x3f	; 63
   5552 3F                  251 	.db #0x3f	; 63
   5553 3F                  252 	.db #0x3f	; 63
   5554                     253 _enemy_kind2_sprite:
   5554 0F                  254 	.db #0x0f	; 15
   5555 0F                  255 	.db #0x0f	; 15
   5556 0F                  256 	.db #0x0f	; 15
   5557 0F                  257 	.db #0x0f	; 15
   5558 0F                  258 	.db #0x0f	; 15
   5559 0F                  259 	.db #0x0f	; 15
   555A 0A                  260 	.db #0x0a	; 10
   555B 05                  261 	.db #0x05	; 5
   555C 00                  262 	.db #0x00	; 0
   555D 00                  263 	.db #0x00	; 0
   555E 00                  264 	.db #0x00	; 0
   555F 05                  265 	.db #0x05	; 5
   5560 0A                  266 	.db #0x0a	; 10
   5561 05                  267 	.db #0x05	; 5
   5562 00                  268 	.db #0x00	; 0
   5563 00                  269 	.db #0x00	; 0
   5564 00                  270 	.db #0x00	; 0
   5565 05                  271 	.db #0x05	; 5
   5566 0A                  272 	.db #0x0a	; 10
   5567 05                  273 	.db #0x05	; 5
   5568 00                  274 	.db #0x00	; 0
   5569 00                  275 	.db #0x00	; 0
   556A 00                  276 	.db #0x00	; 0
   556B 05                  277 	.db #0x05	; 5
   556C 0A                  278 	.db #0x0a	; 10
   556D 05                  279 	.db #0x05	; 5
   556E 00                  280 	.db #0x00	; 0
   556F 00                  281 	.db #0x00	; 0
   5570 00                  282 	.db #0x00	; 0
   5571 05                  283 	.db #0x05	; 5
   5572 0F                  284 	.db #0x0f	; 15
   5573 0F                  285 	.db #0x0f	; 15
   5574 0F                  286 	.db #0x0f	; 15
   5575 0F                  287 	.db #0x0f	; 15
   5576 0F                  288 	.db #0x0f	; 15
   5577 0F                  289 	.db #0x0f	; 15
   5578 0A                  290 	.db #0x0a	; 10
   5579 05                  291 	.db #0x05	; 5
   557A 00                  292 	.db #0x00	; 0
   557B 00                  293 	.db #0x00	; 0
   557C 00                  294 	.db #0x00	; 0
   557D 05                  295 	.db #0x05	; 5
   557E 0A                  296 	.db #0x0a	; 10
   557F 05                  297 	.db #0x05	; 5
   5580 00                  298 	.db #0x00	; 0
   5581 00                  299 	.db #0x00	; 0
   5582 00                  300 	.db #0x00	; 0
   5583 05                  301 	.db #0x05	; 5
   5584 0A                  302 	.db #0x0a	; 10
   5585 05                  303 	.db #0x05	; 5
   5586 00                  304 	.db #0x00	; 0
   5587 00                  305 	.db #0x00	; 0
   5588 00                  306 	.db #0x00	; 0
   5589 05                  307 	.db #0x05	; 5
   558A 0F                  308 	.db #0x0f	; 15
   558B 0F                  309 	.db #0x0f	; 15
   558C 0F                  310 	.db #0x0f	; 15
   558D 0F                  311 	.db #0x0f	; 15
   558E 0F                  312 	.db #0x0f	; 15
   558F 0F                  313 	.db #0x0f	; 15
   5590                     314 _enemy_kind3_sprite:
   5590 33                  315 	.db #0x33	; 51	'3'
   5591 33                  316 	.db #0x33	; 51	'3'
   5592 33                  317 	.db #0x33	; 51	'3'
   5593 33                  318 	.db #0x33	; 51	'3'
   5594 33                  319 	.db #0x33	; 51	'3'
   5595 33                  320 	.db #0x33	; 51	'3'
   5596 33                  321 	.db #0x33	; 51	'3'
   5597 33                  322 	.db #0x33	; 51	'3'
   5598 33                  323 	.db #0x33	; 51	'3'
   5599 33                  324 	.db #0x33	; 51	'3'
   559A 22                  325 	.db #0x22	; 34
   559B 00                  326 	.db #0x00	; 0
   559C 22                  327 	.db #0x22	; 34
   559D 00                  328 	.db #0x00	; 0
   559E 00                  329 	.db #0x00	; 0
   559F 00                  330 	.db #0x00	; 0
   55A0 00                  331 	.db #0x00	; 0
   55A1 00                  332 	.db #0x00	; 0
   55A2 00                  333 	.db #0x00	; 0
   55A3 11                  334 	.db #0x11	; 17
   55A4 22                  335 	.db #0x22	; 34
   55A5 00                  336 	.db #0x00	; 0
   55A6 22                  337 	.db #0x22	; 34
   55A7 00                  338 	.db #0x00	; 0
   55A8 00                  339 	.db #0x00	; 0
   55A9 00                  340 	.db #0x00	; 0
   55AA 00                  341 	.db #0x00	; 0
   55AB 00                  342 	.db #0x00	; 0
   55AC 00                  343 	.db #0x00	; 0
   55AD 11                  344 	.db #0x11	; 17
   55AE 22                  345 	.db #0x22	; 34
   55AF 00                  346 	.db #0x00	; 0
   55B0 22                  347 	.db #0x22	; 34
   55B1 00                  348 	.db #0x00	; 0
   55B2 00                  349 	.db #0x00	; 0
   55B3 00                  350 	.db #0x00	; 0
   55B4 00                  351 	.db #0x00	; 0
   55B5 00                  352 	.db #0x00	; 0
   55B6 00                  353 	.db #0x00	; 0
   55B7 11                  354 	.db #0x11	; 17
   55B8 22                  355 	.db #0x22	; 34
   55B9 00                  356 	.db #0x00	; 0
   55BA 22                  357 	.db #0x22	; 34
   55BB 00                  358 	.db #0x00	; 0
   55BC 00                  359 	.db #0x00	; 0
   55BD 00                  360 	.db #0x00	; 0
   55BE 00                  361 	.db #0x00	; 0
   55BF 00                  362 	.db #0x00	; 0
   55C0 00                  363 	.db #0x00	; 0
   55C1 11                  364 	.db #0x11	; 17
   55C2 22                  365 	.db #0x22	; 34
   55C3 00                  366 	.db #0x00	; 0
   55C4 22                  367 	.db #0x22	; 34
   55C5 00                  368 	.db #0x00	; 0
   55C6 00                  369 	.db #0x00	; 0
   55C7 00                  370 	.db #0x00	; 0
   55C8 00                  371 	.db #0x00	; 0
   55C9 00                  372 	.db #0x00	; 0
   55CA 00                  373 	.db #0x00	; 0
   55CB 11                  374 	.db #0x11	; 17
   55CC 22                  375 	.db #0x22	; 34
   55CD 00                  376 	.db #0x00	; 0
   55CE 22                  377 	.db #0x22	; 34
   55CF 00                  378 	.db #0x00	; 0
   55D0 00                  379 	.db #0x00	; 0
   55D1 00                  380 	.db #0x00	; 0
   55D2 00                  381 	.db #0x00	; 0
   55D3 00                  382 	.db #0x00	; 0
   55D4 00                  383 	.db #0x00	; 0
   55D5 11                  384 	.db #0x11	; 17
   55D6 22                  385 	.db #0x22	; 34
   55D7 00                  386 	.db #0x00	; 0
   55D8 22                  387 	.db #0x22	; 34
   55D9 00                  388 	.db #0x00	; 0
   55DA 00                  389 	.db #0x00	; 0
   55DB 00                  390 	.db #0x00	; 0
   55DC 00                  391 	.db #0x00	; 0
   55DD 00                  392 	.db #0x00	; 0
   55DE 00                  393 	.db #0x00	; 0
   55DF 11                  394 	.db #0x11	; 17
   55E0 22                  395 	.db #0x22	; 34
   55E1 00                  396 	.db #0x00	; 0
   55E2 22                  397 	.db #0x22	; 34
   55E3 00                  398 	.db #0x00	; 0
   55E4 00                  399 	.db #0x00	; 0
   55E5 00                  400 	.db #0x00	; 0
   55E6 00                  401 	.db #0x00	; 0
   55E7 00                  402 	.db #0x00	; 0
   55E8 00                  403 	.db #0x00	; 0
   55E9 11                  404 	.db #0x11	; 17
   55EA 33                  405 	.db #0x33	; 51	'3'
   55EB 33                  406 	.db #0x33	; 51	'3'
   55EC 33                  407 	.db #0x33	; 51	'3'
   55ED 33                  408 	.db #0x33	; 51	'3'
   55EE 33                  409 	.db #0x33	; 51	'3'
   55EF 33                  410 	.db #0x33	; 51	'3'
   55F0 33                  411 	.db #0x33	; 51	'3'
   55F1 33                  412 	.db #0x33	; 51	'3'
   55F2 33                  413 	.db #0x33	; 51	'3'
   55F3 33                  414 	.db #0x33	; 51	'3'
   55F4 22                  415 	.db #0x22	; 34
   55F5 00                  416 	.db #0x00	; 0
   55F6 22                  417 	.db #0x22	; 34
   55F7 00                  418 	.db #0x00	; 0
   55F8 00                  419 	.db #0x00	; 0
   55F9 00                  420 	.db #0x00	; 0
   55FA 00                  421 	.db #0x00	; 0
   55FB 00                  422 	.db #0x00	; 0
   55FC 00                  423 	.db #0x00	; 0
   55FD 11                  424 	.db #0x11	; 17
   55FE 22                  425 	.db #0x22	; 34
   55FF 00                  426 	.db #0x00	; 0
   5600 22                  427 	.db #0x22	; 34
   5601 00                  428 	.db #0x00	; 0
   5602 00                  429 	.db #0x00	; 0
   5603 00                  430 	.db #0x00	; 0
   5604 00                  431 	.db #0x00	; 0
   5605 00                  432 	.db #0x00	; 0
   5606 00                  433 	.db #0x00	; 0
   5607 11                  434 	.db #0x11	; 17
   5608 22                  435 	.db #0x22	; 34
   5609 00                  436 	.db #0x00	; 0
   560A 22                  437 	.db #0x22	; 34
   560B 00                  438 	.db #0x00	; 0
   560C 00                  439 	.db #0x00	; 0
   560D 00                  440 	.db #0x00	; 0
   560E 00                  441 	.db #0x00	; 0
   560F 00                  442 	.db #0x00	; 0
   5610 00                  443 	.db #0x00	; 0
   5611 11                  444 	.db #0x11	; 17
   5612 22                  445 	.db #0x22	; 34
   5613 00                  446 	.db #0x00	; 0
   5614 22                  447 	.db #0x22	; 34
   5615 00                  448 	.db #0x00	; 0
   5616 00                  449 	.db #0x00	; 0
   5617 00                  450 	.db #0x00	; 0
   5618 00                  451 	.db #0x00	; 0
   5619 00                  452 	.db #0x00	; 0
   561A 00                  453 	.db #0x00	; 0
   561B 11                  454 	.db #0x11	; 17
   561C 22                  455 	.db #0x22	; 34
   561D 00                  456 	.db #0x00	; 0
   561E 22                  457 	.db #0x22	; 34
   561F 00                  458 	.db #0x00	; 0
   5620 00                  459 	.db #0x00	; 0
   5621 00                  460 	.db #0x00	; 0
   5622 00                  461 	.db #0x00	; 0
   5623 00                  462 	.db #0x00	; 0
   5624 00                  463 	.db #0x00	; 0
   5625 11                  464 	.db #0x11	; 17
   5626 22                  465 	.db #0x22	; 34
   5627 00                  466 	.db #0x00	; 0
   5628 22                  467 	.db #0x22	; 34
   5629 00                  468 	.db #0x00	; 0
   562A 00                  469 	.db #0x00	; 0
   562B 00                  470 	.db #0x00	; 0
   562C 00                  471 	.db #0x00	; 0
   562D 00                  472 	.db #0x00	; 0
   562E 00                  473 	.db #0x00	; 0
   562F 11                  474 	.db #0x11	; 17
   5630 22                  475 	.db #0x22	; 34
   5631 00                  476 	.db #0x00	; 0
   5632 22                  477 	.db #0x22	; 34
   5633 00                  478 	.db #0x00	; 0
   5634 00                  479 	.db #0x00	; 0
   5635 00                  480 	.db #0x00	; 0
   5636 00                  481 	.db #0x00	; 0
   5637 00                  482 	.db #0x00	; 0
   5638 00                  483 	.db #0x00	; 0
   5639 11                  484 	.db #0x11	; 17
   563A 33                  485 	.db #0x33	; 51	'3'
   563B 33                  486 	.db #0x33	; 51	'3'
   563C 33                  487 	.db #0x33	; 51	'3'
   563D 33                  488 	.db #0x33	; 51	'3'
   563E 33                  489 	.db #0x33	; 51	'3'
   563F 33                  490 	.db #0x33	; 51	'3'
   5640 33                  491 	.db #0x33	; 51	'3'
   5641 33                  492 	.db #0x33	; 51	'3'
   5642 33                  493 	.db #0x33	; 51	'3'
   5643 33                  494 	.db #0x33	; 51	'3'
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   5644                     499 _enemyspawn::
   5644 DD E5         [15]  500 	push	ix
   5646 DD 21 00 00   [14]  501 	ld	ix,#0
   564A DD 39         [15]  502 	add	ix,sp
   564C 21 F1 FF      [10]  503 	ld	hl, #-15
   564F 39            [11]  504 	add	hl, sp
   5650 F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   5651 DD 7E 05      [19]  507 	ld	a, 5 (ix)
   5654 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   5657 CA 17 58      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   565A DD 7E 04      [19]  512 	ld	a, 4 (ix)
   565D DD 77 FE      [19]  513 	ld	-2 (ix), a
   5660 DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5663 DD 77 FF      [19]  515 	ld	-1 (ix), a
   5666 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   5669 DD 66 FF      [19]  517 	ld	h,-1 (ix)
   566C DD 7E 06      [19]  518 	ld	a, 6 (ix)
   566F 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   5670 DD 4E FE      [19]  521 	ld	c,-2 (ix)
   5673 DD 46 FF      [19]  522 	ld	b,-1 (ix)
   5676 03            [ 6]  523 	inc	bc
   5677 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   567A 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   567B DD 7E FE      [19]  527 	ld	a, -2 (ix)
   567E C6 02         [ 7]  528 	add	a, #0x02
   5680 DD 77 FC      [19]  529 	ld	-4 (ix), a
   5683 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5686 CE 00         [ 7]  531 	adc	a, #0x00
   5688 DD 77 FD      [19]  532 	ld	-3 (ix), a
   568B DD 7E 09      [19]  533 	ld	a, 9 (ix)
   568E B7            [ 4]  534 	or	a, a
   568F 28 04         [12]  535 	jr	Z,00114$
   5691 0E 01         [ 7]  536 	ld	c, #0x01
   5693 18 02         [12]  537 	jr	00115$
   5695                     538 00114$:
   5695 0E FF         [ 7]  539 	ld	c, #0xff
   5697                     540 00115$:
   5697 DD 6E FC      [19]  541 	ld	l,-4 (ix)
   569A DD 66 FD      [19]  542 	ld	h,-3 (ix)
   569D 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   569E DD 7E FE      [19]  545 	ld	a, -2 (ix)
   56A1 C6 03         [ 7]  546 	add	a, #0x03
   56A3 DD 77 FA      [19]  547 	ld	-6 (ix), a
   56A6 DD 7E FF      [19]  548 	ld	a, -1 (ix)
   56A9 CE 00         [ 7]  549 	adc	a, #0x00
   56AB DD 77 FB      [19]  550 	ld	-5 (ix), a
   56AE DD 6E FA      [19]  551 	ld	l,-6 (ix)
   56B1 DD 66 FB      [19]  552 	ld	h,-5 (ix)
   56B4 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   56B6 DD 7E FE      [19]  555 	ld	a, -2 (ix)
   56B9 C6 06         [ 7]  556 	add	a, #0x06
   56BB DD 77 F8      [19]  557 	ld	-8 (ix), a
   56BE DD 7E FF      [19]  558 	ld	a, -1 (ix)
   56C1 CE 00         [ 7]  559 	adc	a, #0x00
   56C3 DD 77 F9      [19]  560 	ld	-7 (ix), a
   56C6 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   56C9 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   56CC 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   56CE DD 7E FE      [19]  565 	ld	a, -2 (ix)
   56D1 C6 09         [ 7]  566 	add	a, #0x09
   56D3 DD 77 F8      [19]  567 	ld	-8 (ix), a
   56D6 DD 7E FF      [19]  568 	ld	a, -1 (ix)
   56D9 CE 00         [ 7]  569 	adc	a, #0x00
   56DB DD 77 F9      [19]  570 	ld	-7 (ix), a
   56DE DD 6E F8      [19]  571 	ld	l,-8 (ix)
   56E1 DD 66 F9      [19]  572 	ld	h,-7 (ix)
   56E4 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   56E7 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   56E8 DD 7E FE      [19]  576 	ld	a, -2 (ix)
   56EB C6 04         [ 7]  577 	add	a, #0x04
   56ED DD 77 F8      [19]  578 	ld	-8 (ix), a
   56F0 DD 7E FF      [19]  579 	ld	a, -1 (ix)
   56F3 CE 00         [ 7]  580 	adc	a, #0x00
   56F5 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   56F8 DD 7E FE      [19]  583 	ld	a, -2 (ix)
   56FB C6 05         [ 7]  584 	add	a, #0x05
   56FD DD 77 F6      [19]  585 	ld	-10 (ix), a
   5700 DD 7E FF      [19]  586 	ld	a, -1 (ix)
   5703 CE 00         [ 7]  587 	adc	a, #0x00
   5705 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   5708 DD 7E FE      [19]  590 	ld	a, -2 (ix)
   570B C6 07         [ 7]  591 	add	a, #0x07
   570D DD 77 F4      [19]  592 	ld	-12 (ix), a
   5710 DD 7E FF      [19]  593 	ld	a, -1 (ix)
   5713 CE 00         [ 7]  594 	adc	a, #0x00
   5715 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   5718 DD 7E FE      [19]  597 	ld	a, -2 (ix)
   571B C6 08         [ 7]  598 	add	a, #0x08
   571D DD 77 FE      [19]  599 	ld	-2 (ix), a
   5720 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   5723 CE 00         [ 7]  601 	adc	a, #0x00
   5725 DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   5728 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   572B 3D            [ 4]  605 	dec	a
   572C 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   572E DD 6E F8      [19]  608 	ld	l,-8 (ix)
   5731 DD 66 F9      [19]  609 	ld	h,-7 (ix)
   5734 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   5736 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   5739 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   573C 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   573E DD 6E F4      [19]  616 	ld	l,-12 (ix)
   5741 DD 66 F5      [19]  617 	ld	h,-11 (ix)
   5744 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   5746 DD 6E FE      [19]  620 	ld	l,-2 (ix)
   5749 DD 66 FF      [19]  621 	ld	h,-1 (ix)
   574C 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   574E DD 7E FC      [19]  624 	ld	a, -4 (ix)
   5751 DD 77 F2      [19]  625 	ld	-14 (ix), a
   5754 DD 7E FD      [19]  626 	ld	a, -3 (ix)
   5757 DD 77 F3      [19]  627 	ld	-13 (ix), a
   575A DD 7E 09      [19]  628 	ld	a, 9 (ix)
   575D B7            [ 4]  629 	or	a, a
   575E 28 06         [12]  630 	jr	Z,00116$
   5760 DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5764 18 04         [12]  632 	jr	00117$
   5766                     633 00116$:
   5766 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   576A                     635 00117$:
   576A DD 6E F2      [19]  636 	ld	l,-14 (ix)
   576D DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5770 DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5773 77            [ 7]  639 	ld	(hl), a
   5774 C3 17 58      [10]  640 	jp	00112$
   5777                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   5777 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   577A D6 02         [ 7]  644 	sub	a, #0x02
   577C 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   577E DD 6E F8      [19]  647 	ld	l,-8 (ix)
   5781 DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5784 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5786 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   5789 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   578C 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   578E DD 6E F4      [19]  655 	ld	l,-12 (ix)
   5791 DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5794 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5796 DD 6E FE      [19]  659 	ld	l,-2 (ix)
   5799 DD 66 FF      [19]  660 	ld	h,-1 (ix)
   579C 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   579E DD 4E FA      [19]  663 	ld	c,-6 (ix)
   57A1 DD 46 FB      [19]  664 	ld	b,-5 (ix)
   57A4 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   57A7 B7            [ 4]  666 	or	a, a
   57A8 28 04         [12]  667 	jr	Z,00118$
   57AA 3E 01         [ 7]  668 	ld	a, #0x01
   57AC 18 02         [12]  669 	jr	00119$
   57AE                     670 00118$:
   57AE 3E FF         [ 7]  671 	ld	a, #0xff
   57B0                     672 00119$:
   57B0 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   57B1 DD 6E FC      [19]  675 	ld	l,-4 (ix)
   57B4 DD 66 FD      [19]  676 	ld	h,-3 (ix)
   57B7 36 01         [10]  677 	ld	(hl), #0x01
   57B9 18 5C         [12]  678 	jr	00112$
   57BB                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   57BB DD 7E 08      [19]  681 	ld	a, 8 (ix)
   57BE D6 03         [ 7]  682 	sub	a, #0x03
   57C0 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   57C2 DD 6E F8      [19]  685 	ld	l,-8 (ix)
   57C5 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   57C8 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   57CA DD 6E F6      [19]  689 	ld	l,-10 (ix)
   57CD DD 66 F7      [19]  690 	ld	h,-9 (ix)
   57D0 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   57D2 DD 6E F4      [19]  693 	ld	l,-12 (ix)
   57D5 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   57D8 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   57DA DD 6E FE      [19]  697 	ld	l,-2 (ix)
   57DD DD 66 FF      [19]  698 	ld	h,-1 (ix)
   57E0 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   57E2 DD 4E FC      [19]  701 	ld	c,-4 (ix)
   57E5 DD 46 FD      [19]  702 	ld	b,-3 (ix)
   57E8 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   57EB B7            [ 4]  704 	or	a, a
   57EC 28 04         [12]  705 	jr	Z,00120$
   57EE 3E 01         [ 7]  706 	ld	a, #0x01
   57F0 18 02         [12]  707 	jr	00121$
   57F2                     708 00120$:
   57F2 3E FF         [ 7]  709 	ld	a, #0xff
   57F4                     710 00121$:
   57F4 02            [ 7]  711 	ld	(bc), a
   57F5 18 20         [12]  712 	jr	00112$
   57F7                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   57F7 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   57FA DD 66 F9      [19]  716 	ld	h,-7 (ix)
   57FD 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   57FF DD 6E F6      [19]  719 	ld	l,-10 (ix)
   5802 DD 66 F7      [19]  720 	ld	h,-9 (ix)
   5805 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   5807 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   580A DD 66 F5      [19]  724 	ld	h,-11 (ix)
   580D 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   580F DD 6E FE      [19]  727 	ld	l,-2 (ix)
   5812 DD 66 FF      [19]  728 	ld	h,-1 (ix)
   5815 36 64         [10]  729 	ld	(hl), #0x64
   5817                     730 00112$:
   5817 DD F9         [10]  731 	ld	sp, ix
   5819 DD E1         [14]  732 	pop	ix
   581B C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   581C                     738 _enemyupdate::
   581C DD E5         [15]  739 	push	ix
   581E DD 21 00 00   [14]  740 	ld	ix,#0
   5822 DD 39         [15]  741 	add	ix,sp
   5824 21 F6 FF      [10]  742 	ld	hl, #-10
   5827 39            [11]  743 	add	hl, sp
   5828 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   5829 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   582C DD B6 04      [19]  747 	or	a,4 (ix)
   582F CA 23 5A      [10]  748 	jp	Z,00121$
   5832 DD 7E 04      [19]  749 	ld	a, 4 (ix)
   5835 DD 77 FE      [19]  750 	ld	-2 (ix), a
   5838 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   583B DD 77 FF      [19]  752 	ld	-1 (ix), a
   583E DD 6E FE      [19]  753 	ld	l,-2 (ix)
   5841 DD 66 FF      [19]  754 	ld	h,-1 (ix)
   5844 11 06 00      [10]  755 	ld	de, #0x0006
   5847 19            [11]  756 	add	hl, de
   5848 7E            [ 7]  757 	ld	a, (hl)
   5849 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   584A CA 23 5A      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   584D DD 6E FE      [19]  762 	ld	l,-2 (ix)
   5850 DD 66 FF      [19]  763 	ld	h,-1 (ix)
   5853 11 09 00      [10]  764 	ld	de, #0x0009
   5856 19            [11]  765 	add	hl, de
   5857 7E            [ 7]  766 	ld	a, (hl)
   5858 DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   585B DD 6E FE      [19]  769 	ld	l,-2 (ix)
   585E DD 66 FF      [19]  770 	ld	h,-1 (ix)
   5861 4E            [ 7]  771 	ld	c, (hl)
   5862 DD 7E FE      [19]  772 	ld	a, -2 (ix)
   5865 C6 02         [ 7]  773 	add	a, #0x02
   5867 DD 77 FB      [19]  774 	ld	-5 (ix), a
   586A DD 7E FF      [19]  775 	ld	a, -1 (ix)
   586D CE 00         [ 7]  776 	adc	a, #0x00
   586F DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5872 DD 7E FE      [19]  779 	ld	a, -2 (ix)
   5875 C6 01         [ 7]  780 	add	a, #0x01
   5877 DD 77 F9      [19]  781 	ld	-7 (ix), a
   587A DD 7E FF      [19]  782 	ld	a, -1 (ix)
   587D CE 00         [ 7]  783 	adc	a, #0x00
   587F DD 77 FA      [19]  784 	ld	-6 (ix), a
   5882 DD 5E FE      [19]  785 	ld	e,-2 (ix)
   5885 DD 56 FF      [19]  786 	ld	d,-1 (ix)
   5888 13            [ 6]  787 	inc	de
   5889 13            [ 6]  788 	inc	de
   588A 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   588B 06 00         [ 7]  791 	ld	b, #0x00
   588D DD 6E FB      [19]  792 	ld	l,-5 (ix)
   5890 DD 66 FC      [19]  793 	ld	h,-4 (ix)
   5893 7E            [ 7]  794 	ld	a, (hl)
   5894 DD 77 F8      [19]  795 	ld	-8 (ix), a
   5897 6F            [ 4]  796 	ld	l, a
   5898 DD 7E F8      [19]  797 	ld	a, -8 (ix)
   589B 17            [ 4]  798 	rla
   589C 9F            [ 4]  799 	sbc	a, a
   589D 67            [ 4]  800 	ld	h, a
   589E 09            [11]  801 	add	hl,bc
   589F 4D            [ 4]  802 	ld	c, l
   58A0 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   58A1 DD 7E FD      [19]  805 	ld	a, -3 (ix)
   58A4 D6 02         [ 7]  806 	sub	a, #0x02
   58A6 C2 4F 59      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   58A9 DD 6E F9      [19]  810 	ld	l,-7 (ix)
   58AC DD 66 FA      [19]  811 	ld	h,-6 (ix)
   58AF 6E            [ 7]  812 	ld	l, (hl)
   58B0 DD 75 F6      [19]  813 	ld	-10 (ix), l
   58B3 DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   58B7 1A            [ 7]  815 	ld	a, (de)
   58B8 6F            [ 4]  816 	ld	l, a
   58B9 17            [ 4]  817 	rla
   58BA 9F            [ 4]  818 	sbc	a, a
   58BB 67            [ 4]  819 	ld	h, a
   58BC DD 7E F6      [19]  820 	ld	a, -10 (ix)
   58BF 85            [ 4]  821 	add	a, l
   58C0 DD 77 F6      [19]  822 	ld	-10 (ix), a
   58C3 DD 7E F7      [19]  823 	ld	a, -9 (ix)
   58C6 8C            [ 4]  824 	adc	a, h
   58C7 DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   58CA 79            [ 4]  827 	ld	a, c
   58CB D6 08         [ 7]  828 	sub	a, #0x08
   58CD 78            [ 4]  829 	ld	a, b
   58CE 17            [ 4]  830 	rla
   58CF 3F            [ 4]  831 	ccf
   58D0 1F            [ 4]  832 	rra
   58D1 DE 80         [ 7]  833 	sbc	a, #0x80
   58D3 38 0E         [12]  834 	jr	C,00104$
   58D5 3E 48         [ 7]  835 	ld	a, #0x48
   58D7 B9            [ 4]  836 	cp	a, c
   58D8 3E 00         [ 7]  837 	ld	a, #0x00
   58DA 98            [ 4]  838 	sbc	a, b
   58DB E2 E0 58      [10]  839 	jp	PO, 00161$
   58DE EE 80         [ 7]  840 	xor	a, #0x80
   58E0                     841 00161$:
   58E0 F2 FE 58      [10]  842 	jp	P, 00105$
   58E3                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   58E3 AF            [ 4]  845 	xor	a, a
   58E4 DD 96 F8      [19]  846 	sub	a, -8 (ix)
   58E7 4F            [ 4]  847 	ld	c, a
   58E8 DD 6E FB      [19]  848 	ld	l,-5 (ix)
   58EB DD 66 FC      [19]  849 	ld	h,-4 (ix)
   58EE 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   58EF DD 6E FE      [19]  852 	ld	l,-2 (ix)
   58F2 DD 66 FF      [19]  853 	ld	h,-1 (ix)
   58F5 6E            [ 7]  854 	ld	l, (hl)
   58F6 26 00         [ 7]  855 	ld	h, #0x00
   58F8 79            [ 4]  856 	ld	a, c
   58F9 17            [ 4]  857 	rla
   58FA 9F            [ 4]  858 	sbc	a, a
   58FB 47            [ 4]  859 	ld	b, a
   58FC 09            [11]  860 	add	hl,bc
   58FD 4D            [ 4]  861 	ld	c, l
   58FE                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   58FE DD 7E F6      [19]  864 	ld	a, -10 (ix)
   5901 D6 38         [ 7]  865 	sub	a, #0x38
   5903 DD 7E F7      [19]  866 	ld	a, -9 (ix)
   5906 17            [ 4]  867 	rla
   5907 3F            [ 4]  868 	ccf
   5908 1F            [ 4]  869 	rra
   5909 DE 80         [ 7]  870 	sbc	a, #0x80
   590B 38 12         [12]  871 	jr	C,00107$
   590D 3E 78         [ 7]  872 	ld	a, #0x78
   590F DD BE F6      [19]  873 	cp	a, -10 (ix)
   5912 3E 00         [ 7]  874 	ld	a, #0x00
   5914 DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   5917 E2 1C 59      [10]  876 	jp	PO, 00162$
   591A EE 80         [ 7]  877 	xor	a, #0x80
   591C                     878 00162$:
   591C F2 3B 59      [10]  879 	jp	P, 00108$
   591F                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   591F 1A            [ 7]  882 	ld	a, (de)
   5920 6F            [ 4]  883 	ld	l, a
   5921 AF            [ 4]  884 	xor	a, a
   5922 95            [ 4]  885 	sub	a, l
   5923 DD 77 F8      [19]  886 	ld	-8 (ix), a
   5926 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   5927 DD 6E F9      [19]  889 	ld	l,-7 (ix)
   592A DD 66 FA      [19]  890 	ld	h,-6 (ix)
   592D 5E            [ 7]  891 	ld	e, (hl)
   592E 16 00         [ 7]  892 	ld	d, #0x00
   5930 DD 6E F8      [19]  893 	ld	l, -8 (ix)
   5933 DD 7E F8      [19]  894 	ld	a, -8 (ix)
   5936 17            [ 4]  895 	rla
   5937 9F            [ 4]  896 	sbc	a, a
   5938 67            [ 4]  897 	ld	h, a
   5939 19            [11]  898 	add	hl,de
   593A E3            [19]  899 	ex	(sp), hl
   593B                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   593B DD 6E FE      [19]  902 	ld	l,-2 (ix)
   593E DD 66 FF      [19]  903 	ld	h,-1 (ix)
   5941 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   5942 DD 4E F6      [19]  906 	ld	c, -10 (ix)
   5945 DD 6E F9      [19]  907 	ld	l,-7 (ix)
   5948 DD 66 FA      [19]  908 	ld	h,-6 (ix)
   594B 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   594C C3 23 5A      [10]  911 	jp	00121$
   594F                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   594F 79            [ 4]  915 	ld	a, c
   5950 D6 02         [ 7]  916 	sub	a, #0x02
   5952 78            [ 4]  917 	ld	a, b
   5953 17            [ 4]  918 	rla
   5954 3F            [ 4]  919 	ccf
   5955 1F            [ 4]  920 	rra
   5956 DE 80         [ 7]  921 	sbc	a, #0x80
   5958 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   595A 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   595D DD 6E FB      [19]  926 	ld	l,-5 (ix)
   5960 DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5963 36 01         [10]  928 	ld	(hl), #0x01
   5965                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5965 DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5968 DD 66 FF      [19]  932 	ld	h,-1 (ix)
   596B 23            [ 6]  933 	inc	hl
   596C 23            [ 6]  934 	inc	hl
   596D 23            [ 6]  935 	inc	hl
   596E 23            [ 6]  936 	inc	hl
   596F 6E            [ 7]  937 	ld	l, (hl)
   5970 26 00         [ 7]  938 	ld	h, #0x00
   5972 3E 50         [ 7]  939 	ld	a, #0x50
   5974 95            [ 4]  940 	sub	a, l
   5975 6F            [ 4]  941 	ld	l, a
   5976 3E 00         [ 7]  942 	ld	a, #0x00
   5978 9C            [ 4]  943 	sbc	a, h
   5979 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   597A 7D            [ 4]  946 	ld	a, l
   597B 91            [ 4]  947 	sub	a, c
   597C 7C            [ 4]  948 	ld	a, h
   597D 98            [ 4]  949 	sbc	a, b
   597E E2 83 59      [10]  950 	jp	PO, 00163$
   5981 EE 80         [ 7]  951 	xor	a, #0x80
   5983                     952 00163$:
   5983 F2 8F 59      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5986 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5987 DD 6E FB      [19]  957 	ld	l,-5 (ix)
   598A DD 66 FC      [19]  958 	ld	h,-4 (ix)
   598D 36 FF         [10]  959 	ld	(hl), #0xff
   598F                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   598F DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5992 DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5995 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5996 1A            [ 7]  966 	ld	a, (de)
   5997 4F            [ 4]  967 	ld	c, a
   5998 0C            [ 4]  968 	inc	c
   5999 79            [ 4]  969 	ld	a, c
   599A 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   599B 3E 03         [ 7]  972 	ld	a, #0x03
   599D 91            [ 4]  973 	sub	a, c
   599E E2 A3 59      [10]  974 	jp	PO, 00164$
   59A1 EE 80         [ 7]  975 	xor	a, #0x80
   59A3                     976 00164$:
   59A3 F2 A9 59      [10]  977 	jp	P, 00117$
   59A6 3E 03         [ 7]  978 	ld	a, #0x03
   59A8 12            [ 7]  979 	ld	(de), a
   59A9                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   59A9 DD 6E F9      [19]  982 	ld	l,-7 (ix)
   59AC DD 66 FA      [19]  983 	ld	h,-6 (ix)
   59AF 4E            [ 7]  984 	ld	c, (hl)
   59B0 06 00         [ 7]  985 	ld	b, #0x00
   59B2 1A            [ 7]  986 	ld	a, (de)
   59B3 6F            [ 4]  987 	ld	l, a
   59B4 17            [ 4]  988 	rla
   59B5 9F            [ 4]  989 	sbc	a, a
   59B6 67            [ 4]  990 	ld	h, a
   59B7 09            [11]  991 	add	hl, bc
   59B8 E5            [11]  992 	push	hl
   59B9 FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   59BB DD 7E FE      [19]  995 	ld	a, -2 (ix)
   59BE C6 05         [ 7]  996 	add	a, #0x05
   59C0 DD 77 F6      [19]  997 	ld	-10 (ix), a
   59C3 DD 7E FF      [19]  998 	ld	a, -1 (ix)
   59C6 CE 00         [ 7]  999 	adc	a, #0x00
   59C8 DD 77 F7      [19] 1000 	ld	-9 (ix), a
   59CB E1            [10] 1001 	pop	hl
   59CC E5            [11] 1002 	push	hl
   59CD 7E            [ 7] 1003 	ld	a, (hl)
   59CE DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   59D1 DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   59D4 4E            [ 7] 1006 	ld	c, (hl)
   59D5 06 00         [ 7] 1007 	ld	b, #0x00
   59D7 D5            [11] 1008 	push	de
   59D8 F5            [11] 1009 	push	af
   59D9 33            [ 6] 1010 	inc	sp
   59DA FD E5         [15] 1011 	push	iy
   59DC C5            [11] 1012 	push	bc
   59DD CD 42 4C      [17] 1013 	call	_collision_clamp_y_at
   59E0 F1            [10] 1014 	pop	af
   59E1 F1            [10] 1015 	pop	af
   59E2 33            [ 6] 1016 	inc	sp
   59E3 4D            [ 4] 1017 	ld	c, l
   59E4 D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   59E5 DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   59E8 DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   59EB 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   59EC E1            [10] 1024 	pop	hl
   59ED E5            [11] 1025 	push	hl
   59EE 7E            [ 7] 1026 	ld	a, (hl)
   59EF 06 00         [ 7] 1027 	ld	b, #0x00
   59F1 DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   59F4 DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   59F7 6E            [ 7] 1030 	ld	l, (hl)
   59F8 DD 75 F6      [19] 1031 	ld	-10 (ix), l
   59FB DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   59FF D5            [11] 1033 	push	de
   5A00 F5            [11] 1034 	push	af
   5A01 33            [ 6] 1035 	inc	sp
   5A02 C5            [11] 1036 	push	bc
   5A03 DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5A06 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5A09 E5            [11] 1039 	push	hl
   5A0A CD C3 4B      [17] 1040 	call	_collision_is_on_ground_at
   5A0D F1            [10] 1041 	pop	af
   5A0E F1            [10] 1042 	pop	af
   5A0F 33            [ 6] 1043 	inc	sp
   5A10 D1            [10] 1044 	pop	de
   5A11 7D            [ 4] 1045 	ld	a, l
   5A12 B7            [ 4] 1046 	or	a, a
   5A13 28 0E         [12] 1047 	jr	Z,00121$
   5A15 1A            [ 7] 1048 	ld	a, (de)
   5A16 4F            [ 4] 1049 	ld	c, a
   5A17 AF            [ 4] 1050 	xor	a, a
   5A18 91            [ 4] 1051 	sub	a, c
   5A19 E2 1E 5A      [10] 1052 	jp	PO, 00165$
   5A1C EE 80         [ 7] 1053 	xor	a, #0x80
   5A1E                    1054 00165$:
   5A1E F2 23 5A      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5A21 AF            [ 4] 1057 	xor	a, a
   5A22 12            [ 7] 1058 	ld	(de), a
   5A23                    1059 00121$:
   5A23 DD F9         [10] 1060 	ld	sp, ix
   5A25 DD E1         [14] 1061 	pop	ix
   5A27 C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5A28                    1067 _enemyrender::
   5A28 DD E5         [15] 1068 	push	ix
   5A2A DD 21 00 00   [14] 1069 	ld	ix,#0
   5A2E DD 39         [15] 1070 	add	ix,sp
   5A30 F5            [11] 1071 	push	af
   5A31 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5A32 DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5A35 DD B6 04      [19] 1075 	or	a,4 (ix)
   5A38 CA B5 5A      [10] 1076 	jp	Z,00113$
   5A3B DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5A3E DD 46 05      [19] 1078 	ld	b,5 (ix)
   5A41 C5            [11] 1079 	push	bc
   5A42 FD E1         [14] 1080 	pop	iy
   5A44 FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5A47 B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5A48 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5A4A C5            [11] 1086 	push	bc
   5A4B FD E1         [14] 1087 	pop	iy
   5A4D FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5A50 FE 03         [ 7] 1089 	cp	a, #0x03
   5A52 20 0A         [12] 1090 	jr	NZ,00111$
   5A54 DD 36 FE 90   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5A58 DD 36 FF 55   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5A5C 18 23         [12] 1093 	jr	00112$
   5A5E                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5A5E FE 02         [ 7] 1096 	cp	a, #0x02
   5A60 20 0A         [12] 1097 	jr	NZ,00108$
   5A62 DD 36 FE 54   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5A66 DD 36 FF 55   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5A6A 18 15         [12] 1100 	jr	00112$
   5A6C                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5A6C 3D            [ 4] 1103 	dec	a
   5A6D 20 0A         [12] 1104 	jr	NZ,00105$
   5A6F DD 36 FE 0E   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5A73 DD 36 FF 55   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5A77 18 08         [12] 1107 	jr	00112$
   5A79                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5A79 DD 36 FE CE   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5A7D DD 36 FF 54   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5A81                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5A81 69            [ 4] 1114 	ld	l, c
   5A82 60            [ 4] 1115 	ld	h, b
   5A83 23            [ 6] 1116 	inc	hl
   5A84 56            [ 7] 1117 	ld	d, (hl)
   5A85 0A            [ 7] 1118 	ld	a, (bc)
   5A86 C5            [11] 1119 	push	bc
   5A87 5F            [ 4] 1120 	ld	e, a
   5A88 D5            [11] 1121 	push	de
   5A89 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5A8C E5            [11] 1123 	push	hl
   5A8D CD CE 62      [17] 1124 	call	_cpct_getScreenPtr
   5A90 EB            [ 4] 1125 	ex	de,hl
   5A91 C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5A92 C5            [11] 1128 	push	bc
   5A93 FD E1         [14] 1129 	pop	iy
   5A95 FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5A98 DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5A9B 69            [ 4] 1132 	ld	l, c
   5A9C 60            [ 4] 1133 	ld	h, b
   5A9D 01 04 00      [10] 1134 	ld	bc, #0x0004
   5AA0 09            [11] 1135 	add	hl, bc
   5AA1 4E            [ 7] 1136 	ld	c, (hl)
   5AA2 D5            [11] 1137 	push	de
   5AA3 FD E1         [14] 1138 	pop	iy
   5AA5 DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5AA8 DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5AAB DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5AAE C5            [11] 1142 	push	bc
   5AAF FD E5         [15] 1143 	push	iy
   5AB1 D5            [11] 1144 	push	de
   5AB2 CD FF 60      [17] 1145 	call	_cpct_drawSprite
   5AB5                    1146 00113$:
   5AB5 DD F9         [10] 1147 	ld	sp, ix
   5AB7 DD E1         [14] 1148 	pop	ix
   5AB9 C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5ABA                    1154 _enemydamage::
   5ABA DD E5         [15] 1155 	push	ix
   5ABC DD 21 00 00   [14] 1156 	ld	ix,#0
   5AC0 DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5AC2 DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5AC5 DD B6 04      [19] 1160 	or	a,4 (ix)
   5AC8 28 0F         [12] 1161 	jr	Z,00101$
   5ACA DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5ACD DD 46 05      [19] 1163 	ld	b,5 (ix)
   5AD0 21 06 00      [10] 1164 	ld	hl, #0x0006
   5AD3 09            [11] 1165 	add	hl,bc
   5AD4 EB            [ 4] 1166 	ex	de,hl
   5AD5 1A            [ 7] 1167 	ld	a, (de)
   5AD6 B7            [ 4] 1168 	or	a, a
   5AD7 20 04         [12] 1169 	jr	NZ,00102$
   5AD9                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5AD9 2E 00         [ 7] 1172 	ld	l, #0x00
   5ADB 18 1A         [12] 1173 	jr	00106$
   5ADD                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5ADD 21 07 00      [10] 1176 	ld	hl, #0x0007
   5AE0 09            [11] 1177 	add	hl, bc
   5AE1 4E            [ 7] 1178 	ld	c, (hl)
   5AE2 DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5AE5 91            [ 4] 1180 	sub	a, c
   5AE6 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5AE8 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5AEA AF            [ 4] 1185 	xor	a, a
   5AEB 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5AEC 2E 01         [ 7] 1188 	ld	l, #0x01
   5AEE 18 07         [12] 1189 	jr	00106$
   5AF0                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5AF0 79            [ 4] 1192 	ld	a, c
   5AF1 DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5AF4 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5AF5 2E 00         [ 7] 1196 	ld	l, #0x00
   5AF7                    1197 00106$:
   5AF7 DD E1         [14] 1198 	pop	ix
   5AF9 C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
