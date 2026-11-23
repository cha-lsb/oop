"""The tile grid, and how it draws itself.

Internal engine code. The layout is small, fixed and written by hand: no
procedural generation, no scrolling, no save format. Everything the player
walks on fits on one screen.

A tile knows whether it can be walked on and what creature is waiting on it.
The creature is stored as a **class**, not an instance, so each visit builds a
fresh opponent — and an emptied tile simply forgets it.
"""

import pygame

from oop.engine.constants import (ACCENT, FLOOR_COLOR, FLOOR_EDGE, MAP_ORIGIN,
                                  TILE, WALL_COLOR)
from oop.engine import renderer

# The demonstration dungeon. '#' is wall, '.' is floor.
#
# The three encounter tiles of `game/encounters.py` — (5, 3), (5, 5) and
# (10, 6) — sit on this layout, and the hero starts at (1, 1). Changing a
# character here moves a wall; changing `encounters.py` moves a monster. The
# two files stay independent on purpose.
LAYOUT = [
    "############",
    "#....#.....#",
    "#.##.#.###.#",
    "#........#.#",
    "#.#.###.##.#",
    "#..........#",
    "#.####.###.#",
    "#..........#",
    "############",
]

START = (1, 1)


class Tile:
    """One square of the map."""

    def __init__(self, walkable, encounter=None):
        """Build a tile.

        Args:
            walkable (bool): False for a wall.
            encounter (type | None): the creature class waiting here, if any.
        """
        self.walkable = walkable
        self.encounter = encounter

    def take_encounter(self):
        """Hand over the creature class here and clear the tile.

        Returns:
            type | None: the class to instantiate, or None.
        """
        creature, self.encounter = self.encounter, None
        return creature


class GameMap:
    """The grid the hero walks on."""

    def __init__(self, layout=None, encounters=None):
        """Build the map and drop the encounters onto it.

        Args:
            layout (list | None): rows of '#' and '.'; the built-in dungeon
                when omitted.
            encounters (dict | None): {(column, row): creature class}.
        """
        rows = layout or LAYOUT
        self.width = len(rows[0])
        self.height = len(rows)
        self.start = START
        self.tiles = [[Tile(char == ".") for char in row] for row in rows]

        for position, creature in (encounters or {}).items():
            tile = self.tile_at(position)
            if tile is not None and tile.walkable:
                tile.encounter = creature

    def tile_at(self, position):
        """Return the tile at (column, row), or None if off the grid.

        Args:
            position (tuple): (column, row).

        Returns:
            Tile | None: the tile, or None when the position is outside.
        """
        column, row = position
        if 0 <= row < self.height and 0 <= column < self.width:
            return self.tiles[row][column]
        return None

    def can_walk(self, position):
        """Say whether the hero may step onto a position."""
        tile = self.tile_at(position)
        return tile is not None and tile.walkable

    def draw(self, surface):
        """Draw every tile, and mark the ones still holding a creature.

        Args:
            surface (pygame.Surface): where to draw.
        """
        origin_x, origin_y = MAP_ORIGIN
        for row in range(self.height):
            for column in range(self.width):
                tile = self.tiles[row][column]
                rect = pygame.Rect(origin_x + column * TILE,
                                   origin_y + row * TILE, TILE, TILE)
                pygame.draw.rect(surface, FLOOR_COLOR if tile.walkable
                                 else WALL_COLOR, rect)
                pygame.draw.rect(surface, FLOOR_EDGE, rect, width=1)
                if tile.encounter is not None:
                    pygame.draw.circle(surface, ACCENT, rect.center, 5)

    def screen_position(self, position):
        """Return the pixel centre of a tile.

        Args:
            position (tuple): (column, row).

        Returns:
            tuple: (x, y) in pixels.
        """
        column, row = position
        origin_x, origin_y = MAP_ORIGIN
        return (origin_x + column * TILE + TILE // 2,
                origin_y + row * TILE + TILE // 2)
