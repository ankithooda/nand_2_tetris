from hasm import Assembler

a = Assembler("./max/MaxL.asm")
a._setup_infile()
a._setup_outfile()
a.parse()