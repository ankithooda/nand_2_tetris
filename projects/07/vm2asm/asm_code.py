import sys      # For stderr and stdout


ARTITHMETIC_LOGICAL_2ARGS = {
    "add", "sub", "and", "or", "gt", "lt", "eq"
}

ARTITHMETIC_LOGICAL_1ARG = {"neg", "not"}

PUSH_POP = {"push", "pop"}

SEGMENTS = {
    "local": 1,
    "argument": 2,
    "this": 3,
    "that": 4,
    "pointer": 3,
    "temp": 5,
    "static": 16,
    "constant": 0
}

class ASMCodeGenException(Exception):
    """Exception class for raising all sorts of error occurring during the 
    translation process

    Args:
        Exception (class): Python base class for exception
    """

    def __init__(self, message):
        """Constructor

        Args:
            message (str): error message.
        """
        self.message = message


class ASMCode():
    """Class implementing the code generation logic.
    """

    def __init__(self, vmfile_name):
        self.label_count = 0
        self.vmfile = vmfile_name

    def get_label(self):
        """Returns a label which can be used for 
        implementing jumps.

        Returns:
            str: Label
        """
        label = str(self.label_count)
        self.label_count = self.label_count + 1
        return label

    def generate(self, command, args):
        """Returns the Assembly code for a given VM command.

        Args:
            command (str): VM Command
            args (list of strs): Args to the VM command, can be empty.

        Returns:
            str: Assembly Code.
        """
        # print(command, args)
        # print(SEGMENTS.get(args[0]))

        if command in ARTITHMETIC_LOGICAL_2ARGS:
            return self.arithmetic_logical_2args(command)
        elif command in ARTITHMETIC_LOGICAL_1ARG:
            return self.arithmetic_logical_1_arg(command)
        elif command in PUSH_POP:
            if len(args) != 2:
                raise ASMCodeGenException(f"{command} should have exactly 2 arguments\n")
            elif SEGMENTS.get(args[0]) is None:
                raise ASMCodeGenException(f"{args[0]} is not a valid memory segment\n")
            elif not args[1].isnumeric():
                raise ASMCodeGenException(f"{args[1]} is not a valid address\n")
            elif command == "push":
                return self.handle_push(args[0], args[1])
            elif command == "pop":
                return self.handle_pop(args[0], args[1])    
        else:
            raise ASMCodeGenException(f"Unknown command {command}")

    def handle_push(self, segment, address):
        """Generates code for push command.
        push command pushes the value stored in segment[address] in the stack.

        Args:
            segment (str): Memory segment.
            address (address): Address within the memory segment.

        Returns:
            (list): List of ASM instructions.
        """
        if segment == "constant":
            instructions = self.load_constant(address, "D")
            instructions.extend(self.push("D"))
            return instructions
        else:
            return self.handle_push_from_segments(segment, address)

    def handle_pop(self, segment, address):
        """Generates code for push command.
        push command pushes the value stored in segment[address] in the stack.

        Args:
            segment (str): Memory segment.
            address (address): Address within the memory segment.

        Returns:
            (list): List of ASM instructions.
        """
        if segment == "constant":
            instructions = self.load_constant(address, "D")
            instructions.extend(self.pop("D"))
            return instructions
        else:
            return self.handle_pop_to_segments(segment, address)

    def handle_push_from_segments(self, segment, address):
        """Push from a segment to stack.

        Args:
            segment (str): segment
            address (int): address
        """
        address = int(address)
        mem_address = SEGMENTS.get(segment) + address
        instructions = ["// PUSH FROM SEGMENT"]
        instructions.extend(self.mem_to_reg(mem_address, "D"))
        instructions.extend(self.push("D"))
        return instructions

    def handle_pop_to_segments(self, segment, address):
        """Pop value from stack to a segment

        Args:
            segment (str): segment
            address (int): address
        """
        address = int(address)
        mem_address = SEGMENTS.get(segment) + address
        instructions = ["// POP TO SEGMENT"]
        instructions.extend(self.pop("D"))
        instructions.extend(self.reg_to_mem("D", mem_address))
        return instructions

    def load_constant(self, constant_value, register):
        """Loads a constant value in Register.

        Args:
            constant_value (integer): Value to be loaded in register.
            register (str): Register name. 
        """

        instructions = [
            "// LOAD CONSTANT",
            f"@{constant_value}",
            f"{register}=A"
        ]
        return instructions

    def reg_to_mem(self, register, address):
        """Generates instruction for moving the value stored in register
        to RAM[mem_addres]
        Does not work for register M.

        Args:
            register (str): Register which holds the value.
            address (int): Memory address
        
        Returns:
            (list): List of ASM Instructions.
        """
        instructions = [
            "// MOVE REG TO MEM",
            f"@{address}",
            f"M={register}"
        ]
        return instructions

    def mem_to_reg(self, address, register):
        """Generated ASM instructions from RAM[address] to <register>.

        Args:
            address (int): Memory address
            register (str): Destination register.

        Returns:
            (list): List of ASM Instructions.
        """
        instructions = [
            "// MOVE MEM TO REG",
            f"@{address}"
        ]

        if register != "M":
            instructions.append(f"{register}=M")
        
        return instructions


    def pop(self, register):
        """Generates ASM code for popping a value from stack and storing it in a register.

        Args:
            register (str): Register where popped valie is stored.

        Returns:
            (list): List of ASM instructions.
        """
        pop_instructions = [
            "// POP FROM STACK",
            "@SP",
            "M=M-1",
            "@SP",
            "A=M",         # This should the set the value in M.
        ]

        # Assign value in M to another register.
        if register != "M":
            pop_instructions.append(f"{register}=M")

        return pop_instructions

    def push(self, register):
        """Generates ASM code for popping a value from stack and storing it in a register.

        Args:
            register (str): The name of register whose value is pushed on to stack.

        Returns:
            (list): List of ASM instructions.
        """
        push_instructions = [
            "// PUSH ON TO STACK",
            "@SP",
            "A=M",          # This puts the value in Register M
            "//",
            "@SP",
            "M=M+1"
        ]
        if register != "M":
            push_instructions[3] = f"M={register}"

        return push_instructions

    def arithmetic_logical_2args(self, command):
        """Generates code for Arithmetic-Logical 2 Argument commands.

        Supported commands
        - add, sub, and, or, lt, gt, eq

        Returns:
            (list): List of instructions.
        """
        instructions = [f"// PROCESS COMMAND {command}"]
        fetch_arg_1 = self.pop("D")
        fetch_arg_2 = self.pop("M")
        store_result = self.push("D")

        operations = [] # D=D op M

        if command == "add":
            operations = ["D=M+D"]

        elif command == "sub":
            operations = ["D=M-D"]

        elif command == "and":
            operations = ["D=M&D"]

        elif command == "or":
            operations = ["D=M|D"]

        elif command == "lt":
            settrue_label = f"SETTRUE_{self.get_label()}"
            jump_end_label = f"JUMP_END_{self.get_label()}"

            operations = [
                "D=M-D",
                f"@{settrue_label}",
                "D;JLT",
                "D=0",
                f"@{jump_end_label}",
                "0;JMP",
                f"({settrue_label})",
                "D=-1",
                f"({jump_end_label})"
            ]

        elif command == "eq":
            settrue_label = f"SETTRUE_{self.get_label()}"
            jump_end_label = f"JUMP_END_{self.get_label()}"

            operations = [
                "D=M-D",
                f"@{settrue_label}",
                "D;JEQ",
                "D=0",
                f"@{jump_end_label}",
                "0;JMP",
                f"({settrue_label})",
                "D=-1",
                f"({jump_end_label})"
            ]

        elif command == "gt":
            settrue_label = f"SETTRUE_{self.get_label()}"
            jump_end_label = f"JUMP_END_{self.get_label()}"

            operations = [
                "D=M-D",
                f"@{settrue_label}",
                "D;JGT",
                "D=0",
                f"@{jump_end_label}",
                "0;JMP",
                f"({settrue_label})",
                "D=-1",
                f"({jump_end_label})"
            ]

        instructions.extend(fetch_arg_1)
        instructions.extend(fetch_arg_2)
        instructions.extend(operations)
        instructions.extend(store_result)
        return instructions

    def arithmetic_logical_1_arg(self, command):
        """Generates code for Arithmetic-Logical 2 Argument commands.

        Supported commands
        - add, sub, and, or

        Returns:
            (list): List of instructions.
        """
        instructions = [f"// PROCESS COMMAND {command}"]
        fetch_arg_1 = self.pop("D")
        store_result = self.push("D")

        operation = [] # D=D op M

        if command == "neg":
            operation = ["D=-D"]
        elif command == "not":
            operation = ["D=!D"]

        instructions.extend(fetch_arg_1)
        instructions.extend(operation)
        instructions.extend(store_result)
        return instructions
