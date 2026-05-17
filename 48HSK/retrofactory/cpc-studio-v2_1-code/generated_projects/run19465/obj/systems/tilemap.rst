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
                             13 	.globl _tilemap_init
                             14 	.globl _tilemap_render
                             15 	.globl _tilemap_ground_y
                             16 	.globl _tilemap_platform_y_at
                             17 	.globl _tilemap_is_trap
                             18 	.globl _tilemap_is_ladder
                             19 	.globl _tilemap_is_hidden_zone
                             20 	.globl _tilemap_goal_x
                             21 ;--------------------------------------------------------
                             22 ; special function registers
                             23 ;--------------------------------------------------------
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _DATA
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _INITIALIZED
   5F7D                      32 _gtilegroundy:
   5F7D                      33 	.ds 1
   5F7E                      34 _gtileplatformy:
   5F7E                      35 	.ds 1
   5F7F                      36 _ggoalx:
   5F7F                      37 	.ds 1
                             38 ;--------------------------------------------------------
                             39 ; absolute external ram data
                             40 ;--------------------------------------------------------
                             41 	.area _DABS (ABS)
                             42 ;--------------------------------------------------------
                             43 ; global & static initialisations
                             44 ;--------------------------------------------------------
                             45 	.area _HOME
                             46 	.area _GSINIT
                             47 	.area _GSFINAL
                             48 	.area _GSINIT
                             49 ;--------------------------------------------------------
                             50 ; Home
                             51 ;--------------------------------------------------------
                             52 	.area _HOME
                             53 	.area _HOME
                             54 ;--------------------------------------------------------
                             55 ; code
                             56 ;--------------------------------------------------------
                             57 	.area _CODE
                             58 ;src/systems/tilemap.c:9: void tilemap_init(void) {
                             59 ;	---------------------------------
                             60 ; Function tilemap_init
                             61 ; ---------------------------------
   4FD7                      62 _tilemap_init::
                             63 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   4FD7 2A 32 51      [16]   64 	ld	hl, (_level1tilemapheight)
   4FDA 3E 02         [ 7]   65 	ld	a, #0x02
   4FDC BD            [ 4]   66 	cp	a, l
   4FDD 3E 00         [ 7]   67 	ld	a, #0x00
   4FDF 9C            [ 4]   68 	sbc	a, h
   4FE0 30 0D         [12]   69 	jr	NC,00102$
                             70 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4FE2 7D            [ 4]   71 	ld	a, l
   4FE3 C6 FE         [ 7]   72 	add	a, #0xfe
   4FE5 07            [ 4]   73 	rlca
   4FE6 07            [ 4]   74 	rlca
   4FE7 07            [ 4]   75 	rlca
   4FE8 E6 F8         [ 7]   76 	and	a, #0xf8
   4FEA 32 7D 5F      [13]   77 	ld	(#_gtilegroundy + 0),a
   4FED 18 05         [12]   78 	jr	00103$
   4FEF                      79 00102$:
                             80 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   4FEF 21 7D 5F      [10]   81 	ld	hl,#_gtilegroundy + 0
   4FF2 36 A0         [10]   82 	ld	(hl), #0xa0
   4FF4                      83 00103$:
                             84 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   4FF4 21 7E 5F      [10]   85 	ld	hl, #_gtileplatformy
   4FF7 3A 7D 5F      [13]   86 	ld	a,(#_gtilegroundy + 0)
   4FFA C6 E8         [ 7]   87 	add	a, #0xe8
   4FFC 77            [ 7]   88 	ld	(hl), a
                             89 ;src/systems/tilemap.c:16: ggoalx = 72;
   4FFD 21 7F 5F      [10]   90 	ld	hl,#_ggoalx + 0
   5000 36 48         [10]   91 	ld	(hl), #0x48
   5002 C9            [10]   92 	ret
                             93 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             94 ;	---------------------------------
                             95 ; Function tilemap_render
                             96 ; ---------------------------------
   5003                      97 _tilemap_render::
                             98 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5003 3A 7D 5F      [13]   99 	ld	a, (_gtilegroundy)
   5006 F5            [11]  100 	push	af
   5007 33            [ 6]  101 	inc	sp
   5008 AF            [ 4]  102 	xor	a, a
   5009 F5            [11]  103 	push	af
   500A 33            [ 6]  104 	inc	sp
   500B 21 00 C0      [10]  105 	ld	hl, #0xc000
   500E E5            [11]  106 	push	hl
   500F CD 98 5E      [17]  107 	call	_cpct_getScreenPtr
                            108 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   5012 01 50 08      [10]  109 	ld	bc, #0x0850
   5015 C5            [11]  110 	push	bc
   5016 3E 11         [ 7]  111 	ld	a, #0x11
   5018 F5            [11]  112 	push	af
   5019 33            [ 6]  113 	inc	sp
   501A E5            [11]  114 	push	hl
   501B CD DF 5D      [17]  115 	call	_cpct_drawSolidBox
   501E F1            [10]  116 	pop	af
   501F F1            [10]  117 	pop	af
   5020 33            [ 6]  118 	inc	sp
                            119 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5021 3A 7E 5F      [13]  120 	ld	a, (_gtileplatformy)
   5024 57            [ 4]  121 	ld	d,a
   5025 1E 18         [ 7]  122 	ld	e,#0x18
   5027 D5            [11]  123 	push	de
   5028 21 00 C0      [10]  124 	ld	hl, #0xc000
   502B E5            [11]  125 	push	hl
   502C CD 98 5E      [17]  126 	call	_cpct_getScreenPtr
                            127 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   502F 01 20 04      [10]  128 	ld	bc, #0x0420
   5032 C5            [11]  129 	push	bc
   5033 3E 33         [ 7]  130 	ld	a, #0x33
   5035 F5            [11]  131 	push	af
   5036 33            [ 6]  132 	inc	sp
   5037 E5            [11]  133 	push	hl
   5038 CD DF 5D      [17]  134 	call	_cpct_drawSolidBox
   503B F1            [10]  135 	pop	af
   503C F1            [10]  136 	pop	af
   503D 33            [ 6]  137 	inc	sp
                            138 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   503E 21 7D 5F      [10]  139 	ld	hl,#_gtilegroundy + 0
   5041 46            [ 7]  140 	ld	b, (hl)
   5042 05            [ 4]  141 	dec	b
   5043 05            [ 4]  142 	dec	b
   5044 C5            [11]  143 	push	bc
   5045 33            [ 6]  144 	inc	sp
   5046 3E 38         [ 7]  145 	ld	a, #0x38
   5048 F5            [11]  146 	push	af
   5049 33            [ 6]  147 	inc	sp
   504A 21 00 C0      [10]  148 	ld	hl, #0xc000
   504D E5            [11]  149 	push	hl
   504E CD 98 5E      [17]  150 	call	_cpct_getScreenPtr
                            151 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   5051 01 10 02      [10]  152 	ld	bc, #0x0210
   5054 C5            [11]  153 	push	bc
   5055 3E 66         [ 7]  154 	ld	a, #0x66
   5057 F5            [11]  155 	push	af
   5058 33            [ 6]  156 	inc	sp
   5059 E5            [11]  157 	push	hl
   505A CD DF 5D      [17]  158 	call	_cpct_drawSolidBox
   505D F1            [10]  159 	pop	af
   505E F1            [10]  160 	pop	af
   505F 33            [ 6]  161 	inc	sp
                            162 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   5060 3A 7D 5F      [13]  163 	ld	a,(#_gtilegroundy + 0)
   5063 C6 F0         [ 7]  164 	add	a, #0xf0
   5065 47            [ 4]  165 	ld	b, a
   5066 C5            [11]  166 	push	bc
   5067 33            [ 6]  167 	inc	sp
   5068 3A 7F 5F      [13]  168 	ld	a, (_ggoalx)
   506B F5            [11]  169 	push	af
   506C 33            [ 6]  170 	inc	sp
   506D 21 00 C0      [10]  171 	ld	hl, #0xc000
   5070 E5            [11]  172 	push	hl
   5071 CD 98 5E      [17]  173 	call	_cpct_getScreenPtr
                            174 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   5074 01 02 10      [10]  175 	ld	bc, #0x1002
   5077 C5            [11]  176 	push	bc
   5078 3E 5F         [ 7]  177 	ld	a, #0x5f
   507A F5            [11]  178 	push	af
   507B 33            [ 6]  179 	inc	sp
   507C E5            [11]  180 	push	hl
   507D CD DF 5D      [17]  181 	call	_cpct_drawSolidBox
   5080 F1            [10]  182 	pop	af
   5081 F1            [10]  183 	pop	af
   5082 33            [ 6]  184 	inc	sp
   5083 C9            [10]  185 	ret
                            186 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            187 ;	---------------------------------
                            188 ; Function tilemap_ground_y
                            189 ; ---------------------------------
   5084                     190 _tilemap_ground_y::
                            191 ;src/systems/tilemap.c:35: return gtilegroundy;
   5084 FD 21 7D 5F   [14]  192 	ld	iy, #_gtilegroundy
   5088 FD 6E 00      [19]  193 	ld	l, 0 (iy)
   508B C9            [10]  194 	ret
                            195 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            196 ;	---------------------------------
                            197 ; Function tilemap_platform_y_at
                            198 ; ---------------------------------
   508C                     199 _tilemap_platform_y_at::
                            200 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   508C FD 21 02 00   [14]  201 	ld	iy, #2
   5090 FD 39         [15]  202 	add	iy, sp
   5092 FD 7E 00      [19]  203 	ld	a, 0 (iy)
   5095 D6 18         [ 7]  204 	sub	a, #0x18
   5097 FD 7E 01      [19]  205 	ld	a, 1 (iy)
   509A 17            [ 4]  206 	rla
   509B 3F            [ 4]  207 	ccf
   509C 1F            [ 4]  208 	rra
   509D DE 80         [ 7]  209 	sbc	a, #0x80
   509F 38 1A         [12]  210 	jr	C,00102$
   50A1 3E 38         [ 7]  211 	ld	a, #0x38
   50A3 FD BE 00      [19]  212 	cp	a, 0 (iy)
   50A6 3E 00         [ 7]  213 	ld	a, #0x00
   50A8 FD 9E 01      [19]  214 	sbc	a, 1 (iy)
   50AB E2 B0 50      [10]  215 	jp	PO, 00114$
   50AE EE 80         [ 7]  216 	xor	a, #0x80
   50B0                     217 00114$:
   50B0 FA BB 50      [10]  218 	jp	M, 00102$
                            219 ;src/systems/tilemap.c:40: return gtileplatformy;
   50B3 FD 21 7E 5F   [14]  220 	ld	iy, #_gtileplatformy
   50B7 FD 6E 00      [19]  221 	ld	l, 0 (iy)
   50BA C9            [10]  222 	ret
   50BB                     223 00102$:
                            224 ;src/systems/tilemap.c:42: return 255;
   50BB 2E FF         [ 7]  225 	ld	l, #0xff
   50BD C9            [10]  226 	ret
                            227 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            228 ;	---------------------------------
                            229 ; Function tilemap_is_trap
                            230 ; ---------------------------------
   50BE                     231 _tilemap_is_trap::
   50BE DD E5         [15]  232 	push	ix
   50C0 DD 21 00 00   [14]  233 	ld	ix,#0
   50C4 DD 39         [15]  234 	add	ix,sp
   50C6 F5            [11]  235 	push	af
                            236 ;src/systems/tilemap.c:50: left = x;
   50C7 DD 4E 04      [19]  237 	ld	c,4 (ix)
   50CA DD 46 05      [19]  238 	ld	b,5 (ix)
                            239 ;src/systems/tilemap.c:51: right = x + (i16)w;
   50CD DD 6E 08      [19]  240 	ld	l, 8 (ix)
   50D0 26 00         [ 7]  241 	ld	h, #0x00
   50D2 09            [11]  242 	add	hl, bc
   50D3 33            [ 6]  243 	inc	sp
   50D4 33            [ 6]  244 	inc	sp
   50D5 E5            [11]  245 	push	hl
                            246 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   50D6 DD 5E 09      [19]  247 	ld	e, 9 (ix)
   50D9 16 00         [ 7]  248 	ld	d, #0x00
   50DB DD 6E 06      [19]  249 	ld	l,6 (ix)
   50DE DD 66 07      [19]  250 	ld	h,7 (ix)
   50E1 19            [11]  251 	add	hl, de
   50E2 EB            [ 4]  252 	ex	de,hl
                            253 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   50E3 FD 21 7D 5F   [14]  254 	ld	iy, #_gtilegroundy
   50E7 FD 6E 00      [19]  255 	ld	l, 0 (iy)
   50EA 26 00         [ 7]  256 	ld	h, #0x00
   50EC 2B            [ 6]  257 	dec	hl
   50ED 2B            [ 6]  258 	dec	hl
   50EE 7B            [ 4]  259 	ld	a, e
   50EF 95            [ 4]  260 	sub	a, l
   50F0 7A            [ 4]  261 	ld	a, d
   50F1 9C            [ 4]  262 	sbc	a, h
   50F2 E2 F7 50      [10]  263 	jp	PO, 00119$
   50F5 EE 80         [ 7]  264 	xor	a, #0x80
   50F7                     265 00119$:
   50F7 FA 1B 51      [10]  266 	jp	M, 00102$
   50FA 79            [ 4]  267 	ld	a, c
   50FB D6 48         [ 7]  268 	sub	a, #0x48
   50FD 78            [ 4]  269 	ld	a, b
   50FE 17            [ 4]  270 	rla
   50FF 3F            [ 4]  271 	ccf
   5100 1F            [ 4]  272 	rra
   5101 DE 80         [ 7]  273 	sbc	a, #0x80
   5103 30 16         [12]  274 	jr	NC,00102$
   5105 3E 38         [ 7]  275 	ld	a, #0x38
   5107 DD BE FE      [19]  276 	cp	a, -2 (ix)
   510A 3E 00         [ 7]  277 	ld	a, #0x00
   510C DD 9E FF      [19]  278 	sbc	a, -1 (ix)
   510F E2 14 51      [10]  279 	jp	PO, 00120$
   5112 EE 80         [ 7]  280 	xor	a, #0x80
   5114                     281 00120$:
   5114 F2 1B 51      [10]  282 	jp	P, 00102$
                            283 ;src/systems/tilemap.c:55: return 1;
   5117 2E 01         [ 7]  284 	ld	l, #0x01
   5119 18 02         [12]  285 	jr	00105$
   511B                     286 00102$:
                            287 ;src/systems/tilemap.c:57: return 0;
   511B 2E 00         [ 7]  288 	ld	l, #0x00
   511D                     289 00105$:
   511D DD F9         [10]  290 	ld	sp, ix
   511F DD E1         [14]  291 	pop	ix
   5121 C9            [10]  292 	ret
                            293 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            294 ;	---------------------------------
                            295 ; Function tilemap_is_ladder
                            296 ; ---------------------------------
   5122                     297 _tilemap_is_ladder::
                            298 ;src/systems/tilemap.c:65: return 0;
   5122 2E 00         [ 7]  299 	ld	l, #0x00
   5124 C9            [10]  300 	ret
                            301 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            302 ;	---------------------------------
                            303 ; Function tilemap_is_hidden_zone
                            304 ; ---------------------------------
   5125                     305 _tilemap_is_hidden_zone::
                            306 ;src/systems/tilemap.c:73: return 0;
   5125 2E 00         [ 7]  307 	ld	l, #0x00
   5127 C9            [10]  308 	ret
                            309 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            310 ;	---------------------------------
                            311 ; Function tilemap_goal_x
                            312 ; ---------------------------------
   5128                     313 _tilemap_goal_x::
                            314 ;src/systems/tilemap.c:77: return ggoalx;
   5128 FD 21 7F 5F   [14]  315 	ld	iy, #_ggoalx
   512C FD 6E 00      [19]  316 	ld	l, 0 (iy)
   512F C9            [10]  317 	ret
                            318 	.area _CODE
                            319 	.area _INITIALIZER
   5F98                     320 __xinit__gtilegroundy:
   5F98 A0                  321 	.db #0xa0	; 160
   5F99                     322 __xinit__gtileplatformy:
   5F99 80                  323 	.db #0x80	; 128
   5F9A                     324 __xinit__ggoalx:
   5F9A 48                  325 	.db #0x48	; 72	'H'
                            326 	.area _CABS (ABS)
