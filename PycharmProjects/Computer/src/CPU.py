from typing import *


class CPU:
    def __init__(self, ram, alu):
        self.alu = alu
        self.ram = ram
        self.reg = dict.fromkeys(["PC", "IR", "ACC", "MAR", "MDR", "FLAGS"], 0x00)
        self.running = True
        self.clock = 0

        self.INSTRUCTIONS: Dict[int, Callable[..., Any]] = {
            0x01: self.LDA,
            0x02: self.STA,
            0x03: self.ADD,
            0x04: self.SUB,
            0x05: self.CMP,
            0x06: self.JMP,
            0x07: self.JZ,
            0x08: self.JNZ,
            0x09: self.AND,
            0x0A: self.OR,
            0x0B: self.XOR,
            0x0C: self.NOT,
            0x0D: self.INC,
            0x0E: self.DEC,
            0x0F: self.SHL,
            0x10: self.SHR,
            0xFF: self.HLT,
        }
        self.INSTRUCTIONS_SIZE = {
            0x01: 2,  # LDA
            0x02: 2,  # STA
            0x03: 2,  # ADD
            0x04: 2,  # SUB
            0x05: 2,  # CMP
            0x06: 2,  # JMP
            0x07: 2,  # JZ
            0x08: 2,  # JNZ
            0x09: 2,  # AND
            0x0A: 2,  # OR
            0x0B: 2,  # XOR
            0x0C: 1,  # NOT
            0x0D: 1,  # INC
            0x0E: 1,  # DEC
            0x0F: 1,  # SHL
            0x10: 1,  # SHR
            0xFF: 1,  # HLT
        }

    # ----------------------- INSTRUCTIONS ----------------------- #
    # --- Lecture ---
    def LDA(self, *args):
        value = args[0]
        self.reg["ACC"] = value  # Charger l'opérande dans l'Accumulateur

    # --- Écriture ---
    def STA(self, *args):
        addr = args[0]
        self.ram.write(addr, self.reg["ACC"])  # Stocker l'accumulateur dans la ram

    # --- Arithmétique ---
    def ADD(self, *args):
        value = args[0]
        self.reg["ACC"] = self.alu.ADD(self.reg["ACC"], value)  # Additionner l'opérande avec l'accumulateur

    def SUB(self, *args):
        value = args[0]
        self.reg["ACC"] = self.alu.SUB(self.reg["ACC"], value)  # Soustraire l'opérande à l'accumulateur

    def INC(self):
        self.reg["ACC"] = self.alu.INC(self.reg["ACC"])

    def DEC(self):
        self.reg["ACC"] = self.alu.DEC(self.reg["ACC"])

    # --- Logique ---
    def AND(self, *args):
        value = args[0]
        self.reg["ACC"] = self.alu.AND(self.reg["ACC"], value)

    def OR(self, *args):
        value = args[0]
        self.reg["ACC"] = self.alu.OR(self.reg["ACC"], value)

    def XOR(self, *args):
        value = args[0]
        self.reg["ACC"] = self.alu.XOR(self.reg["ACC"], value)

    def NOT(self):
        self.reg["ACC"] = self.alu.NOT(self.reg["ACC"])

    # --- Comparaison ---
    def CMP(self, *args):
        value = args[0]
        self.alu.CMP(self.reg["ACC"], value)  # Comparer l'opérande et l'accumulateur

    # --- Déplacement ---
    def SHL(self):
        self.reg["ACC"] = self.alu.SHL(self.reg["ACC"])

    def SHR(self):
        self.reg["ACC"] = self.alu.SHR(self.reg["ACC"])

    # --- Contrôle ---
    def JMP(self, *args):  # Saute à l’adresse mémoire spécifiée
        addr = args[0]
        self.reg["PC"] = addr

    def JZ(self, *args):  # Saute à l’adresse mémoire spécifiée si le flag Z de l'alu = 0
        if self.alu.flags["Z"] == 1:
            addr = args[0]
            self.reg["PC"] = addr

    def JNZ(self, *args):  # Saute à l’adresse mémoire spécifiée si le flag Z de l'alu != 0
        if self.alu.flags["Z"] == 0:
            addr = args[0]
            self.reg["PC"] = addr

    def HLT(self):  # Stop le CPU
        self.running = False

    # ----------------------- RUNNING ----------------------- #
    def step(self):
        self.clock += 1

        # récupérer opcode et operands dans IR
        opcode = self.ram.data[self.reg["PC"]]
        size = self.INSTRUCTIONS_SIZE[opcode]  # récupérer la taille de l'instruction
        self.reg["IR"] = self.ram.data[self.reg["PC"]: self.reg["PC"] + size]
        self.reg["PC"] += size  # Incrémenter le pointeur
        operands = self.reg["IR"][1:]  # Récupérer les operands contenues dans IR

        # Vérifier si l'instruction nécessite des operands
        if size > 1:
            self.INSTRUCTIONS[opcode](*operands)
        else:
            self.INSTRUCTIONS[opcode]()

        if self.clock == 1000 or self.reg["PC"] > 0x80:  # Empêche le CPU de boucler ou de lire les données comme instr
            self.running = False
