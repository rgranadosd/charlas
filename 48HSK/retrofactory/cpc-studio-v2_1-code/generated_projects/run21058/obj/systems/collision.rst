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
   6483                      33 _ggroundy:
   6483                      34 	.ds 2
   6485                      35 _gplatformy:
   6485                      36 	.ds 2
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
   4CBF                      61 _collision_init::
                             62 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   4CBF CD 41 53      [17]   63 	call	_tilemap_ground_y
   4CC2 FD 21 83 64   [14]   64 	ld	iy, #_ggroundy
   4CC6 FD 75 00      [19]   65 	ld	0 (iy), l
   4CC9 FD 36 01 00   [19]   66 	ld	1 (iy), #0x00
                             67 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   4CCD 21 20 00      [10]   68 	ld	hl, #0x0020
   4CD0 E5            [11]   69 	push	hl
   4CD1 CD 49 53      [17]   70 	call	_tilemap_platform_y_at
   4CD4 F1            [10]   71 	pop	af
   4CD5 FD 21 85 64   [14]   72 	ld	iy, #_gplatformy
   4CD9 FD 75 00      [19]   73 	ld	0 (iy), l
   4CDC FD 36 01 00   [19]   74 	ld	1 (iy), #0x00
   4CE0 C9            [10]   75 	ret
                             76 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             77 ;	---------------------------------
                             78 ; Function collision_is_on_ground
                             79 ; ---------------------------------
   4CE1                      80 _collision_is_on_ground::
                             81 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   4CE1 21 04 00      [10]   82 	ld	hl, #4+0
   4CE4 39            [11]   83 	add	hl, sp
   4CE5 7E            [ 7]   84 	ld	a, (hl)
   4CE6 F5            [11]   85 	push	af
   4CE7 33            [ 6]   86 	inc	sp
   4CE8 21 03 00      [10]   87 	ld	hl, #3
   4CEB 39            [11]   88 	add	hl, sp
   4CEC 4E            [ 7]   89 	ld	c, (hl)
   4CED 23            [ 6]   90 	inc	hl
   4CEE 46            [ 7]   91 	ld	b, (hl)
   4CEF C5            [11]   92 	push	bc
   4CF0 21 00 00      [10]   93 	ld	hl, #0x0000
   4CF3 E5            [11]   94 	push	hl
   4CF4 CD FB 4C      [17]   95 	call	_collision_is_on_ground_at
   4CF7 F1            [10]   96 	pop	af
   4CF8 F1            [10]   97 	pop	af
   4CF9 33            [ 6]   98 	inc	sp
   4CFA C9            [10]   99 	ret
                            100 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                            101 ;	---------------------------------
                            102 ; Function collision_is_on_ground_at
                            103 ; ---------------------------------
   4CFB                     104 _collision_is_on_ground_at::
   4CFB DD E5         [15]  105 	push	ix
   4CFD DD 21 00 00   [14]  106 	ld	ix,#0
   4D01 DD 39         [15]  107 	add	ix,sp
                            108 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   4D03 CD 41 53      [17]  109 	call	_tilemap_ground_y
   4D06 4D            [ 4]  110 	ld	c, l
   4D07 06 00         [ 7]  111 	ld	b, #0x00
                            112 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   4D09 C5            [11]  113 	push	bc
   4D0A DD 6E 04      [19]  114 	ld	l,4 (ix)
   4D0D DD 66 05      [19]  115 	ld	h,5 (ix)
   4D10 E5            [11]  116 	push	hl
   4D11 CD 49 53      [17]  117 	call	_tilemap_platform_y_at
   4D14 F1            [10]  118 	pop	af
   4D15 C1            [10]  119 	pop	bc
   4D16 FD 21 85 64   [14]  120 	ld	iy, #_gplatformy
   4D1A FD 75 00      [19]  121 	ld	0 (iy), l
   4D1D FD 36 01 00   [19]  122 	ld	1 (iy), #0x00
                            123 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4D21 DD 5E 08      [19]  124 	ld	e, 8 (ix)
   4D24 16 00         [ 7]  125 	ld	d, #0x00
   4D26 DD 7E 06      [19]  126 	ld	a, 6 (ix)
   4D29 83            [ 4]  127 	add	a, e
   4D2A 5F            [ 4]  128 	ld	e, a
   4D2B DD 7E 07      [19]  129 	ld	a, 7 (ix)
   4D2E 8A            [ 4]  130 	adc	a, d
   4D2F 57            [ 4]  131 	ld	d, a
   4D30 FD 7E 00      [19]  132 	ld	a, 0 (iy)
   4D33 3C            [ 4]  133 	inc	a
   4D34 FD B6 01      [19]  134 	or	a, 1 (iy)
   4D37 28 15         [12]  135 	jr	Z,00102$
   4D39 2A 85 64      [16]  136 	ld	hl, (_gplatformy)
   4D3C 23            [ 6]  137 	inc	hl
   4D3D 23            [ 6]  138 	inc	hl
   4D3E 7D            [ 4]  139 	ld	a, l
   4D3F 93            [ 4]  140 	sub	a, e
   4D40 7C            [ 4]  141 	ld	a, h
   4D41 9A            [ 4]  142 	sbc	a, d
   4D42 E2 47 4D      [10]  143 	jp	PO, 00115$
   4D45 EE 80         [ 7]  144 	xor	a, #0x80
   4D47                     145 00115$:
   4D47 FA 4E 4D      [10]  146 	jp	M, 00102$
                            147 ;src/systems/collision.c:23: support = gplatformy;
   4D4A ED 4B 85 64   [20]  148 	ld	bc, (_gplatformy)
   4D4E                     149 00102$:
                            150 ;src/systems/collision.c:26: feet = y + (i16)h;
                            151 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4D4E 7B            [ 4]  152 	ld	a, e
   4D4F 91            [ 4]  153 	sub	a, c
   4D50 7A            [ 4]  154 	ld	a, d
   4D51 98            [ 4]  155 	sbc	a, b
   4D52 E2 57 4D      [10]  156 	jp	PO, 00116$
   4D55 EE 80         [ 7]  157 	xor	a, #0x80
   4D57                     158 00116$:
   4D57 07            [ 4]  159 	rlca
   4D58 E6 01         [ 7]  160 	and	a,#0x01
   4D5A EE 01         [ 7]  161 	xor	a, #0x01
   4D5C 6F            [ 4]  162 	ld	l, a
   4D5D DD E1         [14]  163 	pop	ix
   4D5F C9            [10]  164 	ret
                            165 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            166 ;	---------------------------------
                            167 ; Function collision_clamp_y_to_ground
                            168 ; ---------------------------------
   4D60                     169 _collision_clamp_y_to_ground::
                            170 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4D60 21 04 00      [10]  171 	ld	hl, #4+0
   4D63 39            [11]  172 	add	hl, sp
   4D64 7E            [ 7]  173 	ld	a, (hl)
   4D65 F5            [11]  174 	push	af
   4D66 33            [ 6]  175 	inc	sp
   4D67 21 03 00      [10]  176 	ld	hl, #3
   4D6A 39            [11]  177 	add	hl, sp
   4D6B 4E            [ 7]  178 	ld	c, (hl)
   4D6C 23            [ 6]  179 	inc	hl
   4D6D 46            [ 7]  180 	ld	b, (hl)
   4D6E C5            [11]  181 	push	bc
   4D6F 21 00 00      [10]  182 	ld	hl, #0x0000
   4D72 E5            [11]  183 	push	hl
   4D73 CD 7A 4D      [17]  184 	call	_collision_clamp_y_at
   4D76 F1            [10]  185 	pop	af
   4D77 F1            [10]  186 	pop	af
   4D78 33            [ 6]  187 	inc	sp
   4D79 C9            [10]  188 	ret
                            189 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            190 ;	---------------------------------
                            191 ; Function collision_clamp_y_at
                            192 ; ---------------------------------
   4D7A                     193 _collision_clamp_y_at::
   4D7A DD E5         [15]  194 	push	ix
   4D7C DD 21 00 00   [14]  195 	ld	ix,#0
   4D80 DD 39         [15]  196 	add	ix,sp
   4D82 3B            [ 6]  197 	dec	sp
                            198 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4D83 CD 41 53      [17]  199 	call	_tilemap_ground_y
   4D86 FD 21 83 64   [14]  200 	ld	iy, #_ggroundy
   4D8A FD 75 00      [19]  201 	ld	0 (iy), l
   4D8D FD 36 01 00   [19]  202 	ld	1 (iy), #0x00
                            203 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4D91 DD 4E 08      [19]  204 	ld	c, 8 (ix)
   4D94 06 00         [ 7]  205 	ld	b, #0x00
   4D96 FD 7E 00      [19]  206 	ld	a, 0 (iy)
   4D99 91            [ 4]  207 	sub	a, c
   4D9A 5F            [ 4]  208 	ld	e, a
   4D9B FD 7E 01      [19]  209 	ld	a, 1 (iy)
   4D9E 98            [ 4]  210 	sbc	a, b
   4D9F 57            [ 4]  211 	ld	d, a
                            212 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4DA0 C5            [11]  213 	push	bc
   4DA1 D5            [11]  214 	push	de
   4DA2 DD 6E 04      [19]  215 	ld	l,4 (ix)
   4DA5 DD 66 05      [19]  216 	ld	h,5 (ix)
   4DA8 E5            [11]  217 	push	hl
   4DA9 CD 49 53      [17]  218 	call	_tilemap_platform_y_at
   4DAC F1            [10]  219 	pop	af
   4DAD D1            [10]  220 	pop	de
   4DAE C1            [10]  221 	pop	bc
   4DAF FD 21 85 64   [14]  222 	ld	iy, #_gplatformy
   4DB3 FD 75 00      [19]  223 	ld	0 (iy), l
   4DB6 FD 36 01 00   [19]  224 	ld	1 (iy), #0x00
                            225 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4DBA 7B            [ 4]  226 	ld	a, e
   4DBB DD 96 06      [19]  227 	sub	a, 6 (ix)
   4DBE 7A            [ 4]  228 	ld	a, d
   4DBF DD 9E 07      [19]  229 	sbc	a, 7 (ix)
   4DC2 E2 C7 4D      [10]  230 	jp	PO, 00126$
   4DC5 EE 80         [ 7]  231 	xor	a, #0x80
   4DC7                     232 00126$:
   4DC7 07            [ 4]  233 	rlca
   4DC8 E6 01         [ 7]  234 	and	a,#0x01
   4DCA DD 77 FF      [19]  235 	ld	-1 (ix), a
                            236 ;src/systems/collision.c:41: if (gplatformy != 255) {
   4DCD FD 21 85 64   [14]  237 	ld	iy, #_gplatformy
   4DD1 FD 7E 00      [19]  238 	ld	a, 0 (iy)
   4DD4 3C            [ 4]  239 	inc	a
   4DD5 FD B6 01      [19]  240 	or	a, 1 (iy)
   4DD8 28 24         [12]  241 	jr	Z,00105$
                            242 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   4DDA FD 7E 00      [19]  243 	ld	a, 0 (iy)
   4DDD 91            [ 4]  244 	sub	a, c
   4DDE 4F            [ 4]  245 	ld	c, a
   4DDF FD 7E 01      [19]  246 	ld	a, 1 (iy)
   4DE2 98            [ 4]  247 	sbc	a, b
   4DE3 47            [ 4]  248 	ld	b, a
                            249 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   4DE4 79            [ 4]  250 	ld	a, c
   4DE5 DD 96 06      [19]  251 	sub	a, 6 (ix)
   4DE8 78            [ 4]  252 	ld	a, b
   4DE9 DD 9E 07      [19]  253 	sbc	a, 7 (ix)
   4DEC E2 F1 4D      [10]  254 	jp	PO, 00128$
   4DEF EE 80         [ 7]  255 	xor	a, #0x80
   4DF1                     256 00128$:
   4DF1 F2 FE 4D      [10]  257 	jp	P, 00105$
   4DF4 DD CB FF 46   [20]  258 	bit	0, -1 (ix)
   4DF8 20 04         [12]  259 	jr	NZ,00105$
                            260 ;src/systems/collision.c:44: return platformmaxy;
   4DFA 69            [ 4]  261 	ld	l, c
   4DFB 60            [ 4]  262 	ld	h, b
   4DFC 18 0F         [12]  263 	jr	00108$
   4DFE                     264 00105$:
                            265 ;src/systems/collision.c:48: if (y > maxy) {
   4DFE DD CB FF 46   [20]  266 	bit	0, -1 (ix)
   4E02 28 03         [12]  267 	jr	Z,00107$
                            268 ;src/systems/collision.c:49: return maxy;
   4E04 EB            [ 4]  269 	ex	de,hl
   4E05 18 06         [12]  270 	jr	00108$
   4E07                     271 00107$:
                            272 ;src/systems/collision.c:51: return y;
   4E07 DD 6E 06      [19]  273 	ld	l,6 (ix)
   4E0A DD 66 07      [19]  274 	ld	h,7 (ix)
   4E0D                     275 00108$:
   4E0D 33            [ 6]  276 	inc	sp
   4E0E DD E1         [14]  277 	pop	ix
   4E10 C9            [10]  278 	ret
                            279 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            280 ;	---------------------------------
                            281 ; Function collision_is_on_trap
                            282 ; ---------------------------------
   4E11                     283 _collision_is_on_trap::
                            284 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   4E11 21 07 00      [10]  285 	ld	hl, #7+0
   4E14 39            [11]  286 	add	hl, sp
   4E15 7E            [ 7]  287 	ld	a, (hl)
   4E16 F5            [11]  288 	push	af
   4E17 33            [ 6]  289 	inc	sp
   4E18 21 07 00      [10]  290 	ld	hl, #7+0
   4E1B 39            [11]  291 	add	hl, sp
   4E1C 7E            [ 7]  292 	ld	a, (hl)
   4E1D F5            [11]  293 	push	af
   4E1E 33            [ 6]  294 	inc	sp
   4E1F 21 06 00      [10]  295 	ld	hl, #6
   4E22 39            [11]  296 	add	hl, sp
   4E23 4E            [ 7]  297 	ld	c, (hl)
   4E24 23            [ 6]  298 	inc	hl
   4E25 46            [ 7]  299 	ld	b, (hl)
   4E26 C5            [11]  300 	push	bc
   4E27 21 06 00      [10]  301 	ld	hl, #6
   4E2A 39            [11]  302 	add	hl, sp
   4E2B 4E            [ 7]  303 	ld	c, (hl)
   4E2C 23            [ 6]  304 	inc	hl
   4E2D 46            [ 7]  305 	ld	b, (hl)
   4E2E C5            [11]  306 	push	bc
   4E2F CD 7B 53      [17]  307 	call	_tilemap_is_trap
   4E32 F1            [10]  308 	pop	af
   4E33 F1            [10]  309 	pop	af
   4E34 F1            [10]  310 	pop	af
   4E35 C9            [10]  311 	ret
                            312 ;src/systems/collision.c:58: u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
                            313 ;	---------------------------------
                            314 ; Function collision_is_on_ladder
                            315 ; ---------------------------------
   4E36                     316 _collision_is_on_ladder::
                            317 ;src/systems/collision.c:59: return tilemap_is_ladder(x, y, w, h);
   4E36 21 07 00      [10]  318 	ld	hl, #7+0
   4E39 39            [11]  319 	add	hl, sp
   4E3A 7E            [ 7]  320 	ld	a, (hl)
   4E3B F5            [11]  321 	push	af
   4E3C 33            [ 6]  322 	inc	sp
   4E3D 21 07 00      [10]  323 	ld	hl, #7+0
   4E40 39            [11]  324 	add	hl, sp
   4E41 7E            [ 7]  325 	ld	a, (hl)
   4E42 F5            [11]  326 	push	af
   4E43 33            [ 6]  327 	inc	sp
   4E44 21 06 00      [10]  328 	ld	hl, #6
   4E47 39            [11]  329 	add	hl, sp
   4E48 4E            [ 7]  330 	ld	c, (hl)
   4E49 23            [ 6]  331 	inc	hl
   4E4A 46            [ 7]  332 	ld	b, (hl)
   4E4B C5            [11]  333 	push	bc
   4E4C 21 06 00      [10]  334 	ld	hl, #6
   4E4F 39            [11]  335 	add	hl, sp
   4E50 4E            [ 7]  336 	ld	c, (hl)
   4E51 23            [ 6]  337 	inc	hl
   4E52 46            [ 7]  338 	ld	b, (hl)
   4E53 C5            [11]  339 	push	bc
   4E54 CD DF 53      [17]  340 	call	_tilemap_is_ladder
   4E57 F1            [10]  341 	pop	af
   4E58 F1            [10]  342 	pop	af
   4E59 F1            [10]  343 	pop	af
   4E5A C9            [10]  344 	ret
                            345 	.area _CODE
                            346 	.area _INITIALIZER
   648A                     347 __xinit__ggroundy:
   648A A0 00               348 	.dw #0x00a0
   648C                     349 __xinit__gplatformy:
   648C FF 00               350 	.dw #0x00ff
                            351 	.area _CABS (ABS)
