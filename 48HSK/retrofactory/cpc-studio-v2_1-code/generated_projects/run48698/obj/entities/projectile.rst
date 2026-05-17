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
   6231                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   6231 21 03 00      [10]   54 	ld	hl, #2+1
   6234 39            [11]   55 	add	hl, sp
   6235 7E            [ 7]   56 	ld	a, (hl)
   6236 2B            [ 6]   57 	dec	hl
   6237 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   6238 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   6239 D1            [10]   62 	pop	de
   623A C1            [10]   63 	pop	bc
   623B C5            [11]   64 	push	bc
   623C D5            [11]   65 	push	de
   623D AF            [ 4]   66 	xor	a, a
   623E 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   623F 59            [ 4]   69 	ld	e, c
   6240 50            [ 4]   70 	ld	d, b
   6241 13            [ 6]   71 	inc	de
   6242 AF            [ 4]   72 	xor	a, a
   6243 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   6244 59            [ 4]   75 	ld	e, c
   6245 50            [ 4]   76 	ld	d, b
   6246 13            [ 6]   77 	inc	de
   6247 13            [ 6]   78 	inc	de
   6248 AF            [ 4]   79 	xor	a, a
   6249 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   624A 59            [ 4]   82 	ld	e, c
   624B 50            [ 4]   83 	ld	d, b
   624C 13            [ 6]   84 	inc	de
   624D 13            [ 6]   85 	inc	de
   624E 13            [ 6]   86 	inc	de
   624F AF            [ 4]   87 	xor	a, a
   6250 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   6251 21 04 00      [10]   90 	ld	hl, #0x0004
   6254 09            [11]   91 	add	hl, bc
   6255 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   6257 21 05 00      [10]   94 	ld	hl, #0x0005
   625A 09            [11]   95 	add	hl, bc
   625B 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   625D 21 06 00      [10]   98 	ld	hl, #0x0006
   6260 09            [11]   99 	add	hl, bc
   6261 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   6263 21 07 00      [10]  102 	ld	hl, #0x0007
   6266 09            [11]  103 	add	hl, bc
   6267 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   6269 21 08 00      [10]  106 	ld	hl, #0x0008
   626C 09            [11]  107 	add	hl, bc
   626D 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   626F 21 09 00      [10]  110 	ld	hl, #0x0009
   6272 09            [11]  111 	add	hl, bc
   6273 36 00         [10]  112 	ld	(hl), #0x00
   6275 C9            [10]  113 	ret
   6276                     114 _projectile_basic_sprite:
   6276 3C                  115 	.db #0x3c	; 60
   6277 3C                  116 	.db #0x3c	; 60
   6278 3C                  117 	.db #0x3c	; 60
   6279 3C                  118 	.db #0x3c	; 60
   627A 3C                  119 	.db #0x3c	; 60
   627B 3C                  120 	.db #0x3c	; 60
   627C                     121 _projectile_up_sprite:
   627C C3                  122 	.db #0xc3	; 195
   627D C3                  123 	.db #0xc3	; 195
   627E C3                  124 	.db #0xc3	; 195
   627F C3                  125 	.db #0xc3	; 195
   6280 C3                  126 	.db #0xc3	; 195
   6281 C3                  127 	.db #0xc3	; 195
   6282                     128 _projectile_special_sprite:
   6282 FF                  129 	.db #0xff	; 255
   6283 FF                  130 	.db #0xff	; 255
   6284 FF                  131 	.db #0xff	; 255
   6285 FF                  132 	.db #0xff	; 255
   6286 FF                  133 	.db #0xff	; 255
   6287 FF                  134 	.db #0xff	; 255
   6288 FF                  135 	.db #0xff	; 255
   6289 FF                  136 	.db #0xff	; 255
   628A FF                  137 	.db #0xff	; 255
   628B FF                  138 	.db #0xff	; 255
   628C FF                  139 	.db #0xff	; 255
   628D FF                  140 	.db #0xff	; 255
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   628E                     145 _projectilefire::
   628E DD E5         [15]  146 	push	ix
   6290 DD 21 00 00   [14]  147 	ld	ix,#0
   6294 DD 39         [15]  148 	add	ix,sp
   6296 F5            [11]  149 	push	af
   6297 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   6298 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   629B DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   629E CA 47 63      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   62A1 DD 4E 04      [19]  157 	ld	c,4 (ix)
   62A4 DD 46 05      [19]  158 	ld	b,5 (ix)
   62A7 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   62AA 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   62AB 59            [ 4]  162 	ld	e, c
   62AC 50            [ 4]  163 	ld	d, b
   62AD 13            [ 6]  164 	inc	de
   62AE DD 7E 07      [19]  165 	ld	a, 7 (ix)
   62B1 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   62B2 21 02 00      [10]  168 	ld	hl, #0x0002
   62B5 09            [11]  169 	add	hl,bc
   62B6 E3            [19]  170 	ex	(sp), hl
   62B7 E1            [10]  171 	pop	hl
   62B8 E5            [11]  172 	push	hl
   62B9 DD 7E 08      [19]  173 	ld	a, 8 (ix)
   62BC 77            [ 7]  174 	ld	(hl), a
                            175 ;src/entities/projectile.c:42: projectile->vy = 0;
   62BD 59            [ 4]  176 	ld	e, c
   62BE 50            [ 4]  177 	ld	d, b
   62BF 13            [ 6]  178 	inc	de
   62C0 13            [ 6]  179 	inc	de
   62C1 13            [ 6]  180 	inc	de
   62C2 AF            [ 4]  181 	xor	a, a
   62C3 12            [ 7]  182 	ld	(de), a
                            183 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   62C4 21 09 00      [10]  184 	ld	hl, #0x0009
   62C7 09            [11]  185 	add	hl, bc
   62C8 DD 7E 09      [19]  186 	ld	a, 9 (ix)
   62CB 77            [ 7]  187 	ld	(hl), a
                            188 ;src/entities/projectile.c:44: projectile->active = 1;
   62CC 21 06 00      [10]  189 	ld	hl, #0x0006
   62CF 09            [11]  190 	add	hl, bc
   62D0 36 01         [10]  191 	ld	(hl), #0x01
                            192 ;src/entities/projectile.c:47: projectile->w = 3;
   62D2 21 04 00      [10]  193 	ld	hl, #0x0004
   62D5 09            [11]  194 	add	hl, bc
                            195 ;src/entities/projectile.c:48: projectile->h = 2;
   62D6 79            [ 4]  196 	ld	a, c
   62D7 C6 05         [ 7]  197 	add	a, #0x05
   62D9 5F            [ 4]  198 	ld	e, a
   62DA 78            [ 4]  199 	ld	a, b
   62DB CE 00         [ 7]  200 	adc	a, #0x00
   62DD 57            [ 4]  201 	ld	d, a
                            202 ;src/entities/projectile.c:49: projectile->damage = 1;
   62DE 79            [ 4]  203 	ld	a, c
   62DF C6 07         [ 7]  204 	add	a, #0x07
   62E1 DD 77 FE      [19]  205 	ld	-2 (ix), a
   62E4 78            [ 4]  206 	ld	a, b
   62E5 CE 00         [ 7]  207 	adc	a, #0x00
   62E7 DD 77 FF      [19]  208 	ld	-1 (ix), a
                            209 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   62EA 79            [ 4]  210 	ld	a, c
   62EB C6 08         [ 7]  211 	add	a, #0x08
   62ED 4F            [ 4]  212 	ld	c, a
   62EE 78            [ 4]  213 	ld	a, b
   62EF CE 00         [ 7]  214 	adc	a, #0x00
   62F1 47            [ 4]  215 	ld	b, a
                            216 ;src/entities/projectile.c:46: if (weapon == 0) {
   62F2 DD 7E 09      [19]  217 	ld	a, 9 (ix)
   62F5 B7            [ 4]  218 	or	a, a
   62F6 20 12         [12]  219 	jr	NZ,00107$
                            220 ;src/entities/projectile.c:47: projectile->w = 3;
   62F8 36 03         [10]  221 	ld	(hl), #0x03
                            222 ;src/entities/projectile.c:48: projectile->h = 2;
   62FA 3E 02         [ 7]  223 	ld	a, #0x02
   62FC 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/projectile.c:49: projectile->damage = 1;
   62FD DD 6E FE      [19]  226 	ld	l,-2 (ix)
   6300 DD 66 FF      [19]  227 	ld	h,-1 (ix)
   6303 36 01         [10]  228 	ld	(hl), #0x01
                            229 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   6305 3E 2D         [ 7]  230 	ld	a, #0x2d
   6307 02            [ 7]  231 	ld	(bc), a
   6308 18 3D         [12]  232 	jr	00109$
   630A                     233 00107$:
                            234 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   630A DD 7E 09      [19]  235 	ld	a, 9 (ix)
   630D 3D            [ 4]  236 	dec	a
   630E 20 12         [12]  237 	jr	NZ,00104$
                            238 ;src/entities/projectile.c:52: projectile->w = 2;
   6310 36 02         [10]  239 	ld	(hl), #0x02
                            240 ;src/entities/projectile.c:53: projectile->h = 3;
   6312 3E 03         [ 7]  241 	ld	a, #0x03
   6314 12            [ 7]  242 	ld	(de), a
                            243 ;src/entities/projectile.c:54: projectile->damage = 2;
   6315 DD 6E FE      [19]  244 	ld	l,-2 (ix)
   6318 DD 66 FF      [19]  245 	ld	h,-1 (ix)
   631B 36 02         [10]  246 	ld	(hl), #0x02
                            247 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   631D 3E 1C         [ 7]  248 	ld	a, #0x1c
   631F 02            [ 7]  249 	ld	(bc), a
   6320 18 25         [12]  250 	jr	00109$
   6322                     251 00104$:
                            252 ;src/entities/projectile.c:57: projectile->w = 4;
   6322 36 04         [10]  253 	ld	(hl), #0x04
                            254 ;src/entities/projectile.c:58: projectile->h = 3;
   6324 3E 03         [ 7]  255 	ld	a, #0x03
   6326 12            [ 7]  256 	ld	(de), a
                            257 ;src/entities/projectile.c:59: projectile->damage = 3;
   6327 DD 6E FE      [19]  258 	ld	l,-2 (ix)
   632A DD 66 FF      [19]  259 	ld	h,-1 (ix)
   632D 36 03         [10]  260 	ld	(hl), #0x03
                            261 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   632F 3E 38         [ 7]  262 	ld	a, #0x38
   6331 02            [ 7]  263 	ld	(bc), a
                            264 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   6332 C1            [10]  265 	pop	bc
   6333 C5            [11]  266 	push	bc
   6334 AF            [ 4]  267 	xor	a, a
   6335 DD 96 08      [19]  268 	sub	a, 8 (ix)
   6338 E2 3D 63      [10]  269 	jp	PO, 00131$
   633B EE 80         [ 7]  270 	xor	a, #0x80
   633D                     271 00131$:
   633D F2 44 63      [10]  272 	jp	P, 00111$
   6340 3E 04         [ 7]  273 	ld	a, #0x04
   6342 18 02         [12]  274 	jr	00112$
   6344                     275 00111$:
   6344 3E FC         [ 7]  276 	ld	a, #0xfc
   6346                     277 00112$:
   6346 02            [ 7]  278 	ld	(bc), a
   6347                     279 00109$:
   6347 DD F9         [10]  280 	ld	sp, ix
   6349 DD E1         [14]  281 	pop	ix
   634B C9            [10]  282 	ret
                            283 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            284 ;	---------------------------------
                            285 ; Function projectileupdate
                            286 ; ---------------------------------
   634C                     287 _projectileupdate::
   634C DD E5         [15]  288 	push	ix
   634E DD 21 00 00   [14]  289 	ld	ix,#0
   6352 DD 39         [15]  290 	add	ix,sp
   6354 3B            [ 6]  291 	dec	sp
                            292 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   6355 DD 7E 05      [19]  293 	ld	a, 5 (ix)
   6358 DD B6 04      [19]  294 	or	a,4 (ix)
   635B 28 4A         [12]  295 	jr	Z,00109$
   635D DD 5E 04      [19]  296 	ld	e,4 (ix)
   6360 DD 56 05      [19]  297 	ld	d,5 (ix)
   6363 FD 21 06 00   [14]  298 	ld	iy, #0x0006
   6367 FD 19         [15]  299 	add	iy, de
   6369 FD 7E 00      [19]  300 	ld	a, 0 (iy)
   636C B7            [ 4]  301 	or	a, a
                            302 ;src/entities/projectile.c:67: return;
   636D 28 38         [12]  303 	jr	Z,00109$
                            304 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   636F 1A            [ 7]  305 	ld	a, (de)
   6370 4F            [ 4]  306 	ld	c, a
   6371 6B            [ 4]  307 	ld	l, e
   6372 62            [ 4]  308 	ld	h, d
   6373 23            [ 6]  309 	inc	hl
   6374 23            [ 6]  310 	inc	hl
   6375 6E            [ 7]  311 	ld	l, (hl)
   6376 09            [11]  312 	add	hl, bc
   6377 7D            [ 4]  313 	ld	a, l
   6378 12            [ 7]  314 	ld	(de), a
                            315 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   6379 4B            [ 4]  316 	ld	c, e
   637A 42            [ 4]  317 	ld	b, d
   637B 03            [ 6]  318 	inc	bc
   637C 0A            [ 7]  319 	ld	a, (bc)
   637D DD 77 FF      [19]  320 	ld	-1 (ix), a
   6380 6B            [ 4]  321 	ld	l, e
   6381 62            [ 4]  322 	ld	h, d
   6382 23            [ 6]  323 	inc	hl
   6383 23            [ 6]  324 	inc	hl
   6384 23            [ 6]  325 	inc	hl
   6385 6E            [ 7]  326 	ld	l, (hl)
   6386 DD 7E FF      [19]  327 	ld	a, -1 (ix)
   6389 85            [ 4]  328 	add	a, l
   638A 02            [ 7]  329 	ld	(bc), a
                            330 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   638B 21 08 00      [10]  331 	ld	hl, #0x0008
   638E 19            [11]  332 	add	hl,de
   638F 4D            [ 4]  333 	ld	c, l
   6390 44            [ 4]  334 	ld	b, h
   6391 0A            [ 7]  335 	ld	a, (bc)
   6392 B7            [ 4]  336 	or	a, a
   6393 28 03         [12]  337 	jr	Z,00105$
                            338 ;src/entities/projectile.c:74: projectile->lifetime--;
   6395 C6 FF         [ 7]  339 	add	a, #0xff
   6397 02            [ 7]  340 	ld	(bc), a
   6398                     341 00105$:
                            342 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   6398 1A            [ 7]  343 	ld	a, (de)
   6399 5F            [ 4]  344 	ld	e, a
   639A 3E 4E         [ 7]  345 	ld	a, #0x4e
   639C 93            [ 4]  346 	sub	a, e
   639D 38 04         [12]  347 	jr	C,00106$
   639F 0A            [ 7]  348 	ld	a, (bc)
   63A0 B7            [ 4]  349 	or	a, a
   63A1 20 04         [12]  350 	jr	NZ,00109$
   63A3                     351 00106$:
                            352 ;src/entities/projectile.c:78: projectile->active = 0;
   63A3 FD 36 00 00   [19]  353 	ld	0 (iy), #0x00
   63A7                     354 00109$:
   63A7 33            [ 6]  355 	inc	sp
   63A8 DD E1         [14]  356 	pop	ix
   63AA C9            [10]  357 	ret
                            358 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            359 ;	---------------------------------
                            360 ; Function projectilerender
                            361 ; ---------------------------------
   63AB                     362 _projectilerender::
   63AB DD E5         [15]  363 	push	ix
   63AD DD 21 00 00   [14]  364 	ld	ix,#0
   63B1 DD 39         [15]  365 	add	ix,sp
   63B3 F5            [11]  366 	push	af
   63B4 3B            [ 6]  367 	dec	sp
                            368 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   63B5 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   63B8 DD B6 04      [19]  370 	or	a,4 (ix)
   63BB 28 6B         [12]  371 	jr	Z,00110$
   63BD DD 4E 04      [19]  372 	ld	c,4 (ix)
   63C0 DD 46 05      [19]  373 	ld	b,5 (ix)
   63C3 C5            [11]  374 	push	bc
   63C4 FD E1         [14]  375 	pop	iy
   63C6 FD 7E 06      [19]  376 	ld	a, 6 (iy)
   63C9 B7            [ 4]  377 	or	a, a
                            378 ;src/entities/projectile.c:87: return;
   63CA 28 5C         [12]  379 	jr	Z,00110$
                            380 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   63CC C5            [11]  381 	push	bc
   63CD FD E1         [14]  382 	pop	iy
   63CF FD 7E 09      [19]  383 	ld	a, 9 (iy)
   63D2 B7            [ 4]  384 	or	a, a
   63D3 20 0A         [12]  385 	jr	NZ,00108$
   63D5 DD 36 FE 76   [19]  386 	ld	-2 (ix), #<(_projectile_basic_sprite)
   63D9 DD 36 FF 62   [19]  387 	ld	-1 (ix), #>(_projectile_basic_sprite)
   63DD 18 15         [12]  388 	jr	00109$
   63DF                     389 00108$:
                            390 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   63DF 3D            [ 4]  391 	dec	a
   63E0 20 0A         [12]  392 	jr	NZ,00105$
   63E2 DD 36 FE 7C   [19]  393 	ld	-2 (ix), #<(_projectile_up_sprite)
   63E6 DD 36 FF 62   [19]  394 	ld	-1 (ix), #>(_projectile_up_sprite)
   63EA 18 08         [12]  395 	jr	00109$
   63EC                     396 00105$:
                            397 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   63EC DD 36 FE 82   [19]  398 	ld	-2 (ix), #<(_projectile_special_sprite)
   63F0 DD 36 FF 62   [19]  399 	ld	-1 (ix), #>(_projectile_special_sprite)
   63F4                     400 00109$:
                            401 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   63F4 69            [ 4]  402 	ld	l, c
   63F5 60            [ 4]  403 	ld	h, b
   63F6 23            [ 6]  404 	inc	hl
   63F7 56            [ 7]  405 	ld	d, (hl)
   63F8 0A            [ 7]  406 	ld	a, (bc)
   63F9 C5            [11]  407 	push	bc
   63FA 5F            [ 4]  408 	ld	e, a
   63FB D5            [11]  409 	push	de
   63FC 21 00 C0      [10]  410 	ld	hl, #0xc000
   63FF E5            [11]  411 	push	hl
   6400 CD D6 66      [17]  412 	call	_cpct_getScreenPtr
   6403 EB            [ 4]  413 	ex	de,hl
   6404 C1            [10]  414 	pop	bc
                            415 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   6405 C5            [11]  416 	push	bc
   6406 FD E1         [14]  417 	pop	iy
   6408 FD 7E 05      [19]  418 	ld	a, 5 (iy)
   640B DD 77 FD      [19]  419 	ld	-3 (ix), a
   640E 69            [ 4]  420 	ld	l, c
   640F 60            [ 4]  421 	ld	h, b
   6410 01 04 00      [10]  422 	ld	bc, #0x0004
   6413 09            [11]  423 	add	hl, bc
   6414 4E            [ 7]  424 	ld	c, (hl)
   6415 D5            [11]  425 	push	de
   6416 FD E1         [14]  426 	pop	iy
   6418 DD 5E FE      [19]  427 	ld	e,-2 (ix)
   641B DD 56 FF      [19]  428 	ld	d,-1 (ix)
   641E DD 46 FD      [19]  429 	ld	b, -3 (ix)
   6421 C5            [11]  430 	push	bc
   6422 FD E5         [15]  431 	push	iy
   6424 D5            [11]  432 	push	de
   6425 CD 07 65      [17]  433 	call	_cpct_drawSprite
   6428                     434 00110$:
   6428 DD F9         [10]  435 	ld	sp, ix
   642A DD E1         [14]  436 	pop	ix
   642C C9            [10]  437 	ret
                            438 	.area _CODE
                            439 	.area _INITIALIZER
                            440 	.area _CABS (ABS)
