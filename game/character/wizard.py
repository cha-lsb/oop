from game.character.abstract import Character
from game.dice import Dice

class Wizard(Character):
    def __init__(self, name: str):
        super().__init__(
            name=name, 
            hp=40, 
            strength=4, 
            combat_skill=70,
            stamina = 2,
            initiative = 35, 
            mana=20,
            description="frele, sur de lui, difficile a esquiver"
        )

    def attack(self, target: Character):
        roll = Dice.d100()
        if roll > self.combat_skill:
            return(
                f"{self.name} attacked {target.name}:"
                f"{roll} against {self.combat_skill}, misses"
            )

        dealt = target.take_damage(self.damage_output() + Dice.d6(), pierce_armor=True)
        return f"{self.name} sent a fireball to {target.name}: {dealt} taken"

    def use_special(self, target) -> str:
        cost = 4
        if self.mana < cost:
            return f"{self.name} doesn't have enough mana ({self.mana} / cost)"

        self.mana -= cost
        if not self.roll_to_hit():
            return (f"{self.name} misses his lighting attack: "
                    f"{self.last_roll['roll']} against {self.last_roll['target']}")
        raw_damages = Dice.d6() + 12
        dealt = target.take_damage(raw_damages, pierce_armor=True)
        return (f"{self.name} casts a strong spell : {delt} damages!"
                f"({self.mana})")
