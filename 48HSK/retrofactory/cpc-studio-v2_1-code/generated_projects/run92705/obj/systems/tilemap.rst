                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module tilemap
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSolidBox
                             13 	.globl _tilemap_init
                             14 	.globl _tilemap_render
                             15 	.globl _tilemap_ground_y
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
   49F0                      27 _gtilegroundy:
   49F0                      28 	.ds 1
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
                             49 ;src/systems/tilemap.c:7: void tilemap_init(void) {
                             50 ;	---------------------------------
                             51 ; Function tilemap_init
                             52 ; ---------------------------------
   4345                      53 _tilemap_init::
                             54 ;src/systems/tilemap.c:8: if (level1tilemapheight > 2) {
   4345 2A 8B 43      [16]   55 	ld	hl, (_level1tilemapheight)
   4348 3E 02         [ 7]   56 	ld	a, #0x02
   434A BD            [ 4]   57 	cp	a, l
   434B 3E 00         [ 7]   58 	ld	a, #0x00
   434D 9C            [ 4]   59 	sbc	a, h
   434E 30 0C         [12]   60 	jr	NC,00102$
                             61 ;src/systems/tilemap.c:9: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4350 7D            [ 4]   62 	ld	a, l
   4351 C6 FE         [ 7]   63 	add	a, #0xfe
   4353 07            [ 4]   64 	rlca
   4354 07            [ 4]   65 	rlca
   4355 07            [ 4]   66 	rlca
   4356 E6 F8         [ 7]   67 	and	a, #0xf8
   4358 32 F0 49      [13]   68 	ld	(#_gtilegroundy + 0),a
   435B C9            [10]   69 	ret
   435C                      70 00102$:
                             71 ;src/systems/tilemap.c:11: gtilegroundy = 160;
   435C 21 F0 49      [10]   72 	ld	hl,#_gtilegroundy + 0
   435F 36 A0         [10]   73 	ld	(hl), #0xa0
   4361 C9            [10]   74 	ret
                             75 ;src/systems/tilemap.c:15: void tilemap_render(void) {
                             76 ;	---------------------------------
                             77 ; Function tilemap_render
                             78 ; ---------------------------------
   4362                      79 _tilemap_render::
                             80 ;src/systems/tilemap.c:17: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4362 3A F0 49      [13]   81 	ld	a, (_gtilegroundy)
   4365 F5            [11]   82 	push	af
   4366 33            [ 6]   83 	inc	sp
   4367 AF            [ 4]   84 	xor	a, a
   4368 F5            [11]   85 	push	af
   4369 33            [ 6]   86 	inc	sp
   436A 21 00 C0      [10]   87 	ld	hl, #0xc000
   436D E5            [11]   88 	push	hl
   436E CD AC 49      [17]   89 	call	_cpct_getScreenPtr
                             90 ;src/systems/tilemap.c:18: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4371 01 50 08      [10]   91 	ld	bc, #0x0850
   4374 C5            [11]   92 	push	bc
   4375 3E 11         [ 7]   93 	ld	a, #0x11
   4377 F5            [11]   94 	push	af
   4378 33            [ 6]   95 	inc	sp
   4379 E5            [11]   96 	push	hl
   437A CD F3 48      [17]   97 	call	_cpct_drawSolidBox
   437D F1            [10]   98 	pop	af
   437E F1            [10]   99 	pop	af
   437F 33            [ 6]  100 	inc	sp
   4380 C9            [10]  101 	ret
                            102 ;src/systems/tilemap.c:21: u8 tilemap_ground_y(void) {
                            103 ;	---------------------------------
                            104 ; Function tilemap_ground_y
                            105 ; ---------------------------------
   4381                     106 _tilemap_ground_y::
                            107 ;src/systems/tilemap.c:22: return gtilegroundy;
   4381 FD 21 F0 49   [14]  108 	ld	iy, #_gtilegroundy
   4385 FD 6E 00      [19]  109 	ld	l, 0 (iy)
   4388 C9            [10]  110 	ret
                            111 	.area _CODE
                            112 	.area _INITIALIZER
   4A07                     113 __xinit__gtilegroundy:
   4A07 A0                  114 	.db #0xa0	; 160
                            115 	.area _CABS (ABS)
