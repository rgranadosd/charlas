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
   6423                      33 _gtilegroundy:
   6423                      34 	.ds 1
   6424                      35 _gtileplatformy:
   6424                      36 	.ds 1
   6425                      37 _ggoalx:
   6425                      38 	.ds 1
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
   513A                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   513A 2A B5 52      [16]   65 	ld	hl, (_level1tilemapheight)
   513D 3E 02         [ 7]   66 	ld	a, #0x02
   513F BD            [ 4]   67 	cp	a, l
   5140 3E 00         [ 7]   68 	ld	a, #0x00
   5142 9C            [ 4]   69 	sbc	a, h
   5143 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5145 7D            [ 4]   72 	ld	a, l
   5146 C6 FE         [ 7]   73 	add	a, #0xfe
   5148 07            [ 4]   74 	rlca
   5149 07            [ 4]   75 	rlca
   514A 07            [ 4]   76 	rlca
   514B E6 F8         [ 7]   77 	and	a, #0xf8
   514D 32 23 64      [13]   78 	ld	(#_gtilegroundy + 0),a
   5150 18 05         [12]   79 	jr	00103$
   5152                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5152 21 23 64      [10]   82 	ld	hl,#_gtilegroundy + 0
   5155 36 A0         [10]   83 	ld	(hl), #0xa0
   5157                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5157 21 24 64      [10]   86 	ld	hl, #_gtileplatformy
   515A 3A 23 64      [13]   87 	ld	a,(#_gtilegroundy + 0)
   515D C6 E8         [ 7]   88 	add	a, #0xe8
   515F 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5160 21 25 64      [10]   91 	ld	hl,#_ggoalx + 0
   5163 36 48         [10]   92 	ld	(hl), #0x48
   5165 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5166                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5166 3A 23 64      [13]  100 	ld	a, (_gtilegroundy)
   5169 F5            [11]  101 	push	af
   516A 33            [ 6]  102 	inc	sp
   516B AF            [ 4]  103 	xor	a, a
   516C F5            [11]  104 	push	af
   516D 33            [ 6]  105 	inc	sp
   516E 21 00 C0      [10]  106 	ld	hl, #0xc000
   5171 E5            [11]  107 	push	hl
   5172 CD 41 63      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5175 E5            [11]  110 	push	hl
   5176 21 01 01      [10]  111 	ld	hl, #0x0101
   5179 E5            [11]  112 	push	hl
   517A CD 4E 62      [17]  113 	call	_cpct_px2byteM0
   517D 55            [ 4]  114 	ld	d, l
   517E C1            [10]  115 	pop	bc
   517F 21 50 08      [10]  116 	ld	hl, #0x0850
   5182 E5            [11]  117 	push	hl
   5183 D5            [11]  118 	push	de
   5184 33            [ 6]  119 	inc	sp
   5185 C5            [11]  120 	push	bc
   5186 CD 88 62      [17]  121 	call	_cpct_drawSolidBox
   5189 F1            [10]  122 	pop	af
   518A F1            [10]  123 	pop	af
   518B 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   518C 3A 24 64      [13]  126 	ld	a, (_gtileplatformy)
   518F 57            [ 4]  127 	ld	d,a
   5190 1E 18         [ 7]  128 	ld	e,#0x18
   5192 D5            [11]  129 	push	de
   5193 21 00 C0      [10]  130 	ld	hl, #0xc000
   5196 E5            [11]  131 	push	hl
   5197 CD 41 63      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   519A E5            [11]  134 	push	hl
   519B 21 02 02      [10]  135 	ld	hl, #0x0202
   519E E5            [11]  136 	push	hl
   519F CD 4E 62      [17]  137 	call	_cpct_px2byteM0
   51A2 55            [ 4]  138 	ld	d, l
   51A3 C1            [10]  139 	pop	bc
   51A4 21 20 04      [10]  140 	ld	hl, #0x0420
   51A7 E5            [11]  141 	push	hl
   51A8 D5            [11]  142 	push	de
   51A9 33            [ 6]  143 	inc	sp
   51AA C5            [11]  144 	push	bc
   51AB CD 88 62      [17]  145 	call	_cpct_drawSolidBox
   51AE F1            [10]  146 	pop	af
   51AF F1            [10]  147 	pop	af
   51B0 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   51B1 21 23 64      [10]  150 	ld	hl,#_gtilegroundy + 0
   51B4 46            [ 7]  151 	ld	b, (hl)
   51B5 05            [ 4]  152 	dec	b
   51B6 05            [ 4]  153 	dec	b
   51B7 C5            [11]  154 	push	bc
   51B8 33            [ 6]  155 	inc	sp
   51B9 3E 38         [ 7]  156 	ld	a, #0x38
   51BB F5            [11]  157 	push	af
   51BC 33            [ 6]  158 	inc	sp
   51BD 21 00 C0      [10]  159 	ld	hl, #0xc000
   51C0 E5            [11]  160 	push	hl
   51C1 CD 41 63      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   51C4 E5            [11]  163 	push	hl
   51C5 21 03 03      [10]  164 	ld	hl, #0x0303
   51C8 E5            [11]  165 	push	hl
   51C9 CD 4E 62      [17]  166 	call	_cpct_px2byteM0
   51CC 55            [ 4]  167 	ld	d, l
   51CD C1            [10]  168 	pop	bc
   51CE 21 10 02      [10]  169 	ld	hl, #0x0210
   51D1 E5            [11]  170 	push	hl
   51D2 D5            [11]  171 	push	de
   51D3 33            [ 6]  172 	inc	sp
   51D4 C5            [11]  173 	push	bc
   51D5 CD 88 62      [17]  174 	call	_cpct_drawSolidBox
   51D8 F1            [10]  175 	pop	af
   51D9 F1            [10]  176 	pop	af
   51DA 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   51DB 3A 23 64      [13]  179 	ld	a,(#_gtilegroundy + 0)
   51DE C6 F0         [ 7]  180 	add	a, #0xf0
   51E0 47            [ 4]  181 	ld	b, a
   51E1 C5            [11]  182 	push	bc
   51E2 33            [ 6]  183 	inc	sp
   51E3 3A 25 64      [13]  184 	ld	a, (_ggoalx)
   51E6 F5            [11]  185 	push	af
   51E7 33            [ 6]  186 	inc	sp
   51E8 21 00 C0      [10]  187 	ld	hl, #0xc000
   51EB E5            [11]  188 	push	hl
   51EC CD 41 63      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   51EF E5            [11]  191 	push	hl
   51F0 21 05 05      [10]  192 	ld	hl, #0x0505
   51F3 E5            [11]  193 	push	hl
   51F4 CD 4E 62      [17]  194 	call	_cpct_px2byteM0
   51F7 55            [ 4]  195 	ld	d, l
   51F8 C1            [10]  196 	pop	bc
   51F9 21 02 10      [10]  197 	ld	hl, #0x1002
   51FC E5            [11]  198 	push	hl
   51FD D5            [11]  199 	push	de
   51FE 33            [ 6]  200 	inc	sp
   51FF C5            [11]  201 	push	bc
   5200 CD 88 62      [17]  202 	call	_cpct_drawSolidBox
   5203 F1            [10]  203 	pop	af
   5204 F1            [10]  204 	pop	af
   5205 33            [ 6]  205 	inc	sp
   5206 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5207                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5207 FD 21 23 64   [14]  213 	ld	iy, #_gtilegroundy
   520B FD 6E 00      [19]  214 	ld	l, 0 (iy)
   520E C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   520F                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   520F FD 21 02 00   [14]  222 	ld	iy, #2
   5213 FD 39         [15]  223 	add	iy, sp
   5215 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5218 D6 18         [ 7]  225 	sub	a, #0x18
   521A FD 7E 01      [19]  226 	ld	a, 1 (iy)
   521D 17            [ 4]  227 	rla
   521E 3F            [ 4]  228 	ccf
   521F 1F            [ 4]  229 	rra
   5220 DE 80         [ 7]  230 	sbc	a, #0x80
   5222 38 1A         [12]  231 	jr	C,00102$
   5224 3E 38         [ 7]  232 	ld	a, #0x38
   5226 FD BE 00      [19]  233 	cp	a, 0 (iy)
   5229 3E 00         [ 7]  234 	ld	a, #0x00
   522B FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   522E E2 33 52      [10]  236 	jp	PO, 00114$
   5231 EE 80         [ 7]  237 	xor	a, #0x80
   5233                     238 00114$:
   5233 FA 3E 52      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5236 FD 21 24 64   [14]  241 	ld	iy, #_gtileplatformy
   523A FD 6E 00      [19]  242 	ld	l, 0 (iy)
   523D C9            [10]  243 	ret
   523E                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   523E 2E FF         [ 7]  246 	ld	l, #0xff
   5240 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   5241                     252 _tilemap_is_trap::
   5241 DD E5         [15]  253 	push	ix
   5243 DD 21 00 00   [14]  254 	ld	ix,#0
   5247 DD 39         [15]  255 	add	ix,sp
   5249 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   524A DD 4E 04      [19]  258 	ld	c,4 (ix)
   524D DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5250 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5253 26 00         [ 7]  262 	ld	h, #0x00
   5255 09            [11]  263 	add	hl, bc
   5256 33            [ 6]  264 	inc	sp
   5257 33            [ 6]  265 	inc	sp
   5258 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5259 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   525C 16 00         [ 7]  269 	ld	d, #0x00
   525E DD 6E 06      [19]  270 	ld	l,6 (ix)
   5261 DD 66 07      [19]  271 	ld	h,7 (ix)
   5264 19            [11]  272 	add	hl, de
   5265 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5266 FD 21 23 64   [14]  275 	ld	iy, #_gtilegroundy
   526A FD 6E 00      [19]  276 	ld	l, 0 (iy)
   526D 26 00         [ 7]  277 	ld	h, #0x00
   526F 2B            [ 6]  278 	dec	hl
   5270 2B            [ 6]  279 	dec	hl
   5271 7B            [ 4]  280 	ld	a, e
   5272 95            [ 4]  281 	sub	a, l
   5273 7A            [ 4]  282 	ld	a, d
   5274 9C            [ 4]  283 	sbc	a, h
   5275 E2 7A 52      [10]  284 	jp	PO, 00119$
   5278 EE 80         [ 7]  285 	xor	a, #0x80
   527A                     286 00119$:
   527A FA 9E 52      [10]  287 	jp	M, 00102$
   527D 79            [ 4]  288 	ld	a, c
   527E D6 48         [ 7]  289 	sub	a, #0x48
   5280 78            [ 4]  290 	ld	a, b
   5281 17            [ 4]  291 	rla
   5282 3F            [ 4]  292 	ccf
   5283 1F            [ 4]  293 	rra
   5284 DE 80         [ 7]  294 	sbc	a, #0x80
   5286 30 16         [12]  295 	jr	NC,00102$
   5288 3E 38         [ 7]  296 	ld	a, #0x38
   528A DD BE FE      [19]  297 	cp	a, -2 (ix)
   528D 3E 00         [ 7]  298 	ld	a, #0x00
   528F DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5292 E2 97 52      [10]  300 	jp	PO, 00120$
   5295 EE 80         [ 7]  301 	xor	a, #0x80
   5297                     302 00120$:
   5297 F2 9E 52      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   529A 2E 01         [ 7]  305 	ld	l, #0x01
   529C 18 02         [12]  306 	jr	00105$
   529E                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   529E 2E 00         [ 7]  309 	ld	l, #0x00
   52A0                     310 00105$:
   52A0 DD F9         [10]  311 	ld	sp, ix
   52A2 DD E1         [14]  312 	pop	ix
   52A4 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   52A5                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   52A5 2E 00         [ 7]  320 	ld	l, #0x00
   52A7 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   52A8                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   52A8 2E 00         [ 7]  328 	ld	l, #0x00
   52AA C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   52AB                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   52AB FD 21 25 64   [14]  336 	ld	iy, #_ggoalx
   52AF FD 6E 00      [19]  337 	ld	l, 0 (iy)
   52B2 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   642A                     341 __xinit__gtilegroundy:
   642A A0                  342 	.db #0xa0	; 160
   642B                     343 __xinit__gtileplatformy:
   642B 80                  344 	.db #0x80	; 128
   642C                     345 __xinit__ggoalx:
   642C 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
