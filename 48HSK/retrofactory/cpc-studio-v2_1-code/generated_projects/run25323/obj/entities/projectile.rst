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
   5E09                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5E09 21 03 00      [10]   54 	ld	hl, #2+1
   5E0C 39            [11]   55 	add	hl, sp
   5E0D 7E            [ 7]   56 	ld	a, (hl)
   5E0E 2B            [ 6]   57 	dec	hl
   5E0F B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5E10 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5E11 D1            [10]   62 	pop	de
   5E12 C1            [10]   63 	pop	bc
   5E13 C5            [11]   64 	push	bc
   5E14 D5            [11]   65 	push	de
   5E15 AF            [ 4]   66 	xor	a, a
   5E16 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5E17 59            [ 4]   69 	ld	e, c
   5E18 50            [ 4]   70 	ld	d, b
   5E19 13            [ 6]   71 	inc	de
   5E1A AF            [ 4]   72 	xor	a, a
   5E1B 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5E1C 59            [ 4]   75 	ld	e, c
   5E1D 50            [ 4]   76 	ld	d, b
   5E1E 13            [ 6]   77 	inc	de
   5E1F 13            [ 6]   78 	inc	de
   5E20 AF            [ 4]   79 	xor	a, a
   5E21 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5E22 59            [ 4]   82 	ld	e, c
   5E23 50            [ 4]   83 	ld	d, b
   5E24 13            [ 6]   84 	inc	de
   5E25 13            [ 6]   85 	inc	de
   5E26 13            [ 6]   86 	inc	de
   5E27 AF            [ 4]   87 	xor	a, a
   5E28 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5E29 21 04 00      [10]   90 	ld	hl, #0x0004
   5E2C 09            [11]   91 	add	hl, bc
   5E2D 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5E2F 21 05 00      [10]   94 	ld	hl, #0x0005
   5E32 09            [11]   95 	add	hl, bc
   5E33 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5E35 21 06 00      [10]   98 	ld	hl, #0x0006
   5E38 09            [11]   99 	add	hl, bc
   5E39 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5E3B 21 07 00      [10]  102 	ld	hl, #0x0007
   5E3E 09            [11]  103 	add	hl, bc
   5E3F 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5E41 21 08 00      [10]  106 	ld	hl, #0x0008
   5E44 09            [11]  107 	add	hl, bc
   5E45 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5E47 21 09 00      [10]  110 	ld	hl, #0x0009
   5E4A 09            [11]  111 	add	hl, bc
   5E4B 36 00         [10]  112 	ld	(hl), #0x00
   5E4D C9            [10]  113 	ret
   5E4E                     114 _projectile_basic_sprite:
   5E4E FF                  115 	.db #0xff	; 255
   5E4F FF                  116 	.db #0xff	; 255
   5E50 FF                  117 	.db #0xff	; 255
   5E51 FF                  118 	.db #0xff	; 255
   5E52 FF                  119 	.db #0xff	; 255
   5E53 FF                  120 	.db #0xff	; 255
   5E54                     121 _projectile_up_sprite:
   5E54 CF                  122 	.db #0xcf	; 207
   5E55 CF                  123 	.db #0xcf	; 207
   5E56 CF                  124 	.db #0xcf	; 207
   5E57 CF                  125 	.db #0xcf	; 207
   5E58 CF                  126 	.db #0xcf	; 207
   5E59 CF                  127 	.db #0xcf	; 207
   5E5A                     128 _projectile_special_sprite:
   5E5A F0                  129 	.db #0xf0	; 240
   5E5B F0                  130 	.db #0xf0	; 240
   5E5C F0                  131 	.db #0xf0	; 240
   5E5D F0                  132 	.db #0xf0	; 240
   5E5E F0                  133 	.db #0xf0	; 240
   5E5F F0                  134 	.db #0xf0	; 240
   5E60 F0                  135 	.db #0xf0	; 240
   5E61 F0                  136 	.db #0xf0	; 240
   5E62 F0                  137 	.db #0xf0	; 240
   5E63 F0                  138 	.db #0xf0	; 240
   5E64 F0                  139 	.db #0xf0	; 240
   5E65 F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5E66                     145 _projectilefire::
   5E66 DD E5         [15]  146 	push	ix
   5E68 DD 21 00 00   [14]  147 	ld	ix,#0
   5E6C DD 39         [15]  148 	add	ix,sp
   5E6E F5            [11]  149 	push	af
   5E6F F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5E70 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5E73 DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5E76 CA 18 5F      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5E79 DD 4E 04      [19]  157 	ld	c,4 (ix)
   5E7C DD 46 05      [19]  158 	ld	b,5 (ix)
   5E7F DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5E82 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5E83 59            [ 4]  162 	ld	e, c
   5E84 50            [ 4]  163 	ld	d, b
   5E85 13            [ 6]  164 	inc	de
   5E86 DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5E89 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5E8A 21 02 00      [10]  168 	ld	hl, #0x0002
   5E8D 09            [11]  169 	add	hl,bc
   5E8E DD 75 FE      [19]  170 	ld	-2 (ix), l
   5E91 DD 74 FF      [19]  171 	ld	-1 (ix), h
   5E94 DD 7E 08      [19]  172 	ld	a, 8 (ix)
   5E97 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   5E98 59            [ 4]  175 	ld	e, c
   5E99 50            [ 4]  176 	ld	d, b
   5E9A 13            [ 6]  177 	inc	de
   5E9B 13            [ 6]  178 	inc	de
   5E9C 13            [ 6]  179 	inc	de
   5E9D AF            [ 4]  180 	xor	a, a
   5E9E 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5E9F 21 09 00      [10]  183 	ld	hl, #0x0009
   5EA2 09            [11]  184 	add	hl, bc
   5EA3 DD 7E 09      [19]  185 	ld	a, 9 (ix)
   5EA6 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   5EA7 21 06 00      [10]  188 	ld	hl, #0x0006
   5EAA 09            [11]  189 	add	hl, bc
   5EAB 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   5EAD 21 04 00      [10]  192 	ld	hl, #0x0004
   5EB0 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   5EB1 79            [ 4]  195 	ld	a, c
   5EB2 C6 05         [ 7]  196 	add	a, #0x05
   5EB4 5F            [ 4]  197 	ld	e, a
   5EB5 78            [ 4]  198 	ld	a, b
   5EB6 CE 00         [ 7]  199 	adc	a, #0x00
   5EB8 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   5EB9 79            [ 4]  202 	ld	a, c
   5EBA C6 07         [ 7]  203 	add	a, #0x07
   5EBC DD 77 FC      [19]  204 	ld	-4 (ix), a
   5EBF 78            [ 4]  205 	ld	a, b
   5EC0 CE 00         [ 7]  206 	adc	a, #0x00
   5EC2 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5EC5 79            [ 4]  209 	ld	a, c
   5EC6 C6 08         [ 7]  210 	add	a, #0x08
   5EC8 4F            [ 4]  211 	ld	c, a
   5EC9 78            [ 4]  212 	ld	a, b
   5ECA CE 00         [ 7]  213 	adc	a, #0x00
   5ECC 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   5ECD DD 7E 09      [19]  216 	ld	a, 9 (ix)
   5ED0 B7            [ 4]  217 	or	a, a
   5ED1 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   5ED3 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   5ED5 3E 02         [ 7]  222 	ld	a, #0x02
   5ED7 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   5ED8 E1            [10]  225 	pop	hl
   5ED9 E5            [11]  226 	push	hl
   5EDA 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5EDC 3E 2D         [ 7]  229 	ld	a, #0x2d
   5EDE 02            [ 7]  230 	ld	(bc), a
   5EDF 18 37         [12]  231 	jr	00109$
   5EE1                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5EE1 DD 7E 09      [19]  234 	ld	a, 9 (ix)
   5EE4 3D            [ 4]  235 	dec	a
   5EE5 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   5EE7 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   5EE9 3E 03         [ 7]  240 	ld	a, #0x03
   5EEB 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   5EEC E1            [10]  243 	pop	hl
   5EED E5            [11]  244 	push	hl
   5EEE 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   5EF0 3E 1C         [ 7]  247 	ld	a, #0x1c
   5EF2 02            [ 7]  248 	ld	(bc), a
   5EF3 18 23         [12]  249 	jr	00109$
   5EF5                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   5EF5 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   5EF7 3E 03         [ 7]  254 	ld	a, #0x03
   5EF9 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   5EFA E1            [10]  257 	pop	hl
   5EFB E5            [11]  258 	push	hl
   5EFC 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   5EFE 3E 38         [ 7]  261 	ld	a, #0x38
   5F00 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5F01 D1            [10]  264 	pop	de
   5F02 C1            [10]  265 	pop	bc
   5F03 C5            [11]  266 	push	bc
   5F04 D5            [11]  267 	push	de
   5F05 AF            [ 4]  268 	xor	a, a
   5F06 DD 96 08      [19]  269 	sub	a, 8 (ix)
   5F09 E2 0E 5F      [10]  270 	jp	PO, 00131$
   5F0C EE 80         [ 7]  271 	xor	a, #0x80
   5F0E                     272 00131$:
   5F0E F2 15 5F      [10]  273 	jp	P, 00111$
   5F11 3E 04         [ 7]  274 	ld	a, #0x04
   5F13 18 02         [12]  275 	jr	00112$
   5F15                     276 00111$:
   5F15 3E FC         [ 7]  277 	ld	a, #0xfc
   5F17                     278 00112$:
   5F17 02            [ 7]  279 	ld	(bc), a
   5F18                     280 00109$:
   5F18 DD F9         [10]  281 	ld	sp, ix
   5F1A DD E1         [14]  282 	pop	ix
   5F1C C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   5F1D                     288 _projectileupdate::
   5F1D DD E5         [15]  289 	push	ix
   5F1F DD 21 00 00   [14]  290 	ld	ix,#0
   5F23 DD 39         [15]  291 	add	ix,sp
   5F25 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   5F26 DD 7E 05      [19]  294 	ld	a, 5 (ix)
   5F29 DD B6 04      [19]  295 	or	a,4 (ix)
   5F2C 28 4A         [12]  296 	jr	Z,00109$
   5F2E DD 5E 04      [19]  297 	ld	e,4 (ix)
   5F31 DD 56 05      [19]  298 	ld	d,5 (ix)
   5F34 FD 21 06 00   [14]  299 	ld	iy, #0x0006
   5F38 FD 19         [15]  300 	add	iy, de
   5F3A FD 7E 00      [19]  301 	ld	a, 0 (iy)
   5F3D B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   5F3E 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   5F40 1A            [ 7]  306 	ld	a, (de)
   5F41 4F            [ 4]  307 	ld	c, a
   5F42 6B            [ 4]  308 	ld	l, e
   5F43 62            [ 4]  309 	ld	h, d
   5F44 23            [ 6]  310 	inc	hl
   5F45 23            [ 6]  311 	inc	hl
   5F46 6E            [ 7]  312 	ld	l, (hl)
   5F47 09            [11]  313 	add	hl, bc
   5F48 7D            [ 4]  314 	ld	a, l
   5F49 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   5F4A 4B            [ 4]  317 	ld	c, e
   5F4B 42            [ 4]  318 	ld	b, d
   5F4C 03            [ 6]  319 	inc	bc
   5F4D 0A            [ 7]  320 	ld	a, (bc)
   5F4E DD 77 FF      [19]  321 	ld	-1 (ix), a
   5F51 6B            [ 4]  322 	ld	l, e
   5F52 62            [ 4]  323 	ld	h, d
   5F53 23            [ 6]  324 	inc	hl
   5F54 23            [ 6]  325 	inc	hl
   5F55 23            [ 6]  326 	inc	hl
   5F56 6E            [ 7]  327 	ld	l, (hl)
   5F57 DD 7E FF      [19]  328 	ld	a, -1 (ix)
   5F5A 85            [ 4]  329 	add	a, l
   5F5B 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   5F5C 21 08 00      [10]  332 	ld	hl, #0x0008
   5F5F 19            [11]  333 	add	hl,de
   5F60 4D            [ 4]  334 	ld	c, l
   5F61 44            [ 4]  335 	ld	b, h
   5F62 0A            [ 7]  336 	ld	a, (bc)
   5F63 B7            [ 4]  337 	or	a, a
   5F64 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   5F66 C6 FF         [ 7]  340 	add	a, #0xff
   5F68 02            [ 7]  341 	ld	(bc), a
   5F69                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   5F69 1A            [ 7]  344 	ld	a, (de)
   5F6A 5F            [ 4]  345 	ld	e, a
   5F6B 3E 4E         [ 7]  346 	ld	a, #0x4e
   5F6D 93            [ 4]  347 	sub	a, e
   5F6E 38 04         [12]  348 	jr	C,00106$
   5F70 0A            [ 7]  349 	ld	a, (bc)
   5F71 B7            [ 4]  350 	or	a, a
   5F72 20 04         [12]  351 	jr	NZ,00109$
   5F74                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   5F74 FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   5F78                     355 00109$:
   5F78 33            [ 6]  356 	inc	sp
   5F79 DD E1         [14]  357 	pop	ix
   5F7B C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   5F7C                     363 _projectilerender::
   5F7C DD E5         [15]  364 	push	ix
   5F7E DD 21 00 00   [14]  365 	ld	ix,#0
   5F82 DD 39         [15]  366 	add	ix,sp
   5F84 F5            [11]  367 	push	af
   5F85 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   5F86 DD 7E 05      [19]  370 	ld	a, 5 (ix)
   5F89 DD B6 04      [19]  371 	or	a,4 (ix)
   5F8C 28 6B         [12]  372 	jr	Z,00110$
   5F8E DD 4E 04      [19]  373 	ld	c,4 (ix)
   5F91 DD 46 05      [19]  374 	ld	b,5 (ix)
   5F94 C5            [11]  375 	push	bc
   5F95 FD E1         [14]  376 	pop	iy
   5F97 FD 7E 06      [19]  377 	ld	a, 6 (iy)
   5F9A B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   5F9B 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   5F9D C5            [11]  382 	push	bc
   5F9E FD E1         [14]  383 	pop	iy
   5FA0 FD 7E 09      [19]  384 	ld	a, 9 (iy)
   5FA3 B7            [ 4]  385 	or	a, a
   5FA4 20 0A         [12]  386 	jr	NZ,00108$
   5FA6 DD 36 FE 4E   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   5FAA DD 36 FF 5E   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   5FAE 18 15         [12]  389 	jr	00109$
   5FB0                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   5FB0 3D            [ 4]  392 	dec	a
   5FB1 20 0A         [12]  393 	jr	NZ,00105$
   5FB3 DD 36 FE 54   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   5FB7 DD 36 FF 5E   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   5FBB 18 08         [12]  396 	jr	00109$
   5FBD                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   5FBD DD 36 FE 5A   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   5FC1 DD 36 FF 5E   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   5FC5                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5FC5 69            [ 4]  403 	ld	l, c
   5FC6 60            [ 4]  404 	ld	h, b
   5FC7 23            [ 6]  405 	inc	hl
   5FC8 56            [ 7]  406 	ld	d, (hl)
   5FC9 0A            [ 7]  407 	ld	a, (bc)
   5FCA C5            [11]  408 	push	bc
   5FCB 5F            [ 4]  409 	ld	e, a
   5FCC D5            [11]  410 	push	de
   5FCD 21 00 C0      [10]  411 	ld	hl, #0xc000
   5FD0 E5            [11]  412 	push	hl
   5FD1 CD A7 62      [17]  413 	call	_cpct_getScreenPtr
   5FD4 EB            [ 4]  414 	ex	de,hl
   5FD5 C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   5FD6 C5            [11]  417 	push	bc
   5FD7 FD E1         [14]  418 	pop	iy
   5FD9 FD 7E 05      [19]  419 	ld	a, 5 (iy)
   5FDC DD 77 FD      [19]  420 	ld	-3 (ix), a
   5FDF 69            [ 4]  421 	ld	l, c
   5FE0 60            [ 4]  422 	ld	h, b
   5FE1 01 04 00      [10]  423 	ld	bc, #0x0004
   5FE4 09            [11]  424 	add	hl, bc
   5FE5 4E            [ 7]  425 	ld	c, (hl)
   5FE6 D5            [11]  426 	push	de
   5FE7 FD E1         [14]  427 	pop	iy
   5FE9 DD 5E FE      [19]  428 	ld	e,-2 (ix)
   5FEC DD 56 FF      [19]  429 	ld	d,-1 (ix)
   5FEF DD 46 FD      [19]  430 	ld	b, -3 (ix)
   5FF2 C5            [11]  431 	push	bc
   5FF3 FD E5         [15]  432 	push	iy
   5FF5 D5            [11]  433 	push	de
   5FF6 CD D8 60      [17]  434 	call	_cpct_drawSprite
   5FF9                     435 00110$:
   5FF9 DD F9         [10]  436 	ld	sp, ix
   5FFB DD E1         [14]  437 	pop	ix
   5FFD C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
