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
   5D71                      23 _currenthealth:
   5D71                      24 	.ds 1
   5D72                      25 _currentscore:
   5D72                      26 	.ds 2
   5D74                      27 _currenttime:
   5D74                      28 	.ds 1
   5D75                      29 _currentlives:
   5D75                      30 	.ds 1
   5D76                      31 _currentweapon:
   5D76                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
   5D82                      37 _hudnumbers:
   5D82                      38 	.ds 20
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
   4B78                      63 _hud_draw_digits:
   4B78 DD E5         [15]   64 	push	ix
   4B7A DD 21 00 00   [14]   65 	ld	ix,#0
   4B7E DD 39         [15]   66 	add	ix,sp
   4B80 3B            [ 6]   67 	dec	sp
                             68 ;src/systems/hud.c:24: divisor = 1;
   4B81 01 01 00      [10]   69 	ld	bc, #0x0001
                             70 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4B84 1E 01         [ 7]   71 	ld	e, #0x01
   4B86                      72 00106$:
   4B86 7B            [ 4]   73 	ld	a, e
   4B87 DD 96 06      [19]   74 	sub	a, 6 (ix)
   4B8A 30 0B         [12]   75 	jr	NC,00101$
                             76 ;src/systems/hud.c:26: divisor *= 10;
   4B8C 69            [ 4]   77 	ld	l, c
   4B8D 60            [ 4]   78 	ld	h, b
   4B8E 29            [11]   79 	add	hl, hl
   4B8F 29            [11]   80 	add	hl, hl
   4B90 09            [11]   81 	add	hl, bc
   4B91 29            [11]   82 	add	hl, hl
   4B92 4D            [ 4]   83 	ld	c, l
   4B93 44            [ 4]   84 	ld	b, h
                             85 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4B94 1C            [ 4]   86 	inc	e
   4B95 18 EF         [12]   87 	jr	00106$
   4B97                      88 00101$:
                             89 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4B97 DD 36 FF 00   [19]   90 	ld	-1 (ix), #0x00
   4B9B                      91 00109$:
   4B9B DD 7E FF      [19]   92 	ld	a, -1 (ix)
   4B9E DD 96 06      [19]   93 	sub	a, 6 (ix)
   4BA1 30 7B         [12]   94 	jr	NC,00111$
                             95 ;src/systems/hud.c:30: digit = (u8)(value / divisor);
   4BA3 C5            [11]   96 	push	bc
   4BA4 C5            [11]   97 	push	bc
   4BA5 DD 6E 04      [19]   98 	ld	l,4 (ix)
   4BA8 DD 66 05      [19]   99 	ld	h,5 (ix)
   4BAB E5            [11]  100 	push	hl
   4BAC CD 49 5A      [17]  101 	call	__divuint
   4BAF F1            [10]  102 	pop	af
   4BB0 F1            [10]  103 	pop	af
   4BB1 5D            [ 4]  104 	ld	e, l
   4BB2 C1            [10]  105 	pop	bc
                            106 ;src/systems/hud.c:31: value = (u16)(value % divisor);
   4BB3 C5            [11]  107 	push	bc
   4BB4 D5            [11]  108 	push	de
   4BB5 C5            [11]  109 	push	bc
   4BB6 DD 6E 04      [19]  110 	ld	l,4 (ix)
   4BB9 DD 66 05      [19]  111 	ld	h,5 (ix)
   4BBC E5            [11]  112 	push	hl
   4BBD CD B1 5B      [17]  113 	call	__moduint
   4BC0 F1            [10]  114 	pop	af
   4BC1 F1            [10]  115 	pop	af
   4BC2 D1            [10]  116 	pop	de
   4BC3 C1            [10]  117 	pop	bc
   4BC4 DD 75 04      [19]  118 	ld	4 (ix), l
   4BC7 DD 74 05      [19]  119 	ld	5 (ix), h
                            120 ;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4BCA DD 7E FF      [19]  121 	ld	a, -1 (ix)
   4BCD 07            [ 4]  122 	rlca
   4BCE 07            [ 4]  123 	rlca
   4BCF 07            [ 4]  124 	rlca
   4BD0 E6 F8         [ 7]  125 	and	a, #0xf8
   4BD2 57            [ 4]  126 	ld	d, a
   4BD3 DD 7E 07      [19]  127 	ld	a, 7 (ix)
   4BD6 82            [ 4]  128 	add	a, d
   4BD7 57            [ 4]  129 	ld	d, a
   4BD8 C5            [11]  130 	push	bc
   4BD9 D5            [11]  131 	push	de
   4BDA DD 7E 08      [19]  132 	ld	a, 8 (ix)
   4BDD F5            [11]  133 	push	af
   4BDE 33            [ 6]  134 	inc	sp
   4BDF D5            [11]  135 	push	de
   4BE0 33            [ 6]  136 	inc	sp
   4BE1 21 00 C0      [10]  137 	ld	hl, #0xc000
   4BE4 E5            [11]  138 	push	hl
   4BE5 CD B3 5C      [17]  139 	call	_cpct_getScreenPtr
   4BE8 D1            [10]  140 	pop	de
   4BE9 C1            [10]  141 	pop	bc
                            142 ;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
   4BEA E5            [11]  143 	push	hl
   4BEB FD E1         [14]  144 	pop	iy
   4BED 26 00         [ 7]  145 	ld	h, #0x00
   4BEF 6B            [ 4]  146 	ld	l, e
   4BF0 29            [11]  147 	add	hl, hl
   4BF1 11 82 5D      [10]  148 	ld	de, #_hudnumbers
   4BF4 19            [11]  149 	add	hl, de
   4BF5 5E            [ 7]  150 	ld	e, (hl)
   4BF6 23            [ 6]  151 	inc	hl
   4BF7 56            [ 7]  152 	ld	d, (hl)
   4BF8 C5            [11]  153 	push	bc
   4BF9 21 08 08      [10]  154 	ld	hl, #0x0808
   4BFC E5            [11]  155 	push	hl
   4BFD FD E5         [15]  156 	push	iy
   4BFF D5            [11]  157 	push	de
   4C00 CD 00 5B      [17]  158 	call	_cpct_drawSprite
   4C03 C1            [10]  159 	pop	bc
                            160 ;src/systems/hud.c:36: if (divisor > 1) {
   4C04 3E 01         [ 7]  161 	ld	a, #0x01
   4C06 B9            [ 4]  162 	cp	a, c
   4C07 3E 00         [ 7]  163 	ld	a, #0x00
   4C09 98            [ 4]  164 	sbc	a, b
   4C0A 30 0C         [12]  165 	jr	NC,00110$
                            166 ;src/systems/hud.c:37: divisor /= 10;
   4C0C 21 0A 00      [10]  167 	ld	hl, #0x000a
   4C0F E5            [11]  168 	push	hl
   4C10 C5            [11]  169 	push	bc
   4C11 CD 49 5A      [17]  170 	call	__divuint
   4C14 F1            [10]  171 	pop	af
   4C15 F1            [10]  172 	pop	af
   4C16 4D            [ 4]  173 	ld	c, l
   4C17 44            [ 4]  174 	ld	b, h
   4C18                     175 00110$:
                            176 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4C18 DD 34 FF      [23]  177 	inc	-1 (ix)
   4C1B C3 9B 4B      [10]  178 	jp	00109$
   4C1E                     179 00111$:
   4C1E 33            [ 6]  180 	inc	sp
   4C1F DD E1         [14]  181 	pop	ix
   4C21 C9            [10]  182 	ret
   4C22                     183 __hud_dummy_sprite:
   4C22 00                  184 	.db #0x00	; 0
   4C23 00                  185 	.db 0x00
   4C24 00                  186 	.db 0x00
   4C25 00                  187 	.db 0x00
   4C26 00                  188 	.db 0x00
   4C27 00                  189 	.db 0x00
   4C28 00                  190 	.db 0x00
   4C29 00                  191 	.db 0x00
   4C2A 00                  192 	.db 0x00
   4C2B 00                  193 	.db 0x00
   4C2C 00                  194 	.db 0x00
   4C2D 00                  195 	.db 0x00
   4C2E 00                  196 	.db 0x00
   4C2F 00                  197 	.db 0x00
   4C30 00                  198 	.db 0x00
   4C31 00                  199 	.db 0x00
   4C32 00                  200 	.db 0x00
   4C33 00                  201 	.db 0x00
   4C34 00                  202 	.db 0x00
   4C35 00                  203 	.db 0x00
   4C36 00                  204 	.db 0x00
   4C37 00                  205 	.db 0x00
   4C38 00                  206 	.db 0x00
   4C39 00                  207 	.db 0x00
   4C3A 00                  208 	.db 0x00
   4C3B 00                  209 	.db 0x00
   4C3C 00                  210 	.db 0x00
   4C3D 00                  211 	.db 0x00
   4C3E 00                  212 	.db 0x00
   4C3F 00                  213 	.db 0x00
   4C40 00                  214 	.db 0x00
   4C41 00                  215 	.db 0x00
   4C42 00                  216 	.db 0x00
   4C43 00                  217 	.db 0x00
   4C44 00                  218 	.db 0x00
   4C45 00                  219 	.db 0x00
   4C46 00                  220 	.db 0x00
   4C47 00                  221 	.db 0x00
   4C48 00                  222 	.db 0x00
   4C49 00                  223 	.db 0x00
   4C4A 00                  224 	.db 0x00
   4C4B 00                  225 	.db 0x00
   4C4C 00                  226 	.db 0x00
   4C4D 00                  227 	.db 0x00
   4C4E 00                  228 	.db 0x00
   4C4F 00                  229 	.db 0x00
   4C50 00                  230 	.db 0x00
   4C51 00                  231 	.db 0x00
   4C52 00                  232 	.db 0x00
   4C53 00                  233 	.db 0x00
   4C54 00                  234 	.db 0x00
   4C55 00                  235 	.db 0x00
   4C56 00                  236 	.db 0x00
   4C57 00                  237 	.db 0x00
   4C58 00                  238 	.db 0x00
   4C59 00                  239 	.db 0x00
   4C5A 00                  240 	.db 0x00
   4C5B 00                  241 	.db 0x00
   4C5C 00                  242 	.db 0x00
   4C5D 00                  243 	.db 0x00
   4C5E 00                  244 	.db 0x00
   4C5F 00                  245 	.db 0x00
   4C60 00                  246 	.db 0x00
   4C61 00                  247 	.db 0x00
   4C62                     248 _hudhealth:
   4C62 00                  249 	.db #0x00	; 0
   4C63 00                  250 	.db 0x00
   4C64 00                  251 	.db 0x00
   4C65 00                  252 	.db 0x00
   4C66 00                  253 	.db 0x00
   4C67 00                  254 	.db 0x00
   4C68 00                  255 	.db 0x00
   4C69 00                  256 	.db 0x00
   4C6A 00                  257 	.db 0x00
   4C6B 00                  258 	.db 0x00
   4C6C 00                  259 	.db 0x00
   4C6D 00                  260 	.db 0x00
   4C6E 00                  261 	.db 0x00
   4C6F 00                  262 	.db 0x00
   4C70 00                  263 	.db 0x00
   4C71 00                  264 	.db 0x00
   4C72 00                  265 	.db 0x00
   4C73 00                  266 	.db 0x00
   4C74 00                  267 	.db 0x00
   4C75 00                  268 	.db 0x00
   4C76 00                  269 	.db 0x00
   4C77 00                  270 	.db 0x00
   4C78 00                  271 	.db 0x00
   4C79 00                  272 	.db 0x00
   4C7A 00                  273 	.db 0x00
   4C7B 00                  274 	.db 0x00
   4C7C 00                  275 	.db 0x00
   4C7D 00                  276 	.db 0x00
   4C7E 00                  277 	.db 0x00
   4C7F 00                  278 	.db 0x00
   4C80 00                  279 	.db 0x00
   4C81 00                  280 	.db 0x00
   4C82 00                  281 	.db 0x00
   4C83 00                  282 	.db 0x00
   4C84 00                  283 	.db 0x00
   4C85 00                  284 	.db 0x00
   4C86 00                  285 	.db 0x00
   4C87 00                  286 	.db 0x00
   4C88 00                  287 	.db 0x00
   4C89 00                  288 	.db 0x00
   4C8A 00                  289 	.db 0x00
   4C8B 00                  290 	.db 0x00
   4C8C 00                  291 	.db 0x00
   4C8D 00                  292 	.db 0x00
   4C8E 00                  293 	.db 0x00
   4C8F 00                  294 	.db 0x00
   4C90 00                  295 	.db 0x00
   4C91 00                  296 	.db 0x00
   4C92 00                  297 	.db 0x00
   4C93 00                  298 	.db 0x00
   4C94 00                  299 	.db 0x00
   4C95 00                  300 	.db 0x00
   4C96 00                  301 	.db 0x00
   4C97 00                  302 	.db 0x00
   4C98 00                  303 	.db 0x00
   4C99 00                  304 	.db 0x00
   4C9A 00                  305 	.db 0x00
   4C9B 00                  306 	.db 0x00
   4C9C 00                  307 	.db 0x00
   4C9D 00                  308 	.db 0x00
   4C9E 00                  309 	.db 0x00
   4C9F 00                  310 	.db 0x00
   4CA0 00                  311 	.db 0x00
   4CA1 00                  312 	.db 0x00
   4CA2                     313 _hudlives:
   4CA2 00                  314 	.db #0x00	; 0
   4CA3 00                  315 	.db 0x00
   4CA4 00                  316 	.db 0x00
   4CA5 00                  317 	.db 0x00
   4CA6 00                  318 	.db 0x00
   4CA7 00                  319 	.db 0x00
   4CA8 00                  320 	.db 0x00
   4CA9 00                  321 	.db 0x00
   4CAA 00                  322 	.db 0x00
   4CAB 00                  323 	.db 0x00
   4CAC 00                  324 	.db 0x00
   4CAD 00                  325 	.db 0x00
   4CAE 00                  326 	.db 0x00
   4CAF 00                  327 	.db 0x00
   4CB0 00                  328 	.db 0x00
   4CB1 00                  329 	.db 0x00
   4CB2 00                  330 	.db 0x00
   4CB3 00                  331 	.db 0x00
   4CB4 00                  332 	.db 0x00
   4CB5 00                  333 	.db 0x00
   4CB6 00                  334 	.db 0x00
   4CB7 00                  335 	.db 0x00
   4CB8 00                  336 	.db 0x00
   4CB9 00                  337 	.db 0x00
   4CBA 00                  338 	.db 0x00
   4CBB 00                  339 	.db 0x00
   4CBC 00                  340 	.db 0x00
   4CBD 00                  341 	.db 0x00
   4CBE 00                  342 	.db 0x00
   4CBF 00                  343 	.db 0x00
   4CC0 00                  344 	.db 0x00
   4CC1 00                  345 	.db 0x00
   4CC2 00                  346 	.db 0x00
   4CC3 00                  347 	.db 0x00
   4CC4 00                  348 	.db 0x00
   4CC5 00                  349 	.db 0x00
   4CC6 00                  350 	.db 0x00
   4CC7 00                  351 	.db 0x00
   4CC8 00                  352 	.db 0x00
   4CC9 00                  353 	.db 0x00
   4CCA 00                  354 	.db 0x00
   4CCB 00                  355 	.db 0x00
   4CCC 00                  356 	.db 0x00
   4CCD 00                  357 	.db 0x00
   4CCE 00                  358 	.db 0x00
   4CCF 00                  359 	.db 0x00
   4CD0 00                  360 	.db 0x00
   4CD1 00                  361 	.db 0x00
   4CD2 00                  362 	.db 0x00
   4CD3 00                  363 	.db 0x00
   4CD4 00                  364 	.db 0x00
   4CD5 00                  365 	.db 0x00
   4CD6 00                  366 	.db 0x00
   4CD7 00                  367 	.db 0x00
   4CD8 00                  368 	.db 0x00
   4CD9 00                  369 	.db 0x00
   4CDA 00                  370 	.db 0x00
   4CDB 00                  371 	.db 0x00
   4CDC 00                  372 	.db 0x00
   4CDD 00                  373 	.db 0x00
   4CDE 00                  374 	.db 0x00
   4CDF 00                  375 	.db 0x00
   4CE0 00                  376 	.db 0x00
   4CE1 00                  377 	.db 0x00
                            378 ;src/systems/hud.c:42: void hudinit(void) {
                            379 ;	---------------------------------
                            380 ; Function hudinit
                            381 ; ---------------------------------
   4CE2                     382 _hudinit::
                            383 ;src/systems/hud.c:43: currenthealth = 3;
   4CE2 21 71 5D      [10]  384 	ld	hl,#_currenthealth + 0
   4CE5 36 03         [10]  385 	ld	(hl), #0x03
                            386 ;src/systems/hud.c:44: currentscore  = 0;
   4CE7 21 00 00      [10]  387 	ld	hl, #0x0000
   4CEA 22 72 5D      [16]  388 	ld	(_currentscore), hl
                            389 ;src/systems/hud.c:45: currenttime   = 90;
   4CED 21 74 5D      [10]  390 	ld	hl,#_currenttime + 0
   4CF0 36 5A         [10]  391 	ld	(hl), #0x5a
                            392 ;src/systems/hud.c:46: currentlives  = 3;
   4CF2 21 75 5D      [10]  393 	ld	hl,#_currentlives + 0
   4CF5 36 03         [10]  394 	ld	(hl), #0x03
                            395 ;src/systems/hud.c:47: currentweapon = 0;
   4CF7 21 76 5D      [10]  396 	ld	hl,#_currentweapon + 0
   4CFA 36 00         [10]  397 	ld	(hl), #0x00
   4CFC C9            [10]  398 	ret
                            399 ;src/systems/hud.c:50: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            400 ;	---------------------------------
                            401 ; Function hudupdate
                            402 ; ---------------------------------
   4CFD                     403 _hudupdate::
                            404 ;src/systems/hud.c:51: currenthealth = lives;
   4CFD 21 02 00      [10]  405 	ld	hl, #2+0
   4D00 39            [11]  406 	add	hl, sp
   4D01 7E            [ 7]  407 	ld	a, (hl)
   4D02 32 71 5D      [13]  408 	ld	(#_currenthealth + 0),a
                            409 ;src/systems/hud.c:52: currentscore  = score;
   4D05 21 03 00      [10]  410 	ld	hl, #3+0
   4D08 39            [11]  411 	add	hl, sp
   4D09 7E            [ 7]  412 	ld	a, (hl)
   4D0A 32 72 5D      [13]  413 	ld	(#_currentscore + 0),a
   4D0D 21 04 00      [10]  414 	ld	hl, #3+1
   4D10 39            [11]  415 	add	hl, sp
   4D11 7E            [ 7]  416 	ld	a, (hl)
   4D12 32 73 5D      [13]  417 	ld	(#_currentscore + 1),a
                            418 ;src/systems/hud.c:53: currenttime   = time;
   4D15 21 05 00      [10]  419 	ld	hl, #5+0
   4D18 39            [11]  420 	add	hl, sp
   4D19 7E            [ 7]  421 	ld	a, (hl)
   4D1A 32 74 5D      [13]  422 	ld	(#_currenttime + 0),a
                            423 ;src/systems/hud.c:54: currentlives  = lives;
   4D1D 21 02 00      [10]  424 	ld	hl, #2+0
   4D20 39            [11]  425 	add	hl, sp
   4D21 7E            [ 7]  426 	ld	a, (hl)
   4D22 32 75 5D      [13]  427 	ld	(#_currentlives + 0),a
                            428 ;src/systems/hud.c:55: currentweapon = weapon;
   4D25 21 06 00      [10]  429 	ld	hl, #6+0
   4D28 39            [11]  430 	add	hl, sp
   4D29 7E            [ 7]  431 	ld	a, (hl)
   4D2A 32 76 5D      [13]  432 	ld	(#_currentweapon + 0),a
   4D2D C9            [10]  433 	ret
                            434 ;src/systems/hud.c:58: void hudrender(void) {
                            435 ;	---------------------------------
                            436 ; Function hudrender
                            437 ; ---------------------------------
   4D2E                     438 _hudrender::
                            439 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4D2E 0E 00         [ 7]  440 	ld	c, #0x00
   4D30                     441 00103$:
   4D30 21 71 5D      [10]  442 	ld	hl, #_currenthealth
                            443 ;src/systems/hud.c:65: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);
   4D33 79            [ 4]  444 	ld	a,c
   4D34 BE            [ 7]  445 	cp	a,(hl)
   4D35 30 26         [12]  446 	jr	NC,00101$
   4D37 07            [ 4]  447 	rlca
   4D38 07            [ 4]  448 	rlca
   4D39 07            [ 4]  449 	rlca
   4D3A E6 F8         [ 7]  450 	and	a, #0xf8
   4D3C 47            [ 4]  451 	ld	b, a
   4D3D 04            [ 4]  452 	inc	b
   4D3E 04            [ 4]  453 	inc	b
   4D3F C5            [11]  454 	push	bc
   4D40 3E 02         [ 7]  455 	ld	a, #0x02
   4D42 F5            [11]  456 	push	af
   4D43 33            [ 6]  457 	inc	sp
   4D44 C5            [11]  458 	push	bc
   4D45 33            [ 6]  459 	inc	sp
   4D46 21 00 C0      [10]  460 	ld	hl, #0xc000
   4D49 E5            [11]  461 	push	hl
   4D4A CD B3 5C      [17]  462 	call	_cpct_getScreenPtr
   4D4D 11 08 08      [10]  463 	ld	de, #0x0808
   4D50 D5            [11]  464 	push	de
   4D51 E5            [11]  465 	push	hl
   4D52 21 62 4C      [10]  466 	ld	hl, #_hudhealth
   4D55 E5            [11]  467 	push	hl
   4D56 CD 00 5B      [17]  468 	call	_cpct_drawSprite
   4D59 C1            [10]  469 	pop	bc
                            470 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   4D5A 0C            [ 4]  471 	inc	c
   4D5B 18 D3         [12]  472 	jr	00103$
   4D5D                     473 00101$:
                            474 ;src/systems/hud.c:69: scoretemp = currentscore;
   4D5D 2A 72 5D      [16]  475 	ld	hl, (_currentscore)
                            476 ;src/systems/hud.c:70: hud_draw_digits(scoretemp, 5, 88, 2);
   4D60 01 58 02      [10]  477 	ld	bc, #0x0258
   4D63 C5            [11]  478 	push	bc
   4D64 3E 05         [ 7]  479 	ld	a, #0x05
   4D66 F5            [11]  480 	push	af
   4D67 33            [ 6]  481 	inc	sp
   4D68 E5            [11]  482 	push	hl
   4D69 CD 78 4B      [17]  483 	call	_hud_draw_digits
   4D6C F1            [10]  484 	pop	af
   4D6D F1            [10]  485 	pop	af
   4D6E 33            [ 6]  486 	inc	sp
                            487 ;src/systems/hud.c:72: timetemp = currenttime;
   4D6F 21 74 5D      [10]  488 	ld	hl,#_currenttime + 0
   4D72 4E            [ 7]  489 	ld	c, (hl)
                            490 ;src/systems/hud.c:73: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4D73 06 00         [ 7]  491 	ld	b, #0x00
   4D75 21 38 02      [10]  492 	ld	hl, #0x0238
   4D78 E5            [11]  493 	push	hl
   4D79 3E 03         [ 7]  494 	ld	a, #0x03
   4D7B F5            [11]  495 	push	af
   4D7C 33            [ 6]  496 	inc	sp
   4D7D C5            [11]  497 	push	bc
   4D7E CD 78 4B      [17]  498 	call	_hud_draw_digits
   4D81 F1            [10]  499 	pop	af
                            500 ;src/systems/hud.c:75: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4D82 33            [ 6]  501 	inc	sp
   4D83 21 02 B4      [10]  502 	ld	hl,#0xb402
   4D86 E3            [19]  503 	ex	(sp),hl
   4D87 21 00 C0      [10]  504 	ld	hl, #0xc000
   4D8A E5            [11]  505 	push	hl
   4D8B CD B3 5C      [17]  506 	call	_cpct_getScreenPtr
                            507 ;src/systems/hud.c:76: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4D8E 01 A2 4C      [10]  508 	ld	bc, #_hudlives+0
   4D91 11 08 08      [10]  509 	ld	de, #0x0808
   4D94 D5            [11]  510 	push	de
   4D95 E5            [11]  511 	push	hl
   4D96 C5            [11]  512 	push	bc
   4D97 CD 00 5B      [17]  513 	call	_cpct_drawSprite
                            514 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4D9A 21 0C B4      [10]  515 	ld	hl, #0xb40c
   4D9D E5            [11]  516 	push	hl
   4D9E 21 00 C0      [10]  517 	ld	hl, #0xc000
   4DA1 E5            [11]  518 	push	hl
   4DA2 CD B3 5C      [17]  519 	call	_cpct_getScreenPtr
                            520 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
   4DA5 E5            [11]  521 	push	hl
   4DA6 3E 0A         [ 7]  522 	ld	a, #0x0a
   4DA8 F5            [11]  523 	push	af
   4DA9 33            [ 6]  524 	inc	sp
   4DAA 3A 75 5D      [13]  525 	ld	a, (_currentlives)
   4DAD F5            [11]  526 	push	af
   4DAE 33            [ 6]  527 	inc	sp
   4DAF CD A5 5B      [17]  528 	call	__moduchar
   4DB2 F1            [10]  529 	pop	af
   4DB3 C1            [10]  530 	pop	bc
   4DB4 26 00         [ 7]  531 	ld	h, #0x00
   4DB6 29            [11]  532 	add	hl, hl
   4DB7 11 82 5D      [10]  533 	ld	de, #_hudnumbers
   4DBA 19            [11]  534 	add	hl, de
   4DBB 5E            [ 7]  535 	ld	e, (hl)
   4DBC 23            [ 6]  536 	inc	hl
   4DBD 56            [ 7]  537 	ld	d, (hl)
   4DBE 21 08 08      [10]  538 	ld	hl, #0x0808
   4DC1 E5            [11]  539 	push	hl
   4DC2 C5            [11]  540 	push	bc
   4DC3 D5            [11]  541 	push	de
   4DC4 CD 00 5B      [17]  542 	call	_cpct_drawSprite
                            543 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4DC7 21 46 B4      [10]  544 	ld	hl, #0xb446
   4DCA E5            [11]  545 	push	hl
   4DCB 21 00 C0      [10]  546 	ld	hl, #0xc000
   4DCE E5            [11]  547 	push	hl
   4DCF CD B3 5C      [17]  548 	call	_cpct_getScreenPtr
                            549 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);
   4DD2 E5            [11]  550 	push	hl
   4DD3 3E 0A         [ 7]  551 	ld	a, #0x0a
   4DD5 F5            [11]  552 	push	af
   4DD6 33            [ 6]  553 	inc	sp
   4DD7 3A 76 5D      [13]  554 	ld	a, (_currentweapon)
   4DDA F5            [11]  555 	push	af
   4DDB 33            [ 6]  556 	inc	sp
   4DDC CD A5 5B      [17]  557 	call	__moduchar
   4DDF F1            [10]  558 	pop	af
   4DE0 C1            [10]  559 	pop	bc
   4DE1 26 00         [ 7]  560 	ld	h, #0x00
   4DE3 29            [11]  561 	add	hl, hl
   4DE4 11 82 5D      [10]  562 	ld	de, #_hudnumbers
   4DE7 19            [11]  563 	add	hl, de
   4DE8 5E            [ 7]  564 	ld	e, (hl)
   4DE9 23            [ 6]  565 	inc	hl
   4DEA 56            [ 7]  566 	ld	d, (hl)
   4DEB 21 08 08      [10]  567 	ld	hl, #0x0808
   4DEE E5            [11]  568 	push	hl
   4DEF C5            [11]  569 	push	bc
   4DF0 D5            [11]  570 	push	de
   4DF1 CD 00 5B      [17]  571 	call	_cpct_drawSprite
   4DF4 C9            [10]  572 	ret
                            573 	.area _CODE
                            574 	.area _INITIALIZER
   5D9D                     575 __xinit__hudnumbers:
   5D9D 22 4C               576 	.dw __hud_dummy_sprite
   5D9F 22 4C               577 	.dw __hud_dummy_sprite
   5DA1 22 4C               578 	.dw __hud_dummy_sprite
   5DA3 22 4C               579 	.dw __hud_dummy_sprite
   5DA5 22 4C               580 	.dw __hud_dummy_sprite
   5DA7 22 4C               581 	.dw __hud_dummy_sprite
   5DA9 22 4C               582 	.dw __hud_dummy_sprite
   5DAB 22 4C               583 	.dw __hud_dummy_sprite
   5DAD 22 4C               584 	.dw __hud_dummy_sprite
   5DAF 22 4C               585 	.dw __hud_dummy_sprite
                            586 	.area _CABS (ABS)
