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
                             18 	.globl _tilemap_is_ladder
                             19 	.globl _tilemap_is_hidden_zone
                             20 	.globl _tilemap_goal_x
                             21 ;--------------------------------------------------------
                             22 ; special function registers
                             23 ;--------------------------------------------------------
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _DATA
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _INITIALIZED
   5F34                      32 _gtilegroundy:
   5F34                      33 	.ds 1
   5F35                      34 _gtileplatformy:
   5F35                      35 	.ds 1
   5F36                      36 _ggoalx:
   5F36                      37 	.ds 1
   5F37                      38 _gladderx:
   5F37                      39 	.ds 1
                             40 ;--------------------------------------------------------
                             41 ; absolute external ram data
                             42 ;--------------------------------------------------------
                             43 	.area _DABS (ABS)
                             44 ;--------------------------------------------------------
                             45 ; global & static initialisations
                             46 ;--------------------------------------------------------
                             47 	.area _HOME
                             48 	.area _GSINIT
                             49 	.area _GSFINAL
                             50 	.area _GSINIT
                             51 ;--------------------------------------------------------
                             52 ; Home
                             53 ;--------------------------------------------------------
                             54 	.area _HOME
                             55 	.area _HOME
                             56 ;--------------------------------------------------------
                             57 ; code
                             58 ;--------------------------------------------------------
                             59 	.area _CODE
                             60 ;src/systems/tilemap.c:10: void tilemap_init(void) {
                             61 ;	---------------------------------
                             62 ; Function tilemap_init
                             63 ; ---------------------------------
   4EBD                      64 _tilemap_init::
                             65 ;src/systems/tilemap.c:11: if (level1tilemapheight > 2) {
   4EBD 2A 53 51      [16]   66 	ld	hl, (_level1tilemapheight)
   4EC0 3E 02         [ 7]   67 	ld	a, #0x02
   4EC2 BD            [ 4]   68 	cp	a, l
   4EC3 3E 00         [ 7]   69 	ld	a, #0x00
   4EC5 9C            [ 4]   70 	sbc	a, h
   4EC6 30 0D         [12]   71 	jr	NC,00102$
                             72 ;src/systems/tilemap.c:12: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4EC8 7D            [ 4]   73 	ld	a, l
   4EC9 C6 FE         [ 7]   74 	add	a, #0xfe
   4ECB 07            [ 4]   75 	rlca
   4ECC 07            [ 4]   76 	rlca
   4ECD 07            [ 4]   77 	rlca
   4ECE E6 F8         [ 7]   78 	and	a, #0xf8
   4ED0 32 34 5F      [13]   79 	ld	(#_gtilegroundy + 0),a
   4ED3 18 05         [12]   80 	jr	00103$
   4ED5                      81 00102$:
                             82 ;src/systems/tilemap.c:14: gtilegroundy = 160;
   4ED5 21 34 5F      [10]   83 	ld	hl,#_gtilegroundy + 0
   4ED8 36 A0         [10]   84 	ld	(hl), #0xa0
   4EDA                      85 00103$:
                             86 ;src/systems/tilemap.c:16: gtileplatformy = (u8)(gtilegroundy - 24);
   4EDA 21 35 5F      [10]   87 	ld	hl, #_gtileplatformy
   4EDD 3A 34 5F      [13]   88 	ld	a,(#_gtilegroundy + 0)
   4EE0 C6 E8         [ 7]   89 	add	a, #0xe8
   4EE2 77            [ 7]   90 	ld	(hl), a
                             91 ;src/systems/tilemap.c:17: ggoalx = 72;
   4EE3 21 36 5F      [10]   92 	ld	hl,#_ggoalx + 0
   4EE6 36 48         [10]   93 	ld	(hl), #0x48
                             94 ;src/systems/tilemap.c:18: gladderx = 36;
   4EE8 21 37 5F      [10]   95 	ld	hl,#_gladderx + 0
   4EEB 36 24         [10]   96 	ld	(hl), #0x24
   4EED C9            [10]   97 	ret
                             98 ;src/systems/tilemap.c:21: void tilemap_render(void) {
                             99 ;	---------------------------------
                            100 ; Function tilemap_render
                            101 ; ---------------------------------
   4EEE                     102 _tilemap_render::
                            103 ;src/systems/tilemap.c:23: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4EEE 3A 34 5F      [13]  104 	ld	a, (_gtilegroundy)
   4EF1 F5            [11]  105 	push	af
   4EF2 33            [ 6]  106 	inc	sp
   4EF3 AF            [ 4]  107 	xor	a, a
   4EF4 F5            [11]  108 	push	af
   4EF5 33            [ 6]  109 	inc	sp
   4EF6 21 00 C0      [10]  110 	ld	hl, #0xc000
   4EF9 E5            [11]  111 	push	hl
   4EFA CD 4E 5E      [17]  112 	call	_cpct_getScreenPtr
                            113 ;src/systems/tilemap.c:24: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4EFD 01 50 08      [10]  114 	ld	bc, #0x0850
   4F00 C5            [11]  115 	push	bc
   4F01 3E 11         [ 7]  116 	ld	a, #0x11
   4F03 F5            [11]  117 	push	af
   4F04 33            [ 6]  118 	inc	sp
   4F05 E5            [11]  119 	push	hl
   4F06 CD 95 5D      [17]  120 	call	_cpct_drawSolidBox
   4F09 F1            [10]  121 	pop	af
   4F0A F1            [10]  122 	pop	af
   4F0B 33            [ 6]  123 	inc	sp
                            124 ;src/systems/tilemap.c:26: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   4F0C 3A 35 5F      [13]  125 	ld	a, (_gtileplatformy)
   4F0F 57            [ 4]  126 	ld	d,a
   4F10 1E 18         [ 7]  127 	ld	e,#0x18
   4F12 D5            [11]  128 	push	de
   4F13 21 00 C0      [10]  129 	ld	hl, #0xc000
   4F16 E5            [11]  130 	push	hl
   4F17 CD 4E 5E      [17]  131 	call	_cpct_getScreenPtr
                            132 ;src/systems/tilemap.c:27: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   4F1A 01 20 04      [10]  133 	ld	bc, #0x0420
   4F1D C5            [11]  134 	push	bc
   4F1E 3E 33         [ 7]  135 	ld	a, #0x33
   4F20 F5            [11]  136 	push	af
   4F21 33            [ 6]  137 	inc	sp
   4F22 E5            [11]  138 	push	hl
   4F23 CD 95 5D      [17]  139 	call	_cpct_drawSolidBox
   4F26 F1            [10]  140 	pop	af
   4F27 F1            [10]  141 	pop	af
   4F28 33            [ 6]  142 	inc	sp
                            143 ;src/systems/tilemap.c:29: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, gladderx, gtileplatformy);
   4F29 3A 35 5F      [13]  144 	ld	a, (_gtileplatformy)
   4F2C F5            [11]  145 	push	af
   4F2D 33            [ 6]  146 	inc	sp
   4F2E 3A 37 5F      [13]  147 	ld	a, (_gladderx)
   4F31 F5            [11]  148 	push	af
   4F32 33            [ 6]  149 	inc	sp
   4F33 21 00 C0      [10]  150 	ld	hl, #0xc000
   4F36 E5            [11]  151 	push	hl
   4F37 CD 4E 5E      [17]  152 	call	_cpct_getScreenPtr
   4F3A 4D            [ 4]  153 	ld	c, l
   4F3B 44            [ 4]  154 	ld	b, h
                            155 ;src/systems/tilemap.c:30: cpct_drawSolidBox(pvmem, 0x4A, 2, (u8)(gtilegroundy - gtileplatformy));
   4F3C 21 35 5F      [10]  156 	ld	hl, #_gtileplatformy
   4F3F 3A 34 5F      [13]  157 	ld	a,(#_gtilegroundy + 0)
   4F42 96            [ 7]  158 	sub	a, (hl)
   4F43 57            [ 4]  159 	ld	d, a
   4F44 D5            [11]  160 	push	de
   4F45 33            [ 6]  161 	inc	sp
   4F46 21 4A 02      [10]  162 	ld	hl, #0x024a
   4F49 E5            [11]  163 	push	hl
   4F4A C5            [11]  164 	push	bc
   4F4B CD 95 5D      [17]  165 	call	_cpct_drawSolidBox
   4F4E F1            [10]  166 	pop	af
                            167 ;src/systems/tilemap.c:32: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 4, 56);
   4F4F 33            [ 6]  168 	inc	sp
   4F50 21 04 38      [10]  169 	ld	hl,#0x3804
   4F53 E3            [19]  170 	ex	(sp),hl
   4F54 21 00 C0      [10]  171 	ld	hl, #0xc000
   4F57 E5            [11]  172 	push	hl
   4F58 CD 4E 5E      [17]  173 	call	_cpct_getScreenPtr
                            174 ;src/systems/tilemap.c:33: cpct_drawSolidBox(pvmem, 0x22, 14, 8);
   4F5B 01 0E 08      [10]  175 	ld	bc, #0x080e
   4F5E C5            [11]  176 	push	bc
   4F5F 3E 22         [ 7]  177 	ld	a, #0x22
   4F61 F5            [11]  178 	push	af
   4F62 33            [ 6]  179 	inc	sp
   4F63 E5            [11]  180 	push	hl
   4F64 CD 95 5D      [17]  181 	call	_cpct_drawSolidBox
   4F67 F1            [10]  182 	pop	af
   4F68 F1            [10]  183 	pop	af
   4F69 33            [ 6]  184 	inc	sp
                            185 ;src/systems/tilemap.c:35: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   4F6A 21 34 5F      [10]  186 	ld	hl,#_gtilegroundy + 0
   4F6D 46            [ 7]  187 	ld	b, (hl)
   4F6E 05            [ 4]  188 	dec	b
   4F6F 05            [ 4]  189 	dec	b
   4F70 C5            [11]  190 	push	bc
   4F71 33            [ 6]  191 	inc	sp
   4F72 3E 38         [ 7]  192 	ld	a, #0x38
   4F74 F5            [11]  193 	push	af
   4F75 33            [ 6]  194 	inc	sp
   4F76 21 00 C0      [10]  195 	ld	hl, #0xc000
   4F79 E5            [11]  196 	push	hl
   4F7A CD 4E 5E      [17]  197 	call	_cpct_getScreenPtr
                            198 ;src/systems/tilemap.c:36: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   4F7D 01 10 02      [10]  199 	ld	bc, #0x0210
   4F80 C5            [11]  200 	push	bc
   4F81 3E 66         [ 7]  201 	ld	a, #0x66
   4F83 F5            [11]  202 	push	af
   4F84 33            [ 6]  203 	inc	sp
   4F85 E5            [11]  204 	push	hl
   4F86 CD 95 5D      [17]  205 	call	_cpct_drawSolidBox
   4F89 F1            [10]  206 	pop	af
   4F8A F1            [10]  207 	pop	af
   4F8B 33            [ 6]  208 	inc	sp
                            209 ;src/systems/tilemap.c:38: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   4F8C 3A 34 5F      [13]  210 	ld	a,(#_gtilegroundy + 0)
   4F8F C6 F0         [ 7]  211 	add	a, #0xf0
   4F91 47            [ 4]  212 	ld	b, a
   4F92 C5            [11]  213 	push	bc
   4F93 33            [ 6]  214 	inc	sp
   4F94 3A 36 5F      [13]  215 	ld	a, (_ggoalx)
   4F97 F5            [11]  216 	push	af
   4F98 33            [ 6]  217 	inc	sp
   4F99 21 00 C0      [10]  218 	ld	hl, #0xc000
   4F9C E5            [11]  219 	push	hl
   4F9D CD 4E 5E      [17]  220 	call	_cpct_getScreenPtr
                            221 ;src/systems/tilemap.c:39: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   4FA0 01 02 10      [10]  222 	ld	bc, #0x1002
   4FA3 C5            [11]  223 	push	bc
   4FA4 3E 5F         [ 7]  224 	ld	a, #0x5f
   4FA6 F5            [11]  225 	push	af
   4FA7 33            [ 6]  226 	inc	sp
   4FA8 E5            [11]  227 	push	hl
   4FA9 CD 95 5D      [17]  228 	call	_cpct_drawSolidBox
   4FAC F1            [10]  229 	pop	af
   4FAD F1            [10]  230 	pop	af
   4FAE 33            [ 6]  231 	inc	sp
   4FAF C9            [10]  232 	ret
                            233 ;src/systems/tilemap.c:42: u8 tilemap_ground_y(void) {
                            234 ;	---------------------------------
                            235 ; Function tilemap_ground_y
                            236 ; ---------------------------------
   4FB0                     237 _tilemap_ground_y::
                            238 ;src/systems/tilemap.c:43: return gtilegroundy;
   4FB0 FD 21 34 5F   [14]  239 	ld	iy, #_gtilegroundy
   4FB4 FD 6E 00      [19]  240 	ld	l, 0 (iy)
   4FB7 C9            [10]  241 	ret
                            242 ;src/systems/tilemap.c:46: u8 tilemap_platform_y_at(i16 x) {
                            243 ;	---------------------------------
                            244 ; Function tilemap_platform_y_at
                            245 ; ---------------------------------
   4FB8                     246 _tilemap_platform_y_at::
                            247 ;src/systems/tilemap.c:47: if (x >= 24 && x <= 56) {
   4FB8 FD 21 02 00   [14]  248 	ld	iy, #2
   4FBC FD 39         [15]  249 	add	iy, sp
   4FBE FD 7E 00      [19]  250 	ld	a, 0 (iy)
   4FC1 D6 18         [ 7]  251 	sub	a, #0x18
   4FC3 FD 7E 01      [19]  252 	ld	a, 1 (iy)
   4FC6 17            [ 4]  253 	rla
   4FC7 3F            [ 4]  254 	ccf
   4FC8 1F            [ 4]  255 	rra
   4FC9 DE 80         [ 7]  256 	sbc	a, #0x80
   4FCB 38 1A         [12]  257 	jr	C,00102$
   4FCD 3E 38         [ 7]  258 	ld	a, #0x38
   4FCF FD BE 00      [19]  259 	cp	a, 0 (iy)
   4FD2 3E 00         [ 7]  260 	ld	a, #0x00
   4FD4 FD 9E 01      [19]  261 	sbc	a, 1 (iy)
   4FD7 E2 DC 4F      [10]  262 	jp	PO, 00114$
   4FDA EE 80         [ 7]  263 	xor	a, #0x80
   4FDC                     264 00114$:
   4FDC FA E7 4F      [10]  265 	jp	M, 00102$
                            266 ;src/systems/tilemap.c:48: return gtileplatformy;
   4FDF FD 21 35 5F   [14]  267 	ld	iy, #_gtileplatformy
   4FE3 FD 6E 00      [19]  268 	ld	l, 0 (iy)
   4FE6 C9            [10]  269 	ret
   4FE7                     270 00102$:
                            271 ;src/systems/tilemap.c:50: return 255;
   4FE7 2E FF         [ 7]  272 	ld	l, #0xff
   4FE9 C9            [10]  273 	ret
                            274 ;src/systems/tilemap.c:53: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            275 ;	---------------------------------
                            276 ; Function tilemap_is_trap
                            277 ; ---------------------------------
   4FEA                     278 _tilemap_is_trap::
   4FEA DD E5         [15]  279 	push	ix
   4FEC DD 21 00 00   [14]  280 	ld	ix,#0
   4FF0 DD 39         [15]  281 	add	ix,sp
   4FF2 F5            [11]  282 	push	af
                            283 ;src/systems/tilemap.c:58: left = x;
   4FF3 DD 4E 04      [19]  284 	ld	c,4 (ix)
   4FF6 DD 46 05      [19]  285 	ld	b,5 (ix)
                            286 ;src/systems/tilemap.c:59: right = x + (i16)w;
   4FF9 DD 6E 08      [19]  287 	ld	l, 8 (ix)
   4FFC 26 00         [ 7]  288 	ld	h, #0x00
   4FFE 09            [11]  289 	add	hl, bc
   4FFF 33            [ 6]  290 	inc	sp
   5000 33            [ 6]  291 	inc	sp
   5001 E5            [11]  292 	push	hl
                            293 ;src/systems/tilemap.c:60: feet = y + (i16)h;
   5002 DD 5E 09      [19]  294 	ld	e, 9 (ix)
   5005 16 00         [ 7]  295 	ld	d, #0x00
   5007 DD 6E 06      [19]  296 	ld	l,6 (ix)
   500A DD 66 07      [19]  297 	ld	h,7 (ix)
   500D 19            [11]  298 	add	hl, de
   500E EB            [ 4]  299 	ex	de,hl
                            300 ;src/systems/tilemap.c:62: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   500F FD 21 34 5F   [14]  301 	ld	iy, #_gtilegroundy
   5013 FD 6E 00      [19]  302 	ld	l, 0 (iy)
   5016 26 00         [ 7]  303 	ld	h, #0x00
   5018 2B            [ 6]  304 	dec	hl
   5019 2B            [ 6]  305 	dec	hl
   501A 7B            [ 4]  306 	ld	a, e
   501B 95            [ 4]  307 	sub	a, l
   501C 7A            [ 4]  308 	ld	a, d
   501D 9C            [ 4]  309 	sbc	a, h
   501E E2 23 50      [10]  310 	jp	PO, 00119$
   5021 EE 80         [ 7]  311 	xor	a, #0x80
   5023                     312 00119$:
   5023 FA 47 50      [10]  313 	jp	M, 00102$
   5026 79            [ 4]  314 	ld	a, c
   5027 D6 48         [ 7]  315 	sub	a, #0x48
   5029 78            [ 4]  316 	ld	a, b
   502A 17            [ 4]  317 	rla
   502B 3F            [ 4]  318 	ccf
   502C 1F            [ 4]  319 	rra
   502D DE 80         [ 7]  320 	sbc	a, #0x80
   502F 30 16         [12]  321 	jr	NC,00102$
   5031 3E 38         [ 7]  322 	ld	a, #0x38
   5033 DD BE FE      [19]  323 	cp	a, -2 (ix)
   5036 3E 00         [ 7]  324 	ld	a, #0x00
   5038 DD 9E FF      [19]  325 	sbc	a, -1 (ix)
   503B E2 40 50      [10]  326 	jp	PO, 00120$
   503E EE 80         [ 7]  327 	xor	a, #0x80
   5040                     328 00120$:
   5040 F2 47 50      [10]  329 	jp	P, 00102$
                            330 ;src/systems/tilemap.c:63: return 1;
   5043 2E 01         [ 7]  331 	ld	l, #0x01
   5045 18 02         [12]  332 	jr	00105$
   5047                     333 00102$:
                            334 ;src/systems/tilemap.c:65: return 0;
   5047 2E 00         [ 7]  335 	ld	l, #0x00
   5049                     336 00105$:
   5049 DD F9         [10]  337 	ld	sp, ix
   504B DD E1         [14]  338 	pop	ix
   504D C9            [10]  339 	ret
                            340 ;src/systems/tilemap.c:68: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            341 ;	---------------------------------
                            342 ; Function tilemap_is_ladder
                            343 ; ---------------------------------
   504E                     344 _tilemap_is_ladder::
   504E DD E5         [15]  345 	push	ix
   5050 DD 21 00 00   [14]  346 	ld	ix,#0
   5054 DD 39         [15]  347 	add	ix,sp
   5056 F5            [11]  348 	push	af
   5057 F5            [11]  349 	push	af
                            350 ;src/systems/tilemap.c:73: center = x + ((i16)w / 2);
   5058 DD 5E 08      [19]  351 	ld	e, 8 (ix)
   505B 16 00         [ 7]  352 	ld	d, #0x00
   505D 4B            [ 4]  353 	ld	c, e
   505E 42            [ 4]  354 	ld	b, d
   505F CB 7A         [ 8]  355 	bit	7, d
   5061 28 03         [12]  356 	jr	Z,00108$
   5063 4B            [ 4]  357 	ld	c, e
   5064 42            [ 4]  358 	ld	b, d
   5065 03            [ 6]  359 	inc	bc
   5066                     360 00108$:
   5066 CB 28         [ 8]  361 	sra	b
   5068 CB 19         [ 8]  362 	rr	c
   506A DD 6E 04      [19]  363 	ld	l,4 (ix)
   506D DD 66 05      [19]  364 	ld	h,5 (ix)
   5070 09            [11]  365 	add	hl, bc
   5071 DD 75 FE      [19]  366 	ld	-2 (ix), l
   5074 DD 74 FF      [19]  367 	ld	-1 (ix), h
                            368 ;src/systems/tilemap.c:74: top = y;
   5077 DD 4E 06      [19]  369 	ld	c,6 (ix)
   507A DD 46 07      [19]  370 	ld	b,7 (ix)
                            371 ;src/systems/tilemap.c:75: bottom = y + (i16)h;
   507D DD 6E 09      [19]  372 	ld	l, 9 (ix)
   5080 26 00         [ 7]  373 	ld	h, #0x00
   5082 09            [11]  374 	add	hl, bc
   5083 33            [ 6]  375 	inc	sp
   5084 33            [ 6]  376 	inc	sp
   5085 E5            [11]  377 	push	hl
                            378 ;src/systems/tilemap.c:77: if (center >= (i16)gladderx - 1 && center <= (i16)gladderx + 3 &&
   5086 21 37 5F      [10]  379 	ld	hl,#_gladderx + 0
   5089 5E            [ 7]  380 	ld	e, (hl)
   508A 16 00         [ 7]  381 	ld	d, #0x00
   508C 6B            [ 4]  382 	ld	l, e
   508D 62            [ 4]  383 	ld	h, d
   508E 2B            [ 6]  384 	dec	hl
   508F DD 7E FE      [19]  385 	ld	a, -2 (ix)
   5092 95            [ 4]  386 	sub	a, l
   5093 DD 7E FF      [19]  387 	ld	a, -1 (ix)
   5096 9C            [ 4]  388 	sbc	a, h
   5097 E2 9C 50      [10]  389 	jp	PO, 00129$
   509A EE 80         [ 7]  390 	xor	a, #0x80
   509C                     391 00129$:
   509C FA DD 50      [10]  392 	jp	M, 00102$
   509F 13            [ 6]  393 	inc	de
   50A0 13            [ 6]  394 	inc	de
   50A1 13            [ 6]  395 	inc	de
   50A2 6A            [ 4]  396 	ld	l, d
   50A3 7B            [ 4]  397 	ld	a, e
   50A4 DD 96 FE      [19]  398 	sub	a, -2 (ix)
   50A7 7D            [ 4]  399 	ld	a, l
   50A8 DD 9E FF      [19]  400 	sbc	a, -1 (ix)
   50AB E2 B0 50      [10]  401 	jp	PO, 00130$
   50AE EE 80         [ 7]  402 	xor	a, #0x80
   50B0                     403 00130$:
   50B0 FA DD 50      [10]  404 	jp	M, 00102$
                            405 ;src/systems/tilemap.c:78: bottom >= (i16)gtileplatformy && top <= (i16)gtilegroundy) {
   50B3 21 35 5F      [10]  406 	ld	hl,#_gtileplatformy + 0
   50B6 5E            [ 7]  407 	ld	e, (hl)
   50B7 16 00         [ 7]  408 	ld	d, #0x00
   50B9 DD 7E FC      [19]  409 	ld	a, -4 (ix)
   50BC 93            [ 4]  410 	sub	a, e
   50BD DD 7E FD      [19]  411 	ld	a, -3 (ix)
   50C0 9A            [ 4]  412 	sbc	a, d
   50C1 E2 C6 50      [10]  413 	jp	PO, 00131$
   50C4 EE 80         [ 7]  414 	xor	a, #0x80
   50C6                     415 00131$:
   50C6 FA DD 50      [10]  416 	jp	M, 00102$
   50C9 3A 34 5F      [13]  417 	ld	a,(#_gtilegroundy + 0)
   50CC 16 00         [ 7]  418 	ld	d, #0x00
   50CE 91            [ 4]  419 	sub	a, c
   50CF 7A            [ 4]  420 	ld	a, d
   50D0 98            [ 4]  421 	sbc	a, b
   50D1 E2 D6 50      [10]  422 	jp	PO, 00132$
   50D4 EE 80         [ 7]  423 	xor	a, #0x80
   50D6                     424 00132$:
   50D6 FA DD 50      [10]  425 	jp	M, 00102$
                            426 ;src/systems/tilemap.c:79: return 1;
   50D9 2E 01         [ 7]  427 	ld	l, #0x01
   50DB 18 02         [12]  428 	jr	00106$
   50DD                     429 00102$:
                            430 ;src/systems/tilemap.c:81: return 0;
   50DD 2E 00         [ 7]  431 	ld	l, #0x00
   50DF                     432 00106$:
   50DF DD F9         [10]  433 	ld	sp, ix
   50E1 DD E1         [14]  434 	pop	ix
   50E3 C9            [10]  435 	ret
                            436 ;src/systems/tilemap.c:84: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            437 ;	---------------------------------
                            438 ; Function tilemap_is_hidden_zone
                            439 ; ---------------------------------
   50E4                     440 _tilemap_is_hidden_zone::
   50E4 DD E5         [15]  441 	push	ix
   50E6 DD 21 00 00   [14]  442 	ld	ix,#0
   50EA DD 39         [15]  443 	add	ix,sp
   50EC F5            [11]  444 	push	af
                            445 ;src/systems/tilemap.c:90: left = x;
   50ED DD 5E 04      [19]  446 	ld	e,4 (ix)
   50F0 DD 56 05      [19]  447 	ld	d,5 (ix)
                            448 ;src/systems/tilemap.c:91: right = x + (i16)w;
   50F3 DD 6E 08      [19]  449 	ld	l, 8 (ix)
   50F6 26 00         [ 7]  450 	ld	h, #0x00
   50F8 19            [11]  451 	add	hl, de
   50F9 33            [ 6]  452 	inc	sp
   50FA 33            [ 6]  453 	inc	sp
   50FB E5            [11]  454 	push	hl
                            455 ;src/systems/tilemap.c:92: top = y;
   50FC DD 4E 06      [19]  456 	ld	c,6 (ix)
   50FF DD 46 07      [19]  457 	ld	b,7 (ix)
                            458 ;src/systems/tilemap.c:93: bottom = y + (i16)h;
   5102 DD 6E 09      [19]  459 	ld	l, 9 (ix)
   5105 26 00         [ 7]  460 	ld	h, #0x00
   5107 09            [11]  461 	add	hl, bc
                            462 ;src/systems/tilemap.c:95: if (left < 18 && right > 4 && top < 64 && bottom > 52) {
   5108 7B            [ 4]  463 	ld	a, e
   5109 D6 12         [ 7]  464 	sub	a, #0x12
   510B 7A            [ 4]  465 	ld	a, d
   510C 17            [ 4]  466 	rla
   510D 3F            [ 4]  467 	ccf
   510E 1F            [ 4]  468 	rra
   510F DE 80         [ 7]  469 	sbc	a, #0x80
   5111 30 2F         [12]  470 	jr	NC,00102$
   5113 3E 04         [ 7]  471 	ld	a, #0x04
   5115 DD BE FE      [19]  472 	cp	a, -2 (ix)
   5118 3E 00         [ 7]  473 	ld	a, #0x00
   511A DD 9E FF      [19]  474 	sbc	a, -1 (ix)
   511D E2 22 51      [10]  475 	jp	PO, 00124$
   5120 EE 80         [ 7]  476 	xor	a, #0x80
   5122                     477 00124$:
   5122 F2 42 51      [10]  478 	jp	P, 00102$
   5125 79            [ 4]  479 	ld	a, c
   5126 D6 40         [ 7]  480 	sub	a, #0x40
   5128 78            [ 4]  481 	ld	a, b
   5129 17            [ 4]  482 	rla
   512A 3F            [ 4]  483 	ccf
   512B 1F            [ 4]  484 	rra
   512C DE 80         [ 7]  485 	sbc	a, #0x80
   512E 30 12         [12]  486 	jr	NC,00102$
   5130 3E 34         [ 7]  487 	ld	a, #0x34
   5132 BD            [ 4]  488 	cp	a, l
   5133 3E 00         [ 7]  489 	ld	a, #0x00
   5135 9C            [ 4]  490 	sbc	a, h
   5136 E2 3B 51      [10]  491 	jp	PO, 00125$
   5139 EE 80         [ 7]  492 	xor	a, #0x80
   513B                     493 00125$:
   513B F2 42 51      [10]  494 	jp	P, 00102$
                            495 ;src/systems/tilemap.c:96: return 1;
   513E 2E 01         [ 7]  496 	ld	l, #0x01
   5140 18 02         [12]  497 	jr	00106$
   5142                     498 00102$:
                            499 ;src/systems/tilemap.c:98: return 0;
   5142 2E 00         [ 7]  500 	ld	l, #0x00
   5144                     501 00106$:
   5144 DD F9         [10]  502 	ld	sp, ix
   5146 DD E1         [14]  503 	pop	ix
   5148 C9            [10]  504 	ret
                            505 ;src/systems/tilemap.c:101: u8 tilemap_goal_x(void) {
                            506 ;	---------------------------------
                            507 ; Function tilemap_goal_x
                            508 ; ---------------------------------
   5149                     509 _tilemap_goal_x::
                            510 ;src/systems/tilemap.c:102: return ggoalx;
   5149 FD 21 36 5F   [14]  511 	ld	iy, #_ggoalx
   514D FD 6E 00      [19]  512 	ld	l, 0 (iy)
   5150 C9            [10]  513 	ret
                            514 	.area _CODE
                            515 	.area _INITIALIZER
   5F50                     516 __xinit__gtilegroundy:
   5F50 A0                  517 	.db #0xa0	; 160
   5F51                     518 __xinit__gtileplatformy:
   5F51 80                  519 	.db #0x80	; 128
   5F52                     520 __xinit__ggoalx:
   5F52 48                  521 	.db #0x48	; 72	'H'
   5F53                     522 __xinit__gladderx:
   5F53 24                  523 	.db #0x24	; 36
                            524 	.area _CABS (ABS)
