from game.character import Barbarian 
from game.character import Priest
from game.character import Wizard

from game.item import Weapon
from game.item import Shield
from game.item import Armor
from game.item import Potion

HEAL_POTION = ("Potion de soins", 10, "Hmm, c'est du sang de demon")
def _with_potions(character, count=4):
    for _ in range(count):
        character.equip(Potion(*HEAL_POTION))
    return character

def make_barbarian(name: str):
    hero = Barbarian(name)
    hero.equip(Weapon("Used axe", 4, "Already used"))
    hero.equip(Shield("Wood shield", 2, "The least you can get"))
    hero.equip(Armor("Leather", 2, 0, "Keep good agility"))
    return _with_potions(hero)

def make_wizard(name: str):
    hero = Wizard(name)
    hero.equip(Weapon("Ash stick", 4, "Good polish", two_handed=True))
    hero.equip(Armor("Leather", 2, 0, "Keep good agility"))
    return _with_potions(hero)

def make_priest(name: str):
    hero = Priest(name)
    hero.equip(Weapon("Small sword", 3, "Blessed a tuesday without ceremony"))
    hero.equip(Shield("Wood shield", 2, "Three pieces of wood with glue"))
    hero.equip(Armor("Leather", 2, 0, "Keep good agility"))
    return _with_potions(hero)

PLAYABLE = [
    ("Barbare", make_barbarian, (198, 84, 58)),
    ("Mage", make_wizard, (82, 118, 196)),
    ("Pretre", make_priest, (96, 154, 108)),
]