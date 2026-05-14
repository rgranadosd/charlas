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
   5F28                      29 _ginputleft:
   5F28                      30 	.ds 1
   5F29                      31 _ginputright:
   5F29                      32 	.ds 1
   5F2A                      33 _ginputup:
   5F2A                      34 	.ds 1
   5F2B                      35 _ginputdown:
   5F2B                      36 	.ds 1
   5F2C                      37 _ginputshoot:
   5F2C                      38 	.ds 1
   5F2D                      39 _gprevjump:
   5F2D                      40 	.ds 1
   5F2E                      41 _gprevshoot:
   5F2E                      42 	.ds 1
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
   4F1A                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   4F1A 3A 2A 5F      [13]   73 	ld	a,(#_ginputup + 0)
   4F1D 32 2D 5F      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   4F20 3A 2C 5F      [13]   76 	ld	a,(#_ginputshoot + 0)
   4F23 32 2E 5F      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   4F26 CD 45 5C      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4F29 21 01 01      [10]   81 	ld	hl, #0x0101
   4F2C CD 39 5C      [17]   82 	call	_cpct_isKeyPressed
   4F2F FD 21 28 5F   [14]   83 	ld	iy, #_ginputleft
   4F33 FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4F36 21 00 02      [10]   86 	ld	hl, #0x0200
   4F39 CD 39 5C      [17]   87 	call	_cpct_isKeyPressed
   4F3C FD 21 29 5F   [14]   88 	ld	iy, #_ginputright
   4F40 FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   4F43 21 00 01      [10]   91 	ld	hl, #0x0100
   4F46 CD 39 5C      [17]   92 	call	_cpct_isKeyPressed
   4F49 FD 21 2A 5F   [14]   93 	ld	iy, #_ginputup
   4F4D FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   4F50 21 07 80      [10]   96 	ld	hl, #0x8007
   4F53 CD 39 5C      [17]   97 	call	_cpct_isKeyPressed
   4F56 FD 21 2B 5F   [14]   98 	ld	iy, #_ginputdown
   4F5A FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   4F5D 21 00 04      [10]  101 	ld	hl, #0x0400
   4F60 CD 39 5C      [17]  102 	call	_cpct_isKeyPressed
   4F63 FD 21 2C 5F   [14]  103 	ld	iy, #_ginputshoot
   4F67 FD 75 00      [19]  104 	ld	0 (iy), l
   4F6A C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   4F6B                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   4F6B FD 21 28 5F   [14]  112 	ld	iy, #_ginputleft
   4F6F FD 6E 00      [19]  113 	ld	l, 0 (iy)
   4F72 C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   4F73                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   4F73 FD 21 29 5F   [14]  121 	ld	iy, #_ginputright
   4F77 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   4F7A C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   4F7B                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   4F7B FD 21 2A 5F   [14]  130 	ld	iy, #_ginputup
   4F7F FD 6E 00      [19]  131 	ld	l, 0 (iy)
   4F82 C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   4F83                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   4F83 FD 21 2B 5F   [14]  139 	ld	iy, #_ginputdown
   4F87 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   4F8A C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   4F8B                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   4F8B FD 21 2A 5F   [14]  148 	ld	iy, #_ginputup
   4F8F FD 6E 00      [19]  149 	ld	l, 0 (iy)
   4F92 C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   4F93                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   4F93 3A 2A 5F      [13]  157 	ld	a,(#_ginputup + 0)
   4F96 B7            [ 4]  158 	or	a, a
   4F97 28 06         [12]  159 	jr	Z,00103$
   4F99 3A 2D 5F      [13]  160 	ld	a,(#_gprevjump + 0)
   4F9C B7            [ 4]  161 	or	a, a
   4F9D 28 03         [12]  162 	jr	Z,00104$
   4F9F                     163 00103$:
   4F9F 2E 00         [ 7]  164 	ld	l, #0x00
   4FA1 C9            [10]  165 	ret
   4FA2                     166 00104$:
   4FA2 2E 01         [ 7]  167 	ld	l, #0x01
   4FA4 C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   4FA5                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   4FA5 FD 21 2C 5F   [14]  175 	ld	iy, #_ginputshoot
   4FA9 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   4FAC C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   4FAD                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   4FAD 3A 2C 5F      [13]  184 	ld	a,(#_ginputshoot + 0)
   4FB0 B7            [ 4]  185 	or	a, a
   4FB1 28 06         [12]  186 	jr	Z,00103$
   4FB3 3A 2E 5F      [13]  187 	ld	a,(#_gprevshoot + 0)
   4FB6 B7            [ 4]  188 	or	a, a
   4FB7 28 03         [12]  189 	jr	Z,00104$
   4FB9                     190 00103$:
   4FB9 2E 00         [ 7]  191 	ld	l, #0x00
   4FBB C9            [10]  192 	ret
   4FBC                     193 00104$:
   4FBC 2E 01         [ 7]  194 	ld	l, #0x01
   4FBE C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
