from game.item.abstract import Item

class Potion(Item):
    slot = "belt"

    def __init__(self, name, heal_amount, description=""):
        super().__init__(name, description)
        self.heal_amount = heal_amount

    def apply_effect(self, target):
        healed = target.heal(self.heal_amount)
        if healed == 0:
            return f"{target.name} has full HP already. {self.name} wasted"

        return f"{target.name} drinks {self.name} and recover {self.heal_amount} HP"

    def summary(self):
        return f"{self.name} (+{self.heal_amount} HP)"

