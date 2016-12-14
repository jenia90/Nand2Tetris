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

(LOOP)
    @KBD
    D=M

    @SETWHITE
    D;JEQ // in case not keys were pressed fill the screen with white lines

    @SETBLACK
    D;JNE // if key was pressed fill black

    @LOOP
    0;JMP

(SETWHITE) // sets the value for pixels as white
	@val
	M=0
	@SETSCREEN
	0;JMP

(SETBLACK) // sets the value for pixels as black
	@val
	M=-1
	@SETSCREEN
	0;JMP


(SETSCREEN)
	@8191
	D=A // set the number of pixels to fill
	@n
	M=D // set the terminal value for the iterator

	@i
	M=0 // zero the counter

	@SCREEN
	D=A // get the screen address
	@address
	M=D // set the address variable to starting position of the screen

	(LINELOOP)
		@i
		D=M
		@n
		D=D-M
		@LOOP
		D;JGT // code above checks if we reached the end of the screen

		@val
		D=M // get the value we want to set our screen to

		@address
		A=M // get screen address
		M=D // set the value at the specified address to whats in our val variable

		@i
		M=M+1 // increment counter
		@address
		M=M+1 // incerement address pointer
		@LINELOOP
		0;JMP