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
   6418                      29 _ginputleft:
   6418                      30 	.ds 1
   6419                      31 _ginputright:
   6419                      32 	.ds 1
   641A                      33 _ginputup:
   641A                      34 	.ds 1
   641B                      35 _ginputdown:
   641B                      36 	.ds 1
   641C                      37 _ginputshoot:
   641C                      38 	.ds 1
   641D                      39 _gprevjump:
   641D                      40 	.ds 1
   641E                      41 _gprevshoot:
   641E                      42 	.ds 1
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
   5095                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   5095 3A 1A 64      [13]   73 	ld	a,(#_ginputup + 0)
   5098 32 1D 64      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   509B 3A 1C 64      [13]   76 	ld	a,(#_ginputshoot + 0)
   509E 32 1E 64      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   50A1 CD E5 60      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   50A4 21 01 01      [10]   81 	ld	hl, #0x0101
   50A7 CD D9 60      [17]   82 	call	_cpct_isKeyPressed
   50AA FD 21 18 64   [14]   83 	ld	iy, #_ginputleft
   50AE FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   50B1 21 00 02      [10]   86 	ld	hl, #0x0200
   50B4 CD D9 60      [17]   87 	call	_cpct_isKeyPressed
   50B7 FD 21 19 64   [14]   88 	ld	iy, #_ginputright
   50BB FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   50BE 21 00 01      [10]   91 	ld	hl, #0x0100
   50C1 CD D9 60      [17]   92 	call	_cpct_isKeyPressed
   50C4 FD 21 1A 64   [14]   93 	ld	iy, #_ginputup
   50C8 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   50CB 21 07 80      [10]   96 	ld	hl, #0x8007
   50CE CD D9 60      [17]   97 	call	_cpct_isKeyPressed
   50D1 FD 21 1B 64   [14]   98 	ld	iy, #_ginputdown
   50D5 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   50D8 21 00 04      [10]  101 	ld	hl, #0x0400
   50DB CD D9 60      [17]  102 	call	_cpct_isKeyPressed
   50DE FD 21 1C 64   [14]  103 	ld	iy, #_ginputshoot
   50E2 FD 75 00      [19]  104 	ld	0 (iy), l
   50E5 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   50E6                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   50E6 FD 21 18 64   [14]  112 	ld	iy, #_ginputleft
   50EA FD 6E 00      [19]  113 	ld	l, 0 (iy)
   50ED C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   50EE                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   50EE FD 21 19 64   [14]  121 	ld	iy, #_ginputright
   50F2 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   50F5 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   50F6                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   50F6 FD 21 1A 64   [14]  130 	ld	iy, #_ginputup
   50FA FD 6E 00      [19]  131 	ld	l, 0 (iy)
   50FD C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   50FE                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   50FE FD 21 1B 64   [14]  139 	ld	iy, #_ginputdown
   5102 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   5105 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   5106                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   5106 FD 21 1A 64   [14]  148 	ld	iy, #_ginputup
   510A FD 6E 00      [19]  149 	ld	l, 0 (iy)
   510D C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   510E                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   510E 3A 1A 64      [13]  157 	ld	a,(#_ginputup + 0)
   5111 B7            [ 4]  158 	or	a, a
   5112 28 06         [12]  159 	jr	Z,00103$
   5114 3A 1D 64      [13]  160 	ld	a,(#_gprevjump + 0)
   5117 B7            [ 4]  161 	or	a, a
   5118 28 03         [12]  162 	jr	Z,00104$
   511A                     163 00103$:
   511A 2E 00         [ 7]  164 	ld	l, #0x00
   511C C9            [10]  165 	ret
   511D                     166 00104$:
   511D 2E 01         [ 7]  167 	ld	l, #0x01
   511F C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   5120                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   5120 FD 21 1C 64   [14]  175 	ld	iy, #_ginputshoot
   5124 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   5127 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   5128                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   5128 3A 1C 64      [13]  184 	ld	a,(#_ginputshoot + 0)
   512B B7            [ 4]  185 	or	a, a
   512C 28 06         [12]  186 	jr	Z,00103$
   512E 3A 1E 64      [13]  187 	ld	a,(#_gprevshoot + 0)
   5131 B7            [ 4]  188 	or	a, a
   5132 28 03         [12]  189 	jr	Z,00104$
   5134                     190 00103$:
   5134 2E 00         [ 7]  191 	ld	l, #0x00
   5136 C9            [10]  192 	ret
   5137                     193 00104$:
   5137 2E 01         [ 7]  194 	ld	l, #0x01
   5139 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
