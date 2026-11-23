"""The contracts the engine offers to the code written during the course.
This is the only engine file we'll open together. Everything else in
`engine/` is infrastructure the course never discusses.
"""

from abc import ABC, abstractmethod


class Renderable(ABC):
    """Anything the engine knows how to draw on screen.

    The renderer asks for four things and nothing else. It has no idea whether
    it is drawing a Barbarian, a Wizard or a goblin, and it does not care: as
    long as these four answers exist, it knows how to show the object.
    """
    @property
    @abstractmethod
    def display_name(self) -> str:
        """str: the name written under the character."""

    @property
    @abstractmethod
    def hp(self) -> int:
        """int: current hit points."""

    @property
    @abstractmethod
    def max_hp(self) -> int:
        """int: maximum hit points, used to scale the health bar."""

    @property
    @abstractmethod
    def position(self) -> tuple[int, int]:
        """tuple[int, int]: the (column, row) tile the object occupies."""
