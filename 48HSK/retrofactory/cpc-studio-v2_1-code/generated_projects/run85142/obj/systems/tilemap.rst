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
   6687                      33 _gtilegroundy:
   6687                      34 	.ds 1
   6688                      35 _gtileplatformy:
   6688                      36 	.ds 1
   6689                      37 _ggoalx:
   6689                      38 	.ds 1
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
   52DE                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   52DE 2A 59 54      [16]   65 	ld	hl, (_level1tilemapheight)
   52E1 3E 02         [ 7]   66 	ld	a, #0x02
   52E3 BD            [ 4]   67 	cp	a, l
   52E4 3E 00         [ 7]   68 	ld	a, #0x00
   52E6 9C            [ 4]   69 	sbc	a, h
   52E7 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   52E9 7D            [ 4]   72 	ld	a, l
   52EA C6 FE         [ 7]   73 	add	a, #0xfe
   52EC 07            [ 4]   74 	rlca
   52ED 07            [ 4]   75 	rlca
   52EE 07            [ 4]   76 	rlca
   52EF E6 F8         [ 7]   77 	and	a, #0xf8
   52F1 32 87 66      [13]   78 	ld	(#_gtilegroundy + 0),a
   52F4 18 05         [12]   79 	jr	00103$
   52F6                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   52F6 21 87 66      [10]   82 	ld	hl,#_gtilegroundy + 0
   52F9 36 A0         [10]   83 	ld	(hl), #0xa0
   52FB                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   52FB 21 88 66      [10]   86 	ld	hl, #_gtileplatformy
   52FE 3A 87 66      [13]   87 	ld	a,(#_gtilegroundy + 0)
   5301 C6 E8         [ 7]   88 	add	a, #0xe8
   5303 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5304 21 89 66      [10]   91 	ld	hl,#_ggoalx + 0
   5307 36 48         [10]   92 	ld	(hl), #0x48
   5309 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   530A                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   530A 3A 87 66      [13]  100 	ld	a, (_gtilegroundy)
   530D F5            [11]  101 	push	af
   530E 33            [ 6]  102 	inc	sp
   530F AF            [ 4]  103 	xor	a, a
   5310 F5            [11]  104 	push	af
   5311 33            [ 6]  105 	inc	sp
   5312 21 00 C0      [10]  106 	ld	hl, #0xc000
   5315 E5            [11]  107 	push	hl
   5316 CD A5 65      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5319 E5            [11]  110 	push	hl
   531A 21 01 01      [10]  111 	ld	hl, #0x0101
   531D E5            [11]  112 	push	hl
   531E CD B2 64      [17]  113 	call	_cpct_px2byteM0
   5321 55            [ 4]  114 	ld	d, l
   5322 C1            [10]  115 	pop	bc
   5323 21 50 08      [10]  116 	ld	hl, #0x0850
   5326 E5            [11]  117 	push	hl
   5327 D5            [11]  118 	push	de
   5328 33            [ 6]  119 	inc	sp
   5329 C5            [11]  120 	push	bc
   532A CD EC 64      [17]  121 	call	_cpct_drawSolidBox
   532D F1            [10]  122 	pop	af
   532E F1            [10]  123 	pop	af
   532F 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5330 3A 88 66      [13]  126 	ld	a, (_gtileplatformy)
   5333 57            [ 4]  127 	ld	d,a
   5334 1E 18         [ 7]  128 	ld	e,#0x18
   5336 D5            [11]  129 	push	de
   5337 21 00 C0      [10]  130 	ld	hl, #0xc000
   533A E5            [11]  131 	push	hl
   533B CD A5 65      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   533E E5            [11]  134 	push	hl
   533F 21 02 02      [10]  135 	ld	hl, #0x0202
   5342 E5            [11]  136 	push	hl
   5343 CD B2 64      [17]  137 	call	_cpct_px2byteM0
   5346 55            [ 4]  138 	ld	d, l
   5347 C1            [10]  139 	pop	bc
   5348 21 20 04      [10]  140 	ld	hl, #0x0420
   534B E5            [11]  141 	push	hl
   534C D5            [11]  142 	push	de
   534D 33            [ 6]  143 	inc	sp
   534E C5            [11]  144 	push	bc
   534F CD EC 64      [17]  145 	call	_cpct_drawSolidBox
   5352 F1            [10]  146 	pop	af
   5353 F1            [10]  147 	pop	af
   5354 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   5355 21 87 66      [10]  150 	ld	hl,#_gtilegroundy + 0
   5358 46            [ 7]  151 	ld	b, (hl)
   5359 05            [ 4]  152 	dec	b
   535A 05            [ 4]  153 	dec	b
   535B C5            [11]  154 	push	bc
   535C 33            [ 6]  155 	inc	sp
   535D 3E 38         [ 7]  156 	ld	a, #0x38
   535F F5            [11]  157 	push	af
   5360 33            [ 6]  158 	inc	sp
   5361 21 00 C0      [10]  159 	ld	hl, #0xc000
   5364 E5            [11]  160 	push	hl
   5365 CD A5 65      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   5368 E5            [11]  163 	push	hl
   5369 21 03 03      [10]  164 	ld	hl, #0x0303
   536C E5            [11]  165 	push	hl
   536D CD B2 64      [17]  166 	call	_cpct_px2byteM0
   5370 55            [ 4]  167 	ld	d, l
   5371 C1            [10]  168 	pop	bc
   5372 21 10 02      [10]  169 	ld	hl, #0x0210
   5375 E5            [11]  170 	push	hl
   5376 D5            [11]  171 	push	de
   5377 33            [ 6]  172 	inc	sp
   5378 C5            [11]  173 	push	bc
   5379 CD EC 64      [17]  174 	call	_cpct_drawSolidBox
   537C F1            [10]  175 	pop	af
   537D F1            [10]  176 	pop	af
   537E 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   537F 3A 87 66      [13]  179 	ld	a,(#_gtilegroundy + 0)
   5382 C6 F0         [ 7]  180 	add	a, #0xf0
   5384 47            [ 4]  181 	ld	b, a
   5385 C5            [11]  182 	push	bc
   5386 33            [ 6]  183 	inc	sp
   5387 3A 89 66      [13]  184 	ld	a, (_ggoalx)
   538A F5            [11]  185 	push	af
   538B 33            [ 6]  186 	inc	sp
   538C 21 00 C0      [10]  187 	ld	hl, #0xc000
   538F E5            [11]  188 	push	hl
   5390 CD A5 65      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   5393 E5            [11]  191 	push	hl
   5394 21 05 05      [10]  192 	ld	hl, #0x0505
   5397 E5            [11]  193 	push	hl
   5398 CD B2 64      [17]  194 	call	_cpct_px2byteM0
   539B 55            [ 4]  195 	ld	d, l
   539C C1            [10]  196 	pop	bc
   539D 21 02 10      [10]  197 	ld	hl, #0x1002
   53A0 E5            [11]  198 	push	hl
   53A1 D5            [11]  199 	push	de
   53A2 33            [ 6]  200 	inc	sp
   53A3 C5            [11]  201 	push	bc
   53A4 CD EC 64      [17]  202 	call	_cpct_drawSolidBox
   53A7 F1            [10]  203 	pop	af
   53A8 F1            [10]  204 	pop	af
   53A9 33            [ 6]  205 	inc	sp
   53AA C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   53AB                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   53AB FD 21 87 66   [14]  213 	ld	iy, #_gtilegroundy
   53AF FD 6E 00      [19]  214 	ld	l, 0 (iy)
   53B2 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   53B3                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   53B3 FD 21 02 00   [14]  222 	ld	iy, #2
   53B7 FD 39         [15]  223 	add	iy, sp
   53B9 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   53BC D6 18         [ 7]  225 	sub	a, #0x18
   53BE FD 7E 01      [19]  226 	ld	a, 1 (iy)
   53C1 17            [ 4]  227 	rla
   53C2 3F            [ 4]  228 	ccf
   53C3 1F            [ 4]  229 	rra
   53C4 DE 80         [ 7]  230 	sbc	a, #0x80
   53C6 38 1A         [12]  231 	jr	C,00102$
   53C8 3E 38         [ 7]  232 	ld	a, #0x38
   53CA FD BE 00      [19]  233 	cp	a, 0 (iy)
   53CD 3E 00         [ 7]  234 	ld	a, #0x00
   53CF FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   53D2 E2 D7 53      [10]  236 	jp	PO, 00114$
   53D5 EE 80         [ 7]  237 	xor	a, #0x80
   53D7                     238 00114$:
   53D7 FA E2 53      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   53DA FD 21 88 66   [14]  241 	ld	iy, #_gtileplatformy
   53DE FD 6E 00      [19]  242 	ld	l, 0 (iy)
   53E1 C9            [10]  243 	ret
   53E2                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   53E2 2E FF         [ 7]  246 	ld	l, #0xff
   53E4 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   53E5                     252 _tilemap_is_trap::
   53E5 DD E5         [15]  253 	push	ix
   53E7 DD 21 00 00   [14]  254 	ld	ix,#0
   53EB DD 39         [15]  255 	add	ix,sp
   53ED F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   53EE DD 4E 04      [19]  258 	ld	c,4 (ix)
   53F1 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   53F4 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   53F7 26 00         [ 7]  262 	ld	h, #0x00
   53F9 09            [11]  263 	add	hl, bc
   53FA 33            [ 6]  264 	inc	sp
   53FB 33            [ 6]  265 	inc	sp
   53FC E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   53FD DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5400 16 00         [ 7]  269 	ld	d, #0x00
   5402 DD 6E 06      [19]  270 	ld	l,6 (ix)
   5405 DD 66 07      [19]  271 	ld	h,7 (ix)
   5408 19            [11]  272 	add	hl, de
   5409 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   540A FD 21 87 66   [14]  275 	ld	iy, #_gtilegroundy
   540E FD 6E 00      [19]  276 	ld	l, 0 (iy)
   5411 26 00         [ 7]  277 	ld	h, #0x00
   5413 2B            [ 6]  278 	dec	hl
   5414 2B            [ 6]  279 	dec	hl
   5415 7B            [ 4]  280 	ld	a, e
   5416 95            [ 4]  281 	sub	a, l
   5417 7A            [ 4]  282 	ld	a, d
   5418 9C            [ 4]  283 	sbc	a, h
   5419 E2 1E 54      [10]  284 	jp	PO, 00119$
   541C EE 80         [ 7]  285 	xor	a, #0x80
   541E                     286 00119$:
   541E FA 42 54      [10]  287 	jp	M, 00102$
   5421 79            [ 4]  288 	ld	a, c
   5422 D6 48         [ 7]  289 	sub	a, #0x48
   5424 78            [ 4]  290 	ld	a, b
   5425 17            [ 4]  291 	rla
   5426 3F            [ 4]  292 	ccf
   5427 1F            [ 4]  293 	rra
   5428 DE 80         [ 7]  294 	sbc	a, #0x80
   542A 30 16         [12]  295 	jr	NC,00102$
   542C 3E 38         [ 7]  296 	ld	a, #0x38
   542E DD BE FE      [19]  297 	cp	a, -2 (ix)
   5431 3E 00         [ 7]  298 	ld	a, #0x00
   5433 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5436 E2 3B 54      [10]  300 	jp	PO, 00120$
   5439 EE 80         [ 7]  301 	xor	a, #0x80
   543B                     302 00120$:
   543B F2 42 54      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   543E 2E 01         [ 7]  305 	ld	l, #0x01
   5440 18 02         [12]  306 	jr	00105$
   5442                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   5442 2E 00         [ 7]  309 	ld	l, #0x00
   5444                     310 00105$:
   5444 DD F9         [10]  311 	ld	sp, ix
   5446 DD E1         [14]  312 	pop	ix
   5448 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   5449                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   5449 2E 00         [ 7]  320 	ld	l, #0x00
   544B C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   544C                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   544C 2E 00         [ 7]  328 	ld	l, #0x00
   544E C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   544F                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   544F FD 21 89 66   [14]  336 	ld	iy, #_ggoalx
   5453 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   5456 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   668E                     341 __xinit__gtilegroundy:
   668E A0                  342 	.db #0xa0	; 160
   668F                     343 __xinit__gtileplatformy:
   668F 80                  344 	.db #0x80	; 128
   6690                     345 __xinit__ggoalx:
   6690 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
