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
   59D6                      53 _projectileinit::
                             54 ;src/entities/projectile.c:5: if (!projectile) {
   59D6 21 03 00      [10]   55 	ld	hl, #2+1
   59D9 39            [11]   56 	add	hl, sp
   59DA 7E            [ 7]   57 	ld	a, (hl)
   59DB 2B            [ 6]   58 	dec	hl
   59DC B6            [ 7]   59 	or	a,(hl)
                             60 ;src/entities/projectile.c:6: return;
   59DD C8            [11]   61 	ret	Z
                             62 ;src/entities/projectile.c:9: projectile->x = 0;
   59DE D1            [10]   63 	pop	de
   59DF C1            [10]   64 	pop	bc
   59E0 C5            [11]   65 	push	bc
   59E1 D5            [11]   66 	push	de
   59E2 AF            [ 4]   67 	xor	a, a
   59E3 02            [ 7]   68 	ld	(bc), a
                             69 ;src/entities/projectile.c:10: projectile->y = 0;
   59E4 59            [ 4]   70 	ld	e, c
   59E5 50            [ 4]   71 	ld	d, b
   59E6 13            [ 6]   72 	inc	de
   59E7 AF            [ 4]   73 	xor	a, a
   59E8 12            [ 7]   74 	ld	(de), a
                             75 ;src/entities/projectile.c:11: projectile->vx = 0;
   59E9 59            [ 4]   76 	ld	e, c
   59EA 50            [ 4]   77 	ld	d, b
   59EB 13            [ 6]   78 	inc	de
   59EC 13            [ 6]   79 	inc	de
   59ED AF            [ 4]   80 	xor	a, a
   59EE 12            [ 7]   81 	ld	(de), a
                             82 ;src/entities/projectile.c:12: projectile->vy = 0;
   59EF 59            [ 4]   83 	ld	e, c
   59F0 50            [ 4]   84 	ld	d, b
   59F1 13            [ 6]   85 	inc	de
   59F2 13            [ 6]   86 	inc	de
   59F3 13            [ 6]   87 	inc	de
   59F4 AF            [ 4]   88 	xor	a, a
   59F5 12            [ 7]   89 	ld	(de), a
                             90 ;src/entities/projectile.c:13: projectile->w = 2;
   59F6 21 04 00      [10]   91 	ld	hl, #0x0004
   59F9 09            [11]   92 	add	hl, bc
   59FA 36 02         [10]   93 	ld	(hl), #0x02
                             94 ;src/entities/projectile.c:14: projectile->h = 2;
   59FC 21 05 00      [10]   95 	ld	hl, #0x0005
   59FF 09            [11]   96 	add	hl, bc
   5A00 36 02         [10]   97 	ld	(hl), #0x02
                             98 ;src/entities/projectile.c:15: projectile->active = 0;
   5A02 21 06 00      [10]   99 	ld	hl, #0x0006
   5A05 09            [11]  100 	add	hl, bc
   5A06 36 00         [10]  101 	ld	(hl), #0x00
                            102 ;src/entities/projectile.c:16: projectile->damage = 1;
   5A08 21 07 00      [10]  103 	ld	hl, #0x0007
   5A0B 09            [11]  104 	add	hl, bc
   5A0C 36 01         [10]  105 	ld	(hl), #0x01
                            106 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5A0E 21 08 00      [10]  107 	ld	hl, #0x0008
   5A11 09            [11]  108 	add	hl, bc
   5A12 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5A14 21 09 00      [10]  111 	ld	hl, #0x0009
   5A17 09            [11]  112 	add	hl, bc
   5A18 36 00         [10]  113 	ld	(hl), #0x00
   5A1A C9            [10]  114 	ret
                            115 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            116 ;	---------------------------------
                            117 ; Function projectilefire
                            118 ; ---------------------------------
   5A1B                     119 _projectilefire::
   5A1B DD E5         [15]  120 	push	ix
   5A1D DD 21 00 00   [14]  121 	ld	ix,#0
   5A21 DD 39         [15]  122 	add	ix,sp
   5A23 F5            [11]  123 	push	af
   5A24 F5            [11]  124 	push	af
                            125 ;src/entities/projectile.c:22: if (!projectile) {
   5A25 DD 7E 05      [19]  126 	ld	a, 5 (ix)
   5A28 DD B6 04      [19]  127 	or	a,4 (ix)
                            128 ;src/entities/projectile.c:23: return;
   5A2B CA CD 5A      [10]  129 	jp	Z,00109$
                            130 ;src/entities/projectile.c:26: projectile->x = x;
   5A2E DD 4E 04      [19]  131 	ld	c,4 (ix)
   5A31 DD 46 05      [19]  132 	ld	b,5 (ix)
   5A34 DD 7E 06      [19]  133 	ld	a, 6 (ix)
   5A37 02            [ 7]  134 	ld	(bc), a
                            135 ;src/entities/projectile.c:27: projectile->y = y;
   5A38 59            [ 4]  136 	ld	e, c
   5A39 50            [ 4]  137 	ld	d, b
   5A3A 13            [ 6]  138 	inc	de
   5A3B DD 7E 07      [19]  139 	ld	a, 7 (ix)
   5A3E 12            [ 7]  140 	ld	(de), a
                            141 ;src/entities/projectile.c:28: projectile->vx = dir;
   5A3F 21 02 00      [10]  142 	ld	hl, #0x0002
   5A42 09            [11]  143 	add	hl,bc
   5A43 DD 75 FE      [19]  144 	ld	-2 (ix), l
   5A46 DD 74 FF      [19]  145 	ld	-1 (ix), h
   5A49 DD 7E 08      [19]  146 	ld	a, 8 (ix)
   5A4C 77            [ 7]  147 	ld	(hl), a
                            148 ;src/entities/projectile.c:29: projectile->vy = 0;
   5A4D 59            [ 4]  149 	ld	e, c
   5A4E 50            [ 4]  150 	ld	d, b
   5A4F 13            [ 6]  151 	inc	de
   5A50 13            [ 6]  152 	inc	de
   5A51 13            [ 6]  153 	inc	de
   5A52 AF            [ 4]  154 	xor	a, a
   5A53 12            [ 7]  155 	ld	(de), a
                            156 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5A54 21 09 00      [10]  157 	ld	hl, #0x0009
   5A57 09            [11]  158 	add	hl, bc
   5A58 DD 7E 09      [19]  159 	ld	a, 9 (ix)
   5A5B 77            [ 7]  160 	ld	(hl), a
                            161 ;src/entities/projectile.c:31: projectile->active = 1;
   5A5C 21 06 00      [10]  162 	ld	hl, #0x0006
   5A5F 09            [11]  163 	add	hl, bc
   5A60 36 01         [10]  164 	ld	(hl), #0x01
                            165 ;src/entities/projectile.c:34: projectile->w = 3;
   5A62 21 04 00      [10]  166 	ld	hl, #0x0004
   5A65 09            [11]  167 	add	hl, bc
                            168 ;src/entities/projectile.c:35: projectile->h = 2;
   5A66 79            [ 4]  169 	ld	a, c
   5A67 C6 05         [ 7]  170 	add	a, #0x05
   5A69 5F            [ 4]  171 	ld	e, a
   5A6A 78            [ 4]  172 	ld	a, b
   5A6B CE 00         [ 7]  173 	adc	a, #0x00
   5A6D 57            [ 4]  174 	ld	d, a
                            175 ;src/entities/projectile.c:36: projectile->damage = 1;
   5A6E 79            [ 4]  176 	ld	a, c
   5A6F C6 07         [ 7]  177 	add	a, #0x07
   5A71 DD 77 FC      [19]  178 	ld	-4 (ix), a
   5A74 78            [ 4]  179 	ld	a, b
   5A75 CE 00         [ 7]  180 	adc	a, #0x00
   5A77 DD 77 FD      [19]  181 	ld	-3 (ix), a
                            182 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5A7A 79            [ 4]  183 	ld	a, c
   5A7B C6 08         [ 7]  184 	add	a, #0x08
   5A7D 4F            [ 4]  185 	ld	c, a
   5A7E 78            [ 4]  186 	ld	a, b
   5A7F CE 00         [ 7]  187 	adc	a, #0x00
   5A81 47            [ 4]  188 	ld	b, a
                            189 ;src/entities/projectile.c:33: if (weapon == 0) {
   5A82 DD 7E 09      [19]  190 	ld	a, 9 (ix)
   5A85 B7            [ 4]  191 	or	a, a
   5A86 20 0E         [12]  192 	jr	NZ,00107$
                            193 ;src/entities/projectile.c:34: projectile->w = 3;
   5A88 36 03         [10]  194 	ld	(hl), #0x03
                            195 ;src/entities/projectile.c:35: projectile->h = 2;
   5A8A 3E 02         [ 7]  196 	ld	a, #0x02
   5A8C 12            [ 7]  197 	ld	(de), a
                            198 ;src/entities/projectile.c:36: projectile->damage = 1;
   5A8D E1            [10]  199 	pop	hl
   5A8E E5            [11]  200 	push	hl
   5A8F 36 01         [10]  201 	ld	(hl), #0x01
                            202 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5A91 3E 2D         [ 7]  203 	ld	a, #0x2d
   5A93 02            [ 7]  204 	ld	(bc), a
   5A94 18 37         [12]  205 	jr	00109$
   5A96                     206 00107$:
                            207 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5A96 DD 7E 09      [19]  208 	ld	a, 9 (ix)
   5A99 3D            [ 4]  209 	dec	a
   5A9A 20 0E         [12]  210 	jr	NZ,00104$
                            211 ;src/entities/projectile.c:39: projectile->w = 2;
   5A9C 36 02         [10]  212 	ld	(hl), #0x02
                            213 ;src/entities/projectile.c:40: projectile->h = 3;
   5A9E 3E 03         [ 7]  214 	ld	a, #0x03
   5AA0 12            [ 7]  215 	ld	(de), a
                            216 ;src/entities/projectile.c:41: projectile->damage = 2;
   5AA1 E1            [10]  217 	pop	hl
   5AA2 E5            [11]  218 	push	hl
   5AA3 36 02         [10]  219 	ld	(hl), #0x02
                            220 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5AA5 3E 1C         [ 7]  221 	ld	a, #0x1c
   5AA7 02            [ 7]  222 	ld	(bc), a
   5AA8 18 23         [12]  223 	jr	00109$
   5AAA                     224 00104$:
                            225 ;src/entities/projectile.c:44: projectile->w = 4;
   5AAA 36 04         [10]  226 	ld	(hl), #0x04
                            227 ;src/entities/projectile.c:45: projectile->h = 3;
   5AAC 3E 03         [ 7]  228 	ld	a, #0x03
   5AAE 12            [ 7]  229 	ld	(de), a
                            230 ;src/entities/projectile.c:46: projectile->damage = 3;
   5AAF E1            [10]  231 	pop	hl
   5AB0 E5            [11]  232 	push	hl
   5AB1 36 03         [10]  233 	ld	(hl), #0x03
                            234 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5AB3 3E 38         [ 7]  235 	ld	a, #0x38
   5AB5 02            [ 7]  236 	ld	(bc), a
                            237 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5AB6 D1            [10]  238 	pop	de
   5AB7 C1            [10]  239 	pop	bc
   5AB8 C5            [11]  240 	push	bc
   5AB9 D5            [11]  241 	push	de
   5ABA AF            [ 4]  242 	xor	a, a
   5ABB DD 96 08      [19]  243 	sub	a, 8 (ix)
   5ABE E2 C3 5A      [10]  244 	jp	PO, 00131$
   5AC1 EE 80         [ 7]  245 	xor	a, #0x80
   5AC3                     246 00131$:
   5AC3 F2 CA 5A      [10]  247 	jp	P, 00111$
   5AC6 3E 04         [ 7]  248 	ld	a, #0x04
   5AC8 18 02         [12]  249 	jr	00112$
   5ACA                     250 00111$:
   5ACA 3E FC         [ 7]  251 	ld	a, #0xfc
   5ACC                     252 00112$:
   5ACC 02            [ 7]  253 	ld	(bc), a
   5ACD                     254 00109$:
   5ACD DD F9         [10]  255 	ld	sp, ix
   5ACF DD E1         [14]  256 	pop	ix
   5AD1 C9            [10]  257 	ret
                            258 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            259 ;	---------------------------------
                            260 ; Function projectileupdate
                            261 ; ---------------------------------
   5AD2                     262 _projectileupdate::
   5AD2 DD E5         [15]  263 	push	ix
   5AD4 DD 21 00 00   [14]  264 	ld	ix,#0
   5AD8 DD 39         [15]  265 	add	ix,sp
   5ADA 3B            [ 6]  266 	dec	sp
                            267 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5ADB DD 7E 05      [19]  268 	ld	a, 5 (ix)
   5ADE DD B6 04      [19]  269 	or	a,4 (ix)
   5AE1 28 4A         [12]  270 	jr	Z,00109$
   5AE3 DD 5E 04      [19]  271 	ld	e,4 (ix)
   5AE6 DD 56 05      [19]  272 	ld	d,5 (ix)
   5AE9 FD 21 06 00   [14]  273 	ld	iy, #0x0006
   5AED FD 19         [15]  274 	add	iy, de
   5AEF FD 7E 00      [19]  275 	ld	a, 0 (iy)
   5AF2 B7            [ 4]  276 	or	a, a
                            277 ;src/entities/projectile.c:54: return;
   5AF3 28 38         [12]  278 	jr	Z,00109$
                            279 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5AF5 1A            [ 7]  280 	ld	a, (de)
   5AF6 4F            [ 4]  281 	ld	c, a
   5AF7 6B            [ 4]  282 	ld	l, e
   5AF8 62            [ 4]  283 	ld	h, d
   5AF9 23            [ 6]  284 	inc	hl
   5AFA 23            [ 6]  285 	inc	hl
   5AFB 6E            [ 7]  286 	ld	l, (hl)
   5AFC 09            [11]  287 	add	hl, bc
   5AFD 7D            [ 4]  288 	ld	a, l
   5AFE 12            [ 7]  289 	ld	(de), a
                            290 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5AFF 4B            [ 4]  291 	ld	c, e
   5B00 42            [ 4]  292 	ld	b, d
   5B01 03            [ 6]  293 	inc	bc
   5B02 0A            [ 7]  294 	ld	a, (bc)
   5B03 DD 77 FF      [19]  295 	ld	-1 (ix), a
   5B06 6B            [ 4]  296 	ld	l, e
   5B07 62            [ 4]  297 	ld	h, d
   5B08 23            [ 6]  298 	inc	hl
   5B09 23            [ 6]  299 	inc	hl
   5B0A 23            [ 6]  300 	inc	hl
   5B0B 6E            [ 7]  301 	ld	l, (hl)
   5B0C DD 7E FF      [19]  302 	ld	a, -1 (ix)
   5B0F 85            [ 4]  303 	add	a, l
   5B10 02            [ 7]  304 	ld	(bc), a
                            305 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5B11 21 08 00      [10]  306 	ld	hl, #0x0008
   5B14 19            [11]  307 	add	hl,de
   5B15 4D            [ 4]  308 	ld	c, l
   5B16 44            [ 4]  309 	ld	b, h
   5B17 0A            [ 7]  310 	ld	a, (bc)
   5B18 B7            [ 4]  311 	or	a, a
   5B19 28 03         [12]  312 	jr	Z,00105$
                            313 ;src/entities/projectile.c:61: projectile->lifetime--;
   5B1B C6 FF         [ 7]  314 	add	a, #0xff
   5B1D 02            [ 7]  315 	ld	(bc), a
   5B1E                     316 00105$:
                            317 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5B1E 1A            [ 7]  318 	ld	a, (de)
   5B1F 5F            [ 4]  319 	ld	e, a
   5B20 3E 4E         [ 7]  320 	ld	a, #0x4e
   5B22 93            [ 4]  321 	sub	a, e
   5B23 38 04         [12]  322 	jr	C,00106$
   5B25 0A            [ 7]  323 	ld	a, (bc)
   5B26 B7            [ 4]  324 	or	a, a
   5B27 20 04         [12]  325 	jr	NZ,00109$
   5B29                     326 00106$:
                            327 ;src/entities/projectile.c:65: projectile->active = 0;
   5B29 FD 36 00 00   [19]  328 	ld	0 (iy), #0x00
   5B2D                     329 00109$:
   5B2D 33            [ 6]  330 	inc	sp
   5B2E DD E1         [14]  331 	pop	ix
   5B30 C9            [10]  332 	ret
                            333 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            334 ;	---------------------------------
                            335 ; Function projectilerender
                            336 ; ---------------------------------
   5B31                     337 _projectilerender::
   5B31 DD E5         [15]  338 	push	ix
   5B33 DD 21 00 00   [14]  339 	ld	ix,#0
   5B37 DD 39         [15]  340 	add	ix,sp
   5B39 F5            [11]  341 	push	af
                            342 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5B3A DD 7E 05      [19]  343 	ld	a, 5 (ix)
   5B3D DD B6 04      [19]  344 	or	a,4 (ix)
   5B40 28 72         [12]  345 	jr	Z,00104$
   5B42 DD 5E 04      [19]  346 	ld	e,4 (ix)
   5B45 DD 56 05      [19]  347 	ld	d,5 (ix)
   5B48 D5            [11]  348 	push	de
   5B49 FD E1         [14]  349 	pop	iy
   5B4B FD 7E 06      [19]  350 	ld	a, 6 (iy)
   5B4E B7            [ 4]  351 	or	a, a
                            352 ;src/entities/projectile.c:73: return;
   5B4F 28 63         [12]  353 	jr	Z,00104$
                            354 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5B51 6B            [ 4]  355 	ld	l, e
   5B52 62            [ 4]  356 	ld	h, d
   5B53 23            [ 6]  357 	inc	hl
   5B54 46            [ 7]  358 	ld	b, (hl)
   5B55 1A            [ 7]  359 	ld	a, (de)
   5B56 D5            [11]  360 	push	de
   5B57 C5            [11]  361 	push	bc
   5B58 33            [ 6]  362 	inc	sp
   5B59 F5            [11]  363 	push	af
   5B5A 33            [ 6]  364 	inc	sp
   5B5B 21 00 C0      [10]  365 	ld	hl, #0xc000
   5B5E E5            [11]  366 	push	hl
   5B5F CD 62 5E      [17]  367 	call	_cpct_getScreenPtr
   5B62 4D            [ 4]  368 	ld	c, l
   5B63 44            [ 4]  369 	ld	b, h
   5B64 D1            [10]  370 	pop	de
                            371 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? cpct_px2byteM0(15, 15) : (projectile->weapon == 1 ? cpct_px2byteM0(11, 11) : cpct_px2byteM0(5, 5)), projectile->w, projectile->h);
   5B65 D5            [11]  372 	push	de
   5B66 FD E1         [14]  373 	pop	iy
   5B68 FD 7E 05      [19]  374 	ld	a, 5 (iy)
   5B6B DD 77 FE      [19]  375 	ld	-2 (ix), a
   5B6E D5            [11]  376 	push	de
   5B6F FD E1         [14]  377 	pop	iy
   5B71 FD 7E 04      [19]  378 	ld	a, 4 (iy)
   5B74 DD 77 FF      [19]  379 	ld	-1 (ix), a
   5B77 EB            [ 4]  380 	ex	de,hl
   5B78 11 09 00      [10]  381 	ld	de, #0x0009
   5B7B 19            [11]  382 	add	hl, de
   5B7C 7E            [ 7]  383 	ld	a, (hl)
   5B7D B7            [ 4]  384 	or	a, a
   5B7E 20 0C         [12]  385 	jr	NZ,00106$
   5B80 C5            [11]  386 	push	bc
   5B81 21 0F 0F      [10]  387 	ld	hl, #0x0f0f
   5B84 E5            [11]  388 	push	hl
   5B85 CD 6F 5D      [17]  389 	call	_cpct_px2byteM0
   5B88 55            [ 4]  390 	ld	d, l
   5B89 C1            [10]  391 	pop	bc
   5B8A 18 18         [12]  392 	jr	00107$
   5B8C                     393 00106$:
   5B8C 3D            [ 4]  394 	dec	a
   5B8D 20 0B         [12]  395 	jr	NZ,00108$
   5B8F C5            [11]  396 	push	bc
   5B90 21 0B 0B      [10]  397 	ld	hl, #0x0b0b
   5B93 E5            [11]  398 	push	hl
   5B94 CD 6F 5D      [17]  399 	call	_cpct_px2byteM0
   5B97 C1            [10]  400 	pop	bc
   5B98 18 09         [12]  401 	jr	00109$
   5B9A                     402 00108$:
   5B9A C5            [11]  403 	push	bc
   5B9B 21 05 05      [10]  404 	ld	hl, #0x0505
   5B9E E5            [11]  405 	push	hl
   5B9F CD 6F 5D      [17]  406 	call	_cpct_px2byteM0
   5BA2 C1            [10]  407 	pop	bc
   5BA3                     408 00109$:
   5BA3 55            [ 4]  409 	ld	d, l
   5BA4                     410 00107$:
   5BA4 DD 66 FE      [19]  411 	ld	h, -2 (ix)
   5BA7 DD 6E FF      [19]  412 	ld	l, -1 (ix)
   5BAA E5            [11]  413 	push	hl
   5BAB D5            [11]  414 	push	de
   5BAC 33            [ 6]  415 	inc	sp
   5BAD C5            [11]  416 	push	bc
   5BAE CD A9 5D      [17]  417 	call	_cpct_drawSolidBox
   5BB1 F1            [10]  418 	pop	af
   5BB2 F1            [10]  419 	pop	af
   5BB3 33            [ 6]  420 	inc	sp
   5BB4                     421 00104$:
   5BB4 DD F9         [10]  422 	ld	sp, ix
   5BB6 DD E1         [14]  423 	pop	ix
   5BB8 C9            [10]  424 	ret
                            425 	.area _CODE
                            426 	.area _INITIALIZER
                            427 	.area _CABS (ABS)
