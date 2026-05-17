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
   5F1D                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5F1D 21 03 00      [10]   54 	ld	hl, #2+1
   5F20 39            [11]   55 	add	hl, sp
   5F21 7E            [ 7]   56 	ld	a, (hl)
   5F22 2B            [ 6]   57 	dec	hl
   5F23 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5F24 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5F25 D1            [10]   62 	pop	de
   5F26 C1            [10]   63 	pop	bc
   5F27 C5            [11]   64 	push	bc
   5F28 D5            [11]   65 	push	de
   5F29 AF            [ 4]   66 	xor	a, a
   5F2A 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5F2B 59            [ 4]   69 	ld	e, c
   5F2C 50            [ 4]   70 	ld	d, b
   5F2D 13            [ 6]   71 	inc	de
   5F2E AF            [ 4]   72 	xor	a, a
   5F2F 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5F30 59            [ 4]   75 	ld	e, c
   5F31 50            [ 4]   76 	ld	d, b
   5F32 13            [ 6]   77 	inc	de
   5F33 13            [ 6]   78 	inc	de
   5F34 AF            [ 4]   79 	xor	a, a
   5F35 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5F36 59            [ 4]   82 	ld	e, c
   5F37 50            [ 4]   83 	ld	d, b
   5F38 13            [ 6]   84 	inc	de
   5F39 13            [ 6]   85 	inc	de
   5F3A 13            [ 6]   86 	inc	de
   5F3B AF            [ 4]   87 	xor	a, a
   5F3C 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5F3D 21 04 00      [10]   90 	ld	hl, #0x0004
   5F40 09            [11]   91 	add	hl, bc
   5F41 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5F43 21 05 00      [10]   94 	ld	hl, #0x0005
   5F46 09            [11]   95 	add	hl, bc
   5F47 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5F49 21 06 00      [10]   98 	ld	hl, #0x0006
   5F4C 09            [11]   99 	add	hl, bc
   5F4D 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5F4F 21 07 00      [10]  102 	ld	hl, #0x0007
   5F52 09            [11]  103 	add	hl, bc
   5F53 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5F55 21 08 00      [10]  106 	ld	hl, #0x0008
   5F58 09            [11]  107 	add	hl, bc
   5F59 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5F5B 21 09 00      [10]  110 	ld	hl, #0x0009
   5F5E 09            [11]  111 	add	hl, bc
   5F5F 36 00         [10]  112 	ld	(hl), #0x00
   5F61 C9            [10]  113 	ret
   5F62                     114 _projectile_basic_sprite:
   5F62 FF                  115 	.db #0xff	; 255
   5F63 FF                  116 	.db #0xff	; 255
   5F64 FF                  117 	.db #0xff	; 255
   5F65 FF                  118 	.db #0xff	; 255
   5F66 FF                  119 	.db #0xff	; 255
   5F67 FF                  120 	.db #0xff	; 255
   5F68                     121 _projectile_up_sprite:
   5F68 CF                  122 	.db #0xcf	; 207
   5F69 CF                  123 	.db #0xcf	; 207
   5F6A CF                  124 	.db #0xcf	; 207
   5F6B CF                  125 	.db #0xcf	; 207
   5F6C CF                  126 	.db #0xcf	; 207
   5F6D CF                  127 	.db #0xcf	; 207
   5F6E                     128 _projectile_special_sprite:
   5F6E F0                  129 	.db #0xf0	; 240
   5F6F F0                  130 	.db #0xf0	; 240
   5F70 F0                  131 	.db #0xf0	; 240
   5F71 F0                  132 	.db #0xf0	; 240
   5F72 F0                  133 	.db #0xf0	; 240
   5F73 F0                  134 	.db #0xf0	; 240
   5F74 F0                  135 	.db #0xf0	; 240
   5F75 F0                  136 	.db #0xf0	; 240
   5F76 F0                  137 	.db #0xf0	; 240
   5F77 F0                  138 	.db #0xf0	; 240
   5F78 F0                  139 	.db #0xf0	; 240
   5F79 F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5F7A                     145 _projectilefire::
   5F7A DD E5         [15]  146 	push	ix
   5F7C DD 21 00 00   [14]  147 	ld	ix,#0
   5F80 DD 39         [15]  148 	add	ix,sp
   5F82 F5            [11]  149 	push	af
   5F83 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5F84 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5F87 DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5F8A CA 2C 60      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5F8D DD 4E 04      [19]  157 	ld	c,4 (ix)
   5F90 DD 46 05      [19]  158 	ld	b,5 (ix)
   5F93 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5F96 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5F97 59            [ 4]  162 	ld	e, c
   5F98 50            [ 4]  163 	ld	d, b
   5F99 13            [ 6]  164 	inc	de
   5F9A DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5F9D 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5F9E 21 02 00      [10]  168 	ld	hl, #0x0002
   5FA1 09            [11]  169 	add	hl,bc
   5FA2 DD 75 FE      [19]  170 	ld	-2 (ix), l
   5FA5 DD 74 FF      [19]  171 	ld	-1 (ix), h
   5FA8 DD 7E 08      [19]  172 	ld	a, 8 (ix)
   5FAB 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   5FAC 59            [ 4]  175 	ld	e, c
   5FAD 50            [ 4]  176 	ld	d, b
   5FAE 13            [ 6]  177 	inc	de
   5FAF 13            [ 6]  178 	inc	de
   5FB0 13            [ 6]  179 	inc	de
   5FB1 AF            [ 4]  180 	xor	a, a
   5FB2 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5FB3 21 09 00      [10]  183 	ld	hl, #0x0009
   5FB6 09            [11]  184 	add	hl, bc
   5FB7 DD 7E 09      [19]  185 	ld	a, 9 (ix)
   5FBA 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   5FBB 21 06 00      [10]  188 	ld	hl, #0x0006
   5FBE 09            [11]  189 	add	hl, bc
   5FBF 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   5FC1 21 04 00      [10]  192 	ld	hl, #0x0004
   5FC4 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   5FC5 79            [ 4]  195 	ld	a, c
   5FC6 C6 05         [ 7]  196 	add	a, #0x05
   5FC8 5F            [ 4]  197 	ld	e, a
   5FC9 78            [ 4]  198 	ld	a, b
   5FCA CE 00         [ 7]  199 	adc	a, #0x00
   5FCC 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   5FCD 79            [ 4]  202 	ld	a, c
   5FCE C6 07         [ 7]  203 	add	a, #0x07
   5FD0 DD 77 FC      [19]  204 	ld	-4 (ix), a
   5FD3 78            [ 4]  205 	ld	a, b
   5FD4 CE 00         [ 7]  206 	adc	a, #0x00
   5FD6 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5FD9 79            [ 4]  209 	ld	a, c
   5FDA C6 08         [ 7]  210 	add	a, #0x08
   5FDC 4F            [ 4]  211 	ld	c, a
   5FDD 78            [ 4]  212 	ld	a, b
   5FDE CE 00         [ 7]  213 	adc	a, #0x00
   5FE0 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   5FE1 DD 7E 09      [19]  216 	ld	a, 9 (ix)
   5FE4 B7            [ 4]  217 	or	a, a
   5FE5 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   5FE7 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   5FE9 3E 02         [ 7]  222 	ld	a, #0x02
   5FEB 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   5FEC E1            [10]  225 	pop	hl
   5FED E5            [11]  226 	push	hl
   5FEE 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5FF0 3E 2D         [ 7]  229 	ld	a, #0x2d
   5FF2 02            [ 7]  230 	ld	(bc), a
   5FF3 18 37         [12]  231 	jr	00109$
   5FF5                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5FF5 DD 7E 09      [19]  234 	ld	a, 9 (ix)
   5FF8 3D            [ 4]  235 	dec	a
   5FF9 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   5FFB 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   5FFD 3E 03         [ 7]  240 	ld	a, #0x03
   5FFF 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   6000 E1            [10]  243 	pop	hl
   6001 E5            [11]  244 	push	hl
   6002 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   6004 3E 1C         [ 7]  247 	ld	a, #0x1c
   6006 02            [ 7]  248 	ld	(bc), a
   6007 18 23         [12]  249 	jr	00109$
   6009                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   6009 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   600B 3E 03         [ 7]  254 	ld	a, #0x03
   600D 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   600E E1            [10]  257 	pop	hl
   600F E5            [11]  258 	push	hl
   6010 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   6012 3E 38         [ 7]  261 	ld	a, #0x38
   6014 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   6015 D1            [10]  264 	pop	de
   6016 C1            [10]  265 	pop	bc
   6017 C5            [11]  266 	push	bc
   6018 D5            [11]  267 	push	de
   6019 AF            [ 4]  268 	xor	a, a
   601A DD 96 08      [19]  269 	sub	a, 8 (ix)
   601D E2 22 60      [10]  270 	jp	PO, 00131$
   6020 EE 80         [ 7]  271 	xor	a, #0x80
   6022                     272 00131$:
   6022 F2 29 60      [10]  273 	jp	P, 00111$
   6025 3E 04         [ 7]  274 	ld	a, #0x04
   6027 18 02         [12]  275 	jr	00112$
   6029                     276 00111$:
   6029 3E FC         [ 7]  277 	ld	a, #0xfc
   602B                     278 00112$:
   602B 02            [ 7]  279 	ld	(bc), a
   602C                     280 00109$:
   602C DD F9         [10]  281 	ld	sp, ix
   602E DD E1         [14]  282 	pop	ix
   6030 C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   6031                     288 _projectileupdate::
   6031 DD E5         [15]  289 	push	ix
   6033 DD 21 00 00   [14]  290 	ld	ix,#0
   6037 DD 39         [15]  291 	add	ix,sp
   6039 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   603A DD 7E 05      [19]  294 	ld	a, 5 (ix)
   603D DD B6 04      [19]  295 	or	a,4 (ix)
   6040 28 4A         [12]  296 	jr	Z,00109$
   6042 DD 5E 04      [19]  297 	ld	e,4 (ix)
   6045 DD 56 05      [19]  298 	ld	d,5 (ix)
   6048 FD 21 06 00   [14]  299 	ld	iy, #0x0006
   604C FD 19         [15]  300 	add	iy, de
   604E FD 7E 00      [19]  301 	ld	a, 0 (iy)
   6051 B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   6052 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   6054 1A            [ 7]  306 	ld	a, (de)
   6055 4F            [ 4]  307 	ld	c, a
   6056 6B            [ 4]  308 	ld	l, e
   6057 62            [ 4]  309 	ld	h, d
   6058 23            [ 6]  310 	inc	hl
   6059 23            [ 6]  311 	inc	hl
   605A 6E            [ 7]  312 	ld	l, (hl)
   605B 09            [11]  313 	add	hl, bc
   605C 7D            [ 4]  314 	ld	a, l
   605D 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   605E 4B            [ 4]  317 	ld	c, e
   605F 42            [ 4]  318 	ld	b, d
   6060 03            [ 6]  319 	inc	bc
   6061 0A            [ 7]  320 	ld	a, (bc)
   6062 DD 77 FF      [19]  321 	ld	-1 (ix), a
   6065 6B            [ 4]  322 	ld	l, e
   6066 62            [ 4]  323 	ld	h, d
   6067 23            [ 6]  324 	inc	hl
   6068 23            [ 6]  325 	inc	hl
   6069 23            [ 6]  326 	inc	hl
   606A 6E            [ 7]  327 	ld	l, (hl)
   606B DD 7E FF      [19]  328 	ld	a, -1 (ix)
   606E 85            [ 4]  329 	add	a, l
   606F 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   6070 21 08 00      [10]  332 	ld	hl, #0x0008
   6073 19            [11]  333 	add	hl,de
   6074 4D            [ 4]  334 	ld	c, l
   6075 44            [ 4]  335 	ld	b, h
   6076 0A            [ 7]  336 	ld	a, (bc)
   6077 B7            [ 4]  337 	or	a, a
   6078 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   607A C6 FF         [ 7]  340 	add	a, #0xff
   607C 02            [ 7]  341 	ld	(bc), a
   607D                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   607D 1A            [ 7]  344 	ld	a, (de)
   607E 5F            [ 4]  345 	ld	e, a
   607F 3E 4E         [ 7]  346 	ld	a, #0x4e
   6081 93            [ 4]  347 	sub	a, e
   6082 38 04         [12]  348 	jr	C,00106$
   6084 0A            [ 7]  349 	ld	a, (bc)
   6085 B7            [ 4]  350 	or	a, a
   6086 20 04         [12]  351 	jr	NZ,00109$
   6088                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   6088 FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   608C                     355 00109$:
   608C 33            [ 6]  356 	inc	sp
   608D DD E1         [14]  357 	pop	ix
   608F C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   6090                     363 _projectilerender::
   6090 DD E5         [15]  364 	push	ix
   6092 DD 21 00 00   [14]  365 	ld	ix,#0
   6096 DD 39         [15]  366 	add	ix,sp
   6098 F5            [11]  367 	push	af
   6099 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   609A DD 7E 05      [19]  370 	ld	a, 5 (ix)
   609D DD B6 04      [19]  371 	or	a,4 (ix)
   60A0 28 6B         [12]  372 	jr	Z,00110$
   60A2 DD 4E 04      [19]  373 	ld	c,4 (ix)
   60A5 DD 46 05      [19]  374 	ld	b,5 (ix)
   60A8 C5            [11]  375 	push	bc
   60A9 FD E1         [14]  376 	pop	iy
   60AB FD 7E 06      [19]  377 	ld	a, 6 (iy)
   60AE B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   60AF 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   60B1 C5            [11]  382 	push	bc
   60B2 FD E1         [14]  383 	pop	iy
   60B4 FD 7E 09      [19]  384 	ld	a, 9 (iy)
   60B7 B7            [ 4]  385 	or	a, a
   60B8 20 0A         [12]  386 	jr	NZ,00108$
   60BA DD 36 FE 62   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   60BE DD 36 FF 5F   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   60C2 18 15         [12]  389 	jr	00109$
   60C4                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   60C4 3D            [ 4]  392 	dec	a
   60C5 20 0A         [12]  393 	jr	NZ,00105$
   60C7 DD 36 FE 68   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   60CB DD 36 FF 5F   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   60CF 18 08         [12]  396 	jr	00109$
   60D1                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   60D1 DD 36 FE 6E   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   60D5 DD 36 FF 5F   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   60D9                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   60D9 69            [ 4]  403 	ld	l, c
   60DA 60            [ 4]  404 	ld	h, b
   60DB 23            [ 6]  405 	inc	hl
   60DC 56            [ 7]  406 	ld	d, (hl)
   60DD 0A            [ 7]  407 	ld	a, (bc)
   60DE C5            [11]  408 	push	bc
   60DF 5F            [ 4]  409 	ld	e, a
   60E0 D5            [11]  410 	push	de
   60E1 21 00 C0      [10]  411 	ld	hl, #0xc000
   60E4 E5            [11]  412 	push	hl
   60E5 CD BB 63      [17]  413 	call	_cpct_getScreenPtr
   60E8 EB            [ 4]  414 	ex	de,hl
   60E9 C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   60EA C5            [11]  417 	push	bc
   60EB FD E1         [14]  418 	pop	iy
   60ED FD 7E 05      [19]  419 	ld	a, 5 (iy)
   60F0 DD 77 FD      [19]  420 	ld	-3 (ix), a
   60F3 69            [ 4]  421 	ld	l, c
   60F4 60            [ 4]  422 	ld	h, b
   60F5 01 04 00      [10]  423 	ld	bc, #0x0004
   60F8 09            [11]  424 	add	hl, bc
   60F9 4E            [ 7]  425 	ld	c, (hl)
   60FA D5            [11]  426 	push	de
   60FB FD E1         [14]  427 	pop	iy
   60FD DD 5E FE      [19]  428 	ld	e,-2 (ix)
   6100 DD 56 FF      [19]  429 	ld	d,-1 (ix)
   6103 DD 46 FD      [19]  430 	ld	b, -3 (ix)
   6106 C5            [11]  431 	push	bc
   6107 FD E5         [15]  432 	push	iy
   6109 D5            [11]  433 	push	de
   610A CD EC 61      [17]  434 	call	_cpct_drawSprite
   610D                     435 00110$:
   610D DD F9         [10]  436 	ld	sp, ix
   610F DD E1         [14]  437 	pop	ix
   6111 C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
