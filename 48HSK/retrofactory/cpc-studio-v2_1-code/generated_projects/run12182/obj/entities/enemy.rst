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
                             51 ;src/entities/enemy.c:65: void enemyinit(Enemy* enemy) {
                             52 ;	---------------------------------
                             53 ; Function enemyinit
                             54 ; ---------------------------------
   58D3                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   58D3 21 03 00      [10]   57 	ld	hl, #2+1
   58D6 39            [11]   58 	add	hl, sp
   58D7 7E            [ 7]   59 	ld	a, (hl)
   58D8 2B            [ 6]   60 	dec	hl
   58D9 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   58DA C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   58DB D1            [10]   65 	pop	de
   58DC C1            [10]   66 	pop	bc
   58DD C5            [11]   67 	push	bc
   58DE D5            [11]   68 	push	de
   58DF AF            [ 4]   69 	xor	a, a
   58E0 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   58E1 59            [ 4]   72 	ld	e, c
   58E2 50            [ 4]   73 	ld	d, b
   58E3 13            [ 6]   74 	inc	de
   58E4 AF            [ 4]   75 	xor	a, a
   58E5 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   58E6 59            [ 4]   78 	ld	e, c
   58E7 50            [ 4]   79 	ld	d, b
   58E8 13            [ 6]   80 	inc	de
   58E9 13            [ 6]   81 	inc	de
   58EA AF            [ 4]   82 	xor	a, a
   58EB 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   58EC 59            [ 4]   85 	ld	e, c
   58ED 50            [ 4]   86 	ld	d, b
   58EE 13            [ 6]   87 	inc	de
   58EF 13            [ 6]   88 	inc	de
   58F0 13            [ 6]   89 	inc	de
   58F1 AF            [ 4]   90 	xor	a, a
   58F2 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   58F3 21 04 00      [10]   93 	ld	hl, #0x0004
   58F6 09            [11]   94 	add	hl, bc
   58F7 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   58F9 21 05 00      [10]   97 	ld	hl, #0x0005
   58FC 09            [11]   98 	add	hl, bc
   58FD 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   58FF 21 06 00      [10]  101 	ld	hl, #0x0006
   5902 09            [11]  102 	add	hl, bc
   5903 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   5905 21 07 00      [10]  105 	ld	hl, #0x0007
   5908 09            [11]  106 	add	hl, bc
   5909 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   590B 21 08 00      [10]  109 	ld	hl, #0x0008
   590E 09            [11]  110 	add	hl, bc
   590F 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   5911 21 09 00      [10]  113 	ld	hl, #0x0009
   5914 09            [11]  114 	add	hl, bc
   5915 36 00         [10]  115 	ld	(hl), #0x00
   5917 C9            [10]  116 	ret
   5918                     117 _enemy_kind0_sprite:
   5918 30                  118 	.db #0x30	; 48	'0'
   5919 30                  119 	.db #0x30	; 48	'0'
   591A 30                  120 	.db #0x30	; 48	'0'
   591B 30                  121 	.db #0x30	; 48	'0'
   591C 30                  122 	.db #0x30	; 48	'0'
   591D 00                  123 	.db #0x00	; 0
   591E 00                  124 	.db #0x00	; 0
   591F 10                  125 	.db #0x10	; 16
   5920 30                  126 	.db #0x30	; 48	'0'
   5921 00                  127 	.db #0x00	; 0
   5922 00                  128 	.db #0x00	; 0
   5923 10                  129 	.db #0x10	; 16
   5924 30                  130 	.db #0x30	; 48	'0'
   5925 00                  131 	.db #0x00	; 0
   5926 00                  132 	.db #0x00	; 0
   5927 10                  133 	.db #0x10	; 16
   5928 30                  134 	.db #0x30	; 48	'0'
   5929 00                  135 	.db #0x00	; 0
   592A 00                  136 	.db #0x00	; 0
   592B 10                  137 	.db #0x10	; 16
   592C 30                  138 	.db #0x30	; 48	'0'
   592D 00                  139 	.db #0x00	; 0
   592E 00                  140 	.db #0x00	; 0
   592F 10                  141 	.db #0x10	; 16
   5930 30                  142 	.db #0x30	; 48	'0'
   5931 00                  143 	.db #0x00	; 0
   5932 00                  144 	.db #0x00	; 0
   5933 10                  145 	.db #0x10	; 16
   5934 30                  146 	.db #0x30	; 48	'0'
   5935 00                  147 	.db #0x00	; 0
   5936 00                  148 	.db #0x00	; 0
   5937 10                  149 	.db #0x10	; 16
   5938 30                  150 	.db #0x30	; 48	'0'
   5939 30                  151 	.db #0x30	; 48	'0'
   593A 30                  152 	.db #0x30	; 48	'0'
   593B 30                  153 	.db #0x30	; 48	'0'
   593C 30                  154 	.db #0x30	; 48	'0'
   593D 00                  155 	.db #0x00	; 0
   593E 00                  156 	.db #0x00	; 0
   593F 10                  157 	.db #0x10	; 16
   5940 30                  158 	.db #0x30	; 48	'0'
   5941 00                  159 	.db #0x00	; 0
   5942 00                  160 	.db #0x00	; 0
   5943 10                  161 	.db #0x10	; 16
   5944 30                  162 	.db #0x30	; 48	'0'
   5945 00                  163 	.db #0x00	; 0
   5946 00                  164 	.db #0x00	; 0
   5947 10                  165 	.db #0x10	; 16
   5948 30                  166 	.db #0x30	; 48	'0'
   5949 00                  167 	.db #0x00	; 0
   594A 00                  168 	.db #0x00	; 0
   594B 10                  169 	.db #0x10	; 16
   594C 30                  170 	.db #0x30	; 48	'0'
   594D 00                  171 	.db #0x00	; 0
   594E 00                  172 	.db #0x00	; 0
   594F 10                  173 	.db #0x10	; 16
   5950 30                  174 	.db #0x30	; 48	'0'
   5951 00                  175 	.db #0x00	; 0
   5952 00                  176 	.db #0x00	; 0
   5953 10                  177 	.db #0x10	; 16
   5954 30                  178 	.db #0x30	; 48	'0'
   5955 30                  179 	.db #0x30	; 48	'0'
   5956 30                  180 	.db #0x30	; 48	'0'
   5957 30                  181 	.db #0x30	; 48	'0'
   5958                     182 _enemy_kind1_sprite:
   5958 3F                  183 	.db #0x3f	; 63
   5959 3F                  184 	.db #0x3f	; 63
   595A 3F                  185 	.db #0x3f	; 63
   595B 3F                  186 	.db #0x3f	; 63
   595C 3F                  187 	.db #0x3f	; 63
   595D 2A                  188 	.db #0x2a	; 42
   595E 2A                  189 	.db #0x2a	; 42
   595F 00                  190 	.db #0x00	; 0
   5960 00                  191 	.db #0x00	; 0
   5961 15                  192 	.db #0x15	; 21
   5962 2A                  193 	.db #0x2a	; 42
   5963 2A                  194 	.db #0x2a	; 42
   5964 00                  195 	.db #0x00	; 0
   5965 00                  196 	.db #0x00	; 0
   5966 15                  197 	.db #0x15	; 21
   5967 2A                  198 	.db #0x2a	; 42
   5968 2A                  199 	.db #0x2a	; 42
   5969 00                  200 	.db #0x00	; 0
   596A 00                  201 	.db #0x00	; 0
   596B 15                  202 	.db #0x15	; 21
   596C 2A                  203 	.db #0x2a	; 42
   596D 2A                  204 	.db #0x2a	; 42
   596E 00                  205 	.db #0x00	; 0
   596F 00                  206 	.db #0x00	; 0
   5970 15                  207 	.db #0x15	; 21
   5971 2A                  208 	.db #0x2a	; 42
   5972 2A                  209 	.db #0x2a	; 42
   5973 00                  210 	.db #0x00	; 0
   5974 00                  211 	.db #0x00	; 0
   5975 15                  212 	.db #0x15	; 21
   5976 2A                  213 	.db #0x2a	; 42
   5977 2A                  214 	.db #0x2a	; 42
   5978 00                  215 	.db #0x00	; 0
   5979 00                  216 	.db #0x00	; 0
   597A 15                  217 	.db #0x15	; 21
   597B 3F                  218 	.db #0x3f	; 63
   597C 3F                  219 	.db #0x3f	; 63
   597D 3F                  220 	.db #0x3f	; 63
   597E 3F                  221 	.db #0x3f	; 63
   597F 3F                  222 	.db #0x3f	; 63
   5980 2A                  223 	.db #0x2a	; 42
   5981 2A                  224 	.db #0x2a	; 42
   5982 00                  225 	.db #0x00	; 0
   5983 00                  226 	.db #0x00	; 0
   5984 15                  227 	.db #0x15	; 21
   5985 2A                  228 	.db #0x2a	; 42
   5986 2A                  229 	.db #0x2a	; 42
   5987 00                  230 	.db #0x00	; 0
   5988 00                  231 	.db #0x00	; 0
   5989 15                  232 	.db #0x15	; 21
   598A 2A                  233 	.db #0x2a	; 42
   598B 2A                  234 	.db #0x2a	; 42
   598C 00                  235 	.db #0x00	; 0
   598D 00                  236 	.db #0x00	; 0
   598E 15                  237 	.db #0x15	; 21
   598F 2A                  238 	.db #0x2a	; 42
   5990 2A                  239 	.db #0x2a	; 42
   5991 00                  240 	.db #0x00	; 0
   5992 00                  241 	.db #0x00	; 0
   5993 15                  242 	.db #0x15	; 21
   5994 2A                  243 	.db #0x2a	; 42
   5995 2A                  244 	.db #0x2a	; 42
   5996 00                  245 	.db #0x00	; 0
   5997 00                  246 	.db #0x00	; 0
   5998 15                  247 	.db #0x15	; 21
   5999 3F                  248 	.db #0x3f	; 63
   599A 3F                  249 	.db #0x3f	; 63
   599B 3F                  250 	.db #0x3f	; 63
   599C 3F                  251 	.db #0x3f	; 63
   599D 3F                  252 	.db #0x3f	; 63
   599E                     253 _enemy_kind2_sprite:
   599E 0F                  254 	.db #0x0f	; 15
   599F 0F                  255 	.db #0x0f	; 15
   59A0 0F                  256 	.db #0x0f	; 15
   59A1 0F                  257 	.db #0x0f	; 15
   59A2 0F                  258 	.db #0x0f	; 15
   59A3 0F                  259 	.db #0x0f	; 15
   59A4 0A                  260 	.db #0x0a	; 10
   59A5 05                  261 	.db #0x05	; 5
   59A6 00                  262 	.db #0x00	; 0
   59A7 00                  263 	.db #0x00	; 0
   59A8 00                  264 	.db #0x00	; 0
   59A9 05                  265 	.db #0x05	; 5
   59AA 0A                  266 	.db #0x0a	; 10
   59AB 05                  267 	.db #0x05	; 5
   59AC 00                  268 	.db #0x00	; 0
   59AD 00                  269 	.db #0x00	; 0
   59AE 00                  270 	.db #0x00	; 0
   59AF 05                  271 	.db #0x05	; 5
   59B0 0A                  272 	.db #0x0a	; 10
   59B1 05                  273 	.db #0x05	; 5
   59B2 00                  274 	.db #0x00	; 0
   59B3 00                  275 	.db #0x00	; 0
   59B4 00                  276 	.db #0x00	; 0
   59B5 05                  277 	.db #0x05	; 5
   59B6 0A                  278 	.db #0x0a	; 10
   59B7 05                  279 	.db #0x05	; 5
   59B8 00                  280 	.db #0x00	; 0
   59B9 00                  281 	.db #0x00	; 0
   59BA 00                  282 	.db #0x00	; 0
   59BB 05                  283 	.db #0x05	; 5
   59BC 0F                  284 	.db #0x0f	; 15
   59BD 0F                  285 	.db #0x0f	; 15
   59BE 0F                  286 	.db #0x0f	; 15
   59BF 0F                  287 	.db #0x0f	; 15
   59C0 0F                  288 	.db #0x0f	; 15
   59C1 0F                  289 	.db #0x0f	; 15
   59C2 0A                  290 	.db #0x0a	; 10
   59C3 05                  291 	.db #0x05	; 5
   59C4 00                  292 	.db #0x00	; 0
   59C5 00                  293 	.db #0x00	; 0
   59C6 00                  294 	.db #0x00	; 0
   59C7 05                  295 	.db #0x05	; 5
   59C8 0A                  296 	.db #0x0a	; 10
   59C9 05                  297 	.db #0x05	; 5
   59CA 00                  298 	.db #0x00	; 0
   59CB 00                  299 	.db #0x00	; 0
   59CC 00                  300 	.db #0x00	; 0
   59CD 05                  301 	.db #0x05	; 5
   59CE 0A                  302 	.db #0x0a	; 10
   59CF 05                  303 	.db #0x05	; 5
   59D0 00                  304 	.db #0x00	; 0
   59D1 00                  305 	.db #0x00	; 0
   59D2 00                  306 	.db #0x00	; 0
   59D3 05                  307 	.db #0x05	; 5
   59D4 0F                  308 	.db #0x0f	; 15
   59D5 0F                  309 	.db #0x0f	; 15
   59D6 0F                  310 	.db #0x0f	; 15
   59D7 0F                  311 	.db #0x0f	; 15
   59D8 0F                  312 	.db #0x0f	; 15
   59D9 0F                  313 	.db #0x0f	; 15
   59DA                     314 _enemy_kind3_sprite:
   59DA 33                  315 	.db #0x33	; 51	'3'
   59DB 33                  316 	.db #0x33	; 51	'3'
   59DC 33                  317 	.db #0x33	; 51	'3'
   59DD 33                  318 	.db #0x33	; 51	'3'
   59DE 33                  319 	.db #0x33	; 51	'3'
   59DF 33                  320 	.db #0x33	; 51	'3'
   59E0 33                  321 	.db #0x33	; 51	'3'
   59E1 33                  322 	.db #0x33	; 51	'3'
   59E2 33                  323 	.db #0x33	; 51	'3'
   59E3 33                  324 	.db #0x33	; 51	'3'
   59E4 22                  325 	.db #0x22	; 34
   59E5 00                  326 	.db #0x00	; 0
   59E6 22                  327 	.db #0x22	; 34
   59E7 00                  328 	.db #0x00	; 0
   59E8 00                  329 	.db #0x00	; 0
   59E9 00                  330 	.db #0x00	; 0
   59EA 00                  331 	.db #0x00	; 0
   59EB 00                  332 	.db #0x00	; 0
   59EC 00                  333 	.db #0x00	; 0
   59ED 11                  334 	.db #0x11	; 17
   59EE 22                  335 	.db #0x22	; 34
   59EF 00                  336 	.db #0x00	; 0
   59F0 22                  337 	.db #0x22	; 34
   59F1 00                  338 	.db #0x00	; 0
   59F2 00                  339 	.db #0x00	; 0
   59F3 00                  340 	.db #0x00	; 0
   59F4 00                  341 	.db #0x00	; 0
   59F5 00                  342 	.db #0x00	; 0
   59F6 00                  343 	.db #0x00	; 0
   59F7 11                  344 	.db #0x11	; 17
   59F8 22                  345 	.db #0x22	; 34
   59F9 00                  346 	.db #0x00	; 0
   59FA 22                  347 	.db #0x22	; 34
   59FB 00                  348 	.db #0x00	; 0
   59FC 00                  349 	.db #0x00	; 0
   59FD 00                  350 	.db #0x00	; 0
   59FE 00                  351 	.db #0x00	; 0
   59FF 00                  352 	.db #0x00	; 0
   5A00 00                  353 	.db #0x00	; 0
   5A01 11                  354 	.db #0x11	; 17
   5A02 22                  355 	.db #0x22	; 34
   5A03 00                  356 	.db #0x00	; 0
   5A04 22                  357 	.db #0x22	; 34
   5A05 00                  358 	.db #0x00	; 0
   5A06 00                  359 	.db #0x00	; 0
   5A07 00                  360 	.db #0x00	; 0
   5A08 00                  361 	.db #0x00	; 0
   5A09 00                  362 	.db #0x00	; 0
   5A0A 00                  363 	.db #0x00	; 0
   5A0B 11                  364 	.db #0x11	; 17
   5A0C 22                  365 	.db #0x22	; 34
   5A0D 00                  366 	.db #0x00	; 0
   5A0E 22                  367 	.db #0x22	; 34
   5A0F 00                  368 	.db #0x00	; 0
   5A10 00                  369 	.db #0x00	; 0
   5A11 00                  370 	.db #0x00	; 0
   5A12 00                  371 	.db #0x00	; 0
   5A13 00                  372 	.db #0x00	; 0
   5A14 00                  373 	.db #0x00	; 0
   5A15 11                  374 	.db #0x11	; 17
   5A16 22                  375 	.db #0x22	; 34
   5A17 00                  376 	.db #0x00	; 0
   5A18 22                  377 	.db #0x22	; 34
   5A19 00                  378 	.db #0x00	; 0
   5A1A 00                  379 	.db #0x00	; 0
   5A1B 00                  380 	.db #0x00	; 0
   5A1C 00                  381 	.db #0x00	; 0
   5A1D 00                  382 	.db #0x00	; 0
   5A1E 00                  383 	.db #0x00	; 0
   5A1F 11                  384 	.db #0x11	; 17
   5A20 22                  385 	.db #0x22	; 34
   5A21 00                  386 	.db #0x00	; 0
   5A22 22                  387 	.db #0x22	; 34
   5A23 00                  388 	.db #0x00	; 0
   5A24 00                  389 	.db #0x00	; 0
   5A25 00                  390 	.db #0x00	; 0
   5A26 00                  391 	.db #0x00	; 0
   5A27 00                  392 	.db #0x00	; 0
   5A28 00                  393 	.db #0x00	; 0
   5A29 11                  394 	.db #0x11	; 17
   5A2A 22                  395 	.db #0x22	; 34
   5A2B 00                  396 	.db #0x00	; 0
   5A2C 22                  397 	.db #0x22	; 34
   5A2D 00                  398 	.db #0x00	; 0
   5A2E 00                  399 	.db #0x00	; 0
   5A2F 00                  400 	.db #0x00	; 0
   5A30 00                  401 	.db #0x00	; 0
   5A31 00                  402 	.db #0x00	; 0
   5A32 00                  403 	.db #0x00	; 0
   5A33 11                  404 	.db #0x11	; 17
   5A34 33                  405 	.db #0x33	; 51	'3'
   5A35 33                  406 	.db #0x33	; 51	'3'
   5A36 33                  407 	.db #0x33	; 51	'3'
   5A37 33                  408 	.db #0x33	; 51	'3'
   5A38 33                  409 	.db #0x33	; 51	'3'
   5A39 33                  410 	.db #0x33	; 51	'3'
   5A3A 33                  411 	.db #0x33	; 51	'3'
   5A3B 33                  412 	.db #0x33	; 51	'3'
   5A3C 33                  413 	.db #0x33	; 51	'3'
   5A3D 33                  414 	.db #0x33	; 51	'3'
   5A3E 22                  415 	.db #0x22	; 34
   5A3F 00                  416 	.db #0x00	; 0
   5A40 22                  417 	.db #0x22	; 34
   5A41 00                  418 	.db #0x00	; 0
   5A42 00                  419 	.db #0x00	; 0
   5A43 00                  420 	.db #0x00	; 0
   5A44 00                  421 	.db #0x00	; 0
   5A45 00                  422 	.db #0x00	; 0
   5A46 00                  423 	.db #0x00	; 0
   5A47 11                  424 	.db #0x11	; 17
   5A48 22                  425 	.db #0x22	; 34
   5A49 00                  426 	.db #0x00	; 0
   5A4A 22                  427 	.db #0x22	; 34
   5A4B 00                  428 	.db #0x00	; 0
   5A4C 00                  429 	.db #0x00	; 0
   5A4D 00                  430 	.db #0x00	; 0
   5A4E 00                  431 	.db #0x00	; 0
   5A4F 00                  432 	.db #0x00	; 0
   5A50 00                  433 	.db #0x00	; 0
   5A51 11                  434 	.db #0x11	; 17
   5A52 22                  435 	.db #0x22	; 34
   5A53 00                  436 	.db #0x00	; 0
   5A54 22                  437 	.db #0x22	; 34
   5A55 00                  438 	.db #0x00	; 0
   5A56 00                  439 	.db #0x00	; 0
   5A57 00                  440 	.db #0x00	; 0
   5A58 00                  441 	.db #0x00	; 0
   5A59 00                  442 	.db #0x00	; 0
   5A5A 00                  443 	.db #0x00	; 0
   5A5B 11                  444 	.db #0x11	; 17
   5A5C 22                  445 	.db #0x22	; 34
   5A5D 00                  446 	.db #0x00	; 0
   5A5E 22                  447 	.db #0x22	; 34
   5A5F 00                  448 	.db #0x00	; 0
   5A60 00                  449 	.db #0x00	; 0
   5A61 00                  450 	.db #0x00	; 0
   5A62 00                  451 	.db #0x00	; 0
   5A63 00                  452 	.db #0x00	; 0
   5A64 00                  453 	.db #0x00	; 0
   5A65 11                  454 	.db #0x11	; 17
   5A66 22                  455 	.db #0x22	; 34
   5A67 00                  456 	.db #0x00	; 0
   5A68 22                  457 	.db #0x22	; 34
   5A69 00                  458 	.db #0x00	; 0
   5A6A 00                  459 	.db #0x00	; 0
   5A6B 00                  460 	.db #0x00	; 0
   5A6C 00                  461 	.db #0x00	; 0
   5A6D 00                  462 	.db #0x00	; 0
   5A6E 00                  463 	.db #0x00	; 0
   5A6F 11                  464 	.db #0x11	; 17
   5A70 22                  465 	.db #0x22	; 34
   5A71 00                  466 	.db #0x00	; 0
   5A72 22                  467 	.db #0x22	; 34
   5A73 00                  468 	.db #0x00	; 0
   5A74 00                  469 	.db #0x00	; 0
   5A75 00                  470 	.db #0x00	; 0
   5A76 00                  471 	.db #0x00	; 0
   5A77 00                  472 	.db #0x00	; 0
   5A78 00                  473 	.db #0x00	; 0
   5A79 11                  474 	.db #0x11	; 17
   5A7A 22                  475 	.db #0x22	; 34
   5A7B 00                  476 	.db #0x00	; 0
   5A7C 22                  477 	.db #0x22	; 34
   5A7D 00                  478 	.db #0x00	; 0
   5A7E 00                  479 	.db #0x00	; 0
   5A7F 00                  480 	.db #0x00	; 0
   5A80 00                  481 	.db #0x00	; 0
   5A81 00                  482 	.db #0x00	; 0
   5A82 00                  483 	.db #0x00	; 0
   5A83 11                  484 	.db #0x11	; 17
   5A84 33                  485 	.db #0x33	; 51	'3'
   5A85 33                  486 	.db #0x33	; 51	'3'
   5A86 33                  487 	.db #0x33	; 51	'3'
   5A87 33                  488 	.db #0x33	; 51	'3'
   5A88 33                  489 	.db #0x33	; 51	'3'
   5A89 33                  490 	.db #0x33	; 51	'3'
   5A8A 33                  491 	.db #0x33	; 51	'3'
   5A8B 33                  492 	.db #0x33	; 51	'3'
   5A8C 33                  493 	.db #0x33	; 51	'3'
   5A8D 33                  494 	.db #0x33	; 51	'3'
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   5A8E                     499 _enemyspawn::
   5A8E DD E5         [15]  500 	push	ix
   5A90 DD 21 00 00   [14]  501 	ld	ix,#0
   5A94 DD 39         [15]  502 	add	ix,sp
   5A96 21 F1 FF      [10]  503 	ld	hl, #-15
   5A99 39            [11]  504 	add	hl, sp
   5A9A F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   5A9B DD 7E 05      [19]  507 	ld	a, 5 (ix)
   5A9E DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   5AA1 CA 61 5C      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   5AA4 DD 7E 04      [19]  512 	ld	a, 4 (ix)
   5AA7 DD 77 FC      [19]  513 	ld	-4 (ix), a
   5AAA DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5AAD DD 77 FD      [19]  515 	ld	-3 (ix), a
   5AB0 DD 6E FC      [19]  516 	ld	l,-4 (ix)
   5AB3 DD 66 FD      [19]  517 	ld	h,-3 (ix)
   5AB6 DD 7E 06      [19]  518 	ld	a, 6 (ix)
   5AB9 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   5ABA DD 4E FC      [19]  521 	ld	c,-4 (ix)
   5ABD DD 46 FD      [19]  522 	ld	b,-3 (ix)
   5AC0 03            [ 6]  523 	inc	bc
   5AC1 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   5AC4 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   5AC5 DD 7E FC      [19]  527 	ld	a, -4 (ix)
   5AC8 C6 02         [ 7]  528 	add	a, #0x02
   5ACA DD 77 FE      [19]  529 	ld	-2 (ix), a
   5ACD DD 7E FD      [19]  530 	ld	a, -3 (ix)
   5AD0 CE 00         [ 7]  531 	adc	a, #0x00
   5AD2 DD 77 FF      [19]  532 	ld	-1 (ix), a
   5AD5 DD 7E 09      [19]  533 	ld	a, 9 (ix)
   5AD8 B7            [ 4]  534 	or	a, a
   5AD9 28 04         [12]  535 	jr	Z,00114$
   5ADB 0E 01         [ 7]  536 	ld	c, #0x01
   5ADD 18 02         [12]  537 	jr	00115$
   5ADF                     538 00114$:
   5ADF 0E FF         [ 7]  539 	ld	c, #0xff
   5AE1                     540 00115$:
   5AE1 DD 6E FE      [19]  541 	ld	l,-2 (ix)
   5AE4 DD 66 FF      [19]  542 	ld	h,-1 (ix)
   5AE7 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   5AE8 DD 7E FC      [19]  545 	ld	a, -4 (ix)
   5AEB C6 03         [ 7]  546 	add	a, #0x03
   5AED DD 77 FA      [19]  547 	ld	-6 (ix), a
   5AF0 DD 7E FD      [19]  548 	ld	a, -3 (ix)
   5AF3 CE 00         [ 7]  549 	adc	a, #0x00
   5AF5 DD 77 FB      [19]  550 	ld	-5 (ix), a
   5AF8 DD 6E FA      [19]  551 	ld	l,-6 (ix)
   5AFB DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5AFE 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   5B00 DD 7E FC      [19]  555 	ld	a, -4 (ix)
   5B03 C6 06         [ 7]  556 	add	a, #0x06
   5B05 DD 77 F8      [19]  557 	ld	-8 (ix), a
   5B08 DD 7E FD      [19]  558 	ld	a, -3 (ix)
   5B0B CE 00         [ 7]  559 	adc	a, #0x00
   5B0D DD 77 F9      [19]  560 	ld	-7 (ix), a
   5B10 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   5B13 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   5B16 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   5B18 DD 7E FC      [19]  565 	ld	a, -4 (ix)
   5B1B C6 09         [ 7]  566 	add	a, #0x09
   5B1D DD 77 F8      [19]  567 	ld	-8 (ix), a
   5B20 DD 7E FD      [19]  568 	ld	a, -3 (ix)
   5B23 CE 00         [ 7]  569 	adc	a, #0x00
   5B25 DD 77 F9      [19]  570 	ld	-7 (ix), a
   5B28 DD 6E F8      [19]  571 	ld	l,-8 (ix)
   5B2B DD 66 F9      [19]  572 	ld	h,-7 (ix)
   5B2E DD 7E 08      [19]  573 	ld	a, 8 (ix)
   5B31 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   5B32 DD 7E FC      [19]  576 	ld	a, -4 (ix)
   5B35 C6 04         [ 7]  577 	add	a, #0x04
   5B37 DD 77 F8      [19]  578 	ld	-8 (ix), a
   5B3A DD 7E FD      [19]  579 	ld	a, -3 (ix)
   5B3D CE 00         [ 7]  580 	adc	a, #0x00
   5B3F DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   5B42 DD 7E FC      [19]  583 	ld	a, -4 (ix)
   5B45 C6 05         [ 7]  584 	add	a, #0x05
   5B47 DD 77 F6      [19]  585 	ld	-10 (ix), a
   5B4A DD 7E FD      [19]  586 	ld	a, -3 (ix)
   5B4D CE 00         [ 7]  587 	adc	a, #0x00
   5B4F DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   5B52 DD 7E FC      [19]  590 	ld	a, -4 (ix)
   5B55 C6 07         [ 7]  591 	add	a, #0x07
   5B57 DD 77 F4      [19]  592 	ld	-12 (ix), a
   5B5A DD 7E FD      [19]  593 	ld	a, -3 (ix)
   5B5D CE 00         [ 7]  594 	adc	a, #0x00
   5B5F DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   5B62 DD 7E FC      [19]  597 	ld	a, -4 (ix)
   5B65 C6 08         [ 7]  598 	add	a, #0x08
   5B67 DD 77 FC      [19]  599 	ld	-4 (ix), a
   5B6A DD 7E FD      [19]  600 	ld	a, -3 (ix)
   5B6D CE 00         [ 7]  601 	adc	a, #0x00
   5B6F DD 77 FD      [19]  602 	ld	-3 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   5B72 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   5B75 3D            [ 4]  605 	dec	a
   5B76 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   5B78 DD 6E F8      [19]  608 	ld	l,-8 (ix)
   5B7B DD 66 F9      [19]  609 	ld	h,-7 (ix)
   5B7E 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   5B80 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   5B83 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   5B86 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   5B88 DD 6E F4      [19]  616 	ld	l,-12 (ix)
   5B8B DD 66 F5      [19]  617 	ld	h,-11 (ix)
   5B8E 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   5B90 DD 6E FC      [19]  620 	ld	l,-4 (ix)
   5B93 DD 66 FD      [19]  621 	ld	h,-3 (ix)
   5B96 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   5B98 DD 7E FE      [19]  624 	ld	a, -2 (ix)
   5B9B DD 77 F2      [19]  625 	ld	-14 (ix), a
   5B9E DD 7E FF      [19]  626 	ld	a, -1 (ix)
   5BA1 DD 77 F3      [19]  627 	ld	-13 (ix), a
   5BA4 DD 7E 09      [19]  628 	ld	a, 9 (ix)
   5BA7 B7            [ 4]  629 	or	a, a
   5BA8 28 06         [12]  630 	jr	Z,00116$
   5BAA DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5BAE 18 04         [12]  632 	jr	00117$
   5BB0                     633 00116$:
   5BB0 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5BB4                     635 00117$:
   5BB4 DD 6E F2      [19]  636 	ld	l,-14 (ix)
   5BB7 DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5BBA DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5BBD 77            [ 7]  639 	ld	(hl), a
   5BBE C3 61 5C      [10]  640 	jp	00112$
   5BC1                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   5BC1 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   5BC4 D6 02         [ 7]  644 	sub	a, #0x02
   5BC6 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   5BC8 DD 6E F8      [19]  647 	ld	l,-8 (ix)
   5BCB DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5BCE 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5BD0 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   5BD3 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   5BD6 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   5BD8 DD 6E F4      [19]  655 	ld	l,-12 (ix)
   5BDB DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5BDE 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5BE0 DD 6E FC      [19]  659 	ld	l,-4 (ix)
   5BE3 DD 66 FD      [19]  660 	ld	h,-3 (ix)
   5BE6 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   5BE8 DD 4E FA      [19]  663 	ld	c,-6 (ix)
   5BEB DD 46 FB      [19]  664 	ld	b,-5 (ix)
   5BEE DD 7E 09      [19]  665 	ld	a, 9 (ix)
   5BF1 B7            [ 4]  666 	or	a, a
   5BF2 28 04         [12]  667 	jr	Z,00118$
   5BF4 3E 01         [ 7]  668 	ld	a, #0x01
   5BF6 18 02         [12]  669 	jr	00119$
   5BF8                     670 00118$:
   5BF8 3E FF         [ 7]  671 	ld	a, #0xff
   5BFA                     672 00119$:
   5BFA 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   5BFB DD 6E FE      [19]  675 	ld	l,-2 (ix)
   5BFE DD 66 FF      [19]  676 	ld	h,-1 (ix)
   5C01 36 01         [10]  677 	ld	(hl), #0x01
   5C03 18 5C         [12]  678 	jr	00112$
   5C05                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   5C05 DD 7E 08      [19]  681 	ld	a, 8 (ix)
   5C08 D6 03         [ 7]  682 	sub	a, #0x03
   5C0A 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   5C0C DD 6E F8      [19]  685 	ld	l,-8 (ix)
   5C0F DD 66 F9      [19]  686 	ld	h,-7 (ix)
   5C12 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   5C14 DD 6E F6      [19]  689 	ld	l,-10 (ix)
   5C17 DD 66 F7      [19]  690 	ld	h,-9 (ix)
   5C1A 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   5C1C DD 6E F4      [19]  693 	ld	l,-12 (ix)
   5C1F DD 66 F5      [19]  694 	ld	h,-11 (ix)
   5C22 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   5C24 DD 6E FC      [19]  697 	ld	l,-4 (ix)
   5C27 DD 66 FD      [19]  698 	ld	h,-3 (ix)
   5C2A 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   5C2C DD 4E FE      [19]  701 	ld	c,-2 (ix)
   5C2F DD 46 FF      [19]  702 	ld	b,-1 (ix)
   5C32 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   5C35 B7            [ 4]  704 	or	a, a
   5C36 28 04         [12]  705 	jr	Z,00120$
   5C38 3E 01         [ 7]  706 	ld	a, #0x01
   5C3A 18 02         [12]  707 	jr	00121$
   5C3C                     708 00120$:
   5C3C 3E FF         [ 7]  709 	ld	a, #0xff
   5C3E                     710 00121$:
   5C3E 02            [ 7]  711 	ld	(bc), a
   5C3F 18 20         [12]  712 	jr	00112$
   5C41                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   5C41 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   5C44 DD 66 F9      [19]  716 	ld	h,-7 (ix)
   5C47 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   5C49 DD 6E F6      [19]  719 	ld	l,-10 (ix)
   5C4C DD 66 F7      [19]  720 	ld	h,-9 (ix)
   5C4F 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   5C51 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   5C54 DD 66 F5      [19]  724 	ld	h,-11 (ix)
   5C57 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   5C59 DD 6E FC      [19]  727 	ld	l,-4 (ix)
   5C5C DD 66 FD      [19]  728 	ld	h,-3 (ix)
   5C5F 36 64         [10]  729 	ld	(hl), #0x64
   5C61                     730 00112$:
   5C61 DD F9         [10]  731 	ld	sp, ix
   5C63 DD E1         [14]  732 	pop	ix
   5C65 C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   5C66                     738 _enemyupdate::
   5C66 DD E5         [15]  739 	push	ix
   5C68 DD 21 00 00   [14]  740 	ld	ix,#0
   5C6C DD 39         [15]  741 	add	ix,sp
   5C6E 21 F6 FF      [10]  742 	ld	hl, #-10
   5C71 39            [11]  743 	add	hl, sp
   5C72 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   5C73 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   5C76 DD B6 04      [19]  747 	or	a,4 (ix)
   5C79 CA 6D 5E      [10]  748 	jp	Z,00121$
   5C7C DD 7E 04      [19]  749 	ld	a, 4 (ix)
   5C7F DD 77 FE      [19]  750 	ld	-2 (ix), a
   5C82 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   5C85 DD 77 FF      [19]  752 	ld	-1 (ix), a
   5C88 DD 6E FE      [19]  753 	ld	l,-2 (ix)
   5C8B DD 66 FF      [19]  754 	ld	h,-1 (ix)
   5C8E 11 06 00      [10]  755 	ld	de, #0x0006
   5C91 19            [11]  756 	add	hl, de
   5C92 7E            [ 7]  757 	ld	a, (hl)
   5C93 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   5C94 CA 6D 5E      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5C97 DD 6E FE      [19]  762 	ld	l,-2 (ix)
   5C9A DD 66 FF      [19]  763 	ld	h,-1 (ix)
   5C9D 11 09 00      [10]  764 	ld	de, #0x0009
   5CA0 19            [11]  765 	add	hl, de
   5CA1 7E            [ 7]  766 	ld	a, (hl)
   5CA2 DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5CA5 DD 6E FE      [19]  769 	ld	l,-2 (ix)
   5CA8 DD 66 FF      [19]  770 	ld	h,-1 (ix)
   5CAB 4E            [ 7]  771 	ld	c, (hl)
   5CAC DD 7E FE      [19]  772 	ld	a, -2 (ix)
   5CAF C6 02         [ 7]  773 	add	a, #0x02
   5CB1 DD 77 FB      [19]  774 	ld	-5 (ix), a
   5CB4 DD 7E FF      [19]  775 	ld	a, -1 (ix)
   5CB7 CE 00         [ 7]  776 	adc	a, #0x00
   5CB9 DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5CBC DD 7E FE      [19]  779 	ld	a, -2 (ix)
   5CBF C6 01         [ 7]  780 	add	a, #0x01
   5CC1 DD 77 F9      [19]  781 	ld	-7 (ix), a
   5CC4 DD 7E FF      [19]  782 	ld	a, -1 (ix)
   5CC7 CE 00         [ 7]  783 	adc	a, #0x00
   5CC9 DD 77 FA      [19]  784 	ld	-6 (ix), a
   5CCC DD 5E FE      [19]  785 	ld	e,-2 (ix)
   5CCF DD 56 FF      [19]  786 	ld	d,-1 (ix)
   5CD2 13            [ 6]  787 	inc	de
   5CD3 13            [ 6]  788 	inc	de
   5CD4 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5CD5 06 00         [ 7]  791 	ld	b, #0x00
   5CD7 DD 6E FB      [19]  792 	ld	l,-5 (ix)
   5CDA DD 66 FC      [19]  793 	ld	h,-4 (ix)
   5CDD 7E            [ 7]  794 	ld	a, (hl)
   5CDE DD 77 F8      [19]  795 	ld	-8 (ix), a
   5CE1 6F            [ 4]  796 	ld	l, a
   5CE2 DD 7E F8      [19]  797 	ld	a, -8 (ix)
   5CE5 17            [ 4]  798 	rla
   5CE6 9F            [ 4]  799 	sbc	a, a
   5CE7 67            [ 4]  800 	ld	h, a
   5CE8 09            [11]  801 	add	hl,bc
   5CE9 4D            [ 4]  802 	ld	c, l
   5CEA 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5CEB DD 7E FD      [19]  805 	ld	a, -3 (ix)
   5CEE D6 02         [ 7]  806 	sub	a, #0x02
   5CF0 C2 99 5D      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5CF3 DD 6E F9      [19]  810 	ld	l,-7 (ix)
   5CF6 DD 66 FA      [19]  811 	ld	h,-6 (ix)
   5CF9 6E            [ 7]  812 	ld	l, (hl)
   5CFA DD 75 F6      [19]  813 	ld	-10 (ix), l
   5CFD DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   5D01 1A            [ 7]  815 	ld	a, (de)
   5D02 6F            [ 4]  816 	ld	l, a
   5D03 17            [ 4]  817 	rla
   5D04 9F            [ 4]  818 	sbc	a, a
   5D05 67            [ 4]  819 	ld	h, a
   5D06 DD 7E F6      [19]  820 	ld	a, -10 (ix)
   5D09 85            [ 4]  821 	add	a, l
   5D0A DD 77 F6      [19]  822 	ld	-10 (ix), a
   5D0D DD 7E F7      [19]  823 	ld	a, -9 (ix)
   5D10 8C            [ 4]  824 	adc	a, h
   5D11 DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   5D14 79            [ 4]  827 	ld	a, c
   5D15 D6 08         [ 7]  828 	sub	a, #0x08
   5D17 78            [ 4]  829 	ld	a, b
   5D18 17            [ 4]  830 	rla
   5D19 3F            [ 4]  831 	ccf
   5D1A 1F            [ 4]  832 	rra
   5D1B DE 80         [ 7]  833 	sbc	a, #0x80
   5D1D 38 0E         [12]  834 	jr	C,00104$
   5D1F 3E 48         [ 7]  835 	ld	a, #0x48
   5D21 B9            [ 4]  836 	cp	a, c
   5D22 3E 00         [ 7]  837 	ld	a, #0x00
   5D24 98            [ 4]  838 	sbc	a, b
   5D25 E2 2A 5D      [10]  839 	jp	PO, 00161$
   5D28 EE 80         [ 7]  840 	xor	a, #0x80
   5D2A                     841 00161$:
   5D2A F2 48 5D      [10]  842 	jp	P, 00105$
   5D2D                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   5D2D AF            [ 4]  845 	xor	a, a
   5D2E DD 96 F8      [19]  846 	sub	a, -8 (ix)
   5D31 4F            [ 4]  847 	ld	c, a
   5D32 DD 6E FB      [19]  848 	ld	l,-5 (ix)
   5D35 DD 66 FC      [19]  849 	ld	h,-4 (ix)
   5D38 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   5D39 DD 6E FE      [19]  852 	ld	l,-2 (ix)
   5D3C DD 66 FF      [19]  853 	ld	h,-1 (ix)
   5D3F 6E            [ 7]  854 	ld	l, (hl)
   5D40 26 00         [ 7]  855 	ld	h, #0x00
   5D42 79            [ 4]  856 	ld	a, c
   5D43 17            [ 4]  857 	rla
   5D44 9F            [ 4]  858 	sbc	a, a
   5D45 47            [ 4]  859 	ld	b, a
   5D46 09            [11]  860 	add	hl,bc
   5D47 4D            [ 4]  861 	ld	c, l
   5D48                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   5D48 DD 7E F6      [19]  864 	ld	a, -10 (ix)
   5D4B D6 38         [ 7]  865 	sub	a, #0x38
   5D4D DD 7E F7      [19]  866 	ld	a, -9 (ix)
   5D50 17            [ 4]  867 	rla
   5D51 3F            [ 4]  868 	ccf
   5D52 1F            [ 4]  869 	rra
   5D53 DE 80         [ 7]  870 	sbc	a, #0x80
   5D55 38 12         [12]  871 	jr	C,00107$
   5D57 3E 78         [ 7]  872 	ld	a, #0x78
   5D59 DD BE F6      [19]  873 	cp	a, -10 (ix)
   5D5C 3E 00         [ 7]  874 	ld	a, #0x00
   5D5E DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   5D61 E2 66 5D      [10]  876 	jp	PO, 00162$
   5D64 EE 80         [ 7]  877 	xor	a, #0x80
   5D66                     878 00162$:
   5D66 F2 85 5D      [10]  879 	jp	P, 00108$
   5D69                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   5D69 1A            [ 7]  882 	ld	a, (de)
   5D6A 6F            [ 4]  883 	ld	l, a
   5D6B AF            [ 4]  884 	xor	a, a
   5D6C 95            [ 4]  885 	sub	a, l
   5D6D DD 77 F8      [19]  886 	ld	-8 (ix), a
   5D70 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   5D71 DD 6E F9      [19]  889 	ld	l,-7 (ix)
   5D74 DD 66 FA      [19]  890 	ld	h,-6 (ix)
   5D77 5E            [ 7]  891 	ld	e, (hl)
   5D78 16 00         [ 7]  892 	ld	d, #0x00
   5D7A DD 6E F8      [19]  893 	ld	l, -8 (ix)
   5D7D DD 7E F8      [19]  894 	ld	a, -8 (ix)
   5D80 17            [ 4]  895 	rla
   5D81 9F            [ 4]  896 	sbc	a, a
   5D82 67            [ 4]  897 	ld	h, a
   5D83 19            [11]  898 	add	hl,de
   5D84 E3            [19]  899 	ex	(sp), hl
   5D85                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   5D85 DD 6E FE      [19]  902 	ld	l,-2 (ix)
   5D88 DD 66 FF      [19]  903 	ld	h,-1 (ix)
   5D8B 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   5D8C DD 4E F6      [19]  906 	ld	c, -10 (ix)
   5D8F DD 6E F9      [19]  907 	ld	l,-7 (ix)
   5D92 DD 66 FA      [19]  908 	ld	h,-6 (ix)
   5D95 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   5D96 C3 6D 5E      [10]  911 	jp	00121$
   5D99                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   5D99 79            [ 4]  915 	ld	a, c
   5D9A D6 02         [ 7]  916 	sub	a, #0x02
   5D9C 78            [ 4]  917 	ld	a, b
   5D9D 17            [ 4]  918 	rla
   5D9E 3F            [ 4]  919 	ccf
   5D9F 1F            [ 4]  920 	rra
   5DA0 DE 80         [ 7]  921 	sbc	a, #0x80
   5DA2 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   5DA4 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   5DA7 DD 6E FB      [19]  926 	ld	l,-5 (ix)
   5DAA DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5DAD 36 01         [10]  928 	ld	(hl), #0x01
   5DAF                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5DAF DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5DB2 DD 66 FF      [19]  932 	ld	h,-1 (ix)
   5DB5 23            [ 6]  933 	inc	hl
   5DB6 23            [ 6]  934 	inc	hl
   5DB7 23            [ 6]  935 	inc	hl
   5DB8 23            [ 6]  936 	inc	hl
   5DB9 6E            [ 7]  937 	ld	l, (hl)
   5DBA 26 00         [ 7]  938 	ld	h, #0x00
   5DBC 3E 50         [ 7]  939 	ld	a, #0x50
   5DBE 95            [ 4]  940 	sub	a, l
   5DBF 6F            [ 4]  941 	ld	l, a
   5DC0 3E 00         [ 7]  942 	ld	a, #0x00
   5DC2 9C            [ 4]  943 	sbc	a, h
   5DC3 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5DC4 7D            [ 4]  946 	ld	a, l
   5DC5 91            [ 4]  947 	sub	a, c
   5DC6 7C            [ 4]  948 	ld	a, h
   5DC7 98            [ 4]  949 	sbc	a, b
   5DC8 E2 CD 5D      [10]  950 	jp	PO, 00163$
   5DCB EE 80         [ 7]  951 	xor	a, #0x80
   5DCD                     952 00163$:
   5DCD F2 D9 5D      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5DD0 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5DD1 DD 6E FB      [19]  957 	ld	l,-5 (ix)
   5DD4 DD 66 FC      [19]  958 	ld	h,-4 (ix)
   5DD7 36 FF         [10]  959 	ld	(hl), #0xff
   5DD9                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5DD9 DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5DDC DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5DDF 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5DE0 1A            [ 7]  966 	ld	a, (de)
   5DE1 4F            [ 4]  967 	ld	c, a
   5DE2 0C            [ 4]  968 	inc	c
   5DE3 79            [ 4]  969 	ld	a, c
   5DE4 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   5DE5 3E 03         [ 7]  972 	ld	a, #0x03
   5DE7 91            [ 4]  973 	sub	a, c
   5DE8 E2 ED 5D      [10]  974 	jp	PO, 00164$
   5DEB EE 80         [ 7]  975 	xor	a, #0x80
   5DED                     976 00164$:
   5DED F2 F3 5D      [10]  977 	jp	P, 00117$
   5DF0 3E 03         [ 7]  978 	ld	a, #0x03
   5DF2 12            [ 7]  979 	ld	(de), a
   5DF3                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   5DF3 DD 6E F9      [19]  982 	ld	l,-7 (ix)
   5DF6 DD 66 FA      [19]  983 	ld	h,-6 (ix)
   5DF9 4E            [ 7]  984 	ld	c, (hl)
   5DFA 06 00         [ 7]  985 	ld	b, #0x00
   5DFC 1A            [ 7]  986 	ld	a, (de)
   5DFD 6F            [ 4]  987 	ld	l, a
   5DFE 17            [ 4]  988 	rla
   5DFF 9F            [ 4]  989 	sbc	a, a
   5E00 67            [ 4]  990 	ld	h, a
   5E01 09            [11]  991 	add	hl, bc
   5E02 E5            [11]  992 	push	hl
   5E03 FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5E05 DD 7E FE      [19]  995 	ld	a, -2 (ix)
   5E08 C6 05         [ 7]  996 	add	a, #0x05
   5E0A DD 77 F6      [19]  997 	ld	-10 (ix), a
   5E0D DD 7E FF      [19]  998 	ld	a, -1 (ix)
   5E10 CE 00         [ 7]  999 	adc	a, #0x00
   5E12 DD 77 F7      [19] 1000 	ld	-9 (ix), a
   5E15 E1            [10] 1001 	pop	hl
   5E16 E5            [11] 1002 	push	hl
   5E17 7E            [ 7] 1003 	ld	a, (hl)
   5E18 DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   5E1B DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   5E1E 4E            [ 7] 1006 	ld	c, (hl)
   5E1F 06 00         [ 7] 1007 	ld	b, #0x00
   5E21 D5            [11] 1008 	push	de
   5E22 F5            [11] 1009 	push	af
   5E23 33            [ 6] 1010 	inc	sp
   5E24 FD E5         [15] 1011 	push	iy
   5E26 C5            [11] 1012 	push	bc
   5E27 CD 40 4C      [17] 1013 	call	_collision_clamp_y_at
   5E2A F1            [10] 1014 	pop	af
   5E2B F1            [10] 1015 	pop	af
   5E2C 33            [ 6] 1016 	inc	sp
   5E2D 4D            [ 4] 1017 	ld	c, l
   5E2E D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5E2F DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   5E32 DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   5E35 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5E36 E1            [10] 1024 	pop	hl
   5E37 E5            [11] 1025 	push	hl
   5E38 7E            [ 7] 1026 	ld	a, (hl)
   5E39 06 00         [ 7] 1027 	ld	b, #0x00
   5E3B DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   5E3E DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   5E41 6E            [ 7] 1030 	ld	l, (hl)
   5E42 DD 75 F6      [19] 1031 	ld	-10 (ix), l
   5E45 DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   5E49 D5            [11] 1033 	push	de
   5E4A F5            [11] 1034 	push	af
   5E4B 33            [ 6] 1035 	inc	sp
   5E4C C5            [11] 1036 	push	bc
   5E4D DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5E50 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5E53 E5            [11] 1039 	push	hl
   5E54 CD C1 4B      [17] 1040 	call	_collision_is_on_ground_at
   5E57 F1            [10] 1041 	pop	af
   5E58 F1            [10] 1042 	pop	af
   5E59 33            [ 6] 1043 	inc	sp
   5E5A D1            [10] 1044 	pop	de
   5E5B 7D            [ 4] 1045 	ld	a, l
   5E5C B7            [ 4] 1046 	or	a, a
   5E5D 28 0E         [12] 1047 	jr	Z,00121$
   5E5F 1A            [ 7] 1048 	ld	a, (de)
   5E60 4F            [ 4] 1049 	ld	c, a
   5E61 AF            [ 4] 1050 	xor	a, a
   5E62 91            [ 4] 1051 	sub	a, c
   5E63 E2 68 5E      [10] 1052 	jp	PO, 00165$
   5E66 EE 80         [ 7] 1053 	xor	a, #0x80
   5E68                    1054 00165$:
   5E68 F2 6D 5E      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5E6B AF            [ 4] 1057 	xor	a, a
   5E6C 12            [ 7] 1058 	ld	(de), a
   5E6D                    1059 00121$:
   5E6D DD F9         [10] 1060 	ld	sp, ix
   5E6F DD E1         [14] 1061 	pop	ix
   5E71 C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5E72                    1067 _enemyrender::
   5E72 DD E5         [15] 1068 	push	ix
   5E74 DD 21 00 00   [14] 1069 	ld	ix,#0
   5E78 DD 39         [15] 1070 	add	ix,sp
   5E7A F5            [11] 1071 	push	af
   5E7B 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5E7C DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5E7F DD B6 04      [19] 1075 	or	a,4 (ix)
   5E82 CA FF 5E      [10] 1076 	jp	Z,00113$
   5E85 DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5E88 DD 46 05      [19] 1078 	ld	b,5 (ix)
   5E8B C5            [11] 1079 	push	bc
   5E8C FD E1         [14] 1080 	pop	iy
   5E8E FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5E91 B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5E92 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5E94 C5            [11] 1086 	push	bc
   5E95 FD E1         [14] 1087 	pop	iy
   5E97 FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5E9A FE 03         [ 7] 1089 	cp	a, #0x03
   5E9C 20 0A         [12] 1090 	jr	NZ,00111$
   5E9E DD 36 FE DA   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5EA2 DD 36 FF 59   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5EA6 18 23         [12] 1093 	jr	00112$
   5EA8                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5EA8 FE 02         [ 7] 1096 	cp	a, #0x02
   5EAA 20 0A         [12] 1097 	jr	NZ,00108$
   5EAC DD 36 FE 9E   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5EB0 DD 36 FF 59   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5EB4 18 15         [12] 1100 	jr	00112$
   5EB6                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5EB6 3D            [ 4] 1103 	dec	a
   5EB7 20 0A         [12] 1104 	jr	NZ,00105$
   5EB9 DD 36 FE 58   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5EBD DD 36 FF 59   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5EC1 18 08         [12] 1107 	jr	00112$
   5EC3                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5EC3 DD 36 FE 18   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5EC7 DD 36 FF 59   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5ECB                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5ECB 69            [ 4] 1114 	ld	l, c
   5ECC 60            [ 4] 1115 	ld	h, b
   5ECD 23            [ 6] 1116 	inc	hl
   5ECE 56            [ 7] 1117 	ld	d, (hl)
   5ECF 0A            [ 7] 1118 	ld	a, (bc)
   5ED0 C5            [11] 1119 	push	bc
   5ED1 5F            [ 4] 1120 	ld	e, a
   5ED2 D5            [11] 1121 	push	de
   5ED3 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5ED6 E5            [11] 1123 	push	hl
   5ED7 CD 2D 67      [17] 1124 	call	_cpct_getScreenPtr
   5EDA EB            [ 4] 1125 	ex	de,hl
   5EDB C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5EDC C5            [11] 1128 	push	bc
   5EDD FD E1         [14] 1129 	pop	iy
   5EDF FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5EE2 DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5EE5 69            [ 4] 1132 	ld	l, c
   5EE6 60            [ 4] 1133 	ld	h, b
   5EE7 01 04 00      [10] 1134 	ld	bc, #0x0004
   5EEA 09            [11] 1135 	add	hl, bc
   5EEB 4E            [ 7] 1136 	ld	c, (hl)
   5EEC D5            [11] 1137 	push	de
   5EED FD E1         [14] 1138 	pop	iy
   5EEF DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5EF2 DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5EF5 DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5EF8 C5            [11] 1142 	push	bc
   5EF9 FD E5         [15] 1143 	push	iy
   5EFB D5            [11] 1144 	push	de
   5EFC CD 5E 65      [17] 1145 	call	_cpct_drawSprite
   5EFF                    1146 00113$:
   5EFF DD F9         [10] 1147 	ld	sp, ix
   5F01 DD E1         [14] 1148 	pop	ix
   5F03 C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5F04                    1154 _enemydamage::
   5F04 DD E5         [15] 1155 	push	ix
   5F06 DD 21 00 00   [14] 1156 	ld	ix,#0
   5F0A DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5F0C DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5F0F DD B6 04      [19] 1160 	or	a,4 (ix)
   5F12 28 0F         [12] 1161 	jr	Z,00101$
   5F14 DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5F17 DD 46 05      [19] 1163 	ld	b,5 (ix)
   5F1A 21 06 00      [10] 1164 	ld	hl, #0x0006
   5F1D 09            [11] 1165 	add	hl,bc
   5F1E EB            [ 4] 1166 	ex	de,hl
   5F1F 1A            [ 7] 1167 	ld	a, (de)
   5F20 B7            [ 4] 1168 	or	a, a
   5F21 20 04         [12] 1169 	jr	NZ,00102$
   5F23                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5F23 2E 00         [ 7] 1172 	ld	l, #0x00
   5F25 18 1A         [12] 1173 	jr	00106$
   5F27                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5F27 21 07 00      [10] 1176 	ld	hl, #0x0007
   5F2A 09            [11] 1177 	add	hl, bc
   5F2B 4E            [ 7] 1178 	ld	c, (hl)
   5F2C DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5F2F 91            [ 4] 1180 	sub	a, c
   5F30 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5F32 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5F34 AF            [ 4] 1185 	xor	a, a
   5F35 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5F36 2E 01         [ 7] 1188 	ld	l, #0x01
   5F38 18 07         [12] 1189 	jr	00106$
   5F3A                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5F3A 79            [ 4] 1192 	ld	a, c
   5F3B DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5F3E 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5F3F 2E 00         [ 7] 1196 	ld	l, #0x00
   5F41                    1197 00106$:
   5F41 DD E1         [14] 1198 	pop	ix
   5F43 C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
