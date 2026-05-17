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
   5F9B                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5F9B 21 03 00      [10]   54 	ld	hl, #2+1
   5F9E 39            [11]   55 	add	hl, sp
   5F9F 7E            [ 7]   56 	ld	a, (hl)
   5FA0 2B            [ 6]   57 	dec	hl
   5FA1 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5FA2 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5FA3 D1            [10]   62 	pop	de
   5FA4 C1            [10]   63 	pop	bc
   5FA5 C5            [11]   64 	push	bc
   5FA6 D5            [11]   65 	push	de
   5FA7 AF            [ 4]   66 	xor	a, a
   5FA8 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5FA9 59            [ 4]   69 	ld	e, c
   5FAA 50            [ 4]   70 	ld	d, b
   5FAB 13            [ 6]   71 	inc	de
   5FAC AF            [ 4]   72 	xor	a, a
   5FAD 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5FAE 59            [ 4]   75 	ld	e, c
   5FAF 50            [ 4]   76 	ld	d, b
   5FB0 13            [ 6]   77 	inc	de
   5FB1 13            [ 6]   78 	inc	de
   5FB2 AF            [ 4]   79 	xor	a, a
   5FB3 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5FB4 59            [ 4]   82 	ld	e, c
   5FB5 50            [ 4]   83 	ld	d, b
   5FB6 13            [ 6]   84 	inc	de
   5FB7 13            [ 6]   85 	inc	de
   5FB8 13            [ 6]   86 	inc	de
   5FB9 AF            [ 4]   87 	xor	a, a
   5FBA 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5FBB 21 04 00      [10]   90 	ld	hl, #0x0004
   5FBE 09            [11]   91 	add	hl, bc
   5FBF 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5FC1 21 05 00      [10]   94 	ld	hl, #0x0005
   5FC4 09            [11]   95 	add	hl, bc
   5FC5 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5FC7 21 06 00      [10]   98 	ld	hl, #0x0006
   5FCA 09            [11]   99 	add	hl, bc
   5FCB 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5FCD 21 07 00      [10]  102 	ld	hl, #0x0007
   5FD0 09            [11]  103 	add	hl, bc
   5FD1 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5FD3 21 08 00      [10]  106 	ld	hl, #0x0008
   5FD6 09            [11]  107 	add	hl, bc
   5FD7 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5FD9 21 09 00      [10]  110 	ld	hl, #0x0009
   5FDC 09            [11]  111 	add	hl, bc
   5FDD 36 00         [10]  112 	ld	(hl), #0x00
   5FDF C9            [10]  113 	ret
   5FE0                     114 _projectile_basic_sprite:
   5FE0 FF                  115 	.db #0xff	; 255
   5FE1 FF                  116 	.db #0xff	; 255
   5FE2 FF                  117 	.db #0xff	; 255
   5FE3 FF                  118 	.db #0xff	; 255
   5FE4 FF                  119 	.db #0xff	; 255
   5FE5 FF                  120 	.db #0xff	; 255
   5FE6                     121 _projectile_up_sprite:
   5FE6 CF                  122 	.db #0xcf	; 207
   5FE7 CF                  123 	.db #0xcf	; 207
   5FE8 CF                  124 	.db #0xcf	; 207
   5FE9 CF                  125 	.db #0xcf	; 207
   5FEA CF                  126 	.db #0xcf	; 207
   5FEB CF                  127 	.db #0xcf	; 207
   5FEC                     128 _projectile_special_sprite:
   5FEC F0                  129 	.db #0xf0	; 240
   5FED F0                  130 	.db #0xf0	; 240
   5FEE F0                  131 	.db #0xf0	; 240
   5FEF F0                  132 	.db #0xf0	; 240
   5FF0 F0                  133 	.db #0xf0	; 240
   5FF1 F0                  134 	.db #0xf0	; 240
   5FF2 F0                  135 	.db #0xf0	; 240
   5FF3 F0                  136 	.db #0xf0	; 240
   5FF4 F0                  137 	.db #0xf0	; 240
   5FF5 F0                  138 	.db #0xf0	; 240
   5FF6 F0                  139 	.db #0xf0	; 240
   5FF7 F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5FF8                     145 _projectilefire::
   5FF8 DD E5         [15]  146 	push	ix
   5FFA DD 21 00 00   [14]  147 	ld	ix,#0
   5FFE DD 39         [15]  148 	add	ix,sp
   6000 F5            [11]  149 	push	af
   6001 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   6002 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   6005 DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   6008 CA AA 60      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   600B DD 4E 04      [19]  157 	ld	c,4 (ix)
   600E DD 46 05      [19]  158 	ld	b,5 (ix)
   6011 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   6014 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   6015 59            [ 4]  162 	ld	e, c
   6016 50            [ 4]  163 	ld	d, b
   6017 13            [ 6]  164 	inc	de
   6018 DD 7E 07      [19]  165 	ld	a, 7 (ix)
   601B 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   601C 21 02 00      [10]  168 	ld	hl, #0x0002
   601F 09            [11]  169 	add	hl,bc
   6020 DD 75 FE      [19]  170 	ld	-2 (ix), l
   6023 DD 74 FF      [19]  171 	ld	-1 (ix), h
   6026 DD 7E 08      [19]  172 	ld	a, 8 (ix)
   6029 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   602A 59            [ 4]  175 	ld	e, c
   602B 50            [ 4]  176 	ld	d, b
   602C 13            [ 6]  177 	inc	de
   602D 13            [ 6]  178 	inc	de
   602E 13            [ 6]  179 	inc	de
   602F AF            [ 4]  180 	xor	a, a
   6030 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   6031 21 09 00      [10]  183 	ld	hl, #0x0009
   6034 09            [11]  184 	add	hl, bc
   6035 DD 7E 09      [19]  185 	ld	a, 9 (ix)
   6038 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   6039 21 06 00      [10]  188 	ld	hl, #0x0006
   603C 09            [11]  189 	add	hl, bc
   603D 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   603F 21 04 00      [10]  192 	ld	hl, #0x0004
   6042 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   6043 79            [ 4]  195 	ld	a, c
   6044 C6 05         [ 7]  196 	add	a, #0x05
   6046 5F            [ 4]  197 	ld	e, a
   6047 78            [ 4]  198 	ld	a, b
   6048 CE 00         [ 7]  199 	adc	a, #0x00
   604A 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   604B 79            [ 4]  202 	ld	a, c
   604C C6 07         [ 7]  203 	add	a, #0x07
   604E DD 77 FC      [19]  204 	ld	-4 (ix), a
   6051 78            [ 4]  205 	ld	a, b
   6052 CE 00         [ 7]  206 	adc	a, #0x00
   6054 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   6057 79            [ 4]  209 	ld	a, c
   6058 C6 08         [ 7]  210 	add	a, #0x08
   605A 4F            [ 4]  211 	ld	c, a
   605B 78            [ 4]  212 	ld	a, b
   605C CE 00         [ 7]  213 	adc	a, #0x00
   605E 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   605F DD 7E 09      [19]  216 	ld	a, 9 (ix)
   6062 B7            [ 4]  217 	or	a, a
   6063 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   6065 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   6067 3E 02         [ 7]  222 	ld	a, #0x02
   6069 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   606A E1            [10]  225 	pop	hl
   606B E5            [11]  226 	push	hl
   606C 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   606E 3E 2D         [ 7]  229 	ld	a, #0x2d
   6070 02            [ 7]  230 	ld	(bc), a
   6071 18 37         [12]  231 	jr	00109$
   6073                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   6073 DD 7E 09      [19]  234 	ld	a, 9 (ix)
   6076 3D            [ 4]  235 	dec	a
   6077 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   6079 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   607B 3E 03         [ 7]  240 	ld	a, #0x03
   607D 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   607E E1            [10]  243 	pop	hl
   607F E5            [11]  244 	push	hl
   6080 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   6082 3E 1C         [ 7]  247 	ld	a, #0x1c
   6084 02            [ 7]  248 	ld	(bc), a
   6085 18 23         [12]  249 	jr	00109$
   6087                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   6087 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   6089 3E 03         [ 7]  254 	ld	a, #0x03
   608B 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   608C E1            [10]  257 	pop	hl
   608D E5            [11]  258 	push	hl
   608E 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   6090 3E 38         [ 7]  261 	ld	a, #0x38
   6092 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   6093 D1            [10]  264 	pop	de
   6094 C1            [10]  265 	pop	bc
   6095 C5            [11]  266 	push	bc
   6096 D5            [11]  267 	push	de
   6097 AF            [ 4]  268 	xor	a, a
   6098 DD 96 08      [19]  269 	sub	a, 8 (ix)
   609B E2 A0 60      [10]  270 	jp	PO, 00131$
   609E EE 80         [ 7]  271 	xor	a, #0x80
   60A0                     272 00131$:
   60A0 F2 A7 60      [10]  273 	jp	P, 00111$
   60A3 3E 04         [ 7]  274 	ld	a, #0x04
   60A5 18 02         [12]  275 	jr	00112$
   60A7                     276 00111$:
   60A7 3E FC         [ 7]  277 	ld	a, #0xfc
   60A9                     278 00112$:
   60A9 02            [ 7]  279 	ld	(bc), a
   60AA                     280 00109$:
   60AA DD F9         [10]  281 	ld	sp, ix
   60AC DD E1         [14]  282 	pop	ix
   60AE C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   60AF                     288 _projectileupdate::
   60AF DD E5         [15]  289 	push	ix
   60B1 DD 21 00 00   [14]  290 	ld	ix,#0
   60B5 DD 39         [15]  291 	add	ix,sp
   60B7 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   60B8 DD 7E 05      [19]  294 	ld	a, 5 (ix)
   60BB DD B6 04      [19]  295 	or	a,4 (ix)
   60BE 28 4A         [12]  296 	jr	Z,00109$
   60C0 DD 5E 04      [19]  297 	ld	e,4 (ix)
   60C3 DD 56 05      [19]  298 	ld	d,5 (ix)
   60C6 FD 21 06 00   [14]  299 	ld	iy, #0x0006
   60CA FD 19         [15]  300 	add	iy, de
   60CC FD 7E 00      [19]  301 	ld	a, 0 (iy)
   60CF B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   60D0 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   60D2 1A            [ 7]  306 	ld	a, (de)
   60D3 4F            [ 4]  307 	ld	c, a
   60D4 6B            [ 4]  308 	ld	l, e
   60D5 62            [ 4]  309 	ld	h, d
   60D6 23            [ 6]  310 	inc	hl
   60D7 23            [ 6]  311 	inc	hl
   60D8 6E            [ 7]  312 	ld	l, (hl)
   60D9 09            [11]  313 	add	hl, bc
   60DA 7D            [ 4]  314 	ld	a, l
   60DB 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   60DC 4B            [ 4]  317 	ld	c, e
   60DD 42            [ 4]  318 	ld	b, d
   60DE 03            [ 6]  319 	inc	bc
   60DF 0A            [ 7]  320 	ld	a, (bc)
   60E0 DD 77 FF      [19]  321 	ld	-1 (ix), a
   60E3 6B            [ 4]  322 	ld	l, e
   60E4 62            [ 4]  323 	ld	h, d
   60E5 23            [ 6]  324 	inc	hl
   60E6 23            [ 6]  325 	inc	hl
   60E7 23            [ 6]  326 	inc	hl
   60E8 6E            [ 7]  327 	ld	l, (hl)
   60E9 DD 7E FF      [19]  328 	ld	a, -1 (ix)
   60EC 85            [ 4]  329 	add	a, l
   60ED 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   60EE 21 08 00      [10]  332 	ld	hl, #0x0008
   60F1 19            [11]  333 	add	hl,de
   60F2 4D            [ 4]  334 	ld	c, l
   60F3 44            [ 4]  335 	ld	b, h
   60F4 0A            [ 7]  336 	ld	a, (bc)
   60F5 B7            [ 4]  337 	or	a, a
   60F6 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   60F8 C6 FF         [ 7]  340 	add	a, #0xff
   60FA 02            [ 7]  341 	ld	(bc), a
   60FB                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   60FB 1A            [ 7]  344 	ld	a, (de)
   60FC 5F            [ 4]  345 	ld	e, a
   60FD 3E 4E         [ 7]  346 	ld	a, #0x4e
   60FF 93            [ 4]  347 	sub	a, e
   6100 38 04         [12]  348 	jr	C,00106$
   6102 0A            [ 7]  349 	ld	a, (bc)
   6103 B7            [ 4]  350 	or	a, a
   6104 20 04         [12]  351 	jr	NZ,00109$
   6106                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   6106 FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   610A                     355 00109$:
   610A 33            [ 6]  356 	inc	sp
   610B DD E1         [14]  357 	pop	ix
   610D C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   610E                     363 _projectilerender::
   610E DD E5         [15]  364 	push	ix
   6110 DD 21 00 00   [14]  365 	ld	ix,#0
   6114 DD 39         [15]  366 	add	ix,sp
   6116 F5            [11]  367 	push	af
   6117 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   6118 DD 7E 05      [19]  370 	ld	a, 5 (ix)
   611B DD B6 04      [19]  371 	or	a,4 (ix)
   611E 28 6B         [12]  372 	jr	Z,00110$
   6120 DD 4E 04      [19]  373 	ld	c,4 (ix)
   6123 DD 46 05      [19]  374 	ld	b,5 (ix)
   6126 C5            [11]  375 	push	bc
   6127 FD E1         [14]  376 	pop	iy
   6129 FD 7E 06      [19]  377 	ld	a, 6 (iy)
   612C B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   612D 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   612F C5            [11]  382 	push	bc
   6130 FD E1         [14]  383 	pop	iy
   6132 FD 7E 09      [19]  384 	ld	a, 9 (iy)
   6135 B7            [ 4]  385 	or	a, a
   6136 20 0A         [12]  386 	jr	NZ,00108$
   6138 DD 36 FE E0   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   613C DD 36 FF 5F   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   6140 18 15         [12]  389 	jr	00109$
   6142                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   6142 3D            [ 4]  392 	dec	a
   6143 20 0A         [12]  393 	jr	NZ,00105$
   6145 DD 36 FE E6   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   6149 DD 36 FF 5F   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   614D 18 08         [12]  396 	jr	00109$
   614F                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   614F DD 36 FE EC   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   6153 DD 36 FF 5F   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   6157                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   6157 69            [ 4]  403 	ld	l, c
   6158 60            [ 4]  404 	ld	h, b
   6159 23            [ 6]  405 	inc	hl
   615A 56            [ 7]  406 	ld	d, (hl)
   615B 0A            [ 7]  407 	ld	a, (bc)
   615C C5            [11]  408 	push	bc
   615D 5F            [ 4]  409 	ld	e, a
   615E D5            [11]  410 	push	de
   615F 21 00 C0      [10]  411 	ld	hl, #0xc000
   6162 E5            [11]  412 	push	hl
   6163 CD 39 64      [17]  413 	call	_cpct_getScreenPtr
   6166 EB            [ 4]  414 	ex	de,hl
   6167 C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   6168 C5            [11]  417 	push	bc
   6169 FD E1         [14]  418 	pop	iy
   616B FD 7E 05      [19]  419 	ld	a, 5 (iy)
   616E DD 77 FD      [19]  420 	ld	-3 (ix), a
   6171 69            [ 4]  421 	ld	l, c
   6172 60            [ 4]  422 	ld	h, b
   6173 01 04 00      [10]  423 	ld	bc, #0x0004
   6176 09            [11]  424 	add	hl, bc
   6177 4E            [ 7]  425 	ld	c, (hl)
   6178 D5            [11]  426 	push	de
   6179 FD E1         [14]  427 	pop	iy
   617B DD 5E FE      [19]  428 	ld	e,-2 (ix)
   617E DD 56 FF      [19]  429 	ld	d,-1 (ix)
   6181 DD 46 FD      [19]  430 	ld	b, -3 (ix)
   6184 C5            [11]  431 	push	bc
   6185 FD E5         [15]  432 	push	iy
   6187 D5            [11]  433 	push	de
   6188 CD 6A 62      [17]  434 	call	_cpct_drawSprite
   618B                     435 00110$:
   618B DD F9         [10]  436 	ld	sp, ix
   618D DD E1         [14]  437 	pop	ix
   618F C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
