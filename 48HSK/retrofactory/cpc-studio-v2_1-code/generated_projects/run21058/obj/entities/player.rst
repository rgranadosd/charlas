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
                             18 	.globl _cpct_drawSprite
                             19 	.globl _playerinit
                             20 	.globl _playerupdate
                             21 	.globl _playerrender
                             22 	.globl _player_get_ammo
                             23 	.globl _player_get_health
                             24 	.globl _player_get_weapon
                             25 ;--------------------------------------------------------
                             26 ; special function registers
                             27 ;--------------------------------------------------------
                             28 ;--------------------------------------------------------
                             29 ; ram data
                             30 ;--------------------------------------------------------
                             31 	.area _DATA
                             32 ;--------------------------------------------------------
                             33 ; ram data
                             34 ;--------------------------------------------------------
                             35 	.area _INITIALIZED
                             36 ;--------------------------------------------------------
                             37 ; absolute external ram data
                             38 ;--------------------------------------------------------
                             39 	.area _DABS (ABS)
                             40 ;--------------------------------------------------------
                             41 ; global & static initialisations
                             42 ;--------------------------------------------------------
                             43 	.area _HOME
                             44 	.area _GSINIT
                             45 	.area _GSFINAL
                             46 	.area _GSINIT
                             47 ;--------------------------------------------------------
                             48 ; Home
                             49 ;--------------------------------------------------------
                             50 	.area _HOME
                             51 	.area _HOME
                             52 ;--------------------------------------------------------
                             53 ; code
                             54 ;--------------------------------------------------------
                             55 	.area _CODE
                             56 ;src/entities/player.c:17: void playerinit(Player* player) {
                             57 ;	---------------------------------
                             58 ; Function playerinit
                             59 ; ---------------------------------
   5BF2                      60 _playerinit::
                             61 ;src/entities/player.c:18: if (!player) {
   5BF2 21 03 00      [10]   62 	ld	hl, #2+1
   5BF5 39            [11]   63 	add	hl, sp
   5BF6 7E            [ 7]   64 	ld	a, (hl)
   5BF7 2B            [ 6]   65 	dec	hl
   5BF8 B6            [ 7]   66 	or	a,(hl)
                             67 ;src/entities/player.c:19: return;
   5BF9 C8            [11]   68 	ret	Z
                             69 ;src/entities/player.c:22: player->x = 20;
   5BFA D1            [10]   70 	pop	de
   5BFB C1            [10]   71 	pop	bc
   5BFC C5            [11]   72 	push	bc
   5BFD D5            [11]   73 	push	de
   5BFE 3E 14         [ 7]   74 	ld	a, #0x14
   5C00 02            [ 7]   75 	ld	(bc), a
                             76 ;src/entities/player.c:23: player->y = 120;
   5C01 69            [ 4]   77 	ld	l, c
   5C02 60            [ 4]   78 	ld	h, b
   5C03 23            [ 6]   79 	inc	hl
   5C04 36 78         [10]   80 	ld	(hl), #0x78
                             81 ;src/entities/player.c:24: player->vx = 0;
   5C06 59            [ 4]   82 	ld	e, c
   5C07 50            [ 4]   83 	ld	d, b
   5C08 13            [ 6]   84 	inc	de
   5C09 13            [ 6]   85 	inc	de
   5C0A AF            [ 4]   86 	xor	a, a
   5C0B 12            [ 7]   87 	ld	(de), a
                             88 ;src/entities/player.c:25: player->vy = 0;
   5C0C 59            [ 4]   89 	ld	e, c
   5C0D 50            [ 4]   90 	ld	d, b
   5C0E 13            [ 6]   91 	inc	de
   5C0F 13            [ 6]   92 	inc	de
   5C10 13            [ 6]   93 	inc	de
   5C11 AF            [ 4]   94 	xor	a, a
   5C12 12            [ 7]   95 	ld	(de), a
                             96 ;src/entities/player.c:26: player->w = 4;
   5C13 21 04 00      [10]   97 	ld	hl, #0x0004
   5C16 09            [11]   98 	add	hl, bc
   5C17 36 04         [10]   99 	ld	(hl), #0x04
                            100 ;src/entities/player.c:27: player->h = 16;
   5C19 21 05 00      [10]  101 	ld	hl, #0x0005
   5C1C 09            [11]  102 	add	hl, bc
   5C1D 36 10         [10]  103 	ld	(hl), #0x10
                            104 ;src/entities/player.c:28: player->health = 3;
   5C1F 21 06 00      [10]  105 	ld	hl, #0x0006
   5C22 09            [11]  106 	add	hl, bc
   5C23 36 03         [10]  107 	ld	(hl), #0x03
                            108 ;src/entities/player.c:29: player->weapon = 0;
   5C25 21 07 00      [10]  109 	ld	hl, #0x0007
   5C28 09            [11]  110 	add	hl, bc
   5C29 36 00         [10]  111 	ld	(hl), #0x00
                            112 ;src/entities/player.c:30: player->facing_left = 0;
   5C2B 21 08 00      [10]  113 	ld	hl, #0x0008
   5C2E 09            [11]  114 	add	hl, bc
   5C2F 36 00         [10]  115 	ld	(hl), #0x00
                            116 ;src/entities/player.c:31: player->jump_hold = 0;
   5C31 21 09 00      [10]  117 	ld	hl, #0x0009
   5C34 09            [11]  118 	add	hl, bc
   5C35 36 00         [10]  119 	ld	(hl), #0x00
   5C37 C9            [10]  120 	ret
                            121 ;src/entities/player.c:34: void playerupdate(Player* player) {
                            122 ;	---------------------------------
                            123 ; Function playerupdate
                            124 ; ---------------------------------
   5C38                     125 _playerupdate::
   5C38 DD E5         [15]  126 	push	ix
   5C3A DD 21 00 00   [14]  127 	ld	ix,#0
   5C3E DD 39         [15]  128 	add	ix,sp
   5C40 21 F2 FF      [10]  129 	ld	hl, #-14
   5C43 39            [11]  130 	add	hl, sp
   5C44 F9            [ 6]  131 	ld	sp, hl
                            132 ;src/entities/player.c:38: if (!player) {
   5C45 DD 7E 05      [19]  133 	ld	a, 5 (ix)
   5C48 DD B6 04      [19]  134 	or	a,4 (ix)
                            135 ;src/entities/player.c:39: return;
   5C4B CA 7F 5E      [10]  136 	jp	Z,00141$
                            137 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5C4E CD 20 52      [17]  138 	call	_input_is_left_pressed
                            139 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5C51 DD 4E 04      [19]  140 	ld	c,4 (ix)
   5C54 DD 46 05      [19]  141 	ld	b,5 (ix)
   5C57 59            [ 4]  142 	ld	e, c
   5C58 50            [ 4]  143 	ld	d, b
   5C59 13            [ 6]  144 	inc	de
   5C5A 13            [ 6]  145 	inc	de
                            146 ;src/entities/player.c:44: player->facing_left = 1;
   5C5B 79            [ 4]  147 	ld	a, c
   5C5C C6 08         [ 7]  148 	add	a, #0x08
   5C5E DD 77 FE      [19]  149 	ld	-2 (ix), a
   5C61 78            [ 4]  150 	ld	a, b
   5C62 CE 00         [ 7]  151 	adc	a, #0x00
   5C64 DD 77 FF      [19]  152 	ld	-1 (ix), a
                            153 ;src/entities/player.c:42: if (input_is_left_pressed()) {
   5C67 7D            [ 4]  154 	ld	a, l
   5C68 B7            [ 4]  155 	or	a, a
   5C69 28 0E         [12]  156 	jr	Z,00116$
                            157 ;src/entities/player.c:43: player->vx = (i8)(player->vx - kplayeracceleration);
   5C6B 1A            [ 7]  158 	ld	a, (de)
   5C6C C6 FF         [ 7]  159 	add	a, #0xff
   5C6E 12            [ 7]  160 	ld	(de), a
                            161 ;src/entities/player.c:44: player->facing_left = 1;
   5C6F DD 6E FE      [19]  162 	ld	l,-2 (ix)
   5C72 DD 66 FF      [19]  163 	ld	h,-1 (ix)
   5C75 36 01         [10]  164 	ld	(hl), #0x01
   5C77 18 55         [12]  165 	jr	00117$
   5C79                     166 00116$:
                            167 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5C79 C5            [11]  168 	push	bc
   5C7A D5            [11]  169 	push	de
   5C7B CD 28 52      [17]  170 	call	_input_is_right_pressed
   5C7E DD 75 FD      [19]  171 	ld	-3 (ix), l
   5C81 D1            [10]  172 	pop	de
   5C82 C1            [10]  173 	pop	bc
                            174 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5C83 1A            [ 7]  175 	ld	a, (de)
                            176 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5C84 6F            [ 4]  177 	ld	l,a
   5C85 3C            [ 4]  178 	inc	a
   5C86 DD 77 FC      [19]  179 	ld	-4 (ix), a
                            180 ;src/entities/player.c:45: } else if (input_is_right_pressed()) {
   5C89 DD 7E FD      [19]  181 	ld	a, -3 (ix)
   5C8C B7            [ 4]  182 	or	a, a
   5C8D 28 0E         [12]  183 	jr	Z,00113$
                            184 ;src/entities/player.c:46: player->vx = (i8)(player->vx + kplayeracceleration);
   5C8F DD 7E FC      [19]  185 	ld	a, -4 (ix)
   5C92 12            [ 7]  186 	ld	(de), a
                            187 ;src/entities/player.c:47: player->facing_left = 0;
   5C93 DD 6E FE      [19]  188 	ld	l,-2 (ix)
   5C96 DD 66 FF      [19]  189 	ld	h,-1 (ix)
   5C99 36 00         [10]  190 	ld	(hl), #0x00
   5C9B 18 31         [12]  191 	jr	00117$
   5C9D                     192 00113$:
                            193 ;src/entities/player.c:48: } else if (player->vx > 0) {
   5C9D AF            [ 4]  194 	xor	a, a
   5C9E 95            [ 4]  195 	sub	a, l
   5C9F E2 A4 5C      [10]  196 	jp	PO, 00223$
   5CA2 EE 80         [ 7]  197 	xor	a, #0x80
   5CA4                     198 00223$:
   5CA4 F2 B8 5C      [10]  199 	jp	P, 00110$
                            200 ;src/entities/player.c:49: player->vx = (i8)(player->vx - kplayerdeceleration);
   5CA7 7D            [ 4]  201 	ld	a, l
   5CA8 C6 FF         [ 7]  202 	add	a, #0xff
   5CAA DD 77 FD      [19]  203 	ld	-3 (ix), a
   5CAD 12            [ 7]  204 	ld	(de),a
                            205 ;src/entities/player.c:50: if (player->vx < 0) player->vx = 0;
   5CAE DD CB FD 7E   [20]  206 	bit	7, -3 (ix)
   5CB2 28 1A         [12]  207 	jr	Z,00117$
   5CB4 AF            [ 4]  208 	xor	a, a
   5CB5 12            [ 7]  209 	ld	(de), a
   5CB6 18 16         [12]  210 	jr	00117$
   5CB8                     211 00110$:
                            212 ;src/entities/player.c:51: } else if (player->vx < 0) {
   5CB8 CB 7D         [ 8]  213 	bit	7, l
   5CBA 28 12         [12]  214 	jr	Z,00117$
                            215 ;src/entities/player.c:52: player->vx = (i8)(player->vx + kplayerdeceleration);
   5CBC DD 7E FC      [19]  216 	ld	a, -4 (ix)
   5CBF 12            [ 7]  217 	ld	(de), a
                            218 ;src/entities/player.c:53: if (player->vx > 0) player->vx = 0;
   5CC0 AF            [ 4]  219 	xor	a, a
   5CC1 DD 96 FC      [19]  220 	sub	a, -4 (ix)
   5CC4 E2 C9 5C      [10]  221 	jp	PO, 00224$
   5CC7 EE 80         [ 7]  222 	xor	a, #0x80
   5CC9                     223 00224$:
   5CC9 F2 CE 5C      [10]  224 	jp	P, 00117$
   5CCC AF            [ 4]  225 	xor	a, a
   5CCD 12            [ 7]  226 	ld	(de), a
   5CCE                     227 00117$:
                            228 ;src/entities/player.c:56: if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
   5CCE 1A            [ 7]  229 	ld	a, (de)
   5CCF 6F            [ 4]  230 	ld	l, a
   5CD0 3E 03         [ 7]  231 	ld	a, #0x03
   5CD2 95            [ 4]  232 	sub	a, l
   5CD3 E2 D8 5C      [10]  233 	jp	PO, 00225$
   5CD6 EE 80         [ 7]  234 	xor	a, #0x80
   5CD8                     235 00225$:
   5CD8 F2 DE 5C      [10]  236 	jp	P, 00119$
   5CDB 3E 03         [ 7]  237 	ld	a, #0x03
   5CDD 12            [ 7]  238 	ld	(de), a
   5CDE                     239 00119$:
                            240 ;src/entities/player.c:57: if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;
   5CDE 1A            [ 7]  241 	ld	a, (de)
   5CDF EE 80         [ 7]  242 	xor	a, #0x80
   5CE1 D6 7D         [ 7]  243 	sub	a, #0x7d
   5CE3 30 03         [12]  244 	jr	NC,00121$
   5CE5 3E FD         [ 7]  245 	ld	a, #0xfd
   5CE7 12            [ 7]  246 	ld	(de), a
   5CE8                     247 00121$:
                            248 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5CE8 C5            [11]  249 	push	bc
   5CE9 D5            [11]  250 	push	de
   5CEA CD 48 52      [17]  251 	call	_input_is_jump_just_pressed
   5CED DD 75 FC      [19]  252 	ld	-4 (ix), l
   5CF0 D1            [10]  253 	pop	de
   5CF1 C1            [10]  254 	pop	bc
   5CF2 21 05 00      [10]  255 	ld	hl, #0x0005
   5CF5 09            [11]  256 	add	hl,bc
   5CF6 DD 75 FE      [19]  257 	ld	-2 (ix), l
   5CF9 DD 74 FF      [19]  258 	ld	-1 (ix), h
   5CFC 21 01 00      [10]  259 	ld	hl, #0x0001
   5CFF 09            [11]  260 	add	hl,bc
   5D00 DD 75 FA      [19]  261 	ld	-6 (ix), l
   5D03 DD 74 FB      [19]  262 	ld	-5 (ix), h
                            263 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5D06 21 03 00      [10]  264 	ld	hl, #0x0003
   5D09 09            [11]  265 	add	hl,bc
   5D0A DD 75 F8      [19]  266 	ld	-8 (ix), l
   5D0D DD 74 F9      [19]  267 	ld	-7 (ix), h
                            268 ;src/entities/player.c:61: player->jump_hold = 5;
   5D10 21 09 00      [10]  269 	ld	hl, #0x0009
   5D13 09            [11]  270 	add	hl,bc
   5D14 DD 75 F6      [19]  271 	ld	-10 (ix), l
   5D17 DD 74 F7      [19]  272 	ld	-9 (ix), h
                            273 ;src/entities/player.c:59: if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
   5D1A DD 7E FC      [19]  274 	ld	a, -4 (ix)
   5D1D B7            [ 4]  275 	or	a, a
   5D1E 28 4E         [12]  276 	jr	Z,00123$
   5D20 DD 6E FE      [19]  277 	ld	l,-2 (ix)
   5D23 DD 66 FF      [19]  278 	ld	h,-1 (ix)
   5D26 7E            [ 7]  279 	ld	a, (hl)
   5D27 DD 6E FA      [19]  280 	ld	l,-6 (ix)
   5D2A DD 66 FB      [19]  281 	ld	h,-5 (ix)
   5D2D 6E            [ 7]  282 	ld	l, (hl)
   5D2E DD 75 F4      [19]  283 	ld	-12 (ix), l
   5D31 DD 36 F5 00   [19]  284 	ld	-11 (ix), #0x00
   5D35 F5            [11]  285 	push	af
   5D36 0A            [ 7]  286 	ld	a, (bc)
   5D37 6F            [ 4]  287 	ld	l, a
   5D38 F1            [10]  288 	pop	af
   5D39 DD 75 F2      [19]  289 	ld	-14 (ix), l
   5D3C DD 36 F3 00   [19]  290 	ld	-13 (ix), #0x00
   5D40 C5            [11]  291 	push	bc
   5D41 D5            [11]  292 	push	de
   5D42 F5            [11]  293 	push	af
   5D43 33            [ 6]  294 	inc	sp
   5D44 DD 6E F4      [19]  295 	ld	l,-12 (ix)
   5D47 DD 66 F5      [19]  296 	ld	h,-11 (ix)
   5D4A E5            [11]  297 	push	hl
   5D4B DD 6E F2      [19]  298 	ld	l,-14 (ix)
   5D4E DD 66 F3      [19]  299 	ld	h,-13 (ix)
   5D51 E5            [11]  300 	push	hl
   5D52 CD FB 4C      [17]  301 	call	_collision_is_on_ground_at
   5D55 F1            [10]  302 	pop	af
   5D56 F1            [10]  303 	pop	af
   5D57 33            [ 6]  304 	inc	sp
   5D58 D1            [10]  305 	pop	de
   5D59 C1            [10]  306 	pop	bc
   5D5A 7D            [ 4]  307 	ld	a, l
   5D5B B7            [ 4]  308 	or	a, a
   5D5C 28 10         [12]  309 	jr	Z,00123$
                            310 ;src/entities/player.c:60: player->vy = kplayerjumpvelocity;
   5D5E DD 6E F8      [19]  311 	ld	l,-8 (ix)
   5D61 DD 66 F9      [19]  312 	ld	h,-7 (ix)
   5D64 36 FA         [10]  313 	ld	(hl), #0xfa
                            314 ;src/entities/player.c:61: player->jump_hold = 5;
   5D66 DD 6E F6      [19]  315 	ld	l,-10 (ix)
   5D69 DD 66 F7      [19]  316 	ld	h,-9 (ix)
   5D6C 36 05         [10]  317 	ld	(hl), #0x05
   5D6E                     318 00123$:
                            319 ;src/entities/player.c:64: if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
   5D6E C5            [11]  320 	push	bc
   5D6F D5            [11]  321 	push	de
   5D70 CD 40 52      [17]  322 	call	_input_is_jump_pressed
   5D73 7D            [ 4]  323 	ld	a, l
   5D74 D1            [10]  324 	pop	de
   5D75 C1            [10]  325 	pop	bc
   5D76 B7            [ 4]  326 	or	a, a
   5D77 28 31         [12]  327 	jr	Z,00126$
   5D79 DD 6E F6      [19]  328 	ld	l,-10 (ix)
   5D7C DD 66 F7      [19]  329 	ld	h,-9 (ix)
   5D7F 7E            [ 7]  330 	ld	a, (hl)
   5D80 B7            [ 4]  331 	or	a, a
   5D81 28 27         [12]  332 	jr	Z,00126$
   5D83 DD 6E F8      [19]  333 	ld	l,-8 (ix)
   5D86 DD 66 F9      [19]  334 	ld	h,-7 (ix)
   5D89 6E            [ 7]  335 	ld	l, (hl)
   5D8A CB 7D         [ 8]  336 	bit	7, l
   5D8C 28 1C         [12]  337 	jr	Z,00126$
                            338 ;src/entities/player.c:65: player->vy = (i8)(player->vy + kplayerjumpboost);
   5D8E 7D            [ 4]  339 	ld	a, l
   5D8F C6 FF         [ 7]  340 	add	a, #0xff
   5D91 DD 6E F8      [19]  341 	ld	l,-8 (ix)
   5D94 DD 66 F9      [19]  342 	ld	h,-7 (ix)
   5D97 77            [ 7]  343 	ld	(hl), a
                            344 ;src/entities/player.c:66: player->jump_hold--;
   5D98 DD 6E F6      [19]  345 	ld	l,-10 (ix)
   5D9B DD 66 F7      [19]  346 	ld	h,-9 (ix)
   5D9E 7E            [ 7]  347 	ld	a, (hl)
   5D9F C6 FF         [ 7]  348 	add	a, #0xff
   5DA1 DD 6E F6      [19]  349 	ld	l,-10 (ix)
   5DA4 DD 66 F7      [19]  350 	ld	h,-9 (ix)
   5DA7 77            [ 7]  351 	ld	(hl), a
   5DA8 18 08         [12]  352 	jr	00127$
   5DAA                     353 00126$:
                            354 ;src/entities/player.c:68: player->jump_hold = 0;
   5DAA DD 6E F6      [19]  355 	ld	l,-10 (ix)
   5DAD DD 66 F7      [19]  356 	ld	h,-9 (ix)
   5DB0 36 00         [10]  357 	ld	(hl), #0x00
   5DB2                     358 00127$:
                            359 ;src/entities/player.c:71: player->vy = (i8)(player->vy + kplayergravity);
   5DB2 DD 6E F8      [19]  360 	ld	l,-8 (ix)
   5DB5 DD 66 F9      [19]  361 	ld	h,-7 (ix)
   5DB8 7E            [ 7]  362 	ld	a, (hl)
   5DB9 3C            [ 4]  363 	inc	a
   5DBA DD 77 F2      [19]  364 	ld	-14 (ix), a
   5DBD DD 6E F8      [19]  365 	ld	l,-8 (ix)
   5DC0 DD 66 F9      [19]  366 	ld	h,-7 (ix)
   5DC3 DD 7E F2      [19]  367 	ld	a, -14 (ix)
   5DC6 77            [ 7]  368 	ld	(hl), a
                            369 ;src/entities/player.c:72: if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;
   5DC7 3E 04         [ 7]  370 	ld	a, #0x04
   5DC9 DD 96 F2      [19]  371 	sub	a, -14 (ix)
   5DCC E2 D1 5D      [10]  372 	jp	PO, 00226$
   5DCF EE 80         [ 7]  373 	xor	a, #0x80
   5DD1                     374 00226$:
   5DD1 F2 DC 5D      [10]  375 	jp	P, 00131$
   5DD4 DD 6E F8      [19]  376 	ld	l,-8 (ix)
   5DD7 DD 66 F9      [19]  377 	ld	h,-7 (ix)
   5DDA 36 04         [10]  378 	ld	(hl), #0x04
   5DDC                     379 00131$:
                            380 ;src/entities/player.c:74: nextx = (i16)player->x + (i16)player->vx;
   5DDC 0A            [ 7]  381 	ld	a, (bc)
   5DDD DD 77 F2      [19]  382 	ld	-14 (ix), a
   5DE0 DD 36 F3 00   [19]  383 	ld	-13 (ix), #0x00
   5DE4 1A            [ 7]  384 	ld	a, (de)
   5DE5 5F            [ 4]  385 	ld	e, a
   5DE6 17            [ 4]  386 	rla
   5DE7 9F            [ 4]  387 	sbc	a, a
   5DE8 57            [ 4]  388 	ld	d, a
   5DE9 E1            [10]  389 	pop	hl
   5DEA E5            [11]  390 	push	hl
   5DEB 19            [11]  391 	add	hl, de
                            392 ;src/entities/player.c:75: if (nextx < 0) {
   5DEC CB 7C         [ 8]  393 	bit	7, h
   5DEE 28 03         [12]  394 	jr	Z,00133$
                            395 ;src/entities/player.c:76: nextx = 0;
   5DF0 21 00 00      [10]  396 	ld	hl, #0x0000
   5DF3                     397 00133$:
                            398 ;src/entities/player.c:78: if (nextx > 76) {
   5DF3 3E 4C         [ 7]  399 	ld	a, #0x4c
   5DF5 BD            [ 4]  400 	cp	a, l
   5DF6 3E 00         [ 7]  401 	ld	a, #0x00
   5DF8 9C            [ 4]  402 	sbc	a, h
   5DF9 E2 FE 5D      [10]  403 	jp	PO, 00227$
   5DFC EE 80         [ 7]  404 	xor	a, #0x80
   5DFE                     405 00227$:
   5DFE F2 04 5E      [10]  406 	jp	P, 00135$
                            407 ;src/entities/player.c:79: nextx = 76;
   5E01 21 4C 00      [10]  408 	ld	hl, #0x004c
   5E04                     409 00135$:
                            410 ;src/entities/player.c:81: player->x = (u8)nextx;
   5E04 DD 75 F2      [19]  411 	ld	-14 (ix), l
   5E07 7D            [ 4]  412 	ld	a, l
   5E08 02            [ 7]  413 	ld	(bc), a
                            414 ;src/entities/player.c:83: nexty = (i16)player->y + (i16)player->vy;
   5E09 DD 6E FA      [19]  415 	ld	l,-6 (ix)
   5E0C DD 66 FB      [19]  416 	ld	h,-5 (ix)
   5E0F 5E            [ 7]  417 	ld	e, (hl)
   5E10 16 00         [ 7]  418 	ld	d, #0x00
   5E12 DD 6E F8      [19]  419 	ld	l,-8 (ix)
   5E15 DD 66 F9      [19]  420 	ld	h,-7 (ix)
   5E18 6E            [ 7]  421 	ld	l, (hl)
   5E19 7D            [ 4]  422 	ld	a, l
   5E1A 17            [ 4]  423 	rla
   5E1B 9F            [ 4]  424 	sbc	a, a
   5E1C 67            [ 4]  425 	ld	h, a
   5E1D 19            [11]  426 	add	hl, de
   5E1E E5            [11]  427 	push	hl
   5E1F FD E1         [14]  428 	pop	iy
                            429 ;src/entities/player.c:84: nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
   5E21 DD 6E FE      [19]  430 	ld	l,-2 (ix)
   5E24 DD 66 FF      [19]  431 	ld	h,-1 (ix)
   5E27 66            [ 7]  432 	ld	h, (hl)
   5E28 DD 5E F2      [19]  433 	ld	e, -14 (ix)
   5E2B 16 00         [ 7]  434 	ld	d, #0x00
   5E2D C5            [11]  435 	push	bc
   5E2E E5            [11]  436 	push	hl
   5E2F 33            [ 6]  437 	inc	sp
   5E30 FD E5         [15]  438 	push	iy
   5E32 D5            [11]  439 	push	de
   5E33 CD 7A 4D      [17]  440 	call	_collision_clamp_y_at
   5E36 F1            [10]  441 	pop	af
   5E37 F1            [10]  442 	pop	af
   5E38 33            [ 6]  443 	inc	sp
   5E39 C1            [10]  444 	pop	bc
                            445 ;src/entities/player.c:85: if (nexty < 0) {
   5E3A CB 7C         [ 8]  446 	bit	7, h
   5E3C 28 03         [12]  447 	jr	Z,00137$
                            448 ;src/entities/player.c:86: nexty = 0;
   5E3E 21 00 00      [10]  449 	ld	hl, #0x0000
   5E41                     450 00137$:
                            451 ;src/entities/player.c:88: player->y = (u8)nexty;
   5E41 5D            [ 4]  452 	ld	e, l
   5E42 DD 6E FA      [19]  453 	ld	l,-6 (ix)
   5E45 DD 66 FB      [19]  454 	ld	h,-5 (ix)
   5E48 73            [ 7]  455 	ld	(hl), e
                            456 ;src/entities/player.c:90: if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
   5E49 DD 6E FE      [19]  457 	ld	l,-2 (ix)
   5E4C DD 66 FF      [19]  458 	ld	h,-1 (ix)
   5E4F 7E            [ 7]  459 	ld	a, (hl)
   5E50 16 00         [ 7]  460 	ld	d, #0x00
   5E52 F5            [11]  461 	push	af
   5E53 0A            [ 7]  462 	ld	a, (bc)
   5E54 4F            [ 4]  463 	ld	c, a
   5E55 F1            [10]  464 	pop	af
   5E56 06 00         [ 7]  465 	ld	b, #0x00
   5E58 F5            [11]  466 	push	af
   5E59 33            [ 6]  467 	inc	sp
   5E5A D5            [11]  468 	push	de
   5E5B C5            [11]  469 	push	bc
   5E5C CD FB 4C      [17]  470 	call	_collision_is_on_ground_at
   5E5F F1            [10]  471 	pop	af
   5E60 F1            [10]  472 	pop	af
   5E61 33            [ 6]  473 	inc	sp
   5E62 7D            [ 4]  474 	ld	a, l
   5E63 B7            [ 4]  475 	or	a, a
   5E64 28 19         [12]  476 	jr	Z,00141$
   5E66 DD 6E F8      [19]  477 	ld	l,-8 (ix)
   5E69 DD 66 F9      [19]  478 	ld	h,-7 (ix)
   5E6C 4E            [ 7]  479 	ld	c, (hl)
   5E6D AF            [ 4]  480 	xor	a, a
   5E6E 91            [ 4]  481 	sub	a, c
   5E6F E2 74 5E      [10]  482 	jp	PO, 00228$
   5E72 EE 80         [ 7]  483 	xor	a, #0x80
   5E74                     484 00228$:
   5E74 F2 7F 5E      [10]  485 	jp	P, 00141$
                            486 ;src/entities/player.c:91: player->vy = 0;
   5E77 DD 6E F8      [19]  487 	ld	l,-8 (ix)
   5E7A DD 66 F9      [19]  488 	ld	h,-7 (ix)
   5E7D 36 00         [10]  489 	ld	(hl), #0x00
   5E7F                     490 00141$:
   5E7F DD F9         [10]  491 	ld	sp, ix
   5E81 DD E1         [14]  492 	pop	ix
   5E83 C9            [10]  493 	ret
                            494 ;src/entities/player.c:95: void playerrender(const Player* player) {
                            495 ;	---------------------------------
                            496 ; Function playerrender
                            497 ; ---------------------------------
   5E84                     498 _playerrender::
   5E84 DD E5         [15]  499 	push	ix
   5E86 DD 21 00 00   [14]  500 	ld	ix,#0
   5E8A DD 39         [15]  501 	add	ix,sp
   5E8C 3B            [ 6]  502 	dec	sp
                            503 ;src/entities/player.c:98: if (!player) {
   5E8D DD 7E 05      [19]  504 	ld	a, 5 (ix)
   5E90 DD B6 04      [19]  505 	or	a,4 (ix)
                            506 ;src/entities/player.c:99: return;
   5E93 28 38         [12]  507 	jr	Z,00103$
                            508 ;src/entities/player.c:102: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
   5E95 DD 5E 04      [19]  509 	ld	e,4 (ix)
   5E98 DD 56 05      [19]  510 	ld	d,5 (ix)
   5E9B 6B            [ 4]  511 	ld	l, e
   5E9C 62            [ 4]  512 	ld	h, d
   5E9D 23            [ 6]  513 	inc	hl
   5E9E 46            [ 7]  514 	ld	b, (hl)
   5E9F 1A            [ 7]  515 	ld	a, (de)
   5EA0 D5            [11]  516 	push	de
   5EA1 C5            [11]  517 	push	bc
   5EA2 33            [ 6]  518 	inc	sp
   5EA3 F5            [11]  519 	push	af
   5EA4 33            [ 6]  520 	inc	sp
   5EA5 21 00 C0      [10]  521 	ld	hl, #0xc000
   5EA8 E5            [11]  522 	push	hl
   5EA9 CD A5 63      [17]  523 	call	_cpct_getScreenPtr
   5EAC 4D            [ 4]  524 	ld	c, l
   5EAD 44            [ 4]  525 	ld	b, h
   5EAE D1            [10]  526 	pop	de
                            527 ;src/entities/player.c:103: cpct_drawSprite((u8*)sprplayerknight_data, pvmem, player->w, player->h);
   5EAF D5            [11]  528 	push	de
   5EB0 FD E1         [14]  529 	pop	iy
   5EB2 FD 7E 05      [19]  530 	ld	a, 5 (iy)
   5EB5 DD 77 FF      [19]  531 	ld	-1 (ix), a
   5EB8 EB            [ 4]  532 	ex	de,hl
   5EB9 11 04 00      [10]  533 	ld	de, #0x0004
   5EBC 19            [11]  534 	add	hl, de
   5EBD 56            [ 7]  535 	ld	d, (hl)
   5EBE DD 7E FF      [19]  536 	ld	a, -1 (ix)
   5EC1 F5            [11]  537 	push	af
   5EC2 33            [ 6]  538 	inc	sp
   5EC3 D5            [11]  539 	push	de
   5EC4 33            [ 6]  540 	inc	sp
   5EC5 C5            [11]  541 	push	bc
   5EC6 21 01 55      [10]  542 	ld	hl, #_sprplayerknight_data
   5EC9 E5            [11]  543 	push	hl
   5ECA CD D6 61      [17]  544 	call	_cpct_drawSprite
   5ECD                     545 00103$:
   5ECD 33            [ 6]  546 	inc	sp
   5ECE DD E1         [14]  547 	pop	ix
   5ED0 C9            [10]  548 	ret
                            549 ;src/entities/player.c:106: u8 player_get_ammo(const Player* player) {
                            550 ;	---------------------------------
                            551 ; Function player_get_ammo
                            552 ; ---------------------------------
   5ED1                     553 _player_get_ammo::
                            554 ;src/entities/player.c:108: return 3;
   5ED1 2E 03         [ 7]  555 	ld	l, #0x03
   5ED3 C9            [10]  556 	ret
                            557 ;src/entities/player.c:111: u8 player_get_health(const Player* player) {
                            558 ;	---------------------------------
                            559 ; Function player_get_health
                            560 ; ---------------------------------
   5ED4                     561 _player_get_health::
                            562 ;src/entities/player.c:112: return player ? player->health : 0;
   5ED4 21 03 00      [10]  563 	ld	hl, #2+1
   5ED7 39            [11]  564 	add	hl, sp
   5ED8 7E            [ 7]  565 	ld	a, (hl)
   5ED9 2B            [ 6]  566 	dec	hl
   5EDA B6            [ 7]  567 	or	a,(hl)
   5EDB 28 0A         [12]  568 	jr	Z,00103$
   5EDD C1            [10]  569 	pop	bc
   5EDE E1            [10]  570 	pop	hl
   5EDF E5            [11]  571 	push	hl
   5EE0 C5            [11]  572 	push	bc
   5EE1 11 06 00      [10]  573 	ld	de, #0x0006
   5EE4 19            [11]  574 	add	hl, de
   5EE5 6E            [ 7]  575 	ld	l, (hl)
   5EE6 C9            [10]  576 	ret
   5EE7                     577 00103$:
   5EE7 2E 00         [ 7]  578 	ld	l, #0x00
   5EE9 C9            [10]  579 	ret
                            580 ;src/entities/player.c:115: u8 player_get_weapon(const Player* player) {
                            581 ;	---------------------------------
                            582 ; Function player_get_weapon
                            583 ; ---------------------------------
   5EEA                     584 _player_get_weapon::
                            585 ;src/entities/player.c:116: return player ? player->weapon : 0;
   5EEA 21 03 00      [10]  586 	ld	hl, #2+1
   5EED 39            [11]  587 	add	hl, sp
   5EEE 7E            [ 7]  588 	ld	a, (hl)
   5EEF 2B            [ 6]  589 	dec	hl
   5EF0 B6            [ 7]  590 	or	a,(hl)
   5EF1 28 0A         [12]  591 	jr	Z,00103$
   5EF3 C1            [10]  592 	pop	bc
   5EF4 E1            [10]  593 	pop	hl
   5EF5 E5            [11]  594 	push	hl
   5EF6 C5            [11]  595 	push	bc
   5EF7 11 07 00      [10]  596 	ld	de, #0x0007
   5EFA 19            [11]  597 	add	hl, de
   5EFB 6E            [ 7]  598 	ld	l, (hl)
   5EFC C9            [10]  599 	ret
   5EFD                     600 00103$:
   5EFD 2E 00         [ 7]  601 	ld	l, #0x00
   5EFF C9            [10]  602 	ret
                            603 	.area _CODE
                            604 	.area _INITIALIZER
                            605 	.area _CABS (ABS)
