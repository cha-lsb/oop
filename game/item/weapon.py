from game.item.abstract import Item

class Weapon(Item):
    slot = "hand"
    def __init__(self, name, damage_bonus, description: str="", two_handed: bool=False):
        super().__init__(name, description)
        self.damage_bonus = damage_bonus
        if two_handed:
            self.slot = "two_hands"

    def apply_effect(self, target):
        return target.equip(self)

    def summary(self):
        hands = "two-hands weapon" if self.slot == "two-hands" else ""
        return f"{self.name}{hands} (+{self.damage_bonus} damages)"