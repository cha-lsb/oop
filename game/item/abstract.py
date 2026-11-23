from abc import abstractmethod
from game.entity import Entity

class Item(Entity):

    slot = None
    damage_bonus = 0
    defense_bonus = 0
    stamina_bonus = 0

    @abstractmethod
    def apply_effect(self, target):
        """Apply this item to a character and return the line to show"""