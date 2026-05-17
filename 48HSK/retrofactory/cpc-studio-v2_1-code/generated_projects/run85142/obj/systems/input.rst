                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module input
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _cpct_isKeyPressed
                             12 	.globl _cpct_scanKeyboard_f
                             13 	.globl _input_update
                             14 	.globl _input_is_left_pressed
                             15 	.globl _input_is_right_pressed
                             16 	.globl _input_is_up_pressed
                             17 	.globl _input_is_down_pressed
                             18 	.globl _input_is_jump_pressed
                             19 	.globl _input_is_jump_just_pressed
                             20 	.globl _input_is_shoot_pressed
                             21 	.globl _input_is_shoot_just_pressed
                             22 ;--------------------------------------------------------
                             23 ; special function registers
                             24 ;--------------------------------------------------------
                             25 ;--------------------------------------------------------
                             26 ; ram data
                             27 ;--------------------------------------------------------
                             28 	.area _DATA
   667C                      29 _ginputleft:
   667C                      30 	.ds 1
   667D                      31 _ginputright:
   667D                      32 	.ds 1
   667E                      33 _ginputup:
   667E                      34 	.ds 1
   667F                      35 _ginputdown:
   667F                      36 	.ds 1
   6680                      37 _ginputshoot:
   6680                      38 	.ds 1
   6681                      39 _gprevjump:
   6681                      40 	.ds 1
   6682                      41 _gprevshoot:
   6682                      42 	.ds 1
                             43 ;--------------------------------------------------------
                             44 ; ram data
                             45 ;--------------------------------------------------------
                             46 	.area _INITIALIZED
                             47 ;--------------------------------------------------------
                             48 ; absolute external ram data
                             49 ;--------------------------------------------------------
                             50 	.area _DABS (ABS)
                             51 ;--------------------------------------------------------
                             52 ; global & static initialisations
                             53 ;--------------------------------------------------------
                             54 	.area _HOME
                             55 	.area _GSINIT
                             56 	.area _GSFINAL
                             57 	.area _GSINIT
                             58 ;--------------------------------------------------------
                             59 ; Home
                             60 ;--------------------------------------------------------
                             61 	.area _HOME
                             62 	.area _HOME
                             63 ;--------------------------------------------------------
                             64 ; code
                             65 ;--------------------------------------------------------
                             66 	.area _CODE
                             67 ;src/systems/input.c:11: void input_update(void) {
                             68 ;	---------------------------------
                             69 ; Function input_update
                             70 ; ---------------------------------
   5239                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   5239 3A 7E 66      [13]   73 	ld	a,(#_ginputup + 0)
   523C 32 81 66      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   523F 3A 80 66      [13]   76 	ld	a,(#_ginputshoot + 0)
   5242 32 82 66      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   5245 CD 49 63      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   5248 21 01 01      [10]   81 	ld	hl, #0x0101
   524B CD 3D 63      [17]   82 	call	_cpct_isKeyPressed
   524E FD 21 7C 66   [14]   83 	ld	iy, #_ginputleft
   5252 FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   5255 21 00 02      [10]   86 	ld	hl, #0x0200
   5258 CD 3D 63      [17]   87 	call	_cpct_isKeyPressed
   525B FD 21 7D 66   [14]   88 	ld	iy, #_ginputright
   525F FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   5262 21 00 01      [10]   91 	ld	hl, #0x0100
   5265 CD 3D 63      [17]   92 	call	_cpct_isKeyPressed
   5268 FD 21 7E 66   [14]   93 	ld	iy, #_ginputup
   526C FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   526F 21 07 80      [10]   96 	ld	hl, #0x8007
   5272 CD 3D 63      [17]   97 	call	_cpct_isKeyPressed
   5275 FD 21 7F 66   [14]   98 	ld	iy, #_ginputdown
   5279 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   527C 21 00 04      [10]  101 	ld	hl, #0x0400
   527F CD 3D 63      [17]  102 	call	_cpct_isKeyPressed
   5282 FD 21 80 66   [14]  103 	ld	iy, #_ginputshoot
   5286 FD 75 00      [19]  104 	ld	0 (iy), l
   5289 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   528A                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   528A FD 21 7C 66   [14]  112 	ld	iy, #_ginputleft
   528E FD 6E 00      [19]  113 	ld	l, 0 (iy)
   5291 C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   5292                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   5292 FD 21 7D 66   [14]  121 	ld	iy, #_ginputright
   5296 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   5299 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   529A                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   529A FD 21 7E 66   [14]  130 	ld	iy, #_ginputup
   529E FD 6E 00      [19]  131 	ld	l, 0 (iy)
   52A1 C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   52A2                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   52A2 FD 21 7F 66   [14]  139 	ld	iy, #_ginputdown
   52A6 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   52A9 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   52AA                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   52AA FD 21 7E 66   [14]  148 	ld	iy, #_ginputup
   52AE FD 6E 00      [19]  149 	ld	l, 0 (iy)
   52B1 C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   52B2                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   52B2 3A 7E 66      [13]  157 	ld	a,(#_ginputup + 0)
   52B5 B7            [ 4]  158 	or	a, a
   52B6 28 06         [12]  159 	jr	Z,00103$
   52B8 3A 81 66      [13]  160 	ld	a,(#_gprevjump + 0)
   52BB B7            [ 4]  161 	or	a, a
   52BC 28 03         [12]  162 	jr	Z,00104$
   52BE                     163 00103$:
   52BE 2E 00         [ 7]  164 	ld	l, #0x00
   52C0 C9            [10]  165 	ret
   52C1                     166 00104$:
   52C1 2E 01         [ 7]  167 	ld	l, #0x01
   52C3 C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   52C4                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   52C4 FD 21 80 66   [14]  175 	ld	iy, #_ginputshoot
   52C8 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   52CB C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   52CC                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   52CC 3A 80 66      [13]  184 	ld	a,(#_ginputshoot + 0)
   52CF B7            [ 4]  185 	or	a, a
   52D0 28 06         [12]  186 	jr	Z,00103$
   52D2 3A 82 66      [13]  187 	ld	a,(#_gprevshoot + 0)
   52D5 B7            [ 4]  188 	or	a, a
   52D6 28 03         [12]  189 	jr	Z,00104$
   52D8                     190 00103$:
   52D8 2E 00         [ 7]  191 	ld	l, #0x00
   52DA C9            [10]  192 	ret
   52DB                     193 00104$:
   52DB 2E 01         [ 7]  194 	ld	l, #0x01
   52DD C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
