class ALU:
    def __init__(self):
        self.Z = 0

    def add(self, a, b):
        r = a + b
        self.Z = int(r == 0)
        return r

    def sub(self, a, b):
        r = a - b
        self.Z = int(r == 0)
        return r
