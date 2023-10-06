import unittest
from hasm import Assembler

class TestAssembler(unittest.TestCase):

    def test_a_instruction(self):
        asm_code = "@1"
        machine_code = "0000000000000001"

        a = Assembler(None)
        self.assertEqual(a.process_a_instruction(asm_code), machine_code)

    def test_c_instruction(self):
        asm_code_1 = "D=D+M;JEQ"
        asm_code_2 = "D+M;JMP"
        asm_code_3 = "M;JLE"
        asm_code_4 = "A"

        a = Assembler(None)
        self.assertEqual(a.process_c_instruction(asm_code_1), "1111000010010010")
        self.assertEqual(a.process_c_instruction(asm_code_2), "1111000010000111")
        self.assertEqual(a.process_c_instruction(asm_code_3), "1111110000000110")
        self.assertEqual(a.process_c_instruction(asm_code_4), "1110110000000000")

    def test_parse_line(self):
        asm_code_1 = "@1"
        asm_code_2 = "//comment"
        asm_code_3 = "M;JLE"

        a = Assembler(None)
        self.assertEqual(a.parse_line(asm_code_1), "0000000000000001")
        self.assertEqual(a.parse_line(asm_code_2), None)
        self.assertEqual(a.parse_line(asm_code_3), "1111110000000110")

if __name__ == '__main__':
    unittest.main()