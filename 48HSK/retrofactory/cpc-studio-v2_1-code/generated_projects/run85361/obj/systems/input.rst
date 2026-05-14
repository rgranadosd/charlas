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
   5D77                      29 _ginputleft:
   5D77                      30 	.ds 1
   5D78                      31 _ginputright:
   5D78                      32 	.ds 1
   5D79                      33 _ginputup:
   5D79                      34 	.ds 1
   5D7A                      35 _ginputdown:
   5D7A                      36 	.ds 1
   5D7B                      37 _ginputshoot:
   5D7B                      38 	.ds 1
   5D7C                      39 _gprevjump:
   5D7C                      40 	.ds 1
   5D7D                      41 _gprevshoot:
   5D7D                      42 	.ds 1
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
   4DF5                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   4DF5 3A 79 5D      [13]   73 	ld	a,(#_ginputup + 0)
   4DF8 32 7C 5D      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   4DFB 3A 7B 5D      [13]   76 	ld	a,(#_ginputshoot + 0)
   4DFE 32 7D 5D      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   4E01 CD 96 5A      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4E04 21 01 01      [10]   81 	ld	hl, #0x0101
   4E07 CD 8A 5A      [17]   82 	call	_cpct_isKeyPressed
   4E0A FD 21 77 5D   [14]   83 	ld	iy, #_ginputleft
   4E0E FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4E11 21 00 02      [10]   86 	ld	hl, #0x0200
   4E14 CD 8A 5A      [17]   87 	call	_cpct_isKeyPressed
   4E17 FD 21 78 5D   [14]   88 	ld	iy, #_ginputright
   4E1B FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   4E1E 21 00 01      [10]   91 	ld	hl, #0x0100
   4E21 CD 8A 5A      [17]   92 	call	_cpct_isKeyPressed
   4E24 FD 21 79 5D   [14]   93 	ld	iy, #_ginputup
   4E28 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   4E2B 21 07 80      [10]   96 	ld	hl, #0x8007
   4E2E CD 8A 5A      [17]   97 	call	_cpct_isKeyPressed
   4E31 FD 21 7A 5D   [14]   98 	ld	iy, #_ginputdown
   4E35 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   4E38 21 00 04      [10]  101 	ld	hl, #0x0400
   4E3B CD 8A 5A      [17]  102 	call	_cpct_isKeyPressed
   4E3E FD 21 7B 5D   [14]  103 	ld	iy, #_ginputshoot
   4E42 FD 75 00      [19]  104 	ld	0 (iy), l
   4E45 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   4E46                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   4E46 FD 21 77 5D   [14]  112 	ld	iy, #_ginputleft
   4E4A FD 6E 00      [19]  113 	ld	l, 0 (iy)
   4E4D C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   4E4E                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   4E4E FD 21 78 5D   [14]  121 	ld	iy, #_ginputright
   4E52 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   4E55 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   4E56                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   4E56 FD 21 79 5D   [14]  130 	ld	iy, #_ginputup
   4E5A FD 6E 00      [19]  131 	ld	l, 0 (iy)
   4E5D C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   4E5E                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   4E5E FD 21 7A 5D   [14]  139 	ld	iy, #_ginputdown
   4E62 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   4E65 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   4E66                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   4E66 FD 21 79 5D   [14]  148 	ld	iy, #_ginputup
   4E6A FD 6E 00      [19]  149 	ld	l, 0 (iy)
   4E6D C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   4E6E                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   4E6E 3A 79 5D      [13]  157 	ld	a,(#_ginputup + 0)
   4E71 B7            [ 4]  158 	or	a, a
   4E72 28 06         [12]  159 	jr	Z,00103$
   4E74 3A 7C 5D      [13]  160 	ld	a,(#_gprevjump + 0)
   4E77 B7            [ 4]  161 	or	a, a
   4E78 28 03         [12]  162 	jr	Z,00104$
   4E7A                     163 00103$:
   4E7A 2E 00         [ 7]  164 	ld	l, #0x00
   4E7C C9            [10]  165 	ret
   4E7D                     166 00104$:
   4E7D 2E 01         [ 7]  167 	ld	l, #0x01
   4E7F C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   4E80                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   4E80 FD 21 7B 5D   [14]  175 	ld	iy, #_ginputshoot
   4E84 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   4E87 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   4E88                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   4E88 3A 7B 5D      [13]  184 	ld	a,(#_ginputshoot + 0)
   4E8B B7            [ 4]  185 	or	a, a
   4E8C 28 06         [12]  186 	jr	Z,00103$
   4E8E 3A 7D 5D      [13]  187 	ld	a,(#_gprevshoot + 0)
   4E91 B7            [ 4]  188 	or	a, a
   4E92 28 03         [12]  189 	jr	Z,00104$
   4E94                     190 00103$:
   4E94 2E 00         [ 7]  191 	ld	l, #0x00
   4E96 C9            [10]  192 	ret
   4E97                     193 00104$:
   4E97 2E 01         [ 7]  194 	ld	l, #0x01
   4E99 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
