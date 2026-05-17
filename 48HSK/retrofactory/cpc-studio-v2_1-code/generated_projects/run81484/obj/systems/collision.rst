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
   6D8F                      33 _ggroundy:
   6D8F                      34 	.ds 2
   6D91                      35 _gplatformy:
   6D91                      36 	.ds 2
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
   5292                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   5292 CD 18 5A      [17]   63 	call	_tilemap_ground_y
   5295 FD 21 8F 6D   [14]   64 	ld	iy, #_ggroundy
   5299 FD 75 00      [19]   65 	ld	0 (iy), l
   529C FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   52A0 21 20 00      [10]   68 	ld	hl, #0x0020
   52A3 E5            [11]   69 	push	hl
   52A4 CD 20 5A      [17]   70 	call	_tilemap_platform_y_at
   52A7 F1            [10]   71 	pop	af
   52A8 FD 21 91 6D   [14]   72 	ld	iy, #_gplatformy
   52AC FD 75 00      [19]   73 	ld	0 (iy), l
   52AF FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   52B3 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   52B4                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   52B4 21 04 00      [10]   82 	ld	hl, #4+0
   52B7 39            [11]   83 	add	hl, sp
   52B8 7E            [ 7]   84 	ld	a, (hl)
   52B9 F5            [11]   85 	push	af
   52BA 33            [ 6]   86 	inc	sp
   52BB 21 03 00      [10]   87 	ld	hl, #3
   52BE 39            [11]   88 	add	hl, sp
   52BF 4E            [ 7]   89 	ld	c, (hl)
   52C0 23            [ 6]   90 	inc	hl
   52C1 46            [ 7]   91 	ld	b, (hl)
   52C2 C5            [11]   92 	push	bc
   52C3 21 00 00      [10]   93 	ld	hl, #0x0000
   52C6 E5            [11]   94 	push	hl
   52C7 CD CE 52      [17]   95 	call	_collision_is_on_ground_at
   52CA F1            [10]   96 	pop	af
   52CB F1            [10]   97 	pop	af
   52CC 33            [ 6]   98 	inc	sp
   52CD C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   52CE                     104 _collision_is_on_ground_at::
   52CE DD E5         [15]  105 	push	ix
   52D0 DD 21 00 00   [14]  106 	ld	ix,#0
   52D4 DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   52D6 CD 18 5A      [17]  109 	call	_tilemap_ground_y
   52D9 4D            [ 4]  110 	ld	c, l
   52DA 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   52DC C5            [11]  113 	push	bc
   52DD DD 6E 04      [19]  114 	ld	l,4 (ix)
   52E0 DD 66 05      [19]  115 	ld	h,5 (ix)
   52E3 E5            [11]  116 	push	hl
   52E4 CD 20 5A      [17]  117 	call	_tilemap_platform_y_at
   52E7 F1            [10]  118 	pop	af
   52E8 C1            [10]  119 	pop	bc
   52E9 FD 21 91 6D   [14]  120 	ld	iy, #_gplatformy
   52ED FD 75 00      [19]  121 	ld	0 (iy), l
   52F0 FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   52F4 DD 5E 08      [19]  124 	ld	e, 8 (ix)
   52F7 16 00         [ 7]  125 	ld	d, #0x00
   52F9 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   52FC 83            [ 4]  127 	add	a, e
   52FD 5F            [ 4]  128 	ld	e, a
   52FE DD 7E 07      [19]  129 	ld	a, 7 (ix)
   5301 8A            [ 4]  130 	adc	a, d
   5302 57            [ 4]  131 	ld	d, a
   5303 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   5306 3C            [ 4]  133 	inc	a
   5307 FD B6 01      [19]  134 	or	a, 1 (iy)
   530A 28 15         [12]  135 	jr	Z,00102$
   530C 2A 91 6D      [16]  136 	ld	hl, (_gplatformy)
   530F 23            [ 6]  137 	inc	hl
   5310 23            [ 6]  138 	inc	hl
   5311 7D            [ 4]  139 	ld	a, l
   5312 93            [ 4]  140 	sub	a, e
   5313 7C            [ 4]  141 	ld	a, h
   5314 9A            [ 4]  142 	sbc	a, d
   5315 E2 1A 53      [10]  143 	jp	PO, 00115$
   5318 EE 80         [ 7]  144 	xor	a, #0x80
   531A                     145 00115$:
   531A FA 21 53      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   531D ED 4B 91 6D   [20]  148 	ld	bc, (_gplatformy)
   5321                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   5321 7B            [ 4]  152 	ld	a, e
   5322 91            [ 4]  153 	sub	a, c
   5323 7A            [ 4]  154 	ld	a, d
   5324 98            [ 4]  155 	sbc	a, b
   5325 E2 2A 53      [10]  156 	jp	PO, 00116$
   5328 EE 80         [ 7]  157 	xor	a, #0x80
   532A                     158 00116$:
   532A 07            [ 4]  159 	rlca
   532B E6 01         [ 7]  160 	and	a,#0x01
   532D EE 01         [ 7]  161 	xor	a, #0x01
   532F 6F            [ 4]  162 	ld	l, a
   5330 DD E1         [14]  163 	pop	ix
   5332 C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   5333                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   5333 21 04 00      [10]  171 	ld	hl, #4+0
   5336 39            [11]  172 	add	hl, sp
   5337 7E            [ 7]  173 	ld	a, (hl)
   5338 F5            [11]  174 	push	af
   5339 33            [ 6]  175 	inc	sp
   533A 21 03 00      [10]  176 	ld	hl, #3
   533D 39            [11]  177 	add	hl, sp
   533E 4E            [ 7]  178 	ld	c, (hl)
   533F 23            [ 6]  179 	inc	hl
   5340 46            [ 7]  180 	ld	b, (hl)
   5341 C5            [11]  181 	push	bc
   5342 21 00 00      [10]  182 	ld	hl, #0x0000
   5345 E5            [11]  183 	push	hl
   5346 CD 4D 53      [17]  184 	call	_collision_clamp_y_at
   5349 F1            [10]  185 	pop	af
   534A F1            [10]  186 	pop	af
   534B 33            [ 6]  187 	inc	sp
   534C C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   534D                     193 _collision_clamp_y_at::
   534D DD E5         [15]  194 	push	ix
   534F DD 21 00 00   [14]  195 	ld	ix,#0
   5353 DD 39         [15]  196 	add	ix,sp
                            197 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   5355 CD 18 5A      [17]  198 	call	_tilemap_ground_y
   5358 FD 21 8F 6D   [14]  199 	ld	iy, #_ggroundy
   535C FD 75 00      [19]  200 	ld	0 (iy), l
   535F FD 36 01 00   [19]  201 	ld	1 (iy), #0x00
                            202 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   5363 DD 4E 08      [19]  203 	ld	c, 8 (ix)
   5366 06 00         [ 7]  204 	ld	b, #0x00
   5368 FD 7E 00      [19]  205 	ld	a, 0 (iy)
   536B 91            [ 4]  206 	sub	a, c
   536C 5F            [ 4]  207 	ld	e, a
   536D FD 7E 01      [19]  208 	ld	a, 1 (iy)
   5370 98            [ 4]  209 	sbc	a, b
   5371 57            [ 4]  210 	ld	d, a
                            211 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   5372 C5            [11]  212 	push	bc
   5373 D5            [11]  213 	push	de
   5374 DD 6E 04      [19]  214 	ld	l,4 (ix)
   5377 DD 66 05      [19]  215 	ld	h,5 (ix)
   537A E5            [11]  216 	push	hl
   537B CD 20 5A      [17]  217 	call	_tilemap_platform_y_at
   537E F1            [10]  218 	pop	af
   537F D1            [10]  219 	pop	de
   5380 C1            [10]  220 	pop	bc
   5381 FD 21 91 6D   [14]  221 	ld	iy, #_gplatformy
   5385 FD 75 00      [19]  222 	ld	0 (iy), l
   5388 FD 36 01 00   [19]  223 	ld	1 (iy), #0x00
                            224 ;src/systems/collision.c:41: if (gplatformy != 255) {
   538C FD 7E 00      [19]  225 	ld	a, 0 (iy)
   538F 3C            [ 4]  226 	inc	a
   5390 FD B6 01      [19]  227 	or	a, 1 (iy)
   5393 28 32         [12]  228 	jr	Z,00105$
                            229 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   5395 FD 7E 00      [19]  230 	ld	a, 0 (iy)
   5398 91            [ 4]  231 	sub	a, c
   5399 4F            [ 4]  232 	ld	c, a
   539A FD 7E 01      [19]  233 	ld	a, 1 (iy)
   539D 98            [ 4]  234 	sbc	a, b
   539E 47            [ 4]  235 	ld	b, a
                            236 ;src/systems/collision.c:45: if (y > platformmaxy && y < gplatformy) {
   539F 79            [ 4]  237 	ld	a, c
   53A0 DD 96 06      [19]  238 	sub	a, 6 (ix)
   53A3 78            [ 4]  239 	ld	a, b
   53A4 DD 9E 07      [19]  240 	sbc	a, 7 (ix)
   53A7 E2 AC 53      [10]  241 	jp	PO, 00127$
   53AA EE 80         [ 7]  242 	xor	a, #0x80
   53AC                     243 00127$:
   53AC F2 C7 53      [10]  244 	jp	P, 00105$
   53AF 21 91 6D      [10]  245 	ld	hl, #_gplatformy
   53B2 DD 7E 06      [19]  246 	ld	a, 6 (ix)
   53B5 96            [ 7]  247 	sub	a, (hl)
   53B6 DD 7E 07      [19]  248 	ld	a, 7 (ix)
   53B9 23            [ 6]  249 	inc	hl
   53BA 9E            [ 7]  250 	sbc	a, (hl)
   53BB E2 C0 53      [10]  251 	jp	PO, 00128$
   53BE EE 80         [ 7]  252 	xor	a, #0x80
   53C0                     253 00128$:
   53C0 F2 C7 53      [10]  254 	jp	P, 00105$
                            255 ;src/systems/collision.c:46: return platformmaxy;
   53C3 69            [ 4]  256 	ld	l, c
   53C4 60            [ 4]  257 	ld	h, b
   53C5 18 19         [12]  258 	jr	00108$
   53C7                     259 00105$:
                            260 ;src/systems/collision.c:50: if (y > maxy) {
   53C7 7B            [ 4]  261 	ld	a, e
   53C8 DD 96 06      [19]  262 	sub	a, 6 (ix)
   53CB 7A            [ 4]  263 	ld	a, d
   53CC DD 9E 07      [19]  264 	sbc	a, 7 (ix)
   53CF E2 D4 53      [10]  265 	jp	PO, 00129$
   53D2 EE 80         [ 7]  266 	xor	a, #0x80
   53D4                     267 00129$:
   53D4 F2 DA 53      [10]  268 	jp	P, 00107$
                            269 ;src/systems/collision.c:51: return maxy;
   53D7 EB            [ 4]  270 	ex	de,hl
   53D8 18 06         [12]  271 	jr	00108$
   53DA                     272 00107$:
                            273 ;src/systems/collision.c:53: return y;
   53DA DD 6E 06      [19]  274 	ld	l,6 (ix)
   53DD DD 66 07      [19]  275 	ld	h,7 (ix)
   53E0                     276 00108$:
   53E0 DD E1         [14]  277 	pop	ix
   53E2 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:56: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   53E3                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:57: return tilemap_is_trap(x, y, w, h);
   53E3 21 07 00      [10]  285 	ld	hl, #7+0
   53E6 39            [11]  286 	add	hl, sp
   53E7 7E            [ 7]  287 	ld	a, (hl)
   53E8 F5            [11]  288 	push	af
   53E9 33            [ 6]  289 	inc	sp
   53EA 21 07 00      [10]  290 	ld	hl, #7+0
   53ED 39            [11]  291 	add	hl, sp
   53EE 7E            [ 7]  292 	ld	a, (hl)
   53EF F5            [11]  293 	push	af
   53F0 33            [ 6]  294 	inc	sp
   53F1 21 06 00      [10]  295 	ld	hl, #6
   53F4 39            [11]  296 	add	hl, sp
   53F5 4E            [ 7]  297 	ld	c, (hl)
   53F6 23            [ 6]  298 	inc	hl
   53F7 46            [ 7]  299 	ld	b, (hl)
   53F8 C5            [11]  300 	push	bc
   53F9 21 06 00      [10]  301 	ld	hl, #6
   53FC 39            [11]  302 	add	hl, sp
   53FD 4E            [ 7]  303 	ld	c, (hl)
   53FE 23            [ 6]  304 	inc	hl
   53FF 46            [ 7]  305 	ld	b, (hl)
   5400 C5            [11]  306 	push	bc
   5401 CD 52 5A      [17]  307 	call	_tilemap_is_trap
   5404 F1            [10]  308 	pop	af
   5405 F1            [10]  309 	pop	af
   5406 F1            [10]  310 	pop	af
   5407 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:60: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   5408                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:61: return tilemap_is_ladder(x, y, w, h);
   5408 21 07 00      [10]  318 	ld	hl, #7+0
   540B 39            [11]  319 	add	hl, sp
   540C 7E            [ 7]  320 	ld	a, (hl)
   540D F5            [11]  321 	push	af
   540E 33            [ 6]  322 	inc	sp
   540F 21 07 00      [10]  323 	ld	hl, #7+0
   5412 39            [11]  324 	add	hl, sp
   5413 7E            [ 7]  325 	ld	a, (hl)
   5414 F5            [11]  326 	push	af
   5415 33            [ 6]  327 	inc	sp
   5416 21 06 00      [10]  328 	ld	hl, #6
   5419 39            [11]  329 	add	hl, sp
   541A 4E            [ 7]  330 	ld	c, (hl)
   541B 23            [ 6]  331 	inc	hl
   541C 46            [ 7]  332 	ld	b, (hl)
   541D C5            [11]  333 	push	bc
   541E 21 06 00      [10]  334 	ld	hl, #6
   5421 39            [11]  335 	add	hl, sp
   5422 4E            [ 7]  336 	ld	c, (hl)
   5423 23            [ 6]  337 	inc	hl
   5424 46            [ 7]  338 	ld	b, (hl)
   5425 C5            [11]  339 	push	bc
   5426 CD B6 5A      [17]  340 	call	_tilemap_is_ladder
   5429 F1            [10]  341 	pop	af
   542A F1            [10]  342 	pop	af
   542B F1            [10]  343 	pop	af
   542C C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   6D98                     347 __xinit__ggroundy:
   6D98 A0 00               348 	.dw #0x00a0
   6D9A                     349 __xinit__gplatformy:
   6D9A FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
