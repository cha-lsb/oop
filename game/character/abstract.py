from __future__ import annotations
from game.dice import Dice
from game.constants import BELT_SLOTS, BACKPACK_SLOTS, MIN_DAMAGES, DEFEND_BONUS, POWER_ATTACK_PENALTY
from game.entity import Entity


class Character(Entity):
    belt_slots = BELT_SLOTS
    backpack_slots = BACKPACK_SLOTS

    def __init__(
        self,
        name: str, 
        hp: int,
        strength: int,
        combat_skill: int,
        stamina: int = 0,
        mana: int = 0,
        attacks_per_round: int=1,
        initiative: int = 30,
        description: str="",
    ):
        super().__init__(name, description) 
        self.max_hp = hp
        self.hp = hp
        self.strength = strength
        self.combat_skill = combat_skill
        self.stamina = stamina
        self.max_mana = mana
        self.mana = mana
        self.initiative = initiative
        self.attacks_per_round = attacks_per_round

        self.position = (0, 0)

        self.right_hand = None
        self.left_hand = None
        self.body = None
        self.belt = []
        self.backpack = []

        self.defending = False
        self.last_roll = {}
        self.last_damage = None

    def summary(self) -> str:
        return F"{self.name} - {self.hp}/{self.max_hp} PV"

    @property
    def display_name(self) -> str:
        return self.name

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int):
        previous = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - previous

    def take_damage(self, amount: int, pierce_armor: bool=False):
        reduction = self.stamina_value()
        if not pierce_armor:
            reduction += self.defense_value()

        dealt = max(MIN_DAMAGES, amount - reduction)
        self.hp = max(0, self.hp - dealt)
        self.last_damage = {"raw": amount, "reduction": reduction,
                            "pierced": pierce_armor, "dealt": dealt}
        return dealt

    def roll_to_hit(self, modifier: int=0) -> bool:
        roll = Dice.d100()
        target_number = self.combat_skill + modifier
        self.last_roll = {"roll": roll, "target": target_number,
                          "hit": roll <= target_number}
        return roll <= target_number

    def attack(self, target: Character) -> str:
        if not self.roll_to_hit():
            return (f"{self.name} attack {target.name}: "
                    f"{self.last_roll['roll']} against {self.last_roll['target']}, missed!")

        raw_damages = self.damage_output() + Dice.d6()
        dealt = target.take_damage(raw_damages)
        return f"{self.name} hits {target.name}: {dealt} taken"

    def defend(self):
        """Raise the guard once per round"""
        self.defending = True
        return f"{self.name} is on their guards: +{DEFEND_BONUS}"

    def equip(self, item):
        if item in self.backpack:
            self.backpack.remove(item)

        if item.slot == "belt":
            if len(self.belt) >= BELT_SLOTS:
                self.store(item)
                return f"{self.name}'s belt is already full"
            self.belt.append(item)
            return f"{item.name} placed in {self.name}'s belt"

        if item.slot == "body":
            self._displace(self.body)
            self.body = item
            return F"{self.name} wears: {item.name}"

        if item.slot == "two_hands":
            self._displace(self.right_hand)
            self._displace(self.left_hand)
            self.left_hand = None
            self.right_hand = item
            return f"{self.name} takes {item.name} with both hands"

        if self.right_hand is not None and self.right_hand.slot == "two_hands":
            self._displace(self.right_hand)
            self.right_hand = None
        if self.right_hand is None:
            self.right_hand = item
        elif self.left_hand is None:
            self.left_hand = item
        else:
            self._displace(self.right_hand)
            self.right_hand = item
        return F"{self.name} equips {item.name}"

    def swap_hands(self) -> str:
        """Swap what the right and left hands are holding"""
        if self.right_hand is not None and self.right_hand.slot == "two_hands":
            return f"{self.right_hand.name} needs both hands"
        if self.right_hand is None and self.left_hand is None:
            return f"{self.name} has nothing in hand"
        self.right_hand, self.left_hand = self.left_hand, self.right_hand
        return f"{self.name} swaps hands"

    def equipped(self):
        """Returns what's currently equiped"""
        return [item for item in (self.right_hand, self.left_hand, self.body) if item is not None]

    def unequip(self, slot_name: str) -> str:
        item = getattr(self, slot_name, None)
        if item is None:
            return ""
        setattr(self, slot_name, None)
        if not self.store(item):
            setattr(self, slot_name, item)
            return "Backpack is full"
        return f"{self.name} put {item.name} in the bag"

    def rest(self):
        self.mana = self.max_mana
        while len(self.belt) < BELT_SLOTS:
            potion = next((i for i in self.backpack if i.slot == "belt"), None)
            if potion is None:
                break  
            self.backpack.remove(potion)
            self.belt.append(potion)

    def damage_output(self):
        return self.strength + sum(item.damage_bonus for item in self.equipped())

    def defense_value(self):
        return sum(item.defense_bonus for item in self.equipped())

    def stamina_value(self):
        value = self.stamina + sum(item.stamina_bonus for item in self.equipped())
        if self.defending:
            value += DEFEND_BONUS
        return value

    def _displace(self, item):
        """Send a slot's previous item back into the backpack"""
        if item is not None:
            self.store(item)

    def store(self, item):
        if len(self.backpack) >= BACKPACK_SLOTS:
            return False
        self.backpack.append(item)
        return True

    def use_potion(self):
        if not self.belt:
            return f"{self.name} looks for a potion on his belt: nothing"
        potion = self.belt.pop(0)
        return potion.apply_effect(self)

    def use_special(self, target):
        if not self.roll_to_hit(-POWER_ATTACK_PENALTY):
            return (f"{self.name} tries a power punch:"
                    f"{self.last_roll['roll']} against {self.last_roll['target']}, missed!")
        raw_damages = 2 * self.damage_output() + Dice.d6()
        dealt = target.take_damage(raw_damages)
        return f"{self.name} hits with a power punch. {dealt} damages"