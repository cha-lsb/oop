"""The screens that make up a run: exploring, fighting, losing.

Internal engine code. Note what is *not* here: no combat formula, no
initiative order, no loot table. All of that lives in `game/combat.py` and
reaches this file as the `rules` object handed to `ExploreState`. That is what
lets `oop.cli` play exactly the same fight without importing pygame.
"""

import pygame

from oop.engine import input as keys
from oop.engine import renderer
from oop.engine.constants import (ACCENT, DEBUG_TEXT, DIM_TEXT, ENEMY_COLOR, TITLE,
                                  FONT_SIZE_SMALL, LINE_HEIGHT, TEXT_COLOR)

ACTIONS = ["Attaquer", "Se défendre", "Boire une potion", "Capacité spéciale"]


class GameState:
    """One screen. The loop drives whichever of these is current."""

    def __init__(self, game):
        """Remember the running game.

        Args:
            game (Game): the running game.
        """
        self.game = game

    def handle_event(self, event):
        """React to one pygame event. Screens override this."""

    def update(self):
        """Advance anything time-based. Most screens need nothing."""

    def draw(self, surface):
        """Draw the screen. Screens override this."""


class ExploreState(GameState):
    """Walking the map, until a tile turns out to be occupied."""

    def __init__(self, game, player, level, rules):
        """Drop a hero onto a map.

        Args:
            game (Game): the running game.
            player (Character): the hero.
            level (GameMap): the map being walked.
            rules (module): `oop.game.combat` — the rules of a round.
        """
        super().__init__(game)
        self.player = player
        self.level = level
        self.rules = rules
        self.message = "Explorez. I pour l'inventaire, Échap pour quitter."
        if player.position == (0, 0):
            player.position = level.start

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.game.quit()
            return
        if event.key == pygame.K_i:
            # Imported here, not at the top of the file: `screens` imports
            # GameState from this module, so a module-level import would be a
            # cycle. Do not "fix" this.
            from oop.engine.screens import InventoryState
            self.game.change_state(InventoryState(self.game, self.player, self))
            return

        step = keys.direction(event)
        if step is None:
            return
        column, row = self.player.position
        target = (column + step[0], row + step[1])
        if not self.level.can_walk(target):
            self.message = "Un mur."
            return
        self.player.position = target
        self.message = "Vous avancez."
        self._check_encounter(target)

    def _check_encounter(self, position):
        """Start a fight if the tile the hero just entered holds a creature."""
        tile = self.level.tile_at(position)
        creature = tile.take_encounter() if tile else None
        if creature is not None:
            self.game.change_state(
                CombatState(self.game, self.player, creature(), self, self.rules))

    def draw(self, surface):
        renderer.title(surface, TITLE, 40)
        self.level.draw(surface)
        renderer.draw_actor(surface, self.player,
                            self.level.screen_position(self.player.position),
                            radius=21)
        renderer.panel(surface, (656, 96, 272, 200), "HÉROS")
        y = 130
        for label, value in (("PV", f"{self.player.hp} / {self.player.max_hp}"),
                             ("Force", self.player.damage_output()),
                             ("Endurance", self.player.stamina_value()),
                             ("Initiative", self.player.initiative)):
            renderer.text(surface, label, (672, y), DIM_TEXT, FONT_SIZE_SMALL)
            renderer.text(surface, value, (836, y), TEXT_COLOR, FONT_SIZE_SMALL)
            y += LINE_HEIGHT
        renderer.health_bar(surface, (672, y + 8, 240, 8),
                            self.player.hp, self.player.max_hp)
        renderer.text(surface, self.message, (32, 560), DIM_TEXT)
        renderer.text(surface, "flèches se déplacer   I inventaire   Échap quitter",
                      (32, 590), DIM_TEXT, FONT_SIZE_SMALL)


