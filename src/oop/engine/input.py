"""Keyboard decoding.

Internal engine code. One place decides that both the arrows and WASD/ZQSD
mean "walk", so no screen has to repeat the list.

There is no mouse handling anywhere in the engine, by design: the combat menu
is driven by the number keys, which keeps the dispatch students write in
module 6 a plain `if choice == 1`, not hit-testing.
"""

import pygame

# Every key that means "walk one tile", in the four directions. QWERTY and
# AZERTY both work without the player changing anything.
MOVEMENT = {
    pygame.K_UP: (0, -1),    pygame.K_w: (0, -1),  pygame.K_z: (0, -1),
    pygame.K_DOWN: (0, 1),   pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),  pygame.K_a: (-1, 0),  pygame.K_q: (-1, 0),
    pygame.K_RIGHT: (1, 0),  pygame.K_d: (1, 0),
}

# The combat menu. Both the number row and the keypad.
MENU_CHOICE = {
    pygame.K_1: 1, pygame.K_KP1: 1,
    pygame.K_2: 2, pygame.K_KP2: 2,
    pygame.K_3: 3, pygame.K_KP3: 3,
    pygame.K_4: 4, pygame.K_KP4: 4,
}

CONFIRM = (pygame.K_RETURN, pygame.K_KP_ENTER)
CLOSE = (pygame.K_i, pygame.K_ESCAPE)
DEBUG = (pygame.K_F1,)


def direction(event):
    """Return the (dx, dy) a key event asks for, or None.

    Args:
        event (pygame.event.Event): a KEYDOWN event.

    Returns:
        tuple | None: the step to take, or None if the key means something
        else.
    """
    return MOVEMENT.get(event.key)


def menu_choice(event):
    """Return the combat menu number a key event asks for, or None."""
    return MENU_CHOICE.get(event.key)


def is_text(event):
    """Say whether an event carries a printable character to type.

    Args:
        event (pygame.event.Event): a KEYDOWN event.

    Returns:
        bool: True when `event.unicode` can go into a name field.
    """
    return bool(event.unicode) and event.unicode.isprintable()
