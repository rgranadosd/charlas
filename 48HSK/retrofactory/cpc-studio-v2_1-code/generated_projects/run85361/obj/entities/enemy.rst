                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module enemy
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _collision_clamp_y_at
                             12 	.globl _collision_is_on_ground_at
                             13 	.globl _cpct_getScreenPtr
                             14 	.globl _cpct_drawSolidBox
                             15 	.globl _enemyinit
                             16 	.globl _enemyspawn
                             17 	.globl _enemyupdate
                             18 	.globl _enemyrender
                             19 	.globl _enemydamage
                             20 ;--------------------------------------------------------
                             21 ; special function registers
                             22 ;--------------------------------------------------------
                             23 ;--------------------------------------------------------
                             24 ; ram data
                             25 ;--------------------------------------------------------
                             26 	.area _DATA
                             27 ;--------------------------------------------------------
                             28 ; ram data
                             29 ;--------------------------------------------------------
                             30 	.area _INITIALIZED
                             31 ;--------------------------------------------------------
                             32 ; absolute external ram data
                             33 ;--------------------------------------------------------
                             34 	.area _DABS (ABS)
                             35 ;--------------------------------------------------------
                             36 ; global & static initialisations
                             37 ;--------------------------------------------------------
                             38 	.area _HOME
                             39 	.area _GSINIT
                             40 	.area _GSFINAL
                             41 	.area _GSINIT
                             42 ;--------------------------------------------------------
                             43 ; Home
                             44 ;--------------------------------------------------------
                             45 	.area _HOME
                             46 	.area _HOME
                             47 ;--------------------------------------------------------
                             48 ; code
                             49 ;--------------------------------------------------------
                             50 	.area _CODE
                             51 ;src/entities/enemy.c:5: void enemyinit(Enemy* enemy) {
                             52 ;	---------------------------------
                             53 ; Function enemyinit
                             54 ; ---------------------------------
   502A                      55 _enemyinit::
                             56 ;src/entities/enemy.c:6: if (!enemy) {
   502A 21 03 00      [10]   57 	ld	hl, #2+1
   502D 39            [11]   58 	add	hl, sp
   502E 7E            [ 7]   59 	ld	a, (hl)
   502F 2B            [ 6]   60 	dec	hl
   5030 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:7: return;
   5031 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:10: enemy->x = 0;
   5032 D1            [10]   65 	pop	de
   5033 C1            [10]   66 	pop	bc
   5034 C5            [11]   67 	push	bc
   5035 D5            [11]   68 	push	de
   5036 AF            [ 4]   69 	xor	a, a
   5037 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:11: enemy->y = 0;
   5038 59            [ 4]   72 	ld	e, c
   5039 50            [ 4]   73 	ld	d, b
   503A 13            [ 6]   74 	inc	de
   503B AF            [ 4]   75 	xor	a, a
   503C 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:12: enemy->vx = 0;
   503D 59            [ 4]   78 	ld	e, c
   503E 50            [ 4]   79 	ld	d, b
   503F 13            [ 6]   80 	inc	de
   5040 13            [ 6]   81 	inc	de
   5041 AF            [ 4]   82 	xor	a, a
   5042 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:13: enemy->vy = 0;
   5043 59            [ 4]   85 	ld	e, c
   5044 50            [ 4]   86 	ld	d, b
   5045 13            [ 6]   87 	inc	de
   5046 13            [ 6]   88 	inc	de
   5047 13            [ 6]   89 	inc	de
   5048 AF            [ 4]   90 	xor	a, a
   5049 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:14: enemy->w = 4;
   504A 21 04 00      [10]   93 	ld	hl, #0x0004
   504D 09            [11]   94 	add	hl, bc
   504E 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:15: enemy->h = 16;
   5050 21 05 00      [10]   97 	ld	hl, #0x0005
   5053 09            [11]   98 	add	hl, bc
   5054 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:16: enemy->active = 0;
   5056 21 06 00      [10]  101 	ld	hl, #0x0006
   5059 09            [11]  102 	add	hl, bc
   505A 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:17: enemy->health = 1;
   505C 21 07 00      [10]  105 	ld	hl, #0x0007
   505F 09            [11]  106 	add	hl, bc
   5060 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:18: enemy->reward = 100;
   5062 21 08 00      [10]  109 	ld	hl, #0x0008
   5065 09            [11]  110 	add	hl, bc
   5066 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:19: enemy->kind = 0;
   5068 21 09 00      [10]  113 	ld	hl, #0x0009
   506B 09            [11]  114 	add	hl, bc
   506C 36 00         [10]  115 	ld	(hl), #0x00
   506E C9            [10]  116 	ret
                            117 ;src/entities/enemy.c:22: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            118 ;	---------------------------------
                            119 ; Function enemyspawn
                            120 ; ---------------------------------
   506F                     121 _enemyspawn::
   506F DD E5         [15]  122 	push	ix
   5071 DD 21 00 00   [14]  123 	ld	ix,#0
   5075 DD 39         [15]  124 	add	ix,sp
   5077 21 F1 FF      [10]  125 	ld	hl, #-15
   507A 39            [11]  126 	add	hl, sp
   507B F9            [ 6]  127 	ld	sp, hl
                            128 ;src/entities/enemy.c:23: if (!enemy) {
   507C DD 7E 05      [19]  129 	ld	a, 5 (ix)
   507F DD B6 04      [19]  130 	or	a,4 (ix)
                            131 ;src/entities/enemy.c:24: return;
   5082 CA F1 51      [10]  132 	jp	Z,00109$
                            133 ;src/entities/enemy.c:27: enemy->x = x;
   5085 DD 7E 04      [19]  134 	ld	a, 4 (ix)
   5088 DD 77 F5      [19]  135 	ld	-11 (ix), a
   508B DD 7E 05      [19]  136 	ld	a, 5 (ix)
   508E DD 77 F6      [19]  137 	ld	-10 (ix), a
   5091 DD 6E F5      [19]  138 	ld	l,-11 (ix)
   5094 DD 66 F6      [19]  139 	ld	h,-10 (ix)
   5097 DD 7E 06      [19]  140 	ld	a, 6 (ix)
   509A 77            [ 7]  141 	ld	(hl), a
                            142 ;src/entities/enemy.c:28: enemy->y = y;
   509B DD 4E F5      [19]  143 	ld	c,-11 (ix)
   509E DD 46 F6      [19]  144 	ld	b,-10 (ix)
   50A1 03            [ 6]  145 	inc	bc
   50A2 DD 7E 07      [19]  146 	ld	a, 7 (ix)
   50A5 02            [ 7]  147 	ld	(bc), a
                            148 ;src/entities/enemy.c:29: enemy->vx = move_right ? 1 : -1;
   50A6 DD 7E F5      [19]  149 	ld	a, -11 (ix)
   50A9 C6 02         [ 7]  150 	add	a, #0x02
   50AB DD 77 F9      [19]  151 	ld	-7 (ix), a
   50AE DD 7E F6      [19]  152 	ld	a, -10 (ix)
   50B1 CE 00         [ 7]  153 	adc	a, #0x00
   50B3 DD 77 FA      [19]  154 	ld	-6 (ix), a
   50B6 DD 7E 09      [19]  155 	ld	a, 9 (ix)
   50B9 B7            [ 4]  156 	or	a, a
   50BA 28 04         [12]  157 	jr	Z,00111$
   50BC 0E 01         [ 7]  158 	ld	c, #0x01
   50BE 18 02         [12]  159 	jr	00112$
   50C0                     160 00111$:
   50C0 0E FF         [ 7]  161 	ld	c, #0xff
   50C2                     162 00112$:
   50C2 DD 6E F9      [19]  163 	ld	l,-7 (ix)
   50C5 DD 66 FA      [19]  164 	ld	h,-6 (ix)
   50C8 71            [ 7]  165 	ld	(hl), c
                            166 ;src/entities/enemy.c:30: enemy->vy = 0;
   50C9 DD 7E F5      [19]  167 	ld	a, -11 (ix)
   50CC C6 03         [ 7]  168 	add	a, #0x03
   50CE DD 77 F7      [19]  169 	ld	-9 (ix), a
   50D1 DD 7E F6      [19]  170 	ld	a, -10 (ix)
   50D4 CE 00         [ 7]  171 	adc	a, #0x00
   50D6 DD 77 F8      [19]  172 	ld	-8 (ix), a
   50D9 DD 6E F7      [19]  173 	ld	l,-9 (ix)
   50DC DD 66 F8      [19]  174 	ld	h,-8 (ix)
   50DF 36 00         [10]  175 	ld	(hl), #0x00
                            176 ;src/entities/enemy.c:31: enemy->active = 1;
   50E1 DD 7E F5      [19]  177 	ld	a, -11 (ix)
   50E4 C6 06         [ 7]  178 	add	a, #0x06
   50E6 DD 77 F1      [19]  179 	ld	-15 (ix), a
   50E9 DD 7E F6      [19]  180 	ld	a, -10 (ix)
   50EC CE 00         [ 7]  181 	adc	a, #0x00
   50EE DD 77 F2      [19]  182 	ld	-14 (ix), a
   50F1 E1            [10]  183 	pop	hl
   50F2 E5            [11]  184 	push	hl
   50F3 36 01         [10]  185 	ld	(hl), #0x01
                            186 ;src/entities/enemy.c:32: enemy->kind = kind;
   50F5 DD 7E F5      [19]  187 	ld	a, -11 (ix)
   50F8 C6 09         [ 7]  188 	add	a, #0x09
   50FA DD 77 F1      [19]  189 	ld	-15 (ix), a
   50FD DD 7E F6      [19]  190 	ld	a, -10 (ix)
   5100 CE 00         [ 7]  191 	adc	a, #0x00
   5102 DD 77 F2      [19]  192 	ld	-14 (ix), a
   5105 E1            [10]  193 	pop	hl
   5106 E5            [11]  194 	push	hl
   5107 DD 7E 08      [19]  195 	ld	a, 8 (ix)
   510A 77            [ 7]  196 	ld	(hl), a
                            197 ;src/entities/enemy.c:35: enemy->w = 5;
   510B DD 7E F5      [19]  198 	ld	a, -11 (ix)
   510E C6 04         [ 7]  199 	add	a, #0x04
   5110 DD 77 F1      [19]  200 	ld	-15 (ix), a
   5113 DD 7E F6      [19]  201 	ld	a, -10 (ix)
   5116 CE 00         [ 7]  202 	adc	a, #0x00
   5118 DD 77 F2      [19]  203 	ld	-14 (ix), a
                            204 ;src/entities/enemy.c:36: enemy->h = 14;
   511B DD 7E F5      [19]  205 	ld	a, -11 (ix)
   511E C6 05         [ 7]  206 	add	a, #0x05
   5120 DD 77 FB      [19]  207 	ld	-5 (ix), a
   5123 DD 7E F6      [19]  208 	ld	a, -10 (ix)
   5126 CE 00         [ 7]  209 	adc	a, #0x00
   5128 DD 77 FC      [19]  210 	ld	-4 (ix), a
                            211 ;src/entities/enemy.c:37: enemy->health = 2;
   512B DD 7E F5      [19]  212 	ld	a, -11 (ix)
   512E C6 07         [ 7]  213 	add	a, #0x07
   5130 DD 77 F3      [19]  214 	ld	-13 (ix), a
   5133 DD 7E F6      [19]  215 	ld	a, -10 (ix)
   5136 CE 00         [ 7]  216 	adc	a, #0x00
   5138 DD 77 F4      [19]  217 	ld	-12 (ix), a
                            218 ;src/entities/enemy.c:38: enemy->reward = 180;
   513B DD 7E F5      [19]  219 	ld	a, -11 (ix)
   513E C6 08         [ 7]  220 	add	a, #0x08
   5140 DD 77 F5      [19]  221 	ld	-11 (ix), a
   5143 DD 7E F6      [19]  222 	ld	a, -10 (ix)
   5146 CE 00         [ 7]  223 	adc	a, #0x00
   5148 DD 77 F6      [19]  224 	ld	-10 (ix), a
                            225 ;src/entities/enemy.c:34: if (kind == 1) {
   514B DD 7E 08      [19]  226 	ld	a, 8 (ix)
   514E 3D            [ 4]  227 	dec	a
   514F 20 44         [12]  228 	jr	NZ,00107$
                            229 ;src/entities/enemy.c:35: enemy->w = 5;
   5151 E1            [10]  230 	pop	hl
   5152 E5            [11]  231 	push	hl
   5153 36 05         [10]  232 	ld	(hl), #0x05
                            233 ;src/entities/enemy.c:36: enemy->h = 14;
   5155 DD 6E FB      [19]  234 	ld	l,-5 (ix)
   5158 DD 66 FC      [19]  235 	ld	h,-4 (ix)
   515B 36 0E         [10]  236 	ld	(hl), #0x0e
                            237 ;src/entities/enemy.c:37: enemy->health = 2;
   515D DD 6E F3      [19]  238 	ld	l,-13 (ix)
   5160 DD 66 F4      [19]  239 	ld	h,-12 (ix)
   5163 36 02         [10]  240 	ld	(hl), #0x02
                            241 ;src/entities/enemy.c:38: enemy->reward = 180;
   5165 DD 6E F5      [19]  242 	ld	l,-11 (ix)
   5168 DD 66 F6      [19]  243 	ld	h,-10 (ix)
   516B 36 B4         [10]  244 	ld	(hl), #0xb4
                            245 ;src/entities/enemy.c:39: enemy->vx = move_right ? 2 : -2;
   516D DD 7E F9      [19]  246 	ld	a, -7 (ix)
   5170 DD 77 FE      [19]  247 	ld	-2 (ix), a
   5173 DD 7E FA      [19]  248 	ld	a, -6 (ix)
   5176 DD 77 FF      [19]  249 	ld	-1 (ix), a
   5179 DD 7E 09      [19]  250 	ld	a, 9 (ix)
   517C B7            [ 4]  251 	or	a, a
   517D 28 06         [12]  252 	jr	Z,00113$
   517F DD 36 FD 02   [19]  253 	ld	-3 (ix), #0x02
   5183 18 04         [12]  254 	jr	00114$
   5185                     255 00113$:
   5185 DD 36 FD FE   [19]  256 	ld	-3 (ix), #0xfe
   5189                     257 00114$:
   5189 DD 6E FE      [19]  258 	ld	l,-2 (ix)
   518C DD 66 FF      [19]  259 	ld	h,-1 (ix)
   518F DD 7E FD      [19]  260 	ld	a, -3 (ix)
   5192 77            [ 7]  261 	ld	(hl), a
   5193 18 5C         [12]  262 	jr	00109$
   5195                     263 00107$:
                            264 ;src/entities/enemy.c:40: } else if (kind == 2) {
   5195 DD 7E 08      [19]  265 	ld	a, 8 (ix)
   5198 D6 02         [ 7]  266 	sub	a, #0x02
   519A 20 39         [12]  267 	jr	NZ,00104$
                            268 ;src/entities/enemy.c:41: enemy->w = 6;
   519C E1            [10]  269 	pop	hl
   519D E5            [11]  270 	push	hl
   519E 36 06         [10]  271 	ld	(hl), #0x06
                            272 ;src/entities/enemy.c:42: enemy->h = 10;
   51A0 DD 6E FB      [19]  273 	ld	l,-5 (ix)
   51A3 DD 66 FC      [19]  274 	ld	h,-4 (ix)
   51A6 36 0A         [10]  275 	ld	(hl), #0x0a
                            276 ;src/entities/enemy.c:43: enemy->health = 1;
   51A8 DD 6E F3      [19]  277 	ld	l,-13 (ix)
   51AB DD 66 F4      [19]  278 	ld	h,-12 (ix)
   51AE 36 01         [10]  279 	ld	(hl), #0x01
                            280 ;src/entities/enemy.c:44: enemy->reward = 150;
   51B0 DD 6E F5      [19]  281 	ld	l,-11 (ix)
   51B3 DD 66 F6      [19]  282 	ld	h,-10 (ix)
   51B6 36 96         [10]  283 	ld	(hl), #0x96
                            284 ;src/entities/enemy.c:45: enemy->vy = move_right ? 1 : -1;
   51B8 DD 4E F7      [19]  285 	ld	c,-9 (ix)
   51BB DD 46 F8      [19]  286 	ld	b,-8 (ix)
   51BE DD 7E 09      [19]  287 	ld	a, 9 (ix)
   51C1 B7            [ 4]  288 	or	a, a
   51C2 28 04         [12]  289 	jr	Z,00115$
   51C4 3E 01         [ 7]  290 	ld	a, #0x01
   51C6 18 02         [12]  291 	jr	00116$
   51C8                     292 00115$:
   51C8 3E FF         [ 7]  293 	ld	a, #0xff
   51CA                     294 00116$:
   51CA 02            [ 7]  295 	ld	(bc), a
                            296 ;src/entities/enemy.c:46: enemy->vx = 1;
   51CB DD 6E F9      [19]  297 	ld	l,-7 (ix)
   51CE DD 66 FA      [19]  298 	ld	h,-6 (ix)
   51D1 36 01         [10]  299 	ld	(hl), #0x01
   51D3 18 1C         [12]  300 	jr	00109$
   51D5                     301 00104$:
                            302 ;src/entities/enemy.c:48: enemy->w = 4;
   51D5 E1            [10]  303 	pop	hl
   51D6 E5            [11]  304 	push	hl
   51D7 36 04         [10]  305 	ld	(hl), #0x04
                            306 ;src/entities/enemy.c:49: enemy->h = 16;
   51D9 DD 6E FB      [19]  307 	ld	l,-5 (ix)
   51DC DD 66 FC      [19]  308 	ld	h,-4 (ix)
   51DF 36 10         [10]  309 	ld	(hl), #0x10
                            310 ;src/entities/enemy.c:50: enemy->health = 1;
   51E1 DD 6E F3      [19]  311 	ld	l,-13 (ix)
   51E4 DD 66 F4      [19]  312 	ld	h,-12 (ix)
   51E7 36 01         [10]  313 	ld	(hl), #0x01
                            314 ;src/entities/enemy.c:51: enemy->reward = 100;
   51E9 DD 6E F5      [19]  315 	ld	l,-11 (ix)
   51EC DD 66 F6      [19]  316 	ld	h,-10 (ix)
   51EF 36 64         [10]  317 	ld	(hl), #0x64
   51F1                     318 00109$:
   51F1 DD F9         [10]  319 	ld	sp, ix
   51F3 DD E1         [14]  320 	pop	ix
   51F5 C9            [10]  321 	ret
                            322 ;src/entities/enemy.c:55: void enemyupdate(Enemy* enemy) {
                            323 ;	---------------------------------
                            324 ; Function enemyupdate
                            325 ; ---------------------------------
   51F6                     326 _enemyupdate::
   51F6 DD E5         [15]  327 	push	ix
   51F8 DD 21 00 00   [14]  328 	ld	ix,#0
   51FC DD 39         [15]  329 	add	ix,sp
   51FE 21 F6 FF      [10]  330 	ld	hl, #-10
   5201 39            [11]  331 	add	hl, sp
   5202 F9            [ 6]  332 	ld	sp, hl
                            333 ;src/entities/enemy.c:59: if (!enemy || !enemy->active) {
   5203 DD 7E 05      [19]  334 	ld	a, 5 (ix)
   5206 DD B6 04      [19]  335 	or	a,4 (ix)
   5209 CA EC 53      [10]  336 	jp	Z,00121$
   520C DD 7E 04      [19]  337 	ld	a, 4 (ix)
   520F DD 77 FE      [19]  338 	ld	-2 (ix), a
   5212 DD 7E 05      [19]  339 	ld	a, 5 (ix)
   5215 DD 77 FF      [19]  340 	ld	-1 (ix), a
   5218 DD 6E FE      [19]  341 	ld	l,-2 (ix)
   521B DD 66 FF      [19]  342 	ld	h,-1 (ix)
   521E 11 06 00      [10]  343 	ld	de, #0x0006
   5221 19            [11]  344 	add	hl, de
   5222 7E            [ 7]  345 	ld	a, (hl)
   5223 B7            [ 4]  346 	or	a, a
                            347 ;src/entities/enemy.c:60: return;
   5224 CA EC 53      [10]  348 	jp	Z,00121$
                            349 ;src/entities/enemy.c:63: if (enemy->kind == 2) {
   5227 DD 6E FE      [19]  350 	ld	l,-2 (ix)
   522A DD 66 FF      [19]  351 	ld	h,-1 (ix)
   522D 11 09 00      [10]  352 	ld	de, #0x0009
   5230 19            [11]  353 	add	hl, de
   5231 7E            [ 7]  354 	ld	a, (hl)
   5232 DD 77 FB      [19]  355 	ld	-5 (ix), a
                            356 ;src/entities/enemy.c:64: nextx = (i16)enemy->x + (i16)enemy->vx;
   5235 DD 6E FE      [19]  357 	ld	l,-2 (ix)
   5238 DD 66 FF      [19]  358 	ld	h,-1 (ix)
   523B 4E            [ 7]  359 	ld	c, (hl)
   523C DD 7E FE      [19]  360 	ld	a, -2 (ix)
   523F C6 02         [ 7]  361 	add	a, #0x02
   5241 DD 77 FC      [19]  362 	ld	-4 (ix), a
   5244 DD 7E FF      [19]  363 	ld	a, -1 (ix)
   5247 CE 00         [ 7]  364 	adc	a, #0x00
   5249 DD 77 FD      [19]  365 	ld	-3 (ix), a
                            366 ;src/entities/enemy.c:65: nexty = (i16)enemy->y + (i16)enemy->vy;
   524C DD 7E FE      [19]  367 	ld	a, -2 (ix)
   524F C6 01         [ 7]  368 	add	a, #0x01
   5251 DD 77 F9      [19]  369 	ld	-7 (ix), a
   5254 DD 7E FF      [19]  370 	ld	a, -1 (ix)
   5257 CE 00         [ 7]  371 	adc	a, #0x00
   5259 DD 77 FA      [19]  372 	ld	-6 (ix), a
   525C DD 5E FE      [19]  373 	ld	e,-2 (ix)
   525F DD 56 FF      [19]  374 	ld	d,-1 (ix)
   5262 13            [ 6]  375 	inc	de
   5263 13            [ 6]  376 	inc	de
   5264 13            [ 6]  377 	inc	de
                            378 ;src/entities/enemy.c:64: nextx = (i16)enemy->x + (i16)enemy->vx;
   5265 06 00         [ 7]  379 	ld	b, #0x00
   5267 DD 6E FC      [19]  380 	ld	l,-4 (ix)
   526A DD 66 FD      [19]  381 	ld	h,-3 (ix)
   526D 7E            [ 7]  382 	ld	a, (hl)
   526E DD 77 F8      [19]  383 	ld	-8 (ix), a
   5271 6F            [ 4]  384 	ld	l, a
   5272 DD 7E F8      [19]  385 	ld	a, -8 (ix)
   5275 17            [ 4]  386 	rla
   5276 9F            [ 4]  387 	sbc	a, a
   5277 67            [ 4]  388 	ld	h, a
   5278 09            [11]  389 	add	hl,bc
   5279 4D            [ 4]  390 	ld	c, l
   527A 44            [ 4]  391 	ld	b, h
                            392 ;src/entities/enemy.c:63: if (enemy->kind == 2) {
   527B DD 7E FB      [19]  393 	ld	a, -5 (ix)
   527E D6 02         [ 7]  394 	sub	a, #0x02
   5280 C2 29 53      [10]  395 	jp	NZ,00111$
                            396 ;src/entities/enemy.c:64: nextx = (i16)enemy->x + (i16)enemy->vx;
                            397 ;src/entities/enemy.c:65: nexty = (i16)enemy->y + (i16)enemy->vy;
   5283 DD 6E F9      [19]  398 	ld	l,-7 (ix)
   5286 DD 66 FA      [19]  399 	ld	h,-6 (ix)
   5289 6E            [ 7]  400 	ld	l, (hl)
   528A DD 75 F6      [19]  401 	ld	-10 (ix), l
   528D DD 36 F7 00   [19]  402 	ld	-9 (ix), #0x00
   5291 1A            [ 7]  403 	ld	a, (de)
   5292 6F            [ 4]  404 	ld	l, a
   5293 17            [ 4]  405 	rla
   5294 9F            [ 4]  406 	sbc	a, a
   5295 67            [ 4]  407 	ld	h, a
   5296 DD 7E F6      [19]  408 	ld	a, -10 (ix)
   5299 85            [ 4]  409 	add	a, l
   529A DD 77 F6      [19]  410 	ld	-10 (ix), a
   529D DD 7E F7      [19]  411 	ld	a, -9 (ix)
   52A0 8C            [ 4]  412 	adc	a, h
   52A1 DD 77 F7      [19]  413 	ld	-9 (ix), a
                            414 ;src/entities/enemy.c:67: if (nextx < 8 || nextx > 72) {
   52A4 79            [ 4]  415 	ld	a, c
   52A5 D6 08         [ 7]  416 	sub	a, #0x08
   52A7 78            [ 4]  417 	ld	a, b
   52A8 17            [ 4]  418 	rla
   52A9 3F            [ 4]  419 	ccf
   52AA 1F            [ 4]  420 	rra
   52AB DE 80         [ 7]  421 	sbc	a, #0x80
   52AD 38 0E         [12]  422 	jr	C,00104$
   52AF 3E 48         [ 7]  423 	ld	a, #0x48
   52B1 B9            [ 4]  424 	cp	a, c
   52B2 3E 00         [ 7]  425 	ld	a, #0x00
   52B4 98            [ 4]  426 	sbc	a, b
   52B5 E2 BA 52      [10]  427 	jp	PO, 00161$
   52B8 EE 80         [ 7]  428 	xor	a, #0x80
   52BA                     429 00161$:
   52BA F2 D8 52      [10]  430 	jp	P, 00105$
   52BD                     431 00104$:
                            432 ;src/entities/enemy.c:68: enemy->vx = (i8)(-enemy->vx);
   52BD AF            [ 4]  433 	xor	a, a
   52BE DD 96 F8      [19]  434 	sub	a, -8 (ix)
   52C1 4F            [ 4]  435 	ld	c, a
   52C2 DD 6E FC      [19]  436 	ld	l,-4 (ix)
   52C5 DD 66 FD      [19]  437 	ld	h,-3 (ix)
   52C8 71            [ 7]  438 	ld	(hl), c
                            439 ;src/entities/enemy.c:69: nextx = (i16)enemy->x + (i16)enemy->vx;
   52C9 DD 6E FE      [19]  440 	ld	l,-2 (ix)
   52CC DD 66 FF      [19]  441 	ld	h,-1 (ix)
   52CF 6E            [ 7]  442 	ld	l, (hl)
   52D0 26 00         [ 7]  443 	ld	h, #0x00
   52D2 79            [ 4]  444 	ld	a, c
   52D3 17            [ 4]  445 	rla
   52D4 9F            [ 4]  446 	sbc	a, a
   52D5 47            [ 4]  447 	ld	b, a
   52D6 09            [11]  448 	add	hl,bc
   52D7 4D            [ 4]  449 	ld	c, l
   52D8                     450 00105$:
                            451 ;src/entities/enemy.c:71: if (nexty < 56 || nexty > 120) {
   52D8 DD 7E F6      [19]  452 	ld	a, -10 (ix)
   52DB D6 38         [ 7]  453 	sub	a, #0x38
   52DD DD 7E F7      [19]  454 	ld	a, -9 (ix)
   52E0 17            [ 4]  455 	rla
   52E1 3F            [ 4]  456 	ccf
   52E2 1F            [ 4]  457 	rra
   52E3 DE 80         [ 7]  458 	sbc	a, #0x80
   52E5 38 12         [12]  459 	jr	C,00107$
   52E7 3E 78         [ 7]  460 	ld	a, #0x78
   52E9 DD BE F6      [19]  461 	cp	a, -10 (ix)
   52EC 3E 00         [ 7]  462 	ld	a, #0x00
   52EE DD 9E F7      [19]  463 	sbc	a, -9 (ix)
   52F1 E2 F6 52      [10]  464 	jp	PO, 00162$
   52F4 EE 80         [ 7]  465 	xor	a, #0x80
   52F6                     466 00162$:
   52F6 F2 15 53      [10]  467 	jp	P, 00108$
   52F9                     468 00107$:
                            469 ;src/entities/enemy.c:72: enemy->vy = (i8)(-enemy->vy);
   52F9 1A            [ 7]  470 	ld	a, (de)
   52FA 6F            [ 4]  471 	ld	l, a
   52FB AF            [ 4]  472 	xor	a, a
   52FC 95            [ 4]  473 	sub	a, l
   52FD DD 77 F8      [19]  474 	ld	-8 (ix), a
   5300 12            [ 7]  475 	ld	(de),a
                            476 ;src/entities/enemy.c:73: nexty = (i16)enemy->y + (i16)enemy->vy;
   5301 DD 6E F9      [19]  477 	ld	l,-7 (ix)
   5304 DD 66 FA      [19]  478 	ld	h,-6 (ix)
   5307 5E            [ 7]  479 	ld	e, (hl)
   5308 16 00         [ 7]  480 	ld	d, #0x00
   530A DD 6E F8      [19]  481 	ld	l, -8 (ix)
   530D DD 7E F8      [19]  482 	ld	a, -8 (ix)
   5310 17            [ 4]  483 	rla
   5311 9F            [ 4]  484 	sbc	a, a
   5312 67            [ 4]  485 	ld	h, a
   5313 19            [11]  486 	add	hl,de
   5314 E3            [19]  487 	ex	(sp), hl
   5315                     488 00108$:
                            489 ;src/entities/enemy.c:76: enemy->x = (u8)nextx;
   5315 DD 6E FE      [19]  490 	ld	l,-2 (ix)
   5318 DD 66 FF      [19]  491 	ld	h,-1 (ix)
   531B 71            [ 7]  492 	ld	(hl), c
                            493 ;src/entities/enemy.c:77: enemy->y = (u8)nexty;
   531C DD 4E F6      [19]  494 	ld	c, -10 (ix)
   531F DD 6E F9      [19]  495 	ld	l,-7 (ix)
   5322 DD 66 FA      [19]  496 	ld	h,-6 (ix)
   5325 71            [ 7]  497 	ld	(hl), c
                            498 ;src/entities/enemy.c:78: return;
   5326 C3 EC 53      [10]  499 	jp	00121$
   5329                     500 00111$:
                            501 ;src/entities/enemy.c:81: nextx = (i16)enemy->x + (i16)enemy->vx;
                            502 ;src/entities/enemy.c:82: if (nextx < 2) {
   5329 79            [ 4]  503 	ld	a, c
   532A D6 02         [ 7]  504 	sub	a, #0x02
   532C 78            [ 4]  505 	ld	a, b
   532D 17            [ 4]  506 	rla
   532E 3F            [ 4]  507 	ccf
   532F 1F            [ 4]  508 	rra
   5330 DE 80         [ 7]  509 	sbc	a, #0x80
   5332 30 0B         [12]  510 	jr	NC,00113$
                            511 ;src/entities/enemy.c:83: nextx = 2;
   5334 01 02 00      [10]  512 	ld	bc, #0x0002
                            513 ;src/entities/enemy.c:84: enemy->vx = 1;
   5337 DD 6E FC      [19]  514 	ld	l,-4 (ix)
   533A DD 66 FD      [19]  515 	ld	h,-3 (ix)
   533D 36 01         [10]  516 	ld	(hl), #0x01
   533F                     517 00113$:
                            518 ;src/entities/enemy.c:86: if (nextx > 74) {
   533F 3E 4A         [ 7]  519 	ld	a, #0x4a
   5341 B9            [ 4]  520 	cp	a, c
   5342 3E 00         [ 7]  521 	ld	a, #0x00
   5344 98            [ 4]  522 	sbc	a, b
   5345 E2 4A 53      [10]  523 	jp	PO, 00163$
   5348 EE 80         [ 7]  524 	xor	a, #0x80
   534A                     525 00163$:
   534A F2 58 53      [10]  526 	jp	P, 00115$
                            527 ;src/entities/enemy.c:87: nextx = 74;
   534D 01 4A 00      [10]  528 	ld	bc, #0x004a
                            529 ;src/entities/enemy.c:88: enemy->vx = -1;
   5350 DD 6E FC      [19]  530 	ld	l,-4 (ix)
   5353 DD 66 FD      [19]  531 	ld	h,-3 (ix)
   5356 36 FF         [10]  532 	ld	(hl), #0xff
   5358                     533 00115$:
                            534 ;src/entities/enemy.c:90: enemy->x = (u8)nextx;
   5358 DD 6E FE      [19]  535 	ld	l,-2 (ix)
   535B DD 66 FF      [19]  536 	ld	h,-1 (ix)
   535E 71            [ 7]  537 	ld	(hl), c
                            538 ;src/entities/enemy.c:92: enemy->vy = (i8)(enemy->vy + 1);
   535F 1A            [ 7]  539 	ld	a, (de)
   5360 4F            [ 4]  540 	ld	c, a
   5361 0C            [ 4]  541 	inc	c
   5362 79            [ 4]  542 	ld	a, c
   5363 12            [ 7]  543 	ld	(de), a
                            544 ;src/entities/enemy.c:93: if (enemy->vy > 3) enemy->vy = 3;
   5364 3E 03         [ 7]  545 	ld	a, #0x03
   5366 91            [ 4]  546 	sub	a, c
   5367 E2 6C 53      [10]  547 	jp	PO, 00164$
   536A EE 80         [ 7]  548 	xor	a, #0x80
   536C                     549 00164$:
   536C F2 72 53      [10]  550 	jp	P, 00117$
   536F 3E 03         [ 7]  551 	ld	a, #0x03
   5371 12            [ 7]  552 	ld	(de), a
   5372                     553 00117$:
                            554 ;src/entities/enemy.c:94: nexty = (i16)enemy->y + (i16)enemy->vy;
   5372 DD 6E F9      [19]  555 	ld	l,-7 (ix)
   5375 DD 66 FA      [19]  556 	ld	h,-6 (ix)
   5378 4E            [ 7]  557 	ld	c, (hl)
   5379 06 00         [ 7]  558 	ld	b, #0x00
   537B 1A            [ 7]  559 	ld	a, (de)
   537C 6F            [ 4]  560 	ld	l, a
   537D 17            [ 4]  561 	rla
   537E 9F            [ 4]  562 	sbc	a, a
   537F 67            [ 4]  563 	ld	h, a
   5380 09            [11]  564 	add	hl, bc
   5381 E5            [11]  565 	push	hl
   5382 FD E1         [14]  566 	pop	iy
                            567 ;src/entities/enemy.c:95: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5384 DD 7E FE      [19]  568 	ld	a, -2 (ix)
   5387 C6 05         [ 7]  569 	add	a, #0x05
   5389 DD 77 F6      [19]  570 	ld	-10 (ix), a
   538C DD 7E FF      [19]  571 	ld	a, -1 (ix)
   538F CE 00         [ 7]  572 	adc	a, #0x00
   5391 DD 77 F7      [19]  573 	ld	-9 (ix), a
   5394 E1            [10]  574 	pop	hl
   5395 E5            [11]  575 	push	hl
   5396 7E            [ 7]  576 	ld	a, (hl)
   5397 DD 6E FE      [19]  577 	ld	l,-2 (ix)
   539A DD 66 FF      [19]  578 	ld	h,-1 (ix)
   539D 4E            [ 7]  579 	ld	c, (hl)
   539E 06 00         [ 7]  580 	ld	b, #0x00
   53A0 D5            [11]  581 	push	de
   53A1 F5            [11]  582 	push	af
   53A2 33            [ 6]  583 	inc	sp
   53A3 FD E5         [15]  584 	push	iy
   53A5 C5            [11]  585 	push	bc
   53A6 CD 97 4A      [17]  586 	call	_collision_clamp_y_at
   53A9 F1            [10]  587 	pop	af
   53AA F1            [10]  588 	pop	af
   53AB 33            [ 6]  589 	inc	sp
   53AC 4D            [ 4]  590 	ld	c, l
   53AD D1            [10]  591 	pop	de
                            592 ;src/entities/enemy.c:96: enemy->y = (u8)nexty;
   53AE DD 6E F9      [19]  593 	ld	l,-7 (ix)
   53B1 DD 66 FA      [19]  594 	ld	h,-6 (ix)
   53B4 71            [ 7]  595 	ld	(hl), c
                            596 ;src/entities/enemy.c:97: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   53B5 E1            [10]  597 	pop	hl
   53B6 E5            [11]  598 	push	hl
   53B7 7E            [ 7]  599 	ld	a, (hl)
   53B8 06 00         [ 7]  600 	ld	b, #0x00
   53BA DD 6E FE      [19]  601 	ld	l,-2 (ix)
   53BD DD 66 FF      [19]  602 	ld	h,-1 (ix)
   53C0 6E            [ 7]  603 	ld	l, (hl)
   53C1 DD 75 F6      [19]  604 	ld	-10 (ix), l
   53C4 DD 36 F7 00   [19]  605 	ld	-9 (ix), #0x00
   53C8 D5            [11]  606 	push	de
   53C9 F5            [11]  607 	push	af
   53CA 33            [ 6]  608 	inc	sp
   53CB C5            [11]  609 	push	bc
   53CC DD 6E F6      [19]  610 	ld	l,-10 (ix)
   53CF DD 66 F7      [19]  611 	ld	h,-9 (ix)
   53D2 E5            [11]  612 	push	hl
   53D3 CD 18 4A      [17]  613 	call	_collision_is_on_ground_at
   53D6 F1            [10]  614 	pop	af
   53D7 F1            [10]  615 	pop	af
   53D8 33            [ 6]  616 	inc	sp
   53D9 D1            [10]  617 	pop	de
   53DA 7D            [ 4]  618 	ld	a, l
   53DB B7            [ 4]  619 	or	a, a
   53DC 28 0E         [12]  620 	jr	Z,00121$
   53DE 1A            [ 7]  621 	ld	a, (de)
   53DF 4F            [ 4]  622 	ld	c, a
   53E0 AF            [ 4]  623 	xor	a, a
   53E1 91            [ 4]  624 	sub	a, c
   53E2 E2 E7 53      [10]  625 	jp	PO, 00165$
   53E5 EE 80         [ 7]  626 	xor	a, #0x80
   53E7                     627 00165$:
   53E7 F2 EC 53      [10]  628 	jp	P, 00121$
                            629 ;src/entities/enemy.c:98: enemy->vy = 0;
   53EA AF            [ 4]  630 	xor	a, a
   53EB 12            [ 7]  631 	ld	(de), a
   53EC                     632 00121$:
   53EC DD F9         [10]  633 	ld	sp, ix
   53EE DD E1         [14]  634 	pop	ix
   53F0 C9            [10]  635 	ret
                            636 ;src/entities/enemy.c:102: void enemyrender(const Enemy* enemy) {
                            637 ;	---------------------------------
                            638 ; Function enemyrender
                            639 ; ---------------------------------
   53F1                     640 _enemyrender::
   53F1 DD E5         [15]  641 	push	ix
   53F3 DD 21 00 00   [14]  642 	ld	ix,#0
   53F7 DD 39         [15]  643 	add	ix,sp
                            644 ;src/entities/enemy.c:105: if (!enemy || !enemy->active) {
   53F9 DD 7E 05      [19]  645 	ld	a, 5 (ix)
   53FC DD B6 04      [19]  646 	or	a,4 (ix)
   53FF 28 3C         [12]  647 	jr	Z,00104$
   5401 DD 4E 04      [19]  648 	ld	c,4 (ix)
   5404 DD 46 05      [19]  649 	ld	b,5 (ix)
   5407 C5            [11]  650 	push	bc
   5408 FD E1         [14]  651 	pop	iy
   540A FD 7E 06      [19]  652 	ld	a, 6 (iy)
   540D B7            [ 4]  653 	or	a, a
                            654 ;src/entities/enemy.c:106: return;
   540E 28 2D         [12]  655 	jr	Z,00104$
                            656 ;src/entities/enemy.c:109: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5410 69            [ 4]  657 	ld	l, c
   5411 60            [ 4]  658 	ld	h, b
   5412 23            [ 6]  659 	inc	hl
   5413 56            [ 7]  660 	ld	d, (hl)
   5414 0A            [ 7]  661 	ld	a, (bc)
   5415 C5            [11]  662 	push	bc
   5416 5F            [ 4]  663 	ld	e, a
   5417 D5            [11]  664 	push	de
   5418 21 00 C0      [10]  665 	ld	hl, #0xc000
   541B E5            [11]  666 	push	hl
   541C CD B3 5C      [17]  667 	call	_cpct_getScreenPtr
   541F EB            [ 4]  668 	ex	de,hl
   5420 C1            [10]  669 	pop	bc
                            670 ;src/entities/enemy.c:110: cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
   5421 C5            [11]  671 	push	bc
   5422 FD E1         [14]  672 	pop	iy
   5424 FD 7E 05      [19]  673 	ld	a, 5 (iy)
   5427 69            [ 4]  674 	ld	l, c
   5428 60            [ 4]  675 	ld	h, b
   5429 01 04 00      [10]  676 	ld	bc, #0x0004
   542C 09            [11]  677 	add	hl, bc
   542D 46            [ 7]  678 	ld	b, (hl)
   542E F5            [11]  679 	push	af
   542F 33            [ 6]  680 	inc	sp
   5430 C5            [11]  681 	push	bc
   5431 33            [ 6]  682 	inc	sp
   5432 3E 5C         [ 7]  683 	ld	a, #0x5c
   5434 F5            [11]  684 	push	af
   5435 33            [ 6]  685 	inc	sp
   5436 D5            [11]  686 	push	de
   5437 CD FA 5B      [17]  687 	call	_cpct_drawSolidBox
   543A F1            [10]  688 	pop	af
   543B F1            [10]  689 	pop	af
   543C 33            [ 6]  690 	inc	sp
   543D                     691 00104$:
   543D DD E1         [14]  692 	pop	ix
   543F C9            [10]  693 	ret
                            694 ;src/entities/enemy.c:113: u8 enemydamage(Enemy* enemy, u8 damage) {
                            695 ;	---------------------------------
                            696 ; Function enemydamage
                            697 ; ---------------------------------
   5440                     698 _enemydamage::
   5440 DD E5         [15]  699 	push	ix
   5442 DD 21 00 00   [14]  700 	ld	ix,#0
   5446 DD 39         [15]  701 	add	ix,sp
                            702 ;src/entities/enemy.c:114: if (!enemy || !enemy->active) {
   5448 DD 7E 05      [19]  703 	ld	a, 5 (ix)
   544B DD B6 04      [19]  704 	or	a,4 (ix)
   544E 28 0F         [12]  705 	jr	Z,00101$
   5450 DD 4E 04      [19]  706 	ld	c,4 (ix)
   5453 DD 46 05      [19]  707 	ld	b,5 (ix)
   5456 21 06 00      [10]  708 	ld	hl, #0x0006
   5459 09            [11]  709 	add	hl,bc
   545A EB            [ 4]  710 	ex	de,hl
   545B 1A            [ 7]  711 	ld	a, (de)
   545C B7            [ 4]  712 	or	a, a
   545D 20 04         [12]  713 	jr	NZ,00102$
   545F                     714 00101$:
                            715 ;src/entities/enemy.c:115: return 0;
   545F 2E 00         [ 7]  716 	ld	l, #0x00
   5461 18 1A         [12]  717 	jr	00106$
   5463                     718 00102$:
                            719 ;src/entities/enemy.c:118: if (damage >= enemy->health) {
   5463 21 07 00      [10]  720 	ld	hl, #0x0007
   5466 09            [11]  721 	add	hl, bc
   5467 4E            [ 7]  722 	ld	c, (hl)
   5468 DD 7E 06      [19]  723 	ld	a, 6 (ix)
   546B 91            [ 4]  724 	sub	a, c
   546C 38 08         [12]  725 	jr	C,00105$
                            726 ;src/entities/enemy.c:119: enemy->health = 0;
   546E 36 00         [10]  727 	ld	(hl), #0x00
                            728 ;src/entities/enemy.c:120: enemy->active = 0;
   5470 AF            [ 4]  729 	xor	a, a
   5471 12            [ 7]  730 	ld	(de), a
                            731 ;src/entities/enemy.c:121: return 1;
   5472 2E 01         [ 7]  732 	ld	l, #0x01
   5474 18 07         [12]  733 	jr	00106$
   5476                     734 00105$:
                            735 ;src/entities/enemy.c:124: enemy->health = (u8)(enemy->health - damage);
   5476 79            [ 4]  736 	ld	a, c
   5477 DD 96 06      [19]  737 	sub	a, 6 (ix)
   547A 77            [ 7]  738 	ld	(hl), a
                            739 ;src/entities/enemy.c:125: return 0;
   547B 2E 00         [ 7]  740 	ld	l, #0x00
   547D                     741 00106$:
   547D DD E1         [14]  742 	pop	ix
   547F C9            [10]  743 	ret
                            744 	.area _CODE
                            745 	.area _INITIALIZER
                            746 	.area _CABS (ABS)