class CombatState(GameState):
    """A fight: a menu, a log, and the rules module doing the arithmetic."""

    def __init__(self, game, player, enemy, explore, rules):
        """Open a fight.

        Args:
            game (Game): the running game.
            player (Character): the hero.
            enemy (Character): the creature standing on the tile.
            explore (ExploreState): the map to return to on victory.
            rules (module): `oop.game.combat`.
        """
        super().__init__(game)
        self.player = player
        self.enemy = enemy
        self.explore = explore
        self.rules = rules
        self.phase = "player"
        self.debug = False
        self.log = [f"{enemy.display_name} barre le passage !"]

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in keys.DEBUG:
            self.debug = not self.debug
            self.log.append("Détail des calculs : "
                            + ("activé" if self.debug else "coupé"))
            return
        if self.phase != "player":
            if event.key in (pygame.K_SPACE,) + keys.CONFIRM:
                self._leave()
            return

        choice = keys.menu_choice(event)
        if choice is None:
            return
        if not self.rules.is_available(self.player, choice):
            self.log.append("Impossible : rien à la ceinture.")
            return
        self._play(choice)

    def _play(self, choice):
        """Resolve one round and work out whether the fight is over."""
        self.log.extend(self.rules.play_round(self.player, choice, self.enemy,
                                              verbose=self.debug))
        if not self.enemy.is_alive():
            self.phase = "victory"
            self.log.append(f"{self.enemy.display_name} s'effondre.")
            self.log.extend(self.rules.collect_spoils(self.player, self.enemy))
            self.log.append("Espace pour reprendre la route.")
        elif not self.player.is_alive():
            self.phase = "defeat"
            self.log.append("Vous tombez.")
            self.log.append("Espace pour continuer.")

    def _leave(self):
        """Go back to the map, or to the game-over screen."""
        if self.phase == "victory":
            self.game.change_state(self.explore)
        else:
            self.game.change_state(GameOverState(self.game, self.player))

    def draw(self, surface):
        renderer.title(surface, "COMBAT", 40)
        renderer.draw_actor(surface, self.player, (240, 160), radius=72,
                            with_hp=True)
        renderer.draw_actor(surface, self.enemy, (720, 160), radius=72,
                            color=getattr(self.enemy, "color", ENEMY_COLOR),
                            with_hp=True)
        renderer.text(surface, "contre", (480, 160), DIM_TEXT, center=True)

        renderer.panel(surface, (32, 300, 380, 200), "ACTIONS")
        for index, label in enumerate(ACTIONS):
            available = self.rules.is_available(self.player, index + 1)
            color = TEXT_COLOR if available and self.phase == "player" else DIM_TEXT
            renderer.text(surface, f"{index + 1}. {label}", (52, 338 + index * 30),
                          color)
        renderer.text(surface, "F1 détail des calculs", (52, 466), DIM_TEXT,
                      FONT_SIZE_SMALL)

        renderer.panel(surface, (432, 300, 496, 300), "JOURNAL")
        for offset, line in enumerate(self.log[-11:]):
            color = DEBUG_TEXT if line.startswith("   ") else TEXT_COLOR
            renderer.text(surface, line, (450, 336 + offset * LINE_HEIGHT),
                          color, FONT_SIZE_SMALL)


class GameOverState(GameState):
    """The end of a run, won or lost."""

    def __init__(self, game, player):
        """Show the outcome.

        Args:
            game (Game): the running game.
            player (Character): the hero, alive or not.
        """
        super().__init__(game)
        self.player = player
        self.won = player.is_alive()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in keys.CONFIRM:
            self.game.new_game()
        elif event.key == pygame.K_ESCAPE:
            self.game.quit()

    def draw(self, surface):
        headline = "Victory!" if self.won else "GAME OVER"
        renderer.title(surface, headline, 240, ACCENT if self.won else ENEMY_COLOR)
        renderer.text(surface, self.player.summary(), (480, 300), TEXT_COLOR,
                      center=True)
        renderer.text(surface, "Entrée recommencer      Échap quitter",
                      (480, 360), DIM_TEXT, center=True)
