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
                             12 	.globl _cpct_drawSprite
                             13 	.globl _hudinit
                             14 	.globl _hudupdate
                             15 	.globl _hudrender
                             16 ;--------------------------------------------------------
                             17 ; special function registers
                             18 ;--------------------------------------------------------
                             19 ;--------------------------------------------------------
                             20 ; ram data
                             21 ;--------------------------------------------------------
                             22 	.area _DATA
   5F23                      23 _currenthealth:
   5F23                      24 	.ds 1
   5F24                      25 _currentscore:
   5F24                      26 	.ds 2
   5F26                      27 _currenttime:
   5F26                      28 	.ds 1
   5F27                      29 _currentlives:
   5F27                      30 	.ds 1
   5F28                      31 _currentweapon:
   5F28                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
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
                             57 ;src/systems/hud.c:13: static const u8* hud_get_number_sprite(u8 n) {
                             58 ;	---------------------------------
                             59 ; Function hud_get_number_sprite
                             60 ; ---------------------------------
   4D17                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:15: return _hud_dummy_sprite;
   4D17 21 1B 4D      [10]   63 	ld	hl, #__hud_dummy_sprite
   4D1A C9            [10]   64 	ret
   4D1B                      65 __hud_dummy_sprite:
   4D1B 00                   66 	.db #0x00	; 0
   4D1C 00                   67 	.db 0x00
   4D1D 00                   68 	.db 0x00
   4D1E 00                   69 	.db 0x00
   4D1F 00                   70 	.db 0x00
   4D20 00                   71 	.db 0x00
   4D21 00                   72 	.db 0x00
   4D22 00                   73 	.db 0x00
   4D23 00                   74 	.db 0x00
   4D24 00                   75 	.db 0x00
   4D25 00                   76 	.db 0x00
   4D26 00                   77 	.db 0x00
   4D27 00                   78 	.db 0x00
   4D28 00                   79 	.db 0x00
   4D29 00                   80 	.db 0x00
   4D2A 00                   81 	.db 0x00
   4D2B 00                   82 	.db 0x00
   4D2C 00                   83 	.db 0x00
   4D2D 00                   84 	.db 0x00
   4D2E 00                   85 	.db 0x00
   4D2F 00                   86 	.db 0x00
   4D30 00                   87 	.db 0x00
   4D31 00                   88 	.db 0x00
   4D32 00                   89 	.db 0x00
   4D33 00                   90 	.db 0x00
   4D34 00                   91 	.db 0x00
   4D35 00                   92 	.db 0x00
   4D36 00                   93 	.db 0x00
   4D37 00                   94 	.db 0x00
   4D38 00                   95 	.db 0x00
   4D39 00                   96 	.db 0x00
   4D3A 00                   97 	.db 0x00
   4D3B 00                   98 	.db 0x00
   4D3C 00                   99 	.db 0x00
   4D3D 00                  100 	.db 0x00
   4D3E 00                  101 	.db 0x00
   4D3F 00                  102 	.db 0x00
   4D40 00                  103 	.db 0x00
   4D41 00                  104 	.db 0x00
   4D42 00                  105 	.db 0x00
   4D43 00                  106 	.db 0x00
   4D44 00                  107 	.db 0x00
   4D45 00                  108 	.db 0x00
   4D46 00                  109 	.db 0x00
   4D47 00                  110 	.db 0x00
   4D48 00                  111 	.db 0x00
   4D49 00                  112 	.db 0x00
   4D4A 00                  113 	.db 0x00
   4D4B 00                  114 	.db 0x00
   4D4C 00                  115 	.db 0x00
   4D4D 00                  116 	.db 0x00
   4D4E 00                  117 	.db 0x00
   4D4F 00                  118 	.db 0x00
   4D50 00                  119 	.db 0x00
   4D51 00                  120 	.db 0x00
   4D52 00                  121 	.db 0x00
   4D53 00                  122 	.db 0x00
   4D54 00                  123 	.db 0x00
   4D55 00                  124 	.db 0x00
   4D56 00                  125 	.db 0x00
   4D57 00                  126 	.db 0x00
   4D58 00                  127 	.db 0x00
   4D59 00                  128 	.db 0x00
   4D5A 00                  129 	.db 0x00
                            130 ;src/systems/hud.c:20: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            131 ;	---------------------------------
                            132 ; Function hud_draw_digits
                            133 ; ---------------------------------
   4D5B                     134 _hud_draw_digits:
   4D5B DD E5         [15]  135 	push	ix
   4D5D DD 21 00 00   [14]  136 	ld	ix,#0
   4D61 DD 39         [15]  137 	add	ix,sp
   4D63 3B            [ 6]  138 	dec	sp
                            139 ;src/systems/hud.c:26: divisor = 1;
   4D64 01 01 00      [10]  140 	ld	bc, #0x0001
                            141 ;src/systems/hud.c:27: for (i = 1; i < digits; ++i) {
   4D67 1E 01         [ 7]  142 	ld	e, #0x01
   4D69                     143 00106$:
   4D69 7B            [ 4]  144 	ld	a, e
   4D6A DD 96 06      [19]  145 	sub	a, 6 (ix)
   4D6D 30 0B         [12]  146 	jr	NC,00101$
                            147 ;src/systems/hud.c:28: divisor *= 10;
   4D6F 69            [ 4]  148 	ld	l, c
   4D70 60            [ 4]  149 	ld	h, b
   4D71 29            [11]  150 	add	hl, hl
   4D72 29            [11]  151 	add	hl, hl
   4D73 09            [11]  152 	add	hl, bc
   4D74 29            [11]  153 	add	hl, hl
   4D75 4D            [ 4]  154 	ld	c, l
   4D76 44            [ 4]  155 	ld	b, h
                            156 ;src/systems/hud.c:27: for (i = 1; i < digits; ++i) {
   4D77 1C            [ 4]  157 	inc	e
   4D78 18 EF         [12]  158 	jr	00106$
   4D7A                     159 00101$:
                            160 ;src/systems/hud.c:31: for (i = 0; i < digits; ++i) {
   4D7A DD 36 FF 00   [19]  161 	ld	-1 (ix), #0x00
   4D7E                     162 00109$:
   4D7E DD 7E FF      [19]  163 	ld	a, -1 (ix)
   4D81 DD 96 06      [19]  164 	sub	a, 6 (ix)
   4D84 D2 03 4E      [10]  165 	jp	NC, 00111$
                            166 ;src/systems/hud.c:32: digit = (u8)(value / divisor);
   4D87 C5            [11]  167 	push	bc
   4D88 C5            [11]  168 	push	bc
   4D89 DD 6E 04      [19]  169 	ld	l,4 (ix)
   4D8C DD 66 05      [19]  170 	ld	h,5 (ix)
   4D8F E5            [11]  171 	push	hl
   4D90 CD B2 5B      [17]  172 	call	__divuint
   4D93 F1            [10]  173 	pop	af
   4D94 F1            [10]  174 	pop	af
   4D95 5D            [ 4]  175 	ld	e, l
   4D96 C1            [10]  176 	pop	bc
                            177 ;src/systems/hud.c:33: value = (u16)(value % divisor);
   4D97 C5            [11]  178 	push	bc
   4D98 D5            [11]  179 	push	de
   4D99 C5            [11]  180 	push	bc
   4D9A DD 6E 04      [19]  181 	ld	l,4 (ix)
   4D9D DD 66 05      [19]  182 	ld	h,5 (ix)
   4DA0 E5            [11]  183 	push	hl
   4DA1 CD 3D 5D      [17]  184 	call	__moduint
   4DA4 F1            [10]  185 	pop	af
   4DA5 F1            [10]  186 	pop	af
   4DA6 D1            [10]  187 	pop	de
   4DA7 C1            [10]  188 	pop	bc
   4DA8 DD 75 04      [19]  189 	ld	4 (ix), l
   4DAB DD 74 05      [19]  190 	ld	5 (ix), h
                            191 ;src/systems/hud.c:35: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4DAE DD 7E FF      [19]  192 	ld	a, -1 (ix)
   4DB1 07            [ 4]  193 	rlca
   4DB2 07            [ 4]  194 	rlca
   4DB3 07            [ 4]  195 	rlca
   4DB4 E6 F8         [ 7]  196 	and	a, #0xf8
   4DB6 57            [ 4]  197 	ld	d, a
   4DB7 DD 7E 07      [19]  198 	ld	a, 7 (ix)
   4DBA 82            [ 4]  199 	add	a, d
   4DBB 57            [ 4]  200 	ld	d, a
   4DBC C5            [11]  201 	push	bc
   4DBD D5            [11]  202 	push	de
   4DBE DD 7E 08      [19]  203 	ld	a, 8 (ix)
   4DC1 F5            [11]  204 	push	af
   4DC2 33            [ 6]  205 	inc	sp
   4DC3 D5            [11]  206 	push	de
   4DC4 33            [ 6]  207 	inc	sp
   4DC5 21 00 C0      [10]  208 	ld	hl, #0xc000
   4DC8 E5            [11]  209 	push	hl
   4DC9 CD 53 5E      [17]  210 	call	_cpct_getScreenPtr
   4DCC D1            [10]  211 	pop	de
   4DCD C1            [10]  212 	pop	bc
                            213 ;src/systems/hud.c:36: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
   4DCE E5            [11]  214 	push	hl
   4DCF C5            [11]  215 	push	bc
   4DD0 7B            [ 4]  216 	ld	a, e
   4DD1 F5            [11]  217 	push	af
   4DD2 33            [ 6]  218 	inc	sp
   4DD3 CD 17 4D      [17]  219 	call	_hud_get_number_sprite
   4DD6 33            [ 6]  220 	inc	sp
   4DD7 EB            [ 4]  221 	ex	de,hl
   4DD8 C1            [10]  222 	pop	bc
   4DD9 E1            [10]  223 	pop	hl
   4DDA D5            [11]  224 	push	de
   4DDB FD E1         [14]  225 	pop	iy
   4DDD C5            [11]  226 	push	bc
   4DDE 11 08 08      [10]  227 	ld	de, #0x0808
   4DE1 D5            [11]  228 	push	de
   4DE2 E5            [11]  229 	push	hl
   4DE3 FD E5         [15]  230 	push	iy
   4DE5 CD 8C 5C      [17]  231 	call	_cpct_drawSprite
   4DE8 C1            [10]  232 	pop	bc
                            233 ;src/systems/hud.c:38: if (divisor > 1) {
   4DE9 3E 01         [ 7]  234 	ld	a, #0x01
   4DEB B9            [ 4]  235 	cp	a, c
   4DEC 3E 00         [ 7]  236 	ld	a, #0x00
   4DEE 98            [ 4]  237 	sbc	a, b
   4DEF 30 0C         [12]  238 	jr	NC,00110$
                            239 ;src/systems/hud.c:39: divisor /= 10;
   4DF1 21 0A 00      [10]  240 	ld	hl, #0x000a
   4DF4 E5            [11]  241 	push	hl
   4DF5 C5            [11]  242 	push	bc
   4DF6 CD B2 5B      [17]  243 	call	__divuint
   4DF9 F1            [10]  244 	pop	af
   4DFA F1            [10]  245 	pop	af
   4DFB 4D            [ 4]  246 	ld	c, l
   4DFC 44            [ 4]  247 	ld	b, h
   4DFD                     248 00110$:
                            249 ;src/systems/hud.c:31: for (i = 0; i < digits; ++i) {
   4DFD DD 34 FF      [23]  250 	inc	-1 (ix)
   4E00 C3 7E 4D      [10]  251 	jp	00109$
   4E03                     252 00111$:
   4E03 33            [ 6]  253 	inc	sp
   4E04 DD E1         [14]  254 	pop	ix
   4E06 C9            [10]  255 	ret
   4E07                     256 _hudhealth:
   4E07 00                  257 	.db #0x00	; 0
   4E08 00                  258 	.db 0x00
   4E09 00                  259 	.db 0x00
   4E0A 00                  260 	.db 0x00
   4E0B 00                  261 	.db 0x00
   4E0C 00                  262 	.db 0x00
   4E0D 00                  263 	.db 0x00
   4E0E 00                  264 	.db 0x00
   4E0F 00                  265 	.db 0x00
   4E10 00                  266 	.db 0x00
   4E11 00                  267 	.db 0x00
   4E12 00                  268 	.db 0x00
   4E13 00                  269 	.db 0x00
   4E14 00                  270 	.db 0x00
   4E15 00                  271 	.db 0x00
   4E16 00                  272 	.db 0x00
   4E17 00                  273 	.db 0x00
   4E18 00                  274 	.db 0x00
   4E19 00                  275 	.db 0x00
   4E1A 00                  276 	.db 0x00
   4E1B 00                  277 	.db 0x00
   4E1C 00                  278 	.db 0x00
   4E1D 00                  279 	.db 0x00
   4E1E 00                  280 	.db 0x00
   4E1F 00                  281 	.db 0x00
   4E20 00                  282 	.db 0x00
   4E21 00                  283 	.db 0x00
   4E22 00                  284 	.db 0x00
   4E23 00                  285 	.db 0x00
   4E24 00                  286 	.db 0x00
   4E25 00                  287 	.db 0x00
   4E26 00                  288 	.db 0x00
   4E27 00                  289 	.db 0x00
   4E28 00                  290 	.db 0x00
   4E29 00                  291 	.db 0x00
   4E2A 00                  292 	.db 0x00
   4E2B 00                  293 	.db 0x00
   4E2C 00                  294 	.db 0x00
   4E2D 00                  295 	.db 0x00
   4E2E 00                  296 	.db 0x00
   4E2F 00                  297 	.db 0x00
   4E30 00                  298 	.db 0x00
   4E31 00                  299 	.db 0x00
   4E32 00                  300 	.db 0x00
   4E33 00                  301 	.db 0x00
   4E34 00                  302 	.db 0x00
   4E35 00                  303 	.db 0x00
   4E36 00                  304 	.db 0x00
   4E37 00                  305 	.db 0x00
   4E38 00                  306 	.db 0x00
   4E39 00                  307 	.db 0x00
   4E3A 00                  308 	.db 0x00
   4E3B 00                  309 	.db 0x00
   4E3C 00                  310 	.db 0x00
   4E3D 00                  311 	.db 0x00
   4E3E 00                  312 	.db 0x00
   4E3F 00                  313 	.db 0x00
   4E40 00                  314 	.db 0x00
   4E41 00                  315 	.db 0x00
   4E42 00                  316 	.db 0x00
   4E43 00                  317 	.db 0x00
   4E44 00                  318 	.db 0x00
   4E45 00                  319 	.db 0x00
   4E46 00                  320 	.db 0x00
   4E47                     321 _hudlives:
   4E47 00                  322 	.db #0x00	; 0
   4E48 00                  323 	.db 0x00
   4E49 00                  324 	.db 0x00
   4E4A 00                  325 	.db 0x00
   4E4B 00                  326 	.db 0x00
   4E4C 00                  327 	.db 0x00
   4E4D 00                  328 	.db 0x00
   4E4E 00                  329 	.db 0x00
   4E4F 00                  330 	.db 0x00
   4E50 00                  331 	.db 0x00
   4E51 00                  332 	.db 0x00
   4E52 00                  333 	.db 0x00
   4E53 00                  334 	.db 0x00
   4E54 00                  335 	.db 0x00
   4E55 00                  336 	.db 0x00
   4E56 00                  337 	.db 0x00
   4E57 00                  338 	.db 0x00
   4E58 00                  339 	.db 0x00
   4E59 00                  340 	.db 0x00
   4E5A 00                  341 	.db 0x00
   4E5B 00                  342 	.db 0x00
   4E5C 00                  343 	.db 0x00
   4E5D 00                  344 	.db 0x00
   4E5E 00                  345 	.db 0x00
   4E5F 00                  346 	.db 0x00
   4E60 00                  347 	.db 0x00
   4E61 00                  348 	.db 0x00
   4E62 00                  349 	.db 0x00
   4E63 00                  350 	.db 0x00
   4E64 00                  351 	.db 0x00
   4E65 00                  352 	.db 0x00
   4E66 00                  353 	.db 0x00
   4E67 00                  354 	.db 0x00
   4E68 00                  355 	.db 0x00
   4E69 00                  356 	.db 0x00
   4E6A 00                  357 	.db 0x00
   4E6B 00                  358 	.db 0x00
   4E6C 00                  359 	.db 0x00
   4E6D 00                  360 	.db 0x00
   4E6E 00                  361 	.db 0x00
   4E6F 00                  362 	.db 0x00
   4E70 00                  363 	.db 0x00
   4E71 00                  364 	.db 0x00
   4E72 00                  365 	.db 0x00
   4E73 00                  366 	.db 0x00
   4E74 00                  367 	.db 0x00
   4E75 00                  368 	.db 0x00
   4E76 00                  369 	.db 0x00
   4E77 00                  370 	.db 0x00
   4E78 00                  371 	.db 0x00
   4E79 00                  372 	.db 0x00
   4E7A 00                  373 	.db 0x00
   4E7B 00                  374 	.db 0x00
   4E7C 00                  375 	.db 0x00
   4E7D 00                  376 	.db 0x00
   4E7E 00                  377 	.db 0x00
   4E7F 00                  378 	.db 0x00
   4E80 00                  379 	.db 0x00
   4E81 00                  380 	.db 0x00
   4E82 00                  381 	.db 0x00
   4E83 00                  382 	.db 0x00
   4E84 00                  383 	.db 0x00
   4E85 00                  384 	.db 0x00
   4E86 00                  385 	.db 0x00
                            386 ;src/systems/hud.c:44: void hudinit(void) {
                            387 ;	---------------------------------
                            388 ; Function hudinit
                            389 ; ---------------------------------
   4E87                     390 _hudinit::
                            391 ;src/systems/hud.c:45: currenthealth = 3;
   4E87 21 23 5F      [10]  392 	ld	hl,#_currenthealth + 0
   4E8A 36 03         [10]  393 	ld	(hl), #0x03
                            394 ;src/systems/hud.c:46: currentscore  = 0;
   4E8C 21 00 00      [10]  395 	ld	hl, #0x0000
   4E8F 22 24 5F      [16]  396 	ld	(_currentscore), hl
                            397 ;src/systems/hud.c:47: currenttime   = 90;
   4E92 21 26 5F      [10]  398 	ld	hl,#_currenttime + 0
   4E95 36 5A         [10]  399 	ld	(hl), #0x5a
                            400 ;src/systems/hud.c:48: currentlives  = 3;
   4E97 21 27 5F      [10]  401 	ld	hl,#_currentlives + 0
   4E9A 36 03         [10]  402 	ld	(hl), #0x03
                            403 ;src/systems/hud.c:49: currentweapon = 0;
   4E9C 21 28 5F      [10]  404 	ld	hl,#_currentweapon + 0
   4E9F 36 00         [10]  405 	ld	(hl), #0x00
   4EA1 C9            [10]  406 	ret
                            407 ;src/systems/hud.c:52: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            408 ;	---------------------------------
                            409 ; Function hudupdate
                            410 ; ---------------------------------
   4EA2                     411 _hudupdate::
                            412 ;src/systems/hud.c:53: currenthealth = lives;
   4EA2 21 02 00      [10]  413 	ld	hl, #2+0
   4EA5 39            [11]  414 	add	hl, sp
   4EA6 7E            [ 7]  415 	ld	a, (hl)
   4EA7 32 23 5F      [13]  416 	ld	(#_currenthealth + 0),a
                            417 ;src/systems/hud.c:54: currentscore  = score;
   4EAA 21 03 00      [10]  418 	ld	hl, #3+0
   4EAD 39            [11]  419 	add	hl, sp
   4EAE 7E            [ 7]  420 	ld	a, (hl)
   4EAF 32 24 5F      [13]  421 	ld	(#_currentscore + 0),a
   4EB2 21 04 00      [10]  422 	ld	hl, #3+1
   4EB5 39            [11]  423 	add	hl, sp
   4EB6 7E            [ 7]  424 	ld	a, (hl)
   4EB7 32 25 5F      [13]  425 	ld	(#_currentscore + 1),a
                            426 ;src/systems/hud.c:55: currenttime   = time;
   4EBA 21 05 00      [10]  427 	ld	hl, #5+0
   4EBD 39            [11]  428 	add	hl, sp
   4EBE 7E            [ 7]  429 	ld	a, (hl)
   4EBF 32 26 5F      [13]  430 	ld	(#_currenttime + 0),a
                            431 ;src/systems/hud.c:56: currentlives  = lives;
   4EC2 21 02 00      [10]  432 	ld	hl, #2+0
   4EC5 39            [11]  433 	add	hl, sp
   4EC6 7E            [ 7]  434 	ld	a, (hl)
   4EC7 32 27 5F      [13]  435 	ld	(#_currentlives + 0),a
                            436 ;src/systems/hud.c:57: currentweapon = weapon;
   4ECA 21 06 00      [10]  437 	ld	hl, #6+0
   4ECD 39            [11]  438 	add	hl, sp
   4ECE 7E            [ 7]  439 	ld	a, (hl)
   4ECF 32 28 5F      [13]  440 	ld	(#_currentweapon + 0),a
   4ED2 C9            [10]  441 	ret
                            442 ;src/systems/hud.c:60: void hudrender(void) {
                            443 ;	---------------------------------
                            444 ; Function hudrender
                            445 ; ---------------------------------
   4ED3                     446 _hudrender::
                            447 ;src/systems/hud.c:66: for (i = 0; i < currenthealth; ++i) {
   4ED3 0E 00         [ 7]  448 	ld	c, #0x00
   4ED5                     449 00103$:
   4ED5 21 23 5F      [10]  450 	ld	hl, #_currenthealth
                            451 ;src/systems/hud.c:67: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4ED8 79            [ 4]  452 	ld	a,c
   4ED9 BE            [ 7]  453 	cp	a,(hl)
   4EDA 30 24         [12]  454 	jr	NC,00101$
   4EDC 07            [ 4]  455 	rlca
   4EDD 07            [ 4]  456 	rlca
   4EDE 07            [ 4]  457 	rlca
   4EDF E6 F8         [ 7]  458 	and	a, #0xf8
   4EE1 47            [ 4]  459 	ld	b, a
   4EE2 C5            [11]  460 	push	bc
   4EE3 3E 02         [ 7]  461 	ld	a, #0x02
   4EE5 F5            [11]  462 	push	af
   4EE6 33            [ 6]  463 	inc	sp
   4EE7 C5            [11]  464 	push	bc
   4EE8 33            [ 6]  465 	inc	sp
   4EE9 21 00 C0      [10]  466 	ld	hl, #0xc000
   4EEC E5            [11]  467 	push	hl
   4EED CD 53 5E      [17]  468 	call	_cpct_getScreenPtr
   4EF0 11 08 08      [10]  469 	ld	de, #0x0808
   4EF3 D5            [11]  470 	push	de
   4EF4 E5            [11]  471 	push	hl
   4EF5 21 07 4E      [10]  472 	ld	hl, #_hudhealth
   4EF8 E5            [11]  473 	push	hl
   4EF9 CD 8C 5C      [17]  474 	call	_cpct_drawSprite
   4EFC C1            [10]  475 	pop	bc
                            476 ;src/systems/hud.c:66: for (i = 0; i < currenthealth; ++i) {
   4EFD 0C            [ 4]  477 	inc	c
   4EFE 18 D5         [12]  478 	jr	00103$
   4F00                     479 00101$:
                            480 ;src/systems/hud.c:71: scoretemp = currentscore;
   4F00 2A 24 5F      [16]  481 	ld	hl, (_currentscore)
                            482 ;src/systems/hud.c:72: hud_draw_digits(scoretemp, 4, 24, 2);
   4F03 01 18 02      [10]  483 	ld	bc, #0x0218
   4F06 C5            [11]  484 	push	bc
   4F07 3E 04         [ 7]  485 	ld	a, #0x04
   4F09 F5            [11]  486 	push	af
   4F0A 33            [ 6]  487 	inc	sp
   4F0B E5            [11]  488 	push	hl
   4F0C CD 5B 4D      [17]  489 	call	_hud_draw_digits
   4F0F F1            [10]  490 	pop	af
   4F10 F1            [10]  491 	pop	af
   4F11 33            [ 6]  492 	inc	sp
                            493 ;src/systems/hud.c:74: timetemp = currenttime;
   4F12 21 26 5F      [10]  494 	ld	hl,#_currenttime + 0
   4F15 4E            [ 7]  495 	ld	c, (hl)
                            496 ;src/systems/hud.c:75: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4F16 06 00         [ 7]  497 	ld	b, #0x00
   4F18 21 38 02      [10]  498 	ld	hl, #0x0238
   4F1B E5            [11]  499 	push	hl
   4F1C 3E 03         [ 7]  500 	ld	a, #0x03
   4F1E F5            [11]  501 	push	af
   4F1F 33            [ 6]  502 	inc	sp
   4F20 C5            [11]  503 	push	bc
   4F21 CD 5B 4D      [17]  504 	call	_hud_draw_digits
   4F24 F1            [10]  505 	pop	af
                            506 ;src/systems/hud.c:77: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4F25 33            [ 6]  507 	inc	sp
   4F26 21 02 B4      [10]  508 	ld	hl,#0xb402
   4F29 E3            [19]  509 	ex	(sp),hl
   4F2A 21 00 C0      [10]  510 	ld	hl, #0xc000
   4F2D E5            [11]  511 	push	hl
   4F2E CD 53 5E      [17]  512 	call	_cpct_getScreenPtr
                            513 ;src/systems/hud.c:78: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4F31 01 47 4E      [10]  514 	ld	bc, #_hudlives+0
   4F34 11 08 08      [10]  515 	ld	de, #0x0808
   4F37 D5            [11]  516 	push	de
   4F38 E5            [11]  517 	push	hl
   4F39 C5            [11]  518 	push	bc
   4F3A CD 8C 5C      [17]  519 	call	_cpct_drawSprite
                            520 ;src/systems/hud.c:80: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4F3D 21 0C B4      [10]  521 	ld	hl, #0xb40c
   4F40 E5            [11]  522 	push	hl
   4F41 21 00 C0      [10]  523 	ld	hl, #0xc000
   4F44 E5            [11]  524 	push	hl
   4F45 CD 53 5E      [17]  525 	call	_cpct_getScreenPtr
                            526 ;src/systems/hud.c:81: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);
   4F48 E5            [11]  527 	push	hl
   4F49 3E 0A         [ 7]  528 	ld	a, #0x0a
   4F4B F5            [11]  529 	push	af
   4F4C 33            [ 6]  530 	inc	sp
   4F4D 3A 27 5F      [13]  531 	ld	a, (_currentlives)
   4F50 F5            [11]  532 	push	af
   4F51 33            [ 6]  533 	inc	sp
   4F52 CD 31 5D      [17]  534 	call	__moduchar
   4F55 F1            [10]  535 	pop	af
   4F56 55            [ 4]  536 	ld	d, l
   4F57 D5            [11]  537 	push	de
   4F58 33            [ 6]  538 	inc	sp
   4F59 CD 17 4D      [17]  539 	call	_hud_get_number_sprite
   4F5C 33            [ 6]  540 	inc	sp
   4F5D C1            [10]  541 	pop	bc
   4F5E 11 08 08      [10]  542 	ld	de, #0x0808
   4F61 D5            [11]  543 	push	de
   4F62 C5            [11]  544 	push	bc
   4F63 E5            [11]  545 	push	hl
   4F64 CD 8C 5C      [17]  546 	call	_cpct_drawSprite
                            547 ;src/systems/hud.c:83: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4F67 21 46 B4      [10]  548 	ld	hl, #0xb446
   4F6A E5            [11]  549 	push	hl
   4F6B 21 00 C0      [10]  550 	ld	hl, #0xc000
   4F6E E5            [11]  551 	push	hl
   4F6F CD 53 5E      [17]  552 	call	_cpct_getScreenPtr
                            553 ;src/systems/hud.c:84: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
   4F72 E5            [11]  554 	push	hl
   4F73 3E 0A         [ 7]  555 	ld	a, #0x0a
   4F75 F5            [11]  556 	push	af
   4F76 33            [ 6]  557 	inc	sp
   4F77 3A 28 5F      [13]  558 	ld	a, (_currentweapon)
   4F7A F5            [11]  559 	push	af
   4F7B 33            [ 6]  560 	inc	sp
   4F7C CD 31 5D      [17]  561 	call	__moduchar
   4F7F F1            [10]  562 	pop	af
   4F80 55            [ 4]  563 	ld	d, l
   4F81 D5            [11]  564 	push	de
   4F82 33            [ 6]  565 	inc	sp
   4F83 CD 17 4D      [17]  566 	call	_hud_get_number_sprite
   4F86 33            [ 6]  567 	inc	sp
   4F87 C1            [10]  568 	pop	bc
   4F88 11 08 08      [10]  569 	ld	de, #0x0808
   4F8B D5            [11]  570 	push	de
   4F8C C5            [11]  571 	push	bc
   4F8D E5            [11]  572 	push	hl
   4F8E CD 8C 5C      [17]  573 	call	_cpct_drawSprite
   4F91 C9            [10]  574 	ret
                            575 	.area _CODE
                            576 	.area _INITIALIZER
                            577 	.area _CABS (ABS)
