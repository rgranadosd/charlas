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
   5D38                      53 _projectileinit::
                             54 ;src/entities/projectile.c:5: if (!projectile) {
   5D38 21 03 00      [10]   55 	ld	hl, #2+1
   5D3B 39            [11]   56 	add	hl, sp
   5D3C 7E            [ 7]   57 	ld	a, (hl)
   5D3D 2B            [ 6]   58 	dec	hl
   5D3E B6            [ 7]   59 	or	a,(hl)
                             60 ;src/entities/projectile.c:6: return;
   5D3F C8            [11]   61 	ret	Z
                             62 ;src/entities/projectile.c:9: projectile->x = 0;
   5D40 D1            [10]   63 	pop	de
   5D41 C1            [10]   64 	pop	bc
   5D42 C5            [11]   65 	push	bc
   5D43 D5            [11]   66 	push	de
   5D44 AF            [ 4]   67 	xor	a, a
   5D45 02            [ 7]   68 	ld	(bc), a
                             69 ;src/entities/projectile.c:10: projectile->y = 0;
   5D46 59            [ 4]   70 	ld	e, c
   5D47 50            [ 4]   71 	ld	d, b
   5D48 13            [ 6]   72 	inc	de
   5D49 AF            [ 4]   73 	xor	a, a
   5D4A 12            [ 7]   74 	ld	(de), a
                             75 ;src/entities/projectile.c:11: projectile->vx = 0;
   5D4B 59            [ 4]   76 	ld	e, c
   5D4C 50            [ 4]   77 	ld	d, b
   5D4D 13            [ 6]   78 	inc	de
   5D4E 13            [ 6]   79 	inc	de
   5D4F AF            [ 4]   80 	xor	a, a
   5D50 12            [ 7]   81 	ld	(de), a
                             82 ;src/entities/projectile.c:12: projectile->vy = 0;
   5D51 59            [ 4]   83 	ld	e, c
   5D52 50            [ 4]   84 	ld	d, b
   5D53 13            [ 6]   85 	inc	de
   5D54 13            [ 6]   86 	inc	de
   5D55 13            [ 6]   87 	inc	de
   5D56 AF            [ 4]   88 	xor	a, a
   5D57 12            [ 7]   89 	ld	(de), a
                             90 ;src/entities/projectile.c:13: projectile->w = 2;
   5D58 21 04 00      [10]   91 	ld	hl, #0x0004
   5D5B 09            [11]   92 	add	hl, bc
   5D5C 36 02         [10]   93 	ld	(hl), #0x02
                             94 ;src/entities/projectile.c:14: projectile->h = 2;
   5D5E 21 05 00      [10]   95 	ld	hl, #0x0005
   5D61 09            [11]   96 	add	hl, bc
   5D62 36 02         [10]   97 	ld	(hl), #0x02
                             98 ;src/entities/projectile.c:15: projectile->active = 0;
   5D64 21 06 00      [10]   99 	ld	hl, #0x0006
   5D67 09            [11]  100 	add	hl, bc
   5D68 36 00         [10]  101 	ld	(hl), #0x00
                            102 ;src/entities/projectile.c:16: projectile->damage = 1;
   5D6A 21 07 00      [10]  103 	ld	hl, #0x0007
   5D6D 09            [11]  104 	add	hl, bc
   5D6E 36 01         [10]  105 	ld	(hl), #0x01
                            106 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5D70 21 08 00      [10]  107 	ld	hl, #0x0008
   5D73 09            [11]  108 	add	hl, bc
   5D74 36 00         [10]  109 	ld	(hl), #0x00
                            110 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5D76 21 09 00      [10]  111 	ld	hl, #0x0009
   5D79 09            [11]  112 	add	hl, bc
   5D7A 36 00         [10]  113 	ld	(hl), #0x00
   5D7C C9            [10]  114 	ret
                            115 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            116 ;	---------------------------------
                            117 ; Function projectilefire
                            118 ; ---------------------------------
   5D7D                     119 _projectilefire::
   5D7D DD E5         [15]  120 	push	ix
   5D7F DD 21 00 00   [14]  121 	ld	ix,#0
   5D83 DD 39         [15]  122 	add	ix,sp
   5D85 F5            [11]  123 	push	af
   5D86 F5            [11]  124 	push	af
                            125 ;src/entities/projectile.c:22: if (!projectile) {
   5D87 DD 7E 05      [19]  126 	ld	a, 5 (ix)
   5D8A DD B6 04      [19]  127 	or	a,4 (ix)
                            128 ;src/entities/projectile.c:23: return;
   5D8D CA 36 5E      [10]  129 	jp	Z,00109$
                            130 ;src/entities/projectile.c:26: projectile->x = x;
   5D90 DD 4E 04      [19]  131 	ld	c,4 (ix)
   5D93 DD 46 05      [19]  132 	ld	b,5 (ix)
   5D96 DD 7E 06      [19]  133 	ld	a, 6 (ix)
   5D99 02            [ 7]  134 	ld	(bc), a
                            135 ;src/entities/projectile.c:27: projectile->y = y;
   5D9A 59            [ 4]  136 	ld	e, c
   5D9B 50            [ 4]  137 	ld	d, b
   5D9C 13            [ 6]  138 	inc	de
   5D9D DD 7E 07      [19]  139 	ld	a, 7 (ix)
   5DA0 12            [ 7]  140 	ld	(de), a
                            141 ;src/entities/projectile.c:28: projectile->vx = dir;
   5DA1 21 02 00      [10]  142 	ld	hl, #0x0002
   5DA4 09            [11]  143 	add	hl,bc
   5DA5 E3            [19]  144 	ex	(sp), hl
   5DA6 E1            [10]  145 	pop	hl
   5DA7 E5            [11]  146 	push	hl
   5DA8 DD 7E 08      [19]  147 	ld	a, 8 (ix)
   5DAB 77            [ 7]  148 	ld	(hl), a
                            149 ;src/entities/projectile.c:29: projectile->vy = 0;
   5DAC 59            [ 4]  150 	ld	e, c
   5DAD 50            [ 4]  151 	ld	d, b
   5DAE 13            [ 6]  152 	inc	de
   5DAF 13            [ 6]  153 	inc	de
   5DB0 13            [ 6]  154 	inc	de
   5DB1 AF            [ 4]  155 	xor	a, a
   5DB2 12            [ 7]  156 	ld	(de), a
                            157 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   5DB3 21 09 00      [10]  158 	ld	hl, #0x0009
   5DB6 09            [11]  159 	add	hl, bc
   5DB7 DD 7E 09      [19]  160 	ld	a, 9 (ix)
   5DBA 77            [ 7]  161 	ld	(hl), a
                            162 ;src/entities/projectile.c:31: projectile->active = 1;
   5DBB 21 06 00      [10]  163 	ld	hl, #0x0006
   5DBE 09            [11]  164 	add	hl, bc
   5DBF 36 01         [10]  165 	ld	(hl), #0x01
                            166 ;src/entities/projectile.c:34: projectile->w = 3;
   5DC1 21 04 00      [10]  167 	ld	hl, #0x0004
   5DC4 09            [11]  168 	add	hl, bc
                            169 ;src/entities/projectile.c:35: projectile->h = 2;
   5DC5 79            [ 4]  170 	ld	a, c
   5DC6 C6 05         [ 7]  171 	add	a, #0x05
   5DC8 5F            [ 4]  172 	ld	e, a
   5DC9 78            [ 4]  173 	ld	a, b
   5DCA CE 00         [ 7]  174 	adc	a, #0x00
   5DCC 57            [ 4]  175 	ld	d, a
                            176 ;src/entities/projectile.c:36: projectile->damage = 1;
   5DCD 79            [ 4]  177 	ld	a, c
   5DCE C6 07         [ 7]  178 	add	a, #0x07
   5DD0 DD 77 FE      [19]  179 	ld	-2 (ix), a
   5DD3 78            [ 4]  180 	ld	a, b
   5DD4 CE 00         [ 7]  181 	adc	a, #0x00
   5DD6 DD 77 FF      [19]  182 	ld	-1 (ix), a
                            183 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5DD9 79            [ 4]  184 	ld	a, c
   5DDA C6 08         [ 7]  185 	add	a, #0x08
   5DDC 4F            [ 4]  186 	ld	c, a
   5DDD 78            [ 4]  187 	ld	a, b
   5DDE CE 00         [ 7]  188 	adc	a, #0x00
   5DE0 47            [ 4]  189 	ld	b, a
                            190 ;src/entities/projectile.c:33: if (weapon == 0) {
   5DE1 DD 7E 09      [19]  191 	ld	a, 9 (ix)
   5DE4 B7            [ 4]  192 	or	a, a
   5DE5 20 12         [12]  193 	jr	NZ,00107$
                            194 ;src/entities/projectile.c:34: projectile->w = 3;
   5DE7 36 03         [10]  195 	ld	(hl), #0x03
                            196 ;src/entities/projectile.c:35: projectile->h = 2;
   5DE9 3E 02         [ 7]  197 	ld	a, #0x02
   5DEB 12            [ 7]  198 	ld	(de), a
                            199 ;src/entities/projectile.c:36: projectile->damage = 1;
   5DEC DD 6E FE      [19]  200 	ld	l,-2 (ix)
   5DEF DD 66 FF      [19]  201 	ld	h,-1 (ix)
   5DF2 36 01         [10]  202 	ld	(hl), #0x01
                            203 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5DF4 3E 2D         [ 7]  204 	ld	a, #0x2d
   5DF6 02            [ 7]  205 	ld	(bc), a
   5DF7 18 3D         [12]  206 	jr	00109$
   5DF9                     207 00107$:
                            208 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5DF9 DD 7E 09      [19]  209 	ld	a, 9 (ix)
   5DFC 3D            [ 4]  210 	dec	a
   5DFD 20 12         [12]  211 	jr	NZ,00104$
                            212 ;src/entities/projectile.c:39: projectile->w = 2;
   5DFF 36 02         [10]  213 	ld	(hl), #0x02
                            214 ;src/entities/projectile.c:40: projectile->h = 3;
   5E01 3E 03         [ 7]  215 	ld	a, #0x03
   5E03 12            [ 7]  216 	ld	(de), a
                            217 ;src/entities/projectile.c:41: projectile->damage = 2;
   5E04 DD 6E FE      [19]  218 	ld	l,-2 (ix)
   5E07 DD 66 FF      [19]  219 	ld	h,-1 (ix)
   5E0A 36 02         [10]  220 	ld	(hl), #0x02
                            221 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   5E0C 3E 1C         [ 7]  222 	ld	a, #0x1c
   5E0E 02            [ 7]  223 	ld	(bc), a
   5E0F 18 25         [12]  224 	jr	00109$
   5E11                     225 00104$:
                            226 ;src/entities/projectile.c:44: projectile->w = 4;
   5E11 36 04         [10]  227 	ld	(hl), #0x04
                            228 ;src/entities/projectile.c:45: projectile->h = 3;
   5E13 3E 03         [ 7]  229 	ld	a, #0x03
   5E15 12            [ 7]  230 	ld	(de), a
                            231 ;src/entities/projectile.c:46: projectile->damage = 3;
   5E16 DD 6E FE      [19]  232 	ld	l,-2 (ix)
   5E19 DD 66 FF      [19]  233 	ld	h,-1 (ix)
   5E1C 36 03         [10]  234 	ld	(hl), #0x03
                            235 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   5E1E 3E 38         [ 7]  236 	ld	a, #0x38
   5E20 02            [ 7]  237 	ld	(bc), a
                            238 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5E21 C1            [10]  239 	pop	bc
   5E22 C5            [11]  240 	push	bc
   5E23 AF            [ 4]  241 	xor	a, a
   5E24 DD 96 08      [19]  242 	sub	a, 8 (ix)
   5E27 E2 2C 5E      [10]  243 	jp	PO, 00131$
   5E2A EE 80         [ 7]  244 	xor	a, #0x80
   5E2C                     245 00131$:
   5E2C F2 33 5E      [10]  246 	jp	P, 00111$
   5E2F 3E 04         [ 7]  247 	ld	a, #0x04
   5E31 18 02         [12]  248 	jr	00112$
   5E33                     249 00111$:
   5E33 3E FC         [ 7]  250 	ld	a, #0xfc
   5E35                     251 00112$:
   5E35 02            [ 7]  252 	ld	(bc), a
   5E36                     253 00109$:
   5E36 DD F9         [10]  254 	ld	sp, ix
   5E38 DD E1         [14]  255 	pop	ix
   5E3A C9            [10]  256 	ret
                            257 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            258 ;	---------------------------------
                            259 ; Function projectileupdate
                            260 ; ---------------------------------
   5E3B                     261 _projectileupdate::
   5E3B DD E5         [15]  262 	push	ix
   5E3D DD 21 00 00   [14]  263 	ld	ix,#0
   5E41 DD 39         [15]  264 	add	ix,sp
   5E43 3B            [ 6]  265 	dec	sp
                            266 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5E44 DD 7E 05      [19]  267 	ld	a, 5 (ix)
   5E47 DD B6 04      [19]  268 	or	a,4 (ix)
   5E4A 28 4A         [12]  269 	jr	Z,00109$
   5E4C DD 5E 04      [19]  270 	ld	e,4 (ix)
   5E4F DD 56 05      [19]  271 	ld	d,5 (ix)
   5E52 FD 21 06 00   [14]  272 	ld	iy, #0x0006
   5E56 FD 19         [15]  273 	add	iy, de
   5E58 FD 7E 00      [19]  274 	ld	a, 0 (iy)
   5E5B B7            [ 4]  275 	or	a, a
                            276 ;src/entities/projectile.c:54: return;
   5E5C 28 38         [12]  277 	jr	Z,00109$
                            278 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   5E5E 1A            [ 7]  279 	ld	a, (de)
   5E5F 4F            [ 4]  280 	ld	c, a
   5E60 6B            [ 4]  281 	ld	l, e
   5E61 62            [ 4]  282 	ld	h, d
   5E62 23            [ 6]  283 	inc	hl
   5E63 23            [ 6]  284 	inc	hl
   5E64 6E            [ 7]  285 	ld	l, (hl)
   5E65 09            [11]  286 	add	hl, bc
   5E66 7D            [ 4]  287 	ld	a, l
   5E67 12            [ 7]  288 	ld	(de), a
                            289 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   5E68 4B            [ 4]  290 	ld	c, e
   5E69 42            [ 4]  291 	ld	b, d
   5E6A 03            [ 6]  292 	inc	bc
   5E6B 0A            [ 7]  293 	ld	a, (bc)
   5E6C DD 77 FF      [19]  294 	ld	-1 (ix), a
   5E6F 6B            [ 4]  295 	ld	l, e
   5E70 62            [ 4]  296 	ld	h, d
   5E71 23            [ 6]  297 	inc	hl
   5E72 23            [ 6]  298 	inc	hl
   5E73 23            [ 6]  299 	inc	hl
   5E74 6E            [ 7]  300 	ld	l, (hl)
   5E75 DD 7E FF      [19]  301 	ld	a, -1 (ix)
   5E78 85            [ 4]  302 	add	a, l
   5E79 02            [ 7]  303 	ld	(bc), a
                            304 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   5E7A 21 08 00      [10]  305 	ld	hl, #0x0008
   5E7D 19            [11]  306 	add	hl,de
   5E7E 4D            [ 4]  307 	ld	c, l
   5E7F 44            [ 4]  308 	ld	b, h
   5E80 0A            [ 7]  309 	ld	a, (bc)
   5E81 B7            [ 4]  310 	or	a, a
   5E82 28 03         [12]  311 	jr	Z,00105$
                            312 ;src/entities/projectile.c:61: projectile->lifetime--;
   5E84 C6 FF         [ 7]  313 	add	a, #0xff
   5E86 02            [ 7]  314 	ld	(bc), a
   5E87                     315 00105$:
                            316 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   5E87 1A            [ 7]  317 	ld	a, (de)
   5E88 5F            [ 4]  318 	ld	e, a
   5E89 3E 4E         [ 7]  319 	ld	a, #0x4e
   5E8B 93            [ 4]  320 	sub	a, e
   5E8C 38 04         [12]  321 	jr	C,00106$
   5E8E 0A            [ 7]  322 	ld	a, (bc)
   5E8F B7            [ 4]  323 	or	a, a
   5E90 20 04         [12]  324 	jr	NZ,00109$
   5E92                     325 00106$:
                            326 ;src/entities/projectile.c:65: projectile->active = 0;
   5E92 FD 36 00 00   [19]  327 	ld	0 (iy), #0x00
   5E96                     328 00109$:
   5E96 33            [ 6]  329 	inc	sp
   5E97 DD E1         [14]  330 	pop	ix
   5E99 C9            [10]  331 	ret
                            332 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            333 ;	---------------------------------
                            334 ; Function projectilerender
                            335 ; ---------------------------------
   5E9A                     336 _projectilerender::
   5E9A DD E5         [15]  337 	push	ix
   5E9C DD 21 00 00   [14]  338 	ld	ix,#0
   5EA0 DD 39         [15]  339 	add	ix,sp
   5EA2 F5            [11]  340 	push	af
                            341 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   5EA3 DD 7E 05      [19]  342 	ld	a, 5 (ix)
   5EA6 DD B6 04      [19]  343 	or	a,4 (ix)
   5EA9 28 72         [12]  344 	jr	Z,00104$
   5EAB DD 5E 04      [19]  345 	ld	e,4 (ix)
   5EAE DD 56 05      [19]  346 	ld	d,5 (ix)
   5EB1 D5            [11]  347 	push	de
   5EB2 FD E1         [14]  348 	pop	iy
   5EB4 FD 7E 06      [19]  349 	ld	a, 6 (iy)
   5EB7 B7            [ 4]  350 	or	a, a
                            351 ;src/entities/projectile.c:73: return;
   5EB8 28 63         [12]  352 	jr	Z,00104$
                            353 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5EBA 6B            [ 4]  354 	ld	l, e
   5EBB 62            [ 4]  355 	ld	h, d
   5EBC 23            [ 6]  356 	inc	hl
   5EBD 46            [ 7]  357 	ld	b, (hl)
   5EBE 1A            [ 7]  358 	ld	a, (de)
   5EBF D5            [11]  359 	push	de
   5EC0 C5            [11]  360 	push	bc
   5EC1 33            [ 6]  361 	inc	sp
   5EC2 F5            [11]  362 	push	af
   5EC3 33            [ 6]  363 	inc	sp
   5EC4 21 00 C0      [10]  364 	ld	hl, #0xc000
   5EC7 E5            [11]  365 	push	hl
   5EC8 CD CB 61      [17]  366 	call	_cpct_getScreenPtr
   5ECB 4D            [ 4]  367 	ld	c, l
   5ECC 44            [ 4]  368 	ld	b, h
   5ECD D1            [10]  369 	pop	de
                            370 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? cpct_px2byteM0(15, 15) : (projectile->weapon == 1 ? cpct_px2byteM0(11, 11) : cpct_px2byteM0(5, 5)), projectile->w, projectile->h);
   5ECE D5            [11]  371 	push	de
   5ECF FD E1         [14]  372 	pop	iy
   5ED1 FD 7E 05      [19]  373 	ld	a, 5 (iy)
   5ED4 DD 77 FF      [19]  374 	ld	-1 (ix), a
   5ED7 D5            [11]  375 	push	de
   5ED8 FD E1         [14]  376 	pop	iy
   5EDA FD 7E 04      [19]  377 	ld	a, 4 (iy)
   5EDD DD 77 FE      [19]  378 	ld	-2 (ix), a
   5EE0 EB            [ 4]  379 	ex	de,hl
   5EE1 11 09 00      [10]  380 	ld	de, #0x0009
   5EE4 19            [11]  381 	add	hl, de
   5EE5 7E            [ 7]  382 	ld	a, (hl)
   5EE6 B7            [ 4]  383 	or	a, a
   5EE7 20 0C         [12]  384 	jr	NZ,00106$
   5EE9 C5            [11]  385 	push	bc
   5EEA 21 0F 0F      [10]  386 	ld	hl, #0x0f0f
   5EED E5            [11]  387 	push	hl
   5EEE CD D8 60      [17]  388 	call	_cpct_px2byteM0
   5EF1 55            [ 4]  389 	ld	d, l
   5EF2 C1            [10]  390 	pop	bc
   5EF3 18 18         [12]  391 	jr	00107$
   5EF5                     392 00106$:
   5EF5 3D            [ 4]  393 	dec	a
   5EF6 20 0B         [12]  394 	jr	NZ,00108$
   5EF8 C5            [11]  395 	push	bc
   5EF9 21 0B 0B      [10]  396 	ld	hl, #0x0b0b
   5EFC E5            [11]  397 	push	hl
   5EFD CD D8 60      [17]  398 	call	_cpct_px2byteM0
   5F00 C1            [10]  399 	pop	bc
   5F01 18 09         [12]  400 	jr	00109$
   5F03                     401 00108$:
   5F03 C5            [11]  402 	push	bc
   5F04 21 05 05      [10]  403 	ld	hl, #0x0505
   5F07 E5            [11]  404 	push	hl
   5F08 CD D8 60      [17]  405 	call	_cpct_px2byteM0
   5F0B C1            [10]  406 	pop	bc
   5F0C                     407 00109$:
   5F0C 55            [ 4]  408 	ld	d, l
   5F0D                     409 00107$:
   5F0D DD 66 FF      [19]  410 	ld	h, -1 (ix)
   5F10 DD 6E FE      [19]  411 	ld	l, -2 (ix)
   5F13 E5            [11]  412 	push	hl
   5F14 D5            [11]  413 	push	de
   5F15 33            [ 6]  414 	inc	sp
   5F16 C5            [11]  415 	push	bc
   5F17 CD 12 61      [17]  416 	call	_cpct_drawSolidBox
   5F1A F1            [10]  417 	pop	af
   5F1B F1            [10]  418 	pop	af
   5F1C 33            [ 6]  419 	inc	sp
   5F1D                     420 00104$:
   5F1D DD F9         [10]  421 	ld	sp, ix
   5F1F DD E1         [14]  422 	pop	ix
   5F21 C9            [10]  423 	ret
                            424 	.area _CODE
                            425 	.area _INITIALIZER
                            426 	.area _CABS (ABS)
