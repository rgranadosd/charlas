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
   5D7E                      33 _ggroundy:
   5D7E                      34 	.ds 2
   5D80                      35 _gplatformy:
   5D80                      36 	.ds 2
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
   49DC                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   49DC CD 47 4F      [17]   63 	call	_tilemap_ground_y
   49DF FD 21 7E 5D   [14]   64 	ld	iy, #_ggroundy
   49E3 FD 75 00      [19]   65 	ld	0 (iy), l
   49E6 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   49EA 21 20 00      [10]   68 	ld	hl, #0x0020
   49ED E5            [11]   69 	push	hl
   49EE CD 4F 4F      [17]   70 	call	_tilemap_platform_y_at
   49F1 F1            [10]   71 	pop	af
   49F2 FD 21 80 5D   [14]   72 	ld	iy, #_gplatformy
   49F6 FD 75 00      [19]   73 	ld	0 (iy), l
   49F9 FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   49FD C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   49FE                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   49FE 21 04 00      [10]   82 	ld	hl, #4+0
   4A01 39            [11]   83 	add	hl, sp
   4A02 7E            [ 7]   84 	ld	a, (hl)
   4A03 F5            [11]   85 	push	af
   4A04 33            [ 6]   86 	inc	sp
   4A05 21 03 00      [10]   87 	ld	hl, #3
   4A08 39            [11]   88 	add	hl, sp
   4A09 4E            [ 7]   89 	ld	c, (hl)
   4A0A 23            [ 6]   90 	inc	hl
   4A0B 46            [ 7]   91 	ld	b, (hl)
   4A0C C5            [11]   92 	push	bc
   4A0D 21 00 00      [10]   93 	ld	hl, #0x0000
   4A10 E5            [11]   94 	push	hl
   4A11 CD 18 4A      [17]   95 	call	_collision_is_on_ground_at
   4A14 F1            [10]   96 	pop	af
   4A15 F1            [10]   97 	pop	af
   4A16 33            [ 6]   98 	inc	sp
   4A17 C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4A18                     104 _collision_is_on_ground_at::
   4A18 DD E5         [15]  105 	push	ix
   4A1A DD 21 00 00   [14]  106 	ld	ix,#0
   4A1E DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4A20 CD 47 4F      [17]  109 	call	_tilemap_ground_y
   4A23 4D            [ 4]  110 	ld	c, l
   4A24 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4A26 C5            [11]  113 	push	bc
   4A27 DD 6E 04      [19]  114 	ld	l,4 (ix)
   4A2A DD 66 05      [19]  115 	ld	h,5 (ix)
   4A2D E5            [11]  116 	push	hl
   4A2E CD 4F 4F      [17]  117 	call	_tilemap_platform_y_at
   4A31 F1            [10]  118 	pop	af
   4A32 C1            [10]  119 	pop	bc
   4A33 FD 21 80 5D   [14]  120 	ld	iy, #_gplatformy
   4A37 FD 75 00      [19]  121 	ld	0 (iy), l
   4A3A FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4A3E DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4A41 16 00         [ 7]  125 	ld	d, #0x00
   4A43 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4A46 83            [ 4]  127 	add	a, e
   4A47 5F            [ 4]  128 	ld	e, a
   4A48 DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4A4B 8A            [ 4]  130 	adc	a, d
   4A4C 57            [ 4]  131 	ld	d, a
   4A4D FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4A50 3C            [ 4]  133 	inc	a
   4A51 FD B6 01      [19]  134 	or	a, 1 (iy)
   4A54 28 15         [12]  135 	jr	Z,00102$
   4A56 2A 80 5D      [16]  136 	ld	hl, (_gplatformy)
   4A59 23            [ 6]  137 	inc	hl
   4A5A 23            [ 6]  138 	inc	hl
   4A5B 7D            [ 4]  139 	ld	a, l
   4A5C 93            [ 4]  140 	sub	a, e
   4A5D 7C            [ 4]  141 	ld	a, h
   4A5E 9A            [ 4]  142 	sbc	a, d
   4A5F E2 64 4A      [10]  143 	jp	PO, 00115$
   4A62 EE 80         [ 7]  144 	xor	a, #0x80
   4A64                     145 00115$:
   4A64 FA 6B 4A      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4A67 ED 4B 80 5D   [20]  148 	ld	bc, (_gplatformy)
   4A6B                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4A6B 7B            [ 4]  152 	ld	a, e
   4A6C 91            [ 4]  153 	sub	a, c
   4A6D 7A            [ 4]  154 	ld	a, d
   4A6E 98            [ 4]  155 	sbc	a, b
   4A6F E2 74 4A      [10]  156 	jp	PO, 00116$
   4A72 EE 80         [ 7]  157 	xor	a, #0x80
   4A74                     158 00116$:
   4A74 07            [ 4]  159 	rlca
   4A75 E6 01         [ 7]  160 	and	a,#0x01
   4A77 EE 01         [ 7]  161 	xor	a, #0x01
   4A79 6F            [ 4]  162 	ld	l, a
   4A7A DD E1         [14]  163 	pop	ix
   4A7C C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4A7D                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4A7D 21 04 00      [10]  171 	ld	hl, #4+0
   4A80 39            [11]  172 	add	hl, sp
   4A81 7E            [ 7]  173 	ld	a, (hl)
   4A82 F5            [11]  174 	push	af
   4A83 33            [ 6]  175 	inc	sp
   4A84 21 03 00      [10]  176 	ld	hl, #3
   4A87 39            [11]  177 	add	hl, sp
   4A88 4E            [ 7]  178 	ld	c, (hl)
   4A89 23            [ 6]  179 	inc	hl
   4A8A 46            [ 7]  180 	ld	b, (hl)
   4A8B C5            [11]  181 	push	bc
   4A8C 21 00 00      [10]  182 	ld	hl, #0x0000
   4A8F E5            [11]  183 	push	hl
   4A90 CD 97 4A      [17]  184 	call	_collision_clamp_y_at
   4A93 F1            [10]  185 	pop	af
   4A94 F1            [10]  186 	pop	af
   4A95 33            [ 6]  187 	inc	sp
   4A96 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4A97                     193 _collision_clamp_y_at::
   4A97 DD E5         [15]  194 	push	ix
   4A99 DD 21 00 00   [14]  195 	ld	ix,#0
   4A9D DD 39         [15]  196 	add	ix,sp
   4A9F 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4AA0 CD 47 4F      [17]  199 	call	_tilemap_ground_y
   4AA3 FD 21 7E 5D   [14]  200 	ld	iy, #_ggroundy
   4AA7 FD 75 00      [19]  201 	ld	0 (iy), l
   4AAA FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4AAE DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4AB1 06 00         [ 7]  205 	ld	b, #0x00
   4AB3 FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4AB6 91            [ 4]  207 	sub	a, c
   4AB7 5F            [ 4]  208 	ld	e, a
   4AB8 FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4ABB 98            [ 4]  210 	sbc	a, b
   4ABC 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4ABD C5            [11]  213 	push	bc
   4ABE D5            [11]  214 	push	de
   4ABF DD 6E 04      [19]  215 	ld	l,4 (ix)
   4AC2 DD 66 05      [19]  216 	ld	h,5 (ix)
   4AC5 E5            [11]  217 	push	hl
   4AC6 CD 4F 4F      [17]  218 	call	_tilemap_platform_y_at
   4AC9 F1            [10]  219 	pop	af
   4ACA D1            [10]  220 	pop	de
   4ACB C1            [10]  221 	pop	bc
   4ACC FD 21 80 5D   [14]  222 	ld	iy, #_gplatformy
   4AD0 FD 75 00      [19]  223 	ld	0 (iy), l
   4AD3 FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4AD7 7B            [ 4]  226 	ld	a, e
   4AD8 DD 96 06      [19]  227 	sub	a, 6 (ix)
   4ADB 7A            [ 4]  228 	ld	a, d
   4ADC DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4ADF E2 E4 4A      [10]  230 	jp	PO, 00126$
   4AE2 EE 80         [ 7]  231 	xor	a, #0x80
   4AE4                     232 00126$:
   4AE4 07            [ 4]  233 	rlca
   4AE5 E6 01         [ 7]  234 	and	a,#0x01
   4AE7 DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4AEA FD 21 80 5D   [14]  237 	ld	iy, #_gplatformy
   4AEE FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4AF1 3C            [ 4]  239 	inc	a
   4AF2 FD B6 01      [19]  240 	or	a, 1 (iy)
   4AF5 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4AF7 FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4AFA 91            [ 4]  244 	sub	a, c
   4AFB 4F            [ 4]  245 	ld	c, a
   4AFC FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4AFF 98            [ 4]  247 	sbc	a, b
   4B00 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4B01 79            [ 4]  250 	ld	a, c
   4B02 DD 96 06      [19]  251 	sub	a, 6 (ix)
   4B05 78            [ 4]  252 	ld	a, b
   4B06 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4B09 E2 0E 4B      [10]  254 	jp	PO, 00128$
   4B0C EE 80         [ 7]  255 	xor	a, #0x80
   4B0E                     256 00128$:
   4B0E F2 1B 4B      [10]  257 	jp	P, 00105$
   4B11 DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4B15 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4B17 69            [ 4]  261 	ld	l, c
   4B18 60            [ 4]  262 	ld	h, b
   4B19 18 0F         [12]  263 	jr	00108$
   4B1B                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4B1B DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4B1F 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4B21 EB            [ 4]  269 	ex	de,hl
   4B22 18 06         [12]  270 	jr	00108$
   4B24                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4B24 DD 6E 06      [19]  273 	ld	l,6 (ix)
   4B27 DD 66 07      [19]  274 	ld	h,7 (ix)
   4B2A                     275 00108$:
   4B2A 33            [ 6]  276 	inc	sp
   4B2B DD E1         [14]  277 	pop	ix
   4B2D C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4B2E                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4B2E 21 07 00      [10]  285 	ld	hl, #7+0
   4B31 39            [11]  286 	add	hl, sp
   4B32 7E            [ 7]  287 	ld	a, (hl)
   4B33 F5            [11]  288 	push	af
   4B34 33            [ 6]  289 	inc	sp
   4B35 21 07 00      [10]  290 	ld	hl, #7+0
   4B38 39            [11]  291 	add	hl, sp
   4B39 7E            [ 7]  292 	ld	a, (hl)
   4B3A F5            [11]  293 	push	af
   4B3B 33            [ 6]  294 	inc	sp
   4B3C 21 06 00      [10]  295 	ld	hl, #6
   4B3F 39            [11]  296 	add	hl, sp
   4B40 4E            [ 7]  297 	ld	c, (hl)
   4B41 23            [ 6]  298 	inc	hl
   4B42 46            [ 7]  299 	ld	b, (hl)
   4B43 C5            [11]  300 	push	bc
   4B44 21 06 00      [10]  301 	ld	hl, #6
   4B47 39            [11]  302 	add	hl, sp
   4B48 4E            [ 7]  303 	ld	c, (hl)
   4B49 23            [ 6]  304 	inc	hl
   4B4A 46            [ 7]  305 	ld	b, (hl)
   4B4B C5            [11]  306 	push	bc
   4B4C CD 81 4F      [17]  307 	call	_tilemap_is_trap
   4B4F F1            [10]  308 	pop	af
   4B50 F1            [10]  309 	pop	af
   4B51 F1            [10]  310 	pop	af
   4B52 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4B53                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4B53 21 07 00      [10]  318 	ld	hl, #7+0
   4B56 39            [11]  319 	add	hl, sp
   4B57 7E            [ 7]  320 	ld	a, (hl)
   4B58 F5            [11]  321 	push	af
   4B59 33            [ 6]  322 	inc	sp
   4B5A 21 07 00      [10]  323 	ld	hl, #7+0
   4B5D 39            [11]  324 	add	hl, sp
   4B5E 7E            [ 7]  325 	ld	a, (hl)
   4B5F F5            [11]  326 	push	af
   4B60 33            [ 6]  327 	inc	sp
   4B61 21 06 00      [10]  328 	ld	hl, #6
   4B64 39            [11]  329 	add	hl, sp
   4B65 4E            [ 7]  330 	ld	c, (hl)
   4B66 23            [ 6]  331 	inc	hl
   4B67 46            [ 7]  332 	ld	b, (hl)
   4B68 C5            [11]  333 	push	bc
   4B69 21 06 00      [10]  334 	ld	hl, #6
   4B6C 39            [11]  335 	add	hl, sp
   4B6D 4E            [ 7]  336 	ld	c, (hl)
   4B6E 23            [ 6]  337 	inc	hl
   4B6F 46            [ 7]  338 	ld	b, (hl)
   4B70 C5            [11]  339 	push	bc
   4B71 CD E5 4F      [17]  340 	call	_tilemap_is_ladder
   4B74 F1            [10]  341 	pop	af
   4B75 F1            [10]  342 	pop	af
   4B76 F1            [10]  343 	pop	af
   4B77 C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5D99                     347 __xinit__ggroundy:
   5D99 A0 00               348 	.dw #0x00a0
   5D9B                     349 __xinit__gplatformy:
   5D9B FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
