from game.item.abstract import Item

class Shield(Item):
    slot = "hand"
    def __init__(self, name, defense_bonus, description: str=""):
        super().__init__(name, description)
        self.defense_bonus=defense_bonus

    def apply_effect(self, target):
        return target.equip(self)

    def summary(self):
        return f"{self.name} (damages taken reduced by {self.defense_bonus})"