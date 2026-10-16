"""Skip som seiler i hele farvannet med dybde-perspektiv."""

import math
import random
from enum import Enum

import pygame

from src.settings import (
    COLOR_FRIEND, COLOR_FRIEND_DARK,
    COLOR_ENEMY, COLOR_ENEMY_DARK,
    COLOR_TIFFANY_LIGHT, COLOR_TEXT_DIM,
    SHIP_WIDTH, SHIP_HEIGHT,
    SHIP_SPEED_BASE, SHIP_SPEED_DIFFICULTY,
)


class ShipType(Enum):
    FRIEND = "friend"
    ENEMY = "enemy"


class Ship:
    """
    Skip i 2D-farvann.
      x: piksler horisontalt
      z: dybde 0..1  (0 = horisonten, 1 = nederst på skjermen)
    Skala og skjerm-y regnes ut fra z.
    """

    def __init__(self, ship_type, screen_w, screen_h, water_y, difficulty):
        self.type = ship_type
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.water_y = water_y
        self.water_h = max(1.0, screen_h - water_y)

        base_speed = SHIP_SPEED_BASE + difficulty * SHIP_SPEED_DIFFICULTY
        speed_px = base_speed * screen_w * random.uniform(0.85, 1.15)

        edge = random.choices(
            ["left", "right", "horizon", "bottom"],
            weights=[35, 35, 20, 10],
        )[0]

        if edge == "left":
            self.x = -60.0
            self.z = random.uniform(0.15, 0.9)
            angle = random.uniform(-0.35, 0.35)
        elif edge == "right":
            self.x = screen_w + 60.0
            self.z = random.uniform(0.15, 0.9)
            angle = math.pi + random.uniform(-0.35, 0.35)
        elif edge == "horizon":
            self.x = random.uniform(80, screen_w - 80)
            self.z = -0.05
            angle = math.pi / 2 + random.uniform(-0.55, 0.55)
        else:  # bottom
            self.x = random.uniform(80, screen_w - 80)
            self.z = 1.05
            angle = -math.pi / 2 + random.uniform(-0.55, 0.55)

        self.vx = math.cos(angle) * speed_px
        vy_px = math.sin(angle) * speed_px
        self.vz = vy_px / self.water_h

        self.w = SHIP_WIDTH
        self.h = SHIP_HEIGHT
        self.bobbing = random.uniform(0, math.tau)
        self.illuminated = False
        self.resolved = False
        self.wake = []

    # --- Skjermrom ---
    @property
    def screen_y(self) -> float:
        return self.water_y + self.z * self.water_h

    @property
    def scale(self) -> float:
        """0.45 (langt borte) → 1.30 (helt nære)."""
        return 0.45 + self.z * 0.85

    @property
    def is_friend(self) -> bool:
        return self.type == ShipType.FRIEND

    @property
    def is_enemy(self) -> bool:
        return self.type == ShipType.ENEMY

    # --- Oppdatering ---
    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.z += self.vz * dt
        self.bobbing += dt * 3.0

        # Kjølvann (sjelden, for ytelse)
        if random.random() < dt * 8:
            direction = 1 if self.vx > 0 else -1
            self.wake.append({
                "x": self.x - direction * self.w * self.scale / 2,
                "y": self.screen_y + 4 * self.scale,
                "life": 1.0,
                "scale": self.scale,
            })

        alive = []
        for w in self.wake:
            w["life"] -= dt * 0.9
            if w["life"] > 0:
                alive.append(w)
        self.wake = alive

    def is_off_screen(self) -> bool:
        return (self.x < -160 or self.x > self.screen_w + 160
                or self.z < -0.25 or self.z > 1.25)

    # --- Tegning ---
    def draw(self, surface: pygame.Surface) -> None:
        s = self.scale
        bob = math.sin(self.bobbing) * 2 * s
        x = self.x
        y = self.screen_y + bob
        w = self.w * s

        # Kjølvann
        for wk in self.wake:
            alpha = int(wk["life"] * 0.45 * 255)
            radius = max(1, int((1 - wk["life"]) * 10 * wk["scale"] + 2))
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*COLOR_TEXT_DIM, alpha),
                               (radius, radius), radius)
            surface.blit(surf, (int(wk["x"] - radius), int(wk["y"] - radius)))

        hull = COLOR_FRIEND if self.is_friend else COLOR_ENEMY
        hull_dark = COLOR_FRIEND_DARK if self.is_friend else COLOR_ENEMY_DARK

        # Skrog
        pygame.draw.polygon(surface, hull, [
            (x - w / 2,          y - 4 * s),
            (x + w / 2,          y - 4 * s),
            (x + w / 2 - 8 * s,  y + 8 * s),
            (x - w / 2 + 8 * s,  y + 8 * s),
        ])
        pygame.draw.rect(surface, hull_dark,
                         (x - w / 2, y - 4 * s, w, max(1, 2 * s)))

        # Kahyt
        pygame.draw.rect(surface, (30, 41, 59),
                         (x - 8 * s, y - 14 * s, 16 * s, 10 * s))

        # Flagg / lanterne
        if self.is_friend:
            pygame.draw.rect(surface, COLOR_TIFFANY_LIGHT,
                             (x - 2 * s, y - 22 * s, 2 * s, 8 * s))
            flag = COLOR_TIFFANY_LIGHT if self.resolved else (251, 191, 36)
            pygame.draw.polygon(surface, flag, [
                (x,             y - 22 * s),
                (x + 8 * s,     y - 19 * s),
                (x,             y - 16 * s),
            ])
        else:
            pygame.draw.circle(surface, (248, 113, 113),
                               (int(x), int(y - 18 * s)), max(2, int(3 * s)))
            pygame.draw.rect(surface, COLOR_ENEMY_DARK,
                             (x - 2 * s, y - 15 * s, 4 * s, 5 * s))

        # Glød når opplyst
        if self.illuminated:
            gr = int(60 * s)
            glow = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
            base = COLOR_TIFFANY_LIGHT if self.is_friend else (248, 113, 113)
            for r in range(gr, 0, -4):
                a = int((1 - r / gr) * 70)
                pygame.draw.circle(glow, (*base, a), (gr, gr), r)
            surface.blit(glow, (int(x - gr), int(y - gr)),
                         special_flags=pygame.BLEND_RGBA_ADD)