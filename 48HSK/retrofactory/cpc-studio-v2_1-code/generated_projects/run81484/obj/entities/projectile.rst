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
                             12 	.globl _cpct_drawSprite
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
                             48 ;src/entities/projectile.c:22: void projectileinit(Projectile* projectile) {
                             49 ;	---------------------------------
                             50 ; Function projectileinit
                             51 ; ---------------------------------
   66F2                      52 _projectileinit::
                             53 ;src/entities/projectile.c:23: if (!projectile) {
   66F2 21 03 00      [10]   54 	ld	hl, #2+1
   66F5 39            [11]   55 	add	hl, sp
   66F6 7E            [ 7]   56 	ld	a, (hl)
   66F7 2B            [ 6]   57 	dec	hl
   66F8 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:24: return;
   66F9 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:27: projectile->x = 0;
   66FA D1            [10]   62 	pop	de
   66FB C1            [10]   63 	pop	bc
   66FC C5            [11]   64 	push	bc
   66FD D5            [11]   65 	push	de
   66FE AF            [ 4]   66 	xor	a, a
   66FF 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:28: projectile->y = 0;
   6700 59            [ 4]   69 	ld	e, c
   6701 50            [ 4]   70 	ld	d, b
   6702 13            [ 6]   71 	inc	de
   6703 AF            [ 4]   72 	xor	a, a
   6704 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:29: projectile->vx = 0;
   6705 59            [ 4]   75 	ld	e, c
   6706 50            [ 4]   76 	ld	d, b
   6707 13            [ 6]   77 	inc	de
   6708 13            [ 6]   78 	inc	de
   6709 AF            [ 4]   79 	xor	a, a
   670A 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:30: projectile->vy = 0;
   670B 59            [ 4]   82 	ld	e, c
   670C 50            [ 4]   83 	ld	d, b
   670D 13            [ 6]   84 	inc	de
   670E 13            [ 6]   85 	inc	de
   670F 13            [ 6]   86 	inc	de
   6710 AF            [ 4]   87 	xor	a, a
   6711 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:31: projectile->w = 2;
   6712 21 04 00      [10]   90 	ld	hl, #0x0004
   6715 09            [11]   91 	add	hl, bc
   6716 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:32: projectile->h = 2;
   6718 21 05 00      [10]   94 	ld	hl, #0x0005
   671B 09            [11]   95 	add	hl, bc
   671C 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:33: projectile->active = 0;
   671E 21 06 00      [10]   98 	ld	hl, #0x0006
   6721 09            [11]   99 	add	hl, bc
   6722 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:34: projectile->damage = 1;
   6724 21 07 00      [10]  102 	ld	hl, #0x0007
   6727 09            [11]  103 	add	hl, bc
   6728 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:35: projectile->lifetime = 0;
   672A 21 08 00      [10]  106 	ld	hl, #0x0008
   672D 09            [11]  107 	add	hl, bc
   672E 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:36: projectile->weapon = 0;
   6730 21 09 00      [10]  110 	ld	hl, #0x0009
   6733 09            [11]  111 	add	hl, bc
   6734 36 00         [10]  112 	ld	(hl), #0x00
   6736 C9            [10]  113 	ret
   6737                     114 _projectile_basic_sprite:
   6737 FF                  115 	.db #0xff	; 255
   6738 FF                  116 	.db #0xff	; 255
   6739 FF                  117 	.db #0xff	; 255
   673A FF                  118 	.db #0xff	; 255
   673B FF                  119 	.db #0xff	; 255
   673C FF                  120 	.db #0xff	; 255
   673D FF                  121 	.db #0xff	; 255
   673E FF                  122 	.db #0xff	; 255
   673F FF                  123 	.db #0xff	; 255
   6740 FF                  124 	.db #0xff	; 255
   6741 FF                  125 	.db #0xff	; 255
   6742 FF                  126 	.db #0xff	; 255
   6743 FF                  127 	.db #0xff	; 255
   6744 FF                  128 	.db #0xff	; 255
   6745 FF                  129 	.db #0xff	; 255
   6746 FF                  130 	.db #0xff	; 255
   6747                     131 _projectile_up_sprite:
   6747 CF                  132 	.db #0xcf	; 207
   6748 CF                  133 	.db #0xcf	; 207
   6749 CF                  134 	.db #0xcf	; 207
   674A CF                  135 	.db #0xcf	; 207
   674B CF                  136 	.db #0xcf	; 207
   674C CF                  137 	.db #0xcf	; 207
   674D                     138 _projectile_special_sprite:
   674D F0                  139 	.db #0xf0	; 240
   674E F0                  140 	.db #0xf0	; 240
   674F F0                  141 	.db #0xf0	; 240
   6750 F0                  142 	.db #0xf0	; 240
   6751 F0                  143 	.db #0xf0	; 240
   6752 F0                  144 	.db #0xf0	; 240
   6753 F0                  145 	.db #0xf0	; 240
   6754 F0                  146 	.db #0xf0	; 240
   6755 F0                  147 	.db #0xf0	; 240
   6756 F0                  148 	.db #0xf0	; 240
   6757 F0                  149 	.db #0xf0	; 240
   6758 F0                  150 	.db #0xf0	; 240
                            151 ;src/entities/projectile.c:39: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            152 ;	---------------------------------
                            153 ; Function projectilefire
                            154 ; ---------------------------------
   6759                     155 _projectilefire::
   6759 DD E5         [15]  156 	push	ix
   675B DD 21 00 00   [14]  157 	ld	ix,#0
   675F DD 39         [15]  158 	add	ix,sp
   6761 F5            [11]  159 	push	af
   6762 F5            [11]  160 	push	af
                            161 ;src/entities/projectile.c:40: if (!projectile) {
   6763 DD 7E 05      [19]  162 	ld	a, 5 (ix)
   6766 DD B6 04      [19]  163 	or	a,4 (ix)
                            164 ;src/entities/projectile.c:41: return;
   6769 CA 0B 68      [10]  165 	jp	Z,00109$
                            166 ;src/entities/projectile.c:44: projectile->x = x;
   676C DD 4E 04      [19]  167 	ld	c,4 (ix)
   676F DD 46 05      [19]  168 	ld	b,5 (ix)
   6772 DD 7E 06      [19]  169 	ld	a, 6 (ix)
   6775 02            [ 7]  170 	ld	(bc), a
                            171 ;src/entities/projectile.c:45: projectile->y = y;
   6776 59            [ 4]  172 	ld	e, c
   6777 50            [ 4]  173 	ld	d, b
   6778 13            [ 6]  174 	inc	de
   6779 DD 7E 07      [19]  175 	ld	a, 7 (ix)
   677C 12            [ 7]  176 	ld	(de), a
                            177 ;src/entities/projectile.c:46: projectile->vx = dir;
   677D 21 02 00      [10]  178 	ld	hl, #0x0002
   6780 09            [11]  179 	add	hl,bc
   6781 DD 75 FE      [19]  180 	ld	-2 (ix), l
   6784 DD 74 FF      [19]  181 	ld	-1 (ix), h
   6787 DD 7E 08      [19]  182 	ld	a, 8 (ix)
   678A 77            [ 7]  183 	ld	(hl), a
                            184 ;src/entities/projectile.c:47: projectile->vy = 0;
   678B 59            [ 4]  185 	ld	e, c
   678C 50            [ 4]  186 	ld	d, b
   678D 13            [ 6]  187 	inc	de
   678E 13            [ 6]  188 	inc	de
   678F 13            [ 6]  189 	inc	de
   6790 AF            [ 4]  190 	xor	a, a
   6791 12            [ 7]  191 	ld	(de), a
                            192 ;src/entities/projectile.c:48: projectile->weapon = weapon;
   6792 21 09 00      [10]  193 	ld	hl, #0x0009
   6795 09            [11]  194 	add	hl, bc
   6796 DD 7E 09      [19]  195 	ld	a, 9 (ix)
   6799 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/projectile.c:49: projectile->active = 1;
   679A 21 06 00      [10]  198 	ld	hl, #0x0006
   679D 09            [11]  199 	add	hl, bc
   679E 36 01         [10]  200 	ld	(hl), #0x01
                            201 ;src/entities/projectile.c:52: projectile->w = 4;
   67A0 21 04 00      [10]  202 	ld	hl, #0x0004
   67A3 09            [11]  203 	add	hl, bc
                            204 ;src/entities/projectile.c:53: projectile->h = 4;
   67A4 79            [ 4]  205 	ld	a, c
   67A5 C6 05         [ 7]  206 	add	a, #0x05
   67A7 5F            [ 4]  207 	ld	e, a
   67A8 78            [ 4]  208 	ld	a, b
   67A9 CE 00         [ 7]  209 	adc	a, #0x00
   67AB 57            [ 4]  210 	ld	d, a
                            211 ;src/entities/projectile.c:54: projectile->damage = 1;
   67AC 79            [ 4]  212 	ld	a, c
   67AD C6 07         [ 7]  213 	add	a, #0x07
   67AF DD 77 FC      [19]  214 	ld	-4 (ix), a
   67B2 78            [ 4]  215 	ld	a, b
   67B3 CE 00         [ 7]  216 	adc	a, #0x00
   67B5 DD 77 FD      [19]  217 	ld	-3 (ix), a
                            218 ;src/entities/projectile.c:55: projectile->lifetime = 45;
   67B8 79            [ 4]  219 	ld	a, c
   67B9 C6 08         [ 7]  220 	add	a, #0x08
   67BB 4F            [ 4]  221 	ld	c, a
   67BC 78            [ 4]  222 	ld	a, b
   67BD CE 00         [ 7]  223 	adc	a, #0x00
   67BF 47            [ 4]  224 	ld	b, a
                            225 ;src/entities/projectile.c:51: if (weapon == 0) {
   67C0 DD 7E 09      [19]  226 	ld	a, 9 (ix)
   67C3 B7            [ 4]  227 	or	a, a
   67C4 20 0E         [12]  228 	jr	NZ,00107$
                            229 ;src/entities/projectile.c:52: projectile->w = 4;
   67C6 36 04         [10]  230 	ld	(hl), #0x04
                            231 ;src/entities/projectile.c:53: projectile->h = 4;
   67C8 3E 04         [ 7]  232 	ld	a, #0x04
   67CA 12            [ 7]  233 	ld	(de), a
                            234 ;src/entities/projectile.c:54: projectile->damage = 1;
   67CB E1            [10]  235 	pop	hl
   67CC E5            [11]  236 	push	hl
   67CD 36 01         [10]  237 	ld	(hl), #0x01
                            238 ;src/entities/projectile.c:55: projectile->lifetime = 45;
   67CF 3E 2D         [ 7]  239 	ld	a, #0x2d
   67D1 02            [ 7]  240 	ld	(bc), a
   67D2 18 37         [12]  241 	jr	00109$
   67D4                     242 00107$:
                            243 ;src/entities/projectile.c:56: } else if (weapon == 1) {
   67D4 DD 7E 09      [19]  244 	ld	a, 9 (ix)
   67D7 3D            [ 4]  245 	dec	a
   67D8 20 0E         [12]  246 	jr	NZ,00104$
                            247 ;src/entities/projectile.c:57: projectile->w = 2;
   67DA 36 02         [10]  248 	ld	(hl), #0x02
                            249 ;src/entities/projectile.c:58: projectile->h = 3;
   67DC 3E 03         [ 7]  250 	ld	a, #0x03
   67DE 12            [ 7]  251 	ld	(de), a
                            252 ;src/entities/projectile.c:59: projectile->damage = 2;
   67DF E1            [10]  253 	pop	hl
   67E0 E5            [11]  254 	push	hl
   67E1 36 02         [10]  255 	ld	(hl), #0x02
                            256 ;src/entities/projectile.c:60: projectile->lifetime = 28;
   67E3 3E 1C         [ 7]  257 	ld	a, #0x1c
   67E5 02            [ 7]  258 	ld	(bc), a
   67E6 18 23         [12]  259 	jr	00109$
   67E8                     260 00104$:
                            261 ;src/entities/projectile.c:62: projectile->w = 4;
   67E8 36 04         [10]  262 	ld	(hl), #0x04
                            263 ;src/entities/projectile.c:63: projectile->h = 3;
   67EA 3E 03         [ 7]  264 	ld	a, #0x03
   67EC 12            [ 7]  265 	ld	(de), a
                            266 ;src/entities/projectile.c:64: projectile->damage = 3;
   67ED E1            [10]  267 	pop	hl
   67EE E5            [11]  268 	push	hl
   67EF 36 03         [10]  269 	ld	(hl), #0x03
                            270 ;src/entities/projectile.c:65: projectile->lifetime = 56;
   67F1 3E 38         [ 7]  271 	ld	a, #0x38
   67F3 02            [ 7]  272 	ld	(bc), a
                            273 ;src/entities/projectile.c:66: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   67F4 D1            [10]  274 	pop	de
   67F5 C1            [10]  275 	pop	bc
   67F6 C5            [11]  276 	push	bc
   67F7 D5            [11]  277 	push	de
   67F8 AF            [ 4]  278 	xor	a, a
   67F9 DD 96 08      [19]  279 	sub	a, 8 (ix)
   67FC E2 01 68      [10]  280 	jp	PO, 00131$
   67FF EE 80         [ 7]  281 	xor	a, #0x80
   6801                     282 00131$:
   6801 F2 08 68      [10]  283 	jp	P, 00111$
   6804 3E 04         [ 7]  284 	ld	a, #0x04
   6806 18 02         [12]  285 	jr	00112$
   6808                     286 00111$:
   6808 3E FC         [ 7]  287 	ld	a, #0xfc
   680A                     288 00112$:
   680A 02            [ 7]  289 	ld	(bc), a
   680B                     290 00109$:
   680B DD F9         [10]  291 	ld	sp, ix
   680D DD E1         [14]  292 	pop	ix
   680F C9            [10]  293 	ret
                            294 ;src/entities/projectile.c:70: void projectileupdate(Projectile* projectile) {
                            295 ;	---------------------------------
                            296 ; Function projectileupdate
                            297 ; ---------------------------------
   6810                     298 _projectileupdate::
   6810 DD E5         [15]  299 	push	ix
   6812 DD 21 00 00   [14]  300 	ld	ix,#0
   6816 DD 39         [15]  301 	add	ix,sp
   6818 3B            [ 6]  302 	dec	sp
                            303 ;src/entities/projectile.c:71: if (!projectile || !projectile->active) {
   6819 DD 7E 05      [19]  304 	ld	a, 5 (ix)
   681C DD B6 04      [19]  305 	or	a,4 (ix)
   681F 28 4A         [12]  306 	jr	Z,00109$
   6821 DD 5E 04      [19]  307 	ld	e,4 (ix)
   6824 DD 56 05      [19]  308 	ld	d,5 (ix)
   6827 FD 21 06 00   [14]  309 	ld	iy, #0x0006
   682B FD 19         [15]  310 	add	iy, de
   682D FD 7E 00      [19]  311 	ld	a, 0 (iy)
   6830 B7            [ 4]  312 	or	a, a
                            313 ;src/entities/projectile.c:72: return;
   6831 28 38         [12]  314 	jr	Z,00109$
                            315 ;src/entities/projectile.c:75: projectile->x = (u8)(projectile->x + projectile->vx);
   6833 1A            [ 7]  316 	ld	a, (de)
   6834 4F            [ 4]  317 	ld	c, a
   6835 6B            [ 4]  318 	ld	l, e
   6836 62            [ 4]  319 	ld	h, d
   6837 23            [ 6]  320 	inc	hl
   6838 23            [ 6]  321 	inc	hl
   6839 6E            [ 7]  322 	ld	l, (hl)
   683A 09            [11]  323 	add	hl, bc
   683B 7D            [ 4]  324 	ld	a, l
   683C 12            [ 7]  325 	ld	(de), a
                            326 ;src/entities/projectile.c:76: projectile->y = (u8)(projectile->y + projectile->vy);
   683D 4B            [ 4]  327 	ld	c, e
   683E 42            [ 4]  328 	ld	b, d
   683F 03            [ 6]  329 	inc	bc
   6840 0A            [ 7]  330 	ld	a, (bc)
   6841 DD 77 FF      [19]  331 	ld	-1 (ix), a
   6844 6B            [ 4]  332 	ld	l, e
   6845 62            [ 4]  333 	ld	h, d
   6846 23            [ 6]  334 	inc	hl
   6847 23            [ 6]  335 	inc	hl
   6848 23            [ 6]  336 	inc	hl
   6849 6E            [ 7]  337 	ld	l, (hl)
   684A DD 7E FF      [19]  338 	ld	a, -1 (ix)
   684D 85            [ 4]  339 	add	a, l
   684E 02            [ 7]  340 	ld	(bc), a
                            341 ;src/entities/projectile.c:78: if (projectile->lifetime) {
   684F 21 08 00      [10]  342 	ld	hl, #0x0008
   6852 19            [11]  343 	add	hl,de
   6853 4D            [ 4]  344 	ld	c, l
   6854 44            [ 4]  345 	ld	b, h
   6855 0A            [ 7]  346 	ld	a, (bc)
   6856 B7            [ 4]  347 	or	a, a
   6857 28 03         [12]  348 	jr	Z,00105$
                            349 ;src/entities/projectile.c:79: projectile->lifetime--;
   6859 C6 FF         [ 7]  350 	add	a, #0xff
   685B 02            [ 7]  351 	ld	(bc), a
   685C                     352 00105$:
                            353 ;src/entities/projectile.c:82: if (projectile->x > 78 || projectile->lifetime == 0) {
   685C 1A            [ 7]  354 	ld	a, (de)
   685D 5F            [ 4]  355 	ld	e, a
   685E 3E 4E         [ 7]  356 	ld	a, #0x4e
   6860 93            [ 4]  357 	sub	a, e
   6861 38 04         [12]  358 	jr	C,00106$
   6863 0A            [ 7]  359 	ld	a, (bc)
   6864 B7            [ 4]  360 	or	a, a
   6865 20 04         [12]  361 	jr	NZ,00109$
   6867                     362 00106$:
                            363 ;src/entities/projectile.c:83: projectile->active = 0;
   6867 FD 36 00 00   [19]  364 	ld	0 (iy), #0x00
   686B                     365 00109$:
   686B 33            [ 6]  366 	inc	sp
   686C DD E1         [14]  367 	pop	ix
   686E C9            [10]  368 	ret
                            369 ;src/entities/projectile.c:87: void projectilerender(const Projectile* projectile) {
                            370 ;	---------------------------------
                            371 ; Function projectilerender
                            372 ; ---------------------------------
   686F                     373 _projectilerender::
   686F DD E5         [15]  374 	push	ix
   6871 DD 21 00 00   [14]  375 	ld	ix,#0
   6875 DD 39         [15]  376 	add	ix,sp
   6877 F5            [11]  377 	push	af
   6878 3B            [ 6]  378 	dec	sp
                            379 ;src/entities/projectile.c:91: if (!projectile || !projectile->active) {
   6879 DD 7E 05      [19]  380 	ld	a, 5 (ix)
   687C DD B6 04      [19]  381 	or	a,4 (ix)
   687F 28 6B         [12]  382 	jr	Z,00110$
   6881 DD 4E 04      [19]  383 	ld	c,4 (ix)
   6884 DD 46 05      [19]  384 	ld	b,5 (ix)
   6887 C5            [11]  385 	push	bc
   6888 FD E1         [14]  386 	pop	iy
   688A FD 7E 06      [19]  387 	ld	a, 6 (iy)
   688D B7            [ 4]  388 	or	a, a
                            389 ;src/entities/projectile.c:92: return;
   688E 28 5C         [12]  390 	jr	Z,00110$
                            391 ;src/entities/projectile.c:95: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   6890 C5            [11]  392 	push	bc
   6891 FD E1         [14]  393 	pop	iy
   6893 FD 7E 09      [19]  394 	ld	a, 9 (iy)
   6896 B7            [ 4]  395 	or	a, a
   6897 20 0A         [12]  396 	jr	NZ,00108$
   6899 DD 36 FE 37   [19]  397 	ld	-2 (ix), #<(_projectile_basic_sprite)
   689D DD 36 FF 67   [19]  398 	ld	-1 (ix), #>(_projectile_basic_sprite)
   68A1 18 15         [12]  399 	jr	00109$
   68A3                     400 00108$:
                            401 ;src/entities/projectile.c:96: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   68A3 3D            [ 4]  402 	dec	a
   68A4 20 0A         [12]  403 	jr	NZ,00105$
   68A6 DD 36 FE 47   [19]  404 	ld	-2 (ix), #<(_projectile_up_sprite)
   68AA DD 36 FF 67   [19]  405 	ld	-1 (ix), #>(_projectile_up_sprite)
   68AE 18 08         [12]  406 	jr	00109$
   68B0                     407 00105$:
                            408 ;src/entities/projectile.c:97: else sprite = projectile_special_sprite;
   68B0 DD 36 FE 4D   [19]  409 	ld	-2 (ix), #<(_projectile_special_sprite)
   68B4 DD 36 FF 67   [19]  410 	ld	-1 (ix), #>(_projectile_special_sprite)
   68B8                     411 00109$:
                            412 ;src/entities/projectile.c:99: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   68B8 69            [ 4]  413 	ld	l, c
   68B9 60            [ 4]  414 	ld	h, b
   68BA 23            [ 6]  415 	inc	hl
   68BB 56            [ 7]  416 	ld	d, (hl)
   68BC 0A            [ 7]  417 	ld	a, (bc)
   68BD C5            [11]  418 	push	bc
   68BE 5F            [ 4]  419 	ld	e, a
   68BF D5            [11]  420 	push	de
   68C0 21 00 C0      [10]  421 	ld	hl, #0xc000
   68C3 E5            [11]  422 	push	hl
   68C4 CD A5 6B      [17]  423 	call	_cpct_getScreenPtr
   68C7 EB            [ 4]  424 	ex	de,hl
   68C8 C1            [10]  425 	pop	bc
                            426 ;src/entities/projectile.c:100: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   68C9 C5            [11]  427 	push	bc
   68CA FD E1         [14]  428 	pop	iy
   68CC FD 7E 05      [19]  429 	ld	a, 5 (iy)
   68CF DD 77 FD      [19]  430 	ld	-3 (ix), a
   68D2 69            [ 4]  431 	ld	l, c
   68D3 60            [ 4]  432 	ld	h, b
   68D4 01 04 00      [10]  433 	ld	bc, #0x0004
   68D7 09            [11]  434 	add	hl, bc
   68D8 4E            [ 7]  435 	ld	c, (hl)
   68D9 D5            [11]  436 	push	de
   68DA FD E1         [14]  437 	pop	iy
   68DC DD 5E FE      [19]  438 	ld	e,-2 (ix)
   68DF DD 56 FF      [19]  439 	ld	d,-1 (ix)
   68E2 DD 46 FD      [19]  440 	ld	b, -3 (ix)
   68E5 C5            [11]  441 	push	bc
   68E6 FD E5         [15]  442 	push	iy
   68E8 D5            [11]  443 	push	de
   68E9 CD 61 69      [17]  444 	call	_cpct_drawSprite
   68EC                     445 00110$:
   68EC DD F9         [10]  446 	ld	sp, ix
   68EE DD E1         [14]  447 	pop	ix
   68F0 C9            [10]  448 	ret
                            449 	.area _CODE
                            450 	.area _INITIALIZER
                            451 	.area _CABS (ABS)
