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
   5E40                      29 _ginputleft:
   5E40                      30 	.ds 1
   5E41                      31 _ginputright:
   5E41                      32 	.ds 1
   5E42                      33 _ginputup:
   5E42                      34 	.ds 1
   5E43                      35 _ginputdown:
   5E43                      36 	.ds 1
   5E44                      37 _ginputshoot:
   5E44                      38 	.ds 1
   5E45                      39 _gprevjump:
   5E45                      40 	.ds 1
   5E46                      41 _gprevshoot:
   5E46                      42 	.ds 1
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
   4E3F                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   4E3F 3A 42 5E      [13]   73 	ld	a,(#_ginputup + 0)
   4E42 32 45 5E      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   4E45 3A 44 5E      [13]   76 	ld	a,(#_ginputshoot + 0)
   4E48 32 46 5E      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   4E4B CD 5F 5B      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4E4E 21 01 01      [10]   81 	ld	hl, #0x0101
   4E51 CD 53 5B      [17]   82 	call	_cpct_isKeyPressed
   4E54 FD 21 40 5E   [14]   83 	ld	iy, #_ginputleft
   4E58 FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4E5B 21 00 02      [10]   86 	ld	hl, #0x0200
   4E5E CD 53 5B      [17]   87 	call	_cpct_isKeyPressed
   4E61 FD 21 41 5E   [14]   88 	ld	iy, #_ginputright
   4E65 FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   4E68 21 00 01      [10]   91 	ld	hl, #0x0100
   4E6B CD 53 5B      [17]   92 	call	_cpct_isKeyPressed
   4E6E FD 21 42 5E   [14]   93 	ld	iy, #_ginputup
   4E72 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   4E75 21 07 80      [10]   96 	ld	hl, #0x8007
   4E78 CD 53 5B      [17]   97 	call	_cpct_isKeyPressed
   4E7B FD 21 43 5E   [14]   98 	ld	iy, #_ginputdown
   4E7F FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   4E82 21 00 04      [10]  101 	ld	hl, #0x0400
   4E85 CD 53 5B      [17]  102 	call	_cpct_isKeyPressed
   4E88 FD 21 44 5E   [14]  103 	ld	iy, #_ginputshoot
   4E8C FD 75 00      [19]  104 	ld	0 (iy), l
   4E8F C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   4E90                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   4E90 FD 21 40 5E   [14]  112 	ld	iy, #_ginputleft
   4E94 FD 6E 00      [19]  113 	ld	l, 0 (iy)
   4E97 C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   4E98                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   4E98 FD 21 41 5E   [14]  121 	ld	iy, #_ginputright
   4E9C FD 6E 00      [19]  122 	ld	l, 0 (iy)
   4E9F C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   4EA0                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   4EA0 FD 21 42 5E   [14]  130 	ld	iy, #_ginputup
   4EA4 FD 6E 00      [19]  131 	ld	l, 0 (iy)
   4EA7 C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   4EA8                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   4EA8 FD 21 43 5E   [14]  139 	ld	iy, #_ginputdown
   4EAC FD 6E 00      [19]  140 	ld	l, 0 (iy)
   4EAF C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   4EB0                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   4EB0 FD 21 42 5E   [14]  148 	ld	iy, #_ginputup
   4EB4 FD 6E 00      [19]  149 	ld	l, 0 (iy)
   4EB7 C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   4EB8                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   4EB8 3A 42 5E      [13]  157 	ld	a,(#_ginputup + 0)
   4EBB B7            [ 4]  158 	or	a, a
   4EBC 28 06         [12]  159 	jr	Z,00103$
   4EBE 3A 45 5E      [13]  160 	ld	a,(#_gprevjump + 0)
   4EC1 B7            [ 4]  161 	or	a, a
   4EC2 28 03         [12]  162 	jr	Z,00104$
   4EC4                     163 00103$:
   4EC4 2E 00         [ 7]  164 	ld	l, #0x00
   4EC6 C9            [10]  165 	ret
   4EC7                     166 00104$:
   4EC7 2E 01         [ 7]  167 	ld	l, #0x01
   4EC9 C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   4ECA                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   4ECA FD 21 44 5E   [14]  175 	ld	iy, #_ginputshoot
   4ECE FD 6E 00      [19]  176 	ld	l, 0 (iy)
   4ED1 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   4ED2                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   4ED2 3A 44 5E      [13]  184 	ld	a,(#_ginputshoot + 0)
   4ED5 B7            [ 4]  185 	or	a, a
   4ED6 28 06         [12]  186 	jr	Z,00103$
   4ED8 3A 46 5E      [13]  187 	ld	a,(#_gprevshoot + 0)
   4EDB B7            [ 4]  188 	or	a, a
   4EDC 28 03         [12]  189 	jr	Z,00104$
   4EDE                     190 00103$:
   4EDE 2E 00         [ 7]  191 	ld	l, #0x00
   4EE0 C9            [10]  192 	ret
   4EE1                     193 00104$:
   4EE1 2E 01         [ 7]  194 	ld	l, #0x01
   4EE3 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
