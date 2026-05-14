;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module itesenemies
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _flying_harpy_fly
	.globl _undead_soldier_death
	.globl _undead_soldier_walk
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
_undead_soldier_walk:
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xdb	; 219
	.db #0xff	; 255
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x3c	; 60
	.db #0x18	; 24
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xdb	; 219
	.db #0xff	; 255
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x18	; 24
	.db #0x24	; 36
_undead_soldier_death:
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xdb	; 219
	.db #0xff	; 255
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x3c	; 60
	.db #0x18	; 24
	.db #0x18	; 24
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xdb	; 219
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x3c	; 60
	.db #0x18	; 24
	.db #0x00	; 0
	.db #0x18	; 24
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0x7e	; 126
	.db #0x3c	; 60
	.db #0x18	; 24
	.db #0x00	; 0
_flying_harpy_fly:
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xdb	; 219
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xff	; 255
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x3c	; 60
	.db #0x3c	; 60
	.db #0x7e	; 126
	.db #0xdb	; 219
	.db #0xc3	; 195
	.db #0x7e	; 126
	.db #0x3c	; 60
	.area _INITIALIZER
	.area _CABS (ABS)
