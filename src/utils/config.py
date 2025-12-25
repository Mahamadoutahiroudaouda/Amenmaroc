# src/utils/config.py
"""
CONFIGURATION GLOBALE COMPLÈTE
"""

class GlobalConfig:
    # ========== PARAMÈTRES ROBOTS ==========
    N_ROBOTS = 200  # Optimized for visual quality and performance
    ROBOT_RADIUS = 0.08
    MAX_LINEAR_VELOCITY = 0.15
    MAX_ANGULAR_VELOCITY = 2.0
    
    # ========== PARAMÈTRES ARÈNE 3D ==========
    ARENA_WIDTH = 3.2
    ARENA_HEIGHT = 2.0
    ARENA_DEPTH = 1.5  # New for 3D illusion
    SAFE_MARGIN_X = 0.2
    SAFE_MARGIN_Y = 0.15
    SAFE_MARGIN_Z = 0.1
    
    # ========== PARAMÈTRES CAMÉRA CINÉMA ==========
    CAMERA_PRESETS = {
        'travelling': {'elev': 20, 'azim': -35, 'dist': 1.8},
        'grue': {'elev': 45, 'azim': 0, 'dist': 2.2},
        'sol': {'elev': 5, 'azim': -90, 'dist': 1.5},
        'sommet': {'elev': 90, 'azim': 0, 'dist': 2.0},
        'orbital': {'elev': 30, 'azim_speed': 20} # degrees per 10s
    }
    
    @property
    def safe_zone_3d(self):
        return {
            'x_min': -self.ARENA_WIDTH/2 + self.SAFE_MARGIN_X,
            'x_max': self.ARENA_WIDTH/2 - self.SAFE_MARGIN_X,
            'y_min': -self.ARENA_HEIGHT/2 + self.SAFE_MARGIN_Y, 
            'y_max': self.ARENA_HEIGHT/2 - self.SAFE_MARGIN_Y,
            'z_min': 0,
            'z_max': self.ARENA_DEPTH - self.SAFE_MARGIN_Z
        }
    # Pauses contemplatives
    CONTEMPLATION_SHORT = 2.0   # seconds
    CONTEMPLATION_MEDIUM = 3.0  # seconds
    CONTEMPLATION_LONG = 4.0    # seconds
    
    # Transitions lumineuses
    BLACKOUT_DURATION = 0.5     # seconds
    FADEOUT_DURATION = 0.5      # seconds
    LIGHTUP_DURATION = 1.0      # seconds
    
    # Effets lumineux
    PULSE_FREQUENCY = 0.5       # Hz
    SWEEP_DURATION = 2.0        # seconds
    INTENSITY_BUILDUP = 1.5     # seconds
    
    @property
    def safe_zone(self):
        return {
            'x_min': -self.ARENA_WIDTH/2 + self.SAFE_MARGIN_X,
            'x_max': self.ARENA_WIDTH/2 - self.SAFE_MARGIN_X,
            'y_min': -self.ARENA_HEIGHT/2 + self.SAFE_MARGIN_Y, 
            'y_max': self.ARENA_HEIGHT/2 - self.SAFE_MARGIN_Y
        }
    
    # ========== PARAMÈTRES ANIMATION ==========
    FPS = 30
    DEFAULT_DURATION = 180  # 3 minutes
    
    # ## Phase 2: Core Updates
    # - [x] Update config to support 1000 robots
    # - [/] Add new letter formations (J, C, digits 0-9)
    # - [ ] Create text formation functions (JCN2026, 22EME EDITION, FES-MEKNES)
    # - [ ] Enhance flag rain animation with proper color separation
    # - [ ] Implement realistic floating flag with wave effect
    
        # ========== COULEURS ANEM OFFICIELLES ==========
    COLORS = {
        'orange_niger': '#E05206',    # Orange du drapeau
        'blanc_pure': '#FFFFFF',      # Blanc du drapeau  
        'vert_espoir': '#0DB02B',     # Vert du drapeau
        'or_soleil': '#FFD700',       # Soleil nigérien
        'bleu_profond': '#001F3F',    # Ciel nocturne
        'terre_agadez': '#8B4513',    # Terre du désert
        'turquoise': '#39CCCC',       # Eau
        'rouge_passion': '#FF4136',   # Accents
        'sable': '#F4A460',           # Sable du désert
        'ciel_bleu': '#87CEEB',       # Ciel
        'sable_sahara': '#D2B48C',    # Sable du Sahara
        'ciel_couchant': '#FF6B35',   # Orange couchant
        'nuit_violette': '#4B0082'    # Nuit désertique
    }
    
    # Nouveaux paramètres pour la carte
    GEOJSON_COORDS = {
        'niger': [
            [0.16, 11.70], [0.16, 23.53], [15.90, 23.53], [15.90, 11.70], [0.16, 11.70]
        ]
    }
    
    # ========== CHEMINS ==========
    OUTPUT_DIR = "outputs/"
    VIDEO_DIR = "outputs/videos/"

# Instance globale
config = GlobalConfig()