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
   6487                      33 _gtilegroundy:
   6487                      34 	.ds 1
   6488                      35 _gtileplatformy:
   6488                      36 	.ds 1
   6489                      37 _ggoalx:
   6489                      38 	.ds 1
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
   5274                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   5274 2A EF 53      [16]   65 	ld	hl, (_level1tilemapheight)
   5277 3E 02         [ 7]   66 	ld	a, #0x02
   5279 BD            [ 4]   67 	cp	a, l
   527A 3E 00         [ 7]   68 	ld	a, #0x00
   527C 9C            [ 4]   69 	sbc	a, h
   527D 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   527F 7D            [ 4]   72 	ld	a, l
   5280 C6 FE         [ 7]   73 	add	a, #0xfe
   5282 07            [ 4]   74 	rlca
   5283 07            [ 4]   75 	rlca
   5284 07            [ 4]   76 	rlca
   5285 E6 F8         [ 7]   77 	and	a, #0xf8
   5287 32 87 64      [13]   78 	ld	(#_gtilegroundy + 0),a
   528A 18 05         [12]   79 	jr	00103$
   528C                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   528C 21 87 64      [10]   82 	ld	hl,#_gtilegroundy + 0
   528F 36 A0         [10]   83 	ld	(hl), #0xa0
   5291                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5291 21 88 64      [10]   86 	ld	hl, #_gtileplatformy
   5294 3A 87 64      [13]   87 	ld	a,(#_gtilegroundy + 0)
   5297 C6 E8         [ 7]   88 	add	a, #0xe8
   5299 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   529A 21 89 64      [10]   91 	ld	hl,#_ggoalx + 0
   529D 36 48         [10]   92 	ld	(hl), #0x48
   529F C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   52A0                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   52A0 3A 87 64      [13]  100 	ld	a, (_gtilegroundy)
   52A3 F5            [11]  101 	push	af
   52A4 33            [ 6]  102 	inc	sp
   52A5 AF            [ 4]  103 	xor	a, a
   52A6 F5            [11]  104 	push	af
   52A7 33            [ 6]  105 	inc	sp
   52A8 21 00 C0      [10]  106 	ld	hl, #0xc000
   52AB E5            [11]  107 	push	hl
   52AC CD A5 63      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   52AF E5            [11]  110 	push	hl
   52B0 21 01 01      [10]  111 	ld	hl, #0x0101
   52B3 E5            [11]  112 	push	hl
   52B4 CD B2 62      [17]  113 	call	_cpct_px2byteM0
   52B7 55            [ 4]  114 	ld	d, l
   52B8 C1            [10]  115 	pop	bc
   52B9 21 50 08      [10]  116 	ld	hl, #0x0850
   52BC E5            [11]  117 	push	hl
   52BD D5            [11]  118 	push	de
   52BE 33            [ 6]  119 	inc	sp
   52BF C5            [11]  120 	push	bc
   52C0 CD EC 62      [17]  121 	call	_cpct_drawSolidBox
   52C3 F1            [10]  122 	pop	af
   52C4 F1            [10]  123 	pop	af
   52C5 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   52C6 3A 88 64      [13]  126 	ld	a, (_gtileplatformy)
   52C9 57            [ 4]  127 	ld	d,a
   52CA 1E 18         [ 7]  128 	ld	e,#0x18
   52CC D5            [11]  129 	push	de
   52CD 21 00 C0      [10]  130 	ld	hl, #0xc000
   52D0 E5            [11]  131 	push	hl
   52D1 CD A5 63      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   52D4 E5            [11]  134 	push	hl
   52D5 21 02 02      [10]  135 	ld	hl, #0x0202
   52D8 E5            [11]  136 	push	hl
   52D9 CD B2 62      [17]  137 	call	_cpct_px2byteM0
   52DC 55            [ 4]  138 	ld	d, l
   52DD C1            [10]  139 	pop	bc
   52DE 21 20 04      [10]  140 	ld	hl, #0x0420
   52E1 E5            [11]  141 	push	hl
   52E2 D5            [11]  142 	push	de
   52E3 33            [ 6]  143 	inc	sp
   52E4 C5            [11]  144 	push	bc
   52E5 CD EC 62      [17]  145 	call	_cpct_drawSolidBox
   52E8 F1            [10]  146 	pop	af
   52E9 F1            [10]  147 	pop	af
   52EA 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   52EB 21 87 64      [10]  150 	ld	hl,#_gtilegroundy + 0
   52EE 46            [ 7]  151 	ld	b, (hl)
   52EF 05            [ 4]  152 	dec	b
   52F0 05            [ 4]  153 	dec	b
   52F1 C5            [11]  154 	push	bc
   52F2 33            [ 6]  155 	inc	sp
   52F3 3E 38         [ 7]  156 	ld	a, #0x38
   52F5 F5            [11]  157 	push	af
   52F6 33            [ 6]  158 	inc	sp
   52F7 21 00 C0      [10]  159 	ld	hl, #0xc000
   52FA E5            [11]  160 	push	hl
   52FB CD A5 63      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   52FE E5            [11]  163 	push	hl
   52FF 21 03 03      [10]  164 	ld	hl, #0x0303
   5302 E5            [11]  165 	push	hl
   5303 CD B2 62      [17]  166 	call	_cpct_px2byteM0
   5306 55            [ 4]  167 	ld	d, l
   5307 C1            [10]  168 	pop	bc
   5308 21 10 02      [10]  169 	ld	hl, #0x0210
   530B E5            [11]  170 	push	hl
   530C D5            [11]  171 	push	de
   530D 33            [ 6]  172 	inc	sp
   530E C5            [11]  173 	push	bc
   530F CD EC 62      [17]  174 	call	_cpct_drawSolidBox
   5312 F1            [10]  175 	pop	af
   5313 F1            [10]  176 	pop	af
   5314 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   5315 3A 87 64      [13]  179 	ld	a,(#_gtilegroundy + 0)
   5318 C6 F0         [ 7]  180 	add	a, #0xf0
   531A 47            [ 4]  181 	ld	b, a
   531B C5            [11]  182 	push	bc
   531C 33            [ 6]  183 	inc	sp
   531D 3A 89 64      [13]  184 	ld	a, (_ggoalx)
   5320 F5            [11]  185 	push	af
   5321 33            [ 6]  186 	inc	sp
   5322 21 00 C0      [10]  187 	ld	hl, #0xc000
   5325 E5            [11]  188 	push	hl
   5326 CD A5 63      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   5329 E5            [11]  191 	push	hl
   532A 21 05 05      [10]  192 	ld	hl, #0x0505
   532D E5            [11]  193 	push	hl
   532E CD B2 62      [17]  194 	call	_cpct_px2byteM0
   5331 55            [ 4]  195 	ld	d, l
   5332 C1            [10]  196 	pop	bc
   5333 21 02 10      [10]  197 	ld	hl, #0x1002
   5336 E5            [11]  198 	push	hl
   5337 D5            [11]  199 	push	de
   5338 33            [ 6]  200 	inc	sp
   5339 C5            [11]  201 	push	bc
   533A CD EC 62      [17]  202 	call	_cpct_drawSolidBox
   533D F1            [10]  203 	pop	af
   533E F1            [10]  204 	pop	af
   533F 33            [ 6]  205 	inc	sp
   5340 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5341                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5341 FD 21 87 64   [14]  213 	ld	iy, #_gtilegroundy
   5345 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   5348 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   5349                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   5349 FD 21 02 00   [14]  222 	ld	iy, #2
   534D FD 39         [15]  223 	add	iy, sp
   534F FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5352 D6 18         [ 7]  225 	sub	a, #0x18
   5354 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   5357 17            [ 4]  227 	rla
   5358 3F            [ 4]  228 	ccf
   5359 1F            [ 4]  229 	rra
   535A DE 80         [ 7]  230 	sbc	a, #0x80
   535C 38 1A         [12]  231 	jr	C,00102$
   535E 3E 38         [ 7]  232 	ld	a, #0x38
   5360 FD BE 00      [19]  233 	cp	a, 0 (iy)
   5363 3E 00         [ 7]  234 	ld	a, #0x00
   5365 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   5368 E2 6D 53      [10]  236 	jp	PO, 00114$
   536B EE 80         [ 7]  237 	xor	a, #0x80
   536D                     238 00114$:
   536D FA 78 53      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5370 FD 21 88 64   [14]  241 	ld	iy, #_gtileplatformy
   5374 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   5377 C9            [10]  243 	ret
   5378                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   5378 2E FF         [ 7]  246 	ld	l, #0xff
   537A C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   537B                     252 _tilemap_is_trap::
   537B DD E5         [15]  253 	push	ix
   537D DD 21 00 00   [14]  254 	ld	ix,#0
   5381 DD 39         [15]  255 	add	ix,sp
   5383 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   5384 DD 4E 04      [19]  258 	ld	c,4 (ix)
   5387 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   538A DD 6E 08      [19]  261 	ld	l, 8 (ix)
   538D 26 00         [ 7]  262 	ld	h, #0x00
   538F 09            [11]  263 	add	hl, bc
   5390 33            [ 6]  264 	inc	sp
   5391 33            [ 6]  265 	inc	sp
   5392 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5393 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5396 16 00         [ 7]  269 	ld	d, #0x00
   5398 DD 6E 06      [19]  270 	ld	l,6 (ix)
   539B DD 66 07      [19]  271 	ld	h,7 (ix)
   539E 19            [11]  272 	add	hl, de
   539F EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   53A0 FD 21 87 64   [14]  275 	ld	iy, #_gtilegroundy
   53A4 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   53A7 26 00         [ 7]  277 	ld	h, #0x00
   53A9 2B            [ 6]  278 	dec	hl
   53AA 2B            [ 6]  279 	dec	hl
   53AB 7B            [ 4]  280 	ld	a, e
   53AC 95            [ 4]  281 	sub	a, l
   53AD 7A            [ 4]  282 	ld	a, d
   53AE 9C            [ 4]  283 	sbc	a, h
   53AF E2 B4 53      [10]  284 	jp	PO, 00119$
   53B2 EE 80         [ 7]  285 	xor	a, #0x80
   53B4                     286 00119$:
   53B4 FA D8 53      [10]  287 	jp	M, 00102$
   53B7 79            [ 4]  288 	ld	a, c
   53B8 D6 48         [ 7]  289 	sub	a, #0x48
   53BA 78            [ 4]  290 	ld	a, b
   53BB 17            [ 4]  291 	rla
   53BC 3F            [ 4]  292 	ccf
   53BD 1F            [ 4]  293 	rra
   53BE DE 80         [ 7]  294 	sbc	a, #0x80
   53C0 30 16         [12]  295 	jr	NC,00102$
   53C2 3E 38         [ 7]  296 	ld	a, #0x38
   53C4 DD BE FE      [19]  297 	cp	a, -2 (ix)
   53C7 3E 00         [ 7]  298 	ld	a, #0x00
   53C9 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   53CC E2 D1 53      [10]  300 	jp	PO, 00120$
   53CF EE 80         [ 7]  301 	xor	a, #0x80
   53D1                     302 00120$:
   53D1 F2 D8 53      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   53D4 2E 01         [ 7]  305 	ld	l, #0x01
   53D6 18 02         [12]  306 	jr	00105$
   53D8                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   53D8 2E 00         [ 7]  309 	ld	l, #0x00
   53DA                     310 00105$:
   53DA DD F9         [10]  311 	ld	sp, ix
   53DC DD E1         [14]  312 	pop	ix
   53DE C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   53DF                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   53DF 2E 00         [ 7]  320 	ld	l, #0x00
   53E1 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   53E2                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   53E2 2E 00         [ 7]  328 	ld	l, #0x00
   53E4 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   53E5                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   53E5 FD 21 89 64   [14]  336 	ld	iy, #_ggoalx
   53E9 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   53EC C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   648E                     341 __xinit__gtilegroundy:
   648E A0                  342 	.db #0xa0	; 160
   648F                     343 __xinit__gtileplatformy:
   648F 80                  344 	.db #0x80	; 128
   6490                     345 __xinit__ggoalx:
   6490 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
