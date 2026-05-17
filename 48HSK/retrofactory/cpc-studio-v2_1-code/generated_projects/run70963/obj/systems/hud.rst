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
   5F1C                      23 _currenthealth:
   5F1C                      24 	.ds 1
   5F1D                      25 _currentscore:
   5F1D                      26 	.ds 2
   5F1F                      27 _currenttime:
   5F1F                      28 	.ds 1
   5F20                      29 _currentlives:
   5F20                      30 	.ds 1
   5F21                      31 _currentweapon:
   5F21                      32 	.ds 1
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
                             57 ;src/systems/hud.c:16: static const u8* hud_get_number_sprite(u8 digit) {
                             58 ;	---------------------------------
                             59 ; Function hud_get_number_sprite
                             60 ; ---------------------------------
   4D0A                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:18: return _hud_dummy_sprite;
   4D0A 21 0E 4D      [10]   63 	ld	hl, #__hud_dummy_sprite
   4D0D C9            [10]   64 	ret
   4D0E                      65 __hud_dummy_sprite:
   4D0E 00                   66 	.db #0x00	; 0
   4D0F 00                   67 	.db 0x00
   4D10 00                   68 	.db 0x00
   4D11 00                   69 	.db 0x00
   4D12 00                   70 	.db 0x00
   4D13 00                   71 	.db 0x00
   4D14 00                   72 	.db 0x00
   4D15 00                   73 	.db 0x00
   4D16 00                   74 	.db 0x00
   4D17 00                   75 	.db 0x00
   4D18 00                   76 	.db 0x00
   4D19 00                   77 	.db 0x00
   4D1A 00                   78 	.db 0x00
   4D1B 00                   79 	.db 0x00
   4D1C 00                   80 	.db 0x00
   4D1D 00                   81 	.db 0x00
   4D1E 00                   82 	.db 0x00
   4D1F 00                   83 	.db 0x00
   4D20 00                   84 	.db 0x00
   4D21 00                   85 	.db 0x00
   4D22 00                   86 	.db 0x00
   4D23 00                   87 	.db 0x00
   4D24 00                   88 	.db 0x00
   4D25 00                   89 	.db 0x00
   4D26 00                   90 	.db 0x00
   4D27 00                   91 	.db 0x00
   4D28 00                   92 	.db 0x00
   4D29 00                   93 	.db 0x00
   4D2A 00                   94 	.db 0x00
   4D2B 00                   95 	.db 0x00
   4D2C 00                   96 	.db 0x00
   4D2D 00                   97 	.db 0x00
   4D2E 00                   98 	.db 0x00
   4D2F 00                   99 	.db 0x00
   4D30 00                  100 	.db 0x00
   4D31 00                  101 	.db 0x00
   4D32 00                  102 	.db 0x00
   4D33 00                  103 	.db 0x00
   4D34 00                  104 	.db 0x00
   4D35 00                  105 	.db 0x00
   4D36 00                  106 	.db 0x00
   4D37 00                  107 	.db 0x00
   4D38 00                  108 	.db 0x00
   4D39 00                  109 	.db 0x00
   4D3A 00                  110 	.db 0x00
   4D3B 00                  111 	.db 0x00
   4D3C 00                  112 	.db 0x00
   4D3D 00                  113 	.db 0x00
   4D3E 00                  114 	.db 0x00
   4D3F 00                  115 	.db 0x00
   4D40 00                  116 	.db 0x00
   4D41 00                  117 	.db 0x00
   4D42 00                  118 	.db 0x00
   4D43 00                  119 	.db 0x00
   4D44 00                  120 	.db 0x00
   4D45 00                  121 	.db 0x00
   4D46 00                  122 	.db 0x00
   4D47 00                  123 	.db 0x00
   4D48 00                  124 	.db 0x00
   4D49 00                  125 	.db 0x00
   4D4A 00                  126 	.db 0x00
   4D4B 00                  127 	.db 0x00
   4D4C 00                  128 	.db 0x00
   4D4D 00                  129 	.db 0x00
   4D4E                     130 _hudhealth:
   4D4E 00                  131 	.db #0x00	; 0
   4D4F 00                  132 	.db 0x00
   4D50 00                  133 	.db 0x00
   4D51 00                  134 	.db 0x00
   4D52 00                  135 	.db 0x00
   4D53 00                  136 	.db 0x00
   4D54 00                  137 	.db 0x00
   4D55 00                  138 	.db 0x00
   4D56 00                  139 	.db 0x00
   4D57 00                  140 	.db 0x00
   4D58 00                  141 	.db 0x00
   4D59 00                  142 	.db 0x00
   4D5A 00                  143 	.db 0x00
   4D5B 00                  144 	.db 0x00
   4D5C 00                  145 	.db 0x00
   4D5D 00                  146 	.db 0x00
   4D5E 00                  147 	.db 0x00
   4D5F 00                  148 	.db 0x00
   4D60 00                  149 	.db 0x00
   4D61 00                  150 	.db 0x00
   4D62 00                  151 	.db 0x00
   4D63 00                  152 	.db 0x00
   4D64 00                  153 	.db 0x00
   4D65 00                  154 	.db 0x00
   4D66 00                  155 	.db 0x00
   4D67 00                  156 	.db 0x00
   4D68 00                  157 	.db 0x00
   4D69 00                  158 	.db 0x00
   4D6A 00                  159 	.db 0x00
   4D6B 00                  160 	.db 0x00
   4D6C 00                  161 	.db 0x00
   4D6D 00                  162 	.db 0x00
   4D6E 00                  163 	.db 0x00
   4D6F 00                  164 	.db 0x00
   4D70 00                  165 	.db 0x00
   4D71 00                  166 	.db 0x00
   4D72 00                  167 	.db 0x00
   4D73 00                  168 	.db 0x00
   4D74 00                  169 	.db 0x00
   4D75 00                  170 	.db 0x00
   4D76 00                  171 	.db 0x00
   4D77 00                  172 	.db 0x00
   4D78 00                  173 	.db 0x00
   4D79 00                  174 	.db 0x00
   4D7A 00                  175 	.db 0x00
   4D7B 00                  176 	.db 0x00
   4D7C 00                  177 	.db 0x00
   4D7D 00                  178 	.db 0x00
   4D7E 00                  179 	.db 0x00
   4D7F 00                  180 	.db 0x00
   4D80 00                  181 	.db 0x00
   4D81 00                  182 	.db 0x00
   4D82 00                  183 	.db 0x00
   4D83 00                  184 	.db 0x00
   4D84 00                  185 	.db 0x00
   4D85 00                  186 	.db 0x00
   4D86 00                  187 	.db 0x00
   4D87 00                  188 	.db 0x00
   4D88 00                  189 	.db 0x00
   4D89 00                  190 	.db 0x00
   4D8A 00                  191 	.db 0x00
   4D8B 00                  192 	.db 0x00
   4D8C 00                  193 	.db 0x00
   4D8D 00                  194 	.db 0x00
   4D8E                     195 _hudlives:
   4D8E 00                  196 	.db #0x00	; 0
   4D8F 00                  197 	.db 0x00
   4D90 00                  198 	.db 0x00
   4D91 00                  199 	.db 0x00
   4D92 00                  200 	.db 0x00
   4D93 00                  201 	.db 0x00
   4D94 00                  202 	.db 0x00
   4D95 00                  203 	.db 0x00
   4D96 00                  204 	.db 0x00
   4D97 00                  205 	.db 0x00
   4D98 00                  206 	.db 0x00
   4D99 00                  207 	.db 0x00
   4D9A 00                  208 	.db 0x00
   4D9B 00                  209 	.db 0x00
   4D9C 00                  210 	.db 0x00
   4D9D 00                  211 	.db 0x00
   4D9E 00                  212 	.db 0x00
   4D9F 00                  213 	.db 0x00
   4DA0 00                  214 	.db 0x00
   4DA1 00                  215 	.db 0x00
   4DA2 00                  216 	.db 0x00
   4DA3 00                  217 	.db 0x00
   4DA4 00                  218 	.db 0x00
   4DA5 00                  219 	.db 0x00
   4DA6 00                  220 	.db 0x00
   4DA7 00                  221 	.db 0x00
   4DA8 00                  222 	.db 0x00
   4DA9 00                  223 	.db 0x00
   4DAA 00                  224 	.db 0x00
   4DAB 00                  225 	.db 0x00
   4DAC 00                  226 	.db 0x00
   4DAD 00                  227 	.db 0x00
   4DAE 00                  228 	.db 0x00
   4DAF 00                  229 	.db 0x00
   4DB0 00                  230 	.db 0x00
   4DB1 00                  231 	.db 0x00
   4DB2 00                  232 	.db 0x00
   4DB3 00                  233 	.db 0x00
   4DB4 00                  234 	.db 0x00
   4DB5 00                  235 	.db 0x00
   4DB6 00                  236 	.db 0x00
   4DB7 00                  237 	.db 0x00
   4DB8 00                  238 	.db 0x00
   4DB9 00                  239 	.db 0x00
   4DBA 00                  240 	.db 0x00
   4DBB 00                  241 	.db 0x00
   4DBC 00                  242 	.db 0x00
   4DBD 00                  243 	.db 0x00
   4DBE 00                  244 	.db 0x00
   4DBF 00                  245 	.db 0x00
   4DC0 00                  246 	.db 0x00
   4DC1 00                  247 	.db 0x00
   4DC2 00                  248 	.db 0x00
   4DC3 00                  249 	.db 0x00
   4DC4 00                  250 	.db 0x00
   4DC5 00                  251 	.db 0x00
   4DC6 00                  252 	.db 0x00
   4DC7 00                  253 	.db 0x00
   4DC8 00                  254 	.db 0x00
   4DC9 00                  255 	.db 0x00
   4DCA 00                  256 	.db 0x00
   4DCB 00                  257 	.db 0x00
   4DCC 00                  258 	.db 0x00
   4DCD 00                  259 	.db 0x00
                            260 ;src/systems/hud.c:21: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            261 ;	---------------------------------
                            262 ; Function hud_draw_digits
                            263 ; ---------------------------------
   4DCE                     264 _hud_draw_digits:
   4DCE DD E5         [15]  265 	push	ix
   4DD0 DD 21 00 00   [14]  266 	ld	ix,#0
   4DD4 DD 39         [15]  267 	add	ix,sp
   4DD6 3B            [ 6]  268 	dec	sp
                            269 ;src/systems/hud.c:27: divisor = 1;
   4DD7 01 01 00      [10]  270 	ld	bc, #0x0001
                            271 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4DDA 1E 01         [ 7]  272 	ld	e, #0x01
   4DDC                     273 00106$:
   4DDC 7B            [ 4]  274 	ld	a, e
   4DDD DD 96 06      [19]  275 	sub	a, 6 (ix)
   4DE0 30 0B         [12]  276 	jr	NC,00101$
                            277 ;src/systems/hud.c:29: divisor *= 10;
   4DE2 69            [ 4]  278 	ld	l, c
   4DE3 60            [ 4]  279 	ld	h, b
   4DE4 29            [11]  280 	add	hl, hl
   4DE5 29            [11]  281 	add	hl, hl
   4DE6 09            [11]  282 	add	hl, bc
   4DE7 29            [11]  283 	add	hl, hl
   4DE8 4D            [ 4]  284 	ld	c, l
   4DE9 44            [ 4]  285 	ld	b, h
                            286 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4DEA 1C            [ 4]  287 	inc	e
   4DEB 18 EF         [12]  288 	jr	00106$
   4DED                     289 00101$:
                            290 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4DED DD 36 FF 00   [19]  291 	ld	-1 (ix), #0x00
   4DF1                     292 00109$:
   4DF1 DD 7E FF      [19]  293 	ld	a, -1 (ix)
   4DF4 DD 96 06      [19]  294 	sub	a, 6 (ix)
   4DF7 D2 76 4E      [10]  295 	jp	NC, 00111$
                            296 ;src/systems/hud.c:33: digit = (u8)(value / divisor);
   4DFA C5            [11]  297 	push	bc
   4DFB C5            [11]  298 	push	bc
   4DFC DD 6E 04      [19]  299 	ld	l,4 (ix)
   4DFF DD 66 05      [19]  300 	ld	h,5 (ix)
   4E02 E5            [11]  301 	push	hl
   4E03 CD A3 5B      [17]  302 	call	__divuint
   4E06 F1            [10]  303 	pop	af
   4E07 F1            [10]  304 	pop	af
   4E08 5D            [ 4]  305 	ld	e, l
   4E09 C1            [10]  306 	pop	bc
                            307 ;src/systems/hud.c:34: value = (u16)(value % divisor);
   4E0A C5            [11]  308 	push	bc
   4E0B D5            [11]  309 	push	de
   4E0C C5            [11]  310 	push	bc
   4E0D DD 6E 04      [19]  311 	ld	l,4 (ix)
   4E10 DD 66 05      [19]  312 	ld	h,5 (ix)
   4E13 E5            [11]  313 	push	hl
   4E14 CD 2E 5D      [17]  314 	call	__moduint
   4E17 F1            [10]  315 	pop	af
   4E18 F1            [10]  316 	pop	af
   4E19 D1            [10]  317 	pop	de
   4E1A C1            [10]  318 	pop	bc
   4E1B DD 75 04      [19]  319 	ld	4 (ix), l
   4E1E DD 74 05      [19]  320 	ld	5 (ix), h
                            321 ;src/systems/hud.c:36: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4E21 DD 7E FF      [19]  322 	ld	a, -1 (ix)
   4E24 07            [ 4]  323 	rlca
   4E25 07            [ 4]  324 	rlca
   4E26 07            [ 4]  325 	rlca
   4E27 E6 F8         [ 7]  326 	and	a, #0xf8
   4E29 57            [ 4]  327 	ld	d, a
   4E2A DD 7E 07      [19]  328 	ld	a, 7 (ix)
   4E2D 82            [ 4]  329 	add	a, d
   4E2E 57            [ 4]  330 	ld	d, a
   4E2F C5            [11]  331 	push	bc
   4E30 D5            [11]  332 	push	de
   4E31 DD 7E 08      [19]  333 	ld	a, 8 (ix)
   4E34 F5            [11]  334 	push	af
   4E35 33            [ 6]  335 	inc	sp
   4E36 D5            [11]  336 	push	de
   4E37 33            [ 6]  337 	inc	sp
   4E38 21 00 C0      [10]  338 	ld	hl, #0xc000
   4E3B E5            [11]  339 	push	hl
   4E3C CD 4C 5E      [17]  340 	call	_cpct_getScreenPtr
   4E3F D1            [10]  341 	pop	de
   4E40 C1            [10]  342 	pop	bc
                            343 ;src/systems/hud.c:37: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
   4E41 E5            [11]  344 	push	hl
   4E42 C5            [11]  345 	push	bc
   4E43 7B            [ 4]  346 	ld	a, e
   4E44 F5            [11]  347 	push	af
   4E45 33            [ 6]  348 	inc	sp
   4E46 CD 0A 4D      [17]  349 	call	_hud_get_number_sprite
   4E49 33            [ 6]  350 	inc	sp
   4E4A EB            [ 4]  351 	ex	de,hl
   4E4B C1            [10]  352 	pop	bc
   4E4C E1            [10]  353 	pop	hl
   4E4D D5            [11]  354 	push	de
   4E4E FD E1         [14]  355 	pop	iy
   4E50 C5            [11]  356 	push	bc
   4E51 11 08 08      [10]  357 	ld	de, #0x0808
   4E54 D5            [11]  358 	push	de
   4E55 E5            [11]  359 	push	hl
   4E56 FD E5         [15]  360 	push	iy
   4E58 CD 7D 5C      [17]  361 	call	_cpct_drawSprite
   4E5B C1            [10]  362 	pop	bc
                            363 ;src/systems/hud.c:39: if (divisor > 1) {
   4E5C 3E 01         [ 7]  364 	ld	a, #0x01
   4E5E B9            [ 4]  365 	cp	a, c
   4E5F 3E 00         [ 7]  366 	ld	a, #0x00
   4E61 98            [ 4]  367 	sbc	a, b
   4E62 30 0C         [12]  368 	jr	NC,00110$
                            369 ;src/systems/hud.c:40: divisor /= 10;
   4E64 21 0A 00      [10]  370 	ld	hl, #0x000a
   4E67 E5            [11]  371 	push	hl
   4E68 C5            [11]  372 	push	bc
   4E69 CD A3 5B      [17]  373 	call	__divuint
   4E6C F1            [10]  374 	pop	af
   4E6D F1            [10]  375 	pop	af
   4E6E 4D            [ 4]  376 	ld	c, l
   4E6F 44            [ 4]  377 	ld	b, h
   4E70                     378 00110$:
                            379 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4E70 DD 34 FF      [23]  380 	inc	-1 (ix)
   4E73 C3 F1 4D      [10]  381 	jp	00109$
   4E76                     382 00111$:
   4E76 33            [ 6]  383 	inc	sp
   4E77 DD E1         [14]  384 	pop	ix
   4E79 C9            [10]  385 	ret
                            386 ;src/systems/hud.c:45: void hudinit(void) {
                            387 ;	---------------------------------
                            388 ; Function hudinit
                            389 ; ---------------------------------
   4E7A                     390 _hudinit::
                            391 ;src/systems/hud.c:46: currenthealth = 3;
   4E7A 21 1C 5F      [10]  392 	ld	hl,#_currenthealth + 0
   4E7D 36 03         [10]  393 	ld	(hl), #0x03
                            394 ;src/systems/hud.c:47: currentscore  = 0;
   4E7F 21 00 00      [10]  395 	ld	hl, #0x0000
   4E82 22 1D 5F      [16]  396 	ld	(_currentscore), hl
                            397 ;src/systems/hud.c:48: currenttime   = 90;
   4E85 21 1F 5F      [10]  398 	ld	hl,#_currenttime + 0
   4E88 36 5A         [10]  399 	ld	(hl), #0x5a
                            400 ;src/systems/hud.c:49: currentlives  = 3;
   4E8A 21 20 5F      [10]  401 	ld	hl,#_currentlives + 0
   4E8D 36 03         [10]  402 	ld	(hl), #0x03
                            403 ;src/systems/hud.c:50: currentweapon = 0;
   4E8F 21 21 5F      [10]  404 	ld	hl,#_currentweapon + 0
   4E92 36 00         [10]  405 	ld	(hl), #0x00
   4E94 C9            [10]  406 	ret
                            407 ;src/systems/hud.c:53: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            408 ;	---------------------------------
                            409 ; Function hudupdate
                            410 ; ---------------------------------
   4E95                     411 _hudupdate::
                            412 ;src/systems/hud.c:54: currenthealth = lives;
   4E95 21 02 00      [10]  413 	ld	hl, #2+0
   4E98 39            [11]  414 	add	hl, sp
   4E99 7E            [ 7]  415 	ld	a, (hl)
   4E9A 32 1C 5F      [13]  416 	ld	(#_currenthealth + 0),a
                            417 ;src/systems/hud.c:55: currentscore  = score;
   4E9D 21 03 00      [10]  418 	ld	hl, #3+0
   4EA0 39            [11]  419 	add	hl, sp
   4EA1 7E            [ 7]  420 	ld	a, (hl)
   4EA2 32 1D 5F      [13]  421 	ld	(#_currentscore + 0),a
   4EA5 21 04 00      [10]  422 	ld	hl, #3+1
   4EA8 39            [11]  423 	add	hl, sp
   4EA9 7E            [ 7]  424 	ld	a, (hl)
   4EAA 32 1E 5F      [13]  425 	ld	(#_currentscore + 1),a
                            426 ;src/systems/hud.c:56: currenttime   = time;
   4EAD 21 05 00      [10]  427 	ld	hl, #5+0
   4EB0 39            [11]  428 	add	hl, sp
   4EB1 7E            [ 7]  429 	ld	a, (hl)
   4EB2 32 1F 5F      [13]  430 	ld	(#_currenttime + 0),a
                            431 ;src/systems/hud.c:57: currentlives  = lives;
   4EB5 21 02 00      [10]  432 	ld	hl, #2+0
   4EB8 39            [11]  433 	add	hl, sp
   4EB9 7E            [ 7]  434 	ld	a, (hl)
   4EBA 32 20 5F      [13]  435 	ld	(#_currentlives + 0),a
                            436 ;src/systems/hud.c:58: currentweapon = weapon;
   4EBD 21 06 00      [10]  437 	ld	hl, #6+0
   4EC0 39            [11]  438 	add	hl, sp
   4EC1 7E            [ 7]  439 	ld	a, (hl)
   4EC2 32 21 5F      [13]  440 	ld	(#_currentweapon + 0),a
   4EC5 C9            [10]  441 	ret
                            442 ;src/systems/hud.c:61: void hudrender(void) {
                            443 ;	---------------------------------
                            444 ; Function hudrender
                            445 ; ---------------------------------
   4EC6                     446 _hudrender::
                            447 ;src/systems/hud.c:67: for (i = 0; i < currenthealth; ++i) {
   4EC6 0E 00         [ 7]  448 	ld	c, #0x00
   4EC8                     449 00103$:
   4EC8 21 1C 5F      [10]  450 	ld	hl, #_currenthealth
                            451 ;src/systems/hud.c:68: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4ECB 79            [ 4]  452 	ld	a,c
   4ECC BE            [ 7]  453 	cp	a,(hl)
   4ECD 30 24         [12]  454 	jr	NC,00101$
   4ECF 07            [ 4]  455 	rlca
   4ED0 07            [ 4]  456 	rlca
   4ED1 07            [ 4]  457 	rlca
   4ED2 E6 F8         [ 7]  458 	and	a, #0xf8
   4ED4 47            [ 4]  459 	ld	b, a
   4ED5 C5            [11]  460 	push	bc
   4ED6 3E 02         [ 7]  461 	ld	a, #0x02
   4ED8 F5            [11]  462 	push	af
   4ED9 33            [ 6]  463 	inc	sp
   4EDA C5            [11]  464 	push	bc
   4EDB 33            [ 6]  465 	inc	sp
   4EDC 21 00 C0      [10]  466 	ld	hl, #0xc000
   4EDF E5            [11]  467 	push	hl
   4EE0 CD 4C 5E      [17]  468 	call	_cpct_getScreenPtr
   4EE3 11 08 08      [10]  469 	ld	de, #0x0808
   4EE6 D5            [11]  470 	push	de
   4EE7 E5            [11]  471 	push	hl
   4EE8 21 4E 4D      [10]  472 	ld	hl, #_hudhealth
   4EEB E5            [11]  473 	push	hl
   4EEC CD 7D 5C      [17]  474 	call	_cpct_drawSprite
   4EEF C1            [10]  475 	pop	bc
                            476 ;src/systems/hud.c:67: for (i = 0; i < currenthealth; ++i) {
   4EF0 0C            [ 4]  477 	inc	c
   4EF1 18 D5         [12]  478 	jr	00103$
   4EF3                     479 00101$:
                            480 ;src/systems/hud.c:72: scoretemp = currentscore;
   4EF3 2A 1D 5F      [16]  481 	ld	hl, (_currentscore)
                            482 ;src/systems/hud.c:73: hud_draw_digits(scoretemp, 4, 24, 2);
   4EF6 01 18 02      [10]  483 	ld	bc, #0x0218
   4EF9 C5            [11]  484 	push	bc
   4EFA 3E 04         [ 7]  485 	ld	a, #0x04
   4EFC F5            [11]  486 	push	af
   4EFD 33            [ 6]  487 	inc	sp
   4EFE E5            [11]  488 	push	hl
   4EFF CD CE 4D      [17]  489 	call	_hud_draw_digits
   4F02 F1            [10]  490 	pop	af
   4F03 F1            [10]  491 	pop	af
   4F04 33            [ 6]  492 	inc	sp
                            493 ;src/systems/hud.c:75: timetemp = currenttime;
   4F05 21 1F 5F      [10]  494 	ld	hl,#_currenttime + 0
   4F08 4E            [ 7]  495 	ld	c, (hl)
                            496 ;src/systems/hud.c:76: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4F09 06 00         [ 7]  497 	ld	b, #0x00
   4F0B 21 38 02      [10]  498 	ld	hl, #0x0238
   4F0E E5            [11]  499 	push	hl
   4F0F 3E 03         [ 7]  500 	ld	a, #0x03
   4F11 F5            [11]  501 	push	af
   4F12 33            [ 6]  502 	inc	sp
   4F13 C5            [11]  503 	push	bc
   4F14 CD CE 4D      [17]  504 	call	_hud_draw_digits
   4F17 F1            [10]  505 	pop	af
                            506 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4F18 33            [ 6]  507 	inc	sp
   4F19 21 02 B4      [10]  508 	ld	hl,#0xb402
   4F1C E3            [19]  509 	ex	(sp),hl
   4F1D 21 00 C0      [10]  510 	ld	hl, #0xc000
   4F20 E5            [11]  511 	push	hl
   4F21 CD 4C 5E      [17]  512 	call	_cpct_getScreenPtr
                            513 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4F24 01 8E 4D      [10]  514 	ld	bc, #_hudlives+0
   4F27 11 08 08      [10]  515 	ld	de, #0x0808
   4F2A D5            [11]  516 	push	de
   4F2B E5            [11]  517 	push	hl
   4F2C C5            [11]  518 	push	bc
   4F2D CD 7D 5C      [17]  519 	call	_cpct_drawSprite
                            520 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4F30 21 0C B4      [10]  521 	ld	hl, #0xb40c
   4F33 E5            [11]  522 	push	hl
   4F34 21 00 C0      [10]  523 	ld	hl, #0xc000
   4F37 E5            [11]  524 	push	hl
   4F38 CD 4C 5E      [17]  525 	call	_cpct_getScreenPtr
                            526 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);
   4F3B E5            [11]  527 	push	hl
   4F3C 3E 0A         [ 7]  528 	ld	a, #0x0a
   4F3E F5            [11]  529 	push	af
   4F3F 33            [ 6]  530 	inc	sp
   4F40 3A 20 5F      [13]  531 	ld	a, (_currentlives)
   4F43 F5            [11]  532 	push	af
   4F44 33            [ 6]  533 	inc	sp
   4F45 CD 22 5D      [17]  534 	call	__moduchar
   4F48 F1            [10]  535 	pop	af
   4F49 55            [ 4]  536 	ld	d, l
   4F4A D5            [11]  537 	push	de
   4F4B 33            [ 6]  538 	inc	sp
   4F4C CD 0A 4D      [17]  539 	call	_hud_get_number_sprite
   4F4F 33            [ 6]  540 	inc	sp
   4F50 C1            [10]  541 	pop	bc
   4F51 11 08 08      [10]  542 	ld	de, #0x0808
   4F54 D5            [11]  543 	push	de
   4F55 C5            [11]  544 	push	bc
   4F56 E5            [11]  545 	push	hl
   4F57 CD 7D 5C      [17]  546 	call	_cpct_drawSprite
                            547 ;src/systems/hud.c:84: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4F5A 21 46 B4      [10]  548 	ld	hl, #0xb446
   4F5D E5            [11]  549 	push	hl
   4F5E 21 00 C0      [10]  550 	ld	hl, #0xc000
   4F61 E5            [11]  551 	push	hl
   4F62 CD 4C 5E      [17]  552 	call	_cpct_getScreenPtr
                            553 ;src/systems/hud.c:85: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
   4F65 E5            [11]  554 	push	hl
   4F66 3E 0A         [ 7]  555 	ld	a, #0x0a
   4F68 F5            [11]  556 	push	af
   4F69 33            [ 6]  557 	inc	sp
   4F6A 3A 21 5F      [13]  558 	ld	a, (_currentweapon)
   4F6D F5            [11]  559 	push	af
   4F6E 33            [ 6]  560 	inc	sp
   4F6F CD 22 5D      [17]  561 	call	__moduchar
   4F72 F1            [10]  562 	pop	af
   4F73 55            [ 4]  563 	ld	d, l
   4F74 D5            [11]  564 	push	de
   4F75 33            [ 6]  565 	inc	sp
   4F76 CD 0A 4D      [17]  566 	call	_hud_get_number_sprite
   4F79 33            [ 6]  567 	inc	sp
   4F7A C1            [10]  568 	pop	bc
   4F7B 11 08 08      [10]  569 	ld	de, #0x0808
   4F7E D5            [11]  570 	push	de
   4F7F C5            [11]  571 	push	bc
   4F80 E5            [11]  572 	push	hl
   4F81 CD 7D 5C      [17]  573 	call	_cpct_drawSprite
   4F84 C9            [10]  574 	ret
                            575 	.area _CODE
                            576 	.area _INITIALIZER
                            577 	.area _CABS (ABS)
