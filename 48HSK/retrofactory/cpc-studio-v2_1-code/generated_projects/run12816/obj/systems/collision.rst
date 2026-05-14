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
                             11 	.globl _tilemap_is_trap
                             12 	.globl _tilemap_platform_y_at
                             13 	.globl _tilemap_ground_y
                             14 	.globl _collision_init
                             15 	.globl _collision_is_on_ground
                             16 	.globl _collision_is_on_ground_at
                             17 	.globl _collision_clamp_y_to_ground
                             18 	.globl _collision_clamp_y_at
                             19 	.globl _collision_is_on_trap
                             20 ;--------------------------------------------------------
                             21 ; special function registers
                             22 ;--------------------------------------------------------
                             23 ;--------------------------------------------------------
                             24 ; ram data
                             25 ;--------------------------------------------------------
                             26 	.area _DATA
                             27 ;--------------------------------------------------------
                             28 ; ram data
                             29 ;--------------------------------------------------------
                             30 	.area _INITIALIZED
   5A8A                      31 _ggroundy:
   5A8A                      32 	.ds 2
   5A8C                      33 _gplatformy:
   5A8C                      34 	.ds 2
                             35 ;--------------------------------------------------------
                             36 ; absolute external ram data
                             37 ;--------------------------------------------------------
                             38 	.area _DABS (ABS)
                             39 ;--------------------------------------------------------
                             40 ; global & static initialisations
                             41 ;--------------------------------------------------------
                             42 	.area _HOME
                             43 	.area _GSINIT
                             44 	.area _GSFINAL
                             45 	.area _GSINIT
                             46 ;--------------------------------------------------------
                             47 ; Home
                             48 ;--------------------------------------------------------
                             49 	.area _HOME
                             50 	.area _HOME
                             51 ;--------------------------------------------------------
                             52 ; code
                             53 ;--------------------------------------------------------
                             54 	.area _CODE
                             55 ;src/systems/collision.c:7: void collision_init(void) {
                             56 ;	---------------------------------
                             57 ; Function collision_init
                             58 ; ---------------------------------
   46A2                      59 _collision_init::
                             60 ;src/systems/collision.c:8: ggroundy = (i16)tilemap_ground_y();
   46A2 CD CB 4B      [17]   61 	call	_tilemap_ground_y
   46A5 FD 21 8A 5A   [14]   62 	ld	iy, #_ggroundy
   46A9 FD 75 00      [19]   63 	ld	0 (iy), l
   46AC FD 36 01 00   [19]   64 	ld	1 (iy), #0x00
                             65 ;src/systems/collision.c:9: gplatformy = (i16)tilemap_platform_y_at(32);
   46B0 21 20 00      [10]   66 	ld	hl, #0x0020
   46B3 E5            [11]   67 	push	hl
   46B4 CD D3 4B      [17]   68 	call	_tilemap_platform_y_at
   46B7 F1            [10]   69 	pop	af
   46B8 FD 21 8C 5A   [14]   70 	ld	iy, #_gplatformy
   46BC FD 75 00      [19]   71 	ld	0 (iy), l
   46BF FD 36 01 00   [19]   72 	ld	1 (iy), #0x00
   46C3 C9            [10]   73 	ret
                             74 ;src/systems/collision.c:12: u8 collision_is_on_ground(i16 y, u8 h) {
                             75 ;	---------------------------------
                             76 ; Function collision_is_on_ground
                             77 ; ---------------------------------
   46C4                      78 _collision_is_on_ground::
                             79 ;src/systems/collision.c:13: return collision_is_on_ground_at(0, y, h);
   46C4 21 04 00      [10]   80 	ld	hl, #4+0
   46C7 39            [11]   81 	add	hl, sp
   46C8 7E            [ 7]   82 	ld	a, (hl)
   46C9 F5            [11]   83 	push	af
   46CA 33            [ 6]   84 	inc	sp
   46CB 21 03 00      [10]   85 	ld	hl, #3
   46CE 39            [11]   86 	add	hl, sp
   46CF 4E            [ 7]   87 	ld	c, (hl)
   46D0 23            [ 6]   88 	inc	hl
   46D1 46            [ 7]   89 	ld	b, (hl)
   46D2 C5            [11]   90 	push	bc
   46D3 21 00 00      [10]   91 	ld	hl, #0x0000
   46D6 E5            [11]   92 	push	hl
   46D7 CD DE 46      [17]   93 	call	_collision_is_on_ground_at
   46DA F1            [10]   94 	pop	af
   46DB F1            [10]   95 	pop	af
   46DC 33            [ 6]   96 	inc	sp
   46DD C9            [10]   97 	ret
                             98 ;src/systems/collision.c:16: u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
                             99 ;	---------------------------------
                            100 ; Function collision_is_on_ground_at
                            101 ; ---------------------------------
   46DE                     102 _collision_is_on_ground_at::
   46DE DD E5         [15]  103 	push	ix
   46E0 DD 21 00 00   [14]  104 	ld	ix,#0
   46E4 DD 39         [15]  105 	add	ix,sp
                            106 ;src/systems/collision.c:20: support = (i16)tilemap_ground_y();
   46E6 CD CB 4B      [17]  107 	call	_tilemap_ground_y
   46E9 4D            [ 4]  108 	ld	c, l
   46EA 06 00         [ 7]  109 	ld	b, #0x00
                            110 ;src/systems/collision.c:21: gplatformy = (i16)tilemap_platform_y_at(x);
   46EC C5            [11]  111 	push	bc
   46ED DD 6E 04      [19]  112 	ld	l,4 (ix)
   46F0 DD 66 05      [19]  113 	ld	h,5 (ix)
   46F3 E5            [11]  114 	push	hl
   46F4 CD D3 4B      [17]  115 	call	_tilemap_platform_y_at
   46F7 F1            [10]  116 	pop	af
   46F8 C1            [10]  117 	pop	bc
   46F9 FD 21 8C 5A   [14]  118 	ld	iy, #_gplatformy
   46FD FD 75 00      [19]  119 	ld	0 (iy), l
   4700 FD 36 01 00   [19]  120 	ld	1 (iy), #0x00
                            121 ;src/systems/collision.c:22: if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
   4704 DD 5E 08      [19]  122 	ld	e, 8 (ix)
   4707 16 00         [ 7]  123 	ld	d, #0x00
   4709 DD 7E 06      [19]  124 	ld	a, 6 (ix)
   470C 83            [ 4]  125 	add	a, e
   470D 5F            [ 4]  126 	ld	e, a
   470E DD 7E 07      [19]  127 	ld	a, 7 (ix)
   4711 8A            [ 4]  128 	adc	a, d
   4712 57            [ 4]  129 	ld	d, a
   4713 FD 7E 00      [19]  130 	ld	a, 0 (iy)
   4716 3C            [ 4]  131 	inc	a
   4717 FD B6 01      [19]  132 	or	a, 1 (iy)
   471A 28 15         [12]  133 	jr	Z,00102$
   471C 2A 8C 5A      [16]  134 	ld	hl, (_gplatformy)
   471F 23            [ 6]  135 	inc	hl
   4720 23            [ 6]  136 	inc	hl
   4721 7D            [ 4]  137 	ld	a, l
   4722 93            [ 4]  138 	sub	a, e
   4723 7C            [ 4]  139 	ld	a, h
   4724 9A            [ 4]  140 	sbc	a, d
   4725 E2 2A 47      [10]  141 	jp	PO, 00115$
   4728 EE 80         [ 7]  142 	xor	a, #0x80
   472A                     143 00115$:
   472A FA 31 47      [10]  144 	jp	M, 00102$
                            145 ;src/systems/collision.c:23: support = gplatformy;
   472D ED 4B 8C 5A   [20]  146 	ld	bc, (_gplatformy)
   4731                     147 00102$:
                            148 ;src/systems/collision.c:26: feet = y + (i16)h;
                            149 ;src/systems/collision.c:27: return (u8)(feet >= support);
   4731 7B            [ 4]  150 	ld	a, e
   4732 91            [ 4]  151 	sub	a, c
   4733 7A            [ 4]  152 	ld	a, d
   4734 98            [ 4]  153 	sbc	a, b
   4735 E2 3A 47      [10]  154 	jp	PO, 00116$
   4738 EE 80         [ 7]  155 	xor	a, #0x80
   473A                     156 00116$:
   473A 07            [ 4]  157 	rlca
   473B E6 01         [ 7]  158 	and	a,#0x01
   473D EE 01         [ 7]  159 	xor	a, #0x01
   473F 6F            [ 4]  160 	ld	l, a
   4740 DD E1         [14]  161 	pop	ix
   4742 C9            [10]  162 	ret
                            163 ;src/systems/collision.c:30: i16 collision_clamp_y_to_ground(i16 y, u8 h) {
                            164 ;	---------------------------------
                            165 ; Function collision_clamp_y_to_ground
                            166 ; ---------------------------------
   4743                     167 _collision_clamp_y_to_ground::
                            168 ;src/systems/collision.c:31: return collision_clamp_y_at(0, y, h);
   4743 21 04 00      [10]  169 	ld	hl, #4+0
   4746 39            [11]  170 	add	hl, sp
   4747 7E            [ 7]  171 	ld	a, (hl)
   4748 F5            [11]  172 	push	af
   4749 33            [ 6]  173 	inc	sp
   474A 21 03 00      [10]  174 	ld	hl, #3
   474D 39            [11]  175 	add	hl, sp
   474E 4E            [ 7]  176 	ld	c, (hl)
   474F 23            [ 6]  177 	inc	hl
   4750 46            [ 7]  178 	ld	b, (hl)
   4751 C5            [11]  179 	push	bc
   4752 21 00 00      [10]  180 	ld	hl, #0x0000
   4755 E5            [11]  181 	push	hl
   4756 CD 5D 47      [17]  182 	call	_collision_clamp_y_at
   4759 F1            [10]  183 	pop	af
   475A F1            [10]  184 	pop	af
   475B 33            [ 6]  185 	inc	sp
   475C C9            [10]  186 	ret
                            187 ;src/systems/collision.c:34: i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
                            188 ;	---------------------------------
                            189 ; Function collision_clamp_y_at
                            190 ; ---------------------------------
   475D                     191 _collision_clamp_y_at::
   475D DD E5         [15]  192 	push	ix
   475F DD 21 00 00   [14]  193 	ld	ix,#0
   4763 DD 39         [15]  194 	add	ix,sp
   4765 3B            [ 6]  195 	dec	sp
                            196 ;src/systems/collision.c:38: ggroundy = (i16)tilemap_ground_y();
   4766 CD CB 4B      [17]  197 	call	_tilemap_ground_y
   4769 FD 21 8A 5A   [14]  198 	ld	iy, #_ggroundy
   476D FD 75 00      [19]  199 	ld	0 (iy), l
   4770 FD 36 01 00   [19]  200 	ld	1 (iy), #0x00
                            201 ;src/systems/collision.c:39: maxy = ggroundy - (i16)h;
   4774 DD 4E 08      [19]  202 	ld	c, 8 (ix)
   4777 06 00         [ 7]  203 	ld	b, #0x00
   4779 FD 7E 00      [19]  204 	ld	a, 0 (iy)
   477C 91            [ 4]  205 	sub	a, c
   477D 5F            [ 4]  206 	ld	e, a
   477E FD 7E 01      [19]  207 	ld	a, 1 (iy)
   4781 98            [ 4]  208 	sbc	a, b
   4782 57            [ 4]  209 	ld	d, a
                            210 ;src/systems/collision.c:40: gplatformy = (i16)tilemap_platform_y_at(x);
   4783 C5            [11]  211 	push	bc
   4784 D5            [11]  212 	push	de
   4785 DD 6E 04      [19]  213 	ld	l,4 (ix)
   4788 DD 66 05      [19]  214 	ld	h,5 (ix)
   478B E5            [11]  215 	push	hl
   478C CD D3 4B      [17]  216 	call	_tilemap_platform_y_at
   478F F1            [10]  217 	pop	af
   4790 D1            [10]  218 	pop	de
   4791 C1            [10]  219 	pop	bc
   4792 FD 21 8C 5A   [14]  220 	ld	iy, #_gplatformy
   4796 FD 75 00      [19]  221 	ld	0 (iy), l
   4799 FD 36 01 00   [19]  222 	ld	1 (iy), #0x00
                            223 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   479D 7B            [ 4]  224 	ld	a, e
   479E DD 96 06      [19]  225 	sub	a, 6 (ix)
   47A1 7A            [ 4]  226 	ld	a, d
   47A2 DD 9E 07      [19]  227 	sbc	a, 7 (ix)
   47A5 E2 AA 47      [10]  228 	jp	PO, 00126$
   47A8 EE 80         [ 7]  229 	xor	a, #0x80
   47AA                     230 00126$:
   47AA 07            [ 4]  231 	rlca
   47AB E6 01         [ 7]  232 	and	a,#0x01
   47AD DD 77 FF      [19]  233 	ld	-1 (ix), a
                            234 ;src/systems/collision.c:41: if (gplatformy != 255) {
   47B0 FD 21 8C 5A   [14]  235 	ld	iy, #_gplatformy
   47B4 FD 7E 00      [19]  236 	ld	a, 0 (iy)
   47B7 3C            [ 4]  237 	inc	a
   47B8 FD B6 01      [19]  238 	or	a, 1 (iy)
   47BB 28 24         [12]  239 	jr	Z,00105$
                            240 ;src/systems/collision.c:42: platformmaxy = gplatformy - (i16)h;
   47BD FD 7E 00      [19]  241 	ld	a, 0 (iy)
   47C0 91            [ 4]  242 	sub	a, c
   47C1 4F            [ 4]  243 	ld	c, a
   47C2 FD 7E 01      [19]  244 	ld	a, 1 (iy)
   47C5 98            [ 4]  245 	sbc	a, b
   47C6 47            [ 4]  246 	ld	b, a
                            247 ;src/systems/collision.c:43: if (y > platformmaxy && y <= maxy) {
   47C7 79            [ 4]  248 	ld	a, c
   47C8 DD 96 06      [19]  249 	sub	a, 6 (ix)
   47CB 78            [ 4]  250 	ld	a, b
   47CC DD 9E 07      [19]  251 	sbc	a, 7 (ix)
   47CF E2 D4 47      [10]  252 	jp	PO, 00128$
   47D2 EE 80         [ 7]  253 	xor	a, #0x80
   47D4                     254 00128$:
   47D4 F2 E1 47      [10]  255 	jp	P, 00105$
   47D7 DD CB FF 46   [20]  256 	bit	0, -1 (ix)
   47DB 20 04         [12]  257 	jr	NZ,00105$
                            258 ;src/systems/collision.c:44: return platformmaxy;
   47DD 69            [ 4]  259 	ld	l, c
   47DE 60            [ 4]  260 	ld	h, b
   47DF 18 0F         [12]  261 	jr	00108$
   47E1                     262 00105$:
                            263 ;src/systems/collision.c:48: if (y > maxy) {
   47E1 DD CB FF 46   [20]  264 	bit	0, -1 (ix)
   47E5 28 03         [12]  265 	jr	Z,00107$
                            266 ;src/systems/collision.c:49: return maxy;
   47E7 EB            [ 4]  267 	ex	de,hl
   47E8 18 06         [12]  268 	jr	00108$
   47EA                     269 00107$:
                            270 ;src/systems/collision.c:51: return y;
   47EA DD 6E 06      [19]  271 	ld	l,6 (ix)
   47ED DD 66 07      [19]  272 	ld	h,7 (ix)
   47F0                     273 00108$:
   47F0 33            [ 6]  274 	inc	sp
   47F1 DD E1         [14]  275 	pop	ix
   47F3 C9            [10]  276 	ret
                            277 ;src/systems/collision.c:54: u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
                            278 ;	---------------------------------
                            279 ; Function collision_is_on_trap
                            280 ; ---------------------------------
   47F4                     281 _collision_is_on_trap::
                            282 ;src/systems/collision.c:55: return tilemap_is_trap(x, y, w, h);
   47F4 21 07 00      [10]  283 	ld	hl, #7+0
   47F7 39            [11]  284 	add	hl, sp
   47F8 7E            [ 7]  285 	ld	a, (hl)
   47F9 F5            [11]  286 	push	af
   47FA 33            [ 6]  287 	inc	sp
   47FB 21 07 00      [10]  288 	ld	hl, #7+0
   47FE 39            [11]  289 	add	hl, sp
   47FF 7E            [ 7]  290 	ld	a, (hl)
   4800 F5            [11]  291 	push	af
   4801 33            [ 6]  292 	inc	sp
   4802 21 06 00      [10]  293 	ld	hl, #6
   4805 39            [11]  294 	add	hl, sp
   4806 4E            [ 7]  295 	ld	c, (hl)
   4807 23            [ 6]  296 	inc	hl
   4808 46            [ 7]  297 	ld	b, (hl)
   4809 C5            [11]  298 	push	bc
   480A 21 06 00      [10]  299 	ld	hl, #6
   480D 39            [11]  300 	add	hl, sp
   480E 4E            [ 7]  301 	ld	c, (hl)
   480F 23            [ 6]  302 	inc	hl
   4810 46            [ 7]  303 	ld	b, (hl)
   4811 C5            [11]  304 	push	bc
   4812 CD 05 4C      [17]  305 	call	_tilemap_is_trap
   4815 F1            [10]  306 	pop	af
   4816 F1            [10]  307 	pop	af
   4817 F1            [10]  308 	pop	af
   4818 C9            [10]  309 	ret
                            310 	.area _CODE
                            311 	.area _INITIALIZER
   5AA5                     312 __xinit__ggroundy:
   5AA5 A0 00               313 	.dw #0x00a0
   5AA7                     314 __xinit__gplatformy:
   5AA7 FF 00               315 	.dw #0x00ff
                            316 	.area _CABS (ABS)
