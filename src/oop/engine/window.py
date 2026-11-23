"""The window, the clock and the main loop.

Internal engine code. The loop itself never asks what is happening in the
game: it forwards events to the current state, tells it to update and to draw,
and flips the frame. Everything that differs between exploring and fighting
lives in the states, not here.
"""

import pygame

from oop.engine.constants import BG_COLOR, FPS, TITLE, WINDOW_SIZE


class Game:
    """The running game: one window, one clock, one current state."""

    def __init__(self, size=WINDOW_SIZE):
        """Open the window and get the clock going.

        Args:
            size (tuple): (width, height) in pixels.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = None

        # Replaced at the seam, in `oop/main.py`: the engine has no idea how a
        # new run is built, only that something can build one.
        self.new_game = lambda: None

    def change_state(self, state):
        """Swap the state the loop is driving.

        Args:
            state (GameState): the screen taking over.
        """
        self.current_state = state

    def quit(self):
        """Ask the main loop to stop at the end of this frame."""
        self.running = False

    def run(self, state=None):
        """Drive the game until the window is closed.

        Args:
            state (GameState | None): the screen to start on. Handy from
                module 5, where a run is one state and nothing else yet.
        """
        if state is not None:
            self.change_state(state)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_state is not None:
                    self.current_state.handle_event(event)

            if not self.running:
                break

            if self.current_state is not None:
                self.current_state.update()
            self.screen.fill(BG_COLOR)
            if self.current_state is not None:
                self.current_state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
