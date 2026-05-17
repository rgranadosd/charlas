                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module projectile
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSprite
                             13 	.globl _projectileinit
                             14 	.globl _projectilefire
                             15 	.globl _projectileupdate
                             16 	.globl _projectilerender
                             17 ;--------------------------------------------------------
                             18 ; special function registers
                             19 ;--------------------------------------------------------
                             20 ;--------------------------------------------------------
                             21 ; ram data
                             22 ;--------------------------------------------------------
                             23 	.area _DATA
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _INITIALIZED
                             28 ;--------------------------------------------------------
                             29 ; absolute external ram data
                             30 ;--------------------------------------------------------
                             31 	.area _DABS (ABS)
                             32 ;--------------------------------------------------------
                             33 ; global & static initialisations
                             34 ;--------------------------------------------------------
                             35 	.area _HOME
                             36 	.area _GSINIT
                             37 	.area _GSFINAL
                             38 	.area _GSINIT
                             39 ;--------------------------------------------------------
                             40 ; Home
                             41 ;--------------------------------------------------------
                             42 	.area _HOME
                             43 	.area _HOME
                             44 ;--------------------------------------------------------
                             45 ; code
                             46 ;--------------------------------------------------------
                             47 	.area _CODE
                             48 ;src/entities/projectile.c:17: void projectileinit(Projectile* projectile) {
                             49 ;	---------------------------------
                             50 ; Function projectileinit
                             51 ; ---------------------------------
   5EA3                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5EA3 21 03 00      [10]   54 	ld	hl, #2+1
   5EA6 39            [11]   55 	add	hl, sp
   5EA7 7E            [ 7]   56 	ld	a, (hl)
   5EA8 2B            [ 6]   57 	dec	hl
   5EA9 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5EAA C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5EAB D1            [10]   62 	pop	de
   5EAC C1            [10]   63 	pop	bc
   5EAD C5            [11]   64 	push	bc
   5EAE D5            [11]   65 	push	de
   5EAF AF            [ 4]   66 	xor	a, a
   5EB0 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5EB1 59            [ 4]   69 	ld	e, c
   5EB2 50            [ 4]   70 	ld	d, b
   5EB3 13            [ 6]   71 	inc	de
   5EB4 AF            [ 4]   72 	xor	a, a
   5EB5 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5EB6 59            [ 4]   75 	ld	e, c
   5EB7 50            [ 4]   76 	ld	d, b
   5EB8 13            [ 6]   77 	inc	de
   5EB9 13            [ 6]   78 	inc	de
   5EBA AF            [ 4]   79 	xor	a, a
   5EBB 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5EBC 59            [ 4]   82 	ld	e, c
   5EBD 50            [ 4]   83 	ld	d, b
   5EBE 13            [ 6]   84 	inc	de
   5EBF 13            [ 6]   85 	inc	de
   5EC0 13            [ 6]   86 	inc	de
   5EC1 AF            [ 4]   87 	xor	a, a
   5EC2 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5EC3 21 04 00      [10]   90 	ld	hl, #0x0004
   5EC6 09            [11]   91 	add	hl, bc
   5EC7 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5EC9 21 05 00      [10]   94 	ld	hl, #0x0005
   5ECC 09            [11]   95 	add	hl, bc
   5ECD 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5ECF 21 06 00      [10]   98 	ld	hl, #0x0006
   5ED2 09            [11]   99 	add	hl, bc
   5ED3 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5ED5 21 07 00      [10]  102 	ld	hl, #0x0007
   5ED8 09            [11]  103 	add	hl, bc
   5ED9 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5EDB 21 08 00      [10]  106 	ld	hl, #0x0008
   5EDE 09            [11]  107 	add	hl, bc
   5EDF 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5EE1 21 09 00      [10]  110 	ld	hl, #0x0009
   5EE4 09            [11]  111 	add	hl, bc
   5EE5 36 00         [10]  112 	ld	(hl), #0x00
   5EE7 C9            [10]  113 	ret
   5EE8                     114 _projectile_basic_sprite:
   5EE8 FF                  115 	.db #0xff	; 255
   5EE9 FF                  116 	.db #0xff	; 255
   5EEA FF                  117 	.db #0xff	; 255
   5EEB FF                  118 	.db #0xff	; 255
   5EEC FF                  119 	.db #0xff	; 255
   5EED FF                  120 	.db #0xff	; 255
   5EEE                     121 _projectile_up_sprite:
   5EEE CF                  122 	.db #0xcf	; 207
   5EEF CF                  123 	.db #0xcf	; 207
   5EF0 CF                  124 	.db #0xcf	; 207
   5EF1 CF                  125 	.db #0xcf	; 207
   5EF2 CF                  126 	.db #0xcf	; 207
   5EF3 CF                  127 	.db #0xcf	; 207
   5EF4                     128 _projectile_special_sprite:
   5EF4 F0                  129 	.db #0xf0	; 240
   5EF5 F0                  130 	.db #0xf0	; 240
   5EF6 F0                  131 	.db #0xf0	; 240
   5EF7 F0                  132 	.db #0xf0	; 240
   5EF8 F0                  133 	.db #0xf0	; 240
   5EF9 F0                  134 	.db #0xf0	; 240
   5EFA F0                  135 	.db #0xf0	; 240
   5EFB F0                  136 	.db #0xf0	; 240
   5EFC F0                  137 	.db #0xf0	; 240
   5EFD F0                  138 	.db #0xf0	; 240
   5EFE F0                  139 	.db #0xf0	; 240
   5EFF F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5F00                     145 _projectilefire::
   5F00 DD E5         [15]  146 	push	ix
   5F02 DD 21 00 00   [14]  147 	ld	ix,#0
   5F06 DD 39         [15]  148 	add	ix,sp
   5F08 F5            [11]  149 	push	af
   5F09 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5F0A DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5F0D DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5F10 CA B2 5F      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5F13 DD 4E 04      [19]  157 	ld	c,4 (ix)
   5F16 DD 46 05      [19]  158 	ld	b,5 (ix)
   5F19 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5F1C 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5F1D 59            [ 4]  162 	ld	e, c
   5F1E 50            [ 4]  163 	ld	d, b
   5F1F 13            [ 6]  164 	inc	de
   5F20 DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5F23 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5F24 21 02 00      [10]  168 	ld	hl, #0x0002
   5F27 09            [11]  169 	add	hl,bc
   5F28 DD 75 FE      [19]  170 	ld	-2 (ix), l
   5F2B DD 74 FF      [19]  171 	ld	-1 (ix), h
   5F2E DD 7E 08      [19]  172 	ld	a, 8 (ix)
   5F31 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   5F32 59            [ 4]  175 	ld	e, c
   5F33 50            [ 4]  176 	ld	d, b
   5F34 13            [ 6]  177 	inc	de
   5F35 13            [ 6]  178 	inc	de
   5F36 13            [ 6]  179 	inc	de
   5F37 AF            [ 4]  180 	xor	a, a
   5F38 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5F39 21 09 00      [10]  183 	ld	hl, #0x0009
   5F3C 09            [11]  184 	add	hl, bc
   5F3D DD 7E 09      [19]  185 	ld	a, 9 (ix)
   5F40 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   5F41 21 06 00      [10]  188 	ld	hl, #0x0006
   5F44 09            [11]  189 	add	hl, bc
   5F45 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   5F47 21 04 00      [10]  192 	ld	hl, #0x0004
   5F4A 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   5F4B 79            [ 4]  195 	ld	a, c
   5F4C C6 05         [ 7]  196 	add	a, #0x05
   5F4E 5F            [ 4]  197 	ld	e, a
   5F4F 78            [ 4]  198 	ld	a, b
   5F50 CE 00         [ 7]  199 	adc	a, #0x00
   5F52 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   5F53 79            [ 4]  202 	ld	a, c
   5F54 C6 07         [ 7]  203 	add	a, #0x07
   5F56 DD 77 FC      [19]  204 	ld	-4 (ix), a
   5F59 78            [ 4]  205 	ld	a, b
   5F5A CE 00         [ 7]  206 	adc	a, #0x00
   5F5C DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5F5F 79            [ 4]  209 	ld	a, c
   5F60 C6 08         [ 7]  210 	add	a, #0x08
   5F62 4F            [ 4]  211 	ld	c, a
   5F63 78            [ 4]  212 	ld	a, b
   5F64 CE 00         [ 7]  213 	adc	a, #0x00
   5F66 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   5F67 DD 7E 09      [19]  216 	ld	a, 9 (ix)
   5F6A B7            [ 4]  217 	or	a, a
   5F6B 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   5F6D 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   5F6F 3E 02         [ 7]  222 	ld	a, #0x02
   5F71 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   5F72 E1            [10]  225 	pop	hl
   5F73 E5            [11]  226 	push	hl
   5F74 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5F76 3E 2D         [ 7]  229 	ld	a, #0x2d
   5F78 02            [ 7]  230 	ld	(bc), a
   5F79 18 37         [12]  231 	jr	00109$
   5F7B                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5F7B DD 7E 09      [19]  234 	ld	a, 9 (ix)
   5F7E 3D            [ 4]  235 	dec	a
   5F7F 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   5F81 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   5F83 3E 03         [ 7]  240 	ld	a, #0x03
   5F85 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   5F86 E1            [10]  243 	pop	hl
   5F87 E5            [11]  244 	push	hl
   5F88 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   5F8A 3E 1C         [ 7]  247 	ld	a, #0x1c
   5F8C 02            [ 7]  248 	ld	(bc), a
   5F8D 18 23         [12]  249 	jr	00109$
   5F8F                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   5F8F 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   5F91 3E 03         [ 7]  254 	ld	a, #0x03
   5F93 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   5F94 E1            [10]  257 	pop	hl
   5F95 E5            [11]  258 	push	hl
   5F96 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   5F98 3E 38         [ 7]  261 	ld	a, #0x38
   5F9A 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5F9B D1            [10]  264 	pop	de
   5F9C C1            [10]  265 	pop	bc
   5F9D C5            [11]  266 	push	bc
   5F9E D5            [11]  267 	push	de
   5F9F AF            [ 4]  268 	xor	a, a
   5FA0 DD 96 08      [19]  269 	sub	a, 8 (ix)
   5FA3 E2 A8 5F      [10]  270 	jp	PO, 00131$
   5FA6 EE 80         [ 7]  271 	xor	a, #0x80
   5FA8                     272 00131$:
   5FA8 F2 AF 5F      [10]  273 	jp	P, 00111$
   5FAB 3E 04         [ 7]  274 	ld	a, #0x04
   5FAD 18 02         [12]  275 	jr	00112$
   5FAF                     276 00111$:
   5FAF 3E FC         [ 7]  277 	ld	a, #0xfc
   5FB1                     278 00112$:
   5FB1 02            [ 7]  279 	ld	(bc), a
   5FB2                     280 00109$:
   5FB2 DD F9         [10]  281 	ld	sp, ix
   5FB4 DD E1         [14]  282 	pop	ix
   5FB6 C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   5FB7                     288 _projectileupdate::
   5FB7 DD E5         [15]  289 	push	ix
   5FB9 DD 21 00 00   [14]  290 	ld	ix,#0
   5FBD DD 39         [15]  291 	add	ix,sp
   5FBF 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   5FC0 DD 7E 05      [19]  294 	ld	a, 5 (ix)
   5FC3 DD B6 04      [19]  295 	or	a,4 (ix)
   5FC6 28 4A         [12]  296 	jr	Z,00109$
   5FC8 DD 5E 04      [19]  297 	ld	e,4 (ix)
   5FCB DD 56 05      [19]  298 	ld	d,5 (ix)
   5FCE FD 21 06 00   [14]  299 	ld	iy, #0x0006
   5FD2 FD 19         [15]  300 	add	iy, de
   5FD4 FD 7E 00      [19]  301 	ld	a, 0 (iy)
   5FD7 B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   5FD8 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   5FDA 1A            [ 7]  306 	ld	a, (de)
   5FDB 4F            [ 4]  307 	ld	c, a
   5FDC 6B            [ 4]  308 	ld	l, e
   5FDD 62            [ 4]  309 	ld	h, d
   5FDE 23            [ 6]  310 	inc	hl
   5FDF 23            [ 6]  311 	inc	hl
   5FE0 6E            [ 7]  312 	ld	l, (hl)
   5FE1 09            [11]  313 	add	hl, bc
   5FE2 7D            [ 4]  314 	ld	a, l
   5FE3 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   5FE4 4B            [ 4]  317 	ld	c, e
   5FE5 42            [ 4]  318 	ld	b, d
   5FE6 03            [ 6]  319 	inc	bc
   5FE7 0A            [ 7]  320 	ld	a, (bc)
   5FE8 DD 77 FF      [19]  321 	ld	-1 (ix), a
   5FEB 6B            [ 4]  322 	ld	l, e
   5FEC 62            [ 4]  323 	ld	h, d
   5FED 23            [ 6]  324 	inc	hl
   5FEE 23            [ 6]  325 	inc	hl
   5FEF 23            [ 6]  326 	inc	hl
   5FF0 6E            [ 7]  327 	ld	l, (hl)
   5FF1 DD 7E FF      [19]  328 	ld	a, -1 (ix)
   5FF4 85            [ 4]  329 	add	a, l
   5FF5 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   5FF6 21 08 00      [10]  332 	ld	hl, #0x0008
   5FF9 19            [11]  333 	add	hl,de
   5FFA 4D            [ 4]  334 	ld	c, l
   5FFB 44            [ 4]  335 	ld	b, h
   5FFC 0A            [ 7]  336 	ld	a, (bc)
   5FFD B7            [ 4]  337 	or	a, a
   5FFE 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   6000 C6 FF         [ 7]  340 	add	a, #0xff
   6002 02            [ 7]  341 	ld	(bc), a
   6003                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   6003 1A            [ 7]  344 	ld	a, (de)
   6004 5F            [ 4]  345 	ld	e, a
   6005 3E 4E         [ 7]  346 	ld	a, #0x4e
   6007 93            [ 4]  347 	sub	a, e
   6008 38 04         [12]  348 	jr	C,00106$
   600A 0A            [ 7]  349 	ld	a, (bc)
   600B B7            [ 4]  350 	or	a, a
   600C 20 04         [12]  351 	jr	NZ,00109$
   600E                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   600E FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   6012                     355 00109$:
   6012 33            [ 6]  356 	inc	sp
   6013 DD E1         [14]  357 	pop	ix
   6015 C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   6016                     363 _projectilerender::
   6016 DD E5         [15]  364 	push	ix
   6018 DD 21 00 00   [14]  365 	ld	ix,#0
   601C DD 39         [15]  366 	add	ix,sp
   601E F5            [11]  367 	push	af
   601F 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   6020 DD 7E 05      [19]  370 	ld	a, 5 (ix)
   6023 DD B6 04      [19]  371 	or	a,4 (ix)
   6026 28 6B         [12]  372 	jr	Z,00110$
   6028 DD 4E 04      [19]  373 	ld	c,4 (ix)
   602B DD 46 05      [19]  374 	ld	b,5 (ix)
   602E C5            [11]  375 	push	bc
   602F FD E1         [14]  376 	pop	iy
   6031 FD 7E 06      [19]  377 	ld	a, 6 (iy)
   6034 B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   6035 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   6037 C5            [11]  382 	push	bc
   6038 FD E1         [14]  383 	pop	iy
   603A FD 7E 09      [19]  384 	ld	a, 9 (iy)
   603D B7            [ 4]  385 	or	a, a
   603E 20 0A         [12]  386 	jr	NZ,00108$
   6040 DD 36 FE E8   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   6044 DD 36 FF 5E   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   6048 18 15         [12]  389 	jr	00109$
   604A                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   604A 3D            [ 4]  392 	dec	a
   604B 20 0A         [12]  393 	jr	NZ,00105$
   604D DD 36 FE EE   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   6051 DD 36 FF 5E   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   6055 18 08         [12]  396 	jr	00109$
   6057                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   6057 DD 36 FE F4   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   605B DD 36 FF 5E   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   605F                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   605F 69            [ 4]  403 	ld	l, c
   6060 60            [ 4]  404 	ld	h, b
   6061 23            [ 6]  405 	inc	hl
   6062 56            [ 7]  406 	ld	d, (hl)
   6063 0A            [ 7]  407 	ld	a, (bc)
   6064 C5            [11]  408 	push	bc
   6065 5F            [ 4]  409 	ld	e, a
   6066 D5            [11]  410 	push	de
   6067 21 00 C0      [10]  411 	ld	hl, #0xc000
   606A E5            [11]  412 	push	hl
   606B CD 41 63      [17]  413 	call	_cpct_getScreenPtr
   606E EB            [ 4]  414 	ex	de,hl
   606F C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   6070 C5            [11]  417 	push	bc
   6071 FD E1         [14]  418 	pop	iy
   6073 FD 7E 05      [19]  419 	ld	a, 5 (iy)
   6076 DD 77 FD      [19]  420 	ld	-3 (ix), a
   6079 69            [ 4]  421 	ld	l, c
   607A 60            [ 4]  422 	ld	h, b
   607B 01 04 00      [10]  423 	ld	bc, #0x0004
   607E 09            [11]  424 	add	hl, bc
   607F 4E            [ 7]  425 	ld	c, (hl)
   6080 D5            [11]  426 	push	de
   6081 FD E1         [14]  427 	pop	iy
   6083 DD 5E FE      [19]  428 	ld	e,-2 (ix)
   6086 DD 56 FF      [19]  429 	ld	d,-1 (ix)
   6089 DD 46 FD      [19]  430 	ld	b, -3 (ix)
   608C C5            [11]  431 	push	bc
   608D FD E5         [15]  432 	push	iy
   608F D5            [11]  433 	push	de
   6090 CD 72 61      [17]  434 	call	_cpct_drawSprite
   6093                     435 00110$:
   6093 DD F9         [10]  436 	ld	sp, ix
   6095 DD E1         [14]  437 	pop	ix
   6097 C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
