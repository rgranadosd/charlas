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
   6476                      23 _currenthealth:
   6476                      24 	.ds 1
   6477                      25 _currentscore:
   6477                      26 	.ds 2
   6479                      27 _currenttime:
   6479                      28 	.ds 1
   647A                      29 _currentlives:
   647A                      30 	.ds 1
   647B                      31 _currentweapon:
   647B                      32 	.ds 1
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
   4E5B                      61 _hud_get_number_sprite:
                             62 ;src/systems/hud.c:81: switch (digit % 10) {
   4E5B 3E 0A         [ 7]   63 	ld	a, #0x0a
   4E5D F5            [11]   64 	push	af
   4E5E 33            [ 6]   65 	inc	sp
   4E5F 21 03 00      [10]   66 	ld	hl, #3+0
   4E62 39            [11]   67 	add	hl, sp
   4E63 7E            [ 7]   68 	ld	a, (hl)
   4E64 F5            [11]   69 	push	af
   4E65 33            [ 6]   70 	inc	sp
   4E66 CD 7B 62      [17]   71 	call	__moduchar
   4E69 F1            [10]   72 	pop	af
   4E6A 4D            [ 4]   73 	ld	c, l
   4E6B 3E 08         [ 7]   74 	ld	a, #0x08
   4E6D 91            [ 4]   75 	sub	a, c
   4E6E 38 48         [12]   76 	jr	C,00110$
   4E70 06 00         [ 7]   77 	ld	b, #0x00
   4E72 21 79 4E      [10]   78 	ld	hl, #00118$
   4E75 09            [11]   79 	add	hl, bc
   4E76 09            [11]   80 	add	hl, bc
   4E77 09            [11]   81 	add	hl, bc
   4E78 E9            [ 4]   82 	jp	(hl)
   4E79                      83 00118$:
   4E79 C3 94 4E      [10]   84 	jp	00101$
   4E7C C3 98 4E      [10]   85 	jp	00102$
   4E7F C3 9C 4E      [10]   86 	jp	00103$
   4E82 C3 A0 4E      [10]   87 	jp	00104$
   4E85 C3 A4 4E      [10]   88 	jp	00105$
   4E88 C3 A8 4E      [10]   89 	jp	00106$
   4E8B C3 AC 4E      [10]   90 	jp	00107$
   4E8E C3 B0 4E      [10]   91 	jp	00108$
   4E91 C3 B4 4E      [10]   92 	jp	00109$
                             93 ;src/systems/hud.c:82: case 0: return huddigit_0;
   4E94                      94 00101$:
   4E94 21 DC 4E      [10]   95 	ld	hl, #_huddigit_0
   4E97 C9            [10]   96 	ret
                             97 ;src/systems/hud.c:83: case 1: return huddigit_1;
   4E98                      98 00102$:
   4E98 21 FC 4E      [10]   99 	ld	hl, #_huddigit_1
   4E9B C9            [10]  100 	ret
                            101 ;src/systems/hud.c:84: case 2: return huddigit_2;
   4E9C                     102 00103$:
   4E9C 21 1C 4F      [10]  103 	ld	hl, #_huddigit_2
   4E9F C9            [10]  104 	ret
                            105 ;src/systems/hud.c:85: case 3: return huddigit_3;
   4EA0                     106 00104$:
   4EA0 21 3C 4F      [10]  107 	ld	hl, #_huddigit_3
   4EA3 C9            [10]  108 	ret
                            109 ;src/systems/hud.c:86: case 4: return huddigit_4;
   4EA4                     110 00105$:
   4EA4 21 5C 4F      [10]  111 	ld	hl, #_huddigit_4
   4EA7 C9            [10]  112 	ret
                            113 ;src/systems/hud.c:87: case 5: return huddigit_5;
   4EA8                     114 00106$:
   4EA8 21 7C 4F      [10]  115 	ld	hl, #_huddigit_5
   4EAB C9            [10]  116 	ret
                            117 ;src/systems/hud.c:88: case 6: return huddigit_6;
   4EAC                     118 00107$:
   4EAC 21 9C 4F      [10]  119 	ld	hl, #_huddigit_6
   4EAF C9            [10]  120 	ret
                            121 ;src/systems/hud.c:89: case 7: return huddigit_7;
   4EB0                     122 00108$:
   4EB0 21 BC 4F      [10]  123 	ld	hl, #_huddigit_7
   4EB3 C9            [10]  124 	ret
                            125 ;src/systems/hud.c:90: case 8: return huddigit_8;
   4EB4                     126 00109$:
   4EB4 21 DC 4F      [10]  127 	ld	hl, #_huddigit_8
   4EB7 C9            [10]  128 	ret
                            129 ;src/systems/hud.c:91: default: return huddigit_9;
   4EB8                     130 00110$:
   4EB8 21 FC 4F      [10]  131 	ld	hl, #_huddigit_9
                            132 ;src/systems/hud.c:92: }
   4EBB C9            [10]  133 	ret
   4EBC                     134 _hudlives:
   4EBC 30                  135 	.db #0x30	; 48	'0'
   4EBD 30                  136 	.db #0x30	; 48	'0'
   4EBE 30                  137 	.db #0x30	; 48	'0'
   4EBF 30                  138 	.db #0x30	; 48	'0'
   4EC0 20                  139 	.db #0x20	; 32
   4EC1 10                  140 	.db #0x10	; 16
   4EC2 00                  141 	.db #0x00	; 0
   4EC3 10                  142 	.db #0x10	; 16
   4EC4 20                  143 	.db #0x20	; 32
   4EC5 10                  144 	.db #0x10	; 16
   4EC6 00                  145 	.db #0x00	; 0
   4EC7 10                  146 	.db #0x10	; 16
   4EC8 20                  147 	.db #0x20	; 32
   4EC9 10                  148 	.db #0x10	; 16
   4ECA 00                  149 	.db #0x00	; 0
   4ECB 10                  150 	.db #0x10	; 16
   4ECC 30                  151 	.db #0x30	; 48	'0'
   4ECD 30                  152 	.db #0x30	; 48	'0'
   4ECE 30                  153 	.db #0x30	; 48	'0'
   4ECF 30                  154 	.db #0x30	; 48	'0'
   4ED0 20                  155 	.db #0x20	; 32
   4ED1 10                  156 	.db #0x10	; 16
   4ED2 00                  157 	.db #0x00	; 0
   4ED3 10                  158 	.db #0x10	; 16
   4ED4 20                  159 	.db #0x20	; 32
   4ED5 10                  160 	.db #0x10	; 16
   4ED6 00                  161 	.db #0x00	; 0
   4ED7 10                  162 	.db #0x10	; 16
   4ED8 30                  163 	.db #0x30	; 48	'0'
   4ED9 30                  164 	.db #0x30	; 48	'0'
   4EDA 30                  165 	.db #0x30	; 48	'0'
   4EDB 30                  166 	.db #0x30	; 48	'0'
   4EDC                     167 _huddigit_0:
   4EDC 14                  168 	.db #0x14	; 20
   4EDD 3C                  169 	.db #0x3c	; 60
   4EDE 3C                  170 	.db #0x3c	; 60
   4EDF 28                  171 	.db #0x28	; 40
   4EE0 28                  172 	.db #0x28	; 40
   4EE1 00                  173 	.db #0x00	; 0
   4EE2 00                  174 	.db #0x00	; 0
   4EE3 14                  175 	.db #0x14	; 20
   4EE4 28                  176 	.db #0x28	; 40
   4EE5 00                  177 	.db #0x00	; 0
   4EE6 00                  178 	.db #0x00	; 0
   4EE7 14                  179 	.db #0x14	; 20
   4EE8 00                  180 	.db #0x00	; 0
   4EE9 00                  181 	.db #0x00	; 0
   4EEA 00                  182 	.db #0x00	; 0
   4EEB 00                  183 	.db #0x00	; 0
   4EEC 28                  184 	.db #0x28	; 40
   4EED 00                  185 	.db #0x00	; 0
   4EEE 00                  186 	.db #0x00	; 0
   4EEF 14                  187 	.db #0x14	; 20
   4EF0 28                  188 	.db #0x28	; 40
   4EF1 00                  189 	.db #0x00	; 0
   4EF2 00                  190 	.db #0x00	; 0
   4EF3 14                  191 	.db #0x14	; 20
   4EF4 28                  192 	.db #0x28	; 40
   4EF5 00                  193 	.db #0x00	; 0
   4EF6 00                  194 	.db #0x00	; 0
   4EF7 14                  195 	.db #0x14	; 20
   4EF8 14                  196 	.db #0x14	; 20
   4EF9 3C                  197 	.db #0x3c	; 60
   4EFA 3C                  198 	.db #0x3c	; 60
   4EFB 28                  199 	.db #0x28	; 40
   4EFC                     200 _huddigit_1:
   4EFC 00                  201 	.db #0x00	; 0
   4EFD 00                  202 	.db #0x00	; 0
   4EFE 00                  203 	.db #0x00	; 0
   4EFF 00                  204 	.db #0x00	; 0
   4F00 00                  205 	.db #0x00	; 0
   4F01 00                  206 	.db #0x00	; 0
   4F02 00                  207 	.db #0x00	; 0
   4F03 14                  208 	.db #0x14	; 20
   4F04 00                  209 	.db #0x00	; 0
   4F05 00                  210 	.db #0x00	; 0
   4F06 00                  211 	.db #0x00	; 0
   4F07 14                  212 	.db #0x14	; 20
   4F08 00                  213 	.db #0x00	; 0
   4F09 00                  214 	.db #0x00	; 0
   4F0A 00                  215 	.db #0x00	; 0
   4F0B 00                  216 	.db #0x00	; 0
   4F0C 00                  217 	.db #0x00	; 0
   4F0D 00                  218 	.db #0x00	; 0
   4F0E 00                  219 	.db #0x00	; 0
   4F0F 14                  220 	.db #0x14	; 20
   4F10 00                  221 	.db #0x00	; 0
   4F11 00                  222 	.db #0x00	; 0
   4F12 00                  223 	.db #0x00	; 0
   4F13 14                  224 	.db #0x14	; 20
   4F14 00                  225 	.db #0x00	; 0
   4F15 00                  226 	.db #0x00	; 0
   4F16 00                  227 	.db #0x00	; 0
   4F17 14                  228 	.db #0x14	; 20
   4F18 00                  229 	.db #0x00	; 0
   4F19 00                  230 	.db #0x00	; 0
   4F1A 00                  231 	.db #0x00	; 0
   4F1B 00                  232 	.db #0x00	; 0
   4F1C                     233 _huddigit_2:
   4F1C 14                  234 	.db #0x14	; 20
   4F1D 3C                  235 	.db #0x3c	; 60
   4F1E 3C                  236 	.db #0x3c	; 60
   4F1F 28                  237 	.db #0x28	; 40
   4F20 00                  238 	.db #0x00	; 0
   4F21 00                  239 	.db #0x00	; 0
   4F22 00                  240 	.db #0x00	; 0
   4F23 14                  241 	.db #0x14	; 20
   4F24 00                  242 	.db #0x00	; 0
   4F25 00                  243 	.db #0x00	; 0
   4F26 00                  244 	.db #0x00	; 0
   4F27 14                  245 	.db #0x14	; 20
   4F28 14                  246 	.db #0x14	; 20
   4F29 3C                  247 	.db #0x3c	; 60
   4F2A 3C                  248 	.db #0x3c	; 60
   4F2B 28                  249 	.db #0x28	; 40
   4F2C 28                  250 	.db #0x28	; 40
   4F2D 00                  251 	.db #0x00	; 0
   4F2E 00                  252 	.db #0x00	; 0
   4F2F 00                  253 	.db #0x00	; 0
   4F30 28                  254 	.db #0x28	; 40
   4F31 00                  255 	.db #0x00	; 0
   4F32 00                  256 	.db #0x00	; 0
   4F33 00                  257 	.db #0x00	; 0
   4F34 28                  258 	.db #0x28	; 40
   4F35 00                  259 	.db #0x00	; 0
   4F36 00                  260 	.db #0x00	; 0
   4F37 00                  261 	.db #0x00	; 0
   4F38 14                  262 	.db #0x14	; 20
   4F39 3C                  263 	.db #0x3c	; 60
   4F3A 3C                  264 	.db #0x3c	; 60
   4F3B 28                  265 	.db #0x28	; 40
   4F3C                     266 _huddigit_3:
   4F3C 14                  267 	.db #0x14	; 20
   4F3D 3C                  268 	.db #0x3c	; 60
   4F3E 3C                  269 	.db #0x3c	; 60
   4F3F 28                  270 	.db #0x28	; 40
   4F40 00                  271 	.db #0x00	; 0
   4F41 00                  272 	.db #0x00	; 0
   4F42 00                  273 	.db #0x00	; 0
   4F43 14                  274 	.db #0x14	; 20
   4F44 00                  275 	.db #0x00	; 0
   4F45 00                  276 	.db #0x00	; 0
   4F46 00                  277 	.db #0x00	; 0
   4F47 14                  278 	.db #0x14	; 20
   4F48 14                  279 	.db #0x14	; 20
   4F49 3C                  280 	.db #0x3c	; 60
   4F4A 3C                  281 	.db #0x3c	; 60
   4F4B 28                  282 	.db #0x28	; 40
   4F4C 00                  283 	.db #0x00	; 0
   4F4D 00                  284 	.db #0x00	; 0
   4F4E 00                  285 	.db #0x00	; 0
   4F4F 14                  286 	.db #0x14	; 20
   4F50 00                  287 	.db #0x00	; 0
   4F51 00                  288 	.db #0x00	; 0
   4F52 00                  289 	.db #0x00	; 0
   4F53 14                  290 	.db #0x14	; 20
   4F54 00                  291 	.db #0x00	; 0
   4F55 00                  292 	.db #0x00	; 0
   4F56 00                  293 	.db #0x00	; 0
   4F57 14                  294 	.db #0x14	; 20
   4F58 14                  295 	.db #0x14	; 20
   4F59 3C                  296 	.db #0x3c	; 60
   4F5A 3C                  297 	.db #0x3c	; 60
   4F5B 28                  298 	.db #0x28	; 40
   4F5C                     299 _huddigit_4:
   4F5C 00                  300 	.db #0x00	; 0
   4F5D 00                  301 	.db #0x00	; 0
   4F5E 00                  302 	.db #0x00	; 0
   4F5F 00                  303 	.db #0x00	; 0
   4F60 28                  304 	.db #0x28	; 40
   4F61 00                  305 	.db #0x00	; 0
   4F62 00                  306 	.db #0x00	; 0
   4F63 14                  307 	.db #0x14	; 20
   4F64 28                  308 	.db #0x28	; 40
   4F65 00                  309 	.db #0x00	; 0
   4F66 00                  310 	.db #0x00	; 0
   4F67 14                  311 	.db #0x14	; 20
   4F68 14                  312 	.db #0x14	; 20
   4F69 3C                  313 	.db #0x3c	; 60
   4F6A 3C                  314 	.db #0x3c	; 60
   4F6B 28                  315 	.db #0x28	; 40
   4F6C 00                  316 	.db #0x00	; 0
   4F6D 00                  317 	.db #0x00	; 0
   4F6E 00                  318 	.db #0x00	; 0
   4F6F 14                  319 	.db #0x14	; 20
   4F70 00                  320 	.db #0x00	; 0
   4F71 00                  321 	.db #0x00	; 0
   4F72 00                  322 	.db #0x00	; 0
   4F73 14                  323 	.db #0x14	; 20
   4F74 00                  324 	.db #0x00	; 0
   4F75 00                  325 	.db #0x00	; 0
   4F76 00                  326 	.db #0x00	; 0
   4F77 14                  327 	.db #0x14	; 20
   4F78 00                  328 	.db #0x00	; 0
   4F79 00                  329 	.db #0x00	; 0
   4F7A 00                  330 	.db #0x00	; 0
   4F7B 00                  331 	.db #0x00	; 0
   4F7C                     332 _huddigit_5:
   4F7C 14                  333 	.db #0x14	; 20
   4F7D 3C                  334 	.db #0x3c	; 60
   4F7E 3C                  335 	.db #0x3c	; 60
   4F7F 28                  336 	.db #0x28	; 40
   4F80 28                  337 	.db #0x28	; 40
   4F81 00                  338 	.db #0x00	; 0
   4F82 00                  339 	.db #0x00	; 0
   4F83 00                  340 	.db #0x00	; 0
   4F84 28                  341 	.db #0x28	; 40
   4F85 00                  342 	.db #0x00	; 0
   4F86 00                  343 	.db #0x00	; 0
   4F87 00                  344 	.db #0x00	; 0
   4F88 14                  345 	.db #0x14	; 20
   4F89 3C                  346 	.db #0x3c	; 60
   4F8A 3C                  347 	.db #0x3c	; 60
   4F8B 28                  348 	.db #0x28	; 40
   4F8C 00                  349 	.db #0x00	; 0
   4F8D 00                  350 	.db #0x00	; 0
   4F8E 00                  351 	.db #0x00	; 0
   4F8F 14                  352 	.db #0x14	; 20
   4F90 00                  353 	.db #0x00	; 0
   4F91 00                  354 	.db #0x00	; 0
   4F92 00                  355 	.db #0x00	; 0
   4F93 14                  356 	.db #0x14	; 20
   4F94 00                  357 	.db #0x00	; 0
   4F95 00                  358 	.db #0x00	; 0
   4F96 00                  359 	.db #0x00	; 0
   4F97 14                  360 	.db #0x14	; 20
   4F98 14                  361 	.db #0x14	; 20
   4F99 3C                  362 	.db #0x3c	; 60
   4F9A 3C                  363 	.db #0x3c	; 60
   4F9B 28                  364 	.db #0x28	; 40
   4F9C                     365 _huddigit_6:
   4F9C 14                  366 	.db #0x14	; 20
   4F9D 3C                  367 	.db #0x3c	; 60
   4F9E 3C                  368 	.db #0x3c	; 60
   4F9F 28                  369 	.db #0x28	; 40
   4FA0 28                  370 	.db #0x28	; 40
   4FA1 00                  371 	.db #0x00	; 0
   4FA2 00                  372 	.db #0x00	; 0
   4FA3 00                  373 	.db #0x00	; 0
   4FA4 28                  374 	.db #0x28	; 40
   4FA5 00                  375 	.db #0x00	; 0
   4FA6 00                  376 	.db #0x00	; 0
   4FA7 00                  377 	.db #0x00	; 0
   4FA8 14                  378 	.db #0x14	; 20
   4FA9 3C                  379 	.db #0x3c	; 60
   4FAA 3C                  380 	.db #0x3c	; 60
   4FAB 28                  381 	.db #0x28	; 40
   4FAC 28                  382 	.db #0x28	; 40
   4FAD 00                  383 	.db #0x00	; 0
   4FAE 00                  384 	.db #0x00	; 0
   4FAF 14                  385 	.db #0x14	; 20
   4FB0 28                  386 	.db #0x28	; 40
   4FB1 00                  387 	.db #0x00	; 0
   4FB2 00                  388 	.db #0x00	; 0
   4FB3 14                  389 	.db #0x14	; 20
   4FB4 28                  390 	.db #0x28	; 40
   4FB5 00                  391 	.db #0x00	; 0
   4FB6 00                  392 	.db #0x00	; 0
   4FB7 14                  393 	.db #0x14	; 20
   4FB8 14                  394 	.db #0x14	; 20
   4FB9 3C                  395 	.db #0x3c	; 60
   4FBA 3C                  396 	.db #0x3c	; 60
   4FBB 28                  397 	.db #0x28	; 40
   4FBC                     398 _huddigit_7:
   4FBC 14                  399 	.db #0x14	; 20
   4FBD 3C                  400 	.db #0x3c	; 60
   4FBE 3C                  401 	.db #0x3c	; 60
   4FBF 28                  402 	.db #0x28	; 40
   4FC0 00                  403 	.db #0x00	; 0
   4FC1 00                  404 	.db #0x00	; 0
   4FC2 00                  405 	.db #0x00	; 0
   4FC3 14                  406 	.db #0x14	; 20
   4FC4 00                  407 	.db #0x00	; 0
   4FC5 00                  408 	.db #0x00	; 0
   4FC6 00                  409 	.db #0x00	; 0
   4FC7 14                  410 	.db #0x14	; 20
   4FC8 00                  411 	.db #0x00	; 0
   4FC9 00                  412 	.db #0x00	; 0
   4FCA 00                  413 	.db #0x00	; 0
   4FCB 00                  414 	.db #0x00	; 0
   4FCC 00                  415 	.db #0x00	; 0
   4FCD 00                  416 	.db #0x00	; 0
   4FCE 00                  417 	.db #0x00	; 0
   4FCF 14                  418 	.db #0x14	; 20
   4FD0 00                  419 	.db #0x00	; 0
   4FD1 00                  420 	.db #0x00	; 0
   4FD2 00                  421 	.db #0x00	; 0
   4FD3 14                  422 	.db #0x14	; 20
   4FD4 00                  423 	.db #0x00	; 0
   4FD5 00                  424 	.db #0x00	; 0
   4FD6 00                  425 	.db #0x00	; 0
   4FD7 14                  426 	.db #0x14	; 20
   4FD8 00                  427 	.db #0x00	; 0
   4FD9 00                  428 	.db #0x00	; 0
   4FDA 00                  429 	.db #0x00	; 0
   4FDB 00                  430 	.db #0x00	; 0
   4FDC                     431 _huddigit_8:
   4FDC 14                  432 	.db #0x14	; 20
   4FDD 3C                  433 	.db #0x3c	; 60
   4FDE 3C                  434 	.db #0x3c	; 60
   4FDF 28                  435 	.db #0x28	; 40
   4FE0 28                  436 	.db #0x28	; 40
   4FE1 00                  437 	.db #0x00	; 0
   4FE2 00                  438 	.db #0x00	; 0
   4FE3 14                  439 	.db #0x14	; 20
   4FE4 28                  440 	.db #0x28	; 40
   4FE5 00                  441 	.db #0x00	; 0
   4FE6 00                  442 	.db #0x00	; 0
   4FE7 14                  443 	.db #0x14	; 20
   4FE8 14                  444 	.db #0x14	; 20
   4FE9 3C                  445 	.db #0x3c	; 60
   4FEA 3C                  446 	.db #0x3c	; 60
   4FEB 28                  447 	.db #0x28	; 40
   4FEC 28                  448 	.db #0x28	; 40
   4FED 00                  449 	.db #0x00	; 0
   4FEE 00                  450 	.db #0x00	; 0
   4FEF 14                  451 	.db #0x14	; 20
   4FF0 28                  452 	.db #0x28	; 40
   4FF1 00                  453 	.db #0x00	; 0
   4FF2 00                  454 	.db #0x00	; 0
   4FF3 14                  455 	.db #0x14	; 20
   4FF4 28                  456 	.db #0x28	; 40
   4FF5 00                  457 	.db #0x00	; 0
   4FF6 00                  458 	.db #0x00	; 0
   4FF7 14                  459 	.db #0x14	; 20
   4FF8 14                  460 	.db #0x14	; 20
   4FF9 3C                  461 	.db #0x3c	; 60
   4FFA 3C                  462 	.db #0x3c	; 60
   4FFB 28                  463 	.db #0x28	; 40
   4FFC                     464 _huddigit_9:
   4FFC 14                  465 	.db #0x14	; 20
   4FFD 3C                  466 	.db #0x3c	; 60
   4FFE 3C                  467 	.db #0x3c	; 60
   4FFF 28                  468 	.db #0x28	; 40
   5000 28                  469 	.db #0x28	; 40
   5001 00                  470 	.db #0x00	; 0
   5002 00                  471 	.db #0x00	; 0
   5003 14                  472 	.db #0x14	; 20
   5004 28                  473 	.db #0x28	; 40
   5005 00                  474 	.db #0x00	; 0
   5006 00                  475 	.db #0x00	; 0
   5007 14                  476 	.db #0x14	; 20
   5008 14                  477 	.db #0x14	; 20
   5009 3C                  478 	.db #0x3c	; 60
   500A 3C                  479 	.db #0x3c	; 60
   500B 28                  480 	.db #0x28	; 40
   500C 00                  481 	.db #0x00	; 0
   500D 00                  482 	.db #0x00	; 0
   500E 00                  483 	.db #0x00	; 0
   500F 14                  484 	.db #0x14	; 20
   5010 00                  485 	.db #0x00	; 0
   5011 00                  486 	.db #0x00	; 0
   5012 00                  487 	.db #0x00	; 0
   5013 14                  488 	.db #0x14	; 20
   5014 00                  489 	.db #0x00	; 0
   5015 00                  490 	.db #0x00	; 0
   5016 00                  491 	.db #0x00	; 0
   5017 14                  492 	.db #0x14	; 20
   5018 14                  493 	.db #0x14	; 20
   5019 3C                  494 	.db #0x3c	; 60
   501A 3C                  495 	.db #0x3c	; 60
   501B 28                  496 	.db #0x28	; 40
                            497 ;src/systems/hud.c:95: static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
                            498 ;	---------------------------------
                            499 ; Function hud_draw_digits
                            500 ; ---------------------------------
   501C                     501 _hud_draw_digits:
   501C DD E5         [15]  502 	push	ix
   501E DD 21 00 00   [14]  503 	ld	ix,#0
   5022 DD 39         [15]  504 	add	ix,sp
   5024 3B            [ 6]  505 	dec	sp
                            506 ;src/systems/hud.c:101: divisor = 1;
   5025 01 01 00      [10]  507 	ld	bc, #0x0001
                            508 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   5028 1E 01         [ 7]  509 	ld	e, #0x01
   502A                     510 00106$:
   502A 7B            [ 4]  511 	ld	a, e
   502B DD 96 06      [19]  512 	sub	a, 6 (ix)
   502E 30 0B         [12]  513 	jr	NC,00101$
                            514 ;src/systems/hud.c:103: divisor *= 10;
   5030 69            [ 4]  515 	ld	l, c
   5031 60            [ 4]  516 	ld	h, b
   5032 29            [11]  517 	add	hl, hl
   5033 29            [11]  518 	add	hl, hl
   5034 09            [11]  519 	add	hl, bc
   5035 29            [11]  520 	add	hl, hl
   5036 4D            [ 4]  521 	ld	c, l
   5037 44            [ 4]  522 	ld	b, h
                            523 ;src/systems/hud.c:102: for (i = 1; i < digits; ++i) {
   5038 1C            [ 4]  524 	inc	e
   5039 18 EF         [12]  525 	jr	00106$
   503B                     526 00101$:
                            527 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   503B DD 36 FF 00   [19]  528 	ld	-1 (ix), #0x00
   503F                     529 00109$:
   503F DD 7E FF      [19]  530 	ld	a, -1 (ix)
   5042 DD 96 06      [19]  531 	sub	a, 6 (ix)
   5045 30 79         [12]  532 	jr	NC,00111$
                            533 ;src/systems/hud.c:107: digit = (u8)(value / divisor);
   5047 C5            [11]  534 	push	bc
   5048 C5            [11]  535 	push	bc
   5049 DD 6E 04      [19]  536 	ld	l,4 (ix)
   504C DD 66 05      [19]  537 	ld	h,5 (ix)
   504F E5            [11]  538 	push	hl
   5050 CD FC 60      [17]  539 	call	__divuint
   5053 F1            [10]  540 	pop	af
   5054 F1            [10]  541 	pop	af
   5055 5D            [ 4]  542 	ld	e, l
   5056 C1            [10]  543 	pop	bc
                            544 ;src/systems/hud.c:108: value = (u16)(value % divisor);
   5057 C5            [11]  545 	push	bc
   5058 D5            [11]  546 	push	de
   5059 C5            [11]  547 	push	bc
   505A DD 6E 04      [19]  548 	ld	l,4 (ix)
   505D DD 66 05      [19]  549 	ld	h,5 (ix)
   5060 E5            [11]  550 	push	hl
   5061 CD 87 62      [17]  551 	call	__moduint
   5064 F1            [10]  552 	pop	af
   5065 F1            [10]  553 	pop	af
   5066 D1            [10]  554 	pop	de
   5067 C1            [10]  555 	pop	bc
   5068 DD 75 04      [19]  556 	ld	4 (ix), l
   506B DD 74 05      [19]  557 	ld	5 (ix), h
                            558 ;src/systems/hud.c:110: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 4), y);
   506E DD 7E FF      [19]  559 	ld	a, -1 (ix)
   5071 87            [ 4]  560 	add	a, a
   5072 87            [ 4]  561 	add	a, a
   5073 57            [ 4]  562 	ld	d, a
   5074 DD 7E 07      [19]  563 	ld	a, 7 (ix)
   5077 82            [ 4]  564 	add	a, d
   5078 57            [ 4]  565 	ld	d, a
   5079 C5            [11]  566 	push	bc
   507A D5            [11]  567 	push	de
   507B DD 7E 08      [19]  568 	ld	a, 8 (ix)
   507E F5            [11]  569 	push	af
   507F 33            [ 6]  570 	inc	sp
   5080 D5            [11]  571 	push	de
   5081 33            [ 6]  572 	inc	sp
   5082 21 00 C0      [10]  573 	ld	hl, #0xc000
   5085 E5            [11]  574 	push	hl
   5086 CD A5 63      [17]  575 	call	_cpct_getScreenPtr
   5089 D1            [10]  576 	pop	de
   508A C1            [10]  577 	pop	bc
                            578 ;src/systems/hud.c:111: cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 4, 8);
   508B E5            [11]  579 	push	hl
   508C C5            [11]  580 	push	bc
   508D 7B            [ 4]  581 	ld	a, e
   508E F5            [11]  582 	push	af
   508F 33            [ 6]  583 	inc	sp
   5090 CD 5B 4E      [17]  584 	call	_hud_get_number_sprite
   5093 33            [ 6]  585 	inc	sp
   5094 EB            [ 4]  586 	ex	de,hl
   5095 C1            [10]  587 	pop	bc
   5096 E1            [10]  588 	pop	hl
   5097 D5            [11]  589 	push	de
   5098 FD E1         [14]  590 	pop	iy
   509A C5            [11]  591 	push	bc
   509B 11 04 08      [10]  592 	ld	de, #0x0804
   509E D5            [11]  593 	push	de
   509F E5            [11]  594 	push	hl
   50A0 FD E5         [15]  595 	push	iy
   50A2 CD D6 61      [17]  596 	call	_cpct_drawSprite
   50A5 C1            [10]  597 	pop	bc
                            598 ;src/systems/hud.c:113: if (divisor > 1) {
   50A6 3E 01         [ 7]  599 	ld	a, #0x01
   50A8 B9            [ 4]  600 	cp	a, c
   50A9 3E 00         [ 7]  601 	ld	a, #0x00
   50AB 98            [ 4]  602 	sbc	a, b
   50AC 30 0C         [12]  603 	jr	NC,00110$
                            604 ;src/systems/hud.c:114: divisor /= 10;
   50AE 21 0A 00      [10]  605 	ld	hl, #0x000a
   50B1 E5            [11]  606 	push	hl
   50B2 C5            [11]  607 	push	bc
   50B3 CD FC 60      [17]  608 	call	__divuint
   50B6 F1            [10]  609 	pop	af
   50B7 F1            [10]  610 	pop	af
   50B8 4D            [ 4]  611 	ld	c, l
   50B9 44            [ 4]  612 	ld	b, h
   50BA                     613 00110$:
                            614 ;src/systems/hud.c:106: for (i = 0; i < digits; ++i) {
   50BA DD 34 FF      [23]  615 	inc	-1 (ix)
   50BD C3 3F 50      [10]  616 	jp	00109$
   50C0                     617 00111$:
   50C0 33            [ 6]  618 	inc	sp
   50C1 DD E1         [14]  619 	pop	ix
   50C3 C9            [10]  620 	ret
                            621 ;src/systems/hud.c:119: void hudinit(void) {
                            622 ;	---------------------------------
                            623 ; Function hudinit
                            624 ; ---------------------------------
   50C4                     625 _hudinit::
                            626 ;src/systems/hud.c:120: currenthealth = 3;
   50C4 21 76 64      [10]  627 	ld	hl,#_currenthealth + 0
   50C7 36 03         [10]  628 	ld	(hl), #0x03
                            629 ;src/systems/hud.c:121: currentscore  = 0;
   50C9 21 00 00      [10]  630 	ld	hl, #0x0000
   50CC 22 77 64      [16]  631 	ld	(_currentscore), hl
                            632 ;src/systems/hud.c:122: currenttime   = 90;
   50CF 21 79 64      [10]  633 	ld	hl,#_currenttime + 0
   50D2 36 5A         [10]  634 	ld	(hl), #0x5a
                            635 ;src/systems/hud.c:123: currentlives  = 3;
   50D4 21 7A 64      [10]  636 	ld	hl,#_currentlives + 0
   50D7 36 03         [10]  637 	ld	(hl), #0x03
                            638 ;src/systems/hud.c:124: currentweapon = 0;
   50D9 21 7B 64      [10]  639 	ld	hl,#_currentweapon + 0
   50DC 36 00         [10]  640 	ld	(hl), #0x00
   50DE C9            [10]  641 	ret
                            642 ;src/systems/hud.c:127: void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
                            643 ;	---------------------------------
                            644 ; Function hudupdate
                            645 ; ---------------------------------
   50DF                     646 _hudupdate::
                            647 ;src/systems/hud.c:128: currenthealth = lives;
   50DF 21 02 00      [10]  648 	ld	hl, #2+0
   50E2 39            [11]  649 	add	hl, sp
   50E3 7E            [ 7]  650 	ld	a, (hl)
   50E4 32 76 64      [13]  651 	ld	(#_currenthealth + 0),a
                            652 ;src/systems/hud.c:129: currentscore  = score;
   50E7 21 03 00      [10]  653 	ld	hl, #3+0
   50EA 39            [11]  654 	add	hl, sp
   50EB 7E            [ 7]  655 	ld	a, (hl)
   50EC 32 77 64      [13]  656 	ld	(#_currentscore + 0),a
   50EF 21 04 00      [10]  657 	ld	hl, #3+1
   50F2 39            [11]  658 	add	hl, sp
   50F3 7E            [ 7]  659 	ld	a, (hl)
   50F4 32 78 64      [13]  660 	ld	(#_currentscore + 1),a
                            661 ;src/systems/hud.c:130: currenttime   = time;
   50F7 21 05 00      [10]  662 	ld	hl, #5+0
   50FA 39            [11]  663 	add	hl, sp
   50FB 7E            [ 7]  664 	ld	a, (hl)
   50FC 32 79 64      [13]  665 	ld	(#_currenttime + 0),a
                            666 ;src/systems/hud.c:131: currentlives  = lives;
   50FF 21 02 00      [10]  667 	ld	hl, #2+0
   5102 39            [11]  668 	add	hl, sp
   5103 7E            [ 7]  669 	ld	a, (hl)
   5104 32 7A 64      [13]  670 	ld	(#_currentlives + 0),a
                            671 ;src/systems/hud.c:132: currentweapon = weapon;
   5107 21 06 00      [10]  672 	ld	hl, #6+0
   510A 39            [11]  673 	add	hl, sp
   510B 7E            [ 7]  674 	ld	a, (hl)
   510C 32 7B 64      [13]  675 	ld	(#_currentweapon + 0),a
   510F C9            [10]  676 	ret
                            677 ;src/systems/hud.c:135: void hudrender(void) {
                            678 ;	---------------------------------
                            679 ; Function hudrender
                            680 ; ---------------------------------
   5110                     681 _hudrender::
                            682 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   5110 0E 00         [ 7]  683 	ld	c, #0x00
   5112                     684 00103$:
   5112 21 76 64      [10]  685 	ld	hl, #_currenthealth
                            686 ;src/systems/hud.c:142: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
   5115 79            [ 4]  687 	ld	a,c
   5116 BE            [ 7]  688 	cp	a,(hl)
   5117 30 24         [12]  689 	jr	NC,00101$
   5119 07            [ 4]  690 	rlca
   511A 07            [ 4]  691 	rlca
   511B 07            [ 4]  692 	rlca
   511C E6 F8         [ 7]  693 	and	a, #0xf8
   511E 47            [ 4]  694 	ld	b, a
   511F C5            [11]  695 	push	bc
   5120 3E 02         [ 7]  696 	ld	a, #0x02
   5122 F5            [11]  697 	push	af
   5123 33            [ 6]  698 	inc	sp
   5124 C5            [11]  699 	push	bc
   5125 33            [ 6]  700 	inc	sp
   5126 21 00 C0      [10]  701 	ld	hl, #0xc000
   5129 E5            [11]  702 	push	hl
   512A CD A5 63      [17]  703 	call	_cpct_getScreenPtr
   512D 11 04 08      [10]  704 	ld	de, #0x0804
   5130 D5            [11]  705 	push	de
   5131 E5            [11]  706 	push	hl
   5132 21 61 55      [10]  707 	ld	hl, #_hudhealthbar_data
   5135 E5            [11]  708 	push	hl
   5136 CD D6 61      [17]  709 	call	_cpct_drawSprite
   5139 C1            [10]  710 	pop	bc
                            711 ;src/systems/hud.c:141: for (i = 0; i < currenthealth; ++i) {
   513A 0C            [ 4]  712 	inc	c
   513B 18 D5         [12]  713 	jr	00103$
   513D                     714 00101$:
                            715 ;src/systems/hud.c:146: scoretemp = currentscore;
   513D 2A 77 64      [16]  716 	ld	hl, (_currentscore)
                            717 ;src/systems/hud.c:147: hud_draw_digits(scoretemp, 4, 24, 2);
   5140 01 18 02      [10]  718 	ld	bc, #0x0218
   5143 C5            [11]  719 	push	bc
   5144 3E 04         [ 7]  720 	ld	a, #0x04
   5146 F5            [11]  721 	push	af
   5147 33            [ 6]  722 	inc	sp
   5148 E5            [11]  723 	push	hl
   5149 CD 1C 50      [17]  724 	call	_hud_draw_digits
   514C F1            [10]  725 	pop	af
   514D F1            [10]  726 	pop	af
   514E 33            [ 6]  727 	inc	sp
                            728 ;src/systems/hud.c:149: timetemp = currenttime;
   514F 21 79 64      [10]  729 	ld	hl,#_currenttime + 0
   5152 4E            [ 7]  730 	ld	c, (hl)
                            731 ;src/systems/hud.c:150: hud_draw_digits((u16)timetemp, 3, 56, 2);
   5153 06 00         [ 7]  732 	ld	b, #0x00
   5155 21 38 02      [10]  733 	ld	hl, #0x0238
   5158 E5            [11]  734 	push	hl
   5159 3E 03         [ 7]  735 	ld	a, #0x03
   515B F5            [11]  736 	push	af
   515C 33            [ 6]  737 	inc	sp
   515D C5            [11]  738 	push	bc
   515E CD 1C 50      [17]  739 	call	_hud_draw_digits
   5161 F1            [10]  740 	pop	af
                            741 ;src/systems/hud.c:152: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
   5162 33            [ 6]  742 	inc	sp
   5163 21 02 B4      [10]  743 	ld	hl,#0xb402
   5166 E3            [19]  744 	ex	(sp),hl
   5167 21 00 C0      [10]  745 	ld	hl, #0xc000
   516A E5            [11]  746 	push	hl
   516B CD A5 63      [17]  747 	call	_cpct_getScreenPtr
                            748 ;src/systems/hud.c:153: cpct_drawSprite((u8*)hudlives, pvmem, 4, 8);
   516E 01 BC 4E      [10]  749 	ld	bc, #_hudlives+0
   5171 11 04 08      [10]  750 	ld	de, #0x0804
   5174 D5            [11]  751 	push	de
   5175 E5            [11]  752 	push	hl
   5176 C5            [11]  753 	push	bc
   5177 CD D6 61      [17]  754 	call	_cpct_drawSprite
                            755 ;src/systems/hud.c:155: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
   517A 21 0C B4      [10]  756 	ld	hl, #0xb40c
   517D E5            [11]  757 	push	hl
   517E 21 00 C0      [10]  758 	ld	hl, #0xc000
   5181 E5            [11]  759 	push	hl
   5182 CD A5 63      [17]  760 	call	_cpct_getScreenPtr
                            761 ;src/systems/hud.c:156: cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 4, 8);
   5185 E5            [11]  762 	push	hl
   5186 3E 0A         [ 7]  763 	ld	a, #0x0a
   5188 F5            [11]  764 	push	af
   5189 33            [ 6]  765 	inc	sp
   518A 3A 7A 64      [13]  766 	ld	a, (_currentlives)
   518D F5            [11]  767 	push	af
   518E 33            [ 6]  768 	inc	sp
   518F CD 7B 62      [17]  769 	call	__moduchar
   5192 F1            [10]  770 	pop	af
   5193 55            [ 4]  771 	ld	d, l
   5194 D5            [11]  772 	push	de
   5195 33            [ 6]  773 	inc	sp
   5196 CD 5B 4E      [17]  774 	call	_hud_get_number_sprite
   5199 33            [ 6]  775 	inc	sp
   519A C1            [10]  776 	pop	bc
   519B 11 04 08      [10]  777 	ld	de, #0x0804
   519E D5            [11]  778 	push	de
   519F C5            [11]  779 	push	bc
   51A0 E5            [11]  780 	push	hl
   51A1 CD D6 61      [17]  781 	call	_cpct_drawSprite
                            782 ;src/systems/hud.c:158: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
   51A4 21 46 B4      [10]  783 	ld	hl, #0xb446
   51A7 E5            [11]  784 	push	hl
   51A8 21 00 C0      [10]  785 	ld	hl, #0xc000
   51AB E5            [11]  786 	push	hl
   51AC CD A5 63      [17]  787 	call	_cpct_getScreenPtr
                            788 ;src/systems/hud.c:159: cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 4, 8);
   51AF E5            [11]  789 	push	hl
   51B0 3E 0A         [ 7]  790 	ld	a, #0x0a
   51B2 F5            [11]  791 	push	af
   51B3 33            [ 6]  792 	inc	sp
   51B4 3A 7B 64      [13]  793 	ld	a, (_currentweapon)
   51B7 F5            [11]  794 	push	af
   51B8 33            [ 6]  795 	inc	sp
   51B9 CD 7B 62      [17]  796 	call	__moduchar
   51BC F1            [10]  797 	pop	af
   51BD 55            [ 4]  798 	ld	d, l
   51BE D5            [11]  799 	push	de
   51BF 33            [ 6]  800 	inc	sp
   51C0 CD 5B 4E      [17]  801 	call	_hud_get_number_sprite
   51C3 33            [ 6]  802 	inc	sp
   51C4 C1            [10]  803 	pop	bc
   51C5 11 04 08      [10]  804 	ld	de, #0x0804
   51C8 D5            [11]  805 	push	de
   51C9 C5            [11]  806 	push	bc
   51CA E5            [11]  807 	push	hl
   51CB CD D6 61      [17]  808 	call	_cpct_drawSprite
   51CE C9            [10]  809 	ret
                            810 	.area _CODE
                            811 	.area _INITIALIZER
                            812 	.area _CABS (ABS)
