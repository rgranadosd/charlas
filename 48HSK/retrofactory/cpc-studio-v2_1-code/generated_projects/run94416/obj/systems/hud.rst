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
   650A                      23 _currenthealth:
   650A                      24 	.ds 1
   650B                      25 _currentscore:
   650B                      26 	.ds 2
   650D                      27 _currenttime:
   650D                      28 	.ds 1
   650E                      29 _currentlives:
   650E                      30 	.ds 1
   650F                      31 _currentweapon:
   650F                      32 	.ds 1
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
   4E68                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:81: switch (digit % 10) {
   4E68 3E 0A         [ 7]   63 	ld	a, #0x0a
   4E6A F5            [11]   64 	push	af
   4E6B 33            [ 6]   65 	inc	sp
   4E6C 21 03 00      [10]   66 	ld	hl, #3+0
   4E6F 39            [11]   67 	add	hl, sp
   4E70 7E            [ 7]   68 	ld	a, (hl)
   4E71 F5            [11]   69 	push	af
   4E72 33            [ 6]   70 	inc	sp
   4E73 CD 0F 63      [17]   71 	call	__moduchar
   4E76 F1            [10]   72 	pop	af
   4E77 4D            [ 4]   73 	ld	c, l
   4E78 3E 08         [ 7]   74 	ld	a, #0x08
   4E7A 91            [ 4]   75 	sub	a, c
   4E7B 38 48         [12]   76 	jr	C,00110$
   4E7D 06 00         [ 7]   77 	ld	b, #0x00
   4E7F 21 86 4E      [10]   78 	ld	hl, #00118$
   4E82 09            [11]   79 	add	hl, bc
   4E83 09            [11]   80 	add	hl, bc
   4E84 09            [11]   81 	add	hl, bc
   4E85 E9            [ 4]   82 	jp	(hl)
   4E86                      83 00118$:
   4E86 C3 A1 4E      [10]   84 	jp	00101$
   4E89 C3 A5 4E      [10]   85 	jp	00102$
   4E8C C3 A9 4E      [10]   86 	jp	00103$
   4E8F C3 AD 4E      [10]   87 	jp	00104$
   4E92 C3 B1 4E      [10]   88 	jp	00105$
   4E95 C3 B5 4E      [10]   89 	jp	00106$
   4E98 C3 B9 4E      [10]   90 	jp	00107$
   4E9B C3 BD 4E      [10]   91 	jp	00108$
   4E9E C3 C1 4E      [10]   92 	jp	00109$
                             93 ;src/systems/hud.c:82: case 0: return huddigit_0;
   4EA1                      94 00101$:
   4EA1 21 E9 4E      [10]   95 	ld	hl, #_huddigit_0
   4EA4 C9            [10]   96 	ret
                             97 ;src/systems/hud.c:83: case 1: return huddigit_1;
   4EA5                      98 00102$:
   4EA5 21 09 4F      [10]   99 	ld	hl, #_huddigit_1
   4EA8 C9            [10]  100 	ret
                            101 ;src/systems/hud.c:84: case 2: return huddigit_2;
   4EA9                     102 00103$:
   4EA9 21 29 4F      [10]  103 	ld	hl, #_huddigit_2
   4EAC C9            [10]  104 	ret
                            105 ;src/systems/hud.c:85: case 3: return huddigit_3;
   4EAD                     106 00104$:
   4EAD 21 49 4F      [10]  107 	ld	hl, #_huddigit_3
   4EB0 C9            [10]  108 	ret
                            109 ;src/systems/hud.c:86: case 4: return huddigit_4;
   4EB1                     110 00105$:
   4EB1 21 69 4F      [10]  111 	ld	hl, #_huddigit_4
   4EB4 C9            [10]  112 	ret
                            113 ;src/systems/hud.c:87: case 5: return huddigit_5;
   4EB5                     114 00106$:
   4EB5 21 89 4F      [10]  115 	ld	hl, #_huddigit_5
   4EB8 C9            [10]  116 	ret
                            117 ;src/systems/hud.c:88: case 6: return huddigit_6;
   4EB9                     118 00107$:
   4EB9 21 A9 4F      [10]  119 	ld	hl, #_huddigit_6
   4EBC C9            [10]  120 	ret
                            121 ;src/systems/hud.c:89: case 7: return huddigit_7;
   4EBD                     122 00108$:
   4EBD 21 C9 4F      [10]  123 	ld	hl, #_huddigit_7
   4EC0 C9            [10]  124 	ret
                            125 ;src/systems/hud.c:90: case 8: return huddigit_8;
   4EC1                     126 00109$:
   4EC1 21 E9 4F      [10]  127 	ld	hl, #_huddigit_8
   4EC4 C9            [10]  128 	ret
                            129 ;src/systems/hud.c:91: default: return huddigit_9;
   4EC5                     130 00110$:
   4EC5 21 09 50      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:92: }
   4EC8 C9            [10]  133 	ret
   4EC9                     134 _hudlives:
   4EC9 30                  135 	.db #0x30	; 48	'0'
   4ECA 30                  136 	.db #0x30	; 48	'0'
   4ECB 30                  137 	.db #0x30	; 48	'0'
   4ECC 30                  138 	.db #0x30	; 48	'0'
   4ECD 20                  139 	.db #0x20	; 32
   4ECE 10                  140 	.db #0x10	; 16
   4ECF 00                  141 	.db #0x00	; 0
   4ED0 10                  142 	.db #0x10	; 16
   4ED1 20                  143 	.db #0x20	; 32
   4ED2 10                  144 	.db #0x10	; 16
   4ED3 00                  145 	.db #0x00	; 0
   4ED4 10                  146 	.db #0x10	; 16
   4ED5 20                  147 	.db #0x20	; 32
   4ED6 10                  148 	.db #0x10	; 16
   4ED7 00                  149 	.db #0x00	; 0
   4ED8 10                  150 	.db #0x10	; 16
   4ED9 30                  151 	.db #0x30	; 48	'0'
   4EDA 30                  152 	.db #0x30	; 48	'0'
   4EDB 30                  153 	.db #0x30	; 48	'0'
   4EDC 30                  154 	.db #0x30	; 48	'0'
   4EDD 20                  155 	.db #0x20	; 32
   4EDE 10                  156 	.db #0x10	; 16
   4EDF 00                  157 	.db #0x00	; 0
   4EE0 10                  158 	.db #0x10	; 16
   4EE1 20                  159 	.db #0x20	; 32
   4EE2 10                  160 	.db #0x10	; 16
   4EE3 00                  161 	.db #0x00	; 0
   4EE4 10                  162 	.db #0x10	; 16
   4EE5 30                  163 	.db #0x30	; 48	'0'
   4EE6 30                  164 	.db #0x30	; 48	'0'
   4EE7 30                  165 	.db #0x30	; 48	'0'
   4EE8 30                  166 	.db #0x30	; 48	'0'
   4EE9                     167 _huddigit_0:
   4EE9 14                  168 	.db #0x14	; 20
   4EEA 3C                  169 	.db #0x3c	; 60
   4EEB 3C                  170 	.db #0x3c	; 60
   4EEC 28                  171 	.db #0x28	; 40
   4EED 28                  172 	.db #0x28	; 40
   4EEE 00                  173 	.db #0x00	; 0
   4EEF 00                  174 	.db #0x00	; 0
   4EF0 14                  175 	.db #0x14	; 20
   4EF1 28                  176 	.db #0x28	; 40
   4EF2 00                  177 	.db #0x00	; 0
   4EF3 00                  178 	.db #0x00	; 0
   4EF4 14                  179 	.db #0x14	; 20
   4EF5 00                  180 	.db #0x00	; 0
   4EF6 00                  181 	.db #0x00	; 0
   4EF7 00                  182 	.db #0x00	; 0
   4EF8 00                  183 	.db #0x00	; 0
   4EF9 28                  184 	.db #0x28	; 40
   4EFA 00                  185 	.db #0x00	; 0
   4EFB 00                  186 	.db #0x00	; 0
   4EFC 14                  187 	.db #0x14	; 20
   4EFD 28                  188 	.db #0x28	; 40
   4EFE 00                  189 	.db #0x00	; 0
   4EFF 00                  190 	.db #0x00	; 0
   4F00 14                  191 	.db #0x14	; 20
   4F01 28                  192 	.db #0x28	; 40
   4F02 00                  193 	.db #0x00	; 0
   4F03 00                  194 	.db #0x00	; 0
   4F04 14                  195 	.db #0x14	; 20
   4F05 14                  196 	.db #0x14	; 20
   4F06 3C                  197 	.db #0x3c	; 60
   4F07 3C                  198 	.db #0x3c	; 60
   4F08 28                  199 	.db #0x28	; 40
   4F09                     200 _huddigit_1:
   4F09 00                  201 	.db #0x00	; 0
   4F0A 00                  202 	.db #0x00	; 0
   4F0B 00                  203 	.db #0x00	; 0
   4F0C 00                  204 	.db #0x00	; 0
   4F0D 00                  205 	.db #0x00	; 0
   4F0E 00                  206 	.db #0x00	; 0
   4F0F 00                  207 	.db #0x00	; 0
   4F10 14                  208 	.db #0x14	; 20
   4F11 00                  209 	.db #0x00	; 0
   4F12 00                  210 	.db #0x00	; 0
   4F13 00                  211 	.db #0x00	; 0
   4F14 14                  212 	.db #0x14	; 20
   4F15 00                  213 	.db #0x00	; 0
   4F16 00                  214 	.db #0x00	; 0
   4F17 00                  215 	.db #0x00	; 0
   4F18 00                  216 	.db #0x00	; 0
   4F19 00                  217 	.db #0x00	; 0
   4F1A 00                  218 	.db #0x00	; 0
   4F1B 00                  219 	.db #0x00	; 0
   4F1C 14                  220 	.db #0x14	; 20
   4F1D 00                  221 	.db #0x00	; 0
   4F1E 00                  222 	.db #0x00	; 0
   4F1F 00                  223 	.db #0x00	; 0
   4F20 14                  224 	.db #0x14	; 20
   4F21 00                  225 	.db #0x00	; 0
   4F22 00                  226 	.db #0x00	; 0
   4F23 00                  227 	.db #0x00	; 0
   4F24 14                  228 	.db #0x14	; 20
   4F25 00                  229 	.db #0x00	; 0
   4F26 00                  230 	.db #0x00	; 0
   4F27 00                  231 	.db #0x00	; 0
   4F28 00                  232 	.db #0x00	; 0
   4F29                     233 _huddigit_2:
   4F29 14                  234 	.db #0x14	; 20
   4F2A 3C                  235 	.db #0x3c	; 60
   4F2B 3C                  236 	.db #0x3c	; 60
   4F2C 28                  237 	.db #0x28	; 40
   4F2D 00                  238 	.db #0x00	; 0
   4F2E 00                  239 	.db #0x00	; 0
   4F2F 00                  240 	.db #0x00	; 0
   4F30 14                  241 	.db #0x14	; 20
   4F31 00                  242 	.db #0x00	; 0
   4F32 00                  243 	.db #0x00	; 0
   4F33 00                  244 	.db #0x00	; 0
   4F34 14                  245 	.db #0x14	; 20
   4F35 14                  246 	.db #0x14	; 20
   4F36 3C                  247 	.db #0x3c	; 60
   4F37 3C                  248 	.db #0x3c	; 60
   4F38 28                  249 	.db #0x28	; 40
   4F39 28                  250 	.db #0x28	; 40
   4F3A 00                  251 	.db #0x00	; 0
   4F3B 00                  252 	.db #0x00	; 0
   4F3C 00                  253 	.db #0x00	; 0
   4F3D 28                  254 	.db #0x28	; 40
   4F3E 00                  255 	.db #0x00	; 0
   4F3F 00                  256 	.db #0x00	; 0
   4F40 00                  257 	.db #0x00	; 0
   4F41 28                  258 	.db #0x28	; 40
   4F42 00                  259 	.db #0x00	; 0
   4F43 00                  260 	.db #0x00	; 0
   4F44 00                  261 	.db #0x00	; 0
   4F45 14                  262 	.db #0x14	; 20
   4F46 3C                  263 	.db #0x3c	; 60
   4F47 3C                  264 	.db #0x3c	; 60
   4F48 28                  265 	.db #0x28	; 40
   4F49                     266 _huddigit_3:
   4F49 14                  267 	.db #0x14	; 20
   4F4A 3C                  268 	.db #0x3c	; 60
   4F4B 3C                  269 	.db #0x3c	; 60
   4F4C 28                  270 	.db #0x28	; 40
   4F4D 00                  271 	.db #0x00	; 0
   4F4E 00                  272 	.db #0x00	; 0
   4F4F 00                  273 	.db #0x00	; 0
   4F50 14                  274 	.db #0x14	; 20
   4F51 00                  275 	.db #0x00	; 0
   4F52 00                  276 	.db #0x00	; 0
   4F53 00                  277 	.db #0x00	; 0
   4F54 14                  278 	.db #0x14	; 20
   4F55 14                  279 	.db #0x14	; 20
   4F56 3C                  280 	.db #0x3c	; 60
   4F57 3C                  281 	.db #0x3c	; 60
   4F58 28                  282 	.db #0x28	; 40
   4F59 00                  283 	.db #0x00	; 0
   4F5A 00                  284 	.db #0x00	; 0
   4F5B 00                  285 	.db #0x00	; 0
   4F5C 14                  286 	.db #0x14	; 20
   4F5D 00                  287 	.db #0x00	; 0
   4F5E 00                  288 	.db #0x00	; 0
   4F5F 00                  289 	.db #0x00	; 0
   4F60 14                  290 	.db #0x14	; 20
   4F61 00                  291 	.db #0x00	; 0
   4F62 00                  292 	.db #0x00	; 0
   4F63 00                  293 	.db #0x00	; 0
   4F64 14                  294 	.db #0x14	; 20
   4F65 14                  295 	.db #0x14	; 20
   4F66 3C                  296 	.db #0x3c	; 60
   4F67 3C                  297 	.db #0x3c	; 60
   4F68 28                  298 	.db #0x28	; 40
   4F69                     299 _huddigit_4:
   4F69 00                  300 	.db #0x00	; 0
   4F6A 00                  301 	.db #0x00	; 0
   4F6B 00                  302 	.db #0x00	; 0
   4F6C 00                  303 	.db #0x00	; 0
   4F6D 28                  304 	.db #0x28	; 40
   4F6E 00                  305 	.db #0x00	; 0
   4F6F 00                  306 	.db #0x00	; 0
   4F70 14                  307 	.db #0x14	; 20
   4F71 28                  308 	.db #0x28	; 40
   4F72 00                  309 	.db #0x00	; 0
   4F73 00                  310 	.db #0x00	; 0
   4F74 14                  311 	.db #0x14	; 20
   4F75 14                  312 	.db #0x14	; 20
   4F76 3C                  313 	.db #0x3c	; 60
   4F77 3C                  314 	.db #0x3c	; 60
   4F78 28                  315 	.db #0x28	; 40
   4F79 00                  316 	.db #0x00	; 0
   4F7A 00                  317 	.db #0x00	; 0
   4F7B 00                  318 	.db #0x00	; 0
   4F7C 14                  319 	.db #0x14	; 20
   4F7D 00                  320 	.db #0x00	; 0
   4F7E 00                  321 	.db #0x00	; 0
   4F7F 00                  322 	.db #0x00	; 0
   4F80 14                  323 	.db #0x14	; 20
   4F81 00                  324 	.db #0x00	; 0
   4F82 00                  325 	.db #0x00	; 0
   4F83 00                  326 	.db #0x00	; 0
   4F84 14                  327 	.db #0x14	; 20
   4F85 00                  328 	.db #0x00	; 0
   4F86 00                  329 	.db #0x00	; 0
   4F87 00                  330 	.db #0x00	; 0
   4F88 00                  331 	.db #0x00	; 0
   4F89                     332 _huddigit_5:
   4F89 14                  333 	.db #0x14	; 20
   4F8A 3C                  334 	.db #0x3c	; 60
   4F8B 3C                  335 	.db #0x3c	; 60
   4F8C 28                  336 	.db #0x28	; 40
   4F8D 28                  337 	.db #0x28	; 40
   4F8E 00                  338 	.db #0x00	; 0
   4F8F 00                  339 	.db #0x00	; 0
   4F90 00                  340 	.db #0x00	; 0
   4F91 28                  341 	.db #0x28	; 40
   4F92 00                  342 	.db #0x00	; 0
   4F93 00                  343 	.db #0x00	; 0
   4F94 00                  344 	.db #0x00	; 0
   4F95 14                  345 	.db #0x14	; 20
   4F96 3C                  346 	.db #0x3c	; 60
   4F97 3C                  347 	.db #0x3c	; 60
   4F98 28                  348 	.db #0x28	; 40
   4F99 00                  349 	.db #0x00	; 0
   4F9A 00                  350 	.db #0x00	; 0
   4F9B 00                  351 	.db #0x00	; 0
   4F9C 14                  352 	.db #0x14	; 20
   4F9D 00                  353 	.db #0x00	; 0
   4F9E 00                  354 	.db #0x00	; 0
   4F9F 00                  355 	.db #0x00	; 0
   4FA0 14                  356 	.db #0x14	; 20
   4FA1 00                  357 	.db #0x00	; 0
   4FA2 00                  358 	.db #0x00	; 0
   4FA3 00                  359 	.db #0x00	; 0
   4FA4 14                  360 	.db #0x14	; 20
   4FA5 14                  361 	.db #0x14	; 20
   4FA6 3C                  362 	.db #0x3c	; 60
   4FA7 3C                  363 	.db #0x3c	; 60
   4FA8 28                  364 	.db #0x28	; 40
   4FA9                     365 _huddigit_6:
   4FA9 14                  366 	.db #0x14	; 20
   4FAA 3C                  367 	.db #0x3c	; 60
   4FAB 3C                  368 	.db #0x3c	; 60
   4FAC 28                  369 	.db #0x28	; 40
   4FAD 28                  370 	.db #0x28	; 40
   4FAE 00                  371 	.db #0x00	; 0
   4FAF 00                  372 	.db #0x00	; 0
   4FB0 00                  373 	.db #0x00	; 0
   4FB1 28                  374 	.db #0x28	; 40
   4FB2 00                  375 	.db #0x00	; 0
   4FB3 00                  376 	.db #0x00	; 0
   4FB4 00                  377 	.db #0x00	; 0
   4FB5 14                  378 	.db #0x14	; 20
   4FB6 3C                  379 	.db #0x3c	; 60
   4FB7 3C                  380 	.db #0x3c	; 60
   4FB8 28                  381 	.db #0x28	; 40
   4FB9 28                  382 	.db #0x28	; 40
   4FBA 00                  383 	.db #0x00	; 0
   4FBB 00                  384 	.db #0x00	; 0
   4FBC 14                  385 	.db #0x14	; 20
   4FBD 28                  386 	.db #0x28	; 40
   4FBE 00                  387 	.db #0x00	; 0
   4FBF 00                  388 	.db #0x00	; 0
   4FC0 14                  389 	.db #0x14	; 20
   4FC1 28                  390 	.db #0x28	; 40
   4FC2 00                  391 	.db #0x00	; 0
   4FC3 00                  392 	.db #0x00	; 0
   4FC4 14                  393 	.db #0x14	; 20
   4FC5 14                  394 	.db #0x14	; 20
   4FC6 3C                  395 	.db #0x3c	; 60
   4FC7 3C                  396 	.db #0x3c	; 60
   4FC8 28                  397 	.db #0x28	; 40
   4FC9                     398 _huddigit_7:
   4FC9 14                  399 	.db #0x14	; 20
   4FCA 3C                  400 	.db #0x3c	; 60
   4FCB 3C                  401 	.db #0x3c	; 60
   4FCC 28                  402 	.db #0x28	; 40
   4FCD 00                  403 	.db #0x00	; 0
   4FCE 00                  404 	.db #0x00	; 0
   4FCF 00                  405 	.db #0x00	; 0
   4FD0 14                  406 	.db #0x14	; 20
   4FD1 00                  407 	.db #0x00	; 0
   4FD2 00                  408 	.db #0x00	; 0
   4FD3 00                  409 	.db #0x00	; 0
   4FD4 14                  410 	.db #0x14	; 20
   4FD5 00                  411 	.db #0x00	; 0
   4FD6 00                  412 	.db #0x00	; 0
   4FD7 00                  413 	.db #0x00	; 0
   4FD8 00                  414 	.db #0x00	; 0
   4FD9 00                  415 	.db #0x00	; 0
   4FDA 00                  416 	.db #0x00	; 0
   4FDB 00                  417 	.db #0x00	; 0
   4FDC 14                  418 	.db #0x14	; 20
   4FDD 00                  419 	.db #0x00	; 0
   4FDE 00                  420 	.db #0x00	; 0
   4FDF 00                  421 	.db #0x00	; 0
   4FE0 14                  422 	.db #0x14	; 20
   4FE1 00                  423 	.db #0x00	; 0
   4FE2 00                  424 	.db #0x00	; 0
   4FE3 00                  425 	.db #0x00	; 0
   4FE4 14                  426 	.db #0x14	; 20
   4FE5 00                  427 	.db #0x00	; 0
   4FE6 00                  428 	.db #0x00	; 0
   4FE7 00                  429 	.db #0x00	; 0
   4FE8 00                  430 	.db #0x00	; 0
   4FE9                     431 _huddigit_8:
   4FE9 14                  432 	.db #0x14	; 20
   4FEA 3C                  433 	.db #0x3c	; 60
   4FEB 3C                  434 	.db #0x3c	; 60
   4FEC 28                  435 	.db #0x28	; 40
   4FED 28                  436 	.db #0x28	; 40
   4FEE 00                  437 	.db #0x00	; 0
   4FEF 00                  438 	.db #0x00	; 0
   4FF0 14                  439 	.db #0x14	; 20
   4FF1 28                  440 	.db #0x28	; 40
   4FF2 00                  441 	.db #0x00	; 0
   4FF3 00                  442 	.db #0x00	; 0
   4FF4 14                  443 	.db #0x14	; 20
   4FF5 14                  444 	.db #0x14	; 20
   4FF6 3C                  445 	.db #0x3c	; 60
   4FF7 3C                  446 	.db #0x3c	; 60
   4FF8 28                  447 	.db #0x28	; 40
   4FF9 28                  448 	.db #0x28	; 40
   4FFA 00                  449 	.db #0x00	; 0
   4FFB 00                  450 	.db #0x00	; 0
   4FFC 14                  451 	.db #0x14	; 20
   4FFD 28                  452 	.db #0x28	; 40
   4FFE 00                  453 	.db #0x00	; 0
   4FFF 00                  454 	.db #0x00	; 0
   5000 14                  455 	.db #0x14	; 20
   5001 28                  456 	.db #0x28	; 40
   5002 00                  457 	.db #0x00	; 0
   5003 00                  458 	.db #0x00	; 0
   5004 14                  459 	.db #0x14	; 20
   5005 14                  460 	.db #0x14	; 20
   5006 3C                  461 	.db #0x3c	; 60
   5007 3C                  462 	.db #0x3c	; 60
   5008 28                  463 	.db #0x28	; 40
   5009                     464 _huddigit_9:
   5009 14                  465 	.db #0x14	; 20
   500A 3C                  466 	.db #0x3c	; 60
   500B 3C                  467 	.db #0x3c	; 60
   500C 28                  468 	.db #0x28	; 40
   500D 28                  469 	.db #0x28	; 40
   500E 00                  470 	.db #0x00	; 0
   500F 00                  471 	.db #0x00	; 0
   5010 14                  472 	.db #0x14	; 20
   5011 28                  473 	.db #0x28	; 40
   5012 00                  474 	.db #0x00	; 0
   5013 00                  475 	.db #0x00	; 0
   5014 14                  476 	.db #0x14	; 20
   5015 14                  477 	.db #0x14	; 20
   5016 3C                  478 	.db #0x3c	; 60
   5017 3C                  479 	.db #0x3c	; 60
   5018 28                  480 	.db #0x28	; 40
   5019 00                  481 	.db #0x00	; 0
   501A 00                  482 	.db #0x00	; 0
   501B 00                  483 	.db #0x00	; 0
   501C 14                  484 	.db #0x14	; 20
   501D 00                  485 	.db #0x00	; 0
   501E 00                  486 	.db #0x00	; 0
   501F 00                  487 	.db #0x00	; 0
   5020 14                  488 	.db #0x14	; 20
   5021 00                  489 	.db #0x00	; 0
   5022 00                  490 	.db #0x00	; 0
   5023 00                  491 	.db #0x00	; 0
   5024 14                  492 	.db #0x14	; 20
   5025 14                  493 	.db #0x14	; 20
   5026 3C                  494 	.db #0x3c	; 60
   5027 3C                  495 	.db #0x3c	; 60
   5028 28                  496 	.db #0x28	; 40
                            497 ;src/systems/hud.c:95: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            498 ;	---------------------------------
                            499 ; Function hud_draw_digits
                            500 ; ---------------------------------
   5029                     501 _hud_draw_digits:
   5029 DD E5         [15]  502 	push	ix
   502B DD 21 00 00   [14]  503 	ld	ix,#0
   502F DD 39         [15]  504 	add	ix,sp
   5031 3B            [ 6]  505 	dec	sp
                            506 ;src/systems/hud.c:101: divisor = 1;
   5032 01 01 00      [10]  507 	ld	bc, #0x0001
                            508 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   5035 1E 01         [ 7]  509 	ld	e, #0x01
   5037                     510 00106$:
   5037 7B            [ 4]  511 	ld	a, e
   5038 DD 96 06      [19]  512 	sub	a, 6 (ix)
   503B 30 0B         [12]  513 	jr	NC,00101$
                            514 ;src/systems/hud.c:103: divisor *= 10;
   503D 69            [ 4]  515 	ld	l, c
   503E 60            [ 4]  516 	ld	h, b
   503F 29            [11]  517 	add	hl, hl
   5040 29            [11]  518 	add	hl, hl
   5041 09            [11]  519 	add	hl, bc
   5042 29            [11]  520 	add	hl, hl
   5043 4D            [ 4]  521 	ld	c, l
   5044 44            [ 4]  522 	ld	b, h
                            523 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   5045 1C            [ 4]  524 	inc	e
   5046 18 EF         [12]  525 	jr	00106$
   5048                     526 00101$:
                            527 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   5048 DD 36 FF 00   [19]  528 	ld	-1 (ix), #0x00
   504C                     529 00109$:
   504C DD 7E FF      [19]  530 	ld	a, -1 (ix)
   504F DD 96 06      [19]  531 	sub	a, 6 (ix)
   5052 30 79         [12]  532 	jr	NC,00111$
                            533 ;src/systems/hud.c:107: digit = (u8)(value / divisor);
   5054 C5            [11]  534 	push	bc
   5055 C5            [11]  535 	push	bc
   5056 DD 6E 04      [19]  536 	ld	l,4 (ix)
   5059 DD 66 05      [19]  537 	ld	h,5 (ix)
   505C E5            [11]  538 	push	hl
   505D CD 90 61      [17]  539 	call	__divuint
   5060 F1            [10]  540 	pop	af
   5061 F1            [10]  541 	pop	af
   5062 5D            [ 4]  542 	ld	e, l
   5063 C1            [10]  543 	pop	bc
                            544 ;src/systems/hud.c:108: value = (u16)(value % divisor);
   5064 C5            [11]  545 	push	bc
   5065 D5            [11]  546 	push	de
   5066 C5            [11]  547 	push	bc
   5067 DD 6E 04      [19]  548 	ld	l,4 (ix)
   506A DD 66 05      [19]  549 	ld	h,5 (ix)
   506D E5            [11]  550 	push	hl
   506E CD 1B 63      [17]  551 	call	__moduint
   5071 F1            [10]  552 	pop	af
   5072 F1            [10]  553 	pop	af
   5073 D1            [10]  554 	pop	de
   5074 C1            [10]  555 	pop	bc
   5075 DD 75 04      [19]  556 	ld	4 (ix), l
   5078 DD 74 05      [19]  557 	ld	5 (ix), h
                            558 ;src/systems/hud.c:110: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   507B DD 7E FF      [19]  559 	ld	a, -1 (ix)
   507E 87            [ 4]  560 	add	a, a
   507F 87            [ 4]  561 	add	a, a
   5080 57            [ 4]  562 	ld	d, a
   5081 DD 7E 07      [19]  563 	ld	a, 7 (ix)
   5084 82            [ 4]  564 	add	a, d
   5085 57            [ 4]  565 	ld	d, a
   5086 C5            [11]  566 	push	bc
   5087 D5            [11]  567 	push	de
   5088 DD 7E 08      [19]  568 	ld	a, 8 (ix)
   508B F5            [11]  569 	push	af
   508C 33            [ 6]  570 	inc	sp
   508D D5            [11]  571 	push	de
   508E 33            [ 6]  572 	inc	sp
   508F 21 00 C0      [10]  573 	ld	hl, #0xc000
   5092 E5            [11]  574 	push	hl
   5093 CD 39 64      [17]  575 	call	_cpct_getScreenPtr
   5096 D1            [10]  576 	pop	de
   5097 C1            [10]  577 	pop	bc
                            578 ;src/systems/hud.c:111: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   5098 E5            [11]  579 	push	hl
   5099 C5            [11]  580 	push	bc
   509A 7B            [ 4]  581 	ld	a, e
   509B F5            [11]  582 	push	af
   509C 33            [ 6]  583 	inc	sp
   509D CD 68 4E      [17]  584 	call	_hud_get_number_sprite
   50A0 33            [ 6]  585 	inc	sp
   50A1 EB            [ 4]  586 	ex	de,hl
   50A2 C1            [10]  587 	pop	bc
   50A3 E1            [10]  588 	pop	hl
   50A4 D5            [11]  589 	push	de
   50A5 FD E1         [14]  590 	pop	iy
   50A7 C5            [11]  591 	push	bc
   50A8 11 04 08      [10]  592 	ld	de, #0x0804
   50AB D5            [11]  593 	push	de
   50AC E5            [11]  594 	push	hl
   50AD FD E5         [15]  595 	push	iy
   50AF CD 6A 62      [17]  596 	call	_cpct_drawSprite
   50B2 C1            [10]  597 	pop	bc
                            598 ;src/systems/hud.c:113: if (divisor > 1) {
   50B3 3E 01         [ 7]  599 	ld	a, #0x01
   50B5 B9            [ 4]  600 	cp	a, c
   50B6 3E 00         [ 7]  601 	ld	a, #0x00
   50B8 98            [ 4]  602 	sbc	a, b
   50B9 30 0C         [12]  603 	jr	NC,00110$
                            604 ;src/systems/hud.c:114: divisor /= 10;
   50BB 21 0A 00      [10]  605 	ld	hl, #0x000a
   50BE E5            [11]  606 	push	hl
   50BF C5            [11]  607 	push	bc
   50C0 CD 90 61      [17]  608 	call	__divuint
   50C3 F1            [10]  609 	pop	af
   50C4 F1            [10]  610 	pop	af
   50C5 4D            [ 4]  611 	ld	c, l
   50C6 44            [ 4]  612 	ld	b, h
   50C7                     613 00110$:
                            614 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   50C7 DD 34 FF      [23]  615 	inc	-1 (ix)
   50CA C3 4C 50      [10]  616 	jp	00109$
   50CD                     617 00111$:
   50CD 33            [ 6]  618 	inc	sp
   50CE DD E1         [14]  619 	pop	ix
   50D0 C9            [10]  620 	ret
                            621 ;src/systems/hud.c:119: void hudinit(void) {
                            622 ;	---------------------------------
                            623 ; Function hudinit
                            624 ; ---------------------------------
   50D1                     625 _hudinit::
                            626 ;src/systems/hud.c:120: currenthealth = 3;
   50D1 21 0A 65      [10]  627 	ld	hl,#_currenthealth + 0
   50D4 36 03         [10]  628 	ld	(hl), #0x03
                            629 ;src/systems/hud.c:121: currentscore  = 0;
   50D6 21 00 00      [10]  630 	ld	hl, #0x0000
   50D9 22 0B 65      [16]  631 	ld	(_currentscore), hl
                            632 ;src/systems/hud.c:122: currenttime   = 90;
   50DC 21 0D 65      [10]  633 	ld	hl,#_currenttime + 0
   50DF 36 5A         [10]  634 	ld	(hl), #0x5a
                            635 ;src/systems/hud.c:123: currentlives  = 3;
   50E1 21 0E 65      [10]  636 	ld	hl,#_currentlives + 0
   50E4 36 03         [10]  637 	ld	(hl), #0x03
                            638 ;src/systems/hud.c:124: currentweapon = 0;
   50E6 21 0F 65      [10]  639 	ld	hl,#_currentweapon + 0
   50E9 36 00         [10]  640 	ld	(hl), #0x00
   50EB C9            [10]  641 	ret
                            642 ;src/systems/hud.c:127: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            643 ;	---------------------------------
                            644 ; Function hudupdate
                            645 ; ---------------------------------
   50EC                     646 _hudupdate::
                            647 ;src/systems/hud.c:128: currenthealth = lives;
   50EC 21 02 00      [10]  648 	ld	hl, #2+0
   50EF 39            [11]  649 	add	hl, sp
   50F0 7E            [ 7]  650 	ld	a, (hl)
   50F1 32 0A 65      [13]  651 	ld	(#_currenthealth + 0),a
                            652 ;src/systems/hud.c:129: currentscore  = score;
   50F4 21 03 00      [10]  653 	ld	hl, #3+0
   50F7 39            [11]  654 	add	hl, sp
   50F8 7E            [ 7]  655 	ld	a, (hl)
   50F9 32 0B 65      [13]  656 	ld	(#_currentscore + 0),a
   50FC 21 04 00      [10]  657 	ld	hl, #3+1
   50FF 39            [11]  658 	add	hl, sp
   5100 7E            [ 7]  659 	ld	a, (hl)
   5101 32 0C 65      [13]  660 	ld	(#_currentscore + 1),a
                            661 ;src/systems/hud.c:130: currenttime   = time;
   5104 21 05 00      [10]  662 	ld	hl, #5+0
   5107 39            [11]  663 	add	hl, sp
   5108 7E            [ 7]  664 	ld	a, (hl)
   5109 32 0D 65      [13]  665 	ld	(#_currenttime + 0),a
                            666 ;src/systems/hud.c:131: currentlives  = lives;
   510C 21 02 00      [10]  667 	ld	hl, #2+0
   510F 39            [11]  668 	add	hl, sp
   5110 7E            [ 7]  669 	ld	a, (hl)
   5111 32 0E 65      [13]  670 	ld	(#_currentlives + 0),a
                            671 ;src/systems/hud.c:132: currentweapon = weapon;
   5114 21 06 00      [10]  672 	ld	hl, #6+0
   5117 39            [11]  673 	add	hl, sp
   5118 7E            [ 7]  674 	ld	a, (hl)
   5119 32 0F 65      [13]  675 	ld	(#_currentweapon + 0),a
   511C C9            [10]  676 	ret
                            677 ;src/systems/hud.c:135: void hudrender(void) {
                            678 ;	---------------------------------
                            679 ; Function hudrender
                            680 ; ---------------------------------
   511D                     681 _hudrender::
                            682 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   511D 0E 00         [ 7]  683 	ld	c, #0x00
   511F                     684 00103$:
   511F 21 0A 65      [10]  685 	ld	hl, #_currenthealth
                            686 ;src/systems/hud.c:142: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   5122 79            [ 4]  687 	ld	a,c
   5123 BE            [ 7]  688 	cp	a,(hl)
   5124 30 24         [12]  689 	jr	NC,00101$
   5126 07            [ 4]  690 	rlca
   5127 07            [ 4]  691 	rlca
   5128 07            [ 4]  692 	rlca
   5129 E6 F8         [ 7]  693 	and	a, #0xf8
   512B 47            [ 4]  694 	ld	b, a
   512C C5            [11]  695 	push	bc
   512D 3E 02         [ 7]  696 	ld	a, #0x02
   512F F5            [11]  697 	push	af
   5130 33            [ 6]  698 	inc	sp
   5131 C5            [11]  699 	push	bc
   5132 33            [ 6]  700 	inc	sp
   5133 21 00 C0      [10]  701 	ld	hl, #0xc000
   5136 E5            [11]  702 	push	hl
   5137 CD 39 64      [17]  703 	call	_cpct_getScreenPtr
   513A 11 04 08      [10]  704 	ld	de, #0x0804
   513D D5            [11]  705 	push	de
   513E E5            [11]  706 	push	hl
   513F 21 FC 55      [10]  707 	ld	hl, #_hudhealthbar_data
   5142 E5            [11]  708 	push	hl
   5143 CD 6A 62      [17]  709 	call	_cpct_drawSprite
   5146 C1            [10]  710 	pop	bc
                            711 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   5147 0C            [ 4]  712 	inc	c
   5148 18 D5         [12]  713 	jr	00103$
   514A                     714 00101$:
                            715 ;src/systems/hud.c:146: scoretemp = currentscore;
   514A 2A 0B 65      [16]  716 	ld	hl, (_currentscore)
                            717 ;src/systems/hud.c:147: hud_draw_digits(scoretemp, 4, 24, 2);
   514D 01 18 02      [10]  718 	ld	bc, #0x0218
   5150 C5            [11]  719 	push	bc
   5151 3E 04         [ 7]  720 	ld	a, #0x04
   5153 F5            [11]  721 	push	af
   5154 33            [ 6]  722 	inc	sp
   5155 E5            [11]  723 	push	hl
   5156 CD 29 50      [17]  724 	call	_hud_draw_digits
   5159 F1            [10]  725 	pop	af
   515A F1            [10]  726 	pop	af
   515B 33            [ 6]  727 	inc	sp
                            728 ;src/systems/hud.c:149: timetemp = currenttime;
   515C 21 0D 65      [10]  729 	ld	hl,#_currenttime + 0
   515F 4E            [ 7]  730 	ld	c, (hl)
                            731 ;src/systems/hud.c:150: hud_draw_digits((u16)timetemp, 3, 56, 2);
   5160 06 00         [ 7]  732 	ld	b, #0x00
   5162 21 38 02      [10]  733 	ld	hl, #0x0238
   5165 E5            [11]  734 	push	hl
   5166 3E 03         [ 7]  735 	ld	a, #0x03
   5168 F5            [11]  736 	push	af
   5169 33            [ 6]  737 	inc	sp
   516A C5            [11]  738 	push	bc
   516B CD 29 50      [17]  739 	call	_hud_draw_digits
   516E F1            [10]  740 	pop	af
                            741 ;src/systems/hud.c:152: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   516F 33            [ 6]  742 	inc	sp
   5170 21 02 B4      [10]  743 	ld	hl,#0xb402
   5173 E3            [19]  744 	ex	(sp),hl
   5174 21 00 C0      [10]  745 	ld	hl, #0xc000
   5177 E5            [11]  746 	push	hl
   5178 CD 39 64      [17]  747 	call	_cpct_getScreenPtr
                            748 ;src/systems/hud.c:153: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   517B 01 C9 4E      [10]  749 	ld	bc, #_hudlives+0
   517E 11 04 08      [10]  750 	ld	de, #0x0804
   5181 D5            [11]  751 	push	de
   5182 E5            [11]  752 	push	hl
   5183 C5            [11]  753 	push	bc
   5184 CD 6A 62      [17]  754 	call	_cpct_drawSprite
                            755 ;src/systems/hud.c:155: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   5187 21 0C B4      [10]  756 	ld	hl, #0xb40c
   518A E5            [11]  757 	push	hl
   518B 21 00 C0      [10]  758 	ld	hl, #0xc000
   518E E5            [11]  759 	push	hl
   518F CD 39 64      [17]  760 	call	_cpct_getScreenPtr
                            761 ;src/systems/hud.c:156: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   5192 E5            [11]  762 	push	hl
   5193 3E 0A         [ 7]  763 	ld	a, #0x0a
   5195 F5            [11]  764 	push	af
   5196 33            [ 6]  765 	inc	sp
   5197 3A 0E 65      [13]  766 	ld	a, (_currentlives)
   519A F5            [11]  767 	push	af
   519B 33            [ 6]  768 	inc	sp
   519C CD 0F 63      [17]  769 	call	__moduchar
   519F F1            [10]  770 	pop	af
   51A0 55            [ 4]  771 	ld	d, l
   51A1 D5            [11]  772 	push	de
   51A2 33            [ 6]  773 	inc	sp
   51A3 CD 68 4E      [17]  774 	call	_hud_get_number_sprite
   51A6 33            [ 6]  775 	inc	sp
   51A7 C1            [10]  776 	pop	bc
   51A8 11 04 08      [10]  777 	ld	de, #0x0804
   51AB D5            [11]  778 	push	de
   51AC C5            [11]  779 	push	bc
   51AD E5            [11]  780 	push	hl
   51AE CD 6A 62      [17]  781 	call	_cpct_drawSprite
                            782 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   51B1 21 46 B4      [10]  783 	ld	hl, #0xb446
   51B4 E5            [11]  784 	push	hl
   51B5 21 00 C0      [10]  785 	ld	hl, #0xc000
   51B8 E5            [11]  786 	push	hl
   51B9 CD 39 64      [17]  787 	call	_cpct_getScreenPtr
                            788 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   51BC E5            [11]  789 	push	hl
   51BD 3E 0A         [ 7]  790 	ld	a, #0x0a
   51BF F5            [11]  791 	push	af
   51C0 33            [ 6]  792 	inc	sp
   51C1 3A 0F 65      [13]  793 	ld	a, (_currentweapon)
   51C4 F5            [11]  794 	push	af
   51C5 33            [ 6]  795 	inc	sp
   51C6 CD 0F 63      [17]  796 	call	__moduchar
   51C9 F1            [10]  797 	pop	af
   51CA 55            [ 4]  798 	ld	d, l
   51CB D5            [11]  799 	push	de
   51CC 33            [ 6]  800 	inc	sp
   51CD CD 68 4E      [17]  801 	call	_hud_get_number_sprite
   51D0 33            [ 6]  802 	inc	sp
   51D1 C1            [10]  803 	pop	bc
   51D2 11 04 08      [10]  804 	ld	de, #0x0804
   51D5 D5            [11]  805 	push	de
   51D6 C5            [11]  806 	push	bc
   51D7 E5            [11]  807 	push	hl
   51D8 CD 6A 62      [17]  808 	call	_cpct_drawSprite
   51DB C9            [10]  809 	ret
                            810 	.area _CODE
                            811 	.area _INITIALIZER
                            812 	.area _CABS (ABS)
