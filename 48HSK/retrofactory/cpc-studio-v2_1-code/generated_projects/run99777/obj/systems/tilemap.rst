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
   62B3                      33 _gtilegroundy:
   62B3                      34 	.ds 1
   62B4                      35 _gtileplatformy:
   62B4                      36 	.ds 1
   62B5                      37 _ggoalx:
   62B5                      38 	.ds 1
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
   5047                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   5047 2A C2 51      [16]   65 	ld	hl, (_level1tilemapheight)
   504A 3E 02         [ 7]   66 	ld	a, #0x02
   504C BD            [ 4]   67 	cp	a, l
   504D 3E 00         [ 7]   68 	ld	a, #0x00
   504F 9C            [ 4]   69 	sbc	a, h
   5050 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5052 7D            [ 4]   72 	ld	a, l
   5053 C6 FE         [ 7]   73 	add	a, #0xfe
   5055 07            [ 4]   74 	rlca
   5056 07            [ 4]   75 	rlca
   5057 07            [ 4]   76 	rlca
   5058 E6 F8         [ 7]   77 	and	a, #0xf8
   505A 32 B3 62      [13]   78 	ld	(#_gtilegroundy + 0),a
   505D 18 05         [12]   79 	jr	00103$
   505F                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   505F 21 B3 62      [10]   82 	ld	hl,#_gtilegroundy + 0
   5062 36 A0         [10]   83 	ld	(hl), #0xa0
   5064                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5064 21 B4 62      [10]   86 	ld	hl, #_gtileplatformy
   5067 3A B3 62      [13]   87 	ld	a,(#_gtilegroundy + 0)
   506A C6 E8         [ 7]   88 	add	a, #0xe8
   506C 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   506D 21 B5 62      [10]   91 	ld	hl,#_ggoalx + 0
   5070 36 48         [10]   92 	ld	(hl), #0x48
   5072 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5073                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5073 3A B3 62      [13]  100 	ld	a, (_gtilegroundy)
   5076 F5            [11]  101 	push	af
   5077 33            [ 6]  102 	inc	sp
   5078 AF            [ 4]  103 	xor	a, a
   5079 F5            [11]  104 	push	af
   507A 33            [ 6]  105 	inc	sp
   507B 21 00 C0      [10]  106 	ld	hl, #0xc000
   507E E5            [11]  107 	push	hl
   507F CD CB 61      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5082 E5            [11]  110 	push	hl
   5083 21 01 01      [10]  111 	ld	hl, #0x0101
   5086 E5            [11]  112 	push	hl
   5087 CD D8 60      [17]  113 	call	_cpct_px2byteM0
   508A 55            [ 4]  114 	ld	d, l
   508B C1            [10]  115 	pop	bc
   508C 21 50 08      [10]  116 	ld	hl, #0x0850
   508F E5            [11]  117 	push	hl
   5090 D5            [11]  118 	push	de
   5091 33            [ 6]  119 	inc	sp
   5092 C5            [11]  120 	push	bc
   5093 CD 12 61      [17]  121 	call	_cpct_drawSolidBox
   5096 F1            [10]  122 	pop	af
   5097 F1            [10]  123 	pop	af
   5098 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5099 3A B4 62      [13]  126 	ld	a, (_gtileplatformy)
   509C 57            [ 4]  127 	ld	d,a
   509D 1E 18         [ 7]  128 	ld	e,#0x18
   509F D5            [11]  129 	push	de
   50A0 21 00 C0      [10]  130 	ld	hl, #0xc000
   50A3 E5            [11]  131 	push	hl
   50A4 CD CB 61      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   50A7 E5            [11]  134 	push	hl
   50A8 21 02 02      [10]  135 	ld	hl, #0x0202
   50AB E5            [11]  136 	push	hl
   50AC CD D8 60      [17]  137 	call	_cpct_px2byteM0
   50AF 55            [ 4]  138 	ld	d, l
   50B0 C1            [10]  139 	pop	bc
   50B1 21 20 04      [10]  140 	ld	hl, #0x0420
   50B4 E5            [11]  141 	push	hl
   50B5 D5            [11]  142 	push	de
   50B6 33            [ 6]  143 	inc	sp
   50B7 C5            [11]  144 	push	bc
   50B8 CD 12 61      [17]  145 	call	_cpct_drawSolidBox
   50BB F1            [10]  146 	pop	af
   50BC F1            [10]  147 	pop	af
   50BD 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   50BE 21 B3 62      [10]  150 	ld	hl,#_gtilegroundy + 0
   50C1 46            [ 7]  151 	ld	b, (hl)
   50C2 05            [ 4]  152 	dec	b
   50C3 05            [ 4]  153 	dec	b
   50C4 C5            [11]  154 	push	bc
   50C5 33            [ 6]  155 	inc	sp
   50C6 3E 38         [ 7]  156 	ld	a, #0x38
   50C8 F5            [11]  157 	push	af
   50C9 33            [ 6]  158 	inc	sp
   50CA 21 00 C0      [10]  159 	ld	hl, #0xc000
   50CD E5            [11]  160 	push	hl
   50CE CD CB 61      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   50D1 E5            [11]  163 	push	hl
   50D2 21 03 03      [10]  164 	ld	hl, #0x0303
   50D5 E5            [11]  165 	push	hl
   50D6 CD D8 60      [17]  166 	call	_cpct_px2byteM0
   50D9 55            [ 4]  167 	ld	d, l
   50DA C1            [10]  168 	pop	bc
   50DB 21 10 02      [10]  169 	ld	hl, #0x0210
   50DE E5            [11]  170 	push	hl
   50DF D5            [11]  171 	push	de
   50E0 33            [ 6]  172 	inc	sp
   50E1 C5            [11]  173 	push	bc
   50E2 CD 12 61      [17]  174 	call	_cpct_drawSolidBox
   50E5 F1            [10]  175 	pop	af
   50E6 F1            [10]  176 	pop	af
   50E7 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   50E8 3A B3 62      [13]  179 	ld	a,(#_gtilegroundy + 0)
   50EB C6 F0         [ 7]  180 	add	a, #0xf0
   50ED 47            [ 4]  181 	ld	b, a
   50EE C5            [11]  182 	push	bc
   50EF 33            [ 6]  183 	inc	sp
   50F0 3A B5 62      [13]  184 	ld	a, (_ggoalx)
   50F3 F5            [11]  185 	push	af
   50F4 33            [ 6]  186 	inc	sp
   50F5 21 00 C0      [10]  187 	ld	hl, #0xc000
   50F8 E5            [11]  188 	push	hl
   50F9 CD CB 61      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   50FC E5            [11]  191 	push	hl
   50FD 21 05 05      [10]  192 	ld	hl, #0x0505
   5100 E5            [11]  193 	push	hl
   5101 CD D8 60      [17]  194 	call	_cpct_px2byteM0
   5104 55            [ 4]  195 	ld	d, l
   5105 C1            [10]  196 	pop	bc
   5106 21 02 10      [10]  197 	ld	hl, #0x1002
   5109 E5            [11]  198 	push	hl
   510A D5            [11]  199 	push	de
   510B 33            [ 6]  200 	inc	sp
   510C C5            [11]  201 	push	bc
   510D CD 12 61      [17]  202 	call	_cpct_drawSolidBox
   5110 F1            [10]  203 	pop	af
   5111 F1            [10]  204 	pop	af
   5112 33            [ 6]  205 	inc	sp
   5113 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5114                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5114 FD 21 B3 62   [14]  213 	ld	iy, #_gtilegroundy
   5118 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   511B C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   511C                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   511C FD 21 02 00   [14]  222 	ld	iy, #2
   5120 FD 39         [15]  223 	add	iy, sp
   5122 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5125 D6 18         [ 7]  225 	sub	a, #0x18
   5127 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   512A 17            [ 4]  227 	rla
   512B 3F            [ 4]  228 	ccf
   512C 1F            [ 4]  229 	rra
   512D DE 80         [ 7]  230 	sbc	a, #0x80
   512F 38 1A         [12]  231 	jr	C,00102$
   5131 3E 38         [ 7]  232 	ld	a, #0x38
   5133 FD BE 00      [19]  233 	cp	a, 0 (iy)
   5136 3E 00         [ 7]  234 	ld	a, #0x00
   5138 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   513B E2 40 51      [10]  236 	jp	PO, 00114$
   513E EE 80         [ 7]  237 	xor	a, #0x80
   5140                     238 00114$:
   5140 FA 4B 51      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5143 FD 21 B4 62   [14]  241 	ld	iy, #_gtileplatformy
   5147 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   514A C9            [10]  243 	ret
   514B                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   514B 2E FF         [ 7]  246 	ld	l, #0xff
   514D C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   514E                     252 _tilemap_is_trap::
   514E DD E5         [15]  253 	push	ix
   5150 DD 21 00 00   [14]  254 	ld	ix,#0
   5154 DD 39         [15]  255 	add	ix,sp
   5156 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   5157 DD 4E 04      [19]  258 	ld	c,4 (ix)
   515A DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   515D DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5160 26 00         [ 7]  262 	ld	h, #0x00
   5162 09            [11]  263 	add	hl, bc
   5163 33            [ 6]  264 	inc	sp
   5164 33            [ 6]  265 	inc	sp
   5165 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5166 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5169 16 00         [ 7]  269 	ld	d, #0x00
   516B DD 6E 06      [19]  270 	ld	l,6 (ix)
   516E DD 66 07      [19]  271 	ld	h,7 (ix)
   5171 19            [11]  272 	add	hl, de
   5172 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5173 FD 21 B3 62   [14]  275 	ld	iy, #_gtilegroundy
   5177 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   517A 26 00         [ 7]  277 	ld	h, #0x00
   517C 2B            [ 6]  278 	dec	hl
   517D 2B            [ 6]  279 	dec	hl
   517E 7B            [ 4]  280 	ld	a, e
   517F 95            [ 4]  281 	sub	a, l
   5180 7A            [ 4]  282 	ld	a, d
   5181 9C            [ 4]  283 	sbc	a, h
   5182 E2 87 51      [10]  284 	jp	PO, 00119$
   5185 EE 80         [ 7]  285 	xor	a, #0x80
   5187                     286 00119$:
   5187 FA AB 51      [10]  287 	jp	M, 00102$
   518A 79            [ 4]  288 	ld	a, c
   518B D6 48         [ 7]  289 	sub	a, #0x48
   518D 78            [ 4]  290 	ld	a, b
   518E 17            [ 4]  291 	rla
   518F 3F            [ 4]  292 	ccf
   5190 1F            [ 4]  293 	rra
   5191 DE 80         [ 7]  294 	sbc	a, #0x80
   5193 30 16         [12]  295 	jr	NC,00102$
   5195 3E 38         [ 7]  296 	ld	a, #0x38
   5197 DD BE FE      [19]  297 	cp	a, -2 (ix)
   519A 3E 00         [ 7]  298 	ld	a, #0x00
   519C DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   519F E2 A4 51      [10]  300 	jp	PO, 00120$
   51A2 EE 80         [ 7]  301 	xor	a, #0x80
   51A4                     302 00120$:
   51A4 F2 AB 51      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   51A7 2E 01         [ 7]  305 	ld	l, #0x01
   51A9 18 02         [12]  306 	jr	00105$
   51AB                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   51AB 2E 00         [ 7]  309 	ld	l, #0x00
   51AD                     310 00105$:
   51AD DD F9         [10]  311 	ld	sp, ix
   51AF DD E1         [14]  312 	pop	ix
   51B1 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   51B2                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   51B2 2E 00         [ 7]  320 	ld	l, #0x00
   51B4 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   51B5                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   51B5 2E 00         [ 7]  328 	ld	l, #0x00
   51B7 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   51B8                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   51B8 FD 21 B5 62   [14]  336 	ld	iy, #_ggoalx
   51BC FD 6E 00      [19]  337 	ld	l, 0 (iy)
   51BF C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   62BA                     341 __xinit__gtilegroundy:
   62BA A0                  342 	.db #0xa0	; 160
   62BB                     343 __xinit__gtileplatformy:
   62BB 80                  344 	.db #0x80	; 128
   62BC                     345 __xinit__ggoalx:
   62BC 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
