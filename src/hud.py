"""HUD — olje-bar, poeng, liv og lys-indikator."""

import pygame

from src.settings import (
    COLOR_TEXT_DIM,
    COLOR_TIFFANY_LIGHT,
    COLOR_OIL_FULL,
    COLOR_OIL_LOW,
    MAX_OIL,
)


class HUD:
    def __init__(self, screen_w: int, screen_h: int) -> None:
        self.screen_w = screen_w
        self.screen_h = screen_h
        pygame.font.init()
        self.font_small = pygame.font.SysFont("consolas,monospace", 14, bold=True)
        self.font_label = pygame.font.SysFont("consolas,monospace", 13)
        self.font_value = pygame.font.SysFont("consolas,monospace", 26, bold=True)
        self.font_lives = pygame.font.SysFont("segoeui,arial", 26, bold=True)

    def draw(self, surface: pygame.Surface, oil: float, score: int,
             lives: int, beam_on: bool = True) -> None:
        pad = 20

        # ---- Venstre: Olje ----
        label = self.font_label.render("OLJE", True, COLOR_TEXT_DIM)
        surface.blit(label, (pad, pad))

        bar_x = pad
        bar_y = pad + 20
        bar_w = 180
        bar_h = 10

        # Bakgrunn
        pygame.draw.rect(surface, (35, 45, 60),
                         (bar_x, bar_y, bar_w, bar_h), border_radius=5)

        # Fyll
        pct = max(0.0, min(1.0, oil / MAX_OIL))
        fill_w = int(bar_w * pct)
        fill_color = COLOR_OIL_LOW if pct < 0.3 else COLOR_OIL_FULL
        if fill_w > 0:
            pygame.draw.rect(surface, fill_color,
                             (bar_x, bar_y, fill_w, bar_h), border_radius=5)

        # Prosent-tall
        pct_surf = self.font_label.render(f"{int(pct * 100)}%", True, COLOR_TEXT_DIM)
        surface.blit(pct_surf, (bar_x + bar_w + 10, bar_y - 3))

        # Indikator: LYS PÅ / LYS AV
        if beam_on:
            indicator_text = "● LYS PÅ — olje brukes"
            indicator_color = COLOR_TIFFANY_LIGHT
        else:
            indicator_text = "○ LYS AV — olje spares"
            indicator_color = (120, 140, 160)
        ind_surf = self.font_label.render(indicator_text, True, indicator_color)
        surface.blit(ind_surf, (pad, bar_y + bar_h + 8))

        # ---- Høyre: Poeng + Liv ----
        score_label = self.font_label.render("POENG", True, COLOR_TEXT_DIM)
        score_value = self.font_value.render(str(score), True, COLOR_TIFFANY_LIGHT)

        sx = self.screen_w - pad - score_value.get_width()
        surface.blit(score_label,
                     (self.screen_w - pad - score_label.get_width(), pad))
        surface.blit(score_value, (sx, pad + 18))

        # Liv (hjerter)
        hearts = "♥" * max(0, lives) + "♡" * max(0, 3 - lives)
        hearts_surf = self.font_lives.render(hearts, True, (248, 113, 113))
        hx = self.screen_w - pad - hearts_surf.get_width()
        hy = pad + 55
        surface.blit(hearts_surf, (hx, hy))