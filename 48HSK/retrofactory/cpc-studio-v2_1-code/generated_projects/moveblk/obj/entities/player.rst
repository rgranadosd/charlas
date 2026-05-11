                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module player
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSolidBox
                             13 	.globl _cpct_isKeyPressed
                             14 	.globl _player_init
                             15 	.globl _player_update
                             16 	.globl _player_render
                             17 ;--------------------------------------------------------
                             18 ; special function registers
                             19 ;--------------------------------------------------------
                             20 ;--------------------------------------------------------
                             21 ; ram data
                             22 ;--------------------------------------------------------
                             23 	.area _DATA
   423D                      24 _px:
   423D                      25 	.ds 1
   423E                      26 _py:
   423E                      27 	.ds 1
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _INITIALIZED
                             32 ;--------------------------------------------------------
                             33 ; absolute external ram data
                             34 ;--------------------------------------------------------
                             35 	.area _DABS (ABS)
                             36 ;--------------------------------------------------------
                             37 ; global & static initialisations
                             38 ;--------------------------------------------------------
                             39 	.area _HOME
                             40 	.area _GSINIT
                             41 	.area _GSFINAL
                             42 	.area _GSINIT
                             43 ;--------------------------------------------------------
                             44 ; Home
                             45 ;--------------------------------------------------------
                             46 	.area _HOME
                             47 	.area _HOME
                             48 ;--------------------------------------------------------
                             49 ; code
                             50 ;--------------------------------------------------------
                             51 	.area _CODE
                             52 ;src/entities/player.c:7: void player_init(void) {
                             53 ;	---------------------------------
                             54 ; Function player_init
                             55 ; ---------------------------------
   4033                      56 _player_init::
                             57 ;src/entities/player.c:8: px = 20;
   4033 21 3D 42      [10]   58 	ld	hl,#_px + 0
   4036 36 14         [10]   59 	ld	(hl), #0x14
                             60 ;src/entities/player.c:9: py = 80;
   4038 21 3E 42      [10]   61 	ld	hl,#_py + 0
   403B 36 50         [10]   62 	ld	(hl), #0x50
   403D C9            [10]   63 	ret
                             64 ;src/entities/player.c:12: void player_update(void) {
                             65 ;	---------------------------------
                             66 ; Function player_update
                             67 ; ---------------------------------
   403E                      68 _player_update::
                             69 ;src/entities/player.c:13: if (cpct_isKeyPressed(Key_CursorLeft) && px > 0)
   403E 21 01 01      [10]   70 	ld	hl, #0x0101
   4041 CD B0 40      [17]   71 	call	_cpct_isKeyPressed
   4044 7D            [ 4]   72 	ld	a, l
   4045 B7            [ 4]   73 	or	a, a
   4046 28 10         [12]   74 	jr	Z,00102$
   4048 FD 21 3D 42   [14]   75 	ld	iy, #_px
   404C FD 7E 00      [19]   76 	ld	a, 0 (iy)
   404F B7            [ 4]   77 	or	a, a
   4050 28 06         [12]   78 	jr	Z,00102$
                             79 ;src/entities/player.c:14: px -= 2;
   4052 FD 35 00      [23]   80 	dec	0 (iy)
   4055 FD 35 00      [23]   81 	dec	0 (iy)
   4058                      82 00102$:
                             83 ;src/entities/player.c:16: if (cpct_isKeyPressed(Key_CursorRight) && px < 70)
   4058 21 00 02      [10]   84 	ld	hl, #0x0200
   405B CD B0 40      [17]   85 	call	_cpct_isKeyPressed
   405E 7D            [ 4]   86 	ld	a, l
   405F B7            [ 4]   87 	or	a, a
   4060 C8            [11]   88 	ret	Z
   4061 FD 21 3D 42   [14]   89 	ld	iy, #_px
   4065 FD 7E 00      [19]   90 	ld	a, 0 (iy)
   4068 D6 46         [ 7]   91 	sub	a, #0x46
   406A D0            [11]   92 	ret	NC
                             93 ;src/entities/player.c:17: px += 2;
   406B FD 34 00      [23]   94 	inc	0 (iy)
   406E FD 34 00      [23]   95 	inc	0 (iy)
   4071 C9            [10]   96 	ret
                             97 ;src/entities/player.c:20: void player_render(void) {
                             98 ;	---------------------------------
                             99 ; Function player_render
                            100 ; ---------------------------------
   4072                     101 _player_render::
                            102 ;src/entities/player.c:23: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, py);
   4072 3A 3E 42      [13]  103 	ld	a, (_py)
   4075 F5            [11]  104 	push	af
   4076 33            [ 6]  105 	inc	sp
   4077 AF            [ 4]  106 	xor	a, a
   4078 F5            [11]  107 	push	af
   4079 33            [ 6]  108 	inc	sp
   407A 21 00 C0      [10]  109 	ld	hl, #0xc000
   407D E5            [11]  110 	push	hl
   407E CD 1D 42      [17]  111 	call	_cpct_getScreenPtr
                            112 ;src/entities/player.c:24: cpct_drawSolidBox(pvmem, 0x00, 80, 8);
   4081 01 50 08      [10]  113 	ld	bc, #0x0850
   4084 C5            [11]  114 	push	bc
   4085 AF            [ 4]  115 	xor	a, a
   4086 F5            [11]  116 	push	af
   4087 33            [ 6]  117 	inc	sp
   4088 E5            [11]  118 	push	hl
   4089 CD 64 41      [17]  119 	call	_cpct_drawSolidBox
   408C F1            [10]  120 	pop	af
   408D F1            [10]  121 	pop	af
   408E 33            [ 6]  122 	inc	sp
                            123 ;src/entities/player.c:26: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, px, py);
   408F 3A 3E 42      [13]  124 	ld	a, (_py)
   4092 F5            [11]  125 	push	af
   4093 33            [ 6]  126 	inc	sp
   4094 3A 3D 42      [13]  127 	ld	a, (_px)
   4097 F5            [11]  128 	push	af
   4098 33            [ 6]  129 	inc	sp
   4099 21 00 C0      [10]  130 	ld	hl, #0xc000
   409C E5            [11]  131 	push	hl
   409D CD 1D 42      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/entities/player.c:27: cpct_drawSolidBox(pvmem, 0xF0, 4, 8);
   40A0 01 04 08      [10]  134 	ld	bc, #0x0804
   40A3 C5            [11]  135 	push	bc
   40A4 3E F0         [ 7]  136 	ld	a, #0xf0
   40A6 F5            [11]  137 	push	af
   40A7 33            [ 6]  138 	inc	sp
   40A8 E5            [11]  139 	push	hl
   40A9 CD 64 41      [17]  140 	call	_cpct_drawSolidBox
   40AC F1            [10]  141 	pop	af
   40AD F1            [10]  142 	pop	af
   40AE 33            [ 6]  143 	inc	sp
   40AF C9            [10]  144 	ret
                            145 	.area _CODE
                            146 	.area _INITIALIZER
                            147 	.area _CABS (ABS)
