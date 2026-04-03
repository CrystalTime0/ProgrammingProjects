class Vehicule:
    def __init__(self, color, brand, nb_wheels, length):
        self.color = color
        self.brand = brand
        self.nb_wheels = nb_wheels
        self.length = length
        self.position = 0
        self.avancer()

    def avancer(self):
        self.position += self.calculate_speed()
        return self.position

    def calculate_speed(self):
        return self.length // self.nb_wheels

class CamionCiterne(Vehicule):
    def __init__(self, color, brand, nb_wheels, length, volume):
        Vehicule.__init__(self, color, brand, nb_wheels, length)
        self.volume = volume

    def printstzstz(self):
        print(self.brand)
        self.avancer()