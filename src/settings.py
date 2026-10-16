"""
Alle konstanter og konfigurasjon for Lysvokteren.
Endre her for å justere balanse, farger og ytelse.
"""

# ============ VINDU ============
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Lysvokteren — En reise gjennom tåken"
FPS = 60

# ============ FARGER ============
# Bakgrunn
COLOR_SKY_TOP = (4, 7, 15)
COLOR_SKY_MID = (10, 26, 47)
COLOR_SKY_BOT = (15, 42, 69)
COLOR_WATER_TOP = (10, 26, 42)
COLOR_WATER_BOT = (2, 5, 9)

# Tiffany & Svart-palett (fra tidligere prosjekt)
COLOR_TIFFANY = (45, 212, 191)
COLOR_TIFFANY_LIGHT = (94, 234, 212)
COLOR_TIFFANY_DARK = (14, 116, 144)

# Lys / beam
COLOR_BEAM_CORE = (255, 255, 240)
COLOR_BEAM_OUTER = (253, 224, 71)
COLOR_GLASS = (254, 243, 199)

# Skip
COLOR_FRIEND = (16, 185, 129)
COLOR_FRIEND_DARK = (6, 95, 70)
COLOR_ENEMY = (220, 38, 38)
COLOR_ENEMY_DARK = (127, 29, 29)

# UI
COLOR_TEXT = (234, 246, 255)
COLOR_TEXT_DIM = (100, 116, 139)
COLOR_TEXT_MID = (148, 163, 184)
COLOR_WHITE = (255, 255, 255)
COLOR_OIL_FULL = (251, 191, 36)
COLOR_OIL_LOW = (248, 113, 113)
COLOR_STAR = (224, 242, 254)

# ============ MAYAK (LIGHTHOUSE) ============
BEAM_WIDTH = 0.42           # radianer (total bredde)
BEAM_LENGTH = 900           # piksler
BEAM_ROTATION_SPEED = 12.0  # hvor raskt strålen følger mus
LIGHTHOUSE_OFFSET_Y = 0.28  # hvor høyt over vannet (andel av H)
WATER_LEVEL = 0.66          # hvor vannet starter (andel av H)

# ============ SPILLBALANSE ============
STARTING_LIVES = 3
STARTING_OIL = 100.0
MAX_OIL = 100.0

OIL_DRAIN_BASE = 3.5        # per sekund
OIL_DRAIN_DIFFICULTY = 0.4  # ekstra per difficulty-nivå
OIL_REWARD_FRIEND = 25.0    # belønning for å lyse opp venn
OIL_PENALTY_ENEMY = 25.0    # straff for å lyse opp fiende

SCORE_FRIEND = 200
SCORE_ENEMY_MISSED = 100    # bonus for å la fiende passere
SCORE_ENEMY_HIT = -150      # straff for å lyse fiende

DIFFICULTY_GROWTH = 0.045   # per sekund
SPAWN_BASE = 2.0            # sekunder mellom skip ved difficulty=1
SPAWN_MIN = 0.7             # aldri raskere enn dette
SPAWN_ENEMY_CHANCE_BASE = 0.22
SPAWN_ENEMY_CHANCE_MAX = 0.45
SPAWN_ENEMY_CHANCE_GROWTH = 0.06

SHIP_SPEED_BASE = 0.045     # andel av skjermbredde per sekund
SHIP_SPEED_DIFFICULTY = 0.012
SHIP_WIDTH = 60
SHIP_HEIGHT = 26

# ============ PARTIKLER ============
PARTICLE_GRAVITY = 0.12
PARTICLE_FRICTION = 0.98
PARTICLE_DECAY_MIN = 0.012
PARTICLE_DECAY_MAX = 0.032

# ============ YTELSE ============
MAX_PARTICLES = 400
NUM_STARS = 120
NUM_AURORA_LAYERS = 3