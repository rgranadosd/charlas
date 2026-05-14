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
   507C                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   507C 21 03 00      [10]   57 	ld	hl, #2+1
   507F 39            [11]   58 	add	hl, sp
   5080 7E            [ 7]   59 	ld	a, (hl)
   5081 2B            [ 6]   60 	dec	hl
   5082 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   5083 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   5084 D1            [10]   65 	pop	de
   5085 C1            [10]   66 	pop	bc
   5086 C5            [11]   67 	push	bc
   5087 D5            [11]   68 	push	de
   5088 AF            [ 4]   69 	xor	a, a
   5089 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   508A 59            [ 4]   72 	ld	e, c
   508B 50            [ 4]   73 	ld	d, b
   508C 13            [ 6]   74 	inc	de
   508D AF            [ 4]   75 	xor	a, a
   508E 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   508F 59            [ 4]   78 	ld	e, c
   5090 50            [ 4]   79 	ld	d, b
   5091 13            [ 6]   80 	inc	de
   5092 13            [ 6]   81 	inc	de
   5093 AF            [ 4]   82 	xor	a, a
   5094 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   5095 59            [ 4]   85 	ld	e, c
   5096 50            [ 4]   86 	ld	d, b
   5097 13            [ 6]   87 	inc	de
   5098 13            [ 6]   88 	inc	de
   5099 13            [ 6]   89 	inc	de
   509A AF            [ 4]   90 	xor	a, a
   509B 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   509C 21 04 00      [10]   93 	ld	hl, #0x0004
   509F 09            [11]   94 	add	hl, bc
   50A0 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   50A2 21 05 00      [10]   97 	ld	hl, #0x0005
   50A5 09            [11]   98 	add	hl, bc
   50A6 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   50A8 21 06 00      [10]  101 	ld	hl, #0x0006
   50AB 09            [11]  102 	add	hl, bc
   50AC 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   50AE 21 07 00      [10]  105 	ld	hl, #0x0007
   50B1 09            [11]  106 	add	hl, bc
   50B2 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   50B4 21 08 00      [10]  109 	ld	hl, #0x0008
   50B7 09            [11]  110 	add	hl, bc
   50B8 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:19: enemy->kind = 0;
   50BA 21 09 00      [10]  113 	ld	hl, #0x0009
   50BD 09            [11]  114 	add	hl, bc
   50BE 36 00         [10]  115 	ld	(hl), #0x00
   50C0 C9            [10]  116 	ret
                            117 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            118 ;	---------------------------------
                            119 ; Function enemyspawn
                            120 ; ---------------------------------
   50C1                     121 _enemyspawn::
   50C1 DD E5         [15]  122 	push	ix
   50C3 DD 21 00 00   [14]  123 	ld	ix,#0
   50C7 DD 39         [15]  124 	add	ix,sp
   50C9 21 F1 FF      [10]  125 	ld	hl, #-15
   50CC 39            [11]  126 	add	hl, sp
   50CD F9            [ 6]  127 	ld	sp, hl
                            128 ;src/entities/enemy.c:23: if (!enemy) {
   50CE DD 7E 05      [19]  129 	ld	a, 5 (ix)
   50D1 DD B6 04      [19]  130 	or	a,4 (ix)
                            131 ;src/entities/enemy.c:24: return;
   50D4 CA 8E 52      [10]  132 	jp	Z,00112$
                            133 ;src/entities/enemy.c:27: enemy->x = x;
   50D7 DD 7E 04      [19]  134 	ld	a, 4 (ix)
   50DA DD 77 F7      [19]  135 	ld	-9 (ix), a
   50DD DD 7E 05      [19]  136 	ld	a, 5 (ix)
   50E0 DD 77 F8      [19]  137 	ld	-8 (ix), a
   50E3 DD 6E F7      [19]  138 	ld	l,-9 (ix)
   50E6 DD 66 F8      [19]  139 	ld	h,-8 (ix)
   50E9 DD 7E 06      [19]  140 	ld	a, 6 (ix)
   50EC 77            [ 7]  141 	ld	(hl), a
                            142 ;src/entities/enemy.c:28: enemy->y = y;
   50ED DD 4E F7      [19]  143 	ld	c,-9 (ix)
   50F0 DD 46 F8      [19]  144 	ld	b,-8 (ix)
   50F3 03            [ 6]  145 	inc	bc
   50F4 DD 7E 07      [19]  146 	ld	a, 7 (ix)
   50F7 02            [ 7]  147 	ld	(bc), a
                            148 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   50F8 DD 7E F7      [19]  149 	ld	a, -9 (ix)
   50FB C6 02         [ 7]  150 	add	a, #0x02
   50FD DD 77 F3      [19]  151 	ld	-13 (ix), a
   5100 DD 7E F8      [19]  152 	ld	a, -8 (ix)
   5103 CE 00         [ 7]  153 	adc	a, #0x00
   5105 DD 77 F4      [19]  154 	ld	-12 (ix), a
   5108 DD 7E 09      [19]  155 	ld	a, 9 (ix)
   510B B7            [ 4]  156 	or	a, a
   510C 28 04         [12]  157 	jr	Z,00114$
   510E 0E 01         [ 7]  158 	ld	c, #0x01
   5110 18 02         [12]  159 	jr	00115$
   5112                     160 00114$:
   5112 0E FF         [ 7]  161 	ld	c, #0xff
   5114                     162 00115$:
   5114 DD 6E F3      [19]  163 	ld	l,-13 (ix)
   5117 DD 66 F4      [19]  164 	ld	h,-12 (ix)
   511A 71            [ 7]  165 	ld	(hl), c
                            166 ;src/entities/enemy.c:30: enemy->vy = 0;
   511B DD 7E F7      [19]  167 	ld	a, -9 (ix)
   511E C6 03         [ 7]  168 	add	a, #0x03
   5120 DD 77 F5      [19]  169 	ld	-11 (ix), a
   5123 DD 7E F8      [19]  170 	ld	a, -8 (ix)
   5126 CE 00         [ 7]  171 	adc	a, #0x00
   5128 DD 77 F6      [19]  172 	ld	-10 (ix), a
   512B DD 6E F5      [19]  173 	ld	l,-11 (ix)
   512E DD 66 F6      [19]  174 	ld	h,-10 (ix)
   5131 36 00         [10]  175 	ld	(hl), #0x00
                            176 ;src/entities/enemy.c:31: enemy->active = 1;
   5133 DD 7E F7      [19]  177 	ld	a, -9 (ix)
   5136 C6 06         [ 7]  178 	add	a, #0x06
   5138 DD 77 FE      [19]  179 	ld	-2 (ix), a
   513B DD 7E F8      [19]  180 	ld	a, -8 (ix)
   513E CE 00         [ 7]  181 	adc	a, #0x00
   5140 DD 77 FF      [19]  182 	ld	-1 (ix), a
   5143 DD 6E FE      [19]  183 	ld	l,-2 (ix)
   5146 DD 66 FF      [19]  184 	ld	h,-1 (ix)
   5149 36 01         [10]  185 	ld	(hl), #0x01
                            186 ;src/entities/enemy.c:32: enemy->kind = kind;
   514B DD 7E F7      [19]  187 	ld	a, -9 (ix)
   514E C6 09         [ 7]  188 	add	a, #0x09
   5150 DD 77 FE      [19]  189 	ld	-2 (ix), a
   5153 DD 7E F8      [19]  190 	ld	a, -8 (ix)
   5156 CE 00         [ 7]  191 	adc	a, #0x00
   5158 DD 77 FF      [19]  192 	ld	-1 (ix), a
   515B DD 6E FE      [19]  193 	ld	l,-2 (ix)
   515E DD 66 FF      [19]  194 	ld	h,-1 (ix)
   5161 DD 7E 08      [19]  195 	ld	a, 8 (ix)
   5164 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/enemy.c:35: enemy->w = 5;
   5165 DD 7E F7      [19]  198 	ld	a, -9 (ix)
   5168 C6 04         [ 7]  199 	add	a, #0x04
   516A DD 77 FE      [19]  200 	ld	-2 (ix), a
   516D DD 7E F8      [19]  201 	ld	a, -8 (ix)
   5170 CE 00         [ 7]  202 	adc	a, #0x00
   5172 DD 77 FF      [19]  203 	ld	-1 (ix), a
                            204 ;src/entities/enemy.c:36: enemy->h = 14;
   5175 DD 7E F7      [19]  205 	ld	a, -9 (ix)
   5178 C6 05         [ 7]  206 	add	a, #0x05
   517A DD 77 FA      [19]  207 	ld	-6 (ix), a
   517D DD 7E F8      [19]  208 	ld	a, -8 (ix)
   5180 CE 00         [ 7]  209 	adc	a, #0x00
   5182 DD 77 FB      [19]  210 	ld	-5 (ix), a
                            211 ;src/entities/enemy.c:37: enemy->health = 2;
   5185 DD 7E F7      [19]  212 	ld	a, -9 (ix)
   5188 C6 07         [ 7]  213 	add	a, #0x07
   518A DD 77 FC      [19]  214 	ld	-4 (ix), a
   518D DD 7E F8      [19]  215 	ld	a, -8 (ix)
   5190 CE 00         [ 7]  216 	adc	a, #0x00
   5192 DD 77 FD      [19]  217 	ld	-3 (ix), a
                            218 ;src/entities/enemy.c:38: enemy->reward = 180;
   5195 DD 7E F7      [19]  219 	ld	a, -9 (ix)
   5198 C6 08         [ 7]  220 	add	a, #0x08
   519A DD 77 F7      [19]  221 	ld	-9 (ix), a
   519D DD 7E F8      [19]  222 	ld	a, -8 (ix)
   51A0 CE 00         [ 7]  223 	adc	a, #0x00
   51A2 DD 77 F8      [19]  224 	ld	-8 (ix), a
                            225 ;src/entities/enemy.c:34: if (kind == 1) {
   51A5 DD 7E 08      [19]  226 	ld	a, 8 (ix)
   51A8 3D            [ 4]  227 	dec	a
   51A9 20 45         [12]  228 	jr	NZ,00110$
                            229 ;src/entities/enemy.c:35: enemy->w = 5;
   51AB DD 6E FE      [19]  230 	ld	l,-2 (ix)
   51AE DD 66 FF      [19]  231 	ld	h,-1 (ix)
   51B1 36 05         [10]  232 	ld	(hl), #0x05
                            233 ;src/entities/enemy.c:36: enemy->h = 14;
   51B3 DD 6E FA      [19]  234 	ld	l,-6 (ix)
   51B6 DD 66 FB      [19]  235 	ld	h,-5 (ix)
   51B9 36 0E         [10]  236 	ld	(hl), #0x0e
                            237 ;src/entities/enemy.c:37: enemy->health = 2;
   51BB DD 6E FC      [19]  238 	ld	l,-4 (ix)
   51BE DD 66 FD      [19]  239 	ld	h,-3 (ix)
   51C1 36 02         [10]  240 	ld	(hl), #0x02
                            241 ;src/entities/enemy.c:38: enemy->reward = 180;
   51C3 DD 6E F7      [19]  242 	ld	l,-9 (ix)
   51C6 DD 66 F8      [19]  243 	ld	h,-8 (ix)
   51C9 36 B4         [10]  244 	ld	(hl), #0xb4
                            245 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   51CB DD 7E F3      [19]  246 	ld	a, -13 (ix)
   51CE DD 77 F1      [19]  247 	ld	-15 (ix), a
   51D1 DD 7E F4      [19]  248 	ld	a, -12 (ix)
   51D4 DD 77 F2      [19]  249 	ld	-14 (ix), a
   51D7 DD 7E 09      [19]  250 	ld	a, 9 (ix)
   51DA B7            [ 4]  251 	or	a, a
   51DB 28 06         [12]  252 	jr	Z,00116$
   51DD DD 36 F9 02   [19]  253 	ld	-7 (ix), #0x02
   51E1 18 04         [12]  254 	jr	00117$
   51E3                     255 00116$:
   51E3 DD 36 F9 FE   [19]  256 	ld	-7 (ix), #0xfe
   51E7                     257 00117$:
   51E7 E1            [10]  258 	pop	hl
   51E8 E5            [11]  259 	push	hl
   51E9 DD 7E F9      [19]  260 	ld	a, -7 (ix)
   51EC 77            [ 7]  261 	ld	(hl), a
   51ED C3 8E 52      [10]  262 	jp	00112$
   51F0                     263 00110$:
                            264 ;src/entities/enemy.c:40: } else if (kind == 2) {
   51F0 DD 7E 08      [19]  265 	ld	a, 8 (ix)
   51F3 D6 02         [ 7]  266 	sub	a, #0x02
   51F5 20 3D         [12]  267 	jr	NZ,00107$
                            268 ;src/entities/enemy.c:41: enemy->w = 6;
   51F7 DD 6E FE      [19]  269 	ld	l,-2 (ix)
   51FA DD 66 FF      [19]  270 	ld	h,-1 (ix)
   51FD 36 06         [10]  271 	ld	(hl), #0x06
                            272 ;src/entities/enemy.c:42: enemy->h = 10;
   51FF DD 6E FA      [19]  273 	ld	l,-6 (ix)
   5202 DD 66 FB      [19]  274 	ld	h,-5 (ix)
   5205 36 0A         [10]  275 	ld	(hl), #0x0a
                            276 ;src/entities/enemy.c:43: enemy->health = 1;
   5207 DD 6E FC      [19]  277 	ld	l,-4 (ix)
   520A DD 66 FD      [19]  278 	ld	h,-3 (ix)
   520D 36 01         [10]  279 	ld	(hl), #0x01
                            280 ;src/entities/enemy.c:44: enemy->reward = 150;
   520F DD 6E F7      [19]  281 	ld	l,-9 (ix)
   5212 DD 66 F8      [19]  282 	ld	h,-8 (ix)
   5215 36 96         [10]  283 	ld	(hl), #0x96
                            284 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5217 DD 4E F5      [19]  285 	ld	c,-11 (ix)
   521A DD 46 F6      [19]  286 	ld	b,-10 (ix)
   521D DD 7E 09      [19]  287 	ld	a, 9 (ix)
   5220 B7            [ 4]  288 	or	a, a
   5221 28 04         [12]  289 	jr	Z,00118$
   5223 3E 01         [ 7]  290 	ld	a, #0x01
   5225 18 02         [12]  291 	jr	00119$
   5227                     292 00118$:
   5227 3E FF         [ 7]  293 	ld	a, #0xff
   5229                     294 00119$:
   5229 02            [ 7]  295 	ld	(bc), a
                            296 ;src/entities/enemy.c:46: enemy->vx = 1;
   522A DD 6E F3      [19]  297 	ld	l,-13 (ix)
   522D DD 66 F4      [19]  298 	ld	h,-12 (ix)
   5230 36 01         [10]  299 	ld	(hl), #0x01
   5232 18 5A         [12]  300 	jr	00112$
   5234                     301 00107$:
                            302 ;src/entities/enemy.c:47: } else if (kind == 3) {
   5234 DD 7E 08      [19]  303 	ld	a, 8 (ix)
   5237 D6 03         [ 7]  304 	sub	a, #0x03
   5239 20 33         [12]  305 	jr	NZ,00104$
                            306 ;src/entities/enemy.c:48: enemy->w = 10;
   523B DD 6E FE      [19]  307 	ld	l,-2 (ix)
   523E DD 66 FF      [19]  308 	ld	h,-1 (ix)
   5241 36 0A         [10]  309 	ld	(hl), #0x0a
                            310 ;src/entities/enemy.c:49: enemy->h = 18;
   5243 DD 6E FA      [19]  311 	ld	l,-6 (ix)
   5246 DD 66 FB      [19]  312 	ld	h,-5 (ix)
   5249 36 12         [10]  313 	ld	(hl), #0x12
                            314 ;src/entities/enemy.c:50: enemy->health = 8;
   524B DD 6E FC      [19]  315 	ld	l,-4 (ix)
   524E DD 66 FD      [19]  316 	ld	h,-3 (ix)
   5251 36 08         [10]  317 	ld	(hl), #0x08
                            318 ;src/entities/enemy.c:51: enemy->reward = 800;
   5253 DD 6E F7      [19]  319 	ld	l,-9 (ix)
   5256 DD 66 F8      [19]  320 	ld	h,-8 (ix)
   5259 36 20         [10]  321 	ld	(hl), #0x20
                            322 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   525B D1            [10]  323 	pop	de
   525C C1            [10]  324 	pop	bc
   525D C5            [11]  325 	push	bc
   525E D5            [11]  326 	push	de
   525F DD 7E 09      [19]  327 	ld	a, 9 (ix)
   5262 B7            [ 4]  328 	or	a, a
   5263 28 04         [12]  329 	jr	Z,00120$
   5265 3E 01         [ 7]  330 	ld	a, #0x01
   5267 18 02         [12]  331 	jr	00121$
   5269                     332 00120$:
   5269 3E FF         [ 7]  333 	ld	a, #0xff
   526B                     334 00121$:
   526B 02            [ 7]  335 	ld	(bc), a
   526C 18 20         [12]  336 	jr	00112$
   526E                     337 00104$:
                            338 ;src/entities/enemy.c:54: enemy->w = 4;
   526E DD 6E FE      [19]  339 	ld	l,-2 (ix)
   5271 DD 66 FF      [19]  340 	ld	h,-1 (ix)
   5274 36 04         [10]  341 	ld	(hl), #0x04
                            342 ;src/entities/enemy.c:55: enemy->h = 16;
   5276 DD 6E FA      [19]  343 	ld	l,-6 (ix)
   5279 DD 66 FB      [19]  344 	ld	h,-5 (ix)
   527C 36 10         [10]  345 	ld	(hl), #0x10
                            346 ;src/entities/enemy.c:56: enemy->health = 1;
   527E DD 6E FC      [19]  347 	ld	l,-4 (ix)
   5281 DD 66 FD      [19]  348 	ld	h,-3 (ix)
   5284 36 01         [10]  349 	ld	(hl), #0x01
                            350 ;src/entities/enemy.c:57: enemy->reward = 100;
   5286 DD 6E F7      [19]  351 	ld	l,-9 (ix)
   5289 DD 66 F8      [19]  352 	ld	h,-8 (ix)
   528C 36 64         [10]  353 	ld	(hl), #0x64
   528E                     354 00112$:
   528E DD F9         [10]  355 	ld	sp, ix
   5290 DD E1         [14]  356 	pop	ix
   5292 C9            [10]  357 	ret
                            358 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            359 ;	---------------------------------
                            360 ; Function enemyupdate
                            361 ; ---------------------------------
   5293                     362 _enemyupdate::
   5293 DD E5         [15]  363 	push	ix
   5295 DD 21 00 00   [14]  364 	ld	ix,#0
   5299 DD 39         [15]  365 	add	ix,sp
   529B 21 F6 FF      [10]  366 	ld	hl, #-10
   529E 39            [11]  367 	add	hl, sp
   529F F9            [ 6]  368 	ld	sp, hl
                            369 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   52A0 DD 7E 05      [19]  370 	ld	a, 5 (ix)
   52A3 DD B6 04      [19]  371 	or	a,4 (ix)
   52A6 CA 85 54      [10]  372 	jp	Z,00121$
   52A9 DD 7E 04      [19]  373 	ld	a, 4 (ix)
   52AC DD 77 F8      [19]  374 	ld	-8 (ix), a
   52AF DD 7E 05      [19]  375 	ld	a, 5 (ix)
   52B2 DD 77 F9      [19]  376 	ld	-7 (ix), a
   52B5 C1            [10]  377 	pop	bc
   52B6 E1            [10]  378 	pop	hl
   52B7 E5            [11]  379 	push	hl
   52B8 C5            [11]  380 	push	bc
   52B9 11 06 00      [10]  381 	ld	de, #0x0006
   52BC 19            [11]  382 	add	hl, de
   52BD 7E            [ 7]  383 	ld	a, (hl)
   52BE B7            [ 4]  384 	or	a, a
                            385 ;src/entities/enemy.c:66: return;
   52BF CA 85 54      [10]  386 	jp	Z,00121$
                            387 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   52C2 C1            [10]  388 	pop	bc
   52C3 E1            [10]  389 	pop	hl
   52C4 E5            [11]  390 	push	hl
   52C5 C5            [11]  391 	push	bc
   52C6 11 09 00      [10]  392 	ld	de, #0x0009
   52C9 19            [11]  393 	add	hl, de
   52CA 7E            [ 7]  394 	ld	a, (hl)
   52CB DD 77 FF      [19]  395 	ld	-1 (ix), a
                            396 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   52CE DD 6E F8      [19]  397 	ld	l,-8 (ix)
   52D1 DD 66 F9      [19]  398 	ld	h,-7 (ix)
   52D4 4E            [ 7]  399 	ld	c, (hl)
   52D5 DD 7E F8      [19]  400 	ld	a, -8 (ix)
   52D8 C6 02         [ 7]  401 	add	a, #0x02
   52DA DD 77 FB      [19]  402 	ld	-5 (ix), a
   52DD DD 7E F9      [19]  403 	ld	a, -7 (ix)
   52E0 CE 00         [ 7]  404 	adc	a, #0x00
   52E2 DD 77 FC      [19]  405 	ld	-4 (ix), a
                            406 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   52E5 DD 7E F8      [19]  407 	ld	a, -8 (ix)
   52E8 C6 01         [ 7]  408 	add	a, #0x01
   52EA DD 77 FD      [19]  409 	ld	-3 (ix), a
   52ED DD 7E F9      [19]  410 	ld	a, -7 (ix)
   52F0 CE 00         [ 7]  411 	adc	a, #0x00
   52F2 DD 77 FE      [19]  412 	ld	-2 (ix), a
   52F5 DD 5E F8      [19]  413 	ld	e,-8 (ix)
   52F8 DD 56 F9      [19]  414 	ld	d,-7 (ix)
   52FB 13            [ 6]  415 	inc	de
   52FC 13            [ 6]  416 	inc	de
   52FD 13            [ 6]  417 	inc	de
                            418 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   52FE 06 00         [ 7]  419 	ld	b, #0x00
   5300 DD 6E FB      [19]  420 	ld	l,-5 (ix)
   5303 DD 66 FC      [19]  421 	ld	h,-4 (ix)
   5306 7E            [ 7]  422 	ld	a, (hl)
   5307 DD 77 FA      [19]  423 	ld	-6 (ix), a
   530A 6F            [ 4]  424 	ld	l, a
   530B DD 7E FA      [19]  425 	ld	a, -6 (ix)
   530E 17            [ 4]  426 	rla
   530F 9F            [ 4]  427 	sbc	a, a
   5310 67            [ 4]  428 	ld	h, a
   5311 09            [11]  429 	add	hl,bc
   5312 4D            [ 4]  430 	ld	c, l
   5313 44            [ 4]  431 	ld	b, h
                            432 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   5314 DD 7E FF      [19]  433 	ld	a, -1 (ix)
   5317 D6 02         [ 7]  434 	sub	a, #0x02
   5319 C2 C2 53      [10]  435 	jp	NZ,00111$
                            436 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            437 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   531C DD 6E FD      [19]  438 	ld	l,-3 (ix)
   531F DD 66 FE      [19]  439 	ld	h,-2 (ix)
   5322 6E            [ 7]  440 	ld	l, (hl)
   5323 DD 75 F6      [19]  441 	ld	-10 (ix), l
   5326 DD 36 F7 00   [19]  442 	ld	-9 (ix), #0x00
   532A 1A            [ 7]  443 	ld	a, (de)
   532B 6F            [ 4]  444 	ld	l, a
   532C 17            [ 4]  445 	rla
   532D 9F            [ 4]  446 	sbc	a, a
   532E 67            [ 4]  447 	ld	h, a
   532F DD 7E F6      [19]  448 	ld	a, -10 (ix)
   5332 85            [ 4]  449 	add	a, l
   5333 DD 77 F6      [19]  450 	ld	-10 (ix), a
   5336 DD 7E F7      [19]  451 	ld	a, -9 (ix)
   5339 8C            [ 4]  452 	adc	a, h
   533A DD 77 F7      [19]  453 	ld	-9 (ix), a
                            454 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   533D 79            [ 4]  455 	ld	a, c
   533E D6 08         [ 7]  456 	sub	a, #0x08
   5340 78            [ 4]  457 	ld	a, b
   5341 17            [ 4]  458 	rla
   5342 3F            [ 4]  459 	ccf
   5343 1F            [ 4]  460 	rra
   5344 DE 80         [ 7]  461 	sbc	a, #0x80
   5346 38 0E         [12]  462 	jr	C,00104$
   5348 3E 48         [ 7]  463 	ld	a, #0x48
   534A B9            [ 4]  464 	cp	a, c
   534B 3E 00         [ 7]  465 	ld	a, #0x00
   534D 98            [ 4]  466 	sbc	a, b
   534E E2 53 53      [10]  467 	jp	PO, 00161$
   5351 EE 80         [ 7]  468 	xor	a, #0x80
   5353                     469 00161$:
   5353 F2 71 53      [10]  470 	jp	P, 00105$
   5356                     471 00104$:
                            472 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   5356 AF            [ 4]  473 	xor	a, a
   5357 DD 96 FA      [19]  474 	sub	a, -6 (ix)
   535A 4F            [ 4]  475 	ld	c, a
   535B DD 6E FB      [19]  476 	ld	l,-5 (ix)
   535E DD 66 FC      [19]  477 	ld	h,-4 (ix)
   5361 71            [ 7]  478 	ld	(hl), c
                            479 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   5362 DD 6E F8      [19]  480 	ld	l,-8 (ix)
   5365 DD 66 F9      [19]  481 	ld	h,-7 (ix)
   5368 6E            [ 7]  482 	ld	l, (hl)
   5369 26 00         [ 7]  483 	ld	h, #0x00
   536B 79            [ 4]  484 	ld	a, c
   536C 17            [ 4]  485 	rla
   536D 9F            [ 4]  486 	sbc	a, a
   536E 47            [ 4]  487 	ld	b, a
   536F 09            [11]  488 	add	hl,bc
   5370 4D            [ 4]  489 	ld	c, l
   5371                     490 00105$:
                            491 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   5371 DD 7E F6      [19]  492 	ld	a, -10 (ix)
   5374 D6 38         [ 7]  493 	sub	a, #0x38
   5376 DD 7E F7      [19]  494 	ld	a, -9 (ix)
   5379 17            [ 4]  495 	rla
   537A 3F            [ 4]  496 	ccf
   537B 1F            [ 4]  497 	rra
   537C DE 80         [ 7]  498 	sbc	a, #0x80
   537E 38 12         [12]  499 	jr	C,00107$
   5380 3E 78         [ 7]  500 	ld	a, #0x78
   5382 DD BE F6      [19]  501 	cp	a, -10 (ix)
   5385 3E 00         [ 7]  502 	ld	a, #0x00
   5387 DD 9E F7      [19]  503 	sbc	a, -9 (ix)
   538A E2 8F 53      [10]  504 	jp	PO, 00162$
   538D EE 80         [ 7]  505 	xor	a, #0x80
   538F                     506 00162$:
   538F F2 AE 53      [10]  507 	jp	P, 00108$
   5392                     508 00107$:
                            509 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   5392 1A            [ 7]  510 	ld	a, (de)
   5393 6F            [ 4]  511 	ld	l, a
   5394 AF            [ 4]  512 	xor	a, a
   5395 95            [ 4]  513 	sub	a, l
   5396 DD 77 FA      [19]  514 	ld	-6 (ix), a
   5399 12            [ 7]  515 	ld	(de),a
                            516 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   539A DD 6E FD      [19]  517 	ld	l,-3 (ix)
   539D DD 66 FE      [19]  518 	ld	h,-2 (ix)
   53A0 5E            [ 7]  519 	ld	e, (hl)
   53A1 16 00         [ 7]  520 	ld	d, #0x00
   53A3 DD 6E FA      [19]  521 	ld	l, -6 (ix)
   53A6 DD 7E FA      [19]  522 	ld	a, -6 (ix)
   53A9 17            [ 4]  523 	rla
   53AA 9F            [ 4]  524 	sbc	a, a
   53AB 67            [ 4]  525 	ld	h, a
   53AC 19            [11]  526 	add	hl,de
   53AD E3            [19]  527 	ex	(sp), hl
   53AE                     528 00108$:
                            529 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   53AE DD 6E F8      [19]  530 	ld	l,-8 (ix)
   53B1 DD 66 F9      [19]  531 	ld	h,-7 (ix)
   53B4 71            [ 7]  532 	ld	(hl), c
                            533 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   53B5 DD 4E F6      [19]  534 	ld	c, -10 (ix)
   53B8 DD 6E FD      [19]  535 	ld	l,-3 (ix)
   53BB DD 66 FE      [19]  536 	ld	h,-2 (ix)
   53BE 71            [ 7]  537 	ld	(hl), c
                            538 ;src/entities/enemy.c:84: return;
   53BF C3 85 54      [10]  539 	jp	00121$
   53C2                     540 00111$:
                            541 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            542 ;src/entities/enemy.c:88: if (nextx < 2) {
   53C2 79            [ 4]  543 	ld	a, c
   53C3 D6 02         [ 7]  544 	sub	a, #0x02
   53C5 78            [ 4]  545 	ld	a, b
   53C6 17            [ 4]  546 	rla
   53C7 3F            [ 4]  547 	ccf
   53C8 1F            [ 4]  548 	rra
   53C9 DE 80         [ 7]  549 	sbc	a, #0x80
   53CB 30 0B         [12]  550 	jr	NC,00113$
                            551 ;src/entities/enemy.c:89: nextx = 2;
   53CD 01 02 00      [10]  552 	ld	bc, #0x0002
                            553 ;src/entities/enemy.c:90: enemy->vx = 1;
   53D0 DD 6E FB      [19]  554 	ld	l,-5 (ix)
   53D3 DD 66 FC      [19]  555 	ld	h,-4 (ix)
   53D6 36 01         [10]  556 	ld	(hl), #0x01
   53D8                     557 00113$:
                            558 ;src/entities/enemy.c:92: if (nextx > 74) {
   53D8 3E 4A         [ 7]  559 	ld	a, #0x4a
   53DA B9            [ 4]  560 	cp	a, c
   53DB 3E 00         [ 7]  561 	ld	a, #0x00
   53DD 98            [ 4]  562 	sbc	a, b
   53DE E2 E3 53      [10]  563 	jp	PO, 00163$
   53E1 EE 80         [ 7]  564 	xor	a, #0x80
   53E3                     565 00163$:
   53E3 F2 F1 53      [10]  566 	jp	P, 00115$
                            567 ;src/entities/enemy.c:93: nextx = 74;
   53E6 01 4A 00      [10]  568 	ld	bc, #0x004a
                            569 ;src/entities/enemy.c:94: enemy->vx = -1;
   53E9 DD 6E FB      [19]  570 	ld	l,-5 (ix)
   53EC DD 66 FC      [19]  571 	ld	h,-4 (ix)
   53EF 36 FF         [10]  572 	ld	(hl), #0xff
   53F1                     573 00115$:
                            574 ;src/entities/enemy.c:96: enemy->x = (u8)nextx;
   53F1 DD 6E F8      [19]  575 	ld	l,-8 (ix)
   53F4 DD 66 F9      [19]  576 	ld	h,-7 (ix)
   53F7 71            [ 7]  577 	ld	(hl), c
                            578 ;src/entities/enemy.c:98: enemy->vy = (i8)(enemy->vy + 1);
   53F8 1A            [ 7]  579 	ld	a, (de)
   53F9 4F            [ 4]  580 	ld	c, a
   53FA 0C            [ 4]  581 	inc	c
   53FB 79            [ 4]  582 	ld	a, c
   53FC 12            [ 7]  583 	ld	(de), a
                            584 ;src/entities/enemy.c:99: if (enemy->vy > 3) enemy->vy = 3;
   53FD 3E 03         [ 7]  585 	ld	a, #0x03
   53FF 91            [ 4]  586 	sub	a, c
   5400 E2 05 54      [10]  587 	jp	PO, 00164$
   5403 EE 80         [ 7]  588 	xor	a, #0x80
   5405                     589 00164$:
   5405 F2 0B 54      [10]  590 	jp	P, 00117$
   5408 3E 03         [ 7]  591 	ld	a, #0x03
   540A 12            [ 7]  592 	ld	(de), a
   540B                     593 00117$:
                            594 ;src/entities/enemy.c:100: nexty = (i16)enemy->y + (i16)enemy->vy;
   540B DD 6E FD      [19]  595 	ld	l,-3 (ix)
   540E DD 66 FE      [19]  596 	ld	h,-2 (ix)
   5411 4E            [ 7]  597 	ld	c, (hl)
   5412 06 00         [ 7]  598 	ld	b, #0x00
   5414 1A            [ 7]  599 	ld	a, (de)
   5415 6F            [ 4]  600 	ld	l, a
   5416 17            [ 4]  601 	rla
   5417 9F            [ 4]  602 	sbc	a, a
   5418 67            [ 4]  603 	ld	h, a
   5419 09            [11]  604 	add	hl, bc
   541A E5            [11]  605 	push	hl
   541B FD E1         [14]  606 	pop	iy
                            607 ;src/entities/enemy.c:101: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   541D DD 7E F8      [19]  608 	ld	a, -8 (ix)
   5420 C6 05         [ 7]  609 	add	a, #0x05
   5422 DD 77 F6      [19]  610 	ld	-10 (ix), a
   5425 DD 7E F9      [19]  611 	ld	a, -7 (ix)
   5428 CE 00         [ 7]  612 	adc	a, #0x00
   542A DD 77 F7      [19]  613 	ld	-9 (ix), a
   542D E1            [10]  614 	pop	hl
   542E E5            [11]  615 	push	hl
   542F 7E            [ 7]  616 	ld	a, (hl)
   5430 DD 6E F8      [19]  617 	ld	l,-8 (ix)
   5433 DD 66 F9      [19]  618 	ld	h,-7 (ix)
   5436 4E            [ 7]  619 	ld	c, (hl)
   5437 06 00         [ 7]  620 	ld	b, #0x00
   5439 D5            [11]  621 	push	de
   543A F5            [11]  622 	push	af
   543B 33            [ 6]  623 	inc	sp
   543C FD E5         [15]  624 	push	iy
   543E C5            [11]  625 	push	bc
   543F CD E3 4A      [17]  626 	call	_collision_clamp_y_at
   5442 F1            [10]  627 	pop	af
   5443 F1            [10]  628 	pop	af
   5444 33            [ 6]  629 	inc	sp
   5445 4D            [ 4]  630 	ld	c, l
   5446 D1            [10]  631 	pop	de
                            632 ;src/entities/enemy.c:102: enemy->y = (u8)nexty;
   5447 DD 6E FD      [19]  633 	ld	l,-3 (ix)
   544A DD 66 FE      [19]  634 	ld	h,-2 (ix)
   544D 71            [ 7]  635 	ld	(hl), c
                            636 ;src/entities/enemy.c:103: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   544E E1            [10]  637 	pop	hl
   544F E5            [11]  638 	push	hl
   5450 7E            [ 7]  639 	ld	a, (hl)
   5451 06 00         [ 7]  640 	ld	b, #0x00
   5453 DD 6E F8      [19]  641 	ld	l,-8 (ix)
   5456 DD 66 F9      [19]  642 	ld	h,-7 (ix)
   5459 6E            [ 7]  643 	ld	l, (hl)
   545A DD 75 F6      [19]  644 	ld	-10 (ix), l
   545D DD 36 F7 00   [19]  645 	ld	-9 (ix), #0x00
   5461 D5            [11]  646 	push	de
   5462 F5            [11]  647 	push	af
   5463 33            [ 6]  648 	inc	sp
   5464 C5            [11]  649 	push	bc
   5465 DD 6E F6      [19]  650 	ld	l,-10 (ix)
   5468 DD 66 F7      [19]  651 	ld	h,-9 (ix)
   546B E5            [11]  652 	push	hl
   546C CD 64 4A      [17]  653 	call	_collision_is_on_ground_at
   546F F1            [10]  654 	pop	af
   5470 F1            [10]  655 	pop	af
   5471 33            [ 6]  656 	inc	sp
   5472 D1            [10]  657 	pop	de
   5473 7D            [ 4]  658 	ld	a, l
   5474 B7            [ 4]  659 	or	a, a
   5475 28 0E         [12]  660 	jr	Z,00121$
   5477 1A            [ 7]  661 	ld	a, (de)
   5478 4F            [ 4]  662 	ld	c, a
   5479 AF            [ 4]  663 	xor	a, a
   547A 91            [ 4]  664 	sub	a, c
   547B E2 80 54      [10]  665 	jp	PO, 00165$
   547E EE 80         [ 7]  666 	xor	a, #0x80
   5480                     667 00165$:
   5480 F2 85 54      [10]  668 	jp	P, 00121$
                            669 ;src/entities/enemy.c:104: enemy->vy = 0;
   5483 AF            [ 4]  670 	xor	a, a
   5484 12            [ 7]  671 	ld	(de), a
   5485                     672 00121$:
   5485 DD F9         [10]  673 	ld	sp, ix
   5487 DD E1         [14]  674 	pop	ix
   5489 C9            [10]  675 	ret
                            676 ;src/entities/enemy.c:108: void enemyrender(const Enemy* enemy) {
                            677 ;	---------------------------------
                            678 ; Function enemyrender
                            679 ; ---------------------------------
   548A                     680 _enemyrender::
   548A DD E5         [15]  681 	push	ix
   548C DD 21 00 00   [14]  682 	ld	ix,#0
   5490 DD 39         [15]  683 	add	ix,sp
   5492 3B            [ 6]  684 	dec	sp
                            685 ;src/entities/enemy.c:112: if (!enemy || !enemy->active) {
   5493 DD 7E 05      [19]  686 	ld	a, 5 (ix)
   5496 DD B6 04      [19]  687 	or	a,4 (ix)
   5499 28 65         [12]  688 	jr	Z,00113$
   549B DD 4E 04      [19]  689 	ld	c,4 (ix)
   549E DD 46 05      [19]  690 	ld	b,5 (ix)
   54A1 C5            [11]  691 	push	bc
   54A2 FD E1         [14]  692 	pop	iy
   54A4 FD 7E 06      [19]  693 	ld	a, 6 (iy)
   54A7 B7            [ 4]  694 	or	a, a
                            695 ;src/entities/enemy.c:113: return;
   54A8 28 56         [12]  696 	jr	Z,00113$
                            697 ;src/entities/enemy.c:116: if (enemy->kind == 3) colour = 0x4C;
   54AA C5            [11]  698 	push	bc
   54AB FD E1         [14]  699 	pop	iy
   54AD FD 7E 09      [19]  700 	ld	a, 9 (iy)
   54B0 FE 03         [ 7]  701 	cp	a, #0x03
   54B2 20 04         [12]  702 	jr	NZ,00111$
   54B4 1E 4C         [ 7]  703 	ld	e, #0x4c
   54B6 18 11         [12]  704 	jr	00112$
   54B8                     705 00111$:
                            706 ;src/entities/enemy.c:117: else if (enemy->kind == 2) colour = 0x5A;
   54B8 FE 02         [ 7]  707 	cp	a, #0x02
   54BA 20 04         [12]  708 	jr	NZ,00108$
   54BC 1E 5A         [ 7]  709 	ld	e, #0x5a
   54BE 18 09         [12]  710 	jr	00112$
   54C0                     711 00108$:
                            712 ;src/entities/enemy.c:118: else if (enemy->kind == 1) colour = 0x4E;
   54C0 3D            [ 4]  713 	dec	a
   54C1 20 04         [12]  714 	jr	NZ,00105$
   54C3 1E 4E         [ 7]  715 	ld	e, #0x4e
   54C5 18 02         [12]  716 	jr	00112$
   54C7                     717 00105$:
                            718 ;src/entities/enemy.c:119: else colour = 0x5C;
   54C7 1E 5C         [ 7]  719 	ld	e, #0x5c
   54C9                     720 00112$:
                            721 ;src/entities/enemy.c:121: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   54C9 69            [ 4]  722 	ld	l, c
   54CA 60            [ 4]  723 	ld	h, b
   54CB 23            [ 6]  724 	inc	hl
   54CC 56            [ 7]  725 	ld	d, (hl)
   54CD 0A            [ 7]  726 	ld	a, (bc)
   54CE C5            [11]  727 	push	bc
   54CF D5            [11]  728 	push	de
   54D0 5F            [ 4]  729 	ld	e, a
   54D1 D5            [11]  730 	push	de
   54D2 21 00 C0      [10]  731 	ld	hl, #0xc000
   54D5 E5            [11]  732 	push	hl
   54D6 CD 74 5D      [17]  733 	call	_cpct_getScreenPtr
   54D9 D1            [10]  734 	pop	de
   54DA C1            [10]  735 	pop	bc
   54DB E5            [11]  736 	push	hl
   54DC FD E1         [14]  737 	pop	iy
                            738 ;src/entities/enemy.c:122: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   54DE 69            [ 4]  739 	ld	l, c
   54DF 60            [ 4]  740 	ld	h, b
   54E0 23            [ 6]  741 	inc	hl
   54E1 23            [ 6]  742 	inc	hl
   54E2 23            [ 6]  743 	inc	hl
   54E3 23            [ 6]  744 	inc	hl
   54E4 23            [ 6]  745 	inc	hl
   54E5 7E            [ 7]  746 	ld	a, (hl)
   54E6 DD 77 FF      [19]  747 	ld	-1 (ix), a
   54E9 69            [ 4]  748 	ld	l, c
   54EA 60            [ 4]  749 	ld	h, b
   54EB 01 04 00      [10]  750 	ld	bc, #0x0004
   54EE 09            [11]  751 	add	hl, bc
   54EF 56            [ 7]  752 	ld	d, (hl)
   54F0 FD E5         [15]  753 	push	iy
   54F2 C1            [10]  754 	pop	bc
   54F3 DD 7E FF      [19]  755 	ld	a, -1 (ix)
   54F6 F5            [11]  756 	push	af
   54F7 33            [ 6]  757 	inc	sp
   54F8 D5            [11]  758 	push	de
   54F9 C5            [11]  759 	push	bc
   54FA CD BB 5C      [17]  760 	call	_cpct_drawSolidBox
   54FD F1            [10]  761 	pop	af
   54FE F1            [10]  762 	pop	af
   54FF 33            [ 6]  763 	inc	sp
   5500                     764 00113$:
   5500 33            [ 6]  765 	inc	sp
   5501 DD E1         [14]  766 	pop	ix
   5503 C9            [10]  767 	ret
                            768 ;src/entities/enemy.c:125: u8 enemydamage(Enemy* enemy, u8 damage) {
                            769 ;	---------------------------------
                            770 ; Function enemydamage
                            771 ; ---------------------------------
   5504                     772 _enemydamage::
   5504 DD E5         [15]  773 	push	ix
   5506 DD 21 00 00   [14]  774 	ld	ix,#0
   550A DD 39         [15]  775 	add	ix,sp
                            776 ;src/entities/enemy.c:126: if (!enemy || !enemy->active) {
   550C DD 7E 05      [19]  777 	ld	a, 5 (ix)
   550F DD B6 04      [19]  778 	or	a,4 (ix)
   5512 28 0F         [12]  779 	jr	Z,00101$
   5514 DD 4E 04      [19]  780 	ld	c,4 (ix)
   5517 DD 46 05      [19]  781 	ld	b,5 (ix)
   551A 21 06 00      [10]  782 	ld	hl, #0x0006
   551D 09            [11]  783 	add	hl,bc
   551E EB            [ 4]  784 	ex	de,hl
   551F 1A            [ 7]  785 	ld	a, (de)
   5520 B7            [ 4]  786 	or	a, a
   5521 20 04         [12]  787 	jr	NZ,00102$
   5523                     788 00101$:
                            789 ;src/entities/enemy.c:127: return 0;
   5523 2E 00         [ 7]  790 	ld	l, #0x00
   5525 18 1A         [12]  791 	jr	00106$
   5527                     792 00102$:
                            793 ;src/entities/enemy.c:130: if (damage >= enemy->health) {
   5527 21 07 00      [10]  794 	ld	hl, #0x0007
   552A 09            [11]  795 	add	hl, bc
   552B 4E            [ 7]  796 	ld	c, (hl)
   552C DD 7E 06      [19]  797 	ld	a, 6 (ix)
   552F 91            [ 4]  798 	sub	a, c
   5530 38 08         [12]  799 	jr	C,00105$
                            800 ;src/entities/enemy.c:131: enemy->health = 0;
   5532 36 00         [10]  801 	ld	(hl), #0x00
                            802 ;src/entities/enemy.c:132: enemy->active = 0;
   5534 AF            [ 4]  803 	xor	a, a
   5535 12            [ 7]  804 	ld	(de), a
                            805 ;src/entities/enemy.c:133: return 1;
   5536 2E 01         [ 7]  806 	ld	l, #0x01
   5538 18 07         [12]  807 	jr	00106$
   553A                     808 00105$:
                            809 ;src/entities/enemy.c:136: enemy->health = (u8)(enemy->health - damage);
   553A 79            [ 4]  810 	ld	a, c
   553B DD 96 06      [19]  811 	sub	a, 6 (ix)
   553E 77            [ 7]  812 	ld	(hl), a
                            813 ;src/entities/enemy.c:137: return 0;
   553F 2E 00         [ 7]  814 	ld	l, #0x00
   5541                     815 00106$:
   5541 DD E1         [14]  816 	pop	ix
   5543 C9            [10]  817 	ret
                            818 	.area _CODE
                            819 	.area _INITIALIZER
                            820 	.area _CABS (ABS)
