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
   5A34                      53 _projectileinit::
                             54 ;src/entities/projectile.c:5: if (!projectile) {
   5A34 21 03 00      [10]   55 	ld	hl, #2+1
   5A37 39            [11]   56 	add	hl, sp
   5A38 7E            [ 7]   57 	ld	a, (hl)
   5A39 2B            [ 6]   58 	dec	hl
   5A3A B6            [ 7]   59 	or	a,(hl)
                             60 ;src/entities/projectile.c:6: return;
   5A3B C8            [11]   61 	ret	Z
                             62 ;src/entities/projectile.c:9: projectile->x = 0;
   5A3C D1            [10]   63 	pop	de
   5A3D C1            [10]   64 	pop	bc
   5A3E C5            [11]   65 	push	bc
   5A3F D5            [11]   66 	push	de
   5A40 AF            [ 4]   67 	xor	a, a
   5A41 02            [ 7]   68 	ld	(bc), a
                             69 ;src/entities/projectile.c:10: projectile->y = 0;
   5A42 59            [ 4]   70 	ld	e, c
   5A43 50            [ 4]   71 	ld	d, b
   5A44 13            [ 6]   72 	inc	de
   5A45 AF            [ 4]   73 	xor	a, a
   5A46 12            [ 7]   74 	ld	(de), a
                             75 ;src/entities/projectile.c:11: projectile->vx = 0;
   5A47 59            [ 4]   76 	ld	e, c
   5A48 50            [ 4]   77 	ld	d, b
   5A49 13            [ 6]   78 	inc	de
   5A4A 13            [ 6]   79 	inc	de
   5A4B AF            [ 4]   80 	xor	a, a
   5A4C 12            [ 7]   81 	ld	(de), a
                             82 ;src/entities/projectile.c:12: projectile->vy = 0;
   5A4D 59            [ 4]   83 	ld	e, c
   5A4E 50            [ 4]   84 	ld	d, b
   5A4F 13            [ 6]   85 	inc	de
   5A50 13            [ 6]   86 	inc	de
   5A51 13            [ 6]   87 	inc	de
   5A52 AF            [ 4]   88 	xor	a, a
   5A53 12            [ 7]   89 	ld	(de), a
                             90 ;src/entities/projectile.c:13: projectile->w = 2;
   5A54 21 04 00      [10]   91 	ld	hl, #0x0004
   5A57 09            [11]   92 	add	hl, bc
   5A58 36 02         [10]   93 	ld	(hl), #0x02
                             94 ;src/entities/projectile.c:14: projectile->h = 2;
   5A5A 21 05 00      [10]   95 	ld	hl, #0x0005
   5A5D 09            [11]   96 	add	hl, bc
   5A5E 36 02         [10]   97 	ld	(hl), #0x02
                             98 ;src/entities/projectile.c:15: projectile->active = 0;
   5A60 21 06 00      [10]   99 	ld	hl, #0x0006
   5A63 09            [11]  100 	add	hl, bc
   5A64 36 00         [10]  101 	ld	(hl), #0x00
                            102 ;src/entities/projectile.c:16: projectile->damage = 1;
   5A66 21 07 00      [10]  103 	ld	hl, #0x0007
   5A69 09            [11]  104 	add	hl, bc
   5A6A 36 01         [10]  105 	ld	(hl), #0x01
                            106 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5A6C 21 08 00      [10]  107 	ld	hl, #0x0008
   5A6F 09            [11]  108 	add	hl, bc
   5A70 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5A72 21 09 00      [10]  111 	ld	hl, #0x0009
   5A75 09            [11]  112 	add	hl, bc
   5A76 36 00         [10]  113 	ld	(hl), #0x00
   5A78 C9            [10]  114 	ret
                            115 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            116 ;	---------------------------------
                            117 ; Function projectilefire
                            118 ; ---------------------------------
   5A79                     119 _projectilefire::
   5A79 DD E5         [15]  120 	push	ix
   5A7B DD 21 00 00   [14]  121 	ld	ix,#0
   5A7F DD 39         [15]  122 	add	ix,sp
   5A81 F5            [11]  123 	push	af
   5A82 F5            [11]  124 	push	af
                            125 ;src/entities/projectile.c:22: if (!projectile) {
   5A83 DD 7E 05      [19]  126 	ld	a, 5 (ix)
   5A86 DD B6 04      [19]  127 	or	a,4 (ix)
                            128 ;src/entities/projectile.c:23: return;
   5A89 CA 2B 5B      [10]  129 	jp	Z,00109$
                            130 ;src/entities/projectile.c:26: projectile->x = x;
   5A8C DD 4E 04      [19]  131 	ld	c,4 (ix)
   5A8F DD 46 05      [19]  132 	ld	b,5 (ix)
   5A92 DD 7E 06      [19]  133 	ld	a, 6 (ix)
   5A95 02            [ 7]  134 	ld	(bc), a
                            135 ;src/entities/projectile.c:27: projectile->y = y;
   5A96 59            [ 4]  136 	ld	e, c
   5A97 50            [ 4]  137 	ld	d, b
   5A98 13            [ 6]  138 	inc	de
   5A99 DD 7E 07      [19]  139 	ld	a, 7 (ix)
   5A9C 12            [ 7]  140 	ld	(de), a
                            141 ;src/entities/projectile.c:28: projectile->vx = dir;
   5A9D 21 02 00      [10]  142 	ld	hl, #0x0002
   5AA0 09            [11]  143 	add	hl,bc
   5AA1 DD 75 FE      [19]  144 	ld	-2 (ix), l
   5AA4 DD 74 FF      [19]  145 	ld	-1 (ix), h
   5AA7 DD 7E 08      [19]  146 	ld	a, 8 (ix)
   5AAA 77            [ 7]  147 	ld	(hl), a
                            148 ;src/entities/projectile.c:29: projectile->vy = 0;
   5AAB 59            [ 4]  149 	ld	e, c
   5AAC 50            [ 4]  150 	ld	d, b
   5AAD 13            [ 6]  151 	inc	de
   5AAE 13            [ 6]  152 	inc	de
   5AAF 13            [ 6]  153 	inc	de
   5AB0 AF            [ 4]  154 	xor	a, a
   5AB1 12            [ 7]  155 	ld	(de), a
                            156 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5AB2 21 09 00      [10]  157 	ld	hl, #0x0009
   5AB5 09            [11]  158 	add	hl, bc
   5AB6 DD 7E 09      [19]  159 	ld	a, 9 (ix)
   5AB9 77            [ 7]  160 	ld	(hl), a
                            161 ;src/entities/projectile.c:31: projectile->active = 1;
   5ABA 21 06 00      [10]  162 	ld	hl, #0x0006
   5ABD 09            [11]  163 	add	hl, bc
   5ABE 36 01         [10]  164 	ld	(hl), #0x01
                            165 ;src/entities/projectile.c:34: projectile->w = 3;
   5AC0 21 04 00      [10]  166 	ld	hl, #0x0004
   5AC3 09            [11]  167 	add	hl, bc
                            168 ;src/entities/projectile.c:35: projectile->h = 2;
   5AC4 79            [ 4]  169 	ld	a, c
   5AC5 C6 05         [ 7]  170 	add	a, #0x05
   5AC7 5F            [ 4]  171 	ld	e, a
   5AC8 78            [ 4]  172 	ld	a, b
   5AC9 CE 00         [ 7]  173 	adc	a, #0x00
   5ACB 57            [ 4]  174 	ld	d, a
                            175 ;src/entities/projectile.c:36: projectile->damage = 1;
   5ACC 79            [ 4]  176 	ld	a, c
   5ACD C6 07         [ 7]  177 	add	a, #0x07
   5ACF DD 77 FC      [19]  178 	ld	-4 (ix), a
   5AD2 78            [ 4]  179 	ld	a, b
   5AD3 CE 00         [ 7]  180 	adc	a, #0x00
   5AD5 DD 77 FD      [19]  181 	ld	-3 (ix), a
                            182 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AD8 79            [ 4]  183 	ld	a, c
   5AD9 C6 08         [ 7]  184 	add	a, #0x08
   5ADB 4F            [ 4]  185 	ld	c, a
   5ADC 78            [ 4]  186 	ld	a, b
   5ADD CE 00         [ 7]  187 	adc	a, #0x00
   5ADF 47            [ 4]  188 	ld	b, a
                            189 ;src/entities/projectile.c:33: if (weapon == 0) {
   5AE0 DD 7E 09      [19]  190 	ld	a, 9 (ix)
   5AE3 B7            [ 4]  191 	or	a, a
   5AE4 20 0E         [12]  192 	jr	NZ,00107$
                            193 ;src/entities/projectile.c:34: projectile->w = 3;
   5AE6 36 03         [10]  194 	ld	(hl), #0x03
                            195 ;src/entities/projectile.c:35: projectile->h = 2;
   5AE8 3E 02         [ 7]  196 	ld	a, #0x02
   5AEA 12            [ 7]  197 	ld	(de), a
                            198 ;src/entities/projectile.c:36: projectile->damage = 1;
   5AEB E1            [10]  199 	pop	hl
   5AEC E5            [11]  200 	push	hl
   5AED 36 01         [10]  201 	ld	(hl), #0x01
                            202 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5AEF 3E 2D         [ 7]  203 	ld	a, #0x2d
   5AF1 02            [ 7]  204 	ld	(bc), a
   5AF2 18 37         [12]  205 	jr	00109$
   5AF4                     206 00107$:
                            207 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5AF4 DD 7E 09      [19]  208 	ld	a, 9 (ix)
   5AF7 3D            [ 4]  209 	dec	a
   5AF8 20 0E         [12]  210 	jr	NZ,00104$
                            211 ;src/entities/projectile.c:39: projectile->w = 2;
   5AFA 36 02         [10]  212 	ld	(hl), #0x02
                            213 ;src/entities/projectile.c:40: projectile->h = 3;
   5AFC 3E 03         [ 7]  214 	ld	a, #0x03
   5AFE 12            [ 7]  215 	ld	(de), a
                            216 ;src/entities/projectile.c:41: projectile->damage = 2;
   5AFF E1            [10]  217 	pop	hl
   5B00 E5            [11]  218 	push	hl
   5B01 36 02         [10]  219 	ld	(hl), #0x02
                            220 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5B03 3E 1C         [ 7]  221 	ld	a, #0x1c
   5B05 02            [ 7]  222 	ld	(bc), a
   5B06 18 23         [12]  223 	jr	00109$
   5B08                     224 00104$:
                            225 ;src/entities/projectile.c:44: projectile->w = 4;
   5B08 36 04         [10]  226 	ld	(hl), #0x04
                            227 ;src/entities/projectile.c:45: projectile->h = 3;
   5B0A 3E 03         [ 7]  228 	ld	a, #0x03
   5B0C 12            [ 7]  229 	ld	(de), a
                            230 ;src/entities/projectile.c:46: projectile->damage = 3;
   5B0D E1            [10]  231 	pop	hl
   5B0E E5            [11]  232 	push	hl
   5B0F 36 03         [10]  233 	ld	(hl), #0x03
                            234 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5B11 3E 38         [ 7]  235 	ld	a, #0x38
   5B13 02            [ 7]  236 	ld	(bc), a
                            237 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5B14 D1            [10]  238 	pop	de
   5B15 C1            [10]  239 	pop	bc
   5B16 C5            [11]  240 	push	bc
   5B17 D5            [11]  241 	push	de
   5B18 AF            [ 4]  242 	xor	a, a
   5B19 DD 96 08      [19]  243 	sub	a, 8 (ix)
   5B1C E2 21 5B      [10]  244 	jp	PO, 00131$
   5B1F EE 80         [ 7]  245 	xor	a, #0x80
   5B21                     246 00131$:
   5B21 F2 28 5B      [10]  247 	jp	P, 00111$
   5B24 3E 04         [ 7]  248 	ld	a, #0x04
   5B26 18 02         [12]  249 	jr	00112$
   5B28                     250 00111$:
   5B28 3E FC         [ 7]  251 	ld	a, #0xfc
   5B2A                     252 00112$:
   5B2A 02            [ 7]  253 	ld	(bc), a
   5B2B                     254 00109$:
   5B2B DD F9         [10]  255 	ld	sp, ix
   5B2D DD E1         [14]  256 	pop	ix
   5B2F C9            [10]  257 	ret
                            258 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            259 ;	---------------------------------
                            260 ; Function projectileupdate
                            261 ; ---------------------------------
   5B30                     262 _projectileupdate::
   5B30 DD E5         [15]  263 	push	ix
   5B32 DD 21 00 00   [14]  264 	ld	ix,#0
   5B36 DD 39         [15]  265 	add	ix,sp
   5B38 3B            [ 6]  266 	dec	sp
                            267 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5B39 DD 7E 05      [19]  268 	ld	a, 5 (ix)
   5B3C DD B6 04      [19]  269 	or	a,4 (ix)
   5B3F 28 4A         [12]  270 	jr	Z,00109$
   5B41 DD 5E 04      [19]  271 	ld	e,4 (ix)
   5B44 DD 56 05      [19]  272 	ld	d,5 (ix)
   5B47 FD 21 06 00   [14]  273 	ld	iy, #0x0006
   5B4B FD 19         [15]  274 	add	iy, de
   5B4D FD 7E 00      [19]  275 	ld	a, 0 (iy)
   5B50 B7            [ 4]  276 	or	a, a
                            277 ;src/entities/projectile.c:54: return;
   5B51 28 38         [12]  278 	jr	Z,00109$
                            279 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5B53 1A            [ 7]  280 	ld	a, (de)
   5B54 4F            [ 4]  281 	ld	c, a
   5B55 6B            [ 4]  282 	ld	l, e
   5B56 62            [ 4]  283 	ld	h, d
   5B57 23            [ 6]  284 	inc	hl
   5B58 23            [ 6]  285 	inc	hl
   5B59 6E            [ 7]  286 	ld	l, (hl)
   5B5A 09            [11]  287 	add	hl, bc
   5B5B 7D            [ 4]  288 	ld	a, l
   5B5C 12            [ 7]  289 	ld	(de), a
                            290 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5B5D 4B            [ 4]  291 	ld	c, e
   5B5E 42            [ 4]  292 	ld	b, d
   5B5F 03            [ 6]  293 	inc	bc
   5B60 0A            [ 7]  294 	ld	a, (bc)
   5B61 DD 77 FF      [19]  295 	ld	-1 (ix), a
   5B64 6B            [ 4]  296 	ld	l, e
   5B65 62            [ 4]  297 	ld	h, d
   5B66 23            [ 6]  298 	inc	hl
   5B67 23            [ 6]  299 	inc	hl
   5B68 23            [ 6]  300 	inc	hl
   5B69 6E            [ 7]  301 	ld	l, (hl)
   5B6A DD 7E FF      [19]  302 	ld	a, -1 (ix)
   5B6D 85            [ 4]  303 	add	a, l
   5B6E 02            [ 7]  304 	ld	(bc), a
                            305 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5B6F 21 08 00      [10]  306 	ld	hl, #0x0008
   5B72 19            [11]  307 	add	hl,de
   5B73 4D            [ 4]  308 	ld	c, l
   5B74 44            [ 4]  309 	ld	b, h
   5B75 0A            [ 7]  310 	ld	a, (bc)
   5B76 B7            [ 4]  311 	or	a, a
   5B77 28 03         [12]  312 	jr	Z,00105$
                            313 ;src/entities/projectile.c:61: projectile->lifetime--;
   5B79 C6 FF         [ 7]  314 	add	a, #0xff
   5B7B 02            [ 7]  315 	ld	(bc), a
   5B7C                     316 00105$:
                            317 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5B7C 1A            [ 7]  318 	ld	a, (de)
   5B7D 5F            [ 4]  319 	ld	e, a
   5B7E 3E 4E         [ 7]  320 	ld	a, #0x4e
   5B80 93            [ 4]  321 	sub	a, e
   5B81 38 04         [12]  322 	jr	C,00106$
   5B83 0A            [ 7]  323 	ld	a, (bc)
   5B84 B7            [ 4]  324 	or	a, a
   5B85 20 04         [12]  325 	jr	NZ,00109$
   5B87                     326 00106$:
                            327 ;src/entities/projectile.c:65: projectile->active = 0;
   5B87 FD 36 00 00   [19]  328 	ld	0 (iy), #0x00
   5B8B                     329 00109$:
   5B8B 33            [ 6]  330 	inc	sp
   5B8C DD E1         [14]  331 	pop	ix
   5B8E C9            [10]  332 	ret
                            333 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            334 ;	---------------------------------
                            335 ; Function projectilerender
                            336 ; ---------------------------------
   5B8F                     337 _projectilerender::
   5B8F DD E5         [15]  338 	push	ix
   5B91 DD 21 00 00   [14]  339 	ld	ix,#0
   5B95 DD 39         [15]  340 	add	ix,sp
   5B97 F5            [11]  341 	push	af
                            342 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5B98 DD 7E 05      [19]  343 	ld	a, 5 (ix)
   5B9B DD B6 04      [19]  344 	or	a,4 (ix)
   5B9E 28 72         [12]  345 	jr	Z,00104$
   5BA0 DD 5E 04      [19]  346 	ld	e,4 (ix)
   5BA3 DD 56 05      [19]  347 	ld	d,5 (ix)
   5BA6 D5            [11]  348 	push	de
   5BA7 FD E1         [14]  349 	pop	iy
   5BA9 FD 7E 06      [19]  350 	ld	a, 6 (iy)
   5BAC B7            [ 4]  351 	or	a, a
                            352 ;src/entities/projectile.c:73: return;
   5BAD 28 63         [12]  353 	jr	Z,00104$
                            354 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5BAF 6B            [ 4]  355 	ld	l, e
   5BB0 62            [ 4]  356 	ld	h, d
   5BB1 23            [ 6]  357 	inc	hl
   5BB2 46            [ 7]  358 	ld	b, (hl)
   5BB3 1A            [ 7]  359 	ld	a, (de)
   5BB4 D5            [11]  360 	push	de
   5BB5 C5            [11]  361 	push	bc
   5BB6 33            [ 6]  362 	inc	sp
   5BB7 F5            [11]  363 	push	af
   5BB8 33            [ 6]  364 	inc	sp
   5BB9 21 00 C0      [10]  365 	ld	hl, #0xc000
   5BBC E5            [11]  366 	push	hl
   5BBD CD A9 5E      [17]  367 	call	_cpct_getScreenPtr
   5BC0 4D            [ 4]  368 	ld	c, l
   5BC1 44            [ 4]  369 	ld	b, h
   5BC2 D1            [10]  370 	pop	de
                            371 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? cpct_px2byteM0(15, 15) : (projectile->weapon == 1 ? cpct_px2byteM0(11, 11) : cpct_px2byteM0(5, 5)), projectile->w, projectile->h);
   5BC3 D5            [11]  372 	push	de
   5BC4 FD E1         [14]  373 	pop	iy
   5BC6 FD 7E 05      [19]  374 	ld	a, 5 (iy)
   5BC9 DD 77 FF      [19]  375 	ld	-1 (ix), a
   5BCC D5            [11]  376 	push	de
   5BCD FD E1         [14]  377 	pop	iy
   5BCF FD 7E 04      [19]  378 	ld	a, 4 (iy)
   5BD2 DD 77 FE      [19]  379 	ld	-2 (ix), a
   5BD5 EB            [ 4]  380 	ex	de,hl
   5BD6 11 09 00      [10]  381 	ld	de, #0x0009
   5BD9 19            [11]  382 	add	hl, de
   5BDA 7E            [ 7]  383 	ld	a, (hl)
   5BDB B7            [ 4]  384 	or	a, a
   5BDC 20 0C         [12]  385 	jr	NZ,00106$
   5BDE C5            [11]  386 	push	bc
   5BDF 21 0F 0F      [10]  387 	ld	hl, #0x0f0f
   5BE2 E5            [11]  388 	push	hl
   5BE3 CD B6 5D      [17]  389 	call	_cpct_px2byteM0
   5BE6 55            [ 4]  390 	ld	d, l
   5BE7 C1            [10]  391 	pop	bc
   5BE8 18 18         [12]  392 	jr	00107$
   5BEA                     393 00106$:
   5BEA 3D            [ 4]  394 	dec	a
   5BEB 20 0B         [12]  395 	jr	NZ,00108$
   5BED C5            [11]  396 	push	bc
   5BEE 21 0B 0B      [10]  397 	ld	hl, #0x0b0b
   5BF1 E5            [11]  398 	push	hl
   5BF2 CD B6 5D      [17]  399 	call	_cpct_px2byteM0
   5BF5 C1            [10]  400 	pop	bc
   5BF6 18 09         [12]  401 	jr	00109$
   5BF8                     402 00108$:
   5BF8 C5            [11]  403 	push	bc
   5BF9 21 05 05      [10]  404 	ld	hl, #0x0505
   5BFC E5            [11]  405 	push	hl
   5BFD CD B6 5D      [17]  406 	call	_cpct_px2byteM0
   5C00 C1            [10]  407 	pop	bc
   5C01                     408 00109$:
   5C01 55            [ 4]  409 	ld	d, l
   5C02                     410 00107$:
   5C02 DD 66 FF      [19]  411 	ld	h, -1 (ix)
   5C05 DD 6E FE      [19]  412 	ld	l, -2 (ix)
   5C08 E5            [11]  413 	push	hl
   5C09 D5            [11]  414 	push	de
   5C0A 33            [ 6]  415 	inc	sp
   5C0B C5            [11]  416 	push	bc
   5C0C CD F0 5D      [17]  417 	call	_cpct_drawSolidBox
   5C0F F1            [10]  418 	pop	af
   5C10 F1            [10]  419 	pop	af
   5C11 33            [ 6]  420 	inc	sp
   5C12                     421 00104$:
   5C12 DD F9         [10]  422 	ld	sp, ix
   5C14 DD E1         [14]  423 	pop	ix
   5C16 C9            [10]  424 	ret
                            425 	.area _CODE
                            426 	.area _INITIALIZER
                            427 	.area _CABS (ABS)
