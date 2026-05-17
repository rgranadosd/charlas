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
   5875                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   5875 21 03 00      [10]   57 	ld	hl, #2+1
   5878 39            [11]   58 	add	hl, sp
   5879 7E            [ 7]   59 	ld	a, (hl)
   587A 2B            [ 6]   60 	dec	hl
   587B B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   587C C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   587D D1            [10]   65 	pop	de
   587E C1            [10]   66 	pop	bc
   587F C5            [11]   67 	push	bc
   5880 D5            [11]   68 	push	de
   5881 AF            [ 4]   69 	xor	a, a
   5882 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   5883 59            [ 4]   72 	ld	e, c
   5884 50            [ 4]   73 	ld	d, b
   5885 13            [ 6]   74 	inc	de
   5886 AF            [ 4]   75 	xor	a, a
   5887 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   5888 59            [ 4]   78 	ld	e, c
   5889 50            [ 4]   79 	ld	d, b
   588A 13            [ 6]   80 	inc	de
   588B 13            [ 6]   81 	inc	de
   588C AF            [ 4]   82 	xor	a, a
   588D 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   588E 59            [ 4]   85 	ld	e, c
   588F 50            [ 4]   86 	ld	d, b
   5890 13            [ 6]   87 	inc	de
   5891 13            [ 6]   88 	inc	de
   5892 13            [ 6]   89 	inc	de
   5893 AF            [ 4]   90 	xor	a, a
   5894 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   5895 21 04 00      [10]   93 	ld	hl, #0x0004
   5898 09            [11]   94 	add	hl, bc
   5899 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   589B 21 05 00      [10]   97 	ld	hl, #0x0005
   589E 09            [11]   98 	add	hl, bc
   589F 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   58A1 21 06 00      [10]  101 	ld	hl, #0x0006
   58A4 09            [11]  102 	add	hl, bc
   58A5 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   58A7 21 07 00      [10]  105 	ld	hl, #0x0007
   58AA 09            [11]  106 	add	hl, bc
   58AB 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   58AD 21 08 00      [10]  109 	ld	hl, #0x0008
   58B0 09            [11]  110 	add	hl, bc
   58B1 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   58B3 21 09 00      [10]  113 	ld	hl, #0x0009
   58B6 09            [11]  114 	add	hl, bc
   58B7 36 00         [10]  115 	ld	(hl), #0x00
   58B9 C9            [10]  116 	ret
   58BA                     117 _enemy_kind0_sprite:
   58BA 66                  118 	.db #0x66	; 102	'f'
   58BB 66                  119 	.db #0x66	; 102	'f'
   58BC 66                  120 	.db #0x66	; 102	'f'
   58BD 66                  121 	.db #0x66	; 102	'f'
   58BE 66                  122 	.db #0x66	; 102	'f'
   58BF 66                  123 	.db #0x66	; 102	'f'
   58C0 00                  124 	.db #0x00	; 0
   58C1 66                  125 	.db #0x66	; 102	'f'
   58C2 66                  126 	.db #0x66	; 102	'f'
   58C3 66                  127 	.db #0x66	; 102	'f'
   58C4 00                  128 	.db #0x00	; 0
   58C5 66                  129 	.db #0x66	; 102	'f'
   58C6 66                  130 	.db #0x66	; 102	'f'
   58C7 66                  131 	.db #0x66	; 102	'f'
   58C8 00                  132 	.db #0x00	; 0
   58C9 66                  133 	.db #0x66	; 102	'f'
   58CA 66                  134 	.db #0x66	; 102	'f'
   58CB 66                  135 	.db #0x66	; 102	'f'
   58CC 00                  136 	.db #0x00	; 0
   58CD 66                  137 	.db #0x66	; 102	'f'
   58CE 66                  138 	.db #0x66	; 102	'f'
   58CF 66                  139 	.db #0x66	; 102	'f'
   58D0 00                  140 	.db #0x00	; 0
   58D1 66                  141 	.db #0x66	; 102	'f'
   58D2 66                  142 	.db #0x66	; 102	'f'
   58D3 66                  143 	.db #0x66	; 102	'f'
   58D4 00                  144 	.db #0x00	; 0
   58D5 66                  145 	.db #0x66	; 102	'f'
   58D6 66                  146 	.db #0x66	; 102	'f'
   58D7 66                  147 	.db #0x66	; 102	'f'
   58D8 00                  148 	.db #0x00	; 0
   58D9 66                  149 	.db #0x66	; 102	'f'
   58DA 66                  150 	.db #0x66	; 102	'f'
   58DB 66                  151 	.db #0x66	; 102	'f'
   58DC 66                  152 	.db #0x66	; 102	'f'
   58DD 66                  153 	.db #0x66	; 102	'f'
   58DE 66                  154 	.db #0x66	; 102	'f'
   58DF 66                  155 	.db #0x66	; 102	'f'
   58E0 00                  156 	.db #0x00	; 0
   58E1 66                  157 	.db #0x66	; 102	'f'
   58E2 66                  158 	.db #0x66	; 102	'f'
   58E3 66                  159 	.db #0x66	; 102	'f'
   58E4 00                  160 	.db #0x00	; 0
   58E5 66                  161 	.db #0x66	; 102	'f'
   58E6 66                  162 	.db #0x66	; 102	'f'
   58E7 66                  163 	.db #0x66	; 102	'f'
   58E8 00                  164 	.db #0x00	; 0
   58E9 66                  165 	.db #0x66	; 102	'f'
   58EA 66                  166 	.db #0x66	; 102	'f'
   58EB 66                  167 	.db #0x66	; 102	'f'
   58EC 00                  168 	.db #0x00	; 0
   58ED 66                  169 	.db #0x66	; 102	'f'
   58EE 66                  170 	.db #0x66	; 102	'f'
   58EF 66                  171 	.db #0x66	; 102	'f'
   58F0 00                  172 	.db #0x00	; 0
   58F1 66                  173 	.db #0x66	; 102	'f'
   58F2 66                  174 	.db #0x66	; 102	'f'
   58F3 66                  175 	.db #0x66	; 102	'f'
   58F4 00                  176 	.db #0x00	; 0
   58F5 66                  177 	.db #0x66	; 102	'f'
   58F6 66                  178 	.db #0x66	; 102	'f'
   58F7 66                  179 	.db #0x66	; 102	'f'
   58F8 66                  180 	.db #0x66	; 102	'f'
   58F9 66                  181 	.db #0x66	; 102	'f'
   58FA                     182 _enemy_kind1_sprite:
   58FA 99                  183 	.db #0x99	; 153
   58FB 99                  184 	.db #0x99	; 153
   58FC 99                  185 	.db #0x99	; 153
   58FD 99                  186 	.db #0x99	; 153
   58FE 99                  187 	.db #0x99	; 153
   58FF 99                  188 	.db #0x99	; 153
   5900 00                  189 	.db #0x00	; 0
   5901 99                  190 	.db #0x99	; 153
   5902 00                  191 	.db #0x00	; 0
   5903 99                  192 	.db #0x99	; 153
   5904 99                  193 	.db #0x99	; 153
   5905 00                  194 	.db #0x00	; 0
   5906 99                  195 	.db #0x99	; 153
   5907 00                  196 	.db #0x00	; 0
   5908 99                  197 	.db #0x99	; 153
   5909 99                  198 	.db #0x99	; 153
   590A 00                  199 	.db #0x00	; 0
   590B 99                  200 	.db #0x99	; 153
   590C 00                  201 	.db #0x00	; 0
   590D 99                  202 	.db #0x99	; 153
   590E 99                  203 	.db #0x99	; 153
   590F 00                  204 	.db #0x00	; 0
   5910 99                  205 	.db #0x99	; 153
   5911 00                  206 	.db #0x00	; 0
   5912 99                  207 	.db #0x99	; 153
   5913 99                  208 	.db #0x99	; 153
   5914 00                  209 	.db #0x00	; 0
   5915 99                  210 	.db #0x99	; 153
   5916 00                  211 	.db #0x00	; 0
   5917 99                  212 	.db #0x99	; 153
   5918 99                  213 	.db #0x99	; 153
   5919 00                  214 	.db #0x00	; 0
   591A 99                  215 	.db #0x99	; 153
   591B 00                  216 	.db #0x00	; 0
   591C 99                  217 	.db #0x99	; 153
   591D 99                  218 	.db #0x99	; 153
   591E 99                  219 	.db #0x99	; 153
   591F 99                  220 	.db #0x99	; 153
   5920 99                  221 	.db #0x99	; 153
   5921 99                  222 	.db #0x99	; 153
   5922 99                  223 	.db #0x99	; 153
   5923 00                  224 	.db #0x00	; 0
   5924 99                  225 	.db #0x99	; 153
   5925 00                  226 	.db #0x00	; 0
   5926 99                  227 	.db #0x99	; 153
   5927 99                  228 	.db #0x99	; 153
   5928 00                  229 	.db #0x00	; 0
   5929 99                  230 	.db #0x99	; 153
   592A 00                  231 	.db #0x00	; 0
   592B 99                  232 	.db #0x99	; 153
   592C 99                  233 	.db #0x99	; 153
   592D 00                  234 	.db #0x00	; 0
   592E 99                  235 	.db #0x99	; 153
   592F 00                  236 	.db #0x00	; 0
   5930 99                  237 	.db #0x99	; 153
   5931 99                  238 	.db #0x99	; 153
   5932 00                  239 	.db #0x00	; 0
   5933 99                  240 	.db #0x99	; 153
   5934 00                  241 	.db #0x00	; 0
   5935 99                  242 	.db #0x99	; 153
   5936 99                  243 	.db #0x99	; 153
   5937 00                  244 	.db #0x00	; 0
   5938 99                  245 	.db #0x99	; 153
   5939 00                  246 	.db #0x00	; 0
   593A 99                  247 	.db #0x99	; 153
   593B 99                  248 	.db #0x99	; 153
   593C 99                  249 	.db #0x99	; 153
   593D 99                  250 	.db #0x99	; 153
   593E 99                  251 	.db #0x99	; 153
   593F 99                  252 	.db #0x99	; 153
   5940                     253 _enemy_kind2_sprite:
   5940 CC                  254 	.db #0xcc	; 204
   5941 CC                  255 	.db #0xcc	; 204
   5942 CC                  256 	.db #0xcc	; 204
   5943 CC                  257 	.db #0xcc	; 204
   5944 CC                  258 	.db #0xcc	; 204
   5945 CC                  259 	.db #0xcc	; 204
   5946 CC                  260 	.db #0xcc	; 204
   5947 00                  261 	.db #0x00	; 0
   5948 00                  262 	.db #0x00	; 0
   5949 CC                  263 	.db #0xcc	; 204
   594A 00                  264 	.db #0x00	; 0
   594B CC                  265 	.db #0xcc	; 204
   594C CC                  266 	.db #0xcc	; 204
   594D 00                  267 	.db #0x00	; 0
   594E 00                  268 	.db #0x00	; 0
   594F CC                  269 	.db #0xcc	; 204
   5950 00                  270 	.db #0x00	; 0
   5951 CC                  271 	.db #0xcc	; 204
   5952 CC                  272 	.db #0xcc	; 204
   5953 00                  273 	.db #0x00	; 0
   5954 00                  274 	.db #0x00	; 0
   5955 CC                  275 	.db #0xcc	; 204
   5956 00                  276 	.db #0x00	; 0
   5957 CC                  277 	.db #0xcc	; 204
   5958 CC                  278 	.db #0xcc	; 204
   5959 00                  279 	.db #0x00	; 0
   595A 00                  280 	.db #0x00	; 0
   595B CC                  281 	.db #0xcc	; 204
   595C 00                  282 	.db #0x00	; 0
   595D CC                  283 	.db #0xcc	; 204
   595E CC                  284 	.db #0xcc	; 204
   595F CC                  285 	.db #0xcc	; 204
   5960 CC                  286 	.db #0xcc	; 204
   5961 CC                  287 	.db #0xcc	; 204
   5962 CC                  288 	.db #0xcc	; 204
   5963 CC                  289 	.db #0xcc	; 204
   5964 CC                  290 	.db #0xcc	; 204
   5965 00                  291 	.db #0x00	; 0
   5966 00                  292 	.db #0x00	; 0
   5967 CC                  293 	.db #0xcc	; 204
   5968 00                  294 	.db #0x00	; 0
   5969 CC                  295 	.db #0xcc	; 204
   596A CC                  296 	.db #0xcc	; 204
   596B 00                  297 	.db #0x00	; 0
   596C 00                  298 	.db #0x00	; 0
   596D CC                  299 	.db #0xcc	; 204
   596E 00                  300 	.db #0x00	; 0
   596F CC                  301 	.db #0xcc	; 204
   5970 CC                  302 	.db #0xcc	; 204
   5971 00                  303 	.db #0x00	; 0
   5972 00                  304 	.db #0x00	; 0
   5973 CC                  305 	.db #0xcc	; 204
   5974 00                  306 	.db #0x00	; 0
   5975 CC                  307 	.db #0xcc	; 204
   5976 CC                  308 	.db #0xcc	; 204
   5977 CC                  309 	.db #0xcc	; 204
   5978 CC                  310 	.db #0xcc	; 204
   5979 CC                  311 	.db #0xcc	; 204
   597A CC                  312 	.db #0xcc	; 204
   597B CC                  313 	.db #0xcc	; 204
   597C                     314 _enemy_kind3_sprite:
   597C FF                  315 	.db #0xff	; 255
   597D FF                  316 	.db #0xff	; 255
   597E FF                  317 	.db #0xff	; 255
   597F FF                  318 	.db #0xff	; 255
   5980 FF                  319 	.db #0xff	; 255
   5981 FF                  320 	.db #0xff	; 255
   5982 FF                  321 	.db #0xff	; 255
   5983 FF                  322 	.db #0xff	; 255
   5984 FF                  323 	.db #0xff	; 255
   5985 FF                  324 	.db #0xff	; 255
   5986 FF                  325 	.db #0xff	; 255
   5987 00                  326 	.db #0x00	; 0
   5988 00                  327 	.db #0x00	; 0
   5989 00                  328 	.db #0x00	; 0
   598A FF                  329 	.db #0xff	; 255
   598B 00                  330 	.db #0x00	; 0
   598C 00                  331 	.db #0x00	; 0
   598D 00                  332 	.db #0x00	; 0
   598E 00                  333 	.db #0x00	; 0
   598F FF                  334 	.db #0xff	; 255
   5990 FF                  335 	.db #0xff	; 255
   5991 00                  336 	.db #0x00	; 0
   5992 00                  337 	.db #0x00	; 0
   5993 00                  338 	.db #0x00	; 0
   5994 FF                  339 	.db #0xff	; 255
   5995 00                  340 	.db #0x00	; 0
   5996 00                  341 	.db #0x00	; 0
   5997 00                  342 	.db #0x00	; 0
   5998 00                  343 	.db #0x00	; 0
   5999 FF                  344 	.db #0xff	; 255
   599A FF                  345 	.db #0xff	; 255
   599B 00                  346 	.db #0x00	; 0
   599C 00                  347 	.db #0x00	; 0
   599D 00                  348 	.db #0x00	; 0
   599E FF                  349 	.db #0xff	; 255
   599F 00                  350 	.db #0x00	; 0
   59A0 00                  351 	.db #0x00	; 0
   59A1 00                  352 	.db #0x00	; 0
   59A2 00                  353 	.db #0x00	; 0
   59A3 FF                  354 	.db #0xff	; 255
   59A4 FF                  355 	.db #0xff	; 255
   59A5 00                  356 	.db #0x00	; 0
   59A6 00                  357 	.db #0x00	; 0
   59A7 00                  358 	.db #0x00	; 0
   59A8 FF                  359 	.db #0xff	; 255
   59A9 00                  360 	.db #0x00	; 0
   59AA 00                  361 	.db #0x00	; 0
   59AB 00                  362 	.db #0x00	; 0
   59AC 00                  363 	.db #0x00	; 0
   59AD FF                  364 	.db #0xff	; 255
   59AE FF                  365 	.db #0xff	; 255
   59AF 00                  366 	.db #0x00	; 0
   59B0 00                  367 	.db #0x00	; 0
   59B1 00                  368 	.db #0x00	; 0
   59B2 FF                  369 	.db #0xff	; 255
   59B3 00                  370 	.db #0x00	; 0
   59B4 00                  371 	.db #0x00	; 0
   59B5 00                  372 	.db #0x00	; 0
   59B6 00                  373 	.db #0x00	; 0
   59B7 FF                  374 	.db #0xff	; 255
   59B8 FF                  375 	.db #0xff	; 255
   59B9 00                  376 	.db #0x00	; 0
   59BA 00                  377 	.db #0x00	; 0
   59BB 00                  378 	.db #0x00	; 0
   59BC FF                  379 	.db #0xff	; 255
   59BD 00                  380 	.db #0x00	; 0
   59BE 00                  381 	.db #0x00	; 0
   59BF 00                  382 	.db #0x00	; 0
   59C0 00                  383 	.db #0x00	; 0
   59C1 FF                  384 	.db #0xff	; 255
   59C2 FF                  385 	.db #0xff	; 255
   59C3 00                  386 	.db #0x00	; 0
   59C4 00                  387 	.db #0x00	; 0
   59C5 00                  388 	.db #0x00	; 0
   59C6 FF                  389 	.db #0xff	; 255
   59C7 00                  390 	.db #0x00	; 0
   59C8 00                  391 	.db #0x00	; 0
   59C9 00                  392 	.db #0x00	; 0
   59CA 00                  393 	.db #0x00	; 0
   59CB FF                  394 	.db #0xff	; 255
   59CC FF                  395 	.db #0xff	; 255
   59CD 00                  396 	.db #0x00	; 0
   59CE 00                  397 	.db #0x00	; 0
   59CF 00                  398 	.db #0x00	; 0
   59D0 FF                  399 	.db #0xff	; 255
   59D1 00                  400 	.db #0x00	; 0
   59D2 00                  401 	.db #0x00	; 0
   59D3 00                  402 	.db #0x00	; 0
   59D4 00                  403 	.db #0x00	; 0
   59D5 FF                  404 	.db #0xff	; 255
   59D6 FF                  405 	.db #0xff	; 255
   59D7 FF                  406 	.db #0xff	; 255
   59D8 FF                  407 	.db #0xff	; 255
   59D9 FF                  408 	.db #0xff	; 255
   59DA FF                  409 	.db #0xff	; 255
   59DB FF                  410 	.db #0xff	; 255
   59DC FF                  411 	.db #0xff	; 255
   59DD FF                  412 	.db #0xff	; 255
   59DE FF                  413 	.db #0xff	; 255
   59DF FF                  414 	.db #0xff	; 255
   59E0 FF                  415 	.db #0xff	; 255
   59E1 00                  416 	.db #0x00	; 0
   59E2 00                  417 	.db #0x00	; 0
   59E3 00                  418 	.db #0x00	; 0
   59E4 FF                  419 	.db #0xff	; 255
   59E5 00                  420 	.db #0x00	; 0
   59E6 00                  421 	.db #0x00	; 0
   59E7 00                  422 	.db #0x00	; 0
   59E8 00                  423 	.db #0x00	; 0
   59E9 FF                  424 	.db #0xff	; 255
   59EA FF                  425 	.db #0xff	; 255
   59EB 00                  426 	.db #0x00	; 0
   59EC 00                  427 	.db #0x00	; 0
   59ED 00                  428 	.db #0x00	; 0
   59EE FF                  429 	.db #0xff	; 255
   59EF 00                  430 	.db #0x00	; 0
   59F0 00                  431 	.db #0x00	; 0
   59F1 00                  432 	.db #0x00	; 0
   59F2 00                  433 	.db #0x00	; 0
   59F3 FF                  434 	.db #0xff	; 255
   59F4 FF                  435 	.db #0xff	; 255
   59F5 00                  436 	.db #0x00	; 0
   59F6 00                  437 	.db #0x00	; 0
   59F7 00                  438 	.db #0x00	; 0
   59F8 FF                  439 	.db #0xff	; 255
   59F9 00                  440 	.db #0x00	; 0
   59FA 00                  441 	.db #0x00	; 0
   59FB 00                  442 	.db #0x00	; 0
   59FC 00                  443 	.db #0x00	; 0
   59FD FF                  444 	.db #0xff	; 255
   59FE FF                  445 	.db #0xff	; 255
   59FF 00                  446 	.db #0x00	; 0
   5A00 00                  447 	.db #0x00	; 0
   5A01 00                  448 	.db #0x00	; 0
   5A02 FF                  449 	.db #0xff	; 255
   5A03 00                  450 	.db #0x00	; 0
   5A04 00                  451 	.db #0x00	; 0
   5A05 00                  452 	.db #0x00	; 0
   5A06 00                  453 	.db #0x00	; 0
   5A07 FF                  454 	.db #0xff	; 255
   5A08 FF                  455 	.db #0xff	; 255
   5A09 00                  456 	.db #0x00	; 0
   5A0A 00                  457 	.db #0x00	; 0
   5A0B 00                  458 	.db #0x00	; 0
   5A0C FF                  459 	.db #0xff	; 255
   5A0D 00                  460 	.db #0x00	; 0
   5A0E 00                  461 	.db #0x00	; 0
   5A0F 00                  462 	.db #0x00	; 0
   5A10 00                  463 	.db #0x00	; 0
   5A11 FF                  464 	.db #0xff	; 255
   5A12 FF                  465 	.db #0xff	; 255
   5A13 00                  466 	.db #0x00	; 0
   5A14 00                  467 	.db #0x00	; 0
   5A15 00                  468 	.db #0x00	; 0
   5A16 FF                  469 	.db #0xff	; 255
   5A17 00                  470 	.db #0x00	; 0
   5A18 00                  471 	.db #0x00	; 0
   5A19 00                  472 	.db #0x00	; 0
   5A1A 00                  473 	.db #0x00	; 0
   5A1B FF                  474 	.db #0xff	; 255
   5A1C FF                  475 	.db #0xff	; 255
   5A1D 00                  476 	.db #0x00	; 0
   5A1E 00                  477 	.db #0x00	; 0
   5A1F 00                  478 	.db #0x00	; 0
   5A20 FF                  479 	.db #0xff	; 255
   5A21 00                  480 	.db #0x00	; 0
   5A22 00                  481 	.db #0x00	; 0
   5A23 00                  482 	.db #0x00	; 0
   5A24 00                  483 	.db #0x00	; 0
   5A25 FF                  484 	.db #0xff	; 255
   5A26 FF                  485 	.db #0xff	; 255
   5A27 FF                  486 	.db #0xff	; 255
   5A28 FF                  487 	.db #0xff	; 255
   5A29 FF                  488 	.db #0xff	; 255
   5A2A FF                  489 	.db #0xff	; 255
   5A2B FF                  490 	.db #0xff	; 255
   5A2C FF                  491 	.db #0xff	; 255
   5A2D FF                  492 	.db #0xff	; 255
   5A2E FF                  493 	.db #0xff	; 255
   5A2F FF                  494 	.db #0xff	; 255
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   5A30                     499 _enemyspawn::
   5A30 DD E5         [15]  500 	push	ix
   5A32 DD 21 00 00   [14]  501 	ld	ix,#0
   5A36 DD 39         [15]  502 	add	ix,sp
   5A38 21 F1 FF      [10]  503 	ld	hl, #-15
   5A3B 39            [11]  504 	add	hl, sp
   5A3C F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   5A3D DD 7E 05      [19]  507 	ld	a, 5 (ix)
   5A40 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   5A43 CA 03 5C      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   5A46 DD 7E 04      [19]  512 	ld	a, 4 (ix)
   5A49 DD 77 FC      [19]  513 	ld	-4 (ix), a
   5A4C DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5A4F DD 77 FD      [19]  515 	ld	-3 (ix), a
   5A52 DD 6E FC      [19]  516 	ld	l,-4 (ix)
   5A55 DD 66 FD      [19]  517 	ld	h,-3 (ix)
   5A58 DD 7E 06      [19]  518 	ld	a, 6 (ix)
   5A5B 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   5A5C DD 4E FC      [19]  521 	ld	c,-4 (ix)
   5A5F DD 46 FD      [19]  522 	ld	b,-3 (ix)
   5A62 03            [ 6]  523 	inc	bc
   5A63 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   5A66 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   5A67 DD 7E FC      [19]  527 	ld	a, -4 (ix)
   5A6A C6 02         [ 7]  528 	add	a, #0x02
   5A6C DD 77 FE      [19]  529 	ld	-2 (ix), a
   5A6F DD 7E FD      [19]  530 	ld	a, -3 (ix)
   5A72 CE 00         [ 7]  531 	adc	a, #0x00
   5A74 DD 77 FF      [19]  532 	ld	-1 (ix), a
   5A77 DD 7E 09      [19]  533 	ld	a, 9 (ix)
   5A7A B7            [ 4]  534 	or	a, a
   5A7B 28 04         [12]  535 	jr	Z,00114$
   5A7D 0E 01         [ 7]  536 	ld	c, #0x01
   5A7F 18 02         [12]  537 	jr	00115$
   5A81                     538 00114$:
   5A81 0E FF         [ 7]  539 	ld	c, #0xff
   5A83                     540 00115$:
   5A83 DD 6E FE      [19]  541 	ld	l,-2 (ix)
   5A86 DD 66 FF      [19]  542 	ld	h,-1 (ix)
   5A89 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   5A8A DD 7E FC      [19]  545 	ld	a, -4 (ix)
   5A8D C6 03         [ 7]  546 	add	a, #0x03
   5A8F DD 77 FA      [19]  547 	ld	-6 (ix), a
   5A92 DD 7E FD      [19]  548 	ld	a, -3 (ix)
   5A95 CE 00         [ 7]  549 	adc	a, #0x00
   5A97 DD 77 FB      [19]  550 	ld	-5 (ix), a
   5A9A DD 6E FA      [19]  551 	ld	l,-6 (ix)
   5A9D DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5AA0 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   5AA2 DD 7E FC      [19]  555 	ld	a, -4 (ix)
   5AA5 C6 06         [ 7]  556 	add	a, #0x06
   5AA7 DD 77 F8      [19]  557 	ld	-8 (ix), a
   5AAA DD 7E FD      [19]  558 	ld	a, -3 (ix)
   5AAD CE 00         [ 7]  559 	adc	a, #0x00
   5AAF DD 77 F9      [19]  560 	ld	-7 (ix), a
   5AB2 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   5AB5 DD 66 F9      [19]  562 	ld	h,-7 (ix)
   5AB8 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   5ABA DD 7E FC      [19]  565 	ld	a, -4 (ix)
   5ABD C6 09         [ 7]  566 	add	a, #0x09
   5ABF DD 77 F8      [19]  567 	ld	-8 (ix), a
   5AC2 DD 7E FD      [19]  568 	ld	a, -3 (ix)
   5AC5 CE 00         [ 7]  569 	adc	a, #0x00
   5AC7 DD 77 F9      [19]  570 	ld	-7 (ix), a
   5ACA DD 6E F8      [19]  571 	ld	l,-8 (ix)
   5ACD DD 66 F9      [19]  572 	ld	h,-7 (ix)
   5AD0 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   5AD3 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   5AD4 DD 7E FC      [19]  576 	ld	a, -4 (ix)
   5AD7 C6 04         [ 7]  577 	add	a, #0x04
   5AD9 DD 77 F8      [19]  578 	ld	-8 (ix), a
   5ADC DD 7E FD      [19]  579 	ld	a, -3 (ix)
   5ADF CE 00         [ 7]  580 	adc	a, #0x00
   5AE1 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   5AE4 DD 7E FC      [19]  583 	ld	a, -4 (ix)
   5AE7 C6 05         [ 7]  584 	add	a, #0x05
   5AE9 DD 77 F6      [19]  585 	ld	-10 (ix), a
   5AEC DD 7E FD      [19]  586 	ld	a, -3 (ix)
   5AEF CE 00         [ 7]  587 	adc	a, #0x00
   5AF1 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   5AF4 DD 7E FC      [19]  590 	ld	a, -4 (ix)
   5AF7 C6 07         [ 7]  591 	add	a, #0x07
   5AF9 DD 77 F4      [19]  592 	ld	-12 (ix), a
   5AFC DD 7E FD      [19]  593 	ld	a, -3 (ix)
   5AFF CE 00         [ 7]  594 	adc	a, #0x00
   5B01 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   5B04 DD 7E FC      [19]  597 	ld	a, -4 (ix)
   5B07 C6 08         [ 7]  598 	add	a, #0x08
   5B09 DD 77 FC      [19]  599 	ld	-4 (ix), a
   5B0C DD 7E FD      [19]  600 	ld	a, -3 (ix)
   5B0F CE 00         [ 7]  601 	adc	a, #0x00
   5B11 DD 77 FD      [19]  602 	ld	-3 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   5B14 DD 7E 08      [19]  604 	ld	a, 8 (ix)
   5B17 3D            [ 4]  605 	dec	a
   5B18 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   5B1A DD 6E F8      [19]  608 	ld	l,-8 (ix)
   5B1D DD 66 F9      [19]  609 	ld	h,-7 (ix)
   5B20 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   5B22 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   5B25 DD 66 F7      [19]  613 	ld	h,-9 (ix)
   5B28 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   5B2A DD 6E F4      [19]  616 	ld	l,-12 (ix)
   5B2D DD 66 F5      [19]  617 	ld	h,-11 (ix)
   5B30 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   5B32 DD 6E FC      [19]  620 	ld	l,-4 (ix)
   5B35 DD 66 FD      [19]  621 	ld	h,-3 (ix)
   5B38 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   5B3A DD 7E FE      [19]  624 	ld	a, -2 (ix)
   5B3D DD 77 F2      [19]  625 	ld	-14 (ix), a
   5B40 DD 7E FF      [19]  626 	ld	a, -1 (ix)
   5B43 DD 77 F3      [19]  627 	ld	-13 (ix), a
   5B46 DD 7E 09      [19]  628 	ld	a, 9 (ix)
   5B49 B7            [ 4]  629 	or	a, a
   5B4A 28 06         [12]  630 	jr	Z,00116$
   5B4C DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5B50 18 04         [12]  632 	jr	00117$
   5B52                     633 00116$:
   5B52 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5B56                     635 00117$:
   5B56 DD 6E F2      [19]  636 	ld	l,-14 (ix)
   5B59 DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5B5C DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5B5F 77            [ 7]  639 	ld	(hl), a
   5B60 C3 03 5C      [10]  640 	jp	00112$
   5B63                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   5B63 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   5B66 D6 02         [ 7]  644 	sub	a, #0x02
   5B68 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   5B6A DD 6E F8      [19]  647 	ld	l,-8 (ix)
   5B6D DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5B70 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5B72 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   5B75 DD 66 F7      [19]  652 	ld	h,-9 (ix)
   5B78 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   5B7A DD 6E F4      [19]  655 	ld	l,-12 (ix)
   5B7D DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5B80 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5B82 DD 6E FC      [19]  659 	ld	l,-4 (ix)
   5B85 DD 66 FD      [19]  660 	ld	h,-3 (ix)
   5B88 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   5B8A DD 4E FA      [19]  663 	ld	c,-6 (ix)
   5B8D DD 46 FB      [19]  664 	ld	b,-5 (ix)
   5B90 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   5B93 B7            [ 4]  666 	or	a, a
   5B94 28 04         [12]  667 	jr	Z,00118$
   5B96 3E 01         [ 7]  668 	ld	a, #0x01
   5B98 18 02         [12]  669 	jr	00119$
   5B9A                     670 00118$:
   5B9A 3E FF         [ 7]  671 	ld	a, #0xff
   5B9C                     672 00119$:
   5B9C 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   5B9D DD 6E FE      [19]  675 	ld	l,-2 (ix)
   5BA0 DD 66 FF      [19]  676 	ld	h,-1 (ix)
   5BA3 36 01         [10]  677 	ld	(hl), #0x01
   5BA5 18 5C         [12]  678 	jr	00112$
   5BA7                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   5BA7 DD 7E 08      [19]  681 	ld	a, 8 (ix)
   5BAA D6 03         [ 7]  682 	sub	a, #0x03
   5BAC 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   5BAE DD 6E F8      [19]  685 	ld	l,-8 (ix)
   5BB1 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   5BB4 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   5BB6 DD 6E F6      [19]  689 	ld	l,-10 (ix)
   5BB9 DD 66 F7      [19]  690 	ld	h,-9 (ix)
   5BBC 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   5BBE DD 6E F4      [19]  693 	ld	l,-12 (ix)
   5BC1 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   5BC4 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   5BC6 DD 6E FC      [19]  697 	ld	l,-4 (ix)
   5BC9 DD 66 FD      [19]  698 	ld	h,-3 (ix)
   5BCC 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   5BCE DD 4E FE      [19]  701 	ld	c,-2 (ix)
   5BD1 DD 46 FF      [19]  702 	ld	b,-1 (ix)
   5BD4 DD 7E 09      [19]  703 	ld	a, 9 (ix)
   5BD7 B7            [ 4]  704 	or	a, a
   5BD8 28 04         [12]  705 	jr	Z,00120$
   5BDA 3E 01         [ 7]  706 	ld	a, #0x01
   5BDC 18 02         [12]  707 	jr	00121$
   5BDE                     708 00120$:
   5BDE 3E FF         [ 7]  709 	ld	a, #0xff
   5BE0                     710 00121$:
   5BE0 02            [ 7]  711 	ld	(bc), a
   5BE1 18 20         [12]  712 	jr	00112$
   5BE3                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   5BE3 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   5BE6 DD 66 F9      [19]  716 	ld	h,-7 (ix)
   5BE9 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   5BEB DD 6E F6      [19]  719 	ld	l,-10 (ix)
   5BEE DD 66 F7      [19]  720 	ld	h,-9 (ix)
   5BF1 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   5BF3 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   5BF6 DD 66 F5      [19]  724 	ld	h,-11 (ix)
   5BF9 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   5BFB DD 6E FC      [19]  727 	ld	l,-4 (ix)
   5BFE DD 66 FD      [19]  728 	ld	h,-3 (ix)
   5C01 36 64         [10]  729 	ld	(hl), #0x64
   5C03                     730 00112$:
   5C03 DD F9         [10]  731 	ld	sp, ix
   5C05 DD E1         [14]  732 	pop	ix
   5C07 C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   5C08                     738 _enemyupdate::
   5C08 DD E5         [15]  739 	push	ix
   5C0A DD 21 00 00   [14]  740 	ld	ix,#0
   5C0E DD 39         [15]  741 	add	ix,sp
   5C10 21 F6 FF      [10]  742 	ld	hl, #-10
   5C13 39            [11]  743 	add	hl, sp
   5C14 F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   5C15 DD 7E 05      [19]  746 	ld	a, 5 (ix)
   5C18 DD B6 04      [19]  747 	or	a,4 (ix)
   5C1B CA 0F 5E      [10]  748 	jp	Z,00121$
   5C1E DD 7E 04      [19]  749 	ld	a, 4 (ix)
   5C21 DD 77 FE      [19]  750 	ld	-2 (ix), a
   5C24 DD 7E 05      [19]  751 	ld	a, 5 (ix)
   5C27 DD 77 FF      [19]  752 	ld	-1 (ix), a
   5C2A DD 6E FE      [19]  753 	ld	l,-2 (ix)
   5C2D DD 66 FF      [19]  754 	ld	h,-1 (ix)
   5C30 11 06 00      [10]  755 	ld	de, #0x0006
   5C33 19            [11]  756 	add	hl, de
   5C34 7E            [ 7]  757 	ld	a, (hl)
   5C35 B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   5C36 CA 0F 5E      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5C39 DD 6E FE      [19]  762 	ld	l,-2 (ix)
   5C3C DD 66 FF      [19]  763 	ld	h,-1 (ix)
   5C3F 11 09 00      [10]  764 	ld	de, #0x0009
   5C42 19            [11]  765 	add	hl, de
   5C43 7E            [ 7]  766 	ld	a, (hl)
   5C44 DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5C47 DD 6E FE      [19]  769 	ld	l,-2 (ix)
   5C4A DD 66 FF      [19]  770 	ld	h,-1 (ix)
   5C4D 4E            [ 7]  771 	ld	c, (hl)
   5C4E DD 7E FE      [19]  772 	ld	a, -2 (ix)
   5C51 C6 02         [ 7]  773 	add	a, #0x02
   5C53 DD 77 FB      [19]  774 	ld	-5 (ix), a
   5C56 DD 7E FF      [19]  775 	ld	a, -1 (ix)
   5C59 CE 00         [ 7]  776 	adc	a, #0x00
   5C5B DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5C5E DD 7E FE      [19]  779 	ld	a, -2 (ix)
   5C61 C6 01         [ 7]  780 	add	a, #0x01
   5C63 DD 77 F9      [19]  781 	ld	-7 (ix), a
   5C66 DD 7E FF      [19]  782 	ld	a, -1 (ix)
   5C69 CE 00         [ 7]  783 	adc	a, #0x00
   5C6B DD 77 FA      [19]  784 	ld	-6 (ix), a
   5C6E DD 5E FE      [19]  785 	ld	e,-2 (ix)
   5C71 DD 56 FF      [19]  786 	ld	d,-1 (ix)
   5C74 13            [ 6]  787 	inc	de
   5C75 13            [ 6]  788 	inc	de
   5C76 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5C77 06 00         [ 7]  791 	ld	b, #0x00
   5C79 DD 6E FB      [19]  792 	ld	l,-5 (ix)
   5C7C DD 66 FC      [19]  793 	ld	h,-4 (ix)
   5C7F 7E            [ 7]  794 	ld	a, (hl)
   5C80 DD 77 F8      [19]  795 	ld	-8 (ix), a
   5C83 6F            [ 4]  796 	ld	l, a
   5C84 DD 7E F8      [19]  797 	ld	a, -8 (ix)
   5C87 17            [ 4]  798 	rla
   5C88 9F            [ 4]  799 	sbc	a, a
   5C89 67            [ 4]  800 	ld	h, a
   5C8A 09            [11]  801 	add	hl,bc
   5C8B 4D            [ 4]  802 	ld	c, l
   5C8C 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5C8D DD 7E FD      [19]  805 	ld	a, -3 (ix)
   5C90 D6 02         [ 7]  806 	sub	a, #0x02
   5C92 C2 3B 5D      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5C95 DD 6E F9      [19]  810 	ld	l,-7 (ix)
   5C98 DD 66 FA      [19]  811 	ld	h,-6 (ix)
   5C9B 6E            [ 7]  812 	ld	l, (hl)
   5C9C DD 75 F6      [19]  813 	ld	-10 (ix), l
   5C9F DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   5CA3 1A            [ 7]  815 	ld	a, (de)
   5CA4 6F            [ 4]  816 	ld	l, a
   5CA5 17            [ 4]  817 	rla
   5CA6 9F            [ 4]  818 	sbc	a, a
   5CA7 67            [ 4]  819 	ld	h, a
   5CA8 DD 7E F6      [19]  820 	ld	a, -10 (ix)
   5CAB 85            [ 4]  821 	add	a, l
   5CAC DD 77 F6      [19]  822 	ld	-10 (ix), a
   5CAF DD 7E F7      [19]  823 	ld	a, -9 (ix)
   5CB2 8C            [ 4]  824 	adc	a, h
   5CB3 DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   5CB6 79            [ 4]  827 	ld	a, c
   5CB7 D6 08         [ 7]  828 	sub	a, #0x08
   5CB9 78            [ 4]  829 	ld	a, b
   5CBA 17            [ 4]  830 	rla
   5CBB 3F            [ 4]  831 	ccf
   5CBC 1F            [ 4]  832 	rra
   5CBD DE 80         [ 7]  833 	sbc	a, #0x80
   5CBF 38 0E         [12]  834 	jr	C,00104$
   5CC1 3E 48         [ 7]  835 	ld	a, #0x48
   5CC3 B9            [ 4]  836 	cp	a, c
   5CC4 3E 00         [ 7]  837 	ld	a, #0x00
   5CC6 98            [ 4]  838 	sbc	a, b
   5CC7 E2 CC 5C      [10]  839 	jp	PO, 00161$
   5CCA EE 80         [ 7]  840 	xor	a, #0x80
   5CCC                     841 00161$:
   5CCC F2 EA 5C      [10]  842 	jp	P, 00105$
   5CCF                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   5CCF AF            [ 4]  845 	xor	a, a
   5CD0 DD 96 F8      [19]  846 	sub	a, -8 (ix)
   5CD3 4F            [ 4]  847 	ld	c, a
   5CD4 DD 6E FB      [19]  848 	ld	l,-5 (ix)
   5CD7 DD 66 FC      [19]  849 	ld	h,-4 (ix)
   5CDA 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   5CDB DD 6E FE      [19]  852 	ld	l,-2 (ix)
   5CDE DD 66 FF      [19]  853 	ld	h,-1 (ix)
   5CE1 6E            [ 7]  854 	ld	l, (hl)
   5CE2 26 00         [ 7]  855 	ld	h, #0x00
   5CE4 79            [ 4]  856 	ld	a, c
   5CE5 17            [ 4]  857 	rla
   5CE6 9F            [ 4]  858 	sbc	a, a
   5CE7 47            [ 4]  859 	ld	b, a
   5CE8 09            [11]  860 	add	hl,bc
   5CE9 4D            [ 4]  861 	ld	c, l
   5CEA                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   5CEA DD 7E F6      [19]  864 	ld	a, -10 (ix)
   5CED D6 38         [ 7]  865 	sub	a, #0x38
   5CEF DD 7E F7      [19]  866 	ld	a, -9 (ix)
   5CF2 17            [ 4]  867 	rla
   5CF3 3F            [ 4]  868 	ccf
   5CF4 1F            [ 4]  869 	rra
   5CF5 DE 80         [ 7]  870 	sbc	a, #0x80
   5CF7 38 12         [12]  871 	jr	C,00107$
   5CF9 3E 78         [ 7]  872 	ld	a, #0x78
   5CFB DD BE F6      [19]  873 	cp	a, -10 (ix)
   5CFE 3E 00         [ 7]  874 	ld	a, #0x00
   5D00 DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   5D03 E2 08 5D      [10]  876 	jp	PO, 00162$
   5D06 EE 80         [ 7]  877 	xor	a, #0x80
   5D08                     878 00162$:
   5D08 F2 27 5D      [10]  879 	jp	P, 00108$
   5D0B                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   5D0B 1A            [ 7]  882 	ld	a, (de)
   5D0C 6F            [ 4]  883 	ld	l, a
   5D0D AF            [ 4]  884 	xor	a, a
   5D0E 95            [ 4]  885 	sub	a, l
   5D0F DD 77 F8      [19]  886 	ld	-8 (ix), a
   5D12 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   5D13 DD 6E F9      [19]  889 	ld	l,-7 (ix)
   5D16 DD 66 FA      [19]  890 	ld	h,-6 (ix)
   5D19 5E            [ 7]  891 	ld	e, (hl)
   5D1A 16 00         [ 7]  892 	ld	d, #0x00
   5D1C DD 6E F8      [19]  893 	ld	l, -8 (ix)
   5D1F DD 7E F8      [19]  894 	ld	a, -8 (ix)
   5D22 17            [ 4]  895 	rla
   5D23 9F            [ 4]  896 	sbc	a, a
   5D24 67            [ 4]  897 	ld	h, a
   5D25 19            [11]  898 	add	hl,de
   5D26 E3            [19]  899 	ex	(sp), hl
   5D27                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   5D27 DD 6E FE      [19]  902 	ld	l,-2 (ix)
   5D2A DD 66 FF      [19]  903 	ld	h,-1 (ix)
   5D2D 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   5D2E DD 4E F6      [19]  906 	ld	c, -10 (ix)
   5D31 DD 6E F9      [19]  907 	ld	l,-7 (ix)
   5D34 DD 66 FA      [19]  908 	ld	h,-6 (ix)
   5D37 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   5D38 C3 0F 5E      [10]  911 	jp	00121$
   5D3B                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   5D3B 79            [ 4]  915 	ld	a, c
   5D3C D6 02         [ 7]  916 	sub	a, #0x02
   5D3E 78            [ 4]  917 	ld	a, b
   5D3F 17            [ 4]  918 	rla
   5D40 3F            [ 4]  919 	ccf
   5D41 1F            [ 4]  920 	rra
   5D42 DE 80         [ 7]  921 	sbc	a, #0x80
   5D44 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   5D46 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   5D49 DD 6E FB      [19]  926 	ld	l,-5 (ix)
   5D4C DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5D4F 36 01         [10]  928 	ld	(hl), #0x01
   5D51                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5D51 DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5D54 DD 66 FF      [19]  932 	ld	h,-1 (ix)
   5D57 23            [ 6]  933 	inc	hl
   5D58 23            [ 6]  934 	inc	hl
   5D59 23            [ 6]  935 	inc	hl
   5D5A 23            [ 6]  936 	inc	hl
   5D5B 6E            [ 7]  937 	ld	l, (hl)
   5D5C 26 00         [ 7]  938 	ld	h, #0x00
   5D5E 3E 50         [ 7]  939 	ld	a, #0x50
   5D60 95            [ 4]  940 	sub	a, l
   5D61 6F            [ 4]  941 	ld	l, a
   5D62 3E 00         [ 7]  942 	ld	a, #0x00
   5D64 9C            [ 4]  943 	sbc	a, h
   5D65 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5D66 7D            [ 4]  946 	ld	a, l
   5D67 91            [ 4]  947 	sub	a, c
   5D68 7C            [ 4]  948 	ld	a, h
   5D69 98            [ 4]  949 	sbc	a, b
   5D6A E2 6F 5D      [10]  950 	jp	PO, 00163$
   5D6D EE 80         [ 7]  951 	xor	a, #0x80
   5D6F                     952 00163$:
   5D6F F2 7B 5D      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5D72 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5D73 DD 6E FB      [19]  957 	ld	l,-5 (ix)
   5D76 DD 66 FC      [19]  958 	ld	h,-4 (ix)
   5D79 36 FF         [10]  959 	ld	(hl), #0xff
   5D7B                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5D7B DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5D7E DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5D81 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5D82 1A            [ 7]  966 	ld	a, (de)
   5D83 4F            [ 4]  967 	ld	c, a
   5D84 0C            [ 4]  968 	inc	c
   5D85 79            [ 4]  969 	ld	a, c
   5D86 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   5D87 3E 03         [ 7]  972 	ld	a, #0x03
   5D89 91            [ 4]  973 	sub	a, c
   5D8A E2 8F 5D      [10]  974 	jp	PO, 00164$
   5D8D EE 80         [ 7]  975 	xor	a, #0x80
   5D8F                     976 00164$:
   5D8F F2 95 5D      [10]  977 	jp	P, 00117$
   5D92 3E 03         [ 7]  978 	ld	a, #0x03
   5D94 12            [ 7]  979 	ld	(de), a
   5D95                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   5D95 DD 6E F9      [19]  982 	ld	l,-7 (ix)
   5D98 DD 66 FA      [19]  983 	ld	h,-6 (ix)
   5D9B 4E            [ 7]  984 	ld	c, (hl)
   5D9C 06 00         [ 7]  985 	ld	b, #0x00
   5D9E 1A            [ 7]  986 	ld	a, (de)
   5D9F 6F            [ 4]  987 	ld	l, a
   5DA0 17            [ 4]  988 	rla
   5DA1 9F            [ 4]  989 	sbc	a, a
   5DA2 67            [ 4]  990 	ld	h, a
   5DA3 09            [11]  991 	add	hl, bc
   5DA4 E5            [11]  992 	push	hl
   5DA5 FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5DA7 DD 7E FE      [19]  995 	ld	a, -2 (ix)
   5DAA C6 05         [ 7]  996 	add	a, #0x05
   5DAC DD 77 F6      [19]  997 	ld	-10 (ix), a
   5DAF DD 7E FF      [19]  998 	ld	a, -1 (ix)
   5DB2 CE 00         [ 7]  999 	adc	a, #0x00
   5DB4 DD 77 F7      [19] 1000 	ld	-9 (ix), a
   5DB7 E1            [10] 1001 	pop	hl
   5DB8 E5            [11] 1002 	push	hl
   5DB9 7E            [ 7] 1003 	ld	a, (hl)
   5DBA DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   5DBD DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   5DC0 4E            [ 7] 1006 	ld	c, (hl)
   5DC1 06 00         [ 7] 1007 	ld	b, #0x00
   5DC3 D5            [11] 1008 	push	de
   5DC4 F5            [11] 1009 	push	af
   5DC5 33            [ 6] 1010 	inc	sp
   5DC6 FD E5         [15] 1011 	push	iy
   5DC8 C5            [11] 1012 	push	bc
   5DC9 CD 42 4C      [17] 1013 	call	_collision_clamp_y_at
   5DCC F1            [10] 1014 	pop	af
   5DCD F1            [10] 1015 	pop	af
   5DCE 33            [ 6] 1016 	inc	sp
   5DCF 4D            [ 4] 1017 	ld	c, l
   5DD0 D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5DD1 DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   5DD4 DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   5DD7 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5DD8 E1            [10] 1024 	pop	hl
   5DD9 E5            [11] 1025 	push	hl
   5DDA 7E            [ 7] 1026 	ld	a, (hl)
   5DDB 06 00         [ 7] 1027 	ld	b, #0x00
   5DDD DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   5DE0 DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   5DE3 6E            [ 7] 1030 	ld	l, (hl)
   5DE4 DD 75 F6      [19] 1031 	ld	-10 (ix), l
   5DE7 DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   5DEB D5            [11] 1033 	push	de
   5DEC F5            [11] 1034 	push	af
   5DED 33            [ 6] 1035 	inc	sp
   5DEE C5            [11] 1036 	push	bc
   5DEF DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5DF2 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5DF5 E5            [11] 1039 	push	hl
   5DF6 CD C3 4B      [17] 1040 	call	_collision_is_on_ground_at
   5DF9 F1            [10] 1041 	pop	af
   5DFA F1            [10] 1042 	pop	af
   5DFB 33            [ 6] 1043 	inc	sp
   5DFC D1            [10] 1044 	pop	de
   5DFD 7D            [ 4] 1045 	ld	a, l
   5DFE B7            [ 4] 1046 	or	a, a
   5DFF 28 0E         [12] 1047 	jr	Z,00121$
   5E01 1A            [ 7] 1048 	ld	a, (de)
   5E02 4F            [ 4] 1049 	ld	c, a
   5E03 AF            [ 4] 1050 	xor	a, a
   5E04 91            [ 4] 1051 	sub	a, c
   5E05 E2 0A 5E      [10] 1052 	jp	PO, 00165$
   5E08 EE 80         [ 7] 1053 	xor	a, #0x80
   5E0A                    1054 00165$:
   5E0A F2 0F 5E      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5E0D AF            [ 4] 1057 	xor	a, a
   5E0E 12            [ 7] 1058 	ld	(de), a
   5E0F                    1059 00121$:
   5E0F DD F9         [10] 1060 	ld	sp, ix
   5E11 DD E1         [14] 1061 	pop	ix
   5E13 C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5E14                    1067 _enemyrender::
   5E14 DD E5         [15] 1068 	push	ix
   5E16 DD 21 00 00   [14] 1069 	ld	ix,#0
   5E1A DD 39         [15] 1070 	add	ix,sp
   5E1C F5            [11] 1071 	push	af
   5E1D 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5E1E DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5E21 DD B6 04      [19] 1075 	or	a,4 (ix)
   5E24 CA A1 5E      [10] 1076 	jp	Z,00113$
   5E27 DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5E2A DD 46 05      [19] 1078 	ld	b,5 (ix)
   5E2D C5            [11] 1079 	push	bc
   5E2E FD E1         [14] 1080 	pop	iy
   5E30 FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5E33 B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5E34 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5E36 C5            [11] 1086 	push	bc
   5E37 FD E1         [14] 1087 	pop	iy
   5E39 FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5E3C FE 03         [ 7] 1089 	cp	a, #0x03
   5E3E 20 0A         [12] 1090 	jr	NZ,00111$
   5E40 DD 36 FE 7C   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5E44 DD 36 FF 59   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5E48 18 23         [12] 1093 	jr	00112$
   5E4A                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5E4A FE 02         [ 7] 1096 	cp	a, #0x02
   5E4C 20 0A         [12] 1097 	jr	NZ,00108$
   5E4E DD 36 FE 40   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5E52 DD 36 FF 59   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5E56 18 15         [12] 1100 	jr	00112$
   5E58                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5E58 3D            [ 4] 1103 	dec	a
   5E59 20 0A         [12] 1104 	jr	NZ,00105$
   5E5B DD 36 FE FA   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5E5F DD 36 FF 58   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5E63 18 08         [12] 1107 	jr	00112$
   5E65                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5E65 DD 36 FE BA   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5E69 DD 36 FF 58   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5E6D                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5E6D 69            [ 4] 1114 	ld	l, c
   5E6E 60            [ 4] 1115 	ld	h, b
   5E6F 23            [ 6] 1116 	inc	hl
   5E70 56            [ 7] 1117 	ld	d, (hl)
   5E71 0A            [ 7] 1118 	ld	a, (bc)
   5E72 C5            [11] 1119 	push	bc
   5E73 5F            [ 4] 1120 	ld	e, a
   5E74 D5            [11] 1121 	push	de
   5E75 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5E78 E5            [11] 1123 	push	hl
   5E79 CD D6 66      [17] 1124 	call	_cpct_getScreenPtr
   5E7C EB            [ 4] 1125 	ex	de,hl
   5E7D C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5E7E C5            [11] 1128 	push	bc
   5E7F FD E1         [14] 1129 	pop	iy
   5E81 FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5E84 DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5E87 69            [ 4] 1132 	ld	l, c
   5E88 60            [ 4] 1133 	ld	h, b
   5E89 01 04 00      [10] 1134 	ld	bc, #0x0004
   5E8C 09            [11] 1135 	add	hl, bc
   5E8D 4E            [ 7] 1136 	ld	c, (hl)
   5E8E D5            [11] 1137 	push	de
   5E8F FD E1         [14] 1138 	pop	iy
   5E91 DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5E94 DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5E97 DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5E9A C5            [11] 1142 	push	bc
   5E9B FD E5         [15] 1143 	push	iy
   5E9D D5            [11] 1144 	push	de
   5E9E CD 07 65      [17] 1145 	call	_cpct_drawSprite
   5EA1                    1146 00113$:
   5EA1 DD F9         [10] 1147 	ld	sp, ix
   5EA3 DD E1         [14] 1148 	pop	ix
   5EA5 C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5EA6                    1154 _enemydamage::
   5EA6 DD E5         [15] 1155 	push	ix
   5EA8 DD 21 00 00   [14] 1156 	ld	ix,#0
   5EAC DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5EAE DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5EB1 DD B6 04      [19] 1160 	or	a,4 (ix)
   5EB4 28 0F         [12] 1161 	jr	Z,00101$
   5EB6 DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5EB9 DD 46 05      [19] 1163 	ld	b,5 (ix)
   5EBC 21 06 00      [10] 1164 	ld	hl, #0x0006
   5EBF 09            [11] 1165 	add	hl,bc
   5EC0 EB            [ 4] 1166 	ex	de,hl
   5EC1 1A            [ 7] 1167 	ld	a, (de)
   5EC2 B7            [ 4] 1168 	or	a, a
   5EC3 20 04         [12] 1169 	jr	NZ,00102$
   5EC5                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5EC5 2E 00         [ 7] 1172 	ld	l, #0x00
   5EC7 18 1A         [12] 1173 	jr	00106$
   5EC9                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5EC9 21 07 00      [10] 1176 	ld	hl, #0x0007
   5ECC 09            [11] 1177 	add	hl, bc
   5ECD 4E            [ 7] 1178 	ld	c, (hl)
   5ECE DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5ED1 91            [ 4] 1180 	sub	a, c
   5ED2 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5ED4 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5ED6 AF            [ 4] 1185 	xor	a, a
   5ED7 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5ED8 2E 01         [ 7] 1188 	ld	l, #0x01
   5EDA 18 07         [12] 1189 	jr	00106$
   5EDC                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5EDC 79            [ 4] 1192 	ld	a, c
   5EDD DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5EE0 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5EE1 2E 00         [ 7] 1196 	ld	l, #0x00
   5EE3                    1197 00106$:
   5EE3 DD E1         [14] 1198 	pop	ix
   5EE5 C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
