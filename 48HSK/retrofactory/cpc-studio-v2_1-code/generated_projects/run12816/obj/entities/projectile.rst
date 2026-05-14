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
   55D9                      52 _projectileinit::
                             53 ;src/entities/projectile.c:5: if (!projectile) {
   55D9 21 03 00      [10]   54 	ld	hl, #2+1
   55DC 39            [11]   55 	add	hl, sp
   55DD 7E            [ 7]   56 	ld	a, (hl)
   55DE 2B            [ 6]   57 	dec	hl
   55DF B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:6: return;
   55E0 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:9: projectile->x = 0;
   55E1 D1            [10]   62 	pop	de
   55E2 C1            [10]   63 	pop	bc
   55E3 C5            [11]   64 	push	bc
   55E4 D5            [11]   65 	push	de
   55E5 AF            [ 4]   66 	xor	a, a
   55E6 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:10: projectile->y = 0;
   55E7 59            [ 4]   69 	ld	e, c
   55E8 50            [ 4]   70 	ld	d, b
   55E9 13            [ 6]   71 	inc	de
   55EA AF            [ 4]   72 	xor	a, a
   55EB 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:11: projectile->vx = 0;
   55EC 59            [ 4]   75 	ld	e, c
   55ED 50            [ 4]   76 	ld	d, b
   55EE 13            [ 6]   77 	inc	de
   55EF 13            [ 6]   78 	inc	de
   55F0 AF            [ 4]   79 	xor	a, a
   55F1 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:12: projectile->vy = 0;
   55F2 59            [ 4]   82 	ld	e, c
   55F3 50            [ 4]   83 	ld	d, b
   55F4 13            [ 6]   84 	inc	de
   55F5 13            [ 6]   85 	inc	de
   55F6 13            [ 6]   86 	inc	de
   55F7 AF            [ 4]   87 	xor	a, a
   55F8 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:13: projectile->w = 2;
   55F9 21 04 00      [10]   90 	ld	hl, #0x0004
   55FC 09            [11]   91 	add	hl, bc
   55FD 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:14: projectile->h = 2;
   55FF 21 05 00      [10]   94 	ld	hl, #0x0005
   5602 09            [11]   95 	add	hl, bc
   5603 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:15: projectile->active = 0;
   5605 21 06 00      [10]   98 	ld	hl, #0x0006
   5608 09            [11]   99 	add	hl, bc
   5609 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:16: projectile->damage = 1;
   560B 21 07 00      [10]  102 	ld	hl, #0x0007
   560E 09            [11]  103 	add	hl, bc
   560F 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:17: projectile->lifetime = 0;
   5611 21 08 00      [10]  106 	ld	hl, #0x0008
   5614 09            [11]  107 	add	hl, bc
   5615 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:18: projectile->weapon = 0;
   5617 21 09 00      [10]  110 	ld	hl, #0x0009
   561A 09            [11]  111 	add	hl, bc
   561B 36 00         [10]  112 	ld	(hl), #0x00
   561D C9            [10]  113 	ret
                            114 ;src/entities/projectile.c:21: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            115 ;	---------------------------------
                            116 ; Function projectilefire
                            117 ; ---------------------------------
   561E                     118 _projectilefire::
   561E DD E5         [15]  119 	push	ix
   5620 DD 21 00 00   [14]  120 	ld	ix,#0
   5624 DD 39         [15]  121 	add	ix,sp
   5626 F5            [11]  122 	push	af
                            123 ;src/entities/projectile.c:22: if (!projectile) {
   5627 DD 7E 05      [19]  124 	ld	a, 5 (ix)
   562A DD B6 04      [19]  125 	or	a,4 (ix)
                            126 ;src/entities/projectile.c:23: return;
   562D 28 6E         [12]  127 	jr	Z,00106$
                            128 ;src/entities/projectile.c:26: projectile->x = x;
   562F DD 5E 04      [19]  129 	ld	e,4 (ix)
   5632 DD 56 05      [19]  130 	ld	d,5 (ix)
   5635 DD 7E 06      [19]  131 	ld	a, 6 (ix)
   5638 12            [ 7]  132 	ld	(de), a
                            133 ;src/entities/projectile.c:27: projectile->y = y;
   5639 4B            [ 4]  134 	ld	c, e
   563A 42            [ 4]  135 	ld	b, d
   563B 03            [ 6]  136 	inc	bc
   563C DD 7E 07      [19]  137 	ld	a, 7 (ix)
   563F 02            [ 7]  138 	ld	(bc), a
                            139 ;src/entities/projectile.c:28: projectile->vx = dir;
   5640 4B            [ 4]  140 	ld	c, e
   5641 42            [ 4]  141 	ld	b, d
   5642 03            [ 6]  142 	inc	bc
   5643 03            [ 6]  143 	inc	bc
   5644 DD 7E 08      [19]  144 	ld	a, 8 (ix)
   5647 02            [ 7]  145 	ld	(bc), a
                            146 ;src/entities/projectile.c:29: projectile->vy = 0;
   5648 4B            [ 4]  147 	ld	c, e
   5649 42            [ 4]  148 	ld	b, d
   564A 03            [ 6]  149 	inc	bc
   564B 03            [ 6]  150 	inc	bc
   564C 03            [ 6]  151 	inc	bc
   564D AF            [ 4]  152 	xor	a, a
   564E 02            [ 7]  153 	ld	(bc), a
                            154 ;src/entities/projectile.c:30: projectile->weapon = weapon;
   564F 21 09 00      [10]  155 	ld	hl, #0x0009
   5652 19            [11]  156 	add	hl, de
   5653 DD 7E 09      [19]  157 	ld	a, 9 (ix)
   5656 77            [ 7]  158 	ld	(hl), a
                            159 ;src/entities/projectile.c:31: projectile->active = 1;
   5657 21 06 00      [10]  160 	ld	hl, #0x0006
   565A 19            [11]  161 	add	hl, de
   565B 36 01         [10]  162 	ld	(hl), #0x01
                            163 ;src/entities/projectile.c:34: projectile->w = 3;
   565D 21 04 00      [10]  164 	ld	hl, #0x0004
   5660 19            [11]  165 	add	hl, de
                            166 ;src/entities/projectile.c:35: projectile->h = 2;
   5661 7B            [ 4]  167 	ld	a, e
   5662 C6 05         [ 7]  168 	add	a, #0x05
   5664 4F            [ 4]  169 	ld	c, a
   5665 7A            [ 4]  170 	ld	a, d
   5666 CE 00         [ 7]  171 	adc	a, #0x00
   5668 47            [ 4]  172 	ld	b, a
                            173 ;src/entities/projectile.c:36: projectile->damage = 1;
   5669 7B            [ 4]  174 	ld	a, e
   566A C6 07         [ 7]  175 	add	a, #0x07
   566C DD 77 FE      [19]  176 	ld	-2 (ix), a
   566F 7A            [ 4]  177 	ld	a, d
   5670 CE 00         [ 7]  178 	adc	a, #0x00
   5672 DD 77 FF      [19]  179 	ld	-1 (ix), a
                            180 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   5675 7B            [ 4]  181 	ld	a, e
   5676 C6 08         [ 7]  182 	add	a, #0x08
   5678 5F            [ 4]  183 	ld	e, a
   5679 7A            [ 4]  184 	ld	a, d
   567A CE 00         [ 7]  185 	adc	a, #0x00
   567C 57            [ 4]  186 	ld	d, a
                            187 ;src/entities/projectile.c:33: if (weapon == 0) {
   567D DD 7E 09      [19]  188 	ld	a, 9 (ix)
   5680 B7            [ 4]  189 	or	a, a
   5681 20 0E         [12]  190 	jr	NZ,00104$
                            191 ;src/entities/projectile.c:34: projectile->w = 3;
   5683 36 03         [10]  192 	ld	(hl), #0x03
                            193 ;src/entities/projectile.c:35: projectile->h = 2;
   5685 3E 02         [ 7]  194 	ld	a, #0x02
   5687 02            [ 7]  195 	ld	(bc), a
                            196 ;src/entities/projectile.c:36: projectile->damage = 1;
   5688 E1            [10]  197 	pop	hl
   5689 E5            [11]  198 	push	hl
   568A 36 01         [10]  199 	ld	(hl), #0x01
                            200 ;src/entities/projectile.c:37: projectile->lifetime = 45;
   568C 3E 2D         [ 7]  201 	ld	a, #0x2d
   568E 12            [ 7]  202 	ld	(de), a
   568F 18 0C         [12]  203 	jr	00106$
   5691                     204 00104$:
                            205 ;src/entities/projectile.c:39: projectile->w = 2;
   5691 36 02         [10]  206 	ld	(hl), #0x02
                            207 ;src/entities/projectile.c:40: projectile->h = 3;
   5693 3E 03         [ 7]  208 	ld	a, #0x03
   5695 02            [ 7]  209 	ld	(bc), a
                            210 ;src/entities/projectile.c:41: projectile->damage = 2;
   5696 E1            [10]  211 	pop	hl
   5697 E5            [11]  212 	push	hl
   5698 36 02         [10]  213 	ld	(hl), #0x02
                            214 ;src/entities/projectile.c:42: projectile->lifetime = 28;
   569A 3E 1C         [ 7]  215 	ld	a, #0x1c
   569C 12            [ 7]  216 	ld	(de), a
   569D                     217 00106$:
   569D DD F9         [10]  218 	ld	sp, ix
   569F DD E1         [14]  219 	pop	ix
   56A1 C9            [10]  220 	ret
                            221 ;src/entities/projectile.c:46: void projectileupdate(Projectile* projectile) {
                            222 ;	---------------------------------
                            223 ; Function projectileupdate
                            224 ; ---------------------------------
   56A2                     225 _projectileupdate::
   56A2 DD E5         [15]  226 	push	ix
   56A4 DD 21 00 00   [14]  227 	ld	ix,#0
   56A8 DD 39         [15]  228 	add	ix,sp
   56AA 3B            [ 6]  229 	dec	sp
                            230 ;src/entities/projectile.c:47: if (!projectile || !projectile->active) {
   56AB DD 7E 05      [19]  231 	ld	a, 5 (ix)
   56AE DD B6 04      [19]  232 	or	a,4 (ix)
   56B1 28 4A         [12]  233 	jr	Z,00109$
   56B3 DD 5E 04      [19]  234 	ld	e,4 (ix)
   56B6 DD 56 05      [19]  235 	ld	d,5 (ix)
   56B9 FD 21 06 00   [14]  236 	ld	iy, #0x0006
   56BD FD 19         [15]  237 	add	iy, de
   56BF FD 7E 00      [19]  238 	ld	a, 0 (iy)
   56C2 B7            [ 4]  239 	or	a, a
                            240 ;src/entities/projectile.c:48: return;
   56C3 28 38         [12]  241 	jr	Z,00109$
                            242 ;src/entities/projectile.c:51: projectile->x = (u8)(projectile->x + projectile->vx);
   56C5 1A            [ 7]  243 	ld	a, (de)
   56C6 4F            [ 4]  244 	ld	c, a
   56C7 6B            [ 4]  245 	ld	l, e
   56C8 62            [ 4]  246 	ld	h, d
   56C9 23            [ 6]  247 	inc	hl
   56CA 23            [ 6]  248 	inc	hl
   56CB 6E            [ 7]  249 	ld	l, (hl)
   56CC 09            [11]  250 	add	hl, bc
   56CD 7D            [ 4]  251 	ld	a, l
   56CE 12            [ 7]  252 	ld	(de), a
                            253 ;src/entities/projectile.c:52: projectile->y = (u8)(projectile->y + projectile->vy);
   56CF 4B            [ 4]  254 	ld	c, e
   56D0 42            [ 4]  255 	ld	b, d
   56D1 03            [ 6]  256 	inc	bc
   56D2 0A            [ 7]  257 	ld	a, (bc)
   56D3 DD 77 FF      [19]  258 	ld	-1 (ix), a
   56D6 6B            [ 4]  259 	ld	l, e
   56D7 62            [ 4]  260 	ld	h, d
   56D8 23            [ 6]  261 	inc	hl
   56D9 23            [ 6]  262 	inc	hl
   56DA 23            [ 6]  263 	inc	hl
   56DB 6E            [ 7]  264 	ld	l, (hl)
   56DC DD 7E FF      [19]  265 	ld	a, -1 (ix)
   56DF 85            [ 4]  266 	add	a, l
   56E0 02            [ 7]  267 	ld	(bc), a
                            268 ;src/entities/projectile.c:54: if (projectile->lifetime) {
   56E1 21 08 00      [10]  269 	ld	hl, #0x0008
   56E4 19            [11]  270 	add	hl,de
   56E5 4D            [ 4]  271 	ld	c, l
   56E6 44            [ 4]  272 	ld	b, h
   56E7 0A            [ 7]  273 	ld	a, (bc)
   56E8 B7            [ 4]  274 	or	a, a
   56E9 28 03         [12]  275 	jr	Z,00105$
                            276 ;src/entities/projectile.c:55: projectile->lifetime--;
   56EB C6 FF         [ 7]  277 	add	a, #0xff
   56ED 02            [ 7]  278 	ld	(bc), a
   56EE                     279 00105$:
                            280 ;src/entities/projectile.c:58: if (projectile->x > 78 || projectile->lifetime == 0) {
   56EE 1A            [ 7]  281 	ld	a, (de)
   56EF 5F            [ 4]  282 	ld	e, a
   56F0 3E 4E         [ 7]  283 	ld	a, #0x4e
   56F2 93            [ 4]  284 	sub	a, e
   56F3 38 04         [12]  285 	jr	C,00106$
   56F5 0A            [ 7]  286 	ld	a, (bc)
   56F6 B7            [ 4]  287 	or	a, a
   56F7 20 04         [12]  288 	jr	NZ,00109$
   56F9                     289 00106$:
                            290 ;src/entities/projectile.c:59: projectile->active = 0;
   56F9 FD 36 00 00   [19]  291 	ld	0 (iy), #0x00
   56FD                     292 00109$:
   56FD 33            [ 6]  293 	inc	sp
   56FE DD E1         [14]  294 	pop	ix
   5700 C9            [10]  295 	ret
                            296 ;src/entities/projectile.c:63: void projectilerender(const Projectile* projectile) {
                            297 ;	---------------------------------
                            298 ; Function projectilerender
                            299 ; ---------------------------------
   5701                     300 _projectilerender::
   5701 DD E5         [15]  301 	push	ix
   5703 DD 21 00 00   [14]  302 	ld	ix,#0
   5707 DD 39         [15]  303 	add	ix,sp
   5709 F5            [11]  304 	push	af
                            305 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   570A DD 7E 05      [19]  306 	ld	a, 5 (ix)
   570D DD B6 04      [19]  307 	or	a,4 (ix)
   5710 28 54         [12]  308 	jr	Z,00104$
   5712 DD 5E 04      [19]  309 	ld	e,4 (ix)
   5715 DD 56 05      [19]  310 	ld	d,5 (ix)
   5718 D5            [11]  311 	push	de
   5719 FD E1         [14]  312 	pop	iy
   571B FD 7E 06      [19]  313 	ld	a, 6 (iy)
   571E B7            [ 4]  314 	or	a, a
                            315 ;src/entities/projectile.c:67: return;
   571F 28 45         [12]  316 	jr	Z,00104$
                            317 ;src/entities/projectile.c:70: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5721 6B            [ 4]  318 	ld	l, e
   5722 62            [ 4]  319 	ld	h, d
   5723 23            [ 6]  320 	inc	hl
   5724 46            [ 7]  321 	ld	b, (hl)
   5725 1A            [ 7]  322 	ld	a, (de)
   5726 D5            [11]  323 	push	de
   5727 C5            [11]  324 	push	bc
   5728 33            [ 6]  325 	inc	sp
   5729 F5            [11]  326 	push	af
   572A 33            [ 6]  327 	inc	sp
   572B 21 00 C0      [10]  328 	ld	hl, #0xc000
   572E E5            [11]  329 	push	hl
   572F CD D5 59      [17]  330 	call	_cpct_getScreenPtr
   5732 4D            [ 4]  331 	ld	c, l
   5733 44            [ 4]  332 	ld	b, h
   5734 D1            [10]  333 	pop	de
                            334 ;src/entities/projectile.c:71: cpct_drawSolidBox(pvmem, projectile->weapon ? 0x6B : 0x0F, projectile->w, projectile->h);
   5735 D5            [11]  335 	push	de
   5736 FD E1         [14]  336 	pop	iy
   5738 FD 7E 05      [19]  337 	ld	a, 5 (iy)
   573B DD 77 FF      [19]  338 	ld	-1 (ix), a
   573E D5            [11]  339 	push	de
   573F FD E1         [14]  340 	pop	iy
   5741 FD 7E 04      [19]  341 	ld	a, 4 (iy)
   5744 DD 77 FE      [19]  342 	ld	-2 (ix), a
   5747 EB            [ 4]  343 	ex	de,hl
   5748 11 09 00      [10]  344 	ld	de, #0x0009
   574B 19            [11]  345 	add	hl, de
   574C 7E            [ 7]  346 	ld	a, (hl)
   574D B7            [ 4]  347 	or	a, a
   574E 28 04         [12]  348 	jr	Z,00106$
   5750 16 6B         [ 7]  349 	ld	d, #0x6b
   5752 18 02         [12]  350 	jr	00107$
   5754                     351 00106$:
   5754 16 0F         [ 7]  352 	ld	d, #0x0f
   5756                     353 00107$:
   5756 DD 66 FF      [19]  354 	ld	h, -1 (ix)
   5759 DD 6E FE      [19]  355 	ld	l, -2 (ix)
   575C E5            [11]  356 	push	hl
   575D D5            [11]  357 	push	de
   575E 33            [ 6]  358 	inc	sp
   575F C5            [11]  359 	push	bc
   5760 CD 1C 59      [17]  360 	call	_cpct_drawSolidBox
   5763 F1            [10]  361 	pop	af
   5764 F1            [10]  362 	pop	af
   5765 33            [ 6]  363 	inc	sp
   5766                     364 00104$:
   5766 DD F9         [10]  365 	ld	sp, ix
   5768 DD E1         [14]  366 	pop	ix
   576A C9            [10]  367 	ret
                            368 	.area _CODE
                            369 	.area _INITIALIZER
                            370 	.area _CABS (ABS)
