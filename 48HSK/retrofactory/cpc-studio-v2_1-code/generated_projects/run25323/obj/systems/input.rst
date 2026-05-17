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
   637E                      29 _ginputleft:
   637E                      30 	.ds 1
   637F                      31 _ginputright:
   637F                      32 	.ds 1
   6380                      33 _ginputup:
   6380                      34 	.ds 1
   6381                      35 _ginputdown:
   6381                      36 	.ds 1
   6382                      37 _ginputshoot:
   6382                      38 	.ds 1
   6383                      39 _gprevjump:
   6383                      40 	.ds 1
   6384                      41 _gprevshoot:
   6384                      42 	.ds 1
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
   5097                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   5097 3A 80 63      [13]   73 	ld	a,(#_ginputup + 0)
   509A 32 83 63      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   509D 3A 82 63      [13]   76 	ld	a,(#_ginputshoot + 0)
   50A0 32 84 63      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   50A3 CD 4B 60      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   50A6 21 01 01      [10]   81 	ld	hl, #0x0101
   50A9 CD 3F 60      [17]   82 	call	_cpct_isKeyPressed
   50AC FD 21 7E 63   [14]   83 	ld	iy, #_ginputleft
   50B0 FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   50B3 21 00 02      [10]   86 	ld	hl, #0x0200
   50B6 CD 3F 60      [17]   87 	call	_cpct_isKeyPressed
   50B9 FD 21 7F 63   [14]   88 	ld	iy, #_ginputright
   50BD FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   50C0 21 00 01      [10]   91 	ld	hl, #0x0100
   50C3 CD 3F 60      [17]   92 	call	_cpct_isKeyPressed
   50C6 FD 21 80 63   [14]   93 	ld	iy, #_ginputup
   50CA FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   50CD 21 07 80      [10]   96 	ld	hl, #0x8007
   50D0 CD 3F 60      [17]   97 	call	_cpct_isKeyPressed
   50D3 FD 21 81 63   [14]   98 	ld	iy, #_ginputdown
   50D7 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   50DA 21 00 04      [10]  101 	ld	hl, #0x0400
   50DD CD 3F 60      [17]  102 	call	_cpct_isKeyPressed
   50E0 FD 21 82 63   [14]  103 	ld	iy, #_ginputshoot
   50E4 FD 75 00      [19]  104 	ld	0 (iy), l
   50E7 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   50E8                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   50E8 FD 21 7E 63   [14]  112 	ld	iy, #_ginputleft
   50EC FD 6E 00      [19]  113 	ld	l, 0 (iy)
   50EF C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   50F0                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   50F0 FD 21 7F 63   [14]  121 	ld	iy, #_ginputright
   50F4 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   50F7 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   50F8                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   50F8 FD 21 80 63   [14]  130 	ld	iy, #_ginputup
   50FC FD 6E 00      [19]  131 	ld	l, 0 (iy)
   50FF C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   5100                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   5100 FD 21 81 63   [14]  139 	ld	iy, #_ginputdown
   5104 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   5107 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   5108                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   5108 FD 21 80 63   [14]  148 	ld	iy, #_ginputup
   510C FD 6E 00      [19]  149 	ld	l, 0 (iy)
   510F C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   5110                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   5110 3A 80 63      [13]  157 	ld	a,(#_ginputup + 0)
   5113 B7            [ 4]  158 	or	a, a
   5114 28 06         [12]  159 	jr	Z,00103$
   5116 3A 83 63      [13]  160 	ld	a,(#_gprevjump + 0)
   5119 B7            [ 4]  161 	or	a, a
   511A 28 03         [12]  162 	jr	Z,00104$
   511C                     163 00103$:
   511C 2E 00         [ 7]  164 	ld	l, #0x00
   511E C9            [10]  165 	ret
   511F                     166 00104$:
   511F 2E 01         [ 7]  167 	ld	l, #0x01
   5121 C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   5122                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   5122 FD 21 82 63   [14]  175 	ld	iy, #_ginputshoot
   5126 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   5129 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   512A                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   512A 3A 82 63      [13]  184 	ld	a,(#_ginputshoot + 0)
   512D B7            [ 4]  185 	or	a, a
   512E 28 06         [12]  186 	jr	Z,00103$
   5130 3A 84 63      [13]  187 	ld	a,(#_gprevshoot + 0)
   5133 B7            [ 4]  188 	or	a, a
   5134 28 03         [12]  189 	jr	Z,00104$
   5136                     190 00103$:
   5136 2E 00         [ 7]  191 	ld	l, #0x00
   5138 C9            [10]  192 	ret
   5139                     193 00104$:
   5139 2E 01         [ 7]  194 	ld	l, #0x01
   513B C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
