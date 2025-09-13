from RAM import RAM
from CPU import CPU
from ALU import ALU

alu = ALU()
ram = RAM()
cpu = CPU(ram, alu)

with open("code.txt", "r") as code:
    lines = code.readline()
lines = [int(op, 16) for op in lines.split()]

for address, value in enumerate(lines):
    ram.write(address, value)

while cpu.running:
    cpu.step()
print(vars(cpu))
print(vars(vars(cpu)["ram"]))
