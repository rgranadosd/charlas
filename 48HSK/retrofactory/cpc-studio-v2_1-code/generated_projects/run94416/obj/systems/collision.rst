                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module collision
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _tilemap_is_ladder
                             12 	.globl _tilemap_is_trap
                             13 	.globl _tilemap_platform_y_at
                             14 	.globl _tilemap_ground_y
                             15 	.globl _collision_init
                             16 	.globl _collision_is_on_ground
                             17 	.globl _collision_is_on_ground_at
                             18 	.globl _collision_clamp_y_to_ground
                             19 	.globl _collision_clamp_y_at
                             20 	.globl _collision_is_on_trap
                             21 	.globl _collision_is_on_ladder
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
   6517                      33 _ggroundy:
   6517                      34 	.ds 2
   6519                      35 _gplatformy:
   6519                      36 	.ds 2
                             37 ;--------------------------------------------------------
                             38 ; absolute external ram data
                             39 ;--------------------------------------------------------
                             40 	.area _DABS (ABS)
                             41 ;--------------------------------------------------------
                             42 ; global & static initialisations
                             43 ;--------------------------------------------------------
                             44 	.area _HOME
                             45 	.area _GSINIT
                             46 	.area _GSFINAL
                             47 	.area _GSINIT
                             48 ;--------------------------------------------------------
                             49 ; Home
                             50 ;--------------------------------------------------------
                             51 	.area _HOME
                             52 	.area _HOME
                             53 ;--------------------------------------------------------
                             54 ; code
                             55 ;--------------------------------------------------------
                             56 	.area _CODE
                             57 ;src/systems/collision.c:7: void collision_init(void) {
                             58 ;	---------------------------------
                             59 ; Function collision_init
                             60 ; ---------------------------------
   4CCC                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4CCC CD BC 53      [17]   63 	call	_tilemap_ground_y
   4CCF FD 21 17 65   [14]   64 	ld	iy, #_ggroundy
   4CD3 FD 75 00      [19]   65 	ld	0 (iy), l
   4CD6 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4CDA 21 20 00      [10]   68 	ld	hl, #0x0020
   4CDD E5            [11]   69 	push	hl
   4CDE CD C4 53      [17]   70 	call	_tilemap_platform_y_at
   4CE1 F1            [10]   71 	pop	af
   4CE2 FD 21 19 65   [14]   72 	ld	iy, #_gplatformy
   4CE6 FD 75 00      [19]   73 	ld	0 (iy), l
   4CE9 FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4CED C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4CEE                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4CEE 21 04 00      [10]   82 	ld	hl, #4+0
   4CF1 39            [11]   83 	add	hl, sp
   4CF2 7E            [ 7]   84 	ld	a, (hl)
   4CF3 F5            [11]   85 	push	af
   4CF4 33            [ 6]   86 	inc	sp
   4CF5 21 03 00      [10]   87 	ld	hl, #3
   4CF8 39            [11]   88 	add	hl, sp
   4CF9 4E            [ 7]   89 	ld	c, (hl)
   4CFA 23            [ 6]   90 	inc	hl
   4CFB 46            [ 7]   91 	ld	b, (hl)
   4CFC C5            [11]   92 	push	bc
   4CFD 21 00 00      [10]   93 	ld	hl, #0x0000
   4D00 E5            [11]   94 	push	hl
   4D01 CD 08 4D      [17]   95 	call	_collision_is_on_ground_at
   4D04 F1            [10]   96 	pop	af
   4D05 F1            [10]   97 	pop	af
   4D06 33            [ 6]   98 	inc	sp
   4D07 C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4D08                     104 _collision_is_on_ground_at::
   4D08 DD E5         [15]  105 	push	ix
   4D0A DD 21 00 00   [14]  106 	ld	ix,#0
   4D0E DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4D10 CD BC 53      [17]  109 	call	_tilemap_ground_y
   4D13 4D            [ 4]  110 	ld	c, l
   4D14 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4D16 C5            [11]  113 	push	bc
   4D17 DD 6E 04      [19]  114 	ld	l,4 (ix)
   4D1A DD 66 05      [19]  115 	ld	h,5 (ix)
   4D1D E5            [11]  116 	push	hl
   4D1E CD C4 53      [17]  117 	call	_tilemap_platform_y_at
   4D21 F1            [10]  118 	pop	af
   4D22 C1            [10]  119 	pop	bc
   4D23 FD 21 19 65   [14]  120 	ld	iy, #_gplatformy
   4D27 FD 75 00      [19]  121 	ld	0 (iy), l
   4D2A FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4D2E DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4D31 16 00         [ 7]  125 	ld	d, #0x00
   4D33 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4D36 83            [ 4]  127 	add	a, e
   4D37 5F            [ 4]  128 	ld	e, a
   4D38 DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4D3B 8A            [ 4]  130 	adc	a, d
   4D3C 57            [ 4]  131 	ld	d, a
   4D3D FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4D40 3C            [ 4]  133 	inc	a
   4D41 FD B6 01      [19]  134 	or	a, 1 (iy)
   4D44 28 15         [12]  135 	jr	Z,00102$
   4D46 2A 19 65      [16]  136 	ld	hl, (_gplatformy)
   4D49 23            [ 6]  137 	inc	hl
   4D4A 23            [ 6]  138 	inc	hl
   4D4B 7D            [ 4]  139 	ld	a, l
   4D4C 93            [ 4]  140 	sub	a, e
   4D4D 7C            [ 4]  141 	ld	a, h
   4D4E 9A            [ 4]  142 	sbc	a, d
   4D4F E2 54 4D      [10]  143 	jp	PO, 00115$
   4D52 EE 80         [ 7]  144 	xor	a, #0x80
   4D54                     145 00115$:
   4D54 FA 5B 4D      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4D57 ED 4B 19 65   [20]  148 	ld	bc, (_gplatformy)
   4D5B                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4D5B 7B            [ 4]  152 	ld	a, e
   4D5C 91            [ 4]  153 	sub	a, c
   4D5D 7A            [ 4]  154 	ld	a, d
   4D5E 98            [ 4]  155 	sbc	a, b
   4D5F E2 64 4D      [10]  156 	jp	PO, 00116$
   4D62 EE 80         [ 7]  157 	xor	a, #0x80
   4D64                     158 00116$:
   4D64 07            [ 4]  159 	rlca
   4D65 E6 01         [ 7]  160 	and	a,#0x01
   4D67 EE 01         [ 7]  161 	xor	a, #0x01
   4D69 6F            [ 4]  162 	ld	l, a
   4D6A DD E1         [14]  163 	pop	ix
   4D6C C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4D6D                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4D6D 21 04 00      [10]  171 	ld	hl, #4+0
   4D70 39            [11]  172 	add	hl, sp
   4D71 7E            [ 7]  173 	ld	a, (hl)
   4D72 F5            [11]  174 	push	af
   4D73 33            [ 6]  175 	inc	sp
   4D74 21 03 00      [10]  176 	ld	hl, #3
   4D77 39            [11]  177 	add	hl, sp
   4D78 4E            [ 7]  178 	ld	c, (hl)
   4D79 23            [ 6]  179 	inc	hl
   4D7A 46            [ 7]  180 	ld	b, (hl)
   4D7B C5            [11]  181 	push	bc
   4D7C 21 00 00      [10]  182 	ld	hl, #0x0000
   4D7F E5            [11]  183 	push	hl
   4D80 CD 87 4D      [17]  184 	call	_collision_clamp_y_at
   4D83 F1            [10]  185 	pop	af
   4D84 F1            [10]  186 	pop	af
   4D85 33            [ 6]  187 	inc	sp
   4D86 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4D87                     193 _collision_clamp_y_at::
   4D87 DD E5         [15]  194 	push	ix
   4D89 DD 21 00 00   [14]  195 	ld	ix,#0
   4D8D DD 39         [15]  196 	add	ix,sp
   4D8F 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4D90 CD BC 53      [17]  199 	call	_tilemap_ground_y
   4D93 FD 21 17 65   [14]  200 	ld	iy, #_ggroundy
   4D97 FD 75 00      [19]  201 	ld	0 (iy), l
   4D9A FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4D9E DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4DA1 06 00         [ 7]  205 	ld	b, #0x00
   4DA3 FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4DA6 91            [ 4]  207 	sub	a, c
   4DA7 5F            [ 4]  208 	ld	e, a
   4DA8 FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4DAB 98            [ 4]  210 	sbc	a, b
   4DAC 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4DAD C5            [11]  213 	push	bc
   4DAE D5            [11]  214 	push	de
   4DAF DD 6E 04      [19]  215 	ld	l,4 (ix)
   4DB2 DD 66 05      [19]  216 	ld	h,5 (ix)
   4DB5 E5            [11]  217 	push	hl
   4DB6 CD C4 53      [17]  218 	call	_tilemap_platform_y_at
   4DB9 F1            [10]  219 	pop	af
   4DBA D1            [10]  220 	pop	de
   4DBB C1            [10]  221 	pop	bc
   4DBC FD 21 19 65   [14]  222 	ld	iy, #_gplatformy
   4DC0 FD 75 00      [19]  223 	ld	0 (iy), l
   4DC3 FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4DC7 7B            [ 4]  226 	ld	a, e
   4DC8 DD 96 06      [19]  227 	sub	a, 6 (ix)
   4DCB 7A            [ 4]  228 	ld	a, d
   4DCC DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4DCF E2 D4 4D      [10]  230 	jp	PO, 00126$
   4DD2 EE 80         [ 7]  231 	xor	a, #0x80
   4DD4                     232 00126$:
   4DD4 07            [ 4]  233 	rlca
   4DD5 E6 01         [ 7]  234 	and	a,#0x01
   4DD7 DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4DDA FD 21 19 65   [14]  237 	ld	iy, #_gplatformy
   4DDE FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4DE1 3C            [ 4]  239 	inc	a
   4DE2 FD B6 01      [19]  240 	or	a, 1 (iy)
   4DE5 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4DE7 FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4DEA 91            [ 4]  244 	sub	a, c
   4DEB 4F            [ 4]  245 	ld	c, a
   4DEC FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4DEF 98            [ 4]  247 	sbc	a, b
   4DF0 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4DF1 79            [ 4]  250 	ld	a, c
   4DF2 DD 96 06      [19]  251 	sub	a, 6 (ix)
   4DF5 78            [ 4]  252 	ld	a, b
   4DF6 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4DF9 E2 FE 4D      [10]  254 	jp	PO, 00128$
   4DFC EE 80         [ 7]  255 	xor	a, #0x80
   4DFE                     256 00128$:
   4DFE F2 0B 4E      [10]  257 	jp	P, 00105$
   4E01 DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4E05 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4E07 69            [ 4]  261 	ld	l, c
   4E08 60            [ 4]  262 	ld	h, b
   4E09 18 0F         [12]  263 	jr	00108$
   4E0B                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4E0B DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4E0F 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4E11 EB            [ 4]  269 	ex	de,hl
   4E12 18 06         [12]  270 	jr	00108$
   4E14                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4E14 DD 6E 06      [19]  273 	ld	l,6 (ix)
   4E17 DD 66 07      [19]  274 	ld	h,7 (ix)
   4E1A                     275 00108$:
   4E1A 33            [ 6]  276 	inc	sp
   4E1B DD E1         [14]  277 	pop	ix
   4E1D C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4E1E                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4E1E 21 07 00      [10]  285 	ld	hl, #7+0
   4E21 39            [11]  286 	add	hl, sp
   4E22 7E            [ 7]  287 	ld	a, (hl)
   4E23 F5            [11]  288 	push	af
   4E24 33            [ 6]  289 	inc	sp
   4E25 21 07 00      [10]  290 	ld	hl, #7+0
   4E28 39            [11]  291 	add	hl, sp
   4E29 7E            [ 7]  292 	ld	a, (hl)
   4E2A F5            [11]  293 	push	af
   4E2B 33            [ 6]  294 	inc	sp
   4E2C 21 06 00      [10]  295 	ld	hl, #6
   4E2F 39            [11]  296 	add	hl, sp
   4E30 4E            [ 7]  297 	ld	c, (hl)
   4E31 23            [ 6]  298 	inc	hl
   4E32 46            [ 7]  299 	ld	b, (hl)
   4E33 C5            [11]  300 	push	bc
   4E34 21 06 00      [10]  301 	ld	hl, #6
   4E37 39            [11]  302 	add	hl, sp
   4E38 4E            [ 7]  303 	ld	c, (hl)
   4E39 23            [ 6]  304 	inc	hl
   4E3A 46            [ 7]  305 	ld	b, (hl)
   4E3B C5            [11]  306 	push	bc
   4E3C CD F6 53      [17]  307 	call	_tilemap_is_trap
   4E3F F1            [10]  308 	pop	af
   4E40 F1            [10]  309 	pop	af
   4E41 F1            [10]  310 	pop	af
   4E42 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4E43                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4E43 21 07 00      [10]  318 	ld	hl, #7+0
   4E46 39            [11]  319 	add	hl, sp
   4E47 7E            [ 7]  320 	ld	a, (hl)
   4E48 F5            [11]  321 	push	af
   4E49 33            [ 6]  322 	inc	sp
   4E4A 21 07 00      [10]  323 	ld	hl, #7+0
   4E4D 39            [11]  324 	add	hl, sp
   4E4E 7E            [ 7]  325 	ld	a, (hl)
   4E4F F5            [11]  326 	push	af
   4E50 33            [ 6]  327 	inc	sp
   4E51 21 06 00      [10]  328 	ld	hl, #6
   4E54 39            [11]  329 	add	hl, sp
   4E55 4E            [ 7]  330 	ld	c, (hl)
   4E56 23            [ 6]  331 	inc	hl
   4E57 46            [ 7]  332 	ld	b, (hl)
   4E58 C5            [11]  333 	push	bc
   4E59 21 06 00      [10]  334 	ld	hl, #6
   4E5C 39            [11]  335 	add	hl, sp
   4E5D 4E            [ 7]  336 	ld	c, (hl)
   4E5E 23            [ 6]  337 	inc	hl
   4E5F 46            [ 7]  338 	ld	b, (hl)
   4E60 C5            [11]  339 	push	bc
   4E61 CD 5A 54      [17]  340 	call	_tilemap_is_ladder
   4E64 F1            [10]  341 	pop	af
   4E65 F1            [10]  342 	pop	af
   4E66 F1            [10]  343 	pop	af
   4E67 C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   651E                     347 __xinit__ggroundy:
   651E A0 00               348 	.dw #0x00a0
   6520                     349 __xinit__gplatformy:
   6520 FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
