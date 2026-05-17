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
   63BB                      23 _currenthealth:
   63BB                      24 	.ds 1
   63BC                      25 _currentscore:
   63BC                      26 	.ds 2
   63BE                      27 _currenttime:
   63BE                      28 	.ds 1
   63BF                      29 _currentlives:
   63BF                      30 	.ds 1
   63C0                      31 _currentweapon:
   63C0                      32 	.ds 1
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
   4D23                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:87: switch (digit % 10) {
   4D23 3E 0A         [ 7]   63 	ld	a, #0x0a
   4D25 F5            [11]   64 	push	af
   4D26 33            [ 6]   65 	inc	sp
   4D27 21 03 00      [10]   66 	ld	hl, #3+0
   4D2A 39            [11]   67 	add	hl, sp
   4D2B 7E            [ 7]   68 	ld	a, (hl)
   4D2C F5            [11]   69 	push	af
   4D2D 33            [ 6]   70 	inc	sp
   4D2E CD C0 61      [17]   71 	call	__moduchar
   4D31 F1            [10]   72 	pop	af
   4D32 4D            [ 4]   73 	ld	c, l
   4D33 3E 08         [ 7]   74 	ld	a, #0x08
   4D35 91            [ 4]   75 	sub	a, c
   4D36 38 48         [12]   76 	jr	C,00110$
   4D38 06 00         [ 7]   77 	ld	b, #0x00
   4D3A 21 41 4D      [10]   78 	ld	hl, #00118$
   4D3D 09            [11]   79 	add	hl, bc
   4D3E 09            [11]   80 	add	hl, bc
   4D3F 09            [11]   81 	add	hl, bc
   4D40 E9            [ 4]   82 	jp	(hl)
   4D41                      83 00118$:
   4D41 C3 5C 4D      [10]   84 	jp	00101$
   4D44 C3 60 4D      [10]   85 	jp	00102$
   4D47 C3 64 4D      [10]   86 	jp	00103$
   4D4A C3 68 4D      [10]   87 	jp	00104$
   4D4D C3 6C 4D      [10]   88 	jp	00105$
   4D50 C3 70 4D      [10]   89 	jp	00106$
   4D53 C3 74 4D      [10]   90 	jp	00107$
   4D56 C3 78 4D      [10]   91 	jp	00108$
   4D59 C3 7C 4D      [10]   92 	jp	00109$
                             93 ;src/systems/hud.c:88: case 0: return huddigit_0;
   4D5C                      94 00101$:
   4D5C 21 C4 4D      [10]   95 	ld	hl, #_huddigit_0
   4D5F C9            [10]   96 	ret
                             97 ;src/systems/hud.c:89: case 1: return huddigit_1;
   4D60                      98 00102$:
   4D60 21 E4 4D      [10]   99 	ld	hl, #_huddigit_1
   4D63 C9            [10]  100 	ret
                            101 ;src/systems/hud.c:90: case 2: return huddigit_2;
   4D64                     102 00103$:
   4D64 21 04 4E      [10]  103 	ld	hl, #_huddigit_2
   4D67 C9            [10]  104 	ret
                            105 ;src/systems/hud.c:91: case 3: return huddigit_3;
   4D68                     106 00104$:
   4D68 21 24 4E      [10]  107 	ld	hl, #_huddigit_3
   4D6B C9            [10]  108 	ret
                            109 ;src/systems/hud.c:92: case 4: return huddigit_4;
   4D6C                     110 00105$:
   4D6C 21 44 4E      [10]  111 	ld	hl, #_huddigit_4
   4D6F C9            [10]  112 	ret
                            113 ;src/systems/hud.c:93: case 5: return huddigit_5;
   4D70                     114 00106$:
   4D70 21 64 4E      [10]  115 	ld	hl, #_huddigit_5
   4D73 C9            [10]  116 	ret
                            117 ;src/systems/hud.c:94: case 6: return huddigit_6;
   4D74                     118 00107$:
   4D74 21 84 4E      [10]  119 	ld	hl, #_huddigit_6
   4D77 C9            [10]  120 	ret
                            121 ;src/systems/hud.c:95: case 7: return huddigit_7;
   4D78                     122 00108$:
   4D78 21 A4 4E      [10]  123 	ld	hl, #_huddigit_7
   4D7B C9            [10]  124 	ret
                            125 ;src/systems/hud.c:96: case 8: return huddigit_8;
   4D7C                     126 00109$:
   4D7C 21 C4 4E      [10]  127 	ld	hl, #_huddigit_8
   4D7F C9            [10]  128 	ret
                            129 ;src/systems/hud.c:97: default: return huddigit_9;
   4D80                     130 00110$:
   4D80 21 E4 4E      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:98: }
   4D83 C9            [10]  133 	ret
   4D84                     134 _hudhealth:
   4D84 3C                  135 	.db #0x3c	; 60
   4D85 3C                  136 	.db #0x3c	; 60
   4D86 3C                  137 	.db #0x3c	; 60
   4D87 3C                  138 	.db #0x3c	; 60
   4D88 28                  139 	.db #0x28	; 40
   4D89 28                  140 	.db #0x28	; 40
   4D8A 00                  141 	.db #0x00	; 0
   4D8B 14                  142 	.db #0x14	; 20
   4D8C 28                  143 	.db #0x28	; 40
   4D8D 28                  144 	.db #0x28	; 40
   4D8E 00                  145 	.db #0x00	; 0
   4D8F 14                  146 	.db #0x14	; 20
   4D90 28                  147 	.db #0x28	; 40
   4D91 28                  148 	.db #0x28	; 40
   4D92 00                  149 	.db #0x00	; 0
   4D93 14                  150 	.db #0x14	; 20
   4D94 3C                  151 	.db #0x3c	; 60
   4D95 3C                  152 	.db #0x3c	; 60
   4D96 3C                  153 	.db #0x3c	; 60
   4D97 3C                  154 	.db #0x3c	; 60
   4D98 28                  155 	.db #0x28	; 40
   4D99 28                  156 	.db #0x28	; 40
   4D9A 00                  157 	.db #0x00	; 0
   4D9B 14                  158 	.db #0x14	; 20
   4D9C 28                  159 	.db #0x28	; 40
   4D9D 28                  160 	.db #0x28	; 40
   4D9E 00                  161 	.db #0x00	; 0
   4D9F 14                  162 	.db #0x14	; 20
   4DA0 3C                  163 	.db #0x3c	; 60
   4DA1 3C                  164 	.db #0x3c	; 60
   4DA2 3C                  165 	.db #0x3c	; 60
   4DA3 3C                  166 	.db #0x3c	; 60
   4DA4                     167 _hudlives:
   4DA4 30                  168 	.db #0x30	; 48	'0'
   4DA5 30                  169 	.db #0x30	; 48	'0'
   4DA6 30                  170 	.db #0x30	; 48	'0'
   4DA7 30                  171 	.db #0x30	; 48	'0'
   4DA8 20                  172 	.db #0x20	; 32
   4DA9 10                  173 	.db #0x10	; 16
   4DAA 00                  174 	.db #0x00	; 0
   4DAB 10                  175 	.db #0x10	; 16
   4DAC 20                  176 	.db #0x20	; 32
   4DAD 10                  177 	.db #0x10	; 16
   4DAE 00                  178 	.db #0x00	; 0
   4DAF 10                  179 	.db #0x10	; 16
   4DB0 20                  180 	.db #0x20	; 32
   4DB1 10                  181 	.db #0x10	; 16
   4DB2 00                  182 	.db #0x00	; 0
   4DB3 10                  183 	.db #0x10	; 16
   4DB4 30                  184 	.db #0x30	; 48	'0'
   4DB5 30                  185 	.db #0x30	; 48	'0'
   4DB6 30                  186 	.db #0x30	; 48	'0'
   4DB7 30                  187 	.db #0x30	; 48	'0'
   4DB8 20                  188 	.db #0x20	; 32
   4DB9 10                  189 	.db #0x10	; 16
   4DBA 00                  190 	.db #0x00	; 0
   4DBB 10                  191 	.db #0x10	; 16
   4DBC 20                  192 	.db #0x20	; 32
   4DBD 10                  193 	.db #0x10	; 16
   4DBE 00                  194 	.db #0x00	; 0
   4DBF 10                  195 	.db #0x10	; 16
   4DC0 30                  196 	.db #0x30	; 48	'0'
   4DC1 30                  197 	.db #0x30	; 48	'0'
   4DC2 30                  198 	.db #0x30	; 48	'0'
   4DC3 30                  199 	.db #0x30	; 48	'0'
   4DC4                     200 _huddigit_0:
   4DC4 14                  201 	.db #0x14	; 20
   4DC5 3C                  202 	.db #0x3c	; 60
   4DC6 3C                  203 	.db #0x3c	; 60
   4DC7 28                  204 	.db #0x28	; 40
   4DC8 28                  205 	.db #0x28	; 40
   4DC9 00                  206 	.db #0x00	; 0
   4DCA 00                  207 	.db #0x00	; 0
   4DCB 14                  208 	.db #0x14	; 20
   4DCC 28                  209 	.db #0x28	; 40
   4DCD 00                  210 	.db #0x00	; 0
   4DCE 00                  211 	.db #0x00	; 0
   4DCF 14                  212 	.db #0x14	; 20
   4DD0 00                  213 	.db #0x00	; 0
   4DD1 00                  214 	.db #0x00	; 0
   4DD2 00                  215 	.db #0x00	; 0
   4DD3 00                  216 	.db #0x00	; 0
   4DD4 28                  217 	.db #0x28	; 40
   4DD5 00                  218 	.db #0x00	; 0
   4DD6 00                  219 	.db #0x00	; 0
   4DD7 14                  220 	.db #0x14	; 20
   4DD8 28                  221 	.db #0x28	; 40
   4DD9 00                  222 	.db #0x00	; 0
   4DDA 00                  223 	.db #0x00	; 0
   4DDB 14                  224 	.db #0x14	; 20
   4DDC 28                  225 	.db #0x28	; 40
   4DDD 00                  226 	.db #0x00	; 0
   4DDE 00                  227 	.db #0x00	; 0
   4DDF 14                  228 	.db #0x14	; 20
   4DE0 14                  229 	.db #0x14	; 20
   4DE1 3C                  230 	.db #0x3c	; 60
   4DE2 3C                  231 	.db #0x3c	; 60
   4DE3 28                  232 	.db #0x28	; 40
   4DE4                     233 _huddigit_1:
   4DE4 00                  234 	.db #0x00	; 0
   4DE5 00                  235 	.db #0x00	; 0
   4DE6 00                  236 	.db #0x00	; 0
   4DE7 00                  237 	.db #0x00	; 0
   4DE8 00                  238 	.db #0x00	; 0
   4DE9 00                  239 	.db #0x00	; 0
   4DEA 00                  240 	.db #0x00	; 0
   4DEB 14                  241 	.db #0x14	; 20
   4DEC 00                  242 	.db #0x00	; 0
   4DED 00                  243 	.db #0x00	; 0
   4DEE 00                  244 	.db #0x00	; 0
   4DEF 14                  245 	.db #0x14	; 20
   4DF0 00                  246 	.db #0x00	; 0
   4DF1 00                  247 	.db #0x00	; 0
   4DF2 00                  248 	.db #0x00	; 0
   4DF3 00                  249 	.db #0x00	; 0
   4DF4 00                  250 	.db #0x00	; 0
   4DF5 00                  251 	.db #0x00	; 0
   4DF6 00                  252 	.db #0x00	; 0
   4DF7 14                  253 	.db #0x14	; 20
   4DF8 00                  254 	.db #0x00	; 0
   4DF9 00                  255 	.db #0x00	; 0
   4DFA 00                  256 	.db #0x00	; 0
   4DFB 14                  257 	.db #0x14	; 20
   4DFC 00                  258 	.db #0x00	; 0
   4DFD 00                  259 	.db #0x00	; 0
   4DFE 00                  260 	.db #0x00	; 0
   4DFF 14                  261 	.db #0x14	; 20
   4E00 00                  262 	.db #0x00	; 0
   4E01 00                  263 	.db #0x00	; 0
   4E02 00                  264 	.db #0x00	; 0
   4E03 00                  265 	.db #0x00	; 0
   4E04                     266 _huddigit_2:
   4E04 14                  267 	.db #0x14	; 20
   4E05 3C                  268 	.db #0x3c	; 60
   4E06 3C                  269 	.db #0x3c	; 60
   4E07 28                  270 	.db #0x28	; 40
   4E08 00                  271 	.db #0x00	; 0
   4E09 00                  272 	.db #0x00	; 0
   4E0A 00                  273 	.db #0x00	; 0
   4E0B 14                  274 	.db #0x14	; 20
   4E0C 00                  275 	.db #0x00	; 0
   4E0D 00                  276 	.db #0x00	; 0
   4E0E 00                  277 	.db #0x00	; 0
   4E0F 14                  278 	.db #0x14	; 20
   4E10 14                  279 	.db #0x14	; 20
   4E11 3C                  280 	.db #0x3c	; 60
   4E12 3C                  281 	.db #0x3c	; 60
   4E13 28                  282 	.db #0x28	; 40
   4E14 28                  283 	.db #0x28	; 40
   4E15 00                  284 	.db #0x00	; 0
   4E16 00                  285 	.db #0x00	; 0
   4E17 00                  286 	.db #0x00	; 0
   4E18 28                  287 	.db #0x28	; 40
   4E19 00                  288 	.db #0x00	; 0
   4E1A 00                  289 	.db #0x00	; 0
   4E1B 00                  290 	.db #0x00	; 0
   4E1C 28                  291 	.db #0x28	; 40
   4E1D 00                  292 	.db #0x00	; 0
   4E1E 00                  293 	.db #0x00	; 0
   4E1F 00                  294 	.db #0x00	; 0
   4E20 14                  295 	.db #0x14	; 20
   4E21 3C                  296 	.db #0x3c	; 60
   4E22 3C                  297 	.db #0x3c	; 60
   4E23 28                  298 	.db #0x28	; 40
   4E24                     299 _huddigit_3:
   4E24 14                  300 	.db #0x14	; 20
   4E25 3C                  301 	.db #0x3c	; 60
   4E26 3C                  302 	.db #0x3c	; 60
   4E27 28                  303 	.db #0x28	; 40
   4E28 00                  304 	.db #0x00	; 0
   4E29 00                  305 	.db #0x00	; 0
   4E2A 00                  306 	.db #0x00	; 0
   4E2B 14                  307 	.db #0x14	; 20
   4E2C 00                  308 	.db #0x00	; 0
   4E2D 00                  309 	.db #0x00	; 0
   4E2E 00                  310 	.db #0x00	; 0
   4E2F 14                  311 	.db #0x14	; 20
   4E30 14                  312 	.db #0x14	; 20
   4E31 3C                  313 	.db #0x3c	; 60
   4E32 3C                  314 	.db #0x3c	; 60
   4E33 28                  315 	.db #0x28	; 40
   4E34 00                  316 	.db #0x00	; 0
   4E35 00                  317 	.db #0x00	; 0
   4E36 00                  318 	.db #0x00	; 0
   4E37 14                  319 	.db #0x14	; 20
   4E38 00                  320 	.db #0x00	; 0
   4E39 00                  321 	.db #0x00	; 0
   4E3A 00                  322 	.db #0x00	; 0
   4E3B 14                  323 	.db #0x14	; 20
   4E3C 00                  324 	.db #0x00	; 0
   4E3D 00                  325 	.db #0x00	; 0
   4E3E 00                  326 	.db #0x00	; 0
   4E3F 14                  327 	.db #0x14	; 20
   4E40 14                  328 	.db #0x14	; 20
   4E41 3C                  329 	.db #0x3c	; 60
   4E42 3C                  330 	.db #0x3c	; 60
   4E43 28                  331 	.db #0x28	; 40
   4E44                     332 _huddigit_4:
   4E44 00                  333 	.db #0x00	; 0
   4E45 00                  334 	.db #0x00	; 0
   4E46 00                  335 	.db #0x00	; 0
   4E47 00                  336 	.db #0x00	; 0
   4E48 28                  337 	.db #0x28	; 40
   4E49 00                  338 	.db #0x00	; 0
   4E4A 00                  339 	.db #0x00	; 0
   4E4B 14                  340 	.db #0x14	; 20
   4E4C 28                  341 	.db #0x28	; 40
   4E4D 00                  342 	.db #0x00	; 0
   4E4E 00                  343 	.db #0x00	; 0
   4E4F 14                  344 	.db #0x14	; 20
   4E50 14                  345 	.db #0x14	; 20
   4E51 3C                  346 	.db #0x3c	; 60
   4E52 3C                  347 	.db #0x3c	; 60
   4E53 28                  348 	.db #0x28	; 40
   4E54 00                  349 	.db #0x00	; 0
   4E55 00                  350 	.db #0x00	; 0
   4E56 00                  351 	.db #0x00	; 0
   4E57 14                  352 	.db #0x14	; 20
   4E58 00                  353 	.db #0x00	; 0
   4E59 00                  354 	.db #0x00	; 0
   4E5A 00                  355 	.db #0x00	; 0
   4E5B 14                  356 	.db #0x14	; 20
   4E5C 00                  357 	.db #0x00	; 0
   4E5D 00                  358 	.db #0x00	; 0
   4E5E 00                  359 	.db #0x00	; 0
   4E5F 14                  360 	.db #0x14	; 20
   4E60 00                  361 	.db #0x00	; 0
   4E61 00                  362 	.db #0x00	; 0
   4E62 00                  363 	.db #0x00	; 0
   4E63 00                  364 	.db #0x00	; 0
   4E64                     365 _huddigit_5:
   4E64 14                  366 	.db #0x14	; 20
   4E65 3C                  367 	.db #0x3c	; 60
   4E66 3C                  368 	.db #0x3c	; 60
   4E67 28                  369 	.db #0x28	; 40
   4E68 28                  370 	.db #0x28	; 40
   4E69 00                  371 	.db #0x00	; 0
   4E6A 00                  372 	.db #0x00	; 0
   4E6B 00                  373 	.db #0x00	; 0
   4E6C 28                  374 	.db #0x28	; 40
   4E6D 00                  375 	.db #0x00	; 0
   4E6E 00                  376 	.db #0x00	; 0
   4E6F 00                  377 	.db #0x00	; 0
   4E70 14                  378 	.db #0x14	; 20
   4E71 3C                  379 	.db #0x3c	; 60
   4E72 3C                  380 	.db #0x3c	; 60
   4E73 28                  381 	.db #0x28	; 40
   4E74 00                  382 	.db #0x00	; 0
   4E75 00                  383 	.db #0x00	; 0
   4E76 00                  384 	.db #0x00	; 0
   4E77 14                  385 	.db #0x14	; 20
   4E78 00                  386 	.db #0x00	; 0
   4E79 00                  387 	.db #0x00	; 0
   4E7A 00                  388 	.db #0x00	; 0
   4E7B 14                  389 	.db #0x14	; 20
   4E7C 00                  390 	.db #0x00	; 0
   4E7D 00                  391 	.db #0x00	; 0
   4E7E 00                  392 	.db #0x00	; 0
   4E7F 14                  393 	.db #0x14	; 20
   4E80 14                  394 	.db #0x14	; 20
   4E81 3C                  395 	.db #0x3c	; 60
   4E82 3C                  396 	.db #0x3c	; 60
   4E83 28                  397 	.db #0x28	; 40
   4E84                     398 _huddigit_6:
   4E84 14                  399 	.db #0x14	; 20
   4E85 3C                  400 	.db #0x3c	; 60
   4E86 3C                  401 	.db #0x3c	; 60
   4E87 28                  402 	.db #0x28	; 40
   4E88 28                  403 	.db #0x28	; 40
   4E89 00                  404 	.db #0x00	; 0
   4E8A 00                  405 	.db #0x00	; 0
   4E8B 00                  406 	.db #0x00	; 0
   4E8C 28                  407 	.db #0x28	; 40
   4E8D 00                  408 	.db #0x00	; 0
   4E8E 00                  409 	.db #0x00	; 0
   4E8F 00                  410 	.db #0x00	; 0
   4E90 14                  411 	.db #0x14	; 20
   4E91 3C                  412 	.db #0x3c	; 60
   4E92 3C                  413 	.db #0x3c	; 60
   4E93 28                  414 	.db #0x28	; 40
   4E94 28                  415 	.db #0x28	; 40
   4E95 00                  416 	.db #0x00	; 0
   4E96 00                  417 	.db #0x00	; 0
   4E97 14                  418 	.db #0x14	; 20
   4E98 28                  419 	.db #0x28	; 40
   4E99 00                  420 	.db #0x00	; 0
   4E9A 00                  421 	.db #0x00	; 0
   4E9B 14                  422 	.db #0x14	; 20
   4E9C 28                  423 	.db #0x28	; 40
   4E9D 00                  424 	.db #0x00	; 0
   4E9E 00                  425 	.db #0x00	; 0
   4E9F 14                  426 	.db #0x14	; 20
   4EA0 14                  427 	.db #0x14	; 20
   4EA1 3C                  428 	.db #0x3c	; 60
   4EA2 3C                  429 	.db #0x3c	; 60
   4EA3 28                  430 	.db #0x28	; 40
   4EA4                     431 _huddigit_7:
   4EA4 14                  432 	.db #0x14	; 20
   4EA5 3C                  433 	.db #0x3c	; 60
   4EA6 3C                  434 	.db #0x3c	; 60
   4EA7 28                  435 	.db #0x28	; 40
   4EA8 00                  436 	.db #0x00	; 0
   4EA9 00                  437 	.db #0x00	; 0
   4EAA 00                  438 	.db #0x00	; 0
   4EAB 14                  439 	.db #0x14	; 20
   4EAC 00                  440 	.db #0x00	; 0
   4EAD 00                  441 	.db #0x00	; 0
   4EAE 00                  442 	.db #0x00	; 0
   4EAF 14                  443 	.db #0x14	; 20
   4EB0 00                  444 	.db #0x00	; 0
   4EB1 00                  445 	.db #0x00	; 0
   4EB2 00                  446 	.db #0x00	; 0
   4EB3 00                  447 	.db #0x00	; 0
   4EB4 00                  448 	.db #0x00	; 0
   4EB5 00                  449 	.db #0x00	; 0
   4EB6 00                  450 	.db #0x00	; 0
   4EB7 14                  451 	.db #0x14	; 20
   4EB8 00                  452 	.db #0x00	; 0
   4EB9 00                  453 	.db #0x00	; 0
   4EBA 00                  454 	.db #0x00	; 0
   4EBB 14                  455 	.db #0x14	; 20
   4EBC 00                  456 	.db #0x00	; 0
   4EBD 00                  457 	.db #0x00	; 0
   4EBE 00                  458 	.db #0x00	; 0
   4EBF 14                  459 	.db #0x14	; 20
   4EC0 00                  460 	.db #0x00	; 0
   4EC1 00                  461 	.db #0x00	; 0
   4EC2 00                  462 	.db #0x00	; 0
   4EC3 00                  463 	.db #0x00	; 0
   4EC4                     464 _huddigit_8:
   4EC4 14                  465 	.db #0x14	; 20
   4EC5 3C                  466 	.db #0x3c	; 60
   4EC6 3C                  467 	.db #0x3c	; 60
   4EC7 28                  468 	.db #0x28	; 40
   4EC8 28                  469 	.db #0x28	; 40
   4EC9 00                  470 	.db #0x00	; 0
   4ECA 00                  471 	.db #0x00	; 0
   4ECB 14                  472 	.db #0x14	; 20
   4ECC 28                  473 	.db #0x28	; 40
   4ECD 00                  474 	.db #0x00	; 0
   4ECE 00                  475 	.db #0x00	; 0
   4ECF 14                  476 	.db #0x14	; 20
   4ED0 14                  477 	.db #0x14	; 20
   4ED1 3C                  478 	.db #0x3c	; 60
   4ED2 3C                  479 	.db #0x3c	; 60
   4ED3 28                  480 	.db #0x28	; 40
   4ED4 28                  481 	.db #0x28	; 40
   4ED5 00                  482 	.db #0x00	; 0
   4ED6 00                  483 	.db #0x00	; 0
   4ED7 14                  484 	.db #0x14	; 20
   4ED8 28                  485 	.db #0x28	; 40
   4ED9 00                  486 	.db #0x00	; 0
   4EDA 00                  487 	.db #0x00	; 0
   4EDB 14                  488 	.db #0x14	; 20
   4EDC 28                  489 	.db #0x28	; 40
   4EDD 00                  490 	.db #0x00	; 0
   4EDE 00                  491 	.db #0x00	; 0
   4EDF 14                  492 	.db #0x14	; 20
   4EE0 14                  493 	.db #0x14	; 20
   4EE1 3C                  494 	.db #0x3c	; 60
   4EE2 3C                  495 	.db #0x3c	; 60
   4EE3 28                  496 	.db #0x28	; 40
   4EE4                     497 _huddigit_9:
   4EE4 14                  498 	.db #0x14	; 20
   4EE5 3C                  499 	.db #0x3c	; 60
   4EE6 3C                  500 	.db #0x3c	; 60
   4EE7 28                  501 	.db #0x28	; 40
   4EE8 28                  502 	.db #0x28	; 40
   4EE9 00                  503 	.db #0x00	; 0
   4EEA 00                  504 	.db #0x00	; 0
   4EEB 14                  505 	.db #0x14	; 20
   4EEC 28                  506 	.db #0x28	; 40
   4EED 00                  507 	.db #0x00	; 0
   4EEE 00                  508 	.db #0x00	; 0
   4EEF 14                  509 	.db #0x14	; 20
   4EF0 14                  510 	.db #0x14	; 20
   4EF1 3C                  511 	.db #0x3c	; 60
   4EF2 3C                  512 	.db #0x3c	; 60
   4EF3 28                  513 	.db #0x28	; 40
   4EF4 00                  514 	.db #0x00	; 0
   4EF5 00                  515 	.db #0x00	; 0
   4EF6 00                  516 	.db #0x00	; 0
   4EF7 14                  517 	.db #0x14	; 20
   4EF8 00                  518 	.db #0x00	; 0
   4EF9 00                  519 	.db #0x00	; 0
   4EFA 00                  520 	.db #0x00	; 0
   4EFB 14                  521 	.db #0x14	; 20
   4EFC 00                  522 	.db #0x00	; 0
   4EFD 00                  523 	.db #0x00	; 0
   4EFE 00                  524 	.db #0x00	; 0
   4EFF 14                  525 	.db #0x14	; 20
   4F00 14                  526 	.db #0x14	; 20
   4F01 3C                  527 	.db #0x3c	; 60
   4F02 3C                  528 	.db #0x3c	; 60
   4F03 28                  529 	.db #0x28	; 40
                            530 ;src/systems/hud.c:101: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            531 ;	---------------------------------
                            532 ; Function hud_draw_digits
                            533 ; ---------------------------------
   4F04                     534 _hud_draw_digits:
   4F04 DD E5         [15]  535 	push	ix
   4F06 DD 21 00 00   [14]  536 	ld	ix,#0
   4F0A DD 39         [15]  537 	add	ix,sp
   4F0C 3B            [ 6]  538 	dec	sp
                            539 ;src/systems/hud.c:107: divisor = 1;
   4F0D 01 01 00      [10]  540 	ld	bc, #0x0001
                            541 ;src/systems/hud.c:108: for (i = 1; i < digits; ++i) {
   4F10 1E 01         [ 7]  542 	ld	e, #0x01
   4F12                     543 00106$:
   4F12 7B            [ 4]  544 	ld	a, e
   4F13 DD 96 06      [19]  545 	sub	a, 6 (ix)
   4F16 30 0B         [12]  546 	jr	NC,00101$
                            547 ;src/systems/hud.c:109: divisor *= 10;
   4F18 69            [ 4]  548 	ld	l, c
   4F19 60            [ 4]  549 	ld	h, b
   4F1A 29            [11]  550 	add	hl, hl
   4F1B 29            [11]  551 	add	hl, hl
   4F1C 09            [11]  552 	add	hl, bc
   4F1D 29            [11]  553 	add	hl, hl
   4F1E 4D            [ 4]  554 	ld	c, l
   4F1F 44            [ 4]  555 	ld	b, h
                            556 ;src/systems/hud.c:108: for (i = 1; i < digits; ++i) {
   4F20 1C            [ 4]  557 	inc	e
   4F21 18 EF         [12]  558 	jr	00106$
   4F23                     559 00101$:
                            560 ;src/systems/hud.c:112: for (i = 0; i < digits; ++i) {
   4F23 DD 36 FF 00   [19]  561 	ld	-1 (ix), #0x00
   4F27                     562 00109$:
   4F27 DD 7E FF      [19]  563 	ld	a, -1 (ix)
   4F2A DD 96 06      [19]  564 	sub	a, 6 (ix)
   4F2D 30 79         [12]  565 	jr	NC,00111$
                            566 ;src/systems/hud.c:113: digit = (u8)(value / divisor);
   4F2F C5            [11]  567 	push	bc
   4F30 C5            [11]  568 	push	bc
   4F31 DD 6E 04      [19]  569 	ld	l,4 (ix)
   4F34 DD 66 05      [19]  570 	ld	h,5 (ix)
   4F37 E5            [11]  571 	push	hl
   4F38 CD 41 60      [17]  572 	call	__divuint
   4F3B F1            [10]  573 	pop	af
   4F3C F1            [10]  574 	pop	af
   4F3D 5D            [ 4]  575 	ld	e, l
   4F3E C1            [10]  576 	pop	bc
                            577 ;src/systems/hud.c:114: value = (u16)(value % divisor);
   4F3F C5            [11]  578 	push	bc
   4F40 D5            [11]  579 	push	de
   4F41 C5            [11]  580 	push	bc
   4F42 DD 6E 04      [19]  581 	ld	l,4 (ix)
   4F45 DD 66 05      [19]  582 	ld	h,5 (ix)
   4F48 E5            [11]  583 	push	hl
   4F49 CD CC 61      [17]  584 	call	__moduint
   4F4C F1            [10]  585 	pop	af
   4F4D F1            [10]  586 	pop	af
   4F4E D1            [10]  587 	pop	de
   4F4F C1            [10]  588 	pop	bc
   4F50 DD 75 04      [19]  589 	ld	4 (ix), l
   4F53 DD 74 05      [19]  590 	ld	5 (ix), h
                            591 ;src/systems/hud.c:116: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   4F56 DD 7E FF      [19]  592 	ld	a, -1 (ix)
   4F59 87            [ 4]  593 	add	a, a
   4F5A 87            [ 4]  594 	add	a, a
   4F5B 57            [ 4]  595 	ld	d, a
   4F5C DD 7E 07      [19]  596 	ld	a, 7 (ix)
   4F5F 82            [ 4]  597 	add	a, d
   4F60 57            [ 4]  598 	ld	d, a
   4F61 C5            [11]  599 	push	bc
   4F62 D5            [11]  600 	push	de
   4F63 DD 7E 08      [19]  601 	ld	a, 8 (ix)
   4F66 F5            [11]  602 	push	af
   4F67 33            [ 6]  603 	inc	sp
   4F68 D5            [11]  604 	push	de
   4F69 33            [ 6]  605 	inc	sp
   4F6A 21 00 C0      [10]  606 	ld	hl, #0xc000
   4F6D E5            [11]  607 	push	hl
   4F6E CD EA 62      [17]  608 	call	_cpct_getScreenPtr
   4F71 D1            [10]  609 	pop	de
   4F72 C1            [10]  610 	pop	bc
                            611 ;src/systems/hud.c:117: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   4F73 E5            [11]  612 	push	hl
   4F74 C5            [11]  613 	push	bc
   4F75 7B            [ 4]  614 	ld	a, e
   4F76 F5            [11]  615 	push	af
   4F77 33            [ 6]  616 	inc	sp
   4F78 CD 23 4D      [17]  617 	call	_hud_get_number_sprite
   4F7B 33            [ 6]  618 	inc	sp
   4F7C EB            [ 4]  619 	ex	de,hl
   4F7D C1            [10]  620 	pop	bc
   4F7E E1            [10]  621 	pop	hl
   4F7F D5            [11]  622 	push	de
   4F80 FD E1         [14]  623 	pop	iy
   4F82 C5            [11]  624 	push	bc
   4F83 11 04 08      [10]  625 	ld	de, #0x0804
   4F86 D5            [11]  626 	push	de
   4F87 E5            [11]  627 	push	hl
   4F88 FD E5         [15]  628 	push	iy
   4F8A CD 1B 61      [17]  629 	call	_cpct_drawSprite
   4F8D C1            [10]  630 	pop	bc
                            631 ;src/systems/hud.c:119: if (divisor > 1) {
   4F8E 3E 01         [ 7]  632 	ld	a, #0x01
   4F90 B9            [ 4]  633 	cp	a, c
   4F91 3E 00         [ 7]  634 	ld	a, #0x00
   4F93 98            [ 4]  635 	sbc	a, b
   4F94 30 0C         [12]  636 	jr	NC,00110$
                            637 ;src/systems/hud.c:120: divisor /= 10;
   4F96 21 0A 00      [10]  638 	ld	hl, #0x000a
   4F99 E5            [11]  639 	push	hl
   4F9A C5            [11]  640 	push	bc
   4F9B CD 41 60      [17]  641 	call	__divuint
   4F9E F1            [10]  642 	pop	af
   4F9F F1            [10]  643 	pop	af
   4FA0 4D            [ 4]  644 	ld	c, l
   4FA1 44            [ 4]  645 	ld	b, h
   4FA2                     646 00110$:
                            647 ;src/systems/hud.c:112: for (i = 0; i < digits; ++i) {
   4FA2 DD 34 FF      [23]  648 	inc	-1 (ix)
   4FA5 C3 27 4F      [10]  649 	jp	00109$
   4FA8                     650 00111$:
   4FA8 33            [ 6]  651 	inc	sp
   4FA9 DD E1         [14]  652 	pop	ix
   4FAB C9            [10]  653 	ret
                            654 ;src/systems/hud.c:125: void hudinit(void) {
                            655 ;	---------------------------------
                            656 ; Function hudinit
                            657 ; ---------------------------------
   4FAC                     658 _hudinit::
                            659 ;src/systems/hud.c:126: currenthealth = 3;
   4FAC 21 BB 63      [10]  660 	ld	hl,#_currenthealth + 0
   4FAF 36 03         [10]  661 	ld	(hl), #0x03
                            662 ;src/systems/hud.c:127: currentscore  = 0;
   4FB1 21 00 00      [10]  663 	ld	hl, #0x0000
   4FB4 22 BC 63      [16]  664 	ld	(_currentscore), hl
                            665 ;src/systems/hud.c:128: currenttime   = 90;
   4FB7 21 BE 63      [10]  666 	ld	hl,#_currenttime + 0
   4FBA 36 5A         [10]  667 	ld	(hl), #0x5a
                            668 ;src/systems/hud.c:129: currentlives  = 3;
   4FBC 21 BF 63      [10]  669 	ld	hl,#_currentlives + 0
   4FBF 36 03         [10]  670 	ld	(hl), #0x03
                            671 ;src/systems/hud.c:130: currentweapon = 0;
   4FC1 21 C0 63      [10]  672 	ld	hl,#_currentweapon + 0
   4FC4 36 00         [10]  673 	ld	(hl), #0x00
   4FC6 C9            [10]  674 	ret
                            675 ;src/systems/hud.c:133: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            676 ;	---------------------------------
                            677 ; Function hudupdate
                            678 ; ---------------------------------
   4FC7                     679 _hudupdate::
                            680 ;src/systems/hud.c:134: currenthealth = lives;
   4FC7 21 02 00      [10]  681 	ld	hl, #2+0
   4FCA 39            [11]  682 	add	hl, sp
   4FCB 7E            [ 7]  683 	ld	a, (hl)
   4FCC 32 BB 63      [13]  684 	ld	(#_currenthealth + 0),a
                            685 ;src/systems/hud.c:135: currentscore  = score;
   4FCF 21 03 00      [10]  686 	ld	hl, #3+0
   4FD2 39            [11]  687 	add	hl, sp
   4FD3 7E            [ 7]  688 	ld	a, (hl)
   4FD4 32 BC 63      [13]  689 	ld	(#_currentscore + 0),a
   4FD7 21 04 00      [10]  690 	ld	hl, #3+1
   4FDA 39            [11]  691 	add	hl, sp
   4FDB 7E            [ 7]  692 	ld	a, (hl)
   4FDC 32 BD 63      [13]  693 	ld	(#_currentscore + 1),a
                            694 ;src/systems/hud.c:136: currenttime   = time;
   4FDF 21 05 00      [10]  695 	ld	hl, #5+0
   4FE2 39            [11]  696 	add	hl, sp
   4FE3 7E            [ 7]  697 	ld	a, (hl)
   4FE4 32 BE 63      [13]  698 	ld	(#_currenttime + 0),a
                            699 ;src/systems/hud.c:137: currentlives  = lives;
   4FE7 21 02 00      [10]  700 	ld	hl, #2+0
   4FEA 39            [11]  701 	add	hl, sp
   4FEB 7E            [ 7]  702 	ld	a, (hl)
   4FEC 32 BF 63      [13]  703 	ld	(#_currentlives + 0),a
                            704 ;src/systems/hud.c:138: currentweapon = weapon;
   4FEF 21 06 00      [10]  705 	ld	hl, #6+0
   4FF2 39            [11]  706 	add	hl, sp
   4FF3 7E            [ 7]  707 	ld	a, (hl)
   4FF4 32 C0 63      [13]  708 	ld	(#_currentweapon + 0),a
   4FF7 C9            [10]  709 	ret
                            710 ;src/systems/hud.c:141: void hudrender(void) {
                            711 ;	---------------------------------
                            712 ; Function hudrender
                            713 ; ---------------------------------
   4FF8                     714 _hudrender::
                            715 ;src/systems/hud.c:147: for (i = 0; i < currenthealth; ++i) {
   4FF8 0E 00         [ 7]  716 	ld	c, #0x00
   4FFA                     717 00103$:
   4FFA 21 BB 63      [10]  718 	ld	hl, #_currenthealth
                            719 ;src/systems/hud.c:148: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4FFD 79            [ 4]  720 	ld	a,c
   4FFE BE            [ 7]  721 	cp	a,(hl)
   4FFF 30 24         [12]  722 	jr	NC,00101$
   5001 07            [ 4]  723 	rlca
   5002 07            [ 4]  724 	rlca
   5003 07            [ 4]  725 	rlca
   5004 E6 F8         [ 7]  726 	and	a, #0xf8
   5006 47            [ 4]  727 	ld	b, a
   5007 C5            [11]  728 	push	bc
   5008 3E 02         [ 7]  729 	ld	a, #0x02
   500A F5            [11]  730 	push	af
   500B 33            [ 6]  731 	inc	sp
   500C C5            [11]  732 	push	bc
   500D 33            [ 6]  733 	inc	sp
   500E 21 00 C0      [10]  734 	ld	hl, #0xc000
   5011 E5            [11]  735 	push	hl
   5012 CD EA 62      [17]  736 	call	_cpct_getScreenPtr
   5015 11 04 08      [10]  737 	ld	de, #0x0804
   5018 D5            [11]  738 	push	de
   5019 E5            [11]  739 	push	hl
   501A 21 84 4D      [10]  740 	ld	hl, #_hudhealth
   501D E5            [11]  741 	push	hl
   501E CD 1B 61      [17]  742 	call	_cpct_drawSprite
   5021 C1            [10]  743 	pop	bc
                            744 ;src/systems/hud.c:147: for (i = 0; i < currenthealth; ++i) {
   5022 0C            [ 4]  745 	inc	c
   5023 18 D5         [12]  746 	jr	00103$
   5025                     747 00101$:
                            748 ;src/systems/hud.c:152: scoretemp = currentscore;
   5025 2A BC 63      [16]  749 	ld	hl, (_currentscore)
                            750 ;src/systems/hud.c:153: hud_draw_digits(scoretemp, 4, 24, 2);
   5028 01 18 02      [10]  751 	ld	bc, #0x0218
   502B C5            [11]  752 	push	bc
   502C 3E 04         [ 7]  753 	ld	a, #0x04
   502E F5            [11]  754 	push	af
   502F 33            [ 6]  755 	inc	sp
   5030 E5            [11]  756 	push	hl
   5031 CD 04 4F      [17]  757 	call	_hud_draw_digits
   5034 F1            [10]  758 	pop	af
   5035 F1            [10]  759 	pop	af
   5036 33            [ 6]  760 	inc	sp
                            761 ;src/systems/hud.c:155: timetemp = currenttime;
   5037 21 BE 63      [10]  762 	ld	hl,#_currenttime + 0
   503A 4E            [ 7]  763 	ld	c, (hl)
                            764 ;src/systems/hud.c:156: hud_draw_digits((u16)timetemp, 3, 56, 2);
   503B 06 00         [ 7]  765 	ld	b, #0x00
   503D 21 38 02      [10]  766 	ld	hl, #0x0238
   5040 E5            [11]  767 	push	hl
   5041 3E 03         [ 7]  768 	ld	a, #0x03
   5043 F5            [11]  769 	push	af
   5044 33            [ 6]  770 	inc	sp
   5045 C5            [11]  771 	push	bc
   5046 CD 04 4F      [17]  772 	call	_hud_draw_digits
   5049 F1            [10]  773 	pop	af
                            774 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   504A 33            [ 6]  775 	inc	sp
   504B 21 02 B4      [10]  776 	ld	hl,#0xb402
   504E E3            [19]  777 	ex	(sp),hl
   504F 21 00 C0      [10]  778 	ld	hl, #0xc000
   5052 E5            [11]  779 	push	hl
   5053 CD EA 62      [17]  780 	call	_cpct_getScreenPtr
                            781 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   5056 01 A4 4D      [10]  782 	ld	bc, #_hudlives+0
   5059 11 04 08      [10]  783 	ld	de, #0x0804
   505C D5            [11]  784 	push	de
   505D E5            [11]  785 	push	hl
   505E C5            [11]  786 	push	bc
   505F CD 1B 61      [17]  787 	call	_cpct_drawSprite
                            788 ;src/systems/hud.c:161: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   5062 21 0C B4      [10]  789 	ld	hl, #0xb40c
   5065 E5            [11]  790 	push	hl
   5066 21 00 C0      [10]  791 	ld	hl, #0xc000
   5069 E5            [11]  792 	push	hl
   506A CD EA 62      [17]  793 	call	_cpct_getScreenPtr
                            794 ;src/systems/hud.c:162: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   506D E5            [11]  795 	push	hl
   506E 3E 0A         [ 7]  796 	ld	a, #0x0a
   5070 F5            [11]  797 	push	af
   5071 33            [ 6]  798 	inc	sp
   5072 3A BF 63      [13]  799 	ld	a, (_currentlives)
   5075 F5            [11]  800 	push	af
   5076 33            [ 6]  801 	inc	sp
   5077 CD C0 61      [17]  802 	call	__moduchar
   507A F1            [10]  803 	pop	af
   507B 55            [ 4]  804 	ld	d, l
   507C D5            [11]  805 	push	de
   507D 33            [ 6]  806 	inc	sp
   507E CD 23 4D      [17]  807 	call	_hud_get_number_sprite
   5081 33            [ 6]  808 	inc	sp
   5082 C1            [10]  809 	pop	bc
   5083 11 04 08      [10]  810 	ld	de, #0x0804
   5086 D5            [11]  811 	push	de
   5087 C5            [11]  812 	push	bc
   5088 E5            [11]  813 	push	hl
   5089 CD 1B 61      [17]  814 	call	_cpct_drawSprite
                            815 ;src/systems/hud.c:164: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   508C 21 46 B4      [10]  816 	ld	hl, #0xb446
   508F E5            [11]  817 	push	hl
   5090 21 00 C0      [10]  818 	ld	hl, #0xc000
   5093 E5            [11]  819 	push	hl
   5094 CD EA 62      [17]  820 	call	_cpct_getScreenPtr
                            821 ;src/systems/hud.c:165: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   5097 E5            [11]  822 	push	hl
   5098 3E 0A         [ 7]  823 	ld	a, #0x0a
   509A F5            [11]  824 	push	af
   509B 33            [ 6]  825 	inc	sp
   509C 3A C0 63      [13]  826 	ld	a, (_currentweapon)
   509F F5            [11]  827 	push	af
   50A0 33            [ 6]  828 	inc	sp
   50A1 CD C0 61      [17]  829 	call	__moduchar
   50A4 F1            [10]  830 	pop	af
   50A5 55            [ 4]  831 	ld	d, l
   50A6 D5            [11]  832 	push	de
   50A7 33            [ 6]  833 	inc	sp
   50A8 CD 23 4D      [17]  834 	call	_hud_get_number_sprite
   50AB 33            [ 6]  835 	inc	sp
   50AC C1            [10]  836 	pop	bc
   50AD 11 04 08      [10]  837 	ld	de, #0x0804
   50B0 D5            [11]  838 	push	de
   50B1 C5            [11]  839 	push	bc
   50B2 E5            [11]  840 	push	hl
   50B3 CD 1B 61      [17]  841 	call	_cpct_drawSprite
   50B6 C9            [10]  842 	ret
                            843 	.area _CODE
                            844 	.area _INITIALIZER
                            845 	.area _CABS (ABS)
