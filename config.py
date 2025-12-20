# src/utils/config.py
"""
CONFIGURATION GLOBALE COMPLÈTE
"""

class GlobalConfig:
    # ========== PARAMÈTRES ROBOTS ==========
    N_ROBOTS = 50
    ROBOT_RADIUS = 0.08
    MAX_LINEAR_VELOCITY = 0.15
    MAX_ANGULAR_VELOCITY = 2.0
    
    # ========== PARAMÈTRES ARÈNE ==========
    ARENA_WIDTH = 3.2
    ARENA_HEIGHT = 2.0
    SAFE_MARGIN_X = 0.2
    SAFE_MARGIN_Y = 0.15
    
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
        'ciel_bleu': '#87CEEB'        # Ciel
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