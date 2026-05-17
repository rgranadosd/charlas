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
   5E30                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5E30 21 03 00      [10]   54 	ld	hl, #2+1
   5E33 39            [11]   55 	add	hl, sp
   5E34 7E            [ 7]   56 	ld	a, (hl)
   5E35 2B            [ 6]   57 	dec	hl
   5E36 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5E37 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5E38 D1            [10]   62 	pop	de
   5E39 C1            [10]   63 	pop	bc
   5E3A C5            [11]   64 	push	bc
   5E3B D5            [11]   65 	push	de
   5E3C AF            [ 4]   66 	xor	a, a
   5E3D 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5E3E 59            [ 4]   69 	ld	e, c
   5E3F 50            [ 4]   70 	ld	d, b
   5E40 13            [ 6]   71 	inc	de
   5E41 AF            [ 4]   72 	xor	a, a
   5E42 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5E43 59            [ 4]   75 	ld	e, c
   5E44 50            [ 4]   76 	ld	d, b
   5E45 13            [ 6]   77 	inc	de
   5E46 13            [ 6]   78 	inc	de
   5E47 AF            [ 4]   79 	xor	a, a
   5E48 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5E49 59            [ 4]   82 	ld	e, c
   5E4A 50            [ 4]   83 	ld	d, b
   5E4B 13            [ 6]   84 	inc	de
   5E4C 13            [ 6]   85 	inc	de
   5E4D 13            [ 6]   86 	inc	de
   5E4E AF            [ 4]   87 	xor	a, a
   5E4F 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5E50 21 04 00      [10]   90 	ld	hl, #0x0004
   5E53 09            [11]   91 	add	hl, bc
   5E54 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5E56 21 05 00      [10]   94 	ld	hl, #0x0005
   5E59 09            [11]   95 	add	hl, bc
   5E5A 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5E5C 21 06 00      [10]   98 	ld	hl, #0x0006
   5E5F 09            [11]   99 	add	hl, bc
   5E60 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5E62 21 07 00      [10]  102 	ld	hl, #0x0007
   5E65 09            [11]  103 	add	hl, bc
   5E66 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5E68 21 08 00      [10]  106 	ld	hl, #0x0008
   5E6B 09            [11]  107 	add	hl, bc
   5E6C 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5E6E 21 09 00      [10]  110 	ld	hl, #0x0009
   5E71 09            [11]  111 	add	hl, bc
   5E72 36 00         [10]  112 	ld	(hl), #0x00
   5E74 C9            [10]  113 	ret
   5E75                     114 _projectile_basic_sprite:
   5E75 FF                  115 	.db #0xff	; 255
   5E76 FF                  116 	.db #0xff	; 255
   5E77 FF                  117 	.db #0xff	; 255
   5E78 FF                  118 	.db #0xff	; 255
   5E79 FF                  119 	.db #0xff	; 255
   5E7A FF                  120 	.db #0xff	; 255
   5E7B                     121 _projectile_up_sprite:
   5E7B CF                  122 	.db #0xcf	; 207
   5E7C CF                  123 	.db #0xcf	; 207
   5E7D CF                  124 	.db #0xcf	; 207
   5E7E CF                  125 	.db #0xcf	; 207
   5E7F CF                  126 	.db #0xcf	; 207
   5E80 CF                  127 	.db #0xcf	; 207
   5E81                     128 _projectile_special_sprite:
   5E81 F0                  129 	.db #0xf0	; 240
   5E82 F0                  130 	.db #0xf0	; 240
   5E83 F0                  131 	.db #0xf0	; 240
   5E84 F0                  132 	.db #0xf0	; 240
   5E85 F0                  133 	.db #0xf0	; 240
   5E86 F0                  134 	.db #0xf0	; 240
   5E87 F0                  135 	.db #0xf0	; 240
   5E88 F0                  136 	.db #0xf0	; 240
   5E89 F0                  137 	.db #0xf0	; 240
   5E8A F0                  138 	.db #0xf0	; 240
   5E8B F0                  139 	.db #0xf0	; 240
   5E8C F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5E8D                     145 _projectilefire::
   5E8D DD E5         [15]  146 	push	ix
   5E8F DD 21 00 00   [14]  147 	ld	ix,#0
   5E93 DD 39         [15]  148 	add	ix,sp
   5E95 F5            [11]  149 	push	af
   5E96 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5E97 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5E9A DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5E9D CA 3F 5F      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5EA0 DD 4E 04      [19]  157 	ld	c,4 (ix)
   5EA3 DD 46 05      [19]  158 	ld	b,5 (ix)
   5EA6 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5EA9 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5EAA 59            [ 4]  162 	ld	e, c
   5EAB 50            [ 4]  163 	ld	d, b
   5EAC 13            [ 6]  164 	inc	de
   5EAD DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5EB0 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5EB1 21 02 00      [10]  168 	ld	hl, #0x0002
   5EB4 09            [11]  169 	add	hl,bc
   5EB5 DD 75 FE      [19]  170 	ld	-2 (ix), l
   5EB8 DD 74 FF      [19]  171 	ld	-1 (ix), h
   5EBB DD 7E 08      [19]  172 	ld	a, 8 (ix)
   5EBE 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   5EBF 59            [ 4]  175 	ld	e, c
   5EC0 50            [ 4]  176 	ld	d, b
   5EC1 13            [ 6]  177 	inc	de
   5EC2 13            [ 6]  178 	inc	de
   5EC3 13            [ 6]  179 	inc	de
   5EC4 AF            [ 4]  180 	xor	a, a
   5EC5 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5EC6 21 09 00      [10]  183 	ld	hl, #0x0009
   5EC9 09            [11]  184 	add	hl, bc
   5ECA DD 7E 09      [19]  185 	ld	a, 9 (ix)
   5ECD 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   5ECE 21 06 00      [10]  188 	ld	hl, #0x0006
   5ED1 09            [11]  189 	add	hl, bc
   5ED2 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   5ED4 21 04 00      [10]  192 	ld	hl, #0x0004
   5ED7 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   5ED8 79            [ 4]  195 	ld	a, c
   5ED9 C6 05         [ 7]  196 	add	a, #0x05
   5EDB 5F            [ 4]  197 	ld	e, a
   5EDC 78            [ 4]  198 	ld	a, b
   5EDD CE 00         [ 7]  199 	adc	a, #0x00
   5EDF 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   5EE0 79            [ 4]  202 	ld	a, c
   5EE1 C6 07         [ 7]  203 	add	a, #0x07
   5EE3 DD 77 FC      [19]  204 	ld	-4 (ix), a
   5EE6 78            [ 4]  205 	ld	a, b
   5EE7 CE 00         [ 7]  206 	adc	a, #0x00
   5EE9 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5EEC 79            [ 4]  209 	ld	a, c
   5EED C6 08         [ 7]  210 	add	a, #0x08
   5EEF 4F            [ 4]  211 	ld	c, a
   5EF0 78            [ 4]  212 	ld	a, b
   5EF1 CE 00         [ 7]  213 	adc	a, #0x00
   5EF3 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   5EF4 DD 7E 09      [19]  216 	ld	a, 9 (ix)
   5EF7 B7            [ 4]  217 	or	a, a
   5EF8 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   5EFA 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   5EFC 3E 02         [ 7]  222 	ld	a, #0x02
   5EFE 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   5EFF E1            [10]  225 	pop	hl
   5F00 E5            [11]  226 	push	hl
   5F01 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5F03 3E 2D         [ 7]  229 	ld	a, #0x2d
   5F05 02            [ 7]  230 	ld	(bc), a
   5F06 18 37         [12]  231 	jr	00109$
   5F08                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5F08 DD 7E 09      [19]  234 	ld	a, 9 (ix)
   5F0B 3D            [ 4]  235 	dec	a
   5F0C 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   5F0E 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   5F10 3E 03         [ 7]  240 	ld	a, #0x03
   5F12 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   5F13 E1            [10]  243 	pop	hl
   5F14 E5            [11]  244 	push	hl
   5F15 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   5F17 3E 1C         [ 7]  247 	ld	a, #0x1c
   5F19 02            [ 7]  248 	ld	(bc), a
   5F1A 18 23         [12]  249 	jr	00109$
   5F1C                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   5F1C 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   5F1E 3E 03         [ 7]  254 	ld	a, #0x03
   5F20 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   5F21 E1            [10]  257 	pop	hl
   5F22 E5            [11]  258 	push	hl
   5F23 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   5F25 3E 38         [ 7]  261 	ld	a, #0x38
   5F27 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5F28 D1            [10]  264 	pop	de
   5F29 C1            [10]  265 	pop	bc
   5F2A C5            [11]  266 	push	bc
   5F2B D5            [11]  267 	push	de
   5F2C AF            [ 4]  268 	xor	a, a
   5F2D DD 96 08      [19]  269 	sub	a, 8 (ix)
   5F30 E2 35 5F      [10]  270 	jp	PO, 00131$
   5F33 EE 80         [ 7]  271 	xor	a, #0x80
   5F35                     272 00131$:
   5F35 F2 3C 5F      [10]  273 	jp	P, 00111$
   5F38 3E 04         [ 7]  274 	ld	a, #0x04
   5F3A 18 02         [12]  275 	jr	00112$
   5F3C                     276 00111$:
   5F3C 3E FC         [ 7]  277 	ld	a, #0xfc
   5F3E                     278 00112$:
   5F3E 02            [ 7]  279 	ld	(bc), a
   5F3F                     280 00109$:
   5F3F DD F9         [10]  281 	ld	sp, ix
   5F41 DD E1         [14]  282 	pop	ix
   5F43 C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   5F44                     288 _projectileupdate::
   5F44 DD E5         [15]  289 	push	ix
   5F46 DD 21 00 00   [14]  290 	ld	ix,#0
   5F4A DD 39         [15]  291 	add	ix,sp
   5F4C 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   5F4D DD 7E 05      [19]  294 	ld	a, 5 (ix)
   5F50 DD B6 04      [19]  295 	or	a,4 (ix)
   5F53 28 4A         [12]  296 	jr	Z,00109$
   5F55 DD 5E 04      [19]  297 	ld	e,4 (ix)
   5F58 DD 56 05      [19]  298 	ld	d,5 (ix)
   5F5B FD 21 06 00   [14]  299 	ld	iy, #0x0006
   5F5F FD 19         [15]  300 	add	iy, de
   5F61 FD 7E 00      [19]  301 	ld	a, 0 (iy)
   5F64 B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   5F65 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   5F67 1A            [ 7]  306 	ld	a, (de)
   5F68 4F            [ 4]  307 	ld	c, a
   5F69 6B            [ 4]  308 	ld	l, e
   5F6A 62            [ 4]  309 	ld	h, d
   5F6B 23            [ 6]  310 	inc	hl
   5F6C 23            [ 6]  311 	inc	hl
   5F6D 6E            [ 7]  312 	ld	l, (hl)
   5F6E 09            [11]  313 	add	hl, bc
   5F6F 7D            [ 4]  314 	ld	a, l
   5F70 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   5F71 4B            [ 4]  317 	ld	c, e
   5F72 42            [ 4]  318 	ld	b, d
   5F73 03            [ 6]  319 	inc	bc
   5F74 0A            [ 7]  320 	ld	a, (bc)
   5F75 DD 77 FF      [19]  321 	ld	-1 (ix), a
   5F78 6B            [ 4]  322 	ld	l, e
   5F79 62            [ 4]  323 	ld	h, d
   5F7A 23            [ 6]  324 	inc	hl
   5F7B 23            [ 6]  325 	inc	hl
   5F7C 23            [ 6]  326 	inc	hl
   5F7D 6E            [ 7]  327 	ld	l, (hl)
   5F7E DD 7E FF      [19]  328 	ld	a, -1 (ix)
   5F81 85            [ 4]  329 	add	a, l
   5F82 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   5F83 21 08 00      [10]  332 	ld	hl, #0x0008
   5F86 19            [11]  333 	add	hl,de
   5F87 4D            [ 4]  334 	ld	c, l
   5F88 44            [ 4]  335 	ld	b, h
   5F89 0A            [ 7]  336 	ld	a, (bc)
   5F8A B7            [ 4]  337 	or	a, a
   5F8B 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   5F8D C6 FF         [ 7]  340 	add	a, #0xff
   5F8F 02            [ 7]  341 	ld	(bc), a
   5F90                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   5F90 1A            [ 7]  344 	ld	a, (de)
   5F91 5F            [ 4]  345 	ld	e, a
   5F92 3E 4E         [ 7]  346 	ld	a, #0x4e
   5F94 93            [ 4]  347 	sub	a, e
   5F95 38 04         [12]  348 	jr	C,00106$
   5F97 0A            [ 7]  349 	ld	a, (bc)
   5F98 B7            [ 4]  350 	or	a, a
   5F99 20 04         [12]  351 	jr	NZ,00109$
   5F9B                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   5F9B FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   5F9F                     355 00109$:
   5F9F 33            [ 6]  356 	inc	sp
   5FA0 DD E1         [14]  357 	pop	ix
   5FA2 C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   5FA3                     363 _projectilerender::
   5FA3 DD E5         [15]  364 	push	ix
   5FA5 DD 21 00 00   [14]  365 	ld	ix,#0
   5FA9 DD 39         [15]  366 	add	ix,sp
   5FAB F5            [11]  367 	push	af
   5FAC 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   5FAD DD 7E 05      [19]  370 	ld	a, 5 (ix)
   5FB0 DD B6 04      [19]  371 	or	a,4 (ix)
   5FB3 28 6B         [12]  372 	jr	Z,00110$
   5FB5 DD 4E 04      [19]  373 	ld	c,4 (ix)
   5FB8 DD 46 05      [19]  374 	ld	b,5 (ix)
   5FBB C5            [11]  375 	push	bc
   5FBC FD E1         [14]  376 	pop	iy
   5FBE FD 7E 06      [19]  377 	ld	a, 6 (iy)
   5FC1 B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   5FC2 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   5FC4 C5            [11]  382 	push	bc
   5FC5 FD E1         [14]  383 	pop	iy
   5FC7 FD 7E 09      [19]  384 	ld	a, 9 (iy)
   5FCA B7            [ 4]  385 	or	a, a
   5FCB 20 0A         [12]  386 	jr	NZ,00108$
   5FCD DD 36 FE 75   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   5FD1 DD 36 FF 5E   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   5FD5 18 15         [12]  389 	jr	00109$
   5FD7                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   5FD7 3D            [ 4]  392 	dec	a
   5FD8 20 0A         [12]  393 	jr	NZ,00105$
   5FDA DD 36 FE 7B   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   5FDE DD 36 FF 5E   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   5FE2 18 08         [12]  396 	jr	00109$
   5FE4                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   5FE4 DD 36 FE 81   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   5FE8 DD 36 FF 5E   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   5FEC                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5FEC 69            [ 4]  403 	ld	l, c
   5FED 60            [ 4]  404 	ld	h, b
   5FEE 23            [ 6]  405 	inc	hl
   5FEF 56            [ 7]  406 	ld	d, (hl)
   5FF0 0A            [ 7]  407 	ld	a, (bc)
   5FF1 C5            [11]  408 	push	bc
   5FF2 5F            [ 4]  409 	ld	e, a
   5FF3 D5            [11]  410 	push	de
   5FF4 21 00 C0      [10]  411 	ld	hl, #0xc000
   5FF7 E5            [11]  412 	push	hl
   5FF8 CD CE 62      [17]  413 	call	_cpct_getScreenPtr
   5FFB EB            [ 4]  414 	ex	de,hl
   5FFC C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   5FFD C5            [11]  417 	push	bc
   5FFE FD E1         [14]  418 	pop	iy
   6000 FD 7E 05      [19]  419 	ld	a, 5 (iy)
   6003 DD 77 FD      [19]  420 	ld	-3 (ix), a
   6006 69            [ 4]  421 	ld	l, c
   6007 60            [ 4]  422 	ld	h, b
   6008 01 04 00      [10]  423 	ld	bc, #0x0004
   600B 09            [11]  424 	add	hl, bc
   600C 4E            [ 7]  425 	ld	c, (hl)
   600D D5            [11]  426 	push	de
   600E FD E1         [14]  427 	pop	iy
   6010 DD 5E FE      [19]  428 	ld	e,-2 (ix)
   6013 DD 56 FF      [19]  429 	ld	d,-1 (ix)
   6016 DD 46 FD      [19]  430 	ld	b, -3 (ix)
   6019 C5            [11]  431 	push	bc
   601A FD E5         [15]  432 	push	iy
   601C D5            [11]  433 	push	de
   601D CD FF 60      [17]  434 	call	_cpct_drawSprite
   6020                     435 00110$:
   6020 DD F9         [10]  436 	ld	sp, ix
   6022 DD E1         [14]  437 	pop	ix
   6024 C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
