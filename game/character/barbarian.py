from game.character.abstract import Character
from game.constants import AVATAR_DIR
from game.dice import Dice

class Barbarian(Character):
    avatar = AVATAR_DIR / "barbarian.png"

    def __init__(self, name: str):
        super().__init__(
            name=name, 
            hp=42, 
            strength=9,
            combat_skill=55,
            description="Une hache, une mauvaise humeur, aucun plan"
        )
        self.rage = 3

    def use_special(self, target) -> str:
        if self.rage <= 0:
            return f"{self.name} has no more rage - regular attack instead"

        self.rage -= 1
        raw_damages = 2 * self.damage_output() + Dice.d6() + 6
        dealt = target.take_damage(raw_damages)
        return f"{self.name} is berserk. {dealt} damages (remaining rage: {self.rage})"
