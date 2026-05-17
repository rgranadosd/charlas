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
   5F32                      23 _currenthealth:
   5F32                      24 	.ds 1
   5F33                      25 _currentscore:
   5F33                      26 	.ds 2
   5F35                      27 _currenttime:
   5F35                      28 	.ds 1
   5F36                      29 _currentlives:
   5F36                      30 	.ds 1
   5F37                      31 _currentweapon:
   5F37                      32 	.ds 1
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
   4D21                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:18: return _hud_dummy_sprite;
   4D21 21 25 4D      [10]   63 	ld	hl, #__hud_dummy_sprite
   4D24 C9            [10]   64 	ret
   4D25                      65 __hud_dummy_sprite:
   4D25 00                   66 	.db #0x00	; 0
   4D26 00                   67 	.db 0x00
   4D27 00                   68 	.db 0x00
   4D28 00                   69 	.db 0x00
   4D29 00                   70 	.db 0x00
   4D2A 00                   71 	.db 0x00
   4D2B 00                   72 	.db 0x00
   4D2C 00                   73 	.db 0x00
   4D2D 00                   74 	.db 0x00
   4D2E 00                   75 	.db 0x00
   4D2F 00                   76 	.db 0x00
   4D30 00                   77 	.db 0x00
   4D31 00                   78 	.db 0x00
   4D32 00                   79 	.db 0x00
   4D33 00                   80 	.db 0x00
   4D34 00                   81 	.db 0x00
   4D35 00                   82 	.db 0x00
   4D36 00                   83 	.db 0x00
   4D37 00                   84 	.db 0x00
   4D38 00                   85 	.db 0x00
   4D39 00                   86 	.db 0x00
   4D3A 00                   87 	.db 0x00
   4D3B 00                   88 	.db 0x00
   4D3C 00                   89 	.db 0x00
   4D3D 00                   90 	.db 0x00
   4D3E 00                   91 	.db 0x00
   4D3F 00                   92 	.db 0x00
   4D40 00                   93 	.db 0x00
   4D41 00                   94 	.db 0x00
   4D42 00                   95 	.db 0x00
   4D43 00                   96 	.db 0x00
   4D44 00                   97 	.db 0x00
   4D45 00                   98 	.db 0x00
   4D46 00                   99 	.db 0x00
   4D47 00                  100 	.db 0x00
   4D48 00                  101 	.db 0x00
   4D49 00                  102 	.db 0x00
   4D4A 00                  103 	.db 0x00
   4D4B 00                  104 	.db 0x00
   4D4C 00                  105 	.db 0x00
   4D4D 00                  106 	.db 0x00
   4D4E 00                  107 	.db 0x00
   4D4F 00                  108 	.db 0x00
   4D50 00                  109 	.db 0x00
   4D51 00                  110 	.db 0x00
   4D52 00                  111 	.db 0x00
   4D53 00                  112 	.db 0x00
   4D54 00                  113 	.db 0x00
   4D55 00                  114 	.db 0x00
   4D56 00                  115 	.db 0x00
   4D57 00                  116 	.db 0x00
   4D58 00                  117 	.db 0x00
   4D59 00                  118 	.db 0x00
   4D5A 00                  119 	.db 0x00
   4D5B 00                  120 	.db 0x00
   4D5C 00                  121 	.db 0x00
   4D5D 00                  122 	.db 0x00
   4D5E 00                  123 	.db 0x00
   4D5F 00                  124 	.db 0x00
   4D60 00                  125 	.db 0x00
   4D61 00                  126 	.db 0x00
   4D62 00                  127 	.db 0x00
   4D63 00                  128 	.db 0x00
   4D64 00                  129 	.db 0x00
   4D65                     130 _hudhealth:
   4D65 00                  131 	.db #0x00	; 0
   4D66 00                  132 	.db 0x00
   4D67 00                  133 	.db 0x00
   4D68 00                  134 	.db 0x00
   4D69 00                  135 	.db 0x00
   4D6A 00                  136 	.db 0x00
   4D6B 00                  137 	.db 0x00
   4D6C 00                  138 	.db 0x00
   4D6D 00                  139 	.db 0x00
   4D6E 00                  140 	.db 0x00
   4D6F 00                  141 	.db 0x00
   4D70 00                  142 	.db 0x00
   4D71 00                  143 	.db 0x00
   4D72 00                  144 	.db 0x00
   4D73 00                  145 	.db 0x00
   4D74 00                  146 	.db 0x00
   4D75 00                  147 	.db 0x00
   4D76 00                  148 	.db 0x00
   4D77 00                  149 	.db 0x00
   4D78 00                  150 	.db 0x00
   4D79 00                  151 	.db 0x00
   4D7A 00                  152 	.db 0x00
   4D7B 00                  153 	.db 0x00
   4D7C 00                  154 	.db 0x00
   4D7D 00                  155 	.db 0x00
   4D7E 00                  156 	.db 0x00
   4D7F 00                  157 	.db 0x00
   4D80 00                  158 	.db 0x00
   4D81 00                  159 	.db 0x00
   4D82 00                  160 	.db 0x00
   4D83 00                  161 	.db 0x00
   4D84 00                  162 	.db 0x00
   4D85 00                  163 	.db 0x00
   4D86 00                  164 	.db 0x00
   4D87 00                  165 	.db 0x00
   4D88 00                  166 	.db 0x00
   4D89 00                  167 	.db 0x00
   4D8A 00                  168 	.db 0x00
   4D8B 00                  169 	.db 0x00
   4D8C 00                  170 	.db 0x00
   4D8D 00                  171 	.db 0x00
   4D8E 00                  172 	.db 0x00
   4D8F 00                  173 	.db 0x00
   4D90 00                  174 	.db 0x00
   4D91 00                  175 	.db 0x00
   4D92 00                  176 	.db 0x00
   4D93 00                  177 	.db 0x00
   4D94 00                  178 	.db 0x00
   4D95 00                  179 	.db 0x00
   4D96 00                  180 	.db 0x00
   4D97 00                  181 	.db 0x00
   4D98 00                  182 	.db 0x00
   4D99 00                  183 	.db 0x00
   4D9A 00                  184 	.db 0x00
   4D9B 00                  185 	.db 0x00
   4D9C 00                  186 	.db 0x00
   4D9D 00                  187 	.db 0x00
   4D9E 00                  188 	.db 0x00
   4D9F 00                  189 	.db 0x00
   4DA0 00                  190 	.db 0x00
   4DA1 00                  191 	.db 0x00
   4DA2 00                  192 	.db 0x00
   4DA3 00                  193 	.db 0x00
   4DA4 00                  194 	.db 0x00
   4DA5                     195 _hudlives:
   4DA5 00                  196 	.db #0x00	; 0
   4DA6 00                  197 	.db 0x00
   4DA7 00                  198 	.db 0x00
   4DA8 00                  199 	.db 0x00
   4DA9 00                  200 	.db 0x00
   4DAA 00                  201 	.db 0x00
   4DAB 00                  202 	.db 0x00
   4DAC 00                  203 	.db 0x00
   4DAD 00                  204 	.db 0x00
   4DAE 00                  205 	.db 0x00
   4DAF 00                  206 	.db 0x00
   4DB0 00                  207 	.db 0x00
   4DB1 00                  208 	.db 0x00
   4DB2 00                  209 	.db 0x00
   4DB3 00                  210 	.db 0x00
   4DB4 00                  211 	.db 0x00
   4DB5 00                  212 	.db 0x00
   4DB6 00                  213 	.db 0x00
   4DB7 00                  214 	.db 0x00
   4DB8 00                  215 	.db 0x00
   4DB9 00                  216 	.db 0x00
   4DBA 00                  217 	.db 0x00
   4DBB 00                  218 	.db 0x00
   4DBC 00                  219 	.db 0x00
   4DBD 00                  220 	.db 0x00
   4DBE 00                  221 	.db 0x00
   4DBF 00                  222 	.db 0x00
   4DC0 00                  223 	.db 0x00
   4DC1 00                  224 	.db 0x00
   4DC2 00                  225 	.db 0x00
   4DC3 00                  226 	.db 0x00
   4DC4 00                  227 	.db 0x00
   4DC5 00                  228 	.db 0x00
   4DC6 00                  229 	.db 0x00
   4DC7 00                  230 	.db 0x00
   4DC8 00                  231 	.db 0x00
   4DC9 00                  232 	.db 0x00
   4DCA 00                  233 	.db 0x00
   4DCB 00                  234 	.db 0x00
   4DCC 00                  235 	.db 0x00
   4DCD 00                  236 	.db 0x00
   4DCE 00                  237 	.db 0x00
   4DCF 00                  238 	.db 0x00
   4DD0 00                  239 	.db 0x00
   4DD1 00                  240 	.db 0x00
   4DD2 00                  241 	.db 0x00
   4DD3 00                  242 	.db 0x00
   4DD4 00                  243 	.db 0x00
   4DD5 00                  244 	.db 0x00
   4DD6 00                  245 	.db 0x00
   4DD7 00                  246 	.db 0x00
   4DD8 00                  247 	.db 0x00
   4DD9 00                  248 	.db 0x00
   4DDA 00                  249 	.db 0x00
   4DDB 00                  250 	.db 0x00
   4DDC 00                  251 	.db 0x00
   4DDD 00                  252 	.db 0x00
   4DDE 00                  253 	.db 0x00
   4DDF 00                  254 	.db 0x00
   4DE0 00                  255 	.db 0x00
   4DE1 00                  256 	.db 0x00
   4DE2 00                  257 	.db 0x00
   4DE3 00                  258 	.db 0x00
   4DE4 00                  259 	.db 0x00
                            260 ;src/systems/hud.c:21: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            261 ;	---------------------------------
                            262 ; Function hud_draw_digits
                            263 ; ---------------------------------
   4DE5                     264 _hud_draw_digits:
   4DE5 DD E5         [15]  265 	push	ix
   4DE7 DD 21 00 00   [14]  266 	ld	ix,#0
   4DEB DD 39         [15]  267 	add	ix,sp
   4DED 3B            [ 6]  268 	dec	sp
                            269 ;src/systems/hud.c:27: divisor = 1;
   4DEE 01 01 00      [10]  270 	ld	bc, #0x0001
                            271 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4DF1 1E 01         [ 7]  272 	ld	e, #0x01
   4DF3                     273 00106$:
   4DF3 7B            [ 4]  274 	ld	a, e
   4DF4 DD 96 06      [19]  275 	sub	a, 6 (ix)
   4DF7 30 0B         [12]  276 	jr	NC,00101$
                            277 ;src/systems/hud.c:29: divisor *= 10;
   4DF9 69            [ 4]  278 	ld	l, c
   4DFA 60            [ 4]  279 	ld	h, b
   4DFB 29            [11]  280 	add	hl, hl
   4DFC 29            [11]  281 	add	hl, hl
   4DFD 09            [11]  282 	add	hl, bc
   4DFE 29            [11]  283 	add	hl, hl
   4DFF 4D            [ 4]  284 	ld	c, l
   4E00 44            [ 4]  285 	ld	b, h
                            286 ;src/systems/hud.c:28: for (i = 1; i < digits; ++i) {
   4E01 1C            [ 4]  287 	inc	e
   4E02 18 EF         [12]  288 	jr	00106$
   4E04                     289 00101$:
                            290 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4E04 DD 36 FF 00   [19]  291 	ld	-1 (ix), #0x00
   4E08                     292 00109$:
   4E08 DD 7E FF      [19]  293 	ld	a, -1 (ix)
   4E0B DD 96 06      [19]  294 	sub	a, 6 (ix)
   4E0E D2 8D 4E      [10]  295 	jp	NC, 00111$
                            296 ;src/systems/hud.c:33: digit = (u8)(value / divisor);
   4E11 C5            [11]  297 	push	bc
   4E12 C5            [11]  298 	push	bc
   4E13 DD 6E 04      [19]  299 	ld	l,4 (ix)
   4E16 DD 66 05      [19]  300 	ld	h,5 (ix)
   4E19 E5            [11]  301 	push	hl
   4E1A CD B9 5B      [17]  302 	call	__divuint
   4E1D F1            [10]  303 	pop	af
   4E1E F1            [10]  304 	pop	af
   4E1F 5D            [ 4]  305 	ld	e, l
   4E20 C1            [10]  306 	pop	bc
                            307 ;src/systems/hud.c:34: value = (u16)(value % divisor);
   4E21 C5            [11]  308 	push	bc
   4E22 D5            [11]  309 	push	de
   4E23 C5            [11]  310 	push	bc
   4E24 DD 6E 04      [19]  311 	ld	l,4 (ix)
   4E27 DD 66 05      [19]  312 	ld	h,5 (ix)
   4E2A E5            [11]  313 	push	hl
   4E2B CD 44 5D      [17]  314 	call	__moduint
   4E2E F1            [10]  315 	pop	af
   4E2F F1            [10]  316 	pop	af
   4E30 D1            [10]  317 	pop	de
   4E31 C1            [10]  318 	pop	bc
   4E32 DD 75 04      [19]  319 	ld	4 (ix), l
   4E35 DD 74 05      [19]  320 	ld	5 (ix), h
                            321 ;src/systems/hud.c:36: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4E38 DD 7E FF      [19]  322 	ld	a, -1 (ix)
   4E3B 07            [ 4]  323 	rlca
   4E3C 07            [ 4]  324 	rlca
   4E3D 07            [ 4]  325 	rlca
   4E3E E6 F8         [ 7]  326 	and	a, #0xf8
   4E40 57            [ 4]  327 	ld	d, a
   4E41 DD 7E 07      [19]  328 	ld	a, 7 (ix)
   4E44 82            [ 4]  329 	add	a, d
   4E45 57            [ 4]  330 	ld	d, a
   4E46 C5            [11]  331 	push	bc
   4E47 D5            [11]  332 	push	de
   4E48 DD 7E 08      [19]  333 	ld	a, 8 (ix)
   4E4B F5            [11]  334 	push	af
   4E4C 33            [ 6]  335 	inc	sp
   4E4D D5            [11]  336 	push	de
   4E4E 33            [ 6]  337 	inc	sp
   4E4F 21 00 C0      [10]  338 	ld	hl, #0xc000
   4E52 E5            [11]  339 	push	hl
   4E53 CD 62 5E      [17]  340 	call	_cpct_getScreenPtr
   4E56 D1            [10]  341 	pop	de
   4E57 C1            [10]  342 	pop	bc
                            343 ;src/systems/hud.c:37: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
   4E58 E5            [11]  344 	push	hl
   4E59 C5            [11]  345 	push	bc
   4E5A 7B            [ 4]  346 	ld	a, e
   4E5B F5            [11]  347 	push	af
   4E5C 33            [ 6]  348 	inc	sp
   4E5D CD 21 4D      [17]  349 	call	_hud_get_number_sprite
   4E60 33            [ 6]  350 	inc	sp
   4E61 EB            [ 4]  351 	ex	de,hl
   4E62 C1            [10]  352 	pop	bc
   4E63 E1            [10]  353 	pop	hl
   4E64 D5            [11]  354 	push	de
   4E65 FD E1         [14]  355 	pop	iy
   4E67 C5            [11]  356 	push	bc
   4E68 11 08 08      [10]  357 	ld	de, #0x0808
   4E6B D5            [11]  358 	push	de
   4E6C E5            [11]  359 	push	hl
   4E6D FD E5         [15]  360 	push	iy
   4E6F CD 93 5C      [17]  361 	call	_cpct_drawSprite
   4E72 C1            [10]  362 	pop	bc
                            363 ;src/systems/hud.c:39: if (divisor > 1) {
   4E73 3E 01         [ 7]  364 	ld	a, #0x01
   4E75 B9            [ 4]  365 	cp	a, c
   4E76 3E 00         [ 7]  366 	ld	a, #0x00
   4E78 98            [ 4]  367 	sbc	a, b
   4E79 30 0C         [12]  368 	jr	NC,00110$
                            369 ;src/systems/hud.c:40: divisor /= 10;
   4E7B 21 0A 00      [10]  370 	ld	hl, #0x000a
   4E7E E5            [11]  371 	push	hl
   4E7F C5            [11]  372 	push	bc
   4E80 CD B9 5B      [17]  373 	call	__divuint
   4E83 F1            [10]  374 	pop	af
   4E84 F1            [10]  375 	pop	af
   4E85 4D            [ 4]  376 	ld	c, l
   4E86 44            [ 4]  377 	ld	b, h
   4E87                     378 00110$:
                            379 ;src/systems/hud.c:32: for (i = 0; i < digits; ++i) {
   4E87 DD 34 FF      [23]  380 	inc	-1 (ix)
   4E8A C3 08 4E      [10]  381 	jp	00109$
   4E8D                     382 00111$:
   4E8D 33            [ 6]  383 	inc	sp
   4E8E DD E1         [14]  384 	pop	ix
   4E90 C9            [10]  385 	ret
                            386 ;src/systems/hud.c:45: void hudinit(void) {
                            387 ;	---------------------------------
                            388 ; Function hudinit
                            389 ; ---------------------------------
   4E91                     390 _hudinit::
                            391 ;src/systems/hud.c:46: currenthealth = 3;
   4E91 21 32 5F      [10]  392 	ld	hl,#_currenthealth + 0
   4E94 36 03         [10]  393 	ld	(hl), #0x03
                            394 ;src/systems/hud.c:47: currentscore  = 0;
   4E96 21 00 00      [10]  395 	ld	hl, #0x0000
   4E99 22 33 5F      [16]  396 	ld	(_currentscore), hl
                            397 ;src/systems/hud.c:48: currenttime   = 90;
   4E9C 21 35 5F      [10]  398 	ld	hl,#_currenttime + 0
   4E9F 36 5A         [10]  399 	ld	(hl), #0x5a
                            400 ;src/systems/hud.c:49: currentlives  = 3;
   4EA1 21 36 5F      [10]  401 	ld	hl,#_currentlives + 0
   4EA4 36 03         [10]  402 	ld	(hl), #0x03
                            403 ;src/systems/hud.c:50: currentweapon = 0;
   4EA6 21 37 5F      [10]  404 	ld	hl,#_currentweapon + 0
   4EA9 36 00         [10]  405 	ld	(hl), #0x00
   4EAB C9            [10]  406 	ret
                            407 ;src/systems/hud.c:53: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            408 ;	---------------------------------
                            409 ; Function hudupdate
                            410 ; ---------------------------------
   4EAC                     411 _hudupdate::
                            412 ;src/systems/hud.c:54: currenthealth = lives;
   4EAC 21 02 00      [10]  413 	ld	hl, #2+0
   4EAF 39            [11]  414 	add	hl, sp
   4EB0 7E            [ 7]  415 	ld	a, (hl)
   4EB1 32 32 5F      [13]  416 	ld	(#_currenthealth + 0),a
                            417 ;src/systems/hud.c:55: currentscore  = score;
   4EB4 21 03 00      [10]  418 	ld	hl, #3+0
   4EB7 39            [11]  419 	add	hl, sp
   4EB8 7E            [ 7]  420 	ld	a, (hl)
   4EB9 32 33 5F      [13]  421 	ld	(#_currentscore + 0),a
   4EBC 21 04 00      [10]  422 	ld	hl, #3+1
   4EBF 39            [11]  423 	add	hl, sp
   4EC0 7E            [ 7]  424 	ld	a, (hl)
   4EC1 32 34 5F      [13]  425 	ld	(#_currentscore + 1),a
                            426 ;src/systems/hud.c:56: currenttime   = time;
   4EC4 21 05 00      [10]  427 	ld	hl, #5+0
   4EC7 39            [11]  428 	add	hl, sp
   4EC8 7E            [ 7]  429 	ld	a, (hl)
   4EC9 32 35 5F      [13]  430 	ld	(#_currenttime + 0),a
                            431 ;src/systems/hud.c:57: currentlives  = lives;
   4ECC 21 02 00      [10]  432 	ld	hl, #2+0
   4ECF 39            [11]  433 	add	hl, sp
   4ED0 7E            [ 7]  434 	ld	a, (hl)
   4ED1 32 36 5F      [13]  435 	ld	(#_currentlives + 0),a
                            436 ;src/systems/hud.c:58: currentweapon = weapon;
   4ED4 21 06 00      [10]  437 	ld	hl, #6+0
   4ED7 39            [11]  438 	add	hl, sp
   4ED8 7E            [ 7]  439 	ld	a, (hl)
   4ED9 32 37 5F      [13]  440 	ld	(#_currentweapon + 0),a
   4EDC C9            [10]  441 	ret
                            442 ;src/systems/hud.c:61: void hudrender(void) {
                            443 ;	---------------------------------
                            444 ; Function hudrender
                            445 ; ---------------------------------
   4EDD                     446 _hudrender::
                            447 ;src/systems/hud.c:67: for (i = 0; i < currenthealth; ++i) {
   4EDD 0E 00         [ 7]  448 	ld	c, #0x00
   4EDF                     449 00103$:
   4EDF 21 32 5F      [10]  450 	ld	hl, #_currenthealth
                            451 ;src/systems/hud.c:68: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4EE2 79            [ 4]  452 	ld	a,c
   4EE3 BE            [ 7]  453 	cp	a,(hl)
   4EE4 30 24         [12]  454 	jr	NC,00101$
   4EE6 07            [ 4]  455 	rlca
   4EE7 07            [ 4]  456 	rlca
   4EE8 07            [ 4]  457 	rlca
   4EE9 E6 F8         [ 7]  458 	and	a, #0xf8
   4EEB 47            [ 4]  459 	ld	b, a
   4EEC C5            [11]  460 	push	bc
   4EED 3E 02         [ 7]  461 	ld	a, #0x02
   4EEF F5            [11]  462 	push	af
   4EF0 33            [ 6]  463 	inc	sp
   4EF1 C5            [11]  464 	push	bc
   4EF2 33            [ 6]  465 	inc	sp
   4EF3 21 00 C0      [10]  466 	ld	hl, #0xc000
   4EF6 E5            [11]  467 	push	hl
   4EF7 CD 62 5E      [17]  468 	call	_cpct_getScreenPtr
   4EFA 11 08 08      [10]  469 	ld	de, #0x0808
   4EFD D5            [11]  470 	push	de
   4EFE E5            [11]  471 	push	hl
   4EFF 21 65 4D      [10]  472 	ld	hl, #_hudhealth
   4F02 E5            [11]  473 	push	hl
   4F03 CD 93 5C      [17]  474 	call	_cpct_drawSprite
   4F06 C1            [10]  475 	pop	bc
                            476 ;src/systems/hud.c:67: for (i = 0; i < currenthealth; ++i) {
   4F07 0C            [ 4]  477 	inc	c
   4F08 18 D5         [12]  478 	jr	00103$
   4F0A                     479 00101$:
                            480 ;src/systems/hud.c:72: scoretemp = currentscore;
   4F0A 2A 33 5F      [16]  481 	ld	hl, (_currentscore)
                            482 ;src/systems/hud.c:73: hud_draw_digits(scoretemp, 4, 24, 2);
   4F0D 01 18 02      [10]  483 	ld	bc, #0x0218
   4F10 C5            [11]  484 	push	bc
   4F11 3E 04         [ 7]  485 	ld	a, #0x04
   4F13 F5            [11]  486 	push	af
   4F14 33            [ 6]  487 	inc	sp
   4F15 E5            [11]  488 	push	hl
   4F16 CD E5 4D      [17]  489 	call	_hud_draw_digits
   4F19 F1            [10]  490 	pop	af
   4F1A F1            [10]  491 	pop	af
   4F1B 33            [ 6]  492 	inc	sp
                            493 ;src/systems/hud.c:75: timetemp = currenttime;
   4F1C 21 35 5F      [10]  494 	ld	hl,#_currenttime + 0
   4F1F 4E            [ 7]  495 	ld	c, (hl)
                            496 ;src/systems/hud.c:76: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4F20 06 00         [ 7]  497 	ld	b, #0x00
   4F22 21 38 02      [10]  498 	ld	hl, #0x0238
   4F25 E5            [11]  499 	push	hl
   4F26 3E 03         [ 7]  500 	ld	a, #0x03
   4F28 F5            [11]  501 	push	af
   4F29 33            [ 6]  502 	inc	sp
   4F2A C5            [11]  503 	push	bc
   4F2B CD E5 4D      [17]  504 	call	_hud_draw_digits
   4F2E F1            [10]  505 	pop	af
                            506 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4F2F 33            [ 6]  507 	inc	sp
   4F30 21 02 B4      [10]  508 	ld	hl,#0xb402
   4F33 E3            [19]  509 	ex	(sp),hl
   4F34 21 00 C0      [10]  510 	ld	hl, #0xc000
   4F37 E5            [11]  511 	push	hl
   4F38 CD 62 5E      [17]  512 	call	_cpct_getScreenPtr
                            513 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4F3B 01 A5 4D      [10]  514 	ld	bc, #_hudlives+0
   4F3E 11 08 08      [10]  515 	ld	de, #0x0808
   4F41 D5            [11]  516 	push	de
   4F42 E5            [11]  517 	push	hl
   4F43 C5            [11]  518 	push	bc
   4F44 CD 93 5C      [17]  519 	call	_cpct_drawSprite
                            520 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4F47 21 0C B4      [10]  521 	ld	hl, #0xb40c
   4F4A E5            [11]  522 	push	hl
   4F4B 21 00 C0      [10]  523 	ld	hl, #0xc000
   4F4E E5            [11]  524 	push	hl
   4F4F CD 62 5E      [17]  525 	call	_cpct_getScreenPtr
                            526 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);
   4F52 E5            [11]  527 	push	hl
   4F53 3E 0A         [ 7]  528 	ld	a, #0x0a
   4F55 F5            [11]  529 	push	af
   4F56 33            [ 6]  530 	inc	sp
   4F57 3A 36 5F      [13]  531 	ld	a, (_currentlives)
   4F5A F5            [11]  532 	push	af
   4F5B 33            [ 6]  533 	inc	sp
   4F5C CD 38 5D      [17]  534 	call	__moduchar
   4F5F F1            [10]  535 	pop	af
   4F60 55            [ 4]  536 	ld	d, l
   4F61 D5            [11]  537 	push	de
   4F62 33            [ 6]  538 	inc	sp
   4F63 CD 21 4D      [17]  539 	call	_hud_get_number_sprite
   4F66 33            [ 6]  540 	inc	sp
   4F67 C1            [10]  541 	pop	bc
   4F68 11 08 08      [10]  542 	ld	de, #0x0808
   4F6B D5            [11]  543 	push	de
   4F6C C5            [11]  544 	push	bc
   4F6D E5            [11]  545 	push	hl
   4F6E CD 93 5C      [17]  546 	call	_cpct_drawSprite
                            547 ;src/systems/hud.c:84: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4F71 21 46 B4      [10]  548 	ld	hl, #0xb446
   4F74 E5            [11]  549 	push	hl
   4F75 21 00 C0      [10]  550 	ld	hl, #0xc000
   4F78 E5            [11]  551 	push	hl
   4F79 CD 62 5E      [17]  552 	call	_cpct_getScreenPtr
                            553 ;src/systems/hud.c:85: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
   4F7C E5            [11]  554 	push	hl
   4F7D 3E 0A         [ 7]  555 	ld	a, #0x0a
   4F7F F5            [11]  556 	push	af
   4F80 33            [ 6]  557 	inc	sp
   4F81 3A 37 5F      [13]  558 	ld	a, (_currentweapon)
   4F84 F5            [11]  559 	push	af
   4F85 33            [ 6]  560 	inc	sp
   4F86 CD 38 5D      [17]  561 	call	__moduchar
   4F89 F1            [10]  562 	pop	af
   4F8A 55            [ 4]  563 	ld	d, l
   4F8B D5            [11]  564 	push	de
   4F8C 33            [ 6]  565 	inc	sp
   4F8D CD 21 4D      [17]  566 	call	_hud_get_number_sprite
   4F90 33            [ 6]  567 	inc	sp
   4F91 C1            [10]  568 	pop	bc
   4F92 11 08 08      [10]  569 	ld	de, #0x0808
   4F95 D5            [11]  570 	push	de
   4F96 C5            [11]  571 	push	bc
   4F97 E5            [11]  572 	push	hl
   4F98 CD 93 5C      [17]  573 	call	_cpct_drawSprite
   4F9B C9            [10]  574 	ret
                            575 	.area _CODE
                            576 	.area _INITIALIZER
                            577 	.area _CABS (ABS)
