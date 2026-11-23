import random

class Dice: 

    @staticmethod
    def roll(sides, count=1):
        return sum(random.randint(1, sides)for _ in range(count))

    @staticmethod
    def d6(count: int=1):
        return Dice.roll(6, count)

    @staticmethod
    def d100(count: int=1):
        return Dice.roll(100, count)

    @staticmethod
    def chance(percent: int) -> bool:
        return Dice.d100() <= percent
