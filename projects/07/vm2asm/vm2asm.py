#!/usr/bin/python3

import sys
from asm_code import ASMCode

class VM2ASM():
    """VM2ASM Class
       1. Implements File I/O and Parsing
    """

    def __init__(self, infile, outfile):
        """Constructor for VM2ASM

        Args:
            infile (str): Input .vm file
            outfile (str): Output .asm file
        """

        self.infile_path = infile
        self.outfile_path = outfile
        self.infile_p = None
        self.outfile_p = None
        self.line_num = 0
        self.error_found = False
        self.asm_code = ASMCode()
        self.generated_code = []


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

    def _reset_inputfile(self):
        """
        1. Resets the opened input file back to the first line.
        2. Resets self.line_num to 0.
        This method should be called before both passes of the assembler.
        """
        self.infile_p.seek(0)
        self.line_num = 0

    def _clean_up(self):
        """Closes input and output files, to be called before exiting.
        """
        if self.infile_p is not None:
            self.infile_p.close()
            self.infile_p = None

        if self.outfile_p is not None:
            self.outfile_p.close()
            self.outfile_p = None

    def write_outfile(self):
        """Write to output file if there were no errors
        """
        # Write to output file only if no errors were found.
        if self.error_found is False:
            self.setup_outfile()
            for code in self.generated_code:
                self.outfile_p.write(f"{code}\n")
            self.outfile_p.flush()
        self._clean_up()

    def parse(self):
        """Reads the input line by line and uses ASMCode module to
        generate Assembly code.
        """
        self.setup_infile()
        for line in self.infile_p.readlines():
            line = line.strip()
            self.line_num = self.line_num + 1
            if len(line) == 0 or line[0:2] == "//":
                continue
            else:
                tokens = line.split(" ")
                command = tokens[0]
                args = tokens[1:]
                code = self.asm_code.generate(command, args)

                if code is not None:
                    self.generated_code.append(code)
                else:
                    self.error_found = True
                    sys.stderr.write(f"Can not generated code for command {line}")


def print_help():
    """Prints help message.
    """
    help_message = '''
    VM2ASM 
    Generates ASM code for .vm file
    Usage
    ./vm2asm.py <input .vm file> <out .asm file>

    '''
    sys.stdout.write(help_message)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_help()
    else:
        assembler = VM2ASM(sys.argv[1], sys.argv[2])
        assembler.setup_infile()
        assembler.parse()
        assembler.write_outfile()
    sys.exit(0)
