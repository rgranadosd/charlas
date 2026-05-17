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
   5F34                      33 _gtilegroundy:
   5F34                      34 	.ds 1
   5F35                      35 _gtileplatformy:
   5F35                      36 	.ds 1
   5F36                      37 _ggoalx:
   5F36                      38 	.ds 1
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
   5037                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   5037 2A B2 51      [16]   65 	ld	hl, (_level1tilemapheight)
   503A 3E 02         [ 7]   66 	ld	a, #0x02
   503C BD            [ 4]   67 	cp	a, l
   503D 3E 00         [ 7]   68 	ld	a, #0x00
   503F 9C            [ 4]   69 	sbc	a, h
   5040 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5042 7D            [ 4]   72 	ld	a, l
   5043 C6 FE         [ 7]   73 	add	a, #0xfe
   5045 07            [ 4]   74 	rlca
   5046 07            [ 4]   75 	rlca
   5047 07            [ 4]   76 	rlca
   5048 E6 F8         [ 7]   77 	and	a, #0xf8
   504A 32 34 5F      [13]   78 	ld	(#_gtilegroundy + 0),a
   504D 18 05         [12]   79 	jr	00103$
   504F                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   504F 21 34 5F      [10]   82 	ld	hl,#_gtilegroundy + 0
   5052 36 A0         [10]   83 	ld	(hl), #0xa0
   5054                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5054 21 35 5F      [10]   86 	ld	hl, #_gtileplatformy
   5057 3A 34 5F      [13]   87 	ld	a,(#_gtilegroundy + 0)
   505A C6 E8         [ 7]   88 	add	a, #0xe8
   505C 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   505D 21 36 5F      [10]   91 	ld	hl,#_ggoalx + 0
   5060 36 48         [10]   92 	ld	(hl), #0x48
   5062 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5063                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5063 3A 34 5F      [13]  100 	ld	a, (_gtilegroundy)
   5066 F5            [11]  101 	push	af
   5067 33            [ 6]  102 	inc	sp
   5068 AF            [ 4]  103 	xor	a, a
   5069 F5            [11]  104 	push	af
   506A 33            [ 6]  105 	inc	sp
   506B 21 00 C0      [10]  106 	ld	hl, #0xc000
   506E E5            [11]  107 	push	hl
   506F CD 53 5E      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5072 E5            [11]  110 	push	hl
   5073 21 01 01      [10]  111 	ld	hl, #0x0101
   5076 E5            [11]  112 	push	hl
   5077 CD 60 5D      [17]  113 	call	_cpct_px2byteM0
   507A 55            [ 4]  114 	ld	d, l
   507B C1            [10]  115 	pop	bc
   507C 21 50 08      [10]  116 	ld	hl, #0x0850
   507F E5            [11]  117 	push	hl
   5080 D5            [11]  118 	push	de
   5081 33            [ 6]  119 	inc	sp
   5082 C5            [11]  120 	push	bc
   5083 CD 9A 5D      [17]  121 	call	_cpct_drawSolidBox
   5086 F1            [10]  122 	pop	af
   5087 F1            [10]  123 	pop	af
   5088 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5089 3A 35 5F      [13]  126 	ld	a, (_gtileplatformy)
   508C 57            [ 4]  127 	ld	d,a
   508D 1E 18         [ 7]  128 	ld	e,#0x18
   508F D5            [11]  129 	push	de
   5090 21 00 C0      [10]  130 	ld	hl, #0xc000
   5093 E5            [11]  131 	push	hl
   5094 CD 53 5E      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   5097 E5            [11]  134 	push	hl
   5098 21 02 02      [10]  135 	ld	hl, #0x0202
   509B E5            [11]  136 	push	hl
   509C CD 60 5D      [17]  137 	call	_cpct_px2byteM0
   509F 55            [ 4]  138 	ld	d, l
   50A0 C1            [10]  139 	pop	bc
   50A1 21 20 04      [10]  140 	ld	hl, #0x0420
   50A4 E5            [11]  141 	push	hl
   50A5 D5            [11]  142 	push	de
   50A6 33            [ 6]  143 	inc	sp
   50A7 C5            [11]  144 	push	bc
   50A8 CD 9A 5D      [17]  145 	call	_cpct_drawSolidBox
   50AB F1            [10]  146 	pop	af
   50AC F1            [10]  147 	pop	af
   50AD 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   50AE 21 34 5F      [10]  150 	ld	hl,#_gtilegroundy + 0
   50B1 46            [ 7]  151 	ld	b, (hl)
   50B2 05            [ 4]  152 	dec	b
   50B3 05            [ 4]  153 	dec	b
   50B4 C5            [11]  154 	push	bc
   50B5 33            [ 6]  155 	inc	sp
   50B6 3E 38         [ 7]  156 	ld	a, #0x38
   50B8 F5            [11]  157 	push	af
   50B9 33            [ 6]  158 	inc	sp
   50BA 21 00 C0      [10]  159 	ld	hl, #0xc000
   50BD E5            [11]  160 	push	hl
   50BE CD 53 5E      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   50C1 E5            [11]  163 	push	hl
   50C2 21 03 03      [10]  164 	ld	hl, #0x0303
   50C5 E5            [11]  165 	push	hl
   50C6 CD 60 5D      [17]  166 	call	_cpct_px2byteM0
   50C9 55            [ 4]  167 	ld	d, l
   50CA C1            [10]  168 	pop	bc
   50CB 21 10 02      [10]  169 	ld	hl, #0x0210
   50CE E5            [11]  170 	push	hl
   50CF D5            [11]  171 	push	de
   50D0 33            [ 6]  172 	inc	sp
   50D1 C5            [11]  173 	push	bc
   50D2 CD 9A 5D      [17]  174 	call	_cpct_drawSolidBox
   50D5 F1            [10]  175 	pop	af
   50D6 F1            [10]  176 	pop	af
   50D7 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   50D8 3A 34 5F      [13]  179 	ld	a,(#_gtilegroundy + 0)
   50DB C6 F0         [ 7]  180 	add	a, #0xf0
   50DD 47            [ 4]  181 	ld	b, a
   50DE C5            [11]  182 	push	bc
   50DF 33            [ 6]  183 	inc	sp
   50E0 3A 36 5F      [13]  184 	ld	a, (_ggoalx)
   50E3 F5            [11]  185 	push	af
   50E4 33            [ 6]  186 	inc	sp
   50E5 21 00 C0      [10]  187 	ld	hl, #0xc000
   50E8 E5            [11]  188 	push	hl
   50E9 CD 53 5E      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   50EC E5            [11]  191 	push	hl
   50ED 21 05 05      [10]  192 	ld	hl, #0x0505
   50F0 E5            [11]  193 	push	hl
   50F1 CD 60 5D      [17]  194 	call	_cpct_px2byteM0
   50F4 55            [ 4]  195 	ld	d, l
   50F5 C1            [10]  196 	pop	bc
   50F6 21 02 10      [10]  197 	ld	hl, #0x1002
   50F9 E5            [11]  198 	push	hl
   50FA D5            [11]  199 	push	de
   50FB 33            [ 6]  200 	inc	sp
   50FC C5            [11]  201 	push	bc
   50FD CD 9A 5D      [17]  202 	call	_cpct_drawSolidBox
   5100 F1            [10]  203 	pop	af
   5101 F1            [10]  204 	pop	af
   5102 33            [ 6]  205 	inc	sp
   5103 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5104                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5104 FD 21 34 5F   [14]  213 	ld	iy, #_gtilegroundy
   5108 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   510B C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   510C                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   510C FD 21 02 00   [14]  222 	ld	iy, #2
   5110 FD 39         [15]  223 	add	iy, sp
   5112 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5115 D6 18         [ 7]  225 	sub	a, #0x18
   5117 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   511A 17            [ 4]  227 	rla
   511B 3F            [ 4]  228 	ccf
   511C 1F            [ 4]  229 	rra
   511D DE 80         [ 7]  230 	sbc	a, #0x80
   511F 38 1A         [12]  231 	jr	C,00102$
   5121 3E 38         [ 7]  232 	ld	a, #0x38
   5123 FD BE 00      [19]  233 	cp	a, 0 (iy)
   5126 3E 00         [ 7]  234 	ld	a, #0x00
   5128 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   512B E2 30 51      [10]  236 	jp	PO, 00114$
   512E EE 80         [ 7]  237 	xor	a, #0x80
   5130                     238 00114$:
   5130 FA 3B 51      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5133 FD 21 35 5F   [14]  241 	ld	iy, #_gtileplatformy
   5137 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   513A C9            [10]  243 	ret
   513B                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   513B 2E FF         [ 7]  246 	ld	l, #0xff
   513D C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   513E                     252 _tilemap_is_trap::
   513E DD E5         [15]  253 	push	ix
   5140 DD 21 00 00   [14]  254 	ld	ix,#0
   5144 DD 39         [15]  255 	add	ix,sp
   5146 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   5147 DD 4E 04      [19]  258 	ld	c,4 (ix)
   514A DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   514D DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5150 26 00         [ 7]  262 	ld	h, #0x00
   5152 09            [11]  263 	add	hl, bc
   5153 33            [ 6]  264 	inc	sp
   5154 33            [ 6]  265 	inc	sp
   5155 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5156 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5159 16 00         [ 7]  269 	ld	d, #0x00
   515B DD 6E 06      [19]  270 	ld	l,6 (ix)
   515E DD 66 07      [19]  271 	ld	h,7 (ix)
   5161 19            [11]  272 	add	hl, de
   5162 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5163 FD 21 34 5F   [14]  275 	ld	iy, #_gtilegroundy
   5167 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   516A 26 00         [ 7]  277 	ld	h, #0x00
   516C 2B            [ 6]  278 	dec	hl
   516D 2B            [ 6]  279 	dec	hl
   516E 7B            [ 4]  280 	ld	a, e
   516F 95            [ 4]  281 	sub	a, l
   5170 7A            [ 4]  282 	ld	a, d
   5171 9C            [ 4]  283 	sbc	a, h
   5172 E2 77 51      [10]  284 	jp	PO, 00119$
   5175 EE 80         [ 7]  285 	xor	a, #0x80
   5177                     286 00119$:
   5177 FA 9B 51      [10]  287 	jp	M, 00102$
   517A 79            [ 4]  288 	ld	a, c
   517B D6 48         [ 7]  289 	sub	a, #0x48
   517D 78            [ 4]  290 	ld	a, b
   517E 17            [ 4]  291 	rla
   517F 3F            [ 4]  292 	ccf
   5180 1F            [ 4]  293 	rra
   5181 DE 80         [ 7]  294 	sbc	a, #0x80
   5183 30 16         [12]  295 	jr	NC,00102$
   5185 3E 38         [ 7]  296 	ld	a, #0x38
   5187 DD BE FE      [19]  297 	cp	a, -2 (ix)
   518A 3E 00         [ 7]  298 	ld	a, #0x00
   518C DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   518F E2 94 51      [10]  300 	jp	PO, 00120$
   5192 EE 80         [ 7]  301 	xor	a, #0x80
   5194                     302 00120$:
   5194 F2 9B 51      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   5197 2E 01         [ 7]  305 	ld	l, #0x01
   5199 18 02         [12]  306 	jr	00105$
   519B                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   519B 2E 00         [ 7]  309 	ld	l, #0x00
   519D                     310 00105$:
   519D DD F9         [10]  311 	ld	sp, ix
   519F DD E1         [14]  312 	pop	ix
   51A1 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   51A2                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   51A2 2E 00         [ 7]  320 	ld	l, #0x00
   51A4 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   51A5                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   51A5 2E 00         [ 7]  328 	ld	l, #0x00
   51A7 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   51A8                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   51A8 FD 21 36 5F   [14]  336 	ld	iy, #_ggoalx
   51AC FD 6E 00      [19]  337 	ld	l, 0 (iy)
   51AF C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   5F3B                     341 __xinit__gtilegroundy:
   5F3B A0                  342 	.db #0xa0	; 160
   5F3C                     343 __xinit__gtileplatformy:
   5F3C 80                  344 	.db #0x80	; 128
   5F3D                     345 __xinit__ggoalx:
   5F3D 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
