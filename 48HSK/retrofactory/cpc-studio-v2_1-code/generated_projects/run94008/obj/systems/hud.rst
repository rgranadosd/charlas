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
   48C7                      23 _currenthealth:
   48C7                      24 	.ds 1
   48C8                      25 _currentscore:
   48C8                      26 	.ds 2
   48CA                      27 _currenttime:
   48CA                      28 	.ds 1
   48CB                      29 _currentlives:
   48CB                      30 	.ds 1
                             31 ;--------------------------------------------------------
                             32 ; ram data
                             33 ;--------------------------------------------------------
                             34 	.area _INITIALIZED
   48D1                      35 _hudnumbers:
   48D1                      36 	.ds 20
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
                             57 ;src/systems/hud.c:18: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                             58 ;	---------------------------------
                             59 ; Function hud_draw_digits
                             60 ; ---------------------------------
   40BF                      61 _hud_draw_digits:
   40BF DD E5         [15]   62 	push	ix
   40C1 DD 21 00 00   [14]   63 	ld	ix,#0
   40C5 DD 39         [15]   64 	add	ix,sp
   40C7 3B            [ 6]   65 	dec	sp
                             66 ;src/systems/hud.c:24: divisor = 1;
   40C8 01 01 00      [10]   67 	ld	bc, #0x0001
                             68 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   40CB 1E 01         [ 7]   69 	ld	e, #0x01
   40CD                      70 00106$:
   40CD 7B            [ 4]   71 	ld	a, e
   40CE DD 96 06      [19]   72 	sub	a, 6 (ix)
   40D1 30 0B         [12]   73 	jr	NC,00101$
                             74 ;src/systems/hud.c:26: divisor *= 10;
   40D3 69            [ 4]   75 	ld	l, c
   40D4 60            [ 4]   76 	ld	h, b
   40D5 29            [11]   77 	add	hl, hl
   40D6 29            [11]   78 	add	hl, hl
   40D7 09            [11]   79 	add	hl, bc
   40D8 29            [11]   80 	add	hl, hl
   40D9 4D            [ 4]   81 	ld	c, l
   40DA 44            [ 4]   82 	ld	b, h
                             83 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   40DB 1C            [ 4]   84 	inc	e
   40DC 18 EF         [12]   85 	jr	00106$
   40DE                      86 00101$:
                             87 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   40DE DD 36 FF 00   [19]   88 	ld	-1 (ix), #0x00
   40E2                      89 00109$:
   40E2 DD 7E FF      [19]   90 	ld	a, -1 (ix)
   40E5 DD 96 06      [19]   91 	sub	a, 6 (ix)
   40E8 30 7B         [12]   92 	jr	NC,00111$
                             93 ;src/systems/hud.c:30: digit = (u8)(value / divisor);
   40EA C5            [11]   94 	push	bc
   40EB C5            [11]   95 	push	bc
   40EC DD 6E 04      [19]   96 	ld	l,4 (ix)
   40EF DD 66 05      [19]   97 	ld	h,5 (ix)
   40F2 E5            [11]   98 	push	hl
   40F3 CD 37 46      [17]   99 	call	__divuint
   40F6 F1            [10]  100 	pop	af
   40F7 F1            [10]  101 	pop	af
   40F8 5D            [ 4]  102 	ld	e, l
   40F9 C1            [10]  103 	pop	bc
                            104 ;src/systems/hud.c:31: value = (u16)(value % divisor);
   40FA C5            [11]  105 	push	bc
   40FB D5            [11]  106 	push	de
   40FC C5            [11]  107 	push	bc
   40FD DD 6E 04      [19]  108 	ld	l,4 (ix)
   4100 DD 66 05      [19]  109 	ld	h,5 (ix)
   4103 E5            [11]  110 	push	hl
   4104 CD 9F 47      [17]  111 	call	__moduint
   4107 F1            [10]  112 	pop	af
   4108 F1            [10]  113 	pop	af
   4109 D1            [10]  114 	pop	de
   410A C1            [10]  115 	pop	bc
   410B DD 75 04      [19]  116 	ld	4 (ix), l
   410E DD 74 05      [19]  117 	ld	5 (ix), h
                            118 ;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   4111 DD 7E FF      [19]  119 	ld	a, -1 (ix)
   4114 07            [ 4]  120 	rlca
   4115 07            [ 4]  121 	rlca
   4116 07            [ 4]  122 	rlca
   4117 E6 F8         [ 7]  123 	and	a, #0xf8
   4119 57            [ 4]  124 	ld	d, a
   411A DD 7E 07      [19]  125 	ld	a, 7 (ix)
   411D 82            [ 4]  126 	add	a, d
   411E 57            [ 4]  127 	ld	d, a
   411F C5            [11]  128 	push	bc
   4120 D5            [11]  129 	push	de
   4121 DD 7E 08      [19]  130 	ld	a, 8 (ix)
   4124 F5            [11]  131 	push	af
   4125 33            [ 6]  132 	inc	sp
   4126 D5            [11]  133 	push	de
   4127 33            [ 6]  134 	inc	sp
   4128 21 00 C0      [10]  135 	ld	hl, #0xc000
   412B E5            [11]  136 	push	hl
   412C CD A1 48      [17]  137 	call	_cpct_getScreenPtr
   412F D1            [10]  138 	pop	de
   4130 C1            [10]  139 	pop	bc
                            140 ;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
   4131 E5            [11]  141 	push	hl
   4132 FD E1         [14]  142 	pop	iy
   4134 26 00         [ 7]  143 	ld	h, #0x00
   4136 6B            [ 4]  144 	ld	l, e
   4137 29            [11]  145 	add	hl, hl
   4138 11 D1 48      [10]  146 	ld	de, #_hudnumbers
   413B 19            [11]  147 	add	hl, de
   413C 5E            [ 7]  148 	ld	e, (hl)
   413D 23            [ 6]  149 	inc	hl
   413E 56            [ 7]  150 	ld	d, (hl)
   413F C5            [11]  151 	push	bc
   4140 21 08 08      [10]  152 	ld	hl, #0x0808
   4143 E5            [11]  153 	push	hl
   4144 FD E5         [15]  154 	push	iy
   4146 D5            [11]  155 	push	de
   4147 CD EE 46      [17]  156 	call	_cpct_drawSprite
   414A C1            [10]  157 	pop	bc
                            158 ;src/systems/hud.c:36: if (divisor > 1) {
   414B 3E 01         [ 7]  159 	ld	a, #0x01
   414D B9            [ 4]  160 	cp	a, c
   414E 3E 00         [ 7]  161 	ld	a, #0x00
   4150 98            [ 4]  162 	sbc	a, b
   4151 30 0C         [12]  163 	jr	NC,00110$
                            164 ;src/systems/hud.c:37: divisor /= 10;
   4153 21 0A 00      [10]  165 	ld	hl, #0x000a
   4156 E5            [11]  166 	push	hl
   4157 C5            [11]  167 	push	bc
   4158 CD 37 46      [17]  168 	call	__divuint
   415B F1            [10]  169 	pop	af
   415C F1            [10]  170 	pop	af
   415D 4D            [ 4]  171 	ld	c, l
   415E 44            [ 4]  172 	ld	b, h
   415F                     173 00110$:
                            174 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   415F DD 34 FF      [23]  175 	inc	-1 (ix)
   4162 C3 E2 40      [10]  176 	jp	00109$
   4165                     177 00111$:
   4165 33            [ 6]  178 	inc	sp
   4166 DD E1         [14]  179 	pop	ix
   4168 C9            [10]  180 	ret
   4169                     181 __hud_dummy_sprite:
   4169 00                  182 	.db #0x00	; 0
   416A 00                  183 	.db 0x00
   416B 00                  184 	.db 0x00
   416C 00                  185 	.db 0x00
   416D 00                  186 	.db 0x00
   416E 00                  187 	.db 0x00
   416F 00                  188 	.db 0x00
   4170 00                  189 	.db 0x00
   4171 00                  190 	.db 0x00
   4172 00                  191 	.db 0x00
   4173 00                  192 	.db 0x00
   4174 00                  193 	.db 0x00
   4175 00                  194 	.db 0x00
   4176 00                  195 	.db 0x00
   4177 00                  196 	.db 0x00
   4178 00                  197 	.db 0x00
   4179 00                  198 	.db 0x00
   417A 00                  199 	.db 0x00
   417B 00                  200 	.db 0x00
   417C 00                  201 	.db 0x00
   417D 00                  202 	.db 0x00
   417E 00                  203 	.db 0x00
   417F 00                  204 	.db 0x00
   4180 00                  205 	.db 0x00
   4181 00                  206 	.db 0x00
   4182 00                  207 	.db 0x00
   4183 00                  208 	.db 0x00
   4184 00                  209 	.db 0x00
   4185 00                  210 	.db 0x00
   4186 00                  211 	.db 0x00
   4187 00                  212 	.db 0x00
   4188 00                  213 	.db 0x00
   4189 00                  214 	.db 0x00
   418A 00                  215 	.db 0x00
   418B 00                  216 	.db 0x00
   418C 00                  217 	.db 0x00
   418D 00                  218 	.db 0x00
   418E 00                  219 	.db 0x00
   418F 00                  220 	.db 0x00
   4190 00                  221 	.db 0x00
   4191 00                  222 	.db 0x00
   4192 00                  223 	.db 0x00
   4193 00                  224 	.db 0x00
   4194 00                  225 	.db 0x00
   4195 00                  226 	.db 0x00
   4196 00                  227 	.db 0x00
   4197 00                  228 	.db 0x00
   4198 00                  229 	.db 0x00
   4199 00                  230 	.db 0x00
   419A 00                  231 	.db 0x00
   419B 00                  232 	.db 0x00
   419C 00                  233 	.db 0x00
   419D 00                  234 	.db 0x00
   419E 00                  235 	.db 0x00
   419F 00                  236 	.db 0x00
   41A0 00                  237 	.db 0x00
   41A1 00                  238 	.db 0x00
   41A2 00                  239 	.db 0x00
   41A3 00                  240 	.db 0x00
   41A4 00                  241 	.db 0x00
   41A5 00                  242 	.db 0x00
   41A6 00                  243 	.db 0x00
   41A7 00                  244 	.db 0x00
   41A8 00                  245 	.db 0x00
   41A9                     246 _hudhealth:
   41A9 00                  247 	.db #0x00	; 0
   41AA 00                  248 	.db 0x00
   41AB 00                  249 	.db 0x00
   41AC 00                  250 	.db 0x00
   41AD 00                  251 	.db 0x00
   41AE 00                  252 	.db 0x00
   41AF 00                  253 	.db 0x00
   41B0 00                  254 	.db 0x00
   41B1 00                  255 	.db 0x00
   41B2 00                  256 	.db 0x00
   41B3 00                  257 	.db 0x00
   41B4 00                  258 	.db 0x00
   41B5 00                  259 	.db 0x00
   41B6 00                  260 	.db 0x00
   41B7 00                  261 	.db 0x00
   41B8 00                  262 	.db 0x00
   41B9 00                  263 	.db 0x00
   41BA 00                  264 	.db 0x00
   41BB 00                  265 	.db 0x00
   41BC 00                  266 	.db 0x00
   41BD 00                  267 	.db 0x00
   41BE 00                  268 	.db 0x00
   41BF 00                  269 	.db 0x00
   41C0 00                  270 	.db 0x00
   41C1 00                  271 	.db 0x00
   41C2 00                  272 	.db 0x00
   41C3 00                  273 	.db 0x00
   41C4 00                  274 	.db 0x00
   41C5 00                  275 	.db 0x00
   41C6 00                  276 	.db 0x00
   41C7 00                  277 	.db 0x00
   41C8 00                  278 	.db 0x00
   41C9 00                  279 	.db 0x00
   41CA 00                  280 	.db 0x00
   41CB 00                  281 	.db 0x00
   41CC 00                  282 	.db 0x00
   41CD 00                  283 	.db 0x00
   41CE 00                  284 	.db 0x00
   41CF 00                  285 	.db 0x00
   41D0 00                  286 	.db 0x00
   41D1 00                  287 	.db 0x00
   41D2 00                  288 	.db 0x00
   41D3 00                  289 	.db 0x00
   41D4 00                  290 	.db 0x00
   41D5 00                  291 	.db 0x00
   41D6 00                  292 	.db 0x00
   41D7 00                  293 	.db 0x00
   41D8 00                  294 	.db 0x00
   41D9 00                  295 	.db 0x00
   41DA 00                  296 	.db 0x00
   41DB 00                  297 	.db 0x00
   41DC 00                  298 	.db 0x00
   41DD 00                  299 	.db 0x00
   41DE 00                  300 	.db 0x00
   41DF 00                  301 	.db 0x00
   41E0 00                  302 	.db 0x00
   41E1 00                  303 	.db 0x00
   41E2 00                  304 	.db 0x00
   41E3 00                  305 	.db 0x00
   41E4 00                  306 	.db 0x00
   41E5 00                  307 	.db 0x00
   41E6 00                  308 	.db 0x00
   41E7 00                  309 	.db 0x00
   41E8 00                  310 	.db 0x00
   41E9                     311 _hudlives:
   41E9 00                  312 	.db #0x00	; 0
   41EA 00                  313 	.db 0x00
   41EB 00                  314 	.db 0x00
   41EC 00                  315 	.db 0x00
   41ED 00                  316 	.db 0x00
   41EE 00                  317 	.db 0x00
   41EF 00                  318 	.db 0x00
   41F0 00                  319 	.db 0x00
   41F1 00                  320 	.db 0x00
   41F2 00                  321 	.db 0x00
   41F3 00                  322 	.db 0x00
   41F4 00                  323 	.db 0x00
   41F5 00                  324 	.db 0x00
   41F6 00                  325 	.db 0x00
   41F7 00                  326 	.db 0x00
   41F8 00                  327 	.db 0x00
   41F9 00                  328 	.db 0x00
   41FA 00                  329 	.db 0x00
   41FB 00                  330 	.db 0x00
   41FC 00                  331 	.db 0x00
   41FD 00                  332 	.db 0x00
   41FE 00                  333 	.db 0x00
   41FF 00                  334 	.db 0x00
   4200 00                  335 	.db 0x00
   4201 00                  336 	.db 0x00
   4202 00                  337 	.db 0x00
   4203 00                  338 	.db 0x00
   4204 00                  339 	.db 0x00
   4205 00                  340 	.db 0x00
   4206 00                  341 	.db 0x00
   4207 00                  342 	.db 0x00
   4208 00                  343 	.db 0x00
   4209 00                  344 	.db 0x00
   420A 00                  345 	.db 0x00
   420B 00                  346 	.db 0x00
   420C 00                  347 	.db 0x00
   420D 00                  348 	.db 0x00
   420E 00                  349 	.db 0x00
   420F 00                  350 	.db 0x00
   4210 00                  351 	.db 0x00
   4211 00                  352 	.db 0x00
   4212 00                  353 	.db 0x00
   4213 00                  354 	.db 0x00
   4214 00                  355 	.db 0x00
   4215 00                  356 	.db 0x00
   4216 00                  357 	.db 0x00
   4217 00                  358 	.db 0x00
   4218 00                  359 	.db 0x00
   4219 00                  360 	.db 0x00
   421A 00                  361 	.db 0x00
   421B 00                  362 	.db 0x00
   421C 00                  363 	.db 0x00
   421D 00                  364 	.db 0x00
   421E 00                  365 	.db 0x00
   421F 00                  366 	.db 0x00
   4220 00                  367 	.db 0x00
   4221 00                  368 	.db 0x00
   4222 00                  369 	.db 0x00
   4223 00                  370 	.db 0x00
   4224 00                  371 	.db 0x00
   4225 00                  372 	.db 0x00
   4226 00                  373 	.db 0x00
   4227 00                  374 	.db 0x00
   4228 00                  375 	.db 0x00
                            376 ;src/systems/hud.c:42: void hudinit(void) {
                            377 ;	---------------------------------
                            378 ; Function hudinit
                            379 ; ---------------------------------
   4229                     380 _hudinit::
                            381 ;src/systems/hud.c:43: currenthealth = 3;
   4229 21 C7 48      [10]  382 	ld	hl,#_currenthealth + 0
   422C 36 03         [10]  383 	ld	(hl), #0x03
                            384 ;src/systems/hud.c:44: currentscore  = 0;
   422E 21 00 00      [10]  385 	ld	hl, #0x0000
   4231 22 C8 48      [16]  386 	ld	(_currentscore), hl
                            387 ;src/systems/hud.c:45: currenttime   = 90;
   4234 21 CA 48      [10]  388 	ld	hl,#_currenttime + 0
   4237 36 5A         [10]  389 	ld	(hl), #0x5a
                            390 ;src/systems/hud.c:46: currentlives  = 3;
   4239 21 CB 48      [10]  391 	ld	hl,#_currentlives + 0
   423C 36 03         [10]  392 	ld	(hl), #0x03
   423E C9            [10]  393 	ret
                            394 ;src/systems/hud.c:49: void hudupdate(u8 health, u16 score, u8 time, u8 lives) {
                            395 ;	---------------------------------
                            396 ; Function hudupdate
                            397 ; ---------------------------------
   423F                     398 _hudupdate::
                            399 ;src/systems/hud.c:50: currenthealth = health;
   423F 21 02 00      [10]  400 	ld	hl, #2+0
   4242 39            [11]  401 	add	hl, sp
   4243 7E            [ 7]  402 	ld	a, (hl)
   4244 32 C7 48      [13]  403 	ld	(#_currenthealth + 0),a
                            404 ;src/systems/hud.c:51: currentscore  = score;
   4247 21 03 00      [10]  405 	ld	hl, #3+0
   424A 39            [11]  406 	add	hl, sp
   424B 7E            [ 7]  407 	ld	a, (hl)
   424C 32 C8 48      [13]  408 	ld	(#_currentscore + 0),a
   424F 21 04 00      [10]  409 	ld	hl, #3+1
   4252 39            [11]  410 	add	hl, sp
   4253 7E            [ 7]  411 	ld	a, (hl)
   4254 32 C9 48      [13]  412 	ld	(#_currentscore + 1),a
                            413 ;src/systems/hud.c:52: currenttime   = time;
   4257 21 05 00      [10]  414 	ld	hl, #5+0
   425A 39            [11]  415 	add	hl, sp
   425B 7E            [ 7]  416 	ld	a, (hl)
   425C 32 CA 48      [13]  417 	ld	(#_currenttime + 0),a
                            418 ;src/systems/hud.c:53: currentlives  = lives;
   425F 21 06 00      [10]  419 	ld	hl, #6+0
   4262 39            [11]  420 	add	hl, sp
   4263 7E            [ 7]  421 	ld	a, (hl)
   4264 32 CB 48      [13]  422 	ld	(#_currentlives + 0),a
   4267 C9            [10]  423 	ret
                            424 ;src/systems/hud.c:56: void hudrender(void) {
                            425 ;	---------------------------------
                            426 ; Function hudrender
                            427 ; ---------------------------------
   4268                     428 _hudrender::
                            429 ;src/systems/hud.c:62: for (i = 0; i < currenthealth; ++i) {
   4268 0E 00         [ 7]  430 	ld	c, #0x00
   426A                     431 00103$:
   426A 21 C7 48      [10]  432 	ld	hl, #_currenthealth
                            433 ;src/systems/hud.c:63: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);
   426D 79            [ 4]  434 	ld	a,c
   426E BE            [ 7]  435 	cp	a,(hl)
   426F 30 26         [12]  436 	jr	NC,00101$
   4271 07            [ 4]  437 	rlca
   4272 07            [ 4]  438 	rlca
   4273 07            [ 4]  439 	rlca
   4274 E6 F8         [ 7]  440 	and	a, #0xf8
   4276 47            [ 4]  441 	ld	b, a
   4277 04            [ 4]  442 	inc	b
   4278 04            [ 4]  443 	inc	b
   4279 C5            [11]  444 	push	bc
   427A 3E 02         [ 7]  445 	ld	a, #0x02
   427C F5            [11]  446 	push	af
   427D 33            [ 6]  447 	inc	sp
   427E C5            [11]  448 	push	bc
   427F 33            [ 6]  449 	inc	sp
   4280 21 00 C0      [10]  450 	ld	hl, #0xc000
   4283 E5            [11]  451 	push	hl
   4284 CD A1 48      [17]  452 	call	_cpct_getScreenPtr
   4287 11 08 08      [10]  453 	ld	de, #0x0808
   428A D5            [11]  454 	push	de
   428B E5            [11]  455 	push	hl
   428C 21 A9 41      [10]  456 	ld	hl, #_hudhealth
   428F E5            [11]  457 	push	hl
   4290 CD EE 46      [17]  458 	call	_cpct_drawSprite
   4293 C1            [10]  459 	pop	bc
                            460 ;src/systems/hud.c:62: for (i = 0; i < currenthealth; ++i) {
   4294 0C            [ 4]  461 	inc	c
   4295 18 D3         [12]  462 	jr	00103$
   4297                     463 00101$:
                            464 ;src/systems/hud.c:67: scoretemp = currentscore;
   4297 2A C8 48      [16]  465 	ld	hl, (_currentscore)
                            466 ;src/systems/hud.c:68: hud_draw_digits(scoretemp, 5, 88, 2);
   429A 01 58 02      [10]  467 	ld	bc, #0x0258
   429D C5            [11]  468 	push	bc
   429E 3E 05         [ 7]  469 	ld	a, #0x05
   42A0 F5            [11]  470 	push	af
   42A1 33            [ 6]  471 	inc	sp
   42A2 E5            [11]  472 	push	hl
   42A3 CD BF 40      [17]  473 	call	_hud_draw_digits
   42A6 F1            [10]  474 	pop	af
   42A7 F1            [10]  475 	pop	af
   42A8 33            [ 6]  476 	inc	sp
                            477 ;src/systems/hud.c:70: timetemp = currenttime;
   42A9 21 CA 48      [10]  478 	ld	hl,#_currenttime + 0
   42AC 4E            [ 7]  479 	ld	c, (hl)
                            480 ;src/systems/hud.c:71: hud_draw_digits((u16)timetemp, 3, 56, 2);
   42AD 06 00         [ 7]  481 	ld	b, #0x00
   42AF 21 38 02      [10]  482 	ld	hl, #0x0238
   42B2 E5            [11]  483 	push	hl
   42B3 3E 03         [ 7]  484 	ld	a, #0x03
   42B5 F5            [11]  485 	push	af
   42B6 33            [ 6]  486 	inc	sp
   42B7 C5            [11]  487 	push	bc
   42B8 CD BF 40      [17]  488 	call	_hud_draw_digits
   42BB F1            [10]  489 	pop	af
                            490 ;src/systems/hud.c:73: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   42BC 33            [ 6]  491 	inc	sp
   42BD 21 02 B4      [10]  492 	ld	hl,#0xb402
   42C0 E3            [19]  493 	ex	(sp),hl
   42C1 21 00 C0      [10]  494 	ld	hl, #0xc000
   42C4 E5            [11]  495 	push	hl
   42C5 CD A1 48      [17]  496 	call	_cpct_getScreenPtr
                            497 ;src/systems/hud.c:74: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   42C8 01 E9 41      [10]  498 	ld	bc, #_hudlives+0
   42CB 11 08 08      [10]  499 	ld	de, #0x0808
   42CE D5            [11]  500 	push	de
   42CF E5            [11]  501 	push	hl
   42D0 C5            [11]  502 	push	bc
   42D1 CD EE 46      [17]  503 	call	_cpct_drawSprite
                            504 ;src/systems/hud.c:76: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   42D4 21 0C B4      [10]  505 	ld	hl, #0xb40c
   42D7 E5            [11]  506 	push	hl
   42D8 21 00 C0      [10]  507 	ld	hl, #0xc000
   42DB E5            [11]  508 	push	hl
   42DC CD A1 48      [17]  509 	call	_cpct_getScreenPtr
                            510 ;src/systems/hud.c:77: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
   42DF E5            [11]  511 	push	hl
   42E0 3E 0A         [ 7]  512 	ld	a, #0x0a
   42E2 F5            [11]  513 	push	af
   42E3 33            [ 6]  514 	inc	sp
   42E4 3A CB 48      [13]  515 	ld	a, (_currentlives)
   42E7 F5            [11]  516 	push	af
   42E8 33            [ 6]  517 	inc	sp
   42E9 CD 93 47      [17]  518 	call	__moduchar
   42EC F1            [10]  519 	pop	af
   42ED C1            [10]  520 	pop	bc
   42EE 26 00         [ 7]  521 	ld	h, #0x00
   42F0 29            [11]  522 	add	hl, hl
   42F1 11 D1 48      [10]  523 	ld	de, #_hudnumbers
   42F4 19            [11]  524 	add	hl, de
   42F5 5E            [ 7]  525 	ld	e, (hl)
   42F6 23            [ 6]  526 	inc	hl
   42F7 56            [ 7]  527 	ld	d, (hl)
   42F8 21 08 08      [10]  528 	ld	hl, #0x0808
   42FB E5            [11]  529 	push	hl
   42FC C5            [11]  530 	push	bc
   42FD D5            [11]  531 	push	de
   42FE CD EE 46      [17]  532 	call	_cpct_drawSprite
   4301 C9            [10]  533 	ret
                            534 	.area _CODE
                            535 	.area _INITIALIZER
   48E8                     536 __xinit__hudnumbers:
   48E8 69 41               537 	.dw __hud_dummy_sprite
   48EA 69 41               538 	.dw __hud_dummy_sprite
   48EC 69 41               539 	.dw __hud_dummy_sprite
   48EE 69 41               540 	.dw __hud_dummy_sprite
   48F0 69 41               541 	.dw __hud_dummy_sprite
   48F2 69 41               542 	.dw __hud_dummy_sprite
   48F4 69 41               543 	.dw __hud_dummy_sprite
   48F6 69 41               544 	.dw __hud_dummy_sprite
   48F8 69 41               545 	.dw __hud_dummy_sprite
   48FA 69 41               546 	.dw __hud_dummy_sprite
                            547 	.area _CABS (ABS)
