#!/usr/bin/python3

import sys

class SymbolTable():
    """Class representing the Symbb
    """

    def __init__(self):
        self.table = {}

    def add_entry(self, symbol, address):
        """Add an entry into the symbol table. 
        
        Args:
            symbol (string): symbol found in the assembly instruction.
            address (integer): address
        """
        self.table[symbol] = address

    def contains(self, symbol):
        """Check whether the symbol table contains a given symbol or not.

        Args:
            symbol (string): Symbol to be checked.

        Returns:
            boolean: True/False based on whether symbol exists in table.
        """
        return self.table.get(symbol) is not None

    def get_address(self, symbol):
        """Get Address corresponding to the symbol.
        Returns None if symbol does not exist.

        Args:
            symbol (string): Symbol

        Returns:
            integer: Address corresponding to the symbol.
        """
        return self.table.get(symbol)

COMP_MICROCODES = {
    "0"     : "0101010",
    "1"     : "0111111",
    "-1"    : "0111010",
    "D"     : "0001100",
    "A"     : "0110000",
    "!D"    : "0001101",
    "!A"    : "0110001",
    "-D"    : "0001111",
    "-A"    : "0110011",
    "D+1"   : "0011111",
    "A+1"   : "0110111",
    "D-1"   : "0001110",
    "A-1"   : "0110010",
    "D+A"   : "0000010",
    "D-A"   : "0010011",
    "A-D"   : "0000111",
    "D&A"   : "0000000",
    "D|A"   : "0010101",
    "M"     : "1110000",
    "!M"    : "1110001",
    "-M"    : "1110011",
    "M+1"   : "1110111",
    "M-1"   : "1110010",
    "D+M"   : "1000010",
    "D-M"   : "1010011",
    "M-D"   : "1000111",
    "D&M"   : "1000000",
    "D|M"   : "1010101"
}

DEST_MICROCODE = {
    "M"   : "001",
    "D"   : "010",
    "DM"  : "011",
    "A"   : "100",
    "AM"  : "101",
    "AD"  : "110",
    "ADM" : "111"
}

JMP_MICROCODE = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

class Assembler():
    """Class for parsing and assembling HACK ASM files
    """

    def __init__(self, path):
        """Constructor for Assembler objects.

        Args:
            path (string): file_path received from the user.
        """
        self.infile_path = path
        self.outfile_path = "out.bin"
        self.infile_p = None
        self.outfile_p = None

    def _setup_infile(self):
        try:
            self.infile_p = open(self.infile_path, mode='r', encoding='UTF-8')
        except Exception as e:
            sys.stderr.write(f"Could not read input file {self.infile_path}\n")
            sys.stderr.write(f"Exception {e}\n")


    def _setup_outfile(self):
            self.outfile_p = open(self.outfile_path, mode='w', encoding='UTF-8')


    def parse(self):
        while True:
            line = self.infile_p.readline()

            if line is None:
                sys.exit(0)
            elif len(line) < 2:
                continue
            else:
                self.parse_line(line.strip())


    def parse_line(self, line):
        print(line)
        if line[0:2] == "//":
            pass
        elif line[0] == "@":
            self.process_a_instruction(line)
        else:
            self.process_c_instruction(line)

    def process_a_instruction(self, line):
        print("A")
        pass

    def process_c_instruction(self, line):
		line = line.replace(" ", "").replace("\t", "")
        
		
        print("C")
        pass




