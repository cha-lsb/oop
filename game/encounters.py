import random

from game.monsters import GiantRat, Goblin, Orc, Skeleton, SkeletonWizard, Troll

# The floor tiles where a monster waits, as (column, row).
ENCOUNTER_TILES = [(5, 3), (5, 5), (10, 6)]

# Every monster that can show up on one of those tiles.
MONSTERS = [Goblin, Orc, Skeleton, GiantRat, Troll, SkeletonWizard]


def random_encounters():
    """Pick a random monster for each encounter tile.

    Called once per run, so every new game gets a different line-up.

    Returns:
        dict: {(column, row): monster class}.
    """
    return {tile: random.choice(MONSTERS) for tile in ENCOUNTER_TILES}
