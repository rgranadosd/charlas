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
   4FAF                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   4FAF 21 03 00      [10]   57 	ld	hl, #2+1
   4FB2 39            [11]   58 	add	hl, sp
   4FB3 7E            [ 7]   59 	ld	a, (hl)
   4FB4 2B            [ 6]   60 	dec	hl
   4FB5 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   4FB6 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   4FB7 D1            [10]   65 	pop	de
   4FB8 C1            [10]   66 	pop	bc
   4FB9 C5            [11]   67 	push	bc
   4FBA D5            [11]   68 	push	de
   4FBB AF            [ 4]   69 	xor	a, a
   4FBC 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   4FBD 59            [ 4]   72 	ld	e, c
   4FBE 50            [ 4]   73 	ld	d, b
   4FBF 13            [ 6]   74 	inc	de
   4FC0 AF            [ 4]   75 	xor	a, a
   4FC1 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   4FC2 59            [ 4]   78 	ld	e, c
   4FC3 50            [ 4]   79 	ld	d, b
   4FC4 13            [ 6]   80 	inc	de
   4FC5 13            [ 6]   81 	inc	de
   4FC6 AF            [ 4]   82 	xor	a, a
   4FC7 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   4FC8 59            [ 4]   85 	ld	e, c
   4FC9 50            [ 4]   86 	ld	d, b
   4FCA 13            [ 6]   87 	inc	de
   4FCB 13            [ 6]   88 	inc	de
   4FCC 13            [ 6]   89 	inc	de
   4FCD AF            [ 4]   90 	xor	a, a
   4FCE 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   4FCF 21 04 00      [10]   93 	ld	hl, #0x0004
   4FD2 09            [11]   94 	add	hl, bc
   4FD3 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   4FD5 21 05 00      [10]   97 	ld	hl, #0x0005
   4FD8 09            [11]   98 	add	hl, bc
   4FD9 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   4FDB 21 06 00      [10]  101 	ld	hl, #0x0006
   4FDE 09            [11]  102 	add	hl, bc
   4FDF 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   4FE1 21 07 00      [10]  105 	ld	hl, #0x0007
   4FE4 09            [11]  106 	add	hl, bc
   4FE5 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   4FE7 21 08 00      [10]  109 	ld	hl, #0x0008
   4FEA 09            [11]  110 	add	hl, bc
   4FEB 36 64         [10]  111 	ld	(hl), #0x64
   4FED C9            [10]  112 	ret
                            113 ;src/entities/enemy.c:21: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 move_right) {
                            114 ;	---------------------------------
                            115 ; Function enemyspawn
                            116 ; ---------------------------------
   4FEE                     117 _enemyspawn::
                            118 ;src/entities/enemy.c:22: if (!enemy) {
   4FEE 21 03 00      [10]  119 	ld	hl, #2+1
   4FF1 39            [11]  120 	add	hl, sp
   4FF2 7E            [ 7]  121 	ld	a, (hl)
   4FF3 2B            [ 6]  122 	dec	hl
   4FF4 B6            [ 7]  123 	or	a,(hl)
                            124 ;src/entities/enemy.c:23: return;
   4FF5 C8            [11]  125 	ret	Z
                            126 ;src/entities/enemy.c:26: enemy->x = x;
   4FF6 D1            [10]  127 	pop	de
   4FF7 C1            [10]  128 	pop	bc
   4FF8 C5            [11]  129 	push	bc
   4FF9 D5            [11]  130 	push	de
   4FFA 21 04 00      [10]  131 	ld	hl, #4+0
   4FFD 39            [11]  132 	add	hl, sp
   4FFE 7E            [ 7]  133 	ld	a, (hl)
   4FFF 02            [ 7]  134 	ld	(bc), a
                            135 ;src/entities/enemy.c:27: enemy->y = y;
   5000 59            [ 4]  136 	ld	e, c
   5001 50            [ 4]  137 	ld	d, b
   5002 13            [ 6]  138 	inc	de
   5003 21 05 00      [10]  139 	ld	hl, #5+0
   5006 39            [11]  140 	add	hl, sp
   5007 7E            [ 7]  141 	ld	a, (hl)
   5008 12            [ 7]  142 	ld	(de), a
                            143 ;src/entities/enemy.c:28: enemy->vx = move_right ? 1 : -1;
   5009 59            [ 4]  144 	ld	e, c
   500A 50            [ 4]  145 	ld	d, b
   500B 13            [ 6]  146 	inc	de
   500C 13            [ 6]  147 	inc	de
   500D 21 06 00      [10]  148 	ld	hl, #6+0
   5010 39            [11]  149 	add	hl, sp
   5011 7E            [ 7]  150 	ld	a, (hl)
   5012 B7            [ 4]  151 	or	a, a
   5013 28 04         [12]  152 	jr	Z,00105$
   5015 3E 01         [ 7]  153 	ld	a, #0x01
   5017 18 02         [12]  154 	jr	00106$
   5019                     155 00105$:
   5019 3E FF         [ 7]  156 	ld	a, #0xff
   501B                     157 00106$:
   501B 12            [ 7]  158 	ld	(de), a
                            159 ;src/entities/enemy.c:29: enemy->vy = 0;
   501C 59            [ 4]  160 	ld	e, c
   501D 50            [ 4]  161 	ld	d, b
   501E 13            [ 6]  162 	inc	de
   501F 13            [ 6]  163 	inc	de
   5020 13            [ 6]  164 	inc	de
   5021 AF            [ 4]  165 	xor	a, a
   5022 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/enemy.c:30: enemy->active = 1;
   5023 21 06 00      [10]  168 	ld	hl, #0x0006
   5026 09            [11]  169 	add	hl, bc
   5027 36 01         [10]  170 	ld	(hl), #0x01
                            171 ;src/entities/enemy.c:31: enemy->health = 1;
   5029 21 07 00      [10]  172 	ld	hl, #0x0007
   502C 09            [11]  173 	add	hl, bc
   502D 36 01         [10]  174 	ld	(hl), #0x01
   502F C9            [10]  175 	ret
                            176 ;src/entities/enemy.c:34: void enemyupdate(Enemy* enemy) {
                            177 ;	---------------------------------
                            178 ; Function enemyupdate
                            179 ; ---------------------------------
   5030                     180 _enemyupdate::
   5030 DD E5         [15]  181 	push	ix
   5032 DD 21 00 00   [14]  182 	ld	ix,#0
   5036 DD 39         [15]  183 	add	ix,sp
   5038 21 FA FF      [10]  184 	ld	hl, #-6
   503B 39            [11]  185 	add	hl, sp
   503C F9            [ 6]  186 	ld	sp, hl
                            187 ;src/entities/enemy.c:38: if (!enemy || !enemy->active) {
   503D DD 7E 05      [19]  188 	ld	a, 5 (ix)
   5040 DD B6 04      [19]  189 	or	a,4 (ix)
   5043 CA 4B 51      [10]  190 	jp	Z,00113$
   5046 DD 7E 04      [19]  191 	ld	a, 4 (ix)
   5049 DD 77 FE      [19]  192 	ld	-2 (ix), a
   504C DD 7E 05      [19]  193 	ld	a, 5 (ix)
   504F DD 77 FF      [19]  194 	ld	-1 (ix), a
   5052 DD 6E FE      [19]  195 	ld	l,-2 (ix)
   5055 DD 66 FF      [19]  196 	ld	h,-1 (ix)
   5058 11 06 00      [10]  197 	ld	de, #0x0006
   505B 19            [11]  198 	add	hl, de
   505C 7E            [ 7]  199 	ld	a, (hl)
   505D B7            [ 4]  200 	or	a, a
                            201 ;src/entities/enemy.c:39: return;
   505E CA 4B 51      [10]  202 	jp	Z,00113$
                            203 ;src/entities/enemy.c:42: nextx = (i16)enemy->x + (i16)enemy->vx;
   5061 DD 6E FE      [19]  204 	ld	l,-2 (ix)
   5064 DD 66 FF      [19]  205 	ld	h,-1 (ix)
   5067 5E            [ 7]  206 	ld	e, (hl)
   5068 16 00         [ 7]  207 	ld	d, #0x00
   506A DD 4E FE      [19]  208 	ld	c,-2 (ix)
   506D DD 46 FF      [19]  209 	ld	b,-1 (ix)
   5070 03            [ 6]  210 	inc	bc
   5071 03            [ 6]  211 	inc	bc
   5072 0A            [ 7]  212 	ld	a, (bc)
   5073 6F            [ 4]  213 	ld	l, a
   5074 17            [ 4]  214 	rla
   5075 9F            [ 4]  215 	sbc	a, a
   5076 67            [ 4]  216 	ld	h, a
   5077 19            [11]  217 	add	hl,de
   5078 EB            [ 4]  218 	ex	de,hl
                            219 ;src/entities/enemy.c:43: if (nextx < 2) {
   5079 7B            [ 4]  220 	ld	a, e
   507A D6 02         [ 7]  221 	sub	a, #0x02
   507C 7A            [ 4]  222 	ld	a, d
   507D 17            [ 4]  223 	rla
   507E 3F            [ 4]  224 	ccf
   507F 1F            [ 4]  225 	rra
   5080 DE 80         [ 7]  226 	sbc	a, #0x80
   5082 30 06         [12]  227 	jr	NC,00105$
                            228 ;src/entities/enemy.c:44: nextx = 2;
   5084 11 02 00      [10]  229 	ld	de, #0x0002
                            230 ;src/entities/enemy.c:45: enemy->vx = 1;
   5087 3E 01         [ 7]  231 	ld	a, #0x01
   5089 02            [ 7]  232 	ld	(bc), a
   508A                     233 00105$:
                            234 ;src/entities/enemy.c:47: if (nextx > 74) {
   508A 3E 4A         [ 7]  235 	ld	a, #0x4a
   508C BB            [ 4]  236 	cp	a, e
   508D 3E 00         [ 7]  237 	ld	a, #0x00
   508F 9A            [ 4]  238 	sbc	a, d
   5090 E2 95 50      [10]  239 	jp	PO, 00139$
   5093 EE 80         [ 7]  240 	xor	a, #0x80
   5095                     241 00139$:
   5095 F2 9E 50      [10]  242 	jp	P, 00107$
                            243 ;src/entities/enemy.c:48: nextx = 74;
   5098 11 4A 00      [10]  244 	ld	de, #0x004a
                            245 ;src/entities/enemy.c:49: enemy->vx = -1;
   509B 3E FF         [ 7]  246 	ld	a, #0xff
   509D 02            [ 7]  247 	ld	(bc), a
   509E                     248 00107$:
                            249 ;src/entities/enemy.c:51: enemy->x = (u8)nextx;
   509E DD 6E FE      [19]  250 	ld	l,-2 (ix)
   50A1 DD 66 FF      [19]  251 	ld	h,-1 (ix)
   50A4 73            [ 7]  252 	ld	(hl), e
                            253 ;src/entities/enemy.c:53: enemy->vy = (i8)(enemy->vy + 1);
   50A5 DD 5E FE      [19]  254 	ld	e,-2 (ix)
   50A8 DD 56 FF      [19]  255 	ld	d,-1 (ix)
   50AB 13            [ 6]  256 	inc	de
   50AC 13            [ 6]  257 	inc	de
   50AD 13            [ 6]  258 	inc	de
   50AE 1A            [ 7]  259 	ld	a, (de)
   50AF 4F            [ 4]  260 	ld	c, a
   50B0 0C            [ 4]  261 	inc	c
   50B1 79            [ 4]  262 	ld	a, c
   50B2 12            [ 7]  263 	ld	(de), a
                            264 ;src/entities/enemy.c:54: if (enemy->vy > 3) enemy->vy = 3;
   50B3 3E 03         [ 7]  265 	ld	a, #0x03
   50B5 91            [ 4]  266 	sub	a, c
   50B6 E2 BB 50      [10]  267 	jp	PO, 00140$
   50B9 EE 80         [ 7]  268 	xor	a, #0x80
   50BB                     269 00140$:
   50BB F2 C1 50      [10]  270 	jp	P, 00109$
   50BE 3E 03         [ 7]  271 	ld	a, #0x03
   50C0 12            [ 7]  272 	ld	(de), a
   50C1                     273 00109$:
                            274 ;src/entities/enemy.c:55: nexty = (i16)enemy->y + (i16)enemy->vy;
   50C1 DD 7E FE      [19]  275 	ld	a, -2 (ix)
   50C4 C6 01         [ 7]  276 	add	a, #0x01
   50C6 DD 77 FC      [19]  277 	ld	-4 (ix), a
   50C9 DD 7E FF      [19]  278 	ld	a, -1 (ix)
   50CC CE 00         [ 7]  279 	adc	a, #0x00
   50CE DD 77 FD      [19]  280 	ld	-3 (ix), a
   50D1 DD 6E FC      [19]  281 	ld	l,-4 (ix)
   50D4 DD 66 FD      [19]  282 	ld	h,-3 (ix)
   50D7 4E            [ 7]  283 	ld	c, (hl)
   50D8 06 00         [ 7]  284 	ld	b, #0x00
   50DA 1A            [ 7]  285 	ld	a, (de)
   50DB 6F            [ 4]  286 	ld	l, a
   50DC 17            [ 4]  287 	rla
   50DD 9F            [ 4]  288 	sbc	a, a
   50DE 67            [ 4]  289 	ld	h, a
   50DF 09            [11]  290 	add	hl, bc
   50E0 E5            [11]  291 	push	hl
   50E1 FD E1         [14]  292 	pop	iy
                            293 ;src/entities/enemy.c:56: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   50E3 DD 7E FE      [19]  294 	ld	a, -2 (ix)
   50E6 C6 05         [ 7]  295 	add	a, #0x05
   50E8 DD 77 FA      [19]  296 	ld	-6 (ix), a
   50EB DD 7E FF      [19]  297 	ld	a, -1 (ix)
   50EE CE 00         [ 7]  298 	adc	a, #0x00
   50F0 DD 77 FB      [19]  299 	ld	-5 (ix), a
   50F3 E1            [10]  300 	pop	hl
   50F4 E5            [11]  301 	push	hl
   50F5 7E            [ 7]  302 	ld	a, (hl)
   50F6 DD 6E FE      [19]  303 	ld	l,-2 (ix)
   50F9 DD 66 FF      [19]  304 	ld	h,-1 (ix)
   50FC 4E            [ 7]  305 	ld	c, (hl)
   50FD 06 00         [ 7]  306 	ld	b, #0x00
   50FF D5            [11]  307 	push	de
   5100 F5            [11]  308 	push	af
   5101 33            [ 6]  309 	inc	sp
   5102 FD E5         [15]  310 	push	iy
   5104 C5            [11]  311 	push	bc
   5105 CD 5D 47      [17]  312 	call	_collision_clamp_y_at
   5108 F1            [10]  313 	pop	af
   5109 F1            [10]  314 	pop	af
   510A 33            [ 6]  315 	inc	sp
   510B D1            [10]  316 	pop	de
                            317 ;src/entities/enemy.c:57: enemy->y = (u8)nexty;
   510C 4D            [ 4]  318 	ld	c, l
   510D DD 6E FC      [19]  319 	ld	l,-4 (ix)
   5110 DD 66 FD      [19]  320 	ld	h,-3 (ix)
   5113 71            [ 7]  321 	ld	(hl), c
                            322 ;src/entities/enemy.c:58: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5114 E1            [10]  323 	pop	hl
   5115 E5            [11]  324 	push	hl
   5116 7E            [ 7]  325 	ld	a, (hl)
   5117 06 00         [ 7]  326 	ld	b, #0x00
   5119 DD 6E FE      [19]  327 	ld	l,-2 (ix)
   511C DD 66 FF      [19]  328 	ld	h,-1 (ix)
   511F 6E            [ 7]  329 	ld	l, (hl)
   5120 DD 75 FA      [19]  330 	ld	-6 (ix), l
   5123 DD 36 FB 00   [19]  331 	ld	-5 (ix), #0x00
   5127 D5            [11]  332 	push	de
   5128 F5            [11]  333 	push	af
   5129 33            [ 6]  334 	inc	sp
   512A C5            [11]  335 	push	bc
   512B DD 6E FA      [19]  336 	ld	l,-6 (ix)
   512E DD 66 FB      [19]  337 	ld	h,-5 (ix)
   5131 E5            [11]  338 	push	hl
   5132 CD DE 46      [17]  339 	call	_collision_is_on_ground_at
   5135 F1            [10]  340 	pop	af
   5136 F1            [10]  341 	pop	af
   5137 33            [ 6]  342 	inc	sp
   5138 D1            [10]  343 	pop	de
   5139 7D            [ 4]  344 	ld	a, l
   513A B7            [ 4]  345 	or	a, a
   513B 28 0E         [12]  346 	jr	Z,00113$
   513D 1A            [ 7]  347 	ld	a, (de)
   513E 4F            [ 4]  348 	ld	c, a
   513F AF            [ 4]  349 	xor	a, a
   5140 91            [ 4]  350 	sub	a, c
   5141 E2 46 51      [10]  351 	jp	PO, 00141$
   5144 EE 80         [ 7]  352 	xor	a, #0x80
   5146                     353 00141$:
   5146 F2 4B 51      [10]  354 	jp	P, 00113$
                            355 ;src/entities/enemy.c:59: enemy->vy = 0;
   5149 AF            [ 4]  356 	xor	a, a
   514A 12            [ 7]  357 	ld	(de), a
   514B                     358 00113$:
   514B DD F9         [10]  359 	ld	sp, ix
   514D DD E1         [14]  360 	pop	ix
   514F C9            [10]  361 	ret
                            362 ;src/entities/enemy.c:63: void enemyrender(const Enemy* enemy) {
                            363 ;	---------------------------------
                            364 ; Function enemyrender
                            365 ; ---------------------------------
   5150                     366 _enemyrender::
   5150 DD E5         [15]  367 	push	ix
   5152 DD 21 00 00   [14]  368 	ld	ix,#0
   5156 DD 39         [15]  369 	add	ix,sp
                            370 ;src/entities/enemy.c:66: if (!enemy || !enemy->active) {
   5158 DD 7E 05      [19]  371 	ld	a, 5 (ix)
   515B DD B6 04      [19]  372 	or	a,4 (ix)
   515E 28 3C         [12]  373 	jr	Z,00104$
   5160 DD 4E 04      [19]  374 	ld	c,4 (ix)
   5163 DD 46 05      [19]  375 	ld	b,5 (ix)
   5166 C5            [11]  376 	push	bc
   5167 FD E1         [14]  377 	pop	iy
   5169 FD 7E 06      [19]  378 	ld	a, 6 (iy)
   516C B7            [ 4]  379 	or	a, a
                            380 ;src/entities/enemy.c:67: return;
   516D 28 2D         [12]  381 	jr	Z,00104$
                            382 ;src/entities/enemy.c:70: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   516F 69            [ 4]  383 	ld	l, c
   5170 60            [ 4]  384 	ld	h, b
   5171 23            [ 6]  385 	inc	hl
   5172 56            [ 7]  386 	ld	d, (hl)
   5173 0A            [ 7]  387 	ld	a, (bc)
   5174 C5            [11]  388 	push	bc
   5175 5F            [ 4]  389 	ld	e, a
   5176 D5            [11]  390 	push	de
   5177 21 00 C0      [10]  391 	ld	hl, #0xc000
   517A E5            [11]  392 	push	hl
   517B CD D5 59      [17]  393 	call	_cpct_getScreenPtr
   517E EB            [ 4]  394 	ex	de,hl
   517F C1            [10]  395 	pop	bc
                            396 ;src/entities/enemy.c:71: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
   5180 C5            [11]  397 	push	bc
   5181 FD E1         [14]  398 	pop	iy
   5183 FD 7E 05      [19]  399 	ld	a, 5 (iy)
   5186 69            [ 4]  400 	ld	l, c
   5187 60            [ 4]  401 	ld	h, b
   5188 01 04 00      [10]  402 	ld	bc, #0x0004
   518B 09            [11]  403 	add	hl, bc
   518C 46            [ 7]  404 	ld	b, (hl)
   518D F5            [11]  405 	push	af
   518E 33            [ 6]  406 	inc	sp
   518F C5            [11]  407 	push	bc
   5190 33            [ 6]  408 	inc	sp
   5191 3E 5C         [ 7]  409 	ld	a, #0x5c
   5193 F5            [11]  410 	push	af
   5194 33            [ 6]  411 	inc	sp
   5195 D5            [11]  412 	push	de
   5196 CD 1C 59      [17]  413 	call	_cpct_drawSolidBox
   5199 F1            [10]  414 	pop	af
   519A F1            [10]  415 	pop	af
   519B 33            [ 6]  416 	inc	sp
   519C                     417 00104$:
   519C DD E1         [14]  418 	pop	ix
   519E C9            [10]  419 	ret
                            420 ;src/entities/enemy.c:74: u8 enemydamage(Enemy* enemy, u8 damage) {
                            421 ;	---------------------------------
                            422 ; Function enemydamage
                            423 ; ---------------------------------
   519F                     424 _enemydamage::
   519F DD E5         [15]  425 	push	ix
   51A1 DD 21 00 00   [14]  426 	ld	ix,#0
   51A5 DD 39         [15]  427 	add	ix,sp
                            428 ;src/entities/enemy.c:75: if (!enemy || !enemy->active) {
   51A7 DD 7E 05      [19]  429 	ld	a, 5 (ix)
   51AA DD B6 04      [19]  430 	or	a,4 (ix)
   51AD 28 0F         [12]  431 	jr	Z,00101$
   51AF DD 4E 04      [19]  432 	ld	c,4 (ix)
   51B2 DD 46 05      [19]  433 	ld	b,5 (ix)
   51B5 21 06 00      [10]  434 	ld	hl, #0x0006
   51B8 09            [11]  435 	add	hl,bc
   51B9 EB            [ 4]  436 	ex	de,hl
   51BA 1A            [ 7]  437 	ld	a, (de)
   51BB B7            [ 4]  438 	or	a, a
   51BC 20 04         [12]  439 	jr	NZ,00102$
   51BE                     440 00101$:
                            441 ;src/entities/enemy.c:76: return 0;
   51BE 2E 00         [ 7]  442 	ld	l, #0x00
   51C0 18 1A         [12]  443 	jr	00106$
   51C2                     444 00102$:
                            445 ;src/entities/enemy.c:79: if (damage >= enemy->health) {
   51C2 21 07 00      [10]  446 	ld	hl, #0x0007
   51C5 09            [11]  447 	add	hl, bc
   51C6 4E            [ 7]  448 	ld	c, (hl)
   51C7 DD 7E 06      [19]  449 	ld	a, 6 (ix)
   51CA 91            [ 4]  450 	sub	a, c
   51CB 38 08         [12]  451 	jr	C,00105$
                            452 ;src/entities/enemy.c:80: enemy->health = 0;
   51CD 36 00         [10]  453 	ld	(hl), #0x00
                            454 ;src/entities/enemy.c:81: enemy->active = 0;
   51CF AF            [ 4]  455 	xor	a, a
   51D0 12            [ 7]  456 	ld	(de), a
                            457 ;src/entities/enemy.c:82: return 1;
   51D1 2E 01         [ 7]  458 	ld	l, #0x01
   51D3 18 07         [12]  459 	jr	00106$
   51D5                     460 00105$:
                            461 ;src/entities/enemy.c:85: enemy->health = (u8)(enemy->health - damage);
   51D5 79            [ 4]  462 	ld	a, c
   51D6 DD 96 06      [19]  463 	sub	a, 6 (ix)
   51D9 77            [ 7]  464 	ld	(hl), a
                            465 ;src/entities/enemy.c:86: return 0;
   51DA 2E 00         [ 7]  466 	ld	l, #0x00
   51DC                     467 00106$:
   51DC DD E1         [14]  468 	pop	ix
   51DE C9            [10]  469 	ret
                            470 	.area _CODE
                            471 	.area _INITIALIZER
                            472 	.area _CABS (ABS)
