"""Matematiske hjelpefunksjoner."""

import math


def normalize_angle(angle: float) -> float:
    """Normaliser vinkel til intervallet [-π, π]."""
    while angle > math.pi:
        angle -= math.tau
    while angle < -math.pi:
        angle += math.tau
    return angle


def angle_difference(a: float, b: float) -> float:
    """Korteste vinkeldifferanse mellom a og b, i [-π, π]."""
    return normalize_angle(a - b)


def lerp(a: float, b: float, t: float) -> float:
    """Lineær interpolasjon."""
    return a + (b - a) * t


def clamp(value: float, min_v: float, max_v: float) -> float:
    """Klem verdi til intervallet [min_v, max_v]."""
    return max(min_v, min(max_v, value))


def point_in_sector(px: float, py: float,
                    cx: float, cy: float,
                    angle: float, half_width: float,
                    length: float) -> bool:
    """
    Sjekk om punktet (px, py) er innenfor en sektor (lysstråle).
    Sektoren har sentrum (cx, cy), retning `angle`, halv bredde
    `half_width`, og lengde `length`.
    """
    dx = px - cx
    dy = py - cy
    dist = math.hypot(dx, dy)

    if dist > length:
        return False
    if dist < 1e-6:
        return True  # punkt i sentrum

    angle_to_point = math.atan2(dy, dx)
    diff = abs(angle_difference(angle_to_point, angle))
    return diff < half_width