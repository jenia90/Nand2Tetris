@256
D = A
@SP
M = D
@RETURN1
D = A
@SP
A = M
M = D 
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
D = M
@5
D = D - A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.init
0;JMP
(RETURN1)
(SimpleFunction.test)
@SP
A = M
M = 0 
@SP
M = M + 1
@SP
A = M
M = 0 
@SP
M = M + 1
@0
D=A
@LCL
A = M+D
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@1
D=A
@LCL
A = M+D
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M + D
@SP
M = M + 1
@SP
M = M - 1
A = M
M = !M
@SP
M = M + 1
@0
D=A
@ARG
A = M+D
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M + D
@SP
M = M + 1
@1
D=A
@ARG
A = M+D
D = M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M - D
@SP
M = M + 1
@LCL
D = M
@R14
M = D
@5
D = A
@R14
D = M - D
A = D
D = M
@R15
M = D
@0
D = A
@ARG
A = M
D = A + D
@R13
M = D
@SP
M = M - 1
A = M
D = M
@R13
A = M
M = D
@ARG
D = M
@SP
M = D + 1
@R14
M = M - 1
A = M
D = M
@THAT
M = D
@R14
M = M - 1
A = M
D = M
@THIS
M = D
@R14
M = M - 1
A = M
D = M
@ARG
M = D
@R14
M = M - 1
A = M
D = M
@LCL
M = D
@R15
A = M
0;JMP
