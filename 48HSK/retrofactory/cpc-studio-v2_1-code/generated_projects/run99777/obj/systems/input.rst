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
   62A8                      29 _ginputleft:
   62A8                      30 	.ds 1
   62A9                      31 _ginputright:
   62A9                      32 	.ds 1
   62AA                      33 _ginputup:
   62AA                      34 	.ds 1
   62AB                      35 _ginputdown:
   62AB                      36 	.ds 1
   62AC                      37 _ginputshoot:
   62AC                      38 	.ds 1
   62AD                      39 _gprevjump:
   62AD                      40 	.ds 1
   62AE                      41 _gprevshoot:
   62AE                      42 	.ds 1
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
   4FA2                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   4FA2 3A AA 62      [13]   73 	ld	a,(#_ginputup + 0)
   4FA5 32 AD 62      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   4FA8 3A AC 62      [13]   76 	ld	a,(#_ginputshoot + 0)
   4FAB 32 AE 62      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   4FAE CD 6F 5F      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4FB1 21 01 01      [10]   81 	ld	hl, #0x0101
   4FB4 CD 63 5F      [17]   82 	call	_cpct_isKeyPressed
   4FB7 FD 21 A8 62   [14]   83 	ld	iy, #_ginputleft
   4FBB FD 75 00      [19]   84 	ld	0 (iy), l
                             85 ;src/systems/input.c:16: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4FBE 21 00 02      [10]   86 	ld	hl, #0x0200
   4FC1 CD 63 5F      [17]   87 	call	_cpct_isKeyPressed
   4FC4 FD 21 A9 62   [14]   88 	ld	iy, #_ginputright
   4FC8 FD 75 00      [19]   89 	ld	0 (iy), l
                             90 ;src/systems/input.c:17: ginputup = cpct_isKeyPressed(Key_CursorUp);
   4FCB 21 00 01      [10]   91 	ld	hl, #0x0100
   4FCE CD 63 5F      [17]   92 	call	_cpct_isKeyPressed
   4FD1 FD 21 AA 62   [14]   93 	ld	iy, #_ginputup
   4FD5 FD 75 00      [19]   94 	ld	0 (iy), l
                             95 ;src/systems/input.c:18: ginputdown = cpct_isKeyPressed(Key_X);
   4FD8 21 07 80      [10]   96 	ld	hl, #0x8007
   4FDB CD 63 5F      [17]   97 	call	_cpct_isKeyPressed
   4FDE FD 21 AB 62   [14]   98 	ld	iy, #_ginputdown
   4FE2 FD 75 00      [19]   99 	ld	0 (iy), l
                            100 ;src/systems/input.c:19: ginputshoot = cpct_isKeyPressed(Key_CursorDown);
   4FE5 21 00 04      [10]  101 	ld	hl, #0x0400
   4FE8 CD 63 5F      [17]  102 	call	_cpct_isKeyPressed
   4FEB FD 21 AC 62   [14]  103 	ld	iy, #_ginputshoot
   4FEF FD 75 00      [19]  104 	ld	0 (iy), l
   4FF2 C9            [10]  105 	ret
                            106 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            107 ;	---------------------------------
                            108 ; Function input_is_left_pressed
                            109 ; ---------------------------------
   4FF3                     110 _input_is_left_pressed::
                            111 ;src/systems/input.c:23: return ginputleft;
   4FF3 FD 21 A8 62   [14]  112 	ld	iy, #_ginputleft
   4FF7 FD 6E 00      [19]  113 	ld	l, 0 (iy)
   4FFA C9            [10]  114 	ret
                            115 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            116 ;	---------------------------------
                            117 ; Function input_is_right_pressed
                            118 ; ---------------------------------
   4FFB                     119 _input_is_right_pressed::
                            120 ;src/systems/input.c:27: return ginputright;
   4FFB FD 21 A9 62   [14]  121 	ld	iy, #_ginputright
   4FFF FD 6E 00      [19]  122 	ld	l, 0 (iy)
   5002 C9            [10]  123 	ret
                            124 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            125 ;	---------------------------------
                            126 ; Function input_is_up_pressed
                            127 ; ---------------------------------
   5003                     128 _input_is_up_pressed::
                            129 ;src/systems/input.c:31: return ginputup;
   5003 FD 21 AA 62   [14]  130 	ld	iy, #_ginputup
   5007 FD 6E 00      [19]  131 	ld	l, 0 (iy)
   500A C9            [10]  132 	ret
                            133 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            134 ;	---------------------------------
                            135 ; Function input_is_down_pressed
                            136 ; ---------------------------------
   500B                     137 _input_is_down_pressed::
                            138 ;src/systems/input.c:35: return ginputdown;
   500B FD 21 AB 62   [14]  139 	ld	iy, #_ginputdown
   500F FD 6E 00      [19]  140 	ld	l, 0 (iy)
   5012 C9            [10]  141 	ret
                            142 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            143 ;	---------------------------------
                            144 ; Function input_is_jump_pressed
                            145 ; ---------------------------------
   5013                     146 _input_is_jump_pressed::
                            147 ;src/systems/input.c:39: return ginputup;
   5013 FD 21 AA 62   [14]  148 	ld	iy, #_ginputup
   5017 FD 6E 00      [19]  149 	ld	l, 0 (iy)
   501A C9            [10]  150 	ret
                            151 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            152 ;	---------------------------------
                            153 ; Function input_is_jump_just_pressed
                            154 ; ---------------------------------
   501B                     155 _input_is_jump_just_pressed::
                            156 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   501B 3A AA 62      [13]  157 	ld	a,(#_ginputup + 0)
   501E B7            [ 4]  158 	or	a, a
   501F 28 06         [12]  159 	jr	Z,00103$
   5021 3A AD 62      [13]  160 	ld	a,(#_gprevjump + 0)
   5024 B7            [ 4]  161 	or	a, a
   5025 28 03         [12]  162 	jr	Z,00104$
   5027                     163 00103$:
   5027 2E 00         [ 7]  164 	ld	l, #0x00
   5029 C9            [10]  165 	ret
   502A                     166 00104$:
   502A 2E 01         [ 7]  167 	ld	l, #0x01
   502C C9            [10]  168 	ret
                            169 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            170 ;	---------------------------------
                            171 ; Function input_is_shoot_pressed
                            172 ; ---------------------------------
   502D                     173 _input_is_shoot_pressed::
                            174 ;src/systems/input.c:47: return ginputshoot;
   502D FD 21 AC 62   [14]  175 	ld	iy, #_ginputshoot
   5031 FD 6E 00      [19]  176 	ld	l, 0 (iy)
   5034 C9            [10]  177 	ret
                            178 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            179 ;	---------------------------------
                            180 ; Function input_is_shoot_just_pressed
                            181 ; ---------------------------------
   5035                     182 _input_is_shoot_just_pressed::
                            183 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   5035 3A AC 62      [13]  184 	ld	a,(#_ginputshoot + 0)
   5038 B7            [ 4]  185 	or	a, a
   5039 28 06         [12]  186 	jr	Z,00103$
   503B 3A AE 62      [13]  187 	ld	a,(#_gprevshoot + 0)
   503E B7            [ 4]  188 	or	a, a
   503F 28 03         [12]  189 	jr	Z,00104$
   5041                     190 00103$:
   5041 2E 00         [ 7]  191 	ld	l, #0x00
   5043 C9            [10]  192 	ret
   5044                     193 00104$:
   5044 2E 01         [ 7]  194 	ld	l, #0x01
   5046 C9            [10]  195 	ret
                            196 	.area _CODE
                            197 	.area _INITIALIZER
                            198 	.area _CABS (ABS)
