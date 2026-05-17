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
   67AD                      29 _ginputleft:
   67AD                      30 	.ds 1
   67AE                      31 _ginputright:
   67AE                      32 	.ds 1
   67AF                      33 _ginputup:
   67AF                      34 	.ds 1
   67B0                      35 _ginputdown:
   67B0                      36 	.ds 1
   67B1                      37 _ginputshoot:
   67B1                      38 	.ds 1
   67B2                      39 _gprevjump:
   67B2                      40 	.ds 1
   67B3                      41 _gprevshoot:
   67B3                      42 	.ds 1
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
   523B                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   523B 3A AF 67      [13]   73 	ld	a,(#_ginputup + 0)
   523E 32 B2 67      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   5241 3A B1 67      [13]   76 	ld	a,(#_ginputshoot + 0)
   5244 32 B3 67      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   5247 CD 7A 64      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   524A 21 01 01      [10]   81 	ld	hl, #0x0101
   524D CD 6E 64      [17]   82 	call	_cpct_isKeyPressed
   5250 FD 21 AD 67   [14]   83 	ld	iy, #_ginputleft
   5254 FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   5257 21 00 02      [10]   86 	ld	hl, #0x0200
   525A CD 6E 64      [17]   87 	call	_cpct_isKeyPressed
   525D FD 21 AE 67   [14]   88 	ld	iy, #_ginputright
   5261 FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   5264 21 00 01      [10]   91 	ld	hl, #0x0100
   5267 CD 6E 64      [17]   92 	call	_cpct_isKeyPressed
   526A FD 21 AF 67   [14]   93 	ld	iy, #_ginputup
   526E FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   5271 21 07 80      [10]   96 	ld	hl, #0x8007
   5274 CD 6E 64      [17]   97 	call	_cpct_isKeyPressed
   5277 FD 21 B0 67   [14]   98 	ld	iy, #_ginputdown
   527B FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   527E 21 00 04      [10]  101 	ld	hl, #0x0400
   5281 CD 6E 64      [17]  102 	call	_cpct_isKeyPressed
   5284 FD 21 B1 67   [14]  103 	ld	iy, #_ginputshoot
   5288 FD 75 00      [19]  104 	ld	0 (iy), l
   528B C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   528C                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   528C FD 21 AD 67   [14]  112 	ld	iy, #_ginputleft
   5290 FD 6E 00      [19]  113 	ld	l, 0 (iy)
   5293 C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   5294                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   5294 FD 21 AE 67   [14]  121 	ld	iy, #_ginputright
   5298 FD 6E 00      [19]  122 	ld	l, 0 (iy)
   529B C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   529C                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   529C FD 21 AF 67   [14]  130 	ld	iy, #_ginputup
   52A0 FD 6E 00      [19]  131 	ld	l, 0 (iy)
   52A3 C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   52A4                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   52A4 FD 21 B0 67   [14]  139 	ld	iy, #_ginputdown
   52A8 FD 6E 00      [19]  140 	ld	l, 0 (iy)
   52AB C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   52AC                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   52AC FD 21 AF 67   [14]  148 	ld	iy, #_ginputup
   52B0 FD 6E 00      [19]  149 	ld	l, 0 (iy)
   52B3 C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   52B4                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   52B4 3A AF 67      [13]  157 	ld	a,(#_ginputup + 0)
   52B7 B7            [ 4]  158 	or	a, a
   52B8 28 06         [12]  159 	jr	Z,00103$
   52BA 3A B2 67      [13]  160 	ld	a,(#_gprevjump + 0)
   52BD B7            [ 4]  161 	or	a, a
   52BE 28 03         [12]  162 	jr	Z,00104$
   52C0                     163 00103$:
   52C0 2E 00         [ 7]  164 	ld	l, #0x00
   52C2 C9            [10]  165 	ret
   52C3                     166 00104$:
   52C3 2E 01         [ 7]  167 	ld	l, #0x01
   52C5 C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   52C6                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   52C6 FD 21 B1 67   [14]  175 	ld	iy, #_ginputshoot
   52CA FD 6E 00      [19]  176 	ld	l, 0 (iy)
   52CD C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   52CE                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   52CE 3A B1 67      [13]  184 	ld	a,(#_ginputshoot + 0)
   52D1 B7            [ 4]  185 	or	a, a
   52D2 28 06         [12]  186 	jr	Z,00103$
   52D4 3A B3 67      [13]  187 	ld	a,(#_gprevshoot + 0)
   52D7 B7            [ 4]  188 	or	a, a
   52D8 28 03         [12]  189 	jr	Z,00104$
   52DA                     190 00103$:
   52DA 2E 00         [ 7]  191 	ld	l, #0x00
   52DC C9            [10]  192 	ret
   52DD                     193 00104$:
   52DD 2E 01         [ 7]  194 	ld	l, #0x01
   52DF C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
