@3030
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@3
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
@3040
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@4
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
@32
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THIS
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
@46
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@THAT
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
@3
D=M
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@4
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
@THIS
D=M
@2
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
@THAT
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
