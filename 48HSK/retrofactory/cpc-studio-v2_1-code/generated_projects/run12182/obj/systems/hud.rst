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
   67FE                      23 _currenthealth:
   67FE                      24 	.ds 1
   67FF                      25 _currentscore:
   67FF                      26 	.ds 2
   6801                      27 _currenttime:
   6801                      28 	.ds 1
   6802                      29 _currentlives:
   6802                      30 	.ds 1
   6803                      31 _currentweapon:
   6803                      32 	.ds 1
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
                             57 ;src/systems/hud.c:86: static const u8* hud_get_number_sprite(u8 digit) {
                             58 ;	---------------------------------
                             59 ; Function hud_get_number_sprite
                             60 ; ---------------------------------
   4D21                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:87: switch (digit % 10) {
   4D21 3E 0A         [ 7]   63 	ld	a, #0x0a
   4D23 F5            [11]   64 	push	af
   4D24 33            [ 6]   65 	inc	sp
   4D25 21 03 00      [10]   66 	ld	hl, #3+0
   4D28 39            [11]   67 	add	hl, sp
   4D29 7E            [ 7]   68 	ld	a, (hl)
   4D2A F5            [11]   69 	push	af
   4D2B 33            [ 6]   70 	inc	sp
   4D2C CD 03 66      [17]   71 	call	__moduchar
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
                             93 ;src/systems/hud.c:88: case 0: return huddigit_0;
   4D5A                      94 00101$:
   4D5A 21 C2 4D      [10]   95 	ld	hl, #_huddigit_0
   4D5D C9            [10]   96 	ret
                             97 ;src/systems/hud.c:89: case 1: return huddigit_1;
   4D5E                      98 00102$:
   4D5E 21 E2 4D      [10]   99 	ld	hl, #_huddigit_1
   4D61 C9            [10]  100 	ret
                            101 ;src/systems/hud.c:90: case 2: return huddigit_2;
   4D62                     102 00103$:
   4D62 21 02 4E      [10]  103 	ld	hl, #_huddigit_2
   4D65 C9            [10]  104 	ret
                            105 ;src/systems/hud.c:91: case 3: return huddigit_3;
   4D66                     106 00104$:
   4D66 21 22 4E      [10]  107 	ld	hl, #_huddigit_3
   4D69 C9            [10]  108 	ret
                            109 ;src/systems/hud.c:92: case 4: return huddigit_4;
   4D6A                     110 00105$:
   4D6A 21 42 4E      [10]  111 	ld	hl, #_huddigit_4
   4D6D C9            [10]  112 	ret
                            113 ;src/systems/hud.c:93: case 5: return huddigit_5;
   4D6E                     114 00106$:
   4D6E 21 62 4E      [10]  115 	ld	hl, #_huddigit_5
   4D71 C9            [10]  116 	ret
                            117 ;src/systems/hud.c:94: case 6: return huddigit_6;
   4D72                     118 00107$:
   4D72 21 82 4E      [10]  119 	ld	hl, #_huddigit_6
   4D75 C9            [10]  120 	ret
                            121 ;src/systems/hud.c:95: case 7: return huddigit_7;
   4D76                     122 00108$:
   4D76 21 A2 4E      [10]  123 	ld	hl, #_huddigit_7
   4D79 C9            [10]  124 	ret
                            125 ;src/systems/hud.c:96: case 8: return huddigit_8;
   4D7A                     126 00109$:
   4D7A 21 C2 4E      [10]  127 	ld	hl, #_huddigit_8
   4D7D C9            [10]  128 	ret
                            129 ;src/systems/hud.c:97: default: return huddigit_9;
   4D7E                     130 00110$:
   4D7E 21 E2 4E      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:98: }
   4D81 C9            [10]  133 	ret
   4D82                     134 _hudhealth:
   4D82 3C                  135 	.db #0x3c	; 60
   4D83 3C                  136 	.db #0x3c	; 60
   4D84 3C                  137 	.db #0x3c	; 60
   4D85 3C                  138 	.db #0x3c	; 60
   4D86 28                  139 	.db #0x28	; 40
   4D87 28                  140 	.db #0x28	; 40
   4D88 00                  141 	.db #0x00	; 0
   4D89 14                  142 	.db #0x14	; 20
   4D8A 28                  143 	.db #0x28	; 40
   4D8B 28                  144 	.db #0x28	; 40
   4D8C 00                  145 	.db #0x00	; 0
   4D8D 14                  146 	.db #0x14	; 20
   4D8E 28                  147 	.db #0x28	; 40
   4D8F 28                  148 	.db #0x28	; 40
   4D90 00                  149 	.db #0x00	; 0
   4D91 14                  150 	.db #0x14	; 20
   4D92 3C                  151 	.db #0x3c	; 60
   4D93 3C                  152 	.db #0x3c	; 60
   4D94 3C                  153 	.db #0x3c	; 60
   4D95 3C                  154 	.db #0x3c	; 60
   4D96 28                  155 	.db #0x28	; 40
   4D97 28                  156 	.db #0x28	; 40
   4D98 00                  157 	.db #0x00	; 0
   4D99 14                  158 	.db #0x14	; 20
   4D9A 28                  159 	.db #0x28	; 40
   4D9B 28                  160 	.db #0x28	; 40
   4D9C 00                  161 	.db #0x00	; 0
   4D9D 14                  162 	.db #0x14	; 20
   4D9E 3C                  163 	.db #0x3c	; 60
   4D9F 3C                  164 	.db #0x3c	; 60
   4DA0 3C                  165 	.db #0x3c	; 60
   4DA1 3C                  166 	.db #0x3c	; 60
   4DA2                     167 _hudlives:
   4DA2 30                  168 	.db #0x30	; 48	'0'
   4DA3 30                  169 	.db #0x30	; 48	'0'
   4DA4 30                  170 	.db #0x30	; 48	'0'
   4DA5 30                  171 	.db #0x30	; 48	'0'
   4DA6 20                  172 	.db #0x20	; 32
   4DA7 10                  173 	.db #0x10	; 16
   4DA8 00                  174 	.db #0x00	; 0
   4DA9 10                  175 	.db #0x10	; 16
   4DAA 20                  176 	.db #0x20	; 32
   4DAB 10                  177 	.db #0x10	; 16
   4DAC 00                  178 	.db #0x00	; 0
   4DAD 10                  179 	.db #0x10	; 16
   4DAE 20                  180 	.db #0x20	; 32
   4DAF 10                  181 	.db #0x10	; 16
   4DB0 00                  182 	.db #0x00	; 0
   4DB1 10                  183 	.db #0x10	; 16
   4DB2 30                  184 	.db #0x30	; 48	'0'
   4DB3 30                  185 	.db #0x30	; 48	'0'
   4DB4 30                  186 	.db #0x30	; 48	'0'
   4DB5 30                  187 	.db #0x30	; 48	'0'
   4DB6 20                  188 	.db #0x20	; 32
   4DB7 10                  189 	.db #0x10	; 16
   4DB8 00                  190 	.db #0x00	; 0
   4DB9 10                  191 	.db #0x10	; 16
   4DBA 20                  192 	.db #0x20	; 32
   4DBB 10                  193 	.db #0x10	; 16
   4DBC 00                  194 	.db #0x00	; 0
   4DBD 10                  195 	.db #0x10	; 16
   4DBE 30                  196 	.db #0x30	; 48	'0'
   4DBF 30                  197 	.db #0x30	; 48	'0'
   4DC0 30                  198 	.db #0x30	; 48	'0'
   4DC1 30                  199 	.db #0x30	; 48	'0'
   4DC2                     200 _huddigit_0:
   4DC2 14                  201 	.db #0x14	; 20
   4DC3 3C                  202 	.db #0x3c	; 60
   4DC4 3C                  203 	.db #0x3c	; 60
   4DC5 28                  204 	.db #0x28	; 40
   4DC6 28                  205 	.db #0x28	; 40
   4DC7 00                  206 	.db #0x00	; 0
   4DC8 00                  207 	.db #0x00	; 0
   4DC9 14                  208 	.db #0x14	; 20
   4DCA 28                  209 	.db #0x28	; 40
   4DCB 00                  210 	.db #0x00	; 0
   4DCC 00                  211 	.db #0x00	; 0
   4DCD 14                  212 	.db #0x14	; 20
   4DCE 00                  213 	.db #0x00	; 0
   4DCF 00                  214 	.db #0x00	; 0
   4DD0 00                  215 	.db #0x00	; 0
   4DD1 00                  216 	.db #0x00	; 0
   4DD2 28                  217 	.db #0x28	; 40
   4DD3 00                  218 	.db #0x00	; 0
   4DD4 00                  219 	.db #0x00	; 0
   4DD5 14                  220 	.db #0x14	; 20
   4DD6 28                  221 	.db #0x28	; 40
   4DD7 00                  222 	.db #0x00	; 0
   4DD8 00                  223 	.db #0x00	; 0
   4DD9 14                  224 	.db #0x14	; 20
   4DDA 28                  225 	.db #0x28	; 40
   4DDB 00                  226 	.db #0x00	; 0
   4DDC 00                  227 	.db #0x00	; 0
   4DDD 14                  228 	.db #0x14	; 20
   4DDE 14                  229 	.db #0x14	; 20
   4DDF 3C                  230 	.db #0x3c	; 60
   4DE0 3C                  231 	.db #0x3c	; 60
   4DE1 28                  232 	.db #0x28	; 40
   4DE2                     233 _huddigit_1:
   4DE2 00                  234 	.db #0x00	; 0
   4DE3 00                  235 	.db #0x00	; 0
   4DE4 00                  236 	.db #0x00	; 0
   4DE5 00                  237 	.db #0x00	; 0
   4DE6 00                  238 	.db #0x00	; 0
   4DE7 00                  239 	.db #0x00	; 0
   4DE8 00                  240 	.db #0x00	; 0
   4DE9 14                  241 	.db #0x14	; 20
   4DEA 00                  242 	.db #0x00	; 0
   4DEB 00                  243 	.db #0x00	; 0
   4DEC 00                  244 	.db #0x00	; 0
   4DED 14                  245 	.db #0x14	; 20
   4DEE 00                  246 	.db #0x00	; 0
   4DEF 00                  247 	.db #0x00	; 0
   4DF0 00                  248 	.db #0x00	; 0
   4DF1 00                  249 	.db #0x00	; 0
   4DF2 00                  250 	.db #0x00	; 0
   4DF3 00                  251 	.db #0x00	; 0
   4DF4 00                  252 	.db #0x00	; 0
   4DF5 14                  253 	.db #0x14	; 20
   4DF6 00                  254 	.db #0x00	; 0
   4DF7 00                  255 	.db #0x00	; 0
   4DF8 00                  256 	.db #0x00	; 0
   4DF9 14                  257 	.db #0x14	; 20
   4DFA 00                  258 	.db #0x00	; 0
   4DFB 00                  259 	.db #0x00	; 0
   4DFC 00                  260 	.db #0x00	; 0
   4DFD 14                  261 	.db #0x14	; 20
   4DFE 00                  262 	.db #0x00	; 0
   4DFF 00                  263 	.db #0x00	; 0
   4E00 00                  264 	.db #0x00	; 0
   4E01 00                  265 	.db #0x00	; 0
   4E02                     266 _huddigit_2:
   4E02 14                  267 	.db #0x14	; 20
   4E03 3C                  268 	.db #0x3c	; 60
   4E04 3C                  269 	.db #0x3c	; 60
   4E05 28                  270 	.db #0x28	; 40
   4E06 00                  271 	.db #0x00	; 0
   4E07 00                  272 	.db #0x00	; 0
   4E08 00                  273 	.db #0x00	; 0
   4E09 14                  274 	.db #0x14	; 20
   4E0A 00                  275 	.db #0x00	; 0
   4E0B 00                  276 	.db #0x00	; 0
   4E0C 00                  277 	.db #0x00	; 0
   4E0D 14                  278 	.db #0x14	; 20
   4E0E 14                  279 	.db #0x14	; 20
   4E0F 3C                  280 	.db #0x3c	; 60
   4E10 3C                  281 	.db #0x3c	; 60
   4E11 28                  282 	.db #0x28	; 40
   4E12 28                  283 	.db #0x28	; 40
   4E13 00                  284 	.db #0x00	; 0
   4E14 00                  285 	.db #0x00	; 0
   4E15 00                  286 	.db #0x00	; 0
   4E16 28                  287 	.db #0x28	; 40
   4E17 00                  288 	.db #0x00	; 0
   4E18 00                  289 	.db #0x00	; 0
   4E19 00                  290 	.db #0x00	; 0
   4E1A 28                  291 	.db #0x28	; 40
   4E1B 00                  292 	.db #0x00	; 0
   4E1C 00                  293 	.db #0x00	; 0
   4E1D 00                  294 	.db #0x00	; 0
   4E1E 14                  295 	.db #0x14	; 20
   4E1F 3C                  296 	.db #0x3c	; 60
   4E20 3C                  297 	.db #0x3c	; 60
   4E21 28                  298 	.db #0x28	; 40
   4E22                     299 _huddigit_3:
   4E22 14                  300 	.db #0x14	; 20
   4E23 3C                  301 	.db #0x3c	; 60
   4E24 3C                  302 	.db #0x3c	; 60
   4E25 28                  303 	.db #0x28	; 40
   4E26 00                  304 	.db #0x00	; 0
   4E27 00                  305 	.db #0x00	; 0
   4E28 00                  306 	.db #0x00	; 0
   4E29 14                  307 	.db #0x14	; 20
   4E2A 00                  308 	.db #0x00	; 0
   4E2B 00                  309 	.db #0x00	; 0
   4E2C 00                  310 	.db #0x00	; 0
   4E2D 14                  311 	.db #0x14	; 20
   4E2E 14                  312 	.db #0x14	; 20
   4E2F 3C                  313 	.db #0x3c	; 60
   4E30 3C                  314 	.db #0x3c	; 60
   4E31 28                  315 	.db #0x28	; 40
   4E32 00                  316 	.db #0x00	; 0
   4E33 00                  317 	.db #0x00	; 0
   4E34 00                  318 	.db #0x00	; 0
   4E35 14                  319 	.db #0x14	; 20
   4E36 00                  320 	.db #0x00	; 0
   4E37 00                  321 	.db #0x00	; 0
   4E38 00                  322 	.db #0x00	; 0
   4E39 14                  323 	.db #0x14	; 20
   4E3A 00                  324 	.db #0x00	; 0
   4E3B 00                  325 	.db #0x00	; 0
   4E3C 00                  326 	.db #0x00	; 0
   4E3D 14                  327 	.db #0x14	; 20
   4E3E 14                  328 	.db #0x14	; 20
   4E3F 3C                  329 	.db #0x3c	; 60
   4E40 3C                  330 	.db #0x3c	; 60
   4E41 28                  331 	.db #0x28	; 40
   4E42                     332 _huddigit_4:
   4E42 00                  333 	.db #0x00	; 0
   4E43 00                  334 	.db #0x00	; 0
   4E44 00                  335 	.db #0x00	; 0
   4E45 00                  336 	.db #0x00	; 0
   4E46 28                  337 	.db #0x28	; 40
   4E47 00                  338 	.db #0x00	; 0
   4E48 00                  339 	.db #0x00	; 0
   4E49 14                  340 	.db #0x14	; 20
   4E4A 28                  341 	.db #0x28	; 40
   4E4B 00                  342 	.db #0x00	; 0
   4E4C 00                  343 	.db #0x00	; 0
   4E4D 14                  344 	.db #0x14	; 20
   4E4E 14                  345 	.db #0x14	; 20
   4E4F 3C                  346 	.db #0x3c	; 60
   4E50 3C                  347 	.db #0x3c	; 60
   4E51 28                  348 	.db #0x28	; 40
   4E52 00                  349 	.db #0x00	; 0
   4E53 00                  350 	.db #0x00	; 0
   4E54 00                  351 	.db #0x00	; 0
   4E55 14                  352 	.db #0x14	; 20
   4E56 00                  353 	.db #0x00	; 0
   4E57 00                  354 	.db #0x00	; 0
   4E58 00                  355 	.db #0x00	; 0
   4E59 14                  356 	.db #0x14	; 20
   4E5A 00                  357 	.db #0x00	; 0
   4E5B 00                  358 	.db #0x00	; 0
   4E5C 00                  359 	.db #0x00	; 0
   4E5D 14                  360 	.db #0x14	; 20
   4E5E 00                  361 	.db #0x00	; 0
   4E5F 00                  362 	.db #0x00	; 0
   4E60 00                  363 	.db #0x00	; 0
   4E61 00                  364 	.db #0x00	; 0
   4E62                     365 _huddigit_5:
   4E62 14                  366 	.db #0x14	; 20
   4E63 3C                  367 	.db #0x3c	; 60
   4E64 3C                  368 	.db #0x3c	; 60
   4E65 28                  369 	.db #0x28	; 40
   4E66 28                  370 	.db #0x28	; 40
   4E67 00                  371 	.db #0x00	; 0
   4E68 00                  372 	.db #0x00	; 0
   4E69 00                  373 	.db #0x00	; 0
   4E6A 28                  374 	.db #0x28	; 40
   4E6B 00                  375 	.db #0x00	; 0
   4E6C 00                  376 	.db #0x00	; 0
   4E6D 00                  377 	.db #0x00	; 0
   4E6E 14                  378 	.db #0x14	; 20
   4E6F 3C                  379 	.db #0x3c	; 60
   4E70 3C                  380 	.db #0x3c	; 60
   4E71 28                  381 	.db #0x28	; 40
   4E72 00                  382 	.db #0x00	; 0
   4E73 00                  383 	.db #0x00	; 0
   4E74 00                  384 	.db #0x00	; 0
   4E75 14                  385 	.db #0x14	; 20
   4E76 00                  386 	.db #0x00	; 0
   4E77 00                  387 	.db #0x00	; 0
   4E78 00                  388 	.db #0x00	; 0
   4E79 14                  389 	.db #0x14	; 20
   4E7A 00                  390 	.db #0x00	; 0
   4E7B 00                  391 	.db #0x00	; 0
   4E7C 00                  392 	.db #0x00	; 0
   4E7D 14                  393 	.db #0x14	; 20
   4E7E 14                  394 	.db #0x14	; 20
   4E7F 3C                  395 	.db #0x3c	; 60
   4E80 3C                  396 	.db #0x3c	; 60
   4E81 28                  397 	.db #0x28	; 40
   4E82                     398 _huddigit_6:
   4E82 14                  399 	.db #0x14	; 20
   4E83 3C                  400 	.db #0x3c	; 60
   4E84 3C                  401 	.db #0x3c	; 60
   4E85 28                  402 	.db #0x28	; 40
   4E86 28                  403 	.db #0x28	; 40
   4E87 00                  404 	.db #0x00	; 0
   4E88 00                  405 	.db #0x00	; 0
   4E89 00                  406 	.db #0x00	; 0
   4E8A 28                  407 	.db #0x28	; 40
   4E8B 00                  408 	.db #0x00	; 0
   4E8C 00                  409 	.db #0x00	; 0
   4E8D 00                  410 	.db #0x00	; 0
   4E8E 14                  411 	.db #0x14	; 20
   4E8F 3C                  412 	.db #0x3c	; 60
   4E90 3C                  413 	.db #0x3c	; 60
   4E91 28                  414 	.db #0x28	; 40
   4E92 28                  415 	.db #0x28	; 40
   4E93 00                  416 	.db #0x00	; 0
   4E94 00                  417 	.db #0x00	; 0
   4E95 14                  418 	.db #0x14	; 20
   4E96 28                  419 	.db #0x28	; 40
   4E97 00                  420 	.db #0x00	; 0
   4E98 00                  421 	.db #0x00	; 0
   4E99 14                  422 	.db #0x14	; 20
   4E9A 28                  423 	.db #0x28	; 40
   4E9B 00                  424 	.db #0x00	; 0
   4E9C 00                  425 	.db #0x00	; 0
   4E9D 14                  426 	.db #0x14	; 20
   4E9E 14                  427 	.db #0x14	; 20
   4E9F 3C                  428 	.db #0x3c	; 60
   4EA0 3C                  429 	.db #0x3c	; 60
   4EA1 28                  430 	.db #0x28	; 40
   4EA2                     431 _huddigit_7:
   4EA2 14                  432 	.db #0x14	; 20
   4EA3 3C                  433 	.db #0x3c	; 60
   4EA4 3C                  434 	.db #0x3c	; 60
   4EA5 28                  435 	.db #0x28	; 40
   4EA6 00                  436 	.db #0x00	; 0
   4EA7 00                  437 	.db #0x00	; 0
   4EA8 00                  438 	.db #0x00	; 0
   4EA9 14                  439 	.db #0x14	; 20
   4EAA 00                  440 	.db #0x00	; 0
   4EAB 00                  441 	.db #0x00	; 0
   4EAC 00                  442 	.db #0x00	; 0
   4EAD 14                  443 	.db #0x14	; 20
   4EAE 00                  444 	.db #0x00	; 0
   4EAF 00                  445 	.db #0x00	; 0
   4EB0 00                  446 	.db #0x00	; 0
   4EB1 00                  447 	.db #0x00	; 0
   4EB2 00                  448 	.db #0x00	; 0
   4EB3 00                  449 	.db #0x00	; 0
   4EB4 00                  450 	.db #0x00	; 0
   4EB5 14                  451 	.db #0x14	; 20
   4EB6 00                  452 	.db #0x00	; 0
   4EB7 00                  453 	.db #0x00	; 0
   4EB8 00                  454 	.db #0x00	; 0
   4EB9 14                  455 	.db #0x14	; 20
   4EBA 00                  456 	.db #0x00	; 0
   4EBB 00                  457 	.db #0x00	; 0
   4EBC 00                  458 	.db #0x00	; 0
   4EBD 14                  459 	.db #0x14	; 20
   4EBE 00                  460 	.db #0x00	; 0
   4EBF 00                  461 	.db #0x00	; 0
   4EC0 00                  462 	.db #0x00	; 0
   4EC1 00                  463 	.db #0x00	; 0
   4EC2                     464 _huddigit_8:
   4EC2 14                  465 	.db #0x14	; 20
   4EC3 3C                  466 	.db #0x3c	; 60
   4EC4 3C                  467 	.db #0x3c	; 60
   4EC5 28                  468 	.db #0x28	; 40
   4EC6 28                  469 	.db #0x28	; 40
   4EC7 00                  470 	.db #0x00	; 0
   4EC8 00                  471 	.db #0x00	; 0
   4EC9 14                  472 	.db #0x14	; 20
   4ECA 28                  473 	.db #0x28	; 40
   4ECB 00                  474 	.db #0x00	; 0
   4ECC 00                  475 	.db #0x00	; 0
   4ECD 14                  476 	.db #0x14	; 20
   4ECE 14                  477 	.db #0x14	; 20
   4ECF 3C                  478 	.db #0x3c	; 60
   4ED0 3C                  479 	.db #0x3c	; 60
   4ED1 28                  480 	.db #0x28	; 40
   4ED2 28                  481 	.db #0x28	; 40
   4ED3 00                  482 	.db #0x00	; 0
   4ED4 00                  483 	.db #0x00	; 0
   4ED5 14                  484 	.db #0x14	; 20
   4ED6 28                  485 	.db #0x28	; 40
   4ED7 00                  486 	.db #0x00	; 0
   4ED8 00                  487 	.db #0x00	; 0
   4ED9 14                  488 	.db #0x14	; 20
   4EDA 28                  489 	.db #0x28	; 40
   4EDB 00                  490 	.db #0x00	; 0
   4EDC 00                  491 	.db #0x00	; 0
   4EDD 14                  492 	.db #0x14	; 20
   4EDE 14                  493 	.db #0x14	; 20
   4EDF 3C                  494 	.db #0x3c	; 60
   4EE0 3C                  495 	.db #0x3c	; 60
   4EE1 28                  496 	.db #0x28	; 40
   4EE2                     497 _huddigit_9:
   4EE2 14                  498 	.db #0x14	; 20
   4EE3 3C                  499 	.db #0x3c	; 60
   4EE4 3C                  500 	.db #0x3c	; 60
   4EE5 28                  501 	.db #0x28	; 40
   4EE6 28                  502 	.db #0x28	; 40
   4EE7 00                  503 	.db #0x00	; 0
   4EE8 00                  504 	.db #0x00	; 0
   4EE9 14                  505 	.db #0x14	; 20
   4EEA 28                  506 	.db #0x28	; 40
   4EEB 00                  507 	.db #0x00	; 0
   4EEC 00                  508 	.db #0x00	; 0
   4EED 14                  509 	.db #0x14	; 20
   4EEE 14                  510 	.db #0x14	; 20
   4EEF 3C                  511 	.db #0x3c	; 60
   4EF0 3C                  512 	.db #0x3c	; 60
   4EF1 28                  513 	.db #0x28	; 40
   4EF2 00                  514 	.db #0x00	; 0
   4EF3 00                  515 	.db #0x00	; 0
   4EF4 00                  516 	.db #0x00	; 0
   4EF5 14                  517 	.db #0x14	; 20
   4EF6 00                  518 	.db #0x00	; 0
   4EF7 00                  519 	.db #0x00	; 0
   4EF8 00                  520 	.db #0x00	; 0
   4EF9 14                  521 	.db #0x14	; 20
   4EFA 00                  522 	.db #0x00	; 0
   4EFB 00                  523 	.db #0x00	; 0
   4EFC 00                  524 	.db #0x00	; 0
   4EFD 14                  525 	.db #0x14	; 20
   4EFE 14                  526 	.db #0x14	; 20
   4EFF 3C                  527 	.db #0x3c	; 60
   4F00 3C                  528 	.db #0x3c	; 60
   4F01 28                  529 	.db #0x28	; 40
                            530 ;src/systems/hud.c:101: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            531 ;	---------------------------------
                            532 ; Function hud_draw_digits
                            533 ; ---------------------------------
   4F02                     534 _hud_draw_digits:
   4F02 DD E5         [15]  535 	push	ix
   4F04 DD 21 00 00   [14]  536 	ld	ix,#0
   4F08 DD 39         [15]  537 	add	ix,sp
   4F0A 3B            [ 6]  538 	dec	sp
                            539 ;src/systems/hud.c:107: divisor = 1;
   4F0B 01 01 00      [10]  540 	ld	bc, #0x0001
                            541 ;src/systems/hud.c:108: for (i = 1; i < digits; ++i) {
   4F0E 1E 01         [ 7]  542 	ld	e, #0x01
   4F10                     543 00106$:
   4F10 7B            [ 4]  544 	ld	a, e
   4F11 DD 96 06      [19]  545 	sub	a, 6 (ix)
   4F14 30 0B         [12]  546 	jr	NC,00101$
                            547 ;src/systems/hud.c:109: divisor *= 10;
   4F16 69            [ 4]  548 	ld	l, c
   4F17 60            [ 4]  549 	ld	h, b
   4F18 29            [11]  550 	add	hl, hl
   4F19 29            [11]  551 	add	hl, hl
   4F1A 09            [11]  552 	add	hl, bc
   4F1B 29            [11]  553 	add	hl, hl
   4F1C 4D            [ 4]  554 	ld	c, l
   4F1D 44            [ 4]  555 	ld	b, h
                            556 ;src/systems/hud.c:108: for (i = 1; i < digits; ++i) {
   4F1E 1C            [ 4]  557 	inc	e
   4F1F 18 EF         [12]  558 	jr	00106$
   4F21                     559 00101$:
                            560 ;src/systems/hud.c:112: for (i = 0; i < digits; ++i) {
   4F21 DD 36 FF 00   [19]  561 	ld	-1 (ix), #0x00
   4F25                     562 00109$:
   4F25 DD 7E FF      [19]  563 	ld	a, -1 (ix)
   4F28 DD 96 06      [19]  564 	sub	a, 6 (ix)
   4F2B 30 79         [12]  565 	jr	NC,00111$
                            566 ;src/systems/hud.c:113: digit = (u8)(value / divisor);
   4F2D C5            [11]  567 	push	bc
   4F2E C5            [11]  568 	push	bc
   4F2F DD 6E 04      [19]  569 	ld	l,4 (ix)
   4F32 DD 66 05      [19]  570 	ld	h,5 (ix)
   4F35 E5            [11]  571 	push	hl
   4F36 CD 84 64      [17]  572 	call	__divuint
   4F39 F1            [10]  573 	pop	af
   4F3A F1            [10]  574 	pop	af
   4F3B 5D            [ 4]  575 	ld	e, l
   4F3C C1            [10]  576 	pop	bc
                            577 ;src/systems/hud.c:114: value = (u16)(value % divisor);
   4F3D C5            [11]  578 	push	bc
   4F3E D5            [11]  579 	push	de
   4F3F C5            [11]  580 	push	bc
   4F40 DD 6E 04      [19]  581 	ld	l,4 (ix)
   4F43 DD 66 05      [19]  582 	ld	h,5 (ix)
   4F46 E5            [11]  583 	push	hl
   4F47 CD 0F 66      [17]  584 	call	__moduint
   4F4A F1            [10]  585 	pop	af
   4F4B F1            [10]  586 	pop	af
   4F4C D1            [10]  587 	pop	de
   4F4D C1            [10]  588 	pop	bc
   4F4E DD 75 04      [19]  589 	ld	4 (ix), l
   4F51 DD 74 05      [19]  590 	ld	5 (ix), h
                            591 ;src/systems/hud.c:116: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   4F54 DD 7E FF      [19]  592 	ld	a, -1 (ix)
   4F57 87            [ 4]  593 	add	a, a
   4F58 87            [ 4]  594 	add	a, a
   4F59 57            [ 4]  595 	ld	d, a
   4F5A DD 7E 07      [19]  596 	ld	a, 7 (ix)
   4F5D 82            [ 4]  597 	add	a, d
   4F5E 57            [ 4]  598 	ld	d, a
   4F5F C5            [11]  599 	push	bc
   4F60 D5            [11]  600 	push	de
   4F61 DD 7E 08      [19]  601 	ld	a, 8 (ix)
   4F64 F5            [11]  602 	push	af
   4F65 33            [ 6]  603 	inc	sp
   4F66 D5            [11]  604 	push	de
   4F67 33            [ 6]  605 	inc	sp
   4F68 21 00 C0      [10]  606 	ld	hl, #0xc000
   4F6B E5            [11]  607 	push	hl
   4F6C CD 2D 67      [17]  608 	call	_cpct_getScreenPtr
   4F6F D1            [10]  609 	pop	de
   4F70 C1            [10]  610 	pop	bc
                            611 ;src/systems/hud.c:117: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   4F71 E5            [11]  612 	push	hl
   4F72 C5            [11]  613 	push	bc
   4F73 7B            [ 4]  614 	ld	a, e
   4F74 F5            [11]  615 	push	af
   4F75 33            [ 6]  616 	inc	sp
   4F76 CD 21 4D      [17]  617 	call	_hud_get_number_sprite
   4F79 33            [ 6]  618 	inc	sp
   4F7A EB            [ 4]  619 	ex	de,hl
   4F7B C1            [10]  620 	pop	bc
   4F7C E1            [10]  621 	pop	hl
   4F7D D5            [11]  622 	push	de
   4F7E FD E1         [14]  623 	pop	iy
   4F80 C5            [11]  624 	push	bc
   4F81 11 04 08      [10]  625 	ld	de, #0x0804
   4F84 D5            [11]  626 	push	de
   4F85 E5            [11]  627 	push	hl
   4F86 FD E5         [15]  628 	push	iy
   4F88 CD 5E 65      [17]  629 	call	_cpct_drawSprite
   4F8B C1            [10]  630 	pop	bc
                            631 ;src/systems/hud.c:119: if (divisor > 1) {
   4F8C 3E 01         [ 7]  632 	ld	a, #0x01
   4F8E B9            [ 4]  633 	cp	a, c
   4F8F 3E 00         [ 7]  634 	ld	a, #0x00
   4F91 98            [ 4]  635 	sbc	a, b
   4F92 30 0C         [12]  636 	jr	NC,00110$
                            637 ;src/systems/hud.c:120: divisor /= 10;
   4F94 21 0A 00      [10]  638 	ld	hl, #0x000a
   4F97 E5            [11]  639 	push	hl
   4F98 C5            [11]  640 	push	bc
   4F99 CD 84 64      [17]  641 	call	__divuint
   4F9C F1            [10]  642 	pop	af
   4F9D F1            [10]  643 	pop	af
   4F9E 4D            [ 4]  644 	ld	c, l
   4F9F 44            [ 4]  645 	ld	b, h
   4FA0                     646 00110$:
                            647 ;src/systems/hud.c:112: for (i = 0; i < digits; ++i) {
   4FA0 DD 34 FF      [23]  648 	inc	-1 (ix)
   4FA3 C3 25 4F      [10]  649 	jp	00109$
   4FA6                     650 00111$:
   4FA6 33            [ 6]  651 	inc	sp
   4FA7 DD E1         [14]  652 	pop	ix
   4FA9 C9            [10]  653 	ret
                            654 ;src/systems/hud.c:125: void hudinit(void) {
                            655 ;	---------------------------------
                            656 ; Function hudinit
                            657 ; ---------------------------------
   4FAA                     658 _hudinit::
                            659 ;src/systems/hud.c:126: currenthealth = 3;
   4FAA 21 FE 67      [10]  660 	ld	hl,#_currenthealth + 0
   4FAD 36 03         [10]  661 	ld	(hl), #0x03
                            662 ;src/systems/hud.c:127: currentscore  = 0;
   4FAF 21 00 00      [10]  663 	ld	hl, #0x0000
   4FB2 22 FF 67      [16]  664 	ld	(_currentscore), hl
                            665 ;src/systems/hud.c:128: currenttime   = 90;
   4FB5 21 01 68      [10]  666 	ld	hl,#_currenttime + 0
   4FB8 36 5A         [10]  667 	ld	(hl), #0x5a
                            668 ;src/systems/hud.c:129: currentlives  = 3;
   4FBA 21 02 68      [10]  669 	ld	hl,#_currentlives + 0
   4FBD 36 03         [10]  670 	ld	(hl), #0x03
                            671 ;src/systems/hud.c:130: currentweapon = 0;
   4FBF 21 03 68      [10]  672 	ld	hl,#_currentweapon + 0
   4FC2 36 00         [10]  673 	ld	(hl), #0x00
   4FC4 C9            [10]  674 	ret
                            675 ;src/systems/hud.c:133: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            676 ;	---------------------------------
                            677 ; Function hudupdate
                            678 ; ---------------------------------
   4FC5                     679 _hudupdate::
                            680 ;src/systems/hud.c:134: currenthealth = lives;
   4FC5 21 02 00      [10]  681 	ld	hl, #2+0
   4FC8 39            [11]  682 	add	hl, sp
   4FC9 7E            [ 7]  683 	ld	a, (hl)
   4FCA 32 FE 67      [13]  684 	ld	(#_currenthealth + 0),a
                            685 ;src/systems/hud.c:135: currentscore  = score;
   4FCD 21 03 00      [10]  686 	ld	hl, #3+0
   4FD0 39            [11]  687 	add	hl, sp
   4FD1 7E            [ 7]  688 	ld	a, (hl)
   4FD2 32 FF 67      [13]  689 	ld	(#_currentscore + 0),a
   4FD5 21 04 00      [10]  690 	ld	hl, #3+1
   4FD8 39            [11]  691 	add	hl, sp
   4FD9 7E            [ 7]  692 	ld	a, (hl)
   4FDA 32 00 68      [13]  693 	ld	(#_currentscore + 1),a
                            694 ;src/systems/hud.c:136: currenttime   = time;
   4FDD 21 05 00      [10]  695 	ld	hl, #5+0
   4FE0 39            [11]  696 	add	hl, sp
   4FE1 7E            [ 7]  697 	ld	a, (hl)
   4FE2 32 01 68      [13]  698 	ld	(#_currenttime + 0),a
                            699 ;src/systems/hud.c:137: currentlives  = lives;
   4FE5 21 02 00      [10]  700 	ld	hl, #2+0
   4FE8 39            [11]  701 	add	hl, sp
   4FE9 7E            [ 7]  702 	ld	a, (hl)
   4FEA 32 02 68      [13]  703 	ld	(#_currentlives + 0),a
                            704 ;src/systems/hud.c:138: currentweapon = weapon;
   4FED 21 06 00      [10]  705 	ld	hl, #6+0
   4FF0 39            [11]  706 	add	hl, sp
   4FF1 7E            [ 7]  707 	ld	a, (hl)
   4FF2 32 03 68      [13]  708 	ld	(#_currentweapon + 0),a
   4FF5 C9            [10]  709 	ret
                            710 ;src/systems/hud.c:141: void hudrender(void) {
                            711 ;	---------------------------------
                            712 ; Function hudrender
                            713 ; ---------------------------------
   4FF6                     714 _hudrender::
                            715 ;src/systems/hud.c:147: for (i = 0; i < currenthealth; ++i) {
   4FF6 0E 00         [ 7]  716 	ld	c, #0x00
   4FF8                     717 00103$:
   4FF8 21 FE 67      [10]  718 	ld	hl, #_currenthealth
                            719 ;src/systems/hud.c:148: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4FFB 79            [ 4]  720 	ld	a,c
   4FFC BE            [ 7]  721 	cp	a,(hl)
   4FFD 30 24         [12]  722 	jr	NC,00101$
   4FFF 07            [ 4]  723 	rlca
   5000 07            [ 4]  724 	rlca
   5001 07            [ 4]  725 	rlca
   5002 E6 F8         [ 7]  726 	and	a, #0xf8
   5004 47            [ 4]  727 	ld	b, a
   5005 C5            [11]  728 	push	bc
   5006 3E 02         [ 7]  729 	ld	a, #0x02
   5008 F5            [11]  730 	push	af
   5009 33            [ 6]  731 	inc	sp
   500A C5            [11]  732 	push	bc
   500B 33            [ 6]  733 	inc	sp
   500C 21 00 C0      [10]  734 	ld	hl, #0xc000
   500F E5            [11]  735 	push	hl
   5010 CD 2D 67      [17]  736 	call	_cpct_getScreenPtr
   5013 11 04 08      [10]  737 	ld	de, #0x0804
   5016 D5            [11]  738 	push	de
   5017 E5            [11]  739 	push	hl
   5018 21 82 4D      [10]  740 	ld	hl, #_hudhealth
   501B E5            [11]  741 	push	hl
   501C CD 5E 65      [17]  742 	call	_cpct_drawSprite
   501F C1            [10]  743 	pop	bc
                            744 ;src/systems/hud.c:147: for (i = 0; i < currenthealth; ++i) {
   5020 0C            [ 4]  745 	inc	c
   5021 18 D5         [12]  746 	jr	00103$
   5023                     747 00101$:
                            748 ;src/systems/hud.c:152: scoretemp = currentscore;
   5023 2A FF 67      [16]  749 	ld	hl, (_currentscore)
                            750 ;src/systems/hud.c:153: hud_draw_digits(scoretemp, 4, 24, 2);
   5026 01 18 02      [10]  751 	ld	bc, #0x0218
   5029 C5            [11]  752 	push	bc
   502A 3E 04         [ 7]  753 	ld	a, #0x04
   502C F5            [11]  754 	push	af
   502D 33            [ 6]  755 	inc	sp
   502E E5            [11]  756 	push	hl
   502F CD 02 4F      [17]  757 	call	_hud_draw_digits
   5032 F1            [10]  758 	pop	af
   5033 F1            [10]  759 	pop	af
   5034 33            [ 6]  760 	inc	sp
                            761 ;src/systems/hud.c:155: timetemp = currenttime;
   5035 21 01 68      [10]  762 	ld	hl,#_currenttime + 0
   5038 4E            [ 7]  763 	ld	c, (hl)
                            764 ;src/systems/hud.c:156: hud_draw_digits((u16)timetemp, 3, 56, 2);
   5039 06 00         [ 7]  765 	ld	b, #0x00
   503B 21 38 02      [10]  766 	ld	hl, #0x0238
   503E E5            [11]  767 	push	hl
   503F 3E 03         [ 7]  768 	ld	a, #0x03
   5041 F5            [11]  769 	push	af
   5042 33            [ 6]  770 	inc	sp
   5043 C5            [11]  771 	push	bc
   5044 CD 02 4F      [17]  772 	call	_hud_draw_digits
   5047 F1            [10]  773 	pop	af
                            774 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   5048 33            [ 6]  775 	inc	sp
   5049 21 02 B4      [10]  776 	ld	hl,#0xb402
   504C E3            [19]  777 	ex	(sp),hl
   504D 21 00 C0      [10]  778 	ld	hl, #0xc000
   5050 E5            [11]  779 	push	hl
   5051 CD 2D 67      [17]  780 	call	_cpct_getScreenPtr
                            781 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   5054 01 A2 4D      [10]  782 	ld	bc, #_hudlives+0
   5057 11 04 08      [10]  783 	ld	de, #0x0804
   505A D5            [11]  784 	push	de
   505B E5            [11]  785 	push	hl
   505C C5            [11]  786 	push	bc
   505D CD 5E 65      [17]  787 	call	_cpct_drawSprite
                            788 ;src/systems/hud.c:161: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   5060 21 0C B4      [10]  789 	ld	hl, #0xb40c
   5063 E5            [11]  790 	push	hl
   5064 21 00 C0      [10]  791 	ld	hl, #0xc000
   5067 E5            [11]  792 	push	hl
   5068 CD 2D 67      [17]  793 	call	_cpct_getScreenPtr
                            794 ;src/systems/hud.c:162: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   506B E5            [11]  795 	push	hl
   506C 3E 0A         [ 7]  796 	ld	a, #0x0a
   506E F5            [11]  797 	push	af
   506F 33            [ 6]  798 	inc	sp
   5070 3A 02 68      [13]  799 	ld	a, (_currentlives)
   5073 F5            [11]  800 	push	af
   5074 33            [ 6]  801 	inc	sp
   5075 CD 03 66      [17]  802 	call	__moduchar
   5078 F1            [10]  803 	pop	af
   5079 55            [ 4]  804 	ld	d, l
   507A D5            [11]  805 	push	de
   507B 33            [ 6]  806 	inc	sp
   507C CD 21 4D      [17]  807 	call	_hud_get_number_sprite
   507F 33            [ 6]  808 	inc	sp
   5080 C1            [10]  809 	pop	bc
   5081 11 04 08      [10]  810 	ld	de, #0x0804
   5084 D5            [11]  811 	push	de
   5085 C5            [11]  812 	push	bc
   5086 E5            [11]  813 	push	hl
   5087 CD 5E 65      [17]  814 	call	_cpct_drawSprite
                            815 ;src/systems/hud.c:164: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   508A 21 46 B4      [10]  816 	ld	hl, #0xb446
   508D E5            [11]  817 	push	hl
   508E 21 00 C0      [10]  818 	ld	hl, #0xc000
   5091 E5            [11]  819 	push	hl
   5092 CD 2D 67      [17]  820 	call	_cpct_getScreenPtr
                            821 ;src/systems/hud.c:165: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   5095 E5            [11]  822 	push	hl
   5096 3E 0A         [ 7]  823 	ld	a, #0x0a
   5098 F5            [11]  824 	push	af
   5099 33            [ 6]  825 	inc	sp
   509A 3A 03 68      [13]  826 	ld	a, (_currentweapon)
   509D F5            [11]  827 	push	af
   509E 33            [ 6]  828 	inc	sp
   509F CD 03 66      [17]  829 	call	__moduchar
   50A2 F1            [10]  830 	pop	af
   50A3 55            [ 4]  831 	ld	d, l
   50A4 D5            [11]  832 	push	de
   50A5 33            [ 6]  833 	inc	sp
   50A6 CD 21 4D      [17]  834 	call	_hud_get_number_sprite
   50A9 33            [ 6]  835 	inc	sp
   50AA C1            [10]  836 	pop	bc
   50AB 11 04 08      [10]  837 	ld	de, #0x0804
   50AE D5            [11]  838 	push	de
   50AF C5            [11]  839 	push	bc
   50B0 E5            [11]  840 	push	hl
   50B1 CD 5E 65      [17]  841 	call	_cpct_drawSprite
   50B4 C9            [10]  842 	ret
                            843 	.area _CODE
                            844 	.area _INITIALIZER
                            845 	.area _CABS (ABS)
