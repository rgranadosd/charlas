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
                             13 	.globl _cpct_px2byteM0
                             14 	.globl _projectileinit
                             15 	.globl _projectilefire
                             16 	.globl _projectileupdate
                             17 	.globl _projectilerender
                             18 ;--------------------------------------------------------
                             19 ; special function registers
                             20 ;--------------------------------------------------------
                             21 ;--------------------------------------------------------
                             22 ; ram data
                             23 ;--------------------------------------------------------
                             24 	.area _DATA
                             25 ;--------------------------------------------------------
                             26 ; ram data
                             27 ;--------------------------------------------------------
                             28 	.area _INITIALIZED
                             29 ;--------------------------------------------------------
                             30 ; absolute external ram data
                             31 ;--------------------------------------------------------
                             32 	.area _DABS (ABS)
                             33 ;--------------------------------------------------------
                             34 ; global & static initialisations
                             35 ;--------------------------------------------------------
                             36 	.area _HOME
                             37 	.area _GSINIT
                             38 	.area _GSFINAL
                             39 	.area _GSINIT
                             40 ;--------------------------------------------------------
                             41 ; Home
                             42 ;--------------------------------------------------------
                             43 	.area _HOME
                             44 	.area _HOME
                             45 ;--------------------------------------------------------
                             46 ; code
                             47 ;--------------------------------------------------------
                             48 	.area _CODE
                             49 ;src/entities/projectile.c:4: void projectileinit(Projectile* projectile) {
                             50 ;	---------------------------------
                             51 ; Function projectileinit
                             52 ; ---------------------------------
   59F2                      53 _projectileinit::
                             54 ;src/entities/projectile.c:5: if (!projectile) {
   59F2 21 03 00      [10]   55 	ld	hl, #2+1
   59F5 39            [11]   56 	add	hl, sp
   59F6 7E            [ 7]   57 	ld	a, (hl)
   59F7 2B            [ 6]   58 	dec	hl
   59F8 B6            [ 7]   59 	or	a,(hl)
                             60 ;src/entities/projectile.c:6: return;
   59F9 C8            [11]   61 	ret	Z
                             62 ;src/entities/projectile.c:9: projectile->x = 0;
   59FA D1            [10]   63 	pop	de
   59FB C1            [10]   64 	pop	bc
   59FC C5            [11]   65 	push	bc
   59FD D5            [11]   66 	push	de
   59FE AF            [ 4]   67 	xor	a, a
   59FF 02            [ 7]   68 	ld	(bc), a
                             69 ;src/entities/projectile.c:10: projectile->y = 0;
   5A00 59            [ 4]   70 	ld	e, c
   5A01 50            [ 4]   71 	ld	d, b
   5A02 13            [ 6]   72 	inc	de
   5A03 AF            [ 4]   73 	xor	a, a
   5A04 12            [ 7]   74 	ld	(de), a
                             75 ;src/entities/projectile.c:11: projectile->vx = 0;
   5A05 59            [ 4]   76 	ld	e, c
   5A06 50            [ 4]   77 	ld	d, b
   5A07 13            [ 6]   78 	inc	de
   5A08 13            [ 6]   79 	inc	de
   5A09 AF            [ 4]   80 	xor	a, a
   5A0A 12            [ 7]   81 	ld	(de), a
                             82 ;src/entities/projectile.c:12: projectile->vy = 0;
   5A0B 59            [ 4]   83 	ld	e, c
   5A0C 50            [ 4]   84 	ld	d, b
   5A0D 13            [ 6]   85 	inc	de
   5A0E 13            [ 6]   86 	inc	de
   5A0F 13            [ 6]   87 	inc	de
   5A10 AF            [ 4]   88 	xor	a, a
   5A11 12            [ 7]   89 	ld	(de), a
                             90 ;src/entities/projectile.c:13: projectile->w = 2;
   5A12 21 04 00      [10]   91 	ld	hl, #0x0004
   5A15 09            [11]   92 	add	hl, bc
   5A16 36 02         [10]   93 	ld	(hl), #0x02
                             94 ;src/entities/projectile.c:14: projectile->h = 2;
   5A18 21 05 00      [10]   95 	ld	hl, #0x0005
   5A1B 09            [11]   96 	add	hl, bc
   5A1C 36 02         [10]   97 	ld	(hl), #0x02
                             98 ;src/entities/projectile.c:15: projectile->active = 0;
   5A1E 21 06 00      [10]   99 	ld	hl, #0x0006
   5A21 09            [11]  100 	add	hl, bc
   5A22 36 00         [10]  101 	ld	(hl), #0x00
                            102 ;src/entities/projectile.c:16: projectile->damage = 1;
   5A24 21 07 00      [10]  103 	ld	hl, #0x0007
   5A27 09            [11]  104 	add	hl, bc
   5A28 36 01         [10]  105 	ld	(hl), #0x01
                            106 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5A2A 21 08 00      [10]  107 	ld	hl, #0x0008
   5A2D 09            [11]  108 	add	hl, bc
   5A2E 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5A30 21 09 00      [10]  111 	ld	hl, #0x0009
   5A33 09            [11]  112 	add	hl, bc
   5A34 36 00         [10]  113 	ld	(hl), #0x00
   5A36 C9            [10]  114 	ret
                            115 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            116 ;	---------------------------------
                            117 ; Function projectilefire
                            118 ; ---------------------------------
   5A37                     119 _projectilefire::
   5A37 DD E5         [15]  120 	push	ix
   5A39 DD 21 00 00   [14]  121 	ld	ix,#0
   5A3D DD 39         [15]  122 	add	ix,sp
   5A3F F5            [11]  123 	push	af
   5A40 F5            [11]  124 	push	af
                            125 ;src/entities/projectile.c:22: if (!projectile) {
   5A41 DD 7E 05      [19]  126 	ld	a, 5 (ix)
   5A44 DD B6 04      [19]  127 	or	a,4 (ix)
                            128 ;src/entities/projectile.c:23: return;
   5A47 CA E9 5A      [10]  129 	jp	Z,00109$
                            130 ;src/entities/projectile.c:26: projectile->x = x;
   5A4A DD 4E 04      [19]  131 	ld	c,4 (ix)
   5A4D DD 46 05      [19]  132 	ld	b,5 (ix)
   5A50 DD 7E 06      [19]  133 	ld	a, 6 (ix)
   5A53 02            [ 7]  134 	ld	(bc), a
                            135 ;src/entities/projectile.c:27: projectile->y = y;
   5A54 59            [ 4]  136 	ld	e, c
   5A55 50            [ 4]  137 	ld	d, b
   5A56 13            [ 6]  138 	inc	de
   5A57 DD 7E 07      [19]  139 	ld	a, 7 (ix)
   5A5A 12            [ 7]  140 	ld	(de), a
                            141 ;src/entities/projectile.c:28: projectile->vx = dir;
   5A5B 21 02 00      [10]  142 	ld	hl, #0x0002
   5A5E 09            [11]  143 	add	hl,bc
   5A5F DD 75 FE      [19]  144 	ld	-2 (ix), l
   5A62 DD 74 FF      [19]  145 	ld	-1 (ix), h
   5A65 DD 7E 08      [19]  146 	ld	a, 8 (ix)
   5A68 77            [ 7]  147 	ld	(hl), a
                            148 ;src/entities/projectile.c:29: projectile->vy = 0;
   5A69 59            [ 4]  149 	ld	e, c
   5A6A 50            [ 4]  150 	ld	d, b
   5A6B 13            [ 6]  151 	inc	de
   5A6C 13            [ 6]  152 	inc	de
   5A6D 13            [ 6]  153 	inc	de
   5A6E AF            [ 4]  154 	xor	a, a
   5A6F 12            [ 7]  155 	ld	(de), a
                            156 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5A70 21 09 00      [10]  157 	ld	hl, #0x0009
   5A73 09            [11]  158 	add	hl, bc
   5A74 DD 7E 09      [19]  159 	ld	a, 9 (ix)
   5A77 77            [ 7]  160 	ld	(hl), a
                            161 ;src/entities/projectile.c:31: projectile->active = 1;
   5A78 21 06 00      [10]  162 	ld	hl, #0x0006
   5A7B 09            [11]  163 	add	hl, bc
   5A7C 36 01         [10]  164 	ld	(hl), #0x01
                            165 ;src/entities/projectile.c:34: projectile->w = 3;
   5A7E 21 04 00      [10]  166 	ld	hl, #0x0004
   5A81 09            [11]  167 	add	hl, bc
                            168 ;src/entities/projectile.c:35: projectile->h = 2;
   5A82 79            [ 4]  169 	ld	a, c
   5A83 C6 05         [ 7]  170 	add	a, #0x05
   5A85 5F            [ 4]  171 	ld	e, a
   5A86 78            [ 4]  172 	ld	a, b
   5A87 CE 00         [ 7]  173 	adc	a, #0x00
   5A89 57            [ 4]  174 	ld	d, a
                            175 ;src/entities/projectile.c:36: projectile->damage = 1;
   5A8A 79            [ 4]  176 	ld	a, c
   5A8B C6 07         [ 7]  177 	add	a, #0x07
   5A8D DD 77 FC      [19]  178 	ld	-4 (ix), a
   5A90 78            [ 4]  179 	ld	a, b
   5A91 CE 00         [ 7]  180 	adc	a, #0x00
   5A93 DD 77 FD      [19]  181 	ld	-3 (ix), a
                            182 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5A96 79            [ 4]  183 	ld	a, c
   5A97 C6 08         [ 7]  184 	add	a, #0x08
   5A99 4F            [ 4]  185 	ld	c, a
   5A9A 78            [ 4]  186 	ld	a, b
   5A9B CE 00         [ 7]  187 	adc	a, #0x00
   5A9D 47            [ 4]  188 	ld	b, a
                            189 ;src/entities/projectile.c:33: if (weapon == 0) {
   5A9E DD 7E 09      [19]  190 	ld	a, 9 (ix)
   5AA1 B7            [ 4]  191 	or	a, a
   5AA2 20 0E         [12]  192 	jr	NZ,00107$
                            193 ;src/entities/projectile.c:34: projectile->w = 3;
   5AA4 36 03         [10]  194 	ld	(hl), #0x03
                            195 ;src/entities/projectile.c:35: projectile->h = 2;
   5AA6 3E 02         [ 7]  196 	ld	a, #0x02
   5AA8 12            [ 7]  197 	ld	(de), a
                            198 ;src/entities/projectile.c:36: projectile->damage = 1;
   5AA9 E1            [10]  199 	pop	hl
   5AAA E5            [11]  200 	push	hl
   5AAB 36 01         [10]  201 	ld	(hl), #0x01
                            202 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AAD 3E 2D         [ 7]  203 	ld	a, #0x2d
   5AAF 02            [ 7]  204 	ld	(bc), a
   5AB0 18 37         [12]  205 	jr	00109$
   5AB2                     206 00107$:
                            207 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5AB2 DD 7E 09      [19]  208 	ld	a, 9 (ix)
   5AB5 3D            [ 4]  209 	dec	a
   5AB6 20 0E         [12]  210 	jr	NZ,00104$
                            211 ;src/entities/projectile.c:39: projectile->w = 2;
   5AB8 36 02         [10]  212 	ld	(hl), #0x02
                            213 ;src/entities/projectile.c:40: projectile->h = 3;
   5ABA 3E 03         [ 7]  214 	ld	a, #0x03
   5ABC 12            [ 7]  215 	ld	(de), a
                            216 ;src/entities/projectile.c:41: projectile->damage = 2;
   5ABD E1            [10]  217 	pop	hl
   5ABE E5            [11]  218 	push	hl
   5ABF 36 02         [10]  219 	ld	(hl), #0x02
                            220 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5AC1 3E 1C         [ 7]  221 	ld	a, #0x1c
   5AC3 02            [ 7]  222 	ld	(bc), a
   5AC4 18 23         [12]  223 	jr	00109$
   5AC6                     224 00104$:
                            225 ;src/entities/projectile.c:44: projectile->w = 4;
   5AC6 36 04         [10]  226 	ld	(hl), #0x04
                            227 ;src/entities/projectile.c:45: projectile->h = 3;
   5AC8 3E 03         [ 7]  228 	ld	a, #0x03
   5ACA 12            [ 7]  229 	ld	(de), a
                            230 ;src/entities/projectile.c:46: projectile->damage = 3;
   5ACB E1            [10]  231 	pop	hl
   5ACC E5            [11]  232 	push	hl
   5ACD 36 03         [10]  233 	ld	(hl), #0x03
                            234 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5ACF 3E 38         [ 7]  235 	ld	a, #0x38
   5AD1 02            [ 7]  236 	ld	(bc), a
                            237 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5AD2 D1            [10]  238 	pop	de
   5AD3 C1            [10]  239 	pop	bc
   5AD4 C5            [11]  240 	push	bc
   5AD5 D5            [11]  241 	push	de
   5AD6 AF            [ 4]  242 	xor	a, a
   5AD7 DD 96 08      [19]  243 	sub	a, 8 (ix)
   5ADA E2 DF 5A      [10]  244 	jp	PO, 00131$
   5ADD EE 80         [ 7]  245 	xor	a, #0x80
   5ADF                     246 00131$:
   5ADF F2 E6 5A      [10]  247 	jp	P, 00111$
   5AE2 3E 04         [ 7]  248 	ld	a, #0x04
   5AE4 18 02         [12]  249 	jr	00112$
   5AE6                     250 00111$:
   5AE6 3E FC         [ 7]  251 	ld	a, #0xfc
   5AE8                     252 00112$:
   5AE8 02            [ 7]  253 	ld	(bc), a
   5AE9                     254 00109$:
   5AE9 DD F9         [10]  255 	ld	sp, ix
   5AEB DD E1         [14]  256 	pop	ix
   5AED C9            [10]  257 	ret
                            258 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            259 ;	---------------------------------
                            260 ; Function projectileupdate
                            261 ; ---------------------------------
   5AEE                     262 _projectileupdate::
   5AEE DD E5         [15]  263 	push	ix
   5AF0 DD 21 00 00   [14]  264 	ld	ix,#0
   5AF4 DD 39         [15]  265 	add	ix,sp
   5AF6 3B            [ 6]  266 	dec	sp
                            267 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5AF7 DD 7E 05      [19]  268 	ld	a, 5 (ix)
   5AFA DD B6 04      [19]  269 	or	a,4 (ix)
   5AFD 28 4A         [12]  270 	jr	Z,00109$
   5AFF DD 5E 04      [19]  271 	ld	e,4 (ix)
   5B02 DD 56 05      [19]  272 	ld	d,5 (ix)
   5B05 FD 21 06 00   [14]  273 	ld	iy, #0x0006
   5B09 FD 19         [15]  274 	add	iy, de
   5B0B FD 7E 00      [19]  275 	ld	a, 0 (iy)
   5B0E B7            [ 4]  276 	or	a, a
                            277 ;src/entities/projectile.c:54: return;
   5B0F 28 38         [12]  278 	jr	Z,00109$
                            279 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5B11 1A            [ 7]  280 	ld	a, (de)
   5B12 4F            [ 4]  281 	ld	c, a
   5B13 6B            [ 4]  282 	ld	l, e
   5B14 62            [ 4]  283 	ld	h, d
   5B15 23            [ 6]  284 	inc	hl
   5B16 23            [ 6]  285 	inc	hl
   5B17 6E            [ 7]  286 	ld	l, (hl)
   5B18 09            [11]  287 	add	hl, bc
   5B19 7D            [ 4]  288 	ld	a, l
   5B1A 12            [ 7]  289 	ld	(de), a
                            290 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5B1B 4B            [ 4]  291 	ld	c, e
   5B1C 42            [ 4]  292 	ld	b, d
   5B1D 03            [ 6]  293 	inc	bc
   5B1E 0A            [ 7]  294 	ld	a, (bc)
   5B1F DD 77 FF      [19]  295 	ld	-1 (ix), a
   5B22 6B            [ 4]  296 	ld	l, e
   5B23 62            [ 4]  297 	ld	h, d
   5B24 23            [ 6]  298 	inc	hl
   5B25 23            [ 6]  299 	inc	hl
   5B26 23            [ 6]  300 	inc	hl
   5B27 6E            [ 7]  301 	ld	l, (hl)
   5B28 DD 7E FF      [19]  302 	ld	a, -1 (ix)
   5B2B 85            [ 4]  303 	add	a, l
   5B2C 02            [ 7]  304 	ld	(bc), a
                            305 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5B2D 21 08 00      [10]  306 	ld	hl, #0x0008
   5B30 19            [11]  307 	add	hl,de
   5B31 4D            [ 4]  308 	ld	c, l
   5B32 44            [ 4]  309 	ld	b, h
   5B33 0A            [ 7]  310 	ld	a, (bc)
   5B34 B7            [ 4]  311 	or	a, a
   5B35 28 03         [12]  312 	jr	Z,00105$
                            313 ;src/entities/projectile.c:61: projectile->lifetime--;
   5B37 C6 FF         [ 7]  314 	add	a, #0xff
   5B39 02            [ 7]  315 	ld	(bc), a
   5B3A                     316 00105$:
                            317 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5B3A 1A            [ 7]  318 	ld	a, (de)
   5B3B 5F            [ 4]  319 	ld	e, a
   5B3C 3E 4E         [ 7]  320 	ld	a, #0x4e
   5B3E 93            [ 4]  321 	sub	a, e
   5B3F 38 04         [12]  322 	jr	C,00106$
   5B41 0A            [ 7]  323 	ld	a, (bc)
   5B42 B7            [ 4]  324 	or	a, a
   5B43 20 04         [12]  325 	jr	NZ,00109$
   5B45                     326 00106$:
                            327 ;src/entities/projectile.c:65: projectile->active = 0;
   5B45 FD 36 00 00   [19]  328 	ld	0 (iy), #0x00
   5B49                     329 00109$:
   5B49 33            [ 6]  330 	inc	sp
   5B4A DD E1         [14]  331 	pop	ix
   5B4C C9            [10]  332 	ret
                            333 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            334 ;	---------------------------------
                            335 ; Function projectilerender
                            336 ; ---------------------------------
   5B4D                     337 _projectilerender::
   5B4D DD E5         [15]  338 	push	ix
   5B4F DD 21 00 00   [14]  339 	ld	ix,#0
   5B53 DD 39         [15]  340 	add	ix,sp
   5B55 F5            [11]  341 	push	af
                            342 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5B56 DD 7E 05      [19]  343 	ld	a, 5 (ix)
   5B59 DD B6 04      [19]  344 	or	a,4 (ix)
   5B5C 28 72         [12]  345 	jr	Z,00104$
   5B5E DD 5E 04      [19]  346 	ld	e,4 (ix)
   5B61 DD 56 05      [19]  347 	ld	d,5 (ix)
   5B64 D5            [11]  348 	push	de
   5B65 FD E1         [14]  349 	pop	iy
   5B67 FD 7E 06      [19]  350 	ld	a, 6 (iy)
   5B6A B7            [ 4]  351 	or	a, a
                            352 ;src/entities/projectile.c:73: return;
   5B6B 28 63         [12]  353 	jr	Z,00104$
                            354 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5B6D 6B            [ 4]  355 	ld	l, e
   5B6E 62            [ 4]  356 	ld	h, d
   5B6F 23            [ 6]  357 	inc	hl
   5B70 46            [ 7]  358 	ld	b, (hl)
   5B71 1A            [ 7]  359 	ld	a, (de)
   5B72 D5            [11]  360 	push	de
   5B73 C5            [11]  361 	push	bc
   5B74 33            [ 6]  362 	inc	sp
   5B75 F5            [11]  363 	push	af
   5B76 33            [ 6]  364 	inc	sp
   5B77 21 00 C0      [10]  365 	ld	hl, #0xc000
   5B7A E5            [11]  366 	push	hl
   5B7B CD 7E 5E      [17]  367 	call	_cpct_getScreenPtr
   5B7E 4D            [ 4]  368 	ld	c, l
   5B7F 44            [ 4]  369 	ld	b, h
   5B80 D1            [10]  370 	pop	de
                            371 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? cpct_px2byteM0(15, 15) : (projectile->weapon == 1 ? cpct_px2byteM0(11, 11) : cpct_px2byteM0(5, 5)), projectile->w, projectile->h);
   5B81 D5            [11]  372 	push	de
   5B82 FD E1         [14]  373 	pop	iy
   5B84 FD 7E 05      [19]  374 	ld	a, 5 (iy)
   5B87 DD 77 FF      [19]  375 	ld	-1 (ix), a
   5B8A D5            [11]  376 	push	de
   5B8B FD E1         [14]  377 	pop	iy
   5B8D FD 7E 04      [19]  378 	ld	a, 4 (iy)
   5B90 DD 77 FE      [19]  379 	ld	-2 (ix), a
   5B93 EB            [ 4]  380 	ex	de,hl
   5B94 11 09 00      [10]  381 	ld	de, #0x0009
   5B97 19            [11]  382 	add	hl, de
   5B98 7E            [ 7]  383 	ld	a, (hl)
   5B99 B7            [ 4]  384 	or	a, a
   5B9A 20 0C         [12]  385 	jr	NZ,00106$
   5B9C C5            [11]  386 	push	bc
   5B9D 21 0F 0F      [10]  387 	ld	hl, #0x0f0f
   5BA0 E5            [11]  388 	push	hl
   5BA1 CD 8B 5D      [17]  389 	call	_cpct_px2byteM0
   5BA4 55            [ 4]  390 	ld	d, l
   5BA5 C1            [10]  391 	pop	bc
   5BA6 18 18         [12]  392 	jr	00107$
   5BA8                     393 00106$:
   5BA8 3D            [ 4]  394 	dec	a
   5BA9 20 0B         [12]  395 	jr	NZ,00108$
   5BAB C5            [11]  396 	push	bc
   5BAC 21 0B 0B      [10]  397 	ld	hl, #0x0b0b
   5BAF E5            [11]  398 	push	hl
   5BB0 CD 8B 5D      [17]  399 	call	_cpct_px2byteM0
   5BB3 C1            [10]  400 	pop	bc
   5BB4 18 09         [12]  401 	jr	00109$
   5BB6                     402 00108$:
   5BB6 C5            [11]  403 	push	bc
   5BB7 21 05 05      [10]  404 	ld	hl, #0x0505
   5BBA E5            [11]  405 	push	hl
   5BBB CD 8B 5D      [17]  406 	call	_cpct_px2byteM0
   5BBE C1            [10]  407 	pop	bc
   5BBF                     408 00109$:
   5BBF 55            [ 4]  409 	ld	d, l
   5BC0                     410 00107$:
   5BC0 DD 66 FF      [19]  411 	ld	h, -1 (ix)
   5BC3 DD 6E FE      [19]  412 	ld	l, -2 (ix)
   5BC6 E5            [11]  413 	push	hl
   5BC7 D5            [11]  414 	push	de
   5BC8 33            [ 6]  415 	inc	sp
   5BC9 C5            [11]  416 	push	bc
   5BCA CD C5 5D      [17]  417 	call	_cpct_drawSolidBox
   5BCD F1            [10]  418 	pop	af
   5BCE F1            [10]  419 	pop	af
   5BCF 33            [ 6]  420 	inc	sp
   5BD0                     421 00104$:
   5BD0 DD F9         [10]  422 	ld	sp, ix
   5BD2 DD E1         [14]  423 	pop	ix
   5BD4 C9            [10]  424 	ret
                            425 	.area _CODE
                            426 	.area _INITIALIZER
                            427 	.area _CABS (ABS)
