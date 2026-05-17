                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module player
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _collision_clamp_y_at
                             12 	.globl _collision_is_on_ground_at
                             13 	.globl _input_is_jump_just_pressed
                             14 	.globl _input_is_jump_pressed
                             15 	.globl _input_is_right_pressed
                             16 	.globl _input_is_left_pressed
                             17 	.globl _cpct_getScreenPtr
                             18 	.globl _cpct_drawSolidBox
                             19 	.globl _playerinit
                             20 	.globl _playerupdate
                             21 	.globl _playerrender
                             22 ;--------------------------------------------------------
                             23 ; special function registers
                             24 ;--------------------------------------------------------
                             25 ;--------------------------------------------------------
                             26 ; ram data
                             27 ;--------------------------------------------------------
                             28 	.area _DATA
                             29 ;--------------------------------------------------------
                             30 ; ram data
                             31 ;--------------------------------------------------------
                             32 	.area _INITIALIZED
                             33 ;--------------------------------------------------------
                             34 ; absolute external ram data
                             35 ;--------------------------------------------------------
                             36 	.area _DABS (ABS)
                             37 ;--------------------------------------------------------
                             38 ; global & static initialisations
                             39 ;--------------------------------------------------------
                             40 	.area _HOME
                             41 	.area _GSINIT
                             42 	.area _GSFINAL
                             43 	.area _GSINIT
                             44 ;--------------------------------------------------------
                             45 ; Home
                             46 ;--------------------------------------------------------
                             47 	.area _HOME
                             48 	.area _HOME
                             49 ;--------------------------------------------------------
                             50 ; code
                             51 ;--------------------------------------------------------
                             52 	.area _CODE
                             53 ;src/entities/player.c:14: void playerinit(Player* player) {
                             54 ;	---------------------------------
                             55 ; Function playerinit
                             56 ; ---------------------------------
   5645                      57 _playerinit::
                             58 ;src/entities/player.c:15: if (!player) {
   5645 21 03 00      [10]   59 	ld	hl, #2+1
   5648 39            [11]   60 	add	hl, sp
   5649 7E            [ 7]   61 	ld	a, (hl)
   564A 2B            [ 6]   62 	dec	hl
   564B B6            [ 7]   63 	or	a,(hl)
                             64 ;src/entities/player.c:16: return;
   564C C8            [11]   65 	ret	Z
                             66 ;src/entities/player.c:19: player->x = 20;
   564D D1            [10]   67 	pop	de
   564E C1            [10]   68 	pop	bc
   564F C5            [11]   69 	push	bc
   5650 D5            [11]   70 	push	de
   5651 3E 14         [ 7]   71 	ld	a, #0x14
   5653 02            [ 7]   72 	ld	(bc), a
                             73 ;src/entities/player.c:20: player->y = 120;
   5654 69            [ 4]   74 	ld	l, c
   5655 60            [ 4]   75 	ld	h, b
   5656 23            [ 6]   76 	inc	hl
   5657 36 78         [10]   77 	ld	(hl), #0x78
                             78 ;src/entities/player.c:21: player->vx = 0;
   5659 59            [ 4]   79 	ld	e, c
   565A 50            [ 4]   80 	ld	d, b
   565B 13            [ 6]   81 	inc	de
   565C 13            [ 6]   82 	inc	de
   565D AF            [ 4]   83 	xor	a, a
   565E 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/player.c:22: player->vy = 0;
   565F 59            [ 4]   86 	ld	e, c
   5660 50            [ 4]   87 	ld	d, b
   5661 13            [ 6]   88 	inc	de
   5662 13            [ 6]   89 	inc	de
   5663 13            [ 6]   90 	inc	de
   5664 AF            [ 4]   91 	xor	a, a
   5665 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/player.c:23: player->w = 4;
   5666 21 04 00      [10]   94 	ld	hl, #0x0004
   5669 09            [11]   95 	add	hl, bc
   566A 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/player.c:24: player->h = 16;
   566C 21 05 00      [10]   98 	ld	hl, #0x0005
   566F 09            [11]   99 	add	hl, bc
   5670 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/player.c:25: player->health = 3;
   5672 21 06 00      [10]  102 	ld	hl, #0x0006
   5675 09            [11]  103 	add	hl, bc
   5676 36 03         [10]  104 	ld	(hl), #0x03
                            105 ;src/entities/player.c:26: player->facing_left = 0;
   5678 21 07 00      [10]  106 	ld	hl, #0x0007
   567B 09            [11]  107 	add	hl, bc
   567C 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/player.c:27: player->jump_hold = 0;
   567E 21 08 00      [10]  110 	ld	hl, #0x0008
   5681 09            [11]  111 	add	hl, bc
   5682 36 00         [10]  112 	ld	(hl), #0x00
   5684 C9            [10]  113 	ret
   5685                     114 _kplayermovespeed:
   5685 03                  115 	.db #0x03	;  3
   5686                     116 _kplayeracceleration:
   5686 01                  117 	.db #0x01	;  1
   5687                     118 _kplayerdeceleration:
   5687 01                  119 	.db #0x01	;  1
   5688                     120 _kplayergravity:
   5688 01                  121 	.db #0x01	;  1
   5689                     122 _kplayermaxfall:
   5689 04                  123 	.db #0x04	;  4
   568A                     124 _kplayerjumpvelocity:
   568A FA                  125 	.db #0xfa	; -6
   568B                     126 _kplayerjumpboost:
   568B FF                  127 	.db #0xff	; -1
                            128 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            129 ;	---------------------------------
                            130 ; Function playerupdate
                            131 ; ---------------------------------
   568C                     132 _playerupdate::
   568C DD E5         [15]  133 	push	ix
   568E DD 21 00 00   [14]  134 	ld	ix,#0
   5692 DD 39         [15]  135 	add	ix,sp
   5694 21 ED FF      [10]  136 	ld	hl, #-19
   5697 39            [11]  137 	add	hl, sp
   5698 F9            [ 6]  138 	ld	sp, hl
                            139 ;src/entities/player.c:34: if (!player) {
   5699 DD 7E 05      [19]  140 	ld	a, 5 (ix)
   569C DD B6 04      [19]  141 	or	a,4 (ix)
                            142 ;src/entities/player.c:35: return;
   569F CA F5 59      [10]  143 	jp	Z,00141$
                            144 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   56A2 CD 83 4F      [17]  145 	call	_input_is_left_pressed
   56A5 4D            [ 4]  146 	ld	c, l
                            147 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   56A6 DD 7E 04      [19]  148 	ld	a, 4 (ix)
   56A9 DD 77 FA      [19]  149 	ld	-6 (ix), a
   56AC DD 7E 05      [19]  150 	ld	a, 5 (ix)
   56AF DD 77 FB      [19]  151 	ld	-5 (ix), a
   56B2 DD 7E FA      [19]  152 	ld	a, -6 (ix)
   56B5 C6 02         [ 7]  153 	add	a, #0x02
   56B7 DD 77 FC      [19]  154 	ld	-4 (ix), a
   56BA DD 7E FB      [19]  155 	ld	a, -5 (ix)
   56BD CE 00         [ 7]  156 	adc	a, #0x00
   56BF DD 77 FD      [19]  157 	ld	-3 (ix), a
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   56C2 DD 7E FA      [19]  159 	ld	a, -6 (ix)
   56C5 C6 07         [ 7]  160 	add	a, #0x07
   56C7 DD 77 FE      [19]  161 	ld	-2 (ix), a
   56CA DD 7E FB      [19]  162 	ld	a, -5 (ix)
   56CD CE 00         [ 7]  163 	adc	a, #0x00
   56CF DD 77 FF      [19]  164 	ld	-1 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   56D2 79            [ 4]  166 	ld	a, c
   56D3 B7            [ 4]  167 	or	a, a
   56D4 28 1E         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   56D6 DD 6E FC      [19]  170 	ld	l,-4 (ix)
   56D9 DD 66 FD      [19]  171 	ld	h,-3 (ix)
   56DC 4E            [ 7]  172 	ld	c, (hl)
   56DD 21 86 56      [10]  173 	ld	hl,#_kplayeracceleration + 0
   56E0 46            [ 7]  174 	ld	b, (hl)
   56E1 79            [ 4]  175 	ld	a, c
   56E2 90            [ 4]  176 	sub	a, b
   56E3 DD 6E FC      [19]  177 	ld	l,-4 (ix)
   56E6 DD 66 FD      [19]  178 	ld	h,-3 (ix)
   56E9 77            [ 7]  179 	ld	(hl), a
                            180 ;src/entities/player.c:40: player->facing_left = 1;
   56EA DD 6E FE      [19]  181 	ld	l,-2 (ix)
   56ED DD 66 FF      [19]  182 	ld	h,-1 (ix)
   56F0 36 01         [10]  183 	ld	(hl), #0x01
   56F2 18 6B         [12]  184 	jr	00117$
   56F4                     185 00116$:
                            186 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   56F4 CD 8B 4F      [17]  187 	call	_input_is_right_pressed
   56F7 7D            [ 4]  188 	ld	a, l
                            189 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   56F8 DD 6E FC      [19]  190 	ld	l,-4 (ix)
   56FB DD 66 FD      [19]  191 	ld	h,-3 (ix)
   56FE 4E            [ 7]  192 	ld	c, (hl)
                            193 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   56FF B7            [ 4]  194 	or	a, a
   5700 28 17         [12]  195 	jr	Z,00113$
                            196 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   5702 21 86 56      [10]  197 	ld	hl,#_kplayeracceleration + 0
   5705 5E            [ 7]  198 	ld	e, (hl)
   5706 79            [ 4]  199 	ld	a, c
   5707 83            [ 4]  200 	add	a, e
   5708 DD 6E FC      [19]  201 	ld	l,-4 (ix)
   570B DD 66 FD      [19]  202 	ld	h,-3 (ix)
   570E 77            [ 7]  203 	ld	(hl), a
                            204 ;src/entities/player.c:43: player->facing_left = 0;
   570F DD 6E FE      [19]  205 	ld	l,-2 (ix)
   5712 DD 66 FF      [19]  206 	ld	h,-1 (ix)
   5715 36 00         [10]  207 	ld	(hl), #0x00
   5717 18 46         [12]  208 	jr	00117$
   5719                     209 00113$:
                            210 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5719 21 87 56      [10]  211 	ld	hl,#_kplayerdeceleration + 0
   571C 46            [ 7]  212 	ld	b, (hl)
                            213 ;src/entities/player.c:44: } else if (player->vx > 0) {
   571D AF            [ 4]  214 	xor	a, a
   571E 91            [ 4]  215 	sub	a, c
   571F E2 24 57      [10]  216 	jp	PO, 00223$
   5722 EE 80         [ 7]  217 	xor	a, #0x80
   5724                     218 00223$:
   5724 F2 3F 57      [10]  219 	jp	P, 00110$
                            220 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5727 79            [ 4]  221 	ld	a, c
   5728 90            [ 4]  222 	sub	a, b
   5729 4F            [ 4]  223 	ld	c, a
   572A DD 6E FC      [19]  224 	ld	l,-4 (ix)
   572D DD 66 FD      [19]  225 	ld	h,-3 (ix)
   5730 71            [ 7]  226 	ld	(hl), c
                            227 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   5731 CB 79         [ 8]  228 	bit	7, c
   5733 28 2A         [12]  229 	jr	Z,00117$
   5735 DD 6E FC      [19]  230 	ld	l,-4 (ix)
   5738 DD 66 FD      [19]  231 	ld	h,-3 (ix)
   573B 36 00         [10]  232 	ld	(hl), #0x00
   573D 18 20         [12]  233 	jr	00117$
   573F                     234 00110$:
                            235 ;src/entities/player.c:47: } else if (player->vx < 0) {
   573F CB 79         [ 8]  236 	bit	7, c
   5741 28 1C         [12]  237 	jr	Z,00117$
                            238 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   5743 79            [ 4]  239 	ld	a, c
   5744 80            [ 4]  240 	add	a, b
   5745 4F            [ 4]  241 	ld	c, a
   5746 DD 6E FC      [19]  242 	ld	l,-4 (ix)
   5749 DD 66 FD      [19]  243 	ld	h,-3 (ix)
   574C 71            [ 7]  244 	ld	(hl), c
                            245 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   574D AF            [ 4]  246 	xor	a, a
   574E 91            [ 4]  247 	sub	a, c
   574F E2 54 57      [10]  248 	jp	PO, 00224$
   5752 EE 80         [ 7]  249 	xor	a, #0x80
   5754                     250 00224$:
   5754 F2 5F 57      [10]  251 	jp	P, 00117$
   5757 DD 6E FC      [19]  252 	ld	l,-4 (ix)
   575A DD 66 FD      [19]  253 	ld	h,-3 (ix)
   575D 36 00         [10]  254 	ld	(hl), #0x00
   575F                     255 00117$:
                            256 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   575F DD 6E FC      [19]  257 	ld	l,-4 (ix)
   5762 DD 66 FD      [19]  258 	ld	h,-3 (ix)
   5765 46            [ 7]  259 	ld	b, (hl)
   5766 21 85 56      [10]  260 	ld	hl,#_kplayermovespeed + 0
   5769 4E            [ 7]  261 	ld	c, (hl)
   576A 79            [ 4]  262 	ld	a, c
   576B 90            [ 4]  263 	sub	a, b
   576C E2 71 57      [10]  264 	jp	PO, 00225$
   576F EE 80         [ 7]  265 	xor	a, #0x80
   5771                     266 00225$:
   5771 F2 7B 57      [10]  267 	jp	P, 00119$
   5774 DD 6E FC      [19]  268 	ld	l,-4 (ix)
   5777 DD 66 FD      [19]  269 	ld	h,-3 (ix)
   577A 71            [ 7]  270 	ld	(hl), c
   577B                     271 00119$:
                            272 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   577B DD 6E FC      [19]  273 	ld	l,-4 (ix)
   577E DD 66 FD      [19]  274 	ld	h,-3 (ix)
   5781 7E            [ 7]  275 	ld	a, (hl)
   5782 DD 77 FE      [19]  276 	ld	-2 (ix), a
   5785 3A 85 56      [13]  277 	ld	a,(#_kplayermovespeed + 0)
   5788 DD 77 F9      [19]  278 	ld	-7 (ix), a
   578B DD 77 F7      [19]  279 	ld	-9 (ix), a
   578E DD 7E F9      [19]  280 	ld	a, -7 (ix)
   5791 17            [ 4]  281 	rla
   5792 9F            [ 4]  282 	sbc	a, a
   5793 DD 77 F8      [19]  283 	ld	-8 (ix), a
   5796 AF            [ 4]  284 	xor	a, a
   5797 DD 96 F7      [19]  285 	sub	a, -9 (ix)
   579A DD 77 F7      [19]  286 	ld	-9 (ix), a
   579D 3E 00         [ 7]  287 	ld	a, #0x00
   579F DD 9E F8      [19]  288 	sbc	a, -8 (ix)
   57A2 DD 77 F8      [19]  289 	ld	-8 (ix), a
   57A5 DD 7E FE      [19]  290 	ld	a, -2 (ix)
   57A8 DD 77 FE      [19]  291 	ld	-2 (ix), a
   57AB 17            [ 4]  292 	rla
   57AC 9F            [ 4]  293 	sbc	a, a
   57AD DD 77 FF      [19]  294 	ld	-1 (ix), a
   57B0 DD 7E FE      [19]  295 	ld	a, -2 (ix)
   57B3 DD 96 F7      [19]  296 	sub	a, -9 (ix)
   57B6 DD 7E FF      [19]  297 	ld	a, -1 (ix)
   57B9 DD 9E F8      [19]  298 	sbc	a, -8 (ix)
   57BC E2 C1 57      [10]  299 	jp	PO, 00226$
   57BF EE 80         [ 7]  300 	xor	a, #0x80
   57C1                     301 00226$:
   57C1 F2 D0 57      [10]  302 	jp	P, 00121$
   57C4 AF            [ 4]  303 	xor	a, a
   57C5 DD 96 F9      [19]  304 	sub	a, -7 (ix)
   57C8 4F            [ 4]  305 	ld	c, a
   57C9 DD 6E FC      [19]  306 	ld	l,-4 (ix)
   57CC DD 66 FD      [19]  307 	ld	h,-3 (ix)
   57CF 71            [ 7]  308 	ld	(hl), c
   57D0                     309 00121$:
                            310 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   57D0 CD AB 4F      [17]  311 	call	_input_is_jump_just_pressed
   57D3 DD 75 F7      [19]  312 	ld	-9 (ix), l
   57D6 DD 7E FA      [19]  313 	ld	a, -6 (ix)
   57D9 C6 05         [ 7]  314 	add	a, #0x05
   57DB DD 77 FE      [19]  315 	ld	-2 (ix), a
   57DE DD 7E FB      [19]  316 	ld	a, -5 (ix)
   57E1 CE 00         [ 7]  317 	adc	a, #0x00
   57E3 DD 77 FF      [19]  318 	ld	-1 (ix), a
   57E6 DD 7E FA      [19]  319 	ld	a, -6 (ix)
   57E9 C6 01         [ 7]  320 	add	a, #0x01
   57EB DD 77 F5      [19]  321 	ld	-11 (ix), a
   57EE DD 7E FB      [19]  322 	ld	a, -5 (ix)
   57F1 CE 00         [ 7]  323 	adc	a, #0x00
   57F3 DD 77 F6      [19]  324 	ld	-10 (ix), a
                            325 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   57F6 DD 7E FA      [19]  326 	ld	a, -6 (ix)
   57F9 C6 03         [ 7]  327 	add	a, #0x03
   57FB DD 77 F3      [19]  328 	ld	-13 (ix), a
   57FE DD 7E FB      [19]  329 	ld	a, -5 (ix)
   5801 CE 00         [ 7]  330 	adc	a, #0x00
   5803 DD 77 F4      [19]  331 	ld	-12 (ix), a
                            332 ;src/entities/player.c:57: player->jump_hold = 5;
   5806 DD 7E FA      [19]  333 	ld	a, -6 (ix)
   5809 C6 08         [ 7]  334 	add	a, #0x08
   580B DD 77 F1      [19]  335 	ld	-15 (ix), a
   580E DD 7E FB      [19]  336 	ld	a, -5 (ix)
   5811 CE 00         [ 7]  337 	adc	a, #0x00
   5813 DD 77 F2      [19]  338 	ld	-14 (ix), a
                            339 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5816 DD 7E F7      [19]  340 	ld	a, -9 (ix)
   5819 B7            [ 4]  341 	or	a, a
   581A 28 3A         [12]  342 	jr	Z,00123$
   581C DD 6E FE      [19]  343 	ld	l,-2 (ix)
   581F DD 66 FF      [19]  344 	ld	h,-1 (ix)
   5822 7E            [ 7]  345 	ld	a, (hl)
   5823 DD 6E F5      [19]  346 	ld	l,-11 (ix)
   5826 DD 66 F6      [19]  347 	ld	h,-10 (ix)
   5829 4E            [ 7]  348 	ld	c, (hl)
   582A 06 00         [ 7]  349 	ld	b, #0x00
   582C DD 6E FA      [19]  350 	ld	l,-6 (ix)
   582F DD 66 FB      [19]  351 	ld	h,-5 (ix)
   5832 5E            [ 7]  352 	ld	e, (hl)
   5833 16 00         [ 7]  353 	ld	d, #0x00
   5835 F5            [11]  354 	push	af
   5836 33            [ 6]  355 	inc	sp
   5837 C5            [11]  356 	push	bc
   5838 D5            [11]  357 	push	de
   5839 CD 57 4B      [17]  358 	call	_collision_is_on_ground_at
   583C F1            [10]  359 	pop	af
   583D F1            [10]  360 	pop	af
   583E 33            [ 6]  361 	inc	sp
   583F 7D            [ 4]  362 	ld	a, l
   5840 B7            [ 4]  363 	or	a, a
   5841 28 13         [12]  364 	jr	Z,00123$
                            365 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   5843 21 8A 56      [10]  366 	ld	hl,#_kplayerjumpvelocity + 0
   5846 4E            [ 7]  367 	ld	c, (hl)
   5847 DD 6E F3      [19]  368 	ld	l,-13 (ix)
   584A DD 66 F4      [19]  369 	ld	h,-12 (ix)
   584D 71            [ 7]  370 	ld	(hl), c
                            371 ;src/entities/player.c:57: player->jump_hold = 5;
   584E DD 6E F1      [19]  372 	ld	l,-15 (ix)
   5851 DD 66 F2      [19]  373 	ld	h,-14 (ix)
   5854 36 05         [10]  374 	ld	(hl), #0x05
   5856                     375 00123$:
                            376 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5856 CD A3 4F      [17]  377 	call	_input_is_jump_pressed
   5859 DD 75 F7      [19]  378 	ld	-9 (ix), l
   585C 7D            [ 4]  379 	ld	a, l
   585D B7            [ 4]  380 	or	a, a
   585E 28 41         [12]  381 	jr	Z,00126$
   5860 DD 6E F1      [19]  382 	ld	l,-15 (ix)
   5863 DD 66 F2      [19]  383 	ld	h,-14 (ix)
   5866 7E            [ 7]  384 	ld	a, (hl)
   5867 DD 77 F7      [19]  385 	ld	-9 (ix), a
   586A B7            [ 4]  386 	or	a, a
   586B 28 34         [12]  387 	jr	Z,00126$
   586D DD 6E F3      [19]  388 	ld	l,-13 (ix)
   5870 DD 66 F4      [19]  389 	ld	h,-12 (ix)
   5873 7E            [ 7]  390 	ld	a, (hl)
   5874 DD 77 F7      [19]  391 	ld	-9 (ix), a
   5877 DD CB F7 7E   [20]  392 	bit	7, -9 (ix)
   587B 28 24         [12]  393 	jr	Z,00126$
                            394 ;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
   587D 3A 8B 56      [13]  395 	ld	a,(#_kplayerjumpboost + 0)
   5880 DD 77 F9      [19]  396 	ld	-7 (ix), a
   5883 DD 7E F7      [19]  397 	ld	a, -9 (ix)
   5886 DD 86 F9      [19]  398 	add	a, -7 (ix)
   5889 DD 6E F3      [19]  399 	ld	l,-13 (ix)
   588C DD 66 F4      [19]  400 	ld	h,-12 (ix)
   588F 77            [ 7]  401 	ld	(hl), a
                            402 ;src/entities/player.c:62: player->jump_hold--;
   5890 DD 6E F1      [19]  403 	ld	l,-15 (ix)
   5893 DD 66 F2      [19]  404 	ld	h,-14 (ix)
   5896 4E            [ 7]  405 	ld	c, (hl)
   5897 0D            [ 4]  406 	dec	c
   5898 DD 6E F1      [19]  407 	ld	l,-15 (ix)
   589B DD 66 F2      [19]  408 	ld	h,-14 (ix)
   589E 71            [ 7]  409 	ld	(hl), c
   589F 18 08         [12]  410 	jr	00127$
   58A1                     411 00126$:
                            412 ;src/entities/player.c:64: player->jump_hold = 0;
   58A1 DD 6E F1      [19]  413 	ld	l,-15 (ix)
   58A4 DD 66 F2      [19]  414 	ld	h,-14 (ix)
   58A7 36 00         [10]  415 	ld	(hl), #0x00
   58A9                     416 00127$:
                            417 ;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
   58A9 DD 6E F3      [19]  418 	ld	l,-13 (ix)
   58AC DD 66 F4      [19]  419 	ld	h,-12 (ix)
   58AF 4E            [ 7]  420 	ld	c, (hl)
   58B0 21 88 56      [10]  421 	ld	hl,#_kplayergravity + 0
   58B3 46            [ 7]  422 	ld	b, (hl)
   58B4 79            [ 4]  423 	ld	a, c
   58B5 80            [ 4]  424 	add	a, b
   58B6 4F            [ 4]  425 	ld	c, a
   58B7 DD 6E F3      [19]  426 	ld	l,-13 (ix)
   58BA DD 66 F4      [19]  427 	ld	h,-12 (ix)
   58BD 71            [ 7]  428 	ld	(hl), c
                            429 ;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   58BE 21 89 56      [10]  430 	ld	hl,#_kplayermaxfall + 0
   58C1 46            [ 7]  431 	ld	b, (hl)
   58C2 78            [ 4]  432 	ld	a, b
   58C3 91            [ 4]  433 	sub	a, c
   58C4 E2 C9 58      [10]  434 	jp	PO, 00227$
   58C7 EE 80         [ 7]  435 	xor	a, #0x80
   58C9                     436 00227$:
   58C9 F2 D3 58      [10]  437 	jp	P, 00131$
   58CC DD 6E F3      [19]  438 	ld	l,-13 (ix)
   58CF DD 66 F4      [19]  439 	ld	h,-12 (ix)
   58D2 70            [ 7]  440 	ld	(hl), b
   58D3                     441 00131$:
                            442 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   58D3 DD 6E FA      [19]  443 	ld	l,-6 (ix)
   58D6 DD 66 FB      [19]  444 	ld	h,-5 (ix)
   58D9 4E            [ 7]  445 	ld	c, (hl)
   58DA DD 71 F1      [19]  446 	ld	-15 (ix), c
   58DD DD 36 F2 00   [19]  447 	ld	-14 (ix), #0x00
   58E1 DD 6E FC      [19]  448 	ld	l,-4 (ix)
   58E4 DD 66 FD      [19]  449 	ld	h,-3 (ix)
   58E7 7E            [ 7]  450 	ld	a, (hl)
   58E8 DD 77 F7      [19]  451 	ld	-9 (ix), a
   58EB DD 77 F7      [19]  452 	ld	-9 (ix), a
   58EE 17            [ 4]  453 	rla
   58EF 9F            [ 4]  454 	sbc	a, a
   58F0 DD 77 F8      [19]  455 	ld	-8 (ix), a
   58F3 DD 7E F7      [19]  456 	ld	a, -9 (ix)
   58F6 DD 86 F1      [19]  457 	add	a, -15 (ix)
   58F9 DD 77 EF      [19]  458 	ld	-17 (ix), a
   58FC DD 7E F8      [19]  459 	ld	a, -8 (ix)
   58FF DD 8E F2      [19]  460 	adc	a, -14 (ix)
   5902 DD 77 F0      [19]  461 	ld	-16 (ix), a
                            462 ;src/entities/player.c:71: if (nextx < 0) {
   5905 DD CB F0 7E   [20]  463 	bit	7, -16 (ix)
   5909 28 08         [12]  464 	jr	Z,00133$
                            465 ;src/entities/player.c:72: nextx = 0;
   590B DD 36 EF 00   [19]  466 	ld	-17 (ix), #0x00
   590F DD 36 F0 00   [19]  467 	ld	-16 (ix), #0x00
   5913                     468 00133$:
                            469 ;src/entities/player.c:74: if (nextx > 76) {
   5913 3E 4C         [ 7]  470 	ld	a, #0x4c
   5915 DD BE EF      [19]  471 	cp	a, -17 (ix)
   5918 3E 00         [ 7]  472 	ld	a, #0x00
   591A DD 9E F0      [19]  473 	sbc	a, -16 (ix)
   591D E2 22 59      [10]  474 	jp	PO, 00228$
   5920 EE 80         [ 7]  475 	xor	a, #0x80
   5922                     476 00228$:
   5922 F2 2D 59      [10]  477 	jp	P, 00135$
                            478 ;src/entities/player.c:75: nextx = 76;
   5925 DD 36 EF 4C   [19]  479 	ld	-17 (ix), #0x4c
   5929 DD 36 F0 00   [19]  480 	ld	-16 (ix), #0x00
   592D                     481 00135$:
                            482 ;src/entities/player.c:77: player->x = (u8)nextx;
   592D DD 7E EF      [19]  483 	ld	a, -17 (ix)
   5930 DD 77 F1      [19]  484 	ld	-15 (ix), a
   5933 DD 6E FA      [19]  485 	ld	l,-6 (ix)
   5936 DD 66 FB      [19]  486 	ld	h,-5 (ix)
   5939 DD 7E F1      [19]  487 	ld	a, -15 (ix)
   593C 77            [ 7]  488 	ld	(hl), a
                            489 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   593D DD 6E F5      [19]  490 	ld	l,-11 (ix)
   5940 DD 66 F6      [19]  491 	ld	h,-10 (ix)
   5943 4E            [ 7]  492 	ld	c, (hl)
   5944 DD 71 F7      [19]  493 	ld	-9 (ix), c
   5947 DD 36 F8 00   [19]  494 	ld	-8 (ix), #0x00
   594B DD 6E F3      [19]  495 	ld	l,-13 (ix)
   594E DD 66 F4      [19]  496 	ld	h,-12 (ix)
   5951 7E            [ 7]  497 	ld	a, (hl)
   5952 DD 77 FC      [19]  498 	ld	-4 (ix), a
   5955 17            [ 4]  499 	rla
   5956 9F            [ 4]  500 	sbc	a, a
   5957 DD 77 FD      [19]  501 	ld	-3 (ix), a
   595A DD 7E FC      [19]  502 	ld	a, -4 (ix)
   595D DD 86 F7      [19]  503 	add	a, -9 (ix)
   5960 DD 77 F7      [19]  504 	ld	-9 (ix), a
   5963 DD 7E FD      [19]  505 	ld	a, -3 (ix)
   5966 DD 8E F8      [19]  506 	adc	a, -8 (ix)
   5969 DD 77 F8      [19]  507 	ld	-8 (ix), a
                            508 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   596C DD 6E FE      [19]  509 	ld	l,-2 (ix)
   596F DD 66 FF      [19]  510 	ld	h,-1 (ix)
   5972 7E            [ 7]  511 	ld	a, (hl)
   5973 DD 77 F9      [19]  512 	ld	-7 (ix), a
   5976 DD 7E F1      [19]  513 	ld	a, -15 (ix)
   5979 DD 77 F1      [19]  514 	ld	-15 (ix), a
   597C DD 36 F2 00   [19]  515 	ld	-14 (ix), #0x00
   5980 DD 7E F9      [19]  516 	ld	a, -7 (ix)
   5983 F5            [11]  517 	push	af
   5984 33            [ 6]  518 	inc	sp
   5985 DD 6E F7      [19]  519 	ld	l,-9 (ix)
   5988 DD 66 F8      [19]  520 	ld	h,-8 (ix)
   598B E5            [11]  521 	push	hl
   598C DD 6E F1      [19]  522 	ld	l,-15 (ix)
   598F DD 66 F2      [19]  523 	ld	h,-14 (ix)
   5992 E5            [11]  524 	push	hl
   5993 CD D6 4B      [17]  525 	call	_collision_clamp_y_at
   5996 F1            [10]  526 	pop	af
   5997 F1            [10]  527 	pop	af
   5998 33            [ 6]  528 	inc	sp
   5999 DD 74 F2      [19]  529 	ld	-14 (ix), h
   599C DD 75 F1      [19]  530 	ld	-15 (ix), l
   599F DD 75 ED      [19]  531 	ld	-19 (ix), l
   59A2 DD 7E F2      [19]  532 	ld	a, -14 (ix)
   59A5 DD 77 EE      [19]  533 	ld	-18 (ix), a
                            534 ;src/entities/player.c:81: if (nexty < 0) {
   59A8 DD CB EE 7E   [20]  535 	bit	7, -18 (ix)
   59AC 28 04         [12]  536 	jr	Z,00137$
                            537 ;src/entities/player.c:82: nexty = 0;
   59AE 21 00 00      [10]  538 	ld	hl, #0x0000
   59B1 E3            [19]  539 	ex	(sp), hl
   59B2                     540 00137$:
                            541 ;src/entities/player.c:84: player->y = (u8)nexty;
   59B2 DD 4E ED      [19]  542 	ld	c, -19 (ix)
   59B5 DD 6E F5      [19]  543 	ld	l,-11 (ix)
   59B8 DD 66 F6      [19]  544 	ld	h,-10 (ix)
   59BB 71            [ 7]  545 	ld	(hl), c
                            546 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   59BC DD 6E FE      [19]  547 	ld	l,-2 (ix)
   59BF DD 66 FF      [19]  548 	ld	h,-1 (ix)
   59C2 7E            [ 7]  549 	ld	a, (hl)
   59C3 06 00         [ 7]  550 	ld	b, #0x00
   59C5 DD 6E FA      [19]  551 	ld	l,-6 (ix)
   59C8 DD 66 FB      [19]  552 	ld	h,-5 (ix)
   59CB 5E            [ 7]  553 	ld	e, (hl)
   59CC 16 00         [ 7]  554 	ld	d, #0x00
   59CE F5            [11]  555 	push	af
   59CF 33            [ 6]  556 	inc	sp
   59D0 C5            [11]  557 	push	bc
   59D1 D5            [11]  558 	push	de
   59D2 CD 57 4B      [17]  559 	call	_collision_is_on_ground_at
   59D5 F1            [10]  560 	pop	af
   59D6 F1            [10]  561 	pop	af
   59D7 33            [ 6]  562 	inc	sp
   59D8 7D            [ 4]  563 	ld	a, l
   59D9 B7            [ 4]  564 	or	a, a
   59DA 28 19         [12]  565 	jr	Z,00141$
   59DC DD 6E F3      [19]  566 	ld	l,-13 (ix)
   59DF DD 66 F4      [19]  567 	ld	h,-12 (ix)
   59E2 4E            [ 7]  568 	ld	c, (hl)
   59E3 AF            [ 4]  569 	xor	a, a
   59E4 91            [ 4]  570 	sub	a, c
   59E5 E2 EA 59      [10]  571 	jp	PO, 00229$
   59E8 EE 80         [ 7]  572 	xor	a, #0x80
   59EA                     573 00229$:
   59EA F2 F5 59      [10]  574 	jp	P, 00141$
                            575 ;src/entities/player.c:87: player->vy = 0;
   59ED DD 6E F3      [19]  576 	ld	l,-13 (ix)
   59F0 DD 66 F4      [19]  577 	ld	h,-12 (ix)
   59F3 36 00         [10]  578 	ld	(hl), #0x00
   59F5                     579 00141$:
   59F5 DD F9         [10]  580 	ld	sp, ix
   59F7 DD E1         [14]  581 	pop	ix
   59F9 C9            [10]  582 	ret
                            583 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            584 ;	---------------------------------
                            585 ; Function playerrender
                            586 ; ---------------------------------
   59FA                     587 _playerrender::
   59FA DD E5         [15]  588 	push	ix
   59FC DD 21 00 00   [14]  589 	ld	ix,#0
   5A00 DD 39         [15]  590 	add	ix,sp
                            591 ;src/entities/player.c:94: if (!player) {
   5A02 DD 7E 05      [19]  592 	ld	a, 5 (ix)
   5A05 DD B6 04      [19]  593 	or	a,4 (ix)
                            594 ;src/entities/player.c:95: return;
   5A08 28 32         [12]  595 	jr	Z,00103$
                            596 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5A0A DD 5E 04      [19]  597 	ld	e,4 (ix)
   5A0D DD 56 05      [19]  598 	ld	d,5 (ix)
   5A10 6B            [ 4]  599 	ld	l, e
   5A11 62            [ 4]  600 	ld	h, d
   5A12 23            [ 6]  601 	inc	hl
   5A13 46            [ 7]  602 	ld	b, (hl)
   5A14 1A            [ 7]  603 	ld	a, (de)
   5A15 D5            [11]  604 	push	de
   5A16 C5            [11]  605 	push	bc
   5A17 33            [ 6]  606 	inc	sp
   5A18 F5            [11]  607 	push	af
   5A19 33            [ 6]  608 	inc	sp
   5A1A 21 00 C0      [10]  609 	ld	hl, #0xc000
   5A1D E5            [11]  610 	push	hl
   5A1E CD 98 5E      [17]  611 	call	_cpct_getScreenPtr
   5A21 4D            [ 4]  612 	ld	c, l
   5A22 44            [ 4]  613 	ld	b, h
   5A23 D1            [10]  614 	pop	de
                            615 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   5A24 D5            [11]  616 	push	de
   5A25 FD E1         [14]  617 	pop	iy
   5A27 FD 7E 05      [19]  618 	ld	a, 5 (iy)
   5A2A EB            [ 4]  619 	ex	de,hl
   5A2B 11 04 00      [10]  620 	ld	de, #0x0004
   5A2E 19            [11]  621 	add	hl, de
   5A2F 56            [ 7]  622 	ld	d, (hl)
   5A30 F5            [11]  623 	push	af
   5A31 33            [ 6]  624 	inc	sp
   5A32 1E 4F         [ 7]  625 	ld	e, #0x4f
   5A34 D5            [11]  626 	push	de
   5A35 C5            [11]  627 	push	bc
   5A36 CD DF 5D      [17]  628 	call	_cpct_drawSolidBox
   5A39 F1            [10]  629 	pop	af
   5A3A F1            [10]  630 	pop	af
   5A3B 33            [ 6]  631 	inc	sp
   5A3C                     632 00103$:
   5A3C DD E1         [14]  633 	pop	ix
   5A3E C9            [10]  634 	ret
                            635 	.area _CODE
                            636 	.area _INITIALIZER
                            637 	.area _CABS (ABS)
