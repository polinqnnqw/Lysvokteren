"""Partikkelsystem — for eksplosjoner, gnister og lysglød."""

import math
import random
from dataclasses import dataclass, field

import pygame

from src.settings import (
    PARTICLE_GRAVITY,
    PARTICLE_FRICTION,
    PARTICLE_DECAY_MIN,
    PARTICLE_DECAY_MAX,
    MAX_PARTICLES,
)


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    decay: float
    color: tuple
    size: float


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []

    def burst(self,
              x: float,
              y: float,
              color: tuple,
              count: int = 14,
              spread: float = 4.0) -> None:
        for _ in range(count):
            if len(self.particles) >= MAX_PARTICLES:
                break
            angle = random.uniform(0, math.tau)
            speed = random.uniform(1.0, spread)
            self.particles.append(Particle(
                x=x,
                y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed - 1.0,
                life=1.0,
                decay=random.uniform(PARTICLE_DECAY_MIN, PARTICLE_DECAY_MAX),
                color=color,
                size=random.uniform(1.0, 4.0),
            ))

    def update(self, dt: float) -> None:
        alive = []
        for p in self.particles:
            p.x += p.vx * dt * 60
            p.y += p.vy * dt * 60
            p.vy += PARTICLE_GRAVITY
            p.vx *= PARTICLE_FRICTION
            p.life -= p.decay
            if p.life > 0:
                alive.append(p)
        self.particles = alive

    def draw(self, surface: pygame.Surface) -> None:
        """Tegn partikler med additive blending for lysglød."""
        if not self.particles:
            return

        # Bruk en midlertidig alpha-surface for glød
        glow = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        for p in self.particles:
            alpha = int(max(0.0, min(1.0, p.life)) * 255)
            r = max(1, int(p.size * p.life))
            color_with_alpha = (*p.color, alpha)
            pygame.draw.circle(glow, color_with_alpha, (int(p.x), int(p.y)), r)

        surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def clear(self) -> None:
        self.particles.clear()