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
                             16 	.globl _tilemap_platform_y_at
                             17 	.globl _tilemap_is_trap
                             18 	.globl _tilemap_goal_x
                             19 ;--------------------------------------------------------
                             20 ; special function registers
                             21 ;--------------------------------------------------------
                             22 ;--------------------------------------------------------
                             23 ; ram data
                             24 ;--------------------------------------------------------
                             25 	.area _DATA
                             26 ;--------------------------------------------------------
                             27 ; ram data
                             28 ;--------------------------------------------------------
                             29 	.area _INITIALIZED
   5AA2                      30 _gtilegroundy:
   5AA2                      31 	.ds 1
   5AA3                      32 _gtileplatformy:
   5AA3                      33 	.ds 1
   5AA4                      34 _ggoalx:
   5AA4                      35 	.ds 1
                             36 ;--------------------------------------------------------
                             37 ; absolute external ram data
                             38 ;--------------------------------------------------------
                             39 	.area _DABS (ABS)
                             40 ;--------------------------------------------------------
                             41 ; global & static initialisations
                             42 ;--------------------------------------------------------
                             43 	.area _HOME
                             44 	.area _GSINIT
                             45 	.area _GSFINAL
                             46 	.area _GSINIT
                             47 ;--------------------------------------------------------
                             48 ; Home
                             49 ;--------------------------------------------------------
                             50 	.area _HOME
                             51 	.area _HOME
                             52 ;--------------------------------------------------------
                             53 ; code
                             54 ;--------------------------------------------------------
                             55 	.area _CODE
                             56 ;src/systems/tilemap.c:9: void tilemap_init(void) {
                             57 ;	---------------------------------
                             58 ; Function tilemap_init
                             59 ; ---------------------------------
   4B1E                      60 _tilemap_init::
                             61 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   4B1E 2A 73 4C      [16]   62 	ld	hl, (_level1tilemapheight)
   4B21 3E 02         [ 7]   63 	ld	a, #0x02
   4B23 BD            [ 4]   64 	cp	a, l
   4B24 3E 00         [ 7]   65 	ld	a, #0x00
   4B26 9C            [ 4]   66 	sbc	a, h
   4B27 30 0D         [12]   67 	jr	NC,00102$
                             68 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4B29 7D            [ 4]   69 	ld	a, l
   4B2A C6 FE         [ 7]   70 	add	a, #0xfe
   4B2C 07            [ 4]   71 	rlca
   4B2D 07            [ 4]   72 	rlca
   4B2E 07            [ 4]   73 	rlca
   4B2F E6 F8         [ 7]   74 	and	a, #0xf8
   4B31 32 A2 5A      [13]   75 	ld	(#_gtilegroundy + 0),a
   4B34 18 05         [12]   76 	jr	00103$
   4B36                      77 00102$:
                             78 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   4B36 21 A2 5A      [10]   79 	ld	hl,#_gtilegroundy + 0
   4B39 36 A0         [10]   80 	ld	(hl), #0xa0
   4B3B                      81 00103$:
                             82 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   4B3B 21 A3 5A      [10]   83 	ld	hl, #_gtileplatformy
   4B3E 3A A2 5A      [13]   84 	ld	a,(#_gtilegroundy + 0)
   4B41 C6 E8         [ 7]   85 	add	a, #0xe8
   4B43 77            [ 7]   86 	ld	(hl), a
                             87 ;src/systems/tilemap.c:16: ggoalx = 72;
   4B44 21 A4 5A      [10]   88 	ld	hl,#_ggoalx + 0
   4B47 36 48         [10]   89 	ld	(hl), #0x48
   4B49 C9            [10]   90 	ret
                             91 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             92 ;	---------------------------------
                             93 ; Function tilemap_render
                             94 ; ---------------------------------
   4B4A                      95 _tilemap_render::
                             96 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4B4A 3A A2 5A      [13]   97 	ld	a, (_gtilegroundy)
   4B4D F5            [11]   98 	push	af
   4B4E 33            [ 6]   99 	inc	sp
   4B4F AF            [ 4]  100 	xor	a, a
   4B50 F5            [11]  101 	push	af
   4B51 33            [ 6]  102 	inc	sp
   4B52 21 00 C0      [10]  103 	ld	hl, #0xc000
   4B55 E5            [11]  104 	push	hl
   4B56 CD D5 59      [17]  105 	call	_cpct_getScreenPtr
                            106 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4B59 01 50 08      [10]  107 	ld	bc, #0x0850
   4B5C C5            [11]  108 	push	bc
   4B5D 3E 11         [ 7]  109 	ld	a, #0x11
   4B5F F5            [11]  110 	push	af
   4B60 33            [ 6]  111 	inc	sp
   4B61 E5            [11]  112 	push	hl
   4B62 CD 1C 59      [17]  113 	call	_cpct_drawSolidBox
   4B65 F1            [10]  114 	pop	af
   4B66 F1            [10]  115 	pop	af
   4B67 33            [ 6]  116 	inc	sp
                            117 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   4B68 3A A3 5A      [13]  118 	ld	a, (_gtileplatformy)
   4B6B 57            [ 4]  119 	ld	d,a
   4B6C 1E 18         [ 7]  120 	ld	e,#0x18
   4B6E D5            [11]  121 	push	de
   4B6F 21 00 C0      [10]  122 	ld	hl, #0xc000
   4B72 E5            [11]  123 	push	hl
   4B73 CD D5 59      [17]  124 	call	_cpct_getScreenPtr
                            125 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   4B76 01 20 04      [10]  126 	ld	bc, #0x0420
   4B79 C5            [11]  127 	push	bc
   4B7A 3E 33         [ 7]  128 	ld	a, #0x33
   4B7C F5            [11]  129 	push	af
   4B7D 33            [ 6]  130 	inc	sp
   4B7E E5            [11]  131 	push	hl
   4B7F CD 1C 59      [17]  132 	call	_cpct_drawSolidBox
   4B82 F1            [10]  133 	pop	af
   4B83 F1            [10]  134 	pop	af
   4B84 33            [ 6]  135 	inc	sp
                            136 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   4B85 21 A2 5A      [10]  137 	ld	hl,#_gtilegroundy + 0
   4B88 46            [ 7]  138 	ld	b, (hl)
   4B89 05            [ 4]  139 	dec	b
   4B8A 05            [ 4]  140 	dec	b
   4B8B C5            [11]  141 	push	bc
   4B8C 33            [ 6]  142 	inc	sp
   4B8D 3E 38         [ 7]  143 	ld	a, #0x38
   4B8F F5            [11]  144 	push	af
   4B90 33            [ 6]  145 	inc	sp
   4B91 21 00 C0      [10]  146 	ld	hl, #0xc000
   4B94 E5            [11]  147 	push	hl
   4B95 CD D5 59      [17]  148 	call	_cpct_getScreenPtr
                            149 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   4B98 01 10 02      [10]  150 	ld	bc, #0x0210
   4B9B C5            [11]  151 	push	bc
   4B9C 3E 66         [ 7]  152 	ld	a, #0x66
   4B9E F5            [11]  153 	push	af
   4B9F 33            [ 6]  154 	inc	sp
   4BA0 E5            [11]  155 	push	hl
   4BA1 CD 1C 59      [17]  156 	call	_cpct_drawSolidBox
   4BA4 F1            [10]  157 	pop	af
   4BA5 F1            [10]  158 	pop	af
   4BA6 33            [ 6]  159 	inc	sp
                            160 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   4BA7 3A A2 5A      [13]  161 	ld	a,(#_gtilegroundy + 0)
   4BAA C6 F0         [ 7]  162 	add	a, #0xf0
   4BAC 47            [ 4]  163 	ld	b, a
   4BAD C5            [11]  164 	push	bc
   4BAE 33            [ 6]  165 	inc	sp
   4BAF 3A A4 5A      [13]  166 	ld	a, (_ggoalx)
   4BB2 F5            [11]  167 	push	af
   4BB3 33            [ 6]  168 	inc	sp
   4BB4 21 00 C0      [10]  169 	ld	hl, #0xc000
   4BB7 E5            [11]  170 	push	hl
   4BB8 CD D5 59      [17]  171 	call	_cpct_getScreenPtr
                            172 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   4BBB 01 02 10      [10]  173 	ld	bc, #0x1002
   4BBE C5            [11]  174 	push	bc
   4BBF 3E 5F         [ 7]  175 	ld	a, #0x5f
   4BC1 F5            [11]  176 	push	af
   4BC2 33            [ 6]  177 	inc	sp
   4BC3 E5            [11]  178 	push	hl
   4BC4 CD 1C 59      [17]  179 	call	_cpct_drawSolidBox
   4BC7 F1            [10]  180 	pop	af
   4BC8 F1            [10]  181 	pop	af
   4BC9 33            [ 6]  182 	inc	sp
   4BCA C9            [10]  183 	ret
                            184 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            185 ;	---------------------------------
                            186 ; Function tilemap_ground_y
                            187 ; ---------------------------------
   4BCB                     188 _tilemap_ground_y::
                            189 ;src/systems/tilemap.c:35: return gtilegroundy;
   4BCB FD 21 A2 5A   [14]  190 	ld	iy, #_gtilegroundy
   4BCF FD 6E 00      [19]  191 	ld	l, 0 (iy)
   4BD2 C9            [10]  192 	ret
                            193 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            194 ;	---------------------------------
                            195 ; Function tilemap_platform_y_at
                            196 ; ---------------------------------
   4BD3                     197 _tilemap_platform_y_at::
                            198 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   4BD3 FD 21 02 00   [14]  199 	ld	iy, #2
   4BD7 FD 39         [15]  200 	add	iy, sp
   4BD9 FD 7E 00      [19]  201 	ld	a, 0 (iy)
   4BDC D6 18         [ 7]  202 	sub	a, #0x18
   4BDE FD 7E 01      [19]  203 	ld	a, 1 (iy)
   4BE1 17            [ 4]  204 	rla
   4BE2 3F            [ 4]  205 	ccf
   4BE3 1F            [ 4]  206 	rra
   4BE4 DE 80         [ 7]  207 	sbc	a, #0x80
   4BE6 38 1A         [12]  208 	jr	C,00102$
   4BE8 3E 38         [ 7]  209 	ld	a, #0x38
   4BEA FD BE 00      [19]  210 	cp	a, 0 (iy)
   4BED 3E 00         [ 7]  211 	ld	a, #0x00
   4BEF FD 9E 01      [19]  212 	sbc	a, 1 (iy)
   4BF2 E2 F7 4B      [10]  213 	jp	PO, 00114$
   4BF5 EE 80         [ 7]  214 	xor	a, #0x80
   4BF7                     215 00114$:
   4BF7 FA 02 4C      [10]  216 	jp	M, 00102$
                            217 ;src/systems/tilemap.c:40: return gtileplatformy;
   4BFA FD 21 A3 5A   [14]  218 	ld	iy, #_gtileplatformy
   4BFE FD 6E 00      [19]  219 	ld	l, 0 (iy)
   4C01 C9            [10]  220 	ret
   4C02                     221 00102$:
                            222 ;src/systems/tilemap.c:42: return 255;
   4C02 2E FF         [ 7]  223 	ld	l, #0xff
   4C04 C9            [10]  224 	ret
                            225 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            226 ;	---------------------------------
                            227 ; Function tilemap_is_trap
                            228 ; ---------------------------------
   4C05                     229 _tilemap_is_trap::
   4C05 DD E5         [15]  230 	push	ix
   4C07 DD 21 00 00   [14]  231 	ld	ix,#0
   4C0B DD 39         [15]  232 	add	ix,sp
   4C0D F5            [11]  233 	push	af
                            234 ;src/systems/tilemap.c:50: left = x;
   4C0E DD 4E 04      [19]  235 	ld	c,4 (ix)
   4C11 DD 46 05      [19]  236 	ld	b,5 (ix)
                            237 ;src/systems/tilemap.c:51: right = x + (i16)w;
   4C14 DD 6E 08      [19]  238 	ld	l, 8 (ix)
   4C17 26 00         [ 7]  239 	ld	h, #0x00
   4C19 09            [11]  240 	add	hl, bc
   4C1A 33            [ 6]  241 	inc	sp
   4C1B 33            [ 6]  242 	inc	sp
   4C1C E5            [11]  243 	push	hl
                            244 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   4C1D DD 5E 09      [19]  245 	ld	e, 9 (ix)
   4C20 16 00         [ 7]  246 	ld	d, #0x00
   4C22 DD 6E 06      [19]  247 	ld	l,6 (ix)
   4C25 DD 66 07      [19]  248 	ld	h,7 (ix)
   4C28 19            [11]  249 	add	hl, de
   4C29 EB            [ 4]  250 	ex	de,hl
                            251 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   4C2A FD 21 A2 5A   [14]  252 	ld	iy, #_gtilegroundy
   4C2E FD 6E 00      [19]  253 	ld	l, 0 (iy)
   4C31 26 00         [ 7]  254 	ld	h, #0x00
   4C33 2B            [ 6]  255 	dec	hl
   4C34 2B            [ 6]  256 	dec	hl
   4C35 7B            [ 4]  257 	ld	a, e
   4C36 95            [ 4]  258 	sub	a, l
   4C37 7A            [ 4]  259 	ld	a, d
   4C38 9C            [ 4]  260 	sbc	a, h
   4C39 E2 3E 4C      [10]  261 	jp	PO, 00119$
   4C3C EE 80         [ 7]  262 	xor	a, #0x80
   4C3E                     263 00119$:
   4C3E FA 62 4C      [10]  264 	jp	M, 00102$
   4C41 79            [ 4]  265 	ld	a, c
   4C42 D6 48         [ 7]  266 	sub	a, #0x48
   4C44 78            [ 4]  267 	ld	a, b
   4C45 17            [ 4]  268 	rla
   4C46 3F            [ 4]  269 	ccf
   4C47 1F            [ 4]  270 	rra
   4C48 DE 80         [ 7]  271 	sbc	a, #0x80
   4C4A 30 16         [12]  272 	jr	NC,00102$
   4C4C 3E 38         [ 7]  273 	ld	a, #0x38
   4C4E DD BE FE      [19]  274 	cp	a, -2 (ix)
   4C51 3E 00         [ 7]  275 	ld	a, #0x00
   4C53 DD 9E FF      [19]  276 	sbc	a, -1 (ix)
   4C56 E2 5B 4C      [10]  277 	jp	PO, 00120$
   4C59 EE 80         [ 7]  278 	xor	a, #0x80
   4C5B                     279 00120$:
   4C5B F2 62 4C      [10]  280 	jp	P, 00102$
                            281 ;src/systems/tilemap.c:55: return 1;
   4C5E 2E 01         [ 7]  282 	ld	l, #0x01
   4C60 18 02         [12]  283 	jr	00105$
   4C62                     284 00102$:
                            285 ;src/systems/tilemap.c:57: return 0;
   4C62 2E 00         [ 7]  286 	ld	l, #0x00
   4C64                     287 00105$:
   4C64 DD F9         [10]  288 	ld	sp, ix
   4C66 DD E1         [14]  289 	pop	ix
   4C68 C9            [10]  290 	ret
                            291 ;src/systems/tilemap.c:60: u8 tilemap_goal_x(void) {
                            292 ;	---------------------------------
                            293 ; Function tilemap_goal_x
                            294 ; ---------------------------------
   4C69                     295 _tilemap_goal_x::
                            296 ;src/systems/tilemap.c:61: return ggoalx;
   4C69 FD 21 A4 5A   [14]  297 	ld	iy, #_ggoalx
   4C6D FD 6E 00      [19]  298 	ld	l, 0 (iy)
   4C70 C9            [10]  299 	ret
                            300 	.area _CODE
                            301 	.area _INITIALIZER
   5ABD                     302 __xinit__gtilegroundy:
   5ABD A0                  303 	.db #0xa0	; 160
   5ABE                     304 __xinit__gtileplatformy:
   5ABE 80                  305 	.db #0x80	; 128
   5ABF                     306 __xinit__ggoalx:
   5ABF 48                  307 	.db #0x48	; 72	'H'
                            308 	.area _CABS (ABS)
