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
   6D93                      33 _gtilegroundy:
   6D93                      34 	.ds 1
   6D94                      35 _gtileplatformy:
   6D94                      36 	.ds 1
   6D95                      37 _ggoalx:
   6D95                      38 	.ds 1
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
   592B                      63 _tilemap_init::
                             64 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   592B 2A C6 5A      [16]   65 	ld	hl, (_level1tilemapheight)
   592E 3E 02         [ 7]   66 	ld	a, #0x02
   5930 BD            [ 4]   67 	cp	a, l
   5931 3E 00         [ 7]   68 	ld	a, #0x00
   5933 9C            [ 4]   69 	sbc	a, h
   5934 30 0D         [12]   70 	jr	NC,00102$
                             71 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   5936 7D            [ 4]   72 	ld	a, l
   5937 C6 FE         [ 7]   73 	add	a, #0xfe
   5939 07            [ 4]   74 	rlca
   593A 07            [ 4]   75 	rlca
   593B 07            [ 4]   76 	rlca
   593C E6 F8         [ 7]   77 	and	a, #0xf8
   593E 32 93 6D      [13]   78 	ld	(#_gtilegroundy + 0),a
   5941 18 05         [12]   79 	jr	00103$
   5943                      80 00102$:
                             81 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   5943 21 93 6D      [10]   82 	ld	hl,#_gtilegroundy + 0
   5946 36 A0         [10]   83 	ld	(hl), #0xa0
   5948                      84 00103$:
                             85 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   5948 21 94 6D      [10]   86 	ld	hl, #_gtileplatformy
   594B 3A 93 6D      [13]   87 	ld	a,(#_gtilegroundy + 0)
   594E C6 E8         [ 7]   88 	add	a, #0xe8
   5950 77            [ 7]   89 	ld	(hl), a
                             90 ;src/systems/tilemap.c:16: ggoalx = 72;
   5951 21 95 6D      [10]   91 	ld	hl,#_ggoalx + 0
   5954 36 48         [10]   92 	ld	(hl), #0x48
   5956 C9            [10]   93 	ret
                             94 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             95 ;	---------------------------------
                             96 ; Function tilemap_render
                             97 ; ---------------------------------
   5957                      98 _tilemap_render::
                             99 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   5957 3A 93 6D      [13]  100 	ld	a, (_gtilegroundy)
   595A F5            [11]  101 	push	af
   595B 33            [ 6]  102 	inc	sp
   595C AF            [ 4]  103 	xor	a, a
   595D F5            [11]  104 	push	af
   595E 33            [ 6]  105 	inc	sp
   595F 21 00 C0      [10]  106 	ld	hl, #0xc000
   5962 E5            [11]  107 	push	hl
   5963 CD A5 6B      [17]  108 	call	_cpct_getScreenPtr
                            109 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem,      cpct_px2byteM0(1, 1), 40, 8);
   5966 E5            [11]  110 	push	hl
   5967 21 01 01      [10]  111 	ld	hl, #0x0101
   596A E5            [11]  112 	push	hl
   596B CD 81 6A      [17]  113 	call	_cpct_px2byteM0
   596E 55            [ 4]  114 	ld	d, l
   596F C1            [10]  115 	pop	bc
   5970 C5            [11]  116 	push	bc
   5971 FD E1         [14]  117 	pop	iy
   5973 C5            [11]  118 	push	bc
   5974 21 28 08      [10]  119 	ld	hl, #0x0828
   5977 E5            [11]  120 	push	hl
   5978 D5            [11]  121 	push	de
   5979 33            [ 6]  122 	inc	sp
   597A FD E5         [15]  123 	push	iy
   597C CD BB 6A      [17]  124 	call	_cpct_drawSolidBox
   597F F1            [10]  125 	pop	af
   5980 33            [ 6]  126 	inc	sp
   5981 21 01 01      [10]  127 	ld	hl,#0x0101
   5984 E3            [19]  128 	ex	(sp),hl
   5985 CD 81 6A      [17]  129 	call	_cpct_px2byteM0
   5988 55            [ 4]  130 	ld	d, l
   5989 C1            [10]  131 	pop	bc
   598A 21 28 00      [10]  132 	ld	hl, #0x0028
   598D 09            [11]  133 	add	hl,bc
   598E 4D            [ 4]  134 	ld	c, l
   598F 44            [ 4]  135 	ld	b, h
   5990 21 28 08      [10]  136 	ld	hl, #0x0828
   5993 E5            [11]  137 	push	hl
   5994 D5            [11]  138 	push	de
   5995 33            [ 6]  139 	inc	sp
   5996 C5            [11]  140 	push	bc
   5997 CD BB 6A      [17]  141 	call	_cpct_drawSolidBox
   599A F1            [10]  142 	pop	af
   599B F1            [10]  143 	pop	af
   599C 33            [ 6]  144 	inc	sp
                            145 ;src/systems/tilemap.c:25: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   599D 3A 94 6D      [13]  146 	ld	a, (_gtileplatformy)
   59A0 57            [ 4]  147 	ld	d,a
   59A1 1E 18         [ 7]  148 	ld	e,#0x18
   59A3 D5            [11]  149 	push	de
   59A4 21 00 C0      [10]  150 	ld	hl, #0xc000
   59A7 E5            [11]  151 	push	hl
   59A8 CD A5 6B      [17]  152 	call	_cpct_getScreenPtr
                            153 ;src/systems/tilemap.c:26: cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);
   59AB E5            [11]  154 	push	hl
   59AC 21 02 02      [10]  155 	ld	hl, #0x0202
   59AF E5            [11]  156 	push	hl
   59B0 CD 81 6A      [17]  157 	call	_cpct_px2byteM0
   59B3 55            [ 4]  158 	ld	d, l
   59B4 C1            [10]  159 	pop	bc
   59B5 21 20 04      [10]  160 	ld	hl, #0x0420
   59B8 E5            [11]  161 	push	hl
   59B9 D5            [11]  162 	push	de
   59BA 33            [ 6]  163 	inc	sp
   59BB C5            [11]  164 	push	bc
   59BC CD BB 6A      [17]  165 	call	_cpct_drawSolidBox
   59BF F1            [10]  166 	pop	af
   59C0 F1            [10]  167 	pop	af
   59C1 33            [ 6]  168 	inc	sp
                            169 ;src/systems/tilemap.c:28: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   59C2 21 93 6D      [10]  170 	ld	hl,#_gtilegroundy + 0
   59C5 46            [ 7]  171 	ld	b, (hl)
   59C6 05            [ 4]  172 	dec	b
   59C7 05            [ 4]  173 	dec	b
   59C8 C5            [11]  174 	push	bc
   59C9 33            [ 6]  175 	inc	sp
   59CA 3E 38         [ 7]  176 	ld	a, #0x38
   59CC F5            [11]  177 	push	af
   59CD 33            [ 6]  178 	inc	sp
   59CE 21 00 C0      [10]  179 	ld	hl, #0xc000
   59D1 E5            [11]  180 	push	hl
   59D2 CD A5 6B      [17]  181 	call	_cpct_getScreenPtr
                            182 ;src/systems/tilemap.c:29: cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);
   59D5 E5            [11]  183 	push	hl
   59D6 21 03 03      [10]  184 	ld	hl, #0x0303
   59D9 E5            [11]  185 	push	hl
   59DA CD 81 6A      [17]  186 	call	_cpct_px2byteM0
   59DD 55            [ 4]  187 	ld	d, l
   59DE C1            [10]  188 	pop	bc
   59DF 21 10 02      [10]  189 	ld	hl, #0x0210
   59E2 E5            [11]  190 	push	hl
   59E3 D5            [11]  191 	push	de
   59E4 33            [ 6]  192 	inc	sp
   59E5 C5            [11]  193 	push	bc
   59E6 CD BB 6A      [17]  194 	call	_cpct_drawSolidBox
   59E9 F1            [10]  195 	pop	af
   59EA F1            [10]  196 	pop	af
   59EB 33            [ 6]  197 	inc	sp
                            198 ;src/systems/tilemap.c:31: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   59EC 3A 93 6D      [13]  199 	ld	a,(#_gtilegroundy + 0)
   59EF C6 F0         [ 7]  200 	add	a, #0xf0
   59F1 47            [ 4]  201 	ld	b, a
   59F2 C5            [11]  202 	push	bc
   59F3 33            [ 6]  203 	inc	sp
   59F4 3A 95 6D      [13]  204 	ld	a, (_ggoalx)
   59F7 F5            [11]  205 	push	af
   59F8 33            [ 6]  206 	inc	sp
   59F9 21 00 C0      [10]  207 	ld	hl, #0xc000
   59FC E5            [11]  208 	push	hl
   59FD CD A5 6B      [17]  209 	call	_cpct_getScreenPtr
                            210 ;src/systems/tilemap.c:32: cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
   5A00 E5            [11]  211 	push	hl
   5A01 21 05 05      [10]  212 	ld	hl, #0x0505
   5A04 E5            [11]  213 	push	hl
   5A05 CD 81 6A      [17]  214 	call	_cpct_px2byteM0
   5A08 55            [ 4]  215 	ld	d, l
   5A09 C1            [10]  216 	pop	bc
   5A0A 21 02 10      [10]  217 	ld	hl, #0x1002
   5A0D E5            [11]  218 	push	hl
   5A0E D5            [11]  219 	push	de
   5A0F 33            [ 6]  220 	inc	sp
   5A10 C5            [11]  221 	push	bc
   5A11 CD BB 6A      [17]  222 	call	_cpct_drawSolidBox
   5A14 F1            [10]  223 	pop	af
   5A15 F1            [10]  224 	pop	af
   5A16 33            [ 6]  225 	inc	sp
   5A17 C9            [10]  226 	ret
                            227 ;src/systems/tilemap.c:35: u8 tilemap_ground_y(void) {
                            228 ;	---------------------------------
                            229 ; Function tilemap_ground_y
                            230 ; ---------------------------------
   5A18                     231 _tilemap_ground_y::
                            232 ;src/systems/tilemap.c:36: return gtilegroundy;
   5A18 FD 21 93 6D   [14]  233 	ld	iy, #_gtilegroundy
   5A1C FD 6E 00      [19]  234 	ld	l, 0 (iy)
   5A1F C9            [10]  235 	ret
                            236 ;src/systems/tilemap.c:39: u8 tilemap_platform_y_at(i16 x) {
                            237 ;	---------------------------------
                            238 ; Function tilemap_platform_y_at
                            239 ; ---------------------------------
   5A20                     240 _tilemap_platform_y_at::
                            241 ;src/systems/tilemap.c:40: if (x >= 24 && x <= 56) {
   5A20 FD 21 02 00   [14]  242 	ld	iy, #2
   5A24 FD 39         [15]  243 	add	iy, sp
   5A26 FD 7E 00      [19]  244 	ld	a, 0 (iy)
   5A29 D6 18         [ 7]  245 	sub	a, #0x18
   5A2B FD 7E 01      [19]  246 	ld	a, 1 (iy)
   5A2E 17            [ 4]  247 	rla
   5A2F 3F            [ 4]  248 	ccf
   5A30 1F            [ 4]  249 	rra
   5A31 DE 80         [ 7]  250 	sbc	a, #0x80
   5A33 38 1A         [12]  251 	jr	C,00102$
   5A35 3E 38         [ 7]  252 	ld	a, #0x38
   5A37 FD BE 00      [19]  253 	cp	a, 0 (iy)
   5A3A 3E 00         [ 7]  254 	ld	a, #0x00
   5A3C FD 9E 01      [19]  255 	sbc	a, 1 (iy)
   5A3F E2 44 5A      [10]  256 	jp	PO, 00114$
   5A42 EE 80         [ 7]  257 	xor	a, #0x80
   5A44                     258 00114$:
   5A44 FA 4F 5A      [10]  259 	jp	M, 00102$
                            260 ;src/systems/tilemap.c:41: return gtileplatformy;
   5A47 FD 21 94 6D   [14]  261 	ld	iy, #_gtileplatformy
   5A4B FD 6E 00      [19]  262 	ld	l, 0 (iy)
   5A4E C9            [10]  263 	ret
   5A4F                     264 00102$:
                            265 ;src/systems/tilemap.c:43: return 255;
   5A4F 2E FF         [ 7]  266 	ld	l, #0xff
   5A51 C9            [10]  267 	ret
                            268 ;src/systems/tilemap.c:46: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            269 ;	---------------------------------
                            270 ; Function tilemap_is_trap
                            271 ; ---------------------------------
   5A52                     272 _tilemap_is_trap::
   5A52 DD E5         [15]  273 	push	ix
   5A54 DD 21 00 00   [14]  274 	ld	ix,#0
   5A58 DD 39         [15]  275 	add	ix,sp
   5A5A F5            [11]  276 	push	af
                            277 ;src/systems/tilemap.c:51: left = x;
   5A5B DD 4E 04      [19]  278 	ld	c,4 (ix)
   5A5E DD 46 05      [19]  279 	ld	b,5 (ix)
                            280 ;src/systems/tilemap.c:52: right = x + (i16)w;
   5A61 DD 6E 08      [19]  281 	ld	l, 8 (ix)
   5A64 26 00         [ 7]  282 	ld	h, #0x00
   5A66 09            [11]  283 	add	hl, bc
   5A67 33            [ 6]  284 	inc	sp
   5A68 33            [ 6]  285 	inc	sp
   5A69 E5            [11]  286 	push	hl
                            287 ;src/systems/tilemap.c:53: feet = y + (i16)h;
   5A6A DD 5E 09      [19]  288 	ld	e, 9 (ix)
   5A6D 16 00         [ 7]  289 	ld	d, #0x00
   5A6F DD 6E 06      [19]  290 	ld	l,6 (ix)
   5A72 DD 66 07      [19]  291 	ld	h,7 (ix)
   5A75 19            [11]  292 	add	hl, de
   5A76 EB            [ 4]  293 	ex	de,hl
                            294 ;src/systems/tilemap.c:55: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   5A77 FD 21 93 6D   [14]  295 	ld	iy, #_gtilegroundy
   5A7B FD 6E 00      [19]  296 	ld	l, 0 (iy)
   5A7E 26 00         [ 7]  297 	ld	h, #0x00
   5A80 2B            [ 6]  298 	dec	hl
   5A81 2B            [ 6]  299 	dec	hl
   5A82 7B            [ 4]  300 	ld	a, e
   5A83 95            [ 4]  301 	sub	a, l
   5A84 7A            [ 4]  302 	ld	a, d
   5A85 9C            [ 4]  303 	sbc	a, h
   5A86 E2 8B 5A      [10]  304 	jp	PO, 00119$
   5A89 EE 80         [ 7]  305 	xor	a, #0x80
   5A8B                     306 00119$:
   5A8B FA AF 5A      [10]  307 	jp	M, 00102$
   5A8E 79            [ 4]  308 	ld	a, c
   5A8F D6 48         [ 7]  309 	sub	a, #0x48
   5A91 78            [ 4]  310 	ld	a, b
   5A92 17            [ 4]  311 	rla
   5A93 3F            [ 4]  312 	ccf
   5A94 1F            [ 4]  313 	rra
   5A95 DE 80         [ 7]  314 	sbc	a, #0x80
   5A97 30 16         [12]  315 	jr	NC,00102$
   5A99 3E 38         [ 7]  316 	ld	a, #0x38
   5A9B DD BE FE      [19]  317 	cp	a, -2 (ix)
   5A9E 3E 00         [ 7]  318 	ld	a, #0x00
   5AA0 DD 9E FF      [19]  319 	sbc	a, -1 (ix)
   5AA3 E2 A8 5A      [10]  320 	jp	PO, 00120$
   5AA6 EE 80         [ 7]  321 	xor	a, #0x80
   5AA8                     322 00120$:
   5AA8 F2 AF 5A      [10]  323 	jp	P, 00102$
                            324 ;src/systems/tilemap.c:56: return 1;
   5AAB 2E 01         [ 7]  325 	ld	l, #0x01
   5AAD 18 02         [12]  326 	jr	00105$
   5AAF                     327 00102$:
                            328 ;src/systems/tilemap.c:58: return 0;
   5AAF 2E 00         [ 7]  329 	ld	l, #0x00
   5AB1                     330 00105$:
   5AB1 DD F9         [10]  331 	ld	sp, ix
   5AB3 DD E1         [14]  332 	pop	ix
   5AB5 C9            [10]  333 	ret
                            334 ;src/systems/tilemap.c:61: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            335 ;	---------------------------------
                            336 ; Function tilemap_is_ladder
                            337 ; ---------------------------------
   5AB6                     338 _tilemap_is_ladder::
                            339 ;src/systems/tilemap.c:66: return 0;
   5AB6 2E 00         [ 7]  340 	ld	l, #0x00
   5AB8 C9            [10]  341 	ret
                            342 ;src/systems/tilemap.c:69: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            343 ;	---------------------------------
                            344 ; Function tilemap_is_hidden_zone
                            345 ; ---------------------------------
   5AB9                     346 _tilemap_is_hidden_zone::
                            347 ;src/systems/tilemap.c:74: return 0;
   5AB9 2E 00         [ 7]  348 	ld	l, #0x00
   5ABB C9            [10]  349 	ret
                            350 ;src/systems/tilemap.c:77: u8 tilemap_goal_x(void) {
                            351 ;	---------------------------------
                            352 ; Function tilemap_goal_x
                            353 ; ---------------------------------
   5ABC                     354 _tilemap_goal_x::
                            355 ;src/systems/tilemap.c:78: return ggoalx;
   5ABC FD 21 95 6D   [14]  356 	ld	iy, #_ggoalx
   5AC0 FD 6E 00      [19]  357 	ld	l, 0 (iy)
   5AC3 C9            [10]  358 	ret
                            359 	.area _CODE
                            360 	.area _INITIALIZER
   6D9C                     361 __xinit__gtilegroundy:
   6D9C A0                  362 	.db #0xa0	; 160
   6D9D                     363 __xinit__gtileplatformy:
   6D9D 80                  364 	.db #0x80	; 128
   6D9E                     365 __xinit__ggoalx:
   6D9E 48                  366 	.db #0x48	; 72	'H'
                            367 	.area _CABS (ABS)
