#!/usr/bin/python3

import sys

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

        if self.outfile_p is not None:
            self.outfile_p.close()
