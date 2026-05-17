;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module playerknight
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _sprplayerknight_data
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _INITIALIZED
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area _DABS (ABS)
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area _HOME
	.area _GSINIT
	.area _GSFINAL
	.area _GSINIT
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area _HOME
	.area _HOME
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area _CODE
	.area _CODE
_sprplayerknight_data:
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xbe	; 190
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x7d	; 125
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xbe	; 190
	.db #0xff	; 255
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0x7d	; 125
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xea	; 234
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xbe	; 190
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0x94	; 148
	.db #0xff	; 255
	.db #0xbe	; 190
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xff	; 255
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x7d	; 125
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xc0	; 192
	.db #0xd5	; 213
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x7d	; 125
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xc0	; 192
	.db #0xbe	; 190
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xc0	; 192
	.db #0x94	; 148
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xc0	; 192
	.db #0x94	; 148
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xc0	; 192
	.db #0x94	; 148
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x68	; 104	'h'
	.db #0xc0	; 192
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xc0	; 192
	.db #0x94	; 148
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xbe	; 190
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xff	; 255
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0xff	; 255
	.db #0xbe	; 190
	.db #0x3c	; 60
	.area _INITIALIZER
	.area _CABS (ABS)
