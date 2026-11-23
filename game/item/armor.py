from game.item.abstract import Item

class Armor(Item):
    slot = "body"

    def __init__(self, name, defense_bonus, stamina_bonus=0, description=""):
        super().__init__(name, description)
        self.defense_bonus = defense_bonus
        self.stamina_bonus = stamina_bonus

    def apply_effect(self, target):
        return target.equip(self)

    def summary(self):
        extra = f", +{self.stamina_bonus} stamina" if self.stamina_bonus else ""
        return f"{self.name} (-{self.defense_bonus} damages taken {extra})"