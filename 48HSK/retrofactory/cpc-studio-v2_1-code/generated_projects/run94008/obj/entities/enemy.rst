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
   43C5                      51 _enemyinit::
                             52 ;src/entities/enemy.c:5: if (!enemy) {
   43C5 21 03 00      [10]   53 	ld	hl, #2+1
   43C8 39            [11]   54 	add	hl, sp
   43C9 7E            [ 7]   55 	ld	a, (hl)
   43CA 2B            [ 6]   56 	dec	hl
   43CB B6            [ 7]   57 	or	a,(hl)
                             58 ;src/entities/enemy.c:6: return;
   43CC C8            [11]   59 	ret	Z
                             60 ;src/entities/enemy.c:9: enemy->x = 0;
   43CD D1            [10]   61 	pop	de
   43CE C1            [10]   62 	pop	bc
   43CF C5            [11]   63 	push	bc
   43D0 D5            [11]   64 	push	de
   43D1 AF            [ 4]   65 	xor	a, a
   43D2 02            [ 7]   66 	ld	(bc), a
                             67 ;src/entities/enemy.c:10: enemy->y = 0;
   43D3 59            [ 4]   68 	ld	e, c
   43D4 50            [ 4]   69 	ld	d, b
   43D5 13            [ 6]   70 	inc	de
   43D6 AF            [ 4]   71 	xor	a, a
   43D7 12            [ 7]   72 	ld	(de), a
                             73 ;src/entities/enemy.c:11: enemy->vx = 0;
   43D8 59            [ 4]   74 	ld	e, c
   43D9 50            [ 4]   75 	ld	d, b
   43DA 13            [ 6]   76 	inc	de
   43DB 13            [ 6]   77 	inc	de
   43DC AF            [ 4]   78 	xor	a, a
   43DD 12            [ 7]   79 	ld	(de), a
                             80 ;src/entities/enemy.c:12: enemy->vy = 0;
   43DE 59            [ 4]   81 	ld	e, c
   43DF 50            [ 4]   82 	ld	d, b
   43E0 13            [ 6]   83 	inc	de
   43E1 13            [ 6]   84 	inc	de
   43E2 13            [ 6]   85 	inc	de
   43E3 AF            [ 4]   86 	xor	a, a
   43E4 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/enemy.c:13: enemy->w = 4;
   43E5 21 04 00      [10]   89 	ld	hl, #0x0004
   43E8 09            [11]   90 	add	hl, bc
   43E9 36 04         [10]   91 	ld	(hl), #0x04
                             92 ;src/entities/enemy.c:14: enemy->h = 16;
   43EB 21 05 00      [10]   93 	ld	hl, #0x0005
   43EE 09            [11]   94 	add	hl, bc
   43EF 36 10         [10]   95 	ld	(hl), #0x10
                             96 ;src/entities/enemy.c:15: enemy->active = 0;
   43F1 21 06 00      [10]   97 	ld	hl, #0x0006
   43F4 09            [11]   98 	add	hl, bc
   43F5 36 00         [10]   99 	ld	(hl), #0x00
   43F7 C9            [10]  100 	ret
                            101 ;src/entities/enemy.c:18: void enemyupdate(Enemy* enemy) {
                            102 ;	---------------------------------
                            103 ; Function enemyupdate
                            104 ; ---------------------------------
   43F8                     105 _enemyupdate::
   43F8 DD E5         [15]  106 	push	ix
   43FA DD 21 00 00   [14]  107 	ld	ix,#0
   43FE DD 39         [15]  108 	add	ix,sp
                            109 ;src/entities/enemy.c:19: if (!enemy || !enemy->active) {
   4400 DD 7E 05      [19]  110 	ld	a, 5 (ix)
   4403 DD B6 04      [19]  111 	or	a,4 (ix)
   4406 28 25         [12]  112 	jr	Z,00104$
   4408 DD 4E 04      [19]  113 	ld	c,4 (ix)
   440B DD 46 05      [19]  114 	ld	b,5 (ix)
   440E C5            [11]  115 	push	bc
   440F FD E1         [14]  116 	pop	iy
   4411 FD 7E 06      [19]  117 	ld	a, 6 (iy)
   4414 B7            [ 4]  118 	or	a, a
                            119 ;src/entities/enemy.c:20: return;
   4415 28 16         [12]  120 	jr	Z,00104$
                            121 ;src/entities/enemy.c:23: enemy->x = (u8)(enemy->x + enemy->vx);
   4417 0A            [ 7]  122 	ld	a, (bc)
   4418 5F            [ 4]  123 	ld	e, a
   4419 69            [ 4]  124 	ld	l, c
   441A 60            [ 4]  125 	ld	h, b
   441B 23            [ 6]  126 	inc	hl
   441C 23            [ 6]  127 	inc	hl
   441D 56            [ 7]  128 	ld	d, (hl)
   441E 7B            [ 4]  129 	ld	a, e
   441F 82            [ 4]  130 	add	a, d
   4420 02            [ 7]  131 	ld	(bc), a
                            132 ;src/entities/enemy.c:24: enemy->y = (u8)(enemy->y + enemy->vy);
   4421 59            [ 4]  133 	ld	e, c
   4422 50            [ 4]  134 	ld	d, b
   4423 13            [ 6]  135 	inc	de
   4424 1A            [ 7]  136 	ld	a, (de)
   4425 69            [ 4]  137 	ld	l, c
   4426 60            [ 4]  138 	ld	h, b
   4427 23            [ 6]  139 	inc	hl
   4428 23            [ 6]  140 	inc	hl
   4429 23            [ 6]  141 	inc	hl
   442A 4E            [ 7]  142 	ld	c, (hl)
   442B 81            [ 4]  143 	add	a, c
   442C 12            [ 7]  144 	ld	(de), a
   442D                     145 00104$:
   442D DD E1         [14]  146 	pop	ix
   442F C9            [10]  147 	ret
                            148 ;src/entities/enemy.c:27: void enemyrender(const Enemy* enemy) {
                            149 ;	---------------------------------
                            150 ; Function enemyrender
                            151 ; ---------------------------------
   4430                     152 _enemyrender::
   4430 DD E5         [15]  153 	push	ix
   4432 DD 21 00 00   [14]  154 	ld	ix,#0
   4436 DD 39         [15]  155 	add	ix,sp
                            156 ;src/entities/enemy.c:30: if (!enemy || !enemy->active) {
   4438 DD 7E 05      [19]  157 	ld	a, 5 (ix)
   443B DD B6 04      [19]  158 	or	a,4 (ix)
   443E 28 3C         [12]  159 	jr	Z,00104$
   4440 DD 4E 04      [19]  160 	ld	c,4 (ix)
   4443 DD 46 05      [19]  161 	ld	b,5 (ix)
   4446 C5            [11]  162 	push	bc
   4447 FD E1         [14]  163 	pop	iy
   4449 FD 7E 06      [19]  164 	ld	a, 6 (iy)
   444C B7            [ 4]  165 	or	a, a
                            166 ;src/entities/enemy.c:31: return;
   444D 28 2D         [12]  167 	jr	Z,00104$
                            168 ;src/entities/enemy.c:34: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   444F 69            [ 4]  169 	ld	l, c
   4450 60            [ 4]  170 	ld	h, b
   4451 23            [ 6]  171 	inc	hl
   4452 56            [ 7]  172 	ld	d, (hl)
   4453 0A            [ 7]  173 	ld	a, (bc)
   4454 C5            [11]  174 	push	bc
   4455 5F            [ 4]  175 	ld	e, a
   4456 D5            [11]  176 	push	de
   4457 21 00 C0      [10]  177 	ld	hl, #0xc000
   445A E5            [11]  178 	push	hl
   445B CD A1 48      [17]  179 	call	_cpct_getScreenPtr
   445E EB            [ 4]  180 	ex	de,hl
   445F C1            [10]  181 	pop	bc
                            182 ;src/entities/enemy.c:35: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
   4460 C5            [11]  183 	push	bc
   4461 FD E1         [14]  184 	pop	iy
   4463 FD 7E 05      [19]  185 	ld	a, 5 (iy)
   4466 69            [ 4]  186 	ld	l, c
   4467 60            [ 4]  187 	ld	h, b
   4468 01 04 00      [10]  188 	ld	bc, #0x0004
   446B 09            [11]  189 	add	hl, bc
   446C 46            [ 7]  190 	ld	b, (hl)
   446D F5            [11]  191 	push	af
   446E 33            [ 6]  192 	inc	sp
   446F C5            [11]  193 	push	bc
   4470 33            [ 6]  194 	inc	sp
   4471 3E 5C         [ 7]  195 	ld	a, #0x5c
   4473 F5            [11]  196 	push	af
   4474 33            [ 6]  197 	inc	sp
   4475 D5            [11]  198 	push	de
   4476 CD E8 47      [17]  199 	call	_cpct_drawSolidBox
   4479 F1            [10]  200 	pop	af
   447A F1            [10]  201 	pop	af
   447B 33            [ 6]  202 	inc	sp
   447C                     203 00104$:
   447C DD E1         [14]  204 	pop	ix
   447E C9            [10]  205 	ret
                            206 	.area _CODE
                            207 	.area _INITIALIZER
                            208 	.area _CABS (ABS)
