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
   5A18                      52 _projectileinit::
                             53 ;src/entities/projectile.c:5: if (!projectile) {
   5A18 21 03 00      [10]   54 	ld	hl, #2+1
   5A1B 39            [11]   55 	add	hl, sp
   5A1C 7E            [ 7]   56 	ld	a, (hl)
   5A1D 2B            [ 6]   57 	dec	hl
   5A1E B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:6: return;
   5A1F C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:9: projectile->x = 0;
   5A20 D1            [10]   62 	pop	de
   5A21 C1            [10]   63 	pop	bc
   5A22 C5            [11]   64 	push	bc
   5A23 D5            [11]   65 	push	de
   5A24 AF            [ 4]   66 	xor	a, a
   5A25 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:10: projectile->y = 0;
   5A26 59            [ 4]   69 	ld	e, c
   5A27 50            [ 4]   70 	ld	d, b
   5A28 13            [ 6]   71 	inc	de
   5A29 AF            [ 4]   72 	xor	a, a
   5A2A 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:11: projectile->vx = 0;
   5A2B 59            [ 4]   75 	ld	e, c
   5A2C 50            [ 4]   76 	ld	d, b
   5A2D 13            [ 6]   77 	inc	de
   5A2E 13            [ 6]   78 	inc	de
   5A2F AF            [ 4]   79 	xor	a, a
   5A30 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:12: projectile->vy = 0;
   5A31 59            [ 4]   82 	ld	e, c
   5A32 50            [ 4]   83 	ld	d, b
   5A33 13            [ 6]   84 	inc	de
   5A34 13            [ 6]   85 	inc	de
   5A35 13            [ 6]   86 	inc	de
   5A36 AF            [ 4]   87 	xor	a, a
   5A37 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:13: projectile->w = 2;
   5A38 21 04 00      [10]   90 	ld	hl, #0x0004
   5A3B 09            [11]   91 	add	hl, bc
   5A3C 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:14: projectile->h = 2;
   5A3E 21 05 00      [10]   94 	ld	hl, #0x0005
   5A41 09            [11]   95 	add	hl, bc
   5A42 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:15: projectile->active = 0;
   5A44 21 06 00      [10]   98 	ld	hl, #0x0006
   5A47 09            [11]   99 	add	hl, bc
   5A48 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:16: projectile->damage = 1;
   5A4A 21 07 00      [10]  102 	ld	hl, #0x0007
   5A4D 09            [11]  103 	add	hl, bc
   5A4E 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5A50 21 08 00      [10]  106 	ld	hl, #0x0008
   5A53 09            [11]  107 	add	hl, bc
   5A54 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5A56 21 09 00      [10]  110 	ld	hl, #0x0009
   5A59 09            [11]  111 	add	hl, bc
   5A5A 36 00         [10]  112 	ld	(hl), #0x00
   5A5C C9            [10]  113 	ret
                            114 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            115 ;	---------------------------------
                            116 ; Function projectilefire
                            117 ; ---------------------------------
   5A5D                     118 _projectilefire::
   5A5D DD E5         [15]  119 	push	ix
   5A5F DD 21 00 00   [14]  120 	ld	ix,#0
   5A63 DD 39         [15]  121 	add	ix,sp
   5A65 F5            [11]  122 	push	af
   5A66 F5            [11]  123 	push	af
                            124 ;src/entities/projectile.c:22: if (!projectile) {
   5A67 DD 7E 05      [19]  125 	ld	a, 5 (ix)
   5A6A DD B6 04      [19]  126 	or	a,4 (ix)
                            127 ;src/entities/projectile.c:23: return;
   5A6D CA 0F 5B      [10]  128 	jp	Z,00109$
                            129 ;src/entities/projectile.c:26: projectile->x = x;
   5A70 DD 4E 04      [19]  130 	ld	c,4 (ix)
   5A73 DD 46 05      [19]  131 	ld	b,5 (ix)
   5A76 DD 7E 06      [19]  132 	ld	a, 6 (ix)
   5A79 02            [ 7]  133 	ld	(bc), a
                            134 ;src/entities/projectile.c:27: projectile->y = y;
   5A7A 59            [ 4]  135 	ld	e, c
   5A7B 50            [ 4]  136 	ld	d, b
   5A7C 13            [ 6]  137 	inc	de
   5A7D DD 7E 07      [19]  138 	ld	a, 7 (ix)
   5A80 12            [ 7]  139 	ld	(de), a
                            140 ;src/entities/projectile.c:28: projectile->vx = dir;
   5A81 21 02 00      [10]  141 	ld	hl, #0x0002
   5A84 09            [11]  142 	add	hl,bc
   5A85 DD 75 FE      [19]  143 	ld	-2 (ix), l
   5A88 DD 74 FF      [19]  144 	ld	-1 (ix), h
   5A8B DD 7E 08      [19]  145 	ld	a, 8 (ix)
   5A8E 77            [ 7]  146 	ld	(hl), a
                            147 ;src/entities/projectile.c:29: projectile->vy = 0;
   5A8F 59            [ 4]  148 	ld	e, c
   5A90 50            [ 4]  149 	ld	d, b
   5A91 13            [ 6]  150 	inc	de
   5A92 13            [ 6]  151 	inc	de
   5A93 13            [ 6]  152 	inc	de
   5A94 AF            [ 4]  153 	xor	a, a
   5A95 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5A96 21 09 00      [10]  156 	ld	hl, #0x0009
   5A99 09            [11]  157 	add	hl, bc
   5A9A DD 7E 09      [19]  158 	ld	a, 9 (ix)
   5A9D 77            [ 7]  159 	ld	(hl), a
                            160 ;src/entities/projectile.c:31: projectile->active = 1;
   5A9E 21 06 00      [10]  161 	ld	hl, #0x0006
   5AA1 09            [11]  162 	add	hl, bc
   5AA2 36 01         [10]  163 	ld	(hl), #0x01
                            164 ;src/entities/projectile.c:34: projectile->w = 3;
   5AA4 21 04 00      [10]  165 	ld	hl, #0x0004
   5AA7 09            [11]  166 	add	hl, bc
                            167 ;src/entities/projectile.c:35: projectile->h = 2;
   5AA8 79            [ 4]  168 	ld	a, c
   5AA9 C6 05         [ 7]  169 	add	a, #0x05
   5AAB 5F            [ 4]  170 	ld	e, a
   5AAC 78            [ 4]  171 	ld	a, b
   5AAD CE 00         [ 7]  172 	adc	a, #0x00
   5AAF 57            [ 4]  173 	ld	d, a
                            174 ;src/entities/projectile.c:36: projectile->damage = 1;
   5AB0 79            [ 4]  175 	ld	a, c
   5AB1 C6 07         [ 7]  176 	add	a, #0x07
   5AB3 DD 77 FC      [19]  177 	ld	-4 (ix), a
   5AB6 78            [ 4]  178 	ld	a, b
   5AB7 CE 00         [ 7]  179 	adc	a, #0x00
   5AB9 DD 77 FD      [19]  180 	ld	-3 (ix), a
                            181 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5ABC 79            [ 4]  182 	ld	a, c
   5ABD C6 08         [ 7]  183 	add	a, #0x08
   5ABF 4F            [ 4]  184 	ld	c, a
   5AC0 78            [ 4]  185 	ld	a, b
   5AC1 CE 00         [ 7]  186 	adc	a, #0x00
   5AC3 47            [ 4]  187 	ld	b, a
                            188 ;src/entities/projectile.c:33: if (weapon == 0) {
   5AC4 DD 7E 09      [19]  189 	ld	a, 9 (ix)
   5AC7 B7            [ 4]  190 	or	a, a
   5AC8 20 0E         [12]  191 	jr	NZ,00107$
                            192 ;src/entities/projectile.c:34: projectile->w = 3;
   5ACA 36 03         [10]  193 	ld	(hl), #0x03
                            194 ;src/entities/projectile.c:35: projectile->h = 2;
   5ACC 3E 02         [ 7]  195 	ld	a, #0x02
   5ACE 12            [ 7]  196 	ld	(de), a
                            197 ;src/entities/projectile.c:36: projectile->damage = 1;
   5ACF E1            [10]  198 	pop	hl
   5AD0 E5            [11]  199 	push	hl
   5AD1 36 01         [10]  200 	ld	(hl), #0x01
                            201 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AD3 3E 2D         [ 7]  202 	ld	a, #0x2d
   5AD5 02            [ 7]  203 	ld	(bc), a
   5AD6 18 37         [12]  204 	jr	00109$
   5AD8                     205 00107$:
                            206 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5AD8 DD 7E 09      [19]  207 	ld	a, 9 (ix)
   5ADB 3D            [ 4]  208 	dec	a
   5ADC 20 0E         [12]  209 	jr	NZ,00104$
                            210 ;src/entities/projectile.c:39: projectile->w = 2;
   5ADE 36 02         [10]  211 	ld	(hl), #0x02
                            212 ;src/entities/projectile.c:40: projectile->h = 3;
   5AE0 3E 03         [ 7]  213 	ld	a, #0x03
   5AE2 12            [ 7]  214 	ld	(de), a
                            215 ;src/entities/projectile.c:41: projectile->damage = 2;
   5AE3 E1            [10]  216 	pop	hl
   5AE4 E5            [11]  217 	push	hl
   5AE5 36 02         [10]  218 	ld	(hl), #0x02
                            219 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5AE7 3E 1C         [ 7]  220 	ld	a, #0x1c
   5AE9 02            [ 7]  221 	ld	(bc), a
   5AEA 18 23         [12]  222 	jr	00109$
   5AEC                     223 00104$:
                            224 ;src/entities/projectile.c:44: projectile->w = 4;
   5AEC 36 04         [10]  225 	ld	(hl), #0x04
                            226 ;src/entities/projectile.c:45: projectile->h = 3;
   5AEE 3E 03         [ 7]  227 	ld	a, #0x03
   5AF0 12            [ 7]  228 	ld	(de), a
                            229 ;src/entities/projectile.c:46: projectile->damage = 3;
   5AF1 E1            [10]  230 	pop	hl
   5AF2 E5            [11]  231 	push	hl
   5AF3 36 03         [10]  232 	ld	(hl), #0x03
                            233 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5AF5 3E 38         [ 7]  234 	ld	a, #0x38
   5AF7 02            [ 7]  235 	ld	(bc), a
                            236 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5AF8 D1            [10]  237 	pop	de
   5AF9 C1            [10]  238 	pop	bc
   5AFA C5            [11]  239 	push	bc
   5AFB D5            [11]  240 	push	de
   5AFC AF            [ 4]  241 	xor	a, a
   5AFD DD 96 08      [19]  242 	sub	a, 8 (ix)
   5B00 E2 05 5B      [10]  243 	jp	PO, 00131$
   5B03 EE 80         [ 7]  244 	xor	a, #0x80
   5B05                     245 00131$:
   5B05 F2 0C 5B      [10]  246 	jp	P, 00111$
   5B08 3E 04         [ 7]  247 	ld	a, #0x04
   5B0A 18 02         [12]  248 	jr	00112$
   5B0C                     249 00111$:
   5B0C 3E FC         [ 7]  250 	ld	a, #0xfc
   5B0E                     251 00112$:
   5B0E 02            [ 7]  252 	ld	(bc), a
   5B0F                     253 00109$:
   5B0F DD F9         [10]  254 	ld	sp, ix
   5B11 DD E1         [14]  255 	pop	ix
   5B13 C9            [10]  256 	ret
                            257 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            258 ;	---------------------------------
                            259 ; Function projectileupdate
                            260 ; ---------------------------------
   5B14                     261 _projectileupdate::
   5B14 DD E5         [15]  262 	push	ix
   5B16 DD 21 00 00   [14]  263 	ld	ix,#0
   5B1A DD 39         [15]  264 	add	ix,sp
   5B1C 3B            [ 6]  265 	dec	sp
                            266 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5B1D DD 7E 05      [19]  267 	ld	a, 5 (ix)
   5B20 DD B6 04      [19]  268 	or	a,4 (ix)
   5B23 28 4A         [12]  269 	jr	Z,00109$
   5B25 DD 5E 04      [19]  270 	ld	e,4 (ix)
   5B28 DD 56 05      [19]  271 	ld	d,5 (ix)
   5B2B FD 21 06 00   [14]  272 	ld	iy, #0x0006
   5B2F FD 19         [15]  273 	add	iy, de
   5B31 FD 7E 00      [19]  274 	ld	a, 0 (iy)
   5B34 B7            [ 4]  275 	or	a, a
                            276 ;src/entities/projectile.c:54: return;
   5B35 28 38         [12]  277 	jr	Z,00109$
                            278 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5B37 1A            [ 7]  279 	ld	a, (de)
   5B38 4F            [ 4]  280 	ld	c, a
   5B39 6B            [ 4]  281 	ld	l, e
   5B3A 62            [ 4]  282 	ld	h, d
   5B3B 23            [ 6]  283 	inc	hl
   5B3C 23            [ 6]  284 	inc	hl
   5B3D 6E            [ 7]  285 	ld	l, (hl)
   5B3E 09            [11]  286 	add	hl, bc
   5B3F 7D            [ 4]  287 	ld	a, l
   5B40 12            [ 7]  288 	ld	(de), a
                            289 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5B41 4B            [ 4]  290 	ld	c, e
   5B42 42            [ 4]  291 	ld	b, d
   5B43 03            [ 6]  292 	inc	bc
   5B44 0A            [ 7]  293 	ld	a, (bc)
   5B45 DD 77 FF      [19]  294 	ld	-1 (ix), a
   5B48 6B            [ 4]  295 	ld	l, e
   5B49 62            [ 4]  296 	ld	h, d
   5B4A 23            [ 6]  297 	inc	hl
   5B4B 23            [ 6]  298 	inc	hl
   5B4C 23            [ 6]  299 	inc	hl
   5B4D 6E            [ 7]  300 	ld	l, (hl)
   5B4E DD 7E FF      [19]  301 	ld	a, -1 (ix)
   5B51 85            [ 4]  302 	add	a, l
   5B52 02            [ 7]  303 	ld	(bc), a
                            304 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5B53 21 08 00      [10]  305 	ld	hl, #0x0008
   5B56 19            [11]  306 	add	hl,de
   5B57 4D            [ 4]  307 	ld	c, l
   5B58 44            [ 4]  308 	ld	b, h
   5B59 0A            [ 7]  309 	ld	a, (bc)
   5B5A B7            [ 4]  310 	or	a, a
   5B5B 28 03         [12]  311 	jr	Z,00105$
                            312 ;src/entities/projectile.c:61: projectile->lifetime--;
   5B5D C6 FF         [ 7]  313 	add	a, #0xff
   5B5F 02            [ 7]  314 	ld	(bc), a
   5B60                     315 00105$:
                            316 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5B60 1A            [ 7]  317 	ld	a, (de)
   5B61 5F            [ 4]  318 	ld	e, a
   5B62 3E 4E         [ 7]  319 	ld	a, #0x4e
   5B64 93            [ 4]  320 	sub	a, e
   5B65 38 04         [12]  321 	jr	C,00106$
   5B67 0A            [ 7]  322 	ld	a, (bc)
   5B68 B7            [ 4]  323 	or	a, a
   5B69 20 04         [12]  324 	jr	NZ,00109$
   5B6B                     325 00106$:
                            326 ;src/entities/projectile.c:65: projectile->active = 0;
   5B6B FD 36 00 00   [19]  327 	ld	0 (iy), #0x00
   5B6F                     328 00109$:
   5B6F 33            [ 6]  329 	inc	sp
   5B70 DD E1         [14]  330 	pop	ix
   5B72 C9            [10]  331 	ret
                            332 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            333 ;	---------------------------------
                            334 ; Function projectilerender
                            335 ; ---------------------------------
   5B73                     336 _projectilerender::
   5B73 DD E5         [15]  337 	push	ix
   5B75 DD 21 00 00   [14]  338 	ld	ix,#0
   5B79 DD 39         [15]  339 	add	ix,sp
   5B7B F5            [11]  340 	push	af
                            341 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5B7C DD 7E 05      [19]  342 	ld	a, 5 (ix)
   5B7F DD B6 04      [19]  343 	or	a,4 (ix)
   5B82 28 5B         [12]  344 	jr	Z,00104$
   5B84 DD 5E 04      [19]  345 	ld	e,4 (ix)
   5B87 DD 56 05      [19]  346 	ld	d,5 (ix)
   5B8A D5            [11]  347 	push	de
   5B8B FD E1         [14]  348 	pop	iy
   5B8D FD 7E 06      [19]  349 	ld	a, 6 (iy)
   5B90 B7            [ 4]  350 	or	a, a
                            351 ;src/entities/projectile.c:73: return;
   5B91 28 4C         [12]  352 	jr	Z,00104$
                            353 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5B93 6B            [ 4]  354 	ld	l, e
   5B94 62            [ 4]  355 	ld	h, d
   5B95 23            [ 6]  356 	inc	hl
   5B96 46            [ 7]  357 	ld	b, (hl)
   5B97 1A            [ 7]  358 	ld	a, (de)
   5B98 D5            [11]  359 	push	de
   5B99 C5            [11]  360 	push	bc
   5B9A 33            [ 6]  361 	inc	sp
   5B9B F5            [11]  362 	push	af
   5B9C 33            [ 6]  363 	inc	sp
   5B9D 21 00 C0      [10]  364 	ld	hl, #0xc000
   5BA0 E5            [11]  365 	push	hl
   5BA1 CD 4E 5E      [17]  366 	call	_cpct_getScreenPtr
   5BA4 4D            [ 4]  367 	ld	c, l
   5BA5 44            [ 4]  368 	ld	b, h
   5BA6 D1            [10]  369 	pop	de
                            370 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? 0x0F : (projectile->weapon == 1 ? 0x6B : 0x5A), projectile->w, projectile->h);
   5BA7 D5            [11]  371 	push	de
   5BA8 FD E1         [14]  372 	pop	iy
   5BAA FD 7E 05      [19]  373 	ld	a, 5 (iy)
   5BAD DD 77 FF      [19]  374 	ld	-1 (ix), a
   5BB0 D5            [11]  375 	push	de
   5BB1 FD E1         [14]  376 	pop	iy
   5BB3 FD 7E 04      [19]  377 	ld	a, 4 (iy)
   5BB6 DD 77 FE      [19]  378 	ld	-2 (ix), a
   5BB9 EB            [ 4]  379 	ex	de,hl
   5BBA 11 09 00      [10]  380 	ld	de, #0x0009
   5BBD 19            [11]  381 	add	hl, de
   5BBE 7E            [ 7]  382 	ld	a, (hl)
   5BBF B7            [ 4]  383 	or	a, a
   5BC0 20 04         [12]  384 	jr	NZ,00106$
   5BC2 16 0F         [ 7]  385 	ld	d, #0x0f
   5BC4 18 09         [12]  386 	jr	00107$
   5BC6                     387 00106$:
   5BC6 3D            [ 4]  388 	dec	a
   5BC7 20 04         [12]  389 	jr	NZ,00108$
   5BC9 16 6B         [ 7]  390 	ld	d, #0x6b
   5BCB 18 02         [12]  391 	jr	00109$
   5BCD                     392 00108$:
   5BCD 16 5A         [ 7]  393 	ld	d, #0x5a
   5BCF                     394 00109$:
   5BCF                     395 00107$:
   5BCF DD 66 FF      [19]  396 	ld	h, -1 (ix)
   5BD2 DD 6E FE      [19]  397 	ld	l, -2 (ix)
   5BD5 E5            [11]  398 	push	hl
   5BD6 D5            [11]  399 	push	de
   5BD7 33            [ 6]  400 	inc	sp
   5BD8 C5            [11]  401 	push	bc
   5BD9 CD 95 5D      [17]  402 	call	_cpct_drawSolidBox
   5BDC F1            [10]  403 	pop	af
   5BDD F1            [10]  404 	pop	af
   5BDE 33            [ 6]  405 	inc	sp
   5BDF                     406 00104$:
   5BDF DD F9         [10]  407 	ld	sp, ix
   5BE1 DD E1         [14]  408 	pop	ix
   5BE3 C9            [10]  409 	ret
                            410 	.area _CODE
                            411 	.area _INITIALIZER
                            412 	.area _CABS (ABS)
