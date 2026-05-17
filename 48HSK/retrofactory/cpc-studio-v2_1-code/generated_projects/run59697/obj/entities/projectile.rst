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
   5E45                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5E45 21 03 00      [10]   54 	ld	hl, #2+1
   5E48 39            [11]   55 	add	hl, sp
   5E49 7E            [ 7]   56 	ld	a, (hl)
   5E4A 2B            [ 6]   57 	dec	hl
   5E4B B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5E4C C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5E4D D1            [10]   62 	pop	de
   5E4E C1            [10]   63 	pop	bc
   5E4F C5            [11]   64 	push	bc
   5E50 D5            [11]   65 	push	de
   5E51 AF            [ 4]   66 	xor	a, a
   5E52 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5E53 59            [ 4]   69 	ld	e, c
   5E54 50            [ 4]   70 	ld	d, b
   5E55 13            [ 6]   71 	inc	de
   5E56 AF            [ 4]   72 	xor	a, a
   5E57 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5E58 59            [ 4]   75 	ld	e, c
   5E59 50            [ 4]   76 	ld	d, b
   5E5A 13            [ 6]   77 	inc	de
   5E5B 13            [ 6]   78 	inc	de
   5E5C AF            [ 4]   79 	xor	a, a
   5E5D 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5E5E 59            [ 4]   82 	ld	e, c
   5E5F 50            [ 4]   83 	ld	d, b
   5E60 13            [ 6]   84 	inc	de
   5E61 13            [ 6]   85 	inc	de
   5E62 13            [ 6]   86 	inc	de
   5E63 AF            [ 4]   87 	xor	a, a
   5E64 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5E65 21 04 00      [10]   90 	ld	hl, #0x0004
   5E68 09            [11]   91 	add	hl, bc
   5E69 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5E6B 21 05 00      [10]   94 	ld	hl, #0x0005
   5E6E 09            [11]   95 	add	hl, bc
   5E6F 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5E71 21 06 00      [10]   98 	ld	hl, #0x0006
   5E74 09            [11]   99 	add	hl, bc
   5E75 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5E77 21 07 00      [10]  102 	ld	hl, #0x0007
   5E7A 09            [11]  103 	add	hl, bc
   5E7B 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5E7D 21 08 00      [10]  106 	ld	hl, #0x0008
   5E80 09            [11]  107 	add	hl, bc
   5E81 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5E83 21 09 00      [10]  110 	ld	hl, #0x0009
   5E86 09            [11]  111 	add	hl, bc
   5E87 36 00         [10]  112 	ld	(hl), #0x00
   5E89 C9            [10]  113 	ret
   5E8A                     114 _projectile_basic_sprite:
   5E8A FF                  115 	.db #0xff	; 255
   5E8B FF                  116 	.db #0xff	; 255
   5E8C FF                  117 	.db #0xff	; 255
   5E8D FF                  118 	.db #0xff	; 255
   5E8E FF                  119 	.db #0xff	; 255
   5E8F FF                  120 	.db #0xff	; 255
   5E90                     121 _projectile_up_sprite:
   5E90 CF                  122 	.db #0xcf	; 207
   5E91 CF                  123 	.db #0xcf	; 207
   5E92 CF                  124 	.db #0xcf	; 207
   5E93 CF                  125 	.db #0xcf	; 207
   5E94 CF                  126 	.db #0xcf	; 207
   5E95 CF                  127 	.db #0xcf	; 207
   5E96                     128 _projectile_special_sprite:
   5E96 F0                  129 	.db #0xf0	; 240
   5E97 F0                  130 	.db #0xf0	; 240
   5E98 F0                  131 	.db #0xf0	; 240
   5E99 F0                  132 	.db #0xf0	; 240
   5E9A F0                  133 	.db #0xf0	; 240
   5E9B F0                  134 	.db #0xf0	; 240
   5E9C F0                  135 	.db #0xf0	; 240
   5E9D F0                  136 	.db #0xf0	; 240
   5E9E F0                  137 	.db #0xf0	; 240
   5E9F F0                  138 	.db #0xf0	; 240
   5EA0 F0                  139 	.db #0xf0	; 240
   5EA1 F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5EA2                     145 _projectilefire::
   5EA2 DD E5         [15]  146 	push	ix
   5EA4 DD 21 00 00   [14]  147 	ld	ix,#0
   5EA8 DD 39         [15]  148 	add	ix,sp
   5EAA F5            [11]  149 	push	af
   5EAB F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5EAC DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5EAF DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5EB2 CA 5B 5F      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5EB5 DD 4E 04      [19]  157 	ld	c,4 (ix)
   5EB8 DD 46 05      [19]  158 	ld	b,5 (ix)
   5EBB DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5EBE 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5EBF 59            [ 4]  162 	ld	e, c
   5EC0 50            [ 4]  163 	ld	d, b
   5EC1 13            [ 6]  164 	inc	de
   5EC2 DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5EC5 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5EC6 21 02 00      [10]  168 	ld	hl, #0x0002
   5EC9 09            [11]  169 	add	hl,bc
   5ECA E3            [19]  170 	ex	(sp), hl
   5ECB E1            [10]  171 	pop	hl
   5ECC E5            [11]  172 	push	hl
   5ECD DD 7E 08      [19]  173 	ld	a, 8 (ix)
   5ED0 77            [ 7]  174 	ld	(hl), a
                            175 ;src/entities/projectile.c:42: projectile->vy = 0;
   5ED1 59            [ 4]  176 	ld	e, c
   5ED2 50            [ 4]  177 	ld	d, b
   5ED3 13            [ 6]  178 	inc	de
   5ED4 13            [ 6]  179 	inc	de
   5ED5 13            [ 6]  180 	inc	de
   5ED6 AF            [ 4]  181 	xor	a, a
   5ED7 12            [ 7]  182 	ld	(de), a
                            183 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5ED8 21 09 00      [10]  184 	ld	hl, #0x0009
   5EDB 09            [11]  185 	add	hl, bc
   5EDC DD 7E 09      [19]  186 	ld	a, 9 (ix)
   5EDF 77            [ 7]  187 	ld	(hl), a
                            188 ;src/entities/projectile.c:44: projectile->active = 1;
   5EE0 21 06 00      [10]  189 	ld	hl, #0x0006
   5EE3 09            [11]  190 	add	hl, bc
   5EE4 36 01         [10]  191 	ld	(hl), #0x01
                            192 ;src/entities/projectile.c:47: projectile->w = 3;
   5EE6 21 04 00      [10]  193 	ld	hl, #0x0004
   5EE9 09            [11]  194 	add	hl, bc
                            195 ;src/entities/projectile.c:48: projectile->h = 2;
   5EEA 79            [ 4]  196 	ld	a, c
   5EEB C6 05         [ 7]  197 	add	a, #0x05
   5EED 5F            [ 4]  198 	ld	e, a
   5EEE 78            [ 4]  199 	ld	a, b
   5EEF CE 00         [ 7]  200 	adc	a, #0x00
   5EF1 57            [ 4]  201 	ld	d, a
                            202 ;src/entities/projectile.c:49: projectile->damage = 1;
   5EF2 79            [ 4]  203 	ld	a, c
   5EF3 C6 07         [ 7]  204 	add	a, #0x07
   5EF5 DD 77 FE      [19]  205 	ld	-2 (ix), a
   5EF8 78            [ 4]  206 	ld	a, b
   5EF9 CE 00         [ 7]  207 	adc	a, #0x00
   5EFB DD 77 FF      [19]  208 	ld	-1 (ix), a
                            209 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5EFE 79            [ 4]  210 	ld	a, c
   5EFF C6 08         [ 7]  211 	add	a, #0x08
   5F01 4F            [ 4]  212 	ld	c, a
   5F02 78            [ 4]  213 	ld	a, b
   5F03 CE 00         [ 7]  214 	adc	a, #0x00
   5F05 47            [ 4]  215 	ld	b, a
                            216 ;src/entities/projectile.c:46: if (weapon == 0) {
   5F06 DD 7E 09      [19]  217 	ld	a, 9 (ix)
   5F09 B7            [ 4]  218 	or	a, a
   5F0A 20 12         [12]  219 	jr	NZ,00107$
                            220 ;src/entities/projectile.c:47: projectile->w = 3;
   5F0C 36 03         [10]  221 	ld	(hl), #0x03
                            222 ;src/entities/projectile.c:48: projectile->h = 2;
   5F0E 3E 02         [ 7]  223 	ld	a, #0x02
   5F10 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/projectile.c:49: projectile->damage = 1;
   5F11 DD 6E FE      [19]  226 	ld	l,-2 (ix)
   5F14 DD 66 FF      [19]  227 	ld	h,-1 (ix)
   5F17 36 01         [10]  228 	ld	(hl), #0x01
                            229 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5F19 3E 2D         [ 7]  230 	ld	a, #0x2d
   5F1B 02            [ 7]  231 	ld	(bc), a
   5F1C 18 3D         [12]  232 	jr	00109$
   5F1E                     233 00107$:
                            234 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5F1E DD 7E 09      [19]  235 	ld	a, 9 (ix)
   5F21 3D            [ 4]  236 	dec	a
   5F22 20 12         [12]  237 	jr	NZ,00104$
                            238 ;src/entities/projectile.c:52: projectile->w = 2;
   5F24 36 02         [10]  239 	ld	(hl), #0x02
                            240 ;src/entities/projectile.c:53: projectile->h = 3;
   5F26 3E 03         [ 7]  241 	ld	a, #0x03
   5F28 12            [ 7]  242 	ld	(de), a
                            243 ;src/entities/projectile.c:54: projectile->damage = 2;
   5F29 DD 6E FE      [19]  244 	ld	l,-2 (ix)
   5F2C DD 66 FF      [19]  245 	ld	h,-1 (ix)
   5F2F 36 02         [10]  246 	ld	(hl), #0x02
                            247 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   5F31 3E 1C         [ 7]  248 	ld	a, #0x1c
   5F33 02            [ 7]  249 	ld	(bc), a
   5F34 18 25         [12]  250 	jr	00109$
   5F36                     251 00104$:
                            252 ;src/entities/projectile.c:57: projectile->w = 4;
   5F36 36 04         [10]  253 	ld	(hl), #0x04
                            254 ;src/entities/projectile.c:58: projectile->h = 3;
   5F38 3E 03         [ 7]  255 	ld	a, #0x03
   5F3A 12            [ 7]  256 	ld	(de), a
                            257 ;src/entities/projectile.c:59: projectile->damage = 3;
   5F3B DD 6E FE      [19]  258 	ld	l,-2 (ix)
   5F3E DD 66 FF      [19]  259 	ld	h,-1 (ix)
   5F41 36 03         [10]  260 	ld	(hl), #0x03
                            261 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   5F43 3E 38         [ 7]  262 	ld	a, #0x38
   5F45 02            [ 7]  263 	ld	(bc), a
                            264 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5F46 C1            [10]  265 	pop	bc
   5F47 C5            [11]  266 	push	bc
   5F48 AF            [ 4]  267 	xor	a, a
   5F49 DD 96 08      [19]  268 	sub	a, 8 (ix)
   5F4C E2 51 5F      [10]  269 	jp	PO, 00131$
   5F4F EE 80         [ 7]  270 	xor	a, #0x80
   5F51                     271 00131$:
   5F51 F2 58 5F      [10]  272 	jp	P, 00111$
   5F54 3E 04         [ 7]  273 	ld	a, #0x04
   5F56 18 02         [12]  274 	jr	00112$
   5F58                     275 00111$:
   5F58 3E FC         [ 7]  276 	ld	a, #0xfc
   5F5A                     277 00112$:
   5F5A 02            [ 7]  278 	ld	(bc), a
   5F5B                     279 00109$:
   5F5B DD F9         [10]  280 	ld	sp, ix
   5F5D DD E1         [14]  281 	pop	ix
   5F5F C9            [10]  282 	ret
                            283 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            284 ;	---------------------------------
                            285 ; Function projectileupdate
                            286 ; ---------------------------------
   5F60                     287 _projectileupdate::
   5F60 DD E5         [15]  288 	push	ix
   5F62 DD 21 00 00   [14]  289 	ld	ix,#0
   5F66 DD 39         [15]  290 	add	ix,sp
   5F68 3B            [ 6]  291 	dec	sp
                            292 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   5F69 DD 7E 05      [19]  293 	ld	a, 5 (ix)
   5F6C DD B6 04      [19]  294 	or	a,4 (ix)
   5F6F 28 4A         [12]  295 	jr	Z,00109$
   5F71 DD 5E 04      [19]  296 	ld	e,4 (ix)
   5F74 DD 56 05      [19]  297 	ld	d,5 (ix)
   5F77 FD 21 06 00   [14]  298 	ld	iy, #0x0006
   5F7B FD 19         [15]  299 	add	iy, de
   5F7D FD 7E 00      [19]  300 	ld	a, 0 (iy)
   5F80 B7            [ 4]  301 	or	a, a
                            302 ;src/entities/projectile.c:67: return;
   5F81 28 38         [12]  303 	jr	Z,00109$
                            304 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   5F83 1A            [ 7]  305 	ld	a, (de)
   5F84 4F            [ 4]  306 	ld	c, a
   5F85 6B            [ 4]  307 	ld	l, e
   5F86 62            [ 4]  308 	ld	h, d
   5F87 23            [ 6]  309 	inc	hl
   5F88 23            [ 6]  310 	inc	hl
   5F89 6E            [ 7]  311 	ld	l, (hl)
   5F8A 09            [11]  312 	add	hl, bc
   5F8B 7D            [ 4]  313 	ld	a, l
   5F8C 12            [ 7]  314 	ld	(de), a
                            315 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   5F8D 4B            [ 4]  316 	ld	c, e
   5F8E 42            [ 4]  317 	ld	b, d
   5F8F 03            [ 6]  318 	inc	bc
   5F90 0A            [ 7]  319 	ld	a, (bc)
   5F91 DD 77 FF      [19]  320 	ld	-1 (ix), a
   5F94 6B            [ 4]  321 	ld	l, e
   5F95 62            [ 4]  322 	ld	h, d
   5F96 23            [ 6]  323 	inc	hl
   5F97 23            [ 6]  324 	inc	hl
   5F98 23            [ 6]  325 	inc	hl
   5F99 6E            [ 7]  326 	ld	l, (hl)
   5F9A DD 7E FF      [19]  327 	ld	a, -1 (ix)
   5F9D 85            [ 4]  328 	add	a, l
   5F9E 02            [ 7]  329 	ld	(bc), a
                            330 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   5F9F 21 08 00      [10]  331 	ld	hl, #0x0008
   5FA2 19            [11]  332 	add	hl,de
   5FA3 4D            [ 4]  333 	ld	c, l
   5FA4 44            [ 4]  334 	ld	b, h
   5FA5 0A            [ 7]  335 	ld	a, (bc)
   5FA6 B7            [ 4]  336 	or	a, a
   5FA7 28 03         [12]  337 	jr	Z,00105$
                            338 ;src/entities/projectile.c:74: projectile->lifetime--;
   5FA9 C6 FF         [ 7]  339 	add	a, #0xff
   5FAB 02            [ 7]  340 	ld	(bc), a
   5FAC                     341 00105$:
                            342 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   5FAC 1A            [ 7]  343 	ld	a, (de)
   5FAD 5F            [ 4]  344 	ld	e, a
   5FAE 3E 4E         [ 7]  345 	ld	a, #0x4e
   5FB0 93            [ 4]  346 	sub	a, e
   5FB1 38 04         [12]  347 	jr	C,00106$
   5FB3 0A            [ 7]  348 	ld	a, (bc)
   5FB4 B7            [ 4]  349 	or	a, a
   5FB5 20 04         [12]  350 	jr	NZ,00109$
   5FB7                     351 00106$:
                            352 ;src/entities/projectile.c:78: projectile->active = 0;
   5FB7 FD 36 00 00   [19]  353 	ld	0 (iy), #0x00
   5FBB                     354 00109$:
   5FBB 33            [ 6]  355 	inc	sp
   5FBC DD E1         [14]  356 	pop	ix
   5FBE C9            [10]  357 	ret
                            358 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            359 ;	---------------------------------
                            360 ; Function projectilerender
                            361 ; ---------------------------------
   5FBF                     362 _projectilerender::
   5FBF DD E5         [15]  363 	push	ix
   5FC1 DD 21 00 00   [14]  364 	ld	ix,#0
   5FC5 DD 39         [15]  365 	add	ix,sp
   5FC7 F5            [11]  366 	push	af
   5FC8 3B            [ 6]  367 	dec	sp
                            368 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   5FC9 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   5FCC DD B6 04      [19]  370 	or	a,4 (ix)
   5FCF 28 6B         [12]  371 	jr	Z,00110$
   5FD1 DD 4E 04      [19]  372 	ld	c,4 (ix)
   5FD4 DD 46 05      [19]  373 	ld	b,5 (ix)
   5FD7 C5            [11]  374 	push	bc
   5FD8 FD E1         [14]  375 	pop	iy
   5FDA FD 7E 06      [19]  376 	ld	a, 6 (iy)
   5FDD B7            [ 4]  377 	or	a, a
                            378 ;src/entities/projectile.c:87: return;
   5FDE 28 5C         [12]  379 	jr	Z,00110$
                            380 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   5FE0 C5            [11]  381 	push	bc
   5FE1 FD E1         [14]  382 	pop	iy
   5FE3 FD 7E 09      [19]  383 	ld	a, 9 (iy)
   5FE6 B7            [ 4]  384 	or	a, a
   5FE7 20 0A         [12]  385 	jr	NZ,00108$
   5FE9 DD 36 FE 8A   [19]  386 	ld	-2 (ix), #<(_projectile_basic_sprite)
   5FED DD 36 FF 5E   [19]  387 	ld	-1 (ix), #>(_projectile_basic_sprite)
   5FF1 18 15         [12]  388 	jr	00109$
   5FF3                     389 00108$:
                            390 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   5FF3 3D            [ 4]  391 	dec	a
   5FF4 20 0A         [12]  392 	jr	NZ,00105$
   5FF6 DD 36 FE 90   [19]  393 	ld	-2 (ix), #<(_projectile_up_sprite)
   5FFA DD 36 FF 5E   [19]  394 	ld	-1 (ix), #>(_projectile_up_sprite)
   5FFE 18 08         [12]  395 	jr	00109$
   6000                     396 00105$:
                            397 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   6000 DD 36 FE 96   [19]  398 	ld	-2 (ix), #<(_projectile_special_sprite)
   6004 DD 36 FF 5E   [19]  399 	ld	-1 (ix), #>(_projectile_special_sprite)
   6008                     400 00109$:
                            401 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   6008 69            [ 4]  402 	ld	l, c
   6009 60            [ 4]  403 	ld	h, b
   600A 23            [ 6]  404 	inc	hl
   600B 56            [ 7]  405 	ld	d, (hl)
   600C 0A            [ 7]  406 	ld	a, (bc)
   600D C5            [11]  407 	push	bc
   600E 5F            [ 4]  408 	ld	e, a
   600F D5            [11]  409 	push	de
   6010 21 00 C0      [10]  410 	ld	hl, #0xc000
   6013 E5            [11]  411 	push	hl
   6014 CD EA 62      [17]  412 	call	_cpct_getScreenPtr
   6017 EB            [ 4]  413 	ex	de,hl
   6018 C1            [10]  414 	pop	bc
                            415 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   6019 C5            [11]  416 	push	bc
   601A FD E1         [14]  417 	pop	iy
   601C FD 7E 05      [19]  418 	ld	a, 5 (iy)
   601F DD 77 FD      [19]  419 	ld	-3 (ix), a
   6022 69            [ 4]  420 	ld	l, c
   6023 60            [ 4]  421 	ld	h, b
   6024 01 04 00      [10]  422 	ld	bc, #0x0004
   6027 09            [11]  423 	add	hl, bc
   6028 4E            [ 7]  424 	ld	c, (hl)
   6029 D5            [11]  425 	push	de
   602A FD E1         [14]  426 	pop	iy
   602C DD 5E FE      [19]  427 	ld	e,-2 (ix)
   602F DD 56 FF      [19]  428 	ld	d,-1 (ix)
   6032 DD 46 FD      [19]  429 	ld	b, -3 (ix)
   6035 C5            [11]  430 	push	bc
   6036 FD E5         [15]  431 	push	iy
   6038 D5            [11]  432 	push	de
   6039 CD 1B 61      [17]  433 	call	_cpct_drawSprite
   603C                     434 00110$:
   603C DD F9         [10]  435 	ld	sp, ix
   603E DD E1         [14]  436 	pop	ix
   6040 C9            [10]  437 	ret
                            438 	.area _CODE
                            439 	.area _INITIALIZER
                            440 	.area _CABS (ABS)
