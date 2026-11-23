OOP - Tiny RPG game
========

A small turn-based dungeon crawler written in Python with [pygame](https://www.pygame.org/),
built using object-oriented programming.
Few in-game lines are in french because c'est mieux.

Features
--------

* Three playable classes: Barbarian (*Barbare*), Wizard (*Mage*) and Priest (*Prêtre*),
  each with its own special ability.
* Turn-based combat with initiative order, d100 hit rolls, armour and stamina
  damage reduction, and multiple attacks per round.
* Equipment slots (right hand, left hand, body), a potion belt and a backpack.
* Loot: a defeated creature hands over whatever it was carrying.
* An optional breakdown of every dice roll and damage calculation (`F1` in combat).

Requirements
------------

* Python 3.11 or newer
* [uv](https://docs.astral.sh/uv/) (recommended), or pip
* pygame 2.6.1 or newer (installed automatically)

Installation
------------

Clone the repository, then install the dependencies:

```bash
uv sync
```

Without uv:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -e .
```

Usage
-----

Start the game from the repository root:

```bash
uv run python main.py
```

`try_it.py` is a scratch script that drops a Barbarian straight onto the map,
with no character creation and no encounters:

```bash
uv run python try_it.py
```

Controls
--------

| Screen             | Key                                | Action                          |
|--------------------|------------------------------------|---------------------------------|
| Character creation | `1`–`3`                            | Pick a class                    |
|                    | Letters, `Backspace`               | Type the hero's name            |
|                    | `Enter`                            | Start the run                   |
| Map                | Arrow keys, `WASD` or `ZQSD`       | Move one tile                   |
|                    | `I`                                | Open the character sheet        |
|                    | `Esc`                              | Quit                            |
| Inventory          | Arrow keys                         | Move the cursor                 |
|                    | `Enter`                            | Equip an item, or put it away   |
|                    | `S`                                | Swap hands                      |
|                    | `I` or `Esc`                       | Close                           |
| Combat             | `1` Attack, `2` Defend, `3` Potion, `4` Special | Choose an action   |
|                    | `F1`                               | Toggle the calculation details  |
|                    | `Space` or `Enter`                 | Leave once the fight is over    |
| Game over          | `Enter` / `Esc`                    | Play again / Quit               |

Project Organization
--------------------

The code is split in two on purpose. `src/oop/engine/` is the pygame engine: it
is provided and is not part of what the course teaches. `game/` holds the
classes written during the course: characters, items, monsters and the combat
rules. The engine never imports from `game/`; the two meet in `main.py`.

```
├── main.py                 <- Entry point: wires the game rules into the engine.
├── try_it.py               <- Scratch script for quick experiments.
├── pyproject.toml          <- Project metadata and dependencies.
├── uv.lock                 <- Locked dependency versions.
│
├── game                    <- Course code: the rules and content of the game.
│   ├── entity.py           <- Entity, the abstract base of characters and items.
│   ├── character
│   │   ├── abstract.py     <- Character: stats, equipment, attack, defence.
│   │   ├── barbarian.py    <- Barbarian: rage-powered special attack.
│   │   ├── wizard.py       <- Wizard: armour-piercing attacks and spells.
│   │   └── priest.py       <- Priest: healing special ability.
│   ├── item
│   │   ├── abstract.py     <- Item, the abstract base of every item.
│   │   ├── weapon.py       <- One- and two-handed weapons.
│   │   ├── shield.py       <- Shields.
│   │   ├── armor.py        <- Body armour.
│   │   └── potion.py       <- Healing potions, carried on the belt.
│   ├── monsters.py         <- Goblin, Orc, Skeleton, Giant Rat, Troll, Skeleton Wizard.
│   ├── encounters.py       <- Which monster waits on which map tile.
│   ├── roster.py           <- The playable classes and their starting kit.
│   ├── combat.py           <- Round order, enemy AI, round resolution, loot.
│   ├── dice.py             <- Dice rolls (d6, d100, percentage chance).
│   └── constants.py        <- Game-rule constants (slot counts, bonuses).
│
└── src/oop/engine          <- Pygame engine, provided and not taught.
    ├── interfaces.py       <- Renderable: the contract the engine draws from.
    ├── window.py           <- The window, the clock and the main loop.
    ├── state.py            <- Explore, combat and game-over screens.
    ├── screens.py          <- Character creation and inventory screens.
    ├── map.py              <- The tile grid and the dungeon layout.
    ├── renderer.py         <- Drawing primitives (text, panels, health bars).
    ├── input.py            <- Keyboard mapping (QWERTY and AZERTY).
    └── constants.py        <- Window size, colours, fonts.
```
