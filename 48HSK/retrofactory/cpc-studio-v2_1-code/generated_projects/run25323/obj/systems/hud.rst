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
   6378                      23 _currenthealth:
   6378                      24 	.ds 1
   6379                      25 _currentscore:
   6379                      26 	.ds 2
   637B                      27 _currenttime:
   637B                      28 	.ds 1
   637C                      29 _currentlives:
   637C                      30 	.ds 1
   637D                      31 _currentweapon:
   637D                      32 	.ds 1
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
   4D23                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:81: switch (digit % 10) {
   4D23 3E 0A         [ 7]   63 	ld	a, #0x0a
   4D25 F5            [11]   64 	push	af
   4D26 33            [ 6]   65 	inc	sp
   4D27 21 03 00      [10]   66 	ld	hl, #3+0
   4D2A 39            [11]   67 	add	hl, sp
   4D2B 7E            [ 7]   68 	ld	a, (hl)
   4D2C F5            [11]   69 	push	af
   4D2D 33            [ 6]   70 	inc	sp
   4D2E CD 7D 61      [17]   71 	call	__moduchar
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
                             93 ;src/systems/hud.c:82: case 0: return huddigit_0;
   4D5C                      94 00101$:
   4D5C 21 A4 4D      [10]   95 	ld	hl, #_huddigit_0
   4D5F C9            [10]   96 	ret
                             97 ;src/systems/hud.c:83: case 1: return huddigit_1;
   4D60                      98 00102$:
   4D60 21 C4 4D      [10]   99 	ld	hl, #_huddigit_1
   4D63 C9            [10]  100 	ret
                            101 ;src/systems/hud.c:84: case 2: return huddigit_2;
   4D64                     102 00103$:
   4D64 21 E4 4D      [10]  103 	ld	hl, #_huddigit_2
   4D67 C9            [10]  104 	ret
                            105 ;src/systems/hud.c:85: case 3: return huddigit_3;
   4D68                     106 00104$:
   4D68 21 04 4E      [10]  107 	ld	hl, #_huddigit_3
   4D6B C9            [10]  108 	ret
                            109 ;src/systems/hud.c:86: case 4: return huddigit_4;
   4D6C                     110 00105$:
   4D6C 21 24 4E      [10]  111 	ld	hl, #_huddigit_4
   4D6F C9            [10]  112 	ret
                            113 ;src/systems/hud.c:87: case 5: return huddigit_5;
   4D70                     114 00106$:
   4D70 21 44 4E      [10]  115 	ld	hl, #_huddigit_5
   4D73 C9            [10]  116 	ret
                            117 ;src/systems/hud.c:88: case 6: return huddigit_6;
   4D74                     118 00107$:
   4D74 21 64 4E      [10]  119 	ld	hl, #_huddigit_6
   4D77 C9            [10]  120 	ret
                            121 ;src/systems/hud.c:89: case 7: return huddigit_7;
   4D78                     122 00108$:
   4D78 21 84 4E      [10]  123 	ld	hl, #_huddigit_7
   4D7B C9            [10]  124 	ret
                            125 ;src/systems/hud.c:90: case 8: return huddigit_8;
   4D7C                     126 00109$:
   4D7C 21 A4 4E      [10]  127 	ld	hl, #_huddigit_8
   4D7F C9            [10]  128 	ret
                            129 ;src/systems/hud.c:91: default: return huddigit_9;
   4D80                     130 00110$:
   4D80 21 C4 4E      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:92: }
   4D83 C9            [10]  133 	ret
   4D84                     134 _hudlives:
   4D84 30                  135 	.db #0x30	; 48	'0'
   4D85 30                  136 	.db #0x30	; 48	'0'
   4D86 30                  137 	.db #0x30	; 48	'0'
   4D87 30                  138 	.db #0x30	; 48	'0'
   4D88 20                  139 	.db #0x20	; 32
   4D89 10                  140 	.db #0x10	; 16
   4D8A 00                  141 	.db #0x00	; 0
   4D8B 10                  142 	.db #0x10	; 16
   4D8C 20                  143 	.db #0x20	; 32
   4D8D 10                  144 	.db #0x10	; 16
   4D8E 00                  145 	.db #0x00	; 0
   4D8F 10                  146 	.db #0x10	; 16
   4D90 20                  147 	.db #0x20	; 32
   4D91 10                  148 	.db #0x10	; 16
   4D92 00                  149 	.db #0x00	; 0
   4D93 10                  150 	.db #0x10	; 16
   4D94 30                  151 	.db #0x30	; 48	'0'
   4D95 30                  152 	.db #0x30	; 48	'0'
   4D96 30                  153 	.db #0x30	; 48	'0'
   4D97 30                  154 	.db #0x30	; 48	'0'
   4D98 20                  155 	.db #0x20	; 32
   4D99 10                  156 	.db #0x10	; 16
   4D9A 00                  157 	.db #0x00	; 0
   4D9B 10                  158 	.db #0x10	; 16
   4D9C 20                  159 	.db #0x20	; 32
   4D9D 10                  160 	.db #0x10	; 16
   4D9E 00                  161 	.db #0x00	; 0
   4D9F 10                  162 	.db #0x10	; 16
   4DA0 30                  163 	.db #0x30	; 48	'0'
   4DA1 30                  164 	.db #0x30	; 48	'0'
   4DA2 30                  165 	.db #0x30	; 48	'0'
   4DA3 30                  166 	.db #0x30	; 48	'0'
   4DA4                     167 _huddigit_0:
   4DA4 14                  168 	.db #0x14	; 20
   4DA5 3C                  169 	.db #0x3c	; 60
   4DA6 3C                  170 	.db #0x3c	; 60
   4DA7 28                  171 	.db #0x28	; 40
   4DA8 28                  172 	.db #0x28	; 40
   4DA9 00                  173 	.db #0x00	; 0
   4DAA 00                  174 	.db #0x00	; 0
   4DAB 14                  175 	.db #0x14	; 20
   4DAC 28                  176 	.db #0x28	; 40
   4DAD 00                  177 	.db #0x00	; 0
   4DAE 00                  178 	.db #0x00	; 0
   4DAF 14                  179 	.db #0x14	; 20
   4DB0 00                  180 	.db #0x00	; 0
   4DB1 00                  181 	.db #0x00	; 0
   4DB2 00                  182 	.db #0x00	; 0
   4DB3 00                  183 	.db #0x00	; 0
   4DB4 28                  184 	.db #0x28	; 40
   4DB5 00                  185 	.db #0x00	; 0
   4DB6 00                  186 	.db #0x00	; 0
   4DB7 14                  187 	.db #0x14	; 20
   4DB8 28                  188 	.db #0x28	; 40
   4DB9 00                  189 	.db #0x00	; 0
   4DBA 00                  190 	.db #0x00	; 0
   4DBB 14                  191 	.db #0x14	; 20
   4DBC 28                  192 	.db #0x28	; 40
   4DBD 00                  193 	.db #0x00	; 0
   4DBE 00                  194 	.db #0x00	; 0
   4DBF 14                  195 	.db #0x14	; 20
   4DC0 14                  196 	.db #0x14	; 20
   4DC1 3C                  197 	.db #0x3c	; 60
   4DC2 3C                  198 	.db #0x3c	; 60
   4DC3 28                  199 	.db #0x28	; 40
   4DC4                     200 _huddigit_1:
   4DC4 00                  201 	.db #0x00	; 0
   4DC5 00                  202 	.db #0x00	; 0
   4DC6 00                  203 	.db #0x00	; 0
   4DC7 00                  204 	.db #0x00	; 0
   4DC8 00                  205 	.db #0x00	; 0
   4DC9 00                  206 	.db #0x00	; 0
   4DCA 00                  207 	.db #0x00	; 0
   4DCB 14                  208 	.db #0x14	; 20
   4DCC 00                  209 	.db #0x00	; 0
   4DCD 00                  210 	.db #0x00	; 0
   4DCE 00                  211 	.db #0x00	; 0
   4DCF 14                  212 	.db #0x14	; 20
   4DD0 00                  213 	.db #0x00	; 0
   4DD1 00                  214 	.db #0x00	; 0
   4DD2 00                  215 	.db #0x00	; 0
   4DD3 00                  216 	.db #0x00	; 0
   4DD4 00                  217 	.db #0x00	; 0
   4DD5 00                  218 	.db #0x00	; 0
   4DD6 00                  219 	.db #0x00	; 0
   4DD7 14                  220 	.db #0x14	; 20
   4DD8 00                  221 	.db #0x00	; 0
   4DD9 00                  222 	.db #0x00	; 0
   4DDA 00                  223 	.db #0x00	; 0
   4DDB 14                  224 	.db #0x14	; 20
   4DDC 00                  225 	.db #0x00	; 0
   4DDD 00                  226 	.db #0x00	; 0
   4DDE 00                  227 	.db #0x00	; 0
   4DDF 14                  228 	.db #0x14	; 20
   4DE0 00                  229 	.db #0x00	; 0
   4DE1 00                  230 	.db #0x00	; 0
   4DE2 00                  231 	.db #0x00	; 0
   4DE3 00                  232 	.db #0x00	; 0
   4DE4                     233 _huddigit_2:
   4DE4 14                  234 	.db #0x14	; 20
   4DE5 3C                  235 	.db #0x3c	; 60
   4DE6 3C                  236 	.db #0x3c	; 60
   4DE7 28                  237 	.db #0x28	; 40
   4DE8 00                  238 	.db #0x00	; 0
   4DE9 00                  239 	.db #0x00	; 0
   4DEA 00                  240 	.db #0x00	; 0
   4DEB 14                  241 	.db #0x14	; 20
   4DEC 00                  242 	.db #0x00	; 0
   4DED 00                  243 	.db #0x00	; 0
   4DEE 00                  244 	.db #0x00	; 0
   4DEF 14                  245 	.db #0x14	; 20
   4DF0 14                  246 	.db #0x14	; 20
   4DF1 3C                  247 	.db #0x3c	; 60
   4DF2 3C                  248 	.db #0x3c	; 60
   4DF3 28                  249 	.db #0x28	; 40
   4DF4 28                  250 	.db #0x28	; 40
   4DF5 00                  251 	.db #0x00	; 0
   4DF6 00                  252 	.db #0x00	; 0
   4DF7 00                  253 	.db #0x00	; 0
   4DF8 28                  254 	.db #0x28	; 40
   4DF9 00                  255 	.db #0x00	; 0
   4DFA 00                  256 	.db #0x00	; 0
   4DFB 00                  257 	.db #0x00	; 0
   4DFC 28                  258 	.db #0x28	; 40
   4DFD 00                  259 	.db #0x00	; 0
   4DFE 00                  260 	.db #0x00	; 0
   4DFF 00                  261 	.db #0x00	; 0
   4E00 14                  262 	.db #0x14	; 20
   4E01 3C                  263 	.db #0x3c	; 60
   4E02 3C                  264 	.db #0x3c	; 60
   4E03 28                  265 	.db #0x28	; 40
   4E04                     266 _huddigit_3:
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
   4E14 00                  283 	.db #0x00	; 0
   4E15 00                  284 	.db #0x00	; 0
   4E16 00                  285 	.db #0x00	; 0
   4E17 14                  286 	.db #0x14	; 20
   4E18 00                  287 	.db #0x00	; 0
   4E19 00                  288 	.db #0x00	; 0
   4E1A 00                  289 	.db #0x00	; 0
   4E1B 14                  290 	.db #0x14	; 20
   4E1C 00                  291 	.db #0x00	; 0
   4E1D 00                  292 	.db #0x00	; 0
   4E1E 00                  293 	.db #0x00	; 0
   4E1F 14                  294 	.db #0x14	; 20
   4E20 14                  295 	.db #0x14	; 20
   4E21 3C                  296 	.db #0x3c	; 60
   4E22 3C                  297 	.db #0x3c	; 60
   4E23 28                  298 	.db #0x28	; 40
   4E24                     299 _huddigit_4:
   4E24 00                  300 	.db #0x00	; 0
   4E25 00                  301 	.db #0x00	; 0
   4E26 00                  302 	.db #0x00	; 0
   4E27 00                  303 	.db #0x00	; 0
   4E28 28                  304 	.db #0x28	; 40
   4E29 00                  305 	.db #0x00	; 0
   4E2A 00                  306 	.db #0x00	; 0
   4E2B 14                  307 	.db #0x14	; 20
   4E2C 28                  308 	.db #0x28	; 40
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
   4E40 00                  328 	.db #0x00	; 0
   4E41 00                  329 	.db #0x00	; 0
   4E42 00                  330 	.db #0x00	; 0
   4E43 00                  331 	.db #0x00	; 0
   4E44                     332 _huddigit_5:
   4E44 14                  333 	.db #0x14	; 20
   4E45 3C                  334 	.db #0x3c	; 60
   4E46 3C                  335 	.db #0x3c	; 60
   4E47 28                  336 	.db #0x28	; 40
   4E48 28                  337 	.db #0x28	; 40
   4E49 00                  338 	.db #0x00	; 0
   4E4A 00                  339 	.db #0x00	; 0
   4E4B 00                  340 	.db #0x00	; 0
   4E4C 28                  341 	.db #0x28	; 40
   4E4D 00                  342 	.db #0x00	; 0
   4E4E 00                  343 	.db #0x00	; 0
   4E4F 00                  344 	.db #0x00	; 0
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
   4E60 14                  361 	.db #0x14	; 20
   4E61 3C                  362 	.db #0x3c	; 60
   4E62 3C                  363 	.db #0x3c	; 60
   4E63 28                  364 	.db #0x28	; 40
   4E64                     365 _huddigit_6:
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
   4E74 28                  382 	.db #0x28	; 40
   4E75 00                  383 	.db #0x00	; 0
   4E76 00                  384 	.db #0x00	; 0
   4E77 14                  385 	.db #0x14	; 20
   4E78 28                  386 	.db #0x28	; 40
   4E79 00                  387 	.db #0x00	; 0
   4E7A 00                  388 	.db #0x00	; 0
   4E7B 14                  389 	.db #0x14	; 20
   4E7C 28                  390 	.db #0x28	; 40
   4E7D 00                  391 	.db #0x00	; 0
   4E7E 00                  392 	.db #0x00	; 0
   4E7F 14                  393 	.db #0x14	; 20
   4E80 14                  394 	.db #0x14	; 20
   4E81 3C                  395 	.db #0x3c	; 60
   4E82 3C                  396 	.db #0x3c	; 60
   4E83 28                  397 	.db #0x28	; 40
   4E84                     398 _huddigit_7:
   4E84 14                  399 	.db #0x14	; 20
   4E85 3C                  400 	.db #0x3c	; 60
   4E86 3C                  401 	.db #0x3c	; 60
   4E87 28                  402 	.db #0x28	; 40
   4E88 00                  403 	.db #0x00	; 0
   4E89 00                  404 	.db #0x00	; 0
   4E8A 00                  405 	.db #0x00	; 0
   4E8B 14                  406 	.db #0x14	; 20
   4E8C 00                  407 	.db #0x00	; 0
   4E8D 00                  408 	.db #0x00	; 0
   4E8E 00                  409 	.db #0x00	; 0
   4E8F 14                  410 	.db #0x14	; 20
   4E90 00                  411 	.db #0x00	; 0
   4E91 00                  412 	.db #0x00	; 0
   4E92 00                  413 	.db #0x00	; 0
   4E93 00                  414 	.db #0x00	; 0
   4E94 00                  415 	.db #0x00	; 0
   4E95 00                  416 	.db #0x00	; 0
   4E96 00                  417 	.db #0x00	; 0
   4E97 14                  418 	.db #0x14	; 20
   4E98 00                  419 	.db #0x00	; 0
   4E99 00                  420 	.db #0x00	; 0
   4E9A 00                  421 	.db #0x00	; 0
   4E9B 14                  422 	.db #0x14	; 20
   4E9C 00                  423 	.db #0x00	; 0
   4E9D 00                  424 	.db #0x00	; 0
   4E9E 00                  425 	.db #0x00	; 0
   4E9F 14                  426 	.db #0x14	; 20
   4EA0 00                  427 	.db #0x00	; 0
   4EA1 00                  428 	.db #0x00	; 0
   4EA2 00                  429 	.db #0x00	; 0
   4EA3 00                  430 	.db #0x00	; 0
   4EA4                     431 _huddigit_8:
   4EA4 14                  432 	.db #0x14	; 20
   4EA5 3C                  433 	.db #0x3c	; 60
   4EA6 3C                  434 	.db #0x3c	; 60
   4EA7 28                  435 	.db #0x28	; 40
   4EA8 28                  436 	.db #0x28	; 40
   4EA9 00                  437 	.db #0x00	; 0
   4EAA 00                  438 	.db #0x00	; 0
   4EAB 14                  439 	.db #0x14	; 20
   4EAC 28                  440 	.db #0x28	; 40
   4EAD 00                  441 	.db #0x00	; 0
   4EAE 00                  442 	.db #0x00	; 0
   4EAF 14                  443 	.db #0x14	; 20
   4EB0 14                  444 	.db #0x14	; 20
   4EB1 3C                  445 	.db #0x3c	; 60
   4EB2 3C                  446 	.db #0x3c	; 60
   4EB3 28                  447 	.db #0x28	; 40
   4EB4 28                  448 	.db #0x28	; 40
   4EB5 00                  449 	.db #0x00	; 0
   4EB6 00                  450 	.db #0x00	; 0
   4EB7 14                  451 	.db #0x14	; 20
   4EB8 28                  452 	.db #0x28	; 40
   4EB9 00                  453 	.db #0x00	; 0
   4EBA 00                  454 	.db #0x00	; 0
   4EBB 14                  455 	.db #0x14	; 20
   4EBC 28                  456 	.db #0x28	; 40
   4EBD 00                  457 	.db #0x00	; 0
   4EBE 00                  458 	.db #0x00	; 0
   4EBF 14                  459 	.db #0x14	; 20
   4EC0 14                  460 	.db #0x14	; 20
   4EC1 3C                  461 	.db #0x3c	; 60
   4EC2 3C                  462 	.db #0x3c	; 60
   4EC3 28                  463 	.db #0x28	; 40
   4EC4                     464 _huddigit_9:
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
   4ED4 00                  481 	.db #0x00	; 0
   4ED5 00                  482 	.db #0x00	; 0
   4ED6 00                  483 	.db #0x00	; 0
   4ED7 14                  484 	.db #0x14	; 20
   4ED8 00                  485 	.db #0x00	; 0
   4ED9 00                  486 	.db #0x00	; 0
   4EDA 00                  487 	.db #0x00	; 0
   4EDB 14                  488 	.db #0x14	; 20
   4EDC 00                  489 	.db #0x00	; 0
   4EDD 00                  490 	.db #0x00	; 0
   4EDE 00                  491 	.db #0x00	; 0
   4EDF 14                  492 	.db #0x14	; 20
   4EE0 14                  493 	.db #0x14	; 20
   4EE1 3C                  494 	.db #0x3c	; 60
   4EE2 3C                  495 	.db #0x3c	; 60
   4EE3 28                  496 	.db #0x28	; 40
                            497 ;src/systems/hud.c:95: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            498 ;	---------------------------------
                            499 ; Function hud_draw_digits
                            500 ; ---------------------------------
   4EE4                     501 _hud_draw_digits:
   4EE4 DD E5         [15]  502 	push	ix
   4EE6 DD 21 00 00   [14]  503 	ld	ix,#0
   4EEA DD 39         [15]  504 	add	ix,sp
   4EEC 3B            [ 6]  505 	dec	sp
                            506 ;src/systems/hud.c:101: divisor = 1;
   4EED 01 01 00      [10]  507 	ld	bc, #0x0001
                            508 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   4EF0 1E 01         [ 7]  509 	ld	e, #0x01
   4EF2                     510 00106$:
   4EF2 7B            [ 4]  511 	ld	a, e
   4EF3 DD 96 06      [19]  512 	sub	a, 6 (ix)
   4EF6 30 0B         [12]  513 	jr	NC,00101$
                            514 ;src/systems/hud.c:103: divisor *= 10;
   4EF8 69            [ 4]  515 	ld	l, c
   4EF9 60            [ 4]  516 	ld	h, b
   4EFA 29            [11]  517 	add	hl, hl
   4EFB 29            [11]  518 	add	hl, hl
   4EFC 09            [11]  519 	add	hl, bc
   4EFD 29            [11]  520 	add	hl, hl
   4EFE 4D            [ 4]  521 	ld	c, l
   4EFF 44            [ 4]  522 	ld	b, h
                            523 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   4F00 1C            [ 4]  524 	inc	e
   4F01 18 EF         [12]  525 	jr	00106$
   4F03                     526 00101$:
                            527 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   4F03 DD 36 FF 00   [19]  528 	ld	-1 (ix), #0x00
   4F07                     529 00109$:
   4F07 DD 7E FF      [19]  530 	ld	a, -1 (ix)
   4F0A DD 96 06      [19]  531 	sub	a, 6 (ix)
   4F0D 30 79         [12]  532 	jr	NC,00111$
                            533 ;src/systems/hud.c:107: digit = (u8)(value / divisor);
   4F0F C5            [11]  534 	push	bc
   4F10 C5            [11]  535 	push	bc
   4F11 DD 6E 04      [19]  536 	ld	l,4 (ix)
   4F14 DD 66 05      [19]  537 	ld	h,5 (ix)
   4F17 E5            [11]  538 	push	hl
   4F18 CD FE 5F      [17]  539 	call	__divuint
   4F1B F1            [10]  540 	pop	af
   4F1C F1            [10]  541 	pop	af
   4F1D 5D            [ 4]  542 	ld	e, l
   4F1E C1            [10]  543 	pop	bc
                            544 ;src/systems/hud.c:108: value = (u16)(value % divisor);
   4F1F C5            [11]  545 	push	bc
   4F20 D5            [11]  546 	push	de
   4F21 C5            [11]  547 	push	bc
   4F22 DD 6E 04      [19]  548 	ld	l,4 (ix)
   4F25 DD 66 05      [19]  549 	ld	h,5 (ix)
   4F28 E5            [11]  550 	push	hl
   4F29 CD 89 61      [17]  551 	call	__moduint
   4F2C F1            [10]  552 	pop	af
   4F2D F1            [10]  553 	pop	af
   4F2E D1            [10]  554 	pop	de
   4F2F C1            [10]  555 	pop	bc
   4F30 DD 75 04      [19]  556 	ld	4 (ix), l
   4F33 DD 74 05      [19]  557 	ld	5 (ix), h
                            558 ;src/systems/hud.c:110: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   4F36 DD 7E FF      [19]  559 	ld	a, -1 (ix)
   4F39 87            [ 4]  560 	add	a, a
   4F3A 87            [ 4]  561 	add	a, a
   4F3B 57            [ 4]  562 	ld	d, a
   4F3C DD 7E 07      [19]  563 	ld	a, 7 (ix)
   4F3F 82            [ 4]  564 	add	a, d
   4F40 57            [ 4]  565 	ld	d, a
   4F41 C5            [11]  566 	push	bc
   4F42 D5            [11]  567 	push	de
   4F43 DD 7E 08      [19]  568 	ld	a, 8 (ix)
   4F46 F5            [11]  569 	push	af
   4F47 33            [ 6]  570 	inc	sp
   4F48 D5            [11]  571 	push	de
   4F49 33            [ 6]  572 	inc	sp
   4F4A 21 00 C0      [10]  573 	ld	hl, #0xc000
   4F4D E5            [11]  574 	push	hl
   4F4E CD A7 62      [17]  575 	call	_cpct_getScreenPtr
   4F51 D1            [10]  576 	pop	de
   4F52 C1            [10]  577 	pop	bc
                            578 ;src/systems/hud.c:111: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   4F53 E5            [11]  579 	push	hl
   4F54 C5            [11]  580 	push	bc
   4F55 7B            [ 4]  581 	ld	a, e
   4F56 F5            [11]  582 	push	af
   4F57 33            [ 6]  583 	inc	sp
   4F58 CD 23 4D      [17]  584 	call	_hud_get_number_sprite
   4F5B 33            [ 6]  585 	inc	sp
   4F5C EB            [ 4]  586 	ex	de,hl
   4F5D C1            [10]  587 	pop	bc
   4F5E E1            [10]  588 	pop	hl
   4F5F D5            [11]  589 	push	de
   4F60 FD E1         [14]  590 	pop	iy
   4F62 C5            [11]  591 	push	bc
   4F63 11 04 08      [10]  592 	ld	de, #0x0804
   4F66 D5            [11]  593 	push	de
   4F67 E5            [11]  594 	push	hl
   4F68 FD E5         [15]  595 	push	iy
   4F6A CD D8 60      [17]  596 	call	_cpct_drawSprite
   4F6D C1            [10]  597 	pop	bc
                            598 ;src/systems/hud.c:113: if (divisor > 1) {
   4F6E 3E 01         [ 7]  599 	ld	a, #0x01
   4F70 B9            [ 4]  600 	cp	a, c
   4F71 3E 00         [ 7]  601 	ld	a, #0x00
   4F73 98            [ 4]  602 	sbc	a, b
   4F74 30 0C         [12]  603 	jr	NC,00110$
                            604 ;src/systems/hud.c:114: divisor /= 10;
   4F76 21 0A 00      [10]  605 	ld	hl, #0x000a
   4F79 E5            [11]  606 	push	hl
   4F7A C5            [11]  607 	push	bc
   4F7B CD FE 5F      [17]  608 	call	__divuint
   4F7E F1            [10]  609 	pop	af
   4F7F F1            [10]  610 	pop	af
   4F80 4D            [ 4]  611 	ld	c, l
   4F81 44            [ 4]  612 	ld	b, h
   4F82                     613 00110$:
                            614 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   4F82 DD 34 FF      [23]  615 	inc	-1 (ix)
   4F85 C3 07 4F      [10]  616 	jp	00109$
   4F88                     617 00111$:
   4F88 33            [ 6]  618 	inc	sp
   4F89 DD E1         [14]  619 	pop	ix
   4F8B C9            [10]  620 	ret
                            621 ;src/systems/hud.c:119: void hudinit(void) {
                            622 ;	---------------------------------
                            623 ; Function hudinit
                            624 ; ---------------------------------
   4F8C                     625 _hudinit::
                            626 ;src/systems/hud.c:120: currenthealth = 3;
   4F8C 21 78 63      [10]  627 	ld	hl,#_currenthealth + 0
   4F8F 36 03         [10]  628 	ld	(hl), #0x03
                            629 ;src/systems/hud.c:121: currentscore  = 0;
   4F91 21 00 00      [10]  630 	ld	hl, #0x0000
   4F94 22 79 63      [16]  631 	ld	(_currentscore), hl
                            632 ;src/systems/hud.c:122: currenttime   = 90;
   4F97 21 7B 63      [10]  633 	ld	hl,#_currenttime + 0
   4F9A 36 5A         [10]  634 	ld	(hl), #0x5a
                            635 ;src/systems/hud.c:123: currentlives  = 3;
   4F9C 21 7C 63      [10]  636 	ld	hl,#_currentlives + 0
   4F9F 36 03         [10]  637 	ld	(hl), #0x03
                            638 ;src/systems/hud.c:124: currentweapon = 0;
   4FA1 21 7D 63      [10]  639 	ld	hl,#_currentweapon + 0
   4FA4 36 00         [10]  640 	ld	(hl), #0x00
   4FA6 C9            [10]  641 	ret
                            642 ;src/systems/hud.c:127: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            643 ;	---------------------------------
                            644 ; Function hudupdate
                            645 ; ---------------------------------
   4FA7                     646 _hudupdate::
                            647 ;src/systems/hud.c:128: currenthealth = lives;
   4FA7 21 02 00      [10]  648 	ld	hl, #2+0
   4FAA 39            [11]  649 	add	hl, sp
   4FAB 7E            [ 7]  650 	ld	a, (hl)
   4FAC 32 78 63      [13]  651 	ld	(#_currenthealth + 0),a
                            652 ;src/systems/hud.c:129: currentscore  = score;
   4FAF 21 03 00      [10]  653 	ld	hl, #3+0
   4FB2 39            [11]  654 	add	hl, sp
   4FB3 7E            [ 7]  655 	ld	a, (hl)
   4FB4 32 79 63      [13]  656 	ld	(#_currentscore + 0),a
   4FB7 21 04 00      [10]  657 	ld	hl, #3+1
   4FBA 39            [11]  658 	add	hl, sp
   4FBB 7E            [ 7]  659 	ld	a, (hl)
   4FBC 32 7A 63      [13]  660 	ld	(#_currentscore + 1),a
                            661 ;src/systems/hud.c:130: currenttime   = time;
   4FBF 21 05 00      [10]  662 	ld	hl, #5+0
   4FC2 39            [11]  663 	add	hl, sp
   4FC3 7E            [ 7]  664 	ld	a, (hl)
   4FC4 32 7B 63      [13]  665 	ld	(#_currenttime + 0),a
                            666 ;src/systems/hud.c:131: currentlives  = lives;
   4FC7 21 02 00      [10]  667 	ld	hl, #2+0
   4FCA 39            [11]  668 	add	hl, sp
   4FCB 7E            [ 7]  669 	ld	a, (hl)
   4FCC 32 7C 63      [13]  670 	ld	(#_currentlives + 0),a
                            671 ;src/systems/hud.c:132: currentweapon = weapon;
   4FCF 21 06 00      [10]  672 	ld	hl, #6+0
   4FD2 39            [11]  673 	add	hl, sp
   4FD3 7E            [ 7]  674 	ld	a, (hl)
   4FD4 32 7D 63      [13]  675 	ld	(#_currentweapon + 0),a
   4FD7 C9            [10]  676 	ret
                            677 ;src/systems/hud.c:135: void hudrender(void) {
                            678 ;	---------------------------------
                            679 ; Function hudrender
                            680 ; ---------------------------------
   4FD8                     681 _hudrender::
                            682 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   4FD8 0E 00         [ 7]  683 	ld	c, #0x00
   4FDA                     684 00103$:
   4FDA 21 78 63      [10]  685 	ld	hl, #_currenthealth
                            686 ;src/systems/hud.c:142: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   4FDD 79            [ 4]  687 	ld	a,c
   4FDE BE            [ 7]  688 	cp	a,(hl)
   4FDF 30 24         [12]  689 	jr	NC,00101$
   4FE1 07            [ 4]  690 	rlca
   4FE2 07            [ 4]  691 	rlca
   4FE3 07            [ 4]  692 	rlca
   4FE4 E6 F8         [ 7]  693 	and	a, #0xf8
   4FE6 47            [ 4]  694 	ld	b, a
   4FE7 C5            [11]  695 	push	bc
   4FE8 3E 02         [ 7]  696 	ld	a, #0x02
   4FEA F5            [11]  697 	push	af
   4FEB 33            [ 6]  698 	inc	sp
   4FEC C5            [11]  699 	push	bc
   4FED 33            [ 6]  700 	inc	sp
   4FEE 21 00 C0      [10]  701 	ld	hl, #0xc000
   4FF1 E5            [11]  702 	push	hl
   4FF2 CD A7 62      [17]  703 	call	_cpct_getScreenPtr
   4FF5 11 04 08      [10]  704 	ld	de, #0x0804
   4FF8 D5            [11]  705 	push	de
   4FF9 E5            [11]  706 	push	hl
   4FFA 21 09 54      [10]  707 	ld	hl, #_hudhealthbar_data
   4FFD E5            [11]  708 	push	hl
   4FFE CD D8 60      [17]  709 	call	_cpct_drawSprite
   5001 C1            [10]  710 	pop	bc
                            711 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   5002 0C            [ 4]  712 	inc	c
   5003 18 D5         [12]  713 	jr	00103$
   5005                     714 00101$:
                            715 ;src/systems/hud.c:146: scoretemp = currentscore;
   5005 2A 79 63      [16]  716 	ld	hl, (_currentscore)
                            717 ;src/systems/hud.c:147: hud_draw_digits(scoretemp, 4, 24, 2);
   5008 01 18 02      [10]  718 	ld	bc, #0x0218
   500B C5            [11]  719 	push	bc
   500C 3E 04         [ 7]  720 	ld	a, #0x04
   500E F5            [11]  721 	push	af
   500F 33            [ 6]  722 	inc	sp
   5010 E5            [11]  723 	push	hl
   5011 CD E4 4E      [17]  724 	call	_hud_draw_digits
   5014 F1            [10]  725 	pop	af
   5015 F1            [10]  726 	pop	af
   5016 33            [ 6]  727 	inc	sp
                            728 ;src/systems/hud.c:149: timetemp = currenttime;
   5017 21 7B 63      [10]  729 	ld	hl,#_currenttime + 0
   501A 4E            [ 7]  730 	ld	c, (hl)
                            731 ;src/systems/hud.c:150: hud_draw_digits((u16)timetemp, 3, 56, 2);
   501B 06 00         [ 7]  732 	ld	b, #0x00
   501D 21 38 02      [10]  733 	ld	hl, #0x0238
   5020 E5            [11]  734 	push	hl
   5021 3E 03         [ 7]  735 	ld	a, #0x03
   5023 F5            [11]  736 	push	af
   5024 33            [ 6]  737 	inc	sp
   5025 C5            [11]  738 	push	bc
   5026 CD E4 4E      [17]  739 	call	_hud_draw_digits
   5029 F1            [10]  740 	pop	af
                            741 ;src/systems/hud.c:152: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   502A 33            [ 6]  742 	inc	sp
   502B 21 02 B4      [10]  743 	ld	hl,#0xb402
   502E E3            [19]  744 	ex	(sp),hl
   502F 21 00 C0      [10]  745 	ld	hl, #0xc000
   5032 E5            [11]  746 	push	hl
   5033 CD A7 62      [17]  747 	call	_cpct_getScreenPtr
                            748 ;src/systems/hud.c:153: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   5036 01 84 4D      [10]  749 	ld	bc, #_hudlives+0
   5039 11 04 08      [10]  750 	ld	de, #0x0804
   503C D5            [11]  751 	push	de
   503D E5            [11]  752 	push	hl
   503E C5            [11]  753 	push	bc
   503F CD D8 60      [17]  754 	call	_cpct_drawSprite
                            755 ;src/systems/hud.c:155: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   5042 21 0C B4      [10]  756 	ld	hl, #0xb40c
   5045 E5            [11]  757 	push	hl
   5046 21 00 C0      [10]  758 	ld	hl, #0xc000
   5049 E5            [11]  759 	push	hl
   504A CD A7 62      [17]  760 	call	_cpct_getScreenPtr
                            761 ;src/systems/hud.c:156: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   504D E5            [11]  762 	push	hl
   504E 3E 0A         [ 7]  763 	ld	a, #0x0a
   5050 F5            [11]  764 	push	af
   5051 33            [ 6]  765 	inc	sp
   5052 3A 7C 63      [13]  766 	ld	a, (_currentlives)
   5055 F5            [11]  767 	push	af
   5056 33            [ 6]  768 	inc	sp
   5057 CD 7D 61      [17]  769 	call	__moduchar
   505A F1            [10]  770 	pop	af
   505B 55            [ 4]  771 	ld	d, l
   505C D5            [11]  772 	push	de
   505D 33            [ 6]  773 	inc	sp
   505E CD 23 4D      [17]  774 	call	_hud_get_number_sprite
   5061 33            [ 6]  775 	inc	sp
   5062 C1            [10]  776 	pop	bc
   5063 11 04 08      [10]  777 	ld	de, #0x0804
   5066 D5            [11]  778 	push	de
   5067 C5            [11]  779 	push	bc
   5068 E5            [11]  780 	push	hl
   5069 CD D8 60      [17]  781 	call	_cpct_drawSprite
                            782 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   506C 21 46 B4      [10]  783 	ld	hl, #0xb446
   506F E5            [11]  784 	push	hl
   5070 21 00 C0      [10]  785 	ld	hl, #0xc000
   5073 E5            [11]  786 	push	hl
   5074 CD A7 62      [17]  787 	call	_cpct_getScreenPtr
                            788 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   5077 E5            [11]  789 	push	hl
   5078 3E 0A         [ 7]  790 	ld	a, #0x0a
   507A F5            [11]  791 	push	af
   507B 33            [ 6]  792 	inc	sp
   507C 3A 7D 63      [13]  793 	ld	a, (_currentweapon)
   507F F5            [11]  794 	push	af
   5080 33            [ 6]  795 	inc	sp
   5081 CD 7D 61      [17]  796 	call	__moduchar
   5084 F1            [10]  797 	pop	af
   5085 55            [ 4]  798 	ld	d, l
   5086 D5            [11]  799 	push	de
   5087 33            [ 6]  800 	inc	sp
   5088 CD 23 4D      [17]  801 	call	_hud_get_number_sprite
   508B 33            [ 6]  802 	inc	sp
   508C C1            [10]  803 	pop	bc
   508D 11 04 08      [10]  804 	ld	de, #0x0804
   5090 D5            [11]  805 	push	de
   5091 C5            [11]  806 	push	bc
   5092 E5            [11]  807 	push	hl
   5093 CD D8 60      [17]  808 	call	_cpct_drawSprite
   5096 C9            [10]  809 	ret
                            810 	.area _CODE
                            811 	.area _INITIALIZER
                            812 	.area _CABS (ABS)
