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
   680F                      33 _gtilegroundy:
   680F                      34 	.ds 1
   6810                      35 _gtileplatformy:
   6810                      36 	.ds 1
   6811                      37 _ggoalx:
   6811                      38 	.ds 1
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
   515A                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   515A 2A D5 52      [16]   65 	ld	hl, (_level1tilemapheight)
   515D 3E 02         [ 7]   66 	ld	a, #0x02
   515F BD            [ 4]   67 	cp	a, l
   5160 3E 00         [ 7]   68 	ld	a, #0x00
   5162 9C            [ 4]   69 	sbc	a, h
   5163 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5165 7D            [ 4]   72 	ld	a, l
   5166 C6 FE         [ 7]   73 	add	a, #0xfe
   5168 07            [ 4]   74 	rlca
   5169 07            [ 4]   75 	rlca
   516A 07            [ 4]   76 	rlca
   516B E6 F8         [ 7]   77 	and	a, #0xf8
   516D 32 0F 68      [13]   78 	ld	(#_gtilegroundy + 0),a
   5170 18 05         [12]   79 	jr	00103$
   5172                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5172 21 0F 68      [10]   82 	ld	hl,#_gtilegroundy + 0
   5175 36 A0         [10]   83 	ld	(hl), #0xa0
   5177                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5177 21 10 68      [10]   86 	ld	hl, #_gtileplatformy
   517A 3A 0F 68      [13]   87 	ld	a,(#_gtilegroundy + 0)
   517D C6 E8         [ 7]   88 	add	a, #0xe8
   517F 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5180 21 11 68      [10]   91 	ld	hl,#_ggoalx + 0
   5183 36 48         [10]   92 	ld	(hl), #0x48
   5185 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5186                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5186 3A 0F 68      [13]  100 	ld	a, (_gtilegroundy)
   5189 F5            [11]  101 	push	af
   518A 33            [ 6]  102 	inc	sp
   518B AF            [ 4]  103 	xor	a, a
   518C F5            [11]  104 	push	af
   518D 33            [ 6]  105 	inc	sp
   518E 21 00 C0      [10]  106 	ld	hl, #0xc000
   5191 E5            [11]  107 	push	hl
   5192 CD 2D 67      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5195 E5            [11]  110 	push	hl
   5196 21 01 01      [10]  111 	ld	hl, #0x0101
   5199 E5            [11]  112 	push	hl
   519A CD 3A 66      [17]  113 	call	_cpct_px2byteM0
   519D 55            [ 4]  114 	ld	d, l
   519E C1            [10]  115 	pop	bc
   519F 21 50 08      [10]  116 	ld	hl, #0x0850
   51A2 E5            [11]  117 	push	hl
   51A3 D5            [11]  118 	push	de
   51A4 33            [ 6]  119 	inc	sp
   51A5 C5            [11]  120 	push	bc
   51A6 CD 74 66      [17]  121 	call	_cpct_drawSolidBox
   51A9 F1            [10]  122 	pop	af
   51AA F1            [10]  123 	pop	af
   51AB 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   51AC 3A 10 68      [13]  126 	ld	a, (_gtileplatformy)
   51AF 57            [ 4]  127 	ld	d,a
   51B0 1E 18         [ 7]  128 	ld	e,#0x18
   51B2 D5            [11]  129 	push	de
   51B3 21 00 C0      [10]  130 	ld	hl, #0xc000
   51B6 E5            [11]  131 	push	hl
   51B7 CD 2D 67      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   51BA E5            [11]  134 	push	hl
   51BB 21 02 02      [10]  135 	ld	hl, #0x0202
   51BE E5            [11]  136 	push	hl
   51BF CD 3A 66      [17]  137 	call	_cpct_px2byteM0
   51C2 55            [ 4]  138 	ld	d, l
   51C3 C1            [10]  139 	pop	bc
   51C4 21 20 04      [10]  140 	ld	hl, #0x0420
   51C7 E5            [11]  141 	push	hl
   51C8 D5            [11]  142 	push	de
   51C9 33            [ 6]  143 	inc	sp
   51CA C5            [11]  144 	push	bc
   51CB CD 74 66      [17]  145 	call	_cpct_drawSolidBox
   51CE F1            [10]  146 	pop	af
   51CF F1            [10]  147 	pop	af
   51D0 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   51D1 21 0F 68      [10]  150 	ld	hl,#_gtilegroundy + 0
   51D4 46            [ 7]  151 	ld	b, (hl)
   51D5 05            [ 4]  152 	dec	b
   51D6 05            [ 4]  153 	dec	b
   51D7 C5            [11]  154 	push	bc
   51D8 33            [ 6]  155 	inc	sp
   51D9 3E 38         [ 7]  156 	ld	a, #0x38
   51DB F5            [11]  157 	push	af
   51DC 33            [ 6]  158 	inc	sp
   51DD 21 00 C0      [10]  159 	ld	hl, #0xc000
   51E0 E5            [11]  160 	push	hl
   51E1 CD 2D 67      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   51E4 E5            [11]  163 	push	hl
   51E5 21 03 03      [10]  164 	ld	hl, #0x0303
   51E8 E5            [11]  165 	push	hl
   51E9 CD 3A 66      [17]  166 	call	_cpct_px2byteM0
   51EC 55            [ 4]  167 	ld	d, l
   51ED C1            [10]  168 	pop	bc
   51EE 21 10 02      [10]  169 	ld	hl, #0x0210
   51F1 E5            [11]  170 	push	hl
   51F2 D5            [11]  171 	push	de
   51F3 33            [ 6]  172 	inc	sp
   51F4 C5            [11]  173 	push	bc
   51F5 CD 74 66      [17]  174 	call	_cpct_drawSolidBox
   51F8 F1            [10]  175 	pop	af
   51F9 F1            [10]  176 	pop	af
   51FA 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   51FB 3A 0F 68      [13]  179 	ld	a,(#_gtilegroundy + 0)
   51FE C6 F0         [ 7]  180 	add	a, #0xf0
   5200 47            [ 4]  181 	ld	b, a
   5201 C5            [11]  182 	push	bc
   5202 33            [ 6]  183 	inc	sp
   5203 3A 11 68      [13]  184 	ld	a, (_ggoalx)
   5206 F5            [11]  185 	push	af
   5207 33            [ 6]  186 	inc	sp
   5208 21 00 C0      [10]  187 	ld	hl, #0xc000
   520B E5            [11]  188 	push	hl
   520C CD 2D 67      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   520F E5            [11]  191 	push	hl
   5210 21 05 05      [10]  192 	ld	hl, #0x0505
   5213 E5            [11]  193 	push	hl
   5214 CD 3A 66      [17]  194 	call	_cpct_px2byteM0
   5217 55            [ 4]  195 	ld	d, l
   5218 C1            [10]  196 	pop	bc
   5219 21 02 10      [10]  197 	ld	hl, #0x1002
   521C E5            [11]  198 	push	hl
   521D D5            [11]  199 	push	de
   521E 33            [ 6]  200 	inc	sp
   521F C5            [11]  201 	push	bc
   5220 CD 74 66      [17]  202 	call	_cpct_drawSolidBox
   5223 F1            [10]  203 	pop	af
   5224 F1            [10]  204 	pop	af
   5225 33            [ 6]  205 	inc	sp
   5226 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5227                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5227 FD 21 0F 68   [14]  213 	ld	iy, #_gtilegroundy
   522B FD 6E 00      [19]  214 	ld	l, 0 (iy)
   522E C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   522F                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   522F FD 21 02 00   [14]  222 	ld	iy, #2
   5233 FD 39         [15]  223 	add	iy, sp
   5235 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5238 D6 18         [ 7]  225 	sub	a, #0x18
   523A FD 7E 01      [19]  226 	ld	a, 1 (iy)
   523D 17            [ 4]  227 	rla
   523E 3F            [ 4]  228 	ccf
   523F 1F            [ 4]  229 	rra
   5240 DE 80         [ 7]  230 	sbc	a, #0x80
   5242 38 1A         [12]  231 	jr	C,00102$
   5244 3E 38         [ 7]  232 	ld	a, #0x38
   5246 FD BE 00      [19]  233 	cp	a, 0 (iy)
   5249 3E 00         [ 7]  234 	ld	a, #0x00
   524B FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   524E E2 53 52      [10]  236 	jp	PO, 00114$
   5251 EE 80         [ 7]  237 	xor	a, #0x80
   5253                     238 00114$:
   5253 FA 5E 52      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5256 FD 21 10 68   [14]  241 	ld	iy, #_gtileplatformy
   525A FD 6E 00      [19]  242 	ld	l, 0 (iy)
   525D C9            [10]  243 	ret
   525E                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   525E 2E FF         [ 7]  246 	ld	l, #0xff
   5260 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   5261                     252 _tilemap_is_trap::
   5261 DD E5         [15]  253 	push	ix
   5263 DD 21 00 00   [14]  254 	ld	ix,#0
   5267 DD 39         [15]  255 	add	ix,sp
   5269 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   526A DD 4E 04      [19]  258 	ld	c,4 (ix)
   526D DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5270 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5273 26 00         [ 7]  262 	ld	h, #0x00
   5275 09            [11]  263 	add	hl, bc
   5276 33            [ 6]  264 	inc	sp
   5277 33            [ 6]  265 	inc	sp
   5278 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5279 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   527C 16 00         [ 7]  269 	ld	d, #0x00
   527E DD 6E 06      [19]  270 	ld	l,6 (ix)
   5281 DD 66 07      [19]  271 	ld	h,7 (ix)
   5284 19            [11]  272 	add	hl, de
   5285 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5286 FD 21 0F 68   [14]  275 	ld	iy, #_gtilegroundy
   528A FD 6E 00      [19]  276 	ld	l, 0 (iy)
   528D 26 00         [ 7]  277 	ld	h, #0x00
   528F 2B            [ 6]  278 	dec	hl
   5290 2B            [ 6]  279 	dec	hl
   5291 7B            [ 4]  280 	ld	a, e
   5292 95            [ 4]  281 	sub	a, l
   5293 7A            [ 4]  282 	ld	a, d
   5294 9C            [ 4]  283 	sbc	a, h
   5295 E2 9A 52      [10]  284 	jp	PO, 00119$
   5298 EE 80         [ 7]  285 	xor	a, #0x80
   529A                     286 00119$:
   529A FA BE 52      [10]  287 	jp	M, 00102$
   529D 79            [ 4]  288 	ld	a, c
   529E D6 48         [ 7]  289 	sub	a, #0x48
   52A0 78            [ 4]  290 	ld	a, b
   52A1 17            [ 4]  291 	rla
   52A2 3F            [ 4]  292 	ccf
   52A3 1F            [ 4]  293 	rra
   52A4 DE 80         [ 7]  294 	sbc	a, #0x80
   52A6 30 16         [12]  295 	jr	NC,00102$
   52A8 3E 38         [ 7]  296 	ld	a, #0x38
   52AA DD BE FE      [19]  297 	cp	a, -2 (ix)
   52AD 3E 00         [ 7]  298 	ld	a, #0x00
   52AF DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   52B2 E2 B7 52      [10]  300 	jp	PO, 00120$
   52B5 EE 80         [ 7]  301 	xor	a, #0x80
   52B7                     302 00120$:
   52B7 F2 BE 52      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   52BA 2E 01         [ 7]  305 	ld	l, #0x01
   52BC 18 02         [12]  306 	jr	00105$
   52BE                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   52BE 2E 00         [ 7]  309 	ld	l, #0x00
   52C0                     310 00105$:
   52C0 DD F9         [10]  311 	ld	sp, ix
   52C2 DD E1         [14]  312 	pop	ix
   52C4 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   52C5                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   52C5 2E 00         [ 7]  320 	ld	l, #0x00
   52C7 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   52C8                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   52C8 2E 00         [ 7]  328 	ld	l, #0x00
   52CA C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   52CB                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   52CB FD 21 11 68   [14]  336 	ld	iy, #_ggoalx
   52CF FD 6E 00      [19]  337 	ld	l, 0 (iy)
   52D2 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   6816                     341 __xinit__gtilegroundy:
   6816 A0                  342 	.db #0xa0	; 160
   6817                     343 __xinit__gtileplatformy:
   6817 80                  344 	.db #0x80	; 128
   6818                     345 __xinit__ggoalx:
   6818 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
