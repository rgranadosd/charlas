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
   5E5F                      32 _gtilegroundy:
   5E5F                      33 	.ds 1
   5E60                      34 _gtileplatformy:
   5E60                      35 	.ds 1
   5E61                      36 _ggoalx:
   5E61                      37 	.ds 1
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
   4EE4                      62 _tilemap_init::
                             63 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   4EE4 2A 3F 50      [16]   64 	ld	hl, (_level1tilemapheight)
   4EE7 3E 02         [ 7]   65 	ld	a, #0x02
   4EE9 BD            [ 4]   66 	cp	a, l
   4EEA 3E 00         [ 7]   67 	ld	a, #0x00
   4EEC 9C            [ 4]   68 	sbc	a, h
   4EED 30 0D         [12]   69 	jr	NC,00102$
                             70 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4EEF 7D            [ 4]   71 	ld	a, l
   4EF0 C6 FE         [ 7]   72 	add	a, #0xfe
   4EF2 07            [ 4]   73 	rlca
   4EF3 07            [ 4]   74 	rlca
   4EF4 07            [ 4]   75 	rlca
   4EF5 E6 F8         [ 7]   76 	and	a, #0xf8
   4EF7 32 5F 5E      [13]   77 	ld	(#_gtilegroundy + 0),a
   4EFA 18 05         [12]   78 	jr	00103$
   4EFC                      79 00102$:
                             80 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   4EFC 21 5F 5E      [10]   81 	ld	hl,#_gtilegroundy + 0
   4EFF 36 A0         [10]   82 	ld	(hl), #0xa0
   4F01                      83 00103$:
                             84 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   4F01 21 60 5E      [10]   85 	ld	hl, #_gtileplatformy
   4F04 3A 5F 5E      [13]   86 	ld	a,(#_gtilegroundy + 0)
   4F07 C6 E8         [ 7]   87 	add	a, #0xe8
   4F09 77            [ 7]   88 	ld	(hl), a
                             89 ;src/systems/tilemap.c:16: ggoalx = 72;
   4F0A 21 61 5E      [10]   90 	ld	hl,#_ggoalx + 0
   4F0D 36 48         [10]   91 	ld	(hl), #0x48
   4F0F C9            [10]   92 	ret
                             93 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             94 ;	---------------------------------
                             95 ; Function tilemap_render
                             96 ; ---------------------------------
   4F10                      97 _tilemap_render::
                             98 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4F10 3A 5F 5E      [13]   99 	ld	a, (_gtilegroundy)
   4F13 F5            [11]  100 	push	af
   4F14 33            [ 6]  101 	inc	sp
   4F15 AF            [ 4]  102 	xor	a, a
   4F16 F5            [11]  103 	push	af
   4F17 33            [ 6]  104 	inc	sp
   4F18 21 00 C0      [10]  105 	ld	hl, #0xc000
   4F1B E5            [11]  106 	push	hl
   4F1C CD 7C 5D      [17]  107 	call	_cpct_getScreenPtr
                            108 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4F1F 01 50 08      [10]  109 	ld	bc, #0x0850
   4F22 C5            [11]  110 	push	bc
   4F23 3E 11         [ 7]  111 	ld	a, #0x11
   4F25 F5            [11]  112 	push	af
   4F26 33            [ 6]  113 	inc	sp
   4F27 E5            [11]  114 	push	hl
   4F28 CD C3 5C      [17]  115 	call	_cpct_drawSolidBox
   4F2B F1            [10]  116 	pop	af
   4F2C F1            [10]  117 	pop	af
   4F2D 33            [ 6]  118 	inc	sp
                            119 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   4F2E 3A 60 5E      [13]  120 	ld	a, (_gtileplatformy)
   4F31 57            [ 4]  121 	ld	d,a
   4F32 1E 18         [ 7]  122 	ld	e,#0x18
   4F34 D5            [11]  123 	push	de
   4F35 21 00 C0      [10]  124 	ld	hl, #0xc000
   4F38 E5            [11]  125 	push	hl
   4F39 CD 7C 5D      [17]  126 	call	_cpct_getScreenPtr
                            127 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   4F3C 01 20 04      [10]  128 	ld	bc, #0x0420
   4F3F C5            [11]  129 	push	bc
   4F40 3E 33         [ 7]  130 	ld	a, #0x33
   4F42 F5            [11]  131 	push	af
   4F43 33            [ 6]  132 	inc	sp
   4F44 E5            [11]  133 	push	hl
   4F45 CD C3 5C      [17]  134 	call	_cpct_drawSolidBox
   4F48 F1            [10]  135 	pop	af
   4F49 F1            [10]  136 	pop	af
   4F4A 33            [ 6]  137 	inc	sp
                            138 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   4F4B 21 5F 5E      [10]  139 	ld	hl,#_gtilegroundy + 0
   4F4E 46            [ 7]  140 	ld	b, (hl)
   4F4F 05            [ 4]  141 	dec	b
   4F50 05            [ 4]  142 	dec	b
   4F51 C5            [11]  143 	push	bc
   4F52 33            [ 6]  144 	inc	sp
   4F53 3E 38         [ 7]  145 	ld	a, #0x38
   4F55 F5            [11]  146 	push	af
   4F56 33            [ 6]  147 	inc	sp
   4F57 21 00 C0      [10]  148 	ld	hl, #0xc000
   4F5A E5            [11]  149 	push	hl
   4F5B CD 7C 5D      [17]  150 	call	_cpct_getScreenPtr
                            151 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   4F5E 01 10 02      [10]  152 	ld	bc, #0x0210
   4F61 C5            [11]  153 	push	bc
   4F62 3E 66         [ 7]  154 	ld	a, #0x66
   4F64 F5            [11]  155 	push	af
   4F65 33            [ 6]  156 	inc	sp
   4F66 E5            [11]  157 	push	hl
   4F67 CD C3 5C      [17]  158 	call	_cpct_drawSolidBox
   4F6A F1            [10]  159 	pop	af
   4F6B F1            [10]  160 	pop	af
   4F6C 33            [ 6]  161 	inc	sp
                            162 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   4F6D 3A 5F 5E      [13]  163 	ld	a,(#_gtilegroundy + 0)
   4F70 C6 F0         [ 7]  164 	add	a, #0xf0
   4F72 47            [ 4]  165 	ld	b, a
   4F73 C5            [11]  166 	push	bc
   4F74 33            [ 6]  167 	inc	sp
   4F75 3A 61 5E      [13]  168 	ld	a, (_ggoalx)
   4F78 F5            [11]  169 	push	af
   4F79 33            [ 6]  170 	inc	sp
   4F7A 21 00 C0      [10]  171 	ld	hl, #0xc000
   4F7D E5            [11]  172 	push	hl
   4F7E CD 7C 5D      [17]  173 	call	_cpct_getScreenPtr
                            174 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   4F81 01 02 10      [10]  175 	ld	bc, #0x1002
   4F84 C5            [11]  176 	push	bc
   4F85 3E 5F         [ 7]  177 	ld	a, #0x5f
   4F87 F5            [11]  178 	push	af
   4F88 33            [ 6]  179 	inc	sp
   4F89 E5            [11]  180 	push	hl
   4F8A CD C3 5C      [17]  181 	call	_cpct_drawSolidBox
   4F8D F1            [10]  182 	pop	af
   4F8E F1            [10]  183 	pop	af
   4F8F 33            [ 6]  184 	inc	sp
   4F90 C9            [10]  185 	ret
                            186 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            187 ;	---------------------------------
                            188 ; Function tilemap_ground_y
                            189 ; ---------------------------------
   4F91                     190 _tilemap_ground_y::
                            191 ;src/systems/tilemap.c:35: return gtilegroundy;
   4F91 FD 21 5F 5E   [14]  192 	ld	iy, #_gtilegroundy
   4F95 FD 6E 00      [19]  193 	ld	l, 0 (iy)
   4F98 C9            [10]  194 	ret
                            195 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            196 ;	---------------------------------
                            197 ; Function tilemap_platform_y_at
                            198 ; ---------------------------------
   4F99                     199 _tilemap_platform_y_at::
                            200 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   4F99 FD 21 02 00   [14]  201 	ld	iy, #2
   4F9D FD 39         [15]  202 	add	iy, sp
   4F9F FD 7E 00      [19]  203 	ld	a, 0 (iy)
   4FA2 D6 18         [ 7]  204 	sub	a, #0x18
   4FA4 FD 7E 01      [19]  205 	ld	a, 1 (iy)
   4FA7 17            [ 4]  206 	rla
   4FA8 3F            [ 4]  207 	ccf
   4FA9 1F            [ 4]  208 	rra
   4FAA DE 80         [ 7]  209 	sbc	a, #0x80
   4FAC 38 1A         [12]  210 	jr	C,00102$
   4FAE 3E 38         [ 7]  211 	ld	a, #0x38
   4FB0 FD BE 00      [19]  212 	cp	a, 0 (iy)
   4FB3 3E 00         [ 7]  213 	ld	a, #0x00
   4FB5 FD 9E 01      [19]  214 	sbc	a, 1 (iy)
   4FB8 E2 BD 4F      [10]  215 	jp	PO, 00114$
   4FBB EE 80         [ 7]  216 	xor	a, #0x80
   4FBD                     217 00114$:
   4FBD FA C8 4F      [10]  218 	jp	M, 00102$
                            219 ;src/systems/tilemap.c:40: return gtileplatformy;
   4FC0 FD 21 60 5E   [14]  220 	ld	iy, #_gtileplatformy
   4FC4 FD 6E 00      [19]  221 	ld	l, 0 (iy)
   4FC7 C9            [10]  222 	ret
   4FC8                     223 00102$:
                            224 ;src/systems/tilemap.c:42: return 255;
   4FC8 2E FF         [ 7]  225 	ld	l, #0xff
   4FCA C9            [10]  226 	ret
                            227 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            228 ;	---------------------------------
                            229 ; Function tilemap_is_trap
                            230 ; ---------------------------------
   4FCB                     231 _tilemap_is_trap::
   4FCB DD E5         [15]  232 	push	ix
   4FCD DD 21 00 00   [14]  233 	ld	ix,#0
   4FD1 DD 39         [15]  234 	add	ix,sp
   4FD3 F5            [11]  235 	push	af
                            236 ;src/systems/tilemap.c:50: left = x;
   4FD4 DD 4E 04      [19]  237 	ld	c,4 (ix)
   4FD7 DD 46 05      [19]  238 	ld	b,5 (ix)
                            239 ;src/systems/tilemap.c:51: right = x + (i16)w;
   4FDA DD 6E 08      [19]  240 	ld	l, 8 (ix)
   4FDD 26 00         [ 7]  241 	ld	h, #0x00
   4FDF 09            [11]  242 	add	hl, bc
   4FE0 33            [ 6]  243 	inc	sp
   4FE1 33            [ 6]  244 	inc	sp
   4FE2 E5            [11]  245 	push	hl
                            246 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   4FE3 DD 5E 09      [19]  247 	ld	e, 9 (ix)
   4FE6 16 00         [ 7]  248 	ld	d, #0x00
   4FE8 DD 6E 06      [19]  249 	ld	l,6 (ix)
   4FEB DD 66 07      [19]  250 	ld	h,7 (ix)
   4FEE 19            [11]  251 	add	hl, de
   4FEF EB            [ 4]  252 	ex	de,hl
                            253 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   4FF0 FD 21 5F 5E   [14]  254 	ld	iy, #_gtilegroundy
   4FF4 FD 6E 00      [19]  255 	ld	l, 0 (iy)
   4FF7 26 00         [ 7]  256 	ld	h, #0x00
   4FF9 2B            [ 6]  257 	dec	hl
   4FFA 2B            [ 6]  258 	dec	hl
   4FFB 7B            [ 4]  259 	ld	a, e
   4FFC 95            [ 4]  260 	sub	a, l
   4FFD 7A            [ 4]  261 	ld	a, d
   4FFE 9C            [ 4]  262 	sbc	a, h
   4FFF E2 04 50      [10]  263 	jp	PO, 00119$
   5002 EE 80         [ 7]  264 	xor	a, #0x80
   5004                     265 00119$:
   5004 FA 28 50      [10]  266 	jp	M, 00102$
   5007 79            [ 4]  267 	ld	a, c
   5008 D6 48         [ 7]  268 	sub	a, #0x48
   500A 78            [ 4]  269 	ld	a, b
   500B 17            [ 4]  270 	rla
   500C 3F            [ 4]  271 	ccf
   500D 1F            [ 4]  272 	rra
   500E DE 80         [ 7]  273 	sbc	a, #0x80
   5010 30 16         [12]  274 	jr	NC,00102$
   5012 3E 38         [ 7]  275 	ld	a, #0x38
   5014 DD BE FE      [19]  276 	cp	a, -2 (ix)
   5017 3E 00         [ 7]  277 	ld	a, #0x00
   5019 DD 9E FF      [19]  278 	sbc	a, -1 (ix)
   501C E2 21 50      [10]  279 	jp	PO, 00120$
   501F EE 80         [ 7]  280 	xor	a, #0x80
   5021                     281 00120$:
   5021 F2 28 50      [10]  282 	jp	P, 00102$
                            283 ;src/systems/tilemap.c:55: return 1;
   5024 2E 01         [ 7]  284 	ld	l, #0x01
   5026 18 02         [12]  285 	jr	00105$
   5028                     286 00102$:
                            287 ;src/systems/tilemap.c:57: return 0;
   5028 2E 00         [ 7]  288 	ld	l, #0x00
   502A                     289 00105$:
   502A DD F9         [10]  290 	ld	sp, ix
   502C DD E1         [14]  291 	pop	ix
   502E C9            [10]  292 	ret
                            293 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            294 ;	---------------------------------
                            295 ; Function tilemap_is_ladder
                            296 ; ---------------------------------
   502F                     297 _tilemap_is_ladder::
                            298 ;src/systems/tilemap.c:65: return 0;
   502F 2E 00         [ 7]  299 	ld	l, #0x00
   5031 C9            [10]  300 	ret
                            301 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            302 ;	---------------------------------
                            303 ; Function tilemap_is_hidden_zone
                            304 ; ---------------------------------
   5032                     305 _tilemap_is_hidden_zone::
                            306 ;src/systems/tilemap.c:73: return 0;
   5032 2E 00         [ 7]  307 	ld	l, #0x00
   5034 C9            [10]  308 	ret
                            309 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            310 ;	---------------------------------
                            311 ; Function tilemap_goal_x
                            312 ; ---------------------------------
   5035                     313 _tilemap_goal_x::
                            314 ;src/systems/tilemap.c:77: return ggoalx;
   5035 FD 21 61 5E   [14]  315 	ld	iy, #_ggoalx
   5039 FD 6E 00      [19]  316 	ld	l, 0 (iy)
   503C C9            [10]  317 	ret
                            318 	.area _CODE
                            319 	.area _INITIALIZER
   5E7A                     320 __xinit__gtilegroundy:
   5E7A A0                  321 	.db #0xa0	; 160
   5E7B                     322 __xinit__gtileplatformy:
   5E7B 80                  323 	.db #0x80	; 128
   5E7C                     324 __xinit__ggoalx:
   5E7C 48                  325 	.db #0x48	; 72	'H'
                            326 	.area _CABS (ABS)
