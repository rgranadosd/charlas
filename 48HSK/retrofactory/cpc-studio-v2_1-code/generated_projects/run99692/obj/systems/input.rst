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
                             17 ;--------------------------------------------------------
                             18 ; special function registers
                             19 ;--------------------------------------------------------
                             20 ;--------------------------------------------------------
                             21 ; ram data
                             22 ;--------------------------------------------------------
                             23 	.area _DATA
   48D0                      24 _ginputleft:
   48D0                      25 	.ds 1
   48D1                      26 _ginputright:
   48D1                      27 	.ds 1
   48D2                      28 _ginputjump:
   48D2                      29 	.ds 1
                             30 ;--------------------------------------------------------
                             31 ; ram data
                             32 ;--------------------------------------------------------
                             33 	.area _INITIALIZED
                             34 ;--------------------------------------------------------
                             35 ; absolute external ram data
                             36 ;--------------------------------------------------------
                             37 	.area _DABS (ABS)
                             38 ;--------------------------------------------------------
                             39 ; global & static initialisations
                             40 ;--------------------------------------------------------
                             41 	.area _HOME
                             42 	.area _GSINIT
                             43 	.area _GSFINAL
                             44 	.area _GSINIT
                             45 ;--------------------------------------------------------
                             46 ; Home
                             47 ;--------------------------------------------------------
                             48 	.area _HOME
                             49 	.area _HOME
                             50 ;--------------------------------------------------------
                             51 ; code
                             52 ;--------------------------------------------------------
                             53 	.area _CODE
                             54 ;src/systems/input.c:7: void input_update(void) {
                             55 ;	---------------------------------
                             56 ; Function input_update
                             57 ; ---------------------------------
   4302                      58 _input_update::
                             59 ;src/systems/input.c:8: cpct_scanKeyboard_f();
   4302 CD 88 46      [17]   60 	call	_cpct_scanKeyboard_f
                             61 ;src/systems/input.c:9: ginputleft = cpct_isKeyPressed(Key_CursorLeft);
   4305 21 01 01      [10]   62 	ld	hl, #0x0101
   4308 CD 7C 46      [17]   63 	call	_cpct_isKeyPressed
   430B FD 21 D0 48   [14]   64 	ld	iy, #_ginputleft
   430F FD 75 00      [19]   65 	ld	0 (iy), l
                             66 ;src/systems/input.c:10: ginputright = cpct_isKeyPressed(Key_CursorRight);
   4312 21 00 02      [10]   67 	ld	hl, #0x0200
   4315 CD 7C 46      [17]   68 	call	_cpct_isKeyPressed
   4318 FD 21 D1 48   [14]   69 	ld	iy, #_ginputright
   431C FD 75 00      [19]   70 	ld	0 (iy), l
                             71 ;src/systems/input.c:11: ginputjump = cpct_isKeyPressed(Key_CursorUp);
   431F 21 00 01      [10]   72 	ld	hl, #0x0100
   4322 CD 7C 46      [17]   73 	call	_cpct_isKeyPressed
   4325 FD 21 D2 48   [14]   74 	ld	iy, #_ginputjump
   4329 FD 75 00      [19]   75 	ld	0 (iy), l
   432C C9            [10]   76 	ret
                             77 ;src/systems/input.c:14: u8 input_is_left_pressed(void) {
                             78 ;	---------------------------------
                             79 ; Function input_is_left_pressed
                             80 ; ---------------------------------
   432D                      81 _input_is_left_pressed::
                             82 ;src/systems/input.c:15: return ginputleft;
   432D FD 21 D0 48   [14]   83 	ld	iy, #_ginputleft
   4331 FD 6E 00      [19]   84 	ld	l, 0 (iy)
   4334 C9            [10]   85 	ret
                             86 ;src/systems/input.c:18: u8 input_is_right_pressed(void) {
                             87 ;	---------------------------------
                             88 ; Function input_is_right_pressed
                             89 ; ---------------------------------
   4335                      90 _input_is_right_pressed::
                             91 ;src/systems/input.c:19: return ginputright;
   4335 FD 21 D1 48   [14]   92 	ld	iy, #_ginputright
   4339 FD 6E 00      [19]   93 	ld	l, 0 (iy)
   433C C9            [10]   94 	ret
                             95 ;src/systems/input.c:22: u8 input_is_jump_pressed(void) {
                             96 ;	---------------------------------
                             97 ; Function input_is_jump_pressed
                             98 ; ---------------------------------
   433D                      99 _input_is_jump_pressed::
                            100 ;src/systems/input.c:23: return ginputjump;
   433D FD 21 D2 48   [14]  101 	ld	iy, #_ginputjump
   4341 FD 6E 00      [19]  102 	ld	l, 0 (iy)
   4344 C9            [10]  103 	ret
                            104 	.area _CODE
                            105 	.area _INITIALIZER
                            106 	.area _CABS (ABS)
