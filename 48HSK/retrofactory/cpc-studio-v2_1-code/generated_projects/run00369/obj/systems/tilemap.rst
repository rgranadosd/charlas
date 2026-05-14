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
   5F47                      32 _gtilegroundy:
   5F47                      33 	.ds 1
   5F48                      34 _gtileplatformy:
   5F48                      35 	.ds 1
   5F49                      36 _ggoalx:
   5F49                      37 	.ds 1
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
   4FBF                      62 _tilemap_init::
                             63 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   4FBF 2A 1A 51      [16]   64 	ld	hl, (_level1tilemapheight)
   4FC2 3E 02         [ 7]   65 	ld	a, #0x02
   4FC4 BD            [ 4]   66 	cp	a, l
   4FC5 3E 00         [ 7]   67 	ld	a, #0x00
   4FC7 9C            [ 4]   68 	sbc	a, h
   4FC8 30 0D         [12]   69 	jr	NC,00102$
                             70 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4FCA 7D            [ 4]   71 	ld	a, l
   4FCB C6 FE         [ 7]   72 	add	a, #0xfe
   4FCD 07            [ 4]   73 	rlca
   4FCE 07            [ 4]   74 	rlca
   4FCF 07            [ 4]   75 	rlca
   4FD0 E6 F8         [ 7]   76 	and	a, #0xf8
   4FD2 32 47 5F      [13]   77 	ld	(#_gtilegroundy + 0),a
   4FD5 18 05         [12]   78 	jr	00103$
   4FD7                      79 00102$:
                             80 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   4FD7 21 47 5F      [10]   81 	ld	hl,#_gtilegroundy + 0
   4FDA 36 A0         [10]   82 	ld	(hl), #0xa0
   4FDC                      83 00103$:
                             84 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   4FDC 21 48 5F      [10]   85 	ld	hl, #_gtileplatformy
   4FDF 3A 47 5F      [13]   86 	ld	a,(#_gtilegroundy + 0)
   4FE2 C6 E8         [ 7]   87 	add	a, #0xe8
   4FE4 77            [ 7]   88 	ld	(hl), a
                             89 ;src/systems/tilemap.c:16: ggoalx = 72;
   4FE5 21 49 5F      [10]   90 	ld	hl,#_ggoalx + 0
   4FE8 36 48         [10]   91 	ld	(hl), #0x48
   4FEA C9            [10]   92 	ret
                             93 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             94 ;	---------------------------------
                             95 ; Function tilemap_render
                             96 ; ---------------------------------
   4FEB                      97 _tilemap_render::
                             98 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4FEB 3A 47 5F      [13]   99 	ld	a, (_gtilegroundy)
   4FEE F5            [11]  100 	push	af
   4FEF 33            [ 6]  101 	inc	sp
   4FF0 AF            [ 4]  102 	xor	a, a
   4FF1 F5            [11]  103 	push	af
   4FF2 33            [ 6]  104 	inc	sp
   4FF3 21 00 C0      [10]  105 	ld	hl, #0xc000
   4FF6 E5            [11]  106 	push	hl
   4FF7 CD 62 5E      [17]  107 	call	_cpct_getScreenPtr
                            108 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4FFA 01 50 08      [10]  109 	ld	bc, #0x0850
   4FFD C5            [11]  110 	push	bc
   4FFE 3E 11         [ 7]  111 	ld	a, #0x11
   5000 F5            [11]  112 	push	af
   5001 33            [ 6]  113 	inc	sp
   5002 E5            [11]  114 	push	hl
   5003 CD A9 5D      [17]  115 	call	_cpct_drawSolidBox
   5006 F1            [10]  116 	pop	af
   5007 F1            [10]  117 	pop	af
   5008 33            [ 6]  118 	inc	sp
                            119 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   5009 3A 48 5F      [13]  120 	ld	a, (_gtileplatformy)
   500C 57            [ 4]  121 	ld	d,a
   500D 1E 18         [ 7]  122 	ld	e,#0x18
   500F D5            [11]  123 	push	de
   5010 21 00 C0      [10]  124 	ld	hl, #0xc000
   5013 E5            [11]  125 	push	hl
   5014 CD 62 5E      [17]  126 	call	_cpct_getScreenPtr
                            127 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   5017 01 20 04      [10]  128 	ld	bc, #0x0420
   501A C5            [11]  129 	push	bc
   501B 3E 33         [ 7]  130 	ld	a, #0x33
   501D F5            [11]  131 	push	af
   501E 33            [ 6]  132 	inc	sp
   501F E5            [11]  133 	push	hl
   5020 CD A9 5D      [17]  134 	call	_cpct_drawSolidBox
   5023 F1            [10]  135 	pop	af
   5024 F1            [10]  136 	pop	af
   5025 33            [ 6]  137 	inc	sp
                            138 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   5026 21 47 5F      [10]  139 	ld	hl,#_gtilegroundy + 0
   5029 46            [ 7]  140 	ld	b, (hl)
   502A 05            [ 4]  141 	dec	b
   502B 05            [ 4]  142 	dec	b
   502C C5            [11]  143 	push	bc
   502D 33            [ 6]  144 	inc	sp
   502E 3E 38         [ 7]  145 	ld	a, #0x38
   5030 F5            [11]  146 	push	af
   5031 33            [ 6]  147 	inc	sp
   5032 21 00 C0      [10]  148 	ld	hl, #0xc000
   5035 E5            [11]  149 	push	hl
   5036 CD 62 5E      [17]  150 	call	_cpct_getScreenPtr
                            151 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   5039 01 10 02      [10]  152 	ld	bc, #0x0210
   503C C5            [11]  153 	push	bc
   503D 3E 66         [ 7]  154 	ld	a, #0x66
   503F F5            [11]  155 	push	af
   5040 33            [ 6]  156 	inc	sp
   5041 E5            [11]  157 	push	hl
   5042 CD A9 5D      [17]  158 	call	_cpct_drawSolidBox
   5045 F1            [10]  159 	pop	af
   5046 F1            [10]  160 	pop	af
   5047 33            [ 6]  161 	inc	sp
                            162 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   5048 3A 47 5F      [13]  163 	ld	a,(#_gtilegroundy + 0)
   504B C6 F0         [ 7]  164 	add	a, #0xf0
   504D 47            [ 4]  165 	ld	b, a
   504E C5            [11]  166 	push	bc
   504F 33            [ 6]  167 	inc	sp
   5050 3A 49 5F      [13]  168 	ld	a, (_ggoalx)
   5053 F5            [11]  169 	push	af
   5054 33            [ 6]  170 	inc	sp
   5055 21 00 C0      [10]  171 	ld	hl, #0xc000
   5058 E5            [11]  172 	push	hl
   5059 CD 62 5E      [17]  173 	call	_cpct_getScreenPtr
                            174 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   505C 01 02 10      [10]  175 	ld	bc, #0x1002
   505F C5            [11]  176 	push	bc
   5060 3E 5F         [ 7]  177 	ld	a, #0x5f
   5062 F5            [11]  178 	push	af
   5063 33            [ 6]  179 	inc	sp
   5064 E5            [11]  180 	push	hl
   5065 CD A9 5D      [17]  181 	call	_cpct_drawSolidBox
   5068 F1            [10]  182 	pop	af
   5069 F1            [10]  183 	pop	af
   506A 33            [ 6]  184 	inc	sp
   506B C9            [10]  185 	ret
                            186 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            187 ;	---------------------------------
                            188 ; Function tilemap_ground_y
                            189 ; ---------------------------------
   506C                     190 _tilemap_ground_y::
                            191 ;src/systems/tilemap.c:35: return gtilegroundy;
   506C FD 21 47 5F   [14]  192 	ld	iy, #_gtilegroundy
   5070 FD 6E 00      [19]  193 	ld	l, 0 (iy)
   5073 C9            [10]  194 	ret
                            195 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            196 ;	---------------------------------
                            197 ; Function tilemap_platform_y_at
                            198 ; ---------------------------------
   5074                     199 _tilemap_platform_y_at::
                            200 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   5074 FD 21 02 00   [14]  201 	ld	iy, #2
   5078 FD 39         [15]  202 	add	iy, sp
   507A FD 7E 00      [19]  203 	ld	a, 0 (iy)
   507D D6 18         [ 7]  204 	sub	a, #0x18
   507F FD 7E 01      [19]  205 	ld	a, 1 (iy)
   5082 17            [ 4]  206 	rla
   5083 3F            [ 4]  207 	ccf
   5084 1F            [ 4]  208 	rra
   5085 DE 80         [ 7]  209 	sbc	a, #0x80
   5087 38 1A         [12]  210 	jr	C,00102$
   5089 3E 38         [ 7]  211 	ld	a, #0x38
   508B FD BE 00      [19]  212 	cp	a, 0 (iy)
   508E 3E 00         [ 7]  213 	ld	a, #0x00
   5090 FD 9E 01      [19]  214 	sbc	a, 1 (iy)
   5093 E2 98 50      [10]  215 	jp	PO, 00114$
   5096 EE 80         [ 7]  216 	xor	a, #0x80
   5098                     217 00114$:
   5098 FA A3 50      [10]  218 	jp	M, 00102$
                            219 ;src/systems/tilemap.c:40: return gtileplatformy;
   509B FD 21 48 5F   [14]  220 	ld	iy, #_gtileplatformy
   509F FD 6E 00      [19]  221 	ld	l, 0 (iy)
   50A2 C9            [10]  222 	ret
   50A3                     223 00102$:
                            224 ;src/systems/tilemap.c:42: return 255;
   50A3 2E FF         [ 7]  225 	ld	l, #0xff
   50A5 C9            [10]  226 	ret
                            227 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            228 ;	---------------------------------
                            229 ; Function tilemap_is_trap
                            230 ; ---------------------------------
   50A6                     231 _tilemap_is_trap::
   50A6 DD E5         [15]  232 	push	ix
   50A8 DD 21 00 00   [14]  233 	ld	ix,#0
   50AC DD 39         [15]  234 	add	ix,sp
   50AE F5            [11]  235 	push	af
                            236 ;src/systems/tilemap.c:50: left = x;
   50AF DD 4E 04      [19]  237 	ld	c,4 (ix)
   50B2 DD 46 05      [19]  238 	ld	b,5 (ix)
                            239 ;src/systems/tilemap.c:51: right = x + (i16)w;
   50B5 DD 6E 08      [19]  240 	ld	l, 8 (ix)
   50B8 26 00         [ 7]  241 	ld	h, #0x00
   50BA 09            [11]  242 	add	hl, bc
   50BB 33            [ 6]  243 	inc	sp
   50BC 33            [ 6]  244 	inc	sp
   50BD E5            [11]  245 	push	hl
                            246 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   50BE DD 5E 09      [19]  247 	ld	e, 9 (ix)
   50C1 16 00         [ 7]  248 	ld	d, #0x00
   50C3 DD 6E 06      [19]  249 	ld	l,6 (ix)
   50C6 DD 66 07      [19]  250 	ld	h,7 (ix)
   50C9 19            [11]  251 	add	hl, de
   50CA EB            [ 4]  252 	ex	de,hl
                            253 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   50CB FD 21 47 5F   [14]  254 	ld	iy, #_gtilegroundy
   50CF FD 6E 00      [19]  255 	ld	l, 0 (iy)
   50D2 26 00         [ 7]  256 	ld	h, #0x00
   50D4 2B            [ 6]  257 	dec	hl
   50D5 2B            [ 6]  258 	dec	hl
   50D6 7B            [ 4]  259 	ld	a, e
   50D7 95            [ 4]  260 	sub	a, l
   50D8 7A            [ 4]  261 	ld	a, d
   50D9 9C            [ 4]  262 	sbc	a, h
   50DA E2 DF 50      [10]  263 	jp	PO, 00119$
   50DD EE 80         [ 7]  264 	xor	a, #0x80
   50DF                     265 00119$:
   50DF FA 03 51      [10]  266 	jp	M, 00102$
   50E2 79            [ 4]  267 	ld	a, c
   50E3 D6 48         [ 7]  268 	sub	a, #0x48
   50E5 78            [ 4]  269 	ld	a, b
   50E6 17            [ 4]  270 	rla
   50E7 3F            [ 4]  271 	ccf
   50E8 1F            [ 4]  272 	rra
   50E9 DE 80         [ 7]  273 	sbc	a, #0x80
   50EB 30 16         [12]  274 	jr	NC,00102$
   50ED 3E 38         [ 7]  275 	ld	a, #0x38
   50EF DD BE FE      [19]  276 	cp	a, -2 (ix)
   50F2 3E 00         [ 7]  277 	ld	a, #0x00
   50F4 DD 9E FF      [19]  278 	sbc	a, -1 (ix)
   50F7 E2 FC 50      [10]  279 	jp	PO, 00120$
   50FA EE 80         [ 7]  280 	xor	a, #0x80
   50FC                     281 00120$:
   50FC F2 03 51      [10]  282 	jp	P, 00102$
                            283 ;src/systems/tilemap.c:55: return 1;
   50FF 2E 01         [ 7]  284 	ld	l, #0x01
   5101 18 02         [12]  285 	jr	00105$
   5103                     286 00102$:
                            287 ;src/systems/tilemap.c:57: return 0;
   5103 2E 00         [ 7]  288 	ld	l, #0x00
   5105                     289 00105$:
   5105 DD F9         [10]  290 	ld	sp, ix
   5107 DD E1         [14]  291 	pop	ix
   5109 C9            [10]  292 	ret
                            293 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            294 ;	---------------------------------
                            295 ; Function tilemap_is_ladder
                            296 ; ---------------------------------
   510A                     297 _tilemap_is_ladder::
                            298 ;src/systems/tilemap.c:65: return 0;
   510A 2E 00         [ 7]  299 	ld	l, #0x00
   510C C9            [10]  300 	ret
                            301 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            302 ;	---------------------------------
                            303 ; Function tilemap_is_hidden_zone
                            304 ; ---------------------------------
   510D                     305 _tilemap_is_hidden_zone::
                            306 ;src/systems/tilemap.c:73: return 0;
   510D 2E 00         [ 7]  307 	ld	l, #0x00
   510F C9            [10]  308 	ret
                            309 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            310 ;	---------------------------------
                            311 ; Function tilemap_goal_x
                            312 ; ---------------------------------
   5110                     313 _tilemap_goal_x::
                            314 ;src/systems/tilemap.c:77: return ggoalx;
   5110 FD 21 49 5F   [14]  315 	ld	iy, #_ggoalx
   5114 FD 6E 00      [19]  316 	ld	l, 0 (iy)
   5117 C9            [10]  317 	ret
                            318 	.area _CODE
                            319 	.area _INITIALIZER
   5F62                     320 __xinit__gtilegroundy:
   5F62 A0                  321 	.db #0xa0	; 160
   5F63                     322 __xinit__gtileplatformy:
   5F63 80                  323 	.db #0x80	; 128
   5F64                     324 __xinit__ggoalx:
   5F64 48                  325 	.db #0x48	; 72	'H'
                            326 	.area _CABS (ABS)
