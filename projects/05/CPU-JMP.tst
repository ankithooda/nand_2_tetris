// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/CPU-external.tst

load CPU.hdl,
output-file CPU-JMP.out,
// compare-to CPU-JMP.cmp,
output-list time%S0.4.0 inM%D0.6.0 instruction%B0.16.0 reset%B2.1.2 outM%D1.6.0 writeM%B3.1.3 addressM%D0.5.0 pc%D0.5.0;

// No JMP

set instruction %B0000000011111111, // @3
tick, tock;

set instruction %B1110110000010000, // D=A
tick, tock;

set instruction %B0000000011111111, // @3
tick, tock;

set instruction %B1110010011000000, // D-A
tick, tock, output;

// JGT - Should Jump

set instruction %B0000000011111111, // @3
tick, tock;

set instruction %B1110110000010000, // D=A
tick, tock;

set instruction %B0000000001111111, // @3
tick, tock;

set instruction %B1110010011000001, // D-A;JGT
tick, tock, output;

// JGT - Should Not Jump

set instruction %B0000000011111111, // @3
tick, tock;

set instruction %B1110110000010000, // D=A
tick, tock;

set instruction %B0000000011111111, // @3
tick, tock;

set instruction %B1110010011000001, // D-A;JGT
tick, tock, output;

// JGT - Should Not Jump

set instruction %B0000000001111111, // @3
tick, tock;

set instruction %B1110110000010000, // D=A
tick, tock;

set instruction %B0000000011111111, // @3
tick, tock;

set instruction %B1110010011000001, // D-A;JGT
tick, tock, output;
