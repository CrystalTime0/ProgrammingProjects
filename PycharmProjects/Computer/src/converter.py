from typing import *

filepath = "prgm/"
file_name = "even_or_odd.txt"

# Dictionnaire des instructions → opcodes
OPCODES = {
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


def _assemble_asm():
    program = []
    with open(filepath + "asm/" + file_name, "r") as f:
        for line in f:
            line.strip()
            if line.split() == [] or line.startswith(";"):  # Ignorer les commentaires ou les lignes vides
                continue

            parts = line.split()
            instr = parts[0].upper()

            if instr not in OPCODES:
                raise ValueError(f"Instruction inconnue: {instr}")

            program.append(OPCODES[instr])

            if len(parts) > 1:
                operand = parts[1]
                if operand.startswith("0x"):
                    program.append(int(operand, 16))
                elif operand.startswith("0b"):
                    program.append(int(operand, 2))
                else:
                    program.append(int(operand))

        return program


def convert(prgm: List[int], mode: str = "hex") -> List:
    converted_prgm: List = []
    for value in prgm:
        if code_mode == "hex":
            converted_prgm.append(f"{value:02X}")
        elif code_mode == "bin":
            converted_prgm.append(f"{value:08b}")

    return converted_prgm


def make_and_write_file(prgm: List, file_path: str):
    with open(file_path, "w") as f:
        f.write(" ".join(str(x) for x in prgm))


if __name__ == "__main__":
    code = _assemble_asm()
    for code_mode in ["hex", "bin"]:
        tmp_filepath = filepath + code_mode + "/" + file_name
        make_and_write_file(convert(code, code_mode), tmp_filepath)
