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
   5F22                      23 _currenthealth:
   5F22                      24 	.ds 1
   5F23                      25 _currentscore:
   5F23                      26 	.ds 2
   5F25                      27 _currenttime:
   5F25                      28 	.ds 1
   5F26                      29 _currentlives:
   5F26                      30 	.ds 1
   5F27                      31 _currentweapon:
   5F27                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
   5F33                      37 _hudnumbers:
   5F33                      38 	.ds 20
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
                             59 ;src/systems/hud.c:18: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                             60 ;	---------------------------------
                             61 ; Function hud_draw_digits
                             62 ; ---------------------------------
   4C9D                      63 _hud_draw_digits:
   4C9D DD E5         [15]   64 	push	ix
   4C9F DD 21 00 00   [14]   65 	ld	ix,#0
   4CA3 DD 39         [15]   66 	add	ix,sp
   4CA5 3B            [ 6]   67 	dec	sp
                             68 ;src/systems/hud.c:24: divisor = 1;
   4CA6 01 01 00      [10]   69 	ld	bc, #0x0001
                             70 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4CA9 1E 01         [ 7]   71 	ld	e, #0x01
   4CAB                      72 00106$:
   4CAB 7B            [ 4]   73 	ld	a, e
   4CAC DD 96 06      [19]   74 	sub	a, 6 (ix)
   4CAF 30 0B         [12]   75 	jr	NC,00101$
                             76 ;src/systems/hud.c:26: divisor *= 10;
   4CB1 69            [ 4]   77 	ld	l, c
   4CB2 60            [ 4]   78 	ld	h, b
   4CB3 29            [11]   79 	add	hl, hl
   4CB4 29            [11]   80 	add	hl, hl
   4CB5 09            [11]   81 	add	hl, bc
   4CB6 29            [11]   82 	add	hl, hl
   4CB7 4D            [ 4]   83 	ld	c, l
   4CB8 44            [ 4]   84 	ld	b, h
                             85 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4CB9 1C            [ 4]   86 	inc	e
   4CBA 18 EF         [12]   87 	jr	00106$
   4CBC                      88 00101$:
                             89 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4CBC DD 36 FF 00   [19]   90 	ld	-1 (ix), #0x00
   4CC0                      91 00109$:
   4CC0 DD 7E FF      [19]   92 	ld	a, -1 (ix)
   4CC3 DD 96 06      [19]   93 	sub	a, 6 (ix)
   4CC6 30 7B         [12]   94 	jr	NC,00111$
                             95 ;src/systems/hud.c:30: digit = (u8)(value / divisor);
   4CC8 C5            [11]   96 	push	bc
   4CC9 C5            [11]   97 	push	bc
   4CCA DD 6E 04      [19]   98 	ld	l,4 (ix)
   4CCD DD 66 05      [19]   99 	ld	h,5 (ix)
   4CD0 E5            [11]  100 	push	hl
   4CD1 CD F8 5B      [17]  101 	call	__divuint
   4CD4 F1            [10]  102 	pop	af
   4CD5 F1            [10]  103 	pop	af
   4CD6 5D            [ 4]  104 	ld	e, l
   4CD7 C1            [10]  105 	pop	bc
                            106 ;src/systems/hud.c:31: value = (u16)(value % divisor);
   4CD8 C5            [11]  107 	push	bc
   4CD9 D5            [11]  108 	push	de
   4CDA C5            [11]  109 	push	bc
   4CDB DD 6E 04      [19]  110 	ld	l,4 (ix)
   4CDE DD 66 05      [19]  111 	ld	h,5 (ix)
   4CE1 E5            [11]  112 	push	hl
   4CE2 CD 60 5D      [17]  113 	call	__moduint
   4CE5 F1            [10]  114 	pop	af
   4CE6 F1            [10]  115 	pop	af
   4CE7 D1            [10]  116 	pop	de
   4CE8 C1            [10]  117 	pop	bc
   4CE9 DD 75 04      [19]  118 	ld	4 (ix), l
   4CEC DD 74 05      [19]  119 	ld	5 (ix), h
                            120 ;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4CEF DD 7E FF      [19]  121 	ld	a, -1 (ix)
   4CF2 07            [ 4]  122 	rlca
   4CF3 07            [ 4]  123 	rlca
   4CF4 07            [ 4]  124 	rlca
   4CF5 E6 F8         [ 7]  125 	and	a, #0xf8
   4CF7 57            [ 4]  126 	ld	d, a
   4CF8 DD 7E 07      [19]  127 	ld	a, 7 (ix)
   4CFB 82            [ 4]  128 	add	a, d
   4CFC 57            [ 4]  129 	ld	d, a
   4CFD C5            [11]  130 	push	bc
   4CFE D5            [11]  131 	push	de
   4CFF DD 7E 08      [19]  132 	ld	a, 8 (ix)
   4D02 F5            [11]  133 	push	af
   4D03 33            [ 6]  134 	inc	sp
   4D04 D5            [11]  135 	push	de
   4D05 33            [ 6]  136 	inc	sp
   4D06 21 00 C0      [10]  137 	ld	hl, #0xc000
   4D09 E5            [11]  138 	push	hl
   4D0A CD 62 5E      [17]  139 	call	_cpct_getScreenPtr
   4D0D D1            [10]  140 	pop	de
   4D0E C1            [10]  141 	pop	bc
                            142 ;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
   4D0F E5            [11]  143 	push	hl
   4D10 FD E1         [14]  144 	pop	iy
   4D12 26 00         [ 7]  145 	ld	h, #0x00
   4D14 6B            [ 4]  146 	ld	l, e
   4D15 29            [11]  147 	add	hl, hl
   4D16 11 33 5F      [10]  148 	ld	de, #_hudnumbers
   4D19 19            [11]  149 	add	hl, de
   4D1A 5E            [ 7]  150 	ld	e, (hl)
   4D1B 23            [ 6]  151 	inc	hl
   4D1C 56            [ 7]  152 	ld	d, (hl)
   4D1D C5            [11]  153 	push	bc
   4D1E 21 08 08      [10]  154 	ld	hl, #0x0808
   4D21 E5            [11]  155 	push	hl
   4D22 FD E5         [15]  156 	push	iy
   4D24 D5            [11]  157 	push	de
   4D25 CD AF 5C      [17]  158 	call	_cpct_drawSprite
   4D28 C1            [10]  159 	pop	bc
                            160 ;src/systems/hud.c:36: if (divisor > 1) {
   4D29 3E 01         [ 7]  161 	ld	a, #0x01
   4D2B B9            [ 4]  162 	cp	a, c
   4D2C 3E 00         [ 7]  163 	ld	a, #0x00
   4D2E 98            [ 4]  164 	sbc	a, b
   4D2F 30 0C         [12]  165 	jr	NC,00110$
                            166 ;src/systems/hud.c:37: divisor /= 10;
   4D31 21 0A 00      [10]  167 	ld	hl, #0x000a
   4D34 E5            [11]  168 	push	hl
   4D35 C5            [11]  169 	push	bc
   4D36 CD F8 5B      [17]  170 	call	__divuint
   4D39 F1            [10]  171 	pop	af
   4D3A F1            [10]  172 	pop	af
   4D3B 4D            [ 4]  173 	ld	c, l
   4D3C 44            [ 4]  174 	ld	b, h
   4D3D                     175 00110$:
                            176 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4D3D DD 34 FF      [23]  177 	inc	-1 (ix)
   4D40 C3 C0 4C      [10]  178 	jp	00109$
   4D43                     179 00111$:
   4D43 33            [ 6]  180 	inc	sp
   4D44 DD E1         [14]  181 	pop	ix
   4D46 C9            [10]  182 	ret
   4D47                     183 __hud_dummy_sprite:
   4D47 00                  184 	.db #0x00	; 0
   4D48 00                  185 	.db 0x00
   4D49 00                  186 	.db 0x00
   4D4A 00                  187 	.db 0x00
   4D4B 00                  188 	.db 0x00
   4D4C 00                  189 	.db 0x00
   4D4D 00                  190 	.db 0x00
   4D4E 00                  191 	.db 0x00
   4D4F 00                  192 	.db 0x00
   4D50 00                  193 	.db 0x00
   4D51 00                  194 	.db 0x00
   4D52 00                  195 	.db 0x00
   4D53 00                  196 	.db 0x00
   4D54 00                  197 	.db 0x00
   4D55 00                  198 	.db 0x00
   4D56 00                  199 	.db 0x00
   4D57 00                  200 	.db 0x00
   4D58 00                  201 	.db 0x00
   4D59 00                  202 	.db 0x00
   4D5A 00                  203 	.db 0x00
   4D5B 00                  204 	.db 0x00
   4D5C 00                  205 	.db 0x00
   4D5D 00                  206 	.db 0x00
   4D5E 00                  207 	.db 0x00
   4D5F 00                  208 	.db 0x00
   4D60 00                  209 	.db 0x00
   4D61 00                  210 	.db 0x00
   4D62 00                  211 	.db 0x00
   4D63 00                  212 	.db 0x00
   4D64 00                  213 	.db 0x00
   4D65 00                  214 	.db 0x00
   4D66 00                  215 	.db 0x00
   4D67 00                  216 	.db 0x00
   4D68 00                  217 	.db 0x00
   4D69 00                  218 	.db 0x00
   4D6A 00                  219 	.db 0x00
   4D6B 00                  220 	.db 0x00
   4D6C 00                  221 	.db 0x00
   4D6D 00                  222 	.db 0x00
   4D6E 00                  223 	.db 0x00
   4D6F 00                  224 	.db 0x00
   4D70 00                  225 	.db 0x00
   4D71 00                  226 	.db 0x00
   4D72 00                  227 	.db 0x00
   4D73 00                  228 	.db 0x00
   4D74 00                  229 	.db 0x00
   4D75 00                  230 	.db 0x00
   4D76 00                  231 	.db 0x00
   4D77 00                  232 	.db 0x00
   4D78 00                  233 	.db 0x00
   4D79 00                  234 	.db 0x00
   4D7A 00                  235 	.db 0x00
   4D7B 00                  236 	.db 0x00
   4D7C 00                  237 	.db 0x00
   4D7D 00                  238 	.db 0x00
   4D7E 00                  239 	.db 0x00
   4D7F 00                  240 	.db 0x00
   4D80 00                  241 	.db 0x00
   4D81 00                  242 	.db 0x00
   4D82 00                  243 	.db 0x00
   4D83 00                  244 	.db 0x00
   4D84 00                  245 	.db 0x00
   4D85 00                  246 	.db 0x00
   4D86 00                  247 	.db 0x00
   4D87                     248 _hudhealth:
   4D87 00                  249 	.db #0x00	; 0
   4D88 00                  250 	.db 0x00
   4D89 00                  251 	.db 0x00
   4D8A 00                  252 	.db 0x00
   4D8B 00                  253 	.db 0x00
   4D8C 00                  254 	.db 0x00
   4D8D 00                  255 	.db 0x00
   4D8E 00                  256 	.db 0x00
   4D8F 00                  257 	.db 0x00
   4D90 00                  258 	.db 0x00
   4D91 00                  259 	.db 0x00
   4D92 00                  260 	.db 0x00
   4D93 00                  261 	.db 0x00
   4D94 00                  262 	.db 0x00
   4D95 00                  263 	.db 0x00
   4D96 00                  264 	.db 0x00
   4D97 00                  265 	.db 0x00
   4D98 00                  266 	.db 0x00
   4D99 00                  267 	.db 0x00
   4D9A 00                  268 	.db 0x00
   4D9B 00                  269 	.db 0x00
   4D9C 00                  270 	.db 0x00
   4D9D 00                  271 	.db 0x00
   4D9E 00                  272 	.db 0x00
   4D9F 00                  273 	.db 0x00
   4DA0 00                  274 	.db 0x00
   4DA1 00                  275 	.db 0x00
   4DA2 00                  276 	.db 0x00
   4DA3 00                  277 	.db 0x00
   4DA4 00                  278 	.db 0x00
   4DA5 00                  279 	.db 0x00
   4DA6 00                  280 	.db 0x00
   4DA7 00                  281 	.db 0x00
   4DA8 00                  282 	.db 0x00
   4DA9 00                  283 	.db 0x00
   4DAA 00                  284 	.db 0x00
   4DAB 00                  285 	.db 0x00
   4DAC 00                  286 	.db 0x00
   4DAD 00                  287 	.db 0x00
   4DAE 00                  288 	.db 0x00
   4DAF 00                  289 	.db 0x00
   4DB0 00                  290 	.db 0x00
   4DB1 00                  291 	.db 0x00
   4DB2 00                  292 	.db 0x00
   4DB3 00                  293 	.db 0x00
   4DB4 00                  294 	.db 0x00
   4DB5 00                  295 	.db 0x00
   4DB6 00                  296 	.db 0x00
   4DB7 00                  297 	.db 0x00
   4DB8 00                  298 	.db 0x00
   4DB9 00                  299 	.db 0x00
   4DBA 00                  300 	.db 0x00
   4DBB 00                  301 	.db 0x00
   4DBC 00                  302 	.db 0x00
   4DBD 00                  303 	.db 0x00
   4DBE 00                  304 	.db 0x00
   4DBF 00                  305 	.db 0x00
   4DC0 00                  306 	.db 0x00
   4DC1 00                  307 	.db 0x00
   4DC2 00                  308 	.db 0x00
   4DC3 00                  309 	.db 0x00
   4DC4 00                  310 	.db 0x00
   4DC5 00                  311 	.db 0x00
   4DC6 00                  312 	.db 0x00
   4DC7                     313 _hudlives:
   4DC7 00                  314 	.db #0x00	; 0
   4DC8 00                  315 	.db 0x00
   4DC9 00                  316 	.db 0x00
   4DCA 00                  317 	.db 0x00
   4DCB 00                  318 	.db 0x00
   4DCC 00                  319 	.db 0x00
   4DCD 00                  320 	.db 0x00
   4DCE 00                  321 	.db 0x00
   4DCF 00                  322 	.db 0x00
   4DD0 00                  323 	.db 0x00
   4DD1 00                  324 	.db 0x00
   4DD2 00                  325 	.db 0x00
   4DD3 00                  326 	.db 0x00
   4DD4 00                  327 	.db 0x00
   4DD5 00                  328 	.db 0x00
   4DD6 00                  329 	.db 0x00
   4DD7 00                  330 	.db 0x00
   4DD8 00                  331 	.db 0x00
   4DD9 00                  332 	.db 0x00
   4DDA 00                  333 	.db 0x00
   4DDB 00                  334 	.db 0x00
   4DDC 00                  335 	.db 0x00
   4DDD 00                  336 	.db 0x00
   4DDE 00                  337 	.db 0x00
   4DDF 00                  338 	.db 0x00
   4DE0 00                  339 	.db 0x00
   4DE1 00                  340 	.db 0x00
   4DE2 00                  341 	.db 0x00
   4DE3 00                  342 	.db 0x00
   4DE4 00                  343 	.db 0x00
   4DE5 00                  344 	.db 0x00
   4DE6 00                  345 	.db 0x00
   4DE7 00                  346 	.db 0x00
   4DE8 00                  347 	.db 0x00
   4DE9 00                  348 	.db 0x00
   4DEA 00                  349 	.db 0x00
   4DEB 00                  350 	.db 0x00
   4DEC 00                  351 	.db 0x00
   4DED 00                  352 	.db 0x00
   4DEE 00                  353 	.db 0x00
   4DEF 00                  354 	.db 0x00
   4DF0 00                  355 	.db 0x00
   4DF1 00                  356 	.db 0x00
   4DF2 00                  357 	.db 0x00
   4DF3 00                  358 	.db 0x00
   4DF4 00                  359 	.db 0x00
   4DF5 00                  360 	.db 0x00
   4DF6 00                  361 	.db 0x00
   4DF7 00                  362 	.db 0x00
   4DF8 00                  363 	.db 0x00
   4DF9 00                  364 	.db 0x00
   4DFA 00                  365 	.db 0x00
   4DFB 00                  366 	.db 0x00
   4DFC 00                  367 	.db 0x00
   4DFD 00                  368 	.db 0x00
   4DFE 00                  369 	.db 0x00
   4DFF 00                  370 	.db 0x00
   4E00 00                  371 	.db 0x00
   4E01 00                  372 	.db 0x00
   4E02 00                  373 	.db 0x00
   4E03 00                  374 	.db 0x00
   4E04 00                  375 	.db 0x00
   4E05 00                  376 	.db 0x00
   4E06 00                  377 	.db 0x00
                            378 ;src/systems/hud.c:42: void hudinit(void) {
                            379 ;	---------------------------------
                            380 ; Function hudinit
                            381 ; ---------------------------------
   4E07                     382 _hudinit::
                            383 ;src/systems/hud.c:43: currenthealth = 3;
   4E07 21 22 5F      [10]  384 	ld	hl,#_currenthealth + 0
   4E0A 36 03         [10]  385 	ld	(hl), #0x03
                            386 ;src/systems/hud.c:44: currentscore  = 0;
   4E0C 21 00 00      [10]  387 	ld	hl, #0x0000
   4E0F 22 23 5F      [16]  388 	ld	(_currentscore), hl
                            389 ;src/systems/hud.c:45: currenttime   = 90;
   4E12 21 25 5F      [10]  390 	ld	hl,#_currenttime + 0
   4E15 36 5A         [10]  391 	ld	(hl), #0x5a
                            392 ;src/systems/hud.c:46: currentlives  = 3;
   4E17 21 26 5F      [10]  393 	ld	hl,#_currentlives + 0
   4E1A 36 03         [10]  394 	ld	(hl), #0x03
                            395 ;src/systems/hud.c:47: currentweapon = 0;
   4E1C 21 27 5F      [10]  396 	ld	hl,#_currentweapon + 0
   4E1F 36 00         [10]  397 	ld	(hl), #0x00
   4E21 C9            [10]  398 	ret
                            399 ;src/systems/hud.c:50: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            400 ;	---------------------------------
                            401 ; Function hudupdate
                            402 ; ---------------------------------
   4E22                     403 _hudupdate::
                            404 ;src/systems/hud.c:51: currenthealth = lives;
   4E22 21 02 00      [10]  405 	ld	hl, #2+0
   4E25 39            [11]  406 	add	hl, sp
   4E26 7E            [ 7]  407 	ld	a, (hl)
   4E27 32 22 5F      [13]  408 	ld	(#_currenthealth + 0),a
                            409 ;src/systems/hud.c:52: currentscore  = score;
   4E2A 21 03 00      [10]  410 	ld	hl, #3+0
   4E2D 39            [11]  411 	add	hl, sp
   4E2E 7E            [ 7]  412 	ld	a, (hl)
   4E2F 32 23 5F      [13]  413 	ld	(#_currentscore + 0),a
   4E32 21 04 00      [10]  414 	ld	hl, #3+1
   4E35 39            [11]  415 	add	hl, sp
   4E36 7E            [ 7]  416 	ld	a, (hl)
   4E37 32 24 5F      [13]  417 	ld	(#_currentscore + 1),a
                            418 ;src/systems/hud.c:53: currenttime   = time;
   4E3A 21 05 00      [10]  419 	ld	hl, #5+0
   4E3D 39            [11]  420 	add	hl, sp
   4E3E 7E            [ 7]  421 	ld	a, (hl)
   4E3F 32 25 5F      [13]  422 	ld	(#_currenttime + 0),a
                            423 ;src/systems/hud.c:54: currentlives  = lives;
   4E42 21 02 00      [10]  424 	ld	hl, #2+0
   4E45 39            [11]  425 	add	hl, sp
   4E46 7E            [ 7]  426 	ld	a, (hl)
   4E47 32 26 5F      [13]  427 	ld	(#_currentlives + 0),a
                            428 ;src/systems/hud.c:55: currentweapon = weapon;
   4E4A 21 06 00      [10]  429 	ld	hl, #6+0
   4E4D 39            [11]  430 	add	hl, sp
   4E4E 7E            [ 7]  431 	ld	a, (hl)
   4E4F 32 27 5F      [13]  432 	ld	(#_currentweapon + 0),a
   4E52 C9            [10]  433 	ret
                            434 ;src/systems/hud.c:58: void hudrender(void) {
                            435 ;	---------------------------------
                            436 ; Function hudrender
                            437 ; ---------------------------------
   4E53                     438 _hudrender::
                            439 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4E53 0E 00         [ 7]  440 	ld	c, #0x00
   4E55                     441 00103$:
   4E55 21 22 5F      [10]  442 	ld	hl, #_currenthealth
                            443 ;src/systems/hud.c:65: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);
   4E58 79            [ 4]  444 	ld	a,c
   4E59 BE            [ 7]  445 	cp	a,(hl)
   4E5A 30 26         [12]  446 	jr	NC,00101$
   4E5C 07            [ 4]  447 	rlca
   4E5D 07            [ 4]  448 	rlca
   4E5E 07            [ 4]  449 	rlca
   4E5F E6 F8         [ 7]  450 	and	a, #0xf8
   4E61 47            [ 4]  451 	ld	b, a
   4E62 04            [ 4]  452 	inc	b
   4E63 04            [ 4]  453 	inc	b
   4E64 C5            [11]  454 	push	bc
   4E65 3E 02         [ 7]  455 	ld	a, #0x02
   4E67 F5            [11]  456 	push	af
   4E68 33            [ 6]  457 	inc	sp
   4E69 C5            [11]  458 	push	bc
   4E6A 33            [ 6]  459 	inc	sp
   4E6B 21 00 C0      [10]  460 	ld	hl, #0xc000
   4E6E E5            [11]  461 	push	hl
   4E6F CD 62 5E      [17]  462 	call	_cpct_getScreenPtr
   4E72 11 08 08      [10]  463 	ld	de, #0x0808
   4E75 D5            [11]  464 	push	de
   4E76 E5            [11]  465 	push	hl
   4E77 21 87 4D      [10]  466 	ld	hl, #_hudhealth
   4E7A E5            [11]  467 	push	hl
   4E7B CD AF 5C      [17]  468 	call	_cpct_drawSprite
   4E7E C1            [10]  469 	pop	bc
                            470 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4E7F 0C            [ 4]  471 	inc	c
   4E80 18 D3         [12]  472 	jr	00103$
   4E82                     473 00101$:
                            474 ;src/systems/hud.c:69: scoretemp = currentscore;
   4E82 2A 23 5F      [16]  475 	ld	hl, (_currentscore)
                            476 ;src/systems/hud.c:70: hud_draw_digits(scoretemp, 5, 88, 2);
   4E85 01 58 02      [10]  477 	ld	bc, #0x0258
   4E88 C5            [11]  478 	push	bc
   4E89 3E 05         [ 7]  479 	ld	a, #0x05
   4E8B F5            [11]  480 	push	af
   4E8C 33            [ 6]  481 	inc	sp
   4E8D E5            [11]  482 	push	hl
   4E8E CD 9D 4C      [17]  483 	call	_hud_draw_digits
   4E91 F1            [10]  484 	pop	af
   4E92 F1            [10]  485 	pop	af
   4E93 33            [ 6]  486 	inc	sp
                            487 ;src/systems/hud.c:72: timetemp = currenttime;
   4E94 21 25 5F      [10]  488 	ld	hl,#_currenttime + 0
   4E97 4E            [ 7]  489 	ld	c, (hl)
                            490 ;src/systems/hud.c:73: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4E98 06 00         [ 7]  491 	ld	b, #0x00
   4E9A 21 38 02      [10]  492 	ld	hl, #0x0238
   4E9D E5            [11]  493 	push	hl
   4E9E 3E 03         [ 7]  494 	ld	a, #0x03
   4EA0 F5            [11]  495 	push	af
   4EA1 33            [ 6]  496 	inc	sp
   4EA2 C5            [11]  497 	push	bc
   4EA3 CD 9D 4C      [17]  498 	call	_hud_draw_digits
   4EA6 F1            [10]  499 	pop	af
                            500 ;src/systems/hud.c:75: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4EA7 33            [ 6]  501 	inc	sp
   4EA8 21 02 B4      [10]  502 	ld	hl,#0xb402
   4EAB E3            [19]  503 	ex	(sp),hl
   4EAC 21 00 C0      [10]  504 	ld	hl, #0xc000
   4EAF E5            [11]  505 	push	hl
   4EB0 CD 62 5E      [17]  506 	call	_cpct_getScreenPtr
                            507 ;src/systems/hud.c:76: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4EB3 01 C7 4D      [10]  508 	ld	bc, #_hudlives+0
   4EB6 11 08 08      [10]  509 	ld	de, #0x0808
   4EB9 D5            [11]  510 	push	de
   4EBA E5            [11]  511 	push	hl
   4EBB C5            [11]  512 	push	bc
   4EBC CD AF 5C      [17]  513 	call	_cpct_drawSprite
                            514 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4EBF 21 0C B4      [10]  515 	ld	hl, #0xb40c
   4EC2 E5            [11]  516 	push	hl
   4EC3 21 00 C0      [10]  517 	ld	hl, #0xc000
   4EC6 E5            [11]  518 	push	hl
   4EC7 CD 62 5E      [17]  519 	call	_cpct_getScreenPtr
                            520 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
   4ECA E5            [11]  521 	push	hl
   4ECB 3E 0A         [ 7]  522 	ld	a, #0x0a
   4ECD F5            [11]  523 	push	af
   4ECE 33            [ 6]  524 	inc	sp
   4ECF 3A 26 5F      [13]  525 	ld	a, (_currentlives)
   4ED2 F5            [11]  526 	push	af
   4ED3 33            [ 6]  527 	inc	sp
   4ED4 CD 54 5D      [17]  528 	call	__moduchar
   4ED7 F1            [10]  529 	pop	af
   4ED8 C1            [10]  530 	pop	bc
   4ED9 26 00         [ 7]  531 	ld	h, #0x00
   4EDB 29            [11]  532 	add	hl, hl
   4EDC 11 33 5F      [10]  533 	ld	de, #_hudnumbers
   4EDF 19            [11]  534 	add	hl, de
   4EE0 5E            [ 7]  535 	ld	e, (hl)
   4EE1 23            [ 6]  536 	inc	hl
   4EE2 56            [ 7]  537 	ld	d, (hl)
   4EE3 21 08 08      [10]  538 	ld	hl, #0x0808
   4EE6 E5            [11]  539 	push	hl
   4EE7 C5            [11]  540 	push	bc
   4EE8 D5            [11]  541 	push	de
   4EE9 CD AF 5C      [17]  542 	call	_cpct_drawSprite
                            543 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4EEC 21 46 B4      [10]  544 	ld	hl, #0xb446
   4EEF E5            [11]  545 	push	hl
   4EF0 21 00 C0      [10]  546 	ld	hl, #0xc000
   4EF3 E5            [11]  547 	push	hl
   4EF4 CD 62 5E      [17]  548 	call	_cpct_getScreenPtr
                            549 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);
   4EF7 E5            [11]  550 	push	hl
   4EF8 3E 0A         [ 7]  551 	ld	a, #0x0a
   4EFA F5            [11]  552 	push	af
   4EFB 33            [ 6]  553 	inc	sp
   4EFC 3A 27 5F      [13]  554 	ld	a, (_currentweapon)
   4EFF F5            [11]  555 	push	af
   4F00 33            [ 6]  556 	inc	sp
   4F01 CD 54 5D      [17]  557 	call	__moduchar
   4F04 F1            [10]  558 	pop	af
   4F05 C1            [10]  559 	pop	bc
   4F06 26 00         [ 7]  560 	ld	h, #0x00
   4F08 29            [11]  561 	add	hl, hl
   4F09 11 33 5F      [10]  562 	ld	de, #_hudnumbers
   4F0C 19            [11]  563 	add	hl, de
   4F0D 5E            [ 7]  564 	ld	e, (hl)
   4F0E 23            [ 6]  565 	inc	hl
   4F0F 56            [ 7]  566 	ld	d, (hl)
   4F10 21 08 08      [10]  567 	ld	hl, #0x0808
   4F13 E5            [11]  568 	push	hl
   4F14 C5            [11]  569 	push	bc
   4F15 D5            [11]  570 	push	de
   4F16 CD AF 5C      [17]  571 	call	_cpct_drawSprite
   4F19 C9            [10]  572 	ret
                            573 	.area _CODE
                            574 	.area _INITIALIZER
   5F4E                     575 __xinit__hudnumbers:
   5F4E 47 4D               576 	.dw __hud_dummy_sprite
   5F50 47 4D               577 	.dw __hud_dummy_sprite
   5F52 47 4D               578 	.dw __hud_dummy_sprite
   5F54 47 4D               579 	.dw __hud_dummy_sprite
   5F56 47 4D               580 	.dw __hud_dummy_sprite
   5F58 47 4D               581 	.dw __hud_dummy_sprite
   5F5A 47 4D               582 	.dw __hud_dummy_sprite
   5F5C 47 4D               583 	.dw __hud_dummy_sprite
   5F5E 47 4D               584 	.dw __hud_dummy_sprite
   5F60 47 4D               585 	.dw __hud_dummy_sprite
                            586 	.area _CABS (ABS)
