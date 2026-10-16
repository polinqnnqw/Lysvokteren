"""
Lysvokteren — et atmosfærisk arcade-spill.
Entry point. Kjør: python main.py
"""

import sys
import pygame

from src.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS
from src.game import Game


def main() -> int:
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)  # cap for stability

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    game.handle_keydown(event.key)
            elif event.type == pygame.MOUSEMOTION:
                game.handle_mousemove(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

        game.update(dt)
        game.render()

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())