                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module level1
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _gpalette
                             12 	.globl _level1tileproperties
                             13 	.globl _level1tilemap
                             14 	.globl _level1tilemapheight
                             15 	.globl _level1tilemapwidth
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
                             47 	.area _CODE
   5AC4                      48 _level1tilemapwidth:
   5AC4 14 00                49 	.dw #0x0014
   5AC6                      50 _level1tilemapheight:
   5AC6 12 00                51 	.dw #0x0012
   5AC8                      52 _level1tilemap:
   5AC8 01                   53 	.db #0x01	; 1
   5AC9 01                   54 	.db #0x01	; 1
   5ACA 01                   55 	.db #0x01	; 1
   5ACB 01                   56 	.db #0x01	; 1
   5ACC 01                   57 	.db #0x01	; 1
   5ACD 01                   58 	.db #0x01	; 1
   5ACE 01                   59 	.db #0x01	; 1
   5ACF 01                   60 	.db #0x01	; 1
   5AD0 01                   61 	.db #0x01	; 1
   5AD1 01                   62 	.db #0x01	; 1
   5AD2 01                   63 	.db #0x01	; 1
   5AD3 00                   64 	.db #0x00	; 0
   5AD4 00                   65 	.db #0x00	; 0
   5AD5 00                   66 	.db #0x00	; 0
   5AD6 00                   67 	.db #0x00	; 0
   5AD7 00                   68 	.db #0x00	; 0
   5AD8 00                   69 	.db #0x00	; 0
   5AD9 00                   70 	.db #0x00	; 0
   5ADA 00                   71 	.db #0x00	; 0
   5ADB 01                   72 	.db #0x01	; 1
   5ADC 01                   73 	.db #0x01	; 1
   5ADD 01                   74 	.db #0x01	; 1
   5ADE 01                   75 	.db #0x01	; 1
   5ADF 01                   76 	.db #0x01	; 1
   5AE0 01                   77 	.db #0x01	; 1
   5AE1 01                   78 	.db #0x01	; 1
   5AE2 01                   79 	.db #0x01	; 1
   5AE3 01                   80 	.db #0x01	; 1
   5AE4 01                   81 	.db #0x01	; 1
   5AE5 01                   82 	.db #0x01	; 1
   5AE6                      83 _level1tileproperties:
   5AE6 00                   84 	.db #0x00	; 0
   5AE7 01                   85 	.db #0x01	; 1
   5AE8                      86 _gpalette:
   5AE8 17                   87 	.db #0x17	; 23
   5AE9 14                   88 	.db #0x14	; 20
   5AEA 0E                   89 	.db #0x0e	; 14
   5AEB 0C                   90 	.db #0x0c	; 12
   5AEC 0B                   91 	.db #0x0b	; 11
   5AED 0A                   92 	.db #0x0a	; 10
   5AEE 00                   93 	.db #0x00	; 0
   5AEF 06                   94 	.db #0x06	; 6
   5AF0 15                   95 	.db #0x15	; 21
   5AF1 12                   96 	.db #0x12	; 18
   5AF2 1E                   97 	.db #0x1e	; 30
   5AF3 16                   98 	.db #0x16	; 22
   5AF4 07                   99 	.db #0x07	; 7
   5AF5 1A                  100 	.db #0x1a	; 26
   5AF6 1C                  101 	.db #0x1c	; 28
   5AF7 1F                  102 	.db #0x1f	; 31
                            103 	.area _INITIALIZER
                            104 	.area _CABS (ABS)
