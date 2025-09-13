class ALU:
    def __init__(self):
        self.flags = {"Z": 0, "N": 0, "C": 0}  # Z pour = 0 | N pour négatif | C pour dépassement des 8bit

    # --- Arithmétique ---
    def ADD(self, a, b):  # Additionner
        r = a + b
        self._update_flags(r)
        return r

    def SUB(self, a, b):  # Soustraire
        r = a - b
        self._update_flags(r)
        return r

    def INC(self, a):  # Incrémenter
        r = a + 1
        self._update_flags(r)
        return r

    def DEC(self, a):  # Décrémenter
        r = a - 1
        self._update_flags(r)
        return r

    # --- Logique ---
    def AND(self, a, b):
        r = a & b
        self._update_flags(r)
        return r

    def OR(self, a, b):
        r = a | b
        self._update_flags(r)
        return r

    def XOR(self, a, b):  # Seulement 1 des 2
        r = a ^ b
        self._update_flags(r)
        return r

    def NOT(self, a):
        r = ~a
        self._update_flags(r)
        return r

    # --- Comparaison ---
    def CMP(self, a, b):  # Se servir des flags pour avoir le résultat
        r = a - b
        self._update_flags(r)
        self.flags["C"] = int(a < b)  # Pour savoir si on a dépasser les 8bit ex: -5 = 251

    # --- Méthode interne pour mettre à jour les flags ---
    def _update_flags(self, result):
        self.flags["Z"] = int(result == 0)
        self.flags["N"] = int(result < 0)
