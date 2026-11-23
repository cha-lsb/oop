"""Character creation, and the character sheet / inventory screen.

Internal engine code.

The inventory uses a single cursor that travels over every cell — equipment
slots, belt, backpack — and never "picks an item up". `Entrée` reads where the
cursor is and acts: an item in the bag gets equipped into whatever its own
`slot` says, an occupied slot gets emptied into the bag. There is no carry
mode, so there is nothing to cancel and no illegal placement to refuse.
"""

import pygame

from oop.engine import input as keys
from oop.engine import renderer
from oop.engine.constants import (ACCENT, CURSOR_COLOR, DIM_TEXT,
                                  FONT_SIZE_SMALL, LINE_HEIGHT, TEXT_COLOR)
from oop.engine.state import GameState

EQUIPMENT_SLOTS = (("right_hand", "Main droite"),
                   ("left_hand", "Main gauche"),
                   ("body", "Corps"))

BAG_COLUMNS = 4


class CharacterCreationState(GameState):
    """Pick a class, type a name, start the run."""

    def __init__(self, game, choices, on_done):
        """Build the first screen of a run.

        Args:
            game (Game): the running game.
            choices (list): `roster.PLAYABLE` — (label, factory, colour)
                tuples. Bare tuples, so that `game/` never has to import an
                engine type.
            on_done (callable): called with the finished character.
        """
        super().__init__(game)
        self.choices = list(choices)
        self.on_done = on_done
        self.selected = 0
        self.name = ""
        # One sample per class, built once, so the cards can show real stats
        # instead of a table duplicated here.
        self.samples = [factory("") for _, factory, _ in self.choices]

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.game.quit()
            return
        if event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
            return
        if event.key in keys.CONFIRM:
            self._start()
            return

        choice = keys.menu_choice(event)
        if choice is not None and choice <= len(self.choices):
            self.selected = choice - 1
            return
        if keys.is_text(event) and len(self.name) < 20:
            self.name += event.unicode

    def _start(self):
        """Build the chosen character and hand it to the seam."""
        label, factory, color = self.choices[self.selected]
        hero = factory(self.name.strip() or label)
        hero.color = color
        self.on_done(hero)

    def draw(self, surface):
        width = surface.get_width()
        middle = width // 2
        renderer.title(surface, "CRÉATION DU PERSONNAGE", 50)
        renderer.text(surface, f"Nom :  {self.name or '…'}_", (middle, 100),
                      TEXT_COLOR, center=True)

        # The cards share the window's width and stay centred, however many
        # classes the roster offers.
        count = len(self.choices)
        gap = 30
        card_width = min(260, (width - 2 * 40 - (count - 1) * gap) // count)
        left = (width - count * card_width - (count - 1) * gap) // 2

        for index, (label, _, color) in enumerate(self.choices):
            sample = self.samples[index]
            chosen = index == self.selected
            rect = pygame.Rect(left + index * (card_width + gap), 135,
                               card_width, 380)
            renderer.panel(surface, rect)
            if chosen:
                pygame.draw.rect(surface, CURSOR_COLOR, rect, width=2,
                                 border_radius=6)
            renderer.text(surface, str(index + 1), (rect.x + 12, rect.y + 10),
                          DIM_TEXT, FONT_SIZE_SMALL)
            renderer.text(surface, label.upper(), (rect.centerx, rect.y + 32),
                          ACCENT if chosen else TEXT_COLOR, center=True, bold=True)
            renderer.draw_token(surface, sample, (rect.centerx, rect.y + 115),
                                60, color)
            rows = (("PV", sample.max_hp), ("Force", sample.strength),
                    ("CC", sample.combat_skill), ("End.", sample.stamina),
                    ("Init.", sample.initiative),
                    ("Att.", sample.attacks_per_round))
            for row, (key, value) in enumerate(rows):
                y = rect.y + 200 + row * LINE_HEIGHT
                renderer.text(surface, key, (rect.x + 36, y), DIM_TEXT,
                              FONT_SIZE_SMALL)
                renderer.text(surface, value, (rect.right - 52, y), TEXT_COLOR,
                              FONT_SIZE_SMALL)

        renderer.text(surface, self.samples[self.selected].description,
                      (middle, 550), ACCENT, center=True)
        renderer.text(surface, f"1-{count} choisir      Entrée valider",
                      (middle, 595), DIM_TEXT, center=True)


class InventoryState(GameState):
    """The character sheet and the bag, on one screen, with one cursor."""

    def __init__(self, game, player, parent):
        """Open the sheet over the map.

        Args:
            game (Game): the running game.
            player (Character): the hero.
            parent (ExploreState): the screen to go back to.
        """
        super().__init__(game)
        self.player = player
        self.parent = parent
        self.cursor = 0
        self.message = ""
        self.cells = []
        self._rebuild_cells()

    def _rebuild_cells(self):
        """Lay the cursor's world out as one flat list of cells.

        Equipment slots first, then the belt, then the backpack grid. Keeping
        it flat is what makes the single-cursor model simple: moving is an
        index, and `Entrée` only has to read `kind`.
        """
        cells = [{"kind": name, "index": 0, "label": label}
                 for name, label in EQUIPMENT_SLOTS]
        for index in range(self.player.belt_slots):
            cells.append({"kind": "belt", "index": index, "label": "Ceinture"})
        for index in range(self.player.backpack_slots):
            cells.append({"kind": "bag", "index": index, "label": "Sac"})
        self.cells = cells
        self.cursor = max(0, min(self.cursor, len(cells) - 1))

    def _item_at(self, cell):
        """Return the item sitting in a cell, or None."""
        if cell["kind"] == "belt":
            belt = self.player.belt
            return belt[cell["index"]] if cell["index"] < len(belt) else None
        if cell["kind"] == "bag":
            bag = self.player.backpack
            return bag[cell["index"]] if cell["index"] < len(bag) else None
        return getattr(self.player, cell["kind"])

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in keys.CLOSE:
            self.game.change_state(self.parent)
            return
        if event.key == pygame.K_s:
            self.message = self.player.swap_hands()
            return
        if event.key in keys.CONFIRM:
            self._activate()
            return

        step = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1,
                pygame.K_UP: -BAG_COLUMNS, pygame.K_DOWN: BAG_COLUMNS}.get(event.key)
        if step is not None:
            self.cursor = max(0, min(self.cursor + step, len(self.cells) - 1))

    def _activate(self):
        """Equip what the cursor points at, or put it away."""
        cell = self.cells[self.cursor]
        item = self._item_at(cell)
        if item is None:
            return
        if cell["kind"] in ("bag", "belt"):
            self.message = self.player.equip(item)
        else:
            self.message = self.player.unequip(cell["kind"])
        self._rebuild_cells()

    def _preview(self):
        """Return the (label, now, later) rows for the live preview.

        Only meaningful when the cursor rests on something in the bag: it
        answers "what would this change", which is the module 4 argument made
        visible.
        """
        item = self._item_at(self.cells[self.cursor])
        rows = [("PV", f"{self.player.hp} / {self.player.max_hp}", None),
                ("Force", self.player.damage_output(), None),
                ("Cap. combat", f"{self.player.combat_skill} %", None),
                ("Endurance", self.player.stamina_value(), None),
                ("Défense", self.player.defense_value(), None),
                ("Initiative", self.player.initiative, None),
                ("Attaques", self.player.attacks_per_round, None),
                ("Mana", f"{self.player.mana} / {self.player.max_mana}", None)]
        if item is None or self.cells[self.cursor]["kind"] != "bag":
            return rows, None

        rows[1] = ("Force", self.player.damage_output(),
                   self.player.damage_output() + getattr(item, "damage_bonus", 0))
        rows[3] = ("Endurance", self.player.stamina_value(),
                   self.player.stamina_value() + getattr(item, "stamina_bonus", 0))
        rows[4] = ("Défense", self.player.defense_value(),
                   self.player.defense_value() + getattr(item, "defense_bonus", 0))
        return rows, item

    def draw(self, surface):
        renderer.title(surface, "FICHE & INVENTAIRE", 40)
        rows, previewed = self._preview()

        renderer.panel(surface, (32, 88, 260, 330), "FICHE")
        renderer.text(surface, self.player.display_name, (52, 118), TEXT_COLOR,
                      bold=True)
        renderer.text(surface, type(self.player).__name__, (52, 142), DIM_TEXT,
                      FONT_SIZE_SMALL)
        for index, (label, now, later) in enumerate(rows):
            y = 180 + index * LINE_HEIGHT
            renderer.text(surface, label, (52, y), DIM_TEXT, FONT_SIZE_SMALL)
            shown = f"{now} → {later}" if later is not None and later != now else now
            renderer.text(surface, shown, (200, y),
                          ACCENT if later is not None and later != now else TEXT_COLOR,
                          FONT_SIZE_SMALL)

        renderer.panel(surface, (312, 88, 260, 330), "ÉQUIPEMENT")
        for index, (name, label) in enumerate(EQUIPMENT_SLOTS):
            item = getattr(self.player, name)
            rect = pygame.Rect(332, 140 + index * 72, 220, 34)
            renderer.slot(surface, rect, label, item,
                          selected=self.cursor == index)
        renderer.text(surface, "Ceinture", (332, 360), DIM_TEXT, FONT_SIZE_SMALL)
        for index in range(self.player.belt_slots):
            cell_index = len(EQUIPMENT_SLOTS) + index
            rect = pygame.Rect(332 + index * 40, 380, 32, 32)
            renderer.slot(surface, rect, None, None,
                          selected=self.cursor == cell_index)
            if index < len(self.player.belt):
                pygame.draw.circle(surface, ACCENT, rect.center, 7)

        bag = self.player.backpack
        renderer.panel(surface, (592, 88, 336, 330),
                       f"SAC ({len(bag)}/{self.player.backpack_slots})")
        first_bag = len(EQUIPMENT_SLOTS) + self.player.belt_slots
        for index in range(self.player.backpack_slots):
            column, row = index % BAG_COLUMNS, index // BAG_COLUMNS
            rect = pygame.Rect(612 + column * 78, 130 + row * 46, 70, 38)
            item = bag[index] if index < len(bag) else None
            renderer.slot(surface, rect, None, None,
                          selected=self.cursor == first_bag + index)
            if item is not None:
                renderer.text(surface, item.name[:8], (rect.x + 6, rect.y + 12),
                              TEXT_COLOR, FONT_SIZE_SMALL)

        detail = previewed.summary() if previewed is not None else self.message
        renderer.text(surface, detail or "", (32, 450), ACCENT, FONT_SIZE_SMALL)
        if previewed is not None and previewed.description:
            renderer.text(surface, previewed.description, (32, 472), DIM_TEXT,
                          FONT_SIZE_SMALL)
        renderer.text(surface,
                      "Flèches déplacer   Entrée équiper / ranger   S changer de main"
                      "   I fermer", (32, 590), DIM_TEXT, FONT_SIZE_SMALL)
