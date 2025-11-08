from typing import *


class CPU:
    def __init__(self, ram, alu):
        self.alu = alu
        self.ram = ram
        self.reg = dict.fromkeys(["PC", "IR", "ACC", "MAR", "MDR", "FLAGS"], 0x00)
        self.running = True
        self.clock = 0

        self.INSTRUCTIONS: Dict[int, Callable[..., Any]] = {
            0x01: self.LDI,
            0x02: self.LDA,
            0x03: self.STA,
            0x04: self.ADD,
            0x05: self.SUB,
            0x06: self.CMP,
            0x07: self.JMP,
            0x08: self.JZ,
            0x09: self.JNZ,
            0x0A: self.JN,
            0x0B: self.JNN,
            0x0C: self.AND,
            0x0D: self.OR,
            0x0E: self.XOR,
            0x0F: self.NOT,
            0x10: self.INC,
            0x11: self.DEC,
            0x12: self.SHL,
            0x13: self.SHR,
            0x14: self.PRT,
            0x15: self.IPT,
            0xFF: self.HLT,
        }
        self.INSTRUCTIONS_SIZE = {
            0x01: 2,  # LDI (val)
            0x02: 2,  # LDA (addr)
            0x03: 2,  # STA (addr)
            0x04: 2,  # ADD (val)
            0x05: 2,  # SUB (val)
            0x06: 2,  # CMP (val)
            0x07: 2,  # JMP (addr)
            0x08: 2,  # JZ (addr)
            0x09: 2,  # JNZ (addr)
            0x0A: 2,  # JN (addr)
            0x0B: 2,  # JNN (addr)
            0x0C: 2,  # AND (val)
            0x0D: 2,  # OR  (val)
            0x0E: 2,  # XOR (val)
            0x0F: 1,  # NOT
            0x10: 1,  # INC
            0x11: 1,  # DEC
            0x12: 1,  # SHL
            0x13: 1,  # SHR
            0x14: 2,  # PRT (addr)
            0x15: 1,  # IPT
            0xFF: 1,  # HLT
        }

    # ----------------------- INSTRUCTIONS ----------------------- #
    # --- Lecture ---
    def LDI(self, *args):
        value = args[0]
        self.reg["ACC"] = value  # Charger l'opérande dans l'Accumulateur

    def LDA(self, *args):
        addr = args[0]
        self.reg["ACC"] = self.ram.read(addr)

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

    # --- I/O ---
    def PRT(self, *args):
        addr = args[0]
        print(self.ram.data[addr])
    def IPT(self):
        self.reg["ACC"] = int(input("?"))

    # --- Contrôle ---
    def JMP(self, *args):  # Saute à l’adresse mémoire spécifiée
        addr = args[0]
        self.reg["PC"] = addr

    def JZ(self, *args):  # Saute à l’adresse mémoire spécifiée si le flag Z de l'alu = 1
        if self.alu.flags["Z"] == 1:
            addr = args[0]
            self.reg["PC"] = addr

    def JNZ(self, *args):  # Saute à l’adresse mémoire spécifiée si le flag Z de l'alu = 0
        if self.alu.flags["Z"] == 0:
            addr = args[0]
            self.reg["PC"] = addr

    def JN(self, *args):  # Saute à l’adresse mémoire spécifiée si le flag N de l'alu = 1
        if self.alu.flags["N"] == 1:
            addr = args[0]
            self.reg["PC"] = addr

    def JNN(self, *args):  # Saute à l’adresse mémoire spécifiée si le flag N de l'alu = 0
        if self.alu.flags["N"] == 0:
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
