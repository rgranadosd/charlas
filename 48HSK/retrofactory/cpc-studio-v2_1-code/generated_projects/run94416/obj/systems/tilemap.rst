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
   651B                      33 _gtilegroundy:
   651B                      34 	.ds 1
   651C                      35 _gtileplatformy:
   651C                      36 	.ds 1
   651D                      37 _ggoalx:
   651D                      38 	.ds 1
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
   52EF                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   52EF 2A 6A 54      [16]   65 	ld	hl, (_level1tilemapheight)
   52F2 3E 02         [ 7]   66 	ld	a, #0x02
   52F4 BD            [ 4]   67 	cp	a, l
   52F5 3E 00         [ 7]   68 	ld	a, #0x00
   52F7 9C            [ 4]   69 	sbc	a, h
   52F8 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   52FA 7D            [ 4]   72 	ld	a, l
   52FB C6 FE         [ 7]   73 	add	a, #0xfe
   52FD 07            [ 4]   74 	rlca
   52FE 07            [ 4]   75 	rlca
   52FF 07            [ 4]   76 	rlca
   5300 E6 F8         [ 7]   77 	and	a, #0xf8
   5302 32 1B 65      [13]   78 	ld	(#_gtilegroundy + 0),a
   5305 18 05         [12]   79 	jr	00103$
   5307                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5307 21 1B 65      [10]   82 	ld	hl,#_gtilegroundy + 0
   530A 36 A0         [10]   83 	ld	(hl), #0xa0
   530C                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   530C 21 1C 65      [10]   86 	ld	hl, #_gtileplatformy
   530F 3A 1B 65      [13]   87 	ld	a,(#_gtilegroundy + 0)
   5312 C6 E8         [ 7]   88 	add	a, #0xe8
   5314 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5315 21 1D 65      [10]   91 	ld	hl,#_ggoalx + 0
   5318 36 48         [10]   92 	ld	(hl), #0x48
   531A C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   531B                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   531B 3A 1B 65      [13]  100 	ld	a, (_gtilegroundy)
   531E F5            [11]  101 	push	af
   531F 33            [ 6]  102 	inc	sp
   5320 AF            [ 4]  103 	xor	a, a
   5321 F5            [11]  104 	push	af
   5322 33            [ 6]  105 	inc	sp
   5323 21 00 C0      [10]  106 	ld	hl, #0xc000
   5326 E5            [11]  107 	push	hl
   5327 CD 39 64      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   532A E5            [11]  110 	push	hl
   532B 21 01 01      [10]  111 	ld	hl, #0x0101
   532E E5            [11]  112 	push	hl
   532F CD 46 63      [17]  113 	call	_cpct_px2byteM0
   5332 55            [ 4]  114 	ld	d, l
   5333 C1            [10]  115 	pop	bc
   5334 21 50 08      [10]  116 	ld	hl, #0x0850
   5337 E5            [11]  117 	push	hl
   5338 D5            [11]  118 	push	de
   5339 33            [ 6]  119 	inc	sp
   533A C5            [11]  120 	push	bc
   533B CD 80 63      [17]  121 	call	_cpct_drawSolidBox
   533E F1            [10]  122 	pop	af
   533F F1            [10]  123 	pop	af
   5340 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5341 3A 1C 65      [13]  126 	ld	a, (_gtileplatformy)
   5344 57            [ 4]  127 	ld	d,a
   5345 1E 18         [ 7]  128 	ld	e,#0x18
   5347 D5            [11]  129 	push	de
   5348 21 00 C0      [10]  130 	ld	hl, #0xc000
   534B E5            [11]  131 	push	hl
   534C CD 39 64      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   534F E5            [11]  134 	push	hl
   5350 21 02 02      [10]  135 	ld	hl, #0x0202
   5353 E5            [11]  136 	push	hl
   5354 CD 46 63      [17]  137 	call	_cpct_px2byteM0
   5357 55            [ 4]  138 	ld	d, l
   5358 C1            [10]  139 	pop	bc
   5359 21 20 04      [10]  140 	ld	hl, #0x0420
   535C E5            [11]  141 	push	hl
   535D D5            [11]  142 	push	de
   535E 33            [ 6]  143 	inc	sp
   535F C5            [11]  144 	push	bc
   5360 CD 80 63      [17]  145 	call	_cpct_drawSolidBox
   5363 F1            [10]  146 	pop	af
   5364 F1            [10]  147 	pop	af
   5365 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   5366 21 1B 65      [10]  150 	ld	hl,#_gtilegroundy + 0
   5369 46            [ 7]  151 	ld	b, (hl)
   536A 05            [ 4]  152 	dec	b
   536B 05            [ 4]  153 	dec	b
   536C C5            [11]  154 	push	bc
   536D 33            [ 6]  155 	inc	sp
   536E 3E 38         [ 7]  156 	ld	a, #0x38
   5370 F5            [11]  157 	push	af
   5371 33            [ 6]  158 	inc	sp
   5372 21 00 C0      [10]  159 	ld	hl, #0xc000
   5375 E5            [11]  160 	push	hl
   5376 CD 39 64      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   5379 E5            [11]  163 	push	hl
   537A 21 03 03      [10]  164 	ld	hl, #0x0303
   537D E5            [11]  165 	push	hl
   537E CD 46 63      [17]  166 	call	_cpct_px2byteM0
   5381 55            [ 4]  167 	ld	d, l
   5382 C1            [10]  168 	pop	bc
   5383 21 10 02      [10]  169 	ld	hl, #0x0210
   5386 E5            [11]  170 	push	hl
   5387 D5            [11]  171 	push	de
   5388 33            [ 6]  172 	inc	sp
   5389 C5            [11]  173 	push	bc
   538A CD 80 63      [17]  174 	call	_cpct_drawSolidBox
   538D F1            [10]  175 	pop	af
   538E F1            [10]  176 	pop	af
   538F 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   5390 3A 1B 65      [13]  179 	ld	a,(#_gtilegroundy + 0)
   5393 C6 F0         [ 7]  180 	add	a, #0xf0
   5395 47            [ 4]  181 	ld	b, a
   5396 C5            [11]  182 	push	bc
   5397 33            [ 6]  183 	inc	sp
   5398 3A 1D 65      [13]  184 	ld	a, (_ggoalx)
   539B F5            [11]  185 	push	af
   539C 33            [ 6]  186 	inc	sp
   539D 21 00 C0      [10]  187 	ld	hl, #0xc000
   53A0 E5            [11]  188 	push	hl
   53A1 CD 39 64      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   53A4 E5            [11]  191 	push	hl
   53A5 21 05 05      [10]  192 	ld	hl, #0x0505
   53A8 E5            [11]  193 	push	hl
   53A9 CD 46 63      [17]  194 	call	_cpct_px2byteM0
   53AC 55            [ 4]  195 	ld	d, l
   53AD C1            [10]  196 	pop	bc
   53AE 21 02 10      [10]  197 	ld	hl, #0x1002
   53B1 E5            [11]  198 	push	hl
   53B2 D5            [11]  199 	push	de
   53B3 33            [ 6]  200 	inc	sp
   53B4 C5            [11]  201 	push	bc
   53B5 CD 80 63      [17]  202 	call	_cpct_drawSolidBox
   53B8 F1            [10]  203 	pop	af
   53B9 F1            [10]  204 	pop	af
   53BA 33            [ 6]  205 	inc	sp
   53BB C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   53BC                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   53BC FD 21 1B 65   [14]  213 	ld	iy, #_gtilegroundy
   53C0 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   53C3 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   53C4                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   53C4 FD 21 02 00   [14]  222 	ld	iy, #2
   53C8 FD 39         [15]  223 	add	iy, sp
   53CA FD 7E 00      [19]  224 	ld	a, 0 (iy)
   53CD D6 18         [ 7]  225 	sub	a, #0x18
   53CF FD 7E 01      [19]  226 	ld	a, 1 (iy)
   53D2 17            [ 4]  227 	rla
   53D3 3F            [ 4]  228 	ccf
   53D4 1F            [ 4]  229 	rra
   53D5 DE 80         [ 7]  230 	sbc	a, #0x80
   53D7 38 1A         [12]  231 	jr	C,00102$
   53D9 3E 38         [ 7]  232 	ld	a, #0x38
   53DB FD BE 00      [19]  233 	cp	a, 0 (iy)
   53DE 3E 00         [ 7]  234 	ld	a, #0x00
   53E0 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   53E3 E2 E8 53      [10]  236 	jp	PO, 00114$
   53E6 EE 80         [ 7]  237 	xor	a, #0x80
   53E8                     238 00114$:
   53E8 FA F3 53      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   53EB FD 21 1C 65   [14]  241 	ld	iy, #_gtileplatformy
   53EF FD 6E 00      [19]  242 	ld	l, 0 (iy)
   53F2 C9            [10]  243 	ret
   53F3                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   53F3 2E FF         [ 7]  246 	ld	l, #0xff
   53F5 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   53F6                     252 _tilemap_is_trap::
   53F6 DD E5         [15]  253 	push	ix
   53F8 DD 21 00 00   [14]  254 	ld	ix,#0
   53FC DD 39         [15]  255 	add	ix,sp
   53FE F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   53FF DD 4E 04      [19]  258 	ld	c,4 (ix)
   5402 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5405 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5408 26 00         [ 7]  262 	ld	h, #0x00
   540A 09            [11]  263 	add	hl, bc
   540B 33            [ 6]  264 	inc	sp
   540C 33            [ 6]  265 	inc	sp
   540D E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   540E DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5411 16 00         [ 7]  269 	ld	d, #0x00
   5413 DD 6E 06      [19]  270 	ld	l,6 (ix)
   5416 DD 66 07      [19]  271 	ld	h,7 (ix)
   5419 19            [11]  272 	add	hl, de
   541A EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   541B FD 21 1B 65   [14]  275 	ld	iy, #_gtilegroundy
   541F FD 6E 00      [19]  276 	ld	l, 0 (iy)
   5422 26 00         [ 7]  277 	ld	h, #0x00
   5424 2B            [ 6]  278 	dec	hl
   5425 2B            [ 6]  279 	dec	hl
   5426 7B            [ 4]  280 	ld	a, e
   5427 95            [ 4]  281 	sub	a, l
   5428 7A            [ 4]  282 	ld	a, d
   5429 9C            [ 4]  283 	sbc	a, h
   542A E2 2F 54      [10]  284 	jp	PO, 00119$
   542D EE 80         [ 7]  285 	xor	a, #0x80
   542F                     286 00119$:
   542F FA 53 54      [10]  287 	jp	M, 00102$
   5432 79            [ 4]  288 	ld	a, c
   5433 D6 48         [ 7]  289 	sub	a, #0x48
   5435 78            [ 4]  290 	ld	a, b
   5436 17            [ 4]  291 	rla
   5437 3F            [ 4]  292 	ccf
   5438 1F            [ 4]  293 	rra
   5439 DE 80         [ 7]  294 	sbc	a, #0x80
   543B 30 16         [12]  295 	jr	NC,00102$
   543D 3E 38         [ 7]  296 	ld	a, #0x38
   543F DD BE FE      [19]  297 	cp	a, -2 (ix)
   5442 3E 00         [ 7]  298 	ld	a, #0x00
   5444 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5447 E2 4C 54      [10]  300 	jp	PO, 00120$
   544A EE 80         [ 7]  301 	xor	a, #0x80
   544C                     302 00120$:
   544C F2 53 54      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   544F 2E 01         [ 7]  305 	ld	l, #0x01
   5451 18 02         [12]  306 	jr	00105$
   5453                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   5453 2E 00         [ 7]  309 	ld	l, #0x00
   5455                     310 00105$:
   5455 DD F9         [10]  311 	ld	sp, ix
   5457 DD E1         [14]  312 	pop	ix
   5459 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   545A                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   545A 2E 00         [ 7]  320 	ld	l, #0x00
   545C C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   545D                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   545D 2E 00         [ 7]  328 	ld	l, #0x00
   545F C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   5460                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   5460 FD 21 1D 65   [14]  336 	ld	iy, #_ggoalx
   5464 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   5467 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   6522                     341 __xinit__gtilegroundy:
   6522 A0                  342 	.db #0xa0	; 160
   6523                     343 __xinit__gtileplatformy:
   6523 80                  344 	.db #0x80	; 128
   6524                     345 __xinit__ggoalx:
   6524 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
