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
   5F1A                      33 _gtilegroundy:
   5F1A                      34 	.ds 1
   5F1B                      35 _gtileplatformy:
   5F1B                      36 	.ds 1
   5F1C                      37 _ggoalx:
   5F1C                      38 	.ds 1
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
   502A                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   502A 2A A5 51      [16]   65 	ld	hl, (_level1tilemapheight)
   502D 3E 02         [ 7]   66 	ld	a, #0x02
   502F BD            [ 4]   67 	cp	a, l
   5030 3E 00         [ 7]   68 	ld	a, #0x00
   5032 9C            [ 4]   69 	sbc	a, h
   5033 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5035 7D            [ 4]   72 	ld	a, l
   5036 C6 FE         [ 7]   73 	add	a, #0xfe
   5038 07            [ 4]   74 	rlca
   5039 07            [ 4]   75 	rlca
   503A 07            [ 4]   76 	rlca
   503B E6 F8         [ 7]   77 	and	a, #0xf8
   503D 32 1A 5F      [13]   78 	ld	(#_gtilegroundy + 0),a
   5040 18 05         [12]   79 	jr	00103$
   5042                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5042 21 1A 5F      [10]   82 	ld	hl,#_gtilegroundy + 0
   5045 36 A0         [10]   83 	ld	(hl), #0xa0
   5047                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5047 21 1B 5F      [10]   86 	ld	hl, #_gtileplatformy
   504A 3A 1A 5F      [13]   87 	ld	a,(#_gtilegroundy + 0)
   504D C6 E8         [ 7]   88 	add	a, #0xe8
   504F 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5050 21 1C 5F      [10]   91 	ld	hl,#_ggoalx + 0
   5053 36 48         [10]   92 	ld	(hl), #0x48
   5055 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5056                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5056 3A 1A 5F      [13]  100 	ld	a, (_gtilegroundy)
   5059 F5            [11]  101 	push	af
   505A 33            [ 6]  102 	inc	sp
   505B AF            [ 4]  103 	xor	a, a
   505C F5            [11]  104 	push	af
   505D 33            [ 6]  105 	inc	sp
   505E 21 00 C0      [10]  106 	ld	hl, #0xc000
   5061 E5            [11]  107 	push	hl
   5062 CD 39 5E      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   5065 E5            [11]  110 	push	hl
   5066 21 01 01      [10]  111 	ld	hl, #0x0101
   5069 E5            [11]  112 	push	hl
   506A CD 46 5D      [17]  113 	call	_cpct_px2byteM0
   506D 55            [ 4]  114 	ld	d, l
   506E C1            [10]  115 	pop	bc
   506F 21 50 08      [10]  116 	ld	hl, #0x0850
   5072 E5            [11]  117 	push	hl
   5073 D5            [11]  118 	push	de
   5074 33            [ 6]  119 	inc	sp
   5075 C5            [11]  120 	push	bc
   5076 CD 80 5D      [17]  121 	call	_cpct_drawSolidBox
   5079 F1            [10]  122 	pop	af
   507A F1            [10]  123 	pop	af
   507B 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   507C 3A 1B 5F      [13]  126 	ld	a, (_gtileplatformy)
   507F 57            [ 4]  127 	ld	d,a
   5080 1E 18         [ 7]  128 	ld	e,#0x18
   5082 D5            [11]  129 	push	de
   5083 21 00 C0      [10]  130 	ld	hl, #0xc000
   5086 E5            [11]  131 	push	hl
   5087 CD 39 5E      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   508A E5            [11]  134 	push	hl
   508B 21 02 02      [10]  135 	ld	hl, #0x0202
   508E E5            [11]  136 	push	hl
   508F CD 46 5D      [17]  137 	call	_cpct_px2byteM0
   5092 55            [ 4]  138 	ld	d, l
   5093 C1            [10]  139 	pop	bc
   5094 21 20 04      [10]  140 	ld	hl, #0x0420
   5097 E5            [11]  141 	push	hl
   5098 D5            [11]  142 	push	de
   5099 33            [ 6]  143 	inc	sp
   509A C5            [11]  144 	push	bc
   509B CD 80 5D      [17]  145 	call	_cpct_drawSolidBox
   509E F1            [10]  146 	pop	af
   509F F1            [10]  147 	pop	af
   50A0 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   50A1 21 1A 5F      [10]  150 	ld	hl,#_gtilegroundy + 0
   50A4 46            [ 7]  151 	ld	b, (hl)
   50A5 05            [ 4]  152 	dec	b
   50A6 05            [ 4]  153 	dec	b
   50A7 C5            [11]  154 	push	bc
   50A8 33            [ 6]  155 	inc	sp
   50A9 3E 38         [ 7]  156 	ld	a, #0x38
   50AB F5            [11]  157 	push	af
   50AC 33            [ 6]  158 	inc	sp
   50AD 21 00 C0      [10]  159 	ld	hl, #0xc000
   50B0 E5            [11]  160 	push	hl
   50B1 CD 39 5E      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   50B4 E5            [11]  163 	push	hl
   50B5 21 03 03      [10]  164 	ld	hl, #0x0303
   50B8 E5            [11]  165 	push	hl
   50B9 CD 46 5D      [17]  166 	call	_cpct_px2byteM0
   50BC 55            [ 4]  167 	ld	d, l
   50BD C1            [10]  168 	pop	bc
   50BE 21 10 02      [10]  169 	ld	hl, #0x0210
   50C1 E5            [11]  170 	push	hl
   50C2 D5            [11]  171 	push	de
   50C3 33            [ 6]  172 	inc	sp
   50C4 C5            [11]  173 	push	bc
   50C5 CD 80 5D      [17]  174 	call	_cpct_drawSolidBox
   50C8 F1            [10]  175 	pop	af
   50C9 F1            [10]  176 	pop	af
   50CA 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   50CB 3A 1A 5F      [13]  179 	ld	a,(#_gtilegroundy + 0)
   50CE C6 F0         [ 7]  180 	add	a, #0xf0
   50D0 47            [ 4]  181 	ld	b, a
   50D1 C5            [11]  182 	push	bc
   50D2 33            [ 6]  183 	inc	sp
   50D3 3A 1C 5F      [13]  184 	ld	a, (_ggoalx)
   50D6 F5            [11]  185 	push	af
   50D7 33            [ 6]  186 	inc	sp
   50D8 21 00 C0      [10]  187 	ld	hl, #0xc000
   50DB E5            [11]  188 	push	hl
   50DC CD 39 5E      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   50DF E5            [11]  191 	push	hl
   50E0 21 05 05      [10]  192 	ld	hl, #0x0505
   50E3 E5            [11]  193 	push	hl
   50E4 CD 46 5D      [17]  194 	call	_cpct_px2byteM0
   50E7 55            [ 4]  195 	ld	d, l
   50E8 C1            [10]  196 	pop	bc
   50E9 21 02 10      [10]  197 	ld	hl, #0x1002
   50EC E5            [11]  198 	push	hl
   50ED D5            [11]  199 	push	de
   50EE 33            [ 6]  200 	inc	sp
   50EF C5            [11]  201 	push	bc
   50F0 CD 80 5D      [17]  202 	call	_cpct_drawSolidBox
   50F3 F1            [10]  203 	pop	af
   50F4 F1            [10]  204 	pop	af
   50F5 33            [ 6]  205 	inc	sp
   50F6 C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   50F7                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   50F7 FD 21 1A 5F   [14]  213 	ld	iy, #_gtilegroundy
   50FB FD 6E 00      [19]  214 	ld	l, 0 (iy)
   50FE C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   50FF                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   50FF FD 21 02 00   [14]  222 	ld	iy, #2
   5103 FD 39         [15]  223 	add	iy, sp
   5105 FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5108 D6 18         [ 7]  225 	sub	a, #0x18
   510A FD 7E 01      [19]  226 	ld	a, 1 (iy)
   510D 17            [ 4]  227 	rla
   510E 3F            [ 4]  228 	ccf
   510F 1F            [ 4]  229 	rra
   5110 DE 80         [ 7]  230 	sbc	a, #0x80
   5112 38 1A         [12]  231 	jr	C,00102$
   5114 3E 38         [ 7]  232 	ld	a, #0x38
   5116 FD BE 00      [19]  233 	cp	a, 0 (iy)
   5119 3E 00         [ 7]  234 	ld	a, #0x00
   511B FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   511E E2 23 51      [10]  236 	jp	PO, 00114$
   5121 EE 80         [ 7]  237 	xor	a, #0x80
   5123                     238 00114$:
   5123 FA 2E 51      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   5126 FD 21 1B 5F   [14]  241 	ld	iy, #_gtileplatformy
   512A FD 6E 00      [19]  242 	ld	l, 0 (iy)
   512D C9            [10]  243 	ret
   512E                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   512E 2E FF         [ 7]  246 	ld	l, #0xff
   5130 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   5131                     252 _tilemap_is_trap::
   5131 DD E5         [15]  253 	push	ix
   5133 DD 21 00 00   [14]  254 	ld	ix,#0
   5137 DD 39         [15]  255 	add	ix,sp
   5139 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   513A DD 4E 04      [19]  258 	ld	c,4 (ix)
   513D DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5140 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   5143 26 00         [ 7]  262 	ld	h, #0x00
   5145 09            [11]  263 	add	hl, bc
   5146 33            [ 6]  264 	inc	sp
   5147 33            [ 6]  265 	inc	sp
   5148 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5149 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   514C 16 00         [ 7]  269 	ld	d, #0x00
   514E DD 6E 06      [19]  270 	ld	l,6 (ix)
   5151 DD 66 07      [19]  271 	ld	h,7 (ix)
   5154 19            [11]  272 	add	hl, de
   5155 EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5156 FD 21 1A 5F   [14]  275 	ld	iy, #_gtilegroundy
   515A FD 6E 00      [19]  276 	ld	l, 0 (iy)
   515D 26 00         [ 7]  277 	ld	h, #0x00
   515F 2B            [ 6]  278 	dec	hl
   5160 2B            [ 6]  279 	dec	hl
   5161 7B            [ 4]  280 	ld	a, e
   5162 95            [ 4]  281 	sub	a, l
   5163 7A            [ 4]  282 	ld	a, d
   5164 9C            [ 4]  283 	sbc	a, h
   5165 E2 6A 51      [10]  284 	jp	PO, 00119$
   5168 EE 80         [ 7]  285 	xor	a, #0x80
   516A                     286 00119$:
   516A FA 8E 51      [10]  287 	jp	M, 00102$
   516D 79            [ 4]  288 	ld	a, c
   516E D6 48         [ 7]  289 	sub	a, #0x48
   5170 78            [ 4]  290 	ld	a, b
   5171 17            [ 4]  291 	rla
   5172 3F            [ 4]  292 	ccf
   5173 1F            [ 4]  293 	rra
   5174 DE 80         [ 7]  294 	sbc	a, #0x80
   5176 30 16         [12]  295 	jr	NC,00102$
   5178 3E 38         [ 7]  296 	ld	a, #0x38
   517A DD BE FE      [19]  297 	cp	a, -2 (ix)
   517D 3E 00         [ 7]  298 	ld	a, #0x00
   517F DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5182 E2 87 51      [10]  300 	jp	PO, 00120$
   5185 EE 80         [ 7]  301 	xor	a, #0x80
   5187                     302 00120$:
   5187 F2 8E 51      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   518A 2E 01         [ 7]  305 	ld	l, #0x01
   518C 18 02         [12]  306 	jr	00105$
   518E                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   518E 2E 00         [ 7]  309 	ld	l, #0x00
   5190                     310 00105$:
   5190 DD F9         [10]  311 	ld	sp, ix
   5192 DD E1         [14]  312 	pop	ix
   5194 C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   5195                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   5195 2E 00         [ 7]  320 	ld	l, #0x00
   5197 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   5198                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   5198 2E 00         [ 7]  328 	ld	l, #0x00
   519A C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   519B                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   519B FD 21 1C 5F   [14]  336 	ld	iy, #_ggoalx
   519F FD 6E 00      [19]  337 	ld	l, 0 (iy)
   51A2 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   5F21                     341 __xinit__gtilegroundy:
   5F21 A0                  342 	.db #0xa0	; 160
   5F22                     343 __xinit__gtileplatformy:
   5F22 80                  344 	.db #0x80	; 128
   5F23                     345 __xinit__ggoalx:
   5F23 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
