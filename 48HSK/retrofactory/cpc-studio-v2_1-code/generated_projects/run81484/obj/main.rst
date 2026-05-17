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
   5269                      52 _cpc_entry_wrapper::
                             53 ;src/main.c:23: __endasm;
                             54 	.globl	cpc_run_address
                             55 	.globl	s__INITIALIZER
                             56 	.globl	s__INITIALIZED
                             57 	.globl	l__INITIALIZER
   5269                      58 	    cpc_run_address::
   5269 F3            [ 4]   59 	di
   526A 31 F0 BF      [10]   60 	ld	sp, #0xBFF0
   526D 01 09 00      [10]   61 	ld	bc, #l__INITIALIZER
   5270 78            [ 4]   62 	ld	a, b
   5271 B1            [ 4]   63 	or	c
   5272 28 08         [12]   64 	jr	z, 00001$
   5274 11 8D 6D      [10]   65 	ld	de, #s__INITIALIZED
   5277 21 96 6D      [10]   66 	ld	hl, #s__INITIALIZER
   527A ED B0         [21]   67 	ldir
   527C                      68 	00001$:
   527C CD 80 52      [17]   69 	call	_main
   527F C9            [10]   70 	ret
                             71 ;src/main.c:26: void main(void) {
                             72 ;	---------------------------------
                             73 ; Function main
                             74 ; ---------------------------------
   5280                      75 _main::
                             76 ;src/main.c:31: __endasm;
   5280 F3            [ 4]   77 	di
   5281 31 F0 BF      [10]   78 	ld	sp, #0xBFF0
                             79 ;src/main.c:33: game_init();
   5284 CD B8 42      [17]   80 	call	_game_init
                             81 ;src/main.c:34: while (1) {
   5287                      82 00102$:
                             83 ;src/main.c:35: game_update();
   5287 CD B5 43      [17]   84 	call	_game_update
                             85 ;src/main.c:36: cpct_waitVSYNC();  /* sync BEFORE clear+draw: beam is at top when we start clearing */
   528A CD 6B 6A      [17]   86 	call	_cpct_waitVSYNC
                             87 ;src/main.c:37: game_render();
   528D CD 1D 4B      [17]   88 	call	_game_render
   5290 18 F5         [12]   89 	jr	00102$
                             90 	.area _CODE
                             91 	.area _INITIALIZER
                             92 	.area _CABS (ABS)
