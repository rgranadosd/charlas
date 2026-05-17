                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module itesplayerweapons
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _sprites_player_weapons_data
                             12 ;--------------------------------------------------------
                             13 ; special function registers
                             14 ;--------------------------------------------------------
                             15 ;--------------------------------------------------------
                             16 ; ram data
                             17 ;--------------------------------------------------------
                             18 	.area _DATA
                             19 ;--------------------------------------------------------
                             20 ; ram data
                             21 ;--------------------------------------------------------
                             22 	.area _INITIALIZED
                             23 ;--------------------------------------------------------
                             24 ; absolute external ram data
                             25 ;--------------------------------------------------------
                             26 	.area _DABS (ABS)
                             27 ;--------------------------------------------------------
                             28 ; global & static initialisations
                             29 ;--------------------------------------------------------
                             30 	.area _HOME
                             31 	.area _GSINIT
                             32 	.area _GSFINAL
                             33 	.area _GSINIT
                             34 ;--------------------------------------------------------
                             35 ; Home
                             36 ;--------------------------------------------------------
                             37 	.area _HOME
                             38 	.area _HOME
                             39 ;--------------------------------------------------------
                             40 ; code
                             41 ;--------------------------------------------------------
                             42 	.area _CODE
                             43 	.area _CODE
   5BB8                      44 _sprites_player_weapons_data:
   5BB8 FF                   45 	.db #0xff	; 255
   5BB9 FF                   46 	.db #0xff	; 255
   5BBA FF                   47 	.db #0xff	; 255
   5BBB FF                   48 	.db #0xff	; 255
   5BBC AA                   49 	.db #0xaa	; 170
   5BBD AA                   50 	.db #0xaa	; 170
   5BBE 00                   51 	.db #0x00	; 0
   5BBF 55                   52 	.db #0x55	; 85	'U'
   5BC0 AA                   53 	.db #0xaa	; 170
   5BC1 AA                   54 	.db #0xaa	; 170
   5BC2 00                   55 	.db #0x00	; 0
   5BC3 55                   56 	.db #0x55	; 85	'U'
   5BC4 AA                   57 	.db #0xaa	; 170
   5BC5 AA                   58 	.db #0xaa	; 170
   5BC6 00                   59 	.db #0x00	; 0
   5BC7 55                   60 	.db #0x55	; 85	'U'
   5BC8 AA                   61 	.db #0xaa	; 170
   5BC9 AA                   62 	.db #0xaa	; 170
   5BCA 00                   63 	.db #0x00	; 0
   5BCB 55                   64 	.db #0x55	; 85	'U'
   5BCC AA                   65 	.db #0xaa	; 170
   5BCD AA                   66 	.db #0xaa	; 170
   5BCE 00                   67 	.db #0x00	; 0
   5BCF 55                   68 	.db #0x55	; 85	'U'
   5BD0 AA                   69 	.db #0xaa	; 170
   5BD1 AA                   70 	.db #0xaa	; 170
   5BD2 00                   71 	.db #0x00	; 0
   5BD3 55                   72 	.db #0x55	; 85	'U'
   5BD4 AA                   73 	.db #0xaa	; 170
   5BD5 AA                   74 	.db #0xaa	; 170
   5BD6 00                   75 	.db #0x00	; 0
   5BD7 55                   76 	.db #0x55	; 85	'U'
   5BD8 FF                   77 	.db #0xff	; 255
   5BD9 FF                   78 	.db #0xff	; 255
   5BDA FF                   79 	.db #0xff	; 255
   5BDB FF                   80 	.db #0xff	; 255
   5BDC AA                   81 	.db #0xaa	; 170
   5BDD AA                   82 	.db #0xaa	; 170
   5BDE 00                   83 	.db #0x00	; 0
   5BDF 55                   84 	.db #0x55	; 85	'U'
   5BE0 AA                   85 	.db #0xaa	; 170
   5BE1 AA                   86 	.db #0xaa	; 170
   5BE2 00                   87 	.db #0x00	; 0
   5BE3 55                   88 	.db #0x55	; 85	'U'
   5BE4 AA                   89 	.db #0xaa	; 170
   5BE5 AA                   90 	.db #0xaa	; 170
   5BE6 00                   91 	.db #0x00	; 0
   5BE7 55                   92 	.db #0x55	; 85	'U'
   5BE8 AA                   93 	.db #0xaa	; 170
   5BE9 AA                   94 	.db #0xaa	; 170
   5BEA 00                   95 	.db #0x00	; 0
   5BEB 55                   96 	.db #0x55	; 85	'U'
   5BEC AA                   97 	.db #0xaa	; 170
   5BED AA                   98 	.db #0xaa	; 170
   5BEE 00                   99 	.db #0x00	; 0
   5BEF 55                  100 	.db #0x55	; 85	'U'
   5BF0 AA                  101 	.db #0xaa	; 170
   5BF1 AA                  102 	.db #0xaa	; 170
   5BF2 00                  103 	.db #0x00	; 0
   5BF3 55                  104 	.db #0x55	; 85	'U'
   5BF4 FF                  105 	.db #0xff	; 255
   5BF5 FF                  106 	.db #0xff	; 255
   5BF6 FF                  107 	.db #0xff	; 255
   5BF7 FF                  108 	.db #0xff	; 255
                            109 	.area _INITIALIZER
                            110 	.area _CABS (ABS)
