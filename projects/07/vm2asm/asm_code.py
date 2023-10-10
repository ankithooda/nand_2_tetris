import sys      # For stderr and stdout


ARTITHMETIC_LOGICAL_2ARGS = {
    "add", "sub", "and", "or"
}

ARTITHMETIC_LOGICAL_1ARG = {"gt", "lt", "eq"}

PUSH_POP = {"push", "pop"}

SEGMENTS = {"lcl", "args", "this", "that", "pointer", "temp", "constant", "static"}

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

    def generate(self, command, args):
        """Returns the Assembly code for a given VM command.

        Args:
            command (str): VM Command
            args (list of strs): Args to the VM command, can be empty.

        Returns:
            str: Assembly Code.
        """

        if command in ARTITHMETIC_LOGICAL_2ARGS:
            return self.arithmetic_logical_2args(command)
        elif command in ARTITHMETIC_LOGICAL_1ARG:
            return self.arithmetic_logical_1_arg(command)
        elif command in PUSH_POP:
            if len(args) != 2:
                raise ASMCodeGenException(f"{command} should have exactly 2 arguments")
            elif args[0] not in SEGMENTS:
                raise ASMCodeGenException(f"{args[0]} is not a valid memory segment")
            elif not args[1].isnumeric():
                raise ASMCodeGenException(f"{args[1]} is not a valid address")
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

    def handle_pop(self, segment, address):
        """Generates code for push command.
        push command pushes the value stored in segment[address] in the stack.

        Args:
            segment (str): Memory segment.
            address (address): Address within the memory segment.

        Returns:
            (list): List of ASM instructions.
        """
        print(segment, address)
        if segment == "constant":
            instructions = self.load_constant(address, "D")
            instructions.extend(self.pop("D"))
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
        """Generates instruction for moving the value stored in RAM[mem_addres]
        to the <register>.

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

        if register == "M":
            return instructions
        else:
            return instructions.append(f"{register}=M")

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
            "A=M",
            f"{register}=M"
        ]
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
            "A=M",
            f"M={register}",
            "@SP",
            "M=M+1"
        ]
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

        operations = ["APPLY OPERATION"] # D=D op M

        if command == "add":
            operations = ["D=D+M"]
        elif command == "sub":
            operations = ["D=D+M"]
        elif command == "and":
            operations = ["D=D&M"]
        elif command == "or":
            operations = ["D=D|M"]
        elif command == "lt":
            print("are we her")
            operations = ["QWER"]
            # operations = [
            #     "@SETTRUE",
            #     "M-D;JEQ",
            #     "D=0",
            #     "(SETTRUE)",
            #     "D=-1"
            # ]

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

        operation = None # D=D op M

        if command == "neg":
            operation = "D=-D"
        elif command == "sub":
            operation = "D=!D"

        instructions.extend(fetch_arg_1)
        instructions.append(operation)
        instructions.extend(store_result)
        return instructions
