class ASSEMBLEUR:
    def __init__(self, filepath: str, mode: str = "asm"):
        self.filepath = filepath
        self.mode = mode.lower()

        # Dictionnaire des instructions → opcodes
        self.OPCODES = {
            "LDI": 0x01,
            "LDA": 0x02,
            "STA": 0x03,
            "ADD": 0x04,
            "SUB": 0x05,
            "CMP": 0x06,
            "JMP": 0x07,
            "JZ": 0x08,
            "JNZ": 0x09,
            "JN": 0x0A,
            "JNN": 0x0B,
            "AND": 0x0C,
            "OR": 0x0D,
            "XOR": 0x0E,
            "NOT": 0x0F,
            "INC": 0x10,
            "DEC": 0x11,
            "SHL": 0x12,
            "SHR": 0x13,
            "PRT": 0x14,
            "IPT": 0x15,
            "HLT": 0xFF,
        }

    def assemble(self) -> list[int]:
        """Assemble selon le mode choisi (asm, hex, bin)."""
        if self.mode == "asm":
            return self._assemble_asm()
        elif self.mode == "hex":
            return self._assemble_hex()
        elif self.mode == "bin":
            return self._assemble_bin()
        else:
            raise ValueError(f"Mode inconnu : {self.mode}")

    def _assemble_asm(self):
        program = []
        with open(self.filepath, "r") as f:
            for line in f:
                line.strip()
                if line.split() == [] or line.startswith(";"):  # Ignorer les commentaires ou les lignes vides
                    continue

                parts = line.split()
                instr = parts[0].upper()

                if instr not in self.OPCODES:
                    raise ValueError(f"Instruction inconnue: {instr}")

                program.append(self.OPCODES[instr])

                if len(parts) > 1:
                    operand = parts[1]
                    if operand.startswith("0x"):
                        program.append(int(operand, 16))
                    elif operand.startswith("0b"):
                        program.append(int(operand, 2))
                    else:
                        program.append(int(operand))

            return program

    def _assemble_hex(self) -> list[int]:
        """Lit un fichier contenant des nombres hexadécimaux."""
        program = []
        with open(self.filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(";"):
                    continue
                for token in line.split():
                    program.append(int(token, 16))
        return program

    def _assemble_bin(self) -> list[int]:
        """Lit un fichier contenant des nombres binaires."""
        program = []
        with open(self.filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(";"):
                    continue
                for token in line.split():
                    program.append(int(token, 2))
        return program
