@7
D=A
// PUSH ON TO STACK
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
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
