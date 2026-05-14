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
   5E57                      32 _gtilegroundy:
   5E57                      33 	.ds 1
   5E58                      34 _gtileplatformy:
   5E58                      35 	.ds 1
   5E59                      36 _ggoalx:
   5E59                      37 	.ds 1
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
   4EE6                      62 _tilemap_init::
                             63 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   4EE6 2A 41 50      [16]   64 	ld	hl, (_level1tilemapheight)
   4EE9 3E 02         [ 7]   65 	ld	a, #0x02
   4EEB BD            [ 4]   66 	cp	a, l
   4EEC 3E 00         [ 7]   67 	ld	a, #0x00
   4EEE 9C            [ 4]   68 	sbc	a, h
   4EEF 30 0D         [12]   69 	jr	NC,00102$
                             70 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4EF1 7D            [ 4]   71 	ld	a, l
   4EF2 C6 FE         [ 7]   72 	add	a, #0xfe
   4EF4 07            [ 4]   73 	rlca
   4EF5 07            [ 4]   74 	rlca
   4EF6 07            [ 4]   75 	rlca
   4EF7 E6 F8         [ 7]   76 	and	a, #0xf8
   4EF9 32 57 5E      [13]   77 	ld	(#_gtilegroundy + 0),a
   4EFC 18 05         [12]   78 	jr	00103$
   4EFE                      79 00102$:
                             80 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   4EFE 21 57 5E      [10]   81 	ld	hl,#_gtilegroundy + 0
   4F01 36 A0         [10]   82 	ld	(hl), #0xa0
   4F03                      83 00103$:
                             84 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   4F03 21 58 5E      [10]   85 	ld	hl, #_gtileplatformy
   4F06 3A 57 5E      [13]   86 	ld	a,(#_gtilegroundy + 0)
   4F09 C6 E8         [ 7]   87 	add	a, #0xe8
   4F0B 77            [ 7]   88 	ld	(hl), a
                             89 ;src/systems/tilemap.c:16: ggoalx = 72;
   4F0C 21 59 5E      [10]   90 	ld	hl,#_ggoalx + 0
   4F0F 36 48         [10]   91 	ld	(hl), #0x48
   4F11 C9            [10]   92 	ret
                             93 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             94 ;	---------------------------------
                             95 ; Function tilemap_render
                             96 ; ---------------------------------
   4F12                      97 _tilemap_render::
                             98 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4F12 3A 57 5E      [13]   99 	ld	a, (_gtilegroundy)
   4F15 F5            [11]  100 	push	af
   4F16 33            [ 6]  101 	inc	sp
   4F17 AF            [ 4]  102 	xor	a, a
   4F18 F5            [11]  103 	push	af
   4F19 33            [ 6]  104 	inc	sp
   4F1A 21 00 C0      [10]  105 	ld	hl, #0xc000
   4F1D E5            [11]  106 	push	hl
   4F1E CD 74 5D      [17]  107 	call	_cpct_getScreenPtr
                            108 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4F21 01 50 08      [10]  109 	ld	bc, #0x0850
   4F24 C5            [11]  110 	push	bc
   4F25 3E 11         [ 7]  111 	ld	a, #0x11
   4F27 F5            [11]  112 	push	af
   4F28 33            [ 6]  113 	inc	sp
   4F29 E5            [11]  114 	push	hl
   4F2A CD BB 5C      [17]  115 	call	_cpct_drawSolidBox
   4F2D F1            [10]  116 	pop	af
   4F2E F1            [10]  117 	pop	af
   4F2F 33            [ 6]  118 	inc	sp
                            119 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   4F30 3A 58 5E      [13]  120 	ld	a, (_gtileplatformy)
   4F33 57            [ 4]  121 	ld	d,a
   4F34 1E 18         [ 7]  122 	ld	e,#0x18
   4F36 D5            [11]  123 	push	de
   4F37 21 00 C0      [10]  124 	ld	hl, #0xc000
   4F3A E5            [11]  125 	push	hl
   4F3B CD 74 5D      [17]  126 	call	_cpct_getScreenPtr
                            127 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   4F3E 01 20 04      [10]  128 	ld	bc, #0x0420
   4F41 C5            [11]  129 	push	bc
   4F42 3E 33         [ 7]  130 	ld	a, #0x33
   4F44 F5            [11]  131 	push	af
   4F45 33            [ 6]  132 	inc	sp
   4F46 E5            [11]  133 	push	hl
   4F47 CD BB 5C      [17]  134 	call	_cpct_drawSolidBox
   4F4A F1            [10]  135 	pop	af
   4F4B F1            [10]  136 	pop	af
   4F4C 33            [ 6]  137 	inc	sp
                            138 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   4F4D 21 57 5E      [10]  139 	ld	hl,#_gtilegroundy + 0
   4F50 46            [ 7]  140 	ld	b, (hl)
   4F51 05            [ 4]  141 	dec	b
   4F52 05            [ 4]  142 	dec	b
   4F53 C5            [11]  143 	push	bc
   4F54 33            [ 6]  144 	inc	sp
   4F55 3E 38         [ 7]  145 	ld	a, #0x38
   4F57 F5            [11]  146 	push	af
   4F58 33            [ 6]  147 	inc	sp
   4F59 21 00 C0      [10]  148 	ld	hl, #0xc000
   4F5C E5            [11]  149 	push	hl
   4F5D CD 74 5D      [17]  150 	call	_cpct_getScreenPtr
                            151 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   4F60 01 10 02      [10]  152 	ld	bc, #0x0210
   4F63 C5            [11]  153 	push	bc
   4F64 3E 66         [ 7]  154 	ld	a, #0x66
   4F66 F5            [11]  155 	push	af
   4F67 33            [ 6]  156 	inc	sp
   4F68 E5            [11]  157 	push	hl
   4F69 CD BB 5C      [17]  158 	call	_cpct_drawSolidBox
   4F6C F1            [10]  159 	pop	af
   4F6D F1            [10]  160 	pop	af
   4F6E 33            [ 6]  161 	inc	sp
                            162 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   4F6F 3A 57 5E      [13]  163 	ld	a,(#_gtilegroundy + 0)
   4F72 C6 F0         [ 7]  164 	add	a, #0xf0
   4F74 47            [ 4]  165 	ld	b, a
   4F75 C5            [11]  166 	push	bc
   4F76 33            [ 6]  167 	inc	sp
   4F77 3A 59 5E      [13]  168 	ld	a, (_ggoalx)
   4F7A F5            [11]  169 	push	af
   4F7B 33            [ 6]  170 	inc	sp
   4F7C 21 00 C0      [10]  171 	ld	hl, #0xc000
   4F7F E5            [11]  172 	push	hl
   4F80 CD 74 5D      [17]  173 	call	_cpct_getScreenPtr
                            174 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   4F83 01 02 10      [10]  175 	ld	bc, #0x1002
   4F86 C5            [11]  176 	push	bc
   4F87 3E 5F         [ 7]  177 	ld	a, #0x5f
   4F89 F5            [11]  178 	push	af
   4F8A 33            [ 6]  179 	inc	sp
   4F8B E5            [11]  180 	push	hl
   4F8C CD BB 5C      [17]  181 	call	_cpct_drawSolidBox
   4F8F F1            [10]  182 	pop	af
   4F90 F1            [10]  183 	pop	af
   4F91 33            [ 6]  184 	inc	sp
   4F92 C9            [10]  185 	ret
                            186 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            187 ;	---------------------------------
                            188 ; Function tilemap_ground_y
                            189 ; ---------------------------------
   4F93                     190 _tilemap_ground_y::
                            191 ;src/systems/tilemap.c:35: return gtilegroundy;
   4F93 FD 21 57 5E   [14]  192 	ld	iy, #_gtilegroundy
   4F97 FD 6E 00      [19]  193 	ld	l, 0 (iy)
   4F9A C9            [10]  194 	ret
                            195 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            196 ;	---------------------------------
                            197 ; Function tilemap_platform_y_at
                            198 ; ---------------------------------
   4F9B                     199 _tilemap_platform_y_at::
                            200 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   4F9B FD 21 02 00   [14]  201 	ld	iy, #2
   4F9F FD 39         [15]  202 	add	iy, sp
   4FA1 FD 7E 00      [19]  203 	ld	a, 0 (iy)
   4FA4 D6 18         [ 7]  204 	sub	a, #0x18
   4FA6 FD 7E 01      [19]  205 	ld	a, 1 (iy)
   4FA9 17            [ 4]  206 	rla
   4FAA 3F            [ 4]  207 	ccf
   4FAB 1F            [ 4]  208 	rra
   4FAC DE 80         [ 7]  209 	sbc	a, #0x80
   4FAE 38 1A         [12]  210 	jr	C,00102$
   4FB0 3E 38         [ 7]  211 	ld	a, #0x38
   4FB2 FD BE 00      [19]  212 	cp	a, 0 (iy)
   4FB5 3E 00         [ 7]  213 	ld	a, #0x00
   4FB7 FD 9E 01      [19]  214 	sbc	a, 1 (iy)
   4FBA E2 BF 4F      [10]  215 	jp	PO, 00114$
   4FBD EE 80         [ 7]  216 	xor	a, #0x80
   4FBF                     217 00114$:
   4FBF FA CA 4F      [10]  218 	jp	M, 00102$
                            219 ;src/systems/tilemap.c:40: return gtileplatformy;
   4FC2 FD 21 58 5E   [14]  220 	ld	iy, #_gtileplatformy
   4FC6 FD 6E 00      [19]  221 	ld	l, 0 (iy)
   4FC9 C9            [10]  222 	ret
   4FCA                     223 00102$:
                            224 ;src/systems/tilemap.c:42: return 255;
   4FCA 2E FF         [ 7]  225 	ld	l, #0xff
   4FCC C9            [10]  226 	ret
                            227 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            228 ;	---------------------------------
                            229 ; Function tilemap_is_trap
                            230 ; ---------------------------------
   4FCD                     231 _tilemap_is_trap::
   4FCD DD E5         [15]  232 	push	ix
   4FCF DD 21 00 00   [14]  233 	ld	ix,#0
   4FD3 DD 39         [15]  234 	add	ix,sp
   4FD5 F5            [11]  235 	push	af
                            236 ;src/systems/tilemap.c:50: left = x;
   4FD6 DD 4E 04      [19]  237 	ld	c,4 (ix)
   4FD9 DD 46 05      [19]  238 	ld	b,5 (ix)
                            239 ;src/systems/tilemap.c:51: right = x + (i16)w;
   4FDC DD 6E 08      [19]  240 	ld	l, 8 (ix)
   4FDF 26 00         [ 7]  241 	ld	h, #0x00
   4FE1 09            [11]  242 	add	hl, bc
   4FE2 33            [ 6]  243 	inc	sp
   4FE3 33            [ 6]  244 	inc	sp
   4FE4 E5            [11]  245 	push	hl
                            246 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   4FE5 DD 5E 09      [19]  247 	ld	e, 9 (ix)
   4FE8 16 00         [ 7]  248 	ld	d, #0x00
   4FEA DD 6E 06      [19]  249 	ld	l,6 (ix)
   4FED DD 66 07      [19]  250 	ld	h,7 (ix)
   4FF0 19            [11]  251 	add	hl, de
   4FF1 EB            [ 4]  252 	ex	de,hl
                            253 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   4FF2 FD 21 57 5E   [14]  254 	ld	iy, #_gtilegroundy
   4FF6 FD 6E 00      [19]  255 	ld	l, 0 (iy)
   4FF9 26 00         [ 7]  256 	ld	h, #0x00
   4FFB 2B            [ 6]  257 	dec	hl
   4FFC 2B            [ 6]  258 	dec	hl
   4FFD 7B            [ 4]  259 	ld	a, e
   4FFE 95            [ 4]  260 	sub	a, l
   4FFF 7A            [ 4]  261 	ld	a, d
   5000 9C            [ 4]  262 	sbc	a, h
   5001 E2 06 50      [10]  263 	jp	PO, 00119$
   5004 EE 80         [ 7]  264 	xor	a, #0x80
   5006                     265 00119$:
   5006 FA 2A 50      [10]  266 	jp	M, 00102$
   5009 79            [ 4]  267 	ld	a, c
   500A D6 48         [ 7]  268 	sub	a, #0x48
   500C 78            [ 4]  269 	ld	a, b
   500D 17            [ 4]  270 	rla
   500E 3F            [ 4]  271 	ccf
   500F 1F            [ 4]  272 	rra
   5010 DE 80         [ 7]  273 	sbc	a, #0x80
   5012 30 16         [12]  274 	jr	NC,00102$
   5014 3E 38         [ 7]  275 	ld	a, #0x38
   5016 DD BE FE      [19]  276 	cp	a, -2 (ix)
   5019 3E 00         [ 7]  277 	ld	a, #0x00
   501B DD 9E FF      [19]  278 	sbc	a, -1 (ix)
   501E E2 23 50      [10]  279 	jp	PO, 00120$
   5021 EE 80         [ 7]  280 	xor	a, #0x80
   5023                     281 00120$:
   5023 F2 2A 50      [10]  282 	jp	P, 00102$
                            283 ;src/systems/tilemap.c:55: return 1;
   5026 2E 01         [ 7]  284 	ld	l, #0x01
   5028 18 02         [12]  285 	jr	00105$
   502A                     286 00102$:
                            287 ;src/systems/tilemap.c:57: return 0;
   502A 2E 00         [ 7]  288 	ld	l, #0x00
   502C                     289 00105$:
   502C DD F9         [10]  290 	ld	sp, ix
   502E DD E1         [14]  291 	pop	ix
   5030 C9            [10]  292 	ret
                            293 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            294 ;	---------------------------------
                            295 ; Function tilemap_is_ladder
                            296 ; ---------------------------------
   5031                     297 _tilemap_is_ladder::
                            298 ;src/systems/tilemap.c:65: return 0;
   5031 2E 00         [ 7]  299 	ld	l, #0x00
   5033 C9            [10]  300 	ret
                            301 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            302 ;	---------------------------------
                            303 ; Function tilemap_is_hidden_zone
                            304 ; ---------------------------------
   5034                     305 _tilemap_is_hidden_zone::
                            306 ;src/systems/tilemap.c:73: return 0;
   5034 2E 00         [ 7]  307 	ld	l, #0x00
   5036 C9            [10]  308 	ret
                            309 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            310 ;	---------------------------------
                            311 ; Function tilemap_goal_x
                            312 ; ---------------------------------
   5037                     313 _tilemap_goal_x::
                            314 ;src/systems/tilemap.c:77: return ggoalx;
   5037 FD 21 59 5E   [14]  315 	ld	iy, #_ggoalx
   503B FD 6E 00      [19]  316 	ld	l, 0 (iy)
   503E C9            [10]  317 	ret
                            318 	.area _CODE
                            319 	.area _INITIALIZER
   5E72                     320 __xinit__gtilegroundy:
   5E72 A0                  321 	.db #0xa0	; 160
   5E73                     322 __xinit__gtileplatformy:
   5E73 80                  323 	.db #0x80	; 128
   5E74                     324 __xinit__ggoalx:
   5E74 48                  325 	.db #0x48	; 72	'H'
                            326 	.area _CABS (ABS)
