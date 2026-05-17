                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module projectile
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSprite
                             13 	.globl _projectileinit
                             14 	.globl _projectilefire
                             15 	.globl _projectileupdate
                             16 	.globl _projectilerender
                             17 ;--------------------------------------------------------
                             18 ; special function registers
                             19 ;--------------------------------------------------------
                             20 ;--------------------------------------------------------
                             21 ; ram data
                             22 ;--------------------------------------------------------
                             23 	.area _DATA
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _INITIALIZED
                             28 ;--------------------------------------------------------
                             29 ; absolute external ram data
                             30 ;--------------------------------------------------------
                             31 	.area _DABS (ABS)
                             32 ;--------------------------------------------------------
                             33 ; global & static initialisations
                             34 ;--------------------------------------------------------
                             35 	.area _HOME
                             36 	.area _GSINIT
                             37 	.area _GSFINAL
                             38 	.area _GSINIT
                             39 ;--------------------------------------------------------
                             40 ; Home
                             41 ;--------------------------------------------------------
                             42 	.area _HOME
                             43 	.area _HOME
                             44 ;--------------------------------------------------------
                             45 ; code
                             46 ;--------------------------------------------------------
                             47 	.area _CODE
                             48 ;src/entities/projectile.c:17: void projectileinit(Projectile* projectile) {
                             49 ;	---------------------------------
                             50 ; Function projectileinit
                             51 ; ---------------------------------
   628F                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   628F 21 03 00      [10]   54 	ld	hl, #2+1
   6292 39            [11]   55 	add	hl, sp
   6293 7E            [ 7]   56 	ld	a, (hl)
   6294 2B            [ 6]   57 	dec	hl
   6295 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   6296 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   6297 D1            [10]   62 	pop	de
   6298 C1            [10]   63 	pop	bc
   6299 C5            [11]   64 	push	bc
   629A D5            [11]   65 	push	de
   629B AF            [ 4]   66 	xor	a, a
   629C 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   629D 59            [ 4]   69 	ld	e, c
   629E 50            [ 4]   70 	ld	d, b
   629F 13            [ 6]   71 	inc	de
   62A0 AF            [ 4]   72 	xor	a, a
   62A1 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   62A2 59            [ 4]   75 	ld	e, c
   62A3 50            [ 4]   76 	ld	d, b
   62A4 13            [ 6]   77 	inc	de
   62A5 13            [ 6]   78 	inc	de
   62A6 AF            [ 4]   79 	xor	a, a
   62A7 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   62A8 59            [ 4]   82 	ld	e, c
   62A9 50            [ 4]   83 	ld	d, b
   62AA 13            [ 6]   84 	inc	de
   62AB 13            [ 6]   85 	inc	de
   62AC 13            [ 6]   86 	inc	de
   62AD AF            [ 4]   87 	xor	a, a
   62AE 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   62AF 21 04 00      [10]   90 	ld	hl, #0x0004
   62B2 09            [11]   91 	add	hl, bc
   62B3 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   62B5 21 05 00      [10]   94 	ld	hl, #0x0005
   62B8 09            [11]   95 	add	hl, bc
   62B9 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   62BB 21 06 00      [10]   98 	ld	hl, #0x0006
   62BE 09            [11]   99 	add	hl, bc
   62BF 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   62C1 21 07 00      [10]  102 	ld	hl, #0x0007
   62C4 09            [11]  103 	add	hl, bc
   62C5 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   62C7 21 08 00      [10]  106 	ld	hl, #0x0008
   62CA 09            [11]  107 	add	hl, bc
   62CB 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   62CD 21 09 00      [10]  110 	ld	hl, #0x0009
   62D0 09            [11]  111 	add	hl, bc
   62D1 36 00         [10]  112 	ld	(hl), #0x00
   62D3 C9            [10]  113 	ret
   62D4                     114 _projectile_basic_sprite:
   62D4 FF                  115 	.db #0xff	; 255
   62D5 FF                  116 	.db #0xff	; 255
   62D6 FF                  117 	.db #0xff	; 255
   62D7 FF                  118 	.db #0xff	; 255
   62D8 FF                  119 	.db #0xff	; 255
   62D9 FF                  120 	.db #0xff	; 255
   62DA                     121 _projectile_up_sprite:
   62DA CF                  122 	.db #0xcf	; 207
   62DB CF                  123 	.db #0xcf	; 207
   62DC CF                  124 	.db #0xcf	; 207
   62DD CF                  125 	.db #0xcf	; 207
   62DE CF                  126 	.db #0xcf	; 207
   62DF CF                  127 	.db #0xcf	; 207
   62E0                     128 _projectile_special_sprite:
   62E0 F0                  129 	.db #0xf0	; 240
   62E1 F0                  130 	.db #0xf0	; 240
   62E2 F0                  131 	.db #0xf0	; 240
   62E3 F0                  132 	.db #0xf0	; 240
   62E4 F0                  133 	.db #0xf0	; 240
   62E5 F0                  134 	.db #0xf0	; 240
   62E6 F0                  135 	.db #0xf0	; 240
   62E7 F0                  136 	.db #0xf0	; 240
   62E8 F0                  137 	.db #0xf0	; 240
   62E9 F0                  138 	.db #0xf0	; 240
   62EA F0                  139 	.db #0xf0	; 240
   62EB F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   62EC                     145 _projectilefire::
   62EC DD E5         [15]  146 	push	ix
   62EE DD 21 00 00   [14]  147 	ld	ix,#0
   62F2 DD 39         [15]  148 	add	ix,sp
   62F4 F5            [11]  149 	push	af
   62F5 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   62F6 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   62F9 DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   62FC CA 9E 63      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   62FF DD 4E 04      [19]  157 	ld	c,4 (ix)
   6302 DD 46 05      [19]  158 	ld	b,5 (ix)
   6305 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   6308 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   6309 59            [ 4]  162 	ld	e, c
   630A 50            [ 4]  163 	ld	d, b
   630B 13            [ 6]  164 	inc	de
   630C DD 7E 07      [19]  165 	ld	a, 7 (ix)
   630F 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   6310 21 02 00      [10]  168 	ld	hl, #0x0002
   6313 09            [11]  169 	add	hl,bc
   6314 DD 75 FE      [19]  170 	ld	-2 (ix), l
   6317 DD 74 FF      [19]  171 	ld	-1 (ix), h
   631A DD 7E 08      [19]  172 	ld	a, 8 (ix)
   631D 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   631E 59            [ 4]  175 	ld	e, c
   631F 50            [ 4]  176 	ld	d, b
   6320 13            [ 6]  177 	inc	de
   6321 13            [ 6]  178 	inc	de
   6322 13            [ 6]  179 	inc	de
   6323 AF            [ 4]  180 	xor	a, a
   6324 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   6325 21 09 00      [10]  183 	ld	hl, #0x0009
   6328 09            [11]  184 	add	hl, bc
   6329 DD 7E 09      [19]  185 	ld	a, 9 (ix)
   632C 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   632D 21 06 00      [10]  188 	ld	hl, #0x0006
   6330 09            [11]  189 	add	hl, bc
   6331 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   6333 21 04 00      [10]  192 	ld	hl, #0x0004
   6336 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   6337 79            [ 4]  195 	ld	a, c
   6338 C6 05         [ 7]  196 	add	a, #0x05
   633A 5F            [ 4]  197 	ld	e, a
   633B 78            [ 4]  198 	ld	a, b
   633C CE 00         [ 7]  199 	adc	a, #0x00
   633E 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   633F 79            [ 4]  202 	ld	a, c
   6340 C6 07         [ 7]  203 	add	a, #0x07
   6342 DD 77 FC      [19]  204 	ld	-4 (ix), a
   6345 78            [ 4]  205 	ld	a, b
   6346 CE 00         [ 7]  206 	adc	a, #0x00
   6348 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   634B 79            [ 4]  209 	ld	a, c
   634C C6 08         [ 7]  210 	add	a, #0x08
   634E 4F            [ 4]  211 	ld	c, a
   634F 78            [ 4]  212 	ld	a, b
   6350 CE 00         [ 7]  213 	adc	a, #0x00
   6352 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   6353 DD 7E 09      [19]  216 	ld	a, 9 (ix)
   6356 B7            [ 4]  217 	or	a, a
   6357 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   6359 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   635B 3E 02         [ 7]  222 	ld	a, #0x02
   635D 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   635E E1            [10]  225 	pop	hl
   635F E5            [11]  226 	push	hl
   6360 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   6362 3E 2D         [ 7]  229 	ld	a, #0x2d
   6364 02            [ 7]  230 	ld	(bc), a
   6365 18 37         [12]  231 	jr	00109$
   6367                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   6367 DD 7E 09      [19]  234 	ld	a, 9 (ix)
   636A 3D            [ 4]  235 	dec	a
   636B 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   636D 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   636F 3E 03         [ 7]  240 	ld	a, #0x03
   6371 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   6372 E1            [10]  243 	pop	hl
   6373 E5            [11]  244 	push	hl
   6374 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   6376 3E 1C         [ 7]  247 	ld	a, #0x1c
   6378 02            [ 7]  248 	ld	(bc), a
   6379 18 23         [12]  249 	jr	00109$
   637B                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   637B 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   637D 3E 03         [ 7]  254 	ld	a, #0x03
   637F 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   6380 E1            [10]  257 	pop	hl
   6381 E5            [11]  258 	push	hl
   6382 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   6384 3E 38         [ 7]  261 	ld	a, #0x38
   6386 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   6387 D1            [10]  264 	pop	de
   6388 C1            [10]  265 	pop	bc
   6389 C5            [11]  266 	push	bc
   638A D5            [11]  267 	push	de
   638B AF            [ 4]  268 	xor	a, a
   638C DD 96 08      [19]  269 	sub	a, 8 (ix)
   638F E2 94 63      [10]  270 	jp	PO, 00131$
   6392 EE 80         [ 7]  271 	xor	a, #0x80
   6394                     272 00131$:
   6394 F2 9B 63      [10]  273 	jp	P, 00111$
   6397 3E 04         [ 7]  274 	ld	a, #0x04
   6399 18 02         [12]  275 	jr	00112$
   639B                     276 00111$:
   639B 3E FC         [ 7]  277 	ld	a, #0xfc
   639D                     278 00112$:
   639D 02            [ 7]  279 	ld	(bc), a
   639E                     280 00109$:
   639E DD F9         [10]  281 	ld	sp, ix
   63A0 DD E1         [14]  282 	pop	ix
   63A2 C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   63A3                     288 _projectileupdate::
   63A3 DD E5         [15]  289 	push	ix
   63A5 DD 21 00 00   [14]  290 	ld	ix,#0
   63A9 DD 39         [15]  291 	add	ix,sp
   63AB 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   63AC DD 7E 05      [19]  294 	ld	a, 5 (ix)
   63AF DD B6 04      [19]  295 	or	a,4 (ix)
   63B2 28 4A         [12]  296 	jr	Z,00109$
   63B4 DD 5E 04      [19]  297 	ld	e,4 (ix)
   63B7 DD 56 05      [19]  298 	ld	d,5 (ix)
   63BA FD 21 06 00   [14]  299 	ld	iy, #0x0006
   63BE FD 19         [15]  300 	add	iy, de
   63C0 FD 7E 00      [19]  301 	ld	a, 0 (iy)
   63C3 B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   63C4 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   63C6 1A            [ 7]  306 	ld	a, (de)
   63C7 4F            [ 4]  307 	ld	c, a
   63C8 6B            [ 4]  308 	ld	l, e
   63C9 62            [ 4]  309 	ld	h, d
   63CA 23            [ 6]  310 	inc	hl
   63CB 23            [ 6]  311 	inc	hl
   63CC 6E            [ 7]  312 	ld	l, (hl)
   63CD 09            [11]  313 	add	hl, bc
   63CE 7D            [ 4]  314 	ld	a, l
   63CF 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   63D0 4B            [ 4]  317 	ld	c, e
   63D1 42            [ 4]  318 	ld	b, d
   63D2 03            [ 6]  319 	inc	bc
   63D3 0A            [ 7]  320 	ld	a, (bc)
   63D4 DD 77 FF      [19]  321 	ld	-1 (ix), a
   63D7 6B            [ 4]  322 	ld	l, e
   63D8 62            [ 4]  323 	ld	h, d
   63D9 23            [ 6]  324 	inc	hl
   63DA 23            [ 6]  325 	inc	hl
   63DB 23            [ 6]  326 	inc	hl
   63DC 6E            [ 7]  327 	ld	l, (hl)
   63DD DD 7E FF      [19]  328 	ld	a, -1 (ix)
   63E0 85            [ 4]  329 	add	a, l
   63E1 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   63E2 21 08 00      [10]  332 	ld	hl, #0x0008
   63E5 19            [11]  333 	add	hl,de
   63E6 4D            [ 4]  334 	ld	c, l
   63E7 44            [ 4]  335 	ld	b, h
   63E8 0A            [ 7]  336 	ld	a, (bc)
   63E9 B7            [ 4]  337 	or	a, a
   63EA 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   63EC C6 FF         [ 7]  340 	add	a, #0xff
   63EE 02            [ 7]  341 	ld	(bc), a
   63EF                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   63EF 1A            [ 7]  344 	ld	a, (de)
   63F0 5F            [ 4]  345 	ld	e, a
   63F1 3E 4E         [ 7]  346 	ld	a, #0x4e
   63F3 93            [ 4]  347 	sub	a, e
   63F4 38 04         [12]  348 	jr	C,00106$
   63F6 0A            [ 7]  349 	ld	a, (bc)
   63F7 B7            [ 4]  350 	or	a, a
   63F8 20 04         [12]  351 	jr	NZ,00109$
   63FA                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   63FA FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   63FE                     355 00109$:
   63FE 33            [ 6]  356 	inc	sp
   63FF DD E1         [14]  357 	pop	ix
   6401 C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   6402                     363 _projectilerender::
   6402 DD E5         [15]  364 	push	ix
   6404 DD 21 00 00   [14]  365 	ld	ix,#0
   6408 DD 39         [15]  366 	add	ix,sp
   640A F5            [11]  367 	push	af
   640B 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   640C DD 7E 05      [19]  370 	ld	a, 5 (ix)
   640F DD B6 04      [19]  371 	or	a,4 (ix)
   6412 28 6B         [12]  372 	jr	Z,00110$
   6414 DD 4E 04      [19]  373 	ld	c,4 (ix)
   6417 DD 46 05      [19]  374 	ld	b,5 (ix)
   641A C5            [11]  375 	push	bc
   641B FD E1         [14]  376 	pop	iy
   641D FD 7E 06      [19]  377 	ld	a, 6 (iy)
   6420 B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   6421 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   6423 C5            [11]  382 	push	bc
   6424 FD E1         [14]  383 	pop	iy
   6426 FD 7E 09      [19]  384 	ld	a, 9 (iy)
   6429 B7            [ 4]  385 	or	a, a
   642A 20 0A         [12]  386 	jr	NZ,00108$
   642C DD 36 FE D4   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   6430 DD 36 FF 62   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   6434 18 15         [12]  389 	jr	00109$
   6436                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   6436 3D            [ 4]  392 	dec	a
   6437 20 0A         [12]  393 	jr	NZ,00105$
   6439 DD 36 FE DA   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   643D DD 36 FF 62   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   6441 18 08         [12]  396 	jr	00109$
   6443                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   6443 DD 36 FE E0   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   6447 DD 36 FF 62   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   644B                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   644B 69            [ 4]  403 	ld	l, c
   644C 60            [ 4]  404 	ld	h, b
   644D 23            [ 6]  405 	inc	hl
   644E 56            [ 7]  406 	ld	d, (hl)
   644F 0A            [ 7]  407 	ld	a, (bc)
   6450 C5            [11]  408 	push	bc
   6451 5F            [ 4]  409 	ld	e, a
   6452 D5            [11]  410 	push	de
   6453 21 00 C0      [10]  411 	ld	hl, #0xc000
   6456 E5            [11]  412 	push	hl
   6457 CD 2D 67      [17]  413 	call	_cpct_getScreenPtr
   645A EB            [ 4]  414 	ex	de,hl
   645B C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   645C C5            [11]  417 	push	bc
   645D FD E1         [14]  418 	pop	iy
   645F FD 7E 05      [19]  419 	ld	a, 5 (iy)
   6462 DD 77 FD      [19]  420 	ld	-3 (ix), a
   6465 69            [ 4]  421 	ld	l, c
   6466 60            [ 4]  422 	ld	h, b
   6467 01 04 00      [10]  423 	ld	bc, #0x0004
   646A 09            [11]  424 	add	hl, bc
   646B 4E            [ 7]  425 	ld	c, (hl)
   646C D5            [11]  426 	push	de
   646D FD E1         [14]  427 	pop	iy
   646F DD 5E FE      [19]  428 	ld	e,-2 (ix)
   6472 DD 56 FF      [19]  429 	ld	d,-1 (ix)
   6475 DD 46 FD      [19]  430 	ld	b, -3 (ix)
   6478 C5            [11]  431 	push	bc
   6479 FD E5         [15]  432 	push	iy
   647B D5            [11]  433 	push	de
   647C CD 5E 65      [17]  434 	call	_cpct_drawSprite
   647F                     435 00110$:
   647F DD F9         [10]  436 	ld	sp, ix
   6481 DD E1         [14]  437 	pop	ix
   6483 C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
