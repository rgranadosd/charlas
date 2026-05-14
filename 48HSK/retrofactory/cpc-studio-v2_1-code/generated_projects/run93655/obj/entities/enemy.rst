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
   507A                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   507A 21 03 00      [10]   57 	ld	hl, #2+1
   507D 39            [11]   58 	add	hl, sp
   507E 7E            [ 7]   59 	ld	a, (hl)
   507F 2B            [ 6]   60 	dec	hl
   5080 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   5081 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   5082 D1            [10]   65 	pop	de
   5083 C1            [10]   66 	pop	bc
   5084 C5            [11]   67 	push	bc
   5085 D5            [11]   68 	push	de
   5086 AF            [ 4]   69 	xor	a, a
   5087 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   5088 59            [ 4]   72 	ld	e, c
   5089 50            [ 4]   73 	ld	d, b
   508A 13            [ 6]   74 	inc	de
   508B AF            [ 4]   75 	xor	a, a
   508C 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   508D 59            [ 4]   78 	ld	e, c
   508E 50            [ 4]   79 	ld	d, b
   508F 13            [ 6]   80 	inc	de
   5090 13            [ 6]   81 	inc	de
   5091 AF            [ 4]   82 	xor	a, a
   5092 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   5093 59            [ 4]   85 	ld	e, c
   5094 50            [ 4]   86 	ld	d, b
   5095 13            [ 6]   87 	inc	de
   5096 13            [ 6]   88 	inc	de
   5097 13            [ 6]   89 	inc	de
   5098 AF            [ 4]   90 	xor	a, a
   5099 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   509A 21 04 00      [10]   93 	ld	hl, #0x0004
   509D 09            [11]   94 	add	hl, bc
   509E 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   50A0 21 05 00      [10]   97 	ld	hl, #0x0005
   50A3 09            [11]   98 	add	hl, bc
   50A4 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   50A6 21 06 00      [10]  101 	ld	hl, #0x0006
   50A9 09            [11]  102 	add	hl, bc
   50AA 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   50AC 21 07 00      [10]  105 	ld	hl, #0x0007
   50AF 09            [11]  106 	add	hl, bc
   50B0 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   50B2 21 08 00      [10]  109 	ld	hl, #0x0008
   50B5 09            [11]  110 	add	hl, bc
   50B6 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:19: enemy->kind = 0;
   50B8 21 09 00      [10]  113 	ld	hl, #0x0009
   50BB 09            [11]  114 	add	hl, bc
   50BC 36 00         [10]  115 	ld	(hl), #0x00
   50BE C9            [10]  116 	ret
                            117 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            118 ;	---------------------------------
                            119 ; Function enemyspawn
                            120 ; ---------------------------------
   50BF                     121 _enemyspawn::
   50BF DD E5         [15]  122 	push	ix
   50C1 DD 21 00 00   [14]  123 	ld	ix,#0
   50C5 DD 39         [15]  124 	add	ix,sp
   50C7 21 F1 FF      [10]  125 	ld	hl, #-15
   50CA 39            [11]  126 	add	hl, sp
   50CB F9            [ 6]  127 	ld	sp, hl
                            128 ;src/entities/enemy.c:23: if (!enemy) {
   50CC DD 7E 05      [19]  129 	ld	a, 5 (ix)
   50CF DD B6 04      [19]  130 	or	a,4 (ix)
                            131 ;src/entities/enemy.c:24: return;
   50D2 CA 92 52      [10]  132 	jp	Z,00112$
                            133 ;src/entities/enemy.c:27: enemy->x = x;
   50D5 DD 7E 04      [19]  134 	ld	a, 4 (ix)
   50D8 DD 77 FE      [19]  135 	ld	-2 (ix), a
   50DB DD 7E 05      [19]  136 	ld	a, 5 (ix)
   50DE DD 77 FF      [19]  137 	ld	-1 (ix), a
   50E1 DD 6E FE      [19]  138 	ld	l,-2 (ix)
   50E4 DD 66 FF      [19]  139 	ld	h,-1 (ix)
   50E7 DD 7E 06      [19]  140 	ld	a, 6 (ix)
   50EA 77            [ 7]  141 	ld	(hl), a
                            142 ;src/entities/enemy.c:28: enemy->y = y;
   50EB DD 4E FE      [19]  143 	ld	c,-2 (ix)
   50EE DD 46 FF      [19]  144 	ld	b,-1 (ix)
   50F1 03            [ 6]  145 	inc	bc
   50F2 DD 7E 07      [19]  146 	ld	a, 7 (ix)
   50F5 02            [ 7]  147 	ld	(bc), a
                            148 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   50F6 DD 7E FE      [19]  149 	ld	a, -2 (ix)
   50F9 C6 02         [ 7]  150 	add	a, #0x02
   50FB DD 77 FC      [19]  151 	ld	-4 (ix), a
   50FE DD 7E FF      [19]  152 	ld	a, -1 (ix)
   5101 CE 00         [ 7]  153 	adc	a, #0x00
   5103 DD 77 FD      [19]  154 	ld	-3 (ix), a
   5106 DD 7E 09      [19]  155 	ld	a, 9 (ix)
   5109 B7            [ 4]  156 	or	a, a
   510A 28 04         [12]  157 	jr	Z,00114$
   510C 0E 01         [ 7]  158 	ld	c, #0x01
   510E 18 02         [12]  159 	jr	00115$
   5110                     160 00114$:
   5110 0E FF         [ 7]  161 	ld	c, #0xff
   5112                     162 00115$:
   5112 DD 6E FC      [19]  163 	ld	l,-4 (ix)
   5115 DD 66 FD      [19]  164 	ld	h,-3 (ix)
   5118 71            [ 7]  165 	ld	(hl), c
                            166 ;src/entities/enemy.c:30: enemy->vy = 0;
   5119 DD 7E FE      [19]  167 	ld	a, -2 (ix)
   511C C6 03         [ 7]  168 	add	a, #0x03
   511E DD 77 FA      [19]  169 	ld	-6 (ix), a
   5121 DD 7E FF      [19]  170 	ld	a, -1 (ix)
   5124 CE 00         [ 7]  171 	adc	a, #0x00
   5126 DD 77 FB      [19]  172 	ld	-5 (ix), a
   5129 DD 6E FA      [19]  173 	ld	l,-6 (ix)
   512C DD 66 FB      [19]  174 	ld	h,-5 (ix)
   512F 36 00         [10]  175 	ld	(hl), #0x00
                            176 ;src/entities/enemy.c:31: enemy->active = 1;
   5131 DD 7E FE      [19]  177 	ld	a, -2 (ix)
   5134 C6 06         [ 7]  178 	add	a, #0x06
   5136 DD 77 F8      [19]  179 	ld	-8 (ix), a
   5139 DD 7E FF      [19]  180 	ld	a, -1 (ix)
   513C CE 00         [ 7]  181 	adc	a, #0x00
   513E DD 77 F9      [19]  182 	ld	-7 (ix), a
   5141 DD 6E F8      [19]  183 	ld	l,-8 (ix)
   5144 DD 66 F9      [19]  184 	ld	h,-7 (ix)
   5147 36 01         [10]  185 	ld	(hl), #0x01
                            186 ;src/entities/enemy.c:32: enemy->kind = kind;
   5149 DD 7E FE      [19]  187 	ld	a, -2 (ix)
   514C C6 09         [ 7]  188 	add	a, #0x09
   514E DD 77 F8      [19]  189 	ld	-8 (ix), a
   5151 DD 7E FF      [19]  190 	ld	a, -1 (ix)
   5154 CE 00         [ 7]  191 	adc	a, #0x00
   5156 DD 77 F9      [19]  192 	ld	-7 (ix), a
   5159 DD 6E F8      [19]  193 	ld	l,-8 (ix)
   515C DD 66 F9      [19]  194 	ld	h,-7 (ix)
   515F DD 7E 08      [19]  195 	ld	a, 8 (ix)
   5162 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/enemy.c:35: enemy->w = 5;
   5163 DD 7E FE      [19]  198 	ld	a, -2 (ix)
   5166 C6 04         [ 7]  199 	add	a, #0x04
   5168 DD 77 F8      [19]  200 	ld	-8 (ix), a
   516B DD 7E FF      [19]  201 	ld	a, -1 (ix)
   516E CE 00         [ 7]  202 	adc	a, #0x00
   5170 DD 77 F9      [19]  203 	ld	-7 (ix), a
                            204 ;src/entities/enemy.c:36: enemy->h = 14;
   5173 DD 7E FE      [19]  205 	ld	a, -2 (ix)
   5176 C6 05         [ 7]  206 	add	a, #0x05
   5178 DD 77 F6      [19]  207 	ld	-10 (ix), a
   517B DD 7E FF      [19]  208 	ld	a, -1 (ix)
   517E CE 00         [ 7]  209 	adc	a, #0x00
   5180 DD 77 F7      [19]  210 	ld	-9 (ix), a
                            211 ;src/entities/enemy.c:37: enemy->health = 2;
   5183 DD 7E FE      [19]  212 	ld	a, -2 (ix)
   5186 C6 07         [ 7]  213 	add	a, #0x07
   5188 DD 77 F4      [19]  214 	ld	-12 (ix), a
   518B DD 7E FF      [19]  215 	ld	a, -1 (ix)
   518E CE 00         [ 7]  216 	adc	a, #0x00
   5190 DD 77 F5      [19]  217 	ld	-11 (ix), a
                            218 ;src/entities/enemy.c:38: enemy->reward = 180;
   5193 DD 7E FE      [19]  219 	ld	a, -2 (ix)
   5196 C6 08         [ 7]  220 	add	a, #0x08
   5198 DD 77 FE      [19]  221 	ld	-2 (ix), a
   519B DD 7E FF      [19]  222 	ld	a, -1 (ix)
   519E CE 00         [ 7]  223 	adc	a, #0x00
   51A0 DD 77 FF      [19]  224 	ld	-1 (ix), a
                            225 ;src/entities/enemy.c:34: if (kind == 1) {
   51A3 DD 7E 08      [19]  226 	ld	a, 8 (ix)
   51A6 3D            [ 4]  227 	dec	a
   51A7 20 49         [12]  228 	jr	NZ,00110$
                            229 ;src/entities/enemy.c:35: enemy->w = 5;
   51A9 DD 6E F8      [19]  230 	ld	l,-8 (ix)
   51AC DD 66 F9      [19]  231 	ld	h,-7 (ix)
   51AF 36 05         [10]  232 	ld	(hl), #0x05
                            233 ;src/entities/enemy.c:36: enemy->h = 14;
   51B1 DD 6E F6      [19]  234 	ld	l,-10 (ix)
   51B4 DD 66 F7      [19]  235 	ld	h,-9 (ix)
   51B7 36 0E         [10]  236 	ld	(hl), #0x0e
                            237 ;src/entities/enemy.c:37: enemy->health = 2;
   51B9 DD 6E F4      [19]  238 	ld	l,-12 (ix)
   51BC DD 66 F5      [19]  239 	ld	h,-11 (ix)
   51BF 36 02         [10]  240 	ld	(hl), #0x02
                            241 ;src/entities/enemy.c:38: enemy->reward = 180;
   51C1 DD 6E FE      [19]  242 	ld	l,-2 (ix)
   51C4 DD 66 FF      [19]  243 	ld	h,-1 (ix)
   51C7 36 B4         [10]  244 	ld	(hl), #0xb4
                            245 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   51C9 DD 7E FC      [19]  246 	ld	a, -4 (ix)
   51CC DD 77 F2      [19]  247 	ld	-14 (ix), a
   51CF DD 7E FD      [19]  248 	ld	a, -3 (ix)
   51D2 DD 77 F3      [19]  249 	ld	-13 (ix), a
   51D5 DD 7E 09      [19]  250 	ld	a, 9 (ix)
   51D8 B7            [ 4]  251 	or	a, a
   51D9 28 06         [12]  252 	jr	Z,00116$
   51DB DD 36 F1 02   [19]  253 	ld	-15 (ix), #0x02
   51DF 18 04         [12]  254 	jr	00117$
   51E1                     255 00116$:
   51E1 DD 36 F1 FE   [19]  256 	ld	-15 (ix), #0xfe
   51E5                     257 00117$:
   51E5 DD 6E F2      [19]  258 	ld	l,-14 (ix)
   51E8 DD 66 F3      [19]  259 	ld	h,-13 (ix)
   51EB DD 7E F1      [19]  260 	ld	a, -15 (ix)
   51EE 77            [ 7]  261 	ld	(hl), a
   51EF C3 92 52      [10]  262 	jp	00112$
   51F2                     263 00110$:
                            264 ;src/entities/enemy.c:40: } else if (kind == 2) {
   51F2 DD 7E 08      [19]  265 	ld	a, 8 (ix)
   51F5 D6 02         [ 7]  266 	sub	a, #0x02
   51F7 20 3D         [12]  267 	jr	NZ,00107$
                            268 ;src/entities/enemy.c:41: enemy->w = 6;
   51F9 DD 6E F8      [19]  269 	ld	l,-8 (ix)
   51FC DD 66 F9      [19]  270 	ld	h,-7 (ix)
   51FF 36 06         [10]  271 	ld	(hl), #0x06
                            272 ;src/entities/enemy.c:42: enemy->h = 10;
   5201 DD 6E F6      [19]  273 	ld	l,-10 (ix)
   5204 DD 66 F7      [19]  274 	ld	h,-9 (ix)
   5207 36 0A         [10]  275 	ld	(hl), #0x0a
                            276 ;src/entities/enemy.c:43: enemy->health = 1;
   5209 DD 6E F4      [19]  277 	ld	l,-12 (ix)
   520C DD 66 F5      [19]  278 	ld	h,-11 (ix)
   520F 36 01         [10]  279 	ld	(hl), #0x01
                            280 ;src/entities/enemy.c:44: enemy->reward = 150;
   5211 DD 6E FE      [19]  281 	ld	l,-2 (ix)
   5214 DD 66 FF      [19]  282 	ld	h,-1 (ix)
   5217 36 96         [10]  283 	ld	(hl), #0x96
                            284 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   5219 DD 4E FA      [19]  285 	ld	c,-6 (ix)
   521C DD 46 FB      [19]  286 	ld	b,-5 (ix)
   521F DD 7E 09      [19]  287 	ld	a, 9 (ix)
   5222 B7            [ 4]  288 	or	a, a
   5223 28 04         [12]  289 	jr	Z,00118$
   5225 3E 01         [ 7]  290 	ld	a, #0x01
   5227 18 02         [12]  291 	jr	00119$
   5229                     292 00118$:
   5229 3E FF         [ 7]  293 	ld	a, #0xff
   522B                     294 00119$:
   522B 02            [ 7]  295 	ld	(bc), a
                            296 ;src/entities/enemy.c:46: enemy->vx = 1;
   522C DD 6E FC      [19]  297 	ld	l,-4 (ix)
   522F DD 66 FD      [19]  298 	ld	h,-3 (ix)
   5232 36 01         [10]  299 	ld	(hl), #0x01
   5234 18 5C         [12]  300 	jr	00112$
   5236                     301 00107$:
                            302 ;src/entities/enemy.c:47: } else if (kind == 3) {
   5236 DD 7E 08      [19]  303 	ld	a, 8 (ix)
   5239 D6 03         [ 7]  304 	sub	a, #0x03
   523B 20 35         [12]  305 	jr	NZ,00104$
                            306 ;src/entities/enemy.c:48: enemy->w = 10;
   523D DD 6E F8      [19]  307 	ld	l,-8 (ix)
   5240 DD 66 F9      [19]  308 	ld	h,-7 (ix)
   5243 36 0A         [10]  309 	ld	(hl), #0x0a
                            310 ;src/entities/enemy.c:49: enemy->h = 18;
   5245 DD 6E F6      [19]  311 	ld	l,-10 (ix)
   5248 DD 66 F7      [19]  312 	ld	h,-9 (ix)
   524B 36 12         [10]  313 	ld	(hl), #0x12
                            314 ;src/entities/enemy.c:50: enemy->health = 8;
   524D DD 6E F4      [19]  315 	ld	l,-12 (ix)
   5250 DD 66 F5      [19]  316 	ld	h,-11 (ix)
   5253 36 08         [10]  317 	ld	(hl), #0x08
                            318 ;src/entities/enemy.c:51: enemy->reward = 800;
   5255 DD 6E FE      [19]  319 	ld	l,-2 (ix)
   5258 DD 66 FF      [19]  320 	ld	h,-1 (ix)
   525B 36 20         [10]  321 	ld	(hl), #0x20
                            322 ;src/entities/enemy.c:52: enemy->vx = move_right ? 1 : -1;
   525D DD 4E FC      [19]  323 	ld	c,-4 (ix)
   5260 DD 46 FD      [19]  324 	ld	b,-3 (ix)
   5263 DD 7E 09      [19]  325 	ld	a, 9 (ix)
   5266 B7            [ 4]  326 	or	a, a
   5267 28 04         [12]  327 	jr	Z,00120$
   5269 3E 01         [ 7]  328 	ld	a, #0x01
   526B 18 02         [12]  329 	jr	00121$
   526D                     330 00120$:
   526D 3E FF         [ 7]  331 	ld	a, #0xff
   526F                     332 00121$:
   526F 02            [ 7]  333 	ld	(bc), a
   5270 18 20         [12]  334 	jr	00112$
   5272                     335 00104$:
                            336 ;src/entities/enemy.c:54: enemy->w = 4;
   5272 DD 6E F8      [19]  337 	ld	l,-8 (ix)
   5275 DD 66 F9      [19]  338 	ld	h,-7 (ix)
   5278 36 04         [10]  339 	ld	(hl), #0x04
                            340 ;src/entities/enemy.c:55: enemy->h = 16;
   527A DD 6E F6      [19]  341 	ld	l,-10 (ix)
   527D DD 66 F7      [19]  342 	ld	h,-9 (ix)
   5280 36 10         [10]  343 	ld	(hl), #0x10
                            344 ;src/entities/enemy.c:56: enemy->health = 1;
   5282 DD 6E F4      [19]  345 	ld	l,-12 (ix)
   5285 DD 66 F5      [19]  346 	ld	h,-11 (ix)
   5288 36 01         [10]  347 	ld	(hl), #0x01
                            348 ;src/entities/enemy.c:57: enemy->reward = 100;
   528A DD 6E FE      [19]  349 	ld	l,-2 (ix)
   528D DD 66 FF      [19]  350 	ld	h,-1 (ix)
   5290 36 64         [10]  351 	ld	(hl), #0x64
   5292                     352 00112$:
   5292 DD F9         [10]  353 	ld	sp, ix
   5294 DD E1         [14]  354 	pop	ix
   5296 C9            [10]  355 	ret
                            356 ;src/entities/enemy.c:61: void enemyupdate(Enemy* enemy) {
                            357 ;	---------------------------------
                            358 ; Function enemyupdate
                            359 ; ---------------------------------
   5297                     360 _enemyupdate::
   5297 DD E5         [15]  361 	push	ix
   5299 DD 21 00 00   [14]  362 	ld	ix,#0
   529D DD 39         [15]  363 	add	ix,sp
   529F 21 F6 FF      [10]  364 	ld	hl, #-10
   52A2 39            [11]  365 	add	hl, sp
   52A3 F9            [ 6]  366 	ld	sp, hl
                            367 ;src/entities/enemy.c:65: if (!enemy || !enemy->active) {
   52A4 DD 7E 05      [19]  368 	ld	a, 5 (ix)
   52A7 DD B6 04      [19]  369 	or	a,4 (ix)
   52AA CA 8D 54      [10]  370 	jp	Z,00121$
   52AD DD 7E 04      [19]  371 	ld	a, 4 (ix)
   52B0 DD 77 FE      [19]  372 	ld	-2 (ix), a
   52B3 DD 7E 05      [19]  373 	ld	a, 5 (ix)
   52B6 DD 77 FF      [19]  374 	ld	-1 (ix), a
   52B9 DD 6E FE      [19]  375 	ld	l,-2 (ix)
   52BC DD 66 FF      [19]  376 	ld	h,-1 (ix)
   52BF 11 06 00      [10]  377 	ld	de, #0x0006
   52C2 19            [11]  378 	add	hl, de
   52C3 7E            [ 7]  379 	ld	a, (hl)
   52C4 B7            [ 4]  380 	or	a, a
                            381 ;src/entities/enemy.c:66: return;
   52C5 CA 8D 54      [10]  382 	jp	Z,00121$
                            383 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   52C8 DD 6E FE      [19]  384 	ld	l,-2 (ix)
   52CB DD 66 FF      [19]  385 	ld	h,-1 (ix)
   52CE 11 09 00      [10]  386 	ld	de, #0x0009
   52D1 19            [11]  387 	add	hl, de
   52D2 7E            [ 7]  388 	ld	a, (hl)
   52D3 DD 77 FD      [19]  389 	ld	-3 (ix), a
                            390 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   52D6 DD 6E FE      [19]  391 	ld	l,-2 (ix)
   52D9 DD 66 FF      [19]  392 	ld	h,-1 (ix)
   52DC 4E            [ 7]  393 	ld	c, (hl)
   52DD DD 7E FE      [19]  394 	ld	a, -2 (ix)
   52E0 C6 02         [ 7]  395 	add	a, #0x02
   52E2 DD 77 FB      [19]  396 	ld	-5 (ix), a
   52E5 DD 7E FF      [19]  397 	ld	a, -1 (ix)
   52E8 CE 00         [ 7]  398 	adc	a, #0x00
   52EA DD 77 FC      [19]  399 	ld	-4 (ix), a
                            400 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   52ED DD 7E FE      [19]  401 	ld	a, -2 (ix)
   52F0 C6 01         [ 7]  402 	add	a, #0x01
   52F2 DD 77 F9      [19]  403 	ld	-7 (ix), a
   52F5 DD 7E FF      [19]  404 	ld	a, -1 (ix)
   52F8 CE 00         [ 7]  405 	adc	a, #0x00
   52FA DD 77 FA      [19]  406 	ld	-6 (ix), a
   52FD DD 5E FE      [19]  407 	ld	e,-2 (ix)
   5300 DD 56 FF      [19]  408 	ld	d,-1 (ix)
   5303 13            [ 6]  409 	inc	de
   5304 13            [ 6]  410 	inc	de
   5305 13            [ 6]  411 	inc	de
                            412 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
   5306 06 00         [ 7]  413 	ld	b, #0x00
   5308 DD 6E FB      [19]  414 	ld	l,-5 (ix)
   530B DD 66 FC      [19]  415 	ld	h,-4 (ix)
   530E 7E            [ 7]  416 	ld	a, (hl)
   530F DD 77 F8      [19]  417 	ld	-8 (ix), a
   5312 6F            [ 4]  418 	ld	l, a
   5313 DD 7E F8      [19]  419 	ld	a, -8 (ix)
   5316 17            [ 4]  420 	rla
   5317 9F            [ 4]  421 	sbc	a, a
   5318 67            [ 4]  422 	ld	h, a
   5319 09            [11]  423 	add	hl,bc
   531A 4D            [ 4]  424 	ld	c, l
   531B 44            [ 4]  425 	ld	b, h
                            426 ;src/entities/enemy.c:69: if (enemy->kind == 2) {
   531C DD 7E FD      [19]  427 	ld	a, -3 (ix)
   531F D6 02         [ 7]  428 	sub	a, #0x02
   5321 C2 CA 53      [10]  429 	jp	NZ,00111$
                            430 ;src/entities/enemy.c:70: nextx = (i16)enemy->x + (i16)enemy->vx;
                            431 ;src/entities/enemy.c:71: nexty = (i16)enemy->y + (i16)enemy->vy;
   5324 DD 6E F9      [19]  432 	ld	l,-7 (ix)
   5327 DD 66 FA      [19]  433 	ld	h,-6 (ix)
   532A 6E            [ 7]  434 	ld	l, (hl)
   532B DD 75 F6      [19]  435 	ld	-10 (ix), l
   532E DD 36 F7 00   [19]  436 	ld	-9 (ix), #0x00
   5332 1A            [ 7]  437 	ld	a, (de)
   5333 6F            [ 4]  438 	ld	l, a
   5334 17            [ 4]  439 	rla
   5335 9F            [ 4]  440 	sbc	a, a
   5336 67            [ 4]  441 	ld	h, a
   5337 DD 7E F6      [19]  442 	ld	a, -10 (ix)
   533A 85            [ 4]  443 	add	a, l
   533B DD 77 F6      [19]  444 	ld	-10 (ix), a
   533E DD 7E F7      [19]  445 	ld	a, -9 (ix)
   5341 8C            [ 4]  446 	adc	a, h
   5342 DD 77 F7      [19]  447 	ld	-9 (ix), a
                            448 ;src/entities/enemy.c:73: if (nextx < 8 || nextx > 72) {
   5345 79            [ 4]  449 	ld	a, c
   5346 D6 08         [ 7]  450 	sub	a, #0x08
   5348 78            [ 4]  451 	ld	a, b
   5349 17            [ 4]  452 	rla
   534A 3F            [ 4]  453 	ccf
   534B 1F            [ 4]  454 	rra
   534C DE 80         [ 7]  455 	sbc	a, #0x80
   534E 38 0E         [12]  456 	jr	C,00104$
   5350 3E 48         [ 7]  457 	ld	a, #0x48
   5352 B9            [ 4]  458 	cp	a, c
   5353 3E 00         [ 7]  459 	ld	a, #0x00
   5355 98            [ 4]  460 	sbc	a, b
   5356 E2 5B 53      [10]  461 	jp	PO, 00161$
   5359 EE 80         [ 7]  462 	xor	a, #0x80
   535B                     463 00161$:
   535B F2 79 53      [10]  464 	jp	P, 00105$
   535E                     465 00104$:
                            466 ;src/entities/enemy.c:74: enemy->vx = (i8)(-enemy->vx);
   535E AF            [ 4]  467 	xor	a, a
   535F DD 96 F8      [19]  468 	sub	a, -8 (ix)
   5362 4F            [ 4]  469 	ld	c, a
   5363 DD 6E FB      [19]  470 	ld	l,-5 (ix)
   5366 DD 66 FC      [19]  471 	ld	h,-4 (ix)
   5369 71            [ 7]  472 	ld	(hl), c
                            473 ;src/entities/enemy.c:75: nextx = (i16)enemy->x + (i16)enemy->vx;
   536A DD 6E FE      [19]  474 	ld	l,-2 (ix)
   536D DD 66 FF      [19]  475 	ld	h,-1 (ix)
   5370 6E            [ 7]  476 	ld	l, (hl)
   5371 26 00         [ 7]  477 	ld	h, #0x00
   5373 79            [ 4]  478 	ld	a, c
   5374 17            [ 4]  479 	rla
   5375 9F            [ 4]  480 	sbc	a, a
   5376 47            [ 4]  481 	ld	b, a
   5377 09            [11]  482 	add	hl,bc
   5378 4D            [ 4]  483 	ld	c, l
   5379                     484 00105$:
                            485 ;src/entities/enemy.c:77: if (nexty < 56 || nexty > 120) {
   5379 DD 7E F6      [19]  486 	ld	a, -10 (ix)
   537C D6 38         [ 7]  487 	sub	a, #0x38
   537E DD 7E F7      [19]  488 	ld	a, -9 (ix)
   5381 17            [ 4]  489 	rla
   5382 3F            [ 4]  490 	ccf
   5383 1F            [ 4]  491 	rra
   5384 DE 80         [ 7]  492 	sbc	a, #0x80
   5386 38 12         [12]  493 	jr	C,00107$
   5388 3E 78         [ 7]  494 	ld	a, #0x78
   538A DD BE F6      [19]  495 	cp	a, -10 (ix)
   538D 3E 00         [ 7]  496 	ld	a, #0x00
   538F DD 9E F7      [19]  497 	sbc	a, -9 (ix)
   5392 E2 97 53      [10]  498 	jp	PO, 00162$
   5395 EE 80         [ 7]  499 	xor	a, #0x80
   5397                     500 00162$:
   5397 F2 B6 53      [10]  501 	jp	P, 00108$
   539A                     502 00107$:
                            503 ;src/entities/enemy.c:78: enemy->vy = (i8)(-enemy->vy);
   539A 1A            [ 7]  504 	ld	a, (de)
   539B 6F            [ 4]  505 	ld	l, a
   539C AF            [ 4]  506 	xor	a, a
   539D 95            [ 4]  507 	sub	a, l
   539E DD 77 F8      [19]  508 	ld	-8 (ix), a
   53A1 12            [ 7]  509 	ld	(de),a
                            510 ;src/entities/enemy.c:79: nexty = (i16)enemy->y + (i16)enemy->vy;
   53A2 DD 6E F9      [19]  511 	ld	l,-7 (ix)
   53A5 DD 66 FA      [19]  512 	ld	h,-6 (ix)
   53A8 5E            [ 7]  513 	ld	e, (hl)
   53A9 16 00         [ 7]  514 	ld	d, #0x00
   53AB DD 6E F8      [19]  515 	ld	l, -8 (ix)
   53AE DD 7E F8      [19]  516 	ld	a, -8 (ix)
   53B1 17            [ 4]  517 	rla
   53B2 9F            [ 4]  518 	sbc	a, a
   53B3 67            [ 4]  519 	ld	h, a
   53B4 19            [11]  520 	add	hl,de
   53B5 E3            [19]  521 	ex	(sp), hl
   53B6                     522 00108$:
                            523 ;src/entities/enemy.c:82: enemy->x = (u8)nextx;
   53B6 DD 6E FE      [19]  524 	ld	l,-2 (ix)
   53B9 DD 66 FF      [19]  525 	ld	h,-1 (ix)
   53BC 71            [ 7]  526 	ld	(hl), c
                            527 ;src/entities/enemy.c:83: enemy->y = (u8)nexty;
   53BD DD 4E F6      [19]  528 	ld	c, -10 (ix)
   53C0 DD 6E F9      [19]  529 	ld	l,-7 (ix)
   53C3 DD 66 FA      [19]  530 	ld	h,-6 (ix)
   53C6 71            [ 7]  531 	ld	(hl), c
                            532 ;src/entities/enemy.c:84: return;
   53C7 C3 8D 54      [10]  533 	jp	00121$
   53CA                     534 00111$:
                            535 ;src/entities/enemy.c:87: nextx = (i16)enemy->x + (i16)enemy->vx;
                            536 ;src/entities/enemy.c:88: if (nextx < 2) {
   53CA 79            [ 4]  537 	ld	a, c
   53CB D6 02         [ 7]  538 	sub	a, #0x02
   53CD 78            [ 4]  539 	ld	a, b
   53CE 17            [ 4]  540 	rla
   53CF 3F            [ 4]  541 	ccf
   53D0 1F            [ 4]  542 	rra
   53D1 DE 80         [ 7]  543 	sbc	a, #0x80
   53D3 30 0B         [12]  544 	jr	NC,00113$
                            545 ;src/entities/enemy.c:89: nextx = 2;
   53D5 01 02 00      [10]  546 	ld	bc, #0x0002
                            547 ;src/entities/enemy.c:90: enemy->vx = 1;
   53D8 DD 6E FB      [19]  548 	ld	l,-5 (ix)
   53DB DD 66 FC      [19]  549 	ld	h,-4 (ix)
   53DE 36 01         [10]  550 	ld	(hl), #0x01
   53E0                     551 00113$:
                            552 ;src/entities/enemy.c:92: if (nextx > 74) {
   53E0 3E 4A         [ 7]  553 	ld	a, #0x4a
   53E2 B9            [ 4]  554 	cp	a, c
   53E3 3E 00         [ 7]  555 	ld	a, #0x00
   53E5 98            [ 4]  556 	sbc	a, b
   53E6 E2 EB 53      [10]  557 	jp	PO, 00163$
   53E9 EE 80         [ 7]  558 	xor	a, #0x80
   53EB                     559 00163$:
   53EB F2 F9 53      [10]  560 	jp	P, 00115$
                            561 ;src/entities/enemy.c:93: nextx = 74;
   53EE 01 4A 00      [10]  562 	ld	bc, #0x004a
                            563 ;src/entities/enemy.c:94: enemy->vx = -1;
   53F1 DD 6E FB      [19]  564 	ld	l,-5 (ix)
   53F4 DD 66 FC      [19]  565 	ld	h,-4 (ix)
   53F7 36 FF         [10]  566 	ld	(hl), #0xff
   53F9                     567 00115$:
                            568 ;src/entities/enemy.c:96: enemy->x = (u8)nextx;
   53F9 DD 6E FE      [19]  569 	ld	l,-2 (ix)
   53FC DD 66 FF      [19]  570 	ld	h,-1 (ix)
   53FF 71            [ 7]  571 	ld	(hl), c
                            572 ;src/entities/enemy.c:98: enemy->vy = (i8)(enemy->vy + 1);
   5400 1A            [ 7]  573 	ld	a, (de)
   5401 4F            [ 4]  574 	ld	c, a
   5402 0C            [ 4]  575 	inc	c
   5403 79            [ 4]  576 	ld	a, c
   5404 12            [ 7]  577 	ld	(de), a
                            578 ;src/entities/enemy.c:99: if (enemy->vy > 3) enemy->vy = 3;
   5405 3E 03         [ 7]  579 	ld	a, #0x03
   5407 91            [ 4]  580 	sub	a, c
   5408 E2 0D 54      [10]  581 	jp	PO, 00164$
   540B EE 80         [ 7]  582 	xor	a, #0x80
   540D                     583 00164$:
   540D F2 13 54      [10]  584 	jp	P, 00117$
   5410 3E 03         [ 7]  585 	ld	a, #0x03
   5412 12            [ 7]  586 	ld	(de), a
   5413                     587 00117$:
                            588 ;src/entities/enemy.c:100: nexty = (i16)enemy->y + (i16)enemy->vy;
   5413 DD 6E F9      [19]  589 	ld	l,-7 (ix)
   5416 DD 66 FA      [19]  590 	ld	h,-6 (ix)
   5419 4E            [ 7]  591 	ld	c, (hl)
   541A 06 00         [ 7]  592 	ld	b, #0x00
   541C 1A            [ 7]  593 	ld	a, (de)
   541D 6F            [ 4]  594 	ld	l, a
   541E 17            [ 4]  595 	rla
   541F 9F            [ 4]  596 	sbc	a, a
   5420 67            [ 4]  597 	ld	h, a
   5421 09            [11]  598 	add	hl, bc
   5422 E5            [11]  599 	push	hl
   5423 FD E1         [14]  600 	pop	iy
                            601 ;src/entities/enemy.c:101: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5425 DD 7E FE      [19]  602 	ld	a, -2 (ix)
   5428 C6 05         [ 7]  603 	add	a, #0x05
   542A DD 77 F6      [19]  604 	ld	-10 (ix), a
   542D DD 7E FF      [19]  605 	ld	a, -1 (ix)
   5430 CE 00         [ 7]  606 	adc	a, #0x00
   5432 DD 77 F7      [19]  607 	ld	-9 (ix), a
   5435 E1            [10]  608 	pop	hl
   5436 E5            [11]  609 	push	hl
   5437 7E            [ 7]  610 	ld	a, (hl)
   5438 DD 6E FE      [19]  611 	ld	l,-2 (ix)
   543B DD 66 FF      [19]  612 	ld	h,-1 (ix)
   543E 4E            [ 7]  613 	ld	c, (hl)
   543F 06 00         [ 7]  614 	ld	b, #0x00
   5441 D5            [11]  615 	push	de
   5442 F5            [11]  616 	push	af
   5443 33            [ 6]  617 	inc	sp
   5444 FD E5         [15]  618 	push	iy
   5446 C5            [11]  619 	push	bc
   5447 CD E1 4A      [17]  620 	call	_collision_clamp_y_at
   544A F1            [10]  621 	pop	af
   544B F1            [10]  622 	pop	af
   544C 33            [ 6]  623 	inc	sp
   544D 4D            [ 4]  624 	ld	c, l
   544E D1            [10]  625 	pop	de
                            626 ;src/entities/enemy.c:102: enemy->y = (u8)nexty;
   544F DD 6E F9      [19]  627 	ld	l,-7 (ix)
   5452 DD 66 FA      [19]  628 	ld	h,-6 (ix)
   5455 71            [ 7]  629 	ld	(hl), c
                            630 ;src/entities/enemy.c:103: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5456 E1            [10]  631 	pop	hl
   5457 E5            [11]  632 	push	hl
   5458 7E            [ 7]  633 	ld	a, (hl)
   5459 06 00         [ 7]  634 	ld	b, #0x00
   545B DD 6E FE      [19]  635 	ld	l,-2 (ix)
   545E DD 66 FF      [19]  636 	ld	h,-1 (ix)
   5461 6E            [ 7]  637 	ld	l, (hl)
   5462 DD 75 F6      [19]  638 	ld	-10 (ix), l
   5465 DD 36 F7 00   [19]  639 	ld	-9 (ix), #0x00
   5469 D5            [11]  640 	push	de
   546A F5            [11]  641 	push	af
   546B 33            [ 6]  642 	inc	sp
   546C C5            [11]  643 	push	bc
   546D DD 6E F6      [19]  644 	ld	l,-10 (ix)
   5470 DD 66 F7      [19]  645 	ld	h,-9 (ix)
   5473 E5            [11]  646 	push	hl
   5474 CD 62 4A      [17]  647 	call	_collision_is_on_ground_at
   5477 F1            [10]  648 	pop	af
   5478 F1            [10]  649 	pop	af
   5479 33            [ 6]  650 	inc	sp
   547A D1            [10]  651 	pop	de
   547B 7D            [ 4]  652 	ld	a, l
   547C B7            [ 4]  653 	or	a, a
   547D 28 0E         [12]  654 	jr	Z,00121$
   547F 1A            [ 7]  655 	ld	a, (de)
   5480 4F            [ 4]  656 	ld	c, a
   5481 AF            [ 4]  657 	xor	a, a
   5482 91            [ 4]  658 	sub	a, c
   5483 E2 88 54      [10]  659 	jp	PO, 00165$
   5486 EE 80         [ 7]  660 	xor	a, #0x80
   5488                     661 00165$:
   5488 F2 8D 54      [10]  662 	jp	P, 00121$
                            663 ;src/entities/enemy.c:104: enemy->vy = 0;
   548B AF            [ 4]  664 	xor	a, a
   548C 12            [ 7]  665 	ld	(de), a
   548D                     666 00121$:
   548D DD F9         [10]  667 	ld	sp, ix
   548F DD E1         [14]  668 	pop	ix
   5491 C9            [10]  669 	ret
                            670 ;src/entities/enemy.c:108: void enemyrender(const Enemy* enemy) {
                            671 ;	---------------------------------
                            672 ; Function enemyrender
                            673 ; ---------------------------------
   5492                     674 _enemyrender::
   5492 DD E5         [15]  675 	push	ix
   5494 DD 21 00 00   [14]  676 	ld	ix,#0
   5498 DD 39         [15]  677 	add	ix,sp
   549A 3B            [ 6]  678 	dec	sp
                            679 ;src/entities/enemy.c:112: if (!enemy || !enemy->active) {
   549B DD 7E 05      [19]  680 	ld	a, 5 (ix)
   549E DD B6 04      [19]  681 	or	a,4 (ix)
   54A1 28 65         [12]  682 	jr	Z,00113$
   54A3 DD 4E 04      [19]  683 	ld	c,4 (ix)
   54A6 DD 46 05      [19]  684 	ld	b,5 (ix)
   54A9 C5            [11]  685 	push	bc
   54AA FD E1         [14]  686 	pop	iy
   54AC FD 7E 06      [19]  687 	ld	a, 6 (iy)
   54AF B7            [ 4]  688 	or	a, a
                            689 ;src/entities/enemy.c:113: return;
   54B0 28 56         [12]  690 	jr	Z,00113$
                            691 ;src/entities/enemy.c:116: if (enemy->kind == 3) colour = 0x4C;
   54B2 C5            [11]  692 	push	bc
   54B3 FD E1         [14]  693 	pop	iy
   54B5 FD 7E 09      [19]  694 	ld	a, 9 (iy)
   54B8 FE 03         [ 7]  695 	cp	a, #0x03
   54BA 20 04         [12]  696 	jr	NZ,00111$
   54BC 1E 4C         [ 7]  697 	ld	e, #0x4c
   54BE 18 11         [12]  698 	jr	00112$
   54C0                     699 00111$:
                            700 ;src/entities/enemy.c:117: else if (enemy->kind == 2) colour = 0x5A;
   54C0 FE 02         [ 7]  701 	cp	a, #0x02
   54C2 20 04         [12]  702 	jr	NZ,00108$
   54C4 1E 5A         [ 7]  703 	ld	e, #0x5a
   54C6 18 09         [12]  704 	jr	00112$
   54C8                     705 00108$:
                            706 ;src/entities/enemy.c:118: else if (enemy->kind == 1) colour = 0x4E;
   54C8 3D            [ 4]  707 	dec	a
   54C9 20 04         [12]  708 	jr	NZ,00105$
   54CB 1E 4E         [ 7]  709 	ld	e, #0x4e
   54CD 18 02         [12]  710 	jr	00112$
   54CF                     711 00105$:
                            712 ;src/entities/enemy.c:119: else colour = 0x5C;
   54CF 1E 5C         [ 7]  713 	ld	e, #0x5c
   54D1                     714 00112$:
                            715 ;src/entities/enemy.c:121: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   54D1 69            [ 4]  716 	ld	l, c
   54D2 60            [ 4]  717 	ld	h, b
   54D3 23            [ 6]  718 	inc	hl
   54D4 56            [ 7]  719 	ld	d, (hl)
   54D5 0A            [ 7]  720 	ld	a, (bc)
   54D6 C5            [11]  721 	push	bc
   54D7 D5            [11]  722 	push	de
   54D8 5F            [ 4]  723 	ld	e, a
   54D9 D5            [11]  724 	push	de
   54DA 21 00 C0      [10]  725 	ld	hl, #0xc000
   54DD E5            [11]  726 	push	hl
   54DE CD 7C 5D      [17]  727 	call	_cpct_getScreenPtr
   54E1 D1            [10]  728 	pop	de
   54E2 C1            [10]  729 	pop	bc
   54E3 E5            [11]  730 	push	hl
   54E4 FD E1         [14]  731 	pop	iy
                            732 ;src/entities/enemy.c:122: cpct_drawSolidBox(pvmem, colour, enemy->w, enemy->h);
   54E6 69            [ 4]  733 	ld	l, c
   54E7 60            [ 4]  734 	ld	h, b
   54E8 23            [ 6]  735 	inc	hl
   54E9 23            [ 6]  736 	inc	hl
   54EA 23            [ 6]  737 	inc	hl
   54EB 23            [ 6]  738 	inc	hl
   54EC 23            [ 6]  739 	inc	hl
   54ED 7E            [ 7]  740 	ld	a, (hl)
   54EE DD 77 FF      [19]  741 	ld	-1 (ix), a
   54F1 69            [ 4]  742 	ld	l, c
   54F2 60            [ 4]  743 	ld	h, b
   54F3 01 04 00      [10]  744 	ld	bc, #0x0004
   54F6 09            [11]  745 	add	hl, bc
   54F7 56            [ 7]  746 	ld	d, (hl)
   54F8 FD E5         [15]  747 	push	iy
   54FA C1            [10]  748 	pop	bc
   54FB DD 7E FF      [19]  749 	ld	a, -1 (ix)
   54FE F5            [11]  750 	push	af
   54FF 33            [ 6]  751 	inc	sp
   5500 D5            [11]  752 	push	de
   5501 C5            [11]  753 	push	bc
   5502 CD C3 5C      [17]  754 	call	_cpct_drawSolidBox
   5505 F1            [10]  755 	pop	af
   5506 F1            [10]  756 	pop	af
   5507 33            [ 6]  757 	inc	sp
   5508                     758 00113$:
   5508 33            [ 6]  759 	inc	sp
   5509 DD E1         [14]  760 	pop	ix
   550B C9            [10]  761 	ret
                            762 ;src/entities/enemy.c:125: u8 enemydamage(Enemy* enemy, u8 damage) {
                            763 ;	---------------------------------
                            764 ; Function enemydamage
                            765 ; ---------------------------------
   550C                     766 _enemydamage::
   550C DD E5         [15]  767 	push	ix
   550E DD 21 00 00   [14]  768 	ld	ix,#0
   5512 DD 39         [15]  769 	add	ix,sp
                            770 ;src/entities/enemy.c:126: if (!enemy || !enemy->active) {
   5514 DD 7E 05      [19]  771 	ld	a, 5 (ix)
   5517 DD B6 04      [19]  772 	or	a,4 (ix)
   551A 28 0F         [12]  773 	jr	Z,00101$
   551C DD 4E 04      [19]  774 	ld	c,4 (ix)
   551F DD 46 05      [19]  775 	ld	b,5 (ix)
   5522 21 06 00      [10]  776 	ld	hl, #0x0006
   5525 09            [11]  777 	add	hl,bc
   5526 EB            [ 4]  778 	ex	de,hl
   5527 1A            [ 7]  779 	ld	a, (de)
   5528 B7            [ 4]  780 	or	a, a
   5529 20 04         [12]  781 	jr	NZ,00102$
   552B                     782 00101$:
                            783 ;src/entities/enemy.c:127: return 0;
   552B 2E 00         [ 7]  784 	ld	l, #0x00
   552D 18 1A         [12]  785 	jr	00106$
   552F                     786 00102$:
                            787 ;src/entities/enemy.c:130: if (damage >= enemy->health) {
   552F 21 07 00      [10]  788 	ld	hl, #0x0007
   5532 09            [11]  789 	add	hl, bc
   5533 4E            [ 7]  790 	ld	c, (hl)
   5534 DD 7E 06      [19]  791 	ld	a, 6 (ix)
   5537 91            [ 4]  792 	sub	a, c
   5538 38 08         [12]  793 	jr	C,00105$
                            794 ;src/entities/enemy.c:131: enemy->health = 0;
   553A 36 00         [10]  795 	ld	(hl), #0x00
                            796 ;src/entities/enemy.c:132: enemy->active = 0;
   553C AF            [ 4]  797 	xor	a, a
   553D 12            [ 7]  798 	ld	(de), a
                            799 ;src/entities/enemy.c:133: return 1;
   553E 2E 01         [ 7]  800 	ld	l, #0x01
   5540 18 07         [12]  801 	jr	00106$
   5542                     802 00105$:
                            803 ;src/entities/enemy.c:136: enemy->health = (u8)(enemy->health - damage);
   5542 79            [ 4]  804 	ld	a, c
   5543 DD 96 06      [19]  805 	sub	a, 6 (ix)
   5546 77            [ 7]  806 	ld	(hl), a
                            807 ;src/entities/enemy.c:137: return 0;
   5547 2E 00         [ 7]  808 	ld	l, #0x00
   5549                     809 00106$:
   5549 DD E1         [14]  810 	pop	ix
   554B C9            [10]  811 	ret
                            812 	.area _CODE
                            813 	.area _INITIALIZER
                            814 	.area _CABS (ABS)
