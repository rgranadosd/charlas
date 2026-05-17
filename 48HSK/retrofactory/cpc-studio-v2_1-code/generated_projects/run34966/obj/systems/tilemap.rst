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
   5F5F                      33 _gtilegroundy:
   5F5F                      34 	.ds 1
   5F60                      35 _gtileplatformy:
   5F60                      36 	.ds 1
   5F61                      37 _ggoalx:
   5F61                      38 	.ds 1
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
   5043                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   5043 2A BE 51      [16]   65 	ld	hl, (_level1tilemapheight)
   5046 3E 02         [ 7]   66 	ld	a, #0x02
   5048 BD            [ 4]   67 	cp	a, l
   5049 3E 00         [ 7]   68 	ld	a, #0x00
   504B 9C            [ 4]   69 	sbc	a, h
   504C 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   504E 7D            [ 4]   72 	ld	a, l
   504F C6 FE         [ 7]   73 	add	a, #0xfe
   5051 07            [ 4]   74 	rlca
   5052 07            [ 4]   75 	rlca
   5053 07            [ 4]   76 	rlca
   5054 E6 F8         [ 7]   77 	and	a, #0xf8
   5056 32 5F 5F      [13]   78 	ld	(#_gtilegroundy + 0),a
   5059 18 05         [12]   79 	jr	00103$
   505B                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   505B 21 5F 5F      [10]   82 	ld	hl,#_gtilegroundy + 0
   505E 36 A0         [10]   83 	ld	(hl), #0xa0
   5060                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5060 21 60 5F      [10]   86 	ld	hl, #_gtileplatformy
   5063 3A 5F 5F      [13]   87 	ld	a,(#_gtilegroundy + 0)
   5066 C6 E8         [ 7]   88 	add	a, #0xe8
   5068 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5069 21 61 5F      [10]   91 	ld	hl,#_ggoalx + 0
   506C 36 48         [10]   92 	ld	(hl), #0x48
   506E C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   506F                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   506F 3A 5F 5F      [13]  100 	ld	a, (_gtilegroundy)
   5072 F5            [11]  101 	push	af
   5073 33            [ 6]  102 	inc	sp
   5074 AF            [ 4]  103 	xor	a, a
   5075 F5            [11]  104 	push	af
   5076 33            [ 6]  105 	inc	sp
   5077 21 00 C0      [10]  106 	ld	hl, #0xc000
   507A E5            [11]  107 	push	hl
   507B CD 7E 5E      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   507E E5            [11]  110 	push	hl
   507F 21 01 01      [10]  111 	ld	hl, #0x0101
   5082 E5            [11]  112 	push	hl
   5083 CD 8B 5D      [17]  113 	call	_cpct_px2byteM0
   5086 55            [ 4]  114 	ld	d, l
   5087 C1            [10]  115 	pop	bc
   5088 21 50 08      [10]  116 	ld	hl, #0x0850
   508B E5            [11]  117 	push	hl
   508C D5            [11]  118 	push	de
   508D 33            [ 6]  119 	inc	sp
   508E C5            [11]  120 	push	bc
   508F CD C5 5D      [17]  121 	call	_cpct_drawSolidBox
   5092 F1            [10]  122 	pop	af
   5093 F1            [10]  123 	pop	af
   5094 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5095 3A 60 5F      [13]  126 	ld	a, (_gtileplatformy)
   5098 57            [ 4]  127 	ld	d,a
   5099 1E 18         [ 7]  128 	ld	e,#0x18
   509B D5            [11]  129 	push	de
   509C 21 00 C0      [10]  130 	ld	hl, #0xc000
   509F E5            [11]  131 	push	hl
   50A0 CD 7E 5E      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   50A3 E5            [11]  134 	push	hl
   50A4 21 02 02      [10]  135 	ld	hl, #0x0202
   50A7 E5            [11]  136 	push	hl
   50A8 CD 8B 5D      [17]  137 	call	_cpct_px2byteM0
   50AB 55            [ 4]  138 	ld	d, l
   50AC C1            [10]  139 	pop	bc
   50AD 21 20 04      [10]  140 	ld	hl, #0x0420
   50B0 E5            [11]  141 	push	hl
   50B1 D5            [11]  142 	push	de
   50B2 33            [ 6]  143 	inc	sp
   50B3 C5            [11]  144 	push	bc
   50B4 CD C5 5D      [17]  145 	call	_cpct_drawSolidBox
   50B7 F1            [10]  146 	pop	af
   50B8 F1            [10]  147 	pop	af
   50B9 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   50BA 21 5F 5F      [10]  150 	ld	hl,#_gtilegroundy + 0
   50BD 46            [ 7]  151 	ld	b, (hl)
   50BE 05            [ 4]  152 	dec	b
   50BF 05            [ 4]  153 	dec	b
   50C0 C5            [11]  154 	push	bc
   50C1 33            [ 6]  155 	inc	sp
   50C2 3E 38         [ 7]  156 	ld	a, #0x38
   50C4 F5            [11]  157 	push	af
   50C5 33            [ 6]  158 	inc	sp
   50C6 21 00 C0      [10]  159 	ld	hl, #0xc000
   50C9 E5            [11]  160 	push	hl
   50CA CD 7E 5E      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   50CD E5            [11]  163 	push	hl
   50CE 21 03 03      [10]  164 	ld	hl, #0x0303
   50D1 E5            [11]  165 	push	hl
   50D2 CD 8B 5D      [17]  166 	call	_cpct_px2byteM0
   50D5 55            [ 4]  167 	ld	d, l
   50D6 C1            [10]  168 	pop	bc
   50D7 21 10 02      [10]  169 	ld	hl, #0x0210
   50DA E5            [11]  170 	push	hl
   50DB D5            [11]  171 	push	de
   50DC 33            [ 6]  172 	inc	sp
   50DD C5            [11]  173 	push	bc
   50DE CD C5 5D      [17]  174 	call	_cpct_drawSolidBox
   50E1 F1            [10]  175 	pop	af
   50E2 F1            [10]  176 	pop	af
   50E3 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   50E4 3A 5F 5F      [13]  179 	ld	a,(#_gtilegroundy + 0)
   50E7 C6 F0         [ 7]  180 	add	a, #0xf0
   50E9 47            [ 4]  181 	ld	b, a
   50EA C5            [11]  182 	push	bc
   50EB 33            [ 6]  183 	inc	sp
   50EC 3A 61 5F      [13]  184 	ld	a, (_ggoalx)
   50EF F5            [11]  185 	push	af
   50F0 33            [ 6]  186 	inc	sp
   50F1 21 00 C0      [10]  187 	ld	hl, #0xc000
   50F4 E5            [11]  188 	push	hl
   50F5 CD 7E 5E      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   50F8 E5            [11]  191 	push	hl
   50F9 21 05 05      [10]  192 	ld	hl, #0x0505
   50FC E5            [11]  193 	push	hl
   50FD CD 8B 5D      [17]  194 	call	_cpct_px2byteM0
   5100 55            [ 4]  195 	ld	d, l
   5101 C1            [10]  196 	pop	bc
   5102 21 02 10      [10]  197 	ld	hl, #0x1002
   5105 E5            [11]  198 	push	hl
   5106 D5            [11]  199 	push	de
   5107 33            [ 6]  200 	inc	sp
   5108 C5            [11]  201 	push	bc
   5109 CD C5 5D      [17]  202 	call	_cpct_drawSolidBox
   510C F1            [10]  203 	pop	af
   510D F1            [10]  204 	pop	af
   510E 33            [ 6]  205 	inc	sp
   510F C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   5110                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   5110 FD 21 5F 5F   [14]  213 	ld	iy, #_gtilegroundy
   5114 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   5117 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   5118                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   5118 FD 21 02 00   [14]  222 	ld	iy, #2
   511C FD 39         [15]  223 	add	iy, sp
   511E FD 7E 00      [19]  224 	ld	a, 0 (iy)
   5121 D6 18         [ 7]  225 	sub	a, #0x18
   5123 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   5126 17            [ 4]  227 	rla
   5127 3F            [ 4]  228 	ccf
   5128 1F            [ 4]  229 	rra
   5129 DE 80         [ 7]  230 	sbc	a, #0x80
   512B 38 1A         [12]  231 	jr	C,00102$
   512D 3E 38         [ 7]  232 	ld	a, #0x38
   512F FD BE 00      [19]  233 	cp	a, 0 (iy)
   5132 3E 00         [ 7]  234 	ld	a, #0x00
   5134 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   5137 E2 3C 51      [10]  236 	jp	PO, 00114$
   513A EE 80         [ 7]  237 	xor	a, #0x80
   513C                     238 00114$:
   513C FA 47 51      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   513F FD 21 60 5F   [14]  241 	ld	iy, #_gtileplatformy
   5143 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   5146 C9            [10]  243 	ret
   5147                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   5147 2E FF         [ 7]  246 	ld	l, #0xff
   5149 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   514A                     252 _tilemap_is_trap::
   514A DD E5         [15]  253 	push	ix
   514C DD 21 00 00   [14]  254 	ld	ix,#0
   5150 DD 39         [15]  255 	add	ix,sp
   5152 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   5153 DD 4E 04      [19]  258 	ld	c,4 (ix)
   5156 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5159 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   515C 26 00         [ 7]  262 	ld	h, #0x00
   515E 09            [11]  263 	add	hl, bc
   515F 33            [ 6]  264 	inc	sp
   5160 33            [ 6]  265 	inc	sp
   5161 E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5162 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5165 16 00         [ 7]  269 	ld	d, #0x00
   5167 DD 6E 06      [19]  270 	ld	l,6 (ix)
   516A DD 66 07      [19]  271 	ld	h,7 (ix)
   516D 19            [11]  272 	add	hl, de
   516E EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   516F FD 21 5F 5F   [14]  275 	ld	iy, #_gtilegroundy
   5173 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   5176 26 00         [ 7]  277 	ld	h, #0x00
   5178 2B            [ 6]  278 	dec	hl
   5179 2B            [ 6]  279 	dec	hl
   517A 7B            [ 4]  280 	ld	a, e
   517B 95            [ 4]  281 	sub	a, l
   517C 7A            [ 4]  282 	ld	a, d
   517D 9C            [ 4]  283 	sbc	a, h
   517E E2 83 51      [10]  284 	jp	PO, 00119$
   5181 EE 80         [ 7]  285 	xor	a, #0x80
   5183                     286 00119$:
   5183 FA A7 51      [10]  287 	jp	M, 00102$
   5186 79            [ 4]  288 	ld	a, c
   5187 D6 48         [ 7]  289 	sub	a, #0x48
   5189 78            [ 4]  290 	ld	a, b
   518A 17            [ 4]  291 	rla
   518B 3F            [ 4]  292 	ccf
   518C 1F            [ 4]  293 	rra
   518D DE 80         [ 7]  294 	sbc	a, #0x80
   518F 30 16         [12]  295 	jr	NC,00102$
   5191 3E 38         [ 7]  296 	ld	a, #0x38
   5193 DD BE FE      [19]  297 	cp	a, -2 (ix)
   5196 3E 00         [ 7]  298 	ld	a, #0x00
   5198 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   519B E2 A0 51      [10]  300 	jp	PO, 00120$
   519E EE 80         [ 7]  301 	xor	a, #0x80
   51A0                     302 00120$:
   51A0 F2 A7 51      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   51A3 2E 01         [ 7]  305 	ld	l, #0x01
   51A5 18 02         [12]  306 	jr	00105$
   51A7                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   51A7 2E 00         [ 7]  309 	ld	l, #0x00
   51A9                     310 00105$:
   51A9 DD F9         [10]  311 	ld	sp, ix
   51AB DD E1         [14]  312 	pop	ix
   51AD C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   51AE                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   51AE 2E 00         [ 7]  320 	ld	l, #0x00
   51B0 C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   51B1                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   51B1 2E 00         [ 7]  328 	ld	l, #0x00
   51B3 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   51B4                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   51B4 FD 21 61 5F   [14]  336 	ld	iy, #_ggoalx
   51B8 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   51BB C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   5F66                     341 __xinit__gtilegroundy:
   5F66 A0                  342 	.db #0xa0	; 160
   5F67                     343 __xinit__gtileplatformy:
   5F67 80                  344 	.db #0x80	; 128
   5F68                     345 __xinit__ggoalx:
   5F68 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
