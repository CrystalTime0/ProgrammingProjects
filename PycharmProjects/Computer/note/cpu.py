# Mini processeur von Neumann très simple

# mémoire : instructions + données dans la même RAM
RAM = [0]*256   # 256 cases mémoire
PC = 0          # compteur ordinal
IR = 0          # instruction courante
ACC = 0         # accumulateur

# Programme : somme de 5 + 7 puis stockage à l'adresse 20
# Code machine (opcode, operand) :
# LDA 10 / ADD 11 / STA 20 / HLT
program = [
    1, 10,  # LDA 10
    2, 11,  # ADD 11
    3, 20,  # STA 20
    255     # HLT
]
# Données
RAM[10] = 5
RAM[11] = 7

# Charger le programme dans la RAM à partir de 0
for i, byte in enumerate(program):
    RAM[i] = byte

# Dictionnaire des instructions
def LDA(addr):
    global ACC
    ACC = RAM[addr]

def ADD(addr):
    global ACC
    ACC += RAM[addr]

def STA(addr):
    RAM[addr] = ACC

def HLT():
    global running
    running = False

# Table des opcodes
INSTRUCTIONS = {
    1: LDA,
    2: ADD,
    3: STA,
    255: HLT
}

# Cycle fetch-decode-execute
running = True
while running:
    IR = RAM[PC]           # fetch
    PC += 1
    if IR == 255:           # HLT n'a pas d'opérande
        INSTRUCTIONS[IR]()
        break
    operand = RAM[PC]       # fetch opérande
    PC += 1
    INSTRUCTIONS[IR](operand)  # execute

print("Programme terminé")
print("ACC =", ACC)
print("RAM[20] =", RAM[20])
