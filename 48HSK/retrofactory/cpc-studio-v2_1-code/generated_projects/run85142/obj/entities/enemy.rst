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
   574B                      55 _enemyinit::
                             56 ;src/entities/enemy.c:66: if (!enemy) {
   574B 21 03 00      [10]   57 	ld	hl, #2+1
   574E 39            [11]   58 	add	hl, sp
   574F 7E            [ 7]   59 	ld	a, (hl)
   5750 2B            [ 6]   60 	dec	hl
   5751 B6            [ 7]   61 	or	a,(hl)
                             62 ;src/entities/enemy.c:67: return;
   5752 C8            [11]   63 	ret	Z
                             64 ;src/entities/enemy.c:70: enemy->x = 0;
   5753 D1            [10]   65 	pop	de
   5754 C1            [10]   66 	pop	bc
   5755 C5            [11]   67 	push	bc
   5756 D5            [11]   68 	push	de
   5757 AF            [ 4]   69 	xor	a, a
   5758 02            [ 7]   70 	ld	(bc), a
                             71 ;src/entities/enemy.c:71: enemy->y = 0;
   5759 59            [ 4]   72 	ld	e, c
   575A 50            [ 4]   73 	ld	d, b
   575B 13            [ 6]   74 	inc	de
   575C AF            [ 4]   75 	xor	a, a
   575D 12            [ 7]   76 	ld	(de), a
                             77 ;src/entities/enemy.c:72: enemy->vx = 0;
   575E 59            [ 4]   78 	ld	e, c
   575F 50            [ 4]   79 	ld	d, b
   5760 13            [ 6]   80 	inc	de
   5761 13            [ 6]   81 	inc	de
   5762 AF            [ 4]   82 	xor	a, a
   5763 12            [ 7]   83 	ld	(de), a
                             84 ;src/entities/enemy.c:73: enemy->vy = 0;
   5764 59            [ 4]   85 	ld	e, c
   5765 50            [ 4]   86 	ld	d, b
   5766 13            [ 6]   87 	inc	de
   5767 13            [ 6]   88 	inc	de
   5768 13            [ 6]   89 	inc	de
   5769 AF            [ 4]   90 	xor	a, a
   576A 12            [ 7]   91 	ld	(de), a
                             92 ;src/entities/enemy.c:74: enemy->w = 4;
   576B 21 04 00      [10]   93 	ld	hl, #0x0004
   576E 09            [11]   94 	add	hl, bc
   576F 36 04         [10]   95 	ld	(hl), #0x04
                             96 ;src/entities/enemy.c:75: enemy->h = 16;
   5771 21 05 00      [10]   97 	ld	hl, #0x0005
   5774 09            [11]   98 	add	hl, bc
   5775 36 10         [10]   99 	ld	(hl), #0x10
                            100 ;src/entities/enemy.c:76: enemy->active = 0;
   5777 21 06 00      [10]  101 	ld	hl, #0x0006
   577A 09            [11]  102 	add	hl, bc
   577B 36 00         [10]  103 	ld	(hl), #0x00
                            104 ;src/entities/enemy.c:77: enemy->health = 1;
   577D 21 07 00      [10]  105 	ld	hl, #0x0007
   5780 09            [11]  106 	add	hl, bc
   5781 36 01         [10]  107 	ld	(hl), #0x01
                            108 ;src/entities/enemy.c:78: enemy->reward = 100;
   5783 21 08 00      [10]  109 	ld	hl, #0x0008
   5786 09            [11]  110 	add	hl, bc
   5787 36 64         [10]  111 	ld	(hl), #0x64
                            112 ;src/entities/enemy.c:79: enemy->kind = 0;
   5789 21 09 00      [10]  113 	ld	hl, #0x0009
   578C 09            [11]  114 	add	hl, bc
   578D 36 00         [10]  115 	ld	(hl), #0x00
   578F C9            [10]  116 	ret
   5790                     117 _enemy_kind0_sprite:
   5790 66                  118 	.db #0x66	; 102	'f'
   5791 66                  119 	.db #0x66	; 102	'f'
   5792 66                  120 	.db #0x66	; 102	'f'
   5793 66                  121 	.db #0x66	; 102	'f'
   5794 66                  122 	.db #0x66	; 102	'f'
   5795 66                  123 	.db #0x66	; 102	'f'
   5796 00                  124 	.db #0x00	; 0
   5797 66                  125 	.db #0x66	; 102	'f'
   5798 66                  126 	.db #0x66	; 102	'f'
   5799 66                  127 	.db #0x66	; 102	'f'
   579A 00                  128 	.db #0x00	; 0
   579B 66                  129 	.db #0x66	; 102	'f'
   579C 66                  130 	.db #0x66	; 102	'f'
   579D 66                  131 	.db #0x66	; 102	'f'
   579E 00                  132 	.db #0x00	; 0
   579F 66                  133 	.db #0x66	; 102	'f'
   57A0 66                  134 	.db #0x66	; 102	'f'
   57A1 66                  135 	.db #0x66	; 102	'f'
   57A2 00                  136 	.db #0x00	; 0
   57A3 66                  137 	.db #0x66	; 102	'f'
   57A4 66                  138 	.db #0x66	; 102	'f'
   57A5 66                  139 	.db #0x66	; 102	'f'
   57A6 00                  140 	.db #0x00	; 0
   57A7 66                  141 	.db #0x66	; 102	'f'
   57A8 66                  142 	.db #0x66	; 102	'f'
   57A9 66                  143 	.db #0x66	; 102	'f'
   57AA 00                  144 	.db #0x00	; 0
   57AB 66                  145 	.db #0x66	; 102	'f'
   57AC 66                  146 	.db #0x66	; 102	'f'
   57AD 66                  147 	.db #0x66	; 102	'f'
   57AE 00                  148 	.db #0x00	; 0
   57AF 66                  149 	.db #0x66	; 102	'f'
   57B0 66                  150 	.db #0x66	; 102	'f'
   57B1 66                  151 	.db #0x66	; 102	'f'
   57B2 66                  152 	.db #0x66	; 102	'f'
   57B3 66                  153 	.db #0x66	; 102	'f'
   57B4 66                  154 	.db #0x66	; 102	'f'
   57B5 66                  155 	.db #0x66	; 102	'f'
   57B6 00                  156 	.db #0x00	; 0
   57B7 66                  157 	.db #0x66	; 102	'f'
   57B8 66                  158 	.db #0x66	; 102	'f'
   57B9 66                  159 	.db #0x66	; 102	'f'
   57BA 00                  160 	.db #0x00	; 0
   57BB 66                  161 	.db #0x66	; 102	'f'
   57BC 66                  162 	.db #0x66	; 102	'f'
   57BD 66                  163 	.db #0x66	; 102	'f'
   57BE 00                  164 	.db #0x00	; 0
   57BF 66                  165 	.db #0x66	; 102	'f'
   57C0 66                  166 	.db #0x66	; 102	'f'
   57C1 66                  167 	.db #0x66	; 102	'f'
   57C2 00                  168 	.db #0x00	; 0
   57C3 66                  169 	.db #0x66	; 102	'f'
   57C4 66                  170 	.db #0x66	; 102	'f'
   57C5 66                  171 	.db #0x66	; 102	'f'
   57C6 00                  172 	.db #0x00	; 0
   57C7 66                  173 	.db #0x66	; 102	'f'
   57C8 66                  174 	.db #0x66	; 102	'f'
   57C9 66                  175 	.db #0x66	; 102	'f'
   57CA 00                  176 	.db #0x00	; 0
   57CB 66                  177 	.db #0x66	; 102	'f'
   57CC 66                  178 	.db #0x66	; 102	'f'
   57CD 66                  179 	.db #0x66	; 102	'f'
   57CE 66                  180 	.db #0x66	; 102	'f'
   57CF 66                  181 	.db #0x66	; 102	'f'
   57D0                     182 _enemy_kind1_sprite:
   57D0 99                  183 	.db #0x99	; 153
   57D1 99                  184 	.db #0x99	; 153
   57D2 99                  185 	.db #0x99	; 153
   57D3 99                  186 	.db #0x99	; 153
   57D4 99                  187 	.db #0x99	; 153
   57D5 99                  188 	.db #0x99	; 153
   57D6 00                  189 	.db #0x00	; 0
   57D7 99                  190 	.db #0x99	; 153
   57D8 00                  191 	.db #0x00	; 0
   57D9 99                  192 	.db #0x99	; 153
   57DA 99                  193 	.db #0x99	; 153
   57DB 00                  194 	.db #0x00	; 0
   57DC 99                  195 	.db #0x99	; 153
   57DD 00                  196 	.db #0x00	; 0
   57DE 99                  197 	.db #0x99	; 153
   57DF 99                  198 	.db #0x99	; 153
   57E0 00                  199 	.db #0x00	; 0
   57E1 99                  200 	.db #0x99	; 153
   57E2 00                  201 	.db #0x00	; 0
   57E3 99                  202 	.db #0x99	; 153
   57E4 99                  203 	.db #0x99	; 153
   57E5 00                  204 	.db #0x00	; 0
   57E6 99                  205 	.db #0x99	; 153
   57E7 00                  206 	.db #0x00	; 0
   57E8 99                  207 	.db #0x99	; 153
   57E9 99                  208 	.db #0x99	; 153
   57EA 00                  209 	.db #0x00	; 0
   57EB 99                  210 	.db #0x99	; 153
   57EC 00                  211 	.db #0x00	; 0
   57ED 99                  212 	.db #0x99	; 153
   57EE 99                  213 	.db #0x99	; 153
   57EF 00                  214 	.db #0x00	; 0
   57F0 99                  215 	.db #0x99	; 153
   57F1 00                  216 	.db #0x00	; 0
   57F2 99                  217 	.db #0x99	; 153
   57F3 99                  218 	.db #0x99	; 153
   57F4 99                  219 	.db #0x99	; 153
   57F5 99                  220 	.db #0x99	; 153
   57F6 99                  221 	.db #0x99	; 153
   57F7 99                  222 	.db #0x99	; 153
   57F8 99                  223 	.db #0x99	; 153
   57F9 00                  224 	.db #0x00	; 0
   57FA 99                  225 	.db #0x99	; 153
   57FB 00                  226 	.db #0x00	; 0
   57FC 99                  227 	.db #0x99	; 153
   57FD 99                  228 	.db #0x99	; 153
   57FE 00                  229 	.db #0x00	; 0
   57FF 99                  230 	.db #0x99	; 153
   5800 00                  231 	.db #0x00	; 0
   5801 99                  232 	.db #0x99	; 153
   5802 99                  233 	.db #0x99	; 153
   5803 00                  234 	.db #0x00	; 0
   5804 99                  235 	.db #0x99	; 153
   5805 00                  236 	.db #0x00	; 0
   5806 99                  237 	.db #0x99	; 153
   5807 99                  238 	.db #0x99	; 153
   5808 00                  239 	.db #0x00	; 0
   5809 99                  240 	.db #0x99	; 153
   580A 00                  241 	.db #0x00	; 0
   580B 99                  242 	.db #0x99	; 153
   580C 99                  243 	.db #0x99	; 153
   580D 00                  244 	.db #0x00	; 0
   580E 99                  245 	.db #0x99	; 153
   580F 00                  246 	.db #0x00	; 0
   5810 99                  247 	.db #0x99	; 153
   5811 99                  248 	.db #0x99	; 153
   5812 99                  249 	.db #0x99	; 153
   5813 99                  250 	.db #0x99	; 153
   5814 99                  251 	.db #0x99	; 153
   5815 99                  252 	.db #0x99	; 153
   5816                     253 _enemy_kind2_sprite:
   5816 CC                  254 	.db #0xcc	; 204
   5817 CC                  255 	.db #0xcc	; 204
   5818 CC                  256 	.db #0xcc	; 204
   5819 CC                  257 	.db #0xcc	; 204
   581A CC                  258 	.db #0xcc	; 204
   581B CC                  259 	.db #0xcc	; 204
   581C CC                  260 	.db #0xcc	; 204
   581D 00                  261 	.db #0x00	; 0
   581E 00                  262 	.db #0x00	; 0
   581F CC                  263 	.db #0xcc	; 204
   5820 00                  264 	.db #0x00	; 0
   5821 CC                  265 	.db #0xcc	; 204
   5822 CC                  266 	.db #0xcc	; 204
   5823 00                  267 	.db #0x00	; 0
   5824 00                  268 	.db #0x00	; 0
   5825 CC                  269 	.db #0xcc	; 204
   5826 00                  270 	.db #0x00	; 0
   5827 CC                  271 	.db #0xcc	; 204
   5828 CC                  272 	.db #0xcc	; 204
   5829 00                  273 	.db #0x00	; 0
   582A 00                  274 	.db #0x00	; 0
   582B CC                  275 	.db #0xcc	; 204
   582C 00                  276 	.db #0x00	; 0
   582D CC                  277 	.db #0xcc	; 204
   582E CC                  278 	.db #0xcc	; 204
   582F 00                  279 	.db #0x00	; 0
   5830 00                  280 	.db #0x00	; 0
   5831 CC                  281 	.db #0xcc	; 204
   5832 00                  282 	.db #0x00	; 0
   5833 CC                  283 	.db #0xcc	; 204
   5834 CC                  284 	.db #0xcc	; 204
   5835 CC                  285 	.db #0xcc	; 204
   5836 CC                  286 	.db #0xcc	; 204
   5837 CC                  287 	.db #0xcc	; 204
   5838 CC                  288 	.db #0xcc	; 204
   5839 CC                  289 	.db #0xcc	; 204
   583A CC                  290 	.db #0xcc	; 204
   583B 00                  291 	.db #0x00	; 0
   583C 00                  292 	.db #0x00	; 0
   583D CC                  293 	.db #0xcc	; 204
   583E 00                  294 	.db #0x00	; 0
   583F CC                  295 	.db #0xcc	; 204
   5840 CC                  296 	.db #0xcc	; 204
   5841 00                  297 	.db #0x00	; 0
   5842 00                  298 	.db #0x00	; 0
   5843 CC                  299 	.db #0xcc	; 204
   5844 00                  300 	.db #0x00	; 0
   5845 CC                  301 	.db #0xcc	; 204
   5846 CC                  302 	.db #0xcc	; 204
   5847 00                  303 	.db #0x00	; 0
   5848 00                  304 	.db #0x00	; 0
   5849 CC                  305 	.db #0xcc	; 204
   584A 00                  306 	.db #0x00	; 0
   584B CC                  307 	.db #0xcc	; 204
   584C CC                  308 	.db #0xcc	; 204
   584D CC                  309 	.db #0xcc	; 204
   584E CC                  310 	.db #0xcc	; 204
   584F CC                  311 	.db #0xcc	; 204
   5850 CC                  312 	.db #0xcc	; 204
   5851 CC                  313 	.db #0xcc	; 204
   5852                     314 _enemy_kind3_sprite:
   5852 FF                  315 	.db #0xff	; 255
   5853 FF                  316 	.db #0xff	; 255
   5854 FF                  317 	.db #0xff	; 255
   5855 FF                  318 	.db #0xff	; 255
   5856 FF                  319 	.db #0xff	; 255
   5857 FF                  320 	.db #0xff	; 255
   5858 FF                  321 	.db #0xff	; 255
   5859 FF                  322 	.db #0xff	; 255
   585A FF                  323 	.db #0xff	; 255
   585B FF                  324 	.db #0xff	; 255
   585C FF                  325 	.db #0xff	; 255
   585D 00                  326 	.db #0x00	; 0
   585E 00                  327 	.db #0x00	; 0
   585F 00                  328 	.db #0x00	; 0
   5860 FF                  329 	.db #0xff	; 255
   5861 00                  330 	.db #0x00	; 0
   5862 00                  331 	.db #0x00	; 0
   5863 00                  332 	.db #0x00	; 0
   5864 00                  333 	.db #0x00	; 0
   5865 FF                  334 	.db #0xff	; 255
   5866 FF                  335 	.db #0xff	; 255
   5867 00                  336 	.db #0x00	; 0
   5868 00                  337 	.db #0x00	; 0
   5869 00                  338 	.db #0x00	; 0
   586A FF                  339 	.db #0xff	; 255
   586B 00                  340 	.db #0x00	; 0
   586C 00                  341 	.db #0x00	; 0
   586D 00                  342 	.db #0x00	; 0
   586E 00                  343 	.db #0x00	; 0
   586F FF                  344 	.db #0xff	; 255
   5870 FF                  345 	.db #0xff	; 255
   5871 00                  346 	.db #0x00	; 0
   5872 00                  347 	.db #0x00	; 0
   5873 00                  348 	.db #0x00	; 0
   5874 FF                  349 	.db #0xff	; 255
   5875 00                  350 	.db #0x00	; 0
   5876 00                  351 	.db #0x00	; 0
   5877 00                  352 	.db #0x00	; 0
   5878 00                  353 	.db #0x00	; 0
   5879 FF                  354 	.db #0xff	; 255
   587A FF                  355 	.db #0xff	; 255
   587B 00                  356 	.db #0x00	; 0
   587C 00                  357 	.db #0x00	; 0
   587D 00                  358 	.db #0x00	; 0
   587E FF                  359 	.db #0xff	; 255
   587F 00                  360 	.db #0x00	; 0
   5880 00                  361 	.db #0x00	; 0
   5881 00                  362 	.db #0x00	; 0
   5882 00                  363 	.db #0x00	; 0
   5883 FF                  364 	.db #0xff	; 255
   5884 FF                  365 	.db #0xff	; 255
   5885 00                  366 	.db #0x00	; 0
   5886 00                  367 	.db #0x00	; 0
   5887 00                  368 	.db #0x00	; 0
   5888 FF                  369 	.db #0xff	; 255
   5889 00                  370 	.db #0x00	; 0
   588A 00                  371 	.db #0x00	; 0
   588B 00                  372 	.db #0x00	; 0
   588C 00                  373 	.db #0x00	; 0
   588D FF                  374 	.db #0xff	; 255
   588E FF                  375 	.db #0xff	; 255
   588F 00                  376 	.db #0x00	; 0
   5890 00                  377 	.db #0x00	; 0
   5891 00                  378 	.db #0x00	; 0
   5892 FF                  379 	.db #0xff	; 255
   5893 00                  380 	.db #0x00	; 0
   5894 00                  381 	.db #0x00	; 0
   5895 00                  382 	.db #0x00	; 0
   5896 00                  383 	.db #0x00	; 0
   5897 FF                  384 	.db #0xff	; 255
   5898 FF                  385 	.db #0xff	; 255
   5899 00                  386 	.db #0x00	; 0
   589A 00                  387 	.db #0x00	; 0
   589B 00                  388 	.db #0x00	; 0
   589C FF                  389 	.db #0xff	; 255
   589D 00                  390 	.db #0x00	; 0
   589E 00                  391 	.db #0x00	; 0
   589F 00                  392 	.db #0x00	; 0
   58A0 00                  393 	.db #0x00	; 0
   58A1 FF                  394 	.db #0xff	; 255
   58A2 FF                  395 	.db #0xff	; 255
   58A3 00                  396 	.db #0x00	; 0
   58A4 00                  397 	.db #0x00	; 0
   58A5 00                  398 	.db #0x00	; 0
   58A6 FF                  399 	.db #0xff	; 255
   58A7 00                  400 	.db #0x00	; 0
   58A8 00                  401 	.db #0x00	; 0
   58A9 00                  402 	.db #0x00	; 0
   58AA 00                  403 	.db #0x00	; 0
   58AB FF                  404 	.db #0xff	; 255
   58AC FF                  405 	.db #0xff	; 255
   58AD FF                  406 	.db #0xff	; 255
   58AE FF                  407 	.db #0xff	; 255
   58AF FF                  408 	.db #0xff	; 255
   58B0 FF                  409 	.db #0xff	; 255
   58B1 FF                  410 	.db #0xff	; 255
   58B2 FF                  411 	.db #0xff	; 255
   58B3 FF                  412 	.db #0xff	; 255
   58B4 FF                  413 	.db #0xff	; 255
   58B5 FF                  414 	.db #0xff	; 255
   58B6 FF                  415 	.db #0xff	; 255
   58B7 00                  416 	.db #0x00	; 0
   58B8 00                  417 	.db #0x00	; 0
   58B9 00                  418 	.db #0x00	; 0
   58BA FF                  419 	.db #0xff	; 255
   58BB 00                  420 	.db #0x00	; 0
   58BC 00                  421 	.db #0x00	; 0
   58BD 00                  422 	.db #0x00	; 0
   58BE 00                  423 	.db #0x00	; 0
   58BF FF                  424 	.db #0xff	; 255
   58C0 FF                  425 	.db #0xff	; 255
   58C1 00                  426 	.db #0x00	; 0
   58C2 00                  427 	.db #0x00	; 0
   58C3 00                  428 	.db #0x00	; 0
   58C4 FF                  429 	.db #0xff	; 255
   58C5 00                  430 	.db #0x00	; 0
   58C6 00                  431 	.db #0x00	; 0
   58C7 00                  432 	.db #0x00	; 0
   58C8 00                  433 	.db #0x00	; 0
   58C9 FF                  434 	.db #0xff	; 255
   58CA FF                  435 	.db #0xff	; 255
   58CB 00                  436 	.db #0x00	; 0
   58CC 00                  437 	.db #0x00	; 0
   58CD 00                  438 	.db #0x00	; 0
   58CE FF                  439 	.db #0xff	; 255
   58CF 00                  440 	.db #0x00	; 0
   58D0 00                  441 	.db #0x00	; 0
   58D1 00                  442 	.db #0x00	; 0
   58D2 00                  443 	.db #0x00	; 0
   58D3 FF                  444 	.db #0xff	; 255
   58D4 FF                  445 	.db #0xff	; 255
   58D5 00                  446 	.db #0x00	; 0
   58D6 00                  447 	.db #0x00	; 0
   58D7 00                  448 	.db #0x00	; 0
   58D8 FF                  449 	.db #0xff	; 255
   58D9 00                  450 	.db #0x00	; 0
   58DA 00                  451 	.db #0x00	; 0
   58DB 00                  452 	.db #0x00	; 0
   58DC 00                  453 	.db #0x00	; 0
   58DD FF                  454 	.db #0xff	; 255
   58DE FF                  455 	.db #0xff	; 255
   58DF 00                  456 	.db #0x00	; 0
   58E0 00                  457 	.db #0x00	; 0
   58E1 00                  458 	.db #0x00	; 0
   58E2 FF                  459 	.db #0xff	; 255
   58E3 00                  460 	.db #0x00	; 0
   58E4 00                  461 	.db #0x00	; 0
   58E5 00                  462 	.db #0x00	; 0
   58E6 00                  463 	.db #0x00	; 0
   58E7 FF                  464 	.db #0xff	; 255
   58E8 FF                  465 	.db #0xff	; 255
   58E9 00                  466 	.db #0x00	; 0
   58EA 00                  467 	.db #0x00	; 0
   58EB 00                  468 	.db #0x00	; 0
   58EC FF                  469 	.db #0xff	; 255
   58ED 00                  470 	.db #0x00	; 0
   58EE 00                  471 	.db #0x00	; 0
   58EF 00                  472 	.db #0x00	; 0
   58F0 00                  473 	.db #0x00	; 0
   58F1 FF                  474 	.db #0xff	; 255
   58F2 FF                  475 	.db #0xff	; 255
   58F3 00                  476 	.db #0x00	; 0
   58F4 00                  477 	.db #0x00	; 0
   58F5 00                  478 	.db #0x00	; 0
   58F6 FF                  479 	.db #0xff	; 255
   58F7 00                  480 	.db #0x00	; 0
   58F8 00                  481 	.db #0x00	; 0
   58F9 00                  482 	.db #0x00	; 0
   58FA 00                  483 	.db #0x00	; 0
   58FB FF                  484 	.db #0xff	; 255
   58FC FF                  485 	.db #0xff	; 255
   58FD FF                  486 	.db #0xff	; 255
   58FE FF                  487 	.db #0xff	; 255
   58FF FF                  488 	.db #0xff	; 255
   5900 FF                  489 	.db #0xff	; 255
   5901 FF                  490 	.db #0xff	; 255
   5902 FF                  491 	.db #0xff	; 255
   5903 FF                  492 	.db #0xff	; 255
   5904 FF                  493 	.db #0xff	; 255
   5905 FF                  494 	.db #0xff	; 255
                            495 ;src/entities/enemy.c:82: void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right) {
                            496 ;	---------------------------------
                            497 ; Function enemyspawn
                            498 ; ---------------------------------
   5906                     499 _enemyspawn::
   5906 DD E5         [15]  500 	push	ix
   5908 DD 21 00 00   [14]  501 	ld	ix,#0
   590C DD 39         [15]  502 	add	ix,sp
   590E 21 F1 FF      [10]  503 	ld	hl, #-15
   5911 39            [11]  504 	add	hl, sp
   5912 F9            [ 6]  505 	ld	sp, hl
                            506 ;src/entities/enemy.c:83: if (!enemy) {
   5913 DD 7E 05      [19]  507 	ld	a, 5 (ix)
   5916 DD B6 04      [19]  508 	or	a,4 (ix)
                            509 ;src/entities/enemy.c:84: return;
   5919 CA D9 5A      [10]  510 	jp	Z,00112$
                            511 ;src/entities/enemy.c:87: enemy->x = x;
   591C DD 7E 04      [19]  512 	ld	a, 4 (ix)
   591F DD 77 FE      [19]  513 	ld	-2 (ix), a
   5922 DD 7E 05      [19]  514 	ld	a, 5 (ix)
   5925 DD 77 FF      [19]  515 	ld	-1 (ix), a
   5928 DD 6E FE      [19]  516 	ld	l,-2 (ix)
   592B DD 66 FF      [19]  517 	ld	h,-1 (ix)
   592E DD 7E 06      [19]  518 	ld	a, 6 (ix)
   5931 77            [ 7]  519 	ld	(hl), a
                            520 ;src/entities/enemy.c:88: enemy->y = y;
   5932 DD 4E FE      [19]  521 	ld	c,-2 (ix)
   5935 DD 46 FF      [19]  522 	ld	b,-1 (ix)
   5938 03            [ 6]  523 	inc	bc
   5939 DD 7E 07      [19]  524 	ld	a, 7 (ix)
   593C 02            [ 7]  525 	ld	(bc), a
                            526 ;src/entities/enemy.c:89: enemy->vx = move_right ? 1 : -1;
   593D DD 7E FE      [19]  527 	ld	a, -2 (ix)
   5940 C6 02         [ 7]  528 	add	a, #0x02
   5942 DD 77 FC      [19]  529 	ld	-4 (ix), a
   5945 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5948 CE 00         [ 7]  531 	adc	a, #0x00
   594A DD 77 FD      [19]  532 	ld	-3 (ix), a
   594D DD 7E 09      [19]  533 	ld	a, 9 (ix)
   5950 B7            [ 4]  534 	or	a, a
   5951 28 04         [12]  535 	jr	Z,00114$
   5953 0E 01         [ 7]  536 	ld	c, #0x01
   5955 18 02         [12]  537 	jr	00115$
   5957                     538 00114$:
   5957 0E FF         [ 7]  539 	ld	c, #0xff
   5959                     540 00115$:
   5959 DD 6E FC      [19]  541 	ld	l,-4 (ix)
   595C DD 66 FD      [19]  542 	ld	h,-3 (ix)
   595F 71            [ 7]  543 	ld	(hl), c
                            544 ;src/entities/enemy.c:90: enemy->vy = 0;
   5960 DD 7E FE      [19]  545 	ld	a, -2 (ix)
   5963 C6 03         [ 7]  546 	add	a, #0x03
   5965 DD 77 FA      [19]  547 	ld	-6 (ix), a
   5968 DD 7E FF      [19]  548 	ld	a, -1 (ix)
   596B CE 00         [ 7]  549 	adc	a, #0x00
   596D DD 77 FB      [19]  550 	ld	-5 (ix), a
   5970 DD 6E FA      [19]  551 	ld	l,-6 (ix)
   5973 DD 66 FB      [19]  552 	ld	h,-5 (ix)
   5976 36 00         [10]  553 	ld	(hl), #0x00
                            554 ;src/entities/enemy.c:91: enemy->active = 1;
   5978 DD 7E FE      [19]  555 	ld	a, -2 (ix)
   597B C6 06         [ 7]  556 	add	a, #0x06
   597D DD 77 F8      [19]  557 	ld	-8 (ix), a
   5980 DD 7E FF      [19]  558 	ld	a, -1 (ix)
   5983 CE 00         [ 7]  559 	adc	a, #0x00
   5985 DD 77 F9      [19]  560 	ld	-7 (ix), a
   5988 DD 6E F8      [19]  561 	ld	l,-8 (ix)
   598B DD 66 F9      [19]  562 	ld	h,-7 (ix)
   598E 36 01         [10]  563 	ld	(hl), #0x01
                            564 ;src/entities/enemy.c:92: enemy->kind = kind;
   5990 DD 7E FE      [19]  565 	ld	a, -2 (ix)
   5993 C6 09         [ 7]  566 	add	a, #0x09
   5995 DD 77 F8      [19]  567 	ld	-8 (ix), a
   5998 DD 7E FF      [19]  568 	ld	a, -1 (ix)
   599B CE 00         [ 7]  569 	adc	a, #0x00
   599D DD 77 F9      [19]  570 	ld	-7 (ix), a
   59A0 DD 6E F8      [19]  571 	ld	l,-8 (ix)
   59A3 DD 66 F9      [19]  572 	ld	h,-7 (ix)
   59A6 DD 7E 08      [19]  573 	ld	a, 8 (ix)
   59A9 77            [ 7]  574 	ld	(hl), a
                            575 ;src/entities/enemy.c:95: enemy->w = 5;
   59AA DD 7E FE      [19]  576 	ld	a, -2 (ix)
   59AD C6 04         [ 7]  577 	add	a, #0x04
   59AF DD 77 F8      [19]  578 	ld	-8 (ix), a
   59B2 DD 7E FF      [19]  579 	ld	a, -1 (ix)
   59B5 CE 00         [ 7]  580 	adc	a, #0x00
   59B7 DD 77 F9      [19]  581 	ld	-7 (ix), a
                            582 ;src/entities/enemy.c:96: enemy->h = 14;
   59BA DD 7E FE      [19]  583 	ld	a, -2 (ix)
   59BD C6 05         [ 7]  584 	add	a, #0x05
   59BF DD 77 F6      [19]  585 	ld	-10 (ix), a
   59C2 DD 7E FF      [19]  586 	ld	a, -1 (ix)
   59C5 CE 00         [ 7]  587 	adc	a, #0x00
   59C7 DD 77 F7      [19]  588 	ld	-9 (ix), a
                            589 ;src/entities/enemy.c:97: enemy->health = 2;
   59CA DD 7E FE      [19]  590 	ld	a, -2 (ix)
   59CD C6 07         [ 7]  591 	add	a, #0x07
   59CF DD 77 F4      [19]  592 	ld	-12 (ix), a
   59D2 DD 7E FF      [19]  593 	ld	a, -1 (ix)
   59D5 CE 00         [ 7]  594 	adc	a, #0x00
   59D7 DD 77 F5      [19]  595 	ld	-11 (ix), a
                            596 ;src/entities/enemy.c:98: enemy->reward = 180;
   59DA DD 7E FE      [19]  597 	ld	a, -2 (ix)
   59DD C6 08         [ 7]  598 	add	a, #0x08
   59DF DD 77 FE      [19]  599 	ld	-2 (ix), a
   59E2 DD 7E FF      [19]  600 	ld	a, -1 (ix)
   59E5 CE 00         [ 7]  601 	adc	a, #0x00
   59E7 DD 77 FF      [19]  602 	ld	-1 (ix), a
                            603 ;src/entities/enemy.c:94: if (kind == 1) {
   59EA DD 7E 08      [19]  604 	ld	a, 8 (ix)
   59ED 3D            [ 4]  605 	dec	a
   59EE 20 49         [12]  606 	jr	NZ,00110$
                            607 ;src/entities/enemy.c:95: enemy->w = 5;
   59F0 DD 6E F8      [19]  608 	ld	l,-8 (ix)
   59F3 DD 66 F9      [19]  609 	ld	h,-7 (ix)
   59F6 36 05         [10]  610 	ld	(hl), #0x05
                            611 ;src/entities/enemy.c:96: enemy->h = 14;
   59F8 DD 6E F6      [19]  612 	ld	l,-10 (ix)
   59FB DD 66 F7      [19]  613 	ld	h,-9 (ix)
   59FE 36 0E         [10]  614 	ld	(hl), #0x0e
                            615 ;src/entities/enemy.c:97: enemy->health = 2;
   5A00 DD 6E F4      [19]  616 	ld	l,-12 (ix)
   5A03 DD 66 F5      [19]  617 	ld	h,-11 (ix)
   5A06 36 02         [10]  618 	ld	(hl), #0x02
                            619 ;src/entities/enemy.c:98: enemy->reward = 180;
   5A08 DD 6E FE      [19]  620 	ld	l,-2 (ix)
   5A0B DD 66 FF      [19]  621 	ld	h,-1 (ix)
   5A0E 36 B4         [10]  622 	ld	(hl), #0xb4
                            623 ;src/entities/enemy.c:99: enemy->vx = move_right ? 2 : -2;
   5A10 DD 7E FC      [19]  624 	ld	a, -4 (ix)
   5A13 DD 77 F2      [19]  625 	ld	-14 (ix), a
   5A16 DD 7E FD      [19]  626 	ld	a, -3 (ix)
   5A19 DD 77 F3      [19]  627 	ld	-13 (ix), a
   5A1C DD 7E 09      [19]  628 	ld	a, 9 (ix)
   5A1F B7            [ 4]  629 	or	a, a
   5A20 28 06         [12]  630 	jr	Z,00116$
   5A22 DD 36 F1 02   [19]  631 	ld	-15 (ix), #0x02
   5A26 18 04         [12]  632 	jr	00117$
   5A28                     633 00116$:
   5A28 DD 36 F1 FE   [19]  634 	ld	-15 (ix), #0xfe
   5A2C                     635 00117$:
   5A2C DD 6E F2      [19]  636 	ld	l,-14 (ix)
   5A2F DD 66 F3      [19]  637 	ld	h,-13 (ix)
   5A32 DD 7E F1      [19]  638 	ld	a, -15 (ix)
   5A35 77            [ 7]  639 	ld	(hl), a
   5A36 C3 D9 5A      [10]  640 	jp	00112$
   5A39                     641 00110$:
                            642 ;src/entities/enemy.c:100: } else if (kind == 2) {
   5A39 DD 7E 08      [19]  643 	ld	a, 8 (ix)
   5A3C D6 02         [ 7]  644 	sub	a, #0x02
   5A3E 20 3D         [12]  645 	jr	NZ,00107$
                            646 ;src/entities/enemy.c:101: enemy->w = 6;
   5A40 DD 6E F8      [19]  647 	ld	l,-8 (ix)
   5A43 DD 66 F9      [19]  648 	ld	h,-7 (ix)
   5A46 36 06         [10]  649 	ld	(hl), #0x06
                            650 ;src/entities/enemy.c:102: enemy->h = 10;
   5A48 DD 6E F6      [19]  651 	ld	l,-10 (ix)
   5A4B DD 66 F7      [19]  652 	ld	h,-9 (ix)
   5A4E 36 0A         [10]  653 	ld	(hl), #0x0a
                            654 ;src/entities/enemy.c:103: enemy->health = 1;
   5A50 DD 6E F4      [19]  655 	ld	l,-12 (ix)
   5A53 DD 66 F5      [19]  656 	ld	h,-11 (ix)
   5A56 36 01         [10]  657 	ld	(hl), #0x01
                            658 ;src/entities/enemy.c:104: enemy->reward = 150;
   5A58 DD 6E FE      [19]  659 	ld	l,-2 (ix)
   5A5B DD 66 FF      [19]  660 	ld	h,-1 (ix)
   5A5E 36 96         [10]  661 	ld	(hl), #0x96
                            662 ;src/entities/enemy.c:105: enemy->vy = move_right ? 1 : -1;
   5A60 DD 4E FA      [19]  663 	ld	c,-6 (ix)
   5A63 DD 46 FB      [19]  664 	ld	b,-5 (ix)
   5A66 DD 7E 09      [19]  665 	ld	a, 9 (ix)
   5A69 B7            [ 4]  666 	or	a, a
   5A6A 28 04         [12]  667 	jr	Z,00118$
   5A6C 3E 01         [ 7]  668 	ld	a, #0x01
   5A6E 18 02         [12]  669 	jr	00119$
   5A70                     670 00118$:
   5A70 3E FF         [ 7]  671 	ld	a, #0xff
   5A72                     672 00119$:
   5A72 02            [ 7]  673 	ld	(bc), a
                            674 ;src/entities/enemy.c:106: enemy->vx = 1;
   5A73 DD 6E FC      [19]  675 	ld	l,-4 (ix)
   5A76 DD 66 FD      [19]  676 	ld	h,-3 (ix)
   5A79 36 01         [10]  677 	ld	(hl), #0x01
   5A7B 18 5C         [12]  678 	jr	00112$
   5A7D                     679 00107$:
                            680 ;src/entities/enemy.c:107: } else if (kind == 3) {
   5A7D DD 7E 08      [19]  681 	ld	a, 8 (ix)
   5A80 D6 03         [ 7]  682 	sub	a, #0x03
   5A82 20 35         [12]  683 	jr	NZ,00104$
                            684 ;src/entities/enemy.c:108: enemy->w = 10;
   5A84 DD 6E F8      [19]  685 	ld	l,-8 (ix)
   5A87 DD 66 F9      [19]  686 	ld	h,-7 (ix)
   5A8A 36 0A         [10]  687 	ld	(hl), #0x0a
                            688 ;src/entities/enemy.c:109: enemy->h = 18;
   5A8C DD 6E F6      [19]  689 	ld	l,-10 (ix)
   5A8F DD 66 F7      [19]  690 	ld	h,-9 (ix)
   5A92 36 12         [10]  691 	ld	(hl), #0x12
                            692 ;src/entities/enemy.c:110: enemy->health = 8;
   5A94 DD 6E F4      [19]  693 	ld	l,-12 (ix)
   5A97 DD 66 F5      [19]  694 	ld	h,-11 (ix)
   5A9A 36 08         [10]  695 	ld	(hl), #0x08
                            696 ;src/entities/enemy.c:111: enemy->reward = 800;
   5A9C DD 6E FE      [19]  697 	ld	l,-2 (ix)
   5A9F DD 66 FF      [19]  698 	ld	h,-1 (ix)
   5AA2 36 20         [10]  699 	ld	(hl), #0x20
                            700 ;src/entities/enemy.c:112: enemy->vx = move_right ? 1 : -1;
   5AA4 DD 4E FC      [19]  701 	ld	c,-4 (ix)
   5AA7 DD 46 FD      [19]  702 	ld	b,-3 (ix)
   5AAA DD 7E 09      [19]  703 	ld	a, 9 (ix)
   5AAD B7            [ 4]  704 	or	a, a
   5AAE 28 04         [12]  705 	jr	Z,00120$
   5AB0 3E 01         [ 7]  706 	ld	a, #0x01
   5AB2 18 02         [12]  707 	jr	00121$
   5AB4                     708 00120$:
   5AB4 3E FF         [ 7]  709 	ld	a, #0xff
   5AB6                     710 00121$:
   5AB6 02            [ 7]  711 	ld	(bc), a
   5AB7 18 20         [12]  712 	jr	00112$
   5AB9                     713 00104$:
                            714 ;src/entities/enemy.c:114: enemy->w = 4;
   5AB9 DD 6E F8      [19]  715 	ld	l,-8 (ix)
   5ABC DD 66 F9      [19]  716 	ld	h,-7 (ix)
   5ABF 36 04         [10]  717 	ld	(hl), #0x04
                            718 ;src/entities/enemy.c:115: enemy->h = 16;
   5AC1 DD 6E F6      [19]  719 	ld	l,-10 (ix)
   5AC4 DD 66 F7      [19]  720 	ld	h,-9 (ix)
   5AC7 36 10         [10]  721 	ld	(hl), #0x10
                            722 ;src/entities/enemy.c:116: enemy->health = 1;
   5AC9 DD 6E F4      [19]  723 	ld	l,-12 (ix)
   5ACC DD 66 F5      [19]  724 	ld	h,-11 (ix)
   5ACF 36 01         [10]  725 	ld	(hl), #0x01
                            726 ;src/entities/enemy.c:117: enemy->reward = 100;
   5AD1 DD 6E FE      [19]  727 	ld	l,-2 (ix)
   5AD4 DD 66 FF      [19]  728 	ld	h,-1 (ix)
   5AD7 36 64         [10]  729 	ld	(hl), #0x64
   5AD9                     730 00112$:
   5AD9 DD F9         [10]  731 	ld	sp, ix
   5ADB DD E1         [14]  732 	pop	ix
   5ADD C9            [10]  733 	ret
                            734 ;src/entities/enemy.c:121: void enemyupdate(Enemy* enemy) {
                            735 ;	---------------------------------
                            736 ; Function enemyupdate
                            737 ; ---------------------------------
   5ADE                     738 _enemyupdate::
   5ADE DD E5         [15]  739 	push	ix
   5AE0 DD 21 00 00   [14]  740 	ld	ix,#0
   5AE4 DD 39         [15]  741 	add	ix,sp
   5AE6 21 F6 FF      [10]  742 	ld	hl, #-10
   5AE9 39            [11]  743 	add	hl, sp
   5AEA F9            [ 6]  744 	ld	sp, hl
                            745 ;src/entities/enemy.c:125: if (!enemy || !enemy->active) {
   5AEB DD 7E 05      [19]  746 	ld	a, 5 (ix)
   5AEE DD B6 04      [19]  747 	or	a,4 (ix)
   5AF1 CA E5 5C      [10]  748 	jp	Z,00121$
   5AF4 DD 7E 04      [19]  749 	ld	a, 4 (ix)
   5AF7 DD 77 FE      [19]  750 	ld	-2 (ix), a
   5AFA DD 7E 05      [19]  751 	ld	a, 5 (ix)
   5AFD DD 77 FF      [19]  752 	ld	-1 (ix), a
   5B00 DD 6E FE      [19]  753 	ld	l,-2 (ix)
   5B03 DD 66 FF      [19]  754 	ld	h,-1 (ix)
   5B06 11 06 00      [10]  755 	ld	de, #0x0006
   5B09 19            [11]  756 	add	hl, de
   5B0A 7E            [ 7]  757 	ld	a, (hl)
   5B0B B7            [ 4]  758 	or	a, a
                            759 ;src/entities/enemy.c:126: return;
   5B0C CA E5 5C      [10]  760 	jp	Z,00121$
                            761 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5B0F DD 6E FE      [19]  762 	ld	l,-2 (ix)
   5B12 DD 66 FF      [19]  763 	ld	h,-1 (ix)
   5B15 11 09 00      [10]  764 	ld	de, #0x0009
   5B18 19            [11]  765 	add	hl, de
   5B19 7E            [ 7]  766 	ld	a, (hl)
   5B1A DD 77 FD      [19]  767 	ld	-3 (ix), a
                            768 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5B1D DD 6E FE      [19]  769 	ld	l,-2 (ix)
   5B20 DD 66 FF      [19]  770 	ld	h,-1 (ix)
   5B23 4E            [ 7]  771 	ld	c, (hl)
   5B24 DD 7E FE      [19]  772 	ld	a, -2 (ix)
   5B27 C6 02         [ 7]  773 	add	a, #0x02
   5B29 DD 77 FB      [19]  774 	ld	-5 (ix), a
   5B2C DD 7E FF      [19]  775 	ld	a, -1 (ix)
   5B2F CE 00         [ 7]  776 	adc	a, #0x00
   5B31 DD 77 FC      [19]  777 	ld	-4 (ix), a
                            778 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5B34 DD 7E FE      [19]  779 	ld	a, -2 (ix)
   5B37 C6 01         [ 7]  780 	add	a, #0x01
   5B39 DD 77 F9      [19]  781 	ld	-7 (ix), a
   5B3C DD 7E FF      [19]  782 	ld	a, -1 (ix)
   5B3F CE 00         [ 7]  783 	adc	a, #0x00
   5B41 DD 77 FA      [19]  784 	ld	-6 (ix), a
   5B44 DD 5E FE      [19]  785 	ld	e,-2 (ix)
   5B47 DD 56 FF      [19]  786 	ld	d,-1 (ix)
   5B4A 13            [ 6]  787 	inc	de
   5B4B 13            [ 6]  788 	inc	de
   5B4C 13            [ 6]  789 	inc	de
                            790 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
   5B4D 06 00         [ 7]  791 	ld	b, #0x00
   5B4F DD 6E FB      [19]  792 	ld	l,-5 (ix)
   5B52 DD 66 FC      [19]  793 	ld	h,-4 (ix)
   5B55 7E            [ 7]  794 	ld	a, (hl)
   5B56 DD 77 F8      [19]  795 	ld	-8 (ix), a
   5B59 6F            [ 4]  796 	ld	l, a
   5B5A DD 7E F8      [19]  797 	ld	a, -8 (ix)
   5B5D 17            [ 4]  798 	rla
   5B5E 9F            [ 4]  799 	sbc	a, a
   5B5F 67            [ 4]  800 	ld	h, a
   5B60 09            [11]  801 	add	hl,bc
   5B61 4D            [ 4]  802 	ld	c, l
   5B62 44            [ 4]  803 	ld	b, h
                            804 ;src/entities/enemy.c:129: if (enemy->kind == 2) {
   5B63 DD 7E FD      [19]  805 	ld	a, -3 (ix)
   5B66 D6 02         [ 7]  806 	sub	a, #0x02
   5B68 C2 11 5C      [10]  807 	jp	NZ,00111$
                            808 ;src/entities/enemy.c:130: nextx = (i16)enemy->x + (i16)enemy->vx;
                            809 ;src/entities/enemy.c:131: nexty = (i16)enemy->y + (i16)enemy->vy;
   5B6B DD 6E F9      [19]  810 	ld	l,-7 (ix)
   5B6E DD 66 FA      [19]  811 	ld	h,-6 (ix)
   5B71 6E            [ 7]  812 	ld	l, (hl)
   5B72 DD 75 F6      [19]  813 	ld	-10 (ix), l
   5B75 DD 36 F7 00   [19]  814 	ld	-9 (ix), #0x00
   5B79 1A            [ 7]  815 	ld	a, (de)
   5B7A 6F            [ 4]  816 	ld	l, a
   5B7B 17            [ 4]  817 	rla
   5B7C 9F            [ 4]  818 	sbc	a, a
   5B7D 67            [ 4]  819 	ld	h, a
   5B7E DD 7E F6      [19]  820 	ld	a, -10 (ix)
   5B81 85            [ 4]  821 	add	a, l
   5B82 DD 77 F6      [19]  822 	ld	-10 (ix), a
   5B85 DD 7E F7      [19]  823 	ld	a, -9 (ix)
   5B88 8C            [ 4]  824 	adc	a, h
   5B89 DD 77 F7      [19]  825 	ld	-9 (ix), a
                            826 ;src/entities/enemy.c:133: if (nextx < 8 || nextx > 72) {
   5B8C 79            [ 4]  827 	ld	a, c
   5B8D D6 08         [ 7]  828 	sub	a, #0x08
   5B8F 78            [ 4]  829 	ld	a, b
   5B90 17            [ 4]  830 	rla
   5B91 3F            [ 4]  831 	ccf
   5B92 1F            [ 4]  832 	rra
   5B93 DE 80         [ 7]  833 	sbc	a, #0x80
   5B95 38 0E         [12]  834 	jr	C,00104$
   5B97 3E 48         [ 7]  835 	ld	a, #0x48
   5B99 B9            [ 4]  836 	cp	a, c
   5B9A 3E 00         [ 7]  837 	ld	a, #0x00
   5B9C 98            [ 4]  838 	sbc	a, b
   5B9D E2 A2 5B      [10]  839 	jp	PO, 00161$
   5BA0 EE 80         [ 7]  840 	xor	a, #0x80
   5BA2                     841 00161$:
   5BA2 F2 C0 5B      [10]  842 	jp	P, 00105$
   5BA5                     843 00104$:
                            844 ;src/entities/enemy.c:134: enemy->vx = (i8)(-enemy->vx);
   5BA5 AF            [ 4]  845 	xor	a, a
   5BA6 DD 96 F8      [19]  846 	sub	a, -8 (ix)
   5BA9 4F            [ 4]  847 	ld	c, a
   5BAA DD 6E FB      [19]  848 	ld	l,-5 (ix)
   5BAD DD 66 FC      [19]  849 	ld	h,-4 (ix)
   5BB0 71            [ 7]  850 	ld	(hl), c
                            851 ;src/entities/enemy.c:135: nextx = (i16)enemy->x + (i16)enemy->vx;
   5BB1 DD 6E FE      [19]  852 	ld	l,-2 (ix)
   5BB4 DD 66 FF      [19]  853 	ld	h,-1 (ix)
   5BB7 6E            [ 7]  854 	ld	l, (hl)
   5BB8 26 00         [ 7]  855 	ld	h, #0x00
   5BBA 79            [ 4]  856 	ld	a, c
   5BBB 17            [ 4]  857 	rla
   5BBC 9F            [ 4]  858 	sbc	a, a
   5BBD 47            [ 4]  859 	ld	b, a
   5BBE 09            [11]  860 	add	hl,bc
   5BBF 4D            [ 4]  861 	ld	c, l
   5BC0                     862 00105$:
                            863 ;src/entities/enemy.c:137: if (nexty < 56 || nexty > 120) {
   5BC0 DD 7E F6      [19]  864 	ld	a, -10 (ix)
   5BC3 D6 38         [ 7]  865 	sub	a, #0x38
   5BC5 DD 7E F7      [19]  866 	ld	a, -9 (ix)
   5BC8 17            [ 4]  867 	rla
   5BC9 3F            [ 4]  868 	ccf
   5BCA 1F            [ 4]  869 	rra
   5BCB DE 80         [ 7]  870 	sbc	a, #0x80
   5BCD 38 12         [12]  871 	jr	C,00107$
   5BCF 3E 78         [ 7]  872 	ld	a, #0x78
   5BD1 DD BE F6      [19]  873 	cp	a, -10 (ix)
   5BD4 3E 00         [ 7]  874 	ld	a, #0x00
   5BD6 DD 9E F7      [19]  875 	sbc	a, -9 (ix)
   5BD9 E2 DE 5B      [10]  876 	jp	PO, 00162$
   5BDC EE 80         [ 7]  877 	xor	a, #0x80
   5BDE                     878 00162$:
   5BDE F2 FD 5B      [10]  879 	jp	P, 00108$
   5BE1                     880 00107$:
                            881 ;src/entities/enemy.c:138: enemy->vy = (i8)(-enemy->vy);
   5BE1 1A            [ 7]  882 	ld	a, (de)
   5BE2 6F            [ 4]  883 	ld	l, a
   5BE3 AF            [ 4]  884 	xor	a, a
   5BE4 95            [ 4]  885 	sub	a, l
   5BE5 DD 77 F8      [19]  886 	ld	-8 (ix), a
   5BE8 12            [ 7]  887 	ld	(de),a
                            888 ;src/entities/enemy.c:139: nexty = (i16)enemy->y + (i16)enemy->vy;
   5BE9 DD 6E F9      [19]  889 	ld	l,-7 (ix)
   5BEC DD 66 FA      [19]  890 	ld	h,-6 (ix)
   5BEF 5E            [ 7]  891 	ld	e, (hl)
   5BF0 16 00         [ 7]  892 	ld	d, #0x00
   5BF2 DD 6E F8      [19]  893 	ld	l, -8 (ix)
   5BF5 DD 7E F8      [19]  894 	ld	a, -8 (ix)
   5BF8 17            [ 4]  895 	rla
   5BF9 9F            [ 4]  896 	sbc	a, a
   5BFA 67            [ 4]  897 	ld	h, a
   5BFB 19            [11]  898 	add	hl,de
   5BFC E3            [19]  899 	ex	(sp), hl
   5BFD                     900 00108$:
                            901 ;src/entities/enemy.c:142: enemy->x = (u8)nextx;
   5BFD DD 6E FE      [19]  902 	ld	l,-2 (ix)
   5C00 DD 66 FF      [19]  903 	ld	h,-1 (ix)
   5C03 71            [ 7]  904 	ld	(hl), c
                            905 ;src/entities/enemy.c:143: enemy->y = (u8)nexty;
   5C04 DD 4E F6      [19]  906 	ld	c, -10 (ix)
   5C07 DD 6E F9      [19]  907 	ld	l,-7 (ix)
   5C0A DD 66 FA      [19]  908 	ld	h,-6 (ix)
   5C0D 71            [ 7]  909 	ld	(hl), c
                            910 ;src/entities/enemy.c:144: return;
   5C0E C3 E5 5C      [10]  911 	jp	00121$
   5C11                     912 00111$:
                            913 ;src/entities/enemy.c:147: nextx = (i16)enemy->x + (i16)enemy->vx;
                            914 ;src/entities/enemy.c:148: if (nextx < 2) {
   5C11 79            [ 4]  915 	ld	a, c
   5C12 D6 02         [ 7]  916 	sub	a, #0x02
   5C14 78            [ 4]  917 	ld	a, b
   5C15 17            [ 4]  918 	rla
   5C16 3F            [ 4]  919 	ccf
   5C17 1F            [ 4]  920 	rra
   5C18 DE 80         [ 7]  921 	sbc	a, #0x80
   5C1A 30 0B         [12]  922 	jr	NC,00113$
                            923 ;src/entities/enemy.c:149: nextx = 2;
   5C1C 01 02 00      [10]  924 	ld	bc, #0x0002
                            925 ;src/entities/enemy.c:150: enemy->vx = 1;
   5C1F DD 6E FB      [19]  926 	ld	l,-5 (ix)
   5C22 DD 66 FC      [19]  927 	ld	h,-4 (ix)
   5C25 36 01         [10]  928 	ld	(hl), #0x01
   5C27                     929 00113$:
                            930 ;src/entities/enemy.c:153: i16 maxx = (i16)(80 - (i16)enemy->w);
   5C27 DD 6E FE      [19]  931 	ld	l,-2 (ix)
   5C2A DD 66 FF      [19]  932 	ld	h,-1 (ix)
   5C2D 23            [ 6]  933 	inc	hl
   5C2E 23            [ 6]  934 	inc	hl
   5C2F 23            [ 6]  935 	inc	hl
   5C30 23            [ 6]  936 	inc	hl
   5C31 6E            [ 7]  937 	ld	l, (hl)
   5C32 26 00         [ 7]  938 	ld	h, #0x00
   5C34 3E 50         [ 7]  939 	ld	a, #0x50
   5C36 95            [ 4]  940 	sub	a, l
   5C37 6F            [ 4]  941 	ld	l, a
   5C38 3E 00         [ 7]  942 	ld	a, #0x00
   5C3A 9C            [ 4]  943 	sbc	a, h
   5C3B 67            [ 4]  944 	ld	h, a
                            945 ;src/entities/enemy.c:154: if (nextx > maxx) {
   5C3C 7D            [ 4]  946 	ld	a, l
   5C3D 91            [ 4]  947 	sub	a, c
   5C3E 7C            [ 4]  948 	ld	a, h
   5C3F 98            [ 4]  949 	sbc	a, b
   5C40 E2 45 5C      [10]  950 	jp	PO, 00163$
   5C43 EE 80         [ 7]  951 	xor	a, #0x80
   5C45                     952 00163$:
   5C45 F2 51 5C      [10]  953 	jp	P, 00115$
                            954 ;src/entities/enemy.c:155: nextx = maxx;
   5C48 4D            [ 4]  955 	ld	c, l
                            956 ;src/entities/enemy.c:156: enemy->vx = -1;
   5C49 DD 6E FB      [19]  957 	ld	l,-5 (ix)
   5C4C DD 66 FC      [19]  958 	ld	h,-4 (ix)
   5C4F 36 FF         [10]  959 	ld	(hl), #0xff
   5C51                     960 00115$:
                            961 ;src/entities/enemy.c:159: enemy->x = (u8)nextx;
   5C51 DD 6E FE      [19]  962 	ld	l,-2 (ix)
   5C54 DD 66 FF      [19]  963 	ld	h,-1 (ix)
   5C57 71            [ 7]  964 	ld	(hl), c
                            965 ;src/entities/enemy.c:161: enemy->vy = (i8)(enemy->vy + 1);
   5C58 1A            [ 7]  966 	ld	a, (de)
   5C59 4F            [ 4]  967 	ld	c, a
   5C5A 0C            [ 4]  968 	inc	c
   5C5B 79            [ 4]  969 	ld	a, c
   5C5C 12            [ 7]  970 	ld	(de), a
                            971 ;src/entities/enemy.c:162: if (enemy->vy > 3) enemy->vy = 3;
   5C5D 3E 03         [ 7]  972 	ld	a, #0x03
   5C5F 91            [ 4]  973 	sub	a, c
   5C60 E2 65 5C      [10]  974 	jp	PO, 00164$
   5C63 EE 80         [ 7]  975 	xor	a, #0x80
   5C65                     976 00164$:
   5C65 F2 6B 5C      [10]  977 	jp	P, 00117$
   5C68 3E 03         [ 7]  978 	ld	a, #0x03
   5C6A 12            [ 7]  979 	ld	(de), a
   5C6B                     980 00117$:
                            981 ;src/entities/enemy.c:163: nexty = (i16)enemy->y + (i16)enemy->vy;
   5C6B DD 6E F9      [19]  982 	ld	l,-7 (ix)
   5C6E DD 66 FA      [19]  983 	ld	h,-6 (ix)
   5C71 4E            [ 7]  984 	ld	c, (hl)
   5C72 06 00         [ 7]  985 	ld	b, #0x00
   5C74 1A            [ 7]  986 	ld	a, (de)
   5C75 6F            [ 4]  987 	ld	l, a
   5C76 17            [ 4]  988 	rla
   5C77 9F            [ 4]  989 	sbc	a, a
   5C78 67            [ 4]  990 	ld	h, a
   5C79 09            [11]  991 	add	hl, bc
   5C7A E5            [11]  992 	push	hl
   5C7B FD E1         [14]  993 	pop	iy
                            994 ;src/entities/enemy.c:164: nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
   5C7D DD 7E FE      [19]  995 	ld	a, -2 (ix)
   5C80 C6 05         [ 7]  996 	add	a, #0x05
   5C82 DD 77 F6      [19]  997 	ld	-10 (ix), a
   5C85 DD 7E FF      [19]  998 	ld	a, -1 (ix)
   5C88 CE 00         [ 7]  999 	adc	a, #0x00
   5C8A DD 77 F7      [19] 1000 	ld	-9 (ix), a
   5C8D E1            [10] 1001 	pop	hl
   5C8E E5            [11] 1002 	push	hl
   5C8F 7E            [ 7] 1003 	ld	a, (hl)
   5C90 DD 6E FE      [19] 1004 	ld	l,-2 (ix)
   5C93 DD 66 FF      [19] 1005 	ld	h,-1 (ix)
   5C96 4E            [ 7] 1006 	ld	c, (hl)
   5C97 06 00         [ 7] 1007 	ld	b, #0x00
   5C99 D5            [11] 1008 	push	de
   5C9A F5            [11] 1009 	push	af
   5C9B 33            [ 6] 1010 	inc	sp
   5C9C FD E5         [15] 1011 	push	iy
   5C9E C5            [11] 1012 	push	bc
   5C9F CD 40 4C      [17] 1013 	call	_collision_clamp_y_at
   5CA2 F1            [10] 1014 	pop	af
   5CA3 F1            [10] 1015 	pop	af
   5CA4 33            [ 6] 1016 	inc	sp
   5CA5 4D            [ 4] 1017 	ld	c, l
   5CA6 D1            [10] 1018 	pop	de
                           1019 ;src/entities/enemy.c:165: enemy->y = (u8)nexty;
   5CA7 DD 6E F9      [19] 1020 	ld	l,-7 (ix)
   5CAA DD 66 FA      [19] 1021 	ld	h,-6 (ix)
   5CAD 71            [ 7] 1022 	ld	(hl), c
                           1023 ;src/entities/enemy.c:166: if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
   5CAE E1            [10] 1024 	pop	hl
   5CAF E5            [11] 1025 	push	hl
   5CB0 7E            [ 7] 1026 	ld	a, (hl)
   5CB1 06 00         [ 7] 1027 	ld	b, #0x00
   5CB3 DD 6E FE      [19] 1028 	ld	l,-2 (ix)
   5CB6 DD 66 FF      [19] 1029 	ld	h,-1 (ix)
   5CB9 6E            [ 7] 1030 	ld	l, (hl)
   5CBA DD 75 F6      [19] 1031 	ld	-10 (ix), l
   5CBD DD 36 F7 00   [19] 1032 	ld	-9 (ix), #0x00
   5CC1 D5            [11] 1033 	push	de
   5CC2 F5            [11] 1034 	push	af
   5CC3 33            [ 6] 1035 	inc	sp
   5CC4 C5            [11] 1036 	push	bc
   5CC5 DD 6E F6      [19] 1037 	ld	l,-10 (ix)
   5CC8 DD 66 F7      [19] 1038 	ld	h,-9 (ix)
   5CCB E5            [11] 1039 	push	hl
   5CCC CD C1 4B      [17] 1040 	call	_collision_is_on_ground_at
   5CCF F1            [10] 1041 	pop	af
   5CD0 F1            [10] 1042 	pop	af
   5CD1 33            [ 6] 1043 	inc	sp
   5CD2 D1            [10] 1044 	pop	de
   5CD3 7D            [ 4] 1045 	ld	a, l
   5CD4 B7            [ 4] 1046 	or	a, a
   5CD5 28 0E         [12] 1047 	jr	Z,00121$
   5CD7 1A            [ 7] 1048 	ld	a, (de)
   5CD8 4F            [ 4] 1049 	ld	c, a
   5CD9 AF            [ 4] 1050 	xor	a, a
   5CDA 91            [ 4] 1051 	sub	a, c
   5CDB E2 E0 5C      [10] 1052 	jp	PO, 00165$
   5CDE EE 80         [ 7] 1053 	xor	a, #0x80
   5CE0                    1054 00165$:
   5CE0 F2 E5 5C      [10] 1055 	jp	P, 00121$
                           1056 ;src/entities/enemy.c:167: enemy->vy = 0;
   5CE3 AF            [ 4] 1057 	xor	a, a
   5CE4 12            [ 7] 1058 	ld	(de), a
   5CE5                    1059 00121$:
   5CE5 DD F9         [10] 1060 	ld	sp, ix
   5CE7 DD E1         [14] 1061 	pop	ix
   5CE9 C9            [10] 1062 	ret
                           1063 ;src/entities/enemy.c:171: void enemyrender(const Enemy* enemy) {
                           1064 ;	---------------------------------
                           1065 ; Function enemyrender
                           1066 ; ---------------------------------
   5CEA                    1067 _enemyrender::
   5CEA DD E5         [15] 1068 	push	ix
   5CEC DD 21 00 00   [14] 1069 	ld	ix,#0
   5CF0 DD 39         [15] 1070 	add	ix,sp
   5CF2 F5            [11] 1071 	push	af
   5CF3 3B            [ 6] 1072 	dec	sp
                           1073 ;src/entities/enemy.c:175: if (!enemy || !enemy->active) {
   5CF4 DD 7E 05      [19] 1074 	ld	a, 5 (ix)
   5CF7 DD B6 04      [19] 1075 	or	a,4 (ix)
   5CFA CA 77 5D      [10] 1076 	jp	Z,00113$
   5CFD DD 4E 04      [19] 1077 	ld	c,4 (ix)
   5D00 DD 46 05      [19] 1078 	ld	b,5 (ix)
   5D03 C5            [11] 1079 	push	bc
   5D04 FD E1         [14] 1080 	pop	iy
   5D06 FD 7E 06      [19] 1081 	ld	a, 6 (iy)
   5D09 B7            [ 4] 1082 	or	a, a
                           1083 ;src/entities/enemy.c:176: return;
   5D0A 28 6B         [12] 1084 	jr	Z,00113$
                           1085 ;src/entities/enemy.c:179: if (enemy->kind == 3) sprite = enemy_kind3_sprite;
   5D0C C5            [11] 1086 	push	bc
   5D0D FD E1         [14] 1087 	pop	iy
   5D0F FD 7E 09      [19] 1088 	ld	a, 9 (iy)
   5D12 FE 03         [ 7] 1089 	cp	a, #0x03
   5D14 20 0A         [12] 1090 	jr	NZ,00111$
   5D16 DD 36 FE 52   [19] 1091 	ld	-2 (ix), #<(_enemy_kind3_sprite)
   5D1A DD 36 FF 58   [19] 1092 	ld	-1 (ix), #>(_enemy_kind3_sprite)
   5D1E 18 23         [12] 1093 	jr	00112$
   5D20                    1094 00111$:
                           1095 ;src/entities/enemy.c:180: else if (enemy->kind == 2) sprite = enemy_kind2_sprite;
   5D20 FE 02         [ 7] 1096 	cp	a, #0x02
   5D22 20 0A         [12] 1097 	jr	NZ,00108$
   5D24 DD 36 FE 16   [19] 1098 	ld	-2 (ix), #<(_enemy_kind2_sprite)
   5D28 DD 36 FF 58   [19] 1099 	ld	-1 (ix), #>(_enemy_kind2_sprite)
   5D2C 18 15         [12] 1100 	jr	00112$
   5D2E                    1101 00108$:
                           1102 ;src/entities/enemy.c:181: else if (enemy->kind == 1) sprite = enemy_kind1_sprite;
   5D2E 3D            [ 4] 1103 	dec	a
   5D2F 20 0A         [12] 1104 	jr	NZ,00105$
   5D31 DD 36 FE D0   [19] 1105 	ld	-2 (ix), #<(_enemy_kind1_sprite)
   5D35 DD 36 FF 57   [19] 1106 	ld	-1 (ix), #>(_enemy_kind1_sprite)
   5D39 18 08         [12] 1107 	jr	00112$
   5D3B                    1108 00105$:
                           1109 ;src/entities/enemy.c:182: else sprite = enemy_kind0_sprite;
   5D3B DD 36 FE 90   [19] 1110 	ld	-2 (ix), #<(_enemy_kind0_sprite)
   5D3F DD 36 FF 57   [19] 1111 	ld	-1 (ix), #>(_enemy_kind0_sprite)
   5D43                    1112 00112$:
                           1113 ;src/entities/enemy.c:184: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
   5D43 69            [ 4] 1114 	ld	l, c
   5D44 60            [ 4] 1115 	ld	h, b
   5D45 23            [ 6] 1116 	inc	hl
   5D46 56            [ 7] 1117 	ld	d, (hl)
   5D47 0A            [ 7] 1118 	ld	a, (bc)
   5D48 C5            [11] 1119 	push	bc
   5D49 5F            [ 4] 1120 	ld	e, a
   5D4A D5            [11] 1121 	push	de
   5D4B 21 00 C0      [10] 1122 	ld	hl, #0xc000
   5D4E E5            [11] 1123 	push	hl
   5D4F CD A5 65      [17] 1124 	call	_cpct_getScreenPtr
   5D52 EB            [ 4] 1125 	ex	de,hl
   5D53 C1            [10] 1126 	pop	bc
                           1127 ;src/entities/enemy.c:185: cpct_drawSprite((u8*)sprite, pvmem, enemy->w, enemy->h);
   5D54 C5            [11] 1128 	push	bc
   5D55 FD E1         [14] 1129 	pop	iy
   5D57 FD 7E 05      [19] 1130 	ld	a, 5 (iy)
   5D5A DD 77 FD      [19] 1131 	ld	-3 (ix), a
   5D5D 69            [ 4] 1132 	ld	l, c
   5D5E 60            [ 4] 1133 	ld	h, b
   5D5F 01 04 00      [10] 1134 	ld	bc, #0x0004
   5D62 09            [11] 1135 	add	hl, bc
   5D63 4E            [ 7] 1136 	ld	c, (hl)
   5D64 D5            [11] 1137 	push	de
   5D65 FD E1         [14] 1138 	pop	iy
   5D67 DD 5E FE      [19] 1139 	ld	e,-2 (ix)
   5D6A DD 56 FF      [19] 1140 	ld	d,-1 (ix)
   5D6D DD 46 FD      [19] 1141 	ld	b, -3 (ix)
   5D70 C5            [11] 1142 	push	bc
   5D71 FD E5         [15] 1143 	push	iy
   5D73 D5            [11] 1144 	push	de
   5D74 CD D6 63      [17] 1145 	call	_cpct_drawSprite
   5D77                    1146 00113$:
   5D77 DD F9         [10] 1147 	ld	sp, ix
   5D79 DD E1         [14] 1148 	pop	ix
   5D7B C9            [10] 1149 	ret
                           1150 ;src/entities/enemy.c:188: u8 enemydamage(Enemy* enemy, u8 damage) {
                           1151 ;	---------------------------------
                           1152 ; Function enemydamage
                           1153 ; ---------------------------------
   5D7C                    1154 _enemydamage::
   5D7C DD E5         [15] 1155 	push	ix
   5D7E DD 21 00 00   [14] 1156 	ld	ix,#0
   5D82 DD 39         [15] 1157 	add	ix,sp
                           1158 ;src/entities/enemy.c:189: if (!enemy || !enemy->active) {
   5D84 DD 7E 05      [19] 1159 	ld	a, 5 (ix)
   5D87 DD B6 04      [19] 1160 	or	a,4 (ix)
   5D8A 28 0F         [12] 1161 	jr	Z,00101$
   5D8C DD 4E 04      [19] 1162 	ld	c,4 (ix)
   5D8F DD 46 05      [19] 1163 	ld	b,5 (ix)
   5D92 21 06 00      [10] 1164 	ld	hl, #0x0006
   5D95 09            [11] 1165 	add	hl,bc
   5D96 EB            [ 4] 1166 	ex	de,hl
   5D97 1A            [ 7] 1167 	ld	a, (de)
   5D98 B7            [ 4] 1168 	or	a, a
   5D99 20 04         [12] 1169 	jr	NZ,00102$
   5D9B                    1170 00101$:
                           1171 ;src/entities/enemy.c:190: return 0;
   5D9B 2E 00         [ 7] 1172 	ld	l, #0x00
   5D9D 18 1A         [12] 1173 	jr	00106$
   5D9F                    1174 00102$:
                           1175 ;src/entities/enemy.c:193: if (damage >= enemy->health) {
   5D9F 21 07 00      [10] 1176 	ld	hl, #0x0007
   5DA2 09            [11] 1177 	add	hl, bc
   5DA3 4E            [ 7] 1178 	ld	c, (hl)
   5DA4 DD 7E 06      [19] 1179 	ld	a, 6 (ix)
   5DA7 91            [ 4] 1180 	sub	a, c
   5DA8 38 08         [12] 1181 	jr	C,00105$
                           1182 ;src/entities/enemy.c:194: enemy->health = 0;
   5DAA 36 00         [10] 1183 	ld	(hl), #0x00
                           1184 ;src/entities/enemy.c:195: enemy->active = 0;
   5DAC AF            [ 4] 1185 	xor	a, a
   5DAD 12            [ 7] 1186 	ld	(de), a
                           1187 ;src/entities/enemy.c:196: return 1;
   5DAE 2E 01         [ 7] 1188 	ld	l, #0x01
   5DB0 18 07         [12] 1189 	jr	00106$
   5DB2                    1190 00105$:
                           1191 ;src/entities/enemy.c:199: enemy->health = (u8)(enemy->health - damage);
   5DB2 79            [ 4] 1192 	ld	a, c
   5DB3 DD 96 06      [19] 1193 	sub	a, 6 (ix)
   5DB6 77            [ 7] 1194 	ld	(hl), a
                           1195 ;src/entities/enemy.c:200: return 0;
   5DB7 2E 00         [ 7] 1196 	ld	l, #0x00
   5DB9                    1197 00106$:
   5DB9 DD E1         [14] 1198 	pop	ix
   5DBB C9            [10] 1199 	ret
                           1200 	.area _CODE
                           1201 	.area _INITIALIZER
                           1202 	.area _CABS (ABS)
