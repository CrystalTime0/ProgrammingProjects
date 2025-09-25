from RAM import RAM
from CPU import CPU
from ALU import ALU
from ASSEMBLEUR import ASSEMBLEUR

# --- SETUP ---
prgm_filepath = "prgm/ass/even_or_odd.txt"
mode = "asm"
log = True

alu = ALU()
ram = RAM()
cpu = CPU(ram, alu)
assembleur = ASSEMBLEUR(prgm_filepath, mode)


def log_print():
    print(vars(cpu))
    print(vars(vars(cpu)["ram"]))
    print(alu.flags)


for address, value in enumerate(assembleur.assemble()):
    ram.write(address, value)

# --- EXECUTION ---
while cpu.running:
    cpu.step()

    if log:
        log_print()
