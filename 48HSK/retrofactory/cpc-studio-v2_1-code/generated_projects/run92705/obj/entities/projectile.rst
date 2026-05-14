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
                             14 	.globl _projectileupdate
                             15 	.globl _projectilerender
                             16 ;--------------------------------------------------------
                             17 ; special function registers
                             18 ;--------------------------------------------------------
                             19 ;--------------------------------------------------------
                             20 ; ram data
                             21 ;--------------------------------------------------------
                             22 	.area _DATA
                             23 ;--------------------------------------------------------
                             24 ; ram data
                             25 ;--------------------------------------------------------
                             26 	.area _INITIALIZED
                             27 ;--------------------------------------------------------
                             28 ; absolute external ram data
                             29 ;--------------------------------------------------------
                             30 	.area _DABS (ABS)
                             31 ;--------------------------------------------------------
                             32 ; global & static initialisations
                             33 ;--------------------------------------------------------
                             34 	.area _HOME
                             35 	.area _GSINIT
                             36 	.area _GSFINAL
                             37 	.area _GSINIT
                             38 ;--------------------------------------------------------
                             39 ; Home
                             40 ;--------------------------------------------------------
                             41 	.area _HOME
                             42 	.area _HOME
                             43 ;--------------------------------------------------------
                             44 ; code
                             45 ;--------------------------------------------------------
                             46 	.area _CODE
                             47 ;src/entities/projectile.c:4: void projectileinit(Projectile* projectile) {
                             48 ;	---------------------------------
                             49 ; Function projectileinit
                             50 ; ---------------------------------
   4688                      51 _projectileinit::
                             52 ;src/entities/projectile.c:5: if (!projectile) {
   4688 21 03 00      [10]   53 	ld	hl, #2+1
   468B 39            [11]   54 	add	hl, sp
   468C 7E            [ 7]   55 	ld	a, (hl)
   468D 2B            [ 6]   56 	dec	hl
   468E B6            [ 7]   57 	or	a,(hl)
                             58 ;src/entities/projectile.c:6: return;
   468F C8            [11]   59 	ret	Z
                             60 ;src/entities/projectile.c:9: projectile->x = 0;
   4690 D1            [10]   61 	pop	de
   4691 C1            [10]   62 	pop	bc
   4692 C5            [11]   63 	push	bc
   4693 D5            [11]   64 	push	de
   4694 AF            [ 4]   65 	xor	a, a
   4695 02            [ 7]   66 	ld	(bc), a
                             67 ;src/entities/projectile.c:10: projectile->y = 0;
   4696 59            [ 4]   68 	ld	e, c
   4697 50            [ 4]   69 	ld	d, b
   4698 13            [ 6]   70 	inc	de
   4699 AF            [ 4]   71 	xor	a, a
   469A 12            [ 7]   72 	ld	(de), a
                             73 ;src/entities/projectile.c:11: projectile->vx = 0;
   469B 59            [ 4]   74 	ld	e, c
   469C 50            [ 4]   75 	ld	d, b
   469D 13            [ 6]   76 	inc	de
   469E 13            [ 6]   77 	inc	de
   469F AF            [ 4]   78 	xor	a, a
   46A0 12            [ 7]   79 	ld	(de), a
                             80 ;src/entities/projectile.c:12: projectile->vy = 0;
   46A1 59            [ 4]   81 	ld	e, c
   46A2 50            [ 4]   82 	ld	d, b
   46A3 13            [ 6]   83 	inc	de
   46A4 13            [ 6]   84 	inc	de
   46A5 13            [ 6]   85 	inc	de
   46A6 AF            [ 4]   86 	xor	a, a
   46A7 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/projectile.c:13: projectile->w = 2;
   46A8 21 04 00      [10]   89 	ld	hl, #0x0004
   46AB 09            [11]   90 	add	hl, bc
   46AC 36 02         [10]   91 	ld	(hl), #0x02
                             92 ;src/entities/projectile.c:14: projectile->h = 2;
   46AE 21 05 00      [10]   93 	ld	hl, #0x0005
   46B1 09            [11]   94 	add	hl, bc
   46B2 36 02         [10]   95 	ld	(hl), #0x02
                             96 ;src/entities/projectile.c:15: projectile->active = 0;
   46B4 21 06 00      [10]   97 	ld	hl, #0x0006
   46B7 09            [11]   98 	add	hl, bc
   46B8 36 00         [10]   99 	ld	(hl), #0x00
   46BA C9            [10]  100 	ret
                            101 ;src/entities/projectile.c:18: void projectileupdate(Projectile* projectile) {
                            102 ;	---------------------------------
                            103 ; Function projectileupdate
                            104 ; ---------------------------------
   46BB                     105 _projectileupdate::
   46BB DD E5         [15]  106 	push	ix
   46BD DD 21 00 00   [14]  107 	ld	ix,#0
   46C1 DD 39         [15]  108 	add	ix,sp
                            109 ;src/entities/projectile.c:19: if (!projectile || !projectile->active) {
   46C3 DD 7E 05      [19]  110 	ld	a, 5 (ix)
   46C6 DD B6 04      [19]  111 	or	a,4 (ix)
   46C9 28 25         [12]  112 	jr	Z,00104$
   46CB DD 4E 04      [19]  113 	ld	c,4 (ix)
   46CE DD 46 05      [19]  114 	ld	b,5 (ix)
   46D1 C5            [11]  115 	push	bc
   46D2 FD E1         [14]  116 	pop	iy
   46D4 FD 7E 06      [19]  117 	ld	a, 6 (iy)
   46D7 B7            [ 4]  118 	or	a, a
                            119 ;src/entities/projectile.c:20: return;
   46D8 28 16         [12]  120 	jr	Z,00104$
                            121 ;src/entities/projectile.c:23: projectile->x = (u8)(projectile->x + projectile->vx);
   46DA 0A            [ 7]  122 	ld	a, (bc)
   46DB 5F            [ 4]  123 	ld	e, a
   46DC 69            [ 4]  124 	ld	l, c
   46DD 60            [ 4]  125 	ld	h, b
   46DE 23            [ 6]  126 	inc	hl
   46DF 23            [ 6]  127 	inc	hl
   46E0 56            [ 7]  128 	ld	d, (hl)
   46E1 7B            [ 4]  129 	ld	a, e
   46E2 82            [ 4]  130 	add	a, d
   46E3 02            [ 7]  131 	ld	(bc), a
                            132 ;src/entities/projectile.c:24: projectile->y = (u8)(projectile->y + projectile->vy);
   46E4 59            [ 4]  133 	ld	e, c
   46E5 50            [ 4]  134 	ld	d, b
   46E6 13            [ 6]  135 	inc	de
   46E7 1A            [ 7]  136 	ld	a, (de)
   46E8 69            [ 4]  137 	ld	l, c
   46E9 60            [ 4]  138 	ld	h, b
   46EA 23            [ 6]  139 	inc	hl
   46EB 23            [ 6]  140 	inc	hl
   46EC 23            [ 6]  141 	inc	hl
   46ED 4E            [ 7]  142 	ld	c, (hl)
   46EE 81            [ 4]  143 	add	a, c
   46EF 12            [ 7]  144 	ld	(de), a
   46F0                     145 00104$:
   46F0 DD E1         [14]  146 	pop	ix
   46F2 C9            [10]  147 	ret
                            148 ;src/entities/projectile.c:27: void projectilerender(const Projectile* projectile) {
                            149 ;	---------------------------------
                            150 ; Function projectilerender
                            151 ; ---------------------------------
   46F3                     152 _projectilerender::
   46F3 DD E5         [15]  153 	push	ix
   46F5 DD 21 00 00   [14]  154 	ld	ix,#0
   46F9 DD 39         [15]  155 	add	ix,sp
                            156 ;src/entities/projectile.c:30: if (!projectile || !projectile->active) {
   46FB DD 7E 05      [19]  157 	ld	a, 5 (ix)
   46FE DD B6 04      [19]  158 	or	a,4 (ix)
   4701 28 3C         [12]  159 	jr	Z,00104$
   4703 DD 4E 04      [19]  160 	ld	c,4 (ix)
   4706 DD 46 05      [19]  161 	ld	b,5 (ix)
   4709 C5            [11]  162 	push	bc
   470A FD E1         [14]  163 	pop	iy
   470C FD 7E 06      [19]  164 	ld	a, 6 (iy)
   470F B7            [ 4]  165 	or	a, a
                            166 ;src/entities/projectile.c:31: return;
   4710 28 2D         [12]  167 	jr	Z,00104$
                            168 ;src/entities/projectile.c:34: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   4712 69            [ 4]  169 	ld	l, c
   4713 60            [ 4]  170 	ld	h, b
   4714 23            [ 6]  171 	inc	hl
   4715 56            [ 7]  172 	ld	d, (hl)
   4716 0A            [ 7]  173 	ld	a, (bc)
   4717 C5            [11]  174 	push	bc
   4718 5F            [ 4]  175 	ld	e, a
   4719 D5            [11]  176 	push	de
   471A 21 00 C0      [10]  177 	ld	hl, #0xc000
   471D E5            [11]  178 	push	hl
   471E CD AC 49      [17]  179 	call	_cpct_getScreenPtr
   4721 EB            [ 4]  180 	ex	de,hl
   4722 C1            [10]  181 	pop	bc
                            182 ;src/entities/projectile.c:35: cpct_drawSolidBox(pvmem, 0x0F, projectile->w, projectile->h);
   4723 C5            [11]  183 	push	bc
   4724 FD E1         [14]  184 	pop	iy
   4726 FD 7E 05      [19]  185 	ld	a, 5 (iy)
   4729 69            [ 4]  186 	ld	l, c
   472A 60            [ 4]  187 	ld	h, b
   472B 01 04 00      [10]  188 	ld	bc, #0x0004
   472E 09            [11]  189 	add	hl, bc
   472F 46            [ 7]  190 	ld	b, (hl)
   4730 F5            [11]  191 	push	af
   4731 33            [ 6]  192 	inc	sp
   4732 C5            [11]  193 	push	bc
   4733 33            [ 6]  194 	inc	sp
   4734 3E 0F         [ 7]  195 	ld	a, #0x0f
   4736 F5            [11]  196 	push	af
   4737 33            [ 6]  197 	inc	sp
   4738 D5            [11]  198 	push	de
   4739 CD F3 48      [17]  199 	call	_cpct_drawSolidBox
   473C F1            [10]  200 	pop	af
   473D F1            [10]  201 	pop	af
   473E 33            [ 6]  202 	inc	sp
   473F                     203 00104$:
   473F DD E1         [14]  204 	pop	ix
   4741 C9            [10]  205 	ret
                            206 	.area _CODE
                            207 	.area _INITIALIZER
                            208 	.area _CABS (ABS)
