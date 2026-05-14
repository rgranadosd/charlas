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
   5544                      57 _playerinit::
                             58 ;src/entities/player.c:15: if (!player) {
   5544 21 03 00      [10]   59 	ld	hl, #2+1
   5547 39            [11]   60 	add	hl, sp
   5548 7E            [ 7]   61 	ld	a, (hl)
   5549 2B            [ 6]   62 	dec	hl
   554A B6            [ 7]   63 	or	a,(hl)
                             64 ;src/entities/player.c:16: return;
   554B C8            [11]   65 	ret	Z
                             66 ;src/entities/player.c:19: player->x = 20;
   554C D1            [10]   67 	pop	de
   554D C1            [10]   68 	pop	bc
   554E C5            [11]   69 	push	bc
   554F D5            [11]   70 	push	de
   5550 3E 14         [ 7]   71 	ld	a, #0x14
   5552 02            [ 7]   72 	ld	(bc), a
                             73 ;src/entities/player.c:20: player->y = 120;
   5553 69            [ 4]   74 	ld	l, c
   5554 60            [ 4]   75 	ld	h, b
   5555 23            [ 6]   76 	inc	hl
   5556 36 78         [10]   77 	ld	(hl), #0x78
                             78 ;src/entities/player.c:21: player->vx = 0;
   5558 59            [ 4]   79 	ld	e, c
   5559 50            [ 4]   80 	ld	d, b
   555A 13            [ 6]   81 	inc	de
   555B 13            [ 6]   82 	inc	de
   555C AF            [ 4]   83 	xor	a, a
   555D 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/player.c:22: player->vy = 0;
   555E 59            [ 4]   86 	ld	e, c
   555F 50            [ 4]   87 	ld	d, b
   5560 13            [ 6]   88 	inc	de
   5561 13            [ 6]   89 	inc	de
   5562 13            [ 6]   90 	inc	de
   5563 AF            [ 4]   91 	xor	a, a
   5564 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/player.c:23: player->w = 4;
   5565 21 04 00      [10]   94 	ld	hl, #0x0004
   5568 09            [11]   95 	add	hl, bc
   5569 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/player.c:24: player->h = 16;
   556B 21 05 00      [10]   98 	ld	hl, #0x0005
   556E 09            [11]   99 	add	hl, bc
   556F 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/player.c:25: player->health = 3;
   5571 21 06 00      [10]  102 	ld	hl, #0x0006
   5574 09            [11]  103 	add	hl, bc
   5575 36 03         [10]  104 	ld	(hl), #0x03
                            105 ;src/entities/player.c:26: player->facing_left = 0;
   5577 21 07 00      [10]  106 	ld	hl, #0x0007
   557A 09            [11]  107 	add	hl, bc
   557B 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/player.c:27: player->jump_hold = 0;
   557D 21 08 00      [10]  110 	ld	hl, #0x0008
   5580 09            [11]  111 	add	hl, bc
   5581 36 00         [10]  112 	ld	(hl), #0x00
   5583 C9            [10]  113 	ret
   5584                     114 _kplayermovespeed:
   5584 03                  115 	.db #0x03	;  3
   5585                     116 _kplayeracceleration:
   5585 01                  117 	.db #0x01	;  1
   5586                     118 _kplayerdeceleration:
   5586 01                  119 	.db #0x01	;  1
   5587                     120 _kplayergravity:
   5587 01                  121 	.db #0x01	;  1
   5588                     122 _kplayermaxfall:
   5588 04                  123 	.db #0x04	;  4
   5589                     124 _kplayerjumpvelocity:
   5589 FA                  125 	.db #0xfa	; -6
   558A                     126 _kplayerjumpboost:
   558A FF                  127 	.db #0xff	; -1
                            128 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            129 ;	---------------------------------
                            130 ; Function playerupdate
                            131 ; ---------------------------------
   558B                     132 _playerupdate::
   558B DD E5         [15]  133 	push	ix
   558D DD 21 00 00   [14]  134 	ld	ix,#0
   5591 DD 39         [15]  135 	add	ix,sp
   5593 21 ED FF      [10]  136 	ld	hl, #-19
   5596 39            [11]  137 	add	hl, sp
   5597 F9            [ 6]  138 	ld	sp, hl
                            139 ;src/entities/player.c:34: if (!player) {
   5598 DD 7E 05      [19]  140 	ld	a, 5 (ix)
   559B DD B6 04      [19]  141 	or	a,4 (ix)
                            142 ;src/entities/player.c:35: return;
   559E CA F4 58      [10]  143 	jp	Z,00141$
                            144 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   55A1 CD 92 4E      [17]  145 	call	_input_is_left_pressed
   55A4 4D            [ 4]  146 	ld	c, l
                            147 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   55A5 DD 7E 04      [19]  148 	ld	a, 4 (ix)
   55A8 DD 77 FE      [19]  149 	ld	-2 (ix), a
   55AB DD 7E 05      [19]  150 	ld	a, 5 (ix)
   55AE DD 77 FF      [19]  151 	ld	-1 (ix), a
   55B1 DD 7E FE      [19]  152 	ld	a, -2 (ix)
   55B4 C6 02         [ 7]  153 	add	a, #0x02
   55B6 DD 77 FC      [19]  154 	ld	-4 (ix), a
   55B9 DD 7E FF      [19]  155 	ld	a, -1 (ix)
   55BC CE 00         [ 7]  156 	adc	a, #0x00
   55BE DD 77 FD      [19]  157 	ld	-3 (ix), a
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   55C1 DD 7E FE      [19]  159 	ld	a, -2 (ix)
   55C4 C6 07         [ 7]  160 	add	a, #0x07
   55C6 DD 77 FA      [19]  161 	ld	-6 (ix), a
   55C9 DD 7E FF      [19]  162 	ld	a, -1 (ix)
   55CC CE 00         [ 7]  163 	adc	a, #0x00
   55CE DD 77 FB      [19]  164 	ld	-5 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   55D1 79            [ 4]  166 	ld	a, c
   55D2 B7            [ 4]  167 	or	a, a
   55D3 28 1E         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   55D5 DD 6E FC      [19]  170 	ld	l,-4 (ix)
   55D8 DD 66 FD      [19]  171 	ld	h,-3 (ix)
   55DB 4E            [ 7]  172 	ld	c, (hl)
   55DC 21 85 55      [10]  173 	ld	hl,#_kplayeracceleration + 0
   55DF 46            [ 7]  174 	ld	b, (hl)
   55E0 79            [ 4]  175 	ld	a, c
   55E1 90            [ 4]  176 	sub	a, b
   55E2 DD 6E FC      [19]  177 	ld	l,-4 (ix)
   55E5 DD 66 FD      [19]  178 	ld	h,-3 (ix)
   55E8 77            [ 7]  179 	ld	(hl), a
                            180 ;src/entities/player.c:40: player->facing_left = 1;
   55E9 DD 6E FA      [19]  181 	ld	l,-6 (ix)
   55EC DD 66 FB      [19]  182 	ld	h,-5 (ix)
   55EF 36 01         [10]  183 	ld	(hl), #0x01
   55F1 18 6B         [12]  184 	jr	00117$
   55F3                     185 00116$:
                            186 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   55F3 CD 9A 4E      [17]  187 	call	_input_is_right_pressed
   55F6 7D            [ 4]  188 	ld	a, l
                            189 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   55F7 DD 6E FC      [19]  190 	ld	l,-4 (ix)
   55FA DD 66 FD      [19]  191 	ld	h,-3 (ix)
   55FD 4E            [ 7]  192 	ld	c, (hl)
                            193 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   55FE B7            [ 4]  194 	or	a, a
   55FF 28 17         [12]  195 	jr	Z,00113$
                            196 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   5601 21 85 55      [10]  197 	ld	hl,#_kplayeracceleration + 0
   5604 5E            [ 7]  198 	ld	e, (hl)
   5605 79            [ 4]  199 	ld	a, c
   5606 83            [ 4]  200 	add	a, e
   5607 DD 6E FC      [19]  201 	ld	l,-4 (ix)
   560A DD 66 FD      [19]  202 	ld	h,-3 (ix)
   560D 77            [ 7]  203 	ld	(hl), a
                            204 ;src/entities/player.c:43: player->facing_left = 0;
   560E DD 6E FA      [19]  205 	ld	l,-6 (ix)
   5611 DD 66 FB      [19]  206 	ld	h,-5 (ix)
   5614 36 00         [10]  207 	ld	(hl), #0x00
   5616 18 46         [12]  208 	jr	00117$
   5618                     209 00113$:
                            210 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5618 21 86 55      [10]  211 	ld	hl,#_kplayerdeceleration + 0
   561B 46            [ 7]  212 	ld	b, (hl)
                            213 ;src/entities/player.c:44: } else if (player->vx > 0) {
   561C AF            [ 4]  214 	xor	a, a
   561D 91            [ 4]  215 	sub	a, c
   561E E2 23 56      [10]  216 	jp	PO, 00223$
   5621 EE 80         [ 7]  217 	xor	a, #0x80
   5623                     218 00223$:
   5623 F2 3E 56      [10]  219 	jp	P, 00110$
                            220 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   5626 79            [ 4]  221 	ld	a, c
   5627 90            [ 4]  222 	sub	a, b
   5628 4F            [ 4]  223 	ld	c, a
   5629 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   562C DD 66 FD      [19]  225 	ld	h,-3 (ix)
   562F 71            [ 7]  226 	ld	(hl), c
                            227 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   5630 CB 79         [ 8]  228 	bit	7, c
   5632 28 2A         [12]  229 	jr	Z,00117$
   5634 DD 6E FC      [19]  230 	ld	l,-4 (ix)
   5637 DD 66 FD      [19]  231 	ld	h,-3 (ix)
   563A 36 00         [10]  232 	ld	(hl), #0x00
   563C 18 20         [12]  233 	jr	00117$
   563E                     234 00110$:
                            235 ;src/entities/player.c:47: } else if (player->vx < 0) {
   563E CB 79         [ 8]  236 	bit	7, c
   5640 28 1C         [12]  237 	jr	Z,00117$
                            238 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   5642 79            [ 4]  239 	ld	a, c
   5643 80            [ 4]  240 	add	a, b
   5644 4F            [ 4]  241 	ld	c, a
   5645 DD 6E FC      [19]  242 	ld	l,-4 (ix)
   5648 DD 66 FD      [19]  243 	ld	h,-3 (ix)
   564B 71            [ 7]  244 	ld	(hl), c
                            245 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   564C AF            [ 4]  246 	xor	a, a
   564D 91            [ 4]  247 	sub	a, c
   564E E2 53 56      [10]  248 	jp	PO, 00224$
   5651 EE 80         [ 7]  249 	xor	a, #0x80
   5653                     250 00224$:
   5653 F2 5E 56      [10]  251 	jp	P, 00117$
   5656 DD 6E FC      [19]  252 	ld	l,-4 (ix)
   5659 DD 66 FD      [19]  253 	ld	h,-3 (ix)
   565C 36 00         [10]  254 	ld	(hl), #0x00
   565E                     255 00117$:
                            256 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   565E DD 6E FC      [19]  257 	ld	l,-4 (ix)
   5661 DD 66 FD      [19]  258 	ld	h,-3 (ix)
   5664 46            [ 7]  259 	ld	b, (hl)
   5665 21 84 55      [10]  260 	ld	hl,#_kplayermovespeed + 0
   5668 4E            [ 7]  261 	ld	c, (hl)
   5669 79            [ 4]  262 	ld	a, c
   566A 90            [ 4]  263 	sub	a, b
   566B E2 70 56      [10]  264 	jp	PO, 00225$
   566E EE 80         [ 7]  265 	xor	a, #0x80
   5670                     266 00225$:
   5670 F2 7A 56      [10]  267 	jp	P, 00119$
   5673 DD 6E FC      [19]  268 	ld	l,-4 (ix)
   5676 DD 66 FD      [19]  269 	ld	h,-3 (ix)
   5679 71            [ 7]  270 	ld	(hl), c
   567A                     271 00119$:
                            272 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   567A DD 6E FC      [19]  273 	ld	l,-4 (ix)
   567D DD 66 FD      [19]  274 	ld	h,-3 (ix)
   5680 7E            [ 7]  275 	ld	a, (hl)
   5681 DD 77 FA      [19]  276 	ld	-6 (ix), a
   5684 3A 84 55      [13]  277 	ld	a,(#_kplayermovespeed + 0)
   5687 DD 77 F9      [19]  278 	ld	-7 (ix), a
   568A DD 77 F7      [19]  279 	ld	-9 (ix), a
   568D DD 7E F9      [19]  280 	ld	a, -7 (ix)
   5690 17            [ 4]  281 	rla
   5691 9F            [ 4]  282 	sbc	a, a
   5692 DD 77 F8      [19]  283 	ld	-8 (ix), a
   5695 AF            [ 4]  284 	xor	a, a
   5696 DD 96 F7      [19]  285 	sub	a, -9 (ix)
   5699 DD 77 F7      [19]  286 	ld	-9 (ix), a
   569C 3E 00         [ 7]  287 	ld	a, #0x00
   569E DD 9E F8      [19]  288 	sbc	a, -8 (ix)
   56A1 DD 77 F8      [19]  289 	ld	-8 (ix), a
   56A4 DD 7E FA      [19]  290 	ld	a, -6 (ix)
   56A7 DD 77 FA      [19]  291 	ld	-6 (ix), a
   56AA 17            [ 4]  292 	rla
   56AB 9F            [ 4]  293 	sbc	a, a
   56AC DD 77 FB      [19]  294 	ld	-5 (ix), a
   56AF DD 7E FA      [19]  295 	ld	a, -6 (ix)
   56B2 DD 96 F7      [19]  296 	sub	a, -9 (ix)
   56B5 DD 7E FB      [19]  297 	ld	a, -5 (ix)
   56B8 DD 9E F8      [19]  298 	sbc	a, -8 (ix)
   56BB E2 C0 56      [10]  299 	jp	PO, 00226$
   56BE EE 80         [ 7]  300 	xor	a, #0x80
   56C0                     301 00226$:
   56C0 F2 CF 56      [10]  302 	jp	P, 00121$
   56C3 AF            [ 4]  303 	xor	a, a
   56C4 DD 96 F9      [19]  304 	sub	a, -7 (ix)
   56C7 4F            [ 4]  305 	ld	c, a
   56C8 DD 6E FC      [19]  306 	ld	l,-4 (ix)
   56CB DD 66 FD      [19]  307 	ld	h,-3 (ix)
   56CE 71            [ 7]  308 	ld	(hl), c
   56CF                     309 00121$:
                            310 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   56CF CD BA 4E      [17]  311 	call	_input_is_jump_just_pressed
   56D2 DD 75 F7      [19]  312 	ld	-9 (ix), l
   56D5 DD 7E FE      [19]  313 	ld	a, -2 (ix)
   56D8 C6 05         [ 7]  314 	add	a, #0x05
   56DA DD 77 FA      [19]  315 	ld	-6 (ix), a
   56DD DD 7E FF      [19]  316 	ld	a, -1 (ix)
   56E0 CE 00         [ 7]  317 	adc	a, #0x00
   56E2 DD 77 FB      [19]  318 	ld	-5 (ix), a
   56E5 DD 7E FE      [19]  319 	ld	a, -2 (ix)
   56E8 C6 01         [ 7]  320 	add	a, #0x01
   56EA DD 77 F5      [19]  321 	ld	-11 (ix), a
   56ED DD 7E FF      [19]  322 	ld	a, -1 (ix)
   56F0 CE 00         [ 7]  323 	adc	a, #0x00
   56F2 DD 77 F6      [19]  324 	ld	-10 (ix), a
                            325 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   56F5 DD 7E FE      [19]  326 	ld	a, -2 (ix)
   56F8 C6 03         [ 7]  327 	add	a, #0x03
   56FA DD 77 F3      [19]  328 	ld	-13 (ix), a
   56FD DD 7E FF      [19]  329 	ld	a, -1 (ix)
   5700 CE 00         [ 7]  330 	adc	a, #0x00
   5702 DD 77 F4      [19]  331 	ld	-12 (ix), a
                            332 ;src/entities/player.c:57: player->jump_hold = 5;
   5705 DD 7E FE      [19]  333 	ld	a, -2 (ix)
   5708 C6 08         [ 7]  334 	add	a, #0x08
   570A DD 77 F1      [19]  335 	ld	-15 (ix), a
   570D DD 7E FF      [19]  336 	ld	a, -1 (ix)
   5710 CE 00         [ 7]  337 	adc	a, #0x00
   5712 DD 77 F2      [19]  338 	ld	-14 (ix), a
                            339 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5715 DD 7E F7      [19]  340 	ld	a, -9 (ix)
   5718 B7            [ 4]  341 	or	a, a
   5719 28 3A         [12]  342 	jr	Z,00123$
   571B DD 6E FA      [19]  343 	ld	l,-6 (ix)
   571E DD 66 FB      [19]  344 	ld	h,-5 (ix)
   5721 7E            [ 7]  345 	ld	a, (hl)
   5722 DD 6E F5      [19]  346 	ld	l,-11 (ix)
   5725 DD 66 F6      [19]  347 	ld	h,-10 (ix)
   5728 4E            [ 7]  348 	ld	c, (hl)
   5729 06 00         [ 7]  349 	ld	b, #0x00
   572B DD 6E FE      [19]  350 	ld	l,-2 (ix)
   572E DD 66 FF      [19]  351 	ld	h,-1 (ix)
   5731 5E            [ 7]  352 	ld	e, (hl)
   5732 16 00         [ 7]  353 	ld	d, #0x00
   5734 F5            [11]  354 	push	af
   5735 33            [ 6]  355 	inc	sp
   5736 C5            [11]  356 	push	bc
   5737 D5            [11]  357 	push	de
   5738 CD 64 4A      [17]  358 	call	_collision_is_on_ground_at
   573B F1            [10]  359 	pop	af
   573C F1            [10]  360 	pop	af
   573D 33            [ 6]  361 	inc	sp
   573E 7D            [ 4]  362 	ld	a, l
   573F B7            [ 4]  363 	or	a, a
   5740 28 13         [12]  364 	jr	Z,00123$
                            365 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   5742 21 89 55      [10]  366 	ld	hl,#_kplayerjumpvelocity + 0
   5745 4E            [ 7]  367 	ld	c, (hl)
   5746 DD 6E F3      [19]  368 	ld	l,-13 (ix)
   5749 DD 66 F4      [19]  369 	ld	h,-12 (ix)
   574C 71            [ 7]  370 	ld	(hl), c
                            371 ;src/entities/player.c:57: player->jump_hold = 5;
   574D DD 6E F1      [19]  372 	ld	l,-15 (ix)
   5750 DD 66 F2      [19]  373 	ld	h,-14 (ix)
   5753 36 05         [10]  374 	ld	(hl), #0x05
   5755                     375 00123$:
                            376 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5755 CD B2 4E      [17]  377 	call	_input_is_jump_pressed
   5758 DD 75 F7      [19]  378 	ld	-9 (ix), l
   575B 7D            [ 4]  379 	ld	a, l
   575C B7            [ 4]  380 	or	a, a
   575D 28 41         [12]  381 	jr	Z,00126$
   575F DD 6E F1      [19]  382 	ld	l,-15 (ix)
   5762 DD 66 F2      [19]  383 	ld	h,-14 (ix)
   5765 7E            [ 7]  384 	ld	a, (hl)
   5766 DD 77 F7      [19]  385 	ld	-9 (ix), a
   5769 B7            [ 4]  386 	or	a, a
   576A 28 34         [12]  387 	jr	Z,00126$
   576C DD 6E F3      [19]  388 	ld	l,-13 (ix)
   576F DD 66 F4      [19]  389 	ld	h,-12 (ix)
   5772 7E            [ 7]  390 	ld	a, (hl)
   5773 DD 77 F7      [19]  391 	ld	-9 (ix), a
   5776 DD CB F7 7E   [20]  392 	bit	7, -9 (ix)
   577A 28 24         [12]  393 	jr	Z,00126$
                            394 ;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
   577C 3A 8A 55      [13]  395 	ld	a,(#_kplayerjumpboost + 0)
   577F DD 77 F9      [19]  396 	ld	-7 (ix), a
   5782 DD 7E F7      [19]  397 	ld	a, -9 (ix)
   5785 DD 86 F9      [19]  398 	add	a, -7 (ix)
   5788 DD 6E F3      [19]  399 	ld	l,-13 (ix)
   578B DD 66 F4      [19]  400 	ld	h,-12 (ix)
   578E 77            [ 7]  401 	ld	(hl), a
                            402 ;src/entities/player.c:62: player->jump_hold--;
   578F DD 6E F1      [19]  403 	ld	l,-15 (ix)
   5792 DD 66 F2      [19]  404 	ld	h,-14 (ix)
   5795 4E            [ 7]  405 	ld	c, (hl)
   5796 0D            [ 4]  406 	dec	c
   5797 DD 6E F1      [19]  407 	ld	l,-15 (ix)
   579A DD 66 F2      [19]  408 	ld	h,-14 (ix)
   579D 71            [ 7]  409 	ld	(hl), c
   579E 18 08         [12]  410 	jr	00127$
   57A0                     411 00126$:
                            412 ;src/entities/player.c:64: player->jump_hold = 0;
   57A0 DD 6E F1      [19]  413 	ld	l,-15 (ix)
   57A3 DD 66 F2      [19]  414 	ld	h,-14 (ix)
   57A6 36 00         [10]  415 	ld	(hl), #0x00
   57A8                     416 00127$:
                            417 ;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
   57A8 DD 6E F3      [19]  418 	ld	l,-13 (ix)
   57AB DD 66 F4      [19]  419 	ld	h,-12 (ix)
   57AE 4E            [ 7]  420 	ld	c, (hl)
   57AF 21 87 55      [10]  421 	ld	hl,#_kplayergravity + 0
   57B2 46            [ 7]  422 	ld	b, (hl)
   57B3 79            [ 4]  423 	ld	a, c
   57B4 80            [ 4]  424 	add	a, b
   57B5 4F            [ 4]  425 	ld	c, a
   57B6 DD 6E F3      [19]  426 	ld	l,-13 (ix)
   57B9 DD 66 F4      [19]  427 	ld	h,-12 (ix)
   57BC 71            [ 7]  428 	ld	(hl), c
                            429 ;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   57BD 21 88 55      [10]  430 	ld	hl,#_kplayermaxfall + 0
   57C0 46            [ 7]  431 	ld	b, (hl)
   57C1 78            [ 4]  432 	ld	a, b
   57C2 91            [ 4]  433 	sub	a, c
   57C3 E2 C8 57      [10]  434 	jp	PO, 00227$
   57C6 EE 80         [ 7]  435 	xor	a, #0x80
   57C8                     436 00227$:
   57C8 F2 D2 57      [10]  437 	jp	P, 00131$
   57CB DD 6E F3      [19]  438 	ld	l,-13 (ix)
   57CE DD 66 F4      [19]  439 	ld	h,-12 (ix)
   57D1 70            [ 7]  440 	ld	(hl), b
   57D2                     441 00131$:
                            442 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   57D2 DD 6E FE      [19]  443 	ld	l,-2 (ix)
   57D5 DD 66 FF      [19]  444 	ld	h,-1 (ix)
   57D8 4E            [ 7]  445 	ld	c, (hl)
   57D9 DD 71 F1      [19]  446 	ld	-15 (ix), c
   57DC DD 36 F2 00   [19]  447 	ld	-14 (ix), #0x00
   57E0 DD 6E FC      [19]  448 	ld	l,-4 (ix)
   57E3 DD 66 FD      [19]  449 	ld	h,-3 (ix)
   57E6 7E            [ 7]  450 	ld	a, (hl)
   57E7 DD 77 F7      [19]  451 	ld	-9 (ix), a
   57EA DD 77 F7      [19]  452 	ld	-9 (ix), a
   57ED 17            [ 4]  453 	rla
   57EE 9F            [ 4]  454 	sbc	a, a
   57EF DD 77 F8      [19]  455 	ld	-8 (ix), a
   57F2 DD 7E F7      [19]  456 	ld	a, -9 (ix)
   57F5 DD 86 F1      [19]  457 	add	a, -15 (ix)
   57F8 DD 77 EF      [19]  458 	ld	-17 (ix), a
   57FB DD 7E F8      [19]  459 	ld	a, -8 (ix)
   57FE DD 8E F2      [19]  460 	adc	a, -14 (ix)
   5801 DD 77 F0      [19]  461 	ld	-16 (ix), a
                            462 ;src/entities/player.c:71: if (nextx < 0) {
   5804 DD CB F0 7E   [20]  463 	bit	7, -16 (ix)
   5808 28 08         [12]  464 	jr	Z,00133$
                            465 ;src/entities/player.c:72: nextx = 0;
   580A DD 36 EF 00   [19]  466 	ld	-17 (ix), #0x00
   580E DD 36 F0 00   [19]  467 	ld	-16 (ix), #0x00
   5812                     468 00133$:
                            469 ;src/entities/player.c:74: if (nextx > 76) {
   5812 3E 4C         [ 7]  470 	ld	a, #0x4c
   5814 DD BE EF      [19]  471 	cp	a, -17 (ix)
   5817 3E 00         [ 7]  472 	ld	a, #0x00
   5819 DD 9E F0      [19]  473 	sbc	a, -16 (ix)
   581C E2 21 58      [10]  474 	jp	PO, 00228$
   581F EE 80         [ 7]  475 	xor	a, #0x80
   5821                     476 00228$:
   5821 F2 2C 58      [10]  477 	jp	P, 00135$
                            478 ;src/entities/player.c:75: nextx = 76;
   5824 DD 36 EF 4C   [19]  479 	ld	-17 (ix), #0x4c
   5828 DD 36 F0 00   [19]  480 	ld	-16 (ix), #0x00
   582C                     481 00135$:
                            482 ;src/entities/player.c:77: player->x = (u8)nextx;
   582C DD 7E EF      [19]  483 	ld	a, -17 (ix)
   582F DD 77 F1      [19]  484 	ld	-15 (ix), a
   5832 DD 6E FE      [19]  485 	ld	l,-2 (ix)
   5835 DD 66 FF      [19]  486 	ld	h,-1 (ix)
   5838 DD 7E F1      [19]  487 	ld	a, -15 (ix)
   583B 77            [ 7]  488 	ld	(hl), a
                            489 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   583C DD 6E F5      [19]  490 	ld	l,-11 (ix)
   583F DD 66 F6      [19]  491 	ld	h,-10 (ix)
   5842 4E            [ 7]  492 	ld	c, (hl)
   5843 DD 71 F7      [19]  493 	ld	-9 (ix), c
   5846 DD 36 F8 00   [19]  494 	ld	-8 (ix), #0x00
   584A DD 6E F3      [19]  495 	ld	l,-13 (ix)
   584D DD 66 F4      [19]  496 	ld	h,-12 (ix)
   5850 7E            [ 7]  497 	ld	a, (hl)
   5851 DD 77 FC      [19]  498 	ld	-4 (ix), a
   5854 17            [ 4]  499 	rla
   5855 9F            [ 4]  500 	sbc	a, a
   5856 DD 77 FD      [19]  501 	ld	-3 (ix), a
   5859 DD 7E FC      [19]  502 	ld	a, -4 (ix)
   585C DD 86 F7      [19]  503 	add	a, -9 (ix)
   585F DD 77 F7      [19]  504 	ld	-9 (ix), a
   5862 DD 7E FD      [19]  505 	ld	a, -3 (ix)
   5865 DD 8E F8      [19]  506 	adc	a, -8 (ix)
   5868 DD 77 F8      [19]  507 	ld	-8 (ix), a
                            508 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   586B DD 6E FA      [19]  509 	ld	l,-6 (ix)
   586E DD 66 FB      [19]  510 	ld	h,-5 (ix)
   5871 7E            [ 7]  511 	ld	a, (hl)
   5872 DD 77 F9      [19]  512 	ld	-7 (ix), a
   5875 DD 7E F1      [19]  513 	ld	a, -15 (ix)
   5878 DD 77 F1      [19]  514 	ld	-15 (ix), a
   587B DD 36 F2 00   [19]  515 	ld	-14 (ix), #0x00
   587F DD 7E F9      [19]  516 	ld	a, -7 (ix)
   5882 F5            [11]  517 	push	af
   5883 33            [ 6]  518 	inc	sp
   5884 DD 6E F7      [19]  519 	ld	l,-9 (ix)
   5887 DD 66 F8      [19]  520 	ld	h,-8 (ix)
   588A E5            [11]  521 	push	hl
   588B DD 6E F1      [19]  522 	ld	l,-15 (ix)
   588E DD 66 F2      [19]  523 	ld	h,-14 (ix)
   5891 E5            [11]  524 	push	hl
   5892 CD E3 4A      [17]  525 	call	_collision_clamp_y_at
   5895 F1            [10]  526 	pop	af
   5896 F1            [10]  527 	pop	af
   5897 33            [ 6]  528 	inc	sp
   5898 DD 74 F2      [19]  529 	ld	-14 (ix), h
   589B DD 75 F1      [19]  530 	ld	-15 (ix), l
   589E DD 75 ED      [19]  531 	ld	-19 (ix), l
   58A1 DD 7E F2      [19]  532 	ld	a, -14 (ix)
   58A4 DD 77 EE      [19]  533 	ld	-18 (ix), a
                            534 ;src/entities/player.c:81: if (nexty < 0) {
   58A7 DD CB EE 7E   [20]  535 	bit	7, -18 (ix)
   58AB 28 04         [12]  536 	jr	Z,00137$
                            537 ;src/entities/player.c:82: nexty = 0;
   58AD 21 00 00      [10]  538 	ld	hl, #0x0000
   58B0 E3            [19]  539 	ex	(sp), hl
   58B1                     540 00137$:
                            541 ;src/entities/player.c:84: player->y = (u8)nexty;
   58B1 DD 4E ED      [19]  542 	ld	c, -19 (ix)
   58B4 DD 6E F5      [19]  543 	ld	l,-11 (ix)
   58B7 DD 66 F6      [19]  544 	ld	h,-10 (ix)
   58BA 71            [ 7]  545 	ld	(hl), c
                            546 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   58BB DD 6E FA      [19]  547 	ld	l,-6 (ix)
   58BE DD 66 FB      [19]  548 	ld	h,-5 (ix)
   58C1 7E            [ 7]  549 	ld	a, (hl)
   58C2 06 00         [ 7]  550 	ld	b, #0x00
   58C4 DD 6E FE      [19]  551 	ld	l,-2 (ix)
   58C7 DD 66 FF      [19]  552 	ld	h,-1 (ix)
   58CA 5E            [ 7]  553 	ld	e, (hl)
   58CB 16 00         [ 7]  554 	ld	d, #0x00
   58CD F5            [11]  555 	push	af
   58CE 33            [ 6]  556 	inc	sp
   58CF C5            [11]  557 	push	bc
   58D0 D5            [11]  558 	push	de
   58D1 CD 64 4A      [17]  559 	call	_collision_is_on_ground_at
   58D4 F1            [10]  560 	pop	af
   58D5 F1            [10]  561 	pop	af
   58D6 33            [ 6]  562 	inc	sp
   58D7 7D            [ 4]  563 	ld	a, l
   58D8 B7            [ 4]  564 	or	a, a
   58D9 28 19         [12]  565 	jr	Z,00141$
   58DB DD 6E F3      [19]  566 	ld	l,-13 (ix)
   58DE DD 66 F4      [19]  567 	ld	h,-12 (ix)
   58E1 4E            [ 7]  568 	ld	c, (hl)
   58E2 AF            [ 4]  569 	xor	a, a
   58E3 91            [ 4]  570 	sub	a, c
   58E4 E2 E9 58      [10]  571 	jp	PO, 00229$
   58E7 EE 80         [ 7]  572 	xor	a, #0x80
   58E9                     573 00229$:
   58E9 F2 F4 58      [10]  574 	jp	P, 00141$
                            575 ;src/entities/player.c:87: player->vy = 0;
   58EC DD 6E F3      [19]  576 	ld	l,-13 (ix)
   58EF DD 66 F4      [19]  577 	ld	h,-12 (ix)
   58F2 36 00         [10]  578 	ld	(hl), #0x00
   58F4                     579 00141$:
   58F4 DD F9         [10]  580 	ld	sp, ix
   58F6 DD E1         [14]  581 	pop	ix
   58F8 C9            [10]  582 	ret
                            583 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            584 ;	---------------------------------
                            585 ; Function playerrender
                            586 ; ---------------------------------
   58F9                     587 _playerrender::
   58F9 DD E5         [15]  588 	push	ix
   58FB DD 21 00 00   [14]  589 	ld	ix,#0
   58FF DD 39         [15]  590 	add	ix,sp
                            591 ;src/entities/player.c:94: if (!player) {
   5901 DD 7E 05      [19]  592 	ld	a, 5 (ix)
   5904 DD B6 04      [19]  593 	or	a,4 (ix)
                            594 ;src/entities/player.c:95: return;
   5907 28 32         [12]  595 	jr	Z,00103$
                            596 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5909 DD 5E 04      [19]  597 	ld	e,4 (ix)
   590C DD 56 05      [19]  598 	ld	d,5 (ix)
   590F 6B            [ 4]  599 	ld	l, e
   5910 62            [ 4]  600 	ld	h, d
   5911 23            [ 6]  601 	inc	hl
   5912 46            [ 7]  602 	ld	b, (hl)
   5913 1A            [ 7]  603 	ld	a, (de)
   5914 D5            [11]  604 	push	de
   5915 C5            [11]  605 	push	bc
   5916 33            [ 6]  606 	inc	sp
   5917 F5            [11]  607 	push	af
   5918 33            [ 6]  608 	inc	sp
   5919 21 00 C0      [10]  609 	ld	hl, #0xc000
   591C E5            [11]  610 	push	hl
   591D CD 74 5D      [17]  611 	call	_cpct_getScreenPtr
   5920 4D            [ 4]  612 	ld	c, l
   5921 44            [ 4]  613 	ld	b, h
   5922 D1            [10]  614 	pop	de
                            615 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   5923 D5            [11]  616 	push	de
   5924 FD E1         [14]  617 	pop	iy
   5926 FD 7E 05      [19]  618 	ld	a, 5 (iy)
   5929 EB            [ 4]  619 	ex	de,hl
   592A 11 04 00      [10]  620 	ld	de, #0x0004
   592D 19            [11]  621 	add	hl, de
   592E 56            [ 7]  622 	ld	d, (hl)
   592F F5            [11]  623 	push	af
   5930 33            [ 6]  624 	inc	sp
   5931 1E 4F         [ 7]  625 	ld	e, #0x4f
   5933 D5            [11]  626 	push	de
   5934 C5            [11]  627 	push	bc
   5935 CD BB 5C      [17]  628 	call	_cpct_drawSolidBox
   5938 F1            [10]  629 	pop	af
   5939 F1            [10]  630 	pop	af
   593A 33            [ 6]  631 	inc	sp
   593B                     632 00103$:
   593B DD E1         [14]  633 	pop	ix
   593D C9            [10]  634 	ret
                            635 	.area _CODE
                            636 	.area _INITIALIZER
                            637 	.area _CABS (ABS)
