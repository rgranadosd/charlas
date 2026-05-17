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
                             12 	.globl _cpct_scanKeyboard
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
   6CC4                      29 _ginputleft:
   6CC4                      30 	.ds 1
   6CC5                      31 _ginputright:
   6CC5                      32 	.ds 1
   6CC6                      33 _ginputup:
   6CC6                      34 	.ds 1
   6CC7                      35 _ginputdown:
   6CC7                      36 	.ds 1
   6CC8                      37 _ginputjump:
   6CC8                      38 	.ds 1
   6CC9                      39 _ginputshoot:
   6CC9                      40 	.ds 1
   6CCA                      41 _gprevjump:
   6CCA                      42 	.ds 1
   6CCB                      43 _gprevshoot:
   6CCB                      44 	.ds 1
                             45 ;--------------------------------------------------------
                             46 ; ram data
                             47 ;--------------------------------------------------------
                             48 	.area _INITIALIZED
                             49 ;--------------------------------------------------------
                             50 ; absolute external ram data
                             51 ;--------------------------------------------------------
                             52 	.area _DABS (ABS)
                             53 ;--------------------------------------------------------
                             54 ; global & static initialisations
                             55 ;--------------------------------------------------------
                             56 	.area _HOME
                             57 	.area _GSINIT
                             58 	.area _GSFINAL
                             59 	.area _GSINIT
                             60 ;--------------------------------------------------------
                             61 ; Home
                             62 ;--------------------------------------------------------
                             63 	.area _HOME
                             64 	.area _HOME
                             65 ;--------------------------------------------------------
                             66 ; code
                             67 ;--------------------------------------------------------
                             68 	.area _CODE
                             69 ;src/systems/input.c:12: void input_update(void) {
                             70 ;	---------------------------------
                             71 ; Function input_update
                             72 ; ---------------------------------
   57A1                      73 _input_update::
                             74 ;src/systems/input.c:13: gprevjump = ginputjump;
   57A1 3A C8 6C      [13]   75 	ld	a,(#_ginputjump + 0)
   57A4 32 CA 6C      [13]   76 	ld	(#_gprevjump + 0),a
                             77 ;src/systems/input.c:14: gprevshoot = ginputshoot;
   57A7 3A C9 6C      [13]   78 	ld	a,(#_ginputshoot + 0)
   57AA 32 CB 6C      [13]   79 	ld	(#_gprevshoot + 0),a
                             80 ;src/systems/input.c:15: cpct_scanKeyboard();
   57AD CD 74 6B      [17]   81 	call	_cpct_scanKeyboard
                             82 ;src/systems/input.c:20: ginputleft  = (u8)(cpct_isKeyPressed(Key_CursorLeft)  || cpct_isKeyPressed(Key_O) || cpct_isKeyPressed(Key_A) || cpct_isKeyPressed(Joy0_Left));
   57B0 21 01 01      [10]   83 	ld	hl, #0x0101
   57B3 CD 32 69      [17]   84 	call	_cpct_isKeyPressed
   57B6 7D            [ 4]   85 	ld	a, l
   57B7 B7            [ 4]   86 	or	a, a
   57B8 20 21         [12]   87 	jr	NZ,00104$
   57BA 21 04 04      [10]   88 	ld	hl, #0x0404
   57BD CD 32 69      [17]   89 	call	_cpct_isKeyPressed
   57C0 7D            [ 4]   90 	ld	a, l
   57C1 B7            [ 4]   91 	or	a, a
   57C2 20 17         [12]   92 	jr	NZ,00104$
   57C4 21 08 20      [10]   93 	ld	hl, #0x2008
   57C7 CD 32 69      [17]   94 	call	_cpct_isKeyPressed
   57CA 7D            [ 4]   95 	ld	a, l
   57CB B7            [ 4]   96 	or	a, a
   57CC 20 0D         [12]   97 	jr	NZ,00104$
   57CE 21 09 04      [10]   98 	ld	hl, #0x0409
   57D1 CD 32 69      [17]   99 	call	_cpct_isKeyPressed
   57D4 7D            [ 4]  100 	ld	a, l
   57D5 B7            [ 4]  101 	or	a,a
   57D6 20 03         [12]  102 	jr	NZ,00104$
   57D8 4F            [ 4]  103 	ld	c,a
   57D9 18 02         [12]  104 	jr	00105$
   57DB                     105 00104$:
   57DB 0E 01         [ 7]  106 	ld	c, #0x01
   57DD                     107 00105$:
   57DD 21 C4 6C      [10]  108 	ld	hl,#_ginputleft + 0
   57E0 71            [ 7]  109 	ld	(hl), c
                            110 ;src/systems/input.c:21: ginputright = (u8)(cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_P) || cpct_isKeyPressed(Key_D) || cpct_isKeyPressed(Joy0_Right));
   57E1 21 00 02      [10]  111 	ld	hl, #0x0200
   57E4 CD 32 69      [17]  112 	call	_cpct_isKeyPressed
   57E7 7D            [ 4]  113 	ld	a, l
   57E8 B7            [ 4]  114 	or	a, a
   57E9 20 21         [12]  115 	jr	NZ,00113$
   57EB 21 03 08      [10]  116 	ld	hl, #0x0803
   57EE CD 32 69      [17]  117 	call	_cpct_isKeyPressed
   57F1 7D            [ 4]  118 	ld	a, l
   57F2 B7            [ 4]  119 	or	a, a
   57F3 20 17         [12]  120 	jr	NZ,00113$
   57F5 21 07 20      [10]  121 	ld	hl, #0x2007
   57F8 CD 32 69      [17]  122 	call	_cpct_isKeyPressed
   57FB 7D            [ 4]  123 	ld	a, l
   57FC B7            [ 4]  124 	or	a, a
   57FD 20 0D         [12]  125 	jr	NZ,00113$
   57FF 21 09 08      [10]  126 	ld	hl, #0x0809
   5802 CD 32 69      [17]  127 	call	_cpct_isKeyPressed
   5805 7D            [ 4]  128 	ld	a, l
   5806 B7            [ 4]  129 	or	a,a
   5807 20 03         [12]  130 	jr	NZ,00113$
   5809 4F            [ 4]  131 	ld	c,a
   580A 18 02         [12]  132 	jr	00114$
   580C                     133 00113$:
   580C 0E 01         [ 7]  134 	ld	c, #0x01
   580E                     135 00114$:
   580E 21 C5 6C      [10]  136 	ld	hl,#_ginputright + 0
   5811 71            [ 7]  137 	ld	(hl), c
                            138 ;src/systems/input.c:22: ginputup    = (u8)(cpct_isKeyPressed(Key_CursorUp)    || cpct_isKeyPressed(Key_Q) || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Joy0_Up));
   5812 21 00 01      [10]  139 	ld	hl, #0x0100
   5815 CD 32 69      [17]  140 	call	_cpct_isKeyPressed
   5818 7D            [ 4]  141 	ld	a, l
   5819 B7            [ 4]  142 	or	a, a
   581A 20 21         [12]  143 	jr	NZ,00122$
   581C 21 08 08      [10]  144 	ld	hl, #0x0808
   581F CD 32 69      [17]  145 	call	_cpct_isKeyPressed
   5822 7D            [ 4]  146 	ld	a, l
   5823 B7            [ 4]  147 	or	a, a
   5824 20 17         [12]  148 	jr	NZ,00122$
   5826 21 07 08      [10]  149 	ld	hl, #0x0807
   5829 CD 32 69      [17]  150 	call	_cpct_isKeyPressed
   582C 7D            [ 4]  151 	ld	a, l
   582D B7            [ 4]  152 	or	a, a
   582E 20 0D         [12]  153 	jr	NZ,00122$
   5830 21 09 01      [10]  154 	ld	hl, #0x0109
   5833 CD 32 69      [17]  155 	call	_cpct_isKeyPressed
   5836 7D            [ 4]  156 	ld	a, l
   5837 B7            [ 4]  157 	or	a,a
   5838 20 03         [12]  158 	jr	NZ,00122$
   583A 4F            [ 4]  159 	ld	c,a
   583B 18 02         [12]  160 	jr	00123$
   583D                     161 00122$:
   583D 0E 01         [ 7]  162 	ld	c, #0x01
   583F                     163 00123$:
   583F 21 C6 6C      [10]  164 	ld	hl,#_ginputup + 0
   5842 71            [ 7]  165 	ld	(hl), c
                            166 ;src/systems/input.c:23: ginputdown  = (u8)(cpct_isKeyPressed(Key_CursorDown)  || cpct_isKeyPressed(Key_S) || cpct_isKeyPressed(Joy0_Down));
   5843 21 00 04      [10]  167 	ld	hl, #0x0400
   5846 CD 32 69      [17]  168 	call	_cpct_isKeyPressed
   5849 7D            [ 4]  169 	ld	a, l
   584A B7            [ 4]  170 	or	a, a
   584B 20 17         [12]  171 	jr	NZ,00131$
   584D 21 07 10      [10]  172 	ld	hl, #0x1007
   5850 CD 32 69      [17]  173 	call	_cpct_isKeyPressed
   5853 7D            [ 4]  174 	ld	a, l
   5854 B7            [ 4]  175 	or	a, a
   5855 20 0D         [12]  176 	jr	NZ,00131$
   5857 21 09 02      [10]  177 	ld	hl, #0x0209
   585A CD 32 69      [17]  178 	call	_cpct_isKeyPressed
   585D 7D            [ 4]  179 	ld	a, l
   585E B7            [ 4]  180 	or	a,a
   585F 20 03         [12]  181 	jr	NZ,00131$
   5861 4F            [ 4]  182 	ld	c,a
   5862 18 02         [12]  183 	jr	00132$
   5864                     184 00131$:
   5864 0E 01         [ 7]  185 	ld	c, #0x01
   5866                     186 00132$:
   5866 21 C7 6C      [10]  187 	ld	hl,#_ginputdown + 0
   5869 71            [ 7]  188 	ld	(hl), c
                            189 ;src/systems/input.c:24: ginputjump  = (u8)(cpct_isKeyPressed(Key_Space) || cpct_isKeyPressed(Key_Z) || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Joy0_Fire1));
   586A 21 05 80      [10]  190 	ld	hl, #0x8005
   586D CD 32 69      [17]  191 	call	_cpct_isKeyPressed
   5870 7D            [ 4]  192 	ld	a, l
   5871 B7            [ 4]  193 	or	a, a
   5872 20 21         [12]  194 	jr	NZ,00137$
   5874 21 08 80      [10]  195 	ld	hl, #0x8008
   5877 CD 32 69      [17]  196 	call	_cpct_isKeyPressed
   587A 7D            [ 4]  197 	ld	a, l
   587B B7            [ 4]  198 	or	a, a
   587C 20 17         [12]  199 	jr	NZ,00137$
   587E 21 07 80      [10]  200 	ld	hl, #0x8007
   5881 CD 32 69      [17]  201 	call	_cpct_isKeyPressed
   5884 7D            [ 4]  202 	ld	a, l
   5885 B7            [ 4]  203 	or	a, a
   5886 20 0D         [12]  204 	jr	NZ,00137$
   5888 21 09 10      [10]  205 	ld	hl, #0x1009
   588B CD 32 69      [17]  206 	call	_cpct_isKeyPressed
   588E 7D            [ 4]  207 	ld	a, l
   588F B7            [ 4]  208 	or	a,a
   5890 20 03         [12]  209 	jr	NZ,00137$
   5892 4F            [ 4]  210 	ld	c,a
   5893 18 02         [12]  211 	jr	00138$
   5895                     212 00137$:
   5895 0E 01         [ 7]  213 	ld	c, #0x01
   5897                     214 00138$:
   5897 21 C8 6C      [10]  215 	ld	hl,#_ginputjump + 0
   589A 71            [ 7]  216 	ld	(hl), c
                            217 ;src/systems/input.c:25: ginputshoot = (u8)(cpct_isKeyPressed(Key_Control) || cpct_isKeyPressed(Key_Return) || cpct_isKeyPressed(Key_CursorDown) || cpct_isKeyPressed(Joy0_Fire2) || cpct_isKeyPressed(Joy0_Fire3));
   589B 21 02 80      [10]  218 	ld	hl, #0x8002
   589E CD 32 69      [17]  219 	call	_cpct_isKeyPressed
   58A1 7D            [ 4]  220 	ld	a, l
   58A2 B7            [ 4]  221 	or	a, a
   58A3 20 2B         [12]  222 	jr	NZ,00146$
   58A5 21 02 04      [10]  223 	ld	hl, #0x0402
   58A8 CD 32 69      [17]  224 	call	_cpct_isKeyPressed
   58AB 7D            [ 4]  225 	ld	a, l
   58AC B7            [ 4]  226 	or	a, a
   58AD 20 21         [12]  227 	jr	NZ,00146$
   58AF 21 00 04      [10]  228 	ld	hl, #0x0400
   58B2 CD 32 69      [17]  229 	call	_cpct_isKeyPressed
   58B5 7D            [ 4]  230 	ld	a, l
   58B6 B7            [ 4]  231 	or	a, a
   58B7 20 17         [12]  232 	jr	NZ,00146$
   58B9 21 09 20      [10]  233 	ld	hl, #0x2009
   58BC CD 32 69      [17]  234 	call	_cpct_isKeyPressed
   58BF 7D            [ 4]  235 	ld	a, l
   58C0 B7            [ 4]  236 	or	a, a
   58C1 20 0D         [12]  237 	jr	NZ,00146$
   58C3 21 09 40      [10]  238 	ld	hl, #0x4009
   58C6 CD 32 69      [17]  239 	call	_cpct_isKeyPressed
   58C9 7D            [ 4]  240 	ld	a, l
   58CA B7            [ 4]  241 	or	a,a
   58CB 20 03         [12]  242 	jr	NZ,00146$
   58CD 4F            [ 4]  243 	ld	c,a
   58CE 18 02         [12]  244 	jr	00147$
   58D0                     245 00146$:
   58D0 0E 01         [ 7]  246 	ld	c, #0x01
   58D2                     247 00147$:
   58D2 21 C9 6C      [10]  248 	ld	hl,#_ginputshoot + 0
   58D5 71            [ 7]  249 	ld	(hl), c
   58D6 C9            [10]  250 	ret
                            251 ;src/systems/input.c:28: u8 input_is_left_pressed(void) {
                            252 ;	---------------------------------
                            253 ; Function input_is_left_pressed
                            254 ; ---------------------------------
   58D7                     255 _input_is_left_pressed::
                            256 ;src/systems/input.c:29: return ginputleft;
   58D7 FD 21 C4 6C   [14]  257 	ld	iy, #_ginputleft
   58DB FD 6E 00      [19]  258 	ld	l, 0 (iy)
   58DE C9            [10]  259 	ret
                            260 ;src/systems/input.c:32: u8 input_is_right_pressed(void) {
                            261 ;	---------------------------------
                            262 ; Function input_is_right_pressed
                            263 ; ---------------------------------
   58DF                     264 _input_is_right_pressed::
                            265 ;src/systems/input.c:33: return ginputright;
   58DF FD 21 C5 6C   [14]  266 	ld	iy, #_ginputright
   58E3 FD 6E 00      [19]  267 	ld	l, 0 (iy)
   58E6 C9            [10]  268 	ret
                            269 ;src/systems/input.c:36: u8 input_is_up_pressed(void) {
                            270 ;	---------------------------------
                            271 ; Function input_is_up_pressed
                            272 ; ---------------------------------
   58E7                     273 _input_is_up_pressed::
                            274 ;src/systems/input.c:37: return ginputup;
   58E7 FD 21 C6 6C   [14]  275 	ld	iy, #_ginputup
   58EB FD 6E 00      [19]  276 	ld	l, 0 (iy)
   58EE C9            [10]  277 	ret
                            278 ;src/systems/input.c:40: u8 input_is_down_pressed(void) {
                            279 ;	---------------------------------
                            280 ; Function input_is_down_pressed
                            281 ; ---------------------------------
   58EF                     282 _input_is_down_pressed::
                            283 ;src/systems/input.c:41: return ginputdown;
   58EF FD 21 C7 6C   [14]  284 	ld	iy, #_ginputdown
   58F3 FD 6E 00      [19]  285 	ld	l, 0 (iy)
   58F6 C9            [10]  286 	ret
                            287 ;src/systems/input.c:44: u8 input_is_jump_pressed(void) {
                            288 ;	---------------------------------
                            289 ; Function input_is_jump_pressed
                            290 ; ---------------------------------
   58F7                     291 _input_is_jump_pressed::
                            292 ;src/systems/input.c:45: return ginputjump;
   58F7 FD 21 C8 6C   [14]  293 	ld	iy, #_ginputjump
   58FB FD 6E 00      [19]  294 	ld	l, 0 (iy)
   58FE C9            [10]  295 	ret
                            296 ;src/systems/input.c:48: u8 input_is_jump_just_pressed(void) {
                            297 ;	---------------------------------
                            298 ; Function input_is_jump_just_pressed
                            299 ; ---------------------------------
   58FF                     300 _input_is_jump_just_pressed::
                            301 ;src/systems/input.c:49: return (u8)(ginputjump && !gprevjump);
   58FF 3A C8 6C      [13]  302 	ld	a,(#_ginputjump + 0)
   5902 B7            [ 4]  303 	or	a, a
   5903 28 06         [12]  304 	jr	Z,00103$
   5905 3A CA 6C      [13]  305 	ld	a,(#_gprevjump + 0)
   5908 B7            [ 4]  306 	or	a, a
   5909 28 03         [12]  307 	jr	Z,00104$
   590B                     308 00103$:
   590B 2E 00         [ 7]  309 	ld	l, #0x00
   590D C9            [10]  310 	ret
   590E                     311 00104$:
   590E 2E 01         [ 7]  312 	ld	l, #0x01
   5910 C9            [10]  313 	ret
                            314 ;src/systems/input.c:52: u8 input_is_shoot_pressed(void) {
                            315 ;	---------------------------------
                            316 ; Function input_is_shoot_pressed
                            317 ; ---------------------------------
   5911                     318 _input_is_shoot_pressed::
                            319 ;src/systems/input.c:53: return ginputshoot;
   5911 FD 21 C9 6C   [14]  320 	ld	iy, #_ginputshoot
   5915 FD 6E 00      [19]  321 	ld	l, 0 (iy)
   5918 C9            [10]  322 	ret
                            323 ;src/systems/input.c:56: u8 input_is_shoot_just_pressed(void) {
                            324 ;	---------------------------------
                            325 ; Function input_is_shoot_just_pressed
                            326 ; ---------------------------------
   5919                     327 _input_is_shoot_just_pressed::
                            328 ;src/systems/input.c:57: return (u8)(ginputshoot && !gprevshoot);
   5919 3A C9 6C      [13]  329 	ld	a,(#_ginputshoot + 0)
   591C B7            [ 4]  330 	or	a, a
   591D 28 06         [12]  331 	jr	Z,00103$
   591F 3A CB 6C      [13]  332 	ld	a,(#_gprevshoot + 0)
   5922 B7            [ 4]  333 	or	a, a
   5923 28 03         [12]  334 	jr	Z,00104$
   5925                     335 00103$:
   5925 2E 00         [ 7]  336 	ld	l, #0x00
   5927 C9            [10]  337 	ret
   5928                     338 00104$:
   5928 2E 01         [ 7]  339 	ld	l, #0x01
   592A C9            [10]  340 	ret
                            341 	.area _CODE
                            342 	.area _INITIALIZER
                            343 	.area _CABS (ABS)
