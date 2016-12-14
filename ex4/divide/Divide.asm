@R13
D=M
@div
M=D

@R14
D=M
@den
M=D

@R15
M=0

@c
M=1

@den
D=M
@div
D=D-M
@END
D;JGT
@EQUALS
D;JEQ

(LOOP1)
	@div
	D=M
	@den
	D=D-M
	@NEXT
	D;JLT

	@den
	M=M<<
	@c
	M=M<<
	@LOOP1
	0;JMP
	
(NEXT)
	@den
	M=M>>
	@c
	M=M>>

	(LOOP2)
		@c
		D=M
		@END
		D;JEQ

		@den
		D=M
		@div
		D=M-D
		@IFDIV
		D;JLT

		@div
		M=D
		@c
		D=M
		@R15
		M=M+D

		(IFDIV)
			@c
			M=M>>
			@den
			M=M>>
			@LOOP2
			0;JMP


(EQUALS)
	@R15
	M=1

(END)

