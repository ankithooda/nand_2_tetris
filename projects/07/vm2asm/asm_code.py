import sys      # For stderr and stdout

VM_COMMANDS = {
    "push": [],
    "pop": [],
    "add": [],
    "sub": [],
    "neg": [],
    "eq": [],
    "gt": [],
    "lt": [],
    "and": [],
    "or": [],
    "not": []
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
            return "ASMCODE"
        else:
            return None
