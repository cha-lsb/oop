from src.oop.engine.map import GameMap
from src.oop.engine.screens import CharacterCreationState
from src.oop.engine.state import ExploreState
from src.oop.engine.window import Game
from game import combat
from game.encounters import random_encounters
from game.roster import PLAYABLE


def start_adventure(game, hero):
    """Drop a freshly created hero onto the map.

    Args:
        game (Game): the running game.
        hero (Character): the character the player just built.
    """
    level = GameMap(encounters=random_encounters())
    game.change_state(ExploreState(game, hero, level, combat))


def creation_screen(game):
    """Build the character-creation screen for a new run.

    Args:
        game (Game): the running game.

    Returns:
        CharacterCreationState: the first screen of a run.
    """
    return CharacterCreationState(
        game, PLAYABLE, on_done=lambda hero: start_adventure(game, hero))


def main():
    game = Game()
    game.new_game = lambda: game.change_state(creation_screen(game))
    game.new_game()
    game.run()


if __name__ == "__main__":
    main()