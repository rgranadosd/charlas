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
   6804                      29 _ginputleft:
   6804                      30 	.ds 1
   6805                      31 _ginputright:
   6805                      32 	.ds 1
   6806                      33 _ginputup:
   6806                      34 	.ds 1
   6807                      35 _ginputdown:
   6807                      36 	.ds 1
   6808                      37 _ginputshoot:
   6808                      38 	.ds 1
   6809                      39 _gprevjump:
   6809                      40 	.ds 1
   680A                      41 _gprevshoot:
   680A                      42 	.ds 1
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
   50B5                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   50B5 3A 06 68      [13]   73 	ld	a,(#_ginputup + 0)
   50B8 32 09 68      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   50BB 3A 08 68      [13]   76 	ld	a,(#_ginputshoot + 0)
   50BE 32 0A 68      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   50C1 CD D1 64      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   50C4 21 01 01      [10]   81 	ld	hl, #0x0101
   50C7 CD C5 64      [17]   82 	call	_cpct_isKeyPressed
   50CA FD 21 04 68   [14]   83 	ld	iy, #_ginputleft
   50CE FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   50D1 21 00 02      [10]   86 	ld	hl, #0x0200
   50D4 CD C5 64      [17]   87 	call	_cpct_isKeyPressed
   50D7 FD 21 05 68   [14]   88 	ld	iy, #_ginputright
   50DB FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   50DE 21 00 01      [10]   91 	ld	hl, #0x0100
   50E1 CD C5 64      [17]   92 	call	_cpct_isKeyPressed
   50E4 FD 21 06 68   [14]   93 	ld	iy, #_ginputup
   50E8 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   50EB 21 07 80      [10]   96 	ld	hl, #0x8007
   50EE CD C5 64      [17]   97 	call	_cpct_isKeyPressed
   50F1 FD 21 07 68   [14]   98 	ld	iy, #_ginputdown
   50F5 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   50F8 21 00 04      [10]  101 	ld	hl, #0x0400
   50FB CD C5 64      [17]  102 	call	_cpct_isKeyPressed
   50FE FD 21 08 68   [14]  103 	ld	iy, #_ginputshoot
   5102 FD 75 00      [19]  104 	ld	0 (iy), l
   5105 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   5106                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   5106 FD 21 04 68   [14]  112 	ld	iy, #_ginputleft
   510A FD 6E 00      [19]  113 	ld	l, 0 (iy)
   510D C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   510E                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   510E FD 21 05 68   [14]  121 	ld	iy, #_ginputright
   5112 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   5115 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   5116                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   5116 FD 21 06 68   [14]  130 	ld	iy, #_ginputup
   511A FD 6E 00      [19]  131 	ld	l, 0 (iy)
   511D C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   511E                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   511E FD 21 07 68   [14]  139 	ld	iy, #_ginputdown
   5122 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   5125 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   5126                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   5126 FD 21 06 68   [14]  148 	ld	iy, #_ginputup
   512A FD 6E 00      [19]  149 	ld	l, 0 (iy)
   512D C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   512E                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   512E 3A 06 68      [13]  157 	ld	a,(#_ginputup + 0)
   5131 B7            [ 4]  158 	or	a, a
   5132 28 06         [12]  159 	jr	Z,00103$
   5134 3A 09 68      [13]  160 	ld	a,(#_gprevjump + 0)
   5137 B7            [ 4]  161 	or	a, a
   5138 28 03         [12]  162 	jr	Z,00104$
   513A                     163 00103$:
   513A 2E 00         [ 7]  164 	ld	l, #0x00
   513C C9            [10]  165 	ret
   513D                     166 00104$:
   513D 2E 01         [ 7]  167 	ld	l, #0x01
   513F C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   5140                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   5140 FD 21 08 68   [14]  175 	ld	iy, #_ginputshoot
   5144 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   5147 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   5148                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   5148 3A 08 68      [13]  184 	ld	a,(#_ginputshoot + 0)
   514B B7            [ 4]  185 	or	a, a
   514C 28 06         [12]  186 	jr	Z,00103$
   514E 3A 0A 68      [13]  187 	ld	a,(#_gprevshoot + 0)
   5151 B7            [ 4]  188 	or	a, a
   5152 28 03         [12]  189 	jr	Z,00104$
   5154                     190 00103$:
   5154 2E 00         [ 7]  191 	ld	l, #0x00
   5156 C9            [10]  192 	ret
   5157                     193 00104$:
   5157 2E 01         [ 7]  194 	ld	l, #0x01
   5159 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
