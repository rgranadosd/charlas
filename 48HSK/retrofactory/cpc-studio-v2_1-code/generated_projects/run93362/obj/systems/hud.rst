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
   5E32                      23 _currenthealth:
   5E32                      24 	.ds 1
   5E33                      25 _currentscore:
   5E33                      26 	.ds 2
   5E35                      27 _currenttime:
   5E35                      28 	.ds 1
   5E36                      29 _currentlives:
   5E36                      30 	.ds 1
   5E37                      31 _currentweapon:
   5E37                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
   5E43                      37 _hudnumbers:
   5E43                      38 	.ds 20
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
   4BC4                      63 _hud_draw_digits:
   4BC4 DD E5         [15]   64 	push	ix
   4BC6 DD 21 00 00   [14]   65 	ld	ix,#0
   4BCA DD 39         [15]   66 	add	ix,sp
   4BCC 3B            [ 6]   67 	dec	sp
                             68 ;src/systems/hud.c:24: divisor = 1;
   4BCD 01 01 00      [10]   69 	ld	bc, #0x0001
                             70 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4BD0 1E 01         [ 7]   71 	ld	e, #0x01
   4BD2                      72 00106$:
   4BD2 7B            [ 4]   73 	ld	a, e
   4BD3 DD 96 06      [19]   74 	sub	a, 6 (ix)
   4BD6 30 0B         [12]   75 	jr	NC,00101$
                             76 ;src/systems/hud.c:26: divisor *= 10;
   4BD8 69            [ 4]   77 	ld	l, c
   4BD9 60            [ 4]   78 	ld	h, b
   4BDA 29            [11]   79 	add	hl, hl
   4BDB 29            [11]   80 	add	hl, hl
   4BDC 09            [11]   81 	add	hl, bc
   4BDD 29            [11]   82 	add	hl, hl
   4BDE 4D            [ 4]   83 	ld	c, l
   4BDF 44            [ 4]   84 	ld	b, h
                             85 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4BE0 1C            [ 4]   86 	inc	e
   4BE1 18 EF         [12]   87 	jr	00106$
   4BE3                      88 00101$:
                             89 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4BE3 DD 36 FF 00   [19]   90 	ld	-1 (ix), #0x00
   4BE7                      91 00109$:
   4BE7 DD 7E FF      [19]   92 	ld	a, -1 (ix)
   4BEA DD 96 06      [19]   93 	sub	a, 6 (ix)
   4BED 30 7B         [12]   94 	jr	NC,00111$
                             95 ;src/systems/hud.c:30: digit = (u8)(value / divisor);
   4BEF C5            [11]   96 	push	bc
   4BF0 C5            [11]   97 	push	bc
   4BF1 DD 6E 04      [19]   98 	ld	l,4 (ix)
   4BF4 DD 66 05      [19]   99 	ld	h,5 (ix)
   4BF7 E5            [11]  100 	push	hl
   4BF8 CD 0A 5B      [17]  101 	call	__divuint
   4BFB F1            [10]  102 	pop	af
   4BFC F1            [10]  103 	pop	af
   4BFD 5D            [ 4]  104 	ld	e, l
   4BFE C1            [10]  105 	pop	bc
                            106 ;src/systems/hud.c:31: value = (u16)(value % divisor);
   4BFF C5            [11]  107 	push	bc
   4C00 D5            [11]  108 	push	de
   4C01 C5            [11]  109 	push	bc
   4C02 DD 6E 04      [19]  110 	ld	l,4 (ix)
   4C05 DD 66 05      [19]  111 	ld	h,5 (ix)
   4C08 E5            [11]  112 	push	hl
   4C09 CD 72 5C      [17]  113 	call	__moduint
   4C0C F1            [10]  114 	pop	af
   4C0D F1            [10]  115 	pop	af
   4C0E D1            [10]  116 	pop	de
   4C0F C1            [10]  117 	pop	bc
   4C10 DD 75 04      [19]  118 	ld	4 (ix), l
   4C13 DD 74 05      [19]  119 	ld	5 (ix), h
                            120 ;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4C16 DD 7E FF      [19]  121 	ld	a, -1 (ix)
   4C19 07            [ 4]  122 	rlca
   4C1A 07            [ 4]  123 	rlca
   4C1B 07            [ 4]  124 	rlca
   4C1C E6 F8         [ 7]  125 	and	a, #0xf8
   4C1E 57            [ 4]  126 	ld	d, a
   4C1F DD 7E 07      [19]  127 	ld	a, 7 (ix)
   4C22 82            [ 4]  128 	add	a, d
   4C23 57            [ 4]  129 	ld	d, a
   4C24 C5            [11]  130 	push	bc
   4C25 D5            [11]  131 	push	de
   4C26 DD 7E 08      [19]  132 	ld	a, 8 (ix)
   4C29 F5            [11]  133 	push	af
   4C2A 33            [ 6]  134 	inc	sp
   4C2B D5            [11]  135 	push	de
   4C2C 33            [ 6]  136 	inc	sp
   4C2D 21 00 C0      [10]  137 	ld	hl, #0xc000
   4C30 E5            [11]  138 	push	hl
   4C31 CD 74 5D      [17]  139 	call	_cpct_getScreenPtr
   4C34 D1            [10]  140 	pop	de
   4C35 C1            [10]  141 	pop	bc
                            142 ;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
   4C36 E5            [11]  143 	push	hl
   4C37 FD E1         [14]  144 	pop	iy
   4C39 26 00         [ 7]  145 	ld	h, #0x00
   4C3B 6B            [ 4]  146 	ld	l, e
   4C3C 29            [11]  147 	add	hl, hl
   4C3D 11 43 5E      [10]  148 	ld	de, #_hudnumbers
   4C40 19            [11]  149 	add	hl, de
   4C41 5E            [ 7]  150 	ld	e, (hl)
   4C42 23            [ 6]  151 	inc	hl
   4C43 56            [ 7]  152 	ld	d, (hl)
   4C44 C5            [11]  153 	push	bc
   4C45 21 08 08      [10]  154 	ld	hl, #0x0808
   4C48 E5            [11]  155 	push	hl
   4C49 FD E5         [15]  156 	push	iy
   4C4B D5            [11]  157 	push	de
   4C4C CD C1 5B      [17]  158 	call	_cpct_drawSprite
   4C4F C1            [10]  159 	pop	bc
                            160 ;src/systems/hud.c:36: if (divisor > 1) {
   4C50 3E 01         [ 7]  161 	ld	a, #0x01
   4C52 B9            [ 4]  162 	cp	a, c
   4C53 3E 00         [ 7]  163 	ld	a, #0x00
   4C55 98            [ 4]  164 	sbc	a, b
   4C56 30 0C         [12]  165 	jr	NC,00110$
                            166 ;src/systems/hud.c:37: divisor /= 10;
   4C58 21 0A 00      [10]  167 	ld	hl, #0x000a
   4C5B E5            [11]  168 	push	hl
   4C5C C5            [11]  169 	push	bc
   4C5D CD 0A 5B      [17]  170 	call	__divuint
   4C60 F1            [10]  171 	pop	af
   4C61 F1            [10]  172 	pop	af
   4C62 4D            [ 4]  173 	ld	c, l
   4C63 44            [ 4]  174 	ld	b, h
   4C64                     175 00110$:
                            176 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4C64 DD 34 FF      [23]  177 	inc	-1 (ix)
   4C67 C3 E7 4B      [10]  178 	jp	00109$
   4C6A                     179 00111$:
   4C6A 33            [ 6]  180 	inc	sp
   4C6B DD E1         [14]  181 	pop	ix
   4C6D C9            [10]  182 	ret
   4C6E                     183 __hud_dummy_sprite:
   4C6E 00                  184 	.db #0x00	; 0
   4C6F 00                  185 	.db 0x00
   4C70 00                  186 	.db 0x00
   4C71 00                  187 	.db 0x00
   4C72 00                  188 	.db 0x00
   4C73 00                  189 	.db 0x00
   4C74 00                  190 	.db 0x00
   4C75 00                  191 	.db 0x00
   4C76 00                  192 	.db 0x00
   4C77 00                  193 	.db 0x00
   4C78 00                  194 	.db 0x00
   4C79 00                  195 	.db 0x00
   4C7A 00                  196 	.db 0x00
   4C7B 00                  197 	.db 0x00
   4C7C 00                  198 	.db 0x00
   4C7D 00                  199 	.db 0x00
   4C7E 00                  200 	.db 0x00
   4C7F 00                  201 	.db 0x00
   4C80 00                  202 	.db 0x00
   4C81 00                  203 	.db 0x00
   4C82 00                  204 	.db 0x00
   4C83 00                  205 	.db 0x00
   4C84 00                  206 	.db 0x00
   4C85 00                  207 	.db 0x00
   4C86 00                  208 	.db 0x00
   4C87 00                  209 	.db 0x00
   4C88 00                  210 	.db 0x00
   4C89 00                  211 	.db 0x00
   4C8A 00                  212 	.db 0x00
   4C8B 00                  213 	.db 0x00
   4C8C 00                  214 	.db 0x00
   4C8D 00                  215 	.db 0x00
   4C8E 00                  216 	.db 0x00
   4C8F 00                  217 	.db 0x00
   4C90 00                  218 	.db 0x00
   4C91 00                  219 	.db 0x00
   4C92 00                  220 	.db 0x00
   4C93 00                  221 	.db 0x00
   4C94 00                  222 	.db 0x00
   4C95 00                  223 	.db 0x00
   4C96 00                  224 	.db 0x00
   4C97 00                  225 	.db 0x00
   4C98 00                  226 	.db 0x00
   4C99 00                  227 	.db 0x00
   4C9A 00                  228 	.db 0x00
   4C9B 00                  229 	.db 0x00
   4C9C 00                  230 	.db 0x00
   4C9D 00                  231 	.db 0x00
   4C9E 00                  232 	.db 0x00
   4C9F 00                  233 	.db 0x00
   4CA0 00                  234 	.db 0x00
   4CA1 00                  235 	.db 0x00
   4CA2 00                  236 	.db 0x00
   4CA3 00                  237 	.db 0x00
   4CA4 00                  238 	.db 0x00
   4CA5 00                  239 	.db 0x00
   4CA6 00                  240 	.db 0x00
   4CA7 00                  241 	.db 0x00
   4CA8 00                  242 	.db 0x00
   4CA9 00                  243 	.db 0x00
   4CAA 00                  244 	.db 0x00
   4CAB 00                  245 	.db 0x00
   4CAC 00                  246 	.db 0x00
   4CAD 00                  247 	.db 0x00
   4CAE                     248 _hudhealth:
   4CAE 00                  249 	.db #0x00	; 0
   4CAF 00                  250 	.db 0x00
   4CB0 00                  251 	.db 0x00
   4CB1 00                  252 	.db 0x00
   4CB2 00                  253 	.db 0x00
   4CB3 00                  254 	.db 0x00
   4CB4 00                  255 	.db 0x00
   4CB5 00                  256 	.db 0x00
   4CB6 00                  257 	.db 0x00
   4CB7 00                  258 	.db 0x00
   4CB8 00                  259 	.db 0x00
   4CB9 00                  260 	.db 0x00
   4CBA 00                  261 	.db 0x00
   4CBB 00                  262 	.db 0x00
   4CBC 00                  263 	.db 0x00
   4CBD 00                  264 	.db 0x00
   4CBE 00                  265 	.db 0x00
   4CBF 00                  266 	.db 0x00
   4CC0 00                  267 	.db 0x00
   4CC1 00                  268 	.db 0x00
   4CC2 00                  269 	.db 0x00
   4CC3 00                  270 	.db 0x00
   4CC4 00                  271 	.db 0x00
   4CC5 00                  272 	.db 0x00
   4CC6 00                  273 	.db 0x00
   4CC7 00                  274 	.db 0x00
   4CC8 00                  275 	.db 0x00
   4CC9 00                  276 	.db 0x00
   4CCA 00                  277 	.db 0x00
   4CCB 00                  278 	.db 0x00
   4CCC 00                  279 	.db 0x00
   4CCD 00                  280 	.db 0x00
   4CCE 00                  281 	.db 0x00
   4CCF 00                  282 	.db 0x00
   4CD0 00                  283 	.db 0x00
   4CD1 00                  284 	.db 0x00
   4CD2 00                  285 	.db 0x00
   4CD3 00                  286 	.db 0x00
   4CD4 00                  287 	.db 0x00
   4CD5 00                  288 	.db 0x00
   4CD6 00                  289 	.db 0x00
   4CD7 00                  290 	.db 0x00
   4CD8 00                  291 	.db 0x00
   4CD9 00                  292 	.db 0x00
   4CDA 00                  293 	.db 0x00
   4CDB 00                  294 	.db 0x00
   4CDC 00                  295 	.db 0x00
   4CDD 00                  296 	.db 0x00
   4CDE 00                  297 	.db 0x00
   4CDF 00                  298 	.db 0x00
   4CE0 00                  299 	.db 0x00
   4CE1 00                  300 	.db 0x00
   4CE2 00                  301 	.db 0x00
   4CE3 00                  302 	.db 0x00
   4CE4 00                  303 	.db 0x00
   4CE5 00                  304 	.db 0x00
   4CE6 00                  305 	.db 0x00
   4CE7 00                  306 	.db 0x00
   4CE8 00                  307 	.db 0x00
   4CE9 00                  308 	.db 0x00
   4CEA 00                  309 	.db 0x00
   4CEB 00                  310 	.db 0x00
   4CEC 00                  311 	.db 0x00
   4CED 00                  312 	.db 0x00
   4CEE                     313 _hudlives:
   4CEE 00                  314 	.db #0x00	; 0
   4CEF 00                  315 	.db 0x00
   4CF0 00                  316 	.db 0x00
   4CF1 00                  317 	.db 0x00
   4CF2 00                  318 	.db 0x00
   4CF3 00                  319 	.db 0x00
   4CF4 00                  320 	.db 0x00
   4CF5 00                  321 	.db 0x00
   4CF6 00                  322 	.db 0x00
   4CF7 00                  323 	.db 0x00
   4CF8 00                  324 	.db 0x00
   4CF9 00                  325 	.db 0x00
   4CFA 00                  326 	.db 0x00
   4CFB 00                  327 	.db 0x00
   4CFC 00                  328 	.db 0x00
   4CFD 00                  329 	.db 0x00
   4CFE 00                  330 	.db 0x00
   4CFF 00                  331 	.db 0x00
   4D00 00                  332 	.db 0x00
   4D01 00                  333 	.db 0x00
   4D02 00                  334 	.db 0x00
   4D03 00                  335 	.db 0x00
   4D04 00                  336 	.db 0x00
   4D05 00                  337 	.db 0x00
   4D06 00                  338 	.db 0x00
   4D07 00                  339 	.db 0x00
   4D08 00                  340 	.db 0x00
   4D09 00                  341 	.db 0x00
   4D0A 00                  342 	.db 0x00
   4D0B 00                  343 	.db 0x00
   4D0C 00                  344 	.db 0x00
   4D0D 00                  345 	.db 0x00
   4D0E 00                  346 	.db 0x00
   4D0F 00                  347 	.db 0x00
   4D10 00                  348 	.db 0x00
   4D11 00                  349 	.db 0x00
   4D12 00                  350 	.db 0x00
   4D13 00                  351 	.db 0x00
   4D14 00                  352 	.db 0x00
   4D15 00                  353 	.db 0x00
   4D16 00                  354 	.db 0x00
   4D17 00                  355 	.db 0x00
   4D18 00                  356 	.db 0x00
   4D19 00                  357 	.db 0x00
   4D1A 00                  358 	.db 0x00
   4D1B 00                  359 	.db 0x00
   4D1C 00                  360 	.db 0x00
   4D1D 00                  361 	.db 0x00
   4D1E 00                  362 	.db 0x00
   4D1F 00                  363 	.db 0x00
   4D20 00                  364 	.db 0x00
   4D21 00                  365 	.db 0x00
   4D22 00                  366 	.db 0x00
   4D23 00                  367 	.db 0x00
   4D24 00                  368 	.db 0x00
   4D25 00                  369 	.db 0x00
   4D26 00                  370 	.db 0x00
   4D27 00                  371 	.db 0x00
   4D28 00                  372 	.db 0x00
   4D29 00                  373 	.db 0x00
   4D2A 00                  374 	.db 0x00
   4D2B 00                  375 	.db 0x00
   4D2C 00                  376 	.db 0x00
   4D2D 00                  377 	.db 0x00
                            378 ;src/systems/hud.c:42: void hudinit(void) {
                            379 ;	---------------------------------
                            380 ; Function hudinit
                            381 ; ---------------------------------
   4D2E                     382 _hudinit::
                            383 ;src/systems/hud.c:43: currenthealth = 3;
   4D2E 21 32 5E      [10]  384 	ld	hl,#_currenthealth + 0
   4D31 36 03         [10]  385 	ld	(hl), #0x03
                            386 ;src/systems/hud.c:44: currentscore  = 0;
   4D33 21 00 00      [10]  387 	ld	hl, #0x0000
   4D36 22 33 5E      [16]  388 	ld	(_currentscore), hl
                            389 ;src/systems/hud.c:45: currenttime   = 90;
   4D39 21 35 5E      [10]  390 	ld	hl,#_currenttime + 0
   4D3C 36 5A         [10]  391 	ld	(hl), #0x5a
                            392 ;src/systems/hud.c:46: currentlives  = 3;
   4D3E 21 36 5E      [10]  393 	ld	hl,#_currentlives + 0
   4D41 36 03         [10]  394 	ld	(hl), #0x03
                            395 ;src/systems/hud.c:47: currentweapon = 0;
   4D43 21 37 5E      [10]  396 	ld	hl,#_currentweapon + 0
   4D46 36 00         [10]  397 	ld	(hl), #0x00
   4D48 C9            [10]  398 	ret
                            399 ;src/systems/hud.c:50: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            400 ;	---------------------------------
                            401 ; Function hudupdate
                            402 ; ---------------------------------
   4D49                     403 _hudupdate::
                            404 ;src/systems/hud.c:51: currenthealth = lives;
   4D49 21 02 00      [10]  405 	ld	hl, #2+0
   4D4C 39            [11]  406 	add	hl, sp
   4D4D 7E            [ 7]  407 	ld	a, (hl)
   4D4E 32 32 5E      [13]  408 	ld	(#_currenthealth + 0),a
                            409 ;src/systems/hud.c:52: currentscore  = score;
   4D51 21 03 00      [10]  410 	ld	hl, #3+0
   4D54 39            [11]  411 	add	hl, sp
   4D55 7E            [ 7]  412 	ld	a, (hl)
   4D56 32 33 5E      [13]  413 	ld	(#_currentscore + 0),a
   4D59 21 04 00      [10]  414 	ld	hl, #3+1
   4D5C 39            [11]  415 	add	hl, sp
   4D5D 7E            [ 7]  416 	ld	a, (hl)
   4D5E 32 34 5E      [13]  417 	ld	(#_currentscore + 1),a
                            418 ;src/systems/hud.c:53: currenttime   = time;
   4D61 21 05 00      [10]  419 	ld	hl, #5+0
   4D64 39            [11]  420 	add	hl, sp
   4D65 7E            [ 7]  421 	ld	a, (hl)
   4D66 32 35 5E      [13]  422 	ld	(#_currenttime + 0),a
                            423 ;src/systems/hud.c:54: currentlives  = lives;
   4D69 21 02 00      [10]  424 	ld	hl, #2+0
   4D6C 39            [11]  425 	add	hl, sp
   4D6D 7E            [ 7]  426 	ld	a, (hl)
   4D6E 32 36 5E      [13]  427 	ld	(#_currentlives + 0),a
                            428 ;src/systems/hud.c:55: currentweapon = weapon;
   4D71 21 06 00      [10]  429 	ld	hl, #6+0
   4D74 39            [11]  430 	add	hl, sp
   4D75 7E            [ 7]  431 	ld	a, (hl)
   4D76 32 37 5E      [13]  432 	ld	(#_currentweapon + 0),a
   4D79 C9            [10]  433 	ret
                            434 ;src/systems/hud.c:58: void hudrender(void) {
                            435 ;	---------------------------------
                            436 ; Function hudrender
                            437 ; ---------------------------------
   4D7A                     438 _hudrender::
                            439 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4D7A 0E 00         [ 7]  440 	ld	c, #0x00
   4D7C                     441 00103$:
   4D7C 21 32 5E      [10]  442 	ld	hl, #_currenthealth
                            443 ;src/systems/hud.c:65: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);
   4D7F 79            [ 4]  444 	ld	a,c
   4D80 BE            [ 7]  445 	cp	a,(hl)
   4D81 30 26         [12]  446 	jr	NC,00101$
   4D83 07            [ 4]  447 	rlca
   4D84 07            [ 4]  448 	rlca
   4D85 07            [ 4]  449 	rlca
   4D86 E6 F8         [ 7]  450 	and	a, #0xf8
   4D88 47            [ 4]  451 	ld	b, a
   4D89 04            [ 4]  452 	inc	b
   4D8A 04            [ 4]  453 	inc	b
   4D8B C5            [11]  454 	push	bc
   4D8C 3E 02         [ 7]  455 	ld	a, #0x02
   4D8E F5            [11]  456 	push	af
   4D8F 33            [ 6]  457 	inc	sp
   4D90 C5            [11]  458 	push	bc
   4D91 33            [ 6]  459 	inc	sp
   4D92 21 00 C0      [10]  460 	ld	hl, #0xc000
   4D95 E5            [11]  461 	push	hl
   4D96 CD 74 5D      [17]  462 	call	_cpct_getScreenPtr
   4D99 11 08 08      [10]  463 	ld	de, #0x0808
   4D9C D5            [11]  464 	push	de
   4D9D E5            [11]  465 	push	hl
   4D9E 21 AE 4C      [10]  466 	ld	hl, #_hudhealth
   4DA1 E5            [11]  467 	push	hl
   4DA2 CD C1 5B      [17]  468 	call	_cpct_drawSprite
   4DA5 C1            [10]  469 	pop	bc
                            470 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4DA6 0C            [ 4]  471 	inc	c
   4DA7 18 D3         [12]  472 	jr	00103$
   4DA9                     473 00101$:
                            474 ;src/systems/hud.c:69: scoretemp = currentscore;
   4DA9 2A 33 5E      [16]  475 	ld	hl, (_currentscore)
                            476 ;src/systems/hud.c:70: hud_draw_digits(scoretemp, 5, 88, 2);
   4DAC 01 58 02      [10]  477 	ld	bc, #0x0258
   4DAF C5            [11]  478 	push	bc
   4DB0 3E 05         [ 7]  479 	ld	a, #0x05
   4DB2 F5            [11]  480 	push	af
   4DB3 33            [ 6]  481 	inc	sp
   4DB4 E5            [11]  482 	push	hl
   4DB5 CD C4 4B      [17]  483 	call	_hud_draw_digits
   4DB8 F1            [10]  484 	pop	af
   4DB9 F1            [10]  485 	pop	af
   4DBA 33            [ 6]  486 	inc	sp
                            487 ;src/systems/hud.c:72: timetemp = currenttime;
   4DBB 21 35 5E      [10]  488 	ld	hl,#_currenttime + 0
   4DBE 4E            [ 7]  489 	ld	c, (hl)
                            490 ;src/systems/hud.c:73: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4DBF 06 00         [ 7]  491 	ld	b, #0x00
   4DC1 21 38 02      [10]  492 	ld	hl, #0x0238
   4DC4 E5            [11]  493 	push	hl
   4DC5 3E 03         [ 7]  494 	ld	a, #0x03
   4DC7 F5            [11]  495 	push	af
   4DC8 33            [ 6]  496 	inc	sp
   4DC9 C5            [11]  497 	push	bc
   4DCA CD C4 4B      [17]  498 	call	_hud_draw_digits
   4DCD F1            [10]  499 	pop	af
                            500 ;src/systems/hud.c:75: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4DCE 33            [ 6]  501 	inc	sp
   4DCF 21 02 B4      [10]  502 	ld	hl,#0xb402
   4DD2 E3            [19]  503 	ex	(sp),hl
   4DD3 21 00 C0      [10]  504 	ld	hl, #0xc000
   4DD6 E5            [11]  505 	push	hl
   4DD7 CD 74 5D      [17]  506 	call	_cpct_getScreenPtr
                            507 ;src/systems/hud.c:76: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4DDA 01 EE 4C      [10]  508 	ld	bc, #_hudlives+0
   4DDD 11 08 08      [10]  509 	ld	de, #0x0808
   4DE0 D5            [11]  510 	push	de
   4DE1 E5            [11]  511 	push	hl
   4DE2 C5            [11]  512 	push	bc
   4DE3 CD C1 5B      [17]  513 	call	_cpct_drawSprite
                            514 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4DE6 21 0C B4      [10]  515 	ld	hl, #0xb40c
   4DE9 E5            [11]  516 	push	hl
   4DEA 21 00 C0      [10]  517 	ld	hl, #0xc000
   4DED E5            [11]  518 	push	hl
   4DEE CD 74 5D      [17]  519 	call	_cpct_getScreenPtr
                            520 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
   4DF1 E5            [11]  521 	push	hl
   4DF2 3E 0A         [ 7]  522 	ld	a, #0x0a
   4DF4 F5            [11]  523 	push	af
   4DF5 33            [ 6]  524 	inc	sp
   4DF6 3A 36 5E      [13]  525 	ld	a, (_currentlives)
   4DF9 F5            [11]  526 	push	af
   4DFA 33            [ 6]  527 	inc	sp
   4DFB CD 66 5C      [17]  528 	call	__moduchar
   4DFE F1            [10]  529 	pop	af
   4DFF C1            [10]  530 	pop	bc
   4E00 26 00         [ 7]  531 	ld	h, #0x00
   4E02 29            [11]  532 	add	hl, hl
   4E03 11 43 5E      [10]  533 	ld	de, #_hudnumbers
   4E06 19            [11]  534 	add	hl, de
   4E07 5E            [ 7]  535 	ld	e, (hl)
   4E08 23            [ 6]  536 	inc	hl
   4E09 56            [ 7]  537 	ld	d, (hl)
   4E0A 21 08 08      [10]  538 	ld	hl, #0x0808
   4E0D E5            [11]  539 	push	hl
   4E0E C5            [11]  540 	push	bc
   4E0F D5            [11]  541 	push	de
   4E10 CD C1 5B      [17]  542 	call	_cpct_drawSprite
                            543 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4E13 21 46 B4      [10]  544 	ld	hl, #0xb446
   4E16 E5            [11]  545 	push	hl
   4E17 21 00 C0      [10]  546 	ld	hl, #0xc000
   4E1A E5            [11]  547 	push	hl
   4E1B CD 74 5D      [17]  548 	call	_cpct_getScreenPtr
                            549 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);
   4E1E E5            [11]  550 	push	hl
   4E1F 3E 0A         [ 7]  551 	ld	a, #0x0a
   4E21 F5            [11]  552 	push	af
   4E22 33            [ 6]  553 	inc	sp
   4E23 3A 37 5E      [13]  554 	ld	a, (_currentweapon)
   4E26 F5            [11]  555 	push	af
   4E27 33            [ 6]  556 	inc	sp
   4E28 CD 66 5C      [17]  557 	call	__moduchar
   4E2B F1            [10]  558 	pop	af
   4E2C C1            [10]  559 	pop	bc
   4E2D 26 00         [ 7]  560 	ld	h, #0x00
   4E2F 29            [11]  561 	add	hl, hl
   4E30 11 43 5E      [10]  562 	ld	de, #_hudnumbers
   4E33 19            [11]  563 	add	hl, de
   4E34 5E            [ 7]  564 	ld	e, (hl)
   4E35 23            [ 6]  565 	inc	hl
   4E36 56            [ 7]  566 	ld	d, (hl)
   4E37 21 08 08      [10]  567 	ld	hl, #0x0808
   4E3A E5            [11]  568 	push	hl
   4E3B C5            [11]  569 	push	bc
   4E3C D5            [11]  570 	push	de
   4E3D CD C1 5B      [17]  571 	call	_cpct_drawSprite
   4E40 C9            [10]  572 	ret
                            573 	.area _CODE
                            574 	.area _INITIALIZER
   5E5E                     575 __xinit__hudnumbers:
   5E5E 6E 4C               576 	.dw __hud_dummy_sprite
   5E60 6E 4C               577 	.dw __hud_dummy_sprite
   5E62 6E 4C               578 	.dw __hud_dummy_sprite
   5E64 6E 4C               579 	.dw __hud_dummy_sprite
   5E66 6E 4C               580 	.dw __hud_dummy_sprite
   5E68 6E 4C               581 	.dw __hud_dummy_sprite
   5E6A 6E 4C               582 	.dw __hud_dummy_sprite
   5E6C 6E 4C               583 	.dw __hud_dummy_sprite
   5E6E 6E 4C               584 	.dw __hud_dummy_sprite
   5E70 6E 4C               585 	.dw __hud_dummy_sprite
                            586 	.area _CABS (ABS)
