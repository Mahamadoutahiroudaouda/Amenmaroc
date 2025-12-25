# src/projects/project_11_naissance_nation.py
"""
PROJET #11: "NAISSANCE D'UNE NATION"
Spectacle cinématographique 3D pour l'ouverture ANEM 2025.
Drones formant le drapeau nigérien émergeant du Sahara.
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from formations.letter_formations import LetterFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project11NaissanceNation:
    """Show d'ouverture premium: Naissance d'une Nation."""
    
    def __init__(self, n_robots=100):
        self.n = n_robots
        self.base = BaseFormations(self.n)
        self.letters = LetterFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases (30 seconds each = 180s total)
        self.phases = {
            '1_desert': 30,
            '2_orange': 30,
            '3_blanc': 30,
            '4_vert': 30,
            '5_vibration': 30,
            '6_niger': 30
        }
        
        # Paramètres pour les effets
        self.n_particles = 300  # Particules de sable
        self.particles_pos = self._init_particles()
        
        print(f"🎬 PROJET #11 'NAISSANCE D'UNE NATION' INITIALISÉ: {self.n} drones")

    def _init_particles(self):
        """Initialise les particules de sable au sol."""
        x = np.random.uniform(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2, self.n_particles)
        y = np.random.uniform(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2, self.n_particles)
        z = np.random.uniform(0, 0.05, self.n_particles)
        return np.array([x, y, z])

    def update_particles(self, time_val):
        """Anime les particules de sable avec le vent."""
        # Vent souffle principalement selon X
        self.particles_pos[0] += 0.05 * np.sin(time_val * 0.5) + 0.02
        self.particles_pos[1] += 0.01 * np.cos(time_val * 0.3)
        
        # Reset les particules qui sortent
        mask = self.particles_pos[0] > config.ARENA_WIDTH/2
        self.particles_pos[0][mask] = -config.ARENA_WIDTH/2
        return self.particles_pos

    def phase_1_desert(self, duration=30):
        """0:00-0:30 - Désert vide s'animant, 100 points au sol."""
        steps = int(duration * config.FPS)
        
        # Points au sol (éparpillés)
        target_x = np.random.uniform(-0.8, 0.8, self.n)
        target_y = np.random.uniform(-0.4, 0.4, self.n)
        target_z = np.zeros(self.n)
        target_pos = np.array([target_x, target_y, target_z])
        
        for step in range(steps):
            time_val = step / config.FPS
            # Apparition progressive (0 à 100 drones)
            n_visible = int(self.n * (step / steps))
            
            positions = np.zeros((3, self.n))
            # Les drones "visibles" sont au sol
            if n_visible > 0:
                positions[:, :n_visible] = target_pos[:, :n_visible]
                
            yield positions, time_val, "Le Désert S'Éveille"

    def phase_2_orange(self, start_pos, duration=30):
        """0:30-1:00 - Émergence Orange: élévation et couleur."""
        steps = int(duration * config.FPS)
        start_time = 30
        
        # Formation: Bande supérieure (Z stable, Y haut, X étalé)
        target_x = np.linspace(-1.2, 1.2, self.n)
        target_y = np.full(self.n, 0.6)
        target_z = np.full(self.n, 0.8)
        target_pos = np.array([target_x, target_y, target_z])
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_pos, 5, 'ease_in_out')
        ):
            if step >= steps: break
            time_val = start_time + step / config.FPS
            yield positions, time_val, "Émergence Orange"

    def phase_3_blanc(self, start_pos, duration=30):
        """1:00-1:30 - Naissance du Blanc et Soleil d'Or."""
        steps = int(duration * config.FPS)
        start_time = 60
        
        # Réorganisation pour inclure la bande blanche (on divise les robots)
        n_orange = self.n // 3
        n_blanc = self.n // 3
        n_soleil = self.n // 10
        n_rest = self.n - n_orange - n_blanc - n_soleil
        
        # Target: Drapeau partiel
        tx = []
        ty = []
        tz = []
        
        # Orange reste en haut
        tx.extend(np.linspace(-1.2, 1.2, n_orange))
        ty.extend(np.full(n_orange, 0.6))
        tz.extend(np.full(n_orange, 0.8))
        
        # Blanc au centre
        tx.extend(np.linspace(-1.2, 1.2, n_blanc))
        ty.extend(np.full(n_blanc, 0.0))
        tz.extend(np.full(n_blanc, 0.8))
        
        # Soleil au centre
        angles = np.linspace(0, 2*np.pi, n_soleil)
        tx.extend(0.15 * np.cos(angles))
        ty.extend(0.15 * np.sin(angles))
        tz.extend(np.full(n_soleil, 0.81)) # Légèrement devant
        
        # Le reste attend au sol ou rejoint le blanc
        tx.extend(np.linspace(-1.2, 1.2, n_rest))
        ty.extend(np.full(n_rest, 0.0))
        tz.extend(np.full(n_rest, 0.8))
        
        target_pos = np.array([tx, ty, tz])
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_pos, 5, 'ease_in_out')
        ):
            if step >= steps: break
            time_val = start_time + step / config.FPS
            yield positions, time_val, "Paix Blanche & Soleil d'Or"

    def phase_4_vert(self, start_pos, duration=30):
        """1:30-2:00 - Verdure de l'Espoir: Drapeau Complet."""
        steps = int(duration * config.FPS)
        start_time = 90
        
        n_bande = self.n // 3
        n_soleil = 12
        n_side = (self.n - n_soleil) // 3
        
        tx, ty, tz = [], [], []
        
        # Bande Orange
        tx.extend(np.linspace(-1.2, 1.2, n_side))
        ty.extend(np.full(n_side, 0.6))
        tz.extend(np.full(n_side, 0.8))
        
        # Bande Blanche
        tx.extend(np.linspace(-1.2, 1.2, n_side))
        ty.extend(np.full(n_side, 0.0))
        tz.extend(np.full(n_side, 0.8))
        
        # Bande Verte
        tx.extend(np.linspace(-1.2, 1.2, n_side))
        ty.extend(np.full(n_side, -0.6))
        tz.extend(np.full(n_side, 0.8))
        
        # Soleil (précis)
        angles = np.linspace(0, 2*np.pi, n_soleil)
        tx.extend(0.2 * np.cos(angles))
        ty.extend(0.2 * np.sin(angles))
        tz.extend(np.full(n_soleil, 0.82))
        
        # Ajuster pour arriver à N
        while len(tx) < self.n:
            tx.append(0); ty.append(-0.6); tz.append(0.8)
            
        target_pos = np.array([tx[:self.n], ty[:self.n], tz[:self.n]])
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_pos, 5, 'ease_in_out')
        ):
            if step >= steps: break
            time_val = start_time + step / config.FPS
            yield positions, time_val, "Espoir Vert - Drapeau National"

    def phase_5_vibration(self, start_pos, duration=30):
        """2:00-2:30 - Drapeau qui vit (ondulations)."""
        steps = int(duration * config.FPS)
        start_time = 120
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = start_pos.copy()
            
            # Effet d'ondulation (Wave)
            wave_amp = 0.05
            wave_freq = 2.0
            for i in range(self.n):
                # Ondulation selon Z basée sur X et le temps
                positions[2, i] += wave_amp * np.sin(wave_freq * positions[0, i] + time_val * 3)
                # Légère dérive Y
                positions[1, i] += 0.01 * np.cos(time_val * 2 + i * 0.1)
                
            yield positions, time_val, "Le Souffle de la Nation"

    def phase_6_niger(self, start_pos, duration=30):
        """2:30-3:00 - Transformation en 'NIGER'."""
        steps = int(duration * config.FPS)
        start_time = 150
        
        # Utiliser LetterFormations pour N-I-G-E-R
        target_pos_2d = self.letters.get_NIGER_formation()
        # Convertir en 3D (Z = 1.0 pour être proche de la caméra)
        target_pos = np.zeros((3, self.n))
        target_pos[0:2, :target_pos_2d.shape[1]] = target_pos_2d
        target_pos[2, :] = 1.0
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_pos, 8, 'ease_in_out')
        ):
            if step >= steps: break
            time_val = start_time + step / config.FPS
            
            # Pulsation finale
            pulse = 1.0 + 0.05 * np.sin(time_val * 4)
            positions[0:2, :] *= pulse
            
            yield positions, time_val, "NIGER - Éternel"

    def get_drone_color(self, phase_name, time_val, index, pos):
        """Calcule la couleur dynamique pour un drone spécifique."""
        # Logique de couleur basée sur la position et la phase
        
        # 1. Couleurs de base du drapeau pour les phases 2 à 5
        if 'orange' in phase_name.lower():
            return config.COLORS['orange_niger']
        
        if 'blanc' in phase_name.lower() or 'drapeau' in phase_name.lower() or 'souffle' in phase_name.lower():
            y = pos[1]
            # Détection de la bande par position Y
            if y > 0.3: return config.COLORS['orange_niger']
            if y < -0.3: return config.COLORS['vert_espoir']
            
            # Soleil au centre
            dist_center = np.sqrt(pos[0]**2 + pos[1]**2)
            if dist_center < 0.25 and abs(pos[2] - 0.8) > 0.01: # Si c'est le soleil (Z décalé)
                return config.COLORS['or_soleil']
                
            return config.COLORS['blanc_pure']
            
        if 'niger' in phase_name.lower():
            # Dégradé sur les lettres
            x = pos[0]
            if x < -0.6: return config.COLORS['orange_niger']
            if x < 0.2: return config.COLORS['blanc_pure']
            return config.COLORS['vert_espoir']

        # Par défaut (Désert / Phase 1)
        return config.COLORS['sable_sahara']

    def run_complete_animation(self):
        """Générateur principal pour l'animation complète."""
        current_pos = None
        frame = 0
        
        # Phase 1
        for pos, t, name in self.phase_1_desert():
            current_pos = pos
            yield pos, name, t, frame
            frame += 1
            
        # Phase 2
        for pos, t, name in self.phase_2_orange(current_pos):
            current_pos = pos
            yield pos, name, t, frame
            frame += 1
            
        # Phase 3
        for pos, t, name in self.phase_3_blanc(current_pos):
            current_pos = pos
            yield pos, name, t, frame
            frame += 1
            
        # Phase 4
        for pos, t, name in self.phase_4_vert(current_pos):
            current_pos = pos
            yield pos, name, t, frame
            frame += 1
            
        # Phase 5
        for pos, t, name in self.phase_5_vibration(current_pos):
            current_pos = pos
            yield pos, name, t, frame
            frame += 1
            
        # Phase 6
        for pos, t, name in self.phase_6_niger(current_pos):
            current_pos = pos
            yield pos, name, t, frame
            frame += 1
