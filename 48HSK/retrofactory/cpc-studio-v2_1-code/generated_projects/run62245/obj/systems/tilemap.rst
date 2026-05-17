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
   63B0                      33 _gtilegroundy:
   63B0                      34 	.ds 1
   63B1                      35 _gtileplatformy:
   63B1                      36 	.ds 1
   63B2                      37 _ggoalx:
   63B2                      38 	.ds 1
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
   515C                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   515C 2A D7 52      [16]   65 	ld	hl, (_level1tilemapheight)
   515F 3E 02         [ 7]   66 	ld	a, #0x02
   5161 BD            [ 4]   67 	cp	a, l
   5162 3E 00         [ 7]   68 	ld	a, #0x00
   5164 9C            [ 4]   69 	sbc	a, h
   5165 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5167 7D            [ 4]   72 	ld	a, l
   5168 C6 FE         [ 7]   73 	add	a, #0xfe
   516A 07            [ 4]   74 	rlca
   516B 07            [ 4]   75 	rlca
   516C 07            [ 4]   76 	rlca
   516D E6 F8         [ 7]   77 	and	a, #0xf8
   516F 32 B0 63      [13]   78 	ld	(#_gtilegroundy + 0),a
   5172 18 05         [12]   79 	jr	00103$
   5174                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5174 21 B0 63      [10]   82 	ld	hl,#_gtilegroundy + 0
   5177 36 A0         [10]   83 	ld	(hl), #0xa0
   5179                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5179 21 B1 63      [10]   86 	ld	hl, #_gtileplatformy
   517C 3A B0 63      [13]   87 	ld	a,(#_gtilegroundy + 0)
   517F C6 E8         [ 7]   88 	add	a, #0xe8
   5181 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5182 21 B2 63      [10]   91 	ld	hl,#_ggoalx + 0
   5185 36 48         [10]   92 	ld	(hl), #0x48
   5187 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5188                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5188 3A B0 63      [13]  100 	ld	a, (_gtilegroundy)
   518B F5            [11]  101 	push	af
   518C 33            [ 6]  102 	inc	sp
   518D AF            [ 4]  103 	xor	a, a
   518E F5            [11]  104 	push	af
   518F 33            [ 6]  105 	inc	sp
   5190 21 00 C0      [10]  106 	ld	hl, #0xc000
   5193 E5            [11]  107 	push	hl
   5194 CD CE 62      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5197 E5            [11]  110 	push	hl
   5198 21 01 01      [10]  111 	ld	hl, #0x0101
   519B E5            [11]  112 	push	hl
   519C CD DB 61      [17]  113 	call	_cpct_px2byteM0
   519F 55            [ 4]  114 	ld	d, l
   51A0 C1            [10]  115 	pop	bc
   51A1 21 50 08      [10]  116 	ld	hl, #0x0850
   51A4 E5            [11]  117 	push	hl
   51A5 D5            [11]  118 	push	de
   51A6 33            [ 6]  119 	inc	sp
   51A7 C5            [11]  120 	push	bc
   51A8 CD 15 62      [17]  121 	call	_cpct_drawSolidBox
   51AB F1            [10]  122 	pop	af
   51AC F1            [10]  123 	pop	af
   51AD 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   51AE 3A B1 63      [13]  126 	ld	a, (_gtileplatformy)
   51B1 57            [ 4]  127 	ld	d,a
   51B2 1E 18         [ 7]  128 	ld	e,#0x18
   51B4 D5            [11]  129 	push	de
   51B5 21 00 C0      [10]  130 	ld	hl, #0xc000
   51B8 E5            [11]  131 	push	hl
   51B9 CD CE 62      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   51BC E5            [11]  134 	push	hl
   51BD 21 02 02      [10]  135 	ld	hl, #0x0202
   51C0 E5            [11]  136 	push	hl
   51C1 CD DB 61      [17]  137 	call	_cpct_px2byteM0
   51C4 55            [ 4]  138 	ld	d, l
   51C5 C1            [10]  139 	pop	bc
   51C6 21 20 04      [10]  140 	ld	hl, #0x0420
   51C9 E5            [11]  141 	push	hl
   51CA D5            [11]  142 	push	de
   51CB 33            [ 6]  143 	inc	sp
   51CC C5            [11]  144 	push	bc
   51CD CD 15 62      [17]  145 	call	_cpct_drawSolidBox
   51D0 F1            [10]  146 	pop	af
   51D1 F1            [10]  147 	pop	af
   51D2 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   51D3 21 B0 63      [10]  150 	ld	hl,#_gtilegroundy + 0
   51D6 46            [ 7]  151 	ld	b, (hl)
   51D7 05            [ 4]  152 	dec	b
   51D8 05            [ 4]  153 	dec	b
   51D9 C5            [11]  154 	push	bc
   51DA 33            [ 6]  155 	inc	sp
   51DB 3E 38         [ 7]  156 	ld	a, #0x38
   51DD F5            [11]  157 	push	af
   51DE 33            [ 6]  158 	inc	sp
   51DF 21 00 C0      [10]  159 	ld	hl, #0xc000
   51E2 E5            [11]  160 	push	hl
   51E3 CD CE 62      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   51E6 E5            [11]  163 	push	hl
   51E7 21 03 03      [10]  164 	ld	hl, #0x0303
   51EA E5            [11]  165 	push	hl
   51EB CD DB 61      [17]  166 	call	_cpct_px2byteM0
   51EE 55            [ 4]  167 	ld	d, l
   51EF C1            [10]  168 	pop	bc
   51F0 21 10 02      [10]  169 	ld	hl, #0x0210
   51F3 E5            [11]  170 	push	hl
   51F4 D5            [11]  171 	push	de
   51F5 33            [ 6]  172 	inc	sp
   51F6 C5            [11]  173 	push	bc
   51F7 CD 15 62      [17]  174 	call	_cpct_drawSolidBox
   51FA F1            [10]  175 	pop	af
   51FB F1            [10]  176 	pop	af
   51FC 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   51FD 3A B0 63      [13]  179 	ld	a,(#_gtilegroundy + 0)
   5200 C6 F0         [ 7]  180 	add	a, #0xf0
   5202 47            [ 4]  181 	ld	b, a
   5203 C5            [11]  182 	push	bc
   5204 33            [ 6]  183 	inc	sp
   5205 3A B2 63      [13]  184 	ld	a, (_ggoalx)
   5208 F5            [11]  185 	push	af
   5209 33            [ 6]  186 	inc	sp
   520A 21 00 C0      [10]  187 	ld	hl, #0xc000
   520D E5            [11]  188 	push	hl
   520E CD CE 62      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   5211 E5            [11]  191 	push	hl
   5212 21 05 05      [10]  192 	ld	hl, #0x0505
   5215 E5            [11]  193 	push	hl
   5216 CD DB 61      [17]  194 	call	_cpct_px2byteM0
   5219 55            [ 4]  195 	ld	d, l
   521A C1            [10]  196 	pop	bc
   521B 21 02 10      [10]  197 	ld	hl, #0x1002
   521E E5            [11]  198 	push	hl
   521F D5            [11]  199 	push	de
   5220 33            [ 6]  200 	inc	sp
   5221 C5            [11]  201 	push	bc
   5222 CD 15 62      [17]  202 	call	_cpct_drawSolidBox
   5225 F1            [10]  203 	pop	af
   5226 F1            [10]  204 	pop	af
   5227 33            [ 6]  205 	inc	sp
   5228 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5229                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5229 FD 21 B0 63   [14]  213 	ld	iy, #_gtilegroundy
   522D FD 6E 00      [19]  214 	ld	l, 0 (iy)
   5230 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   5231                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   5231 FD 21 02 00   [14]  222 	ld	iy, #2
   5235 FD 39         [15]  223 	add	iy, sp
   5237 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   523A D6 18         [ 7]  225 	sub	a, #0x18
   523C FD 7E 01      [19]  226 	ld	a, 1 (iy)
   523F 17            [ 4]  227 	rla
   5240 3F            [ 4]  228 	ccf
   5241 1F            [ 4]  229 	rra
   5242 DE 80         [ 7]  230 	sbc	a, #0x80
   5244 38 1A         [12]  231 	jr	C,00102$
   5246 3E 38         [ 7]  232 	ld	a, #0x38
   5248 FD BE 00      [19]  233 	cp	a, 0 (iy)
   524B 3E 00         [ 7]  234 	ld	a, #0x00
   524D FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   5250 E2 55 52      [10]  236 	jp	PO, 00114$
   5253 EE 80         [ 7]  237 	xor	a, #0x80
   5255                     238 00114$:
   5255 FA 60 52      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5258 FD 21 B1 63   [14]  241 	ld	iy, #_gtileplatformy
   525C FD 6E 00      [19]  242 	ld	l, 0 (iy)
   525F C9            [10]  243 	ret
   5260                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   5260 2E FF         [ 7]  246 	ld	l, #0xff
   5262 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   5263                     252 _tilemap_is_trap::
   5263 DD E5         [15]  253 	push	ix
   5265 DD 21 00 00   [14]  254 	ld	ix,#0
   5269 DD 39         [15]  255 	add	ix,sp
   526B F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   526C DD 4E 04      [19]  258 	ld	c,4 (ix)
   526F DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5272 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5275 26 00         [ 7]  262 	ld	h, #0x00
   5277 09            [11]  263 	add	hl, bc
   5278 33            [ 6]  264 	inc	sp
   5279 33            [ 6]  265 	inc	sp
   527A E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   527B DD 5E 09      [19]  268 	ld	e, 9 (ix)
   527E 16 00         [ 7]  269 	ld	d, #0x00
   5280 DD 6E 06      [19]  270 	ld	l,6 (ix)
   5283 DD 66 07      [19]  271 	ld	h,7 (ix)
   5286 19            [11]  272 	add	hl, de
   5287 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5288 FD 21 B0 63   [14]  275 	ld	iy, #_gtilegroundy
   528C FD 6E 00      [19]  276 	ld	l, 0 (iy)
   528F 26 00         [ 7]  277 	ld	h, #0x00
   5291 2B            [ 6]  278 	dec	hl
   5292 2B            [ 6]  279 	dec	hl
   5293 7B            [ 4]  280 	ld	a, e
   5294 95            [ 4]  281 	sub	a, l
   5295 7A            [ 4]  282 	ld	a, d
   5296 9C            [ 4]  283 	sbc	a, h
   5297 E2 9C 52      [10]  284 	jp	PO, 00119$
   529A EE 80         [ 7]  285 	xor	a, #0x80
   529C                     286 00119$:
   529C FA C0 52      [10]  287 	jp	M, 00102$
   529F 79            [ 4]  288 	ld	a, c
   52A0 D6 48         [ 7]  289 	sub	a, #0x48
   52A2 78            [ 4]  290 	ld	a, b
   52A3 17            [ 4]  291 	rla
   52A4 3F            [ 4]  292 	ccf
   52A5 1F            [ 4]  293 	rra
   52A6 DE 80         [ 7]  294 	sbc	a, #0x80
   52A8 30 16         [12]  295 	jr	NC,00102$
   52AA 3E 38         [ 7]  296 	ld	a, #0x38
   52AC DD BE FE      [19]  297 	cp	a, -2 (ix)
   52AF 3E 00         [ 7]  298 	ld	a, #0x00
   52B1 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   52B4 E2 B9 52      [10]  300 	jp	PO, 00120$
   52B7 EE 80         [ 7]  301 	xor	a, #0x80
   52B9                     302 00120$:
   52B9 F2 C0 52      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   52BC 2E 01         [ 7]  305 	ld	l, #0x01
   52BE 18 02         [12]  306 	jr	00105$
   52C0                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   52C0 2E 00         [ 7]  309 	ld	l, #0x00
   52C2                     310 00105$:
   52C2 DD F9         [10]  311 	ld	sp, ix
   52C4 DD E1         [14]  312 	pop	ix
   52C6 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   52C7                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   52C7 2E 00         [ 7]  320 	ld	l, #0x00
   52C9 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   52CA                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   52CA 2E 00         [ 7]  328 	ld	l, #0x00
   52CC C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   52CD                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   52CD FD 21 B2 63   [14]  336 	ld	iy, #_ggoalx
   52D1 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   52D4 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   63B7                     341 __xinit__gtilegroundy:
   63B7 A0                  342 	.db #0xa0	; 160
   63B8                     343 __xinit__gtileplatformy:
   63B8 80                  344 	.db #0x80	; 128
   63B9                     345 __xinit__ggoalx:
   63B9 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
