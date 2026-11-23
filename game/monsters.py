from game.character import Character, Wizard
from game.item import Weapon, Armor, Potion

class Goblin(Character):
	def __init__(self):
		super().__init__("Goblin", hp=20, strength=7, combat_skill=40, stamina=1)
		self.store(Weapon("Dague", 2, "In a poor shape but quick"))

class Orc(Character):
	def __init__(self):
		super().__init__("Orc", hp=28, strength=10, combat_skill=45, stamina=2)
		self.equip(Armor("Rust plates", 2, 1, "Somehow holds together"))

class Skeleton(Character):
	def __init__(self):
		super().__init__("Skeleton", hp=18, strength=6, combat_skill=45, stamina=0)
		self.equip(Armor("Thick leather", 3, description="good, not great"))

class GiantRat(Character):
	def __init__(self):
		super().__init__(
			"Rat geant",
			hp=12,
			strength=4,
			combat_skill=40,
			stamina=0,
			initiative=45,
			attacks_per_round=2,
			description="Bites twice"
		)

class Troll(Character):
	REGEN = 4
	def __init__(self):
		super().__init__(
			"Troll",
			hp=40,
			strength=12,
			combat_skill=35,
			stamina=3,
			initiative=20,
			description="slow but strong"
		)

	def defend(self) -> str:
		healed = self.heal(self.REGEN)
		return f"{super().defend()}. Feels better (+{healed} HP)"

class SkeletonWizard(Wizard):
	def __init__(self):
		super().__init__("Sorcier Squelette")
		self.max_hp = self.hp = 26
		self.strength = 5 
		self.combat_skill = 50
		self.stamina = 1
		self.initiative = 32
		self.max_mana = self.mana = 8
		self.description = "Roi liche, pas content"
		self.equip(Weapon(
			name="Baton d'os", damage_bonus=3, description="probablement un femur")
		)
		self.store(Potion("Grande potion", 16, "Seulement en cas d'urgence"))