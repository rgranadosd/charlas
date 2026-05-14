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
                             16 	.globl _input_is_jump_pressed
                             17 	.globl _input_is_jump_just_pressed
                             18 	.globl _input_is_shoot_pressed
                             19 	.globl _input_is_shoot_just_pressed
                             20 ;--------------------------------------------------------
                             21 ; special function registers
                             22 ;--------------------------------------------------------
                             23 ;--------------------------------------------------------
                             24 ; ram data
                             25 ;--------------------------------------------------------
                             26 	.area _DATA
   5A84                      27 _ginputleft:
   5A84                      28 	.ds 1
   5A85                      29 _ginputright:
   5A85                      30 	.ds 1
   5A86                      31 _ginputjump:
   5A86                      32 	.ds 1
   5A87                      33 _ginputshoot:
   5A87                      34 	.ds 1
   5A88                      35 _gprevjump:
   5A88                      36 	.ds 1
   5A89                      37 _gprevshoot:
   5A89                      38 	.ds 1
                             39 ;--------------------------------------------------------
                             40 ; ram data
                             41 ;--------------------------------------------------------
                             42 	.area _INITIALIZED
                             43 ;--------------------------------------------------------
                             44 ; absolute external ram data
                             45 ;--------------------------------------------------------
                             46 	.area _DABS (ABS)
                             47 ;--------------------------------------------------------
                             48 ; global & static initialisations
                             49 ;--------------------------------------------------------
                             50 	.area _HOME
                             51 	.area _GSINIT
                             52 	.area _GSFINAL
                             53 	.area _GSINIT
                             54 ;--------------------------------------------------------
                             55 ; Home
                             56 ;--------------------------------------------------------
                             57 	.area _HOME
                             58 	.area _HOME
                             59 ;--------------------------------------------------------
                             60 ; code
                             61 ;--------------------------------------------------------
                             62 	.area _CODE
                             63 ;src/systems/input.c:10: void input_update(void) {
                             64 ;	---------------------------------
                             65 ; Function input_update
                             66 ; ---------------------------------
   4A96                      67 _input_update::
                             68 ;src/systems/input.c:11: gprevjump = ginputjump;
   4A96 3A 86 5A      [13]   69 	ld	a,(#_ginputjump + 0)
   4A99 32 88 5A      [13]   70 	ld	(#_gprevjump + 0),a
                             71 ;src/systems/input.c:12: gprevshoot = ginputshoot;
   4A9C 3A 87 5A      [13]   72 	ld	a,(#_ginputshoot + 0)
   4A9F 32 89 5A      [13]   73 	ld	(#_gprevshoot + 0),a
                             74 ;src/systems/input.c:13: cpct_scanKeyboard_f();
   4AA2 CD B8 57      [17]   75 	call	_cpct_scanKeyboard_f
                             76 ;src/systems/input.c:14: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4AA5 21 01 01      [10]   77 	ld	hl, #0x0101
   4AA8 CD AC 57      [17]   78 	call	_cpct_isKeyPressed
   4AAB FD 21 84 5A   [14]   79 	ld	iy, #_ginputleft
   4AAF FD 75 00      [19]   80 	ld	0 (iy), l
                             81 ;src/systems/input.c:15: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4AB2 21 00 02      [10]   82 	ld	hl, #0x0200
   4AB5 CD AC 57      [17]   83 	call	_cpct_isKeyPressed
   4AB8 FD 21 85 5A   [14]   84 	ld	iy, #_ginputright
   4ABC FD 75 00      [19]   85 	ld	0 (iy), l
                             86 ;src/systems/input.c:16: ginputjump = cpct_isKeyPressed(Key_CursorUp);
   4ABF 21 00 01      [10]   87 	ld	hl, #0x0100
   4AC2 CD AC 57      [17]   88 	call	_cpct_isKeyPressed
   4AC5 FD 21 86 5A   [14]   89 	ld	iy, #_ginputjump
   4AC9 FD 75 00      [19]   90 	ld	0 (iy), l
                             91 ;src/systems/input.c:17: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   4ACC 21 00 04      [10]   92 	ld	hl, #0x0400
   4ACF CD AC 57      [17]   93 	call	_cpct_isKeyPressed
   4AD2 FD 21 87 5A   [14]   94 	ld	iy, #_ginputshoot
   4AD6 FD 75 00      [19]   95 	ld	0 (iy), l
   4AD9 C9            [10]   96 	ret
                             97 ;src/systems/input.c:20: u8 input_is_left_pressed(void) {
                             98 ;	---------------------------------
                             99 ; Function input_is_left_pressed
                            100 ; ---------------------------------
   4ADA                     101 _input_is_left_pressed::
                            102 ;src/systems/input.c:21: return ginputleft;
   4ADA FD 21 84 5A   [14]  103 	ld	iy, #_ginputleft
   4ADE FD 6E 00      [19]  104 	ld	l, 0 (iy)
   4AE1 C9            [10]  105 	ret
                            106 ;src/systems/input.c:24: u8 input_is_right_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_right_pressed
                            109 ; ---------------------------------
   4AE2                     110 _input_is_right_pressed::
                            111 ;src/systems/input.c:25: return ginputright;
   4AE2 FD 21 85 5A   [14]  112 	ld	iy, #_ginputright
   4AE6 FD 6E 00      [19]  113 	ld	l, 0 (iy)
   4AE9 C9            [10]  114 	ret
                            115 ;src/systems/input.c:28: u8 input_is_jump_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_jump_pressed
                            118 ; ---------------------------------
   4AEA                     119 _input_is_jump_pressed::
                            120 ;src/systems/input.c:29: return ginputjump;
   4AEA FD 21 86 5A   [14]  121 	ld	iy, #_ginputjump
   4AEE FD 6E 00      [19]  122 	ld	l, 0 (iy)
   4AF1 C9            [10]  123 	ret
                            124 ;src/systems/input.c:32: u8 input_is_jump_just_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_jump_just_pressed
                            127 ; ---------------------------------
   4AF2                     128 _input_is_jump_just_pressed::
                            129 ;src/systems/input.c:33: return (u8)(ginputjump && !gprevjump);
   4AF2 3A 86 5A      [13]  130 	ld	a,(#_ginputjump + 0)
   4AF5 B7            [ 4]  131 	or	a, a
   4AF6 28 06         [12]  132 	jr	Z,00103$
   4AF8 3A 88 5A      [13]  133 	ld	a,(#_gprevjump + 0)
   4AFB B7            [ 4]  134 	or	a, a
   4AFC 28 03         [12]  135 	jr	Z,00104$
   4AFE                     136 00103$:
   4AFE 2E 00         [ 7]  137 	ld	l, #0x00
   4B00 C9            [10]  138 	ret
   4B01                     139 00104$:
   4B01 2E 01         [ 7]  140 	ld	l, #0x01
   4B03 C9            [10]  141 	ret
                            142 ;src/systems/input.c:36: u8 input_is_shoot_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_shoot_pressed
                            145 ; ---------------------------------
   4B04                     146 _input_is_shoot_pressed::
                            147 ;src/systems/input.c:37: return ginputshoot;
   4B04 FD 21 87 5A   [14]  148 	ld	iy, #_ginputshoot
   4B08 FD 6E 00      [19]  149 	ld	l, 0 (iy)
   4B0B C9            [10]  150 	ret
                            151 ;src/systems/input.c:40: u8 input_is_shoot_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_shoot_just_pressed
                            154 ; ---------------------------------
   4B0C                     155 _input_is_shoot_just_pressed::
                            156 ;src/systems/input.c:41: return (u8)(ginputshoot && !gprevshoot);
   4B0C 3A 87 5A      [13]  157 	ld	a,(#_ginputshoot + 0)
   4B0F B7            [ 4]  158 	or	a, a
   4B10 28 06         [12]  159 	jr	Z,00103$
   4B12 3A 89 5A      [13]  160 	ld	a,(#_gprevshoot + 0)
   4B15 B7            [ 4]  161 	or	a, a
   4B16 28 03         [12]  162 	jr	Z,00104$
   4B18                     163 00103$:
   4B18 2E 00         [ 7]  164 	ld	l, #0x00
   4B1A C9            [10]  165 	ret
   4B1B                     166 00104$:
   4B1B 2E 01         [ 7]  167 	ld	l, #0x01
   4B1D C9            [10]  168 	ret
                            169 	.area _CODE
                            170 	.area _INITIALIZER
                            171 	.area _CABS (ABS)
