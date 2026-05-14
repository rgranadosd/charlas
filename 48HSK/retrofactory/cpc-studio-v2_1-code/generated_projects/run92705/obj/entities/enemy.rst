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
   4416                      51 _enemyinit::
                             52 ;src/entities/enemy.c:5: if (!enemy) {
   4416 21 03 00      [10]   53 	ld	hl, #2+1
   4419 39            [11]   54 	add	hl, sp
   441A 7E            [ 7]   55 	ld	a, (hl)
   441B 2B            [ 6]   56 	dec	hl
   441C B6            [ 7]   57 	or	a,(hl)
                             58 ;src/entities/enemy.c:6: return;
   441D C8            [11]   59 	ret	Z
                             60 ;src/entities/enemy.c:9: enemy->x = 0;
   441E D1            [10]   61 	pop	de
   441F C1            [10]   62 	pop	bc
   4420 C5            [11]   63 	push	bc
   4421 D5            [11]   64 	push	de
   4422 AF            [ 4]   65 	xor	a, a
   4423 02            [ 7]   66 	ld	(bc), a
                             67 ;src/entities/enemy.c:10: enemy->y = 0;
   4424 59            [ 4]   68 	ld	e, c
   4425 50            [ 4]   69 	ld	d, b
   4426 13            [ 6]   70 	inc	de
   4427 AF            [ 4]   71 	xor	a, a
   4428 12            [ 7]   72 	ld	(de), a
                             73 ;src/entities/enemy.c:11: enemy->vx = 0;
   4429 59            [ 4]   74 	ld	e, c
   442A 50            [ 4]   75 	ld	d, b
   442B 13            [ 6]   76 	inc	de
   442C 13            [ 6]   77 	inc	de
   442D AF            [ 4]   78 	xor	a, a
   442E 12            [ 7]   79 	ld	(de), a
                             80 ;src/entities/enemy.c:12: enemy->vy = 0;
   442F 59            [ 4]   81 	ld	e, c
   4430 50            [ 4]   82 	ld	d, b
   4431 13            [ 6]   83 	inc	de
   4432 13            [ 6]   84 	inc	de
   4433 13            [ 6]   85 	inc	de
   4434 AF            [ 4]   86 	xor	a, a
   4435 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/enemy.c:13: enemy->w = 4;
   4436 21 04 00      [10]   89 	ld	hl, #0x0004
   4439 09            [11]   90 	add	hl, bc
   443A 36 04         [10]   91 	ld	(hl), #0x04
                             92 ;src/entities/enemy.c:14: enemy->h = 16;
   443C 21 05 00      [10]   93 	ld	hl, #0x0005
   443F 09            [11]   94 	add	hl, bc
   4440 36 10         [10]   95 	ld	(hl), #0x10
                             96 ;src/entities/enemy.c:15: enemy->active = 0;
   4442 21 06 00      [10]   97 	ld	hl, #0x0006
   4445 09            [11]   98 	add	hl, bc
   4446 36 00         [10]   99 	ld	(hl), #0x00
   4448 C9            [10]  100 	ret
                            101 ;src/entities/enemy.c:18: void enemyupdate(Enemy* enemy) {
                            102 ;	---------------------------------
                            103 ; Function enemyupdate
                            104 ; ---------------------------------
   4449                     105 _enemyupdate::
   4449 DD E5         [15]  106 	push	ix
   444B DD 21 00 00   [14]  107 	ld	ix,#0
   444F DD 39         [15]  108 	add	ix,sp
                            109 ;src/entities/enemy.c:19: if (!enemy || !enemy->active) {
   4451 DD 7E 05      [19]  110 	ld	a, 5 (ix)
   4454 DD B6 04      [19]  111 	or	a,4 (ix)
   4457 28 25         [12]  112 	jr	Z,00104$
   4459 DD 4E 04      [19]  113 	ld	c,4 (ix)
   445C DD 46 05      [19]  114 	ld	b,5 (ix)
   445F C5            [11]  115 	push	bc
   4460 FD E1         [14]  116 	pop	iy
   4462 FD 7E 06      [19]  117 	ld	a, 6 (iy)
   4465 B7            [ 4]  118 	or	a, a
                            119 ;src/entities/enemy.c:20: return;
   4466 28 16         [12]  120 	jr	Z,00104$
                            121 ;src/entities/enemy.c:23: enemy->x = (u8)(enemy->x + enemy->vx);
   4468 0A            [ 7]  122 	ld	a, (bc)
   4469 5F            [ 4]  123 	ld	e, a
   446A 69            [ 4]  124 	ld	l, c
   446B 60            [ 4]  125 	ld	h, b
   446C 23            [ 6]  126 	inc	hl
   446D 23            [ 6]  127 	inc	hl
   446E 56            [ 7]  128 	ld	d, (hl)
   446F 7B            [ 4]  129 	ld	a, e
   4470 82            [ 4]  130 	add	a, d
   4471 02            [ 7]  131 	ld	(bc), a
                            132 ;src/entities/enemy.c:24: enemy->y = (u8)(enemy->y + enemy->vy);
   4472 59            [ 4]  133 	ld	e, c
   4473 50            [ 4]  134 	ld	d, b
   4474 13            [ 6]  135 	inc	de
   4475 1A            [ 7]  136 	ld	a, (de)
   4476 69            [ 4]  137 	ld	l, c
   4477 60            [ 4]  138 	ld	h, b
   4478 23            [ 6]  139 	inc	hl
   4479 23            [ 6]  140 	inc	hl
   447A 23            [ 6]  141 	inc	hl
   447B 4E            [ 7]  142 	ld	c, (hl)
   447C 81            [ 4]  143 	add	a, c
   447D 12            [ 7]  144 	ld	(de), a
   447E                     145 00104$:
   447E DD E1         [14]  146 	pop	ix
   4480 C9            [10]  147 	ret
                            148 ;src/entities/enemy.c:27: void enemyrender(const Enemy* enemy) {
                            149 ;	---------------------------------
                            150 ; Function enemyrender
                            151 ; ---------------------------------
   4481                     152 _enemyrender::
   4481 DD E5         [15]  153 	push	ix
   4483 DD 21 00 00   [14]  154 	ld	ix,#0
   4487 DD 39         [15]  155 	add	ix,sp
                            156 ;src/entities/enemy.c:30: if (!enemy || !enemy->active) {
   4489 DD 7E 05      [19]  157 	ld	a, 5 (ix)
   448C DD B6 04      [19]  158 	or	a,4 (ix)
   448F 28 3C         [12]  159 	jr	Z,00104$
   4491 DD 4E 04      [19]  160 	ld	c,4 (ix)
   4494 DD 46 05      [19]  161 	ld	b,5 (ix)
   4497 C5            [11]  162 	push	bc
   4498 FD E1         [14]  163 	pop	iy
   449A FD 7E 06      [19]  164 	ld	a, 6 (iy)
   449D B7            [ 4]  165 	or	a, a
                            166 ;src/entities/enemy.c:31: return;
   449E 28 2D         [12]  167 	jr	Z,00104$
                            168 ;src/entities/enemy.c:34: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   44A0 69            [ 4]  169 	ld	l, c
   44A1 60            [ 4]  170 	ld	h, b
   44A2 23            [ 6]  171 	inc	hl
   44A3 56            [ 7]  172 	ld	d, (hl)
   44A4 0A            [ 7]  173 	ld	a, (bc)
   44A5 C5            [11]  174 	push	bc
   44A6 5F            [ 4]  175 	ld	e, a
   44A7 D5            [11]  176 	push	de
   44A8 21 00 C0      [10]  177 	ld	hl, #0xc000
   44AB E5            [11]  178 	push	hl
   44AC CD AC 49      [17]  179 	call	_cpct_getScreenPtr
   44AF EB            [ 4]  180 	ex	de,hl
   44B0 C1            [10]  181 	pop	bc
                            182 ;src/entities/enemy.c:35: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
   44B1 C5            [11]  183 	push	bc
   44B2 FD E1         [14]  184 	pop	iy
   44B4 FD 7E 05      [19]  185 	ld	a, 5 (iy)
   44B7 69            [ 4]  186 	ld	l, c
   44B8 60            [ 4]  187 	ld	h, b
   44B9 01 04 00      [10]  188 	ld	bc, #0x0004
   44BC 09            [11]  189 	add	hl, bc
   44BD 46            [ 7]  190 	ld	b, (hl)
   44BE F5            [11]  191 	push	af
   44BF 33            [ 6]  192 	inc	sp
   44C0 C5            [11]  193 	push	bc
   44C1 33            [ 6]  194 	inc	sp
   44C2 3E 5C         [ 7]  195 	ld	a, #0x5c
   44C4 F5            [11]  196 	push	af
   44C5 33            [ 6]  197 	inc	sp
   44C6 D5            [11]  198 	push	de
   44C7 CD F3 48      [17]  199 	call	_cpct_drawSolidBox
   44CA F1            [10]  200 	pop	af
   44CB F1            [10]  201 	pop	af
   44CC 33            [ 6]  202 	inc	sp
   44CD                     203 00104$:
   44CD DD E1         [14]  204 	pop	ix
   44CF C9            [10]  205 	ret
                            206 	.area _CODE
                            207 	.area _INITIALIZER
                            208 	.area _CABS (ABS)
