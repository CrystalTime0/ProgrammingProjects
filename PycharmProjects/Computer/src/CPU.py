class CPU:
    def __init__(self, ram, alu, reg_nb=8):
        self.alu = alu
        self.ram = ram
        self.reg = [0] * reg_nb
        self.pc = 0x00
        self.running = True
        self.clock = 0

    def step(self):
        instr_size = 1
        self.reg[2] = self.ram.data[self.pc]
        self.reg[1] = self.pc

        if self.reg[2] == 0x00:  # Reset ACC
            self.reg[0] = 0
            instr_size = 1
        elif self.reg[2] == 0x01:  # LOAD [destination][data]
            self.reg[self.ram.data[self.pc + 1]] = self.ram.data[self.pc + 2]
            instr_size = 3
        elif self.reg[2] == 0x02:  # IN Increment +1 [registre]
            self.reg[self.ram.data[self.pc + 1]] = self.alu.add(self.reg[self.ram.data[self.pc + 1]], 0x01)
            instr_size = 2
        elif self.reg[2] == 0x03:  # ADC Addition with Carry [operand]
            self.reg[0] = self.alu.add(self.ram.data[self.pc + 1], self.reg[0])
            instr_size = 2

        elif self.reg[2] == 0xFF:  # HALT
            self.running = False

        self.pc += instr_size
        self.clock += 1
        if self.clock == 100:
            self.running = False
