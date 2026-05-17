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
   6389                      33 _gtilegroundy:
   6389                      34 	.ds 1
   638A                      35 _gtileplatformy:
   638A                      36 	.ds 1
   638B                      37 _ggoalx:
   638B                      38 	.ds 1
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
   513C                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   513C 2A B7 52      [16]   65 	ld	hl, (_level1tilemapheight)
   513F 3E 02         [ 7]   66 	ld	a, #0x02
   5141 BD            [ 4]   67 	cp	a, l
   5142 3E 00         [ 7]   68 	ld	a, #0x00
   5144 9C            [ 4]   69 	sbc	a, h
   5145 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5147 7D            [ 4]   72 	ld	a, l
   5148 C6 FE         [ 7]   73 	add	a, #0xfe
   514A 07            [ 4]   74 	rlca
   514B 07            [ 4]   75 	rlca
   514C 07            [ 4]   76 	rlca
   514D E6 F8         [ 7]   77 	and	a, #0xf8
   514F 32 89 63      [13]   78 	ld	(#_gtilegroundy + 0),a
   5152 18 05         [12]   79 	jr	00103$
   5154                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5154 21 89 63      [10]   82 	ld	hl,#_gtilegroundy + 0
   5157 36 A0         [10]   83 	ld	(hl), #0xa0
   5159                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5159 21 8A 63      [10]   86 	ld	hl, #_gtileplatformy
   515C 3A 89 63      [13]   87 	ld	a,(#_gtilegroundy + 0)
   515F C6 E8         [ 7]   88 	add	a, #0xe8
   5161 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5162 21 8B 63      [10]   91 	ld	hl,#_ggoalx + 0
   5165 36 48         [10]   92 	ld	(hl), #0x48
   5167 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5168                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5168 3A 89 63      [13]  100 	ld	a, (_gtilegroundy)
   516B F5            [11]  101 	push	af
   516C 33            [ 6]  102 	inc	sp
   516D AF            [ 4]  103 	xor	a, a
   516E F5            [11]  104 	push	af
   516F 33            [ 6]  105 	inc	sp
   5170 21 00 C0      [10]  106 	ld	hl, #0xc000
   5173 E5            [11]  107 	push	hl
   5174 CD A7 62      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5177 E5            [11]  110 	push	hl
   5178 21 01 01      [10]  111 	ld	hl, #0x0101
   517B E5            [11]  112 	push	hl
   517C CD B4 61      [17]  113 	call	_cpct_px2byteM0
   517F 55            [ 4]  114 	ld	d, l
   5180 C1            [10]  115 	pop	bc
   5181 21 50 08      [10]  116 	ld	hl, #0x0850
   5184 E5            [11]  117 	push	hl
   5185 D5            [11]  118 	push	de
   5186 33            [ 6]  119 	inc	sp
   5187 C5            [11]  120 	push	bc
   5188 CD EE 61      [17]  121 	call	_cpct_drawSolidBox
   518B F1            [10]  122 	pop	af
   518C F1            [10]  123 	pop	af
   518D 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   518E 3A 8A 63      [13]  126 	ld	a, (_gtileplatformy)
   5191 57            [ 4]  127 	ld	d,a
   5192 1E 18         [ 7]  128 	ld	e,#0x18
   5194 D5            [11]  129 	push	de
   5195 21 00 C0      [10]  130 	ld	hl, #0xc000
   5198 E5            [11]  131 	push	hl
   5199 CD A7 62      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   519C E5            [11]  134 	push	hl
   519D 21 02 02      [10]  135 	ld	hl, #0x0202
   51A0 E5            [11]  136 	push	hl
   51A1 CD B4 61      [17]  137 	call	_cpct_px2byteM0
   51A4 55            [ 4]  138 	ld	d, l
   51A5 C1            [10]  139 	pop	bc
   51A6 21 20 04      [10]  140 	ld	hl, #0x0420
   51A9 E5            [11]  141 	push	hl
   51AA D5            [11]  142 	push	de
   51AB 33            [ 6]  143 	inc	sp
   51AC C5            [11]  144 	push	bc
   51AD CD EE 61      [17]  145 	call	_cpct_drawSolidBox
   51B0 F1            [10]  146 	pop	af
   51B1 F1            [10]  147 	pop	af
   51B2 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   51B3 21 89 63      [10]  150 	ld	hl,#_gtilegroundy + 0
   51B6 46            [ 7]  151 	ld	b, (hl)
   51B7 05            [ 4]  152 	dec	b
   51B8 05            [ 4]  153 	dec	b
   51B9 C5            [11]  154 	push	bc
   51BA 33            [ 6]  155 	inc	sp
   51BB 3E 38         [ 7]  156 	ld	a, #0x38
   51BD F5            [11]  157 	push	af
   51BE 33            [ 6]  158 	inc	sp
   51BF 21 00 C0      [10]  159 	ld	hl, #0xc000
   51C2 E5            [11]  160 	push	hl
   51C3 CD A7 62      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   51C6 E5            [11]  163 	push	hl
   51C7 21 03 03      [10]  164 	ld	hl, #0x0303
   51CA E5            [11]  165 	push	hl
   51CB CD B4 61      [17]  166 	call	_cpct_px2byteM0
   51CE 55            [ 4]  167 	ld	d, l
   51CF C1            [10]  168 	pop	bc
   51D0 21 10 02      [10]  169 	ld	hl, #0x0210
   51D3 E5            [11]  170 	push	hl
   51D4 D5            [11]  171 	push	de
   51D5 33            [ 6]  172 	inc	sp
   51D6 C5            [11]  173 	push	bc
   51D7 CD EE 61      [17]  174 	call	_cpct_drawSolidBox
   51DA F1            [10]  175 	pop	af
   51DB F1            [10]  176 	pop	af
   51DC 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   51DD 3A 89 63      [13]  179 	ld	a,(#_gtilegroundy + 0)
   51E0 C6 F0         [ 7]  180 	add	a, #0xf0
   51E2 47            [ 4]  181 	ld	b, a
   51E3 C5            [11]  182 	push	bc
   51E4 33            [ 6]  183 	inc	sp
   51E5 3A 8B 63      [13]  184 	ld	a, (_ggoalx)
   51E8 F5            [11]  185 	push	af
   51E9 33            [ 6]  186 	inc	sp
   51EA 21 00 C0      [10]  187 	ld	hl, #0xc000
   51ED E5            [11]  188 	push	hl
   51EE CD A7 62      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   51F1 E5            [11]  191 	push	hl
   51F2 21 05 05      [10]  192 	ld	hl, #0x0505
   51F5 E5            [11]  193 	push	hl
   51F6 CD B4 61      [17]  194 	call	_cpct_px2byteM0
   51F9 55            [ 4]  195 	ld	d, l
   51FA C1            [10]  196 	pop	bc
   51FB 21 02 10      [10]  197 	ld	hl, #0x1002
   51FE E5            [11]  198 	push	hl
   51FF D5            [11]  199 	push	de
   5200 33            [ 6]  200 	inc	sp
   5201 C5            [11]  201 	push	bc
   5202 CD EE 61      [17]  202 	call	_cpct_drawSolidBox
   5205 F1            [10]  203 	pop	af
   5206 F1            [10]  204 	pop	af
   5207 33            [ 6]  205 	inc	sp
   5208 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5209                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5209 FD 21 89 63   [14]  213 	ld	iy, #_gtilegroundy
   520D FD 6E 00      [19]  214 	ld	l, 0 (iy)
   5210 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   5211                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   5211 FD 21 02 00   [14]  222 	ld	iy, #2
   5215 FD 39         [15]  223 	add	iy, sp
   5217 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   521A D6 18         [ 7]  225 	sub	a, #0x18
   521C FD 7E 01      [19]  226 	ld	a, 1 (iy)
   521F 17            [ 4]  227 	rla
   5220 3F            [ 4]  228 	ccf
   5221 1F            [ 4]  229 	rra
   5222 DE 80         [ 7]  230 	sbc	a, #0x80
   5224 38 1A         [12]  231 	jr	C,00102$
   5226 3E 38         [ 7]  232 	ld	a, #0x38
   5228 FD BE 00      [19]  233 	cp	a, 0 (iy)
   522B 3E 00         [ 7]  234 	ld	a, #0x00
   522D FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   5230 E2 35 52      [10]  236 	jp	PO, 00114$
   5233 EE 80         [ 7]  237 	xor	a, #0x80
   5235                     238 00114$:
   5235 FA 40 52      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5238 FD 21 8A 63   [14]  241 	ld	iy, #_gtileplatformy
   523C FD 6E 00      [19]  242 	ld	l, 0 (iy)
   523F C9            [10]  243 	ret
   5240                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   5240 2E FF         [ 7]  246 	ld	l, #0xff
   5242 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   5243                     252 _tilemap_is_trap::
   5243 DD E5         [15]  253 	push	ix
   5245 DD 21 00 00   [14]  254 	ld	ix,#0
   5249 DD 39         [15]  255 	add	ix,sp
   524B F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   524C DD 4E 04      [19]  258 	ld	c,4 (ix)
   524F DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5252 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5255 26 00         [ 7]  262 	ld	h, #0x00
   5257 09            [11]  263 	add	hl, bc
   5258 33            [ 6]  264 	inc	sp
   5259 33            [ 6]  265 	inc	sp
   525A E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   525B DD 5E 09      [19]  268 	ld	e, 9 (ix)
   525E 16 00         [ 7]  269 	ld	d, #0x00
   5260 DD 6E 06      [19]  270 	ld	l,6 (ix)
   5263 DD 66 07      [19]  271 	ld	h,7 (ix)
   5266 19            [11]  272 	add	hl, de
   5267 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5268 FD 21 89 63   [14]  275 	ld	iy, #_gtilegroundy
   526C FD 6E 00      [19]  276 	ld	l, 0 (iy)
   526F 26 00         [ 7]  277 	ld	h, #0x00
   5271 2B            [ 6]  278 	dec	hl
   5272 2B            [ 6]  279 	dec	hl
   5273 7B            [ 4]  280 	ld	a, e
   5274 95            [ 4]  281 	sub	a, l
   5275 7A            [ 4]  282 	ld	a, d
   5276 9C            [ 4]  283 	sbc	a, h
   5277 E2 7C 52      [10]  284 	jp	PO, 00119$
   527A EE 80         [ 7]  285 	xor	a, #0x80
   527C                     286 00119$:
   527C FA A0 52      [10]  287 	jp	M, 00102$
   527F 79            [ 4]  288 	ld	a, c
   5280 D6 48         [ 7]  289 	sub	a, #0x48
   5282 78            [ 4]  290 	ld	a, b
   5283 17            [ 4]  291 	rla
   5284 3F            [ 4]  292 	ccf
   5285 1F            [ 4]  293 	rra
   5286 DE 80         [ 7]  294 	sbc	a, #0x80
   5288 30 16         [12]  295 	jr	NC,00102$
   528A 3E 38         [ 7]  296 	ld	a, #0x38
   528C DD BE FE      [19]  297 	cp	a, -2 (ix)
   528F 3E 00         [ 7]  298 	ld	a, #0x00
   5291 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5294 E2 99 52      [10]  300 	jp	PO, 00120$
   5297 EE 80         [ 7]  301 	xor	a, #0x80
   5299                     302 00120$:
   5299 F2 A0 52      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   529C 2E 01         [ 7]  305 	ld	l, #0x01
   529E 18 02         [12]  306 	jr	00105$
   52A0                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   52A0 2E 00         [ 7]  309 	ld	l, #0x00
   52A2                     310 00105$:
   52A2 DD F9         [10]  311 	ld	sp, ix
   52A4 DD E1         [14]  312 	pop	ix
   52A6 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   52A7                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   52A7 2E 00         [ 7]  320 	ld	l, #0x00
   52A9 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   52AA                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   52AA 2E 00         [ 7]  328 	ld	l, #0x00
   52AC C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   52AD                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   52AD FD 21 8B 63   [14]  336 	ld	iy, #_ggoalx
   52B1 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   52B4 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   6390                     341 __xinit__gtilegroundy:
   6390 A0                  342 	.db #0xa0	; 160
   6391                     343 __xinit__gtileplatformy:
   6391 80                  344 	.db #0x80	; 128
   6392                     345 __xinit__ggoalx:
   6392 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
