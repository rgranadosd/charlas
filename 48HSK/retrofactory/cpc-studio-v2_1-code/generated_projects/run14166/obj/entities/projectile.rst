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
   5D8C                      52 _projectileinit::
                             53 ;src/entities/projectile.c:18: if (!projectile) {
   5D8C 21 03 00      [10]   54 	ld	hl, #2+1
   5D8F 39            [11]   55 	add	hl, sp
   5D90 7E            [ 7]   56 	ld	a, (hl)
   5D91 2B            [ 6]   57 	dec	hl
   5D92 B6            [ 7]   58 	or	a,(hl)
                             59 ;src/entities/projectile.c:19: return;
   5D93 C8            [11]   60 	ret	Z
                             61 ;src/entities/projectile.c:22: projectile->x = 0;
   5D94 D1            [10]   62 	pop	de
   5D95 C1            [10]   63 	pop	bc
   5D96 C5            [11]   64 	push	bc
   5D97 D5            [11]   65 	push	de
   5D98 AF            [ 4]   66 	xor	a, a
   5D99 02            [ 7]   67 	ld	(bc), a
                             68 ;src/entities/projectile.c:23: projectile->y = 0;
   5D9A 59            [ 4]   69 	ld	e, c
   5D9B 50            [ 4]   70 	ld	d, b
   5D9C 13            [ 6]   71 	inc	de
   5D9D AF            [ 4]   72 	xor	a, a
   5D9E 12            [ 7]   73 	ld	(de), a
                             74 ;src/entities/projectile.c:24: projectile->vx = 0;
   5D9F 59            [ 4]   75 	ld	e, c
   5DA0 50            [ 4]   76 	ld	d, b
   5DA1 13            [ 6]   77 	inc	de
   5DA2 13            [ 6]   78 	inc	de
   5DA3 AF            [ 4]   79 	xor	a, a
   5DA4 12            [ 7]   80 	ld	(de), a
                             81 ;src/entities/projectile.c:25: projectile->vy = 0;
   5DA5 59            [ 4]   82 	ld	e, c
   5DA6 50            [ 4]   83 	ld	d, b
   5DA7 13            [ 6]   84 	inc	de
   5DA8 13            [ 6]   85 	inc	de
   5DA9 13            [ 6]   86 	inc	de
   5DAA AF            [ 4]   87 	xor	a, a
   5DAB 12            [ 7]   88 	ld	(de), a
                             89 ;src/entities/projectile.c:26: projectile->w = 2;
   5DAC 21 04 00      [10]   90 	ld	hl, #0x0004
   5DAF 09            [11]   91 	add	hl, bc
   5DB0 36 02         [10]   92 	ld	(hl), #0x02
                             93 ;src/entities/projectile.c:27: projectile->h = 2;
   5DB2 21 05 00      [10]   94 	ld	hl, #0x0005
   5DB5 09            [11]   95 	add	hl, bc
   5DB6 36 02         [10]   96 	ld	(hl), #0x02
                             97 ;src/entities/projectile.c:28: projectile->active = 0;
   5DB8 21 06 00      [10]   98 	ld	hl, #0x0006
   5DBB 09            [11]   99 	add	hl, bc
   5DBC 36 00         [10]  100 	ld	(hl), #0x00
                            101 ;src/entities/projectile.c:29: projectile->damage = 1;
   5DBE 21 07 00      [10]  102 	ld	hl, #0x0007
   5DC1 09            [11]  103 	add	hl, bc
   5DC2 36 01         [10]  104 	ld	(hl), #0x01
                            105 ;src/entities/projectile.c:30: projectile->lifetime = 0;
   5DC4 21 08 00      [10]  106 	ld	hl, #0x0008
   5DC7 09            [11]  107 	add	hl, bc
   5DC8 36 00         [10]  108 	ld	(hl), #0x00
                            109 ;src/entities/projectile.c:31: projectile->weapon = 0;
   5DCA 21 09 00      [10]  110 	ld	hl, #0x0009
   5DCD 09            [11]  111 	add	hl, bc
   5DCE 36 00         [10]  112 	ld	(hl), #0x00
   5DD0 C9            [10]  113 	ret
   5DD1                     114 _projectile_basic_sprite:
   5DD1 FF                  115 	.db #0xff	; 255
   5DD2 FF                  116 	.db #0xff	; 255
   5DD3 FF                  117 	.db #0xff	; 255
   5DD4 FF                  118 	.db #0xff	; 255
   5DD5 FF                  119 	.db #0xff	; 255
   5DD6 FF                  120 	.db #0xff	; 255
   5DD7                     121 _projectile_up_sprite:
   5DD7 CF                  122 	.db #0xcf	; 207
   5DD8 CF                  123 	.db #0xcf	; 207
   5DD9 CF                  124 	.db #0xcf	; 207
   5DDA CF                  125 	.db #0xcf	; 207
   5DDB CF                  126 	.db #0xcf	; 207
   5DDC CF                  127 	.db #0xcf	; 207
   5DDD                     128 _projectile_special_sprite:
   5DDD F0                  129 	.db #0xf0	; 240
   5DDE F0                  130 	.db #0xf0	; 240
   5DDF F0                  131 	.db #0xf0	; 240
   5DE0 F0                  132 	.db #0xf0	; 240
   5DE1 F0                  133 	.db #0xf0	; 240
   5DE2 F0                  134 	.db #0xf0	; 240
   5DE3 F0                  135 	.db #0xf0	; 240
   5DE4 F0                  136 	.db #0xf0	; 240
   5DE5 F0                  137 	.db #0xf0	; 240
   5DE6 F0                  138 	.db #0xf0	; 240
   5DE7 F0                  139 	.db #0xf0	; 240
   5DE8 F0                  140 	.db #0xf0	; 240
                            141 ;src/entities/projectile.c:34: void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
                            142 ;	---------------------------------
                            143 ; Function projectilefire
                            144 ; ---------------------------------
   5DE9                     145 _projectilefire::
   5DE9 DD E5         [15]  146 	push	ix
   5DEB DD 21 00 00   [14]  147 	ld	ix,#0
   5DEF DD 39         [15]  148 	add	ix,sp
   5DF1 F5            [11]  149 	push	af
   5DF2 F5            [11]  150 	push	af
                            151 ;src/entities/projectile.c:35: if (!projectile) {
   5DF3 DD 7E 05      [19]  152 	ld	a, 5 (ix)
   5DF6 DD B6 04      [19]  153 	or	a,4 (ix)
                            154 ;src/entities/projectile.c:36: return;
   5DF9 CA 9B 5E      [10]  155 	jp	Z,00109$
                            156 ;src/entities/projectile.c:39: projectile->x = x;
   5DFC DD 4E 04      [19]  157 	ld	c,4 (ix)
   5DFF DD 46 05      [19]  158 	ld	b,5 (ix)
   5E02 DD 7E 06      [19]  159 	ld	a, 6 (ix)
   5E05 02            [ 7]  160 	ld	(bc), a
                            161 ;src/entities/projectile.c:40: projectile->y = y;
   5E06 59            [ 4]  162 	ld	e, c
   5E07 50            [ 4]  163 	ld	d, b
   5E08 13            [ 6]  164 	inc	de
   5E09 DD 7E 07      [19]  165 	ld	a, 7 (ix)
   5E0C 12            [ 7]  166 	ld	(de), a
                            167 ;src/entities/projectile.c:41: projectile->vx = dir;
   5E0D 21 02 00      [10]  168 	ld	hl, #0x0002
   5E10 09            [11]  169 	add	hl,bc
   5E11 DD 75 FE      [19]  170 	ld	-2 (ix), l
   5E14 DD 74 FF      [19]  171 	ld	-1 (ix), h
   5E17 DD 7E 08      [19]  172 	ld	a, 8 (ix)
   5E1A 77            [ 7]  173 	ld	(hl), a
                            174 ;src/entities/projectile.c:42: projectile->vy = 0;
   5E1B 59            [ 4]  175 	ld	e, c
   5E1C 50            [ 4]  176 	ld	d, b
   5E1D 13            [ 6]  177 	inc	de
   5E1E 13            [ 6]  178 	inc	de
   5E1F 13            [ 6]  179 	inc	de
   5E20 AF            [ 4]  180 	xor	a, a
   5E21 12            [ 7]  181 	ld	(de), a
                            182 ;src/entities/projectile.c:43: projectile->weapon = weapon;
   5E22 21 09 00      [10]  183 	ld	hl, #0x0009
   5E25 09            [11]  184 	add	hl, bc
   5E26 DD 7E 09      [19]  185 	ld	a, 9 (ix)
   5E29 77            [ 7]  186 	ld	(hl), a
                            187 ;src/entities/projectile.c:44: projectile->active = 1;
   5E2A 21 06 00      [10]  188 	ld	hl, #0x0006
   5E2D 09            [11]  189 	add	hl, bc
   5E2E 36 01         [10]  190 	ld	(hl), #0x01
                            191 ;src/entities/projectile.c:47: projectile->w = 3;
   5E30 21 04 00      [10]  192 	ld	hl, #0x0004
   5E33 09            [11]  193 	add	hl, bc
                            194 ;src/entities/projectile.c:48: projectile->h = 2;
   5E34 79            [ 4]  195 	ld	a, c
   5E35 C6 05         [ 7]  196 	add	a, #0x05
   5E37 5F            [ 4]  197 	ld	e, a
   5E38 78            [ 4]  198 	ld	a, b
   5E39 CE 00         [ 7]  199 	adc	a, #0x00
   5E3B 57            [ 4]  200 	ld	d, a
                            201 ;src/entities/projectile.c:49: projectile->damage = 1;
   5E3C 79            [ 4]  202 	ld	a, c
   5E3D C6 07         [ 7]  203 	add	a, #0x07
   5E3F DD 77 FC      [19]  204 	ld	-4 (ix), a
   5E42 78            [ 4]  205 	ld	a, b
   5E43 CE 00         [ 7]  206 	adc	a, #0x00
   5E45 DD 77 FD      [19]  207 	ld	-3 (ix), a
                            208 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5E48 79            [ 4]  209 	ld	a, c
   5E49 C6 08         [ 7]  210 	add	a, #0x08
   5E4B 4F            [ 4]  211 	ld	c, a
   5E4C 78            [ 4]  212 	ld	a, b
   5E4D CE 00         [ 7]  213 	adc	a, #0x00
   5E4F 47            [ 4]  214 	ld	b, a
                            215 ;src/entities/projectile.c:46: if (weapon == 0) {
   5E50 DD 7E 09      [19]  216 	ld	a, 9 (ix)
   5E53 B7            [ 4]  217 	or	a, a
   5E54 20 0E         [12]  218 	jr	NZ,00107$
                            219 ;src/entities/projectile.c:47: projectile->w = 3;
   5E56 36 03         [10]  220 	ld	(hl), #0x03
                            221 ;src/entities/projectile.c:48: projectile->h = 2;
   5E58 3E 02         [ 7]  222 	ld	a, #0x02
   5E5A 12            [ 7]  223 	ld	(de), a
                            224 ;src/entities/projectile.c:49: projectile->damage = 1;
   5E5B E1            [10]  225 	pop	hl
   5E5C E5            [11]  226 	push	hl
   5E5D 36 01         [10]  227 	ld	(hl), #0x01
                            228 ;src/entities/projectile.c:50: projectile->lifetime = 45;
   5E5F 3E 2D         [ 7]  229 	ld	a, #0x2d
   5E61 02            [ 7]  230 	ld	(bc), a
   5E62 18 37         [12]  231 	jr	00109$
   5E64                     232 00107$:
                            233 ;src/entities/projectile.c:51: } else if (weapon == 1) {
   5E64 DD 7E 09      [19]  234 	ld	a, 9 (ix)
   5E67 3D            [ 4]  235 	dec	a
   5E68 20 0E         [12]  236 	jr	NZ,00104$
                            237 ;src/entities/projectile.c:52: projectile->w = 2;
   5E6A 36 02         [10]  238 	ld	(hl), #0x02
                            239 ;src/entities/projectile.c:53: projectile->h = 3;
   5E6C 3E 03         [ 7]  240 	ld	a, #0x03
   5E6E 12            [ 7]  241 	ld	(de), a
                            242 ;src/entities/projectile.c:54: projectile->damage = 2;
   5E6F E1            [10]  243 	pop	hl
   5E70 E5            [11]  244 	push	hl
   5E71 36 02         [10]  245 	ld	(hl), #0x02
                            246 ;src/entities/projectile.c:55: projectile->lifetime = 28;
   5E73 3E 1C         [ 7]  247 	ld	a, #0x1c
   5E75 02            [ 7]  248 	ld	(bc), a
   5E76 18 23         [12]  249 	jr	00109$
   5E78                     250 00104$:
                            251 ;src/entities/projectile.c:57: projectile->w = 4;
   5E78 36 04         [10]  252 	ld	(hl), #0x04
                            253 ;src/entities/projectile.c:58: projectile->h = 3;
   5E7A 3E 03         [ 7]  254 	ld	a, #0x03
   5E7C 12            [ 7]  255 	ld	(de), a
                            256 ;src/entities/projectile.c:59: projectile->damage = 3;
   5E7D E1            [10]  257 	pop	hl
   5E7E E5            [11]  258 	push	hl
   5E7F 36 03         [10]  259 	ld	(hl), #0x03
                            260 ;src/entities/projectile.c:60: projectile->lifetime = 56;
   5E81 3E 38         [ 7]  261 	ld	a, #0x38
   5E83 02            [ 7]  262 	ld	(bc), a
                            263 ;src/entities/projectile.c:61: projectile->vx = (i8)(dir > 0 ? 4 : -4);
   5E84 D1            [10]  264 	pop	de
   5E85 C1            [10]  265 	pop	bc
   5E86 C5            [11]  266 	push	bc
   5E87 D5            [11]  267 	push	de
   5E88 AF            [ 4]  268 	xor	a, a
   5E89 DD 96 08      [19]  269 	sub	a, 8 (ix)
   5E8C E2 91 5E      [10]  270 	jp	PO, 00131$
   5E8F EE 80         [ 7]  271 	xor	a, #0x80
   5E91                     272 00131$:
   5E91 F2 98 5E      [10]  273 	jp	P, 00111$
   5E94 3E 04         [ 7]  274 	ld	a, #0x04
   5E96 18 02         [12]  275 	jr	00112$
   5E98                     276 00111$:
   5E98 3E FC         [ 7]  277 	ld	a, #0xfc
   5E9A                     278 00112$:
   5E9A 02            [ 7]  279 	ld	(bc), a
   5E9B                     280 00109$:
   5E9B DD F9         [10]  281 	ld	sp, ix
   5E9D DD E1         [14]  282 	pop	ix
   5E9F C9            [10]  283 	ret
                            284 ;src/entities/projectile.c:65: void projectileupdate(Projectile* projectile) {
                            285 ;	---------------------------------
                            286 ; Function projectileupdate
                            287 ; ---------------------------------
   5EA0                     288 _projectileupdate::
   5EA0 DD E5         [15]  289 	push	ix
   5EA2 DD 21 00 00   [14]  290 	ld	ix,#0
   5EA6 DD 39         [15]  291 	add	ix,sp
   5EA8 3B            [ 6]  292 	dec	sp
                            293 ;src/entities/projectile.c:66: if (!projectile || !projectile->active) {
   5EA9 DD 7E 05      [19]  294 	ld	a, 5 (ix)
   5EAC DD B6 04      [19]  295 	or	a,4 (ix)
   5EAF 28 4A         [12]  296 	jr	Z,00109$
   5EB1 DD 5E 04      [19]  297 	ld	e,4 (ix)
   5EB4 DD 56 05      [19]  298 	ld	d,5 (ix)
   5EB7 FD 21 06 00   [14]  299 	ld	iy, #0x0006
   5EBB FD 19         [15]  300 	add	iy, de
   5EBD FD 7E 00      [19]  301 	ld	a, 0 (iy)
   5EC0 B7            [ 4]  302 	or	a, a
                            303 ;src/entities/projectile.c:67: return;
   5EC1 28 38         [12]  304 	jr	Z,00109$
                            305 ;src/entities/projectile.c:70: projectile->x = (u8)(projectile->x + projectile->vx);
   5EC3 1A            [ 7]  306 	ld	a, (de)
   5EC4 4F            [ 4]  307 	ld	c, a
   5EC5 6B            [ 4]  308 	ld	l, e
   5EC6 62            [ 4]  309 	ld	h, d
   5EC7 23            [ 6]  310 	inc	hl
   5EC8 23            [ 6]  311 	inc	hl
   5EC9 6E            [ 7]  312 	ld	l, (hl)
   5ECA 09            [11]  313 	add	hl, bc
   5ECB 7D            [ 4]  314 	ld	a, l
   5ECC 12            [ 7]  315 	ld	(de), a
                            316 ;src/entities/projectile.c:71: projectile->y = (u8)(projectile->y + projectile->vy);
   5ECD 4B            [ 4]  317 	ld	c, e
   5ECE 42            [ 4]  318 	ld	b, d
   5ECF 03            [ 6]  319 	inc	bc
   5ED0 0A            [ 7]  320 	ld	a, (bc)
   5ED1 DD 77 FF      [19]  321 	ld	-1 (ix), a
   5ED4 6B            [ 4]  322 	ld	l, e
   5ED5 62            [ 4]  323 	ld	h, d
   5ED6 23            [ 6]  324 	inc	hl
   5ED7 23            [ 6]  325 	inc	hl
   5ED8 23            [ 6]  326 	inc	hl
   5ED9 6E            [ 7]  327 	ld	l, (hl)
   5EDA DD 7E FF      [19]  328 	ld	a, -1 (ix)
   5EDD 85            [ 4]  329 	add	a, l
   5EDE 02            [ 7]  330 	ld	(bc), a
                            331 ;src/entities/projectile.c:73: if (projectile->lifetime) {
   5EDF 21 08 00      [10]  332 	ld	hl, #0x0008
   5EE2 19            [11]  333 	add	hl,de
   5EE3 4D            [ 4]  334 	ld	c, l
   5EE4 44            [ 4]  335 	ld	b, h
   5EE5 0A            [ 7]  336 	ld	a, (bc)
   5EE6 B7            [ 4]  337 	or	a, a
   5EE7 28 03         [12]  338 	jr	Z,00105$
                            339 ;src/entities/projectile.c:74: projectile->lifetime--;
   5EE9 C6 FF         [ 7]  340 	add	a, #0xff
   5EEB 02            [ 7]  341 	ld	(bc), a
   5EEC                     342 00105$:
                            343 ;src/entities/projectile.c:77: if (projectile->x > 78 || projectile->lifetime == 0) {
   5EEC 1A            [ 7]  344 	ld	a, (de)
   5EED 5F            [ 4]  345 	ld	e, a
   5EEE 3E 4E         [ 7]  346 	ld	a, #0x4e
   5EF0 93            [ 4]  347 	sub	a, e
   5EF1 38 04         [12]  348 	jr	C,00106$
   5EF3 0A            [ 7]  349 	ld	a, (bc)
   5EF4 B7            [ 4]  350 	or	a, a
   5EF5 20 04         [12]  351 	jr	NZ,00109$
   5EF7                     352 00106$:
                            353 ;src/entities/projectile.c:78: projectile->active = 0;
   5EF7 FD 36 00 00   [19]  354 	ld	0 (iy), #0x00
   5EFB                     355 00109$:
   5EFB 33            [ 6]  356 	inc	sp
   5EFC DD E1         [14]  357 	pop	ix
   5EFE C9            [10]  358 	ret
                            359 ;src/entities/projectile.c:82: void projectilerender(const Projectile* projectile) {
                            360 ;	---------------------------------
                            361 ; Function projectilerender
                            362 ; ---------------------------------
   5EFF                     363 _projectilerender::
   5EFF DD E5         [15]  364 	push	ix
   5F01 DD 21 00 00   [14]  365 	ld	ix,#0
   5F05 DD 39         [15]  366 	add	ix,sp
   5F07 F5            [11]  367 	push	af
   5F08 3B            [ 6]  368 	dec	sp
                            369 ;src/entities/projectile.c:86: if (!projectile || !projectile->active) {
   5F09 DD 7E 05      [19]  370 	ld	a, 5 (ix)
   5F0C DD B6 04      [19]  371 	or	a,4 (ix)
   5F0F 28 6B         [12]  372 	jr	Z,00110$
   5F11 DD 4E 04      [19]  373 	ld	c,4 (ix)
   5F14 DD 46 05      [19]  374 	ld	b,5 (ix)
   5F17 C5            [11]  375 	push	bc
   5F18 FD E1         [14]  376 	pop	iy
   5F1A FD 7E 06      [19]  377 	ld	a, 6 (iy)
   5F1D B7            [ 4]  378 	or	a, a
                            379 ;src/entities/projectile.c:87: return;
   5F1E 28 5C         [12]  380 	jr	Z,00110$
                            381 ;src/entities/projectile.c:90: if (projectile->weapon == 0) sprite = projectile_basic_sprite;
   5F20 C5            [11]  382 	push	bc
   5F21 FD E1         [14]  383 	pop	iy
   5F23 FD 7E 09      [19]  384 	ld	a, 9 (iy)
   5F26 B7            [ 4]  385 	or	a, a
   5F27 20 0A         [12]  386 	jr	NZ,00108$
   5F29 DD 36 FE D1   [19]  387 	ld	-2 (ix), #<(_projectile_basic_sprite)
   5F2D DD 36 FF 5D   [19]  388 	ld	-1 (ix), #>(_projectile_basic_sprite)
   5F31 18 15         [12]  389 	jr	00109$
   5F33                     390 00108$:
                            391 ;src/entities/projectile.c:91: else if (projectile->weapon == 1) sprite = projectile_up_sprite;
   5F33 3D            [ 4]  392 	dec	a
   5F34 20 0A         [12]  393 	jr	NZ,00105$
   5F36 DD 36 FE D7   [19]  394 	ld	-2 (ix), #<(_projectile_up_sprite)
   5F3A DD 36 FF 5D   [19]  395 	ld	-1 (ix), #>(_projectile_up_sprite)
   5F3E 18 08         [12]  396 	jr	00109$
   5F40                     397 00105$:
                            398 ;src/entities/projectile.c:92: else sprite = projectile_special_sprite;
   5F40 DD 36 FE DD   [19]  399 	ld	-2 (ix), #<(_projectile_special_sprite)
   5F44 DD 36 FF 5D   [19]  400 	ld	-1 (ix), #>(_projectile_special_sprite)
   5F48                     401 00109$:
                            402 ;src/entities/projectile.c:94: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
   5F48 69            [ 4]  403 	ld	l, c
   5F49 60            [ 4]  404 	ld	h, b
   5F4A 23            [ 6]  405 	inc	hl
   5F4B 56            [ 7]  406 	ld	d, (hl)
   5F4C 0A            [ 7]  407 	ld	a, (bc)
   5F4D C5            [11]  408 	push	bc
   5F4E 5F            [ 4]  409 	ld	e, a
   5F4F D5            [11]  410 	push	de
   5F50 21 00 C0      [10]  411 	ld	hl, #0xc000
   5F53 E5            [11]  412 	push	hl
   5F54 CD 2A 62      [17]  413 	call	_cpct_getScreenPtr
   5F57 EB            [ 4]  414 	ex	de,hl
   5F58 C1            [10]  415 	pop	bc
                            416 ;src/entities/projectile.c:95: cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
   5F59 C5            [11]  417 	push	bc
   5F5A FD E1         [14]  418 	pop	iy
   5F5C FD 7E 05      [19]  419 	ld	a, 5 (iy)
   5F5F DD 77 FD      [19]  420 	ld	-3 (ix), a
   5F62 69            [ 4]  421 	ld	l, c
   5F63 60            [ 4]  422 	ld	h, b
   5F64 01 04 00      [10]  423 	ld	bc, #0x0004
   5F67 09            [11]  424 	add	hl, bc
   5F68 4E            [ 7]  425 	ld	c, (hl)
   5F69 D5            [11]  426 	push	de
   5F6A FD E1         [14]  427 	pop	iy
   5F6C DD 5E FE      [19]  428 	ld	e,-2 (ix)
   5F6F DD 56 FF      [19]  429 	ld	d,-1 (ix)
   5F72 DD 46 FD      [19]  430 	ld	b, -3 (ix)
   5F75 C5            [11]  431 	push	bc
   5F76 FD E5         [15]  432 	push	iy
   5F78 D5            [11]  433 	push	de
   5F79 CD 5B 60      [17]  434 	call	_cpct_drawSprite
   5F7C                     435 00110$:
   5F7C DD F9         [10]  436 	ld	sp, ix
   5F7E DD E1         [14]  437 	pop	ix
   5F80 C9            [10]  438 	ret
                            439 	.area _CODE
                            440 	.area _INITIALIZER
                            441 	.area _CABS (ABS)
