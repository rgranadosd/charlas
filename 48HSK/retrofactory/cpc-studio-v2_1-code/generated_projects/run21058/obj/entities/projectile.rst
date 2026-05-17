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
   5F00                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5F00 21 03 00      [10]   54 	ld	hl, #2+1
   5F03 39            [11]   55 	add	hl, sp
   5F04 7E            [ 7]   56 	ld	a, (hl)
   5F05 2B            [ 6]   57 	dec	hl
   5F06 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5F07 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5F08 D1            [10]   62 	pop	de
   5F09 C1            [10]   63 	pop	bc
   5F0A C5            [11]   64 	push	bc
   5F0B D5            [11]   65 	push	de
   5F0C AF            [ 4]   66 	xor	a, a
   5F0D 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5F0E 59            [ 4]   69 	ld	e, c
   5F0F 50            [ 4]   70 	ld	d, b
   5F10 13            [ 6]   71 	inc	de
   5F11 AF            [ 4]   72 	xor	a, a
   5F12 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5F13 59            [ 4]   75 	ld	e, c
   5F14 50            [ 4]   76 	ld	d, b
   5F15 13            [ 6]   77 	inc	de
   5F16 13            [ 6]   78 	inc	de
   5F17 AF            [ 4]   79 	xor	a, a
   5F18 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5F19 59            [ 4]   82 	ld	e, c
   5F1A 50            [ 4]   83 	ld	d, b
   5F1B 13            [ 6]   84 	inc	de
   5F1C 13            [ 6]   85 	inc	de
   5F1D 13            [ 6]   86 	inc	de
   5F1E AF            [ 4]   87 	xor	a, a
   5F1F 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5F20 21 04 00      [10]   90 	ld	hl, #0x0004
   5F23 09            [11]   91 	add	hl, bc
   5F24 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5F26 21 05 00      [10]   94 	ld	hl, #0x0005
   5F29 09            [11]   95 	add	hl, bc
   5F2A 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5F2C 21 06 00      [10]   98 	ld	hl, #0x0006
   5F2F 09            [11]   99 	add	hl, bc
   5F30 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5F32 21 07 00      [10]  102 	ld	hl, #0x0007
   5F35 09            [11]  103 	add	hl, bc
   5F36 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5F38 21 08 00      [10]  106 	ld	hl, #0x0008
   5F3B 09            [11]  107 	add	hl, bc
   5F3C 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5F3E 21 09 00      [10]  110 	ld	hl, #0x0009
   5F41 09            [11]  111 	add	hl, bc
   5F42 36 00         [10]  112 	ld	(hl), #0x00
   5F44 C9            [10]  113 	ret
   5F45                     114 _projectile_basic_sprite:
   5F45 FF                  115 	.db #0xff	; 255
   5F46 FF                  116 	.db #0xff	; 255
   5F47 FF                  117 	.db #0xff	; 255
   5F48 FF                  118 	.db #0xff	; 255
   5F49 FF                  119 	.db #0xff	; 255
   5F4A FF                  120 	.db #0xff	; 255
   5F4B                     121 _projectile_up_sprite:
   5F4B CF                  122 	.db #0xcf	; 207
   5F4C CF                  123 	.db #0xcf	; 207
   5F4D CF                  124 	.db #0xcf	; 207
   5F4E CF                  125 	.db #0xcf	; 207
   5F4F CF                  126 	.db #0xcf	; 207
   5F50 CF                  127 	.db #0xcf	; 207
   5F51                     128 _projectile_special_sprite:
   5F51 F0                  129 	.db #0xf0	; 240
   5F52 F0                  130 	.db #0xf0	; 240
   5F53 F0                  131 	.db #0xf0	; 240
   5F54 F0                  132 	.db #0xf0	; 240
   5F55 F0                  133 	.db #0xf0	; 240
   5F56 F0                  134 	.db #0xf0	; 240
   5F57 F0                  135 	.db #0xf0	; 240
   5F58 F0                  136 	.db #0xf0	; 240
   5F59 F0                  137 	.db #0xf0	; 240
   5F5A F0                  138 	.db #0xf0	; 240
   5F5B F0                  139 	.db #0xf0	; 240
   5F5C F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5F5D                     145 _projectilefire::
   5F5D DD E5         [15]  146 	push	ix
   5F5F DD 21 00 00   [14]  147 	ld	ix,#0
   5F63 DD 39         [15]  148 	add	ix,sp
   5F65 F5            [11]  149 	push	af
   5F66 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5F67 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5F6A DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5F6D CA 16 60      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5F70 DD 4E 04      [19]  157 	ld	c,4 (ix)
   5F73 DD 46 05      [19]  158 	ld	b,5 (ix)
   5F76 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5F79 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5F7A 59            [ 4]  162 	ld	e, c
   5F7B 50            [ 4]  163 	ld	d, b
   5F7C 13            [ 6]  164 	inc	de
   5F7D DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5F80 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5F81 21 02 00      [10]  168 	ld	hl, #0x0002
   5F84 09            [11]  169 	add	hl,bc
   5F85 E3            [19]  170 	ex	(sp), hl
   5F86 E1            [10]  171 	pop	hl
   5F87 E5            [11]  172 	push	hl
   5F88 DD 7E 08      [19]  173 	ld	a, 8 (ix)
   5F8B 77            [ 7]  174 	ld	(hl), a
                            175 ;src/entities/projectile.c:42: projectile->vy = 0;
   5F8C 59            [ 4]  176 	ld	e, c
   5F8D 50            [ 4]  177 	ld	d, b
   5F8E 13            [ 6]  178 	inc	de
   5F8F 13            [ 6]  179 	inc	de
   5F90 13            [ 6]  180 	inc	de
   5F91 AF            [ 4]  181 	xor	a, a
   5F92 12            [ 7]  182 	ld	(de), a
                            183 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5F93 21 09 00      [10]  184 	ld	hl, #0x0009
   5F96 09            [11]  185 	add	hl, bc
   5F97 DD 7E 09      [19]  186 	ld	a, 9 (ix)
   5F9A 77            [ 7]  187 	ld	(hl), a
                            188 ;src/entities/projectile.c:44: projectile->active = 1;
   5F9B 21 06 00      [10]  189 	ld	hl, #0x0006
   5F9E 09            [11]  190 	add	hl, bc
   5F9F 36 01         [10]  191 	ld	(hl), #0x01
                            192 ;src/entities/projectile.c:47: projectile->w = 3;
   5FA1 21 04 00      [10]  193 	ld	hl, #0x0004
   5FA4 09            [11]  194 	add	hl, bc
                            195 ;src/entities/projectile.c:48: projectile->h = 2;
   5FA5 79            [ 4]  196 	ld	a, c
   5FA6 C6 05         [ 7]  197 	add	a, #0x05
   5FA8 5F            [ 4]  198 	ld	e, a
   5FA9 78            [ 4]  199 	ld	a, b
   5FAA CE 00         [ 7]  200 	adc	a, #0x00
   5FAC 57            [ 4]  201 	ld	d, a
                            202 ;src/entities/projectile.c:49: projectile->damage = 1;
   5FAD 79            [ 4]  203 	ld	a, c
   5FAE C6 07         [ 7]  204 	add	a, #0x07
   5FB0 DD 77 FE      [19]  205 	ld	-2 (ix), a
   5FB3 78            [ 4]  206 	ld	a, b
   5FB4 CE 00         [ 7]  207 	adc	a, #0x00
   5FB6 DD 77 FF      [19]  208 	ld	-1 (ix), a
                            209 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5FB9 79            [ 4]  210 	ld	a, c
   5FBA C6 08         [ 7]  211 	add	a, #0x08
   5FBC 4F            [ 4]  212 	ld	c, a
   5FBD 78            [ 4]  213 	ld	a, b
   5FBE CE 00         [ 7]  214 	adc	a, #0x00
   5FC0 47            [ 4]  215 	ld	b, a
                            216 ;src/entities/projectile.c:46: if (weapon == 0) {
   5FC1 DD 7E 09      [19]  217 	ld	a, 9 (ix)
   5FC4 B7            [ 4]  218 	or	a, a
   5FC5 20 12         [12]  219 	jr	NZ,00107$
                            220 ;src/entities/projectile.c:47: projectile->w = 3;
   5FC7 36 03         [10]  221 	ld	(hl), #0x03
                            222 ;src/entities/projectile.c:48: projectile->h = 2;
   5FC9 3E 02         [ 7]  223 	ld	a, #0x02
   5FCB 12            [ 7]  224 	ld	(de), a
                            225 ;src/entities/projectile.c:49: projectile->damage = 1;
   5FCC DD 6E FE      [19]  226 	ld	l,-2 (ix)
   5FCF DD 66 FF      [19]  227 	ld	h,-1 (ix)
   5FD2 36 01         [10]  228 	ld	(hl), #0x01
                            229 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5FD4 3E 2D         [ 7]  230 	ld	a, #0x2d
   5FD6 02            [ 7]  231 	ld	(bc), a
   5FD7 18 3D         [12]  232 	jr	00109$
   5FD9                     233 00107$:
                            234 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5FD9 DD 7E 09      [19]  235 	ld	a, 9 (ix)
   5FDC 3D            [ 4]  236 	dec	a
   5FDD 20 12         [12]  237 	jr	NZ,00104$
                            238 ;src/entities/projectile.c:52: projectile->w = 2;
   5FDF 36 02         [10]  239 	ld	(hl), #0x02
                            240 ;src/entities/projectile.c:53: projectile->h = 3;
   5FE1 3E 03         [ 7]  241 	ld	a, #0x03
   5FE3 12            [ 7]  242 	ld	(de), a
                            243 ;src/entities/projectile.c:54: projectile->damage = 2;
   5FE4 DD 6E FE      [19]  244 	ld	l,-2 (ix)
   5FE7 DD 66 FF      [19]  245 	ld	h,-1 (ix)
   5FEA 36 02         [10]  246 	ld	(hl), #0x02
                            247 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   5FEC 3E 1C         [ 7]  248 	ld	a, #0x1c
   5FEE 02            [ 7]  249 	ld	(bc), a
   5FEF 18 25         [12]  250 	jr	00109$
   5FF1                     251 00104$:
                            252 ;src/entities/projectile.c:57: projectile->w = 4;
   5FF1 36 04         [10]  253 	ld	(hl), #0x04
                            254 ;src/entities/projectile.c:58: projectile->h = 3;
   5FF3 3E 03         [ 7]  255 	ld	a, #0x03
   5FF5 12            [ 7]  256 	ld	(de), a
                            257 ;src/entities/projectile.c:59: projectile->damage = 3;
   5FF6 DD 6E FE      [19]  258 	ld	l,-2 (ix)
   5FF9 DD 66 FF      [19]  259 	ld	h,-1 (ix)
   5FFC 36 03         [10]  260 	ld	(hl), #0x03
                            261 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   5FFE 3E 38         [ 7]  262 	ld	a, #0x38
   6000 02            [ 7]  263 	ld	(bc), a
                            264 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   6001 C1            [10]  265 	pop	bc
   6002 C5            [11]  266 	push	bc
   6003 AF            [ 4]  267 	xor	a, a
   6004 DD 96 08      [19]  268 	sub	a, 8 (ix)
   6007 E2 0C 60      [10]  269 	jp	PO, 00131$
   600A EE 80         [ 7]  270 	xor	a, #0x80
   600C                     271 00131$:
   600C F2 13 60      [10]  272 	jp	P, 00111$
   600F 3E 04         [ 7]  273 	ld	a, #0x04
   6011 18 02         [12]  274 	jr	00112$
   6013                     275 00111$:
   6013 3E FC         [ 7]  276 	ld	a, #0xfc
   6015                     277 00112$:
   6015 02            [ 7]  278 	ld	(bc), a
   6016                     279 00109$:
   6016 DD F9         [10]  280 	ld	sp, ix
   6018 DD E1         [14]  281 	pop	ix
   601A C9            [10]  282 	ret
                            283 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            284 ;	---------------------------------
                            285 ; Function projectileupdate
                            286 ; ---------------------------------
   601B                     287 _projectileupdate::
   601B DD E5         [15]  288 	push	ix
   601D DD 21 00 00   [14]  289 	ld	ix,#0
   6021 DD 39         [15]  290 	add	ix,sp
   6023 3B            [ 6]  291 	dec	sp
                            292 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   6024 DD 7E 05      [19]  293 	ld	a, 5 (ix)
   6027 DD B6 04      [19]  294 	or	a,4 (ix)
   602A 28 4A         [12]  295 	jr	Z,00109$
   602C DD 5E 04      [19]  296 	ld	e,4 (ix)
   602F DD 56 05      [19]  297 	ld	d,5 (ix)
   6032 FD 21 06 00   [14]  298 	ld	iy, #0x0006
   6036 FD 19         [15]  299 	add	iy, de
   6038 FD 7E 00      [19]  300 	ld	a, 0 (iy)
   603B B7            [ 4]  301 	or	a, a
                            302 ;src/entities/projectile.c:67: return;
   603C 28 38         [12]  303 	jr	Z,00109$
                            304 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   603E 1A            [ 7]  305 	ld	a, (de)
   603F 4F            [ 4]  306 	ld	c, a
   6040 6B            [ 4]  307 	ld	l, e
   6041 62            [ 4]  308 	ld	h, d
   6042 23            [ 6]  309 	inc	hl
   6043 23            [ 6]  310 	inc	hl
   6044 6E            [ 7]  311 	ld	l, (hl)
   6045 09            [11]  312 	add	hl, bc
   6046 7D            [ 4]  313 	ld	a, l
   6047 12            [ 7]  314 	ld	(de), a
                            315 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   6048 4B            [ 4]  316 	ld	c, e
   6049 42            [ 4]  317 	ld	b, d
   604A 03            [ 6]  318 	inc	bc
   604B 0A            [ 7]  319 	ld	a, (bc)
   604C DD 77 FF      [19]  320 	ld	-1 (ix), a
   604F 6B            [ 4]  321 	ld	l, e
   6050 62            [ 4]  322 	ld	h, d
   6051 23            [ 6]  323 	inc	hl
   6052 23            [ 6]  324 	inc	hl
   6053 23            [ 6]  325 	inc	hl
   6054 6E            [ 7]  326 	ld	l, (hl)
   6055 DD 7E FF      [19]  327 	ld	a, -1 (ix)
   6058 85            [ 4]  328 	add	a, l
   6059 02            [ 7]  329 	ld	(bc), a
                            330 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   605A 21 08 00      [10]  331 	ld	hl, #0x0008
   605D 19            [11]  332 	add	hl,de
   605E 4D            [ 4]  333 	ld	c, l
   605F 44            [ 4]  334 	ld	b, h
   6060 0A            [ 7]  335 	ld	a, (bc)
   6061 B7            [ 4]  336 	or	a, a
   6062 28 03         [12]  337 	jr	Z,00105$
                            338 ;src/entities/projectile.c:74: projectile->lifetime--;
   6064 C6 FF         [ 7]  339 	add	a, #0xff
   6066 02            [ 7]  340 	ld	(bc), a
   6067                     341 00105$:
                            342 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   6067 1A            [ 7]  343 	ld	a, (de)
   6068 5F            [ 4]  344 	ld	e, a
   6069 3E 4E         [ 7]  345 	ld	a, #0x4e
   606B 93            [ 4]  346 	sub	a, e
   606C 38 04         [12]  347 	jr	C,00106$
   606E 0A            [ 7]  348 	ld	a, (bc)
   606F B7            [ 4]  349 	or	a, a
   6070 20 04         [12]  350 	jr	NZ,00109$
   6072                     351 00106$:
                            352 ;src/entities/projectile.c:78: projectile->active = 0;
   6072 FD 36 00 00   [19]  353 	ld	0 (iy), #0x00
   6076                     354 00109$:
   6076 33            [ 6]  355 	inc	sp
   6077 DD E1         [14]  356 	pop	ix
   6079 C9            [10]  357 	ret
                            358 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            359 ;	---------------------------------
                            360 ; Function projectilerender
                            361 ; ---------------------------------
   607A                     362 _projectilerender::
   607A DD E5         [15]  363 	push	ix
   607C DD 21 00 00   [14]  364 	ld	ix,#0
   6080 DD 39         [15]  365 	add	ix,sp
   6082 F5            [11]  366 	push	af
   6083 3B            [ 6]  367 	dec	sp
                            368 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   6084 DD 7E 05      [19]  369 	ld	a, 5 (ix)
   6087 DD B6 04      [19]  370 	or	a,4 (ix)
   608A 28 6B         [12]  371 	jr	Z,00110$
   608C DD 4E 04      [19]  372 	ld	c,4 (ix)
   608F DD 46 05      [19]  373 	ld	b,5 (ix)
   6092 C5            [11]  374 	push	bc
   6093 FD E1         [14]  375 	pop	iy
   6095 FD 7E 06      [19]  376 	ld	a, 6 (iy)
   6098 B7            [ 4]  377 	or	a, a
                            378 ;src/entities/projectile.c:87: return;
   6099 28 5C         [12]  379 	jr	Z,00110$
                            380 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   609B C5            [11]  381 	push	bc
   609C FD E1         [14]  382 	pop	iy
   609E FD 7E 09      [19]  383 	ld	a, 9 (iy)
   60A1 B7            [ 4]  384 	or	a, a
   60A2 20 0A         [12]  385 	jr	NZ,00108$
   60A4 DD 36 FE 45   [19]  386 	ld	-2 (ix), #<(_projectile_basic_sprite)
   60A8 DD 36 FF 5F   [19]  387 	ld	-1 (ix), #>(_projectile_basic_sprite)
   60AC 18 15         [12]  388 	jr	00109$
   60AE                     389 00108$:
                            390 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   60AE 3D            [ 4]  391 	dec	a
   60AF 20 0A         [12]  392 	jr	NZ,00105$
   60B1 DD 36 FE 4B   [19]  393 	ld	-2 (ix), #<(_projectile_up_sprite)
   60B5 DD 36 FF 5F   [19]  394 	ld	-1 (ix), #>(_projectile_up_sprite)
   60B9 18 08         [12]  395 	jr	00109$
   60BB                     396 00105$:
                            397 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   60BB DD 36 FE 51   [19]  398 	ld	-2 (ix), #<(_projectile_special_sprite)
   60BF DD 36 FF 5F   [19]  399 	ld	-1 (ix), #>(_projectile_special_sprite)
   60C3                     400 00109$:
                            401 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   60C3 69            [ 4]  402 	ld	l, c
   60C4 60            [ 4]  403 	ld	h, b
   60C5 23            [ 6]  404 	inc	hl
   60C6 56            [ 7]  405 	ld	d, (hl)
   60C7 0A            [ 7]  406 	ld	a, (bc)
   60C8 C5            [11]  407 	push	bc
   60C9 5F            [ 4]  408 	ld	e, a
   60CA D5            [11]  409 	push	de
   60CB 21 00 C0      [10]  410 	ld	hl, #0xc000
   60CE E5            [11]  411 	push	hl
   60CF CD A5 63      [17]  412 	call	_cpct_getScreenPtr
   60D2 EB            [ 4]  413 	ex	de,hl
   60D3 C1            [10]  414 	pop	bc
                            415 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   60D4 C5            [11]  416 	push	bc
   60D5 FD E1         [14]  417 	pop	iy
   60D7 FD 7E 05      [19]  418 	ld	a, 5 (iy)
   60DA DD 77 FD      [19]  419 	ld	-3 (ix), a
   60DD 69            [ 4]  420 	ld	l, c
   60DE 60            [ 4]  421 	ld	h, b
   60DF 01 04 00      [10]  422 	ld	bc, #0x0004
   60E2 09            [11]  423 	add	hl, bc
   60E3 4E            [ 7]  424 	ld	c, (hl)
   60E4 D5            [11]  425 	push	de
   60E5 FD E1         [14]  426 	pop	iy
   60E7 DD 5E FE      [19]  427 	ld	e,-2 (ix)
   60EA DD 56 FF      [19]  428 	ld	d,-1 (ix)
   60ED DD 46 FD      [19]  429 	ld	b, -3 (ix)
   60F0 C5            [11]  430 	push	bc
   60F1 FD E5         [15]  431 	push	iy
   60F3 D5            [11]  432 	push	de
   60F4 CD D6 61      [17]  433 	call	_cpct_drawSprite
   60F7                     434 00110$:
   60F7 DD F9         [10]  435 	ld	sp, ix
   60F9 DD E1         [14]  436 	pop	ix
   60FB C9            [10]  437 	ret
                            438 	.area _CODE
                            439 	.area _INITIALIZER
                            440 	.area _CABS (ABS)
