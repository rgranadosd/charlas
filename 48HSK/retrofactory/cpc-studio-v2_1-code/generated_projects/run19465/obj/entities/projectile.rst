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
                             12 	.globl _cpct_drawSolidBox
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
                             48 ;src/entities/projectile.c:4: void projectileinit(Projectile* projectile) {
                             49 ;	---------------------------------
                             50 ; Function projectileinit
                             51 ; ---------------------------------
   5A3F                      52 _projectileinit::
                             53 ;src/entities/projectile.c:5: if (!projectile) {
   5A3F 21 03 00      [10]   54 	ld	hl, #2+1
   5A42 39            [11]   55 	add	hl, sp
   5A43 7E            [ 7]   56 	ld	a, (hl)
   5A44 2B            [ 6]   57 	dec	hl
   5A45 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:6: return;
   5A46 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:9: projectile->x = 0;
   5A47 D1            [10]   62 	pop	de
   5A48 C1            [10]   63 	pop	bc
   5A49 C5            [11]   64 	push	bc
   5A4A D5            [11]   65 	push	de
   5A4B AF            [ 4]   66 	xor	a, a
   5A4C 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:10: projectile->y = 0;
   5A4D 59            [ 4]   69 	ld	e, c
   5A4E 50            [ 4]   70 	ld	d, b
   5A4F 13            [ 6]   71 	inc	de
   5A50 AF            [ 4]   72 	xor	a, a
   5A51 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:11: projectile->vx = 0;
   5A52 59            [ 4]   75 	ld	e, c
   5A53 50            [ 4]   76 	ld	d, b
   5A54 13            [ 6]   77 	inc	de
   5A55 13            [ 6]   78 	inc	de
   5A56 AF            [ 4]   79 	xor	a, a
   5A57 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:12: projectile->vy = 0;
   5A58 59            [ 4]   82 	ld	e, c
   5A59 50            [ 4]   83 	ld	d, b
   5A5A 13            [ 6]   84 	inc	de
   5A5B 13            [ 6]   85 	inc	de
   5A5C 13            [ 6]   86 	inc	de
   5A5D AF            [ 4]   87 	xor	a, a
   5A5E 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:13: projectile->w = 2;
   5A5F 21 04 00      [10]   90 	ld	hl, #0x0004
   5A62 09            [11]   91 	add	hl, bc
   5A63 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:14: projectile->h = 2;
   5A65 21 05 00      [10]   94 	ld	hl, #0x0005
   5A68 09            [11]   95 	add	hl, bc
   5A69 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:15: projectile->active = 0;
   5A6B 21 06 00      [10]   98 	ld	hl, #0x0006
   5A6E 09            [11]   99 	add	hl, bc
   5A6F 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:16: projectile->damage = 1;
   5A71 21 07 00      [10]  102 	ld	hl, #0x0007
   5A74 09            [11]  103 	add	hl, bc
   5A75 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5A77 21 08 00      [10]  106 	ld	hl, #0x0008
   5A7A 09            [11]  107 	add	hl, bc
   5A7B 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5A7D 21 09 00      [10]  110 	ld	hl, #0x0009
   5A80 09            [11]  111 	add	hl, bc
   5A81 36 00         [10]  112 	ld	(hl), #0x00
   5A83 C9            [10]  113 	ret
                            114 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            115 ;	---------------------------------
                            116 ; Function projectilefire
                            117 ; ---------------------------------
   5A84                     118 _projectilefire::
   5A84 DD E5         [15]  119 	push	ix
   5A86 DD 21 00 00   [14]  120 	ld	ix,#0
   5A8A DD 39         [15]  121 	add	ix,sp
   5A8C F5            [11]  122 	push	af
   5A8D F5            [11]  123 	push	af
                            124 ;src/entities/projectile.c:22: if (!projectile) {
   5A8E DD 7E 05      [19]  125 	ld	a, 5 (ix)
   5A91 DD B6 04      [19]  126 	or	a,4 (ix)
                            127 ;src/entities/projectile.c:23: return;
   5A94 CA 36 5B      [10]  128 	jp	Z,00109$
                            129 ;src/entities/projectile.c:26: projectile->x = x;
   5A97 DD 4E 04      [19]  130 	ld	c,4 (ix)
   5A9A DD 46 05      [19]  131 	ld	b,5 (ix)
   5A9D DD 7E 06      [19]  132 	ld	a, 6 (ix)
   5AA0 02            [ 7]  133 	ld	(bc), a
                            134 ;src/entities/projectile.c:27: projectile->y = y;
   5AA1 59            [ 4]  135 	ld	e, c
   5AA2 50            [ 4]  136 	ld	d, b
   5AA3 13            [ 6]  137 	inc	de
   5AA4 DD 7E 07      [19]  138 	ld	a, 7 (ix)
   5AA7 12            [ 7]  139 	ld	(de), a
                            140 ;src/entities/projectile.c:28: projectile->vx = dir;
   5AA8 21 02 00      [10]  141 	ld	hl, #0x0002
   5AAB 09            [11]  142 	add	hl,bc
   5AAC DD 75 FE      [19]  143 	ld	-2 (ix), l
   5AAF DD 74 FF      [19]  144 	ld	-1 (ix), h
   5AB2 DD 7E 08      [19]  145 	ld	a, 8 (ix)
   5AB5 77            [ 7]  146 	ld	(hl), a
                            147 ;src/entities/projectile.c:29: projectile->vy = 0;
   5AB6 59            [ 4]  148 	ld	e, c
   5AB7 50            [ 4]  149 	ld	d, b
   5AB8 13            [ 6]  150 	inc	de
   5AB9 13            [ 6]  151 	inc	de
   5ABA 13            [ 6]  152 	inc	de
   5ABB AF            [ 4]  153 	xor	a, a
   5ABC 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5ABD 21 09 00      [10]  156 	ld	hl, #0x0009
   5AC0 09            [11]  157 	add	hl, bc
   5AC1 DD 7E 09      [19]  158 	ld	a, 9 (ix)
   5AC4 77            [ 7]  159 	ld	(hl), a
                            160 ;src/entities/projectile.c:31: projectile->active = 1;
   5AC5 21 06 00      [10]  161 	ld	hl, #0x0006
   5AC8 09            [11]  162 	add	hl, bc
   5AC9 36 01         [10]  163 	ld	(hl), #0x01
                            164 ;src/entities/projectile.c:34: projectile->w = 3;
   5ACB 21 04 00      [10]  165 	ld	hl, #0x0004
   5ACE 09            [11]  166 	add	hl, bc
                            167 ;src/entities/projectile.c:35: projectile->h = 2;
   5ACF 79            [ 4]  168 	ld	a, c
   5AD0 C6 05         [ 7]  169 	add	a, #0x05
   5AD2 5F            [ 4]  170 	ld	e, a
   5AD3 78            [ 4]  171 	ld	a, b
   5AD4 CE 00         [ 7]  172 	adc	a, #0x00
   5AD6 57            [ 4]  173 	ld	d, a
                            174 ;src/entities/projectile.c:36: projectile->damage = 1;
   5AD7 79            [ 4]  175 	ld	a, c
   5AD8 C6 07         [ 7]  176 	add	a, #0x07
   5ADA DD 77 FC      [19]  177 	ld	-4 (ix), a
   5ADD 78            [ 4]  178 	ld	a, b
   5ADE CE 00         [ 7]  179 	adc	a, #0x00
   5AE0 DD 77 FD      [19]  180 	ld	-3 (ix), a
                            181 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AE3 79            [ 4]  182 	ld	a, c
   5AE4 C6 08         [ 7]  183 	add	a, #0x08
   5AE6 4F            [ 4]  184 	ld	c, a
   5AE7 78            [ 4]  185 	ld	a, b
   5AE8 CE 00         [ 7]  186 	adc	a, #0x00
   5AEA 47            [ 4]  187 	ld	b, a
                            188 ;src/entities/projectile.c:33: if (weapon == 0) {
   5AEB DD 7E 09      [19]  189 	ld	a, 9 (ix)
   5AEE B7            [ 4]  190 	or	a, a
   5AEF 20 0E         [12]  191 	jr	NZ,00107$
                            192 ;src/entities/projectile.c:34: projectile->w = 3;
   5AF1 36 03         [10]  193 	ld	(hl), #0x03
                            194 ;src/entities/projectile.c:35: projectile->h = 2;
   5AF3 3E 02         [ 7]  195 	ld	a, #0x02
   5AF5 12            [ 7]  196 	ld	(de), a
                            197 ;src/entities/projectile.c:36: projectile->damage = 1;
   5AF6 E1            [10]  198 	pop	hl
   5AF7 E5            [11]  199 	push	hl
   5AF8 36 01         [10]  200 	ld	(hl), #0x01
                            201 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AFA 3E 2D         [ 7]  202 	ld	a, #0x2d
   5AFC 02            [ 7]  203 	ld	(bc), a
   5AFD 18 37         [12]  204 	jr	00109$
   5AFF                     205 00107$:
                            206 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5AFF DD 7E 09      [19]  207 	ld	a, 9 (ix)
   5B02 3D            [ 4]  208 	dec	a
   5B03 20 0E         [12]  209 	jr	NZ,00104$
                            210 ;src/entities/projectile.c:39: projectile->w = 2;
   5B05 36 02         [10]  211 	ld	(hl), #0x02
                            212 ;src/entities/projectile.c:40: projectile->h = 3;
   5B07 3E 03         [ 7]  213 	ld	a, #0x03
   5B09 12            [ 7]  214 	ld	(de), a
                            215 ;src/entities/projectile.c:41: projectile->damage = 2;
   5B0A E1            [10]  216 	pop	hl
   5B0B E5            [11]  217 	push	hl
   5B0C 36 02         [10]  218 	ld	(hl), #0x02
                            219 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5B0E 3E 1C         [ 7]  220 	ld	a, #0x1c
   5B10 02            [ 7]  221 	ld	(bc), a
   5B11 18 23         [12]  222 	jr	00109$
   5B13                     223 00104$:
                            224 ;src/entities/projectile.c:44: projectile->w = 4;
   5B13 36 04         [10]  225 	ld	(hl), #0x04
                            226 ;src/entities/projectile.c:45: projectile->h = 3;
   5B15 3E 03         [ 7]  227 	ld	a, #0x03
   5B17 12            [ 7]  228 	ld	(de), a
                            229 ;src/entities/projectile.c:46: projectile->damage = 3;
   5B18 E1            [10]  230 	pop	hl
   5B19 E5            [11]  231 	push	hl
   5B1A 36 03         [10]  232 	ld	(hl), #0x03
                            233 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5B1C 3E 38         [ 7]  234 	ld	a, #0x38
   5B1E 02            [ 7]  235 	ld	(bc), a
                            236 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5B1F D1            [10]  237 	pop	de
   5B20 C1            [10]  238 	pop	bc
   5B21 C5            [11]  239 	push	bc
   5B22 D5            [11]  240 	push	de
   5B23 AF            [ 4]  241 	xor	a, a
   5B24 DD 96 08      [19]  242 	sub	a, 8 (ix)
   5B27 E2 2C 5B      [10]  243 	jp	PO, 00131$
   5B2A EE 80         [ 7]  244 	xor	a, #0x80
   5B2C                     245 00131$:
   5B2C F2 33 5B      [10]  246 	jp	P, 00111$
   5B2F 3E 04         [ 7]  247 	ld	a, #0x04
   5B31 18 02         [12]  248 	jr	00112$
   5B33                     249 00111$:
   5B33 3E FC         [ 7]  250 	ld	a, #0xfc
   5B35                     251 00112$:
   5B35 02            [ 7]  252 	ld	(bc), a
   5B36                     253 00109$:
   5B36 DD F9         [10]  254 	ld	sp, ix
   5B38 DD E1         [14]  255 	pop	ix
   5B3A C9            [10]  256 	ret
                            257 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            258 ;	---------------------------------
                            259 ; Function projectileupdate
                            260 ; ---------------------------------
   5B3B                     261 _projectileupdate::
   5B3B DD E5         [15]  262 	push	ix
   5B3D DD 21 00 00   [14]  263 	ld	ix,#0
   5B41 DD 39         [15]  264 	add	ix,sp
   5B43 3B            [ 6]  265 	dec	sp
                            266 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5B44 DD 7E 05      [19]  267 	ld	a, 5 (ix)
   5B47 DD B6 04      [19]  268 	or	a,4 (ix)
   5B4A 28 4A         [12]  269 	jr	Z,00109$
   5B4C DD 5E 04      [19]  270 	ld	e,4 (ix)
   5B4F DD 56 05      [19]  271 	ld	d,5 (ix)
   5B52 FD 21 06 00   [14]  272 	ld	iy, #0x0006
   5B56 FD 19         [15]  273 	add	iy, de
   5B58 FD 7E 00      [19]  274 	ld	a, 0 (iy)
   5B5B B7            [ 4]  275 	or	a, a
                            276 ;src/entities/projectile.c:54: return;
   5B5C 28 38         [12]  277 	jr	Z,00109$
                            278 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5B5E 1A            [ 7]  279 	ld	a, (de)
   5B5F 4F            [ 4]  280 	ld	c, a
   5B60 6B            [ 4]  281 	ld	l, e
   5B61 62            [ 4]  282 	ld	h, d
   5B62 23            [ 6]  283 	inc	hl
   5B63 23            [ 6]  284 	inc	hl
   5B64 6E            [ 7]  285 	ld	l, (hl)
   5B65 09            [11]  286 	add	hl, bc
   5B66 7D            [ 4]  287 	ld	a, l
   5B67 12            [ 7]  288 	ld	(de), a
                            289 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5B68 4B            [ 4]  290 	ld	c, e
   5B69 42            [ 4]  291 	ld	b, d
   5B6A 03            [ 6]  292 	inc	bc
   5B6B 0A            [ 7]  293 	ld	a, (bc)
   5B6C DD 77 FF      [19]  294 	ld	-1 (ix), a
   5B6F 6B            [ 4]  295 	ld	l, e
   5B70 62            [ 4]  296 	ld	h, d
   5B71 23            [ 6]  297 	inc	hl
   5B72 23            [ 6]  298 	inc	hl
   5B73 23            [ 6]  299 	inc	hl
   5B74 6E            [ 7]  300 	ld	l, (hl)
   5B75 DD 7E FF      [19]  301 	ld	a, -1 (ix)
   5B78 85            [ 4]  302 	add	a, l
   5B79 02            [ 7]  303 	ld	(bc), a
                            304 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5B7A 21 08 00      [10]  305 	ld	hl, #0x0008
   5B7D 19            [11]  306 	add	hl,de
   5B7E 4D            [ 4]  307 	ld	c, l
   5B7F 44            [ 4]  308 	ld	b, h
   5B80 0A            [ 7]  309 	ld	a, (bc)
   5B81 B7            [ 4]  310 	or	a, a
   5B82 28 03         [12]  311 	jr	Z,00105$
                            312 ;src/entities/projectile.c:61: projectile->lifetime--;
   5B84 C6 FF         [ 7]  313 	add	a, #0xff
   5B86 02            [ 7]  314 	ld	(bc), a
   5B87                     315 00105$:
                            316 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5B87 1A            [ 7]  317 	ld	a, (de)
   5B88 5F            [ 4]  318 	ld	e, a
   5B89 3E 4E         [ 7]  319 	ld	a, #0x4e
   5B8B 93            [ 4]  320 	sub	a, e
   5B8C 38 04         [12]  321 	jr	C,00106$
   5B8E 0A            [ 7]  322 	ld	a, (bc)
   5B8F B7            [ 4]  323 	or	a, a
   5B90 20 04         [12]  324 	jr	NZ,00109$
   5B92                     325 00106$:
                            326 ;src/entities/projectile.c:65: projectile->active = 0;
   5B92 FD 36 00 00   [19]  327 	ld	0 (iy), #0x00
   5B96                     328 00109$:
   5B96 33            [ 6]  329 	inc	sp
   5B97 DD E1         [14]  330 	pop	ix
   5B99 C9            [10]  331 	ret
                            332 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            333 ;	---------------------------------
                            334 ; Function projectilerender
                            335 ; ---------------------------------
   5B9A                     336 _projectilerender::
   5B9A DD E5         [15]  337 	push	ix
   5B9C DD 21 00 00   [14]  338 	ld	ix,#0
   5BA0 DD 39         [15]  339 	add	ix,sp
   5BA2 F5            [11]  340 	push	af
                            341 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5BA3 DD 7E 05      [19]  342 	ld	a, 5 (ix)
   5BA6 DD B6 04      [19]  343 	or	a,4 (ix)
   5BA9 28 5B         [12]  344 	jr	Z,00104$
   5BAB DD 5E 04      [19]  345 	ld	e,4 (ix)
   5BAE DD 56 05      [19]  346 	ld	d,5 (ix)
   5BB1 D5            [11]  347 	push	de
   5BB2 FD E1         [14]  348 	pop	iy
   5BB4 FD 7E 06      [19]  349 	ld	a, 6 (iy)
   5BB7 B7            [ 4]  350 	or	a, a
                            351 ;src/entities/projectile.c:73: return;
   5BB8 28 4C         [12]  352 	jr	Z,00104$
                            353 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5BBA 6B            [ 4]  354 	ld	l, e
   5BBB 62            [ 4]  355 	ld	h, d
   5BBC 23            [ 6]  356 	inc	hl
   5BBD 46            [ 7]  357 	ld	b, (hl)
   5BBE 1A            [ 7]  358 	ld	a, (de)
   5BBF D5            [11]  359 	push	de
   5BC0 C5            [11]  360 	push	bc
   5BC1 33            [ 6]  361 	inc	sp
   5BC2 F5            [11]  362 	push	af
   5BC3 33            [ 6]  363 	inc	sp
   5BC4 21 00 C0      [10]  364 	ld	hl, #0xc000
   5BC7 E5            [11]  365 	push	hl
   5BC8 CD 98 5E      [17]  366 	call	_cpct_getScreenPtr
   5BCB 4D            [ 4]  367 	ld	c, l
   5BCC 44            [ 4]  368 	ld	b, h
   5BCD D1            [10]  369 	pop	de
                            370 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? 0x0F : (projectile->weapon == 1 ? 0x6B : 0x5A), projectile->w, projectile->h);
   5BCE D5            [11]  371 	push	de
   5BCF FD E1         [14]  372 	pop	iy
   5BD1 FD 7E 05      [19]  373 	ld	a, 5 (iy)
   5BD4 DD 77 FE      [19]  374 	ld	-2 (ix), a
   5BD7 D5            [11]  375 	push	de
   5BD8 FD E1         [14]  376 	pop	iy
   5BDA FD 7E 04      [19]  377 	ld	a, 4 (iy)
   5BDD DD 77 FF      [19]  378 	ld	-1 (ix), a
   5BE0 EB            [ 4]  379 	ex	de,hl
   5BE1 11 09 00      [10]  380 	ld	de, #0x0009
   5BE4 19            [11]  381 	add	hl, de
   5BE5 7E            [ 7]  382 	ld	a, (hl)
   5BE6 B7            [ 4]  383 	or	a, a
   5BE7 20 04         [12]  384 	jr	NZ,00106$
   5BE9 16 0F         [ 7]  385 	ld	d, #0x0f
   5BEB 18 09         [12]  386 	jr	00107$
   5BED                     387 00106$:
   5BED 3D            [ 4]  388 	dec	a
   5BEE 20 04         [12]  389 	jr	NZ,00108$
   5BF0 16 6B         [ 7]  390 	ld	d, #0x6b
   5BF2 18 02         [12]  391 	jr	00109$
   5BF4                     392 00108$:
   5BF4 16 5A         [ 7]  393 	ld	d, #0x5a
   5BF6                     394 00109$:
   5BF6                     395 00107$:
   5BF6 DD 66 FE      [19]  396 	ld	h, -2 (ix)
   5BF9 DD 6E FF      [19]  397 	ld	l, -1 (ix)
   5BFC E5            [11]  398 	push	hl
   5BFD D5            [11]  399 	push	de
   5BFE 33            [ 6]  400 	inc	sp
   5BFF C5            [11]  401 	push	bc
   5C00 CD DF 5D      [17]  402 	call	_cpct_drawSolidBox
   5C03 F1            [10]  403 	pop	af
   5C04 F1            [10]  404 	pop	af
   5C05 33            [ 6]  405 	inc	sp
   5C06                     406 00104$:
   5C06 DD F9         [10]  407 	ld	sp, ix
   5C08 DD E1         [14]  408 	pop	ix
   5C0A C9            [10]  409 	ret
                            410 	.area _CODE
                            411 	.area _INITIALIZER
                            412 	.area _CABS (ABS)
