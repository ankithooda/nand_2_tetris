// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Register Uses
// R0 - Lower Bound of Screen Memory
// R1 - Upper Bound of Screen Memory
// R2 - Current Screen Memory address

// Set Lower Bound
@SCREEN
D = A
@R0
M = D

// Set Upper Bound
@SCREEN
D = A
@8192
D = D + A
@R1
M = D

// Set Current
@SCREEN
D = A
@R2
M = D

// Loop for Keyboard check
(KBDCHECK)

@KBD
D = M

@FILLBLACK
D;JNE


@FILLWHITE
D;JEQ

(FILLBLACK)
// Set Black
@R2
A = M
M = -1

// Increment Address
@R2
M = M + 1

// Check Upper Bound
@R2
D = M
@R1
D = M - D
@RESET
D;JLE

@KBDCHECK
0;JMP

(FILLWHITE)
// Set Black
@R2
A = M
M = 0

// Increment Address
@R2
M = M - 1

// Check Lower Bound
@R2
D = M
@R0
D = M - D
@RESET
D;JGE

@KBDCHECK
0;JMP

(RESET)
@SCREEN
D = A
@R2
M = D
@KBDCHECK
0;JMP

