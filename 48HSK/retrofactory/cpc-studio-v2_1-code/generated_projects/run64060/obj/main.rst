                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module main
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _main
                             12 	.globl _game_render
                             13 	.globl _game_update
                             14 	.globl _game_init
                             15 	.globl _cpct_waitVSYNC
                             16 ;--------------------------------------------------------
                             17 ; special function registers
                             18 ;--------------------------------------------------------
                             19 ;--------------------------------------------------------
                             20 ; ram data
                             21 ;--------------------------------------------------------
                             22 	.area _DATA
                             23 ;--------------------------------------------------------
                             24 ; ram data
                             25 ;--------------------------------------------------------
                             26 	.area _INITIALIZED
                             27 ;--------------------------------------------------------
                             28 ; absolute external ram data
                             29 ;--------------------------------------------------------
                             30 	.area _DABS (ABS)
                             31 ;--------------------------------------------------------
                             32 ; global & static initialisations
                             33 ;--------------------------------------------------------
                             34 	.area _HOME
                             35 	.area _GSINIT
                             36 	.area _GSFINAL
                             37 	.area _GSINIT
                             38 ;--------------------------------------------------------
                             39 ; Home
                             40 ;--------------------------------------------------------
                             41 	.area _HOME
                             42 	.area _HOME
                             43 ;--------------------------------------------------------
                             44 ; code
                             45 ;--------------------------------------------------------
                             46 	.area _CODE
                             47 ;src/main.c:4: void main(void) {
                             48 ;	---------------------------------
                             49 ; Function main
                             50 ; ---------------------------------
   4B5C                      51 _main::
                             52 ;src/main.c:9: __endasm;
   4B5C F3            [ 4]   53 	di
   4B5D 31 F0 BF      [10]   54 	ld	sp, #0xBFF0
                             55 ;src/main.c:11: game_init();
   4B60 CD B3 42      [17]   56 	call	_game_init
                             57 ;src/main.c:12: while (1) {
   4B63                      58 00102$:
                             59 ;src/main.c:13: game_update();
   4B63 CD 83 43      [17]   60 	call	_game_update
                             61 ;src/main.c:14: game_render();
   4B66 CD A9 49      [17]   62 	call	_game_render
                             63 ;src/main.c:15: cpct_waitVSYNC();
   4B69 CD 4E 5D      [17]   64 	call	_cpct_waitVSYNC
   4B6C 18 F5         [12]   65 	jr	00102$
                             66 	.area _CODE
                             67 	.area _INITIALIZER
                             68 	.area _CABS (ABS)
