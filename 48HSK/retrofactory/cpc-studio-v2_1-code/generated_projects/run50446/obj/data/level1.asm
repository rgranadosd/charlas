;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.6.8 #9946 (Mac OS X ppc)
;--------------------------------------------------------
	.module level1
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _gpalette
	.globl _level1tileproperties
	.globl _level1tilemap
	.globl _level1tilemapheight
	.globl _level1tilemapwidth
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
_level1tilemapwidth:
	.dw #0x0014
_level1tilemapheight:
	.dw #0x0012
_level1tilemap:
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x01	; 1
_level1tileproperties:
	.db #0x00	; 0
	.db #0x01	; 1
_gpalette:
	.db #0x14	; 20
	.db #0x04	; 4
	.db #0x15	; 21
	.db #0x1c	; 28
	.db #0x0c	; 12
	.db #0x05	; 5
	.db #0x16	; 22
	.db #0x06	; 6
	.db #0x17	; 23
	.db #0x1e	; 30
	.db #0x00	; 0
	.db #0x0e	; 14
	.db #0x07	; 7
	.db #0x12	; 18
	.db #0x0a	; 10
	.db #0x0b	; 11
	.area _INITIALIZER
	.area _CABS (ABS)
