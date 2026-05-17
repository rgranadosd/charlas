                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module hud
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSprite
                             13 	.globl _hudinit
                             14 	.globl _hudupdate
                             15 	.globl _hudrender
                             16 ;--------------------------------------------------------
                             17 ; special function registers
                             18 ;--------------------------------------------------------
                             19 ;--------------------------------------------------------
                             20 ; ram data
                             21 ;--------------------------------------------------------
                             22 	.area _DATA
   6CBE                      23 _currenthealth:
   6CBE                      24 	.ds 1
   6CBF                      25 _currentscore:
   6CBF                      26 	.ds 2
   6CC1                      27 _currenttime:
   6CC1                      28 	.ds 1
   6CC2                      29 _currentlives:
   6CC2                      30 	.ds 1
   6CC3                      31 _currentweapon:
   6CC3                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
                             37 ;--------------------------------------------------------
                             38 ; absolute external ram data
                             39 ;--------------------------------------------------------
                             40 	.area _DABS (ABS)
                             41 ;--------------------------------------------------------
                             42 ; global & static initialisations
                             43 ;--------------------------------------------------------
                             44 	.area _HOME
                             45 	.area _GSINIT
                             46 	.area _GSFINAL
                             47 	.area _GSINIT
                             48 ;--------------------------------------------------------
                             49 ; Home
                             50 ;--------------------------------------------------------
                             51 	.area _HOME
                             52 	.area _HOME
                             53 ;--------------------------------------------------------
                             54 ; code
                             55 ;--------------------------------------------------------
                             56 	.area _CODE
                             57 ;src/systems/hud.c:80: static const u8* hud_get_number_sprite(u8 digit) {
                             58 ;	---------------------------------
                             59 ; Function hud_get_number_sprite
                             60 ; ---------------------------------
   542D                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:81: switch (digit % 10) {
   542D 3E 0A         [ 7]   63 	ld	a, #0x0a
   542F F5            [11]   64 	push	af
   5430 33            [ 6]   65 	inc	sp
   5431 21 03 00      [10]   66 	ld	hl, #3+0
   5434 39            [11]   67 	add	hl, sp
   5435 7E            [ 7]   68 	ld	a, (hl)
   5436 F5            [11]   69 	push	af
   5437 33            [ 6]   70 	inc	sp
   5438 CD 06 6A      [17]   71 	call	__moduchar
   543B F1            [10]   72 	pop	af
   543C 4D            [ 4]   73 	ld	c, l
   543D 3E 08         [ 7]   74 	ld	a, #0x08
   543F 91            [ 4]   75 	sub	a, c
   5440 38 48         [12]   76 	jr	C,00110$
   5442 06 00         [ 7]   77 	ld	b, #0x00
   5444 21 4B 54      [10]   78 	ld	hl, #00118$
   5447 09            [11]   79 	add	hl, bc
   5448 09            [11]   80 	add	hl, bc
   5449 09            [11]   81 	add	hl, bc
   544A E9            [ 4]   82 	jp	(hl)
   544B                      83 00118$:
   544B C3 66 54      [10]   84 	jp	00101$
   544E C3 6A 54      [10]   85 	jp	00102$
   5451 C3 6E 54      [10]   86 	jp	00103$
   5454 C3 72 54      [10]   87 	jp	00104$
   5457 C3 76 54      [10]   88 	jp	00105$
   545A C3 7A 54      [10]   89 	jp	00106$
   545D C3 7E 54      [10]   90 	jp	00107$
   5460 C3 82 54      [10]   91 	jp	00108$
   5463 C3 86 54      [10]   92 	jp	00109$
                             93 ;src/systems/hud.c:82: case 0: return huddigit_0;
   5466                      94 00101$:
   5466 21 AE 54      [10]   95 	ld	hl, #_huddigit_0
   5469 C9            [10]   96 	ret
                             97 ;src/systems/hud.c:83: case 1: return huddigit_1;
   546A                      98 00102$:
   546A 21 CE 54      [10]   99 	ld	hl, #_huddigit_1
   546D C9            [10]  100 	ret
                            101 ;src/systems/hud.c:84: case 2: return huddigit_2;
   546E                     102 00103$:
   546E 21 EE 54      [10]  103 	ld	hl, #_huddigit_2
   5471 C9            [10]  104 	ret
                            105 ;src/systems/hud.c:85: case 3: return huddigit_3;
   5472                     106 00104$:
   5472 21 0E 55      [10]  107 	ld	hl, #_huddigit_3
   5475 C9            [10]  108 	ret
                            109 ;src/systems/hud.c:86: case 4: return huddigit_4;
   5476                     110 00105$:
   5476 21 2E 55      [10]  111 	ld	hl, #_huddigit_4
   5479 C9            [10]  112 	ret
                            113 ;src/systems/hud.c:87: case 5: return huddigit_5;
   547A                     114 00106$:
   547A 21 4E 55      [10]  115 	ld	hl, #_huddigit_5
   547D C9            [10]  116 	ret
                            117 ;src/systems/hud.c:88: case 6: return huddigit_6;
   547E                     118 00107$:
   547E 21 6E 55      [10]  119 	ld	hl, #_huddigit_6
   5481 C9            [10]  120 	ret
                            121 ;src/systems/hud.c:89: case 7: return huddigit_7;
   5482                     122 00108$:
   5482 21 8E 55      [10]  123 	ld	hl, #_huddigit_7
   5485 C9            [10]  124 	ret
                            125 ;src/systems/hud.c:90: case 8: return huddigit_8;
   5486                     126 00109$:
   5486 21 AE 55      [10]  127 	ld	hl, #_huddigit_8
   5489 C9            [10]  128 	ret
                            129 ;src/systems/hud.c:91: default: return huddigit_9;
   548A                     130 00110$:
   548A 21 CE 55      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:92: }
   548D C9            [10]  133 	ret
   548E                     134 _hudlives:
   548E 30                  135 	.db #0x30	; 48	'0'
   548F 30                  136 	.db #0x30	; 48	'0'
   5490 30                  137 	.db #0x30	; 48	'0'
   5491 30                  138 	.db #0x30	; 48	'0'
   5492 20                  139 	.db #0x20	; 32
   5493 10                  140 	.db #0x10	; 16
   5494 00                  141 	.db #0x00	; 0
   5495 10                  142 	.db #0x10	; 16
   5496 20                  143 	.db #0x20	; 32
   5497 10                  144 	.db #0x10	; 16
   5498 00                  145 	.db #0x00	; 0
   5499 10                  146 	.db #0x10	; 16
   549A 20                  147 	.db #0x20	; 32
   549B 10                  148 	.db #0x10	; 16
   549C 00                  149 	.db #0x00	; 0
   549D 10                  150 	.db #0x10	; 16
   549E 30                  151 	.db #0x30	; 48	'0'
   549F 30                  152 	.db #0x30	; 48	'0'
   54A0 30                  153 	.db #0x30	; 48	'0'
   54A1 30                  154 	.db #0x30	; 48	'0'
   54A2 20                  155 	.db #0x20	; 32
   54A3 10                  156 	.db #0x10	; 16
   54A4 00                  157 	.db #0x00	; 0
   54A5 10                  158 	.db #0x10	; 16
   54A6 20                  159 	.db #0x20	; 32
   54A7 10                  160 	.db #0x10	; 16
   54A8 00                  161 	.db #0x00	; 0
   54A9 10                  162 	.db #0x10	; 16
   54AA 30                  163 	.db #0x30	; 48	'0'
   54AB 30                  164 	.db #0x30	; 48	'0'
   54AC 30                  165 	.db #0x30	; 48	'0'
   54AD 30                  166 	.db #0x30	; 48	'0'
   54AE                     167 _huddigit_0:
   54AE 14                  168 	.db #0x14	; 20
   54AF 3C                  169 	.db #0x3c	; 60
   54B0 3C                  170 	.db #0x3c	; 60
   54B1 28                  171 	.db #0x28	; 40
   54B2 28                  172 	.db #0x28	; 40
   54B3 00                  173 	.db #0x00	; 0
   54B4 00                  174 	.db #0x00	; 0
   54B5 14                  175 	.db #0x14	; 20
   54B6 28                  176 	.db #0x28	; 40
   54B7 00                  177 	.db #0x00	; 0
   54B8 00                  178 	.db #0x00	; 0
   54B9 14                  179 	.db #0x14	; 20
   54BA 00                  180 	.db #0x00	; 0
   54BB 00                  181 	.db #0x00	; 0
   54BC 00                  182 	.db #0x00	; 0
   54BD 00                  183 	.db #0x00	; 0
   54BE 28                  184 	.db #0x28	; 40
   54BF 00                  185 	.db #0x00	; 0
   54C0 00                  186 	.db #0x00	; 0
   54C1 14                  187 	.db #0x14	; 20
   54C2 28                  188 	.db #0x28	; 40
   54C3 00                  189 	.db #0x00	; 0
   54C4 00                  190 	.db #0x00	; 0
   54C5 14                  191 	.db #0x14	; 20
   54C6 28                  192 	.db #0x28	; 40
   54C7 00                  193 	.db #0x00	; 0
   54C8 00                  194 	.db #0x00	; 0
   54C9 14                  195 	.db #0x14	; 20
   54CA 14                  196 	.db #0x14	; 20
   54CB 3C                  197 	.db #0x3c	; 60
   54CC 3C                  198 	.db #0x3c	; 60
   54CD 28                  199 	.db #0x28	; 40
   54CE                     200 _huddigit_1:
   54CE 00                  201 	.db #0x00	; 0
   54CF 00                  202 	.db #0x00	; 0
   54D0 00                  203 	.db #0x00	; 0
   54D1 00                  204 	.db #0x00	; 0
   54D2 00                  205 	.db #0x00	; 0
   54D3 00                  206 	.db #0x00	; 0
   54D4 00                  207 	.db #0x00	; 0
   54D5 14                  208 	.db #0x14	; 20
   54D6 00                  209 	.db #0x00	; 0
   54D7 00                  210 	.db #0x00	; 0
   54D8 00                  211 	.db #0x00	; 0
   54D9 14                  212 	.db #0x14	; 20
   54DA 00                  213 	.db #0x00	; 0
   54DB 00                  214 	.db #0x00	; 0
   54DC 00                  215 	.db #0x00	; 0
   54DD 00                  216 	.db #0x00	; 0
   54DE 00                  217 	.db #0x00	; 0
   54DF 00                  218 	.db #0x00	; 0
   54E0 00                  219 	.db #0x00	; 0
   54E1 14                  220 	.db #0x14	; 20
   54E2 00                  221 	.db #0x00	; 0
   54E3 00                  222 	.db #0x00	; 0
   54E4 00                  223 	.db #0x00	; 0
   54E5 14                  224 	.db #0x14	; 20
   54E6 00                  225 	.db #0x00	; 0
   54E7 00                  226 	.db #0x00	; 0
   54E8 00                  227 	.db #0x00	; 0
   54E9 14                  228 	.db #0x14	; 20
   54EA 00                  229 	.db #0x00	; 0
   54EB 00                  230 	.db #0x00	; 0
   54EC 00                  231 	.db #0x00	; 0
   54ED 00                  232 	.db #0x00	; 0
   54EE                     233 _huddigit_2:
   54EE 14                  234 	.db #0x14	; 20
   54EF 3C                  235 	.db #0x3c	; 60
   54F0 3C                  236 	.db #0x3c	; 60
   54F1 28                  237 	.db #0x28	; 40
   54F2 00                  238 	.db #0x00	; 0
   54F3 00                  239 	.db #0x00	; 0
   54F4 00                  240 	.db #0x00	; 0
   54F5 14                  241 	.db #0x14	; 20
   54F6 00                  242 	.db #0x00	; 0
   54F7 00                  243 	.db #0x00	; 0
   54F8 00                  244 	.db #0x00	; 0
   54F9 14                  245 	.db #0x14	; 20
   54FA 14                  246 	.db #0x14	; 20
   54FB 3C                  247 	.db #0x3c	; 60
   54FC 3C                  248 	.db #0x3c	; 60
   54FD 28                  249 	.db #0x28	; 40
   54FE 28                  250 	.db #0x28	; 40
   54FF 00                  251 	.db #0x00	; 0
   5500 00                  252 	.db #0x00	; 0
   5501 00                  253 	.db #0x00	; 0
   5502 28                  254 	.db #0x28	; 40
   5503 00                  255 	.db #0x00	; 0
   5504 00                  256 	.db #0x00	; 0
   5505 00                  257 	.db #0x00	; 0
   5506 28                  258 	.db #0x28	; 40
   5507 00                  259 	.db #0x00	; 0
   5508 00                  260 	.db #0x00	; 0
   5509 00                  261 	.db #0x00	; 0
   550A 14                  262 	.db #0x14	; 20
   550B 3C                  263 	.db #0x3c	; 60
   550C 3C                  264 	.db #0x3c	; 60
   550D 28                  265 	.db #0x28	; 40
   550E                     266 _huddigit_3:
   550E 14                  267 	.db #0x14	; 20
   550F 3C                  268 	.db #0x3c	; 60
   5510 3C                  269 	.db #0x3c	; 60
   5511 28                  270 	.db #0x28	; 40
   5512 00                  271 	.db #0x00	; 0
   5513 00                  272 	.db #0x00	; 0
   5514 00                  273 	.db #0x00	; 0
   5515 14                  274 	.db #0x14	; 20
   5516 00                  275 	.db #0x00	; 0
   5517 00                  276 	.db #0x00	; 0
   5518 00                  277 	.db #0x00	; 0
   5519 14                  278 	.db #0x14	; 20
   551A 14                  279 	.db #0x14	; 20
   551B 3C                  280 	.db #0x3c	; 60
   551C 3C                  281 	.db #0x3c	; 60
   551D 28                  282 	.db #0x28	; 40
   551E 00                  283 	.db #0x00	; 0
   551F 00                  284 	.db #0x00	; 0
   5520 00                  285 	.db #0x00	; 0
   5521 14                  286 	.db #0x14	; 20
   5522 00                  287 	.db #0x00	; 0
   5523 00                  288 	.db #0x00	; 0
   5524 00                  289 	.db #0x00	; 0
   5525 14                  290 	.db #0x14	; 20
   5526 00                  291 	.db #0x00	; 0
   5527 00                  292 	.db #0x00	; 0
   5528 00                  293 	.db #0x00	; 0
   5529 14                  294 	.db #0x14	; 20
   552A 14                  295 	.db #0x14	; 20
   552B 3C                  296 	.db #0x3c	; 60
   552C 3C                  297 	.db #0x3c	; 60
   552D 28                  298 	.db #0x28	; 40
   552E                     299 _huddigit_4:
   552E 00                  300 	.db #0x00	; 0
   552F 00                  301 	.db #0x00	; 0
   5530 00                  302 	.db #0x00	; 0
   5531 00                  303 	.db #0x00	; 0
   5532 28                  304 	.db #0x28	; 40
   5533 00                  305 	.db #0x00	; 0
   5534 00                  306 	.db #0x00	; 0
   5535 14                  307 	.db #0x14	; 20
   5536 28                  308 	.db #0x28	; 40
   5537 00                  309 	.db #0x00	; 0
   5538 00                  310 	.db #0x00	; 0
   5539 14                  311 	.db #0x14	; 20
   553A 14                  312 	.db #0x14	; 20
   553B 3C                  313 	.db #0x3c	; 60
   553C 3C                  314 	.db #0x3c	; 60
   553D 28                  315 	.db #0x28	; 40
   553E 00                  316 	.db #0x00	; 0
   553F 00                  317 	.db #0x00	; 0
   5540 00                  318 	.db #0x00	; 0
   5541 14                  319 	.db #0x14	; 20
   5542 00                  320 	.db #0x00	; 0
   5543 00                  321 	.db #0x00	; 0
   5544 00                  322 	.db #0x00	; 0
   5545 14                  323 	.db #0x14	; 20
   5546 00                  324 	.db #0x00	; 0
   5547 00                  325 	.db #0x00	; 0
   5548 00                  326 	.db #0x00	; 0
   5549 14                  327 	.db #0x14	; 20
   554A 00                  328 	.db #0x00	; 0
   554B 00                  329 	.db #0x00	; 0
   554C 00                  330 	.db #0x00	; 0
   554D 00                  331 	.db #0x00	; 0
   554E                     332 _huddigit_5:
   554E 14                  333 	.db #0x14	; 20
   554F 3C                  334 	.db #0x3c	; 60
   5550 3C                  335 	.db #0x3c	; 60
   5551 28                  336 	.db #0x28	; 40
   5552 28                  337 	.db #0x28	; 40
   5553 00                  338 	.db #0x00	; 0
   5554 00                  339 	.db #0x00	; 0
   5555 00                  340 	.db #0x00	; 0
   5556 28                  341 	.db #0x28	; 40
   5557 00                  342 	.db #0x00	; 0
   5558 00                  343 	.db #0x00	; 0
   5559 00                  344 	.db #0x00	; 0
   555A 14                  345 	.db #0x14	; 20
   555B 3C                  346 	.db #0x3c	; 60
   555C 3C                  347 	.db #0x3c	; 60
   555D 28                  348 	.db #0x28	; 40
   555E 00                  349 	.db #0x00	; 0
   555F 00                  350 	.db #0x00	; 0
   5560 00                  351 	.db #0x00	; 0
   5561 14                  352 	.db #0x14	; 20
   5562 00                  353 	.db #0x00	; 0
   5563 00                  354 	.db #0x00	; 0
   5564 00                  355 	.db #0x00	; 0
   5565 14                  356 	.db #0x14	; 20
   5566 00                  357 	.db #0x00	; 0
   5567 00                  358 	.db #0x00	; 0
   5568 00                  359 	.db #0x00	; 0
   5569 14                  360 	.db #0x14	; 20
   556A 14                  361 	.db #0x14	; 20
   556B 3C                  362 	.db #0x3c	; 60
   556C 3C                  363 	.db #0x3c	; 60
   556D 28                  364 	.db #0x28	; 40
   556E                     365 _huddigit_6:
   556E 14                  366 	.db #0x14	; 20
   556F 3C                  367 	.db #0x3c	; 60
   5570 3C                  368 	.db #0x3c	; 60
   5571 28                  369 	.db #0x28	; 40
   5572 28                  370 	.db #0x28	; 40
   5573 00                  371 	.db #0x00	; 0
   5574 00                  372 	.db #0x00	; 0
   5575 00                  373 	.db #0x00	; 0
   5576 28                  374 	.db #0x28	; 40
   5577 00                  375 	.db #0x00	; 0
   5578 00                  376 	.db #0x00	; 0
   5579 00                  377 	.db #0x00	; 0
   557A 14                  378 	.db #0x14	; 20
   557B 3C                  379 	.db #0x3c	; 60
   557C 3C                  380 	.db #0x3c	; 60
   557D 28                  381 	.db #0x28	; 40
   557E 28                  382 	.db #0x28	; 40
   557F 00                  383 	.db #0x00	; 0
   5580 00                  384 	.db #0x00	; 0
   5581 14                  385 	.db #0x14	; 20
   5582 28                  386 	.db #0x28	; 40
   5583 00                  387 	.db #0x00	; 0
   5584 00                  388 	.db #0x00	; 0
   5585 14                  389 	.db #0x14	; 20
   5586 28                  390 	.db #0x28	; 40
   5587 00                  391 	.db #0x00	; 0
   5588 00                  392 	.db #0x00	; 0
   5589 14                  393 	.db #0x14	; 20
   558A 14                  394 	.db #0x14	; 20
   558B 3C                  395 	.db #0x3c	; 60
   558C 3C                  396 	.db #0x3c	; 60
   558D 28                  397 	.db #0x28	; 40
   558E                     398 _huddigit_7:
   558E 14                  399 	.db #0x14	; 20
   558F 3C                  400 	.db #0x3c	; 60
   5590 3C                  401 	.db #0x3c	; 60
   5591 28                  402 	.db #0x28	; 40
   5592 00                  403 	.db #0x00	; 0
   5593 00                  404 	.db #0x00	; 0
   5594 00                  405 	.db #0x00	; 0
   5595 14                  406 	.db #0x14	; 20
   5596 00                  407 	.db #0x00	; 0
   5597 00                  408 	.db #0x00	; 0
   5598 00                  409 	.db #0x00	; 0
   5599 14                  410 	.db #0x14	; 20
   559A 00                  411 	.db #0x00	; 0
   559B 00                  412 	.db #0x00	; 0
   559C 00                  413 	.db #0x00	; 0
   559D 00                  414 	.db #0x00	; 0
   559E 00                  415 	.db #0x00	; 0
   559F 00                  416 	.db #0x00	; 0
   55A0 00                  417 	.db #0x00	; 0
   55A1 14                  418 	.db #0x14	; 20
   55A2 00                  419 	.db #0x00	; 0
   55A3 00                  420 	.db #0x00	; 0
   55A4 00                  421 	.db #0x00	; 0
   55A5 14                  422 	.db #0x14	; 20
   55A6 00                  423 	.db #0x00	; 0
   55A7 00                  424 	.db #0x00	; 0
   55A8 00                  425 	.db #0x00	; 0
   55A9 14                  426 	.db #0x14	; 20
   55AA 00                  427 	.db #0x00	; 0
   55AB 00                  428 	.db #0x00	; 0
   55AC 00                  429 	.db #0x00	; 0
   55AD 00                  430 	.db #0x00	; 0
   55AE                     431 _huddigit_8:
   55AE 14                  432 	.db #0x14	; 20
   55AF 3C                  433 	.db #0x3c	; 60
   55B0 3C                  434 	.db #0x3c	; 60
   55B1 28                  435 	.db #0x28	; 40
   55B2 28                  436 	.db #0x28	; 40
   55B3 00                  437 	.db #0x00	; 0
   55B4 00                  438 	.db #0x00	; 0
   55B5 14                  439 	.db #0x14	; 20
   55B6 28                  440 	.db #0x28	; 40
   55B7 00                  441 	.db #0x00	; 0
   55B8 00                  442 	.db #0x00	; 0
   55B9 14                  443 	.db #0x14	; 20
   55BA 14                  444 	.db #0x14	; 20
   55BB 3C                  445 	.db #0x3c	; 60
   55BC 3C                  446 	.db #0x3c	; 60
   55BD 28                  447 	.db #0x28	; 40
   55BE 28                  448 	.db #0x28	; 40
   55BF 00                  449 	.db #0x00	; 0
   55C0 00                  450 	.db #0x00	; 0
   55C1 14                  451 	.db #0x14	; 20
   55C2 28                  452 	.db #0x28	; 40
   55C3 00                  453 	.db #0x00	; 0
   55C4 00                  454 	.db #0x00	; 0
   55C5 14                  455 	.db #0x14	; 20
   55C6 28                  456 	.db #0x28	; 40
   55C7 00                  457 	.db #0x00	; 0
   55C8 00                  458 	.db #0x00	; 0
   55C9 14                  459 	.db #0x14	; 20
   55CA 14                  460 	.db #0x14	; 20
   55CB 3C                  461 	.db #0x3c	; 60
   55CC 3C                  462 	.db #0x3c	; 60
   55CD 28                  463 	.db #0x28	; 40
   55CE                     464 _huddigit_9:
   55CE 14                  465 	.db #0x14	; 20
   55CF 3C                  466 	.db #0x3c	; 60
   55D0 3C                  467 	.db #0x3c	; 60
   55D1 28                  468 	.db #0x28	; 40
   55D2 28                  469 	.db #0x28	; 40
   55D3 00                  470 	.db #0x00	; 0
   55D4 00                  471 	.db #0x00	; 0
   55D5 14                  472 	.db #0x14	; 20
   55D6 28                  473 	.db #0x28	; 40
   55D7 00                  474 	.db #0x00	; 0
   55D8 00                  475 	.db #0x00	; 0
   55D9 14                  476 	.db #0x14	; 20
   55DA 14                  477 	.db #0x14	; 20
   55DB 3C                  478 	.db #0x3c	; 60
   55DC 3C                  479 	.db #0x3c	; 60
   55DD 28                  480 	.db #0x28	; 40
   55DE 00                  481 	.db #0x00	; 0
   55DF 00                  482 	.db #0x00	; 0
   55E0 00                  483 	.db #0x00	; 0
   55E1 14                  484 	.db #0x14	; 20
   55E2 00                  485 	.db #0x00	; 0
   55E3 00                  486 	.db #0x00	; 0
   55E4 00                  487 	.db #0x00	; 0
   55E5 14                  488 	.db #0x14	; 20
   55E6 00                  489 	.db #0x00	; 0
   55E7 00                  490 	.db #0x00	; 0
   55E8 00                  491 	.db #0x00	; 0
   55E9 14                  492 	.db #0x14	; 20
   55EA 14                  493 	.db #0x14	; 20
   55EB 3C                  494 	.db #0x3c	; 60
   55EC 3C                  495 	.db #0x3c	; 60
   55ED 28                  496 	.db #0x28	; 40
                            497 ;src/systems/hud.c:95: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            498 ;	---------------------------------
                            499 ; Function hud_draw_digits
                            500 ; ---------------------------------
   55EE                     501 _hud_draw_digits:
   55EE DD E5         [15]  502 	push	ix
   55F0 DD 21 00 00   [14]  503 	ld	ix,#0
   55F4 DD 39         [15]  504 	add	ix,sp
   55F6 3B            [ 6]  505 	dec	sp
                            506 ;src/systems/hud.c:101: divisor = 1;
   55F7 01 01 00      [10]  507 	ld	bc, #0x0001
                            508 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   55FA 1E 01         [ 7]  509 	ld	e, #0x01
   55FC                     510 00106$:
   55FC 7B            [ 4]  511 	ld	a, e
   55FD DD 96 06      [19]  512 	sub	a, 6 (ix)
   5600 30 0B         [12]  513 	jr	NC,00101$
                            514 ;src/systems/hud.c:103: divisor *= 10;
   5602 69            [ 4]  515 	ld	l, c
   5603 60            [ 4]  516 	ld	h, b
   5604 29            [11]  517 	add	hl, hl
   5605 29            [11]  518 	add	hl, hl
   5606 09            [11]  519 	add	hl, bc
   5607 29            [11]  520 	add	hl, hl
   5608 4D            [ 4]  521 	ld	c, l
   5609 44            [ 4]  522 	ld	b, h
                            523 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   560A 1C            [ 4]  524 	inc	e
   560B 18 EF         [12]  525 	jr	00106$
   560D                     526 00101$:
                            527 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   560D DD 36 FF 00   [19]  528 	ld	-1 (ix), #0x00
   5611                     529 00109$:
   5611 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5614 DD 96 06      [19]  531 	sub	a, 6 (ix)
   5617 30 79         [12]  532 	jr	NC,00111$
                            533 ;src/systems/hud.c:107: digit = (u8)(value / divisor);
   5619 C5            [11]  534 	push	bc
   561A C5            [11]  535 	push	bc
   561B DD 6E 04      [19]  536 	ld	l,4 (ix)
   561E DD 66 05      [19]  537 	ld	h,5 (ix)
   5621 E5            [11]  538 	push	hl
   5622 CD F1 68      [17]  539 	call	__divuint
   5625 F1            [10]  540 	pop	af
   5626 F1            [10]  541 	pop	af
   5627 5D            [ 4]  542 	ld	e, l
   5628 C1            [10]  543 	pop	bc
                            544 ;src/systems/hud.c:108: value = (u16)(value % divisor);
   5629 C5            [11]  545 	push	bc
   562A D5            [11]  546 	push	de
   562B C5            [11]  547 	push	bc
   562C DD 6E 04      [19]  548 	ld	l,4 (ix)
   562F DD 66 05      [19]  549 	ld	h,5 (ix)
   5632 E5            [11]  550 	push	hl
   5633 CD 12 6A      [17]  551 	call	__moduint
   5636 F1            [10]  552 	pop	af
   5637 F1            [10]  553 	pop	af
   5638 D1            [10]  554 	pop	de
   5639 C1            [10]  555 	pop	bc
   563A DD 75 04      [19]  556 	ld	4 (ix), l
   563D DD 74 05      [19]  557 	ld	5 (ix), h
                            558 ;src/systems/hud.c:110: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   5640 DD 7E FF      [19]  559 	ld	a, -1 (ix)
   5643 87            [ 4]  560 	add	a, a
   5644 87            [ 4]  561 	add	a, a
   5645 57            [ 4]  562 	ld	d, a
   5646 DD 7E 07      [19]  563 	ld	a, 7 (ix)
   5649 82            [ 4]  564 	add	a, d
   564A 57            [ 4]  565 	ld	d, a
   564B C5            [11]  566 	push	bc
   564C D5            [11]  567 	push	de
   564D DD 7E 08      [19]  568 	ld	a, 8 (ix)
   5650 F5            [11]  569 	push	af
   5651 33            [ 6]  570 	inc	sp
   5652 D5            [11]  571 	push	de
   5653 33            [ 6]  572 	inc	sp
   5654 21 00 C0      [10]  573 	ld	hl, #0xc000
   5657 E5            [11]  574 	push	hl
   5658 CD A5 6B      [17]  575 	call	_cpct_getScreenPtr
   565B D1            [10]  576 	pop	de
   565C C1            [10]  577 	pop	bc
                            578 ;src/systems/hud.c:111: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   565D E5            [11]  579 	push	hl
   565E C5            [11]  580 	push	bc
   565F 7B            [ 4]  581 	ld	a, e
   5660 F5            [11]  582 	push	af
   5661 33            [ 6]  583 	inc	sp
   5662 CD 2D 54      [17]  584 	call	_hud_get_number_sprite
   5665 33            [ 6]  585 	inc	sp
   5666 EB            [ 4]  586 	ex	de,hl
   5667 C1            [10]  587 	pop	bc
   5668 E1            [10]  588 	pop	hl
   5669 D5            [11]  589 	push	de
   566A FD E1         [14]  590 	pop	iy
   566C C5            [11]  591 	push	bc
   566D 11 04 08      [10]  592 	ld	de, #0x0804
   5670 D5            [11]  593 	push	de
   5671 E5            [11]  594 	push	hl
   5672 FD E5         [15]  595 	push	iy
   5674 CD 61 69      [17]  596 	call	_cpct_drawSprite
   5677 C1            [10]  597 	pop	bc
                            598 ;src/systems/hud.c:113: if (divisor > 1) {
   5678 3E 01         [ 7]  599 	ld	a, #0x01
   567A B9            [ 4]  600 	cp	a, c
   567B 3E 00         [ 7]  601 	ld	a, #0x00
   567D 98            [ 4]  602 	sbc	a, b
   567E 30 0C         [12]  603 	jr	NC,00110$
                            604 ;src/systems/hud.c:114: divisor /= 10;
   5680 21 0A 00      [10]  605 	ld	hl, #0x000a
   5683 E5            [11]  606 	push	hl
   5684 C5            [11]  607 	push	bc
   5685 CD F1 68      [17]  608 	call	__divuint
   5688 F1            [10]  609 	pop	af
   5689 F1            [10]  610 	pop	af
   568A 4D            [ 4]  611 	ld	c, l
   568B 44            [ 4]  612 	ld	b, h
   568C                     613 00110$:
                            614 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   568C DD 34 FF      [23]  615 	inc	-1 (ix)
   568F C3 11 56      [10]  616 	jp	00109$
   5692                     617 00111$:
   5692 33            [ 6]  618 	inc	sp
   5693 DD E1         [14]  619 	pop	ix
   5695 C9            [10]  620 	ret
                            621 ;src/systems/hud.c:119: void hudinit(void) {
                            622 ;	---------------------------------
                            623 ; Function hudinit
                            624 ; ---------------------------------
   5696                     625 _hudinit::
                            626 ;src/systems/hud.c:120: currenthealth = 3;
   5696 21 BE 6C      [10]  627 	ld	hl,#_currenthealth + 0
   5699 36 03         [10]  628 	ld	(hl), #0x03
                            629 ;src/systems/hud.c:121: currentscore  = 0;
   569B 21 00 00      [10]  630 	ld	hl, #0x0000
   569E 22 BF 6C      [16]  631 	ld	(_currentscore), hl
                            632 ;src/systems/hud.c:122: currenttime   = 90;
   56A1 21 C1 6C      [10]  633 	ld	hl,#_currenttime + 0
   56A4 36 5A         [10]  634 	ld	(hl), #0x5a
                            635 ;src/systems/hud.c:123: currentlives  = 3;
   56A6 21 C2 6C      [10]  636 	ld	hl,#_currentlives + 0
   56A9 36 03         [10]  637 	ld	(hl), #0x03
                            638 ;src/systems/hud.c:124: currentweapon = 0;
   56AB 21 C3 6C      [10]  639 	ld	hl,#_currentweapon + 0
   56AE 36 00         [10]  640 	ld	(hl), #0x00
   56B0 C9            [10]  641 	ret
                            642 ;src/systems/hud.c:127: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            643 ;	---------------------------------
                            644 ; Function hudupdate
                            645 ; ---------------------------------
   56B1                     646 _hudupdate::
                            647 ;src/systems/hud.c:128: currenthealth = lives;
   56B1 21 02 00      [10]  648 	ld	hl, #2+0
   56B4 39            [11]  649 	add	hl, sp
   56B5 7E            [ 7]  650 	ld	a, (hl)
   56B6 32 BE 6C      [13]  651 	ld	(#_currenthealth + 0),a
                            652 ;src/systems/hud.c:129: currentscore  = score;
   56B9 21 03 00      [10]  653 	ld	hl, #3+0
   56BC 39            [11]  654 	add	hl, sp
   56BD 7E            [ 7]  655 	ld	a, (hl)
   56BE 32 BF 6C      [13]  656 	ld	(#_currentscore + 0),a
   56C1 21 04 00      [10]  657 	ld	hl, #3+1
   56C4 39            [11]  658 	add	hl, sp
   56C5 7E            [ 7]  659 	ld	a, (hl)
   56C6 32 C0 6C      [13]  660 	ld	(#_currentscore + 1),a
                            661 ;src/systems/hud.c:130: currenttime   = time;
   56C9 21 05 00      [10]  662 	ld	hl, #5+0
   56CC 39            [11]  663 	add	hl, sp
   56CD 7E            [ 7]  664 	ld	a, (hl)
   56CE 32 C1 6C      [13]  665 	ld	(#_currenttime + 0),a
                            666 ;src/systems/hud.c:131: currentlives  = lives;
   56D1 21 02 00      [10]  667 	ld	hl, #2+0
   56D4 39            [11]  668 	add	hl, sp
   56D5 7E            [ 7]  669 	ld	a, (hl)
   56D6 32 C2 6C      [13]  670 	ld	(#_currentlives + 0),a
                            671 ;src/systems/hud.c:132: currentweapon = weapon;
   56D9 21 06 00      [10]  672 	ld	hl, #6+0
   56DC 39            [11]  673 	add	hl, sp
   56DD 7E            [ 7]  674 	ld	a, (hl)
   56DE 32 C3 6C      [13]  675 	ld	(#_currentweapon + 0),a
   56E1 C9            [10]  676 	ret
                            677 ;src/systems/hud.c:135: void hudrender(void) {
                            678 ;	---------------------------------
                            679 ; Function hudrender
                            680 ; ---------------------------------
   56E2                     681 _hudrender::
                            682 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   56E2 0E 00         [ 7]  683 	ld	c, #0x00
   56E4                     684 00103$:
   56E4 21 BE 6C      [10]  685 	ld	hl, #_currenthealth
                            686 ;src/systems/hud.c:142: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   56E7 79            [ 4]  687 	ld	a,c
   56E8 BE            [ 7]  688 	cp	a,(hl)
   56E9 30 24         [12]  689 	jr	NC,00101$
   56EB 07            [ 4]  690 	rlca
   56EC 07            [ 4]  691 	rlca
   56ED 07            [ 4]  692 	rlca
   56EE E6 F8         [ 7]  693 	and	a, #0xf8
   56F0 47            [ 4]  694 	ld	b, a
   56F1 C5            [11]  695 	push	bc
   56F2 3E 02         [ 7]  696 	ld	a, #0x02
   56F4 F5            [11]  697 	push	af
   56F5 33            [ 6]  698 	inc	sp
   56F6 C5            [11]  699 	push	bc
   56F7 33            [ 6]  700 	inc	sp
   56F8 21 00 C0      [10]  701 	ld	hl, #0xc000
   56FB E5            [11]  702 	push	hl
   56FC CD A5 6B      [17]  703 	call	_cpct_getScreenPtr
   56FF 11 04 08      [10]  704 	ld	de, #0x0804
   5702 D5            [11]  705 	push	de
   5703 E5            [11]  706 	push	hl
   5704 21 F8 5C      [10]  707 	ld	hl, #_hudhealthbar_data
   5707 E5            [11]  708 	push	hl
   5708 CD 61 69      [17]  709 	call	_cpct_drawSprite
   570B C1            [10]  710 	pop	bc
                            711 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   570C 0C            [ 4]  712 	inc	c
   570D 18 D5         [12]  713 	jr	00103$
   570F                     714 00101$:
                            715 ;src/systems/hud.c:146: scoretemp = currentscore;
   570F 2A BF 6C      [16]  716 	ld	hl, (_currentscore)
                            717 ;src/systems/hud.c:147: hud_draw_digits(scoretemp, 4, 24, 2);
   5712 01 18 02      [10]  718 	ld	bc, #0x0218
   5715 C5            [11]  719 	push	bc
   5716 3E 04         [ 7]  720 	ld	a, #0x04
   5718 F5            [11]  721 	push	af
   5719 33            [ 6]  722 	inc	sp
   571A E5            [11]  723 	push	hl
   571B CD EE 55      [17]  724 	call	_hud_draw_digits
   571E F1            [10]  725 	pop	af
   571F F1            [10]  726 	pop	af
   5720 33            [ 6]  727 	inc	sp
                            728 ;src/systems/hud.c:149: timetemp = currenttime;
   5721 21 C1 6C      [10]  729 	ld	hl,#_currenttime + 0
   5724 4E            [ 7]  730 	ld	c, (hl)
                            731 ;src/systems/hud.c:150: hud_draw_digits((u16)timetemp, 3, 56, 2);
   5725 06 00         [ 7]  732 	ld	b, #0x00
   5727 21 38 02      [10]  733 	ld	hl, #0x0238
   572A E5            [11]  734 	push	hl
   572B 3E 03         [ 7]  735 	ld	a, #0x03
   572D F5            [11]  736 	push	af
   572E 33            [ 6]  737 	inc	sp
   572F C5            [11]  738 	push	bc
   5730 CD EE 55      [17]  739 	call	_hud_draw_digits
   5733 F1            [10]  740 	pop	af
                            741 ;src/systems/hud.c:152: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   5734 33            [ 6]  742 	inc	sp
   5735 21 02 B4      [10]  743 	ld	hl,#0xb402
   5738 E3            [19]  744 	ex	(sp),hl
   5739 21 00 C0      [10]  745 	ld	hl, #0xc000
   573C E5            [11]  746 	push	hl
   573D CD A5 6B      [17]  747 	call	_cpct_getScreenPtr
                            748 ;src/systems/hud.c:153: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   5740 01 8E 54      [10]  749 	ld	bc, #_hudlives+0
   5743 11 04 08      [10]  750 	ld	de, #0x0804
   5746 D5            [11]  751 	push	de
   5747 E5            [11]  752 	push	hl
   5748 C5            [11]  753 	push	bc
   5749 CD 61 69      [17]  754 	call	_cpct_drawSprite
                            755 ;src/systems/hud.c:155: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   574C 21 0C B4      [10]  756 	ld	hl, #0xb40c
   574F E5            [11]  757 	push	hl
   5750 21 00 C0      [10]  758 	ld	hl, #0xc000
   5753 E5            [11]  759 	push	hl
   5754 CD A5 6B      [17]  760 	call	_cpct_getScreenPtr
                            761 ;src/systems/hud.c:156: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   5757 E5            [11]  762 	push	hl
   5758 3E 0A         [ 7]  763 	ld	a, #0x0a
   575A F5            [11]  764 	push	af
   575B 33            [ 6]  765 	inc	sp
   575C 3A C2 6C      [13]  766 	ld	a, (_currentlives)
   575F F5            [11]  767 	push	af
   5760 33            [ 6]  768 	inc	sp
   5761 CD 06 6A      [17]  769 	call	__moduchar
   5764 F1            [10]  770 	pop	af
   5765 55            [ 4]  771 	ld	d, l
   5766 D5            [11]  772 	push	de
   5767 33            [ 6]  773 	inc	sp
   5768 CD 2D 54      [17]  774 	call	_hud_get_number_sprite
   576B 33            [ 6]  775 	inc	sp
   576C C1            [10]  776 	pop	bc
   576D 11 04 08      [10]  777 	ld	de, #0x0804
   5770 D5            [11]  778 	push	de
   5771 C5            [11]  779 	push	bc
   5772 E5            [11]  780 	push	hl
   5773 CD 61 69      [17]  781 	call	_cpct_drawSprite
                            782 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   5776 21 46 B4      [10]  783 	ld	hl, #0xb446
   5779 E5            [11]  784 	push	hl
   577A 21 00 C0      [10]  785 	ld	hl, #0xc000
   577D E5            [11]  786 	push	hl
   577E CD A5 6B      [17]  787 	call	_cpct_getScreenPtr
                            788 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   5781 E5            [11]  789 	push	hl
   5782 3E 0A         [ 7]  790 	ld	a, #0x0a
   5784 F5            [11]  791 	push	af
   5785 33            [ 6]  792 	inc	sp
   5786 3A C3 6C      [13]  793 	ld	a, (_currentweapon)
   5789 F5            [11]  794 	push	af
   578A 33            [ 6]  795 	inc	sp
   578B CD 06 6A      [17]  796 	call	__moduchar
   578E F1            [10]  797 	pop	af
   578F 55            [ 4]  798 	ld	d, l
   5790 D5            [11]  799 	push	de
   5791 33            [ 6]  800 	inc	sp
   5792 CD 2D 54      [17]  801 	call	_hud_get_number_sprite
   5795 33            [ 6]  802 	inc	sp
   5796 C1            [10]  803 	pop	bc
   5797 11 04 08      [10]  804 	ld	de, #0x0804
   579A D5            [11]  805 	push	de
   579B C5            [11]  806 	push	bc
   579C E5            [11]  807 	push	hl
   579D CD 61 69      [17]  808 	call	_cpct_drawSprite
   57A0 C9            [10]  809 	ret
                            810 	.area _CODE
                            811 	.area _INITIALIZER
                            812 	.area _CABS (ABS)
