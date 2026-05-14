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
   5F1C                      33 _ggroundy:
   5F1C                      34 	.ds 2
   5F1E                      35 _gplatformy:
   5F1E                      36 	.ds 2
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
   49FF                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   49FF CD B0 4F      [17]   63 	call	_tilemap_ground_y
   4A02 FD 21 1C 5F   [14]   64 	ld	iy, #_ggroundy
   4A06 FD 75 00      [19]   65 	ld	0 (iy), l
   4A09 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4A0D 21 20 00      [10]   68 	ld	hl, #0x0020
   4A10 E5            [11]   69 	push	hl
   4A11 CD B8 4F      [17]   70 	call	_tilemap_platform_y_at
   4A14 F1            [10]   71 	pop	af
   4A15 FD 21 1E 5F   [14]   72 	ld	iy, #_gplatformy
   4A19 FD 75 00      [19]   73 	ld	0 (iy), l
   4A1C FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4A20 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4A21                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4A21 21 04 00      [10]   82 	ld	hl, #4+0
   4A24 39            [11]   83 	add	hl, sp
   4A25 7E            [ 7]   84 	ld	a, (hl)
   4A26 F5            [11]   85 	push	af
   4A27 33            [ 6]   86 	inc	sp
   4A28 21 03 00      [10]   87 	ld	hl, #3
   4A2B 39            [11]   88 	add	hl, sp
   4A2C 4E            [ 7]   89 	ld	c, (hl)
   4A2D 23            [ 6]   90 	inc	hl
   4A2E 46            [ 7]   91 	ld	b, (hl)
   4A2F C5            [11]   92 	push	bc
   4A30 21 00 00      [10]   93 	ld	hl, #0x0000
   4A33 E5            [11]   94 	push	hl
   4A34 CD 3B 4A      [17]   95 	call	_collision_is_on_ground_at
   4A37 F1            [10]   96 	pop	af
   4A38 F1            [10]   97 	pop	af
   4A39 33            [ 6]   98 	inc	sp
   4A3A C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4A3B                     104 _collision_is_on_ground_at::
   4A3B DD E5         [15]  105 	push	ix
   4A3D DD 21 00 00   [14]  106 	ld	ix,#0
   4A41 DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4A43 CD B0 4F      [17]  109 	call	_tilemap_ground_y
   4A46 4D            [ 4]  110 	ld	c, l
   4A47 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4A49 C5            [11]  113 	push	bc
   4A4A DD 6E 04      [19]  114 	ld	l,4 (ix)
   4A4D DD 66 05      [19]  115 	ld	h,5 (ix)
   4A50 E5            [11]  116 	push	hl
   4A51 CD B8 4F      [17]  117 	call	_tilemap_platform_y_at
   4A54 F1            [10]  118 	pop	af
   4A55 C1            [10]  119 	pop	bc
   4A56 FD 21 1E 5F   [14]  120 	ld	iy, #_gplatformy
   4A5A FD 75 00      [19]  121 	ld	0 (iy), l
   4A5D FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4A61 DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4A64 16 00         [ 7]  125 	ld	d, #0x00
   4A66 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4A69 83            [ 4]  127 	add	a, e
   4A6A 5F            [ 4]  128 	ld	e, a
   4A6B DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4A6E 8A            [ 4]  130 	adc	a, d
   4A6F 57            [ 4]  131 	ld	d, a
   4A70 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4A73 3C            [ 4]  133 	inc	a
   4A74 FD B6 01      [19]  134 	or	a, 1 (iy)
   4A77 28 15         [12]  135 	jr	Z,00102$
   4A79 2A 1E 5F      [16]  136 	ld	hl, (_gplatformy)
   4A7C 23            [ 6]  137 	inc	hl
   4A7D 23            [ 6]  138 	inc	hl
   4A7E 7D            [ 4]  139 	ld	a, l
   4A7F 93            [ 4]  140 	sub	a, e
   4A80 7C            [ 4]  141 	ld	a, h
   4A81 9A            [ 4]  142 	sbc	a, d
   4A82 E2 87 4A      [10]  143 	jp	PO, 00115$
   4A85 EE 80         [ 7]  144 	xor	a, #0x80
   4A87                     145 00115$:
   4A87 FA 8E 4A      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4A8A ED 4B 1E 5F   [20]  148 	ld	bc, (_gplatformy)
   4A8E                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4A8E 7B            [ 4]  152 	ld	a, e
   4A8F 91            [ 4]  153 	sub	a, c
   4A90 7A            [ 4]  154 	ld	a, d
   4A91 98            [ 4]  155 	sbc	a, b
   4A92 E2 97 4A      [10]  156 	jp	PO, 00116$
   4A95 EE 80         [ 7]  157 	xor	a, #0x80
   4A97                     158 00116$:
   4A97 07            [ 4]  159 	rlca
   4A98 E6 01         [ 7]  160 	and	a,#0x01
   4A9A EE 01         [ 7]  161 	xor	a, #0x01
   4A9C 6F            [ 4]  162 	ld	l, a
   4A9D DD E1         [14]  163 	pop	ix
   4A9F C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4AA0                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4AA0 21 04 00      [10]  171 	ld	hl, #4+0
   4AA3 39            [11]  172 	add	hl, sp
   4AA4 7E            [ 7]  173 	ld	a, (hl)
   4AA5 F5            [11]  174 	push	af
   4AA6 33            [ 6]  175 	inc	sp
   4AA7 21 03 00      [10]  176 	ld	hl, #3
   4AAA 39            [11]  177 	add	hl, sp
   4AAB 4E            [ 7]  178 	ld	c, (hl)
   4AAC 23            [ 6]  179 	inc	hl
   4AAD 46            [ 7]  180 	ld	b, (hl)
   4AAE C5            [11]  181 	push	bc
   4AAF 21 00 00      [10]  182 	ld	hl, #0x0000
   4AB2 E5            [11]  183 	push	hl
   4AB3 CD BA 4A      [17]  184 	call	_collision_clamp_y_at
   4AB6 F1            [10]  185 	pop	af
   4AB7 F1            [10]  186 	pop	af
   4AB8 33            [ 6]  187 	inc	sp
   4AB9 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4ABA                     193 _collision_clamp_y_at::
   4ABA DD E5         [15]  194 	push	ix
   4ABC DD 21 00 00   [14]  195 	ld	ix,#0
   4AC0 DD 39         [15]  196 	add	ix,sp
   4AC2 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4AC3 CD B0 4F      [17]  199 	call	_tilemap_ground_y
   4AC6 FD 21 1C 5F   [14]  200 	ld	iy, #_ggroundy
   4ACA FD 75 00      [19]  201 	ld	0 (iy), l
   4ACD FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4AD1 DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4AD4 06 00         [ 7]  205 	ld	b, #0x00
   4AD6 FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4AD9 91            [ 4]  207 	sub	a, c
   4ADA 5F            [ 4]  208 	ld	e, a
   4ADB FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4ADE 98            [ 4]  210 	sbc	a, b
   4ADF 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4AE0 C5            [11]  213 	push	bc
   4AE1 D5            [11]  214 	push	de
   4AE2 DD 6E 04      [19]  215 	ld	l,4 (ix)
   4AE5 DD 66 05      [19]  216 	ld	h,5 (ix)
   4AE8 E5            [11]  217 	push	hl
   4AE9 CD B8 4F      [17]  218 	call	_tilemap_platform_y_at
   4AEC F1            [10]  219 	pop	af
   4AED D1            [10]  220 	pop	de
   4AEE C1            [10]  221 	pop	bc
   4AEF FD 21 1E 5F   [14]  222 	ld	iy, #_gplatformy
   4AF3 FD 75 00      [19]  223 	ld	0 (iy), l
   4AF6 FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4AFA 7B            [ 4]  226 	ld	a, e
   4AFB DD 96 06      [19]  227 	sub	a, 6 (ix)
   4AFE 7A            [ 4]  228 	ld	a, d
   4AFF DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4B02 E2 07 4B      [10]  230 	jp	PO, 00126$
   4B05 EE 80         [ 7]  231 	xor	a, #0x80
   4B07                     232 00126$:
   4B07 07            [ 4]  233 	rlca
   4B08 E6 01         [ 7]  234 	and	a,#0x01
   4B0A DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4B0D FD 21 1E 5F   [14]  237 	ld	iy, #_gplatformy
   4B11 FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4B14 3C            [ 4]  239 	inc	a
   4B15 FD B6 01      [19]  240 	or	a, 1 (iy)
   4B18 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4B1A FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4B1D 91            [ 4]  244 	sub	a, c
   4B1E 4F            [ 4]  245 	ld	c, a
   4B1F FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4B22 98            [ 4]  247 	sbc	a, b
   4B23 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4B24 79            [ 4]  250 	ld	a, c
   4B25 DD 96 06      [19]  251 	sub	a, 6 (ix)
   4B28 78            [ 4]  252 	ld	a, b
   4B29 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4B2C E2 31 4B      [10]  254 	jp	PO, 00128$
   4B2F EE 80         [ 7]  255 	xor	a, #0x80
   4B31                     256 00128$:
   4B31 F2 3E 4B      [10]  257 	jp	P, 00105$
   4B34 DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4B38 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4B3A 69            [ 4]  261 	ld	l, c
   4B3B 60            [ 4]  262 	ld	h, b
   4B3C 18 0F         [12]  263 	jr	00108$
   4B3E                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4B3E DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4B42 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4B44 EB            [ 4]  269 	ex	de,hl
   4B45 18 06         [12]  270 	jr	00108$
   4B47                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4B47 DD 6E 06      [19]  273 	ld	l,6 (ix)
   4B4A DD 66 07      [19]  274 	ld	h,7 (ix)
   4B4D                     275 00108$:
   4B4D 33            [ 6]  276 	inc	sp
   4B4E DD E1         [14]  277 	pop	ix
   4B50 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4B51                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4B51 21 07 00      [10]  285 	ld	hl, #7+0
   4B54 39            [11]  286 	add	hl, sp
   4B55 7E            [ 7]  287 	ld	a, (hl)
   4B56 F5            [11]  288 	push	af
   4B57 33            [ 6]  289 	inc	sp
   4B58 21 07 00      [10]  290 	ld	hl, #7+0
   4B5B 39            [11]  291 	add	hl, sp
   4B5C 7E            [ 7]  292 	ld	a, (hl)
   4B5D F5            [11]  293 	push	af
   4B5E 33            [ 6]  294 	inc	sp
   4B5F 21 06 00      [10]  295 	ld	hl, #6
   4B62 39            [11]  296 	add	hl, sp
   4B63 4E            [ 7]  297 	ld	c, (hl)
   4B64 23            [ 6]  298 	inc	hl
   4B65 46            [ 7]  299 	ld	b, (hl)
   4B66 C5            [11]  300 	push	bc
   4B67 21 06 00      [10]  301 	ld	hl, #6
   4B6A 39            [11]  302 	add	hl, sp
   4B6B 4E            [ 7]  303 	ld	c, (hl)
   4B6C 23            [ 6]  304 	inc	hl
   4B6D 46            [ 7]  305 	ld	b, (hl)
   4B6E C5            [11]  306 	push	bc
   4B6F CD EA 4F      [17]  307 	call	_tilemap_is_trap
   4B72 F1            [10]  308 	pop	af
   4B73 F1            [10]  309 	pop	af
   4B74 F1            [10]  310 	pop	af
   4B75 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4B76                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4B76 21 07 00      [10]  318 	ld	hl, #7+0
   4B79 39            [11]  319 	add	hl, sp
   4B7A 7E            [ 7]  320 	ld	a, (hl)
   4B7B F5            [11]  321 	push	af
   4B7C 33            [ 6]  322 	inc	sp
   4B7D 21 07 00      [10]  323 	ld	hl, #7+0
   4B80 39            [11]  324 	add	hl, sp
   4B81 7E            [ 7]  325 	ld	a, (hl)
   4B82 F5            [11]  326 	push	af
   4B83 33            [ 6]  327 	inc	sp
   4B84 21 06 00      [10]  328 	ld	hl, #6
   4B87 39            [11]  329 	add	hl, sp
   4B88 4E            [ 7]  330 	ld	c, (hl)
   4B89 23            [ 6]  331 	inc	hl
   4B8A 46            [ 7]  332 	ld	b, (hl)
   4B8B C5            [11]  333 	push	bc
   4B8C 21 06 00      [10]  334 	ld	hl, #6
   4B8F 39            [11]  335 	add	hl, sp
   4B90 4E            [ 7]  336 	ld	c, (hl)
   4B91 23            [ 6]  337 	inc	hl
   4B92 46            [ 7]  338 	ld	b, (hl)
   4B93 C5            [11]  339 	push	bc
   4B94 CD 4E 50      [17]  340 	call	_tilemap_is_ladder
   4B97 F1            [10]  341 	pop	af
   4B98 F1            [10]  342 	pop	af
   4B99 F1            [10]  343 	pop	af
   4B9A C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5F38                     347 __xinit__ggroundy:
   5F38 A0 00               348 	.dw #0x00a0
   5F3A                     349 __xinit__gplatformy:
   5F3A FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
