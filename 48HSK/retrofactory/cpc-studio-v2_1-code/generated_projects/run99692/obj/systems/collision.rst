                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module collision
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _tilemap_ground_y
                             12 	.globl _collision_init
                             13 	.globl _collision_is_on_ground
                             14 	.globl _collision_clamp_y_to_ground
                             15 ;--------------------------------------------------------
                             16 ; special function registers
                             17 ;--------------------------------------------------------
                             18 ;--------------------------------------------------------
                             19 ; ram data
                             20 ;--------------------------------------------------------
                             21 	.area _DATA
                             22 ;--------------------------------------------------------
                             23 ; ram data
                             24 ;--------------------------------------------------------
                             25 	.area _INITIALIZED
   48D3                      26 _ggroundy:
   48D3                      27 	.ds 2
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
                             48 ;src/systems/collision.c:6: void collision_init(void) {
                             49 ;	---------------------------------
                             50 ; Function collision_init
                             51 ; ---------------------------------
   4057                      52 _collision_init::
                             53 ;src/systems/collision.c:7: ggroundy = (i16)tilemap_ground_y();
   4057 CD 81 43      [17]   54 	call	_tilemap_ground_y
   405A FD 21 D3 48   [14]   55 	ld	iy, #_ggroundy
   405E FD 75 00      [19]   56 	ld	0 (iy), l
   4061 FD 36 01 00   [19]   57 	ld	1 (iy), #0x00
   4065 C9            [10]   58 	ret
                             59 ;src/systems/collision.c:10: u8 collision_is_on_ground(i16 y, u8 h) {
                             60 ;	---------------------------------
                             61 ; Function collision_is_on_ground
                             62 ; ---------------------------------
   4066                      63 _collision_is_on_ground::
                             64 ;src/systems/collision.c:12: feet = y + (i16)h;
   4066 21 04 00      [10]   65 	ld	hl, #4+0
   4069 39            [11]   66 	add	hl, sp
   406A 4E            [ 7]   67 	ld	c, (hl)
   406B 06 00         [ 7]   68 	ld	b, #0x00
   406D 21 02 00      [10]   69 	ld	hl, #2
   4070 39            [11]   70 	add	hl, sp
   4071 7E            [ 7]   71 	ld	a, (hl)
   4072 23            [ 6]   72 	inc	hl
   4073 66            [ 7]   73 	ld	h, (hl)
   4074 6F            [ 4]   74 	ld	l, a
   4075 09            [11]   75 	add	hl, bc
   4076 4D            [ 4]   76 	ld	c, l
   4077 44            [ 4]   77 	ld	b, h
                             78 ;src/systems/collision.c:13: return (u8)(feet >= ggroundy);
   4078 21 D3 48      [10]   79 	ld	hl, #_ggroundy
   407B 79            [ 4]   80 	ld	a, c
   407C 96            [ 7]   81 	sub	a, (hl)
   407D 78            [ 4]   82 	ld	a, b
   407E 23            [ 6]   83 	inc	hl
   407F 9E            [ 7]   84 	sbc	a, (hl)
   4080 E2 85 40      [10]   85 	jp	PO, 00103$
   4083 EE 80         [ 7]   86 	xor	a, #0x80
   4085                      87 00103$:
   4085 07            [ 4]   88 	rlca
   4086 E6 01         [ 7]   89 	and	a,#0x01
   4088 EE 01         [ 7]   90 	xor	a, #0x01
   408A 6F            [ 4]   91 	ld	l, a
   408B C9            [10]   92 	ret
                             93 ;src/systems/collision.c:16: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                             94 ;	---------------------------------
                             95 ; Function collision_clamp_y_to_ground
                             96 ; ---------------------------------
   408C                      97 _collision_clamp_y_to_ground::
                             98 ;src/systems/collision.c:18: maxy = ggroundy - (i16)h;
   408C 21 04 00      [10]   99 	ld	hl, #4+0
   408F 39            [11]  100 	add	hl, sp
   4090 4E            [ 7]  101 	ld	c, (hl)
   4091 06 00         [ 7]  102 	ld	b, #0x00
   4093 FD 21 D3 48   [14]  103 	ld	iy, #_ggroundy
   4097 FD 7E 00      [19]  104 	ld	a, 0 (iy)
   409A 91            [ 4]  105 	sub	a, c
   409B 4F            [ 4]  106 	ld	c, a
   409C FD 7E 01      [19]  107 	ld	a, 1 (iy)
   409F 98            [ 4]  108 	sbc	a, b
   40A0 47            [ 4]  109 	ld	b, a
                            110 ;src/systems/collision.c:19: if (y > maxy) {
   40A1 79            [ 4]  111 	ld	a, c
   40A2 FD 21 02 00   [14]  112 	ld	iy, #2
   40A6 FD 39         [15]  113 	add	iy, sp
   40A8 FD 96 00      [19]  114 	sub	a, 0 (iy)
   40AB 78            [ 4]  115 	ld	a, b
   40AC FD 9E 01      [19]  116 	sbc	a, 1 (iy)
   40AF E2 B4 40      [10]  117 	jp	PO, 00109$
   40B2 EE 80         [ 7]  118 	xor	a, #0x80
   40B4                     119 00109$:
   40B4 F2 BA 40      [10]  120 	jp	P, 00102$
                            121 ;src/systems/collision.c:20: return maxy;
   40B7 69            [ 4]  122 	ld	l, c
   40B8 60            [ 4]  123 	ld	h, b
   40B9 C9            [10]  124 	ret
   40BA                     125 00102$:
                            126 ;src/systems/collision.c:22: return y;
   40BA C1            [10]  127 	pop	bc
   40BB E1            [10]  128 	pop	hl
   40BC E5            [11]  129 	push	hl
   40BD C5            [11]  130 	push	bc
   40BE C9            [10]  131 	ret
                            132 	.area _CODE
                            133 	.area _INITIALIZER
   48EA                     134 __xinit__ggroundy:
   48EA A0 00               135 	.dw #0x00a0
                            136 	.area _CABS (ABS)
