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
   5A7E                      23 _currenthealth:
   5A7E                      24 	.ds 1
   5A7F                      25 _currentscore:
   5A7F                      26 	.ds 2
   5A81                      27 _currenttime:
   5A81                      28 	.ds 1
   5A82                      29 _currentlives:
   5A82                      30 	.ds 1
   5A83                      31 _currentweapon:
   5A83                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
   5A8E                      37 _hudnumbers:
   5A8E                      38 	.ds 20
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
   4819                      63 _hud_draw_digits:
   4819 DD E5         [15]   64 	push	ix
   481B DD 21 00 00   [14]   65 	ld	ix,#0
   481F DD 39         [15]   66 	add	ix,sp
   4821 3B            [ 6]   67 	dec	sp
                             68 ;src/systems/hud.c:24: divisor = 1;
   4822 01 01 00      [10]   69 	ld	bc, #0x0001
                             70 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4825 1E 01         [ 7]   71 	ld	e, #0x01
   4827                      72 00106$:
   4827 7B            [ 4]   73 	ld	a, e
   4828 DD 96 06      [19]   74 	sub	a, 6 (ix)
   482B 30 0B         [12]   75 	jr	NC,00101$
                             76 ;src/systems/hud.c:26: divisor *= 10;
   482D 69            [ 4]   77 	ld	l, c
   482E 60            [ 4]   78 	ld	h, b
   482F 29            [11]   79 	add	hl, hl
   4830 29            [11]   80 	add	hl, hl
   4831 09            [11]   81 	add	hl, bc
   4832 29            [11]   82 	add	hl, hl
   4833 4D            [ 4]   83 	ld	c, l
   4834 44            [ 4]   84 	ld	b, h
                             85 ;src/systems/hud.c:25: for (i = 1; i < digits; ++i) {
   4835 1C            [ 4]   86 	inc	e
   4836 18 EF         [12]   87 	jr	00106$
   4838                      88 00101$:
                             89 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   4838 DD 36 FF 00   [19]   90 	ld	-1 (ix), #0x00
   483C                      91 00109$:
   483C DD 7E FF      [19]   92 	ld	a, -1 (ix)
   483F DD 96 06      [19]   93 	sub	a, 6 (ix)
   4842 30 7B         [12]   94 	jr	NC,00111$
                             95 ;src/systems/hud.c:30: digit = (u8)(value / divisor);
   4844 C5            [11]   96 	push	bc
   4845 C5            [11]   97 	push	bc
   4846 DD 6E 04      [19]   98 	ld	l,4 (ix)
   4849 DD 66 05      [19]   99 	ld	h,5 (ix)
   484C E5            [11]  100 	push	hl
   484D CD 6B 57      [17]  101 	call	__divuint
   4850 F1            [10]  102 	pop	af
   4851 F1            [10]  103 	pop	af
   4852 5D            [ 4]  104 	ld	e, l
   4853 C1            [10]  105 	pop	bc
                            106 ;src/systems/hud.c:31: value = (u16)(value % divisor);
   4854 C5            [11]  107 	push	bc
   4855 D5            [11]  108 	push	de
   4856 C5            [11]  109 	push	bc
   4857 DD 6E 04      [19]  110 	ld	l,4 (ix)
   485A DD 66 05      [19]  111 	ld	h,5 (ix)
   485D E5            [11]  112 	push	hl
   485E CD D3 58      [17]  113 	call	__moduint
   4861 F1            [10]  114 	pop	af
   4862 F1            [10]  115 	pop	af
   4863 D1            [10]  116 	pop	de
   4864 C1            [10]  117 	pop	bc
   4865 DD 75 04      [19]  118 	ld	4 (ix), l
   4868 DD 74 05      [19]  119 	ld	5 (ix), h
                            120 ;src/systems/hud.c:33: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   486B DD 7E FF      [19]  121 	ld	a, -1 (ix)
   486E 07            [ 4]  122 	rlca
   486F 07            [ 4]  123 	rlca
   4870 07            [ 4]  124 	rlca
   4871 E6 F8         [ 7]  125 	and	a, #0xf8
   4873 57            [ 4]  126 	ld	d, a
   4874 DD 7E 07      [19]  127 	ld	a, 7 (ix)
   4877 82            [ 4]  128 	add	a, d
   4878 57            [ 4]  129 	ld	d, a
   4879 C5            [11]  130 	push	bc
   487A D5            [11]  131 	push	de
   487B DD 7E 08      [19]  132 	ld	a, 8 (ix)
   487E F5            [11]  133 	push	af
   487F 33            [ 6]  134 	inc	sp
   4880 D5            [11]  135 	push	de
   4881 33            [ 6]  136 	inc	sp
   4882 21 00 C0      [10]  137 	ld	hl, #0xc000
   4885 E5            [11]  138 	push	hl
   4886 CD D5 59      [17]  139 	call	_cpct_getScreenPtr
   4889 D1            [10]  140 	pop	de
   488A C1            [10]  141 	pop	bc
                            142 ;src/systems/hud.c:34: cpct_drawSprite((u8*)hudnumbers[digit], pvmem, 8, 8);
   488B E5            [11]  143 	push	hl
   488C FD E1         [14]  144 	pop	iy
   488E 26 00         [ 7]  145 	ld	h, #0x00
   4890 6B            [ 4]  146 	ld	l, e
   4891 29            [11]  147 	add	hl, hl
   4892 11 8E 5A      [10]  148 	ld	de, #_hudnumbers
   4895 19            [11]  149 	add	hl, de
   4896 5E            [ 7]  150 	ld	e, (hl)
   4897 23            [ 6]  151 	inc	hl
   4898 56            [ 7]  152 	ld	d, (hl)
   4899 C5            [11]  153 	push	bc
   489A 21 08 08      [10]  154 	ld	hl, #0x0808
   489D E5            [11]  155 	push	hl
   489E FD E5         [15]  156 	push	iy
   48A0 D5            [11]  157 	push	de
   48A1 CD 22 58      [17]  158 	call	_cpct_drawSprite
   48A4 C1            [10]  159 	pop	bc
                            160 ;src/systems/hud.c:36: if (divisor > 1) {
   48A5 3E 01         [ 7]  161 	ld	a, #0x01
   48A7 B9            [ 4]  162 	cp	a, c
   48A8 3E 00         [ 7]  163 	ld	a, #0x00
   48AA 98            [ 4]  164 	sbc	a, b
   48AB 30 0C         [12]  165 	jr	NC,00110$
                            166 ;src/systems/hud.c:37: divisor /= 10;
   48AD 21 0A 00      [10]  167 	ld	hl, #0x000a
   48B0 E5            [11]  168 	push	hl
   48B1 C5            [11]  169 	push	bc
   48B2 CD 6B 57      [17]  170 	call	__divuint
   48B5 F1            [10]  171 	pop	af
   48B6 F1            [10]  172 	pop	af
   48B7 4D            [ 4]  173 	ld	c, l
   48B8 44            [ 4]  174 	ld	b, h
   48B9                     175 00110$:
                            176 ;src/systems/hud.c:29: for (i = 0; i < digits; ++i) {
   48B9 DD 34 FF      [23]  177 	inc	-1 (ix)
   48BC C3 3C 48      [10]  178 	jp	00109$
   48BF                     179 00111$:
   48BF 33            [ 6]  180 	inc	sp
   48C0 DD E1         [14]  181 	pop	ix
   48C2 C9            [10]  182 	ret
   48C3                     183 __hud_dummy_sprite:
   48C3 00                  184 	.db #0x00	; 0
   48C4 00                  185 	.db 0x00
   48C5 00                  186 	.db 0x00
   48C6 00                  187 	.db 0x00
   48C7 00                  188 	.db 0x00
   48C8 00                  189 	.db 0x00
   48C9 00                  190 	.db 0x00
   48CA 00                  191 	.db 0x00
   48CB 00                  192 	.db 0x00
   48CC 00                  193 	.db 0x00
   48CD 00                  194 	.db 0x00
   48CE 00                  195 	.db 0x00
   48CF 00                  196 	.db 0x00
   48D0 00                  197 	.db 0x00
   48D1 00                  198 	.db 0x00
   48D2 00                  199 	.db 0x00
   48D3 00                  200 	.db 0x00
   48D4 00                  201 	.db 0x00
   48D5 00                  202 	.db 0x00
   48D6 00                  203 	.db 0x00
   48D7 00                  204 	.db 0x00
   48D8 00                  205 	.db 0x00
   48D9 00                  206 	.db 0x00
   48DA 00                  207 	.db 0x00
   48DB 00                  208 	.db 0x00
   48DC 00                  209 	.db 0x00
   48DD 00                  210 	.db 0x00
   48DE 00                  211 	.db 0x00
   48DF 00                  212 	.db 0x00
   48E0 00                  213 	.db 0x00
   48E1 00                  214 	.db 0x00
   48E2 00                  215 	.db 0x00
   48E3 00                  216 	.db 0x00
   48E4 00                  217 	.db 0x00
   48E5 00                  218 	.db 0x00
   48E6 00                  219 	.db 0x00
   48E7 00                  220 	.db 0x00
   48E8 00                  221 	.db 0x00
   48E9 00                  222 	.db 0x00
   48EA 00                  223 	.db 0x00
   48EB 00                  224 	.db 0x00
   48EC 00                  225 	.db 0x00
   48ED 00                  226 	.db 0x00
   48EE 00                  227 	.db 0x00
   48EF 00                  228 	.db 0x00
   48F0 00                  229 	.db 0x00
   48F1 00                  230 	.db 0x00
   48F2 00                  231 	.db 0x00
   48F3 00                  232 	.db 0x00
   48F4 00                  233 	.db 0x00
   48F5 00                  234 	.db 0x00
   48F6 00                  235 	.db 0x00
   48F7 00                  236 	.db 0x00
   48F8 00                  237 	.db 0x00
   48F9 00                  238 	.db 0x00
   48FA 00                  239 	.db 0x00
   48FB 00                  240 	.db 0x00
   48FC 00                  241 	.db 0x00
   48FD 00                  242 	.db 0x00
   48FE 00                  243 	.db 0x00
   48FF 00                  244 	.db 0x00
   4900 00                  245 	.db 0x00
   4901 00                  246 	.db 0x00
   4902 00                  247 	.db 0x00
   4903                     248 _hudhealth:
   4903 00                  249 	.db #0x00	; 0
   4904 00                  250 	.db 0x00
   4905 00                  251 	.db 0x00
   4906 00                  252 	.db 0x00
   4907 00                  253 	.db 0x00
   4908 00                  254 	.db 0x00
   4909 00                  255 	.db 0x00
   490A 00                  256 	.db 0x00
   490B 00                  257 	.db 0x00
   490C 00                  258 	.db 0x00
   490D 00                  259 	.db 0x00
   490E 00                  260 	.db 0x00
   490F 00                  261 	.db 0x00
   4910 00                  262 	.db 0x00
   4911 00                  263 	.db 0x00
   4912 00                  264 	.db 0x00
   4913 00                  265 	.db 0x00
   4914 00                  266 	.db 0x00
   4915 00                  267 	.db 0x00
   4916 00                  268 	.db 0x00
   4917 00                  269 	.db 0x00
   4918 00                  270 	.db 0x00
   4919 00                  271 	.db 0x00
   491A 00                  272 	.db 0x00
   491B 00                  273 	.db 0x00
   491C 00                  274 	.db 0x00
   491D 00                  275 	.db 0x00
   491E 00                  276 	.db 0x00
   491F 00                  277 	.db 0x00
   4920 00                  278 	.db 0x00
   4921 00                  279 	.db 0x00
   4922 00                  280 	.db 0x00
   4923 00                  281 	.db 0x00
   4924 00                  282 	.db 0x00
   4925 00                  283 	.db 0x00
   4926 00                  284 	.db 0x00
   4927 00                  285 	.db 0x00
   4928 00                  286 	.db 0x00
   4929 00                  287 	.db 0x00
   492A 00                  288 	.db 0x00
   492B 00                  289 	.db 0x00
   492C 00                  290 	.db 0x00
   492D 00                  291 	.db 0x00
   492E 00                  292 	.db 0x00
   492F 00                  293 	.db 0x00
   4930 00                  294 	.db 0x00
   4931 00                  295 	.db 0x00
   4932 00                  296 	.db 0x00
   4933 00                  297 	.db 0x00
   4934 00                  298 	.db 0x00
   4935 00                  299 	.db 0x00
   4936 00                  300 	.db 0x00
   4937 00                  301 	.db 0x00
   4938 00                  302 	.db 0x00
   4939 00                  303 	.db 0x00
   493A 00                  304 	.db 0x00
   493B 00                  305 	.db 0x00
   493C 00                  306 	.db 0x00
   493D 00                  307 	.db 0x00
   493E 00                  308 	.db 0x00
   493F 00                  309 	.db 0x00
   4940 00                  310 	.db 0x00
   4941 00                  311 	.db 0x00
   4942 00                  312 	.db 0x00
   4943                     313 _hudlives:
   4943 00                  314 	.db #0x00	; 0
   4944 00                  315 	.db 0x00
   4945 00                  316 	.db 0x00
   4946 00                  317 	.db 0x00
   4947 00                  318 	.db 0x00
   4948 00                  319 	.db 0x00
   4949 00                  320 	.db 0x00
   494A 00                  321 	.db 0x00
   494B 00                  322 	.db 0x00
   494C 00                  323 	.db 0x00
   494D 00                  324 	.db 0x00
   494E 00                  325 	.db 0x00
   494F 00                  326 	.db 0x00
   4950 00                  327 	.db 0x00
   4951 00                  328 	.db 0x00
   4952 00                  329 	.db 0x00
   4953 00                  330 	.db 0x00
   4954 00                  331 	.db 0x00
   4955 00                  332 	.db 0x00
   4956 00                  333 	.db 0x00
   4957 00                  334 	.db 0x00
   4958 00                  335 	.db 0x00
   4959 00                  336 	.db 0x00
   495A 00                  337 	.db 0x00
   495B 00                  338 	.db 0x00
   495C 00                  339 	.db 0x00
   495D 00                  340 	.db 0x00
   495E 00                  341 	.db 0x00
   495F 00                  342 	.db 0x00
   4960 00                  343 	.db 0x00
   4961 00                  344 	.db 0x00
   4962 00                  345 	.db 0x00
   4963 00                  346 	.db 0x00
   4964 00                  347 	.db 0x00
   4965 00                  348 	.db 0x00
   4966 00                  349 	.db 0x00
   4967 00                  350 	.db 0x00
   4968 00                  351 	.db 0x00
   4969 00                  352 	.db 0x00
   496A 00                  353 	.db 0x00
   496B 00                  354 	.db 0x00
   496C 00                  355 	.db 0x00
   496D 00                  356 	.db 0x00
   496E 00                  357 	.db 0x00
   496F 00                  358 	.db 0x00
   4970 00                  359 	.db 0x00
   4971 00                  360 	.db 0x00
   4972 00                  361 	.db 0x00
   4973 00                  362 	.db 0x00
   4974 00                  363 	.db 0x00
   4975 00                  364 	.db 0x00
   4976 00                  365 	.db 0x00
   4977 00                  366 	.db 0x00
   4978 00                  367 	.db 0x00
   4979 00                  368 	.db 0x00
   497A 00                  369 	.db 0x00
   497B 00                  370 	.db 0x00
   497C 00                  371 	.db 0x00
   497D 00                  372 	.db 0x00
   497E 00                  373 	.db 0x00
   497F 00                  374 	.db 0x00
   4980 00                  375 	.db 0x00
   4981 00                  376 	.db 0x00
   4982 00                  377 	.db 0x00
                            378 ;src/systems/hud.c:42: void hudinit(void) {
                            379 ;	---------------------------------
                            380 ; Function hudinit
                            381 ; ---------------------------------
   4983                     382 _hudinit::
                            383 ;src/systems/hud.c:43: currenthealth = 3;
   4983 21 7E 5A      [10]  384 	ld	hl,#_currenthealth + 0
   4986 36 03         [10]  385 	ld	(hl), #0x03
                            386 ;src/systems/hud.c:44: currentscore  = 0;
   4988 21 00 00      [10]  387 	ld	hl, #0x0000
   498B 22 7F 5A      [16]  388 	ld	(_currentscore), hl
                            389 ;src/systems/hud.c:45: currenttime   = 90;
   498E 21 81 5A      [10]  390 	ld	hl,#_currenttime + 0
   4991 36 5A         [10]  391 	ld	(hl), #0x5a
                            392 ;src/systems/hud.c:46: currentlives  = 3;
   4993 21 82 5A      [10]  393 	ld	hl,#_currentlives + 0
   4996 36 03         [10]  394 	ld	(hl), #0x03
                            395 ;src/systems/hud.c:47: currentweapon = 0;
   4998 21 83 5A      [10]  396 	ld	hl,#_currentweapon + 0
   499B 36 00         [10]  397 	ld	(hl), #0x00
   499D C9            [10]  398 	ret
                            399 ;src/systems/hud.c:50: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            400 ;	---------------------------------
                            401 ; Function hudupdate
                            402 ; ---------------------------------
   499E                     403 _hudupdate::
                            404 ;src/systems/hud.c:51: currenthealth = lives;
   499E 21 02 00      [10]  405 	ld	hl, #2+0
   49A1 39            [11]  406 	add	hl, sp
   49A2 7E            [ 7]  407 	ld	a, (hl)
   49A3 32 7E 5A      [13]  408 	ld	(#_currenthealth + 0),a
                            409 ;src/systems/hud.c:52: currentscore  = score;
   49A6 21 03 00      [10]  410 	ld	hl, #3+0
   49A9 39            [11]  411 	add	hl, sp
   49AA 7E            [ 7]  412 	ld	a, (hl)
   49AB 32 7F 5A      [13]  413 	ld	(#_currentscore + 0),a
   49AE 21 04 00      [10]  414 	ld	hl, #3+1
   49B1 39            [11]  415 	add	hl, sp
   49B2 7E            [ 7]  416 	ld	a, (hl)
   49B3 32 80 5A      [13]  417 	ld	(#_currentscore + 1),a
                            418 ;src/systems/hud.c:53: currenttime   = time;
   49B6 21 05 00      [10]  419 	ld	hl, #5+0
   49B9 39            [11]  420 	add	hl, sp
   49BA 7E            [ 7]  421 	ld	a, (hl)
   49BB 32 81 5A      [13]  422 	ld	(#_currenttime + 0),a
                            423 ;src/systems/hud.c:54: currentlives  = lives;
   49BE 21 02 00      [10]  424 	ld	hl, #2+0
   49C1 39            [11]  425 	add	hl, sp
   49C2 7E            [ 7]  426 	ld	a, (hl)
   49C3 32 82 5A      [13]  427 	ld	(#_currentlives + 0),a
                            428 ;src/systems/hud.c:55: currentweapon = weapon;
   49C6 21 06 00      [10]  429 	ld	hl, #6+0
   49C9 39            [11]  430 	add	hl, sp
   49CA 7E            [ 7]  431 	ld	a, (hl)
   49CB 32 83 5A      [13]  432 	ld	(#_currentweapon + 0),a
   49CE C9            [10]  433 	ret
                            434 ;src/systems/hud.c:58: void hudrender(void) {
                            435 ;	---------------------------------
                            436 ; Function hudrender
                            437 ; ---------------------------------
   49CF                     438 _hudrender::
                            439 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   49CF 0E 00         [ 7]  440 	ld	c, #0x00
   49D1                     441 00103$:
   49D1 21 7E 5A      [10]  442 	ld	hl, #_currenthealth
                            443 ;src/systems/hud.c:65: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2 + (i * 8), 2);
   49D4 79            [ 4]  444 	ld	a,c
   49D5 BE            [ 7]  445 	cp	a,(hl)
   49D6 30 26         [12]  446 	jr	NC,00101$
   49D8 07            [ 4]  447 	rlca
   49D9 07            [ 4]  448 	rlca
   49DA 07            [ 4]  449 	rlca
   49DB E6 F8         [ 7]  450 	and	a, #0xf8
   49DD 47            [ 4]  451 	ld	b, a
   49DE 04            [ 4]  452 	inc	b
   49DF 04            [ 4]  453 	inc	b
   49E0 C5            [11]  454 	push	bc
   49E1 3E 02         [ 7]  455 	ld	a, #0x02
   49E3 F5            [11]  456 	push	af
   49E4 33            [ 6]  457 	inc	sp
   49E5 C5            [11]  458 	push	bc
   49E6 33            [ 6]  459 	inc	sp
   49E7 21 00 C0      [10]  460 	ld	hl, #0xc000
   49EA E5            [11]  461 	push	hl
   49EB CD D5 59      [17]  462 	call	_cpct_getScreenPtr
   49EE 11 08 08      [10]  463 	ld	de, #0x0808
   49F1 D5            [11]  464 	push	de
   49F2 E5            [11]  465 	push	hl
   49F3 21 03 49      [10]  466 	ld	hl, #_hudhealth
   49F6 E5            [11]  467 	push	hl
   49F7 CD 22 58      [17]  468 	call	_cpct_drawSprite
   49FA C1            [10]  469 	pop	bc
                            470 ;src/systems/hud.c:64: for (i = 0; i < currenthealth; ++i) {
   49FB 0C            [ 4]  471 	inc	c
   49FC 18 D3         [12]  472 	jr	00103$
   49FE                     473 00101$:
                            474 ;src/systems/hud.c:69: scoretemp = currentscore;
   49FE 2A 7F 5A      [16]  475 	ld	hl, (_currentscore)
                            476 ;src/systems/hud.c:70: hud_draw_digits(scoretemp, 5, 88, 2);
   4A01 01 58 02      [10]  477 	ld	bc, #0x0258
   4A04 C5            [11]  478 	push	bc
   4A05 3E 05         [ 7]  479 	ld	a, #0x05
   4A07 F5            [11]  480 	push	af
   4A08 33            [ 6]  481 	inc	sp
   4A09 E5            [11]  482 	push	hl
   4A0A CD 19 48      [17]  483 	call	_hud_draw_digits
   4A0D F1            [10]  484 	pop	af
   4A0E F1            [10]  485 	pop	af
   4A0F 33            [ 6]  486 	inc	sp
                            487 ;src/systems/hud.c:72: timetemp = currenttime;
   4A10 21 81 5A      [10]  488 	ld	hl,#_currenttime + 0
   4A13 4E            [ 7]  489 	ld	c, (hl)
                            490 ;src/systems/hud.c:73: hud_draw_digits((u16)timetemp, 3, 56, 2);
   4A14 06 00         [ 7]  491 	ld	b, #0x00
   4A16 21 38 02      [10]  492 	ld	hl, #0x0238
   4A19 E5            [11]  493 	push	hl
   4A1A 3E 03         [ 7]  494 	ld	a, #0x03
   4A1C F5            [11]  495 	push	af
   4A1D 33            [ 6]  496 	inc	sp
   4A1E C5            [11]  497 	push	bc
   4A1F CD 19 48      [17]  498 	call	_hud_draw_digits
   4A22 F1            [10]  499 	pop	af
                            500 ;src/systems/hud.c:75: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   4A23 33            [ 6]  501 	inc	sp
   4A24 21 02 B4      [10]  502 	ld	hl,#0xb402
   4A27 E3            [19]  503 	ex	(sp),hl
   4A28 21 00 C0      [10]  504 	ld	hl, #0xc000
   4A2B E5            [11]  505 	push	hl
   4A2C CD D5 59      [17]  506 	call	_cpct_getScreenPtr
                            507 ;src/systems/hud.c:76: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   4A2F 01 43 49      [10]  508 	ld	bc, #_hudlives+0
   4A32 11 08 08      [10]  509 	ld	de, #0x0808
   4A35 D5            [11]  510 	push	de
   4A36 E5            [11]  511 	push	hl
   4A37 C5            [11]  512 	push	bc
   4A38 CD 22 58      [17]  513 	call	_cpct_drawSprite
                            514 ;src/systems/hud.c:78: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   4A3B 21 0C B4      [10]  515 	ld	hl, #0xb40c
   4A3E E5            [11]  516 	push	hl
   4A3F 21 00 C0      [10]  517 	ld	hl, #0xc000
   4A42 E5            [11]  518 	push	hl
   4A43 CD D5 59      [17]  519 	call	_cpct_getScreenPtr
                            520 ;src/systems/hud.c:79: cpct_drawSprite((u8*)hudnumbers[currentlives % 10], pvmem, 8, 8);
   4A46 E5            [11]  521 	push	hl
   4A47 3E 0A         [ 7]  522 	ld	a, #0x0a
   4A49 F5            [11]  523 	push	af
   4A4A 33            [ 6]  524 	inc	sp
   4A4B 3A 82 5A      [13]  525 	ld	a, (_currentlives)
   4A4E F5            [11]  526 	push	af
   4A4F 33            [ 6]  527 	inc	sp
   4A50 CD C7 58      [17]  528 	call	__moduchar
   4A53 F1            [10]  529 	pop	af
   4A54 C1            [10]  530 	pop	bc
   4A55 26 00         [ 7]  531 	ld	h, #0x00
   4A57 29            [11]  532 	add	hl, hl
   4A58 11 8E 5A      [10]  533 	ld	de, #_hudnumbers
   4A5B 19            [11]  534 	add	hl, de
   4A5C 5E            [ 7]  535 	ld	e, (hl)
   4A5D 23            [ 6]  536 	inc	hl
   4A5E 56            [ 7]  537 	ld	d, (hl)
   4A5F 21 08 08      [10]  538 	ld	hl, #0x0808
   4A62 E5            [11]  539 	push	hl
   4A63 C5            [11]  540 	push	bc
   4A64 D5            [11]  541 	push	de
   4A65 CD 22 58      [17]  542 	call	_cpct_drawSprite
                            543 ;src/systems/hud.c:81: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   4A68 21 46 B4      [10]  544 	ld	hl, #0xb446
   4A6B E5            [11]  545 	push	hl
   4A6C 21 00 C0      [10]  546 	ld	hl, #0xc000
   4A6F E5            [11]  547 	push	hl
   4A70 CD D5 59      [17]  548 	call	_cpct_getScreenPtr
                            549 ;src/systems/hud.c:82: cpct_drawSprite((u8*)hudnumbers[currentweapon % 10], pvmem, 8, 8);
   4A73 E5            [11]  550 	push	hl
   4A74 3E 0A         [ 7]  551 	ld	a, #0x0a
   4A76 F5            [11]  552 	push	af
   4A77 33            [ 6]  553 	inc	sp
   4A78 3A 83 5A      [13]  554 	ld	a, (_currentweapon)
   4A7B F5            [11]  555 	push	af
   4A7C 33            [ 6]  556 	inc	sp
   4A7D CD C7 58      [17]  557 	call	__moduchar
   4A80 F1            [10]  558 	pop	af
   4A81 C1            [10]  559 	pop	bc
   4A82 26 00         [ 7]  560 	ld	h, #0x00
   4A84 29            [11]  561 	add	hl, hl
   4A85 11 8E 5A      [10]  562 	ld	de, #_hudnumbers
   4A88 19            [11]  563 	add	hl, de
   4A89 5E            [ 7]  564 	ld	e, (hl)
   4A8A 23            [ 6]  565 	inc	hl
   4A8B 56            [ 7]  566 	ld	d, (hl)
   4A8C 21 08 08      [10]  567 	ld	hl, #0x0808
   4A8F E5            [11]  568 	push	hl
   4A90 C5            [11]  569 	push	bc
   4A91 D5            [11]  570 	push	de
   4A92 CD 22 58      [17]  571 	call	_cpct_drawSprite
   4A95 C9            [10]  572 	ret
                            573 	.area _CODE
                            574 	.area _INITIALIZER
   5AA9                     575 __xinit__hudnumbers:
   5AA9 C3 48               576 	.dw __hud_dummy_sprite
   5AAB C3 48               577 	.dw __hud_dummy_sprite
   5AAD C3 48               578 	.dw __hud_dummy_sprite
   5AAF C3 48               579 	.dw __hud_dummy_sprite
   5AB1 C3 48               580 	.dw __hud_dummy_sprite
   5AB3 C3 48               581 	.dw __hud_dummy_sprite
   5AB5 C3 48               582 	.dw __hud_dummy_sprite
   5AB7 C3 48               583 	.dw __hud_dummy_sprite
   5AB9 C3 48               584 	.dw __hud_dummy_sprite
   5ABB C3 48               585 	.dw __hud_dummy_sprite
                            586 	.area _CABS (ABS)
