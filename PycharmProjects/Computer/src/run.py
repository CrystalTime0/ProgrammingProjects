from RAM import RAM
from CPU import CPU
from ALU import ALU

# --- SETUP ---
prgm_filepath = "prgm/even_or_not.txt"
log = False

alu = ALU()
ram = RAM()
cpu = CPU(ram, alu)

def log_print():
    print(vars(cpu))
    print(vars(vars(cpu)["ram"]))
    print(alu.flags)

with open(prgm_filepath, "r") as code:
    lines = code.readline()
lines = [int(op, 16) for op in lines.split()]

for address, value in enumerate(lines):
    ram.write(address, value)

# --- EXECUTION ---
while cpu.running:
    cpu.step()

    if log:
        log_print()