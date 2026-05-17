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
                             12 	.globl _cpct_setPALColour
                             13 	.globl _cpct_setVideoMode
                             14 	.globl _cpct_memset
                             15 	.globl _cpct_disableFirmware
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
                             47 ;src/main.c:3: void main(void) {
                             48 ;	---------------------------------
                             49 ; Function main
                             50 ; ---------------------------------
   4B5C                      51 _main::
                             52 ;src/main.c:4: cpct_disableFirmware();
   4B5C CD 8A 5D      [17]   53 	call	_cpct_disableFirmware
                             54 ;src/main.c:5: cpct_setVideoMode(0);
   4B5F 2E 00         [ 7]   55 	ld	l, #0x00
   4B61 CD 52 5D      [17]   56 	call	_cpct_setVideoMode
                             57 ;src/main.c:6: cpct_setBorder(0x4C);  // hw colour: bright red
   4B64 21 10 4C      [10]   58 	ld	hl, #0x4c10
   4B67 E5            [11]   59 	push	hl
   4B68 CD 80 5C      [17]   60 	call	_cpct_setPALColour
                             61 ;src/main.c:7: cpct_clearScreen(0x55); // mode 0: nibble pattern -> visible solid colour
   4B6B 21 00 40      [10]   62 	ld	hl, #0x4000
   4B6E E5            [11]   63 	push	hl
   4B6F 3E 55         [ 7]   64 	ld	a, #0x55
   4B71 F5            [11]   65 	push	af
   4B72 33            [ 6]   66 	inc	sp
   4B73 26 C0         [ 7]   67 	ld	h, #0xc0
   4B75 E5            [11]   68 	push	hl
   4B76 CD 7C 5D      [17]   69 	call	_cpct_memset
                             70 ;src/main.c:9: while (1);
   4B79                      71 00102$:
   4B79 18 FE         [12]   72 	jr	00102$
                             73 	.area _CODE
                             74 	.area _INITIALIZER
                             75 	.area _CABS (ABS)
