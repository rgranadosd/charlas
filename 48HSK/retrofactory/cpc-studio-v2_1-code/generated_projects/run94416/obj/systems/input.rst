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
   6510                      29 _ginputleft:
   6510                      30 	.ds 1
   6511                      31 _ginputright:
   6511                      32 	.ds 1
   6512                      33 _ginputup:
   6512                      34 	.ds 1
   6513                      35 _ginputdown:
   6513                      36 	.ds 1
   6514                      37 _ginputshoot:
   6514                      38 	.ds 1
   6515                      39 _gprevjump:
   6515                      40 	.ds 1
   6516                      41 _gprevshoot:
   6516                      42 	.ds 1
                             43 ;--------------------------------------------------------
                             44 ; ram data
                             45 ;--------------------------------------------------------
                             46 	.area _INITIALIZED
                             47 ;--------------------------------------------------------
                             48 ; absolute external ram data
                             49 ;--------------------------------------------------------
                             50 	.area _DABS (ABS)
                             51 ;--------------------------------------------------------
                             52 ; global & static initialisations
                             53 ;--------------------------------------------------------
                             54 	.area _HOME
                             55 	.area _GSINIT
                             56 	.area _GSFINAL
                             57 	.area _GSINIT
                             58 ;--------------------------------------------------------
                             59 ; Home
                             60 ;--------------------------------------------------------
                             61 	.area _HOME
                             62 	.area _HOME
                             63 ;--------------------------------------------------------
                             64 ; code
                             65 ;--------------------------------------------------------
                             66 	.area _CODE
                             67 ;src/systems/input.c:11: void input_update(void) {
                             68 ;	---------------------------------
                             69 ; Function input_update
                             70 ; ---------------------------------
   51DC                      71 _input_update::
                             72 ;src/systems/input.c:12: gprevjump = ginputup;
   51DC 3A 12 65      [13]   73 	ld	a,(#_ginputup + 0)
   51DF 32 15 65      [13]   74 	ld	(#_gprevjump + 0),a
                             75 ;src/systems/input.c:13: gprevshoot = ginputshoot;
   51E2 3A 14 65      [13]   76 	ld	a,(#_ginputshoot + 0)
   51E5 32 16 65      [13]   77 	ld	(#_gprevshoot + 0),a
                             78 ;src/systems/input.c:14: cpct_scanKeyboard_f();
   51E8 CD DD 61      [17]   79 	call	_cpct_scanKeyboard_f
                             80 ;src/systems/input.c:15: ginputleft = (u8)(cpct_isKeyPressed(Key_CursorLeft) || cpct_isKeyPressed(Key_A));
   51EB 21 01 01      [10]   81 	ld	hl, #0x0101
   51EE CD D1 61      [17]   82 	call	_cpct_isKeyPressed
   51F1 7D            [ 4]   83 	ld	a, l
   51F2 B7            [ 4]   84 	or	a, a
   51F3 20 0D         [12]   85 	jr	NZ,00104$
   51F5 21 08 20      [10]   86 	ld	hl, #0x2008
   51F8 CD D1 61      [17]   87 	call	_cpct_isKeyPressed
   51FB 7D            [ 4]   88 	ld	a, l
   51FC B7            [ 4]   89 	or	a,a
   51FD 20 03         [12]   90 	jr	NZ,00104$
   51FF 4F            [ 4]   91 	ld	c,a
   5200 18 02         [12]   92 	jr	00105$
   5202                      93 00104$:
   5202 0E 01         [ 7]   94 	ld	c, #0x01
   5204                      95 00105$:
   5204 21 10 65      [10]   96 	ld	hl,#_ginputleft + 0
   5207 71            [ 7]   97 	ld	(hl), c
                             98 ;src/systems/input.c:16: ginputright = (u8)(cpct_isKeyPressed(Key_CursorRight) || cpct_isKeyPressed(Key_D));
   5208 21 00 02      [10]   99 	ld	hl, #0x0200
   520B CD D1 61      [17]  100 	call	_cpct_isKeyPressed
   520E 7D            [ 4]  101 	ld	a, l
   520F B7            [ 4]  102 	or	a, a
   5210 20 0D         [12]  103 	jr	NZ,00107$
   5212 21 07 20      [10]  104 	ld	hl, #0x2007
   5215 CD D1 61      [17]  105 	call	_cpct_isKeyPressed
   5218 7D            [ 4]  106 	ld	a, l
   5219 B7            [ 4]  107 	or	a,a
   521A 20 03         [12]  108 	jr	NZ,00107$
   521C 4F            [ 4]  109 	ld	c,a
   521D 18 02         [12]  110 	jr	00108$
   521F                     111 00107$:
   521F 0E 01         [ 7]  112 	ld	c, #0x01
   5221                     113 00108$:
   5221 21 11 65      [10]  114 	ld	hl,#_ginputright + 0
   5224 71            [ 7]  115 	ld	(hl), c
                            116 ;src/systems/input.c:17: ginputup = (u8)(cpct_isKeyPressed(Key_CursorUp) || cpct_isKeyPressed(Key_W) || cpct_isKeyPressed(Key_Z));
   5225 21 00 01      [10]  117 	ld	hl, #0x0100
   5228 CD D1 61      [17]  118 	call	_cpct_isKeyPressed
   522B 7D            [ 4]  119 	ld	a, l
   522C B7            [ 4]  120 	or	a, a
   522D 20 17         [12]  121 	jr	NZ,00110$
   522F 21 07 08      [10]  122 	ld	hl, #0x0807
   5232 CD D1 61      [17]  123 	call	_cpct_isKeyPressed
   5235 7D            [ 4]  124 	ld	a, l
   5236 B7            [ 4]  125 	or	a, a
   5237 20 0D         [12]  126 	jr	NZ,00110$
   5239 21 08 80      [10]  127 	ld	hl, #0x8008
   523C CD D1 61      [17]  128 	call	_cpct_isKeyPressed
   523F 7D            [ 4]  129 	ld	a, l
   5240 B7            [ 4]  130 	or	a,a
   5241 20 03         [12]  131 	jr	NZ,00110$
   5243 4F            [ 4]  132 	ld	c,a
   5244 18 02         [12]  133 	jr	00111$
   5246                     134 00110$:
   5246 0E 01         [ 7]  135 	ld	c, #0x01
   5248                     136 00111$:
   5248 21 12 65      [10]  137 	ld	hl,#_ginputup + 0
   524B 71            [ 7]  138 	ld	(hl), c
                            139 ;src/systems/input.c:18: ginputdown = (u8)(cpct_isKeyPressed(Key_CursorDown) || cpct_isKeyPressed(Key_S) || cpct_isKeyPressed(Key_X));
   524C 21 00 04      [10]  140 	ld	hl, #0x0400
   524F CD D1 61      [17]  141 	call	_cpct_isKeyPressed
   5252 7D            [ 4]  142 	ld	a, l
   5253 B7            [ 4]  143 	or	a, a
   5254 20 17         [12]  144 	jr	NZ,00116$
   5256 21 07 10      [10]  145 	ld	hl, #0x1007
   5259 CD D1 61      [17]  146 	call	_cpct_isKeyPressed
   525C 7D            [ 4]  147 	ld	a, l
   525D B7            [ 4]  148 	or	a, a
   525E 20 0D         [12]  149 	jr	NZ,00116$
   5260 21 07 80      [10]  150 	ld	hl, #0x8007
   5263 CD D1 61      [17]  151 	call	_cpct_isKeyPressed
   5266 7D            [ 4]  152 	ld	a, l
   5267 B7            [ 4]  153 	or	a,a
   5268 20 03         [12]  154 	jr	NZ,00116$
   526A 4F            [ 4]  155 	ld	c,a
   526B 18 02         [12]  156 	jr	00117$
   526D                     157 00116$:
   526D 0E 01         [ 7]  158 	ld	c, #0x01
   526F                     159 00117$:
   526F 21 13 65      [10]  160 	ld	hl,#_ginputdown + 0
   5272 71            [ 7]  161 	ld	(hl), c
                            162 ;src/systems/input.c:19: ginputshoot = (u8)(cpct_isKeyPressed(Key_Space) || cpct_isKeyPressed(Key_X) || cpct_isKeyPressed(Key_CursorDown));
   5273 21 05 80      [10]  163 	ld	hl, #0x8005
   5276 CD D1 61      [17]  164 	call	_cpct_isKeyPressed
   5279 7D            [ 4]  165 	ld	a, l
   527A B7            [ 4]  166 	or	a, a
   527B 20 17         [12]  167 	jr	NZ,00122$
   527D 21 07 80      [10]  168 	ld	hl, #0x8007
   5280 CD D1 61      [17]  169 	call	_cpct_isKeyPressed
   5283 7D            [ 4]  170 	ld	a, l
   5284 B7            [ 4]  171 	or	a, a
   5285 20 0D         [12]  172 	jr	NZ,00122$
   5287 21 00 04      [10]  173 	ld	hl, #0x0400
   528A CD D1 61      [17]  174 	call	_cpct_isKeyPressed
   528D 7D            [ 4]  175 	ld	a, l
   528E B7            [ 4]  176 	or	a,a
   528F 20 03         [12]  177 	jr	NZ,00122$
   5291 4F            [ 4]  178 	ld	c,a
   5292 18 02         [12]  179 	jr	00123$
   5294                     180 00122$:
   5294 0E 01         [ 7]  181 	ld	c, #0x01
   5296                     182 00123$:
   5296 21 14 65      [10]  183 	ld	hl,#_ginputshoot + 0
   5299 71            [ 7]  184 	ld	(hl), c
   529A C9            [10]  185 	ret
                            186 ;src/systems/input.c:22: u8 input_is_left_pressed(void) {
                            187 ;	---------------------------------
                            188 ; Function input_is_left_pressed
                            189 ; ---------------------------------
   529B                     190 _input_is_left_pressed::
                            191 ;src/systems/input.c:23: return ginputleft;
   529B FD 21 10 65   [14]  192 	ld	iy, #_ginputleft
   529F FD 6E 00      [19]  193 	ld	l, 0 (iy)
   52A2 C9            [10]  194 	ret
                            195 ;src/systems/input.c:26: u8 input_is_right_pressed(void) {
                            196 ;	---------------------------------
                            197 ; Function input_is_right_pressed
                            198 ; ---------------------------------
   52A3                     199 _input_is_right_pressed::
                            200 ;src/systems/input.c:27: return ginputright;
   52A3 FD 21 11 65   [14]  201 	ld	iy, #_ginputright
   52A7 FD 6E 00      [19]  202 	ld	l, 0 (iy)
   52AA C9            [10]  203 	ret
                            204 ;src/systems/input.c:30: u8 input_is_up_pressed(void) {
                            205 ;	---------------------------------
                            206 ; Function input_is_up_pressed
                            207 ; ---------------------------------
   52AB                     208 _input_is_up_pressed::
                            209 ;src/systems/input.c:31: return ginputup;
   52AB FD 21 12 65   [14]  210 	ld	iy, #_ginputup
   52AF FD 6E 00      [19]  211 	ld	l, 0 (iy)
   52B2 C9            [10]  212 	ret
                            213 ;src/systems/input.c:34: u8 input_is_down_pressed(void) {
                            214 ;	---------------------------------
                            215 ; Function input_is_down_pressed
                            216 ; ---------------------------------
   52B3                     217 _input_is_down_pressed::
                            218 ;src/systems/input.c:35: return ginputdown;
   52B3 FD 21 13 65   [14]  219 	ld	iy, #_ginputdown
   52B7 FD 6E 00      [19]  220 	ld	l, 0 (iy)
   52BA C9            [10]  221 	ret
                            222 ;src/systems/input.c:38: u8 input_is_jump_pressed(void) {
                            223 ;	---------------------------------
                            224 ; Function input_is_jump_pressed
                            225 ; ---------------------------------
   52BB                     226 _input_is_jump_pressed::
                            227 ;src/systems/input.c:39: return ginputup;
   52BB FD 21 12 65   [14]  228 	ld	iy, #_ginputup
   52BF FD 6E 00      [19]  229 	ld	l, 0 (iy)
   52C2 C9            [10]  230 	ret
                            231 ;src/systems/input.c:42: u8 input_is_jump_just_pressed(void) {
                            232 ;	---------------------------------
                            233 ; Function input_is_jump_just_pressed
                            234 ; ---------------------------------
   52C3                     235 _input_is_jump_just_pressed::
                            236 ;src/systems/input.c:43: return (u8)(ginputup && !gprevjump);
   52C3 3A 12 65      [13]  237 	ld	a,(#_ginputup + 0)
   52C6 B7            [ 4]  238 	or	a, a
   52C7 28 06         [12]  239 	jr	Z,00103$
   52C9 3A 15 65      [13]  240 	ld	a,(#_gprevjump + 0)
   52CC B7            [ 4]  241 	or	a, a
   52CD 28 03         [12]  242 	jr	Z,00104$
   52CF                     243 00103$:
   52CF 2E 00         [ 7]  244 	ld	l, #0x00
   52D1 C9            [10]  245 	ret
   52D2                     246 00104$:
   52D2 2E 01         [ 7]  247 	ld	l, #0x01
   52D4 C9            [10]  248 	ret
                            249 ;src/systems/input.c:46: u8 input_is_shoot_pressed(void) {
                            250 ;	---------------------------------
                            251 ; Function input_is_shoot_pressed
                            252 ; ---------------------------------
   52D5                     253 _input_is_shoot_pressed::
                            254 ;src/systems/input.c:47: return ginputshoot;
   52D5 FD 21 14 65   [14]  255 	ld	iy, #_ginputshoot
   52D9 FD 6E 00      [19]  256 	ld	l, 0 (iy)
   52DC C9            [10]  257 	ret
                            258 ;src/systems/input.c:50: u8 input_is_shoot_just_pressed(void) {
                            259 ;	---------------------------------
                            260 ; Function input_is_shoot_just_pressed
                            261 ; ---------------------------------
   52DD                     262 _input_is_shoot_just_pressed::
                            263 ;src/systems/input.c:51: return (u8)(ginputshoot && !gprevshoot);
   52DD 3A 14 65      [13]  264 	ld	a,(#_ginputshoot + 0)
   52E0 B7            [ 4]  265 	or	a, a
   52E1 28 06         [12]  266 	jr	Z,00103$
   52E3 3A 16 65      [13]  267 	ld	a,(#_gprevshoot + 0)
   52E6 B7            [ 4]  268 	or	a, a
   52E7 28 03         [12]  269 	jr	Z,00104$
   52E9                     270 00103$:
   52E9 2E 00         [ 7]  271 	ld	l, #0x00
   52EB C9            [10]  272 	ret
   52EC                     273 00104$:
   52EC 2E 01         [ 7]  274 	ld	l, #0x01
   52EE C9            [10]  275 	ret
                            276 	.area _CODE
                            277 	.area _INITIALIZER
                            278 	.area _CABS (ABS)
