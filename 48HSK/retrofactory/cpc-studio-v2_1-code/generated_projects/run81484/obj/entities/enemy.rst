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
                             14 	.globl _cpct_drawSprite
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
                             51 ;src/entities/enemy.c:85: void enemyinit(Enemy* enemy) {
                             52 ;	---------------------------------
                             53 ; Function enemyinit
                             54 ; ---------------------------------
   5D18                      55 _enemyinit::
                             56 ;src/entities/enemy.c:86: if (!enemy) {
   5D18 21 03 00      [10]   57 	ld	hl, #2+1
   5D1B 39            [11]   58 	add	hl, sp
   5D1C 7E            [ 7]   59 	ld	a, (hl)
   5D1D 2B            [ 6]   60 	dec	hl
   5D1E B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:87: return;
   5D1F C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:90: enemy->x = 0;
   5D20 D1            [10]   65 	pop	de
   5D21 C1            [10]   66 	pop	bc
   5D22 C5            [11]   67 	push	bc
   5D23 D5            [11]   68 	push	de
   5D24 AF            [ 4]   69 	xor	a, a
   5D25 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:91: enemy->y = 0;
   5D26 59            [ 4]   72 	ld	e, c
   5D27 50            [ 4]   73 	ld	d, b
   5D28 13            [ 6]   74 	inc	de
   5D29 AF            [ 4]   75 	xor	a, a
   5D2A 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:92: enemy->vx = 0;
   5D2B 59            [ 4]   78 	ld	e, c
   5D2C 50            [ 4]   79 	ld	d, b
   5D2D 13            [ 6]   80 	inc	de
   5D2E 13            [ 6]   81 	inc	de
   5D2F AF            [ 4]   82 	xor	a, a
   5D30 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:93: enemy->vy = 0;
   5D31 59            [ 4]   85 	ld	e, c
   5D32 50            [ 4]   86 	ld	d, b
   5D33 13            [ 6]   87 	inc	de
   5D34 13            [ 6]   88 	inc	de
   5D35 13            [ 6]   89 	inc	de
   5D36 AF            [ 4]   90 	xor	a, a
   5D37 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:94: enemy->w = 4;
   5D38 21 04 00      [10]   93 	ld	hl, #0x0004
   5D3B 09            [11]   94 	add	hl, bc
   5D3C 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:95: enemy->h = 16;
   5D3E 21 05 00      [10]   97 	ld	hl, #0x0005
   5D41 09            [11]   98 	add	hl, bc
   5D42 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:96: enemy->active = 0;
   5D44 21 06 00      [10]  101 	ld	hl, #0x0006
   5D47 09            [11]  102 	add	hl, bc
   5D48 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:97: enemy->health = 1;
   5D4A 21 07 00      [10]  105 	ld	hl, #0x0007
   5D4D 09            [11]  106 	add	hl, bc
   5D4E 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:98: enemy->reward = 100;
   5D50 21 08 00      [10]  109 	ld	hl, #0x0008
   5D53 09            [11]  110 	add	hl, bc
   5D54 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:99: enemy->kind = 0;
   5D56 21 09 00      [10]  113 	ld	hl, #0x0009
   5D59 09            [11]  114 	add	hl, bc
   5D5A 36 00         [10]  115 	ld	(hl), #0x00
   5D5C C9            [10]  116 	ret
   5D5D                     117 _enemy_kind0_sprite:
   5D5D 30                  118 	.db #0x30	; 48	'0'
   5D5E 30                  119 	.db #0x30	; 48	'0'
   5D5F 30                  120 	.db #0x30	; 48	'0'
   5D60 30                  121 	.db #0x30	; 48	'0'
   5D61 B8                  122 	.db #0xb8	; 184
   5D62 FC                  123 	.db #0xfc	; 252
   5D63 FC                  124 	.db #0xfc	; 252
   5D64 74                  125 	.db #0x74	; 116	't'
   5D65 B8                  126 	.db #0xb8	; 184
   5D66 F8                  127 	.db #0xf8	; 248
   5D67 F4                  128 	.db #0xf4	; 244
   5D68 74                  129 	.db #0x74	; 116	't'
   5D69 B8                  130 	.db #0xb8	; 184
   5D6A FC                  131 	.db #0xfc	; 252
   5D6B FC                  132 	.db #0xfc	; 252
   5D6C 74                  133 	.db #0x74	; 116	't'
   5D6D 30                  134 	.db #0x30	; 48	'0'
   5D6E FC                  135 	.db #0xfc	; 252
   5D6F FC                  136 	.db #0xfc	; 252
   5D70 30                  137 	.db #0x30	; 48	'0'
   5D71 90                  138 	.db #0x90	; 144
   5D72 60                  139 	.db #0x60	; 96
   5D73 90                  140 	.db #0x90	; 144
   5D74 60                  141 	.db #0x60	; 96
   5D75 90                  142 	.db #0x90	; 144
   5D76 C0                  143 	.db #0xc0	; 192
   5D77 C0                  144 	.db #0xc0	; 192
   5D78 60                  145 	.db #0x60	; 96
   5D79 90                  146 	.db #0x90	; 144
   5D7A C0                  147 	.db #0xc0	; 192
   5D7B C0                  148 	.db #0xc0	; 192
   5D7C 60                  149 	.db #0x60	; 96
   5D7D 90                  150 	.db #0x90	; 144
   5D7E C0                  151 	.db #0xc0	; 192
   5D7F C0                  152 	.db #0xc0	; 192
   5D80 60                  153 	.db #0x60	; 96
   5D81 90                  154 	.db #0x90	; 144
   5D82 90                  155 	.db #0x90	; 144
   5D83 60                  156 	.db #0x60	; 96
   5D84 60                  157 	.db #0x60	; 96
   5D85 30                  158 	.db #0x30	; 48	'0'
   5D86 30                  159 	.db #0x30	; 48	'0'
   5D87 30                  160 	.db #0x30	; 48	'0'
   5D88 30                  161 	.db #0x30	; 48	'0'
   5D89 90                  162 	.db #0x90	; 144
   5D8A 90                  163 	.db #0x90	; 144
   5D8B 60                  164 	.db #0x60	; 96
   5D8C 60                  165 	.db #0x60	; 96
   5D8D 60                  166 	.db #0x60	; 96
   5D8E 60                  167 	.db #0x60	; 96
   5D8F 60                  168 	.db #0x60	; 96
   5D90 60                  169 	.db #0x60	; 96
   5D91 60                  170 	.db #0x60	; 96
   5D92 60                  171 	.db #0x60	; 96
   5D93 60                  172 	.db #0x60	; 96
   5D94 60                  173 	.db #0x60	; 96
   5D95 60                  174 	.db #0x60	; 96
   5D96 30                  175 	.db #0x30	; 48	'0'
   5D97 30                  176 	.db #0x30	; 48	'0'
   5D98 90                  177 	.db #0x90	; 144
   5D99 C0                  178 	.db #0xc0	; 192
   5D9A 30                  179 	.db #0x30	; 48	'0'
   5D9B 30                  180 	.db #0x30	; 48	'0'
   5D9C C0                  181 	.db #0xc0	; 192
   5D9D                     182 _enemy_kind1_sprite:
   5D9D 64                  183 	.db #0x64	; 100	'd'
   5D9E 30                  184 	.db #0x30	; 48	'0'
   5D9F 30                  185 	.db #0x30	; 48	'0'
   5DA0 30                  186 	.db #0x30	; 48	'0'
   5DA1 98                  187 	.db #0x98	; 152
   5DA2 64                  188 	.db #0x64	; 100	'd'
   5DA3 FC                  189 	.db #0xfc	; 252
   5DA4 FC                  190 	.db #0xfc	; 252
   5DA5 FC                  191 	.db #0xfc	; 252
   5DA6 98                  192 	.db #0x98	; 152
   5DA7 64                  193 	.db #0x64	; 100	'd'
   5DA8 70                  194 	.db #0x70	; 112	'p'
   5DA9 30                  195 	.db #0x30	; 48	'0'
   5DAA 70                  196 	.db #0x70	; 112	'p'
   5DAB 98                  197 	.db #0x98	; 152
   5DAC 64                  198 	.db #0x64	; 100	'd'
   5DAD 30                  199 	.db #0x30	; 48	'0'
   5DAE 30                  200 	.db #0x30	; 48	'0'
   5DAF 30                  201 	.db #0x30	; 48	'0'
   5DB0 98                  202 	.db #0x98	; 152
   5DB1 CC                  203 	.db #0xcc	; 204
   5DB2 30                  204 	.db #0x30	; 48	'0'
   5DB3 30                  205 	.db #0x30	; 48	'0'
   5DB4 30                  206 	.db #0x30	; 48	'0'
   5DB5 CC                  207 	.db #0xcc	; 204
   5DB6 C4                  208 	.db #0xc4	; 196
   5DB7 C0                  209 	.db #0xc0	; 192
   5DB8 CC                  210 	.db #0xcc	; 204
   5DB9 C0                  211 	.db #0xc0	; 192
   5DBA C8                  212 	.db #0xc8	; 200
   5DBB C4                  213 	.db #0xc4	; 196
   5DBC C0                  214 	.db #0xc0	; 192
   5DBD C0                  215 	.db #0xc0	; 192
   5DBE C0                  216 	.db #0xc0	; 192
   5DBF C8                  217 	.db #0xc8	; 200
   5DC0 C4                  218 	.db #0xc4	; 196
   5DC1 C0                  219 	.db #0xc0	; 192
   5DC2 C0                  220 	.db #0xc0	; 192
   5DC3 C0                  221 	.db #0xc0	; 192
   5DC4 C8                  222 	.db #0xc8	; 200
   5DC5 C4                  223 	.db #0xc4	; 196
   5DC6 C4                  224 	.db #0xc4	; 196
   5DC7 C0                  225 	.db #0xc0	; 192
   5DC8 C8                  226 	.db #0xc8	; 200
   5DC9 C8                  227 	.db #0xc8	; 200
   5DCA C4                  228 	.db #0xc4	; 196
   5DCB C0                  229 	.db #0xc0	; 192
   5DCC CC                  230 	.db #0xcc	; 204
   5DCD C0                  231 	.db #0xc0	; 192
   5DCE C8                  232 	.db #0xc8	; 200
   5DCF CC                  233 	.db #0xcc	; 204
   5DD0 CC                  234 	.db #0xcc	; 204
   5DD1 CC                  235 	.db #0xcc	; 204
   5DD2 CC                  236 	.db #0xcc	; 204
   5DD3 CC                  237 	.db #0xcc	; 204
   5DD4 C4                  238 	.db #0xc4	; 196
   5DD5 C4                  239 	.db #0xc4	; 196
   5DD6 CC                  240 	.db #0xcc	; 204
   5DD7 C8                  241 	.db #0xc8	; 200
   5DD8 C8                  242 	.db #0xc8	; 200
   5DD9 C8                  243 	.db #0xc8	; 200
   5DDA C8                  244 	.db #0xc8	; 200
   5DDB C0                  245 	.db #0xc0	; 192
   5DDC C4                  246 	.db #0xc4	; 196
   5DDD C4                  247 	.db #0xc4	; 196
   5DDE C8                  248 	.db #0xc8	; 200
   5DDF 98                  249 	.db #0x98	; 152
   5DE0 30                  250 	.db #0x30	; 48	'0'
   5DE1 64                  251 	.db #0x64	; 100	'd'
   5DE2 C4                  252 	.db #0xc4	; 196
   5DE3                     253 _enemy_kind2_sprite:
   5DE3 FC                  254 	.db #0xfc	; 252
   5DE4 FC                  255 	.db #0xfc	; 252
   5DE5 FC                  256 	.db #0xfc	; 252
   5DE6 FC                  257 	.db #0xfc	; 252
   5DE7 FC                  258 	.db #0xfc	; 252
   5DE8 FC                  259 	.db #0xfc	; 252
   5DE9 D4                  260 	.db #0xd4	; 212
   5DEA E8                  261 	.db #0xe8	; 232
   5DEB D4                  262 	.db #0xd4	; 212
   5DEC E8                  263 	.db #0xe8	; 232
   5DED D4                  264 	.db #0xd4	; 212
   5DEE E8                  265 	.db #0xe8	; 232
   5DEF D4                  266 	.db #0xd4	; 212
   5DF0 C0                  267 	.db #0xc0	; 192
   5DF1 C0                  268 	.db #0xc0	; 192
   5DF2 C0                  269 	.db #0xc0	; 192
   5DF3 C0                  270 	.db #0xc0	; 192
   5DF4 E8                  271 	.db #0xe8	; 232
   5DF5 D4                  272 	.db #0xd4	; 212
   5DF6 90                  273 	.db #0x90	; 144
   5DF7 C0                  274 	.db #0xc0	; 192
   5DF8 60                  275 	.db #0x60	; 96
   5DF9 C0                  276 	.db #0xc0	; 192
   5DFA E8                  277 	.db #0xe8	; 232
   5DFB FC                  278 	.db #0xfc	; 252
   5DFC FC                  279 	.db #0xfc	; 252
   5DFD FC                  280 	.db #0xfc	; 252
   5DFE FC                  281 	.db #0xfc	; 252
   5DFF FC                  282 	.db #0xfc	; 252
   5E00 FC                  283 	.db #0xfc	; 252
   5E01 D4                  284 	.db #0xd4	; 212
   5E02 74                  285 	.db #0x74	; 116	't'
   5E03 B8                  286 	.db #0xb8	; 184
   5E04 74                  287 	.db #0x74	; 116	't'
   5E05 B8                  288 	.db #0xb8	; 184
   5E06 E8                  289 	.db #0xe8	; 232
   5E07 90                  290 	.db #0x90	; 144
   5E08 90                  291 	.db #0x90	; 144
   5E09 60                  292 	.db #0x60	; 96
   5E0A 90                  293 	.db #0x90	; 144
   5E0B 60                  294 	.db #0x60	; 96
   5E0C 60                  295 	.db #0x60	; 96
   5E0D 30                  296 	.db #0x30	; 48	'0'
   5E0E C0                  297 	.db #0xc0	; 192
   5E0F 30                  298 	.db #0x30	; 48	'0'
   5E10 30                  299 	.db #0x30	; 48	'0'
   5E11 C0                  300 	.db #0xc0	; 192
   5E12 30                  301 	.db #0x30	; 48	'0'
   5E13 FC                  302 	.db #0xfc	; 252
   5E14 D4                  303 	.db #0xd4	; 212
   5E15 FC                  304 	.db #0xfc	; 252
   5E16 FC                  305 	.db #0xfc	; 252
   5E17 E8                  306 	.db #0xe8	; 232
   5E18 FC                  307 	.db #0xfc	; 252
   5E19 FC                  308 	.db #0xfc	; 252
   5E1A FC                  309 	.db #0xfc	; 252
   5E1B C0                  310 	.db #0xc0	; 192
   5E1C C0                  311 	.db #0xc0	; 192
   5E1D FC                  312 	.db #0xfc	; 252
   5E1E FC                  313 	.db #0xfc	; 252
   5E1F                     314 _enemy_kind3_sprite:
   5E1F 3F                  315 	.db #0x3f	; 63
   5E20 3F                  316 	.db #0x3f	; 63
   5E21 3F                  317 	.db #0x3f	; 63
   5E22 3F                  318 	.db #0x3f	; 63
   5E23 3F                  319 	.db #0x3f	; 63
   5E24 3F                  320 	.db #0x3f	; 63
   5E25 3F                  321 	.db #0x3f	; 63
   5E26 3F                  322 	.db #0x3f	; 63
   5E27 3F                  323 	.db #0x3f	; 63
   5E28 3F                  324 	.db #0x3f	; 63
   5E29 95                  325 	.db #0x95	; 149
   5E2A C0                  326 	.db #0xc0	; 192
   5E2B C0                  327 	.db #0xc0	; 192
   5E2C C0                  328 	.db #0xc0	; 192
   5E2D C0                  329 	.db #0xc0	; 192
   5E2E C0                  330 	.db #0xc0	; 192
   5E2F C0                  331 	.db #0xc0	; 192
   5E30 C0                  332 	.db #0xc0	; 192
   5E31 C0                  333 	.db #0xc0	; 192
   5E32 6A                  334 	.db #0x6a	; 106	'j'
   5E33 95                  335 	.db #0x95	; 149
   5E34 CC                  336 	.db #0xcc	; 204
   5E35 C0                  337 	.db #0xc0	; 192
   5E36 C0                  338 	.db #0xc0	; 192
   5E37 CC                  339 	.db #0xcc	; 204
   5E38 C8                  340 	.db #0xc8	; 200
   5E39 C4                  341 	.db #0xc4	; 196
   5E3A C0                  342 	.db #0xc0	; 192
   5E3B CC                  343 	.db #0xcc	; 204
   5E3C 6A                  344 	.db #0x6a	; 106	'j'
   5E3D 95                  345 	.db #0x95	; 149
   5E3E C0                  346 	.db #0xc0	; 192
   5E3F C0                  347 	.db #0xc0	; 192
   5E40 C0                  348 	.db #0xc0	; 192
   5E41 C0                  349 	.db #0xc0	; 192
   5E42 C0                  350 	.db #0xc0	; 192
   5E43 C0                  351 	.db #0xc0	; 192
   5E44 C0                  352 	.db #0xc0	; 192
   5E45 C0                  353 	.db #0xc0	; 192
   5E46 6A                  354 	.db #0x6a	; 106	'j'
   5E47 95                  355 	.db #0x95	; 149
   5E48 90                  356 	.db #0x90	; 144
   5E49 C0                  357 	.db #0xc0	; 192
   5E4A 60                  358 	.db #0x60	; 96
   5E4B C0                  359 	.db #0xc0	; 192
   5E4C 60                  360 	.db #0x60	; 96
   5E4D C0                  361 	.db #0xc0	; 192
   5E4E C0                  362 	.db #0xc0	; 192
   5E4F 90                  363 	.db #0x90	; 144
   5E50 6A                  364 	.db #0x6a	; 106	'j'
   5E51 95                  365 	.db #0x95	; 149
   5E52 C0                  366 	.db #0xc0	; 192
   5E53 C0                  367 	.db #0xc0	; 192
   5E54 C0                  368 	.db #0xc0	; 192
   5E55 C0                  369 	.db #0xc0	; 192
   5E56 C0                  370 	.db #0xc0	; 192
   5E57 C0                  371 	.db #0xc0	; 192
   5E58 C0                  372 	.db #0xc0	; 192
   5E59 C0                  373 	.db #0xc0	; 192
   5E5A 6A                  374 	.db #0x6a	; 106	'j'
   5E5B 3F                  375 	.db #0x3f	; 63
   5E5C C0                  376 	.db #0xc0	; 192
   5E5D C0                  377 	.db #0xc0	; 192
   5E5E C0                  378 	.db #0xc0	; 192
   5E5F C0                  379 	.db #0xc0	; 192
   5E60 C0                  380 	.db #0xc0	; 192
   5E61 C0                  381 	.db #0xc0	; 192
   5E62 C0                  382 	.db #0xc0	; 192
   5E63 C0                  383 	.db #0xc0	; 192
   5E64 3F                  384 	.db #0x3f	; 63
   5E65 3F                  385 	.db #0x3f	; 63
   5E66 95                  386 	.db #0x95	; 149
   5E67 CC                  387 	.db #0xcc	; 204
   5E68 C0                  388 	.db #0xc0	; 192
   5E69 CC                  389 	.db #0xcc	; 204
   5E6A CC                  390 	.db #0xcc	; 204
   5E6B C0                  391 	.db #0xc0	; 192
   5E6C CC                  392 	.db #0xcc	; 204
   5E6D 6A                  393 	.db #0x6a	; 106	'j'
   5E6E 3F                  394 	.db #0x3f	; 63
   5E6F 3F                  395 	.db #0x3f	; 63
   5E70 3F                  396 	.db #0x3f	; 63
   5E71 95                  397 	.db #0x95	; 149
   5E72 C0                  398 	.db #0xc0	; 192
   5E73 6A                  399 	.db #0x6a	; 106	'j'
   5E74 95                  400 	.db #0x95	; 149
   5E75 C0                  401 	.db #0xc0	; 192
   5E76 6A                  402 	.db #0x6a	; 106	'j'
   5E77 3F                  403 	.db #0x3f	; 63
   5E78 3F                  404 	.db #0x3f	; 63
   5E79 95                  405 	.db #0x95	; 149
   5E7A C0                  406 	.db #0xc0	; 192
   5E7B C0                  407 	.db #0xc0	; 192
   5E7C C0                  408 	.db #0xc0	; 192
   5E7D C0                  409 	.db #0xc0	; 192
   5E7E C0                  410 	.db #0xc0	; 192
   5E7F C0                  411 	.db #0xc0	; 192
   5E80 C0                  412 	.db #0xc0	; 192
   5E81 C0                  413 	.db #0xc0	; 192
   5E82 6A                  414 	.db #0x6a	; 106	'j'
   5E83 95                  415 	.db #0x95	; 149
   5E84 C8                  416 	.db #0xc8	; 200
   5E85 C0                  417 	.db #0xc0	; 192
   5E86 C0                  418 	.db #0xc0	; 192
   5E87 C4                  419 	.db #0xc4	; 196
   5E88 C8                  420 	.db #0xc8	; 200
   5E89 C0                  421 	.db #0xc0	; 192
   5E8A C0                  422 	.db #0xc0	; 192
   5E8B C4                  423 	.db #0xc4	; 196
   5E8C 6A                  424 	.db #0x6a	; 106	'j'
   5E8D 95                  425 	.db #0x95	; 149
   5E8E C0                  426 	.db #0xc0	; 192
   5E8F C0                  427 	.db #0xc0	; 192
   5E90 C0                  428 	.db #0xc0	; 192
   5E91 C0                  429 	.db #0xc0	; 192
   5E92 C0                  430 	.db #0xc0	; 192
   5E93 C0                  431 	.db #0xc0	; 192
   5E94 C0                  432 	.db #0xc0	; 192
   5E95 C0                  433 	.db #0xc0	; 192
   5E96 6A                  434 	.db #0x6a	; 106	'j'
   5E97 95                  435 	.db #0x95	; 149
   5E98 C0                  436 	.db #0xc0	; 192
   5E99 3F                  437 	.db #0x3f	; 63
   5E9A 3F                  438 	.db #0x3f	; 63
   5E9B 3F                  439 	.db #0x3f	; 63
   5E9C 3F                  440 	.db #0x3f	; 63
   5E9D C0                  441 	.db #0xc0	; 192
   5E9E C0                  442 	.db #0xc0	; 192
   5E9F C0                  443 	.db #0xc0	; 192
   5EA0 6A                  444 	.db #0x6a	; 106	'j'
   5EA1 95                  445 	.db #0x95	; 149
   5EA2 6A                  446 	.db #0x6a	; 106	'j'
   5EA3 3F                  447 	.db #0x3f	; 63
   5EA4 3F                  448 	.db #0x3f	; 63
   5EA5 3F                  449 	.db #0x3f	; 63
   5EA6 3F                  450 	.db #0x3f	; 63
   5EA7 95                  451 	.db #0x95	; 149
   5EA8 C0                  452 	.db #0xc0	; 192
   5EA9 C0                  453 	.db #0xc0	; 192
   5EAA 6A                  454 	.db #0x6a	; 106	'j'
   5EAB 3F                  455 	.db #0x3f	; 63
   5EAC 3F                  456 	.db #0x3f	; 63
   5EAD 3F                  457 	.db #0x3f	; 63
   5EAE 3F                  458 	.db #0x3f	; 63
   5EAF 3F                  459 	.db #0x3f	; 63
   5EB0 3F                  460 	.db #0x3f	; 63
   5EB1 3F                  461 	.db #0x3f	; 63
   5EB2 3F                  462 	.db #0x3f	; 63
   5EB3 3F                  463 	.db #0x3f	; 63
   5EB4 3F                  464 	.db #0x3f	; 63
   5EB5 95                  465 	.db #0x95	; 149
   5EB6 95                  466 	.db #0x95	; 149
   5EB7 95                  467 	.db #0x95	; 149
   5EB8 95                  468 	.db #0x95	; 149
   5EB9 95                  469 	.db #0x95	; 149
   5EBA 95                  470 	.db #0x95	; 149
   5EBB 95                  471 	.db #0x95	; 149
   5EBC 95                  472 	.db #0x95	; 149
   5EBD 95                  473 	.db #0x95	; 149
   5EBE 3F                  474 	.db #0x3f	; 63
   5EBF 6A                  475 	.db #0x6a	; 106	'j'
   5EC0 6A                  476 	.db #0x6a	; 106	'j'
   5EC1 6A                  477 	.db #0x6a	; 106	'j'
   5EC2 6A                  478 	.db #0x6a	; 106	'j'
   5EC3 6A                  479 	.db #0x6a	; 106	'j'
   5EC4 95                  480 	.db #0x95	; 149
   5EC5 95                  481 	.db #0x95	; 149
   5EC6 95                  482 	.db #0x95	; 149
   5EC7 95                  483 	.db #0x95	; 149
   5EC8 95                  484 	.db #0x95	; 149
   5EC9 C0                  485 	.db #0xc0	; 192
   5ECA 3F                  486 	.db #0x3f	; 63
   5ECB C0                  487 	.db #0xc0	; 192
   5ECC 3F                  488 	.db #0x3f	; 63
   5ECD C0                  489 	.db #0xc0	; 192
   5ECE C0                  490 	.db #0xc0	; 192
   5ECF 3F                  491 	.db #0x3f	; 63
   5ED0 C0                  492 	.db #0xc0	; 192
   5ED1 3F                  493 	.db #0x3f	; 63
   5ED2 C0                  494 	.db #0xc0	; 192
                            495 ;src/entities/enemy.c:102: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   5ED3                     499 _enemyspawn::
   5ED3 DD E5         [15]  500 	push	ix
   5ED5 DD 21 00 00   [14]  501 	ld	ix,#0
   5ED9 DD 39         [15]  502 	add	ix,sp
   5EDB 21 F1 FF      [10]  503 	ld	hl, #-15
   5EDE 39            [11]  504 	add	hl, sp
   5EDF F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:103: if (!enemy) {
   5EE0 DD 7E 05      [19]  507 	ld	a, 5 (ix)
   5EE3 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:104: return;
   5EE6 CA A6 60      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:107: enemy->x = x;
   5EE9 DD 7E 04      [19]  512 	ld	a, 4 (ix)
   5EEC DD 77 FE      [19]  513 	ld	-2 (ix), a
   5EEF DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5EF2 DD 77 FF      [19]  515 	ld	-1 (ix), a
   5EF5 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   5EF8 DD 66 FF      [19]  517 	ld	h,-1 (ix)
   5EFB DD 7E 06      [19]  518 	ld	a, 6 (ix)
   5EFE 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:108: enemy->y = y;
   5EFF DD 4E FE      [19]  521 	ld	c,-2 (ix)
   5F02 DD 46 FF      [19]  522 	ld	b,-1 (ix)
   5F05 03            [ 6]  523 	inc	bc
   5F06 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   5F09 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:109: enemy->vx = move_right ? 1 : -1;
   5F0A DD 7E FE      [19]  527 	ld	a, -2 (ix)
   5F0D C6 02         [ 7]  528 	add	a, #0x02
   5F0F DD 77 FC      [19]  529 	ld	-4 (ix), a
   5F12 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5F15 CE 00         [ 7]  531 	adc	a, #0x00
   5F17 DD 77 FD      [19]  532 	ld	-3 (ix), a
   5F1A DD 7E 09      [19]  533 	ld	a, 9 (ix)
   5F1D B7            [ 4]  534 	or	a, a
   5F1E 28 04         [12]  535 	jr	Z,00114$
   5F20 0E 01         [ 7]  536 	ld	c, #0x01
   5F22 18 02         [12]  537 	jr	00115$
   5F24                     538 00114$:
   5F24 0E FF         [ 7]  539 	ld	c, #0xff
   5F26                     540 00115$:
   5F26 DD 6E FC      [19]  541 	ld	l,-4 (ix)
   5F29 DD 66 FD      [19]  542 	ld	h,-3 (ix)
   5F2C 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:110: enemy->vy = 0;
   5F2D DD 7E FE      [19]  545 	ld	a, -2 (ix)
   5F30 C6 03         [ 7]  546 	add	a, #0x03
   5F32 DD 77 FA      [19]  547 	ld	-6 (ix), a
   5F35 DD 7E FF      [19]  548 	ld	a, -1 (ix)
   5F38 CE 00         [ 7]  549 	adc	a, #0x00
   5F3A DD 77 FB      [19]  550 	ld	-5 (ix), a
   5F3D DD 6E FA      [19]  551 	ld	l,-6 (ix)
   5F40 DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5F43 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:111: enemy->active = 1;
   5F45 DD 7E FE      [19]  555 	ld	a, -2 (ix)
   5F48 C6 06         [ 7]  556 	add	a, #0x06
   5F4A DD 77 F8      [19]  557 	ld	-8 (ix), a
   5F4D DD 7E FF      [19]  558 	ld	a, -1 (ix)
   5F50 CE 00         [ 7]  559 	adc	a, #0x00
   5F52 DD 77 F9      [19]  560 	ld	-7 (ix), a
   5F55 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   5F58 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   5F5B 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:112: enemy->kind = kind;
   5F5D DD 7E FE      [19]  565 	ld	a, -2 (ix)
   5F60 C6 09         [ 7]  566 	add	a, #0x09
   5F62 DD 77 F8      [19]  567 	ld	-8 (ix), a
   5F65 DD 7E FF      [19]  568 	ld	a, -1 (ix)
   5F68 CE 00         [ 7]  569 	adc	a, #0x00
   5F6A DD 77 F9      [19]  570 	ld	-7 (ix), a
   5F6D DD 6E F8      [19]  571 	ld	l,-8 (ix)
   5F70 DD 66 F9      [19]  572 	ld	h,-7 (ix)
   5F73 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   5F76 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:115: enemy->w = 5;
   5F77 DD 7E FE      [19]  576 	ld	a, -2 (ix)
   5F7A C6 04         [ 7]  577 	add	a, #0x04
   5F7C DD 77 F8      [19]  578 	ld	-8 (ix), a
   5F7F DD 7E FF      [19]  579 	ld	a, -1 (ix)
   5F82 CE 00         [ 7]  580 	adc	a, #0x00
   5F84 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:116: enemy->h = 14;
   5F87 DD 7E FE      [19]  583 	ld	a, -2 (ix)
   5F8A C6 05         [ 7]  584 	add	a, #0x05
   5F8C DD 77 F6      [19]  585 	ld	-10 (ix), a
   5F8F DD 7E FF      [19]  586 	ld	a, -1 (ix)
   5F92 CE 00         [ 7]  587 	adc	a, #0x00
   5F94 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:117: enemy->health = 2;
   5F97 DD 7E FE      [19]  590 	ld	a, -2 (ix)
   5F9A C6 07         [ 7]  591 	add	a, #0x07
   5F9C DD 77 F4      [19]  592 	ld	-12 (ix), a
   5F9F DD 7E FF      [19]  593 	ld	a, -1 (ix)
   5FA2 CE 00         [ 7]  594 	adc	a, #0x00
   5FA4 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:118: enemy->reward = 180;
   5FA7 DD 7E FE      [19]  597 	ld	a, -2 (ix)
   5FAA C6 08         [ 7]  598 	add	a, #0x08
   5FAC DD 77 FE      [19]  599 	ld	-2 (ix), a
   5FAF DD 7E FF      [19]  600 	ld	a, -1 (ix)
   5FB2 CE 00         [ 7]  601 	adc	a, #0x00
   5FB4 DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:114: if (kind == 1) {
   5FB7 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   5FBA 3D            [ 4]  605 	dec	a
   5FBB 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:115: enemy->w = 5;
   5FBD DD 6E F8      [19]  608 	ld	l,-8 (ix)
   5FC0 DD 66 F9      [19]  609 	ld	h,-7 (ix)
   5FC3 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:116: enemy->h = 14;
   5FC5 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   5FC8 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   5FCB 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:117: enemy->health = 2;
   5FCD DD 6E F4      [19]  616 	ld	l,-12 (ix)
   5FD0 DD 66 F5      [19]  617 	ld	h,-11 (ix)
   5FD3 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:118: enemy->reward = 180;
   5FD5 DD 6E FE      [19]  620 	ld	l,-2 (ix)
   5FD8 DD 66 FF      [19]  621 	ld	h,-1 (ix)
   5FDB 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:119: enemy->vx = move_right ? 2 : -2;
   5FDD DD 7E FC      [19]  624 	ld	a, -4 (ix)
   5FE0 DD 77 F2      [19]  625 	ld	-14 (ix), a
   5FE3 DD 7E FD      [19]  626 	ld	a, -3 (ix)
   5FE6 DD 77 F3      [19]  627 	ld	-13 (ix), a
   5FE9 DD 7E 09      [19]  628 	ld	a, 9 (ix)
   5FEC B7            [ 4]  629 	or	a, a
   5FED 28 06         [12]  630 	jr	Z,00116$
   5FEF DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5FF3 18 04         [12]  632 	jr	00117$
   5FF5                     633 00116$:
   5FF5 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5FF9                     635 00117$:
   5FF9 DD 6E F2      [19]  636 	ld	l,-14 (ix)
   5FFC DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5FFF DD 7E F1      [19]  638 	ld	a, -15 (ix)
   6002 77            [ 7]  639 	ld	(hl), a
   6003 C3 A6 60      [10]  640 	jp	00112$
   6006                     641 00110$:
                            642 ;src/entities/enemy.c:120: } else if (kind == 2) {
   6006 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   6009 D6 02         [ 7]  644 	sub	a, #0x02
   600B 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:121: enemy->w = 6;
   600D DD 6E F8      [19]  647 	ld	l,-8 (ix)
   6010 DD 66 F9      [19]  648 	ld	h,-7 (ix)
   6013 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:122: enemy->h = 10;
   6015 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   6018 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   601B 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:123: enemy->health = 1;
   601D DD 6E F4      [19]  655 	ld	l,-12 (ix)
   6020 DD 66 F5      [19]  656 	ld	h,-11 (ix)
   6023 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:124: enemy->reward = 150;
   6025 DD 6E FE      [19]  659 	ld	l,-2 (ix)
   6028 DD 66 FF      [19]  660 	ld	h,-1 (ix)
   602B 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:125: enemy->vy = move_right ? 1 : -1;
   602D DD 4E FA      [19]  663 	ld	c,-6 (ix)
   6030 DD 46 FB      [19]  664 	ld	b,-5 (ix)
   6033 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   6036 B7            [ 4]  666 	or	a, a
   6037 28 04         [12]  667 	jr	Z,00118$
   6039 3E 01         [ 7]  668 	ld	a, #0x01
   603B 18 02         [12]  669 	jr	00119$
   603D                     670 00118$:
   603D 3E FF         [ 7]  671 	ld	a, #0xff
   603F                     672 00119$:
   603F 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:126: enemy->vx = 1;
   6040 DD 6E FC      [19]  675 	ld	l,-4 (ix)
   6043 DD 66 FD      [19]  676 	ld	h,-3 (ix)
   6046 36 01         [10]  677 	ld	(hl), #0x01
   6048 18 5C         [12]  678 	jr	00112$
   604A                     679 00107$:
                            680 ;src/entities/enemy.c:127: } else if (kind == 3) {
   604A DD 7E 08      [19]  681 	ld	a, 8 (ix)
   604D D6 03         [ 7]  682 	sub	a, #0x03
   604F 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:128: enemy->w = 10;
   6051 DD 6E F8      [19]  685 	ld	l,-8 (ix)
   6054 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   6057 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:129: enemy->h = 18;
   6059 DD 6E F6      [19]  689 	ld	l,-10 (ix)
   605C DD 66 F7      [19]  690 	ld	h,-9 (ix)
   605F 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:130: enemy->health = 8;
   6061 DD 6E F4      [19]  693 	ld	l,-12 (ix)
   6064 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   6067 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:131: enemy->reward = 800;
   6069 DD 6E FE      [19]  697 	ld	l,-2 (ix)
   606C DD 66 FF      [19]  698 	ld	h,-1 (ix)
   606F 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:132: enemy->vx = move_right ? 1 : -1;
   6071 DD 4E FC      [19]  701 	ld	c,-4 (ix)
   6074 DD 46 FD      [19]  702 	ld	b,-3 (ix)
   6077 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   607A B7            [ 4]  704 	or	a, a
   607B 28 04         [12]  705 	jr	Z,00120$
   607D 3E 01         [ 7]  706 	ld	a, #0x01
   607F 18 02         [12]  707 	jr	00121$
   6081                     708 00120$:
   6081 3E FF         [ 7]  709 	ld	a, #0xff
   6083                     710 00121$:
   6083 02            [ 7]  711 	ld	(bc), a
   6084 18 20         [12]  712 	jr	00112$
   6086                     713 00104$:
                            714 ;src/entities/enemy.c:134: enemy->w = 4;
   6086 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   6089 DD 66 F9      [19]  716 	ld	h,-7 (ix)
   608C 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:135: enemy->h = 16;
   608E DD 6E F6      [19]  719 	ld	l,-10 (ix)
   6091 DD 66 F7      [19]  720 	ld	h,-9 (ix)
   6094 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:136: enemy->health = 1;
   6096 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   6099 DD 66 F5      [19]  724 	ld	h,-11 (ix)
   609C 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:137: enemy->reward = 100;
   609E DD 6E FE      [19]  727 	ld	l,-2 (ix)
   60A1 DD 66 FF      [19]  728 	ld	h,-1 (ix)
   60A4 36 64         [10]  729 	ld	(hl), #0x64
   60A6                     730 00112$:
   60A6 DD F9         [10]  731 	ld	sp, ix
   60A8 DD E1         [14]  732 	pop	ix
   60AA C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:141: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   60AB                     738 _enemyupdate::
   60AB DD E5         [15]  739 	push	ix
   60AD DD 21 00 00   [14]  740 	ld	ix,#0
   60B1 DD 39         [15]  741 	add	ix,sp
   60B3 21 F6 FF      [10]  742 	ld	hl, #-10
   60B6 39            [11]  743 	add	hl, sp
   60B7 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:145: if (!enemy || !enemy->active) {
   60B8 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   60BB DD B6 04      [19]  747 	or	a,4 (ix)
   60BE CA B2 62      [10]  748 	jp	Z,00121$
   60C1 DD 7E 04      [19]  749 	ld	a, 4 (ix)
   60C4 DD 77 FE      [19]  750 	ld	-2 (ix), a
   60C7 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   60CA DD 77 FF      [19]  752 	ld	-1 (ix), a
   60CD DD 6E FE      [19]  753 	ld	l,-2 (ix)
   60D0 DD 66 FF      [19]  754 	ld	h,-1 (ix)
   60D3 11 06 00      [10]  755 	ld	de, #0x0006
   60D6 19            [11]  756 	add	hl, de
   60D7 7E            [ 7]  757 	ld	a, (hl)
   60D8 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:146: return;
   60D9 CA B2 62      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:149: if (enemy->kind == 2) {
   60DC DD 6E FE      [19]  762 	ld	l,-2 (ix)
   60DF DD 66 FF      [19]  763 	ld	h,-1 (ix)
   60E2 11 09 00      [10]  764 	ld	de, #0x0009
   60E5 19            [11]  765 	add	hl, de
   60E6 7E            [ 7]  766 	ld	a, (hl)
   60E7 DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:150: nextx = (i16)enemy->x + (i16)enemy->vx;
   60EA DD 6E FE      [19]  769 	ld	l,-2 (ix)
   60ED DD 66 FF      [19]  770 	ld	h,-1 (ix)
   60F0 4E            [ 7]  771 	ld	c, (hl)
   60F1 DD 7E FE      [19]  772 	ld	a, -2 (ix)
   60F4 C6 02         [ 7]  773 	add	a, #0x02
   60F6 DD 77 FB      [19]  774 	ld	-5 (ix), a
   60F9 DD 7E FF      [19]  775 	ld	a, -1 (ix)
   60FC CE 00         [ 7]  776 	adc	a, #0x00
   60FE DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:151: nexty = (i16)enemy->y + (i16)enemy->vy;
   6101 DD 7E FE      [19]  779 	ld	a, -2 (ix)
   6104 C6 01         [ 7]  780 	add	a, #0x01
   6106 DD 77 F9      [19]  781 	ld	-7 (ix), a
   6109 DD 7E FF      [19]  782 	ld	a, -1 (ix)
   610C CE 00         [ 7]  783 	adc	a, #0x00
   610E DD 77 FA      [19]  784 	ld	-6 (ix), a
   6111 DD 5E FE      [19]  785 	ld	e,-2 (ix)
   6114 DD 56 FF      [19]  786 	ld	d,-1 (ix)
   6117 13            [ 6]  787 	inc	de
   6118 13            [ 6]  788 	inc	de
   6119 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:150: nextx = (i16)enemy->x + (i16)enemy->vx;
   611A 06 00         [ 7]  791 	ld	b, #0x00
   611C DD 6E FB      [19]  792 	ld	l,-5 (ix)
   611F DD 66 FC      [19]  793 	ld	h,-4 (ix)
   6122 7E            [ 7]  794 	ld	a, (hl)
   6123 DD 77 F8      [19]  795 	ld	-8 (ix), a
   6126 6F            [ 4]  796 	ld	l, a
   6127 DD 7E F8      [19]  797 	ld	a, -8 (ix)
   612A 17            [ 4]  798 	rla
   612B 9F            [ 4]  799 	sbc	a, a
   612C 67            [ 4]  800 	ld	h, a
   612D 09            [11]  801 	add	hl,bc
   612E 4D            [ 4]  802 	ld	c, l
   612F 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:149: if (enemy->kind == 2) {
   6130 DD 7E FD      [19]  805 	ld	a, -3 (ix)
   6133 D6 02         [ 7]  806 	sub	a, #0x02
   6135 C2 DE 61      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:150: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:151: nexty = (i16)enemy->y + (i16)enemy->vy;
   6138 DD 6E F9      [19]  810 	ld	l,-7 (ix)
   613B DD 66 FA      [19]  811 	ld	h,-6 (ix)
   613E 6E            [ 7]  812 	ld	l, (hl)
   613F DD 75 F6      [19]  813 	ld	-10 (ix), l
   6142 DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   6146 1A            [ 7]  815 	ld	a, (de)
   6147 6F            [ 4]  816 	ld	l, a
   6148 17            [ 4]  817 	rla
   6149 9F            [ 4]  818 	sbc	a, a
   614A 67            [ 4]  819 	ld	h, a
   614B DD 7E F6      [19]  820 	ld	a, -10 (ix)
   614E 85            [ 4]  821 	add	a, l
   614F DD 77 F6      [19]  822 	ld	-10 (ix), a
   6152 DD 7E F7      [19]  823 	ld	a, -9 (ix)
   6155 8C            [ 4]  824 	adc	a, h
   6156 DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:153: if (nextx < 8 || nextx > 72) {
   6159 79            [ 4]  827 	ld	a, c
   615A D6 08         [ 7]  828 	sub	a, #0x08
   615C 78            [ 4]  829 	ld	a, b
   615D 17            [ 4]  830 	rla
   615E 3F            [ 4]  831 	ccf
   615F 1F            [ 4]  832 	rra
   6160 DE 80         [ 7]  833 	sbc	a, #0x80
   6162 38 0E         [12]  834 	jr	C,00104$
   6164 3E 48         [ 7]  835 	ld	a, #0x48
   6166 B9            [ 4]  836 	cp	a, c
   6167 3E 00         [ 7]  837 	ld	a, #0x00
   6169 98            [ 4]  838 	sbc	a, b
   616A E2 6F 61      [10]  839 	jp	PO, 00161$
   616D EE 80         [ 7]  840 	xor	a, #0x80
   616F                     841 00161$:
   616F F2 8D 61      [10]  842 	jp	P, 00105$
   6172                     843 00104$:
                            844 ;src/entities/enemy.c:154: enemy->vx = (i8)(-enemy->vx);
   6172 AF            [ 4]  845 	xor	a, a
   6173 DD 96 F8      [19]  846 	sub	a, -8 (ix)
   6176 4F            [ 4]  847 	ld	c, a
   6177 DD 6E FB      [19]  848 	ld	l,-5 (ix)
   617A DD 66 FC      [19]  849 	ld	h,-4 (ix)
   617D 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:155: nextx = (i16)enemy->x + (i16)enemy->vx;
   617E DD 6E FE      [19]  852 	ld	l,-2 (ix)
   6181 DD 66 FF      [19]  853 	ld	h,-1 (ix)
   6184 6E            [ 7]  854 	ld	l, (hl)
   6185 26 00         [ 7]  855 	ld	h, #0x00
   6187 79            [ 4]  856 	ld	a, c
   6188 17            [ 4]  857 	rla
   6189 9F            [ 4]  858 	sbc	a, a
   618A 47            [ 4]  859 	ld	b, a
   618B 09            [11]  860 	add	hl,bc
   618C 4D            [ 4]  861 	ld	c, l
   618D                     862 00105$:
                            863 ;src/entities/enemy.c:157: if (nexty < 56 || nexty > 120) {
   618D DD 7E F6      [19]  864 	ld	a, -10 (ix)
   6190 D6 38         [ 7]  865 	sub	a, #0x38
   6192 DD 7E F7      [19]  866 	ld	a, -9 (ix)
   6195 17            [ 4]  867 	rla
   6196 3F            [ 4]  868 	ccf
   6197 1F            [ 4]  869 	rra
   6198 DE 80         [ 7]  870 	sbc	a, #0x80
   619A 38 12         [12]  871 	jr	C,00107$
   619C 3E 78         [ 7]  872 	ld	a, #0x78
   619E DD BE F6      [19]  873 	cp	a, -10 (ix)
   61A1 3E 00         [ 7]  874 	ld	a, #0x00
   61A3 DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   61A6 E2 AB 61      [10]  876 	jp	PO, 00162$
   61A9 EE 80         [ 7]  877 	xor	a, #0x80
   61AB                     878 00162$:
   61AB F2 CA 61      [10]  879 	jp	P, 00108$
   61AE                     880 00107$:
                            881 ;src/entities/enemy.c:158: enemy->vy = (i8)(-enemy->vy);
   61AE 1A            [ 7]  882 	ld	a, (de)
   61AF 6F            [ 4]  883 	ld	l, a
   61B0 AF            [ 4]  884 	xor	a, a
   61B1 95            [ 4]  885 	sub	a, l
   61B2 DD 77 F8      [19]  886 	ld	-8 (ix), a
   61B5 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:159: nexty = (i16)enemy->y + (i16)enemy->vy;
   61B6 DD 6E F9      [19]  889 	ld	l,-7 (ix)
   61B9 DD 66 FA      [19]  890 	ld	h,-6 (ix)
   61BC 5E            [ 7]  891 	ld	e, (hl)
   61BD 16 00         [ 7]  892 	ld	d, #0x00
   61BF DD 6E F8      [19]  893 	ld	l, -8 (ix)
   61C2 DD 7E F8      [19]  894 	ld	a, -8 (ix)
   61C5 17            [ 4]  895 	rla
   61C6 9F            [ 4]  896 	sbc	a, a
   61C7 67            [ 4]  897 	ld	h, a
   61C8 19            [11]  898 	add	hl,de
   61C9 E3            [19]  899 	ex	(sp), hl
   61CA                     900 00108$:
                            901 ;src/entities/enemy.c:162: enemy->x = (u8)nextx;
   61CA DD 6E FE      [19]  902 	ld	l,-2 (ix)
   61CD DD 66 FF      [19]  903 	ld	h,-1 (ix)
   61D0 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:163: enemy->y = (u8)nexty;
   61D1 DD 4E F6      [19]  906 	ld	c, -10 (ix)
   61D4 DD 6E F9      [19]  907 	ld	l,-7 (ix)
   61D7 DD 66 FA      [19]  908 	ld	h,-6 (ix)
   61DA 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:164: return;
   61DB C3 B2 62      [10]  911 	jp	00121$
   61DE                     912 00111$:
                            913 ;src/entities/enemy.c:167: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:168: if (nextx < 2) {
   61DE 79            [ 4]  915 	ld	a, c
   61DF D6 02         [ 7]  916 	sub	a, #0x02
   61E1 78            [ 4]  917 	ld	a, b
   61E2 17            [ 4]  918 	rla
   61E3 3F            [ 4]  919 	ccf
   61E4 1F            [ 4]  920 	rra
   61E5 DE 80         [ 7]  921 	sbc	a, #0x80
   61E7 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:169: nextx = 2;
   61E9 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:170: enemy->vx = 1;
   61EC DD 6E FB      [19]  926 	ld	l,-5 (ix)
   61EF DD 66 FC      [19]  927 	ld	h,-4 (ix)
   61F2 36 01         [10]  928 	ld	(hl), #0x01
   61F4                     929 00113$:
                            930 ;src/entities/enemy.c:173: i16 maxx = (i16)(80 - (i16)enemy->w);
   61F4 DD 6E FE      [19]  931 	ld	l,-2 (ix)
   61F7 DD 66 FF      [19]  932 	ld	h,-1 (ix)
   61FA 23            [ 6]  933 	inc	hl
   61FB 23            [ 6]  934 	inc	hl
   61FC 23            [ 6]  935 	inc	hl
   61FD 23            [ 6]  936 	inc	hl
   61FE 6E            [ 7]  937 	ld	l, (hl)
   61FF 26 00         [ 7]  938 	ld	h, #0x00
   6201 3E 50         [ 7]  939 	ld	a, #0x50
   6203 95            [ 4]  940 	sub	a, l
   6204 6F            [ 4]  941 	ld	l, a
   6205 3E 00         [ 7]  942 	ld	a, #0x00
   6207 9C            [ 4]  943 	sbc	a, h
   6208 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:174: if (nextx > maxx) {
   6209 7D            [ 4]  946 	ld	a, l
   620A 91            [ 4]  947 	sub	a, c
   620B 7C            [ 4]  948 	ld	a, h
   620C 98            [ 4]  949 	sbc	a, b
   620D E2 12 62      [10]  950 	jp	PO, 00163$
   6210 EE 80         [ 7]  951 	xor	a, #0x80
   6212                     952 00163$:
   6212 F2 1E 62      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:175: nextx = maxx;
   6215 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:176: enemy->vx = -1;
   6216 DD 6E FB      [19]  957 	ld	l,-5 (ix)
   6219 DD 66 FC      [19]  958 	ld	h,-4 (ix)
   621C 36 FF         [10]  959 	ld	(hl), #0xff
   621E                     960 00115$:
                            961 ;src/entities/enemy.c:179: enemy->x = (u8)nextx;
   621E DD 6E FE      [19]  962 	ld	l,-2 (ix)
   6221 DD 66 FF      [19]  963 	ld	h,-1 (ix)
   6224 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:181: enemy->vy = (i8)(enemy->vy + 1);
   6225 1A            [ 7]  966 	ld	a, (de)
   6226 4F            [ 4]  967 	ld	c, a
   6227 0C            [ 4]  968 	inc	c
   6228 79            [ 4]  969 	ld	a, c
   6229 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:182: if (enemy->vy > 3) enemy->vy = 3;
   622A 3E 03         [ 7]  972 	ld	a, #0x03
   622C 91            [ 4]  973 	sub	a, c
   622D E2 32 62      [10]  974 	jp	PO, 00164$
   6230 EE 80         [ 7]  975 	xor	a, #0x80
   6232                     976 00164$:
   6232 F2 38 62      [10]  977 	jp	P, 00117$
   6235 3E 03         [ 7]  978 	ld	a, #0x03
   6237 12            [ 7]  979 	ld	(de), a
   6238                     980 00117$:
                            981 ;src/entities/enemy.c:183: nexty = (i16)enemy->y + (i16)enemy->vy;
   6238 DD 6E F9      [19]  982 	ld	l,-7 (ix)
   623B DD 66 FA      [19]  983 	ld	h,-6 (ix)
   623E 4E            [ 7]  984 	ld	c, (hl)
   623F 06 00         [ 7]  985 	ld	b, #0x00
   6241 1A            [ 7]  986 	ld	a, (de)
   6242 6F            [ 4]  987 	ld	l, a
   6243 17            [ 4]  988 	rla
   6244 9F            [ 4]  989 	sbc	a, a
   6245 67            [ 4]  990 	ld	h, a
   6246 09            [11]  991 	add	hl, bc
   6247 E5            [11]  992 	push	hl
   6248 FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:184: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   624A DD 7E FE      [19]  995 	ld	a, -2 (ix)
   624D C6 05         [ 7]  996 	add	a, #0x05
   624F DD 77 F6      [19]  997 	ld	-10 (ix), a
   6252 DD 7E FF      [19]  998 	ld	a, -1 (ix)
   6255 CE 00         [ 7]  999 	adc	a, #0x00
   6257 DD 77 F7      [19] 1000 	ld	-9 (ix), a
   625A E1            [10] 1001 	pop	hl
   625B E5            [11] 1002 	push	hl
   625C 7E            [ 7] 1003 	ld	a, (hl)
   625D DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   6260 DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   6263 4E            [ 7] 1006 	ld	c, (hl)
   6264 06 00         [ 7] 1007 	ld	b, #0x00
   6266 D5            [11] 1008 	push	de
   6267 F5            [11] 1009 	push	af
   6268 33            [ 6] 1010 	inc	sp
   6269 FD E5         [15] 1011 	push	iy
   626B C5            [11] 1012 	push	bc
   626C CD 4D 53      [17] 1013 	call	_collision_clamp_y_at
   626F F1            [10] 1014 	pop	af
   6270 F1            [10] 1015 	pop	af
   6271 33            [ 6] 1016 	inc	sp
   6272 4D            [ 4] 1017 	ld	c, l
   6273 D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:185: enemy->y = (u8)nexty;
   6274 DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   6277 DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   627A 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:186: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   627B E1            [10] 1024 	pop	hl
   627C E5            [11] 1025 	push	hl
   627D 7E            [ 7] 1026 	ld	a, (hl)
   627E 06 00         [ 7] 1027 	ld	b, #0x00
   6280 DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   6283 DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   6286 6E            [ 7] 1030 	ld	l, (hl)
   6287 DD 75 F6      [19] 1031 	ld	-10 (ix), l
   628A DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   628E D5            [11] 1033 	push	de
   628F F5            [11] 1034 	push	af
   6290 33            [ 6] 1035 	inc	sp
   6291 C5            [11] 1036 	push	bc
   6292 DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   6295 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   6298 E5            [11] 1039 	push	hl
   6299 CD CE 52      [17] 1040 	call	_collision_is_on_ground_at
   629C F1            [10] 1041 	pop	af
   629D F1            [10] 1042 	pop	af
   629E 33            [ 6] 1043 	inc	sp
   629F D1            [10] 1044 	pop	de
   62A0 7D            [ 4] 1045 	ld	a, l
   62A1 B7            [ 4] 1046 	or	a, a
   62A2 28 0E         [12] 1047 	jr	Z,00121$
   62A4 1A            [ 7] 1048 	ld	a, (de)
   62A5 4F            [ 4] 1049 	ld	c, a
   62A6 AF            [ 4] 1050 	xor	a, a
   62A7 91            [ 4] 1051 	sub	a, c
   62A8 E2 AD 62      [10] 1052 	jp	PO, 00165$
   62AB EE 80         [ 7] 1053 	xor	a, #0x80
   62AD                    1054 00165$:
   62AD F2 B2 62      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:187: enemy->vy = 0;
   62B0 AF            [ 4] 1057 	xor	a, a
   62B1 12            [ 7] 1058 	ld	(de), a
   62B2                    1059 00121$:
   62B2 DD F9         [10] 1060 	ld	sp, ix
   62B4 DD E1         [14] 1061 	pop	ix
   62B6 C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:191: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   62B7                    1067 _enemyrender::
   62B7 DD E5         [15] 1068 	push	ix
   62B9 DD 21 00 00   [14] 1069 	ld	ix,#0
   62BD DD 39         [15] 1070 	add	ix,sp
   62BF F5            [11] 1071 	push	af
   62C0 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:195: if (!enemy || !enemy->active) {
   62C1 DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   62C4 DD B6 04      [19] 1075 	or	a,4 (ix)
   62C7 CA 44 63      [10] 1076 	jp	Z,00113$
   62CA DD 4E 04      [19] 1077 	ld	c,4 (ix)
   62CD DD 46 05      [19] 1078 	ld	b,5 (ix)
   62D0 C5            [11] 1079 	push	bc
   62D1 FD E1         [14] 1080 	pop	iy
   62D3 FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   62D6 B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:196: return;
   62D7 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:199: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   62D9 C5            [11] 1086 	push	bc
   62DA FD E1         [14] 1087 	pop	iy
   62DC FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   62DF FE 03         [ 7] 1089 	cp	a, #0x03
   62E1 20 0A         [12] 1090 	jr	NZ,00111$
   62E3 DD 36 FE 1F   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   62E7 DD 36 FF 5E   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   62EB 18 23         [12] 1093 	jr	00112$
   62ED                    1094 00111$:
                           1095 ;src/entities/enemy.c:200: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   62ED FE 02         [ 7] 1096 	cp	a, #0x02
   62EF 20 0A         [12] 1097 	jr	NZ,00108$
   62F1 DD 36 FE E3   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   62F5 DD 36 FF 5D   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   62F9 18 15         [12] 1100 	jr	00112$
   62FB                    1101 00108$:
                           1102 ;src/entities/enemy.c:201: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   62FB 3D            [ 4] 1103 	dec	a
   62FC 20 0A         [12] 1104 	jr	NZ,00105$
   62FE DD 36 FE 9D   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   6302 DD 36 FF 5D   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   6306 18 08         [12] 1107 	jr	00112$
   6308                    1108 00105$:
                           1109 ;src/entities/enemy.c:202: else sprite = enemy_kind0_sprite;
   6308 DD 36 FE 5D   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   630C DD 36 FF 5D   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   6310                    1112 00112$:
                           1113 ;src/entities/enemy.c:204: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   6310 69            [ 4] 1114 	ld	l, c
   6311 60            [ 4] 1115 	ld	h, b
   6312 23            [ 6] 1116 	inc	hl
   6313 56            [ 7] 1117 	ld	d, (hl)
   6314 0A            [ 7] 1118 	ld	a, (bc)
   6315 C5            [11] 1119 	push	bc
   6316 5F            [ 4] 1120 	ld	e, a
   6317 D5            [11] 1121 	push	de
   6318 21 00 C0      [10] 1122 	ld	hl, #0xc000
   631B E5            [11] 1123 	push	hl
   631C CD A5 6B      [17] 1124 	call	_cpct_getScreenPtr
   631F EB            [ 4] 1125 	ex	de,hl
   6320 C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:205: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   6321 C5            [11] 1128 	push	bc
   6322 FD E1         [14] 1129 	pop	iy
   6324 FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   6327 DD 77 FD      [19] 1131 	ld	-3 (ix), a
   632A 69            [ 4] 1132 	ld	l, c
   632B 60            [ 4] 1133 	ld	h, b
   632C 01 04 00      [10] 1134 	ld	bc, #0x0004
   632F 09            [11] 1135 	add	hl, bc
   6330 4E            [ 7] 1136 	ld	c, (hl)
   6331 D5            [11] 1137 	push	de
   6332 FD E1         [14] 1138 	pop	iy
   6334 DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   6337 DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   633A DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   633D C5            [11] 1142 	push	bc
   633E FD E5         [15] 1143 	push	iy
   6340 D5            [11] 1144 	push	de
   6341 CD 61 69      [17] 1145 	call	_cpct_drawSprite
   6344                    1146 00113$:
   6344 DD F9         [10] 1147 	ld	sp, ix
   6346 DD E1         [14] 1148 	pop	ix
   6348 C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:208: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   6349                    1154 _enemydamage::
   6349 DD E5         [15] 1155 	push	ix
   634B DD 21 00 00   [14] 1156 	ld	ix,#0
   634F DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:209: if (!enemy || !enemy->active) {
   6351 DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   6354 DD B6 04      [19] 1160 	or	a,4 (ix)
   6357 28 0F         [12] 1161 	jr	Z,00101$
   6359 DD 4E 04      [19] 1162 	ld	c,4 (ix)
   635C DD 46 05      [19] 1163 	ld	b,5 (ix)
   635F 21 06 00      [10] 1164 	ld	hl, #0x0006
   6362 09            [11] 1165 	add	hl,bc
   6363 EB            [ 4] 1166 	ex	de,hl
   6364 1A            [ 7] 1167 	ld	a, (de)
   6365 B7            [ 4] 1168 	or	a, a
   6366 20 04         [12] 1169 	jr	NZ,00102$
   6368                    1170 00101$:
                           1171 ;src/entities/enemy.c:210: return 0;
   6368 2E 00         [ 7] 1172 	ld	l, #0x00
   636A 18 1A         [12] 1173 	jr	00106$
   636C                    1174 00102$:
                           1175 ;src/entities/enemy.c:213: if (damage >= enemy->health) {
   636C 21 07 00      [10] 1176 	ld	hl, #0x0007
   636F 09            [11] 1177 	add	hl, bc
   6370 4E            [ 7] 1178 	ld	c, (hl)
   6371 DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   6374 91            [ 4] 1180 	sub	a, c
   6375 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:214: enemy->health = 0;
   6377 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:215: enemy->active = 0;
   6379 AF            [ 4] 1185 	xor	a, a
   637A 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:216: return 1;
   637B 2E 01         [ 7] 1188 	ld	l, #0x01
   637D 18 07         [12] 1189 	jr	00106$
   637F                    1190 00105$:
                           1191 ;src/entities/enemy.c:219: enemy->health = (u8)(enemy->health - damage);
   637F 79            [ 4] 1192 	ld	a, c
   6380 DD 96 06      [19] 1193 	sub	a, 6 (ix)
   6383 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:220: return 0;
   6384 2E 00         [ 7] 1196 	ld	l, #0x00
   6386                    1197 00106$:
   6386 DD E1         [14] 1198 	pop	ix
   6388 C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
