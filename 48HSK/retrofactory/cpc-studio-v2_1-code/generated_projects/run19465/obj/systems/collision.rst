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
   5F65                      33 _ggroundy:
   5F65                      34 	.ds 2
   5F67                      35 _gplatformy:
   5F67                      36 	.ds 2
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
   4B1B                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4B1B CD 84 50      [17]   63 	call	_tilemap_ground_y
   4B1E FD 21 65 5F   [14]   64 	ld	iy, #_ggroundy
   4B22 FD 75 00      [19]   65 	ld	0 (iy), l
   4B25 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4B29 21 20 00      [10]   68 	ld	hl, #0x0020
   4B2C E5            [11]   69 	push	hl
   4B2D CD 8C 50      [17]   70 	call	_tilemap_platform_y_at
   4B30 F1            [10]   71 	pop	af
   4B31 FD 21 67 5F   [14]   72 	ld	iy, #_gplatformy
   4B35 FD 75 00      [19]   73 	ld	0 (iy), l
   4B38 FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4B3C C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4B3D                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4B3D 21 04 00      [10]   82 	ld	hl, #4+0
   4B40 39            [11]   83 	add	hl, sp
   4B41 7E            [ 7]   84 	ld	a, (hl)
   4B42 F5            [11]   85 	push	af
   4B43 33            [ 6]   86 	inc	sp
   4B44 21 03 00      [10]   87 	ld	hl, #3
   4B47 39            [11]   88 	add	hl, sp
   4B48 4E            [ 7]   89 	ld	c, (hl)
   4B49 23            [ 6]   90 	inc	hl
   4B4A 46            [ 7]   91 	ld	b, (hl)
   4B4B C5            [11]   92 	push	bc
   4B4C 21 00 00      [10]   93 	ld	hl, #0x0000
   4B4F E5            [11]   94 	push	hl
   4B50 CD 57 4B      [17]   95 	call	_collision_is_on_ground_at
   4B53 F1            [10]   96 	pop	af
   4B54 F1            [10]   97 	pop	af
   4B55 33            [ 6]   98 	inc	sp
   4B56 C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4B57                     104 _collision_is_on_ground_at::
   4B57 DD E5         [15]  105 	push	ix
   4B59 DD 21 00 00   [14]  106 	ld	ix,#0
   4B5D DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4B5F CD 84 50      [17]  109 	call	_tilemap_ground_y
   4B62 4D            [ 4]  110 	ld	c, l
   4B63 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4B65 C5            [11]  113 	push	bc
   4B66 DD 6E 04      [19]  114 	ld	l,4 (ix)
   4B69 DD 66 05      [19]  115 	ld	h,5 (ix)
   4B6C E5            [11]  116 	push	hl
   4B6D CD 8C 50      [17]  117 	call	_tilemap_platform_y_at
   4B70 F1            [10]  118 	pop	af
   4B71 C1            [10]  119 	pop	bc
   4B72 FD 21 67 5F   [14]  120 	ld	iy, #_gplatformy
   4B76 FD 75 00      [19]  121 	ld	0 (iy), l
   4B79 FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4B7D DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4B80 16 00         [ 7]  125 	ld	d, #0x00
   4B82 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4B85 83            [ 4]  127 	add	a, e
   4B86 5F            [ 4]  128 	ld	e, a
   4B87 DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4B8A 8A            [ 4]  130 	adc	a, d
   4B8B 57            [ 4]  131 	ld	d, a
   4B8C FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4B8F 3C            [ 4]  133 	inc	a
   4B90 FD B6 01      [19]  134 	or	a, 1 (iy)
   4B93 28 15         [12]  135 	jr	Z,00102$
   4B95 2A 67 5F      [16]  136 	ld	hl, (_gplatformy)
   4B98 23            [ 6]  137 	inc	hl
   4B99 23            [ 6]  138 	inc	hl
   4B9A 7D            [ 4]  139 	ld	a, l
   4B9B 93            [ 4]  140 	sub	a, e
   4B9C 7C            [ 4]  141 	ld	a, h
   4B9D 9A            [ 4]  142 	sbc	a, d
   4B9E E2 A3 4B      [10]  143 	jp	PO, 00115$
   4BA1 EE 80         [ 7]  144 	xor	a, #0x80
   4BA3                     145 00115$:
   4BA3 FA AA 4B      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4BA6 ED 4B 67 5F   [20]  148 	ld	bc, (_gplatformy)
   4BAA                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4BAA 7B            [ 4]  152 	ld	a, e
   4BAB 91            [ 4]  153 	sub	a, c
   4BAC 7A            [ 4]  154 	ld	a, d
   4BAD 98            [ 4]  155 	sbc	a, b
   4BAE E2 B3 4B      [10]  156 	jp	PO, 00116$
   4BB1 EE 80         [ 7]  157 	xor	a, #0x80
   4BB3                     158 00116$:
   4BB3 07            [ 4]  159 	rlca
   4BB4 E6 01         [ 7]  160 	and	a,#0x01
   4BB6 EE 01         [ 7]  161 	xor	a, #0x01
   4BB8 6F            [ 4]  162 	ld	l, a
   4BB9 DD E1         [14]  163 	pop	ix
   4BBB C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4BBC                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4BBC 21 04 00      [10]  171 	ld	hl, #4+0
   4BBF 39            [11]  172 	add	hl, sp
   4BC0 7E            [ 7]  173 	ld	a, (hl)
   4BC1 F5            [11]  174 	push	af
   4BC2 33            [ 6]  175 	inc	sp
   4BC3 21 03 00      [10]  176 	ld	hl, #3
   4BC6 39            [11]  177 	add	hl, sp
   4BC7 4E            [ 7]  178 	ld	c, (hl)
   4BC8 23            [ 6]  179 	inc	hl
   4BC9 46            [ 7]  180 	ld	b, (hl)
   4BCA C5            [11]  181 	push	bc
   4BCB 21 00 00      [10]  182 	ld	hl, #0x0000
   4BCE E5            [11]  183 	push	hl
   4BCF CD D6 4B      [17]  184 	call	_collision_clamp_y_at
   4BD2 F1            [10]  185 	pop	af
   4BD3 F1            [10]  186 	pop	af
   4BD4 33            [ 6]  187 	inc	sp
   4BD5 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4BD6                     193 _collision_clamp_y_at::
   4BD6 DD E5         [15]  194 	push	ix
   4BD8 DD 21 00 00   [14]  195 	ld	ix,#0
   4BDC DD 39         [15]  196 	add	ix,sp
   4BDE 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4BDF CD 84 50      [17]  199 	call	_tilemap_ground_y
   4BE2 FD 21 65 5F   [14]  200 	ld	iy, #_ggroundy
   4BE6 FD 75 00      [19]  201 	ld	0 (iy), l
   4BE9 FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4BED DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4BF0 06 00         [ 7]  205 	ld	b, #0x00
   4BF2 FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4BF5 91            [ 4]  207 	sub	a, c
   4BF6 5F            [ 4]  208 	ld	e, a
   4BF7 FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4BFA 98            [ 4]  210 	sbc	a, b
   4BFB 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4BFC C5            [11]  213 	push	bc
   4BFD D5            [11]  214 	push	de
   4BFE DD 6E 04      [19]  215 	ld	l,4 (ix)
   4C01 DD 66 05      [19]  216 	ld	h,5 (ix)
   4C04 E5            [11]  217 	push	hl
   4C05 CD 8C 50      [17]  218 	call	_tilemap_platform_y_at
   4C08 F1            [10]  219 	pop	af
   4C09 D1            [10]  220 	pop	de
   4C0A C1            [10]  221 	pop	bc
   4C0B FD 21 67 5F   [14]  222 	ld	iy, #_gplatformy
   4C0F FD 75 00      [19]  223 	ld	0 (iy), l
   4C12 FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4C16 7B            [ 4]  226 	ld	a, e
   4C17 DD 96 06      [19]  227 	sub	a, 6 (ix)
   4C1A 7A            [ 4]  228 	ld	a, d
   4C1B DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4C1E E2 23 4C      [10]  230 	jp	PO, 00126$
   4C21 EE 80         [ 7]  231 	xor	a, #0x80
   4C23                     232 00126$:
   4C23 07            [ 4]  233 	rlca
   4C24 E6 01         [ 7]  234 	and	a,#0x01
   4C26 DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4C29 FD 21 67 5F   [14]  237 	ld	iy, #_gplatformy
   4C2D FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4C30 3C            [ 4]  239 	inc	a
   4C31 FD B6 01      [19]  240 	or	a, 1 (iy)
   4C34 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4C36 FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4C39 91            [ 4]  244 	sub	a, c
   4C3A 4F            [ 4]  245 	ld	c, a
   4C3B FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4C3E 98            [ 4]  247 	sbc	a, b
   4C3F 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4C40 79            [ 4]  250 	ld	a, c
   4C41 DD 96 06      [19]  251 	sub	a, 6 (ix)
   4C44 78            [ 4]  252 	ld	a, b
   4C45 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4C48 E2 4D 4C      [10]  254 	jp	PO, 00128$
   4C4B EE 80         [ 7]  255 	xor	a, #0x80
   4C4D                     256 00128$:
   4C4D F2 5A 4C      [10]  257 	jp	P, 00105$
   4C50 DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4C54 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4C56 69            [ 4]  261 	ld	l, c
   4C57 60            [ 4]  262 	ld	h, b
   4C58 18 0F         [12]  263 	jr	00108$
   4C5A                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4C5A DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4C5E 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4C60 EB            [ 4]  269 	ex	de,hl
   4C61 18 06         [12]  270 	jr	00108$
   4C63                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4C63 DD 6E 06      [19]  273 	ld	l,6 (ix)
   4C66 DD 66 07      [19]  274 	ld	h,7 (ix)
   4C69                     275 00108$:
   4C69 33            [ 6]  276 	inc	sp
   4C6A DD E1         [14]  277 	pop	ix
   4C6C C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4C6D                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4C6D 21 07 00      [10]  285 	ld	hl, #7+0
   4C70 39            [11]  286 	add	hl, sp
   4C71 7E            [ 7]  287 	ld	a, (hl)
   4C72 F5            [11]  288 	push	af
   4C73 33            [ 6]  289 	inc	sp
   4C74 21 07 00      [10]  290 	ld	hl, #7+0
   4C77 39            [11]  291 	add	hl, sp
   4C78 7E            [ 7]  292 	ld	a, (hl)
   4C79 F5            [11]  293 	push	af
   4C7A 33            [ 6]  294 	inc	sp
   4C7B 21 06 00      [10]  295 	ld	hl, #6
   4C7E 39            [11]  296 	add	hl, sp
   4C7F 4E            [ 7]  297 	ld	c, (hl)
   4C80 23            [ 6]  298 	inc	hl
   4C81 46            [ 7]  299 	ld	b, (hl)
   4C82 C5            [11]  300 	push	bc
   4C83 21 06 00      [10]  301 	ld	hl, #6
   4C86 39            [11]  302 	add	hl, sp
   4C87 4E            [ 7]  303 	ld	c, (hl)
   4C88 23            [ 6]  304 	inc	hl
   4C89 46            [ 7]  305 	ld	b, (hl)
   4C8A C5            [11]  306 	push	bc
   4C8B CD BE 50      [17]  307 	call	_tilemap_is_trap
   4C8E F1            [10]  308 	pop	af
   4C8F F1            [10]  309 	pop	af
   4C90 F1            [10]  310 	pop	af
   4C91 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4C92                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4C92 21 07 00      [10]  318 	ld	hl, #7+0
   4C95 39            [11]  319 	add	hl, sp
   4C96 7E            [ 7]  320 	ld	a, (hl)
   4C97 F5            [11]  321 	push	af
   4C98 33            [ 6]  322 	inc	sp
   4C99 21 07 00      [10]  323 	ld	hl, #7+0
   4C9C 39            [11]  324 	add	hl, sp
   4C9D 7E            [ 7]  325 	ld	a, (hl)
   4C9E F5            [11]  326 	push	af
   4C9F 33            [ 6]  327 	inc	sp
   4CA0 21 06 00      [10]  328 	ld	hl, #6
   4CA3 39            [11]  329 	add	hl, sp
   4CA4 4E            [ 7]  330 	ld	c, (hl)
   4CA5 23            [ 6]  331 	inc	hl
   4CA6 46            [ 7]  332 	ld	b, (hl)
   4CA7 C5            [11]  333 	push	bc
   4CA8 21 06 00      [10]  334 	ld	hl, #6
   4CAB 39            [11]  335 	add	hl, sp
   4CAC 4E            [ 7]  336 	ld	c, (hl)
   4CAD 23            [ 6]  337 	inc	hl
   4CAE 46            [ 7]  338 	ld	b, (hl)
   4CAF C5            [11]  339 	push	bc
   4CB0 CD 22 51      [17]  340 	call	_tilemap_is_ladder
   4CB3 F1            [10]  341 	pop	af
   4CB4 F1            [10]  342 	pop	af
   4CB5 F1            [10]  343 	pop	af
   4CB6 C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5F80                     347 __xinit__ggroundy:
   5F80 A0 00               348 	.dw #0x00a0
   5F82                     349 __xinit__gplatformy:
   5F82 FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
