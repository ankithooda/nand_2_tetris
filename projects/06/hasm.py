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

class Assembler():
    """Class for parsing and assembling HACK ASM files
    """

    def __init__(self, path):
        """Constructor for Assembler objects.

        Args:
            path (string): file_path received from the user.
        """
        self.path = sys.argv[1]
        self.infile_p = None
        self.outfile_p = None

    def _setup_infile(self):
        pass

    def _setup_outfile(self):
        pass

    def parse(self, line):
        pass

    def parse_line(self, line):
        pass

    def process_a_instruction(self, line):
        pass

    def process_c_instruction(self, line):
        pass




