# src/projects/project_01_anem_lumiere.py
"""
PROJET #1: NAISSANCE D'UNE NATION (CINÉMATIQUE 3D)
Spectacle d'ouverture en 6 phases : Tempête -> Couleur -> Drapeau -> NIGER 3D
"""

import numpy as np
from formations.letter_formations import LetterFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project01AnemLumiere:
    """Implémentation du Tableau #1: Naissance d'une Nation avec illusion 3D."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.letters = LetterFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Structure en 6 phases (30s chacune = 3 minutes)
        self.phases = {
            '1_tempête_sable': 30,
            '2_émergence_vert': 30,
            '3_émergence_blanc': 30,
            '4_formation_soleil': 30,
            '5_drapeau_ondulant': 30,
            '6_niger_3d': 30
        }
        
        print(f"🎬 PROJET #1: NAISSANCE D'UNE NATION (3D)")
        print(f"   Drones: {self.n}")
        print(f"   Durée totale: {sum(self.phases.values())}s")

    def _get_z_positions(self, x, y, time_val, effect_type='flat'):
        """Génère la composante Z pour l'illusion 3D."""
        if effect_type == 'storm':
            return 0.5 + 0.3 * np.random.randn(self.n) # Particules en l'air
        elif effect_type == 'wave':
            return 0.1 * np.sin(x * 2 + time_val * 3) # Ondulation drapeau
        return np.zeros(self.n)

    def phase_1_tempête_sable(self, duration=30):
        """Phase 1: Tempête de sable orange (0:00-0:30)."""
        steps = int(duration * config.FPS)
        for step in range(steps):
            time_val = step / config.FPS
            # Mouvement chaotique dans l'espace
            x = np.random.uniform(-1.6, 1.6, self.n)
            y = np.random.uniform(-1.0, 1.0, self.n)
            z = self._get_z_positions(x, y, time_val, 'storm')
            
            yield np.array([x, y, z]), time_val

    def phase_2_émergence_vert(self, start_pos, duration=30):
        """Phase 2: Émergence bande verte (0:30-1:00)."""
        # Cible: Tiers bas de l'arène
        target_x = np.linspace(-1.3, 1.3, self.n)
        target_y = np.linspace(-0.6, -0.3, self.n)
        target_z = np.zeros(self.n)
        target = np.array([target_x, target_y, target_z])
        
        start_time = self.phases['1_tempête_sable']
        for step, pos in enumerate(self.transitions.interpolate_positions(start_pos[:2], target[:2], duration)):
            time_val = start_time + step / config.FPS
            z = self._get_z_positions(pos[0], pos[1], time_val, 'flat')
            yield np.array([pos[0], pos[1], z]), time_val

    def phase_3_émergence_blanc(self, start_pos, duration=30):
        """Phase 3: Apparition bande blanche (1:00-1:30)."""
        target_x = np.linspace(-1.3, 1.3, self.n)
        target_y = np.linspace(-0.3, 0.3, self.n)
        target_z = np.zeros(self.n)
        target = np.array([target_x, target_y, target_z])
        
        start_time = self.phases['1_tempête_sable'] + self.phases['2_émergence_vert']
        for step, pos in enumerate(self.transitions.interpolate_positions(start_pos[:2], target[:2], duration)):
            time_val = start_time + step / config.FPS
            z = self._get_z_positions(pos[0], pos[1], time_val, 'flat')
            yield np.array([pos[0], pos[1], z]), time_val

    def phase_4_formation_soleil(self, start_pos, duration=30):
        """Phase 4: Formation soleil central (1:30-2:00)."""
        from formations.base_formations import BaseFormations
        base = BaseFormations(self.n)
        target_2d = base.circle(radius=0.2, center=(0, 0))
        target = np.vstack([target_2d, np.zeros(self.n)])
        
        start_time = sum(list(self.phases.values())[:3])
        for step, pos in enumerate(self.transitions.interpolate_positions(start_pos[:2], target[:2], duration)):
            time_val = start_time + step / config.FPS
            z = 0.1 * np.cos(time_val * 4) # Pulsation en Z
            yield np.array([pos[0], pos[1], z]), time_val

    def phase_5_drapeau_ondulant(self, start_pos, duration=30):
        """Phase 5: Drapeau complet qui ondule (2:00-2:30)."""
        grid_width = int(np.sqrt(self.n * 1.5))
        grid_height = self.n // grid_width
        x = np.linspace(-1.3, 1.3, grid_width)
        y = np.linspace(-0.6, 0.6, grid_height)
        xx, yy = np.meshgrid(x, y)
        target_2d = np.array([xx.flatten()[:self.n], yy.flatten()[:self.n]])
        
        start_time = sum(list(self.phases.values())[:4])
        for step, pos in enumerate(self.transitions.interpolate_positions(start_pos[:2], target_2d, duration)):
            time_val = start_time + step / config.FPS
            z = self._get_z_positions(pos[0], pos[1], time_val, 'wave')
            yield np.array([pos[0], pos[1], z]), time_val

    def phase_6_niger_3d(self, start_pos, duration=30):
        """Phase 6: Transformation en NIGER 3D (2:30-3:00)."""
        target_niger = self.letters.get_NIGER_formation()
        
        start_time = sum(list(self.phases.values())[:5])
        for step, pos in enumerate(self.transitions.interpolate_positions(start_pos[:2], target_niger, duration)):
            time_val = start_time + step / config.FPS
            # On soulève les lettres pour la 3D
            z = 0.3 + 0.2 * np.sin(pos[0] * 3 + time_val)
            yield np.array([pos[0], pos[1], z]), time_val

    def run_complete_animation(self):
        """Exécute l'animation complète."""
        current_pos = None
        frame_count = 0
        
        # Phase 1
        for pos, t in self.phase_1_tempête_sable(self.phases['1_tempête_sable']):
            current_pos = pos
            yield pos, "Tempête de Sable", t, frame_count
            frame_count += 1
            
        # Phases 2 à 6
        phase_methods = [
            (self.phase_2_émergence_vert, "Émergence Vert"),
            (self.phase_3_émergence_blanc, "Apparition Blanc"),
            (self.phase_4_formation_soleil, "Formation Soleil"),
            (self.phase_5_drapeau_ondulant, "Drapeau Ondulant"),
            (self.phase_6_niger_3d, "NIGER 3D")
        ]
        
        for method, label in phase_methods:
            phase_duration = self.phases[f"{phase_methods.index((method, label))+2}_{label.lower().replace(' ', '_')}"] if f"{phase_methods.index((method, label))+2}_{label.lower().replace(' ', '_')}" in self.phases else 30
            # Correction index pour les clés de phases
            phase_key = [k for k in self.phases.keys() if label.lower().replace(' ', '_') in k][0]
            for pos, t in method(current_pos, self.phases[phase_key]):
                current_pos = pos
                yield pos, label, t, frame_count
                frame_count += 1