import sys      # For stderr and stdout

VM_COMMANDS = {
    "push": "push",
    "pop": "pop",
    "add": "add",
    "sub": "sub",
    "neg": "neg",
    "eq": "eq",
    "gt": "gt",
    "lt": "lt",
    "and": "and",
    "or": "or",
    "not": "not"
}

MEMORY_SEGMENTS = {
    "constant": "constant"
}

REGISTERS = {
    "A": "A",
    "D": "D",
    "M": "M"
}

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

        if VM_COMMANDS.get(command) is not None:
            if command == "push":
                return self.handle_push(args[0], args[1])
            elif command == "add":
                return self.add()
            else:
                sys.stderr.write(f"Unhandled command {command}\n")
        else:
            return None

    def _add_newline(self, instructions):
        return list(map(lambda x: x+"\n", instructions))

    def handle_push(self, segment, address):
        """Generates code for push command.
        push command pushes the value stored in segment[address] in the stack.

        Args:
            segment (str): Memory segment.
            address (address): Address within the memory segment.

        Returns:
            _type_: _description_
        """
        if segment == "constant":
            instructions = [f"@{address}"]
            instructions.extend(self.push("A"))
            return self._add_newline(instructions)
        else:
            sys.stderr.write(f"Unsupported segment {segment}\n")
            return None

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
        instructions = [f"@{address}"]

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
            "@SP",
            "A=M",
            f"{register}=M",
            "@SP",
            "M=M-1"
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
            "@SP",
            "A=M",
            f"M={register}",
            "@SP",
            "M=M+1"
        ]
        return push_instructions

    def add(self):
        """Generates code for ADD command.

        Returns:
            _type_: _description_
        """
        i1 = self.pop("D")
        i2 = self.pop("M")
        i3 = ["D=D+M"]
        i4 = self.push("D")

        i1.extend(i2)
        i1.extend(i3)
        i1.extend(i4)
        return i1
