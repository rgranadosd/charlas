                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module enemysprites
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _archer_attack_mask
                             12 	.globl _archer_attack_sprite
                             13 	.globl _archer_idle_mask
                             14 	.globl _archer_idle_sprite
                             15 	.globl _zombie_walk_mask
                             16 	.globl _zombie_walk_sprite
                             17 	.globl _zombie_idle_mask
                             18 	.globl _zombie_idle_sprite
                             19 ;--------------------------------------------------------
                             20 ; special function registers
                             21 ;--------------------------------------------------------
                             22 ;--------------------------------------------------------
                             23 ; ram data
                             24 ;--------------------------------------------------------
                             25 	.area _DATA
                             26 ;--------------------------------------------------------
                             27 ; ram data
                             28 ;--------------------------------------------------------
                             29 	.area _INITIALIZED
                             30 ;--------------------------------------------------------
                             31 ; absolute external ram data
                             32 ;--------------------------------------------------------
                             33 	.area _DABS (ABS)
                             34 ;--------------------------------------------------------
                             35 ; global & static initialisations
                             36 ;--------------------------------------------------------
                             37 	.area _HOME
                             38 	.area _GSINIT
                             39 	.area _GSFINAL
                             40 	.area _GSINIT
                             41 ;--------------------------------------------------------
                             42 ; Home
                             43 ;--------------------------------------------------------
                             44 	.area _HOME
                             45 	.area _HOME
                             46 ;--------------------------------------------------------
                             47 ; code
                             48 ;--------------------------------------------------------
                             49 	.area _CODE
                             50 	.area _CODE
   5393                      51 _zombie_idle_sprite:
   5393 00                   52 	.db #0x00	; 0
   5394 00                   53 	.db #0x00	; 0
   5395 00                   54 	.db #0x00	; 0
   5396 00                   55 	.db #0x00	; 0
   5397 00                   56 	.db #0x00	; 0
   5398 00                   57 	.db #0x00	; 0
   5399 00                   58 	.db #0x00	; 0
   539A 00                   59 	.db #0x00	; 0
   539B 0F                   60 	.db #0x0f	; 15
   539C F0                   61 	.db #0xf0	; 240
   539D 00                   62 	.db #0x00	; 0
   539E 00                   63 	.db #0x00	; 0
   539F 00                   64 	.db #0x00	; 0
   53A0 00                   65 	.db #0x00	; 0
   53A1 3F                   66 	.db #0x3f	; 63
   53A2 FC                   67 	.db #0xfc	; 252
   53A3 00                   68 	.db #0x00	; 0
   53A4 00                   69 	.db #0x00	; 0
   53A5 00                   70 	.db #0x00	; 0
   53A6 00                   71 	.db #0x00	; 0
   53A7 3F                   72 	.db #0x3f	; 63
   53A8 FC                   73 	.db #0xfc	; 252
   53A9 00                   74 	.db #0x00	; 0
   53AA 00                   75 	.db #0x00	; 0
   53AB 00                   76 	.db #0x00	; 0
   53AC 00                   77 	.db #0x00	; 0
   53AD 0F                   78 	.db #0x0f	; 15
   53AE F0                   79 	.db #0xf0	; 240
   53AF 00                   80 	.db #0x00	; 0
   53B0 00                   81 	.db #0x00	; 0
   53B1 00                   82 	.db #0x00	; 0
   53B2 00                   83 	.db #0x00	; 0
   53B3 03                   84 	.db #0x03	; 3
   53B4 C0                   85 	.db #0xc0	; 192
   53B5 00                   86 	.db #0x00	; 0
   53B6 00                   87 	.db #0x00	; 0
   53B7 00                   88 	.db #0x00	; 0
   53B8 00                   89 	.db #0x00	; 0
   53B9 03                   90 	.db #0x03	; 3
   53BA C0                   91 	.db #0xc0	; 192
   53BB 00                   92 	.db #0x00	; 0
   53BC 00                   93 	.db #0x00	; 0
   53BD 00                   94 	.db #0x00	; 0
   53BE 00                   95 	.db #0x00	; 0
   53BF 0C                   96 	.db #0x0c	; 12
   53C0 30                   97 	.db #0x30	; 48	'0'
   53C1 00                   98 	.db #0x00	; 0
   53C2 00                   99 	.db #0x00	; 0
   53C3                     100 _zombie_idle_mask:
   53C3 FF                  101 	.db #0xff	; 255
   53C4 FF                  102 	.db #0xff	; 255
   53C5 FF                  103 	.db #0xff	; 255
   53C6 FF                  104 	.db #0xff	; 255
   53C7 FF                  105 	.db #0xff	; 255
   53C8 FF                  106 	.db #0xff	; 255
   53C9 FF                  107 	.db #0xff	; 255
   53CA FF                  108 	.db #0xff	; 255
   53CB F0                  109 	.db #0xf0	; 240
   53CC 0F                  110 	.db #0x0f	; 15
   53CD FF                  111 	.db #0xff	; 255
   53CE FF                  112 	.db #0xff	; 255
   53CF FF                  113 	.db #0xff	; 255
   53D0 FF                  114 	.db #0xff	; 255
   53D1 C0                  115 	.db #0xc0	; 192
   53D2 03                  116 	.db #0x03	; 3
   53D3 FF                  117 	.db #0xff	; 255
   53D4 FF                  118 	.db #0xff	; 255
   53D5 FF                  119 	.db #0xff	; 255
   53D6 FF                  120 	.db #0xff	; 255
   53D7 C0                  121 	.db #0xc0	; 192
   53D8 03                  122 	.db #0x03	; 3
   53D9 FF                  123 	.db #0xff	; 255
   53DA FF                  124 	.db #0xff	; 255
   53DB FF                  125 	.db #0xff	; 255
   53DC FF                  126 	.db #0xff	; 255
   53DD F0                  127 	.db #0xf0	; 240
   53DE 0F                  128 	.db #0x0f	; 15
   53DF FF                  129 	.db #0xff	; 255
   53E0 FF                  130 	.db #0xff	; 255
   53E1 FF                  131 	.db #0xff	; 255
   53E2 FF                  132 	.db #0xff	; 255
   53E3 FC                  133 	.db #0xfc	; 252
   53E4 3F                  134 	.db #0x3f	; 63
   53E5 FF                  135 	.db #0xff	; 255
   53E6 FF                  136 	.db #0xff	; 255
   53E7 FF                  137 	.db #0xff	; 255
   53E8 FF                  138 	.db #0xff	; 255
   53E9 FC                  139 	.db #0xfc	; 252
   53EA 3F                  140 	.db #0x3f	; 63
   53EB FF                  141 	.db #0xff	; 255
   53EC FF                  142 	.db #0xff	; 255
   53ED FF                  143 	.db #0xff	; 255
   53EE FF                  144 	.db #0xff	; 255
   53EF F3                  145 	.db #0xf3	; 243
   53F0 CF                  146 	.db #0xcf	; 207
   53F1 FF                  147 	.db #0xff	; 255
   53F2 FF                  148 	.db #0xff	; 255
   53F3                     149 _zombie_walk_sprite:
   53F3 00                  150 	.db #0x00	; 0
   53F4 00                  151 	.db #0x00	; 0
   53F5 00                  152 	.db #0x00	; 0
   53F6 00                  153 	.db #0x00	; 0
   53F7 00                  154 	.db #0x00	; 0
   53F8 00                  155 	.db #0x00	; 0
   53F9 00                  156 	.db #0x00	; 0
   53FA 00                  157 	.db #0x00	; 0
   53FB 0F                  158 	.db #0x0f	; 15
   53FC F0                  159 	.db #0xf0	; 240
   53FD 00                  160 	.db #0x00	; 0
   53FE 00                  161 	.db #0x00	; 0
   53FF 00                  162 	.db #0x00	; 0
   5400 00                  163 	.db #0x00	; 0
   5401 3F                  164 	.db #0x3f	; 63
   5402 FC                  165 	.db #0xfc	; 252
   5403 00                  166 	.db #0x00	; 0
   5404 00                  167 	.db #0x00	; 0
   5405 00                  168 	.db #0x00	; 0
   5406 00                  169 	.db #0x00	; 0
   5407 3F                  170 	.db #0x3f	; 63
   5408 FC                  171 	.db #0xfc	; 252
   5409 00                  172 	.db #0x00	; 0
   540A 00                  173 	.db #0x00	; 0
   540B 00                  174 	.db #0x00	; 0
   540C 00                  175 	.db #0x00	; 0
   540D 0F                  176 	.db #0x0f	; 15
   540E F0                  177 	.db #0xf0	; 240
   540F 00                  178 	.db #0x00	; 0
   5410 00                  179 	.db #0x00	; 0
   5411 00                  180 	.db #0x00	; 0
   5412 00                  181 	.db #0x00	; 0
   5413 0C                  182 	.db #0x0c	; 12
   5414 30                  183 	.db #0x30	; 48	'0'
   5415 00                  184 	.db #0x00	; 0
   5416 00                  185 	.db #0x00	; 0
   5417 00                  186 	.db #0x00	; 0
   5418 00                  187 	.db #0x00	; 0
   5419 30                  188 	.db #0x30	; 48	'0'
   541A 0C                  189 	.db #0x0c	; 12
   541B 00                  190 	.db #0x00	; 0
   541C 00                  191 	.db #0x00	; 0
   541D 00                  192 	.db #0x00	; 0
   541E 00                  193 	.db #0x00	; 0
   541F 00                  194 	.db #0x00	; 0
   5420 00                  195 	.db #0x00	; 0
   5421 00                  196 	.db #0x00	; 0
   5422 00                  197 	.db #0x00	; 0
   5423                     198 _zombie_walk_mask:
   5423 FF                  199 	.db #0xff	; 255
   5424 FF                  200 	.db #0xff	; 255
   5425 FF                  201 	.db #0xff	; 255
   5426 FF                  202 	.db #0xff	; 255
   5427 FF                  203 	.db #0xff	; 255
   5428 FF                  204 	.db #0xff	; 255
   5429 FF                  205 	.db #0xff	; 255
   542A FF                  206 	.db #0xff	; 255
   542B F0                  207 	.db #0xf0	; 240
   542C 0F                  208 	.db #0x0f	; 15
   542D FF                  209 	.db #0xff	; 255
   542E FF                  210 	.db #0xff	; 255
   542F FF                  211 	.db #0xff	; 255
   5430 FF                  212 	.db #0xff	; 255
   5431 C0                  213 	.db #0xc0	; 192
   5432 03                  214 	.db #0x03	; 3
   5433 FF                  215 	.db #0xff	; 255
   5434 FF                  216 	.db #0xff	; 255
   5435 FF                  217 	.db #0xff	; 255
   5436 FF                  218 	.db #0xff	; 255
   5437 C0                  219 	.db #0xc0	; 192
   5438 03                  220 	.db #0x03	; 3
   5439 FF                  221 	.db #0xff	; 255
   543A FF                  222 	.db #0xff	; 255
   543B FF                  223 	.db #0xff	; 255
   543C FF                  224 	.db #0xff	; 255
   543D F0                  225 	.db #0xf0	; 240
   543E 0F                  226 	.db #0x0f	; 15
   543F FF                  227 	.db #0xff	; 255
   5440 FF                  228 	.db #0xff	; 255
   5441 FF                  229 	.db #0xff	; 255
   5442 FF                  230 	.db #0xff	; 255
   5443 F3                  231 	.db #0xf3	; 243
   5444 CF                  232 	.db #0xcf	; 207
   5445 FF                  233 	.db #0xff	; 255
   5446 FF                  234 	.db #0xff	; 255
   5447 FF                  235 	.db #0xff	; 255
   5448 FF                  236 	.db #0xff	; 255
   5449 CF                  237 	.db #0xcf	; 207
   544A 3F                  238 	.db #0x3f	; 63
   544B FF                  239 	.db #0xff	; 255
   544C FF                  240 	.db #0xff	; 255
   544D FF                  241 	.db #0xff	; 255
   544E FF                  242 	.db #0xff	; 255
   544F FF                  243 	.db #0xff	; 255
   5450 FF                  244 	.db #0xff	; 255
   5451 FF                  245 	.db #0xff	; 255
   5452 FF                  246 	.db #0xff	; 255
   5453                     247 _archer_idle_sprite:
   5453 00                  248 	.db #0x00	; 0
   5454 00                  249 	.db #0x00	; 0
   5455 00                  250 	.db #0x00	; 0
   5456 00                  251 	.db #0x00	; 0
   5457 00                  252 	.db #0x00	; 0
   5458 00                  253 	.db #0x00	; 0
   5459 00                  254 	.db #0x00	; 0
   545A 00                  255 	.db #0x00	; 0
   545B 0F                  256 	.db #0x0f	; 15
   545C F0                  257 	.db #0xf0	; 240
   545D 00                  258 	.db #0x00	; 0
   545E 00                  259 	.db #0x00	; 0
   545F 00                  260 	.db #0x00	; 0
   5460 00                  261 	.db #0x00	; 0
   5461 3F                  262 	.db #0x3f	; 63
   5462 FC                  263 	.db #0xfc	; 252
   5463 00                  264 	.db #0x00	; 0
   5464 00                  265 	.db #0x00	; 0
   5465 00                  266 	.db #0x00	; 0
   5466 00                  267 	.db #0x00	; 0
   5467 3C                  268 	.db #0x3c	; 60
   5468 3C                  269 	.db #0x3c	; 60
   5469 00                  270 	.db #0x00	; 0
   546A 00                  271 	.db #0x00	; 0
   546B 00                  272 	.db #0x00	; 0
   546C 00                  273 	.db #0x00	; 0
   546D 0F                  274 	.db #0x0f	; 15
   546E F0                  275 	.db #0xf0	; 240
   546F 00                  276 	.db #0x00	; 0
   5470 00                  277 	.db #0x00	; 0
   5471 00                  278 	.db #0x00	; 0
   5472 00                  279 	.db #0x00	; 0
   5473 03                  280 	.db #0x03	; 3
   5474 C0                  281 	.db #0xc0	; 192
   5475 00                  282 	.db #0x00	; 0
   5476 00                  283 	.db #0x00	; 0
   5477 00                  284 	.db #0x00	; 0
   5478 00                  285 	.db #0x00	; 0
   5479 03                  286 	.db #0x03	; 3
   547A C0                  287 	.db #0xc0	; 192
   547B 00                  288 	.db #0x00	; 0
   547C 00                  289 	.db #0x00	; 0
   547D 00                  290 	.db #0x00	; 0
   547E 00                  291 	.db #0x00	; 0
   547F 0C                  292 	.db #0x0c	; 12
   5480 30                  293 	.db #0x30	; 48	'0'
   5481 00                  294 	.db #0x00	; 0
   5482 00                  295 	.db #0x00	; 0
   5483                     296 _archer_idle_mask:
   5483 FF                  297 	.db #0xff	; 255
   5484 FF                  298 	.db #0xff	; 255
   5485 FF                  299 	.db #0xff	; 255
   5486 FF                  300 	.db #0xff	; 255
   5487 FF                  301 	.db #0xff	; 255
   5488 FF                  302 	.db #0xff	; 255
   5489 FF                  303 	.db #0xff	; 255
   548A FF                  304 	.db #0xff	; 255
   548B F0                  305 	.db #0xf0	; 240
   548C 0F                  306 	.db #0x0f	; 15
   548D FF                  307 	.db #0xff	; 255
   548E FF                  308 	.db #0xff	; 255
   548F FF                  309 	.db #0xff	; 255
   5490 FF                  310 	.db #0xff	; 255
   5491 C0                  311 	.db #0xc0	; 192
   5492 03                  312 	.db #0x03	; 3
   5493 FF                  313 	.db #0xff	; 255
   5494 FF                  314 	.db #0xff	; 255
   5495 FF                  315 	.db #0xff	; 255
   5496 FF                  316 	.db #0xff	; 255
   5497 C3                  317 	.db #0xc3	; 195
   5498 C3                  318 	.db #0xc3	; 195
   5499 FF                  319 	.db #0xff	; 255
   549A FF                  320 	.db #0xff	; 255
   549B FF                  321 	.db #0xff	; 255
   549C FF                  322 	.db #0xff	; 255
   549D F0                  323 	.db #0xf0	; 240
   549E 0F                  324 	.db #0x0f	; 15
   549F FF                  325 	.db #0xff	; 255
   54A0 FF                  326 	.db #0xff	; 255
   54A1 FF                  327 	.db #0xff	; 255
   54A2 FF                  328 	.db #0xff	; 255
   54A3 FC                  329 	.db #0xfc	; 252
   54A4 3F                  330 	.db #0x3f	; 63
   54A5 FF                  331 	.db #0xff	; 255
   54A6 FF                  332 	.db #0xff	; 255
   54A7 FF                  333 	.db #0xff	; 255
   54A8 FF                  334 	.db #0xff	; 255
   54A9 FC                  335 	.db #0xfc	; 252
   54AA 3F                  336 	.db #0x3f	; 63
   54AB FF                  337 	.db #0xff	; 255
   54AC FF                  338 	.db #0xff	; 255
   54AD FF                  339 	.db #0xff	; 255
   54AE FF                  340 	.db #0xff	; 255
   54AF F3                  341 	.db #0xf3	; 243
   54B0 CF                  342 	.db #0xcf	; 207
   54B1 FF                  343 	.db #0xff	; 255
   54B2 FF                  344 	.db #0xff	; 255
   54B3                     345 _archer_attack_sprite:
   54B3 00                  346 	.db #0x00	; 0
   54B4 00                  347 	.db #0x00	; 0
   54B5 00                  348 	.db #0x00	; 0
   54B6 00                  349 	.db #0x00	; 0
   54B7 00                  350 	.db #0x00	; 0
   54B8 00                  351 	.db #0x00	; 0
   54B9 00                  352 	.db #0x00	; 0
   54BA 00                  353 	.db #0x00	; 0
   54BB 0F                  354 	.db #0x0f	; 15
   54BC F0                  355 	.db #0xf0	; 240
   54BD 00                  356 	.db #0x00	; 0
   54BE 00                  357 	.db #0x00	; 0
   54BF 00                  358 	.db #0x00	; 0
   54C0 00                  359 	.db #0x00	; 0
   54C1 3F                  360 	.db #0x3f	; 63
   54C2 FC                  361 	.db #0xfc	; 252
   54C3 00                  362 	.db #0x00	; 0
   54C4 00                  363 	.db #0x00	; 0
   54C5 00                  364 	.db #0x00	; 0
   54C6 00                  365 	.db #0x00	; 0
   54C7 30                  366 	.db #0x30	; 48	'0'
   54C8 0C                  367 	.db #0x0c	; 12
   54C9 00                  368 	.db #0x00	; 0
   54CA 00                  369 	.db #0x00	; 0
   54CB 00                  370 	.db #0x00	; 0
   54CC 00                  371 	.db #0x00	; 0
   54CD 0F                  372 	.db #0x0f	; 15
   54CE F0                  373 	.db #0xf0	; 240
   54CF 00                  374 	.db #0x00	; 0
   54D0 00                  375 	.db #0x00	; 0
   54D1 00                  376 	.db #0x00	; 0
   54D2 00                  377 	.db #0x00	; 0
   54D3 03                  378 	.db #0x03	; 3
   54D4 C0                  379 	.db #0xc0	; 192
   54D5 00                  380 	.db #0x00	; 0
   54D6 00                  381 	.db #0x00	; 0
   54D7 00                  382 	.db #0x00	; 0
   54D8 00                  383 	.db #0x00	; 0
   54D9 03                  384 	.db #0x03	; 3
   54DA C0                  385 	.db #0xc0	; 192
   54DB 00                  386 	.db #0x00	; 0
   54DC 00                  387 	.db #0x00	; 0
   54DD 00                  388 	.db #0x00	; 0
   54DE 00                  389 	.db #0x00	; 0
   54DF 0C                  390 	.db #0x0c	; 12
   54E0 30                  391 	.db #0x30	; 48	'0'
   54E1 00                  392 	.db #0x00	; 0
   54E2 00                  393 	.db #0x00	; 0
   54E3                     394 _archer_attack_mask:
   54E3 FF                  395 	.db #0xff	; 255
   54E4 FF                  396 	.db #0xff	; 255
   54E5 FF                  397 	.db #0xff	; 255
   54E6 FF                  398 	.db #0xff	; 255
   54E7 FF                  399 	.db #0xff	; 255
   54E8 FF                  400 	.db #0xff	; 255
   54E9 FF                  401 	.db #0xff	; 255
   54EA FF                  402 	.db #0xff	; 255
   54EB F0                  403 	.db #0xf0	; 240
   54EC 0F                  404 	.db #0x0f	; 15
   54ED FF                  405 	.db #0xff	; 255
   54EE FF                  406 	.db #0xff	; 255
   54EF FF                  407 	.db #0xff	; 255
   54F0 FF                  408 	.db #0xff	; 255
   54F1 C0                  409 	.db #0xc0	; 192
   54F2 03                  410 	.db #0x03	; 3
   54F3 FF                  411 	.db #0xff	; 255
   54F4 FF                  412 	.db #0xff	; 255
   54F5 FF                  413 	.db #0xff	; 255
   54F6 FF                  414 	.db #0xff	; 255
   54F7 CF                  415 	.db #0xcf	; 207
   54F8 F3                  416 	.db #0xf3	; 243
   54F9 FF                  417 	.db #0xff	; 255
   54FA FF                  418 	.db #0xff	; 255
   54FB FF                  419 	.db #0xff	; 255
   54FC FF                  420 	.db #0xff	; 255
   54FD F0                  421 	.db #0xf0	; 240
   54FE 0F                  422 	.db #0x0f	; 15
   54FF FF                  423 	.db #0xff	; 255
   5500 FF                  424 	.db #0xff	; 255
   5501 FF                  425 	.db #0xff	; 255
   5502 FF                  426 	.db #0xff	; 255
   5503 FC                  427 	.db #0xfc	; 252
   5504 3F                  428 	.db #0x3f	; 63
   5505 FF                  429 	.db #0xff	; 255
   5506 FF                  430 	.db #0xff	; 255
   5507 FF                  431 	.db #0xff	; 255
   5508 FF                  432 	.db #0xff	; 255
   5509 FC                  433 	.db #0xfc	; 252
   550A 3F                  434 	.db #0x3f	; 63
   550B FF                  435 	.db #0xff	; 255
   550C FF                  436 	.db #0xff	; 255
   550D FF                  437 	.db #0xff	; 255
   550E FF                  438 	.db #0xff	; 255
   550F F3                  439 	.db #0xf3	; 243
   5510 CF                  440 	.db #0xcf	; 207
   5511 FF                  441 	.db #0xff	; 255
   5512 FF                  442 	.db #0xff	; 255
                            443 	.area _INITIALIZER
                            444 	.area _CABS (ABS)
