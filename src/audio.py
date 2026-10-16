"""
Lyd syntetisert i sanntid med numpy + pygame.
Ingen eksterne lydfiler — alt genereres ved oppstart.
import pygame


"""

import numpy as np
import pygame

SAMPLE_RATE = 44100


def _generate_tone(freq: float,
                   duration: float,
                   wave: str = "sine",
                   volume: float = 0.5,
                   slide_to: float | None = None) -> pygame.mixer.Sound:
    """Generer en enkelt tone som pygame Sound."""
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    if slide_to is not None:
        freq_curve = np.linspace(freq, slide_to, n_samples)
        phase = 2 * np.pi * np.cumsum(freq_curve) / SAMPLE_RATE
    else:
        phase = 2 * np.pi * freq * t

    if wave == "sine":
        samples = np.sin(phase)
    elif wave == "square":
        samples = np.sign(np.sin(phase))
    elif wave == "sawtooth":
        samples = 2 * (phase / (2 * np.pi) - np.floor(0.5 + phase / (2 * np.pi)))
    elif wave == "triangle":
        samples = 2 * np.abs(2 * (phase / (2 * np.pi) - np.floor(0.5 + phase / (2 * np.pi)))) - 1
    else:
        samples = np.sin(phase)

    # Envelope (attack + decay)
    attack = int(n_samples * 0.01)
    release = int(n_samples * 0.6)
    env = np.ones(n_samples)
    if attack > 0:
        env[:attack] = np.linspace(0, 1, attack)
    if release > 0:
        env[-release:] = np.linspace(1, 0, release)

    samples = samples * env * volume

    # Konverter til 16-bit stereo
    samples_int = (samples * 32767).astype(np.int16)
    stereo = np.column_stack((samples_int, samples_int))
    return pygame.sndarray.make_sound(stereo)


class AudioManager:
    """Holder alle lyder og spiller dem av."""

    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
            pygame.mixer.init()
            self._build_sounds()
        except pygame.error:
            self.enabled = False

    def _build_sounds(self):
        self.snd_good = _generate_tone(660, 0.18, "sine", 0.35)
        self.snd_good_2 = _generate_tone(990, 0.22, "sine", 0.30)

        self.snd_bad = _generate_tone(180, 0.35, "sawtooth", 0.45, slide_to=80)
        self.snd_miss = _generate_tone(300, 0.25, "triangle", 0.30, slide_to=200)

        self.snd_start = _generate_tone(330, 0.15, "sine", 0.35)
        self.snd_start_2 = _generate_tone(660, 0.30, "sine", 0.35)

        self.snd_over_1 = _generate_tone(440, 0.40, "sine", 0.35)
        self.snd_over_2 = _generate_tone(330, 0.40, "sine", 0.35)
        self.snd_over_3 = _generate_tone(220, 0.50, "sine", 0.35)
        self.snd_over_4 = _generate_tone(165, 0.70, "sine", 0.40)

    def _play(self, sound):
        if self.enabled and sound is not None:
            sound.play()

    def play_good(self):
        self._play(self.snd_good)
        pygame.time.set_timer(pygame.USEREVENT + 1, 80, loops=1)

    def play_good_2(self):
        self._play(self.snd_good_2)

    def play_bad(self):
        self._play(self.snd_bad)

    def play_miss(self):
        self._play(self.snd_miss)

    def play_start(self):
        self._play(self.snd_start)
        pygame.time.set_timer(pygame.USEREVENT + 2, 100, loops=1)

    def play_start_2(self):
        self._play(self.snd_start_2)

    def play_game_over(self):
        self._play(self.snd_over_1)
        pygame.time.set_timer(pygame.USEREVENT + 3, 180, loops=1)
        pygame.time.set_timer(pygame.USEREVENT + 4, 360, loops=1)
        pygame.time.set_timer(pygame.USEREVENT + 5, 540, loops=1)

    def play_game_over_steps(self, step: int):
        if step == 2:
            self._play(self.snd_over_2)
        elif step == 3:
            self._play(self.snd_over_3)
        elif step == 4:
            self._play(self.snd_over_4)