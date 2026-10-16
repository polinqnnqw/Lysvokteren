"""Fyrtårn og lysstråle."""

import math
import pygame

from src.settings import (
    BEAM_WIDTH,
    BEAM_LENGTH,
    BEAM_ROTATION_SPEED,
    COLOR_BEAM_CORE,
    COLOR_BEAM_OUTER,
    COLOR_GLASS,
    COLOR_TIFFANY,
    WATER_LEVEL,
    LIGHTHOUSE_OFFSET_Y,
)
from src.utils import angle_difference


class Lighthouse:
    def __init__(self, screen_w: int, screen_h: int) -> None:
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.base_y = screen_h * WATER_LEVEL
        self.x = screen_w / 2
        self.y = self.base_y - min(180, screen_h * LIGHTHOUSE_OFFSET_Y)

        self.angle = -math.pi / 2
        self.target_angle = -math.pi / 2
        self.beam_on = True
        self.beam_intensity = 1.0

    def update(self, dt: float, target_pos: tuple | None) -> None:
        if target_pos is not None:
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            self.target_angle = math.atan2(dy, dx)
        else:
            t = pygame.time.get_ticks() / 1000.0
            self.target_angle = -math.pi / 2 + math.sin(t * 0.7) * 0.9

        diff = angle_difference(self.target_angle, self.angle)
        self.angle += diff * min(1.0, dt * BEAM_ROTATION_SPEED)

        # Intensity returnerer til normal
        self.beam_intensity += (1.0 - self.beam_intensity) * dt * 4

    def point_in_beam(self, px: float, py: float) -> bool:
        if not self.beam_on:
            return False
        dx = px - self.x
        dy = py - self.y
        dist = math.hypot(dx, dy)
        if dist > BEAM_LENGTH:
            return False
        angle_to = math.atan2(dy, dx)
        diff = abs(angle_difference(angle_to, self.angle))
        return diff < BEAM_WIDTH / 2

    def draw_beam(self, surface: pygame.Surface) -> None:
        if not self.beam_on:
            return

        half = BEAM_WIDTH / 2
        inten = self.beam_intensity

        # Bygg beam på egen surface med alpha, så blend additive
        beam_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        cx, cy = self.x, self.y

        # Ytre stråle
        outer_alpha = int(80 * inten)
        outer_pts = [(cx, cy)]
        steps = 24
        for i in range(steps + 1):
            a = self.angle - half + (2 * half) * (i / steps)
            outer_pts.append((cx + math.cos(a) * BEAM_LENGTH,
                              cy + math.sin(a) * BEAM_LENGTH))
        pygame.draw.polygon(beam_surf, (*COLOR_BEAM_OUTER, outer_alpha), outer_pts)

        # Kjerne (smalere)
        core_alpha = int(160 * inten)
        core_half = half * 0.35
        core_pts = [(cx, cy)]
        for i in range(steps + 1):
            a = self.angle - core_half + (2 * core_half) * (i / steps)
            core_pts.append((cx + math.cos(a) * BEAM_LENGTH,
                             cy + math.sin(a) * BEAM_LENGTH))
        pygame.draw.polygon(beam_surf, (*COLOR_BEAM_CORE, core_alpha), core_pts)

        # Midtlinje
        end_x = cx + math.cos(self.angle) * BEAM_LENGTH
        end_y = cy + math.sin(self.angle) * BEAM_LENGTH
        pygame.draw.line(beam_surf, (255, 255, 255, int(40 * inten)),
                         (cx, cy), (end_x, end_y), 2)

        surface.blit(beam_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def draw_tower(self, surface: pygame.Surface) -> None:
        lx = self.x
        ly = self.y
        by = self.base_y

        # Base
        pygame.draw.ellipse(surface, (10, 15, 24),
                            (lx - 70, by - 12, 140, 36))
        pygame.draw.ellipse(surface, (5, 8, 16),
                            (lx - 90, by + 2, 180, 24))

        # Tårn
        tower_w = 26
        tower_h = by - ly
        tower_pts = [
            (lx - tower_w / 2, by),
            (lx - tower_w / 2 + 6, ly),
            (lx + tower_w / 2 - 6, ly),
            (lx + tower_w / 2, by),
        ]
        pygame.draw.polygon(surface, (30, 41, 59), tower_pts)

        # Stripene
        for i in range(4):
            y1 = ly + (tower_h / 4) * i + tower_h / 8
            t = (y1 - ly) / tower_h
            w = tower_w - t * 10
            pygame.draw.rect(surface, (226, 232, 240),
                             (lx - w / 2, y1, w, 6))

        # Lykt
        pygame.draw.rect(surface, (15, 23, 42), (lx - 12, ly - 8, 24, 12))

        # Glassglød
        glow = 1.0 if self.beam_on else 0.3
        glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        for r in range(28, 0, -3):
            a = int((1 - r / 28) * 100 * glow)
            pygame.draw.circle(glow_surf, (*COLOR_BEAM_OUTER, a), (30, 30), r)
        surface.blit(glow_surf, (int(lx - 30), int(ly - 30)),
                     special_flags=pygame.BLEND_RGBA_ADD)

        pygame.draw.circle(surface, COLOR_GLASS,
                           (int(lx), int(ly - 2)),
                           int(5 * glow + 2))

        # Tak
        pygame.draw.polygon(surface, (15, 23, 42), [
            (lx - 14, ly - 8),
            (lx, ly - 22),
            (lx + 14, ly - 8),
        ])