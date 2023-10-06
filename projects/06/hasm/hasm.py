#!/usr/bin/python3

import sys
from symbol_table import SymbolTable

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

    def __init__(self, infile, outfile):
        """Constructor for Assembler objects.

        Args:
            path (string): file_path received from the user.
        """
        self.infile_path = infile
        self.outfile_path = outfile
        self.infile_p = None
        self.outfile_p = None
        self.line_num = 0
        self.error_found = False
        self.machine_code = []
        self.sym_table = SymbolTable()

    def setup_infile(self):
        """Opens the provided file and stores the file object in infile_p attribute.
        """
        try:
            self.infile_p = open(self.infile_path, mode='r', encoding='UTF-8')
        except Exception as any_exception:
            sys.stderr.write(f"Could not read input file {self.infile_path}\n")
            sys.stderr.write(f"Exception {any_exception}\n")
            self._clean_up()
            sys.exit(1)


    def setup_outfile(self):
        """Opens the output file in write and stores the file object in outfile_p
        attribute.
        """
        try:
            self.outfile_p = open(self.outfile_path, mode='w', encoding='UTF-8')
        except Exception as any_exception:
            sys.stderr.write(f"Could not open output file {self.infile_path}\n")
            sys.stderr.write(f"Exception {any_exception}\n")
            self._clean_up()
            sys.exit(1)        

    def _clean_up(self):
        """Closes input and output files, to be called before exiting.
        """
        self.infile_p.close()
        self.outfile_p.close()

    def seed_symbol_table(self):
        """Seeds the symbol table with predefined symbol,
        """
        self.sym_table.add_entry("R0", 0)
        self.sym_table.add_entry("R1", 1)
        self.sym_table.add_entry("R2", 2)
        self.sym_table.add_entry("R3", 3)
        self.sym_table.add_entry("R4", 4)
        self.sym_table.add_entry("R5", 5)
        self.sym_table.add_entry("R6", 6)
        self.sym_table.add_entry("R7", 7)
        self.sym_table.add_entry("R8", 8)
        self.sym_table.add_entry("R9", 9)
        self.sym_table.add_entry("R10", 10)
        self.sym_table.add_entry("R11", 11)
        self.sym_table.add_entry("R12", 12)
        self.sym_table.add_entry("R13", 13)
        self.sym_table.add_entry("R14", 14)
        self.sym_table.add_entry("R15", 15)

        self.sym_table.add_entry("SP", 0)
        self.sym_table.add_entry("LCL", 1)
        self.sym_table.add_entry("ARG", 2)
        self.sym_table.add_entry("THIS", 3)
        self.sym_table.add_entry("THAT", 4)

        self.sym_table.add_entry("SCREEN", 16384)
        self.sym_table.add_entry("KBD", 24576)



    def build_symbol_table(self):
        """
        First Pass on the input file.
        - Builds symbol table.
        - Ignore comments and empty lines
        """
        self.infile_p.seek(0)
        unassigned_symbol = None
        address = 0
        for line in self.infile_p.readlines():
            self.line_num = self.line_num + 1
            line = line.strip()
            # print(f"--{line}--")
            if len(line) == 0 or line[0:2] == '//':
                continue
            elif line[0] == '(':
                symbol = line[1:-1]
                if unassigned_symbol is None:
                    unassigned_symbol = symbol
                else:
                    sys.stderr.write(f"FATAL {self.line_num} : Can not have two symbol declarations on after another")
            else:
                if unassigned_symbol is not None:
                    self.sym_table.add_entry(unassigned_symbol, address)
                unassigned_symbol = None
                address = address + 1

    def parse(self):
        """Iterates over the input file and parses it line by line.
        Also writes the parsed machine code to the output file.
        """
        self.infile_p.seek(0)
        for line in self.infile_p.readlines():
            self.line_num = self.line_num + 1
            machine_instruction = self.parse_line(line)
            if machine_instruction is not None:
                self.machine_code.append(machine_instruction)

    def write_outfile(self):
        # Write to output file only if no errors were found.
        if self.error_found is False:
            for code in self.machine_code:
                self.outfile_p.write(f"{code}\n")
            
            self.outfile_p.flush()
        self._clean_up()

    def parse_line(self, line):
        """Each line in source code can be a comment, A-Instruction or C-Instruction.
        This method identifies the line type and call appropirate method.

        Args:
            line (str): line from source code file.

        Returns:
            str: Machine code translation of the input line.
        """
        line = line.strip()
        if len(line) == 0:
            return None
        elif line[0:2] == "//":
            return None
        elif line[0] == "@":
            return self.process_a_instruction(line)
        else:
            return self.process_c_instruction(line)

    def process_a_instruction(self, line):
        """Generates machine code of A-Instruction.

        Args:
            line (str): A-Instruction.
        """
        line = line[1:]
        if line.isnumeric():
            line = int(line)
        elif self.sym_table.contains(line):
            line = self.sym_table.get_address(line)
        else:
            sys.stderr.write(f"FATAL {self.line_num}: Uknown Symbol {line}")
            return None

        line_out = f"{line:016b}"
        return line_out

    def process_c_instruction(self, line):
        """Generates machine code of C-Instruction.

        Args:
            line (str): C-Instruction
        """
        line = line.replace(" ", "").replace("\t", "")
        line_out = "111"
        dest = None
        comp = None
        jjj = None

        if line.find("=") != -1:
            dest, line = line.split("=")

        if line.find(";") != -1:
            comp, jjj = line.split(";")
        else:
            comp = line

        # Get microcode for comp
        if COMP_MICROCODES.get(comp):
            line_out = line_out + COMP_MICROCODES.get(comp)
        else:
            self.error_found = True
            sys.stderr.write(f"FATAL {self.line_num}: Unknown computation {comp}\n")
            return None

        # Get microcode for destination
        if dest is None:
            line_out = line_out + "000"
        else:
            dest = ''.join(sorted(dest))
            if DEST_MICROCODE.get(dest):
                line_out = line_out + DEST_MICROCODE.get(dest)
            else:
                self.error_found = True
                sys.stderr.write(f"FATAL {self.line_num}: Unknown destination {dest}\n")
                return None

        # Get microcode for jump bits
        if jjj is None:
            line_out = line_out + "000"
        else:
            if JMP_MICROCODE.get(jjj):
                line_out = line_out + JMP_MICROCODE.get(jjj)
            else:
                self.error_found = True
                sys.stderr.write(f"FATAL {self.line_num}: Unknow jump instruction {jjj}\n")
                return None

        return line_out

def print_help():
    """Prints help message.
    """
    usage = '''
    HACK Assembler
    Usage:
        hasm.py <input file> <output file>
    '''
    print(usage)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_help()
    else:
        assembler = Assembler(sys.argv[1], sys.argv[2])
        assembler.setup_infile()
        assembler.seed_symbol_table()
        assembler.build_symbol_table()
        # assembler.sym_table.debug()
        assembler.parse()
        assembler.setup_outfile()
        assembler.write_outfile()
    sys.exit(0)
