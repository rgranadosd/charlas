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
                             13 	.globl _cpct_px2byteM0
                             14 	.globl _tilemap_init
                             15 	.globl _tilemap_render
                             16 	.globl _tilemap_ground_y
                             17 	.globl _tilemap_platform_y_at
                             18 	.globl _tilemap_is_trap
                             19 	.globl _tilemap_is_ladder
                             20 	.globl _tilemap_is_hidden_zone
                             21 	.globl _tilemap_goal_x
                             22 ;--------------------------------------------------------
                             23 ; special function registers
                             24 ;--------------------------------------------------------
                             25 ;--------------------------------------------------------
                             26 ; ram data
                             27 ;--------------------------------------------------------
                             28 	.area _DATA
                             29 ;--------------------------------------------------------
                             30 ; ram data
                             31 ;--------------------------------------------------------
                             32 	.area _INITIALIZED
   67B8                      33 _gtilegroundy:
   67B8                      34 	.ds 1
   67B9                      35 _gtileplatformy:
   67B9                      36 	.ds 1
   67BA                      37 _ggoalx:
   67BA                      38 	.ds 1
                             39 ;--------------------------------------------------------
                             40 ; absolute external ram data
                             41 ;--------------------------------------------------------
                             42 	.area _DABS (ABS)
                             43 ;--------------------------------------------------------
                             44 ; global & static initialisations
                             45 ;--------------------------------------------------------
                             46 	.area _HOME
                             47 	.area _GSINIT
                             48 	.area _GSFINAL
                             49 	.area _GSINIT
                             50 ;--------------------------------------------------------
                             51 ; Home
                             52 ;--------------------------------------------------------
                             53 	.area _HOME
                             54 	.area _HOME
                             55 ;--------------------------------------------------------
                             56 ; code
                             57 ;--------------------------------------------------------
                             58 	.area _CODE
                             59 ;src/systems/tilemap.c:9: void tilemap_init(void) {
                             60 ;	---------------------------------
                             61 ; Function tilemap_init
                             62 ; ---------------------------------
   52E0                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   52E0 2A 5B 54      [16]   65 	ld	hl, (_level1tilemapheight)
   52E3 3E 02         [ 7]   66 	ld	a, #0x02
   52E5 BD            [ 4]   67 	cp	a, l
   52E6 3E 00         [ 7]   68 	ld	a, #0x00
   52E8 9C            [ 4]   69 	sbc	a, h
   52E9 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   52EB 7D            [ 4]   72 	ld	a, l
   52EC C6 FE         [ 7]   73 	add	a, #0xfe
   52EE 07            [ 4]   74 	rlca
   52EF 07            [ 4]   75 	rlca
   52F0 07            [ 4]   76 	rlca
   52F1 E6 F8         [ 7]   77 	and	a, #0xf8
   52F3 32 B8 67      [13]   78 	ld	(#_gtilegroundy + 0),a
   52F6 18 05         [12]   79 	jr	00103$
   52F8                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   52F8 21 B8 67      [10]   82 	ld	hl,#_gtilegroundy + 0
   52FB 36 A0         [10]   83 	ld	(hl), #0xa0
   52FD                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   52FD 21 B9 67      [10]   86 	ld	hl, #_gtileplatformy
   5300 3A B8 67      [13]   87 	ld	a,(#_gtilegroundy + 0)
   5303 C6 E8         [ 7]   88 	add	a, #0xe8
   5305 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5306 21 BA 67      [10]   91 	ld	hl,#_ggoalx + 0
   5309 36 48         [10]   92 	ld	(hl), #0x48
   530B C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   530C                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   530C 3A B8 67      [13]  100 	ld	a, (_gtilegroundy)
   530F F5            [11]  101 	push	af
   5310 33            [ 6]  102 	inc	sp
   5311 AF            [ 4]  103 	xor	a, a
   5312 F5            [11]  104 	push	af
   5313 33            [ 6]  105 	inc	sp
   5314 21 00 C0      [10]  106 	ld	hl, #0xc000
   5317 E5            [11]  107 	push	hl
   5318 CD D6 66      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   531B E5            [11]  110 	push	hl
   531C 21 01 01      [10]  111 	ld	hl, #0x0101
   531F E5            [11]  112 	push	hl
   5320 CD E3 65      [17]  113 	call	_cpct_px2byteM0
   5323 55            [ 4]  114 	ld	d, l
   5324 C1            [10]  115 	pop	bc
   5325 21 50 08      [10]  116 	ld	hl, #0x0850
   5328 E5            [11]  117 	push	hl
   5329 D5            [11]  118 	push	de
   532A 33            [ 6]  119 	inc	sp
   532B C5            [11]  120 	push	bc
   532C CD 1D 66      [17]  121 	call	_cpct_drawSolidBox
   532F F1            [10]  122 	pop	af
   5330 F1            [10]  123 	pop	af
   5331 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5332 3A B9 67      [13]  126 	ld	a, (_gtileplatformy)
   5335 57            [ 4]  127 	ld	d,a
   5336 1E 18         [ 7]  128 	ld	e,#0x18
   5338 D5            [11]  129 	push	de
   5339 21 00 C0      [10]  130 	ld	hl, #0xc000
   533C E5            [11]  131 	push	hl
   533D CD D6 66      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   5340 E5            [11]  134 	push	hl
   5341 21 02 02      [10]  135 	ld	hl, #0x0202
   5344 E5            [11]  136 	push	hl
   5345 CD E3 65      [17]  137 	call	_cpct_px2byteM0
   5348 55            [ 4]  138 	ld	d, l
   5349 C1            [10]  139 	pop	bc
   534A 21 20 04      [10]  140 	ld	hl, #0x0420
   534D E5            [11]  141 	push	hl
   534E D5            [11]  142 	push	de
   534F 33            [ 6]  143 	inc	sp
   5350 C5            [11]  144 	push	bc
   5351 CD 1D 66      [17]  145 	call	_cpct_drawSolidBox
   5354 F1            [10]  146 	pop	af
   5355 F1            [10]  147 	pop	af
   5356 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   5357 21 B8 67      [10]  150 	ld	hl,#_gtilegroundy + 0
   535A 46            [ 7]  151 	ld	b, (hl)
   535B 05            [ 4]  152 	dec	b
   535C 05            [ 4]  153 	dec	b
   535D C5            [11]  154 	push	bc
   535E 33            [ 6]  155 	inc	sp
   535F 3E 38         [ 7]  156 	ld	a, #0x38
   5361 F5            [11]  157 	push	af
   5362 33            [ 6]  158 	inc	sp
   5363 21 00 C0      [10]  159 	ld	hl, #0xc000
   5366 E5            [11]  160 	push	hl
   5367 CD D6 66      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   536A E5            [11]  163 	push	hl
   536B 21 03 03      [10]  164 	ld	hl, #0x0303
   536E E5            [11]  165 	push	hl
   536F CD E3 65      [17]  166 	call	_cpct_px2byteM0
   5372 55            [ 4]  167 	ld	d, l
   5373 C1            [10]  168 	pop	bc
   5374 21 10 02      [10]  169 	ld	hl, #0x0210
   5377 E5            [11]  170 	push	hl
   5378 D5            [11]  171 	push	de
   5379 33            [ 6]  172 	inc	sp
   537A C5            [11]  173 	push	bc
   537B CD 1D 66      [17]  174 	call	_cpct_drawSolidBox
   537E F1            [10]  175 	pop	af
   537F F1            [10]  176 	pop	af
   5380 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   5381 3A B8 67      [13]  179 	ld	a,(#_gtilegroundy + 0)
   5384 C6 F0         [ 7]  180 	add	a, #0xf0
   5386 47            [ 4]  181 	ld	b, a
   5387 C5            [11]  182 	push	bc
   5388 33            [ 6]  183 	inc	sp
   5389 3A BA 67      [13]  184 	ld	a, (_ggoalx)
   538C F5            [11]  185 	push	af
   538D 33            [ 6]  186 	inc	sp
   538E 21 00 C0      [10]  187 	ld	hl, #0xc000
   5391 E5            [11]  188 	push	hl
   5392 CD D6 66      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   5395 E5            [11]  191 	push	hl
   5396 21 05 05      [10]  192 	ld	hl, #0x0505
   5399 E5            [11]  193 	push	hl
   539A CD E3 65      [17]  194 	call	_cpct_px2byteM0
   539D 55            [ 4]  195 	ld	d, l
   539E C1            [10]  196 	pop	bc
   539F 21 02 10      [10]  197 	ld	hl, #0x1002
   53A2 E5            [11]  198 	push	hl
   53A3 D5            [11]  199 	push	de
   53A4 33            [ 6]  200 	inc	sp
   53A5 C5            [11]  201 	push	bc
   53A6 CD 1D 66      [17]  202 	call	_cpct_drawSolidBox
   53A9 F1            [10]  203 	pop	af
   53AA F1            [10]  204 	pop	af
   53AB 33            [ 6]  205 	inc	sp
   53AC C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   53AD                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   53AD FD 21 B8 67   [14]  213 	ld	iy, #_gtilegroundy
   53B1 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   53B4 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   53B5                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   53B5 FD 21 02 00   [14]  222 	ld	iy, #2
   53B9 FD 39         [15]  223 	add	iy, sp
   53BB FD 7E 00      [19]  224 	ld	a, 0 (iy)
   53BE D6 18         [ 7]  225 	sub	a, #0x18
   53C0 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   53C3 17            [ 4]  227 	rla
   53C4 3F            [ 4]  228 	ccf
   53C5 1F            [ 4]  229 	rra
   53C6 DE 80         [ 7]  230 	sbc	a, #0x80
   53C8 38 1A         [12]  231 	jr	C,00102$
   53CA 3E 38         [ 7]  232 	ld	a, #0x38
   53CC FD BE 00      [19]  233 	cp	a, 0 (iy)
   53CF 3E 00         [ 7]  234 	ld	a, #0x00
   53D1 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   53D4 E2 D9 53      [10]  236 	jp	PO, 00114$
   53D7 EE 80         [ 7]  237 	xor	a, #0x80
   53D9                     238 00114$:
   53D9 FA E4 53      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   53DC FD 21 B9 67   [14]  241 	ld	iy, #_gtileplatformy
   53E0 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   53E3 C9            [10]  243 	ret
   53E4                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   53E4 2E FF         [ 7]  246 	ld	l, #0xff
   53E6 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   53E7                     252 _tilemap_is_trap::
   53E7 DD E5         [15]  253 	push	ix
   53E9 DD 21 00 00   [14]  254 	ld	ix,#0
   53ED DD 39         [15]  255 	add	ix,sp
   53EF F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   53F0 DD 4E 04      [19]  258 	ld	c,4 (ix)
   53F3 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   53F6 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   53F9 26 00         [ 7]  262 	ld	h, #0x00
   53FB 09            [11]  263 	add	hl, bc
   53FC 33            [ 6]  264 	inc	sp
   53FD 33            [ 6]  265 	inc	sp
   53FE E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   53FF DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5402 16 00         [ 7]  269 	ld	d, #0x00
   5404 DD 6E 06      [19]  270 	ld	l,6 (ix)
   5407 DD 66 07      [19]  271 	ld	h,7 (ix)
   540A 19            [11]  272 	add	hl, de
   540B EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   540C FD 21 B8 67   [14]  275 	ld	iy, #_gtilegroundy
   5410 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   5413 26 00         [ 7]  277 	ld	h, #0x00
   5415 2B            [ 6]  278 	dec	hl
   5416 2B            [ 6]  279 	dec	hl
   5417 7B            [ 4]  280 	ld	a, e
   5418 95            [ 4]  281 	sub	a, l
   5419 7A            [ 4]  282 	ld	a, d
   541A 9C            [ 4]  283 	sbc	a, h
   541B E2 20 54      [10]  284 	jp	PO, 00119$
   541E EE 80         [ 7]  285 	xor	a, #0x80
   5420                     286 00119$:
   5420 FA 44 54      [10]  287 	jp	M, 00102$
   5423 79            [ 4]  288 	ld	a, c
   5424 D6 48         [ 7]  289 	sub	a, #0x48
   5426 78            [ 4]  290 	ld	a, b
   5427 17            [ 4]  291 	rla
   5428 3F            [ 4]  292 	ccf
   5429 1F            [ 4]  293 	rra
   542A DE 80         [ 7]  294 	sbc	a, #0x80
   542C 30 16         [12]  295 	jr	NC,00102$
   542E 3E 38         [ 7]  296 	ld	a, #0x38
   5430 DD BE FE      [19]  297 	cp	a, -2 (ix)
   5433 3E 00         [ 7]  298 	ld	a, #0x00
   5435 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5438 E2 3D 54      [10]  300 	jp	PO, 00120$
   543B EE 80         [ 7]  301 	xor	a, #0x80
   543D                     302 00120$:
   543D F2 44 54      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   5440 2E 01         [ 7]  305 	ld	l, #0x01
   5442 18 02         [12]  306 	jr	00105$
   5444                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   5444 2E 00         [ 7]  309 	ld	l, #0x00
   5446                     310 00105$:
   5446 DD F9         [10]  311 	ld	sp, ix
   5448 DD E1         [14]  312 	pop	ix
   544A C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   544B                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   544B 2E 00         [ 7]  320 	ld	l, #0x00
   544D C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   544E                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   544E 2E 00         [ 7]  328 	ld	l, #0x00
   5450 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   5451                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   5451 FD 21 BA 67   [14]  336 	ld	iy, #_ggoalx
   5455 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   5458 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   67BF                     341 __xinit__gtilegroundy:
   67BF A0                  342 	.db #0xa0	; 160
   67C0                     343 __xinit__gtileplatformy:
   67C0 80                  344 	.db #0x80	; 128
   67C1                     345 __xinit__ggoalx:
   67C1 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
