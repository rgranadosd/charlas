                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module enemy
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSolidBox
                             13 	.globl _enemyinit
                             14 	.globl _enemyupdate
                             15 	.globl _enemyrender
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
                             47 ;src/entities/enemy.c:4: void enemyinit(Enemy* enemy) {
                             48 ;	---------------------------------
                             49 ; Function enemyinit
                             50 ; ---------------------------------
   43C9                      51 _enemyinit::
                             52 ;src/entities/enemy.c:5: if (!enemy) {
   43C9 21 03 00      [10]   53 	ld	hl, #2+1
   43CC 39            [11]   54 	add	hl, sp
   43CD 7E            [ 7]   55 	ld	a, (hl)
   43CE 2B            [ 6]   56 	dec	hl
   43CF B6            [ 7]   57 	or	a,(hl)
                             58 ;src/entities/enemy.c:6: return;
   43D0 C8            [11]   59 	ret	Z
                             60 ;src/entities/enemy.c:9: enemy->x = 0;
   43D1 D1            [10]   61 	pop	de
   43D2 C1            [10]   62 	pop	bc
   43D3 C5            [11]   63 	push	bc
   43D4 D5            [11]   64 	push	de
   43D5 AF            [ 4]   65 	xor	a, a
   43D6 02            [ 7]   66 	ld	(bc), a
                             67 ;src/entities/enemy.c:10: enemy->y = 0;
   43D7 59            [ 4]   68 	ld	e, c
   43D8 50            [ 4]   69 	ld	d, b
   43D9 13            [ 6]   70 	inc	de
   43DA AF            [ 4]   71 	xor	a, a
   43DB 12            [ 7]   72 	ld	(de), a
                             73 ;src/entities/enemy.c:11: enemy->vx = 0;
   43DC 59            [ 4]   74 	ld	e, c
   43DD 50            [ 4]   75 	ld	d, b
   43DE 13            [ 6]   76 	inc	de
   43DF 13            [ 6]   77 	inc	de
   43E0 AF            [ 4]   78 	xor	a, a
   43E1 12            [ 7]   79 	ld	(de), a
                             80 ;src/entities/enemy.c:12: enemy->vy = 0;
   43E2 59            [ 4]   81 	ld	e, c
   43E3 50            [ 4]   82 	ld	d, b
   43E4 13            [ 6]   83 	inc	de
   43E5 13            [ 6]   84 	inc	de
   43E6 13            [ 6]   85 	inc	de
   43E7 AF            [ 4]   86 	xor	a, a
   43E8 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/enemy.c:13: enemy->w = 4;
   43E9 21 04 00      [10]   89 	ld	hl, #0x0004
   43EC 09            [11]   90 	add	hl, bc
   43ED 36 04         [10]   91 	ld	(hl), #0x04
                             92 ;src/entities/enemy.c:14: enemy->h = 16;
   43EF 21 05 00      [10]   93 	ld	hl, #0x0005
   43F2 09            [11]   94 	add	hl, bc
   43F3 36 10         [10]   95 	ld	(hl), #0x10
                             96 ;src/entities/enemy.c:15: enemy->active = 0;
   43F5 21 06 00      [10]   97 	ld	hl, #0x0006
   43F8 09            [11]   98 	add	hl, bc
   43F9 36 00         [10]   99 	ld	(hl), #0x00
   43FB C9            [10]  100 	ret
                            101 ;src/entities/enemy.c:18: void enemyupdate(Enemy* enemy) {
                            102 ;	---------------------------------
                            103 ; Function enemyupdate
                            104 ; ---------------------------------
   43FC                     105 _enemyupdate::
   43FC DD E5         [15]  106 	push	ix
   43FE DD 21 00 00   [14]  107 	ld	ix,#0
   4402 DD 39         [15]  108 	add	ix,sp
                            109 ;src/entities/enemy.c:19: if (!enemy || !enemy->active) {
   4404 DD 7E 05      [19]  110 	ld	a, 5 (ix)
   4407 DD B6 04      [19]  111 	or	a,4 (ix)
   440A 28 25         [12]  112 	jr	Z,00104$
   440C DD 4E 04      [19]  113 	ld	c,4 (ix)
   440F DD 46 05      [19]  114 	ld	b,5 (ix)
   4412 C5            [11]  115 	push	bc
   4413 FD E1         [14]  116 	pop	iy
   4415 FD 7E 06      [19]  117 	ld	a, 6 (iy)
   4418 B7            [ 4]  118 	or	a, a
                            119 ;src/entities/enemy.c:20: return;
   4419 28 16         [12]  120 	jr	Z,00104$
                            121 ;src/entities/enemy.c:23: enemy->x = (u8)(enemy->x + enemy->vx);
   441B 0A            [ 7]  122 	ld	a, (bc)
   441C 5F            [ 4]  123 	ld	e, a
   441D 69            [ 4]  124 	ld	l, c
   441E 60            [ 4]  125 	ld	h, b
   441F 23            [ 6]  126 	inc	hl
   4420 23            [ 6]  127 	inc	hl
   4421 56            [ 7]  128 	ld	d, (hl)
   4422 7B            [ 4]  129 	ld	a, e
   4423 82            [ 4]  130 	add	a, d
   4424 02            [ 7]  131 	ld	(bc), a
                            132 ;src/entities/enemy.c:24: enemy->y = (u8)(enemy->y + enemy->vy);
   4425 59            [ 4]  133 	ld	e, c
   4426 50            [ 4]  134 	ld	d, b
   4427 13            [ 6]  135 	inc	de
   4428 1A            [ 7]  136 	ld	a, (de)
   4429 69            [ 4]  137 	ld	l, c
   442A 60            [ 4]  138 	ld	h, b
   442B 23            [ 6]  139 	inc	hl
   442C 23            [ 6]  140 	inc	hl
   442D 23            [ 6]  141 	inc	hl
   442E 4E            [ 7]  142 	ld	c, (hl)
   442F 81            [ 4]  143 	add	a, c
   4430 12            [ 7]  144 	ld	(de), a
   4431                     145 00104$:
   4431 DD E1         [14]  146 	pop	ix
   4433 C9            [10]  147 	ret
                            148 ;src/entities/enemy.c:27: void enemyrender(const Enemy* enemy) {
                            149 ;	---------------------------------
                            150 ; Function enemyrender
                            151 ; ---------------------------------
   4434                     152 _enemyrender::
   4434 DD E5         [15]  153 	push	ix
   4436 DD 21 00 00   [14]  154 	ld	ix,#0
   443A DD 39         [15]  155 	add	ix,sp
                            156 ;src/entities/enemy.c:30: if (!enemy || !enemy->active) {
   443C DD 7E 05      [19]  157 	ld	a, 5 (ix)
   443F DD B6 04      [19]  158 	or	a,4 (ix)
   4442 28 3C         [12]  159 	jr	Z,00104$
   4444 DD 4E 04      [19]  160 	ld	c,4 (ix)
   4447 DD 46 05      [19]  161 	ld	b,5 (ix)
   444A C5            [11]  162 	push	bc
   444B FD E1         [14]  163 	pop	iy
   444D FD 7E 06      [19]  164 	ld	a, 6 (iy)
   4450 B7            [ 4]  165 	or	a, a
                            166 ;src/entities/enemy.c:31: return;
   4451 28 2D         [12]  167 	jr	Z,00104$
                            168 ;src/entities/enemy.c:34: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   4453 69            [ 4]  169 	ld	l, c
   4454 60            [ 4]  170 	ld	h, b
   4455 23            [ 6]  171 	inc	hl
   4456 56            [ 7]  172 	ld	d, (hl)
   4457 0A            [ 7]  173 	ld	a, (bc)
   4458 C5            [11]  174 	push	bc
   4459 5F            [ 4]  175 	ld	e, a
   445A D5            [11]  176 	push	de
   445B 21 00 C0      [10]  177 	ld	hl, #0xc000
   445E E5            [11]  178 	push	hl
   445F CD A5 48      [17]  179 	call	_cpct_getScreenPtr
   4462 EB            [ 4]  180 	ex	de,hl
   4463 C1            [10]  181 	pop	bc
                            182 ;src/entities/enemy.c:35: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
   4464 C5            [11]  183 	push	bc
   4465 FD E1         [14]  184 	pop	iy
   4467 FD 7E 05      [19]  185 	ld	a, 5 (iy)
   446A 69            [ 4]  186 	ld	l, c
   446B 60            [ 4]  187 	ld	h, b
   446C 01 04 00      [10]  188 	ld	bc, #0x0004
   446F 09            [11]  189 	add	hl, bc
   4470 46            [ 7]  190 	ld	b, (hl)
   4471 F5            [11]  191 	push	af
   4472 33            [ 6]  192 	inc	sp
   4473 C5            [11]  193 	push	bc
   4474 33            [ 6]  194 	inc	sp
   4475 3E 5C         [ 7]  195 	ld	a, #0x5c
   4477 F5            [11]  196 	push	af
   4478 33            [ 6]  197 	inc	sp
   4479 D5            [11]  198 	push	de
   447A CD EC 47      [17]  199 	call	_cpct_drawSolidBox
   447D F1            [10]  200 	pop	af
   447E F1            [10]  201 	pop	af
   447F 33            [ 6]  202 	inc	sp
   4480                     203 00104$:
   4480 DD E1         [14]  204 	pop	ix
   4482 C9            [10]  205 	ret
                            206 	.area _CODE
                            207 	.area _INITIALIZER
                            208 	.area _CABS (ABS)
