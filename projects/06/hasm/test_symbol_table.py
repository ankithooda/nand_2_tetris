from symbol_table import SymbolTable

# a = Assembler("./max/MaxL.asm")
# a._setup_infile()
# a._setup_outfile()
# a.parse()

class TestSymbolTable():
    """Test class for the Symbol Table
    """

    def test_add_entry(self):
        """_summary_
        """
        s = SymbolTable()
        s.add_entry("LOOP", 30)
        assert(s.contains("LOOP"))
