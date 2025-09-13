from typing import *


class CPU:
    def __init__(self, ram, alu):
        self.alu = alu
        self.ram = ram
        self.reg = dict.fromkeys(["PC", "IR", "ACC", "MAR", "MDR", "FLAGS"], 0x00)
        self.running = True
        self.clock = 0

        self.INSTRUCTIONS: Dict[int, Callable[..., Any]] = {  # Rajouter AND, OR, XOR, NOT, INC, DEC (SHL et SHR)
            0x00: self.LDA,
            0x01: self.STA,
            0x02: self.ADD,
            0x03: self.SUB,
            0x04: self.CMP,
            0x05: self.JMP,
            0x06: self.JZ,
            0x07: self.JNZ,
            0xFF: self.HLT
        }
        self.INSTRUCTIONS_SIZE = {
            0x00: 2,
            0x01: 2,
            0x02: 2,
            0x03: 2,
            0x04: 2,
            0x05: 2,
            0x06: 2,
            0x07: 2,
            0xFF: 1
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

    # --- Comparaison ---
    def CMP(self, *args):
        value = args[0]
        self.alu.CMP(self.reg["ACC"], value)  # Comparer l'opérande et l'accumulateur

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
