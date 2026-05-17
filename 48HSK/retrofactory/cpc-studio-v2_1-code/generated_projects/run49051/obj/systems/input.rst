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
   6492                      29 _ginputleft:
   6492                      30 	.ds 1
   6493                      31 _ginputright:
   6493                      32 	.ds 1
   6494                      33 _ginputup:
   6494                      34 	.ds 1
   6495                      35 _ginputdown:
   6495                      36 	.ds 1
   6496                      37 _ginputshoot:
   6496                      38 	.ds 1
   6497                      39 _gprevjump:
   6497                      40 	.ds 1
   6498                      41 _gprevshoot:
   6498                      42 	.ds 1
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
   51CF                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   51CF 3A 94 64      [13]   73 	ld	a,(#_ginputup + 0)
   51D2 32 97 64      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   51D5 3A 96 64      [13]   76 	ld	a,(#_ginputshoot + 0)
   51D8 32 98 64      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   51DB CD 5F 61      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   51DE 21 01 01      [10]   81 	ld	hl, #0x0101
   51E1 CD 53 61      [17]   82 	call	_cpct_isKeyPressed
   51E4 FD 21 92 64   [14]   83 	ld	iy, #_ginputleft
   51E8 FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   51EB 21 00 02      [10]   86 	ld	hl, #0x0200
   51EE CD 53 61      [17]   87 	call	_cpct_isKeyPressed
   51F1 FD 21 93 64   [14]   88 	ld	iy, #_ginputright
   51F5 FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   51F8 21 00 01      [10]   91 	ld	hl, #0x0100
   51FB CD 53 61      [17]   92 	call	_cpct_isKeyPressed
   51FE FD 21 94 64   [14]   93 	ld	iy, #_ginputup
   5202 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   5205 21 07 80      [10]   96 	ld	hl, #0x8007
   5208 CD 53 61      [17]   97 	call	_cpct_isKeyPressed
   520B FD 21 95 64   [14]   98 	ld	iy, #_ginputdown
   520F FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   5212 21 00 04      [10]  101 	ld	hl, #0x0400
   5215 CD 53 61      [17]  102 	call	_cpct_isKeyPressed
   5218 FD 21 96 64   [14]  103 	ld	iy, #_ginputshoot
   521C FD 75 00      [19]  104 	ld	0 (iy), l
   521F C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   5220                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   5220 FD 21 92 64   [14]  112 	ld	iy, #_ginputleft
   5224 FD 6E 00      [19]  113 	ld	l, 0 (iy)
   5227 C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   5228                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   5228 FD 21 93 64   [14]  121 	ld	iy, #_ginputright
   522C FD 6E 00      [19]  122 	ld	l, 0 (iy)
   522F C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   5230                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   5230 FD 21 94 64   [14]  130 	ld	iy, #_ginputup
   5234 FD 6E 00      [19]  131 	ld	l, 0 (iy)
   5237 C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   5238                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   5238 FD 21 95 64   [14]  139 	ld	iy, #_ginputdown
   523C FD 6E 00      [19]  140 	ld	l, 0 (iy)
   523F C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   5240                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   5240 FD 21 94 64   [14]  148 	ld	iy, #_ginputup
   5244 FD 6E 00      [19]  149 	ld	l, 0 (iy)
   5247 C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   5248                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   5248 3A 94 64      [13]  157 	ld	a,(#_ginputup + 0)
   524B B7            [ 4]  158 	or	a, a
   524C 28 06         [12]  159 	jr	Z,00103$
   524E 3A 97 64      [13]  160 	ld	a,(#_gprevjump + 0)
   5251 B7            [ 4]  161 	or	a, a
   5252 28 03         [12]  162 	jr	Z,00104$
   5254                     163 00103$:
   5254 2E 00         [ 7]  164 	ld	l, #0x00
   5256 C9            [10]  165 	ret
   5257                     166 00104$:
   5257 2E 01         [ 7]  167 	ld	l, #0x01
   5259 C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   525A                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   525A FD 21 96 64   [14]  175 	ld	iy, #_ginputshoot
   525E FD 6E 00      [19]  176 	ld	l, 0 (iy)
   5261 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   5262                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   5262 3A 96 64      [13]  184 	ld	a,(#_ginputshoot + 0)
   5265 B7            [ 4]  185 	or	a, a
   5266 28 06         [12]  186 	jr	Z,00103$
   5268 3A 98 64      [13]  187 	ld	a,(#_gprevshoot + 0)
   526B B7            [ 4]  188 	or	a, a
   526C 28 03         [12]  189 	jr	Z,00104$
   526E                     190 00103$:
   526E 2E 00         [ 7]  191 	ld	l, #0x00
   5270 C9            [10]  192 	ret
   5271                     193 00104$:
   5271 2E 01         [ 7]  194 	ld	l, #0x01
   5273 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
