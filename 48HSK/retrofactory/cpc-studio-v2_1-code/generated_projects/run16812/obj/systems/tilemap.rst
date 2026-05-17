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
   5FA1                      33 _gtilegroundy:
   5FA1                      34 	.ds 1
   5FA2                      35 _gtileplatformy:
   5FA2                      36 	.ds 1
   5FA3                      37 _ggoalx:
   5FA3                      38 	.ds 1
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
   50B5                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   50B5 2A 30 52      [16]   65 	ld	hl, (_level1tilemapheight)
   50B8 3E 02         [ 7]   66 	ld	a, #0x02
   50BA BD            [ 4]   67 	cp	a, l
   50BB 3E 00         [ 7]   68 	ld	a, #0x00
   50BD 9C            [ 4]   69 	sbc	a, h
   50BE 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   50C0 7D            [ 4]   72 	ld	a, l
   50C1 C6 FE         [ 7]   73 	add	a, #0xfe
   50C3 07            [ 4]   74 	rlca
   50C4 07            [ 4]   75 	rlca
   50C5 07            [ 4]   76 	rlca
   50C6 E6 F8         [ 7]   77 	and	a, #0xf8
   50C8 32 A1 5F      [13]   78 	ld	(#_gtilegroundy + 0),a
   50CB 18 05         [12]   79 	jr	00103$
   50CD                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   50CD 21 A1 5F      [10]   82 	ld	hl,#_gtilegroundy + 0
   50D0 36 A0         [10]   83 	ld	(hl), #0xa0
   50D2                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   50D2 21 A2 5F      [10]   86 	ld	hl, #_gtileplatformy
   50D5 3A A1 5F      [13]   87 	ld	a,(#_gtilegroundy + 0)
   50D8 C6 E8         [ 7]   88 	add	a, #0xe8
   50DA 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   50DB 21 A3 5F      [10]   91 	ld	hl,#_ggoalx + 0
   50DE 36 48         [10]   92 	ld	(hl), #0x48
   50E0 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   50E1                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   50E1 3A A1 5F      [13]  100 	ld	a, (_gtilegroundy)
   50E4 F5            [11]  101 	push	af
   50E5 33            [ 6]  102 	inc	sp
   50E6 AF            [ 4]  103 	xor	a, a
   50E7 F5            [11]  104 	push	af
   50E8 33            [ 6]  105 	inc	sp
   50E9 21 00 C0      [10]  106 	ld	hl, #0xc000
   50EC E5            [11]  107 	push	hl
   50ED CD A9 5E      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   50F0 E5            [11]  110 	push	hl
   50F1 21 01 01      [10]  111 	ld	hl, #0x0101
   50F4 E5            [11]  112 	push	hl
   50F5 CD B6 5D      [17]  113 	call	_cpct_px2byteM0
   50F8 55            [ 4]  114 	ld	d, l
   50F9 C1            [10]  115 	pop	bc
   50FA 21 50 08      [10]  116 	ld	hl, #0x0850
   50FD E5            [11]  117 	push	hl
   50FE D5            [11]  118 	push	de
   50FF 33            [ 6]  119 	inc	sp
   5100 C5            [11]  120 	push	bc
   5101 CD F0 5D      [17]  121 	call	_cpct_drawSolidBox
   5104 F1            [10]  122 	pop	af
   5105 F1            [10]  123 	pop	af
   5106 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5107 3A A2 5F      [13]  126 	ld	a, (_gtileplatformy)
   510A 57            [ 4]  127 	ld	d,a
   510B 1E 18         [ 7]  128 	ld	e,#0x18
   510D D5            [11]  129 	push	de
   510E 21 00 C0      [10]  130 	ld	hl, #0xc000
   5111 E5            [11]  131 	push	hl
   5112 CD A9 5E      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   5115 E5            [11]  134 	push	hl
   5116 21 02 02      [10]  135 	ld	hl, #0x0202
   5119 E5            [11]  136 	push	hl
   511A CD B6 5D      [17]  137 	call	_cpct_px2byteM0
   511D 55            [ 4]  138 	ld	d, l
   511E C1            [10]  139 	pop	bc
   511F 21 20 04      [10]  140 	ld	hl, #0x0420
   5122 E5            [11]  141 	push	hl
   5123 D5            [11]  142 	push	de
   5124 33            [ 6]  143 	inc	sp
   5125 C5            [11]  144 	push	bc
   5126 CD F0 5D      [17]  145 	call	_cpct_drawSolidBox
   5129 F1            [10]  146 	pop	af
   512A F1            [10]  147 	pop	af
   512B 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   512C 21 A1 5F      [10]  150 	ld	hl,#_gtilegroundy + 0
   512F 46            [ 7]  151 	ld	b, (hl)
   5130 05            [ 4]  152 	dec	b
   5131 05            [ 4]  153 	dec	b
   5132 C5            [11]  154 	push	bc
   5133 33            [ 6]  155 	inc	sp
   5134 3E 38         [ 7]  156 	ld	a, #0x38
   5136 F5            [11]  157 	push	af
   5137 33            [ 6]  158 	inc	sp
   5138 21 00 C0      [10]  159 	ld	hl, #0xc000
   513B E5            [11]  160 	push	hl
   513C CD A9 5E      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   513F E5            [11]  163 	push	hl
   5140 21 03 03      [10]  164 	ld	hl, #0x0303
   5143 E5            [11]  165 	push	hl
   5144 CD B6 5D      [17]  166 	call	_cpct_px2byteM0
   5147 55            [ 4]  167 	ld	d, l
   5148 C1            [10]  168 	pop	bc
   5149 21 10 02      [10]  169 	ld	hl, #0x0210
   514C E5            [11]  170 	push	hl
   514D D5            [11]  171 	push	de
   514E 33            [ 6]  172 	inc	sp
   514F C5            [11]  173 	push	bc
   5150 CD F0 5D      [17]  174 	call	_cpct_drawSolidBox
   5153 F1            [10]  175 	pop	af
   5154 F1            [10]  176 	pop	af
   5155 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   5156 3A A1 5F      [13]  179 	ld	a,(#_gtilegroundy + 0)
   5159 C6 F0         [ 7]  180 	add	a, #0xf0
   515B 47            [ 4]  181 	ld	b, a
   515C C5            [11]  182 	push	bc
   515D 33            [ 6]  183 	inc	sp
   515E 3A A3 5F      [13]  184 	ld	a, (_ggoalx)
   5161 F5            [11]  185 	push	af
   5162 33            [ 6]  186 	inc	sp
   5163 21 00 C0      [10]  187 	ld	hl, #0xc000
   5166 E5            [11]  188 	push	hl
   5167 CD A9 5E      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   516A E5            [11]  191 	push	hl
   516B 21 05 05      [10]  192 	ld	hl, #0x0505
   516E E5            [11]  193 	push	hl
   516F CD B6 5D      [17]  194 	call	_cpct_px2byteM0
   5172 55            [ 4]  195 	ld	d, l
   5173 C1            [10]  196 	pop	bc
   5174 21 02 10      [10]  197 	ld	hl, #0x1002
   5177 E5            [11]  198 	push	hl
   5178 D5            [11]  199 	push	de
   5179 33            [ 6]  200 	inc	sp
   517A C5            [11]  201 	push	bc
   517B CD F0 5D      [17]  202 	call	_cpct_drawSolidBox
   517E F1            [10]  203 	pop	af
   517F F1            [10]  204 	pop	af
   5180 33            [ 6]  205 	inc	sp
   5181 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5182                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5182 FD 21 A1 5F   [14]  213 	ld	iy, #_gtilegroundy
   5186 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   5189 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   518A                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   518A FD 21 02 00   [14]  222 	ld	iy, #2
   518E FD 39         [15]  223 	add	iy, sp
   5190 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5193 D6 18         [ 7]  225 	sub	a, #0x18
   5195 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   5198 17            [ 4]  227 	rla
   5199 3F            [ 4]  228 	ccf
   519A 1F            [ 4]  229 	rra
   519B DE 80         [ 7]  230 	sbc	a, #0x80
   519D 38 1A         [12]  231 	jr	C,00102$
   519F 3E 38         [ 7]  232 	ld	a, #0x38
   51A1 FD BE 00      [19]  233 	cp	a, 0 (iy)
   51A4 3E 00         [ 7]  234 	ld	a, #0x00
   51A6 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   51A9 E2 AE 51      [10]  236 	jp	PO, 00114$
   51AC EE 80         [ 7]  237 	xor	a, #0x80
   51AE                     238 00114$:
   51AE FA B9 51      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   51B1 FD 21 A2 5F   [14]  241 	ld	iy, #_gtileplatformy
   51B5 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   51B8 C9            [10]  243 	ret
   51B9                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   51B9 2E FF         [ 7]  246 	ld	l, #0xff
   51BB C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   51BC                     252 _tilemap_is_trap::
   51BC DD E5         [15]  253 	push	ix
   51BE DD 21 00 00   [14]  254 	ld	ix,#0
   51C2 DD 39         [15]  255 	add	ix,sp
   51C4 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   51C5 DD 4E 04      [19]  258 	ld	c,4 (ix)
   51C8 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   51CB DD 6E 08      [19]  261 	ld	l, 8 (ix)
   51CE 26 00         [ 7]  262 	ld	h, #0x00
   51D0 09            [11]  263 	add	hl, bc
   51D1 33            [ 6]  264 	inc	sp
   51D2 33            [ 6]  265 	inc	sp
   51D3 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   51D4 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   51D7 16 00         [ 7]  269 	ld	d, #0x00
   51D9 DD 6E 06      [19]  270 	ld	l,6 (ix)
   51DC DD 66 07      [19]  271 	ld	h,7 (ix)
   51DF 19            [11]  272 	add	hl, de
   51E0 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   51E1 FD 21 A1 5F   [14]  275 	ld	iy, #_gtilegroundy
   51E5 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   51E8 26 00         [ 7]  277 	ld	h, #0x00
   51EA 2B            [ 6]  278 	dec	hl
   51EB 2B            [ 6]  279 	dec	hl
   51EC 7B            [ 4]  280 	ld	a, e
   51ED 95            [ 4]  281 	sub	a, l
   51EE 7A            [ 4]  282 	ld	a, d
   51EF 9C            [ 4]  283 	sbc	a, h
   51F0 E2 F5 51      [10]  284 	jp	PO, 00119$
   51F3 EE 80         [ 7]  285 	xor	a, #0x80
   51F5                     286 00119$:
   51F5 FA 19 52      [10]  287 	jp	M, 00102$
   51F8 79            [ 4]  288 	ld	a, c
   51F9 D6 48         [ 7]  289 	sub	a, #0x48
   51FB 78            [ 4]  290 	ld	a, b
   51FC 17            [ 4]  291 	rla
   51FD 3F            [ 4]  292 	ccf
   51FE 1F            [ 4]  293 	rra
   51FF DE 80         [ 7]  294 	sbc	a, #0x80
   5201 30 16         [12]  295 	jr	NC,00102$
   5203 3E 38         [ 7]  296 	ld	a, #0x38
   5205 DD BE FE      [19]  297 	cp	a, -2 (ix)
   5208 3E 00         [ 7]  298 	ld	a, #0x00
   520A DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   520D E2 12 52      [10]  300 	jp	PO, 00120$
   5210 EE 80         [ 7]  301 	xor	a, #0x80
   5212                     302 00120$:
   5212 F2 19 52      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   5215 2E 01         [ 7]  305 	ld	l, #0x01
   5217 18 02         [12]  306 	jr	00105$
   5219                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   5219 2E 00         [ 7]  309 	ld	l, #0x00
   521B                     310 00105$:
   521B DD F9         [10]  311 	ld	sp, ix
   521D DD E1         [14]  312 	pop	ix
   521F C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   5220                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   5220 2E 00         [ 7]  320 	ld	l, #0x00
   5222 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   5223                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   5223 2E 00         [ 7]  328 	ld	l, #0x00
   5225 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   5226                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   5226 FD 21 A3 5F   [14]  336 	ld	iy, #_ggoalx
   522A FD 6E 00      [19]  337 	ld	l, 0 (iy)
   522D C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   5FA8                     341 __xinit__gtilegroundy:
   5FA8 A0                  342 	.db #0xa0	; 160
   5FA9                     343 __xinit__gtileplatformy:
   5FA9 80                  344 	.db #0x80	; 128
   5FAA                     345 __xinit__ggoalx:
   5FAA 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
