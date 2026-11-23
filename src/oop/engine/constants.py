"""Geometry and palette for the whole window.

Internal engine code. Nothing here is taught: it exists so that no other file
has to hardcode a pixel or a colour.
"""

# --- window -------------------------------------------------------------

WINDOW_SIZE = (960, 640)
FPS = 60
TITLE = "La Horde"

# --- map ----------------------------------------------------------------

TILE = 48
MAP_ORIGIN = (32, 96)

# --- palette ------------------------------------------------------------

BG_COLOR = (18, 18, 24)
PANEL_COLOR = (28, 29, 38)
PANEL_EDGE = (58, 60, 74)
WALL_COLOR = (24, 25, 32)
FLOOR_COLOR = (52, 55, 70)
FLOOR_EDGE = (66, 70, 88)

TEXT_COLOR = (226, 228, 236)
DIM_TEXT = (138, 142, 158)
ACCENT = (206, 174, 92)
DEBUG_TEXT = (128, 176, 148)

HERO_COLOR = (198, 84, 58)
ENEMY_COLOR = (170, 74, 92)
HP_GOOD = (104, 168, 116)
HP_LOW = (196, 92, 72)
HP_BACK = (52, 54, 66)

CURSOR_COLOR = (206, 174, 92)
SLOT_COLOR = (40, 42, 54)
SLOT_EDGE = (62, 64, 78)

# --- type ---------------------------------------------------------------

FONT_SIZE = 18
FONT_SIZE_SMALL = 15
FONT_SIZE_BIG = 34
LINE_HEIGHT = 22
