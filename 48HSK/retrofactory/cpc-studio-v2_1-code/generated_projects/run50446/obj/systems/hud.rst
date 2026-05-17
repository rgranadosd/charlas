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
   6412                      23 _currenthealth:
   6412                      24 	.ds 1
   6413                      25 _currentscore:
   6413                      26 	.ds 2
   6415                      27 _currenttime:
   6415                      28 	.ds 1
   6416                      29 _currentlives:
   6416                      30 	.ds 1
   6417                      31 _currentweapon:
   6417                      32 	.ds 1
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
                             57 ;src/systems/hud.c:80: static const u8* hud_get_number_sprite(u8 digit) {
                             58 ;	---------------------------------
                             59 ; Function hud_get_number_sprite
                             60 ; ---------------------------------
   4D21                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:81: switch (digit % 10) {
   4D21 3E 0A         [ 7]   63 	ld	a, #0x0a
   4D23 F5            [11]   64 	push	af
   4D24 33            [ 6]   65 	inc	sp
   4D25 21 03 00      [10]   66 	ld	hl, #3+0
   4D28 39            [11]   67 	add	hl, sp
   4D29 7E            [ 7]   68 	ld	a, (hl)
   4D2A F5            [11]   69 	push	af
   4D2B 33            [ 6]   70 	inc	sp
   4D2C CD 17 62      [17]   71 	call	__moduchar
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
                             93 ;src/systems/hud.c:82: case 0: return huddigit_0;
   4D5A                      94 00101$:
   4D5A 21 A2 4D      [10]   95 	ld	hl, #_huddigit_0
   4D5D C9            [10]   96 	ret
                             97 ;src/systems/hud.c:83: case 1: return huddigit_1;
   4D5E                      98 00102$:
   4D5E 21 C2 4D      [10]   99 	ld	hl, #_huddigit_1
   4D61 C9            [10]  100 	ret
                            101 ;src/systems/hud.c:84: case 2: return huddigit_2;
   4D62                     102 00103$:
   4D62 21 E2 4D      [10]  103 	ld	hl, #_huddigit_2
   4D65 C9            [10]  104 	ret
                            105 ;src/systems/hud.c:85: case 3: return huddigit_3;
   4D66                     106 00104$:
   4D66 21 02 4E      [10]  107 	ld	hl, #_huddigit_3
   4D69 C9            [10]  108 	ret
                            109 ;src/systems/hud.c:86: case 4: return huddigit_4;
   4D6A                     110 00105$:
   4D6A 21 22 4E      [10]  111 	ld	hl, #_huddigit_4
   4D6D C9            [10]  112 	ret
                            113 ;src/systems/hud.c:87: case 5: return huddigit_5;
   4D6E                     114 00106$:
   4D6E 21 42 4E      [10]  115 	ld	hl, #_huddigit_5
   4D71 C9            [10]  116 	ret
                            117 ;src/systems/hud.c:88: case 6: return huddigit_6;
   4D72                     118 00107$:
   4D72 21 62 4E      [10]  119 	ld	hl, #_huddigit_6
   4D75 C9            [10]  120 	ret
                            121 ;src/systems/hud.c:89: case 7: return huddigit_7;
   4D76                     122 00108$:
   4D76 21 82 4E      [10]  123 	ld	hl, #_huddigit_7
   4D79 C9            [10]  124 	ret
                            125 ;src/systems/hud.c:90: case 8: return huddigit_8;
   4D7A                     126 00109$:
   4D7A 21 A2 4E      [10]  127 	ld	hl, #_huddigit_8
   4D7D C9            [10]  128 	ret
                            129 ;src/systems/hud.c:91: default: return huddigit_9;
   4D7E                     130 00110$:
   4D7E 21 C2 4E      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:92: }
   4D81 C9            [10]  133 	ret
   4D82                     134 _hudlives:
   4D82 30                  135 	.db #0x30	; 48	'0'
   4D83 30                  136 	.db #0x30	; 48	'0'
   4D84 30                  137 	.db #0x30	; 48	'0'
   4D85 30                  138 	.db #0x30	; 48	'0'
   4D86 20                  139 	.db #0x20	; 32
   4D87 10                  140 	.db #0x10	; 16
   4D88 00                  141 	.db #0x00	; 0
   4D89 10                  142 	.db #0x10	; 16
   4D8A 20                  143 	.db #0x20	; 32
   4D8B 10                  144 	.db #0x10	; 16
   4D8C 00                  145 	.db #0x00	; 0
   4D8D 10                  146 	.db #0x10	; 16
   4D8E 20                  147 	.db #0x20	; 32
   4D8F 10                  148 	.db #0x10	; 16
   4D90 00                  149 	.db #0x00	; 0
   4D91 10                  150 	.db #0x10	; 16
   4D92 30                  151 	.db #0x30	; 48	'0'
   4D93 30                  152 	.db #0x30	; 48	'0'
   4D94 30                  153 	.db #0x30	; 48	'0'
   4D95 30                  154 	.db #0x30	; 48	'0'
   4D96 20                  155 	.db #0x20	; 32
   4D97 10                  156 	.db #0x10	; 16
   4D98 00                  157 	.db #0x00	; 0
   4D99 10                  158 	.db #0x10	; 16
   4D9A 20                  159 	.db #0x20	; 32
   4D9B 10                  160 	.db #0x10	; 16
   4D9C 00                  161 	.db #0x00	; 0
   4D9D 10                  162 	.db #0x10	; 16
   4D9E 30                  163 	.db #0x30	; 48	'0'
   4D9F 30                  164 	.db #0x30	; 48	'0'
   4DA0 30                  165 	.db #0x30	; 48	'0'
   4DA1 30                  166 	.db #0x30	; 48	'0'
   4DA2                     167 _huddigit_0:
   4DA2 14                  168 	.db #0x14	; 20
   4DA3 3C                  169 	.db #0x3c	; 60
   4DA4 3C                  170 	.db #0x3c	; 60
   4DA5 28                  171 	.db #0x28	; 40
   4DA6 28                  172 	.db #0x28	; 40
   4DA7 00                  173 	.db #0x00	; 0
   4DA8 00                  174 	.db #0x00	; 0
   4DA9 14                  175 	.db #0x14	; 20
   4DAA 28                  176 	.db #0x28	; 40
   4DAB 00                  177 	.db #0x00	; 0
   4DAC 00                  178 	.db #0x00	; 0
   4DAD 14                  179 	.db #0x14	; 20
   4DAE 00                  180 	.db #0x00	; 0
   4DAF 00                  181 	.db #0x00	; 0
   4DB0 00                  182 	.db #0x00	; 0
   4DB1 00                  183 	.db #0x00	; 0
   4DB2 28                  184 	.db #0x28	; 40
   4DB3 00                  185 	.db #0x00	; 0
   4DB4 00                  186 	.db #0x00	; 0
   4DB5 14                  187 	.db #0x14	; 20
   4DB6 28                  188 	.db #0x28	; 40
   4DB7 00                  189 	.db #0x00	; 0
   4DB8 00                  190 	.db #0x00	; 0
   4DB9 14                  191 	.db #0x14	; 20
   4DBA 28                  192 	.db #0x28	; 40
   4DBB 00                  193 	.db #0x00	; 0
   4DBC 00                  194 	.db #0x00	; 0
   4DBD 14                  195 	.db #0x14	; 20
   4DBE 14                  196 	.db #0x14	; 20
   4DBF 3C                  197 	.db #0x3c	; 60
   4DC0 3C                  198 	.db #0x3c	; 60
   4DC1 28                  199 	.db #0x28	; 40
   4DC2                     200 _huddigit_1:
   4DC2 00                  201 	.db #0x00	; 0
   4DC3 00                  202 	.db #0x00	; 0
   4DC4 00                  203 	.db #0x00	; 0
   4DC5 00                  204 	.db #0x00	; 0
   4DC6 00                  205 	.db #0x00	; 0
   4DC7 00                  206 	.db #0x00	; 0
   4DC8 00                  207 	.db #0x00	; 0
   4DC9 14                  208 	.db #0x14	; 20
   4DCA 00                  209 	.db #0x00	; 0
   4DCB 00                  210 	.db #0x00	; 0
   4DCC 00                  211 	.db #0x00	; 0
   4DCD 14                  212 	.db #0x14	; 20
   4DCE 00                  213 	.db #0x00	; 0
   4DCF 00                  214 	.db #0x00	; 0
   4DD0 00                  215 	.db #0x00	; 0
   4DD1 00                  216 	.db #0x00	; 0
   4DD2 00                  217 	.db #0x00	; 0
   4DD3 00                  218 	.db #0x00	; 0
   4DD4 00                  219 	.db #0x00	; 0
   4DD5 14                  220 	.db #0x14	; 20
   4DD6 00                  221 	.db #0x00	; 0
   4DD7 00                  222 	.db #0x00	; 0
   4DD8 00                  223 	.db #0x00	; 0
   4DD9 14                  224 	.db #0x14	; 20
   4DDA 00                  225 	.db #0x00	; 0
   4DDB 00                  226 	.db #0x00	; 0
   4DDC 00                  227 	.db #0x00	; 0
   4DDD 14                  228 	.db #0x14	; 20
   4DDE 00                  229 	.db #0x00	; 0
   4DDF 00                  230 	.db #0x00	; 0
   4DE0 00                  231 	.db #0x00	; 0
   4DE1 00                  232 	.db #0x00	; 0
   4DE2                     233 _huddigit_2:
   4DE2 14                  234 	.db #0x14	; 20
   4DE3 3C                  235 	.db #0x3c	; 60
   4DE4 3C                  236 	.db #0x3c	; 60
   4DE5 28                  237 	.db #0x28	; 40
   4DE6 00                  238 	.db #0x00	; 0
   4DE7 00                  239 	.db #0x00	; 0
   4DE8 00                  240 	.db #0x00	; 0
   4DE9 14                  241 	.db #0x14	; 20
   4DEA 00                  242 	.db #0x00	; 0
   4DEB 00                  243 	.db #0x00	; 0
   4DEC 00                  244 	.db #0x00	; 0
   4DED 14                  245 	.db #0x14	; 20
   4DEE 14                  246 	.db #0x14	; 20
   4DEF 3C                  247 	.db #0x3c	; 60
   4DF0 3C                  248 	.db #0x3c	; 60
   4DF1 28                  249 	.db #0x28	; 40
   4DF2 28                  250 	.db #0x28	; 40
   4DF3 00                  251 	.db #0x00	; 0
   4DF4 00                  252 	.db #0x00	; 0
   4DF5 00                  253 	.db #0x00	; 0
   4DF6 28                  254 	.db #0x28	; 40
   4DF7 00                  255 	.db #0x00	; 0
   4DF8 00                  256 	.db #0x00	; 0
   4DF9 00                  257 	.db #0x00	; 0
   4DFA 28                  258 	.db #0x28	; 40
   4DFB 00                  259 	.db #0x00	; 0
   4DFC 00                  260 	.db #0x00	; 0
   4DFD 00                  261 	.db #0x00	; 0
   4DFE 14                  262 	.db #0x14	; 20
   4DFF 3C                  263 	.db #0x3c	; 60
   4E00 3C                  264 	.db #0x3c	; 60
   4E01 28                  265 	.db #0x28	; 40
   4E02                     266 _huddigit_3:
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
   4E12 00                  283 	.db #0x00	; 0
   4E13 00                  284 	.db #0x00	; 0
   4E14 00                  285 	.db #0x00	; 0
   4E15 14                  286 	.db #0x14	; 20
   4E16 00                  287 	.db #0x00	; 0
   4E17 00                  288 	.db #0x00	; 0
   4E18 00                  289 	.db #0x00	; 0
   4E19 14                  290 	.db #0x14	; 20
   4E1A 00                  291 	.db #0x00	; 0
   4E1B 00                  292 	.db #0x00	; 0
   4E1C 00                  293 	.db #0x00	; 0
   4E1D 14                  294 	.db #0x14	; 20
   4E1E 14                  295 	.db #0x14	; 20
   4E1F 3C                  296 	.db #0x3c	; 60
   4E20 3C                  297 	.db #0x3c	; 60
   4E21 28                  298 	.db #0x28	; 40
   4E22                     299 _huddigit_4:
   4E22 00                  300 	.db #0x00	; 0
   4E23 00                  301 	.db #0x00	; 0
   4E24 00                  302 	.db #0x00	; 0
   4E25 00                  303 	.db #0x00	; 0
   4E26 28                  304 	.db #0x28	; 40
   4E27 00                  305 	.db #0x00	; 0
   4E28 00                  306 	.db #0x00	; 0
   4E29 14                  307 	.db #0x14	; 20
   4E2A 28                  308 	.db #0x28	; 40
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
   4E3E 00                  328 	.db #0x00	; 0
   4E3F 00                  329 	.db #0x00	; 0
   4E40 00                  330 	.db #0x00	; 0
   4E41 00                  331 	.db #0x00	; 0
   4E42                     332 _huddigit_5:
   4E42 14                  333 	.db #0x14	; 20
   4E43 3C                  334 	.db #0x3c	; 60
   4E44 3C                  335 	.db #0x3c	; 60
   4E45 28                  336 	.db #0x28	; 40
   4E46 28                  337 	.db #0x28	; 40
   4E47 00                  338 	.db #0x00	; 0
   4E48 00                  339 	.db #0x00	; 0
   4E49 00                  340 	.db #0x00	; 0
   4E4A 28                  341 	.db #0x28	; 40
   4E4B 00                  342 	.db #0x00	; 0
   4E4C 00                  343 	.db #0x00	; 0
   4E4D 00                  344 	.db #0x00	; 0
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
   4E5E 14                  361 	.db #0x14	; 20
   4E5F 3C                  362 	.db #0x3c	; 60
   4E60 3C                  363 	.db #0x3c	; 60
   4E61 28                  364 	.db #0x28	; 40
   4E62                     365 _huddigit_6:
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
   4E72 28                  382 	.db #0x28	; 40
   4E73 00                  383 	.db #0x00	; 0
   4E74 00                  384 	.db #0x00	; 0
   4E75 14                  385 	.db #0x14	; 20
   4E76 28                  386 	.db #0x28	; 40
   4E77 00                  387 	.db #0x00	; 0
   4E78 00                  388 	.db #0x00	; 0
   4E79 14                  389 	.db #0x14	; 20
   4E7A 28                  390 	.db #0x28	; 40
   4E7B 00                  391 	.db #0x00	; 0
   4E7C 00                  392 	.db #0x00	; 0
   4E7D 14                  393 	.db #0x14	; 20
   4E7E 14                  394 	.db #0x14	; 20
   4E7F 3C                  395 	.db #0x3c	; 60
   4E80 3C                  396 	.db #0x3c	; 60
   4E81 28                  397 	.db #0x28	; 40
   4E82                     398 _huddigit_7:
   4E82 14                  399 	.db #0x14	; 20
   4E83 3C                  400 	.db #0x3c	; 60
   4E84 3C                  401 	.db #0x3c	; 60
   4E85 28                  402 	.db #0x28	; 40
   4E86 00                  403 	.db #0x00	; 0
   4E87 00                  404 	.db #0x00	; 0
   4E88 00                  405 	.db #0x00	; 0
   4E89 14                  406 	.db #0x14	; 20
   4E8A 00                  407 	.db #0x00	; 0
   4E8B 00                  408 	.db #0x00	; 0
   4E8C 00                  409 	.db #0x00	; 0
   4E8D 14                  410 	.db #0x14	; 20
   4E8E 00                  411 	.db #0x00	; 0
   4E8F 00                  412 	.db #0x00	; 0
   4E90 00                  413 	.db #0x00	; 0
   4E91 00                  414 	.db #0x00	; 0
   4E92 00                  415 	.db #0x00	; 0
   4E93 00                  416 	.db #0x00	; 0
   4E94 00                  417 	.db #0x00	; 0
   4E95 14                  418 	.db #0x14	; 20
   4E96 00                  419 	.db #0x00	; 0
   4E97 00                  420 	.db #0x00	; 0
   4E98 00                  421 	.db #0x00	; 0
   4E99 14                  422 	.db #0x14	; 20
   4E9A 00                  423 	.db #0x00	; 0
   4E9B 00                  424 	.db #0x00	; 0
   4E9C 00                  425 	.db #0x00	; 0
   4E9D 14                  426 	.db #0x14	; 20
   4E9E 00                  427 	.db #0x00	; 0
   4E9F 00                  428 	.db #0x00	; 0
   4EA0 00                  429 	.db #0x00	; 0
   4EA1 00                  430 	.db #0x00	; 0
   4EA2                     431 _huddigit_8:
   4EA2 14                  432 	.db #0x14	; 20
   4EA3 3C                  433 	.db #0x3c	; 60
   4EA4 3C                  434 	.db #0x3c	; 60
   4EA5 28                  435 	.db #0x28	; 40
   4EA6 28                  436 	.db #0x28	; 40
   4EA7 00                  437 	.db #0x00	; 0
   4EA8 00                  438 	.db #0x00	; 0
   4EA9 14                  439 	.db #0x14	; 20
   4EAA 28                  440 	.db #0x28	; 40
   4EAB 00                  441 	.db #0x00	; 0
   4EAC 00                  442 	.db #0x00	; 0
   4EAD 14                  443 	.db #0x14	; 20
   4EAE 14                  444 	.db #0x14	; 20
   4EAF 3C                  445 	.db #0x3c	; 60
   4EB0 3C                  446 	.db #0x3c	; 60
   4EB1 28                  447 	.db #0x28	; 40
   4EB2 28                  448 	.db #0x28	; 40
   4EB3 00                  449 	.db #0x00	; 0
   4EB4 00                  450 	.db #0x00	; 0
   4EB5 14                  451 	.db #0x14	; 20
   4EB6 28                  452 	.db #0x28	; 40
   4EB7 00                  453 	.db #0x00	; 0
   4EB8 00                  454 	.db #0x00	; 0
   4EB9 14                  455 	.db #0x14	; 20
   4EBA 28                  456 	.db #0x28	; 40
   4EBB 00                  457 	.db #0x00	; 0
   4EBC 00                  458 	.db #0x00	; 0
   4EBD 14                  459 	.db #0x14	; 20
   4EBE 14                  460 	.db #0x14	; 20
   4EBF 3C                  461 	.db #0x3c	; 60
   4EC0 3C                  462 	.db #0x3c	; 60
   4EC1 28                  463 	.db #0x28	; 40
   4EC2                     464 _huddigit_9:
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
   4ED2 00                  481 	.db #0x00	; 0
   4ED3 00                  482 	.db #0x00	; 0
   4ED4 00                  483 	.db #0x00	; 0
   4ED5 14                  484 	.db #0x14	; 20
   4ED6 00                  485 	.db #0x00	; 0
   4ED7 00                  486 	.db #0x00	; 0
   4ED8 00                  487 	.db #0x00	; 0
   4ED9 14                  488 	.db #0x14	; 20
   4EDA 00                  489 	.db #0x00	; 0
   4EDB 00                  490 	.db #0x00	; 0
   4EDC 00                  491 	.db #0x00	; 0
   4EDD 14                  492 	.db #0x14	; 20
   4EDE 14                  493 	.db #0x14	; 20
   4EDF 3C                  494 	.db #0x3c	; 60
   4EE0 3C                  495 	.db #0x3c	; 60
   4EE1 28                  496 	.db #0x28	; 40
                            497 ;src/systems/hud.c:95: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            498 ;	---------------------------------
                            499 ; Function hud_draw_digits
                            500 ; ---------------------------------
   4EE2                     501 _hud_draw_digits:
   4EE2 DD E5         [15]  502 	push	ix
   4EE4 DD 21 00 00   [14]  503 	ld	ix,#0
   4EE8 DD 39         [15]  504 	add	ix,sp
   4EEA 3B            [ 6]  505 	dec	sp
                            506 ;src/systems/hud.c:101: divisor = 1;
   4EEB 01 01 00      [10]  507 	ld	bc, #0x0001
                            508 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   4EEE 1E 01         [ 7]  509 	ld	e, #0x01
   4EF0                     510 00106$:
   4EF0 7B            [ 4]  511 	ld	a, e
   4EF1 DD 96 06      [19]  512 	sub	a, 6 (ix)
   4EF4 30 0B         [12]  513 	jr	NC,00101$
                            514 ;src/systems/hud.c:103: divisor *= 10;
   4EF6 69            [ 4]  515 	ld	l, c
   4EF7 60            [ 4]  516 	ld	h, b
   4EF8 29            [11]  517 	add	hl, hl
   4EF9 29            [11]  518 	add	hl, hl
   4EFA 09            [11]  519 	add	hl, bc
   4EFB 29            [11]  520 	add	hl, hl
   4EFC 4D            [ 4]  521 	ld	c, l
   4EFD 44            [ 4]  522 	ld	b, h
                            523 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   4EFE 1C            [ 4]  524 	inc	e
   4EFF 18 EF         [12]  525 	jr	00106$
   4F01                     526 00101$:
                            527 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   4F01 DD 36 FF 00   [19]  528 	ld	-1 (ix), #0x00
   4F05                     529 00109$:
   4F05 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   4F08 DD 96 06      [19]  531 	sub	a, 6 (ix)
   4F0B 30 79         [12]  532 	jr	NC,00111$
                            533 ;src/systems/hud.c:107: digit = (u8)(value / divisor);
   4F0D C5            [11]  534 	push	bc
   4F0E C5            [11]  535 	push	bc
   4F0F DD 6E 04      [19]  536 	ld	l,4 (ix)
   4F12 DD 66 05      [19]  537 	ld	h,5 (ix)
   4F15 E5            [11]  538 	push	hl
   4F16 CD 98 60      [17]  539 	call	__divuint
   4F19 F1            [10]  540 	pop	af
   4F1A F1            [10]  541 	pop	af
   4F1B 5D            [ 4]  542 	ld	e, l
   4F1C C1            [10]  543 	pop	bc
                            544 ;src/systems/hud.c:108: value = (u16)(value % divisor);
   4F1D C5            [11]  545 	push	bc
   4F1E D5            [11]  546 	push	de
   4F1F C5            [11]  547 	push	bc
   4F20 DD 6E 04      [19]  548 	ld	l,4 (ix)
   4F23 DD 66 05      [19]  549 	ld	h,5 (ix)
   4F26 E5            [11]  550 	push	hl
   4F27 CD 23 62      [17]  551 	call	__moduint
   4F2A F1            [10]  552 	pop	af
   4F2B F1            [10]  553 	pop	af
   4F2C D1            [10]  554 	pop	de
   4F2D C1            [10]  555 	pop	bc
   4F2E DD 75 04      [19]  556 	ld	4 (ix), l
   4F31 DD 74 05      [19]  557 	ld	5 (ix), h
                            558 ;src/systems/hud.c:110: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   4F34 DD 7E FF      [19]  559 	ld	a, -1 (ix)
   4F37 87            [ 4]  560 	add	a, a
   4F38 87            [ 4]  561 	add	a, a
   4F39 57            [ 4]  562 	ld	d, a
   4F3A DD 7E 07      [19]  563 	ld	a, 7 (ix)
   4F3D 82            [ 4]  564 	add	a, d
   4F3E 57            [ 4]  565 	ld	d, a
   4F3F C5            [11]  566 	push	bc
   4F40 D5            [11]  567 	push	de
   4F41 DD 7E 08      [19]  568 	ld	a, 8 (ix)
   4F44 F5            [11]  569 	push	af
   4F45 33            [ 6]  570 	inc	sp
   4F46 D5            [11]  571 	push	de
   4F47 33            [ 6]  572 	inc	sp
   4F48 21 00 C0      [10]  573 	ld	hl, #0xc000
   4F4B E5            [11]  574 	push	hl
   4F4C CD 41 63      [17]  575 	call	_cpct_getScreenPtr
   4F4F D1            [10]  576 	pop	de
   4F50 C1            [10]  577 	pop	bc
                            578 ;src/systems/hud.c:111: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   4F51 E5            [11]  579 	push	hl
   4F52 C5            [11]  580 	push	bc
   4F53 7B            [ 4]  581 	ld	a, e
   4F54 F5            [11]  582 	push	af
   4F55 33            [ 6]  583 	inc	sp
   4F56 CD 21 4D      [17]  584 	call	_hud_get_number_sprite
   4F59 33            [ 6]  585 	inc	sp
   4F5A EB            [ 4]  586 	ex	de,hl
   4F5B C1            [10]  587 	pop	bc
   4F5C E1            [10]  588 	pop	hl
   4F5D D5            [11]  589 	push	de
   4F5E FD E1         [14]  590 	pop	iy
   4F60 C5            [11]  591 	push	bc
   4F61 11 04 08      [10]  592 	ld	de, #0x0804
   4F64 D5            [11]  593 	push	de
   4F65 E5            [11]  594 	push	hl
   4F66 FD E5         [15]  595 	push	iy
   4F68 CD 72 61      [17]  596 	call	_cpct_drawSprite
   4F6B C1            [10]  597 	pop	bc
                            598 ;src/systems/hud.c:113: if (divisor > 1) {
   4F6C 3E 01         [ 7]  599 	ld	a, #0x01
   4F6E B9            [ 4]  600 	cp	a, c
   4F6F 3E 00         [ 7]  601 	ld	a, #0x00
   4F71 98            [ 4]  602 	sbc	a, b
   4F72 30 0C         [12]  603 	jr	NC,00110$
                            604 ;src/systems/hud.c:114: divisor /= 10;
   4F74 21 0A 00      [10]  605 	ld	hl, #0x000a
   4F77 E5            [11]  606 	push	hl
   4F78 C5            [11]  607 	push	bc
   4F79 CD 98 60      [17]  608 	call	__divuint
   4F7C F1            [10]  609 	pop	af
   4F7D F1            [10]  610 	pop	af
   4F7E 4D            [ 4]  611 	ld	c, l
   4F7F 44            [ 4]  612 	ld	b, h
   4F80                     613 00110$:
                            614 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   4F80 DD 34 FF      [23]  615 	inc	-1 (ix)
   4F83 C3 05 4F      [10]  616 	jp	00109$
   4F86                     617 00111$:
   4F86 33            [ 6]  618 	inc	sp
   4F87 DD E1         [14]  619 	pop	ix
   4F89 C9            [10]  620 	ret
                            621 ;src/systems/hud.c:119: void hudinit(void) {
                            622 ;	---------------------------------
                            623 ; Function hudinit
                            624 ; ---------------------------------
   4F8A                     625 _hudinit::
                            626 ;src/systems/hud.c:120: currenthealth = 3;
   4F8A 21 12 64      [10]  627 	ld	hl,#_currenthealth + 0
   4F8D 36 03         [10]  628 	ld	(hl), #0x03
                            629 ;src/systems/hud.c:121: currentscore  = 0;
   4F8F 21 00 00      [10]  630 	ld	hl, #0x0000
   4F92 22 13 64      [16]  631 	ld	(_currentscore), hl
                            632 ;src/systems/hud.c:122: currenttime   = 90;
   4F95 21 15 64      [10]  633 	ld	hl,#_currenttime + 0
   4F98 36 5A         [10]  634 	ld	(hl), #0x5a
                            635 ;src/systems/hud.c:123: currentlives  = 3;
   4F9A 21 16 64      [10]  636 	ld	hl,#_currentlives + 0
   4F9D 36 03         [10]  637 	ld	(hl), #0x03
                            638 ;src/systems/hud.c:124: currentweapon = 0;
   4F9F 21 17 64      [10]  639 	ld	hl,#_currentweapon + 0
   4FA2 36 00         [10]  640 	ld	(hl), #0x00
   4FA4 C9            [10]  641 	ret
                            642 ;src/systems/hud.c:127: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            643 ;	---------------------------------
                            644 ; Function hudupdate
                            645 ; ---------------------------------
   4FA5                     646 _hudupdate::
                            647 ;src/systems/hud.c:128: currenthealth = lives;
   4FA5 21 02 00      [10]  648 	ld	hl, #2+0
   4FA8 39            [11]  649 	add	hl, sp
   4FA9 7E            [ 7]  650 	ld	a, (hl)
   4FAA 32 12 64      [13]  651 	ld	(#_currenthealth + 0),a
                            652 ;src/systems/hud.c:129: currentscore  = score;
   4FAD 21 03 00      [10]  653 	ld	hl, #3+0
   4FB0 39            [11]  654 	add	hl, sp
   4FB1 7E            [ 7]  655 	ld	a, (hl)
   4FB2 32 13 64      [13]  656 	ld	(#_currentscore + 0),a
   4FB5 21 04 00      [10]  657 	ld	hl, #3+1
   4FB8 39            [11]  658 	add	hl, sp
   4FB9 7E            [ 7]  659 	ld	a, (hl)
   4FBA 32 14 64      [13]  660 	ld	(#_currentscore + 1),a
                            661 ;src/systems/hud.c:130: currenttime   = time;
   4FBD 21 05 00      [10]  662 	ld	hl, #5+0
   4FC0 39            [11]  663 	add	hl, sp
   4FC1 7E            [ 7]  664 	ld	a, (hl)
   4FC2 32 15 64      [13]  665 	ld	(#_currenttime + 0),a
                            666 ;src/systems/hud.c:131: currentlives  = lives;
   4FC5 21 02 00      [10]  667 	ld	hl, #2+0
   4FC8 39            [11]  668 	add	hl, sp
   4FC9 7E            [ 7]  669 	ld	a, (hl)
   4FCA 32 16 64      [13]  670 	ld	(#_currentlives + 0),a
                            671 ;src/systems/hud.c:132: currentweapon = weapon;
   4FCD 21 06 00      [10]  672 	ld	hl, #6+0
   4FD0 39            [11]  673 	add	hl, sp
   4FD1 7E            [ 7]  674 	ld	a, (hl)
   4FD2 32 17 64      [13]  675 	ld	(#_currentweapon + 0),a
   4FD5 C9            [10]  676 	ret
                            677 ;src/systems/hud.c:135: void hudrender(void) {
                            678 ;	---------------------------------
                            679 ; Function hudrender
                            680 ; ---------------------------------
   4FD6                     681 _hudrender::
                            682 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   4FD6 0E 00         [ 7]  683 	ld	c, #0x00
   4FD8                     684 00103$:
   4FD8 21 12 64      [10]  685 	ld	hl, #_currenthealth
                            686 ;src/systems/hud.c:142: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4FDB 79            [ 4]  687 	ld	a,c
   4FDC BE            [ 7]  688 	cp	a,(hl)
   4FDD 30 24         [12]  689 	jr	NC,00101$
   4FDF 07            [ 4]  690 	rlca
   4FE0 07            [ 4]  691 	rlca
   4FE1 07            [ 4]  692 	rlca
   4FE2 E6 F8         [ 7]  693 	and	a, #0xf8
   4FE4 47            [ 4]  694 	ld	b, a
   4FE5 C5            [11]  695 	push	bc
   4FE6 3E 02         [ 7]  696 	ld	a, #0x02
   4FE8 F5            [11]  697 	push	af
   4FE9 33            [ 6]  698 	inc	sp
   4FEA C5            [11]  699 	push	bc
   4FEB 33            [ 6]  700 	inc	sp
   4FEC 21 00 C0      [10]  701 	ld	hl, #0xc000
   4FEF E5            [11]  702 	push	hl
   4FF0 CD 41 63      [17]  703 	call	_cpct_getScreenPtr
   4FF3 11 04 08      [10]  704 	ld	de, #0x0804
   4FF6 D5            [11]  705 	push	de
   4FF7 E5            [11]  706 	push	hl
   4FF8 21 E7 54      [10]  707 	ld	hl, #_hudhealthbar_data
   4FFB E5            [11]  708 	push	hl
   4FFC CD 72 61      [17]  709 	call	_cpct_drawSprite
   4FFF C1            [10]  710 	pop	bc
                            711 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   5000 0C            [ 4]  712 	inc	c
   5001 18 D5         [12]  713 	jr	00103$
   5003                     714 00101$:
                            715 ;src/systems/hud.c:146: scoretemp = currentscore;
   5003 2A 13 64      [16]  716 	ld	hl, (_currentscore)
                            717 ;src/systems/hud.c:147: hud_draw_digits(scoretemp, 4, 24, 2);
   5006 01 18 02      [10]  718 	ld	bc, #0x0218
   5009 C5            [11]  719 	push	bc
   500A 3E 04         [ 7]  720 	ld	a, #0x04
   500C F5            [11]  721 	push	af
   500D 33            [ 6]  722 	inc	sp
   500E E5            [11]  723 	push	hl
   500F CD E2 4E      [17]  724 	call	_hud_draw_digits
   5012 F1            [10]  725 	pop	af
   5013 F1            [10]  726 	pop	af
   5014 33            [ 6]  727 	inc	sp
                            728 ;src/systems/hud.c:149: timetemp = currenttime;
   5015 21 15 64      [10]  729 	ld	hl,#_currenttime + 0
   5018 4E            [ 7]  730 	ld	c, (hl)
                            731 ;src/systems/hud.c:150: hud_draw_digits((u16)timetemp, 3, 56, 2);
   5019 06 00         [ 7]  732 	ld	b, #0x00
   501B 21 38 02      [10]  733 	ld	hl, #0x0238
   501E E5            [11]  734 	push	hl
   501F 3E 03         [ 7]  735 	ld	a, #0x03
   5021 F5            [11]  736 	push	af
   5022 33            [ 6]  737 	inc	sp
   5023 C5            [11]  738 	push	bc
   5024 CD E2 4E      [17]  739 	call	_hud_draw_digits
   5027 F1            [10]  740 	pop	af
                            741 ;src/systems/hud.c:152: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   5028 33            [ 6]  742 	inc	sp
   5029 21 02 B4      [10]  743 	ld	hl,#0xb402
   502C E3            [19]  744 	ex	(sp),hl
   502D 21 00 C0      [10]  745 	ld	hl, #0xc000
   5030 E5            [11]  746 	push	hl
   5031 CD 41 63      [17]  747 	call	_cpct_getScreenPtr
                            748 ;src/systems/hud.c:153: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   5034 01 82 4D      [10]  749 	ld	bc, #_hudlives+0
   5037 11 04 08      [10]  750 	ld	de, #0x0804
   503A D5            [11]  751 	push	de
   503B E5            [11]  752 	push	hl
   503C C5            [11]  753 	push	bc
   503D CD 72 61      [17]  754 	call	_cpct_drawSprite
                            755 ;src/systems/hud.c:155: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   5040 21 0C B4      [10]  756 	ld	hl, #0xb40c
   5043 E5            [11]  757 	push	hl
   5044 21 00 C0      [10]  758 	ld	hl, #0xc000
   5047 E5            [11]  759 	push	hl
   5048 CD 41 63      [17]  760 	call	_cpct_getScreenPtr
                            761 ;src/systems/hud.c:156: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   504B E5            [11]  762 	push	hl
   504C 3E 0A         [ 7]  763 	ld	a, #0x0a
   504E F5            [11]  764 	push	af
   504F 33            [ 6]  765 	inc	sp
   5050 3A 16 64      [13]  766 	ld	a, (_currentlives)
   5053 F5            [11]  767 	push	af
   5054 33            [ 6]  768 	inc	sp
   5055 CD 17 62      [17]  769 	call	__moduchar
   5058 F1            [10]  770 	pop	af
   5059 55            [ 4]  771 	ld	d, l
   505A D5            [11]  772 	push	de
   505B 33            [ 6]  773 	inc	sp
   505C CD 21 4D      [17]  774 	call	_hud_get_number_sprite
   505F 33            [ 6]  775 	inc	sp
   5060 C1            [10]  776 	pop	bc
   5061 11 04 08      [10]  777 	ld	de, #0x0804
   5064 D5            [11]  778 	push	de
   5065 C5            [11]  779 	push	bc
   5066 E5            [11]  780 	push	hl
   5067 CD 72 61      [17]  781 	call	_cpct_drawSprite
                            782 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   506A 21 46 B4      [10]  783 	ld	hl, #0xb446
   506D E5            [11]  784 	push	hl
   506E 21 00 C0      [10]  785 	ld	hl, #0xc000
   5071 E5            [11]  786 	push	hl
   5072 CD 41 63      [17]  787 	call	_cpct_getScreenPtr
                            788 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   5075 E5            [11]  789 	push	hl
   5076 3E 0A         [ 7]  790 	ld	a, #0x0a
   5078 F5            [11]  791 	push	af
   5079 33            [ 6]  792 	inc	sp
   507A 3A 17 64      [13]  793 	ld	a, (_currentweapon)
   507D F5            [11]  794 	push	af
   507E 33            [ 6]  795 	inc	sp
   507F CD 17 62      [17]  796 	call	__moduchar
   5082 F1            [10]  797 	pop	af
   5083 55            [ 4]  798 	ld	d, l
   5084 D5            [11]  799 	push	de
   5085 33            [ 6]  800 	inc	sp
   5086 CD 21 4D      [17]  801 	call	_hud_get_number_sprite
   5089 33            [ 6]  802 	inc	sp
   508A C1            [10]  803 	pop	bc
   508B 11 04 08      [10]  804 	ld	de, #0x0804
   508E D5            [11]  805 	push	de
   508F C5            [11]  806 	push	bc
   5090 E5            [11]  807 	push	hl
   5091 CD 72 61      [17]  808 	call	_cpct_drawSprite
   5094 C9            [10]  809 	ret
                            810 	.area _CODE
                            811 	.area _INITIALIZER
                            812 	.area _CABS (ABS)
