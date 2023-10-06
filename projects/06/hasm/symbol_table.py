class SymbolTable():
    """Class representing the Symbol Table
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