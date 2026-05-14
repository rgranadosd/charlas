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
   5A25                      52 _projectileinit::
                             53 ;src/entities/projectile.c:5: if (!projectile) {
   5A25 21 03 00      [10]   54 	ld	hl, #2+1
   5A28 39            [11]   55 	add	hl, sp
   5A29 7E            [ 7]   56 	ld	a, (hl)
   5A2A 2B            [ 6]   57 	dec	hl
   5A2B B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:6: return;
   5A2C C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:9: projectile->x = 0;
   5A2D D1            [10]   62 	pop	de
   5A2E C1            [10]   63 	pop	bc
   5A2F C5            [11]   64 	push	bc
   5A30 D5            [11]   65 	push	de
   5A31 AF            [ 4]   66 	xor	a, a
   5A32 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:10: projectile->y = 0;
   5A33 59            [ 4]   69 	ld	e, c
   5A34 50            [ 4]   70 	ld	d, b
   5A35 13            [ 6]   71 	inc	de
   5A36 AF            [ 4]   72 	xor	a, a
   5A37 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:11: projectile->vx = 0;
   5A38 59            [ 4]   75 	ld	e, c
   5A39 50            [ 4]   76 	ld	d, b
   5A3A 13            [ 6]   77 	inc	de
   5A3B 13            [ 6]   78 	inc	de
   5A3C AF            [ 4]   79 	xor	a, a
   5A3D 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:12: projectile->vy = 0;
   5A3E 59            [ 4]   82 	ld	e, c
   5A3F 50            [ 4]   83 	ld	d, b
   5A40 13            [ 6]   84 	inc	de
   5A41 13            [ 6]   85 	inc	de
   5A42 13            [ 6]   86 	inc	de
   5A43 AF            [ 4]   87 	xor	a, a
   5A44 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:13: projectile->w = 2;
   5A45 21 04 00      [10]   90 	ld	hl, #0x0004
   5A48 09            [11]   91 	add	hl, bc
   5A49 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:14: projectile->h = 2;
   5A4B 21 05 00      [10]   94 	ld	hl, #0x0005
   5A4E 09            [11]   95 	add	hl, bc
   5A4F 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:15: projectile->active = 0;
   5A51 21 06 00      [10]   98 	ld	hl, #0x0006
   5A54 09            [11]   99 	add	hl, bc
   5A55 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:16: projectile->damage = 1;
   5A57 21 07 00      [10]  102 	ld	hl, #0x0007
   5A5A 09            [11]  103 	add	hl, bc
   5A5B 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5A5D 21 08 00      [10]  106 	ld	hl, #0x0008
   5A60 09            [11]  107 	add	hl, bc
   5A61 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5A63 21 09 00      [10]  110 	ld	hl, #0x0009
   5A66 09            [11]  111 	add	hl, bc
   5A67 36 00         [10]  112 	ld	(hl), #0x00
   5A69 C9            [10]  113 	ret
                            114 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            115 ;	---------------------------------
                            116 ; Function projectilefire
                            117 ; ---------------------------------
   5A6A                     118 _projectilefire::
   5A6A DD E5         [15]  119 	push	ix
   5A6C DD 21 00 00   [14]  120 	ld	ix,#0
   5A70 DD 39         [15]  121 	add	ix,sp
   5A72 F5            [11]  122 	push	af
   5A73 F5            [11]  123 	push	af
                            124 ;src/entities/projectile.c:22: if (!projectile) {
   5A74 DD 7E 05      [19]  125 	ld	a, 5 (ix)
   5A77 DD B6 04      [19]  126 	or	a,4 (ix)
                            127 ;src/entities/projectile.c:23: return;
   5A7A CA 23 5B      [10]  128 	jp	Z,00109$
                            129 ;src/entities/projectile.c:26: projectile->x = x;
   5A7D DD 4E 04      [19]  130 	ld	c,4 (ix)
   5A80 DD 46 05      [19]  131 	ld	b,5 (ix)
   5A83 DD 7E 06      [19]  132 	ld	a, 6 (ix)
   5A86 02            [ 7]  133 	ld	(bc), a
                            134 ;src/entities/projectile.c:27: projectile->y = y;
   5A87 59            [ 4]  135 	ld	e, c
   5A88 50            [ 4]  136 	ld	d, b
   5A89 13            [ 6]  137 	inc	de
   5A8A DD 7E 07      [19]  138 	ld	a, 7 (ix)
   5A8D 12            [ 7]  139 	ld	(de), a
                            140 ;src/entities/projectile.c:28: projectile->vx = dir;
   5A8E 21 02 00      [10]  141 	ld	hl, #0x0002
   5A91 09            [11]  142 	add	hl,bc
   5A92 E3            [19]  143 	ex	(sp), hl
   5A93 E1            [10]  144 	pop	hl
   5A94 E5            [11]  145 	push	hl
   5A95 DD 7E 08      [19]  146 	ld	a, 8 (ix)
   5A98 77            [ 7]  147 	ld	(hl), a
                            148 ;src/entities/projectile.c:29: projectile->vy = 0;
   5A99 59            [ 4]  149 	ld	e, c
   5A9A 50            [ 4]  150 	ld	d, b
   5A9B 13            [ 6]  151 	inc	de
   5A9C 13            [ 6]  152 	inc	de
   5A9D 13            [ 6]  153 	inc	de
   5A9E AF            [ 4]  154 	xor	a, a
   5A9F 12            [ 7]  155 	ld	(de), a
                            156 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5AA0 21 09 00      [10]  157 	ld	hl, #0x0009
   5AA3 09            [11]  158 	add	hl, bc
   5AA4 DD 7E 09      [19]  159 	ld	a, 9 (ix)
   5AA7 77            [ 7]  160 	ld	(hl), a
                            161 ;src/entities/projectile.c:31: projectile->active = 1;
   5AA8 21 06 00      [10]  162 	ld	hl, #0x0006
   5AAB 09            [11]  163 	add	hl, bc
   5AAC 36 01         [10]  164 	ld	(hl), #0x01
                            165 ;src/entities/projectile.c:34: projectile->w = 3;
   5AAE 21 04 00      [10]  166 	ld	hl, #0x0004
   5AB1 09            [11]  167 	add	hl, bc
                            168 ;src/entities/projectile.c:35: projectile->h = 2;
   5AB2 79            [ 4]  169 	ld	a, c
   5AB3 C6 05         [ 7]  170 	add	a, #0x05
   5AB5 5F            [ 4]  171 	ld	e, a
   5AB6 78            [ 4]  172 	ld	a, b
   5AB7 CE 00         [ 7]  173 	adc	a, #0x00
   5AB9 57            [ 4]  174 	ld	d, a
                            175 ;src/entities/projectile.c:36: projectile->damage = 1;
   5ABA 79            [ 4]  176 	ld	a, c
   5ABB C6 07         [ 7]  177 	add	a, #0x07
   5ABD DD 77 FE      [19]  178 	ld	-2 (ix), a
   5AC0 78            [ 4]  179 	ld	a, b
   5AC1 CE 00         [ 7]  180 	adc	a, #0x00
   5AC3 DD 77 FF      [19]  181 	ld	-1 (ix), a
                            182 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AC6 79            [ 4]  183 	ld	a, c
   5AC7 C6 08         [ 7]  184 	add	a, #0x08
   5AC9 4F            [ 4]  185 	ld	c, a
   5ACA 78            [ 4]  186 	ld	a, b
   5ACB CE 00         [ 7]  187 	adc	a, #0x00
   5ACD 47            [ 4]  188 	ld	b, a
                            189 ;src/entities/projectile.c:33: if (weapon == 0) {
   5ACE DD 7E 09      [19]  190 	ld	a, 9 (ix)
   5AD1 B7            [ 4]  191 	or	a, a
   5AD2 20 12         [12]  192 	jr	NZ,00107$
                            193 ;src/entities/projectile.c:34: projectile->w = 3;
   5AD4 36 03         [10]  194 	ld	(hl), #0x03
                            195 ;src/entities/projectile.c:35: projectile->h = 2;
   5AD6 3E 02         [ 7]  196 	ld	a, #0x02
   5AD8 12            [ 7]  197 	ld	(de), a
                            198 ;src/entities/projectile.c:36: projectile->damage = 1;
   5AD9 DD 6E FE      [19]  199 	ld	l,-2 (ix)
   5ADC DD 66 FF      [19]  200 	ld	h,-1 (ix)
   5ADF 36 01         [10]  201 	ld	(hl), #0x01
                            202 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AE1 3E 2D         [ 7]  203 	ld	a, #0x2d
   5AE3 02            [ 7]  204 	ld	(bc), a
   5AE4 18 3D         [12]  205 	jr	00109$
   5AE6                     206 00107$:
                            207 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5AE6 DD 7E 09      [19]  208 	ld	a, 9 (ix)
   5AE9 3D            [ 4]  209 	dec	a
   5AEA 20 12         [12]  210 	jr	NZ,00104$
                            211 ;src/entities/projectile.c:39: projectile->w = 2;
   5AEC 36 02         [10]  212 	ld	(hl), #0x02
                            213 ;src/entities/projectile.c:40: projectile->h = 3;
   5AEE 3E 03         [ 7]  214 	ld	a, #0x03
   5AF0 12            [ 7]  215 	ld	(de), a
                            216 ;src/entities/projectile.c:41: projectile->damage = 2;
   5AF1 DD 6E FE      [19]  217 	ld	l,-2 (ix)
   5AF4 DD 66 FF      [19]  218 	ld	h,-1 (ix)
   5AF7 36 02         [10]  219 	ld	(hl), #0x02
                            220 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5AF9 3E 1C         [ 7]  221 	ld	a, #0x1c
   5AFB 02            [ 7]  222 	ld	(bc), a
   5AFC 18 25         [12]  223 	jr	00109$
   5AFE                     224 00104$:
                            225 ;src/entities/projectile.c:44: projectile->w = 4;
   5AFE 36 04         [10]  226 	ld	(hl), #0x04
                            227 ;src/entities/projectile.c:45: projectile->h = 3;
   5B00 3E 03         [ 7]  228 	ld	a, #0x03
   5B02 12            [ 7]  229 	ld	(de), a
                            230 ;src/entities/projectile.c:46: projectile->damage = 3;
   5B03 DD 6E FE      [19]  231 	ld	l,-2 (ix)
   5B06 DD 66 FF      [19]  232 	ld	h,-1 (ix)
   5B09 36 03         [10]  233 	ld	(hl), #0x03
                            234 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5B0B 3E 38         [ 7]  235 	ld	a, #0x38
   5B0D 02            [ 7]  236 	ld	(bc), a
                            237 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5B0E C1            [10]  238 	pop	bc
   5B0F C5            [11]  239 	push	bc
   5B10 AF            [ 4]  240 	xor	a, a
   5B11 DD 96 08      [19]  241 	sub	a, 8 (ix)
   5B14 E2 19 5B      [10]  242 	jp	PO, 00131$
   5B17 EE 80         [ 7]  243 	xor	a, #0x80
   5B19                     244 00131$:
   5B19 F2 20 5B      [10]  245 	jp	P, 00111$
   5B1C 3E 04         [ 7]  246 	ld	a, #0x04
   5B1E 18 02         [12]  247 	jr	00112$
   5B20                     248 00111$:
   5B20 3E FC         [ 7]  249 	ld	a, #0xfc
   5B22                     250 00112$:
   5B22 02            [ 7]  251 	ld	(bc), a
   5B23                     252 00109$:
   5B23 DD F9         [10]  253 	ld	sp, ix
   5B25 DD E1         [14]  254 	pop	ix
   5B27 C9            [10]  255 	ret
                            256 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            257 ;	---------------------------------
                            258 ; Function projectileupdate
                            259 ; ---------------------------------
   5B28                     260 _projectileupdate::
   5B28 DD E5         [15]  261 	push	ix
   5B2A DD 21 00 00   [14]  262 	ld	ix,#0
   5B2E DD 39         [15]  263 	add	ix,sp
   5B30 3B            [ 6]  264 	dec	sp
                            265 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5B31 DD 7E 05      [19]  266 	ld	a, 5 (ix)
   5B34 DD B6 04      [19]  267 	or	a,4 (ix)
   5B37 28 4A         [12]  268 	jr	Z,00109$
   5B39 DD 5E 04      [19]  269 	ld	e,4 (ix)
   5B3C DD 56 05      [19]  270 	ld	d,5 (ix)
   5B3F FD 21 06 00   [14]  271 	ld	iy, #0x0006
   5B43 FD 19         [15]  272 	add	iy, de
   5B45 FD 7E 00      [19]  273 	ld	a, 0 (iy)
   5B48 B7            [ 4]  274 	or	a, a
                            275 ;src/entities/projectile.c:54: return;
   5B49 28 38         [12]  276 	jr	Z,00109$
                            277 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5B4B 1A            [ 7]  278 	ld	a, (de)
   5B4C 4F            [ 4]  279 	ld	c, a
   5B4D 6B            [ 4]  280 	ld	l, e
   5B4E 62            [ 4]  281 	ld	h, d
   5B4F 23            [ 6]  282 	inc	hl
   5B50 23            [ 6]  283 	inc	hl
   5B51 6E            [ 7]  284 	ld	l, (hl)
   5B52 09            [11]  285 	add	hl, bc
   5B53 7D            [ 4]  286 	ld	a, l
   5B54 12            [ 7]  287 	ld	(de), a
                            288 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5B55 4B            [ 4]  289 	ld	c, e
   5B56 42            [ 4]  290 	ld	b, d
   5B57 03            [ 6]  291 	inc	bc
   5B58 0A            [ 7]  292 	ld	a, (bc)
   5B59 DD 77 FF      [19]  293 	ld	-1 (ix), a
   5B5C 6B            [ 4]  294 	ld	l, e
   5B5D 62            [ 4]  295 	ld	h, d
   5B5E 23            [ 6]  296 	inc	hl
   5B5F 23            [ 6]  297 	inc	hl
   5B60 23            [ 6]  298 	inc	hl
   5B61 6E            [ 7]  299 	ld	l, (hl)
   5B62 DD 7E FF      [19]  300 	ld	a, -1 (ix)
   5B65 85            [ 4]  301 	add	a, l
   5B66 02            [ 7]  302 	ld	(bc), a
                            303 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5B67 21 08 00      [10]  304 	ld	hl, #0x0008
   5B6A 19            [11]  305 	add	hl,de
   5B6B 4D            [ 4]  306 	ld	c, l
   5B6C 44            [ 4]  307 	ld	b, h
   5B6D 0A            [ 7]  308 	ld	a, (bc)
   5B6E B7            [ 4]  309 	or	a, a
   5B6F 28 03         [12]  310 	jr	Z,00105$
                            311 ;src/entities/projectile.c:61: projectile->lifetime--;
   5B71 C6 FF         [ 7]  312 	add	a, #0xff
   5B73 02            [ 7]  313 	ld	(bc), a
   5B74                     314 00105$:
                            315 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5B74 1A            [ 7]  316 	ld	a, (de)
   5B75 5F            [ 4]  317 	ld	e, a
   5B76 3E 4E         [ 7]  318 	ld	a, #0x4e
   5B78 93            [ 4]  319 	sub	a, e
   5B79 38 04         [12]  320 	jr	C,00106$
   5B7B 0A            [ 7]  321 	ld	a, (bc)
   5B7C B7            [ 4]  322 	or	a, a
   5B7D 20 04         [12]  323 	jr	NZ,00109$
   5B7F                     324 00106$:
                            325 ;src/entities/projectile.c:65: projectile->active = 0;
   5B7F FD 36 00 00   [19]  326 	ld	0 (iy), #0x00
   5B83                     327 00109$:
   5B83 33            [ 6]  328 	inc	sp
   5B84 DD E1         [14]  329 	pop	ix
   5B86 C9            [10]  330 	ret
                            331 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            332 ;	---------------------------------
                            333 ; Function projectilerender
                            334 ; ---------------------------------
   5B87                     335 _projectilerender::
   5B87 DD E5         [15]  336 	push	ix
   5B89 DD 21 00 00   [14]  337 	ld	ix,#0
   5B8D DD 39         [15]  338 	add	ix,sp
   5B8F F5            [11]  339 	push	af
                            340 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5B90 DD 7E 05      [19]  341 	ld	a, 5 (ix)
   5B93 DD B6 04      [19]  342 	or	a,4 (ix)
   5B96 28 5B         [12]  343 	jr	Z,00104$
   5B98 DD 5E 04      [19]  344 	ld	e,4 (ix)
   5B9B DD 56 05      [19]  345 	ld	d,5 (ix)
   5B9E D5            [11]  346 	push	de
   5B9F FD E1         [14]  347 	pop	iy
   5BA1 FD 7E 06      [19]  348 	ld	a, 6 (iy)
   5BA4 B7            [ 4]  349 	or	a, a
                            350 ;src/entities/projectile.c:73: return;
   5BA5 28 4C         [12]  351 	jr	Z,00104$
                            352 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5BA7 6B            [ 4]  353 	ld	l, e
   5BA8 62            [ 4]  354 	ld	h, d
   5BA9 23            [ 6]  355 	inc	hl
   5BAA 46            [ 7]  356 	ld	b, (hl)
   5BAB 1A            [ 7]  357 	ld	a, (de)
   5BAC D5            [11]  358 	push	de
   5BAD C5            [11]  359 	push	bc
   5BAE 33            [ 6]  360 	inc	sp
   5BAF F5            [11]  361 	push	af
   5BB0 33            [ 6]  362 	inc	sp
   5BB1 21 00 C0      [10]  363 	ld	hl, #0xc000
   5BB4 E5            [11]  364 	push	hl
   5BB5 CD 62 5E      [17]  365 	call	_cpct_getScreenPtr
   5BB8 4D            [ 4]  366 	ld	c, l
   5BB9 44            [ 4]  367 	ld	b, h
   5BBA D1            [10]  368 	pop	de
                            369 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? 0x0F : (projectile->weapon == 1 ? 0x6B : 0x5A), projectile->w, projectile->h);
   5BBB D5            [11]  370 	push	de
   5BBC FD E1         [14]  371 	pop	iy
   5BBE FD 7E 05      [19]  372 	ld	a, 5 (iy)
   5BC1 DD 77 FF      [19]  373 	ld	-1 (ix), a
   5BC4 D5            [11]  374 	push	de
   5BC5 FD E1         [14]  375 	pop	iy
   5BC7 FD 7E 04      [19]  376 	ld	a, 4 (iy)
   5BCA DD 77 FE      [19]  377 	ld	-2 (ix), a
   5BCD EB            [ 4]  378 	ex	de,hl
   5BCE 11 09 00      [10]  379 	ld	de, #0x0009
   5BD1 19            [11]  380 	add	hl, de
   5BD2 7E            [ 7]  381 	ld	a, (hl)
   5BD3 B7            [ 4]  382 	or	a, a
   5BD4 20 04         [12]  383 	jr	NZ,00106$
   5BD6 16 0F         [ 7]  384 	ld	d, #0x0f
   5BD8 18 09         [12]  385 	jr	00107$
   5BDA                     386 00106$:
   5BDA 3D            [ 4]  387 	dec	a
   5BDB 20 04         [12]  388 	jr	NZ,00108$
   5BDD 16 6B         [ 7]  389 	ld	d, #0x6b
   5BDF 18 02         [12]  390 	jr	00109$
   5BE1                     391 00108$:
   5BE1 16 5A         [ 7]  392 	ld	d, #0x5a
   5BE3                     393 00109$:
   5BE3                     394 00107$:
   5BE3 DD 66 FF      [19]  395 	ld	h, -1 (ix)
   5BE6 DD 6E FE      [19]  396 	ld	l, -2 (ix)
   5BE9 E5            [11]  397 	push	hl
   5BEA D5            [11]  398 	push	de
   5BEB 33            [ 6]  399 	inc	sp
   5BEC C5            [11]  400 	push	bc
   5BED CD A9 5D      [17]  401 	call	_cpct_drawSolidBox
   5BF0 F1            [10]  402 	pop	af
   5BF1 F1            [10]  403 	pop	af
   5BF2 33            [ 6]  404 	inc	sp
   5BF3                     405 00104$:
   5BF3 DD F9         [10]  406 	ld	sp, ix
   5BF5 DD E1         [14]  407 	pop	ix
   5BF7 C9            [10]  408 	ret
                            409 	.area _CODE
                            410 	.area _INITIALIZER
                            411 	.area _CABS (ABS)
