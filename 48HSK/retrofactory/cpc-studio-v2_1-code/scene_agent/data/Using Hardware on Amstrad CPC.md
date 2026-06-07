





Espacios

🌎
retrostudio

Avatar de usuario
🌎




Using Hardware on Amstrad CPC.md
Fırat Salgür

/index /about

Keyboard Scanning Directly Using Hardware on Amstrad CPC
Oct 23, 2020

This document describes how the keyboard matrix is accessed on Amstrad CPC 464/6128 without the firmware. The two chips responsible for this are the Intel 8255 (PPI), and AY-3-8912 (PSG).

Intel 8255 (PPI), AY-3-8912 (PSG) and Keyboard Matrix Fig. 1 (source: Cpcwiki)

Table of Contents
Intel 8255 (PPI)

AY-3-8912 (PSG)

How Keyboard Matrix Bits Are Sampled

Keyboard Matrix

Example

1 Intel 8255 (PPI)
8255 allows sharing the CPU bus with multiple I/O components. It has three 8-bit port registers, and a control register for setting the direction of these ports. For keyboard purposes, we are interested in Port A, Port C, and the control register.

Port A is connected to AY-3-8912's data pins. Port C's upper two bits are connected to AY-3-8912's control registers BDIR and BC1. These are outlined with a blue rectangle in Figure 1. Port C's lower 4 bits are connected to 74ls145 decoder, which then is connected to the keyboard matrix rows. Of the 4-bits, only from 0 to 10 are used for selecting the bit line. Keyboard columns are handled by the AY-3-8912. These are outlined with a green rectangle in Figure 1.

2 AY-3-8912 (PSG)
AY-3-8912 is a sound generator, but also contains two general purpose I/O port registers. One of the ports is connected to keyboard matrix columns. With the PPI's 10 bit lines, this allows sampling 10*8, 80 unique keys from the keyboard.

3 How Keyboard Matrix Bits Are Sampled
The main idea is to configure PPI and PSG so that we select the bit line we want to sample. This involves the following steps:

Set PPI's Port A and C as output:

text
ld     bc, #f782
out    (c), c
Select PSG's register 14 on Port A:

text
ld     bc, #f40e
out    (c), c
Latch PSG register:

text
ld     bc, #f6c0
out    (c), c
ld     bc, #f600
out    (c), c
Set PPI's Port A as input and C as output:

text
ld     bc, #f792
out    (c), c
Select the keyboard matrix row want to sample:
text
ld     bc, #f640
out    (c), c
Sample the value on Port A:

text
ld     b, #f4
in     a, (c)
This will have the first row of keyboard matrix in accumulator.

We can write a routine to sample all 10 rows into a buffer if necessary.

4 Keyboard Matrix
Bit						Line	Line			
0	1	2	3	4	5	6	7	8	9
7	f.	f0	Ctrl	>,	< .	Space	V	X	Z	Del
6	Enter	f2	` \|? /|M|N|B|C|Caps<br>Lock|Unused|							
5	f3	f1	Shift	* :	K	J	F / Joy 1 Fire 1	D	A	Joy 0 Fire
1
4	f6	f5	f4	+ ;	L	H	G / Joy 1 Fire 2	S	Tab	Joy 0 Fire
2
3	f9	f8	} ]	P	I	Y	T / Joy 1 Right	W	Q	Joy 0
Right
2	Cursor
Down	f7	Return		@	O	U	R / Joy 1 Left	E	Esc
1	Cursor
Right	Copy	{ [	= -	) 9	
' 7	% 5 / Joy 1
Down	#
3	" 2	Joy 0
Down
0	Cursor Up	Cursor
Left	Clr	Â£
^	
0	( 8	& 6 / Joy 1 Up	$ 4	! 1	Joy 0 Up
Keyboard Scan Matrix (source: http://cpctech.cpcwiki.de/docs/keyboard.html)

5 Example
The below routine will check line 8, which contains ESC key.

text
keypres di
        ld      bc, #f782
        out     (c), c
        ld      bc, #f40e
        out     (c), c
        ld      bc, #f6c0
        out     (c), c
        ld      bc, #f600
        out     (c), c
        ld      bc, #f792
        out     (c), c
        ld      bc, #f648
        out     (c), c
        ld      b, #f4
        in      a, (c)
        ei
        ret
It can be used when firmware is not an option.

 1 Login

0 Comments

==> picture [559 x 435] intentionally omitted <==

----- Start of picture text -----

G Start the discussion…
LOG IN WITH OR SIGN UP WITH DISQUS ?
Name
 Share Best Newest Oldest
Be the 3rst to comment.
Subscribe Privacy Do Not Sell My Data
Fırat Salgür
Fırat Salgür neuro-sys
firatsalgur
**----- End of picture text -----**
