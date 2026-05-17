                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module hud
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_getScreenPtr
                             12 	.globl _cpct_drawSprite
                             13 	.globl _hudinit
                             14 	.globl _hudupdate
                             15 	.globl _hudrender
                             16 ;--------------------------------------------------------
                             17 ; special function registers
                             18 ;--------------------------------------------------------
                             19 ;--------------------------------------------------------
                             20 ; ram data
                             21 ;--------------------------------------------------------
                             22 	.area _DATA
   6676                      23 _currenthealth:
   6676                      24 	.ds 1
   6677                      25 _currentscore:
   6677                      26 	.ds 2
   6679                      27 _currenttime:
   6679                      28 	.ds 1
   667A                      29 _currentlives:
   667A                      30 	.ds 1
   667B                      31 _currentweapon:
   667B                      32 	.ds 1
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
                             37 ;--------------------------------------------------------
                             38 ; absolute external ram data
                             39 ;--------------------------------------------------------
                             40 	.area _DABS (ABS)
                             41 ;--------------------------------------------------------
                             42 ; global & static initialisations
                             43 ;--------------------------------------------------------
                             44 	.area _HOME
                             45 	.area _GSINIT
                             46 	.area _GSFINAL
                             47 	.area _GSINIT
                             48 ;--------------------------------------------------------
                             49 ; Home
                             50 ;--------------------------------------------------------
                             51 	.area _HOME
                             52 	.area _HOME
                             53 ;--------------------------------------------------------
                             54 ; code
                             55 ;--------------------------------------------------------
                             56 	.area _CODE
                             57 ;src/systems/hud.c:134: static const u8* hud_get_number_sprite(u8 digit) {
                             58 ;	---------------------------------
                             59 ; Function hud_get_number_sprite
                             60 ; ---------------------------------
   4D21                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:135: switch (digit % 10) {
   4D21 3E 0A         [ 7]   63 	ld	a, #0x0a
   4D23 F5            [11]   64 	push	af
   4D24 33            [ 6]   65 	inc	sp
   4D25 21 03 00      [10]   66 	ld	hl, #3+0
   4D28 39            [11]   67 	add	hl, sp
   4D29 7E            [ 7]   68 	ld	a, (hl)
   4D2A F5            [11]   69 	push	af
   4D2B 33            [ 6]   70 	inc	sp
   4D2C CD 7B 64      [17]   71 	call	__moduchar
   4D2F F1            [10]   72 	pop	af
   4D30 4D            [ 4]   73 	ld	c, l
   4D31 3E 08         [ 7]   74 	ld	a, #0x08
   4D33 91            [ 4]   75 	sub	a, c
   4D34 38 48         [12]   76 	jr	C,00110$
   4D36 06 00         [ 7]   77 	ld	b, #0x00
   4D38 21 3F 4D      [10]   78 	ld	hl, #00118$
   4D3B 09            [11]   79 	add	hl, bc
   4D3C 09            [11]   80 	add	hl, bc
   4D3D 09            [11]   81 	add	hl, bc
   4D3E E9            [ 4]   82 	jp	(hl)
   4D3F                      83 00118$:
   4D3F C3 5A 4D      [10]   84 	jp	00101$
   4D42 C3 5E 4D      [10]   85 	jp	00102$
   4D45 C3 62 4D      [10]   86 	jp	00103$
   4D48 C3 66 4D      [10]   87 	jp	00104$
   4D4B C3 6A 4D      [10]   88 	jp	00105$
   4D4E C3 6E 4D      [10]   89 	jp	00106$
   4D51 C3 72 4D      [10]   90 	jp	00107$
   4D54 C3 76 4D      [10]   91 	jp	00108$
   4D57 C3 7A 4D      [10]   92 	jp	00109$
                             93 ;src/systems/hud.c:136: case 0: return huddigit_0;
   4D5A                      94 00101$:
   4D5A 21 02 4E      [10]   95 	ld	hl, #_huddigit_0
   4D5D C9            [10]   96 	ret
                             97 ;src/systems/hud.c:137: case 1: return huddigit_1;
   4D5E                      98 00102$:
   4D5E 21 42 4E      [10]   99 	ld	hl, #_huddigit_1
   4D61 C9            [10]  100 	ret
                            101 ;src/systems/hud.c:138: case 2: return huddigit_2;
   4D62                     102 00103$:
   4D62 21 82 4E      [10]  103 	ld	hl, #_huddigit_2
   4D65 C9            [10]  104 	ret
                            105 ;src/systems/hud.c:139: case 3: return huddigit_3;
   4D66                     106 00104$:
   4D66 21 C2 4E      [10]  107 	ld	hl, #_huddigit_3
   4D69 C9            [10]  108 	ret
                            109 ;src/systems/hud.c:140: case 4: return huddigit_4;
   4D6A                     110 00105$:
   4D6A 21 02 4F      [10]  111 	ld	hl, #_huddigit_4
   4D6D C9            [10]  112 	ret
                            113 ;src/systems/hud.c:141: case 5: return huddigit_5;
   4D6E                     114 00106$:
   4D6E 21 42 4F      [10]  115 	ld	hl, #_huddigit_5
   4D71 C9            [10]  116 	ret
                            117 ;src/systems/hud.c:142: case 6: return huddigit_6;
   4D72                     118 00107$:
   4D72 21 82 4F      [10]  119 	ld	hl, #_huddigit_6
   4D75 C9            [10]  120 	ret
                            121 ;src/systems/hud.c:143: case 7: return huddigit_7;
   4D76                     122 00108$:
   4D76 21 C2 4F      [10]  123 	ld	hl, #_huddigit_7
   4D79 C9            [10]  124 	ret
                            125 ;src/systems/hud.c:144: case 8: return huddigit_8;
   4D7A                     126 00109$:
   4D7A 21 02 50      [10]  127 	ld	hl, #_huddigit_8
   4D7D C9            [10]  128 	ret
                            129 ;src/systems/hud.c:145: default: return huddigit_9;
   4D7E                     130 00110$:
   4D7E 21 42 50      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:146: }
   4D81 C9            [10]  133 	ret
   4D82                     134 _hudhealth:
   4D82 F0                  135 	.db #0xf0	; 240
   4D83 F0                  136 	.db #0xf0	; 240
   4D84 F0                  137 	.db #0xf0	; 240
   4D85 F0                  138 	.db #0xf0	; 240
   4D86 F0                  139 	.db #0xf0	; 240
   4D87 F0                  140 	.db #0xf0	; 240
   4D88 F0                  141 	.db #0xf0	; 240
   4D89 F0                  142 	.db #0xf0	; 240
   4D8A F0                  143 	.db #0xf0	; 240
   4D8B 00                  144 	.db #0x00	; 0
   4D8C F0                  145 	.db #0xf0	; 240
   4D8D 00                  146 	.db #0x00	; 0
   4D8E 00                  147 	.db #0x00	; 0
   4D8F 00                  148 	.db #0x00	; 0
   4D90 00                  149 	.db #0x00	; 0
   4D91 F0                  150 	.db #0xf0	; 240
   4D92 F0                  151 	.db #0xf0	; 240
   4D93 00                  152 	.db #0x00	; 0
   4D94 F0                  153 	.db #0xf0	; 240
   4D95 00                  154 	.db #0x00	; 0
   4D96 00                  155 	.db #0x00	; 0
   4D97 00                  156 	.db #0x00	; 0
   4D98 00                  157 	.db #0x00	; 0
   4D99 F0                  158 	.db #0xf0	; 240
   4D9A F0                  159 	.db #0xf0	; 240
   4D9B 00                  160 	.db #0x00	; 0
   4D9C F0                  161 	.db #0xf0	; 240
   4D9D 00                  162 	.db #0x00	; 0
   4D9E 00                  163 	.db #0x00	; 0
   4D9F 00                  164 	.db #0x00	; 0
   4DA0 00                  165 	.db #0x00	; 0
   4DA1 F0                  166 	.db #0xf0	; 240
   4DA2 F0                  167 	.db #0xf0	; 240
   4DA3 F0                  168 	.db #0xf0	; 240
   4DA4 F0                  169 	.db #0xf0	; 240
   4DA5 F0                  170 	.db #0xf0	; 240
   4DA6 F0                  171 	.db #0xf0	; 240
   4DA7 F0                  172 	.db #0xf0	; 240
   4DA8 F0                  173 	.db #0xf0	; 240
   4DA9 F0                  174 	.db #0xf0	; 240
   4DAA F0                  175 	.db #0xf0	; 240
   4DAB 00                  176 	.db #0x00	; 0
   4DAC F0                  177 	.db #0xf0	; 240
   4DAD 00                  178 	.db #0x00	; 0
   4DAE 00                  179 	.db #0x00	; 0
   4DAF 00                  180 	.db #0x00	; 0
   4DB0 00                  181 	.db #0x00	; 0
   4DB1 F0                  182 	.db #0xf0	; 240
   4DB2 F0                  183 	.db #0xf0	; 240
   4DB3 00                  184 	.db #0x00	; 0
   4DB4 F0                  185 	.db #0xf0	; 240
   4DB5 00                  186 	.db #0x00	; 0
   4DB6 00                  187 	.db #0x00	; 0
   4DB7 00                  188 	.db #0x00	; 0
   4DB8 00                  189 	.db #0x00	; 0
   4DB9 F0                  190 	.db #0xf0	; 240
   4DBA F0                  191 	.db #0xf0	; 240
   4DBB F0                  192 	.db #0xf0	; 240
   4DBC F0                  193 	.db #0xf0	; 240
   4DBD F0                  194 	.db #0xf0	; 240
   4DBE F0                  195 	.db #0xf0	; 240
   4DBF F0                  196 	.db #0xf0	; 240
   4DC0 F0                  197 	.db #0xf0	; 240
   4DC1 F0                  198 	.db #0xf0	; 240
   4DC2                     199 _hudlives:
   4DC2 CC                  200 	.db #0xcc	; 204
   4DC3 CC                  201 	.db #0xcc	; 204
   4DC4 CC                  202 	.db #0xcc	; 204
   4DC5 CC                  203 	.db #0xcc	; 204
   4DC6 CC                  204 	.db #0xcc	; 204
   4DC7 CC                  205 	.db #0xcc	; 204
   4DC8 CC                  206 	.db #0xcc	; 204
   4DC9 CC                  207 	.db #0xcc	; 204
   4DCA CC                  208 	.db #0xcc	; 204
   4DCB 00                  209 	.db #0x00	; 0
   4DCC 00                  210 	.db #0x00	; 0
   4DCD CC                  211 	.db #0xcc	; 204
   4DCE 00                  212 	.db #0x00	; 0
   4DCF 00                  213 	.db #0x00	; 0
   4DD0 00                  214 	.db #0x00	; 0
   4DD1 CC                  215 	.db #0xcc	; 204
   4DD2 CC                  216 	.db #0xcc	; 204
   4DD3 00                  217 	.db #0x00	; 0
   4DD4 00                  218 	.db #0x00	; 0
   4DD5 CC                  219 	.db #0xcc	; 204
   4DD6 00                  220 	.db #0x00	; 0
   4DD7 00                  221 	.db #0x00	; 0
   4DD8 00                  222 	.db #0x00	; 0
   4DD9 CC                  223 	.db #0xcc	; 204
   4DDA CC                  224 	.db #0xcc	; 204
   4DDB 00                  225 	.db #0x00	; 0
   4DDC 00                  226 	.db #0x00	; 0
   4DDD CC                  227 	.db #0xcc	; 204
   4DDE 00                  228 	.db #0x00	; 0
   4DDF 00                  229 	.db #0x00	; 0
   4DE0 00                  230 	.db #0x00	; 0
   4DE1 CC                  231 	.db #0xcc	; 204
   4DE2 CC                  232 	.db #0xcc	; 204
   4DE3 CC                  233 	.db #0xcc	; 204
   4DE4 CC                  234 	.db #0xcc	; 204
   4DE5 CC                  235 	.db #0xcc	; 204
   4DE6 CC                  236 	.db #0xcc	; 204
   4DE7 CC                  237 	.db #0xcc	; 204
   4DE8 CC                  238 	.db #0xcc	; 204
   4DE9 CC                  239 	.db #0xcc	; 204
   4DEA CC                  240 	.db #0xcc	; 204
   4DEB 00                  241 	.db #0x00	; 0
   4DEC 00                  242 	.db #0x00	; 0
   4DED CC                  243 	.db #0xcc	; 204
   4DEE 00                  244 	.db #0x00	; 0
   4DEF 00                  245 	.db #0x00	; 0
   4DF0 00                  246 	.db #0x00	; 0
   4DF1 CC                  247 	.db #0xcc	; 204
   4DF2 CC                  248 	.db #0xcc	; 204
   4DF3 00                  249 	.db #0x00	; 0
   4DF4 00                  250 	.db #0x00	; 0
   4DF5 CC                  251 	.db #0xcc	; 204
   4DF6 00                  252 	.db #0x00	; 0
   4DF7 00                  253 	.db #0x00	; 0
   4DF8 00                  254 	.db #0x00	; 0
   4DF9 CC                  255 	.db #0xcc	; 204
   4DFA CC                  256 	.db #0xcc	; 204
   4DFB CC                  257 	.db #0xcc	; 204
   4DFC CC                  258 	.db #0xcc	; 204
   4DFD CC                  259 	.db #0xcc	; 204
   4DFE CC                  260 	.db #0xcc	; 204
   4DFF CC                  261 	.db #0xcc	; 204
   4E00 CC                  262 	.db #0xcc	; 204
   4E01 CC                  263 	.db #0xcc	; 204
   4E02                     264 _huddigit_0:
   4E02 00                  265 	.db #0x00	; 0
   4E03 F0                  266 	.db #0xf0	; 240
   4E04 F0                  267 	.db #0xf0	; 240
   4E05 F0                  268 	.db #0xf0	; 240
   4E06 F0                  269 	.db #0xf0	; 240
   4E07 F0                  270 	.db #0xf0	; 240
   4E08 F0                  271 	.db #0xf0	; 240
   4E09 00                  272 	.db #0x00	; 0
   4E0A F0                  273 	.db #0xf0	; 240
   4E0B 00                  274 	.db #0x00	; 0
   4E0C 00                  275 	.db #0x00	; 0
   4E0D 00                  276 	.db #0x00	; 0
   4E0E 00                  277 	.db #0x00	; 0
   4E0F 00                  278 	.db #0x00	; 0
   4E10 00                  279 	.db #0x00	; 0
   4E11 F0                  280 	.db #0xf0	; 240
   4E12 F0                  281 	.db #0xf0	; 240
   4E13 00                  282 	.db #0x00	; 0
   4E14 00                  283 	.db #0x00	; 0
   4E15 00                  284 	.db #0x00	; 0
   4E16 00                  285 	.db #0x00	; 0
   4E17 00                  286 	.db #0x00	; 0
   4E18 00                  287 	.db #0x00	; 0
   4E19 F0                  288 	.db #0xf0	; 240
   4E1A 00                  289 	.db #0x00	; 0
   4E1B 00                  290 	.db #0x00	; 0
   4E1C 00                  291 	.db #0x00	; 0
   4E1D 00                  292 	.db #0x00	; 0
   4E1E 00                  293 	.db #0x00	; 0
   4E1F 00                  294 	.db #0x00	; 0
   4E20 00                  295 	.db #0x00	; 0
   4E21 00                  296 	.db #0x00	; 0
   4E22 F0                  297 	.db #0xf0	; 240
   4E23 00                  298 	.db #0x00	; 0
   4E24 00                  299 	.db #0x00	; 0
   4E25 00                  300 	.db #0x00	; 0
   4E26 00                  301 	.db #0x00	; 0
   4E27 00                  302 	.db #0x00	; 0
   4E28 00                  303 	.db #0x00	; 0
   4E29 F0                  304 	.db #0xf0	; 240
   4E2A F0                  305 	.db #0xf0	; 240
   4E2B 00                  306 	.db #0x00	; 0
   4E2C 00                  307 	.db #0x00	; 0
   4E2D 00                  308 	.db #0x00	; 0
   4E2E 00                  309 	.db #0x00	; 0
   4E2F 00                  310 	.db #0x00	; 0
   4E30 00                  311 	.db #0x00	; 0
   4E31 F0                  312 	.db #0xf0	; 240
   4E32 F0                  313 	.db #0xf0	; 240
   4E33 00                  314 	.db #0x00	; 0
   4E34 00                  315 	.db #0x00	; 0
   4E35 00                  316 	.db #0x00	; 0
   4E36 00                  317 	.db #0x00	; 0
   4E37 00                  318 	.db #0x00	; 0
   4E38 00                  319 	.db #0x00	; 0
   4E39 F0                  320 	.db #0xf0	; 240
   4E3A 00                  321 	.db #0x00	; 0
   4E3B F0                  322 	.db #0xf0	; 240
   4E3C F0                  323 	.db #0xf0	; 240
   4E3D F0                  324 	.db #0xf0	; 240
   4E3E F0                  325 	.db #0xf0	; 240
   4E3F F0                  326 	.db #0xf0	; 240
   4E40 F0                  327 	.db #0xf0	; 240
   4E41 00                  328 	.db #0x00	; 0
   4E42                     329 _huddigit_1:
   4E42 00                  330 	.db #0x00	; 0
   4E43 00                  331 	.db #0x00	; 0
   4E44 00                  332 	.db #0x00	; 0
   4E45 00                  333 	.db #0x00	; 0
   4E46 00                  334 	.db #0x00	; 0
   4E47 00                  335 	.db #0x00	; 0
   4E48 00                  336 	.db #0x00	; 0
   4E49 00                  337 	.db #0x00	; 0
   4E4A 00                  338 	.db #0x00	; 0
   4E4B 00                  339 	.db #0x00	; 0
   4E4C 00                  340 	.db #0x00	; 0
   4E4D 00                  341 	.db #0x00	; 0
   4E4E 00                  342 	.db #0x00	; 0
   4E4F 00                  343 	.db #0x00	; 0
   4E50 00                  344 	.db #0x00	; 0
   4E51 F0                  345 	.db #0xf0	; 240
   4E52 00                  346 	.db #0x00	; 0
   4E53 00                  347 	.db #0x00	; 0
   4E54 00                  348 	.db #0x00	; 0
   4E55 00                  349 	.db #0x00	; 0
   4E56 00                  350 	.db #0x00	; 0
   4E57 00                  351 	.db #0x00	; 0
   4E58 00                  352 	.db #0x00	; 0
   4E59 F0                  353 	.db #0xf0	; 240
   4E5A 00                  354 	.db #0x00	; 0
   4E5B 00                  355 	.db #0x00	; 0
   4E5C 00                  356 	.db #0x00	; 0
   4E5D 00                  357 	.db #0x00	; 0
   4E5E 00                  358 	.db #0x00	; 0
   4E5F 00                  359 	.db #0x00	; 0
   4E60 00                  360 	.db #0x00	; 0
   4E61 00                  361 	.db #0x00	; 0
   4E62 00                  362 	.db #0x00	; 0
   4E63 00                  363 	.db #0x00	; 0
   4E64 00                  364 	.db #0x00	; 0
   4E65 00                  365 	.db #0x00	; 0
   4E66 00                  366 	.db #0x00	; 0
   4E67 00                  367 	.db #0x00	; 0
   4E68 00                  368 	.db #0x00	; 0
   4E69 F0                  369 	.db #0xf0	; 240
   4E6A 00                  370 	.db #0x00	; 0
   4E6B 00                  371 	.db #0x00	; 0
   4E6C 00                  372 	.db #0x00	; 0
   4E6D 00                  373 	.db #0x00	; 0
   4E6E 00                  374 	.db #0x00	; 0
   4E6F 00                  375 	.db #0x00	; 0
   4E70 00                  376 	.db #0x00	; 0
   4E71 F0                  377 	.db #0xf0	; 240
   4E72 00                  378 	.db #0x00	; 0
   4E73 00                  379 	.db #0x00	; 0
   4E74 00                  380 	.db #0x00	; 0
   4E75 00                  381 	.db #0x00	; 0
   4E76 00                  382 	.db #0x00	; 0
   4E77 00                  383 	.db #0x00	; 0
   4E78 00                  384 	.db #0x00	; 0
   4E79 F0                  385 	.db #0xf0	; 240
   4E7A 00                  386 	.db #0x00	; 0
   4E7B 00                  387 	.db #0x00	; 0
   4E7C 00                  388 	.db #0x00	; 0
   4E7D 00                  389 	.db #0x00	; 0
   4E7E 00                  390 	.db #0x00	; 0
   4E7F 00                  391 	.db #0x00	; 0
   4E80 00                  392 	.db #0x00	; 0
   4E81 00                  393 	.db #0x00	; 0
   4E82                     394 _huddigit_2:
   4E82 00                  395 	.db #0x00	; 0
   4E83 F0                  396 	.db #0xf0	; 240
   4E84 F0                  397 	.db #0xf0	; 240
   4E85 F0                  398 	.db #0xf0	; 240
   4E86 F0                  399 	.db #0xf0	; 240
   4E87 F0                  400 	.db #0xf0	; 240
   4E88 F0                  401 	.db #0xf0	; 240
   4E89 00                  402 	.db #0x00	; 0
   4E8A 00                  403 	.db #0x00	; 0
   4E8B 00                  404 	.db #0x00	; 0
   4E8C 00                  405 	.db #0x00	; 0
   4E8D 00                  406 	.db #0x00	; 0
   4E8E 00                  407 	.db #0x00	; 0
   4E8F 00                  408 	.db #0x00	; 0
   4E90 00                  409 	.db #0x00	; 0
   4E91 F0                  410 	.db #0xf0	; 240
   4E92 00                  411 	.db #0x00	; 0
   4E93 00                  412 	.db #0x00	; 0
   4E94 00                  413 	.db #0x00	; 0
   4E95 00                  414 	.db #0x00	; 0
   4E96 00                  415 	.db #0x00	; 0
   4E97 00                  416 	.db #0x00	; 0
   4E98 00                  417 	.db #0x00	; 0
   4E99 F0                  418 	.db #0xf0	; 240
   4E9A 00                  419 	.db #0x00	; 0
   4E9B F0                  420 	.db #0xf0	; 240
   4E9C F0                  421 	.db #0xf0	; 240
   4E9D F0                  422 	.db #0xf0	; 240
   4E9E F0                  423 	.db #0xf0	; 240
   4E9F F0                  424 	.db #0xf0	; 240
   4EA0 F0                  425 	.db #0xf0	; 240
   4EA1 00                  426 	.db #0x00	; 0
   4EA2 F0                  427 	.db #0xf0	; 240
   4EA3 00                  428 	.db #0x00	; 0
   4EA4 00                  429 	.db #0x00	; 0
   4EA5 00                  430 	.db #0x00	; 0
   4EA6 00                  431 	.db #0x00	; 0
   4EA7 00                  432 	.db #0x00	; 0
   4EA8 00                  433 	.db #0x00	; 0
   4EA9 00                  434 	.db #0x00	; 0
   4EAA F0                  435 	.db #0xf0	; 240
   4EAB 00                  436 	.db #0x00	; 0
   4EAC 00                  437 	.db #0x00	; 0
   4EAD 00                  438 	.db #0x00	; 0
   4EAE 00                  439 	.db #0x00	; 0
   4EAF 00                  440 	.db #0x00	; 0
   4EB0 00                  441 	.db #0x00	; 0
   4EB1 00                  442 	.db #0x00	; 0
   4EB2 F0                  443 	.db #0xf0	; 240
   4EB3 00                  444 	.db #0x00	; 0
   4EB4 00                  445 	.db #0x00	; 0
   4EB5 00                  446 	.db #0x00	; 0
   4EB6 00                  447 	.db #0x00	; 0
   4EB7 00                  448 	.db #0x00	; 0
   4EB8 00                  449 	.db #0x00	; 0
   4EB9 00                  450 	.db #0x00	; 0
   4EBA 00                  451 	.db #0x00	; 0
   4EBB F0                  452 	.db #0xf0	; 240
   4EBC F0                  453 	.db #0xf0	; 240
   4EBD F0                  454 	.db #0xf0	; 240
   4EBE F0                  455 	.db #0xf0	; 240
   4EBF F0                  456 	.db #0xf0	; 240
   4EC0 F0                  457 	.db #0xf0	; 240
   4EC1 00                  458 	.db #0x00	; 0
   4EC2                     459 _huddigit_3:
   4EC2 00                  460 	.db #0x00	; 0
   4EC3 F0                  461 	.db #0xf0	; 240
   4EC4 F0                  462 	.db #0xf0	; 240
   4EC5 F0                  463 	.db #0xf0	; 240
   4EC6 F0                  464 	.db #0xf0	; 240
   4EC7 F0                  465 	.db #0xf0	; 240
   4EC8 F0                  466 	.db #0xf0	; 240
   4EC9 00                  467 	.db #0x00	; 0
   4ECA 00                  468 	.db #0x00	; 0
   4ECB 00                  469 	.db #0x00	; 0
   4ECC 00                  470 	.db #0x00	; 0
   4ECD 00                  471 	.db #0x00	; 0
   4ECE 00                  472 	.db #0x00	; 0
   4ECF 00                  473 	.db #0x00	; 0
   4ED0 00                  474 	.db #0x00	; 0
   4ED1 F0                  475 	.db #0xf0	; 240
   4ED2 00                  476 	.db #0x00	; 0
   4ED3 00                  477 	.db #0x00	; 0
   4ED4 00                  478 	.db #0x00	; 0
   4ED5 00                  479 	.db #0x00	; 0
   4ED6 00                  480 	.db #0x00	; 0
   4ED7 00                  481 	.db #0x00	; 0
   4ED8 00                  482 	.db #0x00	; 0
   4ED9 F0                  483 	.db #0xf0	; 240
   4EDA 00                  484 	.db #0x00	; 0
   4EDB F0                  485 	.db #0xf0	; 240
   4EDC F0                  486 	.db #0xf0	; 240
   4EDD F0                  487 	.db #0xf0	; 240
   4EDE F0                  488 	.db #0xf0	; 240
   4EDF F0                  489 	.db #0xf0	; 240
   4EE0 F0                  490 	.db #0xf0	; 240
   4EE1 00                  491 	.db #0x00	; 0
   4EE2 00                  492 	.db #0x00	; 0
   4EE3 00                  493 	.db #0x00	; 0
   4EE4 00                  494 	.db #0x00	; 0
   4EE5 00                  495 	.db #0x00	; 0
   4EE6 00                  496 	.db #0x00	; 0
   4EE7 00                  497 	.db #0x00	; 0
   4EE8 00                  498 	.db #0x00	; 0
   4EE9 F0                  499 	.db #0xf0	; 240
   4EEA 00                  500 	.db #0x00	; 0
   4EEB 00                  501 	.db #0x00	; 0
   4EEC 00                  502 	.db #0x00	; 0
   4EED 00                  503 	.db #0x00	; 0
   4EEE 00                  504 	.db #0x00	; 0
   4EEF 00                  505 	.db #0x00	; 0
   4EF0 00                  506 	.db #0x00	; 0
   4EF1 F0                  507 	.db #0xf0	; 240
   4EF2 00                  508 	.db #0x00	; 0
   4EF3 00                  509 	.db #0x00	; 0
   4EF4 00                  510 	.db #0x00	; 0
   4EF5 00                  511 	.db #0x00	; 0
   4EF6 00                  512 	.db #0x00	; 0
   4EF7 00                  513 	.db #0x00	; 0
   4EF8 00                  514 	.db #0x00	; 0
   4EF9 F0                  515 	.db #0xf0	; 240
   4EFA 00                  516 	.db #0x00	; 0
   4EFB F0                  517 	.db #0xf0	; 240
   4EFC F0                  518 	.db #0xf0	; 240
   4EFD F0                  519 	.db #0xf0	; 240
   4EFE F0                  520 	.db #0xf0	; 240
   4EFF F0                  521 	.db #0xf0	; 240
   4F00 F0                  522 	.db #0xf0	; 240
   4F01 00                  523 	.db #0x00	; 0
   4F02                     524 _huddigit_4:
   4F02 00                  525 	.db #0x00	; 0
   4F03 00                  526 	.db #0x00	; 0
   4F04 00                  527 	.db #0x00	; 0
   4F05 00                  528 	.db #0x00	; 0
   4F06 00                  529 	.db #0x00	; 0
   4F07 00                  530 	.db #0x00	; 0
   4F08 00                  531 	.db #0x00	; 0
   4F09 00                  532 	.db #0x00	; 0
   4F0A F0                  533 	.db #0xf0	; 240
   4F0B 00                  534 	.db #0x00	; 0
   4F0C 00                  535 	.db #0x00	; 0
   4F0D 00                  536 	.db #0x00	; 0
   4F0E 00                  537 	.db #0x00	; 0
   4F0F 00                  538 	.db #0x00	; 0
   4F10 00                  539 	.db #0x00	; 0
   4F11 F0                  540 	.db #0xf0	; 240
   4F12 F0                  541 	.db #0xf0	; 240
   4F13 00                  542 	.db #0x00	; 0
   4F14 00                  543 	.db #0x00	; 0
   4F15 00                  544 	.db #0x00	; 0
   4F16 00                  545 	.db #0x00	; 0
   4F17 00                  546 	.db #0x00	; 0
   4F18 00                  547 	.db #0x00	; 0
   4F19 F0                  548 	.db #0xf0	; 240
   4F1A 00                  549 	.db #0x00	; 0
   4F1B F0                  550 	.db #0xf0	; 240
   4F1C F0                  551 	.db #0xf0	; 240
   4F1D F0                  552 	.db #0xf0	; 240
   4F1E F0                  553 	.db #0xf0	; 240
   4F1F F0                  554 	.db #0xf0	; 240
   4F20 F0                  555 	.db #0xf0	; 240
   4F21 00                  556 	.db #0x00	; 0
   4F22 00                  557 	.db #0x00	; 0
   4F23 00                  558 	.db #0x00	; 0
   4F24 00                  559 	.db #0x00	; 0
   4F25 00                  560 	.db #0x00	; 0
   4F26 00                  561 	.db #0x00	; 0
   4F27 00                  562 	.db #0x00	; 0
   4F28 00                  563 	.db #0x00	; 0
   4F29 F0                  564 	.db #0xf0	; 240
   4F2A 00                  565 	.db #0x00	; 0
   4F2B 00                  566 	.db #0x00	; 0
   4F2C 00                  567 	.db #0x00	; 0
   4F2D 00                  568 	.db #0x00	; 0
   4F2E 00                  569 	.db #0x00	; 0
   4F2F 00                  570 	.db #0x00	; 0
   4F30 00                  571 	.db #0x00	; 0
   4F31 F0                  572 	.db #0xf0	; 240
   4F32 00                  573 	.db #0x00	; 0
   4F33 00                  574 	.db #0x00	; 0
   4F34 00                  575 	.db #0x00	; 0
   4F35 00                  576 	.db #0x00	; 0
   4F36 00                  577 	.db #0x00	; 0
   4F37 00                  578 	.db #0x00	; 0
   4F38 00                  579 	.db #0x00	; 0
   4F39 F0                  580 	.db #0xf0	; 240
   4F3A 00                  581 	.db #0x00	; 0
   4F3B 00                  582 	.db #0x00	; 0
   4F3C 00                  583 	.db #0x00	; 0
   4F3D 00                  584 	.db #0x00	; 0
   4F3E 00                  585 	.db #0x00	; 0
   4F3F 00                  586 	.db #0x00	; 0
   4F40 00                  587 	.db #0x00	; 0
   4F41 00                  588 	.db #0x00	; 0
   4F42                     589 _huddigit_5:
   4F42 00                  590 	.db #0x00	; 0
   4F43 F0                  591 	.db #0xf0	; 240
   4F44 F0                  592 	.db #0xf0	; 240
   4F45 F0                  593 	.db #0xf0	; 240
   4F46 F0                  594 	.db #0xf0	; 240
   4F47 F0                  595 	.db #0xf0	; 240
   4F48 F0                  596 	.db #0xf0	; 240
   4F49 00                  597 	.db #0x00	; 0
   4F4A F0                  598 	.db #0xf0	; 240
   4F4B 00                  599 	.db #0x00	; 0
   4F4C 00                  600 	.db #0x00	; 0
   4F4D 00                  601 	.db #0x00	; 0
   4F4E 00                  602 	.db #0x00	; 0
   4F4F 00                  603 	.db #0x00	; 0
   4F50 00                  604 	.db #0x00	; 0
   4F51 00                  605 	.db #0x00	; 0
   4F52 F0                  606 	.db #0xf0	; 240
   4F53 00                  607 	.db #0x00	; 0
   4F54 00                  608 	.db #0x00	; 0
   4F55 00                  609 	.db #0x00	; 0
   4F56 00                  610 	.db #0x00	; 0
   4F57 00                  611 	.db #0x00	; 0
   4F58 00                  612 	.db #0x00	; 0
   4F59 00                  613 	.db #0x00	; 0
   4F5A 00                  614 	.db #0x00	; 0
   4F5B F0                  615 	.db #0xf0	; 240
   4F5C F0                  616 	.db #0xf0	; 240
   4F5D F0                  617 	.db #0xf0	; 240
   4F5E F0                  618 	.db #0xf0	; 240
   4F5F F0                  619 	.db #0xf0	; 240
   4F60 F0                  620 	.db #0xf0	; 240
   4F61 00                  621 	.db #0x00	; 0
   4F62 00                  622 	.db #0x00	; 0
   4F63 00                  623 	.db #0x00	; 0
   4F64 00                  624 	.db #0x00	; 0
   4F65 00                  625 	.db #0x00	; 0
   4F66 00                  626 	.db #0x00	; 0
   4F67 00                  627 	.db #0x00	; 0
   4F68 00                  628 	.db #0x00	; 0
   4F69 F0                  629 	.db #0xf0	; 240
   4F6A 00                  630 	.db #0x00	; 0
   4F6B 00                  631 	.db #0x00	; 0
   4F6C 00                  632 	.db #0x00	; 0
   4F6D 00                  633 	.db #0x00	; 0
   4F6E 00                  634 	.db #0x00	; 0
   4F6F 00                  635 	.db #0x00	; 0
   4F70 00                  636 	.db #0x00	; 0
   4F71 F0                  637 	.db #0xf0	; 240
   4F72 00                  638 	.db #0x00	; 0
   4F73 00                  639 	.db #0x00	; 0
   4F74 00                  640 	.db #0x00	; 0
   4F75 00                  641 	.db #0x00	; 0
   4F76 00                  642 	.db #0x00	; 0
   4F77 00                  643 	.db #0x00	; 0
   4F78 00                  644 	.db #0x00	; 0
   4F79 F0                  645 	.db #0xf0	; 240
   4F7A 00                  646 	.db #0x00	; 0
   4F7B F0                  647 	.db #0xf0	; 240
   4F7C F0                  648 	.db #0xf0	; 240
   4F7D F0                  649 	.db #0xf0	; 240
   4F7E F0                  650 	.db #0xf0	; 240
   4F7F F0                  651 	.db #0xf0	; 240
   4F80 F0                  652 	.db #0xf0	; 240
   4F81 00                  653 	.db #0x00	; 0
   4F82                     654 _huddigit_6:
   4F82 00                  655 	.db #0x00	; 0
   4F83 F0                  656 	.db #0xf0	; 240
   4F84 F0                  657 	.db #0xf0	; 240
   4F85 F0                  658 	.db #0xf0	; 240
   4F86 F0                  659 	.db #0xf0	; 240
   4F87 F0                  660 	.db #0xf0	; 240
   4F88 F0                  661 	.db #0xf0	; 240
   4F89 00                  662 	.db #0x00	; 0
   4F8A F0                  663 	.db #0xf0	; 240
   4F8B 00                  664 	.db #0x00	; 0
   4F8C 00                  665 	.db #0x00	; 0
   4F8D 00                  666 	.db #0x00	; 0
   4F8E 00                  667 	.db #0x00	; 0
   4F8F 00                  668 	.db #0x00	; 0
   4F90 00                  669 	.db #0x00	; 0
   4F91 00                  670 	.db #0x00	; 0
   4F92 F0                  671 	.db #0xf0	; 240
   4F93 00                  672 	.db #0x00	; 0
   4F94 00                  673 	.db #0x00	; 0
   4F95 00                  674 	.db #0x00	; 0
   4F96 00                  675 	.db #0x00	; 0
   4F97 00                  676 	.db #0x00	; 0
   4F98 00                  677 	.db #0x00	; 0
   4F99 00                  678 	.db #0x00	; 0
   4F9A 00                  679 	.db #0x00	; 0
   4F9B F0                  680 	.db #0xf0	; 240
   4F9C F0                  681 	.db #0xf0	; 240
   4F9D F0                  682 	.db #0xf0	; 240
   4F9E F0                  683 	.db #0xf0	; 240
   4F9F F0                  684 	.db #0xf0	; 240
   4FA0 F0                  685 	.db #0xf0	; 240
   4FA1 00                  686 	.db #0x00	; 0
   4FA2 F0                  687 	.db #0xf0	; 240
   4FA3 00                  688 	.db #0x00	; 0
   4FA4 00                  689 	.db #0x00	; 0
   4FA5 00                  690 	.db #0x00	; 0
   4FA6 00                  691 	.db #0x00	; 0
   4FA7 00                  692 	.db #0x00	; 0
   4FA8 00                  693 	.db #0x00	; 0
   4FA9 F0                  694 	.db #0xf0	; 240
   4FAA F0                  695 	.db #0xf0	; 240
   4FAB 00                  696 	.db #0x00	; 0
   4FAC 00                  697 	.db #0x00	; 0
   4FAD 00                  698 	.db #0x00	; 0
   4FAE 00                  699 	.db #0x00	; 0
   4FAF 00                  700 	.db #0x00	; 0
   4FB0 00                  701 	.db #0x00	; 0
   4FB1 F0                  702 	.db #0xf0	; 240
   4FB2 F0                  703 	.db #0xf0	; 240
   4FB3 00                  704 	.db #0x00	; 0
   4FB4 00                  705 	.db #0x00	; 0
   4FB5 00                  706 	.db #0x00	; 0
   4FB6 00                  707 	.db #0x00	; 0
   4FB7 00                  708 	.db #0x00	; 0
   4FB8 00                  709 	.db #0x00	; 0
   4FB9 F0                  710 	.db #0xf0	; 240
   4FBA 00                  711 	.db #0x00	; 0
   4FBB F0                  712 	.db #0xf0	; 240
   4FBC F0                  713 	.db #0xf0	; 240
   4FBD F0                  714 	.db #0xf0	; 240
   4FBE F0                  715 	.db #0xf0	; 240
   4FBF F0                  716 	.db #0xf0	; 240
   4FC0 F0                  717 	.db #0xf0	; 240
   4FC1 00                  718 	.db #0x00	; 0
   4FC2                     719 _huddigit_7:
   4FC2 00                  720 	.db #0x00	; 0
   4FC3 F0                  721 	.db #0xf0	; 240
   4FC4 F0                  722 	.db #0xf0	; 240
   4FC5 F0                  723 	.db #0xf0	; 240
   4FC6 F0                  724 	.db #0xf0	; 240
   4FC7 F0                  725 	.db #0xf0	; 240
   4FC8 F0                  726 	.db #0xf0	; 240
   4FC9 00                  727 	.db #0x00	; 0
   4FCA 00                  728 	.db #0x00	; 0
   4FCB 00                  729 	.db #0x00	; 0
   4FCC 00                  730 	.db #0x00	; 0
   4FCD 00                  731 	.db #0x00	; 0
   4FCE 00                  732 	.db #0x00	; 0
   4FCF 00                  733 	.db #0x00	; 0
   4FD0 00                  734 	.db #0x00	; 0
   4FD1 F0                  735 	.db #0xf0	; 240
   4FD2 00                  736 	.db #0x00	; 0
   4FD3 00                  737 	.db #0x00	; 0
   4FD4 00                  738 	.db #0x00	; 0
   4FD5 00                  739 	.db #0x00	; 0
   4FD6 00                  740 	.db #0x00	; 0
   4FD7 00                  741 	.db #0x00	; 0
   4FD8 00                  742 	.db #0x00	; 0
   4FD9 F0                  743 	.db #0xf0	; 240
   4FDA 00                  744 	.db #0x00	; 0
   4FDB 00                  745 	.db #0x00	; 0
   4FDC 00                  746 	.db #0x00	; 0
   4FDD 00                  747 	.db #0x00	; 0
   4FDE 00                  748 	.db #0x00	; 0
   4FDF 00                  749 	.db #0x00	; 0
   4FE0 00                  750 	.db #0x00	; 0
   4FE1 00                  751 	.db #0x00	; 0
   4FE2 00                  752 	.db #0x00	; 0
   4FE3 00                  753 	.db #0x00	; 0
   4FE4 00                  754 	.db #0x00	; 0
   4FE5 00                  755 	.db #0x00	; 0
   4FE6 00                  756 	.db #0x00	; 0
   4FE7 00                  757 	.db #0x00	; 0
   4FE8 00                  758 	.db #0x00	; 0
   4FE9 F0                  759 	.db #0xf0	; 240
   4FEA 00                  760 	.db #0x00	; 0
   4FEB 00                  761 	.db #0x00	; 0
   4FEC 00                  762 	.db #0x00	; 0
   4FED 00                  763 	.db #0x00	; 0
   4FEE 00                  764 	.db #0x00	; 0
   4FEF 00                  765 	.db #0x00	; 0
   4FF0 00                  766 	.db #0x00	; 0
   4FF1 F0                  767 	.db #0xf0	; 240
   4FF2 00                  768 	.db #0x00	; 0
   4FF3 00                  769 	.db #0x00	; 0
   4FF4 00                  770 	.db #0x00	; 0
   4FF5 00                  771 	.db #0x00	; 0
   4FF6 00                  772 	.db #0x00	; 0
   4FF7 00                  773 	.db #0x00	; 0
   4FF8 00                  774 	.db #0x00	; 0
   4FF9 F0                  775 	.db #0xf0	; 240
   4FFA 00                  776 	.db #0x00	; 0
   4FFB 00                  777 	.db #0x00	; 0
   4FFC 00                  778 	.db #0x00	; 0
   4FFD 00                  779 	.db #0x00	; 0
   4FFE 00                  780 	.db #0x00	; 0
   4FFF 00                  781 	.db #0x00	; 0
   5000 00                  782 	.db #0x00	; 0
   5001 00                  783 	.db #0x00	; 0
   5002                     784 _huddigit_8:
   5002 00                  785 	.db #0x00	; 0
   5003 F0                  786 	.db #0xf0	; 240
   5004 F0                  787 	.db #0xf0	; 240
   5005 F0                  788 	.db #0xf0	; 240
   5006 F0                  789 	.db #0xf0	; 240
   5007 F0                  790 	.db #0xf0	; 240
   5008 F0                  791 	.db #0xf0	; 240
   5009 00                  792 	.db #0x00	; 0
   500A F0                  793 	.db #0xf0	; 240
   500B 00                  794 	.db #0x00	; 0
   500C 00                  795 	.db #0x00	; 0
   500D 00                  796 	.db #0x00	; 0
   500E 00                  797 	.db #0x00	; 0
   500F 00                  798 	.db #0x00	; 0
   5010 00                  799 	.db #0x00	; 0
   5011 F0                  800 	.db #0xf0	; 240
   5012 F0                  801 	.db #0xf0	; 240
   5013 00                  802 	.db #0x00	; 0
   5014 00                  803 	.db #0x00	; 0
   5015 00                  804 	.db #0x00	; 0
   5016 00                  805 	.db #0x00	; 0
   5017 00                  806 	.db #0x00	; 0
   5018 00                  807 	.db #0x00	; 0
   5019 F0                  808 	.db #0xf0	; 240
   501A 00                  809 	.db #0x00	; 0
   501B F0                  810 	.db #0xf0	; 240
   501C F0                  811 	.db #0xf0	; 240
   501D F0                  812 	.db #0xf0	; 240
   501E F0                  813 	.db #0xf0	; 240
   501F F0                  814 	.db #0xf0	; 240
   5020 F0                  815 	.db #0xf0	; 240
   5021 00                  816 	.db #0x00	; 0
   5022 F0                  817 	.db #0xf0	; 240
   5023 00                  818 	.db #0x00	; 0
   5024 00                  819 	.db #0x00	; 0
   5025 00                  820 	.db #0x00	; 0
   5026 00                  821 	.db #0x00	; 0
   5027 00                  822 	.db #0x00	; 0
   5028 00                  823 	.db #0x00	; 0
   5029 F0                  824 	.db #0xf0	; 240
   502A F0                  825 	.db #0xf0	; 240
   502B 00                  826 	.db #0x00	; 0
   502C 00                  827 	.db #0x00	; 0
   502D 00                  828 	.db #0x00	; 0
   502E 00                  829 	.db #0x00	; 0
   502F 00                  830 	.db #0x00	; 0
   5030 00                  831 	.db #0x00	; 0
   5031 F0                  832 	.db #0xf0	; 240
   5032 F0                  833 	.db #0xf0	; 240
   5033 00                  834 	.db #0x00	; 0
   5034 00                  835 	.db #0x00	; 0
   5035 00                  836 	.db #0x00	; 0
   5036 00                  837 	.db #0x00	; 0
   5037 00                  838 	.db #0x00	; 0
   5038 00                  839 	.db #0x00	; 0
   5039 F0                  840 	.db #0xf0	; 240
   503A 00                  841 	.db #0x00	; 0
   503B F0                  842 	.db #0xf0	; 240
   503C F0                  843 	.db #0xf0	; 240
   503D F0                  844 	.db #0xf0	; 240
   503E F0                  845 	.db #0xf0	; 240
   503F F0                  846 	.db #0xf0	; 240
   5040 F0                  847 	.db #0xf0	; 240
   5041 00                  848 	.db #0x00	; 0
   5042                     849 _huddigit_9:
   5042 00                  850 	.db #0x00	; 0
   5043 F0                  851 	.db #0xf0	; 240
   5044 F0                  852 	.db #0xf0	; 240
   5045 F0                  853 	.db #0xf0	; 240
   5046 F0                  854 	.db #0xf0	; 240
   5047 F0                  855 	.db #0xf0	; 240
   5048 F0                  856 	.db #0xf0	; 240
   5049 00                  857 	.db #0x00	; 0
   504A F0                  858 	.db #0xf0	; 240
   504B 00                  859 	.db #0x00	; 0
   504C 00                  860 	.db #0x00	; 0
   504D 00                  861 	.db #0x00	; 0
   504E 00                  862 	.db #0x00	; 0
   504F 00                  863 	.db #0x00	; 0
   5050 00                  864 	.db #0x00	; 0
   5051 F0                  865 	.db #0xf0	; 240
   5052 F0                  866 	.db #0xf0	; 240
   5053 00                  867 	.db #0x00	; 0
   5054 00                  868 	.db #0x00	; 0
   5055 00                  869 	.db #0x00	; 0
   5056 00                  870 	.db #0x00	; 0
   5057 00                  871 	.db #0x00	; 0
   5058 00                  872 	.db #0x00	; 0
   5059 F0                  873 	.db #0xf0	; 240
   505A 00                  874 	.db #0x00	; 0
   505B F0                  875 	.db #0xf0	; 240
   505C F0                  876 	.db #0xf0	; 240
   505D F0                  877 	.db #0xf0	; 240
   505E F0                  878 	.db #0xf0	; 240
   505F F0                  879 	.db #0xf0	; 240
   5060 F0                  880 	.db #0xf0	; 240
   5061 00                  881 	.db #0x00	; 0
   5062 00                  882 	.db #0x00	; 0
   5063 00                  883 	.db #0x00	; 0
   5064 00                  884 	.db #0x00	; 0
   5065 00                  885 	.db #0x00	; 0
   5066 00                  886 	.db #0x00	; 0
   5067 00                  887 	.db #0x00	; 0
   5068 00                  888 	.db #0x00	; 0
   5069 F0                  889 	.db #0xf0	; 240
   506A 00                  890 	.db #0x00	; 0
   506B 00                  891 	.db #0x00	; 0
   506C 00                  892 	.db #0x00	; 0
   506D 00                  893 	.db #0x00	; 0
   506E 00                  894 	.db #0x00	; 0
   506F 00                  895 	.db #0x00	; 0
   5070 00                  896 	.db #0x00	; 0
   5071 F0                  897 	.db #0xf0	; 240
   5072 00                  898 	.db #0x00	; 0
   5073 00                  899 	.db #0x00	; 0
   5074 00                  900 	.db #0x00	; 0
   5075 00                  901 	.db #0x00	; 0
   5076 00                  902 	.db #0x00	; 0
   5077 00                  903 	.db #0x00	; 0
   5078 00                  904 	.db #0x00	; 0
   5079 F0                  905 	.db #0xf0	; 240
   507A 00                  906 	.db #0x00	; 0
   507B F0                  907 	.db #0xf0	; 240
   507C F0                  908 	.db #0xf0	; 240
   507D F0                  909 	.db #0xf0	; 240
   507E F0                  910 	.db #0xf0	; 240
   507F F0                  911 	.db #0xf0	; 240
   5080 F0                  912 	.db #0xf0	; 240
   5081 00                  913 	.db #0x00	; 0
                            914 ;src/systems/hud.c:149: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            915 ;	---------------------------------
                            916 ; Function hud_draw_digits
                            917 ; ---------------------------------
   5082                     918 _hud_draw_digits:
   5082 DD E5         [15]  919 	push	ix
   5084 DD 21 00 00   [14]  920 	ld	ix,#0
   5088 DD 39         [15]  921 	add	ix,sp
   508A 3B            [ 6]  922 	dec	sp
                            923 ;src/systems/hud.c:155: divisor = 1;
   508B 01 01 00      [10]  924 	ld	bc, #0x0001
                            925 ;src/systems/hud.c:156: for (i = 1; i < digits; ++i) {
   508E 1E 01         [ 7]  926 	ld	e, #0x01
   5090                     927 00106$:
   5090 7B            [ 4]  928 	ld	a, e
   5091 DD 96 06      [19]  929 	sub	a, 6 (ix)
   5094 30 0B         [12]  930 	jr	NC,00101$
                            931 ;src/systems/hud.c:157: divisor *= 10;
   5096 69            [ 4]  932 	ld	l, c
   5097 60            [ 4]  933 	ld	h, b
   5098 29            [11]  934 	add	hl, hl
   5099 29            [11]  935 	add	hl, hl
   509A 09            [11]  936 	add	hl, bc
   509B 29            [11]  937 	add	hl, hl
   509C 4D            [ 4]  938 	ld	c, l
   509D 44            [ 4]  939 	ld	b, h
                            940 ;src/systems/hud.c:156: for (i = 1; i < digits; ++i) {
   509E 1C            [ 4]  941 	inc	e
   509F 18 EF         [12]  942 	jr	00106$
   50A1                     943 00101$:
                            944 ;src/systems/hud.c:160: for (i = 0; i < digits; ++i) {
   50A1 DD 36 FF 00   [19]  945 	ld	-1 (ix), #0x00
   50A5                     946 00109$:
   50A5 DD 7E FF      [19]  947 	ld	a, -1 (ix)
   50A8 DD 96 06      [19]  948 	sub	a, 6 (ix)
   50AB D2 2A 51      [10]  949 	jp	NC, 00111$
                            950 ;src/systems/hud.c:161: digit = (u8)(value / divisor);
   50AE C5            [11]  951 	push	bc
   50AF C5            [11]  952 	push	bc
   50B0 DD 6E 04      [19]  953 	ld	l,4 (ix)
   50B3 DD 66 05      [19]  954 	ld	h,5 (ix)
   50B6 E5            [11]  955 	push	hl
   50B7 CD FC 62      [17]  956 	call	__divuint
   50BA F1            [10]  957 	pop	af
   50BB F1            [10]  958 	pop	af
   50BC 5D            [ 4]  959 	ld	e, l
   50BD C1            [10]  960 	pop	bc
                            961 ;src/systems/hud.c:162: value = (u16)(value % divisor);
   50BE C5            [11]  962 	push	bc
   50BF D5            [11]  963 	push	de
   50C0 C5            [11]  964 	push	bc
   50C1 DD 6E 04      [19]  965 	ld	l,4 (ix)
   50C4 DD 66 05      [19]  966 	ld	h,5 (ix)
   50C7 E5            [11]  967 	push	hl
   50C8 CD 87 64      [17]  968 	call	__moduint
   50CB F1            [10]  969 	pop	af
   50CC F1            [10]  970 	pop	af
   50CD D1            [10]  971 	pop	de
   50CE C1            [10]  972 	pop	bc
   50CF DD 75 04      [19]  973 	ld	4 (ix), l
   50D2 DD 74 05      [19]  974 	ld	5 (ix), h
                            975 ;src/systems/hud.c:164: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
   50D5 DD 7E FF      [19]  976 	ld	a, -1 (ix)
   50D8 07            [ 4]  977 	rlca
   50D9 07            [ 4]  978 	rlca
   50DA 07            [ 4]  979 	rlca
   50DB E6 F8         [ 7]  980 	and	a, #0xf8
   50DD 57            [ 4]  981 	ld	d, a
   50DE DD 7E 07      [19]  982 	ld	a, 7 (ix)
   50E1 82            [ 4]  983 	add	a, d
   50E2 57            [ 4]  984 	ld	d, a
   50E3 C5            [11]  985 	push	bc
   50E4 D5            [11]  986 	push	de
   50E5 DD 7E 08      [19]  987 	ld	a, 8 (ix)
   50E8 F5            [11]  988 	push	af
   50E9 33            [ 6]  989 	inc	sp
   50EA D5            [11]  990 	push	de
   50EB 33            [ 6]  991 	inc	sp
   50EC 21 00 C0      [10]  992 	ld	hl, #0xc000
   50EF E5            [11]  993 	push	hl
   50F0 CD A5 65      [17]  994 	call	_cpct_getScreenPtr
   50F3 D1            [10]  995 	pop	de
   50F4 C1            [10]  996 	pop	bc
                            997 ;src/systems/hud.c:165: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);
   50F5 E5            [11]  998 	push	hl
   50F6 C5            [11]  999 	push	bc
   50F7 7B            [ 4] 1000 	ld	a, e
   50F8 F5            [11] 1001 	push	af
   50F9 33            [ 6] 1002 	inc	sp
   50FA CD 21 4D      [17] 1003 	call	_hud_get_number_sprite
   50FD 33            [ 6] 1004 	inc	sp
   50FE EB            [ 4] 1005 	ex	de,hl
   50FF C1            [10] 1006 	pop	bc
   5100 E1            [10] 1007 	pop	hl
   5101 D5            [11] 1008 	push	de
   5102 FD E1         [14] 1009 	pop	iy
   5104 C5            [11] 1010 	push	bc
   5105 11 08 08      [10] 1011 	ld	de, #0x0808
   5108 D5            [11] 1012 	push	de
   5109 E5            [11] 1013 	push	hl
   510A FD E5         [15] 1014 	push	iy
   510C CD D6 63      [17] 1015 	call	_cpct_drawSprite
   510F C1            [10] 1016 	pop	bc
                           1017 ;src/systems/hud.c:167: if (divisor > 1) {
   5110 3E 01         [ 7] 1018 	ld	a, #0x01
   5112 B9            [ 4] 1019 	cp	a, c
   5113 3E 00         [ 7] 1020 	ld	a, #0x00
   5115 98            [ 4] 1021 	sbc	a, b
   5116 30 0C         [12] 1022 	jr	NC,00110$
                           1023 ;src/systems/hud.c:168: divisor /= 10;
   5118 21 0A 00      [10] 1024 	ld	hl, #0x000a
   511B E5            [11] 1025 	push	hl
   511C C5            [11] 1026 	push	bc
   511D CD FC 62      [17] 1027 	call	__divuint
   5120 F1            [10] 1028 	pop	af
   5121 F1            [10] 1029 	pop	af
   5122 4D            [ 4] 1030 	ld	c, l
   5123 44            [ 4] 1031 	ld	b, h
   5124                    1032 00110$:
                           1033 ;src/systems/hud.c:160: for (i = 0; i < digits; ++i) {
   5124 DD 34 FF      [23] 1034 	inc	-1 (ix)
   5127 C3 A5 50      [10] 1035 	jp	00109$
   512A                    1036 00111$:
   512A 33            [ 6] 1037 	inc	sp
   512B DD E1         [14] 1038 	pop	ix
   512D C9            [10] 1039 	ret
                           1040 ;src/systems/hud.c:173: void hudinit(void) {
                           1041 ;	---------------------------------
                           1042 ; Function hudinit
                           1043 ; ---------------------------------
   512E                    1044 _hudinit::
                           1045 ;src/systems/hud.c:174: currenthealth = 3;
   512E 21 76 66      [10] 1046 	ld	hl,#_currenthealth + 0
   5131 36 03         [10] 1047 	ld	(hl), #0x03
                           1048 ;src/systems/hud.c:175: currentscore  = 0;
   5133 21 00 00      [10] 1049 	ld	hl, #0x0000
   5136 22 77 66      [16] 1050 	ld	(_currentscore), hl
                           1051 ;src/systems/hud.c:176: currenttime   = 90;
   5139 21 79 66      [10] 1052 	ld	hl,#_currenttime + 0
   513C 36 5A         [10] 1053 	ld	(hl), #0x5a
                           1054 ;src/systems/hud.c:177: currentlives  = 3;
   513E 21 7A 66      [10] 1055 	ld	hl,#_currentlives + 0
   5141 36 03         [10] 1056 	ld	(hl), #0x03
                           1057 ;src/systems/hud.c:178: currentweapon = 0;
   5143 21 7B 66      [10] 1058 	ld	hl,#_currentweapon + 0
   5146 36 00         [10] 1059 	ld	(hl), #0x00
   5148 C9            [10] 1060 	ret
                           1061 ;src/systems/hud.c:181: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                           1062 ;	---------------------------------
                           1063 ; Function hudupdate
                           1064 ; ---------------------------------
   5149                    1065 _hudupdate::
                           1066 ;src/systems/hud.c:182: currenthealth = lives;
   5149 21 02 00      [10] 1067 	ld	hl, #2+0
   514C 39            [11] 1068 	add	hl, sp
   514D 7E            [ 7] 1069 	ld	a, (hl)
   514E 32 76 66      [13] 1070 	ld	(#_currenthealth + 0),a
                           1071 ;src/systems/hud.c:183: currentscore  = score;
   5151 21 03 00      [10] 1072 	ld	hl, #3+0
   5154 39            [11] 1073 	add	hl, sp
   5155 7E            [ 7] 1074 	ld	a, (hl)
   5156 32 77 66      [13] 1075 	ld	(#_currentscore + 0),a
   5159 21 04 00      [10] 1076 	ld	hl, #3+1
   515C 39            [11] 1077 	add	hl, sp
   515D 7E            [ 7] 1078 	ld	a, (hl)
   515E 32 78 66      [13] 1079 	ld	(#_currentscore + 1),a
                           1080 ;src/systems/hud.c:184: currenttime   = time;
   5161 21 05 00      [10] 1081 	ld	hl, #5+0
   5164 39            [11] 1082 	add	hl, sp
   5165 7E            [ 7] 1083 	ld	a, (hl)
   5166 32 79 66      [13] 1084 	ld	(#_currenttime + 0),a
                           1085 ;src/systems/hud.c:185: currentlives  = lives;
   5169 21 02 00      [10] 1086 	ld	hl, #2+0
   516C 39            [11] 1087 	add	hl, sp
   516D 7E            [ 7] 1088 	ld	a, (hl)
   516E 32 7A 66      [13] 1089 	ld	(#_currentlives + 0),a
                           1090 ;src/systems/hud.c:186: currentweapon = weapon;
   5171 21 06 00      [10] 1091 	ld	hl, #6+0
   5174 39            [11] 1092 	add	hl, sp
   5175 7E            [ 7] 1093 	ld	a, (hl)
   5176 32 7B 66      [13] 1094 	ld	(#_currentweapon + 0),a
   5179 C9            [10] 1095 	ret
                           1096 ;src/systems/hud.c:189: void hudrender(void) {
                           1097 ;	---------------------------------
                           1098 ; Function hudrender
                           1099 ; ---------------------------------
   517A                    1100 _hudrender::
                           1101 ;src/systems/hud.c:195: for (i = 0; i < currenthealth; ++i) {
   517A 0E 00         [ 7] 1102 	ld	c, #0x00
   517C                    1103 00103$:
   517C 21 76 66      [10] 1104 	ld	hl, #_currenthealth
                           1105 ;src/systems/hud.c:196: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   517F 79            [ 4] 1106 	ld	a,c
   5180 BE            [ 7] 1107 	cp	a,(hl)
   5181 30 24         [12] 1108 	jr	NC,00101$
   5183 07            [ 4] 1109 	rlca
   5184 07            [ 4] 1110 	rlca
   5185 07            [ 4] 1111 	rlca
   5186 E6 F8         [ 7] 1112 	and	a, #0xf8
   5188 47            [ 4] 1113 	ld	b, a
   5189 C5            [11] 1114 	push	bc
   518A 3E 02         [ 7] 1115 	ld	a, #0x02
   518C F5            [11] 1116 	push	af
   518D 33            [ 6] 1117 	inc	sp
   518E C5            [11] 1118 	push	bc
   518F 33            [ 6] 1119 	inc	sp
   5190 21 00 C0      [10] 1120 	ld	hl, #0xc000
   5193 E5            [11] 1121 	push	hl
   5194 CD A5 65      [17] 1122 	call	_cpct_getScreenPtr
   5197 11 08 08      [10] 1123 	ld	de, #0x0808
   519A D5            [11] 1124 	push	de
   519B E5            [11] 1125 	push	hl
   519C 21 82 4D      [10] 1126 	ld	hl, #_hudhealth
   519F E5            [11] 1127 	push	hl
   51A0 CD D6 63      [17] 1128 	call	_cpct_drawSprite
   51A3 C1            [10] 1129 	pop	bc
                           1130 ;src/systems/hud.c:195: for (i = 0; i < currenthealth; ++i) {
   51A4 0C            [ 4] 1131 	inc	c
   51A5 18 D5         [12] 1132 	jr	00103$
   51A7                    1133 00101$:
                           1134 ;src/systems/hud.c:200: scoretemp = currentscore;
   51A7 2A 77 66      [16] 1135 	ld	hl, (_currentscore)
                           1136 ;src/systems/hud.c:201: hud_draw_digits(scoretemp, 4, 24, 2);
   51AA 01 18 02      [10] 1137 	ld	bc, #0x0218
   51AD C5            [11] 1138 	push	bc
   51AE 3E 04         [ 7] 1139 	ld	a, #0x04
   51B0 F5            [11] 1140 	push	af
   51B1 33            [ 6] 1141 	inc	sp
   51B2 E5            [11] 1142 	push	hl
   51B3 CD 82 50      [17] 1143 	call	_hud_draw_digits
   51B6 F1            [10] 1144 	pop	af
   51B7 F1            [10] 1145 	pop	af
   51B8 33            [ 6] 1146 	inc	sp
                           1147 ;src/systems/hud.c:203: timetemp = currenttime;
   51B9 21 79 66      [10] 1148 	ld	hl,#_currenttime + 0
   51BC 4E            [ 7] 1149 	ld	c, (hl)
                           1150 ;src/systems/hud.c:204: hud_draw_digits((u16)timetemp, 3, 56, 2);
   51BD 06 00         [ 7] 1151 	ld	b, #0x00
   51BF 21 38 02      [10] 1152 	ld	hl, #0x0238
   51C2 E5            [11] 1153 	push	hl
   51C3 3E 03         [ 7] 1154 	ld	a, #0x03
   51C5 F5            [11] 1155 	push	af
   51C6 33            [ 6] 1156 	inc	sp
   51C7 C5            [11] 1157 	push	bc
   51C8 CD 82 50      [17] 1158 	call	_hud_draw_digits
   51CB F1            [10] 1159 	pop	af
                           1160 ;src/systems/hud.c:206: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   51CC 33            [ 6] 1161 	inc	sp
   51CD 21 02 B4      [10] 1162 	ld	hl,#0xb402
   51D0 E3            [19] 1163 	ex	(sp),hl
   51D1 21 00 C0      [10] 1164 	ld	hl, #0xc000
   51D4 E5            [11] 1165 	push	hl
   51D5 CD A5 65      [17] 1166 	call	_cpct_getScreenPtr
                           1167 ;src/systems/hud.c:207: cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);
   51D8 01 C2 4D      [10] 1168 	ld	bc, #_hudlives+0
   51DB 11 08 08      [10] 1169 	ld	de, #0x0808
   51DE D5            [11] 1170 	push	de
   51DF E5            [11] 1171 	push	hl
   51E0 C5            [11] 1172 	push	bc
   51E1 CD D6 63      [17] 1173 	call	_cpct_drawSprite
                           1174 ;src/systems/hud.c:209: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   51E4 21 0C B4      [10] 1175 	ld	hl, #0xb40c
   51E7 E5            [11] 1176 	push	hl
   51E8 21 00 C0      [10] 1177 	ld	hl, #0xc000
   51EB E5            [11] 1178 	push	hl
   51EC CD A5 65      [17] 1179 	call	_cpct_getScreenPtr
                           1180 ;src/systems/hud.c:210: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);
   51EF E5            [11] 1181 	push	hl
   51F0 3E 0A         [ 7] 1182 	ld	a, #0x0a
   51F2 F5            [11] 1183 	push	af
   51F3 33            [ 6] 1184 	inc	sp
   51F4 3A 7A 66      [13] 1185 	ld	a, (_currentlives)
   51F7 F5            [11] 1186 	push	af
   51F8 33            [ 6] 1187 	inc	sp
   51F9 CD 7B 64      [17] 1188 	call	__moduchar
   51FC F1            [10] 1189 	pop	af
   51FD 55            [ 4] 1190 	ld	d, l
   51FE D5            [11] 1191 	push	de
   51FF 33            [ 6] 1192 	inc	sp
   5200 CD 21 4D      [17] 1193 	call	_hud_get_number_sprite
   5203 33            [ 6] 1194 	inc	sp
   5204 C1            [10] 1195 	pop	bc
   5205 11 08 08      [10] 1196 	ld	de, #0x0808
   5208 D5            [11] 1197 	push	de
   5209 C5            [11] 1198 	push	bc
   520A E5            [11] 1199 	push	hl
   520B CD D6 63      [17] 1200 	call	_cpct_drawSprite
                           1201 ;src/systems/hud.c:212: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   520E 21 46 B4      [10] 1202 	ld	hl, #0xb446
   5211 E5            [11] 1203 	push	hl
   5212 21 00 C0      [10] 1204 	ld	hl, #0xc000
   5215 E5            [11] 1205 	push	hl
   5216 CD A5 65      [17] 1206 	call	_cpct_getScreenPtr
                           1207 ;src/systems/hud.c:213: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
   5219 E5            [11] 1208 	push	hl
   521A 3E 0A         [ 7] 1209 	ld	a, #0x0a
   521C F5            [11] 1210 	push	af
   521D 33            [ 6] 1211 	inc	sp
   521E 3A 7B 66      [13] 1212 	ld	a, (_currentweapon)
   5221 F5            [11] 1213 	push	af
   5222 33            [ 6] 1214 	inc	sp
   5223 CD 7B 64      [17] 1215 	call	__moduchar
   5226 F1            [10] 1216 	pop	af
   5227 55            [ 4] 1217 	ld	d, l
   5228 D5            [11] 1218 	push	de
   5229 33            [ 6] 1219 	inc	sp
   522A CD 21 4D      [17] 1220 	call	_hud_get_number_sprite
   522D 33            [ 6] 1221 	inc	sp
   522E C1            [10] 1222 	pop	bc
   522F 11 08 08      [10] 1223 	ld	de, #0x0808
   5232 D5            [11] 1224 	push	de
   5233 C5            [11] 1225 	push	bc
   5234 E5            [11] 1226 	push	hl
   5235 CD D6 63      [17] 1227 	call	_cpct_drawSprite
   5238 C9            [10] 1228 	ret
                           1229 	.area _CODE
                           1230 	.area _INITIALIZER
                           1231 	.area _CABS (ABS)
