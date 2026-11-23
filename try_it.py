import os
import sys

import pygame
from oop.engine.map import GameMap
from oop.engine.state import ExploreState
from oop.engine.window import Game
from game.character.barbarian import Barbarian


hero = Barbarian ("sara")
game = Game()
game.run(ExploreState(game, hero, GameMap(), None))