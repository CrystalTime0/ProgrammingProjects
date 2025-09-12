class RAM:
    def __init__(self, size=192):  # 128 instr et 64 data
        self.data = [0x00] * size

    def read(self, addr):
        return self.data[addr]

    def write(self, addr, value):
        self.data[addr] = value
