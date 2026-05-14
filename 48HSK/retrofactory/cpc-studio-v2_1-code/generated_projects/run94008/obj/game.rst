                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module game
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _playerrender
                             12 	.globl _playerupdate
                             13 	.globl _playerinit
                             14 	.globl _collision_init
                             15 	.globl _input_update
                             16 	.globl _tilemap_render
                             17 	.globl _tilemap_init
                             18 	.globl _cpct_setVideoMode
                             19 	.globl _cpct_memset
                             20 	.globl _cpct_disableFirmware
                             21 	.globl _game_init
                             22 	.globl _game_update
                             23 	.globl _game_render
                             24 ;--------------------------------------------------------
                             25 ; special function registers
                             26 ;--------------------------------------------------------
                             27 ;--------------------------------------------------------
                             28 ; ram data
                             29 ;--------------------------------------------------------
                             30 	.area _DATA
   48C1                      31 _g_player:
   48C1                      32 	.ds 6
                             33 ;--------------------------------------------------------
                             34 ; ram data
                             35 ;--------------------------------------------------------
                             36 	.area _INITIALIZED
                             37 ;--------------------------------------------------------
                             38 ; absolute external ram data
                             39 ;--------------------------------------------------------
                             40 	.area _DABS (ABS)
                             41 ;--------------------------------------------------------
                             42 ; global & static initialisations
                             43 ;--------------------------------------------------------
                             44 	.area _HOME
                             45 	.area _GSINIT
                             46 	.area _GSFINAL
                             47 	.area _GSINIT
                             48 ;--------------------------------------------------------
                             49 ; Home
                             50 ;--------------------------------------------------------
                             51 	.area _HOME
                             52 	.area _HOME
                             53 ;--------------------------------------------------------
                             54 ; code
                             55 ;--------------------------------------------------------
                             56 	.area _CODE
                             57 ;src/game.c:10: void game_init(void) {
                             58 ;	---------------------------------
                             59 ; Function game_init
                             60 ; ---------------------------------
   4000                      61 _game_init::
                             62 ;src/game.c:11: cpct_disableFirmware();
   4000 CD D8 47      [17]   63 	call	_cpct_disableFirmware
                             64 ;src/game.c:12: cpct_setVideoMode(1);
   4003 2E 01         [ 7]   65 	ld	l, #0x01
   4005 CD BC 47      [17]   66 	call	_cpct_setVideoMode
                             67 ;src/game.c:13: cpct_clearScreen(0x00);
   4008 21 00 40      [10]   68 	ld	hl, #0x4000
   400B E5            [11]   69 	push	hl
   400C AF            [ 4]   70 	xor	a, a
   400D F5            [11]   71 	push	af
   400E 33            [ 6]   72 	inc	sp
   400F 26 C0         [ 7]   73 	ld	h, #0xc0
   4011 E5            [11]   74 	push	hl
   4012 CD CA 47      [17]   75 	call	_cpct_memset
                             76 ;src/game.c:14: tilemap_init();
   4015 CD 45 43      [17]   77 	call	_tilemap_init
                             78 ;src/game.c:15: collision_init();
   4018 CD 57 40      [17]   79 	call	_collision_init
                             80 ;src/game.c:16: playerinit(&g_player);
   401B 21 C1 48      [10]   81 	ld	hl, #_g_player
   401E E5            [11]   82 	push	hl
   401F CD 7F 44      [17]   83 	call	_playerinit
   4022 F1            [10]   84 	pop	af
   4023 C9            [10]   85 	ret
                             86 ;src/game.c:19: void game_update(void) {
                             87 ;	---------------------------------
                             88 ; Function game_update
                             89 ; ---------------------------------
   4024                      90 _game_update::
                             91 ;src/game.c:20: input_update();
   4024 CD 02 43      [17]   92 	call	_input_update
                             93 ;src/game.c:21: playerupdate(&g_player);
   4027 21 C1 48      [10]   94 	ld	hl, #_g_player
   402A E5            [11]   95 	push	hl
   402B CD B0 44      [17]   96 	call	_playerupdate
   402E F1            [10]   97 	pop	af
   402F C9            [10]   98 	ret
                             99 ;src/game.c:24: void game_render(void) {
                            100 ;	---------------------------------
                            101 ; Function game_render
                            102 ; ---------------------------------
   4030                     103 _game_render::
                            104 ;src/game.c:25: cpct_clearScreen(0x00);
   4030 21 00 40      [10]  105 	ld	hl, #0x4000
   4033 E5            [11]  106 	push	hl
   4034 AF            [ 4]  107 	xor	a, a
   4035 F5            [11]  108 	push	af
   4036 33            [ 6]  109 	inc	sp
   4037 26 C0         [ 7]  110 	ld	h, #0xc0
   4039 E5            [11]  111 	push	hl
   403A CD CA 47      [17]  112 	call	_cpct_memset
                            113 ;src/game.c:26: tilemap_render();
   403D CD 62 43      [17]  114 	call	_tilemap_render
                            115 ;src/game.c:27: playerrender(&g_player);
   4040 21 C1 48      [10]  116 	ld	hl, #_g_player
   4043 E5            [11]  117 	push	hl
   4044 CD F2 45      [17]  118 	call	_playerrender
   4047 F1            [10]  119 	pop	af
   4048 C9            [10]  120 	ret
                            121 	.area _CODE
                            122 	.area _INITIALIZER
                            123 	.area _CABS (ABS)
