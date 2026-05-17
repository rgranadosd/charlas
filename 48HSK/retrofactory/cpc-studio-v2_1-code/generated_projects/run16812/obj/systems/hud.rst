                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module hud
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSolidBox
                             13 	.globl _cpct_drawSprite
                             14 	.globl _cpct_px2byteM0
                             15 	.globl _hudinit
                             16 	.globl _hudupdate
                             17 	.globl _hudrender
                             18 ;--------------------------------------------------------
                             19 ; special function registers
                             20 ;--------------------------------------------------------
                             21 ;--------------------------------------------------------
                             22 ; ram data
                             23 ;--------------------------------------------------------
                             24 	.area _DATA
   5F90                      25 _currenthealth:
   5F90                      26 	.ds 1
   5F91                      27 _currentscore:
   5F91                      28 	.ds 2
   5F93                      29 _currenttime:
   5F93                      30 	.ds 1
   5F94                      31 _currentlives:
   5F94                      32 	.ds 1
   5F95                      33 _currentweapon:
   5F95                      34 	.ds 1
                             35 ;--------------------------------------------------------
                             36 ; ram data
                             37 ;--------------------------------------------------------
                             38 	.area _INITIALIZED
                             39 ;--------------------------------------------------------
                             40 ; absolute external ram data
                             41 ;--------------------------------------------------------
                             42 	.area _DABS (ABS)
                             43 ;--------------------------------------------------------
                             44 ; global & static initialisations
                             45 ;--------------------------------------------------------
                             46 	.area _HOME
                             47 	.area _GSINIT
                             48 	.area _GSFINAL
                             49 	.area _GSINIT
                             50 ;--------------------------------------------------------
                             51 ; Home
                             52 ;--------------------------------------------------------
                             53 	.area _HOME
                             54 	.area _HOME
                             55 ;--------------------------------------------------------
                             56 ; code
                             57 ;--------------------------------------------------------
                             58 	.area _CODE
                             59 ;src/systems/hud.c:16: static const u8* hud_get_number_sprite(u8 digit) {
                             60 ;	---------------------------------
                             61 ; Function hud_get_number_sprite
                             62 ; ---------------------------------
   4D0E                      63 _hud_get_number_sprite:
                             64 ;src/systems/hud.c:18: return _hud_dummy_sprite;
   4D0E 21 12 4D      [10]   65 	ld	hl, #__hud_dummy_sprite
   4D11 C9            [10]   66 	ret
   4D12                      67 __hud_dummy_sprite:
   4D12 00                   68 	.db #0x00	; 0
   4D13 00                   69 	.db 0x00
   4D14 00                   70 	.db 0x00
   4D15 00                   71 	.db 0x00
   4D16 00                   72 	.db 0x00
   4D17 00                   73 	.db 0x00
   4D18 00                   74 	.db 0x00
   4D19 00                   75 	.db 0x00
   4D1A 00                   76 	.db 0x00
   4D1B 00                   77 	.db 0x00
   4D1C 00                   78 	.db 0x00
   4D1D 00                   79 	.db 0x00
   4D1E 00                   80 	.db 0x00
   4D1F 00                   81 	.db 0x00
   4D20 00                   82 	.db 0x00
   4D21 00                   83 	.db 0x00
   4D22 00                   84 	.db 0x00
   4D23 00                   85 	.db 0x00
   4D24 00                   86 	.db 0x00
   4D25 00                   87 	.db 0x00
   4D26 00                   88 	.db 0x00
   4D27 00                   89 	.db 0x00
   4D28 00                   90 	.db 0x00
   4D29 00                   91 	.db 0x00
   4D2A 00                   92 	.db 0x00
   4D2B 00                   93 	.db 0x00
   4D2C 00                   94 	.db 0x00
   4D2D 00                   95 	.db 0x00
   4D2E 00                   96 	.db 0x00
   4D2F 00                   97 	.db 0x00
   4D30 00                   98 	.db 0x00
   4D31 00                   99 	.db 0x00
   4D32 00                  100 	.db 0x00
   4D33 00                  101 	.db 0x00
   4D34 00                  102 	.db 0x00
   4D35 00                  103 	.db 0x00
   4D36 00                  104 	.db 0x00
   4D37 00                  105 	.db 0x00
   4D38 00                  106 	.db 0x00
   4D39 00                  107 	.db 0x00
   4D3A 00                  108 	.db 0x00
   4D3B 00                  109 	.db 0x00
   4D3C 00                  110 	.db 0x00
   4D3D 00                  111 	.db 0x00
   4D3E 00                  112 	.db 0x00
   4D3F 00                  113 	.db 0x00
   4D40 00                  114 	.db 0x00
   4D41 00                  115 	.db 0x00
   4D42 00                  116 	.db 0x00
   4D43 00                  117 	.db 0x00
   4D44 00                  118 	.db 0x00
   4D45 00                  119 	.db 0x00
   4D46 00                  120 	.db 0x00
   4D47 00                  121 	.db 0x00
   4D48 00                  122 	.db 0x00
   4D49 00                  123 	.db 0x00
   4D4A 00                  124 	.db 0x00
   4D4B 00                  125 	.db 0x00
   4D4C 00                  126 	.db 0x00
   4D4D 00                  127 	.db 0x00
   4D4E 00                  128 	.db 0x00
   4D4F 00                  129 	.db 0x00
   4D50 00                  130 	.db 0x00
   4D51 00                  131 	.db 0x00
   4D52                     132 _hudhealth:
   4D52 00                  133 	.db #0x00	; 0
   4D53 00                  134 	.db 0x00
   4D54 00                  135 	.db 0x00
   4D55 00                  136 	.db 0x00
   4D56 00                  137 	.db 0x00
   4D57 00                  138 	.db 0x00
   4D58 00                  139 	.db 0x00
   4D59 00                  140 	.db 0x00
   4D5A 00                  141 	.db 0x00
   4D5B 00                  142 	.db 0x00
   4D5C 00                  143 	.db 0x00
   4D5D 00                  144 	.db 0x00
   4D5E 00                  145 	.db 0x00
   4D5F 00                  146 	.db 0x00
   4D60 00                  147 	.db 0x00
   4D61 00                  148 	.db 0x00
   4D62 00                  149 	.db 0x00
   4D63 00                  150 	.db 0x00
   4D64 00                  151 	.db 0x00
   4D65 00                  152 	.db 0x00
   4D66 00                  153 	.db 0x00
   4D67 00                  154 	.db 0x00
   4D68 00                  155 	.db 0x00
   4D69 00                  156 	.db 0x00
   4D6A 00                  157 	.db 0x00
   4D6B 00                  158 	.db 0x00
   4D6C 00                  159 	.db 0x00
   4D6D 00                  160 	.db 0x00
   4D6E 00                  161 	.db 0x00
   4D6F 00                  162 	.db 0x00
   4D70 00                  163 	.db 0x00
   4D71 00                  164 	.db 0x00
   4D72 00                  165 	.db 0x00
   4D73 00                  166 	.db 0x00
   4D74 00                  167 	.db 0x00
   4D75 00                  168 	.db 0x00
   4D76 00                  169 	.db 0x00
   4D77 00                  170 	.db 0x00
   4D78 00                  171 	.db 0x00
   4D79 00                  172 	.db 0x00
   4D7A 00                  173 	.db 0x00
   4D7B 00                  174 	.db 0x00
   4D7C 00                  175 	.db 0x00
   4D7D 00                  176 	.db 0x00
   4D7E 00                  177 	.db 0x00
   4D7F 00                  178 	.db 0x00
   4D80 00                  179 	.db 0x00
   4D81 00                  180 	.db 0x00
   4D82 00                  181 	.db 0x00
   4D83 00                  182 	.db 0x00
   4D84 00                  183 	.db 0x00
   4D85 00                  184 	.db 0x00
   4D86 00                  185 	.db 0x00
   4D87 00                  186 	.db 0x00
   4D88 00                  187 	.db 0x00
   4D89 00                  188 	.db 0x00
   4D8A 00                  189 	.db 0x00
   4D8B 00                  190 	.db 0x00
   4D8C 00                  191 	.db 0x00
   4D8D 00                  192 	.db 0x00
   4D8E 00                  193 	.db 0x00
   4D8F 00                  194 	.db 0x00
   4D90 00                  195 	.db 0x00
   4D91 00                  196 	.db 0x00
   4D92                     197 _hudlives:
   4D92 00                  198 	.db #0x00	; 0
   4D93 00                  199 	.db 0x00
   4D94 00                  200 	.db 0x00
   4D95 00                  201 	.db 0x00
   4D96 00                  202 	.db 0x00
   4D97 00                  203 	.db 0x00
   4D98 00                  204 	.db 0x00
   4D99 00                  205 	.db 0x00
   4D9A 00                  206 	.db 0x00
   4D9B 00                  207 	.db 0x00
   4D9C 00                  208 	.db 0x00
   4D9D 00                  209 	.db 0x00
   4D9E 00                  210 	.db 0x00
   4D9F 00                  211 	.db 0x00
   4DA0 00                  212 	.db 0x00
   4DA1 00                  213 	.db 0x00
   4DA2 00                  214 	.db 0x00
   4DA3 00                  215 	.db 0x00
   4DA4 00                  216 	.db 0x00
   4DA5 00                  217 	.db 0x00
   4DA6 00                  218 	.db 0x00
   4DA7 00                  219 	.db 0x00
   4DA8 00                  220 	.db 0x00
   4DA9 00                  221 	.db 0x00
   4DAA 00                  222 	.db 0x00
   4DAB 00                  223 	.db 0x00
   4DAC 00                  224 	.db 0x00
   4DAD 00                  225 	.db 0x00
   4DAE 00                  226 	.db 0x00
   4DAF 00                  227 	.db 0x00
   4DB0 00                  228 	.db 0x00
   4DB1 00                  229 	.db 0x00
   4DB2 00                  230 	.db 0x00
   4DB3 00                  231 	.db 0x00
   4DB4 00                  232 	.db 0x00
   4DB5 00                  233 	.db 0x00
   4DB6 00                  234 	.db 0x00
   4DB7 00                  235 	.db 0x00
   4DB8 00                  236 	.db 0x00
   4DB9 00                  237 	.db 0x00
   4DBA 00                  238 	.db 0x00
   4DBB 00                  239 	.db 0x00
   4DBC 00                  240 	.db 0x00
   4DBD 00                  241 	.db 0x00
   4DBE 00                  242 	.db 0x00
   4DBF 00                  243 	.db 0x00
   4DC0 00                  244 	.db 0x00
   4DC1 00                  245 	.db 0x00
   4DC2 00                  246 	.db 0x00
   4DC3 00                  247 	.db 0x00
   4DC4 00                  248 	.db 0x00
   4DC5 00                  249 	.db 0x00
   4DC6 00                  250 	.db 0x00
   4DC7 00                  251 	.db 0x00
   4DC8 00                  252 	.db 0x00
   4DC9 00                  253 	.db 0x00
   4DCA 00                  254 	.db 0x00
   4DCB 00                  255 	.db 0x00
   4DCC 00                  256 	.db 0x00
   4DCD 00                  257 	.db 0x00
   4DCE 00                  258 	.db 0x00
   4DCF 00                  259 	.db 0x00
   4DD0 00                  260 	.db 0x00
   4DD1 00                  261 	.db 0x00
                            262 ;src/systems/hud.c:21: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            263 ;	---------------------------------
                            264 ; Function hud_draw_digits
                            265 ; ---------------------------------
   4DD2                     266 _hud_draw_digits:
   4DD2 DD E5         [15]  267 	push	ix
   4DD4 DD 21 00 00   [14]  268 	ld	ix,#0
   4DD8 DD 39         [15]  269 	add	ix,sp
   4DDA 3B            [ 6]  270 	dec	sp
                            271 ;src/systems/hud.c:27: divisor = 1;
   4DDB 01 01 00      [10]  272 	ld	bc, #0x0001
                            273 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4DDE 1E 01         [ 7]  274 	ld	e, #0x01
   4DE0                     275 00106$:
   4DE0 7B            [ 4]  276 	ld	a, e
   4DE1 DD 96 06      [19]  277 	sub	a, 6 (ix)
   4DE4 30 0B         [12]  278 	jr	NC,00101$
                            279 ;src/systems/hud.c:29: divisor *= 10;
   4DE6 69            [ 4]  280 	ld	l, c
   4DE7 60            [ 4]  281 	ld	h, b
   4DE8 29            [11]  282 	add	hl, hl
   4DE9 29            [11]  283 	add	hl, hl
   4DEA 09            [11]  284 	add	hl, bc
   4DEB 29            [11]  285 	add	hl, hl
   4DEC 4D            [ 4]  286 	ld	c, l
   4DED 44            [ 4]  287 	ld	b, h
                            288 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4DEE 1C            [ 4]  289 	inc	e
   4DEF 18 EF         [12]  290 	jr	00106$
   4DF1                     291 00101$:
                            292 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4DF1 DD 36 FF 00   [19]  293 	ld	-1 (ix), #0x00
   4DF5                     294 00109$:
   4DF5 DD 7E FF      [19]  295 	ld	a, -1 (ix)
   4DF8 DD 96 06      [19]  296 	sub	a, 6 (ix)
   4DFB D2 7A 4E      [10]  297 	jp	NC, 00111$
                            298 ;src/systems/hud.c:33: digit = (u8)(value / divisor);
   4DFE C5            [11]  299 	push	bc
   4DFF C5            [11]  300 	push	bc
   4E00 DD 6E 04      [19]  301 	ld	l,4 (ix)
   4E03 DD 66 05      [19]  302 	ld	h,5 (ix)
   4E06 E5            [11]  303 	push	hl
   4E07 CD 17 5C      [17]  304 	call	__divuint
   4E0A F1            [10]  305 	pop	af
   4E0B F1            [10]  306 	pop	af
   4E0C 5D            [ 4]  307 	ld	e, l
   4E0D C1            [10]  308 	pop	bc
                            309 ;src/systems/hud.c:34: value = (u16)(value % divisor);
   4E0E C5            [11]  310 	push	bc
   4E0F D5            [11]  311 	push	de
   4E10 C5            [11]  312 	push	bc
   4E11 DD 6E 04      [19]  313 	ld	l,4 (ix)
   4E14 DD 66 05      [19]  314 	ld	h,5 (ix)
   4E17 E5            [11]  315 	push	hl
   4E18 CD D5 5E      [17]  316 	call	__moduint
   4E1B F1            [10]  317 	pop	af
   4E1C F1            [10]  318 	pop	af
   4E1D D1            [10]  319 	pop	de
   4E1E C1            [10]  320 	pop	bc
   4E1F DD 75 04      [19]  321 	ld	4 (ix), l
   4E22 DD 74 05      [19]  322 	ld	5 (ix), h
                            323 ;src/systems/hud.c:36: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4E25 DD 7E FF      [19]  324 	ld	a, -1 (ix)
   4E28 07            [ 4]  325 	rlca
   4E29 07            [ 4]  326 	rlca
   4E2A 07            [ 4]  327 	rlca
   4E2B E6 F8         [ 7]  328 	and	a, #0xf8
   4E2D 57            [ 4]  329 	ld	d, a
   4E2E DD 7E 07      [19]  330 	ld	a, 7 (ix)
   4E31 82            [ 4]  331 	add	a, d
   4E32 57            [ 4]  332 	ld	d, a
   4E33 C5            [11]  333 	push	bc
   4E34 D5            [11]  334 	push	de
   4E35 DD 7E 08      [19]  335 	ld	a, 8 (ix)
   4E38 F5            [11]  336 	push	af
   4E39 33            [ 6]  337 	inc	sp
   4E3A D5            [11]  338 	push	de
   4E3B 33            [ 6]  339 	inc	sp
   4E3C 21 00 C0      [10]  340 	ld	hl, #0xc000
   4E3F E5            [11]  341 	push	hl
   4E40 CD A9 5E      [17]  342 	call	_cpct_getScreenPtr
   4E43 D1            [10]  343 	pop	de
   4E44 C1            [10]  344 	pop	bc
                            345 ;src/systems/hud.c:37: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
   4E45 E5            [11]  346 	push	hl
   4E46 C5            [11]  347 	push	bc
   4E47 7B            [ 4]  348 	ld	a, e
   4E48 F5            [11]  349 	push	af
   4E49 33            [ 6]  350 	inc	sp
   4E4A CD 0E 4D      [17]  351 	call	_hud_get_number_sprite
   4E4D 33            [ 6]  352 	inc	sp
   4E4E EB            [ 4]  353 	ex	de,hl
   4E4F C1            [10]  354 	pop	bc
   4E50 E1            [10]  355 	pop	hl
   4E51 D5            [11]  356 	push	de
   4E52 FD E1         [14]  357 	pop	iy
   4E54 C5            [11]  358 	push	bc
   4E55 11 08 08      [10]  359 	ld	de, #0x0808
   4E58 D5            [11]  360 	push	de
   4E59 E5            [11]  361 	push	hl
   4E5A FD E5         [15]  362 	push	iy
   4E5C CD F1 5C      [17]  363 	call	_cpct_drawSprite
   4E5F C1            [10]  364 	pop	bc
                            365 ;src/systems/hud.c:39: if (divisor > 1) {
   4E60 3E 01         [ 7]  366 	ld	a, #0x01
   4E62 B9            [ 4]  367 	cp	a, c
   4E63 3E 00         [ 7]  368 	ld	a, #0x00
   4E65 98            [ 4]  369 	sbc	a, b
   4E66 30 0C         [12]  370 	jr	NC,00110$
                            371 ;src/systems/hud.c:40: divisor /= 10;
   4E68 21 0A 00      [10]  372 	ld	hl, #0x000a
   4E6B E5            [11]  373 	push	hl
   4E6C C5            [11]  374 	push	bc
   4E6D CD 17 5C      [17]  375 	call	__divuint
   4E70 F1            [10]  376 	pop	af
   4E71 F1            [10]  377 	pop	af
   4E72 4D            [ 4]  378 	ld	c, l
   4E73 44            [ 4]  379 	ld	b, h
   4E74                     380 00110$:
                            381 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4E74 DD 34 FF      [23]  382 	inc	-1 (ix)
   4E77 C3 F5 4D      [10]  383 	jp	00109$
   4E7A                     384 00111$:
   4E7A 33            [ 6]  385 	inc	sp
   4E7B DD E1         [14]  386 	pop	ix
   4E7D C9            [10]  387 	ret
                            388 ;src/systems/hud.c:45: void hudinit(void) {
                            389 ;	---------------------------------
                            390 ; Function hudinit
                            391 ; ---------------------------------
   4E7E                     392 _hudinit::
                            393 ;src/systems/hud.c:46: currenthealth = 3;
   4E7E 21 90 5F      [10]  394 	ld	hl,#_currenthealth + 0
   4E81 36 03         [10]  395 	ld	(hl), #0x03
                            396 ;src/systems/hud.c:47: currentscore  = 0;
   4E83 21 00 00      [10]  397 	ld	hl, #0x0000
   4E86 22 91 5F      [16]  398 	ld	(_currentscore), hl
                            399 ;src/systems/hud.c:48: currenttime   = 90;
   4E89 21 93 5F      [10]  400 	ld	hl,#_currenttime + 0
   4E8C 36 5A         [10]  401 	ld	(hl), #0x5a
                            402 ;src/systems/hud.c:49: currentlives  = 3;
   4E8E 21 94 5F      [10]  403 	ld	hl,#_currentlives + 0
   4E91 36 03         [10]  404 	ld	(hl), #0x03
                            405 ;src/systems/hud.c:50: currentweapon = 0;
   4E93 21 95 5F      [10]  406 	ld	hl,#_currentweapon + 0
   4E96 36 00         [10]  407 	ld	(hl), #0x00
   4E98 C9            [10]  408 	ret
                            409 ;src/systems/hud.c:53: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            410 ;	---------------------------------
                            411 ; Function hudupdate
                            412 ; ---------------------------------
   4E99                     413 _hudupdate::
                            414 ;src/systems/hud.c:54: currenthealth = lives;
   4E99 21 02 00      [10]  415 	ld	hl, #2+0
   4E9C 39            [11]  416 	add	hl, sp
   4E9D 7E            [ 7]  417 	ld	a, (hl)
   4E9E 32 90 5F      [13]  418 	ld	(#_currenthealth + 0),a
                            419 ;src/systems/hud.c:55: currentscore  = score;
   4EA1 21 03 00      [10]  420 	ld	hl, #3+0
   4EA4 39            [11]  421 	add	hl, sp
   4EA5 7E            [ 7]  422 	ld	a, (hl)
   4EA6 32 91 5F      [13]  423 	ld	(#_currentscore + 0),a
   4EA9 21 04 00      [10]  424 	ld	hl, #3+1
   4EAC 39            [11]  425 	add	hl, sp
   4EAD 7E            [ 7]  426 	ld	a, (hl)
   4EAE 32 92 5F      [13]  427 	ld	(#_currentscore + 1),a
                            428 ;src/systems/hud.c:56: currenttime   = time;
   4EB1 21 05 00      [10]  429 	ld	hl, #5+0
   4EB4 39            [11]  430 	add	hl, sp
   4EB5 7E            [ 7]  431 	ld	a, (hl)
   4EB6 32 93 5F      [13]  432 	ld	(#_currenttime + 0),a
                            433 ;src/systems/hud.c:57: currentlives  = lives;
   4EB9 21 02 00      [10]  434 	ld	hl, #2+0
   4EBC 39            [11]  435 	add	hl, sp
   4EBD 7E            [ 7]  436 	ld	a, (hl)
   4EBE 32 94 5F      [13]  437 	ld	(#_currentlives + 0),a
                            438 ;src/systems/hud.c:58: currentweapon = weapon;
   4EC1 21 06 00      [10]  439 	ld	hl, #6+0
   4EC4 39            [11]  440 	add	hl, sp
   4EC5 7E            [ 7]  441 	ld	a, (hl)
   4EC6 32 95 5F      [13]  442 	ld	(#_currentweapon + 0),a
   4EC9 C9            [10]  443 	ret
                            444 ;src/systems/hud.c:61: void hudrender(void) {
                            445 ;	---------------------------------
                            446 ; Function hudrender
                            447 ; ---------------------------------
   4ECA                     448 _hudrender::
   4ECA DD E5         [15]  449 	push	ix
   4ECC DD 21 00 00   [14]  450 	ld	ix,#0
   4ED0 DD 39         [15]  451 	add	ix,sp
   4ED2 3B            [ 6]  452 	dec	sp
                            453 ;src/systems/hud.c:68: for (i = 0; i < currenthealth && i < 5; ++i) {
   4ED3 0E 00         [ 7]  454 	ld	c, #0x00
   4ED5                     455 00115$:
   4ED5 21 90 5F      [10]  456 	ld	hl, #_currenthealth
   4ED8 79            [ 4]  457 	ld	a,c
   4ED9 BE            [ 7]  458 	cp	a,(hl)
   4EDA 30 37         [12]  459 	jr	NC,00101$
                            460 ;src/systems/hud.c:69: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (u8)(i * 3), 2);
   4EDC FE 05         [ 7]  461 	cp	a,#0x05
   4EDE 30 33         [12]  462 	jr	NC,00101$
   4EE0 87            [ 4]  463 	add	a, a
   4EE1 81            [ 4]  464 	add	a, c
   4EE2 47            [ 4]  465 	ld	b, a
   4EE3 C5            [11]  466 	push	bc
   4EE4 3E 02         [ 7]  467 	ld	a, #0x02
   4EE6 F5            [11]  468 	push	af
   4EE7 33            [ 6]  469 	inc	sp
   4EE8 C5            [11]  470 	push	bc
   4EE9 33            [ 6]  471 	inc	sp
   4EEA 21 00 C0      [10]  472 	ld	hl, #0xc000
   4EED E5            [11]  473 	push	hl
   4EEE CD A9 5E      [17]  474 	call	_cpct_getScreenPtr
   4EF1 C1            [10]  475 	pop	bc
                            476 ;src/systems/hud.c:70: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), 2, 4);
   4EF2 E5            [11]  477 	push	hl
   4EF3 C5            [11]  478 	push	bc
   4EF4 11 06 06      [10]  479 	ld	de, #0x0606
   4EF7 D5            [11]  480 	push	de
   4EF8 CD B6 5D      [17]  481 	call	_cpct_px2byteM0
   4EFB 55            [ 4]  482 	ld	d, l
   4EFC C1            [10]  483 	pop	bc
   4EFD E1            [10]  484 	pop	hl
   4EFE 5D            [ 4]  485 	ld	e, l
   4EFF 44            [ 4]  486 	ld	b, h
   4F00 C5            [11]  487 	push	bc
   4F01 21 02 04      [10]  488 	ld	hl, #0x0402
   4F04 E5            [11]  489 	push	hl
   4F05 D5            [11]  490 	push	de
   4F06 33            [ 6]  491 	inc	sp
   4F07 4B            [ 4]  492 	ld	c,e
   4F08 C5            [11]  493 	push	bc
   4F09 CD F0 5D      [17]  494 	call	_cpct_drawSolidBox
   4F0C F1            [10]  495 	pop	af
   4F0D F1            [10]  496 	pop	af
   4F0E 33            [ 6]  497 	inc	sp
   4F0F C1            [10]  498 	pop	bc
                            499 ;src/systems/hud.c:68: for (i = 0; i < currenthealth && i < 5; ++i) {
   4F10 0C            [ 4]  500 	inc	c
   4F11 18 C2         [12]  501 	jr	00115$
   4F13                     502 00101$:
                            503 ;src/systems/hud.c:73: scorebar = (u8)(currentscore / 100);
   4F13 21 64 00      [10]  504 	ld	hl, #0x0064
   4F16 E5            [11]  505 	push	hl
   4F17 2A 91 5F      [16]  506 	ld	hl, (_currentscore)
   4F1A E5            [11]  507 	push	hl
   4F1B CD 17 5C      [17]  508 	call	__divuint
   4F1E F1            [10]  509 	pop	af
   4F1F F1            [10]  510 	pop	af
   4F20 4D            [ 4]  511 	ld	c, l
                            512 ;src/systems/hud.c:74: if (scorebar > 20) {
   4F21 3E 14         [ 7]  513 	ld	a, #0x14
   4F23 91            [ 4]  514 	sub	a, c
   4F24 30 02         [12]  515 	jr	NC,00103$
                            516 ;src/systems/hud.c:75: scorebar = 20;
   4F26 0E 14         [ 7]  517 	ld	c, #0x14
   4F28                     518 00103$:
                            519 ;src/systems/hud.c:77: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, 2);
   4F28 C5            [11]  520 	push	bc
   4F29 21 18 02      [10]  521 	ld	hl, #0x0218
   4F2C E5            [11]  522 	push	hl
   4F2D 21 00 C0      [10]  523 	ld	hl, #0xc000
   4F30 E5            [11]  524 	push	hl
   4F31 CD A9 5E      [17]  525 	call	_cpct_getScreenPtr
   4F34 E5            [11]  526 	push	hl
   4F35 21 01 01      [10]  527 	ld	hl, #0x0101
   4F38 E5            [11]  528 	push	hl
   4F39 CD B6 5D      [17]  529 	call	_cpct_px2byteM0
   4F3C 45            [ 4]  530 	ld	b, l
   4F3D D1            [10]  531 	pop	de
   4F3E 78            [ 4]  532 	ld	a, b
   4F3F C1            [10]  533 	pop	bc
   4F40 47            [ 4]  534 	ld	b, a
                            535 ;src/systems/hud.c:70: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), 2, 4);
                            536 ;src/systems/hud.c:78: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 20, 2);
   4F41 C5            [11]  537 	push	bc
   4F42 D5            [11]  538 	push	de
   4F43 21 14 02      [10]  539 	ld	hl, #0x0214
   4F46 E5            [11]  540 	push	hl
   4F47 C5            [11]  541 	push	bc
   4F48 33            [ 6]  542 	inc	sp
   4F49 D5            [11]  543 	push	de
   4F4A CD F0 5D      [17]  544 	call	_cpct_drawSolidBox
   4F4D F1            [10]  545 	pop	af
   4F4E F1            [10]  546 	pop	af
   4F4F 33            [ 6]  547 	inc	sp
   4F50 D1            [10]  548 	pop	de
   4F51 C1            [10]  549 	pop	bc
                            550 ;src/systems/hud.c:79: if (scorebar) {
   4F52 79            [ 4]  551 	ld	a, c
   4F53 B7            [ 4]  552 	or	a, a
   4F54 28 18         [12]  553 	jr	Z,00105$
                            554 ;src/systems/hud.c:80: cpct_drawSolidBox(pvmem, cpct_px2byteM0(14, 14), scorebar, 2);
   4F56 C5            [11]  555 	push	bc
   4F57 D5            [11]  556 	push	de
   4F58 21 0E 0E      [10]  557 	ld	hl, #0x0e0e
   4F5B E5            [11]  558 	push	hl
   4F5C CD B6 5D      [17]  559 	call	_cpct_px2byteM0
   4F5F 65            [ 4]  560 	ld	h, l
   4F60 D1            [10]  561 	pop	de
   4F61 C1            [10]  562 	pop	bc
   4F62 06 02         [ 7]  563 	ld	b, #0x02
   4F64 C5            [11]  564 	push	bc
   4F65 E5            [11]  565 	push	hl
   4F66 33            [ 6]  566 	inc	sp
   4F67 D5            [11]  567 	push	de
   4F68 CD F0 5D      [17]  568 	call	_cpct_drawSolidBox
   4F6B F1            [10]  569 	pop	af
   4F6C F1            [10]  570 	pop	af
   4F6D 33            [ 6]  571 	inc	sp
   4F6E                     572 00105$:
                            573 ;src/systems/hud.c:83: timebar = (u8)(currenttime / 5);
   4F6E 3E 05         [ 7]  574 	ld	a, #0x05
   4F70 F5            [11]  575 	push	af
   4F71 33            [ 6]  576 	inc	sp
   4F72 3A 93 5F      [13]  577 	ld	a, (_currenttime)
   4F75 F5            [11]  578 	push	af
   4F76 33            [ 6]  579 	inc	sp
   4F77 CD 1F 5C      [17]  580 	call	__divuchar
   4F7A F1            [10]  581 	pop	af
   4F7B 4D            [ 4]  582 	ld	c, l
                            583 ;src/systems/hud.c:84: if (timebar > 19) {
   4F7C 3E 13         [ 7]  584 	ld	a, #0x13
   4F7E 91            [ 4]  585 	sub	a, c
   4F7F 30 02         [12]  586 	jr	NC,00107$
                            587 ;src/systems/hud.c:85: timebar = 19;
   4F81 0E 13         [ 7]  588 	ld	c, #0x13
   4F83                     589 00107$:
                            590 ;src/systems/hud.c:87: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, 2);
   4F83 C5            [11]  591 	push	bc
   4F84 21 38 02      [10]  592 	ld	hl, #0x0238
   4F87 E5            [11]  593 	push	hl
   4F88 21 00 C0      [10]  594 	ld	hl, #0xc000
   4F8B E5            [11]  595 	push	hl
   4F8C CD A9 5E      [17]  596 	call	_cpct_getScreenPtr
   4F8F E5            [11]  597 	push	hl
   4F90 21 01 01      [10]  598 	ld	hl, #0x0101
   4F93 E5            [11]  599 	push	hl
   4F94 CD B6 5D      [17]  600 	call	_cpct_px2byteM0
   4F97 45            [ 4]  601 	ld	b, l
   4F98 D1            [10]  602 	pop	de
   4F99 78            [ 4]  603 	ld	a, b
   4F9A C1            [10]  604 	pop	bc
   4F9B 47            [ 4]  605 	ld	b, a
                            606 ;src/systems/hud.c:70: cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), 2, 4);
                            607 ;src/systems/hud.c:88: cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 20, 2);
   4F9C C5            [11]  608 	push	bc
   4F9D D5            [11]  609 	push	de
   4F9E 21 14 02      [10]  610 	ld	hl, #0x0214
   4FA1 E5            [11]  611 	push	hl
   4FA2 C5            [11]  612 	push	bc
   4FA3 33            [ 6]  613 	inc	sp
   4FA4 D5            [11]  614 	push	de
   4FA5 CD F0 5D      [17]  615 	call	_cpct_drawSolidBox
   4FA8 F1            [10]  616 	pop	af
   4FA9 F1            [10]  617 	pop	af
   4FAA 33            [ 6]  618 	inc	sp
   4FAB D1            [10]  619 	pop	de
   4FAC C1            [10]  620 	pop	bc
                            621 ;src/systems/hud.c:89: if (timebar) {
   4FAD 79            [ 4]  622 	ld	a, c
   4FAE B7            [ 4]  623 	or	a, a
   4FAF 28 18         [12]  624 	jr	Z,00109$
                            625 ;src/systems/hud.c:90: cpct_drawSolidBox(pvmem, cpct_px2byteM0(9, 9), timebar, 2);
   4FB1 C5            [11]  626 	push	bc
   4FB2 D5            [11]  627 	push	de
   4FB3 21 09 09      [10]  628 	ld	hl, #0x0909
   4FB6 E5            [11]  629 	push	hl
   4FB7 CD B6 5D      [17]  630 	call	_cpct_px2byteM0
   4FBA 65            [ 4]  631 	ld	h, l
   4FBB D1            [10]  632 	pop	de
   4FBC C1            [10]  633 	pop	bc
   4FBD 06 02         [ 7]  634 	ld	b, #0x02
   4FBF C5            [11]  635 	push	bc
   4FC0 E5            [11]  636 	push	hl
   4FC1 33            [ 6]  637 	inc	sp
   4FC2 D5            [11]  638 	push	de
   4FC3 CD F0 5D      [17]  639 	call	_cpct_drawSolidBox
   4FC6 F1            [10]  640 	pop	af
   4FC7 F1            [10]  641 	pop	af
   4FC8 33            [ 6]  642 	inc	sp
   4FC9                     643 00109$:
                            644 ;src/systems/hud.c:93: weaponboxes = currentweapon;
   4FC9 21 95 5F      [10]  645 	ld	hl,#_currentweapon + 0
   4FCC 4E            [ 7]  646 	ld	c, (hl)
                            647 ;src/systems/hud.c:94: if (weaponboxes > 3) {
   4FCD 3E 03         [ 7]  648 	ld	a, #0x03
   4FCF 91            [ 4]  649 	sub	a, c
   4FD0 30 02         [12]  650 	jr	NC,00131$
                            651 ;src/systems/hud.c:95: weaponboxes = 3;
   4FD2 0E 03         [ 7]  652 	ld	c, #0x03
                            653 ;src/systems/hud.c:97: for (i = 0; i < weaponboxes; ++i) {
   4FD4                     654 00131$:
   4FD4 06 00         [ 7]  655 	ld	b, #0x00
   4FD6                     656 00118$:
                            657 ;src/systems/hud.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (u8)(72 + (i * 2)), 6);
   4FD6 78            [ 4]  658 	ld	a,b
   4FD7 B9            [ 4]  659 	cp	a,c
   4FD8 30 32         [12]  660 	jr	NC,00120$
   4FDA 87            [ 4]  661 	add	a, a
   4FDB C6 48         [ 7]  662 	add	a, #0x48
   4FDD 57            [ 4]  663 	ld	d, a
   4FDE C5            [11]  664 	push	bc
   4FDF 3E 06         [ 7]  665 	ld	a, #0x06
   4FE1 F5            [11]  666 	push	af
   4FE2 33            [ 6]  667 	inc	sp
   4FE3 D5            [11]  668 	push	de
   4FE4 33            [ 6]  669 	inc	sp
   4FE5 21 00 C0      [10]  670 	ld	hl, #0xc000
   4FE8 E5            [11]  671 	push	hl
   4FE9 CD A9 5E      [17]  672 	call	_cpct_getScreenPtr
   4FEC E5            [11]  673 	push	hl
   4FED 21 0B 0B      [10]  674 	ld	hl, #0x0b0b
   4FF0 E5            [11]  675 	push	hl
   4FF1 CD B6 5D      [17]  676 	call	_cpct_px2byteM0
   4FF4 DD 75 FF      [19]  677 	ld	-1 (ix), l
   4FF7 D1            [10]  678 	pop	de
   4FF8 21 01 03      [10]  679 	ld	hl, #0x0301
   4FFB E5            [11]  680 	push	hl
   4FFC DD 7E FF      [19]  681 	ld	a, -1 (ix)
   4FFF F5            [11]  682 	push	af
   5000 33            [ 6]  683 	inc	sp
   5001 D5            [11]  684 	push	de
   5002 CD F0 5D      [17]  685 	call	_cpct_drawSolidBox
   5005 F1            [10]  686 	pop	af
   5006 F1            [10]  687 	pop	af
   5007 33            [ 6]  688 	inc	sp
   5008 C1            [10]  689 	pop	bc
                            690 ;src/systems/hud.c:97: for (i = 0; i < weaponboxes; ++i) {
   5009 04            [ 4]  691 	inc	b
   500A 18 CA         [12]  692 	jr	00118$
   500C                     693 00120$:
   500C 33            [ 6]  694 	inc	sp
   500D DD E1         [14]  695 	pop	ix
   500F C9            [10]  696 	ret
                            697 	.area _CODE
                            698 	.area _INITIALIZER
                            699 	.area _CABS (ABS)
