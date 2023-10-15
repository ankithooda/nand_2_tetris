ARTITHMETIC_LOGICAL_2ARGS = {
    "add", "sub", "and", "or", "gt", "lt", "eq"
}

ARTITHMETIC_LOGICAL_1ARG = {"neg", "not"}

PUSH_POP = {"push", "pop"}

DYNAMIC_ADDRESS_SEGMENTS = {
    "local": "LCL",
    "argument": "ARGS",
    "this": "THIS",
    "that": "THAT",
}

FIXED_ADDRESS_SEGMENTS = {
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
        self.vmfile_name = vmfile_name

    def get_label(self):
        """Returns a label which can be used for 
        implementing jumps.

        Returns:
            str: Label
        """
        label = f"{self.vmfile_name}_JUMP_{self.label_count}"
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
            elif FIXED_ADDRESS_SEGMENTS.get(args[0]) is None and DYNAMIC_ADDRESS_SEGMENTS.get(args[0]) is None:
                raise ASMCodeGenException(f"{args[0]} is not a valid memory segment\n")
            elif not args[1].isnumeric():
                raise ASMCodeGenException(f"{args[1]} is not a valid address\n")
            elif command == "push":
                return self.handle_push(args[0], args[1])
            elif command == "pop":
                return self.handle_pop(args[0], args[1])    
        else:
            raise ASMCodeGenException(f"Unknown command {command}")

    def handle_push(self, segment, index):
        """Generates code for push command.
        push command pushes the value stored in segment[address] in the stack.

        Args:
            segment (str): Memory segment.
            address (address): Address within the memory segment.

        Returns:
            (list): List of ASM instructions.
        """
        if segment == "constant":
            instructions = self.load_constant(index, "D")
            instructions.extend(self.push("D"))
            return instructions

        else:
            instructions = self.load_actual_address(segment, index)
            instructions.append("D=M")
            instructions.append(self.push("D"))

    def handle_pop(self, segment, index):
        """Generates code for push command.
        push command pushes the value stored in segment[address] in the stack.

        Args:
            segment (str): Memory segment.
            address (address): Address within the memory segment.

        Returns:
            (list): List of ASM instructions.
        """
        instructions = self.pop("D")
        instructions = self.load_actual_address(segment, index)
        instructions.append("M=D")

    def load_actual_address(self, segment, index):
        """Generates instructions to load the actual address for a given segment and index.

        Args:
            segment (str): Segment
            index (int): Index within the segment.
        
        Returns:
            (list): List of ASM instructions.
        """
        instructions = []
        if segment == "static":
            instructions = [
                f"@{self.vmfile_name}_{index}"
            ]
            return instructions

        if segment == "temp":
            address = FIXED_ADDRESS_SEGMENTS.get("temp")+index
            instructions = [
                f"@{address}"
            ]
            return instructions

        if segment == "pointer":
            address = FIXED_ADDRESS_SEGMENTS.get("pointer")+index
            instructions = [
                f"@{address}"
            ]
            return instructions
            
        if DYNAMIC_ADDRESS_SEGMENTS.get(segment) is not None:
            segment_symbol = DYNAMIC_ADDRESS_SEGMENTS.get(segment)
            instructions = [
                f"@{segment_symbol}",
                "D=M",
                f"@{index}",
                "A=A+D"
            ]
            return instructions
        return instructions

    def load_constant(self, constant_value, register):
        """Loads a constant value in Register.

        Args:
            constant_value (integer): Value to be loaded in register.
            register (str): Register name. 
        """
        return [
            f"@{constant_value}",
            f"{register}=A"
        ]

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
