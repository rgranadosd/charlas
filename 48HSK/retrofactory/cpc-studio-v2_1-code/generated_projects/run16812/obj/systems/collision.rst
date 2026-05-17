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
   5F9D                      33 _ggroundy:
   5F9D                      34 	.ds 2
   5F9F                      35 _gplatformy:
   5F9F                      36 	.ds 2
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
   4B72                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4B72 CD 82 51      [17]   63 	call	_tilemap_ground_y
   4B75 FD 21 9D 5F   [14]   64 	ld	iy, #_ggroundy
   4B79 FD 75 00      [19]   65 	ld	0 (iy), l
   4B7C FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4B80 21 20 00      [10]   68 	ld	hl, #0x0020
   4B83 E5            [11]   69 	push	hl
   4B84 CD 8A 51      [17]   70 	call	_tilemap_platform_y_at
   4B87 F1            [10]   71 	pop	af
   4B88 FD 21 9F 5F   [14]   72 	ld	iy, #_gplatformy
   4B8C FD 75 00      [19]   73 	ld	0 (iy), l
   4B8F FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4B93 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4B94                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4B94 21 04 00      [10]   82 	ld	hl, #4+0
   4B97 39            [11]   83 	add	hl, sp
   4B98 7E            [ 7]   84 	ld	a, (hl)
   4B99 F5            [11]   85 	push	af
   4B9A 33            [ 6]   86 	inc	sp
   4B9B 21 03 00      [10]   87 	ld	hl, #3
   4B9E 39            [11]   88 	add	hl, sp
   4B9F 4E            [ 7]   89 	ld	c, (hl)
   4BA0 23            [ 6]   90 	inc	hl
   4BA1 46            [ 7]   91 	ld	b, (hl)
   4BA2 C5            [11]   92 	push	bc
   4BA3 21 00 00      [10]   93 	ld	hl, #0x0000
   4BA6 E5            [11]   94 	push	hl
   4BA7 CD AE 4B      [17]   95 	call	_collision_is_on_ground_at
   4BAA F1            [10]   96 	pop	af
   4BAB F1            [10]   97 	pop	af
   4BAC 33            [ 6]   98 	inc	sp
   4BAD C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4BAE                     104 _collision_is_on_ground_at::
   4BAE DD E5         [15]  105 	push	ix
   4BB0 DD 21 00 00   [14]  106 	ld	ix,#0
   4BB4 DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4BB6 CD 82 51      [17]  109 	call	_tilemap_ground_y
   4BB9 4D            [ 4]  110 	ld	c, l
   4BBA 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4BBC C5            [11]  113 	push	bc
   4BBD DD 6E 04      [19]  114 	ld	l,4 (ix)
   4BC0 DD 66 05      [19]  115 	ld	h,5 (ix)
   4BC3 E5            [11]  116 	push	hl
   4BC4 CD 8A 51      [17]  117 	call	_tilemap_platform_y_at
   4BC7 F1            [10]  118 	pop	af
   4BC8 C1            [10]  119 	pop	bc
   4BC9 FD 21 9F 5F   [14]  120 	ld	iy, #_gplatformy
   4BCD FD 75 00      [19]  121 	ld	0 (iy), l
   4BD0 FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4BD4 DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4BD7 16 00         [ 7]  125 	ld	d, #0x00
   4BD9 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4BDC 83            [ 4]  127 	add	a, e
   4BDD 5F            [ 4]  128 	ld	e, a
   4BDE DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4BE1 8A            [ 4]  130 	adc	a, d
   4BE2 57            [ 4]  131 	ld	d, a
   4BE3 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4BE6 3C            [ 4]  133 	inc	a
   4BE7 FD B6 01      [19]  134 	or	a, 1 (iy)
   4BEA 28 15         [12]  135 	jr	Z,00102$
   4BEC 2A 9F 5F      [16]  136 	ld	hl, (_gplatformy)
   4BEF 23            [ 6]  137 	inc	hl
   4BF0 23            [ 6]  138 	inc	hl
   4BF1 7D            [ 4]  139 	ld	a, l
   4BF2 93            [ 4]  140 	sub	a, e
   4BF3 7C            [ 4]  141 	ld	a, h
   4BF4 9A            [ 4]  142 	sbc	a, d
   4BF5 E2 FA 4B      [10]  143 	jp	PO, 00115$
   4BF8 EE 80         [ 7]  144 	xor	a, #0x80
   4BFA                     145 00115$:
   4BFA FA 01 4C      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4BFD ED 4B 9F 5F   [20]  148 	ld	bc, (_gplatformy)
   4C01                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4C01 7B            [ 4]  152 	ld	a, e
   4C02 91            [ 4]  153 	sub	a, c
   4C03 7A            [ 4]  154 	ld	a, d
   4C04 98            [ 4]  155 	sbc	a, b
   4C05 E2 0A 4C      [10]  156 	jp	PO, 00116$
   4C08 EE 80         [ 7]  157 	xor	a, #0x80
   4C0A                     158 00116$:
   4C0A 07            [ 4]  159 	rlca
   4C0B E6 01         [ 7]  160 	and	a,#0x01
   4C0D EE 01         [ 7]  161 	xor	a, #0x01
   4C0F 6F            [ 4]  162 	ld	l, a
   4C10 DD E1         [14]  163 	pop	ix
   4C12 C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4C13                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4C13 21 04 00      [10]  171 	ld	hl, #4+0
   4C16 39            [11]  172 	add	hl, sp
   4C17 7E            [ 7]  173 	ld	a, (hl)
   4C18 F5            [11]  174 	push	af
   4C19 33            [ 6]  175 	inc	sp
   4C1A 21 03 00      [10]  176 	ld	hl, #3
   4C1D 39            [11]  177 	add	hl, sp
   4C1E 4E            [ 7]  178 	ld	c, (hl)
   4C1F 23            [ 6]  179 	inc	hl
   4C20 46            [ 7]  180 	ld	b, (hl)
   4C21 C5            [11]  181 	push	bc
   4C22 21 00 00      [10]  182 	ld	hl, #0x0000
   4C25 E5            [11]  183 	push	hl
   4C26 CD 2D 4C      [17]  184 	call	_collision_clamp_y_at
   4C29 F1            [10]  185 	pop	af
   4C2A F1            [10]  186 	pop	af
   4C2B 33            [ 6]  187 	inc	sp
   4C2C C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4C2D                     193 _collision_clamp_y_at::
   4C2D DD E5         [15]  194 	push	ix
   4C2F DD 21 00 00   [14]  195 	ld	ix,#0
   4C33 DD 39         [15]  196 	add	ix,sp
   4C35 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4C36 CD 82 51      [17]  199 	call	_tilemap_ground_y
   4C39 FD 21 9D 5F   [14]  200 	ld	iy, #_ggroundy
   4C3D FD 75 00      [19]  201 	ld	0 (iy), l
   4C40 FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4C44 DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4C47 06 00         [ 7]  205 	ld	b, #0x00
   4C49 FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4C4C 91            [ 4]  207 	sub	a, c
   4C4D 5F            [ 4]  208 	ld	e, a
   4C4E FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4C51 98            [ 4]  210 	sbc	a, b
   4C52 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4C53 C5            [11]  213 	push	bc
   4C54 D5            [11]  214 	push	de
   4C55 DD 6E 04      [19]  215 	ld	l,4 (ix)
   4C58 DD 66 05      [19]  216 	ld	h,5 (ix)
   4C5B E5            [11]  217 	push	hl
   4C5C CD 8A 51      [17]  218 	call	_tilemap_platform_y_at
   4C5F F1            [10]  219 	pop	af
   4C60 D1            [10]  220 	pop	de
   4C61 C1            [10]  221 	pop	bc
   4C62 FD 21 9F 5F   [14]  222 	ld	iy, #_gplatformy
   4C66 FD 75 00      [19]  223 	ld	0 (iy), l
   4C69 FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4C6D 7B            [ 4]  226 	ld	a, e
   4C6E DD 96 06      [19]  227 	sub	a, 6 (ix)
   4C71 7A            [ 4]  228 	ld	a, d
   4C72 DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4C75 E2 7A 4C      [10]  230 	jp	PO, 00126$
   4C78 EE 80         [ 7]  231 	xor	a, #0x80
   4C7A                     232 00126$:
   4C7A 07            [ 4]  233 	rlca
   4C7B E6 01         [ 7]  234 	and	a,#0x01
   4C7D DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4C80 FD 21 9F 5F   [14]  237 	ld	iy, #_gplatformy
   4C84 FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4C87 3C            [ 4]  239 	inc	a
   4C88 FD B6 01      [19]  240 	or	a, 1 (iy)
   4C8B 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4C8D FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4C90 91            [ 4]  244 	sub	a, c
   4C91 4F            [ 4]  245 	ld	c, a
   4C92 FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4C95 98            [ 4]  247 	sbc	a, b
   4C96 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4C97 79            [ 4]  250 	ld	a, c
   4C98 DD 96 06      [19]  251 	sub	a, 6 (ix)
   4C9B 78            [ 4]  252 	ld	a, b
   4C9C DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4C9F E2 A4 4C      [10]  254 	jp	PO, 00128$
   4CA2 EE 80         [ 7]  255 	xor	a, #0x80
   4CA4                     256 00128$:
   4CA4 F2 B1 4C      [10]  257 	jp	P, 00105$
   4CA7 DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4CAB 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4CAD 69            [ 4]  261 	ld	l, c
   4CAE 60            [ 4]  262 	ld	h, b
   4CAF 18 0F         [12]  263 	jr	00108$
   4CB1                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4CB1 DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4CB5 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4CB7 EB            [ 4]  269 	ex	de,hl
   4CB8 18 06         [12]  270 	jr	00108$
   4CBA                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4CBA DD 6E 06      [19]  273 	ld	l,6 (ix)
   4CBD DD 66 07      [19]  274 	ld	h,7 (ix)
   4CC0                     275 00108$:
   4CC0 33            [ 6]  276 	inc	sp
   4CC1 DD E1         [14]  277 	pop	ix
   4CC3 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4CC4                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4CC4 21 07 00      [10]  285 	ld	hl, #7+0
   4CC7 39            [11]  286 	add	hl, sp
   4CC8 7E            [ 7]  287 	ld	a, (hl)
   4CC9 F5            [11]  288 	push	af
   4CCA 33            [ 6]  289 	inc	sp
   4CCB 21 07 00      [10]  290 	ld	hl, #7+0
   4CCE 39            [11]  291 	add	hl, sp
   4CCF 7E            [ 7]  292 	ld	a, (hl)
   4CD0 F5            [11]  293 	push	af
   4CD1 33            [ 6]  294 	inc	sp
   4CD2 21 06 00      [10]  295 	ld	hl, #6
   4CD5 39            [11]  296 	add	hl, sp
   4CD6 4E            [ 7]  297 	ld	c, (hl)
   4CD7 23            [ 6]  298 	inc	hl
   4CD8 46            [ 7]  299 	ld	b, (hl)
   4CD9 C5            [11]  300 	push	bc
   4CDA 21 06 00      [10]  301 	ld	hl, #6
   4CDD 39            [11]  302 	add	hl, sp
   4CDE 4E            [ 7]  303 	ld	c, (hl)
   4CDF 23            [ 6]  304 	inc	hl
   4CE0 46            [ 7]  305 	ld	b, (hl)
   4CE1 C5            [11]  306 	push	bc
   4CE2 CD BC 51      [17]  307 	call	_tilemap_is_trap
   4CE5 F1            [10]  308 	pop	af
   4CE6 F1            [10]  309 	pop	af
   4CE7 F1            [10]  310 	pop	af
   4CE8 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4CE9                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4CE9 21 07 00      [10]  318 	ld	hl, #7+0
   4CEC 39            [11]  319 	add	hl, sp
   4CED 7E            [ 7]  320 	ld	a, (hl)
   4CEE F5            [11]  321 	push	af
   4CEF 33            [ 6]  322 	inc	sp
   4CF0 21 07 00      [10]  323 	ld	hl, #7+0
   4CF3 39            [11]  324 	add	hl, sp
   4CF4 7E            [ 7]  325 	ld	a, (hl)
   4CF5 F5            [11]  326 	push	af
   4CF6 33            [ 6]  327 	inc	sp
   4CF7 21 06 00      [10]  328 	ld	hl, #6
   4CFA 39            [11]  329 	add	hl, sp
   4CFB 4E            [ 7]  330 	ld	c, (hl)
   4CFC 23            [ 6]  331 	inc	hl
   4CFD 46            [ 7]  332 	ld	b, (hl)
   4CFE C5            [11]  333 	push	bc
   4CFF 21 06 00      [10]  334 	ld	hl, #6
   4D02 39            [11]  335 	add	hl, sp
   4D03 4E            [ 7]  336 	ld	c, (hl)
   4D04 23            [ 6]  337 	inc	hl
   4D05 46            [ 7]  338 	ld	b, (hl)
   4D06 C5            [11]  339 	push	bc
   4D07 CD 20 52      [17]  340 	call	_tilemap_is_ladder
   4D0A F1            [10]  341 	pop	af
   4D0B F1            [10]  342 	pop	af
   4D0C F1            [10]  343 	pop	af
   4D0D C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5FA4                     347 __xinit__ggroundy:
   5FA4 A0 00               348 	.dw #0x00a0
   5FA6                     349 __xinit__gplatformy:
   5FA6 FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
