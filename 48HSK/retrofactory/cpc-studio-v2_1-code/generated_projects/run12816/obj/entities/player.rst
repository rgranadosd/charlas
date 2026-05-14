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
   51DF                      57 _playerinit::
                             58 ;src/entities/player.c:15: if (!player) {
   51DF 21 03 00      [10]   59 	ld	hl, #2+1
   51E2 39            [11]   60 	add	hl, sp
   51E3 7E            [ 7]   61 	ld	a, (hl)
   51E4 2B            [ 6]   62 	dec	hl
   51E5 B6            [ 7]   63 	or	a,(hl)
                             64 ;src/entities/player.c:16: return;
   51E6 C8            [11]   65 	ret	Z
                             66 ;src/entities/player.c:19: player->x = 20;
   51E7 D1            [10]   67 	pop	de
   51E8 C1            [10]   68 	pop	bc
   51E9 C5            [11]   69 	push	bc
   51EA D5            [11]   70 	push	de
   51EB 3E 14         [ 7]   71 	ld	a, #0x14
   51ED 02            [ 7]   72 	ld	(bc), a
                             73 ;src/entities/player.c:20: player->y = 120;
   51EE 69            [ 4]   74 	ld	l, c
   51EF 60            [ 4]   75 	ld	h, b
   51F0 23            [ 6]   76 	inc	hl
   51F1 36 78         [10]   77 	ld	(hl), #0x78
                             78 ;src/entities/player.c:21: player->vx = 0;
   51F3 59            [ 4]   79 	ld	e, c
   51F4 50            [ 4]   80 	ld	d, b
   51F5 13            [ 6]   81 	inc	de
   51F6 13            [ 6]   82 	inc	de
   51F7 AF            [ 4]   83 	xor	a, a
   51F8 12            [ 7]   84 	ld	(de), a
                             85 ;src/entities/player.c:22: player->vy = 0;
   51F9 59            [ 4]   86 	ld	e, c
   51FA 50            [ 4]   87 	ld	d, b
   51FB 13            [ 6]   88 	inc	de
   51FC 13            [ 6]   89 	inc	de
   51FD 13            [ 6]   90 	inc	de
   51FE AF            [ 4]   91 	xor	a, a
   51FF 12            [ 7]   92 	ld	(de), a
                             93 ;src/entities/player.c:23: player->w = 4;
   5200 21 04 00      [10]   94 	ld	hl, #0x0004
   5203 09            [11]   95 	add	hl, bc
   5204 36 04         [10]   96 	ld	(hl), #0x04
                             97 ;src/entities/player.c:24: player->h = 16;
   5206 21 05 00      [10]   98 	ld	hl, #0x0005
   5209 09            [11]   99 	add	hl, bc
   520A 36 10         [10]  100 	ld	(hl), #0x10
                            101 ;src/entities/player.c:25: player->health = 3;
   520C 21 06 00      [10]  102 	ld	hl, #0x0006
   520F 09            [11]  103 	add	hl, bc
   5210 36 03         [10]  104 	ld	(hl), #0x03
                            105 ;src/entities/player.c:26: player->facing_left = 0;
   5212 21 07 00      [10]  106 	ld	hl, #0x0007
   5215 09            [11]  107 	add	hl, bc
   5216 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/player.c:27: player->jump_hold = 0;
   5218 21 08 00      [10]  110 	ld	hl, #0x0008
   521B 09            [11]  111 	add	hl, bc
   521C 36 00         [10]  112 	ld	(hl), #0x00
   521E C9            [10]  113 	ret
   521F                     114 _kplayermovespeed:
   521F 03                  115 	.db #0x03	;  3
   5220                     116 _kplayeracceleration:
   5220 01                  117 	.db #0x01	;  1
   5221                     118 _kplayerdeceleration:
   5221 01                  119 	.db #0x01	;  1
   5222                     120 _kplayergravity:
   5222 01                  121 	.db #0x01	;  1
   5223                     122 _kplayermaxfall:
   5223 04                  123 	.db #0x04	;  4
   5224                     124 _kplayerjumpvelocity:
   5224 FA                  125 	.db #0xfa	; -6
   5225                     126 _kplayerjumpboost:
   5225 FF                  127 	.db #0xff	; -1
                            128 ;src/entities/player.c:30: void playerupdate(Player* player) {
                            129 ;	---------------------------------
                            130 ; Function playerupdate
                            131 ; ---------------------------------
   5226                     132 _playerupdate::
   5226 DD E5         [15]  133 	push	ix
   5228 DD 21 00 00   [14]  134 	ld	ix,#0
   522C DD 39         [15]  135 	add	ix,sp
   522E 21 ED FF      [10]  136 	ld	hl, #-19
   5231 39            [11]  137 	add	hl, sp
   5232 F9            [ 6]  138 	ld	sp, hl
                            139 ;src/entities/player.c:34: if (!player) {
   5233 DD 7E 05      [19]  140 	ld	a, 5 (ix)
   5236 DD B6 04      [19]  141 	or	a,4 (ix)
                            142 ;src/entities/player.c:35: return;
   5239 CA 8F 55      [10]  143 	jp	Z,00141$
                            144 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   523C CD DA 4A      [17]  145 	call	_input_is_left_pressed
   523F 4D            [ 4]  146 	ld	c, l
                            147 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   5240 DD 7E 04      [19]  148 	ld	a, 4 (ix)
   5243 DD 77 FE      [19]  149 	ld	-2 (ix), a
   5246 DD 7E 05      [19]  150 	ld	a, 5 (ix)
   5249 DD 77 FF      [19]  151 	ld	-1 (ix), a
   524C DD 7E FE      [19]  152 	ld	a, -2 (ix)
   524F C6 02         [ 7]  153 	add	a, #0x02
   5251 DD 77 FC      [19]  154 	ld	-4 (ix), a
   5254 DD 7E FF      [19]  155 	ld	a, -1 (ix)
   5257 CE 00         [ 7]  156 	adc	a, #0x00
   5259 DD 77 FD      [19]  157 	ld	-3 (ix), a
                            158 ;src/entities/player.c:40: player->facing_left = 1;
   525C DD 7E FE      [19]  159 	ld	a, -2 (ix)
   525F C6 07         [ 7]  160 	add	a, #0x07
   5261 DD 77 FA      [19]  161 	ld	-6 (ix), a
   5264 DD 7E FF      [19]  162 	ld	a, -1 (ix)
   5267 CE 00         [ 7]  163 	adc	a, #0x00
   5269 DD 77 FB      [19]  164 	ld	-5 (ix), a
                            165 ;src/entities/player.c:38: if (input_is_left_pressed()) {
   526C 79            [ 4]  166 	ld	a, c
   526D B7            [ 4]  167 	or	a, a
   526E 28 1E         [12]  168 	jr	Z,00116$
                            169 ;src/entities/player.c:39: player->vx = (i8)(player->vx - kplayeracceleration);
   5270 DD 6E FC      [19]  170 	ld	l,-4 (ix)
   5273 DD 66 FD      [19]  171 	ld	h,-3 (ix)
   5276 4E            [ 7]  172 	ld	c, (hl)
   5277 21 20 52      [10]  173 	ld	hl,#_kplayeracceleration + 0
   527A 46            [ 7]  174 	ld	b, (hl)
   527B 79            [ 4]  175 	ld	a, c
   527C 90            [ 4]  176 	sub	a, b
   527D DD 6E FC      [19]  177 	ld	l,-4 (ix)
   5280 DD 66 FD      [19]  178 	ld	h,-3 (ix)
   5283 77            [ 7]  179 	ld	(hl), a
                            180 ;src/entities/player.c:40: player->facing_left = 1;
   5284 DD 6E FA      [19]  181 	ld	l,-6 (ix)
   5287 DD 66 FB      [19]  182 	ld	h,-5 (ix)
   528A 36 01         [10]  183 	ld	(hl), #0x01
   528C 18 6B         [12]  184 	jr	00117$
   528E                     185 00116$:
                            186 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   528E CD E2 4A      [17]  187 	call	_input_is_right_pressed
   5291 7D            [ 4]  188 	ld	a, l
                            189 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5292 DD 6E FC      [19]  190 	ld	l,-4 (ix)
   5295 DD 66 FD      [19]  191 	ld	h,-3 (ix)
   5298 4E            [ 7]  192 	ld	c, (hl)
                            193 ;src/entities/player.c:41: } else if (input_is_right_pressed()) {
   5299 B7            [ 4]  194 	or	a, a
   529A 28 17         [12]  195 	jr	Z,00113$
                            196 ;src/entities/player.c:42: player->vx = (i8)(player->vx + kplayeracceleration);
   529C 21 20 52      [10]  197 	ld	hl,#_kplayeracceleration + 0
   529F 5E            [ 7]  198 	ld	e, (hl)
   52A0 79            [ 4]  199 	ld	a, c
   52A1 83            [ 4]  200 	add	a, e
   52A2 DD 6E FC      [19]  201 	ld	l,-4 (ix)
   52A5 DD 66 FD      [19]  202 	ld	h,-3 (ix)
   52A8 77            [ 7]  203 	ld	(hl), a
                            204 ;src/entities/player.c:43: player->facing_left = 0;
   52A9 DD 6E FA      [19]  205 	ld	l,-6 (ix)
   52AC DD 66 FB      [19]  206 	ld	h,-5 (ix)
   52AF 36 00         [10]  207 	ld	(hl), #0x00
   52B1 18 46         [12]  208 	jr	00117$
   52B3                     209 00113$:
                            210 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   52B3 21 21 52      [10]  211 	ld	hl,#_kplayerdeceleration + 0
   52B6 46            [ 7]  212 	ld	b, (hl)
                            213 ;src/entities/player.c:44: } else if (player->vx > 0) {
   52B7 AF            [ 4]  214 	xor	a, a
   52B8 91            [ 4]  215 	sub	a, c
   52B9 E2 BE 52      [10]  216 	jp	PO, 00223$
   52BC EE 80         [ 7]  217 	xor	a, #0x80
   52BE                     218 00223$:
   52BE F2 D9 52      [10]  219 	jp	P, 00110$
                            220 ;src/entities/player.c:45: player->vx = (i8)(player->vx - kplayerdeceleration);
   52C1 79            [ 4]  221 	ld	a, c
   52C2 90            [ 4]  222 	sub	a, b
   52C3 4F            [ 4]  223 	ld	c, a
   52C4 DD 6E FC      [19]  224 	ld	l,-4 (ix)
   52C7 DD 66 FD      [19]  225 	ld	h,-3 (ix)
   52CA 71            [ 7]  226 	ld	(hl), c
                            227 ;src/entities/player.c:46: if (player->vx < 0) player->vx = 0;
   52CB CB 79         [ 8]  228 	bit	7, c
   52CD 28 2A         [12]  229 	jr	Z,00117$
   52CF DD 6E FC      [19]  230 	ld	l,-4 (ix)
   52D2 DD 66 FD      [19]  231 	ld	h,-3 (ix)
   52D5 36 00         [10]  232 	ld	(hl), #0x00
   52D7 18 20         [12]  233 	jr	00117$
   52D9                     234 00110$:
                            235 ;src/entities/player.c:47: } else if (player->vx < 0) {
   52D9 CB 79         [ 8]  236 	bit	7, c
   52DB 28 1C         [12]  237 	jr	Z,00117$
                            238 ;src/entities/player.c:48: player->vx = (i8)(player->vx + kplayerdeceleration);
   52DD 79            [ 4]  239 	ld	a, c
   52DE 80            [ 4]  240 	add	a, b
   52DF 4F            [ 4]  241 	ld	c, a
   52E0 DD 6E FC      [19]  242 	ld	l,-4 (ix)
   52E3 DD 66 FD      [19]  243 	ld	h,-3 (ix)
   52E6 71            [ 7]  244 	ld	(hl), c
                            245 ;src/entities/player.c:49: if (player->vx > 0) player->vx = 0;
   52E7 AF            [ 4]  246 	xor	a, a
   52E8 91            [ 4]  247 	sub	a, c
   52E9 E2 EE 52      [10]  248 	jp	PO, 00224$
   52EC EE 80         [ 7]  249 	xor	a, #0x80
   52EE                     250 00224$:
   52EE F2 F9 52      [10]  251 	jp	P, 00117$
   52F1 DD 6E FC      [19]  252 	ld	l,-4 (ix)
   52F4 DD 66 FD      [19]  253 	ld	h,-3 (ix)
   52F7 36 00         [10]  254 	ld	(hl), #0x00
   52F9                     255 00117$:
                            256 ;src/entities/player.c:52: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   52F9 DD 6E FC      [19]  257 	ld	l,-4 (ix)
   52FC DD 66 FD      [19]  258 	ld	h,-3 (ix)
   52FF 46            [ 7]  259 	ld	b, (hl)
   5300 21 1F 52      [10]  260 	ld	hl,#_kplayermovespeed + 0
   5303 4E            [ 7]  261 	ld	c, (hl)
   5304 79            [ 4]  262 	ld	a, c
   5305 90            [ 4]  263 	sub	a, b
   5306 E2 0B 53      [10]  264 	jp	PO, 00225$
   5309 EE 80         [ 7]  265 	xor	a, #0x80
   530B                     266 00225$:
   530B F2 15 53      [10]  267 	jp	P, 00119$
   530E DD 6E FC      [19]  268 	ld	l,-4 (ix)
   5311 DD 66 FD      [19]  269 	ld	h,-3 (ix)
   5314 71            [ 7]  270 	ld	(hl), c
   5315                     271 00119$:
                            272 ;src/entities/player.c:53: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5315 DD 6E FC      [19]  273 	ld	l,-4 (ix)
   5318 DD 66 FD      [19]  274 	ld	h,-3 (ix)
   531B 7E            [ 7]  275 	ld	a, (hl)
   531C DD 77 FA      [19]  276 	ld	-6 (ix), a
   531F 3A 1F 52      [13]  277 	ld	a,(#_kplayermovespeed + 0)
   5322 DD 77 F9      [19]  278 	ld	-7 (ix), a
   5325 DD 77 F7      [19]  279 	ld	-9 (ix), a
   5328 DD 7E F9      [19]  280 	ld	a, -7 (ix)
   532B 17            [ 4]  281 	rla
   532C 9F            [ 4]  282 	sbc	a, a
   532D DD 77 F8      [19]  283 	ld	-8 (ix), a
   5330 AF            [ 4]  284 	xor	a, a
   5331 DD 96 F7      [19]  285 	sub	a, -9 (ix)
   5334 DD 77 F7      [19]  286 	ld	-9 (ix), a
   5337 3E 00         [ 7]  287 	ld	a, #0x00
   5339 DD 9E F8      [19]  288 	sbc	a, -8 (ix)
   533C DD 77 F8      [19]  289 	ld	-8 (ix), a
   533F DD 7E FA      [19]  290 	ld	a, -6 (ix)
   5342 DD 77 FA      [19]  291 	ld	-6 (ix), a
   5345 17            [ 4]  292 	rla
   5346 9F            [ 4]  293 	sbc	a, a
   5347 DD 77 FB      [19]  294 	ld	-5 (ix), a
   534A DD 7E FA      [19]  295 	ld	a, -6 (ix)
   534D DD 96 F7      [19]  296 	sub	a, -9 (ix)
   5350 DD 7E FB      [19]  297 	ld	a, -5 (ix)
   5353 DD 9E F8      [19]  298 	sbc	a, -8 (ix)
   5356 E2 5B 53      [10]  299 	jp	PO, 00226$
   5359 EE 80         [ 7]  300 	xor	a, #0x80
   535B                     301 00226$:
   535B F2 6A 53      [10]  302 	jp	P, 00121$
   535E AF            [ 4]  303 	xor	a, a
   535F DD 96 F9      [19]  304 	sub	a, -7 (ix)
   5362 4F            [ 4]  305 	ld	c, a
   5363 DD 6E FC      [19]  306 	ld	l,-4 (ix)
   5366 DD 66 FD      [19]  307 	ld	h,-3 (ix)
   5369 71            [ 7]  308 	ld	(hl), c
   536A                     309 00121$:
                            310 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   536A CD F2 4A      [17]  311 	call	_input_is_jump_just_pressed
   536D DD 75 F7      [19]  312 	ld	-9 (ix), l
   5370 DD 7E FE      [19]  313 	ld	a, -2 (ix)
   5373 C6 05         [ 7]  314 	add	a, #0x05
   5375 DD 77 FA      [19]  315 	ld	-6 (ix), a
   5378 DD 7E FF      [19]  316 	ld	a, -1 (ix)
   537B CE 00         [ 7]  317 	adc	a, #0x00
   537D DD 77 FB      [19]  318 	ld	-5 (ix), a
   5380 DD 7E FE      [19]  319 	ld	a, -2 (ix)
   5383 C6 01         [ 7]  320 	add	a, #0x01
   5385 DD 77 F5      [19]  321 	ld	-11 (ix), a
   5388 DD 7E FF      [19]  322 	ld	a, -1 (ix)
   538B CE 00         [ 7]  323 	adc	a, #0x00
   538D DD 77 F6      [19]  324 	ld	-10 (ix), a
                            325 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   5390 DD 7E FE      [19]  326 	ld	a, -2 (ix)
   5393 C6 03         [ 7]  327 	add	a, #0x03
   5395 DD 77 F3      [19]  328 	ld	-13 (ix), a
   5398 DD 7E FF      [19]  329 	ld	a, -1 (ix)
   539B CE 00         [ 7]  330 	adc	a, #0x00
   539D DD 77 F4      [19]  331 	ld	-12 (ix), a
                            332 ;src/entities/player.c:57: player->jump_hold = 5;
   53A0 DD 7E FE      [19]  333 	ld	a, -2 (ix)
   53A3 C6 08         [ 7]  334 	add	a, #0x08
   53A5 DD 77 F1      [19]  335 	ld	-15 (ix), a
   53A8 DD 7E FF      [19]  336 	ld	a, -1 (ix)
   53AB CE 00         [ 7]  337 	adc	a, #0x00
   53AD DD 77 F2      [19]  338 	ld	-14 (ix), a
                            339 ;src/entities/player.c:55: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   53B0 DD 7E F7      [19]  340 	ld	a, -9 (ix)
   53B3 B7            [ 4]  341 	or	a, a
   53B4 28 3A         [12]  342 	jr	Z,00123$
   53B6 DD 6E FA      [19]  343 	ld	l,-6 (ix)
   53B9 DD 66 FB      [19]  344 	ld	h,-5 (ix)
   53BC 7E            [ 7]  345 	ld	a, (hl)
   53BD DD 6E F5      [19]  346 	ld	l,-11 (ix)
   53C0 DD 66 F6      [19]  347 	ld	h,-10 (ix)
   53C3 4E            [ 7]  348 	ld	c, (hl)
   53C4 06 00         [ 7]  349 	ld	b, #0x00
   53C6 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   53C9 DD 66 FF      [19]  351 	ld	h,-1 (ix)
   53CC 5E            [ 7]  352 	ld	e, (hl)
   53CD 16 00         [ 7]  353 	ld	d, #0x00
   53CF F5            [11]  354 	push	af
   53D0 33            [ 6]  355 	inc	sp
   53D1 C5            [11]  356 	push	bc
   53D2 D5            [11]  357 	push	de
   53D3 CD DE 46      [17]  358 	call	_collision_is_on_ground_at
   53D6 F1            [10]  359 	pop	af
   53D7 F1            [10]  360 	pop	af
   53D8 33            [ 6]  361 	inc	sp
   53D9 7D            [ 4]  362 	ld	a, l
   53DA B7            [ 4]  363 	or	a, a
   53DB 28 13         [12]  364 	jr	Z,00123$
                            365 ;src/entities/player.c:56: player->vy = kplayerjumpvelocity;
   53DD 21 24 52      [10]  366 	ld	hl,#_kplayerjumpvelocity + 0
   53E0 4E            [ 7]  367 	ld	c, (hl)
   53E1 DD 6E F3      [19]  368 	ld	l,-13 (ix)
   53E4 DD 66 F4      [19]  369 	ld	h,-12 (ix)
   53E7 71            [ 7]  370 	ld	(hl), c
                            371 ;src/entities/player.c:57: player->jump_hold = 5;
   53E8 DD 6E F1      [19]  372 	ld	l,-15 (ix)
   53EB DD 66 F2      [19]  373 	ld	h,-14 (ix)
   53EE 36 05         [10]  374 	ld	(hl), #0x05
   53F0                     375 00123$:
                            376 ;src/entities/player.c:60: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   53F0 CD EA 4A      [17]  377 	call	_input_is_jump_pressed
   53F3 DD 75 F7      [19]  378 	ld	-9 (ix), l
   53F6 7D            [ 4]  379 	ld	a, l
   53F7 B7            [ 4]  380 	or	a, a
   53F8 28 41         [12]  381 	jr	Z,00126$
   53FA DD 6E F1      [19]  382 	ld	l,-15 (ix)
   53FD DD 66 F2      [19]  383 	ld	h,-14 (ix)
   5400 7E            [ 7]  384 	ld	a, (hl)
   5401 DD 77 F7      [19]  385 	ld	-9 (ix), a
   5404 B7            [ 4]  386 	or	a, a
   5405 28 34         [12]  387 	jr	Z,00126$
   5407 DD 6E F3      [19]  388 	ld	l,-13 (ix)
   540A DD 66 F4      [19]  389 	ld	h,-12 (ix)
   540D 7E            [ 7]  390 	ld	a, (hl)
   540E DD 77 F7      [19]  391 	ld	-9 (ix), a
   5411 DD CB F7 7E   [20]  392 	bit	7, -9 (ix)
   5415 28 24         [12]  393 	jr	Z,00126$
                            394 ;src/entities/player.c:61: player->vy = (i8)(player->vy + kplayerjumpboost);
   5417 3A 25 52      [13]  395 	ld	a,(#_kplayerjumpboost + 0)
   541A DD 77 F9      [19]  396 	ld	-7 (ix), a
   541D DD 7E F7      [19]  397 	ld	a, -9 (ix)
   5420 DD 86 F9      [19]  398 	add	a, -7 (ix)
   5423 DD 6E F3      [19]  399 	ld	l,-13 (ix)
   5426 DD 66 F4      [19]  400 	ld	h,-12 (ix)
   5429 77            [ 7]  401 	ld	(hl), a
                            402 ;src/entities/player.c:62: player->jump_hold--;
   542A DD 6E F1      [19]  403 	ld	l,-15 (ix)
   542D DD 66 F2      [19]  404 	ld	h,-14 (ix)
   5430 4E            [ 7]  405 	ld	c, (hl)
   5431 0D            [ 4]  406 	dec	c
   5432 DD 6E F1      [19]  407 	ld	l,-15 (ix)
   5435 DD 66 F2      [19]  408 	ld	h,-14 (ix)
   5438 71            [ 7]  409 	ld	(hl), c
   5439 18 08         [12]  410 	jr	00127$
   543B                     411 00126$:
                            412 ;src/entities/player.c:64: player->jump_hold = 0;
   543B DD 6E F1      [19]  413 	ld	l,-15 (ix)
   543E DD 66 F2      [19]  414 	ld	h,-14 (ix)
   5441 36 00         [10]  415 	ld	(hl), #0x00
   5443                     416 00127$:
                            417 ;src/entities/player.c:67: player->vy = (i8)(player->vy + kplayergravity);
   5443 DD 6E F3      [19]  418 	ld	l,-13 (ix)
   5446 DD 66 F4      [19]  419 	ld	h,-12 (ix)
   5449 4E            [ 7]  420 	ld	c, (hl)
   544A 21 22 52      [10]  421 	ld	hl,#_kplayergravity + 0
   544D 46            [ 7]  422 	ld	b, (hl)
   544E 79            [ 4]  423 	ld	a, c
   544F 80            [ 4]  424 	add	a, b
   5450 4F            [ 4]  425 	ld	c, a
   5451 DD 6E F3      [19]  426 	ld	l,-13 (ix)
   5454 DD 66 F4      [19]  427 	ld	h,-12 (ix)
   5457 71            [ 7]  428 	ld	(hl), c
                            429 ;src/entities/player.c:68: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5458 21 23 52      [10]  430 	ld	hl,#_kplayermaxfall + 0
   545B 46            [ 7]  431 	ld	b, (hl)
   545C 78            [ 4]  432 	ld	a, b
   545D 91            [ 4]  433 	sub	a, c
   545E E2 63 54      [10]  434 	jp	PO, 00227$
   5461 EE 80         [ 7]  435 	xor	a, #0x80
   5463                     436 00227$:
   5463 F2 6D 54      [10]  437 	jp	P, 00131$
   5466 DD 6E F3      [19]  438 	ld	l,-13 (ix)
   5469 DD 66 F4      [19]  439 	ld	h,-12 (ix)
   546C 70            [ 7]  440 	ld	(hl), b
   546D                     441 00131$:
                            442 ;src/entities/player.c:70: nextx = (i16)player->x + (i16)player->vx;
   546D DD 6E FE      [19]  443 	ld	l,-2 (ix)
   5470 DD 66 FF      [19]  444 	ld	h,-1 (ix)
   5473 4E            [ 7]  445 	ld	c, (hl)
   5474 DD 71 F1      [19]  446 	ld	-15 (ix), c
   5477 DD 36 F2 00   [19]  447 	ld	-14 (ix), #0x00
   547B DD 6E FC      [19]  448 	ld	l,-4 (ix)
   547E DD 66 FD      [19]  449 	ld	h,-3 (ix)
   5481 7E            [ 7]  450 	ld	a, (hl)
   5482 DD 77 F7      [19]  451 	ld	-9 (ix), a
   5485 DD 77 F7      [19]  452 	ld	-9 (ix), a
   5488 17            [ 4]  453 	rla
   5489 9F            [ 4]  454 	sbc	a, a
   548A DD 77 F8      [19]  455 	ld	-8 (ix), a
   548D DD 7E F7      [19]  456 	ld	a, -9 (ix)
   5490 DD 86 F1      [19]  457 	add	a, -15 (ix)
   5493 DD 77 EF      [19]  458 	ld	-17 (ix), a
   5496 DD 7E F8      [19]  459 	ld	a, -8 (ix)
   5499 DD 8E F2      [19]  460 	adc	a, -14 (ix)
   549C DD 77 F0      [19]  461 	ld	-16 (ix), a
                            462 ;src/entities/player.c:71: if (nextx < 0) {
   549F DD CB F0 7E   [20]  463 	bit	7, -16 (ix)
   54A3 28 08         [12]  464 	jr	Z,00133$
                            465 ;src/entities/player.c:72: nextx = 0;
   54A5 DD 36 EF 00   [19]  466 	ld	-17 (ix), #0x00
   54A9 DD 36 F0 00   [19]  467 	ld	-16 (ix), #0x00
   54AD                     468 00133$:
                            469 ;src/entities/player.c:74: if (nextx > 76) {
   54AD 3E 4C         [ 7]  470 	ld	a, #0x4c
   54AF DD BE EF      [19]  471 	cp	a, -17 (ix)
   54B2 3E 00         [ 7]  472 	ld	a, #0x00
   54B4 DD 9E F0      [19]  473 	sbc	a, -16 (ix)
   54B7 E2 BC 54      [10]  474 	jp	PO, 00228$
   54BA EE 80         [ 7]  475 	xor	a, #0x80
   54BC                     476 00228$:
   54BC F2 C7 54      [10]  477 	jp	P, 00135$
                            478 ;src/entities/player.c:75: nextx = 76;
   54BF DD 36 EF 4C   [19]  479 	ld	-17 (ix), #0x4c
   54C3 DD 36 F0 00   [19]  480 	ld	-16 (ix), #0x00
   54C7                     481 00135$:
                            482 ;src/entities/player.c:77: player->x = (u8)nextx;
   54C7 DD 7E EF      [19]  483 	ld	a, -17 (ix)
   54CA DD 77 F1      [19]  484 	ld	-15 (ix), a
   54CD DD 6E FE      [19]  485 	ld	l,-2 (ix)
   54D0 DD 66 FF      [19]  486 	ld	h,-1 (ix)
   54D3 DD 7E F1      [19]  487 	ld	a, -15 (ix)
   54D6 77            [ 7]  488 	ld	(hl), a
                            489 ;src/entities/player.c:79: nexty = (i16)player->y + (i16)player->vy;
   54D7 DD 6E F5      [19]  490 	ld	l,-11 (ix)
   54DA DD 66 F6      [19]  491 	ld	h,-10 (ix)
   54DD 4E            [ 7]  492 	ld	c, (hl)
   54DE DD 71 F7      [19]  493 	ld	-9 (ix), c
   54E1 DD 36 F8 00   [19]  494 	ld	-8 (ix), #0x00
   54E5 DD 6E F3      [19]  495 	ld	l,-13 (ix)
   54E8 DD 66 F4      [19]  496 	ld	h,-12 (ix)
   54EB 7E            [ 7]  497 	ld	a, (hl)
   54EC DD 77 FC      [19]  498 	ld	-4 (ix), a
   54EF 17            [ 4]  499 	rla
   54F0 9F            [ 4]  500 	sbc	a, a
   54F1 DD 77 FD      [19]  501 	ld	-3 (ix), a
   54F4 DD 7E FC      [19]  502 	ld	a, -4 (ix)
   54F7 DD 86 F7      [19]  503 	add	a, -9 (ix)
   54FA DD 77 F7      [19]  504 	ld	-9 (ix), a
   54FD DD 7E FD      [19]  505 	ld	a, -3 (ix)
   5500 DD 8E F8      [19]  506 	adc	a, -8 (ix)
   5503 DD 77 F8      [19]  507 	ld	-8 (ix), a
                            508 ;src/entities/player.c:80: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5506 DD 6E FA      [19]  509 	ld	l,-6 (ix)
   5509 DD 66 FB      [19]  510 	ld	h,-5 (ix)
   550C 7E            [ 7]  511 	ld	a, (hl)
   550D DD 77 F9      [19]  512 	ld	-7 (ix), a
   5510 DD 7E F1      [19]  513 	ld	a, -15 (ix)
   5513 DD 77 F1      [19]  514 	ld	-15 (ix), a
   5516 DD 36 F2 00   [19]  515 	ld	-14 (ix), #0x00
   551A DD 7E F9      [19]  516 	ld	a, -7 (ix)
   551D F5            [11]  517 	push	af
   551E 33            [ 6]  518 	inc	sp
   551F DD 6E F7      [19]  519 	ld	l,-9 (ix)
   5522 DD 66 F8      [19]  520 	ld	h,-8 (ix)
   5525 E5            [11]  521 	push	hl
   5526 DD 6E F1      [19]  522 	ld	l,-15 (ix)
   5529 DD 66 F2      [19]  523 	ld	h,-14 (ix)
   552C E5            [11]  524 	push	hl
   552D CD 5D 47      [17]  525 	call	_collision_clamp_y_at
   5530 F1            [10]  526 	pop	af
   5531 F1            [10]  527 	pop	af
   5532 33            [ 6]  528 	inc	sp
   5533 DD 74 F2      [19]  529 	ld	-14 (ix), h
   5536 DD 75 F1      [19]  530 	ld	-15 (ix), l
   5539 DD 75 ED      [19]  531 	ld	-19 (ix), l
   553C DD 7E F2      [19]  532 	ld	a, -14 (ix)
   553F DD 77 EE      [19]  533 	ld	-18 (ix), a
                            534 ;src/entities/player.c:81: if (nexty < 0) {
   5542 DD CB EE 7E   [20]  535 	bit	7, -18 (ix)
   5546 28 04         [12]  536 	jr	Z,00137$
                            537 ;src/entities/player.c:82: nexty = 0;
   5548 21 00 00      [10]  538 	ld	hl, #0x0000
   554B E3            [19]  539 	ex	(sp), hl
   554C                     540 00137$:
                            541 ;src/entities/player.c:84: player->y = (u8)nexty;
   554C DD 4E ED      [19]  542 	ld	c, -19 (ix)
   554F DD 6E F5      [19]  543 	ld	l,-11 (ix)
   5552 DD 66 F6      [19]  544 	ld	h,-10 (ix)
   5555 71            [ 7]  545 	ld	(hl), c
                            546 ;src/entities/player.c:86: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5556 DD 6E FA      [19]  547 	ld	l,-6 (ix)
   5559 DD 66 FB      [19]  548 	ld	h,-5 (ix)
   555C 7E            [ 7]  549 	ld	a, (hl)
   555D 06 00         [ 7]  550 	ld	b, #0x00
   555F DD 6E FE      [19]  551 	ld	l,-2 (ix)
   5562 DD 66 FF      [19]  552 	ld	h,-1 (ix)
   5565 5E            [ 7]  553 	ld	e, (hl)
   5566 16 00         [ 7]  554 	ld	d, #0x00
   5568 F5            [11]  555 	push	af
   5569 33            [ 6]  556 	inc	sp
   556A C5            [11]  557 	push	bc
   556B D5            [11]  558 	push	de
   556C CD DE 46      [17]  559 	call	_collision_is_on_ground_at
   556F F1            [10]  560 	pop	af
   5570 F1            [10]  561 	pop	af
   5571 33            [ 6]  562 	inc	sp
   5572 7D            [ 4]  563 	ld	a, l
   5573 B7            [ 4]  564 	or	a, a
   5574 28 19         [12]  565 	jr	Z,00141$
   5576 DD 6E F3      [19]  566 	ld	l,-13 (ix)
   5579 DD 66 F4      [19]  567 	ld	h,-12 (ix)
   557C 4E            [ 7]  568 	ld	c, (hl)
   557D AF            [ 4]  569 	xor	a, a
   557E 91            [ 4]  570 	sub	a, c
   557F E2 84 55      [10]  571 	jp	PO, 00229$
   5582 EE 80         [ 7]  572 	xor	a, #0x80
   5584                     573 00229$:
   5584 F2 8F 55      [10]  574 	jp	P, 00141$
                            575 ;src/entities/player.c:87: player->vy = 0;
   5587 DD 6E F3      [19]  576 	ld	l,-13 (ix)
   558A DD 66 F4      [19]  577 	ld	h,-12 (ix)
   558D 36 00         [10]  578 	ld	(hl), #0x00
   558F                     579 00141$:
   558F DD F9         [10]  580 	ld	sp, ix
   5591 DD E1         [14]  581 	pop	ix
   5593 C9            [10]  582 	ret
                            583 ;src/entities/player.c:91: void playerrender(const Player* player) {
                            584 ;	---------------------------------
                            585 ; Function playerrender
                            586 ; ---------------------------------
   5594                     587 _playerrender::
   5594 DD E5         [15]  588 	push	ix
   5596 DD 21 00 00   [14]  589 	ld	ix,#0
   559A DD 39         [15]  590 	add	ix,sp
                            591 ;src/entities/player.c:94: if (!player) {
   559C DD 7E 05      [19]  592 	ld	a, 5 (ix)
   559F DD B6 04      [19]  593 	or	a,4 (ix)
                            594 ;src/entities/player.c:95: return;
   55A2 28 32         [12]  595 	jr	Z,00103$
                            596 ;src/entities/player.c:98: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   55A4 DD 5E 04      [19]  597 	ld	e,4 (ix)
   55A7 DD 56 05      [19]  598 	ld	d,5 (ix)
   55AA 6B            [ 4]  599 	ld	l, e
   55AB 62            [ 4]  600 	ld	h, d
   55AC 23            [ 6]  601 	inc	hl
   55AD 46            [ 7]  602 	ld	b, (hl)
   55AE 1A            [ 7]  603 	ld	a, (de)
   55AF D5            [11]  604 	push	de
   55B0 C5            [11]  605 	push	bc
   55B1 33            [ 6]  606 	inc	sp
   55B2 F5            [11]  607 	push	af
   55B3 33            [ 6]  608 	inc	sp
   55B4 21 00 C0      [10]  609 	ld	hl, #0xc000
   55B7 E5            [11]  610 	push	hl
   55B8 CD D5 59      [17]  611 	call	_cpct_getScreenPtr
   55BB 4D            [ 4]  612 	ld	c, l
   55BC 44            [ 4]  613 	ld	b, h
   55BD D1            [10]  614 	pop	de
                            615 ;src/entities/player.c:99: cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
   55BE D5            [11]  616 	push	de
   55BF FD E1         [14]  617 	pop	iy
   55C1 FD 7E 05      [19]  618 	ld	a, 5 (iy)
   55C4 EB            [ 4]  619 	ex	de,hl
   55C5 11 04 00      [10]  620 	ld	de, #0x0004
   55C8 19            [11]  621 	add	hl, de
   55C9 56            [ 7]  622 	ld	d, (hl)
   55CA F5            [11]  623 	push	af
   55CB 33            [ 6]  624 	inc	sp
   55CC 1E 4F         [ 7]  625 	ld	e, #0x4f
   55CE D5            [11]  626 	push	de
   55CF C5            [11]  627 	push	bc
   55D0 CD 1C 59      [17]  628 	call	_cpct_drawSolidBox
   55D3 F1            [10]  629 	pop	af
   55D4 F1            [10]  630 	pop	af
   55D5 33            [ 6]  631 	inc	sp
   55D6                     632 00103$:
   55D6 DD E1         [14]  633 	pop	ix
   55D8 C9            [10]  634 	ret
                            635 	.area _CODE
                            636 	.area _INITIALIZER
                            637 	.area _CABS (ABS)
