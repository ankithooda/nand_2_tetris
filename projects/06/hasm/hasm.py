#!/usr/bin/python3

import sys

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
        self.line_num = 0
        self.error_found = False

    def _setup_infile(self):
        """Opens the provided file and stores the file object in infile_p attribute.
        """
        try:
            self.infile_p = open(self.infile_path, mode='r', encoding='UTF-8')
        except Exception as any_exception:
            sys.stderr.write(f"Could not read input file {self.infile_path}\n")
            sys.stderr.write(f"Exception {any_exception}\n")
            self._clean_up()
            sys.exit(1)


    def _setup_outfile(self):
        """Opens the output file in write and stores the file object in outfile_p
        attribute.
        """
        self.outfile_p = open(self.outfile_path, mode='w', encoding='UTF-8')

    def _clean_up(self):
        """Closes input and output files, to be called before exiting.
        """
        self.infile_p.close()
        self.outfile_p.close()

    def parse(self):
        """Iterates over the input file and parses it line by line.
        Also writes the parsed machine code to the output file.
        """
        machine_code = []
        for line in self.infile_p.readlines():
            self.line_num = self.line_num + 1
            machine_instruction = self.parse_line(line.strip())
            if machine_instruction is not None:
                machine_code.append(machine_instruction)

        # Write to output file only if no errors were found.
        if self.error_found is False:
            for code in machine_code:
                self.outfile_p.write(code)

        self._clean_up()
        sys.exit(0)


    def parse_line(self, line):
        """Each line in source code can be a comment, A-Instruction or C-Instruction.
        This method identifies the line type and call appropirate method.

        Args:
            line (str): line from source code file.

        Returns:
            str: Machine code translation of the input line.
        """
        if line[0:2] == "//":
            return None
        elif line[0] == "@":
            return self.process_a_instruction(line[1:0])
        else:
            return self.process_c_instruction(line)

    def process_a_instruction(self, line):
        """Generates machine code of A-Instruction.

        Args:
            line (str): The label or number in the A-Instruction.
        """
        try:
            line_out = f"{int(line):016b}"
            return line_out
        except ValueError:
            self.error_found = True
            sys.stderr.write(f"FATAL {self.line_num}: A-Instruction needs a 15-bit number {line}")
        except Exception:
            self.error_found = True
            sys.stderr.write(f"FATAL {self.line_num}: Unknown instruction {line}")

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

        # Get microcode for comp
        if COMP_MICROCODES.get(comp):
            line_out = line_out + COMP_MICROCODES.get(comp)
        else:
            self.error_found = True
            sys.stderr.write(f"FATAL {self.line_num}: Unknown computation {comp}")

        # Get microcode for destination
        if dest is None:
            line_out = line_out + "000"
        else:
            if DEST_MICROCODE.get(dest):
                line_out = line_out + DEST_MICROCODE.get(dest)
            else:
                self.error_found = True
                sys.stderr.write(f"FATAL {self.line_num}: Unknown destination {dest}")

        # Get microcode for jump bits
        if jjj is None:
            line_out = line_out + "000"
        else:
            if JMP_MICROCODE.get(jjj):
                line_out = line_out + JMP_MICROCODE.get(jjj)
            else:
                self.error_found = True
                sys.stderr.write(f"FATAL {self.line_num}: Unknow jump instruction {jjj}")
