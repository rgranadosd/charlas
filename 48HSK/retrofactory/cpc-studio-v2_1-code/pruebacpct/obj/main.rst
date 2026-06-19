                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X x86_64)
                              4 ;--------------------------------------------------------
                              5 	.module main
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _main
                             12 	.globl _cpct_getScreenPtr
                             13 	.globl _cpct_drawStringM1
                             14 	.globl _cpct_memset
                             15 ;--------------------------------------------------------
                             16 ; special function registers
                             17 ;--------------------------------------------------------
                             18 ;--------------------------------------------------------
                             19 ; ram data
                             20 ;--------------------------------------------------------
                             21 	.area _DATA
                             22 ;--------------------------------------------------------
                             23 ; ram data
                             24 ;--------------------------------------------------------
                             25 	.area _INITIALIZED
                             26 ;--------------------------------------------------------
                             27 ; absolute external ram data
                             28 ;--------------------------------------------------------
                             29 	.area _DABS (ABS)
                             30 ;--------------------------------------------------------
                             31 ; global & static initialisations
                             32 ;--------------------------------------------------------
                             33 	.area _HOME
                             34 	.area _GSINIT
                             35 	.area _GSFINAL
                             36 	.area _GSINIT
                             37 ;--------------------------------------------------------
                             38 ; Home
                             39 ;--------------------------------------------------------
                             40 	.area _HOME
                             41 	.area _HOME
                             42 ;--------------------------------------------------------
                             43 ; code
                             44 ;--------------------------------------------------------
                             45 	.area _CODE
                             46 ;src/main.c:21: void main(void) {
                             47 ;	---------------------------------
                             48 ; Function main
                             49 ; ---------------------------------
   4000                      50 _main::
                             51 ;src/main.c:25: cpct_memset(CPCT_VMEM_START, 0, 0x4000);
   4000 21 00 40      [10]   52 	ld	hl, #0x4000
   4003 E5            [11]   53 	push	hl
   4004 AF            [ 4]   54 	xor	a, a
   4005 F5            [11]   55 	push	af
   4006 33            [ 6]   56 	inc	sp
   4007 26 C0         [ 7]   57 	ld	h, #0xc0
   4009 E5            [11]   58 	push	hl
   400A CD EE 40      [17]   59 	call	_cpct_memset
                             60 ;src/main.c:28: pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 20, 96);
   400D 21 14 60      [10]   61 	ld	hl, #0x6014
   4010 E5            [11]   62 	push	hl
   4011 21 00 C0      [10]   63 	ld	hl, #0xc000
   4014 E5            [11]   64 	push	hl
   4015 CD FD 40      [17]   65 	call	_cpct_getScreenPtr
                             66 ;src/main.c:29: cpct_drawStringM1("Welcome to CPCtelera!", pvmem, 1, 0);
   4018 01 2B 40      [10]   67 	ld	bc, #___str_0+0
   401B 11 01 00      [10]   68 	ld	de, #0x0001
   401E D5            [11]   69 	push	de
   401F E5            [11]   70 	push	hl
   4020 C5            [11]   71 	push	bc
   4021 CD 41 40      [17]   72 	call	_cpct_drawStringM1
   4024 21 06 00      [10]   73 	ld	hl, #6
   4027 39            [11]   74 	add	hl, sp
   4028 F9            [ 6]   75 	ld	sp, hl
                             76 ;src/main.c:32: while (1);
   4029                      77 00102$:
   4029 18 FE         [12]   78 	jr	00102$
   402B                      79 ___str_0:
   402B 57 65 6C 63 6F 6D    80 	.ascii "Welcome to CPCtelera!"
        65 20 74 6F 20 43
        50 43 74 65 6C 65
        72 61 21
   4040 00                   81 	.db 0x00
                             82 	.area _CODE
                             83 	.area _INITIALIZER
                             84 	.area _CABS (ABS)
