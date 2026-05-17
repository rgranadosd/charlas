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
   5F58                      23 _currenthealth:
   5F58                      24 	.ds 1
   5F59                      25 _currentscore:
   5F59                      26 	.ds 2
   5F5B                      27 _currenttime:
   5F5B                      28 	.ds 1
   5F5C                      29 _currentlives:
   5F5C                      30 	.ds 1
   5F5D                      31 _currentweapon:
   5F5D                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
   5F69                      37 _hudnumbers:
   5F69                      38 	.ds 20
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
   4CB7                      63 _hud_draw_digits:
   4CB7 DD E5         [15]   64 	push	ix
   4CB9 DD 21 00 00   [14]   65 	ld	ix,#0
   4CBD DD 39         [15]   66 	add	ix,sp
   4CBF 3B            [ 6]   67 	dec	sp
                             68 ;src/systems/hud.c:24: divisor = 1;
   4CC0 01 01 00      [10]   69 	ld	bc, #0x0001
                             70 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4CC3 1E 01         [ 7]   71 	ld	e, #0x01
   4CC5                      72 00106$:
   4CC5 7B            [ 4]   73 	ld	a, e
   4CC6 DD 96 06      [19]   74 	sub	a, 6 (ix)
   4CC9 30 0B         [12]   75 	jr	NC,00101$
                             76 ;src/systems/hud.c:26: divisor *= 10;
   4CCB 69            [ 4]   77 	ld	l, c
   4CCC 60            [ 4]   78 	ld	h, b
   4CCD 29            [11]   79 	add	hl, hl
   4CCE 29            [11]   80 	add	hl, hl
   4CCF 09            [11]   81 	add	hl, bc
   4CD0 29            [11]   82 	add	hl, hl
   4CD1 4D            [ 4]   83 	ld	c, l
   4CD2 44            [ 4]   84 	ld	b, h
                             85 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4CD3 1C            [ 4]   86 	inc	e
   4CD4 18 EF         [12]   87 	jr	00106$
   4CD6                      88 00101$:
                             89 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4CD6 DD 36 FF 00   [19]   90 	ld	-1 (ix), #0x00
   4CDA                      91 00109$:
   4CDA DD 7E FF      [19]   92 	ld	a, -1 (ix)
   4CDD DD 96 06      [19]   93 	sub	a, 6 (ix)
   4CE0 30 7B         [12]   94 	jr	NC,00111$
                             95 ;src/systems/hud.c:30: digit = (u8)(value / divisor);
   4CE2 C5            [11]   96 	push	bc
   4CE3 C5            [11]   97 	push	bc
   4CE4 DD 6E 04      [19]   98 	ld	l,4 (ix)
   4CE7 DD 66 05      [19]   99 	ld	h,5 (ix)
   4CEA E5            [11]  100 	push	hl
   4CEB CD 0B 5C      [17]  101 	call	__divuint
   4CEE F1            [10]  102 	pop	af
   4CEF F1            [10]  103 	pop	af
   4CF0 5D            [ 4]  104 	ld	e, l
   4CF1 C1            [10]  105 	pop	bc
                            106 ;src/systems/hud.c:31: value = (u16)(value % divisor);
   4CF2 C5            [11]  107 	push	bc
   4CF3 D5            [11]  108 	push	de
   4CF4 C5            [11]  109 	push	bc
   4CF5 DD 6E 04      [19]  110 	ld	l,4 (ix)
   4CF8 DD 66 05      [19]  111 	ld	h,5 (ix)
   4CFB E5            [11]  112 	push	hl
   4CFC CD 96 5D      [17]  113 	call	__moduint
   4CFF F1            [10]  114 	pop	af
   4D00 F1            [10]  115 	pop	af
   4D01 D1            [10]  116 	pop	de
   4D02 C1            [10]  117 	pop	bc
   4D03 DD 75 04      [19]  118 	ld	4 (ix), l
   4D06 DD 74 05      [19]  119 	ld	5 (ix), h
                            120 ;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4D09 DD 7E FF      [19]  121 	ld	a, -1 (ix)
   4D0C 07            [ 4]  122 	rlca
   4D0D 07            [ 4]  123 	rlca
   4D0E 07            [ 4]  124 	rlca
   4D0F E6 F8         [ 7]  125 	and	a, #0xf8
   4D11 57            [ 4]  126 	ld	d, a
   4D12 DD 7E 07      [19]  127 	ld	a, 7 (ix)
   4D15 82            [ 4]  128 	add	a, d
   4D16 57            [ 4]  129 	ld	d, a
   4D17 C5            [11]  130 	push	bc
   4D18 D5            [11]  131 	push	de
   4D19 DD 7E 08      [19]  132 	ld	a, 8 (ix)
   4D1C F5            [11]  133 	push	af
   4D1D 33            [ 6]  134 	inc	sp
   4D1E D5            [11]  135 	push	de
   4D1F 33            [ 6]  136 	inc	sp
   4D20 21 00 C0      [10]  137 	ld	hl, #0xc000
   4D23 E5            [11]  138 	push	hl
   4D24 CD 98 5E      [17]  139 	call	_cpct_getScreenPtr
   4D27 D1            [10]  140 	pop	de
   4D28 C1            [10]  141 	pop	bc
                            142 ;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
   4D29 E5            [11]  143 	push	hl
   4D2A FD E1         [14]  144 	pop	iy
   4D2C 26 00         [ 7]  145 	ld	h, #0x00
   4D2E 6B            [ 4]  146 	ld	l, e
   4D2F 29            [11]  147 	add	hl, hl
   4D30 11 69 5F      [10]  148 	ld	de, #_hudnumbers
   4D33 19            [11]  149 	add	hl, de
   4D34 5E            [ 7]  150 	ld	e, (hl)
   4D35 23            [ 6]  151 	inc	hl
   4D36 56            [ 7]  152 	ld	d, (hl)
   4D37 C5            [11]  153 	push	bc
   4D38 21 08 08      [10]  154 	ld	hl, #0x0808
   4D3B E5            [11]  155 	push	hl
   4D3C FD E5         [15]  156 	push	iy
   4D3E D5            [11]  157 	push	de
   4D3F CD E5 5C      [17]  158 	call	_cpct_drawSprite
   4D42 C1            [10]  159 	pop	bc
                            160 ;src/systems/hud.c:36: if (divisor > 1) {
   4D43 3E 01         [ 7]  161 	ld	a, #0x01
   4D45 B9            [ 4]  162 	cp	a, c
   4D46 3E 00         [ 7]  163 	ld	a, #0x00
   4D48 98            [ 4]  164 	sbc	a, b
   4D49 30 0C         [12]  165 	jr	NC,00110$
                            166 ;src/systems/hud.c:37: divisor /= 10;
   4D4B 21 0A 00      [10]  167 	ld	hl, #0x000a
   4D4E E5            [11]  168 	push	hl
   4D4F C5            [11]  169 	push	bc
   4D50 CD 0B 5C      [17]  170 	call	__divuint
   4D53 F1            [10]  171 	pop	af
   4D54 F1            [10]  172 	pop	af
   4D55 4D            [ 4]  173 	ld	c, l
   4D56 44            [ 4]  174 	ld	b, h
   4D57                     175 00110$:
                            176 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4D57 DD 34 FF      [23]  177 	inc	-1 (ix)
   4D5A C3 DA 4C      [10]  178 	jp	00109$
   4D5D                     179 00111$:
   4D5D 33            [ 6]  180 	inc	sp
   4D5E DD E1         [14]  181 	pop	ix
   4D60 C9            [10]  182 	ret
   4D61                     183 __hud_dummy_sprite:
   4D61 00                  184 	.db #0x00	; 0
   4D62 00                  185 	.db 0x00
   4D63 00                  186 	.db 0x00
   4D64 00                  187 	.db 0x00
   4D65 00                  188 	.db 0x00
   4D66 00                  189 	.db 0x00
   4D67 00                  190 	.db 0x00
   4D68 00                  191 	.db 0x00
   4D69 00                  192 	.db 0x00
   4D6A 00                  193 	.db 0x00
   4D6B 00                  194 	.db 0x00
   4D6C 00                  195 	.db 0x00
   4D6D 00                  196 	.db 0x00
   4D6E 00                  197 	.db 0x00
   4D6F 00                  198 	.db 0x00
   4D70 00                  199 	.db 0x00
   4D71 00                  200 	.db 0x00
   4D72 00                  201 	.db 0x00
   4D73 00                  202 	.db 0x00
   4D74 00                  203 	.db 0x00
   4D75 00                  204 	.db 0x00
   4D76 00                  205 	.db 0x00
   4D77 00                  206 	.db 0x00
   4D78 00                  207 	.db 0x00
   4D79 00                  208 	.db 0x00
   4D7A 00                  209 	.db 0x00
   4D7B 00                  210 	.db 0x00
   4D7C 00                  211 	.db 0x00
   4D7D 00                  212 	.db 0x00
   4D7E 00                  213 	.db 0x00
   4D7F 00                  214 	.db 0x00
   4D80 00                  215 	.db 0x00
   4D81 00                  216 	.db 0x00
   4D82 00                  217 	.db 0x00
   4D83 00                  218 	.db 0x00
   4D84 00                  219 	.db 0x00
   4D85 00                  220 	.db 0x00
   4D86 00                  221 	.db 0x00
   4D87 00                  222 	.db 0x00
   4D88 00                  223 	.db 0x00
   4D89 00                  224 	.db 0x00
   4D8A 00                  225 	.db 0x00
   4D8B 00                  226 	.db 0x00
   4D8C 00                  227 	.db 0x00
   4D8D 00                  228 	.db 0x00
   4D8E 00                  229 	.db 0x00
   4D8F 00                  230 	.db 0x00
   4D90 00                  231 	.db 0x00
   4D91 00                  232 	.db 0x00
   4D92 00                  233 	.db 0x00
   4D93 00                  234 	.db 0x00
   4D94 00                  235 	.db 0x00
   4D95 00                  236 	.db 0x00
   4D96 00                  237 	.db 0x00
   4D97 00                  238 	.db 0x00
   4D98 00                  239 	.db 0x00
   4D99 00                  240 	.db 0x00
   4D9A 00                  241 	.db 0x00
   4D9B 00                  242 	.db 0x00
   4D9C 00                  243 	.db 0x00
   4D9D 00                  244 	.db 0x00
   4D9E 00                  245 	.db 0x00
   4D9F 00                  246 	.db 0x00
   4DA0 00                  247 	.db 0x00
   4DA1                     248 _hudhealth:
   4DA1 00                  249 	.db #0x00	; 0
   4DA2 00                  250 	.db 0x00
   4DA3 00                  251 	.db 0x00
   4DA4 00                  252 	.db 0x00
   4DA5 00                  253 	.db 0x00
   4DA6 00                  254 	.db 0x00
   4DA7 00                  255 	.db 0x00
   4DA8 00                  256 	.db 0x00
   4DA9 00                  257 	.db 0x00
   4DAA 00                  258 	.db 0x00
   4DAB 00                  259 	.db 0x00
   4DAC 00                  260 	.db 0x00
   4DAD 00                  261 	.db 0x00
   4DAE 00                  262 	.db 0x00
   4DAF 00                  263 	.db 0x00
   4DB0 00                  264 	.db 0x00
   4DB1 00                  265 	.db 0x00
   4DB2 00                  266 	.db 0x00
   4DB3 00                  267 	.db 0x00
   4DB4 00                  268 	.db 0x00
   4DB5 00                  269 	.db 0x00
   4DB6 00                  270 	.db 0x00
   4DB7 00                  271 	.db 0x00
   4DB8 00                  272 	.db 0x00
   4DB9 00                  273 	.db 0x00
   4DBA 00                  274 	.db 0x00
   4DBB 00                  275 	.db 0x00
   4DBC 00                  276 	.db 0x00
   4DBD 00                  277 	.db 0x00
   4DBE 00                  278 	.db 0x00
   4DBF 00                  279 	.db 0x00
   4DC0 00                  280 	.db 0x00
   4DC1 00                  281 	.db 0x00
   4DC2 00                  282 	.db 0x00
   4DC3 00                  283 	.db 0x00
   4DC4 00                  284 	.db 0x00
   4DC5 00                  285 	.db 0x00
   4DC6 00                  286 	.db 0x00
   4DC7 00                  287 	.db 0x00
   4DC8 00                  288 	.db 0x00
   4DC9 00                  289 	.db 0x00
   4DCA 00                  290 	.db 0x00
   4DCB 00                  291 	.db 0x00
   4DCC 00                  292 	.db 0x00
   4DCD 00                  293 	.db 0x00
   4DCE 00                  294 	.db 0x00
   4DCF 00                  295 	.db 0x00
   4DD0 00                  296 	.db 0x00
   4DD1 00                  297 	.db 0x00
   4DD2 00                  298 	.db 0x00
   4DD3 00                  299 	.db 0x00
   4DD4 00                  300 	.db 0x00
   4DD5 00                  301 	.db 0x00
   4DD6 00                  302 	.db 0x00
   4DD7 00                  303 	.db 0x00
   4DD8 00                  304 	.db 0x00
   4DD9 00                  305 	.db 0x00
   4DDA 00                  306 	.db 0x00
   4DDB 00                  307 	.db 0x00
   4DDC 00                  308 	.db 0x00
   4DDD 00                  309 	.db 0x00
   4DDE 00                  310 	.db 0x00
   4DDF 00                  311 	.db 0x00
   4DE0 00                  312 	.db 0x00
   4DE1                     313 _hudlives:
   4DE1 00                  314 	.db #0x00	; 0
   4DE2 00                  315 	.db 0x00
   4DE3 00                  316 	.db 0x00
   4DE4 00                  317 	.db 0x00
   4DE5 00                  318 	.db 0x00
   4DE6 00                  319 	.db 0x00
   4DE7 00                  320 	.db 0x00
   4DE8 00                  321 	.db 0x00
   4DE9 00                  322 	.db 0x00
   4DEA 00                  323 	.db 0x00
   4DEB 00                  324 	.db 0x00
   4DEC 00                  325 	.db 0x00
   4DED 00                  326 	.db 0x00
   4DEE 00                  327 	.db 0x00
   4DEF 00                  328 	.db 0x00
   4DF0 00                  329 	.db 0x00
   4DF1 00                  330 	.db 0x00
   4DF2 00                  331 	.db 0x00
   4DF3 00                  332 	.db 0x00
   4DF4 00                  333 	.db 0x00
   4DF5 00                  334 	.db 0x00
   4DF6 00                  335 	.db 0x00
   4DF7 00                  336 	.db 0x00
   4DF8 00                  337 	.db 0x00
   4DF9 00                  338 	.db 0x00
   4DFA 00                  339 	.db 0x00
   4DFB 00                  340 	.db 0x00
   4DFC 00                  341 	.db 0x00
   4DFD 00                  342 	.db 0x00
   4DFE 00                  343 	.db 0x00
   4DFF 00                  344 	.db 0x00
   4E00 00                  345 	.db 0x00
   4E01 00                  346 	.db 0x00
   4E02 00                  347 	.db 0x00
   4E03 00                  348 	.db 0x00
   4E04 00                  349 	.db 0x00
   4E05 00                  350 	.db 0x00
   4E06 00                  351 	.db 0x00
   4E07 00                  352 	.db 0x00
   4E08 00                  353 	.db 0x00
   4E09 00                  354 	.db 0x00
   4E0A 00                  355 	.db 0x00
   4E0B 00                  356 	.db 0x00
   4E0C 00                  357 	.db 0x00
   4E0D 00                  358 	.db 0x00
   4E0E 00                  359 	.db 0x00
   4E0F 00                  360 	.db 0x00
   4E10 00                  361 	.db 0x00
   4E11 00                  362 	.db 0x00
   4E12 00                  363 	.db 0x00
   4E13 00                  364 	.db 0x00
   4E14 00                  365 	.db 0x00
   4E15 00                  366 	.db 0x00
   4E16 00                  367 	.db 0x00
   4E17 00                  368 	.db 0x00
   4E18 00                  369 	.db 0x00
   4E19 00                  370 	.db 0x00
   4E1A 00                  371 	.db 0x00
   4E1B 00                  372 	.db 0x00
   4E1C 00                  373 	.db 0x00
   4E1D 00                  374 	.db 0x00
   4E1E 00                  375 	.db 0x00
   4E1F 00                  376 	.db 0x00
   4E20 00                  377 	.db 0x00
                            378 ;src/systems/hud.c:42: void hudinit(void) {
                            379 ;	---------------------------------
                            380 ; Function hudinit
                            381 ; ---------------------------------
   4E21                     382 _hudinit::
                            383 ;src/systems/hud.c:43: currenthealth = 3;
   4E21 21 58 5F      [10]  384 	ld	hl,#_currenthealth + 0
   4E24 36 03         [10]  385 	ld	(hl), #0x03
                            386 ;src/systems/hud.c:44: currentscore  = 0;
   4E26 21 00 00      [10]  387 	ld	hl, #0x0000
   4E29 22 59 5F      [16]  388 	ld	(_currentscore), hl
                            389 ;src/systems/hud.c:45: currenttime   = 90;
   4E2C 21 5B 5F      [10]  390 	ld	hl,#_currenttime + 0
   4E2F 36 5A         [10]  391 	ld	(hl), #0x5a
                            392 ;src/systems/hud.c:46: currentlives  = 3;
   4E31 21 5C 5F      [10]  393 	ld	hl,#_currentlives + 0
   4E34 36 03         [10]  394 	ld	(hl), #0x03
                            395 ;src/systems/hud.c:47: currentweapon = 0;
   4E36 21 5D 5F      [10]  396 	ld	hl,#_currentweapon + 0
   4E39 36 00         [10]  397 	ld	(hl), #0x00
   4E3B C9            [10]  398 	ret
                            399 ;src/systems/hud.c:50: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            400 ;	---------------------------------
                            401 ; Function hudupdate
                            402 ; ---------------------------------
   4E3C                     403 _hudupdate::
                            404 ;src/systems/hud.c:51: currenthealth = lives;
   4E3C 21 02 00      [10]  405 	ld	hl, #2+0
   4E3F 39            [11]  406 	add	hl, sp
   4E40 7E            [ 7]  407 	ld	a, (hl)
   4E41 32 58 5F      [13]  408 	ld	(#_currenthealth + 0),a
                            409 ;src/systems/hud.c:52: currentscore  = score;
   4E44 21 03 00      [10]  410 	ld	hl, #3+0
   4E47 39            [11]  411 	add	hl, sp
   4E48 7E            [ 7]  412 	ld	a, (hl)
   4E49 32 59 5F      [13]  413 	ld	(#_currentscore + 0),a
   4E4C 21 04 00      [10]  414 	ld	hl, #3+1
   4E4F 39            [11]  415 	add	hl, sp
   4E50 7E            [ 7]  416 	ld	a, (hl)
   4E51 32 5A 5F      [13]  417 	ld	(#_currentscore + 1),a
                            418 ;src/systems/hud.c:53: currenttime   = time;
   4E54 21 05 00      [10]  419 	ld	hl, #5+0
   4E57 39            [11]  420 	add	hl, sp
   4E58 7E            [ 7]  421 	ld	a, (hl)
   4E59 32 5B 5F      [13]  422 	ld	(#_currenttime + 0),a
                            423 ;src/systems/hud.c:54: currentlives  = lives;
   4E5C 21 02 00      [10]  424 	ld	hl, #2+0
   4E5F 39            [11]  425 	add	hl, sp
   4E60 7E            [ 7]  426 	ld	a, (hl)
   4E61 32 5C 5F      [13]  427 	ld	(#_currentlives + 0),a
                            428 ;src/systems/hud.c:55: currentweapon = weapon;
   4E64 21 06 00      [10]  429 	ld	hl, #6+0
   4E67 39            [11]  430 	add	hl, sp
   4E68 7E            [ 7]  431 	ld	a, (hl)
   4E69 32 5D 5F      [13]  432 	ld	(#_currentweapon + 0),a
   4E6C C9            [10]  433 	ret
                            434 ;src/systems/hud.c:58: void hudrender(void) {
                            435 ;	---------------------------------
                            436 ; Function hudrender
                            437 ; ---------------------------------
   4E6D                     438 _hudrender::
                            439 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4E6D 0E 00         [ 7]  440 	ld	c, #0x00
   4E6F                     441 00103$:
   4E6F 21 58 5F      [10]  442 	ld	hl, #_currenthealth
                            443 ;src/systems/hud.c:65: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4E72 79            [ 4]  444 	ld	a,c
   4E73 BE            [ 7]  445 	cp	a,(hl)
   4E74 30 24         [12]  446 	jr	NC,00101$
   4E76 07            [ 4]  447 	rlca
   4E77 07            [ 4]  448 	rlca
   4E78 07            [ 4]  449 	rlca
   4E79 E6 F8         [ 7]  450 	and	a, #0xf8
   4E7B 47            [ 4]  451 	ld	b, a
   4E7C C5            [11]  452 	push	bc
   4E7D 3E 02         [ 7]  453 	ld	a, #0x02
   4E7F F5            [11]  454 	push	af
   4E80 33            [ 6]  455 	inc	sp
   4E81 C5            [11]  456 	push	bc
   4E82 33            [ 6]  457 	inc	sp
   4E83 21 00 C0      [10]  458 	ld	hl, #0xc000
   4E86 E5            [11]  459 	push	hl
   4E87 CD 98 5E      [17]  460 	call	_cpct_getScreenPtr
   4E8A 11 08 08      [10]  461 	ld	de, #0x0808
   4E8D D5            [11]  462 	push	de
   4E8E E5            [11]  463 	push	hl
   4E8F 21 A1 4D      [10]  464 	ld	hl, #_hudhealth
   4E92 E5            [11]  465 	push	hl
   4E93 CD E5 5C      [17]  466 	call	_cpct_drawSprite
   4E96 C1            [10]  467 	pop	bc
                            468 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4E97 0C            [ 4]  469 	inc	c
   4E98 18 D5         [12]  470 	jr	00103$
   4E9A                     471 00101$:
                            472 ;src/systems/hud.c:69: scoretemp = currentscore;
   4E9A 2A 59 5F      [16]  473 	ld	hl, (_currentscore)
                            474 ;src/systems/hud.c:70: hud_draw_digits(scoretemp, 4, 24, 2);
   4E9D 01 18 02      [10]  475 	ld	bc, #0x0218
   4EA0 C5            [11]  476 	push	bc
   4EA1 3E 04         [ 7]  477 	ld	a, #0x04
   4EA3 F5            [11]  478 	push	af
   4EA4 33            [ 6]  479 	inc	sp
   4EA5 E5            [11]  480 	push	hl
   4EA6 CD B7 4C      [17]  481 	call	_hud_draw_digits
   4EA9 F1            [10]  482 	pop	af
   4EAA F1            [10]  483 	pop	af
   4EAB 33            [ 6]  484 	inc	sp
                            485 ;src/systems/hud.c:72: timetemp = currenttime;
   4EAC 21 5B 5F      [10]  486 	ld	hl,#_currenttime + 0
   4EAF 4E            [ 7]  487 	ld	c, (hl)
                            488 ;src/systems/hud.c:73: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4EB0 06 00         [ 7]  489 	ld	b, #0x00
   4EB2 21 38 02      [10]  490 	ld	hl, #0x0238
   4EB5 E5            [11]  491 	push	hl
   4EB6 3E 03         [ 7]  492 	ld	a, #0x03
   4EB8 F5            [11]  493 	push	af
   4EB9 33            [ 6]  494 	inc	sp
   4EBA C5            [11]  495 	push	bc
   4EBB CD B7 4C      [17]  496 	call	_hud_draw_digits
   4EBE F1            [10]  497 	pop	af
                            498 ;src/systems/hud.c:75: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4EBF 33            [ 6]  499 	inc	sp
   4EC0 21 02 B4      [10]  500 	ld	hl,#0xb402
   4EC3 E3            [19]  501 	ex	(sp),hl
   4EC4 21 00 C0      [10]  502 	ld	hl, #0xc000
   4EC7 E5            [11]  503 	push	hl
   4EC8 CD 98 5E      [17]  504 	call	_cpct_getScreenPtr
                            505 ;src/systems/hud.c:76: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4ECB 01 E1 4D      [10]  506 	ld	bc, #_hudlives+0
   4ECE 11 08 08      [10]  507 	ld	de, #0x0808
   4ED1 D5            [11]  508 	push	de
   4ED2 E5            [11]  509 	push	hl
   4ED3 C5            [11]  510 	push	bc
   4ED4 CD E5 5C      [17]  511 	call	_cpct_drawSprite
                            512 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4ED7 21 0C B4      [10]  513 	ld	hl, #0xb40c
   4EDA E5            [11]  514 	push	hl
   4EDB 21 00 C0      [10]  515 	ld	hl, #0xc000
   4EDE E5            [11]  516 	push	hl
   4EDF CD 98 5E      [17]  517 	call	_cpct_getScreenPtr
                            518 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
   4EE2 E5            [11]  519 	push	hl
   4EE3 3E 0A         [ 7]  520 	ld	a, #0x0a
   4EE5 F5            [11]  521 	push	af
   4EE6 33            [ 6]  522 	inc	sp
   4EE7 3A 5C 5F      [13]  523 	ld	a, (_currentlives)
   4EEA F5            [11]  524 	push	af
   4EEB 33            [ 6]  525 	inc	sp
   4EEC CD 8A 5D      [17]  526 	call	__moduchar
   4EEF F1            [10]  527 	pop	af
   4EF0 C1            [10]  528 	pop	bc
   4EF1 26 00         [ 7]  529 	ld	h, #0x00
   4EF3 29            [11]  530 	add	hl, hl
   4EF4 11 69 5F      [10]  531 	ld	de, #_hudnumbers
   4EF7 19            [11]  532 	add	hl, de
   4EF8 5E            [ 7]  533 	ld	e, (hl)
   4EF9 23            [ 6]  534 	inc	hl
   4EFA 56            [ 7]  535 	ld	d, (hl)
   4EFB 21 08 08      [10]  536 	ld	hl, #0x0808
   4EFE E5            [11]  537 	push	hl
   4EFF C5            [11]  538 	push	bc
   4F00 D5            [11]  539 	push	de
   4F01 CD E5 5C      [17]  540 	call	_cpct_drawSprite
                            541 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4F04 21 46 B4      [10]  542 	ld	hl, #0xb446
   4F07 E5            [11]  543 	push	hl
   4F08 21 00 C0      [10]  544 	ld	hl, #0xc000
   4F0B E5            [11]  545 	push	hl
   4F0C CD 98 5E      [17]  546 	call	_cpct_getScreenPtr
                            547 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);
   4F0F E5            [11]  548 	push	hl
   4F10 3E 0A         [ 7]  549 	ld	a, #0x0a
   4F12 F5            [11]  550 	push	af
   4F13 33            [ 6]  551 	inc	sp
   4F14 3A 5D 5F      [13]  552 	ld	a, (_currentweapon)
   4F17 F5            [11]  553 	push	af
   4F18 33            [ 6]  554 	inc	sp
   4F19 CD 8A 5D      [17]  555 	call	__moduchar
   4F1C F1            [10]  556 	pop	af
   4F1D C1            [10]  557 	pop	bc
   4F1E 26 00         [ 7]  558 	ld	h, #0x00
   4F20 29            [11]  559 	add	hl, hl
   4F21 11 69 5F      [10]  560 	ld	de, #_hudnumbers
   4F24 19            [11]  561 	add	hl, de
   4F25 5E            [ 7]  562 	ld	e, (hl)
   4F26 23            [ 6]  563 	inc	hl
   4F27 56            [ 7]  564 	ld	d, (hl)
   4F28 21 08 08      [10]  565 	ld	hl, #0x0808
   4F2B E5            [11]  566 	push	hl
   4F2C C5            [11]  567 	push	bc
   4F2D D5            [11]  568 	push	de
   4F2E CD E5 5C      [17]  569 	call	_cpct_drawSprite
   4F31 C9            [10]  570 	ret
                            571 	.area _CODE
                            572 	.area _INITIALIZER
   5F84                     573 __xinit__hudnumbers:
   5F84 61 4D               574 	.dw __hud_dummy_sprite
   5F86 61 4D               575 	.dw __hud_dummy_sprite
   5F88 61 4D               576 	.dw __hud_dummy_sprite
   5F8A 61 4D               577 	.dw __hud_dummy_sprite
   5F8C 61 4D               578 	.dw __hud_dummy_sprite
   5F8E 61 4D               579 	.dw __hud_dummy_sprite
   5F90 61 4D               580 	.dw __hud_dummy_sprite
   5F92 61 4D               581 	.dw __hud_dummy_sprite
   5F94 61 4D               582 	.dw __hud_dummy_sprite
   5F96 61 4D               583 	.dw __hud_dummy_sprite
                            584 	.area _CABS (ABS)
