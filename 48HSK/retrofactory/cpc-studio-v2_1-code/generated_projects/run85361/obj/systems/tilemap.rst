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
   5D96                      32 _gtilegroundy:
   5D96                      33 	.ds 1
   5D97                      34 _gtileplatformy:
   5D97                      35 	.ds 1
   5D98                      36 _ggoalx:
   5D98                      37 	.ds 1
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
   4E9A                      62 _tilemap_init::
                             63 ;src/systems/tilemap.c:10: if (level1tilemapheight > 2) {
   4E9A 2A F5 4F      [16]   64 	ld	hl, (_level1tilemapheight)
   4E9D 3E 02         [ 7]   65 	ld	a, #0x02
   4E9F BD            [ 4]   66 	cp	a, l
   4EA0 3E 00         [ 7]   67 	ld	a, #0x00
   4EA2 9C            [ 4]   68 	sbc	a, h
   4EA3 30 0D         [12]   69 	jr	NC,00102$
                             70 ;src/systems/tilemap.c:11: gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
   4EA5 7D            [ 4]   71 	ld	a, l
   4EA6 C6 FE         [ 7]   72 	add	a, #0xfe
   4EA8 07            [ 4]   73 	rlca
   4EA9 07            [ 4]   74 	rlca
   4EAA 07            [ 4]   75 	rlca
   4EAB E6 F8         [ 7]   76 	and	a, #0xf8
   4EAD 32 96 5D      [13]   77 	ld	(#_gtilegroundy + 0),a
   4EB0 18 05         [12]   78 	jr	00103$
   4EB2                      79 00102$:
                             80 ;src/systems/tilemap.c:13: gtilegroundy = 160;
   4EB2 21 96 5D      [10]   81 	ld	hl,#_gtilegroundy + 0
   4EB5 36 A0         [10]   82 	ld	(hl), #0xa0
   4EB7                      83 00103$:
                             84 ;src/systems/tilemap.c:15: gtileplatformy = (u8)(gtilegroundy - 24);
   4EB7 21 97 5D      [10]   85 	ld	hl, #_gtileplatformy
   4EBA 3A 96 5D      [13]   86 	ld	a,(#_gtilegroundy + 0)
   4EBD C6 E8         [ 7]   87 	add	a, #0xe8
   4EBF 77            [ 7]   88 	ld	(hl), a
                             89 ;src/systems/tilemap.c:16: ggoalx = 72;
   4EC0 21 98 5D      [10]   90 	ld	hl,#_ggoalx + 0
   4EC3 36 48         [10]   91 	ld	(hl), #0x48
   4EC5 C9            [10]   92 	ret
                             93 ;src/systems/tilemap.c:19: void tilemap_render(void) {
                             94 ;	---------------------------------
                             95 ; Function tilemap_render
                             96 ; ---------------------------------
   4EC6                      97 _tilemap_render::
                             98 ;src/systems/tilemap.c:21: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
   4EC6 3A 96 5D      [13]   99 	ld	a, (_gtilegroundy)
   4EC9 F5            [11]  100 	push	af
   4ECA 33            [ 6]  101 	inc	sp
   4ECB AF            [ 4]  102 	xor	a, a
   4ECC F5            [11]  103 	push	af
   4ECD 33            [ 6]  104 	inc	sp
   4ECE 21 00 C0      [10]  105 	ld	hl, #0xc000
   4ED1 E5            [11]  106 	push	hl
   4ED2 CD B3 5C      [17]  107 	call	_cpct_getScreenPtr
                            108 ;src/systems/tilemap.c:22: cpct_drawSolidBox(pvmem, 0x11, 80, 8);
   4ED5 01 50 08      [10]  109 	ld	bc, #0x0850
   4ED8 C5            [11]  110 	push	bc
   4ED9 3E 11         [ 7]  111 	ld	a, #0x11
   4EDB F5            [11]  112 	push	af
   4EDC 33            [ 6]  113 	inc	sp
   4EDD E5            [11]  114 	push	hl
   4EDE CD FA 5B      [17]  115 	call	_cpct_drawSolidBox
   4EE1 F1            [10]  116 	pop	af
   4EE2 F1            [10]  117 	pop	af
   4EE3 33            [ 6]  118 	inc	sp
                            119 ;src/systems/tilemap.c:24: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
   4EE4 3A 97 5D      [13]  120 	ld	a, (_gtileplatformy)
   4EE7 57            [ 4]  121 	ld	d,a
   4EE8 1E 18         [ 7]  122 	ld	e,#0x18
   4EEA D5            [11]  123 	push	de
   4EEB 21 00 C0      [10]  124 	ld	hl, #0xc000
   4EEE E5            [11]  125 	push	hl
   4EEF CD B3 5C      [17]  126 	call	_cpct_getScreenPtr
                            127 ;src/systems/tilemap.c:25: cpct_drawSolidBox(pvmem, 0x33, 32, 4);
   4EF2 01 20 04      [10]  128 	ld	bc, #0x0420
   4EF5 C5            [11]  129 	push	bc
   4EF6 3E 33         [ 7]  130 	ld	a, #0x33
   4EF8 F5            [11]  131 	push	af
   4EF9 33            [ 6]  132 	inc	sp
   4EFA E5            [11]  133 	push	hl
   4EFB CD FA 5B      [17]  134 	call	_cpct_drawSolidBox
   4EFE F1            [10]  135 	pop	af
   4EFF F1            [10]  136 	pop	af
   4F00 33            [ 6]  137 	inc	sp
                            138 ;src/systems/tilemap.c:27: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
   4F01 21 96 5D      [10]  139 	ld	hl,#_gtilegroundy + 0
   4F04 46            [ 7]  140 	ld	b, (hl)
   4F05 05            [ 4]  141 	dec	b
   4F06 05            [ 4]  142 	dec	b
   4F07 C5            [11]  143 	push	bc
   4F08 33            [ 6]  144 	inc	sp
   4F09 3E 38         [ 7]  145 	ld	a, #0x38
   4F0B F5            [11]  146 	push	af
   4F0C 33            [ 6]  147 	inc	sp
   4F0D 21 00 C0      [10]  148 	ld	hl, #0xc000
   4F10 E5            [11]  149 	push	hl
   4F11 CD B3 5C      [17]  150 	call	_cpct_getScreenPtr
                            151 ;src/systems/tilemap.c:28: cpct_drawSolidBox(pvmem, 0x66, 16, 2);
   4F14 01 10 02      [10]  152 	ld	bc, #0x0210
   4F17 C5            [11]  153 	push	bc
   4F18 3E 66         [ 7]  154 	ld	a, #0x66
   4F1A F5            [11]  155 	push	af
   4F1B 33            [ 6]  156 	inc	sp
   4F1C E5            [11]  157 	push	hl
   4F1D CD FA 5B      [17]  158 	call	_cpct_drawSolidBox
   4F20 F1            [10]  159 	pop	af
   4F21 F1            [10]  160 	pop	af
   4F22 33            [ 6]  161 	inc	sp
                            162 ;src/systems/tilemap.c:30: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
   4F23 3A 96 5D      [13]  163 	ld	a,(#_gtilegroundy + 0)
   4F26 C6 F0         [ 7]  164 	add	a, #0xf0
   4F28 47            [ 4]  165 	ld	b, a
   4F29 C5            [11]  166 	push	bc
   4F2A 33            [ 6]  167 	inc	sp
   4F2B 3A 98 5D      [13]  168 	ld	a, (_ggoalx)
   4F2E F5            [11]  169 	push	af
   4F2F 33            [ 6]  170 	inc	sp
   4F30 21 00 C0      [10]  171 	ld	hl, #0xc000
   4F33 E5            [11]  172 	push	hl
   4F34 CD B3 5C      [17]  173 	call	_cpct_getScreenPtr
                            174 ;src/systems/tilemap.c:31: cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
   4F37 01 02 10      [10]  175 	ld	bc, #0x1002
   4F3A C5            [11]  176 	push	bc
   4F3B 3E 5F         [ 7]  177 	ld	a, #0x5f
   4F3D F5            [11]  178 	push	af
   4F3E 33            [ 6]  179 	inc	sp
   4F3F E5            [11]  180 	push	hl
   4F40 CD FA 5B      [17]  181 	call	_cpct_drawSolidBox
   4F43 F1            [10]  182 	pop	af
   4F44 F1            [10]  183 	pop	af
   4F45 33            [ 6]  184 	inc	sp
   4F46 C9            [10]  185 	ret
                            186 ;src/systems/tilemap.c:34: u8 tilemap_ground_y(void) {
                            187 ;	---------------------------------
                            188 ; Function tilemap_ground_y
                            189 ; ---------------------------------
   4F47                     190 _tilemap_ground_y::
                            191 ;src/systems/tilemap.c:35: return gtilegroundy;
   4F47 FD 21 96 5D   [14]  192 	ld	iy, #_gtilegroundy
   4F4B FD 6E 00      [19]  193 	ld	l, 0 (iy)
   4F4E C9            [10]  194 	ret
                            195 ;src/systems/tilemap.c:38: u8 tilemap_platform_y_at(i16 x) {
                            196 ;	---------------------------------
                            197 ; Function tilemap_platform_y_at
                            198 ; ---------------------------------
   4F4F                     199 _tilemap_platform_y_at::
                            200 ;src/systems/tilemap.c:39: if (x >= 24 && x <= 56) {
   4F4F FD 21 02 00   [14]  201 	ld	iy, #2
   4F53 FD 39         [15]  202 	add	iy, sp
   4F55 FD 7E 00      [19]  203 	ld	a, 0 (iy)
   4F58 D6 18         [ 7]  204 	sub	a, #0x18
   4F5A FD 7E 01      [19]  205 	ld	a, 1 (iy)
   4F5D 17            [ 4]  206 	rla
   4F5E 3F            [ 4]  207 	ccf
   4F5F 1F            [ 4]  208 	rra
   4F60 DE 80         [ 7]  209 	sbc	a, #0x80
   4F62 38 1A         [12]  210 	jr	C,00102$
   4F64 3E 38         [ 7]  211 	ld	a, #0x38
   4F66 FD BE 00      [19]  212 	cp	a, 0 (iy)
   4F69 3E 00         [ 7]  213 	ld	a, #0x00
   4F6B FD 9E 01      [19]  214 	sbc	a, 1 (iy)
   4F6E E2 73 4F      [10]  215 	jp	PO, 00114$
   4F71 EE 80         [ 7]  216 	xor	a, #0x80
   4F73                     217 00114$:
   4F73 FA 7E 4F      [10]  218 	jp	M, 00102$
                            219 ;src/systems/tilemap.c:40: return gtileplatformy;
   4F76 FD 21 97 5D   [14]  220 	ld	iy, #_gtileplatformy
   4F7A FD 6E 00      [19]  221 	ld	l, 0 (iy)
   4F7D C9            [10]  222 	ret
   4F7E                     223 00102$:
                            224 ;src/systems/tilemap.c:42: return 255;
   4F7E 2E FF         [ 7]  225 	ld	l, #0xff
   4F80 C9            [10]  226 	ret
                            227 ;src/systems/tilemap.c:45: u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
                            228 ;	---------------------------------
                            229 ; Function tilemap_is_trap
                            230 ; ---------------------------------
   4F81                     231 _tilemap_is_trap::
   4F81 DD E5         [15]  232 	push	ix
   4F83 DD 21 00 00   [14]  233 	ld	ix,#0
   4F87 DD 39         [15]  234 	add	ix,sp
   4F89 F5            [11]  235 	push	af
                            236 ;src/systems/tilemap.c:50: left = x;
   4F8A DD 4E 04      [19]  237 	ld	c,4 (ix)
   4F8D DD 46 05      [19]  238 	ld	b,5 (ix)
                            239 ;src/systems/tilemap.c:51: right = x + (i16)w;
   4F90 DD 6E 08      [19]  240 	ld	l, 8 (ix)
   4F93 26 00         [ 7]  241 	ld	h, #0x00
   4F95 09            [11]  242 	add	hl, bc
   4F96 33            [ 6]  243 	inc	sp
   4F97 33            [ 6]  244 	inc	sp
   4F98 E5            [11]  245 	push	hl
                            246 ;src/systems/tilemap.c:52: feet = y + (i16)h;
   4F99 DD 5E 09      [19]  247 	ld	e, 9 (ix)
   4F9C 16 00         [ 7]  248 	ld	d, #0x00
   4F9E DD 6E 06      [19]  249 	ld	l,6 (ix)
   4FA1 DD 66 07      [19]  250 	ld	h,7 (ix)
   4FA4 19            [11]  251 	add	hl, de
   4FA5 EB            [ 4]  252 	ex	de,hl
                            253 ;src/systems/tilemap.c:54: if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
   4FA6 FD 21 96 5D   [14]  254 	ld	iy, #_gtilegroundy
   4FAA FD 6E 00      [19]  255 	ld	l, 0 (iy)
   4FAD 26 00         [ 7]  256 	ld	h, #0x00
   4FAF 2B            [ 6]  257 	dec	hl
   4FB0 2B            [ 6]  258 	dec	hl
   4FB1 7B            [ 4]  259 	ld	a, e
   4FB2 95            [ 4]  260 	sub	a, l
   4FB3 7A            [ 4]  261 	ld	a, d
   4FB4 9C            [ 4]  262 	sbc	a, h
   4FB5 E2 BA 4F      [10]  263 	jp	PO, 00119$
   4FB8 EE 80         [ 7]  264 	xor	a, #0x80
   4FBA                     265 00119$:
   4FBA FA DE 4F      [10]  266 	jp	M, 00102$
   4FBD 79            [ 4]  267 	ld	a, c
   4FBE D6 48         [ 7]  268 	sub	a, #0x48
   4FC0 78            [ 4]  269 	ld	a, b
   4FC1 17            [ 4]  270 	rla
   4FC2 3F            [ 4]  271 	ccf
   4FC3 1F            [ 4]  272 	rra
   4FC4 DE 80         [ 7]  273 	sbc	a, #0x80
   4FC6 30 16         [12]  274 	jr	NC,00102$
   4FC8 3E 38         [ 7]  275 	ld	a, #0x38
   4FCA DD BE FE      [19]  276 	cp	a, -2 (ix)
   4FCD 3E 00         [ 7]  277 	ld	a, #0x00
   4FCF DD 9E FF      [19]  278 	sbc	a, -1 (ix)
   4FD2 E2 D7 4F      [10]  279 	jp	PO, 00120$
   4FD5 EE 80         [ 7]  280 	xor	a, #0x80
   4FD7                     281 00120$:
   4FD7 F2 DE 4F      [10]  282 	jp	P, 00102$
                            283 ;src/systems/tilemap.c:55: return 1;
   4FDA 2E 01         [ 7]  284 	ld	l, #0x01
   4FDC 18 02         [12]  285 	jr	00105$
   4FDE                     286 00102$:
                            287 ;src/systems/tilemap.c:57: return 0;
   4FDE 2E 00         [ 7]  288 	ld	l, #0x00
   4FE0                     289 00105$:
   4FE0 DD F9         [10]  290 	ld	sp, ix
   4FE2 DD E1         [14]  291 	pop	ix
   4FE4 C9            [10]  292 	ret
                            293 ;src/systems/tilemap.c:60: u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
                            294 ;	---------------------------------
                            295 ; Function tilemap_is_ladder
                            296 ; ---------------------------------
   4FE5                     297 _tilemap_is_ladder::
                            298 ;src/systems/tilemap.c:65: return 0;
   4FE5 2E 00         [ 7]  299 	ld	l, #0x00
   4FE7 C9            [10]  300 	ret
                            301 ;src/systems/tilemap.c:68: u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
                            302 ;	---------------------------------
                            303 ; Function tilemap_is_hidden_zone
                            304 ; ---------------------------------
   4FE8                     305 _tilemap_is_hidden_zone::
                            306 ;src/systems/tilemap.c:73: return 0;
   4FE8 2E 00         [ 7]  307 	ld	l, #0x00
   4FEA C9            [10]  308 	ret
                            309 ;src/systems/tilemap.c:76: u8 tilemap_goal_x(void) {
                            310 ;	---------------------------------
                            311 ; Function tilemap_goal_x
                            312 ; ---------------------------------
   4FEB                     313 _tilemap_goal_x::
                            314 ;src/systems/tilemap.c:77: return ggoalx;
   4FEB FD 21 98 5D   [14]  315 	ld	iy, #_ggoalx
   4FEF FD 6E 00      [19]  316 	ld	l, 0 (iy)
   4FF2 C9            [10]  317 	ret
                            318 	.area _CODE
                            319 	.area _INITIALIZER
   5DB1                     320 __xinit__gtilegroundy:
   5DB1 A0                  321 	.db #0xa0	; 160
   5DB2                     322 __xinit__gtileplatformy:
   5DB2 80                  323 	.db #0x80	; 128
   5DB3                     324 __xinit__ggoalx:
   5DB3 48                  325 	.db #0x48	; 72	'H'
                            326 	.area _CABS (ABS)
