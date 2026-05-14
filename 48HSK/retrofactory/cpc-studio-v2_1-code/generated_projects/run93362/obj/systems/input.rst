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
   5E38                      29 _ginputleft:
   5E38                      30 	.ds 1
   5E39                      31 _ginputright:
   5E39                      32 	.ds 1
   5E3A                      33 _ginputup:
   5E3A                      34 	.ds 1
   5E3B                      35 _ginputdown:
   5E3B                      36 	.ds 1
   5E3C                      37 _ginputshoot:
   5E3C                      38 	.ds 1
   5E3D                      39 _gprevjump:
   5E3D                      40 	.ds 1
   5E3E                      41 _gprevshoot:
   5E3E                      42 	.ds 1
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
   4E41                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   4E41 3A 3A 5E      [13]   73 	ld	a,(#_ginputup + 0)
   4E44 32 3D 5E      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   4E47 3A 3C 5E      [13]   76 	ld	a,(#_ginputshoot + 0)
   4E4A 32 3E 5E      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   4E4D CD 57 5B      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4E50 21 01 01      [10]   81 	ld	hl, #0x0101
   4E53 CD 4B 5B      [17]   82 	call	_cpct_isKeyPressed
   4E56 FD 21 38 5E   [14]   83 	ld	iy, #_ginputleft
   4E5A FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4E5D 21 00 02      [10]   86 	ld	hl, #0x0200
   4E60 CD 4B 5B      [17]   87 	call	_cpct_isKeyPressed
   4E63 FD 21 39 5E   [14]   88 	ld	iy, #_ginputright
   4E67 FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   4E6A 21 00 01      [10]   91 	ld	hl, #0x0100
   4E6D CD 4B 5B      [17]   92 	call	_cpct_isKeyPressed
   4E70 FD 21 3A 5E   [14]   93 	ld	iy, #_ginputup
   4E74 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   4E77 21 07 80      [10]   96 	ld	hl, #0x8007
   4E7A CD 4B 5B      [17]   97 	call	_cpct_isKeyPressed
   4E7D FD 21 3B 5E   [14]   98 	ld	iy, #_ginputdown
   4E81 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   4E84 21 00 04      [10]  101 	ld	hl, #0x0400
   4E87 CD 4B 5B      [17]  102 	call	_cpct_isKeyPressed
   4E8A FD 21 3C 5E   [14]  103 	ld	iy, #_ginputshoot
   4E8E FD 75 00      [19]  104 	ld	0 (iy), l
   4E91 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   4E92                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   4E92 FD 21 38 5E   [14]  112 	ld	iy, #_ginputleft
   4E96 FD 6E 00      [19]  113 	ld	l, 0 (iy)
   4E99 C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   4E9A                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   4E9A FD 21 39 5E   [14]  121 	ld	iy, #_ginputright
   4E9E FD 6E 00      [19]  122 	ld	l, 0 (iy)
   4EA1 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   4EA2                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   4EA2 FD 21 3A 5E   [14]  130 	ld	iy, #_ginputup
   4EA6 FD 6E 00      [19]  131 	ld	l, 0 (iy)
   4EA9 C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   4EAA                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   4EAA FD 21 3B 5E   [14]  139 	ld	iy, #_ginputdown
   4EAE FD 6E 00      [19]  140 	ld	l, 0 (iy)
   4EB1 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   4EB2                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   4EB2 FD 21 3A 5E   [14]  148 	ld	iy, #_ginputup
   4EB6 FD 6E 00      [19]  149 	ld	l, 0 (iy)
   4EB9 C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   4EBA                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   4EBA 3A 3A 5E      [13]  157 	ld	a,(#_ginputup + 0)
   4EBD B7            [ 4]  158 	or	a, a
   4EBE 28 06         [12]  159 	jr	Z,00103$
   4EC0 3A 3D 5E      [13]  160 	ld	a,(#_gprevjump + 0)
   4EC3 B7            [ 4]  161 	or	a, a
   4EC4 28 03         [12]  162 	jr	Z,00104$
   4EC6                     163 00103$:
   4EC6 2E 00         [ 7]  164 	ld	l, #0x00
   4EC8 C9            [10]  165 	ret
   4EC9                     166 00104$:
   4EC9 2E 01         [ 7]  167 	ld	l, #0x01
   4ECB C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   4ECC                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   4ECC FD 21 3C 5E   [14]  175 	ld	iy, #_ginputshoot
   4ED0 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   4ED3 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   4ED4                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   4ED4 3A 3C 5E      [13]  184 	ld	a,(#_ginputshoot + 0)
   4ED7 B7            [ 4]  185 	or	a, a
   4ED8 28 06         [12]  186 	jr	Z,00103$
   4EDA 3A 3E 5E      [13]  187 	ld	a,(#_gprevshoot + 0)
   4EDD B7            [ 4]  188 	or	a, a
   4EDE 28 03         [12]  189 	jr	Z,00104$
   4EE0                     190 00103$:
   4EE0 2E 00         [ 7]  191 	ld	l, #0x00
   4EE2 C9            [10]  192 	ret
   4EE3                     193 00104$:
   4EE3 2E 01         [ 7]  194 	ld	l, #0x01
   4EE5 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
