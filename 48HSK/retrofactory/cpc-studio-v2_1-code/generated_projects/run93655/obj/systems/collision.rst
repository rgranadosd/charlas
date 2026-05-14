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
   5E47                      33 _ggroundy:
   5E47                      34 	.ds 2
   5E49                      35 _gplatformy:
   5E49                      36 	.ds 2
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
   4A26                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4A26 CD 91 4F      [17]   63 	call	_tilemap_ground_y
   4A29 FD 21 47 5E   [14]   64 	ld	iy, #_ggroundy
   4A2D FD 75 00      [19]   65 	ld	0 (iy), l
   4A30 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4A34 21 20 00      [10]   68 	ld	hl, #0x0020
   4A37 E5            [11]   69 	push	hl
   4A38 CD 99 4F      [17]   70 	call	_tilemap_platform_y_at
   4A3B F1            [10]   71 	pop	af
   4A3C FD 21 49 5E   [14]   72 	ld	iy, #_gplatformy
   4A40 FD 75 00      [19]   73 	ld	0 (iy), l
   4A43 FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4A47 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4A48                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4A48 21 04 00      [10]   82 	ld	hl, #4+0
   4A4B 39            [11]   83 	add	hl, sp
   4A4C 7E            [ 7]   84 	ld	a, (hl)
   4A4D F5            [11]   85 	push	af
   4A4E 33            [ 6]   86 	inc	sp
   4A4F 21 03 00      [10]   87 	ld	hl, #3
   4A52 39            [11]   88 	add	hl, sp
   4A53 4E            [ 7]   89 	ld	c, (hl)
   4A54 23            [ 6]   90 	inc	hl
   4A55 46            [ 7]   91 	ld	b, (hl)
   4A56 C5            [11]   92 	push	bc
   4A57 21 00 00      [10]   93 	ld	hl, #0x0000
   4A5A E5            [11]   94 	push	hl
   4A5B CD 62 4A      [17]   95 	call	_collision_is_on_ground_at
   4A5E F1            [10]   96 	pop	af
   4A5F F1            [10]   97 	pop	af
   4A60 33            [ 6]   98 	inc	sp
   4A61 C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4A62                     104 _collision_is_on_ground_at::
   4A62 DD E5         [15]  105 	push	ix
   4A64 DD 21 00 00   [14]  106 	ld	ix,#0
   4A68 DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4A6A CD 91 4F      [17]  109 	call	_tilemap_ground_y
   4A6D 4D            [ 4]  110 	ld	c, l
   4A6E 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4A70 C5            [11]  113 	push	bc
   4A71 DD 6E 04      [19]  114 	ld	l,4 (ix)
   4A74 DD 66 05      [19]  115 	ld	h,5 (ix)
   4A77 E5            [11]  116 	push	hl
   4A78 CD 99 4F      [17]  117 	call	_tilemap_platform_y_at
   4A7B F1            [10]  118 	pop	af
   4A7C C1            [10]  119 	pop	bc
   4A7D FD 21 49 5E   [14]  120 	ld	iy, #_gplatformy
   4A81 FD 75 00      [19]  121 	ld	0 (iy), l
   4A84 FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4A88 DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4A8B 16 00         [ 7]  125 	ld	d, #0x00
   4A8D DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4A90 83            [ 4]  127 	add	a, e
   4A91 5F            [ 4]  128 	ld	e, a
   4A92 DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4A95 8A            [ 4]  130 	adc	a, d
   4A96 57            [ 4]  131 	ld	d, a
   4A97 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4A9A 3C            [ 4]  133 	inc	a
   4A9B FD B6 01      [19]  134 	or	a, 1 (iy)
   4A9E 28 15         [12]  135 	jr	Z,00102$
   4AA0 2A 49 5E      [16]  136 	ld	hl, (_gplatformy)
   4AA3 23            [ 6]  137 	inc	hl
   4AA4 23            [ 6]  138 	inc	hl
   4AA5 7D            [ 4]  139 	ld	a, l
   4AA6 93            [ 4]  140 	sub	a, e
   4AA7 7C            [ 4]  141 	ld	a, h
   4AA8 9A            [ 4]  142 	sbc	a, d
   4AA9 E2 AE 4A      [10]  143 	jp	PO, 00115$
   4AAC EE 80         [ 7]  144 	xor	a, #0x80
   4AAE                     145 00115$:
   4AAE FA B5 4A      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4AB1 ED 4B 49 5E   [20]  148 	ld	bc, (_gplatformy)
   4AB5                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4AB5 7B            [ 4]  152 	ld	a, e
   4AB6 91            [ 4]  153 	sub	a, c
   4AB7 7A            [ 4]  154 	ld	a, d
   4AB8 98            [ 4]  155 	sbc	a, b
   4AB9 E2 BE 4A      [10]  156 	jp	PO, 00116$
   4ABC EE 80         [ 7]  157 	xor	a, #0x80
   4ABE                     158 00116$:
   4ABE 07            [ 4]  159 	rlca
   4ABF E6 01         [ 7]  160 	and	a,#0x01
   4AC1 EE 01         [ 7]  161 	xor	a, #0x01
   4AC3 6F            [ 4]  162 	ld	l, a
   4AC4 DD E1         [14]  163 	pop	ix
   4AC6 C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4AC7                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4AC7 21 04 00      [10]  171 	ld	hl, #4+0
   4ACA 39            [11]  172 	add	hl, sp
   4ACB 7E            [ 7]  173 	ld	a, (hl)
   4ACC F5            [11]  174 	push	af
   4ACD 33            [ 6]  175 	inc	sp
   4ACE 21 03 00      [10]  176 	ld	hl, #3
   4AD1 39            [11]  177 	add	hl, sp
   4AD2 4E            [ 7]  178 	ld	c, (hl)
   4AD3 23            [ 6]  179 	inc	hl
   4AD4 46            [ 7]  180 	ld	b, (hl)
   4AD5 C5            [11]  181 	push	bc
   4AD6 21 00 00      [10]  182 	ld	hl, #0x0000
   4AD9 E5            [11]  183 	push	hl
   4ADA CD E1 4A      [17]  184 	call	_collision_clamp_y_at
   4ADD F1            [10]  185 	pop	af
   4ADE F1            [10]  186 	pop	af
   4ADF 33            [ 6]  187 	inc	sp
   4AE0 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4AE1                     193 _collision_clamp_y_at::
   4AE1 DD E5         [15]  194 	push	ix
   4AE3 DD 21 00 00   [14]  195 	ld	ix,#0
   4AE7 DD 39         [15]  196 	add	ix,sp
   4AE9 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4AEA CD 91 4F      [17]  199 	call	_tilemap_ground_y
   4AED FD 21 47 5E   [14]  200 	ld	iy, #_ggroundy
   4AF1 FD 75 00      [19]  201 	ld	0 (iy), l
   4AF4 FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4AF8 DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4AFB 06 00         [ 7]  205 	ld	b, #0x00
   4AFD FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4B00 91            [ 4]  207 	sub	a, c
   4B01 5F            [ 4]  208 	ld	e, a
   4B02 FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4B05 98            [ 4]  210 	sbc	a, b
   4B06 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4B07 C5            [11]  213 	push	bc
   4B08 D5            [11]  214 	push	de
   4B09 DD 6E 04      [19]  215 	ld	l,4 (ix)
   4B0C DD 66 05      [19]  216 	ld	h,5 (ix)
   4B0F E5            [11]  217 	push	hl
   4B10 CD 99 4F      [17]  218 	call	_tilemap_platform_y_at
   4B13 F1            [10]  219 	pop	af
   4B14 D1            [10]  220 	pop	de
   4B15 C1            [10]  221 	pop	bc
   4B16 FD 21 49 5E   [14]  222 	ld	iy, #_gplatformy
   4B1A FD 75 00      [19]  223 	ld	0 (iy), l
   4B1D FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4B21 7B            [ 4]  226 	ld	a, e
   4B22 DD 96 06      [19]  227 	sub	a, 6 (ix)
   4B25 7A            [ 4]  228 	ld	a, d
   4B26 DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4B29 E2 2E 4B      [10]  230 	jp	PO, 00126$
   4B2C EE 80         [ 7]  231 	xor	a, #0x80
   4B2E                     232 00126$:
   4B2E 07            [ 4]  233 	rlca
   4B2F E6 01         [ 7]  234 	and	a,#0x01
   4B31 DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4B34 FD 21 49 5E   [14]  237 	ld	iy, #_gplatformy
   4B38 FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4B3B 3C            [ 4]  239 	inc	a
   4B3C FD B6 01      [19]  240 	or	a, 1 (iy)
   4B3F 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4B41 FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4B44 91            [ 4]  244 	sub	a, c
   4B45 4F            [ 4]  245 	ld	c, a
   4B46 FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4B49 98            [ 4]  247 	sbc	a, b
   4B4A 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4B4B 79            [ 4]  250 	ld	a, c
   4B4C DD 96 06      [19]  251 	sub	a, 6 (ix)
   4B4F 78            [ 4]  252 	ld	a, b
   4B50 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4B53 E2 58 4B      [10]  254 	jp	PO, 00128$
   4B56 EE 80         [ 7]  255 	xor	a, #0x80
   4B58                     256 00128$:
   4B58 F2 65 4B      [10]  257 	jp	P, 00105$
   4B5B DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4B5F 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4B61 69            [ 4]  261 	ld	l, c
   4B62 60            [ 4]  262 	ld	h, b
   4B63 18 0F         [12]  263 	jr	00108$
   4B65                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4B65 DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4B69 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4B6B EB            [ 4]  269 	ex	de,hl
   4B6C 18 06         [12]  270 	jr	00108$
   4B6E                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4B6E DD 6E 06      [19]  273 	ld	l,6 (ix)
   4B71 DD 66 07      [19]  274 	ld	h,7 (ix)
   4B74                     275 00108$:
   4B74 33            [ 6]  276 	inc	sp
   4B75 DD E1         [14]  277 	pop	ix
   4B77 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4B78                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4B78 21 07 00      [10]  285 	ld	hl, #7+0
   4B7B 39            [11]  286 	add	hl, sp
   4B7C 7E            [ 7]  287 	ld	a, (hl)
   4B7D F5            [11]  288 	push	af
   4B7E 33            [ 6]  289 	inc	sp
   4B7F 21 07 00      [10]  290 	ld	hl, #7+0
   4B82 39            [11]  291 	add	hl, sp
   4B83 7E            [ 7]  292 	ld	a, (hl)
   4B84 F5            [11]  293 	push	af
   4B85 33            [ 6]  294 	inc	sp
   4B86 21 06 00      [10]  295 	ld	hl, #6
   4B89 39            [11]  296 	add	hl, sp
   4B8A 4E            [ 7]  297 	ld	c, (hl)
   4B8B 23            [ 6]  298 	inc	hl
   4B8C 46            [ 7]  299 	ld	b, (hl)
   4B8D C5            [11]  300 	push	bc
   4B8E 21 06 00      [10]  301 	ld	hl, #6
   4B91 39            [11]  302 	add	hl, sp
   4B92 4E            [ 7]  303 	ld	c, (hl)
   4B93 23            [ 6]  304 	inc	hl
   4B94 46            [ 7]  305 	ld	b, (hl)
   4B95 C5            [11]  306 	push	bc
   4B96 CD CB 4F      [17]  307 	call	_tilemap_is_trap
   4B99 F1            [10]  308 	pop	af
   4B9A F1            [10]  309 	pop	af
   4B9B F1            [10]  310 	pop	af
   4B9C C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4B9D                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4B9D 21 07 00      [10]  318 	ld	hl, #7+0
   4BA0 39            [11]  319 	add	hl, sp
   4BA1 7E            [ 7]  320 	ld	a, (hl)
   4BA2 F5            [11]  321 	push	af
   4BA3 33            [ 6]  322 	inc	sp
   4BA4 21 07 00      [10]  323 	ld	hl, #7+0
   4BA7 39            [11]  324 	add	hl, sp
   4BA8 7E            [ 7]  325 	ld	a, (hl)
   4BA9 F5            [11]  326 	push	af
   4BAA 33            [ 6]  327 	inc	sp
   4BAB 21 06 00      [10]  328 	ld	hl, #6
   4BAE 39            [11]  329 	add	hl, sp
   4BAF 4E            [ 7]  330 	ld	c, (hl)
   4BB0 23            [ 6]  331 	inc	hl
   4BB1 46            [ 7]  332 	ld	b, (hl)
   4BB2 C5            [11]  333 	push	bc
   4BB3 21 06 00      [10]  334 	ld	hl, #6
   4BB6 39            [11]  335 	add	hl, sp
   4BB7 4E            [ 7]  336 	ld	c, (hl)
   4BB8 23            [ 6]  337 	inc	hl
   4BB9 46            [ 7]  338 	ld	b, (hl)
   4BBA C5            [11]  339 	push	bc
   4BBB CD 2F 50      [17]  340 	call	_tilemap_is_ladder
   4BBE F1            [10]  341 	pop	af
   4BBF F1            [10]  342 	pop	af
   4BC0 F1            [10]  343 	pop	af
   4BC1 C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5E62                     347 __xinit__ggroundy:
   5E62 A0 00               348 	.dw #0x00a0
   5E64                     349 __xinit__gplatformy:
   5E64 FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
