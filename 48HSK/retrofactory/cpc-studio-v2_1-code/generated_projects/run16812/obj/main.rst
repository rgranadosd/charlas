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
                             12 	.globl _cpc_entry_wrapper
                             13 	.globl _game_render
                             14 	.globl _game_update
                             15 	.globl _game_init
                             16 	.globl _cpct_waitVSYNC
                             17 ;--------------------------------------------------------
                             18 ; special function registers
                             19 ;--------------------------------------------------------
                             20 ;--------------------------------------------------------
                             21 ; ram data
                             22 ;--------------------------------------------------------
                             23 	.area _DATA
                             24 ;--------------------------------------------------------
                             25 ; ram data
                             26 ;--------------------------------------------------------
                             27 	.area _INITIALIZED
                             28 ;--------------------------------------------------------
                             29 ; absolute external ram data
                             30 ;--------------------------------------------------------
                             31 	.area _DABS (ABS)
                             32 ;--------------------------------------------------------
                             33 ; global & static initialisations
                             34 ;--------------------------------------------------------
                             35 	.area _HOME
                             36 	.area _GSINIT
                             37 	.area _GSFINAL
                             38 	.area _GSINIT
                             39 ;--------------------------------------------------------
                             40 ; Home
                             41 ;--------------------------------------------------------
                             42 	.area _HOME
                             43 	.area _HOME
                             44 ;--------------------------------------------------------
                             45 ; code
                             46 ;--------------------------------------------------------
                             47 	.area _CODE
                             48 ;src/main.c:4: void cpc_entry_wrapper(void) __naked {
                             49 ;	---------------------------------
                             50 ; Function cpc_entry_wrapper
                             51 ; ---------------------------------
   4B5C                      52 _cpc_entry_wrapper::
                             53 ;src/main.c:10: __endasm;
                             54 	.globl	cpc_run_address
   4B5C                      55 	    cpc_run_address::
   4B5C CD 60 4B      [17]   56 	call	_main
   4B5F C9            [10]   57 	ret
                             58 ;src/main.c:13: void main(void) {
                             59 ;	---------------------------------
                             60 ; Function main
                             61 ; ---------------------------------
   4B60                      62 _main::
                             63 ;src/main.c:18: __endasm;
   4B60 F3            [ 4]   64 	di
   4B61 31 F0 BF      [10]   65 	ld	sp, #0xBFF0
                             66 ;src/main.c:20: game_init();
   4B64 CD B3 42      [17]   67 	call	_game_init
                             68 ;src/main.c:21: while (1) {
   4B67                      69 00102$:
                             70 ;src/main.c:22: game_update();
   4B67 CD 83 43      [17]   71 	call	_game_update
                             72 ;src/main.c:23: game_render();
   4B6A CD A9 49      [17]   73 	call	_game_render
                             74 ;src/main.c:24: cpct_waitVSYNC();
   4B6D CD A0 5D      [17]   75 	call	_cpct_waitVSYNC
   4B70 18 F5         [12]   76 	jr	00102$
                             77 	.area _CODE
                             78 	.area _INITIALIZER
                             79 	.area _CABS (ABS)
