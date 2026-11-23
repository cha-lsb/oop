from game.character.abstract import Character
from game.dice import Dice

class Priest(Character):
    def __init__(self, name: str):
        super().__init__(
            name=name, 
            hp=38, 
            strength=8, 
            combat_skill=55,
            stamina=2,
            initiative=38, 
            mana=15,
            description="Une masse dans une main, sa foi dans l'autre. Do you think I'm spooky?"
        )

    def use_special(self, target: Character) -> str:
        cost = 3
        if self.mana < cost:
            return f"{self.name} doesn't have enough mana ({self.mana} / cost)"
        healed = self.heal(12)
        if healed == 0:
            return F"{self.name} wasted his turn, he's already full life"

        self.mana -= cost
        return (f"{self.name} summons god to heal them: +{healed} HP"
                f"(mana: {self.mana})")