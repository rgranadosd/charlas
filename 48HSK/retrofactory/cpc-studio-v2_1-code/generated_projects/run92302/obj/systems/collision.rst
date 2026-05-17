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
   5F3F                      33 _ggroundy:
   5F3F                      34 	.ds 2
   5F41                      35 _gplatformy:
   5F41                      36 	.ds 2
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
   4B85                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4B85 CD 0E 51      [17]   63 	call	_tilemap_ground_y
   4B88 FD 21 3F 5F   [14]   64 	ld	iy, #_ggroundy
   4B8C FD 75 00      [19]   65 	ld	0 (iy), l
   4B8F FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4B93 21 20 00      [10]   68 	ld	hl, #0x0020
   4B96 E5            [11]   69 	push	hl
   4B97 CD 16 51      [17]   70 	call	_tilemap_platform_y_at
   4B9A F1            [10]   71 	pop	af
   4B9B FD 21 41 5F   [14]   72 	ld	iy, #_gplatformy
   4B9F FD 75 00      [19]   73 	ld	0 (iy), l
   4BA2 FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4BA6 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4BA7                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4BA7 21 04 00      [10]   82 	ld	hl, #4+0
   4BAA 39            [11]   83 	add	hl, sp
   4BAB 7E            [ 7]   84 	ld	a, (hl)
   4BAC F5            [11]   85 	push	af
   4BAD 33            [ 6]   86 	inc	sp
   4BAE 21 03 00      [10]   87 	ld	hl, #3
   4BB1 39            [11]   88 	add	hl, sp
   4BB2 4E            [ 7]   89 	ld	c, (hl)
   4BB3 23            [ 6]   90 	inc	hl
   4BB4 46            [ 7]   91 	ld	b, (hl)
   4BB5 C5            [11]   92 	push	bc
   4BB6 21 00 00      [10]   93 	ld	hl, #0x0000
   4BB9 E5            [11]   94 	push	hl
   4BBA CD C1 4B      [17]   95 	call	_collision_is_on_ground_at
   4BBD F1            [10]   96 	pop	af
   4BBE F1            [10]   97 	pop	af
   4BBF 33            [ 6]   98 	inc	sp
   4BC0 C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4BC1                     104 _collision_is_on_ground_at::
   4BC1 DD E5         [15]  105 	push	ix
   4BC3 DD 21 00 00   [14]  106 	ld	ix,#0
   4BC7 DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4BC9 CD 0E 51      [17]  109 	call	_tilemap_ground_y
   4BCC 4D            [ 4]  110 	ld	c, l
   4BCD 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4BCF C5            [11]  113 	push	bc
   4BD0 DD 6E 04      [19]  114 	ld	l,4 (ix)
   4BD3 DD 66 05      [19]  115 	ld	h,5 (ix)
   4BD6 E5            [11]  116 	push	hl
   4BD7 CD 16 51      [17]  117 	call	_tilemap_platform_y_at
   4BDA F1            [10]  118 	pop	af
   4BDB C1            [10]  119 	pop	bc
   4BDC FD 21 41 5F   [14]  120 	ld	iy, #_gplatformy
   4BE0 FD 75 00      [19]  121 	ld	0 (iy), l
   4BE3 FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4BE7 DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4BEA 16 00         [ 7]  125 	ld	d, #0x00
   4BEC DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4BEF 83            [ 4]  127 	add	a, e
   4BF0 5F            [ 4]  128 	ld	e, a
   4BF1 DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4BF4 8A            [ 4]  130 	adc	a, d
   4BF5 57            [ 4]  131 	ld	d, a
   4BF6 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4BF9 3C            [ 4]  133 	inc	a
   4BFA FD B6 01      [19]  134 	or	a, 1 (iy)
   4BFD 28 15         [12]  135 	jr	Z,00102$
   4BFF 2A 41 5F      [16]  136 	ld	hl, (_gplatformy)
   4C02 23            [ 6]  137 	inc	hl
   4C03 23            [ 6]  138 	inc	hl
   4C04 7D            [ 4]  139 	ld	a, l
   4C05 93            [ 4]  140 	sub	a, e
   4C06 7C            [ 4]  141 	ld	a, h
   4C07 9A            [ 4]  142 	sbc	a, d
   4C08 E2 0D 4C      [10]  143 	jp	PO, 00115$
   4C0B EE 80         [ 7]  144 	xor	a, #0x80
   4C0D                     145 00115$:
   4C0D FA 14 4C      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4C10 ED 4B 41 5F   [20]  148 	ld	bc, (_gplatformy)
   4C14                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4C14 7B            [ 4]  152 	ld	a, e
   4C15 91            [ 4]  153 	sub	a, c
   4C16 7A            [ 4]  154 	ld	a, d
   4C17 98            [ 4]  155 	sbc	a, b
   4C18 E2 1D 4C      [10]  156 	jp	PO, 00116$
   4C1B EE 80         [ 7]  157 	xor	a, #0x80
   4C1D                     158 00116$:
   4C1D 07            [ 4]  159 	rlca
   4C1E E6 01         [ 7]  160 	and	a,#0x01
   4C20 EE 01         [ 7]  161 	xor	a, #0x01
   4C22 6F            [ 4]  162 	ld	l, a
   4C23 DD E1         [14]  163 	pop	ix
   4C25 C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4C26                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4C26 21 04 00      [10]  171 	ld	hl, #4+0
   4C29 39            [11]  172 	add	hl, sp
   4C2A 7E            [ 7]  173 	ld	a, (hl)
   4C2B F5            [11]  174 	push	af
   4C2C 33            [ 6]  175 	inc	sp
   4C2D 21 03 00      [10]  176 	ld	hl, #3
   4C30 39            [11]  177 	add	hl, sp
   4C31 4E            [ 7]  178 	ld	c, (hl)
   4C32 23            [ 6]  179 	inc	hl
   4C33 46            [ 7]  180 	ld	b, (hl)
   4C34 C5            [11]  181 	push	bc
   4C35 21 00 00      [10]  182 	ld	hl, #0x0000
   4C38 E5            [11]  183 	push	hl
   4C39 CD 40 4C      [17]  184 	call	_collision_clamp_y_at
   4C3C F1            [10]  185 	pop	af
   4C3D F1            [10]  186 	pop	af
   4C3E 33            [ 6]  187 	inc	sp
   4C3F C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4C40                     193 _collision_clamp_y_at::
   4C40 DD E5         [15]  194 	push	ix
   4C42 DD 21 00 00   [14]  195 	ld	ix,#0
   4C46 DD 39         [15]  196 	add	ix,sp
   4C48 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4C49 CD 0E 51      [17]  199 	call	_tilemap_ground_y
   4C4C FD 21 3F 5F   [14]  200 	ld	iy, #_ggroundy
   4C50 FD 75 00      [19]  201 	ld	0 (iy), l
   4C53 FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4C57 DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4C5A 06 00         [ 7]  205 	ld	b, #0x00
   4C5C FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4C5F 91            [ 4]  207 	sub	a, c
   4C60 5F            [ 4]  208 	ld	e, a
   4C61 FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4C64 98            [ 4]  210 	sbc	a, b
   4C65 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4C66 C5            [11]  213 	push	bc
   4C67 D5            [11]  214 	push	de
   4C68 DD 6E 04      [19]  215 	ld	l,4 (ix)
   4C6B DD 66 05      [19]  216 	ld	h,5 (ix)
   4C6E E5            [11]  217 	push	hl
   4C6F CD 16 51      [17]  218 	call	_tilemap_platform_y_at
   4C72 F1            [10]  219 	pop	af
   4C73 D1            [10]  220 	pop	de
   4C74 C1            [10]  221 	pop	bc
   4C75 FD 21 41 5F   [14]  222 	ld	iy, #_gplatformy
   4C79 FD 75 00      [19]  223 	ld	0 (iy), l
   4C7C FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4C80 7B            [ 4]  226 	ld	a, e
   4C81 DD 96 06      [19]  227 	sub	a, 6 (ix)
   4C84 7A            [ 4]  228 	ld	a, d
   4C85 DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4C88 E2 8D 4C      [10]  230 	jp	PO, 00126$
   4C8B EE 80         [ 7]  231 	xor	a, #0x80
   4C8D                     232 00126$:
   4C8D 07            [ 4]  233 	rlca
   4C8E E6 01         [ 7]  234 	and	a,#0x01
   4C90 DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4C93 FD 21 41 5F   [14]  237 	ld	iy, #_gplatformy
   4C97 FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4C9A 3C            [ 4]  239 	inc	a
   4C9B FD B6 01      [19]  240 	or	a, 1 (iy)
   4C9E 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4CA0 FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4CA3 91            [ 4]  244 	sub	a, c
   4CA4 4F            [ 4]  245 	ld	c, a
   4CA5 FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4CA8 98            [ 4]  247 	sbc	a, b
   4CA9 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4CAA 79            [ 4]  250 	ld	a, c
   4CAB DD 96 06      [19]  251 	sub	a, 6 (ix)
   4CAE 78            [ 4]  252 	ld	a, b
   4CAF DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4CB2 E2 B7 4C      [10]  254 	jp	PO, 00128$
   4CB5 EE 80         [ 7]  255 	xor	a, #0x80
   4CB7                     256 00128$:
   4CB7 F2 C4 4C      [10]  257 	jp	P, 00105$
   4CBA DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4CBE 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4CC0 69            [ 4]  261 	ld	l, c
   4CC1 60            [ 4]  262 	ld	h, b
   4CC2 18 0F         [12]  263 	jr	00108$
   4CC4                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4CC4 DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4CC8 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4CCA EB            [ 4]  269 	ex	de,hl
   4CCB 18 06         [12]  270 	jr	00108$
   4CCD                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4CCD DD 6E 06      [19]  273 	ld	l,6 (ix)
   4CD0 DD 66 07      [19]  274 	ld	h,7 (ix)
   4CD3                     275 00108$:
   4CD3 33            [ 6]  276 	inc	sp
   4CD4 DD E1         [14]  277 	pop	ix
   4CD6 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4CD7                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4CD7 21 07 00      [10]  285 	ld	hl, #7+0
   4CDA 39            [11]  286 	add	hl, sp
   4CDB 7E            [ 7]  287 	ld	a, (hl)
   4CDC F5            [11]  288 	push	af
   4CDD 33            [ 6]  289 	inc	sp
   4CDE 21 07 00      [10]  290 	ld	hl, #7+0
   4CE1 39            [11]  291 	add	hl, sp
   4CE2 7E            [ 7]  292 	ld	a, (hl)
   4CE3 F5            [11]  293 	push	af
   4CE4 33            [ 6]  294 	inc	sp
   4CE5 21 06 00      [10]  295 	ld	hl, #6
   4CE8 39            [11]  296 	add	hl, sp
   4CE9 4E            [ 7]  297 	ld	c, (hl)
   4CEA 23            [ 6]  298 	inc	hl
   4CEB 46            [ 7]  299 	ld	b, (hl)
   4CEC C5            [11]  300 	push	bc
   4CED 21 06 00      [10]  301 	ld	hl, #6
   4CF0 39            [11]  302 	add	hl, sp
   4CF1 4E            [ 7]  303 	ld	c, (hl)
   4CF2 23            [ 6]  304 	inc	hl
   4CF3 46            [ 7]  305 	ld	b, (hl)
   4CF4 C5            [11]  306 	push	bc
   4CF5 CD 48 51      [17]  307 	call	_tilemap_is_trap
   4CF8 F1            [10]  308 	pop	af
   4CF9 F1            [10]  309 	pop	af
   4CFA F1            [10]  310 	pop	af
   4CFB C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4CFC                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4CFC 21 07 00      [10]  318 	ld	hl, #7+0
   4CFF 39            [11]  319 	add	hl, sp
   4D00 7E            [ 7]  320 	ld	a, (hl)
   4D01 F5            [11]  321 	push	af
   4D02 33            [ 6]  322 	inc	sp
   4D03 21 07 00      [10]  323 	ld	hl, #7+0
   4D06 39            [11]  324 	add	hl, sp
   4D07 7E            [ 7]  325 	ld	a, (hl)
   4D08 F5            [11]  326 	push	af
   4D09 33            [ 6]  327 	inc	sp
   4D0A 21 06 00      [10]  328 	ld	hl, #6
   4D0D 39            [11]  329 	add	hl, sp
   4D0E 4E            [ 7]  330 	ld	c, (hl)
   4D0F 23            [ 6]  331 	inc	hl
   4D10 46            [ 7]  332 	ld	b, (hl)
   4D11 C5            [11]  333 	push	bc
   4D12 21 06 00      [10]  334 	ld	hl, #6
   4D15 39            [11]  335 	add	hl, sp
   4D16 4E            [ 7]  336 	ld	c, (hl)
   4D17 23            [ 6]  337 	inc	hl
   4D18 46            [ 7]  338 	ld	b, (hl)
   4D19 C5            [11]  339 	push	bc
   4D1A CD AC 51      [17]  340 	call	_tilemap_is_ladder
   4D1D F1            [10]  341 	pop	af
   4D1E F1            [10]  342 	pop	af
   4D1F F1            [10]  343 	pop	af
   4D20 C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5F46                     347 __xinit__ggroundy:
   5F46 A0 00               348 	.dw #0x00a0
   5F48                     349 __xinit__gplatformy:
   5F48 FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
