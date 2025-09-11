RAM_SIZE = 64
ram = [0x00] * RAM_SIZE

running = True
opcode = 0
operand = 0
ACC = 0

with open("code.txt", "r") as code:
    lines = code.readline()
lines = [int(op, 16) for op in lines.split()]

for address, op in enumerate(lines):
    ram[address] = op

print(ram)
print([hex(x) for x in ram])

while running:

    # ADD opcode selector
    # ADD opcode jump with nb operand
    if opcode == 0x00:
        ACC = 0
    elif opcode == 0x01:
        pass
