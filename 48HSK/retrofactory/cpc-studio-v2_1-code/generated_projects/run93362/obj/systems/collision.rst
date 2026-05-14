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
   5E3F                      33 _ggroundy:
   5E3F                      34 	.ds 2
   5E41                      35 _gplatformy:
   5E41                      36 	.ds 2
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
   4A28                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4A28 CD 93 4F      [17]   63 	call	_tilemap_ground_y
   4A2B FD 21 3F 5E   [14]   64 	ld	iy, #_ggroundy
   4A2F FD 75 00      [19]   65 	ld	0 (iy), l
   4A32 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4A36 21 20 00      [10]   68 	ld	hl, #0x0020
   4A39 E5            [11]   69 	push	hl
   4A3A CD 9B 4F      [17]   70 	call	_tilemap_platform_y_at
   4A3D F1            [10]   71 	pop	af
   4A3E FD 21 41 5E   [14]   72 	ld	iy, #_gplatformy
   4A42 FD 75 00      [19]   73 	ld	0 (iy), l
   4A45 FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4A49 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4A4A                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4A4A 21 04 00      [10]   82 	ld	hl, #4+0
   4A4D 39            [11]   83 	add	hl, sp
   4A4E 7E            [ 7]   84 	ld	a, (hl)
   4A4F F5            [11]   85 	push	af
   4A50 33            [ 6]   86 	inc	sp
   4A51 21 03 00      [10]   87 	ld	hl, #3
   4A54 39            [11]   88 	add	hl, sp
   4A55 4E            [ 7]   89 	ld	c, (hl)
   4A56 23            [ 6]   90 	inc	hl
   4A57 46            [ 7]   91 	ld	b, (hl)
   4A58 C5            [11]   92 	push	bc
   4A59 21 00 00      [10]   93 	ld	hl, #0x0000
   4A5C E5            [11]   94 	push	hl
   4A5D CD 64 4A      [17]   95 	call	_collision_is_on_ground_at
   4A60 F1            [10]   96 	pop	af
   4A61 F1            [10]   97 	pop	af
   4A62 33            [ 6]   98 	inc	sp
   4A63 C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4A64                     104 _collision_is_on_ground_at::
   4A64 DD E5         [15]  105 	push	ix
   4A66 DD 21 00 00   [14]  106 	ld	ix,#0
   4A6A DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4A6C CD 93 4F      [17]  109 	call	_tilemap_ground_y
   4A6F 4D            [ 4]  110 	ld	c, l
   4A70 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4A72 C5            [11]  113 	push	bc
   4A73 DD 6E 04      [19]  114 	ld	l,4 (ix)
   4A76 DD 66 05      [19]  115 	ld	h,5 (ix)
   4A79 E5            [11]  116 	push	hl
   4A7A CD 9B 4F      [17]  117 	call	_tilemap_platform_y_at
   4A7D F1            [10]  118 	pop	af
   4A7E C1            [10]  119 	pop	bc
   4A7F FD 21 41 5E   [14]  120 	ld	iy, #_gplatformy
   4A83 FD 75 00      [19]  121 	ld	0 (iy), l
   4A86 FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4A8A DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4A8D 16 00         [ 7]  125 	ld	d, #0x00
   4A8F DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4A92 83            [ 4]  127 	add	a, e
   4A93 5F            [ 4]  128 	ld	e, a
   4A94 DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4A97 8A            [ 4]  130 	adc	a, d
   4A98 57            [ 4]  131 	ld	d, a
   4A99 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4A9C 3C            [ 4]  133 	inc	a
   4A9D FD B6 01      [19]  134 	or	a, 1 (iy)
   4AA0 28 15         [12]  135 	jr	Z,00102$
   4AA2 2A 41 5E      [16]  136 	ld	hl, (_gplatformy)
   4AA5 23            [ 6]  137 	inc	hl
   4AA6 23            [ 6]  138 	inc	hl
   4AA7 7D            [ 4]  139 	ld	a, l
   4AA8 93            [ 4]  140 	sub	a, e
   4AA9 7C            [ 4]  141 	ld	a, h
   4AAA 9A            [ 4]  142 	sbc	a, d
   4AAB E2 B0 4A      [10]  143 	jp	PO, 00115$
   4AAE EE 80         [ 7]  144 	xor	a, #0x80
   4AB0                     145 00115$:
   4AB0 FA B7 4A      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4AB3 ED 4B 41 5E   [20]  148 	ld	bc, (_gplatformy)
   4AB7                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4AB7 7B            [ 4]  152 	ld	a, e
   4AB8 91            [ 4]  153 	sub	a, c
   4AB9 7A            [ 4]  154 	ld	a, d
   4ABA 98            [ 4]  155 	sbc	a, b
   4ABB E2 C0 4A      [10]  156 	jp	PO, 00116$
   4ABE EE 80         [ 7]  157 	xor	a, #0x80
   4AC0                     158 00116$:
   4AC0 07            [ 4]  159 	rlca
   4AC1 E6 01         [ 7]  160 	and	a,#0x01
   4AC3 EE 01         [ 7]  161 	xor	a, #0x01
   4AC5 6F            [ 4]  162 	ld	l, a
   4AC6 DD E1         [14]  163 	pop	ix
   4AC8 C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4AC9                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4AC9 21 04 00      [10]  171 	ld	hl, #4+0
   4ACC 39            [11]  172 	add	hl, sp
   4ACD 7E            [ 7]  173 	ld	a, (hl)
   4ACE F5            [11]  174 	push	af
   4ACF 33            [ 6]  175 	inc	sp
   4AD0 21 03 00      [10]  176 	ld	hl, #3
   4AD3 39            [11]  177 	add	hl, sp
   4AD4 4E            [ 7]  178 	ld	c, (hl)
   4AD5 23            [ 6]  179 	inc	hl
   4AD6 46            [ 7]  180 	ld	b, (hl)
   4AD7 C5            [11]  181 	push	bc
   4AD8 21 00 00      [10]  182 	ld	hl, #0x0000
   4ADB E5            [11]  183 	push	hl
   4ADC CD E3 4A      [17]  184 	call	_collision_clamp_y_at
   4ADF F1            [10]  185 	pop	af
   4AE0 F1            [10]  186 	pop	af
   4AE1 33            [ 6]  187 	inc	sp
   4AE2 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4AE3                     193 _collision_clamp_y_at::
   4AE3 DD E5         [15]  194 	push	ix
   4AE5 DD 21 00 00   [14]  195 	ld	ix,#0
   4AE9 DD 39         [15]  196 	add	ix,sp
   4AEB 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4AEC CD 93 4F      [17]  199 	call	_tilemap_ground_y
   4AEF FD 21 3F 5E   [14]  200 	ld	iy, #_ggroundy
   4AF3 FD 75 00      [19]  201 	ld	0 (iy), l
   4AF6 FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4AFA DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4AFD 06 00         [ 7]  205 	ld	b, #0x00
   4AFF FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4B02 91            [ 4]  207 	sub	a, c
   4B03 5F            [ 4]  208 	ld	e, a
   4B04 FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4B07 98            [ 4]  210 	sbc	a, b
   4B08 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4B09 C5            [11]  213 	push	bc
   4B0A D5            [11]  214 	push	de
   4B0B DD 6E 04      [19]  215 	ld	l,4 (ix)
   4B0E DD 66 05      [19]  216 	ld	h,5 (ix)
   4B11 E5            [11]  217 	push	hl
   4B12 CD 9B 4F      [17]  218 	call	_tilemap_platform_y_at
   4B15 F1            [10]  219 	pop	af
   4B16 D1            [10]  220 	pop	de
   4B17 C1            [10]  221 	pop	bc
   4B18 FD 21 41 5E   [14]  222 	ld	iy, #_gplatformy
   4B1C FD 75 00      [19]  223 	ld	0 (iy), l
   4B1F FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4B23 7B            [ 4]  226 	ld	a, e
   4B24 DD 96 06      [19]  227 	sub	a, 6 (ix)
   4B27 7A            [ 4]  228 	ld	a, d
   4B28 DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4B2B E2 30 4B      [10]  230 	jp	PO, 00126$
   4B2E EE 80         [ 7]  231 	xor	a, #0x80
   4B30                     232 00126$:
   4B30 07            [ 4]  233 	rlca
   4B31 E6 01         [ 7]  234 	and	a,#0x01
   4B33 DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4B36 FD 21 41 5E   [14]  237 	ld	iy, #_gplatformy
   4B3A FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4B3D 3C            [ 4]  239 	inc	a
   4B3E FD B6 01      [19]  240 	or	a, 1 (iy)
   4B41 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4B43 FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4B46 91            [ 4]  244 	sub	a, c
   4B47 4F            [ 4]  245 	ld	c, a
   4B48 FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4B4B 98            [ 4]  247 	sbc	a, b
   4B4C 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4B4D 79            [ 4]  250 	ld	a, c
   4B4E DD 96 06      [19]  251 	sub	a, 6 (ix)
   4B51 78            [ 4]  252 	ld	a, b
   4B52 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4B55 E2 5A 4B      [10]  254 	jp	PO, 00128$
   4B58 EE 80         [ 7]  255 	xor	a, #0x80
   4B5A                     256 00128$:
   4B5A F2 67 4B      [10]  257 	jp	P, 00105$
   4B5D DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4B61 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4B63 69            [ 4]  261 	ld	l, c
   4B64 60            [ 4]  262 	ld	h, b
   4B65 18 0F         [12]  263 	jr	00108$
   4B67                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4B67 DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4B6B 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4B6D EB            [ 4]  269 	ex	de,hl
   4B6E 18 06         [12]  270 	jr	00108$
   4B70                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4B70 DD 6E 06      [19]  273 	ld	l,6 (ix)
   4B73 DD 66 07      [19]  274 	ld	h,7 (ix)
   4B76                     275 00108$:
   4B76 33            [ 6]  276 	inc	sp
   4B77 DD E1         [14]  277 	pop	ix
   4B79 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4B7A                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4B7A 21 07 00      [10]  285 	ld	hl, #7+0
   4B7D 39            [11]  286 	add	hl, sp
   4B7E 7E            [ 7]  287 	ld	a, (hl)
   4B7F F5            [11]  288 	push	af
   4B80 33            [ 6]  289 	inc	sp
   4B81 21 07 00      [10]  290 	ld	hl, #7+0
   4B84 39            [11]  291 	add	hl, sp
   4B85 7E            [ 7]  292 	ld	a, (hl)
   4B86 F5            [11]  293 	push	af
   4B87 33            [ 6]  294 	inc	sp
   4B88 21 06 00      [10]  295 	ld	hl, #6
   4B8B 39            [11]  296 	add	hl, sp
   4B8C 4E            [ 7]  297 	ld	c, (hl)
   4B8D 23            [ 6]  298 	inc	hl
   4B8E 46            [ 7]  299 	ld	b, (hl)
   4B8F C5            [11]  300 	push	bc
   4B90 21 06 00      [10]  301 	ld	hl, #6
   4B93 39            [11]  302 	add	hl, sp
   4B94 4E            [ 7]  303 	ld	c, (hl)
   4B95 23            [ 6]  304 	inc	hl
   4B96 46            [ 7]  305 	ld	b, (hl)
   4B97 C5            [11]  306 	push	bc
   4B98 CD CD 4F      [17]  307 	call	_tilemap_is_trap
   4B9B F1            [10]  308 	pop	af
   4B9C F1            [10]  309 	pop	af
   4B9D F1            [10]  310 	pop	af
   4B9E C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4B9F                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4B9F 21 07 00      [10]  318 	ld	hl, #7+0
   4BA2 39            [11]  319 	add	hl, sp
   4BA3 7E            [ 7]  320 	ld	a, (hl)
   4BA4 F5            [11]  321 	push	af
   4BA5 33            [ 6]  322 	inc	sp
   4BA6 21 07 00      [10]  323 	ld	hl, #7+0
   4BA9 39            [11]  324 	add	hl, sp
   4BAA 7E            [ 7]  325 	ld	a, (hl)
   4BAB F5            [11]  326 	push	af
   4BAC 33            [ 6]  327 	inc	sp
   4BAD 21 06 00      [10]  328 	ld	hl, #6
   4BB0 39            [11]  329 	add	hl, sp
   4BB1 4E            [ 7]  330 	ld	c, (hl)
   4BB2 23            [ 6]  331 	inc	hl
   4BB3 46            [ 7]  332 	ld	b, (hl)
   4BB4 C5            [11]  333 	push	bc
   4BB5 21 06 00      [10]  334 	ld	hl, #6
   4BB8 39            [11]  335 	add	hl, sp
   4BB9 4E            [ 7]  336 	ld	c, (hl)
   4BBA 23            [ 6]  337 	inc	hl
   4BBB 46            [ 7]  338 	ld	b, (hl)
   4BBC C5            [11]  339 	push	bc
   4BBD CD 31 50      [17]  340 	call	_tilemap_is_ladder
   4BC0 F1            [10]  341 	pop	af
   4BC1 F1            [10]  342 	pop	af
   4BC2 F1            [10]  343 	pop	af
   4BC3 C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   5E5A                     347 __xinit__ggroundy:
   5E5A A0 00               348 	.dw #0x00a0
   5E5C                     349 __xinit__gplatformy:
   5E5C FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
