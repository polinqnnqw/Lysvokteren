"""Hovedklasse — game loop, state, input, rendering."""

import math
import random

import pygame

from src.settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLOR_TEXT_MID,
    COLOR_TIFFANY,
    COLOR_TIFFANY_LIGHT,
    COLOR_FRIEND,
    COLOR_ENEMY,
    COLOR_WHITE,
    STARTING_LIVES,
    STARTING_OIL,
    MAX_OIL,
    OIL_DRAIN_BASE,
    OIL_DRAIN_DIFFICULTY,
    OIL_REWARD_FRIEND,
    OIL_PENALTY_ENEMY,
    SCORE_FRIEND,
    SCORE_ENEMY_MISSED,
    SCORE_ENEMY_HIT,
    DIFFICULTY_GROWTH,
    SPAWN_BASE,
    SPAWN_MIN,
    SPAWN_ENEMY_CHANCE_BASE,
    SPAWN_ENEMY_CHANCE_MAX,
    SPAWN_ENEMY_CHANCE_GROWTH,
)
from src.audio import AudioManager
from src.hud import HUD
from src.lighthouse import Lighthouse
from src.particles import ParticleSystem
from src.ship import Ship, ShipType
from src.world import World


class GameState:
    MENU = "menu"
    PLAY = "play"
    OVER = "over"


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.w = WINDOW_WIDTH
        self.h = WINDOW_HEIGHT

        self.audio = AudioManager()
        self.world = World(self.w, self.h)
        self.lighthouse = Lighthouse(self.w, self.h)
        self.particles = ParticleSystem()
        self.hud = HUD(self.w, self.h)

        self.font_h1 = pygame.font.SysFont("segoeui,arial", 72, bold=True)
        self.font_h2 = pygame.font.SysFont("segoeui,arial", 28)
        self.font_body = pygame.font.SysFont("segoeui,arial", 18)
        self.font_small = pygame.font.SysFont("consolas,monospace", 14)

        self.state = GameState.MENU
        self.pointer_pos: tuple | None = None

        # Spilldata
        self.ships: list[Ship] = []
        self.score = 0
        self.best = self._load_best()
        self.lives = STARTING_LIVES
        self.oil = STARTING_OIL
        self.time_played = 0.0
        self.difficulty = 1.0
        self.spawn_timer = 1.5
        self.shake = 0.0
        self.flash = 0.0
        self.game_over_step = 0
        self.over_timer = 0.0

    # ---------- Input ----------
    def handle_keydown(self, key: int) -> None:
        if self.state == GameState.PLAY:
            if key == pygame.K_SPACE:
                self.lighthouse.beam_on = not self.lighthouse.beam_on
        elif self.state in (GameState.MENU, GameState.OVER):
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()

    def handle_mousemove(self, pos: tuple) -> None:
        self.pointer_pos = pos

    def handle_click(self, pos: tuple) -> None:
        if self.state in (GameState.MENU, GameState.OVER):
            self.start_game()

    # ---------- Game state ----------
    def start_game(self) -> None:
        self.state = GameState.PLAY
        self.score = 0
        self.lives = STARTING_LIVES
        self.oil = STARTING_OIL
        self.time_played = 0.0
        self.difficulty = 1.0
        self.spawn_timer = 1.5
        self.ships.clear()
        self.particles.clear()
        self.lighthouse.beam_on = True
        self.lighthouse.angle = -math.pi / 2
        self.lighthouse.target_angle = -math.pi / 2
        self.shake = 0.0
        self.flash = 0.0
        self.game_over_step = 0
        self.audio.play_start()

    def end_game(self) -> None:
        self.state = GameState.OVER
        self.over_timer = 0.0
        if self.score > self.best:
            self.best = self.score
            self._save_best()
        self.audio.play_game_over()

    def _load_best(self) -> int:
        try:
            with open(".lysvokteren_best", "r") as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            return 0

    def _save_best(self) -> None:
        try:
            with open(".lysvokteren_best", "w") as f:
                f.write(str(self.best))
        except OSError:
            pass

    # ---------- Update ----------
    def update(self, dt: float) -> None:
        self.world.update(dt)

        # Timing-events (delayed audio)
        for event_id, step in [
            (pygame.USEREVENT + 1, 2),
            (pygame.USEREVENT + 2, "start2"),
            (pygame.USEREVENT + 3, 2),
            (pygame.USEREVENT + 4, 3),
            (pygame.USEREVENT + 5, 4),
        ]:
            for ev in pygame.event.get(event_id):
                if ev.type == event_id:
                    if step == "start2":
                        self.audio.play_start_2()
                    else:
                        self.audio.play_game_over_steps(step)

        if self.state != GameState.PLAY:
            self.over_timer += dt
            self._decay_effects(dt)
            return

        self.time_played += dt
        self.difficulty = 1.0 + self.time_played * DIFFICULTY_GROWTH

        # Olje brukes bare når lyset faktisk er på
        if self.lighthouse.beam_on:
            self.oil -= dt * (OIL_DRAIN_BASE + self.difficulty * OIL_DRAIN_DIFFICULTY)

        # Oppdater fyr
        self.lighthouse.update(dt, self.pointer_pos)

        # Spawn
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._spawn_ship()
            base = max(SPAWN_MIN, SPAWN_BASE - self.difficulty * 0.11)
            self.spawn_timer = base * (0.7 + random.random() * 0.8)

        # Oppdater skip
        for s in self.ships:
            s.update(dt)
            s.illuminated = self.lighthouse.point_in_beam(s.x, s.screen_y)

            if s.illuminated and not s.resolved:
                if s.is_friend:
                    self.score += SCORE_FRIEND
                    self.oil = min(MAX_OIL, self.oil + OIL_REWARD_FRIEND)
                    self.lighthouse.beam_intensity = 1.6
                    self.particles.burst(s.x, s.screen_y,
                                         COLOR_TIFFANY_LIGHT, 22, 5)
                    self.audio.play_good()
                else:
                    self.score = max(0, self.score + SCORE_ENEMY_HIT)
                    self.oil -= OIL_PENALTY_ENEMY
                    self.shake = 14.0
                    self.flash = 0.5
                    self.particles.burst(s.x, s.screen_y,
                                         COLOR_ENEMY, 26, 6)
                    self.audio.play_bad()
                s.resolved = True

        # Skip som går av skjermen
        remaining = []
        for s in self.ships:
            if s.is_off_screen():
                if not s.resolved:
                    if s.is_friend:
                        self.lives -= 1
                        self.shake = 8.0
                        self.audio.play_miss()
                        burst_x = 20 if s.x < self.w / 2 else self.w - 20
                        self.particles.burst(burst_x, s.screen_y,
                                             COLOR_TEXT_MID, 18, 5)
                    else:
                        self.score += SCORE_ENEMY_MISSED
            else:
                remaining.append(s)
        self.ships = remaining

        self.particles.update(dt)
        self._decay_effects(dt)

        if self.oil <= 0 or self.lives <= 0:
            self.end_game()

    def _decay_effects(self, dt: float) -> None:
        self.lighthouse.beam_intensity += (1.0 - self.lighthouse.beam_intensity) * dt * 4
        self.shake *= math.pow(0.001, dt)
        self.flash *= math.pow(0.01, dt)

    def _spawn_ship(self) -> None:
        enemy_chance = min(
            SPAWN_ENEMY_CHANCE_MAX,
            SPAWN_ENEMY_CHANCE_BASE + self.difficulty * SPAWN_ENEMY_CHANCE_GROWTH,
        )
        ship_type = ShipType.ENEMY if random.random() < enemy_chance else ShipType.FRIEND
        self.ships.append(
            Ship(ship_type, self.w, self.h, self.world.water_y, self.difficulty)
        )

    # ---------- Render ----------
    def render(self) -> None:
        # Shake
        shake_x = 0
        shake_y = 0
        if self.shake > 0.5:
            shake_x = int((random.random() - 0.5) * self.shake)
            shake_y = int((random.random() - 0.5) * self.shake)

        # Tegn på midlertidig surface for shake
        scene = pygame.Surface((self.w, self.h))
        self.world.draw(scene, self.lighthouse.x)

        # Skip — bakerst først, nærmest sist
        for s in sorted(self.ships, key=lambda sh: sh.z):
            s.draw(scene)

        self.lighthouse.draw_tower(scene)
        self.lighthouse.draw_beam(scene)
        self.particles.draw(scene)

        # Flash (rød)
        if self.flash > 0.01:
            flash_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            flash_surf.fill((248, 113, 113, int(self.flash * 90)))
            scene.blit(flash_surf, (0, 0))

        # Vignette
        self._draw_vignette(scene)

        self.screen.fill((0, 0, 0))
        self.screen.blit(scene, (shake_x, shake_y))

        # HUD
        if self.state == GameState.PLAY:
            self.hud.draw(self.screen, self.oil, self.score, self.lives,
                          self.lighthouse.beam_on)

        # Overlays
        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.OVER:
            self._draw_game_over()

    def _draw_vignette(self, surface: pygame.Surface) -> None:
        vignette = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        cx, cy = self.w // 2, self.h // 2
        max_r = int(math.hypot(cx, cy))
        min_r = int(max_r * 0.35)
        for r in range(max_r, min_r, -4):
            t = (r - min_r) / (max_r - min_r)
            alpha = int(180 * (t ** 2))
            pygame.draw.circle(vignette, (0, 0, 0, alpha), (cx, cy), r, width=4)
        surface.blit(vignette, (0, 0))

    def _draw_menu(self) -> None:
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((2, 5, 12, 200))
        self.screen.blit(overlay, (0, 0))

        title = self.font_h1.render("LYSVOKTEREN", True, COLOR_TIFFANY_LIGHT)
        sub = self.font_h2.render("En reise gjennom tåken", True, (125, 211, 252))

        intro_lines = [
            "Du er vokteren av det siste fyrtårnet i fjorden.",
            "Skipene seiler i mørket — noen er venner, noen er fiender.",
            "Bruk lysstrålen klokt, og spar på oljen.",
        ]
        intro_surfs = [self.font_body.render(line, True, COLOR_TEXT_MID)
                       for line in intro_lines]

        legend_lines = [
            ("● Venne-skip — må lyses opp", COLOR_FRIEND),
            ("● Fiendtlige — må IKKE lyses", COLOR_ENEMY),
        ]
        legend_surfs = [(self.font_body.render(txt, True, col), col)
                        for txt, col in legend_lines]

        btn_text = self.font_h2.render("Begynn reisen", True, (2, 16, 24))

        y = self.h * 0.18
        self.screen.blit(title, title.get_rect(center=(self.w // 2, y)))
        y += 70
        self.screen.blit(sub, sub.get_rect(center=(self.w // 2, y)))
        y += 60
        for s in intro_surfs:
            self.screen.blit(s, s.get_rect(center=(self.w // 2, y)))
            y += 26
        y += 20
        for s, _ in legend_surfs:
            self.screen.blit(s, s.get_rect(center=(self.w // 2, y)))
            y += 26
        y += 40

        btn_w, btn_h = 280, 60
        btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
        btn_rect.center = (self.w // 2, y)
        pygame.draw.rect(self.screen, COLOR_TIFFANY, btn_rect, border_radius=30)
        self.screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        hint = self.font_small.render(
            "Beveg musen for å styre lyset  ·  MELLOMROM slår lyset av/på",
            True, (100, 116, 139),
        )
        self.screen.blit(hint, hint.get_rect(center=(self.w // 2, self.h - 40)))

    def _draw_game_over(self) -> None:
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((2, 5, 12, 215))
        self.screen.blit(overlay, (0, 0))

        if self.lives <= 0:
            title_text = "Skipene gikk tapt"
            msg_text = "For mange venner fant ikke veien gjennom tåken."
        else:
            title_text = "Oljen tok slutt"
            msg_text = "Fyrtårnet sluknet. Fjorden ble stille."

        title = self.font_h1.render(title_text, True, COLOR_TIFFANY_LIGHT)
        msg = self.font_h2.render(msg_text, True, COLOR_TEXT_MID)

        score_label = self.font_small.render("POENG", True, COLOR_TEXT_DIM)
        score_val = self.font_h1.render(str(self.score), True, COLOR_TIFFANY_LIGHT)
        best_label = self.font_body.render(f"Beste: {self.best}",
                                           True, COLOR_TEXT_MID)

        btn_text = self.font_h2.render("Prøv igjen", True, (2, 16, 24))

        y = self.h * 0.20
        self.screen.blit(title, title.get_rect(center=(self.w // 2, y)))
        y += 70
        self.screen.blit(msg, msg.get_rect(center=(self.w // 2, y)))
        y += 90
        self.screen.blit(score_label, score_label.get_rect(center=(self.w // 2, y)))
        y += 40
        self.screen.blit(score_val, score_val.get_rect(center=(self.w // 2, y)))
        y += 70
        self.screen.blit(best_label, best_label.get_rect(center=(self.w // 2, y)))
        y += 60

        btn_w, btn_h = 260, 60
        btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
        btn_rect.center = (self.w // 2, y)
        pygame.draw.rect(self.screen, COLOR_TIFFANY, btn_rect, border_radius=30)
        self.screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))