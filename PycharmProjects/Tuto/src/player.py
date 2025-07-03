
class Player:
    def __init__(self):
        self.health = 20
        self.iventory = []

    def add_item(self, name):
        if name in self.iventory:
            raise ValueError("Item already exists")
        self.iventory.append(name)
        return True

    def change_health(self, new_health: int):
        self.health = new_health