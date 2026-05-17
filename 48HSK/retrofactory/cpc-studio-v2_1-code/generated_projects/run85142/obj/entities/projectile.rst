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
   6107                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   6107 21 03 00      [10]   54 	ld	hl, #2+1
   610A 39            [11]   55 	add	hl, sp
   610B 7E            [ 7]   56 	ld	a, (hl)
   610C 2B            [ 6]   57 	dec	hl
   610D B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   610E C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   610F D1            [10]   62 	pop	de
   6110 C1            [10]   63 	pop	bc
   6111 C5            [11]   64 	push	bc
   6112 D5            [11]   65 	push	de
   6113 AF            [ 4]   66 	xor	a, a
   6114 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   6115 59            [ 4]   69 	ld	e, c
   6116 50            [ 4]   70 	ld	d, b
   6117 13            [ 6]   71 	inc	de
   6118 AF            [ 4]   72 	xor	a, a
   6119 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   611A 59            [ 4]   75 	ld	e, c
   611B 50            [ 4]   76 	ld	d, b
   611C 13            [ 6]   77 	inc	de
   611D 13            [ 6]   78 	inc	de
   611E AF            [ 4]   79 	xor	a, a
   611F 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   6120 59            [ 4]   82 	ld	e, c
   6121 50            [ 4]   83 	ld	d, b
   6122 13            [ 6]   84 	inc	de
   6123 13            [ 6]   85 	inc	de
   6124 13            [ 6]   86 	inc	de
   6125 AF            [ 4]   87 	xor	a, a
   6126 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   6127 21 04 00      [10]   90 	ld	hl, #0x0004
   612A 09            [11]   91 	add	hl, bc
   612B 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   612D 21 05 00      [10]   94 	ld	hl, #0x0005
   6130 09            [11]   95 	add	hl, bc
   6131 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   6133 21 06 00      [10]   98 	ld	hl, #0x0006
   6136 09            [11]   99 	add	hl, bc
   6137 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   6139 21 07 00      [10]  102 	ld	hl, #0x0007
   613C 09            [11]  103 	add	hl, bc
   613D 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   613F 21 08 00      [10]  106 	ld	hl, #0x0008
   6142 09            [11]  107 	add	hl, bc
   6143 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   6145 21 09 00      [10]  110 	ld	hl, #0x0009
   6148 09            [11]  111 	add	hl, bc
   6149 36 00         [10]  112 	ld	(hl), #0x00
   614B C9            [10]  113 	ret
   614C                     114 _projectile_basic_sprite:
   614C 3C                  115 	.db #0x3c	; 60
   614D 3C                  116 	.db #0x3c	; 60
   614E 3C                  117 	.db #0x3c	; 60
   614F 3C                  118 	.db #0x3c	; 60
   6150 3C                  119 	.db #0x3c	; 60
   6151 3C                  120 	.db #0x3c	; 60
   6152                     121 _projectile_up_sprite:
   6152 C3                  122 	.db #0xc3	; 195
   6153 C3                  123 	.db #0xc3	; 195
   6154 C3                  124 	.db #0xc3	; 195
   6155 C3                  125 	.db #0xc3	; 195
   6156 C3                  126 	.db #0xc3	; 195
   6157 C3                  127 	.db #0xc3	; 195
   6158                     128 _projectile_special_sprite:
   6158 FF                  129 	.db #0xff	; 255
   6159 FF                  130 	.db #0xff	; 255
   615A FF                  131 	.db #0xff	; 255
   615B FF                  132 	.db #0xff	; 255
   615C FF                  133 	.db #0xff	; 255
   615D FF                  134 	.db #0xff	; 255
   615E FF                  135 	.db #0xff	; 255
   615F FF                  136 	.db #0xff	; 255
   6160 FF                  137 	.db #0xff	; 255
   6161 FF                  138 	.db #0xff	; 255
   6162 FF                  139 	.db #0xff	; 255
   6163 FF                  140 	.db #0xff	; 255
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   6164                     145 _projectilefire::
   6164 DD E5         [15]  146 	push	ix
   6166 DD 21 00 00   [14]  147 	ld	ix,#0
   616A DD 39         [15]  148 	add	ix,sp
   616C F5            [11]  149 	push	af
   616D F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   616E DD 7E 05      [19]  152 	ld	a, 5 (ix)
   6171 DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   6174 CA 16 62      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   6177 DD 4E 04      [19]  157 	ld	c,4 (ix)
   617A DD 46 05      [19]  158 	ld	b,5 (ix)
   617D DD 7E 06      [19]  159 	ld	a, 6 (ix)
   6180 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   6181 59            [ 4]  162 	ld	e, c
   6182 50            [ 4]  163 	ld	d, b
   6183 13            [ 6]  164 	inc	de
   6184 DD 7E 07      [19]  165 	ld	a, 7 (ix)
   6187 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   6188 21 02 00      [10]  168 	ld	hl, #0x0002
   618B 09            [11]  169 	add	hl,bc
   618C DD 75 FE      [19]  170 	ld	-2 (ix), l
   618F DD 74 FF      [19]  171 	ld	-1 (ix), h
   6192 DD 7E 08      [19]  172 	ld	a, 8 (ix)
   6195 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   6196 59            [ 4]  175 	ld	e, c
   6197 50            [ 4]  176 	ld	d, b
   6198 13            [ 6]  177 	inc	de
   6199 13            [ 6]  178 	inc	de
   619A 13            [ 6]  179 	inc	de
   619B AF            [ 4]  180 	xor	a, a
   619C 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   619D 21 09 00      [10]  183 	ld	hl, #0x0009
   61A0 09            [11]  184 	add	hl, bc
   61A1 DD 7E 09      [19]  185 	ld	a, 9 (ix)
   61A4 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   61A5 21 06 00      [10]  188 	ld	hl, #0x0006
   61A8 09            [11]  189 	add	hl, bc
   61A9 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   61AB 21 04 00      [10]  192 	ld	hl, #0x0004
   61AE 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   61AF 79            [ 4]  195 	ld	a, c
   61B0 C6 05         [ 7]  196 	add	a, #0x05
   61B2 5F            [ 4]  197 	ld	e, a
   61B3 78            [ 4]  198 	ld	a, b
   61B4 CE 00         [ 7]  199 	adc	a, #0x00
   61B6 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   61B7 79            [ 4]  202 	ld	a, c
   61B8 C6 07         [ 7]  203 	add	a, #0x07
   61BA DD 77 FC      [19]  204 	ld	-4 (ix), a
   61BD 78            [ 4]  205 	ld	a, b
   61BE CE 00         [ 7]  206 	adc	a, #0x00
   61C0 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   61C3 79            [ 4]  209 	ld	a, c
   61C4 C6 08         [ 7]  210 	add	a, #0x08
   61C6 4F            [ 4]  211 	ld	c, a
   61C7 78            [ 4]  212 	ld	a, b
   61C8 CE 00         [ 7]  213 	adc	a, #0x00
   61CA 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   61CB DD 7E 09      [19]  216 	ld	a, 9 (ix)
   61CE B7            [ 4]  217 	or	a, a
   61CF 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   61D1 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   61D3 3E 02         [ 7]  222 	ld	a, #0x02
   61D5 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   61D6 E1            [10]  225 	pop	hl
   61D7 E5            [11]  226 	push	hl
   61D8 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   61DA 3E 2D         [ 7]  229 	ld	a, #0x2d
   61DC 02            [ 7]  230 	ld	(bc), a
   61DD 18 37         [12]  231 	jr	00109$
   61DF                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   61DF DD 7E 09      [19]  234 	ld	a, 9 (ix)
   61E2 3D            [ 4]  235 	dec	a
   61E3 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   61E5 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   61E7 3E 03         [ 7]  240 	ld	a, #0x03
   61E9 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   61EA E1            [10]  243 	pop	hl
   61EB E5            [11]  244 	push	hl
   61EC 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   61EE 3E 1C         [ 7]  247 	ld	a, #0x1c
   61F0 02            [ 7]  248 	ld	(bc), a
   61F1 18 23         [12]  249 	jr	00109$
   61F3                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   61F3 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   61F5 3E 03         [ 7]  254 	ld	a, #0x03
   61F7 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   61F8 E1            [10]  257 	pop	hl
   61F9 E5            [11]  258 	push	hl
   61FA 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   61FC 3E 38         [ 7]  261 	ld	a, #0x38
   61FE 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   61FF D1            [10]  264 	pop	de
   6200 C1            [10]  265 	pop	bc
   6201 C5            [11]  266 	push	bc
   6202 D5            [11]  267 	push	de
   6203 AF            [ 4]  268 	xor	a, a
   6204 DD 96 08      [19]  269 	sub	a, 8 (ix)
   6207 E2 0C 62      [10]  270 	jp	PO, 00131$
   620A EE 80         [ 7]  271 	xor	a, #0x80
   620C                     272 00131$:
   620C F2 13 62      [10]  273 	jp	P, 00111$
   620F 3E 04         [ 7]  274 	ld	a, #0x04
   6211 18 02         [12]  275 	jr	00112$
   6213                     276 00111$:
   6213 3E FC         [ 7]  277 	ld	a, #0xfc
   6215                     278 00112$:
   6215 02            [ 7]  279 	ld	(bc), a
   6216                     280 00109$:
   6216 DD F9         [10]  281 	ld	sp, ix
   6218 DD E1         [14]  282 	pop	ix
   621A C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   621B                     288 _projectileupdate::
   621B DD E5         [15]  289 	push	ix
   621D DD 21 00 00   [14]  290 	ld	ix,#0
   6221 DD 39         [15]  291 	add	ix,sp
   6223 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   6224 DD 7E 05      [19]  294 	ld	a, 5 (ix)
   6227 DD B6 04      [19]  295 	or	a,4 (ix)
   622A 28 4A         [12]  296 	jr	Z,00109$
   622C DD 5E 04      [19]  297 	ld	e,4 (ix)
   622F DD 56 05      [19]  298 	ld	d,5 (ix)
   6232 FD 21 06 00   [14]  299 	ld	iy, #0x0006
   6236 FD 19         [15]  300 	add	iy, de
   6238 FD 7E 00      [19]  301 	ld	a, 0 (iy)
   623B B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   623C 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   623E 1A            [ 7]  306 	ld	a, (de)
   623F 4F            [ 4]  307 	ld	c, a
   6240 6B            [ 4]  308 	ld	l, e
   6241 62            [ 4]  309 	ld	h, d
   6242 23            [ 6]  310 	inc	hl
   6243 23            [ 6]  311 	inc	hl
   6244 6E            [ 7]  312 	ld	l, (hl)
   6245 09            [11]  313 	add	hl, bc
   6246 7D            [ 4]  314 	ld	a, l
   6247 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   6248 4B            [ 4]  317 	ld	c, e
   6249 42            [ 4]  318 	ld	b, d
   624A 03            [ 6]  319 	inc	bc
   624B 0A            [ 7]  320 	ld	a, (bc)
   624C DD 77 FF      [19]  321 	ld	-1 (ix), a
   624F 6B            [ 4]  322 	ld	l, e
   6250 62            [ 4]  323 	ld	h, d
   6251 23            [ 6]  324 	inc	hl
   6252 23            [ 6]  325 	inc	hl
   6253 23            [ 6]  326 	inc	hl
   6254 6E            [ 7]  327 	ld	l, (hl)
   6255 DD 7E FF      [19]  328 	ld	a, -1 (ix)
   6258 85            [ 4]  329 	add	a, l
   6259 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   625A 21 08 00      [10]  332 	ld	hl, #0x0008
   625D 19            [11]  333 	add	hl,de
   625E 4D            [ 4]  334 	ld	c, l
   625F 44            [ 4]  335 	ld	b, h
   6260 0A            [ 7]  336 	ld	a, (bc)
   6261 B7            [ 4]  337 	or	a, a
   6262 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   6264 C6 FF         [ 7]  340 	add	a, #0xff
   6266 02            [ 7]  341 	ld	(bc), a
   6267                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   6267 1A            [ 7]  344 	ld	a, (de)
   6268 5F            [ 4]  345 	ld	e, a
   6269 3E 4E         [ 7]  346 	ld	a, #0x4e
   626B 93            [ 4]  347 	sub	a, e
   626C 38 04         [12]  348 	jr	C,00106$
   626E 0A            [ 7]  349 	ld	a, (bc)
   626F B7            [ 4]  350 	or	a, a
   6270 20 04         [12]  351 	jr	NZ,00109$
   6272                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   6272 FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   6276                     355 00109$:
   6276 33            [ 6]  356 	inc	sp
   6277 DD E1         [14]  357 	pop	ix
   6279 C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   627A                     363 _projectilerender::
   627A DD E5         [15]  364 	push	ix
   627C DD 21 00 00   [14]  365 	ld	ix,#0
   6280 DD 39         [15]  366 	add	ix,sp
   6282 F5            [11]  367 	push	af
   6283 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   6284 DD 7E 05      [19]  370 	ld	a, 5 (ix)
   6287 DD B6 04      [19]  371 	or	a,4 (ix)
   628A 28 6B         [12]  372 	jr	Z,00110$
   628C DD 4E 04      [19]  373 	ld	c,4 (ix)
   628F DD 46 05      [19]  374 	ld	b,5 (ix)
   6292 C5            [11]  375 	push	bc
   6293 FD E1         [14]  376 	pop	iy
   6295 FD 7E 06      [19]  377 	ld	a, 6 (iy)
   6298 B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   6299 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   629B C5            [11]  382 	push	bc
   629C FD E1         [14]  383 	pop	iy
   629E FD 7E 09      [19]  384 	ld	a, 9 (iy)
   62A1 B7            [ 4]  385 	or	a, a
   62A2 20 0A         [12]  386 	jr	NZ,00108$
   62A4 DD 36 FE 4C   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   62A8 DD 36 FF 61   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   62AC 18 15         [12]  389 	jr	00109$
   62AE                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   62AE 3D            [ 4]  392 	dec	a
   62AF 20 0A         [12]  393 	jr	NZ,00105$
   62B1 DD 36 FE 52   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   62B5 DD 36 FF 61   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   62B9 18 08         [12]  396 	jr	00109$
   62BB                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   62BB DD 36 FE 58   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   62BF DD 36 FF 61   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   62C3                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   62C3 69            [ 4]  403 	ld	l, c
   62C4 60            [ 4]  404 	ld	h, b
   62C5 23            [ 6]  405 	inc	hl
   62C6 56            [ 7]  406 	ld	d, (hl)
   62C7 0A            [ 7]  407 	ld	a, (bc)
   62C8 C5            [11]  408 	push	bc
   62C9 5F            [ 4]  409 	ld	e, a
   62CA D5            [11]  410 	push	de
   62CB 21 00 C0      [10]  411 	ld	hl, #0xc000
   62CE E5            [11]  412 	push	hl
   62CF CD A5 65      [17]  413 	call	_cpct_getScreenPtr
   62D2 EB            [ 4]  414 	ex	de,hl
   62D3 C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   62D4 C5            [11]  417 	push	bc
   62D5 FD E1         [14]  418 	pop	iy
   62D7 FD 7E 05      [19]  419 	ld	a, 5 (iy)
   62DA DD 77 FD      [19]  420 	ld	-3 (ix), a
   62DD 69            [ 4]  421 	ld	l, c
   62DE 60            [ 4]  422 	ld	h, b
   62DF 01 04 00      [10]  423 	ld	bc, #0x0004
   62E2 09            [11]  424 	add	hl, bc
   62E3 4E            [ 7]  425 	ld	c, (hl)
   62E4 D5            [11]  426 	push	de
   62E5 FD E1         [14]  427 	pop	iy
   62E7 DD 5E FE      [19]  428 	ld	e,-2 (ix)
   62EA DD 56 FF      [19]  429 	ld	d,-1 (ix)
   62ED DD 46 FD      [19]  430 	ld	b, -3 (ix)
   62F0 C5            [11]  431 	push	bc
   62F1 FD E5         [15]  432 	push	iy
   62F3 D5            [11]  433 	push	de
   62F4 CD D6 63      [17]  434 	call	_cpct_drawSprite
   62F7                     435 00110$:
   62F7 DD F9         [10]  436 	ld	sp, ix
   62F9 DD E1         [14]  437 	pop	ix
   62FB C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
