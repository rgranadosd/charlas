                              1 ;--------------------------------------------------------
                              2 ; File Created by SDCC : free open source ANSI-C Compiler
                              3 ; Version 3.6.8 #9946 (Mac OS X ppc)
                              4 ;--------------------------------------------------------
                              5 	.module playerknight
                              6 	.optsdcc -mz80
                              7 	
                              8 ;--------------------------------------------------------
                              9 ; Public variables in this module
                             10 ;--------------------------------------------------------
                             11 	.globl _sprplayerknight_data
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
   5C18                      44 _sprplayerknight_data:
   5C18 3C                   45 	.db #0x3c	; 60
   5C19 FF                   46 	.db #0xff	; 255
   5C1A FF                   47 	.db #0xff	; 255
   5C1B FF                   48 	.db #0xff	; 255
   5C1C FF                   49 	.db #0xff	; 255
   5C1D FF                   50 	.db #0xff	; 255
   5C1E FF                   51 	.db #0xff	; 255
   5C1F 3C                   52 	.db #0x3c	; 60
   5C20 3C                   53 	.db #0x3c	; 60
   5C21 FF                   54 	.db #0xff	; 255
   5C22 FF                   55 	.db #0xff	; 255
   5C23 FF                   56 	.db #0xff	; 255
   5C24 FF                   57 	.db #0xff	; 255
   5C25 FF                   58 	.db #0xff	; 255
   5C26 FF                   59 	.db #0xff	; 255
   5C27 3C                   60 	.db #0x3c	; 60
   5C28 3C                   61 	.db #0x3c	; 60
   5C29 BE                   62 	.db #0xbe	; 190
   5C2A 3C                   63 	.db #0x3c	; 60
   5C2B 3C                   64 	.db #0x3c	; 60
   5C2C 3C                   65 	.db #0x3c	; 60
   5C2D 3C                   66 	.db #0x3c	; 60
   5C2E 7D                   67 	.db #0x7d	; 125
   5C2F 3C                   68 	.db #0x3c	; 60
   5C30 3C                   69 	.db #0x3c	; 60
   5C31 BE                   70 	.db #0xbe	; 190
   5C32 FF                   71 	.db #0xff	; 255
   5C33 3C                   72 	.db #0x3c	; 60
   5C34 3C                   73 	.db #0x3c	; 60
   5C35 FF                   74 	.db #0xff	; 255
   5C36 7D                   75 	.db #0x7d	; 125
   5C37 3C                   76 	.db #0x3c	; 60
   5C38 3C                   77 	.db #0x3c	; 60
   5C39 FF                   78 	.db #0xff	; 255
   5C3A FF                   79 	.db #0xff	; 255
   5C3B FF                   80 	.db #0xff	; 255
   5C3C FF                   81 	.db #0xff	; 255
   5C3D FF                   82 	.db #0xff	; 255
   5C3E FF                   83 	.db #0xff	; 255
   5C3F 3C                   84 	.db #0x3c	; 60
   5C40 3C                   85 	.db #0x3c	; 60
   5C41 3C                   86 	.db #0x3c	; 60
   5C42 EA                   87 	.db #0xea	; 234
   5C43 C0                   88 	.db #0xc0	; 192
   5C44 C0                   89 	.db #0xc0	; 192
   5C45 D5                   90 	.db #0xd5	; 213
   5C46 3C                   91 	.db #0x3c	; 60
   5C47 3C                   92 	.db #0x3c	; 60
   5C48 FF                   93 	.db #0xff	; 255
   5C49 BE                   94 	.db #0xbe	; 190
   5C4A C0                   95 	.db #0xc0	; 192
   5C4B C0                   96 	.db #0xc0	; 192
   5C4C C0                   97 	.db #0xc0	; 192
   5C4D 94                   98 	.db #0x94	; 148
   5C4E FF                   99 	.db #0xff	; 255
   5C4F BE                  100 	.db #0xbe	; 190
   5C50 68                  101 	.db #0x68	; 104	'h'
   5C51 D5                  102 	.db #0xd5	; 213
   5C52 C0                  103 	.db #0xc0	; 192
   5C53 C0                  104 	.db #0xc0	; 192
   5C54 C0                  105 	.db #0xc0	; 192
   5C55 D5                  106 	.db #0xd5	; 213
   5C56 C0                  107 	.db #0xc0	; 192
   5C57 3C                  108 	.db #0x3c	; 60
   5C58 68                  109 	.db #0x68	; 104	'h'
   5C59 D5                  110 	.db #0xd5	; 213
   5C5A D5                  111 	.db #0xd5	; 213
   5C5B C0                  112 	.db #0xc0	; 192
   5C5C C0                  113 	.db #0xc0	; 192
   5C5D FF                  114 	.db #0xff	; 255
   5C5E C0                  115 	.db #0xc0	; 192
   5C5F 3C                  116 	.db #0x3c	; 60
   5C60 68                  117 	.db #0x68	; 104	'h'
   5C61 D5                  118 	.db #0xd5	; 213
   5C62 3C                  119 	.db #0x3c	; 60
   5C63 3C                  120 	.db #0x3c	; 60
   5C64 3C                  121 	.db #0x3c	; 60
   5C65 7D                  122 	.db #0x7d	; 125
   5C66 C0                  123 	.db #0xc0	; 192
   5C67 3C                  124 	.db #0x3c	; 60
   5C68 68                  125 	.db #0x68	; 104	'h'
   5C69 D5                  126 	.db #0xd5	; 213
   5C6A C0                  127 	.db #0xc0	; 192
   5C6B C0                  128 	.db #0xc0	; 192
   5C6C C0                  129 	.db #0xc0	; 192
   5C6D D5                  130 	.db #0xd5	; 213
   5C6E C0                  131 	.db #0xc0	; 192
   5C6F 3C                  132 	.db #0x3c	; 60
   5C70 68                  133 	.db #0x68	; 104	'h'
   5C71 D5                  134 	.db #0xd5	; 213
   5C72 C0                  135 	.db #0xc0	; 192
   5C73 C0                  136 	.db #0xc0	; 192
   5C74 C0                  137 	.db #0xc0	; 192
   5C75 D5                  138 	.db #0xd5	; 213
   5C76 C0                  139 	.db #0xc0	; 192
   5C77 3C                  140 	.db #0x3c	; 60
   5C78 68                  141 	.db #0x68	; 104	'h'
   5C79 D5                  142 	.db #0xd5	; 213
   5C7A C0                  143 	.db #0xc0	; 192
   5C7B C0                  144 	.db #0xc0	; 192
   5C7C C0                  145 	.db #0xc0	; 192
   5C7D D5                  146 	.db #0xd5	; 213
   5C7E C0                  147 	.db #0xc0	; 192
   5C7F 3C                  148 	.db #0x3c	; 60
   5C80 68                  149 	.db #0x68	; 104	'h'
   5C81 D5                  150 	.db #0xd5	; 213
   5C82 C0                  151 	.db #0xc0	; 192
   5C83 C0                  152 	.db #0xc0	; 192
   5C84 C0                  153 	.db #0xc0	; 192
   5C85 D5                  154 	.db #0xd5	; 213
   5C86 C0                  155 	.db #0xc0	; 192
   5C87 3C                  156 	.db #0x3c	; 60
   5C88 68                  157 	.db #0x68	; 104	'h'
   5C89 D5                  158 	.db #0xd5	; 213
   5C8A C0                  159 	.db #0xc0	; 192
   5C8B C0                  160 	.db #0xc0	; 192
   5C8C C0                  161 	.db #0xc0	; 192
   5C8D D5                  162 	.db #0xd5	; 213
   5C8E C0                  163 	.db #0xc0	; 192
   5C8F 3C                  164 	.db #0x3c	; 60
   5C90 68                  165 	.db #0x68	; 104	'h'
   5C91 D5                  166 	.db #0xd5	; 213
   5C92 C0                  167 	.db #0xc0	; 192
   5C93 C0                  168 	.db #0xc0	; 192
   5C94 C0                  169 	.db #0xc0	; 192
   5C95 D5                  170 	.db #0xd5	; 213
   5C96 C0                  171 	.db #0xc0	; 192
   5C97 3C                  172 	.db #0x3c	; 60
   5C98 68                  173 	.db #0x68	; 104	'h'
   5C99 D5                  174 	.db #0xd5	; 213
   5C9A C0                  175 	.db #0xc0	; 192
   5C9B C0                  176 	.db #0xc0	; 192
   5C9C C0                  177 	.db #0xc0	; 192
   5C9D D5                  178 	.db #0xd5	; 213
   5C9E C0                  179 	.db #0xc0	; 192
   5C9F 3C                  180 	.db #0x3c	; 60
   5CA0 3C                  181 	.db #0x3c	; 60
   5CA1 7D                  182 	.db #0x7d	; 125
   5CA2 C0                  183 	.db #0xc0	; 192
   5CA3 3C                  184 	.db #0x3c	; 60
   5CA4 3C                  185 	.db #0x3c	; 60
   5CA5 C0                  186 	.db #0xc0	; 192
   5CA6 BE                  187 	.db #0xbe	; 190
   5CA7 3C                  188 	.db #0x3c	; 60
   5CA8 3C                  189 	.db #0x3c	; 60
   5CA9 68                  190 	.db #0x68	; 104	'h'
   5CAA C0                  191 	.db #0xc0	; 192
   5CAB 3C                  192 	.db #0x3c	; 60
   5CAC 3C                  193 	.db #0x3c	; 60
   5CAD C0                  194 	.db #0xc0	; 192
   5CAE 94                  195 	.db #0x94	; 148
   5CAF 3C                  196 	.db #0x3c	; 60
   5CB0 3C                  197 	.db #0x3c	; 60
   5CB1 68                  198 	.db #0x68	; 104	'h'
   5CB2 C0                  199 	.db #0xc0	; 192
   5CB3 3C                  200 	.db #0x3c	; 60
   5CB4 3C                  201 	.db #0x3c	; 60
   5CB5 C0                  202 	.db #0xc0	; 192
   5CB6 94                  203 	.db #0x94	; 148
   5CB7 3C                  204 	.db #0x3c	; 60
   5CB8 3C                  205 	.db #0x3c	; 60
   5CB9 68                  206 	.db #0x68	; 104	'h'
   5CBA C0                  207 	.db #0xc0	; 192
   5CBB 3C                  208 	.db #0x3c	; 60
   5CBC 3C                  209 	.db #0x3c	; 60
   5CBD C0                  210 	.db #0xc0	; 192
   5CBE 94                  211 	.db #0x94	; 148
   5CBF 3C                  212 	.db #0x3c	; 60
   5CC0 3C                  213 	.db #0x3c	; 60
   5CC1 68                  214 	.db #0x68	; 104	'h'
   5CC2 C0                  215 	.db #0xc0	; 192
   5CC3 3C                  216 	.db #0x3c	; 60
   5CC4 3C                  217 	.db #0x3c	; 60
   5CC5 C0                  218 	.db #0xc0	; 192
   5CC6 94                  219 	.db #0x94	; 148
   5CC7 3C                  220 	.db #0x3c	; 60
   5CC8 3C                  221 	.db #0x3c	; 60
   5CC9 FF                  222 	.db #0xff	; 255
   5CCA FF                  223 	.db #0xff	; 255
   5CCB 3C                  224 	.db #0x3c	; 60
   5CCC 3C                  225 	.db #0x3c	; 60
   5CCD FF                  226 	.db #0xff	; 255
   5CCE BE                  227 	.db #0xbe	; 190
   5CCF 3C                  228 	.db #0x3c	; 60
   5CD0 3C                  229 	.db #0x3c	; 60
   5CD1 FF                  230 	.db #0xff	; 255
   5CD2 FF                  231 	.db #0xff	; 255
   5CD3 3C                  232 	.db #0x3c	; 60
   5CD4 3C                  233 	.db #0x3c	; 60
   5CD5 FF                  234 	.db #0xff	; 255
   5CD6 BE                  235 	.db #0xbe	; 190
   5CD7 3C                  236 	.db #0x3c	; 60
                            237 	.area _INITIALIZER
                            238 	.area _CABS (ABS)
