"""Bakgrunn: nordlys, stjerner, måne, fjell med snø, vann og tåke."""

import math
import random

import pygame

from src.settings import (
    COLOR_SKY_TOP, COLOR_SKY_MID, COLOR_SKY_BOT,
    COLOR_WATER_TOP, COLOR_WATER_BOT,
    COLOR_STAR, COLOR_TIFFANY,
    WATER_LEVEL, NUM_STARS,
)


class Star:
    def __init__(self, w, max_y):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, max_y)
        self.r = random.uniform(0.4, 1.6)
        self.twinkle = random.uniform(0, math.tau)
        self.speed = random.uniform(0.4, 1.6)
        # Litt fargevariasjon: noen blå, noen gule, de fleste hvite
        r = random.random()
        if r < 0.15:
            self.color = (200, 220, 255)
        elif r < 0.30:
            self.color = (255, 240, 200)
        else:
            self.color = COLOR_STAR


class World:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.water_y = screen_h * WATER_LEVEL
        self.time = 0.0

        # Pre-render himmel og vann
        self.sky_surface = pygame.Surface((screen_w, int(self.water_y)))
        self._build_sky()
        self.water_surface = pygame.Surface((screen_w, screen_h - int(self.water_y)))
        self._build_water()

        # Stjerner
        self.stars = [Star(screen_w, int(self.water_y * 0.85))
                      for _ in range(NUM_STARS)]

        # Måne
        self.moon_x = screen_w * 0.82
        self.moon_y = self.water_y * 0.22

        # Fjell-lag (bakerst → forrest)
        self.mountain_far = self._make_mountain_layer(
            num_peaks=9, base_h=140, variation=45, color=(15, 25, 45), snow=True)
        self.mountain_mid = self._make_mountain_layer(
            num_peaks=11, base_h=90, variation=35, color=(10, 18, 32))
        self.mountain_near = self._make_mountain_layer(
            num_peaks=13, base_h=55, variation=25, color=(5, 10, 20))

    # ---------- Oppsett ----------
    def _build_sky(self):
        h = self.sky_surface.get_height()
        for y in range(h):
            t = y / h
            if t < 0.5:
                c = self._lerp_color(COLOR_SKY_TOP, COLOR_SKY_MID, t * 2)
            else:
                c = self._lerp_color(COLOR_SKY_MID, COLOR_SKY_BOT, (t - 0.5) * 2)
            pygame.draw.line(self.sky_surface, c, (0, y), (self.screen_w, y))

    def _build_water(self):
        h = self.water_surface.get_height()
        for y in range(h):
            t = y / max(1, h)
            c = self._lerp_color(COLOR_WATER_TOP, COLOR_WATER_BOT, t ** 0.7)
            pygame.draw.line(self.water_surface, c, (0, y), (self.screen_w, y))

    def _make_mountain_layer(self, num_peaks, base_h, variation, color,
                             snow=False):
        surf = pygame.Surface((self.screen_w, int(self.water_y)),
                              pygame.SRCALPHA)
        step = self.screen_w / num_peaks

        # Bygg fjelltopper
        peaks = []
        for i in range(num_peaks + 1):
            h = (base_h
                 + math.sin(i * 1.7) * variation
                 + math.cos(i * 0.9) * (variation * 0.7)
                 + math.sin(i * 3.1) * (variation * 0.3))
            peaks.append((i * step, self.water_y - max(10, h)))

        # Fyll fjellene
        points = [(0, self.water_y)] + peaks + [(self.screen_w, self.water_y)]
        pygame.draw.polygon(surf, color, points)

        # Snø på toppene
        if snow:
            for i in range(1, len(peaks) - 1):
                px, py = peaks[i]
                # Bare hvis toppen er «høy nok»
                if py < self.water_y - base_h * 0.7:
                    snow_pts = [
                        (px - 18, py + 22),
                        (px, py),
                        (px + 18, py + 22),
                        (px + 10, py + 18),
                        (px, py + 26),
                        (px - 10, py + 18),
                    ]
                    pygame.draw.polygon(surf, (210, 225, 240, 180), snow_pts)

        return surf

    @staticmethod
    def _lerp_color(a, b, t):
        return (
            int(a[0] + (b[0] - a[0]) * t),
            int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t),
        )

    # ---------- Oppdatering ----------
    def update(self, dt):
        self.time += dt

    # ---------- Tegning ----------
    def draw(self, surface, lighthouse_x):
        # Himmel
        surface.blit(self.sky_surface, (0, 0))

        # Stjerner
        self._draw_stars(surface)

        # Måne
        self._draw_moon(surface)

        # Nordlys (over himmelen, bak fjellene)
        self._draw_aurora(surface)

        # Fjell — bakerst til forrest
        surface.blit(self.mountain_far, (0, 0))
        surface.blit(self.mountain_mid, (0, 0))
        surface.blit(self.mountain_near, (0, 0))

        # Vann
        surface.blit(self.water_surface, (0, int(self.water_y)))

        # Horisont-glød (der himmel møter vann)
        self._draw_horizon_glow(surface)

        # Refleksjon fra fyrtårnet
        self._draw_water_reflection(surface, lighthouse_x)

        # Tåke
        self._draw_fog(surface)

    def _draw_stars(self, surface):
        for s in self.stars:
            tw = 0.5 + 0.5 * math.sin(self.time * s.speed + s.twinkle)
            alpha = int(tw * 230)
            if alpha < 15:
                continue
            r = max(1, int(s.r))
            temp = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(temp, (*s.color, alpha),
                               (r + 1, r + 1), r)
            surface.blit(temp, (int(s.x - r - 1), int(s.y - r - 1)))

    def _draw_moon(self, surface):
        mx, my = int(self.moon_x), int(self.moon_y)

        # Glød rundt månen
        glow = pygame.Surface((140, 140), pygame.SRCALPHA)
        for r in range(70, 0, -3):
            a = int((1 - r / 70) * 40)
            pygame.draw.circle(glow, (220, 230, 255, a), (70, 70), r)
        surface.blit(glow, (mx - 70, my - 70),
                     special_flags=pygame.BLEND_RGBA_ADD)

        # Måneskive
        pygame.draw.circle(surface, (240, 245, 255), (mx, my), 20)
        # Krater-skygger
        pygame.draw.circle(surface, (215, 222, 235), (mx - 5, my - 4), 6)
        pygame.draw.circle(surface, (220, 226, 240), (mx + 7, my + 3), 4)
        pygame.draw.circle(surface, (225, 230, 242), (mx + 2, my + 8), 3)

    def _draw_aurora(self, surface):
        """Vennlige, vandrende bånd av grønt/blått lys."""
        h = int(self.water_y * 0.75)
        aurora = pygame.Surface((self.screen_w, h), pygame.SRCALPHA)

        bands = [
            {"y": 0.30, "h": 70,  "amp": 26, "freq": 0.006,
             "color": (60, 240, 200), "alpha": 32, "speed": 0.30},
            {"y": 0.42, "h": 85,  "amp": 36, "freq": 0.009,
             "color": (80, 220, 235), "alpha": 26, "speed": -0.22},
            {"y": 0.55, "h": 60,  "amp": 22, "freq": 0.005,
             "color": (120, 200, 250), "alpha": 20, "speed": 0.42},
        ]

        for band in bands:
            y_center = h * band["y"]
            top_pts = []
            bot_pts = []
            step = 12
            for x in range(-10, self.screen_w + 10, step):
                off = (math.sin(x * band["freq"] + self.time * band["speed"])
                       * band["amp"])
                off += (math.sin(x * band["freq"] * 2.3
                                 - self.time * band["speed"] * 0.6)
                        * band["amp"] * 0.4)
                top_pts.append((x, y_center + off - band["h"] / 2))
                bot_pts.append((x, y_center + off + band["h"] / 2))

            # Fyll med vertikale strimler og gradient-alpha
            for i in range(len(top_pts) - 1):
                x0, y0 = top_pts[i]
                x1, y1 = bot_pts[i]
                top_y = int(min(y0, y1))
                bot_y = int(max(y0, y1))
                if top_y < 0:
                    top_y = 0
                if bot_y > h:
                    bot_y = h
                # Alpha avtar mot midten av båndet for «courtain»-effekt
                mid = (top_y + bot_y) / 2
                half = max(1, (bot_y - top_y) / 2)
                for y in range(top_y, bot_y, 2):
                    t = abs(y - mid) / half           # 0 = midten, 1 = kant
                    fade = 1 - t                       # mest lys i midten
                    a = int(band["alpha"] * fade)
                    if a <= 0:
                        continue
                    pygame.draw.line(aurora, (*band["color"], a),
                                     (x0, y), (x0 + step, y), 2)

        surface.blit(aurora, (0, 0))

    def _draw_horizon_glow(self, surface):
        """Myk glød akkurat der himmelen møter vannet."""
        glow_h = 30
        glow = pygame.Surface((self.screen_w, glow_h * 2), pygame.SRCALPHA)
        for y in range(glow_h * 2):
            t = abs(y - glow_h) / glow_h
            a = int((1 - t) * 60)
            if a <= 0:
                continue
            pygame.draw.line(glow, (80, 200, 220, a),
                             (0, y), (self.screen_w, y))
        surface.blit(glow, (0, int(self.water_y) - glow_h),
                     special_flags=pygame.BLEND_RGBA_ADD)

    def _draw_water_reflection(self, surface, lx):
        """Fyrtårnets refleksjon i vannet — vandrende striper."""
        refl = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        for i in range(28):
            y = self.water_y + 10 + i * 6
            off = math.sin(self.time * 0.6 + i * 0.7) * 22
            width = 60 - i * 1.4
            if width < 6:
                break
            a = max(0, int(28 - i * 1.0))
            pygame.draw.line(refl, (*COLOR_TIFFANY, a),
                             (lx - width + off, y),
                             (lx + width + off, y), 1)
        surface.blit(refl, (0, 0))

    def _draw_fog(self, surface):
        fog_amount = min(0.55, 0.15 + self.time * 0.008)
        h = 200
        fog = pygame.Surface((self.screen_w, h), pygame.SRCALPHA)
        for y in range(h):
            t = abs(y - h / 2) / (h / 2)
            a = int(fog_amount * 42 * (1 - t))
            if a > 0:
                pygame.draw.line(fog, (148, 163, 184, a),
                                 (0, y), (self.screen_w, y))
        surface.blit(fog, (0, int(self.water_y) - h // 2))