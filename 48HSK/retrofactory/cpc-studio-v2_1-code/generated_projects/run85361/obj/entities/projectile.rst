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
   5876                      52 _projectileinit::
                             53 ;src/entities/projectile.c:5: if (!projectile) {
   5876 21 03 00      [10]   54 	ld	hl, #2+1
   5879 39            [11]   55 	add	hl, sp
   587A 7E            [ 7]   56 	ld	a, (hl)
   587B 2B            [ 6]   57 	dec	hl
   587C B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:6: return;
   587D C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:9: projectile->x = 0;
   587E D1            [10]   62 	pop	de
   587F C1            [10]   63 	pop	bc
   5880 C5            [11]   64 	push	bc
   5881 D5            [11]   65 	push	de
   5882 AF            [ 4]   66 	xor	a, a
   5883 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:10: projectile->y = 0;
   5884 59            [ 4]   69 	ld	e, c
   5885 50            [ 4]   70 	ld	d, b
   5886 13            [ 6]   71 	inc	de
   5887 AF            [ 4]   72 	xor	a, a
   5888 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:11: projectile->vx = 0;
   5889 59            [ 4]   75 	ld	e, c
   588A 50            [ 4]   76 	ld	d, b
   588B 13            [ 6]   77 	inc	de
   588C 13            [ 6]   78 	inc	de
   588D AF            [ 4]   79 	xor	a, a
   588E 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:12: projectile->vy = 0;
   588F 59            [ 4]   82 	ld	e, c
   5890 50            [ 4]   83 	ld	d, b
   5891 13            [ 6]   84 	inc	de
   5892 13            [ 6]   85 	inc	de
   5893 13            [ 6]   86 	inc	de
   5894 AF            [ 4]   87 	xor	a, a
   5895 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:13: projectile->w = 2;
   5896 21 04 00      [10]   90 	ld	hl, #0x0004
   5899 09            [11]   91 	add	hl, bc
   589A 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:14: projectile->h = 2;
   589C 21 05 00      [10]   94 	ld	hl, #0x0005
   589F 09            [11]   95 	add	hl, bc
   58A0 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:15: projectile->active = 0;
   58A2 21 06 00      [10]   98 	ld	hl, #0x0006
   58A5 09            [11]   99 	add	hl, bc
   58A6 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:16: projectile->damage = 1;
   58A8 21 07 00      [10]  102 	ld	hl, #0x0007
   58AB 09            [11]  103 	add	hl, bc
   58AC 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   58AE 21 08 00      [10]  106 	ld	hl, #0x0008
   58B1 09            [11]  107 	add	hl, bc
   58B2 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:18: projectile->weapon = 0;
   58B4 21 09 00      [10]  110 	ld	hl, #0x0009
   58B7 09            [11]  111 	add	hl, bc
   58B8 36 00         [10]  112 	ld	(hl), #0x00
   58BA C9            [10]  113 	ret
                            114 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            115 ;	---------------------------------
                            116 ; Function projectilefire
                            117 ; ---------------------------------
   58BB                     118 _projectilefire::
   58BB DD E5         [15]  119 	push	ix
   58BD DD 21 00 00   [14]  120 	ld	ix,#0
   58C1 DD 39         [15]  121 	add	ix,sp
   58C3 F5            [11]  122 	push	af
   58C4 F5            [11]  123 	push	af
                            124 ;src/entities/projectile.c:22: if (!projectile) {
   58C5 DD 7E 05      [19]  125 	ld	a, 5 (ix)
   58C8 DD B6 04      [19]  126 	or	a,4 (ix)
                            127 ;src/entities/projectile.c:23: return;
   58CB CA 74 59      [10]  128 	jp	Z,00109$
                            129 ;src/entities/projectile.c:26: projectile->x = x;
   58CE DD 4E 04      [19]  130 	ld	c,4 (ix)
   58D1 DD 46 05      [19]  131 	ld	b,5 (ix)
   58D4 DD 7E 06      [19]  132 	ld	a, 6 (ix)
   58D7 02            [ 7]  133 	ld	(bc), a
                            134 ;src/entities/projectile.c:27: projectile->y = y;
   58D8 59            [ 4]  135 	ld	e, c
   58D9 50            [ 4]  136 	ld	d, b
   58DA 13            [ 6]  137 	inc	de
   58DB DD 7E 07      [19]  138 	ld	a, 7 (ix)
   58DE 12            [ 7]  139 	ld	(de), a
                            140 ;src/entities/projectile.c:28: projectile->vx = dir;
   58DF 21 02 00      [10]  141 	ld	hl, #0x0002
   58E2 09            [11]  142 	add	hl,bc
   58E3 E3            [19]  143 	ex	(sp), hl
   58E4 E1            [10]  144 	pop	hl
   58E5 E5            [11]  145 	push	hl
   58E6 DD 7E 08      [19]  146 	ld	a, 8 (ix)
   58E9 77            [ 7]  147 	ld	(hl), a
                            148 ;src/entities/projectile.c:29: projectile->vy = 0;
   58EA 59            [ 4]  149 	ld	e, c
   58EB 50            [ 4]  150 	ld	d, b
   58EC 13            [ 6]  151 	inc	de
   58ED 13            [ 6]  152 	inc	de
   58EE 13            [ 6]  153 	inc	de
   58EF AF            [ 4]  154 	xor	a, a
   58F0 12            [ 7]  155 	ld	(de), a
                            156 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   58F1 21 09 00      [10]  157 	ld	hl, #0x0009
   58F4 09            [11]  158 	add	hl, bc
   58F5 DD 7E 09      [19]  159 	ld	a, 9 (ix)
   58F8 77            [ 7]  160 	ld	(hl), a
                            161 ;src/entities/projectile.c:31: projectile->active = 1;
   58F9 21 06 00      [10]  162 	ld	hl, #0x0006
   58FC 09            [11]  163 	add	hl, bc
   58FD 36 01         [10]  164 	ld	(hl), #0x01
                            165 ;src/entities/projectile.c:34: projectile->w = 3;
   58FF 21 04 00      [10]  166 	ld	hl, #0x0004
   5902 09            [11]  167 	add	hl, bc
                            168 ;src/entities/projectile.c:35: projectile->h = 2;
   5903 79            [ 4]  169 	ld	a, c
   5904 C6 05         [ 7]  170 	add	a, #0x05
   5906 5F            [ 4]  171 	ld	e, a
   5907 78            [ 4]  172 	ld	a, b
   5908 CE 00         [ 7]  173 	adc	a, #0x00
   590A 57            [ 4]  174 	ld	d, a
                            175 ;src/entities/projectile.c:36: projectile->damage = 1;
   590B 79            [ 4]  176 	ld	a, c
   590C C6 07         [ 7]  177 	add	a, #0x07
   590E DD 77 FE      [19]  178 	ld	-2 (ix), a
   5911 78            [ 4]  179 	ld	a, b
   5912 CE 00         [ 7]  180 	adc	a, #0x00
   5914 DD 77 FF      [19]  181 	ld	-1 (ix), a
                            182 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5917 79            [ 4]  183 	ld	a, c
   5918 C6 08         [ 7]  184 	add	a, #0x08
   591A 4F            [ 4]  185 	ld	c, a
   591B 78            [ 4]  186 	ld	a, b
   591C CE 00         [ 7]  187 	adc	a, #0x00
   591E 47            [ 4]  188 	ld	b, a
                            189 ;src/entities/projectile.c:33: if (weapon == 0) {
   591F DD 7E 09      [19]  190 	ld	a, 9 (ix)
   5922 B7            [ 4]  191 	or	a, a
   5923 20 12         [12]  192 	jr	NZ,00107$
                            193 ;src/entities/projectile.c:34: projectile->w = 3;
   5925 36 03         [10]  194 	ld	(hl), #0x03
                            195 ;src/entities/projectile.c:35: projectile->h = 2;
   5927 3E 02         [ 7]  196 	ld	a, #0x02
   5929 12            [ 7]  197 	ld	(de), a
                            198 ;src/entities/projectile.c:36: projectile->damage = 1;
   592A DD 6E FE      [19]  199 	ld	l,-2 (ix)
   592D DD 66 FF      [19]  200 	ld	h,-1 (ix)
   5930 36 01         [10]  201 	ld	(hl), #0x01
                            202 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5932 3E 2D         [ 7]  203 	ld	a, #0x2d
   5934 02            [ 7]  204 	ld	(bc), a
   5935 18 3D         [12]  205 	jr	00109$
   5937                     206 00107$:
                            207 ;src/entities/projectile.c:38: } else if (weapon == 1) {
   5937 DD 7E 09      [19]  208 	ld	a, 9 (ix)
   593A 3D            [ 4]  209 	dec	a
   593B 20 12         [12]  210 	jr	NZ,00104$
                            211 ;src/entities/projectile.c:39: projectile->w = 2;
   593D 36 02         [10]  212 	ld	(hl), #0x02
                            213 ;src/entities/projectile.c:40: projectile->h = 3;
   593F 3E 03         [ 7]  214 	ld	a, #0x03
   5941 12            [ 7]  215 	ld	(de), a
                            216 ;src/entities/projectile.c:41: projectile->damage = 2;
   5942 DD 6E FE      [19]  217 	ld	l,-2 (ix)
   5945 DD 66 FF      [19]  218 	ld	h,-1 (ix)
   5948 36 02         [10]  219 	ld	(hl), #0x02
                            220 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   594A 3E 1C         [ 7]  221 	ld	a, #0x1c
   594C 02            [ 7]  222 	ld	(bc), a
   594D 18 25         [12]  223 	jr	00109$
   594F                     224 00104$:
                            225 ;src/entities/projectile.c:44: projectile->w = 4;
   594F 36 04         [10]  226 	ld	(hl), #0x04
                            227 ;src/entities/projectile.c:45: projectile->h = 3;
   5951 3E 03         [ 7]  228 	ld	a, #0x03
   5953 12            [ 7]  229 	ld	(de), a
                            230 ;src/entities/projectile.c:46: projectile->damage = 3;
   5954 DD 6E FE      [19]  231 	ld	l,-2 (ix)
   5957 DD 66 FF      [19]  232 	ld	h,-1 (ix)
   595A 36 03         [10]  233 	ld	(hl), #0x03
                            234 ;src/entities/projectile.c:47: projectile->lifetime = 56;
   595C 3E 38         [ 7]  235 	ld	a, #0x38
   595E 02            [ 7]  236 	ld	(bc), a
                            237 ;src/entities/projectile.c:48: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   595F C1            [10]  238 	pop	bc
   5960 C5            [11]  239 	push	bc
   5961 AF            [ 4]  240 	xor	a, a
   5962 DD 96 08      [19]  241 	sub	a, 8 (ix)
   5965 E2 6A 59      [10]  242 	jp	PO, 00131$
   5968 EE 80         [ 7]  243 	xor	a, #0x80
   596A                     244 00131$:
   596A F2 71 59      [10]  245 	jp	P, 00111$
   596D 3E 04         [ 7]  246 	ld	a, #0x04
   596F 18 02         [12]  247 	jr	00112$
   5971                     248 00111$:
   5971 3E FC         [ 7]  249 	ld	a, #0xfc
   5973                     250 00112$:
   5973 02            [ 7]  251 	ld	(bc), a
   5974                     252 00109$:
   5974 DD F9         [10]  253 	ld	sp, ix
   5976 DD E1         [14]  254 	pop	ix
   5978 C9            [10]  255 	ret
                            256 ;src/entities/projectile.c:52: void projectileupdate(Projectile* projectile) {
                            257 ;	---------------------------------
                            258 ; Function projectileupdate
                            259 ; ---------------------------------
   5979                     260 _projectileupdate::
   5979 DD E5         [15]  261 	push	ix
   597B DD 21 00 00   [14]  262 	ld	ix,#0
   597F DD 39         [15]  263 	add	ix,sp
   5981 3B            [ 6]  264 	dec	sp
                            265 ;src/entities/projectile.c:53: if (!projectile || !projectile->active) {
   5982 DD 7E 05      [19]  266 	ld	a, 5 (ix)
   5985 DD B6 04      [19]  267 	or	a,4 (ix)
   5988 28 4A         [12]  268 	jr	Z,00109$
   598A DD 5E 04      [19]  269 	ld	e,4 (ix)
   598D DD 56 05      [19]  270 	ld	d,5 (ix)
   5990 FD 21 06 00   [14]  271 	ld	iy, #0x0006
   5994 FD 19         [15]  272 	add	iy, de
   5996 FD 7E 00      [19]  273 	ld	a, 0 (iy)
   5999 B7            [ 4]  274 	or	a, a
                            275 ;src/entities/projectile.c:54: return;
   599A 28 38         [12]  276 	jr	Z,00109$
                            277 ;src/entities/projectile.c:57: projectile->x = (u8)(projectile->x + projectile->vx);
   599C 1A            [ 7]  278 	ld	a, (de)
   599D 4F            [ 4]  279 	ld	c, a
   599E 6B            [ 4]  280 	ld	l, e
   599F 62            [ 4]  281 	ld	h, d
   59A0 23            [ 6]  282 	inc	hl
   59A1 23            [ 6]  283 	inc	hl
   59A2 6E            [ 7]  284 	ld	l, (hl)
   59A3 09            [11]  285 	add	hl, bc
   59A4 7D            [ 4]  286 	ld	a, l
   59A5 12            [ 7]  287 	ld	(de), a
                            288 ;src/entities/projectile.c:58: projectile->y = (u8)(projectile->y + projectile->vy);
   59A6 4B            [ 4]  289 	ld	c, e
   59A7 42            [ 4]  290 	ld	b, d
   59A8 03            [ 6]  291 	inc	bc
   59A9 0A            [ 7]  292 	ld	a, (bc)
   59AA DD 77 FF      [19]  293 	ld	-1 (ix), a
   59AD 6B            [ 4]  294 	ld	l, e
   59AE 62            [ 4]  295 	ld	h, d
   59AF 23            [ 6]  296 	inc	hl
   59B0 23            [ 6]  297 	inc	hl
   59B1 23            [ 6]  298 	inc	hl
   59B2 6E            [ 7]  299 	ld	l, (hl)
   59B3 DD 7E FF      [19]  300 	ld	a, -1 (ix)
   59B6 85            [ 4]  301 	add	a, l
   59B7 02            [ 7]  302 	ld	(bc), a
                            303 ;src/entities/projectile.c:60: if (projectile->lifetime) {
   59B8 21 08 00      [10]  304 	ld	hl, #0x0008
   59BB 19            [11]  305 	add	hl,de
   59BC 4D            [ 4]  306 	ld	c, l
   59BD 44            [ 4]  307 	ld	b, h
   59BE 0A            [ 7]  308 	ld	a, (bc)
   59BF B7            [ 4]  309 	or	a, a
   59C0 28 03         [12]  310 	jr	Z,00105$
                            311 ;src/entities/projectile.c:61: projectile->lifetime--;
   59C2 C6 FF         [ 7]  312 	add	a, #0xff
   59C4 02            [ 7]  313 	ld	(bc), a
   59C5                     314 00105$:
                            315 ;src/entities/projectile.c:64: if (projectile->x > 78 || projectile->lifetime == 0) {
   59C5 1A            [ 7]  316 	ld	a, (de)
   59C6 5F            [ 4]  317 	ld	e, a
   59C7 3E 4E         [ 7]  318 	ld	a, #0x4e
   59C9 93            [ 4]  319 	sub	a, e
   59CA 38 04         [12]  320 	jr	C,00106$
   59CC 0A            [ 7]  321 	ld	a, (bc)
   59CD B7            [ 4]  322 	or	a, a
   59CE 20 04         [12]  323 	jr	NZ,00109$
   59D0                     324 00106$:
                            325 ;src/entities/projectile.c:65: projectile->active = 0;
   59D0 FD 36 00 00   [19]  326 	ld	0 (iy), #0x00
   59D4                     327 00109$:
   59D4 33            [ 6]  328 	inc	sp
   59D5 DD E1         [14]  329 	pop	ix
   59D7 C9            [10]  330 	ret
                            331 ;src/entities/projectile.c:69: void projectilerender(const Projectile* projectile) {
                            332 ;	---------------------------------
                            333 ; Function projectilerender
                            334 ; ---------------------------------
   59D8                     335 _projectilerender::
   59D8 DD E5         [15]  336 	push	ix
   59DA DD 21 00 00   [14]  337 	ld	ix,#0
   59DE DD 39         [15]  338 	add	ix,sp
   59E0 F5            [11]  339 	push	af
                            340 ;src/entities/projectile.c:72: if (!projectile || !projectile->active) {
   59E1 DD 7E 05      [19]  341 	ld	a, 5 (ix)
   59E4 DD B6 04      [19]  342 	or	a,4 (ix)
   59E7 28 5B         [12]  343 	jr	Z,00104$
   59E9 DD 5E 04      [19]  344 	ld	e,4 (ix)
   59EC DD 56 05      [19]  345 	ld	d,5 (ix)
   59EF D5            [11]  346 	push	de
   59F0 FD E1         [14]  347 	pop	iy
   59F2 FD 7E 06      [19]  348 	ld	a, 6 (iy)
   59F5 B7            [ 4]  349 	or	a, a
                            350 ;src/entities/projectile.c:73: return;
   59F6 28 4C         [12]  351 	jr	Z,00104$
                            352 ;src/entities/projectile.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   59F8 6B            [ 4]  353 	ld	l, e
   59F9 62            [ 4]  354 	ld	h, d
   59FA 23            [ 6]  355 	inc	hl
   59FB 46            [ 7]  356 	ld	b, (hl)
   59FC 1A            [ 7]  357 	ld	a, (de)
   59FD D5            [11]  358 	push	de
   59FE C5            [11]  359 	push	bc
   59FF 33            [ 6]  360 	inc	sp
   5A00 F5            [11]  361 	push	af
   5A01 33            [ 6]  362 	inc	sp
   5A02 21 00 C0      [10]  363 	ld	hl, #0xc000
   5A05 E5            [11]  364 	push	hl
   5A06 CD B3 5C      [17]  365 	call	_cpct_getScreenPtr
   5A09 4D            [ 4]  366 	ld	c, l
   5A0A 44            [ 4]  367 	ld	b, h
   5A0B D1            [10]  368 	pop	de
                            369 ;src/entities/projectile.c:77: cpct_drawSolidBox(pvmem, projectile->weapon == 0 ? 0x0F : (projectile->weapon == 1 ? 0x6B : 0x5A), projectile->w, projectile->h);
   5A0C D5            [11]  370 	push	de
   5A0D FD E1         [14]  371 	pop	iy
   5A0F FD 7E 05      [19]  372 	ld	a, 5 (iy)
   5A12 DD 77 FF      [19]  373 	ld	-1 (ix), a
   5A15 D5            [11]  374 	push	de
   5A16 FD E1         [14]  375 	pop	iy
   5A18 FD 7E 04      [19]  376 	ld	a, 4 (iy)
   5A1B DD 77 FE      [19]  377 	ld	-2 (ix), a
   5A1E EB            [ 4]  378 	ex	de,hl
   5A1F 11 09 00      [10]  379 	ld	de, #0x0009
   5A22 19            [11]  380 	add	hl, de
   5A23 7E            [ 7]  381 	ld	a, (hl)
   5A24 B7            [ 4]  382 	or	a, a
   5A25 20 04         [12]  383 	jr	NZ,00106$
   5A27 16 0F         [ 7]  384 	ld	d, #0x0f
   5A29 18 09         [12]  385 	jr	00107$
   5A2B                     386 00106$:
   5A2B 3D            [ 4]  387 	dec	a
   5A2C 20 04         [12]  388 	jr	NZ,00108$
   5A2E 16 6B         [ 7]  389 	ld	d, #0x6b
   5A30 18 02         [12]  390 	jr	00109$
   5A32                     391 00108$:
   5A32 16 5A         [ 7]  392 	ld	d, #0x5a
   5A34                     393 00109$:
   5A34                     394 00107$:
   5A34 DD 66 FF      [19]  395 	ld	h, -1 (ix)
   5A37 DD 6E FE      [19]  396 	ld	l, -2 (ix)
   5A3A E5            [11]  397 	push	hl
   5A3B D5            [11]  398 	push	de
   5A3C 33            [ 6]  399 	inc	sp
   5A3D C5            [11]  400 	push	bc
   5A3E CD FA 5B      [17]  401 	call	_cpct_drawSolidBox
   5A41 F1            [10]  402 	pop	af
   5A42 F1            [10]  403 	pop	af
   5A43 33            [ 6]  404 	inc	sp
   5A44                     405 00104$:
   5A44 DD F9         [10]  406 	ld	sp, ix
   5A46 DD E1         [14]  407 	pop	ix
   5A48 C9            [10]  408 	ret
                            409 	.area _CODE
                            410 	.area _INITIALIZER
                            411 	.area _CABS (ABS)
