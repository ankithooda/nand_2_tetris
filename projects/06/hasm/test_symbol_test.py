import unittest
from symbol_table import SymbolTable


class TestSymbolTableMethods(unittest.TestCase):
    """Test add_entry method. We use contains method to assert.
    """

    def test_all_method(self):
        """Test all methods.
        """
        sym_table = SymbolTable()
        test_symbol = "LOOP"
        test_address = 30

        sym_table.add_entry("LOOP", 30)

        self.assertTrue(sym_table.contains(test_symbol))
        self.assertEqual(sym_table.get_address(test_symbol), test_address)
        self.assertFalse(sym_table.contains("LOOP1"))

if __name__ == '__main__':
    unittest.main()
