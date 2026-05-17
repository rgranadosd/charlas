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
   5F4E                      23 _currenthealth:
   5F4E                      24 	.ds 1
   5F4F                      25 _currentscore:
   5F4F                      26 	.ds 2
   5F51                      27 _currenttime:
   5F51                      28 	.ds 1
   5F52                      29 _currentlives:
   5F52                      30 	.ds 1
   5F53                      31 _currentweapon:
   5F53                      32 	.ds 1
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
   4D23                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:18: return _hud_dummy_sprite;
   4D23 21 27 4D      [10]   63 	ld	hl, #__hud_dummy_sprite
   4D26 C9            [10]   64 	ret
   4D27                      65 __hud_dummy_sprite:
   4D27 00                   66 	.db #0x00	; 0
   4D28 00                   67 	.db 0x00
   4D29 00                   68 	.db 0x00
   4D2A 00                   69 	.db 0x00
   4D2B 00                   70 	.db 0x00
   4D2C 00                   71 	.db 0x00
   4D2D 00                   72 	.db 0x00
   4D2E 00                   73 	.db 0x00
   4D2F 00                   74 	.db 0x00
   4D30 00                   75 	.db 0x00
   4D31 00                   76 	.db 0x00
   4D32 00                   77 	.db 0x00
   4D33 00                   78 	.db 0x00
   4D34 00                   79 	.db 0x00
   4D35 00                   80 	.db 0x00
   4D36 00                   81 	.db 0x00
   4D37 00                   82 	.db 0x00
   4D38 00                   83 	.db 0x00
   4D39 00                   84 	.db 0x00
   4D3A 00                   85 	.db 0x00
   4D3B 00                   86 	.db 0x00
   4D3C 00                   87 	.db 0x00
   4D3D 00                   88 	.db 0x00
   4D3E 00                   89 	.db 0x00
   4D3F 00                   90 	.db 0x00
   4D40 00                   91 	.db 0x00
   4D41 00                   92 	.db 0x00
   4D42 00                   93 	.db 0x00
   4D43 00                   94 	.db 0x00
   4D44 00                   95 	.db 0x00
   4D45 00                   96 	.db 0x00
   4D46 00                   97 	.db 0x00
   4D47 00                   98 	.db 0x00
   4D48 00                   99 	.db 0x00
   4D49 00                  100 	.db 0x00
   4D4A 00                  101 	.db 0x00
   4D4B 00                  102 	.db 0x00
   4D4C 00                  103 	.db 0x00
   4D4D 00                  104 	.db 0x00
   4D4E 00                  105 	.db 0x00
   4D4F 00                  106 	.db 0x00
   4D50 00                  107 	.db 0x00
   4D51 00                  108 	.db 0x00
   4D52 00                  109 	.db 0x00
   4D53 00                  110 	.db 0x00
   4D54 00                  111 	.db 0x00
   4D55 00                  112 	.db 0x00
   4D56 00                  113 	.db 0x00
   4D57 00                  114 	.db 0x00
   4D58 00                  115 	.db 0x00
   4D59 00                  116 	.db 0x00
   4D5A 00                  117 	.db 0x00
   4D5B 00                  118 	.db 0x00
   4D5C 00                  119 	.db 0x00
   4D5D 00                  120 	.db 0x00
   4D5E 00                  121 	.db 0x00
   4D5F 00                  122 	.db 0x00
   4D60 00                  123 	.db 0x00
   4D61 00                  124 	.db 0x00
   4D62 00                  125 	.db 0x00
   4D63 00                  126 	.db 0x00
   4D64 00                  127 	.db 0x00
   4D65 00                  128 	.db 0x00
   4D66 00                  129 	.db 0x00
   4D67                     130 _hudhealth:
   4D67 00                  131 	.db #0x00	; 0
   4D68 00                  132 	.db 0x00
   4D69 00                  133 	.db 0x00
   4D6A 00                  134 	.db 0x00
   4D6B 00                  135 	.db 0x00
   4D6C 00                  136 	.db 0x00
   4D6D 00                  137 	.db 0x00
   4D6E 00                  138 	.db 0x00
   4D6F 00                  139 	.db 0x00
   4D70 00                  140 	.db 0x00
   4D71 00                  141 	.db 0x00
   4D72 00                  142 	.db 0x00
   4D73 00                  143 	.db 0x00
   4D74 00                  144 	.db 0x00
   4D75 00                  145 	.db 0x00
   4D76 00                  146 	.db 0x00
   4D77 00                  147 	.db 0x00
   4D78 00                  148 	.db 0x00
   4D79 00                  149 	.db 0x00
   4D7A 00                  150 	.db 0x00
   4D7B 00                  151 	.db 0x00
   4D7C 00                  152 	.db 0x00
   4D7D 00                  153 	.db 0x00
   4D7E 00                  154 	.db 0x00
   4D7F 00                  155 	.db 0x00
   4D80 00                  156 	.db 0x00
   4D81 00                  157 	.db 0x00
   4D82 00                  158 	.db 0x00
   4D83 00                  159 	.db 0x00
   4D84 00                  160 	.db 0x00
   4D85 00                  161 	.db 0x00
   4D86 00                  162 	.db 0x00
   4D87 00                  163 	.db 0x00
   4D88 00                  164 	.db 0x00
   4D89 00                  165 	.db 0x00
   4D8A 00                  166 	.db 0x00
   4D8B 00                  167 	.db 0x00
   4D8C 00                  168 	.db 0x00
   4D8D 00                  169 	.db 0x00
   4D8E 00                  170 	.db 0x00
   4D8F 00                  171 	.db 0x00
   4D90 00                  172 	.db 0x00
   4D91 00                  173 	.db 0x00
   4D92 00                  174 	.db 0x00
   4D93 00                  175 	.db 0x00
   4D94 00                  176 	.db 0x00
   4D95 00                  177 	.db 0x00
   4D96 00                  178 	.db 0x00
   4D97 00                  179 	.db 0x00
   4D98 00                  180 	.db 0x00
   4D99 00                  181 	.db 0x00
   4D9A 00                  182 	.db 0x00
   4D9B 00                  183 	.db 0x00
   4D9C 00                  184 	.db 0x00
   4D9D 00                  185 	.db 0x00
   4D9E 00                  186 	.db 0x00
   4D9F 00                  187 	.db 0x00
   4DA0 00                  188 	.db 0x00
   4DA1 00                  189 	.db 0x00
   4DA2 00                  190 	.db 0x00
   4DA3 00                  191 	.db 0x00
   4DA4 00                  192 	.db 0x00
   4DA5 00                  193 	.db 0x00
   4DA6 00                  194 	.db 0x00
   4DA7                     195 _hudlives:
   4DA7 00                  196 	.db #0x00	; 0
   4DA8 00                  197 	.db 0x00
   4DA9 00                  198 	.db 0x00
   4DAA 00                  199 	.db 0x00
   4DAB 00                  200 	.db 0x00
   4DAC 00                  201 	.db 0x00
   4DAD 00                  202 	.db 0x00
   4DAE 00                  203 	.db 0x00
   4DAF 00                  204 	.db 0x00
   4DB0 00                  205 	.db 0x00
   4DB1 00                  206 	.db 0x00
   4DB2 00                  207 	.db 0x00
   4DB3 00                  208 	.db 0x00
   4DB4 00                  209 	.db 0x00
   4DB5 00                  210 	.db 0x00
   4DB6 00                  211 	.db 0x00
   4DB7 00                  212 	.db 0x00
   4DB8 00                  213 	.db 0x00
   4DB9 00                  214 	.db 0x00
   4DBA 00                  215 	.db 0x00
   4DBB 00                  216 	.db 0x00
   4DBC 00                  217 	.db 0x00
   4DBD 00                  218 	.db 0x00
   4DBE 00                  219 	.db 0x00
   4DBF 00                  220 	.db 0x00
   4DC0 00                  221 	.db 0x00
   4DC1 00                  222 	.db 0x00
   4DC2 00                  223 	.db 0x00
   4DC3 00                  224 	.db 0x00
   4DC4 00                  225 	.db 0x00
   4DC5 00                  226 	.db 0x00
   4DC6 00                  227 	.db 0x00
   4DC7 00                  228 	.db 0x00
   4DC8 00                  229 	.db 0x00
   4DC9 00                  230 	.db 0x00
   4DCA 00                  231 	.db 0x00
   4DCB 00                  232 	.db 0x00
   4DCC 00                  233 	.db 0x00
   4DCD 00                  234 	.db 0x00
   4DCE 00                  235 	.db 0x00
   4DCF 00                  236 	.db 0x00
   4DD0 00                  237 	.db 0x00
   4DD1 00                  238 	.db 0x00
   4DD2 00                  239 	.db 0x00
   4DD3 00                  240 	.db 0x00
   4DD4 00                  241 	.db 0x00
   4DD5 00                  242 	.db 0x00
   4DD6 00                  243 	.db 0x00
   4DD7 00                  244 	.db 0x00
   4DD8 00                  245 	.db 0x00
   4DD9 00                  246 	.db 0x00
   4DDA 00                  247 	.db 0x00
   4DDB 00                  248 	.db 0x00
   4DDC 00                  249 	.db 0x00
   4DDD 00                  250 	.db 0x00
   4DDE 00                  251 	.db 0x00
   4DDF 00                  252 	.db 0x00
   4DE0 00                  253 	.db 0x00
   4DE1 00                  254 	.db 0x00
   4DE2 00                  255 	.db 0x00
   4DE3 00                  256 	.db 0x00
   4DE4 00                  257 	.db 0x00
   4DE5 00                  258 	.db 0x00
   4DE6 00                  259 	.db 0x00
                            260 ;src/systems/hud.c:21: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            261 ;	---------------------------------
                            262 ; Function hud_draw_digits
                            263 ; ---------------------------------
   4DE7                     264 _hud_draw_digits:
   4DE7 DD E5         [15]  265 	push	ix
   4DE9 DD 21 00 00   [14]  266 	ld	ix,#0
   4DED DD 39         [15]  267 	add	ix,sp
   4DEF 3B            [ 6]  268 	dec	sp
                            269 ;src/systems/hud.c:27: divisor = 1;
   4DF0 01 01 00      [10]  270 	ld	bc, #0x0001
                            271 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4DF3 1E 01         [ 7]  272 	ld	e, #0x01
   4DF5                     273 00106$:
   4DF5 7B            [ 4]  274 	ld	a, e
   4DF6 DD 96 06      [19]  275 	sub	a, 6 (ix)
   4DF9 30 0B         [12]  276 	jr	NC,00101$
                            277 ;src/systems/hud.c:29: divisor *= 10;
   4DFB 69            [ 4]  278 	ld	l, c
   4DFC 60            [ 4]  279 	ld	h, b
   4DFD 29            [11]  280 	add	hl, hl
   4DFE 29            [11]  281 	add	hl, hl
   4DFF 09            [11]  282 	add	hl, bc
   4E00 29            [11]  283 	add	hl, hl
   4E01 4D            [ 4]  284 	ld	c, l
   4E02 44            [ 4]  285 	ld	b, h
                            286 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4E03 1C            [ 4]  287 	inc	e
   4E04 18 EF         [12]  288 	jr	00106$
   4E06                     289 00101$:
                            290 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4E06 DD 36 FF 00   [19]  291 	ld	-1 (ix), #0x00
   4E0A                     292 00109$:
   4E0A DD 7E FF      [19]  293 	ld	a, -1 (ix)
   4E0D DD 96 06      [19]  294 	sub	a, 6 (ix)
   4E10 D2 8F 4E      [10]  295 	jp	NC, 00111$
                            296 ;src/systems/hud.c:33: digit = (u8)(value / divisor);
   4E13 C5            [11]  297 	push	bc
   4E14 C5            [11]  298 	push	bc
   4E15 DD 6E 04      [19]  299 	ld	l,4 (ix)
   4E18 DD 66 05      [19]  300 	ld	h,5 (ix)
   4E1B E5            [11]  301 	push	hl
   4E1C CD D5 5B      [17]  302 	call	__divuint
   4E1F F1            [10]  303 	pop	af
   4E20 F1            [10]  304 	pop	af
   4E21 5D            [ 4]  305 	ld	e, l
   4E22 C1            [10]  306 	pop	bc
                            307 ;src/systems/hud.c:34: value = (u16)(value % divisor);
   4E23 C5            [11]  308 	push	bc
   4E24 D5            [11]  309 	push	de
   4E25 C5            [11]  310 	push	bc
   4E26 DD 6E 04      [19]  311 	ld	l,4 (ix)
   4E29 DD 66 05      [19]  312 	ld	h,5 (ix)
   4E2C E5            [11]  313 	push	hl
   4E2D CD 60 5D      [17]  314 	call	__moduint
   4E30 F1            [10]  315 	pop	af
   4E31 F1            [10]  316 	pop	af
   4E32 D1            [10]  317 	pop	de
   4E33 C1            [10]  318 	pop	bc
   4E34 DD 75 04      [19]  319 	ld	4 (ix), l
   4E37 DD 74 05      [19]  320 	ld	5 (ix), h
                            321 ;src/systems/hud.c:36: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4E3A DD 7E FF      [19]  322 	ld	a, -1 (ix)
   4E3D 07            [ 4]  323 	rlca
   4E3E 07            [ 4]  324 	rlca
   4E3F 07            [ 4]  325 	rlca
   4E40 E6 F8         [ 7]  326 	and	a, #0xf8
   4E42 57            [ 4]  327 	ld	d, a
   4E43 DD 7E 07      [19]  328 	ld	a, 7 (ix)
   4E46 82            [ 4]  329 	add	a, d
   4E47 57            [ 4]  330 	ld	d, a
   4E48 C5            [11]  331 	push	bc
   4E49 D5            [11]  332 	push	de
   4E4A DD 7E 08      [19]  333 	ld	a, 8 (ix)
   4E4D F5            [11]  334 	push	af
   4E4E 33            [ 6]  335 	inc	sp
   4E4F D5            [11]  336 	push	de
   4E50 33            [ 6]  337 	inc	sp
   4E51 21 00 C0      [10]  338 	ld	hl, #0xc000
   4E54 E5            [11]  339 	push	hl
   4E55 CD 7E 5E      [17]  340 	call	_cpct_getScreenPtr
   4E58 D1            [10]  341 	pop	de
   4E59 C1            [10]  342 	pop	bc
                            343 ;src/systems/hud.c:37: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
   4E5A E5            [11]  344 	push	hl
   4E5B C5            [11]  345 	push	bc
   4E5C 7B            [ 4]  346 	ld	a, e
   4E5D F5            [11]  347 	push	af
   4E5E 33            [ 6]  348 	inc	sp
   4E5F CD 23 4D      [17]  349 	call	_hud_get_number_sprite
   4E62 33            [ 6]  350 	inc	sp
   4E63 EB            [ 4]  351 	ex	de,hl
   4E64 C1            [10]  352 	pop	bc
   4E65 E1            [10]  353 	pop	hl
   4E66 D5            [11]  354 	push	de
   4E67 FD E1         [14]  355 	pop	iy
   4E69 C5            [11]  356 	push	bc
   4E6A 11 08 08      [10]  357 	ld	de, #0x0808
   4E6D D5            [11]  358 	push	de
   4E6E E5            [11]  359 	push	hl
   4E6F FD E5         [15]  360 	push	iy
   4E71 CD AF 5C      [17]  361 	call	_cpct_drawSprite
   4E74 C1            [10]  362 	pop	bc
                            363 ;src/systems/hud.c:39: if (divisor > 1) {
   4E75 3E 01         [ 7]  364 	ld	a, #0x01
   4E77 B9            [ 4]  365 	cp	a, c
   4E78 3E 00         [ 7]  366 	ld	a, #0x00
   4E7A 98            [ 4]  367 	sbc	a, b
   4E7B 30 0C         [12]  368 	jr	NC,00110$
                            369 ;src/systems/hud.c:40: divisor /= 10;
   4E7D 21 0A 00      [10]  370 	ld	hl, #0x000a
   4E80 E5            [11]  371 	push	hl
   4E81 C5            [11]  372 	push	bc
   4E82 CD D5 5B      [17]  373 	call	__divuint
   4E85 F1            [10]  374 	pop	af
   4E86 F1            [10]  375 	pop	af
   4E87 4D            [ 4]  376 	ld	c, l
   4E88 44            [ 4]  377 	ld	b, h
   4E89                     378 00110$:
                            379 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4E89 DD 34 FF      [23]  380 	inc	-1 (ix)
   4E8C C3 0A 4E      [10]  381 	jp	00109$
   4E8F                     382 00111$:
   4E8F 33            [ 6]  383 	inc	sp
   4E90 DD E1         [14]  384 	pop	ix
   4E92 C9            [10]  385 	ret
                            386 ;src/systems/hud.c:45: void hudinit(void) {
                            387 ;	---------------------------------
                            388 ; Function hudinit
                            389 ; ---------------------------------
   4E93                     390 _hudinit::
                            391 ;src/systems/hud.c:46: currenthealth = 3;
   4E93 21 4E 5F      [10]  392 	ld	hl,#_currenthealth + 0
   4E96 36 03         [10]  393 	ld	(hl), #0x03
                            394 ;src/systems/hud.c:47: currentscore  = 0;
   4E98 21 00 00      [10]  395 	ld	hl, #0x0000
   4E9B 22 4F 5F      [16]  396 	ld	(_currentscore), hl
                            397 ;src/systems/hud.c:48: currenttime   = 90;
   4E9E 21 51 5F      [10]  398 	ld	hl,#_currenttime + 0
   4EA1 36 5A         [10]  399 	ld	(hl), #0x5a
                            400 ;src/systems/hud.c:49: currentlives  = 3;
   4EA3 21 52 5F      [10]  401 	ld	hl,#_currentlives + 0
   4EA6 36 03         [10]  402 	ld	(hl), #0x03
                            403 ;src/systems/hud.c:50: currentweapon = 0;
   4EA8 21 53 5F      [10]  404 	ld	hl,#_currentweapon + 0
   4EAB 36 00         [10]  405 	ld	(hl), #0x00
   4EAD C9            [10]  406 	ret
                            407 ;src/systems/hud.c:53: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            408 ;	---------------------------------
                            409 ; Function hudupdate
                            410 ; ---------------------------------
   4EAE                     411 _hudupdate::
                            412 ;src/systems/hud.c:54: currenthealth = lives;
   4EAE 21 02 00      [10]  413 	ld	hl, #2+0
   4EB1 39            [11]  414 	add	hl, sp
   4EB2 7E            [ 7]  415 	ld	a, (hl)
   4EB3 32 4E 5F      [13]  416 	ld	(#_currenthealth + 0),a
                            417 ;src/systems/hud.c:55: currentscore  = score;
   4EB6 21 03 00      [10]  418 	ld	hl, #3+0
   4EB9 39            [11]  419 	add	hl, sp
   4EBA 7E            [ 7]  420 	ld	a, (hl)
   4EBB 32 4F 5F      [13]  421 	ld	(#_currentscore + 0),a
   4EBE 21 04 00      [10]  422 	ld	hl, #3+1
   4EC1 39            [11]  423 	add	hl, sp
   4EC2 7E            [ 7]  424 	ld	a, (hl)
   4EC3 32 50 5F      [13]  425 	ld	(#_currentscore + 1),a
                            426 ;src/systems/hud.c:56: currenttime   = time;
   4EC6 21 05 00      [10]  427 	ld	hl, #5+0
   4EC9 39            [11]  428 	add	hl, sp
   4ECA 7E            [ 7]  429 	ld	a, (hl)
   4ECB 32 51 5F      [13]  430 	ld	(#_currenttime + 0),a
                            431 ;src/systems/hud.c:57: currentlives  = lives;
   4ECE 21 02 00      [10]  432 	ld	hl, #2+0
   4ED1 39            [11]  433 	add	hl, sp
   4ED2 7E            [ 7]  434 	ld	a, (hl)
   4ED3 32 52 5F      [13]  435 	ld	(#_currentlives + 0),a
                            436 ;src/systems/hud.c:58: currentweapon = weapon;
   4ED6 21 06 00      [10]  437 	ld	hl, #6+0
   4ED9 39            [11]  438 	add	hl, sp
   4EDA 7E            [ 7]  439 	ld	a, (hl)
   4EDB 32 53 5F      [13]  440 	ld	(#_currentweapon + 0),a
   4EDE C9            [10]  441 	ret
                            442 ;src/systems/hud.c:61: void hudrender(void) {
                            443 ;	---------------------------------
                            444 ; Function hudrender
                            445 ; ---------------------------------
   4EDF                     446 _hudrender::
                            447 ;src/systems/hud.c:67: for (i = 0; i < currenthealth; ++i) {
   4EDF 0E 00         [ 7]  448 	ld	c, #0x00
   4EE1                     449 00103$:
   4EE1 21 4E 5F      [10]  450 	ld	hl, #_currenthealth
                            451 ;src/systems/hud.c:68: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4EE4 79            [ 4]  452 	ld	a,c
   4EE5 BE            [ 7]  453 	cp	a,(hl)
   4EE6 30 24         [12]  454 	jr	NC,00101$
   4EE8 07            [ 4]  455 	rlca
   4EE9 07            [ 4]  456 	rlca
   4EEA 07            [ 4]  457 	rlca
   4EEB E6 F8         [ 7]  458 	and	a, #0xf8
   4EED 47            [ 4]  459 	ld	b, a
   4EEE C5            [11]  460 	push	bc
   4EEF 3E 02         [ 7]  461 	ld	a, #0x02
   4EF1 F5            [11]  462 	push	af
   4EF2 33            [ 6]  463 	inc	sp
   4EF3 C5            [11]  464 	push	bc
   4EF4 33            [ 6]  465 	inc	sp
   4EF5 21 00 C0      [10]  466 	ld	hl, #0xc000
   4EF8 E5            [11]  467 	push	hl
   4EF9 CD 7E 5E      [17]  468 	call	_cpct_getScreenPtr
   4EFC 11 08 08      [10]  469 	ld	de, #0x0808
   4EFF D5            [11]  470 	push	de
   4F00 E5            [11]  471 	push	hl
   4F01 21 67 4D      [10]  472 	ld	hl, #_hudhealth
   4F04 E5            [11]  473 	push	hl
   4F05 CD AF 5C      [17]  474 	call	_cpct_drawSprite
   4F08 C1            [10]  475 	pop	bc
                            476 ;src/systems/hud.c:67: for (i = 0; i < currenthealth; ++i) {
   4F09 0C            [ 4]  477 	inc	c
   4F0A 18 D5         [12]  478 	jr	00103$
   4F0C                     479 00101$:
                            480 ;src/systems/hud.c:72: scoretemp = currentscore;
   4F0C 2A 4F 5F      [16]  481 	ld	hl, (_currentscore)
                            482 ;src/systems/hud.c:73: hud_draw_digits(scoretemp, 4, 24, 2);
   4F0F 01 18 02      [10]  483 	ld	bc, #0x0218
   4F12 C5            [11]  484 	push	bc
   4F13 3E 04         [ 7]  485 	ld	a, #0x04
   4F15 F5            [11]  486 	push	af
   4F16 33            [ 6]  487 	inc	sp
   4F17 E5            [11]  488 	push	hl
   4F18 CD E7 4D      [17]  489 	call	_hud_draw_digits
   4F1B F1            [10]  490 	pop	af
   4F1C F1            [10]  491 	pop	af
   4F1D 33            [ 6]  492 	inc	sp
                            493 ;src/systems/hud.c:75: timetemp = currenttime;
   4F1E 21 51 5F      [10]  494 	ld	hl,#_currenttime + 0
   4F21 4E            [ 7]  495 	ld	c, (hl)
                            496 ;src/systems/hud.c:76: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4F22 06 00         [ 7]  497 	ld	b, #0x00
   4F24 21 38 02      [10]  498 	ld	hl, #0x0238
   4F27 E5            [11]  499 	push	hl
   4F28 3E 03         [ 7]  500 	ld	a, #0x03
   4F2A F5            [11]  501 	push	af
   4F2B 33            [ 6]  502 	inc	sp
   4F2C C5            [11]  503 	push	bc
   4F2D CD E7 4D      [17]  504 	call	_hud_draw_digits
   4F30 F1            [10]  505 	pop	af
                            506 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4F31 33            [ 6]  507 	inc	sp
   4F32 21 02 B4      [10]  508 	ld	hl,#0xb402
   4F35 E3            [19]  509 	ex	(sp),hl
   4F36 21 00 C0      [10]  510 	ld	hl, #0xc000
   4F39 E5            [11]  511 	push	hl
   4F3A CD 7E 5E      [17]  512 	call	_cpct_getScreenPtr
                            513 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4F3D 01 A7 4D      [10]  514 	ld	bc, #_hudlives+0
   4F40 11 08 08      [10]  515 	ld	de, #0x0808
   4F43 D5            [11]  516 	push	de
   4F44 E5            [11]  517 	push	hl
   4F45 C5            [11]  518 	push	bc
   4F46 CD AF 5C      [17]  519 	call	_cpct_drawSprite
                            520 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4F49 21 0C B4      [10]  521 	ld	hl, #0xb40c
   4F4C E5            [11]  522 	push	hl
   4F4D 21 00 C0      [10]  523 	ld	hl, #0xc000
   4F50 E5            [11]  524 	push	hl
   4F51 CD 7E 5E      [17]  525 	call	_cpct_getScreenPtr
                            526 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);
   4F54 E5            [11]  527 	push	hl
   4F55 3E 0A         [ 7]  528 	ld	a, #0x0a
   4F57 F5            [11]  529 	push	af
   4F58 33            [ 6]  530 	inc	sp
   4F59 3A 52 5F      [13]  531 	ld	a, (_currentlives)
   4F5C F5            [11]  532 	push	af
   4F5D 33            [ 6]  533 	inc	sp
   4F5E CD 54 5D      [17]  534 	call	__moduchar
   4F61 F1            [10]  535 	pop	af
   4F62 55            [ 4]  536 	ld	d, l
   4F63 D5            [11]  537 	push	de
   4F64 33            [ 6]  538 	inc	sp
   4F65 CD 23 4D      [17]  539 	call	_hud_get_number_sprite
   4F68 33            [ 6]  540 	inc	sp
   4F69 C1            [10]  541 	pop	bc
   4F6A 11 08 08      [10]  542 	ld	de, #0x0808
   4F6D D5            [11]  543 	push	de
   4F6E C5            [11]  544 	push	bc
   4F6F E5            [11]  545 	push	hl
   4F70 CD AF 5C      [17]  546 	call	_cpct_drawSprite
                            547 ;src/systems/hud.c:84: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4F73 21 46 B4      [10]  548 	ld	hl, #0xb446
   4F76 E5            [11]  549 	push	hl
   4F77 21 00 C0      [10]  550 	ld	hl, #0xc000
   4F7A E5            [11]  551 	push	hl
   4F7B CD 7E 5E      [17]  552 	call	_cpct_getScreenPtr
                            553 ;src/systems/hud.c:85: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
   4F7E E5            [11]  554 	push	hl
   4F7F 3E 0A         [ 7]  555 	ld	a, #0x0a
   4F81 F5            [11]  556 	push	af
   4F82 33            [ 6]  557 	inc	sp
   4F83 3A 53 5F      [13]  558 	ld	a, (_currentweapon)
   4F86 F5            [11]  559 	push	af
   4F87 33            [ 6]  560 	inc	sp
   4F88 CD 54 5D      [17]  561 	call	__moduchar
   4F8B F1            [10]  562 	pop	af
   4F8C 55            [ 4]  563 	ld	d, l
   4F8D D5            [11]  564 	push	de
   4F8E 33            [ 6]  565 	inc	sp
   4F8F CD 23 4D      [17]  566 	call	_hud_get_number_sprite
   4F92 33            [ 6]  567 	inc	sp
   4F93 C1            [10]  568 	pop	bc
   4F94 11 08 08      [10]  569 	ld	de, #0x0808
   4F97 D5            [11]  570 	push	de
   4F98 C5            [11]  571 	push	bc
   4F99 E5            [11]  572 	push	hl
   4F9A CD AF 5C      [17]  573 	call	_cpct_drawSprite
   4F9D C9            [10]  574 	ret
                            575 	.area _CODE
                            576 	.area _INITIALIZER
                            577 	.area _CABS (ABS)
