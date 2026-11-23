"""Drawing primitives.

Internal engine code. Everything the game shows is a rectangle, a circle or a
line of text — no sprite sheets, no animation system.

The one idea worth noticing is `draw_actor`: it accepts anything that answers
the four questions of the `Renderable` contract. It never asks what class it
has been handed.
"""

import pygame

from oop.engine.constants import (ACCENT, CURSOR_COLOR, DIM_TEXT, FONT_SIZE,
                                  FONT_SIZE_BIG,
                                  FONT_SIZE_SMALL, HERO_COLOR, HP_BACK,
                                  HP_GOOD, HP_LOW, PANEL_COLOR, PANEL_EDGE,
                                  SLOT_COLOR, SLOT_EDGE, TEXT_COLOR)

_fonts = {}


def font(size=FONT_SIZE, bold=False):
    """Return a cached font. Built-in only, so there is no asset to ship.

    Args:
        size (int): point size.
        bold (bool): whether to ask for the bold face.

    Returns:
        pygame.font.Font: a ready-to-use font.
    """
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.Font(None, size)
        _fonts[key].set_bold(bold)
    return _fonts[key]


def text(surface, message, position, color=TEXT_COLOR, size=FONT_SIZE,
         bold=False, center=False):
    """Blit one line of text and return the rectangle it occupied.

    Args:
        surface (pygame.Surface): where to draw.
        message (str): the line to write.
        position (tuple): (x, y) — the top-left, or the centre if `center`.
        color (tuple): RGB.
        size (int): point size.
        bold (bool): bold face.
        center (bool): treat `position` as the centre of the line.

    Returns:
        pygame.Rect: the area written to.
    """
    image = font(size, bold).render(str(message), True, color)
    rect = image.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    surface.blit(image, rect)
    return rect


def panel(surface, rect, title=None):
    """Draw a framed panel, optionally with a title on its top edge.

    Args:
        surface (pygame.Surface): where to draw.
        rect (tuple | pygame.Rect): the panel bounds.
        title (str | None): a heading drawn over the top-left corner.

    Returns:
        pygame.Rect: the panel bounds, as a Rect.
    """
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, PANEL_COLOR, rect, border_radius=6)
    pygame.draw.rect(surface, PANEL_EDGE, rect, width=1, border_radius=6)
    if title:
        text(surface, title, (rect.x + 12, rect.y + 8), ACCENT,
             FONT_SIZE_SMALL, bold=True)
    return rect


def health_bar(surface, rect, current, maximum):
    """Draw a health bar scaled by `current / maximum`.

    Args:
        surface (pygame.Surface): where to draw.
        rect (tuple | pygame.Rect): the full-health bounds.
        current (int): hit points left.
        maximum (int): hit points at full health.
    """
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, HP_BACK, rect, border_radius=3)
    share = max(0.0, min(1.0, current / maximum)) if maximum else 0.0
    if share > 0:
        filled = pygame.Rect(rect.x, rect.y, int(rect.width * share), rect.height)
        color = HP_GOOD if share > 0.35 else HP_LOW
        pygame.draw.rect(surface, color, filled, border_radius=3)


def draw_actor(surface, actor, center, radius=16, with_name=True, color=None):
    """Draw anything that satisfies the `Renderable` contract.

    This function is the whole argument of module 5. It reads `display_name`,
    `hp` and `max_hp` and draws them. It has no idea whether it was handed a
    Barbarian, a goblin or something written after it was.

    Args:
        surface (pygame.Surface): where to draw.
        actor (Renderable): the thing to show.
        center (tuple): (x, y) of the token's centre.
        radius (int): token radius in pixels.
        with_name (bool): draw the name and health bar under the token.
        color (tuple | None): override the token colour. Creatures have none
            of their own, so the combat screen tints them from here.
    """
    color = color or getattr(actor, "color", HERO_COLOR)
    pygame.draw.circle(surface, color, center, radius)
    pygame.draw.circle(surface, PANEL_EDGE, center, radius, width=1)
    if not with_name:
        return
    x, y = center
    text(surface, actor.display_name, (x, y + radius + 12), TEXT_COLOR,
         FONT_SIZE_SMALL, center=True)
    health_bar(surface, (x - radius - 8, y + radius + 22, 2 * (radius + 8), 5),
               actor.hp, actor.max_hp)


def slot(surface, rect, label=None, item=None, selected=False):
    """Draw one inventory or equipment cell.

    Args:
        surface (pygame.Surface): where to draw.
        rect (tuple | pygame.Rect): the cell bounds.
        label (str | None): a caption drawn above the cell.
        item (Item | None): what sits in it.
        selected (bool): whether the cursor is on it.

    Returns:
        pygame.Rect: the cell bounds, as a Rect.
    """
    rect = pygame.Rect(rect)
    if label:
        text(surface, label, (rect.x, rect.y - 18), DIM_TEXT, FONT_SIZE_SMALL)
    pygame.draw.rect(surface, SLOT_COLOR, rect, border_radius=4)
    pygame.draw.rect(surface, CURSOR_COLOR if selected else SLOT_EDGE, rect,
                     width=2 if selected else 1, border_radius=4)
    if item is not None:
        text(surface, item.name, (rect.x + 8, rect.centery - 8), TEXT_COLOR,
             FONT_SIZE_SMALL)
    return rect


def title(surface, message, y, color=TEXT_COLOR):
    """Centre a big heading across the window at height `y`."""
    return text(surface, message, (surface.get_width() // 2, y), color,
                FONT_SIZE_BIG, bold=True, center=True)
