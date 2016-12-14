// This file is part of www.nand2tetris.org 

// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/sort.asm

//The program input will be at R14(starting address),R15(length of array).
//The program should sort the array starting at the address in R14 with length specified in R15.

@i
M = 0

@j
M = 0

(OUTER)
	@i
	D=M

	@R15
	D=M-D

	@END //if (n-i) <= 0
	D;JLE

	(INNER)

		@j
		M=M+1 //j++
		D=M

		@R15
		D=M-D

		@ENDIN //if (n-j) <= 0
		D;JLE // jump to inner loop

		@j
		D=M

		@R14
		A=M+D // jump to a[j]
		D=M
		@R1 // temp of a[j]
		M=D

		@i
		D=M

		@R14
		A=M+D // jump to a[i]
		D=M

		@R2 // temp a[i]
		M=D

		@R1
		D=M-D

		@SWAP //if a[i]>a[j]
		D;JGT

		@INNER //jump to inner lop start
		0;JMP

		(SWAP) //swaps a[i] with a[j]
			@i
			D=M

			@R14
			A=M+D
			D=A

			@R3 //a[i]
			M=D

			@j
			D=M

			@R14 
			A=M+D
			D=A

			@R4 //a[j]
			M=D

			@R1 //a[j]
			D=M

			@R3
			A=M
			M=D

			@R2 //a[i]
			D=M

			@R4
			A=M
			M=D

			@INNER // jump to inner loop
			0;JMP

	(ENDIN)
		@i //i++
		M=M+1
		D=M

		@j
		M=D

		@OUTER
		0;JMP
(END)