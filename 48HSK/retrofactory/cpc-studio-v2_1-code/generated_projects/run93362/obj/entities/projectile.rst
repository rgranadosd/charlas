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
   593E                      52 _projectileinit::
                             53 ;src/entities/projectile.c:5: if (!projectile) {
   593E 21 03 00      [10]   54 	ld	hl, #2+1
   5941 39            [11]   55 	add	hl, sp
   5942 7E            [ 7]   56 	ld	a, (hl)
   5943 2B            [ 6]   57 	dec	hl
   5944 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:6: return;
   5945 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:9: projectile->x = 0;
   5946 D1            [10]   62 	pop	de
   5947 C1            [10]   63 	pop	bc
   5948 C5            [11]   64 	push	bc
   5949 D5            [11]   65 	push	de
   594A AF            [ 4]   66 	xor	a, a
   594B 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:10: projectile->y = 0;
   594C 59            [ 4]   69 	ld	e, c
   594D 50            [ 4]   70 	ld	d, b
   594E 13            [ 6]   71 	inc	de
   594F AF            [ 4]   72 	xor	a, a
   5950 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:11: projectile->vx = 0;
   5951 59            [ 4]   75 	ld	e, c
   5952 50            [ 4]   76 	ld	d, b
   5953 13            [ 6]   77 	inc	de
   5954 13            [ 6]   78 	inc	de
   5955 AF            [ 4]   79 	xor	a, a
   5956 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:12: projectile->vy = 0;
   5957 59            [ 4]   82 	ld	e, c
   5958 50            [ 4]   83 	ld	d, b
   5959 13            [ 6]   84 	inc	de
   595A 13            [ 6]   85 	inc	de
   595B 13            [ 6]   86 	inc	de
   595C AF            [ 4]   87 	xor	a, a
   595D 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:13: projectile->w = 2;
   595E 21 04 00      [10]   90 	ld	hl, #0x0004
   5961 09            [11]   91 	add	hl, bc
   5962 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:14: projectile->h = 2;
   5964 21 05 00      [10]   94 	ld	hl, #0x0005
   5967 09            [11]   95 	add	hl, bc
   5968 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:15: projectile->active = 0;
   596A 21 06 00      [10]   98 	ld	hl, #0x0006
   596D 09            [11]   99 	add	hl, bc
   596E 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:16: projectile->damage = 1;
   5970 21 07 00      [10]  102 	ld	hl, #0x0007
   5973 09            [11]  103 	add	hl, bc
   5974 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5976 21 08 00      [10]  106 	ld	hl, #0x0008
   5979 09            [11]  107 	add	hl, bc
   597A 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:18: projectile->weapon = 0;
   597C 21 09 00      [10]  110 	ld	hl, #0x0009
   597F 09            [11]  111 	add	hl, bc
   5980 36 00         [10]  112 	ld	(hl), #0x00
   5982 C9            [10]  113 	ret
                            114 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            115 ;	---------------------------------
                            116 ; Function projectilefire
                            117 ; ---------------------------------
   5983                     118 _projectilefire::
   5983 DD E5         [15]  119 	push	ix
   5985 DD 21 00 00   [14]  120 	ld	ix,#0
   5989 DD 39         [15]  121 	add	ix,sp
   598B F5            [11]  122 	push	af
   598C F5            [11]  123 	push	af
                            124 ;src/entities/projectile.c:22: if (!projectile) {
   598D DD 7E 05      [19]  125 	ld	a, 5 (ix)
   5990 DD B6 04      [19]  126 	or	a,4 (ix)
                            127 ;src/entities/projectile.c:23: return;
   5993 CA 35 5A      [10]  128 	jp	Z,00109$
                            129 ;src/entities/projectile.c:26: projectile->x = x;
   5996 DD 4E 04      [19]  130 	ld	c,4 (ix)
   5999 DD 46 05      [19]  131 	ld	b,5 (ix)
   599C DD 7E 06      [19]  132 	ld	a, 6 (ix)
   599F 02            [ 7]  133 	ld	(bc), a
                            134 ;src/entities/projectile.c:27: projectile->y = y;
   59A0 59            [ 4]  135 	ld	e, c
   59A1 50            [ 4]  136 	ld	d, b
   59A2 13            [ 6]  137 	inc	de
   59A3 DD 7E 07      [19]  138 	ld	a, 7 (ix)
   59A6 12            [ 7]  139 	ld	(de), a
                            140 ;src/entities/projectile.c:28: projectile->vx = dir;
   59A7 21 02 00      [10]  141 	ld	hl, #0x0002
   59AA 09            [11]  142 	add	hl,bc
   59AB DD 75 FE      [19]  143 	ld	-2 (ix), l
   59AE DD 74 FF      [19]  144 	ld	-1 (ix), h
   59B1 DD 7E 08      [19]  145 	ld	a, 8 (ix)
   59B4 77            [ 7]  146 	ld	(hl), a
                            147 ;src/entities/projectile.c:29: projectile->vy = 0;
   59B5 59            [ 4]  148 	ld	e, c
   59B6 50            [ 4]  149 	ld	d, b
   59B7 13            [ 6]  150 	inc	de
   59B8 13            [ 6]  151 	inc	de
   59B9 13            [ 6]  152 	inc	de
   59BA AF            [ 4]  153 	xor	a, a
   59BB 12            [ 7]  154 	ld	(de), a
                            155 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   59BC 21 09 00      [10]  156 	ld	hl, #0x0009
   59BF 09            [11]  157 	add	hl, bc
   59C0 DD 7E 09      [19]  158 	ld	a, 9 (ix)
   59C3 77            [ 7]  159 	ld	(hl), a
                            160 ;src/entities/projectile.c:31: projectile->active = 1;
   59C4 21 06 00      [10]  161 	ld	hl, #0x0006
   59C7 09            [11]  162 	add	hl, bc
   59C8 36 01         [10]  163 	ld	(hl), #0x01
                            164 ;src/entities/projectile.c:34: projectile->w = 3;
   59CA 21 04 00      [10]  165 	ld	hl, #0x0004
   59CD 09            [11]  166 	add	hl, bc
                            167 ;src/entities/projectile.c:35: projectile->h = 2;
   59CE 79            [ 4]  168 	ld	a, c
   59CF C6 05         [ 7]  169 	add	a, #0x05
   59D1 5F            [ 4]  170 	ld	e, a
   59D2 78            [ 4]  171 	ld	a, b
   59D3 CE 00         [ 7]  172 	adc	a, #0x00
   59D5 57            [ 4]  173 	ld	d, a
                            174 ;src/entities/projectile.c:36: projectile->damage = 1;
   59D6 79            [ 4]  175 	ld	a, c
   59D7 C6 07         [ 7]  176 	add	a, #0x07
   59D9 DD 77 FC      [19]  177 	ld	-4 (ix), a
   59DC 78            [ 4]  178 	ld	a, b
   59DD CE 00         [ 7]  179 	adc	a, #0x00
   59DF DD 77 FD      [19]  180 	ld	-3 (ix), a
                            181 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   59E2 79            [ 4]  182 	ld	a, c
   59E3 C6 08         [ 7]  183 	add	a, #0x08
   59E5 4F            [ 4]  184 	ld	c, a
   59E6 78            [ 4]  185 	ld	a, b
   59E7 CE 00         [ 7]  186 	adc	a, #0x00
   59E9 47            [ 4]  187 	ld	b, a
                            188 ;src/entities/projectile.c:33: if (weapon == 0) {
   59EA DD 7E 09      [19]  189 	ld	a, 9 (ix)
   59ED B7            [ 4]  190 	or	a, a
   59EE 20 0E         [12]  191 	jr	NZ,00107$
                            192 ;src/entities/projectile.c:34: projectile->w = 3;
   59F0 36 03         [10]  193 	ld	(hl), #0x03
                            194 ;src/entities/projectile.c:35: projectile->h = 2;
   59F2 3E 02         [ 7]  195 	ld	a, #0x02
   59F4 12            [ 7]  196 	ld	(de), a
                            197 ;src/entities/projectile.c:36: projectile->damage = 1;
   59F5 E1            [10]  198 	pop	hl
   59F6 E5            [11]  199 	push	hl
   59F7 36 01         [10]  200 	ld	(hl), #0x01
                            201 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   59F9 3E 2D         [ 7]  202 	ld	a, #0x2d
   59FB 02            [ 7]  203 	ld	(bc), a
   59FC 18 37         [12]  204 	jr	00109$
   59FE                     205 00107$:
                            206 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   59FE DD 7E 09      [19]  207 	ld	a, 9 (ix)
   5A01 3D            [ 4]  208 	dec	a
   5A02 20 0E         [12]  209 	jr	NZ,00104$
                            210 ;src/entities/projectile.c:39: projectile->w = 2;
   5A04 36 02         [10]  211 	ld	(hl), #0x02
                            212 ;src/entities/projectile.c:40: projectile->h = 3;
   5A06 3E 03         [ 7]  213 	ld	a, #0x03
   5A08 12            [ 7]  214 	ld	(de), a
                            215 ;src/entities/projectile.c:41: projectile->damage = 2;
   5A09 E1            [10]  216 	pop	hl
   5A0A E5            [11]  217 	push	hl
   5A0B 36 02         [10]  218 	ld	(hl), #0x02
                            219 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5A0D 3E 1C         [ 7]  220 	ld	a, #0x1c
   5A0F 02            [ 7]  221 	ld	(bc), a
   5A10 18 23         [12]  222 	jr	00109$
   5A12                     223 00104$:
                            224 ;src/entities/projectile.c:44: projectile->w = 4;
   5A12 36 04         [10]  225 	ld	(hl), #0x04
                            226 ;src/entities/projectile.c:45: projectile->h = 3;
   5A14 3E 03         [ 7]  227 	ld	a, #0x03
   5A16 12            [ 7]  228 	ld	(de), a
                            229 ;src/entities/projectile.c:46: projectile->damage = 3;
   5A17 E1            [10]  230 	pop	hl
   5A18 E5            [11]  231 	push	hl
   5A19 36 03         [10]  232 	ld	(hl), #0x03
                            233 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5A1B 3E 38         [ 7]  234 	ld	a, #0x38
   5A1D 02            [ 7]  235 	ld	(bc), a
                            236 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5A1E D1            [10]  237 	pop	de
   5A1F C1            [10]  238 	pop	bc
   5A20 C5            [11]  239 	push	bc
   5A21 D5            [11]  240 	push	de
   5A22 AF            [ 4]  241 	xor	a, a
   5A23 DD 96 08      [19]  242 	sub	a, 8 (ix)
   5A26 E2 2B 5A      [10]  243 	jp	PO, 00131$
   5A29 EE 80         [ 7]  244 	xor	a, #0x80
   5A2B                     245 00131$:
   5A2B F2 32 5A      [10]  246 	jp	P, 00111$
   5A2E 3E 04         [ 7]  247 	ld	a, #0x04
   5A30 18 02         [12]  248 	jr	00112$
   5A32                     249 00111$:
   5A32 3E FC         [ 7]  250 	ld	a, #0xfc
   5A34                     251 00112$:
   5A34 02            [ 7]  252 	ld	(bc), a
   5A35                     253 00109$:
   5A35 DD F9         [10]  254 	ld	sp, ix
   5A37 DD E1         [14]  255 	pop	ix
   5A39 C9            [10]  256 	ret
                            257 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            258 ;	---------------------------------
                            259 ; Function projectileupdate
                            260 ; ---------------------------------
   5A3A                     261 _projectileupdate::
   5A3A DD E5         [15]  262 	push	ix
   5A3C DD 21 00 00   [14]  263 	ld	ix,#0
   5A40 DD 39         [15]  264 	add	ix,sp
   5A42 3B            [ 6]  265 	dec	sp
                            266 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5A43 DD 7E 05      [19]  267 	ld	a, 5 (ix)
   5A46 DD B6 04      [19]  268 	or	a,4 (ix)
   5A49 28 4A         [12]  269 	jr	Z,00109$
   5A4B DD 5E 04      [19]  270 	ld	e,4 (ix)
   5A4E DD 56 05      [19]  271 	ld	d,5 (ix)
   5A51 FD 21 06 00   [14]  272 	ld	iy, #0x0006
   5A55 FD 19         [15]  273 	add	iy, de
   5A57 FD 7E 00      [19]  274 	ld	a, 0 (iy)
   5A5A B7            [ 4]  275 	or	a, a
                            276 ;src/entities/projectile.c:54: return;
   5A5B 28 38         [12]  277 	jr	Z,00109$
                            278 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5A5D 1A            [ 7]  279 	ld	a, (de)
   5A5E 4F            [ 4]  280 	ld	c, a
   5A5F 6B            [ 4]  281 	ld	l, e
   5A60 62            [ 4]  282 	ld	h, d
   5A61 23            [ 6]  283 	inc	hl
   5A62 23            [ 6]  284 	inc	hl
   5A63 6E            [ 7]  285 	ld	l, (hl)
   5A64 09            [11]  286 	add	hl, bc
   5A65 7D            [ 4]  287 	ld	a, l
   5A66 12            [ 7]  288 	ld	(de), a
                            289 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5A67 4B            [ 4]  290 	ld	c, e
   5A68 42            [ 4]  291 	ld	b, d
   5A69 03            [ 6]  292 	inc	bc
   5A6A 0A            [ 7]  293 	ld	a, (bc)
   5A6B DD 77 FF      [19]  294 	ld	-1 (ix), a
   5A6E 6B            [ 4]  295 	ld	l, e
   5A6F 62            [ 4]  296 	ld	h, d
   5A70 23            [ 6]  297 	inc	hl
   5A71 23            [ 6]  298 	inc	hl
   5A72 23            [ 6]  299 	inc	hl
   5A73 6E            [ 7]  300 	ld	l, (hl)
   5A74 DD 7E FF      [19]  301 	ld	a, -1 (ix)
   5A77 85            [ 4]  302 	add	a, l
   5A78 02            [ 7]  303 	ld	(bc), a
                            304 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5A79 21 08 00      [10]  305 	ld	hl, #0x0008
   5A7C 19            [11]  306 	add	hl,de
   5A7D 4D            [ 4]  307 	ld	c, l
   5A7E 44            [ 4]  308 	ld	b, h
   5A7F 0A            [ 7]  309 	ld	a, (bc)
   5A80 B7            [ 4]  310 	or	a, a
   5A81 28 03         [12]  311 	jr	Z,00105$
                            312 ;src/entities/projectile.c:61: projectile->lifetime--;
   5A83 C6 FF         [ 7]  313 	add	a, #0xff
   5A85 02            [ 7]  314 	ld	(bc), a
   5A86                     315 00105$:
                            316 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5A86 1A            [ 7]  317 	ld	a, (de)
   5A87 5F            [ 4]  318 	ld	e, a
   5A88 3E 4E         [ 7]  319 	ld	a, #0x4e
   5A8A 93            [ 4]  320 	sub	a, e
   5A8B 38 04         [12]  321 	jr	C,00106$
   5A8D 0A            [ 7]  322 	ld	a, (bc)
   5A8E B7            [ 4]  323 	or	a, a
   5A8F 20 04         [12]  324 	jr	NZ,00109$
   5A91                     325 00106$:
                            326 ;src/entities/projectile.c:65: projectile->active = 0;
   5A91 FD 36 00 00   [19]  327 	ld	0 (iy), #0x00
   5A95                     328 00109$:
   5A95 33            [ 6]  329 	inc	sp
   5A96 DD E1         [14]  330 	pop	ix
   5A98 C9            [10]  331 	ret
                            332 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            333 ;	---------------------------------
                            334 ; Function projectilerender
                            335 ; ---------------------------------
   5A99                     336 _projectilerender::
   5A99 DD E5         [15]  337 	push	ix
   5A9B DD 21 00 00   [14]  338 	ld	ix,#0
   5A9F DD 39         [15]  339 	add	ix,sp
   5AA1 F5            [11]  340 	push	af
                            341 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5AA2 DD 7E 05      [19]  342 	ld	a, 5 (ix)
   5AA5 DD B6 04      [19]  343 	or	a,4 (ix)
   5AA8 28 5B         [12]  344 	jr	Z,00104$
   5AAA DD 5E 04      [19]  345 	ld	e,4 (ix)
   5AAD DD 56 05      [19]  346 	ld	d,5 (ix)
   5AB0 D5            [11]  347 	push	de
   5AB1 FD E1         [14]  348 	pop	iy
   5AB3 FD 7E 06      [19]  349 	ld	a, 6 (iy)
   5AB6 B7            [ 4]  350 	or	a, a
                            351 ;src/entities/projectile.c:73: return;
   5AB7 28 4C         [12]  352 	jr	Z,00104$
                            353 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5AB9 6B            [ 4]  354 	ld	l, e
   5ABA 62            [ 4]  355 	ld	h, d
   5ABB 23            [ 6]  356 	inc	hl
   5ABC 46            [ 7]  357 	ld	b, (hl)
   5ABD 1A            [ 7]  358 	ld	a, (de)
   5ABE D5            [11]  359 	push	de
   5ABF C5            [11]  360 	push	bc
   5AC0 33            [ 6]  361 	inc	sp
   5AC1 F5            [11]  362 	push	af
   5AC2 33            [ 6]  363 	inc	sp
   5AC3 21 00 C0      [10]  364 	ld	hl, #0xc000
   5AC6 E5            [11]  365 	push	hl
   5AC7 CD 74 5D      [17]  366 	call	_cpct_getScreenPtr
   5ACA 4D            [ 4]  367 	ld	c, l
   5ACB 44            [ 4]  368 	ld	b, h
   5ACC D1            [10]  369 	pop	de
                            370 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? 0x0F : (projectile->weapon == 1 ? 0x6B : 0x5A), projectile->w, projectile->h);
   5ACD D5            [11]  371 	push	de
   5ACE FD E1         [14]  372 	pop	iy
   5AD0 FD 7E 05      [19]  373 	ld	a, 5 (iy)
   5AD3 DD 77 FF      [19]  374 	ld	-1 (ix), a
   5AD6 D5            [11]  375 	push	de
   5AD7 FD E1         [14]  376 	pop	iy
   5AD9 FD 7E 04      [19]  377 	ld	a, 4 (iy)
   5ADC DD 77 FE      [19]  378 	ld	-2 (ix), a
   5ADF EB            [ 4]  379 	ex	de,hl
   5AE0 11 09 00      [10]  380 	ld	de, #0x0009
   5AE3 19            [11]  381 	add	hl, de
   5AE4 7E            [ 7]  382 	ld	a, (hl)
   5AE5 B7            [ 4]  383 	or	a, a
   5AE6 20 04         [12]  384 	jr	NZ,00106$
   5AE8 16 0F         [ 7]  385 	ld	d, #0x0f
   5AEA 18 09         [12]  386 	jr	00107$
   5AEC                     387 00106$:
   5AEC 3D            [ 4]  388 	dec	a
   5AED 20 04         [12]  389 	jr	NZ,00108$
   5AEF 16 6B         [ 7]  390 	ld	d, #0x6b
   5AF1 18 02         [12]  391 	jr	00109$
   5AF3                     392 00108$:
   5AF3 16 5A         [ 7]  393 	ld	d, #0x5a
   5AF5                     394 00109$:
   5AF5                     395 00107$:
   5AF5 DD 66 FF      [19]  396 	ld	h, -1 (ix)
   5AF8 DD 6E FE      [19]  397 	ld	l, -2 (ix)
   5AFB E5            [11]  398 	push	hl
   5AFC D5            [11]  399 	push	de
   5AFD 33            [ 6]  400 	inc	sp
   5AFE C5            [11]  401 	push	bc
   5AFF CD BB 5C      [17]  402 	call	_cpct_drawSolidBox
   5B02 F1            [10]  403 	pop	af
   5B03 F1            [10]  404 	pop	af
   5B04 33            [ 6]  405 	inc	sp
   5B05                     406 00104$:
   5B05 DD F9         [10]  407 	ld	sp, ix
   5B07 DD E1         [14]  408 	pop	ix
   5B09 C9            [10]  409 	ret
                            410 	.area _CODE
                            411 	.area _INITIALIZER
                            412 	.area _CABS (ABS)
