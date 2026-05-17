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
   5F43                      33 _gtilegroundy:
   5F43                      34 	.ds 1
   5F44                      35 _gtileplatformy:
   5F44                      36 	.ds 1
   5F45                      37 _ggoalx:
   5F45                      38 	.ds 1
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
   5041                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   5041 2A BC 51      [16]   65 	ld	hl, (_level1tilemapheight)
   5044 3E 02         [ 7]   66 	ld	a, #0x02
   5046 BD            [ 4]   67 	cp	a, l
   5047 3E 00         [ 7]   68 	ld	a, #0x00
   5049 9C            [ 4]   69 	sbc	a, h
   504A 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   504C 7D            [ 4]   72 	ld	a, l
   504D C6 FE         [ 7]   73 	add	a, #0xfe
   504F 07            [ 4]   74 	rlca
   5050 07            [ 4]   75 	rlca
   5051 07            [ 4]   76 	rlca
   5052 E6 F8         [ 7]   77 	and	a, #0xf8
   5054 32 43 5F      [13]   78 	ld	(#_gtilegroundy + 0),a
   5057 18 05         [12]   79 	jr	00103$
   5059                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5059 21 43 5F      [10]   82 	ld	hl,#_gtilegroundy + 0
   505C 36 A0         [10]   83 	ld	(hl), #0xa0
   505E                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   505E 21 44 5F      [10]   86 	ld	hl, #_gtileplatformy
   5061 3A 43 5F      [13]   87 	ld	a,(#_gtilegroundy + 0)
   5064 C6 E8         [ 7]   88 	add	a, #0xe8
   5066 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5067 21 45 5F      [10]   91 	ld	hl,#_ggoalx + 0
   506A 36 48         [10]   92 	ld	(hl), #0x48
   506C C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   506D                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   506D 3A 43 5F      [13]  100 	ld	a, (_gtilegroundy)
   5070 F5            [11]  101 	push	af
   5071 33            [ 6]  102 	inc	sp
   5072 AF            [ 4]  103 	xor	a, a
   5073 F5            [11]  104 	push	af
   5074 33            [ 6]  105 	inc	sp
   5075 21 00 C0      [10]  106 	ld	hl, #0xc000
   5078 E5            [11]  107 	push	hl
   5079 CD 62 5E      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);
   507C E5            [11]  110 	push	hl
   507D 21 01 01      [10]  111 	ld	hl, #0x0101
   5080 E5            [11]  112 	push	hl
   5081 CD 6F 5D      [17]  113 	call	_cpct_px2byteM0
   5084 55            [ 4]  114 	ld	d, l
   5085 C1            [10]  115 	pop	bc
   5086 21 50 08      [10]  116 	ld	hl, #0x0850
   5089 E5            [11]  117 	push	hl
   508A D5            [11]  118 	push	de
   508B 33            [ 6]  119 	inc	sp
   508C C5            [11]  120 	push	bc
   508D CD A9 5D      [17]  121 	call	_cpct_drawSolidBox
   5090 F1            [10]  122 	pop	af
   5091 F1            [10]  123 	pop	af
   5092 33            [ 6]  124 	inc	sp
                            125 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5093 3A 44 5F      [13]  126 	ld	a, (_gtileplatformy)
   5096 57            [ 4]  127 	ld	d,a
   5097 1E 18         [ 7]  128 	ld	e,#0x18
   5099 D5            [11]  129 	push	de
   509A 21 00 C0      [10]  130 	ld	hl, #0xc000
   509D E5            [11]  131 	push	hl
   509E CD 62 5E      [17]  132 	call	_cpct_getScreenPtr
                            133 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   50A1 E5            [11]  134 	push	hl
   50A2 21 02 02      [10]  135 	ld	hl, #0x0202
   50A5 E5            [11]  136 	push	hl
   50A6 CD 6F 5D      [17]  137 	call	_cpct_px2byteM0
   50A9 55            [ 4]  138 	ld	d, l
   50AA C1            [10]  139 	pop	bc
   50AB 21 20 04      [10]  140 	ld	hl, #0x0420
   50AE E5            [11]  141 	push	hl
   50AF D5            [11]  142 	push	de
   50B0 33            [ 6]  143 	inc	sp
   50B1 C5            [11]  144 	push	bc
   50B2 CD A9 5D      [17]  145 	call	_cpct_drawSolidBox
   50B5 F1            [10]  146 	pop	af
   50B6 F1            [10]  147 	pop	af
   50B7 33            [ 6]  148 	inc	sp
                            149 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   50B8 21 43 5F      [10]  150 	ld	hl,#_gtilegroundy + 0
   50BB 46            [ 7]  151 	ld	b, (hl)
   50BC 05            [ 4]  152 	dec	b
   50BD 05            [ 4]  153 	dec	b
   50BE C5            [11]  154 	push	bc
   50BF 33            [ 6]  155 	inc	sp
   50C0 3E 38         [ 7]  156 	ld	a, #0x38
   50C2 F5            [11]  157 	push	af
   50C3 33            [ 6]  158 	inc	sp
   50C4 21 00 C0      [10]  159 	ld	hl, #0xc000
   50C7 E5            [11]  160 	push	hl
   50C8 CD 62 5E      [17]  161 	call	_cpct_getScreenPtr
                            162 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   50CB E5            [11]  163 	push	hl
   50CC 21 03 03      [10]  164 	ld	hl, #0x0303
   50CF E5            [11]  165 	push	hl
   50D0 CD 6F 5D      [17]  166 	call	_cpct_px2byteM0
   50D3 55            [ 4]  167 	ld	d, l
   50D4 C1            [10]  168 	pop	bc
   50D5 21 10 02      [10]  169 	ld	hl, #0x0210
   50D8 E5            [11]  170 	push	hl
   50D9 D5            [11]  171 	push	de
   50DA 33            [ 6]  172 	inc	sp
   50DB C5            [11]  173 	push	bc
   50DC CD A9 5D      [17]  174 	call	_cpct_drawSolidBox
   50DF F1            [10]  175 	pop	af
   50E0 F1            [10]  176 	pop	af
   50E1 33            [ 6]  177 	inc	sp
                            178 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   50E2 3A 43 5F      [13]  179 	ld	a,(#_gtilegroundy + 0)
   50E5 C6 F0         [ 7]  180 	add	a, #0xf0
   50E7 47            [ 4]  181 	ld	b, a
   50E8 C5            [11]  182 	push	bc
   50E9 33            [ 6]  183 	inc	sp
   50EA 3A 45 5F      [13]  184 	ld	a, (_ggoalx)
   50ED F5            [11]  185 	push	af
   50EE 33            [ 6]  186 	inc	sp
   50EF 21 00 C0      [10]  187 	ld	hl, #0xc000
   50F2 E5            [11]  188 	push	hl
   50F3 CD 62 5E      [17]  189 	call	_cpct_getScreenPtr
                            190 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   50F6 E5            [11]  191 	push	hl
   50F7 21 05 05      [10]  192 	ld	hl, #0x0505
   50FA E5            [11]  193 	push	hl
   50FB CD 6F 5D      [17]  194 	call	_cpct_px2byteM0
   50FE 55            [ 4]  195 	ld	d, l
   50FF C1            [10]  196 	pop	bc
   5100 21 02 10      [10]  197 	ld	hl, #0x1002
   5103 E5            [11]  198 	push	hl
   5104 D5            [11]  199 	push	de
   5105 33            [ 6]  200 	inc	sp
   5106 C5            [11]  201 	push	bc
   5107 CD A9 5D      [17]  202 	call	_cpct_drawSolidBox
   510A F1            [10]  203 	pop	af
   510B F1            [10]  204 	pop	af
   510C 33            [ 6]  205 	inc	sp
   510D C9            [10]  206 	ret
                            207 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            208 ;	---------------------------------
                            209 ; Function tilemap_ground_y
                            210 ; ---------------------------------
   510E                     211 _tilemap_ground_y::
                            212 ;src/systems/tilemap.c:35: return gtilegroundy;
   510E FD 21 43 5F   [14]  213 	ld	iy, #_gtilegroundy
   5112 FD 6E 00      [19]  214 	ld	l, 0 (iy)
   5115 C9            [10]  215 	ret
                            216 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            217 ;	---------------------------------
                            218 ; Function tilemap_platform_y_at
                            219 ; ---------------------------------
   5116                     220 _tilemap_platform_y_at::
                            221 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   5116 FD 21 02 00   [14]  222 	ld	iy, #2
   511A FD 39         [15]  223 	add	iy, sp
   511C FD 7E 00      [19]  224 	ld	a, 0 (iy)
   511F D6 18         [ 7]  225 	sub	a, #0x18
   5121 FD 7E 01      [19]  226 	ld	a, 1 (iy)
   5124 17            [ 4]  227 	rla
   5125 3F            [ 4]  228 	ccf
   5126 1F            [ 4]  229 	rra
   5127 DE 80         [ 7]  230 	sbc	a, #0x80
   5129 38 1A         [12]  231 	jr	C,00102$
   512B 3E 38         [ 7]  232 	ld	a, #0x38
   512D FD BE 00      [19]  233 	cp	a, 0 (iy)
   5130 3E 00         [ 7]  234 	ld	a, #0x00
   5132 FD 9E 01      [19]  235 	sbc	a, 1 (iy)
   5135 E2 3A 51      [10]  236 	jp	PO, 00114$
   5138 EE 80         [ 7]  237 	xor	a, #0x80
   513A                     238 00114$:
   513A FA 45 51      [10]  239 	jp	M, 00102$
                            240 ;src/systems/tilemap.c:40: return gtileplatformy;
   513D FD 21 44 5F   [14]  241 	ld	iy, #_gtileplatformy
   5141 FD 6E 00      [19]  242 	ld	l, 0 (iy)
   5144 C9            [10]  243 	ret
   5145                     244 00102$:
                            245 ;src/systems/tilemap.c:42: return 255;
   5145 2E FF         [ 7]  246 	ld	l, #0xff
   5147 C9            [10]  247 	ret
                            248 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            249 ;	---------------------------------
                            250 ; Function tilemap_is_trap
                            251 ; ---------------------------------
   5148                     252 _tilemap_is_trap::
   5148 DD E5         [15]  253 	push	ix
   514A DD 21 00 00   [14]  254 	ld	ix,#0
   514E DD 39         [15]  255 	add	ix,sp
   5150 F5            [11]  256 	push	af
                            257 ;src/systems/tilemap.c:50: left = x;
   5151 DD 4E 04      [19]  258 	ld	c,4 (ix)
   5154 DD 46 05      [19]  259 	ld	b,5 (ix)
                            260 ;src/systems/tilemap.c:51: right = x + (i16)w;
   5157 DD 6E 08      [19]  261 	ld	l, 8 (ix)
   515A 26 00         [ 7]  262 	ld	h, #0x00
   515C 09            [11]  263 	add	hl, bc
   515D 33            [ 6]  264 	inc	sp
   515E 33            [ 6]  265 	inc	sp
   515F E5            [11]  266 	push	hl
                            267 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   5160 DD 5E 09      [19]  268 	ld	e, 9 (ix)
   5163 16 00         [ 7]  269 	ld	d, #0x00
   5165 DD 6E 06      [19]  270 	ld	l,6 (ix)
   5168 DD 66 07      [19]  271 	ld	h,7 (ix)
   516B 19            [11]  272 	add	hl, de
   516C EB            [ 4]  273 	ex	de,hl
                            274 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   516D FD 21 43 5F   [14]  275 	ld	iy, #_gtilegroundy
   5171 FD 6E 00      [19]  276 	ld	l, 0 (iy)
   5174 26 00         [ 7]  277 	ld	h, #0x00
   5176 2B            [ 6]  278 	dec	hl
   5177 2B            [ 6]  279 	dec	hl
   5178 7B            [ 4]  280 	ld	a, e
   5179 95            [ 4]  281 	sub	a, l
   517A 7A            [ 4]  282 	ld	a, d
   517B 9C            [ 4]  283 	sbc	a, h
   517C E2 81 51      [10]  284 	jp	PO, 00119$
   517F EE 80         [ 7]  285 	xor	a, #0x80
   5181                     286 00119$:
   5181 FA A5 51      [10]  287 	jp	M, 00102$
   5184 79            [ 4]  288 	ld	a, c
   5185 D6 48         [ 7]  289 	sub	a, #0x48
   5187 78            [ 4]  290 	ld	a, b
   5188 17            [ 4]  291 	rla
   5189 3F            [ 4]  292 	ccf
   518A 1F            [ 4]  293 	rra
   518B DE 80         [ 7]  294 	sbc	a, #0x80
   518D 30 16         [12]  295 	jr	NC,00102$
   518F 3E 38         [ 7]  296 	ld	a, #0x38
   5191 DD BE FE      [19]  297 	cp	a, -2 (ix)
   5194 3E 00         [ 7]  298 	ld	a, #0x00
   5196 DD 9E FF      [19]  299 	sbc	a, -1 (ix)
   5199 E2 9E 51      [10]  300 	jp	PO, 00120$
   519C EE 80         [ 7]  301 	xor	a, #0x80
   519E                     302 00120$:
   519E F2 A5 51      [10]  303 	jp	P, 00102$
                            304 ;src/systems/tilemap.c:55: return 1;
   51A1 2E 01         [ 7]  305 	ld	l, #0x01
   51A3 18 02         [12]  306 	jr	00105$
   51A5                     307 00102$:
                            308 ;src/systems/tilemap.c:57: return 0;
   51A5 2E 00         [ 7]  309 	ld	l, #0x00
   51A7                     310 00105$:
   51A7 DD F9         [10]  311 	ld	sp, ix
   51A9 DD E1         [14]  312 	pop	ix
   51AB C9            [10]  313 	ret
                            314 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            315 ;	---------------------------------
                            316 ; Function tilemap_is_ladder
                            317 ; ---------------------------------
   51AC                     318 _tilemap_is_ladder::
                            319 ;src/systems/tilemap.c:65: return 0;
   51AC 2E 00         [ 7]  320 	ld	l, #0x00
   51AE C9            [10]  321 	ret
                            322 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            323 ;	---------------------------------
                            324 ; Function tilemap_is_hidden_zone
                            325 ; ---------------------------------
   51AF                     326 _tilemap_is_hidden_zone::
                            327 ;src/systems/tilemap.c:73: return 0;
   51AF 2E 00         [ 7]  328 	ld	l, #0x00
   51B1 C9            [10]  329 	ret
                            330 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            331 ;	---------------------------------
                            332 ; Function tilemap_goal_x
                            333 ; ---------------------------------
   51B2                     334 _tilemap_goal_x::
                            335 ;src/systems/tilemap.c:77: return ggoalx;
   51B2 FD 21 45 5F   [14]  336 	ld	iy, #_ggoalx
   51B6 FD 6E 00      [19]  337 	ld	l, 0 (iy)
   51B9 C9            [10]  338 	ret
                            339 	.area _CODE
                            340 	.area _INITIALIZER
   5F4A                     341 __xinit__gtilegroundy:
   5F4A A0                  342 	.db #0xa0	; 160
   5F4B                     343 __xinit__gtileplatformy:
   5F4B 80                  344 	.db #0x80	; 128
   5F4C                     345 __xinit__ggoalx:
   5F4C 48                  346 	.db #0x48	; 72	'H'
                            347 	.area _CABS (ABS)
