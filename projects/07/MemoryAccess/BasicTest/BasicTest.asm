@10
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@0
A=A+D
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@21
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@22
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@2
A=A+D
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@ARG
D=M
@1
A=A+D
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@36
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@6
A=A+D
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@42
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@45
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@5
A=A+D
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@THAT
D=M
@2
A=A+D
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@510
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@11
D=A
@R13
M=D
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
@LCL
D=M
@0
A=A+D
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@5
A=A+D
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
// PROCESS COMMAND add
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M+D
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@1
A=A+D
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
// PROCESS COMMAND sub
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M-D
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@6
A=A+D
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@6
A=A+D
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
// PROCESS COMMAND add
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M+D
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
// PROCESS COMMAND sub
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M-D
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@11
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
// PROCESS COMMAND add
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M
// POP FROM STACK
@SP
M=M-1
@SP
A=M
D=M+D
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
